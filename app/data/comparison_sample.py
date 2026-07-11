"""Sample data for the side-by-side vendor comparison (proof of concept).

Three mock vendor proposals responding to the customer/case capability RFP:
- Acme CaseWorks: established case management platform, unexciting but solid.
- NovaAI FlowSuite: AI-led workflow/analytics product, strong demos, thin
  enterprise evidence.
- Titan Public Sector Suite: large incumbent-style vendor, heavy on
  compliance/process rigour, light on modern integration and slow to adapt.

Panel of three evaluators, scoring 0-5 per criterion per vendor. All data
is synthetic. Evidence references point at fictional proposal pages.
"""

VENDORS = ["Acme CaseWorks", "NovaAI FlowSuite", "Titan Public Sector Suite"]

EVALUATORS = ["Business Rep", "Architect", "Tech PM"]

# Named sample panel for the Setup tab. Keyed by the same role strings as
# EVALUATORS/PANEL_SCORES — do not rename or reorder EVALUATORS to match this;
# consumers should look up EVALUATION_TEAM[role] for display, and continue to
# key scoring data off the role string itself.
EVALUATION_TEAM = {
    "Business Rep": {
        "name": "Priya Chandrasekaran",
        "title": "Business Representative, Case Services",
    },
    "Architect": {
        "name": "Marcus Odendaal",
        "title": "Lead Enterprise Architect",
    },
    "Tech PM": {
        "name": "Fiona Nakamura-Blake",
        "title": "Technical Project Manager",
    },
}

SCORE_SCALE = "0 (no evidence) to 5 (strong, evidenced)"

# Descriptive anchor text per score point, 0-5, for the Setup tab. Restates
# the same 0-5 range as SCORE_SCALE/PANEL_SCORES in fuller procurement
# language; not a separate scale.
SCORING_SCALE = {
    0: "Does not meet the requirement; no evidence offered",
    1: "Minimal alignment; significant gaps or unsupported claims",
    2: "Partial alignment; material gaps remain unresolved",
    3: "Meets the requirement; evidence adequate but not exceptional",
    4: "Strongly meets the requirement with clear, verified evidence",
    5: "Fully meets the requirement with strong, verified evidence and no material gaps",
}

# Selectable Compare-tab scoring modes (see docs/product_decisions.md,
# 2026-07-11). Panel + Consensus is shipped and the documented default;
# Traditional weighted is display/sample data only at this stage.
SCORING_MODES = ["Panel + Consensus", "Traditional weighted"]
DEFAULT_SCORING_MODE = "Panel + Consensus"

# Sample shortlist rule for the Setup tab. Display text describing a rule the
# panel applies by hand in the evaluation workshop — the tool does not run
# this rule or declare a shortlist automatically.
SHORTLIST_RULE = (
    "A vendor is shortlisted only if it has passed every mandatory gate and "
    "reached a minimum consensus score of 3 (\"Meets the requirement\") on "
    "every criterion, with no criterion left unanswered. Applying this rule "
    "is a decision the evaluation panel makes in the workshop, not an "
    "automatic output of the tool."
)

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
        "status": {
            "Acme CaseWorks": "Pass",
            "NovaAI FlowSuite": "Clarify",
            "Titan Public Sector Suite": "Pass",
        },
    },
    {
        "id": "GATE-02",
        "statement": "Full data export available on exit (no lock-in)",
        "status": {
            "Acme CaseWorks": "Pass",
            "NovaAI FlowSuite": "Fail",
            "Titan Public Sector Suite": "Pass",
        },
    },
    {
        "id": "GATE-03",
        "statement": "Audit logging of all user and admin actions",
        "status": {
            "Acme CaseWorks": "Pass",
            "NovaAI FlowSuite": "Clarify",
            "Titan Public Sector Suite": "Pass",
        },
    },
]

