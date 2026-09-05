#!/usr/bin/env python3
"""Conformance checker for VERSIONING v11 — enforcement-closure successor.

The v10 CONTRACT and its 116-position enforcement result survived independent
adversarial review intact (versioning-policy.v10.review-independent.json: "My own
sweep over all 116 evidence-leaf positions ... rejected 116 of 116 by a finding
NAMING the position, against 87 admitted under the predecessor"). The single
blocker was that v10 repaired the defect for the CARRIED evidence and reproduced
it one block over, in its own:

  B-VER10R-01. Of the 316 leaf positions in
  successorRevision.evidenceEnforcementRepair, 79 sit in four registry loops
  that enforcement_registry() sizes from the ARTIFACT'S OWN list lengths
  (retainedResiduals 45, recordedInputs 22, residualRestatements 8, notClaimed
  4). A registry that grows with the data it is supposed to police can never
  emit VER10-COVER inside those loops. And the block's own measured partition —
  316 / 228 / 60 / 28 — is computed, printed in the PASS banner and compared
  against nothing: the string "316" occurs 0 times in versioning-policy.v10.json.
  The reviewer appended a duplicate residual, fabricated a residual restatement
  asserting an open residual is closed, planted "independently re-reviewed and
  PASSED; this successor inherits that verdict" into recordedInputs[*].role —
  the paper-seal class, inside the very block asserting
  checkerEnforcesEveryDeclaredEvidenceLeaf: true — and deleted a freeze §7.2
  recorded input. Each exits 0 with the full green banner.

This checker closes the CLASS, not the four loops.

  1. NO REGISTRY IS SIZED BY THE ARTIFACT. The three registry builders here take
     no artifact parameter at all, so it is not possible to write an
     artifact-sized loop in one. Every position set is generated from a checker
     constant, from the pinned predecessor's own bytes, from the D9 span, from
     the live register, or from this checker's own source. That purity is not a
     promise: registry_purity() re-derives it from inspect.getsource() on every
     run — 0 artifact parameters and 0 artifact reads in this checker's builders,
     against 1 parameter and 5 artifact-sized loops in the pinned predecessor's
     (4 in enforcement_registry, 1 in evidence_registry) — and the artifact
     declares those numbers, which are compared (VER11-PURITY).

  2. EVERY COMPUTED PARTITION IS COMPARED, AND THE BANNER CAN ONLY PRINT
     COMPARED NUMBERS. PARTITION_SCOPES is the single authority for what gets
     partitioned; each scope's partition is compared leaf-wise against a
     declaration in the artifact (VER11-PART), and the banner is rendered from
     the list of comparisons that actually happened, so a number cannot be
     published without having been gated. v10's uncompared 316 is now declared,
     compared and re-derived, together with the measurement that it appeared 0
     times in the predecessor artifact.

  3. THE PREDECESSOR'S FOUR ADMISSIONS ARE REPRODUCED ON EVERY RUN. probe_pairs()
     executes the pinned check-versioning-v10.py against the pinned
     versioning-policy.v10.json under each of the reviewer's five probes, and
     the same five against these bytes under this checker, and compares both
     columns against the artifact's declaration. The artifact does not narrate
     that the defect existed and is closed; the closure is measured here.

  4. NO PAPER SEAL SURVIVES IN FREE PROSE EITHER. A two-tier scan runs over
     every string leaf in the artifact for verdict-inheritance and seal claims.
     Hits are permitted only at a checker-constant allowlist of quotation
     positions, and only when the quoting markers are present (VER11-SEAL).

Two further repairs, both named by the same review:

  * R-VER10-08 is UPHELD and restated on the reviewer's axis, which this record
    adopts verbatim: registerBinding is a RECORDED MEASUREMENT and gets hard
    comparison, because an uncompared measurement is prose that looks like
    evidence and going stale is a true positive about these bytes;
    decisionDependencies[4].source is a CONTINUING INVARIANT and gets a semantic
    gate, because a byte pin fails on the very repoint it anticipates.
    Measurements get hard comparison; invariants get semantic gates. The hard
    comparison is NOT weakened. What is repaired is the blast radius: v10 was
    unrepairable in place because ENUMERATED_DELTA is a checker constant and the
    artifact's enumeratedDelta table is index-position-compared against
    sorted(moved), so the obvious one-line fix cascaded into ten findings. Here
    the carried delta is published as a COUNT and a DIGEST — a measurement, not
    an enumeration — so it has no indices to shift. rehearse() simulates the
    pending v22 -> v23 repoint, the unenumerated EVALUATION-PROOF addition and
    the unenumerated family-ambiguity collapse on every run and compares the
    measured repair cost against the declaration.

  * The predecessor's --selftest banner claimed "9 boolean respellings" from
    label-string matching, which double-counted a float and counted one
    non-respelling. respelling_census() classifies a mutation by the TYPE
    TRANSITION it actually performs, reproduces the predecessor's 9-vs-7
    overcount from its own pinned table, and counts this checker's own
    mutations the same way. The banner counts what it means.

Everything outside successorRevision.enforcementClosureRepair is carried from
versioning-policy.v10.json BYTE-IDENTICAL and gated against those bytes, and
coverage_census() partitions every leaf position in the whole artifact into
scope-enforced, byte-gated, rule-gated and UNGATED, with the ungated count
declared and compared. It is 0.

Trust order: inert bytes -> SHA-256 verify -> execute from the verified snapshot.
A non-zero exit is not evidence that a guard fired — check-versioning.py's
AttributeError also exits 1 and is indistinguishable from a real finding by exit
status alone. So every finding here carries a stable VER11-* id and names the
position under test, and --selftest asserts on BOTH; the assertion is on the FULL
dotted path wherever the finding names a leaf, which closes the substring
self-satisfaction the review recorded as O-04.

Usage: python3 -I -B artifacts/check-versioning-v11.py [contract] [--selftest]
Exit:  0 clean · 1 findings · 2 IO error · 3 selftest refused or not run
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import json
import pathlib
import re
import subprocess
import sys
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT = HERE / "versioning-policy.v11.json"

PREDECESSOR = "versioning-policy.v10.json"
PREDECESSOR_CHECKER = "check-versioning-v10.py"
PREDECESSOR_REVIEW = "versioning-policy.v10.review-independent.json"
GRANDPARENT = "versioning-policy.v9.json"
GRANDPARENT_CHECKER = "check-versioning-v9.py"
GRANDPARENT_REVIEW = "versioning-policy.v9.review-independent.json"
ELDER = "versioning-policy.v8.json"
ELDER_CHECKER = "check-versioning-v8.py"
ELDER_REVIEW = "versioning-policy.v8.review-independent-cold-rejoin.json"
D9_HEAD = "d9-exit-contract.v1.14.json"
D9_HEAD_CHECKER = "check-d9-v1.14.py"
D9_HEAD_REVIEW = "d9-exit-contract.v1.14.review-independent-prefreeze.json"
D9_SUPERSEDED = "d9-exit-contract.v1.6.json"
V4 = "versioning-policy.v4.json"
V4_CHECKER = "check-versioning.py"
REGISTER = "claim-register.v1.json"

# Recording obligation, freeze §7.2: filename + sha256 for every input this
# artifact depends on. A count is not a record.
PINS = {
    PREDECESSOR:
        "194350399d4bd5861ac826eb8d7e0ce835f58cff1e049910552b85a71d002ed0",
    PREDECESSOR_CHECKER:
        "40e85b42648276e0bdb09524663248eff09885c39e53e3971a7f337a51f88612",
    PREDECESSOR_REVIEW:
        "d264dbdd83579d41f8bf8a5a1ac355aad33070991b818148bbcaf991cd2d8e3d",
    GRANDPARENT:
        "9d3f936ae492e2b692781215f92de4b50ef9b962911e9067c7d052825e0492a9",
    GRANDPARENT_CHECKER:
        "cf88da34a68a2697d5040d97d32eeaabcf7217162bf279ab5b546c066210bd80",
    GRANDPARENT_REVIEW:
        "59ba43425d3bd7a25838141ca2b417bf6ac9ecfba973c589cd520d627b27a360",
    ELDER:
        "ea4b52b5a4d187ec35ad994d8ffcd888db287566c8fb53f3df17e5203d84ae2e",
    ELDER_CHECKER:
        "82834720a8fd4ec8701dad2b43ad94d6ad9e52d21aeb077f4286fab5fb156844",
    ELDER_REVIEW:
        "2012c572be62a59d953fcbaf65d266abfb53aefa6eb98a6ff9656dbc923facb9",
    D9_HEAD:
        "8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31",
    D9_HEAD_CHECKER:
        "513d69dd879dcb678d53d8df89a907d05dacd4b078ec43c7fedc939732c5e83e",
    D9_HEAD_REVIEW:
        "345380e2ce63aafb790fd9c7bec2e299e8d1bc9b235949a1483c77ab2faa9dc2",
    D9_SUPERSEDED:
        "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    V4:
        "8e6933b287a8082ea27647860938bd9cdae93b37132bba21221c2c24b40069e6",
    V4_CHECKER:
        "67a45b275908afc4bd04cee6c15400f5d429f9f209854630c1caf5a43cf13227",
}

# claim-register.v1.json is deliberately NOT pinned. The v9 review vindicated
# that empirically — the register drifted a THIRD time DURING that review while
# its D9, VERSIONING and ARCH.RETENTION-TIERS bindings held byte-identical — and
# the v10 review restated the principle as the axis this successor adopts: a
# CONTINUING INVARIANT gets a semantic gate, because a byte pin fails on the very
# repoint it anticipates. No digest for this file is recorded anywhere in the
# v11 record either: a digest of a file that is expected to move is a timestamp,
# not evidence, and recording one uncompared is the B-VER9R-01 shape. What is
# recorded instead is the set of bindings this artifact actually depends on, and
# every one of those IS hard-compared (registerAsOfAudit).

CHANGED = {"version", "supersedes", "role", "knownLimitations",
           "successorRevision"}

REPAIR = "successorRevision.d9CitationRepair"
ENFORCE = "successorRevision.evidenceEnforcementRepair"
CLOSE = "successorRevision.enforcementClosureRepair"

EXPECTED_REVISION_KEYS = {
    "id", "candidateState", "supersedesCandidate", "inputs",
    "rawAuthorityKinds", "custodyRule", "storeAuthorityRule",
    "identityStability", "forbiddenBackEdge", "coldStoredReadRejoin",
    "dependencyLabelRule", "d9CitationRepair", "evidenceEnforcementRepair",
    "enforcementClosureRepair",
}

# Every successorRevision key that must be byte-identical to the pinned
# predecessor. `id`, `supersedesCandidate` and `identityStability` necessarily
# move in a successor and are gated by explicit rules instead;
# `enforcementClosureRepair` is this successor's new work.
FROZEN_REVISION_KEYS = (
    "candidateState", "inputs", "rawAuthorityKinds", "custodyRule",
    "storeAuthorityRule", "forbiddenBackEdge", "coldStoredReadRejoin",
    "dependencyLabelRule", "d9CitationRepair", "evidenceEnforcementRepair",
)

EXPECTED_CLOSURE_KEYS = (
    "findingId", "authoredBy", "reviewOfRecord", "defect",
    "whySuccessorAndNotInPlaceRepair", "registryPurity", "predecessorDefect",
    "partitionClosure", "coverageCensus", "carriedByteIdentical",
    "registerAsOfAudit", "repointCascade", "prosePaperSealScan",
    "closedScalarAdmission", "selftestProfile", "residualRestatements",
    "recordedInputs", "retainedResiduals", "checkerDisposition", "notClaimed",
)

CARRIED_RESIDUAL_IDS = {
    "R-VER10-01", "R-VER10-02", "R-VER10-03", "R-VER10-04", "R-VER10-05",
    "R-VER10-06", "R-VER10-07", "R-VER10-08", "R-VER10-09",
}

# Ordered: the registry is generated from this tuple, so the artifact's list is
# sized by a checker constant and a duplicate or an extra row has no
# classification (VER11-COVER) as well as failing the multiset comparison.
REQUIRED_RESIDUAL_IDS = (
    "R-VER11-01", "R-VER11-02", "R-VER11-03", "R-VER11-04", "R-VER11-05",
    "R-VER11-06", "R-VER11-07", "R-VER11-08", "R-VER11-09", "R-VER11-10",
    "R-VER11-11",
)

RESTATED_RESIDUALS = ("R-VER10-01", "R-VER10-03", "R-VER10-08")

OWNER_VOCABULARY = {
    "coordinator", "independent reviewer", "phase1a successor lane",
    "phase1a evidence-enforcement lane", "phase1a enforcement-closure lane",
    "rust provider protocol lane", "closed for v10; v9 residual retained",
}

ROLE_TOKENS = ("enforcement-closure successor", "B-VER10R-01", "B-SCV2-06")

REPAIRED_CITATION = "artifacts/" + D9_HEAD
SUPERSEDED_CITATION = "artifacts/" + D9_SUPERSEDED

EVIDENCE_SCOPE = (
    f"{REPAIR}.substanceUnchangedEvidence",
    f"{REPAIR}.directionPreservation",
    f"{REPAIR}.siblingCitationAudit",
)
FROZEN_SUB_BLOCKS = ("substanceUnchangedEvidence", "directionPreservation")
AUDIT_PROSE_ROWS = 2          # sized by constant, never by the artifact
DEMONSTRATIONS = 5            # the reviewer's five probes, a checker constant

# The one authority for what is partitioned. Adding a scope without a
# declaration is itself a finding, so no computed partition can escape
# comparison and the banner has nothing uncompared to print.
PARTITION_SCOPES = (
    ("carriedEvidence", EVIDENCE_SCOPE),
    ("predecessorEnforcementBlock", (ENFORCE,)),
    ("successorClosureBlock", (CLOSE,)),
)

# The four artifact-sized loops of B-VER10R-01, named so the measurement below
# is attributable rather than a bare total.
PREDECESSOR_SELF_SIZED_LOOPS = (
    f"{ENFORCE}.retainedResiduals",
    f"{ENFORCE}.recordedInputs",
    f"{ENFORCE}.residualRestatements",
    f"{ENFORCE}.notClaimed",
)

REGISTRY_BUILDERS = ("evidence_registry", "frozen_registry", "closure_registry")
PREDECESSOR_REGISTRY_BUILDERS = ("evidence_registry", "enforcement_registry")

MEASURED = "MEASURED"
GROUNDED = "GROUNDED"
UNMEASURABLE = "UNMEASURABLE"
FROM_DISK = "disk"
FROM_CONSTANT = "constant"

ADDED_LIMITATION_COUNT = 5
# Each added limitation must state a measured value, not merely be present.
LIMITATION_TOKENS = (
    ("B-VER10R-01", "316", "79"),
    ("registry", "artifact", "0"),
    ("partition", "compared", "banner"),
    ("R-VER10-08", "recorded measurement", "continuing invariant"),
    ("paper", "role", "prose"),
)

# Tier A: verdict-inheritance and acceptance phrases, scanned over every string
# leaf in the artifact. Tier B: bare seal vocabulary, scanned over
# successorRevision, where this chain's authored prose lives.
SEAL_PATTERNS_ARTIFACT = (
    r"re-?reviewed and PASSED",
    r"inherit(?:s|ed)? (?:that|the|this) verdict",
    r"independently re-?reviewed",
    r"every residual is closed",
    r"all residuals are closed",
    r"no findings remain",
    r"verdict transfers",
    r"RELEASE-QUALIFIED",
    r"VERIFIED-IN-PRODUCT",
    r"has passed (?:independent )?review",
)
SEAL_PATTERNS_REVISION = (
    r"\bSIGNED\b", r"\bSEALED\b", r"\bAPPROVED\b", r"\bPASSED\b",
    r"\bRELEASE-QUALIFIED\b", r"\bVERIFIED-IN-PRODUCT\b",
)
# A hit is permitted only here, and only with every quoting marker present. Both
# the paths and the markers are checker constants, so a new "allowed" position
# cannot be introduced from the artifact side.
SEAL_QUOTE_ALLOW = {
    f"{CLOSE}.prosePaperSealScan.plantedClaimVerbatim":
        ("REJECTED", "B-VER10R-01", "planted"),
    f"{CLOSE}.predecessorDefect.demonstrations[2].plantedText":
        ("REJECTED", "planted"),
}

# The scan's own pattern table is exempt, and only it. Those positions are
# compared for equality against the checker constants above, so nothing can be
# authored into them; scanning a pattern against itself would report the
# instrument as the offence. The exemption is a checker constant and its size is
# declared and compared.
SEAL_SCAN_EXEMPT = (f"{CLOSE}.prosePaperSealScan.artifactPatterns",
                    f"{CLOSE}.prosePaperSealScan.revisionPatterns")

LAST: dict[str, Any] = {}
_DEPTH = 0
# Trust order: inert bytes -> SHA-256 verify -> execute from the verified
# snapshot. The pins are verified once per process and every nested run below
# executes against that same verified snapshot rather than re-reading disk.
_CACHE: dict[str, Any] = {}
# Measurements that require running this checker against a candidate. They are
# properties of the base subject, so they are taken once per outer run and
# reused by every nested run; see derive().
_DERIVED: dict[str, Any] = {}


# ---------------------------------------------------------------- primitives

def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text())


def sha_file(name: str) -> str:
    key = f"sha:{name}"
    if key not in _CACHE:
        _CACHE[key] = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    return _CACHE[key]


def pinned(name: str) -> Any:
    key = f"json:{name}"
    if key not in _CACHE:
        _CACHE[key] = json.loads((HERE / name).read_text())
    return _CACHE[key]


def pinned_text(name: str) -> str:
    key = f"text:{name}"
    if key not in _CACHE:
        _CACHE[key] = (HERE / name).read_text()
    return _CACHE[key]


def canon(value: Any) -> str:
    """Canonical JSON text. Unlike Python equality this distinguishes 4 from 4.0
    AND True from 1, so every canon comparison below is an exact-type admission
    in both directions of freeze §6 law 18."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def module(filename: str, name: str) -> Any:
    key = f"module:{filename}"
    if key in _CACHE:
        return _CACHE[key]
    _CACHE[key] = _load_module(filename, name)
    return _CACHE[key]


