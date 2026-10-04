"""C66 《太乙统宗宝鉴》三基（君基/臣基/民基）位置周期。

直接来源见证在卷六/卷七编次有差异，但三条公式结构稳定：
- 均先以积年加邦盈差250；
- 君基：大周3600，小周360，30年一邦，午起；
- 臣基：大周360，小周36，3年一邦，午起；
- 民基：大周360，小周12，1年一邦，戌起；
- 均顺行十二辰。

本层只计算三基所在邦及入邦年数。
三基与五福、三神等同宫所主另层，不由位置自动推断。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import BRANCHES, integer

C66_VERSION = "taiyi-c66-three-bases-cycles-v1"

BANG_SURPLUS = 250

THREE_BASES = {
    "君基": {
        "big_cycle": 3600,
        "small_cycle": 360,
        "years_per_state": 30,
        "start_branch": "午",
        "rule_id": "C66-JUNJI",
        "identity": "人君之象",
        "source_title": "明君基太乙所主术",
    },
    "臣基": {
        "big_cycle": 360,
        "small_cycle": 36,
        "years_per_state": 3,
        "start_branch": "午",
        "rule_id": "C66-CHENJI",
        "identity": "辅相之象",
        "source_title": "明臣基太乙所主术",
    },
    "民基": {
        "big_cycle": 360,
        "small_cycle": 12,
        "years_per_state": 1,
        "start_branch": "戌",
        "rule_id": "C66-MINJI",
        "identity": "庶民之象",
        "source_title": "明民基太乙所主术",
    },
}

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "witness_volumes": [6, 7],
    "volume_status": "witness_volume_variant",
    "common": {
        "surplus_name": "邦盈差",
        "surplus": 250,
        "route": "顺行十二辰",
    },
    "君基": {
        "big_cycle": 3600,
        "small_cycle": 360,
        "rate": 30,
        "start": "午邦",
        "direct_formula": (
            "积年加邦盈差二百五十，以大周三千六百除之；"
            "小周三百六十；行邦率三十；命起午邦，顺行十二辰。"
        ),
    },
    "臣基": {
        "big_cycle": 360,
        "small_cycle": 36,
        "rate": 3,
        "start": "午邦",
        "direct_formula": (
            "积年加邦盈差二百五十，以大周三百六十除之；"
            "小周三十六；行邦率三；命起午邦，顺行十二辰。"
        ),
    },
    "民基": {
        "big_cycle": 360,
        "small_cycle": 12,
        "rate": 1,
        "start": "戌邦",
        "source_form_start": "戍邦",
        "direct_formula": (
            "积年加邦盈差二百五十，以大周三百六十除之；"
            "小周十二；命起戍邦，顺行十二辰。"
        ),
        "normalization": "来源转录常写戍邦；地支位置按戌正规化，原字保留在witness。",
    },
    "later_collation": {
        "work": "太乙金钥匙",
        "role": "later_arithmetic_collation",
        "checks": [
            "君基每30年一邦；余200算见子邦第20年",
            "臣基每3年一邦；余2算见午邦第2年",
        ],
    },
}

DEFERRED_LAYER = {
    "same_palace_omens": "deferred_explicit_evidence_layer",
    "auto_same_palace_inference": False,
    "examples": ["臣基与五福", "臣基与民基", "民基与五福"],
    "policy": "C66只求三基位置；同宫断语须后续显式关系层处理。",
}


def _spec(name: str) -> dict[str, Any]:
    try:
        return THREE_BASES[name]
    except KeyError as exc:
        raise ValueError("name须为君基/臣基/民基") from exc


def three_base_position(name: str, accumulated_count: int) -> dict[str, Any]:
    """求君基/臣基/民基所在邦及入邦年数。"""
    spec = _spec(name)
    count = integer(accumulated_count, 1)

    adjusted_count = count + BANG_SURPLUS

    big_remainder = adjusted_count % spec["big_cycle"]
    big_cycle_count = big_remainder or spec["big_cycle"]

    small_remainder = big_cycle_count % spec["small_cycle"]
    small_cycle_count = small_remainder or spec["small_cycle"]

    zero_index = small_cycle_count - 1
    state_offset = zero_index // spec["years_per_state"]
    year_in_state = zero_index % spec["years_per_state"] + 1

    start_index = BRANCHES.index(spec["start_branch"])
    branch = BRANCHES[(start_index + state_offset) % 12]

    return {
        "schema_version": "1.0",
        "canonical": C66_VERSION,
        "rule_id": spec["rule_id"],
        "source_profile": "tongzong_three_bases_cycles",
        "base": name,
        "identity": spec["identity"],
        "accumulated_count": count,
        "surplus": BANG_SURPLUS,
        "adjusted_count": adjusted_count,
        "big_cycle": spec["big_cycle"],
        "big_cycle_remainder": big_remainder,
        "big_cycle_count": big_cycle_count,
        "small_cycle": spec["small_cycle"],
        "small_cycle_remainder": small_remainder,
        "small_cycle_count": small_cycle_count,
        "years_per_state": spec["years_per_state"],
        "state_offset": state_offset,
        "state_number": state_offset + 1,
        "year_in_state": year_in_state,
        "start_branch": spec["start_branch"],
        "branch": branch,
        "same_palace_omens_applied": False,
        "deferred_layer": copy.deepcopy(DEFERRED_LAYER),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "policy": (
            "按积年+邦盈差250后依各自大周/小周/行邦率求位；"
            "余0保留为周期末项。C66不自动比较其他神位，也不生成同宫断语。"
        ),
    }


def junji_position(accumulated_count: int) -> dict[str, Any]:
    return three_base_position("君基", accumulated_count)


def chenji_position(accumulated_count: int) -> dict[str, Any]:
    return three_base_position("臣基", accumulated_count)


def minji_position(accumulated_count: int) -> dict[str, Any]:
    return three_base_position("民基", accumulated_count)


def c66_catalog() -> dict[str, Any]:
    return {
        "canonical": C66_VERSION,
        "source_profile": "tongzong_three_bases_cycles",
        "rule_ids": {name: row["rule_id"] for name, row in THREE_BASES.items()},
        "surplus": BANG_SURPLUS,
        "bases": copy.deepcopy(THREE_BASES),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "deferred_layer": copy.deepcopy(DEFERRED_LAYER),
    }
