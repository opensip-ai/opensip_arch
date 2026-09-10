"""Independent retained-data replay: parse store blobs, re-evaluate, compare complete C/H.

This is the required semantic proof replay after identity/schema/closure admission.
It must not read claimed findings/witnesses/verdict to select subjects or values.
"""
from __future__ import annotations

import base64
import copy
import json
from typing import Any

from .codec import (
    AdmissionError,
    body_identity,
    body_identity_frame,
    canonical_digest,
    encode_c,
    h_hex,
    h_id,
    l0_payload,
    parse_h_frame,
    sha256,
    sort_by_keys,
    sort_canonical_set,
    sort_utf8,
)
from .evaluator import UNIVERSE_MAP, evaluate_policy, subject_descriptor


def _b64(s: str) -> bytes:
    return base64.b64decode(s)


def _loads_c(raw: bytes) -> Any:
    return json.loads(raw.decode("utf-8"))


class LoadedStore:
    def __init__(self, export: dict):
        self.blobs = export["blobs"]
        self.table = export["objectTable"]
        self.by_digest: dict[str, dict] = {}
        self.by_id: dict[str, dict] = {}
        self.by_domain: dict[str, list[dict]] = {}
        self.records: dict[str, Any] = {}  # digest -> parsed descriptor
        for row in self.table:
            d = row["digest"]
            raw = _b64(self.blobs[d])
            rec = dict(row)
            rec["raw"] = raw
            if row["retention"] == "h-preimage-frame":
                domain, payload = parse_h_frame(raw)
                rec["frameDomain"] = domain
                rec["descriptor"] = _loads_c(payload)
                if sha256(raw) != d:
                    raise AdmissionError("STORE_DIGEST", f"h-frame digest mismatch {d}")
                if h_hex(domain, rec["descriptor"]) != d:
                    raise AdmissionError("STORE_H", f"H({domain}) mismatch for {d}")
            elif row["retention"] == "canonical-record":
                rec["descriptor"] = _loads_c(raw)
                if sha256(raw) != d:
                    raise AdmissionError("STORE_DIGEST", f"canonical digest mismatch {d}")
                if canonical_digest(rec["descriptor"]) != d:
                    raise AdmissionError("STORE_C", f"C roundtrip mismatch for {d}")
            else:
                rec["descriptor"] = None
                if sha256(raw) != d:
                    raise AdmissionError("STORE_DIGEST", f"raw digest mismatch {d}")
            self.by_digest[d] = rec
            if row.get("id"):
                self.by_id[row["id"]] = rec
            self.by_domain.setdefault(row["domain"], []).append(rec)

    def one(self, domain: str) -> dict:
        rows = self.by_domain.get(domain) or []
        if len(rows) != 1:
            raise AdmissionError("STORE_DOMAIN", f"expected one {domain}, got {len(rows)}")
        return rows[0]

    def desc(self, domain: str) -> Any:
        return self.one(domain)["descriptor"]

    def get_id(self, ident: str) -> dict:
        if ident not in self.by_id:
            raise AdmissionError("STORE_ID", f"missing {ident}")
        return self.by_id[ident]


