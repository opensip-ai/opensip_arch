#!/usr/bin/env python3
"""P08: capability manifest admission (Bv2 G6), ExecutionId anchoring (G7),
enumerator closure kind (G11), the ADV-B1 budget equality, G4 relocation prose,
and the CVE1 recipe. Independent vectors; exact typed causes.
"""
import contextlib, copy, hashlib, importlib.util, io, json, re, sys
from pathlib import Path

SUBJ = Path("/tmp/opensip-design-corrections/candidate-subject.v8")
F = SUBJ / "docs/coop/design-corrections/foundation"
NATD = SUBJ / "docs/coop/design-corrections/native"
CONTRACTS = SUBJ / "docs/v2/contracts/product-v1"


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
N = load("nat", NATD / "native_evidence_model.v2.py")
CHK = load("idcheck", F / "check-identity.py", True)

R = {"checks": [], "observations": {}}


def rec(n, ok, d=None):
    R["checks"].append({"id": n, "passed": bool(ok), "detail": d})


# ---------------------------------------------------------------------------
# G6: capability manifest -- four inherited gates, CVE1, unresolved-edge
# ---------------------------------------------------------------------------
def capability():
    inherited = CHK.INHERITED_MANIFEST_BYTES
    current = CHK.CURRENT_CAPABILITY_MANIFEST_BYTES

    # the INHERITED twelve-relation golden still admits unchanged (CVE1 unchanged)
    a = N.admit_capability_manifest(inherited)
    rec("CAP-01-inherited-golden-still-admits", a["result"] == "ADMIT",
        {"refusals": a["refusals"], "relations": a["relations"]})
    R["observations"]["inheritedManifestId"] = a["capabilityManifestId"]
    rec("CAP-02-inherited-golden-is-twelve-relations",
        sorted(a["relations"]) == sorted([
            "calls", "clones", "control-flow", "declares", "file", "imports",
            "literal", "package", "reachability", "references", "types",
            "vcs-change"]), {"relations": sorted(a["relations"])})

    # the CURRENT manifest declares the thirteenth relation at rung `observed`
    b = N.admit_capability_manifest(current)
    rec("CAP-03-current-manifest-admits-unresolved-edge",
        b["result"] == "ADMIT" and "unresolved-edge" in b["relations"],
        {"result": b["result"], "refusals": b["refusals"],
         "hasUnresolvedEdge": "unresolved-edge" in b["relations"]})
    R["observations"]["currentManifestId"] = b["capabilityManifestId"]

    # CVE1 identity recipe, recomputed independently from the prose
    mine = hashlib.sha256(b"opensip.capability-manifest.v1\x00" + current).hexdigest()
    rec("CAP-04-CVE1-identity-recipe-reproduced-independently",
        mine == b["capabilityManifestId"],
        {"mine": mine, "model": b["capabilityManifestId"]})
    # and CVE1 is UNCHANGED: the inherited bytes still mint the inherited id
    mine_i = hashlib.sha256(b"opensip.capability-manifest.v1\x00" + inherited).hexdigest()
    rec("CAP-05-CVE1-unchanged-for-inherited-bytes",
        mine_i == a["capabilityManifestId"])

    # --- the four gates, attacked -----------------------------------------
    def mutated(fn):
        value = N.cve1_decode(current)
        fn(value)
        return N.admit_capability_manifest(N.cve1_encode(value))

    def refuses(name, fn, token):
        r = mutated(fn)
        rec(name, r["result"] == "REFUSE" and any(token in x for x in r["refusals"]),
            {"expect": token, "result": r["result"], "refusals": r["refusals"][:6]})

    # ADM-TYPE: a boolean is not an integer schemaVersion
    refuses("CAP-06-ADM-TYPE-boolean-schemaVersion",
            lambda v: v.update(schemaVersion=True), "capability.adm-type")
    refuses("CAP-07-ADM-TYPE-non-string-profile",
            lambda v: v.update(profile=1), "capability.adm-type")
    refuses("CAP-08-ADM-TYPE-non-list-providers",
            lambda v: v.update(providers={}), "capability.adm-type")
    refuses("CAP-09-ADM-TYPE-non-string-providerId",
            lambda v: v["providers"][0].update(providerId=7), "capability.adm-type")

    # ADM-CLOSED: an extra key
    refuses("CAP-10-ADM-CLOSED-extra-key",
            lambda v: v.update(reviewExtraKey="x"), "capability.adm-closed")
    refuses("CAP-11-ADM-CLOSED-missing-key",
            lambda v: v.pop("profile"), "capability.adm-closed")

    # ADM-DOMAIN: an unregistered relation, and a rung from ANOTHER ladder
    refuses("CAP-12-ADM-DOMAIN-unregistered-relation",
            lambda v: v["providers"][0]["relations"].update({"invented": "observed"}),
            "capability.adm-domain:relation")
    refuses("CAP-13-ADM-DOMAIN-rung-from-another-ladder",
            lambda v: v["providers"][0]["relations"].update({"references": "resolved-callee"}),
            "capability.adm-domain:rung")
    refuses("CAP-14-ADM-DOMAIN-unregistered-platform",
            lambda v: v["providers"][0]["platformIds"].append("mainframe-z"),
            "capability.adm-domain:platformId")

    # ADM-ORDER: duplicate and out-of-order platform ids
    def dup_platform(v):
        p = v["providers"][0]["platformIds"]
        v["providers"][0]["platformIds"] = list(p) + [p[0]]
    refuses("CAP-15-ADM-ORDER-duplicate-platform", dup_platform,
            "capability.adm-order")

    def unsorted_platform(v):
        p = sorted(v["providers"][0]["platformIds"], reverse=True)
        if len(p) < 2:
            p = p + p
        v["providers"][0]["platformIds"] = p
    refuses("CAP-16-ADM-ORDER-unsorted-platform", unsorted_platform,
            "capability.adm-order")

    def dup_relation_ids(v):
        if v["coverageForAbsent"]:
            r = v["coverageForAbsent"][0]["relationIds"]
            v["coverageForAbsent"][0]["relationIds"] = list(r) + [r[0]]
    refuses("CAP-17-ADM-ORDER-duplicate-relationIds", dup_relation_ids,
            "capability.adm-order")

    # a duplicated whole provider row
    def dup_provider(v):
        v["providers"] = list(v["providers"]) + [copy.deepcopy(v["providers"][0])]
    r = mutated(dup_provider)
    rec("CAP-18-duplicate-provider-row-refused", r["result"] == "REFUSE",
        {"result": r["result"], "refusals": r["refusals"][:6]})

    # the manifest bytes are the PlanId input: a refused manifest cannot enter
    def bad_manifest_run():
        run, objects, blobs = CHK.build(has_match=True)
        value = N.cve1_decode(CHK.CURRENT_CAPABILITY_MANIFEST_BYTES)
        value["providers"][0]["relations"]["references"] = "resolved-callee"
        raw = N.cve1_encode(value)
        plan = copy.deepcopy(objects[run["planId"]][1])
        d = hashlib.sha256(raw).hexdigest()
        blobs[d] = raw
        plan["capabilityManifestBytesDigest"] = d
        plan["capabilityManifestId"] = hashlib.sha256(
            b"opensip.capability-manifest.v1\x00" + raw).hexdigest()
        run["capabilityManifestId"] = plan["capabilityManifestId"]
        CHK.rekey_plan(objects, blobs, run, plan)
        CHK.resync_coverage(objects, blobs, run)
        CHK.resync_witness(objects, blobs, run)
        CHK.resync_proof_refs(objects, blobs, run)
        M.close_run(run, objects, blobs)
    try:
        bad_manifest_run()
        rec("CAP-19-refused-manifest-cannot-enter-a-Plan", False, {"got": "ADMITTED"})
    except Exception as exc:
        rec("CAP-19-refused-manifest-cannot-enter-a-Plan", True, {"got": str(exc)[:250]})