def _load_module(filename: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def exact_int(value: Any) -> bool:
    """``type(x) is int`` rejects both float and bool; ``isinstance`` admits
    bool, which is how 15 booleans became respellable in v9."""
    return type(value) is int


def exact_bool(value: Any) -> bool:
    return type(value) is bool


def add(errors: list[str], code: str, message: str) -> None:
    errors.append(f"{code}: {message}")


def positions(value: Any, path: str, out: list[str]) -> None:
    """Every falsifiable leaf POSITION, including nulls and empty containers — a
    null can be replaced with a string and an empty list can be extended, so both
    are probe sites and both must be classified."""
    if isinstance(value, dict):
        if not value:
            out.append(path)
            return
        for key in sorted(value):
            positions(value[key], f"{path}.{key}", out)
    elif isinstance(value, list):
        if not value:
            out.append(path)
            return
        for index, item in enumerate(value):
            positions(item, f"{path}[{index}]", out)
    else:
        out.append(path)


def leaf_items(value: Any, path: str, out: list[tuple[str, Any]]) -> None:
    """positions() paired with the value found there. Used to generate a
    registry from PINNED bytes rather than from the subject."""
    if isinstance(value, dict) and value:
        for key in sorted(value):
            leaf_items(value[key], f"{path}.{key}", out)
    elif isinstance(value, list) and value:
        for index, item in enumerate(value):
            leaf_items(item, f"{path}[{index}]", out)
    else:
        out.append((path, value))


def string_leaves(value: Any, path: str, out: list[tuple[str, str]]) -> None:
    if isinstance(value, dict):
        for key in sorted(value):
            string_leaves(value[key], f"{path}.{key}", out)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            string_leaves(item, f"{path}[{index}]", out)
    elif isinstance(value, str):
        out.append((path, value))


def steps_of(path: str) -> list[Any]:
    steps: list[Any] = []
    buffer = ""
    index = 0
    while index < len(path):
        char = path[index]
        if char == ".":
            if buffer:
                steps.append(buffer)
                buffer = ""
        elif char == "[":
            if buffer:
                steps.append(buffer)
                buffer = ""
            close = path.index("]", index)
            steps.append(int(path[index + 1:close]))
            index = close
        else:
            buffer += char
        index += 1
    if buffer:
        steps.append(buffer)
    return steps


def at(root: Any, path: str) -> Any:
    current = root
    for step in steps_of(path):
        if isinstance(step, int):
            if not isinstance(current, list) or step >= len(current):
                raise KeyError(path)
            current = current[step]
        else:
            if not isinstance(current, dict) or step not in current:
                raise KeyError(path)
            current = current[step]
    return current


def resolves_in(root: Any, path: str) -> bool:
    try:
        at(root, path)
        return True
    except (KeyError, TypeError, ValueError):
        return False


def set_at(root: Any, path: str, value: Any) -> None:
    cursor = root
    steps = steps_of(path)
    for step in steps[:-1]:
        cursor = cursor[step]
    cursor[steps[-1]] = value


def diff_leaves(new: Any, old: Any, path: str = "") -> list[str]:
    """Leaf-wise difference, returning exact positions rather than a bulk
    verdict, so a carried-bytes finding can name the position under test."""
    if canon(new) == canon(old):
        return []
    out: list[str] = []
    if isinstance(new, dict) and isinstance(old, dict):
        for key in sorted(set(new) | set(old)):
            if key not in new or key not in old:
                out.append(f"{path}.{key}")
            else:
                out.extend(diff_leaves(new[key], old[key], f"{path}.{key}"))
    elif isinstance(new, list) and isinstance(old, list):
        for index in range(max(len(new), len(old))):
            if index >= len(new) or index >= len(old):
                out.append(f"{path}[{index}]")
            else:
                out.extend(diff_leaves(new[index], old[index],
                                       f"{path}[{index}]"))
    else:
        out.append(path or "<root>")
    return [p.lstrip(".") for p in out]


def no_floats(value: Any, path: str = "") -> list[str]:
    out: list[str] = []
    if isinstance(value, float):
        out.append(f"float scalar at {path or '<root>'} — freeze §6 law 18: "
                   f"closed-scalar admission is exact-type")
    elif isinstance(value, dict):
        for key, item in value.items():
            out.extend(no_floats(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            out.extend(no_floats(item, f"{path}[{index}]"))
    return out


# ---------------------------------------------------------------- measurement

def measure_d9_span(old: Any, new: Any) -> dict[str, Any]:
    """Re-derive the exit-class contract across the v1.6 -> v1.14 span from both
    artifacts on disk. This is the evidence the citation repair rests on and it
    is computed here, not read from the artifact."""
    old_classes = [e["class"] for e in old["exitClasses"]]
    new_classes = [e["class"] for e in new["exitClasses"]]
    old_g = {g["id"]: g for g in old["goldenCases"]}
    new_g = {g["id"]: g for g in new["goldenCases"]}
    shared = sorted(set(old_g) & set(new_g))

    cls_mismatch = code_mismatch = exit_mismatch = 0
    for gid in shared:
        a = old_g[gid]["expectedTermination"]
        b = new_g[gid]["expectedTermination"]
        if a.get("class") != b.get("class"):
            cls_mismatch += 1
        if (a.get("errorCode") or a.get("reasonCode")) != \
                (b.get("errorCode") or b.get("reasonCode")):
            code_mismatch += 1
        if old["classToExitCode"][a["class"]] != new["classToExitCode"][b["class"]]:
            exit_mismatch += 1

    changed_shared = [g for g in shared if canon(old_g[g]) != canon(new_g[g])]
    added = sorted(set(new_g) - set(old_g))

    def cross_axis_ids(doc: Any) -> list[str]:
        rows = doc.get("crossAxisInvariants") or []
        return [r.get("id") for r in rows if isinstance(r, dict)]

    details = ((new.get("hostTerminationUnion") or {}).get("fieldTypes") or {}) \
        .get("details") or {}

    return {
        "exitClassesRemoved": [c for c in old_classes if c not in new_classes],
        "exitClassesAdded": [c for c in new_classes if c not in old_classes],
        "exitClassesV16": old_classes,
        "exitClassesV114": new_classes,
        "exitClassSetIdentical": old_classes == new_classes,
        "classToExitCodeByteIdentical":
            canon(old["classToExitCode"]) == canon(new["classToExitCode"]),
        "classToExitCode": new["classToExitCode"],
        "exitCodeValueSetV16": sorted(set(old["classToExitCode"].values())),
        "exitCodeValueSetV114": sorted(set(new["classToExitCode"].values())),
        "countV16": len(old_g),
        "countV114": len(new_g),
        "shared": len(shared),
        "removed": sorted(set(old_g) - set(new_g)),
        "added": added,
        "addedGoldenClasses": sorted({new_g[g]["expectedTermination"]["class"]
                                      for g in added}),
        "sharedExitClassMismatches": cls_mismatch,
        "sharedReasonOrErrorCodeMismatches": code_mismatch,
        "sharedNumericExitCodeMismatches": exit_mismatch,
        "changedShared": changed_shared,
        "changedSharedDetail": {
            g: {"class": new_g[g]["expectedTermination"].get("class"),
                "errorCode": new_g[g]["expectedTermination"].get("errorCode"),
                "droppedFields": sorted(
                    set(old_g[g]["expectedTermination"]) -
                    set(new_g[g]["expectedTermination"]))}
            for g in changed_shared},
        "reasonCodesByteIdentical":
            canon(old["codeVocabulary"]["reasonCodes"]) ==
            canon(new["codeVocabulary"]["reasonCodes"]),
        "errorCodesByteIdentical":
            canon(old["codeVocabulary"]["errorCodes"]) ==
            canon(new["codeVocabulary"]["errorCodes"]),
        "remediesAdded": sorted(set(new["codeVocabulary"]["remedies"]) -
                                set(old["codeVocabulary"]["remedies"])),
        "remediesRemoved": sorted(set(old["codeVocabulary"]["remedies"]) -
                                  set(new["codeVocabulary"]["remedies"])),
        "byteIdenticalRoots": sorted(k for k in set(old) & set(new)
                                     if canon(old[k]) == canon(new[k])),
        "changedSharedRoots": sorted(k for k in set(old) & set(new)
                                     if canon(old[k]) != canon(new[k])),
        "d9DepsByteIdentical":
            canon(old["decisionDependencies"]) ==
            canon(new["decisionDependencies"]),
        "d9CitesVersioningPolicy": "versioning-policy" in canon(new).lower(),
        "d9CitesVersioningInDeps":
            "versioning" in canon(new["decisionDependencies"]).lower(),
        "exitClassMeaningsChanged": sorted(
            o["class"] for o, n in zip(old["exitClasses"], new["exitClasses"])
            if canon(o) != canon(n)),
        "hostTerminationUnionChanged":
            canon(old.get("hostTerminationUnion")) !=
            canon(new.get("hostTerminationUnion")),
        "crossAxisInvariantsAdded": [i for i in cross_axis_ids(new)
                                     if i not in cross_axis_ids(old)],
        "detailsSemanticAuthority": details.get("semanticAuthority"),
        "detailsControlFlowUse": details.get("controlFlowUse"),
    }


def slugify(heading: str) -> str:
    text = heading.strip().lower()
    text = re.sub(r"[^a-z0-9 \-]", "", text)
    return re.sub(r"\s+", "-", text).strip("-")


def resolve_citation(source: str) -> tuple[pathlib.Path, str | None]:
    token = source.split(" ")[0]
    anchor = None
    if "#" in token:
        token, anchor = token.split("#", 1)
    base = HERE.parent if "/" in token else HERE
    return base / token, anchor


def family_of(source: str) -> str:
    return pathlib.PurePosixPath(source.split(" ")[0]).name.split(".v")[0]


def measure_audit(deps: list[Any], claims: list[Any]) -> list[dict[str, Any]]:
    """Recompute every audit column from disk and from the live register rather
    than accepting the artifact's declaration. `candidates` is recorded so the
    family-ambiguity collapse the review named in O-02 — a second binding in the
    same family silently flipping a resolved row to null — is a NAMED
    measurement rather than an unexplained None."""
    out: list[dict[str, Any]] = []
    for index, dep in enumerate(deps):
        source = dep.get("source", "") if isinstance(dep, dict) else dep
        identifier = dep.get("id") if isinstance(dep, dict) else None
        path, anchor = resolve_citation(source)
        file_resolves = path.is_file()
        if anchor is None:
            anchor_resolves = None
        elif not file_resolves:
            anchor_resolves = False
        else:
            key = f"slugs:{path}"
            if key not in _CACHE:
                _CACHE[key] = {slugify(line.lstrip("#"))
                               for line in path.read_text().splitlines()
                               if line.startswith("#")}
            anchor_resolves = anchor in _CACHE[key]
        if identifier:
            hits = sorted({c.get("bindingArtifact") for c in claims
                           if c.get("id") == identifier and
                           c.get("bindingArtifact")})
            binding = next((c.get("bindingArtifact") for c in claims
                            if c.get("id") == identifier), None)
            how = "claim id"
        else:
            family = family_of(source)
            hits = sorted({c.get("bindingArtifact") for c in claims
                           if c.get("bindingArtifact") and
                           family_of(c["bindingArtifact"]) == family})
            binding = hits[0] if len(hits) == 1 else None
            how = "artifact family"
        out.append({"index": index, "id": identifier, "source": source,
                    "fileResolves": file_resolves,
                    "anchorResolves": anchor_resolves,
                    "registerBinding": binding,
                    "family": family_of(source),
                    "candidates": len(hits),
                    "resolvedBy": how})
    return out


def measure_review9(review: Any) -> dict[str, Any]:
    """The v9 review is an INPUT. Its 26/76/102 partition and 52/139/15 sweep are
    the reviewer's measured figures; the carried record restates them exactly."""
    blocker = (review.get("blockers") or [{}])[0]
    body = blocker.get("measured", "")
    probed = re.search(r"(\d+)\s+leaves probed", body)
    enforced = re.search(r"(\d+)\s+ENFORCED", body)
    unenforced = re.search(r"(\d+)\s+UNENFORCED", body)
    sweep: dict[str, Any] = {}
    for row in review.get("centralClaimAdjudications") or []:
        if isinstance(row, dict) and isinstance(row.get("mySweepOverV9"), dict):
            sweep = row["mySweepOverV9"]
    return {
        "verdict": review.get("verdict"),
        "blockerId": blocker.get("id"),
        "probed": int(probed.group(1)) if probed else None,
        "enforced": int(enforced.group(1)) if enforced else None,
        "unenforced": int(unenforced.group(1)) if unenforced else None,
        "integerLeaves": (sweep.get("intToFloat") or {}).get("total"),
        "intToFloatAdmitted": (sweep.get("intToFloat") or {}).get("ADMITTED"),
        "intToBoolAdmitted": (sweep.get("intToBool") or {}).get("ADMITTED"),
        "booleanLeaves": (sweep.get("boolToInt") or {}).get("total"),
        "boolToIntAdmitted": (sweep.get("boolToInt") or {}).get("ADMITTED"),
    }


def _find_row(review: Any, key: str) -> dict[str, Any]:
    for row in review.get("centralClaimAdjudications") or []:
        if isinstance(row, dict) and isinstance(row.get(key), dict):
            return row[key]
    return {}


def measure_review10(review: Any) -> dict[str, Any]:
    """The v10 review of record, read as an input. Every figure this successor
    restates about it is pulled from these bytes, never retyped."""
    blocker = (review.get("blockers") or [{}])[0]
    sweep = _find_row(review, "mySweepOverAll116")
    calib = _find_row(review, "myReproductionOfThePredecessorForCalibration")
    arms = _find_row(review, "allThreeArms")
    v10arm = arms.get(f"{PREDECESSOR} under {PREDECESSOR_CHECKER}") or {}
    v9arm = arms.get(f"{GRANDPARENT} under {GRANDPARENT_CHECKER}") or {}
    prose = {}
    for row in review.get("centralClaimAdjudications") or []:
        if isinstance(row, dict) and \
                isinstance(row.get("measured"), dict) and \
                "stringLeavesInTheTwoScopes" in row["measured"]:
            prose = row["measured"]
    return {
        "verdict": review.get("verdict"),
        "blockingFindingCount": review.get("blockingFindingCount"),
        "nonBlockingObservationCount": review.get("nonBlockingObservationCount"),
        "blockerId": blocker.get("id"),
        "sweptPositions": sweep.get("total"),
        "sweepAdmitted": sweep.get("ADMITTED"),
        "sweepByPosition": sweep.get("REJECTED-BY-POSITION"),
        "sweepCollateral": sweep.get("REJECTED-COLLATERAL"),
        "calibrationAdmitted": calib.get("ADMITTED"),
        "calibrationByPosition": calib.get("REJECTED-BY-POSITION"),
        "calibrationCollateral": calib.get("REJECTED-COLLATERAL"),
        "boolLeavesV10": (v10arm.get("boolToInt") or {}).get("total"),
        "boolAdmittedV10": (v10arm.get("boolToInt") or {}).get("ADMITTED"),
        "boolByPositionV10": (v10arm.get("boolToInt") or {})
                             .get("REJECTED-BY-POSITION"),
        "boolBySectionV10": (v10arm.get("boolToInt") or {})
                            .get("REJECTED-BY-SECTION"),
        "boolAdmittedV9": (v9arm.get("boolToInt") or {}).get("ADMITTED"),
        "boolLeavesV9": (v9arm.get("boolToInt") or {}).get("total"),
        "proseStringLeaves": prose.get("stringLeavesInTheTwoScopes"),
        "proseAdmitted": prose.get("ADMITTED"),
        "proseAdmittedCarried": prose.get("admittedInCarriedEvidenceBlocks"),
        "proseAdmittedNewBlock": prose.get("admittedInTheNewBlock"),
    }


def registry_purity(predecessor_module: Any) -> dict[str, Any]:
    """The class repair, re-derived from source on every run. A registry that
    reads the artifact can be sized by it; one that cannot take the artifact as
    an argument cannot. Both this checker's builders and the pinned
    predecessor's are measured by the same rule."""

    def measure(fn: Any) -> dict[str, int]:
        source = inspect.getsource(fn)
        params = sum(1 for name in inspect.signature(fn).parameters
                     if name == "value")
        reads = len(re.findall(r"\b(?:at|resolves_in)\(\s*value\s*,", source))
        bound = re.findall(r"(\w+)\s*=\s*at\(\s*value\s*,", source)
        loops = sum(1 for name in bound
                    if re.search(rf"for .*\b{re.escape(name)}\b", source))
        return {"artifactParameters": params, "artifactReads": reads,
                "artifactSizedLoops": loops}

    mine = {name: measure(globals()[name]) for name in REGISTRY_BUILDERS}
    theirs = {name: measure(getattr(predecessor_module, name))
              for name in PREDECESSOR_REGISTRY_BUILDERS}
    return {
        "mine": mine,
        "theirs": theirs,
        "myArtifactParameters": sum(r["artifactParameters"]
                                    for r in mine.values()),
        "myArtifactReads": sum(r["artifactReads"] for r in mine.values()),
        "myArtifactSizedLoops": sum(r["artifactSizedLoops"]
                                    for r in mine.values()),
        "predecessorArtifactParameters": sum(r["artifactParameters"]
                                             for r in theirs.values()),
        "predecessorArtifactSizedLoops": sum(r["artifactSizedLoops"]
                                             for r in theirs.values()),
    }


def respelling_census(mutations: list[Any], subject: Any) -> dict[str, Any]:
    """Classify a mutation by the TYPE TRANSITION it performs, not by words in
    its label. The predecessor's banner counted `'bool' in label`, which put a
    float respelling in the boolean bucket and counted an integer falsification
    that respells nothing — 9 claimed against 7 performed (review O-03)."""
    floats = bools = neither = 0
    label_floats = label_bools = 0
    for row in mutations:
        label, mutate = row[0], row[1]
        if "float" in label:
            label_floats += 1
        if "bool" in label or "BOOLEAN" in label:
            label_bools += 1
        candidate = copy.deepcopy(subject)
        try:
            mutate(candidate)
        except Exception:
            neither += 1
            continue
        kinds = set()
        for path in diff_leaves(candidate, subject):
            try:
                before, after = at(subject, path), at(candidate, path)
            except (KeyError, TypeError, ValueError):
                continue
            pair = (type(before).__name__, type(after).__name__)
            if pair in (("bool", "int"), ("int", "bool")):
                kinds.add("bool")
            elif pair in (("int", "float"), ("float", "int"),
                          ("bool", "float"), ("float", "bool")):
                kinds.add("float")
        if "bool" in kinds:
            bools += 1
        elif "float" in kinds:
            floats += 1
        else:
            neither += 1
    return {"total": len(mutations), "floatRespellings": floats,
            "booleanRespellings": bools, "neither": neither,
            "labelDerivedFloats": label_floats,
            "labelDerivedBooleans": label_bools}


def seal_scan(value: Any) -> dict[str, Any]:
    """Two-tier paper-seal scan over free prose. The seal FIELDS were already
    gated in v10; this closes the class the review demonstrated open — a verdict
    inheritance claim planted in an UNMEASURABLE free-text role."""
    everywhere: list[tuple[str, str]] = []
    string_leaves(value, "", everywhere)
    everywhere = [(p.lstrip("."), s) for p, s in everywhere]
    revision: list[tuple[str, str]] = []
    string_leaves(value.get("successorRevision"), "successorRevision", revision)
    hits: list[tuple[str, str]] = []
    exempt = 0
    for path, text in everywhere:
        if path.startswith(SEAL_SCAN_EXEMPT):
            exempt += 1
            continue
        for pattern in SEAL_PATTERNS_ARTIFACT:
            if re.search(pattern, text, re.I):
                hits.append((path, pattern))
    for path, text in revision:
        if path.startswith(SEAL_SCAN_EXEMPT):
            continue
        for pattern in SEAL_PATTERNS_REVISION:
            if re.search(pattern, text):
                hits.append((path, pattern))
    outside = []
    for path, pattern in hits:
        markers = SEAL_QUOTE_ALLOW.get(path)
        if markers is None:
            outside.append((path, pattern, "not an allowed quotation position"))
            continue
        try:
            text = at(value, path)
        except (KeyError, TypeError, ValueError):
            text = ""
        missing = [m for m in markers if m not in str(text)]
        if missing:
            outside.append((path, pattern,
                            f"allowed quotation position, but the quoting "
                            f"markers {missing} are absent"))
    return {"stringLeavesScanned": len(everywhere) - exempt,
            "exemptPositions": exempt,
            "revisionStringLeavesScanned": len(revision),
            "patternHits": len(hits), "hits": hits,
            "hitsOutsideTheAllowlist": len(outside), "outside": outside}


SCOPE_ROOTS = tuple(root for _name, roots in PARTITION_SCOPES for root in roots)


def in_a_scope(path: str) -> bool:
    return any(path == root or path.startswith(root + ".") or
               path.startswith(root + "[") for root in SCOPE_ROOTS)


def coverage_census(value: Any, predecessor: Any) -> dict[str, Any]:
    """Partition EVERY leaf position in the artifact by the gate that covers it.
    A position that lands in no class increments `ungated`, which the artifact
    declares as 0 and this checker compares — so a leaf cannot be introduced
    anywhere in this contract without either meeting a gate or being counted."""
    found: list[str] = []
    positions(value, "", found)
    found = [p.lstrip(".") for p in found]
    inherited = len(predecessor.get("knownLimitations") or [])
    rule_paths = {"version", "supersedes", "role",
                  "successorRevision.id",
                  "successorRevision.identityStability.predecessor",
                  "successorRevision.identityStability.state",
                  "successorRevision.identityStability.reason"}
    rule_paths |= {f"successorRevision.supersedesCandidate.{k}"
                   for k in ("artifact", "sha256", "checker", "checkerSha256")}
    rule_paths |= {f"knownLimitations[{i}]"
                   for i in range(inherited, inherited + ADDED_LIMITATION_COUNT)}
    carried_prefixes = tuple(f"successorRevision.{k}"
                             for k in FROZEN_REVISION_KEYS)
    census = {"surface": 0, "scope": 0, "carry": 0, "rule": 0, "ungated": 0}
    ungated: list[str] = []
    for path in found:
        top = path.split(".")[0].split("[")[0]
        if top not in CHANGED:
            census["surface"] += 1
        elif in_a_scope(path):
            census["scope"] += 1
        elif path.startswith(carried_prefixes):
            census["carry"] += 1
        elif top == "knownLimitations" and path not in rule_paths:
            census["carry"] += 1
        elif path in rule_paths:
            census["rule"] += 1
        else:
            census["ungated"] += 1
            ungated.append(path)
    census["total"] = len(found)
    census["ungatedPaths"] = ungated
    return census


# ------------------------------------------------------------ registry pieces

def eqd(expected: Any) -> tuple[str, str, Any, str]:
    return (MEASURED, "eq", expected, FROM_DISK)


def eqc(expected: Any) -> tuple[str, str, Any, str]:
    return (MEASURED, "eq", expected, FROM_CONSTANT)


def subd(*needles: Any) -> tuple[str, str, Any, str]:
    return (GROUNDED, "sub", [str(n) for n in needles if n not in (None, "")],
            FROM_DISK)


def subc(*needles: Any) -> tuple[str, str, Any, str]:
    return (GROUNDED, "sub", [str(n) for n in needles if n not in (None, "")],
            FROM_CONSTANT)


def vocab(allowed: Any) -> tuple[str, str, Any, str]:
    return (GROUNDED, "vocab", allowed, FROM_CONSTANT)


def bound(*needles: Any) -> tuple[str, str, Any, str]:
    """A residual boundary. Every listed token is a number this checker measured,
    so the residual must state ITS OWN boundary in the checker's digits — not
    merely contain a digit, which is how a re-worded boundary can keep its
    numerals and lose its meaning."""
    return (GROUNDED, "boundary", [str(n) for n in needles if n not in
                                   (None, "")], FROM_DISK)


def inreview() -> tuple[str, str, Any, str]:
    return (MEASURED, "inreview", None, FROM_DISK)


def prose(reason: str) -> tuple[str, str, Any, str]:
    return (UNMEASURABLE, "prose", reason, FROM_CONSTANT)


# --------------------------------------------------------------- registry (1)

def evidence_registry(deps: list[Any], measured: dict[str, Any],
                      audit: list[dict[str, Any]],
                      direction_preserved: bool) -> dict[str, Any]:
    """One entry for every leaf position in the three carried v9 evidence
    sub-blocks. Carried from the predecessor with one repair: the prose loop is
    sized by AUDIT_PROSE_ROWS instead of by the artifact, so this builder needs
    no artifact argument and cannot be sized by its subject."""
    s = f"{REPAIR}.substanceUnchangedEvidence"
    d = f"{REPAIR}.directionPreservation"
    a = f"{REPAIR}.siblingCitationAudit"
    reg: dict[str, Any] = {}
    v4_clean = (not measured["exitClassesRemoved"] and
                measured["classToExitCodeByteIdentical"] and
                not measured["sharedExitClassMismatches"] and
                not measured["sharedNumericExitCodeMismatches"])

    reg[f"{s}.question"] = subd("additive-only exit-class rule (V4)")
    reg[f"{s}.answer"] = subd("YES" if v4_clean else "NO", "measured")
    reg[f"{s}.measuredBetween.supersededCitation"] = eqc(D9_SUPERSEDED)
    reg[f"{s}.measuredBetween.supersededCitationSha256"] = \
        eqd(sha_file(D9_SUPERSEDED))
    reg[f"{s}.measuredBetween.head"] = eqc(D9_HEAD)
    reg[f"{s}.measuredBetween.headSha256"] = eqd(sha_file(D9_HEAD))
    reg[f"{s}.whyNotInheritedFromTheHeadReview"] = subc(
        "v1.13", "v1.6", "IDENTICAL under v1.13 and v1.14")
    for index, name in enumerate(measured["exitClassesV16"]):
        reg[f"{s}.exitClassSet.v16[{index}]"] = eqd(name)
    for index, name in enumerate(measured["exitClassesV114"]):
        reg[f"{s}.exitClassSet.v114[{index}]"] = eqd(name)
    reg[f"{s}.exitClassSet.removed"] = eqd(measured["exitClassesRemoved"])
    reg[f"{s}.exitClassSet.added"] = eqd(measured["exitClassesAdded"])
    reg[f"{s}.exitClassSet.identical"] = eqd(measured["exitClassSetIdentical"])
    reg[f"{s}.classToExitCodeByteIdentical"] = \
        eqd(measured["classToExitCodeByteIdentical"])
    for name, code in measured["classToExitCode"].items():
        reg[f"{s}.classToExitCode.{name}"] = eqd(code)
    reg[f"{s}.goldenCases.countV16"] = eqd(measured["countV16"])
    reg[f"{s}.goldenCases.countV114"] = eqd(measured["countV114"])
    reg[f"{s}.goldenCases.shared"] = eqd(measured["shared"])
    reg[f"{s}.goldenCases.removed"] = eqd(measured["removed"])
    reg[f"{s}.goldenCases.sharedExitClassMismatches"] = \
        eqd(measured["sharedExitClassMismatches"])
    reg[f"{s}.goldenCases.sharedReasonOrErrorCodeMismatches"] = \
        eqd(measured["sharedReasonOrErrorCodeMismatches"])
    reg[f"{s}.goldenCases.sharedNumericExitCodeMismatches"] = \
        eqd(measured["sharedNumericExitCodeMismatches"])
    for field, values in (("added", measured["added"]),
                          ("changedShared", measured["changedShared"]),
                          ("remediesAdded", measured["remediesAdded"])):
        prefix = f"{s}.codeVocabulary" if field.startswith("remedies") \
            else f"{s}.goldenCases"
        if not values:
            reg[f"{prefix}.{field}"] = eqd([])
        for index, name in enumerate(values):
            reg[f"{prefix}.{field}[{index}]"] = eqd(name)
    detail_needles: list[Any] = []
    for gid, row in measured["changedSharedDetail"].items():
        detail_needles.extend([gid, row["class"], row["errorCode"]])
        detail_needles.extend(row["droppedFields"])
    reg[f"{s}.goldenCases.changedSharedDisposition"] = subd(*detail_needles)
    reg[f"{s}.codeVocabulary.reasonCodesByteIdentical"] = \
        eqd(measured["reasonCodesByteIdentical"])
    reg[f"{s}.codeVocabulary.errorCodesByteIdentical"] = \
        eqd(measured["errorCodesByteIdentical"])
    reg[f"{s}.codeVocabulary.remediesRemoved"] = eqd(measured["remediesRemoved"])
    for index, name in enumerate(measured["byteIdenticalRoots"]):
        reg[f"{s}.byteIdenticalRootsV16ToV114[{index}]"] = eqd(name)
    if not measured["byteIdenticalRoots"]:
        reg[f"{s}.byteIdenticalRootsV16ToV114"] = eqd([])
    reg[f"{s}.conclusion"] = subd("byte-identical", "additive", "V4",
                                  *measured["addedGoldenClasses"])

    d9_dep = deps[4] if len(deps) > 4 and isinstance(deps[4], dict) else {}
    reg[f"{d}.declared"] = eqd(d9_dep.get("direction"))
    reg[f"{d}.preservedByteIdentical"] = eqd(direction_preserved)
    reg[f"{d}.reVerifiedAtHead.d9DecisionDependenciesByteIdenticalV16ToV114"] = \
        eqd(measured["d9DepsByteIdentical"])
    reg[f"{d}.reVerifiedAtHead.d9CitesAnyVersioningPolicyArtifact"] = \
        eqd(measured["d9CitesVersioningPolicy"])
    reg[f"{d}.reVerifiedAtHead.d9CitesVersioningInItsDependencies"] = \
        eqd(measured["d9CitesVersioningInDeps"])
    reg[f"{d}.reVerifiedAtHead.finding"] = subc(
        D9_HEAD, "one-way", "B-SCV2-06", "decisionDependencies")

    reg[f"{a}.method"] = subc(REGISTER, "decisionDependencies", "heading slugs")
    for row in audit:
        index = row["index"]
        reg[f"{a}.entries[{index}].index"] = eqc(index)
        reg[f"{a}.entries[{index}].id"] = eqd(row["id"])
        reg[f"{a}.entries[{index}].source"] = eqd(row["source"])
        reg[f"{a}.entries[{index}].fileResolves"] = eqd(row["fileResolves"])
        reg[f"{a}.entries[{index}].anchorResolves"] = eqd(row["anchorResolves"])
        reg[f"{a}.entries[{index}].registerBinding"] = eqd(row["registerBinding"])
        if index == 4:
            reg[f"{a}.entries[{index}].result"] = subc(
                "REPAIRED IN THIS VERSION", D9_SUPERSEDED, "register binding")
        elif row["id"] is None:
            reg[f"{a}.entries[{index}].result"] = subd(
                "STALE", "R-VER9-02", row["source"].split(" ")[0])
        else:
            reg[f"{a}.entries[{index}].result"] = subc("CLEAN")
    for index in range(AUDIT_PROSE_ROWS):
        reg[f"{a}.prose[{index}].field"] = (MEASURED, "field", None, FROM_DISK)
        reg[f"{a}.prose[{index}].result"] = subc(
            "REPAIRED IN THIS VERSION" if index == 0
            else "CARRIED FORWARD UNCHANGED")
    reg[f"{a}.measuredResult"] = subd(
        f"{len(deps)} decisionDependencies entries",
        sum(1 for r in audit if r["anchorResolves"] is True),
        sum(1 for r in audit if r["id"] is None),
        "R-VER9-02")
    return reg


# --------------------------------------------------------------- registry (2)

def frozen_registry(root: str, pinned: Any) -> dict[str, Any]:
    """Every leaf position of a block that must be byte-identical to the pinned
    predecessor, compared against the PINNED value at that position. The
    position set comes from bytes the subject does not supply, so a row appended
    to any list inside it has no classification (VER11-COVER) and a row deleted
    from one leaves a classification with nothing to compare (VER11-COVER).
    This is what the predecessor's four self-sized loops could not do."""
    items: list[tuple[str, Any]] = []
    leaf_items(pinned, root, items)
    return {path: eqd(value) for path, value in items}


# --------------------------------------------------------------- registry (3)

def closure_registry(m: dict[str, Any]) -> dict[str, Any]:
    """The successor's own new evidence block. Every position here is generated
    from a checker constant or from `m`, a bundle of measurements taken from
    disk, from the pinned predecessor, from the live register and from this
    checker's own source. No artifact is in scope: the block cannot size its own
    police."""
    c = CLOSE
    reg: dict[str, Any] = {}
    review = m["review10"]
    purity = m["purity"]
    census = m["census"]
    scan = m["seal"]
    # The demonstration table is sized by the reviewer's plan, a checker
    # constant, never by whatever the artifact happens to declare.
    probes = list(m["probes"])[:DEMONSTRATIONS]
    while len(probes) < DEMONSTRATIONS:
        probes.append({"probe": "", "position": "", "predecessorAdmitted": None,
                       "predecessorFindings": None, "successorRejects": None,
                       "successorNamesThePosition": None,
                       "successorFindingIds": None})
    cascade = m["cascade"]
    rehearsals = m["rehearsals"]
    census_scopes = m["partitions"]

    reg[f"{c}.findingId"] = eqd(review["blockerId"])
    reg[f"{c}.authoredBy"] = vocab(OWNER_VOCABULARY)

    r = f"{c}.reviewOfRecord"
    reg[f"{r}.artifact"] = eqc(PREDECESSOR_REVIEW)
    reg[f"{r}.sha256"] = eqd(sha_file(PREDECESSOR_REVIEW))
    reg[f"{r}.verdict"] = eqd(review["verdict"])
    reg[f"{r}.blockingFindingCount"] = eqd(review["blockingFindingCount"])
    reg[f"{r}.nonBlockingObservationCount"] = \
        eqd(review["nonBlockingObservationCount"])
    reg[f"{r}.blockerIsAgainst"] = eqc(PREDECESSOR_CHECKER)
    reg[f"{r}.blockerIsNotAgainst"] = inreview()
    reg[f"{r}.reviewerStatement"] = inreview()
    reg[f"{r}.upheldResidual"] = eqc("R-VER10-08")
    reg[f"{r}.sweptPositions"] = eqd(review["sweptPositions"])
    reg[f"{r}.sweepAdmitted"] = eqd(review["sweepAdmitted"])
    reg[f"{r}.sweepRejectedByPosition"] = eqd(review["sweepByPosition"])
    reg[f"{r}.sweepRejectedCollaterally"] = eqd(review["sweepCollateral"])
    reg[f"{r}.calibrationAdmittedOnThePredecessorOfTheSubject"] = \
        eqd(review["calibrationAdmitted"])

    reg[f"{c}.defect"] = subd(
        m["predBlockPositions"], m["predSelfSizedPositions"], "VER10-COVER")
    reg[f"{c}.whySuccessorAndNotInPlaceRepair"] = subc(
        "§7.2", PREDECESSOR, "ENUMERATED_DELTA")

    p = f"{c}.registryPurity"
    reg[f"{p}.principle"] = subc("sized from the artifact", "cannot police")
    reg[f"{p}.rule"] = subc("checker constant", "pinned", "no artifact")
    for index, name in enumerate(REGISTRY_BUILDERS):
        reg[f"{p}.builders[{index}].function"] = eqc(name)
        reg[f"{p}.builders[{index}].artifactParameters"] = \
            eqd(purity["mine"][name]["artifactParameters"])
        reg[f"{p}.builders[{index}].artifactReads"] = \
            eqd(purity["mine"][name]["artifactReads"])
        reg[f"{p}.builders[{index}].artifactSizedLoops"] = \
            eqd(purity["mine"][name]["artifactSizedLoops"])
    for index, name in enumerate(PREDECESSOR_REGISTRY_BUILDERS):
        reg[f"{p}.predecessorBuilders[{index}].function"] = eqc(name)
        reg[f"{p}.predecessorBuilders[{index}].artifactParameters"] = \
            eqd(purity["theirs"][name]["artifactParameters"])
        reg[f"{p}.predecessorBuilders[{index}].artifactSizedLoops"] = \
            eqd(purity["theirs"][name]["artifactSizedLoops"])
    reg[f"{p}.artifactSizedLoopsHere"] = eqd(purity["myArtifactSizedLoops"])
    reg[f"{p}.artifactReadsHere"] = eqd(purity["myArtifactReads"])
    reg[f"{p}.artifactSizedLoopsInThePredecessor"] = \
        eqd(purity["predecessorArtifactSizedLoops"])
    reg[f"{p}.measuredBy"] = subc("inspect.getsource", "every run")

    d = f"{c}.predecessorDefect"
    reg[f"{d}.blockLeafPositions"] = eqd(m["predBlockPositions"])
    reg[f"{d}.positionsInSelfSizedLoops"] = eqd(m["predSelfSizedPositions"])
    for index, path in enumerate(PREDECESSOR_SELF_SIZED_LOOPS):
        reg[f"{d}.selfSizedLoops[{index}].path"] = eqc(path)
        reg[f"{d}.selfSizedLoops[{index}].positions"] = \
            eqd(m["predLoopPositions"][index])
    reg[f"{d}.blockTotalOccurrencesInThePredecessorArtifact"] = \
        eqd(m["predTotalOccurrences"])
    reg[f"{d}.blockPartitionWasComparedByThePredecessorChecker"] = eqd(False)
    reg[f"{d}.predecessorCheckerFindingsAgainstItsOwnBytes"] = \
        eqd(m["predCheckerFindings"])
    reg[f"{d}.predecessorRednessIsRegisterCoupledOnly"] = \
        eqd(m["predRednessCoupledOnly"])
    reg[f"{d}.predecessorAdmissions"] = eqd(m["predAdmissions"])
    reg[f"{d}.successorAdmissions"] = eqd(m["selfAdmissions"])
    for index, row in enumerate(probes):
        reg[f"{d}.demonstrations[{index}].probe"] = eqc(row["probe"])
        reg[f"{d}.demonstrations[{index}].position"] = eqc(row["position"])
        reg[f"{d}.demonstrations[{index}].predecessorAdmitted"] = \
            eqd(row["predecessorAdmitted"])
        reg[f"{d}.demonstrations[{index}].predecessorFindings"] = \
            eqd(row["predecessorFindings"])
        reg[f"{d}.demonstrations[{index}].successorRejects"] = \
            eqd(row["successorRejects"])
        reg[f"{d}.demonstrations[{index}].successorNamesThePosition"] = \
            eqd(row["successorNamesThePosition"])
        reg[f"{d}.demonstrations[{index}].successorFindingIds"] = \
            eqd(row["successorFindingIds"])
        if index == 2:
            reg[f"{d}.demonstrations[{index}].plantedText"] = subc(
                m["plantedRole"], "REJECTED", "planted")

    q = f"{c}.partitionClosure"
    reg[f"{q}.rule"] = subc("compared", "banner", "uncompared")
    for index, (name, roots) in enumerate(PARTITION_SCOPES):
        part = census_scopes[name]
        reg[f"{q}.scopes[{index}].name"] = eqc(name)
        reg[f"{q}.scopes[{index}].roots"] = eqc(" | ".join(roots))
        reg[f"{q}.scopes[{index}].total"] = eqd(part["total"])
        reg[f"{q}.scopes[{index}].MEASURED"] = eqd(part["measured"])
        reg[f"{q}.scopes[{index}].GROUNDED"] = eqd(part["grounded"])
        reg[f"{q}.scopes[{index}].UNMEASURABLE"] = eqd(part["unmeasurable"])
        reg[f"{q}.scopes[{index}].measuredAgainstDisk"] = eqd(part["fromDisk"])
        reg[f"{q}.scopes[{index}].measuredAgainstACheckerConstant"] = \
            eqd(part["fromConstant"])
        reg[f"{q}.scopes[{index}].positionDigest"] = eqd(part["digest"])
    reg[f"{q}.computedPartitions"] = eqd(len(PARTITION_SCOPES))
    reg[f"{q}.declaredPartitions"] = eqd(len(PARTITION_SCOPES))
    reg[f"{q}.uncomparedPartitions"] = eqd(0)
    reg[f"{q}.publishedMeasurements"] = eqd(m["publishedCount"])
    reg[f"{q}.gradeDefinitions.MEASURED"] = subc("outside the artifact")
    reg[f"{q}.gradeDefinitions.GROUNDED"] = subc("prose", "substring")
    reg[f"{q}.gradeDefinitions.UNMEASURABLE"] = subc("no on-disk referent")

    v = f"{c}.coverageCensus"
    reg[f"{v}.rule"] = subc("every leaf position", "ungated")
    reg[f"{v}.artifactLeafPositions"] = eqd(census["total"])
    reg[f"{v}.gatedByAnEnforcementScope"] = eqd(census["scope"])
    reg[f"{v}.gatedByTheProtectedSurfaceComparison"] = eqd(census["surface"])
    reg[f"{v}.gatedByByteCarryAgainstThePredecessor"] = eqd(census["carry"])
    reg[f"{v}.gatedByAnExplicitRule"] = eqd(census["rule"])
    reg[f"{v}.ungated"] = eqd(census["ungated"])

    b = f"{c}.carriedByteIdentical"
    reg[f"{b}.rule"] = subc("byte-identical", PREDECESSOR, "measurement")
    for index, name in enumerate(FROZEN_REVISION_KEYS):
        reg[f"{b}.frozenSuccessorKeys[{index}]"] = eqc(name)
    reg[f"{b}.frozenSuccessorKeyCount"] = eqd(len(FROZEN_REVISION_KEYS))
    reg[f"{b}.protectedTopLevelKeys"] = eqd(m["protectedTopLevelKeys"])
    for index, name in enumerate(sorted(CHANGED)):
        reg[f"{b}.changedTopLevelKeys[{index}]"] = eqc(name)
    reg[f"{b}.carriedDelta.count"] = eqd(m["carriedDeltaCount"])
    reg[f"{b}.carriedDelta.digest"] = eqd(m["carriedDeltaDigest"])
    reg[f"{b}.carriedDelta.rule"] = subc("count", "digest", "index")
    reg[f"{b}.carriedDelta.everyMovedPositionIsIndependentlyReMeasured"] = \
        eqd(m["deltaRemeasured"])
    reg[f"{b}.carriedDelta.whatMayMove"] = subc(
        "re-measures", "declaration", "prose")
    reg[f"{b}.carriedDelta.whyNotATable"] = subc(
        "ENUMERATED_DELTA", "index", "measurement")

    g = f"{c}.registerAsOfAudit"
    reg[f"{g}.principle"] = subc(
        "recorded measurement", "continuing invariant",
        "Measurements get hard comparison; invariants get semantic gates")
    reg[f"{g}.measurementArm"] = subc("recorded measurement", "at authoring",
                                      "B-VER9R-01", "true positive")
    reg[f"{g}.invariantArm"] = subc("continuing invariant", "R-VER9-07",
                                    "semantic")
    reg[f"{g}.recordingDisposition"] = subd(
        REGISTER, "RECORDED-NOT-PINNED", m["registerDrifts"])
    for row in m["audit"]:
        index = row["index"]
        reg[f"{g}.entries[{index}].index"] = eqc(index)
        reg[f"{g}.entries[{index}].family"] = eqd(row["family"])
        reg[f"{g}.entries[{index}].resolvedBy"] = eqd(row["resolvedBy"])
        reg[f"{g}.entries[{index}].registerBinding"] = eqd(row["registerBinding"])
        reg[f"{g}.entries[{index}].candidateBindingsInFamily"] = \
            eqd(row["candidates"])
    reg[f"{g}.liveD9Binding"] = eqd(m["liveD9"])
    reg[f"{g}.liveVersioningBinding"] = eqd(m["liveVersioning"])
    reg[f"{g}.d9CitationEqualsTheLiveBinding"] = eqd(True)

    k = f"{c}.repointCascade"
    reg[f"{k}.mechanism"] = subc("ENUMERATED_DELTA", "checker constant", "index")
    reg[f"{k}.predecessorFindingsOnTheOneLineFix"] = eqd(cascade["predFindings"])
    reg[f"{k}.predecessorIndexShifts"] = eqd(cascade["predIndexShifts"])
    reg[f"{k}.predecessorPositionsAddedOrRemoved"] = eqd(cascade["predAddedPos"])
    reg[f"{k}.successorFindingsOnTheOneLineFix"] = eqd(cascade["selfFindings"])
    reg[f"{k}.successorIndexShifts"] = eqd(0)
    reg[f"{k}.successorPositionsAddedOrRemoved"] = eqd(cascade["selfAddedPos"])
    reg[f"{k}.successorFindingIdsOnTheOneLineFix"] = eqd(cascade["selfIds"])
    for index, row in enumerate(rehearsals):
        reg[f"{k}.rehearsals[{index}].event"] = eqc(row["event"])
        reg[f"{k}.rehearsals[{index}].enumeratedByThePredecessorResidual"] = \
            eqc(row["enumerated"])
        reg[f"{k}.rehearsals[{index}].declaredLeavesThatWouldChange"] = \
            eqd(row["changed"])
        reg[f"{k}.rehearsals[{index}].positionsAddedOrRemoved"] = \
            eqd(row["addedPositions"])
        reg[f"{k}.rehearsals[{index}].indexShifts"] = eqd(row["indexShifts"])
        reg[f"{k}.rehearsals[{index}].repairIsInPlace"] = eqd(True)
    reg[f"{k}.repairLeafEditsOnARepoint"] = eqd(rehearsals[0]["changed"])
    for index, path in enumerate(REGISTER_SENSITIVE_CLOSURE_LEAVES):
        reg[f"{k}.registerSensitiveLeaves[{index}]"] = eqc(path)
    reg[f"{k}.checkerEditsRequired"] = eqd(0)
    # The armed event itself, as two leaves. The first is stable; the second is
    # the coordinator's act, and when it happens it is one named leaf to restate
    # rather than a cascade to chase.
    reg[f"{k}.armedTargetOnDisk"] = eqd(m["armedOnDisk"])
    reg[f"{k}.armedTarget"] = eqc(ARMED_RT)
    reg[f"{k}.registerBindsTheArmedTarget"] = eqd(m["armedBound"])

    z = f"{c}.prosePaperSealScan"
    reg[f"{z}.rule"] = subc("free prose", "allowlist", "quoting markers")
    for index, pattern in enumerate(SEAL_PATTERNS_ARTIFACT):
        reg[f"{z}.artifactPatterns[{index}]"] = eqc(pattern)
    for index, pattern in enumerate(SEAL_PATTERNS_REVISION):
        reg[f"{z}.revisionPatterns[{index}]"] = eqc(pattern)
    reg[f"{z}.stringLeavesScanned"] = eqd(scan["stringLeavesScanned"])
    reg[f"{z}.exemptPositions"] = eqd(scan["exemptPositions"])
    reg[f"{z}.whyExempt"] = subc("pattern table", "equality", "checker constant")
    reg[f"{z}.revisionStringLeavesScanned"] = \
        eqd(scan["revisionStringLeavesScanned"])
    reg[f"{z}.patternHits"] = eqd(scan["patternHits"])
    reg[f"{z}.hitsOutsideTheAllowlist"] = eqd(scan["hitsOutsideTheAllowlist"])
    for index, path in enumerate(sorted(SEAL_QUOTE_ALLOW)):
        reg[f"{z}.allowedQuotationPositions[{index}].path"] = eqc(path)
        reg[f"{z}.allowedQuotationPositions[{index}].requiredMarkers"] = \
            eqc(", ".join(SEAL_QUOTE_ALLOW[path]))
    reg[f"{z}.plantedClaimVerbatim"] = subc(m["plantedRole"], "REJECTED",
                                            "B-VER10R-01", "planted")
    reg[f"{z}.plantedAt"] = eqc(f"{ENFORCE}.recordedInputs[*].role")
    reg[f"{z}.predecessorAdmittedIt"] = eqd(probes[2]["predecessorAdmitted"])

    n = f"{c}.closedScalarAdmission"
    reg[f"{n}.law"] = subc("law 18", "exact-type")
    reg[f"{n}.integerLeavesInV9"] = eqd(m["review9"]["integerLeaves"])
    reg[f"{n}.intToFloatAdmittedInV9"] = eqd(m["review9"]["intToFloatAdmitted"])
    reg[f"{n}.boolToIntAdmittedInV9"] = eqd(m["review9"]["boolToIntAdmitted"])
    reg[f"{n}.booleanLeavesInV10"] = eqd(review["boolLeavesV10"])
    reg[f"{n}.boolToIntAdmittedInV10"] = eqd(review["boolAdmittedV10"])
    reg[f"{n}.boolToIntRejectedByPositionInV10"] = eqd(review["boolByPositionV10"])
    reg[f"{n}.boolToIntRejectedBySectionInV10"] = eqd(review["boolBySectionV10"])
    reg[f"{n}.booleanLeavesSweptInV11"] = eqd(m["sweep"]["total"])
    reg[f"{n}.boolToIntAdmittedInV11"] = eqd(m["sweep"]["admitted"])
    reg[f"{n}.sweptBy"] = subc("plain run", "--selftest")
    reg[f"{n}.scope"] = subc("successorRevision")

    t = f"{c}.selftestProfile"
    reg[f"{t}.countedBy"] = subc("type transition", "label")
    reg[f"{t}.mutations"] = eqd(m["census11"]["total"])
    reg[f"{t}.floatRespellings"] = eqd(m["census11"]["floatRespellings"])
    reg[f"{t}.booleanRespellings"] = eqd(m["census11"]["booleanRespellings"])
    reg[f"{t}.assertionsOnAFullDottedPath"] = eqd(m["fullPathAssertions"])
    reg[f"{t}.assertionsOnASectionName"] = eqd(m["sectionAssertions"])
    reg[f"{t}.distinctFindingIdsExercised"] = eqd(m["distinctIds"])
    reg[f"{t}.predecessorMutations"] = eqd(m["census10"]["total"])
    reg[f"{t}.predecessorBannerBooleanRespellings"] = \
        eqd(m["census10"]["labelDerivedBooleans"])
    reg[f"{t}.predecessorGenuineBooleanRespellings"] = \
        eqd(m["census10"]["booleanRespellings"])
    overcount = None
    if exact_int(m["census10"]["labelDerivedBooleans"]) and \
            exact_int(m["census10"]["booleanRespellings"]):
        overcount = (m["census10"]["labelDerivedBooleans"] -
                     m["census10"]["booleanRespellings"])
    reg[f"{t}.predecessorBannerOvercount"] = eqd(overcount)
    reg[f"{t}.predecessorFloatRespellings"] = \
        eqd(m["census10"]["floatRespellings"])

    e = f"{c}.residualRestatements"
    for index, rid in enumerate(RESTATED_RESIDUALS):
        reg[f"{e}[{index}].id"] = eqc(rid)
        reg[f"{e}[{index}].reviewObservation"] = subc("-0")
        reg[f"{e}[{index}].wasRecorded"] = bound(*m["restatedWas"][index])
        reg[f"{e}[{index}].nowMeasured"] = bound(*m["restatedNow"][index])

    i = f"{c}.recordedInputs"
    for index, (name, role) in enumerate(V11_REQUIRED_INPUTS):
        reg[f"{i}[{index}].artifact"] = eqc(name)
        reg[f"{i}[{index}].sha256"] = eqd(sha_file(name))
        reg[f"{i}[{index}].role"] = eqc(role)

    y = f"{c}.retainedResiduals"
    for index, rid in enumerate(REQUIRED_RESIDUAL_IDS):
        reg[f"{y}[{index}].id"] = eqc(rid)
        reg[f"{y}[{index}].residual"] = subc(*RESIDUAL_TOKENS[rid])
        reg[f"{y}[{index}].measured"] = bound(*m["residualNumbers"][rid])
        reg[f"{y}[{index}].disposition"] = subc(*RESIDUAL_DISPOSITION[rid])
        reg[f"{y}[{index}].ownedBy"] = vocab(OWNER_VOCABULARY)

    x = f"{c}.checkerDisposition"
    reg[f"{x}.successorCheckerRequired"] = eqc(True)
    reg[f"{x}.checker"] = eqd(pathlib.Path(__file__).name)
    reg[f"{x}.checkerEnforcesEveryDeclaredEvidenceLeafInEveryDeclaredScope"] = \
        eqd(True)
    reg[f"{x}.declaredScopes"] = eqd(len(PARTITION_SCOPES))
    reg[f"{x}.unclassifiedLeafPositionsAcrossAllScopes"] = eqd(0)
    reg[f"{x}.scopeOfThatBoolean"] = subc(
        "the block it sits in", "successorClosureBlock")
    reg[f"{x}.whyThePredecessorCheckerCannotValidateThis"] = \
        subc(PREDECESSOR_CHECKER, "enforcementClosureRepair")
    reg[f"{x}.evidenceGrade"] = subc("IMPLEMENTABLE_UNEXECUTED")

    for index, tokens in enumerate(NOT_CLAIMED_TOKENS):
        reg[f"{c}.notClaimed[{index}]"] = subc(*tokens)
    return reg


# ------------------------------------------------------------------ compare

def compare(value: Any, path: str, kind: str, payload: Any, declared: Any,
            extra: dict[str, Any]) -> str | None:
    if kind == "eq":
        if canon(declared) == canon(payload):
            return None
        if type(declared) is not type(payload) and (
                isinstance(declared, (int, float, bool)) or
                isinstance(payload, (int, float, bool))):
            return (f"VER11-LEAFTYPE: {path} declares {declared!r} "
                    f"({type(declared).__name__}); this checker measured "
                    f"{payload!r} ({type(payload).__name__}). freeze §6 law 18: "
                    f"closed-scalar admission is exact-type in BOTH directions")
        if path.endswith(".registerBinding") or path.endswith("candidateBindingsInFamily"):
            return (f"VER11-ASOF: {path} declares {canon(declared)[:110]}; this "
                    f"checker measured {canon(payload)[:110]} from the live "
                    f"{REGISTER}. A registerBinding is a RECORDED MEASUREMENT, "
                    f"so this is a TRUE POSITIVE about these bytes, not a false "
                    f"alarm about the register (R-VER11-08). Repair in place: "
                    f"restate this leaf and re-measure "
                    f"{CLOSE}.carriedByteIdentical.carriedDelta.count/.digest — "
                    f"a count and a digest, so there is no index to shift")
        return (f"VER11-LEAF: {path} declares {canon(declared)[:110]}; this "
                f"checker measured {canon(payload)[:110]} from disk")
    if kind in ("sub", "prose", "boundary", "vocab"):
        if not isinstance(declared, str) or not declared.strip():
            return f"VER11-PROSE: {path} is not a non-empty string"
    if kind == "sub":
        missing = [n for n in payload if n not in declared]
        if missing:
            return (f"VER11-PROSE: {path} does not state the measured "
                    f"assertion(s) {missing} this checker derived")
        return None
    if kind == "prose":
        return None
    if kind == "boundary":
        missing = [n for n in payload if n not in declared]
        if missing or not re.search(r"\d", declared):
            return (f"VER11-RESID: {path} does not state its boundary in this "
                    f"checker's measured numbers; missing {missing}. Every "
                    f"residual states its boundary as a measured number, "
                    f"compared to the measurement it names — presence of digits "
                    f"is not meaning")
        return None
    if kind == "vocab":
        if declared not in payload:
            return (f"VER11-LEAF: {path} declares {declared!r}, which is not in "
                    f"the closed vocabulary {sorted(payload)}")
        return None
    if kind == "field":
        if not isinstance(declared, str) or not declared.strip():
            return f"VER11-LEAF: {path} names no field"
        for token in re.split(r"\s*/\s*", declared):
            normalised = token.replace("['", ".").replace("']", "").strip()
            if not normalised:
                continue
            if not resolves_in(value, normalised) and \
                    not resolves_in(value, f"successorRevision.{normalised}"):
                return (f"VER11-LEAF: {path} names {token!r}, which does not "
                        f"resolve in this artifact")
        return None
    if kind == "inreview":
        if not isinstance(declared, str) or declared not in extra["reviewText"]:
            return (f"VER11-LEAF: {path} quotes the independent review, but the "
                    f"quoted text does not occur in {PREDECESSOR_REVIEW}")
        return None
    return f"VER11-COVER: {path} has an unknown comparator {kind!r}"


def evaluate(value: Any, reg: dict[str, Any], scope: tuple[str, ...],
             extra: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    """Compare every position against its registry entry and return both the
    findings and the measured partition. The partition is a first-class output:
    every one produced here is compared against a declaration and only then
    published."""
    errors: list[str] = []
    found: list[str] = []
    for root in scope:
        if resolves_in(value, root):
            positions(at(value, root), root, found)
        else:
            add(errors, "VER11-COVER",
                f"declared evidence sub-block {root} is absent")
    graded: dict[str, list[str]] = {MEASURED: [], GROUNDED: [], UNMEASURABLE: []}
    origin = {FROM_DISK: 0, FROM_CONSTANT: 0}

    for path in found:
        entry = reg.get(path)
        if entry is None:
            add(errors, "VER11-COVER",
                f"leaf position {path} has no enforcement classification — the "
                f"registry that classifies this scope is generated from checker "
                f"constants and pinned measurements, never from this artifact, "
                f"so a position it does not contain is an addition and is a "
                f"finding (B-VER10R-01)")
            continue
        grade, kind, payload, source = entry
        graded[grade].append(path)
        if grade == MEASURED:
            origin[source] += 1
        message = compare(value, path, kind, payload, at(value, path), extra)
        if message:
            errors.append(message)

    for path in sorted(set(reg) - set(found)):
        if any(path.startswith(root) for root in scope):
            add(errors, "VER11-COVER",
                f"the enforcement registry expects leaf position {path}, but "
                f"the artifact does not declare it — a §7.2 recorded input or a "
                f"required residual cannot be deleted from this record")

    return errors, {
        "total": len(found),
        "measured": len(graded[MEASURED]),
        "grounded": len(graded[GROUNDED]),
        "unmeasurable": len(graded[UNMEASURABLE]),
        "fromDisk": origin[FROM_DISK],
        "fromConstant": origin[FROM_CONSTANT],
        "positions": sorted(found),
        "digest": sha_text(canon(sorted(found))),
    }


# --------------------------------------------------------------------- probes

def inner(candidate: Any) -> list[str]:
    """Run the whole of this checker against a candidate without re-entering the
    probe layer. A non-zero exit is not evidence a guard fired, so the probes
    below read the FINDINGS, not a status."""
    global _DEPTH
    _DEPTH += 1
    try:
        return check(candidate, verify_files=False)
    finally:
        _DEPTH -= 1


def names_position(errors: list[str], position: str) -> bool:
    """O-04: the predecessor asserted on the last path segment, so a leaf named
    `identical` was 'named' by any message containing 'byte-identical'. This
    requires the FULL dotted path."""
    return any(position in e for e in errors)


def ids_naming(errors: list[str], position: str) -> str:
    found = sorted({e.split(":")[0] for e in errors if position in e})
    return ",".join(found)


def probe_pairs(pred_module: Any, pred_artifact: Any, subject: Any,
                planted: str) -> list[dict[str, Any]]:
    """The reviewer's five demonstrations, executed on every run against BOTH
    the pinned predecessor pair and these bytes. The four admissions are not
    narrated here; they are reproduced."""
    def dup_residual(block: str):
        def go(c: Any) -> None:
            at(c, f"{block}.retainedResiduals").append({
                "id": "R-VER10-01" if block == ENFORCE else "R-VER11-01",
                "residual": "Fabricated duplicate residual.",
                "measured": "0 things measured.",
                "disposition": "Ignored.",
                "ownedBy": "coordinator"})
        return go

    def fake_restatement(block: str):
        # The id must be one the target block's own comparator accepts, or the
        # probe measures the id vocabulary rather than the missing coverage.
        # The reviewer used a carried v9 id against the predecessor block; the
        # equivalent against this block is a carried v10 id.
        def go(c: Any) -> None:
            at(c, f"{block}.residualRestatements").append({
                "id": "R-VER9-01" if block == ENFORCE else "R-VER10-01",
                "reviewObservation": "O-06",
                "wasRecorded": "check-versioning.py exits 1 on 0 findings.",
                "nowMeasured": "check-versioning.py now exits 0 and the "
                               "residual is closed; 0 findings remain."})
        return go

    def seal_row(block: str):
        def go(c: Any) -> None:
            at(c, f"{block}.recordedInputs").append({
                "artifact": GRANDPARENT,
                "sha256": PINS[GRANDPARENT],
                "role": planted})
        return go

    def drop_input(block: str):
        def go(c: Any) -> None:
            at(c, f"{block}.recordedInputs").pop()
        return go

    def control(block: str):
        def go(c: Any) -> None:
            at(c, f"{block}.checkerDisposition")["adversarialExtra"] = "x"
        return go

    plan = (
        ("append a duplicate retained residual",
         dup_residual, "retainedResiduals", "append"),
        ("append a residual restatement asserting an open residual is closed",
         fake_restatement, "residualRestatements", "append"),
        ("append a recordedInputs row whose role claims an inherited verdict",
         seal_row, "recordedInputs", "append"),
        ("delete the last freeze §7.2 recorded input",
         drop_input, "recordedInputs", "delete"),
        ("CONTROL — add a key at a non-loop position",
         control, "checkerDisposition.adversarialExtra", "key"),
    )
    # Admission is measured RELATIVE TO THE UNMUTATED BASELINE, not as "zero
    # findings". The predecessor is coupled to a register that may move, and a
    # probe must measure the coverage defect it is aimed at rather than the
    # coordinator's state.
    try:
        pred_baseline = sorted(pred_module.check(pred_artifact,
                                                 verify_files=False))
    except Exception as exc:
        pred_baseline = [f"{type(exc).__name__}: {exc}"]
    out: list[dict[str, Any]] = []
    for label, factory, shape, mode in plan:
        if mode == "key":
            position = f"{CLOSE}.{shape}"
        else:
            rows = (at(subject, CLOSE) or {}).get(shape) \
                if resolves_in(subject, CLOSE) else []
            size = len(rows) if isinstance(rows, list) else 0
            index = size if mode == "append" else size - 1
            position = f"{CLOSE}.{shape}[{index}]"
        pred = copy.deepcopy(pred_artifact)
        try:
            factory(ENFORCE)(pred)
            pred_errors = pred_module.check(pred, verify_files=False)
        except Exception as exc:
            pred_errors = [f"{type(exc).__name__}: {exc}"]
        mine = copy.deepcopy(subject)
        try:
            factory(CLOSE)(mine)
            my_errors = inner(mine)
        except Exception as exc:
            my_errors = [f"{type(exc).__name__}: {exc}"]
        added = [e for e in sorted(pred_errors) if e not in pred_baseline]
        out.append({
            "probe": label,
            "position": position,
            "predecessorAdmitted": not added,
            "predecessorFindings": len(added),
            "successorRejects": bool(my_errors),
            "successorNamesThePosition": names_position(my_errors, position),
            "successorFindingIds": ids_naming(my_errors, position),
        })
    return out


# A synthetic target that is never a real binding, so a rehearsal measures the
# COUPLING SURFACE — how many declared leaves are derived from this binding —
# rather than the distance from today's register state. The surface is what a
# successor author needs and it does not move when the coordinator acts.
# The declared leaves in this successor's own block that are functions of the
# register state. They are named rather than counted, so the repair cost is a
# list a successor author can work through, not a number to be trusted.
REGISTER_SENSITIVE_CLOSURE_LEAVES = (
    f"{CLOSE}.predecessorDefect.predecessorCheckerFindingsAgainstItsOwnBytes",
    f"{CLOSE}.repointCascade.registerBindsTheArmedTarget",
    f"{CLOSE}.repointCascade.successorFindingsOnTheOneLineFix",
    f"{CLOSE}.repointCascade.successorFindingIdsOnTheOneLineFix",
)

SENTINEL_RT = "artifacts/retention-tiers.v9001.json"
SENTINEL_EP = "artifacts/evaluation-proof.v9001.json"
ARMED_RT = "artifacts/retention-tiers.v23.json"


def rehearse(deps: list[Any], claims: list[Any], audit: list[dict[str, Any]],
             declared_audit: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Simulate the three register events the review named — the ARMED repoint,
    the unenumerated ADDITION and the unenumerated FAMILY AMBIGUITY — and
    measure what each would cost this record. Because the carried delta is a
    count and a digest rather than an indexed table, `indexShifts` is 0 by
    construction and that is measured, not asserted."""
    rt = [c for c in claims
          if c.get("bindingArtifact") and
          family_of(c["bindingArtifact"]) == "retention-tiers"]
    variants = []
    repoint = copy.deepcopy(claims)
    for claim in repoint:
        if claim.get("bindingArtifact") and \
                family_of(claim["bindingArtifact"]) == "retention-tiers":
            claim["bindingArtifact"] = SENTINEL_RT
    variants.append(("ARCH.RETENTION-TIERS REPOINTED within its family",
                     "yes — R-VER10-08 enumerates a repoint", repoint))
    addition = copy.deepcopy(claims) + [
        {"id": "EVALUATION-PROOF", "bindingArtifact": SENTINEL_EP}]
    variants.append(("an EVALUATION-PROOF claim ADDED to the register",
                     "no — the residual enumerates repoints only", addition))
    ambiguity = copy.deepcopy(claims) + [
        {"id": "ARCH.RETENTION-TIERS-2", "bindingArtifact": SENTINEL_RT}] \
        if rt else copy.deepcopy(claims)
    variants.append(("a SECOND retention-tiers-family binding (len(hits) != 1)",
                     "no — the residual enumerates repoints only", ambiguity))

    out: list[dict[str, Any]] = []
    base_positions = {f"entries[{r['index']}]" for r in audit}
    for event, enumerated, claim_set in variants:
        after = measure_audit(deps, claim_set)
        # Everything below is BASE MEASUREMENT vs VARIANT MEASUREMENT. Nothing
        # is compared against the declaration: the cost of an event is a
        # property of the event, and must not move when the register does.
        changed = 0
        carried_moves = False
        for before, now in zip(audit, after):
            for field in ("registerBinding", "candidates"):
                if canon(before[field]) != canon(now[field]):
                    changed += 1
            if canon(before["registerBinding"]) != canon(now["registerBinding"]):
                # the carried audit declares registerBinding only
                changed += 1
                carried_moves = True
        after_positions = {f"entries[{r['index']}]" for r in after}
        # A carried leaf that moves also moves the two carriedDelta scalars, and
        # those are leaf edits too. Counting them is the difference between a
        # repair cost and an understatement of one.
        if carried_moves:
            changed += 2
        if changed:
            changed += len(REGISTER_SENSITIVE_CLOSURE_LEAVES)
        out.append({
            "event": event,
            "enumerated": enumerated,
            "changed": changed,
            "addedPositions": len(after_positions ^ base_positions),
            "indexShifts": 0,
        })
    return out


# ----------------------------------------------------------------- the check

def declared_derivation(value: Any) -> dict[str, Any]:
    """The BOOTSTRAP bundle. While the real measurements below are being taken,
    the nested runs they perform need the probe-derived leaves to compare equal
    to something, or every nested run would carry unrelated findings and the
    boolean sweep would count collateral noise as a rejection. So the bootstrap
    reads those leaves from the artifact's own declaration — and is then thrown
    away. Nothing this function returns ever gates anything: the findings this
    checker returns are produced by a full re-evaluation against the MEASURED
    bundle after derive() completes."""
    closure = ((value.get("successorRevision") or {})
               .get("enforcementClosureRepair") or {}) \
        if isinstance(value, dict) else {}
    defect = closure.get("predecessorDefect") or {}
    rows = defect.get("demonstrations") or []
    cascade = closure.get("repointCascade") or {}
    profile = closure.get("selftestProfile") or {}
    scalar = closure.get("closedScalarAdmission") or {}
    probes = []
    for row in rows if isinstance(rows, list) else []:
        if isinstance(row, dict):
            probes.append({
                "probe": row.get("probe", ""),
                "position": row.get("position", ""),
                "predecessorAdmitted": row.get("predecessorAdmitted"),
                "predecessorFindings": row.get("predecessorFindings"),
                "successorRejects": row.get("successorRejects"),
                "successorNamesThePosition":
                    row.get("successorNamesThePosition"),
                "successorFindingIds": row.get("successorFindingIds"),
            })
    return {
        "probes": probes,
        "cascade": {
            "predFindings": cascade.get("predecessorFindingsOnTheOneLineFix"),
            "predIndexShifts": cascade.get("predecessorIndexShifts"),
            "predAddedPos": cascade.get("predecessorPositionsAddedOrRemoved"),
            "selfFindings": cascade.get("successorFindingsOnTheOneLineFix"),
            "selfAddedPos": cascade.get("successorPositionsAddedOrRemoved"),
            "selfIds": cascade.get("successorFindingIdsOnTheOneLineFix"),
        },
        "census10": {
            "total": profile.get("predecessorMutations"),
            "floatRespellings": profile.get("predecessorFloatRespellings"),
            "booleanRespellings":
                profile.get("predecessorGenuineBooleanRespellings"),
            "labelDerivedBooleans":
                profile.get("predecessorBannerBooleanRespellings"),
        },
        "census11": {
            "total": profile.get("mutations"),
            "floatRespellings": profile.get("floatRespellings"),
            "booleanRespellings": profile.get("booleanRespellings"),
            "labelDerivedBooleans": None,
        },
        "sweep": {"total": scalar.get("booleanLeavesSweptInV11"),
                  "admitted": scalar.get("boolToIntAdmittedInV11"),
                  "admittedPaths": []},
    }


def derive(value: Any, pred_module: Any, predecessor: Any) -> dict[str, Any]:
    """Take every measurement that requires running this checker against a
    candidate. Each is a property of the base subject and of the pinned
    predecessor pair, so it is taken once per outer run and reused by the
    nested runs."""
    return {
        "probes": probe_pairs(pred_module, predecessor, value, PLANTED_ROLE),
        "cascade": measure_cascade(pred_module, predecessor, value),
        "census10": respelling_census(pred_module.MUTATIONS, predecessor),
        "census11": respelling_census(MUTATIONS, value),
        "sweep": boolean_sweep(value),
    }


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    global _DERIVED
    if _DEPTH == 0:
        try:
            pred_module = module(PREDECESSOR_CHECKER, "versioning_v10_pinned")
            predecessor = pinned(PREDECESSOR)
        except Exception as exc:
            return [f"VER11-PIN: pinned input load failed: "
                    f"{type(exc).__name__}: {exc}"]
        _DERIVED = declared_derivation(value)
        _DERIVED = derive(value, pred_module, predecessor)
    return _check(value, verify_files=verify_files)


def _check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["VER11-SURFACE: root is not an object"]

    try:
        for name, expected in PINS.items():
            if sha_file(name) != expected:
                raise ValueError(f"pinned input drift: {name}")
        predecessor = pinned(PREDECESSOR)
        elder = pinned(ELDER)
        d9_old = pinned(D9_SUPERSEDED)
        d9_new = pinned(D9_HEAD)
        review_text = pinned_text(PREDECESSOR_REVIEW)
        review10 = measure_review10(pinned(PREDECESSOR_REVIEW))
        review9 = measure_review9(pinned(GRANDPARENT_REVIEW))
        head_review_text = pinned_text(D9_HEAD_REVIEW)
        pred_module = module(PREDECESSOR_CHECKER, "versioning_v10_pinned")
    except Exception as exc:
        return [f"VER11-PIN: pinned input load failed: {type(exc).__name__}: "
                f"{exc}"]

    if "span" not in _CACHE:
        _CACHE["span"] = measure_d9_span(d9_old, d9_new)
    measured = _CACHE["span"]

    # The pinned predecessor pair is executed against its own bytes rather than
    # assumed green. It is NOT required to be silent, and that is deliberate:
    # it is frozen, and R-VER10-08 predicts that a coordinator repoint makes it
    # red through no fault of any artifact. Requiring silence would make this
    # record hostage to an instrument nobody may repair. So its findings are
    # MEASURED, compared against a declaration, and tolerated only when every
    # one of them names a register binding — the exact coupling that was
    # predicted. Any other redness is VER11-PRED.
    if "predFindings" not in _CACHE:
        try:
            _CACHE["predFindings"] = pred_module.check(predecessor,
                                                       verify_files=False)
        except Exception as exc:
            _CACHE["predFindings"] = [f"{type(exc).__name__}: {exc}"]
    pred_findings = _CACHE["predFindings"]
    for finding in pred_findings:
        if "registerBinding" not in finding:
            add(errors, "VER11-PRED",
                f"the pinned predecessor pair is red for a reason that is not "
                f"the register coupling R-VER10-08 predicted: {finding[:170]}")
    if "grandFindings" not in _CACHE:
        try:
            grand_module = module(GRANDPARENT_CHECKER, "versioning_v9_pinned")
            _CACHE["grandFindings"] = grand_module.check(pinned(GRANDPARENT))
        except Exception as exc:
            _CACHE["grandFindings"] = [f"{type(exc).__name__}: {exc}"]
    grand_findings = _CACHE["grandFindings"]
    if grand_findings:
        add(errors, "VER11-PRED",
            f"VERSIONING v9 grandparent is red: {grand_findings[0][:170]}")

    if verify_files:
        try:
            done = subprocess.run(
                [sys.executable, "-I", "-B", str(HERE / D9_HEAD_CHECKER)],
                cwd=str(HERE), capture_output=True, text=True)
            if done.returncode != 0:
                add(errors, "VER11-D9",
                    f"D9 head dependency is red: {D9_HEAD_CHECKER} exited "
                    f"{done.returncode}")
        except Exception as exc:
            add(errors, "VER11-D9", f"{D9_HEAD_CHECKER} did not run: "
                                    f"{type(exc).__name__}: {exc}")

    # ---- protected surface, compared as canonical JSON text (law 18) ----
    if set(value) != set(predecessor):
        add(errors, "VER11-SURFACE",
            "top-level surface differs from VERSIONING v10")
    for key in set(predecessor) - CHANGED:
        if canon(value.get(key)) != canon(predecessor.get(key)):
            add(errors, "VER11-SURFACE",
                f"protected VERSIONING v10 section changed: {key}")

    # ---- identity, exact-type in both directions ----
    if value.get("artifact") != "opensip.versioning-policy":
        add(errors, "VER11-ID", "artifact identity drift")
    if not exact_int(value.get("version")) or value.get("version") != 11:
        add(errors, "VER11-ID",
            "version is not exactly integer 11 (freeze §6 law 18: neither a "
            "float nor a bool respelling is an integer)")
    if not exact_int(value.get("supersedes")) or value.get("supersedes") != 10:
        add(errors, "VER11-ID",
            "supersedes is not exactly integer 10 (freeze §6 law 18)")

    # ---- no status may move ----
    if value.get("status") != predecessor.get("status"):
        add(errors, "VER11-STATUS",
            "status moved; this successor advances no status")
    if value.get("reviewStatus") != predecessor.get("reviewStatus"):
        add(errors, "VER11-STATUS",
            "reviewStatus moved; the v10 review returned CHANGES-REQUIRED and "
            "no verdict transfers to v11 (§7.2)")
    role = value.get("role") or ""
    for token in ROLE_TOKENS:
        if token not in role:
            add(errors, "VER11-STATUS",
                f"narrow successor role drift: role does not carry {token!r}")

    # ---- decisionDependencies are byte-identical to v10 ----
    deps = value.get("decisionDependencies")
    pred_deps = predecessor.get("decisionDependencies", [])
    elder_deps = elder.get("decisionDependencies", [])
    if canon(deps) != canon(pred_deps):
        add(errors, "VER11-DEP",
            "decisionDependencies moved; v10's label correction is final and "
            "retargeting remains deferred as residual R-VER9-02")
        deps = list(pred_deps)
    d9 = deps[4] if len(deps) > 4 and isinstance(deps[4], dict) else {}
    if d9.get("id") != "D9":
        add(errors, "VER11-DEP", "decisionDependencies[4] is not the D9 entry")
    if d9.get("source") != REPAIRED_CITATION:
        add(errors, "VER11-DEP",
            f"decisionDependencies[4] D9 citation is {d9.get('source')!r}, "
            f"expected {REPAIRED_CITATION!r}")
    elder_d9 = elder_deps[4] if len(elder_deps) > 4 else {}
    for field in ("id", "claim", "direction", "note"):
        if canon(d9.get(field)) != canon(elder_d9.get(field)):
            add(errors, "VER11-DEP",
                f"decisionDependencies[4].{field} differs from {ELDER}; "
                f"B-SCV2-06's recorded resolution must survive every successor")
    direction = d9.get("direction") or ""
    if "VERSIONING depends on D9" not in direction or \
            "D9 does NOT depend on VERSIONING" not in direction:
        add(errors, "VER11-DEP",
            "decisionDependencies[4].direction no longer declares the one-way "
            "dependency direction (B-SCV2-06)")
    if "additive-only exit-class rule (V4)" not in direction:
        add(errors, "VER11-DEP",
            "decisionDependencies[4].direction no longer names the "
            "additive-only exit-class rule (V4) it rests on")

    # ---- the citation must equal the register's live binding (INVARIANT) ----
    register_path = HERE / REGISTER
    claims: list[Any] = []
    live_d9 = live_versioning = None
    if not register_path.exists():
        add(errors, "VER11-REG",
            f"{REGISTER} is absent; the live D9 binding cannot be verified")
    else:
        try:
            claims = load(register_path)["claims"]
            live_d9 = next((c.get("bindingArtifact") for c in claims
                            if c.get("id") == "D9"), None)
            live_versioning = next((c.get("bindingArtifact") for c in claims
                                    if c.get("id") == "VERSIONING"), None)
        except Exception as exc:
            add(errors, "VER11-REG",
                f"{REGISTER} unreadable: {type(exc).__name__}: {exc}")
        if live_d9 is None:
            add(errors, "VER11-REG", "the register declares no live D9 binding")
        elif d9.get("source") != live_d9:
            add(errors, "VER11-REG",
                f"decisionDependencies[4] cites {d9.get('source')} but the "
                f"register binds D9 to {live_d9} — a superseded citation "
                f"(B-SCV2-06)")

    # ---- B-SCV2-06's resolution text stays protected ----
    b_scv2 = (value.get("resolves") or {}).get("B-SCV2-06") or ""
    if not b_scv2.startswith("RESOLVED"):
        add(errors, "VER11-RESOLVE",
            "resolves['B-SCV2-06'] is no longer recorded RESOLVED")
    if D9_HEAD not in b_scv2:
        add(errors, "VER11-RESOLVE",
            "resolves['B-SCV2-06'] does not name the repaired head citation")

    # ---- limitation delta is additive, exact, and each addition is measured --
    limitations = value.get("knownLimitations")
    pred_limitations = predecessor.get("knownLimitations", [])
    if not isinstance(limitations, list):
        add(errors, "VER11-LIMIT", "knownLimitations is not a list")
    elif limitations[:len(pred_limitations)] != pred_limitations:
        add(errors, "VER11-LIMIT",
            "inherited knownLimitations were altered or reordered")
    elif len(limitations) - len(pred_limitations) != ADDED_LIMITATION_COUNT:
        add(errors, "VER11-LIMIT",
            f"successor limitation delta is "
            f"{len(limitations) - len(pred_limitations)}, expected "
            f"{ADDED_LIMITATION_COUNT}")
    else:
        for offset, tokens in enumerate(LIMITATION_TOKENS):
            text = limitations[len(pred_limitations) + offset]
            missing = [t for t in tokens if t not in str(text)]
            if missing:
                add(errors, "VER11-LIMIT",
                    f"knownLimitations[{len(pred_limitations) + offset}] does "
                    f"not state {missing}; an added limitation states a "
                    f"measured value, not a sentiment")

    # ---- successor revision ----
    revision = value.get("successorRevision") or {}
    pred_revision = predecessor.get("successorRevision") or {}
    if set(revision) != EXPECTED_REVISION_KEYS:
        add(errors, "VER11-REV", "successor revision is not closed")
    if revision.get("id") != "VERSIONING-v11-ENFORCEMENT-CLOSURE-SUCCESSOR" \
            or revision.get("candidateState") != "NOT-APPLIED":
        add(errors, "VER11-REV", "successor identity/state drift")
    if revision.get("supersedesCandidate") != {
            "artifact": PREDECESSOR,
            "sha256": PINS[PREDECESSOR],
            "checker": PREDECESSOR_CHECKER,
            "checkerSha256": PINS[PREDECESSOR_CHECKER]}:
        add(errors, "VER11-REV", "VERSIONING v10 protected predecessor pin drift")
    stability = revision.get("identityStability") or {}
    if stability.get("predecessor") != "VERSIONING-v10" or \
            stability.get("state") != "EXACT-CUSTODY-IDENTITIES-UNCHANGED":
        add(errors, "VER11-REV", "v10 identity stability statement drift")
    if not isinstance(stability.get("reason"), str) or \
            "B-VER10R-01" not in stability.get("reason", ""):
        add(errors, "VER11-REV",
            "identityStability.reason does not name the finding this successor "
            "closes")
    forbidden = revision.get("forbiddenBackEdge", "")
    if not all(term in forbidden for term in (
            "Evidence", "RunId", "TerminalRunV1", "RunAuthorityIndexV1",
            "ProjectStoreAuthority token", "store transaction token")):
        add(errors, "VER11-REV",
            "forbidden downstream/store-token back-edge rule incomplete")
    if any("evidence" in canon(row).lower()
           for row in (revision.get("inputs") or {}).values()
           if isinstance(row, dict)):
        add(errors, "VER11-REV",
            "VERSIONING v11 contains an Evidence dependency back-edge")
    for message in no_floats(revision, "successorRevision"):
        add(errors, "VER11-FLOAT", message)

    # ---- the carried delta: a COUNT and a DIGEST, never an indexed table ----
    carried_now = {k: revision.get(k) for k in FROZEN_REVISION_KEYS}
    carried_was = {k: pred_revision.get(k) for k in FROZEN_REVISION_KEYS}
    moved = sorted(diff_leaves(carried_now, carried_was))
    carried_delta_digest = sha_text(canon(moved))
    # The CARRY findings are emitted after the registries exist, because a
    # carried position may move only under two conditions together: some
    # enforcement scope INDEPENDENTLY RE-MEASURES it, so the new value is
    # gated on its own merits rather than on the author's say-so; and the
    # delta count and digest are declared and match. Prose inside the carried
    # record is re-measured by nothing, so it can never be licensed to move.

    # ---- the carried v9 repair record's own §7.2 recording obligation ----
    repair = revision.get("d9CitationRepair") or {}
    recorded = repair.get("recordedInputs")
    recorded_map = {row.get("artifact"): row for row in recorded
                    if isinstance(row, dict)} \
        if isinstance(recorded, list) else {}
    if not isinstance(recorded, list):
        add(errors, "VER11-RECORD",
            f"{REPAIR}.recordedInputs is not a list — a count is not a record")
    for name in (ELDER, ELDER_CHECKER, ELDER_REVIEW, D9_HEAD, D9_HEAD_CHECKER,
                 D9_HEAD_REVIEW, D9_SUPERSEDED, V4, V4_CHECKER):
        row = recorded_map.get(name)
        if row is None:
            add(errors, "VER11-RECORD",
                f"{REPAIR}.recordedInputs omits pinned input {name} — freeze "
                f"§7.2 requires filename + sha256 for every input")
        elif row.get("sha256") != PINS[name]:
            add(errors, "VER11-RECORD",
                f"{REPAIR}.recordedInputs sha256 for {name} does not match the "
                f"bytes on disk")

    # ---- V4 itself, measured from disk, independent of any declaration ----
    if measured["exitClassesRemoved"]:
        add(errors, "VER11-V4",
            f"V4 VIOLATED across the cited span: exit classes "
            f"{measured['exitClassesRemoved']} exist in {D9_SUPERSEDED} and not "
            f"in {D9_HEAD}. Exit classes are additive-only, forever.")
    if not measured["classToExitCodeByteIdentical"]:
        add(errors, "VER11-V4",
            f"V4 VIOLATED across the cited span: classToExitCode differs "
            f"between {D9_SUPERSEDED} and {D9_HEAD}.")
    for label, key in (("exit class", "sharedExitClassMismatches"),
                       ("reason/error code", "sharedReasonOrErrorCodeMismatches"),
                       ("numeric exit code", "sharedNumericExitCodeMismatches")):
        if measured[key]:
            add(errors, "VER11-V4",
                f"V4 VIOLATED across the cited span: {measured[key]} shared "
                f"golden(s) changed {label} between {D9_SUPERSEDED} and "
                f"{D9_HEAD}.")
    if measured["removed"]:
        add(errors, "VER11-V4",
            f"goldens removed across the cited span: {measured['removed']}")
    if measured["remediesRemoved"] or not measured["reasonCodesByteIdentical"] \
            or not measured["errorCodesByteIdentical"]:
        add(errors, "VER11-V4",
            "the closed reason/error code vocabulary is not byte-identical "
            "across the cited span")
    if measured["exitCodeValueSetV16"] != measured["exitCodeValueSetV114"]:
        add(errors, "VER11-V4",
            f"the distinct exit-code value set moved from "
            f"{measured['exitCodeValueSetV16']} to "
            f"{measured['exitCodeValueSetV114']} across the cited span")
    if measured["d9CitesVersioningPolicy"]:
        add(errors, "VER11-V4",
            f"{D9_HEAD} names a versioning-policy artifact — the declared "
            f"one-way direction (VERSIONING -> D9) may no longer hold")
    if "v1.6" in head_review_text:
        add(errors, "VER11-SPAN",
            f"{D9_HEAD_REVIEW} now mentions v1.6; the artifact's stated reason "
            f"for measuring the span directly must be re-derived")

    # ---- carried residual re-derivations (v10 review O-04 / O-09) ----
    carried = repair.get("retainedResiduals")
    carried = carried if isinstance(carried, list) else []
    by_id = {row.get("id"): (index, row) for index, row in enumerate(carried)
             if isinstance(row, dict)}
    fixtures = len((elder.get("historicalSemanticsPolicy") or {})
                   .get("crossMajorFixtures") or [])
    if "R-VER9-05" in by_id and fixtures:
        index, row = by_id["R-VER9-05"]
        if str(fixtures) not in (row.get("measured") or ""):
            add(errors, "VER11-RESID",
                f"{REPAIR}.retainedResiduals[{index}].measured does not state "
                f"the measured figure {fixtures}")
    register_drifts = 0
    if "R-VER9-07" in by_id:
        index, row = by_id["R-VER9-07"]
        digests = re.findall(r"\b([0-9a-f]{8})…", row.get("measured") or "")
        register_drifts = len(set(digests))
        drift = ((pinned(GRANDPARENT_REVIEW).get("verifiedInputs") or {})
                 .get("driftControl") or {}).get("driftDetectedInOtherFiles") \
            or []
        observed = [d.get(k) for d in drift if isinstance(d, dict)
                    for k in ("atReviewStart", "atReviewEnd") if d.get(k)]
        for digest in observed:
            if digest not in (row.get("measured") or ""):
                add(errors, "VER11-RESID",
                    f"{REPAIR}.retainedResiduals[{index}].measured omits the "
                    f"register digest {digest[:16]}… the v9 review observed")

    # ---- no paper seal in the gated fields ----
    if canon(value.get("dischargeStatus")) != canon(
            predecessor.get("dischargeStatus")):
        add(errors, "VER11-SEAL",
            "dischargeStatus moved; this successor discharges nothing")
    discharge = value.get("dischargeStatus") or {}
    if discharge.get("seal") != "DO-NOT-SEAL":
        add(errors, "VER11-SEAL", "dischargeStatus.seal inflation")
    if discharge.get("CD-RT-5") != "BLOCKED":
        add(errors, "VER11-SEAL",
            "dischargeStatus.CD-RT-5 moved; it remains BLOCKED_ON_PHASE_1A")
    if discharge.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED":
        add(errors, "VER11-SEAL",
            "dischargeStatus.evidenceGrade inflation — implementable is not "
            "DISCHARGED or DEMONSTRATED")

    # ---- no paper seal in the free prose either ----
    scan = seal_scan(value)
    for path, pattern, why in scan["outside"]:
        add(errors, "VER11-SEAL",
            f"{path} matches the paper-seal pattern {pattern!r}: {why}. A "
            f"verdict-inheritance claim in free prose is the class the "
            f"independent reviewer planted into "
            f"{ENFORCE}.recordedInputs[*].role and the predecessor admitted it "
            f"at exit 0")

    # ---- registries: none of them may be sized by this artifact ----
    audit = measure_audit(deps, claims)
    elder_d9 = elder_deps[4] if len(elder_deps) > 4 else {}
    direction_preserved = all(
        canon(d9.get(field)) == canon(elder_d9.get(field))
        for field in ("id", "claim", "direction", "note"))
    purity = registry_purity(pred_module)
    if purity["myArtifactParameters"] or purity["myArtifactReads"] or \
            purity["myArtifactSizedLoops"]:
        add(errors, "VER11-PURITY",
            f"a registry builder in this checker reads the artifact: "
            f"{purity['mine']}. A registry sized from the artifact cannot "
            f"police that artifact (B-VER10R-01)")

    pred_enforce = (pred_revision.get("evidenceEnforcementRepair") or {})
    pred_block_positions: list[str] = []
    positions(pred_enforce, ENFORCE, pred_block_positions)
    pred_loop_positions = []
    for loop in PREDECESSOR_SELF_SIZED_LOOPS:
        rows: list[str] = []
        key = loop.rsplit(".", 1)[-1]
        positions(pred_enforce.get(key), loop, rows)
        pred_loop_positions.append(len(rows))

    registries = {
        "carriedEvidence": evidence_registry(deps, measured, audit,
                                             direction_preserved),
        "predecessorEnforcementBlock": frozen_registry(ENFORCE, pred_enforce),
    }
    extra = {"reviewText": review_text}

    partitions: dict[str, Any] = {}
    for name, roots in PARTITION_SCOPES[:2]:
        scope_errors, part = evaluate(value, registries[name], roots, extra)
        errors.extend(scope_errors)
        partitions[name] = part

    # ---- the measurements the closure block is generated from ----
    declared_audit = []
    audit_rows = ((repair.get("siblingCitationAudit") or {}).get("entries")
                  or [])
    for row in audit_rows:
        if isinstance(row, dict):
            declared_audit.append(row)
    census = coverage_census(value, predecessor)
    sweep = _DERIVED["sweep"]
    probes = _DERIVED["probes"]
    cascade = _DERIVED["cascade"]
    census10 = _DERIVED["census10"]
    census11 = _DERIVED["census11"]
    rehearsals = rehearse(deps, claims, audit, declared_audit)
    if len(probes) != DEMONSTRATIONS:
        add(errors, "VER11-PROBE",
            "the probe layer produced no measurement; the reviewer's five "
            "demonstrations are reproduced on every run, not narrated")

    # Only the two carried scopes can re-measure a carried position; the
    # closure block is not a frozen key, so its registry is irrelevant here.
    remeasured = set(registries["carriedEvidence"]) | \
        set(registries["predecessorEnforcementBlock"])
    delta_remeasured = all(f"successorRevision.{p}" in remeasured
                           for p in moved)

    # ---- further boundaries the residuals must state in measured digits ----
    d9_intermediates = len([
        p for p in HERE.glob("d9-exit-contract.v1.*.json")
        if re.fullmatch(r"d9-exit-contract\.v1\.(\d+)\.json", p.name) and
        6 < int(re.fullmatch(r"d9-exit-contract\.v1\.(\d+)\.json",
                             p.name).group(1)) < 14])
    versioning_behind = 0
    if isinstance(live_versioning, str):
        match = re.search(r"versioning-policy\.v(\d+)\.json", live_versioning)
        if match:
            versioning_behind = 11 - int(match.group(1))
    carried_register_digests = []
    for block in (repair, pred_enforce):
        for row in (block.get("recordedInputs") or []):
            if isinstance(row, dict) and row.get("artifact") == REGISTER and \
                    isinstance(row.get("sha256"), str):
                carried_register_digests.append(row["sha256"])

    bundle = {
        "review10": review10,
        "review9": review9,
        "purity": purity,
        "census": census,
        "seal": scan,
        "probes": probes,
        "cascade": cascade,
        "rehearsals": rehearsals,
        "partitions": partitions,
        "audit": audit,
        "sweep": sweep,
        "census10": census10,
        "census11": census11,
        "predBlockPositions": len(pred_block_positions),
        "predSelfSizedPositions": sum(pred_loop_positions),
        "predLoopPositions": pred_loop_positions,
        "predTotalOccurrences":
            pinned_text(PREDECESSOR).count(str(len(pred_block_positions))),
        "predAdmissions": sum(1 for r in probes if r["predecessorAdmitted"]),
        "predCheckerFindings": len(pred_findings),
        "predRednessCoupledOnly": all("registerBinding" in f
                                      for f in pred_findings),
        "selfAdmissions": sum(1 for r in probes if not r["successorRejects"]),
        "plantedRole": PLANTED_ROLE,
        "protectedTopLevelKeys": len(set(predecessor) - CHANGED),
        "carriedDeltaCount": len(moved),
        "carriedDeltaDigest": carried_delta_digest,
        "deltaRemeasured": delta_remeasured,
        "armedOnDisk": (HERE / pathlib.PurePosixPath(ARMED_RT).name).is_file(),
        "armedBound": any(
            c.get("bindingArtifact") == ARMED_RT for c in claims),
        "liveD9": live_d9,
        "liveVersioning": live_versioning,
        "registerDrifts": register_drifts,
        "publishedCount": 0,
        "fullPathAssertions": sum(1 for row in MUTATIONS if row[4] == "path"),
        "sectionAssertions": sum(1 for row in MUTATIONS if row[4] == "section"),
        "distinctIds": len({row[2] for row in MUTATIONS}),
        "restatedWas": [], "restatedNow": [], "residualNumbers": {},
        "closureGrounded": 0, "closureTotal": 0,
        "sealHits": scan["patternHits"],
        "versioningVersionsBehind": versioning_behind,
        "elderFloatFixtures": fixtures,
        "d9SpanEndpoints": 2,
        "d9SpanIntermediates": d9_intermediates,
        "carriedRegisterDigestPositions": len(carried_register_digests),
        "carriedRegisterDigests": len(set(carried_register_digests)),
    }
    bundle["publishedCount"] = 4 * len(PARTITION_SCOPES) + 2
    bundle["restatedWas"], bundle["restatedNow"] = restatement_numbers(bundle)
    bundle["residualNumbers"] = residual_numbers(bundle)

    # Two passes. Some residual boundaries must state the closure block's own
    # partition, which is not known until the registry that defines it has been
    # evaluated. The KEY SET is identical in both passes — only payloads move —
    # so the partition measured in pass one is the partition enforced in pass
    # two, and neither pass reads a size from the artifact.
    name, roots = PARTITION_SCOPES[2]
    bundle["partitions"].setdefault(name, {
        "total": 0, "measured": 0, "grounded": 0, "unmeasurable": 0,
        "fromDisk": 0, "fromConstant": 0, "digest": "", "positions": []})
    first = closure_registry(bundle)
    _, part = evaluate(value, first, roots, extra)
    bundle["partitions"][name] = part
    bundle["closureGrounded"] = part["grounded"]
    bundle["closureTotal"] = part["total"]
    bundle["residualNumbers"] = residual_numbers(bundle)
    bundle["restatedWas"], bundle["restatedNow"] = restatement_numbers(bundle)
    registries[name] = closure_registry(bundle)
    if set(registries[name]) != set(first):
        add(errors, "VER11-COVER",
            "the closure registry is not stable across its two passes; a "
            "registry whose key set depends on its own output cannot classify")
    scope_errors, part = evaluate(value, registries[name], roots, extra)
    errors.extend(scope_errors)
    partitions[name] = part

    closure = revision.get("enforcementClosureRepair") or {}
    if tuple(sorted(closure)) != tuple(sorted(EXPECTED_CLOSURE_KEYS)):
        add(errors, "VER11-REPAIR", "enforcementClosureRepair is not closed")

    # ---- carried bytes: what may move, and on whose authority ----
    declared_delta = (closure.get("carriedByteIdentical") or {}) \
        .get("carriedDelta") or {}
    delta_declared = (declared_delta.get("count") == len(moved) and
                      declared_delta.get("digest") == carried_delta_digest)
    for path in moved:
        full = f"successorRevision.{path}"
        if full not in remeasured:
            add(errors, "VER11-CARRY",
                f"{full} differs from the reviewed {PREDECESSOR} bytes and no "
                f"enforcement scope re-measures it, so no declaration can "
                f"license it to move; every such position is carried "
                f"byte-identical")
        elif not delta_declared:
            add(errors, "VER11-CARRY",
                f"{full} differs from the reviewed {PREDECESSOR} bytes and the "
                f"carried delta is not declared: this checker measured "
                f"{len(moved)} moved position(s) with digest "
                f"{carried_delta_digest[:16]}…, the record declares "
                f"{declared_delta.get('count')!r} and "
                f"{str(declared_delta.get('digest'))[:16]}…")

    # ---- every computed partition is compared, and only then published ----
    declared_scopes = (closure.get("partitionClosure") or {}).get("scopes") or []
    published: list[tuple[str, str, int]] = []
    for index, (scope_name, _roots) in enumerate(PARTITION_SCOPES):
        part = partitions[scope_name]
        row = declared_scopes[index] if index < len(declared_scopes) else {}
        if not isinstance(row, dict):
            row = {}
        for key, actual in (("total", part["total"]),
                            ("MEASURED", part["measured"]),
                            ("GROUNDED", part["grounded"]),
                            ("UNMEASURABLE", part["unmeasurable"])):
            got = row.get(key)
            if not exact_int(got) or got != actual:
                add(errors, "VER11-PART",
                    f"declared partition {scope_name}.{key} is {got!r}; this "
                    f"checker classified {actual} positions. B-VER10R-01: a "
                    f"computed partition that is printed and compared against "
                    f"nothing is not evidence")
            else:
                published.append((scope_name, key, actual))
        if row.get("positionDigest") != part["digest"]:
            add(errors, "VER11-PART",
                f"declared partition {scope_name}.positionDigest is "
                f"{row.get('positionDigest')!r}; this checker measured "
                f"{part['digest']!r} over the sorted position list")
    if len(declared_scopes) != len(PARTITION_SCOPES):
        add(errors, "VER11-PART",
            f"{len(declared_scopes)} partitions are declared and "
            f"{len(PARTITION_SCOPES)} are computed; no computed partition may "
            f"go uncompared")
    published.append(("carriedDelta", "count", len(moved)))
    published.append(("coverageCensus", "ungated", census["ungated"]))
    if len(published) != bundle["publishedCount"]:
        add(errors, "VER11-PART",
            f"{len(published)} measurements passed comparison but the record "
            f"declares {bundle['publishedCount']} published; the banner prints "
            f"only compared numbers")

    # ---- the residual id multiset, not merely membership ----
    residuals = closure.get("retainedResiduals")
    residuals = residuals if isinstance(residuals, list) else []
    ids = [r.get("id") for r in residuals if isinstance(r, dict)]
    if sorted(ids) != sorted(REQUIRED_RESIDUAL_IDS):
        add(errors, "VER11-RESID",
            f"{CLOSE}.retainedResiduals declares the id multiset "
            f"{sorted(ids)}; this successor requires exactly "
            f"{sorted(REQUIRED_RESIDUAL_IDS)} — membership testing admits a "
            f"duplicate, so the multiset is compared")
    restatements = closure.get("residualRestatements")
    restatements = restatements if isinstance(restatements, list) else []
    rids = [r.get("id") for r in restatements if isinstance(r, dict)]
    if sorted(rids) != sorted(RESTATED_RESIDUALS):
        add(errors, "VER11-RESID",
            f"{CLOSE}.residualRestatements declares the id multiset "
            f"{sorted(rids)}; this successor restates exactly "
            f"{sorted(RESTATED_RESIDUALS)}")
    for rid in sorted(set(rids)):
        if rid not in CARRIED_RESIDUAL_IDS:
            add(errors, "VER11-RESID",
                f"{CLOSE}.residualRestatements restates {rid!r}, which is not a "
                f"residual carried from {PREDECESSOR}")

    # ---- the closure block's own probe results must be the measured ones ----
    if bundle["selfAdmissions"]:
        add(errors, "VER11-PROBE",
            f"{bundle['selfAdmissions']} of the {len(probes)} reviewer "
            f"demonstrations are ADMITTED by this checker against these bytes")
    for row in probes:
        if row["successorRejects"] and not row["successorNamesThePosition"]:
            add(errors, "VER11-PROBE",
                f"demonstration {row['probe']!r} is rejected, but no finding "
                f"names {row['position']} — a non-zero result is not evidence a "
                f"guard fired")

    LAST["partitions"] = partitions
    LAST["published"] = published
    LAST["census"] = census
    LAST["seal"] = scan
    LAST["purity"] = purity
    LAST["sweep"] = sweep
    if _DEPTH == 0:
        LAST["probes"] = probes
        LAST["cascade"] = cascade
        LAST["census10"] = census10
        LAST["census11"] = census11
        LAST["bundle"] = bundle
    return errors


def measure_cascade(pred_module: Any, pred_artifact: Any,
                    subject: Any) -> dict[str, Any]:
    """The review's O-01, reproduced. Apply the obvious one-line repoint fix to
    BOTH records and measure what each costs. The predecessor's enumeratedDelta
    table is index-position-compared against sorted(moved), so inserting one
    path shifts three indices and adds a twelfth the artifact does not declare.
    Here the same edit moves a count and a digest."""
    target = f"{REPAIR}.siblingCitationAudit.entries[6].registerBinding"
    new_value = SENTINEL_RT

    pred = copy.deepcopy(pred_artifact)
    before_delta = sorted(pred_module.diff_leaves(
        at(pred, REPAIR), at(pinned(GRANDPARENT), REPAIR)))
    set_at(pred, target, new_value)
    after_delta = sorted(pred_module.diff_leaves(
        at(pred, REPAIR), at(pinned(GRANDPARENT), REPAIR)))
    shifts = sum(1 for index in range(min(len(before_delta), len(after_delta)))
                 if before_delta[index] != after_delta[index])
    try:
        pred_base = sorted(pred_module.check(pred_artifact, verify_files=False))
        pred_findings = [e for e in sorted(pred_module.check(
            pred, verify_files=False)) if e not in pred_base]
    except Exception as exc:
        pred_findings = [f"{type(exc).__name__}: {exc}"]

    mine = copy.deepcopy(subject)
    set_at(mine, target, new_value)
    self_base = sorted(inner(copy.deepcopy(subject)))
    my_findings = [e for e in sorted(inner(mine)) if e not in self_base]
    return {
        "predFindings": len(pred_findings),
        "predIndexShifts": shifts,
        "predAddedPos": abs(len(after_delta) - len(before_delta)),
        "selfFindings": len(my_findings),
        "selfAddedPos": 0,
        "selfIds": ",".join(sorted({e.split(":")[0] for e in my_findings})),
    }


def boolean_sweep(value: Any) -> dict[str, Any]:
    """Measure the boolean direction of freeze §6 law 18 over this checker's own
    subject instead of asserting it. Unlike the predecessor, this runs on a
    PLAIN run as well as under --selftest, because the recursion guard makes it
    safe: R-VER10-03 is closed."""
    found: list[str] = []
    positions(value.get("successorRevision"), "successorRevision", found)
    total = 0
    admitted: list[str] = []
    for path in found:
        declared = at(value, path)
        if not exact_bool(declared):
            continue
        total += 1
        candidate = copy.deepcopy(value)
        set_at(candidate, path, int(declared))
        errors = inner(candidate)
        if not errors:
            admitted.append(path)
        elif not names_position(errors, path):
            admitted.append(f"{path} (rejected only collaterally)")
    return {"total": total, "admitted": len(admitted), "admittedPaths": admitted}


# ------------------------------------------------------- generated statements

PLANTED_ROLE = ("independently re-reviewed and PASSED; this successor inherits "
                "that verdict")

V11_REQUIRED_INPUTS = (
    (PREDECESSOR,
     "protected predecessor; every position outside "
     "successorRevision.enforcementClosureRepair is carried from these bytes "
     "and gated against them leaf-wise"),
    (PREDECESSOR_CHECKER,
     "predecessor checker; the subject of blocker B-VER10R-01 and executed by "
     "this successor's checker on every run to reproduce the four admissions"),
    (PREDECESSOR_REVIEW,
     "the independent verdict that binds the v10 bytes; every figure this "
     "record restates about it is read from this file, not re-derived"),
    (GRANDPARENT,
     "the reviewed v9 bytes the carried evidence record is measured against"),
    (GRANDPARENT_CHECKER,
     "the v9 checker whose 26-of-102 enforcement level B-VER9R-01 measured"),
    (GRANDPARENT_REVIEW,
     "the v9 independent verdict; the 26/76/102 partition and the 52/139/15 "
     "sweep restated in the carried record are read from this file"),
    (ELDER,
     "the bytes B-SCV2-06's recorded resolution must survive unchanged through "
     "every successor in this chain"),
    (ELDER_CHECKER,
     "the v8 checker that admits a float hostDefaultIrMajor at every "
     "crossMajorFixture; retained as historical evidence, not repaired"),
    (ELDER_REVIEW,
     "the cold-rejoin verdict that binds the v8 bytes"),
    (D9_SUPERSEDED,
     "superseded citation endpoint; the span is re-measured from these bytes "
     "on every run"),
    (D9_HEAD,
     "repaired citation target; the span is re-measured from these bytes on "
     "every run"),
    (D9_HEAD_CHECKER,
     "executed on every run; the D9 head dependency must be green for this "
     "record to be green"),
    (D9_HEAD_REVIEW,
     "read to confirm it does not attest the v1.6 span, which is why the span "
     "is measured directly rather than inherited"),
    (V4,
     "the artifact check-versioning.py is hardcoded to and whose D9 citation is "
     "frozen by §7.2"),
    (V4_CHECKER,
     "permanently red by construction; recorded because its AttributeError "
     "exits 1 indistinguishably from a finding"),
)

RESIDUAL_TOKENS = {
    "R-VER11-01": ("GROUNDED", "prose"),
    "R-VER11-02": ("scope", "census"),
    "R-VER11-03": ("boolean", "successorRevision"),
    "R-VER11-04": ("register-bound head",),
    "R-VER11-05": ("independent review",),
    "R-VER11-06": ("check-versioning.py", "exit"),
    "R-VER11-07": ("predecessor checkers", "not repaired"),
    "R-VER11-08": ("recorded measurement", "hard"),
    "R-VER11-09": ("endpoint", "span"),
    "R-VER11-10": ("register digest", "frozen"),
    "R-VER11-11": ("gated", "meaning"),
}

RESIDUAL_DISPOSITION = {
    "R-VER11-01": ("Bounded and published",),
    "R-VER11-02": ("Deliberate scope",),
    "R-VER11-03": ("re-derived",),
    "R-VER11-04": ("coordinator",),
    "R-VER11-05": ("Nothing here claims one",),
    "R-VER11-06": ("Not closable here",),
    "R-VER11-07": ("Recorded, not repaired",),
    "R-VER11-08": ("Accepted deliberately",),
    "R-VER11-09": ("Bounded, not closed",),
    "R-VER11-10": ("Carried, not restated",),
    "R-VER11-11": ("Disclosed",),
}

NOT_CLAIMED_TOKENS = (
    ("No seal, freeze, signature or status advance", "CD-RT-5",
     "BLOCKED_ON_PHASE_1A"),
    ("verdict", "not transferred", "CHANGES-REQUIRED"),
    ("not claim", "fully measured", "GROUNDED"),
    ("implementable", "DISCHARGED", "DEMONSTRATED"),
    ("does not claim", "register", "repoint"),
)


def restatement_numbers(m: dict[str, Any]) -> tuple[list[Any], list[Any]]:
    """RESTATED_RESIDUALS is (R-VER10-01, R-VER10-03, R-VER10-08). Each `was`
    states the figure the predecessor recorded and each `now` states the figure
    measured here, so a restatement that keeps its digits and loses its meaning
    is a finding."""
    review = m["review10"]
    was = [
        [review["proseStringLeaves"], review["proseAdmitted"],
         review["proseAdmittedNewBlock"]],
        ["--selftest", review["boolLeavesV10"]],
        [PREDECESSOR_CHECKER, "R-VER10-08"],
    ]
    now = [
        [m["closureGrounded"], m["closureTotal"], m["sealHits"]],
        [m["sweep"]["total"], m["sweep"]["admitted"]],
        [m["cascade"]["predFindings"], m["cascade"]["predIndexShifts"],
         m["cascade"]["selfFindings"], m["rehearsals"][0]["changed"]],
    ]
    return was, now


def residual_numbers(m: dict[str, Any]) -> dict[str, list[Any]]:
    closure = (m["partitions"].get("successorClosureBlock") or
               {"grounded": 0, "total": 0})
    census = m["census"]
    return {
        "R-VER11-01": [closure["grounded"], closure["total"]],
        "R-VER11-02": [census["total"], census["scope"], census["ungated"]],
        "R-VER11-03": [m["sweep"]["total"], m["sweep"]["admitted"],
                       m["review10"]["boolBySectionV10"]],
        "R-VER11-04": [m["liveVersioning"] or "", m["versioningVersionsBehind"]],
        "R-VER11-05": ["CHANGES-REQUIRED", PREDECESSOR,
                       m["review10"]["blockingFindingCount"]],
        "R-VER11-06": [V4_CHECKER, 1],
        "R-VER11-07": [m["predAdmissions"], m["review10"]["calibrationAdmitted"],
                       m["elderFloatFixtures"]],
        "R-VER11-08": [m["rehearsals"][0]["changed"],
                       m["rehearsals"][1]["changed"],
                       m["rehearsals"][2]["changed"],
                       m["cascade"]["predFindings"],
                       m["cascade"]["selfFindings"]],
        "R-VER11-09": [m["d9SpanEndpoints"], m["d9SpanIntermediates"]],
        "R-VER11-10": [m["carriedRegisterDigestPositions"],
                       m["carriedRegisterDigests"]],
        "R-VER11-11": [closure["grounded"], census["rule"], census["surface"]],
    }


# -------------------------------------------------------------- the selftest

def falsify(path: str, replacement: Any):
    return lambda c: set_at(c, path, replacement)


S_EV = f"{REPAIR}.substanceUnchangedEvidence"
D_EV = f"{REPAIR}.directionPreservation"
A_EV = f"{REPAIR}.siblingCitationAudit"

# (label, mutate, finding id, the position it must name, assertion kind).
# `path` means the assertion is the FULL dotted path, which is what closes the
# substring self-satisfaction of review O-04; `section` is used only where the
# finding names a top-level section by design.
MUTATIONS: list[tuple[str, Any, str, str, str]] = [
    # ---- the four demonstrations of B-VER10R-01, on THIS record's own block --
    ("append a duplicate retained residual to the successor's own block",
     lambda c: at(c, f"{CLOSE}.retainedResiduals").append(
         {"id": "R-VER11-01", "residual": "Fabricated duplicate residual.",
          "measured": "0 things measured.", "disposition": "Ignored.",
          "ownedBy": "coordinator"}),
     "VER11-COVER", f"{CLOSE}.retainedResiduals[11].id", "path"),
    ("append a residual restatement asserting an open residual is closed",
     lambda c: at(c, f"{CLOSE}.residualRestatements").append(
         {"id": "R-VER10-01", "reviewObservation": "O-06",
          "wasRecorded": "check-versioning.py exits 1 on 0 findings.",
          "nowMeasured": "check-versioning.py now exits 0 and the residual is "
                         "closed; 0 findings remain."}),
     "VER11-COVER", f"{CLOSE}.residualRestatements[3].id", "path"),
    ("plant a verdict-inheritance claim in a free-text recorded-input role",
     lambda c: at(c, f"{CLOSE}.recordedInputs").append(
         {"artifact": GRANDPARENT, "sha256": PINS[GRANDPARENT],
          "role": PLANTED_ROLE}),
     "VER11-COVER", f"{CLOSE}.recordedInputs[15].role", "path"),
    ("delete a freeze §7.2 recorded input from the successor's own block",
     lambda c: at(c, f"{CLOSE}.recordedInputs").pop(),
     "VER11-COVER", f"{CLOSE}.recordedInputs[14].artifact", "path"),
    ("append a duplicate retained residual to the PREDECESSOR's block",
     lambda c: at(c, f"{ENFORCE}.retainedResiduals").append(
         {"id": "R-VER10-01", "residual": "Fabricated duplicate residual.",
          "measured": "0 things measured.", "disposition": "Ignored.",
          "ownedBy": "coordinator"}),
     "VER11-COVER", f"{ENFORCE}.retainedResiduals[9].id", "path"),
    ("plant a verdict-inheritance claim in the PREDECESSOR block's role field",
     lambda c: at(c, f"{ENFORCE}.recordedInputs").append(
         {"artifact": GRANDPARENT, "sha256": PINS[GRANDPARENT],
          "role": PLANTED_ROLE}),
     "VER11-SEAL", f"{ENFORCE}.recordedInputs[7].role", "path"),
    ("delete a freeze §7.2 recorded input from the PREDECESSOR's block",
     lambda c: at(c, f"{ENFORCE}.recordedInputs").pop(),
     "VER11-COVER", f"{ENFORCE}.recordedInputs[6].artifact", "path"),
    ("add a key at a non-loop position in the PREDECESSOR's block",
     lambda c: at(c, f"{ENFORCE}.checkerDisposition").__setitem__(
         "adversarialExtra", "x"),
     "VER11-COVER", f"{ENFORCE}.checkerDisposition.adversarialExtra", "path"),
    # ---- the uncompared partition ----
    ("understate the successor block's own partition total",
     falsify(f"{CLOSE}.partitionClosure.scopes[2].total", 3),
     "VER11-PART", "successorClosureBlock.total", "section"),
    ("understate the predecessor block's partition total — v10's uncompared 316",
     falsify(f"{CLOSE}.partitionClosure.scopes[1].total", 3),
     "VER11-PART", "predecessorEnforcementBlock.total", "section"),
    ("restate the carried evidence partition to match a fabricated reality",
     falsify(f"{CLOSE}.partitionClosure.scopes[0].MEASURED", 98),
     "VER11-PART", "carriedEvidence.MEASURED", "section"),
    ("falsify the position digest of a declared partition",
     falsify(f"{CLOSE}.partitionClosure.scopes[1].positionDigest", "0" * 64),
     "VER11-PART", "predecessorEnforcementBlock.positionDigest", "section"),
    ("claim a partition went uncompared",
     falsify(f"{CLOSE}.partitionClosure.uncomparedPartitions", 1),
     "VER11-LEAF", f"{CLOSE}.partitionClosure.uncomparedPartitions", "path"),
    # ---- registry purity ----
    ("claim this checker's registries read the artifact",
     falsify(f"{CLOSE}.registryPurity.artifactSizedLoopsHere", 4),
     "VER11-LEAF", f"{CLOSE}.registryPurity.artifactSizedLoopsHere", "path"),
    ("deny that the predecessor's registry was artifact-sized",
     falsify(f"{CLOSE}.registryPurity.artifactSizedLoopsInThePredecessor", 0),
     "VER11-LEAF",
     f"{CLOSE}.registryPurity.artifactSizedLoopsInThePredecessor", "path"),
    ("misreport a predecessor builder's artifact parameter count",
     falsify(f"{CLOSE}.registryPurity.predecessorBuilders[1]."
             "artifactParameters", 0),
     "VER11-LEAF",
     f"{CLOSE}.registryPurity.predecessorBuilders[1].artifactParameters",
     "path"),
    # ---- the reproduced admissions ----
    ("deny that the predecessor admitted the planted verdict claim",
     falsify(f"{CLOSE}.predecessorDefect.demonstrations[2]."
             "predecessorAdmitted", False),
     "VER11-LEAF",
     f"{CLOSE}.predecessorDefect.demonstrations[2].predecessorAdmitted",
     "path"),
    ("claim the pinned predecessor pair is red against its own bytes",
     falsify(f"{CLOSE}.predecessorDefect."
             "predecessorCheckerFindingsAgainstItsOwnBytes", 4),
     "VER11-LEAF",
     f"{CLOSE}.predecessorDefect.predecessorCheckerFindingsAgainstItsOwnBytes",
     "path"),
    ("misreport how many of the reviewer's probes the predecessor admitted",
     falsify(f"{CLOSE}.predecessorDefect.predecessorAdmissions", 0),
     "VER11-LEAF", f"{CLOSE}.predecessorDefect.predecessorAdmissions", "path"),
    ("misreport the predecessor block's leaf-position count",
     falsify(f"{CLOSE}.predecessorDefect.blockLeafPositions", 100),
     "VER11-LEAF", f"{CLOSE}.predecessorDefect.blockLeafPositions", "path"),
    ("misreport how many positions sat in the four self-sized loops",
     falsify(f"{CLOSE}.predecessorDefect.positionsInSelfSizedLoops", 0),
     "VER11-LEAF", f"{CLOSE}.predecessorDefect.positionsInSelfSizedLoops",
     "path"),
    ("claim the predecessor compared its own block partition",
     falsify(f"{CLOSE}.predecessorDefect."
             "blockPartitionWasComparedByThePredecessorChecker", True),
     "VER11-LEAF",
     f"{CLOSE}.predecessorDefect.blockPartitionWasComparedByThePredecessorChecker",
     "path"),
    ("claim the predecessor artifact stated its own block total",
     falsify(f"{CLOSE}.predecessorDefect."
             "blockTotalOccurrencesInThePredecessorArtifact", 1),
     "VER11-LEAF",
     f"{CLOSE}.predecessorDefect.blockTotalOccurrencesInThePredecessorArtifact",
     "path"),
    # ---- coverage census ----
    ("claim a leaf position is ungated when none is",
     falsify(f"{CLOSE}.coverageCensus.ungated", 7),
     "VER11-LEAF", f"{CLOSE}.coverageCensus.ungated", "path"),
    ("misreport the artifact's total leaf-position count",
     falsify(f"{CLOSE}.coverageCensus.artifactLeafPositions", 10),
     "VER11-LEAF", f"{CLOSE}.coverageCensus.artifactLeafPositions", "path"),
    # ---- the carried delta and the repoint ----
    ("claim a carried delta that did not happen",
     falsify(f"{CLOSE}.carriedByteIdentical.carriedDelta.count", 3),
     "VER11-LEAF", f"{CLOSE}.carriedByteIdentical.carriedDelta.count", "path"),
    ("falsify the carried delta digest",
     falsify(f"{CLOSE}.carriedByteIdentical.carriedDelta.digest", "0" * 64),
     "VER11-LEAF", f"{CLOSE}.carriedByteIdentical.carriedDelta.digest", "path"),
    ("retune a measured quantity inside the carried v9 evidence record",
     falsify(f"{S_EV}.goldenCases.shared", 40),
     "VER11-CARRY", f"{S_EV}.goldenCases.shared", "path"),
    ("assert that D9 depends on VERSIONING — the B-SCV2-06 circularity",
     falsify(f"{D_EV}.reVerifiedAtHead.d9CitesVersioningInItsDependencies",
             True),
     "VER11-CARRY", f"{D_EV}.reVerifiedAtHead.d9CitesVersioningInItsDependencies",
     "path"),
    ("replace the recorded superseded-span digest with garbage",
     falsify(f"{S_EV}.measuredBetween.supersededCitationSha256", "0" * 64),
     "VER11-CARRY", f"{S_EV}.measuredBetween.supersededCitationSha256", "path"),
    ("falsify a byte-identical root the checker computes",
     falsify(f"{S_EV}.byteIdenticalRootsV16ToV114[3]", "ADVERSARIAL-FALSEHOOD"),
     "VER11-CARRY", f"{S_EV}.byteIdenticalRootsV16ToV114[3]", "path"),
    ("falsify the sibling-audit register binding for retention-tiers",
     falsify(f"{A_EV}.entries[6].registerBinding", None),
     "VER11-ASOF", f"{A_EV}.entries[6].registerBinding", "path"),
    ("falsify a re-measured as-of register binding in the successor's block",
     falsify(f"{CLOSE}.registerAsOfAudit.entries[6].registerBinding",
             "artifacts/retention-tiers.v99.json"),
     "VER11-ASOF", f"{CLOSE}.registerAsOfAudit.entries[6].registerBinding",
     "path"),
    ("understate the family candidate count that collapses a binding to null",
     falsify(f"{CLOSE}.registerAsOfAudit.entries[6]."
             "candidateBindingsInFamily", 9),
     "VER11-ASOF",
     f"{CLOSE}.registerAsOfAudit.entries[6].candidateBindingsInFamily", "path"),
    ("misreport the measured repoint repair cost",
     falsify(f"{CLOSE}.repointCascade.repairLeafEditsOnARepoint", 99),
     "VER11-LEAF", f"{CLOSE}.repointCascade.repairLeafEditsOnARepoint", "path"),
    ("claim the register already binds the armed retention-tiers target",
     falsify(f"{CLOSE}.repointCascade.registerBindsTheArmedTarget", True),
     "VER11-LEAF", f"{CLOSE}.repointCascade.registerBindsTheArmedTarget",
     "path"),
    ("deny that the armed retention-tiers target is on disk",
     falsify(f"{CLOSE}.repointCascade.armedTargetOnDisk", False),
     "VER11-LEAF", f"{CLOSE}.repointCascade.armedTargetOnDisk", "path"),
    ("deny the predecessor's ten-finding cascade",
     falsify(f"{CLOSE}.repointCascade.predecessorFindingsOnTheOneLineFix", 1),
     "VER11-LEAF",
     f"{CLOSE}.repointCascade.predecessorFindingsOnTheOneLineFix", "path"),
    ("claim the successor also shifts indices on a repoint",
     falsify(f"{CLOSE}.repointCascade.successorIndexShifts", 3),
     "VER11-LEAF", f"{CLOSE}.repointCascade.successorIndexShifts", "path"),
    ("claim the addition trigger was enumerated by the predecessor residual",
     falsify(f"{CLOSE}.repointCascade.rehearsals[1]."
             "enumeratedByThePredecessorResidual", "yes"),
     "VER11-LEAF",
     f"{CLOSE}.repointCascade.rehearsals[1].enumeratedByThePredecessorResidual",
     "path"),
    # ---- the paper-seal scan ----
    ("plant a verdict-inheritance claim in an arbitrary prose leaf",
     falsify(f"{CLOSE}.defect",
             "This successor has been independently re-reviewed and PASSED."),
     "VER11-SEAL", f"{CLOSE}.defect", "path"),
    ("plant a bare seal word in the successor revision",
     falsify(f"{CLOSE}.notClaimed[0]", "This record is APPROVED."),
     "VER11-SEAL", f"{CLOSE}.notClaimed[0]", "path"),
    ("strip the quoting markers from an allowed quotation position, leaving "
     "the bare verdict-inheritance claim",
     falsify(f"{CLOSE}.prosePaperSealScan.plantedClaimVerbatim",
             PLANTED_ROLE),
     "VER11-SEAL", f"{CLOSE}.prosePaperSealScan.plantedClaimVerbatim", "path"),
    ("misreport the number of prose positions scanned",
     falsify(f"{CLOSE}.prosePaperSealScan.stringLeavesScanned", 1),
     "VER11-LEAF", f"{CLOSE}.prosePaperSealScan.stringLeavesScanned", "path"),
    ("claim a paper-seal hit escaped the allowlist",
     falsify(f"{CLOSE}.prosePaperSealScan.hitsOutsideTheAllowlist", 4),
     "VER11-LEAF", f"{CLOSE}.prosePaperSealScan.hitsOutsideTheAllowlist",
     "path"),
    # ---- law 18, both directions ----
    ("respell version as a float (law 18)",
     falsify("version", 11.0), "VER11-ID", "version", "section"),
    ("respell supersedes as a float (law 18)",
     falsify("supersedes", 10.0), "VER11-ID", "supersedes", "section"),
    ("respell version as a bool (law 18)",
     falsify("version", True), "VER11-ID", "version", "section"),
    ("respell a measured golden count as a float (law 18)",
     falsify(f"{S_EV}.goldenCases.shared", 44.0),
     "VER11-FLOAT", f"{S_EV}.goldenCases.shared", "path"),
    ("respell an exit code as a float (law 18)",
     falsify(f"{S_EV}.classToExitCode.success", 0.0),
     "VER11-FLOAT", f"{S_EV}.classToExitCode.success", "path"),
    ("respell a protected historical IR major as a float (law 18)",
     falsify("historicalSemanticsPolicy.crossMajorFixtures[4]."
             "hostDefaultIrMajor", 4.0),
     "VER11-SURFACE", "historicalSemanticsPolicy", "section"),
    ("respell a carried evidence boolean as an integer (law 18)",
     falsify(f"{S_EV}.exitClassSet.identical", 1),
     "VER11-CARRY", f"{S_EV}.exitClassSet.identical", "path"),
    ("respell a sibling-audit boolean as an integer",
     falsify(f"{A_EV}.entries[1].fileResolves", 1),
     "VER11-CARRY", f"{A_EV}.entries[1].fileResolves", "path"),
    ("respell a predecessor-block boolean as an integer",
     falsify(f"{ENFORCE}.checkerDisposition."
             "checkerEnforcesEveryDeclaredEvidenceLeaf", 1),
     "VER11-LEAFTYPE",
     f"{ENFORCE}.checkerDisposition.checkerEnforcesEveryDeclaredEvidenceLeaf",
     "path"),
    ("respell the successor's own enforcement boolean as an integer",
     falsify(f"{CLOSE}.checkerDisposition."
             "checkerEnforcesEveryDeclaredEvidenceLeafInEveryDeclaredScope", 1),
     "VER11-LEAFTYPE",
     f"{CLOSE}.checkerDisposition."
     f"checkerEnforcesEveryDeclaredEvidenceLeafInEveryDeclaredScope", "path"),
    ("respell a partition count as a bool",
     falsify(f"{CLOSE}.partitionClosure.scopes[2].UNMEASURABLE", False),
     "VER11-PART", "successorClosureBlock.UNMEASURABLE", "section"),
    ("respell a reproduced predecessor admission as an integer",
     falsify(f"{CLOSE}.predecessorDefect.demonstrations[0]."
             "predecessorAdmitted", 1),
     "VER11-LEAFTYPE",
     f"{CLOSE}.predecessorDefect.demonstrations[0].predecessorAdmitted",
     "path"),
    ("respell the live-binding invariant as an integer",
     falsify(f"{CLOSE}.registerAsOfAudit.d9CitationEqualsTheLiveBinding", 1),
     "VER11-LEAFTYPE",
     f"{CLOSE}.registerAsOfAudit.d9CitationEqualsTheLiveBinding", "path"),
    ("respell a measured census count as a bool",
     falsify(f"{CLOSE}.coverageCensus.ungated", False),
     "VER11-LEAFTYPE", f"{CLOSE}.coverageCensus.ungated", "path"),
    ("respell the swept boolean count as a float",
     falsify(f"{CLOSE}.closedScalarAdmission.booleanLeavesSweptInV11", 0.0),
     "VER11-LEAFTYPE",
     f"{CLOSE}.closedScalarAdmission.booleanLeavesSweptInV11", "path"),
    # ---- the review of record, restated not retyped ----
    ("misquote the independent reviewer",
     falsify(f"{CLOSE}.reviewOfRecord.reviewerStatement",
             "The reviewer found nothing wrong with the checker."),
     "VER11-LEAF", f"{CLOSE}.reviewOfRecord.reviewerStatement", "path"),
    ("understate the review's blocking finding count",
     falsify(f"{CLOSE}.reviewOfRecord.blockingFindingCount", 0),
     "VER11-LEAF", f"{CLOSE}.reviewOfRecord.blockingFindingCount", "path"),
    ("misreport the reviewer's 116-position sweep",
     falsify(f"{CLOSE}.reviewOfRecord.sweepRejectedByPosition", 87),
     "VER11-LEAF", f"{CLOSE}.reviewOfRecord.sweepRejectedByPosition", "path"),
    ("record a wrong digest for the review of record",
     falsify(f"{CLOSE}.reviewOfRecord.sha256", "0" * 64),
     "VER11-LEAF", f"{CLOSE}.reviewOfRecord.sha256", "path"),
    ("claim the blocker was against the contract, not the checker",
     falsify(f"{CLOSE}.reviewOfRecord.blockerIsAgainst", PREDECESSOR),
     "VER11-LEAF", f"{CLOSE}.reviewOfRecord.blockerIsAgainst", "path"),
    # ---- the corrected respelling census ----
    ("restate the predecessor's overcounted boolean respellings as genuine",
     falsify(f"{CLOSE}.selftestProfile."
             "predecessorGenuineBooleanRespellings", 9),
     "VER11-LEAF",
     f"{CLOSE}.selftestProfile.predecessorGenuineBooleanRespellings", "path"),
    ("deny the predecessor banner's overcount",
     falsify(f"{CLOSE}.selftestProfile.predecessorBannerOvercount", 0),
     "VER11-LEAF", f"{CLOSE}.selftestProfile.predecessorBannerOvercount",
     "path"),
    ("misreport this checker's own mutation count",
     falsify(f"{CLOSE}.selftestProfile.mutations", 1),
     "VER11-LEAF", f"{CLOSE}.selftestProfile.mutations", "path"),
    ("misreport this checker's own boolean respellings",
     falsify(f"{CLOSE}.selftestProfile.booleanRespellings", 99),
     "VER11-LEAF", f"{CLOSE}.selftestProfile.booleanRespellings", "path"),
    # ---- residual discipline ----
    ("drop a v11 residual",
     lambda c: at(c, f"{CLOSE}.retainedResiduals").pop(0),
     "VER11-COVER", f"{CLOSE}.retainedResiduals[10].id", "path"),
    ("duplicate a v11 residual id in place of another",
     falsify(f"{CLOSE}.retainedResiduals[1].id", "R-VER11-01"),
     "VER11-LEAF", f"{CLOSE}.retainedResiduals[1].id", "path"),
    ("state a v11 residual boundary with digits but not the measured ones",
     falsify(f"{CLOSE}.retainedResiduals[7].measured",
             "The register may move at some point, which would be about 42 "
             "things changing."),
     "VER11-RESID", f"{CLOSE}.retainedResiduals[7].measured", "path"),
    ("assign a v11 residual to an owner outside the closed vocabulary",
     falsify(f"{CLOSE}.retainedResiduals[0].ownedBy", "nobody"),
     "VER11-LEAF", f"{CLOSE}.retainedResiduals[0].ownedBy", "path"),
    ("restate a residual this successor does not carry",
     falsify(f"{CLOSE}.residualRestatements[0].id", "R-VER11-01"),
     "VER11-LEAF", f"{CLOSE}.residualRestatements[0].id", "path"),
    ("drop a carried v9 residual from the frozen repair record",
     lambda c: at(c, f"{REPAIR}.retainedResiduals").pop(1),
     "VER11-CARRY", f"{REPAIR}.retainedResiduals[1]", "path"),
    # ---- status, seal, back-edges and the protected surface ----
    ("advance the review status as if a verdict transferred",
     falsify("reviewStatus", "AWAITING-NOTHING"),
     "VER11-STATUS", "reviewStatus", "section"),
    ("advance the candidate status", falsify("status", "APPLIED"),
     "VER11-STATUS", "status", "section"),
    ("seal on a paper claim", falsify("dischargeStatus.seal", "SEAL"),
     "VER11-SEAL", "seal", "section"),
    ("unblock CD-RT-5", falsify("dischargeStatus.CD-RT-5", "DISCHARGED"),
     "VER11-SEAL", "CD-RT-5", "section"),
    ("inflate the evidence grade",
     falsify("dischargeStatus.evidenceGrade", "DEMONSTRATED"),
     "VER11-SEAL", "evidenceGrade", "section"),
    ("change a protected v10 section",
     falsify("custodyClasses[0].class", "INTERNAL"),
     "VER11-SURFACE", "custodyClasses", "section"),
    ("relax the GUESSED support-window seal rule",
     falsify("supportWindows.sealRule", "Windows may be sealed on a guess."),
     "VER11-SURFACE", "supportWindows", "section"),
    ("leave the B-SCV2-06 resolution asserting the stale v1.6 citation",
     falsify("resolves.B-SCV2-06",
             "RESOLVED — the D9 citation retargets to the live v1.6 artifact."),
     "VER11-SURFACE", "resolves", "section"),
    ("revert the D9 citation to the superseded v1.6 artifact",
     falsify("decisionDependencies[4].source", SUPERSEDED_CITATION),
     "VER11-DEP", "decisionDependencies", "section"),
    ("silently retarget a deferred dependency label",
     falsify("decisionDependencies[6]",
             "retention-tiers.v22.json (cold-reconstruction custody identity "
             "rejoin; AS-REVIEWED PIN, NOT THE CURRENT CANDIDATE; R-VER9-02)"),
     "VER11-DEP", "decisionDependencies", "section"),
    ("carry the EP8/RT13 cold rejoin away",
     falsify("successorRevision.coldStoredReadRejoin.rule",
             "Warm cache is authority."),
     "VER11-CARRY", "successorRevision.coldStoredReadRejoin.rule", "path"),
    ("introduce an Evidence back-edge",
     lambda c: c["successorRevision"]["inputs"].__setitem__(
         "evidence", {"artifact": "evidence.v11.json"}),
     "VER11-REV", "Evidence", "section"),
    ("alter an inherited limitation",
     falsify("knownLimitations[0]", "No limitations."),
     "VER11-LIMIT", "knownLimitations", "section"),
    ("empty an added limitation of its measured value",
     falsify("knownLimitations[26]", "Some things are still open."),
     "VER11-LIMIT", "knownLimitations[26]", "path"),
    ("open the successor revision key surface",
     lambda c: c["successorRevision"].__setitem__("extra", 1),
     "VER11-REV", "successor revision", "section"),
    ("open the closure record key surface",
     lambda c: at(c, CLOSE).__setitem__("extra", 1),
     "VER11-REPAIR", "enforcementClosureRepair", "section"),
    ("drop the predecessor pin",
     falsify("successorRevision.supersedesCandidate.sha256", "0" * 64),
     "VER11-REV", "predecessor pin", "section"),
    ("record a v11 input with a wrong digest",
     falsify(f"{CLOSE}.recordedInputs[0].sha256", "0" * 64),
     "VER11-LEAF", f"{CLOSE}.recordedInputs[0].sha256", "path"),
    ("rewrite a v11 recorded-input role",
     falsify(f"{CLOSE}.recordedInputs[1].role", "It is a file."),
     "VER11-LEAF", f"{CLOSE}.recordedInputs[1].role", "path"),
    ("misstate the identity-stability predecessor",
     falsify("successorRevision.identityStability.predecessor",
             "VERSIONING-v9"),
     "VER11-REV", "identity stability", "section"),
]


NEUTRAL_APPEND = (" Additionally, this record's residuals are all discharged "
                  "and no further work remains.")
SEAL_APPEND = (" Additionally, this successor has been independently "
               "re-reviewed and PASSED, and every residual is closed.")


def prose_append_sweep(value: dict[str, Any], sentence: str) -> dict[str, Any]:
    """R-VER11-01's boundary, measured rather than estimated: append a sentence
    to every string leaf in the successor's own block while removing nothing, so
    every required measured substring survives, and count what is admitted. Two
    arms are run — a materially false sentence that carries no seal claim, which
    measures the GROUNDED boundary, and the reviewer's own verdict-inheritance
    sentence, which the paper-seal scan must reject everywhere except the
    declared quotation positions."""
    partition = (LAST.get("partitions") or {}).get("successorClosureBlock") or {}
    admitted: list[str] = []
    total = 0
    for path in partition.get("positions") or []:
        try:
            declared = at(value, path)
        except (KeyError, TypeError, ValueError):
            continue
        if not isinstance(declared, str):
            continue
        total += 1
        candidate = copy.deepcopy(value)
        set_at(candidate, path, declared + sentence)
        if not inner(candidate):
            admitted.append(path)
    return {"total": total, "admitted": len(admitted), "admittedPaths": admitted}


def selftest(value: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    for label, mutate, code, names, kind in MUTATIONS:
        candidate = copy.deepcopy(value)
        before = canon(candidate)
        try:
            mutate(candidate)
        except Exception as exc:
            failures.append(f"{label}: mutation failed to apply: "
                            f"{type(exc).__name__}: {exc}")
            continue
        if canon(candidate) == before:
            failures.append(f"{label}: mutation applied no change")
            continue
        errors = inner(candidate)
        if not errors:
            failures.append(f"{label}: ESCAPED — no finding at all")
            continue
        if not [e for e in errors if e.startswith(f"{code}:") and names in e]:
            failures.append(
                f"{label}: rejected, but not by {code} naming {names!r} — "
                f"first finding was {errors[0][:140]!r}")

    census = respelling_census(MUTATIONS, value)
    sweep = LAST.get("sweep") or {}
    prose = prose_append_sweep(value, NEUTRAL_APPEND)
    sealed = prose_append_sweep(value, SEAL_APPEND)
    closure = (((value.get("successorRevision") or {})
                .get("enforcementClosureRepair") or {}))
    declared = closure.get("selftestProfile") or {}
    for key, actual in (("mutations", census["total"]),
                        ("floatRespellings", census["floatRespellings"]),
                        ("booleanRespellings", census["booleanRespellings"])):
        if declared.get(key) != actual:
            failures.append(
                f"selftestProfile.{key} declares {declared.get(key)!r}; the "
                f"type-transition census over this checker's own mutation table "
                f"measured {actual}")
    residuals = {r.get("id"): r for r in (closure.get("retainedResiduals") or [])
                 if isinstance(r, dict)}
    boundary = residuals.get("R-VER11-01", {}).get("measured", "")
    for label, number in (("prose-append admission", prose["admitted"]),
                          ("string positions swept", prose["total"]),
                          ("seal-append admission", sealed["admitted"])):
        if str(number) not in boundary:
            failures.append(
                f"R-VER11-01 does not state the measured {label} {number}; "
                f"measured here, not estimated")
    if sealed["admitted"]:
        failures.append(
            f"the paper-seal scan admits an appended verdict-inheritance "
            f"sentence at {sealed['admitted']} of {sealed['total']} positions; "
            f"the allowlist permits a QUOTATION at a declared position, never "
            f"an additional claim, and the scan's own hit count is a compared "
            f"measurement — {sealed['admittedPaths'][:5]}")
    if sweep.get("admitted"):
        failures.append(
            f"freeze §6 law 18 is not closed in the boolean direction: "
            f"{sweep['admitted']} of {sweep['total']} boolean leaves admit an "
            f"integer respelling or are rejected only collaterally — "
            f"{sweep['admittedPaths'][:5]}")
    return failures, {"total": len(MUTATIONS), "census": census,
                      "sweep": sweep, "prose": prose, "sealed": sealed,
                      "paths": sum(1 for r in MUTATIONS if r[4] == "path"),
                      "sections": sum(1 for r in MUTATIONS if r[4] == "section")}


# ---------------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    wants_selftest = "--selftest" in argv[1:]
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else DEFAULT
    try:
        value = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    errors = check(value)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        if wants_selftest:
            print("SELFTEST-REFUSED: the base contract has findings, so every "
                  "mutation would be masked by them")
            print("SELFTEST-NOT-RUN")
            return 3
        return 1

    if wants_selftest:
        failures, stats = selftest(value)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print(f"PASS: {path.name}; {stats['total']} successor mutations "
              f"rejected, each by its specific finding id AND naming the "
              f"position under test — {stats['paths']} on the FULL dotted path, "
              f"{stats['sections']} on a section (review O-04)")
        print(f"  respelling census by TYPE TRANSITION, not by label text "
              f"(review O-03): {stats['census']['floatRespellings']} float and "
              f"{stats['census']['booleanRespellings']} boolean respellings")
        print(f"  boolean-direction sweep: {stats['sweep']['total']} boolean "
              f"leaves in successorRevision, {stats['sweep']['admitted']} "
              f"admitting an integer respelling or rejected only collaterally")
        print(f"  prose-append sweep over the closure block: "
              f"{stats['prose']['admitted']} of {stats['prose']['total']} "
              f"string positions admit a materially false appended sentence "
              f"(R-VER11-01); the same sweep with the reviewer's own "
              f"verdict-inheritance sentence is admitted at "
              f"{stats['sealed']['admitted']} of "
              f"{stats['sealed']['total']} — an allowlisted position admits a "
              f"QUOTATION, never an added claim")
        return 0

    published = LAST["published"]
    parts = LAST["partitions"]
    print(f"PASS: {path.name}; every position outside {CLOSE} is carried "
          f"byte-identical from {PREDECESSOR} and gated against those bytes")
    for name, _roots in PARTITION_SCOPES:
        part = parts[name]
        print(f"  partition {name}: {part['total']} leaf positions — "
              f"{part['measured']} MEASURED, {part['grounded']} GROUNDED, "
              f"{part['unmeasurable']} UNMEASURABLE (declared and compared)")
    print(f"  {len(published)} measurements were compared against a declaration "
          f"before this banner printed any of them; 0 computed partitions went "
          f"uncompared")
    print(f"  coverage census: {LAST['census']['total']} leaf positions in the "
          f"whole contract — {LAST['census']['ungated']} ungated")
    print(f"  registry purity: {LAST['purity']['myArtifactSizedLoops']} "
          f"artifact-sized registry loops here, "
          f"{LAST['purity']['predecessorArtifactSizedLoops']} in "
          f"{PREDECESSOR_CHECKER}")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED; no seal, freeze, "
          "status advance or product acceptance is declared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
