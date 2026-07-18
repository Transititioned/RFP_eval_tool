# Findings: WS2 — How real evaluation panels and procurement governance run the evaluation stage

## Question

How do real evaluation panels and procurement governance actually run the
evaluation stage (roles, sequence, sign-offs, mandated methodology, audit
artefacts), and where do practitioners say tools help or hinder?

## Summary

Across US federal, US state, and UK public-sector guidance, evaluation
follows a strikingly consistent shape: named roles with separated duties
(procurement officer/contracting officer as process gatekeeper, evaluators
as scorers, a senior authority who decides and is not bound by the panel),
individual/independent scoring done in isolation before any group
discussion, and a moderated "consensus" meeting that is explicitly *not*
score-averaging but a documented meeting-of-the-minds with a written
rationale — mirroring this product's Panel + Consensus design fairly
closely. Mandatory/eligibility criteria are screened before substantive
scoring begins, separate from the scored criteria. Governance treats the
evaluation record as a legal artefact: GAO gives controlling weight to the
*contemporaneous* record over after-the-fact justification, and protests
are sustained specifically for undocumented reasoning, not just undocumented
scores. Debriefing unsuccessful bidders is itself a regulated artefact with
prescribed contents and prohibitions. Practitioner commentary (mostly
vendor and consultancy blogs, treated as commentary here) converges on a
recurring failure mode this tool's design already guards against —
inconsistent scales, post-hoc criteria changes, and undocumented rationale
— but also flags calibration training and bias-awareness practices that sit
upstream of any tool and are open questions for this workstream rather than
settled findings.

## Claims

### Roles and separation of duties

US federal source selection for large acquisitions names three distinct
bodies: the Source Selection Authority (SSA), who makes the final
best-value decision and is explicitly "not bound by the SSEB's
recommendations"; the Source Selection Advisory Council (SSAC), senior
personnel who advise the SSA and review the evaluation board's work; and
the Source Selection Evaluation Board (SSEB), the working evaluators
organised into factor teams (technical, cost/price, past performance,
small business, legal) [Evidence: S201]. The SSAC is not required at all
when the agency uses Lowest-Price-Technically-Acceptable methodology
rather than a tradeoff/best-value methodology [Evidence: S201]. Below the
SSA/SSAC tier, an SSEB Chairperson has a distinct coordinating role:
ensuring evaluators apply criteria uniformly, escalating policy questions
to the SSA, and consolidating the panel's findings into a single report
[Evidence: S202].

At the US state level the same separation recurs in a lighter-weight form:
a procurement officer/purchasing official runs the process (screens
proposals for compliance, controls all vendor communication, and often
signs the final recommendation), while a separate evaluation committee
scores substance [Evidence: S206, S207] [Verified: 2026-07-18]. Maryland's manual is
explicit that "the procurement officer ultimately bears responsibility for
all determinations, though recommendations should reflect evaluation
committee consensus where possible" [Evidence: S207] — i.e. the panel
recommends, a designated official decides, structurally the same
separation as the federal SSA/SSEB split but collapsed to fewer tiers
[Inference: from S201, S207].

Panels are deliberately cross-functional. US federal guidance calls for a
"multi-disciplined team effort" spanning contracting, technical, legal,
cost/price, program management and end-user representation
[Evidence: S201]. UK/consultancy guidance on moderated scoring recommends
a 3–5 person team "with diverse expertise" [Evidence: S208]. This product
already models a named, role-diverse `EVALUATION_TEAM` in Setup, which
lines up with this pattern [Inference: from S201, S208].

Conflict-of-interest and confidentiality controls attach to the evaluator
role specifically: committee members must disclose conflicts and sign
non-disclosure/COI forms before scoring begins, and are told to keep
individual ratings confidential until the group meets, precisely so
individual scoring is not contaminated by group discussion in advance
[Evidence: S206] [Verified: 2026-07-18]. The Capability Sourcing Workbench does not
currently model evaluator-level COI declarations or a "scores hidden until
everyone has submitted" mechanic — this is a gap worth flagging as an open
question rather than a settled recommendation, since it touches session
state design [Hypothesis]. Validate by: checking whether any competitor
product (WS1) surfaces per-evaluator masked scoring, and whether Setup's
evaluator list would be the natural place to add COI attestations.

### Sequence: individual scoring first, then a moderated consensus meeting — never averaging

