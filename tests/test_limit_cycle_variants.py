from kintaiyi.limit_cycle_variants import (
    compare_limit_cycle_profiles,
    limit_cycle_source_variants,
)


def test_limit_cycle_profiles_are_kept_separate():
    data = limit_cycle_source_variants()
    assert data["canonical_selected"] is None
    assert data["cross_source_merge"] is False
    assert set(data["profiles"]) == {
        "tongzong_yangjiu_bailiu",
        "jinjing_siku_volume7",
    }


def test_tongzong_runtime_profile_stays_implemented():
    data = limit_cycle_source_variants()["profiles"]["tongzong_yangjiu_bailiu"]
    assert data["status"] == "implemented"
    assert data["runtime"] == "kintaiyi.limit_cycles.yangjiu_bailiu_limits"
    assert data["yangjiu"] == {
        "big_limit": 4560,
        "small_limit": 456,
        "surplus_offset": 130,
    }
    assert data["bailiu"] == {
        "big_limit": 4320,
        "small_limit": 288,
        "surplus_offset": 2050,
    }


def test_jinjing_volume7_records_unresolved_yangjiu_region_formula():
    data = limit_cycle_source_variants()["profiles"]["jinjing_siku_volume7"]
    assert data["status"] == "source_variant_not_fully_computable"
    yangjiu = data["yangjiu"]
    assert yangjiu["yuan_years"] == 4560
    assert yangjiu["one_yangjiu_years"] == 456
    assert yangjiu["region_step_text_years"] == 13
    assert yangjiu["region_count"] == 12
    assert yangjiu["consistency"]["status"] == "region_formula_unresolved"
    assert data["runtime"] is None


def test_jinjing_volume7_preserves_bailiu_4330_text_conflict():
    data = limit_cycle_source_variants()["profiles"]["jinjing_siku_volume7"]
    bailiu = data["bailiu"]
    assert bailiu["one_cycle_years"] == 288
    assert bailiu["cycles_per_yuan"] == 15
    assert bailiu["source_text_yuan_years"] == 4330
    assert bailiu["arithmetic_yuan_years"] == 4320
    assert bailiu["region_step_years"] == 24
    assert bailiu["region_count"] == 12
    assert bailiu["consistency"]["status"] == "yuan_total_text_conflict"


def test_limit_cycle_comparison_never_claims_formula_equivalence():
    data = compare_limit_cycle_profiles()
    assert data["yangjiu"]["equivalent_formula"] is False
    assert data["bailiu"]["equivalent_formula"] is False
    assert data["cross_source_merge"] is False
