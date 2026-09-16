"""Discriminating semantic-replay controls (composition s7): mutate ONE evaluator output value of a passing exported
Run, independently re-mint every enclosing identity (finding3 -> proof3 -> evidence3 -> seal3 -> run3 and
policy-derivation3) so no stale hash remains, then run the complete closure in this process on the tampered store.
Expected: graph admission ADMITS (identities are internally consistent) and semantic replay REFUSES.
Usage: python3 tools/runref.py tools/tamper_outputs.py runs/<v>.store.json runs/<v>.tamper-outputs.json
"""
import copy
import hashlib
import json
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1/output/preserved/pre-s41"
sys.path.insert(0, OUT + "/ref")

import canonical as K  # noqa: E402
import closure  # noqa: E402
from store import Store  # noqa: E402


def sfx(i):
    return i.split(":", 1)[1]


def ckey(x):
    return K.C(x)


def get(store, ident, domain):
    return store.get_frame(sfx(ident), {domain})[1]


def remint(store, run_id, proof, finding_map):
    """finding_map: old finding3 id -> new finding3 id (or None for removal). Rebuilds proof/evidence/seal/run/pd."""
    run = get(store, run_id, "run")
    seal = get(store, run["evaluationSealId"], "evaluation-seal")
    evidence = get(store, run["evidenceId"], "semantic-evidence")
    plan = get(store, run["planId"], "plan")

    def remap(ids):
        out = []
        for i in ids:
            n = finding_map.get(i, i)
            if n is not None:
                out.append(n)
        return sorted(set(out), key=ckey)
    proof = copy.deepcopy(proof)
    proof["findingIds"] = remap(proof["findingIds"])
    proof["waivedFindingIds"] = remap(proof["waivedFindingIds"])
    for rr in proof["ruleResults"]:
        rr["findingIds"] = remap(rr["findingIds"])
    proof_id = store.put_object("proof-bundle", proof)
    evidence = dict(evidence, findingIds=proof["findingIds"], proofBundleId=proof_id)
    evidence_id = store.put_object("semantic-evidence", evidence)
    seal = dict(seal, evidenceId=evidence_id, proofBundleId=proof_id, verdict=proof["verdict"])
    seal_id = store.put_object("evaluation-seal", seal)
    run = dict(run, evidenceId=evidence_id, evaluationSealId=seal_id)
    new_run = store.put_object("run", run)
    store.put_object("policy-derivation", {"schemaVersion": 3, "planId": run["planId"], "proofBundleId": proof_id,
                                           "policyDigest": plan["policyDigest"], "waiverDigest": plan["waiverDigest"], "verdict": proof["verdict"]})
    return new_run


def reframe_finding(store, fid, mutate):
    f = copy.deepcopy(get(store, fid, "finding"))
    mutate(f)
    return store.put_object("finding", f)


