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


def load_blank():
    return blank_capability_matrix(), blank_viability_gate(), ""


def load_example():
    return (
        [list(r) for r in COMPLETED_CAPABILITY_MATRIX],
        [list(r) for r in COMPLETED_VIABILITY_GATE],
        "",
    )


def build_app():
    with gr.Blocks(title="RFP Evaluation Tool — MVP-0") as demo:
        gr.Markdown("# RFP Evaluation Tool — Capability Sourcing Workbench MVP-0")
        gr.Markdown(
            "*Evaluate the capability first. Check enterprise viability before sparkle.*"
        )

        with gr.Accordion("1. Scenario Setup", open=True):
            gr.Markdown(SCENARIO_SUMMARY)

        with gr.Row():
            load_blank_btn = gr.Button("Load blank test")
            load_example_btn = gr.Button("Load completed example")

        gr.Markdown("## 2. Capability Coverage Matrix")
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

        gr.Markdown("## 3. Baseline Viability Gate")
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

        gr.Markdown("## 4. Simple Readout")
        readout_btn = gr.Button("Generate readout", variant="primary")
        readout_md = gr.Markdown("")

        with gr.Accordion("Validation questions for testers", open=False):
            gr.Markdown(
                "1. Did any gate feel like you had already answered it in the matrix?\n"
                "2. What else would you want to check before proceeding?\n"
                "3. Does this need a score, or is reading the grid enough?\n"
                "4. Would you actually fill this in for a real sourcing decision?\n"
                "5. Who would own this artifact in your organisation?"
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
