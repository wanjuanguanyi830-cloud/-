import pytest

from kintaiyi.jinjing_huangdao_tables import (
    C118_VERSION,
    MANSION_ORDER,
    c118_catalog,
    mansion_division,
    mansion_span,
    solar_term_anchor,
    term_day_position,
)


def test_c118_catalog_has_complete_direct_tables():
    catalog = c118_catalog()
    assert catalog["canonical"] == C118_VERSION
    assert len(catalog["solar_term_anchors"]) == 24
    assert len(catalog["mansion_spans"]) == 28
    assert len(catalog["divisions"]) == 12
    assert tuple(catalog["mansion_spans"]) == MANSION_ORDER


@pytest.mark.parametrize(
    ("term", "mansion", "num", "den"),
    [
        ("冬至", "斗", 9, 1),
        ("春分", "奎", 4, 1),
        ("夏至", "井", 1, 1),
        ("秋分", "轸", 13, 1),
        ("立冬", "房", 1, 1),
        ("大雪", "箕", 3, 1),
    ],
)
def test_solar_term_anchor_direct_table(term, mansion, num, den):
    data = solar_term_anchor(term)
    assert data["mansion"] == mansion
    assert data["degree"] == {"numerator": num, "denominator": den}


def test_mansion_spans_preserve_fractional_and_ambiguous_entries():
    assert mansion_span("女")["numeric_span"] == {"numerator": 23, "denominator": 2}
    assert mansion_span("奎")["numeric_span"] == {"numerator": 35, "denominator": 2}
    assert mansion_span("轸")["numeric_span"] == {"numerator": 37, "denominator": 2}
    assert mansion_span("箕")["numeric_span"] == {"numerator": 21, "denominator": 2}

    xu = mansion_span("虚")
    assert xu["numeric_span"] is None
    assert xu["status"] == "transcription_ambiguous"
    assert "不据总周天反推" in xu["note"]


def test_twelve_divisions_cover_all_twenty_eight_mansions_once():
    catalog = c118_catalog()
    flattened = [
        mansion
        for row in catalog["divisions"]
        for mansion in row["mansions"]
    ]
    assert len(flattened) == 28
    assert len(set(flattened)) == 28
    assert set(flattened) == set(MANSION_ORDER)


@pytest.mark.parametrize(
    ("mansion", "state", "branch", "regions"),
    [
        ("斗", "吴越", "丑", ["扬州", "交州"]),
        ("虚", "齐", "子", ["青州"]),
        ("奎", "鲁", "戌", ["徐州"]),
        ("参", "晋", "申", ["益州"]),
        ("房", "宋", "卯", ["豫州"]),
        ("箕", "燕", "寅", ["幽州"]),
    ],
)
def test_mansion_division_table(mansion, state, branch, regions):
    data = mansion_division(mansion)
    assert data["state"] == state
    assert data["branch"] == branch
    assert data["regions"] == regions


def test_lidong_sixth_day_matches_jinjing_current_time_example():
    day1 = term_day_position("立冬", 1)
    day5 = term_day_position("立冬", 5)
    day6 = term_day_position("立冬", 6)

    assert (day1["mansion"], day1["degree"]) == (
        "房", {"numerator": 1, "denominator": 1}
    )
    assert (day5["mansion"], day5["degree"]) == (
        "房", {"numerator": 5, "denominator": 1}
    )
    assert (day6["mansion"], day6["degree"]) == (
        "心", {"numerator": 1, "denominator": 1}
    )
    assert day6["division"]["branch"] == "卯"


def test_progression_blocks_when_it_must_use_ambiguous_xu_span():
    # 大寒锚点为女8；推进足够远后进入虚宿并还需继续跨越其未定宿度。
    data = term_day_position("大寒", 20)
    assert data["computable"] is False
    assert data["status"] == "blocked_ambiguous_mansion_span"
    assert data["blocked_by"] == "虚"
    assert data["pending"]


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        solar_term_anchor("不存在")
    with pytest.raises(ValueError):
        mansion_span("不存在")
    with pytest.raises(ValueError):
        mansion_division("不存在")
    with pytest.raises(ValueError):
        term_day_position("立冬", 0)
    with pytest.raises(TypeError):
        term_day_position("立冬", True)
