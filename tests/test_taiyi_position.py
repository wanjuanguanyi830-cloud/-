import json
from pathlib import Path

import pytest

from kintaiyi.taiyi_position import (
    YANG_PALACE_ORDER,
    YIN_PALACE_ORDER,
    taiyi_from_entry_count,
    taiyi_from_ju,
)


FIXTURE = Path(__file__).parent / "fixtures" / "g6_72ju_paths.json"


def test_g2_palace_orders_exclude_center_five():
    assert YANG_PALACE_ORDER == (1, 2, 3, 4, 6, 7, 8, 9)
    assert YIN_PALACE_ORDER == (9, 8, 7, 6, 4, 3, 2, 1)
    assert 5 not in YANG_PALACE_ORDER
    assert 5 not in YIN_PALACE_ORDER


@pytest.mark.parametrize(
    ("dun", "ju", "palace", "count_in_palace"),
    [
        ("阳", 1, 1, 1),
        ("阳", 3, 1, 3),
        ("阳", 4, 2, 1),
        ("阳", 22, 9, 1),
        ("阳", 24, 9, 3),
        ("阳", 25, 1, 1),
        ("阴", 1, 9, 1),
        ("阴", 3, 9, 3),
        ("阴", 4, 8, 1),
        ("阴", 22, 1, 1),
        ("阴", 24, 1, 3),
        ("阴", 25, 9, 1),
    ],
)
def test_g2_three_counts_per_palace_and_24_repeat(dun, ju, palace, count_in_palace):
    data = taiyi_from_ju(ju, dun=dun)
    assert data["taiyi_palace"] == palace
    assert data["count_in_palace"] == count_in_palace


def test_g2_remainder_zero_is_24th_count():
    data = taiyi_from_entry_count(24, dun="阳")
    assert data["remainder_24"] == 24
    assert data["taiyi_palace"] == 9
    assert data["count_in_palace"] == 3


def test_g2_full_yinyang_72ju_matches_collated_fixture():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    mismatches = []

    for dun, rows in (("阳", fixture["yang"]), ("阴", fixture["yin"])):
        for row in rows:
            got = taiyi_from_ju(row["ju"], dun=dun)
            if got["taiyi_palace"] != row["taiyi_palace"]:
                mismatches.append(
                    (dun, row["ju"], got["taiyi_palace"], row["taiyi_palace"])
                )

    assert mismatches == []


def test_g2_all_three_24_blocks_repeat():
    for dun in ("阳", "阴"):
        first = [taiyi_from_ju(i, dun=dun)["taiyi_palace"] for i in range(1, 25)]
        for block in range(3):
            got = [
                taiyi_from_ju(block * 24 + i, dun=dun)["taiyi_palace"]
                for i in range(1, 25)
            ]
            assert got == first
