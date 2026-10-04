"""C52 太乙十精来源注册表。

本批只确认：
- 十精完整名单与次序；
- 各自直接见证的小周数；
- 卷十八/卷二十编次异文；
- 旧实现的名称/周期冲突。

不在 C52 迁移十精位置公式，也不计算十精云气断语。
"""

from __future__ import annotations

import copy
from typing import Any

C52_VERSION = "taiyi-c52-ten-essences-source-registry-v1"

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "witness_volumes": [18, 20],
    "volume_status": "witness_volume_variant",
    "sections": ["十精太乙所主", "十精太乙云气所主"],
    "independent_collation": [
        {
            "work": "武经总要",
            "role": "independent_early_collation",
            "evidence": "十精完整次序及小周法",
        },
        {
            "work": "太白兵备统宗宝鉴",
            "role": "important_collation",
            "evidence": "十精阴阳起宫、顺逆与宫序",
        },
    ],
}

TEN_ESSENCES = (
    {
        "index": 1,
        "name": "天皇",
        "small_cycle": 20,
        "kind": "position",
        "formula_status": "pending_source_formula_audit",
    },
    {
        "index": 2,
        "name": "帝符",
        "small_cycle": 20,
        "kind": "position",
        "formula_status": "pending_source_formula_audit",
    },
    {
        "index": 3,
        "name": "天时",
        "small_cycle": 12,
        "kind": "position",
        "formula_status": "pending_source_formula_audit",
    },
    {
        "index": 4,
        "name": "太尊",
        "small_cycle": 4,
        "kind": "position",
        "formula_status": "implemented_c53",
    },
    {
        "index": 5,
        "name": "飞鸟",
        "small_cycle": 9,
        "kind": "position",
        "formula_status": "implemented_c53",
    },
    {
        "index": 6,
        "name": "五行",
        "small_cycle": 5,
        "kind": "position",
        "formula_status": "pending_source_formula_audit",
    },
    {
        "index": 7,
        "name": "八风",
        "small_cycle": 9,
        "kind": "position",
        "formula_status": "implemented_c53",
    },
    {
        "index": 8,
        "name": "五风",
        "small_cycle": 9,
        "kind": "position",
        "formula_status": "implemented_c53",
    },
    {
        "index": 9,
        "name": "三风",
        "small_cycle": 9,
        "kind": "position",
        "formula_status": "implemented_c53",
    },
    {
        "index": 10,
        "name": "太乙数",
        "small_cycle": 72,
        "kind": "number",
        "formula_status": "pending_source_formula_audit",
    },
)


