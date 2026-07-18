# Verification report: 2026-07-rfp-workflow-ux

## Material claims checked

The list of 17 material claim-clusters below was supplied verbatim by the
Research Lead in the verifier's task prompt (not derived by the verifier).
The Lead also flagged known source-quality issues in advance (S101–S103,
S105–S108, S112, S116 obtained via search-tool excerpt after HTTP 403s;
S205, S212, S214 are search-engine syntheses, not directly-read documents)
and asked that these be weighed explicitly. Both inputs are recorded here
for audit purposes; this verifier did not propose or alter the cut.

WS1 (`findings/ws1-competitor-landscape.md`): (1) Bonfire consensus-override
scoring/divergence-triggered review [S101]; (2) Bonfire Rated Scale vs
Pass/Fail criteria types [S102]; (3) SAP Ariba grading modes [S105, S106];
(4) auto-award-recommendation cluster — JAGGAER IAN [S109], Ivalua SDC
[S111], SAP Ariba award/optimization + ML recommendations [S108], plus the
Inference built on them [from S108, S109, S111]; (5) audit-trail-as-baseline
[S104, S107, S110, S111, S112] plus its Inference.

WS2 (`findings/ws2-procurement-workflow.md`): (6) individual scoring first,
then moderated consensus not averaging [S202, S205, S210]; (7)
criteria/weights locked before proposals seen [S206, S212]; (8) GAO gives
controlling weight to the contemporaneous record [S203]; (9) mandatory
screening before/separate from scoring [S202, S207]; (10) evaluator COI
declarations and pre-consensus confidentiality [S205, S206].

WS3 (`findings/ws3-ux-patterns.md`): (11) Bonfire 30%-spread "Lack of
Consensus" highlighting [S302, S305]; (12) Bonfire predefined
reason-per-score-band input [S304]; (13) question-anchored vs
vendor-anchored traversal [S310]; (14) Bonfire consensus overrides average
and becomes ranking input [S301]; (15) Bonfire per-evaluator progress bars
[S305]; (16) Ivalua agentic "making an award" language [S316] and
advisory-recommendation framing [S315], plus the Inferences from
S315/S316; (17) pass/fail vs graduated scoring must stay distinct (legal
commentary) [S319].

Method: each cited source was re-opened at its ledger URL (direct
WebFetch; where that returned HTTP 403, a JS-rendered empty shell, or
corrupted PDF binary, a targeted WebSearch and/or an alternate URL mirror
was tried as a second attempt, consistent with the mission's "try again,
try archive.org" instruction — `web.archive.org` fetches were attempted
but this environment's WebFetch tool refused them outright, so search-tool
re-derivation was the only available fallback for previously-403'd
sources).

## Per-claim verdicts

1. **WS1 §Consensus and moderation, S101 sentence.** `[Evidence: S101] [Verified: 2026-07-18]`. Direct fetch still returns 403, but a targeted WebSearch retrieved matching text from the live support page confirming the override mechanic, the "enter scores for criteria that haven't been scored at all" detail, and that the Consensus Score overrides the Average Score and becomes the ranking input — matches the claim as written.

2. **WS1 §Individual scoring and weighting, S102 sentence.** `[Evidence: S102] [Verified: 2026-07-18]`. WebSearch confirms Pass/Fail criteria "are not assigned any weighting" and Rated Scale criteria are weighted — matches exactly.

3. **WS1 §Individual scoring and weighting, S105/S106 sentence.** `[Evidence: S105, S106] [Verified: 2026-07-18]`. WebSearch retrieved the SAP Help Portal text directly: three event rules including "Enable approval for team grading," blind grading definition, and weight-points mechanics — matches.

