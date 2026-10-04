"""Modern / reconstructed Taiyi variants.

该包只放非古籍 canonical 的显式现代重构 profile。
"""

from .modern_liunian_nayin import (
    MODERN_NAYIN_PROFILE,
    MODERN_NAYIN_VARIANT_ID,
    compare_modern_nayin_elements,
    modern_day_tone_sequence,
    modern_star_base_nayin,
    modern_star_transformed_nayin,
)

__all__ = [
    "MODERN_NAYIN_PROFILE",
    "MODERN_NAYIN_VARIANT_ID",
    "compare_modern_nayin_elements",
    "modern_day_tone_sequence",
    "modern_star_base_nayin",
    "modern_star_transformed_nayin",
]


from .profile_bundle import (
    MODERN_LIUNIAN_NAYIN_PROFILE,
    MODERN_VARIANT_SECTION_VERSION,
    build_modern_liunian_nayin_profile,
    build_modern_variant_section,
)

__all__ += [
    "MODERN_LIUNIAN_NAYIN_PROFILE",
    "MODERN_VARIANT_SECTION_VERSION",
    "build_modern_liunian_nayin_profile",
    "build_modern_variant_section",
]
