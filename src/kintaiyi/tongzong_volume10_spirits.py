"""《太乙统宗宝鉴》卷十：三旗行宫与九宫贵神。

本模块只实现卷十可直接证明的位置/会合层。
所有计数采用古法“算外”的1基段界，不沿用旧参考代码的0基索引习惯。
"""

from __future__ import annotations

import copy
from collections import Counter
from typing import Any

from .taiyi_rules import integer

VERSION = "taiyi-tongzong-volume10-spirits-v1"

BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
REVERSE_BRANCHES_FROM_HAI = ("亥", "戌", "酉", "申", "未", "午", "巳", "辰", "卯", "寅", "丑", "子")
FOUR_MENG_REVERSE = ("亥", "申", "巳", "寅")

LUOSHU_PALACES = {
    1: "坎",
    2: "坤",
    3: "震",
    4: "巽",
    5: "中",
    6: "乾",
    7: "兑",
    8: "艮",
    9: "离",
}

NOBLE_GODS = {
    1: "太乙",
    2: "摄提",
    3: "轩辕",
    4: "招摇",
    5: "天符",
    6: "青龙",
    7: "咸池",
    8: "太阴",
    9: "天乙",
}

# 小周余1..9所得直事神。原文例“余三，即得太阴”。
DIRECT_GOD_NUMBERS = (1, 9, 8, 7, 6, 5, 4, 3, 2)

# 直事神钧入中宫后，“相次之神飞出乾宫，依次顺行河图九宫”。
# 卷十余三例：太阴(8)中；天乙(9)乾；太乙(1)兑；摄提(2)艮；
# 轩辕(3)离；招摇(4)坎；天符(5)坤；青龙(6)震；咸池(7)巽。
FLY_PALACE_NUMBERS = (6, 7, 8, 9, 1, 2, 3, 4)

SOURCE_WITNESS = {
    "three_banners": {
        "primary": {
            "work": "太乙统宗宝鉴",
            "volume": 10,
            "witness_id": "NGJ892411999009267118912",
            "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny52hi7lfec",
        },
        "parallel": {
            "work": "太乙统宗宝鉴",
            "witness_id": "CADAL02055529",
            "url": "https://www.shidianguji.com/book/CADAL02055529/chapter/1l5erkijq3nl5",
            "note": "OCR数值有讹；三年一移/三十六年一周与四孟一年一移/四年一周可互校边界。",
        },
    },
    "nine_palace_nobles": {
        "primary": {
            "work": "太乙统宗宝鉴",
            "volume": 10,
            "witness_id": "NGJ892411999009267118912",
            "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny52hi7lfec",
            "direct_example": "小周余三，即得太阴；太阴钧入中宫。",
        },
        "parallel": {
            "work": "易学象数论",
            "statement": "周纪三百六十、纪法六十、宫周九、宫盈差三；余起一宫逆行。",
        },
    },
}


def _cycle_count(value: int, cycle: int) -> tuple[int, int]:
    remainder = value % cycle
    return remainder, remainder or cycle


def qinglong_banner(accumulated_year: int) -> dict[str, Any]:
    """太岁青龙旗：纪法60，小周12，余1起子，顺十二辰。"""
    count = integer(accumulated_year, 1)
    sixty_remainder, sixty_count = _cycle_count(count, 60)
    twelve_remainder, twelve_count = _cycle_count(sixty_count, 12)
    return {
        "name": "太岁青龙旗",
        "branch": BRANCHES[twelve_count - 1],
        "accumulated_year": count,
        "cycle_60_remainder": sixty_remainder,
        "cycle_60_count": sixty_count,
        "cycle_12_remainder": twelve_remainder,
        "cycle_12_count": twelve_count,
        "year_in_branch": 1,
        "direction": "forward",
        "start_rule": "余1=子；余12/0=亥；下一年复子",
    }


def taiyin_black_banner(accumulated_year: int) -> dict[str, Any]:
    """太阴黑旗：+25，360/36，三年一移，亥起逆十二辰。"""
    count = integer(accumulated_year, 1)
    adjusted = count + 25
    outer_remainder, outer_count = _cycle_count(adjusted, 360)
    small_remainder, small_count = _cycle_count(outer_count, 36)
    zero_index = small_count - 1
    branch_index = zero_index // 3
    year_in_branch = zero_index % 3 + 1
    return {
        "name": "太阴黑旗",
        "branch": REVERSE_BRANCHES_FROM_HAI[branch_index],
        "accumulated_year": count,
        "surplus": 25,
        "adjusted_count": adjusted,
        "outer_cycle": 360,
        "outer_remainder": outer_remainder,
        "outer_count": outer_count,
        "small_cycle": 36,
        "small_remainder": small_remainder,
        "small_count": small_count,
        "years_per_branch": 3,
        "year_in_branch": year_in_branch,
        "direction": "reverse",
        "start_rule": "小周第1..3年均在亥；第4..6年在戌",
    }


