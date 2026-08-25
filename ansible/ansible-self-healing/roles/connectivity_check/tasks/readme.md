# Connectivity Check Role

The **`connectivity_check`** role is the first stage of the self-healing framework. It verifies that the target host is reachable before any health checks or remediation tasks are executed. If the host is unreachable, the role records the issue for reporting and stops further execution for that host.

---

## Purpose

- Verify SSH connectivity to the target host.
- Determine whether the host is reachable.
- Record unreachable hosts for manual intervention.
- Prevent unnecessary execution of downstream roles.

---

## Workflow

```text
Start
 │
 ▼
Ping Target Host
 │
 ├── Success
 │      │
 │      ▼
 │   Set host_reachable = true
 │      │
 │      ▼
 │   Continue Playbook
 │
 └── Failure
        │
        ▼
Set host_reachable = false
        │
        ▼
Record Manual Intervention
        │
        ▼
End Execution for Host
```

---

## Tasks Performed

### 1. Verify Connectivity

Uses the built-in Ansible `ping` module to confirm that the target host is accessible over SSH.

```yaml
- name: Ping host to verify connectivity
  ansible.builtin.ping:
```

The result is stored in:

```yaml
connectivity_result
```

---

### 2. Determine Reachability

A boolean fact is created based on the ping result.

```yaml
host_reachable: "{{ connectivity_result is succeeded }}"
```

Possible values:

| Value | Meaning |
|--------|---------|
| `true` | Host is reachable |
| `false` | Host is unreachable |

---

### 3. Record Manual Intervention

If the host cannot be reached, the role marks it as requiring administrator attention.

```yaml
manual_intervention_required: true
```

Reason recorded:

```text
Host unreachable via ping/SSH
```

This reason is appended to the shared list:

```yaml
manual_intervention_reasons
```

allowing multiple roles to contribute unresolved issues.

---

### 4. Stop Further Processing

If the host is unreachable, execution ends immediately for that host.

```yaml
ansible.builtin.meta: end_host
```

This prevents unnecessary health checks and remediation attempts on an inaccessible system.

---

## Variables

| Variable | Description |
|----------|-------------|
| `connectivity_result` | Stores the result of the Ansible ping module |
| `host_reachable` | Indicates whether the host is reachable |
| `manual_intervention_required` | Flags whether manual intervention is required |
| `manual_intervention_reasons` | List of reasons requiring administrator action |

---

## Execution Flow

```text
Ping Host
    │
    ▼
Successful?
 ├── Yes
 │      │
 │      ▼
 │ Continue to Next Role
 │
 └── No
        │
        ▼
Record Manual Intervention
        │
        ▼
End Host Execution
```

---

## Example Output

### Reachable Host

```text
TASK [Ping host to verify connectivity] *****************
ok: [web01]

TASK [Set connectivity fact] *****************************
ok: [web01]

Host Status:
✓ Reachable
```

### Unreachable Host

```text
TASK [Ping host to verify connectivity] *****************
fatal: [db01]: UNREACHABLE!

TASK [Record unreachable host for manual intervention] ***
ok: [db01]

TASK [Stop remaining checks on this host if it is unreachable]
META: ending play for db01
```

---

## Benefits

- Validates connectivity before executing expensive operations.
- Avoids false failures caused by unreachable hosts.
- Clearly identifies systems requiring manual attention.
- Prevents unnecessary execution of downstream roles.
- Provides a clean and efficient starting point for the self-healing workflow.
