# Decision brief: RFP-workflow-and-UX makeover for the Capability Sourcing Workbench

Status: final

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

The headline finding that shapes everything below is narrower than the
vendors' language initially suggests. Several large platforms market
computed award recommendations, optimisation scenarios, or agentic
"making an award", but the research did not establish that shipped
products routinely record an award without a human approval action
[Inference: from S108, S109, S111, S312, S313, S315, S317]
[Verified: 2026-07-18]. The workbench is therefore resisting an
automation-oriented *market framing*, not demonstrably departing from a
shipped market norm. Its structural separation between ranking and human
decision remains worth protecting, which makes "What not to adopt" (§4)
a first-class part of this brief without overstating its uniqueness.

---

## 2. What we learned

Findings that survived verification, each with its classification tag and
(where the verifier checked it) its verdict. Claims downgraded to
Hypothesis during verification are shown as tentative in §5, never as
fact here.

### The workbench's spine aligns with defensible public-procurement practice

The governance evidence in this mission comes primarily from US and UK
public procurement. It is not a binding statement of what every private
enterprise buyer must do. It is best read as a deliberately demanding
best-practice analogue for an enterprise decision-support tool, especially
where auditability and challenge-resistance matter
[Inference: from S202, S203, S206, S207, S208, S213, S319].

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

The practical implication is conditional rather than universal: the
workbench's constraints align well with a high-assurance model of
defensible evaluation. They should be preserved because they fit the
product's chosen decision-support posture, not because this research has
proved that all enterprise buyers are legally required to use them.

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

### Observed UX patterns (evidence coverage varies)

Three mechanics below — divergence highlighting, per-score reason capture,
and detailed evaluator progress — were observed primarily in Bonfire after
the research pack explicitly nominated Bonfire for study. They are not
established as recurring market norms. In addition, several Bonfire and SAP
support pages could not be fetched directly; their mechanics were
re-derived through search results rather than independently read. Treat
those details as provisional pending a manual product-page or demo check
[Hypothesis]. Validate by: manually opening or capturing the relevant
Bonfire and SAP help pages, or confirming the mechanics in a product demo.

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

**Support.** The recommendation stands primarily on the product's own
honest-visibility principle and on making an already-computed signal useful.
Bonfire provides a provisional analogue for 30%-spread highlighting and
highlight-to-moderation adjacency [Evidence: S302, S303, S305], while public
procurement guidance supports discussing rather than averaging away
outliers [Evidence: S202] [Verified: 2026-07-18]. Bonfire is a single-vendor
example, not proof of a market norm, and its exact mechanics require the
manual confirmation described in §2 [Hypothesis]. Validate by: confirm
S302/S303/S305 directly and test the proposed treatment with evaluators;
the recommendation still survives if Bonfire's precise presentation does
not.

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

### R2 — Offer explicit question- and vendor-anchored traversal in Compare (Evaluation > Compare)

**Change.** The Compare grid is already criterion-filterable by
architecture domain. Label and offer both reading modes: question-anchored
(one criterion across all vendors) and vendor-anchored (one proposal's
coherence across criteria). Do not declare either the default until a small
usability check shows which better supports the product's capability-first
workflow. This is a framing and ordering change, not a new component.

**Support.** Vendorful advocates question-centric comparison
[Evidence: S310] [Verified: 2026-07-18], but that is vendor-authored
guidance rather than independent usability evidence. The product's own
capability-first stance supplies the counter-case for preserving a
vendor-anchored view [Inference: from S310] [Verified: 2026-07-18].

**Cost.** Low — mostly copy and default state; the grid exists.

**Gradio feasibility.** Achievable in Gradio (filter/sort of an existing
dataframe, matching the existing `.change()` pattern).

### R3 — Do not add mandatory individual-score reasons yet (moved to validation)

**Change.** Retain rationale at consensus, shortlist divergence, and
recommendation. Do not yet convert Evaluate into an input surface or require
a reason for every individual score. Test whether an optional comment solves
a real evaluator or audit problem before changing the product shape.

**Support.** Bonfire appears to capture a predefined reason plus comment at
individual scoring [Evidence: S304], but no governance source in this
mission requires written justification at that stage. S203 supports a
contemporaneous decision record, which the current consensus and downstream
reason fields already provide [Evidence: S203] [Verified: 2026-07-18].

**Cost.** Avoided for now. A future version would add interaction friction,
make the read-only Evaluate sample an input surface, and gain little audit
value unless the reasons persist.

**Validation gate.** [Hypothesis] Optional score comments may still help
moderation without becoming a mandatory governance artefact. Validate by:
observe two evaluation workshops or interview panel members about when a
pre-consensus note prevents rework; require evidence of value and a
persistence decision before building.

