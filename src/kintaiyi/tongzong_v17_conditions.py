"""C33 兼容适配层：卷十七 V17-06/07/08/09。

canonical runtime 位于 tongzong_v17_structured.py。
本模块只保留旧函数名与旧字段形状，不再维护第二套古法判断公式。
"""

from __future__ import annotations

from typing import Any

from .tongzong_v17_structured import (
    C27_VERSION,
    capture_fugitive as _capture_fugitive,
    prisoner_official as _prisoner_official,
    report_truth as _report_truth,
    request_outcome as _request_outcome,
)

COMPAT_VERSION = "taiyi-c33-v17-conditions-compat-v1"

_EFFECT_MAP = {
    "不善之事为实": "实",
    "善事为虚": "虚",
    "吉事应吉": "吉",
    "凶事应凶": "凶",
    "吉事不吉": "不吉",
    "闻吉则吉": "吉",
    "闻凶不凶": "不凶",
    "闻忧则忧": "忧",
    "闻喜不喜": "不喜",
    "闻忧不忧": "不忧",
    "闻喜即喜": "喜",
}


def _compat_meta(data: dict[str, Any]) -> dict[str, Any]:
    return {
        **data,
        "compat_adapter": True,
        "compat_version": COMPAT_VERSION,
        "canonical_runtime": "tongzong_v17_structured",
    }


def hearsay_reality(
    reported_kind: str,
    *,
    skyeyes_yanji_taiyi: bool = False,
    three_doors_ready: bool | None = None,
    five_generals_released: bool | None = None,
    host_clamps_guest: bool = False,
    skyeyes_realm: str | None = None,
) -> dict[str, Any]:
    src = _report_truth(
        reported_kind,
        skyeyes_yanji_taiyi=skyeyes_yanji_taiyi,
        three_doors_ready=three_doors_ready,
        five_generals_released=five_generals_released,
        host_clamps_guest=host_clamps_guest,
        skyeyes_realm=skyeyes_realm,
    )

    evidence = []
    effects = []
    for item in src["positive_evidence"] + src["negative_evidence"]:
        effect = _EFFECT_MAP.get(item["effect"], item["effect"])
        evidence.append({
            "condition": item["condition"],
            "effect": effect,
            "source_status": "stable",
        })
        effects.append(effect)

    source_variant = None
    if src["source_variants"]:
        variant = src["source_variants"][0]
        source_variant = {
            "field": "doors_ready_generals_released_bad_news",
            "status": "variant_conflict",
            "variants": [
                {
                    "witness": row["witness"],
                    "effect": "凶" if "则凶" in row["effect"] else "不凶",
                }
                for row in variant["readings"]
            ],
            "resolution": variant["resolution"],
        }

    if source_variant is not None:
        resolved = "variant_conflict"
    else:
        uniq = list(dict.fromkeys(effects))
        resolved = "未定" if not uniq else uniq[0] if len(uniq) == 1 else "mixed_evidence"

    return _compat_meta({
        "canonical": C27_VERSION,
        "source_profile": src["source_profile"],
        "source_rule_id": src["source_rule_id"],
        "name": src["name"],
        "status": src["status"],
        "computable": src["computable"],
        "reported_kind": reported_kind,
        "evidence": evidence,
        "resolved_effect": resolved,
        "source_variant": source_variant,
        "policy": "兼容层只翻译canonical runtime结果；异文继续保留variant_conflict。",
    })


def capture_fugitive(
    *,
    guest_clamps_host: bool = False,
    skyeyes_realm: str | None = None,
    shiji_realm: str | None = None,
    host_realm: str | None = None,
    taiyi_host_same_palace: bool = False,
    skyeyes_over_taiyi_host: bool = False,
    skyeyes_masks_taiyi: bool = False,
    both_eyes_outer: bool = False,
    hideout_pattern: str | None = None,
    hideout_qi_state: str | None = None,
) -> dict[str, Any]:
    src = _capture_fugitive(
        guest_clamps_host=guest_clamps_host,
        skyeyes_realm=skyeyes_realm,
        shiji_realm=shiji_realm,
        host_realm=host_realm,
        taiyi_host_same_palace=taiyi_host_same_palace,
        skyeyes_over_taiyi_host=skyeyes_over_taiyi_host,
        skyeyes_masks_taiyi=skyeyes_masks_taiyi,
        both_eyes_outer=both_eyes_outer,
        hideout_pattern=hideout_pattern,
        hideout_qi_state=hideout_qi_state,
    )

    catch = [item["condition"] for item in src["capture_evidence"]]
    miss = [item["condition"] for item in src["no_capture_evidence"]]
    for item in src["special_evidence"]:
        if item["effect"] == "得而复失":
            miss.append("天目掩太乙：得而复失")
        else:
            miss.append(item["condition"] + "：" + item["effect"])

    recommendation = src["pursuit_advice"]
    if recommendation == "可据掩迫之下追捕" and hideout_pattern:
        recommendation = f"可按{hideout_pattern}之下寻其藏匿"
    elif recommendation == "不可往，往则受辱且事不济":
        recommendation = "不可往捕；所捕之地旺相有气"

    if hideout_pattern in {"掩", "迫"} and hideout_qi_state in {"旺", "相"}:
        if "所捕之地旺相有气" not in miss:
            miss.append("所捕之地旺相有气")

    if catch and miss:
        verdict = "mixed_evidence"
    elif catch:
        verdict = "捕得"
    elif miss:
        verdict = "不得"
    else:
        verdict = "未定"

    return _compat_meta({
        "canonical": C27_VERSION,
        "source_profile": src["source_profile"],
        "source_rule_id": src["source_rule_id"],
        "name": src["name"],
        "status": src["status"],
        "computable": src["computable"],
        "verdict": verdict,
        "catch_evidence": catch,
        "miss_evidence": miss,
        "hideout": {
            "pattern": hideout_pattern,
            "qi_state": hideout_qi_state,
            "recommendation": recommendation,
        },
        "policy": "兼容层不重算讨捕规则；不得拿主将旺相代替藏匿地旺相。",
    })


