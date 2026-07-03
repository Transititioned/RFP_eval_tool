"""Sample data for the MVP-0 prototype scenario.

The scenario: the organisation needs improved customer/case capability and
must decide whether to reuse, extend, buy, or compose.
"""

OPTIONS = [
    "Existing ERP CRM module",
    "Existing case management platform",
    "Billing platform extension",
    "Shiny AI workflow/analytics product",
    "Hybrid/composite option",
]

CAPABILITY_ROWS = [
    "Customer master",
    "Case lifecycle",
    "Billing interaction",
    "Workflow",
    "Compliance reporting",
    "Data lake integration",
]

VIABILITY_ROWS = [
    "System-of-record clarity",
    "Data ownership / export",
    "Security / access control",
    "Audit logging",
    "Data lake / reporting integration",
    "Operational support",
    "Commercial clarity",
]

CAPABILITY_VALUES = ["Strong", "Partial", "Weak", "Unknown"]
VIABILITY_VALUES = ["Pass", "Clarify", "Fail", "Unknown"]

CAPABILITY_HEADERS = ["Capability"] + OPTIONS
VIABILITY_HEADERS = ["Viability check"] + OPTIONS


def blank_capability_matrix():
    return [[row] + ["Unknown"] * len(OPTIONS) for row in CAPABILITY_ROWS]


def blank_viability_gate():
    return [[row] + ["Unknown"] * len(OPTIONS) for row in VIABILITY_ROWS]


# Columns: ERP CRM, case mgmt, billing ext, shiny AI, hybrid
COMPLETED_CAPABILITY_MATRIX = [
    ["Customer master",       "Strong",  "Weak",    "Partial", "Weak",    "Strong"],
    ["Case lifecycle",        "Partial", "Strong",  "Weak",    "Partial", "Strong"],
    ["Billing interaction",   "Partial", "Weak",    "Strong",  "Weak",    "Partial"],
    ["Workflow",              "Weak",    "Strong",  "Weak",    "Strong",  "Strong"],
    ["Compliance reporting",  "Partial", "Partial", "Partial", "Partial", "Partial"],
    ["Data lake integration", "Partial", "Partial", "Strong",  "Unknown", "Partial"],
]

COMPLETED_VIABILITY_GATE = [
    ["System-of-record clarity",           "Pass",    "Pass",    "Clarify", "Fail",    "Clarify"],
    ["Data ownership / export",            "Pass",    "Pass",    "Pass",    "Fail",    "Pass"],
    ["Security / access control",          "Pass",    "Pass",    "Pass",    "Clarify", "Pass"],
    ["Audit logging",                      "Pass",    "Clarify", "Pass",    "Fail",    "Clarify"],
    ["Data lake / reporting integration",  "Pass",    "Clarify", "Pass",    "Unknown", "Clarify"],
    ["Operational support",                "Pass",    "Pass",    "Pass",    "Clarify", "Clarify"],
    ["Commercial clarity",                 "Pass",    "Pass",    "Clarify", "Clarify", "Clarify"],
]

SCENARIO_SUMMARY = """\
The organisation needs improved customer/case capability.

**Current landscape**

- The ERP has a CRM-like module.
- The billing platform owns account data.
- The existing case management platform has workflow capability.
- A new shiny AI workflow/analytics product looks attractive but may not pass enterprise basics.
- The team must decide whether to **reuse, extend, buy, or compose**.

**Candidate options**

1. Existing ERP CRM module
2. Existing case management platform
3. Billing platform extension
4. Shiny AI workflow/analytics product
5. Hybrid/composite option

**How to use this tool**

First assess **functional capability fit** in the Capability Coverage Matrix,
then assess **baseline enterprise viability** in the Baseline Viability Gate.
Evaluate the capability first. Check enterprise viability before sparkle.
"""
