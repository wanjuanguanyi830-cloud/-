"""C24 卷十五外部观测低依赖规则。

实现 V15-09 五音风、V15-12 风从八卦、V15-13 云气逆顺。
所有风/云信息必须由调用方显式提供；不得从盘面或日期虚构实际观测。
"""

from __future__ import annotations

import copy
from typing import Any

from .tongzong_v15_low_dependency import MARCH_DIRECTIONS

C24_VERSION = "taiyi-c24-tongzong-v15-observation-v1"
SOURCE_PROFILE = "tongzong_volume15"

BRANCH_TONE = {
    "子": "宫",
    "午": "宫",
    "丑": "徵",
    "寅": "徵",
    "未": "徵",
    "申": "徵",
    "卯": "羽",
    "酉": "羽",
    "辰": "商",
    "戌": "商",
    "巳": "角",
    "亥": "角",
}
TONE_ELEMENT = {
    "宫": "土",
    "徵": "火",
    "羽": "水",
    "商": "金",
    "角": "木",
}
ELEMENT_GENERATES = {
    "木": "火",
    "火": "土",
    "土": "金",
    "金": "水",
    "水": "木",
}
ELEMENT_CONTROLS = {
    "木": "土",
    "土": "水",
    "水": "火",
    "火": "金",
    "金": "木",
}

WIND_PALACE_RULES = {
    1: {
        "palace_name": "乾",
        "direction": "西北",
        "side_effect": "利客",
        "movement": "客宜先举",
    },
    8: {
        "palace_name": "坎",
        "direction": "正北",
        "side_effect": "利客",
        "movement": "客宜先举",
    },
    3: {
        "palace_name": "艮",
        "direction": "东北",
        "side_effect": "利客",
        "movement": "客宜先举",
    },
    4: {
        "palace_name": "震",
        "direction": "正东",
        "side_effect": "利主",
        "movement": "主宜后应",
    },
    9: {
        "palace_name": "巽",
        "direction": "东南",
        "side_effect": "利主",
        "movement": "主宜后应",
    },
    2: {
        "palace_name": "离",
        "direction": "正南",
        "side_effect": "利主",
        "movement": "主宜后应",
    },
    7: {
        "palace_name": "坤",
        "direction": "西南",
        "side_effect": "source_text_uncertain",
        "movement": None,
        "source_note": "当前在线OCR作“主有谋不成，主客西北利”等，语句有讹，暂不压成确定胜负。",
    },
    6: {
        "palace_name": "兑",
        "direction": "正西",
        "side_effect": "客有伏兵",
        "movement": "主宜设备",
    },
}

OPPOSITE_DIRECTION = {
    "西北": "东南",
    "东南": "西北",
    "正南": "正北",
    "正北": "正南",
    "东北": "西南",
    "西南": "东北",
    "正东": "正西",
    "正西": "正东",
}

ONLINE_WITNESS = {
    "provider": "识典古籍",
    "url": "https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppxduthvru",
    "edition_note": "不同电子本卷次编排有差异；按术目定位军事应用篇。",
}


def _base(rule_id: str, name: str, source_section: str) -> dict[str, Any]:
    return {
        "canonical": C24_VERSION,
        "source_profile": SOURCE_PROFILE,
        "source_rule_id": rule_id,
        "name": name,
        "source_section": source_section,
        "online_witness": copy.deepcopy(ONLINE_WITNESS),
        "requires_external_observation": True,
        "cross_j4m_merge": False,
        "cross_c8_merge": False,
    }


def _branch_tone(branch: str) -> dict[str, str]:
    if branch not in BRANCH_TONE:
        raise ValueError("地支须为子丑寅卯辰巳午未申酉戌亥")
    tone = BRANCH_TONE[branch]
    return {"branch": branch, "tone": tone, "element": TONE_ELEMENT[tone]}


def _element_relation(day_element: str, wind_element: str) -> str:
    if day_element == wind_element:
        return "same_element"
    if ELEMENT_GENERATES.get(wind_element) == day_element:
        return "wind_parent_of_day"
    if ELEMENT_GENERATES.get(day_element) == wind_element:
        return "wind_child_of_day"
    if ELEMENT_CONTROLS.get(day_element) == wind_element:
        return "day_controls_wind"
    if ELEMENT_CONTROLS.get(wind_element) == day_element:
        return "wind_controls_day"
    return "unclassified"


