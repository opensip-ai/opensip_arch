#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make-ppbs-v9.py

Generate `preview-product-boundary-successor.v9.json` from the frozen
predecessor `docs/coop/artifacts/preview-product-boundary-successor.v8.json`
(sha256 f2e788e5..., recorded at COORD `## D-207`), per the owner-adopted
DR-117 programme (COORD `## D-293` Decision 5; DECISIONS-RECOMMENDED.md
Section B3; DECISION-PACKETS/B3-DR-117-class-A.md).

Run from the repository root.  Writes nothing under docs/.  Runs no
state-changing git command (only `git rev-parse` and `git status`).

    python3 make-ppbs-v9.py [OUTPUT] [--audit AUDIT.json] [--quiet]

OUTPUT may be a directory (the file is written inside it under its
canonical name) or a path ending in `.json`.  Default is the scratchpad
directory this script lives in.

Every factual value in the emitted artifact is measured at run time.
The script FAILS (non-zero exit, nothing written) if any measurement
disagrees with the programme's recorded expectation.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

# --------------------------------------------------------------------------
# Constants: paths and recorded expectations
# --------------------------------------------------------------------------

ARTIFACT_NAME = "preview-product-boundary-successor.v9"
OUT_BASENAME = "preview-product-boundary-successor.v9.json"
VERSION = 9

DEFAULT_OUT_DIR = os.path.dirname(os.path.abspath(__file__))

ART = "docs/coop/artifacts"
PRED_PATH = f"{ART}/preview-product-boundary-successor.v8.json"
PRED_SHA256 = "f2e788e51c347e1033073f0718e701d164affe51e7f667da9bcd49a08837144c"
PRED_RECORDING = "D-207"
PRED_REVIEW_CLAUDE = f"{ART}/preview-product-boundary-successor.v8.review-independent.claude2.json"
PRED_REVIEW_CODEX = f"{ART}/preview-product-boundary-successor.v8.review-independent.codex.json"

V7_PATH = f"{ART}/preview-product-boundary-successor.v7.json"
V7_RECORDING = "D-168"
V7_REVIEW_CLAUDE = f"{ART}/preview-product-boundary-successor.v7.review-independent.claude2.json"
V7_REVIEW_CODEX = f"{ART}/preview-product-boundary-successor.v7.review-independent.codex.json"
V6_PATH = f"{ART}/preview-product-boundary-successor.v6.json"
V6_REVIEW_CLAUDE = f"{ART}/preview-product-boundary-successor.v6.review-independent.claude2.json"
V5_PATH = f"{ART}/preview-product-boundary-successor.v5.json"
V5_RECORDING = "D-137"

CONTRACT_V8_PATH = f"{ART}/product-boundary-successor-contract.v8.json"
CONTRACT_V8_RECORDING = "D-116"
PREVIEW_V2_PATH = f"{ART}/product-boundary-preview.v2.json"

FILE08 = "docs/v2/architecture/08-decision-and-readiness-register.md"
FILE02 = "docs/v2/architecture/02-distribution-and-components.md"
COORD = "docs/coop/COORDINATOR-DECISIONS.md"
V1_SLICE = "docs/coop/v1-slice.md"

REQUIRED_NOW = 28
# The exact bytes of file 08's condition-4 snapshot that `requiredNowUnchanged`
# reproduces.  Asserted verbatim; the number in the artifact is not free.
REQUIRED_NOW_SNAPSHOT = "**28 of 28 required gates name a recorded identifier**"
DR117_EXPECTED_STATUS = "OPEN"
REGISTER_ROW = "DR-117"

# The twelve leftover-joins the predecessor cites at superseded versions.
# (lineage token as it appears in COORD headings, basedOn key stem,
#  version cited by the predecessor, that citation's recording,
#  version current now, that recording, routing kind)
JOINS = [
    ("g29",               "g29Join",              3,  "D-204",  4,  "D-254", "gate"),
    ("g30",               "g30Join",              3,  "D-205",  4,  "D-255", "gate"),
    ("g09",               "g09Join",             10,  "D-189", 12,  "D-288", "gate"),
    ("language-runtime",  "languageRuntimeJoin",  4,  "D-179",  7,  "D-274", "gate"),
    ("g16",               "g16Join",              3,  "D-192",  5,  "D-278", "gate"),
    ("g21",               "g21Join",              4,  "D-196", 13,  "D-292", "gate"),
    ("g23",               "g23Join",              4,  "D-198",  8,  "D-240", "gate"),
    ("permission",        "permissionJoin",       9,  "D-171", 12,  "D-283", "row"),
    ("distribution-core", "distributionCoreJoin", 7,  "D-173",  9,  "D-287", "row"),
    ("monorepo",          "monorepoJoin",         3,  "D-181",  4,  "D-277", "row"),
    ("language-quality",  "languageQualityJoin",  3,  "D-206",  5,  "D-273", "row"),
    ("doctor-actor",      "doctorActorJoin",     11,  "D-170", 12,  "D-285", "row"),
]
JOIN_COUNT_WORD = "twelve"

# Enforcement-evidence class routing, as the predecessor's own
# `existingGate` first clauses state it.  Derived from bytes at run time and
# asserted against this table.
EXPECTED_ROUTING = {
    "DR-G29": ["EE-1", "EE-2", "EE-3b", "EE-4", "EE-5a", "EE-5b", "EE-6a"],
    "DR-G30": ["EE-7a", "EE-7b", "EE-7d"],
    "DR-G09": ["EE-6b"],
    "DR-G14": ["EE-7c"],
    "DR-G16": ["EE-7e"],
    "DR-G21": ["EE-3a"],
    "DR-G23": ["EE-3a"],
}
# Which gate row each gate-routed lineage answers to, and the short gate label
# the record uses for its execution remainder.
GATE_OF_LINEAGE = {
    "g29": ("DR-G29", "G29"),
    "g30": ("DR-G30", "G30"),
    "g09": ("DR-G09", "G09"),
    "language-runtime": ("DR-G14", "G14"),
    "g16": ("DR-G16", "G16"),
    "g21": ("DR-G21", "G21"),
    "g23": ("DR-G23", "G23"),
}
# Non-gate-routed lineages carry an adjacent leftover; these sentences carry
# the predecessor's own statement of what stays where, lineage-qualified.
ROW_LEFTOVER_SENTENCE = {
    "permission": "EE-6b honesty tables remain specified at D-128 / DR-105.",
    "distribution-core": "EE-7a core-inventory leftover remains on DR-101.",
    "monorepo": "EE-7e independent-release leftover remains on DR-121 / G16.",
    "language-quality": "This preview-product-boundary-successor.v9 does not name G13 into required-now.",
    "doctor-actor": "Host-owned doctor probes remain D-002 / D-032 / DR-114.",
}

FOURTEEN_CLASS_IDS = [
    "EE-1", "EE-2", "EE-3a", "EE-3b", "EE-4", "EE-5a", "EE-5b",
    "EE-6a", "EE-6b", "EE-7a", "EE-7b", "EE-7c", "EE-7d", "EE-7e",
]

SPEAKER = "This preview-product-boundary-successor.v9"
SELF = "preview-product-boundary-successor.v9"
PRED_SELF = "preview-product-boundary-successor.v8"


class Fail(Exception):
    """A measurement disagreed with the record.  Nothing is written."""


def fail(msg: str) -> None:
    raise Fail(msg)


def need(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)


# --------------------------------------------------------------------------
# Measurement helpers
# --------------------------------------------------------------------------

