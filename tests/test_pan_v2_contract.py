import pytest

from kintaiyi.pan_v2_contract import (
    CONTRACT_VERSION,
    build_analysis_contract,
    build_modern_contract,
    build_source_variants_contract,
    build_structured_pan_v2,
    validate_structured_pan_v2,
)


def test_analysis_contract_has_fixed_four_sections():
    data = build_analysis_contract(
        patterns={"canonical": "jinjing"},
        eight_divinations={"home": {"rule_id": "D8-01"}},
        seven_methods={"tiger": {"rule_id": "T7-04"}},
        military={"canonical": "taiyi-c8-v1", "source_profile": "volume5_strict"},
    )
    assert set(data) == {"patterns", "eight_divinations", "seven_methods", "military"}


def test_analysis_rejects_legacy_flat_keys():
    with pytest.raises(ValueError):
        build_analysis_contract(military={"軍事戰略": {"legacy": True}})


def test_analysis_rejects_derived_volume_profile():
    with pytest.raises(ValueError):
        build_analysis_contract(
            military={"derived_military_profile": True, "profile": "tongzong_volume17"}
        )


def test_source_variants_use_fixed_slots_without_merging():
    data = build_source_variants_contract(
        patterns={"profiles": {"jinjing_geju": {"x": 1}}},
        zitingjing={"rules": {"taiyi_nine_stars": {"primary_ready": True}}},
        military_derived={"tongzong_volume17": {"payload": {"敵使虛實": {"x": 1}}}},
    )
    assert set(data) == {"patterns", "zitingjing", "military_derived"}
    assert data["patterns"]["profiles"]["jinjing_geju"] == {"x": 1}
    assert data["zitingjing"]["rules"]["taiyi_nine_stars"]["primary_ready"] is True


def test_modern_game_theory_requires_derived_marker():
    with pytest.raises(ValueError):
        build_modern_contract(game_theory={"score": 1})

    data = build_modern_contract(
        game_theory={"derived_modern_feature": True, "score": 1}
    )
    assert data["game_theory"]["score"] == 1


def test_full_structured_pan_uses_expected_root_slots():
    payload = build_structured_pan_v2(
        board={"taiyi": {"palace": 1, "sector": "乾"}},
        military={"canonical": "taiyi-c8-v1", "source_profile": "volume5_strict"},
        modern_game_theory={
            "derived_modern_feature": True,
            "source_of_truth": "structured_taiyi_results",
        },
        zitingjing_variants={
            "primary_source": "zitingjing",
            "primary_source_title": "太乙紫庭经",
        },
        military_derived_variants={
            "tongzong_volume17": {
                "derived_military_profile": True,
                "payload": {"見聞虛實": {"source_rule_id": "V17-06"}},
            }
        },
    )
    assert payload["meta"]["aggregation_contract"] == CONTRACT_VERSION
    assert payload["analysis"]["military"]["canonical"] == "taiyi-c8-v1"
    assert payload["modern"]["game_theory"]["derived_modern_feature"] is True
    assert payload["source_variants"]["zitingjing"]["primary_source"] == "zitingjing"
    assert payload["source_variants"]["military_derived"]["tongzong_volume17"]["derived_military_profile"] is True


def test_center_five_invariant_still_applies_through_contract():
    payload = build_structured_pan_v2(
        board={"taiyi": {"palace": 5, "sector": "中"}},
    )
    assert payload["board"]["taiyi"]["sector"] is None


def test_contract_validator_accepts_contract_builder_output():
    payload = build_structured_pan_v2(
        modern_game_theory={"derived_modern_feature": True},
    )
    checked = validate_structured_pan_v2(payload)
    assert checked["valid"] is True
    assert checked["aggregation_contract"] == CONTRACT_VERSION


def test_contract_validator_catches_unknown_source_variant_root():
    payload = build_structured_pan_v2()
    payload["source_variants"]["random_bucket"] = {"x": 1}
    checked = validate_structured_pan_v2(payload)
    assert checked["valid"] is False
    assert any("未知source_variants根槽" in item for item in checked["errors"])


def test_contract_validator_catches_modern_marker_regression():
    payload = build_structured_pan_v2(
        modern_game_theory={"derived_modern_feature": True},
    )
    payload["modern"]["game_theory"]["derived_modern_feature"] = False
    checked = validate_structured_pan_v2(payload)
    assert checked["valid"] is False
    assert "modern.game_theory缺derived_modern_feature=True" in checked["errors"]


def test_contract_validator_warns_on_plain_c11_payload_without_contract_marker():
    from kintaiyi.pan_v2 import build_pan_v2

    payload = build_pan_v2()
    checked = validate_structured_pan_v2(payload)
    assert checked["valid"] is True
    assert "payload未标当前C30 aggregation_contract" in checked["warnings"]


def test_no_legacy_flat_analysis_reconstruction():
    payload = build_structured_pan_v2(
        compat={
            "legacy_top_level": True,
            "legacy_schema": "pan-v1-flat",
            "quarantined_legacy_keys": ["軍事戰略", "太乙九星"],
        },
    )
    assert payload["analysis"]["military"] == {}
    assert payload["source_variants"] == {}
    assert "軍事戰略" not in payload["analysis"]


def test_c37_wuyun_wuyin_is_allowed_as_dedicated_source_variant_slot():
    data = build_source_variants_contract(
        wuyun_wuyin={
            "wuyun_liuqi": {
                "profiles": {
                    "tongzong_volume3": {"rule_id": "C37-V3-WYUN"},
                    "tongzong_volume10": {"rule_id": "C37-V10-WYUN"},
                }
            }
        }
    )
    assert set(data) == {"wuyun_wuyin"}
    assert data["wuyun_wuyin"]["wuyun_liuqi"]["profiles"]["tongzong_volume3"]["rule_id"] == "C37-V3-WYUN"


def test_c37_wuyun_wuyin_can_flow_through_structured_pan_contract():
    payload = build_structured_pan_v2(
        wuyun_wuyin_variants={
            "wuyin_number": {
                "profiles": {
                    "tongzong_volume3": {"rule_id": "C37-V3-WYIN"}
                }
            }
        }
    )
    assert payload["source_variants"]["wuyun_wuyin"]["wuyin_number"]["profiles"]["tongzong_volume3"]["rule_id"] == "C37-V3-WYIN"
    assert validate_structured_pan_v2(payload)["valid"] is True


def test_c43_volume9_is_allowed_as_dedicated_source_variant_slot():
    data = build_source_variants_contract(
        volume9={
            "ehui_limit": {
                "legacy_replacement": {
                    "source_replacement_complete": True,
                    "rule_id": "C43-V9-EHUI",
                }
            }
        }
    )
    assert set(data) == {"volume9"}
    assert data["volume9"]["ehui_limit"]["legacy_replacement"]["rule_id"] == "C43-V9-EHUI"


def test_c43_volume9_can_flow_through_structured_pan_contract():
    payload = build_structured_pan_v2(
        volume9_variants={
            "ehui_limit": {
                "result": {"rule_id": "C43-V9-EHUI"},
            }
        }
    )
    assert payload["source_variants"]["volume9"]["ehui_limit"]["result"]["rule_id"] == "C43-V9-EHUI"
    assert validate_structured_pan_v2(payload)["valid"] is True
