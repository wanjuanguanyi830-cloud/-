from importlib.util import find_spec
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_modern_nayin_runtime_exists_only_in_variants_namespace():
    assert find_spec("kintaiyi.variants.modern_liunian_nayin") is not None
    assert find_spec("kintaiyi.modern_nayin_variant") is None

    assert (ROOT / "src" / "kintaiyi" / "variants" / "modern_liunian_nayin.py").exists()
    assert not (ROOT / "src" / "kintaiyi" / "modern_nayin_variant.py").exists()


def test_modern_nayin_machine_rules_are_not_j4m03_named():
    assert (ROOT / "rules" / "variants" / "modern_liunian_nayin.json").exists()
    assert not (ROOT / "rules" / "j4m03_nayin_variants.json").exists()


def test_modern_nayin_has_independent_source_and_validation_records():
    assert (ROOT / "sources" / "modern-liunian-nayin-record.md").exists()
    assert (ROOT / "tests" / "reports" / "modern_liunian_nayin_validation.md").exists()


def test_obsolete_j4m_bound_tests_do_not_reappear():
    assert not (ROOT / "tests" / "test_modern_nayin_variant.py").exists()
    assert not (ROOT / "tests" / "test_j4m03_nayin_variants.py").exists()
