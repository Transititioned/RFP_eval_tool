# Decision brief: RFP-workflow-and-UX makeover for the Capability Sourcing Workbench

Status: draft

Mission: `2026-07-rfp-workflow-ux`
Audience: the repo owner, deciding which workflow/UX improvements to build
into the workbench next and in what order.

---

## 1. Context

This brief informs the repo owner's post-MVP decision on which workflow
and UX patterns from the buyer-side RFP-evaluation market are worth
building into the Capability Sourcing Workbench, mapped to specific
tabs/surfaces, and in what order — grounded in what the market and
procurement governance actually do rather than intuition. It is a
makeover brief, not a build schedule: every recommendation is a candidate
for a human build decision, and anything touching a hard scope limit or a
load-bearing product principle is flagged "requires a product decision"
rather than presented as settled. All product data stays synthetic; no
real vendor material named in the research flows into `app/data/`.

The headline finding that shapes everything below: the market's dominant
*direction of travel* — computed "award recommendations", agentic
"making an award", optimization scenarios that name a winner — runs
directly against this product's core principle that the tool never
declares a winner on its own. That makes the workbench's restraint a
deliberate market departure, and makes "What not to adopt" (§4) a
first-class part of this brief rather than an afterthought.

---

## 2. What we learned

Findings that survived verification, each with its classification tag and
(where the verifier checked it) its verdict. Claims downgraded to
Hypothesis during verification are shown as tentative in §5, never as
fact here.

### The workbench's spine already matches governance practice

- Real evaluation runs a fixed two-step sequence: each evaluator scores
  independently first, then the panel meets to reconcile — and averaging
  individual scores explicitly does **not** constitute consensus; US
  federal guidance states this verbatim [Evidence: S202]
  [Verified: 2026-07-18]. UK bid-consultancy practice documents the same
  "moderation meeting": independent scoring first, then discussion-based
  agreement rather than mechanical averaging [Evidence: S208]
  [Verified: 2026-07-18]. This maps closely onto the product's existing
  Evaluate -> Compare -> Moderate structure and its `record_consensus()`
  design [Inference: from S202, S208].
- Mandatory/eligibility criteria are screened *before* and *separately
  from* scoring: federal guidance places an initial screening step ahead
  of substantive evaluation [Evidence: S202] [Verified: 2026-07-18], and
  state guidance has the procurement officer verify responsiveness before
  distributing materials to evaluators [Evidence: S207]
  [Verified: 2026-07-18] — the same principle the product encodes as
  gates-outside-scoring [Evidence: S202, S207] [Verified: 2026-07-18].
  Legal commentary on regulated tenders independently insists pass/fail
  gate results must stay distinct from graduated scores and never be
  blended in [Evidence: S319] [Verified: 2026-07-18], validating the
  workbench's separation from a compliance angle [Inference: from S319]
  [Verified: 2026-07-18].
- Criteria and weights must be locked before proposals are seen, because
  retroactive adjustment is bias: Oregon's manual requires the scoring
  methodology finalised before the solicitation is issued [Evidence: S206]
  [Verified: 2026-07-18], and practitioner guidance is blunt that
  "finalizing criteria after proposals arrive" is the most damaging
  mistake [Evidence: S901] [Verified: 2026-07-18]. This is exactly what
  the Setup approval lock is for — not an arbitrary UX constraint but a
  defensibility requirement [Inference: from S206, S901]
  [Verified: 2026-07-18].
- Documentation is a legal artefact, and *reasoning* matters more than
  the score itself: GAO gives controlling weight to the contemporaneous
  record over after-the-fact justification, and sustains protests
  specifically for undocumented reasoning [Evidence: S203]
  [Verified: 2026-07-18]. This directly supports the product's
  reason-required design on consensus, shortlist divergence, and
  recommendation [Inference: from S203, S202] [Verified: 2026-07-18].

The practical implication: the workbench's most distinctive constraints
are not idiosyncrasies to soften — they are the parts most aligned with
how defensible evaluation actually works. The makeover should reinforce
them, not trade them away for market-common convenience.

### The market's evaluate/score/award feature set

- Individual scoring with configurable per-criterion weighting is a
  near-universal baseline, not a differentiator, across the surveyed
  buyer-side products
  [Inference: from S102, S105, S106, S110, S111, S113, S114]. SAP Ariba
  documents blind grading, weight points, and an "Enable approval for team
  grading" event rule [Evidence: S105, S106]
  [Verified: 2026-07-18].
