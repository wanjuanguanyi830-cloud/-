"""C28 卷十七高依赖综合规则。

实现 V17-01/02/10。只组合显式结构化上游事实，不解析旧中文断语，
不重算格局、内外、旺相或门将公式。
"""

from __future__ import annotations

import copy
from typing import Any, Iterable

C28_VERSION = "taiyi-c28-tongzong-v17-high-v1"
SOURCE_PROFILE = "tongzong_volume17"

ONLINE_WITNESS = {
    "provider": "识典古籍",
    "title": "太乙统宗宝鉴卷十七",
    "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny53enihb1e",
}

MATTER_BY_QI_STATE = {
    "旺": "新事",
    "相": "相争事",
    "胎": "生产妇人事",
    "没": "溺没事",
    "死": "死丧事",
    "囚": "刑禁事",
    "休": "疾病；行人营事无成",
    "废": "废弃、改易、恐惧之事",
}


def _base(rule_id: str, name: str, source_section: str) -> dict[str, Any]:
    return {
        "canonical": C28_VERSION,
        "source_profile": SOURCE_PROFILE,
        "source_rule_id": rule_id,
        "name": name,
        "source_section": source_section,
        "online_witness": copy.deepcopy(ONLINE_WITNESS),
        "cross_c8_merge": False,
        "cross_j4m_merge": False,
    }


def _bool_or_none(name: str, value: bool | None) -> None:
    if value is not None and not isinstance(value, bool):
        raise TypeError(f"{name}须为bool或None")


def _evidence_summary(good: list[dict[str, Any]], bad: list[dict[str, Any]]) -> str:
    if good and bad:
        return "mixed_evidence"
    if good:
        return "favorable"
    if bad:
        return "unfavorable"
    return "undetermined"


def military_action_timing(
    *,
    half_year: str,
    skyeyes_clear_of_qiupo: bool | None,
    shiji_clear_of_yanji: bool | None,
    calc_harmony: bool | None,
    generals_released: bool | None,
    taiyi_under_open_rest_life_door: bool | None,
    obstructing_patterns: Iterable[str] | None = None,
) -> dict[str, Any]:
    """V17-01 出兵举事用日/用时。

    half_year 只表示来源要求的冬至后阳局 / 夏至后阴局背景，不在本函数推遁局。
    """
    if half_year not in {"冬至后", "夏至后"}:
        raise ValueError("half_year须为冬至后或夏至后")
    for name, value in {
        "skyeyes_clear_of_qiupo": skyeyes_clear_of_qiupo,
        "shiji_clear_of_yanji": shiji_clear_of_yanji,
        "calc_harmony": calc_harmony,
        "generals_released": generals_released,
        "taiyi_under_open_rest_life_door": taiyi_under_open_rest_life_door,
    }.items():
        _bool_or_none(name, value)

    patterns = list(obstructing_patterns or [])
    allowed_patterns = {"关", "囚", "掩", "迫", "格", "击", "对"}
    unknown = sorted(set(patterns) - allowed_patterns)
    if unknown:
        raise ValueError(f"未知阻格类型: {', '.join(unknown)}")

    required = {
        "skyeyes_clear_of_qiupo": skyeyes_clear_of_qiupo,
        "shiji_clear_of_yanji": shiji_clear_of_yanji,
        "calc_harmony": calc_harmony,
        "generals_released": generals_released,
    }
    missing = [name for name, value in required.items() if value is None]
    if taiyi_under_open_rest_life_door is None:
        missing.append("taiyi_under_open_rest_life_door")

    blockers: list[dict[str, Any]] = []
    if skyeyes_clear_of_qiupo is False:
        blockers.append({"condition": "文昌有囚迫", "source": "direct"})
    if shiji_clear_of_yanji is False:
        blockers.append({"condition": "始击有掩击", "source": "direct"})
    if calc_harmony is False:
        blockers.append({"condition": "算不和", "source": "direct"})
    if generals_released is False:
        blockers.append({"condition": "大小将不发", "source": "direct"})
    if taiyi_under_open_rest_life_door is True:
        blockers.append({"condition": "太乙在开休生门下", "source": "direct"})
    for pattern in patterns:
        blockers.append({"condition": f"见{pattern}", "source": "supplemental_source_clause"})

    background = "阳局" if half_year == "冬至后" else "阴局"
    computable = not missing
    usable = computable and not blockers and all(value is True for value in required.values()) and taiyi_under_open_rest_life_door is False

    return {
        **_base("V17-01", "出兵用时", "明太乙出兵举事用日之术／用时之术"),
        "status": "ok" if computable else "not_computable",
        "computable": computable,
        "half_year": half_year,
        "required_background": background,
        "missing_inputs": missing,
        "blockers": blockers,
        "usable": usable if computable else None,
        "verdict": (
            "利以兴师动众、征伐举事"
            if usable
            else ("不满足来源用时条件" if computable else "缺结构化条件")
        ),
        "policy": (
            "只组合来源明示条件；不从三门/格局中文字符串反推。"
            "开休生门下是独立阻项，不以“三门具”字段替代。"
        ),
    }


