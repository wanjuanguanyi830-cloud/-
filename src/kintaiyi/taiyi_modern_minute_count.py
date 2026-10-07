"""现代 production 分计：二至瞬间起的逐分钟扩展。

分计不是《太乙统宗宝鉴》卷一“四计”的第五个古法。上游 Kintaiyi 公开文档也明确
把分计标为 modern extension。本模块因此只建立一个显式、版本化、可复现的现代扩展：

- 当前真实冬至/夏至瞬间决定阳/阴半岁；
- 该半岁起点为第1分；
- 每经过完整60秒，entry_count增加1；
- G2..G7仍调用仓库已经校定的共同底层公式，不复制其算法；
- 不附会C119“30时一门”，分计盘不自动生成时计直门。

这个 profile 的目标是为需要分钟级区分度的软件提供稳定 public API，而不是声称发现
古籍中不存在的“分计原法”。
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from .taiyi_calculations import host_guest_calculations
from .taiyi_generals import host_guest_generals
from .taiyi_jishen_shiji import jishen_from_entry_count, shiji_from_jishen_wenchang
from .taiyi_modern_calendar import resolve_time_solstice_half
from .taiyi_position import taiyi_from_entry_count
from .taiyi_wenchang import wenchang_from_entry_count

RULE_ID = "MODERN-TAIYI-MINUTE-COUNT"
SOURCE_PROFILE = "production_modern_solstice_relative_minute_extension_v1"
SECONDS_PER_MINUTE = 60


def _aware_datetime(value: datetime) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError("moment须为datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("moment必须是timezone-aware datetime")
    return value


def minute_core_from_entry_count(entry_count: int, *, dun: str) -> dict[str, Any]:
    """现代分计扩展的入数 -> 既有G2..G7。

    这里仅编排已校定底层函数；分计自身新增的只有“分钟入数”和阴阳半岁选择。
    """
    if isinstance(entry_count, bool) or not isinstance(entry_count, int):
        raise TypeError("entry_count须为整数")
    if entry_count < 1:
        raise ValueError("entry_count须>=1")
    if dun not in {"阳", "陰", "阴", "陽"}:
        raise ValueError("dun须为阳/阴")
    dun_norm = "阳" if dun in {"阳", "陽"} else "阴"

    g2 = taiyi_from_entry_count(entry_count, dun=dun_norm)
    g3 = wenchang_from_entry_count(entry_count, dun=dun_norm)
    g4 = jishen_from_entry_count(entry_count, dun=dun_norm)
    g5 = shiji_from_jishen_wenchang(
        jishen=g4["jishen_sector"],
        wenchang=g3["wenchang_sector"],
    )
    g6 = host_guest_calculations(
        taiyi_palace=g2["taiyi_palace"],
        wenchang=g3["wenchang_sector"],
        shiji=g5["shiji_sector"],
    )
    g7 = host_guest_generals(g6["host_calc"], g6["guest_calc"])

    return {
        "rule_id": "MODERN-TAIYI-MINUTE-CORE",
        "source_profile": SOURCE_PROFILE,
        "count_type": "分计",
        "dun": dun_norm,
        "entry_count": entry_count,
        "local_ju": (entry_count - 1) % 72 + 1,
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
            "g2": g2,
            "g3": g3,
            "g4": g4,
            "g5": g5,
            "g6": g6,
            "g7": g7,
        },
        "policy": (
            "分计只新增逐分钟entry_count与二至半岁阴阳选择；"
            "太乙、文昌、计神、始击、主客算与大小将继续使用既有G2-G7。"
        ),
    }


def accumulated_minute_from_moment(moment: datetime) -> dict[str, Any]:
    """真实二至瞬间起，每完整60秒推进一算。"""
    source = _aware_datetime(moment)
    target_utc = source.astimezone(timezone.utc)
    half = resolve_time_solstice_half(source)
    half_start_utc = half["half_start_utc"]

    elapsed_seconds = (target_utc - half_start_utc).total_seconds()
    if elapsed_seconds < 0:
        raise RuntimeError("所求分早于已解析的当前二至半岁起点")

    elapsed_whole_minutes = int(elapsed_seconds // SECONDS_PER_MINUTE)
    entry_count = elapsed_whole_minutes + 1
    bucket_start_utc = half_start_utc + timedelta(minutes=elapsed_whole_minutes)

    return {
        "rule_id": "MODERN-TAIYI-SOLSTICE-RELATIVE-MINUTE",
        "source_profile": SOURCE_PROFILE,
        "extension_status": "project_defined_modern_extension",
        "solstice_half": half["solstice_half"],
        "dun": half["dun"],
        "input": source,
        "input_utc": target_utc,
        "half_start_utc": half_start_utc,
        "next_half_boundary_utc": half["next_half_boundary_utc"],
        "elapsed_whole_minutes_0based": elapsed_whole_minutes,
        "minute_index_1based": entry_count,
        "entry_count": entry_count,
        "minute_bucket_start_utc": bucket_start_utc,
        "formula": "floor((input_utc - half_start_utc) / 60 seconds) + 1",
        "resolution_seconds": SECONDS_PER_MINUTE,
        "policy": (
            "真实冬/夏至瞬间为半岁分计起点；每完整60秒推进一算。"
            "这是现代扩展，不宣称为古籍四计正文。"
        ),
    }


def modern_minute_count(moment: datetime) -> dict[str, Any]:
    """现代timezone-aware datetime -> 稳定分计扩展盘核心。"""
    source = _aware_datetime(moment)
    arithmetic = accumulated_minute_from_moment(source)
    core = minute_core_from_entry_count(
        arithmetic["entry_count"],
        dun=arithmetic["dun"],
    )

    return {
        "rule_id": RULE_ID,
        "source_profile": SOURCE_PROFILE,
        "extension_status": "stable_modern_extension",
        "input": source,
        "solstice_half": arithmetic["solstice_half"],
        "dun": arithmetic["dun"],
        "entry_count": arithmetic["entry_count"],
        "minute_index_1based": arithmetic["minute_index_1based"],
        "arithmetic": arithmetic,
        "result": core,
        "local_ju": core["local_ju"],
        "taiyi_palace": core["taiyi_palace"],
        "wenchang_sector": core["wenchang_sector"],
        "jishen_sector": core["jishen_sector"],
        "shiji_sector": core["shiji_sector"],
        "host_calc": core["host_calc"],
        "guest_calc": core["guest_calc"],
        "direct_door": None,
        "policy": (
            "分计为分钟级现代扩展；二至阴阳与既有production时计共享真实天文边界，"
            "但不把C119时计直门外推到分计。"
        ),
    }
