"""Public mathematical inputs for the separately reviewed minute rules.

This additive profile deliberately stops before pattern interpretation/scoring.
It neither repairs a chart from an ancient example nor selects a chart profile.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json

from .taiyi_generals import G7_SOURCE_PROFILE, host_guest_generals
from .taiyi_rules import (
    INTRINSIC_WX, PALACE_POINT, PALACE_WX, POSITION_WX, SIXTEEN,
    integer, qi_state, sector_to_nine_palace, validate_sector,
)
from .tongzong_v2_doors import three_readiness_bundle

PROFILE = "reviewed_minute_math_facts_20261015_v1"
FACT_CONTRACT = "MINUTE-REVIEW-INPUT-FACTS-V1"
ROLES = ("home_general", "home_vassal", "away_general", "away_vassal")
INTRINSIC_NAMES = dict(zip(ROLES, ("主大将", "主参将", "客大将", "客参将")))


def _hash(value):
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(data.encode("utf-8")).hexdigest()


def reviewed_minute_input_facts(
    *, source_profile, chart_source_profile, general_source_profile, taiyi, wenchang, shiji,
    home_cal, away_cal, asserted_generals,
):
    """Validate saved generals and expose exact mathematical facts.

    asserted_generals is mandatory: inconsistent stored positions are rejected,
    not silently overwritten. A blocked pair is explicitly center 5/5, matching
    the known-center representation; it is not a normal released pair.
    """
    if source_profile != PROFILE:
        raise ValueError("explicit reviewed minute math source profile required")
    if general_source_profile != G7_SOURCE_PROFILE:
        raise ValueError("matching explicit G7 general source profile required")
    if not isinstance(chart_source_profile, str) or not chart_source_profile.strip():
        raise ValueError("chart source profile required")
    integer(taiyi, 1, 9)
    if taiyi not in PALACE_POINT:
        raise ValueError("Taiyi in center 5 is an invalid chart")
    validate_sector(wenchang)
    validate_sector(shiji)
    if not isinstance(asserted_generals, dict) or set(asserted_generals) != set(ROLES):
        raise ValueError("exact four saved general positions required")
    for palace in asserted_generals.values():
        integer(palace, 1, 9)
    calculated = host_guest_generals(home_cal, away_cal)
    for roles, side in ((ROLES[:2], "host"), (ROLES[2:], "guest")):
        pair = calculated[side]
        expected = (5, 5) if pair["blocked"] else (
            pair["big_general_palace"], pair["assistant_general_palace"],
        )
        if tuple(asserted_generals[role] for role in roles) != expected:
            raise ValueError("saved general positions disagree with mathematical calculation")

    inputs = {
        "taiyi": taiyi, "wenchang": wenchang, "shiji": shiji,
        "home_cal": home_cal, "away_cal": away_cal,
        "asserted_generals": dict(asserted_generals),
        "chart_source_profile": chart_source_profile,
        "general_source_profile": general_source_profile,
    }
    roles = {"taiyi": taiyi, **asserted_generals}
    sectors = {role: PALACE_POINT.get(palace) for role, palace in roles.items()}
    sectors.update({"wenchang": wenchang, "shiji": shiji})
    positions = {}
    for role, sector in sectors.items():
        palace = roles[role] if role in roles else sector_to_nine_palace(sector)
        name = INTRINSIC_NAMES.get(role, {"taiyi": "太乙", "wenchang": "文昌", "shiji": "始击"}.get(role))
        intrinsic = INTRINSIC_WX[name]
        eye = role in ("wenchang", "shiji")
        element = POSITION_WX[sector] if eye else PALACE_WX[palace]
        state = qi_state(intrinsic, element)
        positions[role] = {
            "sector": sector, "palace": palace,
            "is_intershen": sector is not None and SIXTEEN.index(sector) % 2 == 1,
            "intrinsic_element": intrinsic, "landing_element": element,
            "self_qi": state,
            "qi_coordinate": "SIXTEEN_SECTOR" if eye else "NINE_PALACE",
            "death_full_name": "死绝" if state == "死" else None,
            "known_center": palace == 5,
        }

    # Geometry is reported separately from an interpretation. A same-palace
    # affiliation never moves an intershen actor to a palace center.
    actor_roles = [role for role, sector in sectors.items()
                   if sector is not None and SIXTEEN.index(sector) % 2 == 0]
    geometries = []
    for target, target_sector in sectors.items():
        if target_sector is None:
            continue
        index = SIXTEEN.index(target_sector)
        distance = 1 if index % 2 else 2
        neighbors = {(index - distance) % 16, (index + distance) % 16}
        for left, right in combinations(actor_roles, 2):
            if target in (left, right):
                continue
            if {SIXTEEN.index(sectors[left]), SIXTEEN.index(sectors[right])} == neighbors:
                geometries.append({
                    "target": target, "target_sector": target_sector,
                    "actors": sorted((left, right)),
                    "actor_sectors": {left: sectors[left], right: sectors[right]},
                    "coordinate": "EXACT_SIXTEEN_SECTOR_ADJACENT_CENTERS",
                })
    geometries.sort(key=lambda g: (g["target"], g["actors"]))

    doors = three_readiness_bundle(
        taiyi_palace=taiyi, tianmu=wenchang,
        host_big_palace=asserted_generals["home_general"], wenchang=wenchang,
        guest_big_palace=asserted_generals["away_general"], shiji=shiji,
    )
    result = {
        "schema_version": "1.0", "fact_contract_id": FACT_CONTRACT, "source_profile": PROFILE,
        "chart_source_profile": chart_source_profile, "inputs": inputs,
        "general_source_profile": general_source_profile,
        "chart_replay_verified_by_this_operation": False,
        "input_hash": _hash(inputs), "general_calculation": calculated,
        "positions": positions, "flank_geometries": geometries,
        "door_contexts": doors,
        "door_context_basis": "SAME_SELECTED_CHART_POSITIONS_FIXED_OPEN_ANCHOR",
        "time_duty_door_substituted": False,
        "pattern_interpretation": {
            "status": "NOT_BOUND_BY_THIS_MATHEMATICAL_FACT_OPERATION",
            "flank_geometry_is_not_an_approved_tixie_or_xiebi_trigger": True,
            "composite_groups_and_dedup_not_inferred": True,
        },
        "no_ancient_layout_override": True,
        "prediction_generation_enabled": False,
    }
    result["content_hash"] = _hash(result)
    return result