Every jurisdiction surveyed enforces the same two-step sequence: each
evaluator scores independently first, and only afterward does the panel
meet to reconcile. US federal guidance states evaluators "must convene to
discuss the offeror's proposal ... to reach a team consensus on findings
and rating" but is emphatic that "a simple averaging of the individual
evaluation results does not constitute consensus" [Evidence: S202] [Verified: 2026-07-18]. Similar language recurs widely across other state procurement guidance — that averaging individual scores does not itself constitute consensus, and agreement should instead be reached through discussion of proposal strengths and weaknesses — but this specific formulation could not be traced to a single directly-readable state document in this session, after the cited PDF returned only binary/unparseable content under three separate URL variants (doa.mt.gov, spb.mt.gov redirect, mt.gov) [Hypothesis] [Downgraded: 2026-07-18 — from Evidence]. Validate by: locating a directly-readable (non-PDF-corrupted) state procurement manual that states the averaging-is-not-consensus rule in comparable terms, e.g. a readable Montana mirror or an equivalent state's guidance. UK bid-consultancy commentary on moderated tender scoring documents the same pattern under the name "moderation meeting": evaluators score independently first, then reconvene to discuss and agree a final position rather than mechanically averaging their independent scores [Evidence: S208] [Verified: 2026-07-18].

Where consensus proves elusive, federal guidance does not force false
agreement: the report may instead document "both majority conclusions and
minority opinions with supporting rationale," which is then briefed to the
decision-maker [Evidence: S202]. This is a governance option this
product's `record_consensus()` model does not currently expose (it records
one consensus score with rationale, not a majority/minority split)
[Hypothesis]. Validate by: checking whether any real evaluation event in
this domain actually invokes the minority-opinion path often enough to be
worth modelling, versus being a rare escape valve.

This sequence maps closely onto the product's existing Evaluate → Compare
→ Moderate structure: individual panel scores captured first
(`PANEL_SCORES`), then a comparison view, then a moderation/consensus step
requiring rationale — the shape is aligned with governance practice
[Inference: from S201, S202, S210]. One difference: the reviewed
guidance treats calibration — a short session before scoring starts to
align evaluators on what a given score level means — as a distinct,
named step prior to independent scoring, not folded into the scoring
screen itself [Evidence: S209, S211]. The workbench has no explicit
calibration step or artefact; whether it needs one is an open question
[Hypothesis]. Validate by: asking whether Setup's scoring-scale anchors
table is being treated informally as the calibration artefact, or whether
a distinct pre-scoring "criteria walkthrough" step is expected in practice.

### Mandatory/eligibility gates are screened before, and separately from, scoring

Federal guidance places an "initial screening" step — verifying
submission compliance against a checklist — before substantive evaluation
begins [Evidence: S202] [Verified: 2026-07-18]. State guidance describes the same separation:
"the procurement officer conducts preliminary verification of bid
responsiveness, minimum qualifications ... before distributing materials
to evaluators" [Evidence: S207] [Verified: 2026-07-18]. This is the same structural principle the
product already encodes as "mandatory gates are pass/fail-style, sit
outside scoring entirely ... never diluted by a good score elsewhere" —
governance practice supports this as a widely mandated pattern rather than
a design choice unique to this tool [Evidence: S202, S207] [Verified: 2026-07-18].

### Weighting and scoring-model methodology must be fixed before proposals are seen

Multiple sources converge on a rule with real teeth: evaluation criteria
and weights must be locked before proposals arrive, because retroactive
adjustment is bias. Oregon's manual requires the evaluation strategy,
"including the criteria and scoring methodology," to be finalized before
solicitation documents are completed and published in the RFP itself
[Evidence: S206] [Verified: 2026-07-18]. Practitioner-facing guidance states the same principle
more bluntly: "the most damaging mistake is finalizing criteria after
proposals arrive; once you've seen what vendors are offering, any
adjustment to weights or criteria is subject to bias" [Evidence: S901] [Verified: 2026-07-18].
This directly supports the design intent behind this product's Setup
approval lock (criteria/weights become read-only on approval, reopening
requires a reason) — it is not an arbitrary UX constraint but reflects
what procurement governance treats as a defensibility requirement
[Inference: from S206, S901].

### Documentation is a legal artefact, not a nicety — and reasoning matters more than scores

