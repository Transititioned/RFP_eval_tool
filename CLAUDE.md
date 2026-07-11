# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Product

RFP Evaluation Tool / Capability Sourcing Workbench — a decision aid for
capability-led technology sourcing. It evaluates business capability fit and
enterprise viability before vendor proposals are compared, then runs the
evaluation panel's scoring/consensus process — **without the tool ever
declaring a winner on its own.**

Core principle: evaluate the capability first; check enterprise viability
before sparkle.

This started as MVP-0 (a narrow capability/viability demonstrator — see
`docs/product_brief_mvp0.md`) and is being extended into a wider workbench
per `docs/product_decisions.md`. The 12-wave build plan referenced there is a
**north star, not a wave-by-wave contract** — prioritise by value, not by
wave order.

## Commands

```bash
# Install
pip install -r requirements.txt

# Run locally
python app.py

# Run tests (no pytest dependency — plain scripts with test_ functions)
python tests/test_readout.py
python tests/test_comparison.py
python tests/test_overview.py
python tests/test_setup.py
python tests/test_proposals.py
python tests/test_eligibility.py
python tests/test_shortlist.py
python tests/test_recommendation.py

# Deploy (after pushing to GitHub origin)
git push hf main
```

There is no lint/format/build tooling configured in this repo.

Each test file is also directly executable and self-checks all `test_*`
functions in a `if __name__ == "__main__"` block, so `python
tests/test_comparison.py` alone is a full run for that file. pytest will also
discover these files if it's installed, but it isn't a project dependency.

## Hard scope limits — do not add without asking

Role lenses, Market Clarity, bid waste reduction, vendor self-assessment,
challenger path, real document upload/parsing, AI-generated scoring or
summarisation, RFP PDF parsing, procurement workflow integrations, report
builder, broad exports, architecture repository features, generated
clarification questions, authentication, multi-tenant workspaces.

**No scoring, no weighting, no roll-ups in the Readout tab or capability/
viability grids** — the readout only restates what the grids already show.
The Evaluation/Shortlist/Recommendation tabs carry both scoring modes per
the 2026-07-11 decision: quantitative panel scores with human consensus
(default), and traditional weighted criteria scoring
(procurement-standard; mode selector and weights configured in Setup,
weighted totals computed and ranked on the Shortlist tab). In both modes the tool may compute and
display a score or ranking, but never auto-declares a winner —
"Recommended supplier" is always a separate, deliberate human action,
never an automatic rendering of the top score. See "Scoring model" below.

Intake persistence (below) is a deliberate, narrow exception to the
no-persistence rule — don't expand persistence beyond the intake log without
asking first.

This is a proof-of-concept on a **public** Hugging Face Space. It must only
ever hold synthetic/sample data, never real vendor proposals, until private
hosting is in place (see `docs/backlog.md`).

## Architecture

