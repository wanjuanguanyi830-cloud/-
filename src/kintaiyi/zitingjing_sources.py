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
        "primary_source": None,
        "source_role": "legacy_recovery_pointer",
        "primary_evidence_level": "ziting_manuscript_not_attested_modern_appendix_only",
        "collation_sources": ["tongzong_volume6", "sancai_shiwei_volume81"],
        "known_source_rule_id": "C70-TONGZONG-WENCHANG-NINE-STARS",
        "known_source_profile": "tongzong_volume6_ngj_wenchang_nine_stars",
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
        "primary_evidence_level": "ziting_not_attested_cross_source_only",
        "collation_sources": ["tongzong_volume10"],
        "known_source_rule_id": "C126-TONGZONG-THREE-BANNERS",
    },
    "nine_palace_nobles": {
        "legacy_name": "九宫贵神",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_evidence_level": "ziting_not_attested_cross_source_only",
        "collation_sources": ["tongzong_volume10"],
        "known_source_rule_id": "C127-TONGZONG-NINE-PALACE-NOBLES",
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
    elif evidence_level == "ziting_manuscript_not_attested_modern_appendix_only":
        status = "modern_appendix_cross_source_recovery_pointer"
    elif evidence_level == "catalog_attested_text_pending":
        status = "primary_text_pending"
    elif evidence_level == "ziting_not_attested_cross_source_only":
        status = "legacy_cross_source_recovery_pointer"
    else:
        status = "primary_attribution_unverified"

    return {
        "schema_version": "1.0",
        "canonical": ZITINGJING_SOURCE_VERSION,
        "rule_key": rule_key,
        "legacy_name": meta["legacy_name"],
        "primary_source": meta["primary_source"],
        "primary_source_title": (
            PRIMARY_SOURCE_TITLE if meta["primary_source"] == PRIMARY_SOURCE_ID else None
        ),
        "source_role": meta.get("source_role", "primary_candidate"),
        "primary_evidence_level": evidence_level,
        "primary_result_allowed": primary_result_allowed,
        "primary_result": primary,
        "primary_ready": primary_ready,
        "collation_sources": list(meta["collation_sources"]),
        "collation_results": collations,
        "known_source_rule_id": meta.get("known_source_rule_id"),
        "known_source_profile": meta.get("known_source_profile"),
        "canonical_selected": "zitingjing" if primary_ready else None,
        "cross_source_merge": False,
        "status": status,
        "policy": (
            "证据等级必须逐条记录。只有已定位紫庭直接正文的项目可注入primary_result；"
            "文昌九星的研易楼明钞目录未见题名，现代整理附篇只作跨来源恢复指针，现行可执行规则归统宗卷六C70。"
            "三旗行宫/九宫贵神现行可执行公式归统宗卷十。若未来原钞/异本证实另有同术，"
            "必须新增独立witness/profile，不得静默覆盖统宗。"
        ),
    }


def build_zitingjing_p1_sources(
    *,
    results: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """批量构建六项历史来源容器。

    其中三旗行宫/九宫贵神只保留旧术语恢复指针；其现行公式归统宗卷十。
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
        "policy": (
            "太乙九星、文昌变化、始击变化按紫庭直接证据管理；"
            "文昌九星仅保留历史恢复slot，primary_source为空，现行稳定规则归《太乙统宗宝鉴》卷六C70。"
            "三旗行宫与九宫贵神仅作为旧术语恢复指针，现行可执行canonical归《太乙统宗宝鉴》卷十。"
            "未来若发现明钞/异本同术，只新增独立ziting witness/profile。"
        ),
    }


def build_zitingjing_source_variants(
    *,
    results: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """返回可直接合入 pan_v2.source_variants 的根容器。"""
    return {"zitingjing": build_zitingjing_p1_sources(results=results)}
