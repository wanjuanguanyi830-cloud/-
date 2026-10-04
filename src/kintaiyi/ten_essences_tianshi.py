"""C56 十精天时位置 runtime：120大周 / 12小周。

主来源：
- 《太乙统宗宝鉴》卷十八 / 卷二十“明十精太乙所主”：
  命起吕申，顺行十二辰；阴局取阳局对冲。
- 《太白兵备统宗宝鉴》卷十一完整推步正文：
  阳遁起寅，阴遁起申，均顺行十二宫。
- 《武经总要》后集卷十八：
  主条命起吕申，顺行十二辰；一见证另补“阴起武德”。

边界：
- 太白同页前置总括句另见“阳申、阴寅”，与后面的完整推步正文相反；
  作为同书内部异文保留，不覆盖详细算法段。
- 邦盈差二被直接来源否定，不应用。
- 不计算十精云气断事。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import BRANCHES, integer

C56_VERSION = "taiyi-c56-ten-essences-tianshi-v1"

TIANSHI_PATHS = {
    "阳": ("寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"),
    "阴": ("申", "酉", "戌", "亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未"),
}

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "witness_volumes": [18, 20],
    "big_cycle": 120,
    "small_cycle": 12,
    "tongzong": {
        "start": "吕申（寅）",
        "mode": "顺行十二辰；阴局取阳局对冲",
        "status": "primary_direct_formula",
    },
    "taibai_bingbei": {
        "detailed_formula": "阳遁起寅，阴遁起申，均顺行十二宫",
        "intro_summary_variant": "同页前置总括句另见阳起申、阴起寅",
        "status": "internal_witness_conflict_detailed_formula_selected_for_collation",
    },
    "wujing_zongyao": {
        "main": "小周十二，命起吕申，顺行十二辰",
        "variant_addition": "一见证另补阴起武德（武德在申）",
        "status": "supports_primary_start_with_variant_detail",
    },
    "source_status": "tongzong_primary_with_detailed_cross_source_collation",
}

SURPLUS_REJECTION = {
    "witness_value": 2,
    "name": "邦盈差",
    "apply": False,
    "reason": "《统宗》明言古经无此，故不敢用。",
}

LEGACY_AUDIT = {
    "function": "config.tian_shi",
    "canonical_equivalent": False,
    "legacy_small_cycle": 12,
    "direct_big_cycle": 120,
    "direct_small_cycle": 12,
    "reason": (
        "旧函数周期表面相合不足以证明公式相合；C56显式保存阳寅/阴申起点、"
        "两遁顺行十二支、120/12边界及同书异文。"
    ),
}


def _dun(value: str) -> str:
    if value not in ("阳", "阴"):
        raise ValueError("dun须为阳/阴")
    return value


def _cycle_state(accumulated_count: int) -> dict[str, int]:
    count = integer(accumulated_count, 1)
    big_remainder = count % 120
    big_cycle_year = big_remainder or 120
    small_remainder = big_cycle_year % 12
    small_cycle_year = small_remainder or 12
    return {
        "accumulated_count": count,
        "big_cycle": 120,
        "big_cycle_remainder": big_remainder,
        "big_cycle_year": big_cycle_year,
        "small_cycle": 12,
        "small_cycle_remainder": small_remainder,
        "small_cycle_year": small_cycle_year,
    }


def tianshi_position(accumulated_count: int, *, dun: str) -> dict[str, Any]:
    """十精天时位置；显式给阳/阴遁，不从现代日期自动推遁。"""
    dun = _dun(dun)
    cycle = _cycle_state(accumulated_count)
    path = TIANSHI_PATHS[dun]
    index = cycle["small_cycle_year"] - 1
    branch = path[index]

    return {
        "schema_version": "1.0",
        "canonical": C56_VERSION,
        "rule_id": "C56-TIANSHI",
        "source_profile": "tongzong_ten_essences_tianshi",
        "essence": "天时",
        "dun": dun,
        **cycle,
        "path": list(path),
        "path_index": index + 1,
        "branch": branch,
        "branch_index": BRANCHES.index(branch) + 1,
        "surplus_applied": False,
        "surplus_policy": copy.deepcopy(SURPLUS_REJECTION),
        "cloud_omen_applied": False,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "policy": (
            "采用统宗主公式，并以太白完整推步正文与武经主条参校；"
            "太白同页前置总括句的阳申阴寅反向读法仅作内部异文保留。"
            "不采用邦盈差二，不计算十精云气断事。"
        ),
    }


def c56_catalog() -> dict[str, Any]:
    return {
        "canonical": C56_VERSION,
        "rule_id": "C56-TIANSHI",
        "implemented": ["天时"],
        "big_cycle": 120,
        "small_cycle": 12,
        "paths": {key: list(value) for key, value in TIANSHI_PATHS.items()},
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "surplus_rejection": copy.deepcopy(SURPLUS_REJECTION),
        "legacy_audit": copy.deepcopy(LEGACY_AUDIT),
        "cloud_omen_runtime": False,
    }
