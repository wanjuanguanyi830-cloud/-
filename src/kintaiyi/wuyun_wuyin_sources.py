"""C37 《太乙统宗宝鉴》卷三 / 卷十五运六气与五音之数来源拆分。

重点：
- 五运六气：卷三“统行”与卷十“岁会”分 profile；
- 五音之数：只属卷三，不再误标为卷三/卷十混合；
- D8-03 只作为“算数 -> 五音”共同核心 crosswalk，不与 D8-08 数有所主混淆。
"""

from __future__ import annotations

import copy
from typing import Any

from .eight_divinations import wuyin_from_calc
from .wuyun_volume10_collation import volume10_wuyun_collation

C37_VERSION = "taiyi-c37-wuyun-wuyin-sources-v1"

STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")

FIVE_MOVEMENT_BY_STEM = {
    "甲": "土", "己": "土",
    "乙": "金", "庚": "金",
    "丙": "水", "辛": "水",
    "丁": "木", "壬": "木",
    "戊": "火", "癸": "火",
}

SIX_QI_BY_BRANCH = {
    "子": {"qi": "少阴", "transformation": "热"},
    "午": {"qi": "少阴", "transformation": "热"},
    "丑": {"qi": "太阴", "transformation": "湿"},
    "未": {"qi": "太阴", "transformation": "湿"},
    "寅": {"qi": "少阳", "transformation": "相火"},
    "申": {"qi": "少阳", "transformation": "相火"},
    "卯": {"qi": "阳明", "transformation": "燥"},
    "酉": {"qi": "阳明", "transformation": "燥"},
    "辰": {"qi": "太阳", "transformation": "寒"},
    "戌": {"qi": "太阳", "transformation": "寒"},
    "巳": {"qi": "厥阴", "transformation": "风"},
    "亥": {"qi": "厥阴", "transformation": "风"},
}

WUYIN_PAIR_TABLE = {
    (1, 2): {"tone": "宫", "element": "土", "subject": "人君"},
    (3, 4): {"tone": "徵", "element": "火", "subject": "宗庙"},
    (5, 6): {"tone": "羽", "element": "水", "subject": "后妃"},
    (7, 8): {"tone": "商", "element": "金", "subject": "子孙"},
    (9, 10): {"tone": "角", "element": "木", "subject": "疾病"},
}

SOURCE_PROFILES = {
    "tongzong_volume3_wuyun": {
        "work": "太乙统宗宝鉴",
        "volume": 3,
        "section": "明太乙统行五运六气术",
        "scope": "统行框架、五运、主气文昌、客气始击",
    },
    "tongzong_volume10_wuyun": {
        "work": "太乙统宗宝鉴",
        "volume": 10,
        "section": "明太乙岁会五运六气术",
        "scope": "岁会框架、五运六气、主客气及岁会天符关系",
    },
    "tongzong_volume3_wuyin": {
        "work": "太乙统宗宝鉴",
        "volume": 3,
        "section": "明五音之数以推休咎术／明太乙五音之元术",
        "scope": "算数五音休咎与五音之元",
    },
}


def _stem(value: str) -> str:
    if value not in STEMS:
        raise ValueError("year_stem须为十天干")
    return value


def _branch(value: str) -> str:
    if value not in BRANCHES:
        raise ValueError("year_branch须为十二地支")
    return value


def annual_movement(year_stem: str) -> dict[str, Any]:
    """年干 -> 五运，卷三/卷十共同基础。"""
    year_stem = _stem(year_stem)
    return {
        "year_stem": year_stem,
        "movement_element": FIVE_MOVEMENT_BY_STEM[year_stem],
        "movement": f"{FIVE_MOVEMENT_BY_STEM[year_stem]}运",
        "shared_core": True,
    }


def six_qi_assignment(year_branch: str) -> dict[str, Any]:
    """年支 -> 司天气及对宫在泉气；用于卷十岁会 profile。"""
    year_branch = _branch(year_branch)
    index = BRANCHES.index(year_branch)
    opposite = BRANCHES[(index + 6) % 12]
    sitian = SIX_QI_BY_BRANCH[year_branch]
    zaiquan = SIX_QI_BY_BRANCH[opposite]
    return {
        "year_branch": year_branch,
        "sitian": copy.deepcopy(sitian),
        "zaiquan_branch": opposite,
        "zaiquan": copy.deepcopy(zaiquan),
    }


def volume3_wuyun_profile(
    year_stem: str,
    *,
    host_eye: str | None = None,
    guest_eye: str | None = None,
) -> dict[str, Any]:
    """卷三“统行五运六气”profile；不偷带卷十岁会/天符算法。"""
    movement = annual_movement(year_stem)
    return {
        "schema_version": "1.0",
        "canonical": C37_VERSION,
        "rule_id": "C37-V3-WYUN",
        "source_profile": "tongzong_volume3_wuyun",
        "source": copy.deepcopy(SOURCE_PROFILES["tongzong_volume3_wuyun"]),
        "five_movement": movement,
        "host_qi": {
            "deity": "文昌",
            "role": "主气",
            "location": host_eye,
            "source_character": "静而守位",
        },
        "guest_qi": {
            "deity": "始击",
            "role": "客气",
            "location": guest_eye,
            "source_character": "动而不息",
        },
        "suihui_computed": False,
        "tianfu_computed": False,
        "policy": "卷三profile只保存统行主客气框架；岁会、天符留给卷十profile。",
    }


