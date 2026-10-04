"""Eight war divinations, v1, with shared arithmetic and explicit source limits."""

from __future__ import annotations

from ..common.taiyi_space import GOD_POSITION, INNER_GODS, OUTER_GODS

RULESET_ID = "taiyi-war-eight-v1"
RULESET_VERSION = "1.0.0"

WUYIN = {
    1: ("宮", "正音", "土", "人君"),
    2: ("宮", "比宮", "土", "人君"),
    3: ("徵", "正音", "火", "宗廟"),
    4: ("徵", "比徵", "火", "宗廟"),
    5: ("羽", "正音", "水", "后妃"),
    6: ("羽", "比羽", "水", "后妃"),
    7: ("商", "正音", "金", "子孫"),
    8: ("商", "比商", "金", "子孫"),
    9: ("角", "正音", "木", "疾病"),
    10: ("角", "比角", "木", "疾病"),
}
CLASSIC_THREE_TALENT_EXAMPLES = frozenset(
    (*range(16, 20), *range(26, 30), *range(36, 40))
)
PALACE_YINYANG = {
    8: "陽", 3: "陽", 4: "陽", 9: "陽",
    2: "陰", 7: "陰", 6: "陰", 1: "陰",
}


def _positive_integer(n: int, name: str = "算") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be an integer")
    if n <= 0:
        raise ValueError(f"{name} must be positive")
    return n


def calc_components(n: int) -> dict[str, bool]:
    """Shared ten/five/one split for 三才 and 所主.

    “五” is present when the units digit is at least five; “一” is present
    whenever the units digit is non-zero. It is not a separate decimal digit.
    """
    n = _positive_integer(n)
    unit = n % 10
    return {"有十": n >= 10, "有五": unit >= 5, "有一": unit != 0}


def three_talent(n: int) -> dict:
    parts = calc_components(n)
    absent = [name for name, present in (("天", parts["有十"]), ("地", parts["有五"]), ("人", parts["有一"])) if not present]
    disaster = {"天": "天象", "地": "地變", "人": "人事"}
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "算": n, "天": parts["有十"], "地": parts["有五"], "人": parts["有一"],
        "狀態": [f"無{name}" for name in absent],
        "災象": [disaster[name] for name in absent],
        "典型古法三才足數": n in CLASSIC_THREE_TALENT_EXAMPLES,
    }


def calc_length(n: int) -> str:
    """D8-02: 11 and above is long; 1 through 10 is short."""
    return "長" if _positive_integer(n) >= 11 else "短"


def wuyin_from_calc(n: int) -> dict:
    n = _positive_integer(n)
    tail = n % 10 or 10
    tone, quality, element, governs = WUYIN[tail]
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "算": n, "算尾": tail, "五音": tone,
        "正比": quality, "五行": element, "所主": governs,
    }


def gudan_state(n: int) -> dict:
    n = _positive_integer(n)
    unit = n % 10
    tens = n // 10
    single = "單陽" if unit in (1, 3, 7, 9) else "單陰" if unit in (2, 4, 6, 8) else None
    isolated = "孤陽" if tens in (1, 3) else "孤陰" if tens in (2, 4) else None
    combined = None
    if single and isolated == "孤陽" and single == "單陽":
        combined = "重陽"
    elif single and isolated == "孤陰" and single == "單陰":
        combined = "重陰"
    if combined:
        result, disfavor, calamity = combined, ("主" if combined == "重陽" else "客"), ("火" if combined == "重陽" else "水")
    elif isolated:
        result, disfavor, calamity = isolated, ("主" if isolated == "孤陽" else "客"), None
    elif single:
        result, disfavor, calamity = single, ("主" if single == "單陽" else "客"), None
    else:
        result, disfavor, calamity = None, None, None
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "算": n, "單": single, "孤": isolated, "合成": combined,
        "狀態": result, "不利方": disfavor, "厄類": calamity,
    }


def attack_realm(skyeye: str) -> dict:
    """D8-05: fixed inner/outer partition; independent of Taiyi palace."""
    position = GOD_POSITION.get(skyeye)
    if position is None:
        raise ValueError(f"unknown skyeye name: {skyeye!r}")
    if skyeye in INNER_GODS:
        realm = "內"
        target = "外"
    elif skyeye in OUTER_GODS:
        realm = "外"
        target = "內"
    else:
        raise ValueError(f"skyeye has no confirmed inner/outer assignment: {skyeye!r}")
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "天目": skyeye, "位置": position, "天目所在": realm,
        "虛方": realm, "可攻": target,
    }


def compare_calcs(home: int, away: int) -> dict:
    home = _positive_integer(home, "主算")
    away = _positive_integer(away, "客算")
    if away > home:
        result = "客勝勢"
    elif away < home:
        result = "主勝勢"
    else:
        result = "同數"
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "主算": home, "客算": away, "基礎結果": result,
        "古法明文斷語": None if home == away else result,
    }


def yin_yang_disaster(taiyi_palace: int, n: int, side: str) -> dict:
    if isinstance(taiyi_palace, bool) or not isinstance(taiyi_palace, int):
        raise TypeError("taiyi_palace must be an integer")
    if taiyi_palace not in PALACE_YINYANG:
        raise ValueError("taiyi_palace must be one of the eight non-central palaces")
    if side not in ("主", "客"):
        raise ValueError("side must be 主 or 客")
    n = _positive_integer(n)
    palace_yinyang = PALACE_YINYANG[taiyi_palace]
    parity = "奇" if n % 2 else "偶"
    double = (palace_yinyang == "陽" and parity == "奇") or (palace_yinyang == "陰" and parity == "偶")
    state = "重陽" if double and palace_yinyang == "陽" else "重陰" if double else None
    calamity = "火" if state == "重陽" else "水" if state == "重陰" else None
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "太乙宮": taiyi_palace, "宮陰陽": palace_yinyang,
        "算": n, "算奇偶": parity, "狀態": state,
        "災類": calamity, "應方": side if state else None,
    }


def troop_readiness(n: int) -> dict:
    parts = calc_components(n)
    missing = []
    if not parts["有十"]:
        missing.append("無將軍：主將不利")
    if not parts["有五"]:
        missing.append("無吏士：副佐不利")
    if not parts["有一"]:
        missing.append("無兵卒：士卒不利")
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "算": n, "將軍": parts["有十"], "吏士": parts["有五"],
        "兵卒": parts["有一"], "俱備": all(parts.values()),
        "缺項": missing,
        "斷": "利興兵出師" if all(parts.values()) else None,
    }

