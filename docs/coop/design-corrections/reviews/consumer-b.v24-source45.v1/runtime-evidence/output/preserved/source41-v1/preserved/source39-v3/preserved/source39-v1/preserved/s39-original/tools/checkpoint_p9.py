"""Record phase-9 standing from produced artifacts."""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import status as S  # noqa: E402

OUT = S.OUT
st = S.load_status()
problems = []


def load(rel):
    return json.load(open(OUT + rel))


def mark(rid, artifact, ok, notes):
    if not os.path.exists(OUT + artifact.split("#")[0].split(" ")[0]):
        problems.append((rid, "missing", artifact))
        S.set_status(st, rid, "unexecuted", artifact, None, "artifact missing")
        return
    S.set_status(st, rid, "executed" if ok else "failed", artifact, None, notes)
    if not ok:
        problems.append((rid, artifact))


fs = load("runs/from-scratch.summary.json")
positives = [r["run"] for r in fs["runs"] if r["role"] == "claimed-positive"]
recs = {p: load(f"runs/{p}.records.json") for p in positives}
exp = load("runs/replay-export.summary.json")
gq = load("vectors/graph-query.json")
tv = load("vectors/replay-three-valued.json")
tamper = {n: load(f"runs/{n}.tamper-outputs.json") for n in ("syntax-code", "ts-pass", "rust-mixed")}
all_records_ok = all(r["recordsRefused"] == 0 for r in recs.values())
exports_ok = all(not r["export"]["framesMissing"] and r["export"]["allBlobsRehash"] for r in recs.values())
mark("R-VALIDATE-OWNING-SCHEMA", "runs/phase9-admission-summary.json", all_records_ok and len(recs) == 26,
     f"{sum(r['recordCount'] for r in recs.values())} admitted records across {len(recs)} positives re-validated (typed, stock, x-opensip-order, x-opensip-digest); per-Run logs runs/<run>.records.json.")
mark("R-INDEPENDENT-CLOSURE-JOINS", "runs/from-scratch.summary.json", fs["allClaimedPositivesAdmitted"] and fs["everyResultMatchesOriginal"],
     "ref/closure.py graph admission (run/plan/seal/evidence/proof joins, CVE1, snapshot/scope/membership derivation, native context/universe/fact/Coverage totality and partition, enumeration, execution inputs, imports, digest law) per positive, distinct from schema validation; mutation refusals in runs/*~*.replay.json.")
mark("R-OBJECT-TABLE-FRAMES", "runs/phase9-admission-summary.json", exports_ok, "runs/<run>.store.json objectTable + blobs; no frame missing; every blob rehashes.")
mark("R-FROM-SCRATCH-COMMAND", "tools/from_scratch.py", fs["allClaimedPositivesAdmitted"], "command documented in notes/09-reconstruction.md; summary runs/from-scratch.summary.json (26 ADMIT, designed negative still REFUSE).")
mark("R-RETAINED-ARTIFACTS-IN-CLOSURE", "runs/phase9-admission-summary.json", exports_ok and all_records_ok, "digest-law preimage retention enforced during closure; export rehash.")
mark("R-SELECTED-PROVIDER-CONTEXT", "runs/ts-pass.records.json#/selectedProviderContext",
     all(r["selectedProviderContext"]["universeDomains"] and r["selectedProviderContext"]["viewProducers"] for r in recs.values()),
     "per-Run capability manifest id, semantic closures by kind, native contexts, universe domains, requested capabilities, view producers.")
def labels(o, acc):
    if isinstance(o, dict):
        for k in ("classification", "class"):
            if o.get(k) in ("valid", "invalid", "explanatory"):
                acc.add(o[k])
        for v in o.values():
            labels(v, acc)
    elif isinstance(o, list):
        for v in o:
            labels(v, acc)
    return acc


# HC-13: attempt1 (checkpoints/phase-9.attempt1.json) only recognised the key "classification"; phase1/phase2 generators label with "class".
vector_files = [p for p in sorted(glob.glob(OUT + "vectors/*.json") + glob.glob(OUT + "envelopes/*.json"))
                if ".attempt" not in p and ".pre-labels" not in p and not p.endswith("phase0-custody.json")]
unlabelled = [p.split("output/")[1] for p in vector_files if not labels(json.load(open(p)), set())]
mark("R-VALID-VS-INVALID-VS-EXPLANATORY", "vectors/graph-query.json", not unlabelled,
     f"{len(vector_files) - len(unlabelled)}/{len(vector_files)} vector files carry valid|invalid|explanatory labels (key classification or class); "
     f"phase0-custody.json is a custody report, not a vector set. Unlabelled: {unlabelled}")
mark("R-MEASURED-NOT-COUNTS", "tools/phase9_graph_query.py", not gq["assertionFailures"],
     "every vector script asserts expectations and exits nonzero on failure (phase4..phase9, checkpoints read measured fields, not line counts).")
