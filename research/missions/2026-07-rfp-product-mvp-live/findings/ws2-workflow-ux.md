# WS2: Workflow and UX patterns

## Scope used

- Products inspected: Vendorful, Euna Procurement, DeepStream, OpenGov, Bonfire.
- Sources used: five official pages or customer material.
- Saturation or coverage note: question-first comparison and evaluator progress
  were the clearest repeatable patterns. Public pages provide less detail about
  keyboard interaction, dense-table behaviour and mobile use.

Sources:

1. Vendorful RFP process guide — https://vendorful.com/rfp-process/
2. Euna Procurement Sourcing — https://eunasolutions.com/solutions/procurement/sourcing/
3. DeepStream and the CIPS procurement cycle — https://www.deep.stream/blog/how-deepstream-fits-within-the-cips-procurement-cycle
4. OpenGov Procurement FAQ — https://opengov.com/faq/procurement/
5. Bonfire at Western University — https://eunasolutions.com/wp-content/uploads/2023/05/CaseStudy-WesternUniversity-Euna-Solutions.pdf

## Observations

| Product | Capability or pattern | Layer | Observation | Source | Signal | Limitation |
|---|---|---|---|---|---|---|
| Euna, DeepStream | Stage-oriented sourcing journey | UX | The workflow is described as recognisable stages, with Euna reducing it to Build, Solicit and Award and DeepStream mapping work to a procurement cycle. | Sources 2, 3 | Emerging | Marketing stages are too coarse to dictate this app's exact navigation. |
| Vendorful, DeepStream, OpenGov | Question-first side-by-side review | UX | Users compare the same question, response or score across suppliers in one context. | Sources 1, 3, 4 | Common | Must preserve a whole-vendor route for coherence checks. |
| Euna, Bonfire, OpenGov | Visible evaluator participation and progress | UX | Stakeholders work in the evaluation workspace and procurement leads can monitor scoring progress. | Sources 2, 4, 5 | Common | The scan does not establish the best visual treatment. |
| OpenGov, Bonfire | Separate individual and consensus moments | UX | Individual scoring is kept distinct from shared or consensus evaluation. | Sources 4, 5 | Emerging | Consensus facilitation detail is partly hidden behind demos. |
| Vendorful, DeepStream | Evidence kept beside the scoring task | UX | Responses, attachments or question context remain available while assessing and comparing. | Sources 1, 3 | Emerging | In-browser document handling is outside the current public-app scope. |

## Candidate details

- **Stage journey:** use honest current-state and next-action cues rather than
  adding a wizard or more top-level tabs.
- **Question-first comparison:** already substantially present; make it the
  natural route from scoring into discussion.
- **Evaluator progress:** high-value once scores are user-entered; sample scores
  must never fabricate progress.
- **Individual/consensus separation:** aligns directly with the product's
  human-decision principle.
- **Evidence beside the task:** already strong for synthetic extracted evidence;
  no document viewer is needed for this increment.

## Recommended shortlist

1. Honest stage status and next action.
2. Question-first side-by-side review.
3. Selected-evaluator workspace with visible progress.
4. Explicit individual-to-consensus transition.
5. Evidence and gaps beside the scoring/discussion context.

## Follow-on gaps

Test the chosen Gradio score-entry control with realistic criterion and vendor
counts. A later navigation mission can compare whether the twelve top-level
tabs should be consolidated after the live evaluation path exists.
