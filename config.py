"""旧函数名兼容入口。目标仓库此前没有config.py，返回结构详见文档。

七术新增必需输入未提供时返回not_computable或missing；不伪造盘面。
"""
from kintaiyi.seven_methods import lijin, lion, cloud, tiger, leigong, dragon, returnarmy
from kintaiyi.eight_divinations import (
    cal_des, calc_length, calc_preparedness, wuyin_from_calc, gudan_state,
    gudan, gudan_zhanlue, neiwai_gongji, suenwl, tui_danger)
from kintaiyi.taiyi_rules import SIXTEEN_GOD_WX as _SIXTEEN_GOD_WX
from kintaiyi.cycles import (wufu, wufu_gb, bigyo, bigyo_tianmu, dayou_xiong,
    DAYOU_PATH as _DAYOU_BAGUA, DAYOU_TM_PATH as _DAYOU_TM_PATH,
    NUMBER_SUBJECTS as _DAYOU_XIONG)


def _calc_jianbei(n):
    """兼容旧名，两个结果显式分层。"""
    return {"length": calc_length(n), "preparedness": calc_preparedness(n)}


def junshi_zhanlue(home_cal, away_cal=None):
    """数有所主只调用所主规则。"""
    return {"數有所主": {"主": calc_preparedness(home_cal),
            **({"客": calc_preparedness(away_cal)} if away_cal is not None else {})}}
