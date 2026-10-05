"""Stable software-facing API for the Taiyi repository.

This module is intentionally thin. It does not duplicate formulas or source
evidence; it resolves the repository's terminology/rule registries and delegates
calculation to the existing source-specific runtimes.
"""

from __future__ import annotations

import importlib
import json
from importlib import resources
from typing import Any, Callable


def _load_json(package: str, filename: str) -> Any:
    resource = resources.files(package).joinpath(filename)
    return json.loads(resource.read_text(encoding="utf-8"))


def resolve_runtime(reference: str) -> Callable[..., Any]:
    """Resolve package.module.object without hard-coding module imports."""
    if not isinstance(reference, str) or "." not in reference:
        raise ValueError("runtime reference must be a dotted Python path")
    parts = reference.split(".")
    last_error: Exception | None = None
    for split in range(len(parts) - 1, 0, -1):
        module_name = ".".join(parts[:split])
        try:
            obj: Any = importlib.import_module(module_name)
        except ModuleNotFoundError as exc:
            last_error = exc
            continue
        for attr in parts[split:]:
            obj = getattr(obj, attr)
        if not callable(obj):
            raise TypeError(f"runtime is not callable: {reference}")
        return obj
    if last_error is not None:
        raise last_error
    raise ImportError(reference)


def registry_snapshot() -> dict[str, Any]:
    return _load_json("registry", "catalog.json")


def list_catalogs() -> list[dict[str, Any]]:
    index = _load_json("terminology", "catalog-index.json")
    return list(index["stable_catalogs"])


def _catalog_filename(path: str) -> str:
    prefix = "terminology/"
    if not path.startswith(prefix):
        raise ValueError(f"unexpected terminology catalog path: {path}")
    return path[len(prefix):]


def get_term(name_or_key: str, *, catalog: str | None = None) -> dict[str, Any]:
    if not isinstance(name_or_key, str) or not name_or_key:
        raise ValueError("name_or_key must be a non-empty string")
    matches: list[dict[str, Any]] = []
    for meta in list_catalogs():
        if catalog is not None and catalog not in (
            meta["catalog_id"], meta["path"], _catalog_filename(meta["path"])
        ):
            continue
        data = _load_json("terminology", _catalog_filename(meta["path"]))
        for entry in data.get("entries", []):
            names = {entry.get("key"), entry.get("preferred_term")}
            names.update(entry.get("aliases") or [])
            if name_or_key in names:
                matches.append({
                    "catalog_id": meta["catalog_id"],
                    "catalog_path": meta["path"],
                    "scope": meta["scope"],
                    "entry": entry,
                })
    return {"query": name_or_key, "count": len(matches), "matches": matches}


def search_terms(text: str) -> dict[str, Any]:
    if not isinstance(text, str) or not text:
        raise ValueError("text must be a non-empty string")
    needle = text.casefold()
    matches: list[dict[str, Any]] = []
    for meta in list_catalogs():
        data = _load_json("terminology", _catalog_filename(meta["path"]))
        for entry in data.get("entries", []):
            names = [entry.get("key"), entry.get("preferred_term")]
            names.extend(entry.get("aliases") or [])
            if any(isinstance(value, str) and needle in value.casefold() for value in names):
                matches.append({
                    "catalog_id": meta["catalog_id"],
                    "catalog_path": meta["path"],
                    "entry": entry,
                })
    return {"query": text, "count": len(matches), "matches": matches}


def get_rule(rule_id: str) -> dict[str, Any]:
    if not isinstance(rule_id, str) or not rule_id:
        raise ValueError("rule_id must be a non-empty string")
    data = _load_json("rules", "taiyi_v1.json")
    matches: list[dict[str, Any]] = []
    for category_name, records in data.get("categories", {}).items():
        for record in records:
            ids: set[str] = set()
            if isinstance(record.get("id"), str):
                ids.add(record["id"])
            if isinstance(record.get("rule_id"), str):
                ids.add(record["rule_id"])
            ids.update(x for x in record.get("rule_ids", []) if isinstance(x, str))
            if rule_id in ids:
                matches.append({"category": category_name, "record": record})
    return {"rule_id": rule_id, "count": len(matches), "matches": matches}


def list_operations() -> list[dict[str, Any]]:
    return list(_load_json("registry", "operations.json")["operations"])


def _operation(name: str) -> dict[str, Any]:
    for item in list_operations():
        if item["name"] == name:
            return item
    raise KeyError(f"unknown public operation: {name}")


def calculate(operation: str, *args: Any, **kwargs: Any) -> Any:
    spec = _operation(operation)
    if spec.get("status") != "stable":
        raise RuntimeError(f"operation is not stable: {operation}")
    runtime = spec.get("runtime")
    if not runtime:
        raise RuntimeError(f"operation has no runtime: {operation}")
    return resolve_runtime(runtime)(*args, **kwargs)


def calendar_context(moment: Any) -> dict[str, Any]:
    return calculate("modern.calendar_context", moment)


def build_pan(
    moment: Any,
    *,
    count_type: str,
    scenario: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return calculate(
        "modern.pan_v2",
        moment,
        count_type=count_type,
        scenario=scenario,
    )


def explain_result(result: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(result, dict):
        raise TypeError("result must be a dict")
    rule_id = result.get("rule_id")
    rule = get_rule(rule_id) if isinstance(rule_id, str) else {
        "rule_id": None, "count": 0, "matches": []
    }
    return {
        "rule_id": rule_id,
        "source_profile": result.get("source_profile"),
        "canonical": result.get("canonical"),
        "rule_registry": rule,
        "policy": "explanation facade only; does not recompute or merge source profiles",
    }
