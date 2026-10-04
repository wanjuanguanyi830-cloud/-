"""C22 卷十五 / 卷十七军事规则单元目录。

将 C21 综合 payload 拆成独立 source_rule_id。
这里只描述来源、输入依赖和跨层边界，不执行旧算法。
"""

from __future__ import annotations

import copy
from typing import Any

RULE_UNIT_VERSION = "taiyi-c22-military-rule-units-v1"


def _rule(
    rule_id: str,
    *,
    volume_profile: str,
    payload_key: str,
    source_title: str,
    function_name: str,
    inputs: tuple[str, ...],
    dependency_class: str,
    source_status: str = "source_rule",
    external_inputs: tuple[str, ...] = (),
    overlaps: tuple[str, ...] = (),
    notes: str = "",
) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "volume_profile": volume_profile,
        "payload_key": payload_key,
        "source_title": source_title,
        "reference_function": function_name,
        "inputs": list(inputs),
        "dependency_class": dependency_class,
        "source_status": source_status,
        "external_inputs": list(external_inputs),
        "overlaps": list(overlaps),
        "notes": notes,
    }


RULE_UNITS: dict[str, dict[str, Any]] = {
    # 卷十五军事应用
    "V15-01": _rule(
        "V15-01", volume_profile="tongzong_volume15",
        payload_key="奇兵伏兵",
        source_title="明奇兵伏兵之术／明出兵战阵所利术",
        function_name="qibing_fubing",
        inputs=("taiyi", "skyeyes", "shiji", "home_cal", "away_cal", "patterns"),
        dependency_class="high",
        overlaps=("J4M-10",),
        notes="与金镜卷四推奇伏法近名，必须保持独立source profile。",
    ),
    "V15-02": _rule(
        "V15-02", volume_profile="tongzong_volume15",
        payload_key="五陣置旗",
        source_title="明太乙置阵齐旗术／三五八阵之原",
        function_name="wuzhen_bazhen",
        inputs=("home_cal", "away_cal"),
        dependency_class="low",
    ),
    "V15-03": _rule(
        "V15-03", volume_profile="tongzong_volume15",
        payload_key="出兵稱神",
        source_title="明太乙出兵称神术",
        function_name="chubing_chengshen",
        inputs=("home_cal", "away_cal"),
        dependency_class="low",
    ),
    "V15-04": _rule(
        "V15-04", volume_profile="tongzong_volume15",
        payload_key="陳兵出鄉",
        source_title="明陈兵出乡术",
        function_name="chenbing_chuxiang",
        inputs=("home_cal", "away_cal"),
        dependency_class="low",
        overlaps=("J4M-06",),
        notes="不得用本条替代《金镜》卷四推陈兵向背。",
    ),
    "V15-05": _rule(
        "V15-05", volume_profile="tongzong_volume15",
        payload_key="選將之術",
        source_title="明选将之术",
        function_name="xuanjiang_zhi",
        inputs=(),
        dependency_class="static_text",
    ),
    "V15-06": _rule(
        "V15-06", volume_profile="tongzong_volume15",
        payload_key="教兵之術",
        source_title="明教兵之术",
        function_name="jiaobing_shu",
        inputs=(),
        dependency_class="static_text",
    ),
    "V15-07": _rule(
        "V15-07", volume_profile="tongzong_volume15",
        payload_key="隨地制變",
        source_title="随地制变／置阵随地",
        function_name="suidi_zhibian",
        inputs=("terrain_shape", "home_cal", "away_cal"),
        dependency_class="medium",
        external_inputs=("terrain_shape",),
        overlaps=("J4M-07", "J4M-08"),
        notes="与金镜制阵随地/随地制变分层，不自动合并。",
    ),
    "V15-08": _rule(
        "V15-08", volume_profile="tongzong_volume15",
        payload_key="分合用兵",
        source_title="明分合用兵之术",
        function_name="fenhe_yongbing",
        inputs=(
            "home_general", "away_general", "home_vassal", "away_vassal",
            "patterns", "three_doors", "five_generals",
        ),
        dependency_class="high",
        overlaps=("C8-L2", "C8-L3"),
    ),
    "V15-09": _rule(
        "V15-09", volume_profile="tongzong_volume15",
        payload_key="五音風",
        source_title="明五音考风以知盛衰之术",
        function_name="wuyin_feng",
        inputs=("day_branch", "hour_branch", "wind_direction_branch"),
        dependency_class="external_observation",
        external_inputs=("wind_direction_branch",),
    ),
    "V15-10": _rule(
        "V15-10", volume_profile="tongzong_volume15",
        payload_key="五音觀風察將",
        source_title="五音观风察将",
        function_name="guanfeng_chajiang",
        inputs=("wuyin_wind_result", "wind_sound"),
        dependency_class="derived_from_rule",
        external_inputs=("wind_sound",),
        overlaps=("V15-09",),
    ),
    "V15-11": _rule(
        "V15-11", volume_profile="tongzong_volume15",
        payload_key="安營置陣",
        source_title="安营置阵取用日时",
        function_name="anying_rishi",
        inputs=("taiyi", "skyeyes", "shiji", "patterns", "three_doors", "five_generals"),
        dependency_class="high",
    ),
    "V15-12": _rule(
        "V15-12", volume_profile="tongzong_volume15",
        payload_key="風從八卦",
        source_title="明风从八卦而分主客术",
        function_name="feng_bagua_zhuke",
        inputs=("wind_palace",),
        dependency_class="external_observation",
        external_inputs=("wind_palace",),
    ),
    "V15-13": _rule(
        "V15-13", volume_profile="tongzong_volume15",
        payload_key="雲氣逆順",
        source_title="云气所起逆顺",
        function_name="yunqi_nishun",
        inputs=("home_cal", "away_cal", "cloud_from_direction"),
        dependency_class="external_observation",
        external_inputs=("cloud_from_direction",),
    ),
    "V15-14": _rule(
        "V15-14", volume_profile="tongzong_volume15",
        payload_key="軍勢勝負",
        source_title="明出兵军势胜负术＋风云飞鸟",
        function_name="jungshi_shengfu_pan",
        inputs=(
            "taiyi", "home_cal", "away_cal", "wuyin_wind", "cloud_qi",
            "flybird_palace", "skyeyes", "shiji", "home_general", "away_general",
            "patterns",
        ),
        dependency_class="high_composite",
        overlaps=("J4M-11", "J4M-12"),
        notes="卷十五综合军势不得覆盖J4M外部风云飞鸟观测层。",
    ),

    # 卷十七军事占断
    "V17-01": _rule(
        "V17-01", volume_profile="tongzong_volume17",
        payload_key="出兵用時",
        source_title="明太乙出兵举事用日之术／用时之术",
        function_name="chubing_yongshi",
        inputs=(
            "home_cal", "away_cal", "skyeyes_state", "shiji_mask",
            "three_doors", "five_generals", "taiyi_door",
        ),
        dependency_class="high",
        overlaps=("J4M-05",),
    ),
    "V17-02": _rule(
        "V17-02", volume_profile="tongzong_volume17",
        payload_key="敵國動靜",
        source_title="明敌国动静",
        function_name="diguo_dongjing",
        inputs=(
            "away_cal", "three_doors", "five_generals", "taiyi", "skyeyes",
            "shiji", "home_general", "home_vassal", "away_general",
            "away_vassal", "skyeyes_state", "patterns",
        ),
        dependency_class="high",
        overlaps=("C8-L3",),
        notes="敌情占断应用，不是C8主客动静。",
    ),
    "V17-03": _rule(
        "V17-03", volume_profile="tongzong_volume17",
        payload_key="間諜虛實",
        source_title="明敌国有无间谍窥探术",
        function_name="jianmie_xushi",
        inputs=("taiyi", "shiji", "away_general", "skyeyes"),
        dependency_class="medium",
    ),
    "V17-04": _rule(
        "V17-04", volume_profile="tongzong_volume17",
        payload_key="敵使虛實",
        source_title="明敌使虚实之术",
        function_name="dishi_xushi",
        inputs=("taiyi", "shiji", "away_general"),
        dependency_class="medium",
    ),
    "V17-05": _rule(
        "V17-05", volume_profile="tongzong_volume17",
        payload_key="敵兵來方",
        source_title="明敌人来方将卒多寡",
        function_name="dibing_laifang",
        inputs=("taiyi", "away_cal", "shiji", "yin_yang"),
        dependency_class="medium",
    ),
    "V17-06": _rule(
        "V17-06", volume_profile="tongzong_volume17",
        payload_key="見聞虛實",
        source_title="见闻占虚实",
        function_name="jianwen_xushi",
        inputs=(
            "taiyi", "skyeyes", "shiji", "skyeyes_state", "three_doors",
            "five_generals", "patterns", "shiji_mask", "shiji_hit",
            "home_general", "home_vassal", "away_general", "away_vassal",
        ),
        dependency_class="high",
    ),
    "V17-07": _rule(
        "V17-07", volume_profile="tongzong_volume17",
        payload_key="討捕叛亡",
        source_title="讨捕叛亡",
        function_name="taobu_panwang",
        inputs=(
            "taiyi", "skyeyes", "shiji", "home_general", "patterns",
            "skyeyes_state", "shiji_mask", "wax_wane",
        ),
        dependency_class="high",
    ),
    "V17-08": _rule(
        "V17-08", volume_profile="tongzong_volume17",
        payload_key="執囚對吏",
        source_title="执囚对吏",
        function_name="zhiqu_duili",
        inputs=(
            "taiyi", "skyeyes", "home_general", "home_cal", "patterns",
            "shiji_mask", "shiji_hit", "wax_wane",
        ),
        dependency_class="high",
    ),
    "V17-09": _rule(
        "V17-09", volume_profile="tongzong_volume17",
        payload_key="求索所得",
        source_title="明求索有无所得术",
        function_name="qiusuo_suode",
        inputs=(
            "taiyi", "skyeyes", "home_general", "patterns",
            "skyeyes_state", "shiji_ge", "wax_wane",
        ),
        dependency_class="high",
        overlaps=("volume5_inner_outer_attack",),
    ),
    "V17-D1": _rule(
        "V17-D1", volume_profile="cross_volume_helper",
        payload_key="孤虛對照",
        source_title="卷五内外占攻击 × 卷十七求索所得 对照",
        function_name="guxu_duizhao",
        inputs=(
            "taiyi", "skyeyes", "home_general", "patterns",
            "skyeyes_state", "shiji_ge", "wax_wane",
        ),
        dependency_class="derived_cross_volume",
        source_status="derived_cross_volume_helper",
        overlaps=("volume5_inner_outer_attack", "V17-09"),
        notes="不是独立卷十七原法；不得分配V17 canonical source rule号。",
    ),
    "V17-10": _rule(
        "V17-10", volume_profile="tongzong_volume17",
        payload_key="時計諸事",
        source_title="时计占诸事",
        function_name="shiji_zhanshi",
        inputs=(
            "taiyi", "skyeyes", "skyeyes_state", "three_doors", "five_generals",
            "home_cal", "away_cal", "patterns", "shiji_mask", "shiji_hit",
            "wax_wane",
        ),
        dependency_class="high",
    ),
    "V17-11": _rule(
        "V17-11", volume_profile="tongzong_volume17",
        payload_key="占望行人",
        source_title="占望行人及贼来与不来",
        function_name="zhanwang_xingren",
        inputs=("taiyi", "home_cal", "away_cal", "skyeyes", "shiji", "patterns"),
        dependency_class="medium",
    ),
}


