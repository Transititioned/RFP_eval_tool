# Findings: WS3 — Recurring UX patterns for scoring, comparison, progress, divergence, moderation

## Question

What recurring UX patterns do evaluation tools use for scoring input,
side-by-side comparison, progress/completeness, evaluator divergence, and
moderation — and which respect human-decides versus push auto-ranking?

## Summary

Across buyer-side eSourcing tools (Bonfire/Euna, SAP Ariba, JAGGAER,
Prokuria) a small set of UX patterns repeat: criterion-x-vendor grid
comparison (often "question-centric" rather than "vendor-centric"),
numeric-plus-reason scoring input, spread/variance highlighting to flag
evaluator divergence, and a consensus-override step that sits alongside
(not replacing) individual scores — all of which keep a human deciding
the final award. A second, newer cluster of patterns — most visible in
AI-marketed tools (Ivalua's agentic sourcing, Prokuria's automated
scoring dashboard, GEP's evaluation agents) — computes "award
recommendations" or, in Ivalua's own language, can go as far as "making
an award," pushing toward auto-ranking/auto-award with human oversight
recast as optional supervision rather than a mandatory gate. Progress/
completeness is generally shown as a fill-in progress bar or percentage
per evaluator or question set, distinct from any score. Several patterns
(drag-based reordering, live multi-user cell highlighting, hover-based
evidence tooltips) plausibly stretch Gradio's component model; this is
flagged as an open question for the brief, not resolved here.

## Claims

### 1. Scoring input patterns

Digital scorecards in this segment are typically dropdown/numeric-entry
grids paired with a mandatory or optional comment field, rather than free
text alone [Evidence: S318]. Bonfire's evaluator scorecard requires each
evaluator to select a predefined "Reason" for the numeric score they
enter (the reason set changes depending on whether the score is low,
medium, or high), in addition to a free-text comment [Evidence: S304] [Verified: 2026-07-18].
This is a concrete "structured justification" pattern: it forces a
categorical reason to accompany every score, not just at the point of
divergence — a stricter (and more front-loaded) version of this
product's current design, which only requires a rationale at the
consensus-recording step, not at individual scoring
[Inference: from S304]. Prokuria auto-scores single/multiple-choice
questions directly from the vendor's selected answer, but requires the
evaluator to manually enter a score for free-text answers
[Evidence: S312, S313] — i.e. scoring automation in this market is
already selective by question type, not all-or-nothing.

Make Things Accessible's procurement scoring guide uses a small
discrete scale (0–3) with example reference answers written out per
score level, and explicitly warns evaluators not to sum or compare scores
across different requirements as if they were commensurate
[Evidence: S318]. This is a caution pattern (guardrails against
over-aggregating a score) rather than a UI widget, but it is relevant to
any scale/anchor design [Inference: from S318].

### 2. Side-by-side comparison patterns

The dominant grid layout is criteria (or questions) down one axis and
vendors across the other, with cells holding the response, score, and/or
weight [Evidence: S309]. Vendorful's own written guidance recommends a
**question-centric** reading order — "line up questions and answers side
by side" so the evaluator's frame of reference is the question, scoring
each vendor's answer to it in turn, rather than reading one vendor's full
proposal at a time — explicitly because scoring an answer in the context
of its sibling answers "should improve the accuracy of the evaluation"
[Evidence: S310] [Verified: 2026-07-18]. This is a naming worth carrying into the brief: the
choice is not just "grid vs. document," but **question-anchored vs.
vendor-anchored traversal** of the same grid [Inference: from S310] [Verified: 2026-07-18].
Read against the project context in research/context/project-context.md,
this product's Evaluation > Compare tab is already grid-shaped and
criterion-filterable by architecture domain — the open design question
is which traversal order the UI nudges the evaluator toward
[Inference: from S310] [Verified: 2026-07-18].

Responsive's comparison-matrix guidance documents several grid variants
layered onto the same base structure: a plain score grid, a
weighted-score grid (multiplier shown per row), a multi-scorer grid
showing each evaluator's score per vendor side by side, and a "complex
response" variant for comparing long free-text answers — explicitly
naming the risk that combining response text + weights + multiple
scorers in one view "can quickly become complicated and confusing"
[Evidence: S309]. Bonfire is marketed as letting evaluators "compare
qualitative answers side by side" while still being able to open the
underlying vendor documentation for context [Evidence: S305, S306].

SAP Ariba's scorecard view supports expanding/collapsing grading criteria
and sorting the grading information within the scorecard, and is
described in SAP's own marketing as giving "clear, side-by-side
comparisons" across scenarios [Evidence: S307, S308] — though the SAP
help documentation is procedural (how to open/configure the view) rather
than a visual description, so the comparison-layout claim here rests more
on the marketing page than the help page [Inference: from S307, S308].

### 3. Progress / completeness patterns

Bonfire shows each evaluator a per-question-set progress bar that fills
in (described as turning green) as that evaluator completes scoring, plus
an overall percentage-of-project-complete figure evaluators can check
[Evidence: S305] [Verified: 2026-07-18]. This is architecturally close to this product's
Evaluation-landing `evaluation_progress()` telemetry (completion %,
evaluators complete, criteria complete) — the market pattern is a
progress bar/percentage keyed to *process* completion (questions
answered/scored), never to a score or ranking value, which, read against
the project context in research/context/project-context.md, matches this
product's principle of not conflating progress with a score
[Inference: from S305].

Vendor-side response-management tools (a different segment — bid teams
writing proposals, not buyer-side evaluation) show a comparable pattern
in reverse: Responsive's "Project Overview Dashboard" for bid teams
tracks "deadlines, progress completion, and authors and reviewers
summaries" for a response-authoring project [Evidence: S320]. This is
noted only as a segment-adjacent pattern — corroborating that
process-completion dashboards (distinct from any score) are a recurring
idea across both sides of this market, not as evidence for buyer-side
evaluation UX specifically [Inference: from S320]. Validate by: pulling a
screenshot or product tour specifically of a buyer-side (not vendor-side)
evaluation-progress dashboard beyond Bonfire's.

### 4. Evaluator divergence patterns

Bonfire's "Lack of Consensus" pattern is the clearest divergence-signal
UX found: when the spread between the lowest and highest evaluator score
on a single criterion reaches or exceeds a 30% threshold (e.g. a 3-point
spread on a 10-point scale), the criterion's cell is highlighted (orange)
in the Scoring Summary view, drawing attention without altering any
underlying score [Evidence: S302, S305] [Verified: 2026-07-18]. This is functionally the same
signal this product already computes as `score_spread` driving
`focus_queue()` (threshold >= 2), differing mainly — read against the
project context in research/context/project-context.md — in Bonfire's
use of a *relative* (%) threshold versus this product's *absolute*
threshold [Inference: from S302]. A percentage-based spread threshold
could behave differently across scoring scales of different widths and
is worth flagging as a design question rather than assuming either
threshold style is "more correct" [Hypothesis]. Validate by: comparing
behaviour of a %-based vs absolute-based spread threshold against this
product's actual `SCORING_SCALE` anchors.

Written procurement guidance independently converges on the same
practice without necessarily naming software: evaluators score
independently first, then convene to discuss criterion-by-criterion,
stopping specifically on outliers (e.g. one evaluator flagged a security
issue others missed) to "calibrate" rather than simply average away the
difference [Evidence: S317]. This validates the *workflow* rationale
behind spread-driven UI, even where the tool description doesn't detail
the exact screen [Inference: from S317].

### 5. Moderation / consensus patterns

Bonfire's Consensus Scoring lets a designated consensus scorer enter a
single score that *overrides* the average and all individual evaluator
scores for that criterion, and this overriding score becomes the one
used in vendor ranking — individual scores remain visible but are no
longer the ranking input once a consensus score exists
[Evidence: S301] [Verified: 2026-07-18]. This differs in a load-bearing way — read against the
project context in research/context/project-context.md — from this
product's `record_consensus()`, which records a consensus score
*alongside* individual panel scores without deleting or superseding them
in storage — Bonfire's UI treats consensus as replacement, this
product's treats it as an additional recorded fact
[Inference: from S301]. Both patterns keep the decision to set a
consensus score a deliberate human action gated behind a visible
moderation step, differing only — per the project context in
research/context/project-context.md — in whether the individual scores
are retained as first-class data afterward [Inference: from S301].

Bonfire's per-vendor "Criteria Analysis" view is reached from a Scoring
Summary table and is where consensus-mode changes are made — i.e. the
moderation screen is one click away from the divergence-highlighted
summary, not a separate module an evaluator has to navigate to blind
[Evidence: S303]. This "highlight-then-drill-in" adjacency is a UX
sequencing pattern independent of any specific override rule
[Inference: from S303].

### 6. Sorted by stance: human-decides vs. auto-ranking/auto-award

**Human-decides-respecting patterns** (ranking/score is data; a person
takes a separate, reasoned action to act on it):
- Bonfire consensus scoring and lack-of-consensus highlighting — flags
  divergence and lets a human enter an overriding score; ranking updates
  from that human entry, not from an algorithm resolving the spread
  [Evidence: S301, S302].
- Prokuria's scoring dashboard computes totals and a highest score, but
  its own guidance frames "choosing the winner" as a subsequent human
  step ("usually the supplier with the highest rating," implying it is
  not automatic or exclusive) with an explicit call-out that a tie
  requires the buyer to seek more information before deciding
  [Evidence: S312, S313].
- Ivalua's own sourcing-optimization page describes AI generating
  "instant, data-driven recommendations" for allocation decisions, with
  marketing language ("helping you make... decisions faster," not
  "makes the decision") implying the output is advisory
  [Evidence: S315] [Verified: 2026-07-18].
- GEP's description of AI evaluation agents stops at scoring, risk
  flagging, and summarizing for human evaluators — no claim of the AI
  selecting or awarding [Evidence: S317].

**Patterns that push toward auto-ranking / auto-award** (the tool's own
marketing describes the system reaching a selection or award outcome,
with human review recast as optional supervision rather than a mandatory
separate action):
- Ivalua's "AI Agents in Procurement" guide describes agentic sourcing
  agents that can go from selecting suppliers through analyzing bids to
  "offering a suggestion or even taking it further to making an award" —
  i.e. Ivalua's own copy places full automation (not just scoring) inside
  the agent's stated capability range, with human-in-the-loop presented
  as a recommended best practice rather than a structural gate
  [Evidence: S316] [Verified: 2026-07-18].
- Search-tool results attributed to Ivalua a description of agents that
  "detect unmanaged tail-spend categories and trigger sourcing sequences
  without manual initiation," running discovery through scoring through
  award-recommendation preparation end-to-end for low-value purchases,
  positioning the human checkpoint at the end of an automated chain
  rather than before each step — but this description could not be
  confirmed on any fetchable Ivalua page: direct fetches of S316 itself
  and two adjacent Ivalua pages (agentic-ai-in-procurement,
  ai-in-sourcing-and-procurement) did not contain this language, so it
  may be a search-tool fabrication rather than a genuine Ivalua claim
  [Hypothesis] [Downgraded: 2026-07-18 — from Evidence]. Validate by: manually browsing Ivalua's AI-agents guide and
  agentic-sourcing pages directly for autonomous tail-spend sourcing
  claims.
- Marketing language for "automated award recommendations" appears
  across this AI-tool cluster (Ivalua, and adjacent vendor copy found
  during this research) using the word "award" for what the system
  itself outputs, which — regardless of an accompanying human-approval
  claim — normalizes the framing that ranking-to-award is a single
  automatable pipeline rather than two categorically different acts
  (a computed ranking, and a human award decision)
  [Inference: from S315, S316] [Verified: 2026-07-18]. This framing is the one this product's
  core principle (`app/logic/recommendation.py` never storing the
  computed highest-scoring supplier as the recommendation) is explicitly
  designed to resist, which, per the project context in
  research/context/project-context.md, makes it directly relevant to the
  brief's "what not to adopt" section [Inference: from S315, S316] [Verified: 2026-07-18].

The practical takeaway for sorting: the *feature* (compute a ranking) is
near-universal across this market; what differs is whether the product's
own language and default flow treat that ranking as an input to a
separate human act, or as the terminus of an automatable pipeline that a
human merely supervises. This product's stated principle sits firmly in
the first camp and should be described in the brief as a deliberate
departure — read against the project context in
research/context/project-context.md — from where at least part of the
market's AI-marketed tooling is heading
[Inference: from S312, S313, S315, S316, S317].

### 7. Mandatory-gate-outside-scoring pattern

Legal/procurement commentary on public tendering explicitly recommends
buyers make clear upfront when a requirement is scored pass/fail
(exclusionary) versus scored on a graduated scale, because ambiguity
between the two creates legal risk in regulated tenders — a pass/fail
gate result is not blended into or offset by the graduated score
[Evidence: S319] [Verified: 2026-07-18]. This validates, from outside the vendor-tool space and
read against the project context in research/context/project-context.md,
the same separation this product already enforces between mandatory
gates and scored criteria [Inference: from S319] [Verified: 2026-07-18].

### 8. Gradio feasibility notes (flagged, not resolved)

Several of the patterns above imply client-side interaction that may
stretch Gradio's `gr.Blocks`/`gr.Dataframe` model:
- Cell-level conditional highlighting keyed to a computed spread value
  (Bonfire's orange lack-of-consensus cells) — `gr.Dataframe` styling
  hooks exist but per-cell conditional colour driven by a computed
  threshold is more limited than a purpose-built grid component
  [Hypothesis]. Validate by: prototyping conditional `gr.Dataframe`
  styling against gradio==6.19.0's actual styling API.
- A toggle that reveals/hides scoring columns on demand (Prokuria's
  "Show scoring" switch) is plausibly straightforward in Gradio via
  `gr.Checkbox` + `.change()` visibility toggling on components
  [Hypothesis]. Validate by: a small spike matching the existing
  `.click()`/`.change()` pattern in `gradio_app.py`.
- Live, multi-user concurrent editing of the same scoring grid (implied
  by "evaluators complete" telemetry updating in near-real-time across
  users) is a harder fit for a single-process Gradio Blocks app without
  additional session/state-sharing infrastructure this product does not
  have [Hypothesis]. Validate by: checking whether any Evaluation-tab
  recommendation in the eventual brief actually requires cross-session
  live updates, versus refresh-on-action (which this product already
  does via its "Refresh status" pattern).

## Sources proposed

### S301 — Bonfire Support: Consensus Scoring
- URL: https://support.gobonfire.com/hc/en-us/articles/204626548-Consensus-Scoring
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: ux-pattern-analyst (WS3)
- Notes: Primary for how Bonfire's consensus-score override works and that it becomes the ranking input; describes UI as "Consensus" marked scorecard (purple box).

### S302 — Bonfire Support: Lack of Consensus Highlighting on Submission Scores
- URL: https://support.gobonfire.com/hc/en-us/articles/205707928-Lack-of-Consensus-Highlighting-on-Submission-Scores
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: ux-pattern-analyst (WS3)
- Notes: Primary for the 30%-spread orange-highlight divergence pattern and its worked example (6 vs 9 on a 10-point scale).

### S303 — Bonfire Support: Criteria Analysis
- URL: https://support.gobonfire.com/hc/en-us/articles/360042725454-Criteria-Analysis
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: ux-pattern-analyst (WS3)
- Notes: Primary for the navigation path from Scoring Summary to per-vendor Criteria Analysis, and that consensus edits happen from that screen.

### S304 — Bonfire Support: Bonfire scoring reasons
- URL: https://support.gobonfire.com/hc/en-us/articles/207041427-Bonfire-scoring-reasons
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: ux-pattern-analyst (WS3)
- Notes: Primary for the predefined-reason-plus-comment scoring input pattern, including that reason lists vary by score band (low/medium/high).

### S305 — Bonfire (Euna) / Spend Matters Technology Review whitepaper
- URL: https://gobonfire.com/wp-content/uploads/Learn_Whitepaper_Bonfire-Spend-Matters-Technology-Review.pdf
- Type: analyst
- Accessed: 2026-07-18
- Credibility: secondary
- Added by: ux-pattern-analyst (WS3)
- Notes: Analyst-style review distributed by the vendor; used here for the progress-bar-per-question-set description and "compare qualitative answers side by side" phrasing — treat as vendor-favourable analyst commentary, not independent verification.

### S306 — Spend Matters: "Digitizing Manual Sourcing Isn't Easy — Unless You Use Bonfire"
- URL: https://spendmatters.com/2019/04/30/shifting-to-digitization-from-manual-sourcing-processes-isnt-easy-unless-you-use-bonfire/
- Type: analyst
- Accessed: 2026-07-18
- Credibility: secondary
- Added by: ux-pattern-analyst (WS3)
- Notes: Sponsored/partner analyst content (2019, still linked from vendor site in 2026) — corroborates S305's side-by-side qualitative-comparison claim; dated, so treat feature claims as directional not current-state-verified.

### S307 — SAP Help Portal: About Grading and Scoring (SAP Ariba Sourcing)
- URL: https://help.sap.com/docs/ARIBA_SOURCING/148a004128f64bc1837c11a69eb7caab/7d49a3ba71ea10149d7ffcca62d3a33d.html
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: ux-pattern-analyst (WS3)
- Notes: Primary for scorecard-view procedural detail (expand/collapse criteria, sort grading info) — procedural, not a visual/screenshot description.

### S308 — SAP Ariba Sourcing Features page
- URL: https://www.sap.com/products/spend-management/ariba-sourcing/features.html
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary for "product has this feature," commentary for "works well"
- Added by: ux-pattern-analyst (WS3)
- Notes: Marketing page source for "clear, side-by-side comparisons" framing; marketing copy, treat comparison-quality claims as unverified.

### S309 — Responsive: "How to Use a Vendor Comparison Matrix"
- URL: https://www.responsive.io/blog/vendor-comparison-matrix
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: secondary (vendor blog, generic guidance rather than Responsive's own product screenshot)
- Added by: ux-pattern-analyst (WS3)
- Notes: Good for naming grid-variant patterns (simple/weighted/multi-scorer/complex-response) and the explicit multi-scorer divergence example ("Bob and Amy's scores vary widely on Vendor 1"); Responsive is vendor-side (response management), so treat as UX-pattern commentary rather than buyer-side product evidence.

### S310 — Vendorful: "The Essential Guide to Understanding the RFP Process"
- URL: https://info.vendorful.com/rfp-process/
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary for Vendorful's own stated design philosophy, commentary for general market practice
- Added by: ux-pattern-analyst (WS3)
- Notes: Source of the question-centric ("line up questions and answers side by side") vs vendor-centric traversal distinction; also documents linguistic-anchor scoring scale (unacceptable/poor/satisfactory/good/excellent).

### S311 — JAGGAER: Sourcing Optimization solution page
- URL: https://www.jaggaer.com/solutions/sourcing-optimization
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary for "product offers X," commentary for quality
- Added by: ux-pattern-analyst (WS3)
- Notes: Source for configurable per-category weighting (price/quality/lead time/ESG/risk) framed as keeping "awards defensible end-to-end" — marketing copy naming weighting as an audit-defensibility feature.

### S312 — Prokuria blog: "How To Do Automated RFP Scoring In Prokuria"
- URL: https://www.prokuria.com/blog/automated-rfp-scoring
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary for Prokuria's own feature description
- Added by: ux-pattern-analyst (WS3)
- Notes: Source for auto-scoring of choice-questions vs manual scoring of free text, and for framing "choosing the winner" as a distinct human step after the dashboard computes totals.

### S313 — Prokuria Help Center: "Scoring – Create an automated scoring for your request"
- URL: https://support.prokuria.com/buyers-sourcing-managers/requests-rfq-rfp-rfi/scoring-create-an-automated-scoring-for-your-request/
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: ux-pattern-analyst (WS3)
- Notes: Primary for the "Compare responses" page's "Show scoring" toggle revealing Max Points/Points/Weights columns; documentation confirms no auto-selection of a winning vendor.

### S314 — Ivalua blog: "Vendor Selection Process: Steps, Criteria & Checklist Guide"
- URL: https://www.ivalua.com/blog/vendor-selection-process/
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: secondary (general guidance content, not a product-feature description)
- Added by: ux-pattern-analyst (WS3)
- Notes: General guidance framing evaluation as scoring-then-human-choice; does not itself describe Ivalua's UI — used only as corroborating context, not as feature evidence.

### S315 — Ivalua: eSourcing Software solutions page
- URL: https://www.ivalua.com/solutions/process/strategic-sourcing/sourcing/
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary for "product offers X," commentary for quality
- Added by: ux-pattern-analyst (WS3)
- Notes: Source of "Automate data collection, scoring, optimization, and award recommendations" and "Accelerate decisions with instant, data-driven recommendations" — marketing copy; language leans advisory ("recommendations," "helping you decide") rather than auto-award.

### S316 — Ivalua blog: "AI Agents in Procurement: The Ultimate Guide"
- URL: https://www.ivalua.com/blog/ai-agents-in-procurement/
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary for Ivalua's own stated agent capabilities, commentary for whether this is good practice
- Added by: ux-pattern-analyst (WS3)
- Notes: Source of the "offering a suggestion or even taking it further to making an award" phrasing and the tail-spend autonomous-sourcing description; also contains a human-in-the-loop best-practice recommendation elsewhere in the same piece — both should be read together, not selectively.

### S317 — GEP Blog: "AI Agents for RFP & RFQ Evaluation: Faster, Fairer Scoring"
- URL: https://www.gep.com/blog/technology/ai-agents-rfp-rfq-response-evaluation
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: secondary (vendor thought-leadership content, not a specific product screenshot)
- Added by: ux-pattern-analyst (WS3)
- Notes: Source for AI-agent scope stopping at scoring/flagging/summarizing, with humans retaining the final decision; no UI/screenshot detail.

### S318 — Make Things Accessible: "Procurement scoring and maturity" guide
- URL: https://www.makethingsaccessible.com/guides/procurement-scoring-and-maturity/
- Type: other (independent practitioner guide, accessibility-sector focus but methodology is domain-general)
- Accessed: 2026-07-18
- Credibility: commentary
- Added by: ux-pattern-analyst (WS3)
- Notes: Source for the 0–3 anchored-scale-with-example-answers pattern and the explicit warning against comparing/summing scores across unrelated requirements.

### S319 — Bevan Brittan LLP: "Make your intentions clear: 'Pass'/'Fail' scoring and rejection of tenders"
- URL: https://www.bevanbrittan.com/insights/articles/2018/make-your-intentions-clear-passfail-scoring-and-rejection-of-tenders/
- Type: other (law firm procurement-law commentary)
- Accessed: 2026-07-18
- Credibility: commentary
- Added by: ux-pattern-analyst (WS3)
- Notes: Legal-commentary source for why pass/fail (gate) scoring must be kept distinct from graduated scoring in regulated tenders; corroborates the gates-outside-scoring pattern from a compliance angle rather than a UX-feature angle. Article dated 2018; treat legal-risk framing as durable but check for newer UK procurement-law commentary if this claim becomes load-bearing.

### S320 — Responsive: "RFP Response Management Dashboards"
- URL: https://www.responsive.io/blog/rfp-response-management-dashboards
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary for Responsive's own dashboard feature description; segment caveat applies (vendor-side response authoring, not buyer-side evaluation)
- Added by: ux-pattern-analyst (WS3)
- Notes: Source of the "Project Overview Dashboard" quote ("deadlines, progress completion, and authors and reviewers summaries"); used only as a segment-adjacent corroboration for process-completion-dashboard-as-a-pattern, not as buyer-side evaluation evidence.

## Open questions

- I could not find a buyer-side (evaluation) product tour or screenshot
  specifically showing a live, cross-evaluator completion dashboard
  beyond Bonfire's description in a vendor-distributed whitepaper (S305)
  — the Responsive dashboard found (S320) is vendor-side (response
  authoring), a different segment. A stronger buyer-side source would
  need a direct demo video transcript or a review-site screenshot; both
  eluded search within this session's budget.
- The Ivalua "making an award" phrasing (S316) is strong evidence of
  auto-award-leaning marketing language, but I have not confirmed whether
  Ivalua's actual shipped product requires an approval click before an
  award is recorded, or whether that gate is genuinely optional/
  configurable — the brief should treat this as a marketing-language
  finding about market direction, not a confirmed claim about Ivalua's
  workflow enforcement.
- Bonfire's "30% spread" consensus threshold and this product's "spread
  >= 2 (absolute)" threshold are structurally different (relative vs.
  absolute); I did not find a source explaining why Bonfire chose a
  relative threshold, so any brief recommendation to change this
  product's threshold style should be flagged as needing its own design
  rationale, not copied from Bonfire's precedent alone.
- All Gradio-feasibility notes in Claim 8 are marked Hypothesis
  deliberately — this workstream's brief was to *name and evaluate*
  patterns, not judge feasibility; a build-facing follow-up (a small
  Gradio spike) would be needed before any brief recommendation in this
  area is treated as low-risk.
- Time/tooling did not allow direct screenshot review (only text-fetch
  and search-snippet access) for any of these products; every visual
  layout claim above is reconstructed from prose descriptions in docs/
  marketing/analyst text, not from viewing an actual screenshot or demo
  video frame. This is a meaningful source-quality gap the pack
  anticipated ("Product tours, docs with screenshots, demo videos... are
  your raw material") that this session did not fully satisfy — a repeat
  pass with an image-capable fetch of specific vendor demo pages would
  strengthen these claims.
</content>