def enemy_state(
    away_cal: int,
    *,
    calc_harmony: bool | None,
    three_doors_ready: bool | None,
    five_generals_released: bool | None,
    has_yanji: bool = False,
    has_poji: bool = False,
    has_clamp_or_ge: bool = False,
    host_guest_gather_taiyi_front: bool | None = None,
    enemy_origin: str | None = None,
    guest_eye_motion: str | None = None,
) -> dict[str, Any]:
    """V17-02 敌国动静。

    “主客俱会太乙宫前”由上游几何层显式给出；本函数不自己数宫位。
    """
    if isinstance(away_cal, bool) or not isinstance(away_cal, int):
        raise TypeError("away_cal须为int")
    if not 1 <= away_cal <= 40:
        raise ValueError("away_cal须在1..40")
    for name, value in {
        "calc_harmony": calc_harmony,
        "three_doors_ready": three_doors_ready,
        "five_generals_released": five_generals_released,
        "host_guest_gather_taiyi_front": host_guest_gather_taiyi_front,
    }.items():
        _bool_or_none(name, value)
    for name, value in {
        "has_yanji": has_yanji,
        "has_poji": has_poji,
        "has_clamp_or_ge": has_clamp_or_ge,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{name}须为bool")
    if enemy_origin is not None and enemy_origin not in {"北", "南", "东", "西", "四夷"}:
        raise ValueError("enemy_origin须为北/南/东/西/四夷/None")
    if guest_eye_motion is not None and guest_eye_motion not in {"南", "北", "东", "西"}:
        raise ValueError("guest_eye_motion须为南/北/东/西/None")

    if away_cal in {5, 15, 25, 35}:
        return {
            **_base("V17-02", "敌国动静", "明敌国动静"),
            "status": "ok",
            "computable": True,
            "away_cal": away_cal,
            "duse": True,
            "arrival": "敌不来",
            "disposition": "八门杜塞",
            "favorable_evidence": [],
            "hostile_evidence": [],
            "summary": "no_arrival_direct",
            "motion_example": None,
            "policy": "杜塞为来源直接断；不再用其他综合条件覆盖。",
        }

    favorable: list[dict[str, Any]] = []
    hostile: list[dict[str, Any]] = []

    if calc_harmony is True:
        favorable.append({"condition": "客算和"})
    elif calc_harmony is False:
        hostile.append({"condition": "阴阳不和"})
    if three_doors_ready is True:
        favorable.append({"condition": "三门具"})
    elif three_doors_ready is False:
        hostile.append({"condition": "三门不具"})
    if five_generals_released is True:
        favorable.append({"condition": "五将发"})
    elif five_generals_released is False:
        hostile.append({"condition": "五将不发"})
    if not has_yanji and not has_poji and not has_clamp_or_ge:
        favorable.append({"condition": "无掩击迫/扶格"})
    else:
        if has_yanji:
            hostile.append({"condition": "有掩击"})
        if has_poji:
            hostile.append({"condition": "有迫"})
        if has_clamp_or_ge:
            hostile.append({"condition": "有扶挟/格"})
    if host_guest_gather_taiyi_front is True:
        favorable.append({"condition": "主客俱会太乙宫前"})
    elif host_guest_gather_taiyi_front is False:
        hostile.append({"condition": "主客不会太乙宫前"})

    all_good_known = all(value is True for value in (
        calc_harmony, three_doors_ready, five_generals_released,
        host_guest_gather_taiyi_front,
    )) and not (has_yanji or has_poji or has_clamp_or_ge)

    any_bad = bool(hostile)
    if all_good_known:
        summary = "surrender_not_bandit"
        arrival = "敌来降"
        disposition = "不为寇盗"
    elif any_bad and favorable:
        summary = "mixed_evidence"
        arrival = "未定"
        disposition = "好坏征兆并见"
    elif any_bad:
        summary = "hostile_evidence"
        arrival = "若入则为寇盗"
        disposition = "不降"
    else:
        summary = "undetermined"
        arrival = "未定"
        disposition = "待补结构条件"

    motion_example = None
    if enemy_origin == "北" and guest_eye_motion in {"南", "北"}:
        motion_example = {
            "scope": "source_northern_enemy_example",
            "motion": guest_eye_motion,
            "meaning": "来" if guest_eye_motion == "南" else "不来",
        }

    return {
        **_base("V17-02", "敌国动静", "明敌国动静"),
        "status": "ok",
        "computable": True,
        "away_cal": away_cal,
        "duse": False,
        "arrival": arrival,
        "disposition": disposition,
        "favorable_evidence": favorable,
        "hostile_evidence": hostile,
        "summary": summary,
        "motion_example": motion_example,
        "policy": (
            "来降与为寇条件并列保存；不以单一bad布尔值覆盖。"
            "客目南北转行只按原文北狄示例使用，不泛化为四方通则。"
        ),
    }


def hourly_general_affairs(
    *,
    skyeyes_masks_taiyi: bool = False,
    skyeyes_hits_taiyi: bool = False,
    doors_ready: bool | None,
    generals_released: bool | None,
    calc_harmony: bool | None,
    host_clamps_guest_or_blocks_guest: bool = False,
    guest_clamps_host_or_blocks_host: bool = False,
    skyeyes_qi_state: str | None = None,
    skyeyes_opposes_taiyi: bool = False,
    forbidden_directions: Iterable[str] | None = None,
) -> dict[str, Any]:
    """V17-10 时计占诸事。

    旺相休囚等由上游显式给出；吕申加临的方向也只接受上游结果。
    """
    for name, value in {
        "doors_ready": doors_ready,
        "generals_released": generals_released,
        "calc_harmony": calc_harmony,
    }.items():
        _bool_or_none(name, value)
    for name, value in {
        "skyeyes_masks_taiyi": skyeyes_masks_taiyi,
        "skyeyes_hits_taiyi": skyeyes_hits_taiyi,
        "host_clamps_guest_or_blocks_guest": host_clamps_guest_or_blocks_guest,
        "guest_clamps_host_or_blocks_host": guest_clamps_host_or_blocks_host,
        "skyeyes_opposes_taiyi": skyeyes_opposes_taiyi,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{name}须为bool")
    if skyeyes_qi_state is not None and skyeyes_qi_state not in MATTER_BY_QI_STATE:
        raise ValueError("skyeyes_qi_state须为旺/相/胎/没/死/囚/休/废/None")

    good: list[dict[str, Any]] = []
    bad: list[dict[str, Any]] = []
    social: list[dict[str, Any]] = []

    if skyeyes_masks_taiyi:
        bad.append({"condition": "天目掩太乙", "effect": "经行、兴造、置买等百事败失不利"})
    if skyeyes_hits_taiyi:
        bad.append({"condition": "天目击太乙", "effect": "行者见呵留"})

    full_known = all(value is not None for value in (doors_ready, generals_released, calc_harmony))
    if full_known:
        if doors_ready is True and generals_released is True and calc_harmony is True:
            good.append({"condition": "门具将发阴阳和", "effect": "百事吉"})
        elif doors_ready is False and generals_released is False and calc_harmony is False:
            bad.append({"condition": "门不具将不发算不和", "effect": "百事凶"})
        else:
            social.append({
                "condition": "门/将/算条件不齐同向",
                "effect": "当消息而推，不作全吉全凶",
            })

    if host_clamps_guest_or_blocks_guest:
        social.append({
            "condition": "主人扶挟客或关客",
            "effect": "可言吏，不可言民",
        })
    if guest_clamps_host_or_blocks_host:
        social.append({
            "condition": "客扶挟主人或关主",
            "effect": "可言民，不可言吏",
        })

    matter = MATTER_BY_QI_STATE.get(skyeyes_qi_state)
    if skyeyes_qi_state == "囚" and skyeyes_opposes_taiyi:
        matter = f"{matter}；与太乙相对时有赦释之象"

    directions = list(forbidden_directions or [])
    for direction in directions:
        if not isinstance(direction, str) or not direction:
            raise ValueError("forbidden_directions须为非空字符串列表")

    missing = [
        name for name, value in {
            "doors_ready": doors_ready,
            "generals_released": generals_released,
            "calc_harmony": calc_harmony,
        }.items() if value is None
    ]

    return {
        **_base("V17-10", "时计诸事", "明时计以占诸事术"),
        "status": "ok" if not missing else "partial",
        "computable": True,
        "missing_inputs": missing,
        "favorable_evidence": good,
        "unfavorable_evidence": bad,
        "conditional_notes": social,
        "summary": _evidence_summary(good, bad),
        "skyeyes_qi_state": skyeyes_qi_state,
        "matter": matter,
        "forbidden_directions": directions,
        "direction_policy": (
            "吕申加岁月时所得太阳/阴主避向必须由独立上游算法提供；"
            "本条不从太乙宫自行猜方向。"
        ),
        "policy": "综合层只组合结构化条件；不解析格局字符串，不重算旺相休囚。",
    }


def c28_catalog() -> dict[str, Any]:
    return {
        "canonical": C28_VERSION,
        "implemented": ["V17-01", "V17-02", "V17-10"],
        "dependency_class": "high_structured_composite",
        "source_limited_inputs": True,
        "policy": (
            "高依赖规则只组合已结构化事实；"
            "不把C8/J4M/格局层重新解释为卷十七新公式。"
        ),
    }
