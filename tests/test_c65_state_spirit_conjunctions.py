import pytest

from kintaiyi.state_spirit_conjunctions import (
    PAIR_RULES,
    POSITION_BOUNDARY,
    c65_catalog,
    canonical_entity_name,
    same_palace_omen,
)


@pytest.mark.parametrize(
    "pair",
    [
        ("天乙", "地乙"),
        ("天乙", "直符"),
        ("天乙", "四神"),
        ("天乙", "大游"),
        ("天乙", "小游"),
        ("地乙", "直符"),
        ("地乙", "四神"),
        ("地乙", "大游"),
        ("地乙", "小游"),
        ("直符", "四神"),
        ("直符", "大游"),
        ("直符", "小游"),
    ],
)
def test_c65_all_direct_pairs_match_only_when_explicit_same_palace(pair):
    data = same_palace_omen(*pair, same_palace=True)
    assert data["direct_rule_available"] is True
    assert data["status"] == "explicit_same_palace_rule_matched"
    assert len(data["matched_omens"]) == 1
    assert data["matched_omens"][0]["effects"] == PAIR_RULES[data["pair"][0], data["pair"][1]]["effects"]


def test_c65_pair_order_is_symmetric_but_source_rule_is_single():
    forward = same_palace_omen("天乙", "直符", same_palace=True)
    reverse = same_palace_omen("直符", "天乙", same_palace=True)
    assert forward["pair"] == reverse["pair"] == ["天乙", "直符"]
    assert forward["matched_omens"] == reverse["matched_omens"]
    assert forward["matched_omens"][0]["source_section"] == "明天乙太乙金神所主术"


def test_c65_missing_same_palace_evidence_stays_pending():
    data = same_palace_omen("地乙", "四神", same_palace=None)
    assert data["matched_omens"] == []
    assert data["status"] == "same_palace_unchecked"
    assert "不从C64自动判断" in "；".join(data["pending"])


def test_c65_explicit_not_same_palace_has_no_omen():
    data = same_palace_omen("天乙", "地乙", same_palace=False)
    assert data["matched_omens"] == []
    assert data["status"] == "not_same_palace"


def test_c65_unknown_direct_pair_is_not_invented():
    data = same_palace_omen("四神", "大游", same_palace=True)
    assert data["direct_rule_available"] is False
    assert data["matched_omens"] == []
    assert data["status"] == "same_palace_no_direct_c65_rule"


def test_c65_tianyi_diyi_core_effects():
    data = same_palace_omen("天乙", "地乙", same_palace=True)
    effects = data["matched_omens"][0]["effects"]
    assert "兵戈发" in effects
    assert "土工兴废" in effects
    assert "农桑有伤" in effects
    assert "人民愁困" in effects


def test_c65_diyi_zhifu_core_effects():
    data = same_palace_omen("地乙", "直符", same_palace=True)
    assert data["matched_omens"][0]["effects"] == [
        "火旱", "兵盗", "土工大兴", "人民灾疾", "五谷不成"
    ]


def test_c65_zhifu_four_spirits_core_effects():
    data = same_palace_omen("直符", "四神", same_palace=True)
    effects = data["matched_omens"][0]["effects"]
    assert "水旱不调" in effects
    assert "四序失节" in effects
    assert "水火刀兵之厄" in effects


def test_c65_source_name_variants_are_controlled():
    assert canonical_entity_name("大遊") == "大游"
    assert canonical_entity_name("太游") == "大游"
    assert canonical_entity_name("四神水宿") == "四神"

    with pytest.raises(ValueError, match="值符不是C65 canonical"):
        canonical_entity_name("值符")

    assert canonical_entity_name(
        "值符",
        allow_legacy_zhifu_alias=True,
    ) == "直符"


def test_c65_legacy_zhifu_alias_requires_explicit_mode_in_runtime():
    with pytest.raises(ValueError, match="值符不是C65 canonical"):
        same_palace_omen("值符", "四神", same_palace=True)

    data = same_palace_omen(
        "值符",
        "四神",
        same_palace=True,
        allow_legacy_zhifu_alias=True,
    )
    assert data["first"] == "直符"
    assert data["matched_omens"][0]["pair"] == ["直符", "四神"]


def test_c65_rejects_same_entity_and_bad_same_palace_type():
    with pytest.raises(ValueError, match="两个不同对象"):
        same_palace_omen("天乙", "天乙", same_palace=True)
    with pytest.raises(TypeError, match="bool或None"):
        same_palace_omen("天乙", "地乙", same_palace="同宫")


def test_c65_never_auto_reads_c64_positions():
    data = same_palace_omen("天乙", "小游", same_palace=True)
    assert data["position_boundary"] == POSITION_BOUNDARY
    assert data["position_boundary"]["auto_position_lookup_used"] is False
    assert data["position_boundary"]["auto_same_palace_inference_used"] is False


def test_c65_catalog_is_explicit_relation_layer():
    data = c65_catalog()
    assert data["rule_id"] == "C65-THREE-SPIRIT-SAME-PALACE"
    assert len(data["pair_rules"]) == 12
    assert data["position_boundary"]["position_runtime"] == "C64"
    assert data["position_boundary"]["auto_same_palace_inference_used"] is False
