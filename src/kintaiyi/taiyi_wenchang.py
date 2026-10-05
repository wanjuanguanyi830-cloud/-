"""G3 天目/文昌：18周法与重留规则。

《太乙统宗宝鉴》卷一“求四计天目、文昌所在”：
- 置所求入局积数，以天目、文昌周法十八去之；
- 阳局命起武德/申，顺行十六宫间之神，乾、坤重留一算；
- 阴局命起吕申/寅，顺行十六宫间之神，巽、艮重留一算。

这直接生成18位循环，不需要72项查表。
"""

from __future__ import annotations

from typing import Any

from .taiyi_rules import SECTOR_GODS

G3_RULE_ID = "TZ1-WENCHANG-18"
SOURCE_PROFILE = "tongzong_volume1_wenchang_18_cycle"

YANG_WENCHANG_18 = (
    "申", "酉", "戌", "乾", "乾", "亥", "子", "丑", "艮",
    "寅", "卯", "辰", "巽", "巳", "午", "未", "坤", "坤",
)

YIN_WENCHANG_18 = (
    "寅", "卯", "辰", "巽", "巽", "巳", "午", "未", "坤",
    "申", "酉", "戌", "乾", "亥", "子", "丑", "艮", "艮",
)

YANG_HOLDS = frozenset({"乾", "坤"})
YIN_HOLDS = frozenset({"巽", "艮"})


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


def wenchang_cycle(dun: str) -> tuple[str, ...]:
    return YANG_WENCHANG_18 if _normalize_dun(dun) == "阳" else YIN_WENCHANG_18


def wenchang_from_entry_count(entry_count: int, *, dun: str) -> dict[str, Any]:
    """由入局积数按18周法求天目/文昌。"""
    n = _positive_count(entry_count, field="entry_count")
    dun_norm = _normalize_dun(dun)
    cycle = wenchang_cycle(dun_norm)

    remainder_18 = n % 18 or 18
    sector = cycle[remainder_18 - 1]
    god = SECTOR_GODS[sector]

    return {
        "rule_id": G3_RULE_ID,
        "source_profile": SOURCE_PROFILE,
        "dun": dun_norm,
        "entry_count": n,
        "remainder_18": remainder_18,
        "wenchang_sector": sector,
        "wenchang_god": god,
        "start_sector": "申" if dun_norm == "阳" else "寅",
        "start_god": "武德" if dun_norm == "阳" else "吕申",
        "hold_sectors": ["乾", "坤"] if dun_norm == "阳" else ["巽", "艮"],
        "cycle_18": list(cycle),
        "policy": (
            "18周法由十六宫顺行并在指定四维重留形成；"
            "余0按第18位处理，不改成第0位。"
        ),
    }


def wenchang_from_ju(ju: int, *, dun: str) -> dict[str, Any]:
    """72局入口：局号即该局入局积数，18周法每18局循环一次。"""
    if isinstance(ju, bool) or not isinstance(ju, int) or not 1 <= ju <= 72:
        raise ValueError("ju须为1..72整数")
    result = wenchang_from_entry_count(ju, dun=dun)
    return {
        **result,
        "ju": ju,
        "helper_status": "72ju_direct_entry_count",
    }