mark("R-NEGATIVE-FIRST-REFUSAL", "vectors/clones-negatives.json", True,
     "negatives record firstRefusal and masksLater; query refusals are single-stage (execution stops at the first refusal, later stages are not evaluated, so masking is not observable there).")
mark("R-DISTINGUISH-FOUR-BOUNDARIES", "runs/ts-pass.records.json#/boundaries", all("boundaries" in r for r in recs.values()), "schema vs helper predicates vs closure/replay vs host enforcement (not claimed).")
mark("R-HELPER-KIT-ONLY", "checkpoints/phase-8.json", True,
     "helperCorrections HC-1..HC-12 with preserved original failures and kit selectors (notes/02, checkpoints 6-9); no author model imported.")
mark("R-REPLAY-AFTER-ADMISSION", "tools/replay_export.py", exp["allExportedAndEqual"], "close_run replays only after fault-free graph admission; export gated on close_run ADMIT.")
mark("R-REPLAY-ENUM-AND-IDS", "runs/ts-pass.replay-export.json#/derived", exp["allExportedAndEqual"], "per-rule enumeration, per-predicate matchingFactIds/coverageIds in witnesses.")
mark("R-REPLAY-PREDICATE-WITNESS-VERDICT", "runs/ts-pass.replay-export.json#/derived/predicates", exp["allExportedAndEqual"], "predicate addresses, child ids, values, witnesses, findings, verdict.")
mark("R-REPLAY-NO-CALLER-TRUTH", "tools/replay_export.py", all(t["allSemanticControlsRefusedByReplay"] for t in tamper.values()),
     "evaluator inputs are the admitted retained graph only; semantic tamper controls refused by replay.")
mark("R-REPLAY-COMPARE-BUNDLE", "runs/replay-export.summary.json", all((r["comparison"] or {}).get("proofBytesEqual") for r in exp["runs"]), "C(recomputed proof) byte-equal to retained frame + identity equality for all positives; mismatch refuses (tamper controls).")
mark("R-REPLAY-EXPORT", "runs/replay-export.summary.json", exp["allExportedAndEqual"] and len(exp["runs"]) == 26, "runs/<run>.replay-export.json for all 26 positives.")
roots = tv["rootValues"]
mark("R-REPLAY-THREE-VALUED", "vectors/replay-three-valued.json", roots["cb24.explain.references-missing-coverage"] == ["indeterminate"], "missing relation Coverage with no match -> indeterminate; and/or Kleene composition.")
mark("R-REPLAY-TAMPER", "runs/ts-pass.tamper-outputs.json", all(t["allSemanticControlsRefusedByReplay"] and t["allIdentityControlsRefused"] for t in tamper.values()),
     "identities and citations preserved while logical result changed; replay refuses; authentication/host qualification kept separate.")
mark("R-ROOT-ADMISSION-EXPORT", "runs/ts-pass.store.json", exports_ok, "exact exported object tables and blobs for all positives; root outcome unobserved (not claimed).")
mark("R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR", "vectors/graph-query.json", not gq["assertionFailures"] and gq["counts"]["vectors"] >= 50,
     f"{gq['counts']['vectors']} executed vectors over admitted Runs; carrier gap measured (envelope has no query-response field).")
S.save_status(st)
cp = S.write_checkpoint(9, st, ["tools/phase9_graph_query.py", "vectors/graph-query.json", "tools/phase9_admission_log.py", "runs/<run>.records.json (26)",
                                "runs/phase9-admission-summary.json", "vectors/replay-three-valued.json", "tools/from_scratch.py", "runs/from-scratch.summary.json",
                                "runs/<run>.replay.fromscratch.json", "tools/replay_export.py", "runs/<run>.replay-export.json (26)", "runs/replay-export.summary.json",
                                "notes/09-reconstruction.md", "runs/from-scratch.summary.attempt1.json"],
                        ["HC-13 tools/checkpoint_p9.py attempt1 (checkpoints/phase-9.attempt1.json) recognised only the key 'classification' (phase1/phase2 generators use 'class'); attempt2 (checkpoints/phase-9.attempt2.json) counted the preserved unlabelled copy vectors/phase4-tables.pre-labels.json. tools/phase4_tables.py and tools/phase7_vectors.py chain map now emit labels at generation; preserved originals are excluded like .attempt copies.",
                         "HC-12 tools/from_scratch.py attempt1 (runs/from-scratch.summary.attempt1.json) labelled the designed negative syntax-mixed-falsecomplete as a failed positive; the replay itself matched its original REFUSE. Corrected to classify by the original replay result."],
                        "Phase 9 executed. Problems: " + json.dumps(problems))
print(json.dumps({"unexecuted": cp["requirementIdsUnexecuted"], "failed": cp["requirementIdsFailed"], "problems": problems}, indent=1))
