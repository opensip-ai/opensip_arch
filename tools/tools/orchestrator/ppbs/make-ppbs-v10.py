#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make-ppbs-v10.py

Generate `preview-product-boundary-successor.v10.json` from the frozen,
Stage-A-rejected predecessor
`docs/coop/artifacts/preview-product-boundary-successor.v9.json`
(sha256 e0221a1c…), landing the four Stage A findings:

  CLAUDE-PPBS-V9-B1  forty stale cross-lineage currency citations inside the
                     fourteen enforcement-evidence classes
  CLAUDE-PPBS-V9-B2  EE-3a asserts OBL-G23-FX-AUTHORING as leftover-design on a
                     lineage whose current join flags none
  CLAUDE-PPBS-V9-SF1 "the whole reason" / "nothing else is disturbed" overclaim
  PPBSV9-B1          (Codex) the same forty sites, plus the broad byte-identity
                     assertions that cover them

plus CLAUDE-PPBS-V9-ADV-1 (the em-dash heading form in joinCurrencyAudit.method).

The refresh rule is COORD `## D-294` Decision 3: "A successor issued for any
reason refreshes its cross-lineage citations to the versions current at its
dispatch and labels the superseded ones as not current. No frozen artifact is
edited to achieve this."

v10 is v9 plus those changes and nothing else.  The "nothing else" half is
proved, not asserted: after normalizing the refreshed citation tokens and the
EE-3a leftoverDesign sentence in both, v10's fourteen classes must equal v8's
fourteen classes, or the run fails.

Run from the repository root.  Writes nothing under docs/.  Runs no
state-changing git command.

    python3 make-ppbs-v10.py [OUTPUT] [--audit AUDIT.json] [--quiet]
