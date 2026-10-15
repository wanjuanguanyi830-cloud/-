"""Maintainer-reviewed geju profile; historical Jinjing output stays unchanged.

Accept positions from the caller's independently replayed, explicitly pinned
chart source. In particular, do not repair FT36 positions with the G7 formula.
No football points or score predictions are calculated in this module.
"""

from hashlib import sha256
from itertools import combinations, product
import json

from rules.jinjing.geju.engine import GejuContext, analyze_geju

from .taiyi_rules import (
    INTRINSIC_WX, PALACE_POINT, PALACE_WX, POSITION_WX, SIXTEEN,
    integer, qi_state, sector_to_nine_palace, validate_sector,
)
from .tongzong_v2_doors import (three_readiness_bundle, taiyi_door_readiness,
                                 host_door_readiness, guest_door_readiness)

PROFILE = "maintainer_reviewed_geju_20261015_v1"
CENTER_DOOR_PROFILE = "maintainer_reviewed_geju_20261015_v1_1"
RULE_ID = "REVIEWED-GEJU-V1"
ROLE_NAMES = {
    "taiyi": "太乙", "wenchang": "文昌", "shiji": "始擊",
    "home_general": "主大", "home_vassal": "主參",
    "away_general": "客大", "away_vassal": "客參",
}
FROM_NAME = {value: key for key, value in ROLE_NAMES.items()}
GENERALS = ("home_general", "home_vassal", "away_general", "away_vassal")
INTRINSIC_NAMES = dict(zip(GENERALS, ("主大将", "主参将", "客大将", "客参将")))
BASE = {"掩", "擊", "囚", "迫", "關", "格", "對"}


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":")).encode()).hexdigest()


