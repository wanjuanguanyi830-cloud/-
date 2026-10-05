"""Legacy 0-based cycle compatibility adapters.

C97 后：
- 五福旧 project +250 只保留 quarantine compatibility；
- source_115 显式委托 C67 tongzong；
- jinjing 显式委托 C67 jinjing；
- 五福吉算委托 C68；
- C98：大游旧混合profile撤销 canonical 身份；
- C106：大游天目金镜/统宗显式委托 source-specific runtime；
- C107：大游太乙所在宫金镜/统宗显式委托 source-specific runtime；
- 数值兼容可保留，但来源混合/自定义offset不得升格。

本模块只做 legacy 0基 API 适配，不是五福/大游/大游天目的公式真源。
"""

from .taiyi_rules import GOD_POSITION, integer
from .wufu_source_profiles import wufu_position as _c67_wufu_position
from .wufu_auspicious_numbers import wufu_auspicious_beneficiary as _c68_wufu_beneficiary
from .dayou_tianmu_source_profiles import dayou_tianmu_position as _c106_dayou_tianmu_position
from .dayou_position_source_profiles import dayou_position as _c107_dayou_position

WUFU_PATH = (1, 3, 9, 7, 5)
DAYOU_PATH = (7, 8, 9, 1, 2, 3, 4, 6)
DAYOU_TAOJIN_PATH = (7, 6, 4, 3, 2, 1, 9, 8)
DAYOU_TM_PATH = tuple("天道 大武 大武 武德 太簇 阴主 阴德 阴德 大义 地主 阳德 和德 吕申 高丛 太阳 大炅 大神 大威".split())
NUMBER_SUBJECTS = ("士卒", "君王", "王侯臣宰", "后妃", "太子", "民庶", "师帅", "上将军", "中将军", "下将军")
WUFU_PROFILES = {
    "project": {
        "offset": 250,
        "source": "legacy project compatibility",
        "status": "quarantined_noncanonical",
        "replacement": "C67 explicit source profile",
    },
    "source_115": {
        "offset": 115,
        "source": "C67 tongzong adapter",
        "status": "delegated_canonical_source_profile",
        "replacement": "C67-WUFU-TONGZONG",
    },
    "jinjing": {
        "offset": 0,
        "source": "C67 jinjing adapter",
        "status": "delegated_canonical_source_profile",
        "replacement": "C67-WUFU-JINJING",
    },
}
DAYOU_PROFILES = {
    "jinjing_tongzong": {
        "path": DAYOU_PATH,
        "offset": 34,
        "source": "legacy mixed 金镜/统宗 compatibility",
        "status": "quarantined_mixed_source_profile",
        "canonical_equivalent": False,
    },
    "jinjing": {
        "path": DAYOU_PATH,
        "offset": 0,
        "outer_cycle": 4320,
        "small_cycle": 288,
        "source": "C107 jinjing source profile",
        "status": "delegated_canonical_source_profile",
        "canonical_equivalent": True,
        "replacement": "C107-DAYOU-JINJING",
    },
    "tongzong": {
        "path": DAYOU_PATH,
        "offset": 34,
        "outer_cycle": 2880,
        "small_cycle": 288,
        "source": "C107 tongzong source profile",
        "status": "delegated_canonical_source_profile",
        "canonical_equivalent": True,
        "replacement": "C107-DAYOU-TONGZONG",
    },
    "taojin": {
        "path": DAYOU_TAOJIN_PATH,
        "offset": None,
        "source": "淘金歌宫序；历元盈差未确认",
        "status": "source_variant_epoch_pending",
        "canonical_equivalent": False,
    },
}
TM_PROFILES = {
    "tongzong": {
        "offset": 214,
        "core_cycle": 18,
        "outer_cycle": 180,
        "source": "C106 tongzong source profile",
        "status": "delegated_canonical_source_profile",
        "canonical_equivalent": True,
        "replacement": "C106-DAYOU-TIANMU-TONGZONG",
    },
    "jinjing": {
        "offset": 0,
        "core_cycle": 18,
        "yuan": 72,
        "outer_cycle": 72,
        "source": "C106 jinjing source profile",
        "status": "delegated_canonical_source_profile",
        "canonical_equivalent": True,
        "replacement": "C106-DAYOU-TIANMU-JINJING",
    },
}


def _number_subject(year_number, maximum):
    integer(year_number, 1, maximum)
    return NUMBER_SUBJECTS[year_number % 10]


def wufu_gb(year_in_palace):
    """C97：旧字符串接口委托 C68 显式1..45数表。"""
    return _c68_wufu_beneficiary(year_in_palace)["beneficiary"]


