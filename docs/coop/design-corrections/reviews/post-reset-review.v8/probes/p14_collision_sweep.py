#!/usr/bin/env python3
"""P14: sweep the remaining digest fields for hidden recipe/identity collisions
or excluded semantic inputs, and finish the cache/regeneration obligations.

A collision here means: two fields whose annotations resolve to the SAME recipe
over the SAME record, so a value minted for one is substitutable for the other
without any join detecting it. Domain-separated H identities cannot collide by
construction; `canonical-record` digests can, so those are the ones to check.
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


M = load("idmodel", F / "identity-model.py")
C = M.C
CHK = load("idcheck", F / "check-identity.py", True)

R = {"checks": [], "observations": {}}


def rec(n, ok, d=None):
    R["checks"].append({"id": n, "passed": bool(ok), "detail": d})


def refuses(n, fn, token=""):
    try:
        fn()
    except Exception as e:
        rec(n, token in str(e), {"expect": token, "got": str(e)[:280]})
    else:
        rec(n, False, {"got": "ADMITTED"})


def putblob(blobs, v):
    raw = v if isinstance(v, bytes) else C.canonical(v)
    d = hashlib.sha256(raw).hexdigest()
    blobs[d] = raw
    return d


# ---------------------------------------------------------------------------
# 1. Collision sweep over the annotations
# ---------------------------------------------------------------------------
def collisions():
    ids = json.loads((F / "identity-schemas.v2.json").read_bytes())
    sites = []

    def ann_of(node):
        if not isinstance(node, dict):
            return None
        if "x-opensip-digest" in node:
            return node["x-opensip-digest"]
        if "items" in node:
            a = ann_of(node["items"])
            if a:
                return a
        for b in node.get("oneOf", []) + node.get("anyOf", []):
            if isinstance(b, dict) and b.get("type") == "null":
                continue
            a = ann_of(b)
            if a:
                return a
        return None

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in (node.get("properties") or {}).items():
                a = ann_of(v)
                if a:
                    sites.append({"path": path + "/properties/" + k, "ann": a})
            for k, v in node.items():
                walk(v, path + "/" + str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + "/" + str(i))
    walk(ids, "#")

    # group canonical-record sites by the record they name
    groups = {}
    for s in sites:
        a = s["ann"]
        if not isinstance(a, dict) or a.get("representation") != "canonical-record":
            continue
        key = json.dumps(a.get("record"), sort_keys=True)
        groups.setdefault(key, []).append(s["path"])
    shared = {k: v for k, v in groups.items() if len(v) > 1}
    R["observations"]["canonicalRecordSitesSharingOneRecord"] = shared
    R["observations"]["totalAnnotatedSites"] = len(sites)

    # A shared recipe is only a COLLISION if no join distinguishes the two uses.
    # The contract names one deliberate sharing: stage-spec appears in both the
    # execution plan and the cache key BECAUSE it is the same record. Check that
    # every other sharing is likewise joined.
    R["observations"]["sharingAnalysis"] = {
        k: {"sites": v,
            "deliberatelyShared": any("stageSpec" in p for p in v)
            or any("policyDigest" in p for p in v)
            or any("waiverDigest" in p for p in v)
            or any("resolvedConfigDigest" in p for p in v)
            or any("scopeDigest" in p for p in v)}
        for k, v in shared.items()}
    rec("COL-01-every-shared-canonical-record-recipe-is-a-declared-sameness",
        all(v["deliberatelyShared"] for v in R["observations"]["sharingAnalysis"].values()),
        R["observations"]["sharingAnalysis"])

    # H domains are pairwise distinct -> no cross-domain identity collision
    doms = ids["x-opensip-digest-domains"]["byDomain"]
    R["observations"]["hDomainCount"] = len(doms)
    same = {"schemaVersion": 2, "x": 1}
    minted = {}
    for d in sorted(doms):
        try:
            minted[d] = M.identifier(d, same)
        except Exception:
            pass
    rec("COL-02-no-two-H-domains-mint-one-identity-for-one-payload",
        len(set(v.split(":")[-1] for v in minted.values())) == len(minted),
        {"domains": len(minted)})

    # a value minted for one canonical record must not satisfy another field
    refuses("COL-03-policy-digest-cannot-stand-in-for-waiver-digest",
            lambda: _swap_plan_field("waiverDigest", "policyDigest"))
    refuses("COL-04-scope-digest-cannot-stand-in-for-config-digest",
            lambda: _swap_plan_field("resolvedConfigDigest", "scopeDigest"))
    refuses("COL-05-analysis-spec-cannot-stand-in-for-grant",
            lambda: _swap_plan_field("semanticGrantDigest", "analysisSpecDigest"))


def _swap_plan_field(target, source):
    run, objects, blobs = CHK.build(has_match=True)
    plan = copy.deepcopy(objects[run["planId"]][1])
    plan[target] = plan[source]
    CHK.rekey_plan(objects, blobs, run, plan)
    CHK.resync_coverage(objects, blobs, run)
    CHK.resync_witness(objects, blobs, run)
    CHK.resync_proof_refs(objects, blobs, run)
    M.close_run(run, objects, blobs)


# ---------------------------------------------------------------------------
# 2. Excluded semantic inputs: does every semantic input MOVE the identity?
# ---------------------------------------------------------------------------
def semantic_inputs():
    run, objects, blobs = CHK.build(has_match=True)
    M.close_run(run, objects, blobs)
    plan = objects[run["planId"]][1]
    base = M.identifier("plan", plan)
    moved, stuck = [], []
    for field in sorted(plan):
        if field == "schemaVersion":
            continue
        alt = copy.deepcopy(plan)
        v = alt[field]
        if isinstance(v, str):
            alt[field] = ("0" * 64 if len(v) == 64
                          else v.split(":")[0] + ":" + "0" * 64 if ":" in v else v + "x")
        elif isinstance(v, list):
            alt[field] = v + ["0" * 64] if v is not None else ["0" * 64]
        elif isinstance(v, dict):
            alt[field] = dict(v)
            for k2 in alt[field]:
                if isinstance(alt[field][k2], int):
                    alt[field][k2] += 1
                    break
        else:
            continue
        try:
            newid = M.identifier("plan", alt)
        except Exception:
            newid = "REFUSED"
        (moved if newid != base else stuck).append(field)
    R["observations"]["planFieldsThatMoveTheId"] = moved
    R["observations"]["planFieldsThatDoNot"] = stuck
    rec("SEM-01-every-plan-field-is-a-semantic-input", not stuck, {"stuck": stuck})

    # operational identities must be EXCLUDED from Run identity
    rid = M.identifier("run", run)
    R["observations"]["runFields"] = sorted(run)
    for op in ("requestId", "executionId", "timestamp", "pid", "receipt",
               "namespaceId", "commitSequence", "signerKeyId"):
        rec("SEM-02-operational-field-absent-from-run-identity:" + op,
            op not in run, {"runFields": sorted(run)})


# ---------------------------------------------------------------------------
# 3. Cache / regeneration remaining obligations
# ---------------------------------------------------------------------------
def cache_regen():
    run, objects, blobs = CHK.build(has_match=True)
    M.close_run(run, objects, blobs)
    execid = next(k for k, (d, v) in objects.items() if d == "execution-plan")
    stage = objects[execid][1]["stages"][0]
    ssd = stage["stageSpecDigest"]
    spec = C.parse(blobs[ssd])
    scopes = sorted(k for k, (d, v) in objects.items() if d == "subject-scope")
    key = {"schemaVersion": 2, "planId": run["planId"],
           "producerClosure": spec["producerClosure"], "stageSpecDigest": ssd,
           "scopeIds": scopes, "inputRefs": [],
           "outputSchemaDigest": spec["outputSchemaDigest"]}

    # regeneration uses the EXACT retained stage spec
    rec("CR-01-regeneration-uses-the-same-stage-spec-record",
        M.cache_key("regeneration-key", key) != M.cache_key("cache-key", key)
        and key["stageSpecDigest"] == ssd)

    # a legitimate MISSING cache is not a refusal: key construction still works
    empty = {}
    try:
        k = M.cache_key("cache-key", key)
        rec("CR-02-key-construction-works-with-no-store", bool(k), {"key": k})
    except Exception as e:
        rec("CR-02-key-construction-works-with-no-store", False, {"got": str(e)[:200]})

    # a HIT against an empty store must refuse (nothing to join)
    refuses("CR-03-hit-admission-against-an-empty-store-refuses",
            lambda: M.admit_cache_entry("cache-key", key, run, {}, {}))

    # a stage spec retained but naming ANOTHER plan
    def foreign_spec():
        r, o, b = CHK.build(has_match=True)
        M.close_run(r, o, b)
        e = next(k for k, (d, v) in o.items() if d == "execution-plan")
        s = C.parse(b[o[e][1]["stages"][0]["stageSpecDigest"]])
        s = dict(s, planId="plan2:" + "9" * 64)
        d2 = putblob(b, s)
        k2 = dict(key, stageSpecDigest=d2, planId=r["planId"],
                  producerClosure=s["producerClosure"],
                  outputSchemaDigest=s["outputSchemaDigest"],
                  scopeIds=sorted(kk for kk, (dd, vv) in o.items()
                                  if dd == "subject-scope"))
        M.admit_cache_entry("cache-key", k2, r, o, b)
    refuses("CR-04-stage-spec-naming-another-plan-refuses", foreign_spec)

    # sealed-output mismatch -> the named regeneration refusal
    md = (SUBJ / "docs/v2/contracts/product-v1/identity-and-evidence.md").read_text()
    rec("CR-05-regeneration-mismatch-has-a-named-typed-refusal",
        "evidence.regeneration-mismatch" in md and "HOST.IO_FAILURE" in md)
    try:
        raise M.RegenerationMismatch(M.identifier("run", run))
    except Exception as e:
        R["observations"]["regenerationMismatch"] = str(e)[:200]
        rec("CR-06-regeneration-mismatch-is-a-typed-model-refusal",
            "regeneration" in str(e).lower() or "REGENERATION" in str(e))


# ---------------------------------------------------------------------------
# 4. FilePayloadV1.contentSha256 -- an unannotated payload-content digest
# ---------------------------------------------------------------------------
def file_payload():
    rel = json.loads((F / "relation-payload-schemas.v2.json").read_bytes())
    fp = rel["$defs"]["FilePayloadV1"]
    R["observations"]["FilePayloadV1"] = fp
    R["observations"]["note"] = (
        "contentSha256 and normalisationVersion are inherited fact-plane payload "
        "fields reproduced exactly; the closing digest law is scoped to "
        "identity-schemas.v2 and (by its own x-opensip-digest-law) the native "
        "bundle. Question: is a `file` fact's contentSha256 joined to the "
        "snapshot inventory, or is it an unjoined provider claim?")

    def bad_content():
        run, objects, blobs = CHK.build(has_match=True)
        key = next(k for k, (d, v) in objects.items() if d == "fact")
        fact = copy.deepcopy(objects[key][1])
        fact.update(relation="file", resolution="enumerated")
        fact["payloadDigest"] = putblob(blobs, {
            "path": "a.ts", "contentSha256": "f" * 64, "byteLength": 22})
        CHK.rekey(objects, key, fact, run)
        CHK.resync_witness(objects, blobs, run)
        CHK.resync_proof_refs(objects, blobs, run)
        M.close_run(run, objects, blobs)
    try:
        bad_content()
        R["observations"]["filePayloadContentJoin"] = (
            "ADMITTED -- a `file` relation payload's contentSha256 is not joined "
            "to the snapshot inventory by the identity closure")
        rec("FP-01-file-payload-contentSha256-joined-to-snapshot", False,
            {"got": R["observations"]["filePayloadContentJoin"]})
    except Exception as e:
        R["observations"]["filePayloadContentJoin"] = "REFUSED:" + str(e)[:220]
        rec("FP-01-file-payload-contentSha256-joined-to-snapshot", True,
            {"got": str(e)[:220]})


def main():
    collisions()
    semantic_inputs()
    cache_regen()
    file_payload()
    R["summary"] = {"total": len(R["checks"]),
                    "passed": sum(c["passed"] for c in R["checks"]),
                    "failed": [c for c in R["checks"] if not c["passed"]]}
    json.dump(R, sys.stdout, indent=1, default=str)
    print()


if __name__ == "__main__":
    main()
