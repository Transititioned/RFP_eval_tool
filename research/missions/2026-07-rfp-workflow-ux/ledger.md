# Source ledger: 2026-07-rfp-workflow-ux

Schema and rules: `research/core/source-ledger.md`. Written by the
Research Lead only; investigators propose sources in their findings
files using their workstream's ID block. Append-only — retract, never
delete.

## Sources

<!-- Merged verbatim from findings/ws1-competitor-landscape.md (WS1), 2026-07-18 -->

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

<!-- Merged verbatim from findings/ws2-procurement-workflow.md (WS2), 2026-07-18 -->

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
- Retracted: 2026-07-18 — unreadable across three URL variants tried by both investigator and verifier; per the evidence contract no claim may rest on it, and claims citing it must be re-supported or downgraded (verifier report, accepted by Lead).

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

<!-- Merged verbatim from findings/ws3-ux-patterns.md (WS3), 2026-07-18 -->

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

<!-- Merged verbatim from verification.md (verifier proposal, S901+ block), 2026-07-18 -->

### S901 — SteerLab: "What Is RFP Evaluation Criteria? A Buyer's Guide"
- URL: https://www.steerlab.ai/blog/what-is-rfp-evaluation-criteria
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: commentary
- Added by: evidence-verifier
- Notes: Directly fetched; contains the exact quote "The most damaging mistake is finalizing criteria after proposals arrive. Once you've seen what vendors are offering, any adjustment to weights or criteria is subject to bias," currently attributed in WS2's findings to S212 (a search-engine synthesis composited across multiple sites, not a single directly-read document). Proposed so the Lead can re-cite WS2 claim 7's second sentence to a source that can actually be re-opened and confirmed.
