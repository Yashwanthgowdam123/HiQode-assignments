# Ansible Assignment

## 1. Write a playbook to install Nginx, change the port from **80** to **8081**, and deploy some application into it.

## 2. Install Tomcat using a playbook and change the port from **8080** to **9090**.

## 3. Write a playbook to get the target instances report with the following details:

- CPU
- RAM
- Storage
- Hostname

## 4. Create your own custom inventory file and `ansible.cfg` file where the private key and user are declared in the inventory.

The inventory should contain at least the following groups and hosts:

```text
webserver
    web-01
    web-02

appserver
    app-01
    app-02

dbserver
    db-01
```

# 🚀 Ansible Automation Lab

This repository demonstrates three real-world Ansible automation tasks:

- ✅ Install & Configure Nginx with Custom Port
- ✅ Install Tomcat10 and Change Default Port
- ✅ Generate Target Server Resource Report

---

# 📌 Q1 - Install Nginx and Change Port (80 ➜ 8081)

## Inventory Verification

```bash
ansible-playbook /opt/ansible/playbooks/nginx_install_port_change.yml \
-u ubuntu \
-e "host=aws-servers desired_port=8081" \
--list-hosts
```

### Output

```text
playbook: /opt/ansible/playbooks/nginx_install_port_change.yml

play #1 (aws-servers): Install and Configure Nginx

Hosts:
54.234.22.122
52.90.202.67
54.162.157.11
```

---

## Execute Playbook

```bash
ansible-playbook /opt/ansible/playbooks/nginx_install_port_change.yml \
-u ubuntu \
-e "host=aws-servers desired_port=8081"
```

---

## Tasks Performed

- Install Nginx
- Change Listening Port
- Update IPv4 & IPv6 Configuration
- Deploy Sample Application
- Restart Nginx
- Verify Web Server

---

## Execution Summary

| Task | Status |
|-------|--------|
| Install Nginx | ✅ Success |
| Change Port (80 → 8081) | ✅ Success |
| Update IPv4 & IPv6 | ✅ Success |
| Deploy Application | ✅ Success |
| Restart Nginx | ✅ Success |
| Verification | ✅ Success |

---

## Verification

```text
http://54.234.22.122:8081
http://54.162.157.11:8081
http://52.90.202.67:8081
```

---

## Play Recap

| Host | OK | Changed | Failed |
|------|---:|---------:|-------:|
|54.234.22.122|6|4|0|
|54.162.157.11|6|4|0|
|52.90.202.67|6|4|0|

---

# 📌 Q2 - Install Tomcat10 and Change Port (8080 ➜ 9090)

## Inventory Verification

```bash
ansible-playbook /opt/ansible/playbooks/tomcat_install_port_change_v3.yml \
-e "host=today_tomcat_v2" \
--list-hosts
```

### Output

```text
playbook: /opt/ansible/playbooks/tomcat_install_port_change_v3.yml

Hosts:
100.31.88.101
3.92.84.231
```

---

## Execute Playbook

```bash
ansible-playbook /opt/ansible/playbooks/tomcat_install_port_change_v3.yml \
-e "host=today_tomcat_v2"
```

---

## Tasks Performed

- Update apt Repository
- Install Tomcat10
- Modify server.xml
- Change Port 8080 → 9090
- Restart Tomcat
- Verify Service
- Display URL

---

## Execution Summary

| Task | Status |
|-------|--------|
| Update apt Cache | ✅ Success |
| Install Tomcat10 | ✅ Success |
| Change Port | ✅ Success |
| Restart Tomcat | ✅ Success |
| Verify Service | ✅ Success |
| Display URL | ✅ Success |

---

## Verification

```text
http://3.92.84.231:9090
http://100.31.88.101:9090
```

---

## Play Recap

| Host | OK | Changed | Failed |
|------|---:|---------:|-------:|
|3.92.84.231|7|4|0|
|100.31.88.101|7|4|0|

---

# 📌 Q3 - Generate System Resource Report

## Inventory Verification

```bash
ansible-playbook /opt/ansible/playbooks/resource_manager.yml \
-u ubuntu \
-e "host=today_tomcat_v2" \
--list-hosts
```

### Output

```text
playbook: /opt/ansible/playbooks/resource_manager.yml

Hosts:
3.92.84.231
100.31.88.101
```

---

## Execute Playbook

```bash
ansible-playbook /opt/ansible/playbooks/resource_manager.yml \
-u ubuntu \
-e "host=today_tomcat_v2"
```

---

## Tasks Performed

- Gather Ansible Facts
- Collect Storage Information
- Display CPU, RAM, Storage and Hostname

---

## Sample Report

### Server 1

```text
======================================
Hostname : ip-172-31-21-254
CPU      : 2 vCPUs
RAM      : 908 MB (0.89 GB)
Storage  : 8.15 GB
======================================
```

### Server 2

```text
======================================
Hostname : ip-172-31-27-222
CPU      : 2 vCPUs
RAM      : 908 MB (0.89 GB)
Storage  : 8.15 GB
======================================
```

---

## Play Recap

| Host | OK | Changed | Failed |
|------|---:|---------:|-------:|
|3.92.84.231|3|0|0|
|100.31.88.101|3|0|0|

---

# 📊 Overall Project Summary

| Question | Objective | Result |
|-----------|-----------|--------|
| Q1 | Install Nginx & Change Port to **8081** | ✅ Completed |
| Q2 | Install Tomcat10 & Change Port to **9090** | ✅ Completed |
| Q3 | Generate Host Resource Report | ✅ Completed |

---

# 🛠 Technologies Used

- Ansible
- Ubuntu Linux
- AWS EC2
- Nginx
- Apache Tomcat 10
- SSH
- YAML Playbooks

---

# 📁 Playbooks

```text
/opt/ansible/playbooks/
│
├── nginx_install_port_change.yml
├── tomcat_install_port_change_v3.yml
└── resource_manager.yml
```

---

# ✅ Outcome

Successfully automated infrastructure provisioning and configuration using Ansible by:

- Deploying Nginx across multiple EC2 instances.
- Changing the default Nginx port from **80** to **8081**.
- Installing Apache Tomcat10 and changing its default port from **8080** to **9090**.
- Generating system resource reports (Hostname, CPU, RAM, Storage) from remote target servers.
- Managing multiple AWS EC2 instances simultaneously using Ansible inventories and playbooks.
