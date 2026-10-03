from __future__ import annotations

import pytest

from rules.jinjing import eight_door
from rules.jinjing.geju import (
    PALACE_RING,
    SIXTEEN_RING,
    GEJU_RULESET_VERSION,
    GejuContext,
    analyze_geju,
    chen_relation_to_taiyi,
    is_palace_flanked,
    palace_relation_to_taiyi,
    to_legacy_dict,
)


def context(**overrides) -> GejuContext:
    values = {
        "taiyi": 8,
        "wenchang": "巽",
        "shiji": "午",
        "home_big": 4,
        "home_vassal": 9,
        "away_big": 2,
        "away_vassal": 7,
    }
    values.update(overrides)
    return GejuContext(**values)


def keys(detail: dict) -> set[str]:
    return set(detail["舊式"])


@pytest.mark.parametrize(
    ("accumulated", "expected"),
    [
        (0, "驚"), (1, "開"), (30, "開"), (31, "休"), (60, "休"),
        (61, "生"), (90, "生"), (91, "傷"), (120, "傷"),
        (121, "杜"), (150, "杜"), (151, "景"), (180, "景"),
        (181, "死"), (210, "死"), (211, "驚"), (240, "驚"),
        (241, "開"), (480, "驚"),
    ],
)
def test_eight_door_thirty_year_ranges_and_zero_remainder(accumulated, expected):
    assert eight_door(accumulated) == expected


def test_sixteen_god_coordinates_preserve_center_and_intershen():
    assert SIXTEEN_RING == (
        "子", "丑", "艮", "寅", "卯", "辰", "巽", "巳",
        "午", "未", "坤", "申", "酉", "戌", "乾", "亥",
    )
    assert PALACE_RING == (8, 3, 4, 9, 2, 7, 6, 1)
    assert chen_relation_to_taiyi("卯", 4) == "正宮"
    assert chen_relation_to_taiyi("寅", 4) == "內辰"
    assert palace_relation_to_taiyi(3, 8) == "外宮"


def test_palace_flank_uses_the_declared_eight_palace_ring():
    assert is_palace_flanked(1, 6, 8)
    assert is_palace_flanked(4, 3, 9)


def test_upper_eye_controls_cover_hit_and_grid_but_never_pressure():
    cover = analyze_geju(context(taiyi=4, wenchang="卯", shiji="卯", dingmu="寅"))
    hit = analyze_geju(context(taiyi=4, wenchang="卯", shiji="寅", dingmu="寅"))
    event_subjects = [event["主體"] for event in hit["事件"] if event["格局"] == "迫"]
    assert "掩" in keys(cover)
    assert "擊(內辰)" in keys(hit)
    assert all("始擊" not in subjects for subjects in event_subjects)
    assert all("定目" not in subjects for subjects in event_subjects)


def test_intershen_does_not_become_same_palace_prison():
    exact = analyze_geju(context(taiyi=4, wenchang="卯"))
    between = analyze_geju(context(taiyi=4, wenchang="寅"))
    assert "囚(文昌)" in keys(exact)
    assert "囚(文昌)" not in keys(between)
    assert "辰迫(內、文昌)" in keys(between)


def test_pressure_uses_lower_eye_and_four_generals_only():
    detail = analyze_geju(context(taiyi=4, wenchang="寅", shiji="卯", home_big=3))
    pressure_subjects = [event["主體"] for event in detail["事件"] if event["格局"] == "迫"]
    assert any(subjects == ["文昌"] for subjects in pressure_subjects)
    assert any(subjects == ["主大"] for subjects in pressure_subjects)
    assert not any("始擊" in subjects or "定目" in subjects for subjects in pressure_subjects)


def test_lower_eye_palace_pressure_is_separate_from_adjacent_chen_pressure():
    detail = analyze_geju(context(taiyi=4, wenchang="巽"))
    assert "宮迫(外、文昌)" in keys(detail)


def test_general_same_palace_prison_pressure_and_four_general_barrier():
    detail = analyze_geju(context(taiyi=8, home_big=8, home_vassal=3, away_big=3))
    assert "囚(主大)" in keys(detail)
    assert "關(主參、客大)" in keys(detail)
    assert "宮迫(外、主參)" in keys(detail)


