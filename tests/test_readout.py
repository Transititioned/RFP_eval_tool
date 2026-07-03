import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.sample_data import (
    COMPLETED_CAPABILITY_MATRIX,
    COMPLETED_VIABILITY_GATE,
    blank_capability_matrix,
    blank_viability_gate,
)
from app.logic.readout import generate_readout


def test_blank_readout_runs():
    text = generate_readout(blank_capability_matrix(), blank_viability_gate())
    assert "Readout" in text
    assert "score" not in text.lower().replace("no scores", "")


def test_completed_example_flags_shiny_ai_as_blocked():
    text = generate_readout(COMPLETED_CAPABILITY_MATRIX, COMPLETED_VIABILITY_GATE)
    assert "Should not proceed yet" in text
    assert "Shiny AI workflow/analytics product" in text
    # The shiny AI product is strong on workflow but fails enterprise basics.
    assert "system-of-record clarity" in text
    assert "data ownership / export" in text
    assert "audit logging" in text


def test_completed_example_identifies_viable_option():
    text = generate_readout(COMPLETED_CAPABILITY_MATRIX, COMPLETED_VIABILITY_GATE)
    assert "Looks viable enough to continue" in text
    assert "Needs clarification before continuing" in text


if __name__ == "__main__":
    test_blank_readout_runs()
    test_completed_example_flags_shiny_ai_as_blocked()
    test_completed_example_identifies_viable_option()
    print("All tests passed.")