4a. **WS1 §Award justification, JAGGAER (S109) bullet.** `[Evidence: S109] [Disputed: 2026-07-18 — see findings file for full reason]`. The IAN mechanic description and "under the full control of the human operator" quote are confirmed present on S109's own blog page (direct fetch). But the "the constraints, scenarios and supplier inputs behind it" and "Auditable, explainable and ready for finance, risk and the C-suite" quotes are **not** on S109 — a direct, targeted re-fetch of S109 confirmed both phrases absent — and are instead confirmed present on **S110** (JAGGAER's Sourcing Optimization page, correctly cited for the same wording elsewhere in this same findings file's Audit Trail section). This is a source misattribution, not an unsupported claim: the content exists and is in the ledger, just under the wrong ID.

4b. **WS1 §Award justification, Ivalua (S111) bullet.** `[Evidence: S111] [Verified: 2026-07-18]`. Direct fetch confirms "Sourcing Decision Center uses AI and mathematical optimization... helping you make the best allocation decisions faster and with full transparency."

4c. **WS1 §Award justification, SAP Ariba (S108) bullet.** `[Evidence: S108] [Verified: 2026-07-18]`. Direct fetch of S108 itself returned only a page title (same JS-rendering issue the investigator flagged), but WebSearch retrieved matching text from the same URL/topic confirming the "Best Bid" optimization scenario, "determine the optimal suppliers and allocations," and ML-based supplier recommendations. Residual note: the exact ML/historical-data quote could not be pinned to this specific URL versus a closely adjacent SAP help page in the same guided-sourcing documentation set — flagged as a minor residual uncertainty below, not disputed, since the core award-scenario claims are solidly confirmed for this URL.

4d/4e. **WS1 §Award justification, two Inference sentences.** `[Inference: from S108, S109, S111] [Verified: 2026-07-18]` and `[Inference: from S108, S109, S110, S111] [Verified: 2026-07-18]`. Neither inference depends on the specific misattributed quote in 4a — both hold on the broader confirmed theme (each vendor markets a computed "optimal"/"recommended" award).

5. **WS1 §Audit trail, all five sentences plus the closing Inference.** `[Evidence: S107] [Verified: 2026-07-18]`, `[Evidence: S112] [Verified: 2026-07-18]`, `[Evidence: S110] [Verified: 2026-07-18]`, `[Evidence: S111] [Verified: 2026-07-18]`, `[Evidence: S104] [Verified: 2026-07-18]`, and `[Inference: from S104, S107, S110, S111, S112] [Verified: 2026-07-18]`. S104, S110, S111 confirmed by direct fetch; S107 and S112 confirmed by WebSearch re-derivation of the exact quoted text (same 403 workaround the investigator used, independently reproduced here).

6. **WS2 §Sequence, three sentences.**
   - S202 sentence: `[Evidence: S202] [Verified: 2026-07-18]` — direct fetch confirms "a simple averaging of the individual evaluation results does not constitute consensus" verbatim, plus the minority-opinion provision.
   - S205 sentence: `[Evidence: S205] [Disputed: 2026-07-18 — see findings file]`. The cited PDF returned only binary/unparseable content under three separate URL variants tried (doa.mt.gov as ledgered, plus spb.mt.gov and mt.gov mirrors found via search) — this matches the Lead's known flag; the general idea is widely repeated elsewhere but the specific Montana document could not be independently read or confirmed in this session.
   - S210 sentence: `[Evidence: S210] [Disputed: 2026-07-18 — see findings file]`. **Two independent, carefully targeted direct fetches** of the cited GOV.UK page found neither the word "moderation" nor the quoted "considered independently"/"must not be influenced by comparable scores" language anywhere on the page. This looks like content from a different UK procurement-commentary source (moderation-meeting blogs) misattributed to S210.

7. **WS2 §Weighting locked, two sentences.**
   - S206 sentence: `[Evidence: S206] [Verified: 2026-07-18]` — direct fetch confirms "This information must be final and documented in the evaluation strategy prior to completing the solicitation documents" verbatim.
   - S212 sentence: `[Evidence: S212] [Disputed: 2026-07-18 — see findings file]`. S212 is a search-engine synthesis per the Lead's known flag, not a single directly-read document. This verifier located the exact quote on a single directly-readable page (steerlab.ai — proposed below as S901) confirmed by direct fetch, but the findings text still cites only S212, which cannot itself be re-opened as one source. Recommend re-citing to S901 (see Sources proposed).

