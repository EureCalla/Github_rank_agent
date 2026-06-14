-- Github_rank_agent SQLite schema
-- 先定義資料格式，再實作抓取流程（見 AGENTS.md）。
-- 注意：research_github.db 是本 repo 的研究資產，會「納入 git」追蹤；
--       其他 *.db / 快取 / 報告輸出仍不進 git（見 .gitignore）。

-- 每週 GitHub 排行研究資料：一列代表「某來源、某週、某個 repo」的紀錄
CREATE TABLE IF NOT EXISTS research_github (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    -- 來源 / 篩選方式
    source          TEXT    NOT NULL,            -- 例：OpenGithubs/github-weekly-rank
    week            TEXT,                          -- 排行週別 YYYY-Www
    rank            INTEGER,                       -- 該來源當週名次（1 起算）
    -- 來源抓下來的 repo 資訊
    repo_full_name  TEXT    NOT NULL,            -- owner/name
    repo_url        TEXT    NOT NULL,            -- repo 連結
    total_stars     INTEGER,                       -- 總星標數（58.2k -> 58200 正規化）
    weekly_growth   INTEGER,                       -- 上週成長數
    monthly_growth  INTEGER,                       -- 上月成長數
    created_date    TEXT,                          -- 開源時間 YYYY-MM-DD
    description     TEXT,                          -- 項目描述
    language        TEXT,                          -- 語言（此來源無，預設 NULL，未來 API 補）
    -- 個人 / meta 欄位
    fetched_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime')),  -- 下載時間
    personal_rating INTEGER,                       -- 個人評等 1~10，預設 NULL 由人填
    deep_research   INTEGER NOT NULL DEFAULT 0,    -- 深度研究 flag 0/1
    personal_notes  TEXT                           -- 個人心得
);

-- 同一來源、同一週、同一 repo 不重複（UPSERT 的衝突鍵）
CREATE UNIQUE INDEX IF NOT EXISTS idx_research_unique
    ON research_github (source, week, repo_full_name);

-- 依週與名次查詢的常用索引
CREATE INDEX IF NOT EXISTS idx_research_week_rank
    ON research_github (week, rank);
