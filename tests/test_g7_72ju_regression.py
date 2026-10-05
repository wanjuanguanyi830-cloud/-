import json
from pathlib import Path

from kintaiyi.taiyi_generals import host_guest_generals


FIXTURE = Path(__file__).parent / "fixtures" / "g7_72ju_calc_pairs.json"


def _load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_g7_full_yinyang_72ju_regression_counts_and_ranges():
    data = _load()
    counts = {
        "total_sides": 0,
        "blocked_5_15_25_35": 0,
        "exact_10": 0,
        "exact_20": 0,
        "exact_30": 0,
        "exact_40": 0,
        "ordinary_nonblocked": 0,
    }

    for rows in (data["yang"], data["yin"]):
        assert len(rows) == 72
        for row in rows:
            host_calc, guest_calc = row[:2]
            result = host_guest_generals(host_calc, guest_calc)
            for calc_value, side in (
                (host_calc, result["host"]),
                (guest_calc, result["guest"]),
            ):
                counts["total_sides"] += 1
                if calc_value in {5, 15, 25, 35}:
                    counts["blocked_5_15_25_35"] += 1
                    assert side["blocked"] is True
                    assert side["big_general_palace"] is None
                    assert side["assistant_general_palace"] is None
                    assert side["five_generals_released"] is False
                else:
                    assert side["blocked"] is False
                    assert 1 <= side["big_general_palace"] <= 9
                    assert 1 <= side["assistant_general_palace"] <= 9
                    if calc_value == 10:
                        counts["exact_10"] += 1
                    elif calc_value == 20:
                        counts["exact_20"] += 1
                    elif calc_value == 30:
                        counts["exact_30"] += 1
                    elif calc_value == 40:
                        counts["exact_40"] += 1
                    else:
                        counts["ordinary_nonblocked"] += 1

    assert counts == data["expected_counts"]


def test_g7_full_72ju_exact_tens_regression():
    data = _load()
    observed = {10: set(), 20: set(), 30: set(), 40: set()}

    for rows in (data["yang"], data["yin"]):
        for host_calc, guest_calc, *_ in rows:
            result = host_guest_generals(host_calc, guest_calc)
            for calc_value, side in (
                (host_calc, result["host"]),
                (guest_calc, result["guest"]),
            ):
                if calc_value in observed:
                    observed[calc_value].add(
                        (side["big_general_palace"], side["assistant_general_palace"])
                    )

    assert observed[10] == {(1, 3)}
    assert observed[20] == set()  # 144局主客算中没有20，靠卷二正文覆盖。
    assert observed[30] == {(3, 9)}
    assert observed[40] == {(4, 2)}


def test_g7_regression_fixture_keeps_four_source_corrected_calc_cells():
    data = _load()
    assert data["yang"][43][0] == 33
    assert data["yin"][9][1] == 34
    assert data["yin"][38][0] == 37
    assert data["yin"][60][1] == 12
