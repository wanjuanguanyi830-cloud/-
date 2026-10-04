"""C32 跨卷 derived helper。

V17-D1 仅对照 D8-05（内外占攻击）与 V17-09（求索所得）。
不计算内外、不重跑求索、不解析中文断语。
"""

from __future__ import annotations

import copy
from typing import Any

C32_VERSION = "taiyi-c32-cross-volume-guxu-v1"


def _require_dict(name: str, value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{name}须为dict")
    return value


def build_guxu_cross_volume_helper(
    *,
    attack_result: dict[str, Any],
    request_result: dict[str, Any],
) -> dict[str, Any]:
    """V17-D1：卷五/D8-05 × 卷十七/V17-09 只读对照。"""
    attack = _require_dict("attack_result", attack_result)
    request = _require_dict("request_result", request_result)

    if attack.get("rule_id") != "D8-05":
        raise ValueError("attack_result必须来自D8-05")
    if request.get("source_rule_id") != "V17-09":
        raise ValueError("request_result必须来自V17-09")

    attack_realm = attack.get("realm")
    request_realm = ((request.get("inputs") or {}).get("skyeyes_realm"))
    if attack_realm not in {"内", "外"}:
        raise ValueError("D8-05 realm须为内/外")
    if request_realm not in {"内", "外"}:
        raise ValueError("V17-09 inputs.skyeyes_realm须为内/外")

    realm_consistent = attack_realm == request_realm
    guxu = "内为虚" if attack_realm == "内" else "外为孤"
    attack_direction = "外" if attack_realm == "内" else "内"

    request_summary = request.get("summary")
    base_expected = "positive" if attack_realm == "内" else "negative"

    if not realm_consistent:
        alignment = "input_conflict"
    elif request_summary == base_expected:
        alignment = "base_aligned"
    elif request_summary == "mixed_evidence":
        alignment = "request_modified_by_other_conditions"
    elif request_summary in {"positive", "negative"}:
        alignment = "request_direction_changed_by_other_conditions"
    else:
        alignment = "undetermined"

    return {
        "schema_version": "1.0",
        "canonical": C32_VERSION,
        "source_rule_id": "V17-D1",
        "source_status": "derived_cross_volume_helper",
        "cross_volume": True,
        "canonical_source_rule": False,
        "sources": {
            "volume5_or_d8": {
                "rule_id": "D8-05",
                "result": copy.deepcopy(attack),
            },
            "volume17": {
                "rule_id": "V17-09",
                "result": copy.deepcopy(request),
            },
        },
        "realm": attack_realm,
        "guxu": guxu,
        "attack_direction": attack_direction,
        "request_summary": request_summary,
        "realm_consistent": realm_consistent,
        "alignment": alignment,
        "policy": (
            "只比较两个已结构化来源结果；"
            "不得反写D8-05或V17-09，不得成为卷十七canonical source rule。"
        ),
    }


def c32_catalog() -> dict[str, Any]:
    return {
        "canonical": C32_VERSION,
        "helpers": ["V17-D1"],
        "source_status": "derived_cross_volume_helper",
        "canonical_source_rule_count": 0,
        "policy": "跨卷helper永不进入V17 canonical source rule集合。",
    }
