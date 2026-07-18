# Current-product fit map

Repository checked: `app/ui/gradio_app.py`, `app/logic/comparison.py`,
`app/logic/overview.py`, `app/data/comparison_sample.py`, relevant tests,
`CLAUDE.md`, product decisions and backlog.

| Candidate | Current classification | Repository evidence | Value | Leverage | Fit | Differentiation | One-person scope | Uncertainty |
|---|---|---|---|---|---|---|---|---|
| Configurable evaluation framework | Already strong | Setup supports criteria, weights, modes, mandatory requirements and reasoned approval/reopen. | High | High | High | Low | Already built | Low |
| Live multi-evaluator scoring | Present but weak | Evaluate renders one evaluator's `PANEL_SCORES` in a read-only dataframe. | High | High | High | Medium | Medium | Medium |
| Side-by-side comparison | Already strong | Compare is criterion-based, domain-filterable and carries response evidence, confidence and gaps. | High | High | High | Low | Already built | Low |
| Individual-to-consensus workflow | Present but weak | Consensus state and rationale exist, but individual inputs remain sample constants. | High | High | High | Medium | High | Low |
| Evaluator progress and decision history | Present but weak | `evaluation_progress()` accepts live mappings; UI supplies sample scores. Decision logs exist in session. | High | High | High | Medium | High | Low |
| Honest stage status and next action | Present but weak | Overview has honest stage chips/actions but Evaluation status begins only from recorded consensus, not live scoring. | High | High | High | Low | High | Low |
| Question-first side-by-side review | Already strong | Compare rows align each criterion across all vendors. | High | High | High | Low | Already built | Low |
| Selected-evaluator workspace and progress | Present but weak | Evaluator selection exists, but scoring is read-only and not a live queue. | High | High | High | Medium | Medium | Medium |
| Explicit individual-to-consensus transition | Present but weak | Evaluate, Compare and Moderate are separate nested views, but there is no live flagged-item handoff. | High | High | High | Medium | High | Low |
| Evidence and gaps in context | Already strong | Comparison and moderation detail expose summaries, references, confidence and gaps. | High | High | High | Medium | Already built | Low |
| Disagreement-led workshop | Present but weak | `score_spread()` and `focus_queue()` exist; Compare does not visibly route a live disagreement into Moderate. | High | High | High | High | High | Medium |
| Optional blind individual review | Missing | No vendor-identity masking mode; permissions/authentication are deliberately absent. | Medium | Low | Medium | Medium | Medium | High |
| Evidence-gap-to-clarification loop | Deliberately excluded | Gaps are displayed and counted, but generated clarification questions are a hard-scope product decision. | High later | Medium | High later | High | Low now | High |

## Consolidation and removals

- Live scoring, evaluator workspace, progress and stage state are one
  load-bearing capability, not separate backlog epics.
- Side-by-side comparison, framework configuration, evidence context and
  consensus recording are existing leverage; they should be connected, not
  rebuilt.
- Disagreement-led workshop combines divergence visibility and the handoff to
  existing moderation.
- Blind evaluation and generated clarifications remain hypotheses outside the
  next increment.
- Pairwise optimisation, auto-scoring and award automation were removed as
  poor fit.

## Strongest MVP ingredients

1. Session-only individual scoring in the existing evaluator view.
2. Live progress and honest next-action state derived from those scores.
3. Visible divergence in the existing question-first comparison.
4. Direct handoff of a flagged criterion/vendor into existing moderation and consensus.
