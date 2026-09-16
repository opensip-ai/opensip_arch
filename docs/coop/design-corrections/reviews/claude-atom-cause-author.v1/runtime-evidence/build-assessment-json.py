"""Build assessment.json and changed-file-handoff.json from the retained receipts.

Every count is read back out of probes/receipts/, never typed in twice.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE / "probes" / "receipts"
SRC = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source")
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v33")


def js(label, name="stdout.txt"):
    return json.loads((R / label / name).read_text())


def txt(label, name="stdout.txt"):
    return (R / label / name).read_text()


before = {r["path"]: r for r in json.loads((HERE / "before-hashes.json").read_text())}
after = {r["path"]: r for r in json.loads((HERE / "after-hashes.json").read_text())}
custody = js("a10-compare-atom-reports")
discriminate = js("a8-controls-discriminate")
kit = js("a12-kit-implementability.2")
pins = js("a11-stale-pins")
atoms_final = js("check-atoms-final")
realrun_before = js("a3-realrun-stability")
realrun_after = js("a9-realrun-after-correction")
fold_before = js("a1-order-trigger") if (R / "a1-order-trigger" / "stdout.txt").exists() else None
after_corr = js("a4-after-correction")

by_case = {}
for row in discriminate["results"]:
    by_case.setdefault(row["case"], {})[row["model"]] = row["ok"]

PURPOSE = {
    "docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md":
        "Publishes, in section 4, the completeness-result/truth-independence rule, the ascending "
        "scope2/coverage2 selection order, the six-step outgoing cause derivation with each "
        "cause's universe and the exact refs each return carries, the incoming derivation and its "
        "absence of any early return, and the deterministic DEPENDS_ON view with the "
        "coverage-unknown carrier rule. Makes existing behaviour explicit; adds no cause token "
        "and no public field.",
    "docs/coop/design-corrections/foundation/atom_model.v1.py":
        "Minimal reference correction: _coverages_exact and _scopes_exact return their selections "
        "in ascending identifier order instead of host map order, so the first-wins folds "
        "downstream (_conservative_entry's typed carrier, run_suff's nativeCause scan) read a "
        "deterministic logical input. Two return statements plus docstrings; no other behaviour "
        "change.",
    "docs/coop/design-corrections/foundation/check-atoms.v1.py":
        "Six reference controls for the publication boundary, deterministic cause/field "
        "selection, early-stop scope, known-hit dominance and shared incoming/dependency "
        "behaviour, exercising the actually selected atom owner.",
}

changed = []
for path in sorted(after):
    changed.append({
        "path": path,
        "beforeSha256": before[path]["sha256"],
        "afterSha256": after[path]["sha256"],
        "beforeBytes": before[path]["bytes"],
        "afterBytes": after[path]["bytes"],
        "beforeEqualsFrozen33": before[path]["equalsFrozen33"],
        "beforeImage": before[path]["image"],
        "afterImage": after[path]["image"],
        "purpose": PURPOSE[path],
    })

handoff = {
    "standing": "AUTHOR/REFERENCE handoff of an isolated design/reference correction. Not an "
                "acceptance, qualification or approval. No source33, live repository, pin-ledger "
                "or planning-layer edit. Root rebinds pins after handoff.",
    "authorOrigin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "runtime": str(HERE),
    "isolatedSourceCopy": str(SRC),
    "baseline": str(FROZEN),
    "custody": custody["custody"],
    "changedFiles": changed,
    "stalePinEntries": pins["pinEntries"],
    "stalePinCount": pins["staleCount"],
    "pinLedgersEdited": [],
}
(HERE / "changed-file-handoff.json").write_text(json.dumps(handoff, indent=2) + "\n")

assessment = {
    "standing": handoff["standing"],
    "interpreter": "/tmp/opensip-architecture-review-env/bin/python -I -B",
    "receiptsRoot": str(R),
    "custody": custody["custody"],
    "changedFiles": [{k: c[k] for k in ("path", "beforeSha256", "afterSha256")} for c in changed],
    "contractAmendment": {
        "section": "4. Completeness partitions",
        "blocks": [
            "Completeness result and its independence from truth",
            "Selection order (both endpoints)",
            "Outgoing cause derivation (endpoint=source), in order",
            "Incoming cause derivation (endpoint=target)",
            "Deterministic dependency view, and the coverage-unknown carrier",
        ],
        "decisionPlaceholdersRemaining": 0,
        "newCauseTokens": [],
        "newPublicFields": [],
        "rootDecisionsEncoded": {
            "noOwedBindings": "missing-relation-coverage, universe null",
            "bindingsButNoneAvailableAtU": "selector-unbound, universe null",
            "noContainingScope": "uncovered-expected-source-subject, universe U",
            "twoDistinctCausesKept": True,
            "existingChannelsKept": ["atom causes[]", "atom nativeDeficiencies[]",
                                     "per-Coverage entry.deficiency"],
            "knownPositiveDominancePreserved": True,
            "typedOriginalCausesPreserved": True,
        },
    },
    "referenceCorrection": {
        "functions": ["_coverages_exact", "_scopes_exact"],
        "change": "return sorted(out, key=lambda pair: pair[0])",
        "rootCause": "evaluator_input_model.v3.py:161-163 builds facts/scopes/coverages from "
                     "Python set comprehensions; -I implies -E so PYTHONHASHSEED is ignored and "
                     "set iteration order varies per process.",
        "affectedFolds": ["_conservative_entry typed carrier (first-wins)",
                          "run_suff nativeCause scan (first-wins)"],
        "evidenceBefore": {
            "foldProbe": "a1-order-trigger",
            "surfacingProbe": "a2-surfacing",
            "deterministic": False,
        },
        "evidenceAfter": {
            "probe": "a4-after-correction",
            "foldDeterministic": after_corr["fold"]["DETERMINISTIC"],
            "surfaceDeterministic": after_corr["surface"]["DETERMINISTIC"],
            "foldRuns": after_corr["fold"]["runs"],
            "surfaceRuns": after_corr["surface"]["runs"],
            "inputDictOrdersStillVaried": {
                "fold": after_corr["fold"]["distinctDictOrders"],
                "surface": after_corr["surface"]["distinctDictOrders"],
            },
            "distinctHelperOrders": after_corr["fold"]["distinctHelperOrders"],
        },
        "latent": True,
        "latentBasis": "The retained reference fixture Run replays to one proof sha before the "
                       "correction across 8 processes; no shipped fixture reaches the fold.",
    },
    "controls": {
        "checkAtomsCases": {"frozen33": custody["frozen33Report"]["cases"],
                            "successor": custody["successorReport"]["cases"]},
        "checkAtomsResult": {"ok": atoms_final["ok"], "passed": atoms_final["passed"],
                             "failed": atoms_final["failed"]},
        "preExistingCaseResultsUnchanged": custody["sharedCasesIdentical"],
        "added": custody["addedCases"],
        "discriminating": discriminate["discriminating"],
        "publicationControlsPassingBothModels": discriminate["passesBothModels"],
        "honestNote": "Five of the six added controls pass against both the corrected and the "
                      "uncorrected model. They are publication controls: they pin behaviour the "
                      "amended prose now states and the reference already had, so the two cannot "
                      "drift apart. Only the fold-carrier control detects the correction.",
    },
    "focusedChecks": [
        {"check": "check-atoms.v1.py", "exit": 0, "receipt": "check-atoms-final"},
        {"check": "check-replay.v3.py", "exit": 0, "receipt": "focused-check-replay.v3"},
        {"check": "check-semantic-replay.v3.py", "exit": 0,
         "receipt": "focused-check-semantic-replay.v3"},
        {"check": "check-candidate-replay.v3.py", "exit": 0,
         "receipt": "focused-check-candidate-replay.v3"},
        {"check": "check-execution-replay.v3.py", "exit": 0,
         "receipt": "focused-check-execution-replay.v3"},
        {"check": "check-execution-inputs.v1.py", "exit": 0,
         "receipt": "focused-check-execution-inputs.v1"},
        {"check": "check-provider-attribution-return.v2.py", "exit": 0,
         "receipt": "focused-check-provider-attribution-return.v2"},
    ],
    "crossModelStdoutIdentical": {
        "identical": ["check-replay.v3.py", "check-semantic-replay.v3.py",
                      "check-candidate-replay.v3.py", "check-execution-replay.v3.py",
                      "check-execution-inputs.v1.py", "check-provider-attribution-return.v2.py"],
        "differs": ["check-atoms.v1.py"],
        "differsBecause": "the successor adds six cases; the 70 shared case results are identical",
    },
    "runReplay": {
        "path": "seal_fixture -> open_run_closure -> derive -> seal_derived -> replay -> close_run",
        "processesEach": realrun_before["runs"],
        "before": {"runIds": realrun_before["distinctRunIds"],
                   "proofSha256": realrun_before["distinctProofSha256"],
                   "sample": realrun_before["sample"]},
        "after": {"runIds": realrun_after["distinctRunIds"],
                  "proofSha256": realrun_after["distinctProofSha256"],
                  "sample": realrun_after["sample"]},
        "identical": (realrun_before["distinctProofSha256"] == realrun_after["distinctProofSha256"]
                      and realrun_before["distinctRunIds"] == realrun_after["distinctRunIds"]),
        "completeRunParityClaimed": False,
        "completeRunParityNote": "One retained reference Run was replayed, plus the Runs the six "
                                 "affected checks construct internally. The full retained Run "
                                 "corpus was not replayed and the six broad reference groups were "
                                 "not run.",
    },
    "normativeKit": {
        "fileCount": kit["kitFileCount"],
        "roots": kit["kitRoots"],
        "pythonExcluded": True,
        "tokensOnlyInThisContract": kit["tokensOnlyInThisContract"],
        "retainedLooserFirstAttempt": "a12-kit-implementability",
    },
    "limitations": [
        "Not an acceptance, qualification or approval; root owns pin reconciliation and the full "
        "reference groups.",
        f"{pins['staleCount']} pin entries across 5 ledgers go stale; no ledger was edited.",
        "ViewEntryV3.coverage is a two-member enum (complete, unknown) yet _conservative_entry "
        "ranks an intermediate 'partial' and several pre-existing reference checks build entries "
        "with coverage='partial'. Unreachable on admitted input and no existing conclusion turns "
        "on it. Reported, deliberately not changed.",
        "The nondeterminism is latent: demonstrated by controlled multi-process probes, not by a "
        "Run diff.",
        "Published causes are a canonical set (_uniq_causes dedups and sorts), so emission order "
        "is not observable and no control asserts it.",
        "No consumer code or expected output was used; code comparisons are author/reference "
        "evidence, not normative authority.",
    ],
}
(HERE / "assessment.json").write_text(json.dumps(assessment, indent=2) + "\n")

print(json.dumps({
    "wrote": [str(HERE / "assessment.json"), str(HERE / "changed-file-handoff.json")],
    "assessmentSha256": hashlib.sha256((HERE / "assessment.json").read_bytes()).hexdigest(),
    "handoffSha256": hashlib.sha256((HERE / "changed-file-handoff.json").read_bytes()).hexdigest(),
    "changedFiles": len(changed),
    "stalePins": pins["staleCount"],
    "atomCases": atoms_final["passed"],
    "runParityIdentical": assessment["runReplay"]["identical"],
}, indent=2))
