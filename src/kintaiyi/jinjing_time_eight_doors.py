"""C119 《太乙金镜式经》卷一“推八门用法”时计直门层。

本层只处理时计八门直使：
- 阳遁四门：开、生、惊、休；
- 阴遁四门：杜、死、伤、景；
- 三十时一移门；
- 冬至加时直门的240→120→30算法；
- 夏至加时直门的120→30算法（本节局部有缺文，但前一节已直接给阴遁四门次序）。

严格与仓库现有岁计/年计八门分开：
“30时一移门” != “30年一门”。
"""

from __future__ import annotations

import copy
from typing import Any

C119_VERSION = "taiyi-c119-jinjing-volume1-time-eight-doors-v1"

YANG_TIME_DOORS = ("开", "生", "惊", "休")
YIN_TIME_DOORS = ("杜", "死", "伤", "景")
TIME_BLOCK = 30
TIME_DOOR_CYCLE = 120
WINTER_OUTER_CYCLE = 240

ZHANGLIANG_ANCHORS = {
    "阳遁": [
        {"anchor": "冬至甲日夜半甲子以后", "door": "开"},
        {"anchor": "丙日日中甲午以后", "door": "生"},
        {"anchor": "己日夜半甲子以后", "door": "惊"},
        {"anchor": "辛日日中甲午以后", "door": "休"},
    ],
    "阴遁": [
        {"anchor": "夏至甲日夜半甲子以后", "door": "杜"},
        {"anchor": "丙日日中甲午以后", "door": "死"},
        {"anchor": "己日夜半甲子以后", "door": "伤"},
        {"anchor": "辛日日中甲午以后", "door": "景"},
    ],
}

MOVEMENT_RATES = {
    "太乙": {"time_units_per_move": 3},
    "大将": {"time_units_per_move": 1},
}

SOURCE_WITNESS = {
    "work": "太乙金镜式经",
    "volume": 1,
    "sections": [
        "推八门用法",
        "推冬至加时所直门法",
        "推夏至加时所直门法",
    ],
    "direct_core": [
        "阳遁四门开生惊休",
        "阴遁四门杜死伤景",
        "三十时一移门",
        "常以直门加太乙及主客大将随数而行",
        "太乙三时一移，大将一时一移",
        "冬至时实240去之、再120去之、余以30约之为门数",
        "夏至时实120去之、余以30约之为门数",
    ],
    "summer_local_lacuna": (
        "推夏至加时所直门法在‘为门数’后有缺文；"
        "但上一节已直接给阴遁四门杜死伤景及三十时一移门。"
    ),
    "policy": (
        "只实现时计直门，不把卷一年计/岁计八门或其他卷八门公式混入。"
    ),
}

SEPARATION_BOUNDARY = {
    "existing_repository_file": "rules/jinjing/eight_door.py",
    "existing_file_semantics": "240-year / 30-year duty-door cycle",
    "c119_semantics": "time-count / 30-time-unit duty-door cycle",
    "same_formula": False,
    "promotion_policy": "两者必须分层，不得互相代替。",
}

OVERLAY_BOUNDARY = {
    "source_clause": "常以直门加太乙及主客大将随数而行",
    "implemented_position_overlay": False,
    "reason": (
        "本句给出使用原则与移动速率，但未在C119单独重建太乙/大将具体起位坐标公式。"
    ),
}


def _time_real(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("time_real须为整数")
    if value < 0:
        raise ValueError("time_real须>=0")
    return value


def winter_solstice_duty_door(time_real: int) -> dict[str, Any]:
    """王希明冬至加时直门：240去之，再120去之，再按30分四门。"""
    value = _time_real(time_real)
    outer = value % WINTER_OUTER_CYCLE
    inner = outer % TIME_DOOR_CYCLE
    index = inner // TIME_BLOCK
    door = YANG_TIME_DOORS[index]
    return {
        "schema_version": "1.0",
        "canonical": C119_VERSION,
        "rule_id": "C119-WINTER-TIME-DUTY-DOOR",
        "source_profile": "jinjing_volume1_time_eight_doors",
        "dun": "阳遁",
        "time_real": value,
        "outer_remainder_240": outer,
        "inner_remainder_120": inner,
        "door_index": index,
        "duty_door": door,
        "block_size": TIME_BLOCK,
        "source_status": "direct",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "separation_boundary": copy.deepcopy(SEPARATION_BOUNDARY),
    }


def summer_solstice_duty_door(time_real: int) -> dict[str, Any]:
    """夏至加时直门：120去之，按30分阴遁四门。

    本节“为门数”后有缺文；阴遁四门次序来自紧邻“推八门用法”直接正文。
    """
    value = _time_real(time_real)
    remainder = value % TIME_DOOR_CYCLE
    index = remainder // TIME_BLOCK
    door = YIN_TIME_DOORS[index]
    return {
        "schema_version": "1.0",
        "canonical": C119_VERSION,
        "rule_id": "C119-SUMMER-TIME-DUTY-DOOR",
        "source_profile": "jinjing_volume1_time_eight_doors",
        "dun": "阴遁",
        "time_real": value,
        "remainder_120": remainder,
        "door_index": index,
        "duty_door": door,
        "block_size": TIME_BLOCK,
        "source_status": "cross_section_direct_sequence_with_local_lacuna",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "separation_boundary": copy.deepcopy(SEPARATION_BOUNDARY),
    }


def time_duty_door(dun: str, time_real: int) -> dict[str, Any]:
    if dun in ("阳", "阳遁"):
        return winter_solstice_duty_door(time_real)
    if dun in ("阴", "阴遁"):
        return summer_solstice_duty_door(time_real)
    raise ValueError("dun须为阳遁或阴遁")


def movement_rates() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "canonical": C119_VERSION,
        "rule_id": "C119-EIGHT-DOOR-MOVEMENT-RATES",
        "rates": copy.deepcopy(MOVEMENT_RATES),
        "duty_door_block": TIME_BLOCK,
        "overlay_boundary": copy.deepcopy(OVERLAY_BOUNDARY),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
    }


def c119_catalog() -> dict[str, Any]:
    return {
        "canonical": C119_VERSION,
        "rule_ids": [
            "C119-WINTER-TIME-DUTY-DOOR",
            "C119-SUMMER-TIME-DUTY-DOOR",
            "C119-EIGHT-DOOR-MOVEMENT-RATES",
        ],
        "yang_time_doors": list(YANG_TIME_DOORS),
        "yin_time_doors": list(YIN_TIME_DOORS),
        "time_block": TIME_BLOCK,
        "time_door_cycle": TIME_DOOR_CYCLE,
        "winter_outer_cycle": WINTER_OUTER_CYCLE,
        "zhangliang_anchors": copy.deepcopy(ZHANGLIANG_ANCHORS),
        "movement_rates": copy.deepcopy(MOVEMENT_RATES),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "separation_boundary": copy.deepcopy(SEPARATION_BOUNDARY),
        "overlay_boundary": copy.deepcopy(OVERLAY_BOUNDARY),
    }
