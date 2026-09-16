"""Does the DEPENDS_ON fold's carrier depend on Python dict/set iteration order?

Two controlled `declares@syntactic` dep partitions at the same (S,T), carrying DIFFERENT non-null
deficiencies. `_conservative_entry` takes the FIRST entry with a non-null deficiency in `covs`
order, and `covs` order is `_coverages_exact`'s iteration of `inputs['coverages']`.

`evaluator_input_model.v3.py:161-163` builds that dict by iterating a Python SET of ids, and `-I`
ignores PYTHONHASHSEED, so the seed differs per process. Running this repeatedly samples that.

AUTHOR/REFERENCE evidence only. No consumer code or expected output is used.
"""
import importlib.util
import json
import sys
from pathlib import Path

F = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source/"
         "docs/coop/design-corrections/foundation")


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


A = load("atom_under_test", F / "atom_model.v1.py")

SU = "a" * 64          # source universe
TU = "a" * 64          # target universe
CLONES = "c" * 64
DEP_A = "1" * 64       # declares partition A
DEP_B = "2" * 64       # declares partition B


def rc(state="not-applicable", exhaustive=True):
    return {"state": state, "attempted": False, "examinedExhaustive": exhaustive,
            "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}


def cov(relation, resolution, deficiency, native_cause, coverage="unknown", subjects=None):
    return {
        "key": {"relation": relation, "resolution": resolution,
                "sourceUniverse": SU, "targetUniverse": TU,
                "subjectScopeCommitment": "sha256:" + relation[:8].ljust(8, "0") * 8},
        "entry": {"coverage": coverage, "deficiency": deficiency, "nativeCause": native_cause,
                  "confidenceMillionths": 1000000, "resolutionCompleteness": rc(),
                  "derivationKinds": [], "rungUnavailableBecause": ""},
    }


def scope(relation, resolution, subjects):
    return {"relation": relation, "resolution": resolution, "sourceUniverse": SU,
            "targetUniverse": TU, "subjects": list(subjects), "schemaVersion": 2,
            "snapshotId": "snapshot2:" + "0" * 64, "enumeratorClosure": "closure2:" + "0" * 64}


# Insertion order is varied by the caller through a set, mimicking reconstruct's set comprehension.
ids = {DEP_A, DEP_B, CLONES}
coverages = {}
for cid in ids:                      # <- set iteration, exactly as reconstruct does
    if cid == CLONES:
        coverages[cid] = cov("clones", "normalized-body-hash", None, None, coverage="complete",
                             subjects=["src/a.ts"])
    elif cid == DEP_A:
        coverages[cid] = cov("declares", "syntactic", "budget-exhausted", None)
    else:
        coverages[cid] = cov("declares", "syntactic", "input-closure-incomplete",
                             "lockfile-missing")

scopes = {"scope2:" + "c" * 64: scope("clones", "normalized-body-hash", ["src/a.ts"])}

inputs = {
    "planId": "plan2:" + "0" * 64,
    "enumerationPlan": {"cells": [{
        "capabilityId": "clones-fact", "languageMode": "syntax-only", "workspaceRoot": ".",
        "required": True, "kinds": ["file"],
        "programBindings": [{"ordinal": 0, "provenance": "default-unit",
                             "enumerator": {"status": "selected",
                                            "closureId": "closure2:" + "0" * 64},
                             "nativeContextDigest": "b" * 64, "universe": SU,
                             "programEntry": None, "extents": []}]}]},
    "inventories": [], "facts": {}, "scopes": scopes, "coverages": coverages,
    "universeDomains": {SU: "syntax"}, "closures": {},
    "evaluationInputRefs": [], "planSelectedImportIds": [], "imports": {},
    "importPayloads": {}, "importObservations": {}, "targetAttributions": {},
    "incomingSearchAttestations": [], "importScopes": {}, "importFlagsAdapter": {},
    "coverageScopes": {CLONES: "scope2:" + "c" * 64},
    "blobs": {},
}

subject = {"universe": SU, "kind": "file", "nativeSubjectId": "src/a.ts"}
atom = {"op": "none", "relation": "clones", "minResolution": "normalized-body-hash",
        "filters": []}

out = {
    "pid": None,
    "hashRandomizationObservable": hash("src/a.ts"),
    "coverageDictOrder": list(coverages),
    "depCoverageOrderAsSeenByHelper": [
        cid for cid, _ in A._coverages_exact(inputs, "declares", "syntactic", SU, TU)],
}
try:
    res = A.evaluate_atom(atom, subject, inputs)
    causes = [{"code": c.get("code"), "nativeCause": c.get("nativeCause"),
               "universe": (c.get("universe") or "")[:6] or None} for c in res.get("causes") or []]
    out["value"] = res.get("value")
    out["causes"] = causes
    out["nativeDeficiencies"] = res.get("nativeDeficiencies")
    out["coverageIds"] = sorted(res.get("coverageIds") or [])
    out["coverageUnknownNativeCause"] = next(
        (c["nativeCause"] for c in causes if c["code"] == "coverage-unknown"), "NO-COVERAGE-UNKNOWN")
except Exception as exc:  # noqa: BLE001
    out["error"] = f"{type(exc).__name__}: {exc}"

# Also fold directly, so the mechanism is visible even if the atom path short-circuits.
covs = A._coverages_exact(inputs, "declares", "syntactic", SU, TU)
entry, cited = A._conservative_entry("declares", covs)
out["directFold"] = {"covsOrder": [c for c, _ in covs],
                     "foldedDeficiency": entry.get("deficiency"),
                     "foldedNativeCause": entry.get("nativeCause"),
                     "cited": cited}
import os
out["pid"] = os.getpid()
print(json.dumps(out, indent=2, default=str))
sys.exit(0)
