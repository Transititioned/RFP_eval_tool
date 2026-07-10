# Product decisions

Decision record for the Capability Sourcing Workbench upgrade. Newest first.

## 2026-07-10 — Scoring model: panel scores + moderated consensus

How real RFP evaluations work, and what the product models:

- A panel of evaluators (typically Business Rep, Architecture, often a
  Tech PM) each score criteria **individually and quantitatively**.
- The panel then meets in an evaluation workshop, discusses divergent
  scores by category, and reaches **consensus** — a human decision with a
  rationale, not a computed average.
- The final result is always a mix of quantitative and qualitative.

Implications for the build:

- Individual evaluator scores per criterion are first-class data and are
  never discarded or overwritten by consensus.
- Score **variance across evaluators** is a primary signal — it drives the
  evaluation meeting focus queue.
- Consensus scores are entered by humans in the meeting, require a
  rationale, and are recorded alongside (not instead of) individual scores.
- The system never computes and asserts a final blended score or winner on
  its own. Any roll-up is a byproduct of human consensus. This preserves
  the MVP-0 principle "avoid misleading aggregate scoring" — the thing to
  avoid is the software silently declaring a winner, not scores themselves.
- Mandatory gate failures stay visible and are never hidden by scores.

## 2026-07-10 — Privacy: deferred to backlog

Proof-of-concept mock-up on a public Hugging Face Space. Synthetic/sample
data only. Real-document privacy requirements are captured in
[backlog.md](backlog.md) and must be addressed before any real vendor
proposal is uploaded.

## 2026-07-10 — Tenancy: single organisation

Build single-tenant. Multi-client/consultancy isolation is in the backlog,
much later.

## 2026-07-10 — Roadmap: north star, not a contract

The incremental build plan (12 waves, 3 releases) is a directional
reference. Prioritise freely session-to-session by value; don't treat wave
order or wave acceptance criteria as gates.
