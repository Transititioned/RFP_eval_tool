# Mission: 2026-07-rfp-workflow-ux

## Mission statement

Research RFP evaluation products, identify valuable workflow and UX
patterns, and produce an evidence-based makeover brief for the existing
Capability Sourcing Workbench.

## Decision this informs

The repo owner's decision on which workflow and UX improvements to build
into the workbench next (post-MVP polish direction), and in what order —
grounded in what the RFP product market actually does rather than
intuition.

## Layers in force

- Core: `research/core/` (always)
- Pack: `research/packs/rfp/pack.md`
- Context: `research/context/project-context.md`

## Workstreams

Workstreams must be independent — no workstream's input depends on
another's output. Source-ID blocks must not overlap; S901+ is reserved
for verifier/contrarian proposals.

| ID | Role (agent) | Question | Findings file | Source-ID block |
|---|---|---|---|---|
| WS1 | competitor-scout | Which products serve buyer-side RFP evaluation, and what is their feature set across the evaluate/score/award stages (individual scoring, consensus/moderation, weighting, mandatory gates, audit trail, award justification)? | `findings/ws1-competitor-landscape.md` | S101–S199 |
| WS2 | procurement-analyst | How do real evaluation panels and procurement governance actually run the evaluation stage (roles, sequence, sign-offs, mandated methodology, audit artefacts), and where do practitioners say tools help or hinder? | `findings/ws2-procurement-workflow.md` | S201–S299 |
| WS3 | ux-pattern-analyst | What recurring UX patterns do evaluation tools use for scoring input, side-by-side comparison, progress/completeness, evaluator divergence, and moderation — and which respect human-decides versus push auto-ranking? | `findings/ws3-ux-patterns.md` | S301–S399 |

## Constraints

- Recommendations must respect the load-bearing principles and hard
  constraints in `research/context/project-context.md`; anything
  touching a hard scope limit is tagged "requires a product decision".
- UX recommendations must be achievable in Gradio (or flagged as
  platform-stretching).
- Real products are named in research artefacts only; nothing flows into
  `app/data/` samples.

## Deliverable

`brief.md` — an evidence-based makeover brief following the standard
decision-brief structure, with recommendations mapped to specific
tabs/surfaces of the workbench (Overview, Setup, Evaluation
sub-views, Shortlist, Recommendation, etc.), each traced to its
supporting claims, plus a "what not to adopt" section covering
auto-ranking patterns the market uses but this product deliberately
rejects.

## Status

Complete
<!-- Planned | In progress | Complete | Abandoned. Lead-owned. -->
