import pytest

from kintaiyi.limit_cycles import (
    BAILIU_SPEC,
    SOURCE_WITNESS,
    YANGJIU_SPEC,
    bailiu_limit,
    yangjiu_bailiu_limits,
    yangjiu_limit,
)
from kintaiyi.legacy_schema import classify_legacy_field
from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.pan_adapter import attach_v2_to_snapshot
from kintaiyi.pan_v2 import build_pan_v2, validate_pan_v2


def test_c36_source_constants_match_direct_limit_text():
    assert YANGJIU_SPEC == {
        "name": "阳九",
        "big_limit": 4560,
        "small_limit": 456,
        "small_limit_count": 10,
        "surplus_offset": 130,
        "extreme": "阳穷于九",
    }
    assert BAILIU_SPEC == {
        "name": "百六",
        "big_limit": 4320,
        "small_limit": 288,
        "small_limit_count": 15,
        "surplus_offset": 2050,
        "extreme": "阴穷于六",
    }
    assert SOURCE_WITNESS["online_witness_volume"] == 10
    assert SOURCE_WITNESS["project_legacy_volume_label"] == 9
    assert SOURCE_WITNESS["volume_status"] == "witness_volume_variant"


def test_yangjiu_small_limit_boundary_is_not_off_by_one():
    end_first = yangjiu_limit(326)
    next_first = yangjiu_limit(327)

    assert end_first["cycle_remainder"] == 456
    assert end_first["small_limit_index"] == 1
    assert end_first["year_in_small_limit"] == 456
    assert end_first["at_small_limit_end"] is True
    assert end_first["at_big_limit_end"] is False

    assert next_first["cycle_remainder"] == 457
    assert next_first["small_limit_index"] == 2
    assert next_first["year_in_small_limit"] == 1
    assert next_first["at_small_limit_end"] is False


def test_yangjiu_big_limit_end_maps_to_tenth_small_limit_end():
    data = yangjiu_limit(4430)
    assert data["cycle_remainder"] == 0
    assert data["small_limit_index"] == 10
    assert data["year_in_small_limit"] == 456
    assert data["at_small_limit_end"] is True
    assert data["at_big_limit_end"] is True


def test_bailiu_small_limit_boundary_is_not_off_by_one():
    end_first = bailiu_limit(2558)
    next_first = bailiu_limit(2559)

    assert end_first["cycle_remainder"] == 288
    assert end_first["small_limit_index"] == 1
    assert end_first["year_in_small_limit"] == 288
    assert end_first["at_small_limit_end"] is True

    assert next_first["cycle_remainder"] == 289
    assert next_first["small_limit_index"] == 2
    assert next_first["year_in_small_limit"] == 1


def test_bailiu_big_limit_end_maps_to_fifteenth_small_limit_end():
    data = bailiu_limit(2270)
    assert data["cycle_remainder"] == 0
    assert data["small_limit_index"] == 15
    assert data["year_in_small_limit"] == 288
    assert data["at_small_limit_end"] is True
    assert data["at_big_limit_end"] is True


def test_c36_rejects_negative_or_non_integer_accumulated_year():
    with pytest.raises(ValueError):
        yangjiu_limit(-1)
    with pytest.raises(TypeError):
        bailiu_limit(True)
    with pytest.raises(TypeError):
        yangjiu_bailiu_limits(1.5)


def test_c36_bundle_fits_pan_v2_cycles_limits():
    limits = yangjiu_bailiu_limits(1000)
    payload = build_pan_v2(cycles={"limits": limits})
    assert payload["cycles"]["limits"]["yangjiu"]["rule_id"] == "C36-YJ"
    assert payload["cycles"]["limits"]["bailiu"]["rule_id"] == "C36-BL"
    checked = validate_pan_v2(payload)
    assert checked["valid"] is True


def test_c36_legacy_flat_fields_are_quarantined_not_migrated_as_facts():
    assert classify_legacy_field("陽九")["status"] == "quarantined"
    assert classify_legacy_field("陽九")["replacement"] == "cycles.limits.yangjiu"
    assert classify_legacy_field("百六")["status"] == "quarantined"
    assert classify_legacy_field("百六")["replacement"] == "cycles.limits.bailiu"


def _legacy_snapshot():
    return {
        "太乙落宮": 1,
        "太乙": "乾",
        "陽九": "寅",
        "百六": "酉",
    }


def test_old_branch_values_do_not_auto_promote_to_canonical_limits():
    snapshot = attach_v2_to_snapshot(_legacy_snapshot())
    assert snapshot["v2"]["cycles"]["limits"] == {}

    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "cycles.limits.yangjiu",
        "cycles.limits.bailiu",
    ]
    assert report["ready_for_v2_core_consumption"] is False


def test_structured_limits_clear_legacy_branch_replacement_gaps():
    snapshot = attach_v2_to_snapshot(
        _legacy_snapshot(),
        cycles={"limits": yangjiu_bailiu_limits(1000)},
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == []
    assert report["ready_for_v2_core_consumption"] is True
    assert report["quarantined_key_count"] == 2