8. **WS2 §Documentation, all three S203 sentences plus its Inference.** `[Evidence: S203] [Verified: 2026-07-18]` (x3, one per sentence) and `[Inference: from S203, S202] [Verified: 2026-07-18]`. Direct fetch of the law-firm commentary confirms the contemporaneous-record principle, the specific 2025 CMS/Superior Health protest detail, and that GAO rejected post-hoc materials "never mentioned in the contemporaneous evaluation record."

9. **WS2 §Mandatory gates, all three sentences.** `[Evidence: S202] [Verified: 2026-07-18]`, `[Evidence: S207] [Verified: 2026-07-18]`, and `[Evidence: S202, S207] [Verified: 2026-07-18]` (the combined closing sentence). S202's initial-screening step and S207's Maryland "preliminary verification of bid responsiveness... before distributing materials to evaluators" both confirmed by direct fetch, matching the claim closely.

10. **WS2 §Roles, COI/confidentiality sentence [S205, S206].** `[Evidence: S205, S206] [Verified: 2026-07-18]`. S206 alone fully and directly confirms the claim (direct fetch: "Read, sign and submit a conflict of interest form," "Keep rating confidential during individual scoring," no discussion outside committee meetings). S205 remains unreadable per the known flag (same as claim 6) but the claim does not rest solely on it, so it stands as Verified on S206's strength.

