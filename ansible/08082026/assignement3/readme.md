# Dynamic Inventory in Ansible

## Objective

Learn how to create and use a **Dynamic Inventory** in Ansible.

Unlike a static inventory (`hosts.ini`), a dynamic inventory automatically generates the list of managed hosts using a script or program. This is commonly used with cloud providers like AWS, Azure, GCP, VMware, etc.

---

# Lab Environment

| Machine | Hostname | Purpose |
|----------|----------|---------|
| Ansible Controller | ansible-controller | Runs Ansible |
| Target Server 1 | target-server1 | Managed Node |
| Target Server 2 | target-server2 | Managed Node |

---

# Directory Structure

```text
dynamic-inventory/
├── inventory.py
├── ansible.cfg
├── playbook.yml
└── README.md
```

---

# Step 1: Create Project Directory

```bash
mkdir ~/dynamic-inventory
cd ~/dynamic-inventory
```

---

# Step 2: Create Dynamic Inventory Script

Create the inventory file.

```bash
vim inventory.py
```

Paste the following:

```python
#!/usr/bin/env python3

import json

inventory = {
    "webservers": {
        "hosts": [
            "192.168.1.101",
            "192.168.1.102"
        ]
    },

    "_meta": {
        "hostvars": {
            "192.168.1.101": {
                "ansible_user": "ubuntu"
            },
            "192.168.1.102": {
                "ansible_user": "ubuntu"
            }
        }
    }
}

print(json.dumps(inventory))
```

Save the file.

---

# Step 3: Make Script Executable

```bash
chmod +x inventory.py
```

Verify:

```bash
ls -l inventory.py
```

Example:

```text
-rwxr-xr-x 1 ubuntu ubuntu inventory.py
```

---

# Step 4: Test the Dynamic Inventory

Run:

```bash
./inventory.py
```

Expected Output:

```json
{
    "webservers": {
        "hosts": [
            "192.168.1.101",
            "192.168.1.102"
        ]
    },
    "_meta": {
        "hostvars": {
            "192.168.1.101": {
                "ansible_user": "ubuntu"
            },
            "192.168.1.102": {
                "ansible_user": "ubuntu"
            }
        }
    }
}
```

---

# Step 5: Create ansible.cfg

```bash
vim ansible.cfg
```

Contents:

```ini
[defaults]
inventory = ./inventory.py
host_key_checking = False
```

---

# Step 6: Verify Inventory

```bash
ansible-inventory --list
```

Expected Output:

```json
{
    "webservers": {
        "hosts": [
            "192.168.1.101",
            "192.168.1.102"
        ]
    }
}
```

---

# Display Inventory Graph

```bash
ansible-inventory --graph
```

Example Output:

```text
@all:
  |--@ungrouped:
  |--@webservers:
      |--192.168.1.101
      |--192.168.1.102
```

---

# Step 7: Test Connectivity

```bash
ansible webservers -m ping
```

Expected Output:

```text
192.168.1.101 | SUCCESS =>
{
    "changed": false,
    "ping": "pong"
}

192.168.1.102 | SUCCESS =>
{
    "changed": false,
    "ping": "pong"
}
```

---

# Step 8: Create a Playbook

```bash
vim playbook.yml
```

Contents:

```yaml
---
- name: Dynamic Inventory Demo
  hosts: webservers
  become: yes

  tasks:

    - name: Print hostname
      command: hostname
      register: output

    - name: Display hostname
      debug:
        var: output.stdout
```

---

# Step 9: Run the Playbook

```bash
ansible-playbook playbook.yml
```

Expected Output:

```text
PLAY [Dynamic Inventory Demo]

TASK [Print hostname]
ok: [192.168.1.101]
ok: [192.168.1.102]

TASK [Display hostname]
ok: [192.168.1.101] =>
    output.stdout: target-server1

ok: [192.168.1.102] =>
    output.stdout: target-server2

PLAY RECAP

192.168.1.101 : ok=2 changed=1 failed=0
192.168.1.102 : ok=2 changed=1 failed=0
```

---

# Understanding the Inventory Structure

```python
inventory = {
    "webservers": {
        "hosts": [
            "192.168.1.101",
            "192.168.1.102"
        ]
    },

    "_meta": {
        "hostvars": {
            "192.168.1.101": {
                "ansible_user": "ubuntu"
            }
        }
    }
}
```

Explanation:

- `webservers` → Inventory group.
- `hosts` → List of managed hosts.
- `_meta` → Host variables.
- `hostvars` → Variables for individual hosts.
- `ansible_user` → SSH login user.

---

# Dynamic Inventory vs Static Inventory

## Static Inventory

```ini
[webservers]
192.168.1.101
192.168.1.102
```

Advantages

- Easy to create
- Good for small environments
- Simple to understand

Disadvantages

- Manual updates required
- Not suitable for cloud environments
- Difficult to maintain at scale

---

## Dynamic Inventory

Generated automatically.

Example:

```bash
./inventory.py
```

Advantages

- Automatic host discovery
- Ideal for cloud environments
- No manual updates
- Scales easily

Disadvantages

- Slightly more complex
- Requires scripting or inventory plugins

---

# Useful Commands

Show inventory

```bash
ansible-inventory --list
```

Graph view

```bash
ansible-inventory --graph
```

Ping all hosts

```bash
ansible all -m ping
```

Ping webservers group

```bash
ansible webservers -m ping
```

Run playbook

```bash
ansible-playbook playbook.yml
```

Display inventory in YAML

```bash
ansible-inventory --list --yaml
```

---

# Real-World Dynamic Inventory Sources

- AWS EC2
- Microsoft Azure
- Google Cloud Platform (GCP)
- VMware vCenter
- OpenStack
- Kubernetes
- Docker
- Terraform Outputs
- REST APIs
- CMDB (Configuration Management Database)

---

# Interview Questions

### 1. What is Dynamic Inventory?

Dynamic Inventory automatically generates the host list instead of storing it in a static file.

---

### 2. Why use Dynamic Inventory?

To automatically discover hosts in changing environments such as cloud platforms.

---

### 3. What command displays the inventory?

```bash
ansible-inventory --list
```

---

### 4. What command displays inventory as a graph?

```bash
ansible-inventory --graph
```

---

### 5. What is `_meta` in Dynamic Inventory?

`_meta` contains host-specific variables (`hostvars`) and helps Ansible avoid making separate requests for each host.

---

### 6. Which cloud platforms support Dynamic Inventory?

- AWS
- Azure
- GCP
- VMware
- OpenStack
- Kubernetes

---

### 7. What is the difference between Static and Dynamic Inventory?

| Static Inventory | Dynamic Inventory |
|------------------|-------------------|
| Manual host entries | Automatically generated |
| Fixed list of servers | Automatically updated |
| Best for small environments | Best for large/cloud environments |
| Easy to create | Requires scripts or plugins |
| Manual maintenance | Automated maintenance |

---

# Summary

In this lab, you learned how to:

- Create a Python-based Dynamic Inventory script.
- Configure `ansible.cfg` to use the dynamic inventory.
- Verify the inventory using `ansible-inventory`.
- Ping hosts discovered dynamically.
- Run a playbook using the generated inventory.
- Understand the difference between static and dynamic inventory.
- Identify common real-world use cases for Dynamic Inventory in cloud and enterprise environments.
