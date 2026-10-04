"""C41 卷九太游内外重卦、四象策数与内卦动爻。

直接来源：
- 《太乙统宗宝鉴》卷九“明太游内外重卦之策术”
- “明历数长短，以观远近之期术”

本模块只处理已经确定的内卦/外卦结构与入内卦年数。
不负责积年换算，也不调用 C38 阳九/百六行限轨迹。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer

C41_VERSION = "taiyi-c41-dayou-heavy-hexagram-v1"

_TRIGRAM_ALIASES = {
    "乾": "乾",
    "坤": "坤",
    "震": "震",
    "坎": "坎",
    "艮": "艮",
    "巽": "巽",
    "离": "离",
    "離": "离",
    "兑": "兑",
    "兌": "兑",
}

FOUR_IMAGE_CE = {
    "乾": {"four_image": "老阳", "ce": 36},
    "坤": {"four_image": "老阴", "ce": 24},
    "震": {"four_image": "少阳", "ce": 28},
    "坎": {"four_image": "少阳", "ce": 28},
    "艮": {"four_image": "少阳", "ce": 28},
    "巽": {"four_image": "少阴", "ce": 32},
    "离": {"four_image": "少阴", "ce": 32},
    "兑": {"four_image": "少阴", "ce": 32},
}

EPOCH_VARIANTS = {
    "tongzong_offset34_witness": {
        "source": "太乙统宗宝鉴",
        "status": "source_variant",
        "inner_offset": 34,
        "evidence": "太游太乙所在术见“加宫盈差三十四”",
        "selected_for_c41": False,
    },
    "taibai_bingbei_epoch_correction": {
        "source": "太白兵备统宗宝鉴",
        "status": "source_variant",
        "inner_offset": 36610,
        "evidence": "养玄子批评+34牵合纪元，提出另加差三万六千六百一十",
        "selected_for_c41": False,
    },
    "legacy_guiyun_outer_offset50": {
        "source": "legacy guiyun.py",
        "status": "unsupported_legacy_offset",
        "outer_offset": 50,
        "evidence": "旧代码值；当前直接条文未核得等价明文",
        "selected_for_c41": False,
    },
}


def _trigram(value: str) -> str:
    try:
        return _TRIGRAM_ALIASES[value]
    except (KeyError, TypeError):
        raise ValueError("卦须为乾坤震坎艮巽离兑") from None


def four_image_ce(trigram: str) -> dict[str, Any]:
    """返回一卦所属四象与策数。"""
    name = _trigram(trigram)
    return {
        "trigram": name,
        **copy.deepcopy(FOUR_IMAGE_CE[name]),
        "source_rule": "卷九·明太游内外重卦之策术",
    }


def inner_moving_line(year_in_inner_trigram: int) -> dict[str, Any]:
    """太游内卦36年，六年行一爻。"""
    year = integer(year_in_inner_trigram, 1, 36)
    line = (year - 1) // 6 + 1
    start = (line - 1) * 6 + 1
    end = line * 6
    names = ("初爻", "二爻", "三爻", "四爻", "五爻", "上爻")
    return {
        "year_in_inner_trigram": year,
        "line": line,
        "line_name": names[line - 1],
        "year_range": [start, end],
        "line_complete": year == end,
        "source_rule": "卷九·明历数长短，以观远近之期术",
    }


def compose_dayou_heavy_hexagram(
    *,
    inner_trigram: str,
    outer_trigram: str,
    year_in_inner_trigram: int,
) -> dict[str, Any]:
    """按“内卦画内、天数所得外卦画外”组成太游重卦结构。

    不尝试命名六十四卦；这里只输出可审计的上下卦结构、策数与内卦动爻。
    """
    inner = four_image_ce(inner_trigram)
    outer = four_image_ce(outer_trigram)
    moving = inner_moving_line(year_in_inner_trigram)

    return {
        "schema_version": "1.0",
        "canonical": C41_VERSION,
        "rule_id": "C41-DY-HEX",
        "source_profile": "tongzong_volume9_dayou_hexagram",
        "inner": inner,
        "outer": outer,
        "structure": {
            "upper_trigram": outer["trigram"],
            "lower_trigram": inner["trigram"],
            "display": f'{outer["trigram"]}上{inner["trigram"]}下',
        },
        "inner_moving_line": moving,
        "outer_moving_line": None,
        "outer_moving_line_status": "not_attested_in_direct_c41_rule",
        "ce": {
            "inner": inner["ce"],
            "outer": outer["ce"],
            "total": inner["ce"] + outer["ce"],
        },
        "epoch_formula_applied": False,
        "c38_track_used": False,
        "policy": (
            "C41只消费显式内外卦与入内卦年数；"
            "不从积年重算宫卦，不调用C38，也不使用旧+34/+50偏移。"
        ),
    }


def dayou_epoch_variants() -> dict[str, Any]:
    """只列积年见证差异，不选择 epoch 公式。"""
    return {
        "canonical": C41_VERSION,
        "variants": copy.deepcopy(EPOCH_VARIANTS),
        "canonical_selected": None,
        "cross_source_merge": False,
        "runtime_uses_epoch_variant": False,
        "policy": (
            "重卦结构已可直接计算；积年换算另有来源分歧。"
            "C41在分歧解决前只接受显式内外卦，不选择任一epoch。"
        ),
    }
