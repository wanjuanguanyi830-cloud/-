"""C58 十精太乙云气：初移宫云色时变与天气形态观察层。

与 C57 分层：
- C57：十精/太乙/天目等显式合会；
- C58：太乙初移宫时真实云气观察、天气厚薄色象、旱雨取阴阳与旺相速变。

与 C51 分层：
- C51：天子初登位日月旁云气；
- C58：太乙初移宫候云气。
"""

from __future__ import annotations

import copy
from typing import Any

C58_VERSION = "taiyi-c58-ten-essence-cloud-observations-v1"

SOURCE_WITNESS = {
    "primary": {
        "work": "太乙统宗宝鉴",
        "section": "明十精太乙云气所主术",
        "witness_volumes": [18, 20],
    },
    "collation": [
        {
            "work": "太乙金镜式经",
            "section": "推候十精太乙云气法",
            "role": "direct_parallel_collation",
        },
        {
            "work": "武经总要",
            "section": "推候十精太乙云气",
            "role": "independent_early_collation",
        },
        {
            "work": "三才世纬",
            "role": "later_collation",
        },
    ],
}

COLOR_TIMING_RULES = {
    "青": {
        "counts": [3, 4],
        "change_branch_period": ["寅", "卯"],
        "status": "primary_direct",
    },
    "赤": {
        "counts": [9, 2],
        "change_branch_period": ["巳", "午"],
        "status": "collation_supported_primary_online_gap",
        "witness": {
            "tongzong_online": "当前OCR/图像转写未见完整赤色句",
            "jinjing": "赤色，九二，巳午",
            "wujing_zongyao": "赤色，九二，巳午",
        },
    },
    "白": {
        "counts": [7, 6],
        "change_branch_period": ["申", "酉"],
        "status": "primary_direct",
    },
    "黑": {
        "counts": [1, 8],
        "change_branch_period": ["亥", "子"],
        "status": "primary_direct",
    },
}

LEGACY_COLOR_AUDIT = {
    "legacy_yunqi_table": {
        "white_counts": [7, 6],
        "legacy_change_branch_period": ["亥", "子"],
        "canonical_change_branch_period": ["申", "酉"],
        "canonical_equivalent": False,
        "reason": "统宗、金镜、武经均支持白7/6→申酉；旧表误配亥子。",
    },
    "红": {
        "status": "legacy_color_label",
        "canonical_color": "赤",
        "runtime_alias_enabled": False,
    },
}

OBSERVATION_WINDOWS = {
    "日计": {
        "initial_move_offset": 0,
        "allowed_slots": ["日出", "日午", "日晡"],
        "later_offsets": [1, 2],
        "later_status": "不候",
    },
    "时计": {
        "initial_move_offset": 0,
        "allowed_slots": ["初移宫时"],
        "later_offsets": [1, 2],
        "later_status": "不占",
    },
}

WEATHER_TEXTURE_RULES = {
    "纯厚": {
        "effects": ["雨"],
        "status": "direct_parallel",
    },
    "华薄": {
        "effects": ["风"],
        "status": "direct_parallel",
    },
    "黄雾": {
        "effects": ["晕"],
        "status": "direct_parallel",
    },
    "黑赤": {
        "effects": ["风"],
        "status": "stable_core",
        "witness_variants": {
            "jinjing": "风",
            "wujing_zongyao": "风",
            "sancai_shiwei": "风热",
        },
    },
    "青白": {
        "effects": ["寒"],
        "status": "stable_core",
        "witness_variants": {
            "jinjing": "寒",
            "wujing_zongyao": "寒",
            "sancai_shiwei": "风寒",
        },
    },
    "凝润": {
        "effects": ["雾雨"],
        "status": "direct_parallel",
    },
}

CLOUD_FORM_RULES = {
    "如扫": {
        "effects": ["晴"],
        "status": "direct",
    },
    "文彩轮囷萧索": {
        "effects": ["大晴"],
        "status": "collated_phrase",
        "witness_variants": {
            "tongzong_online": "文彩萧索",
            "jinjing": "文彩轮囷萧索",
            "wujing_zongyao": "文彩轮菌萧索",
        },
    },
}

