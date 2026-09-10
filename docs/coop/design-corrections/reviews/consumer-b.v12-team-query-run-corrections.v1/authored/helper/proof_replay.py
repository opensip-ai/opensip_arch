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
from helper.schema_admit import validate_against
from helper.store import Store

TATTR_REL = "docs/coop/design-corrections/foundation/target-attribution.schema.v1.json"
REL_REG_TARGET_FIELD = {
    "imports": "resolvedTarget",
    "calls": "resolvedCallee",
    "references": "resolvedBinding",
    "control-flow": "to",
    "reachability": "reachable",
}


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

    attributions = []
    for r in ei["selectedRefs"]:
        if r["domain"] == "target-attribution":
            attributions.append(parse_canonical(store, r["digest"]))

    ctx_hex = plan["nativeContextDigests"][0]
    ctx_frame = rehash(store, ctx_hex)
    ctx_parsed = parse_h_frame(ctx_frame)
    ctx = ctx_parsed["value"]
    ctx_domain = ctx_parsed["domain"]
    uni_hex = None
    for f in facts:
        uni_hex = f["record"]["sourceUniverse"]
        break
    if uni_hex is None:
        raise RuntimeError("no fact universe")
    uni_frame = rehash(store, uni_hex)
    uni_parsed = parse_h_frame(uni_frame)
    uni = uni_parsed["value"]
    uni_domain = uni_parsed["domain"]

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
    extra_cids = []
    if isinstance(ctx.get("grammarBundle"), dict) and ctx["grammarBundle"].get("closureId"):
        extra_cids.append(ctx["grammarBundle"]["closureId"])
    tc = ctx.get("toolClosure") or {}
    if isinstance(tc, dict) and tc.get("closureId"):
        extra_cids.append(tc["closureId"])
    extra_cids.append(emission_plan["rules"][0]["detectorClosure"])
    extra_cids.append(ei["evaluatorClosure"])
    for cid in extra_cids:
        if cid and cid not in closures:
            closures[cid] = parse_typed_h(store, cid, "closure")

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
        "attributions": attributions,
        "ctx": ctx,
        "ctx_hex": ctx_hex,
        "ctx_domain": ctx_domain,
        "uni": uni,
        "uni_hex": uni_hex,
        "uni_domain": uni_domain,
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

    if g.get("ctx_domain") == "native.context.syntax.v2":
        try:
            syn = admit_syntax_native_context(store, g["ctx"])
            join("grammar-artifacts-in-closure-tree", True, json.dumps(syn["tree"]))
        except AdmissionError as e:
            join("grammar-artifacts-in-closure-tree", False, f"{e.code}: {e}")
        join(
            "selected-grammar-subset",
            set(g["uni"].get("selectedGrammarIds") or [])
            <= {x["grammarId"] for x in g["ctx"]["grammarBundle"]["grammars"]},
            str(g["uni"].get("selectedGrammarIds")),
        )
        join("universe-binds-context", g["uni"]["nativeContextId"] == "sha256:" + g["ctx_hex"])
        join("resolution-attempted-false", g["uni"].get("resolutionAttempted") is False)
    else:
        join("universe-binds-context", g["uni"].get("nativeContextId") == "sha256:" + g["ctx_hex"])

    try:
        memb = admit_unit_membership(store, g["enum_plan"]["membershipDigest"])
        if g.get("ctx_domain") == "native.context.syntax.v2":
            join(
                "syntax-only-membership-unitOrdinal-null",
                memb["units"] == [] and all(r["unitOrdinal"] is None for r in memb["rows"]),
                json.dumps({"units": memb["units"], "rows": memb["rows"]}),
            )
        else:
            join(
                "unit-membership-schema",
                True,
                json.dumps({"nUnits": len(memb.get("units") or []), "nRows": len(memb.get("rows") or [])}),
            )
    except AdmissionError as e:
        join("unit-membership", False, f"{e.code}: {e}")
        memb = None

    try:
        enum_adm = admit_enumeration_inventories(store, g["enum_plan"], g["inventories"])
        join("enumeration-exactly-one-inventory-per-cell-program-kind", True, str(enum_adm["expected"]))
    except AdmissionError as e:
        join("enumeration-exactly-one-inventory-per-cell-program-kind", False, f"{e.code}: {e}")

    for inv in g["inventories"]:
        if inv.get("kind") != "file" or inv.get("state") != "complete":
            continue
        cell = g["enum_plan"]["cells"][inv["cellOrdinal"]]
        pb = cell["programBindings"][inv["programOrdinal"]]
        extent = set()
        for e in pb.get("extents") or []:
            if e.get("kind") == "file":
                extent = set(e.get("paths") or [])
        examined = set(inv.get("examinedPaths") or [])
        row_paths = {r["path"] for r in inv.get("rows") or []}
        join(
            f"file-inventory[{inv['cellOrdinal']}]-complete-extent-equality",
            extent == examined == row_paths and len(inv.get("rows") or []) == len(examined),
            json.dumps(
                {
                    "extent": sorted(extent),
                    "examined": sorted(examined),
                    "rows": sorted(row_paths),
                }
            ),
        )

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
        elif rec["relation"] == "imports":
            join(
                "imports-payload-SubjectIdV1-importer",
                isinstance(pl.get("importer"), str) and ":" in pl.get("importer", ""),
                json.dumps({"importer": pl.get("importer"), "resolvedTarget": pl.get("resolvedTarget")}),
            )
            join("imports-anchor-cardinality", len(rec.get("anchors") or []) >= 1, str(len(rec.get("anchors") or [])))
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

    file_covs_complete = [
        c
        for c in g["coverages"]
        if c["record"]["relation"] == "file" and (c.get("entry") or {}).get("coverage") == "complete"
    ]
    if file_covs_complete:
        inv_paths = {r["path"] for r in g["snapshot"]["sourceInventory"]}
        fact_paths = {
            g["payloads"][f["id"]]["path"] for f in g["facts"] if f["record"]["relation"] == "file"
        }
        missing = sorted(inv_paths - fact_paths)
        extra = sorted(fact_paths - inv_paths)
        join(
            "file-enumerated-snapshot-totality",
            not missing and not extra,
            json.dumps({"missing": missing, "extra": extra, "nSnapshot": len(inv_paths)}),
        )

    facts_by_id = {f["id"]: f for f in g["facts"]}
    selected_closures = set(g["plan"]["semanticClosures"])
    seen_attr_pairs: set[tuple[str, str]] = set()
    view_fact_ids = set(g["view"]["facts"])
    for i, attr in enumerate(g.get("attributions") or []):
        stock = validate_against(attr, TATTR_REL, selector="#", label=f"TargetAttributionV1[{i}]")
        join(
            f"target-attribution[{i}]-schema",
            stock["stockOk"],
            json.dumps(stock.get("errors")[:3] if not stock["stockOk"] else {"sourceFactId": attr.get("sourceFactId")}),
        )
        join(f"target-attribution[{i}]-plan", attr.get("planId") == g["plan_id"], str(attr.get("planId")))
        pair = (attr.get("planId"), attr.get("sourceFactId"))
        join(f"target-attribution[{i}]-unique-fact", pair not in seen_attr_pairs, str(pair))
        seen_attr_pairs.add(pair)
        fid = attr.get("sourceFactId")
        in_view = fid in view_fact_ids
        join(f"target-attribution[{i}]-fact-in-plan-view", in_view, str(fid))
        if not in_view:
            continue
        frec = facts_by_id[fid]["record"]
        pl = g["payloads"][fid]
        join(
            f"target-attribution[{i}]-producer-equals-fact",
            attr.get("producerClosure") == frec["producerClosure"],
            str(attr.get("producerClosure")),
        )
        join(
            f"target-attribution[{i}]-producer-selected",
            attr.get("producerClosure") in selected_closures,
            str(attr.get("producerClosure")),
        )
        ck = (g["closures"].get(attr.get("producerClosure")) or {}).get("kind")
        join(f"target-attribution[{i}]-producer-kind-provider", ck == "provider", str(ck))
        join(
            f"target-attribution[{i}]-universe",
            attr.get("targetUniverse") == frec["targetUniverse"],
            str(attr.get("targetUniverse")),
        )
        field = REL_REG_TARGET_FIELD.get(frec["relation"])
        if field:
            join(
                f"target-attribution[{i}]-native-id",
                attr.get("targetNativeId") == pl.get(field),
                json.dumps({"field": field, "attr": attr.get("targetNativeId"), "payload": pl.get(field)}),
            )
        else:
            join(f"target-attribution[{i}]-field-on-rung", False, frec["relation"])

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
    complete_file_invs = [inv for inv in file_invs if inv.get("state") == "complete"]
    subjects = select_file_subjects(inventories=complete_file_invs, universe=g["uni_hex"], store=None)
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
        file_inventories=complete_file_invs,
        store=None,
    )
    return {"proof": proof, "subjects": subjects}


