"""Github_rank_agent 入口。

每週排行整理流程：
    1. 初始化 / 確認 research_github.db（依 database/schema.sql）
    2. 對每個已啟用的「篩選方式」抓本週排行
    3. UPSERT 進 research_github（保留個人欄位）

第一個篩選方式：OpenGithubs/github-weekly-rank。
"""
from __future__ import annotations

import sys

from github_rank_agent import storage
from github_rank_agent.sources import ENABLED_SOURCES

# Windows 終端預設非 UTF-8，避免中文輸出亂碼
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def run() -> None:
    """執行一次每週排行抓取與寫入。"""
    storage.init_db()
    total = 0
    for source in ENABLED_SOURCES:
        try:
            records = source.fetch()
        except Exception as exc:  # 單一來源失敗不影響其他來源
            print(f"[skip] {source.name}: 抓取失敗 - {exc}")
            continue
        n = storage.upsert_records(records)
        total += n
        print(f"[ok]   {source.name}: 抓到 {n} 筆")
    print(f"完成：共寫入/更新 {total} 筆 -> {storage.config.DB_PATH}")


if __name__ == "__main__":
    run()
