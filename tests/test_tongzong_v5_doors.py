from kintaiyi.tongzong_v5_doors import sanmen_jubu_tongzong, sanmen_jubu_tongzong_from_positions


def test_tz5_three_doors_positive_case_when_both_avoid_three_doors():
    data = sanmen_jubu_tongzong(taiyi_gate="伤", tianmu_gate="景")
    assert data["source_profile"] == "tongzong_volume5_three_doors"
    assert data["three_doors_ready"] is True
    assert data["not_ready_count"] == 0


def test_tz5_three_doors_keeps_explicit_negative_cases():
    two = sanmen_jubu_tongzong(taiyi_gate="开", tianmu_gate="生")
    assert two["three_doors_ready"] is False
    assert two["not_ready_count"] == 2

    three = sanmen_jubu_tongzong(taiyi_gate="休", tianmu_gate="伤")
    assert three["three_doors_ready"] is False
    assert three["not_ready_count"] == 3


def test_tz5_three_doors_does_not_invent_ambiguous_combinations():
    data = sanmen_jubu_tongzong(taiyi_gate="开", tianmu_gate="伤")
    assert data["status"] == "not_defined_by_source_passage"
    assert data["three_doors_ready"] is None



def test_tz5_positions_use_current_direct_gate_overlay():
    ready = sanmen_jubu_tongzong_from_positions(
        taiyi_palace=1, tianmu="卯", direct_gate="伤"
    )
    assert ready["taiyi_gate"] == "伤"
    assert ready["tianmu_gate"] == "死"
    assert ready["three_doors_ready"] is True

    blocked = sanmen_jubu_tongzong_from_positions(
        taiyi_palace=1, tianmu="丑", direct_gate="开"
    )
    assert blocked["taiyi_gate"] == "开"
    assert blocked["tianmu_gate"] == "生"
    assert blocked["three_doors_ready"] is False
