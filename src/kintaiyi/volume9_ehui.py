"""C43 《太乙统宗宝鉴》厄会行限的严格来源契约。

原文要求：
- 即位年“干支”参与加大义；
- 取太阳（天罡）、阴主（天魁）所临；
- 以大武、和德为界，按阴阳顺逆累计；
- 还须参详阳九百六、太乙入卦、旺相休囚等。

旧参考函数只用年支并按16位简单步数，不能视为canonical等价实现。
本模块不猜“加大义”的完整盘式变换，只消费已经结构化的落点与计数证据。
"""

from __future__ import annotations

import copy
from typing import Any, Iterable

from .taiyi_rules import integer

C43_VERSION = "taiyi-c43-volume9-ehui-v1"

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "online_witness_volume": 10,
    "project_legacy_volume_label": 9,
    "volume_status": "witness_volume_variant",
    "section": "明阳九百六，太游行限观历术",
}

STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
SEXAGENARY = frozenset(
    f"{stem}{branch}"
    for stem_index, stem in enumerate(STEMS)
    for branch_index, branch in enumerate(BRANCHES)
    if stem_index % 2 == branch_index % 2
)
SIXTEEN_POINTS = tuple("子丑艮寅卯辰巽巳午未坤申酉戌乾亥")

GOD_IDENTITIES = {
    "大义": "天心",
    "太阳": "天罡",
    "阴主": "天魁",
}

DIRECTION_WITNESS = {
    "boundaries": ["大武", "和德"],
    "reverse_half": ["天道", "大威", "大神", "大炅", "太阳", "高丛", "吕申"],
    "forward_half": ["武德", "太簇", "阴主", "阴德", "大义", "地主", "阳德"],
    "status": "direct_text_structure_only",
    "policy": "只保存原文两半神序；未把它简化成固定16步距离公式。",
}

LEGACY_REFERENCE_AUDIT = {
    "function": "guiyun.ehui_xingxian",
    "canonical_equivalent": False,
    "issues": [
        "只以year_zhi为核心输入，不能表达原文即位年干支",
        "把大义固定为亥后做简单16位偏移",
        "把太阳/阴主距离简化成位置步数",
        "未表达大武/和德界与神数累计",
        "未并列阳九百六、入卦、旺相休囚等修正证据",
    ],
}

SOURCE_EXAMPLES = {
    "han_gaozu": {
        "enthronement_ganzhi": "乙未",
        "taiyang_landing": "申",
        "yinzhu_landing": "寅",
        "count_evidence": [
            {"label": "起数", "value": 1},
            {"label": "大威", "value": 2},
            {"label": "大炅", "value": 9},
            {"label": "高丛", "value": 4},
        ],
        "count_total": 16,
        "later_correction_evidence": {
            "year": 12,
            "condition": "太乙入六十七局，丙午与太岁格",
            "effect": "主崩亡",
        },
        "policy": "16年行限计数与第12年另见太乙格证据并存，不用后者反写基础计数。",
    },
}


def parse_ganzhi(value: str) -> dict[str, str]:
    """C43 必须接完整干支；只给地支不够。"""
    if not isinstance(value, str) or len(value) != 2:
        raise ValueError("即位年须为两字干支")
    stem, branch = value
    if stem not in STEMS or branch not in BRANCHES or value not in SEXAGENARY:
        raise ValueError("即位年须为合法六十甲子干支")
    return {"stem": stem, "branch": branch, "ganzhi": value}


def _point(value: str | None, name: str) -> str | None:
    if value is None:
        return None
    if value not in SIXTEEN_POINTS:
        raise ValueError(f"{name}须为十六宫点")
    return value


def _count_components(
    items: Iterable[dict[str, Any]] | None,
) -> tuple[list[dict[str, Any]], int | None]:
    if items is None:
        return [], None
    rows = list(items)
    if not rows:
        return [], None
    normalized = []
    total = 0
    for row in rows:
        if not isinstance(row, dict):
            raise TypeError("count_evidence每项须为dict")
        label = row.get("label")
        value = row.get("value")
        if not isinstance(label, str) or not label:
            raise ValueError("count_evidence.label须为非空字符串")
        value = integer(value, 0)
        normalized.append({"label": label, "value": value})
        total += value
    return normalized, total


