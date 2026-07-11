import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.comparison_sample import ARCHITECTURE_DOMAINS, CRITERIA, VENDORS
from app.logic.comparison import (
    comparison_rows,
    consensus_ranking,
    evaluation_progress,
    focus_queue,
    format_consensus_log,
    format_criterion_detail,
    record_consensus,
    score_spread,
    weighted_totals,
)

# Synthetic fixtures for evaluation_progress()/weighted_totals()/
# consensus_ranking() — deliberately independent of the sample data so these
# tests exercise the logic itself, not the shape of comparison_sample.py.
FIX_EVALUATORS = ["Business Rep", "Architect"]
FIX_VENDORS = ["Vendor A", "Vendor B"]
FIX_CRITERIA = [
    {"id": "C1", "weight": 60},
    {"id": "C2", "weight": 40},
]
FIX_PANEL_SCORES = {
    ("C1", "Vendor A"): {"Business Rep": 4, "Architect": 4},
    ("C1", "Vendor B"): {"Business Rep": 2, "Architect": 5},  # spread 3
    ("C2", "Vendor A"): {"Business Rep": 3, "Architect": 3},
    # ("C2", "Vendor B") intentionally unscored.
}
FIX_RESPONSES = {
    ("C1", "Vendor A"): {"summary": "ok", "evidence": "p1", "gaps": [], "confidence": "High"},
    ("C1", "Vendor B"): {"summary": "ok", "evidence": "p2", "gaps": ["Missing DR evidence"], "confidence": "Low"},
    ("C2", "Vendor A"): {"summary": "ok", "evidence": "p3", "gaps": [], "confidence": "High"},
}


def test_comparison_rows_cover_domain():
    rows = comparison_rows("Application architecture")
    assert len(rows) == 4
    for row in rows:
        assert len(row) == 1 + len(VENDORS)


def test_unanswered_criterion_is_visible():
    rows = comparison_rows("Cloud architecture")
    assert any("NOT ANSWERED" in cell for row in rows for cell in row)


def test_score_spread():
    # APP-02 NovaAI: Business Rep 4, Architect 1, Tech PM 2 -> spread 3
    assert score_spread("APP-02", "NovaAI FlowSuite") == 3
    assert score_spread("APP-01", "Acme CaseWorks") == 0
    assert score_spread("NOPE-99", "Acme CaseWorks") is None


def test_focus_queue_prioritises_gate_failures_first():
    items = focus_queue()
    assert items, "focus queue should not be empty with sample data"
    assert items[0]["label"].startswith("GATE"), items[0]
    assert "Fail" in items[0]["label"]


def test_focus_queue_includes_high_variance_and_unanswered():
    labels = [i["label"] for i in focus_queue()]
    assert any("score spread" in l for l in labels)
    assert any("not answered" in l for l in labels)


def test_criterion_detail_flags_divergence():
    detail = format_criterion_detail("APP-02")
    assert "High divergence" in detail
    assert "Panel scores" in detail


def test_consensus_requires_rationale():
    log, message = record_consensus([], "APP-02", VENDORS[0], 3, "   ")
    assert log == []
    assert "rationale is required" in message


def test_consensus_recorded_and_individual_scores_untouched():
    from app.data.comparison_sample import PANEL_SCORES

    before = dict(PANEL_SCORES[("APP-02", "NovaAI FlowSuite")])
    log, message = record_consensus(
        [], "APP-02", "NovaAI FlowSuite", 2,
        "Architect concerns about untestable AI changes accepted by panel."
    )
    assert len(log) == 1
    assert "recorded" in message
    assert PANEL_SCORES[("APP-02", "NovaAI FlowSuite")] == before
    rendered = format_consensus_log(log)
    assert "APP-02" in rendered
    assert "preserved" in rendered


def test_all_criteria_have_valid_domains():
    for criterion in CRITERIA:
        assert criterion["domain"] in ARCHITECTURE_DOMAINS


def test_score_spread_accepts_explicit_panel_scores_without_touching_sample():
    # New optional param must not change any existing (no-arg) call site.
    assert score_spread("C1", "Vendor B", FIX_PANEL_SCORES) == 3
    assert score_spread("C1", "Vendor A", FIX_PANEL_SCORES) == 0
    assert score_spread("C2", "Vendor B", FIX_PANEL_SCORES) is None
    # Sample-data call sites still work unchanged.
    assert score_spread("APP-02", "NovaAI FlowSuite") == 3


def test_evaluation_progress_shape_and_counts():
    progress = evaluation_progress(
        FIX_CRITERIA, FIX_VENDORS, FIX_PANEL_SCORES, FIX_RESPONSES, FIX_EVALUATORS
    )
    assert progress["total_slots"] == 8
    assert progress["filled_slots"] == 6
    assert progress["percent_complete"] == 75.0
    assert progress["criteria_complete"] == ["C1"]
    assert progress["criteria_total"] == 2
    assert progress["evaluators_complete"] == []
    assert progress["evaluators_total"] == 2
    assert progress["open_clarifications"] == 1
    assert progress["material_variances"] == 1


def test_evaluation_progress_all_evaluators_complete_when_everything_scored():
    full_scores = dict(FIX_PANEL_SCORES)
    full_scores[("C2", "Vendor B")] = {"Business Rep": 1, "Architect": 1}
    progress = evaluation_progress(
        FIX_CRITERIA, FIX_VENDORS, full_scores, FIX_RESPONSES, FIX_EVALUATORS
    )
    assert progress["filled_slots"] == 8
    assert progress["percent_complete"] == 100.0
    assert set(progress["criteria_complete"]) == {"C1", "C2"}
    assert set(progress["evaluators_complete"]) == {"Business Rep", "Architect"}


