"""C17 P0 来源隔离容器。

只组合已经结构化的来源结果；不调用格局或军事算法，不自动选择“正确版本”。
"""

from __future__ import annotations

import copy
from typing import Any

from .jinjing_v4_military import J4M_RULESET, J4M_SOURCE_PROFILE

SOURCE_PROFILE_VERSION = "taiyi-c17-source-profiles-v1"

PATTERN_PROFILE_KEYS = (
    "tongzong_volume4",
    "jinjing_geju",
)

MILITARY_PROFILE_KEYS = (
    "tongzong_volume5",
    "jinjing_siku_volume4",
    "jingyou_fuying_volume4",
    "c8_upstream",
)

MILITARY_P0_CROSSWALK = {
    "three_doors": {
        "legacy_name": "推三门具不具",
        "jinjing_rule_id": "J4M-01",
        "jingyou_rule_id": "JF4M-01",
        "c8_relation": "C8-L2 consumes an upstream three_doors fact",
        "c8_equivalent_formula": False,
        "policy": "J4M-01若未实现，不得用C8归一化层冒充金镜公式。",
    },
    "five_generals": {
        "legacy_name": "推五将发不发",
        "jinjing_rule_id": "J4M-02",
        "jingyou_rule_id": "JF4M-02",
        "c8_relation": "C8-L2 consumes an upstream five_generals fact",
        "c8_equivalent_formula": False,
        "policy": "J4M-02若未实现，不得用C8归一化层冒充金镜公式。",
    },
    "host_guest_relation": {
        "legacy_name": "推主客相关法",
        "jinjing_rule_id": "J4M-03",
        "jingyou_rule_id": "JF4M-03",
        "c8_relation": "C8-L3 is host/guest movement ordering only; adjacent topic, not replacement",
        "c8_equivalent_formula": False,
        "policy": "J4M-03主客相关法与C8-L3主客动静不得合并。",
    },
}


def _copy_profiles(profiles: dict[str, Any] | None, *, allowed: tuple[str, ...]) -> dict[str, Any]:
    if profiles is None:
        return {}
    if not isinstance(profiles, dict):
        raise TypeError("profiles须为dict")
    unknown = sorted(set(profiles) - set(allowed))
    if unknown:
        raise ValueError(f"未知source profile: {', '.join(unknown)}")
    return {
        key: copy.deepcopy(value)
        for key, value in profiles.items()
        if value is not None
    }


def build_pattern_source_variants(*, profiles: dict[str, Any] | None = None) -> dict[str, Any]:
    """保存统宗卷四与金镜格局结果，不静默合并。

    jinjing_geju 指目标仓库 source-limited 格局引擎：
    主体来源卷三，值事门相关格局另引用卷四。
    """
    copied = _copy_profiles(profiles, allowed=PATTERN_PROFILE_KEYS)
    return {
        "schema_version": "1.0",
        "canonical": SOURCE_PROFILE_VERSION,
        "category": "patterns",
        "profiles": copied,
        "canonical_selected": None,
        "cross_source_merge": False,
        "profile_notes": {
            "tongzong_volume4": "旧参考pan注释《太乙统宗宝鉴》卷四释格局。",
            "jinjing_geju": "目标仓库金镜格局引擎：主体卷三，值事门相关规则引用卷四。",
        },
        "policy": "来源并列保存；除非另有显式比较层，不自动合并事件或断语。",
    }


def _military_topic(name: str, profiles: dict[str, Any] | None) -> dict[str, Any]:
    copied = _copy_profiles(profiles, allowed=MILITARY_PROFILE_KEYS)
    crosswalk = copy.deepcopy(MILITARY_P0_CROSSWALK[name])
    if name == "host_guest_relation" and "c8_upstream" in copied:
        raise ValueError("J4M-03没有C8直接等价实现；不得登记c8_upstream为替代profile")
    return {
        "profiles": copied,
        "canonical_selected": None,
        "cross_source_merge": False,
        "crosswalk": crosswalk,
    }


def build_military_p0_source_variants(
    *,
    three_doors_profiles: dict[str, Any] | None = None,
    five_generals_profiles: dict[str, Any] | None = None,
    host_guest_relation_profiles: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """保存P0三项军事来源，不宣称不同来源公式等价。"""
    return {
        "schema_version": "1.0",
        "canonical": SOURCE_PROFILE_VERSION,
        "category": "military",
        "three_doors": _military_topic("three_doors", three_doors_profiles),
        "five_generals": _military_topic("five_generals", five_generals_profiles),
        "host_guest_relation": _military_topic(
            "host_guest_relation", host_guest_relation_profiles
        ),
        "cross_source_merge": False,
        "policy": (
            "J4M、《福应经》JF4M、统宗与C8并列；不同古籍profile不互补。"
            "C8只可登记其真实角色，不得作为古籍公式替身。"
        ),
    }


def build_p0_source_variants(
    *,
    pattern_profiles: dict[str, Any] | None = None,
    three_doors_profiles: dict[str, Any] | None = None,
    five_generals_profiles: dict[str, Any] | None = None,
    host_guest_relation_profiles: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """构建可直接传入 build_pan_v2(source_variants=...) 的P0容器。"""
    return {
        "patterns": build_pattern_source_variants(profiles=pattern_profiles),
        "military": build_military_p0_source_variants(
            three_doors_profiles=three_doors_profiles,
            five_generals_profiles=five_generals_profiles,
            host_guest_relation_profiles=host_guest_relation_profiles,
        ),
    }



def build_weather_bird_source_variant(
    *,
    jinjing_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """保存 J4M-11 风云飞鸟外部观测结果。

    旧 pan.flybird_wl 仅按盘内飞鸟位置生成断语，不得作为本 profile 替代。
    """
    profiles: dict[str, Any] = {}
    if jinjing_result is not None:
        if not isinstance(jinjing_result, dict):
            raise TypeError("jinjing_result须为dict或None")
        if jinjing_result.get("source_profile") != J4M_SOURCE_PROFILE:
            raise ValueError("J4M-11 source_profile mismatch")
        if jinjing_result.get("ruleset") != J4M_RULESET:
            raise ValueError("J4M-11 ruleset mismatch")
        if jinjing_result.get("rule_id") != "J4M-11":
            raise ValueError("jinjing_result必须来自J4M-11")
        profiles["jinjing_siku_volume4"] = copy.deepcopy(jinjing_result)

    return {
        "schema_version": "1.0",
        "canonical": SOURCE_PROFILE_VERSION,
        "category": "military_weather_bird_support",
        "profiles": profiles,
        "canonical_selected": None,
        "cross_source_merge": False,
        "observation_required": True,
        "legacy_flat_auto_promoted": False,
        "policy": (
            "只接经J4M-11验证的外部风云飞鸟观测结果；"
            "旧flybird_wl盘内推断不得自动升为source profile。"
        ),
    }
