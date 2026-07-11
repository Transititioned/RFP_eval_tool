# Agent instructions

## Product

RFP Evaluation Tool / Capability Sourcing Workbench — a decision aid for
capability-led technology sourcing. Twelve-tab Gradio workflow: Overview
(per-stage status chips + next recommended action), Intake, Options,
Assessment Detail (Capability Coverage Matrix + Baseline Viability Gate),
Readout, Setup (evaluation framework: team, criteria/weights, scoring
mode, approval lock with reasoned reopen), Proposals (readiness register
+ confirm/reopen), Eligibility (vendor gate; exclusion requires a
reason), Evaluation (landing dashboard + Evaluate/Compare/Moderate
views: panel scoring, mandatory gates, consensus recording), Shortlist
(mode-aware computed ranking + separate human shortlist decision;
divergence requires a reason), Recommendation (highest-scoring computed
vs preferred/recommended/approved human-entered, reasons required), and
Validation. Core principle: evaluate the capability first; check
enterprise viability before sparkle.

## Hard scope limits — do not add

Role lenses, Market Clarity, bid waste reduction, vendor self-assessment,
challenger path, real document upload, AI-generated scoring or summarisation,
RFP PDF parsing, procurement workflow, report builder, broad exports,
architecture repository features, generated clarification questions,
authentication.

Staging note: per the 2026-07-11 future-direction decision, synthetic
(fake) RFP document upload for flow testing becomes in scope once the HF
Space is private — synthetic-data-only is the operative rule. Real vendor
documents stay excluded until enterprise controls exist.

Intake persistence is a deliberate, narrow exception (see below) — don't
read this list as still excluding it, and don't expand persistence beyond
the intake log without asking first.

Panel scores, score variance, evidence/confidence fields, human-entered
consensus roll-ups, and traditional weighted criteria scoring are **not**
on this list — they're shipped features of the Evaluation, Shortlist and
Recommendation tabs, offered as two selectable modes (Panel + Consensus,
and Traditional weighted). What's excluded is the tool auto-declaring a
winner without a separate human recommendation action. See the
2026-07-11 entry in `docs/product_decisions.md` for the full resolution.

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
- The **Readout tab** only restates the grids — no scores, no weighting, no roll-ups, and no algorithmic/automatic scoring there. That's specific to Readout, not a whole-app rule: the **Evaluation, Shortlist and Recommendation tabs** legitimately have panel scores, variance, human-entered consensus roll-ups, and (per the 2026-07-11 decision) traditional weighted criteria totals with mode-aware rankings — algorithmic scoring is permitted there, but the tool must never use it to auto-declare a winner, auto-shortlist, or auto-recommend; "Recommended supplier" is always a separate human action.
- Design tone: serious enterprise B2B, restrained, architecture-review-board credible.

## Workflow

- Run locally: `python app.py`
- After changes: commit locally, then `git push origin main` (GitHub) and
  `git push hf main` (Hugging Face Space).