"""GitHub 查詢與 API client。

負責呼叫 GitHub Search API 取得 repo 排名資料。
目前僅定義資料格式與介面，實際查詢尚未實作（見 AGENTS.md：先定義資料格式，再實作抓取流程）。
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RepoRecord:
    """單一 repo 的查詢結果資料格式（對應 database/schema.sql 的 weekly_rankings）。"""

    full_name: str                       # owner/name
    stars: int = 0
    forks: int = 0
    language: str | None = None
    topics: list[str] = field(default_factory=list)


class GithubClient:
    """GitHub Search API 的薄包裝。"""

    def __init__(self, token: str | None = None) -> None:
        self.token = token

    def search_top_repos(self, query: str, limit: int = 50) -> list[RepoRecord]:
        """依查詢條件取得排名前 ``limit`` 的 repo。

        Args:
            query: GitHub search 查詢字串（例如 ``"stars:>1000 language:python"``）。
            limit: 取回的 repo 數量上限。

        Returns:
            依名次排序的 :class:`RepoRecord` 清單。

        Note:
            尚未實作；之後接上 GitHub Search API 時再補 ``requirements.txt``。
        """
        raise NotImplementedError("GitHub Search API 查詢尚未實作")
