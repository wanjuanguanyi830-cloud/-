"""现代 production calendar -> pan v2 适配器。

只做事实搬运与JSON-safe序列化，不复制任何太乙算法。
调用方必须显式选择岁计/月计/日计/时计；四盘不会混成一盘。
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .pan_v2 import build_pan_v2, validate_pan_v2
from .taiyi_modern_calendar import production_calendar_context

RULE_ID = "MODERN-PAN-V2-ADAPTER"

_COUNT_KEY = {
    "岁计": "year_count",
    "月计": "month_count",
    "日计": "day_count",
    "时计": "time_count",
}

_ALIASES = {
    "岁": "岁计", "年": "岁计", "年计": "岁计", "岁计": "岁计",
    "月": "月计", "月计": "月计",
    "日": "日计", "日计": "日计",
    "时": "时计", "時": "时计", "时计": "时计", "時計": "时计",
}


def _kind(value: str) -> str:
    try:
        return _ALIASES[value]
    except (KeyError, TypeError) as exc:
        raise ValueError("count_type须为岁计/月计/日计/时计") from exc


def _json_calendar(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): _json_calendar(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_calendar(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"modern calendar含不可序列化类型: {type(value).__name__}")


def _selected_core(selected: dict[str, Any], kind: str) -> dict[str, Any]:
    result = selected["result"]
    if kind == "时计":
        return result["core"]
    return result


def _general_fact(stage: dict[str, Any]) -> dict[str, Any]:
    return {
        "palace": stage.get("big_general_palace"),
        "assistant_palace": stage.get("assistant_general_palace"),
        "blocked": stage.get("blocked"),
    }


def build_modern_pan_v2(
    moment: datetime,
    *,
    count_type: str,
    scenario: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """一个现代datetime + 显式四计类型 -> pan v2。"""
    kind = _kind(count_type)
    context = production_calendar_context(moment)
    selected = context[_COUNT_KEY[kind]]
    core = _selected_core(selected, kind)

    g7 = core["stages"]["g7"]

    board = {
        "taiyi": {
            "palace": core["taiyi_palace"],
        },
        "eyes": {
            "skyeyes": {"sector": core["wenchang_sector"]},
            "shiji": {"sector": core["shiji_sector"]},
            "jishen": {"sector": core["jishen_sector"]},
        },
        "calculations": {
            "host": {"value": core["host_calc"]},
            "guest": {"value": core["guest_calc"]},
        },
        "generals": {
            "host": _general_fact(g7["host"]),
            "guest": _general_fact(g7["guest"]),
        },
        "doors": {},
    }

    if kind == "时计":
        board["doors"]["direct"] = {
            "door": selected.get("direct_door"),
            "source": "C119",
        }

    calendar = {
        "production_profile": "modern_astronomy_lunisolar",
        "input_moment": moment.isoformat(),
        "count_type": kind,
        "taiyi_year": context["year_boundary"]["taiyi_historical_year"],
        "year_boundary_policy": {
            "unique_boundary": "真实天文冬至交节瞬间",
            "label_rule": "公历Y年冬至瞬间起进入太乙Y+1岁",
            "comparison": context["year_boundary"]["boundary_operator"],
            "ignored_boundaries": context["year_boundary"]["ignored_year_boundaries"],
            "taiyi_year_start_utc": context["year_boundary"]["taiyi_year_start_utc"],
            "next_taiyi_year_start_utc": context["year_boundary"]["next_taiyi_year_start_utc"],
        },
        "lunar": _json_calendar(context["lunisolar"]["lunar"]),
        "ganzhi": _json_calendar(context["lunisolar"]["ganzhi"]),
        "solar_month": _json_calendar(context["solar_month"]),
        "selected_count": _json_calendar(selected),
        "year_boundary": _json_calendar(context["year_boundary"]),
        "time_half": _json_calendar(context["time_half"]),
    }

    payload = build_pan_v2(
        meta={
            "producer": RULE_ID,
            "count_type": kind,
            "calendar_mode": "production_modern",
        },
        calendar=calendar,
        board=board,
        modern={
            "calendar_context": {
                "astronomy_provider": context["astronomy_provider"],
                "lunisolar_provider": context["lunisolar_provider"],
            }
        },
        scenario=scenario,
        compat={
            "legacy_top_level": False,
            "legacy_schema": None,
            "modern_production": True,
        },
    )

    validation = validate_pan_v2(payload)
    if not validation["valid"]:
        raise ValueError(f"生成pan v2未通过验证: {validation['errors']}")
    return payload
