"""C27 卷十七结构条件型规则。

实现 V17-06/07/08/09。只消费显式结构化条件，不解析旧中文断语。
"""

from __future__ import annotations

import copy
from typing import Any

C27_VERSION = "taiyi-c27-tongzong-v17-structured-v1"
SOURCE_PROFILE = "tongzong_volume17"

ONLINE_WITNESS = {
    "provider": "识典古籍",
    "title": "太乙统宗宝鉴卷十七",
    "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny53enihb1e",
}


def _base(rule_id: str, name: str, source_section: str) -> dict[str, Any]:
    return {
        "canonical": C27_VERSION,
        "source_profile": SOURCE_PROFILE,
        "source_rule_id": rule_id,
        "name": name,
        "source_section": source_section,
        "online_witness": copy.deepcopy(ONLINE_WITNESS),
        "cross_c8_merge": False,
        "cross_j4m_merge": False,
    }


def _summary(positive: list[dict[str, Any]], negative: list[dict[str, Any]]) -> str:
    if positive and negative:
        return "mixed_evidence"
    if positive:
        return "positive"
    if negative:
        return "negative"
    return "undetermined"


def report_truth(
    reported_kind: str,
    *,
    skyeyes_yanji_taiyi: bool = False,
    three_doors_ready: bool | None = None,
    five_generals_released: bool | None = None,
    host_clamps_guest: bool = False,
    skyeyes_realm: str | None = None,
) -> dict[str, Any]:
    """V17-06 见闻虚实。

    reported_kind: 吉/凶/忧/喜。
    不把多条条件压成单一if/elif；各条证据并列返回。
    """
    if reported_kind not in {"吉", "凶", "忧", "喜"}:
        raise ValueError("reported_kind须为吉/凶/忧/喜")
    for name, value in {
        "skyeyes_yanji_taiyi": skyeyes_yanji_taiyi,
        "host_clamps_guest": host_clamps_guest,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{name}须为bool")
    for name, value in {
        "three_doors_ready": three_doors_ready,
        "five_generals_released": five_generals_released,
    }.items():
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"{name}须为bool或None")
    if skyeyes_realm is not None and skyeyes_realm not in {"内", "外"}:
        raise ValueError("skyeyes_realm须为内/外/None")

    positive: list[dict[str, Any]] = []
    negative: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []

    if skyeyes_yanji_taiyi:
        if reported_kind in {"凶", "忧"}:
            positive.append({"condition": "天目掩击太乙", "effect": "不善之事为实"})
        elif reported_kind in {"吉", "喜"}:
            negative.append({"condition": "天目掩击太乙", "effect": "善事为虚"})

    if three_doors_ready is True and five_generals_released is True:
        if reported_kind in {"吉", "喜"}:
            positive.append({"condition": "门具将发", "effect": "吉事应吉"})
        elif reported_kind in {"凶", "忧"}:
            variants.append({
                "condition": "门具将发且闻凶",
                "status": "witness_variant",
                "readings": [
                    {"witness": "NGJ识典卷十七", "effect": "闻凶则凶"},
                    {"witness": "CADAL/另一识典见证", "effect": "闻凶不凶"},
                ],
                "resolution": "preserve_both_no_silent_merge",
            })

    if three_doors_ready is False and five_generals_released is False:
        if reported_kind in {"凶", "忧"}:
            negative.append({"condition": "门不具将不发", "effect": "凶事应凶"})
        elif reported_kind in {"吉", "喜"}:
            negative.append({"condition": "门不具将不发", "effect": "吉事不吉"})

    if host_clamps_guest:
        if reported_kind in {"吉", "喜"}:
            positive.append({"condition": "主人挟客", "effect": "闻吉则吉"})
        elif reported_kind in {"凶", "忧"}:
            positive.append({"condition": "主人挟客", "effect": "闻凶不凶"})

    if skyeyes_realm == "内":
        if reported_kind == "忧":
            negative.append({"condition": "天目在内", "effect": "闻忧则忧"})
        elif reported_kind == "喜":
            negative.append({"condition": "天目在内", "effect": "闻喜不喜"})
    elif skyeyes_realm == "外":
        if reported_kind == "忧":
            positive.append({"condition": "天目在外", "effect": "闻忧不忧"})
        elif reported_kind == "喜":
            positive.append({"condition": "天目在外", "effect": "闻喜即喜"})

    return {
        **_base("V17-06", "见闻虚实", "明见闻以占虚实之术"),
        "status": "ok",
        "computable": True,
        "reported_kind": reported_kind,
        "positive_evidence": positive,
        "negative_evidence": negative,
        "source_variants": variants,
        "summary": _summary(positive, negative),
        "policy": "多条件并列保留；门具将发闻凶存在见证异文，不静默择一。",
    }


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
    """V17-07 讨捕叛亡。"""
    for name, value in {
        "guest_clamps_host": guest_clamps_host,
        "taiyi_host_same_palace": taiyi_host_same_palace,
        "skyeyes_over_taiyi_host": skyeyes_over_taiyi_host,
        "skyeyes_masks_taiyi": skyeyes_masks_taiyi,
        "both_eyes_outer": both_eyes_outer,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{name}须为bool")
    for name, value in {
        "skyeyes_realm": skyeyes_realm,
        "shiji_realm": shiji_realm,
        "host_realm": host_realm,
    }.items():
        if value is not None and value not in {"内", "外"}:
            raise ValueError(f"{name}须为内/外/None")
    if hideout_qi_state is not None and hideout_qi_state not in {"旺", "相", "休", "囚", "死"}:
        raise ValueError("hideout_qi_state须为旺/相/休/囚/死/None")

    capture: list[dict[str, Any]] = []
    no_capture: list[dict[str, Any]] = []
    special: list[dict[str, Any]] = []

    if guest_clamps_host:
        capture.append({"condition": "客挟主人", "effect": "捕得"})
    if skyeyes_realm == "内":
        capture.append({"condition": "天目在内", "effect": "捕得"})
    if taiyi_host_same_palace and skyeyes_over_taiyi_host:
        capture.append({"condition": "太乙与主人同宫且天目临之", "effect": "捕得"})
    if host_realm == "外":
        no_capture.append({"condition": "主人在外", "effect": "不得"})
    if both_eyes_outer or (skyeyes_realm == "外" and shiji_realm == "外"):
        no_capture.append({"condition": "二目在外", "effect": "不得"})
    if skyeyes_masks_taiyi:
        special.append({"condition": "天目掩太乙", "effect": "得而复失"})

    pursuit_advice = None
    if hideout_pattern in {"掩", "迫"}:
        if hideout_qi_state in {"旺", "相"}:
            pursuit_advice = "不可往，往则受辱且事不济"
        elif hideout_qi_state is None:
            pursuit_advice = "掩迫处可往，但缺藏匿地旺相输入，未定"
        else:
            pursuit_advice = "可据掩迫之下追捕"
    elif hideout_pattern is not None:
        pursuit_advice = "来源只明确掩迫之下；其他格局不扩断"

    return {
        **_base("V17-07", "讨捕叛亡", "明讨捕叛亡之术"),
        "status": "ok",
        "computable": True,
        "capture_evidence": capture,
        "no_capture_evidence": no_capture,
        "special_evidence": special,
        "summary": _summary(capture, no_capture),
        "hideout_pattern": hideout_pattern,
        "hideout_qi_state": hideout_qi_state,
        "pursuit_advice": pursuit_advice,
        "policy": "藏匿地旺相只作用于hideout_qi_state，不拿主将旺相替代。",
    }


def prisoner_official(
    *,
    skyeyes_yanji_taiyi: bool = False,
    host_realm: str | None = None,
    host_qi_state: str | None = None,
    taiyi_just_entered_palace: bool = False,
    taiyi_host_same_palace: bool = False,
    skyeyes_over_taiyi_host: bool = False,
) -> dict[str, Any]:
    """V17-08 执囚对吏，保留主人内/外异读。"""
    if host_realm is not None and host_realm not in {"内", "外"}:
        raise ValueError("host_realm须为内/外/None")
    if host_qi_state is not None and host_qi_state not in {"旺", "相", "休", "囚", "死"}:
        raise ValueError("host_qi_state须为旺/相/休/囚/死/None")
    for name, value in {
        "skyeyes_yanji_taiyi": skyeyes_yanji_taiyi,
        "taiyi_just_entered_palace": taiyi_just_entered_palace,
        "taiyi_host_same_palace": taiyi_host_same_palace,
        "skyeyes_over_taiyi_host": skyeyes_over_taiyi_host,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{name}须为bool")

    unfavorable: list[dict[str, Any]] = []
    favorable: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []

    if skyeyes_yanji_taiyi:
        unfavorable.append({"condition": "天目掩击太乙", "effect": "不可入狱对吏"})
    if host_qi_state == "旺":
        unfavorable.append({"condition": "主人立旺神", "effect": "不可入狱对吏"})
    if host_realm in {"内", "外"}:
        variants.append({
            "field": "host_realm",
            "input": host_realm,
            "status": "source_variant",
            "readings": [
                {"reading": "主人在外不可入狱", "matches": host_realm == "外"},
                {"reading": "主人在内不可入狱", "matches": host_realm == "内"},
            ],
            "resolution": "preserve_both_no_silent_merge",
        })
    if taiyi_just_entered_palace:
        unfavorable.append({"condition": "太乙初入宫日", "effect": "事迟留难解"})
    if taiyi_host_same_palace and skyeyes_over_taiyi_host:
        favorable.append({"condition": "太乙与主同宫而天目临之", "effect": "入狱易出，遇贵人解忧"})

    return {
        **_base("V17-08", "执囚对吏", "明执囚对吏之术"),
        "status": "ok",
        "computable": True,
        "favorable_evidence": favorable,
        "unfavorable_evidence": unfavorable,
        "source_variants": variants,
        "summary": _summary(favorable, unfavorable),
        "policy": "主人内/外存在相反传本读法，保留variant，不择一覆盖。",
    }


def request_outcome(
    *,
    skyeyes_realm: str | None = None,
    host_clamps_guest: bool = False,
    guest_clamps_host: bool = False,
    host_realm: str | None = None,
    skyeyes_ge_taiyi: bool = False,
    host_qi_state: str | None = None,
    season: str | None = None,
    skyeyes_calc_digit: int | None = None,
) -> dict[str, Any]:
    """V17-09 求索有无所得。"""
    for name, value in {"skyeyes_realm": skyeyes_realm, "host_realm": host_realm}.items():
        if value is not None and value not in {"内", "外"}:
            raise ValueError(f"{name}须为内/外/None")
    for name, value in {
        "host_clamps_guest": host_clamps_guest,
        "guest_clamps_host": guest_clamps_host,
        "skyeyes_ge_taiyi": skyeyes_ge_taiyi,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{name}须为bool")
    if host_qi_state is not None and host_qi_state not in {"旺", "相", "休", "囚", "死"}:
        raise ValueError("host_qi_state须为旺/相/休/囚/死/None")
    if season is not None and season not in {"春", "夏", "秋", "冬"}:
        raise ValueError("season须为春/夏/秋/冬/None")
    if skyeyes_calc_digit is not None:
        if isinstance(skyeyes_calc_digit, bool) or not isinstance(skyeyes_calc_digit, int):
            raise TypeError("skyeyes_calc_digit须为int或None")
        if not 1 <= skyeyes_calc_digit <= 10:
            raise ValueError("skyeyes_calc_digit须在1..10")

    positive: list[dict[str, Any]] = []
    negative: list[dict[str, Any]] = []

    if skyeyes_realm == "内":
        positive.append({"condition": "天目在内", "effect": "请谒求索皆有所得"})
    elif skyeyes_realm == "外":
        negative.append({"condition": "天目在外", "effect": "求索不得"})

    if host_clamps_guest:
        negative.append({"condition": "主人扶客", "effect": "不可请谒求索"})
    if guest_clamps_host:
        positive.append({"condition": "客扶主人", "effect": "求索皆得"})

    if host_realm == "内":
        positive.append({"condition": "主人在内", "effect": "得"})
    elif host_realm == "外":
        negative.append({"condition": "主人在外", "effect": "不得"})

    if skyeyes_ge_taiyi:
        negative.append({"condition": "天目格太乙", "effect": "见贵请谒词讼百事上下相格"})

    if host_qi_state == "旺":
        negative.append({"condition": "主人立旺神", "effect": "不可往见尊长请谒"})

    absolute_qi = False
    if season in {"春", "夏"} and skyeyes_calc_digit == 6:
        absolute_qi = True
    elif season in {"秋", "冬"} and skyeyes_calc_digit == 4:
        absolute_qi = True
    if absolute_qi:
        negative.append({"condition": "天目绝气之数", "effect": "不可请谒干求见贵"})

    return {
        **_base("V17-09", "求索所得", "明求索有无所得术"),
        "status": "ok",
        "computable": True,
        "positive_evidence": positive,
        "negative_evidence": negative,
        "summary": _summary(positive, negative),
        "absolute_qi_number": absolute_qi,
        "policy": "本条独立于V17-D1孤虚对照；多条件冲突时保留mixed_evidence。",
    }


def c27_catalog() -> dict[str, Any]:
    return {
        "canonical": C27_VERSION,
        "implemented": ["V17-06", "V17-07", "V17-08", "V17-09"],
        "dependency_class": "structured_conditions",
        "known_variants": [
            "V17-06_doors_generals_bad_report",
            "V17-08_host_realm",
        ],
        "policy": "只消费结构化事实；不扫描旧中文断语，不与C8/J4M自动综合。",
    }
