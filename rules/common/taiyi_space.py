"""Shared Taiyi coordinates and five-phase rules used by the v1 war methods.

The 16-position ring is positional. A point's element comes from its mapped
Taiyi palace, not from the ordinary earthly-branch element table.
"""

from __future__ import annotations

SIXTEEN_RING = (
    "子", "丑", "艮", "寅", "卯", "辰", "巽", "巳",
    "午", "未", "坤", "申", "酉", "戌", "乾", "亥",
)
PALACE_RING = (8, 3, 4, 9, 2, 7, 6, 1)

PALACE_CENTER_POSITION = {
    8: "子", 3: "艮", 4: "卯", 9: "巽",
    2: "午", 7: "坤", 6: "酉", 1: "乾",
}
POSITION_TO_PALACE = {
    "子": 8, "亥": 8,
    "丑": 3, "艮": 3,
    "寅": 4, "卯": 4,
    "辰": 9, "巽": 9,
    "巳": 2, "午": 2,
    "未": 7, "坤": 7,
    "申": 6, "酉": 6,
    "戌": 1, "乾": 1,
}
PALACE_ELEMENT = {
    1: "金", 2: "火", 3: "土", 4: "木", 5: "土",
    6: "金", 7: "土", 8: "水", 9: "木",
}

# The source forms 大炅 and 太炅 are retained at the same recorded position.
# This mapping accepts both for lookup; it does not select an edition's wording.
GOD_NAMES_BY_POSITION = {
    "子": ("地主",), "丑": ("阳德", "陽德"), "艮": ("和德",), "寅": ("吕申", "呂申"),
    "卯": ("高丛", "高叢"), "辰": ("太阳", "太陽"), "巽": ("大炅", "太炅"), "巳": ("大神",),
    "午": ("大威",), "未": ("天道",), "坤": ("大武",), "申": ("武德",),
    "酉": ("太簇",), "戌": ("阴主", "陰主"), "乾": ("阴德", "陰德"), "亥": ("大义", "大義"),
}
GOD_POSITION = {
    name: position
    for position, names in GOD_NAMES_BY_POSITION.items()
    for name in names
}
INNER_GODS = frozenset(("阴德", "陰德", "大义", "大義", "地主", "阳德", "陽德", "和德", "吕申", "呂申", "高丛", "高叢", "太阳", "太陽"))
OUTER_GODS = frozenset(("大炅", "太炅", "大神", "大威", "天道", "大武", "武德", "太簇", "阴主", "陰主"))

FIRE_TWELVE_STAGES = {
    "寅": "長生", "卯": "沐浴", "辰": "冠帶", "巳": "臨官",
    "午": "帝旺", "未": "衰", "申": "病", "酉": "死",
    "戌": "墓", "亥": "絕", "子": "胎", "丑": "養",
}

GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
ELEMENTS = frozenset(GENERATES)
BRANCHES = frozenset(FIRE_TWELVE_STAGES)
_RING_INDEX = {point: index for index, point in enumerate(SIXTEEN_RING)}


def palace_position(palace: int) -> str:
    """Return the 16-ring representative point for a non-central palace."""
    if isinstance(palace, bool) or not isinstance(palace, int):
        raise TypeError("palace must be an integer")
    if palace not in PALACE_CENTER_POSITION:
        raise ValueError("a 16-ring representative exists only for palaces 1,2,3,4,6,7,8,9")
    return PALACE_CENTER_POSITION[palace]


def palace_for_position(position: str) -> int:
    """Return the nine-palace number associated with a 16-ring position."""
    try:
        return POSITION_TO_PALACE[position]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"unknown 16-ring position: {position!r}") from exc


def element_for_palace(palace: int) -> str:
    """Return the Taiyi nine-palace element, including central palace 5."""
    if isinstance(palace, bool) or not isinstance(palace, int):
        raise TypeError("palace must be an integer")
    try:
        return PALACE_ELEMENT[palace]
    except KeyError as exc:
        raise ValueError(f"unknown nine-palace number: {palace!r}") from exc


def element_at(position: str) -> str:
    """Resolve a 16-ring point through its associated palace element."""
    return element_for_palace(palace_for_position(position))


def dashen_from_lushen(anchor: str | int) -> str:
    """Place 吕申 on an anchor and return the 大神 point, four ring steps later.

    An integer anchor is a non-central Taiyi palace and is first converted to
    that palace's representative point. A branch or trigram point is accepted
    directly. Date conversion and sexagenary calendar interpretation are out
    of scope.
    """
    if isinstance(anchor, bool):
        raise TypeError("anchor must be a palace number or 16-ring position")
    if isinstance(anchor, int):
        point = palace_position(anchor)
    elif isinstance(anchor, str) and anchor in _RING_INDEX:
        point = anchor
    else:
        raise ValueError(f"unknown 吕申加位 anchor: {anchor!r}")
    return SIXTEEN_RING[(_RING_INDEX[point] + 4) % len(SIXTEEN_RING)]


def qi_state(subject_element: str, environment_element: str) -> str:
    """Classify a subject in an environment as 旺、相、休、囚、死."""
    if subject_element not in ELEMENTS or environment_element not in ELEMENTS:
        raise ValueError("both elements must be one of 木、火、土、金、水")
    if subject_element == environment_element:
        return "旺"
    if GENERATES[subject_element] == environment_element:
        return "休"
    if GENERATES[environment_element] == subject_element:
        return "相"
    if CONTROLS[subject_element] == environment_element:
        return "囚"
    return "死"


def fire_stage(position: str) -> str | None:
    """Return the confirmed fire twelve-stage label for a branch point.

    Four trigram points (艮、巽、坤、乾) have no branch-stage lookup and return
    None. The confirmed canonical form is 帝旺; 帝王 is recorded separately
    as a textual variant in the source notes.
    """
    if position not in _RING_INDEX:
        raise ValueError(f"unknown 16-ring position: {position!r}")
    return FIRE_TWELVE_STAGES.get(position)

