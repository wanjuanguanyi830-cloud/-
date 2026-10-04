import pytest

from kintaiyi.ten_essences_cloud_omens import (
    CONJUNCTION_RULES,
    DEFERRED_OBSERVATION_LAYERS,
    PALACE_RULES,
    ZHANGLIANG_SUMMARY_VARIANT,
    c57_catalog,
    ten_essence_cloud_conjunctions,
)


def test_c57_requires_explicit_conjunction_check():
    data = ten_essence_cloud_conjunctions("帝符")
    assert data["conjunctions_checked"] is False
    assert data["status"] == "partial_explicit_evidence"
    assert "无合会时传空list" in "；".join(data["pending"])
    assert data["auto_position_lookup_used"] is False


def test_c57_explicit_empty_check_does_not_invent_omens():
    data = ten_essence_cloud_conjunctions("帝符", conjunctions=[])
    assert data["conjunctions_checked"] is True
    assert data["matched_omens"] == []
    assert data["status"] == "explicit_evidence_complete"


def test_c57_difu_taiyi_base_and_wangxiang_are_cumulative():
    data = ten_essence_cloud_conjunctions(
        "帝符",
        conjunctions=["太乙"],
        taiyi_qi_state="旺相",
    )
    effects = [item["effects"] for item in data["matched_omens"]]
    assert ["日晕", "大风"] in effects
    assert ["小雨", "小阴云", "疾风卒起"] in effects


def test_c57_difu_tianmu_direct_omen():
    data = ten_essence_cloud_conjunctions(
        "帝符",
        conjunctions=["天目"],
    )
    assert data["matched_omens"] == [{
        "kind": "conjunction",
        "essence": "帝符",
        "target": "天目",
        "effects": ["小阴疾风", "日月有变"],
        "source_status": "direct",
        "witness_variants": None,
    }]


def test_c57_tianshi_taiyi_requires_wangxiang_state():
    missing = ten_essence_cloud_conjunctions(
        "天时",
        conjunctions=["太乙"],
    )
    assert missing["matched_omens"] == []
    assert "taiyi_qi_state" in "；".join(missing["pending"])

    hit = ten_essence_cloud_conjunctions(
        "天时",
        conjunctions=["太乙"],
        taiyi_qi_state="旺相",
    )
    assert hit["matched_omens"][0]["effects"] == ["风云卒起", "或阴雨"]


def test_c57_flybird_taiyi_distinguishes_wangxiang_from_non_wangxiang():
    prosperous = ten_essence_cloud_conjunctions(
        "飞鸟",
        conjunctions=["太乙"],
        taiyi_qi_state="旺相",
    )
    assert prosperous["matched_omens"][0]["effects"] == ["天星有变"]

    weak = ten_essence_cloud_conjunctions(
        "飞鸟",
        conjunctions=["太乙"],
        taiyi_qi_state="休囚",
    )
    assert weak["matched_omens"][0]["effects"] == ["大风"]


def test_c57_eightwind_taiyi_can_match_qi_and_yinyang_layers():
    data = ten_essence_cloud_conjunctions(
        "八风",
        conjunctions=["太乙"],
        taiyi_qi_state="旺相",
        taiyi_palace_yinyang="阴",
    )
    effects = [item["effects"] for item in data["matched_omens"]]
    assert ["云起", "小雨"] in effects
    assert ["雨"] in effects


def test_c57_eightwind_yang_palace_is_wind():
    data = ten_essence_cloud_conjunctions(
        "八风",
        conjunctions=["太乙"],
        taiyi_qi_state="非旺相",
        taiyi_palace_yinyang="阳",
    )
    assert [item["effects"] for item in data["matched_omens"]] == [["风"]]


def test_c57_taizun_and_flybird_palace_rules_are_separate():
    taizun = ten_essence_cloud_conjunctions(
        "太尊",
        conjunctions=[],
        essence_palace=8,
    )
    assert taizun["matched_omens"] == [{
        "kind": "palace",
        "essence": "太尊",
        "palace": 8,
        "effects": ["日晕"],
        "source_status": "direct",
    }]

    flybird = ten_essence_cloud_conjunctions(
        "飞鸟",
        conjunctions=[],
        essence_palace=6,
    )
    assert flybird["matched_omens"][0]["effects"] == ["日晕"]


def test_c57_five_elements_normalizes_difu_name_only():
    data = ten_essence_cloud_conjunctions(
        "五行",
        conjunctions=["帝符"],
    )
    item = data["matched_omens"][0]
    assert item["effects"] == ["风昏", "小阴"]
    assert item["source_status"] == "normalized_name_only"
    assert item["witness_variants"] == {
        "tongzong_online": "地符合",
        "wujing_zongyao": "帝符合",
    }


