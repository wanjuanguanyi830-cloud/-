"""文昌九星多见证校勘层。

当前稳定可执行规则为《太乙统宗宝鉴》卷六 NGJ profile（C70）。
本模块同时保存《三才世纬》与统宗 CADAL/NGJ 的星名、值宫年限与算法异文。
研易楼明钞本目录未见文昌九星题名；现代整理本同名附篇来源未证，
因此这里不再等待“紫庭 primary”，也不把现代附篇反推成原钞正文。
"""

from __future__ import annotations

import copy
from typing import Any

WENCHANG_NINE_STARS_COLLATION_VERSION = "wenchang-nine-stars-collation-v1"

SANCAI_SHIWEI_WITNESS = {
    "source_id": "sancai_shiwei_volume81",
    "title": "三才世纬",
    "author": "[明]佚名",
    "volume": 81,
    "section": "求文昌九宫所主分野",
    "url": "https://www.shidianguji.com/book/NCL06493A/chapter/1lz8dgqey7eor",
    "source_class": "external_collation",
    "star_names_reading": [
        "文昌", "玄凤", "明雄", "阴玄", "招摇",
        "华明", "玄武", "玄冥", "雄明",
    ],
    "direct_facts": {
        "palace_count": 9,
        "derivation_phrase": "以三乘三而得九宫，故有九星之名；又以三乘九而得二十有七",
        "placement_basis": "命加所求年干建禄之宫，视所临分野",
        "stem_disaster_groups": ["甲乙", "丙丁", "庚辛", "壬癸", "戊己"],
    },
    "cycle_rate": None,
    "cycle_rate_status": "not_fixed_from_current_witness_excerpt",
}

TONGZONG_CADAL_WITNESS = {
    "source_id": "tongzong_volume6_cadal02094393",
    "title": "太乙统宗宝鉴",
    "author": "[元]晓山老人",
    "volume": 6,
    "section": "明文昌九宫所主分野术",
    "url": "https://www.shidianguji.com/zh/book/CADAL02094393/chapter/1lcppwupo1s0a",
    "source_class": "collation",
    # 保留当前电子见证读法；“招煥”等可能是OCR/底本异字，不在此无痕归一。
    "star_names_reading": [
        "文昌", "玄凤", "明雄", "阴德", "招煥",
        "华明", "玄武", "玄冥", "雄明",
    ],
    "cycle_evidence": {
        "prose_rate_years_per_palace": 10,
        "algorithm_rate_years_per_palace": 30,
        "small_cycle_years": 270,
        "large_cycle_years": 2700,
        "internal_conflict": True,
        "note": "同一电子见证前文作每星十年一宫，后文推法以宫率三十并列小周270/大周2700。",
    },
}

TONGZONG_NGJ_WITNESS = {
    "source_id": "tongzong_volume6_ngj",
    "title": "太乙统宗宝鉴",
    "author": "[元]晓山老人",
    "volume": 6,
    "section": "明文昌九宫所主分野术",
    "url": "https://www.shidianguji.com/zh/book/NGJ892411999009267118912/chapter/1lny526c1g8iw",
    "source_class": "collation",
    # 当前在线见证有“明維 / 維明”等读法；照录，不替它改成另一版“明雄 / 雄明”。
    "star_names_reading": [
        "文昌", "玄凤", "明维", "阴德", "招摇",
        "华明", "玄武", "玄冥", "维明",
    ],
    "palace_table": [
        {"index": 1, "name": "文昌", "palace": "乾", "stem": "壬", "region": "冀州"},
        {"index": 2, "name": "玄凤", "palace": "离", "stem": "丁", "region": "荆州"},
        {"index": 3, "name": "明维", "palace": "艮", "stem": "甲", "region": "青州"},
        {"index": 4, "name": "阴德", "palace": "震", "stem": "乙", "region": "徐州"},
        {"index": 5, "name": "招摇", "palace": "中", "stem": "戊己", "region": "豫州"},
        {"index": 6, "name": "华明", "palace": "兑", "stem": "辛", "region": "雍州"},
        {"index": 7, "name": "玄武", "palace": "坤", "stem": "庚", "region": "梁益州"},
        {"index": 8, "name": "玄冥", "palace": "坎", "stem": "癸", "region": "兖州"},
        {"index": 9, "name": "维明", "palace": "巽", "stem": "丙", "region": "扬州"},
    ],
    "cycle_evidence": {
        "prose_rate_years_per_palace": 30,
        "algorithm_rate_years_per_palace": 30,
        "small_cycle_years": 270,
        "large_cycle_years": 2700,
        "internal_conflict": False,
    },
    "source_specific_runtime": {
        "rule_id": "C70-TONGZONG-WENCHANG-NINE-STARS",
        "module": "wenchang_nine_stars_tongzong",
        "available": True,
        "selected_stable_profile": True,
        "zitingjing_primary_result": False,
    },
}