def controls(exported):
    base = Store.load(exported)
    run_id = exported["runId"]
    run = get(base, run_id, "run")
    seal = get(base, run["evaluationSealId"], "evaluation-seal")
    proof0 = get(base, seal["proofBundleId"], "proof-bundle")
    out = []

    def case(name, fn):
        store = Store.load(exported)
        try:
            new_run, detail = fn(store)
        except Exception as exc:  # a control that cannot be constructed is reported, never silently skipped
            out.append({"control": name, "constructed": False, "error": repr(exc)})
            return
        rep = closure.close_run(store, new_run)
        out.append({"control": name, "constructed": True, "detail": detail, "tamperedRunId": new_run, "originalRunId": run_id,
                    "result": rep["result"], "firstRefusal": rep.get("firstRefusal"), "graphFaults": rep["graphAdmission"]["faults"][:6],
                    "retainedClosureFaults": rep.get("retainedClosure", {}).get("faults", [])[:6],
                    "replayPerformed": rep["semanticReplay"].get("performed", False),
                    "replayFaults": rep["semanticReplay"].get("faults", [])[:6],
                    # HC-33: refused BY REPLAY only when both earlier stages admitted and replay actually ran
                    "refusedBySemanticReplay": rep["result"] == "REFUSE" and not rep["graphAdmission"]["faults"]
                    and rep.get("retainedClosure", {}).get("result") == "ADMIT" and rep["semanticReplay"].get("performed", False)})

    live = [i for i in proof0["findingIds"] if i not in proof0["waivedFindingIds"]]
    target = (live or proof0["findingIds"])[0]

    def param_value(store):
        f = get(store, target, "finding")
        params = copy.deepcopy(store.get_record(f["parameterDigest"]))
        params["parameters"]["matchingFactCount"] += 1
        pd = store.put_record(params)
        nf = reframe_finding(store, target, lambda x: x.__setitem__("parameterDigest", pd))
        return remint(store, run_id, proof0, {target: nf}), "matchingFactCount+1 (same finding count)"

    def citation(store):
        for fid in proof0["findingIds"]:
            f = get(store, fid, "finding")
            drop = next((r for r in f["evidenceRefs"] if r["domain"] in ("coverage", "fact", "import")), None)
            if drop is not None:
                nf = reframe_finding(store, fid, lambda x, drop=drop: x.__setitem__("evidenceRefs", [r for r in x["evidenceRefs"] if r != drop]))
                return remint(store, run_id, proof0, {fid: nf}), f"removed evidenceRef {drop['domain']} from {f['ruleId']}"
        raise ValueError("no finding with a droppable citation")

    def severity(store):
        nf = reframe_finding(store, target, lambda x: x.__setitem__("severity", "error" if x["severity"] != "error" else "warning"))
        return remint(store, run_id, proof0, {target: nf}), "severity changed"

    def waiver_membership(store):
        p = copy.deepcopy(proof0)
        if p["waivedFindingIds"]:
            p["waivedFindingIds"] = []
            d = "waivedFindingIds emptied"
        else:
            p["waivedFindingIds"] = [p["findingIds"][0]]
            d = "waivedFindingIds added"
        return remint(store, run_id, p, {}), d

    def enumeration(store):
        p = copy.deepcopy(proof0)
        rr = next(r for r in p["ruleResults"] if r["enumeration"]["selectedSubjectIds"])
        rr["enumeration"]["selectedSubjectIds"] = rr["enumeration"]["selectedSubjectIds"][1:]
        return remint(store, run_id, p, {}), f"dropped a selected subject of {rr['ruleId']}"

    def drop_finding(store):
        return remint(store, run_id, proof0, {target: None}), "removed one finding from proof and rule result"

    def witness(store):
        p = copy.deepcopy(proof0)
        pp = next(x for x in p["predicateProofs"] if x["operation"] != "and")
        w = copy.deepcopy(store.get_record(pp["witnessDigest"]))
        w["deficiencies"] = w["deficiencies"] + [{"source": "native", "cause": "coverage-unknown", "subjectId": pp["subjectId"],
                                                  "predicateId": pp["predicateId"], "inputRefs": [], "evidenceKind": None,
                                                  "nativeCause": None, "universe": None}]
        w["deficiencies"] = sorted({K.C(d): d for d in w["deficiencies"]}.values(), key=ckey)
        pp["witnessDigest"] = store.put_record(w)
        return remint(store, run_id, p, {}), "added a deficiency to one witness and re-keyed it"

    def verdict(store):
        p = copy.deepcopy(proof0)
        p["verdict"] = "fail" if p["verdict"] != "fail" else "pass"
        return remint(store, run_id, p, {}), f"verdict -> {p['verdict']}"

    def predicate_value(store):
        p = copy.deepcopy(proof0)
        pp = next(x for x in p["predicateProofs"] if x["value"] == "false")
        pp["value"] = "indeterminate"
        return remint(store, run_id, p, {}), f"predicate {pp['predicateId']} false -> indeterminate"

    def imported_address(store):
        p = copy.deepcopy(proof0)
        for pp in p["predicateProofs"]:
            w = store.get_record(pp["witnessDigest"])
            if w["matchingImportRows"]:
                w = copy.deepcopy(w)
                row = w["matchingImportRows"][0]
                row["ordinal"] = 0 if row["ordinal"] != 0 else 1
                w["matchingImportRows"] = sorted({K.C(r): r for r in w["matchingImportRows"]}.values(), key=ckey)
                old = pp["witnessDigest"]
                pp["witnessDigest"] = store.put_record(w)
                fmap = {}
                for fid in proof0["findingIds"]:
                    f = get(store, fid, "finding")
                    if any(r["domain"] == "predicate-witness" and r["digest"] == old for r in f["evidenceRefs"]):
                        refs = [dict(r, digest=pp["witnessDigest"]) if r["digest"] == old else r for r in f["evidenceRefs"]]
                        fmap[fid] = reframe_finding(store, fid, lambda x, refs=refs: x.__setitem__("evidenceRefs", sorted(refs, key=ckey)))
                return remint(store, run_id, p, fmap), f"matchingImportRows ordinal changed on {pp['ruleId']} {pp['predicateId']}"
        raise ValueError("no imported atom witness in this Run")

    for name, fn in (("parameter-value", param_value), ("citation", citation), ("severity", severity),
                     ("waiver-membership", waiver_membership), ("enumeration", enumeration), ("finding-removed", drop_finding),
                     ("witness", witness), ("verdict", verdict), ("predicate-value", predicate_value),
                     ("imported-address", imported_address)):
        case(name, fn)
    # identity-level (non-reminted) controls, expected to refuse at graph admission
    def stale_hash(store):
        p = copy.deepcopy(proof0)
        p["verdict"] = "fail"
        hx = sfx(seal["proofBundleId"])
        store.blobs[hx] = K.frame("proof-bundle", p)  # bytes no longer hash to their key
        return run_id, "proof frame bytes replaced under the old key (no remint)"

    def missing_preimage(store):
        del store.blobs[proof0["executionInputsDigest"]]
        return run_id, "execution-inputs blob removed"

    def missing_output_preimage(store):
        wd = proof0["predicateProofs"][0]["witnessDigest"]
        del store.blobs[wd]
        return run_id, "one witness blob removed"

    for name, fn in (("stale-hash-no-remint", stale_hash), ("missing-input-preimage", missing_preimage),
                     ("missing-output-preimage", missing_output_preimage)):
        case(name, fn)
    return out


def main(src, dst):
    raw = open(src, "rb").read()
    res = controls(json.loads(raw))
    identity = {"stale-hash-no-remint", "missing-input-preimage", "missing-output-preimage"}
    constructed_semantic = [c for c in res if c["control"] not in identity and c.get("constructed")]
    doc = {"store": src, "storeSha256": hashlib.sha256(raw).hexdigest(), "controls": res,
           "semanticControlsConstructed": [c["control"] for c in constructed_semantic],
           "semanticControlsNotConstructed": [c["control"] for c in res if c["control"] not in identity and not c.get("constructed")],
           "allSemanticControlsRefusedByReplay": all(c.get("refusedBySemanticReplay") for c in constructed_semantic),
           "allIdentityControlsRefused": all(c.get("result") == "REFUSE" for c in res if c["control"] in identity)}
    with open(dst, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    for c in res:
        print(c["control"], c.get("result"), "graph:", c.get("graphFaults", [])[:2], "replay:", c.get("replayFaults", [])[:2], c.get("error", ""))
    print("semantic-all-refused-by-replay", doc["allSemanticControlsRefusedByReplay"], "identity-all-refused", doc["allIdentityControlsRefused"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
