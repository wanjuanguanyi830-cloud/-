"""J4M《太乙金镜式经》卷四 -> C8 的显式适配层。

原则：
- 只有显式 source_profile=jinjing_siku_volume4 时才接受 J4M 结果；
- 不修改 C8 volume5_strict 默认行为；
- J4M-01/02 只映射为 C8-L2 上游事实；
- J4M-04 完整结果作为 source-specific overlay 保存，不覆盖 C8-L3 的 winner/policy。
"""

from .jinjing_v4_military import J4M_RULESET, J4M_SOURCE_PROFILE
from .junshi_zhanlue import junshi_zhanlue


ADAPTER_ID = "jinjing-v4-to-c8-explicit-v1"


def _validate_j4m_result(value, rule_id):
    if value is None:
        return None
    if not isinstance(value, dict):
        return f"{rule_id} result must be a dict"
    if value.get("source_profile") != J4M_SOURCE_PROFILE:
        return f"{rule_id} source_profile mismatch"
    if value.get("ruleset") != J4M_RULESET:
        return f"{rule_id} ruleset mismatch"
    if value.get("rule_id") != rule_id:
        return f"expected {rule_id}, got {value.get('rule_id')}"
    return None


def adapt_j4m_to_c8(*, source_profile,
                     three_doors_result=None,
                     five_generals_result=None,
                     host_guest_result=None,
                     home_cal=None, away_cal=None,
                     taiyi=None, skyeyes=None,
                     home_general_state=None, away_general_state=None,
                     home_general_palace=None, away_general_palace=None):
    """把经来源校勘的 J4M 事实显式送入 C8，不改 C8 默认 profile。"""

    if source_profile != J4M_SOURCE_PROFILE:
        return {
            "adapter": ADAPTER_ID,
            "status": "rejected_source_profile",
            "computable": False,
            "requested_source_profile": source_profile,
            "required_source_profile": J4M_SOURCE_PROFILE,
            "policy": "必须显式指定 jinjing_siku_volume4；不得把其他来源伪装成 J4M。",
        }

    errors = []
    for value, rule_id in (
        (three_doors_result, "J4M-01"),
        (five_generals_result, "J4M-02"),
        (host_guest_result, "J4M-04"),
    ):
        error = _validate_j4m_result(value, rule_id)
        if error:
            errors.append(error)

    if errors:
        return {
            "adapter": ADAPTER_ID,
            "status": "invalid_j4m_inputs",
            "computable": False,
            "source_profile": source_profile,
            "errors": errors,
            "policy": "只消费同一 J4M ruleset/profile 的经校勘结果。",
        }

    three_doors_ready = (
        three_doors_result.get("three_doors_ready")
        if isinstance(three_doors_result, dict)
        else None
    )
    five_generals_released = (
        five_generals_result.get("five_generals_released")
        if isinstance(five_generals_result, dict)
        else None
    )

    c8 = junshi_zhanlue(
        home_cal=home_cal,
        away_cal=away_cal,
        taiyi=taiyi,
        skyeyes=skyeyes,
        three_doors=three_doors_ready,
        five_generals=five_generals_released,
        home_general_state=home_general_state,
        away_general_state=away_general_state,
        home_general_palace=home_general_palace,
        away_general_palace=away_general_palace,
    )

    overlay = None
    if host_guest_result is not None:
        overlay = {
            "rule_id": "J4M-04",
            "source_profile": J4M_SOURCE_PROFILE,
            "context": host_guest_result.get("context"),
            "roles": host_guest_result.get("roles"),
            "action_status": host_guest_result.get("action_status"),
            "action_advice": host_guest_result.get("action_advice"),
            "source_campaign_verdict": host_guest_result.get("source_campaign_verdict"),
            "source_temporal_outcome": host_guest_result.get("source_temporal_outcome"),
            "winner": host_guest_result.get("winner"),
            "start_deity": host_guest_result.get("start_deity"),
            "cross_side_calc_reference": host_guest_result.get("cross_side_calc_reference"),
            "policy": "overlay 只保存 J4M-04 完整来源语义；不覆盖 C8-L3 默认 winner/policy。",
        }

    return {
        "adapter": ADAPTER_ID,
        "status": "ok",
        "computable": True,
        "source_profile": J4M_SOURCE_PROFILE,
        "ruleset": J4M_RULESET,
        "mapped_inputs": {
            "J4M-01.three_doors_ready -> C8-L2": three_doors_ready,
            "J4M-02.five_generals_released -> C8-L2": five_generals_released,
        },
        "j4m_overlay": {
            "host_guest_full": overlay,
        },
        "c8_result": c8,
        "default_c8_profile_unchanged": c8.get("source_profile") == "volume5_strict",
        "policy": [
            "J4M-01/02 只作为 C8-L2 上游事实。",
            "J4M-04 作为显式 overlay，不替换 C8-L3。",
            "J4M-03 不进入 adapter，因日计纳音公式仍 partial。",
            "未显式调用本 adapter 时，C8 volume5_strict 行为完全不变。",
        ],
    }
