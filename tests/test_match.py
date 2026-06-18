from skillpack.match import match_task
from skillpack.registry import RegistryEntry


def _entries():
    return [
        RegistryEntry("check_disk_pressure", "skills/check_disk_pressure",
                      "Decide whether storage is under pressure and recommend an action.",
                      tags=["storage", "disk", "capacity"]),
        RegistryEntry("analyze_cluster_health", "skills/analyze_cluster_health",
                      "Turn a cluster health snapshot into a verdict and next checks.",
                      tags=["cluster", "health"]),
        RegistryEntry("summarize_logs", "skills/summarize_logs",
                      "Compress a log slice into a timeline and summary.",
                      tags=["logs", "timeline"]),
    ]


def test_disk_task_ranks_disk_skill_first():
    matches = match_task("the data disk mount is filling up, storage capacity low", _entries())
    assert matches
    assert matches[0].entry.name == "check_disk_pressure"


def test_log_task_ranks_log_skill_first():
    matches = match_task("summarize this huge log timeline for me", _entries())
    assert matches[0].entry.name == "summarize_logs"


def test_no_overlap_returns_empty():
    assert match_task("xyzzy frobnicate", _entries()) == []


def test_scores_are_descending():
    matches = match_task("cluster health and node storage disk", _entries())
    scores = [m.score for m in matches]
    assert scores == sorted(scores, reverse=True)
