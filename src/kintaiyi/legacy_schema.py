"""C14 legacy flat schema 单一字段策略表。

C12 adapter 与 C13 audit 都应从这里读取字段分类，避免各维护一份名单。
本模块不计算任何太乙结果。
"""

from __future__ import annotations

from typing import Any

from .unported_catalog import catalog_unported_field

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

SECTOR_GENERAL_FIELDS = {
    "天乙": "tianyi",
    "地乙": "diyi",
    "四神": "four_spirits",
    "直符": "zhifu",
    "合神": "hegod",
    "計神": "jigod",
    "计神": "jigod",
}

SIXTEEN_PALACE_FIELDS = {
    "十六宮分佈": "sixteen_palaces",
    "十六宫分布": "sixteen_palaces",
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
    "厄會行限": "source_variants.volume9.ehui_limit.legacy_replacement",
    "厄会行限": "source_variants.volume9.ehui_limit.legacy_replacement",
    "國政章易": "source_variants.volume9.governance_change.legacy_replacement",
    "国政章易": "source_variants.volume9.governance_change.legacy_replacement",
    "歲中災發": "source_variants.volume9.disaster_timing.legacy_replacement",
    "岁中灾发": "source_variants.volume9.disaster_timing.legacy_replacement",
    "五運六氣": "source_variants.wuyun_wuyin.wuyun_liuqi.legacy_replacement",
    "五运六气": "source_variants.wuyun_wuyin.wuyun_liuqi.legacy_replacement",
    "五音之數": "source_variants.wuyun_wuyin.wuyin_number.profiles.tongzong_volume3",
    "五音之数": "source_variants.wuyun_wuyin.wuyin_number.profiles.tongzong_volume3",
    "陽九": "cycles.limits.yangjiu",
    "阳九": "cycles.limits.yangjiu",
    "百六": "cycles.limits.bailiu",
    "軍事應用": "source_variants.military_derived.tongzong_volume15.payload",
    "军事应用": "source_variants.military_derived.tongzong_volume15.payload",
    "軍事占斷": "source_variants.military_derived.tongzong_volume17.payload",
    "军事占断": "source_variants.military_derived.tongzong_volume17.payload",
    "太乙九星": "source_variants.zitingjing.rules.taiyi_nine_stars.collation_results.tongzong_volume6",
    "文昌九星": "source_variants.zitingjing.rules.wenchang_nine_stars.collation_results.tongzong_volume6",
    "文昌變化": "source_variants.zitingjing.rules.wenchang_changes.collation_results.tongzong_volume6",
    "文昌变化": "source_variants.zitingjing.rules.wenchang_changes.collation_results.tongzong_volume6",
    "始擊變化": "source_variants.zitingjing.rules.shiji_changes.collation_results.tongzong_volume6",
    "始击变化": "source_variants.zitingjing.rules.shiji_changes.collation_results.tongzong_volume6",
    "三旗行宮": "source_variants.zitingjing.rules.three_banners.collation_results.tongzong_volume10",
    "三旗行宫": "source_variants.zitingjing.rules.three_banners.collation_results.tongzong_volume10",
    "九宮貴神": "source_variants.zitingjing.rules.nine_palace_nobles.collation_results.tongzong_volume10",
    "九宫贵神": "source_variants.zitingjing.rules.nine_palace_nobles.collation_results.tongzong_volume10",
    "釋格局": "source_variants.patterns.profiles",
    "释格局": "source_variants.patterns.profiles",
    "推三門具不具": "source_variants.military.three_doors.profiles",
    "推三门具不具": "source_variants.military.three_doors.profiles",
    "推五將發不發": "source_variants.military.five_generals.profiles",
    "推五将发不发": "source_variants.military.five_generals.profiles",
    "推主客相闗法": "source_variants.military.host_guest_relation.profiles",
    "推主客相關法": "source_variants.military.host_guest_relation.profiles",
    "推主客相关法": "source_variants.military.host_guest_relation.profiles",
    "推太乙風雲飛鳥助戰法": "source_variants.military.weather_bird_support.profiles.jinjing_siku_volume4",
    "推太乙风云飞鸟助战法": "source_variants.military.weather_bird_support.profiles.jinjing_siku_volume4",
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
    targets.update({key: f"board.generals.{value}" for key, value in SECTOR_GENERAL_FIELDS.items()})
    targets.update({key: f"board.{value}" for key, value in SIXTEEN_PALACE_FIELDS.items()})
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
    catalog = catalog_unported_field(key)
    return {
        "policy_version": LEGACY_SCHEMA_POLICY_VERSION,
        "field": key,
        "status": "unported",
        "target": None,
        "replacement": None,
        "candidate_layer": catalog["layer"],
        "priority": catalog["priority"],
        "source_scope": catalog["source_scope"],
        "migration_action": catalog["action"],
        "migrate_whole": catalog["migrate_whole"],
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
