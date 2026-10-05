from kintaiyi.jinjing_taigong_timing import evaluate_taigong_with_rule_readiness


def _base_kwargs(**updates):
    data = dict(
        taiyi_gate="伤",
        tianmu_gate="杜",
        shiji_yanji=False,
        wenchang_qiupo=False,
        major_minor_generals_related=False,
        calc_blocked=False,
        right_taiyi_left_tianmu=True,
        yinyang_harmonious=True,
        blocking_patterns=[],
        taiyi_in_yang_jue=False,
        spirits_independent=True,
        door="开",
        door_has_malefic_spirit=False,
        role="天子",
        occupied_xuanming_target="天乙",
        xuanming_in_wangxiang=True,
        upper_lower_generating=True,
        direct_envoy_clause_matched=True,
    )
    data.update(updates)
    return data


def test_c117_readiness_adapter_positive_chain_keeps_sources_separate():
    data = evaluate_taigong_with_rule_readiness(**_base_kwargs())

    integration = data["readiness_integration"]
    assert integration["three_doors"]["source_profile"] == "tongzong_volume5_three_doors"
    assert integration["three_doors"]["three_doors_ready"] is True
    assert integration["source_five_generals"]["source_profile"] == "jinjing_siku_volume4"
    assert integration["source_five_generals"]["five_generals_released"] is True
    assert integration["effective_five_generals"]["source_profile"] == "cross_source_integration"
    assert integration["effective_five_generals"]["effective_five_generals_released"] is True

    assert data["base_checks"]["three_doors_complete"] is True
    assert data["base_checks"]["five_generals_active"] is True
    assert data["military_action_favorable"] is True
    assert data["xuanming_harmony"] is True
    assert data["greatly_auspicious"] is True


def test_c117_calc_blocked_overrides_effective_readiness_not_j4m_source_fact():
    data = evaluate_taigong_with_rule_readiness(
        **_base_kwargs(calc_blocked=True)
    )

    integration = data["readiness_integration"]
    assert integration["source_five_generals"]["five_generals_released"] is True
    assert integration["effective_five_generals"]["effective_five_generals_released"] is False
    assert integration["effective_five_generals"]["reason"] == "杜塞，取五将不发"

    assert data["base_checks"]["five_generals_active"] is False
    assert data["military_action_favorable"] is False
    assert data["greatly_auspicious"] is False


def test_c117_three_doors_not_ready_short_circuits_taigong_base_chain():
    data = evaluate_taigong_with_rule_readiness(
        **_base_kwargs(taiyi_gate="休", tianmu_gate="伤")
    )

    integration = data["readiness_integration"]
    assert integration["three_doors"]["three_doors_ready"] is False
    assert integration["source_five_generals"]["five_generals_released"] is True
    assert data["base_checks"]["three_doors_complete"] is False
    assert data["military_action_favorable"] is False
    assert data["greatly_auspicious"] is False


def test_c117_undefined_tongzong_door_combination_stays_unknown():
    data = evaluate_taigong_with_rule_readiness(
        **_base_kwargs(taiyi_gate="开", tianmu_gate="伤")
    )

    integration = data["readiness_integration"]
    assert integration["three_doors"]["status"] == "not_defined_by_source_passage"
    assert integration["three_doors"]["three_doors_ready"] is None
    assert integration["source_five_generals"]["five_generals_released"] is True
    assert data["base_checks"]["three_doors_complete"] is None
    assert data["military_action_favorable"] is None
    assert data["greatly_auspicious"] is None


def test_c117_source_blocker_stays_j4m02_even_when_other_blocker_inputs_missing():
    data = evaluate_taigong_with_rule_readiness(
        **_base_kwargs(
            shiji_yanji=True,
            wenchang_qiupo=None,
            major_minor_generals_related=None,
        )
    )

    integration = data["readiness_integration"]
    source = integration["source_five_generals"]
    effective = integration["effective_five_generals"]
    assert source["five_generals_released"] is False
    assert source["blockers"] == ["始击有掩击"]
    assert effective["effective_five_generals_released"] is False
    assert data["military_action_favorable"] is False


def test_c117_readiness_provenance_explicitly_marks_cross_source_integration():
    data = evaluate_taigong_with_rule_readiness(**_base_kwargs())
    bounds = data["readiness_integration"]["source_boundaries"]

    assert bounds["three_doors"] == "太乙统宗宝鉴_卷五"
    assert bounds["five_generals"] == "太乙金镜式经_卷四_J4M-02"
    assert "不伪装" in bounds["calc_blocked"]
    assert bounds["taigong"] == "太乙金镜式经_卷一_推太公考时法"