Python + Gradio only (not React/Vercel). Single `gr.Blocks` app with a
twelve-tab workflow shell; each tab is designed to stand alone (a user
shouldn't have to complete earlier tabs to use a later one).

```
app.py                        entry point: builds and launches the Gradio Blocks app
app/data/sample_data.py       MVP-0 scenario: options, capability/viability rows+values,
                               blank/completed sample grids
app/data/comparison_sample.py Compare/Setup sample data: vendors, evaluators, named
                               evaluation team, architecture domains, mandatory gates,
                               criteria (with weights), extracted responses
                               (evidence/confidence/gaps), panel scores, scoring scale,
                               scoring modes, shortlist rule, proposal readiness
                               register, and vendor eligibility compliance table
app/logic/overview.py         pure functions: intake log + grid values -> per-stage
                               workflow status (chip label + next recommended action)
app/logic/readout.py          pure functions: grid values -> plain-English readout text
app/logic/comparison.py       pure functions: comparison rows, gate rows, score spread,
                               focus queue, consensus recording/formatting, evaluation
                               progress telemetry, weighted_totals (Traditional weighted
                               mode), consensus_ranking (Panel + Consensus mode)
app/logic/persistence.py      appends intake records to a private HF Dataset repo (Hub API)
app/logic/setup.py            pure functions: evaluation-framework approval lock
                               (approve/reopen with reasoned, logged events) + weight
                               sum validation
app/logic/proposals.py        pure functions: proposal-set confirm/reopen state machine
                               (reasoned, logged events) + readiness display rows
app/logic/eligibility.py      pure functions: vendor eligibility outcomes — compliance
                               display rows, record_eligibility (Excluded requires a
                               reason), current outcomes, event log
app/logic/shortlist.py        pure functions: shortlist decision state machine — human
                               proposal vs mechanical ranking (divergence requires a
                               reason), approval with approver+timestamp, event log
app/logic/recommendation.py   pure functions: recommendation state machine — preferred/
                               recommended/approved supplier fields (recommended requires
                               reasons), approval, event log; never stores the computed
                               highest-scoring supplier
app/ui/gradio_app.py          the actual UI: builds all twelve tabs and wires callbacks
```

Data/logic/UI are cleanly separated: `app/data` holds static sample content,
`app/logic` holds pure functions operating on plain Python lists/dicts (no
Gradio imports, easy to unit test), and `app/ui/gradio_app.py` is the only
place that constructs Gradio components and wires `.click()`/`.change()`
handlers. When adding a feature, prefer keeping new business logic in
`app/logic` and calling it from thin UI callbacks, matching the existing
pattern (e.g. `readout_btn.click(lambda cap, via: generate_readout(...), ...)`).

### The twelve tabs

1. **Overview** — workflow status at a glance. One row per stage (Intake,
   Options, Assessment Detail, Readout, Setup, Proposals, Eligibility,
   Evaluation, Shortlist, Recommendation, Validation) with a status chip
   (Not started / In progress / Needs attention / Ready for approval /
   Complete) and a next-recommended-action line, computed by
   `stage_statuses()` in `app/logic/overview.py`. Statuses are honest and
   cheap: Intake from the persistence log, Assessment Detail / Readout from
   the live grid values, Setup from the framework approval state, Proposals
   from the confirm state, Eligibility from recorded outcomes (a user
   action — never derived from the sample compliance table), Evaluation
   from the recorded-consensus log (never from sample `PANEL_SCORES`,
   which would fabricate progress), Shortlist and Recommendation from
   their propose/approve state machines. A "Refresh status" button
   re-reads all of these. No scores, no percentages-complete, no ranking
   on this tab.
2. **Intake** — sourcing request form. "Save intake / continue" builds a
   markdown summary and calls `append_intake_record` (persistence, see
   below). Has a collapsible saved-log viewer (`load_intake_log`) to confirm
   a save landed.
3. **Options** — five editable candidate-option name textboxes. Currently a
   stub, not yet wired to the matrices below.
4. **Assessment Detail** — the original MVP-0 grids, both editable
   `gr.Dataframe` tables keyed by `OPTIONS` from `sample_data.py`:
   - **Capability Coverage Matrix**: Strong / Partial / Weak / Unknown per
     capability x option.
   - **Baseline Viability Gate**: Pass / Clarify / Fail / Unknown per check x
     option.
5. **Readout** — `generate_readout()` turns the two grids above into
   plain-English paragraphs, bucketing each option into viable / needs
   clarification / should not proceed. No scores.
6. **Setup** — evaluation framework configuration: procurement summary
   (refreshed live from Intake fields), named evaluation team
   (`EVALUATION_TEAM`), mandatory requirements (read-only view of the
   gates, outside scoring), scoring mode selector (`SCORING_MODES`, Panel +
   Consensus default; the selected mode drives the Shortlist and
   Recommendation ranking source), editable criteria/weights table with a
   `check_weights()` sum validation
   line, scoring scale anchors (`SCORING_SCALE`), and shortlist rule text.
   Centerpiece is the **approval lock** (`app/logic/setup.py`): "Approve
   evaluation framework" flips criteria/weights, shortlist rule, and
   scoring mode to read-only; editing again requires an explicit "Reopen"
   with a non-empty reason, and every approve/reopen event is timestamped
   in a visible, never-cleared log. Approval state is session-only
   (`gr.State`) — deliberately not persisted.
7. **Proposals** — supplier/proposal readiness register over `VENDORS`
   (`PROPOSAL_READINESS`: Invited / Loaded / Reviewed / Accepted into
   evaluation, sample-data status only — the tool does no document upload,
   parsing, or AI extraction and the copy must never imply it). Primary
   action "Confirm proposal set" is a confirm/reopen state machine
   (`app/logic/proposals.py`) mirroring the Setup approval lock: reopening
   requires a non-empty reason, every event is timestamped in a visible,
   never-cleared log, state is session-only.
8. **Eligibility** — vendor-level mandatory-requirement gate, distinct from
   Assessment Detail's Baseline Viability Gate (that one applies to
   OPTIONS; this one applies to VENDORS). Read-only compliance table
   (`ELIGIBILITY_COMPLIANCE`, requirement x vendor) plus a human outcome
   recorder: each vendor gets exactly one current outcome (Eligible /
   Conditionally eligible / Clarification required / Excluded) via
   `record_eligibility()` — **Excluded refuses to save without a non-empty
   reason** (same pattern as `record_consensus`). Re-recording replaces the
   current outcome but the event log keeps full history; excluded vendors
   stay visible with their reason, never removed. Outcomes are categorical,
   sit outside scoring, and are never auto-derived from the compliance
   table.
