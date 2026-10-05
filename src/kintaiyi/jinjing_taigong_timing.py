"""C117 《太乙金镜式经》卷一“推太公考时法”。

本层只解释正文直接列出的出兵/玄命条件，不自动从其他模块生成事实。

关键边界：
- “右太乙左天目”只消费调用方显式判断，不在此重算宫位方位；
- 掩击迫囚关格对、四郭固/杜、提挟等格局只消费显式列表；
- 吉道只认开/休/生，且“清虚”要求显式无凶恶之神；
- 三门具、五将发必须显式输入；
- 玄命所主由 C116 提供，但是否当前确实临其玄命对象必须显式输入；
- “直使前三五、后二四”句读/结构不在 C117 自行解释，必须由调用方显式给 direct_envoy_clause_matched。
"""

from __future__ import annotations

import copy
from typing import Any, Iterable

from .jinjing_xuanming import xuanming_for_role

C117_VERSION = "taiyi-c117-jinjing-taigong-timing-v1"

AUSPICIOUS_DOORS = frozenset(("开", "休", "生"))

BLOCKING_PATTERN_ALIASES = {
    "擊": "击",
    "關": "关",
    "格": "格",
    "對": "对",
    "提挾": "提挟",
    "四郭固": "四郭固",
    "四郭杜": "四郭杜",
}

SOURCE_WITNESS = {
    "work": "太乙金镜式经",
    "volume": 1,
    "section": "推太公考时法",
    "direct_conditions": [
        "右太乙左天目",
        "阴阳和顺",
        "上下无掩击迫囚关格对",
        "无四郭固杜",
        "不提挟",
        "太乙不在阳绝之地",
        "神将独立",
        "吉道清虚",
        "三门具五将发利以行兵",
        "合玄命王相挟和",
        "玄命临旺相之乡，上下相生",
        "直使前三五、后二四合者大吉",
    ],
    "policy": (
        "只按显式条件解释；不调用格局、八门、五将、季节旺衰或六壬模块自动补条件。"
    ),
}

DIRECT_ENVOY_BOUNDARY = {
    "source_text": "门与玄命上天乙直使前三五后二四合者大吉",
    "status": "structure_not_fully_parsed",
    "auto_computation": False,
    "policy": "C117不把‘前三五、后二四’强拆成未经校定的数位算法。",
}


def _bool_or_none(name: str, value: bool | None) -> bool | None:
    if value not in (None, True, False):
        raise TypeError(f"{name}须为bool或None")
    return value


def _normalize_patterns(patterns: Iterable[str] | None) -> list[str] | None:
    if patterns is None:
        return None
    if isinstance(patterns, (str, bytes)):
        raise TypeError("blocking_patterns须为字符串序列或None")
    out: list[str] = []
    for item in patterns:
        if not isinstance(item, str):
            raise TypeError("blocking_patterns元素须为字符串")
        out.append(BLOCKING_PATTERN_ALIASES.get(item, item))
    return out


