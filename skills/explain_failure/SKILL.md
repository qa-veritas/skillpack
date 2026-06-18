---
name: explain_failure
description: >-
  Translate an error signature plus surrounding log and code context
  into a plain-language explanation and a likely cause class. Use when
  an error message is cryptic or when handing a failure to someone who
  lacks the codebase context.
tags: [error, logs, explanation, triage, rca]
---

# explain_failure

## Purpose

Most error messages describe the symptom at the point of detection, not
the cause. `FORBIDDEN/8/index write (api)` does not say "the cluster
went read-only because a disk crossed the flood-stage watermark." This
skill bridges that gap using the code that emitted the line.

## Inputs

- `error_signature` — the exact error string / exception / status code.
- `log_context` — the surrounding lines (what happened just before).
- `code_context` (optional) — the source location that emits this
  error, recovered by correlating the `file:line` token to the tree
  (see `summarize_logs` / the loglens repo).

## Outputs

```yaml
explanation: >-
  The cluster rejected writes because a node crossed the storage
  flood-stage watermark and flipped indices to read-only. The write
  path surfaces this as FORBIDDEN, which looks like a permissions
  error but is a capacity guard.
cause_class: INFRA            # TEST-BUG | INFRA | FRAMEWORK | PRODUCT | HANG
blast_radius: >-
  All writes to affected indices, cluster-wide, until the watermark
  clears and the read-only block is released.
likely_triggers:
  - "Disk above flood-stage watermark on at least one data node"
  - "Retention/rotation not reclaiming space"
```

## Prompt template

> You are explaining a failure to an engineer who does not have the
> codebase loaded. Inputs: signature {error_signature}, log context
> {log_context}, code context {code_context}.
> 1. Separate the symptom (where it was detected) from the cause (why it
>    happened). Name both.
> 2. Use the code context to explain what condition the emitting code
>    was guarding against — many "permission" or "validation" errors are
>    really capacity, timing, or state guards.
> 3. Assign a cause class. Be willing to say PRODUCT (the system under
>    test is genuinely broken) vs TEST-BUG (the test asked for something
>    impossible).
> 4. State the blast radius honestly: one request, one workload, or the
>    whole cluster.
> Keep the explanation to a short paragraph. No restating the stack
> trace.

## Examples

- **`context deadline exceeded` on a control-plane call.** → symptom is
  a client timeout; cause class often INFRA (slow/over-loaded API) or
  PRODUCT (a handler that blocks). Code context disambiguates.
- **AssertionError comparing a list in order.** → cause class TEST-BUG;
  the assertion assumed ordering the system does not guarantee.

## Composition

Consumes the output of `summarize_logs`. Feeds `identify_root_cause` as
one weighted hypothesis.
