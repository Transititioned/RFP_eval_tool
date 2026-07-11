"""Eligibility tab: per-vendor eligibility outcomes and gate compliance rows.

Outcomes are categorical, human-entered gate-type decisions — Eligible /
Conditionally eligible / Clarification required / Excluded — never a score,
rank, or blend. This mirrors ``record_consensus()`` in
app/logic/comparison.py: a rationale is required for the consequential
action (there, recording consensus; here, excluding a vendor), and history
is never lost — re-recording a vendor's outcome replaces its *current*
outcome but the event log keeps every prior decision.

Pure functions only: plain Python dicts/lists in, plain Python dicts/lists
out. No Gradio imports. No persistence — eligibility state lives in the UI
session only (held in a gr.State on the caller's side); this module never
writes anywhere.
"""

import datetime

# Mirrors app.data.comparison_sample.ELIGIBILITY_OUTCOMES. Kept as a local
# module constant (rather than importing app.data) so this logic module has
# no dependency on the parallel sample-data work landing first, and stays
# independently testable with synthetic fixtures. record_eligibility()
# accepts an ``outcomes`` override for callers that want to validate against
# a different/extended vocabulary without editing this module.
ELIGIBILITY_OUTCOMES = [
    "Eligible",
    "Conditionally eligible",
    "Clarification required",
    "Excluded",
]


def compliance_rows(gates, vendors, compliance):
    """Requirement x vendor display rows: [gate label, value, value, ...].

    ``gates`` is a list of gate dicts with "id"/"statement" (shaped like
    GATES). ``compliance`` is a {gate_id: {vendor: value}} mapping (shaped
    like ELIGIBILITY_COMPLIANCE). A missing cell is never hidden or
    silently defaulted — it renders "NOT RECORDED", the same visibility
    principle as comparison.py's "NOT ANSWERED".
    """
    compliance = compliance or {}
    rows = []
    for gate in gates:
        row = [f"{gate['id']} — {gate['statement']}"]
        gate_compliance = compliance.get(gate["id"], {})
        for vendor in vendors:
            value = gate_compliance.get(vendor)
            row.append(value if value else "NOT RECORDED")
        rows.append(row)
    return rows


def new_eligibility_state():
    """Initial eligibility state: no outcomes, empty event log."""
    return {"outcomes": {}, "events": []}


def _timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def record_eligibility(state, vendor, outcome, reason="", outcomes=ELIGIBILITY_OUTCOMES):
    """Validate and record a vendor's current eligibility outcome.

    Returns (new_state, message). Never mutates the input state in place.

    Refuses (state unchanged, nothing logged):
    - an empty/whitespace vendor;
    - an outcome not in ``outcomes`` (defaults to ELIGIBILITY_OUTCOMES);
    - outcome "Excluded" with an empty/whitespace reason — mirrors
      record_consensus()'s refusal in comparison.py exactly in spirit: no
      reason, no exclusion.

    A reason is optional (but recorded when given) for every other outcome.

    Each vendor has exactly one *current* outcome — recording again for the
    same vendor replaces it in ``state["outcomes"]`` — but the full history
    is preserved, append-only, in ``state["events"]``.
    """
    state = state or new_eligibility_state()

    if not vendor or not vendor.strip():
        return state, "Eligibility not recorded: a vendor is required."
    if outcome not in outcomes:
        return state, f"Eligibility not recorded: unknown outcome '{outcome}'."
    if outcome == "Excluded" and (not reason or not reason.strip()):
        return state, "Eligibility not recorded: excluding a vendor requires a reason."

    vendor = vendor.strip()
    reason = (reason or "").strip()
    event = {
        "vendor": vendor,
        "outcome": outcome,
        "reason": reason,
        "timestamp": _timestamp(),
    }

    new_outcomes = dict(state.get("outcomes", {}))
    new_outcomes[vendor] = event
    new_state = {
        "outcomes": new_outcomes,
        "events": list(state.get("events", [])) + [event],
    }

    if outcome == "Excluded":
        message = f"{vendor} excluded — reason: {reason}"
    else:
        message = f"{outcome} recorded for {vendor}."
    return new_state, message


def current_outcomes(state, vendors):
    """Display rows for every vendor: [vendor, outcome, reason].

    Every vendor in ``vendors`` is always present, even with no recorded
    outcome ("Not yet assessed") — a vendor is never omitted, and an
    Excluded vendor is never dropped from this list either.
    """
    outcomes = (state or {}).get("outcomes", {})
    rows = []
    for vendor in vendors:
        entry = outcomes.get(vendor)
        if entry is None:
            rows.append([vendor, "Not yet assessed", ""])
        else:
            rows.append([vendor, entry["outcome"], entry.get("reason", "")])
    return rows


def format_eligibility_log(state):
    """Markdown rendering of the eligibility event history, newest first."""
    events = (state or {}).get("events", [])
    if not events:
        return "_No eligibility outcomes recorded yet._"

    lines = ["### Eligibility log", ""]
    for event in reversed(events):
        if event["outcome"] == "Excluded":
            lines.append(
                f"- Excluded — {event['vendor']} — reason: {event['reason']} "
                f"({event['timestamp']})"
            )
        elif event.get("reason"):
            lines.append(
                f"- {event['outcome']} — {event['vendor']} — reason: {event['reason']} "
                f"({event['timestamp']})"
            )
        else:
            lines.append(f"- {event['outcome']} — {event['vendor']} ({event['timestamp']})")
    return "\n".join(lines)
