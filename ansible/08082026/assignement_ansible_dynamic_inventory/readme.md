# Dynamic Inventory Grouping using AWS Tags

This document demonstrates how the AWS Dynamic Inventory plugin groups EC2 instances based on AWS Tags and how to target those groups in Ansible playbooks.

---

# Current Inventory Structure

```bash
ansible-inventory --graph
```

Output:

```text
@all:
  |--@ungrouped:
  |--@aws_ec2:
  |  |--tomcat_prod_2
  |  |--nginx_qa_1
  |  |--nginx_prod_1
  |  |--tomcat_qa_1
  |  |--tomcat_prod_1
  |  |--tomcat_qa_2
  |
  |--@_tomcat:
  |  |--tomcat_prod_2
  |  |--tomcat_qa_1
  |  |--tomcat_prod_1
  |  |--tomcat_qa_2
  |
  |--@_prod:
  |  |--tomcat_prod_2
  |  |--nginx_prod_1
  |  |--tomcat_prod_1
  |
  |--@_tomcat_prod:
  |  |--tomcat_prod_2
  |  |--tomcat_prod_1
  |
  |--@_nginx:
  |  |--nginx_qa_1
  |  |--nginx_prod_1
  |
  |--@_qa:
  |  |--nginx_qa_1
  |  |--tomcat_qa_1
  |  |--tomcat_qa_2
  |
  |--@_nginx_qa:
  |  |--nginx_qa_1
  |
  |--@_nginx_prod:
  |  |--nginx_prod_1
  |
  |--@_tomcat_qa:
     |--tomcat_qa_1
     |--tomcat_qa_2
```

---

# Group: Production

```bash
ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml \
-e "host=_prod" --list-host
```

Output:

```text
playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_prod): Ping all AWS EC2 instances
    pattern: ['_prod']
    hosts (3):
      tomcat_prod_1
      nginx_prod_1
      tomcat_prod_2
```

---

# Group: QA

```bash
ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml \
-e "host=_qa" --list-host
```

Output:

```text
playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_qa): Ping all AWS EC2 instances
    pattern: ['_qa']
    hosts (3):
      tomcat_qa_1
      nginx_qa_1
      tomcat_qa_2
```

---

# Group: Tomcat Production

```bash
ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml \
-e "host=_tomcat_prod" --list-host
```

Output:

```text
playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_tomcat_prod): Ping all AWS EC2 instances
    pattern: ['_tomcat_prod']
    hosts (2):
      tomcat_prod_1
      tomcat_prod_2
```

---

# Group: Tomcat QA

```bash
ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml \
-e "host=_tomcat_qa" --list-host
```

Output:

```text
playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_tomcat_qa): Ping all AWS EC2 instances
    pattern: ['_tomcat_qa']
    hosts (2):
      tomcat_qa_2
      tomcat_qa_1
```

---

# Group: Nginx

```bash
ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml \
-e "host=_nginx" --list-host
```

Output:

```text
playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_nginx): Ping all AWS EC2 instances
    pattern: ['_nginx']
    hosts (2):
      nginx_qa_1
      nginx_prod_1
```

---

# Group: Nginx QA

```bash
ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml \
-e "host=_nginx_qa" --list-host
```

Output:

```text
playbook: /opt/ansible/playbooks/dynamic_inventory_trail.yml

  play #1 (_nginx_qa): Ping all AWS EC2 instances
    pattern: ['_nginx_qa']
    hosts (1):
      nginx_qa_1
```

---

# Summary

| Inventory Group | Hosts |
|-----------------|-------|
| `_prod` | `tomcat_prod_1`, `tomcat_prod_2`, `nginx_prod_1` |
| `_qa` | `tomcat_qa_1`, `tomcat_qa_2`, `nginx_qa_1` |
| `_tomcat` | `tomcat_prod_1`, `tomcat_prod_2`, `tomcat_qa_1`, `tomcat_qa_2` |
| `_nginx` | `nginx_prod_1`, `nginx_qa_1` |
| `_tomcat_prod` | `tomcat_prod_1`, `tomcat_prod_2` |
| `_tomcat_qa` | `tomcat_qa_1`, `tomcat_qa_2` |
| `_nginx_prod` | `nginx_prod_1` |
| `_nginx_qa` | `nginx_qa_1` |

---

# Playbook Example

```yaml
---
- name: Ping all AWS EC2 instances
  hosts: "{{ host }}"
  gather_facts: false

  tasks:

    - name: Ping
      ansible.builtin.ping:
```

Run the playbook:

```bash
ansible-playbook /opt/ansible/playbooks/dynamic_inventory_trail.yml \
-e "host=_tomcat_prod"
```

Replace `_tomcat_prod` with any desired inventory group such as:

- `_prod`
- `_qa`
- `_tomcat`
- `_nginx`
- `_tomcat_prod`
- `_tomcat_qa`
- `_nginx_prod`
- `_nginx_qa`