def test_opposition_rules_keep_grid_and_opposite_distinct():
    detail = analyze_geju(context(taiyi=4, wenchang="酉", shiji="酉", away_big=6))
    assert "格(始擊)" in keys(detail)
    assert "格(客大)" in keys(detail)
    assert "對" in keys(detail)


def test_duty_door_alone_controls_execution_and_grid_lift():
    doors = {8: "開", 3: "休", 4: "生", 9: "傷", 2: "杜", 7: "景", 6: "死", 1: "驚"}
    other_open = analyze_geju(context(taiyi=8, duty_door="休", doors=doors))
    duty_open = analyze_geju(context(taiyi=8, duty_door="開", doors=doors))
    assert "執(開生門合)" not in keys(other_open)
    assert "執(開生門合)" in keys(duty_open)
    opposite = analyze_geju(context(taiyi=8, duty_door="開", doors={**doors, 8: "休", 2: "開"}))
    assert "提格(開生門衝)" in keys(opposite)


def test_duty_door_is_calculated_from_the_240_year_cycle():
    doors = {8: "開", 3: "休", 4: "生", 9: "傷", 2: "杜", 7: "景", 6: "死", 1: "驚"}
    start = analyze_geju(context(taiyi=8, accumulated_year=1, doors=doors))
    year_31 = analyze_geju(context(taiyi=8, accumulated_year=31, doors=doors))
    assert start["盤面"]["值事門"] == "開"
    assert "執(開生門合)" in keys(start)
    assert year_31["盤面"]["值事門"] == "休"
    assert "執(開生門合)" not in keys(year_31)
    with pytest.raises(ValueError, match="conflicts"):
        analyze_geju(context(taiyi=8, accumulated_year=31, duty_door="開", doors=doors))


def test_flanking_is_generic_and_records_each_actor_target_pair():
    main_guest_clamp = analyze_geju(
        context(taiyi=6, home_big=9, home_vassal=7, away_big=7, away_vassal=1)
    )
    taiyi_general_clamp = analyze_geju(
        context(taiyi=9, home_big=3, away_big=4)
    )
    assert "提挾(客大、客參夾太乙)" in keys(main_guest_clamp)
    assert "提挾(太乙、主大夾客大)" in keys(taiyi_general_clamp)


def test_xiebi_is_separate_and_requires_two_intershen_eyes():
    detail = analyze_geju(context(taiyi=8, wenchang="亥", shiji="丑", home_big=1, home_vassal=3))
    one_eye = analyze_geju(context(taiyi=8, wenchang="亥", shiji="午"))
    assert "挾閉" in keys(detail)
    assert "挾閉" not in keys(one_eye)


def test_composite_patterns_and_four_guo_du_requirements():
    solid = analyze_geju(context(taiyi=4, wenchang="卯", home_big=6, home_vassal=6))
    assert "囚(文昌)" in keys(solid)
    assert "四郭固" in keys(solid)

    without_secondary = analyze_geju(
        context(taiyi=8, wenchang="卯", shiji="巳", home_big=6, away_big=6, away_vassal=3)
    )
    with_secondary = analyze_geju(
        context(taiyi=8, wenchang="卯", shiji="巳", home_big=6, away_big=6, away_vassal=4)
    )
    assert "四郭杜" not in keys(without_secondary)
    assert "四郭杜" in keys(with_secondary)
    assert not any("四郭社" in event["格局"] for event in with_secondary["事件"])


def test_legacy_dict_adapter_preserves_dictionary_of_labels_to_text():
    detail = analyze_geju(context(taiyi=4, wenchang="寅"))
    assert detail["規則版本"] == GEJU_RULESET_VERSION
    assert to_legacy_dict(detail) == detail["舊式"]
    assert isinstance(to_legacy_dict(detail), dict)


@pytest.mark.parametrize("invalid", [-1, 1.5, True, "30"])
def test_duty_door_rejects_invalid_accumulation(invalid):
    if isinstance(invalid, int) and not isinstance(invalid, bool):
        with pytest.raises(ValueError):
            eight_door(invalid)
    else:
        with pytest.raises(TypeError):
            eight_door(invalid)

