"""Shortlist tab: the propose/approve decision state machine.

A shortlist is a human decision, not an automatic output of the mechanical
ranking (Traditional weighted totals or Panel + Consensus totals). This
module never computes a ranking itself and never defaults the proposal to
the mechanical top-N — the caller (UI) passes the mechanical ranking in
purely as context so ``propose_shortlist()`` can tell whether the human
proposal matches it.

Mirrors the approve/reopen pattern in ``app/logic/setup.py`` and
``app/logic/proposals.py`` (reasoned, timestamped, append-only events) and
the reason-gating pattern in ``record_consensus()``
(app/logic/comparison.py) / ``record_eligibility()``
(app/logic/eligibility.py): a consequential action without a stated reason
is refused, not silently allowed.

Pure functions only: plain Python dicts/lists in, plain Python dicts/lists
out. No Gradio imports. No persistence — shortlist state lives in the UI
session only (held in a gr.State on the caller's side); this module never
writes anywhere.
"""

import datetime


def new_shortlist_state():
    """Initial shortlist state: no proposal, no approval, empty event log."""
    return {"proposal": None, "approved": False, "approval": None, "events": []}


def _timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def propose_shortlist(state, proposed_vendors, mechanical_top, reason=""):
    """Record a human-proposed shortlist. Returns (new_state, message).

    ``proposed_vendors`` is the human's proposed shortlist, in order.
    ``mechanical_top`` is the top-N of whichever mechanical ranking the
    caller is using (e.g. ``weighted_totals()`` or ``consensus_ranking()``),
    trimmed to the same N by the caller before calling this — this module
    does no ranking or trimming itself.

    Refuses (state unchanged, nothing logged):
    - an empty proposal;
    - a proposal that differs from ``mechanical_top`` (by content or order)
      with no non-empty reason given — mirrors ``record_consensus()``'s
      rationale gate exactly in spirit: overriding the mechanical ranking
      requires a stated reason, matching it does not.

    Re-proposing replaces the current proposal (full history stays in
    ``state["events"]``). If the shortlist was previously approved, the
    approval is cleared and an explicit "approval_cleared" event is logged
    — a changed shortlist is never silently treated as still approved.
    """
    state = state or new_shortlist_state()
    proposed_vendors = list(proposed_vendors or [])
    mechanical_top = list(mechanical_top or [])
    reason = (reason or "").strip()

    if not proposed_vendors:
        return state, "Shortlist not proposed: at least one vendor is required."

    matched = proposed_vendors == mechanical_top
    if not matched and not reason:
        return state, (
            "Shortlist not proposed: a reason is required when the proposed "
            "shortlist differs from the mechanical ranking."
        )

    timestamp = _timestamp()
    proposal = {
        "vendors": proposed_vendors,
        "matched_mechanical": matched,
        "reason": reason,
        "timestamp": timestamp,
    }

    events = list(state.get("events", []))
    events.append({
        "type": "proposed",
        "timestamp": timestamp,
        "vendors": proposed_vendors,
        "matched_mechanical": matched,
        "reason": reason,
    })

    was_approved = bool(state.get("approved"))
    if was_approved:
        events.append({
            "type": "approval_cleared",
            "timestamp": timestamp,
            "reason": "Shortlist re-proposed after approval.",
        })

    new_state = {
        "proposal": proposal,
        "approved": False,
        "approval": None,
        "events": events,
    }

    if matched:
        message = "Shortlist proposed, matching the mechanical ranking."
    else:
        message = "Shortlist proposed, differing from the mechanical ranking — reason recorded."
    if was_approved:
        message += " Previous approval cleared."
    return new_state, message


def approve_shortlist(state, approver_name):
    """Approve the current proposed shortlist. Returns (new_state, message).

    Refuses (state unchanged, nothing logged):
    - an empty/whitespace approver name;
    - no current proposal to approve;
    - double-approval (already approved).
    """
    state = state or new_shortlist_state()

    if not approver_name or not approver_name.strip():
        return state, "Shortlist not approved: an approver name is required."
    if state.get("proposal") is None:
        return state, "Shortlist not approved: propose a shortlist first."
    if state.get("approved"):
        return state, "Shortlist is already approved."

    approver_name = approver_name.strip()
    timestamp = _timestamp()
    approval = {"approver": approver_name, "timestamp": timestamp}

    events = list(state.get("events", [])) + [{
        "type": "approved",
        "timestamp": timestamp,
        "approver": approver_name,
    }]

    new_state = {
        "proposal": state["proposal"],
        "approved": True,
        "approval": approval,
        "events": events,
    }
    return new_state, f"Shortlist approved by {approver_name}."


def is_approved(state):
    """True when the current shortlist proposal is approved (None/{} safe)."""
    if not state:
        return False
    return bool(state.get("approved"))


def current_shortlist(state):
    """Display shape for the current proposal, or an empty/unapproved shape.

    Returns:
        {
            "vendors": [str, ...],
            "matched_mechanical": bool or None,  # None if nothing proposed yet
            "reason": str,
            "approved": bool,
            "approver": str or None,
            "approved_at": str or None,
        }
    """
    state = state or new_shortlist_state()
    proposal = state.get("proposal")
    if proposal is None:
        return {
            "vendors": [],
            "matched_mechanical": None,
            "reason": "",
            "approved": False,
            "approver": None,
            "approved_at": None,
        }

    approval = state.get("approval") or {}
    return {
        "vendors": list(proposal["vendors"]),
        "matched_mechanical": proposal["matched_mechanical"],
        "reason": proposal["reason"],
        "approved": bool(state.get("approved")),
        "approver": approval.get("approver"),
        "approved_at": approval.get("timestamp"),
    }


def format_shortlist_log(state):
    """Markdown rendering of the shortlist event history, newest first."""
    events = (state or {}).get("events", [])
    if not events:
        return "_No shortlist proposed yet._"

    lines = ["### Shortlist log", ""]
    for event in reversed(events):
        if event["type"] == "proposed":
            match_text = (
                "matches mechanical ranking" if event["matched_mechanical"]
                else "differs from mechanical ranking"
            )
            suffix = f" — reason: {event['reason']}" if event.get("reason") else ""
            vendors_text = ", ".join(event["vendors"])
            lines.append(
                f"- Proposed {event['timestamp']} — {vendors_text} ({match_text}){suffix}"
            )
        elif event["type"] == "approved":
            lines.append(f"- Approved {event['timestamp']} by {event['approver']}")
        elif event["type"] == "approval_cleared":
            lines.append(f"- Approval cleared {event['timestamp']} — {event['reason']}")
        else:
            lines.append(f"- {event['timestamp']} — {event['type']}")
    return "\n".join(lines)
