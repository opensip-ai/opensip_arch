#!/usr/bin/env python3
"""Assemble author-review.json and the handoff from the recorded receipts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECEIPTS = HERE / "probes" / "receipts"
V9 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v9")
V10 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v10")


def jload(p):
    return json.loads(Path(p).read_text())


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    frozen = jload(HERE / "reports" / "frozen33-verification.json")
    diff = jload(RECEIPTS / "d1b-proof-difference" / "stdout.txt")
    newp = jload(RECEIPTS / "d2-new-proof" / "stdout.txt")
    disc = jload(RECEIPTS / "d3-control-discrimination" / "stdout.txt")
    preserve = jload(HERE / "reports" / "preservation.json")
    final = jload(HERE / "verification" / "final" / "verification.json")
    demo = jload(HERE / "reports" / "honest-failure-demo.json")
    account = jload(V10 / "source33-remint.v1.json")

    receipts = []
    for d in sorted(RECEIPTS.iterdir()):
        if not d.is_dir() or not (d / "command.json").is_file() or not (d / "exit.txt").is_file():
            continue
        receipts.append({"label": d.name, "argv": jload(d / "command.json")["argv"],
                         "exit": int((d / "exit.txt").read_text().strip()),
                         "stdoutBytes": (d / "stdout.txt").stat().st_size,
                         "stderrBytes": (d / "stderr.txt").stat().st_size})

    out = {
        "standing": "AUTHOR reference-package correction only. NOT independent review, NOT blind "
                    "reconstruction, NOT product qualification, NOT acceptance of any kind. The "
                    "source author cannot accept the design, the blind work or the final "
                    "application. Source33 is frozen and was not edited. This package must never "
                    "be supplied to the blind consumer.",
        "session": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
        "ownedOutputs": [str(V10), str(HERE)],
        "frozenSourceVerification": {
            "manifestSha256": frozen["manifestSha256"],
            "manifestShaMatchesExpected": frozen["manifestShaMatchesExpected"],
            "parentManifestSha256": frozen["parentManifestSha256"],
            "files": frozen["verifiedFileCount"], "bytes": frozen["verifiedTotalBytes"],
            "mismatched": frozen["mismatchedCount"], "missing": frozen["missingCount"],
            "extraOnDisk": frozen["extraOnDiskCount"],
            "allBytesVerified": frozen["allBytesVerified"],
        },
        "diagnosis": {
            "symptom": "checkpoint3/author-ts and the two positive binding controls reached "
                       "structural ADMIT then EVALUATOR_COMPLETE_PROOF_REPLAY on frozen source33.",
            "proofFieldsThatDiffered": diff["differingFieldNames"],
            "retainedItem": diff["proofFieldDifferences"]["executionDeficiencies"]["retained"][1],
            "derivedItem": diff["proofFieldDifferences"]["executionDeficiencies"]["derived"][1],
            "rootCause": "author-helpers/evaluator.py kept the pre-source33 carrier rule: a "
                         "Coverage record carrying no pair borrowed records[0]'s deficiency while "
                         "keeping its own null nativeCause (an unzipped, re-paired carrier), with "
                         "a manufactured provider-unavailable behind it.",
            "isSourceDefect": False,
            "whyNot": "Frozen source33 refused correctly. execution-inputs-contract.v1.md sections "
                      "4 and 5 and evaluator-composition-contract.v3.md section 9.6 require each "
                      "retained record to contribute its OWN exact pair, with (null, null) "
                      "bridging to required-cell-unsatisfied and nothing manufactured.",
            "correctionScope": "author helper only; no frozen source byte changed and no fixture "
                               "adjusted to make an old artifact pass.",
        },
        "remint": {
            "newTsRunId": newp["newRunId"], "oldTsRunId": newp["oldRunId"],
            "proofFieldsDifferingOldVsNew": newp["proofFieldsDifferingOldVsNew"],
            "verdictUnchanged": newp["oldVerdict"] == newp["newVerdict"],
            "verdict": newp["newVerdict"],
            "ownerDerivedEqualsRetained": newp["ownerDerivedEqualsRetained"],
            "compareCompleteReplay": newp["compareCompleteReplay"],
            "carrierLawWitness": newp["carrierLawWitness"],
            "runComparison": account["runComparison"],
            "remintedGroups": account["remintedGroups"],
            "reusedExactGroups": account["reusedExactGroups"],
            "regeneratedDerivedArtifacts": account["regeneratedDerivedArtifacts"],
        },
        "negativeControlDiscrimination": {
            "package9": {k: disc["package9-source30-construction"][k] for k in
                         ("baseAdmits", "allControlsRefuse",
                          "refusalsAttributableToTheirOwnMutation")},
            "package10": {k: disc["package10-source33-remint"][k] for k in
                          ("baseAdmits", "allControlsRefuse",
                           "refusalsAttributableToTheirOwnMutation")},
            "conclusion": disc["conclusion"],
        },
        "verifierReportingCorrection": {
            "defect": "verify-package.py asserted mid-flight, so a failing run wrote no "
                      "verification.json at all.",
            "correction": "group crashes and query failures are RECORDED; verification.json is "
                          "always written before the final non-zero exit.",
            "expectationsWeakened": False,
            "expectationsPreserved": [
                "per-group admission/refusal conditions unchanged",
                "ENUMERATION_BINDING_PROGRAM_ENTRY clause unchanged",
                "EVALUATOR_COMPLETE_PROOF_REPLAY clause for negatives unchanged",
                "query condition still passed is True and exactly 7 checks",
                "final assert result['passed'] unchanged",
            ],
            "demonstration": {"exitCode": demo["exitCode"],
                              "verificationJsonWritten": demo["verificationJsonWritten"],
                              "verificationPassed": demo["verificationPassed"],
                              "recordedFailure": next(g["failure"] for g in demo["groups"]
                                                      if g["group"] == "query")},
        },
        "finalVerification": {
            "command": jload(RECEIPTS / "verify-package10-final" / "command.json")["argv"],
            "exitCode": int((RECEIPTS / "verify-package10-final" / "exit.txt").read_text().strip()),
            "passed": final["passed"],
            "sourceManifestSha256": final["sourceManifestSha256"],
            "packageManifestSha256": final["packageManifestSha256"],
            "sourceFilesVerified": final["sourceFilesVerified"],
            "packageFilesVerified": final["packageFilesVerified"],
            "runControlCaseCount": sum(g["count"] for g in final["groups"] if g["group"] != "query"),
            "queryCount": next(g["count"] for g in final["groups"] if g["group"] == "query"),
            "groups": final["groups"],
        },
        "hashes": {
            "sourceManifestSha256": frozen["manifestSha256"],
            "package10ArtifactManifestSha256": sha(V10 / "artifact-manifest.json"),
            "package9ArtifactManifestSha256": preserve["v9ArtifactManifestSha256"],
            "package9MatchesRootClaim": preserve["v9ArtifactManifestMatchesRootClaim"],
            "package10FilesOnDisk": preserve["v10FileCount"],
            "package10ManifestListsItself": False,
        },
        "preservation": {
            "package9FileCount": preserve["v9FileCount"],
            "changedVsV9": preserve["changedVsV9"],
            "addedVsV9": preserve["addedVsV9"],
            "removedVsV9": preserve["removedVsV9"],
            "historicalArtifactsPreserved": preserve["historicalArtifactsPreserved"],
            "sourceRebuildReceiptPreserved": preserve["sourceRebuildReceiptPreserved"],
            "residualAssessmentPreserved": preserve["residualAssessmentPreserved"],
            "originalRequirementHandoffPreserved": preserve["originalRequirementHandoffPreserved"],
            "workspaceHistoryPreserved": preserve["workspaceHistoryPreserved"],
            "beforeImages": "package10/historical-source33-before-remint/",
        },
        "coverage": {
            "runControlCases": 13, "queries": 7,
            "residualProposalsPending": 30,
            "propertiesProbeReproducedByteIdentically": True,
            "mixedUniverseProbeReproducedByteIdentically": True,
        },
        "limits": [
            "Only the TypeScript checkpoint compares a PARTIAL consumer helper with the owner; the "
            "six other positives are owner-derived/replayed self-consistency.",
            "exists/none exercised; and/or/not unexercised; count-at-most and all-covered "
            "unimplemented.",
            "Two-binding construction incomplete; a single explicit selection is retained.",
            "All native/compiler/OS records synthetic and unqualified; host TCB assumed for all 13.",
            "Thirty independent residual proposals remain individually PENDING.",
            "Source33 independent acceptance, whole-design review and blind acceptance remain "
            "required and outstanding.",
            "verification.json is package revalidation BY ITS OWN AUTHOR, not independent "
            "reconstruction.",
            "The corrected helper still emits execution deficiencies only for required "
            "supported-available accounts; it does not establish census, inventory, binding or "
            "candidate deficiencies, nor the unsupported-typed matrix rows the owner emits.",
            "The remint changed which execution deficiency is cited, NOT the verdict (fail both "
            "before and after).",
            "collapsed-deficiencies does not exercise the corrected law; its mutation discards the "
            "second item either way.",
            "No access to any consumer runtime, output or root blind file; none was read.",
        ],
        "receipts": receipts,
        "nonZeroExitReceipts": [r["label"] for r in receipts if r["exit"] != 0],
        "nonZeroExitExplanation": "d1-proof-difference: first probe attempt, wrong decode_store "
                                  "arity, kept. verify-remint-binding / verify-remint-semantic: "
                                  "exit 1 because check-export.v4.py reports 'some check refused', "
                                  "which is the EXPECTED outcome for a negative group and is what "
                                  "verify-package.py encodes per group.",
        "acceptanceClaim": None,
        "independentAssent": None,
        "productQualification": False,
    }
    (HERE / "author-review.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "frozenAllBytesVerified": out["frozenSourceVerification"]["allBytesVerified"],
        "finalPassed": out["finalVerification"]["passed"],
        "finalExit": out["finalVerification"]["exitCode"],
        "cases": out["finalVerification"]["runControlCaseCount"],
        "queries": out["finalVerification"]["queryCount"],
        "package10Manifest": out["hashes"]["package10ArtifactManifestSha256"],
        "changedVsV9": len(out["preservation"]["changedVsV9"]),
        "removedVsV9": len(out["preservation"]["removedVsV9"]),
        "historicalPreserved": out["preservation"]["historicalArtifactsPreserved"],
        "discriminationRepaired": (
            not out["negativeControlDiscrimination"]["package9"]["refusalsAttributableToTheirOwnMutation"]
            and out["negativeControlDiscrimination"]["package10"]["refusalsAttributableToTheirOwnMutation"]),
        "nonZeroExitReceipts": out["nonZeroExitReceipts"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