FOCUS_FORMULA_SKELETONS = {
    "帝符": {
        "big_cycle": 200,
        "small_cycle": 20,
        "identity": "天节之使",
        "route": {
            "start": "阴主",
            "mode": "顺行十六宫间之神",
            "repeat_on": ["地主", "高丛", "大威", "太簇", "坎", "离", "震", "兑"],
            "status": "direct_complete_structure",
        },
        "surplus_variant": {
            "value": 70,
            "source_status": "explicitly_rejected_by_source",
            "apply": False,
            "note": "诸家经旨并无所加之术，依古法不取。",
        },
        "runtime_formula_ready": False,
        "runtime_blocker": "十六神重留路线尚未写成独立可审计步进器。",
    },
    "太尊": {
        "big_cycle": 40,
        "small_cycle": 4,
        "identity": "黄星之长",
        "route": {
            "tongzong_sequence": [8, 6, 2, 4],
            "wujing_zongyao_sequence": [8, 6, 2, 4],
            "taibai_yang_path": [8, 6, 2, 4],
            "taibai_yin_path": [2, 4, 8, 6],
            "status": "implemented_c53_direct_with_collation",
            "canonical_route_for_tongzong_profile": [8, 6, 2, 4],
        },
        "runtime_formula_ready": True,
        "runtime_rule_id": "C53-TAIZUN",
        "runtime_profile": "tongzong_primary_taibai_collation",
    },
    "飞鸟": {
        "big_cycle": 90,
        "small_cycle": 9,
        "identity": "弋七星之使、朱雀之体",
        "route": {
            "tongzong": "命起一宫，顺行九宫",
            "taibai_bingbei": "阳起乾一、阴起巽九，阳顺阴逆，游行九宫",
            "yang_path": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "yin_path": [9, 8, 7, 6, 5, 4, 3, 2, 1],
            "status": "implemented_c53_tongzong_taibai_profile",
        },
        "surplus_variant": {
            "value": 3,
            "source_status": "explicitly_rejected_by_source",
            "apply": False,
            "note": "古法皆无所加，故不取用。",
        },
        "same_name_boundary": {
            "j4m11_external_bird_observation": False,
            "policy": "十精飞鸟是推步神位；J4M-11飞鸟是外部观测，不得互相代替。",
        },
        "runtime_formula_ready": True,
        "runtime_rule_id": "C53-FLYBIRD",
        "runtime_profile": "tongzong_primary_taibai_collation",
    },
    "八风": {
        "big_cycle": 90,
        "small_cycle": 9,
        "identity": "毕星之使",
        "route": {
            "tongzong_yang_path": [2, 3, 4, 5, 6, 7, 8, 9, 1],
            "wujing_zongyao_yang_path": [2, 3, 4, 5, 6, 7, 8, 9, 1],
            "taibai_yang_path": [2, 3, 4, 5, 6, 7, 8, 9, 1],
            "taibai_yin_path": [8, 7, 6, 5, 4, 3, 2, 1, 9],
            "status": "implemented_c53_direct_with_collation",
        },
        "surplus_variant": {
            "year": 4,
            "month_day_hour": 2,
            "source_status": "explicitly_rejected_by_source",
            "apply": False,
            "note": "古法不载，故不取用。",
        },
        "runtime_formula_ready": True,
        "runtime_rule_id": "C53-EIGHTWIND",
        "runtime_profile": "tongzong_primary_taibai_collation",
    },
    "五风": {
        "big_cycle": 90,
        "small_cycle": 9,
        "identity": "箕星之使",
        "route": {
            "tongzong_sequence": [1, 3, 5, 7, 9, 2, 4, 6, 8],
            "jingyou_sequence": [1, 3, 5, 7, 9, 2, 4, 6, 8],
            "jinjing_volume7_sequence": [1, 3, 5, 7, 9, 2, 4, 6, 8],
            "wujing_zongyao_variant_sequence": [1, 3, 5, 9, 7, 2, 4, 6, 8],
            "wujing_zongyao_parallel_sequence": [1, 3, 5, 7, 9, 2, 4, 6, 8],
            "taibai_yang_path": [1, 3, 5, 7, 9, 2, 4, 6, 8],
            "taibai_yin_path": [9, 7, 5, 3, 1, 8, 6, 4, 2],
            "mode": "先奇后耦；阳顺阴逆",
            "status": "implemented_c53_profile_selection",
            "selected_profile": "tongzong_primary_taibai_collation",
            "canonical_route_for_tongzong_profile": [1, 3, 5, 7, 9, 2, 4, 6, 8],
            "cross_source_canonical_selected": None,
            "unselected_source_variant": "wujing_zongyao_135972468",
            "note": (
                "C53选择统宗主见证，并以景祐、金镜、太白兵备及武经平行转录同序参校；"
                "武经一转录9在7前继续作为异文保留，不宣称跨传本唯一。"
            ),
        },
        "surplus_variant": {
            "year": 3,
            "day": 6,
            "source_status": "explicitly_rejected_by_source",
            "apply": False,
            "note": "古法不载，故不取用。",
        },
        "runtime_formula_ready": True,
        "runtime_rule_id": "C53-FIVEWIND",
        "runtime_profile": "tongzong_primary_taibai_collation",
    },
    "三风": {
        "big_cycle": 90,
        "small_cycle": 9,
        "identity": "心星之使",
        "route": {
            "tongzong_sequence": [3, 7, 2, 6, 1, 5, 9, 4, 8],
            "taibai_yang_path": [3, 7, 2, 6, 1, 5, 9, 4, 8],
            "taibai_yin_path": [7, 3, 8, 4, 9, 5, 1, 6, 2],
            "wujing_zongyao_variant_text": "命起五宫，次七二六一五九四八",
            "status": "implemented_c53_primary_with_preserved_variant",
            "selected_profile": "tongzong_primary_taibai_collation",
            "cross_source_canonical_selected": None,
            "note": "统宗与太白兵备阳序相合；武经总要起五宫读法作为异文保留。",
        },
        "surplus_variant": {
            "year": 8,
            "month": 5,
            "day": 2,
            "hour": 5,
            "source_status": "explicitly_rejected_by_source",
            "apply": False,
            "note": "古法无此，故不取用。",
        },
        "runtime_formula_ready": True,
        "runtime_rule_id": "C53-THREEWIND",
        "runtime_profile": "tongzong_primary_taibai_collation",
    },
}

