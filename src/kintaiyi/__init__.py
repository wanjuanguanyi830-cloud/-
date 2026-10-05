"""太乙术语、规则、历史source profiles与modern production入口。

核心项目约束：
- 古籍规则按来源分层，不因同名静默合并；
- modern production 使用现代天文/现代历法事实；
- 太乙岁唯一换年点是真实天文冬至交节瞬间；
- 元旦、春节、立春、春分均不改变太乙岁。
"""

RULESET_VERSION = "taiyi-t7-d8-v1"

PRODUCTION_CALENDAR_MODE = "modern_astronomy_lunisolar"
TAIYI_YEAR_BOUNDARY = "astronomical_winter_solstice"
TAIYI_YEAR_LABEL_RULE = "Gregorian Y winter solstice instant => Taiyi Y+1"
NON_TAIYI_YEAR_BOUNDARIES = ("元旦", "春节", "立春", "春分")

PUBLIC_MODERN_ENTRYPOINTS = {
    "calendar_context": "kintaiyi.taiyi_modern_calendar.production_calendar_context",
    "pan_v2": "kintaiyi.taiyi_modern_pan.build_modern_pan_v2",
}

PUBLIC_API_ENTRYPOINTS = {
    "registry": "kintaiyi.api.registry_snapshot",
    "registry_versions": "kintaiyi.api.registry_versions",
    "repository_status": "kintaiyi.api.repository_status",
    "get_term": "kintaiyi.api.get_term",
    "search_terms": "kintaiyi.api.search_terms",
    "get_rule": "kintaiyi.api.get_rule",
    "calculate": "kintaiyi.api.calculate",
    "calculate_rule": "kintaiyi.api.calculate_rule",
    "rule_runtime_candidates": "kintaiyi.api.rule_runtime_candidates",
    "operations_for_rule": "kintaiyi.api.operations_for_rule",
    "describe_rule": "kintaiyi.api.describe_rule",
    "capabilities": "kintaiyi.api.capabilities",
    "calendar_context": "kintaiyi.api.calendar_context",
    "build_pan": "kintaiyi.api.build_pan",
    "explain_result": "kintaiyi.api.explain_result",
}

from .api import (
    build_pan,
    calculate,
    calculate_rule,
    capabilities,
    calendar_context,
    describe_rule,
    explain_result,
    get_rule,
    get_term,
    list_catalogs,
    list_operations,
    operations_for_rule,
    registry_snapshot,
    registry_versions,
    repository_status,
    rule_runtime_candidates,
    search_terms,
)

__all__ = [
    "RULESET_VERSION",
    "PRODUCTION_CALENDAR_MODE",
    "TAIYI_YEAR_BOUNDARY",
    "TAIYI_YEAR_LABEL_RULE",
    "NON_TAIYI_YEAR_BOUNDARIES",
    "PUBLIC_MODERN_ENTRYPOINTS",
    "PUBLIC_API_ENTRYPOINTS",
    "registry_snapshot",
    "registry_versions",
    "repository_status",
    "list_catalogs",
    "list_operations",
    "get_term",
    "search_terms",
    "get_rule",
    "calculate",
    "calculate_rule",
    "rule_runtime_candidates",
    "operations_for_rule",
    "describe_rule",
    "capabilities",
    "calendar_context",
    "build_pan",
    "explain_result",
]
