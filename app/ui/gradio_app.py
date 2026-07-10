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
    SCORE_SCALE,
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
from app.logic.persistence import FIELDNAMES as INTAKE_LOG_FIELDNAMES
from app.logic.persistence import append_intake_record, load_intake_log
from app.logic.readout import generate_readout

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


def build_app():
    with gr.Blocks(title="RFP Evaluation Tool — MVP-0") as demo:
        gr.Markdown("# Make the right sourcing call before the RFP starts.")
        gr.Markdown(
            "Save your time and make the right call. Our AI assistant will make "
            "sourcing software simple and easy. And audit trailed every step of "
            "the way."
        )

        with gr.Tabs():
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

            with gr.TabItem("5. Validation"):
                gr.Markdown("### Validation questions for testers")
                gr.Markdown(VALIDATION_QUESTIONS_MD)

            with gr.TabItem("6. Compare (preview)"):
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
