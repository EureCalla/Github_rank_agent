"""Github_rank_agent 套件。

每週整理 GitHub repository 排名與趨勢變化，協助後續研究分析。

模組分層（見 README.md「預期專案結構」）：
- config:        設定載入（API token、路徑）
- github_client: GitHub 查詢與 API client
- storage:       排名資料儲存與讀取（SQLite）
- summary:       每週摘要產生
- report:        報告輸出
"""

__version__ = "v2.0"
