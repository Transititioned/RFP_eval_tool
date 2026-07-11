import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.logic.comparison import record_consensus
from app.logic.eligibility import new_eligibility_state, record_eligibility
from app.logic.overview import STAGES, STATUSES, format_overview, stage_statuses
from app.logic.proposals import confirm_proposal_set, new_proposal_state, reopen_proposal_set
from app.logic.recommendation import (
    approve_recommendation,
    new_recommendation_state,
    record_recommendation,
)
from app.logic.setup import approve_framework, new_approval_state, reopen_framework
from app.logic.shortlist import approve_shortlist, new_shortlist_state, propose_shortlist

VENDORS = ["Acme CaseWorks", "NovaAI FlowSuite", "Titan Public Sector Suite"]


def _by_stage(statuses):
    return {s["stage"]: s for s in statuses}


def test_empty_state_all_not_started():
    statuses = stage_statuses(intake_log_rows=[], capability_grid=[], viability_grid=[])
    assert [s["stage"] for s in statuses] == STAGES
    for s in statuses:
        assert s["status"] == "Not started"
        assert s["next_action"]


def test_intake_rows_present_marks_complete():
    rows = [["2026-07-11T00:00:00Z", "Project X", "Business Rep"]]
    statuses = _by_stage(stage_statuses(intake_log_rows=rows, capability_grid=[], viability_grid=[]))
    assert statuses["Intake"]["status"] == "Complete"


def test_partially_filled_grids_in_progress():
    capability_grid = [
        ["Cap A", "Strong", "Unknown"],
        ["Cap B", "Partial", "Weak"],
    ]
    viability_grid = [
        ["Viab A", "Pass", "Unknown"],
    ]
    statuses = _by_stage(
        stage_statuses(intake_log_rows=[], capability_grid=capability_grid, viability_grid=viability_grid)
    )
    assert statuses["Assessment Detail"]["status"] == "In progress"
    # Grids aren't fully filled yet, so the readout isn't ready either.
    assert statuses["Readout"]["status"] == "Not started"


def test_complete_grids_with_fail_needs_attention():
    capability_grid = [
        ["Cap A", "Strong", "Weak"],
        ["Cap B", "Partial", "Strong"],
    ]
    viability_grid = [
        ["Viab A", "Pass", "Fail"],
        ["Viab B", "Pass", "Clarify"],
    ]
    statuses = _by_stage(
        stage_statuses(intake_log_rows=[], capability_grid=capability_grid, viability_grid=viability_grid)
    )
    assert statuses["Assessment Detail"]["status"] == "Needs attention"
    # Every cell is filled in, so the readout is still ready for review even
    # though the assessment itself needs attention.
    assert statuses["Readout"]["status"] == "Ready for approval"


def test_complete_clean_grids_ready_for_readout():
    capability_grid = [
        ["Cap A", "Strong", "Weak"],
        ["Cap B", "Partial", "Strong"],
    ]
    viability_grid = [
        ["Viab A", "Pass", "Pass"],
        ["Viab B", "Pass", "Clarify"],
    ]
    statuses = _by_stage(
        stage_statuses(intake_log_rows=[], capability_grid=capability_grid, viability_grid=viability_grid)
    )
    assert statuses["Assessment Detail"]["status"] == "Complete"
    assert statuses["Readout"]["status"] == "Ready for approval"


def test_downstream_stages_are_always_not_started():
    capability_grid = [["Cap A", "Strong", "Weak"]]
    viability_grid = [["Viab A", "Pass", "Pass"]]
    rows = [["2026-07-11T00:00:00Z", "Project X", "Business Rep"]]
    statuses = _by_stage(
        stage_statuses(intake_log_rows=rows, capability_grid=capability_grid, viability_grid=viability_grid)
    )
    for stage in ("Options", "Setup", "Proposals", "Eligibility", "Evaluation", "Shortlist", "Recommendation", "Validation"):
        assert statuses[stage]["status"] == "Not started", stage


def test_all_statuses_are_from_the_vocabulary():
    capability_grid = [["Cap A", "Strong", "Weak"]]
    viability_grid = [["Viab A", "Pass", "Fail"]]
    statuses = stage_statuses(intake_log_rows=[["r"]], capability_grid=capability_grid, viability_grid=viability_grid)
    for s in statuses:
        assert s["status"] in STATUSES


def test_stage_statuses_without_setup_arg_is_backward_compatible():
    # Existing callers that don't pass setup_approval_state must behave
    # exactly as before this parameter existed.
    statuses = _by_stage(
        stage_statuses(intake_log_rows=[], capability_grid=[], viability_grid=[])
    )
    assert statuses["Setup"]["status"] == "Not started"
    assert statuses["Setup"]["next_action"]


