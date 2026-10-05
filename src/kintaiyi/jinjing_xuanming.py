"""C116 《太乙金镜式经》卷一“推太乙玄命法”。

只实现正文直接列出的身份 -> 玄命所主映射。
不从官阶、命理、行年或其他模块自动推导额外吉凶。
"""

from __future__ import annotations

import copy
from typing import Any

C116_VERSION = "taiyi-c116-jinjing-xuanming-v1"

ROLE_TO_XUANMING = {
    "天子": {"target": "天乙", "target_type": "twelve_general"},
    "皇后": {"target": "天后", "target_type": "twelve_general"},
    "公侯": {"target": "太常", "target_type": "twelve_general"},
    "将军": {"target": "勾陈", "target_type": "twelve_general"},
    "九牧": {"target": "螣蛇", "target_type": "twelve_general"},
    "常侍": {"target": "天空", "target_type": "twelve_general"},
    "二千石": {"target": "青龙", "target_type": "twelve_general"},
    "大夫": {"target": "朱雀", "target_type": "twelve_general"},
    "吏士": {"target": "朱雀", "target_type": "twelve_general"},
    "庶人": {"target": "行年", "target_type": "annual_position"},
}

ROLE_ALIASES = {
    "二干石": "二千石",
}

SOURCE_WITNESS = {
    "work": "太乙金镜式经",
    "volume": 1,
    "section": "推太乙玄命法",
    "direct_table": [
        "天子玄命在天乙",
        "皇后玄命在天后",
        "公侯玄命在太常",
        "将军玄命在勾陈",
        "九牧玄命在螣蛇",
        "常侍玄命在天空",
        "二千石玄命在青龙",
        "大夫吏士玄命在朱雀",
        "庶人玄命在行年",
    ],
    "policy": "只保存身份到玄命对象的直接映射，不由映射本身生成吉凶。",
}


def _normalize_role(role: str) -> str:
    if not isinstance(role, str):
        raise TypeError("role须为字符串")
    role = ROLE_ALIASES.get(role, role)
    if role not in ROLE_TO_XUANMING:
        raise ValueError("未知C116身份")
    return role


def xuanming_for_role(role: str) -> dict[str, Any]:
    canonical_role = _normalize_role(role)
    item = ROLE_TO_XUANMING[canonical_role]
    return {
        "schema_version": "1.0",
        "canonical": C116_VERSION,
        "rule_id": "C116-XUANMING-ROLE",
        "source_profile": "jinjing_volume1_xuanming",
        "role": canonical_role,
        "input_role": role,
        "xuanming_target": item["target"],
        "target_type": item["target_type"],
        "verdict": None,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "policy": "玄命表只给所主位置；旺相/相生等条件由考时层另行解释。",
    }


def xuanming_matches(role: str, occupied_target: str | None) -> dict[str, Any]:
    expected = xuanming_for_role(role)
    if occupied_target is None:
        return {
            **expected,
            "occupied_target": None,
            "matches": None,
            "status": "target_unchecked",
            "pending": ["须显式给当前所临天将/行年位置"],
        }
    if not isinstance(occupied_target, str):
        raise TypeError("occupied_target须为字符串或None")
    return {
        **expected,
        "occupied_target": occupied_target,
        "matches": occupied_target == expected["xuanming_target"],
        "status": "matched" if occupied_target == expected["xuanming_target"] else "not_matched",
        "pending": [],
    }


def c116_catalog() -> dict[str, Any]:
    return {
        "canonical": C116_VERSION,
        "rule_id": "C116-XUANMING-ROLE",
        "role_to_xuanming": copy.deepcopy(ROLE_TO_XUANMING),
        "role_aliases": copy.deepcopy(ROLE_ALIASES),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
    }
