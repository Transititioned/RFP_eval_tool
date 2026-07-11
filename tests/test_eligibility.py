import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.logic.eligibility import (
    ELIGIBILITY_OUTCOMES,
    compliance_rows,
    current_outcomes,
    format_eligibility_log,
    new_eligibility_state,
    record_eligibility,
)

VENDORS = ["Acme CaseWorks", "NovaAI FlowSuite", "Titan Public Sector Suite"]

GATES = [
    {"id": "GATE-01", "statement": "Customer data held in-region"},
    {"id": "GATE-02", "statement": "Full data export available on exit"},
]

COMPLIANCE = {
    "GATE-01": {
        "Acme CaseWorks": "Met",
        "NovaAI FlowSuite": "Unclear",
        # Titan Public Sector Suite intentionally absent.
    },
    # GATE-02 intentionally has no compliance entries recorded at all.
}


def test_compliance_rows_covers_every_gate_and_vendor_shape():
    rows = compliance_rows(GATES, VENDORS, COMPLIANCE)
    assert len(rows) == len(GATES)
    for row in rows:
        assert len(row) == 1 + len(VENDORS)


def test_compliance_rows_missing_cell_is_visible_not_hidden():
    rows = compliance_rows(GATES, VENDORS, COMPLIANCE)
    gate01_row = rows[0]
    titan_idx = VENDORS.index("Titan Public Sector Suite") + 1
    assert gate01_row[titan_idx] == "NOT RECORDED"
    gate02_row = rows[1]
    assert all(cell == "NOT RECORDED" for cell in gate02_row[1:])


def test_compliance_rows_present_values_pass_through():
    rows = compliance_rows(GATES, VENDORS, COMPLIANCE)
    gate01_row = rows[0]
    acme_idx = VENDORS.index("Acme CaseWorks") + 1
    assert gate01_row[acme_idx] == "Met"


def test_new_state_is_empty():
    state = new_eligibility_state()
    assert state["outcomes"] == {}
    assert state["events"] == []


def test_excluded_without_reason_refused_state_unchanged():
    state = new_eligibility_state()
    new_state, message = record_eligibility(state, "NovaAI FlowSuite", "Excluded", "")
    assert new_state == state
    assert new_state["outcomes"] == {}
    assert new_state["events"] == []
    assert "reason" in message.lower()


def test_excluded_with_whitespace_reason_refused():
    state = new_eligibility_state()
    new_state, message = record_eligibility(state, "NovaAI FlowSuite", "Excluded", "   ")
    assert new_state == state
    assert "reason" in message.lower()


def test_excluded_with_reason_recorded():
    state, message = record_eligibility(
        new_eligibility_state(),
        "NovaAI FlowSuite",
        "Excluded",
        "Failed mandatory GATE-02 data export requirement.",
    )
    assert state["outcomes"]["NovaAI FlowSuite"]["outcome"] == "Excluded"
    assert state["outcomes"]["NovaAI FlowSuite"]["reason"] == (
        "Failed mandatory GATE-02 data export requirement."
    )
    assert len(state["events"]) == 1
    assert "excluded" in message.lower()


def test_unknown_outcome_refused():
    state = new_eligibility_state()
    new_state, message = record_eligibility(state, "Acme CaseWorks", "Definitely Eligible")
    assert new_state == state
    assert new_state["outcomes"] == {}
    assert "unknown outcome" in message.lower()


def test_empty_vendor_refused():
    state = new_eligibility_state()
    new_state, message = record_eligibility(state, "   ", "Eligible")
    assert new_state == state
    assert "vendor is required" in message.lower()


def test_re_record_replaces_current_but_keeps_history():
    state, _ = record_eligibility(
        new_eligibility_state(), "Acme CaseWorks", "Conditionally eligible",
        "Pending final reference check.",
    )
    state, _ = record_eligibility(
        state, "Acme CaseWorks", "Eligible", "Reference check completed cleanly.",
    )
    assert state["outcomes"]["Acme CaseWorks"]["outcome"] == "Eligible"
    assert len(state["outcomes"]) == 1
    assert len(state["events"]) == 2
    assert state["events"][0]["outcome"] == "Conditionally eligible"
    assert state["events"][1]["outcome"] == "Eligible"


def test_non_excluded_reason_optional():
    state, message = record_eligibility(new_eligibility_state(), "Titan Public Sector Suite", "Eligible")
    assert state["outcomes"]["Titan Public Sector Suite"]["outcome"] == "Eligible"
    assert state["outcomes"]["Titan Public Sector Suite"]["reason"] == ""
    assert "recorded" in message.lower()


def test_current_outcomes_every_vendor_always_present():
    state, _ = record_eligibility(new_eligibility_state(), "Acme CaseWorks", "Eligible")
    rows = current_outcomes(state, VENDORS)
    assert len(rows) == len(VENDORS)
    by_vendor = {r[0]: r for r in rows}
    assert by_vendor["Acme CaseWorks"][1] == "Eligible"
    assert by_vendor["NovaAI FlowSuite"][1] == "Not yet assessed"
    assert by_vendor["Titan Public Sector Suite"][1] == "Not yet assessed"


def test_excluded_vendor_stays_visible_with_reason():
    state, _ = record_eligibility(
        new_eligibility_state(), "NovaAI FlowSuite", "Excluded",
        "Failed mandatory GATE-02 data export requirement.",
    )
    rows = current_outcomes(state, VENDORS)
    by_vendor = {r[0]: r for r in rows}
    assert by_vendor["NovaAI FlowSuite"][1] == "Excluded"
    assert "GATE-02" in by_vendor["NovaAI FlowSuite"][2]


def test_format_eligibility_log_empty():
    rendered = format_eligibility_log(new_eligibility_state())
    assert "no eligibility outcomes" in rendered.lower()


def test_format_eligibility_log_newest_first_and_excluded_format():
    state, _ = record_eligibility(new_eligibility_state(), "Acme CaseWorks", "Eligible")
    state, _ = record_eligibility(
        state, "NovaAI FlowSuite", "Excluded", "Failed GATE-02."
    )
    rendered = format_eligibility_log(state)
    lines = [l for l in rendered.split("\n") if l.startswith("-")]
    assert len(lines) == 2
    assert lines[0].startswith("- Excluded — NovaAI FlowSuite — reason: Failed GATE-02.")
    assert "Eligible" in lines[1]
    assert "Acme CaseWorks" in lines[1]


def test_eligibility_outcomes_vocabulary_matches_contract():
    assert ELIGIBILITY_OUTCOMES == [
        "Eligible", "Conditionally eligible", "Clarification required", "Excluded",
    ]


def test_record_eligibility_accepts_outcomes_override():
    state, message = record_eligibility(
        new_eligibility_state(), "Acme CaseWorks", "Custom Outcome",
        outcomes=["Custom Outcome"],
    )
    assert state["outcomes"]["Acme CaseWorks"]["outcome"] == "Custom Outcome"
    assert "recorded" in message.lower()


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: ok")
    print("All eligibility tests passed.")
