---
name: add-repo
description: 使用者沒有問乾貨/好料、而是直接丟一個 GitHub repo 連結時觸發；先問是否加入資料庫，若是則讀該 repo 用繁中簡短說明用途並寫入，確認後再問是否標記「想進行深度研究」。
---

# 加入 repo（直接丟 GitHub 連結）

## 觸發

使用者在 `Github_rank_agent` repo 工作時，**沒有問乾貨/好料**，而是直接貼一個 GitHub repo 連結
（如 `https://github.com/owner/name`）。

工作目錄為 repo 根目錄（home：`D:/github/Github_rank_agent`）。

## 流程

### 1. 先問是否加入
回應使用者：「要把這個 repo 放進資料庫嗎？」**停下來等回覆**。
- 若使用者說不要 → 不寫 DB，正常回應即可，結束。

### 2. 讀 repo 並簡短說明
使用者說要之後：
1. 用 **WebFetch 讀該連結**（About / README），理解它在做什麼。
2. 用**繁體中文簡短**告訴使用者這個 repo 在幹嘛（1~2 句）。
3. 用**簡潔乾淨英文**寫描述，寫入資料庫：
   ```bash
   python main.py add-repo <url> --desc "<乾淨英文描述>"
   ```
   - source 預設 `manual`，week 為本 ISO 週，以 `owner/name` 為 key 寫入 `research_github`。

### 3. 確認後問是否標記深度研究
使用者表示對說明沒問題後，再問：「要對這個 repo 標記『想進行深度研究』嗎？」
- 若要：
  ```bash
  python main.py interested <owner/name>
  ```
  寫入 `repo_research`，status=interested。

## 規則
- **回答一律繁體中文**；DB 的 `description` 存乾淨英文。
- 每一步都先問、得到使用者同意再動作，不要一次做完。
- 之後「深度研究」指令會用 `python main.py to-research` 取出被標記的 repo。
