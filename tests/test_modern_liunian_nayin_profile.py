import json
from pathlib import Path


PROFILE_FILE = Path(__file__).parents[1] / "rules" / "variants" / "modern_liunian_nayin.json"


def _profile():
    return json.loads(PROFILE_FILE.read_text(encoding="utf-8"))


def test_modern_liunian_nayin_is_independent_profile_not_j4m03_variant():
    data = _profile()
    assert data["profile_id"] == "modern_liunian_nayin_2026"
    assert data["variant_id"] == "MODERN-LIUNIAN-NAYIN"
    assert data["type"] == "modern_reconstruction"
    assert data["canonical"] is False
    assert "J4M03" not in data["variant_id"]


def test_modern_profile_runtime_is_under_variants_namespace():
    data = _profile()
    assert all(path.startswith("kintaiyi.variants.modern_liunian_nayin.") for path in data["runtime"])


def test_modern_profile_covers_four_counts_without_claiming_ancient_equivalence():
    data = _profile()
    assert data["scope"]["counts"] == ["年计", "月计", "日计", "时计"]
    relation = data["relation_to_ancient_rules"]
    assert "not a J4M-03 variant" in relation["j4m03"]
    assert "不得" in relation["policy"]


def test_modern_profile_runtime_boundaries_are_machine_locked():
    data = _profile()
    boundary = " ".join(data["implementation_boundary"])
    assert "古典律历标准映射" in boundary
    assert "dimension_mode=branch_proxy" in boundary
    assert "不自动推导" in boundary
    assert "不自动给吉凶或胜负" in boundary


def test_modern_profile_records_material_supported_structure():
    data = _profile()
    supported = " ".join(data["supported_content"])
    assert "宫徵羽商角" in supported
    assert "甲丙戊庚壬" in supported
    assert "星神本五行" in supported
    assert "变五行" in supported
    assert "两个纳音" in supported
    assert "四计均可用" in supported
