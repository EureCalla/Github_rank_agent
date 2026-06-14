"""文字清理工具。

來源的 description 常夾雜 emoji、奇怪符號、全形字與多餘空白。
clean_description 統一清成乾淨、可讀的單行文字後才寫入 DB。
（注意：此處只做「去符號 / 正規化 / 收斂空白」，不做語言翻譯；
 非英文描述若要統一成英文，由 weekly-digest skill 在抓取後以 set-desc 修正。）
"""
from __future__ import annotations

import re
import unicodedata

# 智慧引號 / 破折號 / 省略號 -> ASCII
_PUNCT_MAP = {
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "…": "...", " ": " ",
}

# emoji / 圖示 / 雜符號（不含一般文字與標點）
_SYMBOL_RE = re.compile(
    "["
    "\U0001F000-\U0001FAFF"   # emoji & pictographs（含 🔺 等）
    "\U00002600-\U000026FF"   # misc symbols
    "\U00002700-\U000027BF"   # dingbats
    "\U0001F1E6-\U0001F1FF"   # 區域旗幟
    "\U00002B00-\U00002BFF"   # misc symbols & arrows（含 ⭐ U+2B50）
    "\U0001F900-\U0001F9FF"   # supplemental symbols
    "\U0000FE00-\U0000FE0F"   # variation selectors
    "\U00002190-\U000021FF"   # arrows
    "‍"                   # ZWJ
    "]",
    flags=re.UNICODE,
)
_ZERO_WIDTH_RE = re.compile("[​‌‎‏﻿]")


def clean_description(text: str | None) -> str | None:
    """清成乾淨單行文字；空字串回 None。"""
    if not text:
        return None
    text = unicodedata.normalize("NFKC", text)
    for src, dst in _PUNCT_MAP.items():
        text = text.replace(src, dst)
    text = _SYMBOL_RE.sub("", text)
    text = _ZERO_WIDTH_RE.sub("", text)
    # 先把所有空白（含 \t \n）轉成空格，避免下一步刪控制字元時把字黏在一起
    text = re.sub(r"\s", " ", text)
    # 移除剩餘控制字元（category 以 C 開頭；此時已無空白類控制字元）
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")
    # 收斂多個空格
    text = re.sub(r" +", " ", text).strip()
    return text or None
