"""C57 十精太乙云气：显式合会/宫位证据层。

来源：
- 《太乙统宗宝鉴》“明十精太乙所主术”各十精条下合会断语；
- “明十精太乙云气所主术”总括；
- 《武经总要》十精合会作独立早期参校。

边界：
- 不从 C53/C55/C56 落宫结果自动判断“合”；
- 调用方必须显式给出 conjunctions；
- 旺相/非旺相、阴阳宫、宫数也必须显式给出；
- 云色时变、天气厚薄色象另层，不在本函数推断；
- J4M-11 外部飞鸟观测不属于十精飞鸟。
"""

from __future__ import annotations

import copy
from typing import Any

from .ten_essences_source_registry import canonical_ten_essence_name

C57_VERSION = "taiyi-c57-ten-essence-cloud-conjunctions-v1"

ALLOWED_TARGETS = frozenset({
    "太乙", "天目", "天皇", "帝符", "天时", "太尊", "飞鸟",
    "五行", "八风", "五风", "三风", "太乙数",
})

QI_STATES = frozenset({"旺相", "非旺相", "休囚"})
PALACE_YINYANG = frozenset({"阳", "阴"})

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "sections": ["明十精太乙所主术", "明十精太乙云气所主术"],
    "witness_volumes": [18, 20],
    "volume_status": "witness_volume_variant",
    "collation": [
        {
            "work": "武经总要",
            "role": "independent_early_collation",
            "scope": "十精与太乙/诸神合会天气断语",
        }
    ],
    "policy": (
        "主见证与参校只在字义稳定处正规化；"
        "真实异读或OCR不稳处保留variants，不静默选本。"
    ),
}

# 每条规则只在 requires 全部满足时命中。
# effects=None 表示见证异读未决，只返回 witness_variants。
CONJUNCTION_RULES: dict[str, list[dict[str, Any]]] = {
    "天皇": [
        {
            "target": "太乙",
            "effects": ["日晕", "大风"],
            "status": "direct",
        },
        {
            "target": "太乙",
            "qi_state": "旺相",
            "effects": ["风遍天下"],
            "status": "direct",
        },
        {
            "target": "太尊",
            "effects": ["大阴雨", "日月为变"],
            "status": "direct_collated",
        },
        {
            "target": "飞鸟",
            "effects": ["阴雨"],
            "status": "normalized_from_minor_wording_variant",
            "witness_variants": {
                "tongzong": "有阴雨",
                "wujing_zongyao": "小阴雨",
            },
        },
        {
            "target": "天时",
            "effects": None,
            "status": "source_variant_unresolved",
            "witness_variants": {
                "tongzong": "阴昏",
                "wujing_zongyao": "小昏",
            },
        },
        {
            "target": "五风",
            "effects": ["疾风起"],
            "status": "direct",
        },
        {
            "target": "太乙数",
            "effects": ["大风雨"],
            "status": "direct",
        },
    ],
    "帝符": [
        {
            "target": "太乙",
            "effects": ["日晕", "大风"],
            "status": "direct",
        },
        {
            "target": "太乙",
            "qi_state": "旺相",
            "effects": ["小雨", "小阴云", "疾风卒起"],
            "status": "direct",
        },
        {
            "target": "天目",
            "effects": ["小阴疾风", "日月有变"],
            "status": "direct",
        },
    ],
    "天时": [
        {
            "target": "太乙",
            "qi_state": "旺相",
            "effects": ["风云卒起", "或阴雨"],
            "status": "direct",
        },
    ],
    "太尊": [
        {
            "target": "太乙",
            "qi_state": "旺相",
            "effects": ["大阴雨寒"],
            "status": "direct",
        },
        {
            "target": "飞鸟",
            "effects": ["天温", "小雨"],
            "status": "direct_collated",
        },
        {
            "target": "帝符",
            "effects": ["阴雨", "大昏"],
            "status": "direct_collated",
        },
        {
            "target": "天目",
            "effects": ["阴雨"],
            "status": "direct_collated",
        },
    ],
    "飞鸟": [
        {
            "target": "太乙",
            "qi_state": "旺相",
            "effects": ["天星有变"],
            "status": "direct",
        },
        {
            "target": "太乙",
            "qi_state": "非旺相",
            "effects": ["大风"],
            "status": "direct",
        },
        {
            "target": "天时",
            "effects": ["阴风"],
            "status": "direct",
        },
        {
            "target": "三风",
            "effects": ["大风"],
            "status": "direct",
        },
        {
            "target": "五风",
            "effects": ["大风"],
            "status": "direct",
        },
    ],
    "五行": [
        {
            "target": "太乙",
            "qi_state": "旺相",
            "effects": ["暴风", "大寒", "云气昏暗", "或雨"],
            "status": "direct",
        },
        {
            "target": "天目",
            "effects": ["大风", "阴", "日月有变"],
            "status": "direct",
        },
        {
            "target": "八风",
            "effects": ["小阴风雨"],
            "status": "direct",
        },
        {
            "target": "太尊",
            "effects": ["日月变色", "小阴"],
            "status": "direct",
        },
        {
            "target": "帝符",
            "effects": ["风昏", "小阴"],
            "status": "normalized_name_only",
            "witness_variants": {
                "tongzong_online": "地符合",
                "wujing_zongyao": "帝符合",
            },
        },
        {
            "target": "天时",
            "effects": ["大阴昏", "风云起"],
            "status": "direct",
        },
    ],
    "八风": [
        {
            "target": "太乙",
            "qi_state": "旺相",
            "effects": ["云起", "小雨"],
            "status": "direct",
        },
        {
            "target": "太乙",
            "palace_yinyang": "阴",
            "effects": ["雨"],
            "status": "direct",
        },
        {
            "target": "太乙",
            "palace_yinyang": "阳",
            "effects": ["风"],
            "status": "direct",
        },
        {
            "target": "五风",
            "effects": ["阴", "大风", "天昏"],
            "status": "direct",
        },
        {
            "target": "天时",
            "effects": ["阴昏", "日月有变"],
            "status": "direct",
        },
        {
            "target": "天皇",
            "effects": ["大风", "疾阴", "日月有变"],
            "status": "direct",
        },
        {
            "target": "帝符",
            "effects": ["阴雨"],
            "status": "normalized_name_only",
            "witness_variants": {
                "tongzong_online": "地符合",
                "wujing_zongyao": "帝符合",
            },
        },
    ],
    "五风": [
        {
            "target": "太乙",
            "qi_state": "旺相",
            "effects": ["日月有变", "连阴不见天日", "暴风疾雨并作"],
            "status": "direct",
        },
        {
            "target": "太尊",
            "effects": ["小阴雨", "日月有变"],
            "status": "direct",
        },
        {
            "target": "飞鸟",
            "effects": ["疾风"],
            "status": "direct",
        },
        {
            "target": "帝符",
            "effects": ["大风"],
            "status": "direct",
        },
        {
            "target": "天时",
            "effects": ["大风"],
            "status": "direct",
        },
        {
            "target": "天目",
            "effects": ["大阴", "小风", "日月有变"],
            "status": "direct",
        },
    ],
    "三风": [
        {
            "target": "太乙",
            "qi_state": "旺相",
            "effects": ["日月无光", "寒云四起"],
            "status": "direct",
        },
        {
            "target": "天目",
            "effects": ["大阴雨"],
            "status": "direct",
        },
        {
            "target": "天时",
            "effects": None,
            "status": "source_variant_unresolved",
            "witness_variants": {
                "tongzong": "小阴雨",
                "wujing_zongyao": "小阴风",
            },
        },
        {
            "target": "飞鸟",
            "effects": ["疾风阴云", "日月有变"],
            "status": "direct",
        },
        {
            "target": "五风",
            "effects": ["日月有变", "小阴"],
            "status": "direct",
        },
        {
            "target": "太尊",
            "effects": ["小阴雨"],
            "status": "direct",
        },
        {
            "target": "帝符",
            "effects": ["小阴"],
            "status": "direct",
        },
        {
            "target": "天皇",
            "effects": ["天阴", "小风", "日月有变"],
            "status": "direct",
        },
    ],
}

