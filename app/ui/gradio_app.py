"""Gradio UI for the Capability Sourcing Workbench MVP-0."""

import gradio as gr

from app.data.sample_data import (
    CAPABILITY_HEADERS,
    CAPABILITY_VALUES,
    COMPLETED_CAPABILITY_MATRIX,
    COMPLETED_VIABILITY_GATE,
    VIABILITY_HEADERS,
    VIABILITY_VALUES,
    blank_capability_matrix,
    blank_viability_gate,
)
from app.data.comparison_sample import (
    ARCHITECTURE_DOMAINS,
    CRITERIA,
    DEFAULT_SCORING_MODE,
    ELIGIBILITY_COMPLIANCE,
    ELIGIBILITY_OUTCOMES,
    EVALUATION_TEAM,
    GATES,
    PROPOSAL_READINESS,
    PROPOSAL_STATUSES,
    SCORE_SCALE,
    SCORING_MODES,
    SCORING_SCALE,
    SHORTLIST_RULE,
    VENDORS,
)
from app.logic.comparison import (
    comparison_rows,
    format_consensus_log,
    format_criterion_detail,
    format_focus_queue,
    gate_rows,
    record_consensus,
)
from app.logic.eligibility import (
    compliance_rows,
    current_outcomes,
    format_eligibility_log,
    new_eligibility_state,
    record_eligibility,
)
from app.logic.overview import stage_statuses
from app.logic.persistence import FIELDNAMES as INTAKE_LOG_FIELDNAMES
from app.logic.persistence import append_intake_record, load_intake_log
from app.logic.proposals import (
    confirm_proposal_set,
    format_proposal_log,
    is_confirmed,
    new_proposal_state,
    proposal_rows,
    reopen_proposal_set,
)
from app.logic.readout import generate_readout
from app.logic.setup import (
    approve_framework,
    check_weights,
    format_approval_log,
    is_locked,
    new_approval_state,
    reopen_framework,
)

CUSTOM_CSS = """
footer, .footer { display: none !important; }
.gradio-container { max-width: 1280px !important; margin: 0 auto !important; }
h1, h2 { letter-spacing: -0.01em; }
"""

REQUESTER_ROLES = ["PM", "Architect", "Procurement", "Product", "Other"]
YES_NO_UNKNOWN = ["Yes", "No", "Unknown"]

DEFAULT_OPTION_NAMES = [
    "ERP module",
    "Case platform",
    "Billing extension",
    "Shiny AI product",
    "Hybrid/composite option",
]

VALIDATION_QUESTIONS_MD = (
    "1. Did any gate feel like you had already answered it in the matrix?\n"
    "2. What else would you want to check before proceeding?\n"
    "3. Does this need a score, or is reading the grid enough?\n"
    "4. Would you actually fill this in for a real sourcing decision?\n"
    "5. Who would own this artifact in your organisation?"
)

OVERVIEW_INTRO_MD = (
    "Workflow status at a glance for the sourcing evaluation. This restates "
    "progress already captured in the tabs below — it does not compute a "
    "score, weighting, or recommendation."
)

SETUP_INTRO_MD = (
    "Define the evaluation framework — criteria, weights, mandatory "
    "requirements and scoring mode — before proposals are compared. "
    "Approving the framework locks it; reopening it requires a logged reason."
)

SETUP_SCORING_MODE_MD = (
    "**Panel + Consensus** (shipped default) — each evaluator scores every "
    "criterion individually; divergence between evaluators is surfaced and "
    "a consensus score is recorded by the panel with a rationale.\n\n"
    "**Traditional weighted** — criteria carry a percentage weight, in line "
    "with common procurement practice, for a weighted total per vendor.\n\n"
    "In both modes the tool never auto-declares a winner: a recommended "
    "supplier is always a separate, deliberate action taken by the "
    "evaluation panel, not an output of this selector. The weighted-totals "
    "view in Compare is not built yet — this selector configures the "
    "evaluation framework only."
)

