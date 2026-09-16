"""Phase 9 admission evidence per claimed complete positive Run, plus the three-valued replay vector.

For every positive Run (runs/*.replay.json with result ADMIT, excluding mutations/attempt copies):
  * per-record validation log: every record ref/closure.py admitted, re-validated here against its owning schema (typed scalars,
    stock JSON Schema, x-opensip-order walk) and the x-opensip-digest law (runs/<name>.records.json);
  * export sufficiency: object table frames and every referenced blob present and rehashed;
  * selected provider/capability context per Run;
  * the four boundaries: schema, helper predicates, closure joins, host enforcement (never claimed).
Three-valued vector (R-REPLAY-THREE-VALUED): the evaluator re-run over ts-pass retained inputs with an explanatory policy whose atoms
need relations the Run has no Coverage for (vectors/replay-three-valued.json).
Usage: python3 tools/runref.py tools/phase9_admission_log.py
"""
import glob
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24/output"
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/tools")

import canonical as K  # noqa: E402
import closure as CL  # noqa: E402
import digestlaw  # noqa: E402
import evaluator as EV  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402

KIT = schemas.kit()
failures = []


def must(name, cond, detail=None):
    if not cond:
        failures.append({"vector": name, "detail": detail})
    return bool(cond)


def positives():
    names = []
    for p in sorted(glob.glob(f"{OUT}/runs/*.replay.json")):
        name = os.path.basename(p)[:-len(".replay.json")]
        if "~" in name or "." in name:
            continue
        if json.load(open(p))["result"] == "ADMIT":
            names.append(name)
    return names


def record_log(name):
    exported = json.load(open(f"{OUT}/runs/{name}.store.json"))
    store = Store.load(exported)
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    rows, bad = [], 0
    for label, inst, doc, sel in C.admitted:
        r = KIT.admit(inst, doc, sel)
        law = digestlaw.check_instance(store, inst, doc, sel, {"plan": g["plan"]})
        ok = r["ok"] and not law["faults"]
        bad += 0 if ok else 1
        rows.append({"label": label, "document": r["document"], "selector": sel, "typedScalars": r["typed"], "stockErrors": len(r["stock"]),
                     "orderViolations": len(r["order"]), "digestLawFaults": law["faults"], "annotatedDigestFields": law["annotated"], "admitted": ok})
    missing_frames = [row["id"] for row in exported["objectTable"] if row["frameSha256"] not in store.blobs]
    rehash_ok = all(hashlib.sha256(b).hexdigest() == h for h, b in store.blobs.items())
    closures = {row["id"]: store.get_object(row["id"]) for row in exported["objectTable"] if row["domain"] == "closure"}
    replay = json.load(open(f"{OUT}/runs/{name}.replay.json"))
    ctx = {"capabilityManifestId": g["plan"]["capabilityManifestId"], "semanticClosures": {c: closures[c]["kind"] for c in g["plan"]["semanticClosures"]},
           "nativeContextDigests": g["plan"]["nativeContextDigests"], "universeDomains": sorted({b["domain"] for b in g["bound"].values()}),
           "requestedCapabilities": store.get_record(g["plan"]["analysisSpecDigest"])["requestedCapabilities"],
           "viewProducers": sorted({v["producerClosure"] for v in g["views"].values()})}
    log = {"run": name, "runId": exported["runId"], "records": rows, "recordCount": len(rows), "recordsRefused": bad,
           "export": {"objectTableRows": len(exported["objectTable"]), "blobs": len(store.blobs), "framesMissing": missing_frames, "allBlobsRehash": rehash_ok},
           "selectedProviderContext": ctx,
           "boundaries": {"schema": {"recordsValidated": len(rows), "refused": bad},
                          "helperPredicates": {"graphFaults": C.faults, "note": "native_ctx / native_facts / enumeration / execution-inputs / imports re-derivations inside admit_graph"},
                          "closure": {"result": replay["result"], "admittedRecords": replay["graphAdmission"]["admittedRecords"],
                                      "digestLawRecords": (replay["graphAdmission"].get("digestLaw") or {}).get("records")},
                          "replay": {"performed": replay["semanticReplay"].get("performed"), "faults": replay["semanticReplay"].get("faults"),
                                     "freshProcess": replay["receipt"]["freshProcess"], "storeFileSha256": replay["receipt"]["storeFileSha256"]},
                          "hostEnforcement": "not claimed (future qualification: real OS/compiler/crypto/SQLite, host authentication)"}}
    with open(f"{OUT}/runs/{name}.records.json", "w") as fh:
        json.dump(log, fh, indent=1, sort_keys=True)
    must(f"{name}:records", bad == 0 and not missing_frames and rehash_ok and not C.faults and replay["result"] == "ADMIT", (bad, missing_frames[:3], C.faults[:3]))
    return log


