# Mission: 2026-07-rfp-product-mvp-live

## Mission statement

Run the first live, bounded product-MVP scan for the Capability Sourcing
Workbench. Find the most useful category/backend capabilities, workflow and UX
patterns, and uncommon but valuable features in current buyer-side RFP
evaluation products, then select one coherent next increment.

## Decision this informs

Which 3–5 changes should a one-person build team make next so the existing RFP
evaluation proof becomes a usable evaluation workflow rather than a broader
collection of tabs and sample-data demonstrations?

## Research profile

product-mvp

## Current MVP baseline

Authoritative context: `research/context/project-context.md`, `CLAUDE.md`, the
current `app/`, and the tests. The app already has strong framework setup,
eligibility gates, evidence-linked comparison, moderation, shortlist and human
recommendation logic. Individual scoring and much of the evaluation telemetry
still consume shipped sample constants rather than user-entered session state.

## Layers in force

- Core: `research/core/`
- Profile: `research/profiles/product-mvp.md`
- Pack: `research/packs/rfp/pack.md`
- Context: `research/context/project-context.md`

## Workstreams

| ID | Role (agent) | Question | Findings file | Source-ID block |
|---|---|---|---|---|
| WS1 | category-capability-scout | Which established backend, logic and workflow capabilities define a credible small buyer-side RFP evaluation product? | `findings/ws1-category-capabilities.md` | S101–S199 |
| WS2 | workflow-ux-scout | Which current workflow and UX patterns make evaluation work understandable and actionable for a panel? | `findings/ws2-workflow-ux.md` | S201–S299 |
| WS3 | distinctive-feature-scout | Which uncommon but valuable patterns could distinguish this product without turning it into an auto-award or enterprise-suite build? | `findings/ws3-distinctive-features.md` | S301–S399 |

## Constraints

- Maximum 5 products and 5 useful sources per scout.
- Prefer current official product pages, help material and customer cases.
- Lightweight provenance only; commercial presence is a prioritisation signal,
  not proof of value.
- Do not modify the application or tests.
- Select an incremental MVP achievable by one person in the current Python +
  Gradio shape.

## Deliverable

A final product-MVP brief with at most 5 category/backend capabilities, 5
workflow/UX patterns and 3 distinctive ideas; a repository delta; one named
3–5-change next MVP; a reserve MVP; three things not to build; and clear
validation uncertainties.

## Status

Complete
