"""C23 《太乙统宗宝鉴》军事应用低依赖规则第一批。

独立实现 V15-02..06，不导入参考仓库 config.py，不经过旧 junshi_yingyong 综合层。
同名/近名《金镜》规则保持来源隔离。
"""

from __future__ import annotations

import copy
from typing import Any

C23_VERSION = "taiyi-c23-tongzong-v15-low-v1"
SOURCE_PROFILE = "tongzong_volume15"
SOURCE_TITLE = "太乙统宗宝鉴·军事应用篇"

ONLINE_WITNESS = {
    "provider": "识典古籍",
    "title": "太乙统宗宝鉴",
    "url": "https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppxduthvru",
    "edition_note": (
        "不同电子本卷次编排有差异；本项目沿用volume15 profile识别该军事应用篇，"
        "并以术目标题共同定位，不以卷号单独认源。"
    ),
}

# 置阵举旗。当前在线OCR正文一处有“三六直阵”的冲突读法；
# 同篇后文帛色说明“六七白、三青”，另见兵书见证明确“3直、6/7方”。
# 因此结构化采用内部自洽读法，并保留冲突元数据。
FORMATION_RULES = {
    1: {"formation": "曲阵", "element": "水", "flag": "黑旗", "direction": "北方"},
    8: {"formation": "曲阵", "element": "水", "flag": "黑旗", "direction": "北方"},
    3: {"formation": "直阵", "element": "木", "flag": "青旗", "direction": "东方"},
    4: {"formation": "锐阵", "element": "火", "flag": "赤旗", "direction": "南方"},
    9: {"formation": "锐阵", "element": "火", "flag": "赤旗", "direction": "南方"},
    2: {"formation": "圆阵", "element": "土", "flag": "黄旗", "direction": "中央"},
    5: {"formation": "圆阵", "element": "土", "flag": "黄旗", "direction": "中央"},
    6: {"formation": "方阵", "element": "金", "flag": "白旗", "direction": "西方"},
    7: {"formation": "方阵", "element": "金", "flag": "白旗", "direction": "西方"},
}

FORMATION_TEXT_VARIANT = {
    "field": "formation_digits_3_6_7",
    "online_ocr_reading": "三六直阵；六七方阵（六重复）",
    "resolved_reading": "三直阵；六七方阵",
    "evidence": [
        "同篇后文帛色总结为三青、六七白",
        "另一兵书见证明确三算木利直阵、六七金利方阵",
        "五阵五行/五色体系据此自洽",
    ],
    "reference_code_conflict": "参考仓库旧表曾写3/7直阵、6方阵",
    "resolution": "preserve_variant_note_use_coherent_source_reading",
}

MARCH_DIRECTIONS = {
    1: "西北",
    2: "正南",
    3: "东北",
    4: "正东",
    6: "正西",
    7: "西南",
    8: "正北",
    9: "东南",
}

# 出兵称神的常规条目。避免复制长咒文，只保留结构事实。
DEITY_MARCH_RULES = {
    1: {
        "order": "步卒在前、车骑次之、大将居中",
        "tempo": "肃静缓行",
        "ritual_direction": "西北",
        "cloth": "皂帛",
        "facing": "北",
    },
    2: {
        "order": "步卒在前、车骑次之、大将居中",
        "tempo": "肃静缓行",
        "ritual_direction": "正南",
        "cloth": "黄帛",
        "facing": "南",
    },
    3: {
        "order": "步卒在前、车骑次之、大将居中",
        "tempo": "肃静缓行",
        "ritual_direction": "东北",
        "cloth": "青帛",
        "facing": "东",
    },
    4: {
        "order": "步卒在前、车骑次之、大将居中",
        "tempo": "肃静缓行",
        "ritual_direction": "正东",
        "cloth": "赤帛",
        "facing": "东",
    },
    6: {
        "order": "车骑在前、步卒次之、大将居中",
        "tempo": "鼓噪急行",
        "ritual_direction": "正西",
        "cloth": "白帛",
        "facing": "西",
    },
    7: {
        "order": "车骑在前、步卒次之、大将居中",
        "tempo": "鼓噪急行",
        "ritual_direction": "西南",
        "cloth": "白帛",
        "facing": "西南",
    },
    8: {
        "order": "车骑在前、步卒次之、大将居中",
        "tempo": "鼓噪急行",
        "ritual_direction": "正北",
        "cloth": "皂帛",
        "facing": "北",
    },
    9: {
        "order": "车骑在前、步卒次之、大将居中",
        "tempo": "鼓噪急行",
        "ritual_direction": "东南",
        "cloth": "赤帛",
        "facing": "东",
    },
}

