"""三门—五将—出师跨层资格链。

本模块只做 orchestration，不创造新古法：
- J4M-01 / TZ2：三门具不具；
- J4M-02：五将发不发的原典三阻断；
- CORE-WUJIANG-READY：杜塞取“五将不发”；
- J4M-05：算12/22/32、三门具、五将发、开休生出军。

各 source profile 的原始结果完整保留在 stages 中。
"""

from __future__ import annotations

from typing import Any

from .jinjing_v4_military import (
    chushi_fa,
    effective_five_generals_readiness,
    sanmen_jubu_from_period_count,
    wujiang_fabu,
    zhimen_from_cycle_count,
)
from .tongzong_v2_doors import taiyi_door_readiness

PIPELINE_VERSION = "taiyi-military-readiness-pipeline-v1"
BLOCKED_CALCS = frozenset({5, 15, 25, 35})


def _three_doors(
    *,
    profile: str,
    period_count: int,
    taiyi_palace: int,
    tianmu: Any,
) -> dict[str, Any]:
    duty = zhimen_from_cycle_count(period_count)
    if not duty.get("computable"):
        return {
            "profile": profile,
            "duty": duty,
            "result": {
                "status": "not_computable",
                "computable": False,
                "three_doors_ready": None,
            },
        }

    if profile == "jinjing_strict":
        result = sanmen_jubu_from_period_count(
            period_count=period_count,
            taiyi_palace=taiyi_palace,
            tianmu=tianmu,
        )
    elif profile == "tongzong_v2":
        tz2 = taiyi_door_readiness(taiyi_palace, tianmu=tianmu)
        result = {
            **tz2,
            "three_doors_ready": tz2.get("door_ready"),
            "period_count": period_count,
            "direct_gate": duty["direct_gate"],
            "direct_gate_auspice": duty["auspice"],
            "within_240_cycle": duty["within_240_cycle"],
            "block_of_30": duty["block_of_30"],
            "integration_note": (
                "太乙门具按《统宗》卷二开门加太乙；"
                "240/30直使仅作为卷四同条独立岁计吉凶事实。"
            ),
        }
    else:
        raise ValueError("three_doors_profile须为jinjing_strict或tongzong_v2")

    return {"profile": profile, "duty": duty, "result": result}


def military_deployment_readiness(
    calc_value: int,
    *,
    period_count: int,
    taiyi_palace: int,
    tianmu: Any,
    shiji_yanji: bool | None,
    wenchang_qiupo: bool | None,
    major_minor_generals_related: bool | None,
    exit_gate: str | None = None,
    three_doors_profile: str = "jinjing_strict",
    calc_blocked: bool | None = None,
) -> dict[str, Any]:
    """串接三门、五将与J4M-05出师资格。

    calc_blocked 未显式给出时，只按当前 calc_value 是否属于
    5/15/25/35 自动生成当前一方的杜塞事实。
    """
    if calc_blocked is None:
        calc_blocked = calc_value in BLOCKED_CALCS
        calc_blocked_source = "derived_from_current_calc"
    elif isinstance(calc_blocked, bool):
        calc_blocked_source = "explicit"
    else:
        raise TypeError("calc_blocked须为bool或None")

    doors_stage = _three_doors(
        profile=three_doors_profile,
        period_count=period_count,
        taiyi_palace=taiyi_palace,
        tianmu=tianmu,
    )
    three_doors_ready = doors_stage["result"].get("three_doors_ready")

    source_generals = wujiang_fabu(
        shiji_yanji=shiji_yanji,
        wenchang_qiupo=wenchang_qiupo,
        major_minor_generals_related=major_minor_generals_related,
        three_doors_ready=three_doors_ready,
    )

    effective_generals = effective_five_generals_readiness(
        source_five_generals_released=source_generals.get("five_generals_released"),
        calc_blocked=calc_blocked,
    )

    deployment = chushi_fa(
        calc_value,
        three_doors_ready=three_doors_ready,
        five_generals_released=effective_generals.get(
            "effective_five_generals_released"
        ),
        exit_gate=exit_gate,
    )

    return {
        "schema_version": "1.0",
        "canonical": PIPELINE_VERSION,
        "rule_id": "CORE-MILITARY-DEPLOYMENT-READINESS",
        "cross_source_integration": True,
        "calc_value": calc_value,
        "calc_blocked": calc_blocked,
        "calc_blocked_source": calc_blocked_source,
        "three_doors_profile": three_doors_profile,
        "three_doors_ready": three_doors_ready,
        "source_five_generals_released": source_generals.get(
            "five_generals_released"
        ),
        "effective_five_generals_released": effective_generals.get(
            "effective_five_generals_released"
        ),
        "deployment_ready": deployment.get("deployment_ready"),
        "verdict": deployment.get("verdict"),
        "stages": {
            "three_doors": doors_stage,
            "five_generals_source": source_generals,
            "five_generals_effective": effective_generals,
            "deployment": deployment,
        },
        "policy": (
            "只串接既有规则；《统宗》卷二太乙门具仅在显式选择tongzong_v2时使用，"
            "不回写J4M-01。杜塞只在CORE层折算为五将不发。"
        ),
    }
