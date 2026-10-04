"""C60 旧错误公式 / 非等价旧实现隔离注册表。

本模块不是新的算法来源，而是治理层：
- 把已经核定为错误、过度简化、混层或非 canonical 等价的旧实现集中登记；
- 所有条目 promotion_allowed=False；
- 明确 replacement rule / layer；
- 现代但合法的独立 profile 不因“非古籍”被误标成错误公式。

新增旧实现时，若已有来源审计判定其不可直接升格，应在这里登记。
"""

from __future__ import annotations

import copy
from typing import Any

C60_VERSION = "taiyi-c60-legacy-formula-quarantine-v1"


def _q(
    identifier: str,
    *,
    category: str,
    reason: str,
    replacement_rule_ids: tuple[str, ...] = (),
    replacement_layer: str | None = None,
    source_module: str,
    severity: str = "high",
) -> dict[str, Any]:
    return {
        "identifier": identifier,
        "category": category,
        "severity": severity,
        "promotion_allowed": False,
        "canonical_equivalent": False,
        "reason": reason,
        "replacement_rule_ids": list(replacement_rule_ids),
        "replacement_layer": replacement_layer,
        "source_module": source_module,
    }


QUARANTINE: dict[str, dict[str, Any]] = {
    # 十精：明确周期/路径错误或“周期相合但公式并未被证明等价”。
    "config.flybird": _q(
        "config.flybird",
        category="wrong_cycle_and_incomplete_path",
        reason="旧%8且八项路径遗漏中五；直接来源为90大周/9小周/九宫。",
        replacement_rule_ids=("C53-FLYBIRD",),
        replacement_layer="ten_essences.positions",
        source_module="ten_essences_positions",
    ),
    "config.fivewind": _q(
        "config.fivewind",
        category="wrong_cycle",
        reason="旧外层%29无直接依据；来源为90大周/9小周。",
        replacement_rule_ids=("C53-FIVEWIND",),
        replacement_layer="ten_essences.positions",
        source_module="ten_essences_positions",
    ),
    "config.eightwind": _q(
        "config.eightwind",
        category="incomplete_path",
        reason="旧表仅八项并漏中五；直接正文要求九宫完整路径。",
        replacement_rule_ids=("C53-EIGHTWIND",),
        replacement_layer="ten_essences.positions",
        source_module="ten_essences_positions",
    ),
    "config.threewind": _q(
        "config.threewind",
        category="incomplete_path",
        reason="旧八项表漏九宫项，余0分支也不是可审计九步路径。",
        replacement_rule_ids=("C53-THREEWIND",),
        replacement_layer="ten_essences.positions",
        source_module="ten_essences_positions",
    ),
    "config.taijun": _q(
        "config.taijun",
        category="non_equivalent_legacy_route",
        reason="旧mod4只给结果映射，未保存40/4、四正宫路径及阴阳起点来源。",
        replacement_rule_ids=("C53-TAIZUN",),
        replacement_layer="ten_essences.positions",
        source_module="ten_essences_positions",
        severity="medium",
    ),
    "config.wuxing": _q(
        "config.wuxing",
        category="non_equivalent_legacy_route",
        reason="小周5表面相合，但旧函数未保存50/5与阴阳两条来源路径。",
        replacement_rule_ids=("C53-WUXING",),
        replacement_layer="ten_essences.positions",
        source_module="ten_essences_positions",
        severity="medium",
    ),
    "config.tian_wang": _q(
        "config.tian_wang",
        category="non_equivalent_legacy_route",
        reason="小周20相合不足；canonical必须保存200/20、十六神顺行、四维重留和阴局对冲。",
        replacement_rule_ids=("C55-TIANHUANG",),
        replacement_layer="ten_essences.positions",
        source_module="ten_essences_sixteen_gods",
    ),
    "config.kingfu": _q(
        "config.kingfu",
        category="non_equivalent_legacy_route",
        reason="小周20相合不足；canonical必须保存帝符名称边界、四正重留、阴局对冲与17/70盈差隔离。",
        replacement_rule_ids=("C55-DIFU",),
        replacement_layer="ten_essences.positions",
        source_module="ten_essences_sixteen_gods",
    ),
    "config.tian_shi": _q(
        "config.tian_shi",
        category="non_equivalent_legacy_route",
        reason="小周12相合不足；canonical必须保存120/12、阳寅阴申、两遁顺行及太白内部异文。",
        replacement_rule_ids=("C56-TIANSHI",),
        replacement_layer="ten_essences.positions",
        source_module="ten_essences_tianshi",
    ),
    "yunqi._TEN_JING_FN": _q(
        "yunqi._TEN_JING_FN",
        category="wrong_name_set",
        reason="旧名单把帝符写作地符，并用太岁替代第十项太乙数。",
        replacement_rule_ids=("C52-TEN-ESSENCES-REGISTRY",),
        replacement_layer="ten_essences.registry",
        source_module="ten_essences_source_registry",
    ),
    "yunqi.shijing_shu": _q(
        "yunqi.shijing_shu",
        category="mixed_layers",
        reason=(
            "360→72数值核心可参校，但旧wrapper把特殊数值直接混入天气断语，"
            "且未保存数50句读异文与主计/天目/飞鸟显式关系。整体不可升格。"
        ),
        replacement_rule_ids=("C54-TAIYI-NUMBER", "C59-TAIYI-NUMBER-OMEN"),
        replacement_layer="ten_essences.number_and_weather",
        source_module="ten_essences_number_omens",
        severity="medium",
    ),
    "yunqi._YUNQI_COLOR.white": _q(
        "yunqi._YUNQI_COLOR.white",
        category="wrong_cloud_timing_mapping",
        reason=(
            "旧表把白云7/6配亥子；统宗、金镜、武经平行见证均支持"
            "白7/6→申酉，亥子属于黑1/8。"
        ),
        replacement_rule_ids=("C58-CLOUD-TIMING",),
        replacement_layer="ten_essences.cloud_observations",
        source_module="ten_essences_cloud_observations",
    ),

    # 卷九/十等已明确不等价的旧实现。
    "guiyun.yinyang_jiu_e": _q(
        "guiyun.yinyang_jiu_e",
        category="wrong_threshold_model",
        reason="旧函数把九段段长直接当累计阈值，第二段以后区段定位错误。",
        replacement_rule_ids=("C46-YJ-9E",),
        replacement_layer="volume9.nine_calamities",
        source_module="yinyang_nine_calamities",
    ),
    "guiyun.ehui_xingxian": _q(
        "guiyun.ehui_xingxian",
        category="oversimplified_formula",
        reason="旧函数只用年支并按16位简单步数，不能表达太阳/阴主落点、顺逆界与神数累计。",
        replacement_rule_ids=("C43-V9-EHUI",),
        replacement_layer="volume9.ehui_limit",
        source_module="volume9_ehui",
    ),
    "guiyun.guozheng_bianyi": _q(
        "guiyun.guozheng_bianyi",
        category="underspecified_formula",
        reason="旧函数只收年支静态旋转六神，不能表达完整创立年、六神落宫、算长短和格局证据。",
        replacement_rule_ids=("C44-V9-GOV",),
        replacement_layer="volume9.governance_change",
        source_module="volume9_governance",
    ),
    "guiyun.suizhong_zaifa": _q(
        "guiyun.suizhong_zaifa",
        category="oversimplified_formula",
        reason="旧函数用十六位offset且只做简化月层，不能替代合神加岁/月支的月日两阶段。",
        replacement_rule_ids=("C45-V9-DISASTER",),
        replacement_layer="volume9.disaster_timing",
        source_module="volume9_disaster_timing",
    ),
    "guiyun.yunqi_zhanbo": _q(
        "guiyun.yunqi_zhanbo",
        category="semantic_formula_errors",
        reason="旧函数遗漏日支五行、云生辰语义错位、己数错误并用if/elif压扁多重关系。",
        replacement_rule_ids=("C51-CLOUD-OMEN",),
        replacement_layer="coronation_cloud_omens",
        source_module="coronation_cloud_omens",
    ),
    "guiyun.outer_hexagram_offset_50": _q(
        "guiyun.outer_hexagram_offset_50",
        category="unsupported_offset",
        reason="旧大游外卦+50偏移当前无直接明文可证，不得写入C41重卦。",
        replacement_rule_ids=("C41-DY-HEX",),
        replacement_layer="dayou.hexagram",
        source_module="dayou_hexagram",
        severity="medium",
    ),
    "legacy.flybird_wl": _q(
        "legacy.flybird_wl",
        category="wrong_observation_model",
        reason="旧函数从盘内飞鸟位置生成军事断语，不能替代J4M-11要求的外部风云飞鸟观测。",
        replacement_rule_ids=("J4M-11",),
        replacement_layer="jinjing.volume4.military_observation",
        source_module="jinjing_v4_military",
    ),
}


def quarantine_record(identifier: str) -> dict[str, Any]:
    """返回单个隔离条目；未知项不猜测为错误。"""
    try:
        return copy.deepcopy(QUARANTINE[identifier])
    except KeyError as exc:
        raise KeyError(f"未登记的旧公式/实现: {identifier}") from exc


def is_quarantined(identifier: str) -> bool:
    return identifier in QUARANTINE


def quarantine_registry() -> dict[str, Any]:
    records = [copy.deepcopy(QUARANTINE[key]) for key in sorted(QUARANTINE)]
    return {
        "schema_version": "1.0",
        "canonical": C60_VERSION,
        "rule_id": "C60-LEGACY-QUARANTINE",
        "record_count": len(records),
        "records": records,
        "all_promotion_blocked": all(not row["promotion_allowed"] for row in records),
        "policy": (
            "这里只收已经有来源审计依据的错误/非等价旧实现；"
            "未知旧代码保持待审，不因未登记而自动视为canonical。"
            "现代独立profile不等于错误公式，必须另按source_class隔离。"
        ),
    }
