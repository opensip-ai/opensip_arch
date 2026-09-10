"""Independent evaluator3 replay from incorporated contracts.

Inputs: admitted plan/views/facts/coverage/scopes/inventories/program. No caller truth.
"""
from __future__ import annotations

from typing import Any

from helpers.canonical import C, sha256_hex
from helpers.store import Store


KLEENE_NOT = {True: False, False: True, None: None}


def kleene_and(vals: list[bool | None]) -> bool | None:
    if any(v is False for v in vals):
        return False
    if all(v is True for v in vals):
        return True
    return None


def kleene_or(vals: list[bool | None]) -> bool | None:
    if any(v is True for v in vals):
        return True
    if all(v is False for v in vals):
        return False
    return None


def eval_atom(
    atom: dict[str, Any],
    *,
    subject: dict[str, Any],
    facts: list[dict[str, Any]],
    coverages: list[dict[str, Any]],
    scopes: list[dict[str, Any]],
) -> dict[str, Any]:
    """Evaluate a native atom. Three-valued. Missing relation Coverage with no match → indeterminate."""
    rel = atom["relation"]
    min_r = atom["minResolution"]
    op = atom["op"]
    sid = subject["nativeSubjectId"]
    matching = []
    for f in facts:
        if f["descriptor"]["relation"] != rel:
            continue
        # ladder index: we treat exact rung for file (only enumerated)
        if f["descriptor"]["resolution"] != min_r and rel == "file":
            continue
        payload = f.get("payload") or {}
        if rel == "file" and payload.get("path") == sid:
            matching.append(f)
        elif rel == "clones":
            # clones subject is source-path; payload has no path, join via unique anchor
            ancs = f["descriptor"].get("anchors") or []
            if any(a.get("path") == sid for a in ancs):
                matching.append(f)
    # Coverage for this relation/rung whose scope contains subject
    covering = []
    missing_cov = False
    relevant_scopes = [
        sc
        for sc in scopes
        if sc["descriptor"]["relation"] == rel
        and sc["descriptor"]["resolution"] == min_r
        and sid in sc["descriptor"]["subjects"]
        and sc["descriptor"]["sourceUniverse"] == subject["universe"]
    ]
    if not relevant_scopes:
        missing_cov = True
    for sc in relevant_scopes:
        found = False
        for c in coverages:
            if c["descriptor"]["scopeId"] == sc["id"]:
                covering.append(c)
                found = True
        if not found:
            missing_cov = True
    known = len(matching) > 0
    complete_absence = (not known) and (not missing_cov) and all(
        (c.get("payload") or {}).get("entry", {}).get("coverage") == "complete" for c in covering
    )
    value: bool | None
    if op == "exists":
        if known:
            value = True
        elif complete_absence:
            value = False
        else:
            value = None
    elif op == "none":
        if known:
            value = False
        elif complete_absence:
            value = True
        else:
            value = None
    elif op == "count-at-most":
        n = atom.get("n", 0)
        if len(matching) > n:
            value = False
        elif complete_absence or (not missing_cov and len(matching) <= n and covering):
            value = True
        else:
            value = None
    elif op == "all-covered":
        if covering and all((c.get("payload") or {}).get("entry", {}).get("coverage") == "complete" for c in covering) and not missing_cov:
            value = True
        else:
            value = None
    else:
        value = None
    return {
        "value": value,
        "matchingFactIds": [f["id"] for f in matching],
        "coverageIds": [c["id"] for c in covering],
        "missingCoverage": missing_cov,
        "threeValued": value is None,
    }


def eval_predicate(node: dict[str, Any], **kw) -> dict[str, Any]:
    if "relation" in node:
        return eval_atom(node, **kw)
    op = node["op"]
    if op == "not":
        child = eval_predicate(node["operand"], **kw)
        return {"value": KLEENE_NOT[child["value"]], "children": [child], "op": "not"}
    kids = [eval_predicate(x, **kw) for x in node["operands"]]
    vals = [k["value"] for k in kids]
    v = kleene_and(vals) if op == "and" else kleene_or(vals)
    return {"value": v, "children": kids, "op": op}


