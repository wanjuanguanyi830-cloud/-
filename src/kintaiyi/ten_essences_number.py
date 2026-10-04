"""C54 十精太乙数：360周纪 / 72元法的纯数值层。

直接来源：
- 《太乙统宗宝鉴》“明十精太乙所主”第十项；
- 《武经总要》十精太乙数条。

本层只给 1..72 的太乙数，不附带云气/风雨断语。
"""

from __future__ import annotations

from typing import Any

from .taiyi_rules import integer

C54_VERSION = "taiyi-c54-ten-essences-number-v1"

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "witness_volumes": [18, 20],
    "rule": "太乙数",
    "big_cycle": 360,
    "small_cycle": 72,
    "source_text_summary": "周法三百六十去之，不尽；元法七十二去之，不尽，命起一数。",
    "wujing_zongyao": "太乙局法七十二除之，不尽者，命起一数。",
}

LEGACY_AUDIT = {
    "function": "yunqi.shijing_shu",
    "numeric_core_equivalent": True,
    "wrapper_canonical_equivalent": False,
    "reason": (
        "旧函数 rem%360 再 %72 的数值核心与来源周期一致；"
        "但同时附带30/40/50等天气断语与总诀，故整个wrapper不可直接升为C54。"
    ),
}

OMEN_BOUNDARY = {
    "number_only_in_c54": True,
    "weather_omens_applied": False,
    "weather_omen_runtime_rule_id": "C59-TAIYI-NUMBER-OMEN",
    "direct_weather_special_numbers": [30, 40],
    "variant_weather_special_numbers": [50],
    "legacy_noncanonical_special_numbers": [10, 5],
    "policy": (
        "C54只负责1..72数值。30/40与50句读异文由C59解释；"
        "旧10/5独立天气特例无当前直接条文支持。"
    ),
}


def taiyi_number(accumulated_count: int) -> dict[str, Any]:
    """返回 1..72 的十精太乙数，保留360周纪中间量。"""
    count = integer(accumulated_count, 1)

    big_remainder = count % 360
    big_cycle_count = big_remainder or 360
    small_remainder = big_cycle_count % 72
    number = small_remainder or 72

    return {
        "schema_version": "1.0",
        "canonical": C54_VERSION,
        "rule_id": "C54-TAIYI-NUMBER",
        "source_profile": "tongzong_ten_essences_number",
        "accumulated_count": count,
        "big_cycle": 360,
        "big_cycle_remainder": big_remainder,
        "big_cycle_count": big_cycle_count,
        "small_cycle": 72,
        "small_cycle_remainder": small_remainder,
        "taiyi_number": number,
        "number_range": [1, 72],
        "cloud_omen_applied": False,
        "source_witness": dict(SOURCE_WITNESS),
        "legacy_audit": dict(LEGACY_AUDIT),
        "omen_boundary": dict(OMEN_BOUNDARY),
        "policy": (
            "C54只求太乙数；360与72边界余0均保留为周期末项。"
            "不因数值等于30/40/50而自动生成天气断语；旧10/5独立断语亦不采用。"
        ),
    }


def c54_catalog() -> dict[str, Any]:
    return {
        "canonical": C54_VERSION,
        "rule_id": "C54-TAIYI-NUMBER",
        "source_profile": "tongzong_ten_essences_number",
        "big_cycle": 360,
        "small_cycle": 72,
        "legacy_audit": dict(LEGACY_AUDIT),
        "omen_boundary": dict(OMEN_BOUNDARY),
    }
