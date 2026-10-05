"""C69 《太乙金镜式经》卷一“推太乙当时法”核心表层。

本层只实现直接正文中无需补造天文/六壬排式的稳定核心：
- 十日干的天乙朝/暮治神表；
- 魁、罡二辰禁居边界；
- 天乙贵神及前五、后六天将的主事/吉凶表。

完整“二至以后日度所在，加时位（加于时支）”由 C118 与 C69B 在显式输入下接通；
本模块仍只保存 C69 直接表，不把分层实现伪装成完整自动日期单入口。
"""

from __future__ import annotations

import copy
from typing import Any

C69_VERSION = "taiyi-c69-jinjing-current-time-core-v1"

RULER_BRANCHES = {
    "神后": "子",
    "大吉": "丑",
    "功曹": "寅",
    "太冲": "卯",
    "太乙": "巳",
    "胜光": "午",
    "小吉": "未",
    "传送": "申",
    "从魁": "酉",
    "登明": "亥",
}

EXCLUDED_BRANCHES = {
    "辰": {
        "source_name": "罡",
        "designation": "天庭",
        "policy": "非贵所居",
    },
    "戌": {
        "source_name": "魁",
        "source_form": "戍",
        "designation": "天狱",
        "policy": "非贵所居",
    },
}

DAY_PERIOD_RULERS = {
    "甲": {"朝": "小吉", "暮": "大吉"},
    "戊": {"朝": "大吉", "暮": "小吉"},
    "庚": {"朝": "大吉", "暮": "小吉"},
    "己": {"朝": "神后", "暮": "传送"},
    "乙": {"朝": "传送", "暮": "神后"},
    "丁": {"朝": "登明", "暮": "从魁"},
    "丙": {"朝": "从魁", "暮": "登明"},
    "癸": {"朝": "太乙", "暮": "太冲"},
    "壬": {"朝": "太冲", "暮": "太乙"},
    "辛": {"朝": "功曹", "暮": "胜光"},
}

GENERAL_RULES = {
    "天乙贵神": {
        "relative": 0,
        "element": "土",
        "matters": ["贵人", "接引", "升进"],
        "verdict": "conditional",
        "qi_verdicts": {"王相": "吉", "囚死": "凶"},
        "source_status": "direct",
    },
    "螣蛇": {
        "relative": "前一",
        "element": "火",
        "matters": ["惊恐", "战斗"],
        "verdict": "凶",
        "source_status": "direct",
    },
    "朱雀": {
        "relative": "前二",
        "element": "火",
        "matters": ["文书", "口舌", "衣物"],
        "verdict": "凶",
        "source_status": "direct",
    },
    "六合": {
        "relative": "前三",
        "element": "木",
        "matters": ["和合", "婚姻"],
        "verdict": "吉",
        "source_status": "direct",
    },
    "勾陈": {
        "relative": "前四",
        "element": "土",
        "matters": ["勾留", "战斗"],
        "verdict": "凶",
        "source_status": "direct",
    },
    "青龙": {
        "relative": "前五",
        "element": "木",
        "matters": ["迁官", "钱财", "婚姻"],
        "verdict": "吉",
        "source_status": "direct",
    },
    "天后": {
        "relative": "后一",
        "element": "水",
        "matters": ["蔽匿", "妇人", "淫乱事"],
        "verdict": None,
        "source_status": "direct_no_explicit_verdict",
    },
    "太阴": {
        "relative": "后二",
        "element": "金",
        "matters": ["阴人掌事"],
        "verdict": "吉",
        "source_status": "direct",
    },
    "玄武": {
        "relative": "后三",
        "element": "水",
        "matters": ["盗贼", "亡失", "财物"],
        "verdict": "凶",
        "source_status": "direct",
    },
    "太常": {
        "relative": "后四",
        "element": "土",
        "matters": ["财物", "金玉", "酒食"],
        "verdict": "吉",
        "source_status": "direct",
    },
    "白虎": {
        "relative": "后五",
        "element": "金",
        "matters": ["死亡", "哭泣", "兵刃", "道路"],
        "verdict": "凶",
        "source_status": "direct",
    },
    "天空": {
        "relative": "后六",
        "element": "土",
        "matters": ["万物欺殆", "奴婢欺诈"],
        "verdict": "凶",
        "source_status": "direct",
    },
}

SOURCE_WITNESS = {
    "work": "太乙金镜式经",
    "volume": 1,
    "section": "推太乙当时法",
    "direct_core": [
        "二至以后日度所在加时位，加于时支",
        "立五将式之天乙朝暮治神",
        "不理魁罡二辰",
        "主客诸将在吉神下吉，在凶神下凶",
    ],
    "collation": [
        {
            "source": "四库本公开转录",
            "status": "matches_core_table",
        },
        {
            "source": "识典古籍转录",
            "status": "matches_core_table",
        },
    ],
}

