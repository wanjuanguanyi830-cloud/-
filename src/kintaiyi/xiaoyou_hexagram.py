"""C47 《太乙统宗宝鉴》卷九小游轨运、重卦与动爻。

直接来源：
- 明小游轨运内卦所在术
- 明小游轨运外卦所在术
- 明小游内外相重之策术

边界：
- 小游不与C38阳九/百六太游行限混并；
- 不使用大游+34/+50等旧偏移；
- 不命名六十四卦，只保存上/下经卦结构；
- 四象策数只复用C41已校的共享数表，不复用C41积年算法。
"""

from __future__ import annotations

import copy
from typing import Any

from .dayou_hexagram import FOUR_IMAGE_CE
from .taiyi_rules import integer

C47_VERSION = "taiyi-c47-xiaoyou-hexagram-v1"

XIAOYOU_TRIGRAM_PATH = ("乾", "离", "艮", "震", "兑", "坤", "坎", "巽")

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "volume": 9,
    "sections": [
        "明小游轨运内卦所在术",
        "明小游轨运外卦所在术",
        "明小游内外相重之策术",
    ],
    "inner": {
        "big_cycle": 1920,
        "small_cycle": 192,
        "years_per_trigram": 24,
        "path": list(XIAOYOU_TRIGRAM_PATH),
        "ocr_note": (
            "统宗在线一见证大周数字OCR残缺；《太白兵备统宗宝鉴》"
            "明确见一千九百二十、小周一百九十二、率二十四。"
        ),
    },
    "outer": {
        "epoch_cycle": 360,
        "trigram_cycle": 24,
        "years_per_trigram": 3,
        "path": list(XIAOYOU_TRIGRAM_PATH),
        "combined_hexagram_cycle": 192,
        "cycle_note": (
            "统宗公式层保留纪元360与八卦小周24；"
            "参校说明三年一外卦，内外组合周六十四卦经192年。"
        ),
    },
}


def _cycle_year(value: int, cycle: int) -> int:
    """把整除余0正规化为该周期末年，而不是下一周期首年。"""
    remainder = value % cycle
    return cycle if remainder == 0 else remainder


def _track(
    cycle_year: int,
    *,
    years_per_trigram: int,
) -> dict[str, Any]:
    index = (cycle_year - 1) // years_per_trigram
    year_in_trigram = (cycle_year - 1) % years_per_trigram + 1
    trigram = XIAOYOU_TRIGRAM_PATH[index]
    return {
        "trigram_index": index + 1,
        "trigram": trigram,
        "year_in_trigram": year_in_trigram,
        "trigram_complete": year_in_trigram == years_per_trigram,
    }


def xiaoyou_inner_track(accumulated_year: int) -> dict[str, Any]:
    """小游内卦：大周1920，小周192，每24年一经卦。"""
    year = integer(accumulated_year, 1)
    big_cycle_year = _cycle_year(year, 1920)
    small_cycle_year = _cycle_year(big_cycle_year, 192)
    track = _track(small_cycle_year, years_per_trigram=24)

    moving_line = (track["year_in_trigram"] - 1) // 4 + 1
    line_start = (moving_line - 1) * 4 + 1
    line_end = moving_line * 4

    return {
        "schema_version": "1.0",
        "canonical": C47_VERSION,
        "rule_id": "C47-XY-INNER",
        "source_profile": "tongzong_volume9_xiaoyou",
        "accumulated_year": year,
        "big_cycle": 1920,
        "big_cycle_year": big_cycle_year,
        "small_cycle": 192,
        "small_cycle_year": small_cycle_year,
        "years_per_trigram": 24,
        **track,
        "moving_line": moving_line,
        "moving_line_year_range": [line_start, line_end],
        "moving_line_complete": track["year_in_trigram"] == line_end,
        "path": list(XIAOYOU_TRIGRAM_PATH),
        "source_witness": copy.deepcopy(SOURCE_WITNESS["inner"]),
        "policy": "二十四年一内卦，四年行一爻；不加大游宫盈差。",
    }