"""

from __future__ import annotations

import argparse
import copy
import datetime
import hashlib
import importlib.util
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "make_ppbs_v9", os.path.join(_HERE, "make-ppbs-v9.py"))
if _spec is None or _spec.loader is None:                      # pragma: no cover
    raise SystemExit("make-ppbs-v10.py: cannot locate make-ppbs-v9.py beside it")
v9mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v9mod)

# Reused, unchanged, from the v9 generator.
Fail = v9mod.Fail
fail = v9mod.fail
need = v9mod.need
sha256_file = v9mod.sha256_file
read_text = v9mod.read_text
read_json = v9mod.read_json
stem = v9mod.stem
git = v9mod.git
Ledger = v9mod.Ledger
ART = v9mod.ART
FILE08 = v9mod.FILE08
FILE02 = v9mod.FILE02
COORD = v9mod.COORD
V1_SLICE = v9mod.V1_SLICE
JOINS = v9mod.JOINS
JOIN_COUNT_WORD = v9mod.JOIN_COUNT_WORD
REQUIRED_NOW = v9mod.REQUIRED_NOW
REQUIRED_NOW_SNAPSHOT = v9mod.REQUIRED_NOW_SNAPSHOT
REGISTER_ROW = v9mod.REGISTER_ROW
DR117_EXPECTED_STATUS = v9mod.DR117_EXPECTED_STATUS
PRED8_PATH = v9mod.PRED_PATH
PRED8_SHA256 = v9mod.PRED_SHA256

# ---------------------------------------------------------------------------
# v10 constants
# ---------------------------------------------------------------------------

ARTIFACT_NAME = "preview-product-boundary-successor.v10"
OUT_BASENAME = "preview-product-boundary-successor.v10.json"
VERSION = 10
DEFAULT_OUT_DIR = _HERE

SELF = "preview-product-boundary-successor.v10"
SPEAKER = "This preview-product-boundary-successor.v10"
PREV9 = "preview-product-boundary-successor.v9"
PRED8 = "preview-product-boundary-successor.v8"

V9_PATH = f"{ART}/preview-product-boundary-successor.v9.json"
V9_SHA256 = "e0221a1c095f688dcd5b127bce9f712543165599c71dc8415b94fb7bfdea4dd5"
V9_REVIEW_CLAUDE = f"{ART}/preview-product-boundary-successor.v9.review-independent.claude2.json"
V9_REVIEW_CODEX = f"{ART}/preview-product-boundary-successor.v9.review-independent.codex.json"

D294 = "D-294"
D294_REFRESH_RULE = (
    "D-294 Decision 3: a successor issued for any reason refreshes its "
    "cross-lineage citations to the versions current at its dispatch and labels "
    "the superseded ones as not current. No frozen artifact is edited to "
    "achieve this.")

# The one sentence CLAUDE-PPBS-V9-B2 names, verbatim as v9 carries it.
EE3A_OLD_PARTITION = ("leftoverDesign remains [OBL-G21-FX-AUTHORING] and "
                      "[OBL-G23-FX-AUTHORING].")
EE3A_NORM_SENTINEL = "[EE-3A-LEFTOVERDESIGN-PARTITION-NORMALIZED]"

# The citation form D-294 Decision 1 calls the spaced spelling.
CITE_RE = re.compile(r"(?P<lin>[a-z0-9-]+) leftover-join\.v(?P<ver>\d+) \((?P<rec>D-\d+)\)")

# Audit: the inverted currency form, and the "remain(s) on X leftover-join.vN" form.
CURRENCY_INVERTED_RE = re.compile(
    r"[Cc]urrent [^.]{0,90}?leftover-join (?:is|are|remains) "
    r"([a-z0-9-]+)[- ]leftover-join\.v(\d+)")
CURRENCY_REMAIN_ON_RE = re.compile(
    r"(?:remain|remains) on ([a-z0-9-]+)[- ]leftover-join\.v(\d+)")
DEICTIC_V10_RE = re.compile(r"[Tt]his v\d+")
BYTE_IDENTICAL_RE = re.compile(r"byte-identical|byte-identically|byte-for-byte")


# ---------------------------------------------------------------------------
# Audit (v9's rules plus the four the coordinator added)
# ---------------------------------------------------------------------------

def audit_document(doc, current):
    findings = []

    def check(text, where):
        for m in DEICTIC_V10_RE.finditer(text):
            findings.append(f"{where}: deictic version self-reference {m.group(0)!r}")
        for ctx in v9mod.unqualified_version_tokens(text):
            findings.append(f"{where}: bare version token near ...{ctx}...")
        if "{" in text or "}" in text:
            findings.append(f"{where}: unsubstituted brace token")
        for rx, label in ((CURRENCY_INVERTED_RE, "inverted currency claim"),
                          (CURRENCY_REMAIN_ON_RE, "remain-on currency claim")):
            for m in rx.finditer(text):
                lineage, version = m.group(1), int(m.group(2))
                if lineage not in current:
                    continue
                if version != current[lineage][0]:
                    findings.append(
                        f"{where}: {label} names {lineage} leftover-join.v{version}; "
                        f"the current version is v{current[lineage][0]} "
                        f"({current[lineage][1]})")
        if BYTE_IDENTICAL_RE.search(text) and re.search(
                r"\bclasses\b|enforcement-evidence class", text):
            for sentence in re.split(r"(?<=\.)\s+", text):
                if BYTE_IDENTICAL_RE.search(sentence) and re.search(
                        r"\bclasses\b|enforcement-evidence class", sentence):
                    findings.append(
                        f"{where}: byte-identity claim about the enforcement-evidence "
                        f"classes: {sentence[:120]!r}")

    def walk(node, path="$"):
        if isinstance(node, dict):
            for key, value in node.items():
                check(str(key), f"{path}.{key} (key)")
                walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for i, value in enumerate(node):
                walk(value, f"{path}[{i}]")
        elif isinstance(node, str):
            check(node, path)

    walk(doc)
    return findings


# ---------------------------------------------------------------------------
# Normalization used to prove "nothing else changed"
# ---------------------------------------------------------------------------

def normalize_citations(text: str) -> str:
    return CITE_RE.sub(
        lambda m: f"{m.group('lin')} leftover-join.vNORM (D-NORM)", text)


def make_normalizer(new_partition_sentence: str):
    sentinels = {normalize_citations(new_partition_sentence),
                 normalize_citations(EE3A_OLD_PARTITION)}

    def norm(node):
        if isinstance(node, dict):
            return {k: norm(v) for k, v in node.items()}
        if isinstance(node, list):
            return [norm(v) for v in node]
        if isinstance(node, str):
            text = normalize_citations(node)
            for sentinel in sentinels:
                text = text.replace(sentinel, EE3A_NORM_SENTINEL)
            return text
        return node

    return norm


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build(out_path: str, ledger: Ledger, quiet: bool):
    v9mod.assert_repo_root()
    v9mod.assert_docs_tree_clean()

    today = datetime.date.today().isoformat()
    head = git("rev-parse", "HEAD")
    need(re.fullmatch(r"[0-9a-f]{40}", head) is not None,
         f"git HEAD is not a full sha: {head!r}")

    # ---- the frozen, rejected predecessor -------------------------------
    v9_sha = sha256_file(V9_PATH)
    need(v9_sha == V9_SHA256,
         f"the frozen predecessor moved: {V9_PATH} is {v9_sha}, Stage A reviewed "
         f"{V9_SHA256}")
    v9 = read_json(V9_PATH)
    need(v9["artifact"] == PREV9 and v9["version"] == 9,
         "the predecessor file does not identify itself as "
         "preview-product-boundary-successor.v9")

    v8_sha = sha256_file(PRED8_PATH)
    need(v8_sha == PRED8_SHA256, "preview-product-boundary-successor.v8 has moved")
    v8 = read_json(PRED8_PATH)

    # ---- both Stage A verdicts on the predecessor ------------------------
    claude = read_json(V9_REVIEW_CLAUDE)
    codex = read_json(V9_REVIEW_CODEX)
    need(claude.get("verdict") == "REJECT" and codex.get("verdict") == "REJECT",
         "the Stage A verdicts on the predecessor are not both REJECT")
    need(claude.get("blockerCount") == 2 and claude.get("shouldFixCount") == 1,
         "the Claude verdict's counts are not blockerCount 2 / shouldFixCount 1")
    need(codex.get("blockerCount") == 1 and codex.get("shouldFixCount") == 0,
         "the Codex verdict's counts are not blockerCount 1 / shouldFixCount 0")
    claude_ids = [b["id"] for b in claude["blockers"]] + \
                 [s["id"] for s in claude["shouldFix"]]
    claude_adv = [a["id"] for a in claude.get("advisories", [])]
    codex_ids = [b["id"] for b in codex["blockers"]]
    need(claude_ids == ["CLAUDE-PPBS-V9-B1", "CLAUDE-PPBS-V9-B2",
                        "CLAUDE-PPBS-V9-SF1"],
         f"the Claude verdict's finding ids are {claude_ids}")
    need(claude_adv == ["CLAUDE-PPBS-V9-ADV-1"],
         f"the Claude verdict's advisory ids are {claude_adv}")
    need(codex_ids == ["PPBSV9-B1"], f"the Codex verdict's blocker ids are {codex_ids}")
    for pinned in (claude, codex):
        for key in ("subject", "subjectCustody"):
            block = pinned.get(key)
            if isinstance(block, dict):
                for field in ("sha256Expected", "expectedSha256"):
                    if field in block:
                        need(block[field] == V9_SHA256,
                             f"a Stage A verdict reviewed a different subject digest")

    # ---- live measurements ----------------------------------------------
    coord_text = read_text(COORD)
    highest_coord = max(n for _i, n, _l in v9mod.coord_headings(coord_text))
    file08_text = read_text(FILE08)
    file08_sha = sha256_file(FILE08)
    need(REQUIRED_NOW_SNAPSHOT in file08_text,
         f"file 08 no longer carries {REQUIRED_NOW_SNAPSHOT!r}")
    header, row = v9mod.file08_row_cells(file08_text, REGISTER_ROW)
    status_token = v9mod.leading_label(v9mod.file08_cell(header, row, "Status"))
    need(status_token == DR117_EXPECTED_STATUS,
         f"DR-117's live leading label is {status_token!r}, not "
         f"{DR117_EXPECTED_STATUS!r}")
    acceptance_cell = v9mod.file08_cell(header, row, "Required acceptance evidence")
    need(acceptance_cell == v9["registerRowQuoted"]["acceptanceEvidenceCellVerbatim"],
         "DR-117's acceptance-evidence cell has moved")
    need(sha256_file(FILE02) == v9["sevenItems"]["sourceSha256"],
         "file 02 has moved; the seven-item enumeration's source pin would change")
    need(sha256_file(V1_SLICE) == v9["enforcementEvidence"]["v1SlicePin"]["sha256"],
         "the v1-slice has moved")

    # ---- the twelve current joins, measured from COORD --------------------
    current = {}
    cited_by_v8 = {}
    join_rows = []
    for lineage, key_stem, cited_v, cited_rec, exp_v, exp_rec, kind in JOINS:
        number, version, heading = v9mod.current_join_recording(coord_text, lineage)
        recording = f"D-{number}"
        need(version == exp_v and recording == exp_rec,
             f"{lineage} leftover-join currency changed: COORD's highest "
             f"non-CONTESTED recording is {recording} at version {version}; the "
             f"adopted programme names {exp_rec} at version {exp_v}. "
             f"Heading: {heading}")
        path = f"{ART}/{lineage}-leftover-join.v{version}.json"
        sha = sha256_file(path)
        entry = v9mod.coord_entry_text(coord_text, recording)
        need(sha in entry, f"{recording} does not carry the digest of {path}")
        current[lineage] = (version, recording)
        cited_by_v8[lineage] = (cited_v, cited_rec)
        join_rows.append({
            "lineage": lineage, "version": version, "recording": recording,
            "path": path, "sha256": sha,
            "leftoverDesignTrue": v9mod.leftover_design_ids(read_json(path)),
        })
        # the successor's own basedOn must already pin exactly this
        key = f"{key_stem}V{version}"
        need(v9["basedOn"].get(key, {}).get("sha256") == sha,
             f"the predecessor's basedOn.{key} does not pin {path} at its live digest")
    need(len(current) == 12, f"expected twelve lineages, measured {len(current)}")

    g21 = next(r for r in join_rows if r["lineage"] == "g21")
    g23 = next(r for r in join_rows if r["lineage"] == "g23")
    need(g21["leftoverDesignTrue"] == ["OBL-G21-FX-AUTHORING"],
         f"g21 leftover-join.v{g21['version']} flags "
         f"{g21['leftoverDesignTrue']}, not [OBL-G21-FX-AUTHORING]")
    need(g23["leftoverDesignTrue"] == [],
         f"g23 leftover-join.v{g23['version']} flags {g23['leftoverDesignTrue']}; "
         f"CLAUDE-PPBS-V9-B2's repair assumes an empty partition")
    g23_doc = read_json(g23["path"])
    summary_partition = (g23_doc.get("summary") or {}).get("leftoverDesign")
    need(summary_partition == [] or summary_partition is None,
         f"g23's summary.leftoverDesign is {summary_partition!r}, not empty")

    ee3a_new_partition = (
        f"leftoverDesign remains [OBL-G21-FX-AUTHORING] on g21 leftover-join."
        f"v{g21['version']} ({g21['recording']}); g23 leftover-join."
        f"v{g23['version']} ({g23['recording']}) flags no obligation "
        f"leftoverDesign true.")

    # ---- v10 = deep copy of v9, then the enumerated changes ---------------
    doc = copy.deepcopy(v9)
    refreshed_sites = []

    # (1) mechanical currency refresh inside the fourteen classes only
    for cls in doc["enforcementEvidence"]["classes"]:
        for field in ("existingGate", "laterExecution"):
            text = cls.get(field)
            if not isinstance(text, str):
                continue
            occurrence = {"n": 0}

            def replace(m, cls=cls, field=field, text=text, occurrence=occurrence):
                lineage = m.group("lin")
                need(lineage in current,
                     f"{cls['id']}.{field} cites lineage {lineage!r}, which is not "
                     f"one of the twelve")
                old = (int(m.group("ver")), m.group("rec"))
                need(old == cited_by_v8[lineage],
                     f"{cls['id']}.{field} cites {lineage} leftover-join.v{old[0]} "
                     f"({old[1]}); preview-product-boundary-successor.v8 cited "
                     f"v{cited_by_v8[lineage][0]} ({cited_by_v8[lineage][1]}). "
                     f"The refresh is only defined for the superseded citations.")
                version, recording = current[lineage]
                occurrence["n"] += 1
                new = f"{lineage} leftover-join.v{version} ({recording})"
                refreshed_sites.append({
                    "kind": "currency-citation",
                    "class": cls["id"], "field": field,
                    "occurrence": occurrence["n"],
                    "lineage": lineage,
                    "before": m.group(0), "after": new,
                    "context": text[max(0, m.start() - 55):m.end()][-100:],
                })
                return new

            cls[field] = CITE_RE.sub(replace, text)

    need(len(refreshed_sites) == 40,
         f"expected the forty citation sites both reviews enumerate, refreshed "
         f"{len(refreshed_sites)}")

    # (2) CLAUDE-PPBS-V9-B2: EE-3a's leftoverDesign partition
    ee3a = next(c for c in doc["enforcementEvidence"]["classes"] if c["id"] == "EE-3a")
    for field in ("existingGate", "laterExecution"):
        text = ee3a[field]
        need(text.count(EE3A_OLD_PARTITION) == 1,
             f"EE-3a.{field} does not carry the misquoted partition sentence exactly "
             f"once")
        ee3a[field] = text.replace(EE3A_OLD_PARTITION, ee3a_new_partition)
        refreshed_sites.append({
            "kind": "leftoverDesign-partition",
            "class": "EE-3a", "field": field, "occurrence": 1,
            "lineage": "g23",
            "before": EE3A_OLD_PARTITION, "after": ee3a_new_partition,
            "context": "CLAUDE-PPBS-V9-B2",
        })
    site_count = len(refreshed_sites)
    need(site_count == 42,
         f"expected forty currency sites plus two partition sites, got {site_count}")

    # (3) the assertion: nothing else in the fourteen classes changed
    norm = make_normalizer(ee3a_new_partition)
    normalized_v10 = norm(doc["enforcementEvidence"]["classes"])
    normalized_v8 = norm(v8["enforcementEvidence"]["classes"])
    classes_equal = (json.dumps(normalized_v10, sort_keys=True, ensure_ascii=False)
                     == json.dumps(normalized_v8, sort_keys=True, ensure_ascii=False))
    need(classes_equal,
         "after normalizing the refreshed citation tokens and the EE-3a "
         "leftoverDesign partition sentence, the fourteen classes of "
         "preview-product-boundary-successor.v10 do not equal "
         "preview-product-boundary-successor.v8's: something other than the "
         "authorized refresh changed")
    need(doc["sevenItems"]["dispositions"] == v8["sevenItems"]["dispositions"],
         "the seven dispositions are no longer byte-identical to "
         "preview-product-boundary-successor.v8's")
    need(doc["p1p2g3Mapping"] == v8["p1p2g3Mapping"],
         "p1p2g3Mapping is no longer byte-identical")

    by_lineage = {}
    for site in refreshed_sites:
        if site["kind"] != "currency-citation":
            continue
        by_lineage[site["lineage"]] = by_lineage.get(site["lineage"], 0) + 1
    need(sum(by_lineage.values()) == 40,
         "the per-lineage currency tally does not sum to forty")
    partition_sites = [f"EE-3a.{s['field']}" for s in refreshed_sites
                       if s["kind"] == "leftoverDesign-partition"]

    exact_truth = (
        f"The fourteen enforcement-evidence classes of {SELF} are identical to "
        f"{PRED8}'s except the cross-lineage currency sentences refreshed under "
        f"{D294} Decision 3 and the EE-3a leftoverDesign partition sentence "
        f"CLAUDE-PPBS-V9-B2 names: {site_count} sites, being 40 currency citations "
        f"and 2 partition sentences. The seven dispositions and p1p2g3Mapping are "
        f"byte-identical, and that equality is asserted before this file is "
        f"written.")

    doc["enforcementEvidence"]["classesRefresh"] = ledger.new(
        "enforcementEvidence.classesRefresh",
        {
            "rule": D294_REFRESH_RULE,
            "method": (
                "Mechanical rewrite of the version token and the recording D-number "
                "inside enforcementEvidence.classes[*].existingGate and "
                "enforcementEvidence.classes[*].laterExecution only, plus the EE-3a "
                "leftoverDesign partition sentence CLAUDE-PPBS-V9-B2 names. No "
                "identifier, item, subLimb, invariant, input, pass rule, owner or "
                "gate assignment was touched, and no frozen artifact was edited."),
            "siteCount": site_count,
            "currencyCitationSites": 40,
            "leftoverDesignPartitionSites": 2,
            "currencyCitationSitesByLineage": by_lineage,
            "leftoverDesignPartitionSiteList": partition_sites,
            "classEqualityAssertion": {
                "statement": (
                    f"After normalizing the refreshed citation tokens and the EE-3a "
                    f"leftoverDesign partition sentence in both, {SELF}'s fourteen "
                    f"classes equal {PRED8}'s fourteen classes."),
                "method": "canonical JSON comparison of the two normalized arrays",
                "result": "HOLDS",
            },
            "exactTruth": exact_truth,
            "landedFindings": ["CLAUDE-PPBS-V9-B1", "CLAUDE-PPBS-V9-B2", "PPBSV9-B1"],
        },
        "new object: CLAUDE-PPBS-V9-B1 and PPBSV9-B1 require the refresh to be "
        "visible and its scope provable in the artifact itself")

    # ---- speaker retarget where the sentence's meaning is unchanged -------
    RETARGET = [
        "basedOn.predecessorPinningShape",
        "basedOn.g29JoinV4.role", "basedOn.g30JoinV4.role", "basedOn.g09JoinV12.role",
        "basedOn.languageRuntimeJoinV7.role", "basedOn.g16JoinV5.role",
        "basedOn.g21JoinV13.role", "basedOn.g23JoinV8.role",
        "basedOn.permissionJoinV12.role", "basedOn.distributionCoreJoinV9.role",
        "basedOn.monorepoJoinV4.role", "basedOn.languageQualityJoinV5.role",
        "basedOn.doctorActorJoinV12.role",
        "predecessorStanding.stageAGate1Standing",
        "lineage.productBoundarySuccessorContractV8.role",
        "lineage.contractRelationship",
        "enforcementEvidence.ownerOfUnownedPreviewClasses",
        "leftoverDesignOpenStanding",
        "doesNot[2]", "doesNot[22]", "doesNot[25]", "doesNot[26]",
        "findingDisposition CLAUDE-PPBS-V8-ADV-1.disposition",
        "findingDisposition CLAUDE-PPBS-V8-ADV-2.disposition",
        "findingDisposition CLAUDE-PPBS-V7-ADV-2.disposition",
        "findingDisposition CLAUDE-PPBS-V3-ADV-1.venueLimb",
    ]

    def retarget(text: str) -> str:
        return text.replace(PREV9, SELF)

    def apply_retarget(container, key, label):
        old = container[key]
        new = retarget(old)
        need(new != old, f"speaker retarget found nothing to change at {label}")
        container[key] = ledger.rewrite(
            label, old, new,
            "speaker retarget only: the sentence's meaning is unchanged, the "
            "speaker's own version moved")

    for label in RETARGET:
        if label.startswith("doesNot["):
            index = int(label[len("doesNot["):-1])
            apply_retarget(doc["doesNot"], index, label)
        elif label.startswith("findingDisposition "):
            fid, field = label[len("findingDisposition "):].split(".", 1)
            entry = next(e for e in doc["findingDisposition"] if e["id"] == fid)
            apply_retarget(entry, field, label)
        else:
            node = doc
            parts = label.split(".")
            for part in parts[:-1]:
                node = node[part]
            apply_retarget(node, parts[-1], label)

    # ---- CLAUDE-PPBS-V9-ADV-1: the heading form uses an em dash -----------
    old_method = doc["joinCurrencyAudit"]["method"]
    need("## D-NNN - Record" in old_method,
         "joinCurrencyAudit.method no longer carries the ASCII-hyphen heading form")
    sample_heading = v9mod.current_join_recording(coord_text, "g29")[2]
    need(sample_heading.startswith("## D-254 — Record"),
         "COORD's heading form is not '## D-NNN — Record ...'; the quoted form "
         "would still not match")
    doc["joinCurrencyAudit"]["method"] = ledger.rewrite(
        "joinCurrencyAudit.method",
        old_method,
        old_method.replace("## D-NNN - Record", "## D-NNN — Record"),
        "CLAUDE-PPBS-V9-ADV-1: the quoted heading form used an ASCII hyphen where "
        "live COORD headings use an em dash, so a literal match found zero headings")

    # ---- authored rewrites ------------------------------------------------
    doc["artifact"] = ledger.rewrite("artifact", v9["artifact"], ARTIFACT_NAME,
                                     "successor identity")
    doc["version"] = ledger.rewrite("version", v9["version"], VERSION,
                                    "successor identity")
    doc["date"] = ledger.rewrite("date", v9["date"], today, "today's date from the clock")
    doc["head"] = ledger.rewrite("head", v9["head"], head, "re-pinned to live git HEAD")
    doc["file08Pin"] = {"path": FILE08, "sha256": file08_sha}
    doc["registerRowQuoted"]["sourceSha256"] = file08_sha
    ledger.carry("file08Pin.sha256 / registerRowQuoted.sourceSha256",
                 file08_sha,
                 "re-measured at run time; file 08 has not moved since the "
                 "predecessor pinned it")
    ledger.carry("file08StatusToken", doc["file08StatusToken"],
                 "read from live file 08's DR-117 row")
    ledger.carry("requiredNowUnchanged", doc["requiredNowUnchanged"],
                 "asserted against file 08's condition-4 snapshot")

    v9_pin = {
        "path": V9_PATH,
        "sha256": v9_sha,
        "reviews": {
            "claude": v9mod.pin_review(V9_REVIEW_CLAUDE),
            "codex": v9mod.pin_review(V9_REVIEW_CODEX),
        },
        "role": (
            f"Immediate predecessor. Unmoved. Rejected at Stage A and never "
            f"recorded. Claude REJECT at blockerCount 2 / shouldFixCount 1 "
            f"(CLAUDE-PPBS-V9-B1, CLAUDE-PPBS-V9-B2, CLAUDE-PPBS-V9-SF1, with "
            f"advisory CLAUDE-PPBS-V9-ADV-1); Codex REJECT at blockerCount 1 / "
            f"shouldFixCount 0 (PPBSV9-B1); both verdicts recite those counts in "
            f"those fields. Both blockers reach the same bytes from two sides: the "
            f"fourteen enforcement-evidence classes carried {PRED8}'s dispatch-time "
            f"currency sentences forward at forty sites, and EE-3a additionally "
            f"asserted OBL-G23-FX-AUTHORING as leftover-design on a lineage whose "
            f"current join flags none. {SPEAKER} lands all four findings and the "
            f"advisory. Because {PREV9} was never recorded, it never became "
            f"current, and {PRED8} (D-207) remains the current recorded "
            f"remasurement. Not this artifact's version number."),
    }
    ledger.new("basedOn.predecessorV9", v9_pin["role"],
               "new object: the rejected, frozen, unrecorded predecessor and its two "
               "Stage A verdicts")

    based_on = {"predecessorV9": v9_pin}
    for key, value in doc["basedOn"].items():
        based_on[key] = value
    doc["basedOn"] = based_on

    doc["basedOn"]["predecessorV8"]["role"] = ledger.rewrite(
        "basedOn.predecessorV8.role",
        v9["basedOn"]["predecessorV8"]["role"],
        f"Predecessor once removed, and still the current recorded DR-117 leftover "
        f"remasurement, because {PREV9} was rejected and never recorded. Unmoved. "
        f"Recorded at D-207 as the DR-117 leftover remasurement after D-206, "
        f"measured at HEAD {v8['head']} / required-now "
        f"{v8['requiredNowUnchanged']} / file 08 {v8['file08Pin']['sha256']}. Dual "
        f"ACCEPT 0/0 at Stage A. D-293 Decision 5 authorized this lineage's "
        f"successor for two limbs: re-citing the {JOIN_COUNT_WORD} current joins, "
        f"and stating the relationship to product-boundary-successor-contract.v8 "
        f"(D-116). {SPEAKER} performs both, and additionally adds "
        f"predecessorStanding, joinCurrencyAudit, "
        f"enforcementEvidence.classesRefresh and "
        f"lineage.contractRelationship, and rewrites doesNot, eligibilityNote, "
        f"findingDisposition, remeasurementClause, leftoverDesignOpenStanding and "
        f"the registerRowQuoted and file08Pin pins; those are named here rather "
        f"than described as nothing. {exact_truth} "
        f"preview-product-boundary-successor and every leftover-join lineage cited "
        f"here are different lineages; their version numbers are unrelated.",
        "CLAUDE-PPBS-V9-SF1 (drop 'the whole reason' / 'nothing else is "
        "disturbed', name both D-293 Decision 5 limbs and the other rewritten "
        "fields), CLAUDE-PPBS-V9-B1 (the byte-identity claim becomes the exact "
        "truth), and the standing change: v9's rejection leaves "
        "preview-product-boundary-successor.v8 current")

    doc["basedOn"]["predecessorV7"]["role"] = ledger.rewrite(
        "basedOn.predecessorV7.role",
        v9["basedOn"]["predecessorV7"]["role"],
        v9["basedOn"]["predecessorV7"]["role"].replace(
            f"It is no longer this lineage's predecessor: {PRED8} (D-207) is.",
            f"It is no longer this lineage's predecessor: {PREV9} is, and {PRED8} "
            f"(D-207) remains the lineage's current recording."),
        "the immediate predecessor moved from preview-product-boundary-successor.v8 "
        "to preview-product-boundary-successor.v9")

    doc["basedOn"]["relation"] = ledger.rewrite(
        "basedOn.relation", v9["basedOn"]["relation"],
        f"Land the four Stage A findings on {PREV9} and re-cite the "
        f"{JOIN_COUNT_WORD} current leftover-joins at live HEAD, in basedOn, in "
        f"joinCurrencyAudit, in leftoverDesignOpenStanding and - the defect both "
        f"reviewers named - inside the fourteen enforcement-evidence classes, "
        f"refreshed under {D294} Decision 3. {exact_truth} leftover-design of "
        f"unnamed EE classes remains closed. Cited gate and row leftovers are not "
        f"stolen, and no leftover-design is asserted on a lineage whose current "
        f"join does not carry it. {SPEAKER} existing is not SATISFIED-GRADE and "
        f"does not mark SATISFIED.",
        "the predecessor's relation described the twelve-join re-citation and a "
        "byte-identical class carry; both statements change at v10")

    doc["joinCurrencyAudit"]["standing"] = ledger.rewrite(
        "joinCurrencyAudit.standing", v9["joinCurrencyAudit"]["standing"],
        f"All {JOIN_COUNT_WORD} leftover-join citations {PRED8} (D-207) carried as "
        f"current are superseded. {SPEAKER} re-cites all {JOIN_COUNT_WORD} at the "
        f"versions measured above, in basedOn, in leftoverDesignOpenStanding and in "
        f"enforcementEvidence.classes, the last refreshed under {D294} Decision 3 "
        f"at {site_count} sites and reported in "
        f"enforcementEvidence.classesRefresh. D-293 Decision 5 authorizes two "
        f"limbs, and both are performed: the re-citation, and the statement of the "
        f"relationship to product-boundary-successor-contract.v8 (D-116) in "
        f"lineage.contractRelationship. Beyond those two, {SELF} also adds "
        f"predecessorStanding, joinCurrencyAudit and "
        f"enforcementEvidence.classesRefresh and rewrites doesNot, "
        f"eligibilityNote, findingDisposition, remeasurementClause, "
        f"leftoverDesignOpenStanding and the registerRowQuoted and file08Pin pins. "
        f"{exact_truth}",
        "CLAUDE-PPBS-V9-SF1 ('the whole of this successor's substantive change') "
        "and CLAUDE-PPBS-V9-B1 (the byte-identity claim)")

    doc["authorityClaim"] = ledger.rewrite(
        "authorityClaim", v9["authorityClaim"],
        f"{SPEAKER} PROPOSES the DR-117 preview-scoped successor candidate "
        f"authorized by D-132 / file 12 section 5, and is the candidate limb of the "
        f"DR-117 programme the owner adopted at D-293 Decision 5. Its own history "
        f"is this: preview-product-boundary-successor.v5 was recorded at D-137, "
        f"preview-product-boundary-successor.v6 was rejected at Stage A and never "
        f"recorded, preview-product-boundary-successor.v7 was recorded at D-168, "
        f"{PRED8} was recorded at D-207, and {PREV9} was rejected at Stage A by "
        f"both reviewers and never recorded, so {PRED8} is still the current "
        f"recording. {SPEAKER} exists to do what {PREV9} did incompletely: re-cite "
        f"the {JOIN_COUNT_WORD} leftover-joins {PRED8} named as current at the "
        f"versions live at this dispatch, in the enforcement-evidence classes as "
        f"well as in basedOn, under {D294} Decision 3; and to state the "
        f"relationship to product-boundary-successor-contract.v8 (D-116), the "
        f"second limb D-293 Decision 5 names. {exact_truth} leftover-design of "
        f"unnamed EE classes remains closed (D-157 / D-158 / D-159). {SPEAKER} and "
        f"product-boundary-successor-contract.v8 (D-116, the D-137 leftover T2-02 "
        f"candidate) are distinct lineages: {SELF} does not replace, apply, or "
        f"succeed product-boundary-successor-contract.v8, which remains the D-116 "
        f"recording, and neither of the two is applied. {SPEAKER} does not steal "
        f"OBL-G29-FX-AUTHORING or OBL-G30-FX-AUTHORING; their leftover-design stays "
        f"on the current g29 and g30 leftover-joins cited in basedOn, and {SELF} "
        f"asserts no leftover-design on a lineage whose current join does not carry "
        f"it. {SPEAKER} is not a second register row. {SPEAKER} does not SATISFY "
        f"DR-117. {SPEAKER} does not open D-056 Class A and does not lift D-137's "
        f"express reservation; lifting it is the owner's later act in a reviewed "
        f"coordinator entry, not an act of this successor. {SPEAKER} does not "
        f"author fixture bytes and does not invent the DR-131 pack. {SPEAKER} does "
        f"not treat product-boundary-successor-contract.v8 or "
        f"product-boundary-preview.v2 as SATISFIED. {SPEAKER} does not add a DR-G* "
        f"row, does not change live required-now {REQUIRED_NOW}, does not name G13 "
        f"into required-now, applies nothing, and does not authorize "
        f"docs/v2/implementation/. {SPEAKER} existing is not a SATISFIED-GRADE "
        f"cycle. Gate 1 Class A remains false under D-137's express reservation.",
        "the history gains preview-product-boundary-successor.v9's rejection, the "
        "reason-for-existing sentence names the class-level refresh both reviewers "
        "required, and the byte-identity claim becomes the exact truth")

    doc["purpose"] = ledger.rewrite(
        "purpose", v9["purpose"],
        f"Land the four Stage A findings on {PREV9}. Re-cite, at live HEAD, the "
        f"{JOIN_COUNT_WORD} leftover-joins {PRED8} (D-207) cited at versions since "
        f"superseded, pinning each in basedOn at the version its highest "
        f"non-CONTESTED COORD recording names, with both Stage A verdicts, and "
        f"refreshing the same {JOIN_COUNT_WORD} citations inside the fourteen "
        f"enforcement-evidence classes under {D294} Decision 3. State EE-3a's "
        f"leftoverDesign partition as the current g21 and g23 leftover-joins hold "
        f"it. Hold every other byte of the fourteen classes, the seven dispositions "
        f"and p1p2g3Mapping equal to {PRED8}'s, and assert that equality before "
        f"writing. State in terms the relationship between this preview-scoped "
        f"lineage and product-boundary-successor-contract.v8 (D-116). Re-pin file "
        f"08, file 02, the v1-slice, COORD and HEAD, and recompute every "
        f"recordedInputs digest. Preserve leftover-design of unnamed EE classes as "
        f"closed (D-159: gates 2 and 3 hold). Remainder is named-gate execution. "
        f"Gate 1 Class A remains false under D-137's express reservation until a "
        f"coordinator act supersedes it. Do not SATISFY DR-117. Do not open D-056 "
        f"Class A. Do not author fixture, golden, or adapter bytes. Do not invent a "
        f"new product-boundary item, a D9 code, a section 7.1 recipe, a D-006 unit, "
        f"or the DR-131 pack. Do not name G13 into required-now. Do not steal gate "
        f"leftover-design.",
        "the purpose gains the class-level refresh and the EE-3a partition repair, "
        "and 'carry byte-identically' becomes the narrower held-equal statement")

    doc["eligibilityNote"] = ledger.rewrite(
        "eligibilityNote", v9["eligibilityNote"],
        f"D-159 recorded that D-056 Eligibility gates 2 and 3 hold for DR-117. "
        f"leftover-design of unnamed EE classes is closed. CANDIDATE-NOT-APPLIED is "
        f"not a Class A bar (D-085 / D-147). binds NOTHING is {SELF}'s own status "
        f"field, not a cited holding. Gate 1's application-grade / "
        f"no-express-reservation limb is not established by {SELF}; "
        f"predecessorStanding.stageAGate1Standing recites what the two Stage A "
        f"verdicts on {PRED8} say about that limb in their own shapes, and both "
        f"Stage A verdicts on {PREV9} ruled the D-005 grade question NOT SUSTAINED "
        f"on bytes that {SELF} changes. Gate 1 Class A remains false under D-137's "
        f"express reservation until a coordinator act supersedes it. {SPEAKER} "
        f"existing does not perform Gate 4 SATISFIED-GRADE and does not edit file "
        f"08. Preview is not MVP (D-018). Live required-now is {REQUIRED_NOW}. "
        f"Frozen preview-product-boundary-successor.v7 (D-168) is a historical "
        f"measurement, frozen {PREV9} was rejected at Stage A and never recorded, "
        f"and {PRED8} (D-207) remains the current recorded remasurement until a "
        f"coordinator act records {SELF}.",
        "the closing standing sentence changes: preview-product-boundary-successor."
        "v9 exists, was rejected, and never became current; and the two v9 grade "
        "rulings are named")

    for entry in doc["findingDisposition"]:
        if entry["id"] == "CLAUDE-PPBS-V3-ADV-1":
            entry["venueLimb"] = entry["venueLimb"]  # already retargeted above

    doc["predecessorStanding"] = ledger.rewrite(
        "predecessorStanding", "(v9 object)",
        {
            "currentBeforeThisFileIsRecorded": (
                f"{PRED8} (D-207) is the current recorded DR-117 leftover "
                f"remasurement. {PREV9} was rejected at Stage A by both reviewers "
                f"and never recorded, so it never became current and did not "
                f"displace {PRED8}. {SPEAKER} is CANDIDATE-NOT-APPLIED and records "
                f"nothing; until a reviewed coordinator act records {SELF}, "
                f"{PRED8} stays current."),
            "predecessorV9Standing": (
                f"{PREV9} is frozen at {V9_PATH}, sha256 {v9_sha}, rejected at "
                f"Stage A by both reviewers and unrecorded. It is not current and "
                f"never was. It stays frozen; do not record it. Its four findings "
                f"and its advisory are disposed of in findingDisposition."),
            "effectOfRecordingThisFile": (
                f"Once {SELF} is recorded, {PRED8} becomes a historical measurement "
                f"as of HEAD {v8['head']} / required-now "
                f"{v8['requiredNowUnchanged']} / file 08 "
                f"{v8['file08Pin']['sha256']}, and is no longer the current DR-117 "
                f"leftover remasurement. {PRED8} stays frozen; it is not to be "
                f"recorded as current after that act. Nothing in {SELF} unwrites "
                f"D-207."),
            "predecessorV7Standing": v9["predecessorStanding"]["predecessorV7Standing"],
            "earlierStanding": v9["predecessorStanding"]["earlierStanding"],
            "versionNumbers": v9["predecessorStanding"]["versionNumbers"],
            "stageAGate1Standing": doc["predecessorStanding"]["stageAGate1Standing"],
        },
        "preview-product-boundary-successor.v9's rejection is recorded: it never "
        "became current, and preview-product-boundary-successor.v8 stays current "
        "until this successor is recorded")

    doc["doesNot"][13] = ledger.rewrite(
        "doesNot[13]", v9["doesNot"][13],
        f"Does not record frozen preview-product-boundary-successor.v7 or frozen "
        f"{PREV9} as a current leftover remasurement, and does not record frozen "
        f"{PRED8} as a current one either once {SELF} is recorded.",
        "preview-product-boundary-successor.v9 joins the frozen-and-not-current "
        "list")

    # ---- findingDisposition: the four Stage A findings plus the advisory --
    new_dispositions = [
        {
            "id": "CLAUDE-PPBS-V9-B1",
            "severity": "BLOCKER",
            "disposition": (
                f"landed at {SELF}: the forty present-tense cross-lineage currency "
                f"citations inside enforcementEvidence.classes[*].existingGate and "
                f"enforcementEvidence.classes[*].laterExecution are refreshed under "
                f"{D294} Decision 3 to the {JOIN_COUNT_WORD} versions current at "
                f"this dispatch, by a mechanical rewrite of the version token and "
                f"the recording D-number only; and the five byte-identity claims "
                f"that covered them are restated as the exact truth. "
                f"enforcementEvidence.classesRefresh reports the site count and the "
                f"class-equality assertion."),
            "riderNotLanded": (
                f"CLAUDE-PPBS-V9-B1 carries a rider, expressly not separately "
                f"counted, asking that the thirty-four deictic occurrences of "
                f"\"This successor\" inside the fourteen classes be aligned with "
                f"the speaker form used elsewhere. {SELF} does not land it: the "
                f"change authorized here is the currency refresh, and the "
                f"class-equality assertion in enforcementEvidence.classesRefresh "
                f"is what proves nothing else moved. Aligning those thirty-four "
                f"sites would break that proof and is left to a later successor or "
                f"a reviewer's direction."),
            "landedAt": [
                "enforcementEvidence.classes", "enforcementEvidence.classesRefresh",
                "basedOn.predecessorV8.role", "basedOn.relation", "authorityClaim",
                "purpose", "joinCurrencyAudit.standing",
            ],
        },
        {
            "id": "CLAUDE-PPBS-V9-B2",
            "severity": "BLOCKER",
            "disposition": (
                f"landed at {SELF}: EE-3a's leftoverDesign sentence now states the "
                f"measured partition - [OBL-G21-FX-AUTHORING] on g21 "
                f"leftover-join.v{g21['version']} ({g21['recording']}), and g23 "
                f"leftover-join.v{g23['version']} ({g23['recording']}) flags no "
                f"obligation leftoverDesign true - which is what "
                f"basedOn.g23JoinV{g23['version']}.role and "
                f"leftoverDesignOpenStanding already said."),
            "landedAt": [
                "enforcementEvidence.classes EE-3a.existingGate",
                "enforcementEvidence.classes EE-3a.laterExecution",
            ],
        },
        {
            "id": "CLAUDE-PPBS-V9-SF1",
            "severity": "SHOULD-FIX",
            "disposition": (
                f"landed at {SELF}: basedOn.predecessorV8.role and "
                f"joinCurrencyAudit.standing name both D-293 Decision 5 limbs - the "
                f"{JOIN_COUNT_WORD}-join re-citation and the "
                f"product-boundary-successor-contract.v8 relationship - and list "
                f"the other fields this successor adds or rewrites instead of "
                f"saying nothing else is disturbed."),
            "landedAt": ["basedOn.predecessorV8.role", "joinCurrencyAudit.standing"],
        },
        {
            "id": "PPBSV9-B1",
            "severity": "BLOCKER",
            "disposition": (
                f"landed at {SELF}: the same forty sites are refreshed in place "
                f"rather than delimited as a non-operative historical snapshot, so "
                f"the operative CELL-2 routing names the {JOIN_COUNT_WORD} current "
                f"joins; and the broad byte-identity assertions are narrowed to the "
                f"exact truth and proved by the class-equality assertion. The "
                f"required re-review against this successor's final digest is a "
                f"later act (D-293 Decision 5), not something {SELF} performs."),
            "landedAt": [
                "enforcementEvidence.classes", "enforcementEvidence.classesRefresh",
                "basedOn.relation", "authorityClaim", "purpose",
                "joinCurrencyAudit.standing",
            ],
        },
        {
            "id": "CLAUDE-PPBS-V9-ADV-1",
            "severity": "ADVISORY",
            "disposition": (
                f"ACCEPTED as honesty, landed at {SELF}: joinCurrencyAudit.method "
                f"quotes the heading form with the em dash live COORD headings use, "
                f"so the quoted form matches the headings it describes."),
            "landedAt": ["joinCurrencyAudit.method"],
        },
    ]
    ledger.new("findingDisposition CLAUDE-PPBS-V9-B1 / -B2 / -SF1 / PPBSV9-B1 / "
               "CLAUDE-PPBS-V9-ADV-1",
               [d["id"] for d in new_dispositions],
               "the four Stage A findings on preview-product-boundary-successor.v9 "
               "and the advisory raised with them")
    doc["findingDisposition"] = new_dispositions + doc["findingDisposition"]

    # ---- recordedInputs ---------------------------------------------------
    pinned = {}

    def collect(node):
        if isinstance(node, dict):
            for key_path, key_sha in (("path", "sha256"),
                                      ("sourcePath", "sourceSha256")):
                if isinstance(node.get(key_path), str) and \
                        isinstance(node.get(key_sha), str):
                    pinned[node[key_path]] = node[key_sha]
            for value in node.values():
                collect(value)
        elif isinstance(node, list):
            for value in node:
                collect(value)

    collect(doc)
    pinned[COORD] = sha256_file(COORD)
    for path in v9["recordedInputs"]:
        if path == "HEAD":
            continue
        pinned.setdefault(path, sha256_file(path))
    for path in (V9_PATH, V9_REVIEW_CLAUDE, V9_REVIEW_CODEX):
        pinned[path] = sha256_file(path)
    for path, sha in sorted(pinned.items()):
        actual = sha256_file(path)
        need(actual == sha,
             f"pinned digest for {path} does not recompute: document says {sha}, "
             f"bytes are {actual}")
    recorded_inputs = {path: pinned[path] for path in sorted(pinned)}
    recorded_inputs["HEAD"] = head
    for path in v9["recordedInputs"]:
        need(path in recorded_inputs,
             f"the predecessor pinned {path} and this successor drops it")
    for path in (V9_PATH, V9_REVIEW_CLAUDE, V9_REVIEW_CODEX):
        need(path in recorded_inputs, f"{path} is not pinned in recordedInputs")
    doc["recordedInputs"] = ledger.rewrite(
        "recordedInputs", f"{len(v9['recordedInputs'])} entries",
        recorded_inputs,
        "regenerated; the rejected predecessor and both its Stage A verdicts are "
        "added, and every digest is recomputed at run time")

    doc["remeasurementClause"] = ledger.rewrite(
        "remeasurementClause", v9["remeasurementClause"],
        f"If any file pinned in recordedInputs moves in a way that is not "
        f"append-only growth of {COORD} or COORD heading hygiene, re-measure before "
        f"recording. The trigger reaches every one of the "
        f"{len(recorded_inputs) - 1} pinned rows, not an enumerated subset: this "
        f"clause is generated from recordedInputs rather than maintained by "
        f"addition. recordedInputs.HEAD must equal the top-level head. "
        f"file08Pin.sha256, registerRowQuoted.sourceSha256 and "
        f"recordedInputs[{FILE08!r}] must all equal the same live digest of file "
        f"08, and DR-117's leading label there must still be {status_token}. "
        f"sevenItems.sourceSha256 must still equal the live digest of {FILE02}; "
        f"file 08's DR-117 row says any change to that enumeration re-opens the "
        f"row. Each of the {JOIN_COUNT_WORD} current leftover-joins named in "
        f"basedOn and cited in enforcementEvidence.classes must still be the "
        f"version its highest non-CONTESTED COORD recording names; if a later "
        f"recording supersedes one, re-measure and refresh both places before "
        f"recording, under {D294} Decision 3. {SPEAKER} does not unwrite D-137, "
        f"D-157, D-158, D-159, D-167, D-168, D-169, or any entry from D-170 through "
        f"D-{highest_coord}. Frozen preview-product-boundary-successor.v7 remains a "
        f"historical measurement as of HEAD "
        f"5d5d77819ae3019d9e6e02f1e66de3d93c060402 / required-now 26. {SPEAKER} "
        f"existing is not a recording.",
        "the pinned-row count changes, the class citations join the currency "
        "condition, and the speaker moves")

    # ---- final assertions -------------------------------------------------
    need(doc["recordedInputs"]["HEAD"] == doc["head"],
         "recordedInputs.HEAD does not equal the top-level head")
    need(doc["recordedInputs"][FILE08] == doc["file08Pin"]["sha256"]
         == doc["registerRowQuoted"]["sourceSha256"],
         "the three file-08 pins disagree")
    for key, expected in (("status", "CANDIDATE-NOT-APPLIED"),
                          ("reviewStatus", "AWAITING-INDEPENDENT-REVIEW"),
                          ("binds", "NOTHING"),
                          ("sealRecommendation", "DO-NOT-SEAL"),
                          ("registerRow", REGISTER_ROW)):
        need(doc[key] == expected, f"{key} is not {expected}")
    need(len(doc["enforcementEvidence"]["classes"]) == 14, "not fourteen EE classes")
    need(len(doc["sevenItems"]["dispositions"]) == 7, "not seven dispositions")
    need(len(doc["joinCurrencyAudit"]["joins"]) == 12, "not twelve joins")
    need(PREV9 not in json.dumps(doc["enforcementEvidence"]["classes"]),
         "the classes name the rejected predecessor")

    # the whole document must now be free of stale currency and of v9 speakers
    leftover_speakers = []
    for path, text in _strings(doc):
        if f"This {PREV9}" in text:
            leftover_speakers.append(path)
    need(not leftover_speakers,
         "these fields still speak as preview-product-boundary-successor.v9: "
         + ", ".join(leftover_speakers))

    findings = audit_document(doc, current)
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
        print(f"  refreshed sites {site_count} "
              f"(40 currency citations + 2 EE-3a partition sentences)")
        print(f"  classes equal v8 after normalization: {classes_equal}")

    return doc, payload, refreshed_sites, classes_equal, v9, current


def _strings(node, path="$"):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _strings(value, f"{path}.{key}")
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from _strings(value, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


def build_audit(doc, payload, sites, classes_equal, v9, current, ledger, out_path):
    by_lineage = {}
    for site in sites:
        if site["kind"] != "currency-citation":
            continue
        by_lineage[site["lineage"]] = by_lineage.get(site["lineage"], 0) + 1
    return {
        "generator": os.path.basename(os.path.abspath(__file__)),
        "generatedAt": doc["date"],
        "head": doc["head"],
        "predecessor": {"path": V9_PATH, "sha256": V9_SHA256,
                        "standing": "rejected at Stage A, never recorded"},
        "stageAFindingsLanded": ["CLAUDE-PPBS-V9-B1", "CLAUDE-PPBS-V9-B2",
                                 "CLAUDE-PPBS-V9-SF1", "PPBSV9-B1",
                                 "CLAUDE-PPBS-V9-ADV-1"],
        "output": {
            "path": out_path,
            "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
            "bytes": len(payload.encode("utf-8")),
        },
        "refreshRule": D294_REFRESH_RULE,
        "refreshedSites": {
            "total": len(sites),
            "currencyCitations": sum(1 for s in sites
                                     if s["kind"] == "currency-citation"),
            "leftoverDesignPartition": sum(1 for s in sites
                                           if s["kind"] == "leftoverDesign-partition"),
            "currencyCitationsByLineage": by_lineage,
            "sites": sites,
        },
        "currentVersions": {lin: {"version": v, "recording": r}
                            for lin, (v, r) in sorted(current.items())},
        "classEqualityAssertion": {
            "statement": "after normalizing the refreshed citation tokens and the "
                         "EE-3a leftoverDesign partition sentence in both, v10's "
                         "fourteen classes equal v8's fourteen classes",
            "result": classes_equal,
        },
        "rewrittenFields": ledger.rewritten,
        "carriedFields": ledger.carried,
        "newFields": ledger.added,
        "counts": {
            "rewritten": len(ledger.rewritten),
            "carried": len(ledger.carried),
            "new": len(ledger.added),
            "recordedInputsPredecessor": len(v9["recordedInputs"]),
            "recordedInputsSuccessor": len(doc["recordedInputs"]),
            "findingDispositionPredecessor": len(v9["findingDisposition"]),
            "findingDispositionSuccessor": len(doc["findingDisposition"]),
        },
        "auditRules": [
            "no sentence of the inverted currency form or the remain-on form names "
            "a leftover-join version other than the current one for that lineage",
            "no byte-identity claim about the enforcement-evidence classes",
            "no deictic version self-reference matching 'This v<digit>'",
            "no bare version token outside the record's fixed docs/ path forms",
            "no unsubstituted brace token",
            "no field still speaks as preview-product-boundary-successor.v9",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("output", nargs="?", default=DEFAULT_OUT_DIR)
    parser.add_argument("--audit", metavar="PATH")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    out = args.output
    out_path = out if out.endswith(".json") else os.path.join(out, OUT_BASENAME)

    ledger = Ledger()
    try:
        docs_root = os.path.abspath(os.path.join(os.getcwd(), "docs"))
        need(os.path.abspath(out_path) != docs_root
             and not os.path.abspath(out_path).startswith(docs_root + os.sep),
             "refusing to write under docs/: that tree is a frozen provenance record")
        parent = os.path.dirname(os.path.abspath(out_path))
        if not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)
        doc, payload, sites, classes_equal, v9, current = build(
            out_path, ledger, args.quiet)
    except Fail as exc:
        print(f"make-ppbs-v10.py: FAILED: {exc}", file=sys.stderr)
        return 2

    if args.audit:
        audit = build_audit(doc, payload, sites, classes_equal, v9, current,
                            ledger, out_path)
        with open(args.audit, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(audit, indent=2, ensure_ascii=False) + "\n")
        if not args.quiet:
            print(f"wrote {args.audit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
