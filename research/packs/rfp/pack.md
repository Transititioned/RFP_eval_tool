# RFP Product Research Pack

Domain knowledge for researching the RFP / proposal-evaluation /
eSourcing product space. Domain-neutral method lives in `research/core/`;
this pack supplies what to look at and how to judge sources *in this
domain*. It contains nothing specific to the Capability Sourcing
Workbench — that lives in `research/context/`.

## The domain, briefly

"RFP software" spans several overlapping markets. Be precise about which
segment a product serves, because their workflows and UX differ:

- **Buyer-side sourcing/evaluation** — issuing RFPs, collecting vendor
  responses, scoring, awarding (e.g. eSourcing modules of procurement
  suites, standalone evaluation tools). *This is the segment closest to
  our interest.*
- **Vendor-side response management** — bid teams answering RFPs
  (content libraries, answer automation). Adjacent, studied mainly for
  UX patterns, not workflow.
- **Public-sector eProcurement** — regulated tendering with formal
  compliance gates, audit trails, and published evaluation methodology.
  A rich source for governance expectations.

## Seed product list (objects of study)

Starting points, not a census — investigators should extend it and note
segment per product. Naming real products in research artefacts is
expected and fine; this material must never be copied into app sample
data (see `research/README.md`, Boundaries).

- Buyer-side / eSourcing: SAP Ariba Sourcing, Coupa Sourcing, JAGGAER,
  Ivalua, Zip, Vendorful, Prokuria, Euna (Bonfire) — Bonfire's
  evaluator scoring UX is specifically worth study.
- Vendor-side (UX patterns): Responsive (formerly RFPIO), Loopio,
  Qvidian/Upland, QorusDocs.
- Public-sector: e-tendering portals and published government evaluation
  handbooks (often the best *primary* workflow sources).

## Standing research questions by workstream lens

**Competitor landscape (competitor-scout):** Which products serve
buyer-side evaluation? What is their feature checklist for the
evaluate/score/award stages — individual scoring, consensus/moderation,
weighting, mandatory gates, conflict-of-interest handling, audit trail,
award justification? What do they *not* do? How do they price/position
(enterprise suite vs point tool)?

**Procurement workflow practice (procurement-analyst):** How do real
evaluation panels run — roles, sequence, governance sign-offs? What do
government/enterprise procurement handbooks mandate about evaluation
methodology, scoring records, and auditability? Where do practitioners
say tools help or get in the way (forums, practitioner communities)?
What audit artefacts must an evaluation produce?

**UX patterns (ux-pattern-analyst):** How do evaluation tools present
scoring input, side-by-side comparison, progress/completeness,
divergence between evaluators, and moderation workflows? What patterns
appear repeatedly (matrix grids, traffic lights, per-criterion drill-in,
evaluator dashboards)? Which patterns respect "human decides" and which
push auto-ranking? Screenshots/tours/demo videos and review-site
screenshots are the raw material.

## Source-quality guidance for this domain

- **Vendor sites/docs** — primary for "the product has feature X";
  commentary for "feature X works well". Marketing pages overstate;
  product documentation and release notes understate — prefer docs.
- **Review aggregators (G2, Capterra, TrustRadius)** — commentary;
  useful in volume for recurring praise/complaint themes, unreliable for
  any single claim. Note review counts.
- **Government procurement guidance** (e.g. national/state procurement
  handbooks, EU directives material) — primary for workflow and
  governance expectations, and freely citable.
- **Analyst content (Gartner/Forrester/Spend Matters)** — secondary;
  paywalled summaries often circulate — cite only what is actually
  accessible at the recorded URL.
- **Practitioner forums (r/procurement, LinkedIn posts, blogs)** —
  commentary; good for hypotheses, rarely for evidence.

## Domain-specific claim cautions

- Feature-list claims go stale fast — always record `Accessed` dates and
  prefer current product docs over review-site feature matrices.
- "Industry standard" claims are almost always Inference or Hypothesis,
  not Evidence — one vendor doing something is not a standard.
- Distinguish *workflow* claims (what panels must do) from *feature*
  claims (what tools offer) from *UX* claims (how tools present it);
  keep them in their own workstream's findings.
