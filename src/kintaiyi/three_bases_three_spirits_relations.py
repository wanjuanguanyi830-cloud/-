"""C83 三基与天乙 / 地乙 / 直符同宫显式关系层。

来源：《太乙统宗宝鉴》卷六 / 卷七见证。

本层只处理九个 pair：
- 君基 × 天乙 / 地乙 / 直符；
- 臣基 × 天乙 / 地乙 / 直符；
- 民基 × 天乙 / 地乙 / 直符。

边界：
- 不读取 C66 / C64 自动比较位置；
- same_palace 必须显式输入；
- 君基三条原文均含“行为条件 -> 吉/凶”双支，不能压成无条件单一断语；
- 臣基、民基六条按直接灾应保存；
- 四神 / 大游 / 小游不在 C82。
"""

from __future__ import annotations

import copy
from typing import Any

C83_VERSION = "taiyi-c83-three-bases-three-spirits-relations-v1"

BASES = ("君基", "臣基", "民基")
SPIRITS = ("天乙", "地乙", "直符")

LEGACY_SPIRIT_ALIASES = {
    "值符": "直符",
}

RULES: dict[tuple[str, str], dict[str, Any]] = {
    ("君基", "天乙"): {
        "source_section": "明君基太乙所主术",
        "structure": "conditional_governance",
        "favorable": {
            "conduct": ["出符文", "降诏命", "练甲胄", "誓军旅", "征不道", "伐不义"],
            "effects": ["君国致祯祥"],
        },
        "adverse": {
            "conduct": ["好攻战", "轻百姓", "饰城郭", "侵边境"],
            "effects": ["不祥变异", "妖怪", "兵火之咎"],
        },
        "source_status": "direct_conditional",
    },
    ("君基", "地乙"): {
        "source_section": "明君基太乙所主术",
        "structure": "conditional_governance",
        "favorable": {
            "conduct": ["卑宫室", "去奢侈", "息土工", "安百姓", "务农桑", "劝稼穑"],
            "effects": ["德永昌", "地生祥瑞", "天下丰和", "景命惟新"],
        },
        "adverse": {
            "conduct": ["奢淫骄慢", "广营宫室", "缀饰珠玉", "妆丽过甚"],
            "effects": ["兵火丧亡", "五谷荒俭", "民生灾疾", "地生异类妖物"],
        },
        "source_status": "direct_conditional",
    },
    ("君基", "直符"): {
        "source_section": "明君基太乙所主术",
        "structure": "conditional_governance",
        "favorable": {
            "conduct": ["贤佞分别", "宫人有序", "率由旧章", "敬重功勋", "殊别嫡庶"],
            "effects": ["君国升平", "嘉祥"],
        },
        "adverse": {
            "conduct": ["谗邪胜正", "广营宫室", "吏为苛酷", "百姓愁怨"],
            "effects": ["大旱灾伤", "火烧宫庙", "民多饥馑", "疾疫大作", "不利君王"],
        },
        "source_status": "direct_conditional_stable_core",
        "text_boundary": "删去电子转录中不稳的个别治理措辞，只保留两见证可稳定辨识的条件核心。",
    },
    ("臣基", "天乙"): {
        "source_section": "明臣基太乙所主术",
        "structure": "direct_omen",
        "effects": ["横逆不义侵于臣佐", "盗贼"],
        "source_status": "direct",
    },
    ("臣基", "地乙"): {
        "source_section": "明臣基太乙所主术",
        "structure": "direct_omen",
        "effects": ["多土工", "百姓失务"],
        "source_status": "direct",
    },
    ("臣基", "直符"): {
        "source_section": "明臣基太乙所主术",
        "structure": "direct_omen",
        "effects": ["理法不平", "民无所措", "火灾"],
        "source_status": "direct",
    },
    ("民基", "天乙"): {
        "source_section": "明民基太乙所主术",
        "structure": "direct_omen",
        "effects": ["兵盗", "饥荒", "霜雪杀物", "人民不安"],
        "source_status": "direct",
    },
    ("民基", "地乙"): {
        "source_section": "明民基太乙所主术",
        "structure": "direct_omen",
        "effects": ["土工役民", "虫伤稼穑", "禾谷不收", "多生疾患"],
        "source_status": "direct_stable_core",
        "text_boundary": "NGJ/CADAL 个别字有 OCR 差异，按两见证稳定语义核心正规化。",
    },
    ("民基", "直符"): {
        "source_section": "明民基太乙所主术",
        "structure": "direct_omen",
        "effects": ["大旱灾伤", "飞蝗为害", "兵盗亦兴"],
        "source_status": "direct_stable_core",
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
        "卷六/卷七编次差异不复制算法；君基条件句按正反治理分支保存，"
        "臣基/民基直接灾应保存稳定核心，OCR不稳字不扩写。"
    ),
}