def xiaoyou_outer_track(accumulated_year: int) -> dict[str, Any]:
    """小游外卦：纪元360，八卦小周24，每3年一经卦。"""
    year = integer(accumulated_year, 1)
    epoch_cycle_year = _cycle_year(year, 360)
    trigram_cycle_year = _cycle_year(epoch_cycle_year, 24)
    track = _track(trigram_cycle_year, years_per_trigram=3)
    three_talent = ("理天", "理地", "理人")[track["year_in_trigram"] - 1]

    return {
        "schema_version": "1.0",
        "canonical": C47_VERSION,
        "rule_id": "C47-XY-OUTER",
        "source_profile": "tongzong_volume9_xiaoyou",
        "accumulated_year": year,
        "epoch_cycle": 360,
        "epoch_cycle_year": epoch_cycle_year,
        "trigram_cycle": 24,
        "trigram_cycle_year": trigram_cycle_year,
        "years_per_trigram": 3,
        **track,
        "three_talent": three_talent,
        "path": list(XIAOYOU_TRIGRAM_PATH),
        "source_witness": copy.deepcopy(SOURCE_WITNESS["outer"]),
        "policy": (
            "三年一外卦：第一年理天、第二年理地、第三年理人。"
            "纪元360与八卦小周24分层保存，不压成单一周期。"
        ),
    }


def _ce(trigram: str) -> dict[str, Any]:
    base = FOUR_IMAGE_CE[trigram]
    return {
        "trigram": trigram,
        "four_image": base["four_image"],
        "per_line_ce": base["ce"],
        "trigram_ce": base["ce"] * 3,
        "source_dependency": "C41共享四象策数表",
    }


def xiaoyou_heavy_hexagram(accumulated_year: int) -> dict[str, Any]:
    """组合小游上下卦、内卦动爻、外卦三才与策数结构。"""
    inner = xiaoyou_inner_track(accumulated_year)
    outer = xiaoyou_outer_track(accumulated_year)
    inner_ce = _ce(inner["trigram"])
    outer_ce = _ce(outer["trigram"])

    return {
        "schema_version": "1.0",
        "canonical": C47_VERSION,
        "rule_id": "C47-XY-HEX",
        "source_profile": "tongzong_volume9_xiaoyou",
        "accumulated_year": integer(accumulated_year, 1),
        "inner": inner,
        "outer": outer,
        "structure": {
            "upper_trigram": outer["trigram"],
            "lower_trigram": inner["trigram"],
            "display": f'{outer["trigram"]}上{inner["trigram"]}下',
        },
        "inner_moving_line": inner["moving_line"],
        "outer_moving_line": None,
        "outer_moving_line_status": "not_used_by_source_rule",
        "three_talent": outer["three_talent"],
        "ce": {
            "inner": inner_ce,
            "outer": outer_ce,
            "total": inner_ce["trigram_ce"] + outer_ce["trigram_ce"],
        },
        "hexagram_name": None,
        "hexagram_name_status": "not_resolved_in_c46",
        "c38_track_used": False,
        "dayou_epoch_offset_used": False,
        "policy": (
            "以内卦画下、外卦画上；动爻只取小游内卦四年一爻。"
            "不调用C38，不使用大游epoch偏移，不强制命名六十四卦。"
        ),
    }


def xiaoyou_source_profile() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "canonical": C47_VERSION,
        "source_profile": "tongzong_volume9_xiaoyou",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "path": list(XIAOYOU_TRIGRAM_PATH),
        "inner_big_cycle": 1920,
        "inner_small_cycle": 192,
        "inner_rate": 24,
        "outer_epoch_cycle": 360,
        "outer_trigram_cycle": 24,
        "outer_rate": 3,
        "combined_hexagram_cycle": 192,
        "cross_dayou_merge": False,
        "cross_c38_merge": False,
    }
