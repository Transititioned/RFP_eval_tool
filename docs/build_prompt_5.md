# Build prompt 5 — Synthetic RFP upload + AI read-in (flow test)

*Drafted 2026-07-11 to pick up the build. Paste the body below as the next
build prompt. Precondition first.*

**Precondition (manual, before starting):** switch the HF Space to
private (Space Settings → visibility → private). Per the 2026-07-11
future-direction decision, synthetic-document upload is only in scope
once the Space is private. Do not start the build until this is done.

---

Use the data-specialist subagent for sample synthetic RFP documents, the
logic-specialist subagent for the read-in/verification logic, and the
ui-specialist subagent for the screens. Synthetic (fake) documents only —
the synthetic-data-only rule is the operative protection.

Upload: add a per-vendor upload control to the Proposals tab accepting a
small synthetic RFP response document (plain text / markdown first; PDF
can wait). Session-only — do NOT persist uploaded files anywhere
(persistence stays limited to the intake log; expanding it needs a
separate decision). Uploading updates the vendor's readiness status
appropriately (e.g. to "Loaded").

Read-in: new logic module (e.g. app/logic/readin.py) that extracts
candidate evidence per criterion from an uploaded document, producing
records in the existing RESPONSES shape: evidence reference (quote +
location in the document — citations are the point), confidence, gaps.
Two extraction backends behind one interface, mirroring the HF_TOKEN
pattern: if an ANTHROPIC_API_KEY Space secret is set, use the Claude API
for extraction; without it, fall back to a clearly-labeled deterministic
demo extractor (simple keyword/section matching) so the flow is testable
with no key and no cost. The UI must always show which backend produced
an extraction.

Verification queue — the load-bearing part: every extraction lands as
UNVERIFIED and must be explicitly confirmed or rejected by a human
before it counts toward anything. Unverified items are visibly flagged
(same visibility principle as NOT ANSWERED and provisional weighted
totals). Verified evidence merges into a session-level copy of the
responses used by the Evaluation tab's Compare view, clearly
distinguished from the built-in sample data; if that merge proves too
heavy for this pass, a standalone extraction-review panel is an
acceptable fallback — flag the choice. Rejecting an extraction requires
no reason; verifying is one click; both are logged (timestamped,
append-only, session-only, matching the existing state-machine
conventions).

Hard boundaries, per the 2026-07-11 decision: AI extracts and cites —
it never scores, never fills in a panel score, never drafts a consensus,
and nothing from the read-in touches rankings, shortlist, or
recommendation. No AI lens cross-check in this pass (that's the pass
after this one, once read-in works). Restrained copy: this is
evidence extraction with citations, not "AI assessment."

When done: update CLAUDE.md/README.md architecture and tab list
(including the staging notes — synthetic upload is now shipped, so the
hard-limits wording needs reconciling again), extend the test suites
for the new logic (the demo extractor makes the pipeline unit-testable
without an API key), run scope-guardian and report what it flags.