def rule_unit(rule_id: str) -> dict[str, Any]:
    if rule_id not in RULE_UNITS:
        raise ValueError(f"未知军事rule_id: {rule_id}")
    return copy.deepcopy(RULE_UNITS[rule_id])


def units_for_profile(profile: str) -> list[dict[str, Any]]:
    return [
        copy.deepcopy(item)
        for item in RULE_UNITS.values()
        if item["volume_profile"] == profile
    ]


def payload_key_to_rule_id() -> dict[str, str]:
    """旧综合payload key -> 独立规则号。"""
    return {
        item["payload_key"]: rid
        for rid, item in RULE_UNITS.items()
    }


def low_dependency_candidates() -> list[dict[str, Any]]:
    """下一批适合逐条实现的低依赖候选，不含跨卷helper。"""
    allowed = {"low", "static_text", "external_observation"}
    return [
        copy.deepcopy(item)
        for item in RULE_UNITS.values()
        if item["source_status"] == "source_rule"
        and item["dependency_class"] in allowed
    ]


def military_rule_unit_catalog() -> dict[str, Any]:
    v15 = units_for_profile("tongzong_volume15")
    v17 = units_for_profile("tongzong_volume17")
    helpers = units_for_profile("cross_volume_helper")
    return {
        "canonical": RULE_UNIT_VERSION,
        "source_rule_count": len(v15) + len(v17),
        "volume15_source_rules": v15,
        "volume17_source_rules": v17,
        "derived_helpers": helpers,
        "low_dependency_candidates": low_dependency_candidates(),
        "policy": (
            "综合卷次只作容器；每条术法独立rule_id。跨卷helper另列，"
            "不得冒充某一卷canonical source rule。"
        ),
    }
