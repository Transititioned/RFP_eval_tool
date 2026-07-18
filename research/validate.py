"""Deterministic validation of the research structure and contracts.

Run: python research/validate.py

Checks (no network, no dependencies, stdlib only):
  1. The three research layers and their required files exist.
  2. The evidence contract defines the classifications and verdicts, and
     its worked example parses with the exact tag grammar.
  3. The source-ledger schema doc's example entry carries all required
     fields.
  4. The research agents exist with well-formed frontmatter, and the
     /research-rfp command exists and covers its required duties.
  5. The mission template is complete.
  6. Every mission (excluding the template) has a well-formed charter,
     state file, and ledger; workstream source-ID blocks parse and do
     not overlap; each workstream's agent exists.
  7. Mission documents (findings, brief, verification, contrarian
     review) use well-formed claim tags; verdict tags sit adjacent to a
     classification tag; Evidence/Inference citations resolve (findings
     may cite only the ledger plus their own proposals; other documents
     the ledger plus any proposals); findings' proposed source IDs stay
     inside their workstream's block; hypotheses carry "Validate by:"
     lines; ledger entries follow the schema; the brief declares a
     draft/final status.

Known limitation (by design, see research-core.md "Claim discipline"):
the validator checks tag format and placement, not tag *presence* — an
untagged material claim is a human check.

Exit code 0 and "ALL CHECKS PASSED" on success; 1 with FAIL lines otherwise.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "research"
AGENTS_DIR = ROOT / ".claude" / "agents"
COMMANDS_DIR = ROOT / ".claude" / "commands"

RESEARCH_AGENTS = [
    "competitor-scout",
    "procurement-analyst",
    "ux-pattern-analyst",
    "evidence-verifier",
    "contrarian-researcher",
    "product-synthesist",
]

# Exact claim-tag grammar from research/core/evidence-contract.md
RE_EVIDENCE = re.compile(r"\[Evidence: S\d+(?:, S\d+)*\]")
RE_INFERENCE = re.compile(r"\[Inference: from S\d+(?:, S\d+)*\]")
RE_HYPOTHESIS = re.compile(r"\[Hypothesis\]")
RE_VERIFIED = re.compile(r"\[Verified: \d{4}-\d{2}-\d{2}\]")
RE_DISPUTED = re.compile(r"\[Disputed: \d{4}-\d{2}-\d{2} — [^\]]+\]")
RE_DOWNGRADED = re.compile(r"\[Downgraded: \d{4}-\d{2}-\d{2} — from (?:Evidence|Inference)\]")
CLASSIFICATION_RES = (RE_EVIDENCE, RE_INFERENCE, RE_HYPOTHESIS)
VERDICT_RES = (RE_VERIFIED, RE_DISPUTED, RE_DOWNGRADED)
# A verdict tag must immediately follow a classification tag
RE_CLASS_AT_END = re.compile(
    r"(?:\[Evidence: S\d+(?:, S\d+)*\]|\[Inference: from S\d+(?:, S\d+)*\]|\[Hypothesis\])\Z"
)
# Anything that looks like it is trying to be one of our tags
RE_TAG_CANDIDATE = re.compile(
    r"\[(?:evidence|inference|hypothesis|verified|disputed|downgraded)[^\]]*\]",
    re.IGNORECASE,
)
RE_SOURCE_ID = re.compile(r"S(\d+)")
RE_LEDGER_HEADING = re.compile(r"^### (S\d+) — .+", re.MULTILINE)
LEDGER_FIELDS = ["URL:", "Type:", "Accessed:", "Credibility:", "Added by:", "Notes:"]
# Workstream table row: | WS1 | agent | question | `findings/x.md` | S101-S199 |
RE_WS_ROW = re.compile(
    r"^\|\s*(WS\d+)\s*\|\s*([a-z0-9-]+)\s*\|.+\|\s*`(findings/[^`]+)`\s*\|"
    r"\s*S(\d+)[–-]S(\d+)\s*\|\s*$",
    re.MULTILINE,
)

failures = []
passes = 0


def check(ok, label):
    global passes
    if ok:
        passes += 1
    else:
        failures.append(label)
        print("FAIL: " + label)


def read(path):
    return path.read_text(encoding="utf-8")


def check_tags(text, label):
    """Tag grammar for one document. Returns the strict tags found."""
    strict = []
    for rx in CLASSIFICATION_RES + VERDICT_RES:
        strict.extend(m.group(0) for m in rx.finditer(text))
    candidates = [m.group(0) for m in RE_TAG_CANDIDATE.finditer(text)]
    malformed = [c for c in candidates if c not in strict]
    check(not malformed, "%s: malformed claim tags: %s" % (label, malformed))
    floating = []
    for rx in VERDICT_RES:
        for m in rx.finditer(text):
            prefix = text[: m.start()].rstrip()
            if not RE_CLASS_AT_END.search(prefix):
                floating.append(m.group(0))
    check(
        not floating,
        "%s: verdict tag(s) not adjacent to a classification tag: %s" % (label, floating),
    )
    return strict


def check_citations(text, known_ids, label):
    cited = set()
    for rx in (RE_EVIDENCE, RE_INFERENCE):
        for m in rx.finditer(text):
            cited.update(int(n) for n in RE_SOURCE_ID.findall(m.group(0)))
    unresolved = sorted(n for n in cited if n not in known_ids)
    check(
        not unresolved,
        "%s: cites unknown sources %s" % (label, ["S%d" % n for n in unresolved]),
    )


def check_validate_by(text, label):
    n_hyp = len(RE_HYPOTHESIS.findall(text))
    check(
        text.count("Validate by:") >= n_hyp,
        "%s: %d [Hypothesis] tag(s) but fewer 'Validate by:' lines" % (label, n_hyp),
    )


def check_ledger_entries(text, label):
    ids = set(RE_LEDGER_HEADING.findall(text))
    for lid in sorted(ids):
        entry = re.search(
            r"^### %s — .+?(?=^### S\d|\Z)" % lid, text, re.MULTILINE | re.DOTALL
        ).group(0)
        for field in LEDGER_FIELDS:
            check(field in entry, "%s: entry %s missing '%s'" % (label, lid, field))
    return ids


# --- 1. Layer structure -----------------------------------------------------
required_files = [
    RESEARCH / "README.md",
    RESEARCH / "core" / "research-core.md",
    RESEARCH / "core" / "evidence-contract.md",
    RESEARCH / "core" / "source-ledger.md",
    RESEARCH / "packs" / "rfp" / "pack.md",
    RESEARCH / "context" / "project-context.md",
    RESEARCH / "missions" / "_template" / "mission.md",
    RESEARCH / "missions" / "_template" / "state.md",
    RESEARCH / "missions" / "_template" / "ledger.md",
    RESEARCH / "missions" / "_template" / "findings" / "_workstream-template.md",
]
for f in required_files:
    check(f.is_file(), "missing required file: %s" % f.relative_to(ROOT))

if failures:
    print("\n%d check(s) failed before content checks could run." % len(failures))
    sys.exit(1)

# --- 2. Evidence contract ---------------------------------------------------
contract = read(RESEARCH / "core" / "evidence-contract.md")
for term in [
    "Evidence", "Inference", "Hypothesis",
    "Verified", "Disputed", "Downgraded", "Validate by:",
]:
    check(term in contract, "evidence contract: missing term '%s'" % term)

example = re.search(
    r"<!-- contract-example:start -->(.*?)<!-- contract-example:end -->",
    contract,
    re.DOTALL,
)
check(example is not None, "evidence contract: worked example block missing")
if example:
    ex = example.group(1)
    check(len(RE_EVIDENCE.findall(ex)) == 3, "contract example: expected 3 Evidence tags")
    check(len(RE_INFERENCE.findall(ex)) == 2, "contract example: expected 2 Inference tags")
    check(len(RE_HYPOTHESIS.findall(ex)) == 1, "contract example: expected 1 Hypothesis tag")
    check(len(RE_VERIFIED.findall(ex)) == 1, "contract example: expected 1 Verified tag")
    check(len(RE_DISPUTED.findall(ex)) == 1, "contract example: expected 1 Disputed tag")
    check(len(RE_DOWNGRADED.findall(ex)) == 1, "contract example: expected 1 Downgraded tag")
    check("Validate by:" in ex, "contract example: Hypothesis lacks 'Validate by:' line")
    check_tags(ex, "contract example")
    check(
        not RE_DISPUTED.search("[Disputed: 2026-07-18]"),
        "grammar self-test: reasonless [Disputed:] must be rejected",
    )

# --- 3. Source-ledger schema ------------------------------------------------
ledger_doc = read(RESEARCH / "core" / "source-ledger.md")
ex = re.search(
    r"<!-- ledger-example:start -->(.*?)<!-- ledger-example:end -->",
    ledger_doc,
    re.DOTALL,
)
check(ex is not None, "source-ledger doc: example entry block missing")
if ex:
    check(
        RE_LEDGER_HEADING.search(ex.group(1)) is not None,
        "source-ledger doc: example heading malformed",
    )
    for field in LEDGER_FIELDS:
        check(field in ex.group(1), "source-ledger doc: example missing field '%s'" % field)

# --- 4. Agents and command --------------------------------------------------
for name in RESEARCH_AGENTS:
    path = AGENTS_DIR / (name + ".md")
    if not path.is_file():
        check(False, "missing agent: .claude/agents/%s.md" % name)
        continue
    text = read(path)
    fm = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if fm is None:
        check(False, "agent %s: missing frontmatter" % name)
        continue
    front = fm.group(1)
    check(
        re.search(r"^name: %s\s*$" % re.escape(name), front, re.MULTILINE) is not None,
        "agent %s: frontmatter name must match filename" % name,
    )
    for key in ("description:", "tools:", "model:"):
        check(key in front, "agent %s: frontmatter missing '%s'" % (name, key))
    check(
        "research/core/research-core.md" in text
        and "research/core/evidence-contract.md" in text,
        "agent %s: must direct reading of the core contracts" % name,
    )

cmd_path = COMMANDS_DIR / "research-rfp.md"
check(cmd_path.is_file(), "missing command: .claude/commands/research-rfp.md")
if cmd_path.is_file():
    cmd = read(cmd_path)
    check(cmd.startswith("---"), "command: missing frontmatter")
    for duty, needle in [
        ("plan phase", "## 1. Plan"),
        ("parallel delegation", "parallel"),
        ("explicit delegation mechanism", "Agent tool"),
        ("absolute-path passing", "absolute path"),
        ("source ledger", "ledger.md"),
        ("verification", "evidence-verifier"),
        ("contrarian review", "contrarian-researcher"),
        ("synthesis", "product-synthesist"),
        ("restartable state", "state.md"),
        ("decision brief", "brief.md"),
    ]:
        check(needle in cmd, "command: missing %s ('%s')" % (duty, needle))

# --- 5/6. Missions ----------------------------------------------------------
missions_dir = RESEARCH / "missions"
missions = sorted(
    d for d in missions_dir.iterdir() if d.is_dir() and d.name != "_template"
)
check(len(missions) >= 1, "no missions instantiated under research/missions/")

VALID_PHASES = [
    "Not started", "Plan", "Investigate", "Merge", "Verify",
    "Synthesise (draft)", "Contrarian review", "Finalise", "Done",
]
VALID_STATUSES = ["Planned", "In progress", "Complete", "Abandoned"]

for mission in missions:
    mname = mission.name
    charter_p = mission / "mission.md"
    state_p = mission / "state.md"
    ledger_p = mission / "ledger.md"
    for p in (charter_p, state_p, ledger_p):
        check(p.is_file(), "%s: missing %s" % (mname, p.name))
    if not (charter_p.is_file() and state_p.is_file() and ledger_p.is_file()):
        continue

    charter = read(charter_p)
    for section in [
        "## Mission statement", "## Decision this informs", "## Layers in force",
        "## Workstreams", "## Constraints", "## Deliverable", "## Status",
    ]:
        check(section in charter, "%s: mission.md missing '%s'" % (mname, section))

    status_m = re.search(r"## Status\s*\n+([^\n<]+)", charter)
    check(
        status_m is not None and status_m.group(1).strip() in VALID_STATUSES,
        "%s: mission.md Status must be one of %s" % (mname, VALID_STATUSES),
    )

    rows = RE_WS_ROW.findall(charter)
    check(len(rows) >= 1, "%s: no parseable workstream rows" % mname)
    blocks = []
    ws_blocks_by_file = {}
    for ws_id, agent, findings_file, lo, hi in rows:
        lo, hi = int(lo), int(hi)
        check(lo < hi, "%s: %s source-ID block empty or inverted" % (mname, ws_id))
        check(
            hi < 901,
            "%s: %s block overlaps reserved verifier/contrarian block S901+" % (mname, ws_id),
        )
        for plo, phi, pid in blocks:
            check(
                hi < plo or lo > phi,
                "%s: %s block overlaps %s" % (mname, ws_id, pid),
            )
        blocks.append((lo, hi, ws_id))
        ws_blocks_by_file[findings_file] = (lo, hi, ws_id)
        check(
            (AGENTS_DIR / (agent + ".md")).is_file(),
            "%s: %s names unknown agent '%s'" % (mname, ws_id, agent),
        )

    state = read(state_p)
    phase_m = re.search(r"## Phase\s*\n+([^\n<]+)", state)
    check(
        phase_m is not None and phase_m.group(1).strip() in VALID_PHASES,
        "%s: state.md Phase must be one of %s" % (mname, VALID_PHASES),
    )
    check("## Next action" in state, "%s: state.md missing '## Next action'" % mname)
    check("## Log" in state, "%s: state.md missing '## Log'" % mname)

    # --- 7. Ledger entries and mission-document claim tags -------------------
    ledger = read(ledger_p)
    check("## Sources" in ledger, "%s: ledger.md missing '## Sources'" % mname)
    ledger_ids = {int(s[1:]) for s in check_ledger_entries(ledger, "%s: ledger.md" % mname)}

    findings_dir = mission / "findings"
    findings_files = sorted(findings_dir.glob("*.md")) if findings_dir.is_dir() else []
    other_docs = [
        mission / n
        for n in ("brief.md", "verification.md", "contrarian-review.md")
        if (mission / n).is_file()
    ]

    proposed_by_file = {}
    for doc in findings_files + other_docs:
        proposed_by_file[doc] = {
            int(s[1:])
            for s in check_ledger_entries(
                read(doc), "%s/%s" % (mname, doc.relative_to(mission).as_posix())
            )
        }
    all_known = ledger_ids.union(*proposed_by_file.values()) if proposed_by_file else set(ledger_ids)

    for ff in findings_files:
        rel = "findings/%s" % ff.name
        label = "%s/%s" % (mname, rel)
        text = read(ff)
        check(
            rel in ws_blocks_by_file,
            "%s: findings file not declared in any mission.md workstream row" % label,
        )
        if rel in ws_blocks_by_file:
            lo, hi, ws_id = ws_blocks_by_file[rel]
            out_of_block = sorted(
                n for n in proposed_by_file[ff] if not (lo <= n <= hi)
            )
            check(
                not out_of_block,
                "%s: proposes sources outside %s block S%d-S%d: %s"
                % (label, ws_id, lo, hi, ["S%d" % n for n in out_of_block]),
            )
        check_tags(text, label)
        # Findings cite only the merged ledger or their own proposals
        check_citations(text, ledger_ids | proposed_by_file[ff], label)
        check_validate_by(text, label)

    for doc in other_docs:
        label = "%s/%s" % (mname, doc.name)
        text = read(doc)
        check_tags(text, label)
        check_citations(text, all_known, label)
        if doc.name == "brief.md":
            check_validate_by(text, label)
            check(
                re.search(r"^Status: (draft|final)\s*$", text, re.MULTILINE) is not None,
                "%s: brief must declare 'Status: draft' or 'Status: final'" % label,
            )

# --- Result -----------------------------------------------------------------
print("\n%d checks passed, %d failed." % (passes, len(failures)))
if failures:
    sys.exit(1)
print("ALL CHECKS PASSED")
