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

The app opens into a guided twelve-tab workflow. Each tab also stands
alone — you don't have to complete earlier tabs to use a later one.

1. **Overview** — workflow status at a glance: one row per stage (Intake,
   Options, Assessment Detail, Readout, Setup, Proposals, Eligibility,
   Evaluation, Shortlist, Recommendation, Validation) with a status chip
   (Not started / In progress / Needs attention / Ready for approval /
   Complete) and a short next-recommended-action line. Statuses are
   computed honestly from real state (the saved intake log, the current
   grid values, the Setup approval state, the proposal-set confirmation,
   recorded eligibility outcomes, recorded consensus, and the shortlist
   and recommendation decisions). A "Refresh status" button re-checks. No
   scores or completion percentages on this tab.
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
6. **Setup** — evaluation framework configuration: a procurement summary
   refreshed live from the Intake fields, the named evaluation panel,
   mandatory requirements (shown outside scoring), a scoring mode
   selector (Panel + Consensus, default, or Traditional weighted — per
   the 2026-07-11 decision; the weighted-totals view in Compare is not
   built yet), an editable criteria-and-weights table with a
   weights-sum check, the 0–5 scoring scale anchors, and the shortlist
   rule. **Approving the evaluation framework locks it**: criteria,
   weights, scoring mode, and shortlist rule become read-only, and any
   change afterwards requires an explicit "Reopen" with a stated reason
   — every approve/reopen event is timestamped in a visible audit log.
   This is what prevents weights being quietly retuned after proposals
   arrive.
7. **Proposals** — a supplier/proposal readiness register over the sample
   vendors (Invited / Loaded / Reviewed / Accepted into evaluation). This
   is sample-data status only — the tool does not upload, parse, or
   extract documents. "Confirm proposal set" records the confirmation
   with a timestamped audit log; reopening the set afterwards requires a
   stated reason, same as the Setup approval lock.
8. **Eligibility** — a vendor-level mandatory-requirements gate, distinct
   from Assessment Detail's Baseline Viability Gate (that gate assesses
   options; this one assesses vendor proposals). Shows a requirement ×
   vendor compliance table, and lets a human record exactly one outcome
   per vendor: Eligible, Conditionally eligible, Clarification required,
   or Excluded — **recording an exclusion requires a stated reason**, and
   excluded vendors stay visible with that reason rather than
   disappearing. Outcomes sit outside scoring: an exclusion is never
   offset by good scores, and the tool never derives an outcome from the
   compliance table on its own.
9. **Evaluation** — the product's central experience (formerly the
   Compare tab): a landing dashboard plus three working views, previewed
   against the sample vendor proposals:
   - **Landing** — evaluation completeness at a glance: progress %
     (process telemetry, not a vendor score), evaluators complete,
     criteria complete, open clarifications, and material score
     variances.
   - **Evaluate** — a single evaluator's scores per criterion per vendor
     (read-only sample view).
   - **Compare** — the side-by-side grid: mandatory gates shown
     separately from scoring (a gate failure can never be offset by a
     good score elsewhere); criterion-by-criterion comparison filterable
     by architecture domain, with evidence reference and confidence per
     response; unanswered criteria shown as `NOT ANSWERED`, not hidden.
   - **Moderate** — the workshop focus queue (gate failures → unanswered
     criteria → high score spread → low-confidence evidence) and
     consensus recording: a human enters a consensus score with a
     required rationale — it won't save without one; individual scores
     are preserved unchanged alongside every consensus decision.
10. **Shortlist** — a computed, mode-aware ranking (consensus totals or
   weighted totals, per the Setup scoring mode) shown side by side with a
   separate human shortlist decision. Weighted totals always show their
   coverage (how many criteria came from consensus, panel means, or are
   unscored) with a caution when provisional. Proposing a shortlist that
   differs from the computed ranking — including by order — **requires a
   written reason**; approval records who approved and when; changing an
   approved shortlist clears the approval with a logged event. The tool
   never auto-shortlists the top-ranked supplier.
11. **Recommendation** — four explicitly separate fields: Highest-scoring
   supplier (computed, shown as data only), and Preferred, Recommended,
   and Approved supplier (all human-entered; each can differ from the
   others and from the highest score). Recording a recommendation
   **requires written reasons**; risks, conditions/negotiation items, and
   dissenting views are captured as free text. No export or report
   builder.
12. **Validation** — the five standing questions for anyone testing the
   tool (below).

## Scoring model

Two scoring modes, both shipped, both bound by the same rule: the tool
may compute and display a score or ranking, but never auto-declares a
winner. The mode is chosen (and locked by approval) in Setup, and it
determines the ranking shown on the Shortlist and Recommendation tabs.

**Panel + Consensus (default)** — modelled on how real evaluation
panels work, not on an aggregate formula:

- Each evaluator (Business Rep, Architecture, Tech PM, etc.) scores
  criteria individually.
- Score divergence between evaluators is a primary signal — it drives the
  workshop focus queue.
- Consensus is reached by humans in the evaluation meeting and recorded
  with a rationale — it is a decision, not a computed average.
- Its ranking is the sum of recorded consensus scores per vendor; with no
  consensus recorded yet, the tool says so rather than inventing one.

**Traditional weighted** — the procurement-standard model many governance
processes require and can defend to auditors:

- Criteria x weight -> total per vendor, displayed and sortable. Each
  criterion uses its recorded consensus score where one exists, otherwise
  the mean of the individual panel scores; unscored criteria are counted
  and disclosed so a partial total is always visibly provisional.
- The total is a computed number, not a decision — "Recommended
  supplier" still requires a separate human action with rationale.

How Shortlist and Recommendation use the ranking: the ranking is data.
The shortlist is a separate human proposal (a divergence from the
computed ranking requires a written reason), and the recommendation
keeps Highest-scoring / Preferred / Recommended / Approved supplier as
four distinct fields — the tool never converts a top rank into a
shortlist entry or a recommendation on its own.

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
- `app/data/comparison_sample.py` — sample vendor proposals, criteria (with weights), gates, panel scores, evaluation team, scoring scale/modes, shortlist rule, proposal readiness and eligibility compliance for Compare, Setup, Proposals and Eligibility
- `app/logic/overview.py` — per-stage workflow status for the Overview tab
- `app/logic/setup.py` — evaluation-framework approval lock and weights-sum check
- `app/logic/proposals.py` — proposal-set confirm/reopen state machine and readiness rows
- `app/logic/eligibility.py` — vendor eligibility outcomes (exclusion requires a reason)
- `app/logic/shortlist.py` — shortlist proposal/approval state machine (divergence from the computed ranking requires a reason)
- `app/logic/recommendation.py` — recommendation state machine (recommended supplier requires written reasons)
- `app/logic/readout.py` — plain-English readout generation
- `app/logic/comparison.py` — comparison rows, score spread, focus queue, consensus recording
- `app/logic/persistence.py` — appends intake records to a private HF Dataset repo
- `app/ui/gradio_app.py` — Gradio UI (twelve-tab workflow shell)
- `docs/` — product brief, product decisions, backlog, validation test script
- `tests/` — unit tests for readout, comparison, overview, setup, proposals, eligibility, shortlist, and recommendation logic

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
