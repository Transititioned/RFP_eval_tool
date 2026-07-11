"""Evaluation framework setup: the approval lock for criteria/weights.

Once a panel approves the evaluation framework (criteria, weights,
mandatory requirements), it must not be quietly editable — reopening it
requires an explicit, reasoned, visibly-logged action. This mirrors
``record_consensus()`` in app/logic/comparison.py: rationale-gated,
append-only, never silently mutating history.

Pure functions only: plain Python dicts/lists in, plain Python dicts/lists
out. No Gradio imports. No persistence — approval state lives in the UI
session only (held in a gr.State on the caller's side); this module never
writes anywhere.
"""

import datetime

WEIGHT_TOLERANCE = 0.01


def new_approval_state():
    """Initial approval state: not approved, empty event log."""
    return {"approved": False, "events": []}


def _timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def approve_framework(state, note=""):
    """Mark the framework approved and log an 'approved' event.

    Returns (new_state, message). Never mutates the input state in place.
    Refuses (without logging) if the framework is already approved.
    """
    state = state or new_approval_state()
    if state.get("approved"):
        return state, "Framework is already approved."

    event = {
        "type": "approved",
        "timestamp": _timestamp(),
        "note": (note or "").strip(),
    }
    new_state = {
        "approved": True,
        "events": list(state.get("events", [])) + [event],
    }
    return new_state, "Framework approved. Criteria, weights and mandatory requirements are now locked."


def reopen_framework(state, reason):
    """Reopen an approved framework for editing. Requires a non-empty reason.

    Returns (new_state, message). Never mutates the input state in place.
    Refuses if the reason is empty/whitespace, or if the framework is not
    currently approved (never-approved or already-open) — nothing to
    reopen.
    """
    state = state or new_approval_state()
    if not reason or not reason.strip():
        return state, "Framework not reopened: a reason is required."
    if not state.get("approved"):
        return state, "Framework is not currently approved — nothing to reopen."

    event = {
        "type": "reopened",
        "timestamp": _timestamp(),
        "reason": reason.strip(),
    }
    new_state = {
        "approved": False,
        "events": list(state.get("events", [])) + [event],
    }
    return new_state, "Framework reopened. Criteria, weights and mandatory requirements are editable again."


def is_locked(state):
    """True when the framework is currently approved (editors render read-only)."""
    if not state:
        return False
    return bool(state.get("approved"))


def format_approval_log(state):
    """Markdown rendering of the approval event history, newest first."""
    events = (state or {}).get("events", [])
    if not events:
        return "_Not yet approved._"

    lines = ["### Approval log", ""]
    for event in reversed(events):
        if event["type"] == "approved":
            note = event.get("note")
            suffix = f" — {note}" if note else ""
            lines.append(f"- Framework approved {event['timestamp']}{suffix}")
        elif event["type"] == "reopened":
            lines.append(f"- Reopened {event['timestamp']} — reason: {event['reason']}")
        else:
            lines.append(f"- {event['timestamp']} — {event['type']}")
    return "\n".join(lines)


def check_weights(criteria):
    """Validate that criterion weights sum to 100. A warning only, never a block.

    ``criteria`` is a list of criterion dicts that may carry a numeric
    "weight" field. Returns None if weights are present for every
    criterion and sum to 100 (within a small tolerance); otherwise a
    plain-English warning string. Never computes or implies a vendor
    score — this only validates the setup.
    """
    if not criteria:
        return None

    missing = [c.get("id", c.get("statement", "unknown criterion")) for c in criteria if c.get("weight") is None]
    if missing:
        return "Weights missing for: " + ", ".join(str(m) for m in missing) + "."

    total = sum(c["weight"] for c in criteria)
    if abs(total - 100) <= WEIGHT_TOLERANCE:
        return None
    return f"Criteria weights sum to {total:g}, not 100."