def reviewed_geju_facts(*, source_profile, chart_source_profile, taiyi, wenchang,
                        shiji, home_general, home_vassal, away_general,
                        away_vassal, home_cal, away_cal):
    if source_profile not in {PROFILE, CENTER_DOOR_PROFILE}:
        raise ValueError("explicit reviewed geju source profile required")
    if not isinstance(chart_source_profile, str) or not chart_source_profile.strip():
        raise ValueError("chart source profile required")
    integer(taiyi, 1, 9)
    if taiyi not in PALACE_POINT:
        raise ValueError("Taiyi center5 is a chart bug")
    validate_sector(wenchang)
    validate_sector(shiji)
    integer(home_cal, 1, 40)
    integer(away_cal, 1, 40)
    generals = dict(zip(GENERALS, (home_general, home_vassal, away_general, away_vassal)))
    for palace in generals.values():
        integer(palace, 1, 9)
    inputs = dict(source_profile=source_profile, chart_source_profile=chart_source_profile,
                  taiyi=taiyi, wenchang=wenchang, shiji=shiji,
                  home_cal=home_cal, away_cal=away_cal, **generals)
    input_hash = digest(inputs)
    sectors = {"taiyi": PALACE_POINT[taiyi], "wenchang": wenchang, "shiji": shiji,
               **{role: PALACE_POINT.get(p) for role, p in generals.items()}}
    positions = {}
    for role, sector in sectors.items():
        eye = role in ("wenchang", "shiji")
        palace = sector_to_nine_palace(sector) if eye else ({"taiyi": taiyi, **generals})[role]
        intrinsic_name = INTRINSIC_NAMES.get(role, {"taiyi": "太乙", "wenchang": "文昌", "shiji": "始击"}.get(role))
        element = POSITION_WX[sector] if eye else PALACE_WX[palace]
        state = qi_state(INTRINSIC_WX[intrinsic_name], element)
        in_region = palace in ({1, 8, 3, 4} if role.startswith("home_") else {9, 2, 7, 6})
        positions[role] = {
            "palace": palace, "sector": sector,
            "is_intershen": sector is not None and SIXTEEN.index(sector) % 2 == 1,
            "intrinsic_element": INTRINSIC_WX[intrinsic_name], "landing_element": element,
            "qi_coordinate": "SIXTEEN_SECTOR" if eye else "NINE_PALACE",
            "self_qi": state, "death_full_name": "死绝" if state == "死" else None,
            "still_can_fight_eligible": role in GENERALS and in_region and state in {"旺", "相"},
        }
    events = []

    def add(pattern, actors, target, relation, *, components=(), supports=(), branch="BASE"):
        event = {"rule_id": RULE_ID, "pattern": pattern, "actors": sorted(set(actors)),
                 "target": target, "relation": relation, "branch": branch,
                 "component_event_ids": sorted(set(components)),
                 "support_pairs": sorted(supports), "input_hash": input_hash}
        event["event_id"] = digest(event)
        prior = next((old for old in events if old["event_id"] == event["event_id"]), None)
        if prior:
            return prior
        events.append(event)
        return event

    old = analyze_geju(GejuContext(taiyi=taiyi, wenchang=wenchang, shiji=shiji,
                                  home_big=home_general, home_vassal=home_vassal,
                                  away_big=away_general, away_vassal=away_vassal))
    for raw in old["事件"]:
        if raw["格局"] not in BASE:
            continue
        event = add(raw["格局"], [FROM_NAME[a] for a in raw["主體"]],
                    FROM_NAME.get(raw["目標"]), raw["位置"])
        event["source_signature"] = raw
    base = list(events)

    # Exact centers only: an intershen may be a victim, never a projected actor.
    actors = [r for r, s in sectors.items() if s is not None and SIXTEEN.index(s) % 2 == 0]
    support_by_target = {}
    ty_index = SIXTEEN.index(sectors["taiyi"])
    for target, sector in sectors.items():
        if sector is None:
            continue
        index = SIXTEEN.index(sector)
        step = 1 if index % 2 else 2
        neighbors = {(index - step) % 16, (index + step) % 16}
        supports = []
        for a, b in combinations(actors, 2):
            if target in (a, b) or {SIXTEEN.index(sectors[a]), SIXTEEN.index(sectors[b])} != neighbors:
                continue
            independent = {a, b} in (set(GENERALS[:2]), set(GENERALS[2:]))
            local = (index - ty_index) % 16 in {0, 1, 2, 14, 15}
            around_taiyi = (target == "taiyi" or "taiyi" in (a, b)
                            or sectors[a] == sectors["taiyi"] or sectors[b] == sectors["taiyi"])
            no_opposition = all((SIXTEEN.index(sectors[r]) - ty_index) % 16 != 8 for r in (a, b, target))
            if independent or (local and around_taiyi and no_opposition):
                supports.append(sorted((a, b)))
        if supports:
            support_by_target[target] = supports
    closure_support = []
    if positions["wenchang"]["is_intershen"] and positions["shiji"]["is_intershen"]:
        for wc, sj in product(support_by_target.get("wenchang", []), support_by_target.get("shiji", [])):
            actual = set(wc + sj)
            if "taiyi" in actual and actual.intersection(GENERALS[:2]) and actual.intersection(GENERALS[2:]):
                closure_support.append([wc, sj])
    if closure_support:
        actual = {role for proof in closure_support for pair in proof for role in pair}
        constituents = [e["event_id"] for e in base if e["pattern"] in {"囚", "迫", "擊"}
                        and set(e["actors"]) <= {"wenchang", "shiji"}]
        event = add("挾閉", actual, "wenchang,shiji", "間神", components=constituents, branch="VERIFIED_DOUBLE_EYE")
        event["eye_support_pairs"] = closure_support
    for target, supports in support_by_target.items():
        if closure_support and target in {"wenchang", "shiji"}:
            continue
        participants = {role for support in supports for role in support}
        # Explicit constituent relations, not all events sharing one position.
        components = [e["event_id"] for e in base if e["pattern"] in {"囚", "迫", "擊"}
                      and (target in e["actors"] or (target == "taiyi" and set(e["actors"]) <= participants))]
        add("提挾", participants, target, "間神" if positions[target]["is_intershen"] else "正宮",
            components=components, supports=supports, branch="VERIFIED_TARGET_FLANKING")

    guards = [e for e in base if e["pattern"] == "關"]
    prisons = [e for e in base if e["pattern"] == "囚"]
    parents = []
    for eye, branch in (("wenchang", "HOME"), ("shiji", "AWAY")):
        if eye == "wenchang":
            qiu = [e for e in prisons if e["actors"] == ["wenchang"]]
            groups = [[*qiu, guard] for guard in guards] if qiu else []
        elif positions[eye]["palace"] == taiyi:
            valid_guards = [g for g in guards if set(g["actors"]) in (
                set(GENERALS[2:]), {"home_general", "away_general"}, {"home_vassal", "away_vassal"},
            )]
            groups = [[guard] for guard in valid_guards]
            groups += [[q] for q in prisons if q["actors"][0] in GENERALS[2:]]
        else:
            groups = []
        for group in groups:
            participants = {eye, "taiyi", *(r for e in group for r in e["actors"])}
            components = [*group, *(q for q in prisons if set(q["actors"]) <= participants)]
            parents.append(add("四郭固", participants - {"taiyi"}, "taiyi", "復合",
                               components=[e["event_id"] for e in components], branch=branch))
    # Enumerate verified groups before resolving the once-per-side policy.
    # All component membership remains available; no first-returned guard wins.
    if positions["wenchang"]["palace"] == away_vassal != 5 and home_vassal == away_general != 5:
        all_members = {identity for p in parents for identity in p["component_event_ids"]}
        for branch in ("HOME", "AWAY"):
            grouped = [p for p in parents if p["branch"] == branch]
            if not grouped:
                continue
            members = {identity for p in grouped for identity in p["component_event_ids"]}
            extra = [e for e in base if e["pattern"] in {"掩", "迫", "關", "格"} and e["event_id"] not in all_members]
            if extra:
                event = add("四郭杜", ("away_vassal", "wenchang", "home_vassal", "away_general"), None, "復合",
                            components=[p["event_id"] for p in grouped], branch=branch)
                event["extra_categories"] = sorted({e["pattern"] for e in extra})
                event["extra_event_ids"] = sorted(e["event_id"] for e in extra)
                event["parent_component_event_ids"] = sorted(members)

    center_door_policy = source_profile == CENTER_DOOR_PROFILE
    if center_door_policy:
        def center_door(name):
            return {"status": "NOT_APPLICABLE_CENTER", "context": name, "computable": False,
                    "anchor_palace": 5, "door_ready": None,
                    "reason": "MAINTAINER_EXCLUDES_CENTER_FROM_EIGHT_DOORS"}
        door_bundle = {
            "taiyi": taiyi_door_readiness(taiyi, tianmu=wenchang),
            "host": center_door("HOME") if home_general == 5 else host_door_readiness(
                home_general, taiyi_palace=taiyi, wenchang=wenchang),
            "guest": center_door("AWAY") if away_general == 5 else guest_door_readiness(
                away_general, taiyi_palace=taiyi, shiji=shiji),
        }
    else:
        door_bundle = three_readiness_bundle(
            taiyi_palace=taiyi, tianmu=wenchang, host_big_palace=home_general,
            wenchang=wenchang, guest_big_palace=away_general, shiji=shiji,
        )
    blockers = [e["event_id"] for e in base if (
        (e["actors"] == ["shiji"] and e["pattern"] in {"掩", "擊"})
        or (e["actors"] == ["wenchang"] and e["pattern"] in {"囚", "迫"})
        or (e["pattern"] in {"格", "對"} and set(e["actors"]).intersection(GENERALS))
    )]
    readiness = {}
    for name, key, calc in (("TAIYI", "taiyi", home_cal), ("HOME", "host", home_cal), ("AWAY", "guest", away_cal)):
        door = door_bundle[key]
        duse = calc in {5, 15, 25, 35}
        if center_door_policy and door["status"] == "NOT_APPLICABLE_CENTER":
            readiness[name] = {"door": door, "generals_blockers": sorted(blockers),
                               "duse": duse, "computable": False, "ready": None,
                               "not_applicable": True, "missing_reason": None,
                               "applicability_reason": "CENTER_ANCHOR_EXCLUDED"}
            continue
        known_blocked = bool(blockers) or duse
        computable = door["computable"] is True or known_blocked
        ready = False if known_blocked else door["door_ready"]
        readiness[name] = {"door": door, "generals_blockers": sorted(blockers),
                           "duse": duse, "computable": computable, "ready": ready,
                           "missing_reason": None if computable else "DOOR_ANCHOR_NOT_COMPUTABLE"}
    result = {"rule_id": RULE_ID, "source_profile": source_profile, "schema_version": "1.0",
              "inputs": inputs, "input_hash": input_hash, "positions": positions,
              "events": sorted(events, key=lambda e: e["event_id"]), "readiness": readiness,
              "complete": all(r["computable"] or r.get("not_applicable") is True for r in readiness.values()),
              "calculation_profile_repaired_or_swapped": False,
              "door_time_basis": "SAME_SELECTED_MINUTE_CHART_FIXED_OPEN_ANCHOR_NOT_C119_DUTY_CYCLE",
              "ancient_board_exception_applied": False}
    result["content_hash"] = digest(result)
    return result