def sha256_file(path: str) -> str:
    need(os.path.isfile(path), f"pinned input is missing: {path}")
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def stem(path: str) -> str:
    """The artifact name the record uses in prose: basename without `.json`."""
    return os.path.basename(path)[:-5] if path.endswith(".json") else os.path.basename(path)


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], capture_output=True, text=True)
    need(out.returncode == 0, f"git {' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout.strip()


def assert_repo_root() -> None:
    for marker in (COORD, FILE08, FILE02, V1_SLICE, PRED_PATH):
        need(os.path.isfile(marker), f"run this script from the repository root; missing {marker}")


def assert_docs_tree_clean() -> None:
    """Pins must resolve against committed bytes, so no tracked file under
    docs/ may be modified.  Untracked files do not move any pin."""
    status = git("status", "--porcelain", "--", "docs")
    dirty = [ln for ln in status.splitlines() if ln and not ln.startswith("??")]
    need(not dirty, "tracked files under docs/ are modified; pins would not resolve "
                    "against committed bytes:\n  " + "\n  ".join(dirty))


# --------------------------------------------------------------------------
# COORD parsing
# --------------------------------------------------------------------------

def coord_headings(coord_text: str):
    out = []
    for i, line in enumerate(coord_text.splitlines()):
        m = re.match(r"^## D-(\d+)\b", line)
        if m:
            out.append((i, int(m.group(1)), line))
    return out


def coord_entry_text(coord_text: str, decision: str) -> str:
    """Return the full text of `## D-NNN ...` up to the next `## D-` heading."""
    lines = coord_text.splitlines()
    heads = coord_headings(coord_text)
    want = int(decision.split("-")[1])
    for idx, (line_no, number, _line) in enumerate(heads):
        if number == want:
            end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
            return "\n".join(lines[line_no:end])
    fail(f"COORD has no heading {decision}")


def current_join_recording(coord_text: str, lineage: str):
    """The highest non-CONTESTED `## D-NNN - Record <lineage>[- ]leftover-join.vN`
    heading.  Returns (decision_number, version, heading_line)."""
    pat = re.compile(
        r"^## D-(\d+) — Record " + re.escape(lineage) + r"[- ]leftover-join\.v(\d+)\b(.*)$"
    )
    best = None
    for line in coord_text.splitlines():
        m = pat.match(line)
        if not m:
            continue
        if "CONTESTED" in m.group(3):
            continue
        number, version = int(m.group(1)), int(m.group(2))
        if best is None or number > best[0]:
            best = (number, version, line)
    need(best is not None, f"COORD names no leftover-join recording for lineage {lineage}")
    return best


# --------------------------------------------------------------------------
# file 08 parsing
# --------------------------------------------------------------------------

def file08_row_cells(file08_text: str, row_id: str):
    """Cells of the register row whose ID cell is exactly `row_id`."""
    header = None
    for line in file08_text.splitlines():
        if line.startswith("| ID |") and header is None:
            header = [c.strip() for c in line.split("|")]
        cells = [c.strip() for c in line.split("|")]
        if len(cells) > 2 and cells[1] == row_id:
            need(header is not None, "file 08 register table header was not found before the row")
            return header, cells
    fail(f"file 08 has no row whose ID cell is exactly {row_id}")


def file08_cell(header, cells, column_name: str) -> str:
    need(column_name in header, f"file 08 register table has no {column_name!r} column")
    return cells[header.index(column_name)]


def leading_label(cell: str) -> str:
    """The row's leading status label: the first token, stripped of the
    register's `**` / backtick emphasis."""
    token = cell.split()[0] if cell.split() else ""
    return token.strip("`*.,;")


# --------------------------------------------------------------------------
# Review-verdict extraction (recite the review files' actual shapes)
# --------------------------------------------------------------------------

def _count(value):
    if isinstance(value, list):
        return len(value)
    if isinstance(value, int):
        return value
    return None


def verdict_of(path: str) -> str:
    doc = read_json(path)
    inner = doc.get("decision") if isinstance(doc.get("decision"), dict) else {}
    verdict = doc.get("verdict") or inner.get("verdict")
    blockers = _count(doc.get("blockers"))
    if blockers is None:
        blockers = _count(doc.get("blockerCount"))
    if blockers is None:
        blockers = _count(inner.get("blockers"))
    should = _count(doc.get("shouldFix"))
    if should is None:
        should = _count(doc.get("shouldFixCount"))
    if should is None:
        should = _count(inner.get("shouldFix"))
    need(verdict is not None, f"review file states no verdict: {path}")
    need(blockers is not None and should is not None,
         f"review file states no blocker / should-fix counts: {path}")
    return f"{verdict} {blockers}/{should}"


def pin_review(path: str) -> dict:
    return {"path": path, "sha256": sha256_file(path), "verdict": verdict_of(path)}


# --------------------------------------------------------------------------
# House-rule audit
# --------------------------------------------------------------------------

# A version token is lineage-qualified when it is attached to an artifact
# identifier (`...-leftover-join.v4`, `...successor.v9`, `...contract.v8`), or
# when it is one of the record's fixed path forms.
DEICTIC_RE = re.compile(r"[Tt]his v[0-8]\b")
VERSION_RE = re.compile(r"\bv\d+\b")


def unqualified_version_tokens(text: str):
    out = []
    for m in VERSION_RE.finditer(text):
        start = m.start()
        before = text[:start]
        # attached to an identifier: `<word-char>.vN`
        if before.endswith(".") and len(before) >= 2 and (before[-2].isalnum() or before[-2] == "-"):
            continue
        # the record's fixed path forms
        if before.endswith("docs/"):
            continue
        if text[start:start + 8] == "v1-slice":
            continue
        out.append(text[max(0, start - 40):start + 8])
    return out


def audit_strings(node, path="$", findings=None):
    if findings is None:
        findings = []
    if isinstance(node, dict):
        for key, value in node.items():
            audit_one(str(key), f"{path}.{key} (key)", findings)
            audit_strings(value, f"{path}.{key}", findings)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            audit_strings(value, f"{path}[{i}]", findings)
    elif isinstance(node, str):
        audit_one(node, path, findings)
    return findings


def audit_one(text: str, where: str, findings) -> None:
    for m in DEICTIC_RE.finditer(text):
        findings.append(f"{where}: deictic predecessor self-reference {m.group(0)!r}")
    for ctx in unqualified_version_tokens(text):
        findings.append(f"{where}: bare version token near ...{ctx}...")
    if "{" in text or "}" in text:
        findings.append(f"{where}: unsubstituted brace token")


# --------------------------------------------------------------------------
# Change ledger (feeds audit.json)
# --------------------------------------------------------------------------

class Ledger:
    def __init__(self):
        self.rewritten = []
        self.carried = []
        self.added = []

    def rewrite(self, field: str, old, new, why: str):
        """`old is None` means the predecessor had no such field: that is an
        addition, not a rewrite, and is booked separately."""
        if old is None:
            self.added.append({"field": field, "v9": new, "why": why})
        else:
            self.rewritten.append({"field": field, "v8": old, "v9": new, "why": why})
        return new

    def new(self, field: str, value, why: str):
        self.added.append({"field": field, "v9": value, "why": why})
        return value

    def carry(self, field: str, value, why: str = "carried byte-identical from "
                                                  "preview-product-boundary-successor.v8"):
        self.carried.append({"field": field, "why": why})
        return value


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def derive_routing(classes):
    """Map gate row -> class ids, from each class's `existingGate` first clause."""
    routing = {}
    for cls in classes:
        first_clause = cls["existingGate"].split(";")[0].split(".")[0]
        for gate in re.findall(r"DR-G\d\d", first_clause):
            routing.setdefault(gate, []).append(cls["id"])
    return routing


def leftover_design_ids(join_doc):
    obligations = join_doc.get("obligations") or []
    return [o.get("id") for o in obligations if o.get("leftoverDesign") is True]


def build(out_path: str, ledger: Ledger, quiet: bool):
    assert_repo_root()
    assert_docs_tree_clean()

    today = datetime.date.today().isoformat()
    head = git("rev-parse", "HEAD")
    need(re.fullmatch(r"[0-9a-f]{40}", head) is not None, f"git HEAD is not a full sha: {head!r}")

    # ---- predecessor -----------------------------------------------------
    pred_sha = sha256_file(PRED_PATH)
    need(pred_sha == PRED_SHA256,
         f"the frozen predecessor moved: {PRED_PATH} is {pred_sha}, "
         f"D-207 records {PRED_SHA256}")
    pred = read_json(PRED_PATH)
    need(pred["artifact"] == PRED_SELF and pred["version"] == 8,
         "the predecessor file does not identify itself as "
         "preview-product-boundary-successor.v8")
    v7 = read_json(V7_PATH)

    # ---- COORD -----------------------------------------------------------
    coord_text = read_text(COORD)
    highest_coord = max(n for _i, n, _l in coord_headings(coord_text))
    d207 = coord_entry_text(coord_text, PRED_RECORDING)
    need(pred_sha in d207, "D-207 does not carry the predecessor's digest")
    need(coord_entry_text(coord_text, "D-293") is not None, "COORD has no D-293 entry")

    # ---- file 08 ---------------------------------------------------------
    file08_text = read_text(FILE08)
    file08_sha = sha256_file(FILE08)
    need(REQUIRED_NOW_SNAPSHOT in file08_text,
         f"file 08 no longer carries the condition-4 snapshot {REQUIRED_NOW_SNAPSHOT!r}; "
         f"requiredNowUnchanged {REQUIRED_NOW} is not reproducible")
    header, row = file08_row_cells(file08_text, REGISTER_ROW)
    status_cell = file08_cell(header, row, "Status")
    status_token = leading_label(status_cell)
    need(status_token == DR117_EXPECTED_STATUS,
         f"DR-117's live leading label is {status_token!r}, not {DR117_EXPECTED_STATUS!r}; "
         "this artifact's eligibility statements assume OPEN")
    acceptance_cell = file08_cell(header, row, "Required acceptance evidence")
    need(acceptance_cell == pred["registerRowQuoted"]["acceptanceEvidenceCellVerbatim"],
         "DR-117's acceptance-evidence cell has moved since "
         "preview-product-boundary-successor.v8 quoted it")

    # ---- the twelve joins ------------------------------------------------
    joins = []
    for lineage, key_stem, cited_v, cited_rec, exp_v, exp_rec, kind in JOINS:
        number, version, heading = current_join_recording(coord_text, lineage)
        recording = f"D-{number}"
        need(version == exp_v and recording == exp_rec,
             f"{lineage} leftover-join currency changed: COORD's highest non-CONTESTED "
             f"recording is {recording} at version {version}; the adopted programme "
             f"names {exp_rec} at version {exp_v}. Heading: {heading}")
        path = f"{ART}/{lineage}-leftover-join.v{version}.json"
        sha = sha256_file(path)
        entry = coord_entry_text(coord_text, recording)
        need(sha in entry, f"{recording} does not carry the digest of {path}")

        claude = pin_review(f"{ART}/{lineage}-leftover-join.v{version}"
                            ".review-independent.claude2.json")
        codex = pin_review(f"{ART}/{lineage}-leftover-join.v{version}"
                           ".review-independent.codex.json")
        for reviewer, pinned in (("Claude", claude), ("Codex", codex)):
            need(pinned["sha256"] in entry,
                 f"{recording} does not carry the {reviewer} Stage A digest for {path}")
            need(pinned["verdict"].startswith("ACCEPT "),
                 f"{reviewer} Stage A verdict for {path} is {pinned['verdict']!r}, not an ACCEPT")

        # what the predecessor pinned for this lineage
        cited_path = f"{ART}/{lineage}-leftover-join.v{cited_v}.json"
        cited_entry = None
        for value in pred["basedOn"].values():
            if isinstance(value, dict) and value.get("path") == cited_path:
                cited_entry = value
                break
        need(cited_entry is not None,
             f"preview-product-boundary-successor.v8 does not pin {cited_path}")
        need(cited_entry.get("recording") == cited_rec,
             f"preview-product-boundary-successor.v8 records {cited_path} at "
             f"{cited_entry.get('recording')}, the programme names {cited_rec}")
        cited_sha_live = sha256_file(cited_path)
        need(cited_sha_live == cited_entry["sha256"],
             f"the superseded join {cited_path} has moved since "
             f"preview-product-boundary-successor.v8 pinned it")

        join_doc = read_json(path)
        need(join_doc.get("status") == "CANDIDATE-NOT-APPLIED" and join_doc.get("binds") == "NOTHING",
             f"{path} is no longer CANDIDATE-NOT-APPLIED / binds NOTHING")

        joins.append({
            "lineage": lineage,
            "keyStem": key_stem,
            "kind": kind,
            "registerRow": join_doc.get("registerRow"),
            "path": path,
            "sha256": sha,
            "recording": recording,
            "version": version,
            "reviews": {"claude": claude, "codex": codex},
            "leftoverDesignTrue": leftover_design_ids(join_doc),
            "citedPath": cited_path,
            "citedSha256": cited_sha_live,
            "citedRecording": cited_rec,
            "citedVersion": cited_v,
            "citedRole": cited_entry.get("role"),
        })
    need(len(joins) == 12, f"expected twelve current leftover-joins, measured {len(joins)}")

    # ---- carried blocks --------------------------------------------------
    classes = ledger.carry("enforcementEvidence.classes",
                           pred["enforcementEvidence"]["classes"],
                           "the fourteen EE classes are carried byte-for-byte; equality asserted")
    need([c["id"] for c in classes] == FOURTEEN_CLASS_IDS,
         "the predecessor's enforcement-evidence classes are not the fourteen recorded ids")
    need(json.dumps(classes, sort_keys=True, ensure_ascii=False)
         == json.dumps(pred["enforcementEvidence"]["classes"], sort_keys=True, ensure_ascii=False),
         "EE classes are not byte-identical to the predecessor's")

    dispositions = ledger.carry("sevenItems.dispositions",
                                pred["sevenItems"]["dispositions"],
                                "the seven dispositions are carried byte-for-byte; equality asserted")
    need(len(dispositions) == 7 and [d["item"] for d in dispositions] == [1, 2, 3, 4, 5, 6, 7],
         "the predecessor's dispositions are not the seven recorded items")
    need(json.dumps(dispositions, sort_keys=True, ensure_ascii=False)
         == json.dumps(pred["sevenItems"]["dispositions"], sort_keys=True, ensure_ascii=False),
         "the seven dispositions are not byte-identical to the predecessor's")

    routing = derive_routing(classes)
    for gate, expected in EXPECTED_ROUTING.items():
        need(routing.get(gate) == expected,
             f"EE routing for {gate} measures {routing.get(gate)}, the record names {expected}")

    # ---- basedOn ---------------------------------------------------------
    based_on = {}

    based_on["predecessorV8"] = {
        "path": PRED_PATH,
        "sha256": pred_sha,
        "recording": PRED_RECORDING,
        "reviews": {
            "claude": pin_review(PRED_REVIEW_CLAUDE),
            "codex": pin_review(PRED_REVIEW_CODEX),
        },
        "role": ledger.rewrite(
            "basedOn.predecessorV8.role", None,
            f"Immediate predecessor. Unmoved. Recorded at {PRED_RECORDING} as the DR-117 "
            f"leftover remasurement after D-206, measured at HEAD {pred['head']} / "
            f"required-now {pred['requiredNowUnchanged']} / file 08 "
            f"{pred['file08Pin']['sha256']}. Dual ACCEPT 0/0 at Stage A. Every one of the "
            f"{JOIN_COUNT_WORD} leftover-joins it cited as current is superseded at this "
            f"dispatch, which is the whole reason {SELF} exists; nothing else in it is "
            f"disturbed. Its fourteen enforcement-evidence classes and its seven "
            f"dispositions are carried into {SELF} byte-identically. "
            f"preview-product-boundary-successor and every leftover-join lineage cited "
            f"here are different lineages; their version numbers are unrelated.",
            "new object: the predecessor of preview-product-boundary-successor.v9 is "
            "preview-product-boundary-successor.v8, which the predecessor could not state "
            "about itself"),
    }

    based_on["predecessorV7"] = {
        "path": V7_PATH,
        "sha256": sha256_file(V7_PATH),
        "recording": V7_RECORDING,
        "reviews": {
            "claude": pin_review(V7_REVIEW_CLAUDE),
            "codex": pin_review(V7_REVIEW_CODEX),
        },
        "role": ledger.rewrite(
            "basedOn.predecessorV7.role",
            pred["basedOn"]["predecessorV7"]["role"],
            f"Historical measurement. Unmoved. Recorded at {V7_RECORDING}, measured at HEAD "
            f"{v7['head']} / required-now {v7['requiredNowUnchanged']} / file 08 "
            f"{v7['registerRowQuoted']['sourceSha256']}. Dual ACCEPT 0/0 as a historical "
            f"measurement. {PRED_RECORDING} recorded that it stays frozen and is not to be "
            f"recorded as current. It is no longer this lineage's predecessor: "
            f"{PRED_SELF} ({PRED_RECORDING}) is. Not this artifact's version number.",
            "the predecessor called preview-product-boundary-successor.v7 its own "
            "predecessor; at v9 it is one step further back, and its 'not recordable "
            "because file 08 moved and required-now is 28' sentence is spent"),
    }

    based_on["predecessorV6"] = {
        "path": V6_PATH,
        "sha256": sha256_file(V6_PATH),
        "reviews": {"claude": pin_review(V6_REVIEW_CLAUDE)},
        "role": ledger.rewrite(
            "basedOn.predecessorV6.role", None,
            "Historical. Claude Stage A REJECT; Codex not reviewed, and no Codex verdict "
            "file for it exists on disk. Never recorded. Not this artifact's version number.",
            "new object: preview-product-boundary-successor.v8 pinned this predecessor "
            "through the unnamed keys basedOn.path, basedOn.sha256 and basedOn.claudeReview; "
            "v9 pins it as a named object so all predecessors and all "
            f"{JOIN_COUNT_WORD} current joins pin uniformly (CLAUDE-PPBS-V8-ADV-1)"),
    }
    need(based_on["predecessorV6"]["sha256"] == pred["basedOn"]["sha256"],
         "the predecessor's flattened v6 pin does not match the file on disk")
    need(based_on["predecessorV6"]["reviews"]["claude"]["sha256"]
         == pred["basedOn"]["claudeReview"]["sha256"],
         "the predecessor's flattened v6 review pin does not match the file on disk")
    need(not os.path.exists(V6_PATH.replace(".json", ".review-independent.codex.json")),
         "a Codex verdict for preview-product-boundary-successor.v6 now exists; the "
         "'Codex not reviewed' sentence would be contradicted by bytes")

    based_on["predecessorV5"] = {
        "path": V5_PATH,
        "sha256": sha256_file(V5_PATH),
        "recording": V5_RECORDING,
        "reviews": {
            "claude": pin_review(f"{ART}/preview-product-boundary-successor.v5"
                                 ".review-independent.claude2.json"),
            "codex": pin_review(f"{ART}/preview-product-boundary-successor.v5"
                                ".review-independent.codex.json"),
        },
        "role": ledger.rewrite(
            "basedOn.predecessorV5.role", None,
            f"Historical. Recorded at {V5_RECORDING} as DR-117's preview-scoped successor "
            f"candidate, authorized by D-132. The seven dispositions, p1p2g3Mapping and the "
            f"lineage roles entered this lineage there. Not this artifact's version number.",
            "new role text: preview-product-boundary-successor.v8 pinned "
            "preview-product-boundary-successor.v5 with path, sha256 and recording only "
            "and stated no role"),
    }
    need(based_on["predecessorV5"]["sha256"] == pred["basedOn"]["predecessorV5"]["sha256"],
         "preview-product-boundary-successor.v5 has moved since the predecessor pinned it")

    based_on["predecessorPinningShape"] = ledger.new(
        "basedOn.predecessorPinningShape",
        f"{SPEAKER} pins every predecessor and every one of the {JOIN_COUNT_WORD} current "
        f"leftover-joins as a named object carrying path, sha256, the recording where one "
        f"exists, and each Stage A verdict that exists on disk with its path, digest and "
        f"verdict read from the verdict file itself. {PRED_SELF} pinned "
        f"preview-product-boundary-successor.v6 through the unnamed keys basedOn.path, "
        f"basedOn.sha256 and basedOn.claudeReview, and pinned "
        f"doctor-actor-leftover-join.v11 with no verdict block at all; both are now named "
        f"objects with the same digests, which closes CLAUDE-PPBS-V8-ADV-1.",
        "new field: the predecessor stated no pinning discipline, and the uniform shape is "
        "what CLAUDE-PPBS-V8-ADV-1 asked for")

    for join in joins:
        key = f"{join['keyStem']}V{join['version']}"
        if join["kind"] == "gate":
            gate_row, gate_short = GATE_OF_LINEAGE[join["lineage"]]
            class_ids = routing[gate_row]
            if len(class_ids) == 1:
                class_phrase = class_ids[0]
            else:
                class_phrase = ", ".join(class_ids[:-1]) + f", and {class_ids[-1]}"
            if join["lineage"] == "g21":
                remainder = f"Remainder of {class_phrase} shares {gate_short} execution with G23."
            elif join["lineage"] == "g23":
                remainder = f"Remainder of {class_phrase} shares {gate_short} execution with G21."
            else:
                remainder = f"Remainder of {class_phrase} is {gate_short} execution."
        else:
            remainder = ROW_LEFTOVER_SENTENCE[join["lineage"]]

        if join["leftoverDesignTrue"]:
            flags = ("Obligations flagged leftoverDesign true on "
                     f"{stem(join['path'])} at this dispatch: ["
                     + ", ".join(join["leftoverDesignTrue"]) + "]. "
                     f"{SPEAKER} does not steal that leftover-design.")
        else:
            flags = (f"No obligation on {stem(join['path'])} is flagged "
                     f"leftoverDesign true at this dispatch. {SPEAKER} therefore carries no "
                     f"leftover-design claim for this lineage forward.")

        role = (
            f"Current {join['registerRow']} leftover-join at {SELF}'s dispatch, measured as "
            f"the version named by the highest non-CONTESTED COORD recording for this "
            f"lineage ({join['recording']}). {PRED_SELF} cited "
            f"{stem(join['citedPath'])} ({join['citedRecording']}); that "
            f"citation is superseded by {join['recording']}. {flags} {remainder} "
            f"{join['lineage']}-leftover-join and preview-product-boundary-successor are "
            f"different lineages; their version numbers are unrelated."
        )
        based_on[key] = {
            "path": join["path"],
            "sha256": join["sha256"],
            "recording": join["recording"],
            "reviews": join["reviews"],
            "role": ledger.rewrite(
                f"basedOn.{key}.role", join["citedRole"], role,
                f"re-cited: {join['lineage']} leftover-join moved from version "
                f"{join['citedVersion']} ({join['citedRecording']}) to version "
                f"{join['version']} ({join['recording']}); the leftoverDesign list is "
                f"re-measured from the current join's bytes"),
        }

    based_on["relation"] = ledger.rewrite(
        "basedOn.relation", pred["basedOn"]["relation"],
        f"Re-cite the {JOIN_COUNT_WORD} current leftover-joins at live HEAD, replacing the "
        f"{JOIN_COUNT_WORD} superseded citations {PRED_SELF} ({PRED_RECORDING}) carried. "
        f"The fourteen enforcement-evidence classes and the seven dispositions are carried "
        f"from {PRED_SELF} byte-identically, and equality is asserted before this file is "
        f"written. leftover-design of unnamed EE classes remains closed. Cited gate and row "
        f"leftovers are not stolen. p1p2g3Mapping is carried byte-identically. "
        f"{SPEAKER} existing is not SATISFIED-GRADE and does not mark SATISFIED.",
        "the predecessor's relation described a remasurement of "
        "preview-product-boundary-successor.v7 after D-167 / D-169 / D-206; v9's relation "
        "is its own")

    # ---- lineage ---------------------------------------------------------
    contract_sha = sha256_file(CONTRACT_V8_PATH)
    lineage = {
        "productBoundarySuccessorContractV8": {
            "path": CONTRACT_V8_PATH,
            "sha256": contract_sha,
            "recording": CONTRACT_V8_RECORDING,
            "role": ledger.rewrite(
                "lineage.productBoundarySuccessorV8.role -> "
                "lineage.productBoundarySuccessorContractV8.role",
                pred["lineage"]["productBoundarySuccessorV8"]["role"],
                f"Remains DR-117's leftover T2-02 candidate for general succession; D-137 "
                f"records that product-boundary-successor-contract.v8 remains the "
                f"{CONTRACT_V8_RECORDING} leftover T2-02 candidate. {SPEAKER} does not "
                f"replace, apply, or succeed product-boundary-successor-contract.v8.",
                "the predecessor's sentence ended 'does not replace, apply, or succeed v8', "
                "a bare version token that names neither lineage; the key is renamed for the "
                "same reason"),
            "keyRenamedFrom": ledger.new(
                "lineage.productBoundarySuccessorContractV8.keyRenamedFrom",
                "lineage.productBoundarySuccessorV8 in "
                "preview-product-boundary-successor.v8. Two artifacts in the record are "
                "numbered eight - product-boundary-successor-contract.v8 (D-116) and "
                "preview-product-boundary-successor.v8 (D-207) - and a key naming neither "
                "lineage invited conflation. The digest and the recording are unchanged.",
                "new field: the rename is recorded in the artifact itself so a reviewer "
                "diffing against the predecessor sees why the key moved"),
        },
        "productBoundaryPreviewV2": ledger.carry(
            "lineage.productBoundaryPreviewV2", pred["lineage"]["productBoundaryPreviewV2"]),
        "relation": ledger.rewrite(
            "lineage.relation", pred["lineage"]["relation"],
            "Preview-scoped complement authorized by D-132. Not silent succession from "
            "product-boundary-preview.v2. product-boundary-successor-contract.v8 stays "
            "DR-117's leftover T2-02 candidate. File 12 has no authority.",
            "the predecessor wrote 'v8 stays leftover T2-02' and 'preview.v2'; both are "
            "qualified by lineage here"),
        "previewReadAs": ledger.carry("lineage.previewReadAs", pred["lineage"]["previewReadAs"]),
        "contractRelationship": ledger.new(
            "lineage.contractRelationship",
            f"product-boundary-successor-contract.v8 ({CONTRACT_V8_RECORDING}, the D-137 "
            f"'leftover T2-02 candidate') and {SELF} are distinct lineages; their version "
            f"numbers are unrelated. {SPEAKER} is the DR-117 preview-scoped successor "
            f"candidate authorized by D-132 / file 12 section 5, and is the candidate limb "
            f"of the DR-117 programme the owner adopted at D-293 Decision 5. "
            f"product-boundary-successor-contract.v8 remains the {CONTRACT_V8_RECORDING} "
            f"recording and DR-117's leftover T2-02 candidate for general succession. "
            f"Neither of the two is applied: DR-117's live leading label in file 08 is "
            f"{status_token}, product-boundary-successor-contract.v8 stands as the "
            f"{CONTRACT_V8_RECORDING} candidate recording, and {SELF} is "
            f"CANDIDATE-NOT-APPLIED and binds NOTHING. {SPEAKER} does not replace, apply, "
            f"or succeed product-boundary-successor-contract.v8 and does not make it "
            f"historical. Which of the two a later D-056 Class A opening names is not "
            f"decided in the record and is not decided here; that is for the "
            f"owner-controlled entry D-293 Decision 5 reserves.",
            "new field: D-293 Decision 5 requires this successor to state its relationship "
            "to product-boundary-successor-contract.v8 in terms"),
    }
    need(contract_sha == pred["lineage"]["productBoundarySuccessorV8"]["sha256"],
         "product-boundary-successor-contract.v8 has moved since the predecessor pinned it")

    # ---- predecessor standing (history object) ---------------------------
    # Recite the two Stage A verdicts on the predecessor in their own shapes.
    claude_v8 = read_json(PRED_REVIEW_CLAUDE)
    codex_v8 = read_json(PRED_REVIEW_CODEX)
    claude_gate1 = "Does not claim Gate 1 Class A holds."
    need(isinstance(claude_v8.get("whatThisVerdictDoesNotDo"), list)
         and claude_gate1 in claude_v8["whatThisVerdictDoesNotDo"],
         "the Claude Stage A verdict on the predecessor no longer carries "
         f"{claude_gate1!r} in its whatThisVerdictDoesNotDo array")
    codex_elig = codex_v8.get("authorityBoundaryAudit", {}).get("eligibility", {})
    codex_gate1_authority = "D-137 express reservation remains controlling"
    need(codex_elig.get("gate1ClassA") is False
         and codex_elig.get("gate1Authority") == codex_gate1_authority,
         "the Codex Stage A verdict on the predecessor no longer records "
         "authorityBoundaryAudit.eligibility.gate1ClassA false with "
         f"gate1Authority {codex_gate1_authority!r}")

    predecessor_standing = ledger.new(
        "predecessorStanding",
        {
        "currentBeforeThisFileIsRecorded": (
            f"{PRED_SELF} ({PRED_RECORDING}) is the current recorded DR-117 leftover "
            f"remasurement. {SPEAKER} is CANDIDATE-NOT-APPLIED and records nothing; until a "
            f"reviewed coordinator act records {SELF}, {PRED_SELF} stays current."),
        "effectOfRecordingThisFile": (
            f"Once {SELF} is recorded, {PRED_SELF} becomes a historical measurement as of "
            f"HEAD {pred['head']} / required-now {pred['requiredNowUnchanged']} / file 08 "
            f"{pred['file08Pin']['sha256']}, and is no longer the current DR-117 leftover "
            f"remasurement. {PRED_SELF} stays frozen; it is not to be recorded as current "
            f"after that act. Nothing in {SELF} unwrites {PRED_RECORDING}."),
        "predecessorV7Standing": (
            f"preview-product-boundary-successor.v7 ({V7_RECORDING}) remains a historical "
            f"measurement as of HEAD {v7['head']} / required-now "
            f"{v7['requiredNowUnchanged']}, which is what {PRED_RECORDING} recorded. It "
            f"stays frozen; do not record it as current."),
        "earlierStanding": (
            f"preview-product-boundary-successor.v5 ({V5_RECORDING}) is historical. "
            f"preview-product-boundary-successor.v6 was rejected at Stage A by Claude and "
            f"never recorded."),
        "versionNumbers": (
            f"preview-product-boundary-successor, product-boundary-successor-contract, and "
            f"every leftover-join lineage cited in basedOn are different lineages; their "
            f"version numbers are unrelated."),
        "stageAGate1Standing": (
            f"Neither Stage A verdict on {PRED_SELF} grants Gate 1's application-grade / "
            f"no-express-reservation limb, read in the verdict files' own shapes. "
            f"{stem(PRED_REVIEW_CLAUDE)} carries the sentence \"{claude_gate1}\" as a "
            f"member of its whatThisVerdictDoesNotDo array. {stem(PRED_REVIEW_CODEX)} "
            f"carries an authorityBoundaryAudit.eligibility object whose gate1ClassA is "
            f"false and whose gate1Authority is \"{codex_gate1_authority}\". Both shapes "
            f"were read from those files before {SELF} was written. D-293 Decision 5 puts a "
            f"fresh application-grade dual review bound to this successor's final digest "
            f"before any opening entry."),
        },
        "new object: records that preview-product-boundary-successor.v8 (D-207) becomes "
        "historical once this successor is recorded, that "
        "preview-product-boundary-successor.v7 (D-168) remains historical, and what the "
        "two Stage A verdicts on the predecessor say about Gate 1")

    # ---- join currency audit --------------------------------------------
    join_currency_audit = ledger.new(
        "joinCurrencyAudit",
        {
        "count": len(joins),
        "countInWords": JOIN_COUNT_WORD,
        "method": (
            "For each lineage the current version is the one named by the highest "
            "non-CONTESTED COORD heading of the form "
            "'## D-NNN - Record <lineage>[- ]leftover-join.vN as ...'. The named file's "
            "sha256 and both Stage A verdict digests must appear in that entry's own text; "
            "all three were verified before this file was written."),
        "standing": (
            f"All {JOIN_COUNT_WORD} leftover-join citations {PRED_SELF} ({PRED_RECORDING}) "
            f"carried as current are superseded. {SPEAKER} re-cites all {JOIN_COUNT_WORD} at "
            f"the versions measured above. That re-citation is the whole of this "
            f"successor's substantive change; the fourteen enforcement-evidence classes and "
            f"the seven dispositions are carried byte-identically."),
        "joins": [
            {
                "lineage": join["lineage"],
                "registerRow": join["registerRow"],
                "citedByPredecessor": {
                    "path": join["citedPath"],
                    "sha256": join["citedSha256"],
                    "recording": join["citedRecording"],
                },
                "currentAtThisDispatch": {
                    "path": join["path"],
                    "sha256": join["sha256"],
                    "recording": join["recording"],
                },
                "supersededBy": join["recording"],
                "leftoverDesignTrue": join["leftoverDesignTrue"],
            }
            for join in joins
        ],
        },
        "new object: the twelve-join re-citation table (cited by the predecessor -> "
        "current now) that is this successor's reason for existing")

    # ---- enforcementEvidence --------------------------------------------
    v1_slice_pin = dict(pred["enforcementEvidence"]["v1SlicePin"])
    v1_slice_pin["sha256"] = sha256_file(V1_SLICE)
    need(v1_slice_pin["sha256"] == pred["enforcementEvidence"]["v1SlicePin"]["sha256"],
         "the v1-slice has moved since the predecessor pinned it")
    ledger.carry("enforcementEvidence.v1SlicePin",
                 v1_slice_pin,
                 "re-measured at run time and equal to the predecessor's pin")

    enforcement_evidence = {
        "status": ledger.carry("enforcementEvidence.status",
                               pred["enforcementEvidence"]["status"]),
        "ownerOfUnownedPreviewClasses": ledger.rewrite(
            "enforcementEvidence.ownerOfUnownedPreviewClasses",
            pred["enforcementEvidence"]["ownerOfUnownedPreviewClasses"],
            "No preview EE class remains unowned. D-157 / D-158 / D-159 named every class "
            "that preview-product-boundary-successor.v5 marked owner=this-candidate. "
            f"{SPEAKER} remasures that naming against the {JOIN_COUNT_WORD} current "
            "leftover-joins. It does not execute the classes and does not add a DR-G* row.",
            "the predecessor wrote 'every class that v5 marked', a bare version token, and "
            "its 'This successor remasures that naming' sentence did not say against what"),
        "cellAnswer": ledger.carry("enforcementEvidence.cellAnswer",
                                   pred["enforcementEvidence"]["cellAnswer"]),
        "v1SlicePin": v1_slice_pin,
        "classes": classes,
    }

    # ---- doesNot ---------------------------------------------------------
    pred_does_not = list(pred["doesNot"])
    does_not = []
    for item in pred_does_not:
        if item == ("This file existing is not a SATISFIED-GRADE cycle and does not mark "
                    "SATISFIED."):
            does_not.append(ledger.rewrite(
                "doesNot[2]", item,
                f"{SPEAKER} existing is not a SATISFIED-GRADE cycle and does not mark "
                f"SATISFIED.",
                "the speaker sentence must name v9, not 'this file'"))
        elif item == "Does not record frozen v7 as a current remasurement.":
            does_not.append(ledger.rewrite(
                "doesNot[13]", item,
                "Does not record frozen preview-product-boundary-successor.v7 as a current "
                "leftover remasurement, and does not record frozen "
                "preview-product-boundary-successor.v8 as a current one either once "
                f"{SELF} is recorded.",
                "'frozen v7' is a bare version token, and at v9 the same holds of "
                "preview-product-boundary-successor.v8"))
        elif item.startswith("Does not steal leftover-design of OBL-FX-AUTHORING"):
            union = []
            for join in joins:
                for oid in join["leftoverDesignTrue"]:
                    if oid not in union:
                        union.append(oid)
            does_not.append(ledger.rewrite(
                "doesNot[16]", item,
                "Does not steal leftover-design of any obligation flagged leftoverDesign "
                f"true on the {JOIN_COUNT_WORD} current leftover-joins cited in basedOn: ["
                + ", ".join(union) + "].",
                "the predecessor named OBL-G23-FX-AUTHORING among the stolen-nothing list; "
                "g23-leftover-join.v8 (D-240) flags no obligation leftoverDesign true, so "
                "the old sentence would be contradicted by bytes. The list is measured."))
        elif item.startswith("Does not unwrite D-137"):
            does_not.append(ledger.rewrite(
                "doesNot[19]", item,
                "Does not unwrite D-137, D-157, D-158, D-159, D-167, D-168, D-169, or any "
                f"entry of {COORD} from D-170 through D-{highest_coord}.",
                f"the predecessor's list stopped at D-206; COORD's highest heading is now "
                f"D-{highest_coord}"))
        else:
            ledger.carry(f"doesNot[{pred_does_not.index(item)}]", item)
            does_not.append(item)

    does_not.extend(ledger.new(
        "doesNot[20..27]",
        [
        "Does not lift D-137's express reservation; D-207 records that the venue for any "
        "later lift is a reviewed coordinator act, not an artifact, and D-293 Decision 5 "
        "reserves the opening entry to the owner.",
        "Does not apply, replace, or succeed product-boundary-successor-contract.v8 "
        "(D-116), and does not make product-boundary-successor-contract.v8 historical.",
        "Does not decide which of product-boundary-successor-contract.v8 and "
        f"{SELF} a later D-056 Class A opening names.",
        f"Does not edit {FILE08} and does not edit {COORD}.",
        "Does not author G29 or G30 fixture bytes; D-293 Decision 5 places that authoring "
        "after the owner-controlled opening entry.",
        f"Does not perform the fresh application-grade dual review D-293 Decision 5 "
        f"requires; {SELF} is the subject of that review, not its verdict.",
        f"Does not record itself. Recording {SELF} remains a later D-000 act.",
        "Does not SATISFY DR-131 or DR-133.",
        ],
        "eight v9-specific disclaimers: D-137's reservation, the "
        "product-boundary-successor-contract.v8 relationship, the fixture-authoring and "
        "review order D-293 Decision 5 sets, and that this successor records nothing"))

    # ---- findingDisposition ---------------------------------------------
    finding_disposition = ledger.new(
        "findingDisposition CLAUDE-PPBS-V8-ADV-1 / CLAUDE-PPBS-V8-ADV-2",
        [
        {
            "id": "CLAUDE-PPBS-V8-ADV-1",
            "severity": "ADVISORY",
            "disposition": (
                f"ACCEPTED as honesty. {SPEAKER} pins both Stage A verdict paths, digests "
                f"and verdicts for every one of the {JOIN_COUNT_WORD} current leftover-joins "
                f"in basedOn, doctor-actor-leftover-join.v12 (D-285) included, and pins "
                f"preview-product-boundary-successor.v6 as a named object rather than "
                f"through unnamed keys. The pinning asymmetry the advisory named is closed."),
            "landedAt": ["basedOn.doctorActorJoinV12", "basedOn.predecessorV6",
                         "basedOn.predecessorPinningShape"],
        },
        {
            "id": "CLAUDE-PPBS-V8-ADV-2",
            "severity": "ADVISORY",
            "disposition": (
                f"ACCEPTED as honesty. {SPEAKER} regenerates remeasurementClause from "
                f"recordedInputs rather than maintaining an anchor enumeration by addition, "
                f"and says in terms that the trigger reaches every pinned row."),
            "landedAt": ["remeasurementClause", "recordedInputs"],
        },
        ],
        "the two advisories the Claude Stage A verdict on the predecessor raised; both are "
        "landed in this successor")
    for entry in pred["findingDisposition"]:
        entry = json.loads(json.dumps(entry))
        eid = entry.get("id")
        if eid == "CLAUDE-PPBS-V7-ADV-2":
            entry["disposition"] = ledger.rewrite(
                "findingDisposition CLAUDE-PPBS-V7-ADV-2.disposition",
                entry["disposition"],
                "ACCEPTED as honesty. At "
                f"{SELF} the clause no longer enumerates an anchor subset: it is generated "
                "from recordedInputs and its trigger is stated to reach every pinned row.",
                "the predecessor's text enumerated 'v7, both v7 Stage A verdicts, ...' with "
                "bare version tokens, and the enumeration form is the thing "
                "CLAUDE-PPBS-V8-ADV-2 asked to replace")
        elif isinstance(entry.get("disposition"), str) and re.search(
                r"ACCEPTED at v\d+ \(prior\)", entry["disposition"]):
            old = entry["disposition"]
            entry["disposition"] = ledger.rewrite(
                f"findingDisposition {eid}.disposition", old,
                re.sub(r"\bv(\d+)\b", r"preview-product-boundary-successor.v\1", old),
                "bare version token; the lineage is named")
        elif eid == "CLAUDE-PPBS-V3-ADV-1":
            entry["venueLimb"] = ledger.rewrite(
                "findingDisposition CLAUDE-PPBS-V3-ADV-1.venueLimb",
                entry["venueLimb"],
                f"Stands. {SPEAKER} is right to refuse Class A in terms. The venue for "
                f"lifting D-137's reservation is a reviewed coordinator decision, not "
                f"{SELF}, and D-293 Decision 5 reserves that entry to the owner.",
                "the speaker sentence must name v9, and D-293 now names the venue")
        else:
            ledger.carry(f"findingDisposition {eid}", entry)
        finding_disposition.append(entry)

    # ---- leftoverDesignOpenStanding --------------------------------------
    join_clauses = []
    for join in joins:
        base = stem(join["path"])
        if join["leftoverDesignTrue"]:
            join_clauses.append(
                f"current {join['registerRow']} leftover-join is {base} "
                f"({join['recording']}), leftoverDesign true on ["
                + ", ".join(join["leftoverDesignTrue"]) + "]")
        else:
            join_clauses.append(
                f"current {join['registerRow']} leftover-join is {base} "
                f"({join['recording']}), with no obligation flagged leftoverDesign true")
    g23 = [j for j in joins if j["lineage"] == "g23"][0]
    standing_parts = [
        f"The live DR-117 leading label in file 08 is {status_token}.",
        "leftover-design of unnamed EE classes remains closed (D-159).",
        "Remainder is named-gate execution.",
        f"Measured at {SELF}'s dispatch, the current leftover-joins are: "
        + "; ".join(join_clauses) + ".",
        f"{SPEAKER} does not steal those leftovers.",
    ]
    if not g23["leftoverDesignTrue"]:
        standing_parts.append(
            f"{PRED_SELF} recorded leftoverDesign [OBL-G23-FX-AUTHORING] on "
            f"{stem(g23['citedPath'])} ({g23['citedRecording']}); {stem(g23['path'])} flags "
            f"no obligation leftoverDesign true, so {SELF} does not carry that claim "
            f"forward.")
    standing_parts.append("leftover-design of unnamed EE classes is not reopened.")
    standing_parts.append("G13 remains reserved, not named.")
    standing_parts.append("DR-117 is not SATISFIED.")
    leftover_design_open_standing = ledger.rewrite(
        "leftoverDesignOpenStanding", pred["leftoverDesignOpenStanding"],
        " ".join(standing_parts),
        "regenerated from the current joins' bytes; the predecessor's twelve 'Current X "
        "leftover-join is ...' sentences all named superseded versions, and its g23 "
        "leftoverDesign claim is no longer supported by the current join")

    # ---- authorityClaim / purpose (written for v9, not patched) ----------
    authority_claim = ledger.rewrite(
        "authorityClaim", pred["authorityClaim"],
        f"{SPEAKER} PROPOSES the DR-117 preview-scoped successor candidate authorized by "
        f"D-132 / file 12 section 5, and is the candidate limb of the DR-117 programme the "
        f"owner adopted at D-293 Decision 5. Its own history is this: "
        f"preview-product-boundary-successor.v5 was recorded at {V5_RECORDING}, "
        f"preview-product-boundary-successor.v6 was rejected at Stage A and never recorded, "
        f"preview-product-boundary-successor.v7 was recorded at {V7_RECORDING}, and "
        f"{PRED_SELF} was recorded at {PRED_RECORDING}; every one of the "
        f"{JOIN_COUNT_WORD} leftover-joins {PRED_SELF} cited as current has since been "
        f"superseded by a later recording, and {SELF} exists to re-cite those "
        f"{JOIN_COUNT_WORD} at the versions measured live at its own dispatch. "
        f"{SPEAKER} carries the fourteen enforcement-evidence classes and the seven "
        f"dispositions of {PRED_SELF} byte-identically, and that equality is asserted "
        f"before this file is written. leftover-design of unnamed EE classes remains closed "
        f"(D-157 / D-158 / D-159). {SPEAKER} and product-boundary-successor-contract.v8 "
        f"(D-116, the D-137 leftover T2-02 candidate) are distinct lineages: {SELF} does "
        f"not replace, apply, or succeed product-boundary-successor-contract.v8, which "
        f"remains the D-116 recording, and neither of the two is applied. {SPEAKER} does "
        f"not steal OBL-G29-FX-AUTHORING or OBL-G30-FX-AUTHORING; their leftover-design "
        f"stays on the current g29 and g30 leftover-joins cited in basedOn. {SPEAKER} is "
        f"not a second register row. {SPEAKER} does not SATISFY DR-117. {SPEAKER} does not "
        f"open D-056 Class A and does not lift D-137's express reservation; lifting it is "
        f"the owner's later act in a reviewed coordinator entry, not an act of this "
        f"successor. {SPEAKER} does not author fixture bytes and does not invent the DR-131 "
        f"pack. {SPEAKER} does not treat product-boundary-successor-contract.v8 or "
        f"product-boundary-preview.v2 as SATISFIED. {SPEAKER} does not add a DR-G* row, "
        f"does not change live required-now {REQUIRED_NOW}, does not name G13 into "
        f"required-now, applies nothing, and does not authorize docs/v2/implementation/. "
        f"{SPEAKER} existing is not a SATISFIED-GRADE cycle. Gate 1 Class A remains false "
        f"under D-137's express reservation.",
        "written for v9 from scratch: the predecessor's claim was a D-167 / D-169 / D-206 "
        "remasurement statement that cited g29 and g30 leftover-join.v3, and none of that "
        "is v9's history or v9's citation set")

    purpose = ledger.rewrite(
        "purpose", pred["purpose"],
        f"Re-cite, at live HEAD, the {JOIN_COUNT_WORD} leftover-joins {PRED_SELF} "
        f"({PRED_RECORDING}) cited at versions since superseded, pinning each at the "
        f"version its highest non-CONTESTED COORD recording names, with both Stage A "
        f"verdicts. Carry the fourteen enforcement-evidence classes and the seven "
        f"dispositions of {PRED_SELF} byte-identically. State in terms the relationship "
        f"between this preview-scoped lineage and product-boundary-successor-contract.v8 "
        f"(D-116). Re-pin file 08, file 02, the v1-slice, COORD and HEAD, and recompute "
        f"every recordedInputs digest. Preserve leftover-design of unnamed EE classes as "
        f"closed (D-159: gates 2 and 3 hold). Remainder is named-gate execution. Gate 1 "
        f"Class A remains false under D-137's express reservation until a coordinator act "
        f"supersedes it. Do not SATISFY DR-117. Do not open D-056 Class A. Do not author "
        f"fixture, golden, or adapter bytes. Do not invent a new product-boundary item, a "
        f"D9 code, a section 7.1 recipe, a D-006 unit, or the DR-131 pack. Do not name G13 "
        f"into required-now. Do not steal gate leftover-design.",
        "written for v9 from scratch: 'Remasure v7 against live HEAD after D-167 / D-169 / "
        "D-206' is the predecessor's purpose, not this successor's")

    eligibility_note = ledger.rewrite(
        "eligibilityNote", pred["eligibilityNote"],
        f"D-159 recorded that D-056 Eligibility gates 2 and 3 hold for DR-117. "
        f"leftover-design of unnamed EE classes is closed. CANDIDATE-NOT-APPLIED is not a "
        f"Class A bar (D-085 / D-147). binds NOTHING is {SELF}'s own status field, not a "
        f"cited holding. Gate 1's application-grade / no-express-reservation limb is not "
        f"established by {SELF}; predecessorStanding.stageAGate1Standing recites what the "
        f"two Stage A verdicts on {PRED_SELF} say about that limb in their own shapes. "
        f"Gate 1 Class A "
        f"remains false under D-137's express reservation until a coordinator act "
        f"supersedes it. {SPEAKER} existing does not perform Gate 4 SATISFIED-GRADE and "
        f"does not edit file 08. Preview is not MVP (D-018). Live required-now is "
        f"{REQUIRED_NOW}. Frozen preview-product-boundary-successor.v7 ({V7_RECORDING}) is "
        f"a historical measurement, and {PRED_SELF} ({PRED_RECORDING}) remains the current "
        f"recorded remasurement until a coordinator act records {SELF}.",
        "rewritten: the predecessor's closing sentence 'Frozen v7 is not this "
        "remasurement' carries a bare version token and no longer states the lineage's "
        "standing, which at v9 turns on preview-product-boundary-successor.v8")

    # ---- assemble --------------------------------------------------------
    doc = {
        "artifact": ARTIFACT_NAME,
        "version": VERSION,
        "date": today,
        "documentClass": ledger.carry("documentClass", pred["documentClass"]),
        "registerRow": ledger.carry("registerRow", pred["registerRow"]),
        "status": ledger.carry("status", pred["status"]),
        "reviewStatus": ledger.carry("reviewStatus", pred["reviewStatus"]),
        "sealRecommendation": ledger.carry("sealRecommendation", pred["sealRecommendation"]),
        "binds": ledger.carry("binds", pred["binds"]),
        "basedOn": based_on,
        "predecessorStanding": predecessor_standing,
        "joinCurrencyAudit": join_currency_audit,
        "authorityClaim": authority_claim,
        "purpose": purpose,
        "lineage": lineage,
        "p1p2g3Mapping": ledger.carry("p1p2g3Mapping", pred["p1p2g3Mapping"]),
        "registerRowQuoted": {
            "sourcePath": ledger.carry("registerRowQuoted.sourcePath",
                                       pred["registerRowQuoted"]["sourcePath"]),
            "sourceSha256": ledger.rewrite(
                "registerRowQuoted.sourceSha256",
                pred["registerRowQuoted"]["sourceSha256"], file08_sha,
                "re-pinned to live file 08; it moved once, at D-236, and the DR-117 row's "
                "acceptance-evidence cell is verified equal to the quoted bytes"),
            "rowLocationDiscipline": ledger.carry(
                "registerRowQuoted.rowLocationDiscipline",
                pred["registerRowQuoted"]["rowLocationDiscipline"]),
            "acceptanceEvidenceCellVerbatim": ledger.carry(
                "registerRowQuoted.acceptanceEvidenceCellVerbatim", acceptance_cell,
                "carried byte-identical and re-read from live file 08; equality asserted"),
            "cellLimbs": ledger.carry("registerRowQuoted.cellLimbs",
                                      pred["registerRowQuoted"]["cellLimbs"]),
        },
        "sevenItems": {
            "sourcePath": ledger.carry("sevenItems.sourcePath",
                                       pred["sevenItems"]["sourcePath"]),
            "sourceSha256": sha256_file(FILE02),
            "countPin": ledger.carry("sevenItems.countPin", pred["sevenItems"]["countPin"]),
            "dispositions": dispositions,
        },
        "enforcementEvidence": enforcement_evidence,
        "doesNot": does_not,
        "findingDisposition": finding_disposition,
        "eligibilityNote": eligibility_note,
        "recordedInputs": {},          # filled below
        "head": head,
        "requiredNowUnchanged": REQUIRED_NOW,
        "remeasurementClause": "",     # filled below
        "leftoverDesignOpenStanding": leftover_design_open_standing,
        "file08Pin": {"path": FILE08, "sha256": file08_sha},
        "file08StatusToken": status_token,
    }
    need(doc["sevenItems"]["sourceSha256"] == pred["sevenItems"]["sourceSha256"],
         "file 02 has moved; the seven-item enumeration's source pin would change and "
         "file 08 line 299 says any change to that enumeration re-opens DR-117")
    ledger.carry("sevenItems.sourceSha256", doc["sevenItems"]["sourceSha256"],
                 "re-measured at run time and equal to the predecessor's pin")
    ledger.rewrite("date", pred["date"], today, "today's date from the clock")
    ledger.rewrite("head", pred["head"], head, "re-pinned to live git HEAD")
    ledger.rewrite("file08Pin.sha256", pred["file08Pin"]["sha256"], file08_sha,
                   "re-pinned to live file 08")
    ledger.carry("file08StatusToken", status_token,
                 "read from live file 08's DR-117 row; equal to the predecessor's token")
    ledger.carry("requiredNowUnchanged", REQUIRED_NOW,
                 "carried and asserted against file 08's condition-4 snapshot")
    ledger.rewrite("artifact", pred["artifact"], ARTIFACT_NAME, "successor identity")
    ledger.rewrite("version", pred["version"], VERSION, "successor identity")

    # ---- recordedInputs (regenerated) -----------------------------------
    pinned = {}

    def collect(node):
        if isinstance(node, dict):
            for key_path, key_sha in (("path", "sha256"), ("sourcePath", "sourceSha256")):
                if isinstance(node.get(key_path), str) and isinstance(node.get(key_sha), str):
                    pinned[node[key_path]] = node[key_sha]
            for value in node.values():
                collect(value)
        elif isinstance(node, list):
            for value in node:
                collect(value)

    collect(doc)
    pinned[COORD] = sha256_file(COORD)
    pinned[PREVIEW_V2_PATH] = sha256_file(PREVIEW_V2_PATH)
    # every path the predecessor pinned stays pinned, re-measured
    for path in pred["recordedInputs"]:
        if path == "HEAD":
            continue
        pinned.setdefault(path, sha256_file(path))

    for path, sha in sorted(pinned.items()):
        actual = sha256_file(path)
        need(actual == sha,
             f"pinned digest for {path} does not recompute: document says {sha}, "
             f"bytes are {actual}")
    recorded_inputs = {path: pinned[path] for path in sorted(pinned)}
    recorded_inputs["HEAD"] = head
    doc["recordedInputs"] = recorded_inputs
    for path in pred["recordedInputs"]:
        need(path in recorded_inputs,
             f"the predecessor pinned {path} and this successor drops it")
    ledger.rewrite("recordedInputs",
                   f"{len(pred['recordedInputs'])} entries",
                   f"{len(recorded_inputs)} entries",
                   "regenerated: every path pinned anywhere in this successor, plus every "
                   "path the predecessor pinned, each digest recomputed at run time")

    # ---- remeasurementClause (generated from recordedInputs) ------------
    doc["remeasurementClause"] = ledger.rewrite(
        "remeasurementClause", pred["remeasurementClause"],
        f"If any file pinned in recordedInputs moves in a way that is not append-only "
        f"growth of {COORD} or COORD heading hygiene, re-measure before recording. The "
        f"trigger reaches every one of the {len(recorded_inputs) - 1} pinned rows, not an "
        f"enumerated subset: this clause is generated from recordedInputs rather than "
        f"maintained by addition. recordedInputs.HEAD must equal the top-level head. "
        f"file08Pin.sha256, registerRowQuoted.sourceSha256 and recordedInputs[{FILE08!r}] "
        f"must all equal the same live digest of file 08, and DR-117's leading label there "
        f"must still be {status_token}. sevenItems.sourceSha256 must still equal the live "
        f"digest of {FILE02}; file 08's DR-117 row says any change to that enumeration "
        f"re-opens the row. Each of the {JOIN_COUNT_WORD} current leftover-joins named in "
        f"basedOn must still be the version its highest non-CONTESTED COORD recording "
        f"names; if a later recording supersedes one, re-measure before recording. "
        f"{SPEAKER} does not unwrite D-137, D-157, D-158, D-159, D-167, D-168, D-169, or "
        f"any entry from D-170 through D-{highest_coord}. Frozen "
        f"preview-product-boundary-successor.v7 remains a historical measurement as of HEAD "
        f"{v7['head']} / required-now {v7['requiredNowUnchanged']}. {SPEAKER} existing is "
        f"not a recording.",
        "regenerated from recordedInputs for CLAUDE-PPBS-V8-ADV-2, and re-pointed at v9's "
        "own pins; the predecessor's clause named an anchor subset with bare version tokens")

    # ---- final assertions ------------------------------------------------
    need(doc["recordedInputs"]["HEAD"] == doc["head"],
         "recordedInputs.HEAD does not equal the top-level head")
    need(doc["recordedInputs"][FILE08] == doc["file08Pin"]["sha256"]
         == doc["registerRowQuoted"]["sourceSha256"],
         "the three file-08 pins disagree")
    need(doc["status"] == "CANDIDATE-NOT-APPLIED", "status is not CANDIDATE-NOT-APPLIED")
    need(doc["reviewStatus"] == "AWAITING-INDEPENDENT-REVIEW",
         "reviewStatus is not AWAITING-INDEPENDENT-REVIEW")
    need(doc["binds"] == "NOTHING", "binds is not NOTHING")
    need(doc["sealRecommendation"] == "DO-NOT-SEAL", "sealRecommendation is not DO-NOT-SEAL")
    need(doc["registerRow"] == REGISTER_ROW, "registerRow is not DR-117")
    need(len(doc["enforcementEvidence"]["classes"]) == 14, "not fourteen EE classes")
    need(len(doc["sevenItems"]["dispositions"]) == 7, "not seven dispositions")
    need(len(doc["joinCurrencyAudit"]["joins"]) == 12, "not twelve joins in the currency audit")

    findings = audit_strings(doc)
    if findings:
        fail("house-rule audit failed:\n  " + "\n  ".join(findings))

    payload = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(payload)

    if not quiet:
        print(f"wrote {out_path}")
        print(f"  sha256 {hashlib.sha256(payload.encode('utf-8')).hexdigest()}")
        print(f"  bytes  {len(payload.encode('utf-8'))}")
        print(f"  head   {head}")
        print(f"  date   {today}")

    return doc, payload, joins, pred


def build_audit(doc, payload, joins, pred, ledger, out_path):
    return {
        "generator": os.path.basename(os.path.abspath(__file__)),
        "generatedAt": doc["date"],
        "head": doc["head"],
        "predecessor": {"path": PRED_PATH, "sha256": PRED_SHA256, "recording": PRED_RECORDING},
        "output": {
            "path": out_path,
            "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
            "bytes": len(payload.encode("utf-8")),
        },
        "joinsVerified": [
            {
                "lineage": join["lineage"],
                "registerRow": join["registerRow"],
                "predecessorCited": f"leftover-join.v{join['citedVersion']} "
                                    f"({join['citedRecording']})",
                "currentNow": f"leftover-join.v{join['version']} ({join['recording']})",
                "sha256": join["sha256"],
                "leftoverDesignTrue": join["leftoverDesignTrue"],
                "stageAVerdicts": {
                    "claude": join["reviews"]["claude"]["verdict"],
                    "codex": join["reviews"]["codex"]["verdict"],
                },
            }
            for join in joins
        ],
        "rewrittenFields": ledger.rewritten,
        "carriedFields": ledger.carried,
        "newFields": ledger.added,
        "counts": {
            "rewritten": len(ledger.rewritten),
            "carried": len(ledger.carried),
            "new": len(ledger.added),
            "recordedInputsPredecessor": len(pred["recordedInputs"]),
            "recordedInputsSuccessor": len(doc["recordedInputs"]),
            "eeClasses": len(doc["enforcementEvidence"]["classes"]),
            "dispositions": len(doc["sevenItems"]["dispositions"]),
            "doesNotPredecessor": len(pred["doesNot"]),
            "doesNotSuccessor": len(doc["doesNot"]),
        },
        "assertions": [
            "predecessor sha256 equals the D-207 recording",
            "no tracked file under docs/ is modified",
            "the fourteen EE classes are byte-identical to the predecessor's",
            "the seven dispositions are byte-identical to the predecessor's",
            "EE class routing derived from bytes matches the recorded gate map",
            "each of the twelve joins is the version named by its highest non-CONTESTED "
            "COORD recording",
            "each join's digest and both Stage A verdict digests appear in that recording",
            "each join is CANDIDATE-NOT-APPLIED and binds NOTHING",
            "file 08 still carries the condition-4 snapshot that reproduces required-now 28",
            "DR-117's live leading label is OPEN",
            "DR-117's acceptance-evidence cell equals the predecessor's quotation",
            "file 02 is unmoved, so the seven-item enumeration is unchanged",
            "every recordedInputs digest recomputes against live bytes",
            "no path the predecessor pinned is dropped",
            "house-rule audit: no deictic predecessor self-reference, no bare version "
            "token, no unsubstituted brace token",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("output", nargs="?", default=DEFAULT_OUT_DIR,
                        help="output file or directory (default: this script's directory)")
    parser.add_argument("--audit", metavar="PATH",
                        help="also write the rewrite/carry ledger as JSON")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    out = args.output
    out_path = out if out.endswith(".json") else os.path.join(out, OUT_BASENAME)

    ledger = Ledger()
    try:
        # The docs/ tree is a frozen provenance record.  Refuse before any
        # directory is created, so a bad target leaves nothing behind.
        docs_root = os.path.abspath(os.path.join(os.getcwd(), "docs"))
        need(os.path.abspath(out_path) != docs_root
             and not os.path.abspath(out_path).startswith(docs_root + os.sep),
             "refusing to write under docs/: that tree is a frozen provenance record")
        parent = os.path.dirname(os.path.abspath(out_path))
        if not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)
        doc, payload, joins, pred = build(out_path, ledger, args.quiet)
    except Fail as exc:
        print(f"make-ppbs-v9.py: FAILED: {exc}", file=sys.stderr)
        return 2

    if args.audit:
        audit = build_audit(doc, payload, joins, pred, ledger, out_path)
        with open(args.audit, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(audit, indent=2, ensure_ascii=False) + "\n")
        if not args.quiet:
            print(f"wrote {args.audit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
