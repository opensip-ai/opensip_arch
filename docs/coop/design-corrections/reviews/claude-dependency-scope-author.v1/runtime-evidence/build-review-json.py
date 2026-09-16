"""Assemble review.json from the retained receipts. Counts are read back, never retyped."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE / "probes" / "receipts"
REV35 = Path("/tmp/opensip-design-corrections/claude-independent-design.v35")


def js(label):
    return json.loads((R / label / "stdout.txt").read_text())


before, after = json.loads((HERE / "before-hashes.json").read_text()), json.loads((HERE / "after-hashes.json").read_text())
q1o, q1n = js("q1-fallback-reach-frozen35"), js("q1-fallback-reach-successor")
q2 = js("q2-native-producer")
q3o, q3n = js("q3-shapes-frozen35.2"), js("q3-shapes-successor")
q4, q5, q6 = js("q4-controls-discriminate"), js("q5-consumers"), js("q6-custody-delta-pins")
atoms, atoms_model_only = js("check-atoms-successor"), js("check-atoms-model-only")
rev35_raw = (REV35 / "review.json").read_bytes()
rev35 = json.loads(rev35_raw)
a13 = [a for a in rev35["advisories"] if a.get("id") == "A-13"][0]


def v(x):
    return x.get("value") if "value" in x else "REFUSE:" + str(x.get("key"))


mutations = {label: {ep: {"frozen35": v(q3o["mutations"][label][ep]), "successor": v(q3n["mutations"][label][ep]),
                          "successorCitesDependency": "coverage2:" + "2" * 64 in (q3n["mutations"][label][ep].get("coverageIds") or [])}
                     for ep in q3n["mutations"][label]}
             for label in q3n["mutations"]}
commands = []
for d in sorted(R.iterdir()):
    if (d / "command.json").exists() and (d / "exit.txt").exists():
        commands.append({"label": d.name, "argv": json.loads((d / "command.json").read_text())["argv"],
                         "exit": int((d / "exit.txt").read_text())})

doc = {
    "review": "source-author correction of the _select_dep_coverages mapped fallback in dependency-scope-successor.v1",
    "authorOrigin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "standing": "AUTHORSHIP ONLY. Coauthor, never acceptor. Architecture/design/reference. No independent, blind or "
                "application acceptance, readiness, activation, implementation, product qualification, commit or push.",
    "inputs": {
        "frozen35Manifest": {"sha256": q6["manifestSha256"], "matchesDeclared": before["manifestShaMatchesDeclared"]},
        "copyVerification": "/tmp/opensip-design-corrections/root-source36-preparation.v1/copy-verification.json (read before mutation)",
        "rootInvestigation": "/tmp/opensip-design-corrections/root-dependency-scope35-investigation.v1/{assessment.md,probe.py,probe.json}",
        "treatment": "root findings treated as evidence; no consumer, root-blind or package expected-result input",
    },
    "authorshipOfBeforeBytes": q6["rootLayerAfterIncomingBindingV1"],
    "decision": {
        "finding": "SUBSTANTIATED as a reference defect at the synthetic atom API; the reference was looser than published section 4.",
        "correction": "REMOVE the mapped-scope fallback. Same kind, only _scopes_exact scopes at exact (dependency relation, rung, S) "
                      "containing the current subjects pair, by mapping or commitment.",
        "whyNotCarrierValidation": "would still let a valid but wrong-coordinate scope supply the dependency",
        "whyNotConstrain": "a fallback constrained to exact coordinates is identical to the main path (dead code): every exact scope is already selected",
        "refusalVersusIgnore": "non-exact scope ignored as absent (equal to deleting it); a selected exact scope failing its carrier refuses ATOM_NATIVE_CARRIER",
        "preserved": ["I1 and shared prelude", "three cause channels", "known-match and count-bound dominance", "exact-rung selection",
                      "mapping-or-commitment pairing", "ascending dedup and whole-record folds", "different-kind whole-source",
                      "attestation whole-source views", "dependency traversal", "all admission laws"],
        "normativeClarification": "section 4 dependency sentence made explicit (exact selection, no mapped fallback, ignored-vs-refused, every depth); section 9 cases",
    },
    "applicability": {
        "atomApi": {"standing": "synthetic atom-api", "mutations": mutations,
                    "deletedDependencyScope": {ep: [v(q3o["deletedDependencyScope"][ep]), v(q3n["deletedDependencyScope"][ep])]
                                               for ep in q3n["deletedDependencyScope"]},
                    "syntheticDepth2": {k: [v(q3o["syntheticDepth2"][k]), v(q3n["syntheticDepth2"][k])] for k in q3n["syntheticDepth2"]}},
        "nativeProducer": {"standing": "admit_coverage_result_v3 + direct carrier, frozen35", "rows": q2["rows"]},
        "closedRunReadLevel": ["identity-model.v3.py:1598-1603 every view scope admitted as subject-scope",
                               "identity-model.v3.py:1654-1678 COVERAGE_SCOPE_JOIN and admit_coverage_result_v3 over the retained scope",
                               "native_evidence_model.v2.py:1544-1550 key coordinates and commitment joined to the scope",
                               "evaluator_input_model.v3.py:161-163,193 all view scopes copied; coverageScopes from envelope scopeId"],
        "conclusion": "unreachable for inputs reconstructed from an admitted Run (producer measured, closure read); no closed enumeration, "
                      "closed Run or retained Run constructed; no full-Run counterexample claimed",
    },
    "independentReviewV35": {
        "processCompletion": json.loads((REV35 / "process-completion.json").read_text()),
        "reviewJsonSha256": hashlib.sha256(rev35_raw).hexdigest(),
        "verdict": rev35["verdict"], "verdictScope": rev35["verdictScope"],
        "A13": a13,
        "accounting": {
            "sameDefect": True,
            "healedCasesCoveredByControls": a13["healedCases"],
            "healedOnSuccessor": 0,
            "differenceWithMyMeasurement": "my Q3 and root's probe also heal relation null, resolution null and out-of-ladder resolved-binding "
                                           "on frozen35; A-13 does not list them; all are unknown on the successor; reviewer harness not investigated",
            "carrierSentence": "after correction a non-exact scope is not consumed; the answer equals the scope-deleted answer",
            "disposition": "reviewer v35 accepted frozen35, not these successor bytes; A-13 disposition and review of final bytes remain with root",
        },
    },
    "hashes": {"before": before["files"], "after": after["files"]},
    "authorDelta": q6["authorDelta"],
    "custody": {"frozen35": q6["frozen35"], "successor": q6["successor"],
                "watchedRuntimesModifiedAfterStart": q6["filesModifiedAfterThisRuntimeBegan"]},
    "controls": {
        "checkAtomsSuccessor": {"ok": atoms["ok"], "passed": atoms["passed"], "failed": atoms["failed"], "cases": len(atoms["results"])},
        "original89OnCorrectedModelBeforeNewControls": {"ok": atoms_model_only["ok"], "passed": atoms_model_only["passed"],
                                                        "failed": atoms_model_only["failed"]},
        "fallbackReachedByOriginalCases": {"frozen35": q1o["casesReachingFallback"], "successor": q1n["casesReachingFallback"]},
        "added": q4["addedCases"],
        "discriminatingAgainstFrozen35": q4["discriminating"],
        "addedPassBothModels": q4["addedPassBothModels"],
        "original89PassOnFrozen35Model": q4["originalCasesOnFrozen35Model"],
        "changedPreviousExpectations": [], "changedPreviousFixtures": [], "changedPreviousAssertions": [],
    },
    "consumers": q5,
    "pins": {"stalePinRows": q6["stalePinRows"], "rows": q6["pinRows"], "pinAdditionOwed": False,
             "requiredRootSealing": "reseal the 15 rows for the three owned files after review"},
    "dependenciesOnOtherOwners": ["root: reseal 15 stale pins", "root: reconcile A-13 and obtain independent review of these final bytes",
                                  "no schema or other-owner change required"],
    "remainingIssues": [
        {"id": "partial-dependency-census-incoming", "preExisting": True, "corrected": False,
         "measured": {"frozen35": {k: v(x) for k, x in q3o["incomingPartialDependencyObservation"].items()},
                      "successor": {k: v(x) for k, x in q3n["incomingPartialDependencyObservation"].items()}},
         "description": "incoming primary scope over {f,g} with an exact dependency scope for f only: all-covered true on both models; "
                        "needs a normative per-subject dependency totality decision; atom-api only"},
        "no closed enumeration / closed Run / retained Run constructed",
        "depth-2 control uses a synthetic DEPENDS_ON extension (published graph is depth 1)",
        "integrated groups and pin sealing not run (root)",
    ],
    "probeHistoryKept": [
        "q3-shapes-frozen35 first run; q3-shapes-frozen35.2 adds lawful disjoint-scope ordering and the partial-dependency observation "
        "after the two-provider same-subject shape was found to be SUBJECT_SCOPE_PARTITION_OVERLAP at closure (kept as synthetic Q3 row only)",
        "first model Edit attempt failed on text match and changed nothing; redone after reading exact bytes",
    ],
    "commands": commands,
    "grantsNothing": True,
}
text = json.dumps(doc, indent=1, default=str) + "\n"
(HERE / "review.json").write_text(text)
print(json.dumps({"wrote": str(HERE / "review.json"), "sha256": hashlib.sha256(text.encode()).hexdigest(),
                  "commands": len(commands), "mutationRows": len(mutations)}, indent=1))