def replay_rule(
    store: Store,
    *,
    rule: dict[str, Any],
    program: dict[str, Any],
    program_digest: str,
    subjects: list[dict[str, Any]],
    facts: list[dict[str, Any]],
    coverages: list[dict[str, Any]],
    scopes: list[dict[str, Any]],
    inventories: list[dict[str, Any]],
    detector_closure: str,
    view_ids: list[str],
    import_ids: list[str],
) -> dict[str, Any]:
    rid = rule["ruleId"]
    enabled = rule.get("enabled", True)
    inv_refs = [i["digest"] for i in inventories]
    if not enabled:
        return {
            "ruleId": rid,
            "enumeration": {
                "state": "disabled",
                "inventoryRefs": [],
                "selectedSubjectIds": [],
                "unresolvedSubjectIds": [],
                "incompleteInventoryRefs": [],
            },
            "outcome": "disabled",
            "findingIds": [],
            "deficiencies": [],
            "predicateProofs": [],
            "findings": [],
        }
    selected = []
    incomplete = []
    for inv in inventories:
        rec = inv["record"]
        univ = inv.get("universe")
        if rec["state"] == "complete":
            for row in rec["rows"]:
                if row["kind"] == rule["subjectEnumeration"]["subjectKind"]:
                    rr = dict(row)
                    rr["universe"] = univ
                    selected.append(rr)
        else:
            incomplete.append(inv["digest"])
            if rec["state"] == "partial":
                for row in rec["rows"]:
                    if row["kind"] == rule["subjectEnumeration"]["subjectKind"]:
                        rr = dict(row)
                        rr["universe"] = univ
                        selected.append(rr)
    enum = {
        "state": "complete" if not incomplete else "incomplete",
        "inventoryRefs": sorted(
            [{"domain": "subject-inventory", "digest": d} for d in inv_refs],
            key=lambda r: (r["domain"] + r["digest"]).encode(),
        ),
        "selectedSubjectIds": [],
        "unresolvedSubjectIds": [],
        "incompleteInventoryRefs": sorted(incomplete),
    }
    proofs = []
    findings = []
    finding_ids = []
    for row in selected:
        # universe from subject record
        univ = row.get("universe")
        subj = {
            "schemaVersion": 3,
            "universe": univ,
            "kind": row["kind"],
            "nativeSubjectId": row["nativeSubjectId"],
        }
        subj_id = None
        for oid, obj in store.objects.items():
            if obj.get("domain") == "evaluation-subject":
                d = obj["descriptor"]
                if (
                    d.get("universe") == univ
                    and d.get("nativeSubjectId") == row["nativeSubjectId"]
                    and d.get("kind") == row["kind"]
                ):
                    subj_id = oid
                    break
        if subj_id is None:
            rec = {
                "schemaVersion": 3,
                "universe": univ,
                "kind": row["kind"],
                "nativeSubjectId": row["nativeSubjectId"],
            }
            subj_id = store.put_h("evaluation-subject", rec)
        atom_res = eval_predicate(
            rule["emitWhen"],
            subject={"nativeSubjectId": row["nativeSubjectId"], "universe": univ, "kind": row["kind"]},
            facts=facts,
            coverages=coverages,
            scopes=scopes,
        )
        value = atom_res["value"] if "matchingFactIds" in atom_res else atom_res["value"]
        pred_rec = {
            "schemaVersion": 2,
            "ruleProgramDigest": program_digest,
            "ruleId": rid,
            "predicateId": "p",
            "operation": rule["emitWhen"]["op"] if "relation" in rule["emitWhen"] else rule["emitWhen"]["op"],
            "nodeDigest": sha256_hex(C(rule["emitWhen"])),
        }
        pred_d = sha256_hex(C(pred_rec))
        store.put_blob(C(pred_rec))
        match_ids = atom_res.get("matchingFactIds") or []
        cov_ids = atom_res.get("coverageIds") or []
        witness = {
            "schemaVersion": 3,
            "programPredicateDigest": pred_d,
            "matchingFactIds": sorted(match_ids),
            "coverageIds": sorted(cov_ids),
            "countLimit": None,
            "childPredicateIds": [],
            "matchingImportRows": [],
            "uncertainFactIds": [],
            "uncertainImportRows": [],
            "deficiencies": [],
            "kind": "native-atom",
        }
        if value is None:
            witness["deficiencies"] = [
                {
                    "source": "native",
                    "cause": "missing-relation-coverage" if atom_res.get("missingCoverage") else "coverage-unknown",
                    "subjectId": subj_id,
                    "predicateId": "p",
                    "inputRefs": [],
                    "evidenceKind": None,
                    "nativeCause": None,
                    "universe": univ,
                }
            ]
        wit_d = store.put_canonical(witness)
        proofs.append(
            {
                "ruleId": rid,
                "subjectId": subj_id,
                "predicateId": "p",
                "operation": pred_rec["operation"],
                "inputRefs": [],
                "scopeIds": sorted({sc["id"] for sc in scopes if row["nativeSubjectId"] in sc["descriptor"]["subjects"]}),
                "value": {True: "true", False: "false", None: "indeterminate"}[value],
                "witnessDigest": wit_d,
            }
        )
        if value is True:
            # emit finding
            params = {
                "schemaVersion": 2,
                "messageCode": rid,
                "parameters": {
                    "ruleId": rid,
                    "subjectPath": row["path"],
                    "qualifiedName": row["qualifiedName"],
                    "subjectKind": row["kind"],
                    "subjectLanguage": row["subjectLanguage"],
                    "matchingFactCount": len(match_ids),
                    "matchingImportCount": 0,
                },
            }
            param_d = store.put_canonical(params)
            disc = sha256_hex(C([]))
            fp_desc = {
                "schemaVersion": 2,
                "ruleStableId": rid,
                "detectorSemanticsMajor": 1,
                "subjectKey": {
                    "language": row["subjectLanguage"],
                    "kind": row["kind"],
                    "logicalPath": row["path"],
                    "qualifiedName": row["qualifiedName"],
                    "discriminator": disc,
                },
                "relatedSubjectKeys": [],
            }
            fp_id = store.put_h("finding-fingerprint", fp_desc)
            evrefs = [{"domain": "fact", "digest": fid.split(":")[-1]} for fid in match_ids] + [
                {"domain": "coverage", "digest": cid.split(":")[-1] if ":" in cid else cid} for cid in cov_ids
            ]
            evrefs = sorted(evrefs, key=lambda r: C(r))
            finding = {
                "schemaVersion": 3,
                "fingerprint": fp_id,
                "ruleClosure": detector_closure,
                "subjectId": subj_id,
                "messageCode": rid,
                "parameterDigest": param_d,
                "severity": rule.get("severity", "note"),
                "evidenceRefs": evrefs,
                "ruleId": rid,
                "subject": {
                    "language": row["subjectLanguage"],
                    "kind": row["kind"],
                    "logicalPath": row["path"],
                    "qualifiedName": row["qualifiedName"],
                },
                "correspondence": {"state": "matched", "reason": None},
            }
            fid = store.put_h("finding", finding)
            findings.append({"id": fid, "descriptor": finding})
            finding_ids.append(fid)
    # advisory gate=false → pass even with findings
    if rule.get("gate") and finding_ids and rule.get("severity") in ("warning", "error"):
        outcome = "fail"
    elif any(p["value"] == "indeterminate" for p in proofs) and rule.get("gate"):
        outcome = "indeterminate"
    else:
        outcome = "pass"
    enum["selectedSubjectIds"] = sorted(
        [p["subjectId"] for p in proofs if p["subjectId"]],
    )
    return {
        "ruleId": rid,
        "enumeration": enum,
        "outcome": outcome,
        "findingIds": sorted(finding_ids),
        "deficiencies": [],
        "predicateProofs": proofs,
        "findings": findings,
        "witnesses": [],
    }


