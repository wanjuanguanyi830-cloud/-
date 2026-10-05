import json
from pathlib import Path

from kintaiyi.taiyi_core_chain import g2_to_g7_from_ju, g3_to_g7_from_ju, g4_to_g7_from_ju


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