def test_evaluation_progress_empty_inputs_no_crash():
    progress = evaluation_progress([], [], {}, {}, [])
    assert progress["total_slots"] == 0
    assert progress["filled_slots"] == 0
    assert progress["percent_complete"] == 0.0
    assert progress["criteria_complete"] == []
    assert progress["evaluators_complete"] == []
    assert progress["open_clarifications"] == 0
    assert progress["material_variances"] == 0


def test_weighted_totals_uses_panel_mean_when_no_consensus():
    results = weighted_totals(FIX_CRITERIA, FIX_VENDORS, FIX_PANEL_SCORES, [])
    by_vendor = {r["vendor"]: r for r in results}

    vendor_a = by_vendor["Vendor A"]
    assert vendor_a["total"] == 3.6  # (4*60 + 3*40) / 100
    assert vendor_a["n_consensus"] == 0
    assert vendor_a["n_panel_mean"] == 2
    assert vendor_a["n_unscored"] == 0
    assert vendor_a["n_criteria"] == 2

    vendor_b = by_vendor["Vendor B"]
    assert vendor_b["total"] == 2.1  # mean(2,5)=3.5 * 60/100; C2 unscored
    assert vendor_b["n_consensus"] == 0
    assert vendor_b["n_panel_mean"] == 1
    assert vendor_b["n_unscored"] == 1


def test_weighted_totals_is_sorted_descending_and_never_labels_a_winner():
    results = weighted_totals(FIX_CRITERIA, FIX_VENDORS, FIX_PANEL_SCORES, [])
    totals = [r["total"] for r in results]
    assert totals == sorted(totals, reverse=True)
    assert results[0]["vendor"] == "Vendor A"
    for r in results:
        assert "winner" not in r
        assert "recommended" not in r
        assert "shortlisted" not in r


def test_weighted_totals_consensus_overrides_panel_mean():
    consensus_log = [
        {"criterion": "C1", "vendor": "Vendor B", "score": 5, "rationale": "Panel agreed on architect's read."},
    ]
    results = weighted_totals(FIX_CRITERIA, FIX_VENDORS, FIX_PANEL_SCORES, consensus_log)
    vendor_b = next(r for r in results if r["vendor"] == "Vendor B")
    # Consensus score (5) replaces the panel mean (3.5) for C1.
    assert vendor_b["total"] == 3.0  # 5 * 60 / 100, C2 still unscored
    assert vendor_b["n_consensus"] == 1
    assert vendor_b["n_panel_mean"] == 0
    assert vendor_b["n_unscored"] == 1


def test_weighted_totals_uses_most_recent_consensus_entry():
    consensus_log = [
        {"criterion": "C1", "vendor": "Vendor B", "score": 1, "rationale": "First pass."},
        {"criterion": "C1", "vendor": "Vendor B", "score": 5, "rationale": "Revised after discussion."},
    ]
    results = weighted_totals(FIX_CRITERIA, FIX_VENDORS, FIX_PANEL_SCORES, consensus_log)
    vendor_b = next(r for r in results if r["vendor"] == "Vendor B")
    assert vendor_b["total"] == 3.0  # uses score=5, not the superseded score=1


def test_weighted_totals_unscored_criteria_contribute_nothing_but_are_counted():
    results = weighted_totals(FIX_CRITERIA, FIX_VENDORS, FIX_PANEL_SCORES, [])
    vendor_b = next(r for r in results if r["vendor"] == "Vendor B")
    assert vendor_b["n_unscored"] == 1
    assert vendor_b["n_consensus"] + vendor_b["n_panel_mean"] + vendor_b["n_unscored"] == vendor_b["n_criteria"]


def test_consensus_ranking_empty_log_returns_honest_message_not_fabricated_ranking():
    result = consensus_ranking(FIX_VENDORS, [])
    assert result["ranking"] == []
    assert result["message"]
    assert "no consensus" in result["message"].lower()


def test_consensus_ranking_sums_consensus_scores_with_coverage():
    consensus_log = [
        {"criterion": "C1", "vendor": "Vendor A", "score": 4, "rationale": "Agreed."},
        {"criterion": "C1", "vendor": "Vendor B", "score": 5, "rationale": "Agreed."},
    ]
    result = consensus_ranking(FIX_VENDORS, consensus_log)
    assert result["message"] is None
    ranking = result["ranking"]
    assert ranking[0]["vendor"] == "Vendor B"
    assert ranking[0]["total"] == 5
    assert ranking[0]["n_consensus"] == 1
    assert ranking[0]["n_criteria"] == 1
    assert ranking[1]["vendor"] == "Vendor A"
    assert ranking[1]["total"] == 4


def test_consensus_ranking_uses_most_recent_entry_per_vendor_criterion():
    consensus_log = [
        {"criterion": "C1", "vendor": "Vendor A", "score": 2, "rationale": "First pass."},
        {"criterion": "C1", "vendor": "Vendor A", "score": 4, "rationale": "Revised."},
    ]
    result = consensus_ranking(FIX_VENDORS, consensus_log)
    vendor_a = next(r for r in result["ranking"] if r["vendor"] == "Vendor A")
    assert vendor_a["total"] == 4


def test_consensus_ranking_never_labels_a_winner():
    consensus_log = [{"criterion": "C1", "vendor": "Vendor A", "score": 4, "rationale": "Agreed."}]
    result = consensus_ranking(FIX_VENDORS, consensus_log)
    for r in result["ranking"]:
        assert "winner" not in r
        assert "recommended" not in r
        assert "shortlisted" not in r


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: ok")
    print("All comparison tests passed.")
