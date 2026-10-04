"""C63 卷七天乙 / 地乙 / 直符三神 360/36 行宫基础层。

直接来源：《太乙统宗宝鉴》卷七。
三神共同结构：
- 大周360；
- 小周36；
- 每宫3年；
- 十二宫序：1..9，继绛宫、明堂、玉堂；
- 天乙起6宫；
- 地乙起9宫；
- 直符起5宫。

本层只计算所在宫与入宫年。
同宫灾应另层，不因两个位置相同自动制造断语。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer

C63_VERSION = "taiyi-c63-volume7-three-spirit-cycles-v1"

TWELVE_PALACES: tuple[int | str, ...] = (
    1, 2, 3, 4, 5, 6, 7, 8, 9, "绛宫", "明堂", "玉堂"
)

SPIRITS = {
    "天乙": {
        "element": "金",
        "start_palace": 6,
        "source_title": "明天乙太乙金神所主术",
        "rule_id": "C63-TIANYI",
    },
    "地乙": {
        "element": "土",
        "start_palace": 9,
        "source_title": "明地乙太乙土神所主术",
        "rule_id": "C63-DIYI",
    },
    "直符": {
        "element": "火",
        "start_palace": 5,
        "source_title": "明直符太乙火神所主术",
        "rule_id": "C63-ZHIFU",
    },
}

NAME_ALIASES = {
    "天乙": "天乙",
    "地乙": "地乙",
    "直符": "直符",
}

LEGACY_NAME_AUDIT = {
    "值符": {
        "canonical_name": "直符",
        "status": "legacy_or_title_variant",
        "default_alias_enabled": False,
        "reason": "C15旧字段写“明值符太乙所主術”；卷七直接正文以“直符”为主名。",
    }
}

SOURCE_WITNESS = {
    "primary": {
        "work": "太乙统宗宝鉴",
        "volume": 7,
        "common_cycle": {
            "big_cycle": 360,
            "small_cycle": 36,
            "years_per_palace": 3,
            "palace_order": list(TWELVE_PALACES),
        },
        "starts": {
            "天乙": 6,
            "地乙": 9,
            "直符": 5,
        },
        "formula_summary": (
            "大周三百六十，小周三十六，余以行宫率三约；"
            "九宫后接绛宫、明堂、玉堂，算外。"
        ),
    },
    "collation": [
        {
            "work": "古今图书集成·艺术典",
            "role": "later_parallel_summary",
            "evidence": "明确十二宫次序为一至九、绛、明、玉，每三岁移一宫。",
        },
        {
            "work": "太乙秘书",
            "role": "later_collation",
            "evidence": "天乙上元六/中元二/下元绛；地乙九/五/一；直符五/一/九。",
        },
    ],
}

DEFERRED_LAYER = {
    "same_palace_omens": "deferred_explicit_evidence_layer",
    "auto_same_palace_inference": False,
    "reason": (
        "卷七同宫灾应虽有直接正文，但C63只锁定位置周期；"
        "后续应显式声明同宫对象，不从本模块位置结果自动制造断语。"
    ),
}


def canonical_spirit_name(name: str, *, allow_legacy_alias: bool = False) -> str:
    if name in NAME_ALIASES:
        return NAME_ALIASES[name]
    if allow_legacy_alias and name == "值符":
        return "直符"
    if name in LEGACY_NAME_AUDIT:
        raise ValueError(f"{name}不是C63 canonical名称")
    raise ValueError("未知C63神名")


def _cycle_state(accumulated_count: int) -> dict[str, int]:
    count = integer(accumulated_count, 1)

    big_remainder = count % 360
    big_cycle_year = big_remainder or 360

    small_remainder = big_cycle_year % 36
    small_cycle_year = small_remainder or 36

    palace_step = (small_cycle_year - 1) // 3
    year_in_palace = (small_cycle_year - 1) % 3 + 1

    return {
        "accumulated_count": count,
        "big_cycle": 360,
        "big_cycle_remainder": big_remainder,
        "big_cycle_year": big_cycle_year,
        "small_cycle": 36,
        "small_cycle_remainder": small_remainder,
        "small_cycle_year": small_cycle_year,
        "years_per_palace": 3,
        "palace_step": palace_step + 1,
        "year_in_palace": year_in_palace,
    }


def spirit_position(
    name: str,
    accumulated_count: int,
    *,
    allow_legacy_alias: bool = False,
) -> dict[str, Any]:
    """求卷七天乙/地乙/直符所在十二宫与入宫年。"""
    canonical_name = canonical_spirit_name(
        name,
        allow_legacy_alias=allow_legacy_alias,
    )
    spec = SPIRITS[canonical_name]
    cycle = _cycle_state(accumulated_count)

    start_index = TWELVE_PALACES.index(spec["start_palace"])
    offset = cycle["palace_step"] - 1
    palace = TWELVE_PALACES[(start_index + offset) % len(TWELVE_PALACES)]

    return {
        "schema_version": "1.0",
        "canonical": C63_VERSION,
        "rule_id": spec["rule_id"],
        "source_profile": "tongzong_volume7_three_spirit_cycles",
        "spirit": canonical_name,
        "element": spec["element"],
        "source_title": spec["source_title"],
        **cycle,
        "start_palace": spec["start_palace"],
        "palace_order": list(TWELVE_PALACES),
        "palace": palace,
        "same_palace_omens_applied": False,
        "deferred_layer": copy.deepcopy(DEFERRED_LAYER),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "policy": (
            "只按360/36、三年一宫与十二宫序计算位置；"
            "不自动比较其他神位置，也不在C63生成同宫灾应。"
        ),
    }


def tianyi_position(accumulated_count: int) -> dict[str, Any]:
    return spirit_position("天乙", accumulated_count)


def diyi_position(accumulated_count: int) -> dict[str, Any]:
    return spirit_position("地乙", accumulated_count)


def zhifu_position(accumulated_count: int) -> dict[str, Any]:
    return spirit_position("直符", accumulated_count)


def c63_catalog() -> dict[str, Any]:
    return {
        "canonical": C63_VERSION,
        "source_profile": "tongzong_volume7_three_spirit_cycles",
        "rule_ids": {name: row["rule_id"] for name, row in SPIRITS.items()},
        "spirits": copy.deepcopy(SPIRITS),
        "palace_order": list(TWELVE_PALACES),
        "big_cycle": 360,
        "small_cycle": 36,
        "years_per_palace": 3,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "legacy_name_audit": copy.deepcopy(LEGACY_NAME_AUDIT),
        "deferred_layer": copy.deepcopy(DEFERRED_LAYER),
    }
