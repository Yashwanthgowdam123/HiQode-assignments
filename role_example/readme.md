# README.md

# GemFire Ansible Role

This project provides an Ansible role for configuring **VMware GemFire / Apache Geode** members. The role deploys `cache.xml` and `gemfire.properties` using Jinja2 templates and supports:

* PDX Serialization
* WAN Replication (Gateway Sender/Receiver)
* Region configuration
* Environment-specific variables
* Configuration management through Ansible roles

---

## Project Structure

```text
ansible-gemfire/
├── inventory/
│   ├── dev/
│   │   ├── hosts
│   │   └── group_vars/
│   │       └── gemfire.yml
│   └── prod/
├── playbooks/
│   └── gemfire.yml
├── roles/
│   └── gemfire/
│       ├── defaults/
│       │   └── main.yml
│       ├── tasks/
│       │   ├── main.yml
│       │   ├── install.yml
│       │   └── configure.yml
│       ├── templates/
│       │   ├── cache.xml.j2
│       │   └── gemfire.properties.j2
│       ├── handlers/
│       │   └── main.yml
│       └── vars/
└── ansible.cfg
```

---

## Prerequisites

* Ansible 2.12 or later
* SSH access to target servers
* Python installed on managed hosts
* VMware GemFire or Apache Geode installed on target hosts

---

## Inventory

Example `inventory/dev/hosts`

```ini
[gemfire_servers]
server1 ansible_host=192.168.1.101
server2 ansible_host=192.168.1.102

[gemfire_servers:vars]
ansible_user=ec2-user
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

---

## Configuration

Environment-specific configuration is stored in:

```text
inventory/dev/group_vars/gemfire.yml
```

Example:

```yaml
cluster_name: DEV

gateway_sender:
  enabled: true
  id: DEV_TO_DR
  remote_ds_id: 2

gateway_receiver:
  enabled: true
  start_port: 1530
  end_port: 1550

pdx:
  persistent: true
  read_serialized: true
  ignore_unread_fields: false
  disk_store: PDXDiskStore

regions:
  - name: Customer
    type: PARTITION
  - name: Orders
    type: PARTITION
```

---

## Running the Playbook

### Verify connectivity

```bash
ansible -i inventory/dev/hosts gemfire_servers -m ping
```

### Preview changes

```bash
ansible-playbook \
  -i inventory/dev/hosts \
  playbooks/gemfire.yml \
  --check \
  --diff
```

### Deploy configuration

```bash
ansible-playbook \
  -i inventory/dev/hosts \
  playbooks/gemfire.yml \
  --become
```

### Run against a single host

```bash
ansible-playbook \
  -i inventory/dev/hosts \
  playbooks/gemfire.yml \
  --limit server1
```

### Enable verbose logging

```bash
ansible-playbook \
  -i inventory/dev/hosts \
  playbooks/gemfire.yml \
  --become \
  -vvv
```

---

## Generated Files

The role generates the following configuration files on each managed host:

| File                 | Description                                         |
| -------------------- | --------------------------------------------------- |
| `cache.xml`          | Cache configuration including PDX, WAN, and Regions |
| `gemfire.properties` | Distributed system properties                       |

Default deployment location:

```text
/opt/gemfire/config/
```

---

## Supported Features

* PDX Serialization
* Persistent PDX Metadata
* WAN Gateway Sender
* WAN Gateway Receiver
* Region Creation
* Jinja2-based Configuration Templates
* Environment-specific Variables
* Handler-based Service Restart

---

## Customization

The role can be extended to support:

* Multiple Gateway Senders
* Multiple Gateway Receivers
* Async Event Queues
* Disk Stores
* Cache Servers
* Client Subscription Configuration
* Security (SSL/TLS)
* Authentication and Authorization
* Locator Configuration
* Cluster Configuration Service

---

## Example Execution Workflow

```bash
# Verify SSH connectivity
ansible -i inventory/dev/hosts gemfire_servers -m ping

# Preview changes
ansible-playbook -i inventory/dev/hosts playbooks/gemfire.yml --check --diff

# Apply configuration
ansible-playbook -i inventory/dev/hosts playbooks/gemfire.yml --become

# Verify generated cache.xml
ansible -i inventory/dev/hosts gemfire_servers \
  -m shell \
  -a "cat /opt/gemfire/config/cache.xml"
```

---

## License

This project is intended as a reusable Ansible role for automating VMware GemFire or Apache Geode configuration. Modify and extend it to match your organization's deployment standards and operational requirements.

