import json
from pathlib import Path

import pytest

from kintaiyi.taiyi_wenchang import (
    YANG_WENCHANG_18,
    YIN_WENCHANG_18,
    wenchang_from_entry_count,
    wenchang_from_ju,
)


FIXTURE = Path(__file__).parent / "fixtures" / "g6_72ju_paths.json"


def test_g3_exact_18_cycles():
    assert YANG_WENCHANG_18 == (
        "申", "酉", "戌", "乾", "乾", "亥", "子", "丑", "艮",
        "寅", "卯", "辰", "巽", "巳", "午", "未", "坤", "坤",
    )
    assert YIN_WENCHANG_18 == (
        "寅", "卯", "辰", "巽", "巽", "巳", "午", "未", "坤",
        "申", "酉", "戌", "乾", "亥", "子", "丑", "艮", "艮",
    )


@pytest.mark.parametrize(
    ("dun", "ju", "expected"),
    [
        ("阳", 1, "申"),
        ("阳", 4, "乾"),
        ("阳", 5, "乾"),
        ("阳", 17, "坤"),
        ("阳", 18, "坤"),
        ("阳", 19, "申"),
        ("阴", 1, "寅"),
        ("阴", 4, "巽"),
        ("阴", 5, "巽"),
        ("阴", 17, "艮"),
        ("阴", 18, "艮"),
        ("阴", 19, "寅"),
    ],
)
def test_g3_hold_points_and_18_repeat(dun, ju, expected):
    assert wenchang_from_ju(ju, dun=dun)["wenchang_sector"] == expected


def test_g3_remainder_zero_is_eighteenth_position():
    yang = wenchang_from_entry_count(18, dun="阳")
    yin = wenchang_from_entry_count(36, dun="阴")
    assert yang["remainder_18"] == 18
    assert yang["wenchang_sector"] == "坤"
    assert yin["remainder_18"] == 18
    assert yin["wenchang_sector"] == "艮"


def test_g3_full_yinyang_72ju_matches_collated_fixture():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    mismatches = []

    for dun, rows in (("阳", fixture["yang"]), ("阴", fixture["yin"])):
        for row in rows:
            got = wenchang_from_ju(row["ju"], dun=dun)
            if got["wenchang_sector"] != row["host_eye"]:
                mismatches.append(
                    (dun, row["ju"], got["wenchang_sector"], row["host_eye"])
                )

    assert mismatches == []


def test_g3_all_four_18_blocks_repeat_exactly():
    for dun in ("阳", "阴"):
        first = [wenchang_from_ju(i, dun=dun)["wenchang_sector"] for i in range(1, 19)]
        for block in range(4):
            got = [
                wenchang_from_ju(block * 18 + i, dun=dun)["wenchang_sector"]
                for i in range(1, 19)
            ]
            assert got == first
