"""Sample data for the side-by-side vendor comparison (proof of concept).

Two mock vendor proposals responding to the customer/case capability RFP:
- Acme CaseWorks: established case management platform, unexciting but solid.
- NovaAI FlowSuite: AI-led workflow/analytics product, strong demos, thin
  enterprise evidence.

Panel of three evaluators, scoring 0-5 per criterion per vendor. All data
is synthetic. Evidence references point at fictional proposal pages.
"""

VENDORS = ["Acme CaseWorks", "NovaAI FlowSuite"]

EVALUATORS = ["Business Rep", "Architect", "Tech PM"]

SCORE_SCALE = "0 (no evidence) to 5 (strong, evidenced)"

ARCHITECTURE_DOMAINS = [
    "Application architecture",
    "API and integration architecture",
    "Cloud architecture",
    "AI architecture",
    "Delivery architecture",
]

# Mandatory gates sit outside weighted scoring and can never be offset by
# good scores elsewhere. Pass / Clarify / Fail / Unknown.
GATES = [
    {
        "id": "GATE-01",
        "statement": "Customer data held in-region (data residency)",
        "status": {"Acme CaseWorks": "Pass", "NovaAI FlowSuite": "Clarify"},
    },
    {
        "id": "GATE-02",
        "statement": "Full data export available on exit (no lock-in)",
        "status": {"Acme CaseWorks": "Pass", "NovaAI FlowSuite": "Fail"},
    },
    {
        "id": "GATE-03",
        "statement": "Audit logging of all user and admin actions",
        "status": {"Acme CaseWorks": "Pass", "NovaAI FlowSuite": "Clarify"},
    },
]

CRITERIA = [
    {
        "id": "APP-01",
        "domain": "Application architecture",
        "statement": "Case lifecycle management covers intake, triage, resolution and review",
    },
    {
        "id": "APP-02",
        "domain": "Application architecture",
        "statement": "Configuration over customisation for business rule changes",
    },
    {
        "id": "APP-03",
        "domain": "Application architecture",
        "statement": "Clear system-of-record boundaries and data ownership",
    },
    {
        "id": "APP-04",
        "domain": "Application architecture",
        "statement": "Workflow designer usable by trained business staff",
    },
    {
        "id": "API-01",
        "domain": "API and integration architecture",
        "statement": "Documented REST APIs cover all core case and customer entities",
    },
    {
        "id": "API-02",
        "domain": "API and integration architecture",
        "statement": "Event publishing for case state changes (for data lake feed)",
    },
    {
        "id": "CLD-01",
        "domain": "Cloud architecture",
        "statement": "Disaster recovery: documented RPO/RTO with evidence of testing",
    },
]

