---
name: summarize_logs
description: >-
  Compress a log slice into a timeline, clustered errors, and a
  one-paragraph summary. Never read a multi-GB log end to end. Use to
  make a large log tractable.
tags: [logs, summary, timeline, triage, observability]
---

# summarize_logs

## Purpose

Large run logs are too big to read and too important to skip. Find the
*first* error (not the loudest), build a timeline, cluster repeated
noise, and hand back something a human can act on in a minute.

## Inputs

- `log_slice_or_brief` — a bounded slice (a window around the first
  error) or a tiered brief from a code-aware slicer. Never the full
  multi-GB file.

## Outputs

`timeline` (last good checkpoint → first error → cascade onset),
`error_clusters` (signature + count + first flag), a one-paragraph
`summary`, and `emitting_paths` if the slice carries `file:line` tokens.

## Prompt template

> Find the FIRST error by timestamp, not the most frequent. Build a
> short timeline. Cluster repeated errors by signature with counts and
> state plainly which clusters are noise downstream of the first error.
> If the slice has `file:line` tokens, name the emitting code paths.
> Don't paste raw log lines beyond a short quote of the first error.

## Examples

- 214 timeouts after one rejected write → one cause, 213 symptoms.
- No errors, log just stops → likely HANG; report the last progress line
  and the gap to end-of-log.
