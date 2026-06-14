"""Github_rank_agent 入口。

串接每週排名整理流程（目前為骨架，尚未完整實作）：
    1. 查詢 GitHub 排名         -> github_rank_agent.github_client
    2. 儲存本週快照             -> github_rank_agent.storage
    3. 與上週比較產生摘要        -> github_rank_agent.summary
    4. 輸出報告                 -> github_rank_agent.report

GitHub API token 透過環境變數 GITHUB_TOKEN 載入（見 github_rank_agent.config）。
"""
from __future__ import annotations

from github_rank_agent import config, storage
from github_rank_agent.github_client import GithubClient


def run_weekly(query: str = "stars:>1000", limit: int = 50) -> None:
    """執行一次每週排名整理流程。

    Note:
        各步驟的實作仍為 stub，串接邏輯待後續補上。
    """
    storage.init_db()
    client = GithubClient(token=config.get_github_token())
    # TODO: 查詢 -> 儲存 -> 摘要 -> 報告
    raise NotImplementedError("每週流程尚未實作")


if __name__ == "__main__":
    run_weekly()