def volume10_wuyun_profile(
    year_stem: str,
    year_branch: str,
    *,
    host_eye: str | None = None,
    guest_eye: str | None = None,
) -> dict[str, Any]:
    """卷十“岁会五运六气”基础 profile。

    本批只结构化年干五运、年支六气与主客气；岁会/天符具体判表继续独立校勘。
    """
    movement = annual_movement(year_stem)
    six_qi = six_qi_assignment(year_branch)
    collation = volume10_wuyun_collation()
    return {
        "schema_version": "1.0",
        "canonical": C37_VERSION,
        "rule_id": "C37-V10-WYUN",
        "source_profile": "tongzong_volume10_wuyun",
        "source": copy.deepcopy(SOURCE_PROFILES["tongzong_volume10_wuyun"]),
        "five_movement": movement,
        "six_qi": six_qi,
        "host_qi": {"deity": "文昌", "role": "主气", "location": host_eye},
        "guest_qi": {"deity": "始击", "role": "客气", "location": guest_eye},
        "collation": collation,
        "suihui_relations": [],
        "suihui_status": "core_tables_collated_meeting_variant_pending",
        "meeting_enum_status": collation["meeting_enum_status"],
        "taiyi_tianfu_formula_status": collation["taiyi_tianfu_formula_status"],
        "year_stem_only_finalizes_taiguo_buji": False,
        "cross_volume_merge": False,
        "policy": (
            "卷十五运/六气/纪名细表已由C39校勘；"
            "天会、岁会、逆会、辐辏枚举仍有传本差异，"
            "太乙天符须待九宫天符/三旗等结构化输入后再判，"
            "不得退回旧综合函数或只凭年干判太过不及。"
        ),
    }


def volume3_wuyin_from_calc(calc: int) -> dict[str, Any]:
    """卷三五音之数：复用 D8-03 的已校核心映射，但另加卷三来源身份。"""
    d8 = wuyin_from_calc(calc)
    return {
        "schema_version": "1.0",
        "canonical": C37_VERSION,
        "rule_id": "C37-V3-WYIN",
        "source_profile": "tongzong_volume3_wuyin",
        "source": copy.deepcopy(SOURCE_PROFILES["tongzong_volume3_wuyin"]),
        "calc": calc,
        "tone": d8["tone"],
        "element": d8["element"],
        "subject": d8["subject"],
        "d8_crosswalk": {
            "rule_id": "D8-03",
            "formula_reused": True,
            "d8_result": copy.deepcopy(d8),
        },
        "number_subject_rule_d8_08_used": False,
        "policy": (
            "只复用D8-03算数到五音的共同核心；"
            "不得把D8-08数有所主（将军/吏士/兵卒）映射成五音。"
        ),
    }


def wuyin_origin_table() -> dict[str, Any]:
    """卷三“五音之元”已核的数对—音—五行—所象表。"""
    return {
        "schema_version": "1.0",
        "canonical": C37_VERSION,
        "source_profile": "tongzong_volume3_wuyin",
        "pairs": [
            {"numbers": list(pair), **copy.deepcopy(item)}
            for pair, item in WUYIN_PAIR_TABLE.items()
        ],
        "policy": "五音之元只属卷三；不因旧pan与五运六气同一大dict而并入卷十。",
    }


def build_wuyun_wuyin_source_variants(
    *,
    volume3_wuyun: dict[str, Any] | None = None,
    volume10_wuyun: dict[str, Any] | None = None,
    volume3_wuyin: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """构建 C30 source_variants.wuyun_wuyin。"""

    def checked(value: dict[str, Any] | None, profile: str, rule_id: str) -> dict[str, Any]:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise TypeError(f"{profile}结果须为dict")
        if value.get("source_profile") != profile or value.get("rule_id") != rule_id:
            raise ValueError(f"{profile}来源标记不匹配")
        return copy.deepcopy(value)

    v3 = checked(volume3_wuyun, "tongzong_volume3_wuyun", "C37-V3-WYUN")
    v10 = checked(volume10_wuyun, "tongzong_volume10_wuyun", "C37-V10-WYUN")
    wy = checked(volume3_wuyin, "tongzong_volume3_wuyin", "C37-V3-WYIN")

    wuyun_profiles = {
        **({"tongzong_volume3": v3} if v3 else {}),
        **({"tongzong_volume10": v10} if v10 else {}),
    }
    legacy_replacement = (
        {
            "source_split_complete": True,
            "required_profiles": ["tongzong_volume3", "tongzong_volume10"],
        }
        if v3 and v10
        else {}
    )

    return {
        "schema_version": "1.0",
        "canonical": C37_VERSION,
        "wuyun_liuqi": {
            "profiles": wuyun_profiles,
            "legacy_replacement": legacy_replacement,
            "cross_source_merge": False,
            "policy": (
                "卷三统行与卷十岁会分profile，不自动合并；"
                "旧混合flat只有两profile均存在时才算replacement完成。"
            ),
        },
        "wuyin_number": {
            "profiles": {
                **({"tongzong_volume3": wy} if wy else {}),
            },
            "cross_source_merge": False,
            "policy": "五音之数只属卷三。",
        },
    }
