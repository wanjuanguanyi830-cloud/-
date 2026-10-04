"""Versioned v1 war-method rules, isolated from the JinJing ruleset."""

from .eight_divinations import (
    RULESET_ID as EIGHT_DIVINATIONS_RULESET_ID,
    RULESET_VERSION as EIGHT_DIVINATIONS_RULESET_VERSION,
    attack_realm,
    calc_components,
    calc_length,
    compare_calcs,
    gudan_state,
    three_talent,
    troop_readiness,
    wuyin_from_calc,
    yin_yang_disaster,
)
from .seven_tactics import (
    RULESET_ID as SEVEN_TACTICS_RULESET_ID,
    RULESET_VERSION as SEVEN_TACTICS_RULESET_VERSION,
    white_cloud_roll,
    white_dragon_cloud,
    lion_reversal,
    fierce_tiger,
    linjin_ask_way,
    return_army,
    thunder_god_water,
)

__all__ = [
    "EIGHT_DIVINATIONS_RULESET_ID", "EIGHT_DIVINATIONS_RULESET_VERSION",
    "SEVEN_TACTICS_RULESET_ID", "SEVEN_TACTICS_RULESET_VERSION",
    "attack_realm", "calc_components", "calc_length", "compare_calcs",
    "gudan_state", "three_talent", "troop_readiness", "wuyin_from_calc", "yin_yang_disaster",
    "white_cloud_roll", "white_dragon_cloud", "lion_reversal", "fierce_tiger",
    "linjin_ask_way", "return_army", "thunder_god_water",
]

