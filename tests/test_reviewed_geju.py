from copy import deepcopy
import json
from pathlib import Path

import pytest
from kintaiyi import api

PROFILE = "maintainer_reviewed_geju_20261015_v1"
BOARDS = json.loads((Path(__file__).parent / "fixtures/reviewed_minute_144_inputs_v1.json").read_text(encoding="utf-8"))


def inputs(board):
    return {"source_profile": PROFILE, **{k: v for k, v in board.items() if k not in {"board_id", "asserted_generals"}},
            **board["asserted_generals"]}


def run(board=None, **changes):
    values = inputs(board or BOARDS[0])
    values.update(changes)
    return api.calculate("patterns.reviewed_minute_v1", **values)


@pytest.mark.parametrize("board", BOARDS, ids=lambda b: b["board_id"])
def test_all_144_original_sources_preserve_positions_without_g7_repair(board):
    result = run(board)
    assert result == run(deepcopy(board))
    assert result["calculation_profile_repaired_or_swapped"] is False
    assert result["ancient_board_exception_applied"] is False
    for role, palace in board["asserted_generals"].items():
        assert result["positions"][role]["palace"] == palace
    by_id = {e["event_id"]: e for e in result["events"]}
    assert len(by_id) == len(result["events"])
    for event in result["events"]:
        assert event["input_hash"] == result["input_hash"]
        assert set(event["component_event_ids"]) <= set(by_id)
        for pair in event["support_pairs"]:
            assert all(result["positions"][role]["is_intershen"] is False for role in pair)
    assert "points" not in result


def test_n24_does_not_project_intershen_shiji_or_force_the_old_special_case():
    r = run(next(b for b in BOARDS if b["board_id"] == "N24"))
    assert r["inputs"]["home_cal"] == 16 and r["inputs"]["away_cal"] == 1
    for e in r["events"]:
        if e["pattern"] == "提挾" and e["target"] == "shiji":
            assert ["home_general", "home_vassal"] not in e["support_pairs"]
        assert e["pattern"] != "挾閉"
    assert r["positions"]["shiji"]["sector"] == "戌"


def test_independent_same_side_pair_may_flank_remote_target():
    r = run(taiyi=1, wenchang="午", home_general=9, home_vassal=7,
            away_general=4, away_vassal=3)
    hit = next(e for e in r["events"] if e["pattern"] == "提挾" and e["target"] == "wenchang")
    assert ["home_general", "home_vassal"] in hit["support_pairs"]


def test_double_eye_closure_uses_actual_home_away_and_taiyi_support():
    r = run(taiyi=1, wenchang="戌", shiji="亥", home_general=6,
            home_vassal=3, away_general=8, away_vassal=4)
    closure = next(e for e in r["events"] if e["pattern"] == "挾閉")
    assert "taiyi" in closure["actors"]
    assert "home_general" in closure["actors"] and "away_general" in closure["actors"]
    no_away = run(taiyi=1, wenchang="戌", shiji="亥", home_general=6,
                 home_vassal=8, away_general=3, away_vassal=4)
    assert not any(e["pattern"] == "挾閉" for e in no_away["events"])


def test_sigugu_enumerates_all_guards_and_preserves_group_lineage():
    r = run(taiyi=1, wenchang="乾", shiji="巽", home_general=1,
            home_vassal=8, away_general=1, away_vassal=8)
    parents = [e for e in r["events"] if e["pattern"] == "四郭固" and e["branch"] == "HOME"]
    guards = {e["event_id"] for e in r["events"] if e["pattern"] == "關"}
    assert len(parents) == 2
    assert guards <= {i for p in parents for i in p["component_event_ids"]}


def test_sigudu_uses_correct_pairs_and_excludes_parent_components():
    r = run(taiyi=1, wenchang="戌", shiji="乾", home_general=6,
            home_vassal=1, away_general=1, away_vassal=1)
    hits = [e for e in r["events"] if e["pattern"] == "四郭杜"]
    assert hits
    for hit in hits:
        assert set(hit["extra_event_ids"]).isdisjoint(hit["parent_component_event_ids"])
        assert set(hit["extra_categories"]) <= {"掩", "迫", "關", "格"}
    assert r["positions"]["wenchang"]["is_intershen"] is True


def test_qi_gate_only_uses_this_general_own_landing_not_other_roles():
    a = run(home_general=1, home_vassal=8, away_general=2, away_vassal=3)
    b = run(home_general=1, home_vassal=2, away_general=2, away_vassal=6)
    assert a["positions"]["home_general"]["still_can_fight_eligible"] is True
    assert a["positions"]["home_general"] == b["positions"]["home_general"]
    assert a["positions"]["home_vassal"]["self_qi"] == "旺"
    assert b["positions"]["home_vassal"]["self_qi"] == "囚"


def test_center_and_unknown_are_not_filled_or_repaired():
    r = run(home_general=5, home_vassal=5, home_cal=25)
    assert r["positions"]["home_general"]["sector"] is None
    assert r["readiness"]["HOME"]["ready"] is False
    assert r["readiness"]["HOME"]["duse"] is True
    with pytest.raises(ValueError, match="center5"):
        run(taiyi=5)
    with pytest.raises((TypeError, ValueError)):
        run(wenchang=None)
    with pytest.raises(ValueError, match="source profile"):
        run(source_profile="jinjing")


def test_public_rule_and_operation_share_one_runtime_owner():
    assert len(api.rule_runtime_candidates("REVIEWED-GEJU-V1")) == 1
    assert api.get_rule("REVIEWED-GEJU-V1")["count"] == 1
    assert api.calculate_rule("REVIEWED-GEJU-V1", **inputs(BOARDS[0])) == run()