def logical_result_tamper(claimed: dict) -> dict:
    """Preserve identities and citation membership; change claimed logical result."""
    t = copy.deepcopy(claimed)
    t["verdict"] = "fail" if claimed.get("verdict") == "pass" else "pass"
    # Keep predicateProofs, findingIds, witnesses, input refs. Change claimed node value.
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


def remint_enclosing_after_proof_tamper(store: Store, g: dict, tampered_proof: dict) -> dict:
    """Full-graph result tamper: remint proof, evidence, seal, run; then the replacement can be admitted.

    A foreign proof3 identity cannot join this Run's evaluation-seal.proofBundleId.
    Stale-hash (C inequality of a mutated field without reminting) is a separate control.
    """
    proof_h = store.put_h("proof-bundle", tampered_proof, label="tampered-proof")
    evidence = dict(g["evidence"])
    evidence["proofBundleId"] = proof_h["typedId"]
    ev_h = store.put_h("semantic-evidence", evidence, label="tampered-evidence")
    seal = dict(g["seal"])
    seal["evidenceId"] = ev_h["typedId"]
    seal["proofBundleId"] = proof_h["typedId"]
    seal["verdict"] = tampered_proof["verdict"]
    seal_h = store.put_h("evaluation-seal", seal, label="tampered-seal")
    run = dict(g["run"])
    run["evidenceId"] = ev_h["typedId"]
    run["evaluationSealId"] = seal_h["typedId"]
    run_h = store.put_h("run", run, label="tampered-run")
    return {
        "proofId": proof_h["typedId"],
        "evidenceId": ev_h["typedId"],
        "sealId": seal_h["typedId"],
        "runId": run_h["typedId"],
        "proof": tampered_proof,
        "evidence": evidence,
        "seal": seal,
        "run": run,
    }
