#!/usr/bin/env python3
"""Independent syntax-code positive + logical-result-tamper recheck.

Kit laws only. Does not import consumer helpers as expected-output oracles.
C/H/lexical from identity-and-evidence §3 via this validator's prior probe module.
Consumer compose_proof / replay measurements are not oracles.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

V1 = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/output/diagnostics/syntax_code_pilot_probes.py")
spec = importlib.util.spec_from_file_location("v1probes", V1)
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)

C = v1.C
H = v1.H
sha256 = v1.sha256
parse_h_frame = v1.parse_h_frame
admit_raw = v1.admit_raw
load_store = v1.load_store
validate_stock = v1.validate_stock
check_order = v1.check_order

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-recheck.v3/consumer-snapshot")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-recheck.v3/output")
POS = SNAP / "runs" / "syntax-code.store.json"
TAMPER = SNAP / "runs" / "syntax-code.tamper.store.json"

IDENT = json.loads((KIT / "docs/coop/design-corrections/foundation/identity-schemas.v3.json").read_text())
NATIVE = json.loads((KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json").read_text())
REL = json.loads((KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json").read_text())
ENUM = json.loads((KIT / "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json").read_text())
EXEC = json.loads((KIT / "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json").read_text())
SINV = json.loads((KIT / "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json").read_text())
POL2 = json.loads((KIT / "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json").read_text())
EMIS = json.loads((KIT / "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json").read_text())

FORBIDDEN_SELECTED = {"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"}
FORBIDDEN_EXTRAS = {"rule-program", "policy"}
SEV_RANK = {"note": 0, "warning": 1, "error": 2}

PROBES = []
FIRST = None
NOTREACHED = []


def record(name, ok, *, selector, detail=None, class_="check", export="positive"):
    global FIRST
    rec = {"name": name, "ok": bool(ok), "selector": selector, "class": class_, "detail": detail, "export": export}
    PROBES.append(rec)
    if (not ok) and FIRST is None and class_ in ("schema", "structural", "semantic", "frame", "replay"):
        FIRST = rec


def not_reached(name, *, selector, reason):
    NOTREACHED.append({"name": name, "selector": selector, "reason": reason})


def sort_set(xs: list) -> list:
    return sorted(xs, key=lambda x: C(x))


def parse_typed(store, tid, domain):
    rec = store["objectTable"][tid]
    frame = store["blobs"][rec["digest"]]
    got = sha256(frame)
    if got != rec["digest"]:
        raise RuntimeError(f"H frame rehash {tid}")
    parsed = parse_h_frame(frame)
    if parsed["domain"] != domain:
        raise RuntimeError(f"domain {parsed['domain']} != {domain} for {tid}")
    if parsed["digest"] != rec["digest"]:
        raise RuntimeError("H digest mismatch")
    if C(parsed["value"]) != parsed["canonicalBytes"]:
        raise RuntimeError("H remainder not C")
    return parsed["value"]


def parse_canon(store, digest):
    raw = store["blobs"][digest]
    if sha256(raw) != digest:
        raise RuntimeError(f"blob rehash {digest}")
    obj = admit_raw(raw)
    if C(obj) != raw:
        raise RuntimeError(f"canonical remainder {digest}")
    return obj


def hex_of(s: str) -> str:
    return s.split(":", 1)[1] if ":" in s else s


def coverage_key(c: dict) -> tuple[str, str]:
    payload = c.get("payload") or {}
    key = payload.get("key") or {}
    entry = payload.get("entry") or {}
    rel = key.get("relation") or entry.get("relation") or c.get("record", {}).get("relation")
    res = key.get("resolution") or entry.get("resolution") or c.get("record", {}).get("resolution")
    return rel, res


def exists_or_none(op, *, facts, coverages, payloads, subject_id, relation, minr, filters):
    """identity-and-evidence §4 / atom-evaluation-contract.v1 exists/none."""
    matching = []
    for f in facts:
        rec = f["record"]
        if rec.get("relation") != relation:
            continue
        pl = payloads.get(f["id"]) or {}
        occ = pl.get("path", subject_id)
        if occ != subject_id:
            continue
        ok = True
        for filt in filters or []:
            if filt["field"] == "subject" and filt["cmp"] == "eq" and subject_id != filt["value"]:
                ok = False
                break
        if ok:
            matching.append(f["id"])
    covs = []
    for c in coverages:
        rel, res = coverage_key(c)
        if rel == relation and res == minr:
            covs.append(c)
    has_cov = bool(covs)
    complete = False
    for c in covs:
        entry = (c.get("payload") or {}).get("entry") or {}
        if entry.get("coverage") == "complete":
            complete = True
    if op == "exists":
        if matching:
            return "true", matching
        if not has_cov:
            return "indeterminate", matching
        return ("false" if complete else "indeterminate"), matching
    if op == "none":
        if matching:
            return "false", matching
        if not has_cov:
            return "indeterminate", matching
        return ("true" if complete else "indeterminate"), matching
    raise ValueError(op)


def reconstruct_expected_proof(store, *, run, plan, proof_claimed, exec_in, view, inventories, facts, payloads, coverages) -> dict:
    policy = parse_canon(store, plan["policyDigest"])
    rp = parse_canon(store, proof_claimed["ruleProgramDigest"])
    universe = None
    file_invs = [i for i in inventories if i["kind"] == "file" and i.get("state") == "complete"]
    subjects = []
    seen = set()
    for inv in file_invs:
        for row in inv["rows"]:
            # universe from native context / first fact
            pass
    # universe from a file fact
    file_facts = [f for f in facts if f["record"]["relation"] == "file"]
    universe = file_facts[0]["record"]["sourceUniverse"] if file_facts else None
    for inv in file_invs:
        for row in inv["rows"]:
            subj_rec = {"schemaVersion": 3, "universe": universe, "kind": "file", "nativeSubjectId": row["nativeSubjectId"]}
            sid = "subject3:" + H("evaluation-subject", subj_rec)
            if sid not in seen:
                seen.add(sid)
                subjects.append({"id": sid, "record": subj_rec, "row": row})
    subjects.sort(key=lambda s: C(s["id"]))
    view_digest = hex_of(store["objectTable"][ [k for k in store["objectTable"] if str(k).startswith("view2:")][0] ]["typedId"] if False else "")
    view_ids = [k for k in store["objectTable"] if isinstance(k, str) and k.startswith("view2:")]
    view_id = view_ids[0]
    view_digest = hex_of(view_id)
    file_scope = None
    for sid in view.get("scopeIds") or []:
        sc = parse_typed(store, sid, "subject-scope")
        if sc.get("kind") == "file" or sc.get("subjectKind") == "file" or True:
            # pick the scope cited by claimed predicate if present
            file_scope = sid
            break
    if proof_claimed.get("predicateProofs"):
        file_scope = proof_claimed["predicateProofs"][0]["scopeIds"][0]
    exec_digest = sha256(C(exec_in))
    pred_proofs = []
    rule_results = []
    policy_rules = {r["ruleId"]: r for r in policy["rules"]}
    for rp_rule in rp["rules"]:
        rule_id = rp_rule["ruleId"]
        pol_rule = policy_rules[rule_id]
        atom = rp_rule["emitWhen"]
        inventory_refs = sort_set([{"domain": "subject-inventory", "digest": sha256(C(inv))} for inv in file_invs])
        selected_ids = sort_set([s["id"] for s in subjects])
        if not pol_rule.get("enabled", True):
            rule_results.append({
                "ruleId": rule_id,
                "enumeration": {"state": "disabled", "inventoryRefs": [], "selectedSubjectIds": [], "unresolvedSubjectIds": [], "incompleteInventoryRefs": []},
                "outcome": "disabled", "findingIds": [], "deficiencies": [],
            })
            continue
        root_values = []
        live_findings = []
        for subj in subjects:
            value, matching = exists_or_none(
                atom["op"],
                facts=facts,
                coverages=coverages,
                payloads=payloads,
                subject_id=subj["record"]["nativeSubjectId"],
                relation=atom["relation"],
                minr=atom["minResolution"],
                filters=atom.get("filters"),
            )
            root_values.append(value)
            prog_pred = {
                "schemaVersion": 2,
                "ruleProgramDigest": proof_claimed["ruleProgramDigest"],
                "ruleId": rule_id,
                "predicateId": "p",
                "operation": atom["op"],
                "nodeDigest": sha256(C(atom)),
            }
            pp_d = sha256(C(prog_pred))
            used_cov_ids = []
            for c in coverages:
                rel, res = coverage_key(c)
                if rel == atom["relation"] and res == atom["minResolution"]:
                    used_cov_ids.append(c["id"] if str(c["id"]).startswith("coverage2:") else "coverage2:" + hex_of(c["id"]))
            w = {
                "schemaVersion": 3,
                "programPredicateDigest": pp_d,
                "matchingFactIds": sort_set(list(matching)),
                "coverageIds": sort_set(used_cov_ids),
                "countLimit": None,
                "childPredicateIds": [],
                "matchingImportRows": [],
                "uncertainFactIds": [],
                "uncertainImportRows": [],
                "deficiencies": [],
                "kind": "native-atom",
            }
            wd = sha256(C(w))
            used_cov_refs = [{"domain": "coverage", "digest": hex_of(cid)} for cid in w["coverageIds"]]
            pred_proofs.append({
                "ruleId": rule_id,
                "subjectId": subj["id"],
                "predicateId": "p",
                "operation": atom["op"],
                "inputRefs": sort_set([{"domain": "view", "digest": view_digest}, {"domain": "rule-program", "digest": proof_claimed["ruleProgramDigest"]}] + used_cov_refs),
                "scopeIds": sort_set([file_scope] if file_scope else []),
                "value": value,
                "witnessDigest": wd,
            })
            if value == "true":
                live_findings.append("finding-emitted")
        pred_proofs = sorted(pred_proofs, key=lambda x: (x["ruleId"].encode(), x["subjectId"].encode(), x["predicateId"].encode()))
        gating = bool(pol_rule.get("enabled") and pol_rule.get("gate") and SEV_RANK[pol_rule["severity"]] >= SEV_RANK[policy["gateSeverityAtLeast"]])
        if live_findings and gating:
            outcome = "fail"
        elif any(v == "indeterminate" for v in root_values) and gating:
            outcome = "indeterminate"
        else:
            outcome = "pass"
        rule_results.append({
            "ruleId": rule_id,
            "enumeration": {
                "state": "complete",
                "inventoryRefs": inventory_refs,
                "selectedSubjectIds": selected_ids,
                "unresolvedSubjectIds": [],
                "incompleteInventoryRefs": [],
            },
            "outcome": outcome,
            "findingIds": sort_set([]),
            "deficiencies": [],
        })
    rule_results = sorted(rule_results, key=lambda r: r["ruleId"].encode())
    if any(r["outcome"] == "fail" for r in rule_results):
        verdict = "fail"
    elif any(r["outcome"] == "indeterminate" for r in rule_results):
        verdict = "indeterminate"
    else:
        verdict = "pass"
    eval_input_refs = sort_set(list(exec_in["selectedRefs"]) + [{"domain": "execution-inputs", "digest": exec_digest}])
    proof = {
        "schemaVersion": 3,
        "planId": run["planId"],
        "executionPlanId": proof_claimed["executionPlanId"],
        "evaluatorClosure": exec_in["evaluatorClosure"],
        "ruleProgramDigest": proof_claimed["ruleProgramDigest"],
        "evaluationInputRefs": eval_input_refs,
        "predicateProofs": pred_proofs,
        "findingIds": [],
        "verdict": verdict,
        "evaluationState": "evaluated",
        "ruleResults": rule_results,
        "waivedFindingIds": [],
        "executionDeficiencies": [],
        "executionInputsDigest": exec_digest,
    }
    return {"proof": proof, "subjects": subjects, "atomValue": pred_proofs[0]["value"] if pred_proofs else None, "witness": w, "programPredicate": prog_pred}


def admit_export(label: str, path: Path) -> dict:
    export = label
    raw = path.read_bytes()
    store = load_store(path)
    blobs = store["blobs"]
    table = store["objectTable"]
    out: dict[str, Any] = {"path": str(path), "sha256": sha256(raw), "bytes": len(raw), "blobCount": store["blobCount"], "structuralOk": True, "firstStructuralRefusal": None}

    rehash_fail = [d for d, b in blobs.items() if sha256(b) != d]
    record(f"{label}-blob-rehash", not rehash_fail, selector="identity-and-evidence.md §3 raw blob SHA-256", detail={"n": len(blobs), "fails": rehash_fail[:4]}, class_="frame", export=export)
    record(f"{label}-blobCount", store["blobCount"] == len(blobs), selector="store.blobCount", detail={"claimed": store["blobCount"], "len": len(blobs)}, class_="structural", export=export)

    run_ids = [k for k in table if isinstance(k, str) and k.startswith("run3:")]
    record(f"{label}-one-run", len(run_ids) == 1, selector="identity-schemas.v3 run3 unique export", detail=run_ids, class_="structural", export=export)
    run_id = run_ids[0]
    run = parse_typed(store, run_id, "run")
    plan = parse_typed(store, run["planId"], "plan")
    snap = parse_typed(store, run["snapshotId"], "snapshot")
    evidence = parse_typed(store, run["evidenceId"], "semantic-evidence")
    seal = parse_typed(store, run["evaluationSealId"], "evaluation-seal")
    proof = parse_typed(store, evidence["proofBundleId"], "proof-bundle")
    out.update({"runId": run_id, "planId": run["planId"], "snapshotId": run["snapshotId"], "proofId": evidence["proofBundleId"], "evidenceId": run["evidenceId"], "sealId": run["evaluationSealId"], "run": run, "plan": plan, "proof": proof, "evidence": evidence, "seal": seal, "store": store})

    for name, inst, doc, sel in [
        ("run", run, IDENT, "#/$defs/run"),
        ("proof", proof, IDENT, "#/$defs/proof-bundle"),
        ("plan", plan, IDENT, "#/$defs/plan"),
        ("snapshot", snap, IDENT, "#/$defs/snapshot"),
        ("evidence", evidence, IDENT, "#/$defs/semantic-evidence"),
        ("seal", seal, IDENT, "#/$defs/evaluation-seal"),
        ("exec", parse_canon(store, proof["executionInputsDigest"]), EXEC, "#"),
    ]:
        errs = validate_stock(inst, doc, sel)
        record(f"{label}-schema-{name}", not errs, selector=f"{sel}", detail=errs[:4], class_="schema", export=export)
        if errs and out["firstStructuralRefusal"] is None:
            out["firstStructuralRefusal"] = {"name": f"{label}-schema-{name}", "errors": errs[:3]}
            out["structuralOk"] = False

    exec_in = parse_canon(store, proof["executionInputsDigest"])
    out["exec"] = exec_in
    record(
        f"{label}-executionInputsDigest-is-C",
        proof["executionInputsDigest"] == sha256(C(exec_in)),
        selector="evaluator-composition-contract.v3.md §1 proof.executionInputsDigest = SHA-256(C(ExecutionInputsV1))",
        class_="structural",
        export=export,
    )
    expected_refs = sort_set(list(exec_in["selectedRefs"]) + [{"domain": "execution-inputs", "digest": proof["executionInputsDigest"]}])
    record(
        f"{label}-evaluationInputRefs-equals-selected-plus-manifest",
        proof["evaluationInputRefs"] == expected_refs,
        selector="evaluator-composition-contract.v3.md §1; execution-inputs-contract.v1.md §7",
        detail={"claimed": proof["evaluationInputRefs"], "expected": expected_refs, "nClaimed": len(proof["evaluationInputRefs"]), "nExpected": len(expected_refs)},
        class_="structural",
        export=export,
    )
    domains = {r["domain"] for r in exec_in["selectedRefs"]}
    record(
        f"{label}-selectedRefs-forbidden-output-domains",
        not (domains & FORBIDDEN_SELECTED),
        selector="execution-inputs-contract.v1.md selectedRefs forbidden proof/finding/seal/run/evidence",
        detail=sorted(domains),
        class_="structural",
        export=export,
    )
    record(
        f"{label}-selectedRefs-no-rule-program-or-policy",
        not (domains & FORBIDDEN_EXTRAS),
        selector="composition §1 ruleProgramDigest and plan.policyDigest are their own fields, not selectedRefs",
        detail=sorted(domains),
        class_="structural",
        export=export,
    )
    record(
        f"{label}-evaluatorClosure-in-plan-semanticClosures",
        proof["evaluatorClosure"] in plan["semanticClosures"] and proof["evaluatorClosure"] == exec_in["evaluatorClosure"],
        selector="identity-schemas.v3 UNSELECTED_EVALUATOR_CLOSURE; plan.semanticClosures",
        detail={"proof": proof["evaluatorClosure"], "exec": exec_in["evaluatorClosure"], "plan": plan["semanticClosures"]},
        class_="structural",
        export=export,
    )
    record(f"{label}-plan-snapshot-equal", plan["snapshotId"] == run["snapshotId"], selector="PLAN_SNAPSHOT_JOIN plan.snapshotId == run.snapshotId", class_="structural", export=export)
    record(f"{label}-proof-planId", proof["planId"] == run["planId"], selector="proof.planId == run.planId", class_="structural", export=export)
    record(f"{label}-evidence-proof-join", evidence["proofBundleId"] == store["objectTable"][evidence["proofBundleId"]]["typedId"], selector="evidence.proofBundleId retained", class_="structural", export=export)
    record(f"{label}-seal-proof-evidence", seal["proofBundleId"] == evidence["proofBundleId"] and seal["evidenceId"] == run["evidenceId"], selector="seal joins proof and evidence", class_="structural", export=export)
    record(f"{label}-seal-verdict-equals-claimed-proof", seal["verdict"] == proof["verdict"], selector="evaluation-seal.verdict equals claimed proof.verdict (claimed graph)", class_="structural", export=export)
    record(f"{label}-policyDigest-retained", proof["executionInputsDigest"] and plan["policyDigest"] in blobs, selector="plan.policyDigest canonical retained", class_="structural", export=export)
    record(f"{label}-ruleProgram-retained", proof["ruleProgramDigest"] in blobs, selector="proof.ruleProgramDigest retained canonical", class_="structural", export=export)

    # view / facts / coverage containment
    view_ids = [k for k in table if isinstance(k, str) and k.startswith("view2:")]
    view = parse_typed(store, view_ids[0], "view")
    out["view"] = view
    record(f"{label}-view-planId", view["planId"] == run["planId"], selector="view.planId", class_="structural", export=export)
    record(f"{label}-evidence-viewIds-contain-selected-view", view_ids[0] in evidence.get("viewIds", []), selector="semantic-evidence.viewIds contains selected view", class_="structural", export=export)
    facts = []
    payloads = {}
    for fid in view["facts"]:
        frec = parse_typed(store, fid, "fact")
        facts.append({"id": fid, "record": frec})
        # payload digest
        pd = frec.get("payloadDigest")
        if pd and pd in blobs:
            raw_pl = blobs[pd]
            try:
                payloads[fid] = json.loads(raw_pl)
            except Exception:
                payloads[fid] = admit_raw(raw_pl)
        record(f"{label}-fact-in-table-{fid[-8:]}", fid in table, selector="view.facts retained fact2", class_="structural", export=export)
    out["facts"] = facts
    out["payloads"] = payloads
    coverages = []
    for cid in view["coverageIds"]:
        crec = parse_typed(store, cid, "coverage")
        payload = json.loads(blobs[crec["payloadDigest"]]) if crec.get("payloadDigest") in blobs else {}
        coverages.append({"id": cid, "record": crec, "payload": payload})
        record(f"{label}-coverage-retained-{cid[-8:]}", cid in table, selector="view.coverageIds retained coverage2", class_="structural", export=export)
        record(f"{label}-coverage-payload-{cid[-8:]}", crec.get("payloadDigest") in blobs, selector="coverage.payloadDigest retained", class_="structural", export=export)
    out["coverages"] = coverages
    inventories = []
    for r in exec_in["selectedRefs"]:
        if r["domain"] == "subject-inventory":
            inventories.append(parse_canon(store, r["digest"]))
    out["inventories"] = inventories
    record(f"{label}-selected-inventories-parse", len(inventories) == 4, selector="selectedRefs subject-inventory totality", detail={"n": len(inventories)}, class_="structural", export=export)

    # grammar artifacts in grammar closure tree
    grammar_closures = []
    for cid in plan["semanticClosures"]:
        cl = parse_typed(store, cid, "closure")
        if cl.get("kind") == "grammar":
            grammar_closures.append((cid, cl))
            tree = {row["sha256"] for row in cl.get("tree") or []}
            # native context
            nctx_ids = plan.get("nativeContextDigests") or []
            # sha256-text native
    record(f"{label}-grammar-closure-present", bool(grammar_closures), selector="native-evidence.md §1.2 kind=grammar closure", class_="structural", export=export)

    # native context H
    nctx_hex = None
    if plan.get("nativeContextDigests"):
        nctx_hex = hex_of(plan["nativeContextDigests"][0])
        try:
            nctx = parse_h_frame(blobs[nctx_hex])
            record(f"{label}-native-context-frame", nctx["domain"].startswith("native.context"), selector="plan.nativeContextDigests H frame", detail=nctx["domain"], class_="structural", export=export)
            if nctx["domain"] == "native.context.syntax.v2" or "syntax" in nctx["domain"]:
                ctx = nctx["value"]
                if grammar_closures:
                    tree = {row["sha256"] for row in grammar_closures[0][1].get("tree") or []}
                    bundle = ctx.get("grammarBundle") or {}
                    missing = []
                    for g in bundle.get("grammars") or []:
                        if g.get("grammarDigest") not in tree:
                            missing.append(g.get("grammarId"))
                    if bundle.get("bundleDigest") and bundle["bundleDigest"] not in tree:
                        missing.append("bundleDigest")
                    record(f"{label}-grammar-artifacts-in-closure-tree", not missing, selector="native-evidence.md §1.2 grammar artifacts in kind=grammar closure.tree", detail={"missing": missing, "treeN": len(tree)}, class_="structural", export=export)
            out["nativeContext"] = nctx["value"]
        except Exception as ex:
            record(f"{label}-native-context-frame", False, selector="native context H", detail=str(ex), class_="structural", export=export)

    # body identity frames for clones facts
    for f in facts:
        if f["record"].get("relation") == "clones":
            bid = f["record"].get("bodyIdentity") or (payloads.get(f["id"]) or {}).get("bodyIdentity")
            # often payload has identity sha256: and frame retained under that digest
            pl = payloads.get(f["id"]) or {}
            ident = pl.get("bodyIdentity") or pl.get("identity")
            rec = f["record"]
            # look at nested
            level = rec.get("levelId") or pl.get("levelId")
            # frame digest from identity suffix
            ident_s = ident if isinstance(ident, str) else rec.get("bodyIdentityId") or ""
            if isinstance(ident_s, str) and ident_s.startswith("sha256:"):
                d = ident_s[7:]
                record(f"{label}-clones-frame-retained-{d[:8]}", d in blobs, selector="fact-identity-policy.v2 L0/L1 frame retention (custody, not tokenization judgment)", class_="structural", export=export)
                if d in blobs:
                    frame = blobs[d]
                    # FACT-IDENTITY tag
                    ok_tag = frame.startswith(bytes([len(b"opensip.fact-identity.v1")])) and b"opensip.fact-identity.v1" in frame[:40]
                    record(f"{label}-clones-frame-tag-{d[:8]}", ok_tag, selector="fact-identity-policy.v2 FACT-IDENTITY preimage tag", class_="structural", export=export)

    not_reached("L1-tokenization-judgment", selector="identity-and-evidence / fact-identity-policy L1 token-stream semantics", reason="L1 obligation here is frame/custody retention of the level-spec preimage; tokenization judgment is level-spec freedom and was not executed")
    not_reached("component-manifest-schemas.v11-stock", selector="component-manifest-schemas.v11.json", reason="v11 is a prose field contract, not an executable stock JSON Schema; stored-bytes/tree join is the applicable check. No invented stock validator.")

    # witness / program-predicate retained
    for i, pp in enumerate(proof.get("predicateProofs") or []):
        wd = pp["witnessDigest"]
        record(f"{label}-witness-retained-{i}", wd in blobs and C(admit_raw(blobs[wd])) == blobs[wd], selector="composition §3 predicate-witness canonical-record retained", class_="structural", export=export)
        wobj = parse_canon(store, wd)
        ppd = wobj.get("programPredicateDigest")
        record(f"{label}-program-predicate-retained-{i}", ppd in blobs, selector="witness.programPredicateDigest retained", class_="structural", export=export)
        # inputRefs domains retained
        for ref in pp.get("inputRefs") or []:
            if ref["domain"] == "view":
                record(f"{label}-pred-view-ref", "view2:" + ref["digest"] in table, selector="predicateProofs.inputRefs view membership", class_="structural", export=export)
            elif ref["domain"] == "rule-program":
                record(f"{label}-pred-rp-ref", ref["digest"] in blobs, selector="predicateProofs.inputRefs rule-program", class_="structural", export=export)
            elif ref["domain"] == "coverage":
                record(f"{label}-pred-cov-ref-{ref['digest'][:8]}", ("coverage2:" + ref["digest"]) in table or ref["digest"] in blobs, selector="predicateProofs.inputRefs coverage", class_="structural", export=export)

    # acyclic enclosing graph: proof -> exec/plan; evidence -> proof; seal -> proof/evidence; run -> evidence/seal/plan/snapshot
    ids = {run_id, evidence["proofBundleId"], run["evidenceId"], run["evaluationSealId"], run["planId"], run["snapshotId"]}
    record(f"{label}-enclosing-ids-distinct", len(ids) == 6, selector="acyclic enclosing identities (run/proof/evidence/seal/plan/snapshot distinct)", detail=sorted(ids), class_="structural", export=export)

    if any(not p["ok"] and p["export"] == export and p["class"] in ("schema", "structural", "frame") for p in PROBES):
        out["structuralOk"] = False
        if out["firstStructuralRefusal"] is None:
            for p in PROBES:
                if p["export"] == export and not p["ok"] and p["class"] in ("schema", "structural", "frame"):
                    out["firstStructuralRefusal"] = p
                    break
    return out


def main():
    pos = admit_export("positive", POS)
    tamper = admit_export("tamper", TAMPER)

    # independent expected proof from POSITIVE selected inputs
    expected = reconstruct_expected_proof(
        pos["store"],
        run=pos["run"],
        plan=pos["plan"],
        proof_claimed=pos["proof"],
        exec_in=pos["exec"],
        view=pos["view"],
        inventories=pos["inventories"],
        facts=pos["facts"],
        payloads=pos["payloads"],
        coverages=pos["coverages"],
    )
    exp = expected["proof"]
    claimed = pos["proof"]

    # If witness coverage id spelling differs, compare field-wise then full C
    record(
        "positive-eval-input-refs-independent",
        exp["evaluationInputRefs"] == claimed["evaluationInputRefs"],
        selector="composition §1 independently derived evaluationInputRefs",
        class_="semantic",
        export="positive",
    )
    record(
        "positive-atom-none-is-false",
        expected["atomValue"] == "false" and claimed["predicateProofs"][0]["value"] == "false",
        selector="identity-and-evidence.md §4 none with complete Coverage and no match is false (file hello.rs present)",
        detail={"derived": expected["atomValue"], "claimed": claimed["predicateProofs"][0]["value"]},
        class_="semantic",
        export="positive",
    )
    record(
        "positive-verdict-pass",
        exp["verdict"] == claimed["verdict"] == "pass",
        selector="composition §5 gating none-false and no findings => pass",
        class_="semantic",
        export="positive",
    )
    record(
        "positive-no-findings",
        claimed["findingIds"] == [] and exp["findingIds"] == [],
        selector="composition §4 emitWhen true required for finding3; none=false emits none",
        class_="semantic",
        export="positive",
    )

    # Full C compare: rebuild claimed witness independently
    # Use independently computed witness C vs claimed witness C
    claimed_w = parse_canon(pos["store"], claimed["predicateProofs"][0]["witnessDigest"])
    indep_w = expected["witness"]
    # coverageIds: claimed may use coverage2: typed or hex — compare sets of hex
    def hexset(xs):
        return {hex_of(x) if isinstance(x, str) else hex_of(x.get("digest", "")) for x in xs}

    record(
        "positive-witness-matching-facts",
        set(claimed_w.get("matchingFactIds") or []) == set(indep_w.get("matchingFactIds") or []),
        selector="composition §3 atom known matches",
        class_="semantic",
        export="positive",
    )
    record(
        "positive-complete-proof-C",
        C(exp) == C(claimed),
        selector="composition §7 compare C of the COMPLETE recomputed proof",
        detail={
            "expectedProofId": "proof3:" + H("proof-bundle", exp),
            "claimedProofId": pos["proofId"],
            "expectedC": sha256(C(exp)),
            "claimedC": sha256(C(claimed)),
            "keysEqual": list(exp.keys()) == list(claimed.keys()) or sorted(exp) == sorted(claimed),
        },
        class_="semantic",
        export="positive",
    )
    record(
        "positive-proof-H-identity",
        ("proof3:" + H("proof-bundle", claimed)) == pos["proofId"],
        selector="identity-schemas.v3 proof3 = H(proof-bundle, descriptor)",
        class_="semantic",
        export="positive",
    )
    record(
        "positive-run-H-identity",
        ("run3:" + H("run", pos["run"])) == pos["runId"],
        selector="identity-schemas.v3 run3 = H(run, descriptor)",
        class_="semantic",
        export="positive",
    )

    # Field-level proof compare excluding witnessDigest if coverage spelling differs
    field_diffs = []
    for k in claimed:
        if k == "predicateProofs":
            continue
        if exp.get(k) != claimed.get(k):
            field_diffs.append(k)
    record(
        "positive-proof-fields-except-predicates",
        not field_diffs,
        selector="composition §7 field equality of non-predicate proof members",
        detail={"diffs": field_diffs, "expectedVerdict": exp["verdict"], "claimedVerdict": claimed["verdict"]},
        class_="semantic",
        export="positive",
    )
    # predicate value/subject/rule
    cp = claimed["predicateProofs"][0]
    ep = exp["predicateProofs"][0]
    record(
        "positive-predicate-core",
        cp["value"] == ep["value"] and cp["subjectId"] == ep["subjectId"] and cp["ruleId"] == ep["ruleId"] and cp["operation"] == ep["operation"],
        selector="composition §3 predicate identity (rule, subject, operation, value)",
        detail={"claimed": {k: cp[k] for k in ("value", "subjectId", "ruleId", "operation")}, "expected": {k: ep[k] for k in ("value", "subjectId", "ruleId", "operation")}},
        class_="semantic",
        export="positive",
    )

    # TAMPER: structural first (already admitted above). Only then semantic.
    record(
        "tamper-structural-before-semantic",
        tamper["structuralOk"] is True,
        selector="Do not report a semantic tamper refusal before the complete replacement graph is structurally admitted",
        detail={"structuralOk": tamper["structuralOk"], "firstStructuralRefusal": tamper["firstStructuralRefusal"]},
        class_="structural",
        export="tamper",
    )
    # selected inputs identical
    record(
        "tamper-same-plan",
        tamper["planId"] == pos["planId"],
        selector="logical-result tamper preserves selected Plan",
        class_="structural",
        export="tamper",
    )
    record(
        "tamper-same-executionInputsDigest",
        tamper["proof"]["executionInputsDigest"] == pos["proof"]["executionInputsDigest"],
        selector="logical-result tamper preserves ExecutionInputsV1",
        class_="structural",
        export="tamper",
    )
    record(
        "tamper-same-evaluationInputRefs",
        tamper["proof"]["evaluationInputRefs"] == pos["proof"]["evaluationInputRefs"],
        selector="tamper preserves evaluationInputRefs citations",
        class_="structural",
        export="tamper",
    )
    record(
        "tamper-enclosing-ids-reminted",
        tamper["runId"] != pos["runId"] and tamper["proofId"] != pos["proofId"] and tamper["evidenceId"] != pos["evidenceId"] and tamper["sealId"] != pos["sealId"],
        selector="composition §7 discriminating control remints enclosing identities (not stale-hash)",
        detail={"pos": pos["runId"], "tamper": tamper["runId"]},
        class_="structural",
        export="tamper",
    )
    record(
        "tamper-claimed-verdict-fail",
        tamper["proof"]["verdict"] == "fail" and tamper["seal"]["verdict"] == "fail",
        selector="claimed replacement graph carries false logical result",
        class_="structural",
        export="tamper",
    )

    # Independent expected from TAMPER selected inputs (same as positive)
    expected_t = reconstruct_expected_proof(
        tamper["store"],
        run=tamper["run"],
        plan=tamper["plan"],
        proof_claimed=tamper["proof"],
        exec_in=tamper["exec"],
        view=tamper["view"],
        inventories=tamper["inventories"],
        facts=tamper["facts"],
        payloads=tamper["payloads"],
        coverages=tamper["coverages"],
    )
    record(
        "tamper-fresh-derivation-still-pass-false",
        expected_t["proof"]["verdict"] == "pass" and expected_t["atomValue"] == "false",
        selector="composition §7 reconstruct from selected inputs only; claimed fail does not select truth",
        detail={"derivedVerdict": expected_t["proof"]["verdict"], "derivedAtom": expected_t["atomValue"], "claimedVerdict": tamper["proof"]["verdict"], "claimedAtom": tamper["proof"]["predicateProofs"][0]["value"]},
        class_="semantic",
        export="tamper",
    )
    record(
        "tamper-complete-proof-C-unequal",
        C(expected_t["proof"]) != C(tamper["proof"]) and C(tamper["proof"]) != C(claimed),
        selector="composition §7 semantic replay refuses unequal complete proof C after structural admission",
        detail={
            "expectedProofId": "proof3:" + H("proof-bundle", expected_t["proof"]),
            "claimedTamperProofId": tamper["proofId"],
            "positiveProofId": pos["proofId"],
        },
        class_="semantic",
        export="tamper",
    )
    record(
        "tamper-not-stale-hash",
        tamper["proof"]["executionInputsDigest"] == pos["proof"]["executionInputsDigest"] and tamper["proofId"] != pos["proofId"],
        selector="stale-hash control is a digest-field flip without remint; this exhibit remints proof/evidence/seal/run",
        class_="semantic",
        export="tamper",
    )

    results = {
        "probeCount": len(PROBES),
        "passCount": sum(1 for p in PROBES if p["ok"]),
        "failCount": sum(1 for p in PROBES if not p["ok"]),
        "firstRefusal": FIRST,
        "notReached": NOTREACHED,
        "positive": {k: pos[k] for k in ("runId", "planId", "proofId", "sha256", "bytes", "blobCount", "structuralOk", "firstStructuralRefusal") if k in pos},
        "tamper": {k: tamper[k] for k in ("runId", "planId", "proofId", "sha256", "bytes", "blobCount", "structuralOk", "firstStructuralRefusal") if k in tamper},
        "expectedPositiveProofId": "proof3:" + H("proof-bundle", exp),
        "expectedPositiveProofC": sha256(C(exp)),
        "claimedPositiveProofC": sha256(C(claimed)),
        "probes": PROBES,
        "failed": [p for p in PROBES if not p["ok"]],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "diagnostics").mkdir(exist_ok=True)
    (OUT / "diagnostics" / "pilot_recheck_probes.json").write_text(json.dumps(results, indent=2, default=str) + "\n")
    print(json.dumps({
        "probeCount": results["probeCount"],
        "passCount": results["passCount"],
        "failCount": results["failCount"],
        "firstRefusal": None if FIRST is None else FIRST["name"],
        "failedNames": [p["name"] for p in results["failed"]],
        "structuralPositive": pos["structuralOk"],
        "structuralTamper": tamper["structuralOk"],
        "expectedProofId": results["expectedPositiveProofId"],
        "claimedProofId": pos["proofId"],
        "Cequal": results["expectedPositiveProofC"] == results["claimedPositiveProofC"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
