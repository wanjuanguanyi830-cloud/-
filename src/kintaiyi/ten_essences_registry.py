"""C52 十精太乙来源注册表。

目标：先锁来源、卷次、公式骨架与旧实现风险，再逐项迁移 runtime。
本层不把旧 config.py 函数提升为 canonical。

当前重点字段：
帝符、太尊、飞鸟、三风、五风、八风。

注意：
- 十精“飞鸟”是推步所得的十精神位；
- J4M-11 的“飞鸟”是外部真实观测事件；
两者同名但绝非同一输入层。
"""

from __future__ import annotations

import copy
from typing import Any

C52_VERSION = "taiyi-c52-ten-essences-source-registry-v1"

TEN_ESSENCE_ORDER = (
    "天皇",
    "帝符",
    "天时",
    "太尊",
    "飞鸟",
    "五行",
    "八风",
    "五风",
    "三风",
    "太乙数",
)

FOCUS_FIELDS = ("帝符", "太尊", "飞鸟", "三风", "五风", "八风")

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "section_position": "明十精太乙所至",
    "section_cloud": "明十精太乙云气所主术",
    "volume_witnesses": {
        "cadal_online": 20,
        "ngj_or_project_legacy": 18,
    },
    "volume_status": "witness_volume_variant",
    "layer_policy": (
        "十精位置推步与十精云气断事分层；卷十八/卷二十只视作见证卷次差异，"
        "不得因此复制算法。"
    ),
}

# 只记录当前直接文本足以锁定的公式骨架；
# route_status != direct_complete 时禁止据此生成 canonical runtime。
SOURCE_RULES = {
    "帝符": {
        "ordinal": 2,
        "identity": "天节之使",
        "big_cycle": 200,
        "small_cycle": 20,
        "route": {
            "start": "阴主",
            "mode": "顺行十六宫间之神",
            "repeat_on": ["地主", "高丛", "大威", "太簇", "坎", "离", "震", "兑"],
            "status": "direct_complete_structure",
        },
        "rejected_surplus_formula": {
            "value": 70,
            "source_comment": "太乙诸家经旨并无所加之术，今止依古法而求之",
            "apply": False,
        },
        "legacy_function": "config.kingfu",
        "legacy_aliases": ["地符"],
        "legacy_canonical_equivalent": False,
        "legacy_issue": (
            "旧函数主要按积年mod20旋转，未表达大周200、十六神重留结构；"
            "yunqi.py又以“地符”作为key，不能静默替代正文“帝符”。"
        ),
    },
    "太尊": {
        "ordinal": 4,
        "identity": "黄星之长",
        "big_cycle": 40,
        "small_cycle": 4,
        "route": {
            "source_text": "命起至大簇大威高丛逆行八六四四正之宫",
            "status": "text_requires_collation",
            "canonical_route": None,
        },
        "legacy_function": "config.taijun",
        "legacy_canonical_equivalent": False,
        "legacy_issue": (
            "旧函数仅以mod4映子午卯酉；当前正文路线OCR仍需校勘，"
            "不能据旧函数反推canonical路线。"
        ),
    },
    "飞鸟": {
        "ordinal": 5,
        "identity": "弋七星之使、朱雀之体",
        "big_cycle": 90,
        "small_cycle": 9,
        "route": {
            "source_text": "命起一宫阴德，顺行九宫",
            "status": "direct_text_route_start_needs_layout_check",
            "canonical_route": None,
        },
        "rejected_surplus_formula": {
            "value": 3,
            "source_comment": "古法皆无所加，故不取用",
            "apply": False,
        },
        "legacy_function": "config.flybird",
        "legacy_canonical_equivalent": False,
        "legacy_issue": (
            "旧函数使用mod8与八宫序，和正文大周90/小周9并不等价。"
        ),
        "same_name_boundary": {
            "j4m11_external_bird_observation": False,
            "policy": (
                "十精飞鸟是推步神位；J4M-11飞鸟是外部观测。"
                "不得用十精宫位伪造军事飞鸟观测。"
            ),
        },
    },
    "八风": {
        "ordinal": 7,
        "identity": "毕星之使",
        "big_cycle": 90,
        "small_cycle": 9,
        "route": {
            "source_text": "命起大威二宫，次和德三宫，顺行九宫",
            "status": "direct_structure_route_requires_full_sequence_expansion",
            "canonical_route": None,
        },
        "rejected_surplus_formula": {
            "year": 4,
            "month_day_hour": 2,
            "source_comment": "古法不载，故不取用",
            "apply": False,
        },
        "legacy_function": "config.eightwind",
        "legacy_canonical_equivalent": False,
        "legacy_issue": (
            "旧函数保留mod9近似路径，但未建立正文起点/顺行与古法不取盈差的来源契约。"
        ),
    },
    "五风": {
        "ordinal": 8,
        "identity": "箕星之使",
        "big_cycle": 90,
        "small_cycle": 9,
        "route": {
            "sequence": [1, 3, 5, 7, 9, 2, 4, 6, 8],
            "mode": "先阳后阴次第",
            "status": "direct_complete_sequence",
        },
        "rejected_surplus_formula": {
            "year": 3,
            "day": 6,
            "source_comment": "古法不载，故不取用",
            "apply": False,
        },
        "legacy_function": "config.fivewind",
        "legacy_canonical_equivalent": False,
        "legacy_issue": (
            "旧函数以mod29为第一层周期，与正文大周90/小周9直接冲突；"
            "不可迁为canonical。"
        ),
    },
    "三风": {
        "ordinal": 9,
        "identity": "心星之使",
        "big_cycle": 90,
        "small_cycle": 9,
        "route": {
            "source_sequence": [3, 7, 2, 6, 1, 5, 4, 8],
            "status": "source_sequence_incomplete_or_ocr_requires_collation",
            "canonical_route": None,
            "note": "当前见证只显八项，而小周为9；不得自行补第九项。",
        },
        "rejected_surplus_formula": {
            "year": 8,
            "month": 5,
            "day": 2,
            "hour": 5,
            "source_comment": "古法无此，故不取用",
            "apply": False,
        },
        "legacy_function": "config.threewind",
        "legacy_canonical_equivalent": False,
        "legacy_issue": (
            "旧函数虽用mod9，但直接采用八项序列并有余0特殊返回，"
            "在第九项来源未校清前不得视为canonical。"
        ),
    },
}

