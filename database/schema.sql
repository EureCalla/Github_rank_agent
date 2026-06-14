-- Github_rank_agent SQLite schema
-- 三張表，以 repo_full_name（owner/name）互相串接：
--   research_github  週排行快照（純抓取資料）
--   repo_evaluation  個人評價 sheet
--   repo_research    深度研究 sheet
-- 注意：research_github.db 納入 git；抓取流程只動 research_github，絕不碰個人表。

-- 表 1：每週 GitHub 排行研究資料（某來源、某週、某 repo）
CREATE TABLE IF NOT EXISTS research_github (
    id              INTEGER PRIMARY KEY,
    source          TEXT    NOT NULL,            -- 篩選方式，例：OpenGithubs/github-weekly-rank
    week            TEXT,                          -- 排行週別 YYYY-Www
    rank            INTEGER,                       -- 該來源當週名次（1 起算）
    repo_full_name  TEXT    NOT NULL,            -- owner/name（串接 key）
    repo_url        TEXT    NOT NULL,            -- repo 連結
    total_stars     INTEGER,                       -- 總星標數（58.2k -> 58200 正規化）
    weekly_growth   INTEGER,                       -- 上週成長數
    monthly_growth  INTEGER,                       -- 上月成長數
    created_date    TEXT,                          -- 開源時間 YYYY-MM-DD
    description     TEXT,                          -- 項目描述
    language        TEXT,                          -- 語言（此來源無，預設 NULL）
    fetched_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime'))  -- 下載時間
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_research_unique
    ON research_github (source, week, repo_full_name);
CREATE INDEX IF NOT EXISTS idx_research_week_rank
    ON research_github (week, rank);

-- 表 2：個人評價（一個 repo 一筆，跨週共用）
CREATE TABLE IF NOT EXISTS repo_evaluation (
    repo_full_name  TEXT    PRIMARY KEY,         -- 串接 key
    personal_rating INTEGER,                       -- 個人評等 1~10
    personal_notes  TEXT,                          -- 個人心得
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
);

-- 表 3：深度研究（一個 repo 一筆）
CREATE TABLE IF NOT EXISTS repo_research (
    repo_full_name  TEXT    PRIMARY KEY,         -- 串接 key
    status          TEXT    NOT NULL DEFAULT 'interested'
                    CHECK (status IN ('interested','researching','done')),
    interested_at   TEXT,                          -- 標記想研究的時間
    researched_at   TEXT,                          -- 研究完畢時間
    research_notes  TEXT                           -- 研究產出/筆記（未來 skill 填）
);
