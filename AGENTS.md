# Agent instructions

## Product

RFP Evaluation Tool / Capability Sourcing Workbench MVP-0. A tiny Gradio prototype:
Capability Coverage Matrix, Baseline Viability Gate, and a plain-English readout.

Core principle: evaluate the capability first; check enterprise viability before sparkle.

## Hard scope limits — do not add

Role lenses, Market Clarity, bid waste reduction, vendor self-assessment, challenger
path, document upload, AI scoring, RFP PDF parsing, procurement workflow, report
builder, broad exports, architecture repository features, generated clarification
questions, roll-up scores, weighting, evidence fields, authentication, database
persistence.

## Implementation rules

- Python + Gradio only. Not React/Vercel.
- Prefer simple readable Python over clever abstractions.
- Keep Hugging Face Spaces compatibility (pinned `gradio==6.19.0`, matching the Space `sdk_version` in README.md).
- No scoring, no weighting, no roll-ups anywhere. The readout only restates the grids.
- Design tone: serious enterprise B2B, restrained, architecture-review-board credible.

## Workflow

- Run locally: `python app.py`
- After changes: commit locally, then `git push origin main` (GitHub) and
  `git push hf main` (Hugging Face Space).