def haiqi_red_banner(accumulated_year: int) -> dict[str, Any]:
    """害气赤旗：+1，40/4，亥起逆四孟，一年一移。"""
    count = integer(accumulated_year, 1)
    adjusted = count + 1
    outer_remainder, outer_count = _cycle_count(adjusted, 40)
    small_remainder, small_count = _cycle_count(outer_count, 4)
    return {
        "name": "害气赤旗",
        "branch": FOUR_MENG_REVERSE[small_count - 1],
        "accumulated_year": count,
        "surplus": 1,
        "adjusted_count": adjusted,
        "outer_cycle": 40,
        "outer_remainder": outer_remainder,
        "outer_count": outer_count,
        "small_cycle": 4,
        "small_remainder": small_remainder,
        "small_count": small_count,
        "year_in_branch": 1,
        "direction": "reverse",
        "path": list(FOUR_MENG_REVERSE),
        "start_rule": "小周余1=亥，余2=申，余3=巳，余4/0=寅",
    }


def three_banners(accumulated_year: int) -> dict[str, Any]:
    """C126：三旗位置及三旗彼此会合，不自动制造与太乙的会合。"""
    qinglong = qinglong_banner(accumulated_year)
    taiyin = taiyin_black_banner(accumulated_year)
    haiqi = haiqi_red_banner(accumulated_year)
    flags = {
        "太岁青龙旗": qinglong["branch"],
        "太阴黑旗": taiyin["branch"],
        "害气赤旗": haiqi["branch"],
    }
    counts = Counter(flags.values())
    meeting_branches = sorted(branch for branch, n in counts.items() if n >= 2)
    max_count = max(counts.values())
    if max_count == 3:
        meeting = "三神会合"
        source_omen = "灾急"
    elif max_count == 2:
        meeting = "二神会合"
        source_omen = "灾缓"
    else:
        meeting = None
        source_omen = None
    return {
        "schema_version": "1.0",
        "canonical": VERSION,
        "rule_id": "C126-TONGZONG-THREE-BANNERS",
        "source_profile": "tongzong_volume10_three_banners",
        "source_work": "太乙统宗宝鉴",
        "source_volume": 10,
        "accumulated_year": integer(accumulated_year, 1),
        "flags": flags,
        "details": {
            "太岁青龙旗": qinglong,
            "太阴黑旗": taiyin,
            "害气赤旗": haiqi,
        },
        "meeting": meeting,
        "meeting_branches": meeting_branches,
        "source_omen": source_omen,
        "taiyi_meeting_applied": False,
        "source_witness": copy.deepcopy(SOURCE_WITNESS["three_banners"]),
        "boundary": (
            "只按卷十三旗自身位置与二/三旗会合；若要判断三旗与太乙会合，"
            "必须由上层显式提供太乙位置，不在本函数自动推造。"
        ),
    }


def _direct_god(small_count: int) -> tuple[int, str]:
    god_number = DIRECT_GOD_NUMBERS[small_count - 1]
    return god_number, NOBLE_GODS[god_number]


def nine_palace_nobles(accumulated_year: int) -> dict[str, Any]:
    """C127：九宫贵神直事与钧宫飞行分布。"""
    count = integer(accumulated_year, 1)
    cycle_360_remainder, cycle_360_count = _cycle_count(count, 360)
    adjusted = cycle_360_count + 3
    small_remainder, small_count = _cycle_count(adjusted, 9)
    direct_number, direct_name = _direct_god(small_count)

    by_palace_number: dict[int, str] = {5: direct_name}
    for step, palace_number in enumerate(FLY_PALACE_NUMBERS, start=1):
        god_number = ((direct_number - 1 + step) % 9) + 1
        by_palace_number[palace_number] = NOBLE_GODS[god_number]

    distribution = {
        LUOSHU_PALACES[number]: by_palace_number[number]
        for number in range(1, 10)
    }
    god_locations = {
        god: LUOSHU_PALACES[number]
        for number, god in by_palace_number.items()
    }

    return {
        "schema_version": "1.0",
        "canonical": VERSION,
        "rule_id": "C127-TONGZONG-NINE-PALACE-NOBLES",
        "source_profile": "tongzong_volume10_nine_palace_nobles",
        "source_work": "太乙统宗宝鉴",
        "source_volume": 10,
        "accumulated_year": count,
        "cycle_360_remainder": cycle_360_remainder,
        "cycle_360_count": cycle_360_count,
        "palace_surplus": 3,
        "adjusted_count": adjusted,
        "small_cycle": 9,
        "small_remainder": small_remainder,
        "small_count": small_count,
        "direct_god_number": direct_number,
        "direct_god": direct_name,
        "direct_palace": "中",
        "distribution": distribution,
        "god_locations": god_locations,
        "fly_palace_numbers": list(FLY_PALACE_NUMBERS),
        "source_witness": copy.deepcopy(SOURCE_WITNESS["nine_palace_nobles"]),
        "boundary": (
            "本函数只实现卷十直事神与钧宫飞行；各神灾祥、与五福三基等会合"
            "仍由独立解释层消费显式同宫证据。"
        ),
    }


def volume10_spirit_catalog() -> dict[str, Any]:
    return {
        "canonical": VERSION,
        "rule_ids": [
            "C126-TONGZONG-THREE-BANNERS",
            "C127-TONGZONG-NINE-PALACE-NOBLES",
        ],
        "source_profiles": [
            "tongzong_volume10_three_banners",
            "tongzong_volume10_nine_palace_nobles",
        ],
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "cross_source_merge": False,
        "ziting_backfill_allowed": False,
    }
