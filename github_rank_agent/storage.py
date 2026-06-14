"""research_github.db 的儲存與讀取（SQLite）。

三張表以 repo_full_name 串接：
- research_github：週排行快照，由抓取流程 UPSERT；不含個人資料。
- repo_evaluation：個人評價（rating / notes）。
- repo_research：深度研究狀態（interested -> researching -> done）。

抓取流程只動 research_github，絕不碰個人表。
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from . import config
from .models import RepoRecord

VALID_STATUS = ("interested", "researching", "done")

# UPSERT 衝突時會被來源更新的欄位（language 另以 COALESCE 處理）
_SOURCE_COLUMNS = (
    "rank",
    "repo_url",
    "total_stars",
    "weekly_growth",
    "monthly_growth",
    "created_date",
    "description",
    "fetched_at",
)


def _connect(db_path: Path = config.DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path = config.DB_PATH, schema_path: Path = config.SCHEMA_PATH) -> None:
    """依 schema.sql 初始化三張表（不存在時建立）。"""
    schema = schema_path.read_text(encoding="utf-8")
    with _connect(db_path) as conn:
        conn.executescript(schema)


# --------------------------------------------------------------------------- #
# 週排行（research_github）
# --------------------------------------------------------------------------- #
def upsert_records(records: list[RepoRecord], db_path: Path = config.DB_PATH) -> int:
    """寫入/更新一批抓取結果。

    衝突鍵 (source, week, repo_full_name)；衝突時只更新來源欄位，
    language 僅在新值非 NULL 時覆蓋（避免日後 API 補的語言被洗掉）。
    """
    set_clause = ",\n        ".join(f"{c}=excluded.{c}" for c in _SOURCE_COLUMNS)
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


def latest_week(db_path: Path = config.DB_PATH) -> str | None:
    """research_github 中最新的週別。"""
    with _connect(db_path) as conn:
        row = conn.execute("SELECT MAX(week) FROM research_github").fetchone()
    return row[0] if row else None


def load_week_digest(
    week: str | None = None, db_path: Path = config.DB_PATH
) -> list[sqlite3.Row]:
    """讀某週排行，LEFT JOIN 個人評價與研究狀態，依 rank 排序。

    week 省略時取 latest_week()。
    """
    with _connect(db_path) as conn:
        if week is None:
            week = conn.execute("SELECT MAX(week) FROM research_github").fetchone()[0]
        return conn.execute(
            """
            SELECT g.source, g.week, g.rank, g.repo_full_name, g.repo_url,
                   g.total_stars, g.weekly_growth, g.monthly_growth,
                   g.created_date, g.description, g.language,
                   e.personal_rating, e.personal_notes,
                   r.status AS research_status
            FROM research_github g
            LEFT JOIN repo_evaluation e ON e.repo_full_name = g.repo_full_name
            LEFT JOIN repo_research   r ON r.repo_full_name = g.repo_full_name
            WHERE g.week = :week
            ORDER BY g.rank ASC
            """,
            {"week": week},
        ).fetchall()


# --------------------------------------------------------------------------- #
# 個人評價（repo_evaluation）
# --------------------------------------------------------------------------- #
def set_evaluation(
    repo_full_name: str,
    rating: int | None = None,
    notes: str | None = None,
    db_path: Path = config.DB_PATH,
) -> None:
    """設定/更新個人評價。只更新有給的欄位（None 不動）。"""
    if rating is not None and not 1 <= rating <= 10:
        raise ValueError("personal_rating 需介於 1~10")
    sql = """
    INSERT INTO repo_evaluation (repo_full_name, personal_rating, personal_notes, updated_at)
    VALUES (:repo, :rating, :notes, datetime('now','localtime'))
    ON CONFLICT(repo_full_name) DO UPDATE SET
        personal_rating=COALESCE(:rating, repo_evaluation.personal_rating),
        personal_notes =COALESCE(:notes,  repo_evaluation.personal_notes),
        updated_at=datetime('now','localtime')
    """
    with _connect(db_path) as conn:
        conn.execute(sql, {"repo": repo_full_name, "rating": rating, "notes": notes})


# --------------------------------------------------------------------------- #
# 深度研究（repo_research）
# --------------------------------------------------------------------------- #
def set_research_status(
    repo_full_name: str, status: str, db_path: Path = config.DB_PATH
) -> None:
    """設定研究狀態；切到 interested 補 interested_at、切到 done 補 researched_at。"""
    if status not in VALID_STATUS:
        raise ValueError(f"status 需為 {VALID_STATUS} 之一")
    interested_at = "datetime('now','localtime')" if status == "interested" else "NULL"
    researched_at = "datetime('now','localtime')" if status == "done" else "NULL"
    sql = f"""
    INSERT INTO repo_research (repo_full_name, status, interested_at, researched_at)
    VALUES (:repo, :status, {interested_at}, {researched_at})
    ON CONFLICT(repo_full_name) DO UPDATE SET
        status=:status,
        interested_at=COALESCE(repo_research.interested_at, {interested_at}),
        researched_at=CASE WHEN :status='done' THEN {researched_at}
                           ELSE repo_research.researched_at END
    """
    with _connect(db_path) as conn:
        conn.execute(sql, {"repo": repo_full_name, "status": status})


def mark_interested(repo_full_name: str, db_path: Path = config.DB_PATH) -> None:
    """標記為「想進一步研究」。"""
    set_research_status(repo_full_name, "interested", db_path)


def mark_researched(repo_full_name: str, db_path: Path = config.DB_PATH) -> None:
    """標記為「已研究完畢」。"""
    set_research_status(repo_full_name, "done", db_path)


def get_research(
    status: str | None = None, db_path: Path = config.DB_PATH
) -> list[sqlite3.Row]:
    """列出研究狀態；status 省略時回傳全部。"""
    with _connect(db_path) as conn:
        if status is None:
            return conn.execute(
                "SELECT * FROM repo_research ORDER BY interested_at DESC"
            ).fetchall()
        return conn.execute(
            "SELECT * FROM repo_research WHERE status = :s ORDER BY interested_at DESC",
            {"s": status},
        ).fetchall()
