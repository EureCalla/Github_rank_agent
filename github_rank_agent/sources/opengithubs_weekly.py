"""篩選方式：OpenGithubs/github-weekly-rank。

抓取 https://github.com/OpenGithubs/github-weekly-rank 的 README（每週一 8AM 更新），
解析其中每個 repo 的詳細區塊。詳細區塊格式範例（fullwidth 冒號 ：）：

    <h3 ...>1.  https://github.com/owner/name</h3>

    - ⭐ 总星标数量：58.2k
    - 🔺 上周增长数量：51427⭐
    - 🔺 上月增长数量：51427⭐
    - 📅 开源时间：2026-06-01
    - 📝 项目描述：...
"""
from __future__ import annotations

import re
from datetime import date

import requests

from ..models import RepoRecord
from .base import Source

# raw README（default branch 為 main，少數情況退回 master）
_RAW_URLS = (
    "https://raw.githubusercontent.com/OpenGithubs/github-weekly-rank/main/README.md",
    "https://raw.githubusercontent.com/OpenGithubs/github-weekly-rank/master/README.md",
)

# 每個 repo 區塊的標頭：抓「名次. https://github.com/owner/name」
_HEADER_RE = re.compile(
    r"<h3[^>]*>.*?(\d+)\.\s*(https://github\.com/[^\s<]+).*?</h3>",
    re.S,
)


def parse_star_count(text: str | None) -> int | None:
    """把 "58.2k" / "1.2M" / "523" 轉成整數。"""
    if not text:
        return None
    cleaned = text.strip().rstrip("⭐").strip()
    m = re.match(r"([\d.]+)\s*([kKmM]?)", cleaned)
    if not m:
        return None
    num = float(m.group(1))
    mult = {"": 1, "k": 1_000, "m": 1_000_000}[m.group(2).lower()]
    return int(num * mult)


def current_week(today: date | None = None) -> str:
    """以抓取日的 ISO 週別表示，例：2026-W24。"""
    y, w, _ = (today or date.today()).isocalendar()
    return f"{y}-W{w:02d}"


def _field(block: str, pattern: str) -> str | None:
    m = re.search(pattern, block)
    if not m:
        return None
    value = m.group(1).strip()
    return value or None


def _int_field(block: str, pattern: str) -> int | None:
    value = _field(block, pattern)
    return int(value) if value is not None else None


class OpenGithubsWeeklySource(Source):
    name = "OpenGithubs/github-weekly-rank"

    def __init__(self, timeout: int = 20) -> None:
        self.timeout = timeout

    def _download_readme(self) -> str:
        last_error: Exception | None = None
        for url in _RAW_URLS:
            try:
                resp = requests.get(url, timeout=self.timeout)
                if resp.status_code == 404:
                    continue
                resp.raise_for_status()
                resp.encoding = "utf-8"
                return resp.text
            except requests.RequestException as exc:  # noqa: PERF203
                last_error = exc
        raise RuntimeError(f"無法下載 OpenGithubs README：{last_error}")

    def parse(self, text: str, week: str | None = None) -> list[RepoRecord]:
        """解析 README 內容為 RepoRecord 清單（與下載分離，方便測試/重跑）。"""
        week = week or current_week()
        headers = list(_HEADER_RE.finditer(text))
        records: list[RepoRecord] = []
        for i, h in enumerate(headers):
            rank = int(h.group(1))
            url = h.group(2).rstrip("/")
            full_name = url.split("github.com/", 1)[1]
            start = h.end()
            end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
            block = text[start:end]
            records.append(
                RepoRecord(
                    source=self.name,
                    repo_full_name=full_name,
                    repo_url=url,
                    rank=rank,
                    week=week,
                    total_stars=parse_star_count(_field(block, r"总星标数量：([\d.]+\s*[kKmM]?)")),
                    weekly_growth=_int_field(block, r"上周增长数量：(\d+)"),
                    monthly_growth=_int_field(block, r"上月增长数量：(\d+)"),
                    created_date=_field(block, r"开源时间：(\d{4}-\d{2}-\d{2})"),
                    description=_field(block, r"项目描述：(.*)"),
                )
            )
        return records

    def fetch(self) -> list[RepoRecord]:
        return self.parse(self._download_readme())
