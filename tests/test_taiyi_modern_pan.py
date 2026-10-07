from datetime import datetime
from zoneinfo import ZoneInfo

from kintaiyi.pan_v2 import validate_pan_v2
from kintaiyi.taiyi_modern_pan import build_modern_pan_v2


TZ = ZoneInfo("Asia/Shanghai")
MOMENT = datetime(2026, 3, 24, 12, 30, tzinfo=TZ)


def test_modern_pan_v2_builds_all_supported_count_types():
    for kind in ("岁计", "月计", "日计", "时计", "分计"):
        pan = build_modern_pan_v2(MOMENT, count_type=kind)
        assert pan["schema_version"] == "2.0"
        assert pan["meta"]["count_type"] == kind
        assert pan["meta"]["calendar_mode"] == "production_modern"
        assert validate_pan_v2(pan)["valid"] is True


def test_modern_pan_v2_board_contains_core_generated_facts():
    pan = build_modern_pan_v2(MOMENT, count_type="日计")
    assert pan["board"]["taiyi"]["palace"] in {1, 2, 3, 4, 6, 7, 8, 9}
    assert pan["board"]["eyes"]["skyeyes"]["sector"] is not None
    assert pan["board"]["eyes"]["shiji"]["sector"] is not None
    assert pan["board"]["calculations"]["host"]["value"] >= 1
    assert pan["board"]["calculations"]["guest"]["value"] >= 1


def test_time_pan_v2_exposes_c119_direct_door_only_for_time_count():
    time_pan = build_modern_pan_v2(MOMENT, count_type="时计")
    year_pan = build_modern_pan_v2(MOMENT, count_type="岁计")
    minute_pan = build_modern_pan_v2(MOMENT, count_type="分计")

    assert time_pan["board"]["doors"]["direct"]["door"] in {
        "开", "生", "惊", "休", "杜", "死", "伤", "景"
    }
    assert year_pan["board"]["doors"] == {}
    assert minute_pan["board"]["doors"] == {}


def test_modern_pan_v2_calendar_is_json_safe_iso_datetime():
    pan = build_modern_pan_v2(MOMENT, count_type="月计")
    assert pan["calendar"]["input_moment"].endswith("+08:00")
    assert isinstance(pan["calendar"]["year_boundary"]["taiyi_year_start_utc"], str)
    assert isinstance(pan["calendar"]["solar_month"]["month_start_utc"], str)


def test_modern_pan_v2_keeps_taiyi_year_and_lunar_year_separate():
    moment = datetime(2027, 1, 1, 12, tzinfo=TZ)
    pan = build_modern_pan_v2(moment, count_type="岁计")

    assert pan["calendar"]["taiyi_year"] == 2027
    assert pan["calendar"]["lunar"]["year"] == 2026


def test_modern_pan_v2_scenario_remains_explicit():
    pan = build_modern_pan_v2(
        MOMENT,
        count_type="日计",
        scenario={"enemy_camp_day_taiyi_palace": 3},
    )
    assert pan["meta"]["scenario"]["enemy_camp_day_taiyi_palace"] == 3



def test_modern_pan_v2_declares_winter_solstice_as_unique_year_boundary():
    pan = build_modern_pan_v2(MOMENT, count_type="岁计")
    policy = pan["calendar"]["year_boundary_policy"]
    assert policy["unique_boundary"] == "真实天文冬至交节瞬间"
    assert "Y+1" in policy["label_rule"]
    assert policy["ignored_boundaries"] == ["元旦", "春节", "立春", "春分"]


def test_modern_pan_v2_year_switches_at_exact_winter_solstice():
    from datetime import timedelta
    from kintaiyi.taiyi_modern_calendar import winter_solstice_utc

    boundary = winter_solstice_utc(2026)
    before = build_modern_pan_v2(
        boundary - timedelta(microseconds=1),
        count_type="岁计",
    )
    exact = build_modern_pan_v2(
        boundary,
        count_type="岁计",
    )

    assert before["calendar"]["taiyi_year"] == 2026
    assert exact["calendar"]["taiyi_year"] == 2027
    assert (
        exact["calendar"]["year_boundary_policy"]["taiyi_year_start_utc"]
        == boundary.isoformat()
    )


