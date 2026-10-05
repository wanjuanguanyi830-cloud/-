"""C18 《太乙紫庭经》主来源 / 《太乙统宗宝鉴》参校来源容器。

本模块只管理来源层级和结构化结果，不实现六项术法本身。
"""

from __future__ import annotations

import copy
from typing import Any

ZITINGJING_SOURCE_VERSION = "taiyi-c18-zitingjing-source-v1"
PRIMARY_SOURCE_ID = "zitingjing"
PRIMARY_SOURCE_TITLE = "太乙紫庭经"

RULES = {
    "taiyi_nine_stars": {
        "legacy_name": "太乙九星",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_evidence_level": "direct_text_verified",
        "collation_sources": ["tongzong_volume6"],
    },
    "wenchang_nine_stars": {
        "legacy_name": "文昌九星",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_evidence_level": "prior_scan_confirmed_page_record_pending",
        "collation_sources": ["tongzong_volume6", "sancai_shiwei_volume81"],
    },
    "wenchang_changes": {
        "legacy_name": "文昌变化",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_evidence_level": "direct_text_verified",
        "collation_sources": ["tongzong_volume6"],
    },
    "shiji_changes": {
        "legacy_name": "始击变化",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_evidence_level": "direct_text_verified",
        "collation_sources": ["tongzong_volume6"],
    },
    "three_banners": {
        "legacy_name": "三旗行宫",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_evidence_level": "project_attribution_unverified",
        "collation_sources": ["tongzong_volume10"],
    },
    "nine_palace_nobles": {
        "legacy_name": "九宫贵神",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_evidence_level": "project_attribution_unverified",
        "collation_sources": ["tongzong_volume10"],
    },
}


def _validate_rule(rule_key: str) -> dict[str, Any]:
    if rule_key not in RULES:
        raise ValueError(f"未知《太乙紫庭经》P1规则: {rule_key}")
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

    evidence_level = meta["primary_evidence_level"]
    primary_result_allowed = evidence_level == "direct_text_verified"
    if primary_result is not None and not primary_result_allowed:
        raise ValueError(
            f"{rule_key}尚无可逐条校读的《太乙紫庭经》直接正文，"
            "不得注入primary_result"
        )

    primary = copy.deepcopy(primary_result) if primary_result is not None else None
    primary_ready = isinstance(primary, dict) and bool(primary)

    if primary_ready:
        status = "primary_ready"
    elif evidence_level == "direct_text_verified":
        status = "primary_pending"
    elif evidence_level == "prior_scan_confirmed_page_record_pending":
        status = "primary_prior_scan_confirmed_page_record_pending"
    elif evidence_level == "catalog_attested_text_pending":
        status = "primary_text_pending"
    else:
        status = "primary_attribution_unverified"

    return {
        "schema_version": "1.0",
        "canonical": ZITINGJING_SOURCE_VERSION,
        "rule_key": rule_key,
        "legacy_name": meta["legacy_name"],
        "primary_source": meta["primary_source"],
        "primary_source_title": PRIMARY_SOURCE_TITLE,
        "primary_evidence_level": evidence_level,
        "primary_result_allowed": primary_result_allowed,
        "primary_result": primary,
        "primary_ready": primary_ready,
        "collation_sources": list(meta["collation_sources"]),
        "collation_results": collations,
        "canonical_selected": "zitingjing" if primary_ready else None,
        "cross_source_merge": False,
        "status": status,
        "policy": (
            "《太乙紫庭经》是项目拟定的主来源目标，但证据等级必须逐条记录。"
            "只有已定位直接正文的项目可注入primary_result；用户确认的既往扫描事实、旧代码残留、目录证据或项目归属"
            "都不能代替重新挂载的逐页正文。统宗只作参校，不得静默覆盖。"
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
        raise ValueError(f"未知《太乙紫庭经》P1规则: {', '.join(unknown)}")

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
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_source_title": PRIMARY_SOURCE_TITLE,
        "rules": rules,
        "cross_source_merge": False,
        "policy": ("六项均保留《太乙紫庭经》为项目主来源目标，但证据等级不同；"
                   "只有direct_text_verified可生成primary_result；prior_scan_confirmed_page_record_pending只表示该明钞本此前已扫描但原页记录尚未重新挂载。统宗卷六/卷十只作参校。"),
    }


def build_zitingjing_source_variants(
    *,
    results: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """返回可直接合入 pan_v2.source_variants 的根容器。"""
    return {"zitingjing": build_zitingjing_p1_sources(results=results)}
