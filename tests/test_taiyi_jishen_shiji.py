import json
from pathlib import Path

import pytest

from kintaiyi.taiyi_jishen_shiji import (
    g4_g5_from_ju,
    jishen_from_taisui,
    shiji_from_jishen_wenchang,
    shiji_from_taisui_wenchang,
)


FIXTURE = Path(__file__).parent / "fixtures" / "g6_72ju_paths.json"


@pytest.mark.parametrize(
    ("dun", "taisui", "expected"),
    [
        ("阳", "子", "寅"),
        ("阳", "丑", "丑"),
        ("阳", "寅", "子"),
        ("阳", "亥", "卯"),
        ("阴", "子", "申"),
        ("阴", "丑", "未"),
        ("阴", "寅", "午"),
        ("阴", "亥", "酉"),
    ],
)
def test_g4_jishen_reverse_twelve_branches(dun, taisui, expected):
    assert jishen_from_taisui(taisui, dun=dun)["jishen_sector"] == expected


def test_g5_plate_rotation_example_yang_1():
    # 阳1：计神寅加和德艮；文昌武德/申随盘落坤，即始击大武。
    data = shiji_from_jishen_wenchang(jishen="寅", wenchang="武德")
    assert data["hede_sector"] == "艮"
    assert data["check"]["jishen_lands_on_hede"] is True
    assert data["wenchang_sector"] == "申"
    assert data["shiji_sector"] == "坤"
    assert data["shiji_god"] == "大武"


def test_g4_g5_chain_yang_31_produces_yinzhu_xu():
    data = g4_g5_from_ju(ju=31, dun="阳", wenchang="大炅")
    assert data["taisui_branch"] == "午"
    assert data["jishen_sector"] == "申"
    assert data["shiji_sector"] == "戌"
    assert data["shiji_god"] == "阴主"


def test_g5_full_yinyang_72ju_matches_collated_guest_eye_fixture():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    mismatches = []

    for dun, rows in (("阳", fixture["yang"]), ("阴", fixture["yin"])):
        for row in rows:
            data = g4_g5_from_ju(
                ju=row["ju"],
                dun=dun,
                wenchang=row["host_eye"],
            )
            if data["shiji_sector"] != row["guest_eye"]:
                mismatches.append(
                    (
                        dun,
                        row["ju"],
                        data["jishen_sector"],
                        row["host_eye"],
                        data["shiji_sector"],
                        row["guest_eye"],
                    )
                )

    assert mismatches == []


def test_g5_yin_43_44_follow_formula_and_parallel_witnesses():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    row43 = fixture["yin"][42]
    row44 = fixture["yin"][43]

    got43 = g4_g5_from_ju(ju=43, dun="阴", wenchang=row43["host_eye"])
    got44 = g4_g5_from_ju(ju=44, dun="阴", wenchang=row44["host_eye"])

    assert (got43["jishen_sector"], got43["shiji_sector"], row43["guest_calc"]) == (
        "寅",
        "巳",
        1,
    )
    assert (got44["jishen_sector"], got44["shiji_sector"], row44["guest_calc"]) == (
        "丑",
        "坤",
        38,
    )
