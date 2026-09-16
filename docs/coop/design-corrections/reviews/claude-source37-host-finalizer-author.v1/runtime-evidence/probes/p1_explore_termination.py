"""P1 (exploration): derived whole-Run terminations over actually closed Runs, including the new fixture knobs.

Loads THIS runtime's source copy. For each case: close_run admission, the retained population summary, the
condition list, the derivation, route drift, and permutation invariance against the raw D9 reducer.
Refusals are recorded, never swallowed. Writes nothing into any tree; stdout only.
"""
import importlib.util
import json
import sys
import traceback
from pathlib import Path

SRC = Path("/private/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v1/source")
FOUNDATION = SRC / "docs/coop/design-corrections/foundation"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


SR = load("p1_semantic_replay", FOUNDATION / "check-semantic-replay.v3.py")
T = load("p1_run_termination", FOUNDATION / "run_termination_model.v1.py")
S = SR.S


def closed(**kw):
    g = S.build_ts_semantic_graph(**kw)
    run, objects, blobs, actual = SR.close_positive(g)
    return run, objects, blobs, actual


INCOMING = dict(atom=SR.REFS_NONE_TGT, has_declares=False, has_references_fact=True, second_partition=True,
                references_resolved=False, incoming_search=True, incoming_complete=False, target_sidecar=True)
CASES = {
    "incoming-incomplete": lambda: SR.case_incoming_incomplete_unknown()[1],
    "missing-inventory": lambda: SR.case_missing_inventory_execution()[1],
    "stage-budget-foo": lambda: closed(**INCOMING, references_stage_terminals={"foo": "budget-exhausted"})[:3],
    "stage-budget-bar": lambda: closed(**INCOMING, references_stage_terminals={"bar": "budget-exhausted"})[:3],
    "stage-unavailable-foo": lambda: closed(**INCOMING, references_stage_terminals={"foo": "unavailable"})[:3],
    "work-budget-over-incoming": lambda: closed(**INCOMING, budget_limit=1)[:3],
    "work-budget-declares": lambda: closed(atom=SR.DECLARES, has_declares=True, budget_limit=1)[:3],
}
out = {"routeDrift": T.route_drift()}
for label, fn in CASES.items():
    try:
        run, objects, blobs = fn()
        run_id, verdict, population, ctx = T.retained_population(run, objects, blobs)
        conds = T.conditions(population, objects, blobs, ctx["xi"])
        fin = T.finalize(run, objects, blobs)
        evidence = objects[run["evidenceId"]][1]
        coverage = {}
        for cid in evidence["coverageIds"]:
            e = T.C.parse(blobs[objects[cid][1]["payloadDigest"]])["entry"]
            if e["deficiency"] or e["resolutionCompleteness"]["stageTerminal"] not in (None, "complete"):
                coverage[cid] = {"deficiency": e["deficiency"], "state": e["resolutionCompleteness"]["state"],
                                 "stageTerminal": e["resolutionCompleteness"]["stageTerminal"]}
        out[label] = {"runId": run_id, "verdict": verdict, "evaluationState": ctx["proof"]["evaluationState"],
                      "population": sorted({(d["source"], d["cause"]) for d in population}),
                      "conditions": [{k: c[k] for k in ("cause", "origin", "rank", "d9Deficiency", "declaredCarriers", "stageCarriers")} for c in conds],
                      "deficientOrStagedCoverage": coverage, "finalize": fin,
                      "permutation": T.permutation_invariance(conds) if verdict == "indeterminate" else None}
    except Exception as exc:
        out[label] = {"error": type(exc).__name__ + ": " + str(exc)[:800], "tb": traceback.format_exc()[-2500:]}
print(json.dumps(out, indent=1, default=str))
