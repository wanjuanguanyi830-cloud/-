import pytest
import config
from kintaiyi import eight_divinations as d
from kintaiyi.kintaiyi import Taiyi, TaiyiCanonicalMixin
from kintaiyi.taiyi_common import SIXTEEN_GOD_ELEMENTS, qi_relation
from kintaiyi.taiyi_cycles import big_wander, five_blessings, small_wander


def test_legacy_data_and_display_delegate_to_canonical():
    assert config._SIXTEEN_GOD_WX is SIXTEEN_GOD_ELEMENTS
    assert config._GENERAL_WX["主將"] == "金"
    assert config._GENERAL_WX["主參"] == "水"
    assert config._GENERAL_WX["天乙"] == "金"
    assert len(config._WX_REL) == 25
    assert all(state == qi_relation(*key)["state"] for key, state in config._WX_REL.items())
    assert config.cal_des(15) == ["杜塞"]
    assert config._calc_jianbei(15)["preparedness"]["missing"] == ["兵卒"]
    assert "length" not in config._calc_jianbei(15)
    assert config.gudan(12) == config.gudan_zhanlue(12) == d.gudan_analysis(12)
    assert config.suenwl(3, 15, 5, 5)["winner"] == "away"
    assert config.suenwl(10, 10)["status"] == "原典未明言"


def test_fixed_realms_preserve_old_ui_keys_and_signatures():
    for ty in range(1,10):
        data = config.neiwai_gongji(ty, "辰")
        assert {"孤虛","宜攻","斷語"} <= set(data)
        assert data["宜攻"] == "外"
    assert config.neiwai_gongji("大神")["宜攻"] == "內"


def test_cycle_facades_use_new_one_based_core():
    for n in (1,45,46,225,226,10154821):
        assert config.wufu(n)["palace_id"] == five_blessings(n)["palace_id"]
        assert config.bigyo(n)["palace_id"] == big_wander(n, profile="tongzong")["palace_id"]
        assert config.smyo(n) == small_wander(n)["palace_id"]
    assert config.junshi_zhanlue(15)["數有所主"]["主"]["missing"] == ["兵卒"]
    assert config.junshi_zhanlue(15)["五音"]["主"]["tone"] == "羽"
    with pytest.warns(DeprecationWarning):
        assert config.returnarmy(9)["computable"] is False


def test_base_and_four_taiyi_methods_never_use_72_layouts():
    class CalendarFacts(TaiyiCanonicalMixin):
        def accnum(self, style, profile):
            return 10153917 + 622

        def kook(self, *args):
            raise AssertionError("72局不是这些规则真源")
    engine = CalendarFacts()
    assert engine.skyyi(0,0) == 12
    assert engine.kingbase(0,0) in "子丑寅卯辰巳午未申酉戌亥"
    assert engine.officerbase(0,0) in "子丑寅卯辰巳午未申酉戌亥"
    assert engine.pplbase(0,0) in "子丑寅卯辰巳午未申酉戌亥"
    snapshot = Taiyi({"accumulated_year": 10153917 + 622, "ji_style": 0})
    assert snapshot.skyyi(0,0) == 12
    with pytest.raises(ValueError):
        snapshot.accnum(2,0)


def test_ruler_meeting_uses_heaven_not_ordinary_taiyi():
    class Facts(TaiyiCanonicalMixin):
        def accnum(self, *args):
            return 10154539

        def ty(self, *args):
            raise AssertionError("君基+天乙不能使用普通太乙")
    fact = Facts().ming_kingbase(0,0)
    assert fact["heaven_palace_id"] == 12 and fact["heaven_sector"] == "寅"


def test_legacy_json_conversion_cannot_drop_colliding_keys():
    from kintaiyi.pan_adapter import build_v2_from_legacy_snapshot
    with pytest.raises(ValueError, match="重复"):
        build_v2_from_legacy_snapshot({"局式": {1: "first", "1": "second"}})