# ---------------------------------------------------------------------------
# G7: ExecutionId / RequestId absolute end anchor
# ---------------------------------------------------------------------------
def execution_id():
    ids = json.loads((F / "identity-schemas.v2.json").read_bytes())
    common = json.loads(
        (SUBJ / "docs/coop/design-corrections/workflows/schemas/common.schema.json").read_bytes())
    c2 = json.loads((SUBJ / "docs/coop/artifacts/c2-plan-stage-schema.v4.json").read_bytes())

    exec_id = ids["$defs"]["commit-receipt"]["properties"]["executionId"]
    R["observations"]["identityExecutionIdPattern"] = exec_id.get("pattern")
    wf = common["$defs"]["ExecutionId"]
    R["observations"]["workflowExecutionIdPattern"] = wf.get("pattern")
    c2p = c2["planIntent"]["wireTypes"]["executionId"]["pattern"]
    R["observations"]["c2RetainedProvenancePattern"] = c2p

    rec("EXEC-01-identity-successor-is-end-anchored",
        exec_id.get("pattern") == r"^exec1_[0-9a-f]{32}(?![\s\S])")
    rec("EXEC-02-workflow-successor-matches-identity",
        wf.get("pattern") == exec_id.get("pattern"))
    rec("EXEC-03-c2-provenance-selector-retained-unchanged",
        c2p.endswith("$") and "(?![" not in c2p, {"c2": c2p})
    # behavioural: the successor refuses a trailing newline; the C-2 bytes admit it
    val = "exec1_" + "a" * 32 + "\n"
    rec("EXEC-04-successor-refuses-trailing-newline",
        re.match(exec_id["pattern"].replace(r"(?![\s\S])", r"(?![\s\S])"), val) is None
        if "(?!" in exec_id["pattern"] else False,
        {"note": "python re: (?![\\s\\S]) is a real end assertion"})
    rec("EXEC-05-c2-bytes-would-admit-trailing-newline",
        re.match(c2p, val) is not None, {"c2Pattern": c2p})
    # the contract must SAY the successor is deliberately non-equivalent
    md = (CONTRACTS / "identity-and-evidence.md").read_text()
    rec("EXEC-06-contract-declares-deliberate-non-equivalence",
        "not byte-equivalent to the product" in md
        and "product successor grammar is end-anchored" in md
        and "same deliberate non-equivalence security" in md)
    rec("EXEC-07-RequestId-on-the-same-rule",
        r"^req1_[0-9a-f]{32}(?![\s\S])" in md)


