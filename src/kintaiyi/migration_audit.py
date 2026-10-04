"""C13 legacy flat schema 迁移审计。

只做 schema/迁移状态统计，不计算太乙结果。
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable

from .pan_adapter import extract_legacy_snapshot_facts
from .pan_v2 import validate_pan_v2

AUDIT_VERSION = "taiyi-c13-legacy-audit-v1"

_OLD_MILITARY = {"軍事戰略", "军事战略"}
_OLD_GAME_THEORY = {"運籌博弈分析", "运筹博弈分析"}
_OLD_SEVEN_METHODS = {
    "推雷公入水", "推臨津問道", "推临津问道", "推獅子反擲", "推狮子反掷",
    "推白雲捲空", "推白云卷空", "推猛虎相拒", "推白龍得雲", "推白龙得云",
    "推回軍無言", "推回军无言",
}
_OLD_EIGHT_DIVINATIONS = {
    "推多少以占勝負", "推多少以占胜负",
    "推孤單以占成敗", "推孤单以占成败",
    "推陰陽以占厄會", "推阴阳以占厄会",
}


def _nonempty_dict(value: Any) -> bool:
    return isinstance(value, dict) and bool(value)


def _replacement_gaps(snapshot: dict[str, Any]) -> list[str]:
    v2 = snapshot.get("v2")
    if not isinstance(v2, dict):
        return ["v2"]

    analysis = v2.get("analysis") if isinstance(v2.get("analysis"), dict) else {}
    modern = v2.get("modern") if isinstance(v2.get("modern"), dict) else {}

    gaps: list[str] = []
    keys = set(snapshot)

    if keys & _OLD_MILITARY and not _nonempty_dict(analysis.get("military")):
        gaps.append("analysis.military")
    if keys & _OLD_SEVEN_METHODS and not _nonempty_dict(analysis.get("seven_methods")):
        gaps.append("analysis.seven_methods")
    if keys & _OLD_EIGHT_DIVINATIONS and not _nonempty_dict(analysis.get("eight_divinations")):
        gaps.append("analysis.eight_divinations")
    if keys & _OLD_GAME_THEORY and not _nonempty_dict(modern.get("game_theory")):
        gaps.append("modern.game_theory")

    return gaps


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

    for report in reports:
        migrated.update(report["migrated_fact_keys"])
        quarantined.update(report["quarantined_legacy_keys"])
        unported.update(report["unported_legacy_keys"])
        gaps.update(report["replacement_gaps"])

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
        "reports": reports,
    }
