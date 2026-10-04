"""C46 《太乙统宗宝鉴》阴阳九厄水旱灾期。

九段长度合计4560；旧 guiyun.yinyang_jiu_e 把各段长度误当逐项累计阈值。
本模块按段长先构造累计边界，再定位当前厄会。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer

C46_VERSION = "taiyi-c46-yinyang-nine-calamities-v1"

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "online_witness_volume": 10,
    "project_legacy_volume_label": 9,
    "volume_status": "witness_volume_variant",
    "section": "明阴阳九厄水厄旱灾期术",
}

# duration_years 是每一“历”的长度，不是累计终点。
CALAMITY_SEGMENTS = (
    {"index": 1, "name": "一阳九灾", "duration_years": 106, "polarity": "阳", "disaster_years": 9, "disaster": "旱"},
    {"index": 2, "name": "二阴九灾", "duration_years": 374, "polarity": "阴", "disaster_years": 9, "disaster": "水"},
    {"index": 3, "name": "三阳九灾", "duration_years": 480, "polarity": "阳", "disaster_years": 9, "disaster": "旱"},
    {"index": 4, "name": "四阴七灾", "duration_years": 720, "polarity": "阴", "disaster_years": 7, "disaster": "水"},
    {"index": 5, "name": "五阳七灾", "duration_years": 720, "polarity": "阳", "disaster_years": 7, "disaster": "旱"},
    {"index": 6, "name": "六阴五灾", "duration_years": 600, "polarity": "阴", "disaster_years": 5, "disaster": "水"},
    {"index": 7, "name": "七阳五灾", "duration_years": 600, "polarity": "阳", "disaster_years": 5, "disaster": "旱"},
    {"index": 8, "name": "八阴三灾", "duration_years": 480, "polarity": "阴", "disaster_years": 3, "disaster": "水"},
    {"index": 9, "name": "九阳三灾", "duration_years": 480, "polarity": "阳", "disaster_years": 3, "disaster": "旱"},
)

TEXTUAL_NOTES = {
    "fourth_duration": {
        "online_witnesses": [702, 720],
        "normalized_duration_years": 720,
        "reason": (
            "部分在线见证OCR见七百二年，另见证明确七百二十年；"
            "九段采用720时总长恰为阳九一元4560，采用702则仅4542。"
        ),
        "status": "ocr_corrected_by_parallel_witness_and_internal_arithmetic",
    },
    "fourth_label": {
        "online_ocr": "四阳七灾水七年",
        "normalized": "四阴七灾水七年",
        "reason": "本术明确五阳主旱、四阴主水；第四会为水厄，且九会阴阳交错。",
        "status": "ocr_corrected_by_internal_structure",
    },
    "ninth_disaster_years": {
        "online_ocr": "九阳三灾旱五年",
        "normalized_disaster_years": 3,
        "reason": (
            "同句名为“三灾”，且全篇明言九厄灾年共57；"
            "9+9+9+7+7+5+5+3+3=57，若末段取5则为59。"
        ),
        "status": "ocr_corrected_by_internal_arithmetic",
    },
}

LEGACY_REFERENCE_AUDIT = {
    "function": "guiyun.yinyang_jiu_e",
    "canonical_equivalent": False,
    "issues": [
        "把106/374/480/720等每段长度直接当累计阈值比较",
        "循环中虽定义cumulative但未用于边界累计",
        "会导致第二段以后区段定位错误",
        "未保留第四段阴/阳OCR冲突与第九段3/5灾年冲突",
    ],
}


def calamity_timeline() -> list[dict[str, Any]]:
    """把九段长度展开成1..4560的累计区间。"""
    rows = []
    start = 1
    for raw in CALAMITY_SEGMENTS:
        row = copy.deepcopy(raw)
        end = start + row["duration_years"] - 1
        row["start_year"] = start
        row["end_year"] = end
        row["disaster_start_year"] = end - row["disaster_years"] + 1
        row["disaster_end_year"] = end
        rows.append(row)
        start = end + 1
    return rows


def yinyang_nine_calamities(accumulated_year: int) -> dict[str, Any]:
    """按积年+阳盈差130定位九厄。

    0余数视为一元第4560年，而不是下一元第0年。
    """
    accumulated_year = integer(accumulated_year)
    adjusted = accumulated_year + 130
    remainder = adjusted % 4560
    cycle_year = remainder or 4560

    selected = None
    for row in calamity_timeline():
        if row["start_year"] <= cycle_year <= row["end_year"]:
            selected = row
            break
    if selected is None:
        raise RuntimeError("C46九厄时间轴内部错误")

    year_in_segment = cycle_year - selected["start_year"] + 1
    years_to_segment_end = selected["end_year"] - cycle_year
    in_disaster = cycle_year >= selected["disaster_start_year"]
    disaster_year_index = (
        cycle_year - selected["disaster_start_year"] + 1
        if in_disaster
        else None
    )

    return {
        "schema_version": "1.0",
        "canonical": C46_VERSION,
        "rule_id": "C46-YJ-9E",
        "source_profile": "tongzong_yinyang_nine_calamities",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "accumulated_year": accumulated_year,
        "surplus_offset": 130,
        "adjusted_year": adjusted,
        "cycle_length": 4560,
        "cycle_remainder": remainder,
        "cycle_year": cycle_year,
        "current_segment": selected,
        "year_in_segment": year_in_segment,
        "years_to_segment_end": years_to_segment_end,
        "in_disaster_period": in_disaster,
        "disaster_year_index": disaster_year_index,
        "timeline": calamity_timeline(),
        "total_segment_years": sum(item["duration_years"] for item in CALAMITY_SEGMENTS),
        "total_disaster_years": sum(item["disaster_years"] for item in CALAMITY_SEGMENTS),
        "yang_count": sum(item["polarity"] == "阳" for item in CALAMITY_SEGMENTS),
        "yin_count": sum(item["polarity"] == "阴" for item in CALAMITY_SEGMENTS),
        "textual_notes": copy.deepcopy(TEXTUAL_NOTES),
        "legacy_threshold_formula_used": False,
        "policy": (
            "九段106/374/480/720/720/600/600/480/480按各段长度累计；"
            "灾期取每段末尾对应9/7/5/3年。"
            "第四段阴阳字与末段3/5年冲突保留OCR witness并按篇内结构/算术正规化。"
        ),
    }


def c46_catalog() -> dict[str, Any]:
    timeline = calamity_timeline()
    return {
        "canonical": C46_VERSION,
        "rule_id": "C46-YJ-9E",
        "source_profile": "tongzong_yinyang_nine_calamities",
        "segment_count": len(timeline),
        "total_segment_years": sum(row["duration_years"] for row in timeline),
        "total_disaster_years": sum(row["disaster_years"] for row in timeline),
        "yang_count": sum(row["polarity"] == "阳" for row in timeline),
        "yin_count": sum(row["polarity"] == "阴" for row in timeline),
        "legacy_reference_audit": copy.deepcopy(LEGACY_REFERENCE_AUDIT),
    }
