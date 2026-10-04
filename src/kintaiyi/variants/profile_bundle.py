"""现代 / 重构 profile 的显式 pan-v2 容器。

本模块只组装调用方已经计算好的 modern payload：
- 不运行古籍算法；
- 不自动启用任何 modern profile；
- 不写入 analysis/source_variants；
- 只用于显式传给 build_pan_v2(modern=...)。
"""

from __future__ import annotations

import copy
from typing import Any

MODERN_VARIANT_SECTION_VERSION = "taiyi-modern-variants-v1"
MODERN_LIUNIAN_NAYIN_PROFILE = "modern_liunian_nayin_2026"


def build_modern_liunian_nayin_profile(
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """包装已经算好的现代流年纳音结果。

    payload 可以是单个结果或调用方自行组织的结果集合；本函数不重算、不解释。
    """
    if payload is None:
        payload = {}
    if not isinstance(payload, dict):
        raise TypeError("modern Liunian nayin payload须为dict")

    return {
        "profile": MODERN_LIUNIAN_NAYIN_PROFILE,
        "variant_id": "MODERN-LIUNIAN-NAYIN",
        "type": "modern_reconstruction",
        "canonical": False,
        "cross_ancient_merge": False,
        "payload": copy.deepcopy(payload),
        "policy": (
            "现代太乙纳音结果只存放于pan v2 modern区段；"
            "不得自动提升为analysis、source_variants或古籍canonical。"
        ),
    }


def build_modern_variant_section(
    *,
    liunian_nayin: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """构建可显式传入 build_pan_v2(modern=...) 的 modern 区段。

    没有传入任何 profile 时返回空 profiles；不会自动启用现代体系。
    """
    profiles: dict[str, Any] = {}
    if liunian_nayin is not None:
        profiles[MODERN_LIUNIAN_NAYIN_PROFILE] = build_modern_liunian_nayin_profile(
            liunian_nayin
        )

    return {
        "schema_version": "1.0",
        "canonical": MODERN_VARIANT_SECTION_VERSION,
        "profiles": profiles,
        "cross_ancient_merge": False,
        "auto_enabled": False,
        "policy": "现代profile必须显式传入；默认pan v2不自动启用任何现代重构体系。",
    }