# (criterion_id, vendor) -> extracted response record.
# A missing key means the vendor did not answer the criterion.
RESPONSES = {
    ("APP-01", "Acme CaseWorks"): {
        "summary": "Full lifecycle supported out of the box; screens shown for intake, triage, SLA-tracked resolution and QA review.",
        "evidence": "Proposal p.14, section 3.2; demo appendix B",
        "gaps": [],
        "confidence": "High",
    },
    ("APP-01", "NovaAI FlowSuite"): {
        "summary": "Lifecycle handled through configurable AI-suggested flows; triage and resolution demonstrated, review stage described but not shown.",
        "evidence": "Proposal p.9, section 2.4",
        "gaps": ["Review/QA stage not demonstrated"],
        "confidence": "Medium",
    },
    ("APP-02", "Acme CaseWorks"): {
        "summary": "Rules engine with versioned configuration; vendor states 90% of typical changes need no code.",
        "evidence": "Proposal p.18, section 4.1",
        "gaps": ["'90% no-code' claim not evidenced"],
        "confidence": "Medium",
    },
    ("APP-02", "NovaAI FlowSuite"): {
        "summary": "Changes made through natural-language configuration assistant; underlying rule model proprietary.",
        "evidence": "Proposal p.11, section 3.1",
        "gaps": ["No detail on validating or testing AI-applied changes"],
        "confidence": "Low",
    },
    ("APP-03", "Acme CaseWorks"): {
        "summary": "Case record ownership explicit; customer master remains in ERP with documented sync pattern.",
        "evidence": "Proposal p.21, integration diagram 5.2",
        "gaps": [],
        "confidence": "High",
    },
    ("APP-03", "NovaAI FlowSuite"): {
        "summary": "Proposal describes a unified data plane that ingests customer and case data; boundary with existing systems of record unclear.",
        "evidence": "Proposal p.15, section 4.2",
        "gaps": ["System-of-record boundary not defined", "Conflicts with GATE-02 export concern"],
        "confidence": "Low",
    },
    ("APP-04", "Acme CaseWorks"): {
        "summary": "Drag-and-drop workflow designer; vendor cites two reference customers where business staff maintain workflows.",
        "evidence": "Proposal p.19, section 4.3; references appendix D",
        "gaps": [],
        "confidence": "High",
    },
    ("APP-04", "NovaAI FlowSuite"): {
        "summary": "Workflows generated from prompts; impressive demo, but no reference customers using it in production yet.",
        "evidence": "Proposal p.12, section 3.3",
        "gaps": ["No production references"],
        "confidence": "Medium",
    },
    ("API-01", "Acme CaseWorks"): {
        "summary": "OpenAPI specs supplied for case, customer, task and document entities; rate limits documented.",
        "evidence": "Proposal p.24, appendix C (API catalogue)",
        "gaps": [],
        "confidence": "High",
    },
    ("API-01", "NovaAI FlowSuite"): {
        "summary": "REST API described as available for 'core objects'; specification promised post-award.",
        "evidence": "Proposal p.17, section 5.1",
        "gaps": ["API specification not supplied"],
        "confidence": "Low",
    },
    ("API-02", "Acme CaseWorks"): {
        "summary": "Webhook events for case state changes; no native streaming, batch export to data lake nightly.",
        "evidence": "Proposal p.25, section 6.2",
        "gaps": ["No event stream; nightly batch only"],
        "confidence": "High",
    },
    ("API-02", "NovaAI FlowSuite"): {
        "summary": "Kafka-compatible event stream for all state changes, including AI decision events.",
        "evidence": "Proposal p.18, section 5.3",
        "gaps": [],
        "confidence": "Medium",
    },
    ("CLD-01", "Acme CaseWorks"): {
        "summary": "RPO 15 min / RTO 4 h stated with summary of last DR test (dated).",
        "evidence": "Proposal p.28, section 7.4",
        "gaps": [],
        "confidence": "High",
    },
    # NovaAI FlowSuite did not answer CLD-01 — intentionally absent.
}

# (criterion_id, vendor) -> {evaluator: score 0-5}. Individual scores are
# first-class: they are never overwritten by consensus.
PANEL_SCORES = {
    ("APP-01", "Acme CaseWorks"): {"Business Rep": 4, "Architect": 4, "Tech PM": 4},
    ("APP-01", "NovaAI FlowSuite"): {"Business Rep": 4, "Architect": 2, "Tech PM": 3},
    ("APP-02", "Acme CaseWorks"): {"Business Rep": 3, "Architect": 3, "Tech PM": 4},
    ("APP-02", "NovaAI FlowSuite"): {"Business Rep": 4, "Architect": 1, "Tech PM": 2},
    ("APP-03", "Acme CaseWorks"): {"Business Rep": 4, "Architect": 5, "Tech PM": 4},
    ("APP-03", "NovaAI FlowSuite"): {"Business Rep": 3, "Architect": 1, "Tech PM": 1},
    ("APP-04", "Acme CaseWorks"): {"Business Rep": 4, "Architect": 4, "Tech PM": 3},
    ("APP-04", "NovaAI FlowSuite"): {"Business Rep": 5, "Architect": 2, "Tech PM": 3},
    ("API-01", "Acme CaseWorks"): {"Business Rep": 3, "Architect": 5, "Tech PM": 4},
    ("API-01", "NovaAI FlowSuite"): {"Business Rep": 3, "Architect": 1, "Tech PM": 2},
    ("API-02", "Acme CaseWorks"): {"Business Rep": 3, "Architect": 3, "Tech PM": 3},
    ("API-02", "NovaAI FlowSuite"): {"Business Rep": 4, "Architect": 3, "Tech PM": 4},
    ("CLD-01", "Acme CaseWorks"): {"Business Rep": 4, "Architect": 4, "Tech PM": 4},
    ("CLD-01", "NovaAI FlowSuite"): {"Business Rep": 0, "Architect": 0, "Tech PM": 0},
}
