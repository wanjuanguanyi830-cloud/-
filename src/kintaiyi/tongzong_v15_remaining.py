"""《太乙统宗宝鉴》军事应用剩余五条 source-limited runtime。

实现 V15-01 / 07 / 08 / 11 / 14。

原则：
- 只实现术目正文能够直接支持的结构；
- 不把旧 reference implementation 的近似、个别局例或跨层补断带回来；
- 所有格局、门将、阳绝、风云军势等事实均要求显式输入；
- 与 J4M / C8 同名近名规则保持 source profile 隔离。
"""

from __future__ import annotations

import copy
from typing import Any

from .tongzong_v15_low_dependency import formation_flag_from_calc


VERSION = "taiyi-tongzong-v15-remaining-v1"
SOURCE_PROFILE = "tongzong_volume15"

HIDDEN_CALCS = {1, 11, 21, 31}

TERRAIN_FORMATIONS = {
    "后高前下": {"formation": "锐阵", "element": "火", "effect": "利于进战溃敌"},
    "前高后下": {"formation": "直阵", "element": "木", "effect": "利于近守备御待敌"},
    "左右势高": {"formation": "曲阵", "element": "水", "effect": "利于吞敌"},
    "跨斜不便": {"formation": "圆阵", "element": "土", "effect": "利于坚守"},
    "地高广平": {"formation": "方阵", "element": "金", "effect": "利于速战"},
}

TERRAIN_ALIASES = {
    "後高前下": "后高前下",
    "前高後下": "前高后下",
    "左右勢高": "左右势高",
    "跨斜不便於我": "跨斜不便",
    "地高而廣平": "地高广平",
    "地高廣平": "地高广平",
}

TERRAIN_ARMS = [
    {"terrain": "山林沟壑茂林积石", "advantage": "步兵", "comparison": "车骑二不当一"},
    {"terrain": "土山平原四向广野", "advantage": "车骑", "comparison": "步兵十不当一"},
    {"terrain": "山谷幽涧仰高临下", "advantage": "弓弩", "comparison": "短兵百不当一"},
    {
        "terrain": "两阵相近平地浅草",
        "advantage": "长戟类",
        "comparison": "剑盾三不当一",
        "textual_variants": ["长战", "长戎", "长戟"],
        "normalization_note": "电子转录异形并存；按平行古文/兵书见证归为长戟类，不回写单一原字。",
    },
    {
        "terrain": "芦苇竹篠草木蒙茸",
        "advantage": "矛鋋类",
        "comparison": "弓弩三不当一",
        "textual_variants": ["矛旋", "矛鋋", "矛铤"],
        "normalization_note": "电子转录与平行见证字形不同；保留异文并只归一器类。",
    },
]

CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

UPPER_FORBIDDEN = ("掩", "击", "擊", "扶", "格")
LOWER_FORBIDDEN = ("关", "關", "囚", "迫", "对", "對")

MILITARY_OBSERVATION_KEYS = {
    "wind_from_rear",
    "troops_vigorous",
    "horses_neighing",
    "flags_toward_enemy",
    "drums_clear",
    "command_harmonious",
    "crosswind_forward",
    "birth_wind_direction",
    "sky_clear",
    "troops_horses_eager",
    "ranks_happy",
    "wind_harmonious",
    "storm_moves_to_enemy_within_three_days",
    "ghost_wind",
    "violent_wind_rain_weak_morale",
    "gloomy_chaotic_wind",
    "long_overcast_without_rain",
    "no_wind",
    "flag_broken_by_gust",
    "flags_point_backward",
    "reverse_wind_blocks_flags",
    "weapons_flags_abnormal",
    "violent_wind_collapses_camp",
    "reverse_rain_not_wet_clothes",
    "sudden_rain_in_battle",
}


def _base(rule_id: str, name: str, source_section: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "canonical": VERSION,
        "source_profile": SOURCE_PROFILE,
        "source_rule_id": rule_id,
        "name": name,
        "source_section": source_section,
        "cross_j4m_merge": False,
        "cross_c8_merge": False,
    }


def _explicit_patterns(value: list[str] | tuple[str, ...] | None, name: str) -> list[str] | None:
    if value is None:
        return None
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"{name}须为list/tuple或None")
    result = []
    for item in value:
        if not isinstance(item, str):
            raise TypeError(f"{name}各项须为str")
        result.append(item)
    return result


def _has_any(patterns: list[str] | None, needles: tuple[str, ...]) -> bool | None:
    if patterns is None:
        return None
    return any(any(needle in item for needle in needles) for item in patterns)


