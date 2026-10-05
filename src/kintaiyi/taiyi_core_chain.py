"""G4→G5→G6→G7 太乙核心主客链。

输入：
- 太岁支；
- 阴/阳遁；
- 太乙宫；
- 文昌位置。

输出：
- 计神；
- 始击；
- 主算/客算；
- 主/客大将与参将；
- 杜塞状态。

本层只串接已独立校定的G4/G5/G6/G7，不重新实现各自公式。
"""

from __future__ import annotations

from typing import Any

from .taiyi_calculations import host_guest_calculations
from .taiyi_generals import host_guest_generals
from .taiyi_jishen_shiji import shiji_from_taisui_wenchang
from .taiyi_wenchang import wenchang_from_ju
from .taiyi_position import taiyi_from_ju
from .taiyi_taisui import year_entry_from_accumulated_year
from .taiyi_epoch import epoch_context
from .taiyi_four_counts import four_count_core_from_entry_count


CORE_CHAIN_ID = "CORE-G4-G7-CHAIN"


def g4_to_g7_core(
    *,
    taisui_branch: str,
    dun: str,
    taiyi_palace: int,
    wenchang: Any,
) -> dict[str, Any]:
    eyes = shiji_from_taisui_wenchang(
        taisui_branch=taisui_branch,
        dun=dun,
        wenchang=wenchang,
    )
    shiji = eyes["shiji_sector"]

    calculations = host_guest_calculations(
        taiyi_palace=taiyi_palace,
        wenchang=wenchang,
        shiji=shiji,
    )

    generals = host_guest_generals(
        calculations["host_calc"],
        calculations["guest_calc"],
    )

    return {
        "rule_id": CORE_CHAIN_ID,
        "source_profile": "cross_layer_g4_g5_g6_g7",
        "taisui_branch": taisui_branch,
        "dun": eyes["g4"]["dun"],
        "taiyi_palace": taiyi_palace,
        "wenchang": wenchang,
        "jishen_sector": eyes["jishen_sector"],
        "shiji_sector": eyes["shiji_sector"],
        "shiji_god": eyes["shiji_god"],
        "host_calc": calculations["host_calc"],
        "guest_calc": calculations["guest_calc"],
        "host_big_general_palace": generals["host"]["big_general_palace"],
        "host_assistant_general_palace": generals["host"]["assistant_general_palace"],
        "guest_big_general_palace": generals["guest"]["big_general_palace"],
        "guest_assistant_general_palace": generals["guest"]["assistant_general_palace"],
        "host_blocked": generals["host"]["blocked"],
        "guest_blocked": generals["guest"]["blocked"],
        "any_blocked": generals["any_blocked"],
        "stages": {
            "g4_g5": eyes,
            "g6": calculations,
            "g7": generals,
        },
        "policy": (
            "各层只消费上游结构化事实；G5不查sf_list，G6不查find_cal，"
            "G7不重算主客算。"
        ),
    }


def g4_to_g7_from_ju(
    *,
    ju: int,
    dun: str,
    taiyi_palace: int,
    wenchang: Any,
) -> dict[str, Any]:
    """72局回归辅助：局号只恢复太岁支，不作为核心公式来源。"""
    from .taiyi_rules import BRANCHES

    if isinstance(ju, bool) or not isinstance(ju, int) or not 1 <= ju <= 72:
        raise ValueError("ju须为1..72整数")
    taisui_branch = BRANCHES[(ju - 1) % 12]
    result = g4_to_g7_core(
        taisui_branch=taisui_branch,
        dun=dun,
        taiyi_palace=taiyi_palace,
        wenchang=wenchang,
    )
    return {
        **result,
        "ju": ju,
        "helper_status": "regression_only",
    }



def g3_to_g7_from_ju(
    *,
    ju: int,
    dun: str,
    taisui_branch: str,
    taiyi_palace: int,
) -> dict[str, Any]:
    """局号自动生文昌，再串G4→G7。"""
    g3 = wenchang_from_ju(ju, dun=dun)
    core = g4_to_g7_core(
        taisui_branch=taisui_branch,
        dun=dun,
        taiyi_palace=taiyi_palace,
        wenchang=g3["wenchang_sector"],
    )
    return {
        **core,
        "rule_id": "CORE-G3-G7-CHAIN",
        "ju": ju,
        "wenchang_sector": g3["wenchang_sector"],
        "wenchang_god": g3["wenchang_god"],
        "stages": {
            "g3": g3,
            **core["stages"],
        },
        "policy": (
            "局号只用于G3十八周法；G4仍消费显式太岁支。"
            "不得从局号暗推太岁支进入正式业务接口。"
        ),
    }



def g2_to_g7_from_ju(
    *,
    ju: int,
    dun: str,
    taisui_branch: str,
) -> dict[str, Any]:
    """局号自动生成太乙与文昌，再串G4→G7。"""
    g2 = taiyi_from_ju(ju, dun=dun)
    g3 = wenchang_from_ju(ju, dun=dun)
    core = g4_to_g7_core(
        taisui_branch=taisui_branch,
        dun=dun,
        taiyi_palace=g2["taiyi_palace"],
        wenchang=g3["wenchang_sector"],
    )
    return {
        **core,
        "rule_id": "CORE-G2-G7-CHAIN",
        "ju": ju,
        "taiyi_palace": g2["taiyi_palace"],
        "wenchang_sector": g3["wenchang_sector"],
        "wenchang_god": g3["wenchang_god"],
        "stages": {
            "g2": g2,
            "g3": g3,
            **core["stages"],
        },
        "policy": (
            "局号只负责G2/G3入局积数；G4仍显式消费太岁支。"
            "这样避免把局号与太岁支的12支关系偷偷混成同一层。"
        ),
    }



