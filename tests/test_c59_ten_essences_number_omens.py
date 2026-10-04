import pytest

from kintaiyi.ten_essences_number import taiyi_number
from kintaiyi.ten_essences_number_omens import (
    LEGACY_SPECIAL_AUDIT,
    RELATION_RULES,
    SPECIAL_NUMBER_RULES,
    c59_catalog,
    taiyi_number_omens,
)


def _effects(data):
    return [item["effects"] for item in data["matched_omens"]]


def test_c59_number_30_and_40_are_stable_direct_rules():
    thirty = taiyi_number_omens(30, relations=[])
    assert thirty["matched_omens"] == [{
        "kind": "special_number",
        "taiyi_number": 30,
        "effects": ["日晕", "大风"],
        "source_status": "direct_parallel",
    }]

    forty = taiyi_number_omens(40, relations=[])
    assert forty["matched_omens"][0]["effects"] == ["阴雨", "黄雾"]


def test_c59_number_50_stays_unresolved_across_witness_segmentation():
    data = taiyi_number_omens(50, relations=[])
    assert data["matched_omens"] == []
    assert data["unresolved_variant_count"] == 1
    variant = data["unresolved_variants"][0]
    assert variant["taiyi_number"] == 50
    assert variant["canonical_selected"] is None
    assert "日晕、大风" in variant["witness_variants"]["wujing_zongyao"]
    assert "天目" in variant["witness_variants"]["jinjing"]
    assert data["status"] == "explicit_evidence_with_unresolved_variants"


def test_c59_legacy_number_10_and_5_are_not_standalone_canonical_rules():
    ten = taiyi_number_omens(10, relations=[])
    five = taiyi_number_omens(5, relations=[])
    assert ten["matched_omens"] == []
    assert five["matched_omens"] == []
    assert LEGACY_SPECIAL_AUDIT[10]["direct_special_number_rule"] is False
    assert LEGACY_SPECIAL_AUDIT[5]["direct_special_number_rule"] is False
    assert "未见“数得十”" in LEGACY_SPECIAL_AUDIT[10]["reason"]


def test_c59_legacy_50_does_not_steal_yellow_fog_from_number_40():
    assert SPECIAL_NUMBER_RULES[40]["effects"] == ["阴雨", "黄雾"]
    assert SPECIAL_NUMBER_RULES[50]["effects"] is None
    assert "黄雾属于数40" in LEGACY_SPECIAL_AUDIT[50]["reason"]


def test_c59_taiyi_join_and_opposition_are_explicit_relations():
    joined = taiyi_number_omens(17, relations=["合太乙"])
    opposed = taiyi_number_omens(17, relations=["冲太乙"])
    assert joined["matched_omens"][0]["effects"] == ["日晕", "大风"]
    assert opposed["matched_omens"][0]["effects"] == ["日晕", "风起"]
    assert joined["auto_relation_inference_used"] is False


def test_c59_tianmu_join_requires_explicit_wangxiang():
    missing = taiyi_number_omens(17, relations=["合天目"])
    assert missing["matched_omens"] == []
    assert "tianmu_qi_state" in "；".join(missing["pending"])

    weak = taiyi_number_omens(
        17,
        relations=["合天目"],
        tianmu_qi_state="休囚",
    )
    assert weak["matched_omens"] == []

    hit = taiyi_number_omens(
        17,
        relations=["合天目"],
        tianmu_qi_state="旺相",
    )
    assert hit["matched_omens"][0]["effects"] == ["日晕"]


def test_c59_number_50_plus_explicit_tianmu_wangxiang_keeps_both_layers():
    data = taiyi_number_omens(
        50,
        relations=["合天目"],
        tianmu_qi_state="旺相",
    )
    assert ["日晕"] in _effects(data)
    assert data["unresolved_variant_count"] == 1
    assert data["status"] == "explicit_evidence_with_unresolved_variants"


def test_c59_taiyi_clamps_tianmu_is_direct_cumulative_omen():
    data = taiyi_number_omens(17, relations=["太乙挟天目"])
    assert data["matched_omens"][0]["effects"] == ["阴雨", "日晕", "大风"]


