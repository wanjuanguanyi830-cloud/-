import pytest

from kintaiyi.ten_essences_cloud_observations import (
    C51_BOUNDARY,
    COLOR_TIMING_RULES,
    FLYBIRD_TAIYI_WIND_VARIANT,
    LEGACY_COLOR_AUDIT,
    WEATHER_TEXTURE_RULES,
    c58_catalog,
    initial_move_cloud_timing,
    weather_observation_omens,
)


@pytest.mark.parametrize(
    "color,count,branches",
    [
        ("青", 3, ["寅", "卯"]),
        ("青", 4, ["寅", "卯"]),
        ("白", 7, ["申", "酉"]),
        ("白", 6, ["申", "酉"]),
        ("黑", 1, ["亥", "子"]),
        ("黑", 8, ["亥", "子"]),
    ],
)
def test_c58_primary_color_timing_rules(color, count, branches):
    data = initial_move_cloud_timing(
        cloud_color=color,
        day_time_count=count,
        calculation_scope="日计",
        observation_slot="日出",
    )
    assert data["matched"] is True
    assert data["change_branch_period"] == branches
    assert data["source_status"] == "primary_direct"


def test_c58_red_rule_is_collation_supported_primary_online_gap():
    data = initial_move_cloud_timing(
        cloud_color="赤",
        day_time_count=9,
        calculation_scope="日计",
        observation_slot="日午",
    )
    assert data["matched"] is True
    assert data["change_branch_period"] == ["巳", "午"]
    assert data["source_status"] == "collation_supported_primary_online_gap"
    assert data["witness"]["jinjing"] == "赤色，九二，巳午"
    assert data["witness"]["wujing_zongyao"] == "赤色，九二，巳午"


def test_c58_wrong_count_does_not_guess_period():
    data = initial_move_cloud_timing(
        cloud_color="青",
        day_time_count=9,
        calculation_scope="日计",
        observation_slot="日晡",
    )
    assert data["matched"] is False
    assert data["change_branch_period"] is None
    assert data["status"] == "count_not_matched_by_color_rule"


def test_c58_day_observation_window_only_initial_move_day():
    data = initial_move_cloud_timing(
        cloud_color="白",
        day_time_count=7,
        calculation_scope="日计",
        observation_slot="日出",
        move_offset=1,
    )
    assert data["status"] == "outside_source_observation_window"
    assert data["matched"] is False
    assert data["change_branch_period"] is None


def test_c58_time_observation_window_only_initial_move_time():
    hit = initial_move_cloud_timing(
        cloud_color="黑",
        day_time_count=1,
        calculation_scope="时计",
        observation_slot="初移宫时",
    )
    assert hit["matched"] is True

    later = initial_move_cloud_timing(
        cloud_color="黑",
        day_time_count=1,
        calculation_scope="时计",
        observation_slot="初移宫时",
        move_offset=2,
    )
    assert later["status"] == "outside_source_observation_window"


def test_c58_rejects_wrong_slots():
    with pytest.raises(ValueError, match="日出/日午/日晡"):
        initial_move_cloud_timing(
            cloud_color="青",
            day_time_count=3,
            calculation_scope="日计",
            observation_slot="子时",
        )
    with pytest.raises(ValueError, match="初移宫时"):
        initial_move_cloud_timing(
            cloud_color="青",
            day_time_count=3,
            calculation_scope="时计",
            observation_slot="日出",
        )


def test_c58_legacy_white_mapping_is_explicitly_wrong():
    audit = LEGACY_COLOR_AUDIT["legacy_yunqi_table"]
    assert audit["white_counts"] == [7, 6]
    assert audit["legacy_change_branch_period"] == ["亥", "子"]
    assert audit["canonical_change_branch_period"] == ["申", "酉"]
    assert audit["canonical_equivalent"] is False


