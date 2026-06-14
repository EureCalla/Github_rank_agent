"""集中管理設定：路徑與敏感資訊。

敏感資訊（GitHub API token）一律從環境變數載入，不得寫入 repo（見 AGENTS.md）。
"""
from __future__ import annotations

import os
from pathlib import Path

# 專案根目錄（本檔位於 github_rank_agent/ 之下）
ROOT = Path(__file__).resolve().parent.parent

DATABASE_DIR = ROOT / "database"
# 研究資料庫：納入 git 追蹤（本 repo 的研究資產）
DB_PATH = DATABASE_DIR / "research_github.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"
OUTPUT_DIR = ROOT / "output"                      # 報告輸出，不進 git

# GitHub API token 對應的環境變數名稱。
# 目前主流程（抓週排行）不需要 token；保留供未來補抓語言等 enrichment 使用（選填）。
GITHUB_TOKEN_ENV = "GITHUB_TOKEN"


def get_github_token() -> str | None:
    """從環境變數讀取 GitHub API token；未設定時回傳 None。"""
    return os.environ.get(GITHUB_TOKEN_ENV)
