"""C27 卷十七条件组合型占断。

实现 V17-06/07/08/09。所有格局、内外、旺相条件必须由上游显式提供，
本模块不解析旧中文断语，也不自行重建太乙宫界。
"""

from __future__ import annotations

import copy
from typing import Any

C27_VERSION = "taiyi-c27-tongzong-v17-conditions-v1"
SOURCE_PROFILE = "tongzong_volume17"

ONLINE_WITNESSES = {
    "tongzong_cadal": {
        "title": "太乙统宗宝鉴",
        "url": "https://www.shidianguji.com/book/CADAL02055529/chapter/1l5erjqepugiz",
    },
    "tongzong_ngj": {
        "title": "太乙统宗宝鉴卷十七",
        "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny53enihb1e",
    },
    "sancai_shiwei": {
        "title": "三才世纬·所引太乙术",
        "url": "https://www.shidianguji.com/book/NCL06493A/chapter/1lz8dh2j1z7yh",
    },
}

QI_STATES = {"旺", "相", "胎", "没", "死", "囚", "休", "废"}
REALMS = {"内", "外"}


def _base(rule_id: str, name: str, section: str) -> dict[str, Any]:
    return {
        "canonical": C27_VERSION,
        "source_profile": SOURCE_PROFILE,
        "source_rule_id": rule_id,
        "name": name,
        "source_section": section,
        "online_witnesses": copy.deepcopy(ONLINE_WITNESSES),
        "cross_c8_merge": False,
        "cross_j4m_merge": False,
        "legacy_prose_parsing": False,
    }


def _resolve_effects(effects: list[str], *, variant_conflict: bool = False) -> str:
    if variant_conflict:
        return "variant_conflict"
    uniq = list(dict.fromkeys(effects))
    if not uniq:
        return "未定"
    if len(uniq) == 1:
        return uniq[0]
    return "mixed_evidence"