def test_c58_legacy_red_label_not_silently_normalized():
    assert LEGACY_COLOR_AUDIT["红"]["canonical_color"] == "赤"
    assert LEGACY_COLOR_AUDIT["红"]["runtime_alias_enabled"] is False
    with pytest.raises(ValueError, match="赤"):
        initial_move_cloud_timing(
            cloud_color="红",
            day_time_count=9,
            calculation_scope="日计",
            observation_slot="日出",
        )


@pytest.mark.parametrize(
    "texture,effects",
    [
        ("纯厚", ["雨"]),
        ("华薄", ["风"]),
        ("黄雾", ["晕"]),
        ("黑赤", ["风"]),
        ("青白", ["寒"]),
        ("凝润", ["雾雨"]),
    ],
)
def test_c58_weather_texture_rules(texture, effects):
    data = weather_observation_omens(weather_texture=texture)
    assert data["matched_omens"][0]["effects"] == effects
    assert data["auto_weather_inference_used"] is False


def test_c58_black_red_and_blue_white_keep_collation_variants():
    blackred = weather_observation_omens(weather_texture="黑赤")
    assert blackred["matched_omens"][0]["witness_variants"]["sancai_shiwei"] == "风热"

    bluewhite = weather_observation_omens(weather_texture="青白")
    assert bluewhite["matched_omens"][0]["witness_variants"]["sancai_shiwei"] == "风寒"


def test_c58_cloud_form_rules_are_external_observation():
    sweep = weather_observation_omens(cloud_form="如扫")
    assert sweep["matched_omens"][0]["effects"] == ["晴"]

    patterned = weather_observation_omens(cloud_form="文彩轮囷萧索")
    item = patterned["matched_omens"][0]
    assert item["effects"] == ["大晴"]
    assert item["witness_variants"]["tongzong_online"] == "文彩萧索"


def test_c58_drought_rain_choose_divination_mode_only_from_explicit_background():
    dry = weather_observation_omens(current_weather="旱")
    assert dry["divination_mode"] == "阳"

    rain = weather_observation_omens(current_weather="雨")
    assert rain["divination_mode"] == "阴"

    none = weather_observation_omens()
    assert none["divination_mode"] is None
    assert none["status"] == "not_computable"


def test_c58_wangxiang_only_modifies_change_speed():
    prosperous = weather_observation_omens(
        weather_texture="纯厚",
        qi_state="旺相",
    )
    assert prosperous["matched_omens"][0]["effects"] == ["雨"]
    assert prosperous["change_speed"] == "疾速"

    rest = weather_observation_omens(
        weather_texture="纯厚",
        qi_state="休囚",
    )
    assert rest["change_speed"] is None


def test_c58_flybird_taiyi_wind_direction_variant_stays_unresolved():
    data = weather_observation_omens(flybird_taiyi_conjoined=True)
    assert data["flybird_wind_direction"] is None
    variant = data["flybird_wind_direction_variant"]
    assert variant["canonical_selected"] is None
    assert variant["tongzong_online"] == "风从下来"
    assert variant["wujing_zongyao"] == "风从其上来"
    assert variant["runtime_direction_applied"] is False


def test_c58_is_not_c51_coronation_cloud_event():
    assert C51_BOUNDARY["same_observation_event"] is False
    assert C51_BOUNDARY["merge_allowed"] is False
    data = initial_move_cloud_timing(
        cloud_color="青",
        day_time_count=3,
        calculation_scope="日计",
        observation_slot="日出",
    )
    assert data["c51_boundary"]["c51"] == "天子初登位日月旁云气"
    assert data["c51_boundary"]["c58"] == "太乙初移宫候云气"


def test_c58_catalog_preserves_source_layers():
    data = c58_catalog()
    assert data["color_timing_rules"]["白"]["change_branch_period"] == ["申", "酉"]
    assert data["color_timing_rules"]["赤"]["status"] == (
        "collation_supported_primary_online_gap"
    )
    assert data["weather_texture_rules"] == WEATHER_TEXTURE_RULES
    assert data["flybird_taiyi_wind_variant"] == FLYBIRD_TAIYI_WIND_VARIANT
    assert COLOR_TIMING_RULES["黑"]["counts"] == [1, 8]
