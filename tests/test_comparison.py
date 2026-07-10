import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.comparison_sample import ARCHITECTURE_DOMAINS, CRITERIA, VENDORS
from app.logic.comparison import (
    comparison_rows,
    focus_queue,
    format_consensus_log,
    format_criterion_detail,
    record_consensus,
    score_spread,
)


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


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"{name}: ok")
    print("All comparison tests passed.")
