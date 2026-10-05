import pytest

from kintaiyi.jinjing_taigong_timing import (
    C117_VERSION,
    c117_catalog,
    evaluate_taigong_timing,
)


def favorable_case(**updates):
    data = dict(
        right_taiyi_left_tianmu=True,
        yinyang_harmonious=True,
        blocking_patterns=[],
        taiyi_in_yang_jue=False,
        spirits_independent=True,
        door="开",
        door_has_malefic_spirit=False,
        three_doors_complete=True,
        five_generals_active=True,
        role="天子",
        occupied_xuanming_target="天乙",
        xuanming_in_wangxiang=True,
        upper_lower_generating=True,
        direct_envoy_clause_matched=True,
    )
    data.update(updates)
    return evaluate_taigong_timing(**data)


def test_c117_complete_explicit_favorable_chain():
    data = favorable_case()
    assert data["canonical"] == C117_VERSION
    assert data["military_action_favorable"] is True
    assert data["xuanming_harmony"] is True
    assert data["greatly_auspicious"] is True
    assert data["pending"] == []


@pytest.mark.parametrize("door", ["开", "休", "生"])
def test_c117_only_three_auspicious_doors_form_jidao(door):
    assert favorable_case(door=door)["base_checks"]["auspicious_route"] is True


@pytest.mark.parametrize("door", ["伤", "杜", "景", "死", "惊"])
def test_c117_other_doors_are_not_jidao(door):
    data = favorable_case(door=door)
    assert data["base_checks"]["auspicious_route"] is False
    assert data["military_action_favorable"] is False
    assert data["greatly_auspicious"] is False


def test_c117_blocking_pattern_prevents_favorable_military_action():
    data = favorable_case(blocking_patterns=["击", "提挟"])
    assert data["base_checks"]["blocking_patterns_clear"] is False
    assert data["military_action_favorable"] is False


def test_c117_qingxu_requires_no_malefic_spirit_at_door():
    data = favorable_case(door_has_malefic_spirit=True)
    assert data["base_checks"]["route_clear_of_malefic_spirit"] is False
    assert data["military_action_favorable"] is False


def test_c117_xuanming_harmony_uses_c116_role_mapping():
    data = favorable_case(
        role="皇后",
        occupied_xuanming_target="天后",
    )
    assert data["xuanming"]["xuanming_target"] == "天后"
    assert data["xuanming_harmony"] is True

    mismatch = favorable_case(
        role="皇后",
        occupied_xuanming_target="天乙",
    )
    assert mismatch["xuanming_harmony"] is False
    assert mismatch["greatly_auspicious"] is False


def test_c117_direct_envoy_clause_stays_explicit_and_pending():
    data = favorable_case(direct_envoy_clause_matched=None)
    assert data["military_action_favorable"] is True
    assert data["xuanming_harmony"] is True
    assert data["greatly_auspicious"] is None
    assert any("前三五" in item for item in data["pending"])


def test_c117_missing_evidence_does_not_become_false_or_true():
    data = evaluate_taigong_timing(
        right_taiyi_left_tianmu=None,
        yinyang_harmonious=None,
        blocking_patterns=None,
        taiyi_in_yang_jue=None,
        spirits_independent=None,
        door=None,
        door_has_malefic_spirit=None,
        three_doors_complete=None,
        five_generals_active=None,
    )
    assert data["military_action_favorable"] is None
    assert data["xuanming_harmony"] is None
    assert data["greatly_auspicious"] is None
    assert data["pending"]


def test_c117_catalog_never_claims_automatic_rule_lookups():
    catalog = c117_catalog()
    assert catalog["auto_rule_lookups"] is False
    assert catalog["auspicious_doors"] == ["休", "开", "生"]
    assert catalog["direct_envoy_boundary"]["auto_computation"] is False


def test_c117_rejects_xuanming_details_without_role():
    with pytest.raises(ValueError):
        favorable_case(role=None, occupied_xuanming_target="天乙")
