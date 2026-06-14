"""Github_rank_agent 套件。

每週整理 GitHub repository 排名與趨勢變化，存入 research_github.db 供研究評等。

模組分層：
- config:    設定（DB 路徑、token 環境變數）
- models:    RepoRecord 標準資料格式
- sources/:  篩選方式（來源）抓取器，第一個為 OpenGithubs/github-weekly-rank
- storage:   research_github.db 的初始化、UPSERT（保留個人欄位）與查詢
- summary / report:  週報摘要與輸出（後續階段）
- github_client:     GitHub API enrichment（選填，未來用）
"""

__version__ = "v2.0"
