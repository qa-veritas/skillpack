"""Level 2: parse a skill's ``SKILL.md`` into frontmatter + body.

The body is only ever read when a task matches the skill — that's the
whole point of progressive disclosure. This module does the parsing; the
decision to load is made by the matcher and the CLI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


class SkillError(ValueError):
    """Raised when a SKILL.md is missing or has malformed frontmatter."""


@dataclass
class Skill:
    """A parsed skill: metadata from frontmatter, plus the instructions."""

    name: str
    description: str
    body: str
    tags: list[str] = field(default_factory=list)
    directory: Path | None = None

    @property
    def has_smoke(self) -> bool:
        return bool(self.directory) and (self.directory / "scripts" / "smoke.sh").exists()


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        raise SkillError("SKILL.md must start with YAML frontmatter delimited by ---")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SkillError("unterminated frontmatter; expected a closing ---")
    meta = yaml.safe_load(parts[1]) or {}
    return meta, parts[2].strip()


def load_skill(skill_dir: str | Path) -> Skill:
    """Load a skill from its directory (containing ``SKILL.md``).

    Raises:
        SkillError: If ``SKILL.md`` is missing or its frontmatter lacks a
            name or description.
    """
    skill_dir = Path(skill_dir)
    md = skill_dir / "SKILL.md" if skill_dir.is_dir() else skill_dir
    if not md.exists():
        raise SkillError(f"no SKILL.md at {skill_dir}")

    meta, body = _split_frontmatter(md.read_text())
    for required in ("name", "description"):
        if required not in meta:
            raise SkillError(f"{md}: frontmatter missing {required!r}")

    return Skill(
        name=meta["name"],
        description=" ".join(str(meta["description"]).split()),
        body=body,
        tags=list(meta.get("tags", [])),
        directory=md.parent,
    )
