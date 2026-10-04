"""C49 《太乙统宗宝鉴》“明太、小游行宫卦不同术”。

本条解释太游、小游为何使用不同内卦周期/策义。
它不是“每年比较两个当前内卦是否不相等”的布尔规则。
"""

from __future__ import annotations

import copy
from typing import Any

C49_VERSION = "taiyi-c49-taiyou-xiaoyou-distinction-v1"

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "volume": 10,
    "section": "明太、小游行宫卦不同术",
}

SYSTEMS = {
    "taiyou": {
        "name": "太游",
        "inner_trigram_years": 36,
        "rate_symbol": "乾天之策",
        "rank_relation": "尊/上",
        "may_travel_any_trigram": True,
        "not_restricted_to": "乾",
        "canonical_track_dependency": "C38-BL-INNER",
    },
    "xiaoyou": {
        "name": "小游",
        "inner_trigram_years": 24,
        "rate_symbol": "坤地之策",
        "rank_relation": "卑/下",
        "may_travel_any_trigram": True,
        "not_restricted_to": "坤",
        "canonical_track_dependency": "C47-XY-INNER",
    },
}

DOCTRINAL_PRINCIPLE = {
    "question": (
        "太游得乾天之策，何以行坤；小游得坤地之策，何以行乾？"
    ),
    "answer": "阴得阳而生，阳得阴而成；天地配合，阴阳互用，一阴一阳之谓道。",
    "structural_meaning": (
        "乾/坤之策是两套轨运的率义与尊卑说明，不是把太游锁死在乾、"
        "或把小游锁死在坤的卦位限制。"
    ),
}

LEGACY_REFERENCE_AUDIT = {
    "location": "guiyun.zonghe()['行宮卦異']",
    "canonical_equivalent": False,
    "issues": [
        "旧综合包装仅比较dayou内卦 != xiaoyou内卦",
        "原条文讨论的是36年/24年两套轨运及乾天/坤地策义的差别",
        "条文明确解释太游仍可行坤、小游仍可行乾，故当前卦相同也不推翻制度差异",
        "布尔相等/不等只能作为当前状态观察，不是本术的canonical结论",
    ],
}


def taiyou_xiaoyou_distinction() -> dict[str, Any]:
    """返回原文制度差异，不要求当前盘面。"""
    return {
        "schema_version": "1.0",
        "canonical": C49_VERSION,
        "rule_id": "C49-TX-DISTINCTION",
        "source_profile": "tongzong_volume10_taiyou_xiaoyou_distinction",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "systems": copy.deepcopy(SYSTEMS),
        "doctrinal_principle": copy.deepcopy(DOCTRINAL_PRINCIPLE),
        "systems_distinct": True,
        "distinct_by_current_trigram_inequality": False,
        "policy": (
            "太游/小游之不同首先是轨运周期、策义与尊卑职责不同；"
            "不得把当前内卦是否相等当成原文规则本体。"
        ),
    }


def _validate_taiyou_inner(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError("taiyou_inner须为dict")
    if value.get("rule_id") != "C38-BL-INNER":
        raise ValueError("taiyou_inner必须来自C38-BL-INNER")
    if value.get("years_per_palace") != 36:
        raise ValueError("C38太游内卦须保持36年一宫")
    return value


def _validate_xiaoyou_inner(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError("xiaoyou_inner须为dict")
    if value.get("rule_id") != "C47-XY-INNER":
        raise ValueError("xiaoyou_inner必须来自C47-XY-INNER")
    if value.get("years_per_trigram") != 24:
        raise ValueError("C47小游内卦须保持24年一卦")
    return value


def observe_current_inner_trigrams(
    taiyou_inner: dict[str, Any],
    xiaoyou_inner: dict[str, Any],
) -> dict[str, Any]:
    """比较当前两内卦；结果仅是派生观察，不是“卦不同术”的真值。"""
    ty = _validate_taiyou_inner(taiyou_inner)
    xy = _validate_xiaoyou_inner(xiaoyou_inner)

    taiyou_trigram = ty.get("trigram")
    xiaoyou_trigram = xy.get("trigram")
    if not isinstance(taiyou_trigram, str) or not taiyou_trigram:
        raise ValueError("C38太游内卦缺trigram")
    if not isinstance(xiaoyou_trigram, str) or not xiaoyou_trigram:
        raise ValueError("C47小游内卦缺trigram")

    same = taiyou_trigram == xiaoyou_trigram
    return {
        "schema_version": "1.0",
        "canonical": C49_VERSION,
        "rule_id": "C49-TX-OBSERVATION",
        "source_profile": "derived_current_track_observation",
        "taiyou": {
            "rule_id": ty["rule_id"],
            "trigram": taiyou_trigram,
            "years_per_inner_trigram": ty["years_per_palace"],
        },
        "xiaoyou": {
            "rule_id": xy["rule_id"],
            "trigram": xiaoyou_trigram,
            "years_per_inner_trigram": xy["years_per_trigram"],
        },
        "same_current_trigram": same,
        "different_current_trigram": not same,
        "systems_still_distinct": True,
        "semantic_status": "derived_observation_not_source_verdict",
        "policy": (
            "当前内卦同/异只描述这一时点；即使同卦，"
            "C49原文所说36年/24年与乾天/坤地策义的制度差异仍成立。"
        ),
    }


def c49_catalog() -> dict[str, Any]:
    return {
        "canonical": C49_VERSION,
        "rule_id": "C49-TX-DISTINCTION",
        "source_profile": "tongzong_volume10_taiyou_xiaoyou_distinction",
        "systems": copy.deepcopy(SYSTEMS),
        "doctrinal_principle": copy.deepcopy(DOCTRINAL_PRINCIPLE),
        "legacy_reference_audit": copy.deepcopy(LEGACY_REFERENCE_AUDIT),
        "whole_volume9_wrapper_migrated": False,
    }
