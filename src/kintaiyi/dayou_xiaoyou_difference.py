"""C49 《太乙统宗宝鉴》太、小游行宫卦不同术。

本层只比较 C41 太游与 C47 小游的内卦职责：
- 太游：36年一内卦，得乾天之策；
- 小游：24年一内卦，得坤地之策。

当前内卦相同/不同只作派生结构事实，不生成吉凶。
"""

from __future__ import annotations

import copy
from typing import Any

C49_VERSION = "taiyi-c49-dayou-xiaoyou-difference-v1"

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "section": "明太、小游行宫卦不同术",
    "online_witness_volume": 10,
    "volume_status": "witness_volume_boundary_variant",
    "direct_rules": {
        "dayou": {
            "years_per_inner_trigram": 36,
            "symbolic_ce": "乾天之策",
        },
        "xiaoyou": {
            "years_per_inner_trigram": 24,
            "symbolic_ce": "坤地之策",
        },
    },
    "doctrine": [
        "阴得阳而生",
        "阳得阴而成",
        "天地配合",
        "阴阳互用",
        "一阴一阳之谓道",
    ],
}


def _validate_dayou(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError("dayou_hexagram须为dict")
    if value.get("rule_id") != "C41-DY-HEX":
        raise ValueError("dayou_hexagram必须来自C41-DY-HEX")
    if value.get("source_profile") != "tongzong_volume9_dayou_hexagram":
        raise ValueError("C41 source_profile不匹配")
    return value


def _validate_xiaoyou(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError("xiaoyou_hexagram须为dict")
    if value.get("rule_id") != "C47-XY-HEX":
        raise ValueError("xiaoyou_hexagram必须来自C47-XY-HEX")
    if value.get("source_profile") != "tongzong_volume9_xiaoyou":
        raise ValueError("C47 source_profile不匹配")
    return value


def dayou_xiaoyou_difference(
    dayou_hexagram: dict[str, Any],
    xiaoyou_hexagram: dict[str, Any],
) -> dict[str, Any]:
    """比较太游 / 小游当前内卦；不从同异推出灾祥。"""
    dayou = _validate_dayou(dayou_hexagram)
    xiaoyou = _validate_xiaoyou(xiaoyou_hexagram)

    dayou_inner = dayou.get("structure", {}).get("lower_trigram")
    xiaoyou_inner = xiaoyou.get("structure", {}).get("lower_trigram")
    if not isinstance(dayou_inner, str):
        raise ValueError("C41结果缺lower_trigram")
    if not isinstance(xiaoyou_inner, str):
        raise ValueError("C47结果缺lower_trigram")

    same = dayou_inner == xiaoyou_inner
    return {
        "schema_version": "1.0",
        "canonical": C49_VERSION,
        "rule_id": "C49-DY-XY-DIFF",
        "source_profile": "tongzong_volume10_dayou_xiaoyou_difference",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "dayou": {
            "upstream_rule_id": "C41-DY-HEX",
            "inner_trigram": dayou_inner,
            "years_per_inner_trigram": 36,
            "symbolic_ce": "乾天之策",
        },
        "xiaoyou": {
            "upstream_rule_id": "C47-XY-HEX",
            "inner_trigram": xiaoyou_inner,
            "years_per_inner_trigram": 24,
            "symbolic_ce": "坤地之策",
        },
        "same_inner_trigram": same,
        "different_inner_trigram": not same,
        "derived_current_comparison": True,
        "auspice": None,
        "auspice_status": "source_does_not_assign_auspice_from_same_or_different_alone",
        "doctrine": copy.deepcopy(SOURCE_WITNESS["doctrine"]),
        "cross_cycle_merge": False,
        "c38_track_used": False,
        "policy": (
            "C49只解释太游36年/乾策与小游24年/坤策的职责差异；"
            "当前内卦同异是派生事实，不改写C41/C47，也不自动判吉凶。"
        ),
    }


def c49_catalog() -> dict[str, Any]:
    return {
        "canonical": C49_VERSION,
        "rule_id": "C49-DY-XY-DIFF",
        "source_profile": "tongzong_volume10_dayou_xiaoyou_difference",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "upstream_rules": ["C41-DY-HEX", "C47-XY-HEX"],
        "derived_current_comparison": True,
        "auspice_from_same_or_different": False,
        "cross_cycle_merge": False,
    }