def prison_interrogation(
    *,
    skyeyes_yanji_taiyi: bool = False,
    host_realm: str | None = None,
    host_qi_state: str | None = None,
    taiyi_just_entered_palace: bool = False,
    taiyi_host_same_palace: bool = False,
    skyeyes_over_taiyi_host: bool = False,
) -> dict[str, Any]:
    src = _prisoner_official(
        skyeyes_yanji_taiyi=skyeyes_yanji_taiyi,
        host_realm=host_realm,
        host_qi_state=host_qi_state,
        taiyi_just_entered_palace=taiyi_just_entered_palace,
        taiyi_host_same_palace=taiyi_host_same_palace,
        skyeyes_over_taiyi_host=skyeyes_over_taiyi_host,
    )

    disputed_trigger = skyeyes_yanji_taiyi or host_realm == "外" or host_qi_state == "旺"
    source_variant = None
    if disputed_trigger:
        source_variant = {
            "field": "enter_prison_when_yanji_or_host_outer_or_wang",
            "status": "variant_conflict",
            "variants": [
                {"witness": "太乙统宗宝鉴_CADAL", "effect": "宜对吏入狱、易解"},
                {"witness": "三才世纬引文", "effect": "不可入狱对吏"},
            ],
            "resolution": "preserve_both_no_silent_merge",
        }

    favorable = bool(src["favorable_evidence"])
    delayed = taiyi_just_entered_palace
    if source_variant is not None:
        verdict = "variant_conflict"
    elif favorable and (delayed or host_realm == "内"):
        verdict = "mixed_evidence"
    elif favorable:
        verdict = "易解"
    elif delayed:
        verdict = "迟留难解"
    elif host_realm == "内":
        verdict = "不宜"
    else:
        verdict = "未定"

    return _compat_meta({
        "canonical": C27_VERSION,
        "source_profile": src["source_profile"],
        "source_rule_id": src["source_rule_id"],
        "name": src["name"],
        "status": src["status"],
        "computable": src["computable"],
        "verdict": verdict,
        "evidence": [*src["favorable_evidence"], *src["unfavorable_evidence"]],
        "source_variant": source_variant,
        "home_cal_release_rule_applied": False,
        "policy": "兼容层调用canonical prisoner_official；旧16/26/36自动解规则仍不应用，未见该条。",
    })


def request_gain(
    *,
    skyeyes_realm: str | None,
    host_clamps_guest: bool = False,
    guest_clamps_host: bool = False,
    host_realm: str | None = None,
    skyeyes_ge_taiyi: bool = False,
    host_qi_state: str | None = None,
    season: str | None = None,
    skyeyes_calc_digit: int | None = None,
) -> dict[str, Any]:
    src = _request_outcome(
        skyeyes_realm=skyeyes_realm,
        host_clamps_guest=host_clamps_guest,
        guest_clamps_host=guest_clamps_host,
        host_realm=host_realm,
        skyeyes_ge_taiyi=skyeyes_ge_taiyi,
        host_qi_state=host_qi_state,
        season=season,
        skyeyes_calc_digit=skyeyes_calc_digit,
    )

    gain = [item["condition"] for item in src["positive_evidence"]]
    no_gain = [item["condition"] for item in src["negative_evidence"]]
    verdict = {
        "positive": "有得",
        "negative": "不得",
        "mixed_evidence": "mixed_evidence",
        "undetermined": "未定",
    }[src["summary"]]

    return _compat_meta({
        "canonical": C27_VERSION,
        "source_profile": src["source_profile"],
        "source_rule_id": src["source_rule_id"],
        "name": src["name"],
        "status": src["status"],
        "computable": src["computable"],
        "verdict": verdict,
        "gain_evidence": gain,
        "no_gain_evidence": no_gain,
        "absolute_qi_number": src["absolute_qi_number"],
        "cross_volume_helper_used": False,
        "policy": "兼容层只翻译V17-09结果；不调用V17-D1孤虚对照。",
    })


def c27_catalog() -> dict[str, Any]:
    return {
        "canonical": C27_VERSION,
        "compat_adapter": True,
        "canonical_runtime": "tongzong_v17_structured",
        "implemented": ["V17-06", "V17-07", "V17-08", "V17-09"],
        "structured_conditions_only": True,
        "known_variants": [
            "V17-06_doors_ready_bad_news",
            "V17-08_prison_entry_conditions",
        ],
        "policy": "旧模块仅适配字段，不维护第二套古法公式。",
    }
