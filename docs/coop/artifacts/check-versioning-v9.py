#!/usr/bin/env python3
"""Conformance checker for the narrow VERSIONING v9 D9 head citation repair.

v9 supersedes v8 on one thing: `decisionDependencies[4].source` cited
`artifacts/d9-exit-contract.v1.6.json` while `claim-register.v1.json` binds D9
to `artifacts/d9-exit-contract.v1.14.json`. The stale citation was invisible
because the register carried the same one — two instruments wrong in the same
direction read as agreement. §7.2 forbids repairing the reviewed v8 bytes in
place, so the repair is this successor.

Why this file exists at all — `check-versioning.py` cannot validate v9:

  * it hardcodes ``BINDING = "versioning-policy.v4.json"`` and reads another
    path only when one is passed as argv[1], so by default it never sees v9;
  * its ``VER-V4`` guard rejects any contract whose version is not 4;
  * its ``VER-DEP`` loop calls ``d.get("source")`` on every element of
    ``decisionDependencies``, and from v7 onward that list carries bare label
    strings at indices 5 and 6, so passing v8 or v9 raises AttributeError and
    produces a traceback rather than a verdict.

This follows the established v5..v8 successor chain: pin the predecessor and its
checker by digest, run the predecessor checker against the predecessor, require
the protected surface to be unchanged, and assert the declared delta exactly.

Two things this checker does that its predecessors do not, both in response to
freeze §6 law 18 (closed-scalar admission is exact-type):

  * the protected surface is compared as CANONICAL JSON TEXT, not by Python
    equality, so an integer respelled as a float anywhere in the byte-preserved
    sections changes the text and is rejected. `corpus-float-admission-sweep.v1`
    measured `check-versioning-v8.py` admitting `versioning-policy.v8.json`
    `version` retyped to a float at exit 0 with a full green banner, because
    Python evaluates ``8.0 == 8`` as true under a bare ``!=``;
  * every integer this artifact adds is gated with an exact ``type(x) is int``
    check before comparison, which also rejects bool, and no float may appear
    anywhere in the v9 delta subtree.

The substance behind the repaired citation is not taken on trust. This checker
re-derives the exit-class contract across the v1.6 -> v1.14 span from both
artifacts on disk and requires the artifact's declared measurements to equal the
measured ones. That matters because the v1.14 independent review re-derives
against v1.13, not v1.6, and so does not attest the span this citation crosses.

Usage: python3 -I -B artifacts/check-versioning-v9.py [contract] [--selftest]
Exit:  0 clean · 1 findings · 2 IO error · 3 selftest refused or not run
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT = HERE / "versioning-policy.v9.json"

PREDECESSOR = "versioning-policy.v8.json"
PREDECESSOR_CHECKER = "check-versioning-v8.py"
PREDECESSOR_REVIEW = "versioning-policy.v8.review-independent-cold-rejoin.json"
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
        "ea4b52b5a4d187ec35ad994d8ffcd888db287566c8fb53f3df17e5203d84ae2e",
    PREDECESSOR_CHECKER:
        "82834720a8fd4ec8701dad2b43ad94d6ad9e52d21aeb077f4286fab5fb156844",
    PREDECESSOR_REVIEW:
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

# claim-register.v1.json is deliberately NOT pinned. It is coordinator-owned and
# is expected to move when the VERSIONING binding is repointed; pinning its
# bytes would make this checker fail on the very act it anticipates. The gate is
# the semantic invariant instead: the register's live D9 binding must equal this
# artifact's D9 citation.

CHANGED = {
    "version", "supersedes", "role", "decisionDependencies", "resolves",
    "knownLimitations", "successorRevision",
}

EXPECTED_REVISION_KEYS = {
    "id", "candidateState", "supersedesCandidate", "inputs",
    "rawAuthorityKinds", "custodyRule", "storeAuthorityRule",
    "identityStability", "forbiddenBackEdge", "coldStoredReadRejoin",
    "dependencyLabelRule", "d9CitationRepair",
}

EXPECTED_REPAIR_KEYS = {
    "findingId", "authoredBy", "defect", "whyItWasInvisible",
    "whySuccessorAndNotInPlaceRepair", "citation", "recordedInputs",
    "substanceUnchangedEvidence", "directionPreservation",
    "siblingCitationAudit", "retainedResiduals", "checkerDisposition",
    "notClaimed",
}

REQUIRED_RESIDUAL_IDS = {
    "R-VER9-01", "R-VER9-02", "R-VER9-03", "R-VER9-04", "R-VER9-05",
    "R-VER9-06", "R-VER9-07",
}

ADDED_LIMITATION_COUNT = 3

REPAIRED_CITATION = "artifacts/" + D9_HEAD
SUPERSEDED_CITATION = "artifacts/" + D9_SUPERSEDED


def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text())


def sha_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def canon(value: Any) -> str:
    """Canonical JSON text. Unlike Python equality this distinguishes 4 from
    4.0 and True from 1, which is the whole point (freeze §6 law 18)."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def module(filename: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def exact_int(value: Any) -> bool:
    """Exact-type admission for a closed integer scalar. ``type(x) is int``
    rejects both float and bool; ``isinstance`` would admit bool."""
    return type(value) is int