FLYBIRD_TAIYI_WIND_VARIANT = {
    "status": "source_variant_unresolved",
    "tongzong_online": "风从下来",
    "jinjing": "风从其下来",
    "wujing_zongyao": "风从其上来",
    "canonical_selected": None,
    "runtime_direction_applied": False,
}

GENERAL_MODIFIERS = {
    "旱": {
        "divination_mode": "阳",
        "source_rule": "天旱常以阳占之",
    },
    "雨": {
        "divination_mode": "阴",
        "source_rule": "天雨常以阴占之",
    },
    "旺相": {
        "change_speed": "疾速",
        "source_rule": "若得旺相气则其变疾而速",
    },
}

C51_BOUNDARY = {
    "same_cloud_vocabulary": True,
    "same_observation_event": False,
    "c51": "天子初登位日月旁云气",
    "c58": "太乙初移宫候云气",
    "merge_allowed": False,
}


def _validate_count(value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("day_time_count须为整数")
    return value


def initial_move_cloud_timing(
    *,
    cloud_color: str,
    day_time_count: int,
    calculation_scope: str,
    observation_slot: str,
    move_offset: int = 0,
) -> dict[str, Any]:
    """解释太乙初移宫日/时的云色计数与变发支时。"""
    if cloud_color not in COLOR_TIMING_RULES:
        if cloud_color == "红":
            raise ValueError("C58 canonical云色用‘赤’，不默认把旧‘红’静默归一")
        raise ValueError("cloud_color须为青/赤/白/黑")
    count = _validate_count(day_time_count)
    if calculation_scope not in OBSERVATION_WINDOWS:
        raise ValueError("calculation_scope须为日计/时计")
    if not isinstance(move_offset, int) or isinstance(move_offset, bool) or move_offset < 0:
        raise ValueError("move_offset须为非负整数")

    window = OBSERVATION_WINDOWS[calculation_scope]
    if move_offset != 0:
        return {
            "schema_version": "1.0",
            "canonical": C58_VERSION,
            "rule_id": "C58-CLOUD-TIMING",
            "source_profile": "tongzong_ten_essences_cloud_observation",
            "status": "outside_source_observation_window",
            "calculation_scope": calculation_scope,
            "move_offset": move_offset,
            "observation_slot": observation_slot,
            "cloud_color": cloud_color,
            "day_time_count": count,
            "matched": False,
            "change_branch_period": None,
            "policy": (
                f"{calculation_scope}只候太乙初移宫本{ '日' if calculation_scope == '日计' else '时' }；"
                "余二日/时不候占。"
            ),
        }

    if observation_slot not in window["allowed_slots"]:
        raise ValueError(
            f"{calculation_scope} observation_slot须为"
            + "/".join(window["allowed_slots"])
        )

    rule = COLOR_TIMING_RULES[cloud_color]
    matched = count in rule["counts"]
    return {
        "schema_version": "1.0",
        "canonical": C58_VERSION,
        "rule_id": "C58-CLOUD-TIMING",
        "source_profile": "tongzong_ten_essences_cloud_observation",
        "status": "direct_match" if matched else "count_not_matched_by_color_rule",
        "calculation_scope": calculation_scope,
        "move_offset": move_offset,
        "observation_slot": observation_slot,
        "cloud_color": cloud_color,
        "day_time_count": count,
        "expected_counts": list(rule["counts"]),
        "matched": matched,
        "change_branch_period": (
            list(rule["change_branch_period"]) if matched else None
        ),
        "source_status": rule["status"],
        "witness": copy.deepcopy(rule.get("witness")),
        "legacy_color_audit": copy.deepcopy(LEGACY_COLOR_AUDIT),
        "c51_boundary": copy.deepcopy(C51_BOUNDARY),
        "policy": (
            "只按显式云色+日时计数解释变发支时；"
            "不从云色推十精合会，也不与C51登位旁云合并。"
        ),
    }


def weather_observation_omens(
    *,
    weather_texture: str | None = None,
    cloud_form: str | None = None,
    current_weather: str | None = None,
    qi_state: str | None = None,
    flybird_taiyi_conjoined: bool | None = None,
) -> dict[str, Any]:
    """解释天气厚薄/色象与总括修饰；全部观察必须显式输入。"""
    if weather_texture is not None and weather_texture not in WEATHER_TEXTURE_RULES:
        raise ValueError(
            "weather_texture须为纯厚/华薄/黄雾/黑赤/青白/凝润或None"
        )
    if cloud_form is not None and cloud_form not in CLOUD_FORM_RULES:
        raise ValueError("cloud_form须为如扫/文彩轮囷萧索或None")
    if current_weather not in (None, "旱", "雨"):
        raise ValueError("current_weather须为旱/雨或None")
    if qi_state not in (None, "旺相", "非旺相", "休囚"):
        raise ValueError("qi_state须为旺相/非旺相/休囚或None")
    if flybird_taiyi_conjoined not in (None, True, False):
        raise TypeError("flybird_taiyi_conjoined须为bool或None")

    matched = []
    if weather_texture is not None:
        rule = WEATHER_TEXTURE_RULES[weather_texture]
        matched.append({
            "kind": "weather_texture",
            "observation": weather_texture,
            "effects": copy.deepcopy(rule["effects"]),
            "source_status": rule["status"],
            "witness_variants": copy.deepcopy(rule.get("witness_variants")),
        })
    if cloud_form is not None:
        rule = CLOUD_FORM_RULES[cloud_form]
        matched.append({
            "kind": "cloud_form",
            "observation": cloud_form,
            "effects": copy.deepcopy(rule["effects"]),
            "source_status": rule["status"],
            "witness_variants": copy.deepcopy(rule.get("witness_variants")),
        })

    divination_mode = (
        GENERAL_MODIFIERS[current_weather]["divination_mode"]
        if current_weather is not None
        else None
    )
    change_speed = (
        GENERAL_MODIFIERS["旺相"]["change_speed"]
        if qi_state == "旺相"
        else None
    )

    flybird_variant = (
        copy.deepcopy(FLYBIRD_TAIYI_WIND_VARIANT)
        if flybird_taiyi_conjoined is True
        else None
    )

    provided = any([
        weather_texture is not None,
        cloud_form is not None,
        current_weather is not None,
        qi_state is not None,
        flybird_taiyi_conjoined is not None,
    ])
    return {
        "schema_version": "1.0",
        "canonical": C58_VERSION,
        "rule_id": "C58-WEATHER-OBSERVATION",
        "source_profile": "tongzong_ten_essences_cloud_observation",
        "status": "explicit_observation" if provided else "not_computable",
        "matched_omens": matched,
        "current_weather": current_weather,
        "divination_mode": divination_mode,
        "qi_state": qi_state,
        "change_speed": change_speed,
        "flybird_taiyi_conjoined": flybird_taiyi_conjoined,
        "flybird_wind_direction_variant": flybird_variant,
        "flybird_wind_direction": None,
        "c51_boundary": copy.deepcopy(C51_BOUNDARY),
        "auto_weather_inference_used": False,
        "policy": (
            "天气厚薄/色象、旱雨背景、旺相必须来自真实外部观察或上游显式证据。"
            "飞鸟合太乙的风向见证‘上来/下来’冲突，故不输出方向。"
        ),
    }


def c58_catalog() -> dict[str, Any]:
    return {
        "canonical": C58_VERSION,
        "source_profile": "tongzong_ten_essences_cloud_observation",
        "color_timing_rules": copy.deepcopy(COLOR_TIMING_RULES),
        "observation_windows": copy.deepcopy(OBSERVATION_WINDOWS),
        "weather_texture_rules": copy.deepcopy(WEATHER_TEXTURE_RULES),
        "cloud_form_rules": copy.deepcopy(CLOUD_FORM_RULES),
        "flybird_taiyi_wind_variant": copy.deepcopy(FLYBIRD_TAIYI_WIND_VARIANT),
        "general_modifiers": copy.deepcopy(GENERAL_MODIFIERS),
        "legacy_color_audit": copy.deepcopy(LEGACY_COLOR_AUDIT),
        "c51_boundary": copy.deepcopy(C51_BOUNDARY),
    }
