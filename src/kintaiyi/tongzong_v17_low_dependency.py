"""C26 卷十七低依赖占断第一批。

实现 V17-03/04/05/11。所有位置关系与五行关系都要求结构化输入，
不复刻参考仓库中的近似宫界/自动五行猜测。
"""

from __future__ import annotations

import copy
from typing import Any

C26_VERSION = "taiyi-c26-tongzong-v17-low-v1"
SOURCE_PROFILE = "tongzong_volume17"

ONLINE_WITNESS = {
    "provider": "识典古籍",
    "title": "太乙统宗宝鉴卷十七",
    "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny53enihb1e",
}

ELEMENT_CONTROLS = {
    "木": "土",
    "土": "水",
    "水": "火",
    "火": "金",
    "金": "木",
}

ARRIVAL_RELATIVE_DIRECTIONS = {
    "左": "东方",
    "右": "西方",
    "前": "南方",
    "后": "北方",
    "四维": "四维",
}

# 行人来否：多个在线见证对南方“来数”有异文。
TRAVELER_NUMBER_RULES = {
    "北": {
        "not_come": {3, 8},
        "come": {2, 7},
        "status": "stable_across_checked_witnesses",
    },
    "东": {
        "not_come": {4, 9},
        "come": {1, 6},
        "status": "attested_in_cadal_witness",
    },
    "西": {
        "not_come": {1, 6},
        "come": {4, 9},
        "status": "stable_across_checked_witnesses",
    },
    "南": {
        "not_come": {2, 7},
        "come": None,
        "status": "variant_conflict",
        "variants": [
            {
                "witness": "NGJ / 三才世纬引文",
                "come": {1, 6},
            },
            {
                "witness": "CADAL 太乙统宗宝鉴",
                "come": {3, 8},
            },
        ],
    },
}


def _base(rule_id: str, name: str, source_section: str) -> dict[str, Any]:
    return {
        "canonical": C26_VERSION,
        "source_profile": SOURCE_PROFILE,
        "source_rule_id": rule_id,
        "name": name,
        "source_section": source_section,
        "online_witness": copy.deepcopy(ONLINE_WITNESS),
        "cross_c8_merge": False,
        "cross_j4m_merge": False,
    }


def enemy_spy_state(
    *,
    shiji_realm: str,
    away_general_realm: str,
    away_vassal_realm: str | None = None,
    skyeyes_realm: str | None = None,
    away_general_at_skyeyes: bool = False,
    shiji_depth: str | None = None,
) -> dict[str, Any]:
    """V17-03 敌国有无间谍窥探。

    realm 由上游按该篇内外界法结构化，本条不自行重建宫界。
    """
    valid_realms = {"内", "外"}
    for label, value in {
        "shiji_realm": shiji_realm,
        "away_general_realm": away_general_realm,
    }.items():
        if value not in valid_realms:
            raise ValueError(f"{label}须为内或外")
    for label, value in {
        "away_vassal_realm": away_vassal_realm,
        "skyeyes_realm": skyeyes_realm,
    }.items():
        if value is not None and value not in valid_realms:
            raise ValueError(f"{label}须为内/外/None")
    if shiji_depth is not None and shiji_depth not in {"近", "远"}:
        raise ValueError("shiji_depth须为近/远/None")

    events: list[dict[str, str]] = []

    if shiji_realm == "外":
        events.append({
            "event": "foreign_spy_envoy",
            "meaning": "外国遣使入境，窥觇虚实",
        })

    if skyeyes_realm == "外" and away_general_at_skyeyes:
        events.append({
            "event": "spy_entered_our_border",
            "meaning": "主目在外地而客大将临其位，有奸细入境之象",
        })

    if (
        shiji_realm == "外"
        and away_general_realm == "外"
        and away_vassal_realm == "外"
    ):
        events.append({
            "event": "enemy_forces_entering",
            "meaning": "客目、客大将、客参将俱在外地，主敌方遣将卒入境",
        })

    depth_meaning = None
    if shiji_realm == "外" and shiji_depth is not None:
        depth_meaning = "已入境" if shiji_depth == "近" else "始发之期"

    return {
        **_base("V17-03", "间谍虚实", "明敌国有无间谍窥探"),
        "status": "ok",
        "computable": True,
        "inputs": {
            "shiji_realm": shiji_realm,
            "away_general_realm": away_general_realm,
            "away_vassal_realm": away_vassal_realm,
            "skyeyes_realm": skyeyes_realm,
            "away_general_at_skyeyes": bool(away_general_at_skyeyes),
            "shiji_depth": shiji_depth,
        },
        "events": events,
        "depth_meaning": depth_meaning,
        "no_positive_condition": not events,
        "policy": (
            "没有命中条件时只记no_positive_condition，不反推“绝无间谍”；"
            "内外深浅必须由来源一致的上游几何层给出。"
        ),
    }


