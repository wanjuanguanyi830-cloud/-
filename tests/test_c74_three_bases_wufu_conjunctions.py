import pytest

from kintaiyi.three_bases_wufu_conjunctions import (
    PAIR_RULES,
    POSITION_BOUNDARY,
    c74_catalog,
    same_palace_relation,
)


@pytest.mark.parametrize("pair", list(PAIR_RULES))
def test_c74_all_six_pairs_require_explicit_same_palace(pair):
    data = same_palace_relation(*pair, same_palace=True)
    assert data["status"] == "explicit_same_palace_rule_matched"
    assert data["applied_effects"]


def test_c74_pair_order_is_symmetric_but_source_layers_are_not_flattened():
    forward = same_palace_relation(
        "君基", "五福", same_palace=True, initial_conjunction=False
    )
    reverse = same_palace_relation(
        "五福", "君基", same_palace=True, initial_conjunction=False
    )
    assert forward["pair"] == reverse["pair"] == ["君基", "五福"]
    assert forward["applied_effects"] == reverse["applied_effects"]
    assert [row["layer"] for row in forward["applied_effects"]] == [
        "base_section", "wufu_section"
    ]


def test_c74_junji_wufu_preserves_both_sections_and_separate_initial_clause():
    data = same_palace_relation(
        "君基", "五福", same_palace=True, initial_conjunction=True
    )
    layers = {row["layer"]: row["effects"] for row in data["applied_effects"]}
    assert "皇室巩固" in layers["base_section"]
    assert "人君福寿祚享" in layers["wufu_section"]
    assert layers["wufu_initial_conjunction"] == ["合生后储太子"]
    assert data["adjacent_non_same_palace_clause"]["relation"] == "五福与君基相冲"
    assert data["adjacent_non_same_palace_clause"]["applied_in_c74"] is False


def test_c74_chenji_wufu_keeps_initial_conjunction_conditional():
    pending = same_palace_relation("臣基", "五福", same_palace=True)
    assert "initial_conjunction" in "；".join(pending["pending"])
    assert all(
        row["layer"] != "wufu_initial_conjunction"
        for row in pending["applied_effects"]
    )

    checked = same_palace_relation(
        "臣基", "五福", same_palace=True, initial_conjunction=True
    )
    layers = {row["layer"]: row["effects"] for row in checked["applied_effects"]}
    assert "利为宰辅" in layers["base_section"]
    assert layers["wufu_section"] == ["福利辅宰"]
    assert layers["wufu_initial_conjunction"] == ["贤相当生贵人之家"]


def test_c74_minji_wufu_preserves_two_source_sections():
    data = same_palace_relation(
        "民基", "五福", same_palace=True, initial_conjunction=True
    )
    layers = {row["layer"]: row["effects"] for row in data["applied_effects"]}
    assert layers["base_section"] == ["其民富寿", "贤福之人生于民家"]
    assert layers["wufu_section"] == ["四民乐业", "天下熙和"]
    assert layers["wufu_initial_conjunction"] == ["其分富贵人生于白屋之家"]


def test_c74_three_base_pairs_do_not_accept_wufu_initial_flag():
    with pytest.raises(ValueError, match="仅用于含五福"):
        same_palace_relation(
            "君基", "臣基", same_palace=True, initial_conjunction=True
        )


def test_c74_missing_same_palace_evidence_stays_pending():
    data = same_palace_relation("君基", "臣基", same_palace=None)
    assert data["applied_effects"] == []
    assert data["status"] == "same_palace_unchecked"
    assert "不从C66/C67自动判断" in "；".join(data["pending"])


def test_c74_explicit_not_same_palace_has_no_effects():
    data = same_palace_relation("臣基", "民基", same_palace=False)
    assert data["applied_effects"] == []
    assert data["status"] == "not_same_palace"


def test_c74_rejects_logically_inconsistent_initial_conjunction_flags():
    with pytest.raises(ValueError, match="不同宫"):
        same_palace_relation(
            "君基", "五福", same_palace=False, initial_conjunction=True
        )
    with pytest.raises(ValueError, match="未确认同宫"):
        same_palace_relation(
            "君基", "五福", same_palace=None, initial_conjunction=False
        )


def test_c74_rejects_bad_entities_same_entity_and_types():
    with pytest.raises(ValueError, match="君基/臣基/民基/五福"):
        same_palace_relation("天乙", "五福", same_palace=True)
    with pytest.raises(ValueError, match="两个不同对象"):
        same_palace_relation("君基", "君基", same_palace=True)
    with pytest.raises(TypeError, match="same_palace"):
        same_palace_relation("君基", "臣基", same_palace="同宫")
    with pytest.raises(TypeError, match="initial_conjunction"):
        same_palace_relation(
            "君基", "五福", same_palace=True, initial_conjunction="初交"
        )


def test_c74_never_auto_reads_c66_or_c67():
    data = same_palace_relation(
        "民基", "五福", same_palace=True, initial_conjunction=False
    )
    assert data["position_boundary"] == POSITION_BOUNDARY
    assert data["position_boundary"]["auto_position_lookup_used"] is False
    assert data["position_boundary"]["auto_same_palace_inference_used"] is False


def test_c74_catalog_is_six_pair_relation_layer():
    data = c74_catalog()
    assert data["rule_id"] == "C74-THREE-BASES-WUFU-SAME-PALACE"
    assert len(data["pair_rules"]) == 6
    assert data["entities"] == ["君基", "臣基", "民基", "五福"]
    assert data["position_boundary"]["three_bases_position_runtime"] == "C66"
    assert data["position_boundary"]["wufu_position_runtime"] == "C67"
