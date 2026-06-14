# Github_rank_agent Agent Rules

本檔案是 `Github_rank_agent` repo 內的 AI / 維護者協作規範。除非使用者明確要求，不要修改本檔案。

## 專案定位

`Github_rank_agent` 是 side-project：**每週抓 GitHub 排行 → 存進 `research_github.db` → 供個人研究與評等**。

## Agent 任務與進場流程

Agent 進到本 repo 時，預設任務是「抓本週排行並寫入研究資料庫」。執行：

```powershell
python main.py
```

`main.py` 會依序：

1. **初始化 / 確認** `database/research_github.db`（依 `database/schema.sql`，`storage.init_db()`）。
2. 對 `github_rank_agent/sources/` 中**已啟用的「篩選方式（來源）」**逐一抓本週排行。
   - 第一個來源：**OpenGithubs/github-weekly-rank**（`github-weekly-rank` README，每週一 8AM 更新）。
3. 將每筆 repo `UPSERT` 進 `research_github`，記錄 `source`（篩選方式）、`rank`、來源資訊與 `fetched_at`（下載時間）。

**個人欄位保護**：`personal_rating`（個人評等 1~10）、`deep_research`（深度研究 0/1）、`personal_notes`（個人心得）由使用者自行維護，**重抓時一律不覆蓋**（`storage.upsert_records` 已內建）。

## 擴充新的篩選方式

1. 在 `github_rank_agent/sources/` 新增一個 `base.Source` 子類，設定 `name`（會寫入 `source` 欄位）並實作 `fetch() -> list[RepoRecord]`。
2. 在 `github_rank_agent/sources/__init__.py` 的 `ENABLED_SOURCES` 註冊。

## 資料規範

- **`database/research_github.db` 納入 git 追蹤**：它是本 repo 的研究資產（含個人評等與心得），要跟著 GitHub 走。
- 其他 `*.db` / 快取 / 報告輸出 (`output/`) / API token **不得 commit**（見 `.gitignore`）。
- ⚠️ 已知風險：binary SQLite 進 git 後，跨機器各自寫入會無法自動合併（同類問題見 Calla_Agent 的 `memory.db`）。目前單機使用無虞；若未來要雙機同步，改用「文字匯出（CSV/JSONL）+ rebuild」模式。

## 開發原則

- 使用 Python 3.11；套件管理用 `pip + requirements.txt`，不使用 Poetry / Conda。
- 新增套件時必須同步更新 `requirements.txt`。
- GitHub API token 透過環境變數 `GITHUB_TOKEN` 載入，不得寫入 repo（目前主流程不需 token）。
- 修改 repo 前先確認 git 狀態與目前 branch。
- 未經使用者要求，不新增背景排程、不重構既有檔案結構。
- `.gitignore` 與 `LICENSE` 只有在使用者明確要求時才修改。

## 專案結構

```text
Github_rank_agent/
├─ main.py                       # 入口：抓排行 -> 寫 DB
├─ introduce.py                  # 版本資訊（self.version）
├─ requirements.txt
├─ database/
│  ├─ schema.sql                 # research_github 資料表定義
│  └─ research_github.db         # 研究資料庫（納入 git）
└─ github_rank_agent/            # 套件
   ├─ config.py                  # DB 路徑、token 環境變數
   ├─ models.py                  # RepoRecord 標準格式
   ├─ storage.py                 # init_db / upsert_records / load
   ├─ sources/                   # 篩選方式（來源）
   │  ├─ base.py                 # Source 抽象基底
   │  └─ opengithubs_weekly.py   # OpenGithubs/github-weekly-rank
   ├─ summary.py / report.py     # 週報摘要與輸出（後續階段）
   └─ github_client.py           # GitHub API enrichment（選填，未來）
```
