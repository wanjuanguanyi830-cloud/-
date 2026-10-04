"""Shared spatial and five-phase primitives for source-limited Taiyi rules."""

from .taiyi_space import (
    FIRE_TWELVE_STAGES,
    GOD_NAMES_BY_POSITION,
    PALACE_CENTER_POSITION,
    PALACE_ELEMENT,
    PALACE_RING,
    POSITION_TO_PALACE,
    SIXTEEN_RING,
    dashen_from_lushen,
    element_at,
    element_for_palace,
    fire_stage,
    palace_for_position,
    palace_position,
    qi_state,
)

__all__ = [
    "FIRE_TWELVE_STAGES", "GOD_NAMES_BY_POSITION", "PALACE_CENTER_POSITION",
    "PALACE_ELEMENT", "PALACE_RING", "POSITION_TO_PALACE", "SIXTEEN_RING",
    "dashen_from_lushen", "element_at", "element_for_palace", "fire_stage",
    "palace_for_position", "palace_position", "qi_state",
]

