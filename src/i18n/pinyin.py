"""拼音搜索支持：让中文文本可以用拼音全拼/首字母匹配。

数据来源 resources/game_data/pinyin_table.json（离线生成的
「汉字 → 常见读音列表」映射，仅覆盖 zh_CN.json 中出现过的汉字，
约 2200 字 / 36KB），运行时零第三方依赖。

用法::

    from i18n.pinyin import py_match
    py_match('fzr', '风之刃')      # True（首字母）
    py_match('fengzhiren', '风之刃')  # True（全拼）
    py_match('风之', '风之刃')     # True（普通子串，行为向后兼容）
"""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

from palsav import json_tools

_TABLE: Optional[Dict[str, List[str]]] = None


def _load_table() -> Dict[str, List[str]]:
    global _TABLE
    if _TABLE is None:
        try:
            from i18n import _get_resources_dir
            path = os.path.join(_get_resources_dir(), 'game_data', 'pinyin_table.json')
            _TABLE = json_tools.load(path) if os.path.exists(path) else {}
        except Exception:
            _TABLE = {}
    return _TABLE


def _is_cjk(ch: str) -> bool:
    return '\u4e00' <= ch <= '\u9fff'


@lru_cache(maxsize=8192)
def _pinyin_forms(text: str) -> Optional[Tuple[str, str]]:
    """返回 (全拼串, 首字母串)；无汉字时返回 None（走普通子串即可）。

    非汉字字符仅保留 ASCII 字母数字（小写），符号/空格丢弃，
    这样 'plq' 能匹配 '⬢ 帕鲁球' 而不被前缀符号干扰。
    """
    table = _load_table()
    full_parts: List[str] = []
    init_parts: List[str] = []
    has_cjk = False
    for ch in text:
        readings = table.get(ch)
        if readings:
            has_cjk = True
            r = readings[0]
            full_parts.append(r)
            init_parts.append(r[0] if r else '')
        elif _is_cjk(ch):
            # 表外汉字：占位为空，不参与匹配
            has_cjk = True
        else:
            c = ch.lower()
            if c.isascii() and c.isalnum():
                full_parts.append(c)
                init_parts.append(c)
    if not has_cjk:
        return None
    return (''.join(full_parts), ''.join(init_parts))


def py_match(query: str, text: str) -> bool:
    """大小写不敏感的搜索匹配。

    1. 普通子串命中 → True（完全向后兼容原有行为）；
    2. query 为纯 ASCII 且 text 含汉字时，额外尝试拼音全拼、
       拼音首字母子串匹配。
    """
    q = (query or '').strip().lower()
    if not q:
        return True
    tl = (text or '').lower()
    if q in tl:
        return True
    if not q.isascii():
        return False
    forms = _pinyin_forms(text or '')
    if forms is None:
        return False
    q2 = ''.join(c for c in q if c.isalnum())
    if not q2:
        return False
    full, inits = forms
    return q2 in full or q2 in inits