FULL_FORMULA_BOUNDARY = {
    "status": "partial_runtime_upstream_required",
    "implemented_in_c69": [
        "day_stem_morning_evening_tianyi_ruler",
        "excluded_chen_xu_boundary",
        "twelve_general_direct_omens",
    ],
    "implemented_by_c69b": [
        "显式输入下以C118日宿分野支加占时，建立天地盘",
        "按显式日干与朝/暮定位天乙贵人，落地定顺逆并布十二天将",
        "按实体地支或九宫adapter查询所临天将",
    ],
    "pending_upstream": [
        "公历日期到节气第几日仍由上游历法提供",
        "朝/暮仍须调用方显式给定",
    ],
    "upstream_computability_limits": [
        "C118虚宿整数未定；穿越未定虚宿边界的输入返回not_computable",
    ],
    "coordinate_adapter_boundary": {
        "adapter": "九宫到六壬十二支",
        "lossy": True,
        "strict_alternative": "直接给entity_branches",
    },
    "complete_current_time_formula": False,
    "complete_false_means": "完整自动单入口尚未统一；不表示C69B显式输入六壬叠盘核心未实现。",
    "policy": "C118+C69B已实现可算输入下的日度加时与六壬安将；complete_current_time_formula=False只表示日期到节气日序、朝暮判定和坐标入口尚未统一。",
}


def tianyi_period_ruler(day_stem: str, period: str) -> dict[str, Any]:
    """返回《金镜》直接表中的某日干朝/暮天乙治神。"""
    if day_stem not in DAY_PERIOD_RULERS:
        raise ValueError("day_stem须为十天干")
    if period not in ("朝", "暮"):
        raise ValueError("period须为朝/暮")

    ruler = DAY_PERIOD_RULERS[day_stem][period]
    branch = RULER_BRANCHES[ruler]
    return {
        "schema_version": "1.0",
        "canonical": C69_VERSION,
        "rule_id": "C69-TIANYI-PERIOD-RULER",
        "source_profile": "jinjing_volume1_current_time",
        "day_stem": day_stem,
        "period": period,
        "ruler": ruler,
        "branch": branch,
        "excluded_branch": branch in EXCLUDED_BRANCHES,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "full_formula_boundary": copy.deepcopy(FULL_FORMULA_BOUNDARY),
    }


def general_omen(
    general: str,
    *,
    tianyi_qi_state: str | None = None,
) -> dict[str, Any]:
    """解释正文直接给出的天乙/十一神主事与吉凶。"""
    try:
        rule = GENERAL_RULES[general]
    except KeyError as exc:
        raise ValueError("未知C69天将") from exc

    verdict = rule["verdict"]
    pending: list[str] = []

    if general == "天乙贵神":
        if tianyi_qi_state is None:
            verdict = None
            pending.append("天乙贵神须显式给王相/囚死状态后才能定吉凶")
        elif tianyi_qi_state not in ("王相", "囚死"):
            raise ValueError("tianyi_qi_state须为王相/囚死或None")
        else:
            verdict = rule["qi_verdicts"][tianyi_qi_state]
    elif tianyi_qi_state is not None:
        raise ValueError("tianyi_qi_state只用于天乙贵神")

    return {
        "schema_version": "1.0",
        "canonical": C69_VERSION,
        "rule_id": "C69-TWELVE-GENERAL-OMEN",
        "source_profile": "jinjing_volume1_current_time",
        "general": general,
        "relative": rule["relative"],
        "element": rule["element"],
        "matters": copy.deepcopy(rule["matters"]),
        "tianyi_qi_state": tianyi_qi_state,
        "verdict": verdict,
        "source_status": rule["source_status"],
        "pending": pending,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "full_formula_boundary": copy.deepcopy(FULL_FORMULA_BOUNDARY),
    }


def current_time_core(
    *,
    day_stem: str,
    period: str,
    general: str | None = None,
    tianyi_qi_state: str | None = None,
) -> dict[str, Any]:
    """组合已实现核心；不声称完成日度加时的完整排式。"""
    ruler = tianyi_period_ruler(day_stem, period)
    omen = (
        general_omen(general, tianyi_qi_state=tianyi_qi_state)
        if general is not None
        else None
    )
    return {
        "schema_version": "1.0",
        "canonical": C69_VERSION,
        "rule_id": "C69-CURRENT-TIME-CORE",
        "source_profile": "jinjing_volume1_current_time",
        "tianyi_ruler": ruler,
        "general_omen": omen,
        "complete_current_time_formula": False,
        "full_formula_boundary": copy.deepcopy(FULL_FORMULA_BOUNDARY),
        "policy": (
            "C118+C69B已接通可算输入下的日度与六壬叠盘；此标志只表示完整自动日期单入口尚未统一。"
        ),
    }


def c69_catalog() -> dict[str, Any]:
    return {
        "canonical": C69_VERSION,
        "source_profile": "jinjing_volume1_current_time",
        "day_period_rulers": copy.deepcopy(DAY_PERIOD_RULERS),
        "ruler_branches": copy.deepcopy(RULER_BRANCHES),
        "excluded_branches": copy.deepcopy(EXCLUDED_BRANCHES),
        "general_rules": copy.deepcopy(GENERAL_RULES),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "full_formula_boundary": copy.deepcopy(FULL_FORMULA_BOUNDARY),
    }
