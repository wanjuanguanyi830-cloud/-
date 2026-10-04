"""文昌九星的外部参校见证。

本模块不生成《太乙紫庭经》primary_result。
它只保存当前能直接定位的《三才世纬》卷八十一与《太乙统宗宝鉴》卷六见证，
用于比较星名、值宫年限和推步算法异文。
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
}


def wenchang_nine_stars_collation_witnesses() -> dict[str, Any]:
    """返回参校见证，不选择 canonical。"""
    witnesses = [
        copy.deepcopy(SANCAI_SHIWEI_WITNESS),
        copy.deepcopy(TONGZONG_CADAL_WITNESS),
        copy.deepcopy(TONGZONG_NGJ_WITNESS),
    ]
    return {
        "schema_version": "1.0",
        "canonical": WENCHANG_NINE_STARS_COLLATION_VERSION,
        "rule_key": "wenchang_nine_stars",
        "primary_source_target": "zitingjing",
        "primary_evidence_level": "catalog_attested_text_pending",
        "primary_result": None,
        "canonical_selected": None,
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
                "status": "unresolved",
                "values_seen": [10, 30],
                "critical_note": (
                    "统宗CADAL同一见证出现“每星十年一宫”与“宫率三十、小周270、大周2700”并存；"
                    "不得据单句固化值宫周期。"
                ),
            },
        },
        "policy": (
            "这些文本只能作为文昌九星的外部参校见证；"
            "在取得《太乙紫庭秘诀》附录直接正文前，不生成紫庭primary_result，"
            "也不实现10年或30年的canonical推步。"
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
        "canonical_selected": None,
        "cycle_rate_resolved": False,
        "policy": "统宗不同在线见证自身存在星名/周期异文，不在参校层强行择一。",
    }


def sancai_shiwei_wenchang_collation_payload() -> dict[str, Any]:
    """供 C18 source container 的《三才世纬》外部参校使用。"""
    return copy.deepcopy(SANCAI_SHIWEI_WITNESS)
