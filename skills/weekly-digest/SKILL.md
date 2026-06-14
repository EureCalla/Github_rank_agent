---
name: weekly-digest
description: 使用者在本 repo 以「本周好料 / 本週好料 / 本周乾貨 / 本週乾貨 / 本周好貨 / 好料 / 乾貨」等開場時觸發；自動整理本週 GitHub 排行成分類好料總結，並在結尾詢問使用者對哪些 repo 有興趣、寫入想研究標記。
---

# 本周好料 / 本周乾貨

當使用者（在 `Github_rank_agent` repo 工作時）以下列任一語意開場，執行本流程：

- 觸發詞：`本周好料`、`本週好料`、`本周乾貨`、`本週乾貨`、`本周好貨`、`好料`、`乾貨`，或語意相近的「整理本週 GitHub 排行」開場。

工作目錄為 repo 根目錄（home：`D:/github/Github_rank_agent`）。

## 重要規則

- **回答一律用繁體中文**：DB 的 `description` 統一存乾淨英文，但你對使用者輸出的好料總結與所有對話，永遠用繁體中文導讀。
- **description 清理**：抓取時程式已自動清掉 emoji／奇怪符號並收斂空白。產出總結前，若發現某筆描述**非英文或仍雜亂**，先用 `python main.py set-desc <owner/name> "<乾淨英文描述>"` 修正（用簡潔英文重寫），再進行總結。

## 流程

### 1. 確認資料新鮮度
```bash
python main.py fetch --if-needed
python main.py digest
```
- `fetch --if-needed`：**若本週（ISO 週）已有非手動來源（`source != 'manual'`）的排行資料就略過抓取**，直接沿用現有 DB；只有本週還沒抓過時才真的去抓。
- 換句話說：同一週第二次以後問乾貨，不會重抓，直接用 DB 現有內容呈現；手動加入的 repo（source=manual）不會被誤判成「已抓過本週排行」。

### 2. 讀取本週資料
`python main.py digest` 會列出本週每個 repo：名次、`owner/name`、總星標、上週成長、連結、描述，以及既有標記（`⭐想研究` / `✅已研究` / `評N`）。

### 2.5 補齊缺漏的描述（description 為 NULL）
有些 repo 抓下來沒有描述。產出總結前先補齊：

```bash
python main.py missing-desc
```
對列出的每個 repo：
1. 用 **WebFetch 讀 `repo_url`**（GitHub 頁面的 About / README / 簡介），理解它在做什麼。
2. 用**簡潔乾淨的英文**寫一句描述，寫回 DB：
   ```bash
   python main.py set-desc <owner/name> "<乾淨英文描述>"
   ```
3. 全部補完後再進入下一步。

（這樣 DB 的 `description` 永遠是乾淨英文；給使用者看的總結則一律繁體中文。）

### 3. 產出總結：分「新進榜」與「追蹤區」兩塊

只講**本周新貨**，並把你已標記的 repo 獨立成追蹤區。依 `digest` 每筆的 `[NEW]/[SEEN]` 與 `status=` 分桶：

| 桶 | 條件（讀 digest 輸出） | 處理 |
|----|------------------------|------|
| 🆕 **本周新進榜** | `[NEW]` 且 `status=-` | 依主題分類、生動導讀（主秀） |
| 📌 **追蹤區（本周仍在榜）** | `status=` 為 `interested`/`researching`/`done` | 一行列出，帶狀態與名次 |
| （略過） | `[SEEN]` 且 `status=-`（看過、沒標記的舊榜） | 不講（只講新貨） |

格式範例：

```
🎉 本周 GitHub 好貨總結

這週新上榜的好料：

🚀 Top 熱門
- <短名> — <生動描述 + 個人感受詞>（<星標>⭐，本週 +<週增>）

🤖 AI / Agent 生態
- ...

🛠️ 實用工具
- ...

📌 你追蹤中 / 已研究（本周仍在榜）
- <短名> ⭐想研究（#名次）
- <短名> ✅已研究完畢（#名次）
```

**語氣**：生動活潑、讓人讀了會有點雀躍，像朋友在分享好東西；但**別過度浮誇**（避免「神級」「宇宙最強」這類）。適度用「超讚 / 很實用 / 有點猛 / 省爆」這種感受詞即可。

**格式規則**：
- 新進榜**每個分類標題前都加一個 emoji**（例：🚀 Top 熱門、🤖 AI·Agent 生態、🛠️ 實用工具、🧱 開發框架、📈 金融交易、🕷️ 資料/爬蟲、🎨 視覺/前端…），分類依當週內容彈性調整。
- 每筆用**短名**（去掉 owner，owner 可放括號），一句話講清楚它做什麼 + 為何值得看；星標/週增輕點即可。
- 爆量成長（高 `weekly_growth`）特別點出（例：「黑馬」「本週 +51k 爆量」）。
- 追蹤區用 `⭐想研究` / `🔬研究中` / `✅已研究完畢` 標狀態並附名次；追蹤區若本周沒有任何在榜者就省略整塊。
- 不要逐欄貼原始資料，要像導讀。

**改寫示範**（原始資料 → 好料總結寫法）：
- 原始：`Lum1104/Understand-Anything：53.5k stars，週增 7,701。把 code 轉互動知識圖，支援 Claude Code / Codex / Cursor 等。`
- 改寫：`Understand-Anything — 把任何程式碼轉成互動式流程圖／知識圖譜，視覺化超讚！支援 Claude Code / Codex / Cursor（53.5k⭐，本週 +7.7k）`

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
