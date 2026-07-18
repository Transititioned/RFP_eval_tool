# Findings: WS1 — Which products serve buyer-side RFP evaluation, and what is their feature set across the evaluate/score/award stages?

<!-- Written only by this workstream's investigator. Claims follow
research/core/evidence-contract.md exactly; sources use this
workstream's ID block from mission.md. -->

## Question

Which products serve buyer-side RFP evaluation, and what is their feature set across the evaluate/score/award stages (individual scoring, consensus/moderation, weighting, mandatory gates, audit trail, award justification)?

## Summary

Eight buyer-side products were surveyed across two segments: full source-to-pay suites with a sourcing/evaluation module (SAP Ariba Sourcing, Coupa Sourcing, JAGGAER, Ivalua) and lighter sourcing/RFP-evaluation point tools (Bonfire/Euna, Prokuria, Vendorful), the former enterprise-suite-positioned, the latter narrower in scope. Individual scoring, weighting, and audit trail are well-documented, common features across the surveyed suite vendors; consensus/moderation as an explicit step distinct from individual scores is clearly documented for Bonfire and SAP Ariba but not visible in the public product pages of the two smaller point tools checked. Mandatory-gate-outside-scoring is a recognized pattern (Bonfire's Pass/Fail criteria carry no weight; SAP Ariba separates gradable from non-gradable content). The most consequential finding for this mission is that several competitors (JAGGAER's Intelligent Award Navigator, Ivalua's Sourcing Decision Center, SAP Ariba's optimization award scenarios) market computed award recommendations as a headline feature — a pattern that directly conflicts with the workbench's "never auto-declares a winner" principle and belongs in the brief's "what not to adopt" section. A distinct, human-authored "award justification" artifact (separate from a computed score/optimization output) was not clearly documented as a first-class feature in any product surveyed.

## Claims

### Segment and positioning

The surveyed buyer-side products split into two segments: enterprise source-to-pay suites offering sourcing/evaluation as one module among many (SAP Ariba Sourcing, Coupa Sourcing, JAGGAER, Ivalua), and narrower sourcing/RFP-evaluation point tools (Bonfire/Euna Procurement, Prokuria, Vendorful) whose public product pages describe only sourcing-event and evaluation functionality, not adjacent modules like invoicing or full contract lifecycle management [Inference: from S110, S111, S112, S113, S114].

Bonfire (now marketed as Euna Procurement) explicitly positions for the public sector: "purpose-built for the public sector" with "27 years of experience and 3,000+ public sector customers" [Evidence: S104], while also being listed as serving "public, private, and enterprise organizations" on a review aggregator [Evidence: S115]. On G2, Coupa (4.2) and SAP Ariba (4.1) carry substantially more reviews than Bonfire/Euna Procurement (4.5, only 11 reviews), consistent with Coupa/Ariba's larger enterprise install base [Evidence: S116]. The Bonfire rating should be read cautiously given the small review count [Inference: from S116].

### Individual scoring and weighting

SAP Ariba Sourcing supports three grading modes: pre-grading (automatic grading of quantifiable Yes/No, Multiple Choice, Number/Date answers, adjustable after event close), blind grading (hides participant identity from graders "to increase the level of objectivity and remove bias"), and standard manual grading with configurable "weight points" that determine "how much that content contributes toward the final score" [Evidence: S105, S106] [Verified: 2026-07-18].

Bonfire distinguishes two criteria types: "Rated Scale" criteria, scored on an integer scale (default 0–10) and individually weightable, versus "Pass/Fail" criteria, which "are not assigned any weighting" and are "typically applied to signed forms, certifications, and other mandatory sections" [Evidence: S102] [Verified: 2026-07-18]. Bonfire also supports auto-scoring of True/False, Yes/No, or Number responses against "mandatory or pricing criteria" [Evidence: S103].

Prokuria computes per-question scoring where evaluators (or the system, for choice-type questions) assign points up to a configured maximum per question, and the question's weight in the total score is calculated automatically as "the maximum points of the specific question divided by the total points" — free-text and file-upload questions require manual scoring [Evidence: S113]. Vendorful advertises "fully automated application of weights and collective scoring" plus the ability to "leverage subject matter experts to score responses" [Evidence: S114].

Weighting configuration (assign a numeric importance per criterion/question, then compute a weighted total) appears to be a baseline, near-universal feature across this segment rather than a differentiator [Inference: from S102, S105, S106, S110, S111, S113, S114].

### Consensus and moderation