# ---------------------------------------------------------------------------
# G11: enumerator closure kind
# ---------------------------------------------------------------------------
def enumerator_kind():
    ids = json.loads((F / "identity-schemas.v2.json").read_bytes())
    reg = ids["x-opensip-digest-domains"]
    scope = ids["$defs"]["subject-scope"]["properties"]["enumeratorClosure"]
    R["observations"]["enumeratorClosureSchema"] = scope
    md = (CONTRACTS / "native-evidence.md").read_text()
    idmd = (CONTRACTS / "identity-and-evidence.md").read_text()
    # is a kind stated anywhere?
    stated = ("enumeratorClosure" in md or "enumeratorClosure" in idmd)
    kind_named = re.search(r"enumerator[^.]{0,200}?kind\s*[=`]?\s*(provider|toolchain|detector)",
                           md + idmd, re.I | re.S)
    R["observations"]["enumeratorKindStatedIn"] = {
        "nativeMd": "enumeratorClosure" in md,
        "identityMd": "enumeratorClosure" in idmd,
        "kindPhraseFound": bool(kind_named),
        "phrase": kind_named.group(0)[:200] if kind_named else None,
    }
    # does the model ENFORCE a kind?
    src = (F / "identity-model.py").read_text()
    enforced = "enumeratorClosure" in src
    R["observations"]["enumeratorKindEnforcedInModel"] = enforced
    # find the registry row
    row = None
    for k, v in reg.get("byDomain", {}).items():
        if k == "closure":
            row = v
    R["observations"]["closureDomainRow"] = row
    rec("ENUM-01-enumerator-closure-kind-is-stated", bool(kind_named),
        R["observations"]["enumeratorKindStatedIn"])

    # behavioural: does a non-provider enumerator kind actually refuse?
    def try_kind(kind):
        run, objects, blobs = CHK.build(has_match=True)
        skey = next(k for k, (d, v) in objects.items() if d == "subject-scope")
        ekey = objects[skey][1]["enumeratorClosure"]
        closure = copy.deepcopy(objects[ekey][1])
        closure["kind"] = kind
        CHK.rekey(objects, ekey, closure, run)
        CHK.resync_coverage(objects, blobs, run)
        CHK.resync_witness(objects, blobs, run)
        CHK.resync_proof_refs(objects, blobs, run)
        return M.close_run(run, objects, blobs)
    for kind in ("provider", "detector", "evaluator", "adapter", "stdlib"):
        try:
            try_kind(kind)
            outcome = "ADMITTED"
        except Exception as exc:
            outcome = "REFUSED:" + str(exc)[:120]
        R["observations"].setdefault("enumeratorKindBehaviour", {})[kind] = outcome


