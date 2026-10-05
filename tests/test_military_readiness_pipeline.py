from kintaiyi.military_readiness_pipeline import military_deployment_readiness


def test_readiness_pipeline_tongzong_positive_chain_reaches_deployment():
    data = military_deployment_readiness(
        12,
        period_count=91,
        taiyi_palace=1,
        tianmu="卯",
        shiji_yanji=False,
        wenchang_qiupo=False,
        major_minor_generals_related=False,
        exit_gate="开",
        three_doors_profile="tongzong_v5",
    )
    assert data["stages"]["three_doors"]["duty"]["direct_gate"] == "伤"
    assert data["stages"]["three_doors"]["result"]["tianmu_gate"] == "死"
    assert data["three_doors_ready"] is True
    assert data["source_five_generals_released"] is True
    assert data["effective_five_generals_released"] is True
    assert data["deployment_ready"] is True


def test_readiness_pipeline_source_blocker_stops_deployment():
    data = military_deployment_readiness(
        12,
        period_count=91,
        taiyi_palace=1,
        tianmu="卯",
        shiji_yanji=True,
        wenchang_qiupo=None,
        major_minor_generals_related=None,
        exit_gate="开",
        three_doors_profile="tongzong_v5",
    )
    assert data["source_five_generals_released"] is False
    assert data["effective_five_generals_released"] is False
    assert data["deployment_ready"] is False


def test_readiness_pipeline_blocked_calc_forces_five_generals_not_released():
    data = military_deployment_readiness(
        25,
        period_count=91,
        taiyi_palace=1,
        tianmu="卯",
        shiji_yanji=False,
        wenchang_qiupo=False,
        major_minor_generals_related=False,
        exit_gate="开",
        three_doors_profile="tongzong_v5",
    )
    assert data["calc_blocked"] is True
    assert data["source_five_generals_released"] is True
    assert data["effective_five_generals_released"] is False
    assert data["deployment_ready"] is False


def test_readiness_pipeline_jinjing_strict_preserves_positive_gap():
    data = military_deployment_readiness(
        12,
        period_count=91,
        taiyi_palace=1,
        tianmu="卯",
        shiji_yanji=False,
        wenchang_qiupo=False,
        major_minor_generals_related=False,
        exit_gate="开",
        three_doors_profile="jinjing_strict",
    )
    assert data["three_doors_ready"] is None
    assert data["deployment_ready"] is None
    assert data["stages"]["deployment"]["status"] == "not_computable"