def hearsay_reality(
    reported_kind: str,
    *,
    skyeyes_yanji_taiyi: bool = False,
    three_doors_ready: bool | None = None,
    five_generals_released: bool | None = None,
    host_clamps_guest: bool = False,
    skyeyes_realm: str | None = None,
) -> dict[str, Any]:
    """V17-06 明见闻以占虚实。

    reported_kind 使用吉/凶/忧/喜四类。不同条件各自形成证据，
    不按旧函数的if顺序覆盖。
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
    if skyeyes_realm is not None and skyeyes_realm not in REALMS:
        raise ValueError("skyeyes_realm须为内/外/None")

    evidence: list[dict[str, Any]] = []
    effects: list[str] = []
    source_variant = None

    if skyeyes_yanji_taiyi and reported_kind in {"吉", "凶"}:
        effect = "虚" if reported_kind == "吉" else "实"
        evidence.append({
            "condition": "天目掩击太乙",
            "effect": effect,
            "source_status": "stable",
        })
        effects.append(effect)

    door_gen_known = (
        three_doors_ready is not None and five_generals_released is not None
    )
    door_gen_ready = three_doors_ready is True and five_generals_released is True
    door_gen_not_ready = door_gen_known and not door_gen_ready

    if door_gen_ready and reported_kind == "吉":
        evidence.append({
            "condition": "门具将发",
            "effect": "吉",
            "source_status": "stable",
        })
        effects.append("吉")
    elif door_gen_ready and reported_kind == "凶":
        source_variant = {
            "field": "doors_ready_generals_released_bad_news",
            "status": "variant_conflict",
            "variants": [
                {
                    "witness": "太乙统宗宝鉴_CADAL",
                    "effect": "不凶",
                },
                {
                    "witness": "三才世纬引文",
                    "effect": "凶",
                },
            ],
            "resolution": "preserve_both_no_silent_merge",
        }
        evidence.append({
            "condition": "门具将发",
            "effect": "variant_conflict",
            "source_status": "variant",
        })
    elif door_gen_not_ready and reported_kind in {"吉", "凶"}:
        effect = "不吉" if reported_kind == "吉" else "凶"
        evidence.append({
            "condition": "门不具或将不发",
            "effect": effect,
            "source_status": "stable",
        })
        effects.append(effect)

    if host_clamps_guest and reported_kind in {"吉", "凶"}:
        effect = "吉" if reported_kind == "吉" else "不凶"
        evidence.append({
            "condition": "主人挟客",
            "effect": effect,
            "source_status": "attested",
        })
        effects.append(effect)

    if skyeyes_realm == "内" and reported_kind in {"忧", "喜"}:
        effect = "忧" if reported_kind == "忧" else "不喜"
        evidence.append({
            "condition": "天目在内",
            "effect": effect,
            "source_status": "stable",
        })
        effects.append(effect)
    elif skyeyes_realm == "外" and reported_kind in {"忧", "喜"}:
        effect = "不忧" if reported_kind == "忧" else "喜"
        evidence.append({
            "condition": "天目在外",
            "effect": effect,
            "source_status": "stable",
        })
        effects.append(effect)

    return {
        **_base("V17-06", "见闻虚实", "明见闻以占虚实之术"),
        "status": "ok",
        "computable": True,
        "reported_kind": reported_kind,
        "evidence": evidence,
        "resolved_effect": _resolve_effects(
            effects, variant_conflict=source_variant is not None
        ),
        "source_variant": source_variant,
        "policy": (
            "各条件独立列证据；同盘条件互相冲突时保留mixed_evidence。"
            "门具将发遇凶闻存在见证异文，固定variant_conflict。"
        ),
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
    """V17-07 讨捕叛亡。

    关键修正：旺相条件属于“所捕之地/藏匿地”的气，
    不用主将旺相代替。
    """
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
        if value is not None and value not in REALMS:
            raise ValueError(f"{name}须为内/外/None")
    if hideout_pattern not in {None, "掩", "迫"}:
        raise ValueError("hideout_pattern须为掩/迫/None")
    if hideout_qi_state is not None and hideout_qi_state not in QI_STATES:
        raise ValueError("hideout_qi_state须为旺相胎没死囚休废/None")

    catch_evidence: list[str] = []
    miss_evidence: list[str] = []

    if guest_clamps_host:
        catch_evidence.append("客挟主人")
    if shiji_realm == "内":
        catch_evidence.append("下目始击在内")
    if taiyi_host_same_palace and skyeyes_over_taiyi_host:
        catch_evidence.append("太乙与主人同宫而天目临之")
    if skyeyes_realm == "内":
        catch_evidence.append("天目在内")

    if host_realm == "外":
        miss_evidence.append("主人在外")
    if skyeyes_masks_taiyi:
        miss_evidence.append("天目掩太乙：得而复失")
    if both_eyes_outer or (
        skyeyes_realm == "外" and shiji_realm == "外"
    ):
        miss_evidence.append("天目与下目俱在外")

    hideout = {
        "pattern": hideout_pattern,
        "qi_state": hideout_qi_state,
        "recommendation": None,
    }
    if hideout_pattern is not None:
        if hideout_qi_state in {"旺", "相"}:
            hideout["recommendation"] = "不可往捕；所捕之地旺相有气"
            miss_evidence.append("所捕之地旺相有气")
        else:
            hideout["recommendation"] = f"可按{hideout_pattern}之下寻其藏匿"

    if catch_evidence and miss_evidence:
        verdict = "mixed_evidence"
    elif catch_evidence:
        verdict = "捕得"
    elif miss_evidence:
        verdict = "不得"
    else:
        verdict = "未定"

    return {
        **_base("V17-07", "讨捕叛亡", "明讨捕叛亡之术"),
        "status": "ok",
        "computable": True,
        "verdict": verdict,
        "catch_evidence": catch_evidence,
        "miss_evidence": miss_evidence,
        "hideout": hideout,
        "policy": (
            "旺相只作用于藏匿/所捕之地；不得拿主将旺相作为替代。"
            "得机失机并见时保留mixed_evidence。"
        ),
    }


def prison_interrogation(
    *,
    skyeyes_yanji_taiyi: bool = False,
    host_realm: str | None = None,
    host_qi_state: str | None = None,
    taiyi_just_entered_palace: bool = False,
    taiyi_host_same_palace: bool = False,
    skyeyes_over_taiyi_host: bool = False,
) -> dict[str, Any]:
    """V17-08 执囚对吏。

    “天目掩击/主人在外/旺神”在不同见证中有宜入狱与不可入狱的相反读法，
    一律作为source_variant保留。
    """
    if not isinstance(skyeyes_yanji_taiyi, bool):
        raise TypeError("skyeyes_yanji_taiyi须为bool")
    if host_realm is not None and host_realm not in REALMS:
        raise ValueError("host_realm须为内/外/None")
    if host_qi_state is not None and host_qi_state not in QI_STATES:
        raise ValueError("host_qi_state须为旺相胎没死囚休废/None")
    for name, value in {
        "taiyi_just_entered_palace": taiyi_just_entered_palace,
        "taiyi_host_same_palace": taiyi_host_same_palace,
        "skyeyes_over_taiyi_host": skyeyes_over_taiyi_host,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{name}须为bool")

    evidence: list[dict[str, Any]] = []
    source_variant = None

    disputed_trigger = (
        skyeyes_yanji_taiyi
        or host_realm == "外"
        or host_qi_state == "旺"
    )
    if disputed_trigger:
        source_variant = {
            "field": "enter_prison_when_yanji_or_host_outer_or_wang",
            "status": "variant_conflict",
            "variants": [
                {
                    "witness": "太乙统宗宝鉴_CADAL",
                    "effect": "宜对吏入狱、易解",
                },
                {
                    "witness": "三才世纬引文",
                    "effect": "不可入狱对吏",
                },
            ],
            "resolution": "preserve_both_no_silent_merge",
        }
        evidence.append({
            "condition": "掩击/主人在外/旺神",
            "effect": "variant_conflict",
        })

    if host_realm == "内":
        evidence.append({
            "condition": "主人在内",
            "effect": "部分见证作不可入狱对吏",
        })

    if taiyi_just_entered_palace:
        evidence.append({
            "condition": "太乙初入宫",
            "effect": "迟留难解",
        })

    easy_release = (
        taiyi_host_same_palace and skyeyes_over_taiyi_host
    )
    if easy_release:
        evidence.append({
            "condition": "太乙与主人同宫而天目临之",
            "effect": "入狱易出、逢贵人解忧",
        })

    adverse = taiyi_just_entered_palace or host_realm == "内"
    favorable = easy_release

    if source_variant is not None:
        verdict = "variant_conflict"
    elif favorable and adverse:
        verdict = "mixed_evidence"
    elif favorable:
        verdict = "易解"
    elif taiyi_just_entered_palace:
        verdict = "迟留难解"
    elif host_realm == "内":
        verdict = "不宜"
    else:
        verdict = "未定"

    return {
        **_base("V17-08", "执囚对吏", "明执囚对吏之术"),
        "status": "ok",
        "computable": True,
        "verdict": verdict,
        "evidence": evidence,
        "source_variant": source_variant,
        "home_cal_release_rule_applied": False,
        "policy": (
            "不实现参考代码的16/26/36自动解规则：当前已核直接见证未见该条。"
            "文本冲突优先保留source_variant。"
        ),
    }


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
    """V17-09 求索有无所得。"""
    if skyeyes_realm is not None and skyeyes_realm not in REALMS:
        raise ValueError("skyeyes_realm须为内/外/None")
    if host_realm is not None and host_realm not in REALMS:
        raise ValueError("host_realm须为内/外/None")
    for name, value in {
        "host_clamps_guest": host_clamps_guest,
        "guest_clamps_host": guest_clamps_host,
        "skyeyes_ge_taiyi": skyeyes_ge_taiyi,
    }.items():
        if not isinstance(value, bool):
            raise TypeError(f"{name}须为bool")
    if host_qi_state is not None and host_qi_state not in QI_STATES:
        raise ValueError("host_qi_state须为旺相胎没死囚休废/None")
    if season is not None and season not in {"春", "夏", "秋", "冬"}:
        raise ValueError("season须为春/夏/秋/冬/None")
    if skyeyes_calc_digit is not None:
        if isinstance(skyeyes_calc_digit, bool) or not isinstance(skyeyes_calc_digit, int):
            raise TypeError("skyeyes_calc_digit须为int或None")
        if not 1 <= skyeyes_calc_digit <= 10:
            raise ValueError("skyeyes_calc_digit须在1..10")

    gain: list[str] = []
    no_gain: list[str] = []

    if skyeyes_realm == "内":
        gain.append("天目在内：请谒、干求、访人有得")
    elif skyeyes_realm == "外":
        no_gain.append("天目在外：请谒求索不得、访人不见")

    if host_clamps_guest:
        no_gain.append("主人挟客：不可请谒求索")
    if guest_clamps_host:
        gain.append("客挟主人：求索皆得")

    if host_realm == "内":
        gain.append("主人在内为得")
    elif host_realm == "外":
        no_gain.append("主人在外为不得")

    if skyeyes_ge_taiyi:
        no_gain.append("天目格太乙：请谒词讼百事上下格之")

    if host_qi_state == "旺":
        no_gain.append("主人立旺神：不可往见、请谒尊长")

    absolute_qi = False
    if season in {"春", "夏"} and skyeyes_calc_digit == 6:
        absolute_qi = True
    elif season in {"秋", "冬"} and skyeyes_calc_digit == 4:
        absolute_qi = True
    if absolute_qi:
        no_gain.append("天目绝气数：不可请谒干求见贵")

    if gain and no_gain:
        verdict = "mixed_evidence"
    elif gain:
        verdict = "有得"
    elif no_gain:
        verdict = "不得"
    else:
        verdict = "未定"

    return {
        **_base("V17-09", "求索所得", "明求索有无所得术"),
        "status": "ok",
        "computable": True,
        "verdict": verdict,
        "gain_evidence": gain,
        "no_gain_evidence": no_gain,
        "absolute_qi_number": absolute_qi,
        "cross_volume_helper_used": False,
        "policy": (
            "本条独立按卷十七证据判求索；不调用V17-D1孤虚对照。"
            "正负证据并见时保留mixed_evidence。"
        ),
    }


def c27_catalog() -> dict[str, Any]:
    return {
        "canonical": C27_VERSION,
        "implemented": ["V17-06", "V17-07", "V17-08", "V17-09"],
        "structured_conditions_only": True,
        "known_variants": [
            "V17-06_doors_ready_bad_news",
            "V17-08_prison_entry_conditions",
        ],
        "policy": "不解析旧格局字符串；冲突见证并列保存。",
    }
