"""篩選方式（來源）註冊表。

新增來源：實作一個 base.Source 子類，再加進 ENABLED_SOURCES。
"""
from __future__ import annotations

from .base import Source
from .opengithubs_weekly import OpenGithubsWeeklySource

# 進場時會依序抓取的篩選方式
ENABLED_SOURCES: list[Source] = [
    OpenGithubsWeeklySource(),
]

__all__ = ["Source", "OpenGithubsWeeklySource", "ENABLED_SOURCES"]
