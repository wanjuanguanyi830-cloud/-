import json
from pathlib import Path


RULES = Path("rules/taiyi_v1.json")
INDEX = Path("terminology/catalog-index.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _collect_rule_ids(node, out=None):
    if out is None:
        out = set()

    if isinstance(node, list):
        for item in node:
            _collect_rule_ids(item, out)
        return out

    if not isinstance(node, dict):
        return out

    for key, value in node.items():
        if key == "rule_id" and isinstance(value, str):
            out.add(value)
        elif key == "rule_ids" and isinstance(value, list):
            out.update(item for item in value if isinstance(item, str))
        _collect_rule_ids(value, out)

    return out


def test_all_rules_json_rule_ids_are_covered_by_stable_terminology():
    rules = _load(RULES)
    index = _load(INDEX)

    rule_ids = _collect_rule_ids(rules)
    terminology_ids = set()

    for item in index["stable_catalogs"]:
        terminology_ids.update(_collect_rule_ids(_load(item["path"])))

    missing = sorted(rule_ids - terminology_ids)

    assert rule_ids
    assert missing == []


def test_terminology_may_be_more_granular_than_rules_summary():
    rules = _load(RULES)
    index = _load(INDEX)

    rule_ids = _collect_rule_ids(rules)
    terminology_ids = set()

    for item in index["stable_catalogs"]:
        terminology_ids.update(_collect_rule_ids(_load(item["path"])))

    # Stable terminology intentionally records sub-rules such as D8-01..08,
    # T7 methods, C69B overlay steps, and source-profile-specific cycle IDs
    # that are summarized more coarsely in rules/taiyi_v1.json.
    assert terminology_ids.issuperset(rule_ids)
