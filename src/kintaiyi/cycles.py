"""R-WF/R-DY：以0基 accumulated_year 输入；第几年在输出层+1。"""

from .taiyi_rules import GOD_POSITION, integer

WUFU_PATH = (1, 3, 9, 7, 5)
DAYOU_PATH = (7, 8, 9, 1, 2, 3, 4, 6)
DAYOU_TAOJIN_PATH = (7, 6, 4, 3, 2, 1, 9, 8)
DAYOU_TM_PATH = tuple("天道 大武 大武 武德 太簇 阴主 阴德 阴德 大义 地主 阳德 和德 吕申 高丛 太阳 大炅 大神 大威".split())
NUMBER_SUBJECTS = ("士卒", "君王", "王侯臣宰", "后妃", "太子", "民庶", "师帅", "上将军", "中将军", "下将军")
WUFU_PROFILES = {"project": {"offset": 250, "source": "项目canonical"},
                 "source_115": {"offset": 115, "source": "文献+115，仅source profile"}}
DAYOU_PROFILES = {
    "jinjing_tongzong": {"path": DAYOU_PATH, "offset": 34, "source": "金镜/统宗宫序；统宗/象数论宫盈差"},
    "taojin": {"path": DAYOU_TAOJIN_PATH, "offset": None, "source": "淘金歌宫序；历元盈差未确认"}}
TM_PROFILES = {"tongzong": {"offset": 214, "core_cycle": 18, "outer_cycle": 180, "source": "统宗/象数论"},
               "jinjing": {"offset": None, "core_cycle": 18, "yuan": 72, "source": "金镜元法72/周法18；历元盈差未确认"}}


def _number_subject(year_number, maximum):
    integer(year_number, 1, maximum)
    return NUMBER_SUBJECTS[year_number % 10]


def wufu_gb(year_in_palace):
    """吉算是入宫第几年；没有主算参数。"""
    return _number_subject(year_in_palace, 45)


def wufu(accumulated_year, *, profile="project"):
    integer(accumulated_year)
    spec = WUFU_PROFILES[profile]
    index = (accumulated_year + spec["offset"]) % 225
    year = index % 45 + 1
    return {"rule_id": "R-WF", "canonical": "taiyi-t7-d8-v1", "profile": profile,
            "source": spec["source"], "offset": spec["offset"], "cycle_index": index,
            "palace": WUFU_PATH[index // 45], "year_in_palace": year,
            "realm": ("理天", "理地", "理人")[(year - 1) // 15], "auspicious_subject": wufu_gb(year)}


def dayou_xiong(year_in_palace):
    return _number_subject(year_in_palace, 36)


def bigyo(accumulated_year, *, profile="jinjing_tongzong", epoch_offset=None):
    integer(accumulated_year)
    spec = DAYOU_PROFILES[profile]
    offset = spec["offset"] if epoch_offset is None else integer(epoch_offset)
    if offset is None:
        return {"rule_id": "R-DY", "profile": profile, "status": "not_computable", "pending": ["该profile历元盈差未确认；须显式提供epoch_offset"]}
    index = (accumulated_year + offset) % 288
    year = index % 36 + 1
    return {"rule_id": "R-DY", "canonical": "taiyi-t7-d8-v1", "profile": profile,
            "source": spec["source"], "offset": offset, "cycle_index": index,
            "palace": spec["path"][index // 36], "year_in_palace": year,
            "realm": ("治天", "治地", "治人")[(year - 1) // 12], "inauspicious_subject": dayou_xiong(year)}


def bigyo_tianmu(accumulated_year, *, profile="tongzong", epoch_offset=None):
    integer(accumulated_year)
    spec = TM_PROFILES[profile]
    offset = spec["offset"] if epoch_offset is None else integer(epoch_offset)
    if offset is None:
        return {"rule_id": "R-DY-TM", "profile": profile, "status": "not_computable", "pending": ["金镜历元盈差待校；须显式提供epoch_offset"]}
    index = (accumulated_year + offset) % 18
    god = DAYOU_TM_PATH[index]
    return {"rule_id": "R-DY-TM", "profile": profile, "source": spec["source"],
            "offset": offset, "cycle_index": index, "step_number": index + 1,
            "god": god, "position": GOD_POSITION[god], "profile_metadata": dict(spec)}