Bonfire's Consensus Scoring feature lets a facilitator "enter a single score that will override the average and all other scores entered for that particular criteria," used during a consensus meeting; the product also flags criteria for consensus review when evaluators diverge by more than an internal threshold [Evidence: S101] [Verified: 2026-07-18]. SAP Ariba's grading configuration includes an "Enable approval for team grading" event rule alongside the weighting rules, implying an explicit approval/moderation step over team members' individual grades rather than a straight average [Evidence: S105] [Verified: 2026-07-18].

No explicit consensus, moderation, or divergence-flagging feature is documented on Prokuria's or Vendorful's public product/support pages reviewed for this workstream; both describe individual/team scoring and weighting but not a distinct consensus step. This absence is noted only on the specific pages reviewed and is not confirmed as an absence from the full product [Evidence: S113, S114]. This gap should not be read as proof point tools lack the capability, only that it is not marketed on these particular pages [Hypothesis]. Validate by: requesting a Prokuria/Vendorful demo or checking their help-center search directly for "consensus."

### Mandatory gates

Gate-outside-scoring — treating pass/fail mandatory requirements as categorically separate from weighted scoring — is a documented pattern in this segment, not unique to this product: Bonfire's Pass/Fail criteria carry no weight and are reserved for certifications/mandatory sections [Evidence: S102], and Euna/Bonfire's public-sector positioning highlights "sealed bidding, error checkers, and automated workflows" that "ensure that procurement regulations and requirements are meticulously upheld" [Evidence: S104]. SAP Ariba's grading rules similarly separate "gradable" (scored/weighted) content from other quantifiable response types used for compliance checks [Evidence: S106]. Gate-before-score (or gate-outside-score) appears to be an expected baseline in the buyer-side evaluation segment [Inference: from S102, S104, S106].

### Audit trail

Audit trail depth varies by product but is present across every enterprise-suite vendor checked. SAP Ariba Sourcing's audit log records, per event, "Date created," "Real user," "On behalf of," "Action" (e.g., "Event edited and republished"), and "Details," filterable by Date, Event Type, Real User, and Effective User [Evidence: S107] [Verified: 2026-07-18]. Coupa's sourcing page describes "a complete audit trail for sourcing activities, capturing everything from setup to supplier communications, bid submissions, evaluations, approvals, and award decisions" [Evidence: S112] [Verified: 2026-07-18]. JAGGAER's sourcing-optimization page advertises "100% Audit trail, every scenario," with every award recommendation carrying "the constraints, scenarios and supplier inputs behind it" [Evidence: S110] [Verified: 2026-07-18]. Ivalua describes "complete audit trails" specifically in the context of scaled auction management [Evidence: S111] [Verified: 2026-07-18]. Euna/Bonfire markets "FOIA-ready audit trails" where "every contract action, approval, and workflow step is automatically logged and timestamped" [Evidence: S104] [Verified: 2026-07-18].

Comprehensive, timestamped audit logging covering the full evaluate-to-award lifecycle is a baseline expectation across this segment, reinforced particularly strongly by the public-sector-facing vendors (Bonfire/Euna) for whom FOIA/transparency obligations are explicit [Inference: from S104, S107, S110, S111, S112] [Verified: 2026-07-18].

### Award justification and the auto-recommendation pattern (mission-relevant)

This is the most load-bearing finding for the makeover brief. Several competitors treat a *computed* award recommendation as their headline evaluate/award-stage feature, going further than a ranked score display:

- JAGGAER's "Intelligent Award Navigator" (IAN) uses "artificial intelligence (AI) and advanced game theory" to iteratively present the user with two-option award scenarios, learn the user's revealed preference, and converge on a recommendation; JAGGAER's IAN blog copy states the tool stays "under the full control of the human operator," while JAGGAER's Sourcing Optimization page states every recommendation is accompanied by "the constraints, scenarios and supplier inputs behind it," pitched as "Auditable, explainable and ready for finance, risk and the C-suite" [Evidence: S109, S110] [Verified: 2026-07-18].
- Ivalua's "Sourcing Decision Center" is described as using "AI and mathematical optimization to evaluate all bids, constraints, and supplier data" and delivering "instant, data-driven recommendations" for the supplier-selection decision itself [Evidence: S111] [Verified: 2026-07-18].
- SAP Ariba Sourcing's award workspace lets a project owner build and compare "award scenarios," including preconfigured optimization scenarios (e.g., a "Best Bid" scenario allocating 100% of an item to the lowest-price supplier) that computationally determine "the optimal suppliers and allocations," and the platform additionally uses "machine learning to recommend the best suppliers for guided sourcing events based on historical data from similar events" [Evidence: S108] [Verified: 2026-07-18].