def wenchang_nine_stars_collation_witnesses() -> dict[str, Any]:
    """返回文昌九星多见证校勘，并声明当前稳定 C70 profile。"""
    witnesses = [
        copy.deepcopy(SANCAI_SHIWEI_WITNESS),
        copy.deepcopy(TONGZONG_CADAL_WITNESS),
        copy.deepcopy(TONGZONG_NGJ_WITNESS),
    ]
    return {
        "schema_version": "1.0",
        "canonical": WENCHANG_NINE_STARS_COLLATION_VERSION,
        "rule_key": "wenchang_nine_stars",
        "stable_rule_id": "C70-TONGZONG-WENCHANG-NINE-STARS",
        "stable_source_profile": "tongzong_volume6_ngj_wenchang_nine_stars",
        "canonical_selected": "tongzong_volume6_ngj",
        "ziting_manuscript": {
            "status": "toc_title_not_attested",
            "toc_pages": [5, 6],
            "primary_result": None,
        },
        "modern_edition_appendix": {
            "title": "附太乙文昌九星值宫术",
            "status": "catalog_attested_provenance_unresolved",
        },
        "source_specific_runtimes": [
            {
                "source_id": "tongzong_volume6_ngj",
                "rule_id": "C70-TONGZONG-WENCHANG-NINE-STARS",
                "source_profile": "tongzong_volume6_ngj_wenchang_nine_stars",
                "selected_stable_profile": True,
            }
        ],
        "witnesses": witnesses,
        "variant_conflicts": {
            "star_names": {
                "status": "conflicting_readings",
                "examples": [
                    "三才世纬：明雄 / 阴玄 / 雄明",
                    "统宗CADAL：明雄 / 阴德 / 雄明",
                    "统宗NGJ：明维 / 阴德 / 维明",
                ],
            },
            "cycle_rate": {
                "status": "cross_witness_conflict_selected_profile_resolved",
                "values_seen": [10, 30],
                "selected_profile_value": 30,
                "critical_note": (
                    "统宗CADAL同一见证出现“每星十年一宫”与“宫率三十、小周270、大周2700”并存；"
                    "C70只对NGJ见证固定30年，不把该选择覆盖到其他见证。"
                ),
            },
        },
        "policy": (
            "C70按统宗NGJ直接见证独立运行；CADAL与《三才世纬》只作异文参校。"
            "研易楼明钞目录未见文昌九星题名，现代整理附篇来源未证。"
        ),
    }


def tongzong_volume6_wenchang_collation_payload() -> dict[str, Any]:
    """供 C18 source container 的 tongzong_volume6 collation_result 使用。"""
    return {
        "source_id": "tongzong_volume6",
        "witnesses": [
            copy.deepcopy(TONGZONG_CADAL_WITNESS),
            copy.deepcopy(TONGZONG_NGJ_WITNESS),
        ],
        "canonical_selected": "tongzong_volume6_ngj",
        "selected_source_profile": "tongzong_volume6_ngj_wenchang_nine_stars",
        "cycle_rate_resolved_for_selected_profile": True,
        "cross_witness_cycle_conflict": True,
        "policy": "C70选择NGJ作为当前稳定可执行profile；CADAL内部10/30年冲突继续并列，不被NGJ选择覆盖。",
    }


def sancai_shiwei_wenchang_collation_payload() -> dict[str, Any]:
    """供 C18 source container 的《三才世纬》外部参校使用。"""
    return copy.deepcopy(SANCAI_SHIWEI_WITNESS)
