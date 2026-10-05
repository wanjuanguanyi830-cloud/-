"""时计 source-specific 组合层。

连接：
1. TZ1 四计共同核心：冬至后阳局、夏至后阴局；
2. C119 《金镜》卷一时计八门直使：
   - 阳遁：开、生、惊、休，30时一移；
   - 阴遁：杜、死、伤、景，30时一移。

重要：四计“入局积数”和C119“直门时实”来自不同原文步骤，
本层要求分别传入，不假定二者数值必然相同。
"""

from __future__ import annotations

from typing import Any

from .jinjing_time_eight_doors import time_duty_door
from .taiyi_four_counts import four_count_core_from_entry_count, resolve_four_count_dun

RULE_ID = "CORE-TIME-COUNT-PROFILE"


def time_count_profile(
    *,
    entry_count: int,
    solstice_half: str,
    duty_time_real: int | None = None,
) -> dict[str, Any]:
    """时计入局核心 + 可选八门直使。"""
    profile = resolve_four_count_dun(
        "时计",
        solstice_half=solstice_half,
    )
    dun = profile["dun"]

    core = four_count_core_from_entry_count(
        entry_count,
        count_type="时计",
        solstice_half=solstice_half,
    )

    duty = (
        time_duty_door(dun, duty_time_real)
        if duty_time_real is not None
        else None
    )

    return {
        "rule_id": RULE_ID,
        "source_profile": "jinjing_tongzong_time_count_integration",
        "count_type": "时计",
        "solstice_half": solstice_half,
        "dun": dun,
        "entry_count": entry_count,
        "duty_time_real": duty_time_real,
        "core": core,
        "duty_door": duty,
        "taiyi_palace": core["taiyi_palace"],
        "wenchang_sector": core["wenchang_sector"],
        "jishen_sector": core["jishen_sector"],
        "shiji_sector": core["shiji_sector"],
        "host_calc": core["host_calc"],
        "guest_calc": core["guest_calc"],
        "direct_door": duty["duty_door"] if duty is not None else None,
        "policy": (
            "冬至后用阳局、夏至后用阴局；"
            "entry_count与duty_time_real分栏保存，不做未经来源证明的同值假设。"
        ),
    }


def time_profile_contract(solstice_half: str) -> dict[str, Any]:
    """只返回该半岁的时计阴阳与八门序列约束。"""
    profile = resolve_four_count_dun("时计", solstice_half=solstice_half)
    if profile["dun"] == "阳":
        doors = ["开", "生", "惊", "休"]
        solstice_basis = "冬至"
    else:
        doors = ["杜", "死", "伤", "景"]
        solstice_basis = "夏至"
    return {
        "rule_id": "CORE-TIME-PROFILE-CONTRACT",
        "solstice_half": solstice_half,
        "solstice_basis": solstice_basis,
        "dun": profile["dun"],
        "time_duty_doors": doors,
        "door_block": 30,
        "calendar_upstream_required": True,
        "required_calendar_facts": [
            "所求时属于冬至后还是夏至后",
            "四计入局积数entry_count",
            "C119直门时实duty_time_real（若要求八门直使）",
        ],
        "policy": "不得用公历月份近似替代真实冬至/夏至气应边界。",
    }
