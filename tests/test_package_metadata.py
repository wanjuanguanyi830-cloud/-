import kintaiyi


def test_package_metadata_locks_modern_production_calendar_policy():
    assert kintaiyi.PRODUCTION_CALENDAR_MODE == "modern_astronomy_lunisolar"
    assert kintaiyi.TAIYI_YEAR_BOUNDARY == "astronomical_winter_solstice"
    assert kintaiyi.NON_TAIYI_YEAR_BOUNDARIES == ("元旦", "春节", "立春", "春分")
    assert "taiyi_modern_calendar.production_calendar_context" in (
        kintaiyi.PUBLIC_MODERN_ENTRYPOINTS["calendar_context"]
    )
    assert "taiyi_modern_pan.build_modern_pan_v2" in (
        kintaiyi.PUBLIC_MODERN_ENTRYPOINTS["pan_v2"]
    )