def qibing_fubing(
    *,
    skyeyes: Any = None,
    shiji: Any = None,
    home_cal: int | None = None,
    away_cal: int | None = None,
    pattern_evidence: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """V15-01 奇兵伏兵。

    大杀位置直接消费文昌/始击位置；不把局例中的具体时支当通则。
    """

    patterns = _explicit_patterns(pattern_evidence, "pattern_evidence")
    ambush_window = _has_any(patterns, ("掩", "迫"))

    for name, value in {"home_cal": home_cal, "away_cal": away_cal}.items():
        if value is not None:
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name}须为int或None")
            if not 1 <= value <= 40:
                raise ValueError(f"{name}须在1..40")

    missing = []
    if skyeyes is None:
        missing.append("skyeyes")
    if shiji is None:
        missing.append("shiji")
    if patterns is None:
        missing.append("pattern_evidence")

    concealment = {
        "home": home_cal in HIDDEN_CALCS if home_cal is not None else None,
        "away": away_cal in HIDDEN_CALCS if away_cal is not None else None,
        "source_calcs": sorted(HIDDEN_CALCS),
        "terrain": "山林沟涧等隐蔽处",
    }

    return {
        **_base("V15-01", "奇兵伏兵", "明奇兵伏兵之术／明出兵战阵所利术"),
        "status": "ok" if not missing else "partial",
        "computable": not missing,
        "odd_troop_ratio": {"numerator": 3, "denominator": 10},
        "big_kill_positions": {
            "host": {"basis": "文昌/主目所在", "position": copy.deepcopy(skyeyes)},
            "guest": {"basis": "始击/客目所在", "position": copy.deepcopy(shiji)},
        },
        "concealment": concealment,
        "pattern_evidence": copy.deepcopy(patterns),
        "ambush_window": (
            "掩迫时可发伏兵"
            if ambush_window is True
            else "显式检查未见掩迫"
            if ambush_window is False
            else None
        ),
        "missing_inputs": missing,
        "policy": (
            "奇兵三成、大杀取文昌/始击所在、1/11/21/31藏迹、掩迫时发分栏；"
            "不把来源局例中的具体时支提升为通则。"
        ),
    }


def _normalize_terrain(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("terrain_shape须为str或None")
    return TERRAIN_ALIASES.get(value, value)


def _formation_relation(home: dict[str, Any], away: dict[str, Any]) -> dict[str, Any]:
    he = home.get("element")
    ae = away.get("element")
    if not he or not ae:
        return {"winner": None, "relation": "not_computable"}
    if CONTROLS.get(he) == ae:
        return {"winner": "主", "relation": f"{he}制{ae}"}
    if CONTROLS.get(ae) == he:
        return {"winner": "客", "relation": f"{ae}制{he}"}
    return {"winner": None, "relation": "来源只明确五行相制取胜；当前无相克"}


def suidi_zhibian(
    *,
    terrain_shape: str | None = None,
    home_cal: int | None = None,
    away_cal: int | None = None,
) -> dict[str, Any]:
    """V15-07 随地制变／置阵随地。"""

    terrain = _normalize_terrain(terrain_shape)
    terrain_rule = copy.deepcopy(TERRAIN_FORMATIONS.get(terrain))

    home = formation_flag_from_calc(home_cal) if home_cal is not None else None
    away = formation_flag_from_calc(away_cal) if away_cal is not None else None
    relation = (
        _formation_relation(home, away)
        if home is not None and away is not None
        else {"winner": None, "relation": "主客算未同时提供"}
    )

    pending = []
    if terrain is None:
        pending.append("terrain_shape")
    elif terrain_rule is None:
        pending.append("来源未列此地形")

    return {
        **_base("V15-07", "随地制变", "明置阵随地之术／明随地制变之术"),
        "status": "ok" if not pending else "partial",
        "computable": not pending,
        "terrain_shape": terrain,
        "terrain_rule": terrain_rule,
        "terrain_formation_table": copy.deepcopy(TERRAIN_FORMATIONS),
        "terrain_arms_table": copy.deepcopy(TERRAIN_ARMS),
        "home_formation": copy.deepcopy(home),
        "away_formation": copy.deepcopy(away),
        "formation_relation": relation,
        "pending": pending,
        "policy": (
            "地形→宜阵与主客阵形五行相制分层；主客阵形复用V15-02结果，"
            "只在明确相克时给胜方，不以相生/同类常识扩断。"
        ),
    }


def fenhe_yongbing(
    *,
    battle_place_fixed: bool | None = None,
    battle_time_fixed: bool | None = None,
    orders_sent: bool | None = None,
    arrivals: dict[str, str] | None = None,
) -> dict[str, Any]:
    """V15-08 分合用兵。

    原文是军令/期会程序，不把三门五将或将宫同宫加入本条。
    """

    for name, value in {
        "battle_place_fixed": battle_place_fixed,
        "battle_time_fixed": battle_time_fixed,
        "orders_sent": orders_sent,
    }.items():
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"{name}须为bool或None")

    arrival_results = {}
    if arrivals is not None:
        if not isinstance(arrivals, dict):
            raise TypeError("arrivals须为dict或None")
        for commander, state in arrivals.items():
            if state not in {"early", "on_time", "late"}:
                raise ValueError("arrivals值须为early/on_time/late")
            arrival_results[str(commander)] = {
                "state": state,
                "source_consequence": (
                    "赏" if state == "early" else "斩/罚" if state == "late" else "按期会合"
                ),
            }

    prerequisites = {
        "battle_place_fixed": battle_place_fixed,
        "battle_time_fixed": battle_time_fixed,
        "orders_sent": orders_sent,
    }
    values = list(prerequisites.values())
    if all(v is True for v in values):
        ready = True
        status = "ready_to_concentrate"
    elif any(v is False for v in values):
        ready = False
        status = "procedure_incomplete"
    else:
        ready = None
        status = "not_computable"

    return {
        **_base("V15-08", "分合用兵", "明分合用兵术"),
        "status": status,
        "computable": ready is not None,
        "concentration_ready": ready,
        "prerequisites": prerequisites,
        "arrival_results": arrival_results,
        "doctrine": {
            "initial": "分兵据要地",
            "final": "按既定时地会合并力作战",
            "discipline": "先期至者赏，后期至者罚",
        },
        "policy": (
            "本条只结构化分兵、定战地战时、移檄期会与赏罚；"
            "旧实现加入的三门五将、关掩击、主客将同宫条件均不属于本条来源公式。"
        ),
    }


