# WS1: Category/backend capabilities

## Scope used

- Products inspected: Vendorful, Euna Procurement, Prokuria, DeepStream, OpenGov.
- Sources used: five official product or support pages.
- Saturation or coverage note: evaluation structure, panel scoring and
  comparison repeated quickly. Supplier discovery, contracting and full
  source-to-pay capabilities were intentionally outside this decision.

Sources:

1. Vendorful e-RFX — https://vendorful.com/e-sourcing/strategic-sourcing-rfp-rfi-rfq/
2. Euna Procurement Sourcing — https://eunasolutions.com/solutions/procurement/sourcing/
3. Prokuria automated scoring — https://support.prokuria.com/buyers-sourcing-managers/requests-rfq-rfp-rfi/scoring-create-an-automated-scoring-for-your-request/
4. DeepStream supplier analysis — https://www.deep.stream/rfx-software/supplier-analysis
5. OpenGov Procurement FAQ — https://opengov.com/faq/procurement/

## Observations

| Product | Capability or pattern | Layer | Observation | Source | Signal | Limitation |
|---|---|---|---|---|---|---|
| Vendorful, Euna, Prokuria, DeepStream, OpenGov | Configurable evaluation framework | Backend/workflow | Products structure questions or criteria and support consistent scoring; weights and scorecards are common mechanisms. | Sources 1–5 | Common | Public pages do not expose every rule or data shape. |
| Vendorful, Euna, OpenGov | Multi-evaluator scoring | Backend/workflow | Subject-matter experts or invited stakeholders score responses in a shared evaluation workspace. | Sources 1, 2, 5 | Common | Permission and persistence depth varies. |
| Vendorful, DeepStream, OpenGov | Side-by-side response and score comparison | Backend/workflow | Supplier responses or evaluations can be compared against the same question or scorecard rather than assembled manually. | Sources 1, 4, 5 | Common | Product pages show the capability more clearly than its performance at scale. |
| Euna, OpenGov | Individual-to-consensus evaluation | Backend/workflow | Products explicitly support internal stakeholders and individual or consensus evaluation methods. | Sources 2, 5 | Emerging | The exact moderation mechanics are not fully public. |
| Euna, Vendorful | Guardrails and controlled collaboration | Backend/workflow | Permissions, workflow controls, error checks and audit trails keep a multi-person sourcing process controlled. | Sources 1, 2 | Emerging | Enterprise controls can become category bloat for a small app. |

## Candidate details

- **Configurable framework:** category-essential but already strong locally.
- **Live multi-evaluator scoring:** the load-bearing execution capability missing
  from the current UI; the smallest useful version is session-only.
- **Side-by-side comparison:** category-essential and already strong locally.
- **Individual-to-consensus workflow:** category-relevant and already strong in
  logic, but currently runs over sample individual scores.
- **Controlled collaboration:** retain progress visibility and reasons; do not
  copy enterprise permission or workflow engines.

## Recommended shortlist

1. Configurable evaluation framework.
2. Live multi-evaluator scoring.
3. Side-by-side response and score comparison.
4. Individual-to-consensus workflow.
5. Evaluator progress and controlled decision history.

## Follow-on gaps

The scan did not test supplier portals, questionnaire authoring, contracting,
or cross-system integrations because they do not determine the next evaluation
MVP.