# ---------------------------------------------------------------------------
# ADV-B1: plan.budget vs the committed resolved configuration budget
# ---------------------------------------------------------------------------
def budget():
    ids = json.loads((F / "identity-schemas.v2.json").read_bytes())
    pb = ids["$defs"]["plan"]["properties"]["budget"]
    cb = (ids["$defs"]["semantic-configuration"]["properties"]["analysis"]
          ["properties"]["budget"])
    R["observations"]["planBudgetSchema"] = pb
    rec("BUD-01-plan-budget-is-a-closed-record",
        pb.get("additionalProperties") is False
        and sorted(pb.get("required", [])) == ["limit", "unit"], {"schema": pb})
    rec("BUD-02-plan-budget-byte-identical-to-config-budget",
        C.canonical(pb) == C.canonical(cb))
    rec("BUD-03-G8-false-premise-not-reinstated",
        pb != {"type": "object"},
        {"note": "G8 claimed a bare {type:object}; the frozen bytes are closed. "
                 "The retraction is correct and no 'schema correction' is claimed."})

    # ADV-B1: is the equality now ENFORCED?
    def divergent():
        run, objects, blobs = CHK.build(has_match=True)
        plan = copy.deepcopy(objects[run["planId"]][1])
        plan["budget"] = {"unit": "work-units", "limit": 7}
        CHK.rekey_plan(objects, blobs, run, plan)
        CHK.resync_coverage(objects, blobs, run)
        CHK.resync_witness(objects, blobs, run)
        CHK.resync_proof_refs(objects, blobs, run)
        M.close_run(run, objects, blobs)
    try:
        divergent()
        rec("BUD-04-ADV-B1-divergent-budget-refused", False,
            {"got": "ADMITTED -- the Plan's inline budget may contradict its "
                    "own committed resolved configuration"})
    except Exception as exc:
        rec("BUD-04-ADV-B1-divergent-budget-refused", True, {"got": str(exc)[:250]})

    # and the equality must be STATED in the contract, not only coded
    md = (CONTRACTS / "identity-and-evidence.md").read_text()
    R["observations"]["budgetEqualityProse"] = [
        line.strip() for line in md.splitlines()
        if "budget" in line.lower() and ("agree" in line.lower() or "equal" in line.lower())]
    rec("BUD-05-budget-equality-is-stated-in-prose",
        bool(R["observations"]["budgetEqualityProse"]),
        {"lines": R["observations"]["budgetEqualityProse"]})


# ---------------------------------------------------------------------------
# G4: the "Retained:" prose that named three relocated fields
# ---------------------------------------------------------------------------
def relocation_prose():
    md = (CONTRACTS / "native-evidence.md").read_text()
    nd = json.loads((NATD / "native-evidence.schemas.v2.json").read_bytes())
    univ = set(nd["$defs"]["TypeScriptUniverseV2ResolvedInputs"]["properties"])
    ctx = set(nd["$defs"]["TypeScriptNativeContextV2"]["properties"])
    moved = ["compilerOptions", "packageLockIdentity", "resolvedNodeModulesLayout"]
    R["observations"]["G4"] = {
        "universeProperties": sorted(univ),
        "namedButAbsentFromUniverse": [m for m in moved if m not in univ],
        "relocationLanguageInProse": [
            line.strip() for line in md.splitlines()
            if "relocat" in line.lower() or ("Retained:" in line)],
    }
    rec("G4-01-prose-no-longer-lists-relocated-fields-as-universe-Retained",
        not any(re.search(r"Retained:.*(compilerOptions|packageLockIdentity|resolvedNodeModulesLayout)",
                          line) for line in md.splitlines()),
        {"retainedLines": [l.strip() for l in md.splitlines() if "Retained:" in l][:6]})
    rec("G4-02-relocation-is-explained-somewhere",
        "relocat" in md.lower() or "moved to" in md.lower(),
        {"found": [l.strip()[:160] for l in md.splitlines()
                   if "relocat" in l.lower() or "moved to" in l.lower()][:5]})


def main():
    capability()
    execution_id()
    enumerator_kind()
    budget()
    relocation_prose()
    R["summary"] = {"total": len(R["checks"]),
                    "passed": sum(c["passed"] for c in R["checks"]),
                    "failed": [c for c in R["checks"] if not c["passed"]]}
    json.dump(R, sys.stdout, indent=1, default=str)
    print()


if __name__ == "__main__":
    main()
