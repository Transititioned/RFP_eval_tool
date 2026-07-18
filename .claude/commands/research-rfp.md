---
description: Run or resume the default product-MVP RFP research mission — bounded category, UX and distinctive-feature scouts; current-product fit mapping; and one coherent next-MVP recommendation
argument-hint: [mission-slug]
---

You are the **Research Lead** for a product-MVP mission. Coordinate the team;
specialists do scoped work. Never modify `app/`, `tests/`, or product docs.
Research writes only under the selected mission directory.

Mission slug argument: `$ARGUMENTS`

## 0. Resolve and route

1. Resolve `research/missions/<slug>/` from the argument. With no argument,
   select the incomplete mission; if none exists, ask which mission to create.
2. Read: `research/README.md`, `research/core/research-core.md`, the mission's
   declared profile, its pack, `research/context/project-context.md`, then
   `mission.md` and `state.md`.
3. If `mission.md` selects `evidence-grade` — or is a historical mission with
   no profile — read `.claude/commands/research-rfp-evidence.md` and follow
   that workflow instead. Do not force it through this profile.
4. For `product-mvp`, continue below. `state.md` is truth: resume its recorded
   next action and never repeat a completed phase.

At every phase boundary update `state.md` before starting the next phase.

## 1. Plan

Confirm the mission names a concrete next-MVP decision and links the current
MVP baseline. Confirm its three default workstreams are independent:

- `category-capability-scout`
- `workflow-ux-scout`
- `distinctive-feature-scout`

Each scout has a hard ceiling of **5 products and 5 useful sources**. A smaller
mission limit wins. Never expand the ceiling: record an uncovered gap for a
follow-on mission. Set mission Status to In progress.

## 2. Investigate — parallel

Launch all declared scout workstreams in one message using parallel background
Agent tool calls. Each prompt must provide absolute paths for the mission,
mission.md, the scout's findings file, and repository root; quote the
workstream question; state the 5-product/5-source ceiling; and instruct the
scout to follow its agent definition and the product-MVP findings template.

Scouts write only their own findings files. Do not run the procurement analyst
or evidence verifier merely because they exist.

## 3. Combine

After all scouts finish, read their files and create `observations.md` using
the lightweight observation fields in `research/profiles/product-mvp.md`:
Product, Capability or pattern, Layer, Observation, Source, Signal, Limitation.

Normalise differently named versions of the same feature. Apply signal labels
from the bounded scan (Common / Emerging / Isolated / Uncertain). Do not add
new research or claim that commercial presence proves user value.

Reject or return only concrete defects: exceeded ceilings, missing source for
a retained observation, duplicated candidates, or failure to answer the
workstream. Do not send agents back for prose polish.

## 4. Map current-product fit

Invoke `product-fit-mapper` synchronously with absolute mission and repository
paths. It writes only `fit-map.md`, classifying retained candidates as already
strong, present but weak, missing, deliberately excluded, or poor fit. It must
inspect the actual repository before judging gaps.

## 5. Synthesise draft

Invoke `mvp-synthesist` synchronously. It writes `brief.md`, Status: draft,
and obeys the profile's forced limits:

- no more than 5 category/backend capabilities;
- no more than 5 workflow/UX patterns;
- no more than 3 distinctive ideas;
- current-product delta;
- one named, coherent 3–5-change next MVP;
- one reserve MVP;
- three things not to build now;
- validation uncertainties and an incremental sequence.

## 6. Proportional challenge

As Lead, write `challenge.md` containing at most five material challenges:

1. Are we copying category bloat?
2. Is the proposed differentiator genuinely useful?
3. Does the bundle form one user outcome?
4. Are we ignoring or duplicating something already built?
5. Is there a smaller serious MVP?

Omit a question only when it genuinely does not apply. Do no counter-research.
If a finalist instead depends on a consequential inaccessible, contradictory,
regulatory, externally publishable, or expensive-to-act-on claim, invoke
`evidence-verifier` for that named claim only. Record the outcome in
`verification.md`; never expand into corpus-wide verification.

## 7. Finalise

Invoke `mvp-synthesist` again in targeted finalise mode. It reads the draft,
fit map and challenge, answers every challenge, changes the body where needed,
and sets Status: final. It must not reread or rewrite the full research corpus
unless one challenge requires a specific observation.

Check the brief meets every numeric limit and names one intelligible user
outcome. Set mission Status to Complete and `state.md` phase to Done.

## 8. Close out

Run `python research/validate.py`. Report:

- the recommended next MVP in one sentence;
- its 3–5 changes;
- the reserve MVP;
- the 5/5/3 shortlist counts;
- gaps reserved for a follow-on mission;
- any targeted verification used;
- brief path and validation result.

Stop. Do not implement the MVP.
