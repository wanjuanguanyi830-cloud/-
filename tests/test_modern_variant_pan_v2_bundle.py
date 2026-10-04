from kintaiyi.pan_v2 import build_pan_v2
from kintaiyi.variants import (
    MODERN_LIUNIAN_NAYIN_PROFILE,
    build_modern_liunian_nayin_profile,
    build_modern_variant_section,
)


def test_modern_variant_section_is_empty_by_default():
    modern = build_modern_variant_section()
    assert modern["profiles"] == {}
    assert modern["auto_enabled"] is False
    assert modern["cross_ancient_merge"] is False


def test_modern_liunian_profile_requires_explicit_payload():
    payload = {
        "example": {
            "jiazi": "壬子",
            "nayin_name": "桑柘木",
        }
    }
    profile = build_modern_liunian_nayin_profile(payload)
    assert profile["profile"] == MODERN_LIUNIAN_NAYIN_PROFILE
    assert profile["variant_id"] == "MODERN-LIUNIAN-NAYIN"
    assert profile["canonical"] is False
    assert profile["cross_ancient_merge"] is False
    assert profile["payload"] == payload


def test_modern_variant_section_can_be_passed_to_pan_v2_without_touching_analysis():
    modern = build_modern_variant_section(
        liunian_nayin={
            "star": "太乙",
            "base_nayin": "桑柘木",
        }
    )
    pan = build_pan_v2(modern=modern)

    profile = pan["modern"]["profiles"][MODERN_LIUNIAN_NAYIN_PROFILE]
    assert profile["payload"]["star"] == "太乙"
    assert profile["canonical"] is False

    assert pan["analysis"]["patterns"] == {}
    assert pan["analysis"]["eight_divinations"] == {}
    assert pan["analysis"]["seven_methods"] == {}
    assert pan["analysis"]["military"] == {}
    assert pan["source_variants"] == {}


def test_modern_bundle_rejects_non_dict_payload():
    try:
        build_modern_liunian_nayin_profile(["not", "a", "dict"])
    except TypeError as exc:
        assert "payload须为dict" in str(exc)
    else:
        raise AssertionError("expected TypeError")
