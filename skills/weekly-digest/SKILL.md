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
依各 repo 的描述與成長，**由你（agent）歸類**並寫成總結。格式範例：

```
🎉 本周 GitHub 好貨總結

這週也有不少好料，挑幾個亮點：

🚀 Top 熱門
- <短名> — <生動描述 + 個人感受詞>（<星標>⭐，本週 +<週增>）

🤖 AI / Agent 生態
- ...

🛠️ 實用工具
- ...

📈 金融 / 交易
- ...
```

**語氣**：生動活潑、讓人讀了會有點雀躍，像朋友在分享好東西；但**別過度浮誇**（避免「神級」「宇宙最強」這類）。適度用「超讚 / 很實用 / 有點猛 / 省爆」這種感受詞即可。

**格式規則**：
- **每個分類標題前都要加一個 emoji**，依主題挑（例：🚀 Top 熱門、🤖 AI·Agent 生態、🛠️ 實用工具、🧱 開發框架、📈 金融交易、🕷️ 資料/爬蟲、🎨 視覺/前端…）。分類依當週內容彈性調整。
- 每筆用**短名**（去掉 owner，owner 可放括號），一句話講清楚它做什麼 + 為何值得看；星標/週增當亮點輕點即可，不必每筆都塞滿數字。
- 爆量成長（高 `weekly_growth`）特別點出（例：「黑馬」「本週 +51k 爆量」）。
- 已標記的 repo 帶上記號：`✅ 已研究完畢`、`⭐ 想研究`、`評N`。
- 不要逐欄貼原始資料，要像導讀。

**改寫示範**（原始資料 → 好料總結寫法）：
- 原始：`Lum1104/Understand-Anything：53.5k stars，週增 7,701。把 code 轉互動知識圖，支援 Claude Code / Codex / Cursor 等。`
- 改寫：`🧠 Understand-Anything — 把任何程式碼轉成互動式流程圖／知識圖譜，視覺化超讚！支援 Claude Code / Codex / Cursor（53.5k⭐，本週 +7.7k）`

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