NAME_ALIASES = {
    "天皇": "天皇",
    "帝符": "帝符",
    "天时": "天时",
    "天時": "天时",
    "太尊": "太尊",
    "飞鸟": "飞鸟",
    "飛鳥": "飞鸟",
    "五行": "五行",
    "八风": "八风",
    "八風": "八风",
    "五风": "五风",
    "五風": "五风",
    "三风": "三风",
    "三風": "三风",
    "太乙数": "太乙数",
    "太乙數": "太乙数",
}

LEGACY_NAME_AUDIT = {
    "地符": {
        "status": "legacy_noncanonical_alias",
        "canonical_name": "帝符",
        "reason": "直接十精正文列“帝符”；旧yunqi._TEN_JING_FN写“地符”。",
    },
    "太岁": {
        "status": "not_a_ten_essence",
        "canonical_name": None,
        "reason": "十精第十项为太乙数，不是太岁。",
    },
    "太歲": {
        "status": "not_a_ten_essence",
        "canonical_name": None,
        "reason": "十精第十项为太乙数，不是太岁。",
    },
}

LEGACY_FORMULA_AUDIT = {
    "config.tian_wang": {
        "essence": "天皇",
        "legacy_cycle": 20,
        "direct_small_cycle": 20,
        "cycle_matches": True,
        "runtime_ready": False,
        "reason": "小周数相合，但阴阳起宫、重留与岁月日时法仍需逐式核对。",
    },
    "config.kingfu": {
        "essence": "帝符",
        "legacy_cycle": 20,
        "direct_small_cycle": 20,
        "cycle_matches": True,
        "runtime_ready": False,
        "reason": "小周数相合，但旧名称链曾写地符，位置算法须独立审计。",
    },
    "config.tian_shi": {
        "essence": "天时",
        "legacy_cycle": 12,
        "direct_small_cycle": 12,
        "cycle_matches": True,
        "runtime_ready": False,
        "reason": "周期相合，起吕申/阴阳起法仍待逐式确认。",
    },
    "config.taijun": {
        "essence": "太尊",
        "legacy_cycle": 4,
        "direct_small_cycle": 4,
        "cycle_matches": True,
        "runtime_ready": False,
        "reason": "周期相合，阴阳起坎/离与逆行四正宫须另建runtime。",
    },
    "config.flybird": {
        "essence": "飞鸟",
        "legacy_cycle": 8,
        "direct_small_cycle": 9,
        "cycle_matches": False,
        "runtime_ready": False,
        "reason": "旧代码按%8；直接正文与武经总要均见小周九。",
    },
    "config.wuxing": {
        "essence": "五行",
        "legacy_cycle": 5,
        "direct_small_cycle": 5,
        "cycle_matches": True,
        "runtime_ready": False,
        "reason": "周期相合，但阴阳起宫与五宫路径仍待逐式核对。",
    },
    "config.eightwind": {
        "essence": "八风",
        "legacy_cycle": 9,
        "direct_small_cycle": 9,
        "cycle_matches": True,
        "runtime_ready": False,
        "reason": "周期相合，阳顺阴逆及起宫仍需独立审计。",
    },
    "config.fivewind": {
        "essence": "五风",
        "legacy_cycle": 29,
        "direct_small_cycle": 9,
        "cycle_matches": False,
        "runtime_ready": False,
        "reason": "旧代码外层%29；直接正文与武经总要均见小周九。",
    },
    "config.threewind": {
        "essence": "三风",
        "legacy_cycle": 9,
        "direct_small_cycle": 9,
        "cycle_matches": True,
        "runtime_ready": False,
        "reason": "周期相合，但旧零余分支与阴阳宫序仍待审计。",
    },
    "yunqi._TEN_JING_FN": {
        "essence": None,
        "legacy_cycle": None,
        "direct_small_cycle": None,
        "cycle_matches": False,
        "runtime_ready": False,
        "reason": "旧名单把帝符写成地符，并以太岁替代第十项太乙数。",
    },
}

