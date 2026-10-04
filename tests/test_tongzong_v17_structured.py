import pytest

from kintaiyi.tongzong_v17_structured import (
    capture_fugitive,
    c27_catalog,
    prisoner_official,
    report_truth,
    request_outcome,
)


def test_v17_06_yanji_makes_bad_report_real_and_good_report_false():
    bad = report_truth("凶", skyeyes_yanji_taiyi=True)
    good = report_truth("吉", skyeyes_yanji_taiyi=True)
    assert bad["positive_evidence"][0]["effect"] == "不善之事为实"
    assert good["negative_evidence"][0]["effect"] == "善事为虚"


def test_v17_06_doors_generals_bad_report_keeps_source_variant():
    data = report_truth(
        "凶",
        three_doors_ready=True,
        five_generals_released=True,
    )
    assert data["source_variants"]
    variant = data["source_variants"][0]
    assert variant["status"] == "witness_variant"
    assert len(variant["readings"]) == 2
    assert variant["resolution"] == "preserve_both_no_silent_merge"


def test_v17_06_mixed_conditions_do_not_overwrite_each_other():
    data = report_truth(
        "喜",
        skyeyes_yanji_taiyi=True,
        host_clamps_guest=True,
        skyeyes_realm="外",
    )
    assert data["summary"] == "mixed_evidence"
    assert data["positive_evidence"]
    assert data["negative_evidence"]


def test_v17_06_rejects_legacy_prose_kind():
    with pytest.raises(ValueError):
        report_truth("所闻吉事则吉")


def test_v17_07_capture_and_no_capture_can_coexist():
    data = capture_fugitive(
        guest_clamps_host=True,
        host_realm="外",
    )
    assert data["summary"] == "mixed_evidence"
    assert data["capture_evidence"][0]["effect"] == "捕得"
    assert data["no_capture_evidence"][0]["effect"] == "不得"


def test_v17_07_masks_taiyi_is_get_then_lose():
    data = capture_fugitive(skyeyes_masks_taiyi=True)
    assert data["special_evidence"] == [
        {"condition": "天目掩太乙", "effect": "得而复失"}
    ]


def test_v17_07_hideout_qi_state_applies_to_hideout_only():
    bad = capture_fugitive(
        hideout_pattern="掩",
        hideout_qi_state="旺",
    )
    good = capture_fugitive(
        hideout_pattern="迫",
        hideout_qi_state="休",
    )
    assert bad["pursuit_advice"] == "不可往，往则受辱且事不济"
    assert good["pursuit_advice"] == "可据掩迫之下追捕"


def test_v17_07_missing_hideout_qi_does_not_guess():
    data = capture_fugitive(
        hideout_pattern="掩",
        hideout_qi_state=None,
    )
    assert "缺藏匿地旺相输入" in data["pursuit_advice"]


def test_v17_08_preserves_host_realm_variant():
    inner = prisoner_official(host_realm="内")
    outer = prisoner_official(host_realm="外")
    assert inner["source_variants"][0]["status"] == "source_variant"
    assert outer["source_variants"][0]["status"] == "source_variant"
    assert inner["source_variants"][0]["readings"][1]["matches"] is True
    assert outer["source_variants"][0]["readings"][0]["matches"] is True


def test_v17_08_easy_release_and_delay_can_conflict():
    data = prisoner_official(
        taiyi_just_entered_palace=True,
        taiyi_host_same_palace=True,
        skyeyes_over_taiyi_host=True,
    )
    assert data["summary"] == "mixed_evidence"
    assert any("迟留" in item["effect"] for item in data["unfavorable_evidence"])
    assert any("易出" in item["effect"] for item in data["favorable_evidence"])


def test_v17_08_wang_state_is_unfavorable():
    data = prisoner_official(host_qi_state="旺")
    assert data["summary"] == "negative"
    assert data["unfavorable_evidence"][0]["condition"] == "主人立旺神"


def test_v17_09_inner_outer_and_clamps_are_independent_evidence():
    data = request_outcome(
        skyeyes_realm="内",
        host_clamps_guest=True,
        guest_clamps_host=True,
        host_realm="外",
    )
    assert data["summary"] == "mixed_evidence"
    assert len(data["positive_evidence"]) >= 2
    assert len(data["negative_evidence"]) >= 2


def test_v17_09_ge_taiyi_blocks_requests():
    data = request_outcome(skyeyes_ge_taiyi=True)
    assert data["summary"] == "negative"
    assert data["negative_evidence"][0]["condition"] == "天目格太乙"


@pytest.mark.parametrize(
    "season,digit,expected",
    [
        ("春", 6, True),
        ("夏", 6, True),
        ("秋", 4, True),
        ("冬", 4, True),
        ("春", 4, False),
        ("冬", 6, False),
    ],
)
def test_v17_09_absolute_qi_numbers(season, digit, expected):
    data = request_outcome(season=season, skyeyes_calc_digit=digit)
    assert data["absolute_qi_number"] is expected


def test_v17_09_does_not_call_cross_volume_guxu_helper():
    data = request_outcome(
        skyeyes_realm="内",
        host_qi_state="休",
    )
    assert "guxu" not in str(data).lower()
    assert data["source_rule_id"] == "V17-09"


def test_c27_catalog_is_explicitly_structured_only():
    data = c27_catalog()
    assert data["implemented"] == ["V17-06", "V17-07", "V17-08", "V17-09"]
    assert data["dependency_class"] == "structured_conditions"
    assert set(data["known_variants"]) == {
        "V17-06_doors_generals_bad_report",
        "V17-08_host_realm",
    }
