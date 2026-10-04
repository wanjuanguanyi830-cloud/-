"""C30 pan v2 最终聚合契约。

只组装已经结构化的结果，固定 analysis / modern / source_variants 的职责边界。
不调用任何太乙算法。
"""

from __future__ import annotations

import copy
from typing import Any

from .pan_v2 import build_pan_v2, validate_pan_v2

CONTRACT_VERSION = "taiyi-c30-pan-v2-contract-v1"

ANALYSIS_KEYS = ("patterns", "eight_divinations", "seven_methods", "military")
SOURCE_VARIANT_KEYS = ("patterns", "military", "zitingjing", "military_derived", "wuyun_wuyin")
MODERN_KEYS = ("game_theory",)

LEGACY_FORBIDDEN_KEYS = {
    "軍事戰略", "军事战略",
    "運籌博弈分析", "运筹博弈分析",
    "太乙九星", "文昌九星", "文昌變化", "文昌变化", "始擊變化", "始击变化",
    "三旗行宮", "三旗行宫", "九宮貴神", "九宫贵神",
    "五運六氣", "五运六气", "五音之數", "五音之数",
}


def _dict_or_empty(name: str, value: dict[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise TypeError(f"{name}须为dict或None")
    return copy.deepcopy(value)


def build_analysis_contract(
    *,
    patterns: dict[str, Any] | None = None,
    eight_divinations: dict[str, Any] | None = None,
    seven_methods: dict[str, Any] | None = None,
    military: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """构建 v2.analysis。

    military 只接 canonical/明确组合分析（如C8），不接卷十五/十七 derived profile。
    """
    data = {
        "patterns": _dict_or_empty("patterns", patterns),
        "eight_divinations": _dict_or_empty("eight_divinations", eight_divinations),
        "seven_methods": _dict_or_empty("seven_methods", seven_methods),
        "military": _dict_or_empty("military", military),
    }
    for section, value in data.items():
        forbidden = sorted(set(value) & LEGACY_FORBIDDEN_KEYS)
        if forbidden:
            raise ValueError(
                f"analysis.{section}含legacy flat键: {', '.join(forbidden)}"
            )
    if data["military"].get("derived_military_profile") is True:
        raise ValueError("derived military profile不得放analysis.military")
    return data


def build_source_variants_contract(
    *,
    patterns: dict[str, Any] | None = None,
    military: dict[str, Any] | None = None,
    zitingjing: dict[str, Any] | None = None,
    military_derived: dict[str, Any] | None = None,
    wuyun_wuyin: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """构建 v2.source_variants 的固定五槽。

    空槽省略；不同来源槽不自动深合并。
    """
    supplied = {
        "patterns": patterns,
        "military": military,
        "zitingjing": zitingjing,
        "military_derived": military_derived,
        "wuyun_wuyin": wuyun_wuyin,
    }
    out: dict[str, Any] = {}
    for key, value in supplied.items():
        if value is None:
            continue
        if not isinstance(value, dict):
            raise TypeError(f"source_variants.{key}须为dict")
        out[key] = copy.deepcopy(value)
    return out


def build_modern_contract(
    *,
    game_theory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """构建 v2.modern；现代博弈必须带 derived 标记。"""
    out: dict[str, Any] = {}
    if game_theory is not None:
        if not isinstance(game_theory, dict):
            raise TypeError("modern.game_theory须为dict")
        if game_theory.get("derived_modern_feature") is not True:
            raise ValueError("modern.game_theory必须标derived_modern_feature=True")
        out["game_theory"] = copy.deepcopy(game_theory)
    return out


def build_structured_pan_v2(
    *,
    meta: dict[str, Any] | None = None,
    calendar: dict[str, Any] | None = None,
    board: dict[str, Any] | None = None,
    cycles: dict[str, Any] | None = None,
    patterns: dict[str, Any] | None = None,
    eight_divinations: dict[str, Any] | None = None,
    seven_methods: dict[str, Any] | None = None,
    military: dict[str, Any] | None = None,
    modern_game_theory: dict[str, Any] | None = None,
    pattern_variants: dict[str, Any] | None = None,
    military_variants: dict[str, Any] | None = None,
    zitingjing_variants: dict[str, Any] | None = None,
    military_derived_variants: dict[str, Any] | None = None,
    wuyun_wuyin_variants: dict[str, Any] | None = None,
    compat: dict[str, Any] | None = None,
    scenario: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """按C30固定槽位组装完整 pan v2。"""
    analysis = build_analysis_contract(
        patterns=patterns,
        eight_divinations=eight_divinations,
        seven_methods=seven_methods,
        military=military,
    )
    modern = build_modern_contract(game_theory=modern_game_theory)
    variants = build_source_variants_contract(
        patterns=pattern_variants,
        military=military_variants,
        zitingjing=zitingjing_variants,
        military_derived=military_derived_variants,
        wuyun_wuyin=wuyun_wuyin_variants,
    )
    payload = build_pan_v2(
        meta=meta,
        calendar=calendar,
        board=board,
        cycles=cycles,
        analysis=analysis,
        modern=modern,
        source_variants=variants,
        compat=compat,
        scenario=scenario,
    )
    payload["meta"]["aggregation_contract"] = CONTRACT_VERSION
    return payload


def validate_structured_pan_v2(payload: dict[str, Any]) -> dict[str, Any]:
    """在C11 schema validator之上检查C30层级边界。"""
    base = validate_pan_v2(payload)
    errors = list(base["errors"])
    warnings = list(base["warnings"])

    analysis = payload.get("analysis", {})
    if isinstance(analysis, dict):
        military = analysis.get("military", {})
        if isinstance(military, dict) and military.get("derived_military_profile") is True:
            errors.append("analysis.military不得放derived military profile")
        for section in ANALYSIS_KEYS:
            value = analysis.get(section, {})
            if isinstance(value, dict):
                forbidden = sorted(set(value) & LEGACY_FORBIDDEN_KEYS)
                if forbidden:
                    errors.append(
                        f"analysis.{section}含legacy flat键:{','.join(forbidden)}"
                    )

    modern = payload.get("modern", {})
    if isinstance(modern, dict) and "game_theory" in modern:
        gt = modern["game_theory"]
        if not isinstance(gt, dict) or gt.get("derived_modern_feature") is not True:
            errors.append("modern.game_theory缺derived_modern_feature=True")

    variants = payload.get("source_variants", {})
    if isinstance(variants, dict):
        unknown = sorted(set(variants) - set(SOURCE_VARIANT_KEYS))
        if unknown:
            errors.append(f"未知source_variants根槽:{','.join(unknown)}")

    contract = (payload.get("meta") or {}).get("aggregation_contract")
    if contract != CONTRACT_VERSION:
        warnings.append("payload未标当前C30 aggregation_contract")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "schema_version": payload.get("schema_version"),
        "aggregation_contract": contract,
    }
