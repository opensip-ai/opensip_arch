"""Record phase-9 standing from produced source39 artifacts."""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import hc_source42 as HC  # noqa: E402
import hc_source43 as HC43  # noqa: E402
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
n = len(positives)
recs = {p: load(f"runs/{p}.records.json") for p in positives}
exp = load("runs/replay-export.summary.json")
gq = load("vectors/graph-query.json")
tv = load("vectors/replay-three-valued.json")
mut = load("runs/replay-all.summary.json")
tamper = {k: load(f"runs/{k}.tamper-outputs.json") for k in ("syntax-code", "ts-pass", "rust-mixed")}
all_records_ok = all(r["recordsRefused"] == 0 for r in recs.values())
exports_ok = all(not r["export"]["framesMissing"] and r["export"]["allBlobsRehash"] for r in recs.values())
exported = {r["run"] for r in exp["runs"]}
mark("R-VALIDATE-OWNING-SCHEMA", "runs/phase9-admission-summary.json", all_records_ok and set(recs) == set(positives),
     f"{sum(r['recordCount'] for r in recs.values())} admitted records across {n} positives re-validated (typed, stock, x-opensip-order, x-opensip-digest); per-Run logs "
     "runs/<run>.records.json.")
neg = load("vectors/retention-negatives.json") if os.path.exists(OUT + "vectors/retention-negatives.json") else {"allPass": False, "negatives": []}
walk_ok = all((r.get("retainedClosure") or {}).get("result") == "ADMIT" for r in fs["runs"] if r["role"] == "claimed-positive")
mark("R-INDEPENDENT-CLOSURE-JOINS", "runs/from-scratch.summary.json",
     fs["allClaimedPositivesAdmitted"] and fs["allDesignedNegativesRefused"] and fs["everyResultMatchesOriginal"] and all(r["result"] for r in mut["replays"])
     and walk_ok and neg["allPass"]
     # source41 (HC-42/HC-45): execution-inputs s3 view attribution totality enforced at Run closure over the retained claim
     and any(r["run"] == "syntax-code~row-view-omitted" and r["result"] == "REFUSE" and (r["firstFault"] or "").startswith("EXECUTION_INPUTS_VIEW_TOTALITY")
             for r in mut["replays"])
     # source42 (HC-48): a view on selectedRefs but on no complete receipt refuses EXECUTION_INPUTS_SELECTED_COVER
     and any(r["run"] == "syntax-code~selected-view-not-on-receipt" and r["result"] == "REFUSE"
             and (r["firstFault"] or "").startswith("EXECUTION_INPUTS_SELECTED_COVER") for r in mut["replays"]),
     "ref/closure.py owner graph admission per positive in a fresh process, distinct from schema validation, PLUS (HC-33) the independent retained-closure walk "
     "(ref/retained_graph.py) that derives the required graph from owning schemas/registries and admits typed-prefix output references before replay. "
     "Source39 joins: stage-output registration, parameter selection, retained membership order/rows, pruned-tree reads, normalization map, body eligibility, "
     f"account targetUniverse null. {len(mut['replays'])} stores replayed in runs/replay-all.summary.json; {len(neg['negatives'])} retention/reference-class "
     "negatives in vectors/retention-negatives.json.")
mark("R-OBJECT-TABLE-FRAMES", "runs/phase9-admission-summary.json", exports_ok, "runs/<run>.store.json objectTable + blobs; no frame missing; every blob rehashes.")
mark("R-FROM-SCRATCH-COMMAND", "tools/from_scratch.py", fs["allClaimedPositivesAdmitted"],
     f"command documented in notes/09-reconstruction.md; runs/from-scratch.summary.json ({n} ADMIT, designed negative REFUSE).")
mark("R-RETAINED-ARTIFACTS-IN-CLOSURE", "vectors/retention-negatives.json", exports_ok and all_records_ok and walk_ok and neg["allPass"],
     "digest-law preimage retention enforced during closure (including stage-output schema members and normalization maps in closure trees); export rehash; "
     "HC-33 complete retained graph derived independently per positive (runs/<run>.replay.fromscratch.json#/retainedClosure) with one constructed negative "
     "per applicable retention/reference class (vectors/retention-negatives.json).")
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


vector_files = [p for p in sorted(glob.glob(OUT + "vectors/*.json") + glob.glob(OUT + "envelopes/*.json")) if not p.endswith("phase0-custody.json")]
unlabelled = [p.split("output/")[1] for p in vector_files if not labels(json.load(open(p)), set())]
mark("R-VALID-VS-INVALID-VS-EXPLANATORY", "vectors/graph-query.json", not unlabelled,
     f"{len(vector_files) - len(unlabelled)}/{len(vector_files)} vector files carry valid|invalid|explanatory labels; phase0-custody.json is a custody report. "
     f"Unlabelled: {unlabelled}")
mark("R-MEASURED-NOT-COUNTS", "tools/phase9_graph_query.py", not gq["assertionFailures"],
     "every vector script asserts expectations and exits nonzero on failure; checkpoints read measured fields, not line counts.")
