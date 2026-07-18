# Evidence contract

Every material claim in a findings file or decision brief carries exactly
one classification tag. The tag formats below are machine-checked by
`research/validate.py` — use them exactly.

## The three classifications

| Class | Meaning | Tag format |
|---|---|---|
| **Evidence** | Directly supported by a cited source in the mission ledger — the source states this, and a reader following the citation would agree | `[Evidence: S101]` or `[Evidence: S101, S204]` |
| **Inference** | An interpretation or generalisation *of* cited evidence — the sources don't state this, but it follows from them; the reasoning must be visible in the surrounding text | `[Inference: from S101, S204]` |
| **Hypothesis** | Not yet validated — a belief, pattern-guess, or open question; must be accompanied by a "Validate by:" line saying what would confirm or refute it | `[Hypothesis]` |

Rules:

- Tags cite ledger source IDs (`S<number>`). Citing a source that is not
  in the mission's `ledger.md` (or the investigator's proposed-sources
  block destined for it) is a contract violation.
- Single-source citations are valid in both cited forms:
  `[Evidence: S101]` and `[Inference: from S101]`.
- `[Hypothesis]` takes no citation. If specific sources prompted the
  guess without supporting it, name them in the surrounding prose
  ("prompted by S101") so the provenance isn't lost.
- Evidence must not stretch: if the source says "vendor X offers weighted
  scoring" and the claim is "weighted scoring is the industry standard",
  that is an Inference (or a Hypothesis), not Evidence.
- A Hypothesis is not a lesser claim to be hidden — it is often the most
  decision-relevant item in a brief. It just cannot be presented as fact.
- Quotes used as evidence should be short and attributed; findings record
  where in the source the support lives when the source is long.

## Verification tags (applied by the Evidence Verifier only)

The verifier re-opens cited sources for material claims and appends one
verdict tag after the classification tag:

| Verdict | Meaning |
|---|---|
| `[Verified: 2026-07-18]` | Source checked; it supports the claim as classified |
| `[Disputed: 2026-07-18 — <one-line reason>]` | Source checked; support is weaker than claimed, contradicted, or unreachable. The reason is mandatory |

A verdict tag sits immediately after the classification tag it judges —
a free-floating verdict tag is malformed. One verdict tag per claim.

## Downgrades (applied by the claim's author or the Lead, never the verifier)

A Disputed claim must be resolved before the brief is finalised:
Evidence → Inference or Hypothesis; Inference → Hypothesis; or the claim
is retracted (struck through with a dated note, never deleted). The
verifier flags; the claim's author or the Lead applies the downgrade
(the Lead's authority for this specific edit is granted in
`research-core.md` write-ownership, and every downgrade is logged in
`state.md`). Mechanics:

- Replace the classification tag with the downgraded class. A downgrade
  to Hypothesis must add the required "Validate by:" line.
- Replace the triggering `[Disputed: ...]` tag with
  `[Downgraded: YYYY-MM-DD — from Evidence]` (or `— from Inference`), so
  a `[Disputed: ...]` tag still present always means "not yet resolved".
- A `[Verified: ...]` tag never survives a downgrade — nor the
  retraction of the source it relied on. Remove it; the claim may be
  re-verified in its new form.

## Worked example

The block below is valid contract usage and doubles as a parser self-test
for `research/validate.py`. Source IDs here are illustrative.

<!-- contract-example:start -->
Vendor Alpha's product includes side-by-side proposal comparison
[Evidence: S101] [Verified: 2026-07-01]. Both Alpha and Beta gate
mandatory requirements before scoring [Evidence: S101, S102]. Buyers in
this segment appear to expect gate-before-score ordering as a default
[Inference: from S101, S102]. Vendor Beta's consensus module supports
moderated workshops [Evidence: S103] [Disputed: 2026-07-02 — source
describes a roadmap item, not a shipped feature]. Per-criterion weight
configuration is standard in this segment [Inference: from S101]
[Downgraded: 2026-07-02 — from Evidence]. Consensus-workshop support is
a differentiator rather than a baseline feature [Hypothesis].
Validate by: checking feature lists of five more products for
workshop/moderation support.
<!-- contract-example:end -->