9. **Evaluation** — the product's central experience (formerly the Compare
   tab), a landing dashboard plus three nested sub-views over the sample
   vendor proposals (`comparison_sample.py`):
   - **Landing** — `evaluation_progress()` telemetry: completion %
     (process telemetry over scoring slots, not a vendor score),
     evaluators complete, criteria complete, open clarifications (from the
     `RESPONSES` gaps concept), material score variances (spread >= 2).
   - **Evaluate** — single-evaluator view: one evaluator's scores per
     criterion per vendor, read-only sample display.
   - **Compare** — the original side-by-side grid, moved as-is: mandatory
     gates separate from scoring (a gate failure can never be offset by a
     good score elsewhere); criterion-by-criterion comparison filterable
     by architecture domain, each cell carrying evidence reference +
     confidence; unanswered criteria render as `NOT ANSWERED`, never
     hidden (a missing `RESPONSES` key means "not answered").
   - **Moderate** — the original focus queue + consensus recording, moved
     as-is: score-spread drives `focus_queue()`; `record_consensus()`
     requires a non-empty rationale or it refuses to save; individual
     panel scores are never mutated by consensus.
10. **Shortlist** — mode-aware computed ranking + separate human shortlist
   decision. The ranking source follows Setup's scoring mode:
   `weighted_totals()` (Traditional weighted) or `consensus_ranking()`
   (Panel + Consensus, honest empty message when no consensus is
   recorded). Weighted totals carry per-vendor coverage (n via consensus /
   via panel mean / unscored) and the UI shows a provisional-totals
   caution when coverage is partial. The ranking is data: proposing a
   shortlist is a human action (`app/logic/shortlist.py`), and a proposal
   that differs from the mechanical ranking — including by order —
   **refuses to save without a non-empty reason**. Approval records
   approver + timestamp; re-proposing after approval clears the approval
   with an explicit logged event. The tool never auto-shortlists the top
   rank.
11. **Recommendation** — four explicitly distinct fields, never collapsed:
   Highest-scoring supplier (computed live from the active mode's ranking,
   displayed as data, never stored), then Preferred / Recommended /
   Approved supplier (all human-entered via
   `app/logic/recommendation.py`; each may differ from the others and
   from the highest score). Recording a recommendation **refuses without
   written reasons**; risks, conditions/negotiation items, and dissenting
   views are free text. Approval records approver + timestamp;
   re-recording clears approval with a logged event. No export or report
   builder — still a hard scope limit.
12. **Validation** — static standing questions for anyone testing the tool.

