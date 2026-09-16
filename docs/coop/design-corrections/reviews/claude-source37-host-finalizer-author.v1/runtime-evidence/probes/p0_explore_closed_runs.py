"""P0 (exploration): what a closed evaluator3 Run actually retains for whole-Run cause derivation.

Builds actual closed Runs with the maintained check-semantic-replay cases (identity-model.v3.close_run,
complete replay) from THIS runtime's verified source copy and dumps: proof verdict/evaluationState,
ruleResults outcomes and deficiency records, executionDeficiencies, root predicate values, witness
deficiencies, and the retained Coverage entries (deficiency, nativeCause, state, stageTerminal).
Writes nothing into any tree; stdout only. Reference evidence, not qualification.
"""
import importlib.util
import json
import sys
from pathlib import Path

SRC = Path("/private/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v1/source")
FOUNDATION = SRC / "docs/coop/design-corrections/foundation"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


SR = load("p0_semantic_replay", FOUNDATION / "check-semantic-replay.v3.py")
C = SR.C


def ref_domains(refs):
    out = {}
    for r in refs:
        out[r["domain"]] = out.get(r["domain"], 0) + 1
    return out


def dump(label, fn):
    graph, (run, objects, blobs), actual = fn()
    seal = objects[run["evaluationSealId"]][1]
    proof = objects[seal["proofBundleId"]][1]
    evidence = objects[run["evidenceId"]][1]
    coverage = {}
    for cid in evidence["coverageIds"]:
        desc = objects[cid][1]
        entry = C.parse(blobs[desc["payloadDigest"]])["entry"]
        rc = entry["resolutionCompleteness"]
        coverage[cid] = {"relation": entry["relation"], "resolution": entry["resolution"], "coverage": entry["coverage"],
                         "deficiency": entry["deficiency"], "nativeCause": entry["nativeCause"],
                         "state": rc["state"], "stageTerminal": rc["stageTerminal"]}
    roots = {p["subjectId"]: p["value"] for p in proof["predicateProofs"] if p["predicateId"] == "p"}
    witnesses = []
    for p in proof["predicateProofs"]:
        w = C.parse(blobs[p["witnessDigest"]])
        witnesses.append({"ruleId": p["ruleId"], "subjectId": p["subjectId"], "predicateId": p["predicateId"],
                          "value": p["value"], "kind": w["kind"], "childPredicateIds": w["childPredicateIds"],
                          "coverageIds": w["coverageIds"],
                          "deficiencies": [{"source": d["source"], "cause": d["cause"], "refDomains": ref_domains(d["inputRefs"]),
                                            "coverageRefs": ["coverage2:" + r["digest"] for r in d["inputRefs"] if r["domain"] == "coverage"]}
                                           for d in w["deficiencies"]]})
    return {
        "case": label, "runId": actual["runId"], "verdict": proof["verdict"], "evaluationState": proof["evaluationState"],
        "evaluationInputRefDomains": ref_domains(proof["evaluationInputRefs"]),
        "ruleResults": [{"ruleId": r["ruleId"], "outcome": r["outcome"], "enumerationState": r["enumeration"]["state"],
                         "deficiencies": [{"source": d["source"], "cause": d["cause"], "subjectId": d["subjectId"],
                                           "predicateId": d["predicateId"], "refDomains": ref_domains(d["inputRefs"]),
                                           "nativeCause": d["nativeCause"]} for d in r["deficiencies"]]}
                        for r in proof["ruleResults"]],
        "executionDeficiencies": [{"source": d["source"], "cause": d["cause"], "refDomains": ref_domains(d["inputRefs"]),
                                   "coverageRefs": ["coverage2:" + r["digest"] for r in d["inputRefs"] if r["domain"] == "coverage"],
                                   "nativeCause": d["nativeCause"]} for d in proof["executionDeficiencies"]],
        "roots": roots, "witnesses": witnesses, "coverage": coverage,
    }


rows = []
for label, fn in [("references-incoming-incomplete-unknown", SR.case_incoming_incomplete_unknown),
                  ("missing-required-inventory-execution", SR.case_missing_inventory_execution)]:
    try:
        rows.append(dump(label, fn))
    except Exception as exc:  # recorded, never swallowed
        import traceback
        rows.append({"case": label, "error": type(exc).__name__ + ": " + str(exc)[:600], "tb": traceback.format_exc()[-2000:]})
print(json.dumps(rows, indent=1))