- Consensus/moderation as an explicit step distinct from individual
  scores is clearly documented for Bonfire and SAP Ariba but not visible
  on the two smaller point tools' public pages [Evidence: S101]
  [Verified: 2026-07-18]. Bonfire's consensus score *overrides* the
  average and becomes the ranking input [Evidence: S301]
  [Verified: 2026-07-18].
- Gate-outside-scoring is a recognised market pattern: Bonfire's
  Pass/Fail criteria carry no weight [Evidence: S102], SAP Ariba separates
  gradable from non-gradable content [Evidence: S106], and public-sector
  positioning stresses compliance guardrails [Evidence: S104] — a baseline
  expectation in this segment [Inference: from S102, S104, S106].
- Comprehensive, timestamped audit logging across the whole
  evaluate-to-award lifecycle is a baseline expectation, strongest among
  public-sector-facing vendors [Evidence: S104, S107, S110, S111, S112]
  [Verified: 2026-07-18], and read together this is a segment norm rather
  than a differentiator [Inference: from S104, S107, S110, S111, S112]
  [Verified: 2026-07-18].

### Recurring UX patterns

- **Structured reason at the point of scoring.** Bonfire requires each
  evaluator to pick a predefined "Reason" (the reason set changes by
  low/medium/high score band) *plus* a free-text comment for every score
  [Evidence: S304] [Verified: 2026-07-18] — a stricter, more front-loaded
  discipline than this product, which only requires rationale at the
  consensus step [Inference: from S304]. Scorecards in the segment are
  generally dropdown/numeric grids paired with a comment field, with
  small anchored scales (e.g. 0-3 with worked example answers per level)
  [Evidence: S318].
- **Question-anchored traversal.** Vendorful recommends lining up each
  question's answers across vendors side by side (scoring one criterion
  across all vendors before moving on) to improve accuracy — the choice
  is not "grid vs document" but question-anchored vs vendor-anchored
  traversal of the same grid [Evidence: S310] [Verified: 2026-07-18]
  [Inference: from S310] [Verified: 2026-07-18]. The product's Compare
  tab is already grid-shaped and domain-filterable; the open design
  question is which traversal order the UI nudges [Inference: from S310]
  [Verified: 2026-07-18].
- **Divergence highlighting, then drill-in.** Bonfire highlights a
  criterion (orange) in the Scoring Summary when the evaluator spread
  reaches a 30% threshold, without altering any underlying score
  [Evidence: S302, S305] [Verified: 2026-07-18], and the consensus/
  moderation screen is one click away from that highlighted summary
  [Evidence: S303]. This is functionally the same signal the product
  already computes as `score_spread` driving `focus_queue()`, differing
  mainly in Bonfire's relative (%) vs the product's absolute threshold
  [Inference: from S302].
- **Process-completion telemetry, never a score.** Bonfire shows a
  per-question-set progress bar (fills green) plus an overall
  percent-complete figure keyed to *process* completion, never to a score
  [Evidence: S305] [Verified: 2026-07-18] — architecturally the same idea
  as the product's `evaluation_progress()` telemetry, and the same
  don't-conflate-progress-with-score principle [Inference: from S305].
- **Consensus alongside vs consensus as replacement.** Bonfire's
  consensus override supersedes individual scores as the ranking input
  [Evidence: S301] [Verified: 2026-07-18]; the product deliberately
  records consensus *alongside* individual scores without superseding
  them [Inference: from S301]. Both keep setting a consensus score a
  deliberate, gated human action; they differ in whether individual
  scores survive as first-class data [Inference: from S301].

### The market's award stage is where it diverges from this product

- Several competitors market a *computed* award recommendation as the
  headline evaluate/award feature: JAGGAER's Intelligent Award Navigator
  learns a user's revealed preference and converges on a recommendation
  [Evidence: S109, S110] [Verified: 2026-07-18]; Ivalua's Sourcing
  Decision Center delivers "instant, data-driven recommendations" for the
  selection decision [Evidence: S111] [Verified: 2026-07-18]; SAP Ariba
  builds optimization award scenarios ("Best Bid") and uses ML to
  recommend suppliers [Evidence: S108] [Verified: 2026-07-18]. All market
  a system-computed "optimal"/"recommended" award as the differentiating
  value [Inference: from S108, S109, S111] [Verified: 2026-07-18], and
  none frames "the tool must never declare a winner" as a design
  principle in its own right [Inference: from S108, S109, S110, S111]
  [Verified: 2026-07-18].