def enemy_envoy_truth(
    *,
    taiyi_element: str,
    shiji_element: str,
    away_general_element: str,
) -> dict[str, Any]:
    """V17-04 敌使虚实：按太乙与客目/客大将五行制化收集证据。"""
    valid = set(ELEMENT_CONTROLS)
    for name, value in {
        "taiyi_element": taiyi_element,
        "shiji_element": shiji_element,
        "away_general_element": away_general_element,
    }.items():
        if value not in valid:
            raise ValueError(f"{name}须为木火土金水")

    real_evidence = []
    false_evidence = []

    for target_name, target_element in (
        ("客目始击", shiji_element),
        ("客大将", away_general_element),
    ):
        if ELEMENT_CONTROLS[taiyi_element] == target_element:
            real_evidence.append(f"太乙{taiyi_element}制{target_name}{target_element}")
        if ELEMENT_CONTROLS[target_element] == taiyi_element:
            false_evidence.append(f"{target_name}{target_element}反制太乙{taiyi_element}")

    if real_evidence and false_evidence:
        verdict = "mixed_evidence"
    elif real_evidence:
        verdict = "实"
    elif false_evidence:
        verdict = "虚"
    else:
        verdict = "未定"

    return {
        **_base("V17-04", "敌使虚实", "明敌使虚实之术"),
        "status": "ok",
        "computable": True,
        "verdict": verdict,
        "real_evidence": real_evidence,
        "false_evidence": false_evidence,
        "policy": "若实/虚证据同时出现则保留mixed_evidence，不按代码顺序强行覆盖。",
    }


def enemy_arrival_scale(
    away_cal: int,
    *,
    time_yinyang: str,
    calc_harmony: bool | None,
    shiji_relative_position: str | None = None,
) -> dict[str, Any]:
    """V17-05 敌兵来方、将卒多寡。

    - 时计阳/阴：有贼/无贼
    - 5/15/25/35：八门杜塞，不来
    - <=15：兵寡无将
    - >=16 且阴阳和：有将有卒、兵众
    - 来方按客目左/右/前/后/四维。
    """
    if isinstance(away_cal, bool) or not isinstance(away_cal, int):
        raise TypeError("away_cal须为int")
    if not 1 <= away_cal <= 40:
        raise ValueError("away_cal须在1..40")
    if time_yinyang not in {"阳", "阴"}:
        raise ValueError("time_yinyang须为阳或阴")
    if calc_harmony is not None and not isinstance(calc_harmony, bool):
        raise TypeError("calc_harmony须为bool或None")
    if (
        shiji_relative_position is not None
        and shiji_relative_position not in ARRIVAL_RELATIVE_DIRECTIONS
    ):
        raise ValueError("shiji_relative_position须为左/右/前/后/四维/None")

    duse = away_cal in {5, 15, 25, 35}
    enemy_present = time_yinyang == "阳"

    if duse:
        arrival = "不来"
        force_scale = "八门杜塞"
    elif not enemy_present:
        arrival = "无贼"
        force_scale = "不据兵数扩断"
    else:
        arrival = "有贼"
        if away_cal <= 15:
            force_scale = "兵寡、无将"
        elif calc_harmony is True:
            force_scale = "兵众、有将有卒"
        elif calc_harmony is False:
            force_scale = "16以上但阴阳不和，来源大兵条件不成立"
        else:
            force_scale = "16以上但缺阴阳和输入，规模未定"

    direction = (
        ARRIVAL_RELATIVE_DIRECTIONS[shiji_relative_position]
        if shiji_relative_position is not None
        else None
    )

    return {
        **_base("V17-05", "敌兵来方", "明敌人来方将卒多寡"),
        "status": "ok",
        "computable": True,
        "away_cal": away_cal,
        "time_yinyang": time_yinyang,
        "calc_harmony": calc_harmony,
        "duse_no_arrival": duse,
        "enemy_present_by_time_yinyang": enemy_present,
        "arrival": arrival,
        "force_scale": force_scale,
        "shiji_relative_position": shiji_relative_position,
        "direction": direction,
        "policy": "不把“16以上”单独当成兵众充分条件；必须同时满足阴阳和。",
    }


