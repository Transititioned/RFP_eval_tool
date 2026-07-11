"""Proposals tab: the confirm-proposal-set lock.

Once the evaluation office is satisfied every vendor proposal it intends to
evaluate has been loaded and reviewed, it confirms the proposal set for
evaluation. This mirrors ``app/logic/setup.py``'s approval-lock pattern
(confirm/reopen, timestamped append-only event log) rather than inventing a
new convention: confirming isn't decorative, and reopening requires an
explicit, reasoned, visibly-logged action.

Per-vendor readiness (status/note) is display data supplied by the caller
(shaped like ``app.data.comparison_sample.PROPOSAL_READINESS``) — this
module does not own or validate it, it only renders it for the UI table.

Pure functions only: plain Python dicts/lists in, plain Python dicts/lists
out. No Gradio imports. No persistence — proposal-set state lives in the UI
session only (held in a gr.State on the caller's side); this module never
writes anywhere.
"""

import datetime


def new_proposal_state():
    """Initial proposal-set state: not confirmed, empty event log."""
    return {"confirmed": False, "events": []}


def _timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def confirm_proposal_set(state, note=""):
    """Mark the proposal set confirmed and log a 'confirmed' event.

    Returns (new_state, message). Never mutates the input state in place.
    Refuses (without logging) if the proposal set is already confirmed.
    """
    state = state or new_proposal_state()
    if state.get("confirmed"):
        return state, "Proposal set is already confirmed."

    event = {
        "type": "confirmed",
        "timestamp": _timestamp(),
        "note": (note or "").strip(),
    }
    new_state = {
        "confirmed": True,
        "events": list(state.get("events", [])) + [event],
    }
    return new_state, "Proposal set confirmed. Proceed to Eligibility and Evaluation."


def reopen_proposal_set(state, reason):
    """Reopen a confirmed proposal set for editing. Requires a non-empty reason.

    Returns (new_state, message). Never mutates the input state in place.
    Refuses if the reason is empty/whitespace, or if the proposal set is not
    currently confirmed (never-confirmed or already-open) — nothing to
    reopen.
    """
    state = state or new_proposal_state()
    if not reason or not reason.strip():
        return state, "Proposal set not reopened: a reason is required."
    if not state.get("confirmed"):
        return state, "Proposal set is not currently confirmed — nothing to reopen."

    event = {
        "type": "reopened",
        "timestamp": _timestamp(),
        "reason": reason.strip(),
    }
    new_state = {
        "confirmed": False,
        "events": list(state.get("events", [])) + [event],
    }
    return new_state, "Proposal set reopened. The proposal list is editable again."


def is_confirmed(state):
    """True when the proposal set is currently confirmed (None/{} safe)."""
    if not state:
        return False
    return bool(state.get("confirmed"))


def format_proposal_log(state):
    """Markdown rendering of the confirmation event history, newest first."""
    events = (state or {}).get("events", [])
    if not events:
        return "_Proposal set not yet confirmed._"

    lines = ["### Proposal confirmation log", ""]
    for event in reversed(events):
        if event["type"] == "confirmed":
            note = event.get("note")
            suffix = f" — {note}" if note else ""
            lines.append(f"- Proposal set confirmed {event['timestamp']}{suffix}")
        elif event["type"] == "reopened":
            lines.append(f"- Reopened {event['timestamp']} — reason: {event['reason']}")
        else:
            lines.append(f"- {event['timestamp']} — {event['type']}")
    return "\n".join(lines)


def proposal_rows(vendors, readiness):
    """Display rows for the Proposals table: [vendor, status, note].

    ``readiness`` is a {vendor: {"status": str, "note": str}} mapping
    (shaped like PROPOSAL_READINESS). A vendor missing from ``readiness``
    is not omitted or silently defaulted — it renders with an explicit
    "No status recorded" status so the gap is visible in the table.
    """
    readiness = readiness or {}
    rows = []
    for vendor in vendors:
        entry = readiness.get(vendor)
        if entry is None:
            rows.append([vendor, "No status recorded", ""])
        else:
            status = entry.get("status") or "No status recorded"
            note = entry.get("note") or ""
            rows.append([vendor, status, note])
    return rows
