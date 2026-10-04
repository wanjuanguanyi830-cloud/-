"""C67 五福太乙位置：来源 profile 分离。

《太乙统宗宝鉴》与《太乙金镜式经》共享稳定核心：
- 五宫：乾、艮、巽、坤、中；
- 每宫45年；
- 225年完成五宫一轮。

但算法外层不同：
- 统宗：加宫盈差115，大周2250，小周225，再以45约；
- 金镜：直接以225为大周，不见统宗的宫盈差115。

因此调用方必须显式指定 source_profile；不得静默合并。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer

C67_VERSION = "taiyi-c67-wufu-source-profiles-v1"

WUFU_PALACES = (
    {"index": 1, "name": "黄秘", "position": "乾"},
    {"index": 2, "name": "黄始", "position": "艮"},
    {"index": 3, "name": "黄室", "position": "巽"},
    {"index": 4, "name": "黄廷", "position": "坤"},
    {"index": 5, "name": "玄室", "position": "中"},
)

PROFILES = {
    "tongzong": {
        "source_profile": "tongzong_volume6_7_wufu",
        "work": "太乙统宗宝鉴",
        "witness_volumes": [6, 7],
        "surplus_name": "宫盈差",
        "surplus": 115,
        "big_cycle": 2250,
        "small_cycle": 225,
        "years_per_palace": 45,
        "rule_id": "C67-WUFU-TONGZONG",
        "status": "primary_direct",
    },
    "jinjing": {
        "source_profile": "jinjing_volume5_wufu",
        "work": "太乙金镜式经",
        "volume": 5,
        "surplus_name": None,
        "surplus": 0,
        "big_cycle": 225,
        "small_cycle": None,
        "years_per_palace": 45,
        "rule_id": "C67-WUFU-JINJING",
        "status": "independent_source_variant",
    },
}

SOURCE_WITNESS = {
    "stable_core": {
        "cycle": 225,
        "years_per_palace": 45,
        "route": ["乾", "艮", "巽", "坤", "中"],
        "palace_names": ["黄秘", "黄始", "黄室", "黄廷", "玄室"],
    },
    "tongzong": {
        "formula": (
            "积年加宫盈差一百一十五，以大周二千二百五十除之；"
            "再以小周二百二十五去之，余以行宫率四十五约之；"
            "命起乾、艮、巽、坤、中宫。"
        ),
        "witness_volumes": [6, 7],
    },
    "jinjing": {
        "formula": (
            "积年以大周二百二十五去之，不尽为入周年数；"
            "又以四十五约之；命起乾、艮、巽、坤、中宫。"
        ),
        "volume": 5,
        "historical_check": "开元十二年积13331岁，在艮/辽东第11年。",
    },
}

UNSELECTED_VARIANTS = {
    "taibai_bingbei_later": {
        "work": "太白兵备统宗宝鉴",
        "status": "formula_variant_pending_audit",
        "observed": [
            "后期算法段见加宫盈差二百五十",
            "同页另有225/250周数字样冲突",
        ],
        "implemented": False,
        "canonical_selected": None,
        "policy": "未完成独立见证校勘前，不并入统宗115或金镜无盈差profile。",
    }
}

DEFERRED_LAYER = {
    "same_palace_omens": "deferred_explicit_relation_layer",
    "auspicious_number_beneficiaries": "deferred_c68",
    "auto_same_palace_inference": False,
    "policy": (
        "C67只求五福位置；与君基/臣基/民基/四神/大小游等同宫断语另层。"
        "五福吉算受益对象也不混入位置函数。"
    ),
}


def _profile(name: str) -> dict[str, Any]:
    try:
        return PROFILES[name]
    except KeyError as exc:
        raise ValueError("source_profile须为tongzong/jinjing") from exc


def wufu_position(
    accumulated_count: int,
    *,
    source_profile: str,
) -> dict[str, Any]:
    """按显式来源 profile 求五福所在宫与入宫年。"""
    count = integer(accumulated_count, 1)
    profile = _profile(source_profile)

    adjusted_count = count + profile["surplus"]
    big_remainder = adjusted_count % profile["big_cycle"]
    big_cycle_count = big_remainder or profile["big_cycle"]

    if profile["small_cycle"] is None:
        effective_remainder = big_remainder
        effective_count = big_cycle_count
        small_remainder = None
        small_cycle_count = None
    else:
        small_remainder = big_cycle_count % profile["small_cycle"]
        small_cycle_count = small_remainder or profile["small_cycle"]
        effective_remainder = small_remainder
        effective_count = small_cycle_count

    zero_index = effective_count - 1
    palace_index = zero_index // profile["years_per_palace"]
    year_in_palace = zero_index % profile["years_per_palace"] + 1
    palace = WUFU_PALACES[palace_index]

    return {
        "schema_version": "1.0",
        "canonical": C67_VERSION,
        "rule_id": profile["rule_id"],
        "source_profile": profile["source_profile"],
        "profile_key": source_profile,
        "source_work": profile["work"],
        "accumulated_count": count,
        "surplus_name": profile["surplus_name"],
        "surplus": profile["surplus"],
        "adjusted_count": adjusted_count,
        "big_cycle": profile["big_cycle"],
        "big_cycle_remainder": big_remainder,
        "big_cycle_count": big_cycle_count,
        "small_cycle": profile["small_cycle"],
        "small_cycle_remainder": small_remainder,
        "small_cycle_count": small_cycle_count,
        "effective_cycle": 225,
        "effective_remainder": effective_remainder,
        "effective_count": effective_count,
        "years_per_palace": profile["years_per_palace"],
        "palace_number": palace_index + 1,
        "year_in_palace": year_in_palace,
        "palace_name": palace["name"],
        "position": palace["position"],
        "same_palace_omens_applied": False,
        "auspicious_number_layer_applied": False,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "unselected_variants": copy.deepcopy(UNSELECTED_VARIANTS),
        "deferred_layer": copy.deepcopy(DEFERRED_LAYER),
        "policy": (
            "五福统宗/金镜公式必须显式分profile；稳定的225/45与五宫顺序可共用，"
            "但统宗115盈差和2250外周不得写回金镜，金镜无盈差也不得覆盖统宗。"
        ),
    }


def c67_catalog() -> dict[str, Any]:
    return {
        "canonical": C67_VERSION,
        "profiles": copy.deepcopy(PROFILES),
        "stable_palaces": copy.deepcopy(list(WUFU_PALACES)),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "unselected_variants": copy.deepcopy(UNSELECTED_VARIANTS),
        "deferred_layer": copy.deepcopy(DEFERRED_LAYER),
        "default_profile": None,
        "source_profile_required": True,
    }
