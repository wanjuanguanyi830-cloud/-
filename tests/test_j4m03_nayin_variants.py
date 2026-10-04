import json
from pathlib import Path


VARIANT_FILE = Path(__file__).parents[1] / "rules" / "j4m03_nayin_variants.json"


def _catalog():
    return json.loads(VARIANT_FILE.read_text(encoding="utf-8"))


def test_j4m03_nayin_variants_keep_canonical_modern_and_legacy_separate():
    data = _catalog()
    assert data["canonical_rule"] == "J4M-03"
    assert data["canonical_profile"] == "jinjing_siku_volume4"

    by_id = {item["id"]: item for item in data["variants"]}
    assert by_id["J4M03-CANONICAL-TWO-EYE"]["status"] == "implemented"
    assert by_id["J4M03-MODERN-LIUNIAN-NAYIN"]["type"] == "modern_reconstruction"
    assert by_id["J4M03-LEGACY-WCNSJ"]["type"] == "legacy_implementation"
    assert by_id["J4M03-LEGACY-WCNSJ"]["status"] == "quarantined"


def test_modern_liunian_nayin_is_reference_only_not_jinjing_canonical():
    data = _catalog()
    modern = {item["id"]: item for item in data["variants"]}["J4M03-MODERN-LIUNIAN-NAYIN"]

    assert modern["profile"] == "modern_liunian_nayin_2026"
    assert modern["status"] == "implemented_modern_variant"
    assert any(path.endswith(".modern_star_base_nayin") for path in modern["runtime"])
    assert any(path.endswith(".modern_day_tone_sequence") for path in modern["runtime"])
    assert any(path.endswith(".modern_star_transformed_nayin") for path in modern["runtime"])
    assert any(path.endswith(".compare_modern_nayin_elements") for path in modern["runtime"])
    text = " ".join(modern["explicit_non_equivalence"])
    assert "不能据此声称《金镜》" in text
    assert "不能把现代日干变音顺序并入" in text
    assert "不能由该体系改写" in text


def test_modern_variant_records_only_material_supported_structure():
    data = _catalog()
    modern = {item["id"]: item for item in data["variants"]}["J4M03-MODERN-LIUNIAN-NAYIN"]
    supported = " ".join(modern["supported_content"])

    assert "宫徵羽商角" in supported
    assert "甲丙戊庚壬" in supported
    assert "星神本五行" in supported
    assert "变五行" in supported
    assert "两个纳音" in supported
    assert "四计均可用" in supported


def test_modern_variant_runtime_boundaries_are_machine_locked():
    data = _catalog()
    modern = {item["id"]: item for item in data["variants"]}["J4M03-MODERN-LIUNIAN-NAYIN"]
    boundary = " ".join(modern["implementation_boundary"])

    assert "古典律历标准映射" in boundary
    assert "dimension_mode=branch_proxy" in boundary
    assert "不自动推导" in boundary
    assert "不自动给吉凶或胜负" in boundary
