import pytest

from kintaiyi.taiyou_limit_tracks import bailiu_inner_track
from kintaiyi.xiaoyou_hexagram import xiaoyou_inner_track
from kintaiyi.taiyou_xiaoyou_distinction import (
    DOCTRINAL_PRINCIPLE,
    LEGACY_REFERENCE_AUDIT,
    SYSTEMS,
    c49_catalog,
    observe_current_inner_trigrams,
    taiyou_xiaoyou_distinction,
)


def test_c49_systems_keep_distinct_inner_rates():
    assert SYSTEMS["taiyou"]["inner_trigram_years"] == 36
    assert SYSTEMS["xiaoyou"]["inner_trigram_years"] == 24
    assert SYSTEMS["taiyou"]["rate_symbol"] == "乾天之策"
    assert SYSTEMS["xiaoyou"]["rate_symbol"] == "坤地之策"


def test_c49_rate_symbols_do_not_restrict_actual_trigram():
    assert SYSTEMS["taiyou"]["may_travel_any_trigram"] is True
    assert SYSTEMS["xiaoyou"]["may_travel_any_trigram"] is True
    assert SYSTEMS["taiyou"]["not_restricted_to"] == "乾"
    assert SYSTEMS["xiaoyou"]["not_restricted_to"] == "坤"
    assert "太游得乾天之策" in DOCTRINAL_PRINCIPLE["question"]
    assert "阴得阳而生" in DOCTRINAL_PRINCIPLE["answer"]


def test_c49_canonical_rule_is_not_current_trigram_inequality():
    data = taiyou_xiaoyou_distinction()
    assert data["systems_distinct"] is True
    assert data["distinct_by_current_trigram_inequality"] is False
    assert data["systems"]["taiyou"]["inner_trigram_years"] == 36
    assert data["systems"]["xiaoyou"]["inner_trigram_years"] == 24


def test_c49_observation_can_show_same_trigram_without_erasing_system_difference():
    found = None
    for year in range(1, 500):
        ty = bailiu_inner_track(year)
        xy = xiaoyou_inner_track(year)
        if ty["trigram"] == xy["trigram"]:
            found = (ty, xy)
            break

    assert found is not None
    ty, xy = found
    data = observe_current_inner_trigrams(ty, xy)

    assert data["same_current_trigram"] is True
    assert data["different_current_trigram"] is False
    assert data["systems_still_distinct"] is True
    assert data["semantic_status"] == "derived_observation_not_source_verdict"


def test_c49_observation_can_show_different_trigram_as_derived_only():
    found = None
    for year in range(1, 500):
        ty = bailiu_inner_track(year)
        xy = xiaoyou_inner_track(year)
        if ty["trigram"] != xy["trigram"]:
            found = (ty, xy)
            break

    assert found is not None
    ty, xy = found
    data = observe_current_inner_trigrams(ty, xy)

    assert data["same_current_trigram"] is False
    assert data["different_current_trigram"] is True
    assert data["systems_still_distinct"] is True
    assert data["semantic_status"] == "derived_observation_not_source_verdict"


def test_c49_observation_preserves_36_vs_24_rate():
    ty = bailiu_inner_track(1)
    xy = xiaoyou_inner_track(1)
    data = observe_current_inner_trigrams(ty, xy)
    assert data["taiyou"]["years_per_inner_trigram"] == 36
    assert data["xiaoyou"]["years_per_inner_trigram"] == 24


def test_c49_rejects_wrong_source_rule_identities():
    with pytest.raises(ValueError, match="C38-BL-INNER"):
        observe_current_inner_trigrams(
            {"rule_id": "wrong", "years_per_palace": 36, "trigram": "乾"},
            xiaoyou_inner_track(1),
        )

    with pytest.raises(ValueError, match="C47-XY-INNER"):
        observe_current_inner_trigrams(
            bailiu_inner_track(1),
            {"rule_id": "wrong", "years_per_trigram": 24, "trigram": "乾"},
        )


def test_c49_rejects_tampered_rates():
    ty = bailiu_inner_track(1)
    ty["years_per_palace"] = 24
    with pytest.raises(ValueError, match="36年"):
        observe_current_inner_trigrams(ty, xiaoyou_inner_track(1))

    xy = xiaoyou_inner_track(1)
    xy["years_per_trigram"] = 36
    with pytest.raises(ValueError, match="24年"):
        observe_current_inner_trigrams(bailiu_inner_track(1), xy)


def test_c49_legacy_boolean_is_explicitly_non_equivalent():
    assert LEGACY_REFERENCE_AUDIT["canonical_equivalent"] is False
    assert any("!=" in item for item in LEGACY_REFERENCE_AUDIT["issues"])
    assert any("当前卦相同" in item for item in LEGACY_REFERENCE_AUDIT["issues"])


def test_c49_catalog_does_not_mark_whole_volume9_wrapper_migrated():
    data = c49_catalog()
    assert data["rule_id"] == "C49-TX-DISTINCTION"
    assert data["whole_volume9_wrapper_migrated"] is False
    assert data["legacy_reference_audit"]["canonical_equivalent"] is False
