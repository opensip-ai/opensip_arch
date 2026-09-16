#!/usr/bin/env python3
"""Assemble the v2 author-review.json from the recorded receipts and handoff."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECEIPTS = HERE / "probes" / "receipts"


def jload(p):
    return json.loads(Path(p).read_text())


def main() -> int:
    handoff = jload(HERE / "changed-file-handoff.json")
    focused = jload(HERE / "focused-checks-report.json")
    checker = jload(HERE / "suite" / "execution-inputs.stdout")
    v1_checker = jload(Path("/tmp/opensip-design-corrections/claude-execution-account-author.v1")
                       / "suite" / "execution-inputs.stdout")
    delta = jload(RECEIPTS / "q5-v2-delta" / "stdout.txt")
    mixed = jload(RECEIPTS / "q4c-mixed-account-primary" / "stdout.txt")
    cand = jload(RECEIPTS / "q2-candidate-absent" / "stdout.txt")
    order = jload(RECEIPTS / "q1-ordering-authority" / "stdout.txt")
    tree = jload(HERE / "tree-delta.json")

    from collections import Counter
    standings = Counter(c.get("controlStanding") for c in checker["cases"])
    new_cases = sorted({c["case"] for c in checker["cases"]}
                       - {c["case"] for c in v1_checker["cases"]})
    renamed = sorted({c["case"] for c in v1_checker["cases"]}
                     - {c["case"] for c in checker["cases"]})
    full_runs = [c["fullRun"] for c in checker["cases"] if c.get("fullRun")]

    receipts = []
    for d in sorted(RECEIPTS.iterdir()):
        if not d.is_dir() or not (d / "command.json").is_file() or not (d / "exit.txt").is_file():
            continue
        receipts.append({"label": d.name,
                         "argv": jload(d / "command.json")["argv"],
                         "exit": int((d / "exit.txt").read_text().strip())})

    out = {
        "standing": "Bounded FOLLOW-UP source authorship (v2). NOT acceptance, NOT independent "
                    "design or blind acceptance, NOT product qualification. Whole-design and blind "
                    "acceptance remain required and are not claimed. No frozen/live edit, no "
                    "pin/planning edit, no product implementation, no commit, no push.",
        "authority": "root-execution-account-draft-review.v1 and .v2 assessments plus "
                     "primary-pair-probe.json. The v1 runtime is preserved unchanged.",
        "startingBytesVerified": {
            "allV2BeforeEqualV1Handoff": handoff["v2BeforeIsV1Handoff"],
            "modelSha256": next(r["v2BeforeSha256"] for r in
                                handoff["changedInV2"] + handoff["unchangedInV2"]
                                if r["path"].endswith("execution_inputs_model.v1.py")),
            "note": "equals the SHA root's primary-pair-probe.json was taken against",
        },
        "findings": {
            "DRAFT-P1-cell-row-primary-pair": {
                "rootWasRight": True,
                "corrected": "_outcome_from_items takes the first source ACTUALLY carrying a typed "
                             "pair in the cross-source order; (null, null) when none does.",
                "rootProbeReplayed": mixed["rootUnitCounterexample"],
                "admittedFixture": {
                    k: mixed["admittedMixedAccountFixture"][k] for k in
                    ("result", "accountOrder", "rowState", "rowPair", "sourceOrder",
                     "requiredCellDeficiencies", "beforeModelDerivationOfTheseAccounts")
                },
                "fullRun": mixed["fullRun"],
                "conservativeCompletenessLawUnchanged":
                    delta["deriveOutcome"]["everyStateUnchanged"],
                "refsAndCausesUnchanged": {
                    "inputRefs": delta["deriveOutcome"]["everyInputRefListUnchanged"],
                    "nativeCauses": delta["deriveOutcome"]["everyNativeCauseListUnchanged"],
                },
                "changedRowPairs": delta["deriveOutcome"]["changedRowPairs"],
            },
            "DRAFT-P2-cross-source-order": {
                "publishedIn": ["contract §4 table", "M.SOURCE_ORDER",
                                "schema x-opensip-derived-carrier-law.crossSourceOrder"],
                "order": ["enumerator-or-binding", "inventory", "candidate", "account"],
                "authoritiesRead": {
                    "schemaOrders": order["schemaOrders"],
                    "matrixHasAnyXOpensipOrder": order["matrixHasAnyXOpensipOrder"],
                    "anyMatrixRelationArrayIsNotLexical": order["anyMatrixRelationArrayIsNotLexical"],
                    "syntaxRelationsAsAuthored": next(
                        r["relationsAsAuthored"] for r in order["matrixRelations"]
                        if r["capabilityId"] == "syntax"),
                },
                "deterministicBehaviourChanged": False,
                "note": "The account leg is the AUTHORED matrix relations array, not lexical; the "
                        "host's nativeCoverageAccounts order (x-opensip-order 'sequence', which "
                        "enforces nothing) is not read at all.",
            },
            "checker-reporting-standing": {
                "controlStandings": dict(standings),
                "noInventedAdmissionRow": True,
                "fullRunCasesReportRealRows": [
                    {"case": f["case"], "verdict": f["verdict"],
                     "realCellStates": f["sameGraphCellStates"],
                     "bridgedCausesFromAdmission": f["bridgedCausesFromAdmission"],
                     "proofCausePairs": f["executionCausePairs"]}
                    for f in full_runs
                ],
            },
            "independence-claim": {
                "corrected": True,
                "statement": "execution_inputs_fixture.v3.py calls M.derived_applicability, "
                             "M._summarize_coverage_records and M.derive_outcome, so these are "
                             "reference self-consistency controls with explicit oracles, not an "
                             "independent consumer reconstruction.",
            },
            "control-naming": {
                "renamedFrom": "optional-unsupported-cell-does-not-execute-a-provider",
                "renamedTo": "optional-unsupported-cell-owes-no-required-cell-row",
                "qualification": "selected enumerator, non-null U, admitted synthetic unknown "
                                 "Coverage; establishes absence of a required-cell row only. No "
                                 "synthetic fixture here establishes provider execution or its "
                                 "absence.",
            },
            "candidate-carrier": {
                "reachableContradiction": True,
                "evidence": {
                    "availableBindingHasDeficiencyProperty":
                        cand["availableBindingHasDeficiencyProperty"],
                    "availableBindingAdditionalProperties":
                        cand["availableBindingAdditionalProperties"],
                    "bindingCarrierOnAvailableBinding": cand["binding_carrier_on_available_binding"],
                    "optionalNoEnvelope": {
                        k: cand["selectedU_optional_candidate_no_envelope"][k]
                        for k in ("result", "derivedOutcomes", "derivedSources")},
                    "requiredNoEnvelope": {
                        k: cand["selectedU_required_candidate_no_envelope"][k]
                        for k in ("result", "refusals")},
                },
                "correction": "_declared_binding_carrier reads the binding's own declared pair with "
                              "no default; candidate pair = envelope's own, else binding's declared, "
                              "else (null, null). Row state and refs unchanged.",
                "bindingCarrierPreserved": True,
                "enumerationGuardsConfirmed": cand["enumerationGuards"],
            },
            "F4-cross-owner-qualification": {
                "preserved": True,
                "writtenInto": "evaluator-composition-contract.v3.md §9.6",
                "statement": "§9.6's table explicitly PRESCRIBED the provider-unavailable fallback; "
                             "this was a contradiction between two normative owners, not merely a "
                             "reference-side invention. The historical diagnosis is preserved "
                             "unchanged; this is an added qualification.",
            },
            "optional-inventory-same-kind-rule": {
                "changed": False,
                "description": "Existing, deliberately conservative behaviour across all "
                               "kind-matching inventories in the mode domain "
                               "(evaluator_input_model.v3.py:136-138). Not a proved gap.",
            },
        },
        "controls": {
            "checkerCasesV1": len(v1_checker["cases"]),
            "checkerCasesV2": len(checker["cases"]),
            "newCases": new_cases,
            "renamedOrRemovedCases": renamed,
            "mismatches": checker["mismatches"],
            "oracleFailures": checker["oracles"],
        },
        "focusedChecks": {
            "allPassed": focused["allChecksPassed"],
            "exitCodes": {r["name"]: r["exitCode"] for r in focused["checks"]},
            "notRun": focused["notRun"],
            "notRunReason": focused["notRunReason"],
            "authoritativePinsStale": focused["authoritativePinsStale"],
        },
        "existingCallerByteIdentity": {
            "allIdentical": delta["graphFixtureCallers"]["allIdentical"],
            "shapesChecked": sorted(delta["graphFixtureCallers"]["calls"]),
        },
        "wholeTreeDelta": {
            "frozenFiles": tree["frozen"]["files"], "frozenBytes": tree["frozen"]["bytes"],
            "changedVsFrozen32": tree["changedCount"],
            "added": tree["addedFiles"], "removed": tree["removedFiles"],
            "changedInV2": tree["changedInV2"],
            "unchangedSinceV1": tree["unchangedSinceV1"],
            "newFilesTouchedInV2BeyondV1": tree["newFilesTouchedInV2BeyondV1"],
        },
        "limits": [
            "No acceptance of anything; whole-design and blind acceptance remain required.",
            "Reference self-consistency plus explicit oracles, not independent reconstruction.",
            "No provider execution, and no compiler/OS/host/product qualification, is established.",
            "full_run_case's admission columns are a same-graph re-run, made testable by "
            "bridgedCausesEqualProof rather than asserted.",
            "Order survey covered the six arrays feeding a cell row and every capability relations "
            "array; not the whole schema corpus.",
            "blind19's five exports remain un-replayed here; no admission claim is made for any.",
            "The candidate correction changes the candidate item's PAIR only; whether that cell "
            "shape should be admissible at all is owned elsewhere and was not changed.",
        ],
        "receipts": receipts,
        "nonZeroExitReceipts": [r["label"] for r in receipts if r["exit"] != 0],
        "nonZeroExitExplanation": "authoring iterations kept rather than discarded: "
                                  "v2-step1-checker (the control-standing key collided with the "
                                  "admission result's own `standing`; renamed to controlStanding) "
                                  "and two earlier q4 probe runs.",
        "acceptanceClaim": None,
        "productQualification": False,
    }
    (HERE / "author-review.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "changedInV2": handoff["changedInV2Count"],
        "checkerCases": [out["controls"]["checkerCasesV1"], out["controls"]["checkerCasesV2"]],
        "mismatches": out["controls"]["mismatches"],
        "oracleFailures": out["controls"]["oracleFailures"],
        "focusedChecksPassed": out["focusedChecks"]["allPassed"],
        "controlStandings": dict(standings),
        "callerByteIdentity": out["existingCallerByteIdentity"]["allIdentical"],
        "wholeTreeChanged": out["wholeTreeDelta"]["changedVsFrozen32"],
        "newCases": new_cases,
        "renamed": renamed,
    }, indent=2))
    _ = hashlib
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
