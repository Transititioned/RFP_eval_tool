# Source ledger schema

Each mission keeps one `ledger.md` — the structured register of every
source any claim cites. The ledger is append-only: entries are corrected
or marked retracted in place, never deleted, so citations stay resolvable
for the life of the mission.

## Write ownership and ID blocks

Only the **Research Lead** writes `ledger.md`. Investigators *propose*
sources inside their own findings file, in a `## Sources proposed`
section, using entries in the exact schema below with IDs drawn from
their workstream's pre-allocated block (declared in `mission.md`, e.g.
WS1 = S101–S199, WS2 = S201–S299). Blocks never overlap, so the Lead
merges proposed entries into the ledger verbatim during the Merge phase
and no claim tag ever needs renumbering. The verifier and contrarian may
also propose sources (Lead assigns them the S901+ block).

## Entry schema

```
### S101 — <short source title>
- URL: <full URL, or "offline: <description>" for non-web sources>
- Type: vendor-site | product-docs | review-aggregator | analyst |
        government-guidance | forum | academic | news | other
- Accessed: YYYY-MM-DD
- Credibility: primary | secondary | commentary
- Added by: <role, e.g. competitor-scout (WS1)>
- Notes: <one line — what this source is good for, and any bias to
        keep in mind (a vendor's own site is primary for "what the
        product offers", commentary for "whether it is good")>
```

All six fields are required. `Credibility` describes the source's
relationship to the claim it supports, so the same site can be primary
for one kind of claim and commentary for another — when in doubt, note
the distinction in `Notes`.

## Retraction

If a source turns out to be unreachable, misread, or untrustworthy, the
Lead appends `- Retracted: YYYY-MM-DD — <reason>` to the entry. Claims
citing a retracted source must be re-supported or downgraded per the
evidence contract.

## Example entry

<!-- ledger-example:start -->
### S101 — Vendor Alpha product tour
- URL: https://example.com/alpha/product
- Type: vendor-site
- Accessed: 2026-07-01
- Credibility: primary
- Added by: competitor-scout (WS1)
- Notes: Feature claims only; marketing copy, treat capability depth as unverified.
<!-- ledger-example:end -->
