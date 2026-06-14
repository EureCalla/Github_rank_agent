# Github_rank_agent — Claude 專屬說明

> 通用協作規範、資料模型與擴充方式請以 `AGENTS.md` 為準。本檔只放進場摘要。

## 你進到這個 repo 要做什麼

任務：**每週抓 GitHub 排行 → 存進 `database/research_github.db` → 供個人研究評等**。

進場預設動作：`python main.py fetch`（抓本週排行）。

## 觸發詞：本周好料 / 本周乾貨

使用者以「本周好料 / 本週好料 / 本周乾貨 / 本週乾貨 / 本周好貨 / 好料 / 乾貨」等開場時，
依 `skills/weekly-digest/SKILL.md` 執行：讀本週資料 → 產出**分類好料總結** → 結尾問使用者
對哪些 repo 有興趣 → `python main.py interested <owner/name>` 寫入想研究標記。

## 觸發：直接丟 GitHub 連結

使用者沒問乾貨、而是直接貼一個 GitHub repo 連結時，依 `skills/add-repo/SKILL.md` 執行：
先問是否加入資料庫 → 是則讀該 repo、繁中簡短說明、`python main.py add-repo <url> --desc "<英文>"`
→ 確認後問是否標記「想進行深度研究」。

## 三張表（以 repo_full_name 串接）

- `research_github`：週排行快照（抓取資料，勿手改）
- `repo_evaluation`：個人評價（rating 1-10 / notes）
- `repo_research`：深度研究狀態（interested → researching → done）

**抓取只動 `research_github`，不碰個人表。**

## 常用 CLI

```bash
python main.py digest          # 看本週排行（含評價/研究狀態）
python main.py interested <owner/name> ...
python main.py rate <owner/name> <1-10> [--notes "心得"]
python main.py researched <owner/name>
python main.py to-research     # 列出想研究的 repo（給「深度研究」用）
```

細節一律見 `AGENTS.md`。