EIGHT_FORMATIONS = ["天", "地", "风", "云", "龙", "虎", "鸟", "蛇"]


def _base(rule_id: str, name: str, source_title: str) -> dict[str, Any]:
    return {
        "canonical": C23_VERSION,
        "source_profile": SOURCE_PROFILE,
        "source_title": SOURCE_TITLE,
        "source_rule_id": rule_id,
        "name": name,
        "source_section": source_title,
        "online_witness": copy.deepcopy(ONLINE_WITNESS),
        "cross_j4m_merge": False,
        "cross_c8_merge": False,
    }


def _calc_digit(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("算数须为int")
    if not 1 <= value <= 40:
        raise ValueError("算数须在1..40")
    unit = value % 10
    return 10 if unit == 0 else unit


def formation_flag_from_calc(calc: int) -> dict[str, Any]:
    """V15-02 单方五阵置旗。"""
    result = _base("V15-02", "五阵置旗", "明太乙置阵举旗术／明五阵三阵八阵之原")
    digit = _calc_digit(calc)
    rule = FORMATION_RULES.get(digit)
    if rule is None:
        return {
            **result,
            "status": "not_defined_by_source_passage",
            "computable": False,
            "calc": calc,
            "digit": digit,
            "defined_digits": sorted(FORMATION_RULES),
            "known_text_variant": copy.deepcopy(FORMATION_TEXT_VARIANT),
        }
    return {
        **result,
        "status": "ok",
        "computable": True,
        "calc": calc,
        "digit": digit,
        **copy.deepcopy(rule),
        "known_text_variant": copy.deepcopy(FORMATION_TEXT_VARIANT),
    }


def five_formations_and_flags(home_cal: int, away_cal: int) -> dict[str, Any]:
    """V15-02 主客分别读取五阵/旗色，不综合胜负。"""
    return {
        **_base("V15-02", "五阵置旗", "明太乙置阵举旗术／明五阵三阵八阵之原"),
        "status": "ok",
        "computable": True,
        "home": formation_flag_from_calc(home_cal),
        "away": formation_flag_from_calc(away_cal),
        "eight_formations": list(EIGHT_FORMATIONS),
        "policy": "只给阵型与旗色；不由本条自动推出主客胜负。",
    }


def deity_march_from_calc(calc: int, *, side: str) -> dict[str, Any]:
    """V15-03 出兵称神。

    正文常规枚举1/2/3/4/6/7/8/9；5及整十不借旧代码补造完整仪式表。
    """
    if side not in ("主", "客"):
        raise ValueError("side须为主或客")
    result = _base("V15-03", "出兵称神", "明太乙出兵称神术")
    digit = _calc_digit(calc)
    rule = DEITY_MARCH_RULES.get(digit)
    if rule is None:
        return {
            **result,
            "status": "not_regularly_enumerated_by_source",
            "computable": False,
            "side": side,
            "calc": calc,
            "digit": digit,
            "defined_digits": sorted(DEITY_MARCH_RULES),
            "source_note": (
                "正文常规条目未逐项列此数；5相关说明与杜塞/无门并见，"
                "本层不据参考代码扩写仪式细节。"
            ),
        }
    return {
        **result,
        "status": "ok",
        "computable": True,
        "side": side,
        "calc": calc,
        "digit": digit,
        **copy.deepcopy(rule),
        "policy": "保留队列、行军节奏与祭祀方色结构；不复制长咒文。",
    }


def deity_march(home_cal: int, away_cal: int) -> dict[str, Any]:
    return {
        **_base("V15-03", "出兵称神", "明太乙出兵称神术"),
        "status": "ok",
        "computable": True,
        "home": deity_march_from_calc(home_cal, side="主"),
        "away": deity_march_from_calc(away_cal, side="客"),
    }


def march_direction_from_calc(calc: int, *, side: str) -> dict[str, Any]:
    """V15-04 陈兵出乡；与J4M-06推陈兵向背严格分源。"""
    if side not in ("主", "客"):
        raise ValueError("side须为主或客")
    result = _base("V15-04", "陈兵出乡", "明陈兵必出其乡术")
    digit = _calc_digit(calc)
    direction = MARCH_DIRECTIONS.get(digit)
    if direction is None:
        return {
            **result,
            "status": "not_defined_by_source_passage",
            "computable": False,
            "side": side,
            "calc": calc,
            "digit": digit,
            "defined_digits": sorted(MARCH_DIRECTIONS),
            "j4m_equivalent": False,
        }
    return {
        **result,
        "status": "ok",
        "computable": True,
        "side": side,
        "calc": calc,
        "digit": digit,
        "direction": direction,
        "terrain_relation": {
            "顺其乡": "益吉",
            "反其乡": "以顺地形为先，不强守算向",
        },
        "j4m_equivalent": False,
        "policy": "本条只取出乡方向；不得替代J4M-06陈兵向背的阵、旗、背地规则。",
    }


def march_directions(home_cal: int, away_cal: int) -> dict[str, Any]:
    return {
        **_base("V15-04", "陈兵出乡", "明陈兵必出其乡术"),
        "status": "ok",
        "computable": True,
        "home": march_direction_from_calc(home_cal, side="主"),
        "away": march_direction_from_calc(away_cal, side="客"),
    }


def general_selection_principles() -> dict[str, Any]:
    """V15-05 选将之术；用结构化摘要保存八征，不复制长篇训释。"""
    return {
        **_base("V15-05", "选将之术", "明选将之术"),
        "status": "ok",
        "computable": True,
        "method": "八征",
        "checks": [
            {"test": "问之以言", "observe": "辞"},
            {"test": "穷之以辞", "observe": "变"},
            {"test": "与之间谋", "observe": "诚"},
            {"test": "明白显问", "observe": "德"},
            {"test": "使之以财", "observe": "廉"},
            {"test": "试之以色", "observe": "贞"},
            {"test": "告之以危难", "observe": "勇"},
            {"test": "醉之以酒", "observe": "态"},
        ],
        "principle": "外貌与内情可能不相应，应以多种情境综合察其贤否。",
        "policy": "该篇大量承用太公兵书材料；本层保存统宗收录结构，不宣称太乙独有。",
    }


def troop_training_principles() -> dict[str, Any]:
    """V15-06 教兵之术；结构化训练层级与军纪原则。"""
    return {
        **_base("V15-06", "教兵之术", "明教兵之术"),
        "status": "ok",
        "computable": True,
        "command_system": "以金鼓、旗帜和号令整齐士众",
        "progression": [
            {"from": 1, "to": 10},
            {"from": 10, "to": 100},
            {"from": 100, "to": 1000},
            {"from": 1000, "to": 10000},
            {"from": 10000, "to": "三军"},
        ],
        "discipline": [
            "分左右前后反复训练",
            "教成有赏、违教有罚",
            "训练不足、器械不利均削弱战力",
        ],
        "principle": "先教而后战；由小队逐层合成大军，保持号令一致。",
        "policy": "结构化篇章原则，不把后世兵书解释自动当作太乙计算公式。",
    }


def c23_catalog() -> dict[str, Any]:
    return {
        "canonical": C23_VERSION,
        "source_profile": SOURCE_PROFILE,
        "implemented": ["V15-02", "V15-03", "V15-04", "V15-05", "V15-06"],
        "pending_low_dependency": ["V15-09", "V15-12", "V15-13"],
        "policy": (
            "第一批只实现无外部观测或低依赖规则；风、云等外部观测规则留到下一批。"
        ),
    }
