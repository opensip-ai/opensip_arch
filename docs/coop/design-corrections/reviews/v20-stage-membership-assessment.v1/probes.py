"""Independent discriminating probes for CB-GAP-4 and CB-GAP-5.

Runs against the FROZEN v19 reference model only. Writes nothing outside this directory.
Every probe drives the real `close_run` boundary; nothing is asserted from inspection alone.
"""
import importlib.util, pathlib, hashlib, json, sys, copy

FOUND = pathlib.Path("/tmp/opensip-design-corrections/candidate-subject.v19/"
                     "docs/coop/design-corrections/foundation")
sys.path.insert(0, str(FOUND))

# check-identity.py runs its own 1431-check suite and sys.exit(0)s; that exit is the
# baseline control, so it is caught rather than suppressed.
spec = importlib.util.spec_from_file_location("ci", FOUND / "check-identity.py")
ci = importlib.util.module_from_spec(spec)
_baseline_exit = None
try:
    spec.loader.exec_module(ci)
except SystemExit as e:
    _baseline_exit = e.code

M, C, N = ci.M, ci.C, ci.N
RESULTS = []


def record(pid, question, outcome, detail):
    RESULTS.append({"id": pid, "question": question, "outcome": outcome, "detail": detail})
    print("[%s] %s -> %s" % (pid, question, outcome))
    for k, v in detail.items():
        print("      %s: %s" % (k, v))


def close(run, objects, blobs):
    """Returns ('ACCEPT', runId) or ('REFUSE', code)."""
    try:
        return "ACCEPT", M.close_run(run, objects, blobs)
    except Exception as exc:                       # noqa: BLE001 - probe boundary
        return "REFUSE", "%s:%s" % (type(exc).__name__, exc)


def rebuild_from_stage(run, objects, blobs, mutate_spec, mutate_stage):
    """Re-mint the exact dependent chain of a stage-spec edit.

    stage-spec bytes -> execution-plan -> proof-bundle -> semantic-evidence -> seal -> run.
    The Plan is NOT re-minted: no Plan field names the execution plan, so PlanId is invariant
    under a stage edit. Facts, scopes, coverage and views are untouched for the same reason.
    """
    objects = dict(objects); blobs = dict(blobs)

    def put_blob(value):
        raw = C.canonical(value); d = hashlib.sha256(raw).hexdigest(); blobs[d] = raw; return d

    def add(domain, value):
        key = M.identifier(domain, value); objects[key] = (domain, value); return key

    seal_id = run["evaluationSealId"]
    seal = copy.deepcopy(objects[seal_id][1])
    evidence = copy.deepcopy(objects[seal["evidenceId"]][1])
    proof = copy.deepcopy(objects[seal["proofBundleId"]][1])
    ep = copy.deepcopy(objects[seal["executionPlanId"]][1])

    old_spec_digest = ep["stages"][0]["stageSpecDigest"]
    spec = C.parse(blobs[old_spec_digest])
    mutate_spec(spec)
    new_spec_digest = put_blob(spec)
    ep["stages"][0]["stageSpecDigest"] = new_spec_digest
    mutate_stage(ep["stages"][0])
    new_ep = add("execution-plan", ep)

    proof["executionPlanId"] = new_ep
    new_proof = add("proof-bundle", proof)
    evidence["proofBundleId"] = new_proof
    new_evidence = add("semantic-evidence", evidence)
    seal["executionPlanId"] = new_ep
    seal["proofBundleId"] = new_proof
    seal["evidenceId"] = new_evidence
    new_seal = add("evaluation-seal", seal)

    run = dict(run)
    run["evidenceId"] = new_evidence
    run["evaluationSealId"] = new_seal
    return run, objects, blobs