def _wufu_delegated(accumulated_year, source_profile):
    """把旧0基 accumulated_year 转为 C67 的1基 accumulated_count。"""
    count = integer(accumulated_year) + 1
    canonical = _c67_wufu_position(count, source_profile=source_profile)
    palace_by_position = {"乾": 1, "艮": 3, "巽": 9, "坤": 7, "中": 5}
    year = canonical["year_in_palace"]
    return {
        "rule_id": canonical["rule_id"],
        "canonical": canonical["canonical"],
        "profile": "source_115" if source_profile == "tongzong" else "jinjing",
        "source": canonical["source_work"],
        "offset": canonical["surplus"],
        "cycle_index": canonical["effective_count"] - 1,
        "palace": palace_by_position[canonical["position"]],
        "year_in_palace": year,
        # 10月4日旧UI字段保留为兼容派生，不作为 C67 来源事实。
        "realm": ("理天", "理地", "理人")[(year - 1) // 15],
        "realm_status": "legacy_compatibility_derived",
        "auspicious_subject": wufu_gb(year),
        "auspicious_subject_rule": "C68-WUFU-AUSPICIOUS-NUMBER",
        "canonical_delegate": canonical,
        "canonical_equivalent": True,
        "quarantined": False,
    }


def wufu(accumulated_year, *, profile="project"):
    """旧0基五福入口。

    project 保留数值兼容，但明确隔离；
    source_115 / jinjing 委托 C67。
    """
    integer(accumulated_year)
    if profile not in WUFU_PROFILES:
        raise ValueError("未知五福profile")

    if profile == "source_115":
        return _wufu_delegated(accumulated_year, "tongzong")
    if profile == "jinjing":
        return _wufu_delegated(accumulated_year, "jinjing")

    # 历史 project +250：只为旧调用兼容，不能再标 canonical。
    spec = WUFU_PROFILES["project"]
    index = (accumulated_year + spec["offset"]) % 225
    year = index % 45 + 1
    return {
        "rule_id": "LEGACY-WUFU-PROJECT-250",
        "canonical": None,
        "profile": "project",
        "source": spec["source"],
        "offset": spec["offset"],
        "cycle_index": index,
        "palace": WUFU_PATH[index // 45],
        "year_in_palace": year,
        "realm": ("理天", "理地", "理人")[(year - 1) // 15],
        "realm_status": "legacy_compatibility_derived",
        "auspicious_subject": wufu_gb(year),
        "auspicious_subject_rule": "C68-WUFU-AUSPICIOUS-NUMBER",
        "canonical_equivalent": False,
        "quarantined": True,
        "promotion_allowed": False,
        "replacement_rule_ids": ["C67-WUFU-TONGZONG", "C67-WUFU-JINJING"],
        "reason": (
            "旧project +250不属于C67已选统宗+115或金镜无盈差profile；"
            "仅保留0基兼容结果，不得作为统一真源。"
        ),
    }


def dayou_xiong(year_in_palace):
    return _number_subject(year_in_palace, 36)


def _dayou_delegated(accumulated_year, source_profile):
    """把旧0基 accumulated_year 转为 C107 的1基 accumulated_count。"""
    year0 = integer(accumulated_year)
    canonical = _c107_dayou_position(year0 + 1, source_profile=source_profile)
    year = canonical["year_in_palace"]
    return {
        "rule_id": canonical["rule_id"],
        "canonical": canonical["canonical"],
        "profile": source_profile,
        "source": canonical["source_work"],
        "offset": canonical["surplus"],
        "cycle_index": canonical["small_count"] - 1,
        "palace": canonical["palace"],
        "year_in_palace": year,
        "realm": ("治天", "治地", "治人")[(year - 1) // 12],
        "realm_status": "legacy_compatibility_derived",
        "inauspicious_subject": dayou_xiong(year),
        "canonical_delegate": canonical,
        "canonical_equivalent": True,
        "promotion_allowed": True,
        "quarantined": False,
        "profile_metadata": dict(DAYOU_PROFILES[source_profile]),
    }


def bigyo(accumulated_year, *, profile="jinjing_tongzong", epoch_offset=None):
    """旧0基大游入口。

    - jinjing / tongzong：委托 C107；
    - jinjing_tongzong：保留旧混源兼容并 quarantine；
    - taojin：历元未确认，只有显式offset才可兼容试算；
    - 对已知来源profile显式传非来源offset时，仅作 custom compatibility。
    """
    year0 = integer(accumulated_year)
    if profile not in DAYOU_PROFILES:
        raise ValueError("未知大游profile")
    spec = DAYOU_PROFILES[profile]

    if profile in ("jinjing", "tongzong"):
        source_offset = spec["offset"]
        if epoch_offset is None or epoch_offset == source_offset:
            return _dayou_delegated(year0, profile)

        custom_offset = integer(epoch_offset)
        index = (year0 + custom_offset) % 288
        year = index % 36 + 1
        return {
            "rule_id": "LEGACY-DAYOU-CUSTOM-OFFSET",
            "canonical": None,
            "profile": profile,
            "source": "legacy explicit custom epoch_offset",
            "offset": custom_offset,
            "cycle_index": index,
            "palace": spec["path"][index // 36],
            "year_in_palace": year,
            "realm": ("治天", "治地", "治人")[(year - 1) // 12],
            "realm_status": "legacy_compatibility_derived",
            "inauspicious_subject": dayou_xiong(year),
            "canonical_equivalent": False,
            "promotion_allowed": False,
            "quarantined": False,
            "profile_metadata": dict(spec),
            "reason": (
                "调用方显式offset与C107该来源参数不同；"
                "仅作旧接口兼容试算，不覆盖source-specific runtime。"
            ),
        }

    offset = spec["offset"] if epoch_offset is None else integer(epoch_offset)
    if offset is None:
        return {
            "rule_id": "LEGACY-DAYOU-COMPAT",
            "canonical": None,
            "profile": profile,
            "status": "not_computable",
            "pending": ["该profile历元盈差未确认；须显式提供epoch_offset"],
            "canonical_equivalent": False,
            "promotion_allowed": False,
            "quarantined": profile == "jinjing_tongzong",
            "profile_metadata": dict(spec),
        }

    index = (year0 + offset) % 288
    year = index % 36 + 1
    return {
        "rule_id": "LEGACY-DAYOU-COMPAT",
        "canonical": None,
        "profile": profile,
        "source": spec["source"],
        "offset": offset,
        "cycle_index": index,
        "palace": spec["path"][index // 36],
        "year_in_palace": year,
        "realm": ("治天", "治地", "治人")[(year - 1) // 12],
        "inauspicious_subject": dayou_xiong(year),
        "canonical_equivalent": False,
        "promotion_allowed": False,
        "quarantined": profile == "jinjing_tongzong",
        "profile_metadata": dict(spec),
        "reason": (
            "旧jinjing_tongzong把金镜行宫来源与统宗+34混为单一profile；"
            "C107建立后仍只保留兼容数值。"
            if profile == "jinjing_tongzong"
            else "淘金歌路径的历元未确认；显式offset只作兼容试算，不升格。"
        ),
    }


def bigyo_tianmu(accumulated_year, *, profile="tongzong", epoch_offset=None):
    """C106 adapter：旧0基输入 -> C106 1基 source-specific runtime。

    省略 epoch_offset，或显式给出该来源本身的 offset 时，委托 C106。
    只有非来源自定义 offset 才保留 legacy compatibility 试算。
    """
    year0 = integer(accumulated_year)
    if profile not in TM_PROFILES:
        raise ValueError("未知大游天目profile")
    spec = TM_PROFILES[profile]
    source_offset = spec["offset"]

    if epoch_offset is None or epoch_offset == source_offset:
        canonical = _c106_dayou_tianmu_position(
            year0 + 1,
            source_profile=profile,
        )
        return {
            "rule_id": canonical["rule_id"],
            "canonical": canonical["canonical"],
            "profile": profile,
            "source": canonical["source_work"],
            "offset": canonical["surplus"],
            "cycle_index": canonical["step_number"] - 1,
            "step_number": canonical["step_number"],
            "god": canonical["god"],
            "position": canonical["position"],
            "profile_metadata": dict(spec),
            "canonical_delegate": canonical,
            "canonical_equivalent": True,
            "promotion_allowed": True,
            "quarantined": False,
        }

    custom_offset = integer(epoch_offset)
    index = (year0 + custom_offset) % 18
    god = DAYOU_TM_PATH[index]
    return {
        "rule_id": "LEGACY-DAYOU-TIANMU-CUSTOM-OFFSET",
        "canonical": None,
        "profile": profile,
        "source": "legacy explicit custom epoch_offset",
        "offset": custom_offset,
        "cycle_index": index,
        "step_number": index + 1,
        "god": god,
        "position": GOD_POSITION[god],
        "profile_metadata": dict(spec),
        "canonical_equivalent": False,
        "promotion_allowed": False,
        "quarantined": False,
        "reason": (
            "调用方显式offset与C106该来源参数不同；"
            "仅作旧接口兼容试算，不覆盖source-specific runtime。"
        ),
    }

