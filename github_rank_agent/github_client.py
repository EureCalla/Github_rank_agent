"""GitHub API enrichment（選填，未來用）。

本 repo 主流程（抓週排行）是用 sources/ 底下的篩選方式從現成排行頁面抓資料，
不需要 GitHub API token。此模組保留給「未來」用 GitHub API 補來源沒有的欄位
（例如 language、forks、topics），目前尚未使用。
"""
from __future__ import annotations

from .models import RepoRecord


class GithubClient:
    """GitHub REST API 的薄包裝（enrichment 用，尚未實作）。"""

    def __init__(self, token: str | None = None) -> None:
        self.token = token

    def enrich_language(self, record: RepoRecord) -> RepoRecord:
        """以 GitHub API 補上 repo 的主要語言。

        Note:
            尚未實作；之後查 ``GET /repos/{owner}/{repo}`` 填入 ``record.language``。
        """
        raise NotImplementedError("GitHub API enrichment 尚未實作")
