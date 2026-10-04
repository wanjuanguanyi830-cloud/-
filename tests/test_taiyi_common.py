import pytest

from kintaiyi import taiyi_common as c


def test_complete_coordinate_metadata():
    assert len(set(c.SIXTEEN)) == len(c.SIXTEEN) == 16
    assert set(c.SECTOR_GODS) == set(c.SECTOR_ELEMENTS) == set(c.SIXTEEN)
    assert all(c.GOD_SECTORS[god] == sector for sector, god in c.SECTOR_GODS.items())
    assert len(c.SIXTEEN_GOD_ELEMENTS) == 16
    assert [c.SIXTEEN_GOD_ELEMENTS[g] for g in ("和德", "大炅", "大武")] == ["土", "木", "土"]
    assert set(c.NINE_PALACES) == set(range(1, 10))
    assert [(c.nine_palace_to_trigram(i), c.nine_palace_representative_sector(i))
            for i in (2, 4, 6, 8)] == [("离", "午"), ("震", "卯"), ("兑", "酉"), ("坎", "子")]
    assert c.NINE_PALACES[5]["yin_yang"] is None
    assert [c.nine_palace_element(i) for i in range(1, 10)] == list("金火土木土金土水木")


@pytest.mark.parametrize("sector,palace", zip(c.SIXTEEN, (8, 3, 3, 4, 4, 9, 9, 2, 2, 7, 7, 6, 6, 1, 1, 8)))
def test_lossy_projection(sector, palace):
    assert c.sector_to_nine_palace(sector) == palace


@pytest.mark.parametrize("sector,landing", zip(c.SIXTEEN, ["卯", "辰", "巽", "巳", "午", "未", "坤", "申", "酉", "戌", "乾", "亥", "子", "丑", "艮", "寅"]))
def test_dashen_full_ring(sector, landing):
    assert c.dashen_from_sector(sector) == landing
    assert c.rotate_sixteen(sector, -16) == sector
    assert c.rotate_sixteen(landing, -4) == sector
    assert c.rotate_sixteen(sector, 36) == landing


@pytest.mark.parametrize("palace,landing", [(1, "艮"), (2, "酉"), (3, "巽"), (4, "午"), (6, "子"), (7, "乾"), (8, "卯"), (9, "坤")])
def test_dashen_palaces(palace, landing):
    assert c.dashen_from_nine_palace(palace) == landing


def test_center_rejects_sector():
    for fn in (c.nine_palace_representative_sector, c.dashen_from_nine_palace):
        with pytest.raises(ValueError):
            fn(5)
    with pytest.raises(ValueError):
        c.sector_detail("中")


@pytest.mark.parametrize("subject,states", zip("木火土金水", ("旺休囚死相", "相旺休囚死", "死相旺休囚", "囚死相旺休", "休囚死相旺")))
def test_all_25_states(subject, states):
    assert "".join(c.qi_relation(subject, e)["state"] for e in "木火土金水") == states


def test_fire_stages_are_separate_and_complete():
    assert [c.fire_twelve_stage(s) for s in "寅卯辰巳午未申酉戌亥子丑"] == ["长生", "沐浴", "冠带", "临官", "帝旺", "衰", "病", "死", "墓", "绝", "胎", "养"]
    assert all(c.fire_twelve_stage(s) is None for s in "艮巽坤乾")


@pytest.mark.parametrize("sector,state", [("乾", "囚"), ("巽", "相"), ("辰", "休"), ("戌", "休")])
def test_mode_a(sector, state):
    assert c.dashen_self_qi(sector)["state"] == state


@pytest.mark.parametrize("palace,sector,state", [(8, "子", "旺"), (9, "子", "相"), (6, "坤", "相"), (3, "坤", "旺"), (9, "酉", "死")])
def test_mode_b(palace, sector, state):
    assert c.general_palace_qi(palace, sector)["state"] == state


def test_eyes_preserve_dual_elements():
    for sector, palace, element in (("辰", 9, "木"), ("戌", 1, "金")):
        data = c.sector_detail(sector)
        assert (data["element"], data["nine_palace"], data["nine_palace_element"]) == ("土", palace, element)
