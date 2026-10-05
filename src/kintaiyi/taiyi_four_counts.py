"""岁/月/日/时四计的共同入局核心与阴阳profile选择。

《太乙统宗宝鉴》卷一直接说明：
- 太乙所在：岁、月、日、时四计皆同；唯时计夏至后用阴局；
- 天目文昌：四计皆同；唯时计夏至后用阴局；
- 计神：四计皆同；唯夏至后时计用阴局。

因此：
- 岁计：阳局；
- 月计：阳局；
- 日计：阳局；
- 时计冬至半岁：阳局；
- 时计夏至半岁：阴局。

本模块消费“已经由各自历法上游求出的入局积数”；
不自行发明公历日期到积月/积日/积时的换算。
"""

from __future__ import annotations

from typing import Any

from .taiyi_calculations import host_guest_calculations
from .taiyi_generals import host_guest_generals
from .taiyi_jishen_shiji import jishen_from_entry_count, shiji_from_jishen_wenchang
from .taiyi_position import taiyi_from_entry_count
from .taiyi_wenchang import wenchang_from_entry_count

FOUR_COUNT_RULE_ID = "TZ1-FOUR-COUNT-CORE"
SOURCE_PROFILE = "tongzong_volume1_four_count_profiles"
COUNT_TYPES = ("岁计", "月计", "日计", "时计")
SOLSTICE_HALVES = ("冬至后", "夏至后")


def _count_type(value: str) -> str:
    aliases = {
        "岁": "岁计", "年": "岁计", "年计": "岁计", "岁计": "岁计",
        "月": "月计", "月计": "月计",
        "日": "日计", "日计": "日计",
        "时": "时计", "時": "时计", "时计": "时计", "時計": "时计",
    }
    try:
        return aliases[value]
    except (KeyError, TypeError) as exc:
        raise ValueError("count_type须为岁计/月计/日计/时计") from exc


def resolve_four_count_dun(
    count_type: str,
    *,
    solstice_half: str | None = None,
) -> dict[str, Any]:
    """按来源决定四计使用阳局还是阴局。"""
    kind = _count_type(count_type)

    if kind != "时计":
        if solstice_half is not None:
            raise ValueError("只有时计使用冬至后/夏至后选择阴阳局")
        dun = "阳"
        basis = "岁月日四计用阳局；阴局例外只属于时计夏至后"
    else:
        if solstice_half not in SOLSTICE_HALVES:
            raise ValueError("时计必须显式给solstice_half=冬至后或夏至后")
        dun = "阳" if solstice_half == "冬至后" else "阴"
        basis = (
            "冬至后时计用阳局"
            if dun == "阳"
            else "夏至后时计用阴局"
        )

    return {
        "rule_id": "TZ1-FOUR-COUNT-DUN",
        "source_profile": SOURCE_PROFILE,
        "count_type": kind,
        "solstice_half": solstice_half,
        "dun": dun,
        "basis": basis,
        "policy": "不得把时计夏至后阴局规则外推到岁计、月计、日计。",
    }


def entry_context_from_accumulated_count(
    accumulated_count: int,
    *,
    count_type: str,
) -> dict[str, Any]:
    """四计通用：积数 -> 360周/60纪/72局。

    月、日、时各自如何得到 accumulated_count 属于各自历法上游。
    本函数不隐式加入旧传“盈差240”等来源争议常数。
    """
    kind = _count_type(count_type)
    if isinstance(accumulated_count, bool) or not isinstance(accumulated_count, int):
        raise TypeError("accumulated_count须为整数")
    if accumulated_count < 1:
        raise ValueError("accumulated_count须>=1")

    r360 = accumulated_count % 360 or 360
    ji = (r360 - 1) // 60 + 1
    in_ji = (r360 - 1) % 60 + 1
    yuan = (r360 - 1) // 72 + 1
    local_ju = (r360 - 1) % 72 + 1

    return {
        "rule_id": "TZ1-FOUR-COUNT-ENTRY",
        "source_profile": SOURCE_PROFILE,
        "count_type": kind,
        "accumulated_count": accumulated_count,
        "remainder_360": r360,
        "ji_index_1based": ji,
        "count_in_ji": in_ji,
        "yuan_index_1based": yuan,
        "local_ju": local_ju,
        "policy": (
            "只做360/60/72分解；旧传岁计/日计盈差240不在本canonical中隐式加入。"
        ),
    }


def four_count_core_from_entry_count(
    entry_count: int,
    *,
    count_type: str,
    solstice_half: str | None = None,
) -> dict[str, Any]:
    """入局积数 -> G2..G7，共用核心，阴阳由四计profile决定。"""
    profile = resolve_four_count_dun(
        count_type,
        solstice_half=solstice_half,
    )
    dun = profile["dun"]
    kind = profile["count_type"]

    g2 = taiyi_from_entry_count(entry_count, dun=dun)
    g3 = wenchang_from_entry_count(entry_count, dun=dun)
    g4 = jishen_from_entry_count(entry_count, dun=dun)
    g5 = shiji_from_jishen_wenchang(
        jishen=g4["jishen_sector"],
        wenchang=g3["wenchang_sector"],
    )
    g6 = host_guest_calculations(
        taiyi_palace=g2["taiyi_palace"],
        wenchang=g3["wenchang_sector"],
        shiji=g5["shiji_sector"],
    )
    g7 = host_guest_generals(
        g6["host_calc"],
        g6["guest_calc"],
    )

    return {
        "rule_id": FOUR_COUNT_RULE_ID,
        "source_profile": SOURCE_PROFILE,
        "count_type": kind,
        "solstice_half": solstice_half,
        "dun": dun,
        "entry_count": entry_count,
        "taiyi_palace": g2["taiyi_palace"],
        "wenchang_sector": g3["wenchang_sector"],
        "jishen_sector": g4["jishen_sector"],
        "shiji_sector": g5["shiji_sector"],
        "host_calc": g6["host_calc"],
        "guest_calc": g6["guest_calc"],
        "host_big_general_palace": g7["host"]["big_general_palace"],
        "host_assistant_general_palace": g7["host"]["assistant_general_palace"],
        "guest_big_general_palace": g7["guest"]["big_general_palace"],
        "guest_assistant_general_palace": g7["guest"]["assistant_general_palace"],
        "host_blocked": g7["host"]["blocked"],
        "guest_blocked": g7["guest"]["blocked"],
        "stages": {
            "profile": profile,
            "g2": g2,
            "g3": g3,
            "g4": g4,
            "g5": g5,
            "g6": g6,
            "g7": g7,
        },
        "policy": (
            "四计共用G2-G7公式；只有时计夏至后切阴局。"
            "岁月日不得由季节自动改成阴局。"
        ),
    }


def four_count_core_from_accumulated_count(
    accumulated_count: int,
    *,
    count_type: str,
    solstice_half: str | None = None,
) -> dict[str, Any]:
    """积数先落本元72局，再进入四计核心。"""
    entry = entry_context_from_accumulated_count(
        accumulated_count,
        count_type=count_type,
    )
    core = four_count_core_from_entry_count(
        entry["local_ju"],
        count_type=count_type,
        solstice_half=solstice_half,
    )
    return {
        **core,
        "accumulated_count": accumulated_count,
        "entry_context": entry,
        "local_ju": entry["local_ju"],
    }
