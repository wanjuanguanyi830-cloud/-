import json

import pytest

from kintaiyi.pan_v2 import build_pan_v2, validate_pan_v2
from kintaiyi.v2_consumer import build_v2_view_model, read_v2_analysis


def test_builder_emits_complete_v2_root_and_required_children():
    data = build_pan_v2()
    assert data["schema_version"] == "2.0"
    assert set(data) == {
        "schema_version", "meta", "calendar", "board", "cycles",
        "analysis", "modern", "source_variants", "compat",
    }
    assert set(data["board"]) >= {"taiyi", "eyes", "calculations", "generals", "doors"}
    assert set(data["cycles"]) >= {
        "three_bases", "five_blessings", "big_wander", "small_wander", "four_taiyi",
    }
    assert set(data["analysis"]) >= {
        "patterns", "eight_divinations", "seven_methods", "military",
    }


def test_center_five_never_carries_sector16():
    data = build_pan_v2(board={
        "taiyi": {"palace": 5, "sector": "中"},
        "generals": {
            "home_general": {"palace": 5, "sector": "中", "intrinsic_element": "金", "palace_element": "土"},
        },
        "calculations": {
            "home": {"palace": 5, "sector": "中"},
        },
    })
    assert data["board"]["taiyi"]["sector"] is None
    assert data["board"]["generals"]["home_general"]["sector"] is None
    assert data["board"]["calculations"]["home"]["sector"] is None


def test_eyes_and_generals_keep_dual_element_facts():
    data = build_pan_v2(board={
        "eyes": {
            "skyeyes": {
                "sector": "辰",
                "sector_element": "土",
                "nine_palace_element": "木",
            },
        },
        "generals": {
            "home_general": {
                "palace": 6,
                "intrinsic_element": "金",
                "palace_element": "金",
            },
        },
    })
    eyes = data["board"]["eyes"]["skyeyes"]
    general = data["board"]["generals"]["home_general"]
    assert eyes["sector_element"] == "土"
    assert eyes["nine_palace_element"] == "木"
    assert general["intrinsic_element"] == "金"
    assert general["palace_element"] == "金"


def test_scenario_is_explicit_and_limited_to_canonical_keys():
    data = build_pan_v2(scenario={
        "enemy_start_year_branch": "子",
        "enemy_camp_day_taiyi_palace": 3,
        "enemy_first_arrival_taiyi_palace": 2,
    })
    assert data["meta"]["scenario"] == {
        "enemy_start_year_branch": "子",
        "enemy_camp_day_taiyi_palace": 3,
        "enemy_first_arrival_taiyi_palace": 2,
    }

    with pytest.raises(ValueError):
        build_pan_v2(scenario={"away_general_as_enemy_arrival": 9})


def test_builder_is_json_safe_without_stringifying_unknown_objects():
    data = build_pan_v2(
        meta={"tuple_value": ("甲", "子"), "set_value": {"旺", "相"}},
    )
    assert data["meta"]["tuple_value"] == ["甲", "子"]
    assert sorted(data["meta"]["set_value"]) == ["旺", "相"]
    json.dumps(data, ensure_ascii=False)

    class Unsafe:
        pass

    with pytest.raises(TypeError):
        build_pan_v2(meta={"bad": Unsafe()})


def test_validation_accepts_builder_output():
    data = build_pan_v2(
        analysis={"military": {"source_profile": "volume5_strict"}},
    )
    checked = validate_pan_v2(data)
    assert checked["valid"] is True
    assert checked["errors"] == []


def test_validation_rejects_center_sector_regression():
    data = build_pan_v2()
    data["board"]["taiyi"] = {"palace": 5, "sector": "中"}
    checked = validate_pan_v2(data)
    assert checked["valid"] is False
    assert "board.taiyi中五sector必须为null" in checked["errors"]


def test_builder_integrates_with_strict_v2_consumer():
    v2 = build_pan_v2(
        board={"taiyi": {"palace": 1, "sector": "乾"}},
        analysis={"military": {"source_profile": "volume5_strict"}},
    )
    pan = {"主算": [99], "v2": v2}

    view = build_v2_view_model(pan)
    military = read_v2_analysis(pan, "military")

    assert view["legacy_fallback_used"] is False
    assert view["board"]["taiyi"]["palace"] == 1
    assert military["data"]["source_profile"] == "volume5_strict"


def test_validation_warns_when_general_element_layers_are_incomplete():
    data = build_pan_v2(board={
        "generals": {
            "home_general": {"palace": 6, "intrinsic_element": "金"},
        },
    })
    checked = validate_pan_v2(data)
    assert checked["valid"] is True
    assert any("palace_element" in item for item in checked["warnings"])
