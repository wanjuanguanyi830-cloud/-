import pytest

from kintaiyi.tongzong_v17_conditions import (
    C27_VERSION,
    c27_catalog,
    capture_fugitive,
    hearsay_reality,
    prison_interrogation,
    request_gain,
)


def test_v17_06_skyeyes_yanji_good_is_false_bad_is_real():
    good = hearsay_reality("吉", skyeyes_yanji_taiyi=True)
    bad = hearsay_reality("凶", skyeyes_yanji_taiyi=True)
    assert good["canonical"] == C27_VERSION
    assert good["source_rule_id"] == "V17-06"
    assert good["resolved_effect"] == "虚"
    assert bad["resolved_effect"] == "实"


def test_v17_06_doors_ready_good_news_is_good():
    data = hearsay_reality(
        "吉",
        three_doors_ready=True,
        five_generals_released=True,
    )
    assert data["resolved_effect"] == "吉"
    assert data["source_variant"] is None


def test_v17_06_doors_ready_bad_news_preserves_witness_variant():
    data = hearsay_reality(
        "凶",
        three_doors_ready=True,
        five_generals_released=True,
    )
    assert data["resolved_effect"] == "variant_conflict"
    variant = data["source_variant"]
    assert variant["status"] == "variant_conflict"
    assert {item["effect"] for item in variant["variants"]} == {"不凶", "凶"}
    assert variant["resolution"] == "preserve_both_no_silent_merge"


@pytest.mark.parametrize(
    "kind,expected",
    [("吉", "不吉"), ("凶", "凶")],
)
def test_v17_06_doors_or_generals_not_ready(kind, expected):
    data = hearsay_reality(
        kind,
        three_doors_ready=False,
        five_generals_released=True,
    )
    assert data["resolved_effect"] == expected


@pytest.mark.parametrize(
    "realm,kind,expected",
    [
        ("内", "忧", "忧"),
        ("内", "喜", "不喜"),
        ("外", "忧", "不忧"),
        ("外", "喜", "喜"),
    ],
)
def test_v17_06_skyeyes_inner_outer_hearsay(realm, kind, expected):
    data = hearsay_reality(kind, skyeyes_realm=realm)
    assert data["resolved_effect"] == expected


def test_v17_06_conflicting_conditions_stay_mixed():
    data = hearsay_reality(
        "吉",
        skyeyes_yanji_taiyi=True,
        host_clamps_guest=True,
    )
    assert data["resolved_effect"] == "mixed_evidence"
    assert {item["effect"] for item in data["evidence"]} == {"虚", "吉"}


def test_v17_07_guest_clamps_host_is_capture_evidence():
    data = capture_fugitive(guest_clamps_host=True)
    assert data["source_rule_id"] == "V17-07"
    assert data["verdict"] == "捕得"
    assert data["catch_evidence"] == ["客挟主人"]


def test_v17_07_multiple_capture_conditions_accumulate():
    data = capture_fugitive(
        shiji_realm="内",
        skyeyes_realm="内",
        taiyi_host_same_palace=True,
        skyeyes_over_taiyi_host=True,
    )
    assert data["verdict"] == "捕得"
    assert "下目始击在内" in data["catch_evidence"]
    assert "天目在内" in data["catch_evidence"]
    assert "太乙与主人同宫而天目临之" in data["catch_evidence"]


def test_v17_07_host_outer_and_both_eyes_outer_are_miss_evidence():
    data = capture_fugitive(
        skyeyes_realm="外",
        shiji_realm="外",
        host_realm="外",
    )
    assert data["verdict"] == "不得"
    assert "主人在外" in data["miss_evidence"]
    assert "天目与下目俱在外" in data["miss_evidence"]


def test_v17_07_skyeyes_mask_can_produce_mixed_evidence():
    data = capture_fugitive(
        guest_clamps_host=True,
        skyeyes_masks_taiyi=True,
    )
    assert data["verdict"] == "mixed_evidence"
    assert "天目掩太乙：得而复失" in data["miss_evidence"]


def test_v17_07_hideout_pattern_recommends_search_when_not_wang_xiang():
    data = capture_fugitive(
        hideout_pattern="迫",
        hideout_qi_state="休",
    )
    assert data["hideout"]["recommendation"] == "可按迫之下寻其藏匿"
    assert data["verdict"] == "未定"


@pytest.mark.parametrize("state", ["旺", "相"])
def test_v17_07_hideout_wang_xiang_is_not_host_general_proxy(state):
    data = capture_fugitive(
        guest_clamps_host=True,
        hideout_pattern="掩",
        hideout_qi_state=state,
    )
    assert data["verdict"] == "mixed_evidence"
    assert "所捕之地旺相有气" in data["miss_evidence"]
    assert "不可往捕" in data["hideout"]["recommendation"]
    assert "不得拿主将旺相" in data["policy"]