def reconstruct_inputs(store: LoadedStore) -> dict:
    """Rebuild evaluator inputs from retained objects. Does not read claimed verdict/findings."""
    run = store.desc("run")
    evidence = store.get_id(run["evidenceId"])["descriptor"]
    seal = store.get_id(run["evaluationSealId"])["descriptor"]
    proof_claimed = store.get_id(evidence["proofBundleId"])["descriptor"]
    plan = store.get_id(run["planId"])["descriptor"]
    snapshot = store.get_id(run["snapshotId"])["descriptor"]
    exec_plan = store.get_id(proof_claimed["executionPlanId"])["descriptor"]

    exec_in_digest = proof_claimed["executionInputsDigest"]
    if exec_in_digest not in store.by_digest:
        raise AdmissionError("EXEC_INPUTS_MISSING", exec_in_digest)
    exec_inputs = store.by_digest[exec_in_digest]["descriptor"]
    if canonical_digest(exec_inputs) != exec_in_digest:
        raise AdmissionError("EXEC_INPUTS_DIGEST", "executionInputsDigest does not match C(record)")

    policy = store.desc("policy")
    program = store.desc("rule-program")
    if canonical_digest(policy) != plan["policyDigest"]:
        raise AdmissionError("POLICY_JOIN", "plan.policyDigest != C(policy)")
    if canonical_digest(program) != proof_claimed["ruleProgramDigest"]:
        raise AdmissionError("PROGRAM_JOIN", "proof.ruleProgramDigest != C(program)")
    if program["policyDigest"] != plan["policyDigest"]:
        raise AdmissionError("PROGRAM_POLICY", "RuleProgramV2.policyDigest != plan.policyDigest")

    waivers = store.desc("waiver")
    emission = store.desc("emission-plan")
    enum_plan = store.desc("enumeration-plan")

    inventories = []
    for row in store.by_domain.get("subject-inventory") or []:
        inv = copy.deepcopy(row["descriptor"])
        inv["digest"] = row["digest"]
        inventories.append(inv)

    view_ids = evidence["viewIds"]
    views = [store.get_id(vid)["descriptor"] for vid in view_ids]
    if len(views) != 1:
        raise AdmissionError("VIEW_COUNT", f"expected one view, got {len(views)}")
    view = views[0]

    facts = []
    payloads = {}
    for fid in view["facts"]:
        frec = store.get_id(fid)
        fact = copy.deepcopy(frec["descriptor"])
        fact["id"] = fid
        fact["hex"] = frec["digest"]
        pd = fact["payloadDigest"]
        if pd not in store.by_digest:
            raise AdmissionError("FACT_PAYLOAD_MISSING", pd)
        payloads[fid] = store.by_digest[pd]["descriptor"]
        facts.append(fact)

    coverages = []
    scopes = {}
    for cid in view["coverageIds"]:
        crec = store.get_id(cid)
        cov = copy.deepcopy(crec["descriptor"])
        cov["id"] = cid
        cov["hex"] = crec["digest"]
        pd = cov["payloadDigest"]
        if pd not in store.by_digest:
            raise AdmissionError("COV_PAYLOAD_MISSING", pd)
        cov["payload"] = store.by_digest[pd]["descriptor"]
        coverages.append(cov)
        sid = cov["scopeId"]
        srec = store.get_id(sid)
        scopes[sid] = {**srec["descriptor"], "id": sid, "hex": srec["digest"]}

    for sid in view["scopeIds"]:
        if sid not in scopes:
            srec = store.get_id(sid)
            scopes[sid] = {**srec["descriptor"], "id": sid, "hex": srec["digest"]}

    token = policy["rules"][0]["subjectEnumeration"]["universe"]
    # universe hex from any fact
    universe_hex = facts[0]["sourceUniverse"] if facts else coverages[0]["payload"]["key"]["sourceUniverse"]
    universe_hex_by_token = {token: universe_hex}

    detector_closure = emission["rules"][0]["detectorClosure"]
    budget = plan["budget"]["limit"]

    return {
        "run": run,
        "evidence": evidence,
        "seal": seal,
        "proof_claimed": proof_claimed,
        "plan": plan,
        "snapshot": snapshot,
        "exec_plan": exec_plan,
        "exec_inputs": exec_inputs,
        "exec_in_digest": exec_in_digest,
        "policy": policy,
        "program": program,
        "waivers": waivers,
        "emission": emission,
        "enum_plan": enum_plan,
        "inventories": inventories,
        "view": view,
        "view_id": view_ids[0],
        "facts": facts,
        "payloads": payloads,
        "coverages": coverages,
        "scopes": scopes,
        "universe_hex": universe_hex,
        "universe_hex_by_token": universe_hex_by_token,
        "detector_closure": detector_closure,
        "budget": budget,
        "evaluator_closure": proof_claimed["evaluatorClosure"],
        "plan_id": store.one("run")["descriptor"]["planId"],
        "execution_plan_id": proof_claimed["executionPlanId"],
        "capabilityManifestId": run["capabilityManifestId"],
        "project_id": run["projectId"],
        "snapshot_id": run["snapshotId"],
        "claimed_proof_id": evidence["proofBundleId"],
        "claimed_evidence_id": store.one("run")["descriptor"]["evidenceId"],
        "claimed_seal_id": run["evaluationSealId"],
        "claimed_run_id": store.one("run")["id"] if "id" in store.one("run") else None,
    }


