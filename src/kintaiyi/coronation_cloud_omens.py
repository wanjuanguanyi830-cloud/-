"""C51 帝王登位旁云气生克 / 干支数观察层。

来源：C50“明太乙历数之期术”末段登位日月旁云气。
本模块只解释显式云色与登位日干支的五行关系，不生成帝王终年。
"""

from __future__ import annotations

import copy
from typing import Any

from .dayou_lishu import najia_number
from .taiyi_lishu_evidence import CORONATION_CLOUD_NUMBERS, coronation_cloud_evidence
from .volume9_ehui import parse_ganzhi

C51_VERSION = "taiyi-c51-coronation-cloud-omens-v1"

STEM_ELEMENT = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

BRANCH_ELEMENT = {
    "寅": "木", "卯": "木",
    "巳": "火", "午": "火",
    "申": "金", "酉": "金",
    "亥": "水", "子": "水",
    "辰": "土", "戌": "土", "丑": "土", "未": "土",
}

ELEMENT_GENERATES = {
    "木": "火",
    "火": "土",
    "土": "金",
    "金": "水",
    "水": "木",
}

ELEMENT_CONTROLS = {
    "木": "土",
    "土": "水",
    "水": "火",
    "火": "金",
    "金": "木",
}

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "volume": 10,
    "parent_section": "明太乙历数之期术",
    "subsection": "天子初登位日月旁云气生克",
    "direct_rules": [
        "云生日者，国祚昌，多子",
        "云生辰者，内宫享福，多女",
        "云克日者，绝嗣",
        "日生云及比和者，皆吉",
        "阴云位祚不久",
        "五色彩云国代绵远寿昌，子孙兴旺",
        "以干为日，以支为辰",
    ],
    "element_mapping_collation": "五行大义·论配支干",
}

RELATION_EFFECTS = {
    "云生日": ["国祚昌", "多子"],
    "云生辰": ["内宫享福", "多女"],
    "云克日": ["绝嗣"],
    "日生云": ["吉"],
    "比和": ["吉"],
}

FORM_EFFECTS = {
    "阴云": ["位祚不久"],
    "五色彩云": ["国代绵远寿昌", "子孙兴旺"],
}

LEGACY_REFERENCE_AUDIT = {
    "function": "guiyun.yunqi_zhanbo",
    "canonical_equivalent": False,
    "issues": [
        "旧函数只取日干五行，没有真正计算日支（辰）五行",
        "旧“云生辰”分支实际用日干反向生云判断，语义错位",
        "旧_GAN_NUM把己列为4，与已校C42甲己子午九冲突",
        "旧云色只保存单数，未保留五行生数/成数双值",
        "旧函数用if/elif压成单一断语，无法同时保存多个成立关系",
    ],
}


def _relation_flags(cloud_element: str, day_element: str, chen_element: str) -> dict[str, bool]:
    return {
        "云生日": ELEMENT_GENERATES[cloud_element] == day_element,
        "云生辰": ELEMENT_GENERATES[cloud_element] == chen_element,
        "云克日": ELEMENT_CONTROLS[cloud_element] == day_element,
        "日生云": ELEMENT_GENERATES[day_element] == cloud_element,
        "比和": day_element == cloud_element,
    }


def coronation_cloud_omens(
    *,
    day_ganzhi: str,
    cloud_color: str,
    cloud_form: str | None = None,
) -> dict[str, Any]:
    """按“干为日、支为辰”分别判断云气生克。"""
    gz = parse_ganzhi(day_ganzhi)
    if cloud_form not in (None, "阴云", "五色彩云"):
        raise ValueError("cloud_form须为阴云/五色彩云或None")

    cloud = coronation_cloud_evidence(cloud_color)
    cloud_element = cloud["element"]
    day_element = STEM_ELEMENT[gz["stem"]]
    chen_element = BRANCH_ELEMENT[gz["branch"]]

    flags = _relation_flags(cloud_element, day_element, chen_element)
    relations = []
    effects = []
    for name in ("云生日", "云生辰", "云克日", "日生云", "比和"):
        if flags[name]:
            relations.append(name)
            effects.extend(RELATION_EFFECTS[name])

    form_effects = copy.deepcopy(FORM_EFFECTS.get(cloud_form, []))

    stem_number = najia_number(gz["stem"])
    branch_number = najia_number(gz["branch"])
    ganzhi_sum = stem_number + branch_number

    return {
        "schema_version": "1.0",
        "canonical": C51_VERSION,
        "rule_id": "C51-CLOUD-OMEN",
        "source_profile": "tongzong_volume10_coronation_cloud",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "day_ganzhi": gz,
        "day_element": day_element,
        "chen_element": chen_element,
        "cloud": cloud,
        "relation_flags": flags,
        "relations": relations,
        "relation_effects": effects,
        "cloud_form": cloud_form,
        "form_effects": form_effects,
        "ganzhi_numbers": {
            "stem": stem_number,
            "branch": branch_number,
            "sum": ganzhi_sum,
            "source_dependency": "C42纳甲干支数表",
        },
        "cloud_number_selection": None,
        "cloud_number_selection_status": "sheng_cheng_pair_unselected",
        "time_scale": None,
        "time_scale_status": (
            "source_mentions_year_month_day_hour_scales_but_no_unique_selection_rule"
        ),
        "specific_period": None,
        "overall_single_verdict": None,
        "policy": (
            "日=日干、辰=日支，分别比较五行。"
            "五种生克关系可同时成立时并列保存，不用if/elif压成单一断语。"
            "干支数只求和；云气生数/成数与年/月/日时尺度均不擅自选取。"
        ),
    }


def c51_catalog() -> dict[str, Any]:
    return {
        "canonical": C51_VERSION,
        "rule_id": "C51-CLOUD-OMEN",
        "source_profile": "tongzong_volume10_coronation_cloud",
        "stem_elements": copy.deepcopy(STEM_ELEMENT),
        "branch_elements": copy.deepcopy(BRANCH_ELEMENT),
        "cloud_numbers": copy.deepcopy(CORONATION_CLOUD_NUMBERS),
        "relation_effects": copy.deepcopy(RELATION_EFFECTS),
        "legacy_reference_audit": copy.deepcopy(LEGACY_REFERENCE_AUDIT),
    }
