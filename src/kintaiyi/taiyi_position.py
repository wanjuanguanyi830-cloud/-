"""G2 太乙所在：24算小周、三算一宫、八宫循环。

《太乙金镜式经》卷一：
- 以太乙小周法二十四去之；
- 以三约之为宫数；
- 阳遁命起一宫，顺行八宫，不游中五；
- 阴遁命起九宫，逆行八宫，不游中五。

《太乙统宗宝鉴》卷一同法；个别电子OCR把“小周二十四”
误作“二百四十”，但“三算一宫 × 八宫 = 24”与《金镜》原文相互校正。
"""

from __future__ import annotations

from typing import Any

G2_RULE_ID = "J1-TAIYI-24"
SOURCE_PROFILE = "jinjing_tongzong_taiyi_24_cycle"

YANG_PALACE_ORDER = (1, 2, 3, 4, 6, 7, 8, 9)
YIN_PALACE_ORDER = (9, 8, 7, 6, 4, 3, 2, 1)
SMALL_CYCLE = 24
COUNTS_PER_PALACE = 3


def _normalize_dun(dun: str) -> str:
    mapping = {"阳": "阳", "陽": "阳", "阴": "阴", "陰": "阴"}
    try:
        return mapping[dun]
    except (KeyError, TypeError) as exc:
        raise ValueError("dun须为阳/阴") from exc


def _positive_count(value: Any, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field}须为整数")
    if value < 1:
        raise ValueError(f"{field}须>=1")
    return value


def taiyi_from_entry_count(entry_count: int, *, dun: str) -> dict[str, Any]:
    """由入局积数按24小周求太乙宫。"""
    n = _positive_count(entry_count, field="entry_count")
    dun_norm = _normalize_dun(dun)
    order = YANG_PALACE_ORDER if dun_norm == "阳" else YIN_PALACE_ORDER

    remainder_24 = n % SMALL_CYCLE or SMALL_CYCLE
    palace_index = (remainder_24 - 1) // COUNTS_PER_PALACE
    count_in_palace = (remainder_24 - 1) % COUNTS_PER_PALACE + 1
    palace = order[palace_index]

    return {
        "rule_id": G2_RULE_ID,
        "source_profile": SOURCE_PROFILE,
        "dun": dun_norm,
        "entry_count": n,
        "remainder_24": remainder_24,
        "palace_index": palace_index,
        "count_in_palace": count_in_palace,
        "taiyi_palace": palace,
        "palace_order": list(order),
        "small_cycle": SMALL_CYCLE,
        "counts_per_palace": COUNTS_PER_PALACE,
        "middle_five_excluded": True,
        "policy": (
            "24算一周，三算一宫；余0按第24算处理。"
            "阳顺、阴逆，均只行外八宫。"
        ),
    }


def taiyi_from_ju(ju: int, *, dun: str) -> dict[str, Any]:
    """72局入口：局号作为入局积数，24局一周，共重复三周。"""
    if isinstance(ju, bool) or not isinstance(ju, int) or not 1 <= ju <= 72:
        raise ValueError("ju须为1..72整数")
    result = taiyi_from_entry_count(ju, dun=dun)
    return {
        **result,
        "ju": ju,
        "helper_status": "72ju_direct_entry_count",
    }
