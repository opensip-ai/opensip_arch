"""Supplementary probe: is plan.semanticClosures really the ONLY Plan selector array
without an upper bound? Measures the two comparators (nativeContextDigests, importIds)
under the same superset mutation that plan.semanticClosures tolerated.
"""
import importlib.util, pathlib, hashlib, json, sys, copy

FOUND = pathlib.Path("/tmp/opensip-design-corrections/candidate-subject.v19/"
                     "docs/coop/design-corrections/foundation")
sys.path.insert(0, str(FOUND))
spec = importlib.util.spec_from_file_location("ci", FOUND / "check-identity.py")
ci = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(ci)
except SystemExit:
    pass
M, C = ci.M, ci.C
RESULTS = []


def record(pid, q, outcome, detail):
    RESULTS.append({"id": pid, "question": q, "outcome": outcome, "detail": detail})
    print("[%s] %s -> %s" % (pid, q, outcome))
    for k, v in detail.items():
        print("      %s: %s" % (k, v))


def close(run, objects, blobs):
    try:
        return "ACCEPT", M.close_run(run, objects, blobs)
    except Exception as exc:                       # noqa: BLE001
        return "REFUSE", "%s:%s" % (type(exc).__name__, exc)


def remint_plan(run, objects, blobs, mutate_plan):
    """Same complete re-mint as probes.py, parameterised by an arbitrary Plan edit."""
    objects = dict(objects); blobs = dict(blobs)

    def put_blob(v):
        raw = C.canonical(v); d = hashlib.sha256(raw).hexdigest(); blobs[d] = raw; return d

    def add(dom, v):
        k = M.identifier(dom, v); objects[k] = (dom, v); return k

    plan = copy.deepcopy(objects[run["planId"]][1])
    mutate_plan(plan)
    npid = add("plan", plan)
    seal = copy.deepcopy(objects[run["evaluationSealId"]][1])
    evidence = copy.deepcopy(objects[seal["evidenceId"]][1])
    proof = copy.deepcopy(objects[seal["proofBundleId"]][1])
    ep = copy.deepcopy(objects[seal["executionPlanId"]][1])

    ovid = evidence["viewIds"][0]
    view = copy.deepcopy(objects[ovid][1]); view["planId"] = npid
    nvid = add("view", view)
    od, nd = ovid.split(":", 1)[1], nvid.split(":", 1)[1]

    s = C.parse(blobs[ep["stages"][0]["stageSpecDigest"]]); s["planId"] = npid
    ep["stages"][0]["stageSpecDigest"] = put_blob(s); ep["planId"] = npid
    nep = add("execution-plan", ep)

    def retarget(refs):
        for r in refs:
            if r.get("domain") == "view" and r["digest"] == od:
                r["digest"] = nd
    proof["planId"] = npid; proof["executionPlanId"] = nep
    retarget(proof["evaluationInputRefs"])
    for p in proof["predicateProofs"]:
        retarget(p["inputRefs"])
    nproof = add("proof-bundle", proof)
    evidence["planId"] = npid; evidence["viewIds"] = [nvid]; evidence["proofBundleId"] = nproof
    nev = add("semantic-evidence", evidence)
    seal["planId"] = npid; seal["executionPlanId"] = nep
    seal["proofBundleId"] = nproof; seal["evidenceId"] = nev
    nseal = add("evaluation-seal", seal)
    run = dict(run); run["planId"] = npid
    run["evidenceId"] = nev; run["evaluationSealId"] = nseal
    return run, objects, blobs


run0, obj0, blob0 = ci.build()
st0, rid0 = close(run0, obj0, blob0)
plan0 = obj0[run0["planId"]][1]
record("BASE2", "baseline", st0, {"runId": rid0})

# comparator 1: an EXTRA retained native context digest (a real one, from another language build)
run_rs, obj_rs, blob_rs = ci.build(universe_language="rust")
plan_rs = obj_rs[run_rs["planId"]][1]
foreign_ctx = [d for d in plan_rs["nativeContextDigests"]
               if d not in plan0["nativeContextDigests"]]
merged_obj = dict(obj0); merged_obj.update(obj_rs)
merged_blob = dict(blob0); merged_blob.update(blob_rs)
if foreign_ctx:
    r, o, b = remint_plan(run0, merged_obj, merged_blob,
                          lambda p: p.update(nativeContextDigests=sorted(
                              set(p["nativeContextDigests"]) | {foreign_ctx[0]})))
    st, rid = close(r, o, b)
    record("CMP-CONTEXT-SUPERSET",
           "does an EXTRA retained nativeContextDigest close (superset)", st,
           {"added": foreign_ctx[0], "detail": rid})

# comparator 2: an EXTRA importId
r, o, b = remint_plan(run0, merged_obj, merged_blob,
                      lambda p: p.update(importIds=["import2:" + "a" * 64]))
st, rid = close(r, o, b)
record("CMP-IMPORT-SUPERSET", "does an EXTRA importId close (superset)", st, {"detail": rid})

# restate the semanticClosures result under the identical harness
extra = sorted({k for k, v in obj0.items() if v[0] == "closure"} - set(plan0["semanticClosures"]))
r, o, b = remint_plan(run0, merged_obj, merged_blob,
                      lambda p: p.update(semanticClosures=sorted(
                          set(p["semanticClosures"]) | set(extra))))
st, rid = close(r, o, b)
record("CMP-CLOSURE-SUPERSET", "does an EXTRA semanticClosure close (superset)", st,
       {"added": extra, "runId": rid, "differsFromBaseline": rid != rid0})

pathlib.Path(__file__).with_name("probe2-results.json").write_text(
    json.dumps(RESULTS, indent=1) + "\n")
print("\nwrote probe2-results.json")
