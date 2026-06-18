# skillpack

[![ci](https://github.com/qa-veritas/skillpack/actions/workflows/ci.yml/badge.svg)](https://github.com/qa-veritas/skillpack/actions/workflows/ci.yml)

**A tiny framework for progressive-disclosure agent skills: cheap
metadata always, full instructions on match, heavy resources only when
referenced.**

Stuffing every capability an agent might need into one system prompt
burns context and makes the agent worse at all of them. `skillpack`
borrows the progressive-disclosure model: a skill exposes ~100 tokens of
metadata that's always available, a full `SKILL.md` body that loads only
when a task matches its description, and `scripts/` + `kb/` resources
that load only when the skill references them.

```
Level 1  registry.yaml + SKILL.md frontmatter   always loaded   ~100 tokens/skill
Level 2  SKILL.md body                            on match        < 5k tokens
Level 3  scripts/, kb/                            on reference     unbounded (run via shell)
```

A skill is **self-contained, composable, prompt-driven, and
filesystem-based.** It carries knowledge, not a fixed command list.

## Install

```bash
pip install -e .
python -m skillpack --help
```

Python 3.10+. Runtime dependency: `pyyaml`.

## Use

```bash
# Level 1 — list available skills (metadata only)
python -m skillpack list

# Match a task to the skills that should load
python -m skillpack match "the data mount is filling up, will it run out tonight"

# Level 2 — load one skill's full instructions
python -m skillpack show check_disk_pressure

# Level 3 — run a skill's smoke check (if it ships one)
python -m skillpack smoke check_disk_pressure

# Validate the registry: every listed skill has a well-formed SKILL.md
python -m skillpack validate
```

### Example: matching

```
$ python -m skillpack match "the data mount is filling up, will it run out tonight"
1. check_disk_pressure   score 0.42   Decide whether storage is under pressure...
2. analyze_cluster_health score 0.11  Turn a cluster health snapshot into a verdict...
```

Matching is deliberately simple and transparent (token overlap over
name + description + tags). The point isn't a clever ranker; it's that
the agent only pays the token cost of the skills a task actually needs.

## Authoring a skill

```
skills/<name>/
  SKILL.md            # YAML frontmatter (name, description) + body
  scripts/smoke.sh    # optional: a cheap read that proves the skill works
  kb/<ref>.md         # optional: reference material loaded on demand
```

`SKILL.md` frontmatter:

```yaml
---
name: check_disk_pressure
description: >-
  Decide whether a node's storage is under pressure and recommend an
  action. Use when a mount is filling or capacity planning needs a verdict.
tags: [storage, capacity, triage]
---
```

Then register it in `registry.yaml`. See the three bundled example
skills.

## Layout

```
skillpack/
  skillpack/
    __init__.py
    registry.py    # Level 1: load + validate registry.yaml
    loader.py      # Level 2: parse SKILL.md frontmatter + body
    match.py       # task -> ranked skills (transparent token overlap)
    smoke.py       # Level 3: run a skill's smoke script
    cli.py         # list / match / show / smoke / validate
  skills/
    check_disk_pressure/
    summarize_logs/
    analyze_cluster_health/
  registry.yaml
  tests/
  LICENSE
  pyproject.toml
```

## Roadmap

- Pluggable matchers (embedding-based) behind the same interface, so the
  token-overlap default can be swapped without touching callers.
- A `bundle` command to export the matched skills as a single context
  payload for a headless agent run.
- Skill dependency edges (`composes_with`) surfaced in `match` so a
  matched skill pulls its collaborators.
- Per-skill versioning and a `diff` against the installed set.

## License

MIT. See [LICENSE](LICENSE).
