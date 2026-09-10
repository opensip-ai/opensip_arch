#!/usr/bin/env python3
"""Read-only integration probes for full execution replay. Not a Run. No core edits."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path("/tmp/opensip-design-corrections/evaluator-successor.v1/docs/coop/design-corrections/foundation")
PY_NOTE = "python3.12 /tmp/opensip-architecture-review-env/bin/python -I -B"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


F = load("probe_F", "evaluator_graph_fixture.v3.py")
X = load("probe_X", "execution_inputs_fixture.v3.py")
Mexec = load("probe_Mexec", "execution_inputs_model.v1.py")
I = load("probe_I", "evaluator_input_model.v3.py")
R = load("probe_R", "evaluator_replay_model.v3.py")
S = load("probe_S", "evaluator_semantic_fixture.v3.py")
Ident = R.M
C = Ident.C
E = R.E

rows = []


def rec(name, **fields):
    rows.append({"probe": name, **fields})


def derive_graph(g):
    seed, objects, blobs, _ = F.seal_fixture(g)
    _, owner = Ident.open_run_closure(seed, objects, blobs)
    i = g["inputs"]
    out = R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"], i["evaluationInputRefs"], objects, blobs, owner)
    run, objects, blobs = S.seal_derived(g, out, objects, blobs)
    result = R.replay(run, objects, blobs)
    assert Ident.close_run(run, objects, blobs) == result["runId"]
    return (run, objects, blobs), result, out["proof"], g, owner


def near_candidate_admit(*, groups_map, drop_group_blob=False, authority="candidate-only"):
    g = F.build_file_inputs()
    owner = X.admission_kwargs(g)
    uni = "c" * 64
    prov = next(k for k, v in owner["closures"].items() if v.get("kind") == "provider")
    snap = owner["objects"][owner["plan"]["snapshotId"]][1]
    row = next(r for r in snap["sourceInventory"] if r["path"] == "src/index.ts")
    bodies = [{
        "id": "body-a", "path": "src/index.ts", "contentSha256": row["sha256"],
        "byteLength": row["bytes"], "universe": uni,
    }]
    group = {
        "mode": "near", "evidenceLevel": "similar-candidate", "language": "typescript",
        "members": ["body-a"], "authority": authority,
        "matchedEdges": [{"left": "body-a", "right": "body-a", "similarityMillionths": 900000}],
        "grouping": "connected-component", "scoreMeaning": "minimum-member-best-neighbor",
        "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False,
    }
    gd = Mexec.raw_digest(group)
    env = {
        "schemaVersion": 1, "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
        "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near", "languageMode": "syntax-only",
        "universe": uni, "producerClosure": prov, "stageOrdinal": 0, "state": "complete",
        "deficiency": None, "nativeCause": None, "authority": "candidate-only",
        "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False,
        "examinedPaths": ["src/index.ts"], "groupDigests": [gd],
        "sourceBodies": sorted(bodies, key=C.canonical),
    }
    ed = Mexec.raw_digest(env)
    near_spec = {"requestedCapabilities": [
        {"capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True}]}
    near_enum = {
        "schemaVersion": 1, "snapshotId": owner["plan"]["snapshotId"],
        "scopeDigest": owner["plan"]["scopeDigest"], "membershipDigest": "1" * 64,
        "cells": [{"capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".",
                   "required": True, "kinds": [], "programBindings": [{
                       "ordinal": 0, "provenance": "default-unit",
                       "enumerator": {"status": "selected", "closureId": prov},
                       "nativeContextDigest": "b" * 64, "universe": uni, "programEntry": None,
                       "extents": [], "candidateSourcePaths": ["src/index.ts"],
                   }]}],
    }
    stage_d = owner["execution_plan"]["stages"][0]["stageSpecDigest"]
    host_derived = [{"domain": "candidate-producer-result", "digest": ed}]
    manifest = {
        "schemaVersion": 1, "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
        "evaluatorClosure": owner["execution_inputs"]["evaluatorClosure"],
        "enumerationPlanDigest": Mexec.raw_digest(near_enum),
        "analysisSpecDigest": Mexec.raw_digest(near_spec),
        "hostCapture": {
            "custody": "host-tcb-evidence-store", "observation": "stage-return",
            "stageReceipts": [{
                "ordinal": 0, "stageSpecDigest": stage_d,
                "producerClosure": owner["stage_specs"][stage_d]["producerClosure"],
                "outputDomains": list(owner["stage_specs"][stage_d]["outputDomains"]),
                "outputRefs": [], "state": "complete", "unavailableReason": None,
            }],
            "hostDerivedRefs": X.canon_refs(host_derived),
        },
        "selectedRefs": X.canon_refs(host_derived),
        "cellOutcomes": [{
            "ordinal": 0, "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near",
            "languageMode": "syntax-only", "workspaceRoot": ".", "required": True, "kinds": [],
            "universe": uni, "enumeratorStatus": "selected", "enumeratorClosure": prov,
            "state": "complete", "deficiency": None, "nativeCause": None,
            "stageOrdinal": 0, "stageOrdinalNullReason": None,
            "inventoryDigests": [], "viewDigests": [], "candidateResultDigest": ed,
        }],
        "nativeCoverageAccounts": [], "candidateResultRefs": [ed],
    }
    blobs = dict(owner["blobs"])
    blobs[gd] = C.canonical(group)
    blobs[ed] = C.canonical(env)
    if drop_group_blob:
        del blobs[gd]
    near_plan = dict(owner["plan"])
    near_plan["analysisSpecDigest"] = Mexec.raw_digest(near_spec)
    promised = Mexec.promised_pointers(
        manifest, near_plan, owner["execution_plan"], near_enum,
        objects=owner["objects"], blobs=blobs,
    )
    return Mexec.admit_execution_inputs(
        plan_id=owner["plan_id"], plan=near_plan,
        execution_plan_id=owner["execution_plan_id"], execution_plan=owner["execution_plan"],
        enumeration_plan=near_enum, analysis_spec=near_spec, execution_inputs=manifest,
        objects=owner["objects"], blobs=blobs, store_pointers=promised["store_pointers"],
        inventories={}, imports={}, target_attributions={}, incoming_searches={},
        candidate_results={ed: env}, groups={gd: group} if groups_map else {},
        closures=owner["closures"], stage_specs=owner["stage_specs"],
        vcs_observation=owner["vcs_observation"],
    ), promised, gd, ed


def main():
    g = F.build_file_inputs(atom_override={"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []})
    packed, result, proof, g, owner = derive_graph(g)
    run, objects, blobs = packed
    manifest = C.parse(blobs[proof["executionInputsDigest"]])
    exec_refs = [r for r in proof["evaluationInputRefs"] if r["domain"] == "execution-inputs"]
    rec(
        "inputRefs-equal-selectedRefs-plus-self",
        ok=C.equal_typed(proof["evaluationInputRefs"], E.cset(manifest["selectedRefs"] + exec_refs))
        and len(exec_refs) == 1 and exec_refs[0]["digest"] == proof["executionInputsDigest"],
        evaluationInputRefs=len(proof["evaluationInputRefs"]),
        selectedRefs=len(manifest["selectedRefs"]),
    )
    rec(
        "proof-executionInputsDigest-equals-stored-blob",
        ok=proof["executionInputsDigest"] == g["inputs"]["executionInputsDigest"]
        and hashlib.sha256(blobs[proof["executionInputsDigest"]]).hexdigest() == proof["executionInputsDigest"],
        digest=proof["executionInputsDigest"],
    )
    pred_ok = True
    for pred in proof["predicateProofs"]:
        if not {C.canonical(r) for r in pred["inputRefs"]} <= {C.canonical(r) for r in proof["evaluationInputRefs"]}:
            pred_ok = False
    rec("predicate-inputRefs-subseteq-evaluationInputRefs", ok=pred_ok, predicateCount=len(proof["predicateProofs"]))

    # Ambient: same digest and Run.
    g2 = F.build_file_inputs(atom_override={"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []})
    raw = b"unrelated cached bytes, never selected"
    g2["blobs"][hashlib.sha256(raw).hexdigest()] = raw
    closure = {"schemaVersion": 2, "kind": "provider", "manifestDigest": hashlib.sha256(raw).hexdigest(),
               "tree": [], "semanticVersion": "9.0.0", "protocolMajor": 3, "platform": "any"}
    key = Ident.identifier("closure", closure)
    g2["objects"][key] = ("closure", closure)
    packed2, result2, proof2, g2, _ = derive_graph(g2)
    rec(
        "ambient-blob-and-object-preserve-manifest-and-run",
        ok=g2["executionInputsDigest"] == g["executionInputsDigest"] and result2["runId"] == result["runId"],
        digest=g["executionInputsDigest"], runId=result["runId"],
    )

    # Missing package work: original join cause vs projected execution deficiency.
    gp = F.build_file_inputs(
        atom_override={"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []},
        complete_required_native=False,
    )
    _, pr, pp, gp, _ = derive_graph(gp)
    join = C.parse(gp["blobs"][pp["executionInputsDigest"]])
    attached_adm = X.attach_host_capture(copy.deepcopy(F.build_file_inputs(
        atom_override={"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []},
        complete_required_native=False,
    )))["admission"]
    rec(
        "missing-required-package-work-indeterminate",
        ok=pr["verdict"] == "indeterminate" and bool(pp["executionDeficiencies"]) and not pp["findingIds"],
        verdict=pr["verdict"],
        joinCauses=[d.get("cause") for d in attached_adm.get("requiredCellDeficiencies") or []],
        joinDeficiencies=[d.get("deficiency") for d in attached_adm.get("requiredCellDeficiencies") or []],
        proofExecutionCauses=[d.get("cause") for d in pp["executionDeficiencies"]],
        proofNativeCauses=[d.get("nativeCause") for d in pp["executionDeficiencies"]],
    )

    # Wrong complete claim: already in check-execution-replay; re-probe reconstruct refuse.
    liar = F.build_file_inputs(
        atom_override={"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []},
        complete_required_native=False,
    )
    X.attach_host_capture(liar)
    man = copy.deepcopy(liar["executionInputs"])
    for row in man["cellOutcomes"]:
        row.update(state="complete", deficiency=None, nativeCause=None)
    raw_m = C.canonical(man)
    d_m = hashlib.sha256(raw_m).hexdigest()
    liar["blobs"][d_m] = raw_m
    liar["executionInputs"] = man
    liar["inputs"]["executionInputsDigest"] = d_m
    liar["inputs"]["evaluationInputRefs"] = E.cset(man["selectedRefs"] + [{"domain": "execution-inputs", "digest": d_m}])
    seed, objects, blobs, _ = F.seal_fixture(liar)
    Ident.open_run_closure(seed, objects, blobs)
    try:
        Ident.close_run(seed, objects, blobs)
        rec("lying-completion-close-run", ok=False, note="accepted")
    except Exception as exc:
        rec("lying-completion-close-run", ok="EXECUTION_INPUTS_OUTCOME_DERIVE" in str(exc) or "EVALUATOR_EXECUTION_INPUTS_JOIN" in str(exc),
            reason=str(exc)[:200])

    # Missing vs corrupt stored manifest via close_run.
    lost = copy.deepcopy(blobs if False else packed[2])
    run_ok, objects_ok, blobs_ok = packed
    lost_blobs = copy.deepcopy(blobs_ok)
    del lost_blobs[proof["executionInputsDigest"]]
    try:
        Ident.close_run(run_ok, objects_ok, lost_blobs)
        rec("promised-manifest-lost", ok=False)
    except Exception as exc:
        rec("promised-manifest-lost", ok=type(exc).__name__ == "EvidenceUnavailable",
            cls=type(exc).__name__, reason=str(exc)[:160])
    bad_blobs = copy.deepcopy(blobs_ok)
    bad_blobs[proof["executionInputsDigest"]] = b"{}"
    try:
        Ident.close_run(run_ok, objects_ok, bad_blobs)
        rec("manifest-corrupt-bytes", ok=False)
    except Exception as exc:
        rec("manifest-corrupt-bytes", ok=type(exc).__name__ != "EvidenceUnavailable" and "BLOB_DIGEST" in str(exc),
            cls=type(exc).__name__, reason=str(exc)[:160])

    # Inventory selected blob lost vs pointer vs corrupt through admit (promised store_pointers).
    kw = X.admission_kwargs(copy.deepcopy(F.build_file_inputs()))
    inv_d = next(r["digest"] for r in kw["execution_inputs"]["selectedRefs"] if r["domain"] == "subject-inventory")
    ptr = copy.deepcopy(kw)
    ptr["store_pointers"] = [p for p in ptr["store_pointers"] if p != inv_d]
    r_ptr = Mexec.admit_execution_inputs(**ptr)
    lost_kw = copy.deepcopy(kw)
    lost_kw["blobs"] = dict(lost_kw["blobs"])
    lost_kw["blobs"].pop(inv_d, None)
    r_lost = Mexec.admit_execution_inputs(**lost_kw)
    bad_kw = copy.deepcopy(kw)
    bad_kw["blobs"] = dict(bad_kw["blobs"])
    bad_kw["blobs"][inv_d] = b'{"kind":"not-the-inventory"}'
    r_bad = Mexec.admit_execution_inputs(**bad_kw)
    rec("selected-inventory-pointer-omission", ok="EXECUTION_INPUTS_REF_POINTER" in (r_ptr.get("refusals") or []),
        refusals=r_ptr.get("refusals"))
    rec("selected-inventory-lost-bytes", ok="EXECUTION_INPUTS_REF_LOST_BYTES" in (r_lost.get("refusals") or []),
        refusals=r_lost.get("refusals"))
    rec("selected-inventory-corrupt-bytes", ok="EXECUTION_INPUTS_REF_INVALID_BYTES" in (r_bad.get("refusals") or []),
        refusals=r_bad.get("refusals"))

    # promised_pointers one-pass: coverage envelope present, payload missing.
    gcov = F.build_file_inputs()
    X.attach_host_capture(gcov)
    man = gcov["executionInputs"]
    cov_hex = next(r["digest"] for r in man["selectedRefs"] if r["domain"] == "coverage")
    env = gcov["objects"]["coverage2:" + cov_hex][1]
    payload_d = env["payloadDigest"]
    promised_full = Mexec.promised_pointers(
        man, gcov["objects"][gcov["inputs"]["planId"]][1],
        gcov["objects"][gcov["inputs"]["executionPlanId"]][1],
        gcov["enumerationPlan"], objects=gcov["objects"], blobs=gcov["blobs"],
    )
    blobs_nopay = dict(gcov["blobs"])
    del blobs_nopay[payload_d]
    promised_nopay = Mexec.promised_pointers(
        man, gcov["objects"][gcov["inputs"]["planId"]][1],
        gcov["objects"][gcov["inputs"]["executionPlanId"]][1],
        gcov["enumerationPlan"], objects=gcov["objects"], blobs=blobs_nopay,
    )
    rec(
        "promised-pointers-payload-digest-survives-missing-payload-blob",
        ok=payload_d in promised_full["blobDigests"] and payload_d in promised_nopay["blobDigests"],
        payloadDigest=payload_d,
    )
    kw_pay = X.admission_kwargs(gcov)
    kw_pay["blobs"] = blobs_nopay
    kw_pay["store_pointers"] = promised_nopay["store_pointers"]
    r_pay = Mexec.admit_execution_inputs(**kw_pay)
    rec(
        "missing-coverage-payload-is-evidence-unavailable-not-pointer",
        ok="EXECUTION_INPUTS_EVIDENCE_UNAVAILABLE" in (r_pay.get("refusals") or [])
        and "EXECUTION_INPUTS_REF_POINTER" not in (r_pay.get("refusals") or []),
        refusals=r_pay.get("refusals"),
    )

    # Envelope missing: coverage H lost; payloadDigest may drop from promised (parent gone).
    objects_noenv = dict(gcov["objects"])
    del objects_noenv["coverage2:" + cov_hex]
    promised_noenv = Mexec.promised_pointers(
        man, gcov["objects"][gcov["inputs"]["planId"]][1],
        gcov["objects"][gcov["inputs"]["executionPlanId"]][1],
        gcov["enumerationPlan"], objects=objects_noenv, blobs=gcov["blobs"],
    )
    rec(
        "missing-coverage-envelope-does-not-promise-payload-digest",
        ok=("coverage2:" + cov_hex) in promised_noenv["objectKeys"] and payload_d not in promised_noenv["blobDigests"],
        note="parent locator remains from selectedRefs; child payload is discovered only from a present envelope",
    )
    kw_env = X.admission_kwargs(gcov)
    kw_env["objects"] = objects_noenv
    kw_env["store_pointers"] = promised_noenv["store_pointers"]
    r_env = Mexec.admit_execution_inputs(**kw_env)
    rec(
        "missing-coverage-envelope-is-lost-bytes",
        ok="EXECUTION_INPUTS_REF_LOST_BYTES" in (r_env.get("refusals") or []),
        refusals=r_env.get("refusals"),
    )

    # One-pass: coverage named only by a selected view, omitted from selectedRefs — payloadDigest not walked.
    man_omit = copy.deepcopy(man)
    man_omit["selectedRefs"] = [r for r in man_omit["selectedRefs"] if r.get("domain") != "coverage"]
    promised_omit = Mexec.promised_pointers(
        man_omit, gcov["objects"][gcov["inputs"]["planId"]][1],
        gcov["objects"][gcov["inputs"]["executionPlanId"]][1],
        gcov["enumerationPlan"], objects=gcov["objects"], blobs=gcov["blobs"],
    )
    rec(
        "one-pass-omitted-selected-coverage-drops-payloadDigest-from-promised",
        ok=payload_d not in promised_omit["blobDigests"] and ("coverage2:" + cov_hex) in promised_omit["objectKeys"],
        note="view walk adds coverage H key after list(obj); coverage object is not walked for payloadDigest. Admit still refuses SELECTED_COVER on well-typed manifests.",
    )

    # Candidate groups map omitted vs blob present/absent; unsupported authority.
    r_map, _, gd, ed = near_candidate_admit(groups_map=True)
    r_omit, promised_c, gd, ed = near_candidate_admit(groups_map=False)
    rec("candidate-groups-map-omitted-reads-blobs", ok=r_omit.get("result") == "ADMIT" and r_map.get("result") == "ADMIT",
        withMap=r_map.get("result"), withoutMap=r_omit.get("result"), groupInPromised=gd in promised_c["blobDigests"])
    r_lostg, promised_lostg, gd, ed = near_candidate_admit(groups_map=False, drop_group_blob=True)
    rec(
        "candidate-group-blob-missing-is-lost-bytes",
        ok="EXECUTION_INPUTS_REF_LOST_BYTES" in (r_lostg.get("refusals") or [])
        and gd in promised_lostg["blobDigests"],
        refusals=r_lostg.get("refusals"),
    )
    r_auth, _, _, _ = near_candidate_admit(groups_map=False, authority="native")
    rec(
        "candidate-group-non-candidate-authority-refused",
        ok="EXECUTION_INPUTS_CANDIDATE_GROUP" in (r_auth.get("refusals") or []),
        refusals=r_auth.get("refusals"),
    )

    # close_run does not equate proof.executionInputsDigest with evaluationInputRefs execution-inputs.
    gA = F.build_file_inputs(atom_override={"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []})
    packedA, resA, proofA, gA, _ = derive_graph(gA)
    gB = F.build_file_inputs(
        atom_override={"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []},
        complete_required_native=False,
    )
    packedB, resB, proofB, gB, _ = derive_graph(gB)
    runA, objA, blobA = packedA
    mixed = copy.deepcopy(blobA)
    mixed[proofB["executionInputsDigest"]] = blobA.get(proofB["executionInputsDigest"]) or gB["blobs"][proofB["executionInputsDigest"]]
    # remint proof with digest B, refs still A's selection+self
    sealA = objA[runA["evaluationSealId"]][1]
    proof_obj = copy.deepcopy(objA[sealA["proofBundleId"]][1])
    proof_obj["executionInputsDigest"] = proofB["executionInputsDigest"]
    try:
        pid = Ident.identifier("proof-bundle", proof_obj)
        objM = copy.deepcopy(objA)
        blobM = copy.deepcopy(mixed)
        blobM[proofB["executionInputsDigest"]] = gB["blobs"][proofB["executionInputsDigest"]]
        objM[pid] = ("proof-bundle", proof_obj)
        evid = copy.deepcopy(objM[runA["evidenceId"]][1])
        evid["proofBundleId"] = pid
        eid = Ident.identifier("semantic-evidence", evid)
        objM[eid] = ("semantic-evidence", evid)
        sealN = copy.deepcopy(sealA)
        sealN["proofBundleId"] = pid
        sealN["evidenceId"] = eid
        sid = Ident.identifier("evaluation-seal", sealN)
        objM[sid] = ("evaluation-seal", sealN)
        runM = copy.deepcopy(runA)
        runM["evidenceId"] = eid
        runM["evaluationSealId"] = sid
        try:
            Ident.close_run(runM, objM, blobM)
            close_ok = True
            close_reason = "ADMIT"
        except Exception as exc:
            close_ok = False
            close_reason = type(exc).__name__ + ":" + str(exc)[:180]
        try:
            R.replay(runM, objM, blobM)
            replay_ok = True
            replay_reason = "ADMIT"
        except Exception as exc:
            replay_ok = False
            replay_reason = type(exc).__name__ + ":" + str(exc)[:180]
        rec(
            "proof-digest-vs-evaluationInputRefs-execution-inputs-join",
            ok=True,
            closeRunAdmitsMismatchedDigest=close_ok,
            closeRunReason=close_reason,
            replayAdmitsMismatchedDigest=replay_ok,
            replayReason=replay_reason,
            digestA=proofA["executionInputsDigest"],
            digestB=proofB["executionInputsDigest"],
        )
    except Exception as exc:
        rec("proof-digest-vs-evaluationInputRefs-execution-inputs-join", ok=False,
            reason=type(exc).__name__ + ":" + str(exc)[:200])

    # Import totality: default fixture has no imports; reconstruct equality still holds.
    rec(
        "default-fixture-import-selection-empty-and-total",
        ok=not owner["plan"]["importIds"] and not [r for r in proof["evaluationInputRefs"] if r["domain"] == "import"],
        importIds=list(owner["plan"]["importIds"]),
    )

    passed = all(r.get("ok") is True for r in rows if "ok" in r)
    report = {
        "standing": "isolated integration probes of full execution replay; not a Run; not independent acceptance of the 52 unit controls",
        "python": PY_NOTE,
        "passed": passed,
        "count": len(rows),
        "probes": rows,
    }
    text = json.dumps(report, indent=2) + "\n"
    out = Path("/tmp/opensip-design-corrections/grok-execution-inputs.v7/probe-receipt.json")
    out.write_text(text)
    print(text, end="")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
