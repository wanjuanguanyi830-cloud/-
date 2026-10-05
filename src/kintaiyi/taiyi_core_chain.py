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
