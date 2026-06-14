# Github_rank_agent Agent Rules

本檔案是 `Github_rank_agent` repo 內的 AI / 維護者協作規範。除非使用者明確要求，不要修改本檔案。

## 專案定位

`Github_rank_agent` 是 side-project：**每週抓 GitHub 排行 → 存進 `research_github.db` → 供個人研究與評等**。

## Agent 任務與進場流程

Agent 進到本 repo 的預設任務是「抓本週排行並寫入研究資料庫」：

```powershell
python main.py fetch      # 等同 python main.py（無子指令時預設 fetch）
```

`fetch` 會：
1. 初始化/確認 `database/research_github.db`（依 `database/schema.sql`）。
2. 對 `github_rank_agent/sources/` 中已啟用的「篩選方式」逐一抓本週排行（第一個：**OpenGithubs/github-weekly-rank**，每週一 8AM 更新）。
3. 把每筆 repo `UPSERT` 進 `research_github`，記錄 `source`、`rank`、來源資訊與 `fetched_at`。

## 「本周好料 / 本周乾貨」skill

使用者以「本周好料 / 本週好料 / 本周乾貨 / 本週乾貨 / 本周好貨 / 好料 / 乾貨」等開場時，依
`skills/weekly-digest/SKILL.md` 執行：讀本週資料 → 產出分類好料總結 → 結尾問使用者對哪些 repo 有興趣 →
以 `python main.py interested <owner/name>` 寫入想研究標記。

## 資料模型（三張表，以 `repo_full_name` 串接）

| 表 | 用途 | 維護者 |
|----|------|--------|
| `research_github` | 週排行快照（來源/名次/星標/成長/開源時間/描述…） | 抓取流程（勿手改） |
| `repo_evaluation` | 個人評價：`personal_rating`(1-10) / `personal_notes` | 使用者 |
| `repo_research` | 深度研究：`status`（interested→researching→done）+ 時間戳 | 使用者 / 研究 skill |

- 串接 key：三表共用 `repo_full_name`（owner/name）；查詢用 `LEFT JOIN`。
- **抓取流程只動 `research_github`，絕不碰 `repo_evaluation` / `repo_research`**，個人資料不會被重抓覆蓋。

## CLI（給 skill / 手動使用）

```bash
python main.py fetch                          # 抓本週排行
python main.py digest [--week YYYY-Www]       # 印某週排行（含評價/研究狀態）
python main.py interested <owner/name> ...     # 標記想進一步研究
python main.py rate <owner/name> <1-10> [--notes "心得"]
python main.py researched <owner/name>         # 標記已研究完畢
python main.py to-research                      # 列出 status=interested（供「深度研究」）
```

## 擴充新的篩選方式

1. 在 `github_rank_agent/sources/` 新增 `base.Source` 子類，設定 `name`（寫入 `source`）並實作 `fetch() -> list[RepoRecord]`。
2. 於 `github_rank_agent/sources/__init__.py` 的 `ENABLED_SOURCES` 註冊。

## 資料規範

- **`database/research_github.db` 納入 git 追蹤**（本 repo 研究資產）；其他 `*.db`/快取/`output/`/API token 不得 commit（見 `.gitignore`）。
- ⚠️ binary SQLite 進 git 後，跨機器各自寫入無法自動合併（同 Calla_Agent 的 `memory.db`）。單機使用無虞；未來雙機同步建議改「文字匯出（CSV/JSONL）+ rebuild」。

## 開發原則

- Python 3.11；`pip + requirements.txt`，不使用 Poetry / Conda 專案設定檔；新增套件同步更新 `requirements.txt`。
- GitHub API token 走環境變數 `GITHUB_TOKEN`，不得寫入 repo（目前主流程不需 token）。
- 修改 repo 前先確認 git 狀態與 branch；未經要求不新增背景排程、不重構既有結構。
- `.gitignore` 與 `LICENSE` 只有使用者明確要求才改。

## 專案結構

```text
Github_rank_agent/
├─ main.py                       # CLI 入口（fetch / digest / interested / rate / researched / to-research）
├─ introduce.py                  # 版本資訊
├─ requirements.txt
├─ skills/
│  └─ weekly-digest/SKILL.md     # 「本周好料」總結流程
├─ database/
│  ├─ schema.sql                 # 三張表定義
│  └─ research_github.db         # 研究資料庫（納入 git）
└─ github_rank_agent/            # 套件
   ├─ config.py                  # DB 路徑、token 環境變數
   ├─ models.py                  # RepoRecord 標準格式
   ├─ storage.py                 # init_db / upsert / 評價 / 研究狀態 / digest 查詢
   ├─ sources/                   # 篩選方式（base + opengithubs_weekly）
   ├─ summary.py / report.py     # 週報摘要與輸出（後續階段）
   └─ github_client.py           # GitHub API enrichment（選填，未來）
```
