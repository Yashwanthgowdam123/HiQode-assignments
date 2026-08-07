# AWS EC2 Helper Functions

A collection of Bash functions to simplify common AWS EC2 operations directly from the terminal.

These functions allow you to:

- View running EC2 Public IPs
- View running EC2 Private IPs
- Display complete EC2 information
- Create multiple Ubuntu EC2 instances
- Delete all running EC2 instances
- Automatically update an Ansible inventory file

---

# Features

- Interactive menu
- Command line support
- Bulk EC2 creation
- Bulk EC2 termination (with confirmation)
- Auto naming (server1, server2, ...)
- Generates Ansible inventory automatically
- Lightweight (only Bash + AWS CLI)

---

# Prerequisites

Before using these functions, ensure you have:

- Bash
- AWS CLI v2
- Configured AWS credentials

```bash
aws configure
```

You must also have permissions for:

- ec2:DescribeInstances
- ec2:RunInstances
- ec2:TerminateInstances

---

# Installation

Clone the repository.

```bash
git clone https://github.com/<username>/<repo>.git
```

Open your `.bashrc`

```bash
nano ~/.bashrc
```

Copy the functions into your `.bashrc`

Reload Bash.

```bash
source ~/.bashrc
```

---

# Configuration

Update the default values inside the script.

```bash
AMI_ID="ami-xxxxxxxx"
INSTANCE_TYPE="t2.micro"
KEY_NAME="YourKeyPair"
SECURITY_GROUP="sg-xxxxxxxx"
SUBNET_ID="subnet-xxxxxxxx"
```

These values are used whenever a new EC2 instance is created.

---

# Function 1 : getec2

Displays information about running EC2 instances or performs EC2 operations.

## Syntax

```bash
getec2
```

or

```bash
getec2 <command>
```

---

# Interactive Mode

Simply run

```bash
getec2
```

You'll see

```
===========================
         GET EC2
===========================
public
private
complete_info
create <count>
delete
```

Select an option when prompted.

---

# Commands

## 1. List Public IPs

```bash
getec2 public
```

Example

```
54.91.20.14
18.201.33.72
3.85.117.90
```

---

## 2. List Private IPs

```bash
getec2 private
```

Example

```
172.31.20.51
172.31.18.71
172.31.5.12
```

---

## 3. Show Complete EC2 Details

```bash
getec2 complete_info
```

Displays

- Name
- Public IP
- Private IP
- Security Group
- VPC ID
- Instance Type

Example

```
--------------------------------------------------------
|                    DescribeInstances                  |
+---------+---------------+---------------+------------+
| Name    | Public IP     | Private IP    | Type       |
+---------+---------------+---------------+------------+
| server1 | 54.x.x.x      | 172.31.x.x    | t2.micro   |
| server2 | 18.x.x.x      | 172.31.x.x    | t2.micro   |
+---------+---------------+---------------+------------+
```

---

## 4. Create EC2 Instances

Syntax

```bash
getec2 create <count>
```

Example

```bash
getec2 create 3
```

Output

```
Creating server1...
server1 created.

Creating server2...
server2 created.

Creating server3...
server3 created.
```

Instances are tagged automatically.

```
server1
server2
server3
...
```

---

## 5. Delete Running Instances

```bash
getec2 delete
```

The script

- Lists all running instance IDs
- Asks for confirmation
- Terminates all running instances

Example

```
Running Instance IDs

i-0aa123456
i-0bb123456

Terminate ALL running instances? (yes/no):
```

Only

```
yes
```

or

```
y
```

will terminate instances.

---

# Function 2 : update_inventory

Automatically updates an Ansible inventory using the running EC2 Public IPs.

---

## Syntax

```bash
update_inventory
```

or

```bash
update_inventory webservers
```

---

## Without Argument

If no cluster name is supplied,

```bash
update_inventory
```

You'll be prompted

```
Enter cluster name:
```

Example

```
Enter cluster name: webservers
```

Inventory generated

```ini
[webservers]
54.23.11.20
18.214.92.15
```

---

## With Argument

```bash
update_inventory production
```

Produces

```ini
[production]
54.23.11.20
18.214.92.15
```

---

# Inventory Location

The function appends to

```bash
/opt/ansible/inventories/hosts
```

Example

```ini
[webservers]
54.10.20.30
54.20.30.40

[database]
18.200.50.60
18.201.90.70
```

---

# Typical Workflow

Create servers

```bash
getec2 create 3
```

↓

Verify

```bash
getec2 complete_info
```

↓

Generate inventory

```bash
update_inventory webservers
```

↓

Run Ansible

```bash
ansible all -m ping
```

---

# Requirements

- AWS CLI
- Bash
- Ansible (for inventory update feature)

---

# Notes

- Public IPs are retrieved only from **running** EC2 instances.
- Inventory is appended to the existing hosts file.
- Existing inventory entries are **not** overwritten.
- Instance names always start from `server1`. If instances already exist with the same names, duplicate tags may occur.
- Ensure your AWS CLI profile is configured before running the functions.

---

# Future Improvements

- Support custom AMI IDs during creation
- Support instance naming prefixes
- Create Security Groups automatically
- Create Key Pairs automatically
- Support multiple AWS profiles
- Support multiple AWS regions
- Add colored terminal output
- Export inventory in YAML format
- Generate dynamic Ansible inventory
- Delete specific EC2 instances by name or ID

---

# License

MIT License

Feel free to use, modify, and contribute.
