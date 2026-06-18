from pathlib import Path

import pytest

from skillpack.loader import SkillError, load_skill
from skillpack.registry import RegistryError, load_registry

ROOT = Path(__file__).resolve().parents[1]


def test_registry_loads_bundled_skills():
    entries = load_registry(ROOT)
    names = {e.name for e in entries}
    assert {"check_disk_pressure", "summarize_logs", "analyze_cluster_health"} <= names


def test_every_registered_skill_loads():
    for entry in load_registry(ROOT):
        skill = load_skill(ROOT / entry.path)
        assert skill.name == entry.name
        assert skill.body


def test_check_disk_pressure_has_smoke():
    skill = load_skill(ROOT / "skills/check_disk_pressure")
    assert skill.has_smoke


def test_missing_frontmatter_raises(tmp_path):
    (tmp_path / "SKILL.md").write_text("no frontmatter here")
    with pytest.raises(SkillError):
        load_skill(tmp_path)


def test_missing_registry_raises(tmp_path):
    with pytest.raises(RegistryError):
        load_registry(tmp_path)
