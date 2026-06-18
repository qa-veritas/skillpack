---
name: create_verification_strategy
description: >-
  Given an intended change, define the pre-check, the observable
  post-checks that prove it worked, and the signal that triggers
  rollback. Use before applying any change to a live resource.
tags: [verification, change, rollback, precheck, postcheck]
---

# create_verification_strategy

## Purpose

A change is not done when it is applied; it is done when an observable
signal confirms it. This skill turns an intent ("raise the index
cluster heap to 16 GB") into the checks that prove success and the
signal that says "roll back now," *before* the change is made.

## Inputs

- `intended_change` — the action and its goal, in plain terms.
- `current_state` (optional) — the relevant facts from inventory
  (current values, capacity, dependents).

## Outputs

```yaml
pre_check:
  - "Heap currently 8 GB; node RAM 32 GB; rule: heap <= 50% RAM, <= 31 GB."
  - "16 GB satisfies the rule; proceed."
post_checks:
  - check: "Process reports -Xmx16g"
    signal: "JVM args show 16g"
  - check: "Cluster returns to green within 5 min"
    signal: "health endpoint status == green"
  - check: "No OOM / restart loop"
    signal: "0 restarts over 10 min"
rollback_signal: >-
  Cluster not green within 5 min, OR any restart, OR heap pressure
  alarms. Rollback path: re-create with previous -Xmx and keep the old
  container as a named fallback until green.
```

## Prompt template

> You are designing the verification for a change *before* it is made.
> Inputs: intent {intended_change}, current state {current_state}.
> 1. Write a pre-check that confirms the change is feasible and safe
>    against recorded capacity and rules of thumb. If it fails, stop and
>    recommend the smaller change.
> 2. Define post-checks that are *observable* — a health status, a port
>    listening, a process arg, a reconverged count. Not "looks fine."
>    Each post-check names the exact signal.
> 3. Define the rollback signal and the rollback path. Prefer reversible
>    actions (keep the previous artifact as a named fallback until the
>    post-checks pass).
> Output the structured strategy. The change itself is out of scope —
> this skill only defines how we will know it worked.

## Examples

- **Resize a data-bearing VM.** Pre-check: capacity + graceful path
  (ACPI shutdown, never hard kill). Post-check: VM boots, service
  rejoins, data intact. Rollback: revert size, power on.
- **Add a proxied hostname.** Post-check: config test passes and the
  new host resolves to the backend. Rollback: remove the server block,
  reload.

## Composition

Consumes `identify_root_cause` (so the fix verification targets the
real cause) and uses `analyze_cluster_health` / `check_disk_pressure`
as post-checks.
