"""现代 production 月计的太阳月界事实层。

《太乙金镜式经》卷一月计明确：
“若有闰月，只以逐月节气时刻为正也。”

因此 production 月界采用现代天文“节”交节瞬间，不以朔日或闰月额外切月。

十二月建：
- 大雪 -> 子
- 小寒 -> 丑
- 立春 -> 寅
- 惊蛰 -> 卯
- 清明 -> 辰
- 立夏 -> 巳
- 芒种 -> 午
- 小暑 -> 未
- 立秋 -> 申
- 白露 -> 酉
- 寒露 -> 戌
- 立冬 -> 亥
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import astronomy

RULE_ID = "MODERN-TAIYI-SOLAR-MONTH"

# name, apparent solar longitude, approximate Gregorian month/day, month-build branch
JIE_TERMS = (
    ("小寒", 285.0, 1, 5, "丑"),
    ("立春", 315.0, 2, 4, "寅"),
    ("惊蛰", 345.0, 3, 5, "卯"),
    ("清明", 15.0, 4, 4, "辰"),
    ("立夏", 45.0, 5, 5, "巳"),
    ("芒种", 75.0, 6, 5, "午"),
    ("小暑", 105.0, 7, 7, "未"),
    ("立秋", 135.0, 8, 7, "申"),
    ("白露", 165.0, 9, 7, "酉"),
    ("寒露", 195.0, 10, 8, "戌"),
    ("立冬", 225.0, 11, 7, "亥"),
    ("大雪", 255.0, 12, 7, "子"),
)

TERM_BY_NAME = {row[0]: row for row in JIE_TERMS}


def _aware_datetime(value: datetime) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError("moment须为datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("moment必须是timezone-aware datetime")
    return value


def _astro_to_utc(value: Any) -> datetime:
    dt = value.Utc()
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _search_start(year: int, month: int, day: int) -> astronomy.Time:
    # 所有十二节都落在给定近似日期±数日内；从前4日开始搜10日。
    start = datetime(year, month, day, tzinfo=timezone.utc)
    start = start.replace(day=day - 4 if day > 4 else 1)
    return astronomy.Time.Make(
        start.year,
        start.month,
        start.day,
        0,
        0,
        0.0,
    )


def jie_instant_utc(year: int, name: str) -> datetime:
    """求指定公历年的某个“节”交节UTC瞬间。"""
    if name not in TERM_BY_NAME:
        raise ValueError("name须为十二节之一")
    _, longitude, month, day, _ = TERM_BY_NAME[name]

    start_day = max(1, day - 4)
    start = astronomy.Time.Make(year, month, start_day, 0, 0, 0.0)
    found = astronomy.SearchSunLongitude(longitude, start, 10.0)
    if found is None:
        raise RuntimeError(f"未找到{year}年{name}交节")
    return _astro_to_utc(found)


def jie_instants_utc(year: int) -> dict[str, datetime]:
    return {name: jie_instant_utc(year, name) for name, *_ in JIE_TERMS}


def resolve_solar_month(moment: datetime) -> dict[str, Any]:
    """按最近一个“节”交节瞬间确定现代production月建。

    交节瞬间本身计入新月建。
    """
    local = _aware_datetime(moment)
    utc = local.astimezone(timezone.utc)
    year = utc.year

    candidates: list[tuple[datetime, str, str]] = []

    # 前一年大雪覆盖本年小寒前的子月。
    prev_daxue = jie_instant_utc(year - 1, "大雪")
    candidates.append((prev_daxue, "大雪", "子"))

    for name, _, _, _, branch in JIE_TERMS:
        candidates.append((jie_instant_utc(year, name), name, branch))

    # 下一年小寒提供当前大雪后的终点。
    next_xiaohan = jie_instant_utc(year + 1, "小寒")
    candidates.append((next_xiaohan, "小寒", "丑"))

    candidates.sort(key=lambda item: item[0])

    current = None
    following = None
    for item in candidates:
        if item[0] <= utc:
            current = item
        elif item[0] > utc:
            following = item
            break

    if current is None or following is None:
        raise RuntimeError("无法解析太阳月界")

    start, term_name, branch = current
    next_start, next_term_name, next_branch = following

    return {
        "rule_id": RULE_ID,
        "source_profile": "production_modern_astronomy_month_boundary",
        "input": local,
        "input_utc": utc,
        "month_boundary_kind": "节",
        "start_term": term_name,
        "month_build_branch": branch,
        "month_start_utc": start,
        "next_term": next_term_name,
        "next_month_build_branch": next_branch,
        "next_month_start_utc": next_start,
        "boundary_operator": "moment < next_jie => current; moment >= jie => new month",
        "leap_month_effect": "none",
        "policy": (
            "月计production只按十二节精确交节切月；"
            "闰月不额外增加月界，农历闰月仅作为并列日历事实。"
        ),
    }
