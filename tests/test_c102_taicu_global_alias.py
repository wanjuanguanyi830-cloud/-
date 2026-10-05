import json
from pathlib import Path

from kintaiyi.taiyi_rules import GODS, GOD_ALIASES, SIXTEEN_GOD_WX, position


ROOT = Path(__file__).resolve().parents[1]
TERMINOLOGY = ROOT / "terminology" / "sixteen_spirits.json"


def test_c102_taicu_traditional_variant_normalizes_globally():
    assert "太簇" in GODS
    assert "太蔟" not in GODS
    assert GOD_ALIASES["太蔟"] == "太簇"
    assert position("太蔟") == "酉"
    assert position("太簇") == "酉"
    assert SIXTEEN_GOD_WX["太簇"] == "金"


def test_c102_sixteen_spirit_catalog_uses_taicu_as_single_canonical():
    data = json.loads(TERMINOLOGY.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.3.0"

    spirits = [row["spirit"] for row in data["spirits"]]
    assert spirits.count("太簇") == 1
    assert "太蔟" not in spirits

    aliases = {row["alias"]: row for row in data["aliases"]}
    assert aliases["太蔟"]["canonical_name"] == "太簇"
    assert aliases["太蔟"]["status"] == "dictionary_attested_traditional_variant"

    policy = data["canonical_glyph_policy"]["太簇"]
    assert policy["canonical_name"] == "太簇"
    assert policy["accepted_variants"] == ["太簇", "太蔟"]
