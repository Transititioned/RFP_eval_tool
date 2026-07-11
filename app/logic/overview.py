"""Per-stage workflow status for the Overview tab.

Mockup/stub pass: cheap, honest heuristics only. No scores, no weighting,
no roll-ups, no percentage-complete, and nothing that ranks options or
vendors — status chips restate workflow state only, the same restraint the
Readout tab applies to grid values.

Pure functions: plain Python lists/dicts in, plain Python lists/dicts out.
No Gradio imports, no calls to app/logic/persistence.py or the Hub API —
the UI layer is responsible for fetching inputs (e.g. via
``load_intake_log()``) and passing them in.
"""

STAGES = [
    "Intake",
    "Options",
    "Assessment Detail",
    "Readout",
    "Setup",
    "Proposals",
    "Eligibility",
    "Evaluation",
    "Shortlist",
    "Recommendation",
    "Validation",
]

STATUSES = (
    "Not started",
    "In progress",
    "Needs attention",
    "Ready for approval",
    "Complete",
)

# Stages that have no computable state in this preview build: either the
# tab is a stub (Options), or there's a static/standing tab with nothing to
# derive (Validation). Hardcoded to "Not started" rather than fabricated
# from unrelated sample/synthetic data. Evaluation/Shortlist/Recommendation
# used to be hardcoded here too, but now have real derivable state — see
# evaluation_status()/shortlist_status()/recommendation_status() below.
_FIXED_NOT_STARTED_ACTIONS = {
    "Options": "Name candidate options in the Options tab once intake is saved.",
    "Validation": "Review the standing validation questions in the Validation tab.",
}


def _is_filled(value):
    """A cell counts as answered if it's non-empty and not the 'Unknown' placeholder."""
    if value is None:
        return False
    text = str(value).strip()
    if not text:
        return False
    return text.lower() != "unknown"


def _cell_values(grid):
    """All per-option cells in a grid (every column after the row label)."""
    values = []
    for row in grid:
        values.extend(list(row)[1:])
    return values


def intake_status(intake_log_rows):
    """Status/next_action for the Intake stage.

    intake_log_rows: whatever app.logic.persistence.load_intake_log() returns
    as its rows list (or [] if nothing was loaded/saved).
    """
    if intake_log_rows:
        return (
            "Complete",
            "Sourcing request saved. Revisit only if the request itself changes.",
        )
    return "Not started", "Complete the sourcing request form and save it."


def assessment_detail_status(capability_grid, viability_grid):
    """Status/next_action for the Assessment Detail stage.

    Looks at both grids together (Capability Coverage Matrix + Baseline
    Viability Gate), since that's the one Assessment Detail tab. A
    mandatory-gate Fail always surfaces as "Needs attention", even once
    every cell is filled in — the workflow status must never let a Fail
    quietly read as "Complete".
    """
    all_cells = _cell_values(capability_grid) + _cell_values(viability_grid)
    if not all_cells:
        return (
            "Not started",
            "Begin scoring the Capability Coverage Matrix and Baseline Viability Gate.",
        )

    filled = [c for c in all_cells if _is_filled(c)]
    if not filled:
        return (
            "Not started",
            "Begin scoring the Capability Coverage Matrix and Baseline Viability Gate.",
        )
    if len(filled) < len(all_cells):
        return (
            "In progress",
            "Continue filling in the Capability Coverage Matrix and Baseline Viability Gate.",
        )

    viability_cells = _cell_values(viability_grid)
    has_fail = any(str(c).strip().lower() == "fail" for c in viability_cells)
    if has_fail:
        return (
            "Needs attention",
            "Review the Baseline Viability Gate — at least one option has failed "
            "a mandatory check.",
        )
    return "Complete", "Assessment complete — proceed to the Readout tab."


def _grids_fully_filled(capability_grid, viability_grid):
    all_cells = _cell_values(capability_grid) + _cell_values(viability_grid)
    if not all_cells:
        return False
    return all(_is_filled(c) for c in all_cells)


def readout_status(capability_grid, viability_grid):
    """Status/next_action for the Readout stage.

    The readout only restates the two grids, so it's only meaningful once
    they're fully filled in — at that point it's ready for a human to
    generate and review, never auto-marked "Complete" on its own.
    """
    if _grids_fully_filled(capability_grid, viability_grid):
        return "Ready for approval", "Generate and review the plain-English readout."
    return (
        "Not started",
        "Complete the Assessment Detail grids before generating a readout.",
    )


def setup_status(setup_approval_state):
    """Status/next_action for the Setup stage.

    Derived only from the approval state (app.logic.setup), honestly:
    - None, or never approved with an empty event log -> "Not started".
    - Has events but isn't currently approved (i.e. it was approved then
      reopened) -> "Needs attention" — it needs re-approval before the
      workbench should treat criteria/weights as locked again.
    - Currently approved -> "Complete".
    """
    if not setup_approval_state:
        return (
            "Not started",
            "Define criteria, weights and mandatory requirements in the Setup tab.",
        )

    events = setup_approval_state.get("events") or []
    approved = bool(setup_approval_state.get("approved"))

    if approved:
        return (
            "Complete",
            "Framework approved and locked. Reopen only with a logged reason if it must change.",
        )
    if events:
        return (
            "Needs attention",
            "Framework was reopened after approval — review changes and re-approve.",
        )
    return (
        "Not started",
        "Define criteria, weights and mandatory requirements in the Setup tab.",
    )


