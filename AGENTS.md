# Github_rank_agent Agent Rules

本檔案是 `Github_rank_agent` repo 內的 AI / 維護者協作規範。除非使用者明確要求，不要修改本檔案。

## 專案定位

`Github_rank_agent` 是 side-project，用於每週整理 GitHub repository 排名與研究分析資料。

目前狀態：初始化文件階段，尚未建立程式碼入口或資料抓取流程。

## 開發原則

- 使用 Python 3.11。
- 套件管理使用 `pip + requirements.txt`。
- 不使用 Poetry 或 Conda 專案設定檔。
- 本機資料、API token、SQLite DB、報告輸出不得 commit。
- 新增套件時必須同步更新 `requirements.txt`。
- 若建立 SQLite schema，需提供初始化或 migration 腳本。

## 修改規則

- 修改 repo 前先確認 git 狀態與目前 branch。
- 未經使用者要求，不新增程式碼入口或背景排程。
- 未經使用者要求，不重構已存在的檔案結構。
- 文件可依需求更新，但要維持資料研究工具的定位。
- `.gitignore` 與 `LICENSE` 只有在使用者明確要求時才修改。

## 預期 root 文件

- `README.md`：專案說明與使用方式
- `DESIGN.md`：報告 / UI 風格規範
- `requirements.txt`：Python 套件清單
- `.gitignore`：本機資料與輸出忽略規則
- `LICENSE`：授權條款
- `AGENTS.md`：本檔案

## 後續實作提醒

開始寫程式前，先決定資料來源與資料格式。GitHub API token 應透過環境變數或本機設定載入，不得寫入 repo。