CLOUD_LAYER_BOUNDARY = {
    "same_source_family": True,
    "same_formula_layer": False,
    "position_layer": "明十精太乙所至",
    "cloud_layer": "明十精太乙云气所主术",
    "policy": (
        "位置公式只回答十精所在；风云雨雾断事必须另建观察/合会层，"
        "不得在位置runtime里自动生成天气断语。"
    ),
}


def ten_essence_source_registry() -> dict[str, Any]:
    """返回 C52 来源注册表；不执行十精推步。"""
    return {
        "schema_version": "1.0",
        "canonical": C52_VERSION,
        "source_profile": "tongzong_ten_essences_source_registry",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "ten_essence_order": list(TEN_ESSENCE_ORDER),
        "focus_fields": list(FOCUS_FIELDS),
        "rules": copy.deepcopy(SOURCE_RULES),
        "cloud_layer_boundary": copy.deepcopy(CLOUD_LAYER_BOUNDARY),
        "runtime_formula_applied": False,
        "policy": (
            "C52只做来源与公式骨架注册。只有route_status足够、边界测试完成后，"
            "各十精才可逐项建立canonical runtime。旧config函数仅作审计参考。"
        ),
    }


def ten_essence_focus(name: str) -> dict[str, Any]:
    if name not in SOURCE_RULES:
        raise ValueError("C52当前只开放帝符/太尊/飞鸟/三风/五风/八风")
    return {
        "canonical": C52_VERSION,
        "name": name,
        "source_profile": "tongzong_ten_essences_source_registry",
        "rule": copy.deepcopy(SOURCE_RULES[name]),
        "cloud_layer_boundary": copy.deepcopy(CLOUD_LAYER_BOUNDARY),
    }
