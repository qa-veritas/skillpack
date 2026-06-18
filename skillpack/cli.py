"""Command-line entrypoint for skillpack.

Subcommands:
    list       Level 1: print skill metadata
    match      rank skills against a task description
    show       Level 2: print a skill's full instructions
    smoke      Level 3: run a skill's smoke check
    validate   confirm every registered skill has a valid SKILL.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skillpack.loader import SkillError, load_skill
from skillpack.match import match_task
from skillpack.registry import RegistryError, enabled, load_registry
from skillpack.smoke import run_smoke

DEFAULT_ROOT = Path(".")


def _entries(root: Path):
    return load_registry(root)


def cmd_list(args: argparse.Namespace) -> int:
    for entry in _entries(args.root):
        flag = " " if entry.enabled else "x"
        print(f"[{flag}] {entry.name:24} {entry.description[:70]}")
    return 0


def cmd_match(args: argparse.Namespace) -> int:
    matches = match_task(args.task, enabled(_entries(args.root)))
    if not matches:
        print("no matching skills")
        return 0
    for rank, match in enumerate(matches, start=1):
        print(f"{rank}. {match.entry.name:24} score {match.score:<6} {match.entry.description[:60]}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    entry = next((e for e in _entries(args.root) if e.name == args.name), None)
    if entry is None:
        print(f"no such skill: {args.name}", file=sys.stderr)
        return 1
    skill = load_skill(args.root / entry.path)
    print(f"# {skill.name}\n")
    print(skill.description + "\n")
    print(skill.body)
    return 0


def cmd_smoke(args: argparse.Namespace) -> int:
    entries = _entries(args.root)
    targets = [e for e in entries if e.name == args.name] if args.name else enabled(entries)
    failures = 0
    for entry in targets:
        skill = load_skill(args.root / entry.path)
        result = run_smoke(skill)
        print(f"{result.status:8} {result.skill:24} {result.detail}")
        failures += result.status == "failed"
    return 1 if failures else 0


def cmd_validate(args: argparse.Namespace) -> int:
    failures = 0
    for entry in _entries(args.root):
        try:
            load_skill(args.root / entry.path)
            print(f"ok    {entry.name}")
        except SkillError as error:
            failures += 1
            print(f"FAIL  {entry.name}: {error}")
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skillpack", description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="repo root (holds registry.yaml)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="list skill metadata").set_defaults(func=cmd_list)

    p_match = sub.add_parser("match", help="rank skills against a task")
    p_match.add_argument("task")
    p_match.set_defaults(func=cmd_match)

    p_show = sub.add_parser("show", help="print a skill's full instructions")
    p_show.add_argument("name")
    p_show.set_defaults(func=cmd_show)

    p_smoke = sub.add_parser("smoke", help="run smoke checks")
    p_smoke.add_argument("name", nargs="?")
    p_smoke.set_defaults(func=cmd_smoke)

    sub.add_parser("validate", help="validate every SKILL.md").set_defaults(func=cmd_validate)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (RegistryError, SkillError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
