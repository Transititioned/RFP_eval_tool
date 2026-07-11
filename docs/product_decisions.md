# Product decisions

Decision record for the Capability Sourcing Workbench upgrade. Newest first.

## 2026-07-11 — Scoring model: add traditional weighted mode alongside panel consensus

Revisits the blanket "no weighted scores" hard limit from 2026-07-10. The
original rationale was narrower than the limit implied: the risk being
managed is *automated decision-making* — the tool silently declaring a
winner — not scoring itself. That's the right default caution for
AI-generated tooling, but it's overcalibrated here: this product is
decision *support*, not decision *making*, and criteria x weight scoring
is the model most procurement governance processes already require and
can defend to auditors. Excluding it outright makes the tool harder to
adopt inside real procurement processes without a compensating benefit.

Decision:
- Add "Traditional weighted" as a second, selectable Compare-tab scoring
  mode alongside "Panel + Consensus". Criteria x weight -> total per
  vendor, displayed and sortable.
- The non-negotiable rule both modes obey: the tool may compute and
  display a score or ranking, but "Recommended supplier" is always a
  separate, deliberate, human-entered action — never an automatic
  rendering of the top-ranked total. This is the actual boundary between
  decision support and decision making, and it's the part of the
  2026-07-10 decision that stays intact.
- Mandatory gates continue to sit outside both scoring modes and are
  never diluted by score, in either mode.
- Panel + Consensus remains the default/recommended mode; Traditional
  weighted is an alternative, not a replacement — offered because
  procurement is often a gatekeeper on RFP processes and traditional
  scoring is what their governance expects.

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
