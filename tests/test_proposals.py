import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.logic.proposals import (
    confirm_proposal_set,
    format_proposal_log,
    is_confirmed,
    new_proposal_state,
    proposal_rows,
    reopen_proposal_set,
)

VENDORS = ["Acme CaseWorks", "NovaAI FlowSuite", "Titan Public Sector Suite"]

READINESS = {
    "Acme CaseWorks": {
        "status": "Accepted into evaluation",
        "note": "Reviewed against every mandatory gate and criterion.",
    },
    "NovaAI FlowSuite": {
        "status": "Loaded",
        "note": "Several unanswered criteria flagged for follow-up.",
    },
    # Titan Public Sector Suite intentionally absent from readiness.
}


def test_new_state_is_unconfirmed_and_empty():
    state = new_proposal_state()
    assert state["confirmed"] is False
    assert state["events"] == []
    assert is_confirmed(state) is False


def test_confirm_happy_path():
    state = new_proposal_state()
    new_state, message = confirm_proposal_set(state, note="Panel reviewed all vendors.")
    assert new_state is not state
    assert new_state["confirmed"] is True
    assert len(new_state["events"]) == 1
    assert new_state["events"][0]["type"] == "confirmed"
    assert new_state["events"][0]["note"] == "Panel reviewed all vendors."
    assert "confirmed" in message.lower()
    assert is_confirmed(new_state) is True
    # Original state untouched.
    assert state["confirmed"] is False
    assert state["events"] == []


def test_double_confirm_refused():
    state, _ = confirm_proposal_set(new_proposal_state())
    same_state, message = confirm_proposal_set(state)
    assert same_state["events"] == state["events"]
    assert len(same_state["events"]) == 1
    assert "already confirmed" in message.lower()


def test_reopen_with_empty_reason_refused():
    state, _ = confirm_proposal_set(new_proposal_state())
    same_state, message = reopen_proposal_set(state, "   ")
    assert same_state == state
    assert "reason is required" in message.lower()
    assert is_confirmed(same_state) is True


def test_reopen_never_confirmed_refused():
    state = new_proposal_state()
    same_state, message = reopen_proposal_set(state, "Need to add a late vendor.")
    assert same_state == state
    assert "not currently confirmed" in message.lower()


def test_reopen_happy_path_logs_reason():
    state, _ = confirm_proposal_set(new_proposal_state(), note="Initial confirm.")
    reopened, message = reopen_proposal_set(state, "Late vendor proposal accepted.")
    assert reopened is not state
    assert reopened["confirmed"] is False
    assert len(reopened["events"]) == 2
    assert reopened["events"][-1]["type"] == "reopened"
    assert reopened["events"][-1]["reason"] == "Late vendor proposal accepted."
    assert "reopened" in message.lower()
    assert is_confirmed(reopened) is False


def test_reopen_already_open_refused():
    state, _ = confirm_proposal_set(new_proposal_state())
    reopened, _ = reopen_proposal_set(state, "First reopen.")
    same_state, message = reopen_proposal_set(reopened, "Second reopen attempt.")
    assert same_state == reopened
    assert "not currently confirmed" in message.lower()


def test_reconfirm_after_reopen_keeps_full_history():
    state, _ = confirm_proposal_set(new_proposal_state(), note="First pass.")
    reopened, _ = reopen_proposal_set(state, "Adding a late vendor.")
    reconfirmed, message = confirm_proposal_set(reopened, note="Re-confirmed with late vendor.")
    assert reconfirmed["confirmed"] is True
    assert len(reconfirmed["events"]) == 3
    types = [e["type"] for e in reconfirmed["events"]]
    assert types == ["confirmed", "reopened", "confirmed"]
    assert is_confirmed(reconfirmed) is True


def test_is_confirmed_handles_none_and_empty():
    assert is_confirmed(None) is False
    assert is_confirmed({}) is False


def test_format_proposal_log_empty():
    rendered = format_proposal_log(new_proposal_state())
    assert "not yet confirmed" in rendered.lower()


def test_format_proposal_log_populated_newest_first():
    state, _ = confirm_proposal_set(new_proposal_state(), note="Initial confirm.")
    state, _ = reopen_proposal_set(state, "Late vendor added.")
    rendered = format_proposal_log(state)
    lines = [l for l in rendered.split("\n") if l.startswith("-")]
    assert len(lines) == 2
    # Newest first: reopened event appears before the confirmed event.
    assert "Reopened" in lines[0]
    assert "Late vendor added." in lines[0]
    assert "confirmed" in lines[1].lower()
    assert "Initial confirm." in lines[1]


def test_proposal_rows_every_vendor_present_and_correct():
    rows = proposal_rows(VENDORS, READINESS)
    assert len(rows) == len(VENDORS)
    by_vendor = {r[0]: r for r in rows}
    assert by_vendor["Acme CaseWorks"][1] == "Accepted into evaluation"
    assert "mandatory gate" in by_vendor["Acme CaseWorks"][2]
    assert by_vendor["NovaAI FlowSuite"][1] == "Loaded"


def test_proposal_rows_missing_vendor_is_explicit_not_omitted():
    rows = proposal_rows(VENDORS, READINESS)
    by_vendor = {r[0]: r for r in rows}
    assert "Titan Public Sector Suite" in by_vendor
    assert by_vendor["Titan Public Sector Suite"][1] == "No status recorded"


def test_proposal_rows_handles_empty_readiness():
    rows = proposal_rows(VENDORS, {})
    assert len(rows) == len(VENDORS)
    assert all(row[1] == "No status recorded" for row in rows)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: ok")
    print("All proposals tests passed.")
