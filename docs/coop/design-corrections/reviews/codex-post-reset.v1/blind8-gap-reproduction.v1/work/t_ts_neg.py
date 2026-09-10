import json
import sys

sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL
import osip
import run_ts

results = []


def check(name, mutate=None, store_mutate=None, expect=None):
    fx, A, run_id = run_ts.build_run(mutate)
    note = None
    if store_mutate:
        note = store_mutate(fx, A, run_id)
        if isinstance(note, tuple):
            run_id, note = note
    c = CL.Closure(fx.s)
    rep = c.close_run(run_id)
    first = rep["firstFault"]
    ok = (first == expect) if expect else (first is None)
    results.append({"vector": name, "expectedFirstRefusal": expect,
                    "observedFirstRefusal": first, "checks": rep["checks"],
                    "faultCount": len(rep["faults"]),
                    "faults": rep["faults"][:6], "note": note})
    print(("PASS " if ok else "FAIL ") + name, "->", first,
          (rep["faults"][0]["detail"][:120] if rep["faults"] else ""))


check("CB-TS-POS complete positive Run closes", None, None, None)
check("CB-TS-N1 config node kind relabelled against the published path law",
      {"relabel_config_kind": True}, None, "native.config-graph-kind-contradicts-path")
check("CB-TS-N2 stdlib inventory missing an UNSELECTED declaration library",
      {"stdlib_partial_inventory": True}, None,
      "native.native-context-stdlib-inventory-incomplete")
check("CB-TS-N3 compiler version not the admitted closure manifest's",
      {"compiler_version_not_from_manifest": True}, None,
      "native.native-context-compiler-version-not-from-manifest")
check("CB-TS-N4 tool digest outside the named closure tree",
      {"tool_outside_closure": True}, None,
      "native.native-context-tool-not-in-closure")
check("CB-TS-N5 universe contradicting its admitted context",
      {"universe_contradicts_context": True}, None,
      "native.universe-context-field-mismatch")
check("CB-TS-N6 false complete for a clones scope over an unreadable variant",
      {"false_complete_unsupported_variant": True}, None,
      "COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE")
check("CB-TS-N7 complete file@enumerated Coverage omitting an inventoried path",
      {"omit_file_fact": True}, None, "COVERAGE_INVENTORY_TOTALITY_OMITS_PATH")


# ---- store-level negatives -------------------------------------------------
def altered_frame(fx, A, run_id):
    """Mutate the retained frame so it STILL parses and is STILL canonical -
    otherwise frame parsing refuses first and the identity check is masked."""
    h = A.extra["contextHex"]
    fr = fx.s.blobs[h]
    assert b'"5.6.3"' in fr
    fx.s.blobs[h] = fr.replace(b'"5.6.3"', b'"5.6.4"')
    return ("compilerVersion edited inside the retained frame; the payload still "
            "parses and is still canonical, so the IDENTITY check is what refuses")


check("CB-TS-N8 altered retained context frame", None, altered_frame,
      "H_IDENTITY_MISMATCH")


def missing_preimage(fx, A, run_id):
    del fx.s.blobs[A.plan["capabilityManifestBytesDigest"]]
    return "capability manifest artifact bytes dropped from the store"


check("CB-TS-N9 missing preimage is retention loss", None, missing_preimage,
      "EVIDENCE_UNAVAILABLE")


def raw_payload_as_h(fx, A, run_id):
    h = A.extra["universeHex"]
    dom, val = osip.parse_frame(fx.s.blobs[h])
    fx.s.blobs[h] = osip.C(val)      # the raw canonical payload, not the frame
    return "raw canonical payload offered where an H frame is required"


check("CB-TS-N10 raw payload offered as an H identity", None, raw_payload_as_h,
      "UNIVERSE_FRAME")


def unregistered_domain(fx, A, run_id):
    desc = dict(A.contexts[A.extra["contextHex"]][1])
    h = fx.s.put_h("native.context.python.v2", desc)
    plan = dict(A.plan)
    plan["nativeContextDigests"] = sorted(plan["nativeContextDigests"] + [h],
                                          key=lambda x: osip.C(x))
    nh = fx.s.put_h("plan", plan)
    return ("run2:" + _rekey(fx, A, plan, nh),
            "a context under an unregistered H domain, re-framed and re-keyed")


