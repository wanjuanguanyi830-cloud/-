from kintaiyi.tongzong_v2_doors import (
    dingji_duty_door_context,
    guest_door_readiness,
    host_door_readiness,
    taiyi_door_readiness,
    three_readiness_bundle,
)


def test_tz2_taiyi_door_readiness_uses_open_door_at_taiyi():
    blocked = taiyi_door_readiness(1, tianmu="丑")
    assert blocked["anchor_door"] == "开"
    assert blocked["subject_palaces"]["天目"] == 3
    assert blocked["subject_gates"]["天目"] == "生"
    assert blocked["door_ready"] is False

    ready = taiyi_door_readiness(1, tianmu="卯")
    assert ready["subject_gates"]["天目"] == "伤"
    assert ready["door_ready"] is True


def test_tz2_host_door_readiness_observes_taiyi_and_wenchang():
    ready = host_door_readiness(
        8,
        taiyi_palace=1,
        wenchang="午",
    )
    assert ready["palace_to_door"][8] == "开"
    assert ready["subject_gates"] == {"太乙": "惊", "文昌": "杜"}
    assert ready["door_ready"] is True

    blocked = host_door_readiness(
        8,
        taiyi_palace=1,
        wenchang="卯",
    )
    assert blocked["subject_gates"]["文昌"] == "生"
    assert blocked["door_ready"] is False


def test_tz2_guest_door_readiness_observes_taiyi_and_shiji():
    ready = guest_door_readiness(
        3,
        taiyi_palace=7,
        shiji="酉",
    )
    assert ready["subject_gates"]["太乙"] == "杜"
    assert ready["subject_gates"]["始击"] == "景"
    assert ready["door_ready"] is True


def test_tz2_blocked_center_general_does_not_get_fake_door_overlay():
    blocked = host_door_readiness(
        None,
        taiyi_palace=1,
        wenchang="卯",
    )
    assert blocked["computable"] is False
    assert blocked["door_ready"] is None


def test_tz2_dingji_uses_direct_gate_at_dingji_eye_not_open_at_big_general():
    data = dingji_duty_door_context(direct_gate="伤", dingji_eye="卯")
    assert data["anchor_palace"] == 4
    assert data["anchor_door"] == "伤"
    assert data["palace_to_door"][4] == "伤"
    assert data["door_ready"] is None


def test_tz2_bundle_keeps_three_door_readinesses_separate():
    data = three_readiness_bundle(
        taiyi_palace=1,
        tianmu="卯",
        host_big_palace=8,
        wenchang="午",
        guest_big_palace=3,
        shiji="酉",
    )
    assert data["taiyi"]["door_ready"] is True
    assert data["host"]["door_ready"] is True
    assert data["guest"]["door_ready"] is True
    assert data["all_three_ready"] is True
