"""C91 三基与四神 / 大游 / 小游同宫显式关系层。

来源：《太乙统宗宝鉴》卷六 / 卷七见证。

本层覆盖九个 pair：
- 君基 × 四神 / 大游 / 小游；
- 臣基 × 四神 / 大游 / 小游；
- 民基 × 四神 / 大游 / 小游。

边界：
- 不读取 C66 或大小游/四神位置自动比较；
- same_palace 必须显式输入；
- 君基+四神、君基+大游保留治理/应对条件；
- 君基+小游保存“争之象”及原文应对，不压成现代评分；
- 臣基/民基六条按直接灾应保存。
"""

from __future__ import annotations

import copy
from typing import Any

C91_VERSION = "taiyi-c91-three-bases-other-spirits-relations-v1"

BASES = ("君基", "臣基", "民基")
COUNTERPARTS = ("四神", "大游", "小游")

ALIASES = {
    "四神水宿": "四神",
    "太游": "大游",
    "太遊": "大游",
    "大遊": "大游",
    "小遊": "小游",
}

RULES: dict[tuple[str, str], dict[str, Any]] = {
    ("君基", "四神"): {
        "source_section": "明君基太乙所主术",
        "structure": "conditional_governance",
        "favorable": {
            "conduct": [
                "敬奉宗庙",
                "郊祀天地",
                "祷祭神祗",
                "严肃斋戒",
                "奉天时",
                "明刑罚",
            ],
            "effects": ["阴阳调", "邦国道泰"],
        },
        "adverse": {
            "conduct": ["简宗庙", "不祷祠", "废祀祭", "逆天时"],
            "effects": ["水暴百川", "人民流溺", "淫雨为灾", "伤稼穑", "饥馑疾疫"],
        },
        "source_status": "direct_conditional_stable_core",
    },
    ("君基", "大游"): {
        "source_section": "明君基太乙所主术",
        "structure": "conditional_response",
        "base_omens": ["兵革", "水旱", "疾疫之祸"],
        "favorable": {
            "conduct": [
                "修明德",
                "布号令",
                "命将帅",
                "整戈甲",
                "进文儒",
                "行化",
                "施恩宥",
                "察狱讼",
                "省赋敛",
                "恤军民",
            ],
            "effects": [],
        },
        "adverse": {
            "conduct": ["妄兴兵甲", "窃弄干戈", "不恤生灵", "百姓愁怨"],
            "effects": ["国耗民竭", "危亡之祸", "兵灾民困"],
        },
        "source_status": "direct_conditional_response",
        "text_boundary": "正向段以应对/修政为主，不强造一个原文未明写的“必吉”结果。",
    },
    ("君基", "小游"): {
        "source_section": "明君基太乙所主术",
        "structure": "direct_omen_with_response",
        "effects": ["二君同宫", "阴掩阳", "月掩日之象", "争之象", "祸乱不可胜言"],
        "prescribed_response": [
            "宣发诏令",
            "布恩泽",
            "明刑罚",
            "修武备",
            "禁奸",
            "彰威耀武",
            "君主亲征",
        ],
        "source_status": "direct_omen_with_prescribed_response",
    },
    ("臣基", "四神"): {
        "source_section": "明臣基太乙所主术",
        "structure": "direct_omen",
        "effects": ["重赋繁役", "夺民财", "水涝"],
        "source_status": "direct",
    },
    ("臣基", "大游"): {
        "source_section": "明臣基太乙所主术",
        "structure": "direct_omen",
        "effects": ["政讼不平", "农失其务", "水旱", "兵刀", "饥馑", "疾疫"],
        "source_status": "direct",
    },
    ("臣基", "小游"): {
        "source_section": "明臣基太乙所主术",
        "structure": "direct_omen",
        "effects": ["下凌于上", "君囚其臣", "宰辅不利", "诸侯自谋", "上下不协"],
        "source_status": "direct",
    },
    ("民基", "四神"): {
        "source_section": "明民基太乙所主术",
        "structure": "direct_omen",
        "effects": ["水涝", "饥荒", "民多流荡"],
        "source_status": "direct_stable_core",
    },
    ("民基", "大游"): {
        "source_section": "明民基太乙所主术",
        "structure": "direct_omen",
        "effects": ["兵火", "水旱", "人民流移"],
        "source_status": "direct",
    },
    ("民基", "小游"): {
        "source_section": "明民基太乙所主术",
        "structure": "direct_omen",
        "effects": ["稼穑丰收", "兴兵役之事"],
        "source_status": "direct_stable_core_two_witnesses",
        "text_boundary": "NGJ 单一转录字形混乱；CADAL/另一直接见证稳定支持“稼穑丰收，及兴兵役之事”核心。",
    },
}

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "witness_volumes": [6, 7],
    "volume_status": "witness_volume_variant",
    "direct_sections": [
        "明君基太乙所主术",
        "明臣基太乙所主术",
        "明民基太乙所主术",
    ],
    "policy": (
        "君基条的修政/失德条件与直接灾象分栏；"
        "臣基/民基直接灾应只取多见证稳定核心。"
    ),
}

