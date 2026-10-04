"""Canonical shared rules and explicit coordinate conversions.

The 9-palace, 16-sector, 12-branch, and 12-palace Four Taiyi systems are
separate coordinates. Source variants belong in the rule record, not here.
"""

SIXTEEN = tuple("子 丑 艮 寅 卯 辰 巽 巳 午 未 坤 申 酉 戌 乾 亥".split())
BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
GODS = tuple("地主 阳德 和德 吕申 高丛 太阳 大炅 大神 大威 天道 大武 武德 太簇 阴主 阴德 大义".split())
ELEMENTS = tuple("水 土 土 木 木 土 木 火 火 土 土 金 金 土 金 水".split())
POSITION_WX = dict(zip(SIXTEEN, ELEMENTS))
GOD_POSITION = dict(zip(GODS, SIXTEEN))
GOD_ALIASES = {"太炅": "大炅", "太神": "大神"}
SIXTEEN_GOD_WX = dict(zip(GODS, ELEMENTS))

# Palace id -> trigram and its representative point on the 16-sector ring.
NINE_PALACE_TRIGRAM = {
    1: "乾", 2: "离", 3: "艮", 4: "震", 5: "中",
    6: "兑", 7: "坤", 8: "坎", 9: "巽",
}
PALACE_POINT = {1: "乾", 2: "午", 3: "艮", 4: "卯", 6: "酉", 7: "坤", 8: "子", 9: "巽"}
SECTOR_TO_PALACE = {sector: palace for palace, sector in PALACE_POINT.items()}
PALACE_WX = {1: "金", 2: "火", 3: "土", 4: "木", 5: "土", 6: "金", 7: "土", 8: "水", 9: "木"}
PALACE_YIN_YANG = {1: "阴", 2: "阴", 3: "阳", 4: "阳", 5: None, 6: "阴", 7: "阴", 8: "阳", 9: "阳"}

YANG_PALACES = frozenset((8, 3, 4, 9))
YIN_PALACES = frozenset((2, 7, 6, 1))
GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
FIRE_STAGES = dict(zip(tuple("寅卯辰巳午未申酉戌亥子丑"),
                       "长生 沐浴 冠带 临官 帝旺 衰 病 死 墓 绝 胎 养".split()))
CORNER_SECTORS = {"艮": frozenset("丑艮寅"), "巽": frozenset("辰巽巳"),
                  "坤": frozenset("未坤申"), "乾": frozenset("戌乾亥")}
GENERAL_INTRINSIC_WX = {
    "home_general": "金", "home_assistant": "水",
    "away_general": "水", "away_assistant": "木",
}
GENERAL_NAME_ALIASES = {"home_vassal": "home_assistant", "away_vassal": "away_assistant"}


def integer(value, minimum=0, maximum=None):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("须为整数")
    if value < minimum or (maximum is not None and value > maximum):
        raise ValueError("数值超出范围")
    return value


def nine_palace_to_trigram(palace_id):
    return NINE_PALACE_TRIGRAM[integer(palace_id, 1, 9)]


def nine_palace_representative_sector(palace_id):
    """Return the 16-ring representative sector; center palace 5 has none."""
    return PALACE_POINT.get(integer(palace_id, 1, 9))


def sector_to_nine_palace(sector):
    """Convert only the eight defined representative sectors; other sectors return None."""
    if not isinstance(sector, str) or sector not in SIXTEEN:
        raise ValueError("须为十六辰/十六神所对应的位置")
    return SECTOR_TO_PALACE.get(sector)


def palace_element(palace_id):
    return PALACE_WX[integer(palace_id, 1, 9)]


def position(anchor):
    """Legacy normalizer: 9-palace numbers, sectors, or 16-god names to a sector."""
    if isinstance(anchor, int) and not isinstance(anchor, bool):
        integer(anchor, 1, 9)
        sector = nine_palace_representative_sector(anchor)
        if sector is None:
            raise ValueError("中五无十六宫代表点")
        return sector
    anchor = GOD_ALIASES.get(anchor, anchor)
    anchor = GOD_POSITION.get(anchor, anchor)
    if anchor not in SIXTEEN:
        raise ValueError("须为十六宫位置、十六神或外八宫数")
    return anchor


