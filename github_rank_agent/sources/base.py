"""來源（篩選方式）抽象基底。

每個「篩選方式」是一個 Source 子類，負責從某個地方抓本週排行，
回傳一批標準化的 RepoRecord。新增來源 = 新增一個子類並在 __init__.py 註冊。
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import RepoRecord


class Source(ABC):
    """單一篩選方式的抓取器。"""

    #: 篩選方式名稱，會寫入 research_github.source 欄位
    name: str = "unknown"

    @abstractmethod
    def fetch(self) -> list[RepoRecord]:
        """抓取本週排行並回傳標準化結果。"""
        raise NotImplementedError
