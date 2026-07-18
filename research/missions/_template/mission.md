# Mission: <slug>

## Mission statement

<One or two sentences: what this mission researches and why.>

## Decision this informs

<The concrete decision the deliverable feeds. If there is no decision,
there is no mission.>

## Research profile

product-mvp
<!-- product-mvp (default) | evidence-grade -->

## Current MVP baseline

<What is already shipped, partial, stubbed, deliberately excluded, and the
incremental build constraint. Link to authoritative repo context rather than
copying it.>

## Layers in force

- Core: `research/core/` (always)
- Pack: `research/packs/<pack>/pack.md`
- Context: `research/context/project-context.md`

## Workstreams

Workstreams must be independent — no workstream's input depends on another's
output. For evidence-grade missions, source-ID blocks must not overlap and
S901+ is reserved for verifier/contrarian proposals. Product-MVP missions may
retain these blocks for simple provenance but do not require claim tagging.

| ID | Role (agent) | Question | Findings file | Source-ID block |
|---|---|---|---|---|
| WS1 | <agent-name> | <the question this workstream answers> | `findings/ws1-<slug>.md` | S101–S199 |
| WS2 | <agent-name> | <question> | `findings/ws2-<slug>.md` | S201–S299 |

## Constraints

<Mission-specific constraints beyond the context layer, or "None beyond
the layers above.">

For `product-mvp`, the default hard ceilings are 5 products and 5 useful
sources per scout. State any smaller limit here. A larger limit requires an
explicitly approved follow-on mission, not silent expansion.

## Deliverable

For `product-mvp`, `brief.md` must contain no more than 5 category/backend
capabilities, 5 workflow/UX patterns, and 3 distinctive ideas; a delta against
the current product; one named 3–5-change next MVP; one reserve MVP; three
things not to build; and validation uncertainties. Add mission-specific needs
here.

## Status

Planned
<!-- Planned | In progress | Complete | Abandoned. Lead-owned. -->