### R4 — Validate and optionally enrich Setup's existing calibration anchors (Setup)

**Change.** First test whether panels already understand the scoring-scale
anchors as their calibration reference. If not, add one worked example per
score level and clearer calibration copy. Treat this as optional polish, not
a proven governance gap.

**Support.** A practitioner guide uses anchored scales with example answers
[Evidence: S318], and vendor commentary warns against skipping calibration
[Evidence: S209] [Verified: 2026-07-18]. Neither establishes that this
product's existing anchors are inadequate.

**Cost.** Low — an extra column/field in an existing Setup table plus
copy; no new workflow stage required for the minimal version.

**Gradio feasibility.** Achievable (editable dataframe already exists in
Setup).

### R5 — Keep aggregate completion telemetry; test demand for named breakdowns

**Change.** Keep the current aggregate completion %, evaluators-complete and
criteria-complete telemetry. Do not add a named who-is-outstanding view
until users show that coordination value outweighs the surveillance tone.

**Support.** The only specific product example is a Bonfire-distributed
source that could not be directly read [Evidence: S305]. That is too weak
to displace a current surface which already reports aggregate progress.

**Validation gate.** [Hypothesis] A named breakdown may help an evaluation
chair chase incomplete scoring. Validate by: ask panel chairs whether the
aggregate view leaves a recurring coordination problem, and confirm the
Bonfire mechanic from a directly readable source or demo before building.

### R6 — Model evaluator conflict-of-interest attestation and pre-consensus score confidentiality (Setup / Evaluation) — requires a product decision

**Change.** Add per-evaluator COI/NDA attestation (the natural home is
Setup's evaluation-team list) and a "scores hidden until submitted"
confidentiality mechanic so individual scoring is not contaminated by
seeing others' scores first.

**Support.** Public-procurement guidance treats signed COI declarations and
pre-consensus rating confidentiality as evaluator-role requirements
[Evidence: S206] [Verified: 2026-07-18]. SAP Ariba's blind grading is a
market analogue on the confidentiality side [Evidence: S105]
[Verified: 2026-07-18]. For general enterprise buyers this is an
assurance-oriented option, not a proven universal requirement.

**Cost.** Moderate-to-high — introduces new per-evaluator state and
masking logic; the confidentiality mechanic in particular implies
tracking submission state.

**Flag.** **Requires a product decision.** WS2 explicitly flags this as
an open question, not a settled recommendation, because it touches
session-state design and adds a new surface; and masked/hidden scoring
adds state the product does not currently keep. Present as a candidate to
weigh, not an approved build.

### R7 — Do not extend the consensus model for minority opinions yet

**Change.** Keep the existing Recommendation-level dissenting-views field.
Do not extend `record_consensus()` until evidence shows mid-scale enterprise
panels need a distinct minority position at criterion level often enough to
justify the model change.

**Support.** US Army guidance permits majority and minority opinions
[Evidence: S202] [Verified: 2026-07-18], but that evidence comes from large
federal acquisition and does not establish frequency or fit for this
product's intended enterprise use.

**Cost.** Avoided for now; a future version would require a product decision
because it extends the consensus data shape and UI.

---

## 4. What not to adopt

Declining these market-common patterns is a deliberate product position,
not an oversight. Each is something the market does that this product
should keep rejecting.

### 4.1 Computed auto-award / "recommended supplier" as the terminus

Do not adopt a system-computed award recommendation presented as the
human decision — the JAGGAER Intelligent Award Navigator preference-learning
converge-on-a-recommendation model [Evidence: S109, S110]
[Verified: 2026-07-18], Ivalua's Sourcing Decision Center "data-driven
recommendations" for the selection decision [Evidence: S111]
[Verified: 2026-07-18], and SAP Ariba's optimization award scenarios plus
ML supplier recommendations [Evidence: S108] [Verified: 2026-07-18].
These market a computed "optimal"/"recommended" outcome as headline value
[Inference: from S108, S109, S111] [Verified: 2026-07-18]. The evidence
does not show that these products then record an award without human
approval. The workbench should resist collapsing calculation and decision,
while avoiding a claim that every competitor has crossed that line.

### 4.2 Agentic "making an award" / ranking-to-award as one pipeline

Do not adopt the agentic marketing framing where the tool goes from scoring
through to "making an award" [Evidence: S316] [Verified: 2026-07-18]. The
research did not establish the shipped approval mechanics behind that copy;
the problem for this product is the *framing* that
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
auto-scoring [Evidence: S312, S313]). Do not import that mechanic by
default, even for apparently objective gates: this product deliberately
requires humans to record gate and eligibility outcomes rather than deriving
them automatically from a compliance table. Any auto-derivation would
conflict with that principle and **requires a product decision**. Extending
automation to qualitative capability judgement or AI-generated scoring is
also a hard scope limit; the staged-AI direction allows evidence read-in and
cross-checks under its preconditions, never AI input to scores or decisions.

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
- **Individual-score comments may help moderation, but their value and
  persistence are unresolved** (formerly R3) [Hypothesis]. Validate by:
  observe two evaluation workshops or interview panel members about when a
  pre-consensus note prevents rework, then decide whether such notes must
  persist before turning Evaluate into an input surface.
