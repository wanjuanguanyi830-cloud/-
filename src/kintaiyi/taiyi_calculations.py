"""G6 主客算：文昌/始击沿十六宫至太乙的行算。

直接来源：
- 《太乙金镜式经》卷二“推太乙运式法”：
  正宫按本数，间神起一，行算至太乙宫止；
  例：太乙九宫、大义为目 -> 1 + 8 + 3 + 4 = 16。
- 《太乙统宗宝鉴》卷二进一步明确：
  文昌为主目、始击为客目；正宫从宫数起，间神从一而起，
  自左顺行，依宫数算。

项目通过阴阳72局回归补足两个同宫边界：
- 目在太乙同宫正位：取本宫数；
- 目在太乙同宫间辰：强制一算，不绕环继续累计。
"""

from __future__ import annotations

from typing import Any

from .taiyi_rules import (
    PALACE_POINT,
    SIXTEEN,
    position,
    sector_to_nine_palace,
)

G6_RULE_ID = "J2-CALC-01"
G6_SOURCE_PROFILE = "jinjing_v2_calc_with_72ju_edges"
POSITIVE_SECTOR_TO_PALACE = {sector: palace for palace, sector in PALACE_POINT.items()}
INTERSTITIAL_SECTORS = frozenset(set(SIXTEEN) - set(POSITIVE_SECTOR_TO_PALACE))