- The newer AI-marketed cluster pushes further: Ivalua's own copy places
  full automation up to "making an award" inside an agent's stated
  capability range, with human-in-the-loop recast as recommended best
  practice rather than a structural gate [Evidence: S316]
  [Verified: 2026-07-18]. That framing — treating ranking-to-award as one
  automatable pipeline rather than two categorically different acts — is
  exactly what this product's `recommendation.py` (never storing the
  computed highest-scoring supplier as the recommendation) is designed to
  resist [Inference: from S315, S316] [Verified: 2026-07-18], making it
  directly relevant to §4 [Inference: from S315, S316]
  [Verified: 2026-07-18].
- Not everyone in the market goes that far: Prokuria's dashboard computes
  totals but frames "choosing the winner" as a distinct human step and
  calls out that a tie requires the buyer to seek more information
  [Evidence: S312, S313], and GEP's AI evaluation agents stop at scoring,
  flagging, and summarising, leaving the decision to a human
  [Evidence: S317]. So the human-decides stance is a defensible market
  position, not a lonely one.

---

## 3. Recommendations

Each recommendation names the surface, the change, the supporting claims
(with tags and source IDs), the cost in the product's terms, and — where
relevant — Gradio feasibility and any "requires a product decision" flag.
Ordering is by evidence strength and low-risk-first, not by tab order.

### R1 — Surface the divergence signal you already compute, and link it to Moderate (Evaluation > Compare and > Moderate)

**Change.** The product already computes `score_spread` and orders
`focus_queue()` by it, but the spread is not visible *in the Compare
grid*. Add a visible marker on high-spread criteria in Compare (a flag,
badge, or cell emphasis at the existing `>= 2` threshold), and make the
Moderate focus queue reachable directly from a flagged criterion —
mirroring the market's highlight-then-drill-in adjacency.

**Support.** Bonfire's 30%-spread highlighting without altering
underlying scores [Evidence: S302, S305] [Verified: 2026-07-18]; the
moderation screen one click from the highlighted summary
[Evidence: S303]; the governance rationale that outliers should be
discussed and calibrated, not averaged away [Evidence: S202]
[Verified: 2026-07-18] [Evidence: S317]. This reinforces load-bearing
principle 2 (honest visibility) rather than conflicting with it.

**Cost.** Small logic reuse (the signal exists); UI work to render it and
wire navigation.

**Gradio feasibility.** Per-cell conditional colouring driven by a
computed threshold plausibly stretches `gr.Dataframe`'s styling API — a
feasibility spike is warranted before committing to cell-colour
specifically; a row-level flag column or a separate "flagged criteria"
list is a lower-risk fallback that needs no per-cell styling
[Hypothesis]. Validate by: a small Gradio spike testing conditional
`gr.Dataframe` styling against `gradio==6.19.0`, falling back to a flag
column if per-cell colour is not cleanly supported.

### R2 — Make question/criterion-anchored traversal the labelled default in Compare (Evaluation > Compare)

**Change.** The Compare grid is already criterion-filterable by
architecture domain. Make criterion-anchored reading the explicit,
labelled default (score one criterion across all vendors before moving
on), with the vendor-anchored view available as the alternate. This is a
framing/labelling and default-ordering change, not a new component.

**Support.** Vendorful's question-centric recommendation to improve
scoring accuracy [Evidence: S310] [Verified: 2026-07-18]; the
question-anchored vs vendor-anchored naming [Inference: from S310]
[Verified: 2026-07-18].

**Cost.** Low — mostly copy and default state; the grid exists.

**Gradio feasibility.** Achievable in Gradio (filter/sort of an existing
dataframe, matching the existing `.change()` pattern).

### R3 — Add structured reason capture at individual scoring (Evaluation > Evaluate)

**Change.** Bring a lightweight structured-justification field to the
Evaluate sub-view so an individual score can carry a short categorical
reason and/or comment, aligning individual scoring with the rationale
discipline the product already enforces at consensus. Note this changes
Evaluate from its current read-only sample display into an input surface.

**Support.** Bonfire's predefined-reason-per-score-band-plus-comment
pattern [Evidence: S304] [Verified: 2026-07-18]; the observation that
this is a more front-loaded version of the product's consensus-only
rationale [Inference: from S304]; the governance principle that written
per-score reasoning is the artefact that survives protest
[Evidence: S203] [Verified: 2026-07-18] [Inference: from S203, S202]
[Verified: 2026-07-18]; anchored small scales with example answers
[Evidence: S318].

