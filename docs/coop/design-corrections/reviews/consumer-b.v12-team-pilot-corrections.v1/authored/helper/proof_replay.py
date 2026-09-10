"""Fresh-process complete proof reconstruction from an exported store.

Admits selected inputs, derives subjects/predicates/witnesses/findings/
ruleResults/verdict, constructs the complete expected proof, and compares
C with the retained claim. Claimed outputs are read only as locators and
for that final comparison.
"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

from helper.annotated_admit import admit_full_pilot
from helper.body_identity import parse_body_identity_frame
from helper.canonical import C
from helper.closure_admit import (
    admit_body_identity_frame,
    admit_declares_payload,
    admit_enumeration_inventories,
    admit_syntax_native_context,
    admit_unit_membership,
    parse_canonical,
    parse_native_h,
    parse_typed_h,
    rehash,
)
from helper.errors import AdmissionError
from helper.compose_proof import compose_expected_proof, digest_of, select_file_subjects, sort_set
from helper.identity import H, parse_h_frame, typed_id
from helper.store import Store
from pathlib import Path


def _hex(typed: str) -> str:
    return typed.split(":", 1)[1]


def load_graph(store: Store) -> dict[str, Any]:
    run_ids = [k for k in store.object_table if str(k).startswith("run3:")]
    if not run_ids:
        raise RuntimeError("NO_RUN")
    run_id = sorted(run_ids)[0]
    run = parse_typed_h(store, run_id, "run")
    recomputed = typed_id("run", run)
    if recomputed != run_id:
        raise RuntimeError(f"RUN_H_MISMATCH {recomputed} {run_id}")
    seal = parse_typed_h(store, run["evaluationSealId"], "evaluation-seal")
    claimed_proof_id = seal["proofBundleId"]
    claimed_proof = parse_typed_h(store, claimed_proof_id, "proof-bundle")
    # executionInputsDigest is the committed input locator, not a truth oracle
    ei = parse_canonical(store, claimed_proof["executionInputsDigest"])
    plan = parse_typed_h(store, run["planId"], "plan")
    snapshot = parse_typed_h(store, run["snapshotId"], "snapshot")
    policy = parse_canonical(store, plan["policyDigest"])
    # RuleProgramV2 is the published projection of the Plan policy, not a free claimed artifact.
    rp = {
        "schemaVersion": 2,
        "policyDigest": plan["policyDigest"],
        "rules": [
            {
                "ruleId": r["ruleId"],
                "ruleProgramRef": r["ruleProgramRef"],
                "emitWhen": r["emitWhen"],
            }
            for r in sorted(policy["rules"], key=lambda x: x["ruleId"].encode())
        ],
    }
    rp_d = hashlib.sha256(C(rp)).hexdigest()
    retained_rp = parse_canonical(store, rp_d)
    enum_plan = parse_canonical(store, ei["enumerationPlanDigest"])
    view_refs = [r for r in ei["selectedRefs"] if r["domain"] == "view"]
    if len(view_refs) != 1:
        raise RuntimeError(f"expected one selected view, got {len(view_refs)}")
    view_digest = view_refs[0]["digest"]
    view_typed = f"view2:{view_digest}"
    view = parse_typed_h(store, view_typed, "view")

    facts = []
    payloads = {}
    for fid in view["facts"]:
        frec = parse_typed_h(store, fid, "fact")
        pl = parse_canonical(store, frec["payloadDigest"])
        facts.append({"id": fid, "record": frec})
        payloads[fid] = pl

    coverages = []
    scopes = {}
    file_scope_id = None
    for cid in view["coverageIds"]:
        crec = parse_typed_h(store, cid, "coverage")
        payload = parse_canonical(store, crec["payloadDigest"])
        coverages.append(
            {
                "id": cid,
                "record": {
                    "relation": payload["key"]["relation"],
                    "resolution": payload["key"]["resolution"],
                },
                "entry": payload["entry"],
                "payload": payload,
                "h": crec,
            }
        )
        sid = crec["scopeId"]
        scopes[sid] = parse_typed_h(store, sid, "subject-scope")
        if payload["key"]["relation"] == "file":
            file_scope_id = sid
    if file_scope_id is None:
        raise RuntimeError("no file subject-scope")

    inv_digests = []
    for outcome in ei["cellOutcomes"]:
        inv_digests.extend(outcome["inventoryDigests"])
    for r in ei["selectedRefs"]:
        if r["domain"] == "subject-inventory":
            inv_digests.append(r["digest"])
    inventories = []
    seen_inv = set()
    for d in inv_digests:
        if d in seen_inv:
            continue
        seen_inv.add(d)
        inventories.append(parse_canonical(store, d))

    ctx_hex = plan["nativeContextDigests"][0]
    ctx = parse_native_h(store, ctx_hex, "native.context.syntax.v2")
    uni_hex = None
    for f in facts:
        uni_hex = f["record"]["sourceUniverse"]
        break
    if uni_hex is None:
        raise RuntimeError("no fact universe")
    uni = parse_native_h(store, uni_hex, "native.semantic-universe.syntax.v2")

    exec_plan = parse_typed_h(store, ei["executionPlanId"], "execution-plan")
    stage_spec = parse_canonical(store, exec_plan["stages"][0]["stageSpecDigest"])
    analysis_spec = parse_canonical(store, plan["analysisSpecDigest"])
    emission_plan = None
    for p in analysis_spec["parameters"]:
        rec = parse_canonical(store, p["payloadDigest"])
        if rec.get("schemaVersion") == 1 and "rules" in rec and rec["rules"] and "detectorClosure" in rec["rules"][0]:
            emission_plan = rec
    if emission_plan is None:
        raise RuntimeError("no evaluator-emission-plan in analysis-spec parameters")
    evidence = parse_typed_h(store, run["evidenceId"], "semantic-evidence")
    vcs = parse_canonical(store, snapshot["vcsDigest"])

    closures: dict[str, dict] = {}
    for cid in plan["semanticClosures"]:
        closures[cid] = parse_typed_h(store, cid, "closure")
    grammar_cid = ctx["grammarBundle"]["closureId"]
    if grammar_cid not in closures:
        closures[grammar_cid] = parse_typed_h(store, grammar_cid, "closure")
    det_cid = emission_plan["rules"][0]["detectorClosure"]
    if det_cid not in closures:
        closures[det_cid] = parse_typed_h(store, det_cid, "closure")
    eval_cid = ei["evaluatorClosure"]
    if eval_cid not in closures:
        closures[eval_cid] = parse_typed_h(store, eval_cid, "closure")

    coverages_h = [parse_typed_h(store, cid, "coverage") for cid in view["coverageIds"]]
    view_coverages_full = []
    for cid in view["coverageIds"]:
        crec = parse_typed_h(store, cid, "coverage")
        payload = parse_canonical(store, crec["payloadDigest"])
        view_coverages_full.append(
            {
                "id": cid,
                "digest": cid.split(":", 1)[1],
                "record": crec,
                "payload": payload,
                "entry": payload["entry"],
            }
        )
    scopes_list = [parse_typed_h(store, sid, "subject-scope") for sid in view["scopeIds"]]

    return {
        "run_id": run_id,
        "run": run,
        "seal": seal,
        "claimed_proof_id": claimed_proof_id,
        "claimed_proof": claimed_proof,
        "execution_inputs": ei,
        "execution_inputs_digest": claimed_proof["executionInputsDigest"],
        "plan": plan,
        "plan_id": run["planId"],
        "snapshot": snapshot,
        "policy": policy,
        "policy_digest": plan["policyDigest"],
        "rule_program": retained_rp,
        "rule_program_digest": rp_d,
        "enum_plan": enum_plan,
        "view": view,
        "view_digest": view_digest,
        "facts": facts,
        "payloads": payloads,
        "coverages": coverages,
        "file_scope_id": file_scope_id,
        "inventories": inventories,
        "ctx": ctx,
        "ctx_hex": ctx_hex,
        "uni": uni,
        "uni_hex": uni_hex,
        "evaluator_closure": ei["evaluatorClosure"],
        "execution_plan_id": ei["executionPlanId"],
        "execution_plan": exec_plan,
        "stage_spec": stage_spec,
        "analysis_spec": analysis_spec,
        "emission_plan": emission_plan,
        "evidence": evidence,
        "vcs": vcs,
        "closures": closures,
        "coverages_h": coverages_h,
        "views_full": [view],
        "view_coverages_full": view_coverages_full,
        "scopes": scopes_list,
    }


def admit_graph(store: Store, g: dict) -> dict:
    joins = []

    def join(name: str, pred: bool, detail: str = "") -> None:
        joins.append({"name": name, "ok": bool(pred), "detail": detail})

    try:
        syn = admit_syntax_native_context(store, g["ctx"])
        join("grammar-artifacts-in-closure-tree", True, json.dumps(syn["tree"]))
    except AdmissionError as e:
        join("grammar-artifacts-in-closure-tree", False, f"{e.code}: {e}")
    join(
        "selected-grammar-subset",
        set(g["uni"]["selectedGrammarIds"]) <= {x["grammarId"] for x in g["ctx"]["grammarBundle"]["grammars"]},
        str(g["uni"]["selectedGrammarIds"]),
    )
    join("universe-binds-context", g["uni"]["nativeContextId"] == "sha256:" + g["ctx_hex"])
    join("resolution-attempted-false", g["uni"]["resolutionAttempted"] is False)

    try:
        memb = admit_unit_membership(store, g["enum_plan"]["membershipDigest"])
        join(
            "syntax-only-membership-unitOrdinal-null",
            memb["units"] == [] and all(r["unitOrdinal"] is None for r in memb["rows"]),
            json.dumps({"units": memb["units"], "rows": memb["rows"]}),
        )
    except AdmissionError as e:
        join("syntax-only-membership-unitOrdinal-null", False, f"{e.code}: {e}")
        memb = None

    try:
        enum_adm = admit_enumeration_inventories(store, g["enum_plan"], g["inventories"])
        join("enumeration-exactly-one-inventory-per-cell-program-kind", True, str(enum_adm["expected"]))
    except AdmissionError as e:
        join("enumeration-exactly-one-inventory-per-cell-program-kind", False, f"{e.code}: {e}")

    for outcome in g["execution_inputs"]["cellOutcomes"]:
        kinds = list(outcome["kinds"])
        digs = list(outcome["inventoryDigests"])
        invs = [parse_canonical(store, d) for d in digs]
        got_kinds = sorted(i["kind"] for i in invs)
        join(
            f"cellOutcome[{outcome['ordinal']}]-inventoryDigests-exactly-one-per-kind",
            got_kinds == sorted(kinds) and len(digs) == len(kinds),
            f"kinds={kinds} inventoryKinds={got_kinds}",
        )

    for f in g["facts"]:
        rec = f["record"]
        pl = g["payloads"][f["id"]]
        if rec["relation"] == "file":
            join("file-zero-anchors", rec["anchors"] == [])
            row = next(r for r in g["snapshot"]["sourceInventory"] if r["path"] == pl["path"])
            join("file-digest-matches-inventory", pl["contentSha256"] == row["sha256"])
            join("file-length-matches-inventory", pl["byteLength"] == row["bytes"])
            blob = rehash(store, pl["contentSha256"])
            join("file-blob-retained", len(blob) == pl["byteLength"])
        elif rec["relation"] == "declares":
            try:
                admit_declares_payload(store, rec["payloadDigest"])
                join("declares-payload-SubjectIdV1", True, json.dumps(pl))
            except AdmissionError as e:
                join("declares-payload-SubjectIdV1", False, f"{e.code}: {e}")
        elif rec["relation"] == "clones":
            try:
                span = None
                if rec["anchors"]:
                    a = rec["anchors"][0]
                    span = rehash(store, a["blobDigest"])[a["startByte"] : a["endByte"]]
                parsed = admit_body_identity_frame(
                    store,
                    pl["bodyIdentity"],
                    expected_span=span if pl["normalisationLevel"] == "L0-verbatim" else None,
                )
                join(
                    f"clones-bodyIdentity-frame-retained-{pl['normalisationLevel']}",
                    True,
                    parsed["levelId"],
                )
                if pl["normalisationLevel"] != "L0-verbatim":
                    join("clones-non-L0-requires-retained-frame", True, parsed["levelId"])
            except AdmissionError as e:
                join(
                    f"clones-bodyIdentity-frame-retained-{pl['normalisationLevel']}",
                    False,
                    f"{e.code}: {e}",
                )

    try:
        full = admit_full_pilot(store, g)
        for j in full["joins"]:
            joins.append(j)
        join("annotated-owner-admission", full["ok"], f"digestHits={full['digestHits']}")
    except AdmissionError as e:
        join("annotated-owner-admission", False, f"{e.code}: {e}")

    return {"joins": joins, "ok": all(j["ok"] for j in joins)}


class AdmissionErrorWrap(RuntimeError):
    pass


def reconstruct_expected_proof(store: Store, g: dict) -> dict:
    file_invs = [inv for inv in g["inventories"] if inv["kind"] == "file"]
    subjects = select_file_subjects(inventories=file_invs, universe=g["uni_hex"], store=None)
    # Subjects must already be retained; identities must match typed_id of derived records
    for s in subjects:
        rec = store.object_table.get(s["id"])
        if rec is None:
            raise RuntimeError(f"derived subject not retained: {s['id']}")
        frame = rehash(store, rec["digest"])
        parsed = parse_h_frame(frame, allowed_domains={"evaluation-subject"})
        if parsed["value"] != s["record"]:
            raise RuntimeError("subject record mismatch")
    proof = compose_expected_proof(
        plan_id=g["plan_id"],
        execution_plan_id=g["execution_plan_id"],
        evaluator_closure=g["evaluator_closure"],
        policy=g["policy"],
        policy_digest=g["policy_digest"],
        rule_program=g["rule_program"],
        rule_program_digest=g["rule_program_digest"],
        execution_inputs=g["execution_inputs"],
        execution_inputs_digest=g["execution_inputs_digest"],
        subjects=subjects,
        facts=g["facts"],
        payloads=g["payloads"],
        coverages=g["coverages"],
        view_digest=g["view_digest"],
        file_scope_id=g["file_scope_id"],
        file_inventories=file_invs,
        store=None,
    )
    return {"proof": proof, "subjects": subjects}


def logical_result_tamper(claimed: dict) -> dict:
    """Change claimed logical result while preserving selected-input citations.

    Witness digests, evaluationInputRefs, findingIds, and executionInputsDigest
    stay. Verdict, atom value, and gating rule outcome flip. This is the claimed
    proof body only; enclosing evidence/seal/Run identities are reminted by
    export_logical_result_tamper_graph.
    """
    t = copy.deepcopy(claimed)
    t["verdict"] = "fail" if claimed.get("verdict") == "pass" else "pass"
    if t.get("predicateProofs"):
        t["predicateProofs"] = copy.deepcopy(claimed["predicateProofs"])
        for p in t["predicateProofs"]:
            if p.get("value") == "false":
                p["value"] = "true"
                break
    for rr in t.get("ruleResults") or []:
        if rr.get("outcome") == "pass":
            rr["outcome"] = "fail"
    return t


def stale_hash_tamper(claimed: dict) -> dict:
    """Stale-hash control: mutate a digest field only. Do not remint enclosing identities."""
    t = copy.deepcopy(claimed)
    ed = t["executionInputsDigest"]
    t["executionInputsDigest"] = ed[:-1] + ("0" if ed[-1] != "0" else "1")
    return t


def _drop_enclosing_ids(g: dict) -> set[str]:
    return {
        _hex(g["claimed_proof_id"]),
        _hex(g["run"]["evidenceId"]),
        _hex(g["run"]["evaluationSealId"]),
        _hex(g["run_id"]),
    }


def copy_store_without_enclosing(store: Store, drop: set[str]) -> Store:
    """Copy retained selected-input bytes; omit proof/evidence/seal/run frames."""
    new = Store()
    for digest, raw in store.blobs.items():
        if digest in drop:
            continue
        new.blobs[digest] = raw
    for key, meta in store.object_table.items():
        digest = meta.get("digest")
        if digest in drop:
            continue
        if isinstance(key, str) and ":" in key and key.split(":", 1)[1] in drop:
            continue
        if key in drop:
            continue
        new.object_table[key] = copy.deepcopy(meta)
    return new


def export_logical_result_tamper_graph(store: Store, g: dict, out_path: Path) -> dict:
    """Build a structurally valid replacement graph with a false logical result.

    Selected inputs (plan, snapshot, views, coverage, inventories, execution-inputs)
    are byte-identical. Proof/evidence/seal/Run identities and exact H frames are
    rebuilt. Semantic replay against fresh derivation from those inputs must refuse.
    """
    tampered_proof = logical_result_tamper(g["claimed_proof"])
    if tampered_proof["evaluationInputRefs"] != g["claimed_proof"]["evaluationInputRefs"]:
        raise RuntimeError("tamper must preserve evaluationInputRefs citations")
    if [p["witnessDigest"] for p in tampered_proof["predicateProofs"]] != [
        p["witnessDigest"] for p in g["claimed_proof"]["predicateProofs"]
    ]:
        raise RuntimeError("tamper must preserve witness citations")
    drop = _drop_enclosing_ids(g)
    new = copy_store_without_enclosing(store, drop)
    proof_h = new.put_h("proof-bundle", tampered_proof, label="proof-logical-tamper")
    evidence = copy.deepcopy(g["evidence"])
    evidence["proofBundleId"] = proof_h["typedId"]
    ev_h = new.put_h("semantic-evidence", evidence, label="evidence-logical-tamper")
    seal = copy.deepcopy(g["seal"])
    seal["proofBundleId"] = proof_h["typedId"]
    seal["evidenceId"] = ev_h["typedId"]
    seal["verdict"] = tampered_proof["verdict"]
    seal_h = new.put_h("evaluation-seal", seal, label="seal-logical-tamper")
    run = copy.deepcopy(g["run"])
    run["evidenceId"] = ev_h["typedId"]
    run["evaluationSealId"] = seal_h["typedId"]
    run_h = new.put_h("run", run, label="run-logical-tamper")
    new.export(out_path)
    return {
        "path": str(out_path),
        "runId": run_h["typedId"],
        "proofId": proof_h["typedId"],
        "evidenceId": ev_h["typedId"],
        "sealId": seal_h["typedId"],
        "planId": g["plan_id"],
        "snapshotId": g["run"]["snapshotId"],
        "executionInputsDigest": g["execution_inputs_digest"],
        "verdict": tampered_proof["verdict"],
        "atomValue": tampered_proof["predicateProofs"][0]["value"] if tampered_proof["predicateProofs"] else None,
        "citationsPreserved": True,
        "replacementGraph": True,
        "blobCount": len(new.blobs),
        "sha256": hashlib.sha256(out_path.read_bytes()).hexdigest(),
        "bytes": out_path.stat().st_size,
    }
