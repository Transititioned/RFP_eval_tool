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
    EVALUATORS,
    GATES,
    PANEL_SCORES,
    PROPOSAL_READINESS,
    PROPOSAL_STATUSES,
    RESPONSES,
    SCORE_SCALE,
    SCORING_MODES,
    SCORING_SCALE,
    SHORTLIST_RULE,
    VENDORS,
)
from app.logic.comparison import (
    comparison_rows,
    consensus_ranking,
    evaluation_progress,
    format_consensus_log,
    format_criterion_detail,
    format_focus_queue,
    gate_rows,
    record_consensus,
    weighted_totals,
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
from app.logic.recommendation import (
    approve_recommendation,
    current_recommendation,
    format_recommendation_log,
    new_recommendation_state,
    record_recommendation,
)
from app.logic.setup import (
    approve_framework,
    check_weights,
    format_approval_log,
    is_locked,
    new_approval_state,
    reopen_framework,
)
from app.logic.shortlist import (
    approve_shortlist,
    current_shortlist,
    format_shortlist_log,
    new_shortlist_state,
    propose_shortlist,
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

RECOMMENDATION_VENDOR_CHOICES = [""] + VENDORS

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
    "evaluation panel, not an output of this selector. This selector "
    "configures the evaluation framework; the Shortlist and Recommendation "
    "tabs read whichever mode is selected here to display the computed "
    "ranking."
)

SETUP_GATES_INTRO_MD = (
    "Requirements defined here sit outside scoring entirely and are "
    "evaluated per vendor in the Evaluation tab — a failed mandatory "
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

EVALUATION_INTRO_MD = (
    "Vendor proposals are scored against the approved criteria and "
    "mandatory gates here. Evaluators score independently; divergence "
    "between them is a primary signal, and consensus is a separate human "
    "decision recorded with a rationale. The tool never computes or "
    "asserts a blended winner."
)

EVALUATION_LANDING_GUIDANCE_MD = (
    "- **Evaluate** — review sample panel scores for one evaluator, "
    "criterion by criterion.\n"
    "- **Compare** — the side-by-side vendor comparison, filtered by "
    "architecture domain, alongside the mandatory gates.\n"
    "- **Moderate** — work the workshop focus queue and record consensus "
    "decisions."
)

EVALUATION_EVALUATE_INTRO_MD = (
    "Sample panel scores for the selected evaluator, one row per "
    "criterion. This is a read-only preview of recorded panel data — "
    "score entry here does not yet persist changes."
)

EVALUATION_COMPARE_INTRO_MD = (
    "Preview with sample data: three mock proposals against the "
    "customer/case scenario. Panel members score individually; consensus "
    "is reached in the evaluation workshop and recorded with a rationale. "
    "The tool never computes a blended winner."
)

SHORTLIST_INTRO_MD = (
    "The ranking below is computed data, produced under whichever scoring "
    "mode is selected in Setup. It never determines the shortlist by "
    "itself — shortlisting is a separate, recorded human decision made by "
    "the evaluation panel, and the tool never proposes or approves a "
    "shortlist automatically."
)

SHORTLIST_PROPOSAL_REASON_HELP = (
    "Required if your proposed shortlist differs from the computed "
    "ranking — including if only the order differs."
)

RECOMMENDATION_INTRO_MD = (
    "Four distinct fields are tracked here and never merged into one "
    "another:\n\n"
    "- **Highest-scoring supplier** — computed from the active scoring "
    "mode's ranking; this is data, not a decision.\n"
    "- **Preferred supplier** — an individual evaluator's read, which may "
    "differ from the eventual recommendation.\n"
    "- **Recommended supplier** — the evaluation panel's actual decision, "
    "which requires a written reason.\n"
    "- **Approved supplier** — a separate sign-off action recording who "
    "approved the recommendation and when.\n\n"
    "Each of these may differ from the others and from the highest-scoring "
    "supplier — the tool never substitutes one for another."
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
    consensus_log=None,
    shortlist_state=None,
    recommendation_state=None,
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
        consensus_log=consensus_log,
        shortlist_state=shortlist_state,
        recommendation_state=recommendation_state,
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


def _format_evaluation_progress_md(progress):
    """Presentation-only rendering of evaluation_progress() output.

    Restates the dict returned by app.logic.comparison.evaluation_progress()
    as markdown — no score, weighting or ranking is computed here.
    """
    evaluators_complete = progress["evaluators_complete"]
    criteria_complete = progress["criteria_complete"]
    lines = [
        "### Evaluation completeness (sample panel scores)",
        "",
        f"- **Progress:** {progress['filled_slots']} / {progress['total_slots']} "
        f"scoring slots filled ({progress['percent_complete']}%)",
        f"- **Evaluators complete:** {len(evaluators_complete)} / "
        f"{progress['evaluators_total']}"
        + (f" — {', '.join(evaluators_complete)}" if evaluators_complete else ""),
        f"- **Criteria fully scored:** {len(criteria_complete)} / "
        f"{progress['criteria_total']}"
        + (f" — {', '.join(criteria_complete)}" if criteria_complete else ""),
        f"- **Open clarifications:** {progress['open_clarifications']}",
        f"- **Material score variances (spread ≥ 2):** {progress['material_variances']}",
        "",
        "_Process telemetry over the sample panel scores — not a vendor "
        "score, ranking or aggregate._",
    ]
    return "\n".join(lines)


def refresh_evaluation_progress():
    progress = evaluation_progress(CRITERIA, VENDORS, PANEL_SCORES, RESPONSES, EVALUATORS)
    return _format_evaluation_progress_md(progress)


def evaluator_score_rows(evaluator):
    """Read-only reshape of PANEL_SCORES for one evaluator.

    Data selection only (no averaging, weighting or ranking) — there is no
    equivalent app.logic function for this exact shape, and modifying
    app/logic is out of scope for this pass, so the lookup lives here
    alongside similar existing presentation helpers (e.g. _overview_table_rows).
    """
    rows = []
    for criterion in CRITERIA:
        row = [f"{criterion['id']} — {criterion['statement']}"]
        for vendor in VENDORS:
            scores = PANEL_SCORES.get((criterion["id"], vendor), {})
            row.append(scores.get(evaluator, "—"))
        rows.append(row)
    return rows


def _ranked_vendor_order(mode, consensus_log):
    """Vendor names in ranked order under the given scoring mode.

    Thin pass-through over app.logic.comparison's ranking functions — pulls
    out just the "vendor" field in the order those functions already
    computed. No scoring or ranking decisions are made here.
    """
    if mode == "Traditional weighted":
        totals = weighted_totals(CRITERIA, VENDORS, PANEL_SCORES, consensus_log)
        return [t["vendor"] for t in totals]
    result = consensus_ranking(VENDORS, consensus_log)
    return [r["vendor"] for r in result["ranking"]]


def on_refresh_shortlist_ranking(mode, consensus_log):
    if mode == "Traditional weighted":
        totals = weighted_totals(CRITERIA, VENDORS, PANEL_SCORES, consensus_log)
        rows = [
            [t["vendor"], t["total"], t["n_consensus"], t["n_panel_mean"], t["n_unscored"]]
            for t in totals
        ]
        cautions = [
            f"- Totals are provisional: {t['n_unscored']} of {t['n_criteria']} "
            f"criteria unscored for {t['vendor']}."
            for t in totals
            if t["n_unscored"] > 0
        ]
        caution_md = "\n".join(cautions) if cautions else "_All criteria scored for every vendor._"
        mode_md = (
            "**Ranking mode: Traditional weighted.** Totals are computed "
            "data — never a declared winner."
        )
        return (
            mode_md,
            gr.update(value=rows, visible=True),
            gr.update(visible=False),
            caution_md,
        )

    result = consensus_ranking(VENDORS, consensus_log)
    mode_md = "**Ranking mode: Panel + Consensus.**"
    if result["message"]:
        return mode_md, gr.update(visible=False), gr.update(value=[], visible=True), result["message"]

    rows = [
        [r["vendor"], r["total"], r["n_consensus"], r["n_criteria"]]
        for r in result["ranking"]
    ]
    caution_md = (
        "_\"Criteria with consensus\" counts distinct criteria with any "
        "recorded consensus decision so far — not all criteria in the "
        "framework._"
    )
    return (
        mode_md,
        gr.update(visible=False),
        gr.update(value=rows, visible=True),
        caution_md,
    )


def _parse_ranked_list(text):
    return [v.strip() for v in (text or "").split(",") if v.strip()]


def _format_current_shortlist_md(shortlist):
    if not shortlist["vendors"]:
        return "_No shortlist proposed yet._"
    lines = [
        "### Current shortlist",
        "",
        f"- **Vendors (proposed order):** {', '.join(shortlist['vendors'])}",
        f"- **Matches computed ranking:** {'Yes' if shortlist['matched_mechanical'] else 'No'}",
        f"- **Reason:** {shortlist['reason'] or '— none recorded —'}",
        f"- **Approved:** {'Yes' if shortlist['approved'] else 'No'}",
    ]
    if shortlist["approved"]:
        lines.append(f"- **Approved by:** {shortlist['approver']} at {shortlist['approved_at']}")
    return "\n".join(lines)


def on_propose_shortlist(state, proposal_text, reason, mode, consensus_log):
    proposed = _parse_ranked_list(proposal_text)
    mechanical_top = _ranked_vendor_order(mode, consensus_log)[: len(proposed)]
    new_state, message = propose_shortlist(state, proposed, mechanical_top, reason)
    return (
        new_state,
        message,
        format_shortlist_log(new_state),
        _format_current_shortlist_md(current_shortlist(new_state)),
    )


def on_approve_shortlist(state, approver_name):
    new_state, message = approve_shortlist(state, approver_name)
    return (
        new_state,
        message,
        format_shortlist_log(new_state),
        _format_current_shortlist_md(current_shortlist(new_state)),
    )


def on_refresh_highest_scoring(mode, consensus_log):
    if mode == "Traditional weighted":
        totals = weighted_totals(CRITERIA, VENDORS, PANEL_SCORES, consensus_log)
        if not totals:
            return "_Highest-scoring supplier: not available — no vendors configured._"
        top = totals[0]
        return (
            f"**Highest-scoring supplier (Traditional weighted): {top['vendor']}** "
            f"— weighted total {top['total']}. This is computed data, not a "
            "recommendation."
        )

    result = consensus_ranking(VENDORS, consensus_log)
    if result["message"]:
        return "_Highest-scoring supplier (Panel + Consensus): not available — no consensus recorded._"
    top = result["ranking"][0]
    return (
        f"**Highest-scoring supplier (Panel + Consensus): {top['vendor']}** "
        f"— consensus total {top['total']}. This is computed data, not a "
        "recommendation."
    )


def _format_current_recommendation_md(rec):
    lines = [
        "### Current recommendation",
        "",
        f"- **Preferred supplier:** {rec['preferred'] or '— none recorded —'}",
        f"- **Recommended supplier:** {rec['recommended'] or '— none recorded —'}",
        f"- **Reasons:** {rec['reasons'] or '— none recorded —'}",
        f"- **Risks:** {rec['risks'] or '— none recorded —'}",
        f"- **Conditions / negotiation items:** {rec['conditions'] or '— none recorded —'}",
        f"- **Dissenting views:** {rec['dissent'] or '— none recorded —'}",
        f"- **Approved:** {'Yes' if rec['approved'] else 'No'}",
    ]
    if rec["approved"]:
        lines.append(f"- **Approved by:** {rec['approver']} at {rec['approved_at']}")
    return "\n".join(lines)


def on_record_recommendation(state, preferred, recommended, reasons, risks, conditions, dissent):
    new_state, message = record_recommendation(
        state, preferred, recommended, reasons, risks, conditions, dissent
    )
    return (
        new_state,
        message,
        format_recommendation_log(new_state),
        _format_current_recommendation_md(current_recommendation(new_state)),
    )


def on_approve_recommendation(state, approver_name):
    new_state, message = approve_recommendation(state, approver_name)
    return (
        new_state,
        message,
        format_recommendation_log(new_state),
        _format_current_recommendation_md(current_recommendation(new_state)),
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
                            consensus_log=[],
                            shortlist_state=new_shortlist_state(),
                            recommendation_state=new_recommendation_state(),
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

            with gr.TabItem("8. Evaluation"):
                gr.Markdown("### Evaluation")
                gr.Markdown(EVALUATION_INTRO_MD)

                with gr.Tabs():
                    with gr.TabItem("Landing"):
                        gr.Markdown("#### Evaluation dashboard")
                        eval_progress_refresh_btn = gr.Button("Refresh")
                        eval_progress_md = gr.Markdown(
                            _format_evaluation_progress_md(
                                evaluation_progress(
                                    CRITERIA, VENDORS, PANEL_SCORES, RESPONSES, EVALUATORS
                                )
                            )
                        )
                        gr.Markdown("#### Where to go next")
                        gr.Markdown(EVALUATION_LANDING_GUIDANCE_MD)

                    with gr.TabItem("Evaluate"):
                        gr.Markdown(EVALUATION_EVALUATE_INTRO_MD)
                        evaluator_dd = gr.Dropdown(
                            EVALUATORS, value=EVALUATORS[0], label="Evaluator"
                        )
                        evaluator_scores_df = gr.Dataframe(
                            headers=["Criterion"] + VENDORS,
                            value=evaluator_score_rows(EVALUATORS[0]),
                            interactive=False,
                            wrap=True,
                            label="Sample panel scores for this evaluator",
                        )

                    with gr.TabItem("Compare"):
                        gr.Markdown(EVALUATION_COMPARE_INTRO_MD)

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

                    with gr.TabItem("Moderate"):
                        gr.Markdown("#### Workshop focus queue")
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

            with gr.TabItem("9. Shortlist"):
                gr.Markdown("### Shortlist")
                gr.Markdown(SHORTLIST_INTRO_MD)

                gr.Markdown("#### Ranking (computed)")
                shortlist_refresh_btn = gr.Button("Refresh ranking")
                shortlist_mode_md = gr.Markdown("")
                shortlist_weighted_df = gr.Dataframe(
                    headers=[
                        "Vendor",
                        "Weighted total",
                        "Via consensus",
                        "Via panel mean",
                        "Unscored",
                    ],
                    value=[],
                    interactive=False,
                    wrap=True,
                    visible=(DEFAULT_SCORING_MODE == "Traditional weighted"),
                    label="Traditional weighted totals",
                )
                shortlist_consensus_df = gr.Dataframe(
                    headers=[
                        "Vendor",
                        "Consensus total",
                        "Criteria scored (this vendor)",
                        "Criteria with consensus",
                    ],
                    value=[],
                    interactive=False,
                    wrap=True,
                    visible=(DEFAULT_SCORING_MODE == "Panel + Consensus"),
                    label="Panel + Consensus ranking",
                )
                shortlist_caution_md = gr.Markdown("")

                gr.Markdown("#### Proposal")
                shortlist_proposal_tb = gr.Textbox(
                    label="Proposed shortlist (comma-separated, ranked highest to lowest)",
                    placeholder="e.g. Acme CaseWorks, Titan Public Sector Suite",
                )
                shortlist_reason_tb = gr.Textbox(
                    label="Reason",
                    lines=2,
                    placeholder=SHORTLIST_PROPOSAL_REASON_HELP,
                )
                shortlist_propose_btn = gr.Button("Propose shortlist", variant="primary")
                shortlist_propose_status_md = gr.Markdown("")

                gr.Markdown("#### Approval")
                shortlist_state = gr.State(new_shortlist_state())
                shortlist_current_md = gr.Markdown(
                    _format_current_shortlist_md(current_shortlist(new_shortlist_state()))
                )
                shortlist_approver_tb = gr.Textbox(label="Approver name")
                shortlist_approve_btn = gr.Button("Approve shortlist", variant="primary")
                shortlist_approve_status_md = gr.Markdown("")

                shortlist_log_md = gr.Markdown(format_shortlist_log(new_shortlist_state()))

            with gr.TabItem("10. Recommendation"):
                gr.Markdown("### Recommendation")
                gr.Markdown(RECOMMENDATION_INTRO_MD)

                gr.Markdown("#### Highest-scoring supplier (computed)")
                recommendation_highest_refresh_btn = gr.Button("Refresh")
                recommendation_highest_md = gr.Markdown(
                    "_Not refreshed yet — select a scoring mode in Setup and refresh._"
                )

                gr.Markdown("#### Human entry")
                with gr.Row():
                    recommendation_preferred_dd = gr.Dropdown(
                        RECOMMENDATION_VENDOR_CHOICES, value="", label="Preferred supplier"
                    )
                    recommendation_recommended_dd = gr.Dropdown(
                        RECOMMENDATION_VENDOR_CHOICES, value="", label="Recommended supplier"
                    )
                recommendation_reasons_tb = gr.Textbox(
                    label="Reasons (required if a supplier is recommended)", lines=2
                )
                recommendation_risks_tb = gr.Textbox(label="Risks", lines=2)
                recommendation_conditions_tb = gr.Textbox(
                    label="Conditions / negotiation items", lines=2
                )
                recommendation_dissent_tb = gr.Textbox(label="Dissenting views", lines=2)
                recommendation_record_btn = gr.Button(
                    "Record recommendation", variant="primary"
                )
                recommendation_record_status_md = gr.Markdown("")

                gr.Markdown("#### Approval")
                recommendation_state = gr.State(new_recommendation_state())
                recommendation_current_md = gr.Markdown(
                    _format_current_recommendation_md(
                        current_recommendation(new_recommendation_state())
                    )
                )
                recommendation_approver_tb = gr.Textbox(label="Approver name")
                recommendation_approve_btn = gr.Button(
                    "Approve recommendation", variant="primary"
                )
                recommendation_approve_status_md = gr.Markdown("")

                recommendation_log_md = gr.Markdown(
                    format_recommendation_log(new_recommendation_state())
                )

            with gr.TabItem("11. Validation"):
                gr.Markdown("### Validation questions for testers")
                gr.Markdown(VALIDATION_QUESTIONS_MD)

        refresh_overview_btn.click(
            lambda cap, via, setup_state, prop_state, elig_state, cons_log, sl_state, rec_state: refresh_overview(
                cap.values.tolist(),
                via.values.tolist(),
                setup_state,
                prop_state,
                elig_state,
                cons_log,
                sl_state,
                rec_state,
            ),
            inputs=[
                capability_df,
                viability_df,
                setup_approval_state,
                proposals_state,
                eligibility_state,
                consensus_log_state,
                shortlist_state,
                recommendation_state,
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

        eval_progress_refresh_btn.click(
            refresh_evaluation_progress, outputs=eval_progress_md
        )

        evaluator_dd.change(
            evaluator_score_rows, inputs=evaluator_dd, outputs=evaluator_scores_df
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

        shortlist_refresh_btn.click(
            on_refresh_shortlist_ranking,
            inputs=[setup_scoring_mode_radio, consensus_log_state],
            outputs=[
                shortlist_mode_md,
                shortlist_weighted_df,
                shortlist_consensus_df,
                shortlist_caution_md,
            ],
        )

        shortlist_propose_btn.click(
            on_propose_shortlist,
            inputs=[
                shortlist_state,
                shortlist_proposal_tb,
                shortlist_reason_tb,
                setup_scoring_mode_radio,
                consensus_log_state,
            ],
            outputs=[
                shortlist_state,
                shortlist_propose_status_md,
                shortlist_log_md,
                shortlist_current_md,
            ],
        )

        shortlist_approve_btn.click(
            on_approve_shortlist,
            inputs=[shortlist_state, shortlist_approver_tb],
            outputs=[
                shortlist_state,
                shortlist_approve_status_md,
                shortlist_log_md,
                shortlist_current_md,
            ],
        )

        recommendation_highest_refresh_btn.click(
            on_refresh_highest_scoring,
            inputs=[setup_scoring_mode_radio, consensus_log_state],
            outputs=recommendation_highest_md,
        )

        recommendation_record_btn.click(
            on_record_recommendation,
            inputs=[
                recommendation_state,
                recommendation_preferred_dd,
                recommendation_recommended_dd,
                recommendation_reasons_tb,
                recommendation_risks_tb,
                recommendation_conditions_tb,
                recommendation_dissent_tb,
            ],
            outputs=[
                recommendation_state,
                recommendation_record_status_md,
                recommendation_log_md,
                recommendation_current_md,
            ],
        )

        recommendation_approve_btn.click(
            on_approve_recommendation,
            inputs=[recommendation_state, recommendation_approver_tb],
            outputs=[
                recommendation_state,
                recommendation_approve_status_md,
                recommendation_log_md,
                recommendation_current_md,
            ],
        )

    return demo
