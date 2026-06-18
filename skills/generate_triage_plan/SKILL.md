---
name: generate_triage_plan
description: >-
  Produce an ordered investigation plan from a failure classification
  and the available evidence sources, with explicit stop conditions so
  the investigation ends when the next step would not change the
  conclusion. Use at the start of any non-trivial failure.
tags: [triage, plan, investigation, rca]
---

# generate_triage_plan

## Purpose

Unplanned triage wanders. It re-reads the same log, chases the loudest
error instead of the first one, and stops when the engineer is tired
rather than when the question is answered. This skill produces a cheap,
ordered plan with stop conditions before any deep investigation starts.

## Inputs

- `failure_classification` — a first-pass class (PASS / HANG / TEST-BUG
  / INFRA / FRAMEWORK / PRODUCT) plus the error signature.
- `available_evidence` — what can actually be inspected: result
  metadata, logs (and their sizes), support bundles, live cluster
  access (yes/no), prior-incident search, knowledge base.

## Outputs

```yaml
ordered_steps:
  - step: "Parse result metadata for exact phase + counts"
    cost: cheap
    yields: "Confirm class; narrow to a phase"
  - step: "Slice logs around the first error timestamp"
    cost: cheap
    yields: "The emitting code path"
  - step: "Search prior incidents for the error signature"
    cost: cheap
    yields: "Known-issue match or novelty"
  - step: "Inspect live cluster state (if access available)"
    cost: expensive
    yields: "Current vs expected state"
stop_conditions:
  - "A prior incident matches the signature exactly -> attach and stop."
  - "Root cause confidence is high and the next step is expensive."
  - "Evidence is exhausted -> report best hypothesis + what's missing."
```

## Prompt template

> You are planning a triage. Inputs: classification {failure_classification},
> evidence {available_evidence}.
> 1. Order steps cheapest-first and highest-information-first. Parse hard
>    facts (counts, phases, exact signatures) before any reasoning that
>    depends on them.
> 2. For each step, state what it costs and what it would yield. Skip
>    steps whose evidence source is unavailable; degrade gracefully
>    (logs-only if there is no live access).
> 3. Define stop conditions up front: a prior-incident match, a
>    high-confidence cause before an expensive step, or exhausted
>    evidence. The goal is to *end* the investigation deliberately.
> Output the ordered plan and the stop conditions.

## Examples

- **HANG with logs only, no live access.** → plan centers on the last
  progress line before the hang and the timeout owner; skip live-state
  steps; stop when the blocking call is identified.
- **INFRA-class with live access.** → cheap metadata + log slice first,
  then targeted live checks (disk pressure, node readiness) only if the
  logs point there.

## Composition

This is the entry-point skill. It schedules `summarize_logs`,
`explain_failure`, `analyze_cluster_health`, `check_disk_pressure`, and
finally `identify_root_cause`.
