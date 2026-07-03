# MVP-0 validation test script

## Setup

1. Open the app (locally via `python app.py`, or the Hugging Face Space).
2. Read the Scenario Setup section.
3. Click **Load completed example** and click **Generate readout** to see the
   intended end state, then click **Load blank test** to start fresh.

## Task

Working from the scenario, fill in the Capability Coverage Matrix first, then the
Baseline Viability Gate, then generate the readout.

## Questions for testers

1. Did any gate feel like you had already answered it in the matrix?
2. What else would you want to check before proceeding?
3. Does this need a score, or is reading the grid enough?
4. Would you actually fill this in for a real sourcing decision?
5. Who would own this artifact in your organisation?

## What to observe

- Does the tester assess capability before viability, or jump to viability?
- Does the readout match how they would summarise the grids themselves?
- Do they ask for features that are deliberately out of scope (scores, weighting,
  evidence, exports)? Note which ones and why.
