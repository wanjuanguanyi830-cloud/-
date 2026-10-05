"""C69B 《太乙金镜式经》卷一“推太乙当时法”六壬叠盘层。

C69 已实现天乙朝暮治神与十二天将表；C118 已实现日度宿次与十二分野。
本层把两者按正文“日在何宿，计属何辰，以时加位，立贵前后”接起来：

1. 日宿所属十二分野支 = 六壬月将等价支；
2. 以该支加占时，建立天地盘；
3. 按 C69 日干朝/暮表取得天乙贵人的天盘支；
4. 贵人落地亥子丑寅卯辰则顺布，巳午未申酉戌则逆布；
5. 十二天将相对次序按 C69 自身“前五 / 后六”表展开。

本层不自动决定“朝/暮”，调用方必须显式给 period。
九宫到十二支的投影只作为 derived coordinate adapter；中五不可投影。
"""

from __future__ import annotations

import copy
from typing import Any

from .jinjing_current_time import (
    GENERAL_RULES,
    tianyi_period_ruler,
)
from .jinjing_huangdao_tables import term_day_position
from .taiyi_rules import BRANCHES, integer

C69B_VERSION = "taiyi-c69b-current-time-liuren-overlay-v1"

TWELVE_GENERAL_ORDER = (
    "天乙贵神",
    "螣蛇",
    "朱雀",
    "六合",
    "勾陈",
    "青龙",
    "天空",
    "白虎",
    "太常",
    "玄武",
    "太阴",
    "天后",
)

# 后天八卦正宫投到六壬十二支时，四正直接取本支，
# 四维取该卦顺时针侧的孟支。此为坐标适配，不宣称是《金镜》独立原文公式。
# C69 庚申例直接验证：9->巳、7->申、4->卯、2->午。
NINE_PALACE_TO_LIUREN_BRANCH = {
    1: "亥",
    2: "午",
    3: "寅",
    4: "卯",
    6: "酉",
    7: "申",
    8: "子",
    9: "巳",
}

EXAMPLE_ATTESTED_PROJECTION = {
    9: {"branch": "巳", "observed_general": "青龙"},
    7: {"branch": "申", "observed_general": "太常"},
    4: {"branch": "卯", "observed_general": "六合"},
    2: {
        "branch": "午",
        "observed_general": "天空",
        "source_transcription": "天定",
        "note": "公开转录作“天定”；按六壬式与二宫午位复算落天空，保留原转录异读。",
    },
}

SOURCE_WITNESS = {
    "primary": {
        "work": "太乙金镜式经",
        "volume": 1,
        "section": "推太乙当时法",
        "direct_bridge": [
            "算日在何宿，计属何辰，以时加位，立贵前后，以论将之吉凶",
            "更以日度加时，因步六壬式，知天乙成败之分",
        ],
        "example": (
            "庚申日、寅时、立冬六日心宿：太乙九宫/主大九宫在青龙下，"
            "主参七宫在太常下，客大四宫在六合下，客参二宫公开转录作“天定下”。"
        ),
    },
    "referenced_procedure": {
        "work": "六壬大全",
        "scope": "天盘起贵神、地盘定顺逆、十二天将前后次序",
        "role": "《金镜》正文显式引用“六壬式”后的程序性参校",
    },
    "policy": (
        "六壬程序只用于解释《金镜》明确引用的叠盘步骤；"
        "不把四课三传等未被本条调用的六壬内容并入太乙。"
    ),
}

FORMULA_BOUNDARY = {
    "complete_for_explicit_inputs": True,
    "requires_explicit": [
        "term",
        "day_number",
        "hour_branch",
        "day_stem",
        "period",
    ],
    "not_automatic": [
        "公历日期->节气第几日",
        "时辰->朝/暮判定",
    ],
    "upstream_computability_limits": [
        "C118虚宿整数未定；穿越未定虚宿边界的输入返回not_computable",
    ],
    "coordinate_adapter_boundary": {
        "adapter": "九宫->十二支",
        "lossy": True,
        "strict_alternative": "直接提供entity_branches",
    },
    "c69_complete_current_time_formula": False,
    "c69_complete_false_means": "完整自动单入口尚未统一；不表示C69B显式输入六壬叠盘核心未实现。",
    "reason": (
        "C69B在显式输入且C118日度可算时完整执行六壬叠盘；但公历日期到节气日序、"
        "朝暮自动判定与无损坐标入口仍未统一成单一自动日期排盘入口。"
    ),
}