def _taiyi_palace(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("taiyi_palace须为整数")
    if value not in PALACE_POINT:
        raise ValueError("taiyi_palace须为外八宫1/2/3/4/6/7/8/9")
    return value


def _eye_sector(value: Any) -> str:
    return position(value)


def calc_from_eye(taiyi_palace: int, eye: Any, *, side: str | None = None) -> dict[str, Any]:
    """由一个目求算数，并返回完整行算路径。"""
    taiyi = _taiyi_palace(taiyi_palace)
    eye_sector = _eye_sector(eye)
    eye_palace = sector_to_nine_palace(eye_sector)
    taiyi_sector = PALACE_POINT[taiyi]
    eye_is_positive = eye_sector in POSITIVE_SECTOR_TO_PALACE
    eye_position_type = "正宫" if eye_is_positive else "间神"

    # 同宫边界必须先截断，否则间辰会沿十六环绕满一周。
    if eye_palace == taiyi:
        if eye_sector == taiyi_sector:
            value = taiyi
            rule_branch = "same_palace_positive_take_palace_number"
            reason = "目与太乙同宫且目在正位，取本宫数"
        else:
            value = 1
            rule_branch = "same_palace_interstitial_forced_one"
            reason = "目与太乙同宫但在间辰，强制一算"
        return {
            "rule_id": G6_RULE_ID,
            "source_profile": G6_SOURCE_PROFILE,
            "side": side,
            "taiyi_palace": taiyi,
            "taiyi_sector": taiyi_sector,
            "eye": eye,
            "eye_sector": eye_sector,
            "eye_palace": eye_palace,
            "eye_position_type": eye_position_type,
            "same_palace": True,
            "calc_value": value,
            "rule_branch": rule_branch,
            "forced_single_count": value == 1 and not eye_is_positive,
            "path": [
                {
                    "sector": eye_sector,
                    "palace": eye_palace,
                    "counted": True,
                    "value": value,
                    "role": "eye_start_and_taiyi_same_palace",
                }
            ],
            "reason": reason,
            "taiyi_terminal_counted": eye_sector == taiyi_sector,
            "policy": (
                "同宫起点按72局边界直接结算；间辰不得绕环。"
                "正位同宫的本宫数属于目之起算，不是从外部抵达太乙后的终点加算。"
            ),
        }

    total = POSITIVE_SECTOR_TO_PALACE[eye_sector] if eye_is_positive else 1
    path = [
        {
            "sector": eye_sector,
            "palace": eye_palace,
            "counted": True,
            "value": total,
            "role": "eye_start",
        }
    ]

    start_index = SIXTEEN.index(eye_sector)
    reached_taiyi = False
    for step in range(1, len(SIXTEEN) + 1):
        sector = SIXTEEN[(start_index + step) % len(SIXTEEN)]
        palace = sector_to_nine_palace(sector)

        if sector == taiyi_sector:
            path.append(
                {
                    "sector": sector,
                    "palace": palace,
                    "counted": False,
                    "value": 0,
                    "role": "taiyi_terminal",
                }
            )
            reached_taiyi = True
            break

        if sector in POSITIVE_SECTOR_TO_PALACE:
            value = POSITIVE_SECTOR_TO_PALACE[sector]
            total += value
            path.append(
                {
                    "sector": sector,
                    "palace": palace,
                    "counted": True,
                    "value": value,
                    "role": "positive_palace",
                }
            )
        else:
            path.append(
                {
                    "sector": sector,
                    "palace": palace,
                    "counted": False,
                    "value": 0,
                    "role": "interstitial_pass",
                }
            )

    if not reached_taiyi:
        raise RuntimeError("十六宫行算未到太乙终点")

    return {
        "rule_id": G6_RULE_ID,
        "source_profile": G6_SOURCE_PROFILE,
        "side": side,
        "taiyi_palace": taiyi,
        "taiyi_sector": taiyi_sector,
        "eye": eye,
        "eye_sector": eye_sector,
        "eye_palace": eye_palace,
        "eye_position_type": eye_position_type,
        "same_palace": False,
        "calc_value": total,
        "rule_branch": "walk_to_taiyi_excluding_terminal",
        "forced_single_count": False,
        "path": path,
        "reason": "由目起算，顺十六宫累计所经正宫数，抵太乙正位即止，太乙终点不计",
        "taiyi_terminal_counted": False,
        "policy": "间神经过位不另加一；只有目本身在间神时以一作为起算。",
    }


def host_guest_calculations(
    *,
    taiyi_palace: int,
    wenchang: Any,
    shiji: Any,
) -> dict[str, Any]:
    """文昌为主目，始击为客目，一次生成主算、客算。"""
    host = calc_from_eye(taiyi_palace, wenchang, side="主")
    guest = calc_from_eye(taiyi_palace, shiji, side="客")
    return {
        "rule_id": "J2-CALC-01-HOST-GUEST",
        "source_profile": G6_SOURCE_PROFILE,
        "taiyi_palace": taiyi_palace,
        "wenchang": wenchang,
        "shiji": shiji,
        "host": host,
        "guest": guest,
        "host_calc": host["calc_value"],
        "guest_calc": guest["calc_value"],
        "policy": "文昌/下目属主算；始击/上目属客算，两者使用同一行算核心。",
    }


def g6_g7_chain(*, taiyi_palace: int, wenchang: Any, shiji: Any) -> dict[str, Any]:
    """G6主客算直接接G7主客大小将。"""
    from .taiyi_generals import host_guest_generals

    calculations = host_guest_calculations(
        taiyi_palace=taiyi_palace,
        wenchang=wenchang,
        shiji=shiji,
    )
    generals = host_guest_generals(
        calculations["host_calc"],
        calculations["guest_calc"],
    )
    return {
        "rule_id": "CORE-G6-G7-CHAIN",
        "calculations": calculations,
        "generals": generals,
        "host_calc": calculations["host_calc"],
        "guest_calc": calculations["guest_calc"],
        "host_big_general_palace": generals["host"]["big_general_palace"],
        "host_assistant_general_palace": generals["host"]["assistant_general_palace"],
        "guest_big_general_palace": generals["guest"]["big_general_palace"],
        "guest_assistant_general_palace": generals["guest"]["assistant_general_palace"],
        "any_blocked": generals["any_blocked"],
        "policy": "G7只消费G6结果；不得在G7重新推目位或重算主客算。",
    }
