import json
from pathlib import Path

from kintaiyi.taiyi_calculations import calc_from_eye
from kintaiyi.taiyi_rules import PALACE_POINT, sector_to_nine_palace


FIXTURE = Path(__file__).parent / "fixtures" / "g6_72ju_paths.json"


def _load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_g6_full_yinyang_72ju_host_guest_calcs_match():
    data = _load()
    mismatches = []

    for dun, rows in (("阳", data["yang"]), ("阴", data["yin"])):
        assert len(rows) == 72
        for row in rows:
            host = calc_from_eye(row["taiyi_palace"], row["host_eye"], side="主")
            guest = calc_from_eye(row["taiyi_palace"], row["guest_eye"], side="客")
            if host["calc_value"] != row["host_calc"]:
                mismatches.append(
                    (dun, row["ju"], "主", host["calc_value"], row["host_calc"])
                )
            if guest["calc_value"] != row["guest_calc"]:
                mismatches.append(
                    (dun, row["ju"], "客", guest["calc_value"], row["guest_calc"])
                )

    assert mismatches == []


def test_g6_full_72ju_same_palace_boundaries():
    data = _load()
    interval_cases = []
    positive_cases = []

    for dun, rows in (("阳", data["yang"]), ("阴", data["yin"])):
        for row in rows:
            for side, eye, expected in (
                ("主", row["host_eye"], row["host_calc"]),
                ("客", row["guest_eye"], row["guest_calc"]),
            ):
                if sector_to_nine_palace(eye) != row["taiyi_palace"]:
                    continue
                if eye == PALACE_POINT[row["taiyi_palace"]]:
                    positive_cases.append((dun, row["ju"], side, expected))
                    assert expected == row["taiyi_palace"]
                else:
                    interval_cases.append((dun, row["ju"], side, expected))
                    assert expected == 1

    # 阴43/44按G5公式与《武经总要》《太乙秘书》校回大神/大武后。
    assert len(interval_cases) == 22
    assert len(positive_cases) == 20


def test_g6_non_same_palace_paths_stop_at_taiyi_without_counting_terminal():
    data = _load()
    for rows in (data["yang"], data["yin"]):
        for row in rows:
            for side, eye in (("主", row["host_eye"]), ("客", row["guest_eye"])):
                result = calc_from_eye(row["taiyi_palace"], eye, side=side)
                if result["same_palace"]:
                    continue
                terminal = result["path"][-1]
                assert terminal["role"] == "taiyi_terminal"
                assert terminal["sector"] == PALACE_POINT[row["taiyi_palace"]]
                assert terminal["counted"] is False
                assert terminal["value"] == 0


def test_g6_fixture_preserves_source_corrections_and_one_open_witness_conflict():
    data = _load()
    corrections = data["provenance"]["calc_corrections"]
    assert {(x["dun"], x["ju"], x["side"], x["to"]) for x in corrections} == {
        ("阳", 44, "主", 33),
        ("阴", 10, "客", 34),
        ("阴", 39, "主", 37),
        ("阴", 61, "客", 12),
    }

    reviewed = [
        (dun, row["ju"], row["witness_status"])
        for dun, rows in (("阳", data["yang"]), ("阴", data["yin"]))
        for row in rows
        if row["witness_status"] != "resolved"
    ]
    assert reviewed == [
        ("阴", 37, "parallel_witnesses_support_regression_reading"),
        ("阴", 43, "resolved_by_parallel_witnesses"),
        ("阴", 44, "resolved_by_parallel_witnesses"),
    ]