def three_valued():
    exported = json.load(open(f"{OUT}/runs/ts-pass.store.json"))
    store = Store.load(exported)
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    template = next(r for r in g["policy"]["rules"] if r["ruleId"] == "cb24.ts.external-call")
    binding = next(b for b in g["emission"]["rules"] if b["ruleId"] == "cb24.ts.external-call")

    def rule(rid, when):
        return dict(template, ruleId=rid, ruleProgramRef=dict(template["ruleProgramRef"], ruleStableId=rid,
                                                               programDigest=hashlib.sha256(rid.encode()).hexdigest()),
                    enabled=True, severity="error", gate=True, subjectEnumeration={"universe": "typescript", "subjectKind": "symbol"},
                    emitWhen=when, evidenceUse=[], messageCode=rid)
    refs = {"op": "exists", "relation": "references", "minResolution": "resolved-binding", "filters": []}
    calls = {"op": "exists", "relation": "calls", "minResolution": "resolved-callee", "filters": []}
    rules = sorted([rule("cb24.explain.references-missing-coverage", refs), rule("cb24.explain.calls-present", calls),
                    rule("cb24.explain.and-calls-references", {"op": "and", "operands": [calls, refs]}),
                    rule("cb24.explain.or-calls-references", {"op": "or", "operands": [calls, refs]})], key=lambda r: r["ruleId"].encode())
    policy = dict(g["policy"], rules=rules)
    emission = {"schemaVersion": 1, "policyDigest": K.raw_digest(policy), "rules": [dict(binding, ruleId=r["ruleId"], ruleStableId=r["ruleId"]) for r in rules]}
    im = g["imports"]
    inp = EV.Inputs(plan=dict(g["plan"], policyDigest=K.raw_digest(policy)), plan_id=g["plan_id"], exec_plan_id=g["exec_plan_id"],
                    evaluator_closure=g["xi"]["evaluatorClosure"], policy=policy, waivers=g["waivers"], emission=emission, enum_plan=g["enum"],
                    inventories=g["index"]["inventories"], views=g["views"], scopes=g["scopes"], coverages=g["coverages"], facts=g["facts"],
                    fact_payloads=g["payloads"], bound=g["bound"], imports={i: r["wrapper"] for i, r in im.items()},
                    import_payloads={i: r["payload"] for i, r in im.items()}, import_observations={i: r["observation"] for i, r in im.items()},
                    import_scopes={i: r["scope"] for i, r in im.items()}, import_flags={i: r["flags"] for i, r in im.items()}, exec_inputs=g["xi"],
                    exec_inputs_digest=g["proof"]["executionInputsDigest"], required_rows=g["derived"]["requiredRows"], scope_document=g["scope_document"],
                    project_id=g["snapshot"]["projectId"])
    try:
        out = EV.evaluate(inp)
    except EV.EvalRefusal as exc:
        must("three-valued-evaluates", False, exc.key)
        return
    subj = {}
    for rid in out["proof"]["findingIds"]:
        pass
    witnesses = {}
    for p in out["proof"]["predicateProofs"]:
        w = json.loads(out["blobs"][p["witnessDigest"]])
        witnesses.setdefault(p["ruleId"], []).append({"subjectId": p["subjectId"], "predicateId": p["predicateId"], "operation": p["operation"], "value": p["value"],
                                                      "coverageIds": w["coverageIds"], "deficiencies": [(d["source"], d["cause"]) for d in w["deficiencies"]]})
    roots = {rid: sorted({w["value"] for w in ws if w["predicateId"] == "p"}) for rid, ws in witnesses.items()}
    outcomes = {r["ruleId"]: r["outcome"] for r in out["proof"]["ruleResults"]}
    must("references-missing-coverage-never-vacuous", roots.get("cb24.explain.references-missing-coverage") == ["indeterminate"], roots)
    must("calls-with-coverage-determinate", set(roots.get("cb24.explain.calls-present", [])) == {"true", "false"}, roots)
    must("and-false-indeterminate-is-false", "false" in roots.get("cb24.explain.and-calls-references", []) and
         "true" not in roots.get("cb24.explain.and-calls-references", []), roots)
    must("or-true-indeterminate-is-true", "true" in roots.get("cb24.explain.or-calls-references", []), roots)
    with open(f"{OUT}/vectors/replay-three-valued.json", "w") as fh:
        json.dump({"classification": "explanatory", "baseRun": "ts-pass", "policy": policy, "rootValues": roots, "ruleOutcomes": outcomes,
                   "witnesses": witnesses, "findingCount": len(out["findings"]),
                   "law": "strong Kleene composition over atoms; an atom whose relation has no retained Coverage and no match is indeterminate (not vacuous false), "
                          "and(false, indeterminate)=false, or(true, indeterminate)=true (atom-evaluation-contract.v1 s4/s7; workflow-projection-contract.v3 s11, s14)",
                   "note": "explanatory re-evaluation over the retained admitted inputs of ts-pass; no Run is minted"}, fh, indent=1, sort_keys=True)


def main():
    logs = [record_log(n) for n in positives()]
    three_valued()
    tamper = {os.path.basename(p): json.load(open(p)) for p in sorted(glob.glob(f"{OUT}/runs/*.tamper-outputs.json"))}
    summary = {"positives": [{"run": l["run"], "runId": l["runId"], "records": l["recordCount"], "refused": l["recordsRefused"],
                              "closure": l["boundaries"]["closure"]["result"], "replayPerformed": l["boundaries"]["replay"]["performed"],
                              "universeDomains": l["selectedProviderContext"]["universeDomains"]} for l in logs],
               "tamperReports": {k: (v.get("summary") if isinstance(v, dict) and "summary" in v else sorted(v)[:12] if isinstance(v, dict) else None) for k, v in tamper.items()},
               "assertionFailures": failures}
    with open(f"{OUT}/runs/phase9-admission-summary.json", "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print("positives", len(logs), "failures", len(failures))
    print(json.dumps(failures, default=str)[:4000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