def compose_proof(
    store: Store,
    *,
    plan_id: str,
    exec_plan_id: str,
    evaluator_c: str,
    program_digest: str,
    eval_input_refs: list[dict],
    rule_results: list[dict],
    exec_inputs_digest: str,
) -> tuple[str, dict]:
    proofs = []
    finding_ids = []
    for rr in rule_results:
        proofs.extend(rr["predicateProofs"])
        finding_ids.extend(rr["findingIds"])
    # predicate proofs ordered by predicate order
    proofs = sorted(proofs, key=lambda p: f"{p['ruleId']},{p.get('subjectId')},{p['predicateId']}".encode())
    verdict = "pass"
    if any(rr["outcome"] == "fail" for rr in rule_results):
        verdict = "fail"
    elif any(rr["outcome"] == "indeterminate" for rr in rule_results):
        verdict = "indeterminate"
    results = [
        {
            "ruleId": rr["ruleId"],
            "enumeration": rr["enumeration"],
            "outcome": rr["outcome"],
            "findingIds": rr["findingIds"],
            "deficiencies": rr["deficiencies"],
        }
        for rr in rule_results
    ]
    results = sorted(results, key=lambda r: r["ruleId"].encode())
    bundle = {
        "schemaVersion": 3,
        "planId": plan_id,
        "executionPlanId": exec_plan_id,
        "evaluatorClosure": evaluator_c,
        "ruleProgramDigest": program_digest,
        "evaluationInputRefs": sorted(eval_input_refs, key=lambda r: C(r)),
        "predicateProofs": proofs,
        "findingIds": sorted(finding_ids),
        "verdict": verdict,
        "evaluationState": "evaluated",
        "ruleResults": results,
        "waivedFindingIds": [],
        "executionDeficiencies": [],
        "executionInputsDigest": exec_inputs_digest,
    }
    pid = store.put_h("proof-bundle", bundle)
    return pid, bundle
