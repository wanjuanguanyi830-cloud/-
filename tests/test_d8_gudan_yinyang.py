import pytest

from kintaiyi.eight_divinations import gudan_state, tui_danger


@pytest.mark.parametrize(
    ("calc", "state", "disadvantaged", "danger"),
    [
        (1, "单阳", "主", None),
        (3, "单阳", "主", None),
        (2, "单阴", "客", None),
        (8, "单阴", "客", None),
        (10, "孤阳", "主", None),
        (30, "孤阳", "主", None),
        (20, "孤阴", "客", None),
        (40, "孤阴", "客", None),
        (11, "重阳", "主", "火厄"),
        (39, "重阳", "主", "火厄"),
        (22, "重阴", "客", "水厄"),
        (28, "重阴", "客", "水厄"),
    ],
)
def test_gudan_uses_explicit_canonical_number_sets(calc, state, disadvantaged, danger):
    result = gudan_state(calc)

    assert result["state"] == state
    assert result["disadvantaged"] == disadvantaged
    assert result["danger"] == danger
    assert result["blocked"] is False
    assert result["basic_effects"] == [
        {"classification": state, "disadvantaged": disadvantaged}
    ]


@pytest.mark.parametrize("calc", [5, 15, 25, 35])
def test_gudan_does_not_force_blocked_numbers_into_isolated_categories(calc):
    result = gudan_state(calc)

    assert result["blocked"] is True
    assert result["state"] is None
    assert result["single"] is None
    assert result["isolated"] is None
    assert result["disadvantaged"] is None
    assert result["danger"] is None
    assert result["basic_effects"] == []
    assert result["pending"] == ["杜塞数不强塞孤单分类"]


@pytest.mark.parametrize("calc", [12, 14, 18, 21, 23, 27, 32, 34, 38])
def test_gudan_does_not_infer_unlisted_mixed_numbers(calc):
    result = gudan_state(calc)

    assert result["state"] is None
    assert result["basic_effects"] == []


def test_yinyang_danger_is_independent_from_gudan_blocked_status():
    result = tui_danger(8, 15, 22)

    assert result["palace_yinyang"] == "阳"
    assert result["participates"] is True
    assert result["events"] == [
        {"side": "主", "state": "重阳", "danger": "火厄"}
    ]


def test_yinyang_danger_for_yin_palace_even_calc():
    result = tui_danger(2, 11, 22)

    assert result["palace_yinyang"] == "阴"
    assert result["events"] == [
        {"side": "客", "state": "重阴", "danger": "水厄"}
    ]


def test_yinyang_danger_returns_no_danger_for_nonmatching_parity():
    result = tui_danger(8, 16, 22)

    assert result["events"] == []
    assert result["verdict"] == "无厄"


def test_yinyang_danger_center_five_does_not_participate():
    result = tui_danger(5, 15, 22)

    assert result["palace_yinyang"] is None
    assert result["participates"] is False
    assert result["events"] == []
    assert result["verdict"] == "中五不参与本术"
