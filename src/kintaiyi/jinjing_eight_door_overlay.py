"""《太乙金镜式经》八门空间叠加（开门加锚点）。

来源边界：
- 卷二“推八门所主法”固定八门次序与八方：
  开乾、休坎、生艮、伤震、杜巽、景离、死坤、惊兑；
- 卷一“推八门占岁计法”明确“常以开门加太乙”，
  并同列开门加主大将、客大将、定计大将。

本模块只实现“空间叠加”。
它不计算岁计/时计值事门，也不把值事门替换成开门。
"""

from __future__ import annotations

from typing import Any

from .taiyi_rules import GOD_ALIASES, GOD_POSITION, SIXTEEN, sector_to_nine_palace

SOURCE_PROFILE = "jinjing_volume1_2_eight_door_overlay"
RULE_ID = "J1-EIGHT-DOOR-OVERLAY"

DOOR_ORDER = ("开", "休", "生", "伤", "杜", "景", "死", "惊")

# 以乾一为开门时，对应卷二固定八方：
# 乾1 -> 坎8 -> 艮3 -> 震4 -> 巽9 -> 离2 -> 坤7 -> 兑6。
PALACE_RING = (1, 8, 3, 4, 9, 2, 7, 6)


def _palace(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value not in PALACE_RING:
        raise ValueError("锚点宫须为外八宫之一：1/2/3/4/6/7/8/9")
    return value


def _subject_palace(subject: Any) -> int:
    if isinstance(subject, int) and not isinstance(subject, bool):
        return _palace(subject)

    if not isinstance(subject, str):
        raise ValueError("对象须为外八宫数、十六宫位置或十六神名")

    normalized = GOD_ALIASES.get(subject, subject)
    sector = GOD_POSITION.get(normalized, normalized)
    if sector not in SIXTEEN:
        raise ValueError("对象须为外八宫数、十六宫位置或十六神名")
    return sector_to_nine_palace(sector)


def open_door_overlay(anchor_palace: int) -> dict[str, Any]:
    """把开门加在指定外八宫，依八方次序顺布八门。"""
    anchor = _palace(anchor_palace)
    start = PALACE_RING.index(anchor)
    rotated_palaces = PALACE_RING[start:] + PALACE_RING[:start]
    palace_to_door = dict(zip(rotated_palaces, DOOR_ORDER))
    door_to_palace = {door: palace for palace, door in palace_to_door.items()}
    return {
        "source_profile": SOURCE_PROFILE,
        "rule_id": RULE_ID,
        "anchor_palace": anchor,
        "anchor_door": "开",
        "palace_ring": list(PALACE_RING),
        "door_order": list(DOOR_ORDER),
        "palace_to_door": palace_to_door,
        "door_to_palace": door_to_palace,
        "policy": "只实现开门加锚点的空间八门；值事门周期另由岁计/时计规则负责。",
    }


def taiyi_eight_door_context(taiyi_palace: int, *, tianmu=None) -> dict[str, Any]:
    """以开门加太乙宫；可同时求天目在该太乙八门中的所临门。"""
    overlay = open_door_overlay(taiyi_palace)
    if tianmu is None:
        tianmu_palace = None
        tianmu_door = None
    else:
        tianmu_palace = _subject_palace(tianmu)
        tianmu_door = overlay["palace_to_door"][tianmu_palace]

    return {
        **overlay,
        "context": "太乙之八门",
        "taiyi_gate": "开",
        "tianmu": tianmu,
        "tianmu_palace": tianmu_palace,
        "tianmu_gate": tianmu_door,
    }


def general_eight_door_context(anchor_palace: int, *, eye=None, side: str) -> dict[str, Any]:
    """主/客大将八门通用辅助。

    主大将盘观察太乙、文昌；客大将盘观察太乙、始击。
    这里只负责空间叠加与对象所临门，不直接判门具。
    """
    if side not in {"主", "客", "定计"}:
        raise ValueError("side须为主、客或定计")
    overlay = open_door_overlay(anchor_palace)
    eye_palace = _subject_palace(eye) if eye is not None else None
    return {
        **overlay,
        "context": f"{side}大将之八门",
        "side": side,
        "eye": eye,
        "eye_palace": eye_palace,
        "eye_gate": overlay["palace_to_door"].get(eye_palace) if eye_palace is not None else None,
    }
