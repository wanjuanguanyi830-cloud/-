"""Stable software-facing API for the Taiyi repository.

This module is intentionally thin. It does not duplicate formulas or source
evidence; it resolves the repository's terminology/rule registries and delegates
calculation to the existing source-specific runtimes.
"""

from __future__ import annotations

import importlib
import inspect
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


def registry_versions() -> dict[str, str]:
    """Return version identifiers that software can use for compatibility checks."""
    catalog = registry_snapshot()
    operations = _load_json("registry", "operations.json")
    return {
        "public_api_version": catalog["public_api"]["version"],
        "registry_schema_version": catalog["schema_version"],
        "operations_schema_version": operations["schema_version"],
        "operations_api_version": operations["api_version"],
        "operations_registry_id": operations["registry_id"],
    }


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


def _contains_rule_id(node: Any, rule_id: str) -> bool:
    if isinstance(node, dict):
        if node.get("rule_id") == rule_id:
            return True
        ids = node.get("rule_ids", [])
        if isinstance(ids, list) and rule_id in [x for x in ids if isinstance(x, str)]:
            return True
        return any(_contains_rule_id(value, rule_id) for value in node.values())
    if isinstance(node, list):
        return any(_contains_rule_id(value, rule_id) for value in node)
    return False


def get_rule(rule_id: str) -> dict[str, Any]:
    if not isinstance(rule_id, str) or not rule_id:
        raise ValueError("rule_id must be a non-empty string")
    data = _load_json("rules", "taiyi_v1.json")
    matches: list[dict[str, Any]] = []
    for category_name, records in data.get("categories", {}).items():
        for record in records:
            if record.get("id") == rule_id or _contains_rule_id(record, rule_id):
                matches.append({"category": category_name, "record": record})
    return {"rule_id": rule_id, "count": len(matches), "matches": matches}


def _collect_runtime_candidates(
    node: Any,
    rule_id: str,
    *,
    origin: str,
    path: str = "$",
    key_hint: str | None = None,
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    if isinstance(node, dict):
        runtime = node.get("runtime")
        if node.get("rule_id") == rule_id and isinstance(runtime, str):
            candidate: dict[str, Any] = {
                "runtime": runtime,
                "origin": origin,
                "path": path,
            }
            if isinstance(node.get("source_profile"), str):
                candidate["source_profile"] = node["source_profile"]
                if key_hint:
                    candidate["profile_key"] = key_hint
            candidates.append(candidate)
        for key, value in node.items():
            candidates.extend(
                _collect_runtime_candidates(
                    value,
                    rule_id,
                    origin=origin,
                    path=f"{path}.{key}",
                    key_hint=key,
                )
            )
    elif isinstance(node, list):
        for index, value in enumerate(node):
            candidates.extend(
                _collect_runtime_candidates(
                    value,
                    rule_id,
                    origin=origin,
                    path=f"{path}[{index}]",
                    key_hint=None,
                )
            )
    return candidates


def rule_runtime_candidates(rule_id: str) -> list[dict[str, Any]]:
    """Discover exact runtime pointers owned by rules/ or terminology/."""
    if not isinstance(rule_id, str) or not rule_id:
        raise ValueError("rule_id must be a non-empty string")

    found = _collect_runtime_candidates(
        _load_json("rules", "taiyi_v1.json"),
        rule_id,
        origin="rules/taiyi_v1.json",
    )
    for meta in list_catalogs():
        filename = _catalog_filename(meta["path"])
        found.extend(
            _collect_runtime_candidates(
                _load_json("terminology", filename),
                rule_id,
                origin=meta["path"],
            )
        )

    grouped: dict[str, dict[str, Any]] = {}
    for item in found:
        runtime = item["runtime"]
        bucket = grouped.setdefault(
            runtime,
            {"runtime": runtime, "origins": [], "profile_keys": [], "source_profiles": []},
        )
        bucket["origins"].append({"origin": item["origin"], "path": item["path"]})
        if item.get("profile_key") and item["profile_key"] not in bucket["profile_keys"]:
            bucket["profile_keys"].append(item["profile_key"])
        if item.get("source_profile") and item["source_profile"] not in bucket["source_profiles"]:
            bucket["source_profiles"].append(item["source_profile"])
    return list(grouped.values())


def calculate_rule(rule_id: str, *args: Any, **kwargs: Any) -> Any:
    """Calculate by canonical rule_id when it resolves to one runtime.

    Source-specific functions keep their explicit source boundary. If the
    callable requires source_profile and the registry exposes one unique profile
    key for the requested rule_id, the facade supplies that key.
    """
    candidates = rule_runtime_candidates(rule_id)
    if not candidates:
        raise KeyError(f"no runtime registered for rule_id: {rule_id}")
    if len(candidates) != 1:
        refs = ", ".join(item["runtime"] for item in candidates)
        raise RuntimeError(f"ambiguous runtimes for {rule_id}: {refs}")

    candidate = candidates[0]
    runtime = resolve_runtime(candidate["runtime"])
    if "source_profile" not in kwargs:
        signature = inspect.signature(runtime)
        if "source_profile" in signature.parameters:
            profile_keys = candidate.get("profile_keys") or []
            if len(profile_keys) == 1:
                kwargs["source_profile"] = profile_keys[0]
    result = runtime(*args, **kwargs)
    if isinstance(result, dict):
        source_rule_id = result.get("source_rule_id")
        if "rule_id" not in result and source_rule_id == rule_id:
            result = dict(result)
            result["rule_id"] = rule_id
            result["registry_normalized_rule_id"] = True
    return result


def list_operations() -> list[dict[str, Any]]:
    return list(_load_json("registry", "operations.json")["operations"])


def _operation(name: str) -> dict[str, Any]:
    for item in list_operations():
        if item["name"] == name:
            return item
    raise KeyError(f"unknown public operation: {name}")


def operations_for_rule(rule_id: str) -> list[dict[str, Any]]:
    """Return curated public-operation aliases that include a rule_id."""
    if not isinstance(rule_id, str) or not rule_id:
        raise ValueError("rule_id must be a non-empty string")
    return [
        item for item in list_operations()
        if rule_id in item.get("rule_ids", [])
    ]


def capabilities() -> dict[str, Any]:
    """Return frontend-friendly operation groups without duplicating algorithms."""
    operations = list_operations()
    domains: dict[str, list[dict[str, Any]]] = {}
    for item in operations:
        domains.setdefault(item["domain"], []).append({
            "name": item["name"],
            "rule_ids": list(item.get("rule_ids", [])),
            "status": item.get("status"),
            "source_profile_required": bool(item.get("source_profile_required", False)),
        })
    operation_registry = _load_json("registry", "operations.json")
    return {
        "registry_id": operation_registry["registry_id"],
        "api_version": operation_registry["api_version"],
        "operation_count": len(operations),
        "domains": domains,
    }


def describe_rule(rule_id: str) -> dict[str, Any]:
    """Combine rule metadata, exact runtime candidates and public aliases."""
    return {
        "rule_id": rule_id,
        "rule": get_rule(rule_id),
        "runtime_candidates": rule_runtime_candidates(rule_id),
        "operations": operations_for_rule(rule_id),
    }


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
    rule_id = result.get("rule_id") or result.get("source_rule_id")
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
