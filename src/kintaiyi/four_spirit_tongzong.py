"""C92 《太乙统宗宝鉴》卷七四神太乙水神位置与克贼/战克显式层。

本层从旧分支 four_taiyi.py 回收两项，但按现行来源边界重写：
1. 统宗卷七四神位置周期；
2. 古法明列的克贼 / 战克组合。

不恢复旧分支的“三元起宫”默认算法；《太乙秘书》相关起法只登记为
source variant，待独立校勘。
"""

from __future__ import annotations

import copy
from typing import Any

from .state_spirit_cycles import TWELVE_PALACES
from .taiyi_rules import BRANCHES, integer

C92_VERSION = "taiyi-c92-four-spirit-tongzong-v1"

SOURCE_WITNESS = {
    "primary": {
        "work": "太乙统宗宝鉴",
        "witness_volumes": [6, 7],
        "section": "明四神太乙水宿所主术",
        "position_formula": {
            "big_cycle": 360,
            "small_cycle": 36,
            "years_per_palace": 3,
            "start_palace": 1,
            "palace_order": list(TWELVE_PALACES),
            "direction": "forward",
        },
        "special_classification": {
            "克贼": [
                {"year_branches": ["辰", "戌"], "palaces": [5, 9]},
                {"year_branches": ["丑", "未"], "palaces": [7, 3]},
            ],
            "战克": [
                {"year_branches": ["巳", "午"], "palaces": [2, 9]},
            ],
        },
    },
    "later_variant": {
        "work": "太乙秘书",
        "status": "source_variant_not_implemented",
        "observed": [
            "四神三年一移、三十六年一周",
            "另有起自玉堂宫 / 中下元起法叙述",
        ],
        "reason": (
            "与旧分支 four_taiyi.py 的 yuan 起点表不完全一致；"
            "未完成独立三元校勘前，不恢复旧 yuan 参数为 canonical。"
        ),
    },
}

LEGACY_RECOVERY = {
    "branch": "codex/c1-c7-canonical",
    "file": "src/kintaiyi/four_taiyi.py",
    "reused_concepts": [
        "四神十二运行宫",
        "三年一宫",
        "克贼/战克显式组合",
    ],
    "not_reused": [
        "旧 four_taiyi_position(..., yuan=...) 三元起宫默认算法",
        "自动同宫 effects",
        "五福同域自动 effects",
    ],
    "policy": "旧实现只作恢复线索；现行结果以直接来源层为准。",
}


def four_spirit_position(accumulated_count: int) -> dict[str, Any]:
    """按《统宗》卷七直接公式求四神太乙水神所在十二宫。"""
    count = integer(accumulated_count, 1)

    big_remainder = count % 360
    big_cycle_year = big_remainder or 360

    small_remainder = big_cycle_year % 36
    small_cycle_year = small_remainder or 36

    zero_index = small_cycle_year - 1
    palace_offset = zero_index // 3
    year_in_palace = zero_index % 3 + 1

    palace = TWELVE_PALACES[palace_offset]

    return {
        "schema_version": "1.0",
        "canonical": C92_VERSION,
        "rule_id": "C92-FOUR-SPIRIT-POSITION",
        "source_profile": "tongzong_volume7_four_spirit",
        "spirit": "四神",
        "element": "水",
        "accumulated_count": count,
        "big_cycle": 360,
        "big_cycle_remainder": big_remainder,
        "big_cycle_year": big_cycle_year,
        "small_cycle": 36,
        "small_cycle_remainder": small_remainder,
        "small_cycle_year": small_cycle_year,
        "years_per_palace": 3,
        "palace_step": palace_offset + 1,
        "year_in_palace": year_in_palace,
        "start_palace": 1,
        "palace_order": list(TWELVE_PALACES),
        "palace": palace,
        "same_palace_omens_applied": False,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "legacy_recovery": copy.deepcopy(LEGACY_RECOVERY),
        "policy": (
            "只实现《统宗》卷七起一宫、36年小周、三年一宫的连续位置；"
            "不接旧分支未经重新校勘的三元yuan起法。"
        ),
    }


def four_spirit_conflict_classification(
    *,
    year_branch: str,
    palace: int | str,
) -> dict[str, Any]:
    """解释古法明列的四神克贼 / 战克组合。

    只消费显式太岁支与四神所在运行宫，不自动调用位置函数。
    未列组合返回 pending，不按五行常识外推。
    """
    if not isinstance(year_branch, str) or year_branch not in BRANCHES:
        raise ValueError("year_branch须为十二地支")

    if isinstance(palace, bool):
        raise TypeError("palace须为十二运行宫")
    if palace not in TWELVE_PALACES:
        raise ValueError("palace须为1..9或绛宫/明堂/玉堂")

    classification = None
    if year_branch in ("辰", "戌") and palace in (5, 9):
        classification = "克贼"
    elif year_branch in ("丑", "未") and palace in (7, 3):
        classification = "克贼"
    elif year_branch in ("巳", "午") and palace in (2, 9):
        classification = "战克"

    if classification is None:
        status = "source_not_listed"
        effects: list[str] = []
        pending = ["《统宗》古法未在本条明列该太岁支×四神宫组合；不外推"]
    else:
        status = "direct_classification"
        effects = (
            ["水旱", "兵盗", "饥荒"]
            if classification == "克贼"
            else ["尊卑相凌", "上下失序", "凶咎生"]
        )
        pending = []

    return {
        "schema_version": "1.0",
        "canonical": C92_VERSION,
        "rule_id": "C92-FOUR-SPIRIT-CONFLICT-CLASSIFICATION",
        "source_profile": "tongzong_volume7_four_spirit",
        "year_branch": year_branch,
        "palace": palace,
        "classification": classification,
        "effects": effects,
        "status": status,
        "pending": pending,
        "auto_position_lookup_used": False,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "legacy_recovery": copy.deepcopy(LEGACY_RECOVERY),
        "policy": (
            "克贼/战克只按正文列出的显式组合命中；"
            "未列组合不从五行生克自动补判。"
        ),
    }


def c92_catalog() -> dict[str, Any]:
    return {
        "canonical": C92_VERSION,
        "source_profile": "tongzong_volume7_four_spirit",
        "position_rule": "C92-FOUR-SPIRIT-POSITION",
        "classification_rule": "C92-FOUR-SPIRIT-CONFLICT-CLASSIFICATION",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "legacy_recovery": copy.deepcopy(LEGACY_RECOVERY),
    }