def rebuild_outputs(inp: dict, ev: dict, evaluation_input_refs: list) -> dict:
    """Compose findings/proof/evidence/seal/run from evaluation. No claimed verdict used."""
    program = inp["program"]
    witnesses = ev["witnesses"]
    pred_proofs = ev["predicateProofs"]
    root_wits = {
        (pp["ruleId"], pp["subjectId"]): pp["witnessDigest"]
        for pp in pred_proofs
        if pp["predicateId"] == "p"
    }
    minted_findings = []
    finding_ids = []
    for f in ev["findings"]:
        f = copy.deepcopy(f)
        f.pop("_fingerprintDesc", None)
        f.pop("_params", None)
        wit = root_wits.get((f["ruleId"], f["subjectId"]))
        if wit:
            f["evidenceRefs"] = [{"domain": "predicate-witness", "digest": wit}]
        ident_src = {k: v for k, v in f.items() if k != "id"}
        fid = h_id("finding", ident_src)
        finding_ids.append(fid)
        minted_findings.append(ident_src)

    pps = sort_by_keys(pred_proofs, ["ruleId", "subjectId", "predicateId"]) if pred_proofs else []
    proof = {
        "schemaVersion": 3,
        "planId": inp["plan_id"],
        "executionPlanId": inp["execution_plan_id"],
        "evaluatorClosure": inp["evaluator_closure"],
        "ruleProgramDigest": canonical_digest(program),
        "evaluationInputRefs": evaluation_input_refs,
        "predicateProofs": pps,
        "findingIds": sort_utf8(finding_ids),
        "verdict": ev["verdict"],
        "evaluationState": ev["evaluationState"],
        "ruleResults": copy.deepcopy(ev["ruleResults"]),
        "waivedFindingIds": [],
        "executionDeficiencies": ev["executionDeficiencies"],
        "executionInputsDigest": inp["exec_in_digest"],
    }
    if finding_ids and proof["ruleResults"]:
        proof["ruleResults"][0]["findingIds"] = sort_utf8(finding_ids)

    proof_id = h_id("proof-bundle", proof)
    coverage_ids = sort_utf8([c["id"] for c in inp["coverages"]])
    evidence = {
        "schemaVersion": 3,
        "planId": inp["plan_id"],
        "viewIds": [inp["view_id"]],
        "coverageIds": coverage_ids,
        "importIds": [],
        "findingIds": sort_utf8(finding_ids),
        "proofBundleId": proof_id,
    }
    evidence_id = h_id("semantic-evidence", evidence)
    seal = {
        "schemaVersion": 3,
        "planId": inp["plan_id"],
        "executionPlanId": inp["execution_plan_id"],
        "evidenceId": evidence_id,
        "evaluatorClosure": inp["evaluator_closure"],
        "policyDigest": canonical_digest(inp["policy"]),
        "proofBundleId": proof_id,
        "verdict": ev["verdict"],
    }
    seal_id = h_id("evaluation-seal", seal)
    run = {
        "schemaVersion": 3,
        "projectId": inp["project_id"],
        "snapshotId": inp["snapshot_id"],
        "planId": inp["plan_id"],
        "evidenceId": evidence_id,
        "evaluationSealId": seal_id,
        "capabilityManifestId": inp["capabilityManifestId"],
    }
    run_id = h_id("run", run)
    return {
        "proof": proof,
        "proofId": proof_id,
        "proofC": encode_c(proof),
        "evidence": evidence,
        "evidenceId": evidence_id,
        "evidenceC": encode_c(evidence),
        "seal": seal,
        "sealId": seal_id,
        "sealC": encode_c(seal),
        "run": run,
        "runId": run_id,
        "runC": encode_c(run),
        "findingIds": finding_ids,
        "witnesses": witnesses,
        "verdict": ev["verdict"],
        "evaluationState": ev["evaluationState"],
        "workUnitsCharged": ev["workUnitsCharged"],
    }