def _branch(value: str, name: str) -> str:
    if not isinstance(value, str) or value not in BRANCHES:
        raise ValueError(f"{name}须为十二地支")
    return value


def heaven_plate(month_general_branch: str, hour_branch: str) -> dict[str, str]:
    """月将加时：占时地盘支上安月将，顺布十二天盘支。"""
    month_general = _branch(month_general_branch, "month_general_branch")
    hour = _branch(hour_branch, "hour_branch")
    m = BRANCHES.index(month_general)
    h = BRANCHES.index(hour)
    return {
        ground: BRANCHES[(m + (i - h)) % 12]
        for i, ground in enumerate(BRANCHES)
    }


def noble_ground_branch(
    *,
    day_stem: str,
    period: str,
    month_general_branch: str,
    hour_branch: str,
) -> dict[str, Any]:
    ruler = tianyi_period_ruler(day_stem, period)
    plate = heaven_plate(month_general_branch, hour_branch)
    noble_heaven_branch = ruler["branch"]
    ground = next(
        ground for ground, heaven in plate.items()
        if heaven == noble_heaven_branch
    )
    direction = "顺" if ground in ("亥", "子", "丑", "寅", "卯", "辰") else "逆"
    return {
        "schema_version": "1.0",
        "canonical": C69B_VERSION,
        "rule_id": "C69B-NOBLE-GROUND",
        "day_stem": day_stem,
        "period": period,
        "month_general_branch": month_general_branch,
        "hour_branch": hour_branch,
        "tianyi_ruler": ruler["ruler"],
        "noble_heaven_branch": noble_heaven_branch,
        "noble_ground_branch": ground,
        "direction": direction,
        "heaven_plate": plate,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
    }


def twelve_general_plate(
    *,
    day_stem: str,
    period: str,
    month_general_branch: str,
    hour_branch: str,
) -> dict[str, Any]:
    noble = noble_ground_branch(
        day_stem=day_stem,
        period=period,
        month_general_branch=month_general_branch,
        hour_branch=hour_branch,
    )
    start = BRANCHES.index(noble["noble_ground_branch"])
    step = 1 if noble["direction"] == "顺" else -1

    general_by_ground: dict[str, str] = {}
    ground_by_general: dict[str, str] = {}
    for offset, general in enumerate(TWELVE_GENERAL_ORDER):
        ground = BRANCHES[(start + step * offset) % 12]
        general_by_ground[ground] = general
        ground_by_general[general] = ground

    return {
        "schema_version": "1.0",
        "canonical": C69B_VERSION,
        "rule_id": "C69B-TWELVE-GENERAL-PLATE",
        "day_stem": day_stem,
        "period": period,
        "month_general_branch": month_general_branch,
        "hour_branch": hour_branch,
        "noble_ground_branch": noble["noble_ground_branch"],
        "direction": noble["direction"],
        "heaven_plate": noble["heaven_plate"],
        "general_by_ground": general_by_ground,
        "ground_by_general": ground_by_general,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
    }


def palace_to_liuren_branch(palace: int) -> dict[str, Any]:
    palace = integer(palace, 1, 9)
    if palace == 5:
        return {
            "schema_version": "1.0",
            "canonical": C69B_VERSION,
            "rule_id": "C69B-PALACE-BRANCH-PROJECTION",
            "computable": False,
            "palace": 5,
            "branch": None,
            "status": "center_unprojectable",
            "reason": "中五无六壬十二支正位投影",
        }
    branch = NINE_PALACE_TO_LIUREN_BRANCH[palace]
    attested = EXAMPLE_ATTESTED_PROJECTION.get(palace)
    return {
        "schema_version": "1.0",
        "canonical": C69B_VERSION,
        "rule_id": "C69B-PALACE-BRANCH-PROJECTION",
        "computable": True,
        "palace": palace,
        "branch": branch,
        "status": (
            "jinjing_example_attested"
            if attested is not None
            else "derived_bagua_branch_projection"
        ),
        "example_attestation": copy.deepcopy(attested),
        "projection_lossy": True,
        "policy": "该投影只用于十二支六壬叠盘，不替换太乙十六宫精确坐标。",
    }


