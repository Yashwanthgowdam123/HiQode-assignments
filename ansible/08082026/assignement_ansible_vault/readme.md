# Ansible Vault - Complete Beginner Guide

## What is Ansible Vault?

**Ansible Vault** is a feature in Ansible that encrypts sensitive information such as:

* Passwords
* API Keys
* SSH Private Keys
* Database Credentials
* AWS Access Keys
* SSL Certificates

Instead of storing secrets in plain text, Ansible Vault encrypts them and decrypts them only during playbook execution.

---

# Example 1: Encrypt a Variable File (Recommended)

## Step 1: Create a Variable File

```bash
vim secrets.yml
```

Add the following content:

```yaml
db_user: admin
db_password: MyPassword@123
```

Save and exit.

---

## Step 2: Encrypt the File

```bash
ansible-vault encrypt secrets.yml
```

Example Output:

```text
New Vault password:
Confirm New Vault password:
Encryption successful
```

The file is now encrypted.

Example:

```yaml
$ANSIBLE_VAULT;1.1;AES256
6131326239623738646633...
9a8b7c6d5e4f...
```

---

## Step 3: Create the Playbook

Create a file named `playbook.yml`.

```yaml
---
- name: Vault Example
  hosts: webservers
  become: yes

  vars_files:
    - secrets.yml

  tasks:

    - name: Display Database Username
      debug:
        msg: "{{ db_user }}"

    - name: Display Database Password
      debug:
        msg: "{{ db_password }}"
```

---

## Step 4: Execute the Playbook

```bash
ansible-playbook playbook.yml --ask-vault-pass
```

Example Output:

```text
Vault password:

PLAY [Vault Example] *************************************************

TASK [Display Database Username] *************************************
ok: [server1]

MSG:
admin

TASK [Display Database Password] *************************************
ok: [server1]

MSG:
MyPassword@123

PLAY RECAP ***********************************************************
server1 : ok=2 changed=0 unreachable=0 failed=0
```

---

# Example 2: Create an Encrypted File Directly

Create an encrypted file.

```bash
ansible-vault create secrets.yml
```

It opens **vim**.

Add:

```yaml
username: admin
password: Secret123
```

Save and exit.

The file is automatically encrypted.

---

# Example 3: View an Encrypted File

```bash
ansible-vault view secrets.yml
```

Example Output:

```yaml
username: admin
password: Secret123
```

---

# Example 4: Edit an Encrypted File

```bash
ansible-vault edit secrets.yml
```

Modify the password.

```yaml
username: admin
password: NewPassword123
```

Save and exit.

The file is automatically encrypted again.

---

# Example 5: Change the Vault Password

```bash
ansible-vault rekey secrets.yml
```

Example Output:

```text
Vault password:
New Vault password:
Confirm New Vault password:
Rekey successful
```

---

# Example 6: Permanently Decrypt a File

```bash
ansible-vault decrypt secrets.yml
```

Example Output:

```text
Decryption successful
```

The file becomes plain text again.

---

# Example 7: Encrypt an Existing File

Suppose `db.yml` contains:

```yaml
mysql_user: root
mysql_password: password123
```

Encrypt it.

```bash
ansible-vault encrypt db.yml
```

Example Output:

```text
New Vault password:
Confirm Vault password:
Encryption successful
```

---

# Example 8: Encrypt a Single Variable

Encrypt only one variable.

```bash
ansible-vault encrypt_string 'MyPassword123' --name 'db_password'
```

Example Output:

```yaml
db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          6631356133643463...
          6439383562616234...
```

Create `vars.yml`.

```yaml
db_user: admin

db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          6631356133643463...
          6439383562616234...
```

Create Playbook:

```yaml
---
- hosts: all

  vars_files:
    - vars.yml

  tasks:
    - debug:
        msg: "{{ db_password }}"
```

Execute:

```bash
ansible-playbook playbook.yml --ask-vault-pass
```

---

# Example 9: Use a Vault Password File

Create the password file.

```bash
vim vault_pass.txt
```

Contents:

```text
MyVaultPassword
```

Set secure permissions.

```bash
chmod 600 vault_pass.txt
```

Execute playbook.

```bash
ansible-playbook playbook.yml --vault-password-file vault_pass.txt
```

Example Output:

```text
PLAY [all] ************************************************************

TASK [debug] **********************************************************
ok: [server1]

MSG:
MyPassword123

PLAY RECAP ************************************************************
server1 : ok=1 changed=0 unreachable=0 failed=0
```

---

# Example 10: Real-Time Deployment Example

Project Structure

```text
project/
│
├── inventory
├── deploy.yml
├── secrets.yml      (Encrypted)
├── app.war
└── vault_pass.txt
```

### secrets.yml

```yaml
deploy_user: tomcatadmin
deploy_password: Password@123
```

Encrypt the file.

```bash
ansible-vault encrypt secrets.yml
```

---

### deploy.yml

```yaml
---
- name: Deploy WAR File
  hosts: tomcat
  become: yes

  vars_files:
    - secrets.yml

  tasks:

    - name: Copy WAR File
      copy:
        src: app.war
        dest: /opt/tomcat/webapps/

    - name: Verify Deployment User
      debug:
        msg: "Deploying application using {{ deploy_user }}"
```

Run the playbook.

```bash
ansible-playbook -i inventory deploy.yml --ask-vault-pass
```

Example Output:

```text
Vault password:

PLAY [Deploy WAR File] ************************************************

TASK [Copy WAR File] **************************************************
changed: [tomcat-server]

TASK [Verify Deployment User] *****************************************
ok: [tomcat-server]

MSG:
Deploying application using tomcatadmin

PLAY RECAP ************************************************************
tomcat-server : ok=2 changed=1 unreachable=0 failed=0
```

---

# Common Ansible Vault Commands

| Command                                                              | Description                                 |
| -------------------------------------------------------------------- | ------------------------------------------- |
| `ansible-vault create secrets.yml`                                   | Create a new encrypted file                 |
| `ansible-vault encrypt secrets.yml`                                  | Encrypt an existing file                    |
| `ansible-vault decrypt secrets.yml`                                  | Permanently decrypt a file                  |
| `ansible-vault edit secrets.yml`                                     | Edit an encrypted file                      |
| `ansible-vault view secrets.yml`                                     | View encrypted file contents                |
| `ansible-vault rekey secrets.yml`                                    | Change the vault password                   |
| `ansible-vault encrypt_string 'secret' --name 'password'`            | Encrypt a single variable                   |
| `ansible-playbook playbook.yml --ask-vault-pass`                     | Execute playbook by entering vault password |
| `ansible-playbook playbook.yml --vault-password-file vault_pass.txt` | Execute playbook using a password file      |

---

# Best Practices

* Never store passwords in plain text.
* Encrypt only files that contain sensitive information.
* Keep the vault password file outside the project repository.
* Set proper permissions on the password file (`chmod 600`).
* Do not commit the vault password file to Git.
* Use different vault passwords for Development, Testing, and Production environments.
* Use `encrypt_string` when only one or two variables need encryption.
* Regularly rotate (rekey) your vault password for better security.

---

# Summary

Ansible Vault provides a secure way to manage secrets in your automation projects. It allows you to encrypt entire files or individual variables while keeping your playbooks readable and version-control friendly. By combining encrypted variable files with Ansible playbooks, you can safely automate deployments without exposing sensitive credentials.