def ehui_limit_from_evidence(
    *,
    enthronement_ganzhi: str,
    taiyang_landing: str | None = None,
    yinzhu_landing: str | None = None,
    count_evidence: Iterable[dict[str, Any]] | None = None,
    direction: str | None = None,
    correction_evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """只根据显式来源证据组装厄会行限，不推盘式落点。"""
    gz = parse_ganzhi(enthronement_ganzhi)
    taiyang = _point(taiyang_landing, "taiyang_landing")
    yinzhu = _point(yinzhu_landing, "yinzhu_landing")
    if direction not in (None, "顺", "逆"):
        raise ValueError("direction须为顺/逆或None")
    counts, total = _count_components(count_evidence)

    pending = []
    if taiyang is None:
        pending.append("须提供按原盘式求得的太阳所临")
    if yinzhu is None:
        pending.append("须提供按原盘式求得的阴主所临")
    if direction is None:
        pending.append("须提供依大武/和德界判定的顺逆")
    if total is None:
        pending.append("须提供原文神数累计证据，不以16位步数代替")

    computable = not pending
    return {
        "schema_version": "1.0",
        "canonical": C43_VERSION,
        "rule_id": "C43-V9-EHUI",
        "source_profile": "tongzong_volume9_ehui_limit",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "enthronement": gz,
        "dayi_identity": GOD_IDENTITIES["大义"],
        "taiyang": {
            "identity": GOD_IDENTITIES["太阳"],
            "landing": taiyang,
        },
        "yinzhu": {
            "identity": GOD_IDENTITIES["阴主"],
            "landing": yinzhu,
        },
        "direction": direction,
        "direction_witness": copy.deepcopy(DIRECTION_WITNESS),
        "count_evidence": counts,
        "base_limit_years": total if computable else None,
        "computable": computable,
        "status": "computed_from_explicit_source_evidence" if computable else "not_computable",
        "pending": pending,
        "correction_evidence": copy.deepcopy(correction_evidence or []),
        "corrections_applied": False,
        "legacy_simple_step_formula_used": False,
        "policy": (
            "C43不根据单一地支推太阳/阴主，也不按十六点简单步数算年限；"
            "基础行限与太乙格、阳九百六、旺相休囚等后续证据并列，不互相覆盖。"
        ),
    }


def han_gaozu_example() -> dict[str, Any]:
    """把卷九汉高祖例作为校验见证，不当普遍公式。"""
    example = copy.deepcopy(SOURCE_EXAMPLES["han_gaozu"])
    result = ehui_limit_from_evidence(
        enthronement_ganzhi=example["enthronement_ganzhi"],
        taiyang_landing=example["taiyang_landing"],
        yinzhu_landing=example["yinzhu_landing"],
        count_evidence=example["count_evidence"],
        direction="逆",
        correction_evidence=[example["later_correction_evidence"]],
    )
    result["source_example"] = "han_gaozu"
    return result


def build_volume9_ehui_source_variant(
    result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """构建 source_variants.volume9.ehui_limit。

    只有完整可计算的C43结果才生成 legacy_replacement。
    """
    if result is None:
        result = {}
    if not isinstance(result, dict):
        raise TypeError("result须为dict或None")
    if result:
        if result.get("rule_id") != "C43-V9-EHUI":
            raise ValueError("result必须来自C43-V9-EHUI")
        if result.get("source_profile") != "tongzong_volume9_ehui_limit":
            raise ValueError("C43 source_profile不匹配")

    complete = bool(result and result.get("computable") is True)
    return {
        "schema_version": "1.0",
        "canonical": C43_VERSION,
        "result": copy.deepcopy(result),
        "legacy_replacement": (
            {
                "source_replacement_complete": True,
                "rule_id": "C43-V9-EHUI",
            }
            if complete
            else {}
        ),
        "legacy_reference_audit": copy.deepcopy(LEGACY_REFERENCE_AUDIT),
        "cross_source_merge": False,
        "policy": "旧厄会行限只有被完整C43来源证据替换后才清除migration gap。",
    }
