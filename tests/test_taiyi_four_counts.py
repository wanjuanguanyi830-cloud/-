import json
from pathlib import Path

import pytest

from kintaiyi.taiyi_four_counts import (
    entry_context_from_accumulated_count,
    four_count_core_from_entry_count,
    resolve_four_count_dun,
)


FIXTURE = Path(__file__).parent / "fixtures" / "g6_72ju_paths.json"


@pytest.mark.parametrize("kind", ["岁计", "月计", "日计"])
def test_year_month_day_are_source_fixed_to_yang(kind):
    data = resolve_four_count_dun(kind)
    assert data["dun"] == "阳"
    assert data["solstice_half"] is None

    with pytest.raises(ValueError):
        resolve_four_count_dun(kind, solstice_half="夏至后")


def test_time_count_switches_only_at_solstice_half():
    assert resolve_four_count_dun("时计", solstice_half="冬至后")["dun"] == "阳"
    assert resolve_four_count_dun("时计", solstice_half="夏至后")["dun"] == "阴"

    with pytest.raises(ValueError):
        resolve_four_count_dun("时计")


def test_four_count_first_entry_profiles():
    year = four_count_core_from_entry_count(1, count_type="岁计")
    assert (year["taiyi_palace"], year["wenchang_sector"], year["jishen_sector"]) == (
        1, "申", "寅"
    )

    time_yin = four_count_core_from_entry_count(
        1,
        count_type="时计",
        solstice_half="夏至后",
    )
    assert (
        time_yin["taiyi_palace"],
        time_yin["wenchang_sector"],
        time_yin["jishen_sector"],
    ) == (9, "寅", "申")


def test_four_count_yang_profile_matches_full_yang_72_fixture():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    mismatches = []
    for row in fixture["yang"]:
        got = four_count_core_from_entry_count(
            row["ju"],
            count_type="岁计",
        )
        checks = [
            ("太乙", got["taiyi_palace"], row["taiyi_palace"]),
            ("文昌", got["wenchang_sector"], row["host_eye"]),
            ("始击", got["shiji_sector"], row["guest_eye"]),
            ("主算", got["host_calc"], row["host_calc"]),
            ("客算", got["guest_calc"], row["guest_calc"]),
        ]
        for name, actual, expected in checks:
            if actual != expected:
                mismatches.append((row["ju"], name, actual, expected))
    assert mismatches == []


def test_four_count_summer_time_profile_matches_full_yin_72_fixture():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    mismatches = []
    for row in fixture["yin"]:
        got = four_count_core_from_entry_count(
            row["ju"],
            count_type="时计",
            solstice_half="夏至后",
        )
        checks = [
            ("太乙", got["taiyi_palace"], row["taiyi_palace"]),
            ("文昌", got["wenchang_sector"], row["host_eye"]),
            ("始击", got["shiji_sector"], row["guest_eye"]),
            ("主算", got["host_calc"], row["host_calc"]),
            ("客算", got["guest_calc"], row["guest_calc"]),
        ]
        for name, actual, expected in checks:
            if actual != expected:
                mismatches.append((row["ju"], name, actual, expected))
    assert mismatches == []


def test_accumulated_count_entry_decomposition():
    data = entry_context_from_accumulated_count(121, count_type="岁计")
    assert data["remainder_360"] == 121
    assert data["ji_index_1based"] == 3
    assert data["count_in_ji"] == 1
    assert data["yuan_index_1based"] == 2
    assert data["local_ju"] == 49

    end = entry_context_from_accumulated_count(360, count_type="日计")
    assert end["remainder_360"] == 360
    assert end["local_ju"] == 72
