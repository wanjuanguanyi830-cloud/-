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
    "yunqi._YUNQI_COLOR": _q(
        "yunqi._YUNQI_COLOR",
        category="mixed_wrong_and_unsupported_cloud_table",
        reason=(
            "旧表除白7/6→亥子错误外，还混入黄5、黑6、红2/7等"
            "当前直接十精初移宫云色时变条未支持的独立计数/色名；不得整体升格。"
        ),
        replacement_rule_ids=("C58-CLOUD-TIMING", "C58-WEATHER-OBSERVATION"),
        replacement_layer="ten_essences.cloud_observations",
        source_module="ten_essences_cloud_observations",
    ),
    "yunqi._shu_duanyu": _q(
        "yunqi._shu_duanyu",
        category="wrong_special_number_omens",
        reason=(
            "旧函数把数10/5做成独立特例，并把数40的黄雾混到数50；"
            "数50本身又存在统宗/金镜与武经句读异文。"
        ),
        replacement_rule_ids=("C59-TAIYI-NUMBER-OMEN",),
        replacement_layer="ten_essences.number_omens",
        source_module="ten_essences_number_omens",
    ),
    "yunqi._JING_HEHUI": _q(
        "yunqi._JING_HEHUI",
        category="mixed_inaccurate_conjunction_table",
        reason=(
            "旧表含地符旧名、若干宫位/合会断语错配与过度摘要，"
            "且未保存旺相、阴阳宫及真实异文条件。"
        ),
        replacement_rule_ids=("C57-TEN-ESSENCE-CLOUD-CONJUNCTION",),
        replacement_layer="ten_essences.cloud_conjunctions",
        source_module="ten_essences_cloud_omens",
    ),
    "yunqi.shijing_luo": _q(
        "yunqi.shijing_luo",
        category="derived_from_wrong_legacy_ten_essence_map",
        reason=(
            "旧落宫wrapper直接遍历错误的_TEN_JING_FN，"
            "继承地符/太岁错名及多项旧位置公式，不能作为十精位置真源。"
        ),
        replacement_rule_ids=(
            "C52-TEN-ESSENCES-REGISTRY",
            "C53-FLYBIRD",
            "C53-FIVEWIND",
            "C53-TAIZUN",
            "C53-EIGHTWIND",
            "C53-THREEWIND",
            "C53-WUXING",
            "C55-TIANHUANG",
            "C55-DIFU",
            "C56-TIANSHI",
        ),
        replacement_layer="ten_essences.positions",
        source_module="ten_essences_source_registry",
    ),
    "yunqi.yunqi_hehui": _q(
        "yunqi.yunqi_hehui",
        category="automatic_relation_inference",
        reason=(
            "旧函数仅凭旧落宫数相等自动制造‘合太乙’，并用简化阴阳宫集合补断；"
            "C57要求合会事实显式输入，禁止从位置自动生成。"
        ),
        replacement_rule_ids=("C57-TEN-ESSENCE-CLOUD-CONJUNCTION",),
        replacement_layer="ten_essences.cloud_conjunctions",
        source_module="ten_essences_cloud_omens",
    ),
    "yunqi.yunqi_zongduan": _q(
        "yunqi.yunqi_zongduan",
        category="mixed_layers_and_auto_inference",
        reason=(
            "旧综合wrapper把错误位置、太乙数、自动同宫、云色表和子房总诀一次混合；"
            "C52-C59已拆成独立来源层，禁止回写成单一canonical公式。"
        ),
        replacement_rule_ids=(
            "C52-TEN-ESSENCES-REGISTRY",
            "C57-TEN-ESSENCE-CLOUD-CONJUNCTION",
            "C58-CLOUD-TIMING",
            "C58-WEATHER-OBSERVATION",
            "C59-TAIYI-NUMBER-OMEN",
        ),
        replacement_layer="ten_essences.layered_runtime",
        source_module="ten_essences_source_registry",
    ),
    "yunqi.zonghe": _q(
        "yunqi.zonghe",
        category="legacy_composite_wrapper",
        reason=(
            "旧总合继续依赖yunqi_zongduan并自动计算同宫，"
            "只能作为历史展示包装器，不能成为任何来源层真源。"
        ),
        replacement_rule_ids=(
            "C57-TEN-ESSENCE-CLOUD-CONJUNCTION",
            "C58-CLOUD-TIMING",
            "C58-WEATHER-OBSERVATION",
            "C59-TAIYI-NUMBER-OMEN",
        ),
        replacement_layer="ten_essences.layered_runtime",
        source_module="ten_essences_source_registry",
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
    "config.wenchang_nine_stars": _q(
        "config.wenchang_nine_stars",
        category="mixed_witness_names_and_wrong_landing_map",
        reason=(
            "旧实现虽按2700/270/30计算统宗直事周期，但星名表混入文曲/昭摇/立华等异读，"
            "丁误落巽9、壬误落中5；且所谓九星分布循环计算gong后未使用，实际仍返回固定表。"
            "不得作为统宗NGJ或紫庭附篇canonical。"
        ),
        replacement_rule_ids=("C70-TONGZONG-WENCHANG-NINE-STARS",),
        replacement_layer="source_variants.tongzong_volume6.wenchang_nine_stars",
        source_module="wenchang_nine_stars_tongzong",
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
