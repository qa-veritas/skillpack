---
name: identify_root_cause
description: >-
  From all collected findings, pick the single most-likely root cause
  with a confidence level, the supporting evidence, and the cheapest
  test that would falsify it. Use as the synthesis step at the end of a
  triage.
tags: [rca, root-cause, synthesis, triage, confidence]
---

# identify_root_cause

## Purpose

The synthesis step. After the plan, the log summary, the failure
explanation, and any live-state checks, this skill commits to one root
cause — with a confidence level and, critically, the test that would
prove it wrong. A root cause you cannot falsify is a guess.

## Inputs

- `findings_state` — the accumulated structured findings (log summary,
  failure explanation, cluster health, leak verdict, prior-incident
  matches). In practice this is a `state.json`-style document with typed
  sections.

## Outputs

```yaml
root_cause: >-
  A data node crossed the storage flood-stage watermark; the cluster
  flipped indices to read-only; the test's writes were rejected. The
  test is correct; the environment ran out of disk.
cause_class: INFRA
confidence: high            # low | medium | high
supporting_evidence:
  - "First error is a write rejection, not a test assertion."
  - "Disk on node-2 at 94% at the failure timestamp."
  - "All downstream errors are timeout/retry cascade."
falsifying_test: >-
  If disk on every data node was below the watermark at 10:02:48, this
  cause is wrong — re-check node-2's disk timeline at that timestamp.
ruled_out:
  - "TEST-BUG: the assertion logic is unchanged and passed yesterday."
```

## Prompt template

> You are committing to a single root cause. Input: {findings_state}.
> 1. Weigh the hypotheses. Prefer the one that explains the FIRST error
>    and the cascade, not just the loudest symptom.
> 2. Assign a confidence level and justify it from evidence, not vibes.
> 3. Write the cheapest test that would falsify your conclusion. If you
>    cannot write one, your confidence is at most medium.
> 4. List what you ruled out and why — this is as valuable as the cause.
> 5. If evidence is insufficient, say so and name the one missing piece
>    that would decide it, rather than forcing a conclusion.
> Output the structured result.

## Examples

- **Write rejection + disk at 94%.** → INFRA, high confidence,
  falsifiable by the disk timeline.
- **Assertion failure on unordered data.** → TEST-BUG, high confidence;
  falsifying test is whether the system ever guaranteed order.

## Composition

The terminal node of the triage chain. Feeds
`create_verification_strategy` so the fix is verified against the cause
it actually identified, and feeds the journal entry in an
operational-memory system.
