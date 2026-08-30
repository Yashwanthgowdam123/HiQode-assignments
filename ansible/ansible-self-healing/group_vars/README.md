````markdown
## Configuration (`vars/main.yml`)

The remediation framework is fully configurable through the `vars/main.yml` file. Modify the values below to match your environment without changing any playbook or role logic.

```yaml
---
# =========================================================
# Self-Healing Remediation Configuration
# Tune these per-environment. Nothing else needs to change.
# =========================================================

# --- Thresholds ---
disk_usage_threshold: 30     # Trigger disk cleanup if usage exceeds 30%
memory_usage_threshold: 30   # Flag memory usage if it exceeds 30%

# --- Services that must always be running ---
critical_services:
  - nginx
  - tomcat10
  - apache2

# --- Disk cleanup targets when threshold is breached ---
log_cleanup_paths:
  - path: /var/log
    age_days: 14
    patterns:
      - "*.log.gz"
      - "*.log.[0-9]"
      - "*.gz"

  - path: /tmp
    age_days: 7
    patterns:
      - "*"

# --- Users that must exist on every managed host ---
required_users:
  - name: yash
    groups: sudo
    shell: /bin/bash

# --- Directories that must exist with correct ownership/perms ---
required_directories:
  - path: /opt/app
    owner: yash
    group: yash
    mode: "0755"

  - path: /opt/app/logs
    owner: yash
    group: yash
    mode: "0755"

# --- Reporting ---
report_dir: /home/yash/remediation_reports
local_report_dir: ./reports
```

---

## Configuration Parameters

### Thresholds

| Variable | Description | Default |
|----------|-------------|---------|
| `disk_usage_threshold` | Disk usage percentage that triggers automatic cleanup. | `30` |
| `memory_usage_threshold` | Memory usage percentage used for reporting purposes. No automatic remediation is performed. | `30` |

---

### Critical Services

The services listed under `critical_services` are monitored during every remediation run.

If a service is found to be stopped, the playbook automatically attempts to start it.

```yaml
critical_services:
  - nginx
  - tomcat10
  - apache2
```

---

### Disk Cleanup Configuration

Disk cleanup is performed only when the filesystem usage exceeds `disk_usage_threshold`.

Each cleanup target defines:

- Directory to scan
- File age threshold
- File patterns to remove

Example:

```yaml
log_cleanup_paths:
  - path: /var/log
    age_days: 14
    patterns:
      - "*.log.gz"
      - "*.gz"
```

This configuration removes compressed log files older than **14 days** from `/var/log`.

---

### Required Users

Users listed under `required_users` are automatically created if they do not already exist.

Example:

```yaml
required_users:
  - name: yash
    groups: sudo
    shell: /bin/bash
```

The playbook ensures:

- User exists
- Group membership is configured
- Default shell is assigned

---

### Required Directories

Directories defined in `required_directories` are created if missing.

Ownership and permissions are also enforced.

Example:

```yaml
required_directories:
  - path: /opt/app
    owner: yash
    group: yash
    mode: "0755"
```

The playbook ensures:

- Directory exists
- Correct owner
- Correct group
- Correct permissions

---

### Reporting

| Variable | Description |
|----------|-------------|
| `report_dir` | Directory on the managed host where remediation reports are generated. |
| `local_report_dir` | Directory on the Ansible control node where reports are fetched and stored. |

```yaml
report_dir: /home/yash/remediation_reports
local_report_dir: ./reports
```

---

## Customization

To adapt the remediation framework for another environment, simply update the values in `vars/main.yml`.

Common customizations include:

- Changing disk and memory thresholds
- Adding or removing critical services
- Defining additional cleanup paths
- Creating required users
- Managing required directories
- Updating report storage locations

No changes to the playbook or role tasks are required, making the framework reusable across development, testing, and production environments.
````
