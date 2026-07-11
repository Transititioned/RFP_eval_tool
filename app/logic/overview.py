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
# tab is a stub (Options), or the stage doesn't exist yet at all. Hardcoded
# to "Not started" rather than fabricated from unrelated sample/synthetic
# data (e.g. Evaluation must not borrow progress from the Compare tab's
# sample vendors).
_FIXED_NOT_STARTED_ACTIONS = {
    "Options": "Name candidate options in the Options tab once intake is saved.",
    "Proposals": "Not available in this preview build.",
    "Eligibility": "Not available in this preview build.",
    "Evaluation": "Not available in this preview build.",
    "Shortlist": "Not available in this preview build.",
    "Recommendation": "Not available in this preview build.",
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


def stage_statuses(
    intake_log_rows=None,
    capability_grid=None,
    viability_grid=None,
    setup_approval_state=None,
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

    per_stage = {
        "Intake": (intake_stat, intake_action),
        "Assessment Detail": (assessment_stat, assessment_action),
        "Readout": (readout_stat, readout_action),
        "Setup": (setup_stat, setup_action),
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