PALACE_RULES = {
    "太尊": {
        8: {"effects": ["日晕"], "status": "direct"},
        6: {"effects": ["阴昏"], "status": "direct"},
        2: {"effects": ["太阴昏寒"], "status": "direct"},
        4: {"effects": ["日晕"], "status": "direct"},
    },
    "飞鸟": {
        9: {"effects": ["日晕"], "status": "direct"},
        6: {"effects": ["日晕"], "status": "direct"},
    },
}

ZHANGLIANG_SUMMARY_VARIANT = {
    "status": "witness_variant_unresolved",
    "tongzong_online_ocr": (
        "帝符、太尊、天时、五风、八风、三风与太乙合，阳宫‘暗’，阴宫雨"
    ),
    "sancai_shiwei_collation": (
        "帝符、太尊、天时、五行、八风、五风、三风与太乙合，阳宫晴旱，阴宫雨水"
    ),
    "canonical_selected": None,
    "runtime_applied": False,
    "policy": "总括句见证差异未解，不覆盖各十精逐条直接断语。",
}

DEFERRED_OBSERVATION_LAYERS = {
    "initial_move_cloud_color_timing": "deferred",
    "weather_texture_and_color": "deferred",
    "drought_rain_yin_yang_selection": "deferred",
    "wangxiang_speed_modifier": "deferred",
}


def _validate_name(name: str) -> str:
    return canonical_ten_essence_name(name)


def _validate_conjunctions(value: list[str] | None) -> tuple[list[str], bool]:
    if value is None:
        return [], False
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise TypeError("conjunctions须为字符串list或None")
    unknown = [item for item in value if item not in ALLOWED_TARGETS]
    if unknown:
        raise ValueError(f"未知C57合会对象：{unknown[0]}")
    return list(dict.fromkeys(value)), True