def general_under_branch(
    branch: str,
    *,
    general_plate: dict[str, Any],
) -> dict[str, Any]:
    b = _branch(branch, "branch")
    general = general_plate["general_by_ground"][b]
    rule = GENERAL_RULES[general]
    return {
        "branch": b,
        "general": general,
        "verdict": rule["verdict"],
        "matters": copy.deepcopy(rule["matters"]),
        "source_status": rule["source_status"],
    }


def general_under_palace(
    palace: int,
    *,
    general_plate: dict[str, Any],
) -> dict[str, Any]:
    projection = palace_to_liuren_branch(palace)
    if not projection["computable"]:
        return {
            "palace": palace,
            "computable": False,
            "general": None,
            "verdict": None,
            "projection": projection,
        }
    under = general_under_branch(
        projection["branch"],
        general_plate=general_plate,
    )
    return {
        "palace": palace,
        "computable": True,
        **under,
        "projection": projection,
    }


def current_time_liuren_overlay(
    *,
    term: str,
    day_number: int,
    hour_branch: str,
    day_stem: str,
    period: str,
    entity_palaces: dict[str, int] | None = None,
    entity_branches: dict[str, str] | None = None,
) -> dict[str, Any]:
    """从C118日度上游建立C69六壬式十二天将叠盘。

    entity_palaces 使用derived九宫->地支投影；
    更严格的调用方可直接提供 entity_branches。
    """
    day_position = term_day_position(term, day_number)
    if not day_position.get("computable"):
        return {
            "schema_version": "1.0",
            "canonical": C69B_VERSION,
            "rule_id": "C69B-CURRENT-TIME-LIUREN",
            "computable": False,
            "status": "huangdao_upstream_not_computable",
            "day_position": day_position,
            "pending": copy.deepcopy(day_position.get("pending", [])),
        }

    month_general_branch = day_position["division"]["branch"]
    plate = twelve_general_plate(
        day_stem=day_stem,
        period=period,
        month_general_branch=month_general_branch,
        hour_branch=hour_branch,
    )

    entities: dict[str, Any] = {}
    if entity_palaces is not None:
        if not isinstance(entity_palaces, dict):
            raise TypeError("entity_palaces须为dict或None")
        for name, palace in entity_palaces.items():
            if not isinstance(name, str):
                raise TypeError("entity_palaces键须为字符串")
            entities[name] = general_under_palace(
                palace,
                general_plate=plate,
            )

    if entity_branches is not None:
        if not isinstance(entity_branches, dict):
            raise TypeError("entity_branches须为dict或None")
        for name, branch in entity_branches.items():
            if not isinstance(name, str):
                raise TypeError("entity_branches键须为字符串")
            entities[name] = {
                "computable": True,
                **general_under_branch(branch, general_plate=plate),
                "projection": None,
            }

    return {
        "schema_version": "1.0",
        "canonical": C69B_VERSION,
        "rule_id": "C69B-CURRENT-TIME-LIUREN",
        "computable": True,
        "status": "explicit_liuren_overlay",
        "term": term,
        "day_number": day_number,
        "day_position": day_position,
        "month_general_branch": month_general_branch,
        "hour_branch": hour_branch,
        "day_stem": day_stem,
        "period": period,
        "general_plate": plate,
        "entities": entities,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "formula_boundary": copy.deepcopy(FORMULA_BOUNDARY),
    }


def c69b_catalog() -> dict[str, Any]:
    return {
        "canonical": C69B_VERSION,
        "rule_ids": [
            "C69B-NOBLE-GROUND",
            "C69B-TWELVE-GENERAL-PLATE",
            "C69B-PALACE-BRANCH-PROJECTION",
            "C69B-CURRENT-TIME-LIUREN",
        ],
        "twelve_general_order": list(TWELVE_GENERAL_ORDER),
        "nine_palace_to_liuren_branch": copy.deepcopy(NINE_PALACE_TO_LIUREN_BRANCH),
        "example_attested_projection": copy.deepcopy(EXAMPLE_ATTESTED_PROJECTION),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "formula_boundary": copy.deepcopy(FORMULA_BOUNDARY),
    }
