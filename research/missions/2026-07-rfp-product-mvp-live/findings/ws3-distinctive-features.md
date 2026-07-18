# WS3: Distinctive features

## Scope used

- Products inspected: Vendorful, Ivalua, JAGGAER, Euna Procurement, DeepStream.
- Sources used: five official product pages or product explanations.
- Saturation or coverage note: advanced products converge on automation and
  optimisation, but most of that is poor fit here. The useful space is guided
  human judgement, not an automated award.

Sources:

1. Vendorful e-RFX and blind evaluation — https://vendorful.com/e-sourcing/strategic-sourcing-rfp-rfi-rfq/
2. Ivalua Source-to-Contract — https://www.ivalua.com/solutions/process/source-to-contract/
3. JAGGAER Intelligent Award Navigator — https://www.jaggaer.com/blog/intelligent-award-navigator-think-big
4. Euna Procurement Sourcing — https://eunasolutions.com/solutions/procurement/sourcing/
5. DeepStream RFP automation — https://www.deep.stream/blog/rfp-automation

## Observations

| Product | Capability or pattern | Layer | Observation | Source | Signal | Limitation |
|---|---|---|---|---|---|---|
| Vendorful | Blind individual evaluation | Distinctive | Supplier identity can be hidden during response scoring to reduce bias. | Source 1 | Isolated | Identity can leak through response content; permissions are not in current scope. |
| Ivalua | Questionnaire analysis with follow-up prompts | Distinctive | An agent summarises responses, flags risks and suggests follow-up questions rather than only producing a score. | Source 2 | Isolated | AI and generated clarifications require an explicit local product decision. |
| JAGGAER | Pairwise trade-off elicitation | Distinctive | The user repeatedly chooses between feasible scenarios so the system learns decision preferences. | Source 3 | Isolated | Built for complex optimisation and far beyond the next MVP. |
| Euna, DeepStream | Guardrailed, auditable award preparation | Distinctive | Workflow guardrails and traceable records support a defensible award without removing human control. | Sources 4, 5 | Emerging | Much of the surrounding enterprise suite is unnecessary locally. |
| Euna plus current app | Disagreement-led human workshop | Distinctive | Consensus tooling becomes more useful when the app directs limited workshop time to incomplete, divergent or low-confidence items. | Source 4 and current repository | Isolated | This combination needs user testing; do not claim market uniqueness. |

## Candidate details

- **Disagreement-led workshop:** best fit and highest existing leverage; complete
  the live loop before adding another advanced feature.
- **Blind individual evaluation:** a plausible later experiment after live
  scoring, but not required to prove the core workflow.
- **Evidence-gap clarification queue:** potentially valuable and more aligned
  than AI scoring, but generated questions are currently out of scope and
  require a product decision.
- **Pairwise optimisation and automated award preparation:** observed but
  rejected for the next product increment.

## Recommended shortlist

1. Disagreement-led evaluation workshop.
2. Optional blind individual review.
3. Evidence-gap-to-clarification loop (requires a product decision).

## Follow-on gaps

Interview or observe an evaluation panel before building blind mode or an AI
clarification assistant. Their value is plausible, not established by vendor
shipping alone.
