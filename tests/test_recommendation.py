import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.logic.recommendation import (
    approve_recommendation,
    current_recommendation,
    format_recommendation_log,
    new_recommendation_state,
    record_recommendation,
)


def test_new_state_is_empty():
    state = new_recommendation_state()
    assert state["record"] is None
    assert state["approved"] is False
    assert state["approval"] is None
    assert state["events"] == []


def test_recommendation_without_reasons_refused():
    state = new_recommendation_state()
    new_state, message = record_recommendation(
        state, preferred="Acme CaseWorks", recommended="Acme CaseWorks", reasons="   "
    )
    assert new_state == state
    assert new_state["events"] == []
    assert "reason is required" in message.lower()


def test_recommendation_with_reasons_accepted():
    state = new_recommendation_state()
    new_state, message = record_recommendation(
        state,
        preferred="Acme CaseWorks",
        recommended="Acme CaseWorks",
        reasons="Strongest evidenced coverage on lifecycle and DR criteria.",
        risks="Least innovative UX of the three vendors.",
        conditions="Confirm pricing holds for a 3-year term.",
        dissent="Business Rep would have preferred NovaAI on innovation grounds.",
    )
    assert new_state["record"]["preferred"] == "Acme CaseWorks"
    assert new_state["record"]["recommended"] == "Acme CaseWorks"
    assert new_state["record"]["reasons"]
    assert new_state["record"]["risks"]
    assert new_state["record"]["conditions"]
    assert new_state["record"]["dissent"]
    assert len(new_state["events"]) == 1
    assert new_state["events"][0]["type"] == "recorded"
    assert "recorded" in message.lower()


def test_preferred_without_recommended_does_not_require_reasons():
    # Preferred-only entries (e.g. an early personal read before the panel
    # settles on a recommendation) are not held to the "reasons required"
    # gate — that gate is specifically about a *recommended* supplier.
    state = new_recommendation_state()
    new_state, message = record_recommendation(
        state, preferred="NovaAI FlowSuite", recommended="", reasons=""
    )
    assert new_state["record"]["preferred"] == "NovaAI FlowSuite"
    assert new_state["record"]["recommended"] == ""
    assert len(new_state["events"]) == 1
    assert "recorded" in message.lower()


def test_preferred_recommended_and_highest_scoring_can_differ():
    # This module never receives or stores a "highest scoring" value at
    # all -- the point is it can never be smuggled in as the recommendation.
    state, _ = record_recommendation(
        new_recommendation_state(),
        preferred="Titan Public Sector Suite",
        recommended="NovaAI FlowSuite",
        reasons="Panel valued NovaAI's roadmap despite lower current score.",
    )
    display = current_recommendation(state)
    assert display["preferred"] == "Titan Public Sector Suite"
    assert display["recommended"] == "NovaAI FlowSuite"
    assert "highest_scoring" not in display
    assert "highest" not in display


def test_approve_without_approver_name_refused():
    state, _ = record_recommendation(
        new_recommendation_state(), "Acme CaseWorks", "Acme CaseWorks",
        "Strong evidenced coverage.",
    )
    new_state, message = approve_recommendation(state, "")
    assert new_state == state
    assert "approver name is required" in message.lower()


def test_approve_without_record_refused():
    state = new_recommendation_state()
    new_state, message = approve_recommendation(state, "Fiona Nakamura-Blake")
    assert new_state == state
    assert "record a recommendation first" in message.lower()


def test_approve_happy_path():
    state, _ = record_recommendation(
        new_recommendation_state(), "Acme CaseWorks", "Acme CaseWorks",
        "Strong evidenced coverage.",
    )
    new_state, message = approve_recommendation(state, "Fiona Nakamura-Blake")
    assert new_state["approved"] is True
    assert new_state["approval"]["approver"] == "Fiona Nakamura-Blake"
    assert len(new_state["events"]) == 2
    assert new_state["events"][-1]["type"] == "approved"
    assert "approved by Fiona Nakamura-Blake" in message


def test_double_approve_refused():
    state, _ = record_recommendation(
        new_recommendation_state(), "Acme CaseWorks", "Acme CaseWorks",
        "Strong evidenced coverage.",
    )
    state, _ = approve_recommendation(state, "Fiona Nakamura-Blake")
    same_state, message = approve_recommendation(state, "Marcus Odendaal")
    assert same_state == state
    assert "already approved" in message.lower()


def test_re_record_after_approval_clears_approval_with_logged_event():
    state, _ = record_recommendation(
        new_recommendation_state(), "Acme CaseWorks", "Acme CaseWorks",
        "Strong evidenced coverage.",
    )
    state, _ = approve_recommendation(state, "Fiona Nakamura-Blake")
    assert state["approved"] is True

    new_state, message = record_recommendation(
        state, "Acme CaseWorks", "Titan Public Sector Suite",
        "New DR test evidence changed the panel's view.",
    )
    assert new_state["approved"] is False
    assert new_state["approval"] is None
    types = [e["type"] for e in new_state["events"]]
    assert types == ["recorded", "approved", "recorded", "approval_cleared"]
    assert "previous approval cleared" in message.lower()


def test_current_recommendation_empty():
    display = current_recommendation(new_recommendation_state())
    assert display["preferred"] == ""
    assert display["recommended"] == ""
    assert display["approved"] is False
    assert display["approver"] is None


def test_format_recommendation_log_empty():
    rendered = format_recommendation_log(new_recommendation_state())
    assert "no recommendation recorded" in rendered.lower()


def test_format_recommendation_log_newest_first():
    state, _ = record_recommendation(
        new_recommendation_state(), "Acme CaseWorks", "Acme CaseWorks",
        "Strong evidenced coverage.",
    )
    state, _ = approve_recommendation(state, "Fiona Nakamura-Blake")
    rendered = format_recommendation_log(state)
    lines = [l for l in rendered.split("\n") if l.startswith("-")]
    assert len(lines) == 2
    assert "Approved" in lines[0]
    assert "Recorded" in lines[1]


def test_module_never_computes_a_ranking_or_score():
    # (Docstrings may *mention* weighted_totals()/consensus_ranking() by
    # name to explain the "highest-scoring is display data, never stored"
    # contract; an actual import is what's forbidden.)
    import app.logic.recommendation as recommendation_module

    assert not hasattr(recommendation_module, "weighted_totals")
    assert not hasattr(recommendation_module, "consensus_ranking")
    assert not hasattr(recommendation_module, "PANEL_SCORES")
    source = open(recommendation_module.__file__, encoding="utf-8").read()
    assert "from app.data" not in source
    assert "import app.data" not in source
    assert "from app.logic.comparison" not in source


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: ok")
    print("All recommendation tests passed.")
