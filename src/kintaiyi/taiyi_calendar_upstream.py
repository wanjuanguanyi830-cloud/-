"""太乙四计的历法上游安全适配层。

本层的目标不是“猜公历日期”，而是约束外部历法解析结果如何进入
已经校定的岁/月/日/时四计核心。

现代 production 已允许通过现代天文事实层解析岁计换年与冬/夏至半岁；但月计、日计、时计积数仍需各自历法上游。
- 岁计具体日期何时切换积年，现有条文没有足够直接证据可在春节/立春/冬至间任选；
- 月计《金镜》《统宗》存在历元/积月算法版本差异；
- 日计依赖气朔积日与定朔；
- 时计必须依实际冬至/夏至气应时刻判半岁。
"""

from __future__ import annotations

from typing import Any

from .taiyi_core_chain import year_count_from_historical_year
from .taiyi_four_counts import four_count_core_from_accumulated_count
from .taiyi_time_profile import time_count_profile

RULE_ID = "CORE-CALENDAR-UPSTREAM-CONTRACT"

_REQUIREMENTS = {
    "岁计": {
        "required": ["resolved_historical_year"],
        "optional": [],
        "forbidden_guess": "不得由公历月份自行猜春节/立春/冬至岁界",
    },
    "月计": {
        "required": ["accumulated_count"],
        "optional": [],
        "forbidden_guess": "不得用公历月份编号直接代替太乙积月",
    },
    "日计": {
        "required": ["accumulated_count"],
        "optional": [],
        "forbidden_guess": "不得用Unix日数/JDN直接代替气朔积日",
    },
    "时计": {
        "required": ["entry_count", "solstice_half"],
        "optional": ["duty_time_real"],
        "forbidden_guess": "不得用6月/12月固定日期近似冬夏至气应",
    },
}


def _kind(value: str) -> str:
    aliases = {
        "岁": "岁计", "年": "岁计", "年计": "岁计", "岁计": "岁计",
        "月": "月计", "月计": "月计",
        "日": "日计", "日计": "日计",
        "时": "时计", "時": "时计", "时计": "时计", "時計": "时计",
    }
    try:
        return aliases[value]
    except (KeyError, TypeError) as exc:
        raise ValueError("count_type须为岁计/月计/日计/时计") from exc


def calendar_upstream_requirements(count_type: str) -> dict[str, Any]:
    kind = _kind(count_type)
    spec = _REQUIREMENTS[kind]
    return {
        "rule_id": RULE_ID,
        "count_type": kind,
        "required_facts": list(spec["required"]),
        "optional_facts": list(spec["optional"]),
        "automatic_gregorian_resolution": kind == "岁计",
        "forbidden_guess": spec["forbidden_guess"],
        "source_boundary": {
            "岁计": "production统一以真实天文冬至瞬间换年；现代datetime可由modern_calendar解析",
            "月计": "production已由现代十二节月界 + 连续12月积月适配器自动生成；resolved接口仍允许底层显式积数",
            "日计": "production已由《金镜》天监三年六月八日积日锚点 + 现代连续民用日自动生成；resolved接口仍允许底层显式积数",
            "时计": "需先由实际冬夏至气应判半岁并求时计积数",
        }[kind],
    }


def run_resolved_calendar_count(
    *,
    count_type: str,
    resolved_historical_year: int | None = None,
    accumulated_count: int | None = None,
    entry_count: int | None = None,
    solstice_half: str | None = None,
    duty_time_real: int | None = None,
) -> dict[str, Any]:
    """只消费已经由历法层解决的事实，再进入四计核心。"""
    kind = _kind(count_type)

    if kind == "岁计":
        if resolved_historical_year is None:
            raise ValueError("岁计须给resolved_historical_year")
        if any(
            value is not None
            for value in (
                accumulated_count,
                entry_count,
                solstice_half,
                duty_time_real,
            )
        ):
            raise ValueError("岁计统一入口只接受resolved_historical_year")
        result = year_count_from_historical_year(
            historical_year=resolved_historical_year
        )
        upstream = {"resolved_historical_year": resolved_historical_year}

    elif kind in {"月计", "日计"}:
        if accumulated_count is None:
            raise ValueError(f"{kind}须给已经校定的accumulated_count")
        if any(
            value is not None
            for value in (
                resolved_historical_year,
                entry_count,
                solstice_half,
                duty_time_real,
            )
        ):
            raise ValueError(f"{kind}统一入口只接受accumulated_count")
        result = four_count_core_from_accumulated_count(
            accumulated_count,
            count_type=kind,
        )
        upstream = {"accumulated_count": accumulated_count}

    else:
        if entry_count is None:
            raise ValueError("时计须给entry_count")
        if solstice_half is None:
            raise ValueError("时计须给solstice_half=冬至后或夏至后")
        if resolved_historical_year is not None or accumulated_count is not None:
            raise ValueError("时计统一入口不接受岁/月/日积数")
        result = time_count_profile(
            entry_count=entry_count,
            solstice_half=solstice_half,
            duty_time_real=duty_time_real,
        )
        upstream = {
            "entry_count": entry_count,
            "solstice_half": solstice_half,
            "duty_time_real": duty_time_real,
        }

    return {
        "rule_id": "CORE-RESOLVED-CALENDAR-COUNT",
        "count_type": kind,
        "calendar_resolution_status": "resolved_upstream",
        "upstream_facts": upstream,
        "result": result,
        "requirements": calendar_upstream_requirements(kind),
        "policy": (
            "本层只承接已解析传统历法事实；"
            "没有足够来源支持时宁可拒绝，也不从Gregorian datetime猜岁界、朔日或冬夏至。"
        ),
    }


def calendar_automation_status() -> dict[str, Any]:
    """列出从现代datetime完全自动化仍缺的source-specific部件。"""
    return {
        "rule_id": "CORE-CALENDAR-AUTOMATION-STATUS",
        "automatic_gregorian_resolution": False,
        "resolved": [
            "卷一长积年与卷三五子元历元",
            "岁计source-specific固定阳局",
            "四计G2-G7共同核心",
            "时计冬至后阳/夏至后阴profile",
            "C119冬夏二至时计八门直使",
        ],
        "pending": [
            "时计entry_count与C119 duty_time_real各自完整历法生成链",
        ],
        "policy": (
            "岁计换年与时计冬/夏至半岁已由现代天文层自动化；"
            "时计entry_count、duty_time_real未解决前，"
            "不声称四计datetime全自动完成。"
        ),
    }
