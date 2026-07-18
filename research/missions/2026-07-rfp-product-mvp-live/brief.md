# Live product-MVP research brief

Status: final

## Decision

Build a **Guided Evaluation Workshop MVP** next. The live scan confirms that
the category baseline is a connected multi-evaluator workspace, not more
scoring mathematics. The smallest valuable increment is to let a real panel
score, see honest progress and disagreement, and move the exact disputed item
into human consensus using the logic already present.

## Category/backend capability shortlist

### C1 — Configurable evaluation framework

Common category capability; already strong locally and used as leverage.

### C2 — Live multi-evaluator scoring

Common and load-bearing; present but weak because Evaluate is read-only and
uses sample constants.

### C3 — Side-by-side response and score comparison

Common category capability; already strong, question-centred and
evidence-linked locally.

### C4 — Individual-to-consensus workflow

Common in the bounded scan; locally strong in principle but disconnected from
live individual inputs.

### C5 — Evaluator progress and controlled decision history

Common signal; retain lightweight live progress and reasoned session history,
not an enterprise workflow engine.

## Workflow/UX shortlist

### U1 — Honest stage status and next action

Emerging commercial pattern; locally partial because evaluation status cannot
yet reflect real individual scoring.

### U2 — Question-first side-by-side review

Common pattern; already strong locally and the right bridge from individual
scoring into panel discussion.

### U3 — Selected-evaluator workspace with visible progress

Common pattern; present but weak locally because the view cannot record work.

### U4 — Explicit individual-to-consensus transition

Emerging pattern; the nested views exist, but live flagged context is lost
between Compare and Moderate.

### U5 — Evidence and gaps beside the judgement

Emerging pattern; already strong locally and should remain visible through the
workshop path.

## Distinctive-feature shortlist

### D1 — Disagreement-led evaluation workshop

The strongest near-term differentiator: incomplete, divergent or low-confidence
items direct scarce human attention. High local leverage, but user value still
needs validation.

### D2 — Optional blind individual review

Uncommon and potentially useful against identity anchoring, but it should wait
until live scoring exists and can be tested without pretending full anonymity.

### D3 — Evidence-gap-to-clarification loop

Potentially valuable and better aligned than AI scoring: turn a weak evidence
cell into a follow-up task. Generated questions remain outside current scope
and require a product decision.

## Current-product delta

- **Already strong:** framework setup and lock, gates outside scoring,
  question-first comparison, evidence/gap context, consensus rationale,
  shortlist and recommendation separation.
- **Present but weak:** individual scoring, evaluator progress, honest live
  evaluation status, divergence visibility and the Compare-to-Moderate handoff.
- **Missing:** optional blind scoring.
- **Deliberately excluded:** generated clarification questions and AI input to
  scores, consensus, ranking or award decisions.
- **Poor fit:** sourcing optimisation, auto-award, full supplier portal and
  enterprise permission/workflow machinery.

## Recommended next MVP — Guided Evaluation Workshop MVP

User outcome: an evaluation panel can run one real scoring session from
individual input to focused, reasoned consensus without leaving the app or
being misled by sample progress.

| ID | Change | Smallest serious version |
|---|---|---|
| M1 | Make Evaluate a live individual workspace | Let the selected evaluator enter criterion/vendor scores into session state using the existing score shape; do not require a reason for every score. |
| M2 | Drive honest progress and next actions from live state | Reuse `evaluation_progress()` for evaluator completion, criterion completion, open gaps and variance; feed honest state to the Evaluation landing and Overview without treating progress as a vendor score. |
| M3 | Surface discussion-worthy items in Compare | Mark missing, materially divergent and low-confidence criterion/vendor cells using existing rules while preserving question-first side-by-side context. |
| M4 | Carry flagged context into Moderate | A selected flagged item opens or preselects the existing criterion/vendor moderation detail and consensus recorder; individual scores remain unchanged. |

The four changes are one workflow: M1 creates real panel input, M2 makes the
state legible, M3 identifies where human attention is valuable, and M4 turns
that signal into a reasoned decision.

## Reserve MVP — Focused stage navigation

After the live workshop is tested, consolidate the twelve-tab journey around
Setup → Proposals → Eligibility → Evaluate → Moderate → Shortlist with a
compact stage indicator and contextual next action. Reserve it because the
right navigation cannot be judged honestly until the core evaluation path is
live; do not add a wizard or break standalone tab access.

## Three things not to build now

1. A full eSourcing suite: RFP authoring, supplier portal, contracting,
   integrations or enterprise permissions.
2. AI scoring, sourcing optimisation, pairwise award scenarios, auto-shortlist
   or auto-award.
3. Blind mode or generated clarification questions before the live workshop is
   tested and the relevant product decisions are reopened deliberately.

## Validation uncertainties

- Can evaluators enter a realistic score grid comfortably in Gradio? Spike the
  smallest table/form interaction before committing to layout polish.
- Does disagreement-led navigation improve a workshop, or merely expose noise?
  Test with a scripted two- or three-evaluator session and observe what gets
  discussed.
- Is session-only state sufficient for the next proof? Treat persistence as a
  later boundary unless the test cannot be completed without it.
- Does Overview need every individual-score change, or is the Evaluation
  landing enough? Keep only the status cue that helps the next action.

## Incremental sequence

1. Add pure score-recording/state-shape logic and tests.
2. Wire selected-evaluator entry and live progress telemetry.
3. Add the simplest accessible flagged-item presentation in Compare.
4. Connect selected context to Moderate and test the complete workshop.
5. Only then decide whether focused navigation is the next MVP.

## Scan coverage

Each scout stayed within five products and five official sources. The scan
intentionally stopped after category and workflow patterns repeated. No
targeted evidence verifier was needed because the decision rests on visible,
low-cost product patterns plus direct repository fit, not a regulatory or
expensive external claim.