def anying_rishi(
    *,
    yin_yang_harmony: bool | None = None,
    upper_eye_patterns: list[str] | tuple[str, ...] | None = None,
    lower_eye_patterns: list[str] | tuple[str, ...] | None = None,
    taiyi_in_yang_jue: bool | None = None,
    upper_eye_in_yang_jue: bool | None = None,
    lower_eye_in_yang_jue: bool | None = None,
    three_doors_ready: bool | None = None,
    five_generals_released: bool | None = None,
) -> dict[str, Any]:
    """V15-11 安营置阵取用日时。"""

    for name, value in {
        "yin_yang_harmony": yin_yang_harmony,
        "taiyi_in_yang_jue": taiyi_in_yang_jue,
        "upper_eye_in_yang_jue": upper_eye_in_yang_jue,
        "lower_eye_in_yang_jue": lower_eye_in_yang_jue,
        "three_doors_ready": three_doors_ready,
        "five_generals_released": five_generals_released,
    }.items():
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"{name}须为bool或None")

    upper = _explicit_patterns(upper_eye_patterns, "upper_eye_patterns")
    lower = _explicit_patterns(lower_eye_patterns, "lower_eye_patterns")
    upper_bad = _has_any(upper, UPPER_FORBIDDEN)
    lower_bad = _has_any(lower, LOWER_FORBIDDEN)

    conditions = {
        "yin_yang_harmony": yin_yang_harmony,
        "upper_eye_clear": None if upper_bad is None else not upper_bad,
        "lower_eye_clear": None if lower_bad is None else not lower_bad,
        "taiyi_not_in_yang_jue": None if taiyi_in_yang_jue is None else not taiyi_in_yang_jue,
        "upper_eye_not_in_yang_jue": None if upper_eye_in_yang_jue is None else not upper_eye_in_yang_jue,
        "lower_eye_not_in_yang_jue": None if lower_eye_in_yang_jue is None else not lower_eye_in_yang_jue,
        "three_doors_ready": three_doors_ready,
        "five_generals_released": five_generals_released,
    }

    vals = list(conditions.values())
    if any(v is False for v in vals):
        suitable = False
        status = "unfavorable"
    elif all(v is True for v in vals):
        suitable = True
        status = "favorable"
    else:
        suitable = None
        status = "not_computable"

    missing = [key for key, value in conditions.items() if value is None]

    return {
        **_base("V15-11", "安营置阵取用日时", "明安营置阵取用日时之术"),
        "status": status,
        "computable": suitable is not None,
        "suitable": suitable,
        "conditions": conditions,
        "upper_eye_patterns": copy.deepcopy(upper),
        "lower_eye_patterns": copy.deepcopy(lower),
        "missing_inputs": missing,
        "policy": (
            "阴阳和顺、上目无掩击扶格、下目无关囚迫对、太乙与二目不在阳绝、"
            "三门具、五将发必须分别显式给定；不按宫号大小推二目左右。"
        ),
    }