def test_modern_pan_v2_new_year_day_does_not_change_taiyi_year_again():
    from datetime import datetime
    from zoneinfo import ZoneInfo

    tz = ZoneInfo("Asia/Shanghai")
    dec31 = build_modern_pan_v2(
        datetime(2026, 12, 31, 12, tzinfo=tz),
        count_type="岁计",
    )
    jan1 = build_modern_pan_v2(
        datetime(2027, 1, 1, 12, tzinfo=tz),
        count_type="岁计",
    )
    assert dec31["calendar"]["taiyi_year"] == 2027
    assert jan1["calendar"]["taiyi_year"] == 2027



def test_pan_v2_validator_rejects_modern_payload_without_winter_solstice_policy():
    pan = build_modern_pan_v2(MOMENT, count_type="岁计")
    broken = dict(pan)
    broken["calendar"] = dict(pan["calendar"])
    broken["calendar"].pop("year_boundary_policy")
    validation = validate_pan_v2(broken)
    assert validation["valid"] is False
    assert "modern production缺calendar.year_boundary_policy" in validation["errors"]


def test_pan_v2_validator_rejects_non_winter_solstice_modern_year_boundary():
    pan = build_modern_pan_v2(MOMENT, count_type="岁计")
    broken = dict(pan)
    broken["calendar"] = dict(pan["calendar"])
    broken["calendar"]["year_boundary_policy"] = dict(
        pan["calendar"]["year_boundary_policy"]
    )
    broken["calendar"]["year_boundary_policy"]["unique_boundary"] = "立春"
    validation = validate_pan_v2(broken)
    assert validation["valid"] is False
    assert "modern production太乙岁界必须为真实天文冬至交节瞬间" in validation["errors"]



def test_modern_pan_v2_exposes_boundary_registry():
    pan = build_modern_pan_v2(MOMENT, count_type="岁计")
    registry = pan["calendar"]["boundary_registry"]
    assert registry["taiyi_year"]["boundary"] == "真实天文冬至交节瞬间"
    assert registry["gregorian_year"]["canonical_for_taiyi_year"] is False
    assert registry["lunar_year"]["canonical_for_taiyi_year"] is False
    assert registry["jieqi_ganzhi_year"]["canonical_for_taiyi_year"] is False
    assert registry["spring_equinox"]["canonical_for_taiyi_year"] is False



def test_modern_pan_v2_daxue_month_does_not_advance_taiyi_year():
    from kintaiyi.taiyi_modern_solar_month import jie_instant_utc
    from kintaiyi.taiyi_modern_calendar import winter_solstice_utc

    daxue = jie_instant_utc(2026, "大雪")
    winter = winter_solstice_utc(2026)
    probe = daxue + (winter - daxue) / 2

    pan = build_modern_pan_v2(probe, count_type="月计")
    assert pan["calendar"]["solar_month"]["month_build_branch"] == "子"
    assert pan["calendar"]["selected_count"]["month_formula_year"] == 2027
    assert pan["calendar"]["taiyi_year"] == 2026


def test_modern_pan_v2_winter_solstice_advances_taiyi_year_without_new_month():
    from kintaiyi.taiyi_modern_calendar import winter_solstice_utc

    winter = winter_solstice_utc(2026)
    pan = build_modern_pan_v2(winter, count_type="月计")
    assert pan["calendar"]["solar_month"]["month_build_branch"] == "子"
    assert pan["calendar"]["selected_count"]["month_formula_year"] == 2027
    assert pan["calendar"]["taiyi_year"] == 2027


def test_minute_pan_changes_on_the_next_absolute_minute():
    from datetime import timedelta

    first = build_modern_pan_v2(MOMENT, count_type="分计")
    second = build_modern_pan_v2(MOMENT + timedelta(minutes=1), count_type="分计")

    a = first["calendar"]["selected_count"]["entry_count"]
    b = second["calendar"]["selected_count"]["entry_count"]
    assert b == a + 1
    assert first["meta"]["count_type"] == "分计"
    assert second["meta"]["count_type"] == "分计"


def test_minute_alias_is_accepted():
    traditional = build_modern_pan_v2(MOMENT, count_type="分計")
    simplified = build_modern_pan_v2(MOMENT, count_type="分计")
    assert traditional == simplified
