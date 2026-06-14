# Github_rank_agent

`Github_rank_agent` 是用來每週整理 GitHub repository 排名，並協助後續研究分析的 side-project。

目前此 repo 處於初始化階段。本次只建立基本文件與專案規範，尚未加入程式碼入口、資料模型或排程流程。

## 目標

- 定期整理 GitHub repo 排名與趨勢變化。
- 保留每週查詢結果，方便後續比較與研究。
- 將整理結果輸出成可閱讀的摘要或報告。
- 作為研究熱門專案、技術主題與工具趨勢的輔助工具。

## 安裝

先建立 Python 3.11 環境，之後依需求安裝套件：

```powershell
python -m pip install -r requirements.txt
```

目前 `requirements.txt` 尚未加入 runtime dependency；等實作資料抓取或報告產生流程時再補上。

## 預期專案結構

```text
Github_rank_agent/
├─ README.md             # 專案說明
├─ AGENTS.md             # AI / 維護者協作規範
├─ DESIGN.md             # UI / 報告視覺風格紀錄
├─ LICENSE               # 授權條款
├─ requirements.txt      # Python 套件清單
├─ .gitignore            # Git 忽略規則
└─ database/             # 未來放 SQLite 或本機資料快取
```

後續若開始實作，建議再依功能建立清楚的模組分層，例如：

- GitHub 查詢與 API client
- 排名資料儲存與讀取
- 每週摘要產生
- 報告輸出或通知流程

## 維護原則

- 先定義資料格式，再實作抓取流程。
- 不把 API token、私人設定或本機資料庫 commit 進 git。
- 新增套件時同步更新 `requirements.txt`。
- 若建立 SQLite schema，需保留 migration 或初始化腳本。
- 產出報告與快取資料預設視為本機輸出，不直接進 git。
