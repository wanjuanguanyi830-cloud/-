import pytest

from kintaiyi.ten_essences_positions import (
    FLYBIRD_PATHS,
    FIVEWIND_PATHS,
    LEGACY_AUDIT,
    SURPLUS_REJECTION,
    c53_runtime_catalog,
    fivewind_position,
    flybird_position,
)


def test_c53_flybird_paths_are_explicit_yang_forward_yin_reverse():
    assert FLYBIRD_PATHS["阳"] == (1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert FLYBIRD_PATHS["阴"] == (9, 8, 7, 6, 5, 4, 3, 2, 1)


@pytest.mark.parametrize(
    "count,yang_palace,yin_palace",
    [
        (1, 1, 9),
        (2, 2, 8),
        (8, 8, 2),
        (9, 9, 1),
        (10, 1, 9),
        (18, 9, 1),
        (90, 9, 1),
        (91, 1, 9),
    ],
)
def test_c53_flybird_small_cycle_nine_boundaries(count, yang_palace, yin_palace):
    yang = flybird_position(count, dun="阳")
    yin = flybird_position(count, dun="阴")

    assert yang["palace"] == yang_palace
    assert yin["palace"] == yin_palace
    assert yang["small_cycle"] == 9
    assert yin["small_cycle"] == 9


def test_c53_flybird_90_end_is_small_cycle_nine_not_zero():
    data = flybird_position(90, dun="阳")
    assert data["big_cycle_remainder"] == 0
    assert data["big_cycle_year"] == 90
    assert data["small_cycle_remainder"] == 0
    assert data["small_cycle_year"] == 9
    assert data["path_index"] == 9
    assert data["palace"] == 9
    assert data["palace_label"] == "巽"


def test_c53_flybird_rejects_old_mod8_model():
    audit = LEGACY_AUDIT["config.flybird"]
    assert audit["canonical_equivalent"] is False
    assert audit["legacy_outer_modulus"] == 8
    assert audit["direct_big_cycle"] == 90
    assert audit["direct_small_cycle"] == 9
    assert "%8" in audit["issue"]


def test_c53_flybird_is_not_external_j4m_observation():
    data = flybird_position(1, dun="阳")
    assert data["same_name_boundary"]["j4m11_external_observation"] is False
    assert "不得伪造军事飞鸟观测" in data["same_name_boundary"]["policy"]


def test_c53_fivewind_paths_are_odd_even_yang_and_reverse_yin():
    assert FIVEWIND_PATHS["阳"] == (1, 3, 5, 7, 9, 2, 4, 6, 8)
    assert FIVEWIND_PATHS["阴"] == (9, 7, 5, 3, 1, 8, 6, 4, 2)


@pytest.mark.parametrize(
    "count,yang_palace,yin_palace",
    [
        (1, 1, 9),
        (2, 3, 7),
        (5, 9, 1),
        (6, 2, 8),
        (9, 8, 2),
        (10, 1, 9),
        (29, 3, 7),
        (90, 8, 2),
    ],
)
def test_c53_fivewind_positions_follow_direct_nine_cycle(
    count, yang_palace, yin_palace
):
    assert fivewind_position(count, dun="阳")["palace"] == yang_palace
    assert fivewind_position(count, dun="阴")["palace"] == yin_palace


def test_c53_fivewind_rejects_old_mod29_model():
    audit = LEGACY_AUDIT["config.fivewind"]
    assert audit["canonical_equivalent"] is False
    assert audit["legacy_outer_modulus"] == 29
    assert audit["direct_big_cycle"] == 90
    assert audit["direct_small_cycle"] == 9
    assert "%29" in audit["issue"]

    # 第29数按直接小周9余2，阳遁应到第二位三宫，而不是按29重置。
    data = fivewind_position(29, dun="阳")
    assert data["small_cycle_year"] == 2
    assert data["palace"] == 3


@pytest.mark.parametrize("func", [flybird_position, fivewind_position])
def test_c53_requires_explicit_dun(func):
    with pytest.raises(TypeError):
        func(1)
    with pytest.raises(ValueError, match="dun须为阳/阴"):
        func(1, dun="冬至")


@pytest.mark.parametrize("func", [flybird_position, fivewind_position])
def test_c53_rejects_nonpositive_or_bool_count(func):
    with pytest.raises(ValueError):
        func(0, dun="阳")
    with pytest.raises(TypeError):
        func(True, dun="阳")


@pytest.mark.parametrize("func", [flybird_position, fivewind_position])
def test_c53_never_applies_rejected_surplus_or_cloud_omens(func):
    data = func(12, dun="阳")
    assert data["surplus_applied"] is False
    assert data["surplus_policy"]["apply"] is False
    assert data["cloud_omen_applied"] is False


def test_c53_surplus_rejections_preserve_source_boundary():
    assert SURPLUS_REJECTION["飞鸟"]["legacy_or_variant_surplus"] == {"palace": 3}
    assert SURPLUS_REJECTION["飞鸟"]["apply"] is False
    assert "古法皆无所加" in SURPLUS_REJECTION["飞鸟"]["reason"]

    assert SURPLUS_REJECTION["五风"]["legacy_or_variant_surplus"] == {
        "palace": 3,
        "day": 6,
    }
    assert SURPLUS_REJECTION["五风"]["apply"] is False
    assert "古法不载" in SURPLUS_REJECTION["五风"]["reason"]


def test_c53_catalog_only_marks_two_position_runtimes_implemented():
    data = c53_runtime_catalog()
    assert data["implemented"] == ["飞鸟", "五风"]
    assert set(data["pending"]) == {
        "天皇", "帝符", "天时", "太尊", "五行", "八风", "三风", "太乙数"
    }
    assert data["cloud_omen_runtime"] is False
    assert data["pan_contract_extended"] is False


def test_c53_never_introduces_tianyou_taiyi():
    assert "天游太乙" not in repr(c53_runtime_catalog())
