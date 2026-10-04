"""C15 unported legacy 字段目录与迁移优先级。

覆盖参考 Taiyi.pan() 当前尚未由 C14 migrated/quarantined 处理的 67 个顶层字段。
这里只定义迁移元数据，不计算古法结果。
"""

from __future__ import annotations

import copy
from collections import Counter
from typing import Any, Iterable

CATALOG_VERSION = "taiyi-c15-unported-catalog-v1"

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

PRIORITY_MEANING = {
    "P0": "先处理：核心盘面或高风险来源边界，避免继续混法。",
    "P1": "高优先：来源较明确的独立规则/高风险军事层。",
    "P2": "中优先：辅助系统、跨卷或仍需补来源核验。",
    "P3": "后处理：综合包装器或现代派生，不应整体升为canonical。",
}


def _entry(layer: str, source_scope: str, priority: str, action: str, *,
           migrate_whole: bool = True, source_confidence: str = "high",
           target_hint: str | None = None, notes: str = "") -> dict[str, Any]:
    return {
        "layer": layer,
        "source_scope": source_scope,
        "priority": priority,
        "action": action,
        "migrate_whole": migrate_whole,
        "source_confidence": source_confidence,
        "target_hint": target_hint,
        "notes": notes,
    }


CATALOG: dict[str, dict[str, Any]] = {}

# 卷一：参考实现明确说明以 Meeus 月球平近点角映射入转；属于现代派生桥接，
# 不可反标为古籍逐字公式。
for key in ("入轉日", "入轉餘", "朓胸定數", "定朔大餘進退", "定朔小餘", "朓胸明細"):
    CATALOG[key] = _entry(
        "derived", "tongzong_volume1_modern_astronomy_bridge", "P3",
        "keep_as_derived_calendar_feature", migrate_whole=False,
        target_hint="modern.calendar_derived",
        notes="参考实现明确含现代天文映射；古法与现代桥接需分层。",
    )

# 阳九/百六大小限：在线统宗见证题卷十；项目旧资料作卷九，保留卷次variant。
for key in ("陽九", "百六"):
    CATALOG[key] = _entry(
        "canonical", "tongzong_volume10_witness_project_volume9_variant", "P1",
        "use_c36_limit_cycles", source_confidence="high",
        target_hint="cycles.limits",
        notes=(
            "C36 已核直接条文：阳九4560/456加130，百六4320/288加2050。"
            "旧pan同名字段只是地支位置，已quarantine，不得直接搬入cycles.limits。"
        ),
    )

# 基础盘面神将事实：结构上应进入 board，但准确卷次仍待统一来源记录。
for key, target in {
    "天乙": "board.generals.tianyi",
    "地乙": "board.generals.diyi",
    "四神": "board.generals.four_spirits",
    "直符": "board.generals.zhifu",
    "合神": "board.generals.hegod",
    "計神": "board.generals.jigod",
}.items():
    CATALOG[key] = _entry(
        "canonical", "taiyi_core_board_exact_volume_pending", "P0",
        "migrate_board_fact", source_confidence="medium", target_hint=target,
        notes="先迁结构事实；来源卷次需单独留证，不从旧断语推导。",
    )

# 这些周期/十精类字段在旧盘中是直接输出，但当前工作规格尚未完成逐项来源校勘。
for key in ("帝符", "太尊", "飛鳥", "三風", "五風", "八風"):
    CATALOG[key] = _entry(
        "pending", "cycle_or_ten-essences_source_pending", "P2",
        "source_verify_before_migration", source_confidence="low",
        target_hint="cycles",
        notes="不得仅凭旧函数名决定卷次或canonical位置。",
    )

CATALOG["金函玉鏡"] = _entry(
    "source_variant", "auxiliary_jinhan_yujing_system", "P3",
    "keep_separate_source_profile", migrate_whole=False,
    source_confidence="medium", target_hint="source_variants",
    notes="辅助体系，不并入太乙核心canonical。",
)

for key in (
    "二十八宿值日", "太歲二十八宿", "太歲值宿斷事", "始擊二十八宿",
    "始擊值宿斷事", "始擊加臨二十八舍所主", "十天干歲始擊落宮預測",
):
    CATALOG[key] = _entry(
        "source_variant", "auxiliary_twenty_eight_mansions", "P2",
        "separate_auxiliary_profile", source_confidence="medium",
        target_hint="source_variants.twenty_eight_mansions",
        notes="辅助星宿层；不能因出现在pan顶层就当作太乙核心公式。",
    )

