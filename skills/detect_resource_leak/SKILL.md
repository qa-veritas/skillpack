---
name: detect_resource_leak
description: >-
  Spot monotonic growth in a resource (memory, file descriptors,
  handles, disk, goroutines/threads) across repeated snapshots and
  attribute it to an owner. Use for slow degradations, OOM-after-hours,
  and "it works then falls over" symptoms.
tags: [memory, leak, fd, disk, degradation, observability]
---

# detect_resource_leak

## Purpose

Leaks rarely fail fast. They show up as a service that is fine for six
hours and then OOMs, or a node that degrades over a weekend. A single
snapshot cannot prove a leak; a trend can. This skill works on repeated
samples and outputs a verdict plus the suspected owner.

## Inputs

- `time_series_or_snapshots` — two or more timestamped samples of the
  resource (e.g. RSS per process, open FDs per process, disk used per
  mount, thread/goroutine counts).
- `resource_kind` — memory | file_descriptors | disk | threads | handles.

## Outputs

```yaml
leak_verdict: likely            # none | possible | likely
resource_kind: memory
growth_rate: "~180 MB/hour, monotonic over 5 samples"
projection: "OOM (8 GB limit) in ~36h from first sample"
suspected_owner:
  process: worker-pool
  evidence: >-
    Its RSS grows every sample; all other processes are flat. Growth
    correlates with request volume, suggesting per-request retention.
recommended_next: "Heap/FD diff between two samples for worker-pool"
```

## Prompt template

> You are deciding whether a resource is leaking. Inputs: samples
> {time_series_or_snapshots}, kind {resource_kind}.
> 1. Require monotonicity before claiming a leak. Sawtooth (grows, GC
>    drops it) is not a leak; steady upward drift across GC cycles is.
> 2. Compute a growth rate and project time-to-limit if a limit is
>    known. State the linear assumption.
> 3. Attribute: which process/component grows while others stay flat?
>    Correlate growth with a driver (request rate, connection count).
> 4. If only one sample exists, say so and refuse to call a leak —
>    recommend collecting a second sample at a stated interval instead.
> Output the structured verdict.

## Examples

- **RSS grows 180 MB/hr, flat elsewhere.** → `likely`; owner is the
  growing process; next step is a heap diff.
- **FDs spike then return to baseline each cycle.** → `none`; that is
  churn, not a leak. Saying "leak" here erodes trust.

## Composition

Feeds `analyze_cluster_health` (a leaking node is a degrading
component) and `identify_root_cause` for slow-degradation incidents.