def five_tone_wind(
    day_branch: str,
    *,
    wind_direction_branch: str | None = None,
    hour_branch: str | None = None,
) -> dict[str, Any]:
    """V15-09 五音风。

    日支/时支用于五音背景；真实风向支必须显式传入。
    未提供风向时不输出观测性胜负判断。
    """
    result = _base("V15-09", "五音风", "明五音考风以知盛衰之术")
    day = _branch_tone(day_branch)
    hour = _branch_tone(hour_branch) if hour_branch is not None else None

    if wind_direction_branch is None:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "missing_inputs": ["wind_direction_branch"],
            "day_tone": day,
            "hour_tone": hour,
            "policy": "无实测风向，不得由盘面推造风音。",
        }

    wind = _branch_tone(wind_direction_branch)
    relation = _element_relation(day["element"], wind["element"])

    # 本篇明确给出“母来翼子 / 子来扶母”均可见成功。
    if relation == "wind_parent_of_day":
        direct_effect = "母来翼子；出军可见成功"
    elif relation == "wind_child_of_day":
        direct_effect = "子来扶母；出军可见成功"
    else:
        direct_effect = None

    # “辰戌商风为鬼风”在原文例子中是角木日受商金所克；
    # 不把该例无条件推广到所有日音。
    exact_ghost_example = (
        day["tone"] == "角"
        and wind_direction_branch in ("辰", "戌")
        and relation == "wind_controls_day"
    )

    return {
        **result,
        "status": "ok",
        "computable": True,
        "day_tone": day,
        "hour_tone": hour,
        "wind_tone": wind,
        "relation": relation,
        "direct_effect": direct_effect,
        "ghost_wind_exact_example_match": exact_ghost_example,
        "winner": None,
        "policy": (
            "五音关系先结构化；除原文明示的母子相生与特定例证外，"
            "不把一个例局推广成通用主客胜负。"
        ),
    }


def wind_from_bagua(wind_palace: int | None) -> dict[str, Any]:
    """V15-12 风从八卦分主客。

    风起宫必须是实际观测映射结果；中五不属于八卦风向。
    """
    result = _base("V15-12", "风从八卦", "明风从八卦而分主客术")
    if wind_palace is None:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "missing_inputs": ["wind_palace"],
            "policy": "无实测风向宫，不推断风从何卦。",
        }
    if isinstance(wind_palace, bool) or not isinstance(wind_palace, int):
        raise TypeError("wind_palace须为int或None")
    if wind_palace == 5 or wind_palace not in WIND_PALACE_RULES:
        return {
            **result,
            "status": "not_defined_by_source_passage",
            "computable": False,
            "wind_palace": wind_palace,
            "defined_palaces": sorted(WIND_PALACE_RULES),
        }
    return {
        **result,
        "status": "ok",
        "computable": True,
        "wind_palace": wind_palace,
        **copy.deepcopy(WIND_PALACE_RULES[wind_palace]),
        "policy": "只解释显式观测的风起宫；不自动从日期或盘面生成风向。",
    }


def _calc_digit(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("算数须为int")
    if not 1 <= value <= 40:
        raise ValueError("算数须在1..40")
    unit = value % 10
    return 10 if unit == 0 else unit


def _calc_direction(calc: int) -> str | None:
    return MARCH_DIRECTIONS.get(_calc_digit(calc))


def _cloud_relation(calc: int, cloud_from_direction: str) -> dict[str, Any]:
    calc_direction = _calc_direction(calc)
    if calc_direction is None:
        return {
            "calc": calc,
            "calc_direction": None,
            "opposite_direction": None,
            "relation": "source_direction_undefined",
        }
    opposite = OPPOSITE_DIRECTION[calc_direction]
    if cloud_from_direction == calc_direction:
        relation = "顺"
    elif cloud_from_direction == opposite:
        relation = "逆"
    else:
        relation = "不应"
    return {
        "calc": calc,
        "calc_direction": calc_direction,
        "opposite_direction": opposite,
        "relation": relation,
    }


def cloud_qi_direction(
    home_cal: int,
    away_cal: int,
    *,
    cloud_from_direction: str | None,
) -> dict[str, Any]:
    """V15-13 云气所起逆顺。

    原文以“从算而来”为顺、“冲算而来”为逆，故比较实际方向，
    不采用旧代码的数字差5近似。
    """
    result = _base("V15-13", "云气逆顺", "明云气所起逆顺之术")
    if cloud_from_direction is None:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "missing_inputs": ["cloud_from_direction"],
            "home": _cloud_relation(home_cal, ""),
            "away": _cloud_relation(away_cal, ""),
            "policy": "无实测云气来向，不得推造顺逆。",
        }
    if cloud_from_direction not in OPPOSITE_DIRECTION:
        raise ValueError(
            "cloud_from_direction须为西北/东南/正南/正北/东北/西南/正东/正西"
        )

    home = _cloud_relation(home_cal, cloud_from_direction)
    away = _cloud_relation(away_cal, cloud_from_direction)

    return {
        **result,
        "status": "ok",
        "computable": True,
        "cloud_from_direction": cloud_from_direction,
        "home": home,
        "away": away,
        "policy": (
            "顺逆分别按主算、客算之向算/冲向判断；本条不将两边自动压成一个总胜负。"
        ),
    }


def c24_catalog() -> dict[str, Any]:
    return {
        "canonical": C24_VERSION,
        "source_profile": SOURCE_PROFILE,
        "implemented": ["V15-09", "V15-12", "V15-13"],
        "all_require_external_observation": True,
        "next_dependency": [],
        "implemented_by_c25": ["V15-10"],
        "policy": "风云观测必须显式提供；缺观测返回not_computable。",
    }
