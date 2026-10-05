import pytest

from kintaiyi.taiyi_calculations import (
    calc_from_eye,
    g6_g7_chain,
    host_guest_calculations,
)


def test_g6_jinjing_source_example_taiyi_9_dayi_eye_is_16():
    data = calc_from_eye(9, "大义")
    assert data["eye_sector"] == "亥"
    assert data["calc_value"] == 16
    counted = [(x["sector"], x["value"]) for x in data["path"] if x["counted"]]
    assert counted == [("亥", 1), ("子", 8), ("艮", 3), ("卯", 4)]
    assert data["path"][-1]["sector"] == "巽"
    assert data["path"][-1]["role"] == "taiyi_terminal"
    assert data["path"][-1]["counted"] is False


@pytest.mark.parametrize(
    ("taiyi", "eye", "expected"),
    [
        (1, "戌", 1),
        (3, "丑", 1),
        (4, "寅", 1),
        (9, "辰", 1),
        (2, "巳", 1),
        (7, "未", 1),
        (6, "申", 1),
        (8, "亥", 1),
    ],
)
def test_g6_same_palace_interstitial_forced_one(taiyi, eye, expected):
    data = calc_from_eye(taiyi, eye)
    assert data["same_palace"] is True
    assert data["eye_position_type"] == "间神"
    assert data["forced_single_count"] is True
    assert data["calc_value"] == expected
    assert len(data["path"]) == 1


@pytest.mark.parametrize(
    ("taiyi", "eye", "expected"),
    [
        (1, "乾", 1),
        (2, "午", 2),
        (3, "艮", 3),
        (4, "卯", 4),
        (6, "酉", 6),
        (7, "坤", 7),
        (8, "子", 8),
        (9, "巽", 9),
    ],
)
def test_g6_same_palace_positive_takes_own_palace_number(taiyi, eye, expected):
    data = calc_from_eye(taiyi, eye)
    assert data["same_palace"] is True
    assert data["eye_position_type"] == "正宫"
    assert data["calc_value"] == expected


def test_g6_interstitial_start_adds_one_only_once():
    data = calc_from_eye(8, "戌")
    counted = [(x["sector"], x["value"]) for x in data["path"] if x["counted"]]
    assert counted == [("戌", 1), ("乾", 1)]
    assert data["calc_value"] == 2
    assert data["path"][-1]["sector"] == "子"
    assert data["path"][-1]["counted"] is False


def test_g6_host_guest_roles_and_g7_chain():
    calcs = host_guest_calculations(
        taiyi_palace=9,
        wenchang="大义",
        shiji="武德",
    )
    assert calcs["host_calc"] == 16
    assert calcs["guest_calc"] == 23

    chain = g6_g7_chain(
        taiyi_palace=9,
        wenchang="大义",
        shiji="武德",
    )
    assert chain["host_big_general_palace"] == 6
    assert chain["host_assistant_general_palace"] == 8
    assert chain["guest_big_general_palace"] == 3
    assert chain["guest_assistant_general_palace"] == 9
