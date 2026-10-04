"""C10 pan v2 最小消费层。

目标仓库当前没有完整 Taiyi.pan()/Streamlit/CLI 入口，因此本模块只负责建立
“消费 v2、拒绝静默混读 flat legacy”的稳定接口。后续 UI/CLI 只需调用这里。
"""

from __future__ import annotations

from typing import Any

V2_SCHEMA_VERSION = "2.0"
V2_ROOT_KEYS = (
    "meta",
    "calendar",
    "board",
    "cycles",
    "analysis",
    "modern",
    "source_variants",
    "compat",
)


def _not_computable(reason: str, *, missing: list[str] | None = None) -> dict[str, Any]:
    return {
        "schema_version": V2_SCHEMA_VERSION,
        "status": "not_computable",
        "computable": False,
        "reason": reason,
        "missing_inputs": missing or [],
        "consumer_mode": "v2_strict",
    }


def resolve_v2_payload(data: dict[str, Any]) -> dict[str, Any]:
    """接受直接 v2 或 legacy pan 中的 result["v2"]；不自动拼 flat 字段。"""
    if not isinstance(data, dict):
        raise TypeError("data须为dict")

    if data.get("schema_version") == V2_SCHEMA_VERSION:
        payload = data
        source = "direct_v2"
    elif isinstance(data.get("v2"), dict):
        payload = data["v2"]
        source = "embedded_v2"
    else:
        legacy_keys = [key for key in ("主算", "客算", "太乙", "七式", "軍事戰略", "军事战略") if key in data]
        result = _not_computable(
            "缺少 pan v2；严格消费层不会从旧中文顶层字段拼装替代。",
            missing=["v2"],
        )
        result["legacy_top_level_detected"] = bool(legacy_keys)
        result["legacy_keys_detected"] = legacy_keys
        return result

    if payload.get("schema_version") != V2_SCHEMA_VERSION:
        return _not_computable(
            "v2 schema_version不支持。",
            missing=["schema_version=2.0"],
        )

    return {
        "schema_version": V2_SCHEMA_VERSION,
        "status": "ok",
        "computable": True,
        "consumer_mode": "v2_strict",
        "source": source,
        "payload": payload,
        "missing_root_sections": [key for key in V2_ROOT_KEYS if key not in payload],
    }


def read_v2_section(data: dict[str, Any], section: str) -> dict[str, Any]:
    """读取一个 v2 根区段；不存在时显式不可算，不回退 flat。"""
    if section not in V2_ROOT_KEYS:
        raise ValueError(f"未知v2区段: {section}")
    resolved = resolve_v2_payload(data)
    if not resolved.get("computable"):
        return resolved
    payload = resolved["payload"]
    if section not in payload:
        return _not_computable(
            f"v2缺少{section}区段。",
            missing=[section],
        )
    return {
        "schema_version": V2_SCHEMA_VERSION,
        "status": "ok",
        "computable": True,
        "consumer_mode": "v2_strict",
        "section": section,
        "data": payload[section],
    }


def read_v2_analysis(data: dict[str, Any], name: str) -> dict[str, Any]:
    """读取 analysis 下的明确子层，如 eight_divinations/seven_methods/military。"""
    section = read_v2_section(data, "analysis")
    if not section.get("computable"):
        return section
    analysis = section["data"]
    if not isinstance(analysis, dict) or name not in analysis:
        return _not_computable(
            f"v2.analysis缺少{name}。",
            missing=[f"analysis.{name}"],
        )
    return {
        "schema_version": V2_SCHEMA_VERSION,
        "status": "ok",
        "computable": True,
        "consumer_mode": "v2_strict",
        "section": f"analysis.{name}",
        "data": analysis[name],
    }


def read_v2_board(data: dict[str, Any], name: str) -> dict[str, Any]:
    """读取 board 下的明确子层，如 taiyi/eyes/calculations/generals/doors。"""
    section = read_v2_section(data, "board")
    if not section.get("computable"):
        return section
    board = section["data"]
    if not isinstance(board, dict) or name not in board:
        return _not_computable(
            f"v2.board缺少{name}。",
            missing=[f"board.{name}"],
        )
    return {
        "schema_version": V2_SCHEMA_VERSION,
        "status": "ok",
        "computable": True,
        "consumer_mode": "v2_strict",
        "section": f"board.{name}",
        "data": board[name],
    }


def build_v2_view_model(data: dict[str, Any]) -> dict[str, Any]:
    """给未来 CLI/UI 的最小视图模型；只透传 v2 已有层，不制造旧字段。"""
    resolved = resolve_v2_payload(data)
    if not resolved.get("computable"):
        return resolved

    payload = resolved["payload"]
    return {
        "schema_version": V2_SCHEMA_VERSION,
        "consumer_mode": "v2_strict",
        "source": resolved["source"],
        "meta": payload.get("meta"),
        "calendar": payload.get("calendar"),
        "board": payload.get("board"),
        "cycles": payload.get("cycles"),
        "analysis": payload.get("analysis"),
        "modern": payload.get("modern"),
        "source_variants": payload.get("source_variants"),
        "compat": payload.get("compat"),
        "missing_root_sections": resolved["missing_root_sections"],
        "legacy_fallback_used": False,
    }