def proposals_status(proposals_state):
    """Status/next_action for the Proposals stage.

    Derived only from the confirm-proposal-set state
    (app.logic.proposals), the same honest pattern as setup_status():
    - None, or never confirmed with an empty event log -> "Not started".
    - Has events but isn't currently confirmed (i.e. it was confirmed then
      reopened) -> "Needs attention" — it needs re-confirmation.
    - Currently confirmed -> "Complete".
    """
    if not proposals_state:
        return (
            "Not started",
            "Load and confirm the vendor proposal set in the Proposals tab.",
        )

    events = proposals_state.get("events") or []
    confirmed = bool(proposals_state.get("confirmed"))

    if confirmed:
        return (
            "Complete",
            "Proposal set confirmed. Reopen only with a logged reason if it must change.",
        )
    if events:
        return (
            "Needs attention",
            "Proposal set was reopened after confirmation — review and re-confirm.",
        )
    return (
        "Not started",
        "Load and confirm the vendor proposal set in the Proposals tab.",
    )


def eligibility_status(eligibility_state, eligibility_vendors=None):
    """Status/next_action for the Eligibility stage.

    Derived only from recorded eligibility outcomes
    (app.logic.eligibility) — a human action — never from sample
    compliance data:
    - No outcomes recorded -> "Not started".
    - Any *current* outcome is "Clarification required" -> "Needs
      attention", regardless of how many other vendors are assessed —
      mirrors the "gates are never diluted" rule: a clarification flag
      must surface even if everything else looks done.
    - Some, but not (verifiably) all, vendors assessed -> "In progress".
    - Every vendor in ``eligibility_vendors`` has a current outcome ->
      "Complete". If ``eligibility_vendors`` isn't supplied, completeness
      can't be verified, so the status stays "In progress" rather than
      guessing "Complete".
    """
    outcomes = (eligibility_state or {}).get("outcomes") or {}
    if not outcomes:
        return (
            "Not started",
            "Record eligibility outcomes for each vendor in the Eligibility tab.",
        )

    if any(entry.get("outcome") == "Clarification required" for entry in outcomes.values()):
        return (
            "Needs attention",
            "At least one vendor is marked 'Clarification required' — follow up "
            "before proceeding.",
        )

    vendors = eligibility_vendors or []
    if vendors and set(vendors) <= set(outcomes.keys()):
        return (
            "Complete",
            "Every vendor has a recorded eligibility outcome.",
        )
    return (
        "In progress",
        "Continue recording eligibility outcomes for the remaining vendors.",
    )


def evaluation_status(consensus_log):
    """Status/next_action for the Evaluation stage.

    Derived only from user-recorded consensus entries
    (``app.logic.comparison.record_consensus()``'s log shape), never from
    the sample ``PANEL_SCORES`` data — scoring that data ships with would
    fabricate progress the user hasn't actually recorded:
    - None/empty log -> "Not started".
    - Any recorded consensus entry -> "In progress". This stage has no
      "Complete" state of its own here (completeness is what the
      Shortlist/Recommendation stages build on).
    """
    if not consensus_log:
        return (
            "Not started",
            "Score criteria in the Compare tab and record consensus for the panel.",
        )
    return (
        "In progress",
        "Continue recording consensus for remaining criteria in the Compare tab.",
    )


def _propose_approve_status(state, not_started_action, in_progress_action, needs_attention_action, complete_action):
    """Shared status derivation for shortlist_state/recommendation_state.

    Both state shapes follow the same propose-or-record -> approve pattern
    with an explicit "approval_cleared" event on re-proposal/re-record, so
    the status logic is identical modulo copy — see
    app.logic.shortlist/app.logic.recommendation.
    """
    if not state:
        return "Not started", not_started_action

    events = state.get("events") or []
    if not events:
        return "Not started", not_started_action

    if state.get("approved"):
        return "Complete", complete_action

    if any(e.get("type") == "approval_cleared" for e in events):
        return "Needs attention", needs_attention_action

    return "In progress", in_progress_action


def shortlist_status(shortlist_state):
    """Status/next_action for the Shortlist stage.

    Derived only from ``app.logic.shortlist`` state:
    - No events -> "Not started".
    - Proposed but not approved -> "In progress".
    - Approved -> "Complete".
    - Approval cleared by a re-proposal -> "Needs attention" (never silently
      still "Complete").
    """
    return _propose_approve_status(
        shortlist_state,
        not_started_action="Propose a shortlist in the Shortlist tab once vendor scoring is underway.",
        in_progress_action="Shortlist proposed — approve it in the Shortlist tab.",
        needs_attention_action="Shortlist was re-proposed after approval — review and re-approve.",
        complete_action="Shortlist approved. Re-propose only with a reason if it must change.",
    )


