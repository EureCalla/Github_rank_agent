---
name: weekly-digest
description: 使用者在本 repo 以「本周好料 / 本週好料 / 本周乾貨 / 本週乾貨 / 本周好貨 / 好料 / 乾貨」等開場時觸發；自動整理本週 GitHub 排行成分類好料總結，並在結尾詢問使用者對哪些 repo 有興趣、寫入想研究標記。
---

# 本周好料 / 本周乾貨

當使用者（在 `Github_rank_agent` repo 工作時）以下列任一語意開場，執行本流程：

- 觸發詞：`本周好料`、`本週好料`、`本周乾貨`、`本週乾貨`、`本周好貨`、`好料`、`乾貨`，或語意相近的「整理本週 GitHub 排行」開場。

工作目錄為 repo 根目錄（home：`D:/github/Github_rank_agent`）。

## 流程

### 1. 確認資料新鮮度
```bash
python main.py digest
```
- 若輸出「沒有資料」或 `週別` 不是本 ISO 週 → 先抓最新：
  ```bash
  python main.py fetch
  python main.py digest
  ```

### 2. 讀取本週資料
`python main.py digest` 會列出本週每個 repo：名次、`owner/name`、總星標、上週成長、連結、描述，以及既有標記（`⭐想研究` / `✅已研究` / `評N`）。

### 3. 產出分類好料總結
依各 repo 的描述與成長，**由你（agent）歸類**並寫成易讀總結，格式對齊使用者習慣：

```
🎉 本周 GitHub 好貨總結

🚀 Top 熱門
- <Repo> (<owner>) — <一句重點，含星標/成長亮點>

💡 AI / Agent 生態
- ...

🎨 實用工具
- ...

📊 金融 / 交易
- ...
```

規則：
- 分類標題依當週內容彈性調整（常見：Top 熱門、AI/Agent 生態、實用工具、開發框架、金融交易、資料/爬蟲…）。
- 每筆一句話講清楚它做什麼 + 為何值得看；爆量成長（高 `weekly_growth`）特別點出。
- 已標記的 repo 帶上記號：`✅ 已研究完畢`、`⭐ 想研究`、評等分數。
- 不要逐欄貼原始資料，要像導讀。

### 4. 結尾提問並記錄興趣
總結結尾**主動詢問**：「對哪些 repo 有興趣、想進一步研究？」

使用者回覆後，對每個被選中的 repo 執行（repo 用 `owner/name`）：
```bash
python main.py interested <owner/name> [<owner/name> ...]
```
寫入 `repo_research`（status=interested）。

## 後續（非本 skill）
- 使用者說「深度研究」時，由深度研究 skill 以 `python main.py to-research` 取出 status=interested 的 repo 逐一研究，完成後 `python main.py researched <owner/name>`。
- 個人評價：`python main.py rate <owner/name> <1-10> [--notes "心得"]`。

## 資料表（三表以 repo_full_name 串接）
- `research_github`：週排行快照（抓取資料，勿手改）
- `repo_evaluation`：個人評價（rating/notes）
- `repo_research`：深度研究狀態（interested → researching → done）
