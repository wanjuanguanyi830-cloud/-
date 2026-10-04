"""C53 十精位置 runtime：飞鸟、五风。

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
}


def _dun(value: str) -> str:
    if value not in ("阳", "阴"):
        raise ValueError("dun须为阳/阴")
    return value


def _cycle_state(accumulated_count: int) -> dict[str, int]:
    count = integer(accumulated_count, 1)
    big_remainder = count % 90
    big_cycle_year = big_remainder or 90
    small_remainder = big_cycle_year % 9
    small_cycle_year = small_remainder or 9
    return {
        "accumulated_count": count,
        "big_cycle": 90,
        "big_cycle_remainder": big_remainder,
        "big_cycle_year": big_cycle_year,
        "small_cycle": 9,
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
) -> dict[str, Any]:
    dun = _dun(dun)
    cycle = _cycle_state(accumulated_count)
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
        "surplus_policy": copy.deepcopy(SURPLUS_REJECTION[essence]),
        "source_witness": copy.deepcopy(SOURCE_WITNESS[essence]),
        "cloud_omen_applied": False,
        "policy": (
            "只按显式阴阳遁、90大周与9小周求位置；"
            "不自动推遁，不采用被正文否定的宫盈差，不附带十精云气断语。"
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


def c53_runtime_catalog() -> dict[str, Any]:
    return {
        "canonical": C53_VERSION,
        "rule_ids": ["C53-FLYBIRD", "C53-FIVEWIND"],
        "implemented": ["飞鸟", "五风"],
        "pending": ["天皇", "帝符", "天时", "太尊", "五行", "八风", "三风", "太乙数"],
        "legacy_audit": copy.deepcopy(LEGACY_AUDIT),
        "surplus_rejection": copy.deepcopy(SURPLUS_REJECTION),
        "cloud_omen_runtime": False,
        "pan_contract_extended": False,
    }