POSITION_BOUNDARY = {
    "three_bases_position_runtime": "C66",
    "counterpart_position_runtimes": {
        "四神": "separate_existing_or_future_position_source",
        "大游": "C38/C41 source layers; relation layer does not invoke them",
        "小游": "C47 source layer; relation layer does not invoke it",
    },
    "auto_position_lookup_used": False,
    "auto_same_palace_inference_used": False,
    "policy": "C91不从任何位置runtime自动制造同宫证据。",
}

CONDUCT_VALUES = frozenset(("favorable_source_conduct", "adverse_source_conduct"))


def _base(name: str) -> str:
    if name not in BASES:
        raise ValueError("base须为君基/臣基/民基")
    return name


def _counterpart(name: str) -> str:
    if not isinstance(name, str):
        raise TypeError("counterpart须为字符串")
    normalized = ALIASES.get(name, name)
    if normalized not in COUNTERPARTS:
        raise ValueError("counterpart须为四神/大游/小游")
    return normalized


def three_base_other_relation(
    base: str,
    counterpart: str,
    *,
    same_palace: bool | None,
    conduct_branch: str | None = None,
) -> dict[str, Any]:
    """解释三基与四神/大小游的显式同宫关系。"""
    base = _base(base)
    counterpart = _counterpart(counterpart)
    rule = RULES[(base, counterpart)]

    if same_palace not in (None, True, False):
        raise TypeError("same_palace须为bool或None")
    if conduct_branch is not None and conduct_branch not in CONDUCT_VALUES:
        raise ValueError(
            "conduct_branch须为favorable_source_conduct/"
            "adverse_source_conduct或None"
        )

    supports_conduct = rule["structure"] in {
        "conditional_governance",
        "conditional_response",
    }
    if not supports_conduct and conduct_branch is not None:
        raise ValueError("该pair没有C91可选conduct_branch")
    if same_palace is not True and conduct_branch is not None:
        raise ValueError("未显式确认同宫时不能选择conduct_branch")

    pending: list[str] = []
    selected_effects: list[str] = []
    conditional_branches = None
    base_omens = copy.deepcopy(rule.get("base_omens", []))
    prescribed_response = copy.deepcopy(rule.get("prescribed_response", []))

    if same_palace is None:
        status = "same_palace_unchecked"
        pending.append("须显式确认是否同宫；C91不从位置runtime自动判断")
    elif same_palace is False:
        status = "not_same_palace"
    elif rule["structure"] == "direct_omen":
        status = "explicit_same_palace_direct_omen"
        selected_effects = copy.deepcopy(rule["effects"])
    elif rule["structure"] == "direct_omen_with_response":
        status = "explicit_same_palace_direct_omen_with_response"
        selected_effects = copy.deepcopy(rule["effects"])
    else:
        status = "explicit_same_palace_conditional"
        conditional_branches = {
            "favorable_source_conduct": copy.deepcopy(rule["favorable"]),
            "adverse_source_conduct": copy.deepcopy(rule["adverse"]),
        }
        if conduct_branch is None:
            pending.append("本条含原文行为条件；须显式选择conduct_branch才取条件分支结果")
        else:
            selected_effects = copy.deepcopy(
                conditional_branches[conduct_branch]["effects"]
            )

    return {
        "schema_version": "1.0",
        "canonical": C91_VERSION,
        "rule_id": "C91-THREE-BASES-OTHER-SPIRITS",
        "source_profile": "tongzong_three_bases_other_relations",
        "base": base,
        "counterpart": counterpart,
        "same_palace": same_palace,
        "structure": rule["structure"],
        "conduct_branch": conduct_branch,
        "base_omens": base_omens,
        "conditional_branches": conditional_branches,
        "selected_effects": selected_effects,
        "prescribed_response": prescribed_response,
        "status": status,
        "pending": pending,
        "source_section": rule["source_section"],
        "source_status": rule["source_status"],
        "text_boundary": rule.get("text_boundary"),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
        "policy": (
            "C91仅解释显式同宫证据；君基条件与应对按原文结构保留，"
            "不把劝戒文字改写成现代风险评分。"
        ),
    }


def c91_catalog() -> dict[str, Any]:
    return {
        "canonical": C91_VERSION,
        "rule_id": "C91-THREE-BASES-OTHER-SPIRITS",
        "source_profile": "tongzong_three_bases_other_relations",
        "bases": list(BASES),
        "counterparts": list(COUNTERPARTS),
        "pair_count": len(RULES),
        "rules": copy.deepcopy(RULES),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
    }