def g1_to_g7_from_accumulated_year(
    *,
    accumulated_year: int,
    dun: str,
) -> dict[str, Any]:
    """低层阴阳局研究入口：积年 -> G1→G7。

    source-specific岁计不应由调用方任选dun；
    正式岁计请使用 year_count_from_accumulated_year()。
    """
    g1 = year_entry_from_accumulated_year(accumulated_year)
    core = g2_to_g7_from_ju(
        ju=g1["local_ju"],
        dun=dun,
        taisui_branch=g1["taisui_branch"],
    )
    return {
        **core,
        "rule_id": "CORE-G1-G7-CHAIN",
        "accumulated_year": accumulated_year,
        "taisui_ganzhi": g1["taisui_ganzhi"],
        "taisui_branch": g1["taisui_branch"],
        "five_yuan": g1["five_yuan"],
        "five_yuan_index_1based": g1["five_yuan_index_1based"],
        "local_ju": g1["local_ju"],
        "stages": {
            "g1": g1,
            **core["stages"],
        },
        "policy": (
            "这是显式阴阳局的低层/回归入口；"
            "G2/G3消费local_ju，G4消费taisui_branch。"
            "正式岁计按《统宗》卷一固定阳局，应调用year_count_from_accumulated_year。"
        ),
    }



def l0_to_g7_from_historical_year(
    *,
    historical_year: int,
    dun: str,
) -> dict[str, Any]:
    """低层历史年+显式阴阳局研究入口。

    保留用于阴/阳72局回归与兼容；source-specific岁计请使用
    year_count_from_historical_year()，其固定阳局。
    historical_year仍只是已经解析好的岁计年份编号。
    """
    l0 = epoch_context(historical_year)
    accumulated_year = l0["long_epoch"]["accumulated_year"]
    core = g1_to_g7_from_accumulated_year(
        accumulated_year=accumulated_year,
        dun=dun,
    )
    return {
        **core,
        "rule_id": "CORE-L0-G7-CHAIN",
        "historical_year": historical_year,
        "accumulated_year": accumulated_year,
        "five_zi_short_accumulated_year": (
            l0["five_zi_short_epoch"]["five_zi_accumulated_year"]
        ),
        "six_ji_three_yuan": l0["six_ji_three_yuan"],
        "five_zi_from_long": l0["five_zi_from_long"],
        "five_zi_from_short": l0["five_zi_from_short"],
        "epoch_equivalent_mod_360": l0["equivalent_mod_360"],
        "stages": {
            "l0": l0,
            **core["stages"],
        },
        "policy": (
            "低层显式阴阳局研究入口；卷三五子元短积年只并列做mod360校验。"
            "source-specific岁计固定阳局，使用year_count_from_historical_year。"
        ),
    }



def year_count_from_accumulated_year(*, accumulated_year: int) -> dict[str, Any]:
    """source-specific岁计：积年 -> G1 + 四计阳局G2..G7。

    《统宗》卷一“四计皆同，唯时夏至后用阴局”，
    因此岁计不接受dun参数，固定阳局。
    """
    g1 = year_entry_from_accumulated_year(accumulated_year)
    core = four_count_core_from_entry_count(
        g1["local_ju"],
        count_type="岁计",
    )
    return {
        **core,
        "rule_id": "CORE-YEAR-COUNT-G1-G7",
        "accumulated_year": accumulated_year,
        "taisui_ganzhi": g1["taisui_ganzhi"],
        "taisui_branch": g1["taisui_branch"],
        "five_yuan": g1["five_yuan"],
        "five_yuan_index_1based": g1["five_yuan_index_1based"],
        "local_ju": g1["local_ju"],
        "stages": {
            "g1": g1,
            **core["stages"],
        },
        "policy": (
            "岁计固定阳局；夏至后切阴只属于时计。"
            "本入口故意不提供dun参数。"
        ),
    }


def year_count_from_historical_year(*, historical_year: int) -> dict[str, Any]:
    """历史岁计年份 -> L0 -> source-specific岁计G1..G7。"""
    l0 = epoch_context(historical_year)
    accumulated_year = l0["long_epoch"]["accumulated_year"]
    core = year_count_from_accumulated_year(
        accumulated_year=accumulated_year,
    )
    return {
        **core,
        "rule_id": "CORE-L0-YEAR-COUNT-G7",
        "historical_year": historical_year,
        "five_zi_short_accumulated_year": (
            l0["five_zi_short_epoch"]["five_zi_accumulated_year"]
        ),
        "six_ji_three_yuan": l0["six_ji_three_yuan"],
        "five_zi_from_long": l0["five_zi_from_long"],
        "five_zi_from_short": l0["five_zi_from_short"],
        "epoch_equivalent_mod_360": l0["equivalent_mod_360"],
        "stages": {
            "l0": l0,
            **core["stages"],
        },
        "policy": (
            "这是正式岁计入口：卷一长积年 + 阳局四计核心。"
            "具体公历日期归属哪个历史岁计年份仍属于更上游岁界历法层。"
        ),
    }