# "weight" is the criterion's percentage weight for the Traditional weighted
# scoring mode (docs/product_decisions.md, 2026-07-11). Weights are integers
# and sum to 100 across CRITERIA in this sample set. Panel + Consensus mode
# ignores this field entirely.
CRITERIA = [
    {
        "id": "APP-01",
        "domain": "Application architecture",
        "statement": "Case lifecycle management covers intake, triage, resolution and review",
        "weight": 20,
    },
    {
        "id": "APP-02",
        "domain": "Application architecture",
        "statement": "Configuration over customisation for business rule changes",
        "weight": 15,
    },
    {
        "id": "APP-03",
        "domain": "Application architecture",
        "statement": "Clear system-of-record boundaries and data ownership",
        "weight": 15,
    },
    {
        "id": "APP-04",
        "domain": "Application architecture",
        "statement": "Workflow designer usable by trained business staff",
        "weight": 10,
    },
    {
        "id": "API-01",
        "domain": "API and integration architecture",
        "statement": "Documented REST APIs cover all core case and customer entities",
        "weight": 15,
    },
    {
        "id": "API-02",
        "domain": "API and integration architecture",
        "statement": "Event publishing for case state changes (for data lake feed)",
        "weight": 10,
    },
    {
        "id": "CLD-01",
        "domain": "Cloud architecture",
        "statement": "Disaster recovery: documented RPO/RTO with evidence of testing",
        "weight": 15,
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
    ("APP-01", "Titan Public Sector Suite"): {
        "summary": "Full lifecycle supported; intake through review handled by well-established modules, evidenced by long incumbent deployment history.",
        "evidence": "Proposal p.31, section 6.1; reference site visit notes",
        "gaps": [],
        "confidence": "High",
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
    ("APP-02", "Titan Public Sector Suite"): {
        "summary": "Business rule changes require vendor professional services engagement; no self-service configuration surfaced in proposal.",
        "evidence": "Proposal p.40, section 8.2 (change request process)",
        "gaps": ["No configuration-over-customisation path; every change is a paid change request"],
        "confidence": "High",
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
    ("APP-03", "Titan Public Sector Suite"): {
        "summary": "Long-documented system-of-record boundaries as part of standard implementation methodology; customer master stays in ERP.",
        "evidence": "Proposal p.34, integration diagram 6.4",
        "gaps": [],
        "confidence": "High",
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
    ("APP-04", "Titan Public Sector Suite"): {
        "summary": "Workflow designer exists but proposal states business staff typically shadow a vendor consultant for the first two changes.",
        "evidence": "Proposal p.41, section 8.3",
        "gaps": ["Usable by trained business staff without vendor involvement not evidenced"],
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
    ("API-01", "Titan Public Sector Suite"): {
        "summary": "Hybrid SOAP/REST API layer; REST coverage limited to case entity, remaining entities SOAP-only pending a roadmap upgrade.",
        "evidence": "Proposal p.45, section 9.1",
        "gaps": ["Customer and document entities are SOAP-only today"],
        "confidence": "Medium",
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
    ("CLD-01", "Titan Public Sector Suite"): {
        "summary": "RPO 5 min / RTO 1 h with quarterly DR test cadence, evidenced by two years of test reports.",
        "evidence": "Proposal p.52, section 10.2; appendix F (DR test history)",
        "gaps": [],
        "confidence": "High",
    },
    # Titan Public Sector Suite did not answer API-02 (no event architecture,
    # nightly batch only) — intentionally absent.
}

# (criterion_id, vendor) -> {evaluator: score 0-5}. Individual scores are
# first-class: they are never overwritten by consensus.
PANEL_SCORES = {
    ("APP-01", "Acme CaseWorks"): {"Business Rep": 4, "Architect": 4, "Tech PM": 4},
    ("APP-01", "NovaAI FlowSuite"): {"Business Rep": 4, "Architect": 2, "Tech PM": 3},
    ("APP-01", "Titan Public Sector Suite"): {"Business Rep": 4, "Architect": 3, "Tech PM": 3},
    ("APP-02", "Acme CaseWorks"): {"Business Rep": 3, "Architect": 3, "Tech PM": 4},
    ("APP-02", "NovaAI FlowSuite"): {"Business Rep": 4, "Architect": 1, "Tech PM": 2},
    ("APP-02", "Titan Public Sector Suite"): {"Business Rep": 2, "Architect": 2, "Tech PM": 1},
    ("APP-03", "Acme CaseWorks"): {"Business Rep": 4, "Architect": 5, "Tech PM": 4},
    ("APP-03", "NovaAI FlowSuite"): {"Business Rep": 3, "Architect": 1, "Tech PM": 1},
    ("APP-03", "Titan Public Sector Suite"): {"Business Rep": 4, "Architect": 4, "Tech PM": 4},
    ("APP-04", "Acme CaseWorks"): {"Business Rep": 4, "Architect": 4, "Tech PM": 3},
    ("APP-04", "NovaAI FlowSuite"): {"Business Rep": 5, "Architect": 2, "Tech PM": 3},
    ("APP-04", "Titan Public Sector Suite"): {"Business Rep": 2, "Architect": 3, "Tech PM": 1},
    ("API-01", "Acme CaseWorks"): {"Business Rep": 3, "Architect": 5, "Tech PM": 4},
    ("API-01", "NovaAI FlowSuite"): {"Business Rep": 3, "Architect": 1, "Tech PM": 2},
    ("API-01", "Titan Public Sector Suite"): {"Business Rep": 3, "Architect": 2, "Tech PM": 3},
    ("API-02", "Acme CaseWorks"): {"Business Rep": 3, "Architect": 3, "Tech PM": 3},
    ("API-02", "NovaAI FlowSuite"): {"Business Rep": 4, "Architect": 3, "Tech PM": 4},
    ("API-02", "Titan Public Sector Suite"): {"Business Rep": 0, "Architect": 0, "Tech PM": 0},
    ("CLD-01", "Acme CaseWorks"): {"Business Rep": 4, "Architect": 4, "Tech PM": 4},
    ("CLD-01", "NovaAI FlowSuite"): {"Business Rep": 0, "Architect": 0, "Tech PM": 0},
    ("CLD-01", "Titan Public Sector Suite"): {"Business Rep": 5, "Architect": 5, "Tech PM": 4},
}
