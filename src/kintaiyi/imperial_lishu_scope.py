"""C50 《太乙统宗宝鉴》“明太乙历数之期术”来源范围契约。

本条是帝王始终历数的证据编排层：
- 基础厄会：即位年支加大义，视太阳/阴主及合神“四神”；
- 再参太乙运气、太游/小游卦爻、内外极限、囚迫击格掩挟；
- 即位旁云气另属后续独立观察层。

C50不发明独立总年限公式，也不复制C42帝祚历数算术。
"""

from __future__ import annotations

import copy
from typing import Any

C50_VERSION = "taiyi-c50-imperial-lishu-scope-v1"

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "volume": 10,
    "section": "明太乙历数之期术",
    "collation": [
        {
            "work": "太白兵备统宗宝鉴",
            "section": "释大游太乙观历数",
            "role": "important_collation",
        }
    ],
}

SCOPE = {
    "subject": "帝王应天顺人始终之期",
    "independent_total_year_formula_attested": False,
    "base_ehui_method": {
        "accession_year_branch_plus": "大义",
        "primary_targets": ["太阳", "阴主"],
        "hegod_extension": True,
        "four_period_structure": "太阳及其合神、阴主及其合神",
        "implemented_runtime_dependency": "C43-V9-EHUI",
        "dependency_status": (
            "C43已结构化大义/太阳/阴主与显式行限证据；"
            "合神四神扩展在C50只登记source scope，不重算落点。"
        ),
    },
    "correction_layers": [
        {
            "layer": "太游阳九百六行限",
            "dependency": "C38",
            "role": "correction_evidence",
        },
        {
            "layer": "小游轨运卦爻",
            "dependency": "C47",
            "role": "correction_evidence",
        },
        {
            "layer": "小游行爻灾祥",
            "dependency": "C48",
            "role": "correction_evidence",
        },
        {
            "layer": "囚迫击格掩挟等格局",
            "dependency": "pattern_evidence",
            "role": "correction_evidence",
        },
    ],
    "accession_cloud_layer": {
        "status": "pending_separate_source_unit",
        "reason": "即位日月旁云气、干支数另有独立观测/数表，不并入C50总纲算法。",
    },
    "explicit_exclusions": {
        "C42": "卷九历数长短/安居术的策数与纳甲算法，不等于C50帝王始终总纲。",
        "single_formula": "当前直接正文未给一个可替代全部证据层的单一总年限公式。",
    },
}

LEGACY_REFERENCE_AUDIT = {
    "canonical_equivalent": False,
    "legacy_locations": [
        "guiyun.ehui_xingxian",
        "guiyun.lishu_changduan",
        "guiyun.yunqi_zhanbo",
        "guiyun.zonghe",
    ],
    "issues": [
        "旧代码把总纲拆散在多个函数，未保存层级关系",
        "旧ehui_xingxian又把基础厄会简化成十六位步数，已由C43隔离",
        "旧lishu_changduan属于卷九策数/纳甲算法，不能代替C50帝王始终总纲",
        "旧yunqi_zhanbo只是一部分云气观察，不能反向充当总年限公式",
    ],
}


def imperial_lishu_scope() -> dict[str, Any]:
    """返回C50来源职责；本函数不计算具体终年。"""
    return {
        "schema_version": "1.0",
        "canonical": C50_VERSION,
        "rule_id": "C50-V10-LISHU-SCOPE",
        "source_profile": "tongzong_volume10_imperial_lishu_scope",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "scope": copy.deepcopy(SCOPE),
        "specific_end_year": None,
        "specific_end_year_status": "not_computed_by_scope_contract",
        "single_formula_applied": False,
        "policy": (
            "C50只定义帝王始终历数的证据层级；"
            "基础厄会由C43类显式证据承载，太游/小游/格局作校验层。"
            "不得用C42策数余数或任一旧摘要函数直接生成帝王终年。"
        ),
    }


