"""P1 (exploration): the two combined actually closed Runs root probed, rebuilt from THIS runtime's source copy.

For budget_limit=1 with references_stage_terminals.foo in {budget-exhausted, unavailable}: close_run, the
retained population, the condition list, the derivation, every deficient or staged coverage2 record, and
the raw D9 reducer over rotations. Writes nothing into any tree; stdout only.
"""
import importlib.util
import json
import sys
import traceback
from pathlib import Path

SRC = Path("/private/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v2/source")
FOUNDATION = SRC / "docs/coop/design-corrections/foundation"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


SR = load("p1v2_semantic_replay", FOUNDATION / "check-semantic-replay.v3.py")
T = load("p1v2_run_termination", FOUNDATION / "run_termination_model.v1.py")
INCOMING = dict(atom=SR.REFS_NONE_TGT, has_declares=False, has_references_fact=True, second_partition=True,
                references_resolved=False, incoming_search=True, incoming_complete=False, target_sidecar=True)
out = {}
for terminal in ("budget-exhausted", "unavailable"):
    label = "work-budget+stage-" + terminal
    try:
        run, objects, blobs, actual = SR.close_positive(SR.S.build_ts_semantic_graph(
            **INCOMING, budget_limit=1, references_stage_terminals={"foo": terminal}))
        run_id, verdict, population, ctx = T.retained_population(run, objects, blobs)
        conds = T.conditions(population, objects, blobs, ctx["xi"])
        fin = T.finalize(run, objects, blobs)
        coverage = {}
        for cid in objects[run["evidenceId"]][1]["coverageIds"]:
            e = T.C.parse(blobs[objects[cid][1]["payloadDigest"]])["entry"]
            if e["deficiency"] or e["resolutionCompleteness"]["stageTerminal"] not in (None, "complete"):
                coverage[cid] = {"deficiency": e["deficiency"], "state": e["resolutionCompleteness"]["state"],
                                 "stageTerminal": e["resolutionCompleteness"]["stageTerminal"]}
        out[label] = {"runId": run_id, "verdict": verdict, "evaluationState": ctx["proof"]["evaluationState"],
                      "population": sorted({(d["source"], d["cause"]) for d in population}),
                      "conditions": [{k: c[k] for k in ("cause", "origin", "source", "rank", "d9Deficiency", "declaredCarriers", "stageCarriers")} for c in conds],
                      "coverage": coverage, "finalize": fin, "permutation": T.permutation_invariance(conds)}
    except Exception as exc:
        out[label] = {"error": type(exc).__name__ + ": " + str(exc)[:800], "tb": traceback.format_exc()[-2500:]}
print(json.dumps(out, indent=1, default=str))
