"""Legacy display facade. All corrected rules delegate to pure canonical cores."""
from kintaiyi import cycles as _old_cycles
from kintaiyi import eight_divinations as _d8
from kintaiyi import seven_methods as _t7
from kintaiyi import taiyi_common as _common
from kintaiyi import taiyi_cycles as _cycles
from kintaiyi.junshi_zhanlue import junshi_zhanlue as _junshi_zhanlue_c8

lijin = _t7.lijin
lion = _t7.lion
cloud = _t7.cloud
tiger = _t7.tiger
leigong = _t7.leigong
dragon = _t7.dragon
returnarmy = _t7.returnarmy
calc_length = _d8.calc_length
calc_preparedness = _d8.calc_preparedness
wuyin_from_calc = _d8.wuyin_from_calc
gudan_state = _d8.gudan_analysis
gudan = _d8.gudan_analysis
gudan_zhanlue = _d8.gudan_analysis
tui_danger = _d8.yinyang_adversity
_SIXTEEN_GOD_WX = _common.SIXTEEN_GOD_ELEMENTS
_GENERAL_WX = {**_common.GENERAL_ELEMENTS, "始擊": _common.GENERAL_ELEMENTS["始击"],
               "主將": _common.ROLE_ELEMENTS["home_general"], "主參": _common.ROLE_ELEMENTS["home_assistant"],
               "客將": _common.ROLE_ELEMENTS["away_general"], "客參": _common.ROLE_ELEMENTS["away_assistant"],
               "主将": _common.ROLE_ELEMENTS["home_general"], "主参": _common.ROLE_ELEMENTS["home_assistant"],
               "天乙": "金", "地乙": "土", "直符": "火", "四神": "水"}
_WX_REL = {(subject, environment): _common.qi_relation(subject, environment)["state"]
           for subject in _common.GENERATES for environment in _common.GENERATES}
_DAYOU_BAGUA = _cycles.DAYOU_PATH
_DAYOU_TM_PATH = _cycles.DAYOU_TM_PATH
_DAYOU_XIONG = _cycles.NUMBER_SUBJECTS
wufu_gb = _old_cycles.wufu_gb
dayou_xiong = _old_cycles.dayou_xiong


def cal_des(home_cal, away_cal=None, set_cal=None):
    """Old display list; only D8-01 classic tags, not length or preparedness."""
    if away_cal is None and set_cal is None:
        return list(_d8.sancai_analysis(home_cal)["classic_tags"])
    return {name: list(_d8.sancai_analysis(n)["classic_tags"]) for name, n in
            (("home", home_cal), ("away", away_cal), ("set", set_cal)) if n is not None}


def _calc_jianbei(n):
    """D8-08 legacy adapter. Length is available separately as calc_length."""
    return {"preparedness": _d8.calc_preparedness(n)}


def suenwl(home, away, home_general=None, away_general=None, *, pattern_corrections=None):
    return _d8.suenwl(home, away, pattern_corrections=pattern_corrections)


def neiwai_gongji(ty, skyeyes=None):
    # One-argument target API and two-argument reference UI are both accepted.
    data = _d8.attack_realm(ty if skyeyes is None else skyeyes)
    traditional = {"内": "內", "外": "外"}
    return {**data, "天目內外": traditional[data["realm"]],
            "孤虛": "內虛" if data["realm"] == "内" else "外孤",
            "宜攻": traditional[data["attack"]], "斷語": data["verdict"]}


def wufu(accumulated_year, *, profile="project"):
    return _cycles.five_blessings(accumulated_year, profile="project_canonical" if profile == "project" else profile)


def bigyo(accumulated_year, *, profile="jinjing_tongzong", epoch_offset=None):
    return _cycles.big_wander(accumulated_year, profile="tongzong" if profile == "jinjing_tongzong" else profile,
                              epoch_offset=epoch_offset)


def smyo(accumulated_year):
    return _cycles.small_wander(accumulated_year)["palace_id"]


def bigyo_tianmu(accumulated_year, *, profile="tongzong", epoch_offset=None):
    return _cycles.big_wander_skyeyes(accumulated_year, profile=profile, epoch_offset=epoch_offset)


def junshi_zhanlue(home_cal, away_cal=None, *, taiyi=None, skyeyes=None,
                    three_doors=None, five_generals=None,
                    home_general_state=None, away_general_state=None,
                    home_general_palace=None, away_general_palace=None):
    """旧入口兼容层；canonical 结果由 C8 组合层提供。"""
    data = _junshi_zhanlue_c8(
        home_cal=home_cal,
        away_cal=away_cal,
        taiyi=taiyi,
        skyeyes=skyeyes,
        three_doors=three_doors,
        five_generals=five_generals,
        home_general_state=home_general_state,
        away_general_state=away_general_state,
        home_general_palace=home_general_palace,
        away_general_palace=away_general_palace,
    )
    legacy = data["legacy_projection"]
    # 保留旧繁体键；值仍来自 D8-08，不另算。
    data["數有所主"] = {
        "主": legacy["数有所主"]["主算"],
        **({"客": legacy["数有所主"]["客算"]} if away_cal is not None else {}),
    }
    data["五音"] = {
        "主": legacy["五音"]["主算"],
        **({"客": legacy["五音"]["客算"]} if away_cal is not None else {}),
    }
    return data