### Scoring model (see `docs/product_decisions.md` for full rationale)

Two scoring modes, both shipped, both bound by the same rule: the tool
may compute and display a score or ranking, but never auto-declares a
winner. The mode is selected (and locked by approval) in Setup; it drives
the ranking source used by the Shortlist and Recommendation tabs.

**Panel + Consensus (default)** — modelled on how real evaluation panels
work:
- Each evaluator scores criteria individually and quantitatively
  (`PANEL_SCORES`).
- Score divergence across evaluators (`score_spread`) is a primary
  signal — it drives `focus_queue()` ordering: gate failures -> unanswered
  criteria -> high score spread (>=2) -> low-confidence evidence.
- Consensus is a human decision entered in the evaluation workshop,
  requires a rationale, and is recorded *alongside* (never overwriting)
  individual scores.
- Ranking source: `consensus_ranking()` — sum of recorded consensus
  scores per vendor, with coverage shown as "criteria with consensus";
  an empty consensus log yields an honest "not available" message, never
  a fabricated ranking.

**Traditional weighted** — the procurement-standard model many governance
processes require and can defend to auditors:
- Ranking source: `weighted_totals()` — per vendor x criterion, the
  recorded consensus score if one exists, else the mean of individual
  panel scores, multiplied by the criterion weight and summed. Sorted
  output with per-vendor coverage (n via consensus / via panel mean /
  unscored) so a partial total is always visibly provisional.
- The total is a computed number, not a decision — "Recommended
  supplier" still requires a separate human action with rationale.

How Shortlist and Recommendation consume the ranking:
- The mechanical ranking (either mode) is display data. Proposing a
  shortlist is a separate human action; a proposal that differs from the
  mechanical top-N — including by order — requires a non-empty written
  reason (`propose_shortlist()` refuses otherwise).
- Recommendation keeps four fields distinct: Highest-scoring supplier
  (computed, never stored), and Preferred / Recommended / Approved
  supplier (human-entered; recommended requires written reasons).
- Approvals on both tabs record approver + timestamp; changing a
  proposal/recommendation after approval clears the approval with an
  explicit logged event.

Shared across both modes:
- The system never auto-declares a final winner, auto-shortlists, or
  auto-recommends.
- Mandatory gates are pass/fail-style, sit outside scoring entirely in
  both modes, and are never diluted by a good score elsewhere.

## Intake persistence

`app/logic/persistence.py` appends intake records as CSV rows to a private
Hugging Face Dataset repo via the Hub API (`HfApi.upload_file`) — no local
database, no ORM. Each save is a full read-modify-write of the CSV (download
existing rows, append, re-upload), which also gives a natural audit trail as
Dataset repo commit history.

Configured via env vars:
- `HF_TOKEN` — Space secret, required to save. Without it, saving is
  silently skipped and the UI says so explicitly — **this is expected
  behaviour when running locally without secrets, not a bug.**
- `HF_INTAKE_DATASET_REPO` — optional override; defaults to
  `Ausadmin/RFP_evaluation_tool-intake`.

Free tier by design (Hugging Face Dataset repos are free), chosen over the
$5+/month persistent storage add-on while this is a learning-stage
prototype.

## Design tone

Serious enterprise B2B, restrained, architecture-review-board credible — not
a "magic AI toy." Keep new UI copy and components consistent with that tone.

## Workflow

- Run locally: `python app.py`
- After changes: commit locally, then `git push origin main` (GitHub) and
  `git push hf main` (Hugging Face Space) to deploy.
- Keep Hugging Face Spaces compatibility: `gradio==6.19.0` pinned in
  `requirements.txt` must match the `sdk_version` in the README.md front
  matter (the Space's actual config).

## Keeping this file accurate

When editing scope, rule, or "out of scope" statements in any doc in this
repo, cross-check them against what's actually shipped (README feature
list, or the app itself) before relying on them — this project has a
history of scope docs going stale as features ship. If a rule and the
shipped code disagree, flag it rather than silently following either one.
