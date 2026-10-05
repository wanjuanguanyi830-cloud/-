"""《太乙金镜式经》卷一“客主八门与太乙八门开休生三门合”关系层。

本模块只解释李淳风岁计古法的“合”：
- 先以开门加太乙，得太乙之八门；
- 再看主/客大将所在宫，在太乙门盘中落何门；
- 落开、休、生之一，记为该方与太乙三吉门“会合/得吉门”。

依据：
1. 《金镜》卷一原句：“客主八门与太乙八门开休生三门合者大利”；
2. 《太乙淘金歌》“八门起例”把操作解释为“常以开门加太乙……视主将在开休生门下者吉”。

不把“合”解释成三张门盘的开对开、休对休、生对生全部逐名重合。
"""

from __future__ import annotations

from typing import Any

from .jinjing_eight_door_overlay import door_overlay, open_door_overlay
from .jinjing_year_eight_doors import year_duty_door
from .taiyi_generals import host_guest_generals

SOURCE_PROFILE = "jinjing_volume1_li_chunfeng_year_door_meeting"
RULE_ID = "J1-YEAR-DOOR-MEETING"
GOOD_DOORS = frozenset({"开", "休", "生"})
OUTER_PALACES = frozenset({1, 2, 3, 4, 6, 7, 8, 9})


def _palace(value: int | None, *, field: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value not in OUTER_PALACES:
        raise ValueError(f"{field}须为外八宫1/2/3/4/6/7/8/9或None")
    return value


def _side_result(
    *,
    side: str,
    general_palace: int | None,
    palace_to_door: dict[int, str],
) -> dict[str, Any]:
    if general_palace is None:
        return {
            "side": side,
            "general_palace": None,
            "gate_under_taiyi_overlay": None,
            "meets_three_good_doors": None,
            "status": "not_computable",
            "reason": "该方大将无外八宫位置（如杜塞不出中宫）或上游未给",
        }

    gate = palace_to_door[general_palace]
    favorable = gate in GOOD_DOORS
    return {
        "side": side,
        "general_palace": general_palace,
        "gate_under_taiyi_overlay": gate,
        "meets_three_good_doors": favorable,
        "status": "favorable" if favorable else "not_favorable_by_this_rule",
        "verdict": "大利" if favorable else None,
    }


def year_door_meeting(
    *,
    taiyi_palace: int,
    host_big_palace: int | None,
    guest_big_palace: int | None,
) -> dict[str, Any]:
    """判主/客大将在太乙八门中是否会开休生三吉门。

    这是门关系的局部吉凶，不覆盖囚、迫、格、对、杜塞、五将发不发等上层/平行条件。
    """
    taiyi = _palace(taiyi_palace, field="taiyi_palace")
    host = _palace(host_big_palace, field="host_big_palace")
    guest = _palace(guest_big_palace, field="guest_big_palace")
    overlay = open_door_overlay(taiyi)

    host_result = _side_result(
        side="主",
        general_palace=host,
        palace_to_door=overlay["palace_to_door"],
    )
    guest_result = _side_result(
        side="客",
        general_palace=guest,
        palace_to_door=overlay["palace_to_door"],
    )

    return {
        "source_profile": SOURCE_PROFILE,
        "rule_id": RULE_ID,
        "source_scope": "太乙金镜式经_卷一_推八门占岁计法",
        "taiyi_palace": taiyi,
        "taiyi_overlay": overlay["palace_to_door"],
        "three_good_doors": ["开", "休", "生"],
        "host": host_result,
        "guest": guest_result,
        "interpretation": (
            "“合”按平行古注落实为主/客大将所在宫落入太乙门盘的开休生之一；"
            "不解释为三门逐名全部同宫。"
        ),
        "evidence_boundary": {
            "host": "《太乙淘金歌》明释“视主将在开休生门下者吉”",
            "guest": "《金镜》原句并称“客主八门”；客方按同句对称保存，未找到同等清晰的单独客将释句",
        },
        "policy": (
            "本条只给门关系的局部大利/不大利；即使落开休生，"
            "若另有囚迫格对、杜塞、五将不发等，仍由对应规则覆盖最终军事判断。"
        ),
    }



def year_door_meeting_wang_ximing(
    *,
    accumulated_year: int,
    taiyi_palace: int,
    host_big_palace: int | None,
    guest_big_palace: int | None,
) -> dict[str, Any]:
    """王希明岁计直使门空间 profile（平行古注补足）。

    《金镜》卷一直接给出240/30直使周期；《太乙淘金歌》又保存
    “常以直使加太乙”“直使又加主将宫”的操作说明。
    因此这里以当年直使门加太乙，仍按同一方向判断主/客大将
    是否落太乙动态盘的开、休、生三吉门。

    source_status 固定为 parallel_reconstruction，避免冒充《金镜》逐字公式。
    """
    duty = year_duty_door(accumulated_year)
    anchor_door = duty["duty_door"]

    taiyi = _palace(taiyi_palace, field="taiyi_palace")
    host = _palace(host_big_palace, field="host_big_palace")
    guest = _palace(guest_big_palace, field="guest_big_palace")
    overlay = door_overlay(taiyi, anchor_door)

    host_result = _side_result(
        side="主",
        general_palace=host,
        palace_to_door=overlay["palace_to_door"],
    )
    guest_result = _side_result(
        side="客",
        general_palace=guest,
        palace_to_door=overlay["palace_to_door"],
    )

    return {
        "source_profile": "jinjing_volume1_wang_ximing_year_direct_door_meeting_parallel",
        "source_status": "parallel_reconstruction",
        "rule_id": "J1-YEAR-DOOR-MEETING-WANG",
        "source_scope": "金镜卷一岁计直使 + 太乙淘金歌平行空间释法",
        "accumulated_year": accumulated_year,
        "duty_door": anchor_door,
        "duty": duty,
        "taiyi_palace": taiyi,
        "taiyi_overlay": overlay["palace_to_door"],
        "three_good_doors": ["开", "休", "生"],
        "host": host_result,
        "guest": guest_result,
        "interpretation": (
            "直使门加太乙形成动态太乙门盘；主/客大将落该盘开休生之一，"
            "则在本条门关系上为大利。"
        ),
        "policy": (
            "这是平行古注补足的王希明空间profile；"
            "李淳风旧法J1-YEAR-DOOR-MEETING仍固定开门加太乙，二者并存。"
        ),
    }



def year_door_meeting_from_calcs(
    *,
    taiyi_palace: int,
    host_calc: int,
    guest_calc: int,
) -> dict[str, Any]:
    """主客算 -> G7大小将 -> 李淳风太乙三吉门会合。"""
    generals = host_guest_generals(host_calc, guest_calc)
    meeting = year_door_meeting(
        taiyi_palace=taiyi_palace,
        host_big_palace=generals["host"]["big_general_palace"],
        guest_big_palace=generals["guest"]["big_general_palace"],
    )
    return {
        "rule_id": "CORE-G7-J1-YEAR-DOOR-MEETING",
        "source_profile": "cross_layer_g7_to_jinjing_year_doors",
        "generals": generals,
        "meeting": meeting,
        "host_blocked": generals["host"]["blocked"],
        "guest_blocked": generals["guest"]["blocked"],
        "policy": (
            "杜塞方的meeting保持not_computable；"
            "不得把nominal_center=5当成正常五宫去查太乙八门。"
        ),
    }
