"""C45 《太乙统宗宝鉴》岁中灾发月日之期严格来源模型。

两阶段：
1. 太岁合神加岁支，视文昌/天目所临 -> 灾发月；冲处亦然。
2. 当月合神再加当月支，视文昌/天目所临 -> 灾发日支；冲处亦然。

本模块不自行实现“合神加支”的盘式旋转，只消费上游明确落点。
"""

from __future__ import annotations

import copy
from typing import Any

C45_VERSION = "taiyi-c45-volume9-disaster-timing-v1"

BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
SIXTEEN_POINTS = tuple("子丑艮寅卯辰巽巳午未坤申酉戌乾亥")
BRANCH_MONTH = {
    "寅": 1, "卯": 2, "辰": 3, "巳": 4, "午": 5, "未": 6,
    "申": 7, "酉": 8, "戌": 9, "亥": 10, "子": 11, "丑": 12,
}

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "online_witness_volume": 10,
    "project_legacy_volume_label": 9,
    "volume_status": "witness_volume_variant",
    "section": "明岁中灾发月日之期术",
}

SOURCE_PATTERNS = frozenset({"格", "掩", "迫", "击", "挟", "提", "挟提"})

LEGACY_REFERENCE_AUDIT = {
    "function": "guiyun.suizhong_zaifa",
    "canonical_equivalent": False,
    "issues": [
        "旧函数把year_zhi/hegod_zhi/skyeyes_chen作十六位offset，未证明等价于“合神加岁支”盘式",
        "只输出月层，未实现当月合神再加月支求日支期",
        "自建_YANG_GONG集合推旱水，原文只说文昌临阳宫/阴宫",
        "未显式检查文昌加在太乙宫",
        "未把格掩迫击挟提作为独立结构化证据",
    ],
}


def _branch(value: str, name: str) -> str:
    if value not in BRANCHES:
        raise ValueError(f"{name}须为十二地支")
    return value


def _point(value: str, name: str) -> str:
    if value not in SIXTEEN_POINTS:
        raise ValueError(f"{name}须为十六宫点")
    return value


def opposite_point(point: str) -> str:
    point = _point(point, "point")
    index = SIXTEEN_POINTS.index(point)
    return SIXTEEN_POINTS[(index + 8) % 16]


def month_for_point(point: str) -> int | None:
    point = _point(point, "point")
    return BRANCH_MONTH.get(point)


def _patterns(value: list[str] | None) -> tuple[list[str], bool]:
    if value is None:
        return [], False
    if not isinstance(value, list):
        raise TypeError("pattern_evidence须为list或None")
    unknown = [item for item in value if item not in SOURCE_PATTERNS]
    if unknown:
        raise ValueError(f"未知岁中灾发格局: {', '.join(unknown)}")
    return list(value), True


def disaster_month_from_evidence(
    *,
    year_branch: str,
    year_hegod_anchor: str,
    wenchang_landing_after_year_addition: str,
    palace_polarity: str | None = None,
    wenchang_same_as_taiyi: bool | None = None,
    pattern_evidence: list[str] | None = None,
) -> dict[str, Any]:
    """月层：只消费“合神加岁支”后的显式文昌落点。"""
    year_branch = _branch(year_branch, "year_branch")
    hegod = _point(year_hegod_anchor, "year_hegod_anchor")
    landing = _point(
        wenchang_landing_after_year_addition,
        "wenchang_landing_after_year_addition",
    )
    opposite = opposite_point(landing)
    month = month_for_point(landing)
    opposite_month = month_for_point(opposite)

    if palace_polarity not in (None, "阳", "阴"):
        raise ValueError("palace_polarity须为阳/阴或None")
    if wenchang_same_as_taiyi not in (None, True, False):
        raise TypeError("wenchang_same_as_taiyi须为bool或None")
    patterns, patterns_checked = _patterns(pattern_evidence)

    pending = []
    if month is None:
        pending.append("文昌落四维宫时，当前直接条文未给月份换算，不自行折月")
    if opposite_month is None:
        pending.append("冲处落四维宫时，当前直接条文未给月份换算")
    if palace_polarity is None:
        pending.append("须由上游明确文昌所临宫为阳宫或阴宫")
    if wenchang_same_as_taiyi is None:
        pending.append("须显式说明文昌是否加在太乙宫")
    if not patterns_checked:
        pending.append("须显式检查格掩迫击挟提；无格局时传空list")

    water_drought = (
        "旱" if palace_polarity == "阳"
        else "水" if palace_polarity == "阴"
        else None
    )
    bad_year = (
        None
        if wenchang_same_as_taiyi is None or not patterns_checked
        else bool(wenchang_same_as_taiyi or patterns)
    )

    computable = not pending
    return {
        "schema_version": "1.0",
        "canonical": C45_VERSION,
        "rule_id": "C45-V9-MONTH",
        "source_profile": "tongzong_volume9_disaster_timing",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "year_branch": year_branch,
        "year_hegod_anchor": hegod,
        "addition_formula_applied": False,
        "wenchang_landing": landing,
        "opposite_landing": opposite,
        "disaster_month": month,
        "opposite_disaster_month": opposite_month,
        "palace_polarity": palace_polarity,
        "water_drought": water_drought,
        "wenchang_same_as_taiyi": wenchang_same_as_taiyi,
        "pattern_evidence": patterns,
        "annual_disorder": (
            "君臣不协、岁不丰稔" if bad_year is True
            else None
        ),
        "annual_disorder_triggered": bad_year,
        "computable": computable,
        "status": "computed_from_explicit_source_evidence" if computable else "not_computable",
        "pending": pending,
        "legacy_yang_palace_guess_used": False,
        "policy": (
            "月份只按显式文昌落支及其冲支换算；"
            "文昌宫性由上游给定，不从十六点自造阴阳宫表。"
            "太乙同宫与格掩迫击挟提只作年度不协/不稔证据，不改月份。"
        ),
    }


