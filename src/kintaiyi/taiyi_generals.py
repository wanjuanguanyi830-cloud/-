"""太乙主客大将/参将 G7 来源实现。

来源分层：
- 《太乙金镜式经》卷二“推太乙运式法”：
  置算定主客大将；举10置1、24弃20置4之例。
- 《太乙统宗宝鉴》卷二：
  普通数去十用零；10/20/30/40以九去之取余为大将；
  大将宫数三因，仍去十用零，为参将。
- 《武经总要》《太乙秘书》等局例：
  5/15/25/35 为杜塞，大小将不出中宫。

项目口径：
杜塞先截断，不生成正常“五宫大将/五宫参将”；
并向下游输出 five_generals_released=False。
"""

from __future__ import annotations

from typing import Any

G7_RULE_ID = "CORE-G7-GENERALS"
G7_SOURCE_PROFILE = "tongzong_v2_general_formula_with_blockage"
BLOCKED_CALCS = frozenset({5, 15, 25, 35})


def _calc(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("calc_value须为整数")
    if not 1 <= value <= 40:
        raise ValueError("calc_value须在1..40")
    return value


def is_blocked_calc(calc_value: int) -> bool:
    return _calc(calc_value) in BLOCKED_CALCS


def big_general_palace(calc_value: int) -> dict[str, Any]:
    """由算数求大将宫；杜塞优先截断。"""
    n = _calc(calc_value)

    if n in BLOCKED_CALCS:
        return {
            "rule_id": G7_RULE_ID,
            "source_profile": G7_SOURCE_PROFILE,
            "calc_value": n,
            "blocked": True,
            "blocked_kind": "杜塞",
            "nominal_center": 5,
            "big_general_palace": None,
            "formula_branch": "blocked_5_15_25_35",
            "five_generals_released": False,
            "reason": "杜塞，大小将不出中宫，取五将不发",
        }

    if n % 10 == 0:
        # 《统宗》卷二明确：10/20/30/40以九去之。
        big = n % 9
        branch = "exact_tens_mod_9"
    else:
        big = n % 10
        branch = "discard_tens_use_units"

    return {
        "rule_id": G7_RULE_ID,
        "source_profile": G7_SOURCE_PROFILE,
        "calc_value": n,
        "blocked": False,
        "blocked_kind": None,
        "nominal_center": None,
        "big_general_palace": big,
        "formula_branch": branch,
        "five_generals_released": None,
        "reason": "依算数定大将宫",
    }


def assistant_general_palace(big_palace: int) -> int:
    """大将宫数三因，去十用零，得参将宫。"""
    if isinstance(big_palace, bool) or not isinstance(big_palace, int):
        raise TypeError("big_palace须为整数")
    if not 1 <= big_palace <= 9:
        raise ValueError("big_palace须在1..9")
    return (big_palace * 3) % 10


def generals_from_calc(calc_value: int, *, side: str | None = None) -> dict[str, Any]:
    """完整返回一方算数对应的大将、参将、杜塞状态。"""
    base = big_general_palace(calc_value)
    if base["blocked"]:
        assistant = None
    else:
        assistant = assistant_general_palace(base["big_general_palace"])

    return {
        **base,
        "side": side,
        "assistant_general_palace": assistant,
        "general_pair_computable": not base["blocked"],
        "source_boundary": {
            "jinjing_v2": "运式第七/第八步给定大将原则及10、24例",
            "tongzong_v2": "完整普通数、整十、大将三因参将公式",
            "blockage": "5/15/25/35局例明确大小将不出中宫",
        },
        "policy": (
            "杜塞先于大将公式；不得把5/15/25/35机械取个位5后生成正常五宫将。"
        ),
    }


def host_guest_generals(host_calc: int, guest_calc: int) -> dict[str, Any]:
    """一次生成主客两方G7事实，保持双方杜塞独立。"""
    host = generals_from_calc(host_calc, side="主")
    guest = generals_from_calc(guest_calc, side="客")
    return {
        "rule_id": "CORE-G7-HOST-GUEST-GENERALS",
        "source_profile": G7_SOURCE_PROFILE,
        "host": host,
        "guest": guest,
        "any_blocked": host["blocked"] or guest["blocked"],
        "all_general_pairs_computable": (
            host["general_pair_computable"] and guest["general_pair_computable"]
        ),
        "policy": "主客分别由各自算数定将；一方杜塞不改写另一方大将公式。",
    }
