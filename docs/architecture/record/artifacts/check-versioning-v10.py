#!/usr/bin/env python3
"""Conformance checker for VERSIONING v10 — evidence-leaf enforcement closure.

The v9 CONTRACT survived independent adversarial review intact
(versioning-policy.v9.review-independent.json: "I could not falsify a single
factual claim in versioning-policy.v9.json"). The single blocker was against the
CHECKER, and this file exists to close it.

  B-VER9R-01. check-versioning-v9.py re-measures the d9-exit-contract v1.6 ->
  v1.14 span into a `measured` dict and then compares only 26 of the 102 declared
  evidence leaves against it. The reviewer falsified all 102 one at a time: 76
  exited 0 with the full green PASS banner, including the artifact's own recorded
  supersededCitationSha256/headSha256, all eleven entries of
  byteIdenticalRootsV16ToV114, and — worst — d9CitesVersioningInItsDependencies,
  which could be flipped to true, asserting on the artifact's face the exact
  B-SCV2-06 circularity that dependency record exists to refute.

This checker closes it structurally rather than case by case. Every leaf POSITION
in the three declared evidence sub-blocks is enumerated, classified into exactly
one of MEASURED / GROUNDED / UNMEASURABLE, and compared against a value computed
here from disk. A position with no classification is itself a finding
(VER10-COVER), so the partition cannot silently shrink as the artifact grows, and
the measured partition is compared against the partition the artifact declares
(VER10-PART) and printed in the PASS banner. The same discipline is applied to
v10's own new evidence block.

Three further repairs, all named by the same review:

  * freeze §6 law 18 is symmetric and v9 closed one direction only. The reviewer
    measured 52/52 integer leaves rejecting a float respelling and 52/52
    rejecting a bool respelling, but 15 of 139 boolean leaves ADMITTING an
    integer respelling — all 15 inside the new evidence block, because the
    checker never read them. Here every MEASURED leaf is compared as canonical
    JSON text, which is exact-type by construction in BOTH directions
    (canon(4) != canon(4.0) and canon(True) != canon(1)), and --selftest
    re-derives the boolean-to-integer sweep over this checker's own subject so
    the closure is measured on every run rather than asserted once.

  * decisionDependencies[5] and [6] literally read "current candidate", which is
    false: [5] cites evaluation-proof.v8.json (v13 is highest on disk) and [6]
    cites retention-tiers.v13.json (the register binds retention-tiers.v22.json).
    The review independently confirmed that NOT retargeting them is correct — the
    evaluation-proof substance genuinely changed, proofObligationsByClaimShape
    dropping to zero objects at v10 and claimId moving EVIDENCE -> CD-RT-5 at
    v12 — so only the false LABEL is corrected. That needs no re-derivation, and
    VER10-LABEL rejects a silent retarget as firmly as it rejects the old words.

  * three disclosures v9 omitted or understated are measured here: the
    request-rejected class MEANING broadened across the span, hostTerminationUnion
    and crossAxisInvariants moved, and R-VER9-05 cited one float-admitting
    fixture where all thirteen admit. None of the three affects V4, and the
    decisive check — the distinct exit-code value set is identical in both
    versions — is enforced rather than narrated.

Everything else is carried from versioning-policy.v9.json BYTE-IDENTICAL, and
that is enforced leaf-wise rather than in bulk: substanceUnchangedEvidence and
directionPreservation must be canon-identical to the pinned v9 bytes, and
d9CitationRepair may differ from v9 at exactly the enumerated delta paths and
nowhere else (VER10-CARRY / VER10-DELTA). No measured quantity in the v9 evidence
record was retyped, retuned or re-derived by this successor, and that claim is
mechanically checkable rather than a promise.

Trust order: inert bytes -> SHA-256 verify -> execute from the verified snapshot.
A non-zero exit is not evidence that a guard fired — check-versioning.py's
AttributeError also exits 1 and is indistinguishable from a real finding by exit
status alone. So every finding here carries a stable VER10-* id and names the
position under test, and --selftest asserts on BOTH, not merely on non-zero.

Usage: python3 -I -B artifacts/check-versioning-v10.py [contract] [--selftest]
Exit:  0 clean · 1 findings · 2 IO error · 3 selftest refused or not run
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT = HERE / "versioning-policy.v10.json"

PREDECESSOR = "versioning-policy.v9.json"
PREDECESSOR_CHECKER = "check-versioning-v9.py"
PREDECESSOR_REVIEW = "versioning-policy.v9.review-independent.json"
GRANDPARENT = "versioning-policy.v8.json"
GRANDPARENT_CHECKER = "check-versioning-v8.py"
GRANDPARENT_REVIEW = "versioning-policy.v8.review-independent-cold-rejoin.json"
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
        "9d3f936ae492e2b692781215f92de4b50ef9b962911e9067c7d052825e0492a9",
    PREDECESSOR_CHECKER:
        "cf88da34a68a2697d5040d97d32eeaabcf7217162bf279ab5b546c066210bd80",
    PREDECESSOR_REVIEW:
        "59ba43425d3bd7a25838141ca2b417bf6ac9ecfba973c589cd520d627b27a360",
    GRANDPARENT:
        "ea4b52b5a4d187ec35ad994d8ffcd888db287566c8fb53f3df17e5203d84ae2e",
    GRANDPARENT_CHECKER:
        "82834720a8fd4ec8701dad2b43ad94d6ad9e52d21aeb077f4286fab5fb156844",
    GRANDPARENT_REVIEW:
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

# claim-register.v1.json is deliberately NOT pinned, and this is the one design
# decision the v9 review vindicated empirically: the register drifted a THIRD
# time DURING that review (ff4df1d7… -> 20ab0c31…, 31 -> 33 claims) while its
# D9, VERSIONING and ARCH.RETENTION-TIERS bindings held byte-identical and
# check-versioning-v9.py passed under both. "A byte pin would have failed on the
# very repoint it anticipates." The gate is the semantic invariant instead.

CHANGED = {
    "version", "supersedes", "role", "decisionDependencies", "knownLimitations",
    "successorRevision",
}

EXPECTED_REVISION_KEYS = {
    "id", "candidateState", "supersedesCandidate", "inputs",
    "rawAuthorityKinds", "custodyRule", "storeAuthorityRule",
    "identityStability", "forbiddenBackEdge", "coldStoredReadRejoin",
    "dependencyLabelRule", "d9CitationRepair", "evidenceEnforcementRepair",
}

EXPECTED_REPAIR_KEYS = {
    "findingId", "authoredBy", "defect", "whyItWasInvisible",
    "whySuccessorAndNotInPlaceRepair", "citation", "recordedInputs",
    "substanceUnchangedEvidence", "directionPreservation",
    "siblingCitationAudit", "retainedResiduals", "checkerDisposition",
    "notClaimed",
}

EXPECTED_ENFORCEMENT_KEYS = {
    "findingId", "authoredBy", "reviewOfRecord", "defect",
    "whySuccessorAndNotInPlaceRepair", "carriedByteIdentical",
    "evidenceLeafEnforcement", "closedScalarAdmission", "spanDisclosure",
    "dependencyLabelCorrection", "residualRestatements", "recordedInputs",
    "retainedResiduals", "checkerDisposition", "notClaimed",
}

CARRIED_RESIDUAL_IDS = {
    "R-VER9-01", "R-VER9-02", "R-VER9-03", "R-VER9-04", "R-VER9-05",
    "R-VER9-06", "R-VER9-07",
}

REQUIRED_RESIDUAL_IDS = {
    "R-VER10-01", "R-VER10-02", "R-VER10-03", "R-VER10-04", "R-VER10-05",
    "R-VER10-06", "R-VER10-07", "R-VER10-08", "R-VER10-09",
}

OWNER_VOCABULARY = {
    "coordinator", "independent reviewer", "phase1a successor lane",
    "phase1a evidence-enforcement lane", "rust provider protocol lane",
    "closed for v10; v9 residual retained",
}

ADDED_LIMITATION_COUNT = 6

REPAIRED_CITATION = "artifacts/" + D9_HEAD
SUPERSEDED_CITATION = "artifacts/" + D9_SUPERSEDED

REPAIR = "successorRevision.d9CitationRepair"
ENFORCE = "successorRevision.evidenceEnforcementRepair"
EVIDENCE_SCOPE = (
    f"{REPAIR}.substanceUnchangedEvidence",
    f"{REPAIR}.directionPreservation",
    f"{REPAIR}.siblingCitationAudit",
)
# The two sub-blocks carrying every measured quantity must be byte-identical to
# the reviewed v9 bytes. v10 retunes no number the v9 reviewer verified.
FROZEN_SUB_BLOCKS = ("substanceUnchangedEvidence", "directionPreservation")

# The only leaf paths inside d9CitationRepair that may differ from v9, relative
# to d9CitationRepair. Anything else that moves is VER10-CARRY; anything here
# that does NOT move is VER10-DELTA.
ENUMERATED_DELTA = {
    "siblingCitationAudit.entries[5].source",
    "siblingCitationAudit.entries[5].result",
    "siblingCitationAudit.entries[6].source",
    "siblingCitationAudit.entries[6].result",
    "siblingCitationAudit.measuredResult",
    "retainedResiduals[4].measured",
    "retainedResiduals[5].measured",
    "checkerDisposition.checker",
    "checkerDisposition.integerTypeGuard",
    "checkerDisposition.booleanTypeGuard",
    "checkerDisposition.evidenceLeafEnforcement",
}

STALE_LABEL_PHRASE = "; current candidate)"
LABEL_TOKENS = ("AS-REVIEWED PIN", "NOT THE CURRENT CANDIDATE", "R-VER9-02")

MEASURED = "MEASURED"
GROUNDED = "GROUNDED"
UNMEASURABLE = "UNMEASURABLE"

LAST: dict[str, Any] = {}


# ---------------------------------------------------------------- primitives

def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text())


def sha_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def canon(value: Any) -> str:
    """Canonical JSON text. Unlike Python equality this distinguishes 4 from 4.0
    AND True from 1, so every canon comparison below is an exact-type admission
    in both directions of freeze §6 law 18 — the direction v9 closed and the
    direction it left open."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def module(filename: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def exact_int(value: Any) -> bool:
    """``type(x) is int`` rejects both float and bool; ``isinstance`` admits
    bool, which is how 15 booleans became respellable in the predecessor."""
    return type(value) is int


def exact_bool(value: Any) -> bool:
    """The symmetric guard v9 did not have."""
    return type(value) is bool


def add(errors: list[str], code: str, message: str) -> None:
    errors.append(f"{code}: {message}")


