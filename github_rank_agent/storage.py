"""排名研究資料的儲存與讀取（SQLite）。

research_github.db 納入 git 追蹤；schema 由 database/schema.sql 初始化。
重抓時以 UPSERT 更新來源欄位，但「保留」個人欄位
（personal_rating / deep_research / personal_notes）。
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from . import config
from .models import RepoRecord

# UPSERT 時會被來源資料更新的欄位（個人欄位刻意不在內）
_SOURCE_COLUMNS = (
    "rank",
    "repo_url",
    "total_stars",
    "weekly_growth",
    "monthly_growth",
    "created_date",
    "description",
    "language",
    "fetched_at",
)


def _connect(db_path: Path = config.DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path = config.DB_PATH, schema_path: Path = config.SCHEMA_PATH) -> None:
    """依 ``schema.sql`` 初始化 SQLite 資料庫（不存在時建立）。"""
    schema = schema_path.read_text(encoding="utf-8")
    with _connect(db_path) as conn:
        conn.executescript(schema)


def upsert_records(records: list[RepoRecord], db_path: Path = config.DB_PATH) -> int:
    """寫入/更新一批抓取結果。

    衝突鍵為 (source, week, repo_full_name)。衝突時只更新來源欄位，
    保留使用者填寫的個人欄位。``language`` 僅在新值非 NULL 時才覆蓋，
    避免之後用 API 補的語言被無語言來源洗掉。

    Returns:
        實際處理的列數。
    """
    set_clause = ",\n        ".join(
        f"{col}=excluded.{col}" for col in _SOURCE_COLUMNS if col != "language"
    )
    sql = f"""
    INSERT INTO research_github
        (source, week, rank, repo_full_name, repo_url,
         total_stars, weekly_growth, monthly_growth, created_date,
         description, language, fetched_at)
    VALUES
        (:source, :week, :rank, :repo_full_name, :repo_url,
         :total_stars, :weekly_growth, :monthly_growth, :created_date,
         :description, :language, datetime('now','localtime'))
    ON CONFLICT(source, week, repo_full_name) DO UPDATE SET
        {set_clause},
        language=COALESCE(excluded.language, research_github.language)
    """
    rows = [
        {
            "source": r.source,
            "week": r.week,
            "rank": r.rank,
            "repo_full_name": r.repo_full_name,
            "repo_url": r.repo_url,
            "total_stars": r.total_stars,
            "weekly_growth": r.weekly_growth,
            "monthly_growth": r.monthly_growth,
            "created_date": r.created_date,
            "description": r.description,
            "language": r.language,
        }
        for r in records
    ]
    with _connect(db_path) as conn:
        conn.executemany(sql, rows)
    return len(rows)


def load(
    week: str | None = None,
    source: str | None = None,
    db_path: Path = config.DB_PATH,
) -> list[sqlite3.Row]:
    """讀取研究資料；可依週別 / 來源篩選，預設依名次排序。"""
    clauses = []
    params: dict[str, object] = {}
    if week is not None:
        clauses.append("week = :week")
        params["week"] = week
    if source is not None:
        clauses.append("source = :source")
        params["source"] = source
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    sql = f"SELECT * FROM research_github {where} ORDER BY week DESC, rank ASC"
    with _connect(db_path) as conn:
        return conn.execute(sql, params).fetchall()