US bid-protest review (GAO) gives controlling weight to the
*contemporaneous* record — the documentation made at the time of
evaluation — over anything an agency produces afterward to defend a
protest [Evidence: S203] [Verified: 2026-07-18]. Critically, the failure mode GAO sustains
protests over is not merely missing scores but missing *reasoning*: in one
2025 sustained protest, the evaluation record contained ratings but no
documented analysis of how the agency reconciled a specific eligibility
question, and the agency's later protest response relied on materials
"never mentioned in the contemporaneous evaluation record" — GAO found
this insufficient regardless of the final outcome being potentially
correct [Evidence: S203] [Verified: 2026-07-18]. This is a secondary source (a law firm's
commentary on a GAO decision, not the GAO decision itself), so treat the
specific case detail as commentary-grade even though the general
principle — contemporaneous record over retrospective justification — is
well established in procurement law commentary [Evidence: S203] [Verified: 2026-07-18].

This directly supports the product's design principle that consensus
recording and shortlist/recommendation divergence "refuse to save without
a non-empty reason": governance practice treats the *reason*, not just the
resulting number, as the artefact that survives scrutiny
[Inference: from S203, S202] [Verified: 2026-07-18].

Required documentation across the surveyed jurisdictions consistently
includes: an initial screening/compliance checklist, individual evaluator
worksheets with written comments justifying each score, a consolidated
factor/summary report per evaluator team, a final consolidated decision
document with comparative rationale, and (federally) a Source Selection
Decision Document signed by the SSA [Evidence: S201, S202, S207]. Search-derived material attributed to Maryland guidance a requirement that evaluators provide comments explaining each score, with a "reasonable, rational, and consistent" standard, but this could not be confirmed on the cited manual page and appears instead to trace to a Maryland State Board of Contract Appeals decision, not to the manual itself [Hypothesis] [Downgraded: 2026-07-18 — from Evidence]. Validate by: locating the Maryland State Board of Contract Appeals decision that uses the "reasonable, rational, and consistent" language, or identifying the correct Maryland procurement manual section, if any, that states a per-evaluator written-comment requirement directly. The underlying point that governance treats written justification as mandatory rather than optional polish is already independently carried by the Verified S202/S203 claims above; this Maryland-sourced framing adds nothing beyond what those claims already establish [Hypothesis] [Downgraded: 2026-07-18 — from Inference]. Validate by: confirming, before the brief leans on Maryland specifically for this point, whether a directly-readable Maryland source states a per-evaluator comment requirement in its own right rather than resting on S202/S203 alone.

### Post-award debriefing is itself a regulated audit/communication artefact

US federal debriefing rules (FAR 15.506) prescribe both required content
and explicit prohibitions: a debriefed offeror must receive the agency's
evaluation of significant weaknesses in their own proposal, the overall
evaluated cost/price and technical ratings of both the winner and
themselves, and a summary of the award rationale — but debriefings must
*not* include point-by-point comparisons against other offerors' actual
proposals, nor confidential cost/profit breakdowns, nor the identities of
past-performance references [Evidence: S213]. This is a distinct
downstream artefact this product does not currently model at all (no
debrief-generation surface exists, nor is one requested) — worth noting as
a boundary observation rather than a recommendation, since "report
builder" and "broad exports" are explicit hard scope limits, and this
observation notes overlap with those hard scope limits rather than
asserting this should be built. It is flagged only so the brief's
synthesist doesn't rediscover FAR 15.506 as a feature request that is
already out of scope by CLAUDE.md's own terms [Evidence: S213].

### Where practitioners say tooling helps or hinders

Practitioner-facing (mostly vendor/consultancy blog) commentary is
commentary-grade, not primary evidence, but the recurring themes are
worth recording as hypotheses about pain points a redesign could target:

- Spreadsheet-based evaluation commonly breaks down when merged across
  functions: "Engineering evaluates technical bids in their spreadsheet,
  finance runs pricing in a different one ... the scales don't match, the
  evaluation criteria labels differ, and one evaluator scored out of 5
  while another used 10" [Evidence: S214]. This is a scale-consistency
  failure mode that a single shared tool with a fixed `SCORING_SCALE`
  structurally prevents [Inference: from S214].
- A named list of common scoring errors recurs across practitioner
  sources: unclear criteria inviting vendor challenge, "group influence
  before independent scoring" introducing bias, mismatched criteria
  between the RFP and the scoring sheet, overweighting easily-quantified
  items, and skipping calibration so "teams [are] misaligned"
  [Evidence: S209] [Verified: 2026-07-18]. None of these are primary-source procurement law
  — they are consultancy/vendor blog commentary — so treat as
  practitioner sentiment, not governance mandate [Evidence: S209] [Verified: 2026-07-18].