def rebuild_with_plan_closures(run, objects, blobs, new_closures):
    """Re-mint a COMPLETE closing graph for an edited plan.semanticClosures.

    This is the control the blind claim declined to construct. The Plan changes, so every
    record that names planId is re-minted: plan -> view -> stage-spec -> execution-plan ->
    proof (executionPlanId AND the view digest it references) -> evidence -> seal -> run.
    subject-scope, fact and coverage are NOT re-minted: they bind snapshotId and universes,
    not PlanId, so they remain valid members of the new graph unchanged.
    """
    objects = dict(objects); blobs = dict(blobs)

    def put_blob(value):
        raw = C.canonical(value); d = hashlib.sha256(raw).hexdigest(); blobs[d] = raw; return d

    def add(domain, value):
        key = M.identifier(domain, value); objects[key] = (domain, value); return key

    old_plan_id = run["planId"]
    plan = copy.deepcopy(objects[old_plan_id][1])
    plan["semanticClosures"] = sorted(set(new_closures))
    new_plan_id = add("plan", plan)

    seal = copy.deepcopy(objects[run["evaluationSealId"]][1])
    evidence = copy.deepcopy(objects[seal["evidenceId"]][1])
    proof = copy.deepcopy(objects[seal["proofBundleId"]][1])
    ep = copy.deepcopy(objects[seal["executionPlanId"]][1])

    old_view_id = evidence["viewIds"][0]
    view = copy.deepcopy(objects[old_view_id][1])
    view["planId"] = new_plan_id
    new_view_id = add("view", view)
    old_vd, new_vd = old_view_id.split(":", 1)[1], new_view_id.split(":", 1)[1]

    spec = C.parse(blobs[ep["stages"][0]["stageSpecDigest"]])
    spec["planId"] = new_plan_id
    ep["stages"][0]["stageSpecDigest"] = put_blob(spec)
    ep["planId"] = new_plan_id
    new_ep = add("execution-plan", ep)

    def retarget(refs):
        for r in refs:
            if r.get("domain") == "view" and r["digest"] == old_vd:
                r["digest"] = new_vd
    proof["planId"] = new_plan_id
    proof["executionPlanId"] = new_ep
    retarget(proof["evaluationInputRefs"])
    for p in proof["predicateProofs"]:
        retarget(p["inputRefs"])
    new_proof = add("proof-bundle", proof)

    evidence["planId"] = new_plan_id
    evidence["viewIds"] = [new_view_id]
    evidence["proofBundleId"] = new_proof
    new_evidence = add("semantic-evidence", evidence)

    seal["planId"] = new_plan_id
    seal["executionPlanId"] = new_ep
    seal["proofBundleId"] = new_proof
    seal["evidenceId"] = new_evidence
    new_seal = add("evaluation-seal", seal)

    run = dict(run)
    run["planId"] = new_plan_id
    run["evidenceId"] = new_evidence
    run["evaluationSealId"] = new_seal
    return run, objects, blobs


# ---------------------------------------------------------------- baseline
run0, obj0, blob0 = ci.build()
st0, rid0 = close(run0, obj0, blob0)
record("BASE", "does the unmodified v19 fixture close",
       st0, {"runId": rid0, "suiteExit": _baseline_exit})

plan0 = obj0[run0["planId"]][1]
ep0 = obj0[obj0[run0["evaluationSealId"]][1]["executionPlanId"]][1]
spec0 = C.parse(blob0[ep0["stages"][0]["stageSpecDigest"]])
record("BASE-VALUES", "what the fixture actually writes", "OBSERVED",
       {"operation": spec0["operation"],
        "stage-spec.outputDomains": spec0["outputDomains"],
        "execution-plan stage outputDomains": ep0["stages"][0]["outputDomains"],
        "plan.semanticClosures": plan0["semanticClosures"],
        "closureKinds": {k: obj0[k][1]["kind"] for k in plan0["semanticClosures"]}})

# ---------------------------------------------------------------- CB-GAP-4
for pid, newop in [("G4-OP-native.analyze", "native.analyze"),
                   ("G4-OP-analyze", "analyze"),
                   ("G4-OP-derive", "derive"),
                   ("G4-OP-emoji", "\U0001f600 not an operation at all"),
                   ("G4-OP-empty", "")]:
    r, o, b = rebuild_from_stage(run0, obj0, blob0,
                                 lambda s, v=newop: s.update(operation=v), lambda st: None)
    st, rid = close(r, o, b)
    record(pid, "does close_run accept operation=%r" % newop, st,
           {"runId": rid, "runIdDiffersFromBaseline": rid != rid0})

