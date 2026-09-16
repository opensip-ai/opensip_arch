"""Assemble review.json from the retained receipts. Every count is read back from a receipt."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE / "probes" / "receipts"


def js(label):
    return json.loads((R / label / "stdout.txt").read_text())


before, after = json.loads((HERE / "before-hashes.json").read_text()), json.loads((HERE / "after-hashes.json").read_text())
p1o, p1n = js("p1-must-matrix-frozen34.3"), js("p1-must-matrix-successor")
p2o, p2n = js("p2-a12-frozen34"), js("p2-a12-successor")
p3, p4, p5 = js("p3-controls-discriminate.2"), js("p4-consumers"), js("p5-custody-delta-pins.2")
p6o, p6n = js("p6-global-admission-frozen34"), js("p6-global-admission-successor")
atoms, atoms_model_only = js("check-atoms-successor.2"), js("check-atoms-model-only")


def value(x):
    return x.get("value") if "value" in x else "REFUSE:" + str(x.get("key"))


def matrix_delta(old, new, section):
    rows = []
    for label in old[section]:
        for cell in old[section][label]:
            a, b = old[section][label][cell], new[section][label][cell]
            if a != b:
                rows.append({"input": label, "cell": cell, "frozen34": value(a), "successor": value(b),
                             "causesAdded": [c for c in b.get("causes", []) if c not in a.get("causes", [])],
                             "causesRemoved": [c for c in a.get("causes", []) if c not in b.get("causes", [])],
                             "knownFrozen34": len(a.get("known") or []), "knownSuccessor": len(b.get("known") or [])})
    return rows


commands = []
for d in sorted(R.iterdir()):
    if (d / "command.json").exists():
        commands.append({"label": d.name, "argv": json.loads((d / "command.json").read_text())["argv"],
                         "exit": int((d / "exit.txt").read_text())})

ref_delta = matrix_delta(p1o, p1n, "references")
imp_delta = matrix_delta(p1o, p1n, "importsKnownMatches")
doc = {
    "review": "source-author correction of MUST-34-01 and A-12 in the isolated incoming-binding successor tree",
    "authorOrigin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "standing": "Architecture/design/reference authorship. Not independent acceptance, blind acceptance, application, "
                "readiness, activation or product qualification. No commit or push. Root owns pins, generated reports, "
                "navigation/readiness records and freezing.",
    "inputs": {
        "frozenParent34": "/tmp/opensip-design-corrections/candidate-subject.v34",
        "manifestSha256": p5["manifestSha256"],
        "manifestMatchesDeclared": before["manifestShaMatchesDeclared"],
        "independentReview": "/tmp/opensip-design-corrections/claude-independent-design.v34/review.md + review.json "
                             "(newMustIssues, advisories, sourceChangeAssessment); probes/receipts q09, q10, q11 inspected",
        "reviewerEvidenceTreatment": "Evidence to evaluate, not a requirement. q10's matrix parser measured nothing and is "
                                     "superseded by q11; q10 is not used. No consumer, runtime, report or root-blind data used.",
    },
    "decisions": {
        "MUST-34-01": {
            "decision": "ACCEPTED AS A DESIGN DEFECT; CORRECTED CONSERVATIVELY (contract section 4 incoming step I1 + reference).",
            "rule": "endpoint=target, P2 did not return, and no available owed binding has universe = U: accumulate "
                    "selector-unbound (evidenceKind null, nativeCause null, universe key omitted -> projected null), "
                    "completeness unknown, NO return.",
            "precedence": "after P1 and P2; before per-universe accumulation; at most once; order independent",
            "unavailableBindings": "never satisfy I1; beside an owed-family unavailable binding both unavailable-program-binding and selector-unbound are retained",
            "foreignFamilyOnly": "unknown with selector-unbound; both cross-family-edge-not-owed routes retained",
            "explicitSelectionScope": "an explicit/narrowed request narrows work, not what an incoming negative must have searched",
            "knownEvidence": "matching untouched: exists/none and exceeded count-at-most keep known results; only completeness-dependent answers become unknown",
            "reachability": "No normative admission boundary I examined makes the premise unreachable. Not demonstrated reachable at "
                            "closed enumeration admission: I did not run admit_enumeration and built no retained Run. The retained "
                            "analysis-spec and enumeration cell join are per ownership tuple (enumeration_model.v1.py:632-637); "
                            "default-profile non-reachability is the reviewer's q11 (code and receipt read, not re-executed).",
            "oldVersusNewOnRealApi": {"standing": "atom-api", "referencesChangedCells": ref_delta,
                                      "importsKnownMatchChangedCells": imp_delta,
                                      "multiProvider": {k: {"frozen34": value(p1o["multiProvider"][k]["sample"]),
                                                            "successor": value(p1n["multiProvider"][k]["sample"]),
                                                            "orderings": p1n["multiProvider"][k]["orderings"],
                                                            "distinctResultsFrozen34": p1o["multiProvider"][k]["distinctResults"],
                                                            "distinctResultsSuccessor": p1n["multiProvider"][k]["distinctResults"]}
                                                        for k in p1n["multiProvider"]}},
        },
        "A-12": {
            "decision": "ACCEPTED; prose corrected, plus one atom-api admission tightening found while validating item 2.",
            "item1": "Table row 1 no longer offers a qualifying attestation for a scope-less group; admitted-inputs note publishes "
                     "the scopeRefs minItems/exact-join refusal and the empty-subject-scope closure. No schema or admission change.",
            "item2": "Reviewer is correct at the native carrier (absent and null both refused). At the atom API, frozen34 admitted a "
                     "scope whose enumeratorClosure KEY was absent (only null refused) and could answer none=true through it. "
                     "_scope_descriptor now passes fields through so the native carrier refuses absent like null.",
            "oldVersusNew": {"A12-1": {k: [str(value(p2o["A12-1"][k]) if isinstance(p2o["A12-1"][k], dict) else p2o["A12-1"][k]),
                                           str(value(p2n["A12-1"][k]) if isinstance(p2n["A12-1"][k], dict) else p2n["A12-1"][k])]
                                       for k in p2o["A12-1"]},
                             "A12-2": {k: [p2o["A12-2"][k].get("value", p2o["A12-2"][k].get("key", p2o["A12-2"][k].get("admitted"))),
                                           p2n["A12-2"][k].get("value", p2n["A12-2"][k].get("key", p2n["A12-2"][k].get("admitted")))]
                                       for k in p2o["A12-2"]}},
            "globalAdmission": {
                "measured": {"frozen34": p6o, "successor": p6n},
                "finding": "The carrier tightening also reaches GLOBAL IncomingSearchV1 admission: an attestation naming a "
                           "key-absent scope was admitted by frozen34 (and both a references and a calls incoming atom "
                           "answered true); the successor refuses admit_atom_inputs with ATOM_NATIVE_CARRIER, because "
                           "attestation admission pairs its named scopes. A key-absent scope that is neither named by an "
                           "attestation nor consumed by the evaluation is still not validated, and produces no value.",
                "correctedExpectation": "Before measuring, I expected global admission NOT to validate named scopes and "
                                        "drafted that as a remaining issue; P6 showed the opposite and the draft was withdrawn.",
            },
        },
    },
    "hashes": {"before": before["files"], "after": after["files"]},
    "delta": p5["delta"],
    "custody": {"frozen34": p5["frozen34"], "successor": p5["successor"]},
    "controls": {
        "checkAtomsSuccessor": {"ok": atoms["ok"], "passed": atoms["passed"], "failed": atoms["failed"], "cases": len(atoms["results"])},
        "original81OnChangedModelBeforeNewControls": {"ok": atoms_model_only["ok"], "passed": atoms_model_only["passed"],
                                                      "failed": atoms_model_only["failed"]},
        "added": p3["addedCases"],
        "discriminatingAgainstFrozen34Model": p3["discriminating"],
        "passBothModels": p3["passBothModels"],
        "original81PassOnFrozen34Model": p3["originalCasesOnFrozen34Model"],
        "changedPreviousExpectations": [],
        "changedPreviousFixtures": [{
            "case": "test_dep_fold_replaces_whole_records_and_keeps_ties",
            "change": "unresolvedEdgeClasses member 'dynamic-import' -> 'dynamic-import-nonliteral' (a valid UnresolvedEdgeKindV1 member)",
            "why": "the old fixture was not a natively valid ResolutionCompletenessV2 record; the case asserts whole-record equality, "
                   "so no expected result changed"}],
    },
    "consumers": p4,
    "standings": {
        "helper-unit": "test_dep_fold_replaces_whole_records_and_keeps_ties (unchanged standing)",
        "atom-api": "all eight added controls; P1; P2 atom-api rows; P6",
        "stock-schema": "P2 IncomingSearchV1 scopeRefs [] under jsonschema alone",
        "native-carrier": "P2 subject_scope_commitment rows",
        "closed-enumeration-admission": "NOT RUN",
        "retained-Run": "NOT RUN; P4 reference checkers are no-regression evidence only and are not shown to reach I1",
        "promotion": "no result is promoted between standings",
    },
    "pins": {"stalePinRows": p5["stalePinRows"], "rows": p5["pinRows"], "pinAdditionOwed": False, "newFiles": []},
    "dependenciesOnOtherOwners": [{
        "file": "docs/coop/design-corrections/foundation/incoming-search.schema.v1.json",
        "selector": "joins item: 'scopeRefs is the exact union of this providerClosure's owned scopes ...; untagged scopes fall back to all S scopes'",
        "why": "describes no admitted input; the contract now says so. Owner should drop the fallback clause. Not edited (not an owned file)."}],
    "remainingIssues": [
        "MUST-34-01 reachability beyond synthetic atom-api + stock schema is undemonstrated (no closed enumeration admission, no retained Run).",
        "A scope lacking enumeratorClosure that is neither named by an admitted attestation nor consumed by the evaluated "
        "atom is not carrier-validated at the atom API; it contributes nothing to any value (decisions.A-12.globalAdmission).",
        "The untagged-scope branches in _incoming_groups/_admit_incoming_searches are kept as defensive code; for admitted scopes they are unreachable.",
        "Unknown-family obligations are measured only with an unregistered languageMode the enumeration-plan schema refuses (synthetic-only).",
        "15 pin rows are stale; root reseals. The six broad groups and integrated suites were not run.",
        "root-source35-preparation.v1 had 3 files modified after this runtime began; no command here targeted it and they were not read.",
    ],
    "probeErrorsKept": [
        "p1-must-matrix-frozen34: TypeError sorting None with str in cause tuples (probe bug); rerun as .2",
        "p1-must-matrix-frozen34.2: order harness reversed schema-sorted plan cells, corrupting cellOrdinal joins; its "
        "multiProvider distinctResults=2 is a probe artefact, not a model finding; rerun as .3",
        "Bash scan over docs/ for the configuration schema was denied by the permission mode; replaced by Grep",
    ],
    "commands": commands,
    "grantsNothing": True,
}
text = json.dumps(doc, indent=1, default=str) + "\n"
(HERE / "review.json").write_text(text)
print(json.dumps({"wrote": str(HERE / "review.json"), "sha256": hashlib.sha256(text.encode()).hexdigest(),
                  "commands": len(commands), "referencesChangedCells": len(ref_delta),
                  "importsChangedCells": len(imp_delta)}, indent=1))
