"""C112 五福 / 四神 / 大游 / 小游遗留同宫关系恢复层。

本模块只恢复 2026-10-04 旧分支已经实现、但此前未正式迁入 main 的四组关系：
- 五福 × 大游
- 五福 × 小游
- 四神 × 小游
- 大游 × 小游

2026-10-05 重新按《太乙统宗宝鉴》卷七直接见证核定。

边界：
- 不读取 C67/C92/C103/C107 的位置 runtime 自动判断同宫；
- same_palace 必须由调用方显式给出；
- 五福 × 大游保留“五福条”和“大游条”两层文字，不揉成单一伪原文；
- 五福 × 小游必须显式给 virtue 才选择“有德/失德”分支；
- “兵革之灾降于对冲之分”只保存原文关系，不自动计算具体对冲分野。
"""

from __future__ import annotations

import copy
from typing import Any

C112_VERSION = "taiyi-c112-recovered-wander-conjunctions-v1"

ENTITY_ORDER = ("五福", "四神", "大游", "小游")
ALIASES = {
    "太游": "大游",
    "太遊": "大游",
    "大遊": "大游",
    "小遊": "小游",
    "四神水宿": "四神",
}

PAIR_RULES: dict[tuple[str, str], dict[str, Any]] = {
    ("五福", "大游"): {
        "structure": "layered_direct",
        "layers": [
            {
                "source_section": "明五福太乙所主术",
                "effects": ["五福之福减半", "兵盗", "水旱不免"],
                "status": "direct_stable_core",
            },
            {
                "source_section": "明大游太乙所主术",
                "effects": ["兵革之灾降于对冲之分"],
                "status": "direct_stable_core",
            },
        ],
        "localization_boundary": (
            "原文只说明灾降对冲之分；C112不调用坐标 runtime 自动求具体对冲分野。"
        ),
    },
    ("五福", "小游"): {
        "structure": "virtue_branch",
        "source_section": "明五福太乙所主术",
        "branches": {
            True: ["有德者昌"],
            False: ["失德者殃"],
        },
        "status": "direct_stable_core",
    },
    ("四神", "小游"): {
        "structure": "direct_omen",
        "source_section": "明四神太乙水宿所主术",
        "effects": ["人民不安", "多生水涝疾疫"],
        "status": "direct_stable_core",
    },
    ("大游", "小游"): {
        "structure": "direct_omen",
        "source_section": "明大游太乙所主术",
        "effects": ["兵丧", "水旱", "凶暴大作"],
        "status": "direct_stable_core_two_witnesses",
        "text_boundary": (
            "NGJ电子转录一处作“这暴”，CADAL见证明确作“凶暴”；"
            "执行层采用两见证可稳定校定的“凶暴大作”。"
        ),
    },
}

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "volume": 7,
    "primary_witnesses": [
        {
            "id": "NGJ892411999009267118912",
            "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny528zm2srn",
        },
        {
            "id": "CADAL02094393",
            "url": "https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppwvvwt996",
        },
    ],
    "sections": [
        "明五福太乙所主术",
        "明四神太乙水宿所主术",
        "明大游太乙所主术",
    ],
    "policy": (
        "关系层只保存直接见证；电子转录异字按两见证稳定核心正规化，"
        "不得借旧代码补造未见断语。"
    ),
}

RECOVERY_PROVENANCE = {
    "time_window_policy": "only_2026-10-04_and_2026-10-05_prior_work",
    "old_work": [
        {
            "branch": "codex/c1-c7-canonical",
            "file": "src/kintaiyi/taiyi_cycles.py",
            "symbols": [
                "five_blessings_wander_effect",
                "five_blessings_base_meeting",
            ],
        },
        {
            "branch": "codex/taiyi-rules-v2-20261005",
            "file": "src/kintaiyi/cycles.py",
            "symbols": [
                "xiaoyou_suozhu",
                "wufu_interaction",
                "XIAOYOU_EFFECTS",
            ],
        },
    ],
    "recovery_policy": (
        "旧实现仅作为完成工作线索；C112按直接来源重核后重新建模，"
        "不复制旧 project canonical 或旧自动坐标判断。"
    ),
}

