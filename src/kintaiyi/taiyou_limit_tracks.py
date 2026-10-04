"""C38 阳九 / 百六下的太游内外卦行限轨迹。

直接来源：
- 阳九：太游理外卦，10年一宫，80年一竟，57竟=4560；
- 百六：太游理内卦，36年一宫，288年一竟，15竟=4320；
- 宫序起七宫坤，顺行八宫，不入中五：
  7坤 -> 8坎 -> 9巽 -> 1乾 -> 2离 -> 3艮 -> 4震 -> 6兑。

本模块复用 C36 的限周期/盈差，不采用旧 guiyun.py 另外的 +34/+50 轨运偏移。
"""

from __future__ import annotations

from typing import Any

from .limit_cycles import bailiu_limit, yangjiu_limit
from .taiyi_rules import integer

C38_VERSION = "taiyi-c38-taiyou-limit-tracks-v1"

TAIYOU_PALACE_PATH = (7, 8, 9, 1, 2, 3, 4, 6)
TAIYOU_TRIGRAM_PATH = ("坤", "坎", "巽", "乾", "离", "艮", "震", "兑")

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "sections": [
        "明阳九百六太游行限观历术",
        "明太游太乙轨运入内卦所在术",
        "明太游轨运入外卦所在术",
    ],
    "volume_notes": {
        "limit_observation_witness": 10,
        "track_formula_witness": 9,
    },
    "policy": "卷九/卷十为相邻术文与见证编次差异；按条文职责分层，不复制算法。",
}


def _track_from_limit(
    limit: dict[str, Any],
    *,
    track_name: str,
    years_per_palace: int,
    years_per_round: int,
    rounds_per_big_limit: int,
    rule_id: str,
) -> dict[str, Any]:
    cycle_year = (
        limit["big_limit"]
        if limit["cycle_remainder"] == 0
        else limit["cycle_remainder"]
    )
    round_index = (cycle_year - 1) // years_per_round + 1
    year_in_round = (cycle_year - 1) % years_per_round + 1
    palace_index = (year_in_round - 1) // years_per_palace
    year_in_palace = (year_in_round - 1) % years_per_palace + 1

    palace = TAIYOU_PALACE_PATH[palace_index]
    trigram = TAIYOU_TRIGRAM_PATH[palace_index]

    return {
        "rule_id": rule_id,
        "canonical": C38_VERSION,
        "source_profile": "tongzong_taiyou_limit_tracks",
        "source_witness": dict(SOURCE_WITNESS),
        "track": track_name,
        "limit_rule_id": limit["rule_id"],
        "big_limit": limit["big_limit"],
        "years_per_palace": years_per_palace,
        "years_per_round": years_per_round,
        "rounds_per_big_limit": rounds_per_big_limit,
        "cycle_year": cycle_year,
        "round_index": round_index,
        "year_in_round": year_in_round,
        "palace_index": palace_index + 1,
        "palace": palace,
        "trigram": trigram,
        "year_in_palace": year_in_palace,
        "palace_complete": year_in_palace == years_per_palace,
        "round_complete": year_in_round == years_per_round,
        "big_limit_complete": cycle_year == limit["big_limit"],
        "path": [
            {"palace": p, "trigram": g}
            for p, g in zip(TAIYOU_PALACE_PATH, TAIYOU_TRIGRAM_PATH)
        ],
        "policy": (
            "轨迹以C36同一限周期的adjusted remainder为时间轴；"
            "不借旧guiyun +34/+50偏移改写本条阳九/百六行限。"
        ),
    }


def yangjiu_outer_track(accumulated_year: int) -> dict[str, Any]:
    """阳九外卦：10年一宫，80年一竟，57竟=4560。"""
    accumulated_year = integer(accumulated_year)
    return _track_from_limit(
        yangjiu_limit(accumulated_year),
        track_name="阳九外卦",
        years_per_palace=10,
        years_per_round=80,
        rounds_per_big_limit=57,
        rule_id="C38-YJ-OUTER",
    )


def bailiu_inner_track(accumulated_year: int) -> dict[str, Any]:
    """百六内卦：36年一宫，288年一竟，15竟=4320。"""
    accumulated_year = integer(accumulated_year)
    return _track_from_limit(
        bailiu_limit(accumulated_year),
        track_name="百六内卦",
        years_per_palace=36,
        years_per_round=288,
        rounds_per_big_limit=15,
        rule_id="C38-BL-INNER",
    )


def taiyou_limit_tracks(accumulated_year: int) -> dict[str, Any]:
    """构建可嵌入 cycles.limits.taiyou_tracks 的双轨结构。"""
    accumulated_year = integer(accumulated_year)
    return {
        "canonical": C38_VERSION,
        "source_profile": "tongzong_taiyou_limit_tracks",
        "yangjiu_outer": yangjiu_outer_track(accumulated_year),
        "bailiu_inner": bailiu_inner_track(accumulated_year),
        "cross_track_merge": False,
        "policy": (
            "外卦专属阳九、内卦专属百六；"
            "二者共享太游八宫序，但使用各自C36限周期与盈差。"
        ),
    }