def test_c57_tianhuang_flybird_preserves_minor_wording_variant():
    data = ten_essence_cloud_conjunctions(
        "天皇",
        conjunctions=["飞鸟"],
    )
    item = data["matched_omens"][0]
    assert item["effects"] == ["阴雨"]
    assert item["witness_variants"] == {
        "tongzong": "有阴雨",
        "wujing_zongyao": "小阴雨",
    }


def test_c57_unresolved_tianhuang_tianshi_variant_is_not_silently_selected():
    data = ten_essence_cloud_conjunctions(
        "天皇",
        conjunctions=["天时"],
    )
    item = data["matched_omens"][0]
    assert item["effects"] is None
    assert item["source_status"] == "source_variant_unresolved"
    assert data["unresolved_variant_count"] == 1


def test_c57_unresolved_threewind_tianshi_variant_is_preserved():
    data = ten_essence_cloud_conjunctions(
        "三风",
        conjunctions=["天时"],
    )
    item = data["matched_omens"][0]
    assert item["effects"] is None
    assert item["witness_variants"] == {
        "tongzong": "小阴雨",
        "wujing_zongyao": "小阴风",
    }


def test_c57_fivewind_direct_pairwise_rules():
    data = ten_essence_cloud_conjunctions(
        "五风",
        conjunctions=["太尊", "飞鸟", "帝符", "天时", "天目"],
    )
    targets = {item["target"]: item["effects"] for item in data["matched_omens"]}
    assert targets["太尊"] == ["小阴雨", "日月有变"]
    assert targets["飞鸟"] == ["疾风"]
    assert targets["帝符"] == ["大风"]
    assert targets["天时"] == ["大风"]
    assert targets["天目"] == ["大阴", "小风", "日月有变"]


def test_c57_threewind_pairwise_rules():
    data = ten_essence_cloud_conjunctions(
        "三风",
        conjunctions=["天目", "飞鸟", "五风", "太尊", "帝符", "天皇"],
    )
    targets = {item["target"]: item["effects"] for item in data["matched_omens"]}
    assert targets["天目"] == ["大阴雨"]
    assert targets["飞鸟"] == ["疾风阴云", "日月有变"]
    assert targets["五风"] == ["日月有变", "小阴"]
    assert targets["太尊"] == ["小阴雨"]
    assert targets["帝符"] == ["小阴"]
    assert targets["天皇"] == ["天阴", "小风", "日月有变"]


def test_c57_zhangliang_summary_variant_is_not_applied():
    assert ZHANGLIANG_SUMMARY_VARIANT["canonical_selected"] is None
    assert ZHANGLIANG_SUMMARY_VARIANT["runtime_applied"] is False
    data = ten_essence_cloud_conjunctions(
        "五风",
        conjunctions=["太乙"],
        taiyi_qi_state="非旺相",
        taiyi_palace_yinyang="阳",
    )
    assert data["matched_omens"] == []
    assert data["zhangliang_summary_variant"]["runtime_applied"] is False


def test_c57_cloud_color_and_texture_layers_are_deferred():
    assert DEFERRED_OBSERVATION_LAYERS == {
        "initial_move_cloud_color_timing": "deferred",
        "weather_texture_and_color": "deferred",
        "drought_rain_yin_yang_selection": "deferred",
        "wangxiang_speed_modifier": "deferred",
    }


def test_c57_does_not_accept_taiyi_number_as_position_essence():
    with pytest.raises(ValueError, match="number-omen"):
        ten_essence_cloud_conjunctions(
            "太乙数",
            conjunctions=["太乙"],
        )


def test_c57_rejects_legacy_difu_name_and_unknown_target():
    with pytest.raises(ValueError, match="canonical"):
        ten_essence_cloud_conjunctions(
            "地符",
            conjunctions=["太乙"],
        )
    with pytest.raises(ValueError, match="未知C57合会对象"):
        ten_essence_cloud_conjunctions(
            "帝符",
            conjunctions=["太阳"],
        )


def test_c57_catalog_keeps_layers_separate():
    data = c57_catalog()
    assert "帝符" in data["implemented_essences"]
    assert "五风" in data["implemented_essences"]
    assert data["auto_position_lookup_used"] is False
    assert data["zhangliang_summary_variant"]["canonical_selected"] is None
    assert PALACE_RULES["太尊"][8]["effects"] == ["日晕"]
    assert CONJUNCTION_RULES["八风"][0]["target"] == "太乙"