SETUP_GATES_INTRO_MD = (
    "Requirements defined here sit outside scoring entirely and are "
    "evaluated per vendor in the Compare tab — a failed mandatory "
    "requirement can never be offset by a good score elsewhere."
)

PROPOSALS_INTRO_MD = (
    "Supplier and proposal readiness register for this evaluation. The "
    "table below is sample data for this preview build — this tool does "
    "not upload, parse or extract vendor documents; readiness is logged "
    "manually by the evaluation office as proposals are loaded and reviewed."
)

ELIGIBILITY_INTRO_MD = (
    "This eligibility gate applies to **vendors** (proposals), distinct "
    "from the Baseline Viability Gate in Assessment Detail, which applies "
    "to **options**. Eligibility sits outside scoring: an exclusion here is "
    "never offset by a good score elsewhere. The compliance table below is "
    "sample data — outcomes are always recorded as a deliberate human "
    "action, never derived from it automatically."
)

# Presentation-only status -> (background, text) colour mapping for the
# Overview status chips. Deliberately muted; no business logic lives here.
_OVERVIEW_STATUS_COLORS = {
    "Not started": ("#f1f1f1", "#555555"),
    "In progress": ("#e8f0fe", "#1a4480"),
    "Needs attention": ("#fdf3e0", "#8a5a00"),
    "Ready for approval": ("#e6f4f1", "#0f6657"),
    "Complete": ("#e6f4ea", "#1e7e34"),
}


def _overview_status_chip(status):
    bg, fg = _OVERVIEW_STATUS_COLORS.get(status, ("#f1f1f1", "#555555"))
    return (
        f'<span style="background:{bg};color:{fg};padding:2px 10px;'
        f'border-radius:3px;font-size:0.85em;white-space:nowrap;">{status}</span>'
    )


def _overview_table_rows(statuses):
    """Render app.logic.overview.stage_statuses() output as Dataframe rows."""
    return [
        [s["stage"], _overview_status_chip(s["status"]), s["next_action"]]
        for s in statuses
    ]


def load_blank():
    return blank_capability_matrix(), blank_viability_gate(), ""


def load_example():
    return (
        [list(r) for r in COMPLETED_CAPABILITY_MATRIX],
        [list(r) for r in COMPLETED_VIABILITY_GATE],
        "",
    )


def save_intake(
    project_name,
    requester_role,
    business_area,
    problem_statement,
    why_now,
    primary_capability,
    desired_decision_date,
    budget_confirmed,
    compliance_deadline,
    incumbent_or_preferred_vendor,
    existing_license_or_contract,
):
    lines = [
        "### Intake summary",
        "",
        f"- **Project / sourcing name:** {project_name or '_(not set)_'}",
        f"- **Requester role:** {requester_role or '_(not set)_'}",
        f"- **Business area:** {business_area or '_(not set)_'}",
        f"- **Problem statement:** {problem_statement or '_(not set)_'}",
        f"- **Why now:** {why_now or '_(not set)_'}",
        f"- **Primary business capability:** {primary_capability or '_(not set)_'}",
        f"- **Desired decision date:** {desired_decision_date or '_(not set)_'}",
        f"- **Budget confirmed:** {budget_confirmed}",
        f"- **Compliance or regulatory deadline:** {compliance_deadline}",
        f"- **Existing incumbent or preferred vendor:** {incumbent_or_preferred_vendor}",
        f"- **Existing licence or contract available:** {existing_license_or_contract}",
        "",
        "Continue to **Options**, then **Assessment Detail**.",
    ]

    save_status = append_intake_record(
        {
            "project_name": project_name,
            "requester_role": requester_role,
            "business_area": business_area,
            "problem_statement": problem_statement,
            "why_now": why_now,
            "primary_capability": primary_capability,
            "desired_decision_date": desired_decision_date,
            "budget_confirmed": budget_confirmed,
            "compliance_deadline": compliance_deadline,
            "incumbent_or_preferred_vendor": incumbent_or_preferred_vendor,
            "existing_license_or_contract": existing_license_or_contract,
        }
    )
    lines += ["", save_status]

    return "\n".join(lines)