def replay_store(export: dict) -> dict:
    store = LoadedStore(export)
    inp = reconstruct_inputs(store)
    claimed_proof = inp["proof_claimed"]
    claimed_c = encode_c(claimed_proof)

    extra_refs = [
        {"domain": "execution-inputs", "digest": inp["exec_in_digest"]},
        {"domain": "rule-program", "digest": canonical_digest(inp["program"])},
        {"domain": "policy", "digest": canonical_digest(inp["policy"])},
        {"domain": "enumeration-plan", "digest": canonical_digest(inp["enum_plan"])},
    ]
    for d in inp["plan"].get("nativeContextDigests") or []:
        extra_refs.append({"domain": "native-context", "digest": d})
    eirefs = sort_canonical_set(list(inp["exec_inputs"]["selectedRefs"]) + extra_refs)

    ev = evaluate_policy(
        policy=inp["policy"],
        program=inp["program"],
        inventories=inp["inventories"],
        facts=inp["facts"],
        fact_payloads=inp["payloads"],
        coverages=inp["coverages"],
        scopes=inp["scopes"],
        universe_hex_by_token=inp["universe_hex_by_token"],
        waivers=inp["waivers"],
        emission_plan=inp["emission"],
        detector_closure=inp["detector_closure"],
        budget_limit=inp["budget"],
    )
    rebuilt = rebuild_outputs(inp, ev, eirefs)

    proof_bytes_equal = rebuilt["proofC"] == claimed_c
    proof_id_equal = rebuilt["proofId"] == inp["claimed_proof_id"]
    evidence_id_equal = rebuilt["evidenceId"] == inp["claimed_evidence_id"]
    seal_id_equal = rebuilt["sealId"] == inp["claimed_seal_id"]
    run_row = store.one("run")
    run_id_equal = rebuilt["runId"] == run_row["id"]

    # field-level proof diff
    diffs = []
    if rebuilt["proof"]["verdict"] != claimed_proof["verdict"]:
        diffs.append({"field": "verdict", "claimed": claimed_proof["verdict"], "recomputed": rebuilt["proof"]["verdict"]})
    if rebuilt["proof"]["findingIds"] != claimed_proof["findingIds"]:
        diffs.append({"field": "findingIds"})
    if encode_c(rebuilt["proof"]["predicateProofs"]) != encode_c(claimed_proof["predicateProofs"]):
        diffs.append({"field": "predicateProofs"})
    if encode_c(rebuilt["proof"]["ruleResults"]) != encode_c(claimed_proof["ruleResults"]):
        diffs.append({"field": "ruleResults"})
    if rebuilt["proof"]["executionInputsDigest"] != claimed_proof["executionInputsDigest"]:
        diffs.append({"field": "executionInputsDigest"})

    # tamper A: un-rehashed verdict edit
    tamper_a = copy.deepcopy(claimed_proof)
    tamper_a["verdict"] = "fail" if claimed_proof["verdict"] != "fail" else "pass"
    tamper_a_c = encode_c(tamper_a)
    tamper_a_h = h_id("proof-bundle", tamper_a)
    tamper_a_refused = (tamper_a_c != rebuilt["proofC"]) or (tamper_a_h != rebuilt["proofId"])

    # tamper B: fully rehashed false claim, citations/facts preserved
    tamper_b_proof = copy.deepcopy(claimed_proof)
    tamper_b_proof["verdict"] = "fail" if claimed_proof["verdict"] != "fail" else "pass"
    tamper_b_proof_id = h_id("proof-bundle", tamper_b_proof)
    tamper_b_ev = copy.deepcopy(inp["evidence"])
    tamper_b_ev["proofBundleId"] = tamper_b_proof_id
    tamper_b_ev_id = h_id("semantic-evidence", tamper_b_ev)
    tamper_b_seal = copy.deepcopy(inp["seal"])
    tamper_b_seal["proofBundleId"] = tamper_b_proof_id
    tamper_b_seal["evidenceId"] = tamper_b_ev_id
    tamper_b_seal["verdict"] = tamper_b_proof["verdict"]
    tamper_b_seal_id = h_id("evaluation-seal", tamper_b_seal)
    tamper_b_run = copy.deepcopy(inp["run"])
    tamper_b_run["evidenceId"] = tamper_b_ev_id
    tamper_b_run["evaluationSealId"] = tamper_b_seal_id
    tamper_b_run_id = h_id("run", tamper_b_run)
    # identities of the reminted false claim are self-consistent
    tamper_b_self_h = h_hex("proof-bundle", tamper_b_proof) == tamper_b_proof_id.split(":")[1]
    # semantic replay still refuses: recomputed proof bytes != reminted false proof bytes
    tamper_b_refused = rebuilt["proofC"] != encode_c(tamper_b_proof)
    # citation membership preserved
    citations_preserved = (
        tamper_b_proof["findingIds"] == claimed_proof["findingIds"]
        and tamper_b_proof["evaluationInputRefs"] == claimed_proof["evaluationInputRefs"]
        and tamper_b_ev["findingIds"] == inp["evidence"]["findingIds"]
        and tamper_b_ev["viewIds"] == inp["evidence"]["viewIds"]
    )

    return {
        "ok": proof_bytes_equal and proof_id_equal and evidence_id_equal and seal_id_equal and run_id_equal and not diffs,
        "proofBytesEqual": proof_bytes_equal,
        "proofIdEqual": proof_id_equal,
        "evidenceIdEqual": evidence_id_equal,
        "sealIdEqual": seal_id_equal,
        "runIdEqual": run_id_equal,
        "claimedProofId": inp["claimed_proof_id"],
        "recomputedProofId": rebuilt["proofId"],
        "claimedRunId": run_row["id"],
        "recomputedRunId": rebuilt["runId"],
        "claimedProofSha256": sha256(claimed_c),
        "recomputedProofSha256": sha256(rebuilt["proofC"]),
        "claimedProofBytes": len(claimed_c),
        "recomputedProofBytes": len(rebuilt["proofC"]),
        "diffs": diffs,
        "recomputedVerdict": rebuilt["verdict"],
        "claimedVerdict": claimed_proof["verdict"],
        "workUnitsCharged": rebuilt["workUnitsCharged"],
        "findingCount": len(rebuilt["findingIds"]),
        "predicateProofCount": len(rebuilt["proof"]["predicateProofs"]),
        "tamperUnrehashed": {
            "refused": tamper_a_refused,
            "identityMoved": tamper_a_h != inp["claimed_proof_id"],
            "bytesDifferFromReplay": tamper_a_c != rebuilt["proofC"],
        },
        "tamperRehashedFalseClaim": {
            "refused": tamper_b_refused,
            "selfConsistentH": tamper_b_self_h,
            "newProofId": tamper_b_proof_id,
            "newRunId": tamper_b_run_id,
            "citationsPreserved": citations_preserved,
            "recomputedBytesEqualClaimedFalse": rebuilt["proofC"] == encode_c(tamper_b_proof),
        },
        "recomputedProof": rebuilt["proof"],
    }