def test_setup_status_never_started_is_not_started():
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            setup_approval_state=new_approval_state(),
        )
    )
    assert statuses["Setup"]["status"] == "Not started"


def test_setup_status_approved_is_complete():
    state, _ = approve_framework(new_approval_state(), note="Panel sign-off.")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            setup_approval_state=state,
        )
    )
    assert statuses["Setup"]["status"] == "Complete"


def test_setup_status_reopened_needs_attention():
    state, _ = approve_framework(new_approval_state(), note="Panel sign-off.")
    reopened, _ = reopen_framework(state, "Procurement asked for a new mandatory gate.")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            setup_approval_state=reopened,
        )
    )
    assert statuses["Setup"]["status"] == "Needs attention"


def test_format_overview_renders_a_table():
    statuses = stage_statuses(intake_log_rows=[], capability_grid=[], viability_grid=[])
    rendered = format_overview(statuses)
    assert "Intake" in rendered
    assert "Not started" in rendered
    assert rendered.startswith("| Stage |")


def test_stage_statuses_without_proposals_or_eligibility_args_is_backward_compatible():
    statuses = _by_stage(
        stage_statuses(intake_log_rows=[], capability_grid=[], viability_grid=[])
    )
    assert statuses["Proposals"]["status"] == "Not started"
    assert statuses["Proposals"]["next_action"]
    assert statuses["Eligibility"]["status"] == "Not started"
    assert statuses["Eligibility"]["next_action"]


def test_proposals_status_never_confirmed_is_not_started():
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            proposals_state=new_proposal_state(),
        )
    )
    assert statuses["Proposals"]["status"] == "Not started"


def test_proposals_status_confirmed_is_complete():
    state, _ = confirm_proposal_set(new_proposal_state(), note="Panel reviewed all vendors.")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            proposals_state=state,
        )
    )
    assert statuses["Proposals"]["status"] == "Complete"


def test_proposals_status_reopened_needs_attention():
    state, _ = confirm_proposal_set(new_proposal_state())
    reopened, _ = reopen_proposal_set(state, "Late vendor proposal accepted.")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            proposals_state=reopened,
        )
    )
    assert statuses["Proposals"]["status"] == "Needs attention"


def test_eligibility_status_no_outcomes_not_started():
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            eligibility_state=new_eligibility_state(), eligibility_vendors=VENDORS,
        )
    )
    assert statuses["Eligibility"]["status"] == "Not started"


def test_eligibility_status_some_assessed_in_progress():
    state, _ = record_eligibility(new_eligibility_state(), "Acme CaseWorks", "Eligible")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            eligibility_state=state, eligibility_vendors=VENDORS,
        )
    )
    assert statuses["Eligibility"]["status"] == "In progress"


def test_eligibility_status_all_assessed_complete():
    state = new_eligibility_state()
    for vendor in VENDORS:
        state, _ = record_eligibility(state, vendor, "Eligible")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            eligibility_state=state, eligibility_vendors=VENDORS,
        )
    )
    assert statuses["Eligibility"]["status"] == "Complete"


def test_eligibility_status_clarification_required_needs_attention_even_if_all_assessed():
    state = new_eligibility_state()
    for vendor in VENDORS:
        state, _ = record_eligibility(state, vendor, "Eligible")
    state, _ = record_eligibility(state, VENDORS[0], "Clarification required")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            eligibility_state=state, eligibility_vendors=VENDORS,
        )
    )
    assert statuses["Eligibility"]["status"] == "Needs attention"


def test_eligibility_status_without_vendor_list_never_claims_complete():
    state, _ = record_eligibility(new_eligibility_state(), "Acme CaseWorks", "Eligible")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            eligibility_state=state,
        )
    )
    assert statuses["Eligibility"]["status"] == "In progress"


def test_eligibility_status_excluded_vendor_still_counts_toward_assessed():
    state = new_eligibility_state()
    for vendor in VENDORS:
        if vendor == "NovaAI FlowSuite":
            state, _ = record_eligibility(state, vendor, "Excluded", "Failed mandatory gate.")
        else:
            state, _ = record_eligibility(state, vendor, "Eligible")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            eligibility_state=state, eligibility_vendors=VENDORS,
        )
    )
    assert statuses["Eligibility"]["status"] == "Complete"