def _blank(value):
    text = str(value).strip() if value is not None else ""
    return text if text else "— not provided —"


def refresh_setup_procurement_summary(
    project_name,
    requester_role,
    business_area,
    problem_statement,
    desired_decision_date,
):
    """Thin restating of the Intake tab's own fields — no computation."""
    lines = [
        "### Procurement summary (from Intake)",
        "",
        f"- **Project / sourcing name:** {_blank(project_name)}",
        f"- **Requester role:** {_blank(requester_role)}",
        f"- **Business area:** {_blank(business_area)}",
        f"- **Problem statement:** {_blank(problem_statement)}",
        f"- **Desired decision date:** {_blank(desired_decision_date)}",
    ]
    return "\n".join(lines)


def _criteria_table_to_dicts(criteria_table):
    """Reshape a gr.Dataframe value (ID, Domain, Statement, Weight rows) into
    the plain dicts app.logic.setup.check_weights() expects. Data marshaling
    only — no validation logic lives here."""
    rows = criteria_table.values.tolist() if hasattr(criteria_table, "values") else criteria_table
    criteria = []
    for row in rows:
        row = list(row) + [None] * 4
        cid, domain, statement, weight = row[:4]
        try:
            weight_val = float(weight) if weight not in (None, "") else None
        except (TypeError, ValueError):
            weight_val = None
        criteria.append(
            {"id": cid, "domain": domain, "statement": statement, "weight": weight_val}
        )
    return criteria


def check_setup_weights(criteria_table):
    warning = check_weights(_criteria_table_to_dicts(criteria_table))
    return warning or "OK — weights sum to 100."


def on_approve_setup_framework(state, note):
    new_state, message = approve_framework(state, note)
    locked = is_locked(new_state)
    return (
        new_state,
        message,
        format_approval_log(new_state),
        gr.update(interactive=not locked),
        gr.update(interactive=not locked),
        gr.update(interactive=not locked),
    )


def on_reopen_setup_framework(state, reason):
    new_state, message = reopen_framework(state, reason)
    locked = is_locked(new_state)
    return (
        new_state,
        message,
        format_approval_log(new_state),
        gr.update(interactive=not locked),
        gr.update(interactive=not locked),
        gr.update(interactive=not locked),
    )


def refresh_overview(
    capability_grid,
    viability_grid,
    setup_approval_state=None,
    proposals_state=None,
    eligibility_state=None,
):
    """Refresh the Overview tab's workflow status table.

    Thin wiring: fetches the persisted intake log (degrading to [] if
    HF_TOKEN is absent or the fetch fails, same as the Intake tab's saved
    log viewer) and defers all status logic to
    app.logic.overview.stage_statuses.
    """
    intake_rows, _log_status = load_intake_log()
    statuses = stage_statuses(
        intake_rows,
        capability_grid,
        viability_grid,
        setup_approval_state=setup_approval_state,
        proposals_state=proposals_state,
        eligibility_state=eligibility_state,
        eligibility_vendors=VENDORS,
    )
    return _overview_table_rows(statuses)


def on_confirm_proposal_set(state, note):
    new_state, message = confirm_proposal_set(state, note)
    confirmed = is_confirmed(new_state)
    return (
        new_state,
        message,
        format_proposal_log(new_state),
        gr.update(interactive=not confirmed),
    )


def on_reopen_proposal_set(state, reason):
    new_state, message = reopen_proposal_set(state, reason)
    confirmed = is_confirmed(new_state)
    return (
        new_state,
        message,
        format_proposal_log(new_state),
        gr.update(interactive=not confirmed),
    )


