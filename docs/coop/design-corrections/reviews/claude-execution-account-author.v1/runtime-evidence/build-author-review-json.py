#!/usr/bin/env python3
"""Assemble author-review.json from the recorded receipts and handoff."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def jload(p):
    return json.loads(Path(p).read_text())


def main() -> int:
    handoff = jload(HERE / "changed-file-handoff.json")
    suite = jload(HERE / "suite-report.json")
    suite2 = jload(HERE / "suite2-report.json")
    checker = jload(HERE / "suite" / "execution-inputs.stdout")
    baseline = jload(HERE / "probes" / "receipts" / "baseline-check-execution-inputs" / "stdout.txt")
    delta = jload(HERE / "probes" / "receipts" / "p8-before-after-delta" / "stdout.txt")
    callers = jload(HERE / "probes" / "receipts" / "p9-existing-callers-byte-identity" / "stdout.txt")

    schema_after = jload(Path(handoff["afterImagesPreservedIn"])
                         / "docs__coop__design-corrections__foundation__execution-inputs.schema.v1.json")
    schema_precedence = (schema_after["$defs"]["NativeCoverageAccountV1"]
                         ["x-opensip-applicability-precedence"])

    new_cases = sorted({c["case"] for c in checker["cases"]} - {c["case"] for c in baseline["cases"]})
    full_runs = [c["fullRun"] for c in checker["cases"] if c.get("fullRun")]
    precedence = next((c["precedenceTable"] for c in checker["cases"] if c.get("precedenceTable")), None)

    out = {
        "standing": "Bounded execution-account source authorship on the isolated exact32 successor "
                    "copy. NOT acceptance, NOT independent design or consumer review, NOT product "
                    "qualification. No product implementation, live edit, commit or push. This "
                    "session is on the final application's exclusion list.",
        "authority": "root-blind19-diagnosis-assessment.v1/assessment.md, six decisions. Earlier "
                     "diagnostic prose is evidence, not authority.",
        "base": handoff["base"],
        "changedFileCount": handoff["changedFileCount"],
        "changedFiles": [
            {"path": r["path"], "decisions": r["decisions"],
             "beforeSha256": r["beforeSha256"], "afterSha256": r["afterSha256"]}
            for r in handoff["changedFiles"]
        ],
        "inspectedButUnchanged": [r["path"] for r in handoff["inspectedButUnchanged"]],
        "decisions": {
            "1-account-source-universe": {
                "implemented": True,
                "where": ["execution_inputs_model.v1.py want_u", "execution_inputs_fixture.v3.py",
                          "contract §5 external-join clause",
                          "schema x-opensip-external-joins + per-field descriptions"],
                "law": "nativeCoverageAccounts[i].sourceUniverse == EnumerationPlanV1.cells[ci]."
                       "programBindings[po].universe for EVERY applicability; null binding U stays null.",
                "targetUniverse": "deliberately NOT joined; cross-universe targets and "
                                  "multi-universe Runs stay lawful and are controlled.",
                "reachableBehaviourChange": False,
                "reachableBehaviourChangeEvidence": delta["sourceUniverseRuleDeltaOverLawfulShapes"],
                "note": "Publication + uniformity fix. The replaced expression already yielded the "
                        "binding U wherever a binding U existed, because the two nulled tokens are "
                        "reachable only at universe=null. blind19's refusal stands: it emitted null "
                        "for inapplicable-vcs.",
            },
            "2-first-match-applicability": {
                "implemented": True,
                "order": [r["token"] for r in schema_precedence["order"]],
                "reachableBehaviourChange": True,
                "changedCombinations": delta["applicability"]["changed"],
                "unchangedCombinations": delta["applicability"]["unchangedCombinations"],
                "whyUnselectedFirst": "enumeration-contract §1 refuses non-null universe on an "
                                      "unselected enumerator, so testing the universe first made "
                                      "unavailable-unselected unreachable.",
            },
            "3-request-vs-enumerator": {
                "implemented": True,
                "where": ["enumeration-contract.v1.md §1 clarification",
                          "contract §5 unsupported-cell clause",
                          "native-evidence.md explanatory paragraph"],
                "controls": ["optional-unselected-account-retained-typed-disclosure",
                             "optional-unsupported-cell-does-not-execute-a-provider",
                             "full-run-optional-unselected-and-optional-unsupported-close-without-"
                             "execution-deficiency"],
            },
            "4-unsupported-coverage-retained-and-unaccounted": {
                "implemented": True,
                "law": "Lawfully returned unknown Coverage for a selected-U UNSUPPORTED-TYPED "
                       "capability stays in its view, the stage capture, selectedRefs and native "
                       "disclosure; its account has coverageIds empty; derivedAccounts and "
                       "requiredCellDeficiencies carry the matrix pair, not the token alone; a "
                       "complete cell outcome means the account was answered, not that the "
                       "capability became supported.",
                "controls": ["unsupported-typed-account-carries-binding-universe",
                             "selected-u-unsupported-coverage-stays-selected-but-unaccounted",
                             "unsupported-account-discloses-the-matrix-pair-not-only-the-token",
                             "required-unsupported-cell-outcome-complete-but-assessment-indeterminate",
                             "full-run-required-unsupported-matrix-pair-bridge"],
            },
            "5-no-fabricated-carrier": {
                "implemented": True,
                "law": "Primary pair = first retained record that actually carries a typed pair, in "
                       "deterministic order; explicit (null, null) for pure missing work (no returned "
                       "partition, or expected subjects no partition covers); per-record pairs exact; "
                       "obligation carried by the existing null -> required-cell-unsatisfied bridge; "
                       "no new vocabulary member.",
                "carrierDelta": delta["carrier"],
                "controls": ["census-missing-subjects-derive-null-pair",
                             "census-missing-subjects-host-may-not-claim-provider-unavailable",
                             "empty-returned-partitions-host-may-not-claim-provider-unavailable",
                             "typed-native-carrier-survives-alongside-census-failure",
                             "typed-inventory-carriers-survive-alongside-census-failure",
                             "full-run-empty-returned-partitions-bridge-required-cell-unsatisfied",
                             "full-run-census-missing-subjects-bridge-keeps-originating-coverage"],
            },
            "6-query-mutation": {
                "implemented": "N/A to this source authorship",
                "note": "No feature and no vocabulary added. Q1-Q4 remain independent consumer "
                        "corrections after the normative successor.",
            },
        },
        "controls": {
            "checkerCasesBefore": len(baseline["cases"]),
            "checkerCasesAfter": len(checker["cases"]),
            "newCases": new_cases,
            "mismatches": checker["mismatches"],
            "oracleFailures": checker["oracles"],
            "applicabilityPrecedenceTable": precedence,
            "fullRunsThroughCloseRun": full_runs,
        },
        "suites": {
            "evaluator3Jobs": {
                "count": len(suite["checks"]),
                "allPassed": suite["allChecksPassed"],
                "exitCodes": {r["name"]: r["exitCode"] for r in suite["checks"]},
            },
            "referenceChildren": {
                "count": len(suite2["checks"]),
                "allPassed": suite2["passed"],
                "exitCodes": {r["script"]: r["exitCode"] for r in suite2["checks"]},
            },
            "authoritativeSourcePinsStale": sorted(
                {r["path"] for r in suite["stalePins"]} | set(suite2["authoritativeSourcePinsStale"])),
            "pinHandling": "Authoritative ledgers UNCHANGED. A clearly labelled DISPOSABLE rebinding "
                           "in this runtime was used only so the suites could execute; it is never "
                           "copied back. Root owns the real pin/planning rebinding and the final "
                           "current-suite run.",
        },
        "wholeTreeDelta": {
            "report": str(HERE / "tree-delta.json"),
            "frozenFiles": jload(HERE / "tree-delta.json")["frozen"]["files"],
            "frozenBytes": jload(HERE / "tree-delta.json")["frozen"]["bytes"],
            "changed": [r["path"] for r in jload(HERE / "tree-delta.json")["changedFiles"]],
            "added": jload(HERE / "tree-delta.json")["addedFiles"],
            "removed": jload(HERE / "tree-delta.json")["removedFiles"],
            "note": "Per-file hash comparison of this author's writable copy against the frozen32 "
                    "subject. Not a custody claim over frozen32, which remains the root retainer's.",
        },
        "existingCallerByteIdentity": {
            "allIdentical": callers["allExistingCallersIdentical"],
            "shapesChecked": sorted(callers["calls"]),
        },
        "boundaries": [
            "No acceptance of anything is claimed.",
            "No compiler / OS / host / product qualification claimed or requested; native "
            "observations remain synthetic as the parent reference states.",
            "No source pin or planning ledger changed.",
            "No consumer helper imported; blind19's five exports were NOT re-run and no claim is "
            "made that any of them admits; none of their bytes were reminted.",
            "Only the nine listed files were edited; no other owner's file and no admission "
            "boundary was touched.",
            "Full-Run controls are synthetic replay controls.",
        ],
        "remainingIssues": [
            "blind19's five exports were not re-executed by me; the expected 'still refused on "
            "F1/F2/F3, F4 gone' is reasoning from the corrected code, not a replay.",
            "_binding_carrier still defaults to provider-unavailable for a binding that declares no "
            "deficiency. Left in place (binding-owner carrier, which decision 5 lists as something "
            "to preserve) and flagged for root.",
            "Decision 1 has no reachable behavioural effect; confirm publication was the intent.",
            "Applicability table enumerated over 72 combinations across three representative "
            "relations, not every registered relation.",
            "The native-evidence.md change is explanatory only, not a native normative restatement.",
            "evaluator_input_model.v3.py:136-144 lets an optional unselected cell's own unavailable "
            "inventory make an unrelated required rule's enumeration incomplete. Outside bounded "
            "scope; not changed; raised for root.",
            "check-evaluator-composition.v3.py does not exist here; the composition checker is "
            "check-composition.v3.py (unchanged, exits 0).",
            "Full charter artefact assessment remains incomplete, as root already recorded.",
        ],
        "acceptanceClaim": None,
        "productQualification": False,
    }
    (HERE / "author-review.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "changedFileCount": out["changedFileCount"],
        "checkerCases": [out["controls"]["checkerCasesBefore"], out["controls"]["checkerCasesAfter"]],
        "mismatches": out["controls"]["mismatches"],
        "oracleFailures": out["controls"]["oracleFailures"],
        "suitesAllPassed": [out["suites"]["evaluator3Jobs"]["allPassed"],
                            out["suites"]["referenceChildren"]["allPassed"]],
        "stalePins": len(out["suites"]["authoritativeSourcePinsStale"]),
        "callerByteIdentity": out["existingCallerByteIdentity"]["allIdentical"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