def no_floats(value: Any, path: str = "") -> list[str]:
    """The v9 delta introduces no float anywhere. Any float in this subtree is
    either a respelled integer or an unreviewed addition; both are findings."""
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


def measure_d9_span(old: Any, new: Any) -> dict[str, Any]:
    """Re-derive the exit-class contract across the v1.6 -> v1.14 span from both
    artifacts on disk. This is the evidence the repair rests on and it is
    computed here, not read from the artifact."""
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

    return {
        "exitClassesRemoved": [c for c in old_classes if c not in new_classes],
        "exitClassesAdded": [c for c in new_classes if c not in old_classes],
        "exitClassSetIdentical": old_classes == new_classes,
        "classToExitCodeByteIdentical":
            canon(old["classToExitCode"]) == canon(new["classToExitCode"]),
        "countV16": len(old_g),
        "countV114": len(new_g),
        "shared": len(shared),
        "removed": sorted(set(old_g) - set(new_g)),
        "added": sorted(set(new_g) - set(old_g)),
        "sharedExitClassMismatches": cls_mismatch,
        "sharedReasonOrErrorCodeMismatches": code_mismatch,
        "sharedNumericExitCodeMismatches": exit_mismatch,
        "changedShared": [g for g in shared
                          if canon(old_g[g]) != canon(new_g[g])],
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
        "d9DepsByteIdentical":
            canon(old["decisionDependencies"]) ==
            canon(new["decisionDependencies"]),
        "d9CitesVersioningPolicy": "versioning-policy" in canon(new).lower(),
    }


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["root is not an object"]

    try:
        for name, expected in PINS.items():
            if sha_file(name) != expected:
                raise ValueError(f"pinned input drift: {name}")
        predecessor = load(HERE / PREDECESSOR)
        d9_old = load(HERE / D9_SUPERSEDED)
        d9_new = load(HERE / D9_HEAD)
    except Exception as exc:
        return [f"pinned input load failed: {type(exc).__name__}: {exc}"]

    if verify_files:
        try:
            oldmod = module(PREDECESSOR_CHECKER, "versioning_v8_pinned_for_v9")
            old_errors = oldmod.check(predecessor)
        except Exception as exc:
            old_errors = [f"{type(exc).__name__}: {exc}"]
        if old_errors:
            errors.append(f"VERSIONING v8 predecessor is red: {old_errors[0]}")
        # The D9 head checker takes (candidate, predecessor, v16) and bootstraps
        # its own pinned authority, so it is exercised as a whole program.
        try:
            done = subprocess.run(
                [sys.executable, "-I", "-B", str(HERE / D9_HEAD_CHECKER)],
                cwd=str(HERE), capture_output=True, text=True)
            if done.returncode != 0:
                errors.append(
                    f"D9 head dependency is red: {D9_HEAD_CHECKER} exited "
                    f"{done.returncode}")
        except Exception as exc:
            errors.append(f"D9 head checker did not run: {type(exc).__name__}: "
                          f"{exc}")

    # ---- protected surface, compared as canonical JSON text (law 18) ----
    if set(value) != set(predecessor):
        errors.append("top-level surface differs from VERSIONING v8")
    for key in set(predecessor) - CHANGED:
        if canon(value.get(key)) != canon(predecessor.get(key)):
            errors.append(f"protected VERSIONING v8 section changed: {key}")

    # ---- identity, exact-type ----
    if value.get("artifact") != "opensip.versioning-policy":
        errors.append("artifact identity drift")
    if not exact_int(value.get("version")) or value.get("version") != 9:
        errors.append("version is not exactly integer 9 (freeze §6 law 18: a "
                      "float or bool respelling is not an integer)")
    if not exact_int(value.get("supersedes")) or value.get("supersedes") != 8:
        errors.append("supersedes is not exactly integer 8 (freeze §6 law 18)")

    # ---- no status may move ----
    if value.get("status") != predecessor.get("status"):
        errors.append("status moved; this successor advances no status")
    if value.get("reviewStatus") != predecessor.get("reviewStatus"):
        errors.append("reviewStatus moved; the v8 PASS binds v8's bytes and "
                      "does not transfer to v9 (§7.2)")
    if value.get("role") != ("A-prime v4 D9 head citation repair; B-SCV2-06 "
                             "direction and resolution preserved"):
        errors.append("narrow successor role drift")

    # ---- the citation repair itself ----
    deps = value.get("decisionDependencies")
    pred_deps = predecessor.get("decisionDependencies", [])
    if not isinstance(deps, list) or len(deps) != len(pred_deps):
        errors.append("decisionDependencies arity changed")
    else:
        for index, (now, was) in enumerate(zip(deps, pred_deps)):
            if index == 4:
                continue
            if canon(now) != canon(was):
                errors.append(f"decisionDependencies[{index}] changed; only the "
                              f"D9 citation may move in this successor")
        d9 = deps[4]
        if not isinstance(d9, dict) or d9.get("id") != "D9":
            errors.append("decisionDependencies[4] is not the D9 dependency")
        else:
            was = pred_deps[4]
            if d9.get("source") != REPAIRED_CITATION:
                errors.append(
                    f"D9 citation is {d9.get('source')!r}, expected "
                    f"{REPAIRED_CITATION!r}")
            if d9.get("source") == SUPERSEDED_CITATION:
                errors.append("D9 citation is still the superseded v1.6 "
                              "artifact (B-SCV2-06 unrepaired)")
            # B-SCV2-06's resolution is load-bearing and must survive verbatim.
            for field in ("id", "claim", "direction", "note"):
                if canon(d9.get(field)) != canon(was.get(field)):
                    errors.append(
                        f"D9 dependency field {field!r} changed; B-SCV2-06's "
                        f"recorded resolution must survive the citation repair")
            direction = d9.get("direction") or ""
            if "VERSIONING depends on D9" not in direction or \
                    "D9 does NOT depend on VERSIONING" not in direction:
                errors.append("the one-way dependency direction is no longer "
                              "declared (B-SCV2-06)")
            if "additive-only exit-class rule (V4)" not in direction:
                errors.append("the direction no longer names the additive-only "
                              "exit-class rule (V4) it rests on")
            if not set(d9) <= set(was) | {"source"} or set(d9) != set(was):
                errors.append("D9 dependency key surface changed")

    # ---- the citation must equal the register's live binding ----
    register_path = HERE / REGISTER
    if not register_path.exists():
        errors.append(f"{REGISTER} is absent; the live D9 binding cannot be "
                      f"verified")
    else:
        try:
            claims = load(register_path)["claims"]
            live = next((c.get("bindingArtifact") for c in claims
                         if c.get("id") == "D9"), None)
        except Exception as exc:
            live = None
            errors.append(f"{REGISTER} unreadable: {type(exc).__name__}: {exc}")
        if live is None:
            errors.append("the register declares no live D9 binding")
        elif isinstance(deps, list) and len(deps) > 4 and \
                isinstance(deps[4], dict) and deps[4].get("source") != live:
            errors.append(
                f"D9 citation {deps[4].get('source')} still disagrees with the "
                f"register binding {live} — a superseded citation (B-SCV2-06)")

    # ---- B-SCV2-06's resolution text must be repaired, not deleted ----
    resolves = value.get("resolves") or {}
    pred_resolves = predecessor.get("resolves") or {}
    if set(resolves) != set(pred_resolves):
        errors.append("resolves key surface changed")
    for key in set(pred_resolves) & set(resolves):
        if key != "B-SCV2-06" and resolves[key] != pred_resolves[key]:
            errors.append(f"resolves[{key!r}] changed; only the B-SCV2-06 "
                          f"citation restatement may move")
    b_scv2 = resolves.get("B-SCV2-06") or ""
    if not b_scv2.startswith("RESOLVED"):
        errors.append("B-SCV2-06 is no longer recorded RESOLVED")
    if "live v1.6 artifact" in b_scv2:
        errors.append("resolves['B-SCV2-06'] still asserts the superseded v1.6 "
                      "citation — repairing one instrument and not the other is "
                      "the defect that hid this finding")
    if D9_HEAD not in b_scv2:
        errors.append("resolves['B-SCV2-06'] does not name the repaired head "
                      "citation")
    if "VERSIONING depends on D9, not the reverse" not in b_scv2:
        errors.append("resolves['B-SCV2-06'] no longer records the one-way "
                      "direction")

    # ---- limitation delta is additive and exact ----
    limitations = value.get("knownLimitations")
    pred_limitations = predecessor.get("knownLimitations", [])
    if not isinstance(limitations, list):
        errors.append("knownLimitations is not a list")
    elif limitations[:len(pred_limitations)] != pred_limitations:
        errors.append("inherited knownLimitations were altered or reordered")
    elif len(limitations) - len(pred_limitations) != ADDED_LIMITATION_COUNT:
        errors.append(
            f"successor limitation delta is "
            f"{len(limitations) - len(pred_limitations)}, expected "
            f"{ADDED_LIMITATION_COUNT}")

    # ---- successor revision ----
    revision = value.get("successorRevision") or {}
    pred_revision = predecessor.get("successorRevision") or {}
    if set(revision) != EXPECTED_REVISION_KEYS:
        errors.append("successor revision is not closed")
    if revision.get("id") != "VERSIONING-v9-D9-HEAD-CITATION-REPAIR-SUCCESSOR" \
            or revision.get("candidateState") != "NOT-APPLIED":
        errors.append("successor identity/state drift")
    if revision.get("supersedesCandidate") != {
            "artifact": PREDECESSOR,
            "sha256": PINS[PREDECESSOR],
            "checker": PREDECESSOR_CHECKER,
            "checkerSha256": PINS[PREDECESSOR_CHECKER]}:
        errors.append("VERSIONING v8 protected predecessor pin drift")

    # The EP8/RT13 cold stored-read rejoin contract is carried, not re-derived.
    for key in ("inputs", "rawAuthorityKinds", "custodyRule",
                "storeAuthorityRule", "coldStoredReadRejoin",
                "dependencyLabelRule"):
        if canon(revision.get(key)) != canon(pred_revision.get(key)):
            errors.append(f"carried v8 successor contract changed: {key}")
    if revision.get("identityStability", {}).get("predecessor") != \
            "VERSIONING-v8" or \
            revision.get("identityStability", {}).get("state") != \
            "EXACT-CUSTODY-IDENTITIES-UNCHANGED":
        errors.append("v8 identity stability statement drift")
    forbidden = revision.get("forbiddenBackEdge", "")
    if not all(term in forbidden for term in (
            "Evidence", "RunId", "TerminalRunV1", "RunAuthorityIndexV1",
            "ProjectStoreAuthority token", "store transaction token",
            "VERSIONING-v9")):
        errors.append("forbidden downstream/store-token back-edge rule "
                      "incomplete")
    if any("evidence" in canon(row).lower()
           for row in (revision.get("inputs") or {}).values()
           if isinstance(row, dict)):
        errors.append("VERSIONING v9 contains an Evidence dependency back-edge")

    # ---- the repair record ----
    repair = revision.get("d9CitationRepair") or {}
    if set(repair) != EXPECTED_REPAIR_KEYS:
        errors.append("d9CitationRepair is not closed")
    errors.extend(no_floats(repair, "successorRevision.d9CitationRepair"))

    citation = repair.get("citation") or {}
    if citation.get("was") != SUPERSEDED_CITATION or \
            citation.get("now") != REPAIRED_CITATION or \
            citation.get("nowSha256") != PINS[D9_HEAD] or \
            citation.get("fieldsChanged") != ["source"] or \
            citation.get("fieldsPreservedByteIdentical") != [
                "id", "claim", "direction", "note"]:
        errors.append("declared citation delta does not match the repair "
                      "actually made")

    # ---- recording obligation: filename + sha256 for every input ----
    recorded = repair.get("recordedInputs")
    if not isinstance(recorded, list):
        errors.append("recordedInputs is not a list — a count is not a record")
        recorded = []
    recorded_map = {row.get("artifact"): row for row in recorded
                    if isinstance(row, dict)}
    for name, digest in PINS.items():
        row = recorded_map.get(name)
        if row is None:
            errors.append(f"recordedInputs omits pinned input {name} — freeze "
                          f"§7.2 requires filename + sha256 for every input")
        elif row.get("sha256") != digest:
            errors.append(f"recordedInputs sha256 for {name} does not match the "
                          f"bytes on disk")
        elif not row.get("role"):
            errors.append(f"recordedInputs entry for {name} records no role")
    register_row = recorded_map.get(REGISTER)
    if register_row is None:
        errors.append(f"recordedInputs omits {REGISTER}")
    elif not register_row.get("gate", "").startswith("RECORDED-NOT-PINNED"):
        errors.append(f"{REGISTER} must be recorded as RECORDED-NOT-PINNED with "
                      f"the reason it is not byte-gated")

    # ---- substance: re-derived here, not taken from the artifact ----
    measured = measure_d9_span(d9_old, d9_new)
    substance = repair.get("substanceUnchangedEvidence") or {}
    golden = substance.get("goldenCases") or {}
    exit_set = substance.get("exitClassSet") or {}

    declared_ints = {
        "goldenCases.countV16": (golden.get("countV16"), measured["countV16"]),
        "goldenCases.countV114": (golden.get("countV114"),
                                  measured["countV114"]),
        "goldenCases.shared": (golden.get("shared"), measured["shared"]),
        "goldenCases.sharedExitClassMismatches": (
            golden.get("sharedExitClassMismatches"),
            measured["sharedExitClassMismatches"]),
        "goldenCases.sharedReasonOrErrorCodeMismatches": (
            golden.get("sharedReasonOrErrorCodeMismatches"),
            measured["sharedReasonOrErrorCodeMismatches"]),
        "goldenCases.sharedNumericExitCodeMismatches": (
            golden.get("sharedNumericExitCodeMismatches"),
            measured["sharedNumericExitCodeMismatches"]),
    }
    for label, (declared, actual) in declared_ints.items():
        if not exact_int(declared):
            errors.append(f"{label} is not an exact integer (freeze §6 law 18)")
        elif declared != actual:
            errors.append(f"{label} declares {declared}, measured {actual}")

    for name, code in (d9_new["classToExitCode"]).items():
        declared = (substance.get("classToExitCode") or {}).get(name)
        if not exact_int(declared) or declared != code:
            errors.append(f"classToExitCode[{name!r}] declared {declared!r} is "
                          f"not the exact integer {code} on disk")

    # These are the properties V4 actually constrains.
    if measured["exitClassesRemoved"]:
        errors.append(
            f"V4 VIOLATED across the cited span: exit classes "
            f"{measured['exitClassesRemoved']} exist in {D9_SUPERSEDED} and not "
            f"in {D9_HEAD}. Exit classes are additive-only, forever. This is "
            f"not a citation repair.")
    if not measured["classToExitCodeByteIdentical"]:
        errors.append(
            f"V4 VIOLATED across the cited span: classToExitCode differs "
            f"between {D9_SUPERSEDED} and {D9_HEAD}. Renumbering silently "
            f"changes the meaning of every CI configuration in existence. This "
            f"is not a citation repair.")
    for label, key in (("exit class", "sharedExitClassMismatches"),
                       ("reason/error code", "sharedReasonOrErrorCodeMismatches"),
                       ("numeric exit code", "sharedNumericExitCodeMismatches")):
        if measured[key]:
            errors.append(
                f"V4 VIOLATED across the cited span: {measured[key]} shared "
                f"golden(s) changed {label} between {D9_SUPERSEDED} and "
                f"{D9_HEAD}. This is not a citation repair.")
    if measured["removed"]:
        errors.append(f"goldens removed across the cited span: "
                      f"{measured['removed']} — the contract is not additive")
    if measured["remediesRemoved"] or not measured["reasonCodesByteIdentical"] \
            or not measured["errorCodesByteIdentical"]:
        errors.append("the closed reason/error code vocabulary is not "
                      "byte-identical across the cited span")

    if exit_set.get("identical") is not True or \
            exit_set.get("removed") != measured["exitClassesRemoved"] or \
            exit_set.get("added") != measured["exitClassesAdded"]:
        errors.append("declared exit-class set delta does not match the "
                      "measured one")
    if golden.get("removed") != measured["removed"] or \
            golden.get("added") != measured["added"] or \
            golden.get("changedShared") != measured["changedShared"]:
        errors.append("declared golden delta does not match the measured one")
    if substance.get("classToExitCodeByteIdentical") is not True:
        errors.append("the artifact does not assert classToExitCode byte "
                      "identity across the span")
    # The artifact must not launder the head review's v1.13 evidence as if it
    # covered the v1.6 span. That substitution is the whole reason this repair
    # needed its own measurement.
    if "v1.13" not in substance.get("whyNotInheritedFromTheHeadReview", ""):
        errors.append("the artifact does not record that the head review "
                      "attests the v1.13 span, not the v1.6 span it cites")

    # ---- direction re-verified at the head ----
    direction_block = (repair.get("directionPreservation") or {}).get(
        "reVerifiedAtHead") or {}
    if direction_block.get("d9DecisionDependenciesByteIdenticalV16ToV114") is not \
            measured["d9DepsByteIdentical"]:
        errors.append("declared D9 dependency-list identity does not match the "
                      "measured one")
    if direction_block.get("d9CitesAnyVersioningPolicyArtifact") is not \
            measured["d9CitesVersioningPolicy"]:
        errors.append("declared D9 back-citation state does not match the "
                      "measured one")
    if measured["d9CitesVersioningPolicy"]:
        errors.append(
            f"{D9_HEAD} names a versioning-policy artifact — the declared "
            f"one-way direction (VERSIONING -> D9) may no longer hold "
            f"(B-SCV2-06)")

    # ---- sibling citation audit must be present and measured ----
    audit = repair.get("siblingCitationAudit") or {}
    entries = audit.get("entries")
    if not isinstance(entries, list) or len(entries) != len(pred_deps):
        errors.append(f"siblingCitationAudit does not cover all "
                      f"{len(pred_deps)} decisionDependencies entries")
    else:
        for index, row in enumerate(entries):
            if not exact_int(row.get("index")):
                errors.append(f"siblingCitationAudit entry {index} index is not "
                              f"an exact integer (freeze §6 law 18)")
            elif row.get("index") != index:
                errors.append(f"siblingCitationAudit entry {index} is misindexed")
            if not row.get("result"):
                errors.append(f"siblingCitationAudit entry {index} records no "
                              f"measured result")
    if not audit.get("measuredResult"):
        errors.append("siblingCitationAudit records no measured result")

    # ---- residuals retained, not absorbed ----
    residuals = repair.get("retainedResiduals")
    if not isinstance(residuals, list):
        errors.append("retainedResiduals is not a list")
        residuals = []
    ids = {r.get("id") for r in residuals if isinstance(r, dict)}
    for missing in sorted(REQUIRED_RESIDUAL_IDS - ids):
        errors.append(f"retained residual {missing} was dropped")
    for row in residuals:
        if not isinstance(row, dict):
            continue
        for field in ("residual", "measured", "disposition", "ownedBy"):
            if not row.get(field):
                errors.append(f"residual {row.get('id')} records no {field}")

    # ---- no paper seal ----
    if canon(value.get("dischargeStatus")) != canon(
            predecessor.get("dischargeStatus")):
        errors.append("dischargeStatus moved; this successor discharges nothing")
    discharge = value.get("dischargeStatus") or {}
    if discharge.get("seal") != "DO-NOT-SEAL":
        errors.append("seal inflation")
    if discharge.get("CD-RT-5") != "BLOCKED":
        errors.append("CD-RT-5 moved; it remains blocked")
    if discharge.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED":
        errors.append("evidence grade inflation — implementable is not "
                      "DISCHARGED or DEMONSTRATED")
    disposition = repair.get("checkerDisposition") or {}
    if disposition.get("successorCheckerRequired") is not True or \
            disposition.get("checker") != "check-versioning-v9.py":
        errors.append("checker disposition drift")
    if not disposition.get("integerTypeGuard"):
        errors.append("the artifact does not state its integer type-guard "
                      "posture (freeze §6 law 18)")

    return errors


