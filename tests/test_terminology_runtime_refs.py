import importlib
import json
from pathlib import Path


INDEX = Path("terminology/catalog-index.json")
RUNTIME_KEYS = {"runtime", "collation_runtime", "origin_table_runtime"}


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _runtime_refs(node):
    refs = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key in RUNTIME_KEYS and isinstance(value, str):
                refs.append(value)
            elif key == "runtimes" and isinstance(value, list):
                refs.extend(item for item in value if isinstance(item, str))
            refs.extend(_runtime_refs(value))
    elif isinstance(node, list):
        for value in node:
            refs.extend(_runtime_refs(value))
    return refs


def _resolve(ref):
    # A runtime reference may point to a module, function, or module constant.
    try:
        return importlib.import_module(ref)
    except ModuleNotFoundError:
        pass

    parts = ref.split(".")
    last_error = None
    for split in range(len(parts) - 1, 0, -1):
        module_name = ".".join(parts[:split])
        try:
            obj = importlib.import_module(module_name)
        except ModuleNotFoundError as exc:
            last_error = exc
            continue

        for attr in parts[split:]:
            obj = getattr(obj, attr)
        return obj

    if last_error is not None:
        raise last_error
    raise ImportError(ref)


def test_all_stable_catalog_runtime_references_resolve():
    index = _load(INDEX)
    refs = []

    for item in index["stable_catalogs"]:
        data = _load(item["path"])
        refs.extend((item["path"], ref) for ref in _runtime_refs(data))

    assert refs
    unresolved = []
    for path, ref in sorted(set(refs)):
        try:
            _resolve(ref)
        except (ImportError, AttributeError, ModuleNotFoundError) as exc:
            unresolved.append((path, ref, type(exc).__name__, str(exc)))

    assert unresolved == []


def test_runtime_fields_are_code_references_not_normalized_text_values():
    index = _load(INDEX)

    bad = []
    for item in index["stable_catalogs"]:
        data = _load(item["path"])
        for ref in _runtime_refs(data):
            if "." not in ref or any(ch.isspace() for ch in ref):
                bad.append((item["path"], ref))

    assert bad == []