**Cost.** Moderate — adds fields and (if made persistent) touches
session-state design. Keep it a captured reason, never a *gate* that
blocks saving an individual score, to avoid friction that governance does
not require at the individual stage.

**Gradio feasibility.** Straightforward (`gr.Textbox`/`gr.Dropdown` per
row); no platform stretch.

**Flag.** Making Evaluate an input surface (vs read-only sample) is a
product-shape decision, and any persistence of per-score reasons would
extend state beyond the current session-only/intake-log boundary —
**requires a product decision** on both counts.

### R4 — Turn Setup's scoring-scale anchors into an explicit calibration artefact (Setup)

**Change.** Enrich the existing scoring-scale anchors table with a worked
example reference answer per score level, and frame it explicitly as the
panel's calibration reference (what a given level "means") — so the
calibration step governance expects has a home in the tool rather than
being implicit.

**Support.** Anchored 0-3 scale with example answers per level
[Evidence: S318]; "skipping calibration" named among recurring scoring
errors [Evidence: S209] [Verified: 2026-07-18]. WS2 flags whether the
anchors table is already serving as the calibration artefact as an open
question, so treat the framing as the settled part and a distinct
calibration *step* as tentative (see §5).

**Cost.** Low — an extra column/field in an existing Setup table plus
copy; no new workflow stage required for the minimal version.

**Gradio feasibility.** Achievable (editable dataframe already exists in
Setup).

### R5 — Add a per-evaluator completion breakdown to the Evaluation Landing telemetry (Evaluation > Landing)

**Change.** The Landing already shows completion %, evaluators complete,
criteria complete. Add a per-evaluator completion breakdown (who has
finished, who is outstanding), matching the market's per-evaluator
progress view, while keeping everything keyed to process completion,
never to a score.

**Support.** Bonfire's per-evaluator progress bar and percent-complete
figure keyed to process not score [Evidence: S305] [Verified: 2026-07-18]
[Inference: from S305]. Directly consistent with load-bearing principle 2.

**Cost.** Low-to-moderate — telemetry breakdown over existing scoring
slots; a refresh-on-action pattern (which the product already uses) is
sufficient, so no live cross-session infrastructure is needed.

**Gradio feasibility.** Achievable with the existing "Refresh status"
refresh-on-action approach; live multi-user updates are *not* required
for this and should be avoided (see §5).

### R6 — Model evaluator conflict-of-interest attestation and pre-consensus score confidentiality (Setup / Evaluation) — requires a product decision

**Change.** Add per-evaluator COI/NDA attestation (the natural home is
Setup's evaluation-team list) and a "scores hidden until submitted"
confidentiality mechanic so individual scoring is not contaminated by
seeing others' scores first.

**Support.** Governance treats signed COI declarations and pre-consensus
rating confidentiality as standard evaluator-role requirements
[Evidence: S206] [Verified: 2026-07-18]. SAP Ariba's blind grading is the
market analogue on the confidentiality side [Evidence: S105]
[Verified: 2026-07-18].

**Cost.** Moderate-to-high — introduces new per-evaluator state and
masking logic; the confidentiality mechanic in particular implies
tracking submission state.

**Flag.** **Requires a product decision.** WS2 explicitly flags this as
an open question, not a settled recommendation, because it touches
session-state design and adds a new surface; and masked/hidden scoring
adds state the product does not currently keep. Present as a candidate to
weigh, not an approved build.

### R7 — Allow a minority/dissent record at the Moderate consensus step (Evaluation > Moderate) — requires a product decision

**Change.** Let the Moderate step optionally record a documented
minority/dissenting position alongside the agreed consensus score, for
the case where a panel cannot fully agree, rather than assuming a single
agreed score is always reachable.

**Support.** Federal guidance does not force false agreement: the record
may document "both majority conclusions and minority opinions with
supporting rationale" [Evidence: S202] [Verified: 2026-07-18]. (Note the
Recommendation tab already carries a free-text dissenting-views field;
this extends the same idea upstream to the consensus step.)

**Cost.** Moderate — extends `record_consensus()`'s data shape and UI.

**Flag.** **Requires a product decision** — it changes the consensus data
model, and how often the minority path is actually invoked in practice is
unverified (see §5), so build only if that frequency check supports it.

