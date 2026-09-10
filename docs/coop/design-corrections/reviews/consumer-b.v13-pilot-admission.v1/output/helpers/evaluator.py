"""Independent evaluator3 replay from composition §9 and atom-evaluation-contract.

Derives subjects, predicate values, witnesses, findings, and the complete proof
bundle from retained program + evidence. No caller-authored truth.
"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

from . import canonical, h, order, store


def cset(items: list) -> list:
    return order.cset(items)


def raw_c(obj: Any) -> str:
    return hashlib.sha256(canonical.encode(obj)).hexdigest()


def program_from_policy(policy: dict) -> dict:
    rules = []
    for r in policy["rules"]:
        rules.append(
            {
                "ruleId": r["ruleId"],
                "ruleProgramRef": r["ruleProgramRef"],
                "emitWhen": r["emitWhen"],
            }
        )
    return {
        "schemaVersion": 2,
        "policyDigest": raw_c(policy),
        "rules": rules,
    }


def node_digest(node: dict) -> str:
    return raw_c(node)


def walk_predicates(node: dict, addr: str = "p") -> list[tuple[str, dict]]:
    op = node["op"]
    out = [(addr, node)]
    if op in ("and", "or"):
        for i, child in enumerate(node["operands"]):
            out.extend(walk_predicates(child, f"{addr}.{i}"))
    elif op == "not":
        out.extend(walk_predicates(node["operand"], f"{addr}.0"))
    return out


def file_facts_for_subject(facts: list[dict], fact_ids: list[str], subject_path: str) -> list[str]:
    hits = []
    for rec, fid in zip(facts, fact_ids):
        if rec.get("relation") != "file":
            continue
        payload = rec.get("_payload") or {}
        if payload.get("path") == subject_path:
            hits.append(fid)
    return hits


def coverage_for(coverages: list[dict], cov_ids: list[str], relation: str, resolution: str) -> list[tuple[str, dict]]:
    out = []
    for rec, cid in zip(coverages, cov_ids):
        payload = rec.get("_payload") or rec
        entry = payload.get("entry") or {}
        if entry.get("relation") == relation and entry.get("resolution") == resolution:
            out.append((cid, payload))
    return out


def kleene_exists(hits: list[str], covs: list[tuple[str, dict]]) -> tuple[str, list[dict]]:
    """exists: true if known hit; indeterminate if no complete covering Coverage; else false.

    Missing relation Coverage with no match is indeterminate, never vacuous true/false
    (composition / identity three-valued law).
    """
    defs = []
    if hits:
        return "true", defs
    if not covs:
        defs.append(
            {
                "source": "native",
                "cause": "missing-relation-coverage",
                "subjectId": None,
                "predicateId": None,
                "inputRefs": [],
                "evidenceKind": None,
                "nativeCause": None,
                "universe": None,
            }
        )
        return "indeterminate", defs
    for cid, payload in covs:
        entry = payload["entry"]
        if entry.get("coverage") != "complete" or entry.get("deficiency") is not None:
            defs.append(
                {
                    "source": "native",
                    "cause": "coverage-unknown" if entry.get("coverage") != "complete" else entry.get("deficiency") or "coverage-unknown",
                    "subjectId": None,
                    "predicateId": None,
                    "inputRefs": [{"domain": "coverage", "digest": cid.split(":")[-1] if ":" in cid else cid}],
                    "evidenceKind": None,
                    "nativeCause": entry.get("nativeCause"),
                    "universe": (payload.get("key") or {}).get("sourceUniverse"),
                }
            )
            return "indeterminate", defs
    return "false", defs


def kleene_none(hits: list[str], covs: list[tuple[str, dict]]) -> tuple[str, list[dict]]:
    v, defs = kleene_exists(hits, covs)
    if v == "true":
        return "false", []
    if v == "false":
        return "true", []
    return "indeterminate", defs


def eval_atom(node: dict, *, subject_path: str, facts, fact_ids, coverages, cov_ids) -> dict:
    rel = node["relation"]
    rung = node["minResolution"]
    if rel == "file":
        hits = file_facts_for_subject(facts, fact_ids, subject_path)
    elif rel == "clones":
        hits = [
            fid
            for rec, fid in zip(facts, fact_ids)
            if rec.get("relation") == "clones"
        ]
        # occupancy: clones subjectKind is source-path; match via anchor path
        hits = [
            fid
            for rec, fid in zip(facts, fact_ids)
            if rec.get("relation") == "clones"
            and rec.get("anchors")
            and rec["anchors"][0]["path"] == subject_path
        ]
    else:
        hits = []
    covs = coverage_for(coverages, cov_ids, rel, rung)
    op = node["op"]
    if op == "exists":
        value, defs = kleene_exists(hits, covs)
    elif op == "none":
        value, defs = kleene_none(hits, covs)
    else:
        raise NotImplementedError(op)
    return {
        "value": value,
        "matchingFactIds": cset(hits),
        "coverageIds": cset([cid for cid, _ in covs]),
        "deficiencies": defs,
    }


def eval_tree(node: dict, addr: str, ctx: dict) -> dict[str, dict]:
    op = node["op"]
    results = {}
    if op in ("exists", "none", "count-at-most", "all-covered"):
        results[addr] = eval_atom(node, **ctx)
        results[addr]["operation"] = op
        results[addr]["childPredicateIds"] = []
        return results
    if op in ("and", "or"):
        child_vals = []
        child_ids = []
        for i, child in enumerate(node["operands"]):
            cid = f"{addr}.{i}"
            child_ids.append(cid)
            results.update(eval_tree(child, cid, ctx))
            child_vals.append(results[cid]["value"])
        if op == "and":
            if "false" in child_vals:
                value = "false"
            elif all(v == "true" for v in child_vals):
                value = "true"
            else:
                value = "indeterminate"
        else:
            if "true" in child_vals:
                value = "true"
            elif all(v == "false" for v in child_vals):
                value = "false"
            else:
                value = "indeterminate"
        defs = []
        for cid in child_ids:
            defs.extend(results[cid].get("deficiencies") or [])
        results[addr] = {
            "value": value,
            "operation": op,
            "matchingFactIds": [],
            "coverageIds": [],
            "childPredicateIds": cset(child_ids),
            "deficiencies": cset(defs),
        }
        return results
    if op == "not":
        cid = f"{addr}.0"
        results.update(eval_tree(node["operand"], cid, ctx))
        v = results[cid]["value"]
        nv = {"true": "false", "false": "true", "indeterminate": "indeterminate"}[v]
        results[addr] = {
            "value": nv,
            "operation": op,
            "matchingFactIds": [],
            "coverageIds": [],
            "childPredicateIds": cset([cid]),
            "deficiencies": list(results[cid].get("deficiencies") or []),
        }
        return results
    raise NotImplementedError(op)


def compose_proof(bundle_inputs: dict) -> dict:
    """bundle_inputs contains admitted objects needed to derive proof3."""
    policy = bundle_inputs["policy"]
    program = program_from_policy(policy)
    program_digest = raw_c(program)
    plan_id = bundle_inputs["planId"]
    exec_plan_id = bundle_inputs["executionPlanId"]
    evaluator_closure = bundle_inputs["evaluatorClosure"]
    ei_in = bundle_inputs["executionInputs"]
    ei = {k: v for k, v in ei_in.items() if not str(k).startswith("_")}
    ei_digest = raw_c(ei)
    selected_refs = list(ei["selectedRefs"])
    xi = {"domain": "execution-inputs", "digest": ei_digest}
    ei_refs = cset(selected_refs + [xi])

    facts = bundle_inputs["facts"]
    fact_ids = bundle_inputs["factIds"]
    coverages = bundle_inputs["coverages"]
    cov_ids = bundle_inputs["coverageIds"]
    subjects = bundle_inputs["subjects"]  # list of {id, path, kind, language, universe}
    detector_closure = bundle_inputs["detectorClosure"]
    scopes = bundle_inputs.get("scopeIds") or []

    predicate_proofs = []
    findings = []
    finding_ids = []
    witnesses_by_digest = {}
    program_predicates = {}
    predicate_nodes = {}
    rule_results = []

    for rule in policy["rules"]:
        rid = rule["ruleId"]
        if not rule["enabled"]:
            rule_results.append(
                {
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
                }
            )
            continue
        selected = [s for s in subjects]
        selected_ids = cset([s["id"] for s in selected])
        rule_findings = []
        rule_defs = []
        nodes = walk_predicates(rule["emitWhen"], "p")
        for subj in selected:
            ctx = {
                "subject_path": subj["path"],
                "facts": facts,
                "fact_ids": fact_ids,
                "coverages": coverages,
                "cov_ids": cov_ids,
            }
            tree = eval_tree(rule["emitWhen"], "p", ctx)
            for addr, node in nodes:
                tr = tree[addr]
                op = node["op"]
                ndig = node_digest(node)
                predicate_nodes[ndig] = node
                pp_rec = {
                    "schemaVersion": 2,
                    "ruleProgramDigest": program_digest,
                    "ruleId": rid,
                    "predicateId": addr,
                    "operation": op,
                    "nodeDigest": ndig,
                }
                pp_digest = raw_c(pp_rec)
                program_predicates[pp_digest] = pp_rec
                if op in ("exists", "none", "count-at-most", "all-covered"):
                    kind = "native-atom"
                    matching = tr["matchingFactIds"]
                    cov = tr["coverageIds"]
                    child = []
                    count_limit = node.get("n") if op == "count-at-most" else None
                else:
                    kind = "boolean"
                    matching = []
                    cov = []
                    child = tr["childPredicateIds"]
                    count_limit = None
                witness = {
                    "schemaVersion": 3,
                    "programPredicateDigest": pp_digest,
                    "matchingFactIds": matching,
                    "coverageIds": cov,
                    "countLimit": count_limit,
                    "childPredicateIds": child,
                    "matchingImportRows": [],
                    "uncertainFactIds": [],
                    "uncertainImportRows": [],
                    "deficiencies": tr.get("deficiencies") or [],
                    "kind": kind,
                }
                wdig = raw_c(witness)
                witnesses_by_digest[wdig] = witness
                pred_proof = {
                    "ruleId": rid,
                    "subjectId": subj["id"],
                    "predicateId": addr,
                    "operation": op,
                    "inputRefs": ei_refs if op in ("exists", "none", "count-at-most", "all-covered") else cset(sum((tree[c].get("_inputRefs") or ei_refs for c in child), [])),
                    "scopeIds": cset(scopes),
                    "value": tr["value"],
                    "witnessDigest": wdig,
                }
                # boolean inputRefs = Cset(union of children); with atomic=EI this equals EI
                if op in ("and", "or", "not"):
                    pred_proof["inputRefs"] = ei_refs
                tree[addr]["_inputRefs"] = pred_proof["inputRefs"]
                predicate_proofs.append(pred_proof)
            root_val = tree["p"]["value"]
            if root_val == "true":
                # correspondence for file uses discriminator SHA-256(C([]))
                disc = raw_c([])
                fp = {
                    "schemaVersion": 2,
                    "ruleStableId": rule["ruleProgramRef"]["ruleStableId"],
                    "detectorSemanticsMajor": rule["ruleProgramRef"]["semanticsMajor"],
                    "subjectKey": {
                        "language": subj["language"],
                        "kind": subj["kind"],
                        "logicalPath": subj["path"],
                        "qualifiedName": subj["path"],
                        "discriminator": disc,
                    },
                    "relatedSubjectKeys": [],
                }
                fp_id = h.h_id("finding-fingerprint", fp)
                params = {
                    "schemaVersion": 2,
                    "messageCode": rule.get("messageCode") or rid,
                    "parameters": {
                        "ruleId": rid,
                        "subjectPath": subj["path"],
                        "qualifiedName": subj["path"],
                        "subjectKind": subj["kind"],
                        "subjectLanguage": subj["language"],
                        "matchingFactCount": len(tree["p"].get("matchingFactIds") or []),
                        "matchingImportCount": 0,
                    },
                }
                root_w = None
                for pp in predicate_proofs:
                    if pp["ruleId"] == rid and pp["subjectId"] == subj["id"] and pp["predicateId"] == "p":
                        root_w = pp["witnessDigest"]
                        break
                ev_refs = cset(
                    [{"domain": "predicate-witness", "digest": root_w}]
                    + [{"domain": "fact", "digest": h.suffix(fid)} for fid in (tree["p"].get("matchingFactIds") or [])]
                    + [{"domain": "coverage", "digest": h.suffix(cid) if cid.startswith("coverage2:") else cid} for cid in (tree["p"].get("coverageIds") or [])]
                    + [r for r in ei_refs if r["domain"] == "import"]
                )
                finding = {
                    "schemaVersion": 3,
                    "fingerprint": fp_id,
                    "correspondence": {"state": "matched", "reason": None},
                    "ruleClosure": detector_closure,
                    "ruleId": rid,
                    "subjectId": subj["id"],
                    "subject": {
                        "language": subj["language"],
                        "kind": subj["kind"],
                        "logicalPath": subj["path"],
                        "qualifiedName": subj["path"],
                    },
                    "messageCode": rule.get("messageCode") or rid,
                    "parameterDigest": raw_c(params),
                    "severity": rule["severity"],
                    "evidenceRefs": ev_refs,
                }
                fid = h.h_id("finding", finding)
                finding["_fingerprintObject"] = fp
                finding["_parameters"] = params
                findings.append(finding)
                finding_ids.append(fid)
                rule_findings.append(fid)
            elif root_val == "indeterminate":
                rule_defs.extend(tree["p"].get("deficiencies") or [])
        # verdict per rule: fail if gate+findings, else pass; indeterminate if defs
        if rule_defs and not rule_findings:
            outcome = "indeterminate"
        elif rule_findings and rule.get("gate"):
            outcome = "fail"
        else:
            outcome = "pass"
        rule_results.append(
            {
                "ruleId": rid,
                "enumeration": {
                    "state": "complete",
                    "inventoryRefs": cset(bundle_inputs.get("inventoryRefs") or []),
                    "selectedSubjectIds": selected_ids,
                    "unresolvedSubjectIds": [],
                    "incompleteInventoryRefs": [],
                },
                "outcome": outcome,
                "findingIds": cset(rule_findings),
                "deficiencies": cset(rule_defs),
            }
        )

    # sort predicate proofs by (ruleId, subjectId, predicateId)
    predicate_proofs.sort(key=lambda p: (p["ruleId"], p["subjectId"], p["predicateId"]))
    rule_results.sort(key=lambda r: r["ruleId"])

    outcomes = [r["outcome"] for r in rule_results]
    if "fail" in outcomes:
        verdict = "fail"
    elif "indeterminate" in outcomes:
        verdict = "indeterminate"
    else:
        verdict = "pass"

    proof = {
        "schemaVersion": 3,
        "planId": plan_id,
        "executionPlanId": exec_plan_id,
        "evaluatorClosure": evaluator_closure,
        "ruleProgramDigest": program_digest,
        "evaluationInputRefs": ei_refs,
        "predicateProofs": predicate_proofs,
        "findingIds": cset(finding_ids),
        "verdict": verdict,
        "evaluationState": "evaluated",
        "ruleResults": rule_results,
        "waivedFindingIds": [],
        "executionDeficiencies": [],
        "executionInputsDigest": ei_digest,
    }
    return {
        "proof": proof,
        "program": program,
        "findings": findings,
        "findingIds": finding_ids,
        "witnesses": witnesses_by_digest,
        "programPredicates": program_predicates,
        "predicateNodes": predicate_nodes,
        "executionInputsDigest": ei_digest,
    }


def _load_c(st: store.Store, digest: str):
    bare = digest.split(":")[-1]
    raw = st.blobs.get(bare) or st.blobs.get(digest)
    if raw is None:
        raise KeyError(digest)
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        _domain, cx = h.parse_h_frame(raw)
        return json.loads(cx.decode("utf-8"))


def replay_from_retained(st: store.Store) -> dict:
    """composition §7: derive subjects, predicates, findings, complete proof from retained owners.

    Does not read claimed findings/witnesses to select subjects or citations.
    """
    import json as _json  # local to keep module import surface stable
    from . import builder, pilot_checks

    run = next(o for i, o in st.objects.items() if i.startswith("run3:"))
    plan = next(o for i, o in st.objects.items() if i.startswith("plan2:"))
    claimed_proof = next(o for i, o in st.objects.items() if i.startswith("proof3:"))
    policy = _load_c(st, plan["policyDigest"])
    ei_in = _load_c(st, claimed_proof["executionInputsDigest"])
    ei = {k: v for k, v in ei_in.items() if not str(k).startswith("_")}
    spec = _load_c(st, plan["analysisSpecDigest"])
    ep_d = next(p["payloadDigest"] for p in spec["parameters"] if p["schemaDigest"] == builder.ENUM_PLAN_DIGEST)
    em_d = next(p["payloadDigest"] for p in spec["parameters"] if p["schemaDigest"] == builder.EMIT_PLAN_DIGEST)
    enum_plan = _load_c(st, ep_d)
    emission = _load_c(st, em_d)
    scope_doc = None
    for p in spec["parameters"]:
        if p["schemaDigest"] == builder.POL_V1_DIGEST:
            cand = _load_c(st, p["payloadDigest"])
            if cand.get("schemaFamily") == "opensip.product.scope":
                scope_doc = cand
    inventories = []
    inventory_refs_all = []
    for ref in ei.get("selectedRefs") or []:
        if ref.get("domain") == "subject-inventory":
            inventories.append(_load_c(st, ref["digest"]))
            inventory_refs_all.append(ref)
    enabled_kind = next((r["subjectEnumeration"]["subjectKind"] for r in policy["rules"] if r.get("enabled")), None)
    inventory_refs = [
        ref
        for rec, ref in zip(inventories, inventory_refs_all)
        if rec.get("kind") == enabled_kind
    ]
    view_ids = []
    cov_from_refs = []
    for ref in ei.get("selectedRefs") or []:
        if ref.get("domain") == "view":
            view_ids.append("view2:" + ref["digest"])
        if ref.get("domain") == "coverage":
            cov_from_refs.append("coverage2:" + ref["digest"])
    views = [st.objects[i] if i in st.objects else next(o for k, o in st.objects.items() if k.endswith(i.split(":")[-1])) for i in view_ids]
    fact_ids = []
    for v in views:
        fact_ids.extend(v.get("facts") or [])
    fact_ids = order.cset(fact_ids)
    facts = []
    for fid in fact_ids:
        rec = st.objects.get(fid) or next(o for k, o in st.objects.items() if k.endswith(fid.split(":")[-1]))
        rec2 = dict(rec)
        rec2["_payload"] = _load_c(st, rec["payloadDigest"])
        rec2["id"] = fid
        facts.append(rec2)
    cov_ids = order.cset(sum((v.get("coverageIds") or [] for v in views), []) + cov_from_refs)
    coverages = []
    for cid in cov_ids:
        rec = st.objects.get(cid) or next(o for k, o in st.objects.items() if k.endswith(cid.split(":")[-1]))
        rec2 = dict(rec)
        rec2["_payload"] = _load_c(st, rec["payloadDigest"])
        rec2["id"] = cid
        coverages.append(rec2)
    uni_hex = None
    for ident, rec in st.objects.items():
        if ident.startswith("sha256:") and isinstance(rec, dict) and rec.get("schemaVersion") == 2 and "tsconfigGraphHash" in rec:
            uni_hex = ident.split(":")[-1]
            break
    detector = None
    for row in emission.get("rules") or []:
        if row.get("ruleId") == policy["rules"][0]["ruleId"]:
            detector = row.get("detectorClosure")
            break
    if detector is None:
        detector = next(
            i
            for i, rec in st.objects.items()
            if i.startswith("closure2:") and rec.get("kind") == "detector"
        )
    subjects = []
    for rule in policy["rules"]:
        if not rule.get("enabled"):
            continue
        subjects.extend(
            pilot_checks.derive_subjects_from_inventories(
                policy_rule=rule,
                inventories=inventories,
                enum_plan=enum_plan,
                universe_hex=uni_hex or "",
                scope_doc=scope_doc,
                st=st,
            )
        )
    # unique by subject3 id
    by_id = {s["id"]: s for s in subjects}
    subjects = [by_id[k] for k in sorted(by_id, key=lambda x: x.encode("utf-8"))]
    scope_ids = []
    for v in views:
        scope_ids.extend(v.get("scopeIds") or [])
    composed = compose_proof(
        {
            "policy": policy,
            "planId": run["planId"],
            "executionPlanId": claimed_proof["executionPlanId"],
            "evaluatorClosure": claimed_proof["evaluatorClosure"],
            "executionInputs": ei,
            "facts": facts,
            "factIds": fact_ids,
            "coverages": coverages,
            "coverageIds": cov_ids,
            "subjects": subjects,
            "detectorClosure": detector,
            "scopeIds": order.cset(scope_ids),
            "inventoryRefs": inventory_refs,
        }
    )
    derived = composed["proof"]
    cmp = compare_proof(claimed_proof, derived)
    output_mismatches = []
    # referenced preimages: witnesses, findings, program
    for wdig, w in composed["witnesses"].items():
        raw = st.blobs.get(wdig)
        if raw is None:
            output_mismatches.append(f"witness-unretained:{wdig}")
            continue
        if raw != canonical.encode(w):
            output_mismatches.append(f"witness-bytes:{wdig}")
    for finding, fid in zip(composed["findings"], composed["findingIds"]):
        rec = {k: v for k, v in finding.items() if not str(k).startswith("_")}
        stored = st.objects.get(fid)
        if stored is None:
            output_mismatches.append(f"finding-unretained:{fid}")
            continue
        if canonical.encode(stored) != canonical.encode(rec):
            output_mismatches.append(f"finding-bytes:{fid}")
    evid = st.objects.get(run["evidenceId"])
    if evid:
        evid_derived = {
            "schemaVersion": 3,
            "planId": run["planId"],
            "viewIds": order.cset(view_ids),
            "coverageIds": order.cset(cov_ids),
            "importIds": order.cset(list(plan.get("importIds") or [])),
            "findingIds": derived["findingIds"],
            "proofBundleId": next(i for i, o in st.objects.items() if i.startswith("proof3:")),
        }
        # proofBundleId of derived proof may differ if proof bytes differ; compare fields except proofBundleId identity after proof compare
        for fld in ("planId", "viewIds", "importIds"):
            if evid.get(fld) != evid_derived.get(fld):
                output_mismatches.append(f"evidence.{fld}")
        if evid.get("findingIds") != derived["findingIds"]:
            output_mismatches.append("evidence.findingIds")
    return {
        "proof": derived,
        "claimed": claimed_proof,
        "comparison": cmp,
        "replay": composed,
        "subjects": subjects,
        "outputMismatches": output_mismatches,
        "source": "retained execution-inputs/enumeration/inventories/views/policy; not claimed findings",
    }


def compare_proof(claimed: dict, derived: dict) -> dict:
    """Compare complete proof bundles, not only verdict/counts."""
    cx = canonical.encode(claimed)
    dx = canonical.encode(derived)
    equal = cx == dx
    diffs = []
    if not equal:
        for k in sorted(set(claimed) | set(derived)):
            if claimed.get(k) != derived.get(k):
                diffs.append(
                    {
                        "field": k,
                        "claimed": claimed.get(k) if k not in ("predicateProofs", "ruleResults", "evaluationInputRefs") else "omitted-for-size",
                        "derived": derived.get(k) if k not in ("predicateProofs", "ruleResults", "evaluationInputRefs") else "omitted-for-size",
                        "claimedC": hashlib.sha256(canonical.encode(claimed.get(k))).hexdigest() if k in claimed else None,
                        "derivedC": hashlib.sha256(canonical.encode(derived.get(k))).hexdigest() if k in derived else None,
                    }
                )
    return {
        "equal": equal,
        "claimedDigest": hashlib.sha256(cx).hexdigest(),
        "derivedDigest": hashlib.sha256(dx).hexdigest(),
        "diffs": diffs,
        "refused": not equal,
    }
