"""共用資料模型。

``RepoRecord`` 是各「篩選方式（來源）」抓取後回傳的標準格式，
對應 database/schema.sql 的 research_github 表（不含個人欄位）。
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RepoRecord:
    """單一 repo 的抓取結果。

    個人欄位（personal_rating / deep_research / personal_notes）不在此，
    由使用者於 DB 內自行維護，重抓時不覆蓋。
    """

    source: str                       # 篩選方式 / 來源，例：OpenGithubs/github-weekly-rank
    repo_full_name: str               # owner/name
    repo_url: str                     # repo 連結
    rank: int | None = None           # 該來源當週名次
    week: str | None = None           # 排行週別 YYYY-Www
    total_stars: int | None = None    # 總星標數
    weekly_growth: int | None = None  # 上週成長數
    monthly_growth: int | None = None # 上月成長數
    created_date: str | None = None   # 開源時間 YYYY-MM-DD
    description: str | None = None    # 項目描述
    language: str | None = None       # 語言（部分來源沒有）
