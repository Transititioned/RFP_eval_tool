# Agent instructions

## Product

RFP Evaluation Tool / Capability Sourcing Workbench MVP-0. A tiny Gradio prototype:
Capability Coverage Matrix, Baseline Viability Gate, and a plain-English readout.

Core principle: evaluate the capability first; check enterprise viability before sparkle.

## Hard scope limits — do not add

Role lenses, Market Clarity, bid waste reduction, vendor self-assessment, challenger
path, document upload, AI scoring, RFP PDF parsing, procurement workflow, report
builder, broad exports, architecture repository features, generated clarification
questions, roll-up scores, weighting, evidence fields, authentication.

Intake persistence is a deliberate, narrow exception (see below) — don't read this
list as still excluding it, and don't expand persistence beyond the intake log
without asking first.

## Intake persistence

Intake form saves append a row to a private Hugging Face Dataset repo
(`app/logic/persistence.py`), not a database. No local DB, no ORM. Configured via
env vars: `HF_TOKEN` (Space secret, required to save) and
`HF_INTAKE_DATASET_REPO` (optional override; defaults to
`Ausadmin/RFP_evaluation_tool-intake`). Without `HF_TOKEN` set (e.g. running
locally without secrets), saving is skipped and the UI says so — this is expected,
not a bug. Free tier, chosen over the $5+/month persistent storage add-on while
this is still a learning-stage prototype.

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
