"""Build v2 assessment.json and changed-file-handoff.json from the retained receipts."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE / "probes" / "receipts"
SRC = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source")
V1 = Path("/tmp/opensip-design-corrections/claude-atom-cause-author.v1")


def js(label, name="stdout.txt"):
    return json.loads((R / label / name).read_text())


before = {r["path"]: r for r in json.loads((HERE / "before-hashes.json").read_text())}
after = {r["path"]: r for r in json.loads((HERE / "after-hashes.json").read_text())}
custody = js("b6-custody-pins")
repro_before, repro_after = js("b1-repro-before"), js("b1-repro-after")
prelude = js("b2-prelude-cross-family.2")
discriminate = js("b3-controls-discriminate")
realrun = js("b4-realrun-after-v2")
focused = js("b5-focused-checks")
citations = js("b7-clause-citations")
atoms = js("check-atoms-v2")
v1_atoms = json.loads((V1 / "probes/receipts/check-atoms-final/stdout.txt").read_text())

PURPOSE = {
    "docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md":
        "Section 4 restructured into a shared prelude (P1 unavailable-binding scan, P2 no-owed-"
        "binding return taken by BOTH endpoints) plus renumbered outgoing steps 1-4 and a "
        "conditional incoming claim; incoming now names both cross-family routes (unavailable/null "
        "and available/S) and the blocking same-family unavailable case; selection order now "
        "requires dedup-and-sort of the COMBINED Coverage list after pairing; the dependency fold "
        "now spells out whole-record replacement, tie retention, unfolded first-record fields, "
        "ordered union and the whole typed carrier; a new paragraph fixes the universe "
        "optional-vs-required representation boundary; the unsupported partition-census rationale "
        "is removed and 'one per unpaired scope' is scoped to accumulation before canonical dedup.",
    "docs/coop/design-corrections/foundation/atom_model.v1.py":
        "_unique_pairs now deduplicates AND sorts ascending by Coverage id, and "
        "_coverages_for_current_source routes its combined paired list through it, so the list the "
        "fold reads is ascending even when a lower scope id carries a higher Coverage id. This is "
        "the only behaviour change in v2.",
    "docs/coop/design-corrections/foundation/check-atoms.v1.py":
        "Five controls for the shared prelude return, both incoming cross-family shapes, the "
        "blocking same-family unavailable case, same-kind multi-scope selection with a "
        "deliberately reversed scope-vs-coverage mapping, and whole-record fold replacement with "
        "tie retention.",
}

changed = [{
    "path": p,
    "v1FinalSha256": before[p]["sha256"],
    "v2Sha256": after[p]["sha256"],
    "frozen33Sha256": before[p]["frozen33Sha256"],
    "v1FinalBytes": before[p]["bytes"],
    "v2Bytes": after[p]["bytes"],
    "beforeImage": before[p]["image"],
    "afterImage": after[p]["image"],
    "purpose": PURPOSE[p],
} for p in sorted(after)]

handoff = {
    "standing": "AUTHOR/REFERENCE handoff of a bounded correction to the v1 atom-cause handoff. "
                "Not an acceptance, qualification or approval. No frozen33, live-repository, "
                "history, pin-ledger, planning-layer or prior-v1 edit. Root rebinds pins.",
    "authorOrigin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "runtime": str(HERE),
    "isolatedSourceCopy": str(SRC),
    "baselines": {"v1Final": str(V1 / "after-hashes.json"),
                  "frozen33": "/tmp/opensip-design-corrections/candidate-subject.v33"},
    "custody": custody["custody"],
    "changedFiles": changed,
    "stalePinEntries": custody["pinEntries"],
    "stalePinCount": custody["staleCount"],
    "newCheckerFilesAdded": custody["newCheckerFilesAdded"],
    "pinAdditionOwed": False,
    "referenceRunnerWiring": custody["referenceRunnerWiring"],
    "pinLedgersEdited": [],
}
(HERE / "changed-file-handoff.json").write_text(json.dumps(handoff, indent=2) + "\n")

by_case = {}
for row in discriminate["results"]:
    by_case.setdefault(row["case"], {})[row["model"]] = row["ok"]

assessment = {
    "standing": handoff["standing"],
    "interpreter": "/tmp/opensip-architecture-review-env/bin/python -I -B",
    "receiptsRoot": str(R),
    "receiptLabels": sorted(p.name for p in R.iterdir()),
    "custody": custody["custody"],
    "changedFiles": [{k: c[k] for k in ("path", "v1FinalSha256", "v2Sha256")} for c in changed],
    "rootIssues": {
        "1-shared-no-owed-binding-return": {
            "alreadyFixedInV1": False,
            "kind": "prose",
            "evidence": "b2-prelude-cross-family.2",
            "observed": prelude[0],
            "fix": "Section 4 shared prelude P1/P2; incoming claim made conditional on it.",
        },
        "2-incoming-cross-family-both-shapes": {
            "alreadyFixedInV1": False,
            "kind": "prose",
            "evidence": "b2-prelude-cross-family.2",
            "observedBothShapes": prelude[1]["target"]["causes"],
            "observedSameFamilyUnavailable": prelude[2],
            "fix": "Both routes named and retained; same-family unavailable stated blocking "
                   "incoming and silent outgoing.",
        },
        "3-selection-order-through-scope-pairing": {
            "alreadyFixedInV1": False,
            "kind": "reference defect + prose",
            "reproBefore": {"receipt": "b1-repro-before",
                            "sourceSha256": repro_before["sourceSha256"],
                            "mismatchPresent": repro_before["MISMATCH_PRESENT"],
                            "cases": repro_before["cases"]},
            "reproAfter": {"receipt": "b1-repro-after",
                           "sourceSha256": repro_after["sourceSha256"],
                           "mismatchPresent": repro_after["MISMATCH_PRESENT"],
                           "cases": repro_after["cases"]},
            "fix": "_unique_pairs dedups and sorts ascending by Coverage id; "
                   "_coverages_for_current_source routes its combined paired list through it. "
                   "Contract publishes sort-after-pairing-and-dedup.",
            "standing": "Synthetic helper-only inputs. A specification/reference mismatch at a "
                        "helper boundary, NOT a claimed admitted full-Run failure.",
        },
        "4-whole-record-fold-and-ties": {
            "alreadyFixedInV1": False,
            "kind": "prose",
            "control": "test_dep_fold_replaces_whole_records_and_keeps_ties",
            "fix": "Field-by-field fold rule: whole-record resolutionCompleteness/closedWorld "
                   "replacement on strictly worse rank, ties retain the first whole record, "
                   "ordered derivation union, whole typed carrier, and remaining fields "
                   "(resolution, rungUnavailableBecause) from the first partition.",
        },
    },
    "smallerCorrections": {
        "universeRepresentation": "AtomCauseV1.universe is optional+nullable and the reference "
                                  "omits the key; the composition/replay projection writes "
                                  "evaluation-deficiency.universe, which is required+nullable, so "
                                  "an omitted key becomes an explicit null. Section 4's "
                                  "'universe: null' names that logical/projected value. Schemas "
                                  "and recipe unchanged.",
        "removedUnsupportedRationale": "The 'asserting a partition census' justification is "
                                       "deleted; step 3 now states only that evaluation stops "
                                       "before any paired sibling's Coverage is evaluated.",
        "onePerUnpairedScope": "Restated as accumulation before the canonical dedup/order of "
                               "section 7 and the composition Cset law.",
    },
    "v1ReportScopeCorrections": {
        "retainedCorpusClaim": "v1's 'no fixture in the retained corpus reaches it' is "
                               "UNSUPPORTED and is withdrawn. What was executed is one retained "
                               "reference fixture Run plus the affected checks, and those did not "
                               "demonstrate a full-Run failure.",
        "a2SurfacingLabel": "a2-surfacing builds SYNTHETIC ATOM INPUTS and reads the atom result. "
                            "It is atom-cause surfacing, not a proof bundle and not an admitted "
                            "retained Run.",
        "kitCensus": "v1's 169-file token census is a current-contract .md/.json census of this "
                     "tree, NOT the 102-file blind kit, and token presence alone is not "
                     "implementability. v2 replaces it with clause-location evidence for the "
                     "amendment's load-bearing citations only (b7-clause-citations).",
        "observedCounts": {"v1AtomCases": "70 -> 76", "v2AtomCases": "76 -> 81"},
        "samplingVsFixture": "Randomized process sampling of synthetic inputs (v1 a1/a2/a4) is "
                             "reported separately from the retained real fixture Run (v1 a3/a9, "
                             "v2 b4), which was stable in every execution.",
        "v1EvidencePreserved": True,
    },
    "controls": {
        "atomCases": {"v1Final": v1_atoms["passed"], "v2": atoms["passed"]},
        "atomResult": {"ok": atoms["ok"], "passed": atoms["passed"], "failed": atoms["failed"]},
        "added": [c for c in discriminate["v2Added"]],
        "discriminatesV1Final": discriminate["discriminatesV1Final"],
        "discriminatesFrozen33": discriminate["discriminatesFrozen33"],
        "passesAllThreeModels": discriminate["passesAllThree"],
        "honestNote": "Only issue 3 changed behaviour, and only its control discriminates the "
                      "v1->v2 delta. The controls for issues 1, 2 and 4 pass on all three models "
                      "because those were defects in the v1 PROSE, not in the reference; they "
                      "keep the corrected prose and the reference from drifting apart.",
        "whiteBoxNote": "test_dep_fold_replaces_whole_records_and_keeps_ties asserts against "
                        "_conservative_entry directly; the folded record's fields are not "
                        "otherwise observable, and they are exactly what root asked to make "
                        "implementable without Python.",
        "temporaryBaselineRemoved": discriminate["tempBaselineRemoved"],
    },
    "focusedChecks": {
        "justification": "_unique_pairs and _coverages_for_current_source changed, so every "
                         "checker importing atom_model.v1.py (directly or via "
                         "evaluator_replay_model.v3.py / provider_attribution_return_model.v2.py) "
                         "is affected. The contract .md is executed by no checker.",
        "broadGroupsRun": False,
        "atoms": {"exit": 0, "passed": atoms["passed"], "failed": atoms["failed"],
                  "receipt": "check-atoms-v2"},
        "others": focused["checks"],
        "allExitZero": focused["allExitZero"],
        "allIdenticalToV1Final": focused["allIdenticalToV1Final"],
    },
    "retainedFixtureRun": {
        "receipt": "b4-realrun-after-v2",
        "atomModelSha256": realrun["atomModelSha256"],
        "processes": realrun["runs"],
        "distinctRunIds": realrun["distinctRunIds"],
        "distinctProofSha256": realrun["distinctProofSha256"],
        "stableAcrossProcesses": realrun["stableAcrossProcesses"],
        "sample": realrun["sample"],
        "completeRunParityClaimed": False,
        "note": "One retained reference fixture, replayed end to end. Not the retained corpus.",
    },
    "clauseCitations": {
        "receipt": "b7-clause-citations",
        "allResolved": citations["allResolved"],
        "unresolved": citations["unresolved"],
        "scope": citations["standing"],
    },
    "pins": {
        "staleCount": custody["staleCount"],
        "newCheckerFilesAdded": custody["newCheckerFilesAdded"],
        "pinAdditionOwed": False,
        "referenceRunnerWiring": custody["referenceRunnerWiring"],
        "ledgersEdited": [],
    },
    "limitations": [
        "Not an acceptance, qualification or approval; full reference validation and independent "
        "reviews remain pending.",
        "One retained fixture Run was replayed; the retained corpus was not.",
        "Root's counterexample and its repro are synthetic helper-only inputs, not native-schema "
        "admitted Coverage, not a proof and not an admitted Run.",
        "b7-clause-citations covers the amendment's load-bearing citations only; it is not a kit "
        "census and not the 102-file blind kit.",
        "The six broad reference groups were not run here, by instruction.",
        "ViewEntryV3.coverage is a two-member enum while _conservative_entry ranks an intermediate "
        "'partial' used by pre-existing checks; unreachable on admitted input, reported in v1, "
        "still deliberately unchanged.",
        "No new cause tokens or public fields; AtomCauseV1 / evaluation-deficiency schemas and the "
        "projection recipe are untouched.",
    ],
}
(HERE / "assessment.json").write_text(json.dumps(assessment, indent=2) + "\n")

print(json.dumps({
    "wrote": [str(HERE / "assessment.json"), str(HERE / "changed-file-handoff.json")],
    "assessmentSha256": hashlib.sha256((HERE / "assessment.json").read_bytes()).hexdigest(),
    "handoffSha256": hashlib.sha256((HERE / "changed-file-handoff.json").read_bytes()).hexdigest(),
    "changedFiles": len(changed),
    "stalePins": custody["staleCount"],
    "atomCases": atoms["passed"],
    "discriminatesV1Final": discriminate["discriminatesV1Final"],
}, indent=2))
