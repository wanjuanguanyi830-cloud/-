"""C13 legacy flat schema 迁移审计。

只做 schema/迁移状态统计，不计算太乙结果。
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable

from .legacy_schema import replacement_path_for_legacy
from .unported_catalog import unported_catalog_report
from .pan_adapter import extract_legacy_snapshot_facts
from .pan_v2 import validate_pan_v2

AUDIT_VERSION = "taiyi-c13-legacy-audit-v1"

_REPLACEMENT_ORDER = {
    "source_variants.volume9.ehui_limit.legacy_replacement": 16,
    "source_variants.volume9.governance_change.legacy_replacement": 17,
    "source_variants.wuyun_wuyin.wuyun_liuqi.legacy_replacement": 14,
    "source_variants.wuyun_wuyin.wuyin_number.profiles.tongzong_volume3": 15,
    "cycles.limits.yangjiu": -2,
    "cycles.limits.bailiu": -1,
    "source_variants.patterns.profiles": 0,
    "source_variants.military.three_doors.profiles": 1,
    "source_variants.military.five_generals.profiles": 2,
    "source_variants.military.host_guest_relation.profiles": 3,
    "source_variants.military.weather_bird_support.profiles.jinjing_siku_volume4": 4,
    "source_variants.zitingjing.rules.taiyi_nine_stars.collation_results.tongzong_volume6": 5,
    "source_variants.zitingjing.rules.wenchang_nine_stars.collation_results.tongzong_volume6": 6,
    "source_variants.zitingjing.rules.wenchang_changes.collation_results.tongzong_volume6": 7,
    "source_variants.zitingjing.rules.shiji_changes.collation_results.tongzong_volume6": 8,
    "source_variants.zitingjing.rules.three_banners.collation_results.tongzong_volume10": 9,
    "source_variants.zitingjing.rules.nine_palace_nobles.collation_results.tongzong_volume10": 10,
    "source_variants.military_derived.tongzong_volume15.payload": 20,
    "source_variants.military_derived.tongzong_volume17.payload": 21,
    "analysis.military": 10,
    "analysis.seven_methods": 11,
    "analysis.eight_divinations": 12,
    "modern.game_theory": 13,
}


def _path_has_nonempty_dict(root: dict[str, Any], dotted_path: str) -> bool:
    value: Any = root
    for part in dotted_path.split("."):
        if not isinstance(value, dict) or part not in value:
            return False
        value = value[part]
    return isinstance(value, dict) and bool(value)


def _replacement_gaps(snapshot: dict[str, Any]) -> list[str]:
    v2 = snapshot.get("v2")
    if not isinstance(v2, dict):
        return ["v2"]

    gaps = {
        path
        for key in snapshot
        if (path := replacement_path_for_legacy(key)) is not None
        and not _path_has_nonempty_dict(v2, path)
    }
    return sorted(gaps, key=lambda path: (_REPLACEMENT_ORDER.get(path, 99), path))


def audit_legacy_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """审计一个 legacy/pan snapshot 的 v2 迁移状态。"""
    if not isinstance(snapshot, dict):
        raise TypeError("snapshot须为dict")

    facts = extract_legacy_snapshot_facts(snapshot)
    legacy_keys = sorted(key for key in snapshot if key != "v2")
    total = len(legacy_keys)
    consumed = facts["consumed_legacy_keys"]
    quarantined = facts["quarantined_legacy_keys"]
    unported = facts["unported_legacy_keys"]

    v2 = snapshot.get("v2")
    v2_present = isinstance(v2, dict)
    v2_validation = validate_pan_v2(v2) if v2_present else {
        "valid": False,
        "errors": ["缺v2"],
        "warnings": [],
        "schema_version": None,
    }
    gaps = _replacement_gaps(snapshot)
    unported_catalog = unported_catalog_report(unported)

    if not v2_present:
        status = "legacy_only"
    elif not v2_validation["valid"]:
        status = "v2_invalid"
    elif gaps:
        status = "v2_partial_replacements"
    elif unported:
        status = "v2_core_ready_with_unported_legacy"
    else:
        status = "v2_core_ready"

    def ratio(n: int) -> float:
        return round(n / total, 4) if total else 1.0

    return {
        "canonical": AUDIT_VERSION,
        "derived_migration_metadata": True,
        "status": status,
        "legacy_key_count": total,
        "migrated_fact_key_count": len(consumed),
        "quarantined_key_count": len(quarantined),
        "unported_key_count": len(unported),
        "migrated_fact_rate": ratio(len(consumed)),
        "quarantine_rate": ratio(len(quarantined)),
        "unported_rate": ratio(len(unported)),
        "migrated_fact_keys": consumed,
        "quarantined_legacy_keys": quarantined,
        "unported_legacy_keys": unported,
        "unported_layer_counts": unported_catalog["layer_counts"],
        "unported_priority_counts": unported_catalog["priority_counts"],
        "next_migration_candidates": unported_catalog["next_migration_candidates"],
        "v2_present": v2_present,
        "v2_valid": bool(v2_validation["valid"]),
        "v2_errors": list(v2_validation.get("errors", [])),
        "v2_warnings": list(v2_validation.get("warnings", [])),
        "replacement_gaps": gaps,
        "ready_for_v2_core_consumption": (
            v2_present and bool(v2_validation["valid"]) and not gaps
        ),
        "policy": (
            "迁移统计只描述schema状态；quarantined字段必须由结构化C8/C9/D8/T7结果替代，"
            "不得把旧prose重新提升为canonical。"
        ),
    }


def audit_snapshot_collection(snapshots: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """汇总多份 snapshot 的迁移状态与字段频率。"""
    reports = [audit_legacy_snapshot(snapshot) for snapshot in snapshots]
    status_counts = Counter(report["status"] for report in reports)
    migrated = Counter()
    quarantined = Counter()
    unported = Counter()
    gaps = Counter()
    unported_layers = Counter()
    unported_priorities = Counter()

    for report in reports:
        migrated.update(report["migrated_fact_keys"])
        quarantined.update(report["quarantined_legacy_keys"])
        unported.update(report["unported_legacy_keys"])
        gaps.update(report["replacement_gaps"])
        unported_layers.update(report["unported_layer_counts"])
        unported_priorities.update(report["unported_priority_counts"])

    n = len(reports)

    def avg(field: str) -> float:
        if not reports:
            return 0.0
        return round(sum(float(report[field]) for report in reports) / n, 4)

    return {
        "canonical": AUDIT_VERSION,
        "derived_migration_metadata": True,
        "snapshot_count": n,
        "status_counts": dict(sorted(status_counts.items())),
        "ready_for_v2_core_count": sum(
            1 for report in reports if report["ready_for_v2_core_consumption"]
        ),
        "average_migrated_fact_rate": avg("migrated_fact_rate"),
        "average_quarantine_rate": avg("quarantine_rate"),
        "average_unported_rate": avg("unported_rate"),
        "migrated_field_frequency": dict(sorted(migrated.items())),
        "quarantined_field_frequency": dict(sorted(quarantined.items())),
        "unported_field_frequency": dict(sorted(unported.items())),
        "replacement_gap_frequency": dict(sorted(gaps.items())),
        "unported_layer_frequency": dict(sorted(unported_layers.items())),
        "unported_priority_frequency": dict(sorted(unported_priorities.items())),
        "reports": reports,
    }