def test_stage_statuses_without_evaluation_shortlist_recommendation_args_is_backward_compatible():
    statuses = _by_stage(
        stage_statuses(intake_log_rows=[], capability_grid=[], viability_grid=[])
    )
    assert statuses["Evaluation"]["status"] == "Not started"
    assert statuses["Evaluation"]["next_action"]
    assert statuses["Shortlist"]["status"] == "Not started"
    assert statuses["Shortlist"]["next_action"]
    assert statuses["Recommendation"]["status"] == "Not started"
    assert statuses["Recommendation"]["next_action"]


def test_evaluation_status_empty_consensus_log_not_started():
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            consensus_log=[],
        )
    )
    assert statuses["Evaluation"]["status"] == "Not started"


def test_evaluation_status_recorded_consensus_in_progress():
    log, _ = record_consensus([], "APP-01", "Acme CaseWorks", 4, "Panel agreed on evidence.")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            consensus_log=log,
        )
    )
    assert statuses["Evaluation"]["status"] == "In progress"


def test_evaluation_status_never_fabricated_from_sample_panel_scores():
    # Sanity: stage_statuses()/evaluation_status() must derive Evaluation
    # status purely from the consensus_log argument, never by importing the
    # sample PANEL_SCORES data (mentions in comments/docstrings explaining
    # this constraint are fine — an actual import is not).
    import app.logic.overview as overview_module

    assert not hasattr(overview_module, "PANEL_SCORES")
    source = open(overview_module.__file__, encoding="utf-8").read()
    assert "import PANEL_SCORES" not in source
    assert "from app.data" not in source
    assert "import app.data" not in source


def test_shortlist_status_no_events_not_started():
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            shortlist_state=new_shortlist_state(),
        )
    )
    assert statuses["Shortlist"]["status"] == "Not started"


def test_shortlist_status_proposed_not_approved_in_progress():
    state, _ = propose_shortlist(new_shortlist_state(), ["Acme CaseWorks"], ["Acme CaseWorks"])
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            shortlist_state=state,
        )
    )
    assert statuses["Shortlist"]["status"] == "In progress"


def test_shortlist_status_approved_complete():
    state, _ = propose_shortlist(new_shortlist_state(), ["Acme CaseWorks"], ["Acme CaseWorks"])
    state, _ = approve_shortlist(state, "Priya Chandrasekaran")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            shortlist_state=state,
        )
    )
    assert statuses["Shortlist"]["status"] == "Complete"


def test_shortlist_status_reproposed_after_approval_needs_attention():
    state, _ = propose_shortlist(new_shortlist_state(), ["Acme CaseWorks"], ["Acme CaseWorks"])
    state, _ = approve_shortlist(state, "Priya Chandrasekaran")
    state, _ = propose_shortlist(
        state, ["NovaAI FlowSuite"], ["Acme CaseWorks"], reason="New evidence changed the panel's view."
    )
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            shortlist_state=state,
        )
    )
    assert statuses["Shortlist"]["status"] == "Needs attention"


def test_recommendation_status_no_events_not_started():
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            recommendation_state=new_recommendation_state(),
        )
    )
    assert statuses["Recommendation"]["status"] == "Not started"


def test_recommendation_status_recorded_not_approved_in_progress():
    state, _ = record_recommendation(
        new_recommendation_state(), "Acme CaseWorks", "Acme CaseWorks",
        "Strong evidenced coverage.",
    )
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            recommendation_state=state,
        )
    )
    assert statuses["Recommendation"]["status"] == "In progress"


def test_recommendation_status_approved_complete():
    state, _ = record_recommendation(
        new_recommendation_state(), "Acme CaseWorks", "Acme CaseWorks",
        "Strong evidenced coverage.",
    )
    state, _ = approve_recommendation(state, "Fiona Nakamura-Blake")
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            recommendation_state=state,
        )
    )
    assert statuses["Recommendation"]["status"] == "Complete"


def test_recommendation_status_re_recorded_after_approval_needs_attention():
    state, _ = record_recommendation(
        new_recommendation_state(), "Acme CaseWorks", "Acme CaseWorks",
        "Strong evidenced coverage.",
    )
    state, _ = approve_recommendation(state, "Fiona Nakamura-Blake")
    state, _ = record_recommendation(
        state, "Acme CaseWorks", "Titan Public Sector Suite",
        "New DR evidence changed the panel's view.",
    )
    statuses = _by_stage(
        stage_statuses(
            intake_log_rows=[], capability_grid=[], viability_grid=[],
            recommendation_state=state,
        )
    )
    assert statuses["Recommendation"]["status"] == "Needs attention"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: ok")
    print("All overview tests passed.")