def ten_essence_cloud_conjunctions(
    name: str,
    *,
    conjunctions: list[str] | None = None,
    taiyi_qi_state: str | None = None,
    taiyi_palace_yinyang: str | None = None,
    essence_palace: int | None = None,
) -> dict[str, Any]:
    """解释显式十精合会/宫位证据；绝不从位置runtime自动推“合”."""
    canonical = _validate_name(name)
    if canonical == "太乙数":
        raise ValueError("太乙数天气数值规则属于独立number-omen层，不在C57十精神位合会函数")
    if taiyi_qi_state is not None and taiyi_qi_state not in QI_STATES:
        raise ValueError("taiyi_qi_state须为旺相/非旺相/休囚或None")
    if taiyi_palace_yinyang is not None and taiyi_palace_yinyang not in PALACE_YINYANG:
        raise ValueError("taiyi_palace_yinyang须为阳/阴或None")
    if essence_palace is not None and (
        not isinstance(essence_palace, int) or essence_palace not in range(1, 10)
    ):
        raise ValueError("essence_palace须为1..9或None")

    targets, checked = _validate_conjunctions(conjunctions)
    matched: list[dict[str, Any]] = []
    pending: list[str] = []

    for rule in CONJUNCTION_RULES.get(canonical, []):
        if rule["target"] not in targets:
            continue
        required_qi = rule.get("qi_state")
        if required_qi is not None:
            if taiyi_qi_state is None:
                pending.append(f"{canonical}与{rule['target']}合：须给taiyi_qi_state")
                continue
            if required_qi == "非旺相":
                if taiyi_qi_state not in {"非旺相", "休囚"}:
                    continue
            elif taiyi_qi_state != required_qi:
                continue
        required_yy = rule.get("palace_yinyang")
        if required_yy is not None:
            if taiyi_palace_yinyang is None:
                pending.append(f"{canonical}与太乙合：须给taiyi_palace_yinyang")
                continue
            if taiyi_palace_yinyang != required_yy:
                continue

        matched.append({
            "kind": "conjunction",
            "essence": canonical,
            "target": rule["target"],
            "effects": copy.deepcopy(rule.get("effects")),
            "source_status": rule["status"],
            "witness_variants": copy.deepcopy(rule.get("witness_variants")),
        })

    if essence_palace is not None:
        rule = PALACE_RULES.get(canonical, {}).get(essence_palace)
        if rule:
            matched.append({
                "kind": "palace",
                "essence": canonical,
                "palace": essence_palace,
                "effects": copy.deepcopy(rule["effects"]),
                "source_status": rule["status"],
            })

    if not checked:
        pending.append("须显式检查合会对象；无合会时传空list")

    unresolved = [
        item for item in matched
        if item.get("source_status") == "source_variant_unresolved"
    ]
    return {
        "schema_version": "1.0",
        "canonical": C57_VERSION,
        "rule_id": "C57-TEN-ESSENCE-CLOUD-CONJUNCTION",
        "source_profile": "tongzong_ten_essences_cloud_conjunctions",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "essence": canonical,
        "conjunctions": targets,
        "conjunctions_checked": checked,
        "taiyi_qi_state": taiyi_qi_state,
        "taiyi_palace_yinyang": taiyi_palace_yinyang,
        "essence_palace": essence_palace,
        "matched_omens": matched,
        "unresolved_variant_count": len(unresolved),
        "status": (
            "partial_explicit_evidence"
            if pending
            else "explicit_evidence_complete"
        ),
        "pending": list(dict.fromkeys(pending)),
        "zhangliang_summary_variant": copy.deepcopy(ZHANGLIANG_SUMMARY_VARIANT),
        "deferred_observation_layers": copy.deepcopy(DEFERRED_OBSERVATION_LAYERS),
        "auto_position_lookup_used": False,
        "j4m11_external_observation_used": False,
        "policy": (
            "C57只解释调用方显式声明的十精合会/宫位事实；"
            "不读取C53/C55/C56位置自动制造同宫，也不以J4M-11外部飞鸟观测替代十精神位。"
            "总括句异文不覆盖逐条直接断语。"
        ),
    }


def c57_catalog() -> dict[str, Any]:
    return {
        "canonical": C57_VERSION,
        "rule_id": "C57-TEN-ESSENCE-CLOUD-CONJUNCTION",
        "source_profile": "tongzong_ten_essences_cloud_conjunctions",
        "implemented_essences": sorted(CONJUNCTION_RULES),
        "conjunction_rules": copy.deepcopy(CONJUNCTION_RULES),
        "palace_rules": copy.deepcopy(PALACE_RULES),
        "zhangliang_summary_variant": copy.deepcopy(ZHANGLIANG_SUMMARY_VARIANT),
        "deferred_observation_layers": copy.deepcopy(DEFERRED_OBSERVATION_LAYERS),
        "auto_position_lookup_used": False,
    }
