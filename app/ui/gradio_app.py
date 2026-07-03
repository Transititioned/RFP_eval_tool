"""Gradio UI for the Capability Sourcing Workbench MVP-0."""

import gradio as gr

from app.data.sample_data import (
    CAPABILITY_HEADERS,
    CAPABILITY_VALUES,
    COMPLETED_CAPABILITY_MATRIX,
    COMPLETED_VIABILITY_GATE,
    SCENARIO_SUMMARY,
    VIABILITY_HEADERS,
    VIABILITY_VALUES,
    blank_capability_matrix,
    blank_viability_gate,
)
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
    return "\n".join(lines)


def build_app():
    with gr.Blocks(title="RFP Evaluation Tool — MVP-0") as demo:
        gr.Markdown("# RFP Evaluation Tool — Capability Sourcing Workbench MVP-0")
        gr.Markdown(
            "*Evaluate the capability first. Check enterprise viability before sparkle.*"
        )
        gr.Markdown(SCENARIO_SUMMARY)

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

    return demo
