import pytest

from kintaiyi.dayou_hexagram import compose_dayou_heavy_hexagram
from kintaiyi.dayou_xiaoyou_difference import (
    SOURCE_WITNESS,
    c49_catalog,
    dayou_xiaoyou_difference,
)
from kintaiyi.xiaoyou_hexagram import xiaoyou_heavy_hexagram


def _dayou(inner: str):
    return compose_dayou_heavy_hexagram(
        inner_trigram=inner,
        outer_trigram="坤",
        year_in_inner_trigram=1,
    )


def test_c49_direct_period_and_symbolic_ce_roles():
    data = c49_catalog()
    rules = data["source_witness"]["direct_rules"]
    assert rules["dayou"] == {
        "years_per_inner_trigram": 36,
        "symbolic_ce": "乾天之策",
    }
    assert rules["xiaoyou"] == {
        "years_per_inner_trigram": 24,
        "symbolic_ce": "坤地之策",
    }


def test_c49_same_inner_trigram_is_only_derived_fact():
    data = dayou_xiaoyou_difference(
        _dayou("乾"),
        xiaoyou_heavy_hexagram(1),
    )
    assert data["dayou"]["inner_trigram"] == "乾"
    assert data["xiaoyou"]["inner_trigram"] == "乾"
    assert data["same_inner_trigram"] is True
    assert data["different_inner_trigram"] is False
    assert data["derived_current_comparison"] is True
    assert data["auspice"] is None
    assert data["auspice_status"] == (
        "source_does_not_assign_auspice_from_same_or_different_alone"
    )


def test_c49_different_inner_trigram_is_not_bad_omen():
    data = dayou_xiaoyou_difference(
        _dayou("乾"),
        xiaoyou_heavy_hexagram(25),
    )
    assert data["dayou"]["inner_trigram"] == "乾"
    assert data["xiaoyou"]["inner_trigram"] == "离"
    assert data["same_inner_trigram"] is False
    assert data["different_inner_trigram"] is True
    assert data["auspice"] is None


def test_c49_keeps_yin_yang_doctrine_as_explanation_not_formula():
    data = dayou_xiaoyou_difference(
        _dayou("震"),
        xiaoyou_heavy_hexagram(80),
    )
    assert data["doctrine"] == [
        "阴得阳而生",
        "阳得阴而成",
        "天地配合",
        "阴阳互用",
        "一阴一阳之谓道",
    ]
    assert data["cross_cycle_merge"] is False
    assert data["c38_track_used"] is False


def test_c49_does_not_modify_upstream_cycle_roles():
    data = dayou_xiaoyou_difference(
        _dayou("坤"),
        xiaoyou_heavy_hexagram(193),
    )
    assert data["dayou"]["upstream_rule_id"] == "C41-DY-HEX"
    assert data["dayou"]["years_per_inner_trigram"] == 36
    assert data["xiaoyou"]["upstream_rule_id"] == "C47-XY-HEX"
    assert data["xiaoyou"]["years_per_inner_trigram"] == 24


def test_c49_rejects_wrong_dayou_identity():
    with pytest.raises(ValueError, match="C41-DY-HEX"):
        dayou_xiaoyou_difference(
            {"rule_id": "wrong"},
            xiaoyou_heavy_hexagram(1),
        )


def test_c49_rejects_wrong_xiaoyou_identity():
    with pytest.raises(ValueError, match="C47-XY-HEX"):
        dayou_xiaoyou_difference(
            _dayou("乾"),
            {"rule_id": "wrong"},
        )


def test_c49_catalog_declares_no_auspice_and_no_cycle_merge():
    data = c49_catalog()
    assert data["upstream_rules"] == ["C41-DY-HEX", "C47-XY-HEX"]
    assert data["derived_current_comparison"] is True
    assert data["auspice_from_same_or_different"] is False
    assert data["cross_cycle_merge"] is False


def test_c49_records_volume_boundary_witness():
    assert SOURCE_WITNESS["online_witness_volume"] == 10
    assert SOURCE_WITNESS["volume_status"] == "witness_volume_boundary_variant"
