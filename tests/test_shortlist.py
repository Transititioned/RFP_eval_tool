import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.logic.shortlist import (
    approve_shortlist,
    current_shortlist,
    format_shortlist_log,
    is_approved,
    new_shortlist_state,
    propose_shortlist,
)

VENDORS = ["Acme CaseWorks", "NovaAI FlowSuite", "Titan Public Sector Suite"]


def test_new_state_is_empty():
    state = new_shortlist_state()
    assert state["proposal"] is None
    assert state["approved"] is False
    assert state["approval"] is None
    assert state["events"] == []
    assert is_approved(state) is False


def test_empty_proposal_refused():
    state = new_shortlist_state()
    new_state, message = propose_shortlist(state, [], ["Acme CaseWorks"])
    assert new_state == state
    assert new_state["events"] == []
    assert "vendor is required" in message.lower()


def test_divergent_proposal_without_reason_refused():
    state = new_shortlist_state()
    new_state, message = propose_shortlist(
        state, ["NovaAI FlowSuite"], ["Acme CaseWorks"], reason=""
    )
    assert new_state == state
    assert new_state["proposal"] is None
    assert new_state["events"] == []
    assert "reason is required" in message.lower()


def test_divergent_proposal_with_whitespace_reason_refused():
    state = new_shortlist_state()
    new_state, message = propose_shortlist(
        state, ["NovaAI FlowSuite"], ["Acme CaseWorks"], reason="   "
    )
    assert new_state == state
    assert "reason is required" in message.lower()


def test_divergent_proposal_with_reason_accepted():
    state = new_shortlist_state()
    new_state, message = propose_shortlist(
        state, ["NovaAI FlowSuite"], ["Acme CaseWorks"],
        reason="Panel weighed strategic fit higher than the mechanical ranking.",
    )
    assert new_state["proposal"]["vendors"] == ["NovaAI FlowSuite"]
    assert new_state["proposal"]["matched_mechanical"] is False
    assert new_state["proposal"]["reason"]
    assert len(new_state["events"]) == 1
    assert new_state["events"][0]["type"] == "proposed"
    assert "differing" in message.lower()


def test_matching_proposal_without_reason_accepted():
    state = new_shortlist_state()
    mechanical_top = ["Acme CaseWorks", "Titan Public Sector Suite"]
    new_state, message = propose_shortlist(
        state, ["Acme CaseWorks", "Titan Public Sector Suite"], mechanical_top
    )
    assert new_state["proposal"]["matched_mechanical"] is True
    assert new_state["proposal"]["reason"] == ""
    assert len(new_state["events"]) == 1
    assert "matching" in message.lower()


def test_matching_requires_same_order():
    state = new_shortlist_state()
    mechanical_top = ["Acme CaseWorks", "Titan Public Sector Suite"]
    new_state, message = propose_shortlist(
        state, ["Titan Public Sector Suite", "Acme CaseWorks"], mechanical_top,
    )
    # Order differs from mechanical_top, so this counts as a mismatch and
    # requires a reason.
    assert new_state == state
    assert "reason is required" in message.lower()


def test_reproposing_replaces_proposal_keeps_history():
    state, _ = propose_shortlist(
        new_shortlist_state(), ["Acme CaseWorks"], ["Acme CaseWorks"]
    )
    state, _ = propose_shortlist(
        state, ["Titan Public Sector Suite"], ["Acme CaseWorks"],
        reason="Reference checks favoured Titan.",
    )
    assert state["proposal"]["vendors"] == ["Titan Public Sector Suite"]
    assert len(state["events"]) == 2
    assert [e["type"] for e in state["events"]] == ["proposed", "proposed"]


def test_approve_without_approver_name_refused():
    state, _ = propose_shortlist(
        new_shortlist_state(), ["Acme CaseWorks"], ["Acme CaseWorks"]
    )
    new_state, message = approve_shortlist(state, "   ")
    assert new_state == state
    assert "approver name is required" in message.lower()