for pid, doms in [("G4-DOM-view2", ["view2"]),
                  ("G4-DOM-scope2", ["scope2"]),
                  ("G4-DOM-subject-scope", ["subject-scope"]),
                  ("G4-DOM-unregistered", ["totally-unregistered-domain-xyz"]),
                  ("G4-DOM-empty-array", []),
                  ("G4-DOM-mismatch-control", None)]:
    if doms is None:
        # control: the ONE rule identity section 3 does state - spec must equal stage
        r, o, b = rebuild_from_stage(run0, obj0, blob0,
                                     lambda s: s.update(outputDomains=["fact"]),
                                     lambda st: None)
        st, rid = close(r, o, b)
        record(pid, "spec/stage outputDomains disagree (the stated rule)", st, {"detail": rid})
        continue
    r, o, b = rebuild_from_stage(run0, obj0, blob0,
                                 lambda s, v=doms: s.update(outputDomains=list(v)),
                                 lambda st, v=doms: st.update(outputDomains=list(v)))
    st, rid = close(r, o, b)
    record(pid, "does close_run accept outputDomains=%r on BOTH sides" % doms, st,
           {"runId": rid, "runIdDiffersFromBaseline": rid != rid0})

# ---------------------------------------------------------------- CB-GAP-5
all_closures = {k: v[1]["kind"] for k, v in obj0.items() if v[0] == "closure"}
record("G5-INVENTORY", "every retained closure object and its kind", "OBSERVED",
       {"closures": all_closures,
        "selected": plan0["semanticClosures"],
        "retainedButNotSelected": sorted(set(all_closures) - set(plan0["semanticClosures"]))})

extra = sorted(set(all_closures) - set(plan0["semanticClosures"]))
if extra:
    sup = list(plan0["semanticClosures"]) + [extra[0]]
    r, o, b = rebuild_with_plan_closures(run0, obj0, blob0, sup)
    st, rid = close(r, o, b)
    record("G5-SUPERSET", "does a SUPERSET Plan (extra retained closure) close", st,
           {"added": extra[0], "addedKind": all_closures[extra[0]],
            "runId": rid, "runIdDiffersFromBaseline": rid != rid0,
            "planIdDiffers": r["planId"] != run0["planId"]})

    r, o, b = rebuild_with_plan_closures(run0, obj0, blob0, list(plan0["semanticClosures"]) + extra)
    st, rid = close(r, o, b)
    record("G5-SUPERSET-ALL", "does a Plan selecting EVERY retained closure close", st,
           {"added": extra, "runId": rid, "runIdDiffersFromBaseline": rid != rid0})

# a closure2 id that is not retained at all
phantom = "closure2:" + "e" * 64
r, o, b = rebuild_with_plan_closures(run0, obj0, blob0,
                                     list(plan0["semanticClosures"]) + [phantom])
st, rid = close(r, o, b)
record("G5-PHANTOM", "does a Plan selecting an UNRETAINED closure2 id close", st,
       {"added": phantom, "runId": rid, "runIdDiffersFromBaseline": rid != rid0})

# the narrowing direction the blind attempted but did not close
narrow = [c for c in plan0["semanticClosures"] if obj0[c][1]["kind"] == "evaluator"]
r, o, b = rebuild_with_plan_closures(run0, obj0, blob0, narrow)
st, rid = close(r, o, b)
record("G5-NARROW", "does dropping a USED closure (the enumerator) refuse", st,
       {"kept": narrow, "detail": rid})

pathlib.Path(__file__).with_name("probe-results.json").write_text(
    json.dumps({"baselineSuiteExit": _baseline_exit,
                "referencePython": sys.version.split()[0],
                "results": RESULTS}, indent=1) + "\n")
print("\nwrote probe-results.json")
