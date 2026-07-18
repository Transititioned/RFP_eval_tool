# Research team

An in-repo, project-scoped research capability for the Capability Sourcing
Workbench. Its default job is evidence-informed incremental MVP selection,
not exhaustive market reporting. It never modifies the product — research
output is input to human product decisions.

## The four layers

| Layer | Location | Contents | Reusable? |
|---|---|---|---|
| **Research Core** | `research/core/` | Domain-neutral contracts: mission lifecycle, orchestration and restart rules, the evidence classification contract, the source-ledger schema | Yes — nothing in here mentions RFPs or this product |
| **RFP Product Research Pack** | `research/packs/rfp/` | Domain knowledge for researching the RFP/procurement product space: research questions, seed product list, source-quality guidance | Yes, for any RFP-domain research |
| **Local context** | `research/context/` | What *this* application actually is: shipped capabilities, decisions, constraints a brief must respect | No — specific to this repo |
| **Research profile** | `research/profiles/` | Proportional method and output contract: `product-mvp` default or optional `evidence-grade` | Yes |

Missions live in `research/missions/<slug>/` and combine all three layers.
`research/missions/_template/` is the blank mission scaffold.

## Running a mission

```
/research-rfp                      # runs/resumes the most recent mission
/research-rfp 2026-07-rfp-workflow-ux   # runs/resumes a specific mission
```

Every new mission declares a profile. `product-mvp` is the default and must
converge to a 5/5/3 shortlist plus one coherent 3–5-change next MVP.
`evidence-grade` preserves the formal ledger, verifier and contrarian process
for decisions that justify it. Every phase boundary is checkpointed in
`state.md`, so an interrupted mission resumes where it stopped.

The product-MVP ceiling is five products and five useful sources per scout,
with earlier stopping at pattern saturation. An agent cannot expand that
scope; it records a gap for a later approved mission. Formal verification is
conditional and limited to a consequential finalist claim.

Pass 1 establishes these contracts. The existing `/research-rfp` command and
agent roles are rewired to the new default in Pass 2; the completed July
mission remains valid evidence-grade history.

## Roles (see `.claude/agents/`)

- **Research Lead / orchestrator** — the `/research-rfp` command itself,
  run in the main session. Only the Lead writes `ledger.md` and `state.md`.
- **competitor-scout** — product landscape and feature patterns.
- **procurement-analyst** — real-world evaluation workflow practice and
  governance expectations.
- **ux-pattern-analyst** — UX patterns in evaluation/scoring tools.
- **evidence-verifier** — re-checks that cited sources actually support
  material claims.
- **contrarian-researcher** — challenges the draft brief before it is final.
- **product-synthesist** — merges verified findings into the decision brief.

## Validation

```
python research/validate.py
```

Deterministic structural checks over the research layers, agents, command,
and every mission (including claim-tag / ledger cross-references once a
mission has findings). No network, no dependencies.

## Boundaries

- Research artefacts are documents only. A mission never edits `app/`,
  `tests/`, or product docs.
- Research notes may name real products/vendors as **objects of study**.
  That material must never flow into `app/data/` sample content — the
  app's synthetic-data-only rule is unchanged.
- Briefs recommend; humans decide. A brief must flag any recommendation
  that would require relaxing a hard scope limit as "requires a product
  decision" rather than assuming it.
