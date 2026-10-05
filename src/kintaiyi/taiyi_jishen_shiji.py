"""G4计神与G5始击的来源实现。

G4：
- 阳遁太岁子年，计神起寅；
- 阴遁太岁子年，计神起申；
- 均随太岁逆行十二辰。

G5：
- 以计神加和德宫（和德=艮）；
- 用同一盘旋转视文昌所临之下；
- 该地盘位置即始击。

来源：
《太乙金镜式经》卷二“推太乙运式法”；
《太乙统宗宝鉴》卷二“明太乙运式之法”。
"""

from __future__ import annotations

from typing import Any

from .taiyi_rules import (
    BRANCHES,
    GOD_POSITION,
    SECTOR_GODS,
    SIXTEEN,
    position,
    rotate_sixteen,
)

G4_RULE_ID = "J2-JISHEN-01"
G5_RULE_ID = "J2-SHIJI-01"
SOURCE_PROFILE = "jinjing_tongzong_v2_jishen_shiji"
HEDE_SECTOR = GOD_POSITION["和德"]  # 艮


def _normalize_dun(dun: str) -> str:
    mapping = {"阳": "阳", "陽": "阳", "阴": "阴", "陰": "阴"}
    try:
        return mapping[dun]
    except (KeyError, TypeError) as exc:
        raise ValueError("dun须为阳/阴") from exc


def jishen_from_taisui(taisui_branch: str, *, dun: str) -> dict[str, Any]:
    """太岁支 -> 计神。"""
    dun_norm = _normalize_dun(dun)
    if taisui_branch not in BRANCHES:
        raise ValueError("taisui_branch须为十二地支")

    taisui_index = BRANCHES.index(taisui_branch)
    start = "寅" if dun_norm == "阳" else "申"
    start_index = BRANCHES.index(start)
    jishen = BRANCHES[(start_index - taisui_index) % 12]

    return {
        "rule_id": G4_RULE_ID,
        "source_profile": SOURCE_PROFILE,
        "dun": dun_norm,
        "taisui_branch": taisui_branch,
        "start_at_zi_year": start,
        "direction": "逆行十二辰",
        "jishen_sector": jishen,
        "policy": "计神只行十二地支，不入乾坤艮巽四维。",
    }


def jishen_from_entry_count(entry_count: int, *, dun: str) -> dict[str, Any]:
    """四计通用：由入局积数按12周法求计神。"""
    if isinstance(entry_count, bool) or not isinstance(entry_count, int):
        raise TypeError("entry_count须为整数")
    if entry_count < 1:
        raise ValueError("entry_count须>=1")

    dun_norm = _normalize_dun(dun)
    remainder_12 = entry_count % 12 or 12
    start = "寅" if dun_norm == "阳" else "申"
    start_index = BRANCHES.index(start)
    jishen = BRANCHES[(start_index - (remainder_12 - 1)) % 12]

    return {
        "rule_id": G4_RULE_ID,
        "source_profile": SOURCE_PROFILE,
        "dun": dun_norm,
        "entry_count": entry_count,
        "remainder_12": remainder_12,
        "start_sector": start,
        "direction": "逆行十二辰",
        "jishen_sector": jishen,
        "policy": "四计通用12周法；整除12按第12算处理。",
    }


def shiji_from_jishen_wenchang(*, jishen: Any, wenchang: Any) -> dict[str, Any]:
    """计神加和德宫，旋转文昌，求始击。"""
    jishen_sector = position(jishen)
    wenchang_sector = position(wenchang)

    if jishen_sector not in BRANCHES:
        raise ValueError("计神须落十二地支，不得在四维")

    rotation_steps = (
        SIXTEEN.index(HEDE_SECTOR) - SIXTEEN.index(jishen_sector)
    ) % len(SIXTEEN)

    shiji_sector = rotate_sixteen(wenchang_sector, rotation_steps)
    shiji_god = SECTOR_GODS[shiji_sector]

    plate_map = {
        heaven_sector: rotate_sixteen(heaven_sector, rotation_steps)
        for heaven_sector in SIXTEEN
    }

    return {
        "rule_id": G5_RULE_ID,
        "source_profile": SOURCE_PROFILE,
        "jishen_sector": jishen_sector,
        "hede_sector": HEDE_SECTOR,
        "rotation_steps": rotation_steps,
        "wenchang_sector": wenchang_sector,
        "shiji_sector": shiji_sector,
        "shiji_god": shiji_god,
        "plate_map_heaven_to_earth": plate_map,
        "check": {
            "jishen_lands_on_hede": plate_map[jishen_sector] == HEDE_SECTOR,
            "wenchang_lands_on_shiji": plate_map[wenchang_sector] == shiji_sector,
        },
        "policy": (
            "将天盘计神旋到地盘和德(艮)，文昌随同一旋转量落下；"
            "文昌所临之下即始击。"
        ),
    }


def shiji_from_taisui_wenchang(
    *,
    taisui_branch: str,
    dun: str,
    wenchang: Any,
) -> dict[str, Any]:
    """G4 -> G5 连续求计神、始击。"""
    g4 = jishen_from_taisui(taisui_branch, dun=dun)
    g5 = shiji_from_jishen_wenchang(
        jishen=g4["jishen_sector"],
        wenchang=wenchang,
    )
    return {
        "rule_id": "CORE-G4-G5-CHAIN",
        "source_profile": SOURCE_PROFILE,
        "g4": g4,
        "g5": g5,
        "jishen_sector": g4["jishen_sector"],
        "shiji_sector": g5["shiji_sector"],
        "shiji_god": g5["shiji_god"],
    }


def g4_g5_from_ju(*, ju: int, dun: str, wenchang: Any) -> dict[str, Any]:
    """72局回归辅助：局号只用于恢复该局太岁支，不作为G4/G5公式来源。"""
    if isinstance(ju, bool) or not isinstance(ju, int) or not 1 <= ju <= 72:
        raise ValueError("ju须为1..72整数")
    taisui_branch = BRANCHES[(ju - 1) % 12]
    result = shiji_from_taisui_wenchang(
        taisui_branch=taisui_branch,
        dun=dun,
        wenchang=wenchang,
    )
    return {
        **result,
        "ju": ju,
        "taisui_branch": taisui_branch,
        "helper_status": "regression_only",
    }
