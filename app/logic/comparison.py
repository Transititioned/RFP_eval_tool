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


def score_spread(criterion_id, vendor, panel_scores=None):
    """Max minus min across evaluators. None if unscored.

    ``panel_scores`` defaults to the sample ``PANEL_SCORES`` so every
    existing call site keeps working unchanged. Pass an explicit
    ``{(criterion_id, vendor): {evaluator: score}}`` mapping (as
    ``evaluation_progress()``/``weighted_totals()`` do) to compute spread
    against synthetic/session data instead of the sample set.
    """
    source = panel_scores if panel_scores is not None else PANEL_SCORES
    scores = source.get((criterion_id, vendor))
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


def evaluation_progress(criteria, vendors, panel_scores, responses, evaluators):
    """Landing-dashboard telemetry for the Evaluation stage.

    This is process-completion bookkeeping only — how much of the panel
    scoring work has been done — never a vendor score, ranking, or
    aggregate. All four inputs are plain data (shaped like
    ``CRITERIA``/``VENDORS``/``PANEL_SCORES``/``RESPONSES``/``EVALUATORS``)
    so this stays testable against synthetic fixtures.

    Returns a dict:
        {
            "total_slots": int,          # len(criteria) * len(vendors) * len(evaluators)
            "filled_slots": int,         # slots with a recorded evaluator score
            "percent_complete": float,   # filled/total * 100, rounded to 1dp (0.0 if no slots)
            "evaluators_complete": [str, ...],  # evaluators who have scored every slot
            "evaluators_total": int,
            "criteria_complete": [str, ...],    # criterion ids fully scored by every
                                                 # evaluator for every vendor
            "criteria_total": int,
            "open_clarifications": int,  # (criterion, vendor) cells with non-empty gaps
            "material_variances": int,   # (criterion, vendor) cells with score_spread >= 2
        }
    """
    criteria = criteria or []
    vendors = vendors or []
    evaluators = evaluators or []
    panel_scores = panel_scores or {}
    responses = responses or {}

    total_slots = len(criteria) * len(vendors) * len(evaluators)
    filled_slots = 0
    criteria_complete = []
    evaluator_filled_counts = {evaluator: 0 for evaluator in evaluators}
    open_clarifications = 0
    material_variances = 0

    for criterion in criteria:
        criterion_id = criterion["id"]
        criterion_fully_scored = bool(vendors)
        for vendor in vendors:
            key = (criterion_id, vendor)
            scores = panel_scores.get(key, {})
            for evaluator in evaluators:
                if evaluator in scores:
                    filled_slots += 1
                    evaluator_filled_counts[evaluator] += 1
                else:
                    criterion_fully_scored = False

            spread = score_spread(criterion_id, vendor, panel_scores)
            if spread is not None and spread >= 2:
                material_variances += 1

            response = responses.get(key)
            if response and response.get("gaps"):
                open_clarifications += 1

        if criterion_fully_scored:
            criteria_complete.append(criterion_id)

    slots_per_evaluator = len(criteria) * len(vendors)
    evaluators_complete = [
        evaluator
        for evaluator in evaluators
        if slots_per_evaluator and evaluator_filled_counts[evaluator] == slots_per_evaluator
    ]

    percent_complete = round((filled_slots / total_slots) * 100, 1) if total_slots else 0.0

    return {
        "total_slots": total_slots,
        "filled_slots": filled_slots,
        "percent_complete": percent_complete,
        "evaluators_complete": evaluators_complete,
        "evaluators_total": len(evaluators),
        "criteria_complete": criteria_complete,
        "criteria_total": len(criteria),
        "open_clarifications": open_clarifications,
        "material_variances": material_variances,
    }


