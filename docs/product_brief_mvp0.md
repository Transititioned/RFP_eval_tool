# Product brief — MVP-0

## Product

RFP Evaluation Tool / Capability Sourcing Workbench.

## Core principle

Evaluate the capability first. Check enterprise viability before sparkle.

## Problem

Technology sourcing decisions are often driven by product sparkle rather than a
disciplined look at (a) whether the option actually does the business capability
work, and (b) whether it meets baseline enterprise viability requirements —
system-of-record clarity, data ownership, security, audit, support and commercial
clarity.

## MVP-0 scope

Exactly three things:

1. **Capability Coverage Matrix** — capabilities × candidate options, cells rated
   Strong / Partial / Weak / Unknown.
2. **Baseline Viability Gate** — viability checks × candidate options, cells rated
   Pass / Clarify / Fail / Unknown.
3. **Simple readout** — plain-English interpretation of the visible values. No
   scores, no weighting, no roll-ups, no false precision.

## Scenario used in the prototype

The organisation needs improved customer/case capability. The ERP has a CRM-like
module, the billing platform owns account data, the case management platform has
workflow capability, and a shiny AI workflow/analytics product looks attractive but
may not pass enterprise basics. The team must decide whether to reuse, extend, buy,
or compose.

Candidate options: ERP CRM module, case management platform, billing platform
extension, shiny AI workflow/analytics product, hybrid/composite option.

## Design intent

Serious enterprise B2B SaaS. Clean and restrained. Architecture-review-board
credible, procurement-safe. A practical decision aid, not a magic AI toy.

## Explicitly out of scope for MVP-0

Role lenses, Market Clarity, bid waste reduction, vendor self-assessment,
challenger path, document upload, AI scoring, RFP PDF parsing, procurement
workflow, report builder, broad exports, architecture repository features,
generated clarification questions, roll-up scores, weighting, evidence fields,
authentication, database persistence.
