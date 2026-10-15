import copy
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path

import pytest

from kintaiyi import api

PROFILE = "reviewed_minute_math_facts_20261015_v1"
OPERATION = "facts.reviewed_minute_inputs_v1"
FACT_CONTRACT = "MINUTE-REVIEW-INPUT-FACTS-V1"
GENERAL_PROFILE = "tongzong_v2_general_formula_with_blockage"
BOARDS = json.loads((Path(__file__).parent / "fixtures/reviewed_minute_144_inputs_v1.json").read_text(encoding="utf-8"))
# This is an explicit cross-source comparison, not proof that either source is
# erroneous. Original FT36 charts replay byte-for-byte under their own pin.
SOURCE_DIFFERENCES = frozenset(("Y03", "Y22", "Y25", "Y31", "Y70", "N05", "N20", "N26"))
G7_MATCHING_BOARDS = [board for board in BOARDS if board["board_id"] not in SOURCE_DIFFERENCES]


def calculate(board):
    inputs = {key: value for key, value in board.items() if key != "board_id"}
    return api.calculate(OPERATION, source_profile=PROFILE,
                         general_source_profile=GENERAL_PROFILE, **inputs)


@pytest.mark.parametrize("board", BOARDS, ids=lambda b: b["board_id"])
def test_explicit_g7_comparison_keeps_all_144_original_source_assertions(board):
    if board["board_id"] in SOURCE_DIFFERENCES:
        with pytest.raises(ValueError, match="disagree with mathematical calculation"):
            calculate(board)
        return
    result = calculate(board)
    assert result == calculate(copy.deepcopy(board))
    assert result["no_ancient_layout_override"] is True
    assert result["prediction_generation_enabled"] is False
    assert result["chart_replay_verified_by_this_operation"] is False
    assert result["positions"]["taiyi"]["palace"] != 5
    for role, palace in board["asserted_generals"].items():
        assert result["positions"][role]["palace"] == palace
        assert result["positions"][role]["qi_coordinate"] == "NINE_PALACE"
    digest = result.pop("content_hash")
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    assert sha256(payload.encode()).hexdigest() == digest


def test_n24_math_has_no_ancient_layout_or_score_override():
    board = next(b for b in BOARDS if b["board_id"] == "N24")
    result = calculate(board)
    assert (result["inputs"]["home_cal"], result["inputs"]["away_cal"]) == (16, 1)
    assert result["positions"]["home_general"]["palace"] == 6
    assert result["positions"]["home_vassal"]["palace"] == 8
    assert result["positions"]["shiji"]["sector"] == "戌"
    assert result["positions"]["shiji"]["is_intershen"] is True
    # 6/8 are the neighbors of projected palace1, not immediate centers of 戌.
    assert not any(g["target"] == "shiji" and g["actors"] == ["home_general", "home_vassal"]
                   for g in result["flank_geometries"])
    assert any(g["target"] == "shiji" and set(g["actors"]) == {"taiyi", "home_general"}
               for g in result["flank_geometries"])
    assert result["pattern_interpretation"]["flank_geometry_is_not_an_approved_tixie_or_xiebi_trigger"]
    assert "away_points" not in result and "score" not in result
    assert "board_id" not in result["inputs"]


def test_ancient_general_disagreement_is_rejected_instead_of_repaired():
    board = copy.deepcopy(next(b for b in BOARDS if b["board_id"] == "N24"))
    board["asserted_generals"]["home_vassal"] = 1
    with pytest.raises(ValueError, match="disagree with mathematical calculation"):
        calculate(board)


def test_intershen_eyes_are_not_promoted_to_geometric_actors():
    for board in G7_MATCHING_BOARDS:
        result = calculate(board)
        for geometry in result["flank_geometries"]:
            for actor in geometry["actors"]:
                assert result["positions"][actor]["is_intershen"] is False
                assert result["positions"][actor]["sector"] is not None


def test_eye_own_sixteen_sector_is_not_replaced_with_nine_palace_element():
    board = copy.deepcopy(BOARDS[0])
    board["shiji"] = "辰"
    result = calculate(board)
    eye = result["positions"]["shiji"]
    assert eye["intrinsic_element"] == "火"
    assert eye["landing_element"] == "土"
    assert eye["palace"] == 9  # palace element is wood, a different comparison
    assert eye["self_qi"] == "休"
    assert eye["qi_coordinate"] == "SIXTEEN_SECTOR"