- **Named evaluator progress may solve a chair's coordination problem, or
  merely add surveillance** (formerly R5) [Hypothesis]. Validate by: ask
  evaluation chairs whether aggregate telemetry leaves a recurring problem
  and confirm the Bonfire mechanic from a directly readable source or demo.
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

All ten challenges materially informed the final pass. None is treated as
silence or as an instruction to manufacture counter-evidence.

### C1 — Bonfire-seeded selection bias: accepted

The body no longer calls the Bonfire mechanics recurring market patterns.
§2 now identifies the pack's Bonfire seed, single-vendor coverage, and the
need for manual confirmation. R1 survives because it exposes the product's
own existing spread signal and advances honest visibility; the exact Bonfire
presentation is only a provisional analogue. R3 and R5 are no longer build
recommendations.

### C2 — Individual-score reasons add unsupported friction: accepted

R3 now recommends doing nothing until user evidence supports an optional
comment. The brief no longer claims that governance mandates a reason for
every individual score. It recognises that the defensible record is already
captured at consensus and downstream decision points, and that persistence
would be necessary before individual reasons could carry the claimed audit
benefit.

### C3 — Search re-derivation is weaker than independent verification: accepted

§2 now explicitly caveats the Bonfire and SAP mechanics that were re-derived
from search results after direct pages were blocked. R1, R3 and R5 were
narrowed accordingly. The ledger's historic verdicts remain intact as an
audit trail; the final brief no longer treats those verdicts as equivalent
to an independent manual read.

### C4 — Public-sector law was over-generalised to enterprise: accepted

§2 now frames the US/UK governance corpus as a demanding best-practice
analogue, not a binding requirement for private enterprise. R6 is presented
as an assurance-oriented product decision. R7 was moved to validation rather
than retained as an enterprise recommendation.

### C5 — Question-anchored default rested on vendor marketing: accepted

R2 now offers both question- and vendor-anchored traversal and requires a
small usability check before choosing a default. This preserves the
capability-first case for reading a whole proposal while still testing the
comparison efficiency claimed by Vendorful.

### C6 — Auto-award direction overstated shipped behaviour: accepted

§1 and §4 now distinguish automation-oriented marketing language from
confirmed shipped behaviour. The research supports protecting the boundary
between computed ranking and human decision; it does not support claiming
that unattended award is the dominant shipped norm or that the workbench is
unique in retaining human choice.

### C7 — Per-evaluator progress is weak and potentially managerial: accepted

R5 now preserves aggregate telemetry. A named breakdown is an open
hypothesis gated on a real coordination problem and direct confirmation of
the reference mechanic.

### C8 — Objective auto-scoring contradicted the human gate rule: accepted

§4.4 now rejects automatic gate derivation by default. Even apparently
objective auto-scoring would require an explicit product decision because
Eligibility and viability outcomes are deliberately human-recorded.

### C9 — Calibration enrichment may duplicate the existing anchors: accepted

R4 is now optional polish. The first action is to test whether the existing
anchors already function as the panel's calibration artefact; enrichment is
conditional on a demonstrated comprehension gap.

### C10 — Minority opinions were imported from very large federal procurement: accepted

R7 now recommends no consensus-model change. Criterion-level minority
positions remain a hypothesis until mid-scale enterprise evidence shows
they occur often enough to justify new state and UI; the existing
Recommendation dissent field remains the current outlet.

---

## 7. Suggested next steps

Validation actions, not build commitments:

1. Run a small Gradio spike for R1's spread marker. Prefer a flag column or
   flagged-criteria list if conditional dataframe styling is awkward.
2. Usability-test R2's two traversal modes before selecting a default.
3. Check whether Setup's existing anchors already calibrate users; enrich
   them only if R4's comprehension gap is observed.
4. Hold R3, R5 and R7 as validation questions, not backlog commitments.
   Treat R6 as the only larger candidate requiring a deliberate product and
   state-model decision.
5. Resolve the award-justification differentiator hypothesis before using
   it in positioning, and retain §4 as a standing boundary against collapsing
   computed analysis into human gate, shortlist, recommendation or award.
