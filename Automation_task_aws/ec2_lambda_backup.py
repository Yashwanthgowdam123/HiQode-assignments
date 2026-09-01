import os
import time
import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError

# AWS Clients
ec2 = boto3.client("ec2")
s3 = boto3.client("s3")
sns = boto3.client("sns")

# Environment Variables
TAG1_KEY = os.environ["TAG1_KEY"]
TAG1_VALUE = os.environ["TAG1_VALUE"]
TAG2_KEY = os.environ["TAG2_KEY"]
TAG2_VALUE = os.environ["TAG2_VALUE"]

S3_BUCKET = os.environ.get("S3_BUCKET", "ec2-backup-automation")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:003344631245:EC2-Backup-Notifications")
RETENTION_LIMIT = int(os.environ.get("SNAPSHOT_RETENTION", 3))


def ami_exists(instance_id):
    response = ec2.describe_images(
        Owners=["self"],
        Filters=[
            {"Name": "tag:SourceInstance", "Values": [instance_id]},
            {"Name": "state", "Values": ["available", "pending"]}
        ]
    )
    return len(response["Images"]) > 0


def get_name_tag(tags):
    if not tags:
        return None
    for tag in tags:
        if tag["Key"] == "Name":
            return tag["Value"]
    return None


def create_snapshot_with_retry(volume_id, instance_id, max_retries=3):
    """Creates a snapshot with exponential backoff if throttled by AWS rate limits."""
    # Check if a pending snapshot already exists for this volume
    pending_snaps = ec2.describe_snapshots(
        OwnerIds=["self"],
        Filters=[
            {"Name": "volume-id", "Values": [volume_id]},
            {"Name": "status", "Values": ["pending"]}
        ]
    )
    
    if len(pending_snaps.get("Snapshots", [])) > 0:
        return None, "Skipped: A snapshot is already currently in progress for this volume."

    delay = 2
    for attempt in range(max_retries):
        try:
            snapshot = ec2.create_snapshot(
                VolumeId=volume_id,
                Description=f"Snapshot-{instance_id}",
                TagSpecifications=[{
                    "ResourceType": "snapshot",
                    "Tags": [
                        {"Key": "SourceInstance", "Value": instance_id},
                        {"Key": "VolumeId", "Value": volume_id},
                        {"Key": TAG1_KEY, "Value": TAG1_VALUE},
                        {"Key": TAG2_KEY, "Value": TAG2_VALUE}
                    ]
                }]
            )
            return snapshot['SnapshotId'], None
        except ClientError as e:
            if e.response['Error']['Code'] == 'SnapshotCreationPerVolumeRateExceeded':
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                else:
                    return None, f"Failed: {e.response['Error']['Message']}"
            else:
                raise e


def cleanup_old_snapshots(instance_id, logs_list, notification_list):
    """Retains only the latest N snapshots for a target instance, deleting older ones."""
    response = ec2.describe_snapshots(
        OwnerIds=["self"],
        Filters=[
            {"Name": f"tag:{TAG1_KEY}", "Values": [TAG1_VALUE]},
            {"Name": f"tag:{TAG2_KEY}", "Values": [TAG2_VALUE]},
            {"Name": "tag:SourceInstance", "Values": [instance_id]}
        ]
    )
    
    snapshots = response.get("Snapshots", [])
    snapshots.sort(key=lambda x: x["StartTime"], reverse=True)
    
    if len(snapshots) > RETENTION_LIMIT:
        snapshots_to_delete = snapshots[RETENTION_LIMIT:]
        for snap in snapshots_to_delete:
            snap_id = snap["SnapshotId"]
            time_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            
            try:
                ec2.delete_snapshot(SnapshotId=snap_id)
                log_entry = f"<resource_id: {snap_id}> | <action: Deleted Old Snapshot> | <time: {time_str}> | <source_instance: {instance_id}>"
                logs_list.append(log_entry)
                notification_list.append(log_entry)
            except ClientError as e:
                log_entry = f"<resource_id: {snap_id}> | <action: Delete Failed - {e.response['Error']['Code']}> | <time: {time_str}>"
                logs_list.append(log_entry)


def send_sns_notification(notifications):
    if not notifications:
        return
    
    message = "EC2 Backup & Cleanup Report\n" + "="*40 + "\n" + "\n".join(notifications)
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="EC2 Backup & Cleanup Automation Report",
        Message=message
    )


def upload_logs_to_s3(logs):
    if not logs:
        return
    
    timestamp = datetime.now(timezone.utc).strftime("%Y/%m/%d/backup-log-%H%M%S.log")
    log_content = "\n".join(logs)
    
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f"logs/{timestamp}",
        Body=log_content
    )


def lambda_handler(event, context):
    response = ec2.describe_instances(
        Filters=[
            {"Name": f"tag:{TAG1_KEY}", "Values": [TAG1_VALUE]},
            {"Name": f"tag:{TAG2_KEY}", "Values": [TAG2_VALUE]},
            {"Name": "instance-state-name", "Values": ["running"]}
        ]
    )

    count = 0
    logs = []
    notifications = []

    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instance_id = instance["InstanceId"]
            time_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

            # ---------------------------------------------------
            # 1. Create AMI (Only Once)
            # ---------------------------------------------------
            if ami_exists(instance_id):
                log_entry = f"<resource_id: {instance_id}> | <action: AMI Exists Skipped> | <time: {time_str}>"
                logs.append(log_entry)
            else:
                instance_name = get_name_tag(instance.get("Tags", []))
                base_name = instance_name if instance_name else instance_id
                ami_name = f"{base_name}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

                ami = ec2.create_image(
                    InstanceId=instance_id,
                    Name=ami_name,
                    NoReboot=True,
                    TagSpecifications=[{
                        "ResourceType": "image",
                        "Tags": [
                            {"Key": "SourceInstance", "Value": instance_id},
                            {"Key": TAG1_KEY, "Value": TAG1_VALUE},
                            {"Key": TAG2_KEY, "Value": TAG2_VALUE}
                        ]
                    }]
                )
                ami_id = ami['ImageId']
                log_entry = f"<resource_id: {ami_id}> | <action: Created AMI> | <time: {time_str}> | <source_instance: {instance_id}>"
                logs.append(log_entry)
                notifications.append(log_entry)

            # ---------------------------------------------------
            # 2. Root Volume Snapshot
            # ---------------------------------------------------
            root_volume = instance["BlockDeviceMappings"][0]["Ebs"]["VolumeId"]
            snap_id, err_msg = create_snapshot_with_retry(root_volume, instance_id)

            if snap_id:
                log_entry = f"<resource_id: {snap_id}> | <action: Created Snapshot> | <time: {time_str}> | <source_instance: {instance_id}> | <volume: {root_volume}>"
                logs.append(log_entry)
                notifications.append(log_entry)
            else:
                log_entry = f"<resource_id: {root_volume}> | <action: Snapshot Skipped/Failed> | <time: {time_str}> | <details: {err_msg}>"
                logs.append(log_entry)

            # ---------------------------------------------------
            # 3. Snapshot Retention Cleanup (Keep 3 latest)
            # ---------------------------------------------------
            cleanup_old_snapshots(instance_id, logs, notifications)

            count += 1

    upload_logs_to_s3(logs)
    send_sns_notification(notifications)

    return {
        "statusCode": 200,
        "instances_processed": count
    }

