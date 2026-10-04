"""C21 卷十五 / 卷十七军事 derived source profiles。

目标：把旧 flat 的“军事应用”“军事占断”拆成独立来源容器。
本模块不运行任何军事算法，也不与 C8 / J4M 合并。
"""

from __future__ import annotations

import copy
from typing import Any

MILITARY_DERIVED_VERSION = "taiyi-c21-military-derived-v1"

VOLUME15_PROFILE = "tongzong_volume15_military_application"
VOLUME17_PROFILE = "tongzong_volume17_military_divination"

VOLUME15_TOPICS = (
    "奇兵伏兵",
    "五陣置旗",
    "出兵稱神",
    "陳兵出鄉",
    "選將之術",
    "教兵之術",
    "隨地制變",
    "分合用兵",
    "五音風",
    "五音觀風察將",
    "安營置陣",
    "風從八卦",
    "雲氣逆順",
    "軍勢勝負",
)

VOLUME17_TOPICS = (
    "出兵用時",
    "敵國動靜",
    "間諜虛實",
    "敵使虛實",
    "敵兵來方",
    "見聞虛實",
    "討捕叛亡",
    "執囚對吏",
    "求索所得",
    "孤虛對照",
    "時計諸事",
    "占望行人",
)

# 与已存在层的重叠只做说明，绝不自动合并。
CROSS_LAYER_BOUNDARIES = {
    "volume15": {
        "J4M": {
            "奇兵伏兵": "邻近 J4M-10 推奇伏法；不得用卷十五结果回填金镜卷四。",
            "隨地制變": "邻近 J4M-08；必须保持 source profile。",
            "軍勢勝負": "邻近 J4M-11/12 风云飞鸟；卷十五综合断语不得覆盖外部观测规则。",
        },
        "C8": {
            "分合用兵": "可能消费三门五将/格局等事实；不得反写 C8 胜负链。",
            "安營置陣": "属于应用层，不是 C8-L2/L3 的替代。",
        },
    },
    "volume17": {
        "C8": {
            "敵國動靜": "敌情占断应用，不是 C8 主客动静层。",
            "求索所得": "旧代码曾与卷五孤虚对照；必须保持跨卷对照，不得合并真源。",
        },
        "J4M": {
            "出兵用時": "应用性择时，不替代 J4M 出师/主客规则。",
        },
    },
}


def _normalize_payload(
    payload: dict[str, Any] | None,
    *,
    allowed_topics: tuple[str, ...],
) -> tuple[dict[str, Any], list[str]]:
    if payload is None:
        return {}, []
    if not isinstance(payload, dict):
        raise TypeError("military profile payload须为dict")
    unknown = sorted(set(payload) - set(allowed_topics))
    return copy.deepcopy(payload), unknown


def build_volume15_military_profile(
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """保存卷十五军事应用结果，不验证旧算法答案。"""
    data, unknown = _normalize_payload(payload, allowed_topics=VOLUME15_TOPICS)
    return {
        "schema_version": "1.0",
        "canonical": MILITARY_DERIVED_VERSION,
        "profile": VOLUME15_PROFILE,
        "source_scope": "太乙统宗宝鉴_卷十五_军事应用",
        "derived_military_profile": True,
        "cross_volume_merge": False,
        "cross_c8_merge": False,
        "cross_j4m_merge": False,
        "expected_topics": list(VOLUME15_TOPICS),
        "payload": data,
        "unknown_topics": unknown,
        "complete": bool(data) and not unknown and set(data) == set(VOLUME15_TOPICS),
        "boundaries": copy.deepcopy(CROSS_LAYER_BOUNDARIES["volume15"]),
        "policy": (
            "卷十五只作为独立军事应用profile；即使术目与J4M/C8近似，"
            "也不得自动等价、覆盖或反写。"
        ),
    }


def build_volume17_military_profile(
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """保存卷十七军事占断结果，不验证旧算法答案。"""
    data, unknown = _normalize_payload(payload, allowed_topics=VOLUME17_TOPICS)
    return {
        "schema_version": "1.0",
        "canonical": MILITARY_DERIVED_VERSION,
        "profile": VOLUME17_PROFILE,
        "source_scope": "太乙统宗宝鉴_卷十七_军事占断",
        "derived_military_profile": True,
        "cross_volume_merge": False,
        "cross_c8_merge": False,
        "cross_j4m_merge": False,
        "expected_topics": list(VOLUME17_TOPICS),
        "payload": data,
        "unknown_topics": unknown,
        "complete": bool(data) and not unknown and set(data) == set(VOLUME17_TOPICS),
        "boundaries": copy.deepcopy(CROSS_LAYER_BOUNDARIES["volume17"]),
        "policy": (
            "卷十七只作为独立军事占断profile；敌国动静、求索等应用层"
            "不得冒充C8/J4M同名或近名规则。"
        ),
    }


def build_military_derived_source_variants(
    *,
    volume15: dict[str, Any] | None = None,
    volume17: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """返回可合入 pan_v2.source_variants 的军事 derived 容器。"""
    return {
        "military_derived": {
            "schema_version": "1.0",
            "canonical": MILITARY_DERIVED_VERSION,
            "tongzong_volume15": build_volume15_military_profile(volume15),
            "tongzong_volume17": build_volume17_military_profile(volume17),
            "cross_volume_merge": False,
            "policy": "卷十五与卷十七分别保存；禁止与C8/J4M或彼此自动合并。",
        }
    }
