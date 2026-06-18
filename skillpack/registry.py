"""Level 1: the always-loaded skill metadata.

The registry is the cheap index: name, path, description, tags, enabled.
It is what an agent sees at startup. The full instructions live in each
skill's ``SKILL.md`` and load only when a task matches.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


class RegistryError(ValueError):
    """Raised when the registry or a referenced skill is malformed."""


@dataclass
class RegistryEntry:
    """One skill's metadata as listed in the registry."""

    name: str
    path: str
    description: str
    enabled: bool = True
    tags: list[str] = field(default_factory=list)


def load_registry(path: str | Path) -> list[RegistryEntry]:
    """Load and validate ``registry.yaml`` into entries.

    Args:
        path: Path to ``registry.yaml`` or its containing directory.

    Returns:
        The enabled-and-disabled entries, in registry order.

    Raises:
        RegistryError: If the file is missing or an entry lacks a name,
            path, or description.
    """
    path = Path(path)
    if path.is_dir():
        path = path / "registry.yaml"
    if not path.exists():
        raise RegistryError(f"no registry at {path}")

    data = yaml.safe_load(path.read_text()) or {}
    entries: list[RegistryEntry] = []
    for raw in data.get("skills", []):
        for required in ("name", "path", "description"):
            if required not in raw:
                raise RegistryError(f"skill entry missing {required!r}: {raw}")
        entries.append(
            RegistryEntry(
                name=raw["name"],
                path=raw["path"],
                description=" ".join(raw["description"].split()),
                enabled=bool(raw.get("enabled", True)),
                tags=list(raw.get("tags", [])),
            )
        )
    return entries


def enabled(entries: list[RegistryEntry]) -> list[RegistryEntry]:
    """Filter to the enabled entries only."""
    return [entry for entry in entries if entry.enabled]
