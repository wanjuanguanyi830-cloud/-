"""《太乙金鏡式經》卷四八門值事週期。"""

from __future__ import annotations


DOOR_ORDER = ("開", "休", "生", "傷", "杜", "景", "死", "驚")
DOOR_PERIOD = 30
DOOR_CYCLE = DOOR_PERIOD * len(DOOR_ORDER)


def eight_door(accumulated_year: int) -> str:
    """Return the duty door for a one-based accumulated year.

    Residue zero denotes the end of the 240-year cycle, not year zero of the
    next cycle. Zero is accepted for compatibility with the reference API and
    maps to the same final interval as 240.
    """
    if isinstance(accumulated_year, bool) or not isinstance(accumulated_year, int):
        raise TypeError("accumulated_year must be an integer")
    if accumulated_year < 0:
        raise ValueError("accumulated_year must be non-negative")
    cycle_year = accumulated_year % DOOR_CYCLE or DOOR_CYCLE
    return DOOR_ORDER[(cycle_year - 1) // DOOR_PERIOD]

