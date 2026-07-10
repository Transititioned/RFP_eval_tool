"""Logic for the side-by-side vendor comparison.

Models how evaluation panels actually work: evaluators score individually,
divergence between them is a primary signal, and consensus is a human
decision recorded with a rationale — never a computed average. The system
never asserts a blended winner.
"""

from app.data.comparison_sample import (
    CRITERIA,
    EVALUATORS,
    GATES,
    PANEL_SCORES,
    RESPONSES,
    VENDORS,
)


def criteria_for_domain(domain):
    return [c for c in CRITERIA if c["domain"] == domain]


def score_spread(criterion_id, vendor):
    """Max minus min across evaluators. None if unscored."""
    scores = PANEL_SCORES.get((criterion_id, vendor))
    if not scores:
        return None
    values = list(scores.values())
    return max(values) - min(values)


def comparison_rows(domain):
    """Rows for the comparison grid: criterion + one summary cell per vendor."""
    rows = []
    for criterion in criteria_for_domain(domain):
        row = [f"{criterion['id']} — {criterion['statement']}"]
        for vendor in VENDORS:
            response = RESPONSES.get((criterion["id"], vendor))
            if response is None:
                cell = "NOT ANSWERED"
            else:
                cell = response["summary"]
                if response["gaps"]:
                    cell += " | Gaps: " + "; ".join(response["gaps"])
                cell += f" | Evidence: {response['evidence']} | Confidence: {response['confidence']}"
            row.append(cell)
        rows.append(row)
    return rows


def gate_rows():
    return [
        [g["statement"]] + [g["status"][v] for v in VENDORS]
        for g in GATES
    ]


def focus_queue():
    """Order criteria/vendor items by how much workshop attention they need.

    Priority: gate failures first (always), then unanswered criteria, then
    high evaluator variance, then low-confidence evidence.
    """
    items = []

    for gate in GATES:
        for vendor in VENDORS:
            status = gate["status"][vendor]
            if status in ("Fail", "Clarify"):
                items.append({
                    "priority": 0 if status == "Fail" else 1,
                    "label": f"GATE {gate['id']}: {vendor} — {status}",
                    "reason": gate["statement"],
                })

    for criterion in CRITERIA:
        for vendor in VENDORS:
            key = (criterion["id"], vendor)
            response = RESPONSES.get(key)
            if response is None:
                items.append({
                    "priority": 1,
                    "label": f"{criterion['id']}: {vendor} — not answered",
                    "reason": criterion["statement"],
                })
                continue
            spread = score_spread(criterion["id"], vendor)
            if spread is not None and spread >= 2:
                scores = PANEL_SCORES[key]
                detail = ", ".join(f"{e} {s}" for e, s in scores.items())
                items.append({
                    "priority": 2,
                    "label": f"{criterion['id']}: {vendor} — score spread {spread} ({detail})",
                    "reason": criterion["statement"],
                })
            elif response["confidence"] == "Low":
                items.append({
                    "priority": 3,
                    "label": f"{criterion['id']}: {vendor} — low-confidence evidence",
                    "reason": criterion["statement"],
                })

    items.sort(key=lambda i: i["priority"])
    return items


def format_focus_queue():
    items = focus_queue()
    if not items:
        return "_Nothing needs workshop attention._"
    lines = ["### Workshop focus queue", ""]
    lines += [
        f"{n}. **{item['label']}**  \n   {item['reason']}"
        for n, item in enumerate(items, start=1)
    ]
    lines.append("")
    lines.append(
        "_Ordered: gate failures, unanswered criteria, high score spread, "
        "low-confidence evidence. Discuss these before anything else._"
    )
    return "\n".join(lines)


def format_criterion_detail(criterion_id):
    """Full workshop view of one criterion: responses, panel scores, spread."""
    criterion = next((c for c in CRITERIA if c["id"] == criterion_id), None)
    if criterion is None:
        return "_Unknown criterion._"

    lines = [f"### {criterion['id']} — {criterion['statement']}", ""]
    for vendor in VENDORS:
        key = (criterion_id, vendor)
        lines.append(f"#### {vendor}")
        response = RESPONSES.get(key)
        if response is None:
            lines.append("**Not answered in proposal.**")
        else:
            lines.append(response["summary"])
            lines.append(f"- Evidence: {response['evidence']}")
            lines.append(f"- Confidence: {response['confidence']}")
            if response["gaps"]:
                lines.append("- Gaps: " + "; ".join(response["gaps"]))
        scores = PANEL_SCORES.get(key)
        if scores:
            spread = score_spread(criterion_id, vendor)
            score_text = " · ".join(f"{e}: **{s}**" for e, s in scores.items())
            lines.append(f"- Panel scores: {score_text} (spread {spread})")
            if spread is not None and spread >= 2:
                lines.append(
                    "- **High divergence — discuss in workshop before consensus.**"
                )
        lines.append("")
    return "\n".join(lines)


def record_consensus(log, criterion_id, vendor, score, rationale):
    """Validate and append a consensus decision. Returns (log, message).

    Consensus requires a rationale — it is a human decision, not a number.
    Individual panel scores are untouched.
    """
    if not criterion_id or not vendor:
        return log, "Select a criterion and a vendor."
    if not rationale or not rationale.strip():
        return log, "Consensus not recorded: a rationale is required."

    entry = {
        "criterion": criterion_id,
        "vendor": vendor,
        "score": score,
        "rationale": rationale.strip(),
    }
    log = list(log) + [entry]
    return log, f"Consensus recorded for {criterion_id} / {vendor}."


def format_consensus_log(log):
    if not log:
        return "_No consensus decisions recorded yet._"
    lines = [
        "| Criterion | Vendor | Consensus score | Rationale |",
        "|---|---|---|---|",
    ]
    lines += [
        f"| {e['criterion']} | {e['vendor']} | {e['score']} | {e['rationale']} |"
        for e in log
    ]
    lines.append("")
    lines.append(
        "_Individual evaluator scores are preserved unchanged alongside "
        "these consensus decisions._"
    )
    return "\n".join(lines)