def _obs_bool_map(observations: dict[str, bool] | None) -> dict[str, bool] | None:
    if observations is None:
        return None
    if not isinstance(observations, dict):
        raise TypeError("observations须为dict或None")
    unknown = sorted(set(observations) - MILITARY_OBSERVATION_KEYS)
    if unknown:
        raise ValueError(f"未知军势观测: {', '.join(unknown)}")
    result = {}
    for key, value in observations.items():
        if not isinstance(value, bool):
            raise TypeError("observations各值须为bool")
        result[key] = value
    return result


def jungshi_shengfu_pan(
    *,
    observations: dict[str, bool] | None = None,
    wind_strength: str | None = None,
    cloud_state: str | None = None,
) -> dict[str, Any]:
    """V15-14 出兵军势胜负：只消费外部军势/风云观察。"""

    obs = _obs_bool_map(observations)
    if wind_strength not in {None, "strong", "weak", "calm"}:
        raise ValueError("wind_strength须为strong/weak/calm/None")
    if cloud_state not in {None, "thick", "thin"}:
        raise ValueError("cloud_state须为thick/thin/None")

    evidence: list[dict[str, str]] = []
    if obs is not None:
        full_victory_keys = {
            "wind_from_rear", "troops_vigorous", "horses_neighing",
            "flags_toward_enemy", "drums_clear", "command_harmonious",
        }
        if all(obs.get(key) is True for key in full_victory_keys):
            evidence.append({"condition": "出军风后且人马旗鼓上下和", "effect": "大胜之象"})

        success_keys = {
            "birth_wind_direction", "sky_clear", "troops_horses_eager",
            "ranks_happy", "wind_harmonious",
        }
        if all(obs.get(key) is True for key in success_keys):
            evidence.append({"condition": "相生风且天清军和", "effect": "成功之象"})

        simple_effects = {
            "crosswind_forward": "有人助并有获粮来降之象",
            "storm_moves_to_enemy_within_three_days": "得天助、可克之象",
            "ghost_wind": "兵败之象",
            "violent_wind_rain_weak_morale": "军先败之象",
            "gloomy_chaotic_wind": "下谋上，宜设备",
            "long_overcast_without_rain": "下谋上，宜设备",
            "no_wind": "贼不可得",
            "flag_broken_by_gust": "天时不顺，上将凶",
            "flags_point_backward": "三军败、战将凶",
            "reverse_wind_blocks_flags": "大败之象",
            "weapons_flags_abnormal": "交战将凶",
            "violent_wind_collapses_camp": "主将失位、兵士叛散之象",
            "reverse_rain_not_wet_clothes": "天泣，军师大败之象",
            "sudden_rain_in_battle": "落兵，大败之兆",
        }
        for key, effect in simple_effects.items():
            if obs.get(key) is True:
                evidence.append({"condition": key, "effect": effect})

    winner = None
    wind_cloud_relation = None
    if wind_strength == "strong" and cloud_state == "thin":
        winner = "主"
        wind_cloud_relation = "风强云薄：主胜客负"
    elif wind_strength == "weak" and cloud_state == "thick":
        winner = "客"
        wind_cloud_relation = "云厚风弱：客胜主负"
    elif wind_strength is not None and cloud_state is not None:
        wind_cloud_relation = "来源未对当前强弱组合给出明确主客胜负"

    missing = []
    if obs is None:
        missing.append("observations")
    if wind_strength is None:
        missing.append("wind_strength")
    if cloud_state is None:
        missing.append("cloud_state")

    return {
        **_base("V15-14", "出兵军势胜负", "明出兵军势胜负术"),
        "status": "ok" if evidence or winner is not None else "not_computable" if missing else "undetermined",
        "computable": bool(evidence) or winner is not None,
        "observations": copy.deepcopy(obs),
        "evidence": evidence,
        "wind_strength": wind_strength,
        "cloud_state": cloud_state,
        "wind_cloud_relation": wind_cloud_relation,
        "winner": winner,
        "missing_inputs": missing,
        "policy": (
            "本条只解释显式外部风云、人马、旗鼓、营阵观察；"
            "不使用主客算长短、不从十精飞鸟或J4M观测结果自动补事实，"
            "无观测时不得生成来源未支持的默认胜负断语。"
        ),
    }


def remaining_v15_catalog() -> dict[str, Any]:
    return {
        "canonical": VERSION,
        "source_profile": SOURCE_PROFILE,
        "implemented": ["V15-01", "V15-07", "V15-08", "V15-11", "V15-14"],
        "source_limited": True,
        "old_reference_corrections": {
            "V15-01": "不把局例具体时支提升为伏兵通则",
            "V15-08": "删除来源未载的三门五将/将宫同宫分合判断",
            "V15-11": "不按宫号大小推二目左右；要求结构化条件",
            "V15-14": "删除主客算长短与无观测默认断语",
        },
        "policy": "剩余五条完成source-limited拆分；近名J4M/C8层不自动合并。",
    }