def recommendation_status(recommendation_state):
    """Status/next_action for the Recommendation stage.

    Derived only from ``app.logic.recommendation`` state, same pattern as
    ``shortlist_status()``:
    - No events -> "Not started".
    - Recorded but not approved -> "In progress".
    - Approved -> "Complete".
    - Approval cleared by a re-record -> "Needs attention".
    """
    return _propose_approve_status(
        recommendation_state,
        not_started_action="Record a supplier recommendation in the Recommendation tab once evaluation is complete.",
        in_progress_action="Recommendation recorded — approve it in the Recommendation tab.",
        needs_attention_action="Recommendation was re-recorded after approval — review and re-approve.",
        complete_action="Recommendation approved. Re-record only with reasons if it must change.",
    )


def stage_statuses(
    intake_log_rows=None,
    capability_grid=None,
    viability_grid=None,
    setup_approval_state=None,
    proposals_state=None,
    eligibility_state=None,
    eligibility_vendors=None,
    consensus_log=None,
    shortlist_state=None,
    recommendation_state=None,
):
    """Status for every workflow stage, in STAGES order.

    Returns a list of dicts: [{"stage": str, "status": str, "next_action": str}, ...]
    one entry per stage in STAGES, in order.

    Inputs are plain data supplied by the caller (the UI callback), e.g.:
        rows, _ = load_intake_log()
        stage_statuses(rows, capability_table_value, viability_table_value)
    This module never fetches its own data and never imports persistence.

    ``setup_approval_state`` is the dict shape produced by
    app.logic.setup.new_approval_state() / approve_framework() /
    reopen_framework(); omitted or None behaves exactly as before this
    parameter existed (Setup hardcoded to "Not started").

    ``proposals_state`` is the dict shape produced by
    app.logic.proposals.new_proposal_state() / confirm_proposal_set() /
    reopen_proposal_set(); omitted or None behaves exactly as before this
    parameter existed (Proposals hardcoded to "Not started").

    ``eligibility_state`` is the dict shape produced by
    app.logic.eligibility.new_eligibility_state() / record_eligibility();
    ``eligibility_vendors`` is the full vendor list to check completeness
    against (e.g. app.data.comparison_sample.VENDORS). Both omitted or None
    behaves exactly as before these parameters existed (Eligibility
    hardcoded to "Not started").

    ``consensus_log`` is the list shape produced by
    app.logic.comparison.record_consensus(); omitted or None/empty behaves
    exactly as before this parameter existed (Evaluation hardcoded to "Not
    started") — deliberately never derived from the sample PANEL_SCORES.

    ``shortlist_state`` is the dict shape produced by
    app.logic.shortlist.new_shortlist_state() / propose_shortlist() /
    approve_shortlist(); ``recommendation_state`` is the dict shape produced
    by app.logic.recommendation.new_recommendation_state() /
    record_recommendation() / approve_recommendation(). Both omitted or None
    behave exactly as before these parameters existed (Shortlist/
    Recommendation hardcoded to "Not started").
    """
    intake_log_rows = intake_log_rows or []
    capability_grid = capability_grid or []
    viability_grid = viability_grid or []

    intake_stat, intake_action = intake_status(intake_log_rows)
    assessment_stat, assessment_action = assessment_detail_status(
        capability_grid, viability_grid
    )
    readout_stat, readout_action = readout_status(capability_grid, viability_grid)
    setup_stat, setup_action = setup_status(setup_approval_state)
    proposals_stat, proposals_action = proposals_status(proposals_state)
    eligibility_stat, eligibility_action = eligibility_status(
        eligibility_state, eligibility_vendors
    )
    evaluation_stat, evaluation_action = evaluation_status(consensus_log)
    shortlist_stat, shortlist_action = shortlist_status(shortlist_state)
    recommendation_stat, recommendation_action = recommendation_status(recommendation_state)

    per_stage = {
        "Intake": (intake_stat, intake_action),
        "Assessment Detail": (assessment_stat, assessment_action),
        "Readout": (readout_stat, readout_action),
        "Setup": (setup_stat, setup_action),
        "Proposals": (proposals_stat, proposals_action),
        "Eligibility": (eligibility_stat, eligibility_action),
        "Evaluation": (evaluation_stat, evaluation_action),
        "Shortlist": (shortlist_stat, shortlist_action),
        "Recommendation": (recommendation_stat, recommendation_action),
    }

    results = []
    for stage in STAGES:
        if stage in per_stage:
            status, action = per_stage[stage]
        else:
            status = "Not started"
            action = _FIXED_NOT_STARTED_ACTIONS.get(
                stage, "Not available in this preview build."
            )
        results.append({"stage": stage, "status": status, "next_action": action})
    return results


def format_overview(statuses):
    """Render stage_statuses() output as a markdown table for display."""
    lines = [
        "| Stage | Status | Next recommended action |",
        "|---|---|---|",
    ]
    lines += [
        f"| {s['stage']} | {s['status']} | {s['next_action']} |" for s in statuses
    ]
    lines.append("")
    lines.append(
        "_Workflow status only — no scores, weighting, or ranking are computed here._"
    )
    return "\n".join(lines)
