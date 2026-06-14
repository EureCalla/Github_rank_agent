"""每週摘要產生。

比較本週與上週排名，整理出新進榜、排名上升 / 下降的 repo（見 DESIGN.md）。
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .models import RepoRecord


@dataclass
class WeeklySummary:
    """一週排名摘要的資料格式。"""

    week: str
    new_entries: list[RepoRecord] = field(default_factory=list)   # 新進榜
    rank_up: list[RepoRecord] = field(default_factory=list)       # 排名上升
    rank_down: list[RepoRecord] = field(default_factory=list)     # 排名下降


def build_weekly_summary(
    current: list[RepoRecord],
    previous: list[RepoRecord],
    week: str,
) -> WeeklySummary:
    """比較本週與上週排名並產生摘要。

    Note:
        尚未實作。
    """
    raise NotImplementedError("每週摘要產生尚未實作")