@pytest.mark.parametrize("palace", [6, 8, 9])
def test_c59_flybird_join_requires_6_8_9_palace(palace):
    data = taiyi_number_omens(
        17,
        relations=["合飞鸟"],
        flybird_palace=palace,
    )
    assert data["matched_omens"][0]["effects"] == ["日晕"]


def test_c59_flybird_join_missing_or_other_palace_does_not_guess():
    missing = taiyi_number_omens(17, relations=["合飞鸟"])
    assert missing["matched_omens"] == []
    assert "flybird_palace" in "；".join(missing["pending"])

    other = taiyi_number_omens(
        17,
        relations=["合飞鸟"],
        flybird_palace=5,
    )
    assert other["matched_omens"] == []


def test_c59_heaven_earth_and_taiyi_flybird_relations_are_separate():
    data = taiyi_number_omens(
        17,
        relations=["与天地并", "与天地相当", "合太乙飞鸟"],
    )
    effects = _effects(data)
    assert ["日晕"] in effects
    assert ["大风"] in effects
    assert ["疾风"] in effects


def test_c59_main_calculation_rule_requires_10_9_and_preserves_main_8_detail():
    missing = taiyi_number_omens(
        17,
        relations=["合主计"],
        heaven_calculation=10,
        earth_calculation=9,
    )
    assert missing["matched_omens"] == []
    assert "main_calculation" in "；".join(missing["pending"])

    exact = taiyi_number_omens(
        17,
        relations=["合主计"],
        heaven_calculation=10,
        earth_calculation=9,
        main_calculation=8,
    )
    item = exact["matched_omens"][0]
    assert item["effects"] == ["日晕"]
    assert item["witness_variants"] == RELATION_RULES["合主计"]["witness_variants"]

    variant = taiyi_number_omens(
        17,
        relations=["合主计"],
        heaven_calculation=10,
        earth_calculation=9,
        main_calculation=7,
    )
    assert variant["matched_omens"] == []
    assert variant["unresolved_variant_count"] == 1
    assert variant["unresolved_variants"][0]["canonical_selected"] is None


def test_c59_relations_none_is_distinct_from_explicit_empty():
    unknown = taiyi_number_omens(17)
    assert unknown["relations_checked"] is False
    assert "显式传空list" in "；".join(unknown["pending"])

    empty = taiyi_number_omens(17, relations=[])
    assert empty["relations_checked"] is True
    assert empty["pending"] == []
    assert empty["status"] == "explicit_evidence_complete"


def test_c59_c54_number_can_be_passed_explicitly_without_auto_lookup():
    numeric = taiyi_number(390)
    assert numeric["taiyi_number"] == 30

    data = taiyi_number_omens(numeric["taiyi_number"], relations=[])
    assert data["taiyi_number"] == 30
    assert data["auto_number_lookup_used"] is False
    assert data["matched_omens"][0]["effects"] == ["日晕", "大风"]


@pytest.mark.parametrize("bad", [0, 73, -1])
def test_c59_rejects_number_outside_1_72(bad):
    with pytest.raises(ValueError, match="1..72"):
        taiyi_number_omens(bad, relations=[])


def test_c59_rejects_bool_number_unknown_relation_and_bad_context():
    with pytest.raises(TypeError):
        taiyi_number_omens(True, relations=[])
    with pytest.raises(ValueError, match="未知C59关系"):
        taiyi_number_omens(17, relations=["合太阳"])
    with pytest.raises(ValueError, match="1..9"):
        taiyi_number_omens(17, relations=[], flybird_palace=10)
    with pytest.raises(ValueError, match="旺相"):
        taiyi_number_omens(17, relations=[], tianmu_qi_state="强")


def test_c59_catalog_keeps_number_and_relation_layers_explicit():
    data = c59_catalog()
    assert data["rule_id"] == "C59-TAIYI-NUMBER-OMEN"
    assert data["special_number_rules"][30]["effects"] == ["日晕", "大风"]
    assert data["special_number_rules"][50]["canonical_selected"] is None
    assert data["auto_number_lookup_used"] is False
    assert data["auto_relation_inference_used"] is False
