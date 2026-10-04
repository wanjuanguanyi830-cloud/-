"""C18 《紫庭经》主来源 / 《太乙统宗宝鉴》参校来源容器。

本模块只管理来源层级和结构化结果，不实现六项术法本身。
"""

from __future__ import annotations

import copy
from typing import Any

ZITINGJING_SOURCE_VERSION = "taiyi-c18-zitingjing-source-v1"

RULES = {
    "taiyi_nine_stars": {
        "legacy_name": "太乙九星",
        "primary_source": "zitingjing",
        "collation_sources": ["tongzong_volume6"],
    },
    "wenchang_nine_stars": {
        "legacy_name": "文昌九星",
        "primary_source": "zitingjing",
        "collation_sources": ["tongzong_volume6"],
    },
    "wenchang_changes": {
        "legacy_name": "文昌变化",
        "primary_source": "zitingjing",
        "collation_sources": ["tongzong_volume6"],
    },
    "shiji_changes": {
        "legacy_name": "始击变化",
        "primary_source": "zitingjing",
        "collation_sources": ["tongzong_volume6"],
    },
    "three_banners": {
        "legacy_name": "三旗行宫",
        "primary_source": "zitingjing",
        "collation_sources": ["tongzong_volume10"],
    },
    "nine_palace_nobles": {
        "legacy_name": "九宫贵神",
        "primary_source": "zitingjing",
        "collation_sources": ["tongzong_volume10"],
    },
}


def _validate_rule(rule_key: str) -> dict[str, Any]:
    if rule_key not in RULES:
        raise ValueError(f"未知《紫庭经》P1规则: {rule_key}")
    return RULES[rule_key]


def build_zitingjing_rule_sources(
    rule_key: str,
    *,
    primary_result: dict[str, Any] | None = None,
    collation_results: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """保存一个规则的主来源结果与参校来源结果。

    不自动将统宗结果提升为canonical；primary_result缺失时保持未完成。
    """
    meta = _validate_rule(rule_key)
    collations = copy.deepcopy(collation_results or {})
    allowed = set(meta["collation_sources"])
    unknown = sorted(set(collations) - allowed)
    if unknown:
        raise ValueError(f"未知参校来源: {', '.join(unknown)}")

    primary = copy.deepcopy(primary_result) if primary_result is not None else None
    primary_ready = isinstance(primary, dict) and bool(primary)

    return {
        "schema_version": "1.0",
        "canonical": ZITINGJING_SOURCE_VERSION,
        "rule_key": rule_key,
        "legacy_name": meta["legacy_name"],
        "primary_source": meta["primary_source"],
        "primary_result": primary,
        "primary_ready": primary_ready,
        "collation_sources": list(meta["collation_sources"]),
        "collation_results": collations,
        "canonical_selected": "zitingjing" if primary_ready else None,
        "cross_source_merge": False,
        "status": "primary_ready" if primary_ready else "primary_pending",
        "policy": (
            "《紫庭经》为主要参考；《太乙统宗宝鉴》仅作参校。"
            "参校可用于校异、补证、版本比较，但不得静默覆盖主来源。"
        ),
    }


def build_zitingjing_p1_sources(
    *,
    results: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """批量构建六项C18来源容器。

    results[rule_key] 可含 primary_result / collation_results。
    """
    supplied = results or {}
    if not isinstance(supplied, dict):
        raise TypeError("results须为dict")
    unknown = sorted(set(supplied) - set(RULES))
    if unknown:
        raise ValueError(f"未知《紫庭经》P1规则: {', '.join(unknown)}")

    rules = {}
    for key in RULES:
        item = supplied.get(key) or {}
        if not isinstance(item, dict):
            raise TypeError(f"{key}配置须为dict")
        rules[key] = build_zitingjing_rule_sources(
            key,
            primary_result=item.get("primary_result"),
            collation_results=item.get("collation_results"),
        )

    return {
        "schema_version": "1.0",
        "canonical": ZITINGJING_SOURCE_VERSION,
        "primary_source": "zitingjing",
        "rules": rules,
        "cross_source_merge": False,
        "policy": "六项规则均以《紫庭经》为主来源，统宗卷六/卷十只作参校。",
    }