def disaster_day_from_evidence(
    *,
    month_branch: str,
    month_hegod_anchor: str,
    wenchang_landing_after_month_addition: str,
) -> dict[str, Any]:
    """日层：输出灾发日支候选及冲支，不伪造具体月日数字。"""
    month_branch = _branch(month_branch, "month_branch")
    hegod = _point(month_hegod_anchor, "month_hegod_anchor")
    landing = _point(
        wenchang_landing_after_month_addition,
        "wenchang_landing_after_month_addition",
    )
    opposite = opposite_point(landing)

    return {
        "schema_version": "1.0",
        "canonical": C45_VERSION,
        "rule_id": "C45-V9-DAY",
        "source_profile": "tongzong_volume9_disaster_timing",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "month_branch": month_branch,
        "month_hegod_anchor": hegod,
        "addition_formula_applied": False,
        "wenchang_landing": landing,
        "disaster_day_branch": landing,
        "opposite_day_branch": opposite,
        "specific_calendar_day": None,
        "specific_calendar_day_status": "source_only_gives_landing_branch_period",
        "computable": True,
        "policy": "第二阶段只落到支位及冲支；无另一步历法换算时不伪造某月某日数字。",
    }


def disaster_timing_from_evidence(
    month_stage: dict[str, Any],
    day_stage: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """合并两阶段；两阶段都明确才视为完整“月日之期”替代。"""
    if not isinstance(month_stage, dict) or month_stage.get("rule_id") != "C45-V9-MONTH":
        raise ValueError("month_stage必须来自C45-V9-MONTH")
    if day_stage is not None:
        if not isinstance(day_stage, dict) or day_stage.get("rule_id") != "C45-V9-DAY":
            raise ValueError("day_stage必须来自C45-V9-DAY")

    month_ok = month_stage.get("computable") is True
    day_ok = day_stage is not None and day_stage.get("computable") is True
    complete = month_ok and day_ok

    return {
        "schema_version": "1.0",
        "canonical": C45_VERSION,
        "rule_id": "C45-V9-DISASTER",
        "source_profile": "tongzong_volume9_disaster_timing",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "month_stage": copy.deepcopy(month_stage),
        "day_stage": copy.deepcopy(day_stage) if day_stage is not None else {},
        "computable": complete,
        "status": (
            "complete_month_day_timing" if complete
            else "partial_month_only" if month_ok
            else "not_computable"
        ),
        "cross_stage_merge": False,
        "policy": "月层与日层各自保留输入和证据；日层缺失时不得把旧月断语冒充完整‘月日之期’。",
    }


def build_volume9_disaster_source_variant(
    result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if result is None:
        result = {}
    if not isinstance(result, dict):
        raise TypeError("result须为dict或None")
    if result:
        if result.get("rule_id") != "C45-V9-DISASTER":
            raise ValueError("result必须来自C45-V9-DISASTER")
        if result.get("source_profile") != "tongzong_volume9_disaster_timing":
            raise ValueError("C45 source_profile不匹配")

    complete = bool(result and result.get("computable") is True)
    return {
        "schema_version": "1.0",
        "canonical": C45_VERSION,
        "result": copy.deepcopy(result),
        "legacy_replacement": (
            {"source_replacement_complete": True, "rule_id": "C45-V9-DISASTER"}
            if complete
            else {}
        ),
        "legacy_reference_audit": copy.deepcopy(LEGACY_REFERENCE_AUDIT),
        "cross_source_merge": False,
        "policy": "旧岁中灾发只有月、日两阶段均完成的C45结果才清除migration gap。",
    }
