---
title: RFP Evaluation Tool
emoji: 🗂️
colorFrom: gray
colorTo: blue
sdk: gradio
sdk_version: 6.19.0
python_version: '3.13'
app_file: app.py
pinned: false
---

# RFP Evaluation Tool — Capability Sourcing Workbench MVP-0

A minimal decision aid for capability-led technology sourcing.

**Core principle:** evaluate the capability first. Check enterprise viability before sparkle.

## What MVP-0 does

1. **Capability Coverage Matrix** — does each candidate option do the business capability work? (Strong / Partial / Weak / Unknown)
2. **Baseline Viability Gate** — is each option safe, governable and viable enough to continue? (Pass / Clarify / Fail / Unknown)
3. **Simple readout** — a plain-English interpretation of the grids. No scores, no weighting, no roll-ups.

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

## Deployment

Deployed to Hugging Face Spaces by pushing to the `hf` remote:

```bash
git push hf main
```

## Intake persistence

Saving the Intake form appends a row to a private Hugging Face Dataset repo (free
tier — no paid storage add-on). To enable it on the Space:

1. Create a private dataset repo, e.g. `Ausadmin/RFP_evaluation_tool-intake` (or
   set `HF_INTAKE_DATASET_REPO` to a different repo id).
2. Add an `HF_TOKEN` secret to the Space (Settings → Variables and secrets) with
   write access.

Without `HF_TOKEN` set — e.g. running locally without secrets — saving is skipped
and the Intake tab says so; the rest of the app still works.

## Structure

- `app.py` — entry point
- `app/data/sample_data.py` — scenario, headers, blank and completed sample grids
- `app/logic/readout.py` — plain-English readout generation
- `app/logic/persistence.py` — appends intake records to a private HF Dataset repo
- `app/ui/gradio_app.py` — Gradio UI
- `docs/` — product brief and validation test script
- `tests/` — readout logic tests

## Deliberately out of scope for MVP-0

Role lenses, market clarity, bid waste reduction, vendor self-assessment, document upload, AI scoring, RFP parsing, procurement workflow, report builder, exports, weighting, evidence fields, authentication. (Intake persistence is a narrow, deliberate exception — see above.)
