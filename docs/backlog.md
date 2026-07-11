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