POSITION_BOUNDARY = {
    "three_bases_position_runtime": "C66",
    "three_spirits_position_runtime": "C64",
    "auto_position_lookup_used": False,
    "auto_same_palace_inference_used": False,
    "policy": "C83只消费显式关系证据，不调用C66/C64自动生成同宫。",
}

CONDUCT_VALUES = frozenset(("favorable_source_conduct", "adverse_source_conduct"))


def _base(name: str) -> str:
    if name not in BASES:
        raise ValueError("base须为君基/臣基/民基")
    return name


def _spirit(name: str, *, allow_legacy_zhifu_alias: bool) -> str:
    if name in SPIRITS:
        return name
    if name == "值符":
        if allow_legacy_zhifu_alias:
            return LEGACY_SPIRIT_ALIASES[name]
        raise ValueError("值符不是C83 canonical名称；兼容时显式开启alias")
    raise ValueError("spirit须为天乙/地乙/直符")


def three_base_spirit_relation(
    base: str,
    spirit: str,
    *,
    same_palace: bool | None,
    conduct_branch: str | None = None,
    allow_legacy_zhifu_alias: bool = False,
) -> dict[str, Any]:
    """解释三基与三神显式同宫关系。"""
    base = _base(base)
    spirit = _spirit(
        spirit,
        allow_legacy_zhifu_alias=allow_legacy_zhifu_alias,
    )
    rule = RULES[(base, spirit)]

    if same_palace not in (None, True, False):
        raise TypeError("same_palace须为bool或None")
    if conduct_branch is not None and conduct_branch not in CONDUCT_VALUES:
        raise ValueError(
            "conduct_branch须为favorable_source_conduct/"
            "adverse_source_conduct或None"
        )
    if base != "君基" and conduct_branch is not None:
        raise ValueError("conduct_branch仅用于君基条件式同宫条文")
    if same_palace is not True and conduct_branch is not None:
        raise ValueError("未显式确认同宫时不能选择conduct_branch")

    pending: list[str] = []
    selected_effects: list[str] = []
    branches = None

    if same_palace is None:
        status = "same_palace_unchecked"
        pending.append("须显式确认是否同宫；C83不从C66/C64自动判断")
    elif same_palace is False:
        status = "not_same_palace"
    elif rule["structure"] == "direct_omen":
        status = "explicit_same_palace_direct_omen"
        selected_effects = copy.deepcopy(rule["effects"])
    else:
        status = "explicit_same_palace_conditional"
        branches = {
            "favorable_source_conduct": copy.deepcopy(rule["favorable"]),
            "adverse_source_conduct": copy.deepcopy(rule["adverse"]),
        }
        if conduct_branch is None:
            pending.append("君基同宫条文含正反治理条件，须显式选择conduct_branch才取一支断语")
        else:
            selected_effects = copy.deepcopy(branches[conduct_branch]["effects"])

    return {
        "schema_version": "1.0",
        "canonical": C83_VERSION,
        "rule_id": "C83-THREE-BASES-THREE-SPIRITS",
        "source_profile": "tongzong_three_bases_three_spirits_relations",
        "base": base,
        "spirit": spirit,
        "same_palace": same_palace,
        "structure": rule["structure"],
        "conduct_branch": conduct_branch,
        "conditional_branches": branches,
        "selected_effects": selected_effects,
        "status": status,
        "pending": pending,
        "source_section": rule["source_section"],
        "source_status": rule["source_status"],
        "text_boundary": rule.get("text_boundary"),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
        "policy": (
            "只有显式same_palace=True才解释关系；君基三条保留原文条件分支，"
            "未选择治理分支时不压成单一吉凶。"
        ),
    }


def c82_catalog() -> dict[str, Any]:
    return {
        "canonical": C83_VERSION,
        "rule_id": "C83-THREE-BASES-THREE-SPIRITS",
        "source_profile": "tongzong_three_bases_three_spirits_relations",
        "bases": list(BASES),
        "spirits": list(SPIRITS),
        "pair_count": len(RULES),
        "rules": copy.deepcopy(RULES),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
    }