CATALOG["十六宮分佈"] = _entry(
    "canonical", "tongzong_volume2", "P0", "migrate_board_structure",
    target_hint="board.sixteen_palaces",
    notes="参考pan注释明确《太乙统宗宝鉴》卷二。",
)

CATALOG["八宮旺衰"] = _entry(
    "derived", "jieqi_environment_projection", "P2",
    "keep_environment_feature_derived", target_hint="modern.environment",
    notes="旧实现由节气旺衰模块生成；不要冒充太乙盘面原始事实。",
)

CATALOG["推太乙當時法"] = _entry(
    "pending", "source_pending", "P2", "source_verify_before_migration",
    source_confidence="low", target_hint="analysis.rules",
)

# 与当前 J4M / C8 已存在明确来源边界冲突，必须先拆 source profile。
for key, hint in {
    "推三門具不具": "analysis.military.three_doors",
    "推五將發不發": "analysis.military.five_generals",
    "推主客相闗法": "analysis.military.host_guest_relation",
}.items():
    CATALOG[key] = _entry(
        "source_variant", "jinjing_v4_vs_tongzong_military", "P0",
        "split_source_profiles_before_promotion", migrate_whole=False,
        target_hint=hint,
        notes="旧flat结果不得静默覆盖J4M与C8/Tongzong来源差异。",
    )

for key in (
    "明天子巡狩之期術", "明君基太乙所主術", "明臣基太乙所主術",
    "明民基太乙所主術", "明五福太乙所主術", "明五福吉算所主術",
    "明天乙太乙所主術", "明地乙太乙所主術", "明值符太乙所主術",
):
    CATALOG[key] = _entry(
        "pending", "source_pending", "P2", "source_verify_before_migration",
        source_confidence="low", target_hint="analysis.rules",
        notes="旧pan无卷次注释；需先建source record。",
    )

CATALOG["推太乙風雲飛鳥助戰法"] = _entry(
    "source_variant", "jinjing_siku_volume4_J4M-11_vs_legacy_flybird_wl", "P1",
    "use_structured_j4m11_observation_profile", migrate_whole=False,
    source_confidence="high",
    target_hint="source_variants.military.weather_bird_support",
    notes=(
        "J4M-11 已有完整 source-specific runtime，并要求显式外部风云飞鸟观测。"
        "旧 flybird_wl 仅从盘内飞鸟位置生成断语，已降为 legacy quarantine，"
        "不得再作为未迁移公式候选。"
    ),
)

CATALOG["釋格局"] = _entry(
    "source_variant", "tongzong_volume4_vs_jinjing_geju", "P0",
    "split_source_profiles_before_promotion", migrate_whole=False,
    target_hint="analysis.patterns",
    notes="目标仓库已有金镜格局层；统宗卷四必须保留独立profile。",
)

for key in ("三旗行宮", "九宮貴神"):
    CATALOG[key] = _entry(
        "source_variant",
        "zitingjing_project_attribution_unverified_vs_tongzong_volume10_direct",
        "P1",
        "verify_primary_attribution_then_select_profile",
        migrate_whole=False,
        source_confidence="medium",
        target_hint="source_variants.zitingjing",
        notes=(
            "项目曾指定《太乙紫庭经》为主来源目标，但当前已查《太乙紫庭秘诀》"
            "十二卷及附录目录未见同名题目；《太乙统宗宝鉴》卷十有直接可定位文本。"
            "在取得紫庭目录/正文证据前不得把两项标成紫庭canonical。"
        ),
    )

CATALOG["太乙九星"] = _entry(
    "canonical", "zitingjing_direct_primary_tongzong_volume6_collation", "P1",
    "migrate_rule_from_verified_primary_source",
    target_hint="source_variants.zitingjing",
    notes=(
        "《太乙紫庭经》〈释九宫所值九星〉直接正文已定位；"
        "统宗卷六继续作参校，旧 flat 统宗结果只进入 collation_results。"
    ),
)

CATALOG["文昌九星"] = _entry(
    "pending", "zitingjing_catalog_attested_text_pending_tongzong_volume6_collation", "P1",
    "await_primary_text_keep_collation_only", migrate_whole=False,
    source_confidence="medium",
    target_hint="source_variants.zitingjing",
    notes=(
        "目前仅有《太乙紫庭秘诀》目录“附太乙文昌九星值宫术”证据；"
        "正文未取得，10年/30年周期又存在参校冲突。旧 flat 统宗实现只可进入"
        " collation_results，不得升为《太乙紫庭经》primary_result。"
    ),
)

