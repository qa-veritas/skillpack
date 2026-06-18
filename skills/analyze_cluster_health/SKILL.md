---
name: analyze_cluster_health
description: >-
  Turn a cluster health snapshot into a verdict, degraded components,
  and the next checks worth running. Use for health questions and
  pre/post-change checks.
tags: [cluster, health, nodes, quorum, triage]
---

# analyze_cluster_health

## Purpose

A health endpoint returns a wall of JSON. Convert it into a single
verdict (healthy / degraded / down), name the components that are
actually broken, and point at the next check — don't recite every field.

## Inputs

- `health_snapshot_json` — overall status, per-node status, replica /
  shard / quorum counts, pending tasks.
- `node_list` (optional) — expected membership, to catch a node that
  silently dropped out.

## Outputs

`overall_verdict`, `quorum` status, `degraded_components` (with the
specific issue and how long), `next_checks`, and a `confidence` level.

## Prompt template

> State the verdict in one word and justify it. Check quorum /
> control-plane availability first — a degraded data plane with intact
> quorum is recoverable; lost quorum is an emergency. List only
> genuinely degraded components. A node missing from the snapshot
> entirely is worse than one reporting unhealthy. Recommend the next 1-3
> localizing checks. Diagnose only; do not remediate here.

## Examples

- One node NotReady, replicas unassigned, quorum intact → degraded, not
  down; next check is the node, then allocation.
- Two of three control-plane nodes unreachable → down, quorum lost;
  escalate.
