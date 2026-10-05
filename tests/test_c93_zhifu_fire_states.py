import pytest

from kintaiyi.zhifu_fire_states import (
    KNOWN_STATES,
    LEGACY_RECOVERY,
    c93_catalog,
    zhifu_known_fire_state,
)


@pytest.mark.parametrize(
    "palace,state,phrase",
    [
        (2, "旺", "火旺"),
        (3, "长生", "火长生"),
        (4, "败", "火败"),
    ],
)
def test_c93_direct_known_states(palace, state, phrase):
    data = zhifu_known_fire_state(palace)
    assert data["state"] == state
    assert phrase in data["source_phrase"]
    assert data["status"] == "direct_source_state"
    assert data["pending"] == []


@pytest.mark.parametrize("palace", [1, 5, 6, 7, 8, 9, 10, 11, 12])
def test_c93_unknown_palaces_stay_pending_instead_of_auto_filling(palace):
    data = zhifu_known_fire_state(palace)
    assert data["state"] is None
    assert data["status"] == "source_pending"
    assert "不得按十二长生" in "；".join(data["pending"])


def test_c93_does_not_auto_read_c64_position():
    data = zhifu_known_fire_state(2)
    assert data["position_boundary"]["position_runtime"] == "C64-ZHIFU"
    assert data["position_boundary"]["auto_position_lookup_used"] is False


def test_c93_recovery_is_within_user_requested_two_day_window():
    assert LEGACY_RECOVERY["branch"] == "codex/c1-c7-canonical"
    assert LEGACY_RECOVERY["file_commit"] == "f02c052ae88e"
    assert LEGACY_RECOVERY["file_commit_date"].startswith("2026-10-04")
    assert LEGACY_RECOVERY["time_window_policy"] == (
        "only_2026-10-04_and_2026-10-05_prior_work"
    )
    assert LEGACY_RECOVERY["legacy_table"] == {"2": "旺", "3": "长生", "4": "败"} or LEGACY_RECOVERY["legacy_table"] == {2: "旺", 3: "长生", 4: "败"}


def test_c93_rejects_bad_palace_inputs():
    with pytest.raises(TypeError):
        zhifu_known_fire_state(True)
    with pytest.raises(TypeError):
        zhifu_known_fire_state("2")
    with pytest.raises(ValueError):
        zhifu_known_fire_state(0)
    with pytest.raises(ValueError):
        zhifu_known_fire_state(13)


def test_c93_catalog_explicitly_refuses_full_state_table():
    data = c93_catalog()
    assert data["known_palaces"] == [2, 3, 4]
    assert data["full_twelve_palace_state_table_ready"] is False
    assert data["known_states"] == KNOWN_STATES
