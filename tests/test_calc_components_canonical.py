from kintaiyi.eight_divinations import calc_preparedness, sancai


def test_blocked_five_has_ground_only():
    data = calc_preparedness(5)
    assert data["present"] == ["吏士"]
    assert data["missing"] == ["将军", "兵卒"]
    assert sancai(5)["components"] == {"ten": False, "five": True, "one": False}


def test_15_has_heaven_and_ground_only():
    data = calc_preparedness(15)
    assert data["present"] == ["将军", "吏士"]
    assert data["missing"] == ["兵卒"]
    assert sancai(15)["components"] == {"ten": True, "five": True, "one": False}


def test_25_has_heaven_and_ground_only():
    data = calc_preparedness(25)
    assert data["present"] == ["将军", "吏士"]
    assert data["missing"] == ["兵卒"]
    assert sancai(25)["components"] == {"ten": True, "five": True, "one": False}


def test_35_has_heaven_and_ground_only():
    data = calc_preparedness(35)
    assert data["present"] == ["将军", "吏士"]
    assert data["missing"] == ["兵卒"]
    assert sancai(35)["components"] == {"ten": True, "five": True, "one": False}