def _frame(fx, typed):
    return osip.parse_frame(fx.s.blobs[typed.split(":", 1)[1]])[1]


def _rekey(fx, A, plan, plan_hex):
    """Rebuild the whole exec-plan/proof/evidence/seal/Run chain around a
    replacement Plan, so nothing is refused merely for a stale join."""
    pid = "plan2:" + plan_hex
    seal = _frame(fx, A.run["evaluationSealId"])
    ev = _frame(fx, seal["evidenceId"])
    proof = _frame(fx, seal["proofBundleId"])
    execplan = _frame(fx, proof["executionPlanId"])
    execplan = dict(execplan); execplan["planId"] = pid
    eph = fx.s.put_h("execution-plan", execplan)
    proof = dict(proof); proof["planId"] = pid
    proof["executionPlanId"] = "exec-plan2:" + eph
    ph = fx.s.put_h("proof-bundle", proof)
    ev = dict(ev); ev["planId"] = pid; ev["proofBundleId"] = "proof2:" + ph
    eh = fx.s.put_h("semantic-evidence", ev)
    seal = dict(seal); seal["planId"] = pid; seal["evidenceId"] = "evidence2:" + eh
    seal["proofBundleId"] = "proof2:" + ph
    seal["executionPlanId"] = "exec-plan2:" + eph
    sh = fx.s.put_h("evaluation-seal", seal)
    run = dict(A.run); run["planId"] = pid; run["evidenceId"] = "evidence2:" + eh
    run["evaluationSealId"] = "seal2:" + sh
    return fx.s.put_h("run", run)


check("CB-TS-N11 fully re-framed and re-keyed Run around an unregistered H domain",
      None, unregistered_domain, "H_DOMAIN_UNREGISTERED")


def hidden_input(fx, A, run_id):
    """A well-formed, hash-valid object outside the Plan's committed closure."""
    desc = dict(A.contexts[A.extra["contextHex"]][1])
    desc["packageModuleType"] = "module"
    fx.s.put_h("native.context.typescript.v2", desc)
    return "a second, hash-valid TypeScript context no Plan selected"


check("CB-TS-N12 hidden hash-valid context outside plan.nativeContextDigests",
      None, hidden_input, "PLAN_CONTEXT_SET_MISMATCH")

with open("/tmp/opensip-design-corrections/consumer-b.v8/output/"
          "vectors-typescript-run.json", "w") as f:
    json.dump(results, f, indent=1, sort_keys=True)


# ---- inventory-fact joins, clone custody, and cross-record laws ------------
print()
check("CB-TS-N13 file payload claiming a wrong content hash",
      {"file_fact_wrong_hash": True}, None, "SNAPSHOT_JOIN_DIGEST")
check("CB-TS-N14 file payload claiming a wrong byte length",
      {"file_fact_wrong_length": True}, None, "SNAPSHOT_JOIN_LENGTH")
check("CB-TS-N15 file payload naming a path in no snapshot",
      {"file_fact_path_not_inventoried": True}, None,
      "SNAPSHOT_JOIN_PATH_NOT_INVENTORIED")
check("CB-TS-N16 an INVENTORY fact carrying an anchor (class is exactly zero)",
      {"file_fact_with_anchor": True}, None, "FACT_ANCHOR_CARDINALITY")
check("CB-TS-N17 an UNANCHORED source-text fact under a TypeScript universe",
      {"declares_without_anchor": True}, None, "FACT_ANCHOR_CARDINALITY")
check("CB-TS-N18 a clones fact with two anchors",
      {"clone_two_anchors": True}, None, "FACT_ANCHOR_CARDINALITY")
check("CB-TS-N19 normalisationVersion drifting from the framed levelVersion",
      {"clone_wrong_level_version": True}, None, "BODY_FRAME_LEVEL_VERSION")
