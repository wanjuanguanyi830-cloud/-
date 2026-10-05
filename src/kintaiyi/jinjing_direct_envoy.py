"""C121 《太乙金镜式经》卷一阴阳遁太乙直使六纪锚点层。

本层保存“推求阳遁太乙直使法 / 求阴遁太乙直使之法”直接列出的
六纪夜半甲子锚点，以及正文明确的移动原则。

重要边界：
- 王希明在正文后明确批评张良固定日法“有定准、气无盈缩”的问题；
- 因此六纪表保存为直接见证锚点，不把整套旧定日法无条件提升为全年连续 canonical；
- 太乙3时一移、天目1时一移且乾坤重留等句先保留为 movement metadata；
- 在“气应早晚断在临时”的替代规则完全重建前，不实现自动连续推步。
"""

from __future__ import annotations

import copy
from typing import Any

C121_VERSION = "taiyi-c121-jinjing-direct-envoy-anchors-v1"

PALACE_PATH = (1, 2, 3, 4, 6, 7, 8, 9)

YANG_ANCHORS = {
    1: {"taiyi_palace": 1, "tianmu": "武德", "jishen": "寅", "period_label": "二甲仲辰"},
    2: {"taiyi_palace": 6, "tianmu": "地主", "jishen": "寅", "period_label": "二己孟辰"},
    3: {"taiyi_palace": 1, "tianmu": "大炅", "jishen": "寅", "period_label": "二甲季辰"},
    4: {"taiyi_palace": 6, "tianmu": "武德", "jishen": "寅", "period_label": "二己仲辰"},
    5: {"taiyi_palace": 1, "tianmu": "地主", "jishen": "寅", "period_label": "二甲孟辰"},
    6: {"taiyi_palace": 6, "tianmu": "大炅", "jishen": "寅", "period_label": "二己季辰"},
}

YIN_ANCHORS = {
    1: {"taiyi_palace": 9, "tianmu": "吕申", "jishen": "申", "period_label": "二甲仲辰"},
    2: {"taiyi_palace": 4, "tianmu": "大威", "jishen": "申", "period_label": "二己孟辰"},
    3: {"taiyi_palace": 9, "tianmu": "阴德", "jishen": "申", "period_label": "二甲季辰"},
    4: {"taiyi_palace": 4, "tianmu": "吕申", "jishen": "申", "period_label": "二己仲辰"},
    5: {"taiyi_palace": 9, "tianmu": "大威", "jishen": "申", "period_label": "二甲孟辰"},
    6: {"taiyi_palace": 4, "tianmu": "阴德", "jishen": "申", "period_label": "二己季辰"},
}

MOVEMENT_RULES = {
    "阳遁": {
        "taiyi": {
            "start_basis": "冬至气应",
            "direction": "forward",
            "path": list(PALACE_PATH),
            "center_five_used": False,
            "source_statements": ["太乙直使三时一移", "顺行八宫不居中五"],
        },
        "tianmu": {
            "direction": "left_on_sixteen_gods",
            "source_statements": [
                "一时一移左行十六神",
                "乾坤二宫二时一移",
                "乾为天门、坤为人门",
            ],
        },
        "jishen": {
            "start_branch": "寅",
            "direction": "right_on_twelve_branches",
        },
    },
    "阴遁": {
        "taiyi": {
            "start_basis": "夏至气应",
            "direction": "reverse",
            "path": list(reversed(PALACE_PATH)),
            "center_five_used": False,
            "source_statements": ["逆历巽离坤兑四卦八宫", "不游中五"],
        },
        "tianmu": {
            "direction": "reverse_source_profile",
            "source_statements": ["六纪锚点直接列吕申/大威/阴德"],
        },
        "jishen": {
            "start_branch": "申",
            "direction": "source_profile_reverse_context",
        },
    },
}

