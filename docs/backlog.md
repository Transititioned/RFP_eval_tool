# Backlog — deferred items

Items deliberately deferred from the Capability Sourcing Workbench build.
This is a proof-of-concept mock-up; these become real requirements when the
product moves beyond demonstration use.

## Privacy and confidentiality (address before any real vendor documents)

Deferred by product decision 2026-07-10. The app currently runs on a public
Hugging Face Space and must only ever see synthetic/sample data until this
is addressed.

- Private hosting (private HF Space or self-hosted) before proposal
  ingestion handles real vendor documents.
- Confidentiality warnings on any upload surface.
- Upload size limits and file-type validation.
- Temporary-file cleanup after ingestion.
- Secret handling review (tokens, dataset repos).
- Data retention/deletion story for real proposal documents, if/when
  document handling is built (the current Proposals tab is a sample-data
  readiness register only — no upload or ingestion exists today).

## AI assist

Direction decided 2026-07-11 (see product_decisions.md, "Future
direction: AI evidence read-in and AI cross-check assessment").
Two-stage gating: **synthetic (fake) documents only, once the HF Space
is private**; real vendor documents additionally require everything in
the privacy section above plus the enterprise controls below.

- Upload/read-in flow for synthetic RFP documents (flow testing).
- AI evidence read-in with citations into the existing
  evidence/confidence/gaps model; human-verified before it counts.
- AI-drafted clarification questions from identified gaps; human-reviewed
  before sending.
- AI cross-check assessment through role lenses, as a divergence signal
  in the focus queue only — never entering consensus, totals, rankings,
  shortlist, or recommendation.

## Enterprise controls (before any real vendor document or real user)

No enterprise would onboard without these; the product must expect to
pass the same kind of assessment it runs on vendors.

- SSO (SAML/OIDC) and MFA.
- Audit logging of evaluation actions.
- Role-based access aligned to the evaluation panel roles.
- Hosting under an enterprise agreement (not a personal HF account).

## Multi-tenancy / consultancy model (much later)

Deferred by product decision 2026-07-10. Build single-tenant: one
organisation's sourcing team, workspaces are sequential sourcing
activities, not client tenants.

- Workspace isolation per client engagement.
- Identity and access separation between engagements.
- Per-client branding/exports.

## Other deferred items (from the build plan, section "Defer")

- Full procurement portal; vendor submission portal.
- Contract management.
- Enterprise architecture repository; EA-tool export formats.
- Live integrations with procurement suites (Jira/ADO/Confluence exports
  included).
- Complex collaboration and permissions.
- Autonomous final scoring or supplier selection.
- Requirements marketplace; vendor-side bid/no-bid.
- PDF and PowerPoint export (Markdown/HTML/CSV/DOCX come first).
