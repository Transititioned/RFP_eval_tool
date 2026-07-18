# Research team

An in-repo, project-scoped research capability for the Capability Sourcing
Workbench. It runs structured research missions using Claude Code subagents
and produces evidence-classified decision briefs. It never modifies the
product — research output is input to human product decisions.

## The three layers

| Layer | Location | Contents | Reusable? |
|---|---|---|---|
| **Research Core** | `research/core/` | Domain-neutral contracts: mission lifecycle, orchestration and restart rules, the evidence classification contract, the source-ledger schema | Yes — nothing in here mentions RFPs or this product |
| **RFP Product Research Pack** | `research/packs/rfp/` | Domain knowledge for researching the RFP/procurement product space: research questions, seed product list, source-quality guidance | Yes, for any RFP-domain research |
| **Local context** | `research/context/` | What *this* application actually is: shipped capabilities, decisions, constraints a brief must respect | No — specific to this repo |

Missions live in `research/missions/<slug>/` and combine all three layers.
`research/missions/_template/` is the blank mission scaffold.

## Running a mission

```
/research-rfp                      # runs/resumes the most recent mission
/research-rfp 2026-07-rfp-workflow-ux   # runs/resumes a specific mission
```

The command is the Research Lead: it plans, delegates parallel
investigations to the scout/analyst subagents, merges sources into the
mission ledger, sends material claims to the evidence verifier, runs a
contrarian review over the draft brief, and has the synthesist produce
the final decision brief. Every phase boundary is checkpointed in the
mission's `state.md`, so an interrupted mission resumes where it stopped.

The default run is deliberately cost-conscious: Sonnet specialists, an
8–12 useful-source budget per investigative workstream, saturation-based
stopping, and checkpoint-driven finalisation rather than a second full
read of the evidence corpus. A mission may exceed the source budget when a
recorded contradiction or coverage gap genuinely requires it.

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