check("CB-TS-N20 the level SPECIFICATION bytes are not retained",
      {"clone_level_spec_not_retained": True}, None, "EVIDENCE_UNAVAILABLE")
check("CB-TS-N21 a .js body framed with the PROVIDER's language instead of the "
      "BODY's", {"clone_wrong_language_id": True}, None, "BODY_FRAME_LANGUAGE_ID")
check("CB-TS-N22 an L0 payload that is not the enclosing fact's own anchor span",
      {"clone_l0_payload_not_span": True}, None, "BODY_L0_PAYLOAD_NOT_ANCHOR_SPAN")
check("CB-TS-N23 two scopes of one view sharing a partition key AND a subject",
      {"partition_overlap": True}, None, "SUBJECT_SCOPE_PARTITION_OVERLAP")


def hidden_fact(fx, A, run_id):
    """A well-formed, hash-valid fact outside the evaluated view."""
    import osip as _o
    hexd, d = None, None
    for h, blob in list(fx.s.blobs.items()):
        if blob.startswith(_o.FRAME_PREFIX + b"\x00"):
            dom, val = _o.parse_frame(blob)
            if dom == "fact" and val["relation"] == "declares":
                d = dict(val)
                break
    d["confidenceMillionths"] = 999999
    fx.s.put_h("fact", d)
    return "a second hash-valid declares fact no view references"


check("CB-TS-N24 a hash-valid fact retained but referenced by NO view is an "
      "UNREFERENCED CAS blob: not an evaluation input and NOT a refusal "
      "(identity section 3, `Unreferenced CAS blobs are not evaluation inputs`) "
      "- deliberately unlike plan.nativeContextDigests, which IS a set equality",
      None, hidden_fact, None)


def cited_hidden_fact(fx, A, run_id):
    """The discriminating control: the same hidden fact CITED by a predicate
    witness, which is a citation into an object outside the evaluated view."""
    import osip as _o
    d = None
    for h, blob in list(fx.s.blobs.items()):
        if blob.startswith(_o.FRAME_PREFIX + b"\x00"):
            dom, val = _o.parse_frame(blob)
            if dom == "fact" and val["relation"] == "declares":
                d = dict(val)
                break
    d["confidenceMillionths"] = 999999
    hidden = "fact2:" + fx.s.put_h("fact", d)
    seal = _o.parse_frame(fx.s.blobs[A.run["evaluationSealId"].split(":")[1]])[1]
    proof = _o.parse_frame(fx.s.blobs[seal["proofBundleId"].split(":")[1]])[1]
    wd = proof["predicateProofs"][0]["witnessDigest"]
    w, _x = _o.admit_raw(fx.s.get(wd))
    w = dict(w); w["matchingFactIds"] = [hidden]
    nwd = fx.s.put_record(w)
    proof = dict(proof)
    pp = dict(proof["predicateProofs"][0]); pp["witnessDigest"] = nwd
    proof["predicateProofs"] = [pp]
    ph = fx.s.put_h("proof-bundle", proof)
    ev = _o.parse_frame(fx.s.blobs[seal["evidenceId"].split(":")[1]])[1]
    ev = dict(ev); ev["proofBundleId"] = "proof2:" + ph
    eh = fx.s.put_h("semantic-evidence", ev)
    seal = dict(seal); seal["evidenceId"] = "evidence2:" + eh
    seal["proofBundleId"] = "proof2:" + ph
    sh = fx.s.put_h("evaluation-seal", seal)
    run = dict(A.run); run["evidenceId"] = "evidence2:" + eh
    run["evaluationSealId"] = "seal2:" + sh
    return ("run2:" + fx.s.put_h("run", run),
            "the hidden fact is CITED by a predicate witness")


check("CB-TS-N25 a predicate witness citing a fact outside the evaluated view",
      None, cited_hidden_fact, "WITNESS_FACT_OUTSIDE_EVALUATED_VIEW")

with open("/tmp/opensip-design-corrections/consumer-b.v8/output/"
          "vectors-typescript-run.json", "w") as f:
    json.dump(results, f, indent=1, sort_keys=True)