11. **WS3 §Evaluator divergence, S302/S305 sentence.** `[Evidence: S302, S305] [Verified: 2026-07-18]`. WebSearch confirms the 30% threshold, the 3-point-on-10 worked example, the orange highlighting, and the "Scoring Summary" view name — all attributable to S302 alone, so this claim does not actually need S305 to hold (S305's whitepaper PDF could not be read directly in this session; not disputing, since S302 fully carries the claim).

12. **WS3 §Scoring input, S304 sentence.** `[Evidence: S304] [Verified: 2026-07-18]`. WebSearch confirms the predefined Reason requirement, the Low/Medium/High reason-set categories, and that the set updates to match the entered score.

13. **WS3 §Side-by-side comparison, S310 sentence plus its two Inferences.** `[Evidence: S310] [Verified: 2026-07-18]` and `[Inference: from S310] [Verified: 2026-07-18]` (x2). Direct fetch confirms the "line up questions and answers side by side" quote verbatim and the linguistic-anchor (unacceptable/poor/satisfactory/good/excellent) scale.

14. **WS3 §Moderation, S301 sentence.** `[Evidence: S301] [Verified: 2026-07-18]`. WebSearch confirms the Consensus Score "overrides the Average Score and is the score that's used in the calculation to rank vendors" verbatim.

15. **WS3 §Progress/completeness, S305 sentence.** `[Evidence: S305] [Verified: 2026-07-18]`. Direct PDF fetch failed (unparseable, same as S305's other citation above), but WebSearch retrieved matching indexed text ("Progress Bar for each set that will fill in with green when completed... percentage of completion") consistent with the claim.

16. **WS3 §Stance-sorting, three S315/S316 bullets plus two Inferences.**
   - "Making an award" bullet (S316): `[Evidence: S316] [Verified: 2026-07-18]` — direct fetch confirms the exact phrase verbatim, plus a human-in-the-loop recommendation elsewhere in the same piece (both correctly noted as needing to be read together in the findings text).
   - Tail-spend bullet (S316): `[Evidence: S316] [Disputed: 2026-07-18 — see findings file]`. A direct, targeted fetch of S316 searching specifically for "tail-spend"/"unmanaged spend"/autonomous-triggering language found **no match anywhere on the page**. Two related Ivalua pages (agentic-ai-in-procurement, ai-in-sourcing-and-procurement) were also checked directly and do not contain it either. A WebSearch synthesis asserted the quote existed, but repeated direct fetches could not locate it on any Ivalua page reachable in this session — the quote's source cannot be confirmed and may be a search-tool fabrication rather than a genuine misattribution.
   - Advisory-framing bullet (S315): `[Evidence: S315] [Verified: 2026-07-18]` — direct fetch confirms the "helping you make the best allocation decisions faster" framing.
   - Both Inferences: `[Inference: from S315, S316] [Verified: 2026-07-18]` (appears twice in the findings text) — hold on the confirmed "making an award" and advisory-framing content; do not depend on the disputed tail-spend quote.

17. **WS3 §Mandatory-gate pattern, S319 sentence plus its Inference.** `[Evidence: S319] [Verified: 2026-07-18]` and `[Inference: from S319] [Verified: 2026-07-18]`. Direct fetch confirms the pass/fail-must-be-explicit legal principle and the MOD case reference.

**Note:** items 4a, 6 (S210 line), and 7 (S212 line) below were later re-cited by
the authors and re-verdicted in the "Addendum: re-verdict pass" section
further down this document — that addendum supersedes the verdict recorded
for those three specific citations here; the entries below are left as the
historical record of the first pass and are not retroactively edited.

## Summary counts

- Claims/claim-clusters checked (per the Lead's list): 17, comprising 36 individually-tagged sentences/bullets across the three findings files (9 in WS1, 13 in WS2, 14 in WS3 — some clusters combine multiple separately-cited sentences, each getting its own verdict tag).
- Verified: 31 individually-tagged instances.
- Disputed: 5 individually-tagged instances — WS1 claim 4a (JAGGAER S109 quote misattribution), WS2 claim 6 (S205 unreadable, S210 quote not on page — 2 instances), WS2 claim 7 (S212 search-synthesis ungrounded as cited), WS3 claim 16 (tail-spend S316 quote unconfirmed).
- Hypotheses: all carry "Validate by:" lines in all three findings files — no contract violations found on this front (spot-checked every `[Hypothesis]` tag in WS1, WS2, WS3).

## Contract violations found

1. **WS1, JAGGAER IAN bullet (claim 4a):** quotes attributed to S109 that are not present on S109's page but are present on S110's page, which is already correctly cited elsewhere in the same document for the same wording. This is an internally inconsistent citation — the author had the correct source for this material two paragraphs away. Recommend the Lead/author re-cite this sentence's second half to S110 (or S109, S110 jointly) rather than downgrading the claim, since S110 does directly support it.
2. **WS2, S210 sentence (claim 6):** the quoted "moderation meeting" / "considered independently" language does not appear on the cited GOV.UK page under two independent direct-fetch attempts. No alternate source for this specific quote was identified in this session. Recommend downgrade to Inference (UK guidance is consistent with, but does not itself state, the moderation-meeting mechanics — that mechanic is documented by S208, already in the ledger as practitioner commentary) or retraction of the specific sentence.
3. **WS3, tail-spend bullet (claim 16):** quote not locatable on S316 or two adjacent Ivalua pages after direct fetch; the only "confirmation" came from a WebSearch synthesis that could not be tied to any single fetchable page. Recommend downgrade to Hypothesis (with a Validate-by line) or retraction pending a human check of Ivalua's site directly.
4. No missing "Validate by:" lines were found on any `[Hypothesis]` tag in any of the three findings files — this specific contract requirement is satisfied throughout.
5. One near-violation flagged but not treated as a contract breach: WS2's debriefing-artefact paragraph carries `[Evidence: S213]; [Hypothesis]` back-to-back with a "Validate by: none needed for this mission" line. This satisfies the literal contract requirement (a Validate-by line is present) but is worth the Lead's attention as an unusual construction — a Hypothesis that explicitly declines validation reads more like a scope note than an open belief; consider whether it should instead be plain prose outside the claim-tag system.

## Proposed retractions (Lead decides)

- **S205** (Montana RFP Evaluation Process Instructions PDF): unreadable across three URL variants tried by both the original investigator and this verifier (doa.mt.gov as ledgered, plus spb.mt.gov and mt.gov mirrors). Every claim citing it also cites a second, directly-confirmed source (S202/S206), so no claim currently depends on it alone — but as a standing ledger entry it cannot be verified and should either be retracted or replaced with a readable Montana-guidance mirror if a future claim needs it as sole support.
- No other retraction is proposed. S109, S110, S210, and S316 are all real, reachable, directly-fetchable sources that remain valid for other claims already correctly citing them — the issues found are citation/quote-attribution errors, not source unreliability.

## Sources proposed (S901+)

### S901 — SteerLab: "What Is RFP Evaluation Criteria? A Buyer's Guide"
- URL: https://www.steerlab.ai/blog/what-is-rfp-evaluation-criteria
- Type: vendor-site
- Accessed: 2026-07-18
- Credibility: commentary
- Added by: evidence-verifier
- Notes: Directly fetched; contains the exact quote "The most damaging mistake is finalizing criteria after proposals arrive. Once you've seen what vendors are offering, any adjustment to weights or criteria is subject to bias," currently attributed in WS2's findings to S212 (a search-engine synthesis composited across multiple sites, not a single directly-read document). Proposed so the Lead can re-cite WS2 claim 7's second sentence to a source that can actually be re-opened and confirmed.

## Addendum: re-verdict pass (2026-07-18)

Following the Lead's acceptance of the first-pass report — S205 retracted in
`ledger.md`, S901 merged, and the authors' re-citations applied in the
findings files — the coordinator asked for a re-verdict of six specific
re-cited claims plus a check that the author-applied Downgraded verdict
tags carry "Validate by:" lines. This addendum was scoped to exactly those
six claims and the Downgraded-tag check; it does not re-open any other
claim already Verified/Disputed in the body above.

1. **WS1, JAGGAER IAN bullet, now `[Evidence: S109, S110]`.** `[Evidence: S109, S110] [Verified: 2026-07-18]`. The re-cited sentence now correctly separates the two quotes: "under the full control of the human operator" to S109 (confirmed present on S109's blog page by direct fetch in the original pass) and "the constraints, scenarios and supplier inputs behind it" / "Auditable, explainable and ready for finance, risk and the C-suite" to S110 (confirmed present on S110's Sourcing Optimization page by direct fetch in the original pass). Both attributions now hold — the original misattribution is fixed.

2. **WS2, §Sequence moderation-meeting sentence, now `[Evidence: S208]`.** `[Evidence: S208] [Verified: 2026-07-18]`. Direct fetch of S208 (Thornton and Lowe) confirms independent scoring first ("Each evaluator must score independently first. Then meet to agree on final moderated scores through group discussion"), a scheduled "moderation meeting," and discussion-based consensus rather than mechanical averaging ("Look for consensus through open discussion. Avoid forcing agreement if genuine differences exist"). Minor note: the page uses "moderation meeting" only once and more often calls the overall process "moderation" generically — not material to the claim's truth, so not disputed on that basis.

3. **WS2, §Weighting locked, now `[Evidence: S901]` plus `[Inference: from S206, S901]`.** `[Evidence: S901] [Verified: 2026-07-18]` and `[Inference: from S206, S901] [Verified: 2026-07-18]`. S901 (steerlab.ai) was directly fetched and confirmed to carry the exact quote in the original pass; re-confirmed here. The Inference (Setup's approval lock reflecting a defensibility requirement) follows reasonably from S206 (already Verified) plus S901.

4. **WS2, "common scoring errors" bullet, now `[Evidence: S209]` alone.** `[Evidence: S209] [Verified: 2026-07-18]` (both sentences in the bullet). Direct fetch of S209 (Gatekeeper) confirms all five listed errors near-verbatim: unclear criteria, group influence before independent scoring, mismatched RFP/scoring-sheet criteria, overweighting low-priority items, and skipping calibration causing inconsistent scores.

5. **WS2, Documentation-section Maryland sentence and its Inference, re-cited from S205 to S207.** `[Evidence: S207] [Disputed: 2026-07-18 — see findings file]` and `[Inference: from S207, S202] [Disputed: 2026-07-18 — see findings file]`. Two independent direct fetches of the cited Maryland page (one in the original verification pass, one in this addendum) both explicitly searched for and did not find the quoted "which explain or support their score for each evaluation criterion" / "reasonable, rational, and consistent" language. A targeted WebSearch traced the "reasonable, rational, and consistent" framing instead to a Maryland State Board of Contract Appeals case discussing evaluator comment/score alignment — not to the cited manual page — and found the manual's actual per-evaluator duty narrower (evaluators "independently identify strengths and deficiencies to rank each proposal"; it is the *procurement officer*, not individual evaluators, who writes up the comparative strengths/deficiencies memo). This re-citation does not hold as given. The Inference inherits the same problem since it cites S207 jointly with S202, though S202 alone (already Verified) would independently support the general point.

6. **WS2, §Roles paragraph, now `[Evidence: S206, S207]`.** `[Evidence: S206, S207] [Verified: 2026-07-18]`. S206 (Oregon) confirms the procurement professional is "a facilitator and advisor," not a voting committee member, and separately evaluates cost while the committee scores independently and does not see cost data. S207 (Maryland) confirms the procurement officer conducts preliminary/initial review and documents the final recommendation. One caveat for the Lead: a targeted re-fetch of S207 for claim 5 above found Maryland's own commentary characterizing its process as "integrated rather than bifurcated" (the officer "guides the evaluation committee" with "real time direction") rather than a hard procurement-officer/committee wall — this is a matter of degree, not a misattribution, and the paragraph's core separation-of-duties claim still holds across both sources, but "controls all vendor communication" and "screens proposals for compliance" specifically are not verbatim in either fetched page (they generalize from role-separation language already Verified elsewhere in this same document, e.g. S207's preliminary-verification content confirmed under claim 9 above).

**Downgraded-tag check:** every Downgraded verdict tag found in the three findings files carries a "Validate by:" line immediately after (checked each occurrence individually, not just counted): four in WS2 (one from the S205 retraction at the end of the §Sequence paragraph, and three from the S212 reassessment — the practitioner-benefits-list sentence, the tools-help-with-mechanical-consistency synthesis sentence, and the halo-effect sentence, the last spanning two consecutive `[Hypothesis]`-tagged Downgraded instances each with their own Validate-by line), and one in WS3 (the tail-spend claim). No violations found.

**Remaining Disputed verdict tags anywhere in the three findings files after this pass:** exactly one claim, now carrying two Disputed tags — WS2's Documentation-section Maryland sentence (`[Evidence: S207]`) and its Inference (`[Inference: from S207, S202]`), both under item 5 above. Every other previously-Disputed tag in the three findings files has now been resolved to Verified by this addendum (or was already resolved by the author's Downgraded re-citations, which this addendum's Downgraded-tag check separately confirmed are well-formed).

## Verifier's overall assessment

The two workstreams resting most heavily on government/procurement primary
sources (WS2) and vendor product documentation (WS1, WS3) mostly held up
well under re-verification — the large majority of Evidence and Inference
claims in the material-claims list are directly supported by their cited
sources, including several (S101, S102, S107, S112, S212's underlying
content) that could only be re-confirmed through search-tool re-derivation
because direct fetch is still blocked in this environment (403s persisted;
`web.archive.org` was attempted per the mission's instruction but this
session's WebFetch tool refused to fetch it at all, so it was not a usable
fallback here). The disputed claims are concentrated in a specific failure
pattern worth flagging to the Lead directly: three of the six disputes are
**quote misattribution** — text that is real and traceable somewhere in
the source landscape, but not on the specific page the citation names.
Two of those (S109/S110, and the S212/steerlab.ai case) have an easy fix
(re-cite to the correct, already-known-good source). The S210 and
tail-spend/S316 cases are more serious because no correct alternate source
was found for the specific quoted language in this session — these should
not be treated as settled until a human re-checks them directly.
