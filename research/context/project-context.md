# Project context — Capability Sourcing Workbench

What research roles need to know about *this* application. Concise by
design; the authoritative sources are `CLAUDE.md`, `README.md`,
`docs/product_decisions.md`, and `docs/backlog.md` in the repo root —
consult them before relying on a detail that matters, and treat them as
overriding this summary if they disagree.

## What the product is

A decision aid for capability-led technology sourcing (Python + Gradio,
proof-of-concept on a Hugging Face Space). It evaluates business
capability fit and enterprise viability before vendor proposals are
compared, then runs the evaluation panel's scoring/consensus process —
**without the tool ever declaring a winner on its own**. Core principle:
evaluate the capability first; check enterprise viability before sparkle.

## Shipped surface (as of 2026-07-18)

A twelve-tab workflow; each tab stands alone: Overview (per-stage status
chips), Intake (persisted to a private HF dataset — the one persistence
exception), Options, Assessment Detail (capability coverage matrix +
baseline viability gate), Readout (plain-English restatement, no scores
ever), Setup (criteria/weights, scoring-mode selector, approval lock
with reasoned reopen), Proposals (readiness register, no upload),
Eligibility (vendor gate; exclusion requires a reason), Evaluation
(landing dashboard + Evaluate/Compare/Moderate: panel scores, mandatory
gates outside scoring, focus queue, consensus with required rationale),
Shortlist (mode-aware computed ranking + separate human decision;
divergence requires a reason), Recommendation (highest-scoring shown as
data; preferred/recommended/approved human-entered with reasons), and
Validation (standing tester questions). All data is synthetic sample
data; state is session-only except the intake log.

## Load-bearing product principles

A makeover brief must work *with* these, and flag (not assume away) any
recommendation that conflicts:

1. **Decision support, never decision making.** Scores and rankings may
   be computed and displayed, but shortlisting and recommending are
   always separate, deliberate human actions with written reasons. No
   auto-winner, auto-shortlist, or auto-recommendation — ever.
2. **Honest visibility.** Unanswered criteria render as `NOT ANSWERED`;
   partial weighted totals are labelled provisional; empty consensus
   yields "not available", never a fabricated ranking; Overview shows no
   fake progress.
3. **Gates outside scoring.** Mandatory/eligibility gate failures are
   never diluted or offset by good scores.
4. **Reasons and audit.** Destructive or divergent actions (reopen after
   approval, exclusion, ranking divergence, recommendation) require
   written reasons; state machines keep timestamped, never-cleared logs.
5. **Restrained tone.** Serious enterprise B2B,
   architecture-review-board credible — not a "magic AI toy".

## Hard constraints on recommendations

- **Hard scope limits** (CLAUDE.md): role lenses, market clarity, bid
  waste reduction, vendor self-assessment, challenger path, real
  document upload/parsing, AI scoring/summarisation, RFP PDF parsing,
  procurement workflow integrations, report builder, broad exports,
  architecture repository features, generated clarification questions,
  authentication, multi-tenant workspaces. A brief may *discuss* these
  as market observations but must tag any recommendation touching them
  "requires a product decision".
- **Staged AI direction** (decision 2026-07-11): synthetic-document
  upload + AI evidence read-in with human verification becomes in scope
  once the Space is private; AI cross-check lenses later; AI never
  enters consensus, totals, rankings, shortlist or recommendation.
- **Tech shape**: Python + Gradio single Blocks app, no React, pinned
  `gradio==6.19.0`, HF Spaces compatible, no databases, persistence
  limited to the intake log. UX recommendations must be achievable in
  Gradio or be flagged as platform-stretching.
- **Synthetic data only** on the public Space; real vendor names/data
  never enter `app/data/` samples (research notes naming real products
  are fine — they stay in `research/`).

## What a makeover brief is for

The initial mission's deliverable is an evidence-based *makeover brief*:
workflow and UX patterns from the RFP product space worth adopting,
mapped to specific tabs/surfaces of this app, respecting everything
above. It informs the repo owner's build decisions; it does not schedule
or implement them.
