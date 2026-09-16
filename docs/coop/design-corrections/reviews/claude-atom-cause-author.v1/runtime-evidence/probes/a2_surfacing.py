"""Does the nondeterministic fold SURFACE as a differing proof cause?

Primary clones partition is `unknown` with no carrier, so sufficiency fails and `coverage-unknown`
is emitted; its nativeCause comes from run_suff's scan of the view, whose dep entry is the
nondeterministic fold. AUTHOR/REFERENCE evidence only.
"""
import importlib.util
import json
import os
from pathlib import Path

F = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source/"
         "docs/coop/design-corrections/foundation")


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


A = load("atom_surf", F / "atom_model.v1.py")

SU = TU = "a" * 64
CLONES = "c" * 64
DEP_A, DEP_B = "1" * 64, "2" * 64


def rc(exh):
    return {"state": "not-applicable", "attempted": False, "examinedExhaustive": exh,
            "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}


def cov(relation, resolution, deficiency, nc, coverage, commitment, exh=True):
    return {"key": {"relation": relation, "resolution": resolution, "sourceUniverse": SU,
                    "targetUniverse": TU, "subjectScopeCommitment": commitment},
            "entry": {"coverage": coverage, "deficiency": deficiency, "nativeCause": nc,
                      "confidenceMillionths": 1000000, "resolutionCompleteness": rc(exh),
                      "derivationKinds": [], "rungUnavailableBecause": ""}}


CLONE_COMMIT = "sha256:" + "c" * 64
coverages = {}
for cid in {DEP_A, DEP_B, CLONES}:            # set iteration, as reconstruct does
    if cid == CLONES:
        # unknown primary -> sufficiency cannot be satisfied -> coverage-unknown is emitted
        coverages[cid] = cov("clones", "normalized-body-hash", None, None, "unknown",
                             CLONE_COMMIT, exh=False)
    elif cid == DEP_A:
        coverages[cid] = cov("declares", "syntactic", "budget-exhausted", None, "unknown",
                             "sha256:" + "1" * 64)
    else:
        coverages[cid] = cov("declares", "syntactic", "input-closure-incomplete",
                             "lockfile-missing", "unknown", "sha256:" + "2" * 64)

scopes = {"scope2:" + "c" * 64: {"relation": "clones", "resolution": "normalized-body-hash",
                                 "sourceUniverse": SU, "targetUniverse": TU,
                                 "subjects": ["src/a.ts"], "schemaVersion": 2,
                                 "snapshotId": "snapshot2:" + "0" * 64,
                                 "enumeratorClosure": "closure2:" + "0" * 64}}

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
    "universeDomains": {SU: "syntax"}, "closures": {}, "evaluationInputRefs": [],
    "planSelectedImportIds": [], "imports": {}, "importPayloads": {}, "importObservations": {},
    "targetAttributions": {}, "incomingSearchAttestations": [], "importScopes": {},
    "importFlagsAdapter": {}, "coverageScopes": {CLONES: "scope2:" + "c" * 64}, "blobs": {},
}

res = A.evaluate_atom({"op": "none", "relation": "clones",
                       "minResolution": "normalized-body-hash", "filters": []},
                      {"universe": SU, "kind": "file", "nativeSubjectId": "src/a.ts"}, inputs)
causes = [{"code": c.get("code"), "nativeCause": c.get("nativeCause")}
          for c in res.get("causes") or []]
print(json.dumps({
    "pid": os.getpid(),
    "coverageDictOrder": list(coverages),
    "value": res.get("value"),
    "causeCodes": sorted(c["code"] for c in causes),
    "coverageUnknownNativeCause": next(
        (c["nativeCause"] for c in causes if c["code"] == "coverage-unknown"), "ABSENT"),
    "nativeDeficiencies": sorted(res.get("nativeDeficiencies") or []),
    "coverageIds": sorted(res.get("coverageIds") or []),
}, indent=2, default=str))