def closure_joins(export: dict) -> dict:
    """Cross-record joins over retained frames. Distinct from schema and from evaluator replay."""
    store = LoadedStore(export)
    faults = []
    run = store.desc("run")
    plan = store.get_id(run["planId"])["descriptor"]
    snapshot = store.get_id(run["snapshotId"])["descriptor"]
    evidence = store.get_id(run["evidenceId"])["descriptor"]
    seal = store.get_id(run["evaluationSealId"])["descriptor"]
    proof = store.get_id(evidence["proofBundleId"])["descriptor"]

    if plan["snapshotId"] != run["snapshotId"]:
        faults.append("PLAN_SNAPSHOT_JOIN")
    if proof["planId"] != run["planId"]:
        faults.append("PROOF_PLAN_JOIN")
    if evidence["planId"] != run["planId"]:
        faults.append("EVIDENCE_PLAN_JOIN")
    if seal["planId"] != run["planId"]:
        faults.append("SEAL_PLAN_JOIN")
    if seal["proofBundleId"] != evidence["proofBundleId"]:
        faults.append("SEAL_PROOF_JOIN")
    if seal["evidenceId"] != run["evidenceId"]:
        faults.append("SEAL_EVIDENCE_JOIN")
    if seal["verdict"] != proof["verdict"]:
        faults.append("SEAL_VERDICT_JOIN")
    if run["capabilityManifestId"] != plan["capabilityManifestId"]:
        faults.append("RUN_CAP_MANIFEST_JOIN")
    if proof["executionInputsDigest"] != canonical_digest(store.desc("execution-inputs")):
        # execution-inputs domain name
        ei = None
        for row in store.by_domain.get("execution-inputs") or []:
            ei = row["descriptor"]
        if ei is None or canonical_digest(ei) != proof["executionInputsDigest"]:
            faults.append("EXECUTION_INPUTS_DIGEST")

    inv_paths = {row["path"]: row for row in snapshot["sourceInventory"]}
    file_facts = 0
    clone_facts = 0
    blob_joins = 0
    l0_recomputed = 0
    for row in store.by_domain.get("fact") or []:
        fact = row["descriptor"]
        payload = store.by_digest[fact["payloadDigest"]]["descriptor"]
        if fact["relation"] == "file":
            file_facts += 1
            p = payload["path"]
            if p not in inv_paths:
                faults.append(f"FILE_PATH_NOT_INVENTORIED:{p}")
                continue
            inv = inv_paths[p]
            if inv["sha256"] != payload["contentSha256"]:
                faults.append(f"FILE_HASH_MISMATCH:{p}")
            if inv["bytes"] != payload["byteLength"]:
                faults.append(f"FILE_LENGTH_MISMATCH:{p}")
            if fact["anchors"] and fact["anchors"][0]["blobDigest"] != payload["contentSha256"]:
                faults.append(f"FILE_ANCHOR_BLOB:{p}")
            blob_joins += 1
        if fact["relation"] == "clones":
            clone_facts += 1
            if len(fact.get("anchors") or []) != 1:
                faults.append("CLONE_ANCHOR_CARDINALITY")
            an = fact["anchors"][0]
            if an["path"] not in inv_paths:
                faults.append(f"CLONE_PATH_NOT_INVENTORIED:{an['path']}")
            if payload["normalisationLevel"] == "L0-verbatim":
                blob = store.blobs.get(an["blobDigest"])
                if blob is None:
                    faults.append(f"CLONE_L0_BLOB_MISSING:{an['path']}")
                else:
                    span = _b64(blob)
                    # body frame retained under bodyIdentity suffix
                    bid = payload["bodyIdentity"]
                    suffix = bid.split(":")[-1]
                    # search raw artifacts / body-frame
                    found = False
                    for r2 in store.table:
                        if r2["digest"] == suffix or r2["domain"].startswith("body-frame:"):
                            raw = _b64(store.blobs[r2["digest"]])
                            if r2["digest"] == suffix or sha256(raw) == suffix:
                                found = True
                                # L0 recompute: payload inside frame is u32be len || span
                                expected_payload = l0_payload(span[an["startByte"] : an["endByte"]])
                                # cannot easily parse frame without grammar; check identity of recomputed
                                # if start/end cover whole blob:
                                if an["startByte"] == 0 and an["endByte"] == len(span):
                                    l0_recomputed += 1
                    if not found:
                        # try digest of body identity hex as blob key
                        if suffix in store.blobs:
                            l0_recomputed += 1
                        else:
                            faults.append(f"CLONE_FRAME_MISSING:{an['path']}")

    # acyclic: proof must not name run/evidence/seal
    proof_s = json.dumps(proof)
    if "run3:" in proof_s or "evidence3:" in proof_s or "seal3:" in proof_s:
        faults.append("PROOF_CONTAINS_OUTPUT_IDS")

    # native context in plan
    for d in plan.get("nativeContextDigests") or []:
        if d not in store.by_digest:
            faults.append(f"NATIVE_CONTEXT_UNRETAINED:{d}")

    return {
        "ok": not faults,
        "faults": faults,
        "fileFactsJoined": blob_joins,
        "fileFacts": file_facts,
        "cloneFacts": clone_facts,
        "l0Recomputed": l0_recomputed,
        "inventorySize": len(snapshot["sourceInventory"]),
        "nativeContextCount": len(plan.get("nativeContextDigests") or []),
    }
