"""C55 十精天皇 / 帝符：十六神重留位置 runtime。

主来源：
- 《太乙统宗宝鉴》卷十八 / 卷二十“明十精太乙所主”；
- 十六神名位依《太乙统宗宝鉴》卷二，并复用本库 taiyi_rules canonical。

参校：
- 《武经总要》后集卷十八；
- 《太白兵备统宗宝鉴》“太乙十精”。

边界：
- 天皇 / 帝符均为大周200、小周20；
- 小周20不是20个不同神位，而是十六神顺行并在四处重留一算；
- 阴局按《统宗》“取阳局对冲”逐步映射，不改写成另一套无来源逆行表；
- 盈差异文全部只留证，不应用；
- 不计算十精云气断事。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import GOD_POSITION, GODS, SIXTEEN, integer

C55_VERSION = "taiyi-c55-ten-essences-sixteen-god-routes-v1"

GOD_BY_POSITION = dict(zip(SIXTEEN, GODS))

TIANHUANG_YANG_GOD_PATH = (
    "武德", "太簇", "阴主", "阴德", "阴德",
    "大义", "地主", "阳德", "和德", "和德",
    "吕申", "高丛", "太阳", "大炅", "大炅",
    "大神", "大威", "天道", "大武", "大武",
)

DIFU_YANG_GOD_PATH = (
    "阴主", "阴德", "大义", "地主", "地主",
    "阳德", "和德", "吕申", "高丛", "高丛",
    "太阳", "大炅", "大神", "大威", "大威",
    "天道", "大武", "武德", "太簇", "太簇",
)

TIANHUANG_REPEAT_GODS = frozenset(("阴德", "和德", "大炅", "大武"))
DIFU_REPEAT_GODS = frozenset(("地主", "高丛", "大威", "太簇"))

SOURCE_WITNESS = {
    "天皇": {
        "work": "太乙统宗宝鉴",
        "witness_volumes": [18, 20],
        "big_cycle": 200,
        "small_cycle": 20,
        "tongzong": (
            "命起武德，顺行十六宫间之神；遇阴德、和德、大炅、大武"
            "四维之地重留一算；阴局取阳局对冲。"
        ),
        "wujing_zongyao": (
            "小周二十，命武德顺行十六神，四维相关神位重留；"
            "另见阴起吕申逆行读法，仅作参校异文。"
        ),
        "taibai_bingbei": "阳起申、阴起寅，顺行正间十六宫，四维之宫重留一算。",
        "source_status": "tongzong_primary_with_collation_variant",
    },
    "帝符": {
        "work": "太乙统宗宝鉴",
        "witness_volumes": [18, 20],
        "big_cycle": 200,
        "small_cycle": 20,
        "tongzong": (
            "命起阴主，顺行十六宫间之神；遇地主、高丛、大威、太簇"
            "四正之地重留一算；阴局取阳局对冲。"
        ),
        "wujing_zongyao": (
            "小周二十，命起阴主，顺行十六神，四正相关神位重留；"
            "另见阴起太阳逆行读法，仅作参校异文。"
        ),
        "taibai_bingbei": "阳起戌、阴起辰，顺行正间十六宫，四正之宫重留一算。",
        "source_status": "tongzong_primary_with_collation_variant",
    },
}

SURPLUS_REJECTION = {
    "天皇": {
        "witness_values": {"volume18": 14, "volume20": 14},
        "apply": False,
        "reason": "正文明确诸家经旨并无所加之术，止依古法，不采用神盈差。",
    },
    "帝符": {
        "witness_values": {"volume18": 17, "volume20_or_ocr_variant": 70},
        "apply": False,
        "reason": (
            "见证有17/70异读，但正文同时明确诸家经旨并无所加之术；"
            "两值均只留证，不进入runtime。"
        ),
    },
}

LEGACY_AUDIT = {
    "config.tian_wang": {
        "canonical_equivalent": False,
        "legacy_small_cycle": 20,
        "direct_big_cycle": 200,
        "direct_small_cycle": 20,
        "issue": "周期相合不等于公式相合；canonical必须保存十六神顺行、四维重留及阴局对冲。",
    },
    "config.kingfu": {
        "canonical_equivalent": False,
        "legacy_small_cycle": 20,
        "direct_big_cycle": 200,
        "direct_small_cycle": 20,
        "issue": "周期相合不等于公式相合；canonical必须保存四正重留及帝符/地符名称边界。",
    },
}


def _opposite(point: str) -> str:
    idx = SIXTEEN.index(point)
    return SIXTEEN[(idx + 8) % 16]


def _cycle_state(accumulated_count: int) -> dict[str, int]:
    count = integer(accumulated_count, 1)
    big_remainder = count % 200
    big_cycle_year = big_remainder or 200
    small_remainder = big_cycle_year % 20
    small_cycle_year = small_remainder or 20
    return {
        "accumulated_count": count,
        "big_cycle": 200,
        "big_cycle_remainder": big_remainder,
        "big_cycle_year": big_cycle_year,
        "small_cycle": 20,
        "small_cycle_remainder": small_remainder,
        "small_cycle_year": small_cycle_year,
    }


def _validate_dun(dun: str) -> str:
    if dun not in ("阳", "阴"):
        raise ValueError("dun须为阳/阴")
    return dun


def _position(
    *,
    essence: str,
    accumulated_count: int,
    dun: str,
    yang_god_path: tuple[str, ...],
    repeat_gods: frozenset[str],
    rule_id: str,
) -> dict[str, Any]:
    dun = _validate_dun(dun)
    cycle = _cycle_state(accumulated_count)
    index = cycle["small_cycle_year"] - 1

    yang_god = yang_god_path[index]
    yang_point = GOD_POSITION[yang_god]
    point = yang_point if dun == "阳" else _opposite(yang_point)
    god = GOD_BY_POSITION[point]

    visit_ordinal = sum(
        1
        for prior_god in yang_god_path[: index + 1]
        if GOD_POSITION[prior_god] == yang_point
    )

    return {
        "schema_version": "1.0",
        "canonical": C55_VERSION,
        "rule_id": rule_id,
        "source_profile": "tongzong_ten_essences_sixteen_god_routes",
        "essence": essence,
        "dun": dun,
        **cycle,
        "path_index": index + 1,
        "position": point,
        "god": god,
        "yang_reference_position": yang_point,
        "yang_reference_god": yang_god,
        "opposition_applied": dun == "阴",
        "repeat_location": yang_god in repeat_gods,
        "repeat_visit_ordinal": visit_ordinal,
        "surplus_applied": False,
        "surplus_policy": copy.deepcopy(SURPLUS_REJECTION[essence]),
        "cloud_omen_applied": False,
        "source_witness": copy.deepcopy(SOURCE_WITNESS[essence]),
        "policy": (
            "按《统宗》200/20与十六神重留路线求阳局；阴局逐步取阳局对冲。"
            "参校中的逆行读法保留为source variant，不覆盖统宗主profile；"
            "所有盈差均隔离，不计算十精云气断事。"
        ),
    }


def tianhuang_position(accumulated_count: int, *, dun: str) -> dict[str, Any]:
    """天皇：四维位置重留，20算完成一小周。"""
    return _position(
        essence="天皇",
        accumulated_count=accumulated_count,
        dun=dun,
        yang_god_path=TIANHUANG_YANG_GOD_PATH,
        repeat_gods=TIANHUANG_REPEAT_GODS,
        rule_id="C55-TIANHUANG",
    )


def difu_position(accumulated_count: int, *, dun: str) -> dict[str, Any]:
    """帝符：四正位置重留，20算完成一小周。"""
    return _position(
        essence="帝符",
        accumulated_count=accumulated_count,
        dun=dun,
        yang_god_path=DIFU_YANG_GOD_PATH,
        repeat_gods=DIFU_REPEAT_GODS,
        rule_id="C55-DIFU",
    )


def c55_catalog() -> dict[str, Any]:
    return {
        "canonical": C55_VERSION,
        "rule_ids": ["C55-TIANHUANG", "C55-DIFU"],
        "implemented": ["天皇", "帝符"],
        "delegated_position_runtime": {"天时": "C56-TIANSHI"},
        "pending_position": [],
        "repeat_counts": {"天皇": 4, "帝符": 4},
        "surplus_rejection": copy.deepcopy(SURPLUS_REJECTION),
        "legacy_audit": copy.deepcopy(LEGACY_AUDIT),
        "cloud_omen_runtime": False,
    }
