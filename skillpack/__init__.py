"""skillpack: progressive-disclosure agent skills.

Level 1 metadata is always cheap; Level 2 instructions load on match;
Level 3 resources load only when referenced.
"""

from skillpack.loader import Skill, load_skill
from skillpack.match import match_task
from skillpack.registry import RegistryEntry, load_registry

__all__ = ["RegistryEntry", "Skill", "load_registry", "load_skill", "match_task"]

__version__ = "0.1.0"
