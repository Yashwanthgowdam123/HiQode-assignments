## Ansible PEM Permission Issue (Multi-User Controller)

## Issue

We configured the SSH private key (`AwsPrivateKey.pem`) in `ansible.cfg`:

```ini
private_key_file = /home/ubuntu/pemfile/AwsPrivateKey.pem
```

The PEM file was owned by:

```text
Owner : ubuntu
Group : ubuntu
```

When running Ansible as the **ubuntu** user, everything worked correctly.

However, when switching to another user (**yashwanth**) and executing an ad-hoc command:

```bash
ansible -i /opt/ansible/inventories/hosts trial \
  -m shell \
  -a "uptime -p"
```

Ansible failed with the following error:

```text
Load key "/home/ubuntu/pemfile/AwsPrivateKey.pem": Permission denied
ubuntu@98.xx.xx.xx: Permission denied (publickey)
```

### Root Cause

Although the SSH key existed and was valid, the **yashwanth** user did not have permission to read the PEM file located inside another user's home directory (`/home/ubuntu`).

```bash
ls -lrt /home/ubuntu/pemfile/AwsPrivateKey.pem
-r-------- 1 **ubuntu ubuntu** 1679 Jul 21 22:26 /home/ubuntu/pemfile/AwsPrivateKey.pem
```

As a result, SSH could not load the private key and authentication failed.

---

# Solution 1: Switch to the Ubuntu User

Since the PEM file belongs to the `ubuntu` user, switch to that user before running Ansible.

```bash
sudo su - ubuntu
```

Run the ad-hoc command:

```bash
ansible -i /opt/ansible/inventories/hosts trial -m shell -a "uptime -p"
```

This works because the owner of the key is executing the command.

---

# Solution 2: Execute Ansible Using sudo

Instead of switching users, execute the command as the `ubuntu` user.

```bash
sudo su
ansible -i /opt/ansible/inventories/hosts trial -m shell -a "uptime -p"
```

or simply run Ansible using `sudo` if appropriate for your environment.

```bash
sudo ansible -i /opt/ansible/inventories/hosts trial -m shell -a "uptime -p"
```
---

# Solution 3: Grant Access Using ACL (Recommended)

Instead of copying the PEM file for every user, grant read permission to the required user using Access Control Lists (ACL).

## Install ACL

```bash
sudo apt update
sudo apt install acl -y
```

## Grant Permissions

Allow the `yashwanth` user to read the PEM file:

```bash
sudo setfacl -m u:yashwanth:r /home/ubuntu/pemfile/AwsPrivateKey.pem
```

Allow the `yashwanth` user to traverse the required directories:

```bash
sudo setfacl -m u:yashwanth:x /home/ubuntu
sudo setfacl -m u:yashwanth:x /home/ubuntu/pemfile
```

Verify the ACL configuration:

```bash
getfacl /home/ubuntu/pemfile/AwsPrivateKey.pem
```

Now the `yashwanth` user can execute:

```bash
ansible -i /opt/ansible/inventories/hosts trial -m shell -a "uptime -p"
```

without encountering any SSH key permission issues.

---

# Best Practice

For environments where multiple administrators use the same Ansible controller, avoid storing SSH private keys inside a user's home directory.

A better approach is to:

- Create a shared directory (e.g., `/opt/ansible/keys`).
- Store all SSH keys in this directory.
- Assign the directory to a dedicated group (e.g., `ansible`).
- Grant only the required users read access to the keys.
- Reference the shared key path in `ansible.cfg`.

This simplifies key management while maintaining secure access for authorized users.