def _validate_optional_rule(
    value: dict[str, Any] | None,
    *,
    expected_rule_id: str,
    label: str,
) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise TypeError(f"{label}须为dict或None")
    if value.get("rule_id") != expected_rule_id:
        raise ValueError(f"{label}必须来自{expected_rule_id}")
    return copy.deepcopy(value)


def assemble_imperial_lishu_evidence(
    *,
    ehui: dict[str, Any] | None = None,
    taiyou_inner: dict[str, Any] | None = None,
    xiaoyou_hexagram: dict[str, Any] | None = None,
    xiaoyou_omens: dict[str, Any] | None = None,
    pattern_evidence: list[str] | None = None,
    hegod_period_evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """只汇总显式证据，不输出“帝王终年”。"""
    ehui_data = _validate_optional_rule(
        ehui,
        expected_rule_id="C43-V9-EHUI",
        label="ehui",
    )
    taiyou_data = _validate_optional_rule(
        taiyou_inner,
        expected_rule_id="C38-BL-INNER",
        label="taiyou_inner",
    )
    xiaoyou_data = _validate_optional_rule(
        xiaoyou_hexagram,
        expected_rule_id="C47-XY-HEX",
        label="xiaoyou_hexagram",
    )
    omen_data = _validate_optional_rule(
        xiaoyou_omens,
        expected_rule_id="C48-XY-OMEN",
        label="xiaoyou_omens",
    )

    if pattern_evidence is None:
        patterns = []
        patterns_checked = False
    elif not isinstance(pattern_evidence, list) or not all(
        isinstance(item, str) for item in pattern_evidence
    ):
        raise TypeError("pattern_evidence须为字符串list或None")
    else:
        patterns = list(pattern_evidence)
        patterns_checked = True

    if hegod_period_evidence is None:
        hegod = []
        hegod_checked = False
    elif not isinstance(hegod_period_evidence, list) or not all(
        isinstance(item, dict) for item in hegod_period_evidence
    ):
        raise TypeError("hegod_period_evidence须为dict list或None")
    else:
        hegod = copy.deepcopy(hegod_period_evidence)
        hegod_checked = True

    pending = []
    if not ehui_data:
        pending.append("缺基础厄会C43证据")
    if not hegod_checked:
        pending.append("缺太阳/阴主合神四神期的显式核对")
    if not patterns_checked:
        pending.append("缺囚迫击格掩挟等格局核对；无格局时传空list")

    correction_layers = {
        "taiyou_inner": taiyou_data,
        "xiaoyou_hexagram": xiaoyou_data,
        "xiaoyou_omens": omen_data,
        "pattern_evidence": patterns,
    }

    return {
        "schema_version": "1.0",
        "canonical": C50_VERSION,
        "rule_id": "C50-V10-LISHU-EVIDENCE",
        "source_profile": "tongzong_volume10_imperial_lishu_scope",
        "scope": imperial_lishu_scope(),
        "base_ehui": ehui_data,
        "hegod_period_evidence": hegod,
        "correction_layers": correction_layers,
        "evidence_ready": not pending,
        "status": "evidence_bundle_ready" if not pending else "partial_evidence",
        "pending": pending,
        "specific_end_year": None,
        "specific_end_year_computed": False,
        "single_formula_applied": False,
        "policy": (
            "即使证据齐备，C50也只返回证据包；"
            "当前来源未给可由这些层自动折算成单一帝王终年的统一公式。"
        ),
    }


def c50_catalog() -> dict[str, Any]:
    return {
        "canonical": C50_VERSION,
        "rule_id": "C50-V10-LISHU-SCOPE",
        "source_profile": "tongzong_volume10_imperial_lishu_scope",
        "scope": copy.deepcopy(SCOPE),
        "legacy_reference_audit": copy.deepcopy(LEGACY_REFERENCE_AUDIT),
    }