---

## 4. What not to adopt

Declining these market-common patterns is a deliberate product position,
not an oversight. Each is something the market does that this product
should keep rejecting.

### 4.1 Computed auto-award / "recommended supplier" as the terminus

Do not adopt a system-computed award recommendation presented as the
answer — the JAGGAER Intelligent Award Navigator preference-learning
converge-on-a-recommendation model [Evidence: S109, S110]
[Verified: 2026-07-18], Ivalua's Sourcing Decision Center "data-driven
recommendations" for the selection decision [Evidence: S111]
[Verified: 2026-07-18], and SAP Ariba's optimization award scenarios plus
ML supplier recommendations [Evidence: S108] [Verified: 2026-07-18].
These market a computed "optimal"/"recommended" winner as the headline
value [Inference: from S108, S109, S111] [Verified: 2026-07-18], and none
treats withholding the computed answer as a principle
[Inference: from S108, S109, S110, S111] [Verified: 2026-07-18]. This is
the exact pattern the workbench's "never auto-declares a winner"
principle and the four-distinct-fields Recommendation design exist to
resist — adopting it would break load-bearing principle 1.

### 4.2 Agentic "making an award" / ranking-to-award as one pipeline

Do not adopt the agentic framing where the tool goes from scoring through
to "making an award" with human review recast as optional supervision
[Evidence: S316] [Verified: 2026-07-18]. The problem is the *framing* that
ranking-to-award is a single automatable pipeline rather than two
categorically different acts [Inference: from S315, S316]
[Verified: 2026-07-18]. Any future AI work here is additionally bounded by
the staged-AI direction (synthetic-document, private-hosting-only; AI
never enters consensus, totals, rankings, shortlist, or recommendation) —
so even a decision-support-only AI feature in this area **requires a
product decision** and the private-hosting precondition, and must never
cross into the award act.

### 4.3 Consensus that supersedes and discards individual scores

Do not adopt Bonfire's consensus-as-replacement mechanic, where the
consensus score overrides the average and becomes the sole ranking input,
displacing individual scores from the ranking [Evidence: S301]
[Verified: 2026-07-18]. The product's deliberate choice is to record
consensus *alongside* individual scores as an additional first-class fact
[Inference: from S301], which preserves the audit trail governance values
[Evidence: S203] [Verified: 2026-07-18]. Keep consensus additive, not
destructive.

### 4.4 Blanket auto-scoring / AI scoring of qualitative responses

The market auto-scores objective question types (Bonfire's True/False,
Yes/No, Number responses [Evidence: S103]; Prokuria's choice-question
auto-scoring [Evidence: S312, S313]). Auto-scoring narrow *objective*
gate/quantitative fields is defensible, but extending it to qualitative
capability judgement — or any AI-generated scoring/summarisation — is a
hard scope limit in CLAUDE.md and only conceivable later under the
staged-AI, synthetic-only, private-hosting rules. Any move here
**requires a product decision**; do not import the market's
"automated scoring" framing wholesale.

### 4.5 A relative (percentage) divergence threshold copied without its own rationale

Do not swap the product's absolute `>= 2` spread threshold for Bonfire's
relative 30% threshold on precedent alone. A percentage threshold behaves
differently across scales of different widths, and no source explains why
Bonfire chose relative [Hypothesis]. Validate by: comparing %-based vs
absolute-based spread behaviour against the product's actual
`SCORING_SCALE` anchors before changing threshold style.

### 4.6 Debrief / assessment-summary generation and broad exports

Governance downstream produces regulated debrief artefacts with
prescribed content and prohibitions (FAR 15.506) [Evidence: S213], and UK
practice publishes assessment summaries. Tempting as it is to generate
these, "report builder" and "broad exports" are explicit hard scope
limits in CLAUDE.md. Do not build a debrief/report generator; if it is
ever wanted, it **requires a product decision** that reopens that scope
limit deliberately.

---

## 5. Open hypotheses

Each carries what would validate it. Several of these were downgraded from
stronger claims during verification and must be treated as tentative, not
fact.

- **Award-justification as a named, first-class authored artefact may be a
  genuine differentiator.** No surveyed competitor clearly documented a
  dedicated human-authored "award justification"/"recommendation
  rationale" module distinct from computed-score output plus audit
  logging [Hypothesis]. Validate by: reviewing product demos/docs for a
  named justification field across these products, and cross-checking
  whether that artefact is normally produced outside the eSourcing tool
  (e.g. a separate board paper). If confirmed, the workbench's free-text
  reasons on Recommendation are worth positioning as a deliberate
  strength.
