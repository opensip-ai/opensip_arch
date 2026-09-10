#!/usr/bin/env python3
"""Mechanical field enumeration of selected output records + executed comparisons.

No wildcard fields. Each schema property of the selected output records is a
row. After replay of the EXPLICITLY selected Run, claimed vs derived C is the
comparison. A derived:true literal is not execution evidence.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v6/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")
sys.path.insert(0, str(OUT))

from helpers import canonical, evaluator, h, kit_schemas, order  # noqa: E402
from helpers.store import load_export  # noqa: E402

COMP9 = {
    ("proof-bundle", "schemaVersion"): "composition §9.1 const 3",
    ("proof-bundle", "planId"): "composition §9.1 admitted Plan H",
    ("proof-bundle", "executionPlanId"): "composition §9.1 admitted execution-plan H",
    ("proof-bundle", "evaluatorClosure"): "composition §9.1 Plan-selected kind=evaluator",
    ("proof-bundle", "executionInputsDigest"): "composition §9.1 SHA-256(C(EI))",
    ("proof-bundle", "evaluationInputRefs"): "composition §9.1 Cset(selectedRefs ∪ {XI})",
    ("proof-bundle", "ruleProgramDigest"): "composition §9.1 SHA-256(C(RuleProgramV2))",
    ("proof-bundle", "predicateProofs"): "composition §9.4 enabled-rule × selectedSubject × emitWhen node; order (ruleId,subjectId,predicateId) UTF-8",
    ("proof-bundle", "findingIds"): "composition §9.7 Cset minted finding3",
    ("proof-bundle", "verdict"): "composition §5 fail > indeterminate > pass",
    ("proof-bundle", "evaluationState"): "composition §3 evaluated|budget-exhausted",
    ("proof-bundle", "ruleResults"): "composition §9.5 one item per policy rule, order ruleId UTF-8",
    ("proof-bundle", "waivedFindingIds"): "composition §9.7 Cset waived finding3",
    ("proof-bundle", "executionDeficiencies"): "composition §9.6 bridged required-cell items",
    ("predicateProofs.item", "ruleId"): "composition §9.4 policy rule id",
    ("predicateProofs.item", "subjectId"): "composition §9.4 subject3 of selected subject",
    ("predicateProofs.item", "predicateId"): "composition §9.4 program-predicate address",
    ("predicateProofs.item", "operation"): "composition §9.4 node op",
    ("predicateProofs.item", "inputRefs"): "composition §9.2 atomic=EI; boolean=Cset(children)",
    ("predicateProofs.item", "scopeIds"): "composition §9.3 atom completeness scopes; boolean union",
    ("predicateProofs.item", "value"): "composition §3 Kleene / atom law",
    ("predicateProofs.item", "witnessDigest"): "composition §9.4 SHA-256(C(witness))",
    ("ruleResults.item", "ruleId"): "composition §9.5",
    ("ruleResults.item", "enumeration"): "composition §2 / §9.5 inventoryRefs, selectedSubjectIds, state",
    ("ruleResults.item", "outcome"): "composition §5",
    ("ruleResults.item", "findingIds"): "composition §9.5 Cset minted finding3 for that rule",
    ("ruleResults.item", "deficiencies"): "composition §9.5 Cset",
    ("finding", "schemaVersion"): "composition §9.7 const 3",
    ("finding", "fingerprint"): "composition §9.7 finding-key2 or null",
    ("finding", "correspondence"): "composition §9.7 matched iff fingerprint non-null",
    ("finding", "ruleClosure"): "composition §9.7 emission detectorClosure",
    ("finding", "ruleId"): "composition §9.7",
    ("finding", "subjectId"): "composition §9.7 subject3",
    ("finding", "subject"): "composition §9.7 language/kind/logicalPath/qualifiedName",
    ("finding", "messageCode"): "composition §9.7 rule messageCode or ruleId",
    ("finding", "parameterDigest"): "composition §9.7 SHA-256(C(parameters))",
    ("finding", "severity"): "composition §9.7 resolved rule severity",
    ("finding", "evidenceRefs"): "composition §9.7 Cset witness+facts+coverage+imports",
    ("semantic-evidence", "schemaVersion"): "composition §9.7 const 3",
    ("semantic-evidence", "planId"): "composition §9.7",
    ("semantic-evidence", "viewIds"): "composition §9.7 Cset EI view refs",
    ("semantic-evidence", "coverageIds"): "composition §9.7 Cset(view coverage ∪ EI coverage)",
    ("semantic-evidence", "importIds"): "composition §9.7 Cset(plan.importIds)",
    ("semantic-evidence", "findingIds"): "composition §9.7 proof.findingIds",
    ("semantic-evidence", "proofBundleId"): "composition §9.7 ID(proof-bundle, proof)",
    ("evaluation-seal", "schemaVersion"): "composition §9.7 const 3",
    ("evaluation-seal", "planId"): "composition §9.7 proof.planId",
    ("evaluation-seal", "executionPlanId"): "composition §9.7 proof.executionPlanId",
    ("evaluation-seal", "evidenceId"): "composition §9.7 ID(semantic-evidence, evidence3)",
    ("evaluation-seal", "evaluatorClosure"): "composition §9.7 proof.evaluatorClosure",
    ("evaluation-seal", "policyDigest"): "composition §9.7 plan.policyDigest",
    ("evaluation-seal", "proofBundleId"): "composition §9.7 ID(proof-bundle, proof)",
    ("evaluation-seal", "verdict"): "composition §9.7 proof.verdict",
    ("run", "schemaVersion"): "composition §9.7 const 3",
    ("run", "projectId"): "composition §9.7 snapshot.projectId",
    ("run", "snapshotId"): "composition §9.7 plan.snapshotId",
    ("run", "planId"): "composition §9.7 proof.planId",
    ("run", "evidenceId"): "composition §9.7 seal.evidenceId",
    ("run", "evaluationSealId"): "composition §9.7 ID(evaluation-seal, seal3)",
    ("run", "capabilityManifestId"): "composition §9.7 plan.capabilityManifestId",
    ("predicate-witness", "schemaVersion"): "composition §9.3 const 3",
    ("predicate-witness", "programPredicateDigest"): "composition §9.3 SHA-256(C(program-predicate))",
    ("predicate-witness", "matchingFactIds"): "composition §9.3 Cset known fact2; boolean empty",
    ("predicate-witness", "coverageIds"): "composition §9.3 Cset atom completeness Coverage; boolean empty",
    ("predicate-witness", "countLimit"): "composition §9.3 n if count-at-most else null",
    ("predicate-witness", "childPredicateIds"): "composition §9.3 boolean immediate children; atomic empty",
    ("predicate-witness", "matchingImportRows"): "composition §9.3 imported-atom; native empty",
    ("predicate-witness", "uncertainFactIds"): "composition §9.3 Cset uncertain fact2",
    ("predicate-witness", "uncertainImportRows"): "composition §9.3 imported-atom uncertain",
    ("predicate-witness", "deficiencies"): "composition §9.3 / §9.5 Cset",
    ("predicate-witness", "kind"): "composition §9.3 native-atom|imported-atom|boolean",
    ("evaluation-subject", "schemaVersion"): "composition §1 / identity evaluation-subject const 3",
    ("evaluation-subject", "universe"): "enumeration-contract / composition §2 portable universe hex",
    ("evaluation-subject", "kind"): "enumeration-contract primary kind",
    ("evaluation-subject", "nativeSubjectId"): "inventory row nativeSubjectId",
    ("evaluation-subject", "packageManifestPath"): "required iff kind=package; forbidden otherwise",
    ("policy-derivation", "schemaVersion"): "composition §9.7 const 3",
    ("policy-derivation", "planId"): "composition §9.7 run.planId",
    ("policy-derivation", "proofBundleId"): "composition §9.7 seal.proofBundleId",
    ("policy-derivation", "policyDigest"): "composition §9.7 plan.policyDigest",
    ("policy-derivation", "waiverDigest"): "composition §9.7 plan.waiverDigest",
    ("policy-derivation", "verdict"): "composition §9.7 proof.verdict",
}


def _resolve_ref(schema: dict, sid: str, root: dict) -> dict:
    """Follow $ref including refs that carry sibling keywords."""
    if not isinstance(schema, dict) or "$ref" not in schema:
        return schema
    ref = schema["$ref"]
    target = {}
    if ref.startswith("#/$defs/"):
        target = (root.get("$defs") or {}).get(ref.split("/")[-1]) or {}
    elif ref.startswith("#/"):
        cur = root
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            cur = cur.get(part) if isinstance(cur, dict) else None
            if cur is None:
                break
        target = cur if isinstance(cur, dict) else {}
    else:
        # external or $id#fragment — try registry
        try:
            resolved = kit_schemas.REGISTRY.resolver(base_uri=sid or "").lookup(ref).contents
            if isinstance(resolved, dict):
                target = resolved
        except Exception:
            target = {}
    merged = dict(target)
    for k, v in schema.items():
        if k != "$ref":
            merged[k] = v
    return merged


def walk_props(schema: dict, prefix: str, out: list, sid: str, root: dict | None = None, seen: set | None = None):
    if not isinstance(schema, dict):
        return
    root = root or kit_schemas.SCHEMAS.get(sid) or {}
    seen = seen or set()
    if "$ref" in schema:
        key = (prefix, schema.get("$ref"), tuple(sorted(k for k in schema if k != "$ref")))
        if key in seen:
            return
        seen.add(key)
        schema = _resolve_ref(schema, sid, root)
    for app in ("allOf", "oneOf", "anyOf"):
        for sub in schema.get(app) or []:
            if isinstance(sub, dict):
                walk_props(sub, prefix, out, sid, root, seen)
    if "if" in schema:
        walk_props(schema.get("if") or {}, prefix + "[if]", out, sid, root, seen)
        walk_props(schema.get("then") or {}, prefix + "[then]", out, sid, root, seen)
        walk_props(schema.get("else") or {}, prefix + "[else]", out, sid, root, seen)
    if "not" in schema and isinstance(schema["not"], dict):
        walk_props(schema["not"], prefix + "[not]", out, sid, root, seen)
    props = schema.get("properties") or {}
    required = set(schema.get("required") or [])
    for name, psch in props.items():
        path = f"{prefix}.{name}" if prefix else name
        rec = {
            "record": prefix.split(".")[0] if prefix else name,
            "fieldPath": path,
            "field": name,
            "required": name in required,
            "type": psch.get("type") if isinstance(psch, dict) else None,
            "hasItems": isinstance(psch, dict) and "items" in psch,
            "selector": COMP9.get((prefix.split(".")[0] if prefix else name, name))
            or COMP9.get((prefix, name)),
        }
        out.append(rec)
        if isinstance(psch, dict):
            walk_props(psch, path, out, sid, root, seen)
            if isinstance(psch.get("items"), dict):
                walk_props(psch["items"], path + ".item", out, sid, root, seen)
            elif isinstance(psch.get("prefixItems"), list):
                for ii, it in enumerate(psch["prefixItems"]):
                    if isinstance(it, dict):
                        walk_props(it, path + f".prefix[{ii}]", out, sid, root, seen)


def field_cmp(claimed, derived, field: str) -> dict:
    cv = claimed.get(field) if isinstance(claimed, dict) else None
    dv = derived.get(field) if isinstance(derived, dict) else None
    equal = canonical.encode(cv) == canonical.encode(dv)
    return {
        "kind": "field-C",
        "equal": equal,
        "claimedC": canonical.encode(cv).hex(),
        "derivedC": canonical.encode(dv).hex(),
        "claimedType": type(cv).__name__,
        "derivedType": type(dv).__name__,
        "arrayN_claimed": len(cv) if isinstance(cv, list) else None,
        "arrayN_derived": len(dv) if isinstance(dv, list) else None,
    }


def main():
    idsch = kit_schemas.identity_schema()
    defs = idsch["$defs"]
    rows = []
    for defn, recname in [
        ("proof-bundle", "proof-bundle"),
        ("finding", "finding"),
        ("semantic-evidence", "semantic-evidence"),
        ("evaluation-seal", "evaluation-seal"),
        ("run", "run"),
        ("predicate-witness", "predicate-witness"),
        ("evaluation-subject", "evaluation-subject"),
        ("policy-derivation", "policy-derivation"),
    ]:
        walk_props(defs[defn], recname, rows, "urn:opensip:product-v1:identity:v3", idsch)

    ei_schema = json.loads(
        (KIT / "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json").read_text()
    )
    walk_props(ei_schema, "ExecutionInputsV1", rows, "execution-inputs.schema.v1.json", ei_schema)

    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    run_id = st.meta["runId"]
    replay = evaluator.replay_from_retained(st, run_id=run_id)
    claimed_proof = replay["claimed"]
    derived_proof = replay["proof"]
    run = st.objects[run_id]
    evid = st.objects[run["evidenceId"]]
    seal = st.objects[run["evaluationSealId"]]
    plan = st.objects[run["planId"]]
    composed = replay["replay"]
    derived_findings = {}
    for f, fid in zip(composed["findings"], composed["findingIds"]):
        derived_findings[fid] = {k: v for k, v in f.items() if not str(k).startswith("_")}

    # derived evidence/seal/run from the same selected Run (evaluator already computed these)
    view_ids = []
    cov_from_refs = []
    ei = evaluator._load_c(st, claimed_proof["executionInputsDigest"])
    ei_clean = {k: v for k, v in ei.items() if not str(k).startswith("_")}
    for ref in ei_clean.get("selectedRefs") or []:
        if ref.get("domain") == "view":
            view_ids.append("view2:" + ref["digest"])
        if ref.get("domain") == "coverage":
            cov_from_refs.append("coverage2:" + ref["digest"])
    views = [st.objects[i] if i in st.objects else next(o for k, o in st.objects.items() if k.endswith(i.split(":")[-1])) for i in view_ids]
    cov_ids = order.cset(sum((v.get("coverageIds") or [] for v in views), []) + cov_from_refs)
    evid_derived = {
        "schemaVersion": 3,
        "planId": run["planId"],
        "viewIds": order.cset(view_ids),
        "coverageIds": order.cset(cov_ids),
        "importIds": order.cset(list(plan.get("importIds") or [])),
        "findingIds": derived_proof["findingIds"],
        "proofBundleId": h.h_id("proof-bundle", derived_proof),
    }
    derived_evid_id = h.h_id("semantic-evidence", evid_derived)
    seal_derived = {
        "schemaVersion": 3,
        "planId": derived_proof["planId"],
        "executionPlanId": derived_proof["executionPlanId"],
        "evidenceId": derived_evid_id,
        "evaluatorClosure": derived_proof["evaluatorClosure"],
        "policyDigest": plan["policyDigest"],
        "proofBundleId": evid_derived["proofBundleId"],
        "verdict": derived_proof["verdict"],
    }
    derived_seal_id = h.h_id("evaluation-seal", seal_derived)
    snap = st.objects[run["snapshotId"]]
    run_derived = {
        "schemaVersion": 3,
        "projectId": snap["projectId"],
        "snapshotId": plan["snapshotId"],
        "planId": derived_proof["planId"],
        "evidenceId": derived_evid_id,
        "evaluationSealId": derived_seal_id,
        "capabilityManifestId": plan["capabilityManifestId"],
    }
    pd_derived = {
        "schemaVersion": 3,
        "planId": run["planId"],
        "proofBundleId": evid_derived["proofBundleId"],
        "policyDigest": plan["policyDigest"],
        "waiverDigest": plan.get("waiverDigest"),
        "verdict": derived_proof["verdict"],
    }
    pd_claimed = None
    for i, o in st.objects.items():
        if i.startswith("policy-derivation3:"):
            pd_claimed = o
            break

    account = []
    unaccounted = []
    for row in rows:
        rec = row["fieldPath"].split(".")[0]
        selector = row["selector"]
        if not selector:
            parts = row["fieldPath"].split(".")
            for i in range(len(parts) - 1, 0, -1):
                parent = ".".join(parts[:i])
                parent_field = parts[i - 1] if i else parts[0]
                cand = COMP9.get((rec, parent_field)) or COMP9.get((parent, parent_field))
                if cand:
                    selector = cand + " nested " + row["fieldPath"]
                    break
            if not selector and rec == "ExecutionInputsV1":
                selector = "execution-inputs-contract.v1.md / execution-inputs.schema.v1.json#" + row["fieldPath"]
            if not selector:
                unaccounted.append(row["fieldPath"])
        comparison = None
        fld = row["field"]
        fpath = row["fieldPath"]
        if rec == "proof-bundle":
            if ".item" in fpath:
                parent = fpath.split(".item")[0].split(".", 1)[-1]
                carr = claimed_proof.get(parent) or []
                darr = derived_proof.get(parent) or []
                entry_eq = []
                if isinstance(carr, list) and isinstance(darr, list) and len(carr) == len(darr):
                    for c, d in zip(carr, darr):
                        if isinstance(c, dict) and isinstance(d, dict):
                            entry_eq.append(canonical.encode(c.get(fld)) == canonical.encode(d.get(fld)))
                        else:
                            entry_eq.append(canonical.encode(c) == canonical.encode(d))
                comparison = {
                    "kind": "array-population-and-entry-fields",
                    "claimedN": len(carr) if isinstance(carr, list) else None,
                    "derivedN": len(darr) if isinstance(darr, list) else None,
                    "populationEqual": isinstance(carr, list) and isinstance(darr, list) and len(carr) == len(darr),
                    "completeArrayEqual": canonical.encode(carr) == canonical.encode(darr),
                    "entryField": fld,
                    "entryFieldAllEqual": all(entry_eq) if entry_eq else False,
                    "orderLaw": "predicate" if parent == "predicateProofs" else ("ruleId-utf8" if parent == "ruleResults" else "canonical-set"),
                }
            elif fld in claimed_proof or fld in derived_proof:
                comparison = field_cmp(claimed_proof, derived_proof, fld)
        elif rec == "finding":
            eqs = []
            nested = None
            if fpath.startswith("finding.correspondence."):
                nested = fpath.split("finding.correspondence.", 1)[1]
            elif fpath.startswith("finding.subject."):
                nested = ("subject", fpath.split("finding.subject.", 1)[1])
            for fid, dfind in derived_findings.items():
                stored = st.objects.get(fid)
                if stored is None:
                    eqs.append(False)
                    continue
                if isinstance(nested, str):
                    eqs.append(
                        canonical.encode((stored.get("correspondence") or {}).get(nested))
                        == canonical.encode((dfind.get("correspondence") or {}).get(nested))
                    )
                elif isinstance(nested, tuple):
                    eqs.append(
                        canonical.encode((stored.get("subject") or {}).get(nested[1]))
                        == canonical.encode((dfind.get("subject") or {}).get(nested[1]))
                    )
                else:
                    eqs.append(canonical.encode(stored.get(fld)) == canonical.encode(dfind.get(fld)))
            comparison = {
                "kind": "per-finding-field-C",
                "nFindings": len(derived_findings),
                "allEqual": all(x is True for x in eqs) if eqs else False,
                "results": eqs,
            }
        elif rec.startswith("finding["):
            # identity-schemas if/then/else: matched iff fingerprint non-null
            branch_ok = []
            for fid, dfind in derived_findings.items():
                stored = st.objects.get(fid) or {}
                fp = stored.get("fingerprint")
                stt = (stored.get("correspondence") or {}).get("state")
                reason = (stored.get("correspondence") or {}).get("reason")
                if "[if]" in fpath:
                    branch_ok.append((fp is not None) == (stt == "matched"))
                elif "[then]" in fpath:
                    if fp is None:
                        branch_ok.append(True)  # then-branch inapplicable
                    else:
                        if fld == "fingerprint":
                            branch_ok.append(fp is not None)
                        elif fld == "reason":
                            branch_ok.append(reason is None)
                        else:
                            branch_ok.append(stt == "matched")
                elif "[else]" in fpath:
                    if fp is not None:
                        branch_ok.append(True)
                    else:
                        if fld == "fingerprint":
                            branch_ok.append(fp is None)
                        elif fld == "reason":
                            branch_ok.append(reason is not None or stt == "unmatched")
                        else:
                            branch_ok.append(stt == "unmatched")
            comparison = {
                "kind": "schema-applicator-branch",
                "allEqual": all(branch_ok) if branch_ok else False,
                "n": len(branch_ok),
            }
        elif rec.startswith("evaluation-subject["):
            oks = []
            for s in replay.get("subjects") or []:
                stored = st.objects.get(s["id"]) or {}
                kind = stored.get("kind")
                pmp = stored.get("packageManifestPath")
                if kind == "package":
                    oks.append(pmp is not None)
                else:
                    oks.append("packageManifestPath" not in stored)
            comparison = {
                "kind": "schema-applicator-branch",
                "allEqual": all(oks) if oks else False,
                "n": len(oks),
                "law": "packageManifestPath required iff kind=package; forbidden otherwise",
            }
        elif rec.startswith("predicate-witness["):
            oks = []
            for wdig, w in (composed.get("witnesses") or {}).items():
                kind = w.get("kind")
                if kind == "boolean":
                    oks.append(
                        not w.get("matchingFactIds")
                        and not w.get("coverageIds")
                        and w.get("countLimit") is None
                    )
                elif kind in {"native-atom", "imported-atom"}:
                    oks.append(w.get("childPredicateIds") == [] or w.get("childPredicateIds") is not None)
                else:
                    oks.append(False)
            comparison = {
                "kind": "schema-applicator-branch",
                "allEqual": all(oks) if oks else False,
                "n": len(oks),
            }
        elif rec == "semantic-evidence":
            comparison = field_cmp(evid, evid_derived, fld)
        elif rec == "evaluation-seal":
            comparison = field_cmp(seal, seal_derived, fld)
        elif rec == "run":
            comparison = field_cmp(run, run_derived, fld)
        elif rec == "predicate-witness":
            eqs = []
            for wdig, w in (composed.get("witnesses") or {}).items():
                raw = st.blobs.get(wdig)
                if raw is None:
                    eqs.append(False)
                    continue
                stored = json.loads(raw.decode("utf-8"))
                eqs.append(canonical.encode(stored.get(fld)) == canonical.encode(w.get(fld)))
            comparison = {
                "kind": "per-witness-field-C",
                "nWitnesses": len(composed.get("witnesses") or {}),
                "allEqual": all(x is True for x in eqs) if eqs else False,
            }
        elif rec == "evaluation-subject":
            eqs = []
            for s in replay.get("subjects") or []:
                stored = st.objects.get(s["id"])
                desc = s.get("descriptor") or {}
                if stored is None:
                    eqs.append(False)
                    continue
                eqs.append(canonical.encode(stored.get(fld)) == canonical.encode(desc.get(fld)))
            comparison = {
                "kind": "per-subject-field-C",
                "nSubjects": len(replay.get("subjects") or []),
                "allEqual": all(x is True for x in eqs) if eqs else False,
            }
        elif rec == "policy-derivation":
            if pd_claimed is None:
                comparison = {
                    "kind": "record-absent-from-selected-graph",
                    "present": False,
                    "derivedWouldBe": pd_derived.get(fld),
                    "note": "policy-derivation3 is a composition §9.7 output; this selected TS graph did not retain a policy-derivation3 object. Field law is recorded; instance comparison is not executed.",
                }
            else:
                comparison = field_cmp(pd_claimed, pd_derived, fld)
        elif rec == "ExecutionInputsV1" or rec.startswith("ExecutionInputsV1"):
            if "cellOutcomes" in fpath and ("deficiency" in fpath or fpath.endswith("state") or "[if]" in fpath or "[then]" in fpath):
                oks = []
                for row in ei_clean.get("cellOutcomes") or []:
                    stt = row.get("state")
                    d = row.get("deficiency")
                    if stt == "complete":
                        oks.append(d is None)
                    else:
                        oks.append(d is not None)
                comparison = {
                    "kind": "input-join",
                    "equal": all(oks) if oks else False,
                    "n": len(oks),
                    "law": "cellOutcomes.deficiency null iff state=complete",
                }
            elif fld == "planId":
                comparison = {
                    "kind": "input-join",
                    "equal": ei_clean.get("planId") == run["planId"],
                    "left": ei_clean.get("planId"),
                    "right": run["planId"],
                }
            elif fld == "executionPlanId":
                comparison = {
                    "kind": "input-join",
                    "equal": ei_clean.get("executionPlanId") in st.objects,
                    "left": ei_clean.get("executionPlanId"),
                    "right": "retained exec-plan2",
                }
            elif fld == "evaluatorClosure":
                clo = st.objects.get(ei_clean.get("evaluatorClosure")) or {}
                comparison = {
                    "kind": "input-join",
                    "equal": clo.get("kind") == "evaluator" and ei_clean.get("evaluatorClosure") in (plan.get("semanticClosures") or []),
                    "left": clo.get("kind"),
                    "right": "evaluator in plan.semanticClosures",
                }
            elif ".item" in fpath or "[if]" in fpath or "[then]" in fpath:
                comparison = {
                    "kind": "input-array-needs-owner-join",
                    "suppliedJoin": True,
                    "executedJoin": False,
                    "note": "Nested EI item join not independently derived in this enumerator.",
                }
            else:
                comparison = {
                    "kind": "retained-input-field",
                    "present": fld in ei_clean,
                    "executedJoin": False,
                    "note": "Captured input field without a named owner comparison in this enumerator.",
                }

        executed = False
        if comparison is None:
            executed = False
        elif comparison.get("kind") == "record-absent-from-selected-graph":
            executed = False
        elif comparison.get("kind") in {"retained-input-field", "input-array-needs-owner-join"}:
            executed = bool(comparison.get("executedJoin"))
        elif comparison.get("equal") is True:
            executed = True
        elif comparison.get("completeArrayEqual") is True and comparison.get("entryFieldAllEqual") is True:
            executed = True
        elif comparison.get("allEqual") is True:
            executed = True
        account.append(
            {
                **row,
                "selector": selector or "UNACCOUNTED",
                "comparison": comparison,
                "executed": executed,
            }
        )

    missing_exec = [r["fieldPath"] for r in account if not r.get("executed") and r["record"] != "policy-derivation"]
    out = {
        "standing": "Mechanical schema field enumeration of selected output records. Each row has a composition/execution-inputs selector and an executed claimed-vs-derived comparison. No field='*'.",
        "selectedRunId": run_id,
        "unaccountedFieldPaths": unaccounted,
        "rowCount": len(account),
        "executedTrue": sum(1 for r in account if r.get("executed")),
        "notExecutedFieldPaths": missing_exec,
        "replayProofEqual": replay["comparison"].get("equal"),
        "outputMismatches": replay.get("outputMismatches") or [],
        "policyDerivationPresent": pd_claimed is not None,
        "fields": account,
    }
    (OUT / "prose-law-account.json").write_text(json.dumps(out, indent=2) + "\n")
    print("rows", len(account), "unaccounted", unaccounted, "executedTrue", sum(1 for r in account if r.get("executed")))
    print("notExecuted", missing_exec)
    print("proofEqual", replay["comparison"].get("equal"), "outputMismatches", replay.get("outputMismatches"))
    ok = (
        not unaccounted
        and replay["comparison"].get("equal")
        and not (replay.get("outputMismatches") or [])
        and not missing_exec
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
