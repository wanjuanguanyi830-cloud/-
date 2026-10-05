import json
from pathlib import Path

from kintaiyi.taiyi_core_chain import (
    l0_to_g7_from_historical_year,
    year_count_from_accumulated_year,
    year_count_from_historical_year,
    g1_to_g7_from_accumulated_year,
    g2_to_g7_from_ju,
    g3_to_g7_from_ju,
    g4_to_g7_from_ju,
)


FIXTURE = Path(__file__).parent / "fixtures" / "g6_72ju_paths.json"


def test_g4_to_g7_full_72ju_core_chain_matches_calcs():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    mismatches = []

    for dun, rows in (("阳", fixture["yang"]), ("阴", fixture["yin"])):
        for row in rows:
            data = g4_to_g7_from_ju(
                ju=row["ju"],
                dun=dun,
                taiyi_palace=row["taiyi_palace"],
                wenchang=row["host_eye"],
            )
            if data["shiji_sector"] != row["guest_eye"]:
                mismatches.append(
                    (dun, row["ju"], "始击", data["shiji_sector"], row["guest_eye"])
                )
            if data["host_calc"] != row["host_calc"]:
                mismatches.append(
                    (dun, row["ju"], "主算", data["host_calc"], row["host_calc"])
                )
            if data["guest_calc"] != row["guest_calc"]:
                mismatches.append(
                    (dun, row["ju"], "客算", data["guest_calc"], row["guest_calc"])
                )

    assert mismatches == []


def test_g4_to_g7_chain_preserves_blockage():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    # 阳4主算25，为杜塞。
    row = fixture["yang"][3]
    data = g4_to_g7_from_ju(
        ju=row["ju"],
        dun="阳",
        taiyi_palace=row["taiyi_palace"],
        wenchang=row["host_eye"],
    )
    assert data["host_calc"] == 25
    assert data["host_blocked"] is True
    assert data["host_big_general_palace"] is None
    assert data["host_assistant_general_palace"] is None


def test_g4_to_g7_chain_yang31_resolves_shiji_and_guest_calc():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    row = fixture["yang"][30]
    data = g4_to_g7_from_ju(
        ju=31,
        dun="阳",
        taiyi_palace=row["taiyi_palace"],
        wenchang=row["host_eye"],
    )
    assert data["jishen_sector"] == "申"
    assert data["shiji_sector"] == "戌"
    assert data["guest_calc"] == 10
    assert data["guest_big_general_palace"] == 1
    assert data["guest_assistant_general_palace"] == 3



def test_g3_to_g7_full_72ju_chain_matches_wenchang_shiji_and_calcs():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    from kintaiyi.taiyi_rules import BRANCHES

    mismatches = []
    for dun, rows in (("阳", fixture["yang"]), ("阴", fixture["yin"])):
        for row in rows:
            taisui_branch = BRANCHES[(row["ju"] - 1) % 12]
            data = g3_to_g7_from_ju(
                ju=row["ju"],
                dun=dun,
                taisui_branch=taisui_branch,
                taiyi_palace=row["taiyi_palace"],
            )
            checks = [
                ("文昌", data["wenchang_sector"], row["host_eye"]),
                ("始击", data["shiji_sector"], row["guest_eye"]),
                ("主算", data["host_calc"], row["host_calc"]),
                ("客算", data["guest_calc"], row["guest_calc"]),
            ]
            for name, got, expected in checks:
                if got != expected:
                    mismatches.append((dun, row["ju"], name, got, expected))

    assert mismatches == []



def test_g2_to_g7_full_72ju_chain_matches_taiyi_wenchang_shiji_and_calcs():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    from kintaiyi.taiyi_rules import BRANCHES

    mismatches = []
    for dun, rows in (("阳", fixture["yang"]), ("阴", fixture["yin"])):
        for row in rows:
            taisui_branch = BRANCHES[(row["ju"] - 1) % 12]
            data = g2_to_g7_from_ju(
                ju=row["ju"],
                dun=dun,
                taisui_branch=taisui_branch,
            )
            checks = [
                ("太乙", data["taiyi_palace"], row["taiyi_palace"]),
                ("文昌", data["wenchang_sector"], row["host_eye"]),
                ("始击", data["shiji_sector"], row["guest_eye"]),
                ("主算", data["host_calc"], row["host_calc"]),
                ("客算", data["guest_calc"], row["guest_calc"]),
            ]
            for name, got, expected in checks:
                if got != expected:
                    mismatches.append((dun, row["ju"], name, got, expected))

    assert mismatches == []