def on_record_eligibility(state, vendor, outcome, reason):
    new_state, message = record_eligibility(
        state, vendor, outcome, reason, outcomes=ELIGIBILITY_OUTCOMES
    )
    return (
        new_state,
        message,
        current_outcomes(new_state, VENDORS),
        format_eligibility_log(new_state),
    )


def build_app():
    with gr.Blocks(title="RFP Evaluation Tool — MVP-0") as demo:
        gr.Markdown("# Make the right sourcing call before the RFP starts.")
        gr.Markdown(
            "Save your time and make the right call. Our AI assistant will make "
            "sourcing software simple and easy. And audit trailed every step of "
            "the way."
        )

        with gr.Tabs():
            with gr.TabItem("Overview"):
                gr.Markdown("### Workflow status")
                gr.Markdown(OVERVIEW_INTRO_MD)

                refresh_overview_btn = gr.Button("Refresh status")
                overview_df = gr.Dataframe(
                    headers=["Stage", "Status", "Next recommended action"],
                    value=_overview_table_rows(
                        stage_statuses(
                            intake_log_rows=[],
                            capability_grid=blank_capability_matrix(),
                            viability_grid=blank_viability_gate(),
                            setup_approval_state=new_approval_state(),
                            proposals_state=new_proposal_state(),
                            eligibility_state=new_eligibility_state(),
                            eligibility_vendors=VENDORS,
                        )
                    ),
                    datatype=["str", "html", "str"],
                    interactive=False,
                    wrap=True,
                    row_count=(11, "fixed"),
                    column_count=(3, "fixed"),
                    label="Stage status",
                )

            with gr.TabItem("1. Intake"):
                with gr.Row():
                    project_name = gr.Textbox(label="Project / sourcing name")
                    requester_role = gr.Dropdown(
                        REQUESTER_ROLES, label="Requester role"
                    )
                with gr.Row():
                    business_area = gr.Textbox(label="Business area")
                    primary_capability = gr.Textbox(
                        label="Primary business capability"
                    )
                problem_statement = gr.Textbox(
                    label="Short problem statement", lines=2
                )
                why_now = gr.Textbox(label="Why now?", lines=2)
                desired_decision_date = gr.Textbox(
                    label="Desired decision date", placeholder="YYYY-MM-DD"
                )
                with gr.Row():
                    budget_confirmed = gr.Dropdown(
                        YES_NO_UNKNOWN, label="Budget confirmed?", value="Unknown"
                    )
                    compliance_deadline = gr.Dropdown(
                        YES_NO_UNKNOWN,
                        label="Compliance or regulatory deadline?",
                        value="Unknown",
                    )
                with gr.Row():
                    incumbent_or_preferred_vendor = gr.Dropdown(
                        YES_NO_UNKNOWN,
                        label="Existing incumbent or preferred vendor?",
                        value="Unknown",
                    )
                    existing_license_or_contract = gr.Dropdown(
                        YES_NO_UNKNOWN,
                        label="Existing licence or contract available?",
                        value="Unknown",
                    )
                save_intake_btn = gr.Button("Save intake / continue", variant="primary")
                intake_summary_md = gr.Markdown("")

                with gr.Accordion("Saved intake log (persistence check)", open=False):
                    refresh_log_btn = gr.Button("Refresh saved log")
                    intake_log_status_md = gr.Markdown("")
                    intake_log_df = gr.Dataframe(
                        headers=INTAKE_LOG_FIELDNAMES,
                        value=[],
                        datatype=["str"] * len(INTAKE_LOG_FIELDNAMES),
                        interactive=False,
                        label="Saved intake records",
                    )

            with gr.TabItem("2. Options"):
                gr.Markdown("### Candidate options")
                option_boxes = [
                    gr.Textbox(label=f"Option {i + 1}", value=name)
                    for i, name in enumerate(DEFAULT_OPTION_NAMES)
                ]
                gr.Markdown(
                    "_Next version: these options will drive the assessment columns._"
                )

            with gr.TabItem("3. Assessment Detail"):
                with gr.Row():
                    load_blank_btn = gr.Button("Load blank test")
                    load_example_btn = gr.Button("Load completed example")

                gr.Markdown("#### Capability Coverage Matrix")
                gr.Markdown(
                    "Does this option do the business capability work? "
                    f"Allowed values: {', '.join(CAPABILITY_VALUES)}. Edit cells directly."
                )
                capability_df = gr.Dataframe(
                    headers=CAPABILITY_HEADERS,
                    value=blank_capability_matrix(),
                    datatype=["str"] * len(CAPABILITY_HEADERS),
                    interactive=True,
                    row_count=(6, "fixed"),
                    column_count=(len(CAPABILITY_HEADERS), "fixed"),
                    label="Capability Coverage Matrix",
                )

                gr.Markdown("#### Baseline Viability Gate")
                gr.Markdown(
                    "Is this option safe, governable and viable enough to continue? "
                    f"Allowed values: {', '.join(VIABILITY_VALUES)}. Edit cells directly."
                )
                viability_df = gr.Dataframe(
                    headers=VIABILITY_HEADERS,
                    value=blank_viability_gate(),
                    datatype=["str"] * len(VIABILITY_HEADERS),
                    interactive=True,
                    row_count=(7, "fixed"),
                    column_count=(len(VIABILITY_HEADERS), "fixed"),
                    label="Baseline Viability Gate",
                )

            with gr.TabItem("4. Readout"):
                readout_btn = gr.Button("Generate readout", variant="primary")
                readout_md = gr.Markdown("")

            with gr.TabItem("5. Setup"):
                gr.Markdown("### Evaluation framework setup")
                gr.Markdown(SETUP_INTRO_MD)

                gr.Markdown("#### Procurement summary")
                gr.Markdown(
                    "_Restates the Intake tab's own fields — nothing is computed "
                    "or inferred here._"
                )
                setup_refresh_procurement_btn = gr.Button("Refresh from Intake")
                setup_procurement_summary_md = gr.Markdown(
                    refresh_setup_procurement_summary("", "", "", "", "")
                )

                gr.Markdown("#### Evaluation team")
                gr.Dataframe(
                    headers=["Role", "Name", "Title"],
                    value=[
                        [role, info["name"], info["title"]]
                        for role, info in EVALUATION_TEAM.items()
                    ],
                    interactive=False,
                    row_count=(len(EVALUATION_TEAM), "fixed"),
                    column_count=(3, "fixed"),
                    label="Evaluation panel",
                )

                gr.Markdown("#### Mandatory requirements")
                gr.Markdown(SETUP_GATES_INTRO_MD)
                gr.Dataframe(
                    headers=["Gate ID", "Requirement"],
                    value=[[g["id"], g["statement"]] for g in GATES],
                    interactive=False,
                    row_count=(len(GATES), "fixed"),
                    column_count=(2, "fixed"),
                    label="Mandatory requirements (gates)",
                )

                gr.Markdown("#### Scoring mode")
                gr.Markdown(SETUP_SCORING_MODE_MD)
                setup_scoring_mode_radio = gr.Radio(
                    SCORING_MODES,
                    value=DEFAULT_SCORING_MODE,
                    label="Scoring mode",
                )
                setup_weight_editor_df = gr.Dataframe(
                    headers=["ID", "Weight"],
                    value=[[c["id"], c["weight"]] for c in CRITERIA],
                    datatype=["str", "number"],
                    interactive=False,
                    row_count=(len(CRITERIA), "fixed"),
                    column_count=(2, "fixed"),
                    visible=(DEFAULT_SCORING_MODE == "Traditional weighted"),
                    label="Weights (Traditional weighted mode)",
                )

                gr.Markdown("#### Criteria and weights")
                setup_criteria_df = gr.Dataframe(
                    headers=["ID", "Domain", "Statement", "Weight"],
                    value=[
                        [c["id"], c["domain"], c["statement"], c["weight"]]
                        for c in CRITERIA
                    ],
                    datatype=["str", "str", "str", "number"],
                    interactive=True,
                    wrap=True,
                    row_count=(len(CRITERIA), "fixed"),
                    column_count=(4, "fixed"),
                    label="Criteria and weights",
                )
                setup_check_weights_btn = gr.Button("Check weights")
                setup_weight_check_md = gr.Markdown("")

                gr.Markdown("#### Scoring scale")
                gr.Dataframe(
                    headers=["Score", "Description"],
                    value=[[str(k), v] for k, v in sorted(SCORING_SCALE.items())],
                    interactive=False,
                    row_count=(len(SCORING_SCALE), "fixed"),
                    column_count=(2, "fixed"),
                    label="Scoring scale anchors",
                )

                gr.Markdown("#### Shortlist rule")
                setup_shortlist_tb = gr.Textbox(
                    value=SHORTLIST_RULE,
                    lines=4,
                    label="Shortlist rule (part of the framework being approved)",
                )

                gr.Markdown("#### Approval")
                gr.Markdown(
                    "_Approving locks criteria, weights, the shortlist rule and "
                    "scoring mode. Reopening requires a logged reason — this is "
                    "a session-only lock, not a persisted record._"
                )
                setup_approval_state = gr.State(new_approval_state())
                setup_approve_note_tb = gr.Textbox(
                    label="Approval note (optional)", lines=1
                )
                setup_approve_btn = gr.Button(
                    "Approve evaluation framework", variant="primary"
                )
                setup_approval_status_md = gr.Markdown("")

                setup_reopen_reason_tb = gr.Textbox(
                    label="Reason for reopening (required)", lines=1
                )
                setup_reopen_btn = gr.Button("Reopen framework")

                setup_approval_log_md = gr.Markdown(
                    format_approval_log(new_approval_state())
                )

            with gr.TabItem("6. Proposals"):
                gr.Markdown("### Vendor proposal readiness")
                gr.Markdown(PROPOSALS_INTRO_MD)

                gr.Markdown("#### Readiness register")
                gr.Dataframe(
                    headers=["Vendor", "Status", "Note"],
                    value=proposal_rows(VENDORS, PROPOSAL_READINESS),
                    interactive=False,
                    wrap=True,
                    row_count=(len(VENDORS), "fixed"),
                    column_count=(3, "fixed"),
                    label="Proposal readiness",
                )
                gr.Markdown(
                    "**Readiness progression:** " + " → ".join(PROPOSAL_STATUSES)
                )

                gr.Markdown("#### Confirm proposal set")
                gr.Markdown(
                    "Confirming signals that every vendor proposal intended for "
                    "this evaluation has been loaded and reviewed. This is a "
                    "session record scoped to this workbench session, not a "
                    "persisted approval."
                )
                proposals_state = gr.State(new_proposal_state())
                proposals_confirm_note_tb = gr.Textbox(
                    label="Confirmation note (optional)", lines=1
                )
                proposals_confirm_btn = gr.Button(
                    "Confirm proposal set", variant="primary"
                )
                proposals_status_md = gr.Markdown("")

                gr.Markdown("#### Reopen proposal set")
                proposals_reopen_reason_tb = gr.Textbox(
                    label="Reason for reopening (required)", lines=1
                )
                proposals_reopen_btn = gr.Button("Reopen proposal set")

                proposals_log_md = gr.Markdown(format_proposal_log(new_proposal_state()))

            with gr.TabItem("7. Eligibility"):
                gr.Markdown("### Vendor eligibility")
                gr.Markdown(ELIGIBILITY_INTRO_MD)

                gr.Markdown("#### Requirement compliance")
                gr.Dataframe(
                    headers=["Requirement"] + VENDORS,
                    value=compliance_rows(GATES, VENDORS, ELIGIBILITY_COMPLIANCE),
                    interactive=False,
                    wrap=True,
                    row_count=(len(GATES), "fixed"),
                    column_count=(1 + len(VENDORS), "fixed"),
                    label="Requirement compliance (sample data)",
                )

                gr.Markdown("#### Record eligibility outcome")
                with gr.Row():
                    eligibility_vendor_dd = gr.Dropdown(VENDORS, label="Vendor")
                    eligibility_outcome_radio = gr.Radio(
                        ELIGIBILITY_OUTCOMES, label="Outcome"
                    )
                eligibility_reason_tb = gr.Textbox(
                    label="Reason (required when Excluded, optional otherwise)",
                    lines=2,
                )
                eligibility_record_btn = gr.Button(
                    "Record eligibility outcome", variant="primary"
                )
                eligibility_status_md = gr.Markdown("")

                gr.Markdown("#### Current outcomes")
                eligibility_state = gr.State(new_eligibility_state())
                eligibility_outcomes_df = gr.Dataframe(
                    headers=["Vendor", "Outcome", "Reason"],
                    value=current_outcomes(new_eligibility_state(), VENDORS),
                    interactive=False,
                    wrap=True,
                    row_count=(len(VENDORS), "fixed"),
                    column_count=(3, "fixed"),
                    label="Current eligibility outcomes",
                )

                eligibility_log_md = gr.Markdown(
                    format_eligibility_log(new_eligibility_state())
                )

            with gr.TabItem("8. Validation"):
                gr.Markdown("### Validation questions for testers")
                gr.Markdown(VALIDATION_QUESTIONS_MD)

            with gr.TabItem("9. Compare (preview)"):
                gr.Markdown("### Side-by-side vendor comparison")
                gr.Markdown(
                    "_Preview with sample data: two mock proposals against the "
                    "customer/case scenario. Panel members score individually; "
                    "consensus is reached in the evaluation workshop and recorded "
                    "with a rationale. The tool never computes a blended winner._"
                )

                gr.Markdown("#### Mandatory gates (cannot be offset by scores)")
                gr.Dataframe(
                    headers=["Gate"] + VENDORS,
                    value=gate_rows(),
                    interactive=False,
                    label="Mandatory gates",
                )

                gr.Markdown("#### Criterion comparison")
                domain_dd = gr.Dropdown(
                    ARCHITECTURE_DOMAINS,
                    value=ARCHITECTURE_DOMAINS[0],
                    label="Architecture domain",
                )
                comparison_df = gr.Dataframe(
                    headers=["Criterion"] + VENDORS,
                    value=comparison_rows(ARCHITECTURE_DOMAINS[0]),
                    interactive=False,
                    wrap=True,
                    label="Vendor responses (evidence-linked)",
                )

                focus_md = gr.Markdown(format_focus_queue())

                gr.Markdown("#### Criterion detail and workshop consensus")
                gr.Markdown(f"_Score scale: {SCORE_SCALE}._")
                criterion_dd = gr.Dropdown(
                    [c["id"] for c in CRITERIA],
                    value=CRITERIA[0]["id"],
                    label="Criterion",
                )
                detail_md = gr.Markdown(format_criterion_detail(CRITERIA[0]["id"]))

                with gr.Row():
                    consensus_vendor_dd = gr.Dropdown(VENDORS, label="Vendor")
                    consensus_score_dd = gr.Dropdown(
                        [0, 1, 2, 3, 4, 5], label="Consensus score"
                    )
                consensus_rationale_tb = gr.Textbox(
                    label="Consensus rationale (required)", lines=2
                )
                record_consensus_btn = gr.Button(
                    "Record consensus", variant="primary"
                )
                consensus_status_md = gr.Markdown("")
                consensus_log_state = gr.State([])
                consensus_log_md = gr.Markdown(format_consensus_log([]))

        refresh_overview_btn.click(
            lambda cap, via, setup_state, prop_state, elig_state: refresh_overview(
                cap.values.tolist(),
                via.values.tolist(),
                setup_state,
                prop_state,
                elig_state,
            ),
            inputs=[
                capability_df,
                viability_df,
                setup_approval_state,
                proposals_state,
                eligibility_state,
            ],
            outputs=overview_df,
        )

        save_intake_btn.click(
            save_intake,
            inputs=[
                project_name,
                requester_role,
                business_area,
                problem_statement,
                why_now,
                primary_capability,
                desired_decision_date,
                budget_confirmed,
                compliance_deadline,
                incumbent_or_preferred_vendor,
                existing_license_or_contract,
            ],
            outputs=intake_summary_md,
        )

        refresh_log_btn.click(
            load_intake_log, outputs=[intake_log_df, intake_log_status_md]
        )

        load_blank_btn.click(
            load_blank, outputs=[capability_df, viability_df, readout_md]
        )
        load_example_btn.click(
            load_example, outputs=[capability_df, viability_df, readout_md]
        )
        readout_btn.click(
            lambda cap, via: generate_readout(cap.values.tolist(), via.values.tolist()),
            inputs=[capability_df, viability_df],
            outputs=readout_md,
        )

        setup_refresh_procurement_btn.click(
            refresh_setup_procurement_summary,
            inputs=[
                project_name,
                requester_role,
                business_area,
                problem_statement,
                desired_decision_date,
            ],
            outputs=setup_procurement_summary_md,
        )

        setup_scoring_mode_radio.change(
            lambda mode: gr.update(visible=(mode == "Traditional weighted")),
            inputs=setup_scoring_mode_radio,
            outputs=setup_weight_editor_df,
        )

        setup_check_weights_btn.click(
            check_setup_weights,
            inputs=setup_criteria_df,
            outputs=setup_weight_check_md,
        )

        setup_lock_outputs = [
            setup_approval_state,
            setup_approval_status_md,
            setup_approval_log_md,
            setup_criteria_df,
            setup_shortlist_tb,
            setup_scoring_mode_radio,
        ]

        setup_approve_btn.click(
            on_approve_setup_framework,
            inputs=[setup_approval_state, setup_approve_note_tb],
            outputs=setup_lock_outputs,
        )

        setup_reopen_btn.click(
            on_reopen_setup_framework,
            inputs=[setup_approval_state, setup_reopen_reason_tb],
            outputs=setup_lock_outputs,
        )

        proposals_lock_outputs = [
            proposals_state,
            proposals_status_md,
            proposals_log_md,
            proposals_confirm_btn,
        ]

        proposals_confirm_btn.click(
            on_confirm_proposal_set,
            inputs=[proposals_state, proposals_confirm_note_tb],
            outputs=proposals_lock_outputs,
        )

        proposals_reopen_btn.click(
            on_reopen_proposal_set,
            inputs=[proposals_state, proposals_reopen_reason_tb],
            outputs=proposals_lock_outputs,
        )

        eligibility_record_btn.click(
            on_record_eligibility,
            inputs=[
                eligibility_state,
                eligibility_vendor_dd,
                eligibility_outcome_radio,
                eligibility_reason_tb,
            ],
            outputs=[
                eligibility_state,
                eligibility_status_md,
                eligibility_outcomes_df,
                eligibility_log_md,
            ],
        )

        domain_dd.change(
            comparison_rows, inputs=domain_dd, outputs=comparison_df
        )
        criterion_dd.change(
            format_criterion_detail, inputs=criterion_dd, outputs=detail_md
        )

        def on_record_consensus(log, criterion_id, vendor, score, rationale):
            log, message = record_consensus(
                log, criterion_id, vendor, score, rationale
            )
            return log, message, format_consensus_log(log)

        record_consensus_btn.click(
            on_record_consensus,
            inputs=[
                consensus_log_state,
                criterion_dd,
                consensus_vendor_dd,
                consensus_score_dd,
                consensus_rationale_tb,
            ],
            outputs=[consensus_log_state, consensus_status_md, consensus_log_md],
        )

    return demo
