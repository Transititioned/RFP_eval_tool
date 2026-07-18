# Research Core — mission contract

Domain-neutral rules for running a research mission. Nothing in this file
is specific to any product domain; domain knowledge lives in a pack
(`research/packs/<pack>/`), and repo-specific facts live in
`research/context/`. Every research role reads this file first.

## Mission anatomy

A mission is a directory `research/missions/<slug>/`:

```
mission.md        charter: statement, decision informed, workstreams,
                  constraints, deliverable, status
state.md          restartable checkpoint — the single source of truth for
                  how far the mission has progressed
ledger.md         the structured source ledger (schema: source-ledger.md)
findings/         one file per workstream, written by its investigator
verification.md   evidence verifier's report on material claims
contrarian-review.md   contrarian researcher's challenges to the draft brief
brief.md          the decision brief — the mission's deliverable
```

`mission.md`, `state.md` and `ledger.md` exist from mission creation
(instantiate `research/missions/_template/`). The rest appear as phases
complete.

## Lifecycle

Phases, in order. Each phase ends with the Lead updating `state.md`
(phase completed, timestamp, one-line note) **before** starting the next.

1. **Plan** — Lead reads core + pack + context + `mission.md`, confirms
   workstreams and their source-ID blocks, sets status to In progress.
2. **Investigate** — Lead delegates each workstream to its investigator
   subagent **in parallel**. Workstreams must be independent: no
   investigator's input depends on another's output.
3. **Merge** — Lead merges each workstream's proposed sources into
   `ledger.md` and skims findings for contract compliance (claims
   classified, sources in-block). Non-compliant findings go back to the
   investigator, they are not silently fixed.
4. **Verify** — Lead lists the material claims (see below) and runs the
   evidence verifier over them. Verifier writes `verification.md`; claims
   that fail verification are downgraded per the evidence contract.
5. **Synthesise (draft)** — synthesist writes `brief.md` marked
   `Status: draft`, from findings + verification only (never from memory
   of sources not in the ledger).
6. **Contrarian review** — contrarian writes `contrarian-review.md`
   against the draft. Every challenge gets a written response in the
   final brief's "Objections and responses" section — accepted (brief
   changed) or rebutted (with reasons). Ignoring a challenge is not an
   option.
7. **Finalise** — synthesist updates `brief.md` to `Status: final`,
   incorporating responses. Lead sets mission status to Complete and
   reports to the user.

## Restartability

- `state.md` is rewritten at every phase boundary and records: current
  phase, phases completed, next action, and an append-only log line per
  event.
- On `/research-rfp` for an existing mission, the Lead reads `state.md`
  first and resumes from the recorded next action. Completed phases are
  never re-run unless the user asks.
- All inter-role communication goes through mission files, never through
  conversation memory — any role can be restarted cold and reconstruct
  its task from the mission directory.

## Write-ownership (prevents parallel-write conflicts)

- **Lead only**: `ledger.md`, `state.md`, `mission.md` (status field).
  One scoped exception: during the Verify phase the Lead may edit claim
  and verdict tags in findings files to apply downgrades per the
  evidence contract — each downgrade logged in `state.md`. The Lead
  never edits claim text.
- **Investigator**: only its own `findings/<workstream>.md`. Sources are
  *proposed* there using IDs from the workstream's pre-allocated block
  (e.g. WS1 = S101–S199) so merged ledger entries never collide and
  claim tags never need rewriting.
- **Verifier**: `verification.md`, plus verification tags on claims in
  findings files (runs sequentially, after all investigators finish).
- **Contrarian**: `contrarian-review.md` only.
- **Synthesist**: `brief.md` only.

## Material claims

A claim is **material** if changing its truth value would change a
recommendation in the brief. Material Evidence and Inference claims must
be verified in phase 4; Hypotheses are exempt (they carry their own
"how to validate" line instead). The Lead decides materiality — or, if
the Lead's prompt omitted the list, ratifies the verifier's proposed cut
(ratification logged in `state.md`). Either way the chosen claims are
recorded in `verification.md`'s header, so the cut is auditable.

## Claim discipline

Every material claim in findings and briefs is classified per
`research/core/evidence-contract.md` — Evidence, Inference, or
Hypothesis — using the exact tag formats defined there. Unclassified
material claims are contract violations. Enforcement is split:
`research/validate.py` machine-checks tag *format*, citation
resolution, and verdict placement across mission documents, but it
cannot detect a material claim carrying no tag at all — tag *presence*
is a human check, owned by the Lead at Merge and the verifier at Verify.

## The decision brief

`brief.md` structure (synthesist owns it):

1. **Context** — the decision this brief informs, one paragraph.
2. **What we learned** — findings that survived verification, each with
   its classification tag.
3. **Recommendations** — each mapped to the evidence that supports it
   and to the constraint set in `research/context/`. A recommendation
   that conflicts with a stated product constraint is flagged
   "requires a product decision", never presented as settled.
4. **What not to adopt** — patterns considered and rejected, with reasons.
5. **Open hypotheses** — with what would validate each.
6. **Objections and responses** — every contrarian challenge, answered.
7. **Suggested next steps** — validation actions, not implementation
   commitments.

The brief informs a human decision. It never claims the decision.
