"""排名資料儲存與讀取（SQLite）。

DB 檔本身不進 git（見 .gitignore）；schema 由 database/schema.sql 初始化。
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from . import config
from .github_client import RepoRecord


def init_db(db_path: Path = config.DB_PATH, schema_path: Path = config.SCHEMA_PATH) -> None:
    """依 ``schema.sql`` 初始化 SQLite 資料庫（不存在時建立）。"""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema = schema_path.read_text(encoding="utf-8")
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema)


def save_rankings(
    records: list[RepoRecord],
    snapshot_date: str,
    week: str,
    query: str,
    db_path: Path = config.DB_PATH,
) -> None:
    """寫入一週排名快照。

    Note:
        尚未實作；需把 :class:`RepoRecord` 與名次寫入 ``weekly_rankings``。
    """
    raise NotImplementedError("排名快照寫入尚未實作")


def load_rankings(week: str, query: str, db_path: Path = config.DB_PATH) -> list[RepoRecord]:
    """讀取指定週、指定查詢條件的排名。

    Note:
        尚未實作。
    """
    raise NotImplementedError("排名讀取尚未實作")