CLOUD_OMEN_BOUNDARY = {
    "status": "separate_source_unit",
    "runtime_in_c52": False,
    "reason": (
        "“十精太乙云气所主”包含同宫、阴阳宫、旺相休囚、天气厚薄色象等条件，"
        "不得在名称/周期注册阶段顺带迁入。"
    ),
}

TARGET_POLICY = {
    "suggested_future_target": "source_variants.ten_essences",
    "pan_contract_extended_in_c52": False,
    "legacy_top_level_promoted": False,
    "cycles_root_used": False,
    "reason": "十精是独立古法系统；位置公式未逐项校验前不进入cycles真源。",
}


def canonical_ten_essence_name(
    name: str,
    *,
    allow_legacy_alias: bool = False,
) -> str:
    """正规化繁简名称；旧“地符”只在显式兼容模式下映射帝符。"""
    if name in NAME_ALIASES:
        return NAME_ALIASES[name]
    if allow_legacy_alias and name == "地符":
        return "帝符"
    if name in LEGACY_NAME_AUDIT:
        raise ValueError(f"{name}不是canonical十精名称")
    raise ValueError("未知十精名称")


def ten_essence_record(name: str, *, allow_legacy_alias: bool = False) -> dict[str, Any]:
    canonical = canonical_ten_essence_name(
        name,
        allow_legacy_alias=allow_legacy_alias,
    )
    row = next(item for item in TEN_ESSENCES if item["name"] == canonical)
    return {
        "canonical": C52_VERSION,
        "source_profile": "tongzong_ten_essences_registry",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        **copy.deepcopy(row),
        "formula_skeleton": copy.deepcopy(FOCUS_FORMULA_SKELETONS.get(canonical)),
        "runtime_formula_ready": bool(
            FOCUS_FORMULA_SKELETONS.get(canonical, {}).get(
                "runtime_formula_ready",
                row["formula_status"].startswith("implemented_"),
            )
        ),
    }


def ten_essences_registry() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "canonical": C52_VERSION,
        "rule_id": "C52-TEN-ESSENCES-REGISTRY",
        "source_profile": "tongzong_ten_essences_registry",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "essences": copy.deepcopy(list(TEN_ESSENCES)),
        "legacy_name_audit": copy.deepcopy(LEGACY_NAME_AUDIT),
        "legacy_formula_audit": copy.deepcopy(LEGACY_FORMULA_AUDIT),
        "focus_formula_skeletons": copy.deepcopy(FOCUS_FORMULA_SKELETONS),
        "cloud_omen_boundary": copy.deepcopy(CLOUD_OMEN_BOUNDARY),
        "target_policy": copy.deepcopy(TARGET_POLICY),
        "implemented_position_runtimes": ["飞鸟", "五风", "太尊", "八风", "三风"],
        "pending_position_runtimes": [
            "天皇", "帝符", "天时", "五行"
        ],
        "number_runtime_pending": ["太乙数"],
        "position_runtime_ready": False,
        "position_runtime_ready_semantics": "compat_aggregate_all_positions_ready",
        "all_position_runtime_ready": False,
        "cloud_runtime_ready": False,
        "policy": (
            "C52确认名单、次序、小周数，并登记已核的公式骨架与未决点；"
            "公式骨架不等于runtime就绪。旧位置公式无论周期是否相合都不能自动升为canonical。"
        ),
    }
