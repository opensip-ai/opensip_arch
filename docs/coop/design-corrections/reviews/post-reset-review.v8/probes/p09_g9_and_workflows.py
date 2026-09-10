#!/usr/bin/env python3
"""P09: Bv2 G9 (`evidence.pinned` public projection) and the two adjacent
workflow recipes closed at root:
  - policy-test-suite H domain/preimage vs raw policy digests
  - generic mutation idempotency H over MutationReplayScopeV1

The question for each is not "does the code run" but: does the recipe grant
any authority it should not, and can it dedup across requests?
"""
import contextlib, copy, hashlib, importlib.util, io, json, sys
from pathlib import Path

SUBJ = Path("/tmp/opensip-design-corrections/candidate-subject.v8")
DC = SUBJ / "docs/coop/design-corrections"
F = DC / "foundation"


def load(n, p, iso=False):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    if not iso:
        s.loader.exec_module(m)
        return m
    a, b = sys.argv, io.StringIO()
    sys.argv = [str(p)]
    try:
        with contextlib.redirect_stdout(b):
            try:
                s.loader.exec_module(m)
            except SystemExit:
                pass
    finally:
        sys.argv = a
    return m


W = load("wf", DC / "workflows/workflows_model.v1.py")
M = load("idmodel", F / "identity-model.py")
C = M.C

R = {"checks": [], "observations": {}}


def rec(n, ok, d=None):
    R["checks"].append({"id": n, "passed": bool(ok), "detail": d})


def refuses(n, fn, token=""):
    try:
        fn()
    except Exception as exc:
        rec(n, token in str(exc), {"expect": token, "got": str(exc)[:300]})
    else:
        rec(n, False, {"got": "ADMITTED"})


# ---------------------------------------------------------------------------
# G9: evidence.pinned
# ---------------------------------------------------------------------------
def g9():
    reg = json.loads((DC / "public-detail-registry.v1.json").read_bytes())
    codes = [r["code"] for r in reg["records"]]
    rec("G9-01-evidence.pinned-is-a-registered-public-detail",
        "evidence.pinned" in codes)
    row = next(r for r in reg["records"] if r["code"] == "evidence.pinned")
    R["observations"]["registryRow"] = row
    rec("G9-02-registered-with-an-owner", bool(row.get("owner")), {"row": row})

    pins = [{"pinId": "b-baseline", "kind": "baseline"},
            {"pinId": "a-repair", "kind": "repair-prerequisite"},
            {"pinId": "c-export", "kind": "backup-export"}]
    env = W.pinned_purge_refusal("req1_" + "a" * 32, "run2:" + "b" * 64, pins)
    R["observations"]["envelope"] = env
    d = env["termination"]["domainDetail"]
    rec("G9-03-admissible-failure-envelope-exists",
        env["kind"] == "failure" and env["exitCode"] == 2
        and env["termination"]["errorCode"] == "REQUEST.PRECONDITION_FAILED")
    rec("G9-04-complete-pin-inventory-not-a-count",
        len(d["purgeDisclosure"]["activePins"]) == 3
        and all("pinId" in p and "kind" in p for p in d["purgeDisclosure"]["activePins"]))
    rec("G9-05-pins-sorted-uniquely-by-pinId",
        [p["pinId"] for p in d["purgeDisclosure"]["activePins"]]
        == ["a-repair", "b-baseline", "c-export"])
    rec("G9-06-three-ordered-consequences",
        d["purgeDisclosure"]["consequences"] == [
            "named-pins-revoked", "dependent-evidence-replay-unavailable",
            "sealed-history-retained"])
    rec("G9-07-subject-joins-the-disclosure-runId",
        d["subject"] == d["purgeDisclosure"]["runId"])
    rec("G9-08-errors-array-equals-the-single-detail",
        env["errors"] == [d])

    # bounds: an empty pin set is not a lawful pinned refusal
    refuses("G9-09-empty-pin-inventory-refused",
            lambda: W.pinned_purge_refusal("req1_" + "a" * 32, "run2:" + "b" * 64, []))
    # a truncated/aggregated disclosure must not validate
    def truncated():
        e = copy.deepcopy(env)
        e["termination"]["domainDetail"]["purgeDisclosure"]["activePins"] = \
            e["termination"]["domainDetail"]["purgeDisclosure"]["activePins"][:1]
        W.validate_pinned_purge_refusal(e)
    refuses("G9-10-truncated-disclosure-fails-the-join", truncated)

    def wrong_subject():
        e = copy.deepcopy(env)
        e["termination"]["domainDetail"]["subject"] = "run2:" + "c" * 64
        W.validate_pinned_purge_refusal(e)
    refuses("G9-11-subject-not-the-disclosed-run", wrong_subject,
            "PINNED_PURGE_PROJECTION_JOIN")

    def wrong_consequences():
        e = copy.deepcopy(env)
        e["termination"]["domainDetail"]["purgeDisclosure"]["consequences"] = [
            "sealed-history-retained", "named-pins-revoked",
            "dependent-evidence-replay-unavailable"]
        W.validate_pinned_purge_refusal(e)
    refuses("G9-12-reordered-consequences-refused", wrong_consequences)

    def unregistered_kind():
        W.pinned_purge_refusal("req1_" + "a" * 32, "run2:" + "b" * 64,
                               [{"pinId": "x", "kind": "invented-kind"}])
    refuses("G9-13-unregistered-pin-kind-refused", unregistered_kind)

    def wrong_exit():
        e = copy.deepcopy(env)
        e["exitCode"] = 4
        W.validate_pinned_purge_refusal(e)
    refuses("G9-14-wrong-exit-code-refused", wrong_exit)

    # --- the store refusal precedes and outlives the public projection ----
    store = M.EvidenceStore()
    CHK, run, objects, blobs = _run()
    rid = M.identifier("run", run)
    plan = objects[run["planId"]][1]
    proof = [v for d, v in objects.values() if d == "proof-bundle"][0]
    replay = lambda p, o, b, refs: CHK.replay(p, o, b, refs)
    store.prepare(run, objects, blobs, "exec1_" + "a" * 32, replay=replay)
    store.commit("exec1_" + "a" * 32)
    store.pins.add(rid)
    outcome = store.purge(rid)
    rec("G9-15-actual-store-refuses-before-any-projection", outcome == "pinned",
        {"outcome": outcome})
    rec("G9-16-run-and-pins-survive-the-refusal",
        rid in store.pins and store.query(rid) != "not-found")
    forced = store.purge(rid, force=True)
    rec("G9-17-explicit-destructive-authorization-required-to-proceed",
        forced == "purged" and rid not in store.pins, {"forced": forced})
    rec("G9-18-sealed-manifest-retained-after-purge",
        store.query(rid) != "not-found")
    rec("G9-19-evidence-requiring-query-refuses-after-purge",
        store.query(rid, requires_evidence=True) == "precondition-failed")

    # --- the pure helper confers NO authority ----------------------------
    src = (DC / "workflows/workflows_model.v1.py").read_text()
    fn_src = src[src.index("def pinned_purge_refusal"):src.index("def validate_pinned_purge_refusal")]
    forbidden = ["pins.discard", "set_availability", "purge(", "revoke", "delete",
                 "lease", "acquire"]
    R["observations"]["pureHelperForbiddenTokens"] = {
        t: (t in fn_src) for t in forbidden}
    rec("G9-20-pure-helper-performs-no-destructive-or-lease-act",
        not any(t in fn_src for t in forbidden),
        R["observations"]["pureHelperForbiddenTokens"])


