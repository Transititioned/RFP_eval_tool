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
The Compare tab has quantitative panel scores with human consensus
(shipped, default), and — per the 2026-07-11 decision, not yet built — a
second traditional weighted criteria scoring mode (procurement-standard,
for processes that require it). In both modes the tool may compute and
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
six-tab workflow shell; each tab is designed to stand alone (a user shouldn't
have to complete earlier tabs to use a later one).

```
app.py                        entry point: builds and launches the Gradio Blocks app
app/data/sample_data.py       MVP-0 scenario: options, capability/viability rows+values,
                               blank/completed sample grids
app/data/comparison_sample.py Compare-tab sample data: vendors, evaluators, architecture
                               domains, mandatory gates, criteria, extracted responses
                               (evidence/confidence/gaps), and panel scores
app/logic/readout.py          pure functions: grid values -> plain-English readout text
app/logic/comparison.py       pure functions: comparison rows, gate rows, score spread,
                               focus queue, consensus recording/formatting
app/logic/persistence.py      appends intake records to a private HF Dataset repo (Hub API)
app/ui/gradio_app.py          the actual UI: builds all six tabs and wires callbacks
```

Data/logic/UI are cleanly separated: `app/data` holds static sample content,
`app/logic` holds pure functions operating on plain Python lists/dicts (no
Gradio imports, easy to unit test), and `app/ui/gradio_app.py` is the only
place that constructs Gradio components and wires `.click()`/`.change()`
handlers. When adding a feature, prefer keeping new business logic in
`app/logic` and calling it from thin UI callbacks, matching the existing
pattern (e.g. `readout_btn.click(lambda cap, via: generate_readout(...), ...)`).

### The six tabs

1. **Intake** — sourcing request form. "Save intake / continue" builds a
   markdown summary and calls `append_intake_record` (persistence, see
   below). Has a collapsible saved-log viewer (`load_intake_log`) to confirm
   a save landed.
2. **Options** — five editable candidate-option name textboxes. Currently a
   stub, not yet wired to the matrices below.
3. **Assessment Detail** — the original MVP-0 grids, both editable
   `gr.Dataframe` tables keyed by `OPTIONS` from `sample_data.py`:
   - **Capability Coverage Matrix**: Strong / Partial / Weak / Unknown per
     capability x option.
   - **Baseline Viability Gate**: Pass / Clarify / Fail / Unknown per check x
     option.
4. **Readout** — `generate_readout()` turns the two grids above into
   plain-English paragraphs, bucketing each option into viable / needs
   clarification / should not proceed. No scores.
5. **Validation** — static standing questions for anyone testing the tool.
6. **Compare (preview)** — the product's central experience, previewed
   against two sample vendor proposals (`comparison_sample.py`):
   - Mandatory gates shown separately from scoring — a gate failure can
     never be offset by a good score elsewhere.
   - Criterion-by-criterion comparison, filterable by architecture domain,
     each cell carrying evidence reference + confidence. Unanswered criteria
     render as `NOT ANSWERED`, never hidden (a missing `RESPONSES` key means
     "not answered").
   - Individual panel scores (Business Rep / Architect / Tech PM) per
     criterion per vendor, with score-spread (`max - min`) driving a
     workshop focus queue.
   - Consensus recording: `record_consensus()` requires a non-empty
     rationale or it refuses to save; individual panel scores are never
     mutated by consensus.

### Scoring model (see `docs/product_decisions.md` for full rationale)

Two scoring modes, both bound by the same rule: the tool may compute and
display a score or ranking, but never auto-declares a winner. **Panel +
Consensus is shipped and the default today.** Traditional weighted was
decided on 2026-07-11 as a second, selectable mode but is **not yet
implemented** — Compare currently only offers Panel + Consensus.

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

**Traditional weighted** — the procurement-standard model many governance
processes require and can defend to auditors:
- Criteria x weight -> total per vendor, displayed and sortable.
- The total is a computed number, not a decision — "Recommended
  supplier" still requires a separate human action with rationale.

Shared across both modes:
- The system never auto-declares a final winner.
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
