---
name: check_disk_pressure
description: >-
  Decide whether a node's storage is under pressure and recommend an
  action. Use when a mount is filling, a workload reports no-space-left,
  or capacity planning needs a verdict.
tags: [storage, disk, capacity, pressure, triage]
---

# check_disk_pressure

## Purpose

Turn raw storage usage into a decision. "85% full" is not a decision;
"`/data` will hit 100% in ~6 hours at the current write rate; the top
consumer is the index store; reclaim 40 GB of expired snapshots first"
is.

## Inputs

- `df_output_or_metrics` — `df -h` / `df -i` text, or per-mount
  used/total bytes (two timestamped samples enable a fill-rate estimate).
- `thresholds` (optional) — warn/critical. Default warn 80%, critical
  90%; inode warn 85%.

## Outputs

Per mount: `state` (ok/warn/critical), `time_to_full` (if a rate
exists), `top_consumers`, and a `recommended_action` that prefers
reclaiming over resizing.

## Prompt template

> Assess disk pressure. Parse usage per mount including inodes (inode
> exhaustion looks fine on `df -h`). If two samples exist, compute a
> fill rate and time-to-full (state the linear assumption). Identify top
> consumers. Recommend the smallest reversible action first, and call
> out when a "full disk" is really a retention/rotation bug.

## Examples

- Index mount at 86%, no rate data → critical by threshold; check shard
  count and retention before resizing.
- Root at 92% from inodes, 30% bytes → byte view fine, inode view
  critical; target the directory with millions of small files.
