"""Plain-English readout generated from the visible grid values.

Deliberately no scores, no weighting, no roll-ups. The readout only
restates what the grids already show, in sentences.
"""

from app.data.sample_data import OPTIONS


def _normalise(value):
    return str(value).strip().capitalize() if value is not None else "Unknown"


def _rows_by_option(table, option_index):
    """Return {row_label: cell_value} for one option column."""
    result = {}
    for row in table:
        label = str(row[0]).strip()
        cell = row[option_index + 1] if option_index + 1 < len(row) else "Unknown"
        result[label] = _normalise(cell)
    return result


def _join(items):
    items = list(items)
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def generate_readout(capability_table, viability_table):
    """Build a plain-English interpretation of both grids.

    Tables are lists of rows; first cell of each row is the row label,
    remaining cells align with OPTIONS.
    """
    capability_table = [list(r) for r in capability_table]
    viability_table = [list(r) for r in viability_table]

    viable, clarify, blocked = [], [], []
    paragraphs = []

    for i, option in enumerate(OPTIONS):
        caps = _rows_by_option(capability_table, i)
        gates = _rows_by_option(viability_table, i)

        strong = [k for k, v in caps.items() if v == "Strong"]
        weak = [k for k, v in caps.items() if v == "Weak"]
        fails = [k for k, v in gates.items() if v == "Fail"]
        clarifies = [k for k, v in gates.items() if v == "Clarify"]
        unknown_gates = [k for k, v in gates.items() if v == "Unknown"]

        sentences = []
        if strong:
            sentences.append(
                f"**{option}** appears strong on {_join(f.lower() for f in strong)}."
            )
        else:
            sentences.append(
                f"**{option}** shows no strong capability coverage in the matrix so far."
            )
        if weak:
            sentences.append(
                f"It looks weak on {_join(f.lower() for f in weak)}."
            )

        if fails:
            blocked.append(option)
            concerns = fails + clarifies
            sentences.append(
                f"On the viability gate it currently fails or requires clarification on "
                f"{_join(f.lower() for f in concerns)}. It should not proceed as the "
                f"core system until these are resolved."
            )
            if strong:
                sentences.append(
                    f"It may still be useful as a supporting layer for "
                    f"{_join(f.lower() for f in strong)}, but does not yet appear "
                    f"viable as the system of record."
                )
        elif clarifies or unknown_gates:
            clarify.append(option)
            open_items = clarifies + unknown_gates
            sentences.append(
                f"No outright viability failures, but {_join(f.lower() for f in open_items)} "
                f"still need clarification before this option can be relied on."
            )
        else:
            viable.append(option)
            sentences.append(
                "It passes all baseline viability checks as currently assessed."
            )

        paragraphs.append(" ".join(sentences))

    summary_lines = ["## Readout", ""]
    if viable:
        summary_lines.append(
            f"**Looks viable enough to continue:** {_join(viable)}."
        )
    if clarify:
        summary_lines.append(
            f"**Needs clarification before continuing:** {_join(clarify)}."
        )
    if blocked:
        summary_lines.append(
            f"**Should not proceed yet:** {_join(blocked)}."
        )
    if not (viable or clarify or blocked):
        summary_lines.append("No assessments entered yet.")

    summary_lines.append("")
    summary_lines.extend(paragraphs)
    summary_lines.append("")
    summary_lines.append(
        "_This readout restates the grid in plain English. It carries no scores or "
        "weighting; read the grids themselves before deciding._"
    )
    return "\n\n".join(summary_lines)