def evaluate_taigong_timing(
    *,
    right_taiyi_left_tianmu: bool | None,
    yinyang_harmonious: bool | None,
    blocking_patterns: Iterable[str] | None,
    taiyi_in_yang_jue: bool | None,
    spirits_independent: bool | None,
    door: str | None,
    door_has_malefic_spirit: bool | None,
    three_doors_complete: bool | None,
    five_generals_active: bool | None,
    role: str | None = None,
    occupied_xuanming_target: str | None = None,
    xuanming_in_wangxiang: bool | None = None,
    upper_lower_generating: bool | None = None,
    direct_envoy_clause_matched: bool | None = None,
) -> dict[str, Any]:
    """解释“推太公考时法”的显式证据链。"""
    right_taiyi_left_tianmu = _bool_or_none(
        "right_taiyi_left_tianmu", right_taiyi_left_tianmu
    )
    yinyang_harmonious = _bool_or_none("yinyang_harmonious", yinyang_harmonious)
    taiyi_in_yang_jue = _bool_or_none("taiyi_in_yang_jue", taiyi_in_yang_jue)
    spirits_independent = _bool_or_none("spirits_independent", spirits_independent)
    door_has_malefic_spirit = _bool_or_none(
        "door_has_malefic_spirit", door_has_malefic_spirit
    )
    three_doors_complete = _bool_or_none("three_doors_complete", three_doors_complete)
    five_generals_active = _bool_or_none("five_generals_active", five_generals_active)
    xuanming_in_wangxiang = _bool_or_none("xuanming_in_wangxiang", xuanming_in_wangxiang)
    upper_lower_generating = _bool_or_none("upper_lower_generating", upper_lower_generating)
    direct_envoy_clause_matched = _bool_or_none(
        "direct_envoy_clause_matched", direct_envoy_clause_matched
    )
    patterns = _normalize_patterns(blocking_patterns)

    if door is not None and not isinstance(door, str):
        raise TypeError("door须为字符串或None")
    if role is None and occupied_xuanming_target is not None:
        raise ValueError("给occupied_xuanming_target时必须同时给role")
    if role is None and (
        xuanming_in_wangxiang is not None or upper_lower_generating is not None
    ):
        raise ValueError("玄命旺相/相生条件必须同时给role")

    pending: list[str] = []

    if patterns is None:
        blocking_clear = None
        pending.append("须显式给blocking_patterns（可为空列表）")
    else:
        blocking_clear = len(patterns) == 0

    if door is None:
        auspicious_route = None
        pending.append("须显式给当前直门")
    else:
        auspicious_route = door in AUSPICIOUS_DOORS

    if door_has_malefic_spirit is None:
        clear_route = None
        pending.append("须显式确认门下有无凶恶之神")
    else:
        clear_route = door_has_malefic_spirit is False

    base_checks = {
        "right_taiyi_left_tianmu": right_taiyi_left_tianmu,
        "yinyang_harmonious": yinyang_harmonious,
        "blocking_patterns_clear": blocking_clear,
        "taiyi_not_in_yang_jue": (
            None if taiyi_in_yang_jue is None else not taiyi_in_yang_jue
        ),
        "spirits_independent": spirits_independent,
        "auspicious_route": auspicious_route,
        "route_clear_of_malefic_spirit": clear_route,
        "three_doors_complete": three_doors_complete,
        "five_generals_active": five_generals_active,
    }

    if any(value is None for value in base_checks.values()):
        military_action_favorable = None
    else:
        military_action_favorable = all(base_checks.values())

    xuanming: dict[str, Any] | None = None
    xuanming_harmony: bool | None = None
    if role is not None:
        xuanming = xuanming_for_role(role)
        if occupied_xuanming_target is None:
            pending.append("须显式给当前所临玄命对象")
        if xuanming_in_wangxiang is None:
            pending.append("须显式确认玄命是否临旺相之乡")
        if upper_lower_generating is None:
            pending.append("须显式确认上下是否相生")
        target_match = (
            None
            if occupied_xuanming_target is None
            else occupied_xuanming_target == xuanming["xuanming_target"]
        )
        xuanming["occupied_target"] = occupied_xuanming_target
        xuanming["target_match"] = target_match
        xuanming["in_wangxiang"] = xuanming_in_wangxiang
        xuanming["upper_lower_generating"] = upper_lower_generating
        if None not in (target_match, xuanming_in_wangxiang, upper_lower_generating):
            xuanming_harmony = bool(
                target_match and xuanming_in_wangxiang and upper_lower_generating
            )
    else:
        pending.append("未给role，玄命合不合不判")

    if direct_envoy_clause_matched is None:
        pending.append("‘直使前三五、后二四’结构未自动解释；须显式给匹配证据")

    if None in (
        military_action_favorable,
        xuanming_harmony,
        direct_envoy_clause_matched,
    ):
        greatly_auspicious = None
    else:
        greatly_auspicious = bool(
            military_action_favorable
            and xuanming_harmony
            and direct_envoy_clause_matched
        )

    return {
        "schema_version": "1.0",
        "canonical": C117_VERSION,
        "rule_id": "C117-TAIGONG-TIMING",
        "source_profile": "jinjing_volume1_taigong_timing",
        "base_checks": base_checks,
        "blocking_patterns": patterns,
        "door": door,
        "military_action_favorable": military_action_favorable,
        "xuanming": xuanming,
        "xuanming_harmony": xuanming_harmony,
        "direct_envoy_clause_matched": direct_envoy_clause_matched,
        "greatly_auspicious": greatly_auspicious,
        "pending": pending,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "direct_envoy_boundary": copy.deepcopy(DIRECT_ENVOY_BOUNDARY),
        "policy": (
            "三门具五将发与玄命旺相相生均只消费显式证据；"
            "未校定的直使前三五后二四不得自动公式化。"
        ),
    }


