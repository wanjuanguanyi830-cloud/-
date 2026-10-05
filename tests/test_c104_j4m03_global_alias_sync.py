from kintaiyi.jinjing_v4_military import (
    j4m03_eye_element_from_god,
    zhuke_xiangguan,
)
from kintaiyi.taiyi_rules import GOD_ALIASES


def test_c104_j4m03_taicu_alias_uses_global_canonical_value():
    assert GOD_ALIASES["太蔟"] == "太簇"
    assert j4m03_eye_element_from_god("太蔟") == "金"

    result = zhuke_xiangguan(
        host_eye_god="高丛",
        guest_eye_god="太蔟",
    )
    assert result["guest_eye_god"] == "太蔟"
    assert result["guest_eye_god_canonical"] == GOD_ALIASES["太蔟"]
    assert result["god_name_aliases"]["太蔟"] == GOD_ALIASES["太蔟"]
