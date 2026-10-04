import pytest

from kintaiyi.ten_essences_registry import (
    CLOUD_LAYER_BOUNDARY,
    FOCUS_FIELDS,
    SOURCE_RULES,
    SOURCE_WITNESS,
    TEN_ESSENCE_ORDER,
    ten_essence_focus,
    ten_essence_source_registry,
)


def test_c52_ten_essence_order_and_focus_fields():
    assert TEN_ESSENCE_ORDER == (
        "天皇", "帝符", "天时", "太尊", "飞鸟",
        "五行", "八风", "五风", "三风", "太乙数",
    )
    assert FOCUS_FIELDS == ("帝符", "太尊", "飞鸟", "三风", "五风", "八风")


def test_c52_records_volume_witness_variant():
    assert SOURCE_WITNESS["volume_witnesses"] == {
        "cadal_online": 20,
        "ngj_or_project_legacy": 18,
    }
    assert SOURCE_WITNESS["volume_status"] == "witness_volume_variant"


def test_c52_position_and_cloud_layers_are_separate():
    assert CLOUD_LAYER_BOUNDARY["same_source_family"] is True
    assert CLOUD_LAYER_BOUNDARY["same_formula_layer"] is False
    assert CLOUD_LAYER_BOUNDARY["position_layer"] == "明十精太乙所至"
    assert CLOUD_LAYER_BOUNDARY["cloud_layer"] == "明十精太乙云气所主术"


def test_c52_difu_direct_structure_and_rejected_surplus():
    rule = SOURCE_RULES["帝符"]
    assert rule["big_cycle"] == 200
    assert rule["small_cycle"] == 20
    assert rule["route"]["start"] == "阴主"
    assert rule["route"]["status"] == "direct_complete_structure"
    assert rule["route"]["repeat_on"] == [
        "地主", "高丛", "大威", "太簇", "坎", "离", "震", "兑"
    ]
    assert rule["rejected_surplus_formula"]["value"] == 70
    assert rule["rejected_surplus_formula"]["apply"] is False
    assert rule["legacy_canonical_equivalent"] is False
    assert rule["legacy_aliases"] == ["地符"]


def test_c52_taizun_stays_pending_route_collation():
    rule = SOURCE_RULES["太尊"]
    assert rule["big_cycle"] == 40
    assert rule["small_cycle"] == 4
    assert rule["route"]["status"] == "text_requires_collation"
    assert rule["route"]["canonical_route"] is None
    assert rule["legacy_canonical_equivalent"] is False


def test_c52_flying_bird_is_ten_essence_not_j4m_observation():
    rule = SOURCE_RULES["飞鸟"]
    assert rule["big_cycle"] == 90
    assert rule["small_cycle"] == 9
    assert rule["legacy_function"] == "config.flybird"
    assert rule["legacy_canonical_equivalent"] is False
    assert rule["same_name_boundary"]["j4m11_external_bird_observation"] is False
    assert "不得用十精宫位伪造军事飞鸟观测" in rule["same_name_boundary"]["policy"]


def test_c52_fivewind_has_complete_direct_sequence_and_legacy_period_conflict():
    rule = SOURCE_RULES["五风"]
    assert rule["big_cycle"] == 90
    assert rule["small_cycle"] == 9
    assert rule["route"]["sequence"] == [1, 3, 5, 7, 9, 2, 4, 6, 8]
    assert rule["route"]["mode"] == "先阳后阴次第"
    assert rule["route"]["status"] == "direct_complete_sequence"
    assert rule["legacy_canonical_equivalent"] is False
    assert "mod29" in rule["legacy_issue"]


def test_c52_eightwind_keeps_route_expansion_pending():
    rule = SOURCE_RULES["八风"]
    assert rule["big_cycle"] == 90
    assert rule["small_cycle"] == 9
    assert "大威二宫" in rule["route"]["source_text"]
    assert rule["route"]["canonical_route"] is None
    assert rule["rejected_surplus_formula"]["apply"] is False


def test_c52_threewind_does_not_invent_missing_ninth_route_item():
    rule = SOURCE_RULES["三风"]
    assert rule["big_cycle"] == 90
    assert rule["small_cycle"] == 9
    assert rule["route"]["source_sequence"] == [3, 7, 2, 6, 1, 5, 4, 8]
    assert len(rule["route"]["source_sequence"]) == 8
    assert rule["route"]["canonical_route"] is None
    assert "不得自行补第九项" in rule["route"]["note"]


@pytest.mark.parametrize("name", FOCUS_FIELDS)
def test_c52_focus_lookup_returns_registered_rule(name):
    data = ten_essence_focus(name)
    assert data["name"] == name
    assert data["rule"] == SOURCE_RULES[name]
    assert data["cloud_layer_boundary"]["same_formula_layer"] is False


def test_c52_focus_rejects_non_focus_ten_essence():
    with pytest.raises(ValueError, match="只开放"):
        ten_essence_focus("天皇")


def test_c52_registry_never_applies_runtime_formula():
    data = ten_essence_source_registry()
    assert data["runtime_formula_applied"] is False
    assert data["rules"]["帝符"]["legacy_canonical_equivalent"] is False
    assert data["rules"]["五风"]["route"]["status"] == "direct_complete_sequence"