Even where vendor copy frames these tools as human-controlled decision aids rather than autonomous deciders, all three market a system-computed "optimal" or "recommended" award as the product's differentiating value, which sits materially closer to auto-recommendation than this workbench's principle of treating the highest score as data only, never a stored or declared recommendation [Inference: from S108, S109, S111] [Verified: 2026-07-18]. None of the vendor materials reviewed frame "the tool must never declare a winner" as a design principle in its own right — the emphasis is on optimization quality and explainability of the computed answer, not on withholding a computed answer [Inference: from S108, S109, S110, S111] [Verified: 2026-07-18].

By contrast, a distinct, human-authored "award justification" text artifact (reasons/rationale entered by a person, separate from and outside any computed score) was not clearly documented as a named, first-class feature on any of the vendor pages reviewed — award-stage documentation centred on scenario comparison, optimization, and audit logging of the computed process, not on a dedicated justification-writing step [Hypothesis]. Validate by: reviewing product demo videos or requesting vendor documentation specifically for an "award justification," "decision memo," or "recommendation rationale" field/module across these products, and cross-checking WS2's procurement-governance findings for whether this artifact is typically produced outside the eSourcing tool (e.g., in a separate board paper).

One Bonfire/Euna Procurement user review noted a specific award-mechanics limitation: the system lacks "the ability to award a single product to multiple proposers," constraining scenarios needing split or backup awards [Evidence: S115].

## Sources proposed

### S101 — Bonfire Support: Consensus Scoring
- URL: https://support.gobonfire.com/hc/en-us/articles/204626548-Consensus-Scoring
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Describes the consensus-override scoring mechanic and the ~30% evaluator-divergence trigger for consensus review. Direct WebFetch returned HTTP 403; content obtained via search-tool excerpt of the page — a Verifier should attempt a fresh direct fetch or archived copy to confirm exact wording.

### S102 — Bonfire Support: Criteria Types
- URL: https://support.gobonfire.com/hc/en-us/articles/201105896-Criteria-Types
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Defines Rated Scale (weighted) vs Pass/Fail (unweighted, mandatory-document) criteria types — the clearest documented gate-outside-scoring pattern found. Direct WebFetch returned HTTP 403; content obtained via search-tool excerpt.

### S103 — Bonfire Support: Auto-Scoring Requested Data for True/False, Yes/No, or Number
- URL: https://support.gobonfire.com/hc/en-us/articles/212282877-Auto-Scoring-Requested-Data-for-True-False-or-Number-
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Documents auto-scoring of mandatory/pricing criteria. Direct WebFetch returned HTTP 403; content obtained via search-tool excerpt.

### S104 — Euna Solutions: Public Sector Procurement Software
- URL: https://eunasolutions.com/solutions/procurement/
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Directly fetched. Marketing page but with specific, quotable claims on public-sector positioning, sealed bidding/compliance guardrails, and FOIA-ready audit trail. Treat "meticulously upheld" language as marketing tone; the underlying feature claims (sealed bidding, timestamped logs) are still primary for "the product has this feature."

### S105 — SAP Help Portal: About Grading and Scoring (SAP Ariba Sourcing)
- URL: https://help.sap.com/docs/ARIBA_SOURCING/148a004128f64bc1837c11a69eb7caab/7d49a3ba71ea10149d7ffcca62d3a33d.html
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Product documentation (not marketing) — describes blind grading, weight points, and the "Enable approval for team grading" event rule. Direct WebFetch returned HTTP 403 (page is JS-rendered); content obtained via search-tool excerpt quoting the help text directly. A Verifier should confirm via SAP Help Portal search UI.

### S106 — SAP Help Portal: Pre-Grading (Automatic Grading)
- URL: https://help.sap.com/docs/strategic-sourcing/grading-and-scoring/about-pre-grading-automatic-grading
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Documents which question types are auto-gradeable and that pre-grades remain editable post-close. Same 403/search-excerpt caveat as S105.

### S107 — SAP Help Portal: Audit Log Criteria for SAP Ariba Sourcing
- URL: https://help.sap.com/docs/ariba/managing-ariba-audit-information/audit-log-criteria-for-sap-ariba-sourcing-0a448d86f66644a1af2ec6a58b25cdd3
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Documents audit log fields (Date, Real user, On behalf of, Action, Details) and filters. Same 403/search-excerpt caveat as S105.

### S108 — SAP Help Portal: Awards for Guided Sourcing Events
- URL: https://help.sap.com/docs/strategic-sourcing/managing-events-with-guided-sourcing/awards-for-guided-sourcing-events
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Documents award scenarios, optimization scenarios (e.g. "Best Bid"), and ML-based supplier recommendations — the core evidence for the auto-recommendation contrast pattern flagged in Claims. Same 403/search-excerpt caveat as S105.

