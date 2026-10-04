"""C53 九宫/四正型十精位置 runtime：飞鸟、五风、太尊、八风、三风、五行。

直接来源：
- 《太乙统宗宝鉴》十精太乙所主
- 《武经总要》十精小周法
- 《太白兵备统宗宝鉴》阴阳起宫、顺逆参校

边界：
- 调用方必须显式给阳遁/阴遁；
- 不从日期自动推遁；
- 不采用正文明确否定的宫盈差；
- 不计算十精云气断事。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer

C53_VERSION = "taiyi-c53-ten-essences-flybird-fivewind-v1"

PALACE_LABELS = {
    1: "乾",
    2: "离",
    3: "艮",
    4: "震",
    5: "中",
    6: "兑",
    7: "坤",
    8: "坎",
    9: "巽",
}

FLYBIRD_PATHS = {
    "阳": (1, 2, 3, 4, 5, 6, 7, 8, 9),
    "阴": (9, 8, 7, 6, 5, 4, 3, 2, 1),
}

FIVEWIND_PATHS = {
    "阳": (1, 3, 5, 7, 9, 2, 4, 6, 8),
    "阴": (9, 7, 5, 3, 1, 8, 6, 4, 2),
}

TAIZUN_PATHS = {
    "阳": (8, 6, 2, 4),
    "阴": (2, 4, 8, 6),
}

EIGHTWIND_PATHS = {
    "阳": (2, 3, 4, 5, 6, 7, 8, 9, 1),
    "阴": (8, 7, 6, 5, 4, 3, 2, 1, 9),
}

THREEWIND_PATHS = {
    "阳": (3, 7, 2, 6, 1, 5, 9, 4, 8),
    "阴": (7, 3, 8, 4, 9, 5, 1, 6, 2),
}

WUXING_PATHS = {
    "阳": (1, 8, 3, 9, 7),
    "阴": (9, 2, 7, 1, 3),
}

SOURCE_WITNESS = {
    "飞鸟": {
        "work": "太乙统宗宝鉴",
        "witness_volumes": [18, 20],
        "big_cycle": 90,
        "small_cycle": 9,
        "tongzong": "余命起一宫，顺行九宫；宫盈差三古法皆无所加，故不取用",
        "wujing_zongyao": "飞鸟小周九，命起一宫，顺行九宫",
        "taibai_bingbei": "阳起于乾，阴起于巽，阳顺阴逆，游行九宫",
        "source_status": "direct_with_independent_collation",
    },
    "太尊": {
        "work": "太乙统宗宝鉴",
        "witness_volumes": [18, 20],
        "big_cycle": 40,
        "small_cycle": 4,
        "tongzong": "以大周四十、小周四；按八六二四四正之宫逆行",
        "wujing_zongyao": "太尊小周四，命起八宫，次六宫、二宫、四宫，逆行四正宫",
        "taibai_bingbei": "阳起坎八、阴起离二，逆行坎兑离震四正宫",
        "source_status": "direct_route_with_independent_collation",
    },
    "八风": {
        "work": "太乙统宗宝鉴",
        "witness_volumes": [18, 20],
        "big_cycle": 90,
        "small_cycle": 9,
        "tongzong": "命起二宫，次三宫，次第顺行九宫；所加宫差古经不载，故不取用",
        "wujing_zongyao": "八风小周九，命起二宫，顺行九宫",
        "taibai_bingbei": "阳起离二顺行九宫；阴起坎八逆行九宫",
        "source_status": "direct_route_with_independent_collation",
    },
    "三风": {
        "work": "太乙统宗宝鉴",
        "witness_volumes": [18, 20],
        "big_cycle": 90,
        "small_cycle": 9,
        "tongzong": "命起三，次七二六一五九四八，依次而行；附加盈差古法无此，故不取用",
        "wujing_zongyao": "一见证作起五宫，次七二六一五九四八，保留为异文",
        "taibai_bingbei": (
            "阳起三，次七二六一五九四八；"
            "阴起七，次三八四九五一六二"
        ),
        "source_status": "direct_primary_with_collation_variant",
    },
    "五行": {
        "work": "太乙统宗宝鉴",
        "witness_volumes": [18, 20],
        "big_cycle": 50,
        "small_cycle": 5,
        "tongzong": "命起一八三九七宫，周而复始；阴局取阳局对冲",
        "wujing_zongyao": "五行小周五，命起一宫，次八三九七",
        "taibai_bingbei": (
            "阳起乾一，顺行坎八、艮三、巽九、坤七；"
            "阴起巽九，顺行离二、坤七、乾一、艮三"
        ),
        "source_status": "direct_route_with_independent_collation",
    },
    "五风": {
        "work": "太乙统宗宝鉴",
        "witness_volumes": [18, 20],
        "big_cycle": 90,
        "small_cycle": 9,
        "tongzong": (
            "余命起一三五七九、二四六八之宫，先阳后阴次第；"
            "宫盈差三等古法不载，故不取用"
        ),
        "wujing_zongyao": "五风小周九，命起一宫，次三五九七二四六八（文本异序保留参校）",
        "taibai_bingbei": (
            "阳起乾一，先奇后耦顺行；"
            "阴起巽九，逆行坤七、中五、艮三、乾一、坎八、兑六、震四、离二"
        ),
        "source_status": "direct_route_with_collation_variant",
    },
}

LEGACY_AUDIT = {
    "config.flybird": {
        "canonical_equivalent": False,
        "legacy_outer_modulus": 8,
        "direct_big_cycle": 90,
        "direct_small_cycle": 9,
        "issue": "旧%8并按八宫表返回，遗漏中五且与直接小周9冲突。",
    },
    "config.wuxing": {
        "canonical_equivalent": False,
        "legacy_outer_modulus": 5,
        "direct_big_cycle": 50,
        "direct_small_cycle": 5,
        "issue": "旧周期表面相合，但未保存阴阳两条来源路径；C53以直接路径重建，不直接复用旧函数。",
    },
    "config.taijun": {
        "canonical_equivalent": False,
        "legacy_outer_modulus": 4,
        "direct_big_cycle": 40,
        "direct_small_cycle": 4,
        "issue": "旧mod4只给子午卯酉，不保存八六二四四正宫来源路径与阴阳起点。",
    },
    "config.eightwind": {
        "canonical_equivalent": False,
        "legacy_outer_modulus": 9,
        "direct_big_cycle": 90,
        "direct_small_cycle": 9,
        "issue": "旧表只列八项且漏中五；直接正文明确顺行九宫。",
    },
    "config.threewind": {
        "canonical_equivalent": False,
        "legacy_outer_modulus": 9,
        "direct_big_cycle": 90,
        "direct_small_cycle": 9,
        "issue": "旧八项表漏正文中的九宫项，余0分支亦不是可审计九步路径。",
    },
    "config.fivewind": {
        "canonical_equivalent": False,
        "legacy_outer_modulus": 29,
        "direct_big_cycle": 90,
        "direct_small_cycle": 9,
        "issue": "旧%29无直接依据；正文明确大周90、小周9。",
    },
}

SURPLUS_REJECTION = {
    "飞鸟": {
        "legacy_or_variant_surplus": {"palace": 3},
        "apply": False,
        "reason": "正文明确“古法皆无所加，故不取用”。",
    },
    "五风": {
        "legacy_or_variant_surplus": {"palace": 3, "day": 6},
        "apply": False,
        "reason": "正文明确该加差古法不载，故不取用。",
    },
    "八风": {
        "legacy_or_variant_surplus": {"palace": 4, "month_day_hour": 2},
        "apply": False,
        "reason": "正文明确右经书不载，故不取用。",
    },
    "三风": {
        "legacy_or_variant_surplus": {"palace": 8, "month_hour": 5, "day": 2},
        "apply": False,
        "reason": "正文明确考之于古皆无此术，故不取用。",
    },
}


def _dun(value: str) -> str:
    if value not in ("阳", "阴"):
        raise ValueError("dun须为阳/阴")
    return value


def _cycle_state(
    accumulated_count: int,
    *,
    big_cycle: int,
    small_cycle: int,
) -> dict[str, int]:
    count = integer(accumulated_count, 1)
    big_remainder = count % big_cycle
    big_cycle_year = big_remainder or big_cycle
    small_remainder = big_cycle_year % small_cycle
    small_cycle_year = small_remainder or small_cycle
    return {
        "accumulated_count": count,
        "big_cycle": big_cycle,
        "big_cycle_remainder": big_remainder,
        "big_cycle_year": big_cycle_year,
        "small_cycle": small_cycle,
        "small_cycle_remainder": small_remainder,
        "small_cycle_year": small_cycle_year,
    }


def _position(
    *,
    essence: str,
    accumulated_count: int,
    dun: str,
    paths: dict[str, tuple[int, ...]],
    rule_id: str,
    big_cycle: int = 90,
    small_cycle: int = 9,
) -> dict[str, Any]:
    dun = _dun(dun)
    cycle = _cycle_state(
        accumulated_count,
        big_cycle=big_cycle,
        small_cycle=small_cycle,
    )
    path = paths[dun]
    index = cycle["small_cycle_year"] - 1
    palace = path[index]

    return {
        "schema_version": "1.0",
        "canonical": C53_VERSION,
        "rule_id": rule_id,
        "source_profile": "tongzong_ten_essences_positions",
        "essence": essence,
        "dun": dun,
        **cycle,
        "path": list(path),
        "path_index": index + 1,
        "palace": palace,
        "palace_label": PALACE_LABELS[palace],
        "surplus_applied": False,
        "surplus_policy": copy.deepcopy(SURPLUS_REJECTION.get(essence)),
        "source_witness": copy.deepcopy(SOURCE_WITNESS[essence]),
        "cloud_omen_applied": False,
        "policy": (
            "只按显式阴阳遁与本十精直接大周/小周求位置；"
            "不自动推遁，不采用正文否定的附加盈差，不附带十精云气断语。"
        ),
    }


def flybird_position(accumulated_count: int, *, dun: str) -> dict[str, Any]:
    """十精飞鸟位置；不是 J4M-11 外部飞鸟观测。"""
    result = _position(
        essence="飞鸟",
        accumulated_count=accumulated_count,
        dun=dun,
        paths=FLYBIRD_PATHS,
        rule_id="C53-FLYBIRD",
    )
    result["same_name_boundary"] = {
        "j4m11_external_observation": False,
        "policy": "十精飞鸟宫位不得伪造军事飞鸟观测。",
    }
    return result


def fivewind_position(accumulated_count: int, *, dun: str) -> dict[str, Any]:
    """十精五风位置。"""
    return _position(
        essence="五风",
        accumulated_count=accumulated_count,
        dun=dun,
        paths=FIVEWIND_PATHS,
        rule_id="C53-FIVEWIND",
    )


def taizun_position(accumulated_count: int, *, dun: str) -> dict[str, Any]:
    """十精太尊位置：40大周、4小周、四正宫。"""
    return _position(
        essence="太尊",
        accumulated_count=accumulated_count,
        dun=dun,
        paths=TAIZUN_PATHS,
        rule_id="C53-TAIZUN",
        big_cycle=40,
        small_cycle=4,
    )


def eightwind_position(accumulated_count: int, *, dun: str) -> dict[str, Any]:
    """十精八风位置：90大周、9小周。"""
    return _position(
        essence="八风",
        accumulated_count=accumulated_count,
        dun=dun,
        paths=EIGHTWIND_PATHS,
        rule_id="C53-EIGHTWIND",
    )


def threewind_position(accumulated_count: int, *, dun: str) -> dict[str, Any]:
    """十精三风位置；武经起五宫异文仅保留见证，不覆盖统宗主序。"""
    return _position(
        essence="三风",
        accumulated_count=accumulated_count,
        dun=dun,
        paths=THREEWIND_PATHS,
        rule_id="C53-THREEWIND",
    )


def wuxing_position(accumulated_count: int, *, dun: str) -> dict[str, Any]:
    """十精五行位置：50大周、5小周。"""
    return _position(
        essence="五行",
        accumulated_count=accumulated_count,
        dun=dun,
        paths=WUXING_PATHS,
        rule_id="C53-WUXING",
        big_cycle=50,
        small_cycle=5,
    )


def c53_runtime_catalog() -> dict[str, Any]:
    return {
        "canonical": C53_VERSION,
        "rule_ids": [
            "C53-FLYBIRD",
            "C53-FIVEWIND",
            "C53-TAIZUN",
            "C53-EIGHTWIND",
            "C53-THREEWIND",
            "C53-WUXING",
        ],
        "implemented": ["飞鸟", "五风", "太尊", "八风", "三风", "五行"],
        "delegated_position_runtimes": {
            "天皇": "C55-TIANHUANG",
            "帝符": "C55-DIFU",
            "天时": "C56-TIANSHI",
        },
        "number_runtime": "C54-TAIYI-NUMBER",
        "pending": [],
        "legacy_audit": copy.deepcopy(LEGACY_AUDIT),
        "surplus_rejection": copy.deepcopy(SURPLUS_REJECTION),
        "cloud_omen_runtime": False,
        "pan_contract_extended": False,
    }