def test_g1_to_g7_full_72ju_first_yuan_matches_fixture():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    mismatches = []

    for dun, rows in (("阳", fixture["yang"]), ("阴", fixture["yin"])):
        for row in rows:
            data = g1_to_g7_from_accumulated_year(
                accumulated_year=row["ju"],
                dun=dun,
            )
            checks = [
                ("局号", data["local_ju"], row["ju"]),
                ("太乙", data["taiyi_palace"], row["taiyi_palace"]),
                ("文昌", data["wenchang_sector"], row["host_eye"]),
                ("始击", data["shiji_sector"], row["guest_eye"]),
                ("主算", data["host_calc"], row["host_calc"]),
                ("客算", data["guest_calc"], row["guest_calc"]),
            ]
            for name, got, expected in checks:
                if got != expected:
                    mismatches.append((dun, row["ju"], name, got, expected))

    assert mismatches == []


def test_g1_to_g7_same_local_ju_is_stable_across_five_yuan():
    # 同局五元年支相同，G2-G7盘面核心应一致；完整干支/五元本身不同。
    snapshots = []
    for accumulated_year in (31, 103, 175, 247, 319):
        data = g1_to_g7_from_accumulated_year(
            accumulated_year=accumulated_year,
            dun="阳",
        )
        snapshots.append(
            (
                data["local_ju"],
                data["taisui_branch"],
                data["taiyi_palace"],
                data["wenchang_sector"],
                data["shiji_sector"],
                data["host_calc"],
                data["guest_calc"],
            )
        )
    assert len(set(snapshots)) == 1


def test_g1_to_g7_kaiyuan_12_anchor_enters_second_yuan_49th_ju():
    data = g1_to_g7_from_accumulated_year(
        accumulated_year=1_937_281,
        dun="阳",
    )
    assert data["taisui_ganzhi"] == "甲子"
    assert data["five_yuan"] == "丙子"
    assert data["local_ju"] == 49



def test_l0_to_g7_kaiyuan_anchor_matches_direct_long_count_chain():
    via_year = l0_to_g7_from_historical_year(
        historical_year=724,
        dun="阳",
    )
    via_count = g1_to_g7_from_accumulated_year(
        accumulated_year=1_937_281,
        dun="阳",
    )

    assert via_year["accumulated_year"] == 1_937_281
    assert via_year["five_zi_short_accumulated_year"] == 30_001
    assert via_year["epoch_equivalent_mod_360"] is True
    assert via_year["taisui_ganzhi"] == "甲子"
    assert via_year["five_yuan"] == "丙子"
    assert via_year["local_ju"] == 49

    for key in (
        "taiyi_palace",
        "wenchang_sector",
        "shiji_sector",
        "host_calc",
        "guest_calc",
        "host_big_general_palace",
        "guest_big_general_palace",
    ):
        assert via_year[key] == via_count[key]


def test_l0_to_g7_2026_enters_expected_cycle_context():
    data = l0_to_g7_from_historical_year(
        historical_year=2026,
        dun="阳",
    )
    assert data["accumulated_year"] == 1_938_583
    assert data["taisui_ganzhi"] == "丙午"
    assert data["six_ji_three_yuan"]["ji_index_1based"] == 6
    assert data["six_ji_three_yuan"]["yuan_label"] == "下元"
    assert data["five_zi_from_long"]["five_zi_yuan"] == "壬子"
    assert data["local_ju"] == 55


def test_l0_to_g7_long_short_epochs_land_same_five_zi_ju():
    for year in (724, 1024, 2026):
        data = l0_to_g7_from_historical_year(
            historical_year=year,
            dun="阳",
        )
        assert (
            data["five_zi_from_long"]["local_ju"]
            == data["five_zi_from_short"]["local_ju"]
            == data["local_ju"]
        )



def test_source_specific_year_count_is_fixed_yang():
    data = year_count_from_accumulated_year(
        accumulated_year=1_937_281,
    )
    assert data["count_type"] == "岁计"
    assert data["dun"] == "阳"
    assert data["taisui_ganzhi"] == "甲子"
    assert data["local_ju"] == 49


def test_source_specific_historical_year_matches_low_level_yang_entry():
    strict = year_count_from_historical_year(historical_year=724)
    low = l0_to_g7_from_historical_year(
        historical_year=724,
        dun="阳",
    )
    for key in (
        "taiyi_palace",
        "wenchang_sector",
        "shiji_sector",
        "host_calc",
        "guest_calc",
        "host_big_general_palace",
        "guest_big_general_palace",
    ):
        assert strict[key] == low[key]
    assert strict["dun"] == "阳"


def test_low_level_historical_year_yin_remains_research_compatibility_only():
    low = l0_to_g7_from_historical_year(
        historical_year=724,
        dun="阴",
    )
    strict = year_count_from_historical_year(historical_year=724)
    assert low["dun"] == "阴"
    assert strict["dun"] == "阳"
    assert "低层" in low["policy"]
    assert "正式岁计" in strict["policy"]
