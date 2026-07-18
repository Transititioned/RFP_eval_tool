# Research Core — common mission contract

Domain-neutral rules shared by every research mission. Domain knowledge lives
in a pack (`research/packs/<pack>/`), repository facts live in
`research/context/`, and the mission selects a profile from
`research/profiles/`.

## Default purpose

The default profile is **product-mvp**. Its job is to help a small build team
choose the next coherent product increment:

> Find the strongest established backend/workflow capabilities, the most
> useful workflow and UX patterns, and a small number of valuable distinctive
> ideas; map them against the current product; select one achievable next MVP.

Research volume is not an outcome. A useful mission ends in a product choice.

Use **evidence-grade** only when the decision genuinely needs claim-by-claim
verification: governance, regulation, vendor selection, externally published
market claims, or an expensive/irreversible decision whose conclusion depends
on contested evidence.

## Mission anatomy

A mission is a directory under `research/missions/<slug>/` with:

- `mission.md` — profile, decision, current-MVP baseline, workstreams, limits,
  required output and status.
- `state.md` — restartable phase checkpoint and append-only activity log.
- one findings file per independent scout/workstream.
- `brief.md` — the final decision artefact.
- profile-specific working artefacts defined in `research/profiles/`.

Existing evidence-grade missions may also contain a detailed source ledger,
verification report and contrarian review. Product-MVP missions use a compact
observation/feature matrix instead.

## Common lifecycle

1. **Plan** — read core, selected profile, pack, context and mission. Confirm
   the decision is concrete and the workstreams are independent.
2. **Investigate** — run independent scouts in parallel within the mission's
   explicit product and source ceilings.
3. **Combine** — normalise different vendor names for the same capability or
   UX pattern; retain provenance and disagreement.
4. **Map** — compare candidates with the current product: strong, partial,
   missing, deliberately excluded, or poor fit.
5. **Select** — converge to the profile's candidate limits and assemble one
   coherent recommendation.
6. **Challenge** — use the selected profile's proportional challenge gate.
7. **Finalise** — answer material challenges, set the brief final, set the
   mission Complete, validate, and stop. Do not implement recommendations.

The evidence-grade profile adds formal Merge, Verify, Draft and Contrarian
phases. Its existing lifecycle remains defined in
`research/profiles/evidence-grade.md`.

## Restartability

- `state.md` is the truth. Update it at every phase boundary before starting
  the next phase.
- Resume the recorded next action; never rerun a completed phase merely to
  rebuild context.
- All inter-role communication is written to mission files so an interrupted
  role can restart cold.

## Write ownership

- Lead only: mission status, `state.md`, shared candidate/observation matrix.
- Each scout: only its declared findings file.
- Fit mapper/synthesist: the brief and profile-defined synthesis artefacts.
- Conditional verifier/contrarian: only their named review artefact.
- No research role modifies `app/`, `tests/`, or product documentation.

## Common quality rules

- Read the current product before looking for additions.
- Commercial implementation is a prioritisation signal, not proof of user
  value. Record what was observed and where.
- Separate a category pattern from a single-product curiosity.
- Do not confuse a missing feature with a valuable feature.
- Prefer strengthening a weak shipped capability when it creates more value
  than adding another surface.
- A recommendation must state the user problem, current-product delta,
  expected value, scope/effort, uncertainty and smallest serious version.
- A set of unrelated high-scoring features is not an MVP. The final bundle
  must produce one intelligible user outcome.
- Briefs recommend; humans decide.

## Profile selection

Every new `mission.md` declares:

```text
## Research profile

product-mvp
```

Allowed profiles:

- `product-mvp` — default; incremental product feature and MVP selection.
- `evidence-grade` — formal verification for high-stakes claims/decisions.

If the profile is absent on a historical mission, treat it as
`evidence-grade`; do not rewrite completed mission history.
