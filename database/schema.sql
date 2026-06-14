-- Github_rank_agent SQLite schema
-- 先定義資料格式，再實作抓取流程（見 AGENTS.md）。
-- 實際 .db 檔不進 git（見 .gitignore），本檔為初始化腳本。

-- 每週排名快照：一列代表某次查詢中某個 repo 的排名結果
CREATE TABLE IF NOT EXISTS weekly_rankings (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date  TEXT    NOT NULL,            -- 查詢日期 YYYY-MM-DD
    week           TEXT    NOT NULL,            -- ISO 週別 YYYY-Www
    rank           INTEGER NOT NULL,            -- 本次查詢中的名次（1 起算）
    repo_full_name TEXT    NOT NULL,            -- owner/name
    stars          INTEGER,
    forks          INTEGER,
    language       TEXT,
    topics         TEXT,                        -- JSON array 字串
    query          TEXT    NOT NULL,            -- 查詢條件（保留可重現性）
    created_at     TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- 同一週、同一查詢、同一 repo 不重複
CREATE UNIQUE INDEX IF NOT EXISTS idx_weekly_unique
    ON weekly_rankings (week, query, repo_full_name);

-- 依週與名次查詢的常用索引
CREATE INDEX IF NOT EXISTS idx_weekly_week_rank
    ON weekly_rankings (week, rank);
