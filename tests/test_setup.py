import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.logic.setup import (
    approve_framework,
    check_weights,
    format_approval_log,
    is_locked,
    new_approval_state,
    reopen_framework,
)


def test_new_state_is_unlocked_and_empty():
    state = new_approval_state()
    assert state["approved"] is False
    assert state["events"] == []
    assert is_locked(state) is False


def test_approve_happy_path():
    state = new_approval_state()
    new_state, message = approve_framework(state, note="Panel sign-off in workshop.")
    assert new_state is not state
    assert new_state["approved"] is True
    assert len(new_state["events"]) == 1
    assert new_state["events"][0]["type"] == "approved"
    assert new_state["events"][0]["note"] == "Panel sign-off in workshop."
    assert "approved" in message.lower()
    assert is_locked(new_state) is True
    # Original state untouched.
    assert state["approved"] is False
    assert state["events"] == []


def test_double_approve_refused():
    state, _ = approve_framework(new_approval_state())
    same_state, message = approve_framework(state)
    assert same_state["events"] == state["events"]
    assert len(same_state["events"]) == 1
    assert "already approved" in message.lower()


def test_reopen_with_empty_reason_refused():
    state, _ = approve_framework(new_approval_state())
    same_state, message = reopen_framework(state, "   ")
    assert same_state == state
    assert "reason is required" in message.lower()
    assert is_locked(same_state) is True


def test_reopen_never_approved_refused():
    state = new_approval_state()
    same_state, message = reopen_framework(state, "Need to fix a typo in criteria.")
    assert same_state == state
    assert "not currently approved" in message.lower()


def test_reopen_happy_path_logs_reason():
    state, _ = approve_framework(new_approval_state(), note="Initial approval.")
    reopened, message = reopen_framework(state, "Procurement asked for a new mandatory gate.")
    assert reopened is not state
    assert reopened["approved"] is False
    assert len(reopened["events"]) == 2
    assert reopened["events"][-1]["type"] == "reopened"
    assert reopened["events"][-1]["reason"] == "Procurement asked for a new mandatory gate."
    assert "reopened" in message.lower()
    assert is_locked(reopened) is False


def test_reopen_already_open_refused():
    state, _ = approve_framework(new_approval_state())
    reopened, _ = reopen_framework(state, "First reopen.")
    same_state, message = reopen_framework(reopened, "Second reopen attempt.")
    assert same_state == reopened
    assert "not currently approved" in message.lower()


def test_reapprove_after_reopen_keeps_full_history():
    state, _ = approve_framework(new_approval_state(), note="First pass.")
    reopened, _ = reopen_framework(state, "Adding a new criterion.")
    reapproved, message = approve_framework(reopened, note="Re-approved after adding criterion.")
    assert reapproved["approved"] is True
    assert len(reapproved["events"]) == 3
    types = [e["type"] for e in reapproved["events"]]
    assert types == ["approved", "reopened", "approved"]
    assert is_locked(reapproved) is True
    assert "approved" in message.lower()


def test_is_locked_transitions():
    state = new_approval_state()
    assert is_locked(state) is False
    state, _ = approve_framework(state)
    assert is_locked(state) is True
    state, _ = reopen_framework(state, "Need to revise weights.")
    assert is_locked(state) is False


def test_is_locked_handles_none_and_empty():
    assert is_locked(None) is False
    assert is_locked({}) is False


def test_format_approval_log_empty():
    rendered = format_approval_log(new_approval_state())
    assert "Not yet approved" in rendered


def test_format_approval_log_populated_newest_first():
    state, _ = approve_framework(new_approval_state(), note="Initial approval.")
    state, _ = reopen_framework(state, "Weights need revisiting.")
    rendered = format_approval_log(state)
    lines = [l for l in rendered.split("\n") if l.startswith("-")]
    assert len(lines) == 2
    # Newest first: reopened event should appear before the approved event.
    assert "Reopened" in lines[0]
    assert "Weights need revisiting" in lines[0]
    assert "Framework approved" in lines[1]
    assert "Initial approval." in lines[1]


def test_check_weights_sum_ok():
    criteria = [
        {"id": "A", "weight": 40},
        {"id": "B", "weight": 30},
        {"id": "C", "weight": 30},
    ]
    assert check_weights(criteria) is None


def test_check_weights_sum_off():
    criteria = [
        {"id": "A", "weight": 40},
        {"id": "B", "weight": 30},
    ]
    warning = check_weights(criteria)
    assert warning is not None
    assert "70" in warning
    assert "100" in warning


def test_check_weights_missing_weight():
    criteria = [
        {"id": "A", "weight": 50},
        {"id": "B"},
        {"id": "C", "weight": None},
    ]
    warning = check_weights(criteria)
    assert warning is not None
    assert "B" in warning
    assert "C" in warning
    # Does not attempt a sum warning when weights are missing.
    assert "100" not in warning or "sum" not in warning.lower()


def test_check_weights_empty_criteria():
    assert check_weights([]) is None


def test_check_weights_never_touches_vendor_scores():
    # Sanity: the function signature/behaviour is purely about the criteria
    # list passed in — it must not import or reference PANEL_SCORES/VENDORS.
    import app.logic.setup as setup_module

    source = open(setup_module.__file__, encoding="utf-8").read()
    assert "PANEL_SCORES" not in source
    assert "VENDORS" not in source


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: ok")
    print("All setup tests passed.")
