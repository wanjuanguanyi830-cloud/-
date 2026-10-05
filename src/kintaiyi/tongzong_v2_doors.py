"""《太乙统宗宝鉴》卷二“明太乙八门通变术”门具规则。

本模块按卷二正文分别实现：
- 太乙之门具：开门加太乙宫，视天目；
- 主之门具：开门加主大将宫，视太乙、文昌；
- 客之门具：开门加客大将宫，视太乙、始击；
- 定计动态门盘：所求直事门加定计目所在之宫。

这四项不得合并为一张门盘。
"""

from __future__ import annotations

from typing import Any

from .jinjing_eight_door_overlay import duty_door_overlay, open_door_overlay
from .taiyi_rules import position, sector_to_nine_palace

SOURCE_PROFILE = "tongzong_volume2_eight_door_readiness"
SOURCE_SCOPE = "太乙统宗宝鉴_卷二_明太乙八门通变术"
GOOD_DOORS = frozenset({"开", "休", "生"})
OUTER_PALACES = frozenset({1, 2, 3, 4, 6, 7, 8, 9})


def _outer_palace(value: Any, *, field: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field}须为外八宫或十六宫位置")
    if isinstance(value, int):
        if value not in OUTER_PALACES:
            raise ValueError(f"{field}须为外八宫1/2/3/4/6/7/8/9")
        return value
    try:
        return sector_to_nine_palace(position(value))
    except (TypeError, ValueError, KeyError) as exc:
        raise ValueError(f"{field}须为外八宫、十六宫位置或十六神名") from exc


def _not_computable(rule_id: str, name: str, reason: str, **facts: Any) -> dict[str, Any]:
    return {
        "source_profile": SOURCE_PROFILE,
        "source_scope": SOURCE_SCOPE,
        "rule_id": rule_id,
        "name": name,
        "status": "not_computable",
        "computable": False,
        **facts,
        "door_ready": None,
        "reason": reason,
    }


def _evaluate_overlay(
    *,
    rule_id: str,
    name: str,
    anchor_palace: Any,
    subjects: dict[str, Any],
) -> dict[str, Any]:
    if anchor_palace is None:
        return _not_computable(
            rule_id, name, "缺锚点宫；杜塞/不出中宫时不得伪造外八宫门盘",
            anchor_palace=anchor_palace,
        )

    try:
        anchor = _outer_palace(anchor_palace, field="anchor_palace")
        overlay = open_door_overlay(anchor)
        subject_palaces = {
            label: _outer_palace(value, field=label)
            for label, value in subjects.items()
        }
    except ValueError as exc:
        return _not_computable(
            rule_id, name, str(exc),
            anchor_palace=anchor_palace,
            subjects=dict(subjects),
        )

    subject_gates = {
        label: overlay["palace_to_door"][palace]
        for label, palace in subject_palaces.items()
    }
    blocked_by = [
        label for label, gate in subject_gates.items()
        if gate in GOOD_DOORS
    ]
    ready = not blocked_by

    return {
        "source_profile": SOURCE_PROFILE,
        "source_scope": SOURCE_SCOPE,
        "rule_id": rule_id,
        "name": name,
        "status": "ready" if ready else "not_ready",
        "computable": True,
        "anchor_palace": anchor,
        "anchor_door": "开",
        "subjects": dict(subjects),
        "subject_palaces": subject_palaces,
        "subject_gates": subject_gates,
        "good_doors": ["开", "休", "生"],
        "blocked_by": blocked_by,
        "door_ready": ready,
        "palace_to_door": overlay["palace_to_door"],
        "policy": "门具按本条明确观察对象逐一判断；不借另一套太乙/主/客门盘替代。",
    }


def taiyi_door_readiness(taiyi_palace: int, *, tianmu: Any) -> dict[str, Any]:
    """开门加太乙宫；天目不在开休生下，为太乙之门具。"""
    return _evaluate_overlay(
        rule_id="TZ2-DOOR-TAIYI",
        name="太乙之门具",
        anchor_palace=taiyi_palace,
        subjects={"天目": tianmu},
    )


def host_door_readiness(
    host_big_palace: int | None,
    *,
    taiyi_palace: int,
    wenchang: Any,
) -> dict[str, Any]:
    """开门加主大将宫；太乙、文昌皆不在开休生下，为主之门具。"""
    return _evaluate_overlay(
        rule_id="TZ2-DOOR-HOST",
        name="主之门具",
        anchor_palace=host_big_palace,
        subjects={"太乙": taiyi_palace, "文昌": wenchang},
    )


def guest_door_readiness(
    guest_big_palace: int | None,
    *,
    taiyi_palace: int,
    shiji: Any,
) -> dict[str, Any]:
    """开门加客大将宫；太乙、始击皆不在开休生下，为客之门具。"""
    return _evaluate_overlay(
        rule_id="TZ2-DOOR-GUEST",
        name="客之门具",
        anchor_palace=guest_big_palace,
        subjects={"太乙": taiyi_palace, "始击": shiji},
    )


def dingji_duty_door_context(*, direct_gate: str, dingji_eye: Any) -> dict[str, Any]:
    """所求直事门加定计目所在之宫；只生成动态门盘，不补门具断语。"""
    try:
        eye_palace = _outer_palace(dingji_eye, field="定计目")
        overlay = duty_door_overlay(eye_palace, direct_gate)
    except ValueError as exc:
        return _not_computable(
            "TZ2-DOOR-DINGJI",
            "定计直事门盘",
            str(exc),
            direct_gate=direct_gate,
            dingji_eye=dingji_eye,
        )

    return {
        "source_profile": SOURCE_PROFILE,
        "source_scope": SOURCE_SCOPE,
        "rule_id": "TZ2-DOOR-DINGJI",
        "name": "定计直事门盘",
        "status": "ok",
        "computable": True,
        "direct_gate": direct_gate,
        "dingji_eye": dingji_eye,
        "dingji_eye_palace": eye_palace,
        "anchor_palace": eye_palace,
        "anchor_door": direct_gate,
        "palace_to_door": overlay["palace_to_door"],
        "door_ready": None,
        "policy": "卷二只说由此知四计动静吉凶；本层不自行补成主/客门具判定。",
    }


def three_readiness_bundle(
    *,
    taiyi_palace: int,
    tianmu: Any,
    host_big_palace: int | None,
    wenchang: Any,
    guest_big_palace: int | None,
    shiji: Any,
) -> dict[str, Any]:
    """一次返回太乙、主、客三套独立门具；不把三者压成单一布尔值。"""
    taiyi = taiyi_door_readiness(taiyi_palace, tianmu=tianmu)
    host = host_door_readiness(
        host_big_palace, taiyi_palace=taiyi_palace, wenchang=wenchang
    )
    guest = guest_door_readiness(
        guest_big_palace, taiyi_palace=taiyi_palace, shiji=shiji
    )
    return {
        "source_profile": SOURCE_PROFILE,
        "source_scope": SOURCE_SCOPE,
        "rule_id": "TZ2-DOOR-BUNDLE",
        "taiyi": taiyi,
        "host": host,
        "guest": guest,
        "all_three_computable": all(
            item.get("computable") is True for item in (taiyi, host, guest)
        ),
        "all_three_ready": (
            all(item.get("door_ready") is True for item in (taiyi, host, guest))
            if all(item.get("computable") is True for item in (taiyi, host, guest))
            else None
        ),
        "policy": "太乙门具、主门具、客门具是三张不同锚点门盘；all_three_ready仅为整合字段。",
    }
