"""Match a task description to the skills that should load.

Deliberately simple and transparent: token overlap (Jaccard-ish) over a
skill's name, description, and tags. The value is not a clever ranker —
it's that the agent only pays the Level-2 token cost for the skills a
task actually needs. The matcher is a single function so it can be
swapped for an embedding-based one behind the same signature.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from skillpack.registry import RegistryEntry

_TOKEN = re.compile(r"[a-z0-9]+")

# Words that carry no routing signal; ignored on both sides.
_STOP = frozenset(
    """
    a an the of to and or for in on at is are be will would should can could
    it this that these those with without my our your we i you they them
    use used using when how what why where which into out up down over under
    """.split()
)


def _tokens(text: str) -> set[str]:
    return {t for t in _TOKEN.findall(text.lower()) if t not in _STOP and len(t) > 2}


@dataclass
class Match:
    """A skill and its relevance score for a task."""

    entry: RegistryEntry
    score: float


def match_task(task: str, entries: list[RegistryEntry], top: int = 5) -> list[Match]:
    """Rank skills by token overlap with the task.

    Args:
        task: The user's task description.
        entries: Registry entries to rank (enabled ones, typically).
        top: Maximum matches to return.

    Returns:
        Matches with a positive score, highest first, capped at ``top``.
    """
    task_tokens = _tokens(task)
    if not task_tokens:
        return []

    matches: list[Match] = []
    for entry in entries:
        skill_tokens = _tokens(entry.name.replace("_", " ") + " " + entry.description)
        skill_tokens |= {t for tag in entry.tags for t in _tokens(tag)}
        if not skill_tokens:
            continue
        overlap = task_tokens & skill_tokens
        if not overlap:
            continue
        score = len(overlap) / len(task_tokens | skill_tokens)
        matches.append(Match(entry=entry, score=round(score, 3)))

    matches.sort(key=lambda m: m.score, reverse=True)
    return matches[:top]