def _run():
    CHK = load("idcheck", F / "check-identity.py", True)
    run, objects, blobs = CHK.build(has_match=True)
    return CHK, run, objects, blobs


# ---------------------------------------------------------------------------
# The two workflow recipes
# ---------------------------------------------------------------------------
def recipes():
    src = (DC / "workflows/workflows_model.v1.py").read_text()
    # locate the two recipes
    names = [n for n in ("policy_test_suite_identity", "policy_test_suite_digest",
                         "mutation_replay_key", "mutation_idempotency_key",
                         "repair_apply_key")
             if "def " + n in src]
    R["observations"]["recipeFunctionsPresent"] = names
    fns = {n: getattr(W, n) for n in names if hasattr(W, n)}

    # --- policy test suite: an H domain, not a raw policy digest ---------
    suite_fn = fns.get("policy_test_suite_identity") or fns.get("policy_test_suite_digest")
    if suite_fn:
        import inspect
        sig = inspect.signature(suite_fn)
        R["observations"]["policyTestSuiteSignature"] = str(sig)
        R["observations"]["policyTestSuiteSource"] = inspect.getsource(suite_fn)[:1800]

    # --- mutation replay scope -------------------------------------------
    mk = fns.get("mutation_replay_key") or fns.get("mutation_idempotency_key")
    if mk:
        import inspect
        R["observations"]["mutationKeySource"] = inspect.getsource(mk)[:2500]
        sch = json.loads((DC / "workflows/schemas/invocation-record.schema.json").read_bytes())
        scope = None
        for doc in (DC / "workflows/schemas").glob("*.json"):
            j = json.loads(doc.read_bytes())
            if "MutationReplayScopeV1" in json.dumps(j):
                d = j.get("$defs", {}).get("MutationReplayScopeV1")
                if d:
                    scope = {"document": doc.name, "schema": d}
        R["observations"]["MutationReplayScopeV1"] = scope
        if scope:
            props = sorted(scope["schema"].get("properties", {}))
            R["observations"]["mutationScopeFields"] = props
            rec("REC-01-mutation-scope-is-request-and-step-scoped",
                any("request" in p.lower() for p in props)
                and any("step" in p.lower() for p in props), {"fields": props})
            rec("REC-02-mutation-scope-is-a-closed-record",
                scope["schema"].get("additionalProperties") is False)


def main():
    g9()
    recipes()
    R["summary"] = {"total": len(R["checks"]),
                    "passed": sum(c["passed"] for c in R["checks"]),
                    "failed": [c for c in R["checks"] if not c["passed"]]}
    json.dump(R, sys.stdout, indent=1, default=str)
    print()


if __name__ == "__main__":
    main()
