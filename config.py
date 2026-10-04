"""旧函数名兼容入口。目标仓库此前没有config.py，返回结构详见文档。

七术新增必需输入未提供时返回not_computable或missing；不伪造盘面。
"""
from kintaiyi.seven_methods import lijin, lion, cloud, tiger, leigong, dragon, returnarmy
from kintaiyi.eight_divinations import (
    cal_des, calc_length, calc_preparedness, wuyin_from_calc, gudan_state,
    gudan, gudan_zhanlue, neiwai_gongji, suenwl, tui_danger)
from kintaiyi.taiyi_rules import SIXTEEN_GOD_WX as _SIXTEEN_GOD_WX
from kintaiyi.junshi_zhanlue import junshi_zhanlue as _junshi_zhanlue_c8
from kintaiyi.cycles import (wufu, wufu_gb, bigyo, bigyo_tianmu, dayou_xiong,
    DAYOU_PATH as _DAYOU_BAGUA, DAYOU_TM_PATH as _DAYOU_TM_PATH,
    NUMBER_SUBJECTS as _DAYOU_XIONG)


def _calc_jianbei(n):
    """兼容旧名，两个结果显式分层。"""
    return {"length": calc_length(n), "preparedness": calc_preparedness(n)}


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