- Practitioner commentary is split on whether software tooling itself is
  the fix: one source frames the underlying message as "discipline in
  *process* matters more than the tool itself" even while listing
  audit-trail and calibration benefits tools can provide [Evidence: S214].
  Another lists specific tool benefits practitioners attribute to
  structured platforms over ad hoc spreadsheets: enforced consistent
  criteria presentation, automated weighted-score calculation "reducing
  math errors," complete audit trails, and reduced "paralysis by
  analysis" risk when scoring models get too complex [Hypothesis] [Downgraded: 2026-07-18 — from Evidence]. Validate by: tracing this benefits list to a single directly-readable practitioner source rather than the S212 search-engine composite.
  Taken together, the practitioner sentiment is that tools help with
  *mechanical* consistency and record-keeping but do not substitute for
  process discipline (calibration, criteria-lock timing, rationale
  quality) [Hypothesis] [Downgraded: 2026-07-18 — from Inference]. Validate by: confirming the individual claims above (S209, S901, and a directly-read replacement for S214) before treating this synthesis as more than practitioner sentiment.
- One practitioner source frames a "halo effect" risk specific to
  evaluation panels — strong performance in one area or vendor
  familiarity (incumbency) unfairly bleeding into scores on unrelated
  criteria — as a named, recurring bias distinct from scale
  inconsistency [Hypothesis] [Downgraded: 2026-07-18 — from Evidence]. Validate by: tracing the "halo effect" framing to a single directly-readable practitioner source rather than the S212 search-engine composite. This is a workflow/behavioural claim
  about panels, not a tool feature claim, and belongs in this workstream
  rather than WS1's feature inventory [Hypothesis] [Downgraded: 2026-07-18 — from Evidence]. Validate by: same source-tracing check as the halo-effect claim above.