def test_general_self_qi_keeps_rest_prison_dead_distinct():
    states = {}
    for board in G7_MATCHING_BOARDS:
        positions = calculate(board)["positions"]
        for role in ("home_general", "home_vassal", "away_general", "away_vassal"):
            position = positions[role]
            states[position["self_qi"]] = position
    assert set(states) == {"旺", "相", "休", "囚", "死"}
    assert states["死"]["death_full_name"] == "死绝"
    assert states["休"]["death_full_name"] is None
    assert states["囚"]["death_full_name"] is None


def test_known_blockage_is_preserved_and_taiyi_center_is_rejected():
    board = copy.deepcopy(BOARDS[0])
    board["home_cal"] = 25
    board["asserted_generals"].update(home_general=5, home_vassal=5)
    result = calculate(board)
    assert result["positions"]["home_general"]["known_center"] is True
    assert result["general_calculation"]["host"]["blocked"] is True
    assert result["general_calculation"]["host"]["five_generals_released"] is False
    assert result["door_contexts"]["host"]["door_ready"] is None
    board["taiyi"] = 5
    with pytest.raises(ValueError, match="Taiyi in center 5"):
        calculate(board)


@pytest.mark.parametrize("bad", [None, True, 0, 10, "6"])
def test_invalid_general_data_never_becomes_zero_or_a_fact(bad):
    board = copy.deepcopy(BOARDS[0])
    board["asserted_generals"]["home_general"] = bad
    with pytest.raises((TypeError, ValueError)):
        calculate(board)


def test_profile_is_explicit_and_facts_do_not_become_scoring_rule_ids():
    inputs = {key: value for key, value in BOARDS[0].items() if key != "board_id"}
    with pytest.raises(ValueError, match="source profile required"):
        api.calculate(OPERATION, source_profile="jinjing", general_source_profile=GENERAL_PROFILE, **inputs)
    with pytest.raises(ValueError, match="G7 general source profile required"):
        api.calculate(OPERATION, source_profile=PROFILE,
                      general_source_profile="FIVE_MODE_D37_D45_FT36_V1", **inputs)
    operation = next(o for o in api.list_operations() if o["name"] == OPERATION)
    assert callable(api.resolve_runtime(operation["runtime"]))
    assert operation["rule_ids"] == ["R-QI"]  # reused formula, not a new score rule
    result = calculate(BOARDS[0])
    assert result["fact_contract_id"] == FACT_CONTRACT
    assert "rule_id" not in result
    assert api.get_rule(FACT_CONTRACT)["count"] == 0


def test_chart_profile_identity_and_input_hash_are_never_silently_promoted():
    board = copy.deepcopy(BOARDS[0])
    original = calculate(board)
    board["chart_source_profile"] = "explicitly_different_chart_source"
    other = calculate(board)
    assert other["input_hash"] != original["input_hash"]
    assert other["chart_source_profile"] == "explicitly_different_chart_source"
    board["chart_source_profile"] = ""
    with pytest.raises(ValueError, match="chart source profile required"):
        calculate(board)


@pytest.mark.parametrize("month, expected_dun", [(1, "阳"), (7, "阴")])
def test_modern_public_source_covers_72_layouts_without_mixing_ft36(month, expected_dun):
    seen = set()
    start = datetime(2026, month, 15, 0, 0, tzinfo=timezone.utc)
    for minute in range(72):
        chart = api.calculate("modern.minute_count", start + timedelta(minutes=minute))
        core = chart["result"]
        assert core["dun"] == expected_dun
        seen.add(core["local_ju"])
        generals = {
            "home_general": 5 if core["host_blocked"] else core["host_big_general_palace"],
            "home_vassal": 5 if core["host_blocked"] else core["host_assistant_general_palace"],
            "away_general": 5 if core["guest_blocked"] else core["guest_big_general_palace"],
            "away_vassal": 5 if core["guest_blocked"] else core["guest_assistant_general_palace"],
        }
        facts = api.calculate(
            OPERATION, source_profile=PROFILE, general_source_profile=GENERAL_PROFILE,
            chart_source_profile=chart["source_profile"], taiyi=core["taiyi_palace"],
            wenchang=core["wenchang_sector"], shiji=core["shiji_sector"],
            home_cal=core["host_calc"], away_cal=core["guest_calc"], asserted_generals=generals,
        )
        assert facts["chart_source_profile"] == chart["source_profile"]
        assert facts["inputs"]["asserted_generals"] == generals
        assert facts["prediction_generation_enabled"] is False
        assert facts["general_calculation"]["host"]["blocked"] == core["host_blocked"]
        assert facts["general_calculation"]["guest"]["blocked"] == core["guest_blocked"]
    assert seen == set(range(1, 73))