SOURCE_WITNESS = {
    "work": "太乙金镜式经",
    "volume": 1,
    "sections": [
        "推求阳遁太乙直使法",
        "求阴遁太乙直使之法",
    ],
    "direct_core": [
        "阳遁冬至起乾，六甲夜半一宫、六己夜半六宫",
        "阳遁六纪太乙/天目/计神锚点表",
        "阴遁夏至起巽，六甲夜半九宫、六己夜半四宫",
        "阴遁六纪太乙/天目/计神锚点表",
        "太乙不游中五",
    ],
    "policy": "六纪锚点与移动句保存原文层；王希明修正后的气应法未完全重建前不做全年自动连续推步。",
}

WANG_XIMING_BOUNDARY = {
    "status": "author_revision_over_fixed_zhangliang_day_scheme",
    "direct_summary": (
        "王希明指出张良六纪定日法有气应早晚问题，主张以冬至/夏至实际气应为元，"
        "不拘阳日阴日孟仲季辰；气应早晚断在临时。"
    ),
    "continuous_runtime_implemented": False,
    "reason": (
        "正文给出批评与原则，但完整从实际气应时刻到六纪连续位置的替代计算链"
        "尚未在C121独立校定。"
    ),
}


def _period(period: int) -> int:
    if isinstance(period, bool) or not isinstance(period, int):
        raise TypeError("period须为1..6整数")
    if not 1 <= period <= 6:
        raise ValueError("period须为1..6")
    return period


def direct_envoy_anchor(dun: str, period: int) -> dict[str, Any]:
    p = _period(period)
    if dun in ("阳", "阳遁"):
        canonical_dun = "阳遁"
        row = YANG_ANCHORS[p]
        solstice = "冬至"
    elif dun in ("阴", "阴遁"):
        canonical_dun = "阴遁"
        row = YIN_ANCHORS[p]
        solstice = "夏至"
    else:
        raise ValueError("dun须为阳遁或阴遁")

    return {
        "schema_version": "1.0",
        "canonical": C121_VERSION,
        "rule_id": "C121-DIRECT-ENVOY-ANCHOR",
        "source_profile": "jinjing_volume1_direct_envoy",
        "dun": canonical_dun,
        "solstice_basis": solstice,
        "period": p,
        "period_label": row["period_label"],
        "anchor_time": "夜半甲子",
        "taiyi_palace": row["taiyi_palace"],
        "tianmu": row["tianmu"],
        "jishen": row["jishen"],
        "movement_rules": copy.deepcopy(MOVEMENT_RULES[canonical_dun]),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "wang_ximing_boundary": copy.deepcopy(WANG_XIMING_BOUNDARY),
    }


def direct_envoy_movement_catalog(dun: str) -> dict[str, Any]:
    if dun in ("阳", "阳遁"):
        canonical_dun = "阳遁"
    elif dun in ("阴", "阴遁"):
        canonical_dun = "阴遁"
    else:
        raise ValueError("dun须为阳遁或阴遁")
    return {
        "schema_version": "1.0",
        "canonical": C121_VERSION,
        "rule_id": "C121-DIRECT-ENVOY-MOVEMENT",
        "dun": canonical_dun,
        "rules": copy.deepcopy(MOVEMENT_RULES[canonical_dun]),
        "continuous_runtime_implemented": False,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "wang_ximing_boundary": copy.deepcopy(WANG_XIMING_BOUNDARY),
    }


def c121_catalog() -> dict[str, Any]:
    return {
        "canonical": C121_VERSION,
        "rule_ids": [
            "C121-DIRECT-ENVOY-ANCHOR",
            "C121-DIRECT-ENVOY-MOVEMENT",
        ],
        "yang_anchors": copy.deepcopy(YANG_ANCHORS),
        "yin_anchors": copy.deepcopy(YIN_ANCHORS),
        "movement_rules": copy.deepcopy(MOVEMENT_RULES),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "wang_ximing_boundary": copy.deepcopy(WANG_XIMING_BOUNDARY),
    }
