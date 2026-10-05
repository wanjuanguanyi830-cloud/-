import json
from pathlib import Path

import pytest

from kintaiyi.taiyi_rules import (
    FIRE_STAGES,
    GOD_POSITION,
    INTRINSIC_WX,
    PALACE_WX,
    PALACE_YINYANG,
    SECTOR_TO_NINE_PALACE,
    SIXTEEN,
    SIXTEEN_GOD_WX,
    dashen_from_lushen,
    general_palace_qi,
    intrinsic_element,
    nine_palace_detail,
    nine_palace_representative_sector,
    qi_relation,
)


CATALOG = Path("terminology/common-core.json")


EXPECTED_PALACES = {
    1: ("乾", "乾", "金", "阴"),
    2: ("离", "午", "火", "阴"),
    3: ("艮", "艮", "土", "阳"),
    4: ("震", "卯", "木", "阳"),
    5: ("中", None, "土", None),
    6: ("兑", "酉", "金", "阴"),
    7: ("坤", "坤", "土", "阴"),
    8: ("坎", "子", "水", "阳"),
    9: ("巽", "巽", "木", "阳"),
}

EXPECTED_GODS = [
    ("子", "地主", "水"),
    ("丑", "阳德", "土"),
    ("艮", "和德", "土"),
    ("寅", "吕申", "木"),
    ("卯", "高丛", "木"),
    ("辰", "太阳", "土"),
    ("巽", "大炅", "木"),
    ("巳", "大神", "火"),
    ("午", "大威", "火"),
    ("未", "天道", "土"),
    ("坤", "大武", "土"),
    ("申", "武德", "金"),
    ("酉", "太簇", "金"),
    ("戌", "阴主", "土"),
    ("乾", "阴德", "金"),
    ("亥", "大义", "水"),
]

EXPECTED_LUSHEN_SHIFT = {
    "子": "卯", "丑": "辰", "艮": "巽", "寅": "巳",
    "卯": "午", "辰": "未", "巽": "坤", "巳": "申",
    "午": "酉", "未": "戌", "坤": "乾", "申": "亥",
    "酉": "子", "戌": "丑", "乾": "艮", "亥": "寅",
}

EXPECTED_QI = {
    "木": {"木": "旺", "火": "休", "土": "囚", "金": "死", "水": "相"},
    "火": {"木": "相", "火": "旺", "土": "休", "金": "囚", "水": "死"},
    "土": {"木": "死", "火": "相", "土": "旺", "金": "休", "水": "囚"},
    "金": {"木": "囚", "火": "死", "土": "相", "金": "旺", "水": "休"},
    "水": {"木": "休", "火": "囚", "土": "死", "金": "相", "水": "旺"},
}


def _catalog():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_nine_palace_table_is_complete_and_center_has_no_sector():
    for palace, (trigram, sector, element, yin_yang) in EXPECTED_PALACES.items():
        detail = nine_palace_detail(palace)
        assert detail == {
            "palace_id": palace,
            "trigram": trigram,
            "representative_sector": sector,
            "element": element,
            "yin_yang": yin_yang,
        }
        assert PALACE_WX[palace] == element
        assert PALACE_YINYANG[palace] == yin_yang

    with pytest.raises(ValueError):
        nine_palace_representative_sector(5)


def test_sixteen_gods_positions_and_elements_are_stable():
    assert list(SIXTEEN) == [row[0] for row in EXPECTED_GODS]

    for sector, god, element in EXPECTED_GODS:
        assert GOD_POSITION[god] == sector
        assert SIXTEEN_GOD_WX[god] == element


@pytest.mark.parametrize(
    ("sector", "palace"),
    [
        ("亥", 8), ("子", 8),
        ("丑", 3), ("艮", 3),
        ("寅", 4), ("卯", 4),
        ("辰", 9), ("巽", 9),
        ("巳", 2), ("午", 2),
        ("未", 7), ("坤", 7),
        ("申", 6), ("酉", 6),
        ("戌", 1), ("乾", 1),
    ],
)
def test_sixteen_to_nine_palace_projection_is_lossy(sector, palace):
    assert SECTOR_TO_NINE_PALACE[sector] == palace


@pytest.mark.parametrize("sector,landing", EXPECTED_LUSHEN_SHIFT.items())
def test_lushen_shift_is_exactly_plus_four_on_sixteen_ring(sector, landing):
    assert dashen_from_lushen(sector) == landing


def test_center_five_cannot_enter_lushen_shift():
    with pytest.raises(ValueError):
        dashen_from_lushen(5)


@pytest.mark.parametrize(
    ("subject", "environment", "state"),
    [
        (subject, environment, state)
        for subject, row in EXPECTED_QI.items()
        for environment, state in row.items()
    ],
)
def test_qi_relation_covers_all_25_element_pairs(subject, environment, state):
    result = qi_relation(subject, environment)
    assert result["state"] == state


def test_fire_twelve_stages_and_four_dimensions():
    expected = {
        "寅": "长生", "卯": "沐浴", "辰": "冠带", "巳": "临官",
        "午": "帝旺", "未": "衰", "申": "病", "酉": "死",
        "戌": "墓", "亥": "绝", "子": "胎", "丑": "养",
    }
    assert FIRE_STAGES == expected
    for sector in ("艮", "巽", "坤", "乾"):
        assert FIRE_STAGES.get(sector) is None


def test_intrinsic_elements_are_separate_from_mode_b_palace_element():
    assert INTRINSIC_WX == {
        "太乙": "木",
        "始击": "火",
        "文昌": "土",
        "主大将": "金",
        "主参将": "水",
        "客大将": "水",
        "客参将": "木",
    }
    assert intrinsic_element("主大将") == "金"

    # 主大将若实际在8宫，Mode B主体必须取8宫坎水，而不是固有金。
    mode_b = general_palace_qi(8, "卯")
    assert mode_b["model"] == "B"
    assert mode_b["palace_element"] == "水"
    assert mode_b["subject"] == "水"
    assert mode_b["environment"] == "木"
    assert mode_b["state"] == "休"


def test_common_terminology_catalog_matches_runtime_tables():
    data = _catalog()
    by_key = {entry["key"]: entry for entry in data["entries"]}

    palace_table = by_key["taiyi_nine_palaces"]["palaces"]
    for palace, (trigram, sector, element, yin_yang) in EXPECTED_PALACES.items():
        assert palace_table[str(palace)] == {
            "trigram": trigram,
            "representative_sector": sector,
            "element": element,
            "yin_yang": yin_yang,
        }

    assert {
        row["sector"]: (row["god"], row["element"])
        for row in by_key["sixteen_gods"]["table"]
    } == {
        sector: (god, element)
        for sector, god, element in EXPECTED_GODS
    }

    assert by_key["lushen_shift"]["mapping"] == EXPECTED_LUSHEN_SHIFT
    assert by_key["five_element_qi"]["state_matrix"] == EXPECTED_QI
    assert by_key["intrinsic_vs_palace_element"]["intrinsic_elements"] == INTRINSIC_WX


def test_d8_and_t7_catalogs_reference_common_core():
    d8 = json.loads(Path("terminology/d8-eight-divinations.json").read_text(encoding="utf-8"))
    t7 = json.loads(Path("terminology/t7-seven-methods.json").read_text(encoding="utf-8"))

    for catalog in (d8, t7):
        assert catalog["shared_catalog"] == "terminology/common-core.json"
        assert "R-QI" in catalog["shared_rule_refs"]
        assert "R-9" in catalog["shared_rule_refs"]
        assert "R-16" in catalog["shared_rule_refs"]
