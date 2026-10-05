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
DUTY_RULE_ID = "J1-EIGHT-DOOR-DUTY-OVERLAY"

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


def door_overlay(anchor_palace: int, anchor_door: str) -> dict[str, Any]:
    """把指定门加在锚点宫，依同一八门次序顺布。

    anchor_door="开" 对应卷一古法“开门加太乙”；
    anchor_door 为当期直使门时，对应卷一“直门加太乙”的动态盘。
    """
    anchor = _palace(anchor_palace)
    if anchor_door not in DOOR_ORDER:
        raise ValueError("anchor_door须为开休生伤杜景死惊之一")

    palace_start = PALACE_RING.index(anchor)
    rotated_palaces = PALACE_RING[palace_start:] + PALACE_RING[:palace_start]
    door_start = DOOR_ORDER.index(anchor_door)
    rotated_doors = DOOR_ORDER[door_start:] + DOOR_ORDER[:door_start]
    palace_to_door = dict(zip(rotated_palaces, rotated_doors))
    door_to_palace = {door: palace for palace, door in palace_to_door.items()}
    return {
        "source_profile": SOURCE_PROFILE,
        "rule_id": RULE_ID if anchor_door == "开" else DUTY_RULE_ID,
        "anchor_palace": anchor,
        "anchor_door": anchor_door,
        "palace_ring": list(PALACE_RING),
        "door_order": list(DOOR_ORDER),
        "palace_to_door": palace_to_door,
        "door_to_palace": door_to_palace,
        "policy": (
            "空间叠加与值事门周期分层；本函数只消费已知anchor_door，"
            "不自行计算岁计或时计直使。"
        ),
    }


def open_door_overlay(anchor_palace: int) -> dict[str, Any]:
    """古法固定“开门加锚点”空间盘。"""
    return door_overlay(anchor_palace, "开")


def duty_door_overlay(anchor_palace: int, direct_gate: str) -> dict[str, Any]:
    """把已求出的当期直使门加在锚点宫。"""
    return door_overlay(anchor_palace, direct_gate)


def taiyi_eight_door_context(
    taiyi_palace: int, *, tianmu=None, anchor_door: str = "开"
) -> dict[str, Any]:
    """以指定门加太乙宫；可同时求天目在该八门盘中的所临门。"""
    overlay = door_overlay(taiyi_palace, anchor_door)
    if tianmu is None:
        tianmu_palace = None
        tianmu_door = None
    else:
        tianmu_palace = _subject_palace(tianmu)
        tianmu_door = overlay["palace_to_door"][tianmu_palace]

    return {
        **overlay,
        "context": "太乙之八门",
        "taiyi_gate": anchor_door,
        "tianmu": tianmu,
        "tianmu_palace": tianmu_palace,
        "tianmu_gate": tianmu_door,
    }


def general_eight_door_context(anchor_palace: int, *, eye=None, side: str, anchor_door: str = "开") -> dict[str, Any]:
    """主/客大将八门通用辅助。

    主大将盘观察太乙、文昌；客大将盘观察太乙、始击。
    这里只负责空间叠加与对象所临门，不直接判门具。
    """
    if side not in {"主", "客", "定计"}:
        raise ValueError("side须为主、客或定计")
    overlay = door_overlay(anchor_palace, anchor_door)
    eye_palace = _subject_palace(eye) if eye is not None else None
    return {
        **overlay,
        "context": f"{side}大将之八门",
        "side": side,
        "eye": eye,
        "eye_palace": eye_palace,
        "eye_gate": overlay["palace_to_door"].get(eye_palace) if eye_palace is not None else None,
    }