def dashen_from_sector(sector):
    """R-LS-01: move four places forward on the 16-sector ring."""
    if not isinstance(sector, str) or sector not in SIXTEEN:
        raise ValueError("大神起点须为十六辰位置")
    return SIXTEEN[(SIXTEEN.index(sector) + 4) % 16]


def dashen_from_nine_palace(palace_id):
    """Convert a non-center 9-palace id to its representative sector, then add four."""
    sector = nine_palace_representative_sector(palace_id)
    if sector is None:
        raise ValueError("中五无十六辰对应")
    return dashen_from_sector(sector)


def dashen_from_lushen(anchor):
    """Compatibility wrapper for the former mixed-coordinate entry point."""
    if isinstance(anchor, int) and not isinstance(anchor, bool):
        return dashen_from_nine_palace(anchor)
    return dashen_from_sector(position(anchor))


def qi_relation(subject, environment):
    """Five-state relation: 旺、相、死、囚、休; subject is the first argument."""
    if subject not in GENERATES or environment not in GENERATES:
        raise ValueError("须为木火土金水")
    if subject == environment:
        return "旺"
    if GENERATES[environment] == subject:
        return "相"
    if CONTROLS[environment] == subject:
        return "死"
    if CONTROLS[subject] == environment:
        return "囚"
    return "休"


def qi_state(subject, environment):
    """Legacy name; use qi_relation in new code."""
    return qi_relation(subject, environment)


def wuxing_relation_2(subject, environment):
    """Legacy compatibility spelling; the first argument remains the subject."""
    return qi_relation(subject, environment)


def _dashen_result(landing):
    nine_palace = sector_to_nine_palace(landing)
    return {
        "position": landing,
        "sector": landing,
        "sector_element": POSITION_WX[landing],
        "element": POSITION_WX[landing],
        "nine_palace": nine_palace,
        "palace": nine_palace,
        "nine_palace_element": palace_element(nine_palace) if nine_palace is not None else None,
        "state": qi_relation("火", POSITION_WX[landing]),
        "stage": FIRE_STAGES.get(landing),
        "model": "A",
    }


def dashen_qi_from_sector(sector):
    """Mode A result from an explicitly typed 16-sector coordinate."""
    return _dashen_result(dashen_from_sector(sector))


def dashen_qi_from_nine_palace(palace_id):
    """Mode A result from an explicitly typed 9-palace coordinate."""
    return _dashen_result(dashen_from_nine_palace(palace_id))


def dashen_qi(anchor):
    """Legacy mixed-coordinate wrapper; new rules use the typed helpers above."""
    return _dashen_result(dashen_from_lushen(anchor))


def calc_components(n):
    """R-CAL-01: 人 is an odd remainder within each five-count group."""
    integer(n, 1, 40)
    unit = n % 10
    return {"ten": n >= 10, "five": unit >= 5, "one": unit % 5 != 0}


def sexagenary_year(value):
    if value in BRANCHES:
        return None, value
    if not isinstance(value, str) or len(value) != 2 or value[0] not in STEMS or value[1] not in BRANCHES:
        raise ValueError("须为年支或有效干支年")
    cycle = [STEMS[i % 10] + BRANCHES[i % 12] for i in range(60)]
    if value not in cycle:
        raise ValueError("无效干支配对")
    return cycle.index(value), value[1]


def result(rule_id, **fields):
    category = ("seven_methods" if rule_id.startswith("T7") else
                "eight_divinations" if rule_id.startswith("D8") else
                "cycles" if rule_id in {"R-3B", "R-WF", "R-DY", "R-DY-TM", "R-SY", "R-4T"}
                else "shared_rules")
    return {"rule_id": rule_id,
            "category": category,
            "canonical": "taiyi-t7-d8-v2",
            "computable": True,
            **fields}


# Corrected legacy constants and conversion name. _WX_REL is intentionally
# absent: all callers must use the algorithmic qi_relation function.
_GENERAL_WX = GENERAL_INTRINSIC_WX
num2gong = nine_palace_representative_sector


def not_computable(rule_id, missing_inputs=(), reason=None, **fields):
    missing = list(missing_inputs)
    return result(rule_id, computable=False, status="not_computable",
                  missing_inputs=missing, missing=missing, reason=reason, **fields)