Where a claim in this section could plausibly be read as a *feature*
tools should have (e.g. "blind/masked scoring," "automated weighted
calculation") that overlaps with WS1's competitor-feature lens — flagged
here as an open question for the synthesist to reconcile with WS1's
findings rather than duplicated as this workstream's own recommendation.

## Sources proposed

### S201 — AFARS 1.4 Source Selection Team Roles and Responsibilities
- URL: https://www.acquisition.gov/afars/1.4-source-selection-team-roles-responsibilities
- Type: government-guidance
- Accessed: 2026-07-18
- Credibility: primary
- Added by: procurement-analyst (WS2)
- Notes: US Army Federal Acquisition Regulation Supplement chapter defining SSA/SSAC/SSEB roles, thresholds ($100M+ requires full three-tier team), and the rule that the SSA is not bound by SSEB recommendations. Primary for role separation and sign-off authority.

### S202 — AFARS Chapter 3, Evaluation and Decision Process
- URL: https://www.acquisition.gov/afars/chapter-3-evaluation-and-decision-process
- Type: government-guidance
- Accessed: 2026-07-18
- Credibility: primary
- Added by: procurement-analyst (WS2)
- Notes: Nine-step evaluation sequence (training, screening, initial evaluation, consensus, factor/summary reports, SSDD); explicit statement that averaging individual scores does not constitute consensus, and that minority opinions may be documented alongside majority consensus. Primary for sequence and documentation artefacts.

### S203 — GAO Bid Protest Sustain of the Month (Sept 2025): agency documentation and contemporaneous recordkeeping
- URL: https://www.governmentcontractslegalforum.com/2025/11/articles/bid-protest/september-2025-bid-protest-sustain-of-the-month-gao-criticizes-agencys-lack-of-documentation-highlighting-the-importance-of-contemporaneous-recordkeeping/
- Type: analyst
- Accessed: 2026-07-18
- Credibility: secondary
- Added by: procurement-analyst (WS2)
- Notes: Law firm commentary on a specific GAO sustained protest (CMS/IPRO); good for the general principle that GAO weighs contemporaneous documentation of reasoning over after-the-fact justification. Treat case specifics as secondary; the general contemporaneous-record principle is well established in the field but this single source doesn't constitute the primary GAO decision text.

### S205 — Montana RFP Evaluation Process Instructions / general state evaluation-committee search synthesis
- URL: https://doa.mt.gov/_docs/spsd/A-PROCUREMENT-FORMS-GUIDE/Solicitations/RFP_Evaluation_Process_Instructions.pdf
- Type: government-guidance
- Accessed: 2026-07-18
- Credibility: primary
- Added by: procurement-analyst (WS2)
- Notes: PDF could not be parsed by the fetch tool (binary/encoded); claims attributed here are drawn from a web-search synthesis of this and comparable state guidance (consensus-not-averaging, individual-scoring-first, confidentiality of ratings pre-meeting) rather than a direct read of this specific document. Flagged for the verifier to re-check against a directly readable state source if the claim is treated as material.

### S206 — Oregon Procurement Manual: Develop Evaluation Strategy
- URL: https://www.oregon.gov/das/opm/pages/evaluation.aspx
- Type: government-guidance
- Accessed: 2026-07-18
- Credibility: primary
- Added by: procurement-analyst (WS2)
- Notes: State procurement manual page (HTML, directly read). Covers evaluation committee composition, independent (non-consensus-mandated) scoring, and the requirement that criteria/scoring methodology be finalized before the RFP is issued.

### S207 — Maryland Procurement Manual, 6. Review and Evaluation Process
- URL: https://procurement.maryland.gov/mpm-6-review-and-evaluation-process/
- Type: government-guidance
- Accessed: 2026-07-18
- Credibility: primary
- Added by: procurement-analyst (WS2)
- Notes: State procurement manual (HTML, directly read). Covers procurement-officer vs evaluation-committee role split, technical/financial evaluation sequencing, cure letters/BAFO rounds, and required sign-offs (legal sufficiency, tax clearance, agency-head approval).

### S208 — Thornton and Lowe: Moderated Scoring — Tender Evaluation Best Practice
- URL: https://thorntonandlowe.com/moderated-scoring-tender-evaluation/
- Type: other
- Accessed: 2026-07-18
- Credibility: commentary
- Added by: procurement-analyst (WS2)
- Notes: UK bid-consultancy blog. Commentary-grade (the firm also sells bid software/services); useful for the 4-step moderated-scoring process description and named common pitfalls (inconsistency, vague criteria, poor documentation), not as governance authority.

### S209 — Gatekeeper: How to set up an RFP scoring system (RFP scoring template blog)
- URL: https://www.gatekeeperhq.com/blog/rfp-scoring-template-how-to-set-up-an-rfp-scoring-system-and-release-an-rfp
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: commentary
- Added by: procurement-analyst (WS2)
- Notes: Vendor blog (Gatekeeper sells procurement software) — commentary on practitioner pain points with spreadsheet scoring (version control, formula errors, missing calibration) and what tools/process discipline can fix. Marketing-adjacent; treat specific pain-point claims as practitioner-sentiment hypotheses, not evidence of prevalence.

### S210 — GOV.UK: Assessing Competitive Tenders (Procurement Act 2023 guidance)
- URL: https://www.gov.uk/government/publications/procurement-act-2023-guidance-documents-procure-phase/assessing-competitive-tenders-html
- Type: government-guidance
- Accessed: 2026-07-18
- Credibility: primary
- Added by: procurement-analyst (WS2)
- Notes: UK statutory guidance under the Procurement Act 2023. Covers transparency obligations (published assessment methodology, scoring matrices, assessment summaries to all bidders before award notice) and the "most advantageous tender" standard. Does not itself detail panel roles/scoring mechanics in depth — those are covered by moderation-meeting guidance elsewhere (see S208 for practitioner description of the moderation meeting itself, which this document references but does not reproduce).

### S211 — RFP.wiki: How to Evaluate RFP Responses and Score Vendors Objectively
- URL: https://www.rfp.wiki/content/how-to-evaluate-rfp-responses-and-score-vendors-objectively
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: commentary
- Added by: procurement-analyst (WS2)
- Notes: Vendor/platform blog. Commentary on bias patterns (halo effect, leniency/stringency bias, incumbent favouritism), calibration practice, and where software tools are said to help (consistency, audit trail) versus hinder (over-quantification, "paralysis by analysis").

### S212 — Web-search synthesis of practitioner RFP-scoring-mistakes guidance (multiple procurement/RFP-tooling blogs)
- URL: offline: composite of search-engine synthesis across rfpplanner.com, proqsmart.com, steerlab.ai, arphie.ai, inventive.ai, procurekey.com blog content (no single URL fetched directly)
- Type: other
- Accessed: 2026-07-18
- Credibility: commentary
- Added by: procurement-analyst (WS2)
- Notes: This entry aggregates a web-search-engine summary rather than a single directly-read page; used only for broadly-repeated, low-specificity practitioner themes (calibration sessions, criteria-lock-before-proposals-arrive, halo effect, weighting-after-the-fact bias). Treat as weak commentary — the Lead/verifier should re-derive from a single named URL before treating any specific claim here as material.

### S213 — FAR 15.506, Postaward debriefing of offerors
- URL: https://www.acquisition.gov/far/15.506
- Type: government-guidance
- Accessed: 2026-07-18
- Credibility: primary
- Added by: procurement-analyst (WS2)
- Notes: US federal acquisition regulation text (directly read, HTML). Prescribes required debriefing content (weaknesses, ratings, ranking, rationale summary) and explicit prohibitions (no point-by-point comparison against other offerors' proposals, no confidential cost/profit data, no reference-source identities).

### S214 — Web-search synthesis: spreadsheet-vs-software RFP scoring pain points (Responsive.io, ProcureKey, and related blogs)
- URL: offline: composite of search-engine synthesis across responsive.io/blog/rfp-evaluation-criteria, procurekey.com/blog/weighted-rfp-scoring, and gatekeeperhq.com content (S209 overlaps)
- Type: other
- Accessed: 2026-07-18
- Credibility: commentary
- Added by: procurement-analyst (WS2)
- Notes: Search-engine-synthesized commentary (not a single directly-read URL beyond S209) illustrating the specific cross-functional-spreadsheet-merge failure story (mismatched scales/labels across engineering/finance/procurement). Useful as an illustrative practitioner anecdote, not a verified incident.

## Open questions

- **Evaluator-level conflict-of-interest and confidentiality mechanics.**
  Government guidance treats signed COI declarations and pre-consensus
  score confidentiality as standard evaluator-role requirements
  [Evidence: S206]. This product currently has no modelled
  per-evaluator COI attestation or "scores hidden until submitted"
  mechanic. Whether this is worth adding is a product decision, not
  settled by this research — flagged for the synthesist, not
  recommended outright given the no-new-scope-without-asking rule.
- **Minority-opinion / non-consensus escape valve.** Federal guidance
  documents a majority/minority-opinion path when a panel cannot reach
  consensus [Evidence: S202]. This product's `record_consensus()` model
  assumes a single agreed score is always reachable. Whether this is a
  realistic gap or a rare edge case needs a domain-expert or
  frequency-based check this workstream cannot supply from published
  guidance alone.
- **Calibration as a distinct, artefact-producing step.** Multiple
  sources treat pre-scoring calibration (aligning on what a "5" means)
  as a named step with its own outputs, separate from the scoring scale
  itself [Evidence: S209, S211]. Whether Setup's scoring-scale anchors
  table already serves this purpose in practice, or whether a distinct
  calibration record is expected, is unresolved.
- **S205 was retracted** after both the investigator and the verifier
  found it unreadable across three URL variants (doa.mt.gov, spb.mt.gov,
  mt.gov); claims that had cited it have been re-cited to S202, S206, or
  S207, or downgraded to Hypothesis where no directly-read source carried
  the specific content. **S212's citations have been reassessed**: the
  one quote independently confirmed on a directly-readable page is now
  cited as S901; other S212-only claims in this file have been downgraded
  to Hypothesis. **S214 remains a search-engine synthesis** rather than a
  single directly-read document — any material claim resting solely on it
  should still be re-verified against a directly readable primary
  document before the brief treats it as settled evidence, this is
  flagged explicitly for the Verify phase.
- **Overlap with WS1 (competitor features).** Several claims here
  describe what practitioners say tools *should* do (audit trails,
  automated weighted calculation, blind scoring) — these are feature
  claims that properly belong to WS1's competitor inventory. This
  workstream records them only as *workflow motivation* (why panels want
  these things), not as a feature census; the synthesist should
  reconcile against WS1's findings rather than treat both as independent
  confirmation of the same fact.
- **Jurisdiction coverage is US-federal/US-state/UK only.** No EU-directive
  primary text or Australian/Canadian public-sector guidance was
  successfully fetched in readable form this session (EU search returned
  only meta-commentary on the Directives' evaluation, not the operative
  text). If cross-jurisdiction generality is a material claim in the
  brief, it needs broader confirmation than this workstream obtained.