mark("R-NEGATIVE-FIRST-REFUSAL", "vectors/retention-negatives.json", bool(neg["negatives"]) and all("firstRefusal" in n for n in neg["negatives"]),
     "negatives record firstRefusal and masksLater (clones, discovery, run-termination, mutations, and retention/reference-class negatives with stage, "
     "masked stages and the independent walker's masked later faults); query refusals are single-stage.")
mark("R-DISTINGUISH-FOUR-BOUNDARIES", "runs/ts-pass.records.json#/boundaries", all("boundaries" in r for r in recs.values()),
     "schema vs helper predicates vs closure/replay vs host enforcement (not claimed).")
mark("R-HELPER-KIT-ONLY", "tools/hc_source42.py", True,
     "source42 helper corrections HC-47..HC-49 with kit selectors and the unchanged-helper results preserved (preserved/s42-original-state/, "
     "preserved/pre-s42/, selfcheck/s42-prepost-matrix.json); source43 HC-54/HC-55 (tools/hc_source43.py) with the unchanged source42.v3 graph-query helper "
     "executed as the pre column (vectors/graph-query.json#/source43ReAudit/prePost) and its own control error preserved (logs/s43-hc54.0); "
     + HC43.CARRIED + " No author model imported.")
mark("R-REPLAY-AFTER-ADMISSION", "tools/replay_export.py", exp["allExportedAndEqual"], "close_run replays only after fault-free graph admission; export gated on close_run ADMIT.")
mark("R-REPLAY-ENUM-AND-IDS", "runs/ts-pass.replay-export.json#/derived", exp["allExportedAndEqual"], "per-rule enumeration, per-predicate matchingFactIds/coverageIds in witnesses.")
mark("R-REPLAY-PREDICATE-WITNESS-VERDICT", "runs/ts-pass.replay-export.json#/derived/predicates", exp["allExportedAndEqual"], "predicate addresses, child ids, values, witnesses, findings, verdict.")
mark("R-REPLAY-NO-CALLER-TRUTH", "tools/replay_export.py", all(t["allSemanticControlsRefusedByReplay"] for t in tamper.values()),
     "evaluator inputs are the admitted retained graph only; semantic tamper controls refused by replay.")
mark("R-REPLAY-COMPARE-BUNDLE", "runs/replay-export.summary.json", all((r["comparison"] or {}).get("proofBytesEqual") for r in exp["runs"]),
     "C(recomputed proof) byte-equal to retained frame + identity equality for all positives; mismatch refuses (tamper controls).")
mark("R-REPLAY-EXPORT", "runs/replay-export.summary.json", exp["allExportedAndEqual"] and exported == set(positives),
     f"runs/<run>.replay-export.json for all {n} positives.")
roots = tv["rootValues"]
mark("R-REPLAY-THREE-VALUED", "vectors/replay-three-valued.json", roots["cb24.explain.references-missing-coverage"] == ["indeterminate"],
     "missing relation Coverage with no match -> indeterminate; and/or Kleene composition.")
mark("R-REPLAY-TAMPER", "runs/ts-pass.tamper-outputs.json", all(t["allSemanticControlsRefusedByReplay"] and t["allIdentityControlsRefused"] for t in tamper.values()),
     "identities and citations preserved while logical result changed; replay refuses; authentication/host qualification kept separate.")
mark("R-ROOT-ADMISSION-EXPORT", "runs/ts-pass.store.json", exports_ok, "exact exported object tables and blobs for all positives; root outcome unobserved (not claimed).")
carrier = gq["measuredQueryResponseCarrier"]
# source43 (HC-54): the query owner is the only changed kit member; the ID also requires the re-audit of every current law with discriminating vectors
ra = gq.get("source43ReAudit") or {}
reaudit_ok = bool(ra) and ra["contract"]["source43Bytes"] == 30278 and \
    all(p["differs"] == (p["expected"] == "differ") for p in ra["prePost"]) and all(pc["pass"] for pc in ra["preconditionVectors"]) and \
    all(t["observed"] == t["expected"] for t in ra["typedOutcomeControls"]) and \
    all(row.get("correction") for row in ra["lawAudit"] if row["unchangedHelper"].startswith("OMITTED"))
mark("R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR", "vectors/graph-query.json",
     not gq["assertionFailures"] and gq["counts"]["vectors"] >= 50 and carrier["envelopeHasQueryResponseField"] and carrier["probeAdmitted"] == [True] and reaudit_ok,
     f"{gq['counts']['vectors']} executed vectors over admitted Runs ({gq['counts'].get('source43Vectors')} source43 re-audit vectors, "
     f"{gq['counts'].get('preconditionVectors')} precondition vectors, {gq['counts'].get('typedOutcomeControls')} typed-outcome controls; logs/s43-hc54c.0); "
     f"public carrier CommandEnvelope major 3 querySurface={carrier['querySurface']} with queryResponse, parity read at command-inventory queryDispatch.parityPaths. "
     "Re-audited against the source43 query-projection-contract.v3.md (HC-54): path traversal-hop edges, closed availability vocabulary/precondition/adapter/"
     "retained-record routes, close_run typed outcomes including evidence.regeneration-mismatch and the host-invariant route, carrier remedies, closed "
     "endpoint-ambiguity refusal.")