POSITION_BOUNDARY = {
    "wufu_position_runtime": "C67",
    "four_spirit_position_runtime": "C92",
    "xiaoyou_position_runtime": "C103",
    "dayou_position_runtime": "C107",
    "auto_position_lookup_used": False,
    "auto_same_palace_inference_used": False,
    "auto_opposite_division_lookup_used": False,
    "policy": "C112只消费显式关系证据，不调用位置层自动制造同宫或对冲分野。",
}


def _entity(name: str) -> str:
    if not isinstance(name, str):
        raise TypeError("对象名须为字符串")
    normalized = ALIASES.get(name, name)
    if normalized not in ENTITY_ORDER:
        raise ValueError("对象须为五福/四神/大游/小游")
    return normalized


def _pair_key(first: str, second: str) -> tuple[str, str]:
    if first == second:
        raise ValueError("同宫pair须为两个不同对象")
    a = ENTITY_ORDER.index(first)
    b = ENTITY_ORDER.index(second)
    return (first, second) if a < b else (second, first)


def wander_conjunction_relation(
    first: str,
    second: str,
    *,
    same_palace: bool | None,
    virtue: bool | None = None,
) -> dict[str, Any]:
    """解释四组已重核的遗留同宫关系。"""
    a = _entity(first)
    b = _entity(second)
    key = _pair_key(a, b)
    rule = PAIR_RULES.get(key)
    if rule is None:
        raise ValueError("该pair不属于C112；请使用对应现行关系模块")

    if same_palace not in (None, True, False):
        raise TypeError("same_palace须为bool或None")
    if virtue not in (None, True, False):
        raise TypeError("virtue须为bool或None")
    if rule["structure"] != "virtue_branch" and virtue is not None:
        raise ValueError("virtue仅用于五福×小游")
    if same_palace is not True and virtue is not None:
        raise ValueError("未显式确认同宫时不能选择virtue分支")

    effect_layers: list[dict[str, Any]] = []
    selected_effects: list[str] = []
    pending: list[str] = []

    if same_palace is None:
        status = "same_palace_unchecked"
        pending.append("须显式确认是否同宫；C112不从位置runtime自动判断")
    elif same_palace is False:
        status = "not_same_palace"
    elif rule["structure"] == "layered_direct":
        status = "explicit_same_palace_layered_direct"
        effect_layers = copy.deepcopy(rule["layers"])
    elif rule["structure"] == "virtue_branch":
        if virtue is None:
            status = "explicit_same_palace_pending_virtue"
            pending.append("五福×小游须显式给virtue=True/False才能选择有德/失德分支")
        else:
            status = "explicit_same_palace_virtue_branch"
            selected_effects = copy.deepcopy(rule["branches"][virtue])
    else:
        status = "explicit_same_palace_direct_omen"
        effect_layers = [{
            "source_section": rule["source_section"],
            "effects": copy.deepcopy(rule["effects"]),
            "status": rule["status"],
        }]
        selected_effects = copy.deepcopy(rule["effects"])

    return {
        "schema_version": "1.0",
        "canonical": C112_VERSION,
        "rule_id": "C112-RECOVERED-WANDER-CONJUNCTIONS",
        "source_profile": "tongzong_volume7_wander_conjunctions",
        "first": a,
        "second": b,
        "pair": list(key),
        "same_palace": same_palace,
        "structure": rule["structure"],
        "virtue": virtue,
        "effect_layers": effect_layers,
        "selected_effects": selected_effects,
        "pending": pending,
        "status": status,
        "source_rule_status": rule.get("status"),
        "localization_boundary": rule.get("localization_boundary"),
        "text_boundary": rule.get("text_boundary"),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "recovery_provenance": copy.deepcopy(RECOVERY_PROVENANCE),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
        "policy": (
            "只在显式same_palace=True时解释关系；五福×大游保持双来源层，"
            "五福×小游必须显式选择德行分支，任何具体位置/对冲分野均不自动推断。"
        ),
    }


def c112_catalog() -> dict[str, Any]:
    return {
        "canonical": C112_VERSION,
        "rule_id": "C112-RECOVERED-WANDER-CONJUNCTIONS",
        "source_profile": "tongzong_volume7_wander_conjunctions",
        "pair_count": len(PAIR_RULES),
        "pair_rules": copy.deepcopy(PAIR_RULES),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "recovery_provenance": copy.deepcopy(RECOVERY_PROVENANCE),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
    }
