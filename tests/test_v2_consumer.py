import pytest

from kintaiyi.v2_consumer import (
    build_v2_view_model,
    read_v2_analysis,
    read_v2_board,
    read_v2_section,
    resolve_v2_payload,
)


def _sample_v2():
    return {
        "schema_version": "2.0",
        "meta": {"profile": "test"},
        "calendar": {"year": 2026},
        "board": {
            "taiyi": {"palace": 1},
            "eyes": {},
            "calculations": {},
            "generals": {},
            "doors": {},
        },
        "cycles": {},
        "analysis": {
            "patterns": {},
            "eight_divinations": {"home": {"rule_id": "D8-01"}},
            "seven_methods": {"tiger": {"rule_id": "T7-04"}},
            "military": {"source_profile": "volume5_strict"},
        },
        "modern": {},
        "source_variants": {},
        "compat": {"legacy_top_level": True, "legacy_schema": "pan-v1-flat"},
    }


def test_direct_v2_is_accepted():
    resolved = resolve_v2_payload(_sample_v2())
    assert resolved["computable"] is True
    assert resolved["source"] == "direct_v2"
    assert resolved["missing_root_sections"] == []


def test_embedded_v2_is_preferred_over_flat_legacy_fields():
    pan = {
        "主算": [17, "旧字段"],
        "太乙": 8,
        "v2": _sample_v2(),
    }
    resolved = resolve_v2_payload(pan)
    assert resolved["source"] == "embedded_v2"
    assert resolved["payload"]["board"]["taiyi"]["palace"] == 1


def test_flat_only_pan_is_rejected_in_strict_mode():
    data = resolve_v2_payload({
        "主算": [17],
        "客算": [13],
        "太乙": 8,
        "七式": {"猛虎相拒": "吉利成正"},
    })
    assert data["computable"] is False
    assert data["consumer_mode"] == "v2_strict"
    assert data["legacy_top_level_detected"] is True
    assert data["missing_inputs"] == ["v2"]


def test_analysis_reader_never_falls_back_to_flat_field():
    pan = {
        "军事战略": {"wrong": "legacy"},
        "v2": _sample_v2(),
    }
    military = read_v2_analysis(pan, "military")
    assert military["data"] == {"source_profile": "volume5_strict"}


def test_board_reader_uses_v2_board_only():
    pan = {
        "太乙": 8,
        "v2": _sample_v2(),
    }
    taiyi = read_v2_board(pan, "taiyi")
    assert taiyi["data"]["palace"] == 1


def test_missing_analysis_child_is_explicitly_not_computable():
    data = _sample_v2()
    del data["analysis"]["military"]
    result = read_v2_analysis(data, "military")
    assert result["computable"] is False
    assert result["missing_inputs"] == ["analysis.military"]


def test_missing_root_section_is_not_silently_invented():
    data = _sample_v2()
    del data["modern"]
    resolved = resolve_v2_payload(data)
    assert resolved["computable"] is True
    assert resolved["missing_root_sections"] == ["modern"]

    modern = read_v2_section(data, "modern")
    assert modern["computable"] is False
    assert modern["missing_inputs"] == ["modern"]


def test_view_model_reports_no_legacy_fallback():
    view = build_v2_view_model({"主算": [99], "v2": _sample_v2()})
    assert view["legacy_fallback_used"] is False
    assert view["analysis"]["military"]["source_profile"] == "volume5_strict"


def test_unknown_section_name_is_rejected():
    with pytest.raises(ValueError):
        read_v2_section(_sample_v2(), "flat_legacy")
