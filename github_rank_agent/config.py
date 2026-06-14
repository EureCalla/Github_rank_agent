"""集中管理設定：路徑與敏感資訊。

敏感資訊（GitHub API token）一律從環境變數載入，不得寫入 repo（見 AGENTS.md）。
"""
from __future__ import annotations

import os
from pathlib import Path

# 專案根目錄（本檔位於 github_rank_agent/ 之下）
ROOT = Path(__file__).resolve().parent.parent

DATABASE_DIR = ROOT / "database"
DB_PATH = DATABASE_DIR / "github_rank.db"        # 本機快取，不進 git
SCHEMA_PATH = DATABASE_DIR / "schema.sql"
OUTPUT_DIR = ROOT / "output"                      # 報告輸出，不進 git

# GitHub API token 對應的環境變數名稱
GITHUB_TOKEN_ENV = "GITHUB_TOKEN"


def get_github_token() -> str | None:
    """從環境變數讀取 GitHub API token；未設定時回傳 None。"""
    return os.environ.get(GITHUB_TOKEN_ENV)
