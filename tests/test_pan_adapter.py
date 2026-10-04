import copy

from kintaiyi.pan_adapter import (
    ADAPTER_VERSION,
    attach_v2_to_snapshot,
    build_v2_from_legacy_snapshot,
    extract_legacy_snapshot_facts,
)
from kintaiyi.v2_consumer import read_v2_analysis, resolve_v2_payload


def _legacy_snapshot():
    return {
        "太乙計": "年計",
        "太乙公式類別": "統宗",
        "公元日期": "2026-10-05 12:00",
        "干支": ["丙午", "丁酉", "甲子", "庚午"],
        "農曆": {"年": 2026, "月": 8, "日": 25},
        "局式": {"數": 17, "文": "陽遁十七局"},
        "太乙落宮": 1,
        "太乙": "乾",
        "文昌": ["辰", "旧描述只保存"],
        "始擊": "午",
        "定目": "申",
        "主算": [15, ["旧描述可能过时"]],
        "客算": [17, ["旧描述"]],
        "定算": [5, ["旧描述"]],
        "主將": 6,
        "主參": 7,
        "客將": 8,
        "客參": 9,
        "八門值事": "開",
        "八門分佈": {1: "開"},
        "君基": 3,
        "臣基": 4,
        "民基": 5,
        "五福": {"宫": 2},
        "大游": {"宫": 7},
        "小游": {"宫": 8},
        # 以下必须隔离，不能提升：
        "軍事戰略": {"winner": "旧混合法主胜"},
        "推猛虎相拒": "吉利成正但不可攻",
        "運籌博弈分析": {"博弈均衡值": 99},
        "卷十二": {"legacy": True},
    }


def test_extracts_only_snapshot_facts_without_recomputing():
    facts = extract_legacy_snapshot_facts(_legacy_snapshot())
    assert facts["meta"]["calculation_style"] == "年計"
    assert facts["meta"]["adapter"] == ADAPTER_VERSION
    assert facts["calendar"]["ganzhi"][0] == "丙午"
    assert facts["board"]["taiyi"] == {"palace": 1, "sector": "乾"}
    assert facts["board"]["calculations"]["home"]["value"] == 15
    assert facts["board"]["calculations"]["home"]["legacy_description"] == ["旧描述可能过时"]
    assert facts["board"]["generals"]["home_general"]["palace"] == 6
    assert facts["cycles"]["three_bases"]["ruler"] == 3


def test_old_military_and_old_game_theory_are_quarantined():
    v2 = build_v2_from_legacy_snapshot(_legacy_snapshot())
    assert v2["analysis"]["military"] == {}
    assert v2["modern"] == {}
    assert "軍事戰略" in v2["compat"]["quarantined_legacy_keys"]
    assert "推猛虎相拒" in v2["compat"]["quarantined_legacy_keys"]
    assert "運籌博弈分析" in v2["compat"]["quarantined_legacy_keys"]
    assert v2["compat"]["legacy_analysis_promoted"] is False
    assert v2["compat"]["legacy_modern_promoted"] is False


def test_structured_analysis_must_be_explicitly_supplied():
    military = {
        "source_profile": "volume5_strict",
        "cross_volume_merge": False,
    }
    seven_methods = {
        "tiger": {"rule_id": "T7-04", "verdict": "不可攻"},
    }
    v2 = build_v2_from_legacy_snapshot(
        _legacy_snapshot(),
        analysis={"military": military, "seven_methods": seven_methods},
    )
    assert v2["analysis"]["military"] == military
    assert v2["analysis"]["seven_methods"] == seven_methods


def test_modern_layer_must_be_explicitly_supplied():
    modern = {
        "game_theory": {
            "derived_modern_feature": True,
            "cross_system_palace_mapping": False,
        }
    }
    v2 = build_v2_from_legacy_snapshot(_legacy_snapshot(), modern=modern)
    assert v2["modern"] == modern
    assert v2["modern"]["game_theory"]["derived_modern_feature"] is True
    assert v2["modern"]["game_theory"] != _legacy_snapshot()["運籌博弈分析"]


def test_scenario_is_never_inferred_from_legacy_generals():
    snapshot = _legacy_snapshot()
    snapshot["客將"] = 9
    v2 = build_v2_from_legacy_snapshot(snapshot)
    assert "scenario" not in v2["meta"]

    v2 = build_v2_from_legacy_snapshot(
        snapshot,
        scenario={"enemy_first_arrival_taiyi_palace": 2},
    )
    assert v2["meta"]["scenario"]["enemy_first_arrival_taiyi_palace"] == 2
    assert v2["meta"]["scenario"]["enemy_first_arrival_taiyi_palace"] != snapshot["客將"]


def test_center_five_snapshot_is_normalized_by_builder():
    snapshot = _legacy_snapshot()
    snapshot["太乙落宮"] = 5
    snapshot["太乙"] = "中"
    v2 = build_v2_from_legacy_snapshot(snapshot)
    assert v2["board"]["taiyi"]["palace"] == 5
    assert v2["board"]["taiyi"]["sector"] is None


def test_unported_fields_are_recorded_without_becoming_canonical():
    v2 = build_v2_from_legacy_snapshot(_legacy_snapshot())
    assert "卷十二" in v2["compat"]["unported_legacy_keys"]
    assert "卷十二" not in v2["analysis"]
    assert "卷十二" not in v2["modern"]


def test_attach_v2_keeps_legacy_snapshot_for_compat_but_does_not_mutate_input():
    source = _legacy_snapshot()
    before = copy.deepcopy(source)
    result = attach_v2_to_snapshot(
        source,
        analysis={"military": {"source_profile": "volume5_strict"}},
    )
    assert source == before
    assert "v2" not in source
    assert result["軍事戰略"]["winner"] == "旧混合法主胜"
    assert result["v2"]["analysis"]["military"]["source_profile"] == "volume5_strict"


def test_attached_snapshot_is_consumed_v2_first():
    result = attach_v2_to_snapshot(
        _legacy_snapshot(),
        analysis={"military": {"source_profile": "volume5_strict"}},
    )
    resolved = resolve_v2_payload(result)
    military = read_v2_analysis(result, "military")
    assert resolved["source"] == "embedded_v2"
    assert military["data"]["source_profile"] == "volume5_strict"
    assert military["data"] != result["軍事戰略"]


def test_legacy_seven_method_lucky_words_cannot_enter_new_analysis_implicitly():
    snapshot = _legacy_snapshot()
    snapshot["推猛虎相拒"] = "成吉正利"
    v2 = build_v2_from_legacy_snapshot(snapshot)
    assert v2["analysis"]["seven_methods"] == {}
    assert "推猛虎相拒" in v2["compat"]["quarantined_legacy_keys"]