def c117_catalog() -> dict[str, Any]:
    return {
        "canonical": C117_VERSION,
        "rule_id": "C117-TAIGONG-TIMING",
        "auspicious_doors": sorted(AUSPICIOUS_DOORS),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "direct_envoy_boundary": copy.deepcopy(DIRECT_ENVOY_BOUNDARY),
        "auto_rule_lookups": False,
    }


def evaluate_taigong_with_rule_readiness(
    *,
    taiyi_palace: int,
    tianmu: Any,
    shiji_yanji: bool | None,
    wenchang_qiupo: bool | None,
    major_minor_generals_related: bool | None,
    calc_blocked: bool | None,
    right_taiyi_left_tianmu: bool | None,
    yinyang_harmonious: bool | None,
    blocking_patterns: Iterable[str] | None,
    taiyi_in_yang_jue: bool | None,
    spirits_independent: bool | None,
    door: str | None,
    door_has_malefic_spirit: bool | None,
    role: str | None = None,
    occupied_xuanming_target: str | None = None,
    xuanming_in_wangxiang: bool | None = None,
    upper_lower_generating: bool | None = None,
    direct_envoy_clause_matched: bool | None = None,
) -> dict[str, Any]:
    """用现行 source profiles 接入 C117 的“三门具 / 五将发”。

    这是 cross-source integration，不回写成《金镜》卷一逐字公式：
    - 三门正面条件：采用《统宗》卷二“开门加太乙、视天目”的独立 profile；
    - 五将本体阻断：采用《金镜》卷四 J4M-02；
    - 杜塞覆盖：采用项目 CORE-WUJIANG-READY 整合层。

    其余 C117 条件仍须显式输入。
    """
    from .jinjing_v4_military import (
        effective_five_generals_readiness,
        wujiang_fabu,
    )
    from .tongzong_v2_doors import taiyi_door_readiness

    sanmen_source = taiyi_door_readiness(
        taiyi_palace,
        tianmu=tianmu,
    )
    sanmen = {
        **sanmen_source,
        "three_doors_ready": sanmen_source.get("door_ready"),
    }
    source_wujiang = wujiang_fabu(
        shiji_yanji=shiji_yanji,
        wenchang_qiupo=wenchang_qiupo,
        major_minor_generals_related=major_minor_generals_related,
        three_doors_ready=sanmen["three_doors_ready"],
    )
    effective_wujiang = effective_five_generals_readiness(
        source_five_generals_released=source_wujiang.get("five_generals_released"),
        calc_blocked=calc_blocked,
    )

    evaluated = evaluate_taigong_timing(
        right_taiyi_left_tianmu=right_taiyi_left_tianmu,
        yinyang_harmonious=yinyang_harmonious,
        blocking_patterns=blocking_patterns,
        taiyi_in_yang_jue=taiyi_in_yang_jue,
        spirits_independent=spirits_independent,
        door=door,
        door_has_malefic_spirit=door_has_malefic_spirit,
        three_doors_complete=sanmen["three_doors_ready"],
        five_generals_active=effective_wujiang[
            "effective_five_generals_released"
        ],
        role=role,
        occupied_xuanming_target=occupied_xuanming_target,
        xuanming_in_wangxiang=xuanming_in_wangxiang,
        upper_lower_generating=upper_lower_generating,
        direct_envoy_clause_matched=direct_envoy_clause_matched,
    )
    evaluated["readiness_integration"] = {
        "profile": "cross_source_taigong_readiness_v1",
        "three_doors": sanmen,
        "source_five_generals": source_wujiang,
        "effective_five_generals": effective_wujiang,
        "source_boundaries": {
            "three_doors": "太乙统宗宝鉴_卷二_明太乙八门通变术",
            "five_generals": "太乙金镜式经_卷四_J4M-02",
            "calc_blocked": "项目跨层整合事实，不伪装为J4M-02第四原文条件",
            "taigong": "太乙金镜式经_卷一_推太公考时法",
        },
        "policy": (
            "只把已分层核定的ready布尔值送入C117；"
            "不把《统宗》卷二门具文字回填为《金镜》卷一原文。"
        ),
    }
    return evaluated