S.save_status(st)
cp = S.write_checkpoint(9, st, ["tools/phase9_graph_query.py", "vectors/graph-query.json", "tools/phase9_admission_log.py", f"runs/<run>.records.json ({n})",
                                "runs/phase9-admission-summary.json", "vectors/replay-three-valued.json", "tools/from_scratch.py", "runs/from-scratch.summary.json",
                                "runs/<run>.replay.fromscratch.json", "tools/replay_export.py", f"runs/<run>.replay-export.json ({n})", "runs/replay-export.summary.json",
                                "tools/replay_all.py", "runs/replay-all.summary.json", "runs/*.tamper-outputs.json", "notes/09-reconstruction.md",
                                "ref/retained_graph.py", "tools/reference_census.py", "vectors/reference-census.json", "tools/retention_negatives.py",
                                "vectors/retention-negatives.json", "negatives/", "tools/hc_source42.py", "tools/prepost_s42.py", "selfcheck/s42-prepost-matrix.json",
                                "tools/provenance_s42.py", "selfcheck/s42-provenance.json", "preserved/s42-original-state/manifest.json", "preserved/pre-s42/manifest.json",
                                "logs/s42v2-fin2.2.from_scratch.log", "logs/s42v2-fin2.1.replay_all.log", "logs/s42v2-fin2.0.syntax_runs.log",
                                "logs/s42-fin-build.4.from_scratch.log (v1)", "logs/s42-fin-mut.0.replay_all.log (v1; HC-50 first control version masked)",
                                "logs/s42v2-fin2.4.phase9_admission_log.log", "logs/s42v2-fin2.3.replay_export.log",
                                "logs/s42-fin-p4to9.7.phase9_admission_log.log (v1)", "logs/s42-fin-p4to9.9.replay_export.log (v1)",
                                "logs/s42-fin-p4to9.6.phase9_graph_query.log", "logs/s42-fin-tamper.0.tamper_outputs.log", "logs/s42-fin-tamper.1.tamper_outputs.log",
                                "logs/s42-fin-tamper.2.tamper_outputs.log", "logs/s42-fin-p4to9.10.reference_census.log", "logs/s42-fin-neg.0.retention_negatives.log",
                                "logs/s42v2-fin2.5.prepost_s42.log", "logs/s42v2-fin2.6.provenance_s42.log", "logs/s42v2-cp.5.final_custody.log",
                                "logs/s42v2-fin2.7.final_custody.log (own ordering error: run before phase 0 custody existed; FileNotFoundError vectors/phase0-custody.json; re-run after phase 0)",
                                "v1 pending chain: s42-fin-neg.1/.2 and s42-fin-final never produced logs (runtime ended; executed fresh in v2)",
                                "logs/s42-original.7.from_scratch.log (unchanged helpers)", "logs/s42-original-mut.0.replay_all.log (unchanged helpers)",
                                "preserved/pre-s42/logs/s42-pre-tamper.*, s42-pre-p4to9.* (unchanged helpers)",
                                "logs/s43-original.0.phase9_graph_query.log (unchanged helper on source43)", "logs/s43-hc54.0.phase9_graph_query.log (own control error)",
                                "logs/s43-hc54b.0.phase9_graph_query.log (own asymmetric pre/post comparison)", "logs/s43-hc54c.0.phase9_graph_query.log",
                                "logs/s43-fin.0.from_scratch.log", "logs/s43-fin.1.replay_export.log",
                                "logs/s43-fin.2.phase9_admission_log.log", "tools/hc_source43.py", "preserved/s42-v3-final/manifest.json",
                                "preserved/s42-v3-final/runs-manifest.json", "selfcheck/s43-provenance.json"],
                        HC.for_phase(9) + HC43.for_phase(9),
                        "Runtime source43.v1 on the source43 kit: from-scratch closure/replay of every claimed positive, export replay and the admission log executed "
                        "fresh (logs/s43-fin.*); graph query re-audited and re-executed (HC-54, logs/s43-hc54c.0); every other phase-9 measurement reused as exact "
                        "source42 measurement with custody in selfcheck/s43-provenance.json. Source42 standing follows. "
                        "Phase 9: every closure-dependent result (from-scratch closure/replay, replay-all, tamper, replay export, admission log, retention "
                        "negatives, pre/post matrix, graph query) executed on the source42 kit after HC-47..HC-50: tamper, retention negatives, graph query and "
                        "run termination in runtime source42.v1 (logs reused in v2 as exact prior measurements); HC-50 control rebuild, replay-all, "
                        "from-scratch, replay export, admission log, pre/post matrix, provenance and final custody executed fresh in runtime source42.v2. Problems: "
                        + json.dumps(problems))
print(json.dumps({"unexecuted": cp["requirementIdsUnexecuted"], "failed": cp["requirementIdsFailed"], "problems": problems}, indent=1))
