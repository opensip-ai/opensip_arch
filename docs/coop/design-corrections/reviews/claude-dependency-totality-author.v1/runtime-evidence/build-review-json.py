"""Assemble review.json from the retained receipts. Counts and cells are read back, never retyped."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE / "probes" / "receipts"


def js(label):
    return json.loads((R / label / "stdout.txt").read_text())


before = json.loads((HERE / "before-hashes.json").read_text())["files"]
after = json.loads((HERE / "after-hashes.json").read_text())["files"]
z1p, z1s = js("z1-shapes-previous.2"), js("z1-shapes-successor")
z2, z3, z4 = js("z2-controls-discriminate"), js("z3-consumers"), js("z4-custody-delta-pins")
atoms, atoms_model_only = js("check-atoms-successor"), js("check-atoms-model-only")


def value(x):
    return x.get("value") if "value" in x else "REFUSE:" + str(x.get("key"))


changed = []


def walk(a, b, path):
    if isinstance(a, dict) and "admission" in a:
        if a != b:
            changed.append({"cell": "/".join(path), "previous": value(a), "successor": value(b),
                            "nativeDeficienciesPrevious": a.get("nativeDeficiencies"),
                            "nativeDeficienciesSuccessor": b.get("nativeDeficiencies"),
                            "coverageIdsSuccessor": b.get("coverageIds")})
        return
    if isinstance(a, dict):
        for k in a:
            if k in ("model", "modelSha256"):
                continue
            walk(a[k], b[k], path + [k])


walk(z1p, z1s, [])
commands = []
for d in sorted(R.iterdir()):
    if (d / "command.json").exists() and (d / "exit.txt").exists():
        dig = json.loads((d / "digests.json").read_text()) if (d / "digests.json").exists() else {}
        commands.append({"label": d.name, "argv": json.loads((d / "command.json").read_text())["argv"],
                         "exit": int((d / "exit.txt").read_text()), **dig})

doc = {
    "review": "source-author correction: per-subject dependency totality in dependency-totality-successor.v1",
    "authorOrigin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "standing": "AUTHORSHIP ONLY; author never acceptor. Architecture/design/reference. No acceptance, readiness, "
                "application, product qualification, commit or push. Reviewer ce3's assessment not read.",
    "inputs": {
        "copyVerification": "/tmp/opensip-design-corrections/root-source36-preparation.v1/totality-copy-verification.json",
        "rootInvestigation": "/tmp/opensip-design-corrections/root-dependency-totality35-investigation.v1/{probe.py,probe.json}",
        "beforeBytesAre": "completed dependency-scope author bytes (frozen35 + that three-file delta)",
    },
    "decision": {
        "finding": "SUBSTANTIATED: a single folded dependency position let some owed source subjects' partitions establish "
                   "incoming completeness for a whole primary partition (per-scope and whole-source attestation routes); "
                   "regrouping into disjoint partitions changed the answer.",
        "correction": "section 4 Dependency totality (same kind): gap = a present same-kind dependency position leaving an owed "
                      "subject uncovered; the actual view AND the view without gap positions are both evaluated by native "
                      "sufficiency, both answers retained, satisfied only if both are; nothing fabricated.",
        "owedSubjects": {"outgoing": "current source subject", "incomingPerScope": "evaluated source scope subjects",
                         "incomingAttestationView": "union of subjects of the provider group's owned scopes"},
        "covered": "some exact (R, rung, S) selected scope contains the subject AND pairs >=1 Coverage at exact (R, rung, S, T)",
        "unchanged": ["selection and mapping/commitment pairing", "no mapped fallback", "folds and cited coverage",
                      "I1 and search accounting", "known-match and count-bound dominance", "outgoing results",
                      "different-kind whole-source dependencies", "attestation whole-source selection/fold",
                      "exact-rung and recursive-depth semantics", "empty owed set", "admission laws"],
        "alternativesRejected": {
            "dropPosition": "loses the actual partition's deficiency, carrier and cited Coverage",
            "coerceFoldedEntryUnknown": "rewrites actual evidence into a value no partition carries",
            "perSubjectViews": "multiplies evaluations and cause records; no semantic gain",
            "leaveAttestationUnchecked": "measured same unsound true; truth would depend on evidence form",
        },
        "choicesOthersMayJudgeDifferently": [
            "attestation owed set = owned-scope subjects (alternative: S inventory population)",
            "different-kind dependencies left whole-source and unchecked (needs a file->symbol containment decision)",
        ],
    },
    "measurements": {"standing": "synthetic atom-api; syntheticDepth2 rows use an in-process DEPENDS_ON extension",
                     "previousModelSha256": z1p["modelSha256"], "successorModelSha256": z1s["modelSha256"],
                     "changedCells": changed, "changedCellCount": len(changed)},
    "hashes": {"before": before, "after": after},
    "authorDelta": z4["authorDelta"], "cumulativeDeltaVsFrozen35": z4["frozen35Delta"],
    "custody": {"frozen35": z4["frozen35"], "successor": z4["successor"], "placeholders": z4["placeholders"],
                "watchedFilesModifiedAfterThisRuntimeBegan": z4["watchedFilesModifiedAfterThisRuntimeBegan"],
                "note": "root-source36-preparation.v1 additions are root-authored preparation files; not read"},
    "controls": {
        "checkAtomsSuccessor": {"ok": atoms["ok"], "passed": atoms["passed"], "failed": atoms["failed"], "cases": len(atoms["results"])},
        "original95OnCorrectedModelBeforeNewControls": {"ok": atoms_model_only["ok"], "passed": atoms_model_only["passed"],
                                                        "failed": atoms_model_only["failed"]},
        "added": z2["addedCases"], "discriminatingAgainstPreviousModel": z2["discriminating"],
        "addedPassBothModels": z2["addedPassBothModels"],
        "previous95OnPreviousModel": z2["previousCasesOnPreviousModel"],
        "previous95OnSuccessorModel": z2["previousCasesOnSuccessorModel"],
        "previousModelErrors": z2["previousModelErrors"],
        "changedPreviousExpectations": [], "changedPreviousFixtures": [], "changedPreviousAssertions": [],
    },
    "downstreamCheckers": z3,
    "standings": {"syntheticAtomApi": "all controls and Z1", "syntheticDependencyGraph": "depth-2 control",
                  "nativeProducer": "not used", "closedEnumeration": "not run", "retainedOrClosedRun": "not run",
                  "reachabilityClaimed": False},
    "crossOwner": {"required": [], "evidence": ["all callers private to atom_model.v1.py",
                                                "required-relation-missing already a registered native deficiency",
                                                "Z3 downstream checkers byte-identical"],
                   "notImplementedRootPlanned": ["historySubjectOrder duplicate-preserving sequence prose",
                                                 "explicit runtime polarity quantifier wording"]},
    "pins": {"stalePinRows": z4["stalePinRows"], "rows": z4["pinRows"], "pinAdditionOwed": False,
             "requiredRootSealing": "reseal the 15 rows for the three owned files after review"},
    "remainingIssues": [
        "different-kind dependency totality (clones->declares) not subject-checked; needs a normative containment decision",
        "attestation owed set chosen as owned-scope subjects; inventory-population alternative also sound",
        "empty-subject primary reachability scope stays conservatively unknown on both models (unchanged)",
        "reachability beyond synthetic atom-api unestablished; reviewer ce3 assessment and root reconciliation remain",
    ],
    "probeHistoryKept": [
        "z1-shapes-previous: first run also inventoried h (not in any primary scope) so incoming rows carried "
        "uncovered-expected-source-subject; kept; fixed and rerun as z1-shapes-previous.2",
    ],
    "commands": commands,
    "grantsNothing": True,
}
text = json.dumps(doc, indent=1, default=str) + "\n"
(HERE / "review.json").write_text(text)
print(json.dumps({"wrote": str(HERE / "review.json"), "sha256": hashlib.sha256(text.encode()).hexdigest(),
                  "commands": len(commands), "changedCells": len(changed)}, indent=1))
