from rules.jinjing.eight_door import DOOR_CYCLE, DOOR_ORDER, DOOR_PERIOD, eight_door


def test_legacy_eight_door_delegates_to_c123_semantics():
    assert DOOR_PERIOD == 30
    assert DOOR_CYCLE == 240
    assert DOOR_ORDER == ("開", "休", "生", "傷", "杜", "景", "死", "驚")
    assert eight_door(1) == "開"
    assert eight_door(30) == "開"
    assert eight_door(31) == "休"
    assert eight_door(240) == "驚"
    assert eight_door(241) == "開"


def test_legacy_zero_compatibility_is_preserved():
    assert eight_door(0) == "驚"
