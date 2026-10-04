"""C14 legacy flat schema 单一字段策略表。

C12 adapter 与 C13 audit 都应从这里读取字段分类，避免各维护一份名单。
本模块不计算任何太乙结果。
"""

from __future__ import annotations

from typing import Any

LEGACY_SCHEMA_POLICY_VERSION = "taiyi-c14-legacy-schema-policy-v1"

META_MAP = {
    "太乙計": "calculation_style",
    "太乙计": "calculation_style",
    "太乙公式類別": "accumulation_method",
    "太乙公式类别": "accumulation_method",
    "紀元": "epoch",
    "纪元": "epoch",
    "局式": "layout",
    "五子元局": "five_yuan_layout",
}

CALENDAR_MAP = {
    "公元日期": "gregorian",
    "干支": "ganzhi",
    "農曆": "lunar",
    "农历": "lunar",
    "年號": "reign_title",
    "年号": "reign_title",
    "太歲": "year_branch",
    "太岁": "year_branch",
}

SIMPLE_BOARD_FACTS = {
    "太乙落宮": ("taiyi", "palace"),
    "太乙落宫": ("taiyi", "palace"),
    "太乙": ("taiyi", "sector"),
}

GENERAL_FIELDS = {
    "主將": "home_general",
    "主将": "home_general",
    "主參": "home_vassal",
    "主参": "home_vassal",
    "客將": "away_general",
    "客将": "away_general",
    "客參": "away_vassal",
    "客参": "away_vassal",
}

CALC_FIELDS = {
    "主算": "home",
    "客算": "away",
    "定算": "settled",
}

CYCLE_FIELDS = {
    "君基": ("three_bases", "ruler"),
    "臣基": ("three_bases", "minister"),
    "民基": ("three_bases", "people"),
    "五福": ("five_blessings", "legacy_value"),
    "大游": ("big_wander", "legacy_value"),
    "大遊": ("big_wander", "legacy_value"),
    "小游": ("small_wander", "legacy_value"),
    "小遊": ("small_wander", "legacy_value"),
}

DOOR_FIELDS = {
    "八門值事": "duty",
    "八门值事": "duty",
    "八門分佈": "distribution",
    "八门分布": "distribution",
}

EYE_FIELDS = {
    "文昌": "board.eyes.skyeyes",
    "始擊": "board.eyes.shiji",
    "始击": "board.eyes.shiji",
    "定目": "board.eyes.settled_eye",
}

# 旧风险字段 → 新结构必须存在的替代路径。
QUARANTINE_REPLACEMENTS = {
    "軍事戰略": "analysis.military",
    "军事战略": "analysis.military",
    "運籌博弈分析": "modern.game_theory",
    "运筹博弈分析": "modern.game_theory",
    "推雷公入水": "analysis.seven_methods",
    "推臨津問道": "analysis.seven_methods",
    "推临津问道": "analysis.seven_methods",
    "推獅子反擲": "analysis.seven_methods",
    "推狮子反掷": "analysis.seven_methods",
    "推白雲捲空": "analysis.seven_methods",
    "推白云卷空": "analysis.seven_methods",
    "推猛虎相拒": "analysis.seven_methods",
    "推白龍得雲": "analysis.seven_methods",
    "推白龙得云": "analysis.seven_methods",
    "推回軍無言": "analysis.seven_methods",
    "推回军无言": "analysis.seven_methods",
    "推多少以占勝負": "analysis.eight_divinations",
    "推多少以占胜负": "analysis.eight_divinations",
    "推孤單以占成敗": "analysis.eight_divinations",
    "推孤单以占成败": "analysis.eight_divinations",
    "推陰陽以占厄會": "analysis.eight_divinations",
    "推阴阳以占厄会": "analysis.eight_divinations",
}

QUARANTINED_LEGACY_KEYS = frozenset(QUARANTINE_REPLACEMENTS)


def _migrated_targets() -> dict[str, str]:
    targets: dict[str, str] = {}
    targets.update({key: f"meta.{value}" for key, value in META_MAP.items()})
    targets.update({key: f"calendar.{value}" for key, value in CALENDAR_MAP.items()})
    targets.update({
        key: f"board.{section}.{field}"
        for key, (section, field) in SIMPLE_BOARD_FACTS.items()
    })
    targets.update({key: f"board.calculations.{value}" for key, value in CALC_FIELDS.items()})
    targets.update({key: f"board.generals.{value}" for key, value in GENERAL_FIELDS.items()})
    targets.update({key: f"board.doors.{value}" for key, value in DOOR_FIELDS.items()})
    targets.update(EYE_FIELDS)
    targets.update({
        key: f"cycles.{section}.{field}"
        for key, (section, field) in CYCLE_FIELDS.items()
    })
    return targets


MIGRATED_FACT_TARGETS = _migrated_targets()
MIGRATED_FACT_KEYS = frozenset(MIGRATED_FACT_TARGETS)


def replacement_path_for_legacy(key: str) -> str | None:
    return QUARANTINE_REPLACEMENTS.get(key)


def classify_legacy_field(key: str) -> dict[str, Any]:
    """返回一个旧顶层字段的迁移策略。"""
    if key == "v2":
        return {
            "policy_version": LEGACY_SCHEMA_POLICY_VERSION,
            "field": key,
            "status": "embedded_v2",
            "target": "v2",
            "replacement": None,
        }
    if key in MIGRATED_FACT_TARGETS:
        return {
            "policy_version": LEGACY_SCHEMA_POLICY_VERSION,
            "field": key,
            "status": "migrated_fact",
            "target": MIGRATED_FACT_TARGETS[key],
            "replacement": None,
        }
    if key in QUARANTINE_REPLACEMENTS:
        return {
            "policy_version": LEGACY_SCHEMA_POLICY_VERSION,
            "field": key,
            "status": "quarantined",
            "target": "compat.quarantined_legacy_keys",
            "replacement": QUARANTINE_REPLACEMENTS[key],
        }
    return {
        "policy_version": LEGACY_SCHEMA_POLICY_VERSION,
        "field": key,
        "status": "unported",
        "target": None,
        "replacement": None,
    }


def legacy_field_manifest(snapshot: dict[str, Any]) -> dict[str, Any]:
    """逐字段输出迁移策略清单；不读取或解释字段值。"""
    if not isinstance(snapshot, dict):
        raise TypeError("snapshot须为dict")
    fields = [classify_legacy_field(key) for key in sorted(snapshot)]
    counts = {"migrated_fact": 0, "quarantined": 0, "unported": 0, "embedded_v2": 0}
    for item in fields:
        counts[item["status"]] += 1
    return {
        "canonical": LEGACY_SCHEMA_POLICY_VERSION,
        "derived_migration_metadata": True,
        "field_count": len(fields),
        "counts": counts,
        "fields": fields,
    }
