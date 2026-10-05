import json
from pathlib import Path

from kintaiyi import taiyi_rules
from kintaiyi.state_spirit_cycles import TWELVE_PALACES


ROOT = Path(__file__).parents[1]
PALACE_FILE = ROOT / "terminology" / "palace_coordinates.json"
SPIRIT_FILE = ROOT / "terminology" / "sixteen_spirits.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_recovered_sixteen_spirits_match_current_canonical_positions():
    data = _load(SPIRIT_FILE)
    assert data["recovery"]["from_branch"] == "codex/taiyi-base-motion-2026-10-04"
    assert len(data["spirits"]) == 16
    for row in data["spirits"]:
        assert taiyi_rules.GOD_POSITION[row["spirit"]] == row["branch"]


def test_recovered_sixteen_spirit_nine_palaces_match_current_geometry():
    data = _load(SPIRIT_FILE)
    expected = dict(zip(
        taiyi_rules.SIXTEEN,
        (8, 3, 3, 4, 4, 9, 9, 2, 2, 7, 7, 6, 6, 1, 1, 8),
    ))
    for row in data["spirits"]:
        assert row["nine_palace"] == expected[row["branch"]]


def test_recovered_running_palace_order_matches_c64_twelve_palaces():
    data = _load(PALACE_FILE)
    order = data["coordinate_spaces"]["running_palace"]["order"]
    expected = ["乾", "离", "艮", "震", "中", "兑", "坤", "坎", "巽", "绛宫", "明堂", "玉堂"]
    assert order == expected
    assert list(TWELVE_PALACES[:9]) == list(range(1, 10))
    assert list(TWELVE_PALACES[9:]) == ["绛宫", "明堂", "玉堂"]


def test_recovered_running_palace_unique_spirits_match_current_positions():
    data = _load(PALACE_FILE)
    for row in data["running_palaces"]:
        spirit = row["unique_spirit"]
        if spirit is None:
            assert row["running_palace"] == 5
            continue
        marker_position = row["unique_marker"].split("·", 1)[0]
        assert taiyi_rules.GOD_POSITION[spirit] == marker_position


def test_recovered_terminology_assets_are_not_formula_sources():
    for path in (PALACE_FILE, SPIRIT_FILE):
        data = _load(path)
        assert data["status"] == "terminology_reference_not_formula_source"
        assert data["recovery"]["status"] == "recovered_prior_work_crosschecked"
