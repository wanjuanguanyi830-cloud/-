"""旧函数名兼容入口。目标仓库此前没有config.py，返回结构详见文档。

七术新增必需输入未提供时返回not_computable或missing；不伪造盘面。
"""
from kintaiyi.seven_methods import lijin, lion, cloud, tiger, leigong, dragon, returnarmy
from kintaiyi.eight_divinations import (
    cal_des, calc_length, calc_preparedness, wuyin_from_calc, gudan_state,
    gudan, gudan_zhanlue, neiwai_gongji, suenwl, tui_danger)
from kintaiyi.taiyi_rules import SIXTEEN_GOD_WX as _SIXTEEN_GOD_WX
from kintaiyi.taiyi_rules import (
    dashen_from_sector, dashen_from_nine_palace, qi_relation,
    sector_to_nine_palace, nine_palace_to_trigram,
    nine_palace_representative_sector,
    GENERAL_INTRINSIC_WX as _GENERAL_WX,
    num2gong, wuxing_relation_2,
)
from kintaiyi.junshi_zhanlue import junshi_zhanlue as _junshi_zhanlue_c8
from kintaiyi.cycles import (wufu, wufu_gb, bigyo, bigyo_tianmu, dayou_xiong,
    DAYOU_PATH as _DAYOU_BAGUA, DAYOU_TM_PATH as _DAYOU_TM_PATH,
    NUMBER_SUBJECTS as _DAYOU_XIONG, three_bases, kingbase, officerbase,
    pplbase, smyo, small_wander, four_taiyi, four_taiyi_cycle,
    four_taiyi_central_matrix, four_god_water_conflict, xiaoyou_suozhu,
    wufu_interaction)
from kintaiyi.pan_v2 import pan, build_pan_v2


def _calc_jianbei(n):
    """兼容旧名，两个结果显式分层。"""
    return {"length": calc_length(n), "preparedness": calc_preparedness(n)}


def junshi_zhanlue(home_cal, away_cal=None, *, taiyi=None, skyeyes=None,
                    three_doors=None, five_generals=None,
                    home_general_state=None, away_general_state=None,
                    home_general_palace=None, away_general_palace=None):
    """旧入口兼容层；综合 canonical 由 C8 提供，数有所主来自 D8-08。"""
    data = _junshi_zhanlue_c8(
        home_cal=home_cal, away_cal=away_cal, taiyi=taiyi, skyeyes=skyeyes,
        three_doors=three_doors, five_generals=five_generals,
        home_general_state=home_general_state, away_general_state=away_general_state,
        home_general_palace=home_general_palace, away_general_palace=away_general_palace,
    )
    legacy = data["legacy_projection"]
    data["數有所主"] = {
        "主": legacy["数有所主"]["主算"],
        **({"客": legacy["数有所主"]["客算"]} if away_cal is not None else {}),
    }
    data["五音"] = {
        "主": legacy["五音"]["主算"],
        **({"客": legacy["五音"]["客算"]} if away_cal is not None else {}),
    }
    return data