def weighted_totals(criteria, vendors, panel_scores, consensus_log):
    """Per-vendor totals for the Traditional weighted scoring mode.

    Score-per-criterion rule: use the most recently recorded consensus
    score for that (criterion, vendor) if one exists in ``consensus_log``;
    otherwise the mean of the individual panel scores; otherwise the
    criterion contributes nothing to the total but is still counted in
    coverage, so a partial total is never mistaken for a complete one.

    ``consensus_log`` is the list shape produced by ``record_consensus()``
    (each entry a dict with "criterion", "vendor", "score", "rationale").

    Returns a list of dicts, one per vendor, ordered by "total" descending
    (this ordering is data for the UI to display — it is never labelled a
    winner/recommendation):
        [
            {
                "vendor": str,
                "total": float,       # sum(score * weight) / 100, rounded to 2dp
                "n_consensus": int,   # criteria scored via consensus
                "n_panel_mean": int,  # criteria scored via panel mean (no consensus)
                "n_unscored": int,    # criteria with no score at all
                "n_criteria": int,    # len(criteria), for "n of n_criteria" display
            },
            ...
        ]
    """
    criteria = criteria or []
    vendors = vendors or []
    panel_scores = panel_scores or {}
    consensus_log = consensus_log or []

    # Last recorded entry per (criterion, vendor) is the current consensus,
    # matching the "re-recording replaces current, history stays in the
    # log" convention used elsewhere (e.g. eligibility outcomes).
    consensus_by_key = {}
    for entry in consensus_log:
        consensus_by_key[(entry["criterion"], entry["vendor"])] = entry["score"]

    results = []
    for vendor in vendors:
        total = 0.0
        n_consensus = 0
        n_panel_mean = 0
        n_unscored = 0
        for criterion in criteria:
            criterion_id = criterion["id"]
            weight = criterion.get("weight") or 0
            key = (criterion_id, vendor)

            if key in consensus_by_key:
                score = consensus_by_key[key]
                n_consensus += 1
            else:
                scores = panel_scores.get(key)
                if scores:
                    score = sum(scores.values()) / len(scores)
                    n_panel_mean += 1
                else:
                    n_unscored += 1
                    continue

            total += score * weight / 100

        results.append({
            "vendor": vendor,
            "total": round(total, 2),
            "n_consensus": n_consensus,
            "n_panel_mean": n_panel_mean,
            "n_unscored": n_unscored,
            "n_criteria": len(criteria),
        })

    results.sort(key=lambda r: r["total"], reverse=True)
    return results


def consensus_ranking(vendors, consensus_log):
    """Per-vendor sum of recorded consensus scores (Panel + Consensus mode).

    Unlike ``weighted_totals()`` this mode has no weights — it sums the
    raw consensus scores recorded so far. Coverage is reported against the
    set of criteria that have *any* recorded consensus entry (this
    function deliberately takes no ``criteria`` list, so "total" coverage
    means "criteria discussed in consensus so far", not "criteria in the
    framework" — the caller can cross-reference against the full criteria
    list if it needs that).

    Returns a dict:
        {
            "ranking": [
                {"vendor": str, "total": number, "n_consensus": int, "n_criteria": int},
                ...
            ],  # ordered by total descending; [] if nothing recorded
            "message": str or None,  # honest explanation when ranking is [];
                                      # None once a real ranking exists
        }

    An empty/missing ``consensus_log`` returns an empty ranking with an
    explanatory message — never a fabricated ranking.
    """
    vendors = vendors or []
    consensus_log = consensus_log or []

    if not consensus_log:
        return {
            "ranking": [],
            "message": "No consensus decisions recorded yet — ranking not available.",
        }

    # Last recorded entry per (criterion, vendor) is current, same
    # convention as weighted_totals().
    current = {}
    for entry in consensus_log:
        current[(entry["criterion"], entry["vendor"])] = entry["score"]

    total_criteria = len({criterion_id for criterion_id, _vendor in current.keys()})

    ranking = []
    for vendor in vendors:
        vendor_scores = [
            score for (criterion_id, v), score in current.items() if v == vendor
        ]
        ranking.append({
            "vendor": vendor,
            "total": sum(vendor_scores),
            "n_consensus": len(vendor_scores),
            "n_criteria": total_criteria,
        })

    ranking.sort(key=lambda r: r["total"], reverse=True)
    return {"ranking": ranking, "message": None}
