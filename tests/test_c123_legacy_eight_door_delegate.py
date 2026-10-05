from rules.jinjing.eight_door import DOOR_CYCLE, DOOR_ORDER, DOOR_PERIOD, eight_door


def test_legacy_eight_door_delegates_to_c123_semantics():
    assert DOOR_PERIOD == 30
    assert DOOR_CYCLE == 240
    assert DOOR_ORDER == ("开", "休", "生", "伤", "杜", "景", "死", "惊")
    assert eight_door(1) == "开"
    assert eight_door(30) == "开"
    assert eight_door(31) == "休"
    assert eight_door(240) == "惊"
    assert eight_door(241) == "开"


def test_legacy_zero_compatibility_is_preserved():
    assert eight_door(0) == "惊"
