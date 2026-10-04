"""阳九 / 百六来源变体目录。

C36 的可运行大小限仍是《太乙统宗宝鉴》profile。
本模块只登记《太乙金镜式经》卷七的同名规则及其内部数字冲突，
不自动合并、不从疑文补公式。
"""

from __future__ import annotations

import copy
from typing import Any

LIMIT_CYCLE_VARIANTS_VERSION = "taiyi-limit-cycle-variants-v1"

PROFILES = {
    "tongzong_yangjiu_bailiu": {
        "source": "太乙统宗宝鉴",
        "volume": 10,
        "status": "implemented",
        "runtime": "kintaiyi.limit_cycles.yangjiu_bailiu_limits",
        "yangjiu": {
            "big_limit": 4560,
            "small_limit": 456,
            "surplus_offset": 130,
        },
        "bailiu": {
            "big_limit": 4320,
            "small_limit": 288,
            "surplus_offset": 2050,
        },
    },
    "jinjing_siku_volume7": {
        "source": "太乙金镜式经",
        "edition": "四库全书本",
        "volume": 7,
        "status": "source_variant_not_fully_computable",
        "yangjiu": {
            "yuan_years": 4560,
            "one_yangjiu_years": 456,
            "region_step_text_years": 13,
            "region_count": 12,
            "region_origin": "寅邦",
            "region_direction": "顺行",
            "consistency": {
                "cycle_arithmetic": "456×10=4560",
                "region_step_closure": "13×12=156，不能直接闭合456",
                "status": "region_formula_unresolved",
            },
        },
        "bailiu": {
            "one_cycle_years": 288,
            "cycles_per_yuan": 15,
            "source_text_yuan_years": 4330,
            "arithmetic_yuan_years": 4320,
            "region_step_years": 24,
            "region_count": 12,
            "region_origin": "寅邦",
            "region_direction": "顺行",
            "consistency": {
                "cycle_arithmetic": "288×15=4320",
                "source_text_conflict": "正文作4330",
                "region_step_closure": "24×12=288",
                "status": "yuan_total_text_conflict",
            },
        },
        "runtime": None,
        "policy": (
            "只保存卷七直接文本与算术冲突；"
            "在版本校勘解决13年移邦与4330疑文前，不生成金镜位置算法。"
        ),
    },
}


def limit_cycle_source_variants() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "canonical": LIMIT_CYCLE_VARIANTS_VERSION,
        "profiles": copy.deepcopy(PROFILES),
        "canonical_selected": None,
        "cross_source_merge": False,
        "policy": (
            "《统宗》大小限与《金镜》卷七同名阳九/百六并列保存；"
            "不得用一个来源的盈差、大限或移邦法补另一个来源。"
        ),
    }


def compare_limit_cycle_profiles() -> dict[str, Any]:
    """只报告差异，不选择正确版本。"""
    return {
        "yangjiu": {
            "shared": {"yuan_years": 4560, "unit_years": 456},
            "tongzong_extra": {"surplus_offset": 130},
            "jinjing_extra": {"region_step_text_years": 13, "region_origin": "寅邦"},
            "equivalent_formula": False,
        },
        "bailiu": {
            "shared": {"unit_years": 288, "cycles_per_yuan": 15},
            "tongzong": {"yuan_years": 4320, "surplus_offset": 2050},
            "jinjing": {
                "source_text_yuan_years": 4330,
                "arithmetic_yuan_years": 4320,
                "region_step_years": 24,
                "region_origin": "寅邦",
            },
            "equivalent_formula": False,
        },
        "cross_source_merge": False,
    }