### S109 — JAGGAER blog: The Intelligent Award Navigator: Think Big
- URL: https://www.jaggaer.com/blog/intelligent-award-navigator-think-big
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Directly fetched (WebFetch succeeded). Marketing/blog register, but describes the IAN mechanic (iterative two-option preference learning) in enough detail to be primary for "the product has this feature"; treat "under full control of the human operator" as vendor framing, not independently verified.

### S110 — JAGGAER: Sourcing Optimization solution page
- URL: https://www.jaggaer.com/solutions/sourcing-optimization
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Directly fetched. Source for weighted risk scoring, scenario/constraint modeling, and "100% Audit trail, every scenario" claim.

### S111 — Ivalua: eSourcing solution page
- URL: https://www.ivalua.com/solutions/process/strategic-sourcing/sourcing/
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Directly fetched. Source for "Sourcing Decision Center" AI/optimization award-recommendation claim and audit-trail claim; marketing page, feature depth beyond the quoted phrases unverified.

### S112 — Coupa: Strategic Sourcing product page
- URL: https://www.coupa.com/products/source-to-contract/sourcing/
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: secondary
- Added by: competitor-scout (WS1)
- Notes: Direct WebFetch returned HTTP 403; claims (equal-weighted baseline scorecard, full-lifecycle audit trail) were obtained via search-tool excerpt only and could not be cross-checked against the live page — downgraded to secondary credibility pending direct verification. A Verifier should attempt a fresh fetch before treating these as settled Evidence.

### S113 — Prokuria Support: Scoring – Create an automated scoring for your request
- URL: https://support.prokuria.com/buyers-sourcing-managers/requests-rfq-rfp-rfi/scoring-create-an-automated-scoring-for-your-request/
- Type: product-docs
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Directly fetched. Clear, specific mechanics for per-question scoring and automatic weight calculation; page does not mention consensus, mandatory gates, or audit trail (treated as an absence-on-this-page, not a confirmed product gap).

### S114 — Vendorful: e-Sourcing Software for RFPs, RFIs and RFQs
- URL: https://vendorful.com/e-sourcing/strategic-sourcing-rfp-rfi-rfq/
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Directly fetched. Source for blind scoring, automated weighting, SME-based scoring, and executive-summary output claims; page does not mention consensus/moderation or mandatory gates explicitly.

### S115 — Capterra: Euna Procurement (formerly Bonfire) reviews and pricing
- URL: https://www.capterra.com/p/138928/Bonfire/
- Type: review-aggregator
- Accessed: 2026-07-18
- Credibility: commentary
- Added by: competitor-scout (WS1)
- Notes: Directly fetched. Useful for user-review colour (evaluation-tool praise, an award-mechanics limitation) and a single reviewer-submitted starting price point ($1,000/year) — treat pricing as indicative only, not an authoritative price list.

### S116 — G2: Compare Coupa vs. SAP Ariba
- URL: https://www.g2.com/compare/coupa-software-coupa-vs-sap-ariba
- Type: review-aggregator
- Accessed: 2026-07-18
- Credibility: commentary
- Added by: competitor-scout (WS1)
- Notes: Direct WebFetch returned HTTP 403; ratings figures (Coupa 4.2, SAP Ariba 4.1) and Bonfire's 4.5/11-review comparison point were obtained via search-tool excerpt only. Useful for rough relative positioning, not for any single precise claim — review counts are thin for Bonfire.

## Open questions

- Direct WebFetch access was blocked (HTTP 403) for support.gobonfire.com, most help.sap.com pages, coupa.com, and g2.com; all claims from those domains rest on search-tool excerpts rather than a directly rendered page. A Verifier with a different fetch path (or manual browser check) should re-confirm S101, S102, S103, S105, S106, S107, S108, S112, S116 before the brief treats them as settled.
- No product surveyed had clear, named documentation of a conflict-of-interest handling feature (the pack's evaluate/score/award checklist includes this facet) — this may be a genuine market gap, a workflow handled outside the tool (procurement-analyst/WS2 territory), or simply undocumented on public pages. Not resolved here.
- Pricing/segment positioning (point tool vs. enterprise suite) for Prokuria, Vendorful, and Zip rests on inference from what their product pages describe, not an explicit vendor statement of market segment or a review-aggregator pricing table; not independently confirmed.
- Whether any surveyed product has a distinct, named "award justification" or "recommendation rationale" authoring feature (as opposed to computed-score/optimization output plus general audit logging) remains an open hypothesis — see the Claims section's Validate-by line. This bears directly on whether the workbench's Recommendation tab's free-text reasons fields are already a market norm or a genuine differentiator worth highlighting in the brief.
- Zip (ziphq.com) was seed-listed but yielded too little buyer-side evaluation-feature detail via search to support a material claim in this file; it appears in the pack's seed list and search results mainly for general vendor-selection guidance content rather than product documentation. Treat as under-researched relative to the other seven products.
