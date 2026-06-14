# Github_rank_agent — Claude 專屬說明

> 通用協作規範、資料規則與擴充方式請以 `AGENTS.md` 為準。本檔只放進場摘要。

## 你進到這個 repo 要做什麼

本 repo 的任務是：**每週抓 GitHub 排行 → 存進 `database/research_github.db` → 供個人研究評等**。

進場第一動作（除非使用者另有指示）：

```powershell
python main.py
```

它會初始化 `research_github.db`，並對已啟用的「篩選方式」抓本週排行寫入。第一個來源是 **OpenGithubs/github-weekly-rank**。

## 三個重點

1. **個人欄位不可覆蓋**：`personal_rating` / `deep_research` / `personal_notes` 由使用者填，重抓不動它們。
2. **`research_github.db` 納入 git**；其他 `*.db` / token / `output/` 不進 git。
3. **新增篩選方式**：在 `github_rank_agent/sources/` 加一個 `Source` 子類並於 `__init__.py` 的 `ENABLED_SOURCES` 註冊。

細節一律見 `AGENTS.md`。
