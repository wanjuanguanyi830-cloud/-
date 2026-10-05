"""《太乙统宗宝鉴》卷五“三门具不具”独立 source profile。

本模块只补卷五正文明确给出的正面“门具”条件，不回写
四库《太乙金镜式经》卷四 J4M-01 的严格 source-specific runtime。
"""

from __future__ import annotations

from .jinjing_eight_door_overlay import taiyi_eight_door_context

TZ5_THREE_DOORS_PROFILE = "tongzong_volume5_three_doors"
_EIGHT_GATES = ("开", "休", "生", "伤", "杜", "景", "死", "惊")
_THREE_DOORS = {"开", "休", "生"}


def sanmen_jubu_tongzong(*, taiyi_gate=None, tianmu_gate=None):
    """按《统宗》卷五“明三门具不具之术”判断三门具不具。

    明确条件：
    - 太乙、天目分临开/生二门：两门不具；
    - 临休门：三门不具；
    - 太乙、天目都不在开/休/生三门之下：门具。

    同落开、同落生、仅一者临开/生而另一者在三门外等
    文字未明确展开的组合仍保留为未定义，不作现代补全。
    """
    known = set(_EIGHT_GATES)
    for name, gate in (("taiyi_gate", taiyi_gate), ("tianmu_gate", tianmu_gate)):
        if gate is not None and gate not in known:
            return {
                "source_profile": TZ5_THREE_DOORS_PROFILE,
                "source_scope": "太乙统宗宝鉴_卷五_明三门具不具之术",
                "rule_id": "TZ5-THREE-DOORS",
                "status": "not_computable",
                "computable": False,
                "taiyi_gate": taiyi_gate,
                "tianmu_gate": tianmu_gate,
                "three_doors_ready": None,
                "reason": f"{name} 不是八门之一",
            }

    if taiyi_gate is None or tianmu_gate is None:
        return {
            "source_profile": TZ5_THREE_DOORS_PROFILE,
            "source_scope": "太乙统宗宝鉴_卷五_明三门具不具之术",
            "rule_id": "TZ5-THREE-DOORS",
            "status": "not_computable",
            "computable": False,
            "taiyi_gate": taiyi_gate,
            "tianmu_gate": tianmu_gate,
            "three_doors_ready": None,
            "reason": "缺太乙或天目所临门",
        }

    gates = {taiyi_gate, tianmu_gate}
    if "休" in gates:
        status = "three_doors_not_ready"
        ready = False
        not_ready_count = 3
        source_case = "临休门"
    elif gates == {"开", "生"}:
        status = "two_doors_not_ready"
        ready = False
        not_ready_count = 2
        source_case = "太乙天目分临开生二门"
    elif taiyi_gate not in _THREE_DOORS and tianmu_gate not in _THREE_DOORS:
        status = "three_doors_ready"
        ready = True
        not_ready_count = 0
        source_case = "太乙天目皆不在开休生三门之下"
    else:
        status = "not_defined_by_source_passage"
        ready = None
        not_ready_count = None
        source_case = "卷五本段未明确展开该组合"

    return {
        "source_profile": TZ5_THREE_DOORS_PROFILE,
        "source_scope": "太乙统宗宝鉴_卷五_明三门具不具之术",
        "rule_id": "TZ5-THREE-DOORS",
        "status": status,
        "computable": ready is not None,
        "taiyi_gate": taiyi_gate,
        "tianmu_gate": tianmu_gate,
        "three_doors": ["开", "休", "生"],
        "three_doors_ready": ready,
        "not_ready_count": not_ready_count,
        "source_case": source_case,
        "policy": "只实现卷五正文明确组合；不回填《金镜》J4M-01严格profile。",
    }



def sanmen_jubu_tongzong_from_positions(*, taiyi_palace, tianmu, direct_gate):
    """以当期直使门加太乙形成动态八门，再按《统宗》卷五判门具。"""
    context = taiyi_eight_door_context(
        taiyi_palace, tianmu=tianmu, anchor_door=direct_gate
    )
    result = sanmen_jubu_tongzong(
        taiyi_gate=context["taiyi_gate"],
        tianmu_gate=context["tianmu_gate"],
    )
    return {
        **result,
        "input_mode": "positions",
        "direct_gate": direct_gate,
        "taiyi_palace": taiyi_palace,
        "tianmu": tianmu,
        "tianmu_palace": context["tianmu_palace"],
        "eight_door_overlay": context["palace_to_door"],
        "overlay_rule_id": context["rule_id"],
        "integration_note": "直使门加太乙的空间盘负责门位；门具正面结论采用《统宗》卷五profile。",
    }
