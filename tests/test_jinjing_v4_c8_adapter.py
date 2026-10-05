from kintaiyi.jinjing_v4_c8_adapter import adapt_j4m_to_c8
from kintaiyi.jinjing_v4_military import (
    sanmen_jubu,
    wujiang_fabu,
    zhuke_fa,
)
from kintaiyi.junshi_zhanlue import junshi_zhanlue


def test_adapter_requires_explicit_jinjing_profile():
    data = adapt_j4m_to_c8(source_profile="volume5_strict")
    assert data["computable"] is False
    assert data["status"] == "rejected_source_profile"
    assert data["required_source_profile"] == "jinjing_siku_volume4"


def test_adapter_maps_j4m01_and_j4m02_only_as_c8_l2_facts():
    doors = sanmen_jubu(taiyi_gate="休", tianmu_gate="开")
    generals = wujiang_fabu(
        shiji_yanji=False,
        wenchang_qiupo=False,
        major_minor_generals_related=False,
        three_doors_ready=doors["three_doors_ready"],
    )

    data = adapt_j4m_to_c8(
        source_profile="jinjing_siku_volume4",
        three_doors_result=doors,
        five_generals_result=generals,
        home_cal=17,
        away_cal=13,
    )

    l2 = data["c8_result"]["layers"]["three_doors_five_generals"]
    assert l2["three_doors"]["ready"] is False
    assert l2["five_generals"]["released"] is True
    assert l2["joint_ready"] is False
    assert data["mapped_inputs"]["J4M-01.three_doors_ready -> C8-L2"] is False
    assert data["mapped_inputs"]["J4M-02.five_generals_released -> C8-L2"] is True


def test_adapter_preserves_j4m04_as_overlay_without_rewriting_c8_l3():
    doors = {
        "ruleset": "jinjing-siku-v4-military-12",
        "source_profile": "jinjing_siku_volume4",
        "rule_id": "J4M-01",
        "three_doors_ready": True,
    }
    generals = wujiang_fabu(
        shiji_yanji=False,
        wenchang_qiupo=False,
        major_minor_generals_related=False,
        three_doors_ready=True,
    )
    host_guest = zhuke_fa(
        "陈兵原野",
        three_doors_ready=True,
        five_generals_released=True,
        yin_yang_harmonious=True,
        direction="南",
        host_calc=17,
        guest_calc=13,
    )

    data = adapt_j4m_to_c8(
        source_profile="jinjing_siku_volume4",
        three_doors_result=doors,
        five_generals_result=generals,
        host_guest_result=host_guest,
        home_cal=17,
        away_cal=13,
    )

    c8_l3 = data["c8_result"]["layers"]["host_guest_movement"]
    overlay = data["j4m_overlay"]["host_guest_full"]

    assert c8_l3["winner"] is None
    assert overlay["source_campaign_verdict"] == "所向必克"
    assert overlay["source_temporal_outcome"] == "先起者胜，后起者负"
    assert overlay["winner"] == "客"
    assert overlay["start_deity"] == "和德"
    assert data["default_c8_profile_unchanged"] is True
    assert data["c8_result"]["source_profile"] == "volume5_strict"


def test_adapter_rejects_wrong_rule_id_or_profile():
    wrong_rule = {
        "ruleset": "jinjing-siku-v4-military-12",
        "source_profile": "jinjing_siku_volume4",
        "rule_id": "J4M-09",
        "three_doors_ready": True,
    }
    data = adapt_j4m_to_c8(
        source_profile="jinjing_siku_volume4",
        three_doors_result=wrong_rule,
    )
    assert data["status"] == "invalid_j4m_inputs"
    assert any("expected J4M-01" in item for item in data["errors"])


def test_default_c8_behavior_does_not_depend_on_adapter():
    data = junshi_zhanlue(
        home_cal=17,
        away_cal=13,
        three_doors=True,
        five_generals=True,
    )
    assert data["source_profile"] == "volume5_strict"
    assert data["source_variants"] == []
    assert data["layers"]["host_guest_movement"]["winner"] is None
