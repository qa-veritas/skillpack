"""Level 3: run a skill's smoke check.

A smoke check is a cheap, read-only command that proves the skill's
prerequisites work (an endpoint is reachable, credentials are set)
before an agent relies on it. Skills without one simply report
"skipped" and are considered to pass on validation alone.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from skillpack.loader import Skill


@dataclass
class SmokeResult:
    """Outcome of a smoke run."""

    skill: str
    status: str          # passed | failed | skipped
    detail: str = ""


def run_smoke(skill: Skill, timeout: int = 30) -> SmokeResult:
    """Run ``scripts/smoke.sh`` for a skill if present.

    Args:
        skill: The loaded skill.
        timeout: Seconds before the smoke command is killed.

    Returns:
        A :class:`SmokeResult`. ``skipped`` when no smoke script exists.
    """
    if not skill.directory:
        return SmokeResult(skill.name, "skipped", "no directory")

    directory = Path(skill.directory).resolve()
    script = directory / "scripts" / "smoke.sh"
    if not script.exists():
        return SmokeResult(skill.name, "skipped", "no scripts/smoke.sh")

    try:
        proc = subprocess.run(
            ["bash", str(script)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(directory),
        )
    except subprocess.TimeoutExpired:
        return SmokeResult(skill.name, "failed", f"timed out after {timeout}s")

    if proc.returncode == 0:
        return SmokeResult(skill.name, "passed", proc.stdout.strip()[:200])
    return SmokeResult(skill.name, "failed", (proc.stderr or proc.stdout).strip()[:200])
