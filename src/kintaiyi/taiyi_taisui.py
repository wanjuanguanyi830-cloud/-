"""G1 太岁与岁计五元七十二局入口。

《太乙金镜式经》卷一“推太岁所在法”：
- 上元甲子积年先以360去之；
- 再以60去之；
- 命甲子算外，得太岁所在辰。

《太乙统宗宝鉴》卷一进一步把360周拆为五元：
甲子、丙子、戊子、庚子、壬子五元，各72局。
"""

from __future__ import annotations

from typing import Any

from .taiyi_rules import BRANCHES, STEMS

G1_RULE_ID = "J1-TAISUI-60"
YEAR_ENTRY_RULE_ID = "TZ1-FIVE-YUAN-72"
SOURCE_PROFILE = "jinjing_tongzong_year_entry"

CYCLE_60 = tuple(
    STEMS[i % 10] + BRANCHES[i % 12]
    for i in range(60)
)
FIVE_YUAN = ("甲子", "丙子", "戊子", "庚子", "壬子")


def _accumulated_year(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("accumulated_year须为整数")
    if value < 1:
        raise ValueError("accumulated_year须>=1")
    return value


def taisui_from_accumulated_year(accumulated_year: int) -> dict[str, Any]:
    """积年 -> 六十甲子太岁。"""
    n = _accumulated_year(accumulated_year)
    remainder_360 = n % 360 or 360
    remainder_60 = remainder_360 % 60 or 60
    ganzhi = CYCLE_60[remainder_60 - 1]

    return {
        "rule_id": G1_RULE_ID,
        "source_profile": SOURCE_PROFILE,
        "accumulated_year": n,
        "remainder_360": remainder_360,
        "remainder_60": remainder_60,
        "sexagenary_index_1based": remainder_60,
        "taisui_ganzhi": ganzhi,
        "taisui_stem": ganzhi[0],
        "taisui_branch": ganzhi[1],
        "policy": (
            "余0按本周末位处理：360周余0=第360算，60周余0=癸亥；"
            "不能把数学0余数直接当甲子。"
        ),
    }


def year_entry_from_accumulated_year(accumulated_year: int) -> dict[str, Any]:
    """积年 -> 太岁 + 五元 + 本元局号。"""
    g1 = taisui_from_accumulated_year(accumulated_year)
    r360 = g1["remainder_360"]

    five_yuan_index = (r360 - 1) // 72
    local_ju = (r360 - 1) % 72 + 1
    five_yuan = FIVE_YUAN[five_yuan_index]

    return {
        **g1,
        "entry_rule_id": YEAR_ENTRY_RULE_ID,
        "five_yuan_index_1based": five_yuan_index + 1,
        "five_yuan": five_yuan,
        "local_ju": local_ju,
        "yuan_size": 72,
        "outer_cycle": 360,
        "policy_entry": (
            "360周分甲子/丙子/戊子/庚子/壬子五元，各72局；"
            "local_ju供G2/G3消费，太岁支供G4消费。"
        ),
    }


def taisui_from_ju(ju: int) -> dict[str, Any]:
    """72局立成辅助：同局五元年干不同，但地支固定。"""
    if isinstance(ju, bool) or not isinstance(ju, int) or not 1 <= ju <= 72:
        raise ValueError("ju须为1..72整数")
    branch = BRANCHES[(ju - 1) % 12]
    return {
        "rule_id": "REGRESSION-TAISUI-BRANCH-FROM-JU",
        "ju": ju,
        "taisui_branch": branch,
        "status": "regression_helper_only",
        "policy": "只恢复72局表共同年支，不替代正式积年六十甲子计算。",
    }
