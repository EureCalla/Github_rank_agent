"""報告輸出。

將每週摘要輸出為可閱讀格式（Markdown / 文字摘要）。
報告輸出預設視為本機產物，不直接進 git（見 AGENTS.md / .gitignore 的 output/）。
"""
from __future__ import annotations

from .summary import WeeklySummary


def render_markdown(summary: WeeklySummary) -> str:
    """將摘要轉成 Markdown 週報字串。

    Note:
        尚未實作；輸出應包含產出日期、資料範圍、排名清單與變化重點（見 DESIGN.md）。
    """
    raise NotImplementedError("Markdown 報告輸出尚未實作")