for key in ("五運六氣", "五音之數"):
    CATALOG[key] = _entry(
        "source_variant", "tongzong_volume3_and_volume10", "P1",
        "split_cross_volume_sources", migrate_whole=False,
        target_hint="source_variants.wuyun_wuyin",
        notes="参考pan注释本身标卷三/卷十，不能压成单一来源。",
    )

for key, volume in {
    "卷十二": "tongzong_volume12",
    "卷十三": "tongzong_volume13",
    "卷十四": "tongzong_volume14",
    "卷八": "tongzong_volume8",
    "卷九": "tongzong_volume9",
    "卷十": "tongzong_volume10",
    "卷十八": "tongzong_volume18",
    "卷十一": "tongzong_volume11",
}.items():
    CATALOG[key] = _entry(
        "derived", volume, "P3", "split_composite_wrapper",
        migrate_whole=False, target_hint="derived.volume_composites",
        notes="旧键是综合包装器；内部规则逐条迁移，整个dict不得标canonical。",
    )

CATALOG["軍事應用"] = _entry(
    "derived", "tongzong_volume15", "P1", "split_military_rules",
    migrate_whole=False, target_hint="derived.volume15_military",
    notes="卷十五军事应用必须与C8卷五/J4M卷四隔离。",
)

CATALOG["軍事占斷"] = _entry(
    "derived", "tongzong_volume17", "P1", "split_military_rules",
    migrate_whole=False, target_hint="derived.volume17_military",
    notes="卷十七军事占断不得反写C8/J4M结论。",
)

CATALOG["神將所主"] = _entry(
    "derived", "tongzong_volume2_and_volume7", "P2",
    "split_cross_volume_composite", migrate_whole=False,
    target_hint="derived.spirit_general_subjects",
    notes="参考pan注释明确卷二/卷七混合，必须拆源。",
)

for key in ("文昌變化", "始擊變化"):
    CATALOG[key] = _entry(
        "canonical", "zitingjing_primary_tongzong_volume6_collation", "P1",
        "migrate_rule_from_primary_source",
        target_hint="analysis.zitingjing",
        notes=(
            "主要参考《太乙紫庭经》；旧pan以《太乙统宗宝鉴》卷六注释，"
            "统宗保留为重要参校来源；用于校异、补证与版本比较，但不得静默覆盖《太乙紫庭经》主来源。"
        ),
    )

for key in ("厄會行限", "國政章易", "歲中災發"):
    CATALOG[key] = _entry(
        "canonical", "tongzong_volume9", "P2", "migrate_rule_after_source_record",
        source_confidence="high", target_hint="analysis.volume9",
        notes="参考pan注释明确《太乙统宗宝鉴》卷九。",
    )


REFERENCE_PAN_UNPORTED_FIELDS = frozenset(CATALOG)


def catalog_unported_field(key: str) -> dict[str, Any]:
    """查询C15目录；未知字段保持pending，不猜来源。"""
    item = CATALOG.get(key)
    if item is None:
        item = _entry(
            "pending", "unknown", "P3", "source_verify_before_migration",
            migrate_whole=False, source_confidence="low",
            notes="C15未收录的新字段；先补来源记录。",
        )
    return {
        "catalog_version": CATALOG_VERSION,
        "field": key,
        **copy.deepcopy(item),
    }


def prioritize_unported_fields(fields: Iterable[str]) -> list[dict[str, Any]]:
    """按P0→P3、layer、字段名输出迁移队列。"""
    items = [catalog_unported_field(key) for key in fields]
    return sorted(
        items,
        key=lambda x: (PRIORITY_ORDER.get(x["priority"], 99), x["layer"], x["field"]),
    )


def unported_catalog_report(fields: Iterable[str]) -> dict[str, Any]:
    """汇总一组unported字段的layer/priority分布。"""
    items = prioritize_unported_fields(fields)
    layer_counts = Counter(item["layer"] for item in items)
    priority_counts = Counter(item["priority"] for item in items)
    return {
        "canonical": CATALOG_VERSION,
        "derived_migration_metadata": True,
        "field_count": len(items),
        "layer_counts": dict(sorted(layer_counts.items())),
        "priority_counts": dict(sorted(priority_counts.items())),
        "next_migration_candidates": [
            item for item in items if item["priority"] in ("P0", "P1")
        ],
        "fields": items,
    }
