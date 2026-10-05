from collections import Counter

import pytest

from kintaiyi.snapshot_collection import (
    BOUNDARY,
    CORE_METHODS,
    RECOVERY,
    c95_catalog,
    collect_core_snapshot,
    validate_snapshot_selection,
)


class Engine:
    def __init__(self):
        self.calls = Counter()

    def _hit(self, name, style):
        self.calls[(name, style)] += 1

    def accnum(self, style, profile):
        self._hit("accnum", style)
        return 10154821 if style == 0 else 900 + style

    def ty(self, style, profile):
        self._hit("ty", style)
        return 3 if style == 2 else 7

    def __getattr__(self, name):
        if name not in CORE_METHODS.values():
            raise AttributeError(name)

        def method(style, profile):
            self._hit(name, style)
            if name in ("skyeyes", "sf", "se"):
                return "辰"
            return 6

        return method


def test_c95_collector_uses_explicit_year_and_day_styles():
    engine = Engine()
    data = collect_core_snapshot(engine, 1, 0)
    assert data["accumulated_year"] == 901
    assert data["year_accumulated_year"] == 10154821
    assert data["taiyi_palace"] == 7
    assert data["day_taiyi_palace"] == 3
    assert data["ji_style"] == 1


def test_c95_current_year_and_day_style_do_not_double_call_same_primitive():
    year_engine = Engine()
    year = collect_core_snapshot(year_engine, 0, 0)
    assert year["year_accumulated_year"] == year["accumulated_year"]
    assert year_engine.calls[("accnum", 0)] == 1

    day_engine = Engine()
    day = collect_core_snapshot(day_engine, 2, 0)
    assert day["day_taiyi_palace"] == day["taiyi_palace"]
    assert day_engine.calls[("ty", 2)] == 1


def test_c95_each_board_primitive_called_once_for_selected_style():
    engine = Engine()
    collect_core_snapshot(engine, 1, 0)
    for method in CORE_METHODS.values():
        assert engine.calls[(method, 1)] == 1


def test_c95_collector_does_not_build_v2_or_call_rules():
    data = collect_core_snapshot(Engine(), 1, 0)
    assert data["collector_boundary"] == BOUNDARY
    assert data["collector_boundary"]["builds_pan_v2"] is False
    assert data["collector_boundary"]["calls_cycle_rules"] is False
    assert data["collector_boundary"]["calls_analysis_rules"] is False
    assert "v2" not in data
    assert "analysis" not in data
    assert "cycles" not in data


def test_c95_selection_validation_preserves_oct4_behavior():
    snapshot = {"ji_style": 1, "taiyi_acumyear": 2}
    checked = validate_snapshot_selection(
        snapshot,
        ji_style=1,
        taiyi_acumyear=2,
    )
    assert checked["selection_matches"] is True

    with pytest.raises(ValueError, match="ji_style"):
        validate_snapshot_selection(
            snapshot,
            ji_style=0,
            taiyi_acumyear=2,
        )
    with pytest.raises(ValueError, match="taiyi_acumyear"):
        validate_snapshot_selection(
            snapshot,
            ji_style=1,
            taiyi_acumyear=3,
        )


@pytest.mark.parametrize(
    "style,profile",
    [(True, 0), (5, 0), (0, 4), (0, False)],
)
def test_c95_selection_rejects_bool_and_out_of_range(style, profile):
    with pytest.raises((TypeError, ValueError)):
        collect_core_snapshot(Engine(), style, profile)


def test_c95_recovery_only_uses_oct4_oct5_work():
    assert RECOVERY["time_window_policy"] == (
        "only_2026-10-04_and_2026-10-05_prior_work"
    )
    assert all(item["date"].startswith("2026-10-04") for item in RECOVERY["relevant_commits"])
    assert "Taiyi(snapshot).pan旧聚合路径" in RECOVERY["not_recovered"]


def test_c95_catalog_marks_raw_snapshot_boundary():
    data = c95_catalog()
    assert data["boundary"]["output"] == "raw_core_snapshot"
    assert data["boundary"]["next_layer"].startswith("C30")