- **Gradio feasibility of the richer UI patterns is unconfirmed.**
  Per-cell conditional highlighting keyed to a computed spread, a
  show/hide scoring-columns toggle, and any live multi-user grid all sit
  at varying distance from Gradio's component model [Hypothesis].
  Validate by: a small `gradio==6.19.0` spike per pattern — conditional
  `gr.Dataframe` styling for R1, a `gr.Checkbox` + `.change()` visibility
  toggle for a show/hide control, and confirming that no Evaluation-tab
  recommendation actually needs cross-session live updates (refresh-on-
  action already covers R5).
- **Absolute vs relative spread threshold** has no evidenced "right
  answer" [Hypothesis]. Validate by: the `SCORING_SCALE`-based comparison
  in §4.5.
- **A distinct calibration step (beyond enriched anchors) may or may not
  be needed.** Governance treats calibration as a named step, but whether
  Setup's anchors table already serves that purpose in practice is
  unresolved [Hypothesis]. Validate by: checking whether panels treat the
  anchors table as the calibration artefact or expect a separate
  pre-scoring walkthrough with its own record.
- **Evaluator COI/masked-scoring value vs cost is unsettled** (drives R6)
  [Hypothesis]. Validate by: checking whether any competitor surfaces
  per-evaluator masked scoring, and whether Setup's evaluator list is the
  natural home for COI attestations, before committing state design.
- **Minority-opinion frequency is unknown** (drives R7) [Hypothesis].
  Validate by: establishing whether real evaluation events invoke the
  minority/non-consensus path often enough to model, versus its being a
  rare escape valve.
- **Downgraded practitioner claims — treat as sentiment, not fact.** The
  claims that structured tools help mainly with *mechanical* consistency
  and record-keeping (not process discipline), and that a "halo
  effect"/incumbency bias is a distinct recurring panel risk, were
  downgraded during verification because they rested on a search-engine
  synthesis rather than a directly-read source [Hypothesis]. Validate by:
  tracing each to a single directly-readable practitioner source before
  any brief leans on them.
- **Downgraded market-direction claim — unconfirmed.** The description of
  Ivalua agents autonomously detecting tail-spend and triggering sourcing
  end-to-end could not be located on any fetchable Ivalua page and may be
  a search-tool artefact [Hypothesis]. Validate by: manually browsing
  Ivalua's AI-agents/agentic-sourcing pages for autonomous tail-spend
  claims. The confirmed "making an award" language (§4.2) already carries
  the market-direction point without it.
- **Downgraded governance detail — do not rely on it.** A per-evaluator
  written-comment requirement with a "reasonable, rational, and
  consistent" standard, attributed to the Maryland manual, could not be
  confirmed on that page and appears to trace to a separate appeals-board
  decision [Hypothesis]. Validate by: locating the correct source; the
  written-justification point is already independently carried by the
  verified S202/S203 claims, so nothing in §2 or §3 depends on this.

---

## 6. Objections and responses

*Placeholder — completed after contrarian review.* Every challenge raised
in `contrarian-review.md` will be recorded here and answered (accepted,
with what changed; or rebutted, with evidence-grounded reasons) before the
brief is set to `Status: final`.

---

## 7. Suggested next steps

Validation actions, not build commitments:

1. Run the Gradio feasibility spikes in §5 (conditional `gr.Dataframe`
   styling for R1; show/hide toggle; confirm no live cross-session need
   for R5) before treating R1's cell-colour variant as low-risk.
2. Sequence the low-risk, high-alignment items first: R2
   (question-anchored default) and R4 (calibration anchors) are cheap and
   reinforce existing principles; R1 and R5 follow pending the spike.
3. Hold R3, R6, R7 for an explicit product decision — each changes
   product shape or state model (R3 makes Evaluate an input surface; R6
   adds COI/masking state; R7 changes the consensus data model).
4. Resolve the two decision-relevant open questions before building their
   dependents: the award-justification differentiator check (informs how
   to position Recommendation) and the minority-opinion frequency check
   (gates R7).
5. Keep §4 as a standing "will not build" list: revisit only if the repo
   owner deliberately chooses to reopen a hard scope limit, and never as a
   drift toward the market's auto-award default.