def test_approve_without_proposal_refused():
    state = new_shortlist_state()
    new_state, message = approve_shortlist(state, "Priya Chandrasekaran")
    assert new_state == state
    assert "propose a shortlist first" in message.lower()


def test_approve_happy_path():
    state, _ = propose_shortlist(
        new_shortlist_state(), ["Acme CaseWorks"], ["Acme CaseWorks"]
    )
    new_state, message = approve_shortlist(state, "Priya Chandrasekaran")
    assert new_state["approved"] is True
    assert new_state["approval"]["approver"] == "Priya Chandrasekaran"
    assert is_approved(new_state) is True
    assert len(new_state["events"]) == 2
    assert new_state["events"][-1]["type"] == "approved"
    assert "approved by Priya Chandrasekaran" in message


def test_double_approve_refused():
    state, _ = propose_shortlist(
        new_shortlist_state(), ["Acme CaseWorks"], ["Acme CaseWorks"]
    )
    state, _ = approve_shortlist(state, "Priya Chandrasekaran")
    same_state, message = approve_shortlist(state, "Marcus Odendaal")
    assert same_state == state
    assert "already approved" in message.lower()


def test_reproposal_after_approval_clears_approval_with_logged_event():
    state, _ = propose_shortlist(
        new_shortlist_state(), ["Acme CaseWorks"], ["Acme CaseWorks"]
    )
    state, _ = approve_shortlist(state, "Priya Chandrasekaran")
    assert state["approved"] is True

    new_state, message = propose_shortlist(
        state, ["Titan Public Sector Suite"], ["Acme CaseWorks"],
        reason="New reference information changed the panel's view.",
    )
    assert new_state["approved"] is False
    assert new_state["approval"] is None
    types = [e["type"] for e in new_state["events"]]
    assert types == ["proposed", "approved", "proposed", "approval_cleared"]
    assert "previous approval cleared" in message.lower()


def test_current_shortlist_empty():
    display = current_shortlist(new_shortlist_state())
    assert display["vendors"] == []
    assert display["matched_mechanical"] is None
    assert display["approved"] is False
    assert display["approver"] is None


def test_current_shortlist_populated():
    state, _ = propose_shortlist(
        new_shortlist_state(), ["Acme CaseWorks"], ["Acme CaseWorks"]
    )
    state, _ = approve_shortlist(state, "Priya Chandrasekaran")
    display = current_shortlist(state)
    assert display["vendors"] == ["Acme CaseWorks"]
    assert display["matched_mechanical"] is True
    assert display["approved"] is True
    assert display["approver"] == "Priya Chandrasekaran"
    assert display["approved_at"]


def test_format_shortlist_log_empty():
    rendered = format_shortlist_log(new_shortlist_state())
    assert "no shortlist proposed" in rendered.lower()


def test_format_shortlist_log_newest_first():
    state, _ = propose_shortlist(
        new_shortlist_state(), ["Acme CaseWorks"], ["Acme CaseWorks"]
    )
    state, _ = approve_shortlist(state, "Priya Chandrasekaran")
    rendered = format_shortlist_log(state)
    lines = [l for l in rendered.split("\n") if l.startswith("-")]
    assert len(lines) == 2
    assert "Approved" in lines[0]
    assert "Proposed" in lines[1]


def test_module_never_computes_its_own_ranking():
    # Sanity: this module must never import a ranking function or sample
    # scoring data itself — the caller always supplies mechanical_top.
    # (Docstrings may *mention* weighted_totals()/consensus_ranking() by
    # name to explain the contract; an actual import is what's forbidden.)
    import app.logic.shortlist as shortlist_module

    assert not hasattr(shortlist_module, "weighted_totals")
    assert not hasattr(shortlist_module, "consensus_ranking")
    assert not hasattr(shortlist_module, "PANEL_SCORES")
    source = open(shortlist_module.__file__, encoding="utf-8").read()
    assert "from app.data" not in source
    assert "import app.data" not in source
    assert "from app.logic.comparison" not in source


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: ok")
    print("All shortlist tests passed.")