MUTATIONS: list[tuple[str, Any]] = [
    ("revert the D9 citation to the superseded v1.6 artifact",
     lambda c: c["decisionDependencies"][4].__setitem__(
         "source", SUPERSEDED_CITATION)),
    ("point the D9 citation at some other version",
     lambda c: c["decisionDependencies"][4].__setitem__(
         "source", "artifacts/d9-exit-contract.v1.13.json")),
    ("drop the one-way dependency direction (B-SCV2-06)",
     lambda c: c["decisionDependencies"][4].pop("direction")),
    ("rewrite the direction so ownership becomes circular (B-SCV2-06)",
     lambda c: c["decisionDependencies"][4].__setitem__(
         "direction", "D9 depends on VERSIONING.")),
    ("drop the B-SCV2-06 note that records the earlier defect",
     lambda c: c["decisionDependencies"][4].__setitem__("note", "")),
    ("leave the B-SCV2-06 resolution asserting the stale v1.6 citation",
     lambda c: c["resolves"].__setitem__(
         "B-SCV2-06", "RESOLVED — the D9 citation retargets to the live v1.6 "
                      "artifact and VERSIONING depends on D9, not the reverse.")),
    ("respell version as a float (freeze §6 law 18)",
     lambda c: c.__setitem__("version", 9.0)),
    ("respell supersedes as a float (freeze §6 law 18)",
     lambda c: c.__setitem__("supersedes", 8.0)),
    ("respell a measured golden count as a float (freeze §6 law 18)",
     lambda c: c["successorRevision"]["d9CitationRepair"][
         "substanceUnchangedEvidence"]["goldenCases"].__setitem__(
         "shared", 44.0)),
    ("respell an exit code as a float (freeze §6 law 18)",
     lambda c: c["successorRevision"]["d9CitationRepair"][
         "substanceUnchangedEvidence"]["classToExitCode"].__setitem__(
         "success", 0.0)),
    ("respell a protected historical IR major as a float (freeze §6 law 18)",
     lambda c: c["historicalSemanticsPolicy"]["crossMajorFixtures"][4].__setitem__(
         "hostDefaultIrMajor", 4.0)),
    ("overstate the mismatch count as clean when it is not measured",
     lambda c: c["successorRevision"]["d9CitationRepair"][
         "substanceUnchangedEvidence"]["goldenCases"].__setitem__(
         "sharedExitClassMismatches", 1)),
    ("understate the shared golden count",
     lambda c: c["successorRevision"]["d9CitationRepair"][
         "substanceUnchangedEvidence"]["goldenCases"].__setitem__("shared", 40)),
    ("claim the head review covers the v1.6 span",
     lambda c: c["successorRevision"]["d9CitationRepair"][
         "substanceUnchangedEvidence"].__setitem__(
         "whyNotInheritedFromTheHeadReview", "Inherited from the head review.")),
    ("drop a recorded input digest (freeze §7.2 recording obligation)",
     lambda c: c["successorRevision"]["d9CitationRepair"][
         "recordedInputs"].pop(0)),
    ("record an input with a wrong digest",
     lambda c: c["successorRevision"]["d9CitationRepair"]["recordedInputs"][0]
     .__setitem__("sha256", "0" * 64)),
    ("byte-pin the coordinator-owned register",
     lambda c: [row for row in c["successorRevision"]["d9CitationRepair"]
                ["recordedInputs"] if row["artifact"] == REGISTER][0].pop("gate")),
    ("drop the predecessor pin",
     lambda c: c["successorRevision"]["supersedesCandidate"].__setitem__(
         "sha256", "0" * 64)),
    ("change a protected v8 section",
     lambda c: c["custodyClasses"][0].__setitem__("class", "INTERNAL")),
    ("relax the GUESSED support-window seal rule",
     lambda c: c["supportWindows"].__setitem__(
         "sealRule", "Windows may be sealed on a guess.")),
    ("drop the run-manifest NOT-YET-ENFORCEABLE restriction",
     lambda c: c["implementationBacklog"][0].__setitem__(
         "status", "ENFORCEABLE")),
    ("carry the EP8/RT13 cold rejoin away",
     lambda c: c["successorRevision"]["coldStoredReadRejoin"].__setitem__(
         "rule", "Warm cache is authority.")),
    ("silently retarget the carried EP/RT dependency pins",
     lambda c: c["successorRevision"]["inputs"]["retentionCustody"].__setitem__(
         "artifact", "retention-tiers.v22.json")),
    ("absorb a retained residual",
     lambda c: c["successorRevision"]["d9CitationRepair"]["retainedResiduals"]
     .pop(1)),
    ("absorb the EP8/RT13 staleness residual's measurement",
     lambda c: [r for r in c["successorRevision"]["d9CitationRepair"]
                ["retainedResiduals"] if r["id"] == "R-VER9-02"][0]
     .__setitem__("measured", "")),
    ("drop the sibling citation audit",
     lambda c: c["successorRevision"]["d9CitationRepair"]["siblingCitationAudit"]
     .__setitem__("entries", [])),
    ("advance the review status as if v8's PASS transferred",
     lambda c: c.__setitem__("reviewStatus", "PASSED")),
    ("advance the candidate status",
     lambda c: c.__setitem__("status", "APPLIED")),
    ("seal on a paper claim",
     lambda c: c["dischargeStatus"].__setitem__("seal", "SEAL")),
    ("unblock CD-RT-5",
     lambda c: c["dischargeStatus"].__setitem__("CD-RT-5", "DISCHARGED")),
    ("inflate the evidence grade",
     lambda c: c["dischargeStatus"].__setitem__("evidenceGrade", "DEMONSTRATED")),
    ("alter an inherited limitation",
     lambda c: c["knownLimitations"].__setitem__(0, "No limitations.")),
    ("drop the successor limitation delta",
     lambda c: c.__setitem__("knownLimitations", c["knownLimitations"][:17])),
    ("open the successor revision key surface",
     lambda c: c["successorRevision"].__setitem__("extra", 1)),
    ("open the repair record key surface",
     lambda c: c["successorRevision"]["d9CitationRepair"].__setitem__(
         "extra", 1)),
    ("introduce an Evidence back-edge",
     lambda c: c["successorRevision"]["inputs"].__setitem__(
         "evidence", {"artifact": "evidence.v10.json"})),
]


def selftest(value: dict[str, Any]) -> tuple[list[str], int]:
    failures: list[str] = []
    for label, mutate in MUTATIONS:
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
        if not check(candidate, verify_files=False):
            failures.append(f"{label}: ESCAPED — no finding")
    return failures, len(MUTATIONS)


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
            # A dirty base masks every mutation, so the suite must not run and
            # must say so with an exit distinct from green, findings and misuse.
            print("SELFTEST-REFUSED: the base contract has findings, so every "
                  "mutation would be masked by them")
            print("SELFTEST-NOT-RUN")
            return 3
        return 1

    if wants_selftest:
        failures, total = selftest(value)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print(f"PASS: {path.name}; {total} successor mutations rejected, "
              f"including 5 closed-scalar float respellings (freeze §6 law 18)")
        return 0

    print(f"PASS: {path.name}; D9 citation repaired to the register-bound head "
          f"{D9_HEAD}; B-SCV2-06 direction and note byte-identical; exit-class "
          f"contract measured unchanged across the v1.6 to v1.14 span; v8 "
          f"protected surface exact")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED; no seal, freeze, "
          "status advance or product acceptance is declared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
