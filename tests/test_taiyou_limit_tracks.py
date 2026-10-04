from kintaiyi.legacy_schema import classify_legacy_field
from kintaiyi.limit_cycles import yangjiu_bailiu_limits
from kintaiyi.pan_v2 import build_pan_v2, validate_pan_v2
from kintaiyi.taiyou_limit_tracks import (
    TAIYOU_PALACE_PATH,
    TAIYOU_TRIGRAM_PATH,
    bailiu_inner_track,
    taiyou_limit_tracks,
    yangjiu_outer_track,
)


def test_c38_direct_path_is_eight_palaces_without_center():
    assert TAIYOU_PALACE_PATH == (7, 8, 9, 1, 2, 3, 4, 6)
    assert TAIYOU_TRIGRAM_PATH == ("坤", "坎", "巽", "乾", "离", "艮", "震", "兑")
    assert 5 not in TAIYOU_PALACE_PATH


def test_c38_yangjiu_outer_first_year_starts_at_kun():
    data = yangjiu_outer_track(4431)
    assert data["cycle_year"] == 1
    assert data["round_index"] == 1
    assert data["year_in_round"] == 1
    assert data["palace"] == 7
    assert data["trigram"] == "坤"
    assert data["year_in_palace"] == 1


def test_c38_yangjiu_outer_changes_palace_every_ten_years():
    end_kun = yangjiu_outer_track(4440)
    start_kan = yangjiu_outer_track(4441)
    assert end_kun["year_in_round"] == 10
    assert end_kun["palace"] == 7
    assert end_kun["year_in_palace"] == 10
    assert end_kun["palace_complete"] is True

    assert start_kan["year_in_round"] == 11
    assert start_kan["palace"] == 8
    assert start_kan["trigram"] == "坎"
    assert start_kan["year_in_palace"] == 1


def test_c38_yangjiu_outer_eighty_year_round_and_4560_end():
    end_round = yangjiu_outer_track(4510)
    end_big = yangjiu_outer_track(4430)

    assert end_round["year_in_round"] == 80
    assert end_round["palace"] == 6
    assert end_round["trigram"] == "兑"
    assert end_round["round_complete"] is True

    assert end_big["cycle_year"] == 4560
    assert end_big["round_index"] == 57
    assert end_big["year_in_round"] == 80
    assert end_big["palace"] == 6
    assert end_big["year_in_palace"] == 10
    assert end_big["big_limit_complete"] is True


def test_c38_bailiu_inner_first_year_starts_at_kun():
    data = bailiu_inner_track(2271)
    assert data["cycle_year"] == 1
    assert data["round_index"] == 1
    assert data["year_in_round"] == 1
    assert data["palace"] == 7
    assert data["trigram"] == "坤"
    assert data["year_in_palace"] == 1


def test_c38_bailiu_inner_changes_palace_every_36_years():
    end_kun = bailiu_inner_track(2306)
    start_kan = bailiu_inner_track(2307)
    assert end_kun["year_in_round"] == 36
    assert end_kun["palace"] == 7
    assert end_kun["year_in_palace"] == 36
    assert end_kun["palace_complete"] is True

    assert start_kan["year_in_round"] == 37
    assert start_kan["palace"] == 8
    assert start_kan["trigram"] == "坎"
    assert start_kan["year_in_palace"] == 1


def test_c38_bailiu_inner_288_year_round_and_4320_end():
    end_round = bailiu_inner_track(2558)
    end_big = bailiu_inner_track(2270)

    assert end_round["year_in_round"] == 288
    assert end_round["palace"] == 6
    assert end_round["trigram"] == "兑"
    assert end_round["round_complete"] is True

    assert end_big["cycle_year"] == 4320
    assert end_big["round_index"] == 15
    assert end_big["year_in_round"] == 288
    assert end_big["palace"] == 6
    assert end_big["year_in_palace"] == 36
    assert end_big["big_limit_complete"] is True


def test_c38_bundle_keeps_outer_and_inner_tracks_separate():
    data = taiyou_limit_tracks(1000)
    assert set(data) >= {"yangjiu_outer", "bailiu_inner"}
    assert data["yangjiu_outer"]["track"] == "阳九外卦"
    assert data["bailiu_inner"]["track"] == "百六内卦"
    assert data["cross_track_merge"] is False


def test_c38_can_be_embedded_beside_c36_limits_without_modifying_c36():
    limits = yangjiu_bailiu_limits(1000)
    limits["taiyou_tracks"] = taiyou_limit_tracks(1000)
    payload = build_pan_v2(cycles={"limits": limits})

    assert payload["cycles"]["limits"]["yangjiu"]["rule_id"] == "C36-YJ"
    assert payload["cycles"]["limits"]["taiyou_tracks"]["yangjiu_outer"]["rule_id"] == "C38-YJ-OUTER"
    assert validate_pan_v2(payload)["valid"] is True


def test_c38_does_not_mark_old_volume9_composite_wrapper_as_migrated():
    item = classify_legacy_field("卷九")
    assert item["status"] == "unported"
    assert item["candidate_layer"] == "derived"
    assert item["migrate_whole"] is False
