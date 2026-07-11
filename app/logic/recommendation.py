"""Recommendation tab: the final human decision, kept distinct from scoring.

Four fields are always kept explicitly separate and never collapsed into
one another:

1. Highest-scoring supplier — COMPUTED, from whichever mode's ranking is
   active (``weighted_totals()`` or ``consensus_ranking()`` in
   ``app/logic/comparison.py``). The UI passes it in for display only;
   this module never stores it, never accepts it as an input, and never
   treats it as a recommendation. That is the exact auto-winner failure
   mode this product exists to prevent.
2. Preferred supplier — human-entered, may differ from both the
   highest-scoring supplier and the final recommendation (e.g. "my
   personal read, pending panel discussion").
3. Recommended supplier — human-entered, the panel's actual decision.
   Refused without a written reason: a recommendation with no rationale is
   indistinguishable from the tool silently declaring a winner.
4. Approval — a separate human sign-off action (who + when), refused
   without a recorded recommendation to approve.

Mirrors the approve/reopen and reason-gating conventions used throughout
this app (``app/logic/setup.py``, ``app/logic/shortlist.py``,
``record_consensus()`` in ``app/logic/comparison.py``): a changed
recommendation after approval clears the approval, and that is logged
explicitly, never silently.

Pure functions only: plain Python dicts/lists in, plain Python dicts/lists
out. No Gradio imports. No persistence — recommendation state lives in the
UI session only (held in a gr.State on the caller's side); this module
never writes anywhere.
"""

import datetime


def new_recommendation_state():
    """Initial recommendation state: no record, no approval, empty event log."""
    return {"record": None, "approved": False, "approval": None, "events": []}


def _timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def record_recommendation(state, preferred, recommended, reasons, risks="", conditions="", dissent=""):
    """Record the panel's preferred/recommended supplier. Returns (new_state, message).

    ``preferred`` and ``recommended`` are human-entered vendor names — they
    may differ from each other and from whatever the highest-scoring
    supplier is; this function never looks at or receives scores.

    Refuses (state unchanged, nothing logged):
    - ``recommended`` is non-empty but ``reasons`` is empty/whitespace — a
      recommendation without a written reason is exactly the auto-winner
      failure mode this product exists to prevent.

    Re-recording replaces the current record (full history stays in
    ``state["events"]``). If the recommendation was previously approved,
    the approval is cleared and an explicit "approval_cleared" event is
    logged — a changed recommendation is never silently treated as still
    approved.
    """
    state = state or new_recommendation_state()

    preferred = (preferred or "").strip()
    recommended = (recommended or "").strip()
    reasons = (reasons or "").strip()
    risks = (risks or "").strip()
    conditions = (conditions or "").strip()
    dissent = (dissent or "").strip()

    if recommended and not reasons:
        return state, (
            "Recommendation not recorded: a written reason is required when "
            "a supplier is recommended."
        )

    timestamp = _timestamp()
    record = {
        "preferred": preferred,
        "recommended": recommended,
        "reasons": reasons,
        "risks": risks,
        "conditions": conditions,
        "dissent": dissent,
        "timestamp": timestamp,
    }

    events = list(state.get("events", []))
    events.append({"type": "recorded", **record})

    was_approved = bool(state.get("approved"))
    if was_approved:
        events.append({
            "type": "approval_cleared",
            "timestamp": timestamp,
            "reason": "Recommendation re-recorded after approval.",
        })

    new_state = {
        "record": record,
        "approved": False,
        "approval": None,
        "events": events,
    }

    message = "Recommendation recorded."
    if was_approved:
        message += " Previous approval cleared."
    return new_state, message


def approve_recommendation(state, approver_name):
    """Approve the current recorded recommendation. Returns (new_state, message).

    Refuses (state unchanged, nothing logged):
    - an empty/whitespace approver name;
    - no recorded recommendation to approve;
    - double-approval (already approved).
    """
    state = state or new_recommendation_state()

    if not approver_name or not approver_name.strip():
        return state, "Recommendation not approved: an approver name is required."
    if state.get("record") is None:
        return state, "Recommendation not approved: record a recommendation first."
    if state.get("approved"):
        return state, "Recommendation is already approved."

    approver_name = approver_name.strip()
    timestamp = _timestamp()
    approval = {"approver": approver_name, "timestamp": timestamp}

    events = list(state.get("events", [])) + [{
        "type": "approved",
        "timestamp": timestamp,
        "approver": approver_name,
    }]

    new_state = {
        "record": state["record"],
        "approved": True,
        "approval": approval,
        "events": events,
    }
    return new_state, f"Recommendation approved by {approver_name}."


def current_recommendation(state):
    """Display shape for the current record, or an empty/unapproved shape.

    Deliberately has no "highest_scoring" field — the UI must source that
    separately from the active scoring mode's ranking and display it
    alongside, never merged into this shape.

    Returns:
        {
            "preferred": str,
            "recommended": str,
            "reasons": str,
            "risks": str,
            "conditions": str,
            "dissent": str,
            "approved": bool,
            "approver": str or None,
            "approved_at": str or None,
        }
    """
    state = state or new_recommendation_state()
    record = state.get("record")
    if record is None:
        return {
            "preferred": "",
            "recommended": "",
            "reasons": "",
            "risks": "",
            "conditions": "",
            "dissent": "",
            "approved": False,
            "approver": None,
            "approved_at": None,
        }

    approval = state.get("approval") or {}
    return {
        "preferred": record["preferred"],
        "recommended": record["recommended"],
        "reasons": record["reasons"],
        "risks": record["risks"],
        "conditions": record["conditions"],
        "dissent": record["dissent"],
        "approved": bool(state.get("approved")),
        "approver": approval.get("approver"),
        "approved_at": approval.get("timestamp"),
    }


def format_recommendation_log(state):
    """Markdown rendering of the recommendation event history, newest first."""
    events = (state or {}).get("events", [])
    if not events:
        return "_No recommendation recorded yet._"

    lines = ["### Recommendation log", ""]
    for event in reversed(events):
        if event["type"] == "recorded":
            lines.append(
                f"- Recorded {event['timestamp']} — preferred: {event['preferred'] or '—'}, "
                f"recommended: {event['recommended'] or '—'} — reasons: {event['reasons'] or '—'}"
            )
        elif event["type"] == "approved":
            lines.append(f"- Approved {event['timestamp']} by {event['approver']}")
        elif event["type"] == "approval_cleared":
            lines.append(f"- Approval cleared {event['timestamp']} — {event['reason']}")
        else:
            lines.append(f"- {event['timestamp']} — {event['type']}")
    return "\n".join(lines)