def positions(value: Any, path: str, out: list[str]) -> None:
    """Every falsifiable leaf POSITION, including nulls and empty containers — a
    null can be replaced with a string and an empty list can be extended, so both
    are probe sites and both must be classified. The independent reviewer's
    probe set excluded them, giving 102 where this enumeration gives 116; both
    counts are declared and compared."""
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
    """Leaf-wise difference. Returns exact positions rather than a bulk verdict,
    so a carried-bytes finding can name the position under test."""
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
    """The v10 delta introduces no float anywhere. Any float in this subtree is
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


# ---------------------------------------------------------------- measurement

def measure_d9_span(old: Any, new: Any) -> dict[str, Any]:
    """Re-derive the exit-class contract across the v1.6 -> v1.14 span from both
    artifacts on disk. This is the evidence the repair rests on and it is
    computed here, not read from the artifact. The v1.14 independent review
    re-derives against v1.13, not v1.6, so it does not attest this span."""
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
        # O-01 / O-02: the span motions v9 did not enumerate, measured so they
        # are named rather than omitted. None can affect V4 and the exit-code
        # value set above is the decisive check that none did.
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


def measure_audit(deps: list[Any], claims: list[Any]) -> list[dict[str, Any]]:
    """Recompute every audit column from disk and from the live register rather
    than accepting the artifact's declaration. In v9 fileResolves and
    anchorResolves had zero references anywhere in the checker: the audit that
    discovered the two remaining stale citations was itself unverified by the
    instrument that reported it."""
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
            slugs = {slugify(line.lstrip("#"))
                     for line in path.read_text().splitlines()
                     if line.startswith("#")}
            anchor_resolves = anchor in slugs
        if identifier:
            binding = next((c.get("bindingArtifact") for c in claims
                            if c.get("id") == identifier), None)
        else:
            # Bare label strings carry no id, which is exactly why VER-DEP is
            # structurally blind to them. Derive the register claim from the
            # artifact FAMILY of the citation instead, mechanically reproducing
            # the step the v9 author took by hand for entry 6.
            family = pathlib.PurePosixPath(
                source.split(" ")[0]).name.split(".v")[0]
            hits = sorted({c.get("bindingArtifact") for c in claims
                           if c.get("bindingArtifact") and
                           pathlib.PurePosixPath(
                               c["bindingArtifact"]).name.split(".v")[0]
                           == family})
            binding = hits[0] if len(hits) == 1 else None
        out.append({"index": index, "id": identifier, "source": source,
                    "fileResolves": file_resolves,
                    "anchorResolves": anchor_resolves,
                    "registerBinding": binding})
    return out


def measure_review(review: Any) -> dict[str, Any]:
    """Read the predecessor's independent review as an INPUT, not as a claim.
    The 26/76/102 partition and the 52/139/15 sweep are the reviewer's measured
    figures; this artifact must restate them exactly or not at all."""
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
        "blockingFindingCount": review.get("blockingFindingCount"),
        "nonBlockingObservationCount": review.get("nonBlockingObservationCount"),
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


# ------------------------------------------------------- enforcement registry

def eq(expected: Any) -> tuple[str, str, Any]:
    return (MEASURED, "eq", expected)


def sub(*needles: Any) -> tuple[str, str, Any]:
    return (GROUNDED, "sub", [str(n) for n in needles if n not in (None, "")])


def vocab(allowed: Any) -> tuple[str, str, Any]:
    return (GROUNDED, "vocab", allowed)


def boundary() -> tuple[str, str, Any]:
    return (GROUNDED, "boundary", None)


def open_prose(reason: str) -> tuple[str, str, Any]:
    return (UNMEASURABLE, "prose", reason)


def evidence_registry(value: Any, deps: list[Any], measured: dict[str, Any],
                      audit: list[dict[str, Any]],
                      direction_preserved: bool) -> dict[str, Any]:
    """One entry for every leaf position in the three declared evidence
    sub-blocks. This is the structural answer to B-VER9R-01: a position with no
    entry is VER10-COVER, so this checker can never again compute a value and
    then decline to compare the declaration against it."""
    s = f"{REPAIR}.substanceUnchangedEvidence"
    d = f"{REPAIR}.directionPreservation"
    a = f"{REPAIR}.siblingCitationAudit"
    reg: dict[str, Any] = {}
    v4_clean = (not measured["exitClassesRemoved"] and
                measured["classToExitCodeByteIdentical"] and
                not measured["sharedExitClassMismatches"] and
                not measured["sharedNumericExitCodeMismatches"])

    # ---- substanceUnchangedEvidence
    reg[f"{s}.question"] = sub("additive-only exit-class rule (V4)")
    reg[f"{s}.answer"] = sub("YES" if v4_clean else "NO", "measured")
    reg[f"{s}.measuredBetween.supersededCitation"] = eq(D9_SUPERSEDED)
    reg[f"{s}.measuredBetween.supersededCitationSha256"] = \
        eq(sha_file(D9_SUPERSEDED))
    reg[f"{s}.measuredBetween.head"] = eq(D9_HEAD)
    reg[f"{s}.measuredBetween.headSha256"] = eq(sha_file(D9_HEAD))
    reg[f"{s}.whyNotInheritedFromTheHeadReview"] = sub(
        "v1.13", "v1.6", "IDENTICAL under v1.13 and v1.14")
    for index, name in enumerate(measured["exitClassesV16"]):
        reg[f"{s}.exitClassSet.v16[{index}]"] = eq(name)
    for index, name in enumerate(measured["exitClassesV114"]):
        reg[f"{s}.exitClassSet.v114[{index}]"] = eq(name)
    reg[f"{s}.exitClassSet.removed"] = eq(measured["exitClassesRemoved"])
    reg[f"{s}.exitClassSet.added"] = eq(measured["exitClassesAdded"])
    reg[f"{s}.exitClassSet.identical"] = eq(measured["exitClassSetIdentical"])
    reg[f"{s}.classToExitCodeByteIdentical"] = \
        eq(measured["classToExitCodeByteIdentical"])
    for name, code in measured["classToExitCode"].items():
        reg[f"{s}.classToExitCode.{name}"] = eq(code)
    reg[f"{s}.goldenCases.countV16"] = eq(measured["countV16"])
    reg[f"{s}.goldenCases.countV114"] = eq(measured["countV114"])
    reg[f"{s}.goldenCases.shared"] = eq(measured["shared"])
    reg[f"{s}.goldenCases.removed"] = eq(measured["removed"])
    reg[f"{s}.goldenCases.sharedExitClassMismatches"] = \
        eq(measured["sharedExitClassMismatches"])
    reg[f"{s}.goldenCases.sharedReasonOrErrorCodeMismatches"] = \
        eq(measured["sharedReasonOrErrorCodeMismatches"])
    reg[f"{s}.goldenCases.sharedNumericExitCodeMismatches"] = \
        eq(measured["sharedNumericExitCodeMismatches"])
    for field, values in (("added", measured["added"]),
                          ("changedShared", measured["changedShared"]),
                          ("remediesAdded", measured["remediesAdded"])):
        prefix = f"{s}.codeVocabulary" if field.startswith("remedies") \
            else f"{s}.goldenCases"
        if not values:
            reg[f"{prefix}.{field}"] = eq([])
        for index, name in enumerate(values):
            reg[f"{prefix}.{field}[{index}]"] = eq(name)
    detail_needles: list[Any] = []
    for gid, row in measured["changedSharedDetail"].items():
        detail_needles.extend([gid, row["class"], row["errorCode"]])
        detail_needles.extend(row["droppedFields"])
    reg[f"{s}.goldenCases.changedSharedDisposition"] = sub(*detail_needles)
    reg[f"{s}.codeVocabulary.reasonCodesByteIdentical"] = \
        eq(measured["reasonCodesByteIdentical"])
    reg[f"{s}.codeVocabulary.errorCodesByteIdentical"] = \
        eq(measured["errorCodesByteIdentical"])
    reg[f"{s}.codeVocabulary.remediesRemoved"] = eq(measured["remediesRemoved"])
    for index, name in enumerate(measured["byteIdenticalRoots"]):
        reg[f"{s}.byteIdenticalRootsV16ToV114[{index}]"] = eq(name)
    if not measured["byteIdenticalRoots"]:
        reg[f"{s}.byteIdenticalRootsV16ToV114"] = eq([])
    reg[f"{s}.conclusion"] = sub("byte-identical", "additive", "V4",
                                 *measured["addedGoldenClasses"])

    # ---- directionPreservation
    d9_dep = deps[4] if len(deps) > 4 and isinstance(deps[4], dict) else {}
    reg[f"{d}.declared"] = eq(d9_dep.get("direction"))
    reg[f"{d}.preservedByteIdentical"] = eq(direction_preserved)
    reg[f"{d}.reVerifiedAtHead.d9DecisionDependenciesByteIdenticalV16ToV114"] = \
        eq(measured["d9DepsByteIdentical"])
    reg[f"{d}.reVerifiedAtHead.d9CitesAnyVersioningPolicyArtifact"] = \
        eq(measured["d9CitesVersioningPolicy"])
    reg[f"{d}.reVerifiedAtHead.d9CitesVersioningInItsDependencies"] = \
        eq(measured["d9CitesVersioningInDeps"])
    reg[f"{d}.reVerifiedAtHead.finding"] = sub(
        D9_HEAD, "one-way", "B-SCV2-06", "decisionDependencies")

    # ---- siblingCitationAudit
    reg[f"{a}.method"] = sub(REGISTER, "decisionDependencies", "heading slugs")
    for row in audit:
        index = row["index"]
        reg[f"{a}.entries[{index}].index"] = eq(index)
        reg[f"{a}.entries[{index}].id"] = eq(row["id"])
        reg[f"{a}.entries[{index}].source"] = eq(row["source"])
        reg[f"{a}.entries[{index}].fileResolves"] = eq(row["fileResolves"])
        reg[f"{a}.entries[{index}].anchorResolves"] = eq(row["anchorResolves"])
        reg[f"{a}.entries[{index}].registerBinding"] = eq(row["registerBinding"])
        if index == 4:
            reg[f"{a}.entries[{index}].result"] = sub(
                "REPAIRED IN THIS VERSION", D9_SUPERSEDED, "register binding")
        elif row["id"] is None:
            reg[f"{a}.entries[{index}].result"] = sub(
                "STALE", "R-VER9-02", row["source"].split(" ")[0])
        else:
            reg[f"{a}.entries[{index}].result"] = sub("CLEAN")
    prose = at(value, f"{a}.prose") if resolves_in(value, f"{a}.prose") else []
    for index in range(len(prose) if isinstance(prose, list) else 0):
        reg[f"{a}.prose[{index}].field"] = (MEASURED, "field", None)
        reg[f"{a}.prose[{index}].result"] = sub(
            "REPAIRED IN THIS VERSION" if index == 0
            else "CARRIED FORWARD UNCHANGED")
    reg[f"{a}.measuredResult"] = sub(
        f"{len(deps)} decisionDependencies entries",
        sum(1 for r in audit if r["anchorResolves"] is True),
        sum(1 for r in audit if r["id"] is None),
        "R-VER9-02")
    return reg


def enforcement_registry(value: Any, deps: list[Any], measured: dict[str, Any],
                         review_facts: dict[str, Any], partition: dict[str, Any],
                         delta: list[str], frozen_ok: list[str],
                         carry_covered: int) -> dict[str, Any]:
    """The same discipline applied to v10's OWN new evidence. Nothing computed
    here is left uncompared either."""
    e = ENFORCE
    reg: dict[str, Any] = {}
    reg[f"{e}.findingId"] = eq(review_facts["blockerId"])
    reg[f"{e}.authoredBy"] = open_prose(
        "lane attribution: no on-disk referent exists to compare it against")
    reg[f"{e}.reviewOfRecord.artifact"] = eq(PREDECESSOR_REVIEW)
    reg[f"{e}.reviewOfRecord.sha256"] = eq(sha_file(PREDECESSOR_REVIEW))
    reg[f"{e}.reviewOfRecord.verdict"] = eq(review_facts["verdict"])
    reg[f"{e}.reviewOfRecord.blockingFindingCount"] = \
        eq(review_facts["blockingFindingCount"])
    reg[f"{e}.reviewOfRecord.nonBlockingObservationCount"] = \
        eq(review_facts["nonBlockingObservationCount"])
    reg[f"{e}.reviewOfRecord.blockerIsAgainst"] = eq(PREDECESSOR_CHECKER)
    reg[f"{e}.reviewOfRecord.blockerIsNotAgainst"] = eq(PREDECESSOR)
    reg[f"{e}.reviewOfRecord.reviewerStatement"] = (MEASURED, "inreview", None)
    reg[f"{e}.defect"] = sub(review_facts["enforced"], review_facts["unenforced"],
                             review_facts["probed"], PREDECESSOR_CHECKER)
    reg[f"{e}.whySuccessorAndNotInPlaceRepair"] = sub("§7.2", PREDECESSOR)

    c = f"{e}.carriedByteIdentical"
    reg[f"{c}.rule"] = sub("byte-identical", PREDECESSOR)
    for index, name in enumerate(frozen_ok):
        reg[f"{c}.byteIdenticalSubBlocks[{index}]"] = eq(name)
    if not frozen_ok:
        reg[f"{c}.byteIdenticalSubBlocks"] = eq([])
    reg[f"{c}.enumeratedDeltaCount"] = eq(len(delta))
    for index, path in enumerate(delta):
        reg[f"{c}.enumeratedDelta[{index}].path"] = eq(path)
        reg[f"{c}.enumeratedDelta[{index}].why"] = sub(
            path.split(".")[-1].split("[")[0])

    f = f"{e}.evidenceLeafEnforcement"
    for index, path in enumerate(EVIDENCE_SCOPE):
        reg[f"{f}.scope[{index}]"] = eq(path)
    reg[f"{f}.reviewerProbeSetSize"] = eq(partition["probeSetSize"])
    reg[f"{f}.reviewerProbeSetDefinition"] = sub("null", "empty")
    reg[f"{f}.fullPositionSetSize"] = eq(partition["total"])
    reg[f"{f}.predecessor.checker"] = eq(PREDECESSOR_CHECKER)
    reg[f"{f}.predecessor.enforced"] = eq(review_facts["enforced"])
    reg[f"{f}.predecessor.unenforced"] = eq(review_facts["unenforced"])
    reg[f"{f}.predecessor.measuredBy"] = sub(PREDECESSOR_REVIEW)
    reg[f"{f}.partition.MEASURED"] = eq(partition["measured"])
    reg[f"{f}.partition.GROUNDED"] = eq(partition["grounded"])
    reg[f"{f}.partition.UNMEASURABLE"] = eq(partition["unmeasurable"])
    reg[f"{f}.partition.total"] = eq(partition["total"])
    reg[f"{f}.gradeDefinitions.MEASURED"] = sub("computed", "disk")
    reg[f"{f}.gradeDefinitions.GROUNDED"] = sub("prose", "substring")
    reg[f"{f}.gradeDefinitions.UNMEASURABLE"] = sub("no on-disk referent")
    for field, values in (("measuredLeaves", partition["measuredLeaves"]),
                          ("groundedLeaves", partition["groundedLeaves"])):
        if not values:
            reg[f"{f}.{field}"] = eq([])
        for index, path in enumerate(values):
            reg[f"{f}.{field}[{index}]"] = eq(path)
    if not partition["unmeasurableLeaves"]:
        reg[f"{f}.unmeasurableLeaves"] = eq([])
    for index, path in enumerate(partition["unmeasurableLeaves"]):
        reg[f"{f}.unmeasurableLeaves[{index}].path"] = eq(path)
        reg[f"{f}.unmeasurableLeaves[{index}].reason"] = sub("referent")
    reg[f"{f}.carryIdentityCoverage.positionsAlsoByteGatedAgainstV9"] = \
        eq(carry_covered)
    reg[f"{f}.carryIdentityCoverage.rule"] = sub(PREDECESSOR, "byte-identical")

    k = f"{e}.closedScalarAdmission"
    reg[f"{k}.law"] = sub("law 18", "exact-type")
    reg[f"{k}.integerDirection.integerLeavesInV9"] = \
        eq(review_facts["integerLeaves"])
    reg[f"{k}.integerDirection.intToFloatAdmittedInV9"] = \
        eq(review_facts["intToFloatAdmitted"])
    reg[f"{k}.integerDirection.intToBoolAdmittedInV9"] = \
        eq(review_facts["intToBoolAdmitted"])
    reg[f"{k}.integerDirection.disposition"] = sub("closed")
    reg[f"{k}.booleanDirection.booleanLeavesInV9"] = \
        eq(review_facts["booleanLeaves"])
    reg[f"{k}.booleanDirection.boolToIntAdmittedInV9"] = \
        eq(review_facts["boolToIntAdmitted"])
    reg[f"{k}.booleanDirection.booleanLeavesSweptInV10"] = \
        (UNMEASURABLE, "sweptBySelftest",
         "re-derived by --selftest, which respells each boolean and re-runs the "
         "whole check; a plain run cannot re-run the sweep without recursing "
         "into itself, so a plain run gates only the exact-integer type here")
    reg[f"{k}.booleanDirection.boolToIntAdmittedInV10"] = \
        (UNMEASURABLE, "sweptBySelftest",
         "re-derived by --selftest; see R-VER10-03 for the measured boundary of "
         "what a plain run does and does not establish")
    reg[f"{k}.booleanDirection.sweptBy"] = sub("--selftest")
    reg[f"{k}.booleanDirection.scope"] = sub("successorRevision")
    reg[f"{k}.corpusAsymmetry"] = sub("§7.4")

    p = f"{e}.spanDisclosure"
    reg[f"{p}.whyDisclosed"] = sub("V4")
    for field, values in (
            ("exitClassMeaningBroadened", measured["exitClassMeaningsChanged"]),
            ("crossAxisInvariantsAdded", measured["crossAxisInvariantsAdded"]),
            ("exitCodeValueSetV16", measured["exitCodeValueSetV16"]),
            ("exitCodeValueSetV114", measured["exitCodeValueSetV114"]),
            ("changedRootsV16ToV114", measured["changedSharedRoots"])):
        if not values:
            reg[f"{p}.{field}"] = eq([])
        for index, item in enumerate(values):
            reg[f"{p}.{field}[{index}]"] = eq(item)
    reg[f"{p}.exitClassesAddedOrRemoved"] = eq(
        measured["exitClassesAdded"] + measured["exitClassesRemoved"])
    reg[f"{p}.hostTerminationUnionChanged"] = \
        eq(measured["hostTerminationUnionChanged"])
    reg[f"{p}.detailsSemanticAuthority"] = eq(measured["detailsSemanticAuthority"])
    reg[f"{p}.detailsControlFlowUse"] = eq(measured["detailsControlFlowUse"])
    reg[f"{p}.v4Verdict"] = sub("V4", "unaffected")

    n = f"{e}.dependencyLabelCorrection"
    reg[f"{n}.findingId"] = eq("O-03")
    reg[f"{n}.whyNoRederivation"] = sub("label", "re-derivation")
    reg[f"{n}.retargetingRemainsDeferred"] = sub("R-VER9-02")
    for slot, index in enumerate((5, 6)):
        reg[f"{n}.corrected[{slot}].index"] = eq(index)
        reg[f"{n}.corrected[{slot}].was"] = (MEASURED, "wasLabel", index)
        reg[f"{n}.corrected[{slot}].now"] = eq(
            deps[index] if index < len(deps) else None)
        reg[f"{n}.corrected[{slot}].citationTargetMoved"] = eq(False)

    r = f"{e}.residualRestatements"
    restated = at(value, r) if resolves_in(value, r) else []
    for index in range(len(restated) if isinstance(restated, list) else 0):
        reg[f"{r}[{index}].id"] = (MEASURED, "carriedResidual", None)
        reg[f"{r}[{index}].reviewObservation"] = sub("O-0")
        reg[f"{r}[{index}].wasRecorded"] = boundary()
        reg[f"{r}[{index}].nowMeasured"] = boundary()

    i = f"{e}.recordedInputs"
    recorded = at(value, i) if resolves_in(value, i) else []
    for index, row in enumerate(recorded if isinstance(recorded, list) else []):
        name = row.get("artifact") if isinstance(row, dict) else None
        reg[f"{i}[{index}].artifact"] = (MEASURED, "pinName", None)
        reg[f"{i}[{index}].sha256"] = (MEASURED, "pinDigest", name)
        reg[f"{i}[{index}].role"] = open_prose(
            "free-text role of a pinned input; the digest beside it is measured")
        if isinstance(row, dict) and "gate" in row:
            reg[f"{i}[{index}].gate"] = sub("RECORDED-NOT-PINNED")

    t = f"{e}.retainedResiduals"
    residuals = at(value, t) if resolves_in(value, t) else []
    for index in range(len(residuals) if isinstance(residuals, list) else 0):
        reg[f"{t}[{index}].id"] = (MEASURED, "residualId", None)
        reg[f"{t}[{index}].residual"] = open_prose(
            "statement of what remains open; enforced as present and non-empty")
        reg[f"{t}[{index}].measured"] = boundary()
        reg[f"{t}[{index}].disposition"] = open_prose(
            "statement of how the residual is dispositioned")
        reg[f"{t}[{index}].ownedBy"] = vocab(OWNER_VOCABULARY)

    x = f"{e}.checkerDisposition"
    reg[f"{x}.successorCheckerRequired"] = eq(True)
    reg[f"{x}.checker"] = eq(pathlib.Path(__file__).name)
    reg[f"{x}.checkerEnforcesEveryDeclaredEvidenceLeaf"] = eq(True)
    reg[f"{x}.whyTheV9CheckerCannotValidateV10"] = sub(PREDECESSOR_CHECKER)
    reg[f"{x}.evidenceGrade"] = sub("IMPLEMENTABLE_UNEXECUTED")
    notclaimed = at(value, f"{e}.notClaimed") \
        if resolves_in(value, f"{e}.notClaimed") else []
    for index in range(len(notclaimed) if isinstance(notclaimed, list) else 0):
        reg[f"{e}.notClaimed[{index}]"] = sub("not", "no")
    return reg


def compare(value: Any, path: str, kind: str, payload: Any, declared: Any,
            extra: dict[str, Any]) -> str | None:
    if kind == "eq":
        if canon(declared) == canon(payload):
            return None
        if type(declared) is not type(payload) and (
                isinstance(declared, (int, float, bool)) or
                isinstance(payload, (int, float, bool))):
            return (f"VER10-LEAFTYPE: {path} declares {declared!r} "
                    f"({type(declared).__name__}); this checker measured "
                    f"{payload!r} ({type(payload).__name__}). freeze §6 law 18: "
                    f"closed-scalar admission is exact-type in BOTH directions")
        return (f"VER10-LEAF: {path} declares {canon(declared)[:110]}; this "
                f"checker measured {canon(payload)[:110]} from disk")
    if kind in ("sub", "prose", "boundary", "vocab"):
        if not isinstance(declared, str) or not declared.strip():
            return f"VER10-PROSE: {path} is not a non-empty string"
    if kind == "sub":
        missing = [n for n in payload if n not in declared]
        if missing:
            return (f"VER10-PROSE: {path} does not state the measured "
                    f"assertion(s) {missing} this checker derived from disk")
        return None
    if kind == "prose":
        return None
    if kind == "boundary":
        if not re.search(r"\d", declared):
            return (f"VER10-RESID: {path} states no measured number — every "
                    f"residual states its own boundary as a measured number")
        return None
    if kind == "vocab":
        if declared not in payload:
            return (f"VER10-LEAF: {path} declares {declared!r}, which is not in "
                    f"the closed vocabulary {sorted(payload)}")
        return None
    if kind == "field":
        if not isinstance(declared, str) or not declared.strip():
            return f"VER10-LEAF: {path} names no field"
        for token in re.split(r"\s*/\s*", declared):
            normalised = token.replace("['", ".").replace("']", "").strip()
            if not normalised:
                continue
            if not resolves_in(value, normalised) and \
                    not resolves_in(value, f"successorRevision.{normalised}"):
                return (f"VER10-LEAF: {path} names {token!r}, which does not "
                        f"resolve in this artifact")
        return None
    if kind == "inreview":
        if not isinstance(declared, str) or declared not in extra["reviewText"]:
            return (f"VER10-LEAF: {path} quotes the independent review, but the "
                    f"quoted text does not occur in {PREDECESSOR_REVIEW}")
        return None
    if kind == "wasLabel":
        was = extra["predecessorDeps"][payload]
        if canon(declared) != canon(was):
            return (f"VER10-LEAF: {path} declares the superseded label "
                    f"{canon(declared)[:70]}; {PREDECESSOR} carries "
                    f"{canon(was)[:70]}")
        return None
    if kind == "carriedResidual":
        if declared not in CARRIED_RESIDUAL_IDS:
            return (f"VER10-LEAF: {path} restates {declared!r}, which is not a "
                    f"residual carried from {PREDECESSOR}")
        return None
    if kind == "residualId":
        if declared not in REQUIRED_RESIDUAL_IDS:
            return (f"VER10-LEAF: {path} declares {declared!r}, which is not a "
                    f"v10 residual id")
        return None
    if kind == "sweptBySelftest":
        if not exact_int(declared) or declared < 0:
            return (f"VER10-LEAFTYPE: {path} is not an exact non-negative "
                    f"integer (freeze §6 law 18)")
        return None
    if kind == "pinName":
        if declared not in PINS and declared != REGISTER:
            return (f"VER10-RECORD: {path} records {declared!r}, which is not a "
                    f"pinned input of this successor")
        return None
    if kind == "pinDigest":
        if not isinstance(declared, str) or len(declared) != 64:
            return f"VER10-RECORD: {path} is not a sha256"
        if payload in PINS and declared != PINS[payload]:
            return (f"VER10-RECORD: {path} records {declared[:16]}… for "
                    f"{payload}; the bytes on disk hash to {PINS[payload][:16]}…")
        return None
    return f"VER10-COVER: {path} has an unknown comparator {kind!r}"


def evaluate(value: Any, reg: dict[str, Any], scope: tuple[str, ...],
             extra: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    """Compare every position against its registry entry and return both the
    findings and the measured partition. The partition is a first-class output:
    it is published in the banner and compared against the declaration."""
    errors: list[str] = []
    found: list[str] = []
    for root in scope:
        if resolves_in(value, root):
            positions(at(value, root), root, found)
        else:
            add(errors, "VER10-COVER",
                f"declared evidence sub-block {root} is absent")
    graded: dict[str, list[str]] = {MEASURED: [], GROUNDED: [], UNMEASURABLE: []}

    for path in found:
        entry = reg.get(path)
        if entry is None:
            add(errors, "VER10-COVER",
                f"leaf position {path} has no enforcement classification — "
                f"every declared evidence leaf must be compared against a "
                f"measurement or declared unmeasurable and counted (B-VER9R-01)")
            continue
        grade, kind, payload = entry
        graded[grade].append(path)
        message = compare(value, path, kind, payload, at(value, path), extra)
        if message:
            errors.append(message)

    for path in sorted(set(reg) - set(found)):
        if any(path.startswith(root) for root in scope):
            add(errors, "VER10-COVER",
                f"the enforcement registry expects leaf position {path}, but "
                f"the artifact does not declare it")

    return errors, {
        "total": len(found),
        "probeSetSize": sum(1 for p in found
                            if at(value, p) not in (None, [], {})),
        "measured": len(graded[MEASURED]),
        "grounded": len(graded[GROUNDED]),
        "unmeasurable": len(graded[UNMEASURABLE]),
        "measuredLeaves": sorted(graded[MEASURED]),
        "groundedLeaves": sorted(graded[GROUNDED]),
        "unmeasurableLeaves": sorted(graded[UNMEASURABLE]),
    }


# ----------------------------------------------------------------- the check

def check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["VER10-SURFACE: root is not an object"]

    try:
        for name, expected in PINS.items():
            if sha_file(name) != expected:
                raise ValueError(f"pinned input drift: {name}")
        predecessor = load(HERE / PREDECESSOR)
        grandparent = load(HERE / GRANDPARENT)
        d9_old = load(HERE / D9_SUPERSEDED)
        d9_new = load(HERE / D9_HEAD)
        review_text = (HERE / PREDECESSOR_REVIEW).read_text()
        review_facts = measure_review(json.loads(review_text))
        head_review_text = (HERE / D9_HEAD_REVIEW).read_text()
    except Exception as exc:
        return [f"VER10-PIN: pinned input load failed: {type(exc).__name__}: "
                f"{exc}"]

    measured = measure_d9_span(d9_old, d9_new)

    if verify_files:
        try:
            oldmod = module(PREDECESSOR_CHECKER, "versioning_v9_pinned_for_v10")
            old_errors = oldmod.check(predecessor)
        except Exception as exc:
            old_errors = [f"{type(exc).__name__}: {exc}"]
        if old_errors:
            add(errors, "VER10-PRED",
                f"VERSIONING v9 predecessor is red: {old_errors[0]}")
        try:
            done = subprocess.run(
                [sys.executable, "-I", "-B", str(HERE / D9_HEAD_CHECKER)],
                cwd=str(HERE), capture_output=True, text=True)
            if done.returncode != 0:
                add(errors, "VER10-D9",
                    f"D9 head dependency is red: {D9_HEAD_CHECKER} exited "
                    f"{done.returncode}")
        except Exception as exc:
            add(errors, "VER10-D9", f"D9 head checker did not run: "
                                    f"{type(exc).__name__}: {exc}")

    # ---- protected surface, compared as canonical JSON text (law 18) ----
    if set(value) != set(predecessor):
        add(errors, "VER10-SURFACE",
            "top-level surface differs from VERSIONING v9")
    for key in set(predecessor) - CHANGED:
        if canon(value.get(key)) != canon(predecessor.get(key)):
            add(errors, "VER10-SURFACE",
                f"protected VERSIONING v9 section changed: {key}")

    # ---- identity, exact-type in both directions ----
    if value.get("artifact") != "opensip.versioning-policy":
        add(errors, "VER10-ID", "artifact identity drift")
    if not exact_int(value.get("version")) or value.get("version") != 10:
        add(errors, "VER10-ID",
            "version is not exactly integer 10 (freeze §6 law 18: neither a "
            "float nor a bool respelling is an integer)")
    if not exact_int(value.get("supersedes")) or value.get("supersedes") != 9:
        add(errors, "VER10-ID",
            "supersedes is not exactly integer 9 (freeze §6 law 18)")

    # ---- no status may move ----
    if value.get("status") != predecessor.get("status"):
        add(errors, "VER10-STATUS",
            "status moved; this successor advances no status")
    if value.get("reviewStatus") != predecessor.get("reviewStatus"):
        add(errors, "VER10-STATUS",
            "reviewStatus moved; the v9 review returned CHANGES-REQUIRED and no "
            "verdict transfers to v10 (§7.2)")
    role = value.get("role") or ""
    if "evidence-enforcement successor" not in role or "B-SCV2-06" not in role:
        add(errors, "VER10-STATUS", "narrow successor role drift")

    # ---- decisionDependencies: only the [5]/[6] LABELS may move ----
    deps = value.get("decisionDependencies")
    pred_deps = predecessor.get("decisionDependencies", [])
    v8_deps = grandparent.get("decisionDependencies", [])
    if not isinstance(deps, list) or len(deps) != len(pred_deps):
        add(errors, "VER10-DEP", "decisionDependencies arity changed")
        deps = list(pred_deps)
    else:
        for index, (now, was) in enumerate(zip(deps, pred_deps)):
            if index in (5, 6):
                continue
            if canon(now) != canon(was):
                add(errors, "VER10-DEP",
                    f"decisionDependencies[{index}] changed; only the stale "
                    f"[5]/[6] LABELS may move in this successor")
        d9 = deps[4]
        if not isinstance(d9, dict) or d9.get("id") != "D9":
            add(errors, "VER10-DEP",
                "decisionDependencies[4] is not the D9 dependency")
        else:
            if d9.get("source") != REPAIRED_CITATION:
                add(errors, "VER10-DEP",
                    f"decisionDependencies[4] D9 citation is "
                    f"{d9.get('source')!r}, expected {REPAIRED_CITATION!r}")
            if d9.get("source") == SUPERSEDED_CITATION:
                add(errors, "VER10-DEP",
                    "decisionDependencies[4] D9 citation is still the "
                    "superseded v1.6 artifact (B-SCV2-06 unrepaired)")
            v8_d9 = v8_deps[4] if len(v8_deps) > 4 else {}
            for field in ("id", "claim", "direction", "note"):
                if canon(d9.get(field)) != canon(v8_d9.get(field)):
                    add(errors, "VER10-DEP",
                        f"decisionDependencies[4].{field} differs from "
                        f"{GRANDPARENT}; B-SCV2-06's recorded resolution must "
                        f"survive every successor in this chain")
            direction = d9.get("direction") or ""
            if "VERSIONING depends on D9" not in direction or \
                    "D9 does NOT depend on VERSIONING" not in direction:
                add(errors, "VER10-DEP",
                    "decisionDependencies[4].direction no longer declares the "
                    "one-way dependency direction (B-SCV2-06)")
            if "additive-only exit-class rule (V4)" not in direction:
                add(errors, "VER10-DEP",
                    "decisionDependencies[4].direction no longer names the "
                    "additive-only exit-class rule (V4) it rests on")

        # ---- review O-03: the labels that read "current candidate" ----
        for index in (5, 6):
            now, was = deps[index], pred_deps[index]
            if not isinstance(now, str) or not isinstance(was, str):
                add(errors, "VER10-LABEL",
                    f"decisionDependencies[{index}] is no longer a bare label "
                    f"string; changing its shape is a re-derivation, not a "
                    f"label correction")
                continue
            stem = was.split(STALE_LABEL_PHRASE)[0]
            if not now.startswith(stem):
                add(errors, "VER10-LABEL",
                    f"decisionDependencies[{index}] no longer carries the "
                    f"as-reviewed citation target {stem.split(' ')[0]!r}; "
                    f"retargeting re-derives the cold stored-read rejoin and is "
                    f"deferred as residual R-VER9-02, not performed here")
            if STALE_LABEL_PHRASE in now:
                add(errors, "VER10-LABEL",
                    f"decisionDependencies[{index}] still reads 'current "
                    f"candidate', which is false on its face (review O-03)")
            for token in LABEL_TOKENS:
                if token not in now:
                    add(errors, "VER10-LABEL",
                        f"decisionDependencies[{index}] does not carry the "
                        f"corrected label token {token!r}")

    # ---- the citation must equal the register's live binding ----
    register_path = HERE / REGISTER
    claims: list[Any] = []
    if not register_path.exists():
        add(errors, "VER10-REG",
            f"{REGISTER} is absent; the live D9 binding cannot be verified")
    else:
        try:
            claims = load(register_path)["claims"]
            live = next((c.get("bindingArtifact") for c in claims
                         if c.get("id") == "D9"), None)
        except Exception as exc:
            live = None
            add(errors, "VER10-REG",
                f"{REGISTER} unreadable: {type(exc).__name__}: {exc}")
        if live is None:
            add(errors, "VER10-REG", "the register declares no live D9 binding")
        elif isinstance(deps, list) and len(deps) > 4 and \
                isinstance(deps[4], dict) and deps[4].get("source") != live:
            add(errors, "VER10-REG",
                f"decisionDependencies[4] cites {deps[4].get('source')} but the "
                f"register binds D9 to {live} — a superseded citation "
                f"(B-SCV2-06)")

    # ---- B-SCV2-06's resolution text is fully protected from v10 onward ----
    b_scv2 = (value.get("resolves") or {}).get("B-SCV2-06") or ""
    if not b_scv2.startswith("RESOLVED"):
        add(errors, "VER10-RESOLVE",
            "resolves['B-SCV2-06'] is no longer recorded RESOLVED")
    if "live v1.6 artifact" in b_scv2:
        add(errors, "VER10-RESOLVE",
            "resolves['B-SCV2-06'] still asserts the superseded v1.6 citation")
    if D9_HEAD not in b_scv2:
        add(errors, "VER10-RESOLVE",
            "resolves['B-SCV2-06'] does not name the repaired head citation")

    # ---- limitation delta is additive and exact ----
    limitations = value.get("knownLimitations")
    pred_limitations = predecessor.get("knownLimitations", [])
    if not isinstance(limitations, list):
        add(errors, "VER10-LIMIT", "knownLimitations is not a list")
    elif limitations[:len(pred_limitations)] != pred_limitations:
        add(errors, "VER10-LIMIT",
            "inherited knownLimitations were altered or reordered")
    elif len(limitations) - len(pred_limitations) != ADDED_LIMITATION_COUNT:
        add(errors, "VER10-LIMIT",
            f"successor limitation delta is "
            f"{len(limitations) - len(pred_limitations)}, expected "
            f"{ADDED_LIMITATION_COUNT}")

    # ---- successor revision ----
    revision = value.get("successorRevision") or {}
    pred_revision = predecessor.get("successorRevision") or {}
    if set(revision) != EXPECTED_REVISION_KEYS:
        add(errors, "VER10-REV", "successor revision is not closed")
    if revision.get("id") != "VERSIONING-v10-EVIDENCE-ENFORCEMENT-SUCCESSOR" \
            or revision.get("candidateState") != "NOT-APPLIED":
        add(errors, "VER10-REV", "successor identity/state drift")
    if revision.get("supersedesCandidate") != {
            "artifact": PREDECESSOR,
            "sha256": PINS[PREDECESSOR],
            "checker": PREDECESSOR_CHECKER,
            "checkerSha256": PINS[PREDECESSOR_CHECKER]}:
        add(errors, "VER10-REV",
            "VERSIONING v9 protected predecessor pin drift")
    for key in ("inputs", "rawAuthorityKinds", "custodyRule",
                "storeAuthorityRule", "coldStoredReadRejoin",
                "dependencyLabelRule"):
        if canon(revision.get(key)) != canon(pred_revision.get(key)):
            add(errors, "VER10-REV",
                f"carried v9 successor contract changed: {key}")
    if revision.get("identityStability", {}).get("predecessor") != \
            "VERSIONING-v9" or \
            revision.get("identityStability", {}).get("state") != \
            "EXACT-CUSTODY-IDENTITIES-UNCHANGED":
        add(errors, "VER10-REV", "v9 identity stability statement drift")
    forbidden = revision.get("forbiddenBackEdge", "")
    if not all(term in forbidden for term in (
            "Evidence", "RunId", "TerminalRunV1", "RunAuthorityIndexV1",
            "ProjectStoreAuthority token", "store transaction token",
            "VERSIONING-v10")):
        add(errors, "VER10-REV",
            "forbidden downstream/store-token back-edge rule incomplete")
    if any("evidence" in canon(row).lower()
           for row in (revision.get("inputs") or {}).values()
           if isinstance(row, dict)):
        add(errors, "VER10-REV",
            "VERSIONING v10 contains an Evidence dependency back-edge")
    for message in no_floats(revision, "successorRevision"):
        add(errors, "VER10-FLOAT", message)

    # ---- the carried v9 repair record ----
    repair = revision.get("d9CitationRepair") or {}
    pred_repair = pred_revision.get("d9CitationRepair") or {}
    if set(repair) != EXPECTED_REPAIR_KEYS:
        add(errors, "VER10-REPAIR", "d9CitationRepair is not closed")
    moved = diff_leaves(repair, pred_repair)
    for path in sorted(set(moved) - ENUMERATED_DELTA):
        add(errors, "VER10-CARRY",
            f"{REPAIR}.{path} differs from the reviewed {PREDECESSOR} bytes and "
            f"is not in the enumerated delta; every measured quantity in the v9 "
            f"evidence record is carried byte-identical")
    for path in sorted(ENUMERATED_DELTA - set(moved)):
        add(errors, "VER10-DELTA",
            f"{REPAIR}.{path} is declared an enumerated v10 correction but is "
            f"byte-identical to {PREDECESSOR}")
    for name in FROZEN_SUB_BLOCKS:
        if canon(repair.get(name)) != canon(pred_repair.get(name)):
            add(errors, "VER10-CARRY",
                f"{REPAIR}.{name} is not byte-identical to {PREDECESSOR}; v10 "
                f"retunes no measured quantity the v9 review verified")
    frozen_ok = [n for n in FROZEN_SUB_BLOCKS
                 if canon(repair.get(n)) == canon(pred_repair.get(n))]

    citation = repair.get("citation") or {}
    if citation.get("was") != SUPERSEDED_CITATION or \
            citation.get("now") != REPAIRED_CITATION or \
            citation.get("nowSha256") != PINS[D9_HEAD]:
        add(errors, "VER10-REPAIR",
            "declared citation delta does not match the repair actually made")

    # ---- recording obligation: filename + sha256 for every input ----
    recorded = repair.get("recordedInputs")
    recorded_map = {row.get("artifact"): row for row in recorded
                    if isinstance(row, dict)} \
        if isinstance(recorded, list) else {}
    if not isinstance(recorded, list):
        add(errors, "VER10-RECORD",
            f"{REPAIR}.recordedInputs is not a list — a count is not a record")
    for name in (GRANDPARENT, GRANDPARENT_CHECKER, GRANDPARENT_REVIEW, D9_HEAD,
                 D9_HEAD_CHECKER, D9_HEAD_REVIEW, D9_SUPERSEDED, V4, V4_CHECKER):
        row = recorded_map.get(name)
        if row is None:
            add(errors, "VER10-RECORD",
                f"{REPAIR}.recordedInputs omits pinned input {name} — freeze "
                f"§7.2 requires filename + sha256 for every input")
        elif row.get("sha256") != PINS[name]:
            add(errors, "VER10-RECORD",
                f"{REPAIR}.recordedInputs sha256 for {name} does not match the "
                f"bytes on disk")
    register_row = recorded_map.get(REGISTER)
    if register_row is None:
        add(errors, "VER10-RECORD", f"{REPAIR}.recordedInputs omits {REGISTER}")
    elif not register_row.get("gate", "").startswith("RECORDED-NOT-PINNED"):
        add(errors, "VER10-RECORD",
            f"{REGISTER} must be recorded as RECORDED-NOT-PINNED with the "
            f"reason it is not byte-gated")

    # ---- V4 itself, measured from disk, independent of any declaration ----
    if measured["exitClassesRemoved"]:
        add(errors, "VER10-V4",
            f"V4 VIOLATED across the cited span: exit classes "
            f"{measured['exitClassesRemoved']} exist in {D9_SUPERSEDED} and not "
            f"in {D9_HEAD}. Exit classes are additive-only, forever.")
    if not measured["classToExitCodeByteIdentical"]:
        add(errors, "VER10-V4",
            f"V4 VIOLATED across the cited span: classToExitCode differs "
            f"between {D9_SUPERSEDED} and {D9_HEAD}. Renumbering silently "
            f"changes the meaning of every CI configuration in existence.")
    for label, key in (("exit class", "sharedExitClassMismatches"),
                       ("reason/error code", "sharedReasonOrErrorCodeMismatches"),
                       ("numeric exit code", "sharedNumericExitCodeMismatches")):
        if measured[key]:
            add(errors, "VER10-V4",
                f"V4 VIOLATED across the cited span: {measured[key]} shared "
                f"golden(s) changed {label} between {D9_SUPERSEDED} and "
                f"{D9_HEAD}.")
    if measured["removed"]:
        add(errors, "VER10-V4",
            f"goldens removed across the cited span: {measured['removed']} — "
            f"the contract is not additive")
    if measured["remediesRemoved"] or not measured["reasonCodesByteIdentical"] \
            or not measured["errorCodesByteIdentical"]:
        add(errors, "VER10-V4",
            "the closed reason/error code vocabulary is not byte-identical "
            "across the cited span")
    if measured["exitCodeValueSetV16"] != measured["exitCodeValueSetV114"]:
        add(errors, "VER10-V4",
            f"the distinct exit-code value set moved from "
            f"{measured['exitCodeValueSetV16']} to "
            f"{measured['exitCodeValueSetV114']} across the cited span")
    if measured["d9CitesVersioningPolicy"]:
        add(errors, "VER10-V4",
            f"{D9_HEAD} names a versioning-policy artifact — the declared "
            f"one-way direction (VERSIONING -> D9) may no longer hold "
            f"(B-SCV2-06)")
    if "v1.6" in head_review_text:
        add(errors, "VER10-SPAN",
            f"{D9_HEAD_REVIEW} now mentions v1.6; the artifact's stated reason "
            f"for measuring the span directly must be re-derived")

    # ---- the evidence-leaf partition: the answer to B-VER9R-01 ----
    audit = measure_audit(deps, claims)
    v8_d9 = v8_deps[4] if len(v8_deps) > 4 else {}
    d9_now = deps[4] if len(deps) > 4 and isinstance(deps[4], dict) else {}
    direction_preserved = all(
        canon(d9_now.get(field)) == canon(v8_d9.get(field))
        for field in ("id", "claim", "direction", "note"))
    reg = evidence_registry(value, deps, measured, audit, direction_preserved)
    extra = {"reviewText": review_text, "predecessorDeps": pred_deps}
    leaf_errors, partition = evaluate(value, reg, EVIDENCE_SCOPE, extra)
    errors.extend(leaf_errors)
    carry_covered = sum(
        1 for p in (partition["measuredLeaves"] + partition["groundedLeaves"] +
                    partition["unmeasurableLeaves"])
        if any(p.startswith(f"{REPAIR}.{name}") for name in frozen_ok))

    enforcement = revision.get("evidenceEnforcementRepair") or {}
    if set(enforcement) != EXPECTED_ENFORCEMENT_KEYS:
        add(errors, "VER10-REPAIR", "evidenceEnforcementRepair is not closed")
    reg2 = enforcement_registry(value, deps, measured, review_facts, partition,
                                sorted(moved), frozen_ok, carry_covered)
    new_errors, new_partition = evaluate(value, reg2, (ENFORCE,), extra)
    errors.extend(new_errors)

    # ---- the partition itself is a finding when it disagrees ----
    declared_partition = (enforcement.get("evidenceLeafEnforcement") or {}) \
        .get("partition") or {}
    for key, actual in (("MEASURED", partition["measured"]),
                        ("GROUNDED", partition["grounded"]),
                        ("UNMEASURABLE", partition["unmeasurable"]),
                        ("total", partition["total"])):
        got = declared_partition.get(key)
        if not exact_int(got) or got != actual:
            add(errors, "VER10-PART",
                f"declared evidence-leaf partition {key} is {got!r}; this "
                f"checker classified {actual} positions. B-VER9R-01: the "
                f"partition is itself evidence and is compared, not narrated")
    if exact_int(review_facts["enforced"]) and \
            exact_int(review_facts["unenforced"]) and \
            review_facts["enforced"] + review_facts["unenforced"] != \
            partition["probeSetSize"]:
        add(errors, "VER10-PART",
            f"the review's probe set was "
            f"{review_facts['enforced']} + {review_facts['unenforced']} = "
            f"{review_facts['enforced'] + review_facts['unenforced']} leaves, "
            f"but this artifact now declares {partition['probeSetSize']} "
            f"probeable leaves in the same scope; the partition and the review "
            f"no longer describe the same surface")

    # ---- residuals retained, not absorbed ----
    carried = repair.get("retainedResiduals")
    carried = carried if isinstance(carried, list) else []
    carried_ids = {r.get("id") for r in carried if isinstance(r, dict)}
    for missing in sorted(CARRIED_RESIDUAL_IDS - carried_ids):
        add(errors, "VER10-RESID",
            f"carried residual {missing} was dropped from {REPAIR}")
    for index, row in enumerate(carried):
        if not isinstance(row, dict):
            continue
        for field in ("residual", "measured", "disposition", "ownedBy"):
            if not row.get(field):
                add(errors, "VER10-RESID",
                    f"{REPAIR}.retainedResiduals[{index}].{field} is empty; "
                    f"residual {row.get('id')} records no {field}")
        if row.get("measured") and not re.search(r"\d", row["measured"]):
            add(errors, "VER10-RESID",
                f"{REPAIR}.retainedResiduals[{index}].measured states no "
                f"measured number — every residual states its own boundary as "
                f"a measured number")
    # The two restated residuals must carry the figures the review measured,
    # and both figures are re-derived here rather than accepted (review O-04,
    # O-09). R-VER9-05 understated the predecessor float admission by 13x.
    by_id = {row.get("id"): (index, row) for index, row in enumerate(carried)
             if isinstance(row, dict)}
    fixtures = len((grandparent.get("historicalSemanticsPolicy") or {})
                   .get("crossMajorFixtures") or [])
    if "R-VER9-05" in by_id and fixtures:
        index, row = by_id["R-VER9-05"]
        if str(fixtures) not in (row.get("measured") or ""):
            add(errors, "VER10-RESID",
                f"{REPAIR}.retainedResiduals[{index}].measured does not state "
                f"the measured figure {fixtures}: {GRANDPARENT} carries "
                f"{fixtures} crossMajorFixtures and the independent review "
                f"measured that ALL of them admit a float hostDefaultIrMajor "
                f"under {GRANDPARENT_CHECKER}, not only index [4] (review O-04)")
    if "R-VER9-07" in by_id:
        index, row = by_id["R-VER9-07"]
        drift = ((json.loads(review_text).get("verifiedInputs") or {})
                 .get("driftControl") or {}).get("driftDetectedInOtherFiles") \
            or []
        observed = [d.get(k) for d in drift if isinstance(d, dict)
                    for k in ("atReviewStart", "atReviewEnd") if d.get(k)]
        for digest in observed:
            if digest not in (row.get("measured") or ""):
                add(errors, "VER10-RESID",
                    f"{REPAIR}.retainedResiduals[{index}].measured omits the "
                    f"register digest {digest[:16]}… that the independent "
                    f"review observed; the third drift is the empirical "
                    f"vindication of gating this file semantically (review "
                    f"O-09)")
    residuals = enforcement.get("retainedResiduals")
    ids = {r.get("id") for r in residuals if isinstance(r, dict)} \
        if isinstance(residuals, list) else set()
    for missing in sorted(REQUIRED_RESIDUAL_IDS - ids):
        add(errors, "VER10-RESID", f"v10 residual {missing} was dropped")

    # ---- no paper seal ----
    if canon(value.get("dischargeStatus")) != canon(
            predecessor.get("dischargeStatus")):
        add(errors, "VER10-SEAL",
            "dischargeStatus moved; this successor discharges nothing")
    discharge = value.get("dischargeStatus") or {}
    if discharge.get("seal") != "DO-NOT-SEAL":
        add(errors, "VER10-SEAL", "dischargeStatus.seal inflation")
    if discharge.get("CD-RT-5") != "BLOCKED":
        add(errors, "VER10-SEAL",
            "dischargeStatus.CD-RT-5 moved; it remains BLOCKED_ON_PHASE_1A")
    if discharge.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED":
        add(errors, "VER10-SEAL",
            "dischargeStatus.evidenceGrade inflation — implementable is not "
            "DISCHARGED or DEMONSTRATED")

    LAST["partition"] = partition
    LAST["newPartition"] = new_partition
    LAST["carryCovered"] = carry_covered
    return errors


def boolean_sweep(value: Any) -> dict[str, Any]:
    """Measure the boolean direction of freeze §6 law 18 over this checker's own
    subject instead of asserting it. The v9 reviewer measured 15 of 139 boolean
    leaves admitting an integer respelling; here the number is re-derived on
    every --selftest run so the class cannot drift back open unnoticed. This
    runs from selftest, never from check(), so check() never recurses."""
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
        errors = check(candidate, verify_files=False)
        tail = path.split(".")[-1].split("[")[0]
        if not errors:
            admitted.append(path)
        elif not any(tail in e for e in errors):
            admitted.append(f"{path} (rejected only collaterally)")
    return {"total": total, "admitted": len(admitted), "admittedPaths": admitted}


# -------------------------------------------------------------- the selftest

def falsify(path: str, replacement: Any):
    return lambda c: set_at(c, path, replacement)


S_EV = f"{REPAIR}.substanceUnchangedEvidence"
D_EV = f"{REPAIR}.directionPreservation"
A_EV = f"{REPAIR}.siblingCitationAudit"
F_EV = f"{ENFORCE}.evidenceLeafEnforcement"

# (label, mutate, the finding id it must produce, the position it must name).
# A non-zero exit is not evidence a guard fired: both columns are asserted.
MUTATIONS: list[tuple[str, Any, str, str]] = [
    # ---- the three worst leaves named in blocker B-VER9R-01 ----
    ("replace the artifact's own recorded superseded-span digest with garbage",
     falsify(f"{S_EV}.measuredBetween.supersededCitationSha256", "0" * 64),
     "VER10-CARRY", "supersededCitationSha256"),
    ("replace the artifact's own recorded head digest with garbage",
     falsify(f"{S_EV}.measuredBetween.headSha256", "0" * 64),
     "VER10-CARRY", "headSha256"),
    ("falsify a byte-identical root the checker already computes",
     falsify(f"{S_EV}.byteIdenticalRootsV16ToV114[3]", "ADVERSARIAL-FALSEHOOD"),
     "VER10-CARRY", "byteIdenticalRootsV16ToV114[3]"),
    ("assert that D9 depends on VERSIONING — the exact B-SCV2-06 circularity "
     "this dependency record exists to refute",
     falsify(f"{D_EV}.reVerifiedAtHead.d9CitesVersioningInItsDependencies",
             True),
     "VER10-CARRY", "d9CitesVersioningInItsDependencies"),
    # ---- the rest of the leaves the predecessor computed and never compared --
    ("falsify an exit-class NAME list entry",
     falsify(f"{S_EV}.exitClassSet.v16[2]", "ADVERSARIAL-FALSEHOOD"),
     "VER10-CARRY", "exitClassSet.v16[2]"),
    ("falsify a code-vocabulary identity the checker already computes",
     falsify(f"{S_EV}.codeVocabulary.reasonCodesByteIdentical", False),
     "VER10-CARRY", "reasonCodesByteIdentical"),
    ("respell a code-vocabulary identity as the string 'true'",
     falsify(f"{S_EV}.codeVocabulary.errorCodesByteIdentical", "true"),
     "VER10-CARRY", "errorCodesByteIdentical"),
    ("falsify the remedy the span adds",
     falsify(f"{S_EV}.codeVocabulary.remediesAdded[0]", "ADVERSARIAL-FALSEHOOD"),
     "VER10-CARRY", "remediesAdded[0]"),
    ("falsify a sibling-audit file resolution",
     falsify(f"{A_EV}.entries[0].fileResolves", False),
     "VER10-CARRY", "entries[0].fileResolves"),
    ("falsify a sibling-audit anchor resolution",
     falsify(f"{A_EV}.entries[2].anchorResolves", False),
     "VER10-CARRY", "entries[2].anchorResolves"),
    ("falsify the sibling-audit register binding for D9",
     falsify(f"{A_EV}.entries[4].registerBinding", SUPERSEDED_CITATION),
     "VER10-CARRY", "entries[4].registerBinding"),
    ("falsify the sibling-audit register binding for retention-tiers",
     falsify(f"{A_EV}.entries[6].registerBinding", None),
     "VER10-CARRY", "entries[6].registerBinding"),
    ("falsify a sibling-audit source so the audit disagrees with the "
     "dependency it audits",
     falsify(f"{A_EV}.entries[3].source", "architecture/99-nonexistent.md#x"),
     "VER10-CARRY", "entries[3].source"),
    # ---- freeze §6 law 18, BOTH directions ----
    ("respell version as a float (law 18)",
     falsify("version", 10.0), "VER10-ID", "version"),
    ("respell supersedes as a float (law 18)",
     falsify("supersedes", 9.0), "VER10-ID", "supersedes"),
    ("respell version as a bool (law 18)",
     falsify("version", True), "VER10-ID", "version"),
    ("respell a measured golden count as a float (law 18)",
     falsify(f"{S_EV}.goldenCases.shared", 44.0),
     "VER10-FLOAT", "goldenCases.shared"),
    ("respell an exit code as a float (law 18)",
     falsify(f"{S_EV}.classToExitCode.success", 0.0),
     "VER10-FLOAT", "classToExitCode.success"),
    ("respell a protected historical IR major as a float (law 18)",
     falsify("historicalSemanticsPolicy.crossMajorFixtures[4]."
             "hostDefaultIrMajor", 4.0),
     "VER10-SURFACE", "historicalSemanticsPolicy"),
    ("respell a declared evidence BOOLEAN as an integer — the direction v9 "
     "left open (law 18)",
     falsify(f"{S_EV}.exitClassSet.identical", 1),
     "VER10-CARRY", "exitClassSet.identical"),
    ("respell a second declared evidence boolean as an integer",
     falsify(f"{S_EV}.classToExitCodeByteIdentical", 1),
     "VER10-CARRY", "classToExitCodeByteIdentical"),
    ("respell a direction-preservation boolean as an integer",
     falsify(f"{D_EV}.preservedByteIdentical", 1),
     "VER10-CARRY", "preservedByteIdentical"),
    ("respell a sibling-audit boolean as an integer",
     falsify(f"{A_EV}.entries[1].fileResolves", 1),
     "VER10-CARRY", "entries[1].fileResolves"),
    ("respell a new-block boolean as an integer",
     falsify(f"{ENFORCE}.checkerDisposition."
             "checkerEnforcesEveryDeclaredEvidenceLeaf", 1),
     "VER10-LEAFTYPE", "checkerEnforcesEveryDeclaredEvidenceLeaf"),
    ("respell a partition count as a bool",
     falsify(f"{F_EV}.partition.UNMEASURABLE", False),
     "VER10-PART", "UNMEASURABLE"),
    # ---- the enforcement partition itself ----
    ("understate the number of measured leaves",
     falsify(f"{F_EV}.partition.MEASURED", 3), "VER10-PART", "MEASURED"),
    ("overstate the total number of leaf positions",
     falsify(f"{F_EV}.partition.total", 999), "VER10-PART", "total"),
    ("silently drop a leaf from the declared measured table",
     lambda c: at(c, f"{F_EV}.measuredLeaves").pop(0),
     "VER10-LEAF", "measuredLeaves"),
    ("misreport what the predecessor checker enforced",
     falsify(f"{F_EV}.predecessor.unenforced", 0),
     "VER10-LEAF", "predecessor.unenforced"),
    ("delete a declared evidence leaf",
     lambda c: at(c, f"{S_EV}.measuredBetween").pop("head"),
     "VER10-CARRY", "measuredBetween.head"),
    ("add an unclassified evidence leaf",
     lambda c: at(c, f"{S_EV}.measuredBetween").__setitem__("extra", "x"),
     "VER10-COVER", "measuredBetween.extra"),
    # ---- review O-03, the label correction ----
    ("restore the false 'current candidate' label on the EP dependency",
     falsify("decisionDependencies[5]",
             "evaluation-proof.v8.json (durable cold stored-read authority "
             "reconstruction; current candidate)"),
     "VER10-LABEL", "decisionDependencies[5]"),
    ("restore the false 'current candidate' label on the RT dependency",
     falsify("decisionDependencies[6]",
             "retention-tiers.v13.json (cold-reconstruction custody identity "
             "rejoin; current candidate)"),
     "VER10-LABEL", "decisionDependencies[6]"),
    ("silently RETARGET the EP dependency instead of relabelling it",
     falsify("decisionDependencies[5]",
             "evaluation-proof.v13.json (durable cold stored-read authority "
             "reconstruction; AS-REVIEWED PIN, NOT THE CURRENT CANDIDATE; "
             "R-VER9-02)"),
     "VER10-LABEL", "decisionDependencies[5]"),
    ("silently RETARGET the RT dependency to the register-bound head",
     falsify("decisionDependencies[6]",
             "retention-tiers.v22.json (cold-reconstruction custody identity "
             "rejoin; AS-REVIEWED PIN, NOT THE CURRENT CANDIDATE; R-VER9-02)"),
     "VER10-LABEL", "decisionDependencies[6]"),
    # ---- the carried v9 record ----
    ("retune a measured golden count in the carried v9 evidence",
     falsify(f"{S_EV}.goldenCases.shared", 40),
     "VER10-CARRY", "goldenCases.shared"),
    ("rewrite the carried v9 conclusion prose",
     falsify(f"{S_EV}.conclusion", "Everything is fine."),
     "VER10-CARRY", "conclusion"),
    ("claim the head review covers the v1.6 span",
     falsify(f"{S_EV}.whyNotInheritedFromTheHeadReview",
             "Inherited from the head review."),
     "VER10-CARRY", "whyNotInheritedFromTheHeadReview"),
    ("absorb the R-VER9-05 restatement entirely",
     falsify(f"{REPAIR}.retainedResiduals[4].measured", ""),
     "VER10-RESID", "retainedResiduals[4].measured"),
    ("revert R-VER9-05 to the understated single-fixture figure (review O-04)",
     falsify(f"{REPAIR}.retainedResiduals[4].measured",
             "corpus-float-admission-sweep.v1.json records "
             "check-versioning-v8.py admitting one float at "
             "crossMajorFixtures[4].hostDefaultIrMajor."),
     "VER10-RESID", "retainedResiduals[4].measured"),
    ("drop the third register drift from R-VER9-07 (review O-09)",
     falsify(f"{REPAIR}.retainedResiduals[5].measured",
             "claim-register.v1.json was observed at 2 digests and the D9 "
             "binding was stable across both."),
     "VER10-RESID", "retainedResiduals[5].measured"),
    ("point the successor checker at the predecessor",
     falsify(f"{REPAIR}.checkerDisposition.checker", PREDECESSOR_CHECKER),
     "VER10-DELTA", "checkerDisposition.checker"),
    # ---- span disclosure, review O-01 / O-02 ----
    ("deny that the request-rejected class meaning broadened",
     falsify(f"{ENFORCE}.spanDisclosure.exitClassMeaningBroadened[0]",
             "success"),
     "VER10-LEAF", "exitClassMeaningBroadened[0]"),
    ("deny that hostTerminationUnion moved across the span",
     falsify(f"{ENFORCE}.spanDisclosure.hostTerminationUnionChanged", False),
     "VER10-LEAF", "hostTerminationUnionChanged"),
    ("falsify the new cross-axis invariant id",
     falsify(f"{ENFORCE}.spanDisclosure.crossAxisInvariantsAdded[0]", "X99"),
     "VER10-LEAF", "crossAxisInvariantsAdded[0]"),
    ("falsify the distinct exit-code value set",
     falsify(f"{ENFORCE}.spanDisclosure.exitCodeValueSetV114[5]", 131),
     "VER10-LEAF", "exitCodeValueSetV114[5]"),
    ("claim the details bag carries exit-code authority",
     falsify(f"{ENFORCE}.spanDisclosure.detailsControlFlowUse", "PERMITTED"),
     "VER10-LEAF", "detailsControlFlowUse"),
    # ---- the review of record ----
    ("misquote the independent reviewer",
     falsify(f"{ENFORCE}.reviewOfRecord.reviewerStatement",
             "The reviewer found nothing wrong with the checker."),
     "VER10-LEAF", "reviewerStatement"),
    ("understate the review's blocking finding count",
     falsify(f"{ENFORCE}.reviewOfRecord.blockingFindingCount", 0),
     "VER10-LEAF", "blockingFindingCount"),
    ("claim the blocker was against the contract, not the checker",
     falsify(f"{ENFORCE}.reviewOfRecord.blockerIsAgainst", PREDECESSOR),
     "VER10-LEAF", "blockerIsAgainst"),
    ("record a wrong digest for the review of record",
     falsify(f"{ENFORCE}.reviewOfRecord.sha256", "0" * 64),
     "VER10-LEAF", "reviewOfRecord.sha256"),
    # ---- law 18 disclosure ----
    ("misreport the predecessor's admitted boolean respellings",
     falsify(f"{ENFORCE}.closedScalarAdmission.booleanDirection."
             "boolToIntAdmittedInV9", 0),
     "VER10-LEAF", "boolToIntAdmittedInV9"),
    ("misreport the predecessor's integer-leaf population",
     falsify(f"{ENFORCE}.closedScalarAdmission.integerDirection."
             "integerLeavesInV9", 1),
     "VER10-LEAF", "integerLeavesInV9"),
    ("respell the swept boolean count as a float",
     falsify(f"{ENFORCE}.closedScalarAdmission.booleanDirection."
             "boolToIntAdmittedInV10", 0.0),
     "VER10-LEAFTYPE", "boolToIntAdmittedInV10"),
    # ---- status, seal and residual discipline ----
    ("advance the review status as if a verdict transferred",
     falsify("reviewStatus", "PASSED"), "VER10-STATUS", "reviewStatus"),
    ("advance the candidate status", falsify("status", "APPLIED"),
     "VER10-STATUS", "status"),
    ("seal on a paper claim", falsify("dischargeStatus.seal", "SEAL"),
     "VER10-SEAL", "seal"),
    ("unblock CD-RT-5", falsify("dischargeStatus.CD-RT-5", "DISCHARGED"),
     "VER10-SEAL", "CD-RT-5"),
    ("inflate the evidence grade",
     falsify("dischargeStatus.evidenceGrade", "DEMONSTRATED"),
     "VER10-SEAL", "evidenceGrade"),
    ("drop a carried v9 residual",
     lambda c: at(c, f"{REPAIR}.retainedResiduals").pop(1),
     "VER10-RESID", "R-VER9-02"),
    ("drop a v10 residual",
     lambda c: at(c, f"{ENFORCE}.retainedResiduals").pop(0),
     "VER10-RESID", "R-VER10-01"),
    ("state a v10 residual with no measured boundary",
     falsify(f"{ENFORCE}.retainedResiduals[0].measured", "It is fine."),
     "VER10-RESID", "retainedResiduals[0].measured"),
    ("assign a v10 residual to an owner outside the closed vocabulary",
     falsify(f"{ENFORCE}.retainedResiduals[0].ownedBy", "nobody"),
     "VER10-LEAF", "retainedResiduals[0].ownedBy"),
    # ---- protected surface, back-edges and the carried contract ----
    ("change a protected v9 section",
     falsify("custodyClasses[0].class", "INTERNAL"),
     "VER10-SURFACE", "custodyClasses"),
    ("relax the GUESSED support-window seal rule",
     falsify("supportWindows.sealRule", "Windows may be sealed on a guess."),
     "VER10-SURFACE", "supportWindows"),
    ("drop the run-manifest NOT-YET-ENFORCEABLE restriction",
     falsify("implementationBacklog[0].status", "ENFORCEABLE"),
     "VER10-SURFACE", "implementationBacklog"),
    ("leave the B-SCV2-06 resolution asserting the stale v1.6 citation",
     falsify("resolves.B-SCV2-06",
             "RESOLVED — the D9 citation retargets to the live v1.6 artifact "
             "and VERSIONING depends on D9, not the reverse."),
     "VER10-SURFACE", "resolves"),
    ("revert the D9 citation to the superseded v1.6 artifact",
     falsify("decisionDependencies[4].source", SUPERSEDED_CITATION),
     "VER10-DEP", "decisionDependencies[4]"),
    ("rewrite the direction so ownership becomes circular (B-SCV2-06)",
     falsify("decisionDependencies[4].direction", "D9 depends on VERSIONING."),
     "VER10-DEP", "decisionDependencies[4].direction"),
    ("carry the EP8/RT13 cold rejoin away",
     falsify("successorRevision.coldStoredReadRejoin.rule",
             "Warm cache is authority."),
     "VER10-REV", "coldStoredReadRejoin"),
    ("silently retarget the carried EP/RT dependency pins",
     falsify("successorRevision.inputs.retentionCustody.artifact",
             "retention-tiers.v22.json"),
     "VER10-REV", "inputs"),
    ("introduce an Evidence back-edge",
     lambda c: c["successorRevision"]["inputs"].__setitem__(
         "evidence", {"artifact": "evidence.v10.json"}),
     "VER10-REV", "Evidence"),
    ("alter an inherited limitation",
     falsify("knownLimitations[0]", "No limitations."),
     "VER10-LIMIT", "knownLimitations"),
    ("drop the successor limitation delta",
     lambda c: c.__setitem__("knownLimitations", c["knownLimitations"][:20]),
     "VER10-LIMIT", "limitation delta"),
    ("open the successor revision key surface",
     lambda c: c["successorRevision"].__setitem__("extra", 1),
     "VER10-REV", "successor revision"),
    ("open the enforcement record key surface",
     lambda c: at(c, ENFORCE).__setitem__("extra", 1),
     "VER10-REPAIR", "evidenceEnforcementRepair"),
    ("drop the predecessor pin",
     falsify("successorRevision.supersedesCandidate.sha256", "0" * 64),
     "VER10-REV", "predecessor pin"),
    ("record an input with a wrong digest",
     falsify(f"{REPAIR}.recordedInputs[3].sha256", "0" * 64),
     "VER10-CARRY", "recordedInputs[3].sha256"),
    ("byte-pin the coordinator-owned register",
     lambda c: [row for row in at(c, f"{REPAIR}.recordedInputs")
                if row["artifact"] == REGISTER][0].pop("gate"),
     "VER10-CARRY", "gate"),
    ("record a v10 input with a wrong digest",
     falsify(f"{ENFORCE}.recordedInputs[0].sha256", "0" * 64),
     "VER10-RECORD", "recordedInputs[0].sha256"),
]


def selftest(value: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    floats = sum(1 for label, _, _, _ in MUTATIONS if "float" in label)
    bools = sum(1 for label, _, _, _ in MUTATIONS
                if "bool" in label or "BOOLEAN" in label)
    for label, mutate, code, names in MUTATIONS:
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
        errors = check(candidate, verify_files=False)
        if not errors:
            failures.append(f"{label}: ESCAPED — no finding at all")
            continue
        # A non-zero exit is not evidence a guard fired: require the SPECIFIC
        # finding id AND that it names the position under test.
        if not [e for e in errors if e.startswith(f"{code}:") and names in e]:
            failures.append(
                f"{label}: rejected, but not by {code} naming {names!r} — "
                f"first finding was {errors[0][:120]!r}")

    sweep = boolean_sweep(value)
    declared = (((value.get("successorRevision") or {})
                 .get("evidenceEnforcementRepair") or {})
                .get("closedScalarAdmission") or {}).get("booleanDirection") or {}
    if declared.get("booleanLeavesSweptInV10") != sweep["total"]:
        failures.append(
            f"closedScalarAdmission.booleanDirection.booleanLeavesSweptInV10 "
            f"declares {declared.get('booleanLeavesSweptInV10')!r}; this sweep "
            f"found {sweep['total']} boolean leaves in successorRevision")
    if declared.get("boolToIntAdmittedInV10") != sweep["admitted"]:
        failures.append(
            f"closedScalarAdmission.booleanDirection.boolToIntAdmittedInV10 "
            f"declares {declared.get('boolToIntAdmittedInV10')!r}; this sweep "
            f"measured {sweep['admitted']} admitted: {sweep['admittedPaths'][:5]}")
    if sweep["admitted"]:
        failures.append(
            f"freeze §6 law 18 is not closed in the boolean direction: "
            f"{sweep['admitted']} of {sweep['total']} boolean leaves in "
            f"successorRevision admit an integer respelling or are rejected "
            f"only collaterally — {sweep['admittedPaths'][:5]}")

    return failures, {"total": len(MUTATIONS), "floats": floats, "bools": bools,
                      "sweep": sweep}


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
            # A dirty base masks every mutation, so the suite must not run and
            # must say so with an exit distinct from green, findings and misuse.
            print("SELFTEST-REFUSED: the base contract has findings, so every "
                  "mutation would be masked by them")
            print("SELFTEST-NOT-RUN")
            return 3
        return 1

    partition = LAST["partition"]
    new_partition = LAST["newPartition"]

    if wants_selftest:
        failures, stats = selftest(value)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print(f"PASS: {path.name}; {stats['total']} successor mutations "
              f"rejected, each by its specific finding id AND naming the "
              f"position under test; {stats['floats']} float respellings and "
              f"{stats['bools']} boolean respellings (freeze §6 law 18, both "
              f"directions)")
        print(f"  boolean-direction sweep re-derived on this run: "
              f"{stats['sweep']['total']} boolean leaves in successorRevision, "
              f"{stats['sweep']['admitted']} admitting an integer respelling or "
              f"rejected only collaterally")
        return 0

    print(f"PASS: {path.name}; D9 citation carried at the register-bound head "
          f"{D9_HEAD}; the v9 evidence record is byte-identical and every "
          f"measured quantity in it is re-derived from disk, not trusted")
    print(f"  evidence-leaf partition (B-VER9R-01): {partition['total']} leaf "
          f"positions across {len(EVIDENCE_SCOPE)} declared sub-blocks "
          f"({partition['probeSetSize']} in the review's probe set) — "
          f"{partition['measured']} MEASURED, {partition['grounded']} GROUNDED, "
          f"{partition['unmeasurable']} UNMEASURABLE; "
          f"{LAST['carryCovered']} additionally byte-gated against "
          f"{PREDECESSOR}")
    print(f"  v10 enforcement record: {new_partition['total']} leaf positions — "
          f"{new_partition['measured']} MEASURED, {new_partition['grounded']} "
          f"GROUNDED, {new_partition['unmeasurable']} UNMEASURABLE")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED; no seal, freeze, "
          "status advance or product acceptance is declared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
