import pytest

from kintaiyi.cross_volume_helpers import (
    build_guxu_cross_volume_helper,
    c32_catalog,
)
from kintaiyi.eight_divinations import attack_realm
from kintaiyi.tongzong_v17_structured import request_outcome


def test_c32_requires_exact_source_rule_ids():
    with pytest.raises(ValueError):
        build_guxu_cross_volume_helper(
            attack_result={"rule_id": "D8-06", "realm": "内"},
            request_result={"source_rule_id": "V17-09", "inputs": {"skyeyes_realm": "内"}},
        )
    with pytest.raises(ValueError):
        build_guxu_cross_volume_helper(
            attack_result={"rule_id": "D8-05", "realm": "内"},
            request_result={"source_rule_id": "V17-08", "inputs": {"skyeyes_realm": "内"}},
        )


def test_c32_inner_realm_base_alignment():
    attack = {"rule_id": "D8-05", "realm": "内", "verdict": "内虚、宜攻外"}
    request = request_outcome(skyeyes_realm="内")
    data = build_guxu_cross_volume_helper(
        attack_result=attack,
        request_result=request,
    )
    assert data["source_status"] == "derived_cross_volume_helper"
    assert data["canonical_source_rule"] is False
    assert data["guxu"] == "内为虚"
    assert data["attack_direction"] == "外"
    assert data["alignment"] == "base_aligned"


def test_c32_outer_realm_base_alignment():
    attack = {"rule_id": "D8-05", "realm": "外", "verdict": "外孤、宜攻内"}
    request = request_outcome(skyeyes_realm="外")
    data = build_guxu_cross_volume_helper(
        attack_result=attack,
        request_result=request,
    )
    assert data["guxu"] == "外为孤"
    assert data["attack_direction"] == "内"
    assert data["request_summary"] == "negative"
    assert data["alignment"] == "base_aligned"


def test_c32_preserves_v17_mixed_evidence():
    attack = {"rule_id": "D8-05", "realm": "内", "verdict": "内虚、宜攻外"}
    request = request_outcome(
        skyeyes_realm="内",
        host_clamps_guest=True,
    )
    assert request["summary"] == "mixed_evidence"
    data = build_guxu_cross_volume_helper(
        attack_result=attack,
        request_result=request,
    )
    assert data["alignment"] == "request_modified_by_other_conditions"
    assert data["sources"]["volume17"]["result"]["summary"] == "mixed_evidence"


def test_c32_detects_realm_input_conflict_without_recomputing():
    attack = {"rule_id": "D8-05", "realm": "内", "verdict": "内虚、宜攻外"}
    request = request_outcome(skyeyes_realm="外")
    data = build_guxu_cross_volume_helper(
        attack_result=attack,
        request_result=request,
    )
    assert data["realm_consistent"] is False
    assert data["alignment"] == "input_conflict"


def test_c32_does_not_mutate_source_results():
    attack = {"rule_id": "D8-05", "realm": "内", "verdict": "内虚、宜攻外"}
    request = request_outcome(skyeyes_realm="内")
    attack_before = dict(attack)
    request_before = dict(request)

    data = build_guxu_cross_volume_helper(
        attack_result=attack,
        request_result=request,
    )
    data["sources"]["volume5_or_d8"]["result"]["realm"] = "外"

    assert attack == attack_before
    assert request == request_before


def test_c32_catalog_has_no_canonical_source_rules():
    data = c32_catalog()
    assert data["helpers"] == ["V17-D1"]
    assert data["source_status"] == "derived_cross_volume_helper"
    assert data["canonical_source_rule_count"] == 0