def _calc_digit(calc: int) -> int:
    if isinstance(calc, bool) or not isinstance(calc, int):
        raise TypeError("guest_calc须为int")
    if not 1 <= calc <= 40:
        raise ValueError("guest_calc须在1..40")
    unit = calc % 10
    return 10 if unit == 0 else unit


def traveler_arrival(
    travel_direction: str,
    guest_calc: int,
    *,
    has_yanji: bool = False,
    has_guange: bool = False,
) -> dict[str, Any]:
    """V17-11 占望行人及贼来与不来。

    南方“来数”在在线见证中存在1/6与3/8两种读法，保留variant_conflict。
    """
    if travel_direction not in TRAVELER_NUMBER_RULES:
        raise ValueError("travel_direction须为北/南/东/西")
    if not isinstance(has_yanji, bool) or not isinstance(has_guange, bool):
        raise TypeError("has_yanji/has_guange须为bool")

    digit = _calc_digit(guest_calc)
    rule = TRAVELER_NUMBER_RULES[travel_direction]
    not_come = rule["not_come"]
    come = rule["come"]

    source_variant = None
    if digit in not_come:
        base_verdict = "不来"
    elif come is not None and digit in come:
        base_verdict = "来"
    elif rule["status"] == "variant_conflict":
        matches = [
            item["witness"]
            for item in rule["variants"]
            if digit in item["come"]
        ]
        if matches:
            base_verdict = "variant_conflict"
            source_variant = {
                "digit": digit,
                "matching_witnesses": matches,
                "variants": copy.deepcopy(rule["variants"]),
            }
        else:
            base_verdict = "未定"
    else:
        base_verdict = "未定"

    if has_guange:
        effective = "尚未发"
    elif has_yanji:
        effective = "虽发未至"
    else:
        effective = base_verdict

    return {
        **_base("V17-11", "占望行人", "明占望行人及贼来与不来"),
        "status": "ok",
        "computable": True,
        "travel_direction": travel_direction,
        "guest_calc": guest_calc,
        "digit": digit,
        "base_verdict": base_verdict,
        "effective_verdict": effective,
        "has_yanji": has_yanji,
        "has_guange": has_guange,
        "arrival_day_count_method": {
            "type": "guest_calc_days",
            "days": guest_calc,
            "source_example": "客算23则自当日起至第23日为到期",
        },
        "source_variant": source_variant,
        "number_rule_status": rule["status"],
        "policy": "掩击/关格作为明确修正；南方来数异文不静默选本。",
    }


def c26_catalog() -> dict[str, Any]:
    return {
        "canonical": C26_VERSION,
        "implemented": ["V17-03", "V17-04", "V17-05", "V17-11"],
        "source_limited_inputs": True,
        "known_variants": ["V17-11_south_come_numbers"],
        "policy": "几何、五行、观测/格局事实由上游结构化提供。",
    }
