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

# Capability Sourcing Workbench

A decision aid for capability-led technology sourcing: evaluate business
capability fit and enterprise viability before comparing vendor proposals,
then run the evaluation panel's scoring and consensus process without the
tool ever declaring a winner on its own.

**Core principle:** evaluate the capability first. Check enterprise
viability before sparkle.

This started as MVP-0 (a narrow capability/viability demonstrator) and is
being extended into a wider procurement and IT-architecture evaluation
workbench per [docs/product_decisions.md](docs/product_decisions.md) and
the incremental build plan. That plan is a **north star, not a wave-by-wave
contract** — features are prioritised by value, not by the plan's order.

## What the app does today

The app opens into a guided seven-tab workflow. Each tab also stands alone —
you don't have to complete earlier tabs to use a later one.

1. **Overview** — workflow status at a glance: one row per stage (Intake,
   Options, Assessment Detail, Readout, Setup, Proposals, Eligibility,
   Evaluation, Shortlist, Recommendation, Validation) with a status chip
   (Not started / In progress / Needs attention / Ready for approval /
   Complete) and a short next-recommended-action line. Statuses are
   computed honestly from real state (the saved intake log, the current
   grid values); stages not yet built always show "Not started". A
   "Refresh status" button re-checks. No scores or completion percentages.
2. **Intake** — sourcing request fields (project name, requester role,
   business area, problem statement, why now, primary capability, decision
   date, budget/compliance/incumbent/licence flags). "Save intake /
   continue" writes a summary and appends the record to persistent
   storage (see below). A collapsed **saved intake log** viewer lets you
   confirm a save actually landed.
3. **Options** — five editable candidate-option names for the sourcing
   decision (defaults: ERP module, Case platform, Billing extension, Shiny
   AI product, Hybrid/composite option). Currently a stub — not yet wired
   to the matrices.
4. **Assessment Detail** — the original MVP-0 grids:
   - **Capability Coverage Matrix**: does each option do the business
     capability work? (Strong / Partial / Weak / Unknown)
   - **Baseline Viability Gate**: is each option safe, governable and
     viable enough to continue? (Pass / Clarify / Fail / Unknown)
   - "Load blank test" / "Load completed example" buttons; all cells
     editable.
5. **Readout** — a plain-English interpretation of the two grids above. No
   scores, no weighting, no roll-ups — it only restates what the grids
   already show, and calls out options that look viable, need
   clarification, or shouldn't proceed yet.
6. **Validation** — the five standing questions for anyone testing the
   tool (below).
7. **Compare (preview)** — side-by-side vendor comparison, the product's
   central experience, previewed against two sample vendor proposals:
   - **Mandatory gates** shown separately from scoring (data residency,
     data export, audit logging) — a gate failure can never be offset by
     a good score elsewhere.
   - **Criterion-by-criterion comparison**, filterable by architecture
     domain, with an evidence reference and confidence level per response.
     Unanswered criteria are shown as `NOT ANSWERED`, not hidden.
   - **Individual panel scores** (Business Rep / Architect / Tech PM),
     0–5 per criterion per vendor, with score-spread flagged when
     evaluators diverge.
   - **Workshop focus queue**, auto-prioritised: gate failures →
     unanswered criteria → high score spread → low-confidence evidence.
   - **Consensus recording**: a human enters a consensus score with a
     required rationale — it won't save without one. Individual scores
     are preserved unchanged alongside every consensus decision. The tool
     never computes or asserts a blended "winner."

## Scoring model

Two scoring modes, both bound by the same rule: the tool may compute and
display a score or ranking, but never auto-declares a winner. **Panel +
Consensus is shipped and the default today.** Traditional weighted was
decided on 2026-07-11 as a second, selectable mode but is **not yet
implemented** — Compare currently only offers Panel + Consensus.

**Panel + Consensus (default, shipped)** — modelled on how real evaluation
panels work, not on an aggregate formula:

- Each evaluator (Business Rep, Architecture, Tech PM, etc.) scores
  criteria individually.
- Score divergence between evaluators is a primary signal — it drives the
  workshop focus queue.
- Consensus is reached by humans in the evaluation meeting and recorded
  with a rationale — it is a decision, not a computed average.

**Traditional weighted (decided, not yet built)** — the procurement-standard
model many governance processes require and can defend to auditors:

- Criteria x weight -> total per vendor, displayed and sortable.
- The total is a computed number, not a decision — "Recommended
  supplier" still requires a separate human action with rationale.

Shared across both modes:

- Mandatory gates are pass/fail-style and sit outside scoring entirely;
  they are never diluted by a good score elsewhere.
- The system never auto-declares a final winner. "Recommended supplier"
  is always a separate, deliberate human action, never an automatic
  rendering of the top score. See the 2026-07-11 decision in
  [docs/product_decisions.md](docs/product_decisions.md) for the full
  resolution.

See [docs/product_decisions.md](docs/product_decisions.md) for the full
rationale.

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
- `app/data/comparison_sample.py` — sample vendor proposals, criteria, gates and panel scores for Compare
- `app/logic/overview.py` — per-stage workflow status for the Overview tab
- `app/logic/readout.py` — plain-English readout generation
- `app/logic/comparison.py` — comparison rows, score spread, focus queue, consensus recording
- `app/logic/persistence.py` — appends intake records to a private HF Dataset repo
- `app/ui/gradio_app.py` — Gradio UI (seven-tab workflow shell)
- `docs/` — product brief, product decisions, backlog, validation test script
- `tests/` — unit tests for readout, comparison, and overview logic

## Validation questions for testers

1. Did any gate feel like you had already answered it in the matrix?
2. What else would you want to check before proceeding?
3. Does this need a score, or is reading the grid enough?
4. Would you actually fill this in for a real sourcing decision?
5. Who would own this artifact in your organisation?

## Deliberately out of scope for now

Real document upload/parsing, AI-generated summarisation or research,
the tool auto-declaring a final winner without a separate human
recommendation action, authentication, multi-tenant workspaces, real
report exports, procurement-suite integrations. See
[docs/backlog.md](docs/backlog.md) for the full deferred list — notably,
this is a proof-of-concept on a public Hugging Face Space and should only
ever hold synthetic/sample data, not real vendor proposals, until private
hosting is in place.