def test_v17_08_disputed_prison_conditions_preserve_variant():
    data = prison_interrogation(skyeyes_yanji_taiyi=True)
    assert data["source_rule_id"] == "V17-08"
    assert data["verdict"] == "variant_conflict"
    assert data["source_variant"]["status"] == "variant_conflict"
    effects = {item["effect"] for item in data["source_variant"]["variants"]}
    assert effects == {"宜对吏入狱、易解", "不可入狱对吏"}


@pytest.mark.parametrize(
    "kwargs",
    [
        {"host_realm": "外"},
        {"host_qi_state": "旺"},
    ],
)
def test_v17_08_other_disputed_triggers_also_variant(kwargs):
    data = prison_interrogation(**kwargs)
    assert data["verdict"] == "variant_conflict"


def test_v17_08_taiyi_just_entered_is_delayed():
    data = prison_interrogation(taiyi_just_entered_palace=True)
    assert data["verdict"] == "迟留难解"


def test_v17_08_same_palace_skyeyes_over_is_easy_release():
    data = prison_interrogation(
        taiyi_host_same_palace=True,
        skyeyes_over_taiyi_host=True,
    )
    assert data["verdict"] == "易解"


def test_v17_08_stable_positive_and_negative_conditions_are_mixed():
    data = prison_interrogation(
        taiyi_just_entered_palace=True,
        taiyi_host_same_palace=True,
        skyeyes_over_taiyi_host=True,
    )
    assert data["verdict"] == "mixed_evidence"


def test_v17_08_does_not_apply_legacy_16_26_36_release_rule():
    data = prison_interrogation()
    assert data["home_cal_release_rule_applied"] is False
    assert "未见该条" in data["policy"]


def test_v17_09_skyeyes_inner_is_gain_outer_is_no_gain():
    inner = request_gain(skyeyes_realm="内")
    outer = request_gain(skyeyes_realm="外")
    assert inner["source_rule_id"] == "V17-09"
    assert inner["verdict"] == "有得"
    assert outer["verdict"] == "不得"


def test_v17_09_clamp_directions_are_opposite_evidence():
    host = request_gain(
        skyeyes_realm=None,
        host_clamps_guest=True,
    )
    guest = request_gain(
        skyeyes_realm=None,
        guest_clamps_host=True,
    )
    assert host["verdict"] == "不得"
    assert guest["verdict"] == "有得"


def test_v17_09_mixed_positive_and_negative_evidence_is_preserved():
    data = request_gain(
        skyeyes_realm="内",
        host_clamps_guest=True,
    )
    assert data["verdict"] == "mixed_evidence"
    assert data["gain_evidence"]
    assert data["no_gain_evidence"]


def test_v17_09_ge_taiyi_and_wang_are_negative_evidence():
    data = request_gain(
        skyeyes_realm=None,
        skyeyes_ge_taiyi=True,
        host_qi_state="旺",
    )
    assert data["verdict"] == "不得"
    assert len(data["no_gain_evidence"]) == 2


@pytest.mark.parametrize(
    "season,digit",
    [("春", 6), ("夏", 6), ("秋", 4), ("冬", 4)],
)
def test_v17_09_absolute_qi_numbers(season, digit):
    data = request_gain(
        skyeyes_realm=None,
        season=season,
        skyeyes_calc_digit=digit,
    )
    assert data["absolute_qi_number"] is True
    assert data["verdict"] == "不得"


@pytest.mark.parametrize(
    "season,digit",
    [("春", 4), ("夏", 4), ("秋", 6), ("冬", 6)],
)
def test_v17_09_non_absolute_qi_pairs_do_not_invent_negative_evidence(season, digit):
    data = request_gain(
        skyeyes_realm=None,
        season=season,
        skyeyes_calc_digit=digit,
    )
    assert data["absolute_qi_number"] is False
    assert data["verdict"] == "未定"


def test_v17_09_never_calls_cross_volume_guxu_helper():
    data = request_gain(skyeyes_realm="内")
    assert data["cross_volume_helper_used"] is False
    assert "不调用V17-D1" in data["policy"]


def test_invalid_c27_inputs_rejected():
    with pytest.raises(ValueError):
        hearsay_reality("好")
    with pytest.raises(ValueError):
        capture_fugitive(skyeyes_realm="中")
    with pytest.raises(ValueError):
        prison_interrogation(host_qi_state="长生")
    with pytest.raises(ValueError):
        request_gain(skyeyes_realm="中")


def test_c27_catalog_lists_four_rules_and_two_variants():
    data = c27_catalog()
    assert data["implemented"] == ["V17-06", "V17-07", "V17-08", "V17-09"]
    assert data["structured_conditions_only"] is True
    assert data["known_variants"] == [
        "V17-06_doors_ready_bad_news",
        "V17-08_prison_entry_conditions",
    ]
