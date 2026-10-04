"""Legacy zero-based cycle APIs; all arithmetic lives in taiyi_cycles.

These existing APIs accept an elapsed-year index starting at zero. New callers
must use the one-based taiyi_cycles APIs. The explicit +1 is an input adapter.
"""
from . import taiyi_cycles as _c
from .taiyi_common import integer

WUFU_PATH = _c.WUFU_PATH
DAYOU_PATH = _c.DAYOU_PATH
DAYOU_TAOJIN_PATH = _c.DAYOU_TAOJIN_PATH
DAYOU_TM_PATH = _c.DAYOU_TM_PATH
NUMBER_SUBJECTS = _c.NUMBER_SUBJECTS
WUFU_PROFILES = {"project": {"offset": 250, "source": "项目canonical"},
                 "source_115": {"offset": 115, "source": "source_variant"}}
DAYOU_PROFILES = {"jinjing_tongzong": {"path": DAYOU_PATH, "offset": 34, "source": "统宗/象数论"},
                  "taojin": {"path": DAYOU_TAOJIN_PATH, "offset": None, "source": "淘金歌异文"}}
TM_PROFILES = {"tongzong": {"offset": 214, "core_cycle": 18, "outer_cycle": 180, "source": "统宗/象数论"},
               "jinjing": {"offset": 0, "core_cycle": 18, "yuan": 72, "source": "金镜"}}


def _project(data):
    out = {**data, "canonical": "taiyi-t7-d8-v1", "input_basis": "legacy_zero_based"}
    if data["computable"]:
        out["cycle_index"] = data["cycle_year"] - 1
        if "phase" in data:
            out["realm"] = data["phase"]
    else:
        out["pending"] = [data["reason"]]
    return out


def wufu_gb(year_in_palace):
    return _c.five_blessings_lucky_calc(year_in_palace)["subject"]


def wufu(accumulated_year, *, profile="project"):
    integer(accumulated_year)
    return _project(_c.five_blessings(accumulated_year + 1, profile="project_canonical" if profile == "project" else profile))


def dayou_xiong(year_in_palace):
    return _c.number_subject(year_in_palace, 36)["subject"]


def bigyo(accumulated_year, *, profile="jinjing_tongzong", epoch_offset=None):
    integer(accumulated_year)
    return _project(_c.big_wander(accumulated_year + 1,
                    profile="tongzong" if profile == "jinjing_tongzong" else profile,
                    epoch_offset=epoch_offset))


def bigyo_tianmu(accumulated_year, *, profile="tongzong", epoch_offset=None):
    integer(accumulated_year)
    data = _c.big_wander_skyeyes(accumulated_year + 1, profile=profile, epoch_offset=epoch_offset)
    return {**_project(data), "profile_metadata": dict(TM_PROFILES[profile])}
