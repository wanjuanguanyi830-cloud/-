"""C36 《太乙统宗宝鉴》阳九 / 百六大小限。

直接按“求阳九灾变之期大小限数”“求百六灾变之期大小限数术”结构化。
输入沿项目 cycles 约定：0基 accumulated_year，由调用层负责积年纪元。
"""

from __future__ import annotations

from typing import Any

from .taiyi_rules import integer

LIMITS_VERSION = "taiyi-c36-yangjiu-bailiu-v1"

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "online_witness_volume": 10,
    "project_legacy_volume_label": 9,
    "volume_status": "witness_volume_variant",
    "sections": [
        "明太乙阳九百六厄会附",
        "求阳九灾变之期大小限数",
        "求百六灾变之期大小限数术",
    ],
    "policy": "在线见证卷十与项目旧卷九标注并存；视为卷次见证差异，不复制两套算法。",
}

YANGJIU_SPEC = {
    "name": "阳九",
    "big_limit": 4560,
    "small_limit": 456,
    "small_limit_count": 10,
    "surplus_offset": 130,
    "extreme": "阳穷于九",
}

BAILIU_SPEC = {
    "name": "百六",
    "big_limit": 4320,
    "small_limit": 288,
    "small_limit_count": 15,
    "surplus_offset": 2050,
    "extreme": "阴穷于六",
}


def _limit_state(accumulated_year: int, spec: dict[str, Any], rule_id: str) -> dict[str, Any]:
    accumulated_year = integer(accumulated_year)
    big = spec["big_limit"]
    small = spec["small_limit"]
    count = spec["small_limit_count"]
    offset = spec["surplus_offset"]

    adjusted = accumulated_year + offset
    remainder = adjusted % big

    if remainder == 0:
        small_index = count
        year_in_small = small
    else:
        small_index = (remainder - 1) // small + 1
        year_in_small = (remainder - 1) % small + 1

    return {
        "rule_id": rule_id,
        "canonical": LIMITS_VERSION,
        "source_profile": "tongzong_yangjiu_bailiu",
        "source_witness": dict(SOURCE_WITNESS),
        "name": spec["name"],
        "accumulated_year": accumulated_year,
        "surplus_offset": offset,
        "adjusted_year": adjusted,
        "big_limit": big,
        "small_limit": small,
        "small_limit_count": count,
        "cycle_remainder": remainder,
        "small_limit_index": small_index,
        "year_in_small_limit": year_in_small,
        "at_small_limit_end": year_in_small == small,
        "at_big_limit_end": remainder == 0,
        "extreme": spec["extreme"],
        "policy": (
            "大小限只按积年+盈差取模；旧pan的阳九/百六地支位置不是本规则结果，"
            "不得直接搬入canonical cycles.limits。"
        ),
    }


def yangjiu_limit(accumulated_year: int) -> dict[str, Any]:
    """阳九：4560 大限、456 小限、阳盈差 130。"""
    return _limit_state(accumulated_year, YANGJIU_SPEC, "C36-YJ")


def bailiu_limit(accumulated_year: int) -> dict[str, Any]:
    """百六：4320 大限、288 小限、阴盈差 2050。"""
    return _limit_state(accumulated_year, BAILIU_SPEC, "C36-BL")


def yangjiu_bailiu_limits(accumulated_year: int) -> dict[str, Any]:
    """可直接作为 pan v2 cycles.limits 的结构。"""
    accumulated_year = integer(accumulated_year)
    return {
        "canonical": LIMITS_VERSION,
        "source_profile": "tongzong_yangjiu_bailiu",
        "yangjiu": yangjiu_limit(accumulated_year),
        "bailiu": bailiu_limit(accumulated_year),
        "cross_rule_merge": False,
        "policy": "阳九与百六共享积年输入，但各自按独立大限、小限与盈差计算。",
    }
