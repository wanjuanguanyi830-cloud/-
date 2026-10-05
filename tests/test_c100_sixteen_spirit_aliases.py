import json
from pathlib import Path

import pytest

from kintaiyi.eight_divinations import attack_realm
from kintaiyi.taiyi_rules import GOD_ALIASES, position


ROOT = Path(__file__).resolve().parents[1]
TERMINOLOGY = ROOT / "terminology" / "sixteen_spirits.json"


@pytest.mark.parametrize(
    "alias,canonical,sector",
    [
        ("陽德", "阳德", "丑"),
        ("呂申", "吕申", "寅"),
        ("高叢", "高丛", "卯"),
        ("太陽", "太阳", "辰"),
        ("陰主", "阴主", "戌"),
        ("陰德", "阴德", "乾"),
        ("大義", "大义", "亥"),
        ("太炅", "大炅", "巽"),
        ("太神", "大神", "巳"),
        ("大旲", "大炅", "巽"),
    ],
)
def test_c100_glyph_aliases_normalize_to_existing_canonical_spirits(alias, canonical, sector):
    assert GOD_ALIASES[alias] == canonical
    assert position(alias) == sector
    assert position(canonical) == sector


def test_c100_attack_realm_accepts_recovered_traditional_glyphs_without_new_formula():
    simplified = attack_realm("阴德")
    traditional = attack_realm("陰德")
    assert traditional == simplified

    simplified = attack_realm("大义")
    traditional = attack_realm("大義")
    assert traditional == simplified


def test_c100_terminology_catalog_matches_runtime_aliases():
    data = json.loads(TERMINOLOGY.read_text(encoding="utf-8"))
    aliases = {row["alias"]: row["canonical_name"] for row in data["aliases"]}
    for alias, canonical in GOD_ALIASES.items():
        assert aliases[alias] == canonical
    assert data["schema_version"] == "1.3.0"  # C102 adds 太蔟→太簇 global alias
    assert data["recovery"]["additional_oct4_source"]["path"] == (
        "rules/common/taiyi_space.py"
    )
    assert data["recovery"]["additional_oct4_source"]["status"] == (
        "recovered_glyph_aliases_only"
    )
