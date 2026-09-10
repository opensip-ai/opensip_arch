#!/usr/bin/env python3
"""Review-quality self-audit of the v3 PILOT_ADMITS claim.

Kit laws only. Does not import consumer helpers as oracles.
C/H/lexical from identity-and-evidence §3 via this validator's v1 probe module.
Redirected OUT to kit-pilot-selfaudit.v4. Does not mutate earlier outputs.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from collections import defaultdict
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
walk_order = v1.walk_order


def validate_stock(instance: Any, schema_doc: dict, selector: str) -> list[dict]:
    """Stock inhabitance through the pinned local registry closure; no network."""
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    registry = Registry()
    for doc in (IDENT, NATIVE, REL, ENUM, EXEC, SINV, POL2, EMIS, COMMON):
        if isinstance(doc, dict) and "$id" in doc:
            registry = registry.with_resource(doc["$id"], Resource.from_contents(doc))
    if selector.startswith("#/$defs/"):
        name = selector.split("/")[-1]
        if name not in schema_doc.get("$defs", {}):
            return [{"path": [], "message": f"missing def {name}", "validator": "setup"}]
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": (schema_doc.get("$id") or "urn:local") + "/inline-" + name,
            "$defs": schema_doc.get("$defs", {}),
            **schema_doc["$defs"][name],
        }
        order_schema = schema_doc["$defs"][name]
        defs = schema_doc.get("$defs", {})
    else:
        schema = schema_doc
        order_schema = schema_doc
        defs = schema_doc.get("$defs", {})
    errors = []
    try:
        v = Draft202012Validator(schema, registry=registry)
        for e in v.iter_errors(instance):
            errors.append({"path": list(e.absolute_path), "message": e.message, "validator": e.validator})
    except Exception as ex:
        errors.append({"path": [], "message": str(ex), "validator": "setup"})
    for msg in walk_order(instance, order_schema, defs, path="$"):
        errors.append({"path": [], "message": msg, "validator": "x-opensip-order"})
    return errors

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-recheck.v3/consumer-snapshot")
V3_OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-recheck.v3/output")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-selfaudit.v4/output")
POS = SNAP / "runs" / "syntax-code.store.json"
TAMPER = SNAP / "runs" / "syntax-code.tamper.store.json"
MANIFEST = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-recheck.v3/snapshot-manifest.json")
REQ = KIT / "docs" / "coop"  # unused; requirements sit beside kit
REQ_JSON = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject") / ".." 
# requirements.json is beside the kit in the validator subject parent
REQ_PATH = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/requirements.json")
if not REQ_PATH.exists():
    REQ_PATH = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject/requirements.json")

FOUND = KIT / "docs/coop/design-corrections/foundation"
NATIVE_DIR = KIT / "docs/coop/design-corrections/native"
WF = KIT / "docs/coop/design-corrections/workflows"

IDENT = json.loads((FOUND / "identity-schemas.v3.json").read_text())
NATIVE = json.loads((NATIVE_DIR / "native-evidence.schemas.v2.json").read_text())
REL = json.loads((FOUND / "relation-payload-schemas.v2.json").read_text())
ENUM = json.loads((FOUND / "enumeration-plan.schema.v1.json").read_text())
EXEC = json.loads((FOUND / "execution-inputs.schema.v1.json").read_text())
SINV = json.loads((FOUND / "subject-inventory.schema.v1.json").read_text())
POL2 = json.loads((WF / "schemas/policy-document.v2.schema.json").read_text())
EMIS = json.loads((FOUND / "evaluator-emission-plan.schema.v1.json").read_text())
COMMON = json.loads((WF / "schemas/common.schema.json").read_text())

REL_BYTES = (FOUND / "relation-payload-schemas.v2.json").read_bytes()
NATIVE_BYTES = (NATIVE_DIR / "native-evidence.schemas.v2.json").read_bytes()
ENUM_BYTES = (FOUND / "enumeration-plan.schema.v1.json").read_bytes()
EMIS_BYTES = (FOUND / "evaluator-emission-plan.schema.v1.json").read_bytes()
REL_FILE_DIGEST = sha256(REL_BYTES)
NATIVE_FILE_DIGEST = sha256(NATIVE_BYTES)
ENUM_FILE_DIGEST = sha256(ENUM_BYTES)
EMIS_FILE_DIGEST = sha256(EMIS_BYTES)

RELATION_REG = REL["x-opensip-relation-registry"]["relations"]
ANCHOR_CLASSES = REL["x-opensip-relation-registry"]["anchorLaw"]["classes"]
PAYLOAD_REG = IDENT["x-opensip-payload-registry"]
CLOSURE_MEM = IDENT["x-opensip-digest-domains"]["closureMembership"]
DOMAIN_SETS = IDENT["x-opensip-digest-domains"]["domainSets"]

FORBIDDEN_SELECTED = {"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"}
FORBIDDEN_EXTRAS = {"rule-program", "policy"}
SEV_RANK = {"note": 0, "warning": 1, "error": 2}
SUBJECT_ID_RE = re.compile(r"^[a-z][a-z0-9-]*:[^\\s]{1,4096}$")
BODY_TAG = b"opensip.fact-identity.v1"
DIALECT_TABLE = {
    ".rs": "rs",
    ".d.ts": "ts-declaration",
    ".ts": "ts",
    ".tsx": "tsx",
    ".mts": "mts",
    ".cts": "cts",
    ".js": "js",
    ".jsx": "jsx",
    ".mjs": "mjs",
    ".cjs": "cjs",
}
BODY_LANG = IDENT["x-opensip-digest-domains"]["domainSets"]["native-semantic-universe"]["native.semantic-universe.syntax.v2"]["languageVersionBinding"]["bodyLanguageByVariant"]

PROBES: list[dict[str, Any]] = []
NOTREACHED: list[dict[str, Any]] = []
WITHDRAWN: list[dict[str, Any]] = []
MISSED_LAWS: list[dict[str, Any]] = []


def sort_set(xs: list) -> list:
    return sorted(xs, key=lambda x: C(x))


def hex_of(s: str) -> str:
    return s.split(":", 1)[1] if isinstance(s, str) and ":" in s else s


def record(name, ok, *, selector, operands, assertion, class_="structural", export="positive", detail=None, v3_status="missed"):
    rec = {
        "name": name,
        "ok": bool(ok),
        "selector": selector,
        "operands": operands,
        "assertion": assertion,
        "class": class_,
        "export": export,
        "detail": detail,
        "v3Status": v3_status,
    }
    PROBES.append(rec)
    return rec


def not_reached(name, *, selector, reason, export="both"):
    NOTREACHED.append({"name": name, "selector": selector, "reason": reason, "export": export})


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


def u8pref(b: bytes) -> bytes:
    return bytes([len(b)]) + b


def parse_body_frame(frame: bytes) -> dict:
    i = 0

    def take_u8() -> bytes:
        nonlocal i
        n = frame[i]
        i += 1
        b = frame[i : i + n]
        i += n
        return b

    tag = take_u8()
    level_id = take_u8()
    level_version = take_u8()
    language_id = take_u8()
    language_version = take_u8()
    plen = int.from_bytes(frame[i : i + 4], "big")
    i += 4
    payload = frame[i : i + plen]
    return {
        "tag": tag,
        "levelId": level_id.decode("ascii"),
        "levelVersion": level_version,
        "languageId": language_id.decode("ascii"),
        "languageVersion": language_version,
        "payload": payload,
        "restExact": i + plen == len(frame),
        "outerLen": plen,
    }


def longest_suffix(path: str) -> str | None:
    hits = [s for s in DIALECT_TABLE if path.endswith(s)]
    if not hits:
        return None
    return max(hits, key=len)


def coverage_payload_key(payload: dict) -> tuple:
    key = payload.get("key") or {}
    entry = payload.get("entry") or {}
    return (
        key.get("relation") or entry.get("relation"),
        key.get("resolution") or entry.get("resolution"),
        key.get("sourceUniverse"),
        key.get("targetUniverse"),
    )


def exists_or_none(op, *, facts, coverages, payloads, subject_id, relation, minr, filters):
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
        rel, res, _su, _tu = coverage_payload_key(c["payload"])
        if rel == relation and res == minr:
            covs.append(c)
    has_cov = bool(covs)
    complete = any((c["payload"].get("entry") or {}).get("coverage") == "complete" for c in covs)
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


def reconstruct_expected_proof(g: dict) -> dict:
    """Build complete proof C from selected inputs only. Must not read claimed proof fields."""
    store = g["store"]
    run = g["run"]
    plan = g["plan"]
    exec_in = g["exec"]
    view = g["view"]
    inventories = g["inventories"]
    facts = g["facts"]
    payloads = g["payloads"]
    coverages = g["coverages"]
    enum_plan = g["enum_plan"]
    policy = g["policy"]

    # rule program is the projection of Plan-selected policy (identity-and-evidence §3)
    derived_rp = {
        "schemaVersion": 2,
        "policyDigest": plan["policyDigest"],
        "rules": [
            {"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"], "emitWhen": r["emitWhen"]}
            for r in policy["rules"]
        ],
    }
    rp_digest = sha256(C(derived_rp))
    exec_digest = sha256(C(exec_in))
    execution_plan_id = exec_in["executionPlanId"]  # selected ExecutionInputs field, not claimed proof
    evaluator_closure = exec_in["evaluatorClosure"]
    view_id = g["view_id"]
    view_digest = hex_of(view_id)

    # universe from enumeration parameter (selected input), not from a claimed fact
    universe = None
    for cell in enum_plan["cells"]:
        for pb in cell.get("programBindings") or []:
            if pb.get("universe"):
                universe = pb["universe"]
                break
        if universe:
            break

    file_invs = [i for i in inventories if i["kind"] == "file" and i.get("state") == "complete"]
    subjects = []
    seen = set()
    for inv in file_invs:
        for row in inv["rows"]:
            subj_rec = {
                "schemaVersion": 3,
                "universe": universe,
                "kind": "file",
                "nativeSubjectId": row["nativeSubjectId"],
            }
            sid = "subject3:" + H("evaluation-subject", subj_rec)
            if sid not in seen:
                seen.add(sid)
                subjects.append({"id": sid, "record": subj_rec, "row": row})
    subjects.sort(key=lambda s: C(s["id"]))

    def file_scope_for(native_id: str) -> str | None:
        for sid in view.get("scopeIds") or []:
            sc = g["scopes"][sid]
            if sc.get("relation") == "file" and sc.get("resolution") == "enumerated" and native_id in (sc.get("subjects") or []):
                return sid
        return None

    pred_proofs = []
    rule_results = []
    policy_rules = {r["ruleId"]: r for r in policy["rules"]}
    last_w = None
    last_prog = None
    for rp_rule in derived_rp["rules"]:
        rule_id = rp_rule["ruleId"]
        pol_rule = policy_rules[rule_id]
        atom = rp_rule["emitWhen"]
        inventory_refs = sort_set([{"domain": "subject-inventory", "digest": sha256(C(inv))} for inv in file_invs])
        selected_ids = sort_set([s["id"] for s in subjects])
        if not pol_rule.get("enabled", True):
            rule_results.append({
                "ruleId": rule_id,
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
                "ruleProgramDigest": rp_digest,
                "ruleId": rule_id,
                "predicateId": "p",
                "operation": atom["op"],
                "nodeDigest": sha256(C(atom)),
            }
            last_prog = prog_pred
            pp_d = sha256(C(prog_pred))
            used_cov_ids = []
            for c in coverages:
                rel, res, _su, _tu = coverage_payload_key(c["payload"])
                if rel == atom["relation"] and res == atom["minResolution"]:
                    cid = c["id"] if str(c["id"]).startswith("coverage2:") else "coverage2:" + hex_of(c["id"])
                    used_cov_ids.append(cid)
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
            last_w = w
            wd = sha256(C(w))
            used_cov_refs = [{"domain": "coverage", "digest": hex_of(cid)} for cid in w["coverageIds"]]
            file_scope = file_scope_for(subj["record"]["nativeSubjectId"])
            pred_proofs.append({
                "ruleId": rule_id,
                "subjectId": subj["id"],
                "predicateId": "p",
                "operation": atom["op"],
                "inputRefs": sort_set(
                    [{"domain": "view", "digest": view_digest}, {"domain": "rule-program", "digest": rp_digest}]
                    + used_cov_refs
                ),
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
        "planId": exec_in["planId"],
        "executionPlanId": execution_plan_id,
        "evaluatorClosure": evaluator_closure,
        "ruleProgramDigest": rp_digest,
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
    evidence = {
        "schemaVersion": 3,
        "planId": exec_in["planId"],
        "viewIds": sort_set([view_id]),
        "coverageIds": sort_set(list(view.get("coverageIds") or [])),
        "importIds": sort_set(list(plan.get("importIds") or [])),
        "findingIds": [],
        "proofBundleId": "proof3:" + H("proof-bundle", proof),
    }
    seal = {
        "schemaVersion": 3,
        "planId": exec_in["planId"],
        "executionPlanId": execution_plan_id,
        "evidenceId": "evidence3:" + H("semantic-evidence", evidence),
        "evaluatorClosure": evaluator_closure,
        "policyDigest": plan["policyDigest"],
        "proofBundleId": evidence["proofBundleId"],
        "verdict": verdict,
    }
    derived_run = {
        "schemaVersion": 3,
        "projectId": run["projectId"],
        "snapshotId": plan["snapshotId"],
        "planId": exec_in["planId"],
        "evidenceId": seal["evidenceId"],
        "evaluationSealId": "seal3:" + H("evaluation-seal", seal),
        "capabilityManifestId": plan["capabilityManifestId"],
    }
    return {
        "proof": proof,
        "evidence": evidence,
        "seal": seal,
        "run": derived_run,
        "ruleProgram": derived_rp,
        "subjects": subjects,
        "atomValue": pred_proofs[0]["value"] if pred_proofs else None,
        "witness": last_w,
        "programPredicate": last_prog,
        "usedClaimedProofFields": [],
    }


def load_graph(path: Path) -> dict:
    raw = path.read_bytes()
    store = load_store(path)
    blobs = store["blobs"]
    table = store["objectTable"]
    run_ids = [k for k in table if isinstance(k, str) and k.startswith("run3:")]
    run_id = run_ids[0]
    run = parse_typed(store, run_id, "run")
    plan = parse_typed(store, run["planId"], "plan")
    snap = parse_typed(store, run["snapshotId"], "snapshot")
    evidence = parse_typed(store, run["evidenceId"], "semantic-evidence")
    seal = parse_typed(store, run["evaluationSealId"], "evaluation-seal")
    proof = parse_typed(store, evidence["proofBundleId"], "proof-bundle")
    exec_in = parse_canon(store, proof["executionInputsDigest"])
    view_id = evidence["viewIds"][0]
    view = parse_typed(store, view_id, "view")
    facts = []
    payloads = {}
    for fid in view["facts"]:
        frec = parse_typed(store, fid, "fact")
        facts.append({"id": fid, "record": frec})
        pd = frec.get("payloadDigest")
        if pd in blobs:
            payloads[fid] = admit_raw(blobs[pd])
    coverages = []
    for cid in view["coverageIds"]:
        crec = parse_typed(store, cid, "coverage")
        payload = admit_raw(blobs[crec["payloadDigest"]]) if crec.get("payloadDigest") in blobs else {}
        coverages.append({"id": cid, "record": crec, "payload": payload})
    scopes = {}
    for sid in view.get("scopeIds") or []:
        scopes[sid] = parse_typed(store, sid, "subject-scope")
    inventories = []
    inv_by_digest = {}
    for r in exec_in["selectedRefs"]:
        if r["domain"] == "subject-inventory":
            inv = parse_canon(store, r["digest"])
            inventories.append(inv)
            inv_by_digest[r["digest"]] = inv
    policy = parse_canon(store, plan["policyDigest"])
    enum_plan = parse_canon(store, exec_in["enumerationPlanDigest"])
    analysis_spec = parse_canon(store, plan["analysisSpecDigest"])
    nctx = parse_h_frame(blobs[hex_of(plan["nativeContextDigests"][0])])
    closures = {}
    for cid in plan["semanticClosures"]:
        closures[cid] = parse_typed(store, cid, "closure")
    exec_plan = parse_typed(store, exec_in["executionPlanId"], "execution-plan")
    return {
        "path": str(path),
        "sha256": sha256(raw),
        "bytes": len(raw),
        "blobCount": store["blobCount"],
        "store": store,
        "runId": run_id,
        "run": run,
        "plan": plan,
        "snap": snap,
        "evidence": evidence,
        "seal": seal,
        "proof": proof,
        "proofId": evidence["proofBundleId"],
        "evidenceId": run["evidenceId"],
        "sealId": run["evaluationSealId"],
        "exec": exec_in,
        "view": view,
        "view_id": view_id,
        "facts": facts,
        "payloads": payloads,
        "coverages": coverages,
        "scopes": scopes,
        "inventories": inventories,
        "inv_by_digest": inv_by_digest,
        "policy": policy,
        "enum_plan": enum_plan,
        "analysis_spec": analysis_spec,
        "nctx": nctx,
        "closures": closures,
        "exec_plan": exec_plan,
    }


def first_of(export: str, classes: tuple[str, ...]):
    for p in PROBES:
        if p["export"] == export and (not p["ok"]) and p["class"] in classes:
            return p
    return None


def structural_ok(export: str) -> bool:
    return first_of(export, ("schema", "structural", "frame")) is None


def admit_graph(label: str, g: dict) -> None:
    store = g["store"]
    blobs = store["blobs"]
    table = store["objectTable"]
    run, plan, snap, proof, evidence, seal, exec_in = g["run"], g["plan"], g["snap"], g["proof"], g["evidence"], g["seal"], g["exec"]
    view, facts, payloads, coverages, scopes = g["view"], g["facts"], g["payloads"], g["coverages"], g["scopes"]

    rehash_fail = [d for d, b in blobs.items() if sha256(b) != d]
    record(
        f"{label}-blob-rehash",
        not rehash_fail,
        selector="identity-and-evidence.md §3 raw blob SHA-256 of exact bytes",
        operands={"blobCount": len(blobs), "failingDigests": rehash_fail[:4]},
        assertion="every blobs[d] rehashes to d; availability of a key is not this check",
        class_="frame",
        export=label,
        v3_status="present-as-rehash",
    )
    record(
        f"{label}-blobCount",
        store["blobCount"] == len(blobs),
        selector="store.blobCount equals map cardinality",
        operands={"claimed": store["blobCount"], "len": len(blobs)},
        assertion="blobCount == len(blobs)",
        class_="structural",
        export=label,
        v3_status="present",
    )

    run_ids = [k for k in table if isinstance(k, str) and k.startswith("run3:")]
    record(
        f"{label}-one-run",
        len(run_ids) == 1,
        selector="identity-schemas.v3 run3 unique export",
        operands={"runIds": run_ids},
        assertion="exactly one run3 object",
        class_="structural",
        export=label,
        v3_status="present",
    )
    record(
        f"{label}-run-H-identity",
        ("run3:" + H("run", run)) == g["runId"],
        selector="identity-schemas.v3 run3 = H(run, descriptor)",
        operands={"typedId": g["runId"], "recomputed": "run3:" + H("run", run)},
        assertion="typedId equals H(run, C(run-record))",
        class_="frame",
        export=label,
        v3_status="present-on-positive-only",
    )
    record(
        f"{label}-proof-H-identity",
        ("proof3:" + H("proof-bundle", proof)) == g["proofId"],
        selector="identity-schemas.v3 proof3 = H(proof-bundle, descriptor)",
        operands={"typedId": g["proofId"], "recomputed": "proof3:" + H("proof-bundle", proof)},
        assertion="typedId equals H(proof-bundle, C(proof))",
        class_="frame",
        export=label,
        v3_status="present-on-positive-only",
    )
    record(
        f"{label}-evidence-H-identity",
        ("evidence3:" + H("semantic-evidence", evidence)) == g["evidenceId"],
        selector="identity-schemas.v3 evidence3 = H(semantic-evidence, descriptor)",
        operands={"typedId": g["evidenceId"], "recomputed": "evidence3:" + H("semantic-evidence", evidence)},
        assertion="typedId equals H(semantic-evidence, C(evidence))",
        class_="frame",
        export=label,
        v3_status="missed",
    )
    record(
        f"{label}-seal-H-identity",
        ("seal3:" + H("evaluation-seal", seal)) == g["sealId"],
        selector="identity-schemas.v3 seal3 = H(evaluation-seal, descriptor)",
        operands={"typedId": g["sealId"], "recomputed": "seal3:" + H("evaluation-seal", seal)},
        assertion="typedId equals H(evaluation-seal, C(seal))",
        class_="frame",
        export=label,
        v3_status="missed",
    )

    schema_targets = [
        ("run", run, IDENT, "#/$defs/run"),
        ("proof", proof, IDENT, "#/$defs/proof-bundle"),
        ("plan", plan, IDENT, "#/$defs/plan"),
        ("snapshot", snap, IDENT, "#/$defs/snapshot"),
        ("evidence", evidence, IDENT, "#/$defs/semantic-evidence"),
        ("seal", seal, IDENT, "#/$defs/evaluation-seal"),
        ("view", view, IDENT, "#/$defs/view"),
        ("exec", exec_in, EXEC, "#"),
        ("enum", g["enum_plan"], ENUM, "#"),
        ("policy", g["policy"], POL2, "#/$defs/PolicyDocumentV2"),
        ("analysis-spec", g["analysis_spec"], IDENT, "#/$defs/analysis-spec") if "analysis-spec" in IDENT.get("$defs", {}) else None,
        ("exec-plan", g["exec_plan"], IDENT, "#/$defs/execution-plan"),
    ]
    for item in schema_targets:
        if item is None:
            continue
        name, inst, doc, sel = item
        if sel.startswith("#/$defs/") and sel.split("/")[-1] not in doc.get("$defs", {}):
            continue
        errs = validate_stock(inst, doc, sel)
        record(
            f"{label}-schema-{name}",
            not errs,
            selector=f"{sel} stock JSON Schema plus x-opensip-order",
            operands={"record": name, "errorCount": len(errs)},
            assertion="stock inhabitance AND x-opensip-order; stock pass is not the complete join set",
            class_="schema",
            export=label,
            detail=errs[:4],
            v3_status="partial-identity-only",
        )

    # execution-inputs digest is C of the record, not mere blob presence
    record(
        f"{label}-executionInputsDigest-is-C",
        proof["executionInputsDigest"] == sha256(C(exec_in)) and C(exec_in) == blobs[proof["executionInputsDigest"]],
        selector="evaluator-composition-contract.v3.md §1 proof.executionInputsDigest = SHA-256(C(ExecutionInputsV1))",
        operands={"claimed": proof["executionInputsDigest"], "Csha": sha256(C(exec_in))},
        assertion="digest equals SHA-256(C(parsed ExecutionInputsV1)) and blob remainder is C",
        class_="structural",
        export=label,
        v3_status="present-digest-only",
    )
    expected_refs = sort_set(list(exec_in["selectedRefs"]) + [{"domain": "execution-inputs", "digest": proof["executionInputsDigest"]}])
    record(
        f"{label}-evaluationInputRefs-equals-selected-plus-manifest",
        proof["evaluationInputRefs"] == expected_refs,
        selector="evaluator-composition-contract.v3.md §1; execution-inputs-contract.v1.md §7",
        operands={"claimed": proof["evaluationInputRefs"], "expected": expected_refs},
        assertion="evaluationInputRefs canonical-set equals selectedRefs ∪ {execution-inputs digest}",
        class_="structural",
        export=label,
        v3_status="present",
    )
    domains = {r["domain"] for r in exec_in["selectedRefs"]}
    record(
        f"{label}-selectedRefs-forbidden-output-domains",
        not (domains & FORBIDDEN_SELECTED),
        selector="execution-inputs-contract.v1.md selectedRefs forbids proof/finding/seal/run/evidence",
        operands={"domains": sorted(domains)},
        assertion="selectedRefs domains ∩ forbidden = ∅",
        class_="structural",
        export=label,
        v3_status="present",
    )
    record(
        f"{label}-selectedRefs-no-rule-program-or-policy",
        not (domains & FORBIDDEN_EXTRAS),
        selector="composition §1 ruleProgramDigest and plan.policyDigest are their own fields, not selectedRefs",
        operands={"domains": sorted(domains)},
        assertion="rule-program and policy are not selectedRefs members",
        class_="structural",
        export=label,
        v3_status="present",
    )
    record(
        f"{label}-execution-inputs-not-in-selectedRefs",
        "execution-inputs" not in domains,
        selector="execution-inputs-contract.v1.md §7 execution-inputs is not a selectedRefs member (circular)",
        operands={"domains": sorted(domains)},
        assertion="execution-inputs ∉ selectedRefs",
        class_="structural",
        export=label,
        v3_status="missed",
    )

    # selectedRefs exact totality
    receipts = exec_in["hostCapture"]["stageReceipts"]
    view_refs = []
    cov_hexes = []
    for recpt in receipts:
        if recpt.get("state") == "complete":
            for ref in recpt.get("outputRefs") or []:
                if ref["domain"] == "view":
                    view_refs.append(ref["digest"])
                    vid = "view2:" + ref["digest"]
                    vrec = parse_typed(store, vid, "view")
                    for cid in vrec.get("coverageIds") or []:
                        cov_hexes.append(hex_of(cid))
    inv_hexes = []
    for o in exec_in["cellOutcomes"]:
        inv_hexes.extend(o.get("inventoryDigests") or [])
    import_hexes = [hex_of(x) for x in (plan.get("importIds") or [])]
    expected_selected = sort_set(
        [{"domain": "view", "digest": d} for d in view_refs]
        + [{"domain": "coverage", "digest": d} for d in cov_hexes]
        + [{"domain": "subject-inventory", "digest": d} for d in inv_hexes]
        + [{"domain": "import", "digest": d} for d in import_hexes]
    )
    # hostDerivedRefs must equal inventory/candidate/sidecar set
    hdr = sort_set(list(exec_in["hostCapture"].get("hostDerivedRefs") or []))
    inv_selected = sort_set([r for r in exec_in["selectedRefs"] if r["domain"] == "subject-inventory"])
    record(
        f"{label}-selectedRefs-exact-totality",
        sort_set(exec_in["selectedRefs"]) == expected_selected,
        selector="execution-inputs-contract.v1.md §1 selectedRefs is exact totality, not a subset",
        operands={"claimedN": len(exec_in["selectedRefs"]), "expectedN": len(expected_selected), "claimed": exec_in["selectedRefs"], "expected": expected_selected},
        assertion="selectedRefs == union(complete receipt outputRefs, captured view coverageIds, cell-outcome inventories, plan.importIds)",
        class_="structural",
        export=label,
        v3_status="missed-count-only",
        detail={"symmetricDiff": [x for x in expected_selected if x not in exec_in["selectedRefs"]] + [x for x in exec_in["selectedRefs"] if x not in expected_selected]},
    )
    record(
        f"{label}-hostDerivedRefs-equals-selected-inventories",
        hdr == inv_selected,
        selector="execution-inputs-contract.v1.md §6 hostDerivedRefs is the custody set for inventories; selectedRefs blob-domain members equal this set",
        operands={"hostDerivedRefs": hdr, "selectedInventories": inv_selected},
        assertion="hostDerivedRefs canonical-set equals selected subject-inventory refs",
        class_="structural",
        export=label,
        v3_status="missed",
    )

    # cell outcomes: exactly one inventory per kind, kinds set-equal
    cell_ok = True
    cell_detail = []
    for o in exec_in["cellOutcomes"]:
        kinds = list(o.get("kinds") or [])
        digs = list(o.get("inventoryDigests") or [])
        got_kinds = []
        for d in digs:
            inv = g["inv_by_digest"].get(d)
            if inv is None:
                cell_ok = False
                cell_detail.append({"cell": o["cellOrdinal"], "missingInv": d})
                continue
            got_kinds.append(inv["kind"])
        if sorted(got_kinds) != sorted(kinds) or len(got_kinds) != len(set(got_kinds)):
            cell_ok = False
            cell_detail.append({"cell": o["cellOrdinal"], "kinds": kinds, "got": got_kinds})
        if o.get("state") == "complete":
            for d in digs:
                inv = g["inv_by_digest"].get(d)
                if inv and inv.get("state") != "complete":
                    cell_ok = False
                    cell_detail.append({"cell": o["cellOrdinal"], "completeRowPartialInv": d})
    record(
        f"{label}-cell-inventory-kind-totality",
        cell_ok,
        selector="execution-inputs-contract.v1.md §4 inventory digests exactly one per kind, kinds set-equal to the cell",
        operands={"cells": [{"ordinal": o["cellOrdinal"], "kinds": o.get("kinds"), "inventoryDigests": o.get("inventoryDigests")} for o in exec_in["cellOutcomes"]]},
        assertion="each cell: inventory kinds == cell.kinds, unique, retained, complete when outcome complete",
        class_="structural",
        export=label,
        detail=cell_detail,
        v3_status="missed-n-equals-4-only",
    )

    # plan/run/proof/exec joins
    record(
        f"{label}-plan-snapshot-equal",
        plan["snapshotId"] == run["snapshotId"] == snap.get("schemaVersion") and plan["snapshotId"] == run["snapshotId"],
        selector="PLAN_SNAPSHOT_JOIN plan.snapshotId == run.snapshotId",
        operands={"plan": plan["snapshotId"], "run": run["snapshotId"]},
        assertion="plan.snapshotId == run.snapshotId",
        class_="structural",
        export=label,
        v3_status="present",
    )
    # fix the botched assertion above — re-record the real equality (the previous used a mixed expression)
    # The previous record used `plan == run == snap.schemaVersion` which is wrong. Correct:
    PROBES[-1]["ok"] = plan["snapshotId"] == run["snapshotId"]
    PROBES[-1]["assertion"] = "plan.snapshotId == run.snapshotId (not blob presence)"
    PROBES[-1]["operands"] = {"plan.snapshotId": plan["snapshotId"], "run.snapshotId": run["snapshotId"]}

    record(
        f"{label}-proof-planId",
        proof["planId"] == run["planId"] == exec_in["planId"] == view["planId"] == evidence["planId"] == seal["planId"] == g["exec_plan"]["planId"],
        selector="proof/exec/view/evidence/seal/execution-plan planId == run.planId",
        operands={"run": run["planId"], "proof": proof["planId"], "exec": exec_in["planId"], "view": view["planId"]},
        assertion="all planId fields equal the selected Plan",
        class_="structural",
        export=label,
        v3_status="partial-proof-only",
    )
    record(
        f"{label}-exec-analysisSpecDigest-equals-plan",
        exec_in["analysisSpecDigest"] == plan["analysisSpecDigest"] and C(g["analysis_spec"]) == blobs[plan["analysisSpecDigest"]],
        selector="execution-inputs.analysisSpecDigest equals plan.analysisSpecDigest; remainder is C",
        operands={"exec": exec_in["analysisSpecDigest"], "plan": plan["analysisSpecDigest"]},
        assertion="analysisSpecDigest shared and C-remainder",
        class_="structural",
        export=label,
        v3_status="missed",
    )
    record(
        f"{label}-exec-executionPlanId-equals-proof-and-seal",
        exec_in["executionPlanId"] == proof["executionPlanId"] == seal["executionPlanId"]
        and ("exec-plan2:" + H("execution-plan", g["exec_plan"])) == exec_in["executionPlanId"],
        selector="proof.executionPlanId and seal.executionPlanId equal ExecutionInputs.executionPlanId; H identity",
        operands={"exec": exec_in["executionPlanId"], "proof": proof["executionPlanId"], "seal": seal["executionPlanId"]},
        assertion="executionPlanId is the selected exec-plan H, not a claimed-proof free field",
        class_="structural",
        export=label,
        v3_status="missed-copied-from-claimed-proof",
    )

    # evidence/proof/seal/run graph joins — NOT typedId self-identity
    record(
        f"{label}-evidence-proofBundleId-equals-claimed-proof-H",
        evidence["proofBundleId"] == g["proofId"] == ("proof3:" + H("proof-bundle", proof)) == seal["proofBundleId"],
        selector="semantic-evidence.proofBundleId and evaluation-seal.proofBundleId equal the retained proof H",
        operands={"evidence.proofBundleId": evidence["proofBundleId"], "proofH": "proof3:" + H("proof-bundle", proof), "seal.proofBundleId": seal["proofBundleId"]},
        assertion="evidence.proofBundleId == seal.proofBundleId == H(proof-bundle, claimed proof). Object-table typedId self-identity is not this join.",
        class_="structural",
        export=label,
        v3_status="present-as-typedId-tautology",
    )
    record(
        f"{label}-run-evidence-seal-triangle",
        run["evidenceId"] == g["evidenceId"] == seal["evidenceId"] == ("evidence3:" + H("semantic-evidence", evidence))
        and run["evaluationSealId"] == g["sealId"] == ("seal3:" + H("evaluation-seal", seal)),
        selector="run.evidenceId == seal.evidenceId == H(evidence); run.evaluationSealId == H(seal)",
        operands={"run.evidenceId": run["evidenceId"], "seal.evidenceId": seal["evidenceId"], "run.evaluationSealId": run["evaluationSealId"]},
        assertion="run/seal/evidence enclosing triangle",
        class_="structural",
        export=label,
        v3_status="partial-seal-proof-evidence",
    )
    record(
        f"{label}-evidence-viewIds-equals-selected-views",
        sort_set(evidence.get("viewIds") or []) == sort_set([g["view_id"]]),
        selector="composition retained-input: authoritative evidence view set equals selected view inputs",
        operands={"evidence.viewIds": evidence.get("viewIds"), "selectedView": g["view_id"]},
        assertion="evidence.viewIds canonical-set equals captured complete-receipt views",
        class_="structural",
        export=label,
        v3_status="present-containment-only",
    )
    record(
        f"{label}-evidence-coverageIds-equals-view-union",
        sort_set(evidence.get("coverageIds") or []) == sort_set(list(view.get("coverageIds") or [])),
        selector="composition retained-input: evidence coverage set is the union of selected views' coverageIds",
        operands={"evidence.coverageIds": evidence.get("coverageIds"), "view.coverageIds": view.get("coverageIds")},
        assertion="evidence.coverageIds == view.coverageIds (union of selected views)",
        class_="structural",
        export=label,
        v3_status="missed",
    )
    record(
        f"{label}-evidence-importIds-equals-plan-importIds",
        sort_set(evidence.get("importIds") or []) == sort_set(list(plan.get("importIds") or [])),
        selector="identity-schemas.v3 semantic-evidence.importIds IMPORT_JOIN equals plan.importIds",
        operands={"evidence.importIds": evidence.get("importIds"), "plan.importIds": plan.get("importIds")},
        assertion="evidence.importIds canonical-set equals plan.importIds",
        class_="structural",
        export=label,
        v3_status="missed",
    )
    record(
        f"{label}-evidence-findingIds-equals-proof-findingIds",
        sort_set(evidence.get("findingIds") or []) == sort_set(list(proof.get("findingIds") or [])),
        selector="semantic-evidence.findingIds equals proof.findingIds",
        operands={"evidence.findingIds": evidence.get("findingIds"), "proof.findingIds": proof.get("findingIds")},
        assertion="finding id sets equal",
        class_="structural",
        export=label,
        v3_status="missed",
    )
    record(
        f"{label}-seal-policyDigest-equals-plan",
        seal["policyDigest"] == plan["policyDigest"] and C(g["policy"]) == blobs[plan["policyDigest"]],
        selector="evaluation-seal.policyDigest equals plan.policyDigest; C remainder",
        operands={"seal.policyDigest": seal["policyDigest"], "plan.policyDigest": plan["policyDigest"]},
        assertion="seal.policyDigest == plan.policyDigest == SHA-256(C(policy))",
        class_="structural",
        export=label,
        v3_status="missed-blob-presence-only",
    )
    record(
        f"{label}-seal-verdict-equals-claimed-proof",
        seal["verdict"] == proof["verdict"],
        selector="evaluation-seal.verdict equals claimed proof.verdict (claimed-graph join, not independent truth)",
        operands={"seal.verdict": seal["verdict"], "proof.verdict": proof["verdict"]},
        assertion="claimed seal.verdict == claimed proof.verdict",
        class_="structural",
        export=label,
        v3_status="present",
    )
    record(
        f"{label}-run-capabilityManifestId-equals-plan",
        run["capabilityManifestId"] == plan["capabilityManifestId"],
        selector="run.capabilityManifestId equals plan.capabilityManifestId",
        operands={"run": run["capabilityManifestId"], "plan": plan["capabilityManifestId"]},
        assertion="capabilityManifestId shared",
        class_="structural",
        export=label,
        v3_status="missed",
    )
    record(
        f"{label}-plan-scopeDigest-equals-snapshot",
        plan["scopeDigest"] == snap["scopeDigest"],
        selector="plan.scopeDigest equals snapshot.scopeDigest",
        operands={"plan": plan["scopeDigest"], "snapshot": snap["scopeDigest"]},
        assertion="scopeDigest shared",
        class_="structural",
        export=label,
        v3_status="missed",
    )
    cap_bytes_ok = plan["capabilityManifestBytesDigest"] in blobs and sha256(blobs[plan["capabilityManifestBytesDigest"]]) == plan["capabilityManifestBytesDigest"]
    record(
        f"{label}-capability-manifest-bytes-rehash",
        cap_bytes_ok,
        selector="plan.capabilityManifestBytesDigest raw-artifact rehash of retained manifest body",
        operands={"digest": plan["capabilityManifestBytesDigest"], "retained": plan["capabilityManifestBytesDigest"] in blobs},
        assertion="bytes present AND rehash; presence alone is not the join",
        class_="structural",
        export=label,
        v3_status="missed",
    )

    # closure membership
    ev_kind = g["closures"].get(proof["evaluatorClosure"], {}).get("kind")
    record(
        f"{label}-evaluatorClosure-direct-semanticClosures-kind-evaluator",
        proof["evaluatorClosure"] in plan["semanticClosures"]
        and proof["evaluatorClosure"] == exec_in["evaluatorClosure"] == seal["evaluatorClosure"]
        and ev_kind == "evaluator",
        selector="identity-schemas.v3 closureMembership.direct evaluation-seal.evaluatorClosure; equalToDirect proof-bundle.evaluatorClosure; closureKinds evaluator",
        operands={
            "proof.evaluatorClosure": proof["evaluatorClosure"],
            "exec.evaluatorClosure": exec_in["evaluatorClosure"],
            "seal.evaluatorClosure": seal["evaluatorClosure"],
            "plan.semanticClosures": plan["semanticClosures"],
            "kind": ev_kind,
        },
        assertion="proof == exec == seal evaluatorClosure ∈ plan.semanticClosures AND kind=evaluator. Membership is not blob presence.",
        class_="structural",
        export=label,
        v3_status="partial-in-set-only",
    )
    view_kind = g["closures"].get(view["producerClosure"], {}).get("kind")
    fact_prod_ok = all(f["record"]["producerClosure"] == view["producerClosure"] for f in facts)
    record(
        f"{label}-view-producerClosure-provider-and-fact-equal",
        view["producerClosure"] in plan["semanticClosures"] and view_kind == "provider" and fact_prod_ok,
        selector="closureMembership.direct view.producerClosure; equalToDirect fact.producerClosure; kind=provider",
        operands={"view.producerClosure": view["producerClosure"], "kind": view_kind, "factProducerEqual": fact_prod_ok},
        assertion="view.producerClosure ∈ semanticClosures, kind=provider, every fact.producerClosure equals it",
        class_="structural",
        export=label,
        v3_status="missed",
    )
    enum_ok = True
    enum_detail = []
    for sid, sc in scopes.items():
        cid = sc.get("enumeratorClosure")
        kind = g["closures"].get(cid, {}).get("kind")
        if cid not in plan["semanticClosures"] or kind != "provider":
            enum_ok = False
            enum_detail.append({"scope": sid, "enumeratorClosure": cid, "kind": kind})
    record(
        f"{label}-scope-enumeratorClosure-provider",
        enum_ok,
        selector="closureMembership.direct subject-scope.enumeratorClosure; kind=provider",
        operands={"scopes": [{"id": s, "enumeratorClosure": scopes[s].get("enumeratorClosure")} for s in scopes]},
        assertion="each evaluated view scope enumeratorClosure ∈ semanticClosures and kind=provider",
        class_="structural",
        export=label,
        detail=enum_detail,
        v3_status="missed",
    )
    detector_ids = [cid for cid, cl in g["closures"].items() if cl.get("kind") == "detector"]
    record(
        f"{label}-detector-closure-selected",
        bool(detector_ids) and all(d in plan["semanticClosures"] for d in detector_ids),
        selector="composition §1 emission binding detectorClosure is a selected closure of kind detector",
        operands={"detectorClosures": detector_ids},
        assertion="kind=detector closure is in plan.semanticClosures (provider/evaluator cannot stand in)",
        class_="structural",
        export=label,
        v3_status="missed",
    )

    # native context + grammar tree — selectedThroughOtherInput, not flattened requirement
    nctx = g["nctx"]
    record(
        f"{label}-native-context-domain",
        nctx["domain"] == "native.context.syntax.v2",
        selector="identity-schemas.v3 domainSets native.context.syntax.v2",
        operands={"domain": nctx["domain"], "digest": plan["nativeContextDigests"][0]},
        assertion="plan.nativeContextDigests[0] H-frame domain is native.context.syntax.v2",
        class_="structural",
        export=label,
        v3_status="present-startswith",
    )
    gb = (nctx["value"] or {}).get("grammarBundle") or {}
    grammar_id = gb.get("closureId")
    grammar_cl = None
    if grammar_id:
        grammar_cl = parse_typed(store, grammar_id, "closure")
    tree = {row["sha256"] for row in (grammar_cl or {}).get("tree") or []}
    missing_tree = []
    for gram in gb.get("grammars") or []:
        if gram.get("grammarDigest") not in tree:
            missing_tree.append(("grammarDigest", gram.get("grammarDigest")))
    if gb.get("bundleDigest") and gb["bundleDigest"] not in tree:
        missing_tree.append(("bundleDigest", gb["bundleDigest"]))
    spec_d = (gb.get("normalizer") or {}).get("specificationDigest")
    if spec_d and spec_d not in tree:
        missing_tree.append(("specificationDigest", spec_d))
    record(
        f"{label}-grammar-artifacts-in-kind-grammar-tree",
        grammar_cl is not None and grammar_cl.get("kind") == "grammar" and not missing_tree,
        selector="native-evidence.md §1.2; identity-schemas.v3 closureJoins grammarBundle.closureId kind=grammar; artifacts in closure.tree",
        operands={"closureId": grammar_id, "kind": (grammar_cl or {}).get("kind"), "treeN": len(tree), "missing": missing_tree},
        assertion="grammarBundle.closureId kind=grammar AND bundleDigest, each grammarDigest, and normalizer.specificationDigest are tree members. Blob availability outside the tree is not membership.",
        class_="structural",
        export=label,
        v3_status="present-partial-skipped-normalizer",
    )
    record(
        f"{label}-grammar-closure-not-required-flattened-into-semanticClosures",
        True,
        selector="closureMembership.selectedThroughOtherInput SyntaxGrammarBundleV1.closureId via plan.nativeContextDigests and registered context closureJoins",
        operands={"grammarClosureInSemanticClosures": grammar_id in plan["semanticClosures"], "selectedThroughNativeContext": True},
        assertion="grammar may also appear in semanticClosures; the law is nativeContext closureJoin, not a flatten-all requirement",
        class_="structural",
        export=label,
        v3_status="present-as-semanticClosures-scan",
        detail={"inSemanticClosures": grammar_id in plan["semanticClosures"]},
    )
    # universe nativeContextId join
    uhex = None
    for f in facts:
        if f["record"].get("sourceUniverse"):
            uhex = f["record"]["sourceUniverse"]
            break
    universe_ok = False
    universe_detail = {}
    if uhex and uhex in blobs:
        uframe = parse_h_frame(blobs[uhex])
        universe_detail = {"domain": uframe["domain"], "nativeContextId": (uframe["value"] or {}).get("nativeContextId")}
        want = "sha256:" + hex_of(plan["nativeContextDigests"][0])
        universe_ok = uframe["domain"] == "native.semantic-universe.syntax.v2" and uframe["value"].get("nativeContextId") == want
    record(
        f"{label}-universe-nativeContextId-join",
        universe_ok,
        selector="identity-schemas.v3 native.semantic-universe.syntax.v2 contextField nativeContextId; contextForm sha256-text",
        operands={"universe": uhex, "plan.nativeContextDigests": plan["nativeContextDigests"], **universe_detail},
        assertion="fact.sourceUniverse H-frame nativeContextId equals sha256: + plan native context digest",
        class_="structural",
        export=label,
        v3_status="missed",
    )

    # payload registry — document bytes, C remainder, selector. NOT json.loads / whole-bundle.
    for f in facts:
        rec = f["record"]
        rel = rec["relation"]
        row = RELATION_REG[rel]
        raw_pl = blobs.get(rec["payloadDigest"])
        parsed_pl = payloads.get(f["id"])
        c_rem = raw_pl is not None and parsed_pl is not None and C(parsed_pl) == raw_pl
        schema_d = rec.get("payloadSchemaDigest") == REL_FILE_DIGEST
        sel = row["selector"]
        sel_errs = validate_stock(parsed_pl, REL, sel) if parsed_pl is not None else [{"message": "missing payload"}]
        record(
            f"{label}-fact-payload-registry-{rel}-{f['id'][-8:]}",
            schema_d and c_rem and not sel_errs,
            selector="identity-schemas.v3 x-opensip-payload-registry class=relation; identity-and-evidence.md §3 payloadSchemaDigest raw SHA-256 of exact full relation-payload-schemas.v2.json; codec C; selector from relation row",
            operands={
                "fact": f["id"],
                "relation": rel,
                "payloadSchemaDigest": rec.get("payloadSchemaDigest"),
                "documentSha256": REL_FILE_DIGEST,
                "payloadDigest": rec.get("payloadDigest"),
                "Cremainder": c_rem,
                "selector": sel,
                "selectorErrors": sel_errs[:3],
            },
            assertion="payloadSchemaDigest == SHA-256(exact full document bytes) AND payloadDigest blob == C(payload) AND selector inhabitance. Blob presence, JSON.loads, or whole-bundle inhabitance is not this join.",
            class_="structural",
            export=label,
            v3_status="missed",
        )
        # resolution ladder
        ladder = row.get("ladder") or []
        record(
            f"{label}-fact-resolution-in-ladder-{rel}-{f['id'][-8:]}",
            rec.get("resolution") in ladder,
            selector="relation-payload-schemas.v2.json membershipRule: resolution ∈ that relation's ladder",
            operands={"relation": rel, "resolution": rec.get("resolution"), "ladder": ladder},
            assertion="fact.resolution is a member of the relation ladder (not a global rung vocabulary)",
            class_="structural",
            export=label,
            v3_status="missed",
        )
        if row.get("universeRule") == "same-only":
            record(
                f"{label}-fact-universeRule-same-only-{rel}-{f['id'][-8:]}",
                rec.get("sourceUniverse") == rec.get("targetUniverse"),
                selector="relation-payload-schemas.v2.json universeRule same-only",
                operands={"sourceUniverse": rec.get("sourceUniverse"), "targetUniverse": rec.get("targetUniverse")},
                assertion="sourceUniverse == targetUniverse",
                class_="structural",
                export=label,
                v3_status="missed",
            )
        # anchor cardinality
        n_anc = len(rec.get("anchors") or [])
        aclass = row["anchorLaw"]["class"]
        if aclass == "inventory":
            aok = n_anc == 0
            arule = "exactly 0"
        elif aclass == "body-identity":
            aok = n_anc == 1
            arule = "exactly 1"
        else:
            aok = n_anc >= 1
            arule = "minimum 1"
        record(
            f"{label}-fact-anchorLaw-{rel}-{f['id'][-8:]}",
            aok,
            selector="relation-payload-schemas.v2.json x-opensip-relation-registry.anchorLaw",
            operands={"relation": rel, "class": aclass, "nAnchors": n_anc, "rule": arule, "anchors": rec.get("anchors")},
            assertion=f"len(fact.anchors) {arule} for class {aclass}",
            class_="structural",
            export=label,
            v3_status="missed",
        )
        record(
            f"{label}-fact-snapshotId-{f['id'][-8:]}",
            rec.get("snapshotId") == run["snapshotId"],
            selector="REFERENCE_SOURCE_JOIN fact.snapshotId == run.snapshotId",
            operands={"fact.snapshotId": rec.get("snapshotId"), "run.snapshotId": run["snapshotId"]},
            assertion="fact.snapshotId equals Run snapshot",
            class_="structural",
            export=label,
            v3_status="missed",
        )

    # file snapshotJoins inventoried-file
    inv_by_path = {row["path"]: row for row in snap.get("sourceInventory") or []}
    for f in facts:
        rec, pl = f["record"], payloads.get(f["id"])
        if rec["relation"] != "file" or pl is None:
            continue
        row = inv_by_path.get(pl.get("path"))
        blob = blobs.get(pl.get("contentSha256")) if pl.get("contentSha256") else None
        joins = {
            "pathInInventory": row is not None,
            "digestEquals": row is not None and row["sha256"] == pl.get("contentSha256"),
            "lengthEquals": row is not None and row["bytes"] == pl.get("byteLength"),
            "blobRetained": blob is not None,
            "blobRehash": blob is not None and sha256(blob) == pl.get("contentSha256"),
            "blobLength": blob is not None and len(blob) == pl.get("byteLength"),
        }
        record(
            f"{label}-file-snapshotJoins-inventoried-file-{f['id'][-8:]}",
            all(joins.values()),
            selector="relation-payload-schemas.v2.json relations/file/snapshotJoins inventoried-file; native-evidence inventoryIsNotGrammarGated still requires snapshot joins",
            operands={"path": pl.get("path"), "contentSha256": pl.get("contentSha256"), "byteLength": pl.get("byteLength"), "inventoryRow": row, "joins": joins},
            assertion="path ∈ snapshot.sourceInventory AND contentSha256 AND byteLength AND retained bytes rehash AND length. Blob presence without digest/length/path is not the join.",
            class_="structural",
            export=label,
            v3_status="missed-in-v3-present-in-v1",
        )

    # coverage payload registry
    for c in coverages:
        crec, payload = c["record"], c["payload"]
        raw_pl = blobs.get(crec.get("payloadDigest"))
        c_rem = raw_pl is not None and C(payload) == raw_pl
        schema_d = crec.get("payloadSchemaDigest") == NATIVE_FILE_DIGEST
        payload_sv = str(payload.get("schemaVersion"))
        row = ((PAYLOAD_REG.get("classes") or {}).get("coverage") or {}).get("rows") or {}
        cov_row = row.get(payload_sv) or row.get("3")
        sel = (cov_row or {}).get("selector") or "#/$defs/CoverageResultV3"
        sel_errs = validate_stock(payload, NATIVE, sel)
        record(
            f"{label}-coverage-payload-registry-{c['id'][-8:]}",
            schema_d and c_rem and not sel_errs and payload.get("schemaVersion") == 3 and crec.get("schemaVersion") == 2,
            selector="x-opensip-payload-registry class=coverage keyedBy payload.schemaVersion=3 document native-evidence.schemas.v2.json selector #/$defs/CoverageResultV3; envelope schemaVersion 2",
            operands={
                "coverage": c["id"],
                "envelopeSchemaVersion": crec.get("schemaVersion"),
                "payloadSchemaVersion": payload.get("schemaVersion"),
                "payloadSchemaDigest": crec.get("payloadSchemaDigest"),
                "documentSha256": NATIVE_FILE_DIGEST,
                "Cremainder": c_rem,
                "selectorErrors": sel_errs[:3],
            },
            assertion="coverage wrapper schemaVersion=2, payload schemaVersion=3, payloadSchemaDigest == SHA-256(exact full native-evidence.schemas.v2.json), payloadDigest blob == C(payload), CoverageResultV3 inhabitance. Envelope field presence is not payload admission.",
            class_="structural",
            export=label,
            v3_status="missed-payloadDigest-in-blobs-only",
        )
        # coverage key vs scope
        sc = scopes.get(crec.get("scopeId"))
        key = payload.get("key") or {}
        entry = payload.get("entry") or {}
        scope_join = sc is not None and sc.get("relation") == (key.get("relation") or entry.get("relation")) and sc.get("resolution") == (key.get("resolution") or entry.get("resolution")) and sc.get("sourceUniverse") == key.get("sourceUniverse") and sc.get("targetUniverse") == key.get("targetUniverse") and sc.get("snapshotId") == run["snapshotId"]
        record(
            f"{label}-coverage-key-scope-join-{c['id'][-8:]}",
            scope_join and crec.get("scopeId") in view["scopeIds"],
            selector="coverage envelope scopeId; payload.key matches that subject-scope's relation/rung/universes; scope ∈ view.scopeIds",
            operands={"scopeId": crec.get("scopeId"), "key": key, "scope": {k: sc.get(k) for k in ("relation", "resolution", "sourceUniverse", "targetUniverse", "snapshotId")} if sc else None},
            assertion="coverage.scopeId is a view scope and payload.key matches that scope's partition coordinates",
            class_="structural",
            export=label,
            v3_status="missed",
        )

    # coverageTotalityLaw file@enumerated
    file_facts_by_path_univ = defaultdict(list)
    for f in facts:
        rec, pl = f["record"], payloads.get(f["id"]) or {}
        if rec.get("relation") == "file" and rec.get("resolution") == "enumerated":
            file_facts_by_path_univ[(pl.get("path"), rec.get("sourceUniverse"), rec.get("targetUniverse"), rec.get("snapshotId"))].append(f["id"])
    totality_fail = []
    for sid, sc in scopes.items():
        if sc.get("relation") != "file" or sc.get("resolution") != "enumerated":
            continue
        paired = None
        for c in coverages:
            if c["record"].get("scopeId") == sid:
                paired = c
                break
        if paired is None:
            continue
        if (paired["payload"].get("entry") or {}).get("coverage") != "complete":
            continue
        inv_paths = {row["path"] for row in snap.get("sourceInventory") or []}
        for subj in sc.get("subjects") or []:
            if subj not in inv_paths:
                continue
            key = (subj, sc.get("sourceUniverse"), sc.get("targetUniverse"), sc.get("snapshotId"))
            if not file_facts_by_path_univ.get(key):
                totality_fail.append({"scope": sid, "subject": subj, "matchOn": key})
    record(
        f"{label}-coverageTotalityLaw-file-enumerated",
        not totality_fail,
        selector="relation-payload-schemas.v2.json coverageTotalityLaw file@enumerated; identity-and-evidence.md §3 omission half",
        operands={"snapshotPaths": [r["path"] for r in snap.get("sourceInventory") or []], "fileFactPaths": [ (payloads.get(f["id"]) or {}).get("path") for f in facts if f["record"].get("relation") == "file"], "failures": totality_fail},
        assertion="for each complete file@enumerated scope, every inventoried subject in that scope has a same-view file@enumerated fact matching matchOn (snapshotId, relation, resolution, sourceUniverse, targetUniverse). A fact from another universe does not discharge this scope.",
        class_="structural",
        export=label,
        v3_status="missed",
    )

    # coveragePartitionLaw
    groups = defaultdict(list)
    for sid, sc in scopes.items():
        key = (sc.get("snapshotId"), sc.get("relation"), sc.get("resolution"), sc.get("sourceUniverse"), sc.get("targetUniverse"))
        groups[key].append((sid, list(sc.get("subjects") or [])))
    overlap = []
    for key, members in groups.items():
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                a = set(members[i][1])
                b = set(members[j][1])
                inter = a & b
                if inter:
                    overlap.append({"key": key, "a": members[i][0], "b": members[j][0], "subjects": sorted(inter)})
    record(
        f"{label}-coveragePartitionLaw-disjoint-subjects",
        not overlap,
        selector="relation-payload-schemas.v2.json coveragePartitionLaw partitionKey; SUBJECT_SCOPE_PARTITION_OVERLAP",
        operands={"groups": {str(k): [m[0] for m in v] for k, v in groups.items()}, "overlaps": overlap},
        assertion="within one view, scopes sharing (snapshotId, relation, resolution, sourceUniverse, targetUniverse) have pairwise disjoint subjects. Different partitions may share subjects.",
        class_="structural",
        export=label,
        v3_status="missed",
    )

    # view.schemaDigests registered documents
    registered = {REL_FILE_DIGEST, NATIVE_FILE_DIGEST}
    unreg = [d for d in (view.get("schemaDigests") or []) if d not in registered]
    record(
        f"{label}-view-schemaDigests-registered",
        not unreg,
        selector="identity-and-evidence.md §3 view.schemaDigests members are raw SHA-256 of closed payload-registry documents; SCHEMA_DOCUMENT_UNREGISTERED",
        operands={"view.schemaDigests": view.get("schemaDigests"), "registered": sorted(registered), "unregistered": unreg},
        assertion="each view.schemaDigests member is a registered document digest. The set is selected, not a derived union, and carries no payload-admission authority of its own.",
        class_="structural",
        export=label,
        v3_status="missed",
    )

    # analysis-spec parameters pin exact document bytes
    param_ok = True
    param_detail = []
    known_docs = {ENUM_FILE_DIGEST: "enumeration-plan.schema.v1.json", EMIS_FILE_DIGEST: "evaluator-emission-plan.schema.v1.json"}
    for p in g["analysis_spec"].get("parameters") or []:
        sd = p.get("schemaDigest")
        pd = p.get("payloadDigest")
        payload_retained = pd in blobs and sha256(blobs[pd]) == pd and C(admit_raw(blobs[pd])) == blobs[pd]
        if sd not in known_docs or not payload_retained:
            param_ok = False
        param_detail.append({"schemaDigest": sd, "known": known_docs.get(sd), "payloadC": payload_retained})
    record(
        f"{label}-analysis-spec-parameters-document-bytes",
        param_ok and len(g["analysis_spec"].get("parameters") or []) == 2,
        selector="composition §1 analysis-spec.parameters names exact document bytes and C(payload) bytes; exactly one EnumerationPlanV1 and one EvaluatorEmissionPlanV1",
        operands={"parameters": param_detail, "enumDoc": ENUM_FILE_DIGEST, "emisDoc": EMIS_FILE_DIGEST},
        assertion="each parameter.schemaDigest is SHA-256 of the exact full schema document; payloadDigest is C remainder",
        class_="structural",
        export=label,
        v3_status="missed",
    )

    # rule program derived from policy, not a free artifact
    derived_rp = {
        "schemaVersion": 2,
        "policyDigest": plan["policyDigest"],
        "rules": [
            {"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"], "emitWhen": r["emitWhen"]}
            for r in g["policy"]["rules"]
        ],
    }
    derived_rp_digest = sha256(C(derived_rp))
    claimed_rp = parse_canon(store, proof["ruleProgramDigest"])
    record(
        f"{label}-ruleProgram-is-policy-projection",
        derived_rp_digest == proof["ruleProgramDigest"] and claimed_rp["policyDigest"] == plan["policyDigest"] and C(claimed_rp) == blobs[proof["ruleProgramDigest"]],
        selector="identity-and-evidence.md §3 proof.ruleProgramDigest is the projection of Plan-selected policy rules; policyDigest must equal the Plan's",
        operands={"derived": derived_rp_digest, "claimed": proof["ruleProgramDigest"], "policyDigest": plan["policyDigest"]},
        assertion="C(RuleProgramV2{schemaVersion:2, policyDigest:plan.policyDigest, rules:[{ruleId, ruleProgramRef, emitWhen}] in policy order}) equals claimed digest. Copying claimed ruleProgramDigest into the expected proof is not this join.",
        class_="structural",
        export=label,
        v3_status="missed-copied-claimed-digest",
    )

    # native coverage accounts: supported-available coverageIds equals matching partitions
    acct_ok = True
    acct_detail = []
    for a in exec_in["nativeCoverageAccounts"]:
        if a.get("applicability") == "supported-available":
            matching = []
            for c in coverages:
                rel, res, su, tu = coverage_payload_key(c["payload"])
                if rel == a.get("relation") and res == a.get("resolution") and su == a.get("sourceUniverse") and tu == a.get("targetUniverse"):
                    matching.append(hex_of(c["id"]))
            if sort_set(a.get("coverageIds") or []) != sort_set(matching):
                acct_ok = False
                acct_detail.append({"account": a, "matching": matching})
            if not matching:
                acct_ok = False
                acct_detail.append({"native-work-incomplete": a})
        elif a.get("applicability") == "inapplicable-vcs":
            if a.get("coverageIds"):
                acct_ok = False
                acct_detail.append({"inapplicable-had-coverage": a})
    record(
        f"{label}-nativeCoverageAccounts-partition-equality",
        acct_ok,
        selector="execution-inputs-contract.v1.md §5 supported-available coverageIds equals every matching returned partition (not a complete subset); inapplicable-vcs none",
        operands={"accounts": exec_in["nativeCoverageAccounts"], "failures": acct_detail},
        assertion="each supported-available account.coverageIds == matching view Coverage of that (relation, rung, S, T). Empty matching is native-work-incomplete. Equality, not subset.",
        class_="structural",
        export=label,
        v3_status="missed",
    )

    # body-identity framing vs tokenization freedom
    gb_ctx = gb
    for f in facts:
        rec, pl = f["record"], payloads.get(f["id"]) or {}
        if rec.get("relation") != "clones":
            continue
        bid = pl.get("bodyIdentity")
        form_ok = isinstance(bid, str) and bid.startswith("sha256:") and len(bid) == 71
        hex_id = bid[7:] if form_ok else ""
        frame = blobs.get(hex_id) if form_ok else None
        record(
            f"{label}-clones-bodyIdentity-frame-retained-{pl.get('normalisationLevel')}-{f['id'][-8:]}",
            form_ok and frame is not None and sha256(frame) == hex_id,
            selector="identity-and-evidence.md §3 bodyIdentity is sha256: + SHA-256 of framed preimage; frame retained under that suffix; relation-payload-schemas.v2 bodyIdentityJoin",
            operands={"bodyIdentity": bid, "retained": frame is not None, "rehash": frame is not None and sha256(frame) == hex_id},
            assertion="frame bytes retained AND rehash to the suffix. Presence of some other blob is not frame custody.",
            class_="structural",
            export=label,
            v3_status="present-presence-only",
        )
        if frame is None:
            continue
        parsed = parse_body_frame(frame)
        record(
            f"{label}-clones-frame-tag-and-components-{pl.get('normalisationLevel')}-{f['id'][-8:]}",
            parsed["tag"] == BODY_TAG and parsed["restExact"] and parsed["levelId"] == pl.get("normalisationLevel") and parsed["levelVersion"] == hashlib.sha256(blobs[spec_d]).digest() if spec_d in blobs else False,
            selector="identity-and-evidence.md §3 FACT-IDENTITY components: tag, levelId, levelVersion=raw 32 of retained spec, languageId, languageVersion; L1–L3 token-stream framing parsed, not judged",
            operands={"tag": parsed["tag"].decode("ascii", "replace"), "levelId": parsed["levelId"], "payloadLevel": pl.get("normalisationLevel"), "levelVersionHex": parsed["levelVersion"].hex(), "specDigest": spec_d, "languageId": parsed["languageId"], "languageVersionLen": len(parsed["languageVersion"])},
            assertion="frame parses; levelId equals payload.normalisationLevel; levelVersion equals raw SHA-256 of retained level-spec bytes. This is framing/custody, not tokenisation judgment.",
            class_="structural",
            export=label,
            v3_status="present-tag-startswith-only",
        )
        anchors = rec.get("anchors") or []
        if len(anchors) == 1:
            anc = anchors[0]
            src = blobs.get(anc.get("blobDigest"))
            record(
                f"{label}-clones-anchor-blob-{f['id'][-8:]}",
                src is not None and sha256(src) == anc.get("blobDigest") and anc.get("path") in inv_by_path and 0 <= anc["startByte"] < anc["endByte"] <= len(src),
                selector="identity-and-evidence.md §3 clones single anchor is the body span; blobDigest is retained source bytes",
                operands={"anchor": anc, "blobLen": len(src) if src is not None else None},
                assertion="anchor blob retained, rehashes, path inventoried, span within bytes",
                class_="structural",
                export=label,
                v3_status="missed",
            )
            if pl.get("normalisationLevel") == "L0-verbatim" and src is not None:
                span = src[anc["startByte"] : anc["endByte"]]
                l0_payload = len(span).to_bytes(4, "big") + span
                variant = DIALECT_TABLE[longest_suffix(anc["path"])]
                blv = {
                    "schemaVersion": 1,
                    "languageId": BODY_LANG[variant],
                    "compilerName": gb_ctx["parserName"],
                    "compilerVersion": gb_ctx["parserVersion"],
                    "compilerBuild": gb_ctx["bundleDigest"],
                    "dialect": {"grammarVariant": variant},
                }
                lv = hashlib.sha256(C(blv)).digest()
                pre = (
                    u8pref(BODY_TAG)
                    + u8pref(b"L0-verbatim")
                    + u8pref(hashlib.sha256(blobs[spec_d]).digest())
                    + u8pref(blv["languageId"].encode("ascii"))
                    + u8pref(lv)
                    + len(l0_payload).to_bytes(4, "big")
                    + l0_payload
                )
                recomputed = "sha256:" + sha256(pre)
                record(
                    f"{label}-clones-L0-languageVersionBinding-{f['id'][-8:]}",
                    recomputed == bid and parsed["payload"] == l0_payload and parsed["languageVersion"] == lv and parsed["languageId"] == blv["languageId"],
                    selector="identity-schemas.v3 languageVersionBindingLaw; native.semantic-universe.syntax.v2 languageVersionBinding derived; identity-and-evidence.md §3 L0 payload_len == raw_byte_len+4",
                    operands={"recomputed": recomputed, "claimed": bid, "derivedBlv": blv, "frameLanguageVersion": parsed["languageVersion"].hex(), "derivedLanguageVersion": lv.hex()},
                    assertion="closure rebuilds body-language-version from native-context grammarBundle parserName/parserVersion/bundleDigest + dialect from longest anchor suffix; languageVersion is raw 32 of SHA-256(C(blv)); L0 payload is double length-prefixed span. Equality of an opaque claimed hash without this derivation is not the join.",
                    class_="structural",
                    export=label,
                    v3_status="missed-in-v3-present-in-v1",
                )
            elif pl.get("normalisationLevel") == "L1-lexical":
                # parse token-stream framing only
                pay = parsed["payload"]
                framed = False
                token_n = None
                if len(pay) >= 4:
                    token_n = int.from_bytes(pay[:4], "big")
                    framed = True  # length prefix present; we do not judge token kinds/values
                record(
                    f"{label}-clones-L1-token-stream-framing-custody-{f['id'][-8:]}",
                    framed and parsed["restExact"] and frame is not None,
                    selector="relation-payload-schemas.v2.json bodyIdentityJoin tokenStreamFraming: closure parses retained L1-L3 stream to prove custody and framing; it does not and must not judge the tokenisation itself",
                    operands={"outerLen": parsed["outerLen"], "tokenCountPrefix": token_n, "levelId": parsed["levelId"]},
                    assertion="L1 frame retained and outer/token-count prefixes parse. Tokenisation judgment is notReached.",
                    class_="structural",
                    export=label,
                    v3_status="present-as-blob-presence",
                )

    # no invented syntax-only unit
    invented = []
    for d, raw in blobs.items():
        if b"syntax-only" in raw and b"unitOrdinal" in raw:
            try:
                obj = admit_raw(raw)
            except Exception:
                continue
            if isinstance(obj, dict) and obj.get("unitKind") == "syntax-only" and obj.get("unitOrdinal") == 0:
                invented.append(d)
    record(
        f"{label}-no-invented-syntax-only-unit",
        not invented,
        selector="native-evidence.md §1.2 a file on the compiler-free path is syntax-only membership with unitOrdinal: null, not a member of an invented unit",
        operands={"inventedUnitRecords": invented},
        assertion="no retained UnitMembershipV1 with unitKind=syntax-only and unitOrdinal=0",
        class_="structural",
        export=label,
        v3_status="missed-in-v3",
    )

    # witnesses: canonical-record schemaVersion 3 without H prefix; C remainder; matching facts ⊆ view.facts
    for i, pp in enumerate(proof.get("predicateProofs") or []):
        wd = pp["witnessDigest"]
        raw_w = blobs.get(wd)
        wobj = admit_raw(raw_w) if raw_w is not None else None
        record(
            f"{label}-witness-canonical-record-{i}",
            raw_w is not None and wobj is not None and C(wobj) == raw_w and wobj.get("schemaVersion") == 3 and not wd.startswith("proof"),
            selector="composition §1 predicate-witness is canonical-record schemaVersion 3 without an H prefix",
            operands={"witnessDigest": wd, "schemaVersion": None if wobj is None else wobj.get("schemaVersion"), "Cremainder": raw_w is not None and wobj is not None and C(wobj) == raw_w},
            assertion="witness blob == C(witness) schemaVersion 3. Blob presence is not canonical remainder.",
            class_="structural",
            export=label,
            v3_status="present-in-blobs-and-C",
        )
        if wobj:
            record(
                f"{label}-witness-matchingFactIds-subset-view-{i}",
                set(wobj.get("matchingFactIds") or []).issubset(set(view["facts"])),
                selector="composition §3 atomic witnesses exact matching evidence from admitted view facts",
                operands={"matchingFactIds": wobj.get("matchingFactIds"), "view.facts": view["facts"]},
                assertion="every matchingFactId is a member of the selected view.facts",
                class_="structural",
                export=label,
                v3_status="missed",
            )
            ppd = wobj.get("programPredicateDigest")
            raw_pp = blobs.get(ppd)
            pobj = admit_raw(raw_pp) if raw_pp is not None else None
            record(
                f"{label}-programPredicate-C-{i}",
                raw_pp is not None and pobj is not None and C(pobj) == raw_pp and pobj.get("ruleProgramDigest") == proof["ruleProgramDigest"],
                selector="composition §3 program-predicate address law; ruleProgramDigest join",
                operands={"programPredicateDigest": ppd, "p.ruleProgramDigest": None if pobj is None else pobj.get("ruleProgramDigest"), "proof.ruleProgramDigest": proof["ruleProgramDigest"]},
                assertion="program-predicate retained as C remainder and cites the same ruleProgramDigest",
                class_="structural",
                export=label,
                v3_status="present-in-blobs-only",
            )
        for ref in pp.get("inputRefs") or []:
            if ref["domain"] == "view":
                ok_ref = ("view2:" + ref["digest"]) in table
            elif ref["domain"] == "rule-program":
                ok_ref = ref["digest"] in blobs and C(admit_raw(blobs[ref["digest"]])) == blobs[ref["digest"]]
            elif ref["domain"] == "coverage":
                ok_ref = ("coverage2:" + ref["digest"]) in table
            else:
                ok_ref = False
            record(
                f"{label}-pred-inputRef-{ref['domain']}-{ref['digest'][:8]}",
                ok_ref,
                selector="composition §3 all input references are direct retained roots or members of an evaluated view",
                operands={"ref": ref},
                assertion="inputRef resolves to the correct domain object/blob with C/H remainder, not merely a digest string present somewhere",
                class_="structural",
                export=label,
                v3_status="present-or-in-blobs",
            )

    # waiver retained
    record(
        f"{label}-waiverDigest-retained-C",
        plan["waiverDigest"] in blobs and C(admit_raw(blobs[plan["waiverDigest"]])) == blobs[plan["waiverDigest"]],
        selector="composition §5 consume ONLY the effective WaiverSet bytes committed by Plan",
        operands={"waiverDigest": plan["waiverDigest"]},
        assertion="plan.waiverDigest blob is C remainder",
        class_="structural",
        export=label,
        v3_status="missed",
    )

    ids = {g["runId"], g["proofId"], g["evidenceId"], g["sealId"], run["planId"], run["snapshotId"]}
    record(
        f"{label}-enclosing-ids-distinct",
        len(ids) == 6,
        selector="acyclic enclosing identities (run/proof/evidence/seal/plan/snapshot distinct)",
        operands={"ids": sorted(ids)},
        assertion="six enclosing identities are pairwise distinct. Distinctness is not the complete join.",
        class_="structural",
        export=label,
        v3_status="present",
    )

    # graph-internal claimed predicate value vs retained witness matches (admission of claimed outputs' internal consistency is still not independent replay)
    # Classified as structural-of-claimed-outputs because it joins two retained claimed records without reconstructing from selected inputs.
    for i, pp in enumerate(proof.get("predicateProofs") or []):
        wobj = parse_canon(store, pp["witnessDigest"])
        matches = list(wobj.get("matchingFactIds") or [])
        if pp["operation"] == "none":
            derived_from_witness = "false" if matches else None
        elif pp["operation"] == "exists":
            derived_from_witness = "true" if matches else None
        else:
            derived_from_witness = None
        if derived_from_witness is not None:
            record(
                f"{label}-claimed-predicate-value-agrees-with-retained-witness-matches-{i}",
                pp["value"] == derived_from_witness,
                selector="composition §3 atomic known matches: exists with known match is true, none with known match is false. Claimed predicate value must agree with the retained witness matchingFactIds.",
                operands={"claimedValue": pp["value"], "matchingFactIds": matches, "derivedFromWitnessMatches": derived_from_witness, "operation": pp["operation"]},
                assertion="if matchingFactIds nonempty then none=>false and exists=>true. A reminted proof identity with a flipped value against the same witness is not a complete claimed-output join.",
                class_="structural",
                export=label,
                v3_status="missed",
            )
        if pp["value"] == "true":
            record(
                f"{label}-claimed-emitWhen-true-has-finding3-{i}",
                bool(proof.get("findingIds")),
                selector="composition §4 for each subject with emitWhen=true emit exactly one full finding3 occurrence",
                operands={"claimedValue": pp["value"], "findingIds": proof.get("findingIds")},
                assertion="claimed true emitWhen requires a finding3 id on the proof. Empty findingIds with value true is an incomplete replacement graph.",
                class_="structural",
                export=label,
                v3_status="missed",
            )

    not_reached(
        "L1-tokenization-judgment",
        selector="identity-and-evidence.md §3 / relation-payload-schemas.v2.json bodyIdentityJoin tokenStreamFraming / fact-identity-policy.v2 L1",
        reason="L1 obligation executed here is FACT-IDENTITY frame/custody retention and outer/token-count prefix parse. Tokenisation judgment is level-spec freedom and was not executed.",
        export=label,
    )
    not_reached(
        "component-manifest-schemas.v11-stock",
        selector="docs/coop/artifacts/component-manifest-schemas.v11.json",
        reason="v11 is a prose field contract, not an executable stock JSON Schema. Stored-bytes/tree join remains the applicable check. No invented stock validator.",
        export=label,
    )


def semantic_replay(label: str, g: dict, *, require_equal: bool) -> dict:
    expected = reconstruct_expected_proof(g)
    exp, claimed = expected["proof"], g["proof"]
    record(
        f"{label}-expected-proof-did-not-read-claimed-proof-fields",
        expected["usedClaimedProofFields"] == [],
        selector="composition §7 may not read claimed findings/witnesses to select subjects, parameters, citations or output IDs; executionPlanId/ruleProgramDigest/scopeIds derived from selected inputs",
        operands={"usedClaimedProofFields": expected["usedClaimedProofFields"], "derived.executionPlanId": exp["executionPlanId"], "claimed.executionPlanId": claimed["executionPlanId"], "derived.ruleProgramDigest": exp["ruleProgramDigest"], "claimed.ruleProgramDigest": claimed["ruleProgramDigest"]},
        assertion="reconstruction inputs are plan, execution-inputs, enumeration, policy, view/facts/coverage/inventories. Claimed proof fields are comparison operands only.",
        class_="semantic",
        export=label,
        v3_status="v3-read-claimed-executionPlanId-ruleProgramDigest-scopeIds",
    )
    record(
        f"{label}-derived-executionPlanId-from-exec",
        exp["executionPlanId"] == g["exec"]["executionPlanId"],
        selector="proof.executionPlanId derived from ExecutionInputsV1.executionPlanId",
        operands={"derived": exp["executionPlanId"], "exec": g["exec"]["executionPlanId"], "claimed": claimed["executionPlanId"]},
        assertion="derived executionPlanId equals selected exec field (claimed compared separately)",
        class_="semantic",
        export=label,
        v3_status="v3-copied-claimed",
    )
    record(
        f"{label}-derived-ruleProgramDigest-from-policy",
        exp["ruleProgramDigest"] == sha256(C(expected["ruleProgram"])),
        selector="identity-and-evidence.md §3 rule program is the policy projection",
        operands={"derived": exp["ruleProgramDigest"]},
        assertion="derived digest is SHA-256(C(policy projection))",
        class_="semantic",
        export=label,
        v3_status="v3-copied-claimed",
    )
    record(
        f"{label}-eval-input-refs-independent",
        exp["evaluationInputRefs"] == claimed["evaluationInputRefs"],
        selector="composition §1 independently derived evaluationInputRefs",
        operands={"derived": exp["evaluationInputRefs"], "claimed": claimed["evaluationInputRefs"]},
        assertion="derived evaluationInputRefs equals claimed (comparison after independent construction)",
        class_="semantic",
        export=label,
        v3_status="present",
    )
    record(
        f"{label}-atom-from-selected-facts-and-complete-coverage",
        expected["atomValue"] == ("false" if require_equal else expected["atomValue"]),
        selector="identity-and-evidence.md §4 / atom-evaluation-contract.v1.md none with known match is false; none with complete Coverage and no match is true",
        operands={"derivedAtom": expected["atomValue"], "claimedAtom": claimed["predicateProofs"][0]["value"], "matchingFactsFromView": [f["id"] for f in g["facts"] if f["record"]["relation"] == "file"]},
        assertion="atom evaluated over selected view facts + covering Coverage, not over claimed predicate value",
        class_="semantic",
        export=label,
        v3_status="present-compared-to-claimed",
        detail={"require_equal": require_equal},
    )
    ceq = C(exp) == C(claimed)
    record(
        f"{label}-complete-proof-C",
        ceq if require_equal else (not ceq),
        selector="evaluator-composition-contract.v3.md §7 compare C of the COMPLETE recomputed proof. Counts, selected predicate fields, final verdict, or existence of a recomputed digest alone are insufficient. Equality to a consumer claim cannot prove a shared derivation valid unless the expected proof itself was built from selected inputs under these laws.",
        operands={
            "expectedProofId": "proof3:" + H("proof-bundle", exp),
            "claimedProofId": g["proofId"],
            "expectedC": sha256(C(exp)),
            "claimedC": sha256(C(claimed)),
            "Cequal": ceq,
            "derivedVerdict": exp["verdict"],
            "claimedVerdict": claimed["verdict"],
            "derivedAtom": expected["atomValue"],
            "claimedAtom": claimed["predicateProofs"][0]["value"],
        },
        assertion=("complete C equal" if require_equal else "complete C unequal after structural admission") + "; field-wise verdict/atom/count is not a substitute",
        class_="semantic",
        export=label,
        v3_status="present-but-expected-used-claimed-fields",
    )
    if require_equal:
        record(
            f"{label}-complete-evidence-C",
            C(expected["evidence"]) == C(g["evidence"]),
            selector="composition §7 every referenced output preimage; evidence reconstructed from selected views/coverage/imports and derived proof H",
            operands={"expectedEvidenceId": "evidence3:" + H("semantic-evidence", expected["evidence"]), "claimedEvidenceId": g["evidenceId"], "Cequal": C(expected["evidence"]) == C(g["evidence"])},
            assertion="C(derived evidence) equals claimed evidence",
            class_="semantic",
            export=label,
            v3_status="missed",
        )
        record(
            f"{label}-complete-seal-C",
            C(expected["seal"]) == C(g["seal"]),
            selector="composition §7 independently reconstructs semantic evidence, seal and Run",
            operands={"expectedSealId": "seal3:" + H("evaluation-seal", expected["seal"]), "claimedSealId": g["sealId"], "Cequal": C(expected["seal"]) == C(g["seal"])},
            assertion="C(derived seal) equals claimed seal",
            class_="semantic",
            export=label,
            v3_status="missed",
        )
        record(
            f"{label}-complete-run-C",
            C(expected["run"]) == C(g["run"]),
            selector="composition §7 independently reconstructs Run",
            operands={"expectedRunId": "run3:" + H("run", expected["run"]), "claimedRunId": g["runId"], "Cequal": C(expected["run"]) == C(g["run"])},
            assertion="C(derived run) equals claimed run",
            class_="semantic",
            export=label,
            v3_status="missed",
        )
        record(
            f"{label}-witness-C",
            C(expected["witness"]) == C(parse_canon(g["store"], claimed["predicateProofs"][0]["witnessDigest"])),
            selector="composition §3 independently constructed native-atom witness C",
            operands={"expectedWitnessDigest": sha256(C(expected["witness"])), "claimedWitnessDigest": claimed["predicateProofs"][0]["witnessDigest"]},
            assertion="C(derived witness) equals claimed witness",
            class_="semantic",
            export=label,
            v3_status="present-matching-facts-set-only",
        )
    return expected


def custody_checks():
    man = json.loads(MANIFEST.read_text())
    # snapshot-manifest.json structure: files list with sha256
    files = man.get("files") or man.get("entries") or []
    if isinstance(man.get("files"), dict):
        items = list(man["files"].items())
        fail = []
        for rel, meta in items:
            p = SNAP / rel
            if not p.exists():
                fail.append(("missing", rel))
                continue
            want = meta if isinstance(meta, str) else meta.get("sha256")
            got = sha256(p.read_bytes())
            if got != want:
                fail.append(("mismatch", rel, want, got))
        record(
            "custody-snapshot-files",
            not fail and len(items) == 264,
            selector="continuation-inputs existingSnapshotManifest; snapshot bytes not reminted",
            operands={"fileCount": len(items), "expected": 264, "failures": fail[:6], "manifestSha256": sha256(MANIFEST.read_bytes())},
            assertion="every listed snapshot file rehashes to the manifest; 264/264",
            class_="custody",
            export="standing",
            v3_status="present",
        )
    elif isinstance(files, list) and files:
        fail = []
        for ent in files:
            rel = ent.get("path") or ent.get("file")
            p = SNAP / rel
            if not p.exists():
                fail.append(("missing", rel))
                continue
            got = sha256(p.read_bytes())
            if got != ent.get("sha256"):
                fail.append(("mismatch", rel))
        record(
            "custody-snapshot-files",
            not fail and len(files) == 264,
            selector="continuation-inputs existingSnapshotManifest; snapshot bytes not reminted",
            operands={"fileCount": len(files), "failures": fail[:6], "manifestSha256": sha256(MANIFEST.read_bytes())},
            assertion="264/264 snapshot files match manifest",
            class_="custody",
            export="standing",
            v3_status="present",
        )
    v3_md = V3_OUT / "pilot-review.md"
    v3_json = V3_OUT / "pilot-review.json"
    record(
        "custody-v3-report-preserved",
        v3_md.exists() and v3_json.exists() and json.loads(v3_json.read_text()).get("outcome") == "PILOT_ADMITS",
        selector="self-audit preserves earlier report bytes; does not edit v3 output",
        operands={"v3md": sha256(v3_md.read_bytes()), "v3json": sha256(v3_json.read_bytes())},
        assertion="v3 pilot-review.md/json still present with outcome PILOT_ADMITS",
        class_="custody",
        export="standing",
        v3_status="n/a",
    )
    frozen = {
        "ts.store.json": "885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d",
        "rust.store.json": "67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315",
        "syntax-data.store.json": "1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092",
        "rust-partial-clones.store.json": "b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246",
    }
    fz_fail = []
    for name, want in frozen.items():
        p = SNAP / "runs" / name
        got = sha256(p.read_bytes())
        if got != want:
            fz_fail.append({"name": name, "got": got, "want": want})
    record(
        "custody-frozen-other-runs",
        not fz_fail,
        selector="other four Run stores out of scoped recheck; hashes verified unchanged",
        operands={"frozen": frozen, "failures": fz_fail},
        assertion="ts/rust/syntax-data/rust-partial-clones stores unchanged",
        class_="custody",
        export="standing",
        v3_status="present",
    )
    preserved = {
        "original": "8b0f6d826ed04f604ce8614e63b55e9666a9abdd48702f6b155c92c4ce54e654",
        "structuralRefused": "2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7",
        "evaluationInputRefsRefused": "0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36",
    }
    pr_map = {
        "original": SNAP / "preserved-failures/syntax-code-original/runs/syntax-code.store.json",
        "structuralRefused": SNAP / "preserved-failures/syntax-code-structural-refused/runs/syntax-code.store.json",
        "evaluationInputRefsRefused": SNAP / "preserved-failures/syntax-code-evaluation-input-refs-refused/runs/syntax-code.store.json",
    }
    pr_fail = []
    for k, want in preserved.items():
        got = sha256(pr_map[k].read_bytes())
        if got != want:
            pr_fail.append({"k": k, "got": got, "want": want})
    record(
        "custody-preserved-predecessor-failures",
        not pr_fail,
        selector="preserve failed examples; original/structural/eirefs stores byte-identical",
        operands={"preserved": preserved, "failures": pr_fail},
        assertion="three predecessor syntax-code stores unchanged",
        class_="custody",
        export="standing",
        v3_status="present",
    )


def main() -> int:
    WITHDRAWN.extend([
        {
            "grade": "v3 independently reconstructed expected proof",
            "reason": "reconstruct_expected_proof read claimed proof.executionPlanId, proof.ruleProgramDigest, and proof.predicateProofs[0].scopeIds[0] as reconstruction inputs. C-equality to the consumer claim could not prove a shared selected-input derivation.",
            "selector": "evaluator-composition-contract.v3.md §7",
        },
        {
            "grade": "v3 evidence-proof-join",
            "reason": "checked object-table typedId self-identity (evidence.proofBundleId == table[id].typedId), not evidence.proofBundleId ↔ H(proof) ↔ seal.proofBundleId ↔ run.evidenceId.",
            "selector": "identity-schemas.v3 semantic-evidence.proofBundleId / evaluation-seal.proofBundleId",
        },
        {
            "grade": "v3 coverage-payload / ruleProgram / policyDigest retained",
            "reason": "equated blob-key presence with payload-registry document-byte join, C remainder, and selector inhabitance.",
            "selector": "x-opensip-payload-registry; identity-and-evidence.md §3",
        },
        {
            "grade": "v3 129/129 executed applicable laws / existingLawImplementationMisses none",
            "reason": "probe count is not a charter-conformance count. Payload registry, coverage totality/partition, selectedRefs exact totality, file snapshotJoins, languageVersionBindingLaw, closureMembership equalToDirect, seal.policyDigest, evidence coverage/import/finding sets, cell kind totality, nativeCoverageAccounts equality, and independent evidence/seal/run C were not executed.",
            "selector": "self-audit inventory",
        },
        {
            "grade": "v3 tamper-structural-before-semantic PASS as complete graph admission",
            "reason": "structuralOk was schema/H/selectedRefs-equality/remint-distinctness. Distinct enclosing identities and equal generated selected-input bytes are not the complete required join set.",
            "selector": "composition §7 report separately bounded shape/unit checks, complete graph admission and complete semantic replay",
        },
    ])
    MISSED_LAWS.extend([
        {"law": "x-opensip-payload-registry relation class", "owner": "identity-schemas.v3.json#/x-opensip-payload-registry", "v3": "not executed"},
        {"law": "x-opensip-payload-registry coverage class", "owner": "identity-schemas.v3.json#/x-opensip-payload-registry", "v3": "payloadDigest in blobs only"},
        {"law": "coverageTotalityLaw file@enumerated", "owner": "relation-payload-schemas.v2.json", "v3": "not executed"},
        {"law": "coveragePartitionLaw", "owner": "relation-payload-schemas.v2.json", "v3": "not executed"},
        {"law": "file snapshotJoins inventoried-file", "owner": "relation-payload-schemas.v2.json relations/file/snapshotJoins", "v3": "not executed (present in v1)"},
        {"law": "anchorLaw cardinalities", "owner": "relation-payload-schemas.v2.json anchorLaw", "v3": "not executed"},
        {"law": "languageVersionBindingLaw L0 derived", "owner": "identity-schemas.v3.json languageVersionBindingLaw", "v3": "frame tag presence only"},
        {"law": "closureMembership equalToDirect fact.producerClosure / proof.evaluatorClosure==seal", "owner": "identity-schemas.v3.json closureMembership", "v3": "evaluator in semanticClosures only"},
        {"law": "selectedRefs exact totality vs receipts+coverage+cell inventories", "owner": "execution-inputs-contract.v1.md §1", "v3": "n==4 inventories only"},
        {"law": "seal.policyDigest == plan.policyDigest", "owner": "identity-schemas.v3 evaluation-seal.policyDigest", "v3": "plan.policyDigest in blobs"},
        {"law": "evidence.coverageIds == view.coverageIds; importIds == plan.importIds", "owner": "identity-schemas.v3 semantic-evidence; composition §7", "v3": "view in evidence.viewIds containment"},
        {"law": "independent evidence/seal/run C", "owner": "composition §7", "v3": "proof C only"},
        {"law": "claimed predicate value vs retained witness matchingFactIds", "owner": "composition §3", "v3": "not executed"},
        {"law": "emitWhen true requires finding3", "owner": "composition §4", "v3": "not executed on claimed tamper graph"},
        {"law": "nativeCoverageAccounts coverageIds equality", "owner": "execution-inputs-contract.v1.md §5", "v3": "not executed"},
        {"law": "ruleProgram is policy projection", "owner": "identity-and-evidence.md §3", "v3": "copied claimed digest into expected proof"},
        {"law": "universe nativeContextId join", "owner": "identity-schemas.v3 native.semantic-universe.syntax.v2", "v3": "not executed"},
        {"law": "IMPORT_JOIN evidence.importIds", "owner": "identity-schemas.v3 semantic-evidence.importIds", "v3": "not executed"},
    ])

    custody_checks()
    pos = load_graph(POS)
    tamper = load_graph(TAMPER)
    admit_graph("positive", pos)
    admit_graph("tamper", tamper)

    pos_struct = first_of("positive", ("schema", "structural", "frame"))
    tamper_struct = first_of("tamper", ("schema", "structural", "frame"))

    expected_pos = None
    expected_t = None
    if pos_struct is None:
        expected_pos = semantic_replay("positive", pos, require_equal=True)
    else:
        not_reached(
            "positive-semantic-replay",
            selector="composition §7 complete replay after input admission",
            reason=f"positive structural refusal {pos_struct['name']} precedes replay; semantic replay notReached",
            export="positive",
        )
    if tamper_struct is None:
        expected_t = semantic_replay("tamper", tamper, require_equal=False)
        record(
            "tamper-structural-before-semantic",
            True,
            selector="Do not report a semantic tamper refusal before the complete replacement graph is structurally admitted",
            operands={"firstStructuralRefusal": None},
            assertion="tamper complete-graph admission passed; semantic C compare is therefore reached",
            class_="structural",
            export="tamper",
            v3_status="present-on-incomplete-admission",
        )
        record(
            "tamper-same-plan-and-executionInputs",
            tamper["plan"]["snapshotId"] == pos["plan"]["snapshotId"]
            and tamper["proof"]["executionInputsDigest"] == pos["proof"]["executionInputsDigest"]
            and tamper["exec"]["planId"] == pos["exec"]["planId"],
            selector="logical-result tamper preserves selected Plan and ExecutionInputsV1",
            operands={"posExec": pos["proof"]["executionInputsDigest"], "tamperExec": tamper["proof"]["executionInputsDigest"]},
            assertion="same selected inputs",
            class_="structural",
            export="tamper",
            v3_status="present",
        )
        record(
            "tamper-enclosing-ids-reminted",
            tamper["runId"] != pos["runId"] and tamper["proofId"] != pos["proofId"] and tamper["evidenceId"] != pos["evidenceId"] and tamper["sealId"] != pos["sealId"],
            selector="composition §7 discriminating control remints enclosing identities (not stale-hash)",
            operands={"pos": {"run": pos["runId"], "proof": pos["proofId"]}, "tamper": {"run": tamper["runId"], "proof": tamper["proofId"]}},
            assertion="run/proof/evidence/seal identities reminted. Remint distinctness is not by itself a complete graph.",
            class_="structural",
            export="tamper",
            v3_status="present",
        )
        record(
            "tamper-not-stale-hash",
            tamper["proof"]["executionInputsDigest"] == pos["proof"]["executionInputsDigest"] and tamper["proofId"] != pos["proofId"],
            selector="stale-hash control is a digest-field flip without remint; this exhibit remints proof/evidence/seal/run",
            operands={"sameExec": tamper["proof"]["executionInputsDigest"] == pos["proof"]["executionInputsDigest"], "proofReminted": tamper["proofId"] != pos["proofId"]},
            assertion="same selected-input digest and reminted proof identity",
            class_="semantic",
            export="tamper",
            v3_status="present",
        )
        record(
            "tamper-fresh-derivation-still-pass-false",
            expected_t["proof"]["verdict"] == "pass" and expected_t["atomValue"] == "false",
            selector="composition §7 reconstruct from selected inputs only; claimed fail does not select truth",
            operands={"derivedVerdict": expected_t["proof"]["verdict"], "derivedAtom": expected_t["atomValue"], "claimedVerdict": tamper["proof"]["verdict"], "claimedAtom": tamper["proof"]["predicateProofs"][0]["value"]},
            assertion="fresh derivation from tamper selected inputs remains pass/false",
            class_="semantic",
            export="tamper",
            v3_status="present-but-used-claimed-fields",
        )
    else:
        not_reached(
            "tamper-semantic-replay",
            selector="composition §7 semantic replay of logical-result tamper",
            reason=f"tamper complete-graph admission refused at {tamper_struct['name']} before semantic C compare; semantic replay notReached",
            export="tamper",
        )
        record(
            "tamper-structural-before-semantic",
            False,
            selector="Do not report a semantic tamper refusal before the complete replacement graph is structurally admitted",
            operands={"firstStructuralRefusal": tamper_struct["name"], "selector": tamper_struct["selector"]},
            assertion="semantic tamper claim is notReached because the replacement graph is not fully admitted",
            class_="structural",
            export="tamper",
            v3_status="present-on-incomplete-admission",
        )

    pos_sem = first_of("positive", ("semantic", "replay"))
    tamper_sem = first_of("tamper", ("semantic", "replay"))
    tamper_semantic_reached = tamper_struct is None

    if pos_struct is not None:
        outcome = "PILOT_REFUSED"
        first_boundary = {"export": "positive", "phase": "structural", "probe": pos_struct}
    elif pos_sem is not None:
        outcome = "PILOT_REFUSED"
        first_boundary = {"export": "positive", "phase": "semantic", "probe": pos_sem}
    elif not tamper_semantic_reached:
        outcome = "PILOT_REFUSED"
        first_boundary = {"export": "tamper", "phase": "structural", "probe": tamper_struct, "semanticReplay": "notReached"}
    elif tamper_sem is not None and tamper_sem["name"] not in (
        "tamper-complete-proof-C",
        "tamper-fresh-derivation-still-pass-false",
        "tamper-not-stale-hash",
    ):
        # unexpected semantic failure besides the intended C-unequal
        if tamper_sem["name"] == "tamper-complete-proof-C" and tamper_sem["ok"] is False:
            outcome = "PILOT_REFUSED"
            first_boundary = {"export": "tamper", "phase": "semantic", "probe": tamper_sem}
        else:
            # intended refuse is complete-proof-C ok==True meaning C unequal when require_equal False
            outcome = "PILOT_ADMITS" if all(p["ok"] for p in PROBES if p["class"] != "custody" or p["ok"]) else "PILOT_REFUSED"
            first_boundary = None
    else:
        # tamper complete-proof-C with require_equal False is ok when C unequal
        outcome = "PILOT_ADMITS"
        first_boundary = {
            "export": "tamper",
            "phase": "semantic-after-structural-admission",
            "name": "tamper-complete-proof-C",
            "note": "intended discriminating refuse: derived pass/false vs claimed fail/true",
        }

    # Refine outcome: any non-ok probe in schema/structural/frame/semantic except intended tamper C-unequal success
    failed = [p for p in PROBES if not p["ok"]]
    # intended: tamper-complete-proof-C ok True means C unequal as required
    blocking = [p for p in failed if p["class"] in ("schema", "structural", "frame", "semantic", "replay", "custody")]
    if blocking:
        # first in probe order
        b0 = blocking[0]
        if b0["export"] == "positive" or b0["class"] == "custody":
            outcome = "PILOT_REFUSED"
            first_boundary = {"export": b0["export"], "phase": b0["class"], "probe": b0}
        elif b0["export"] == "tamper" and b0["class"] in ("schema", "structural", "frame"):
            outcome = "PILOT_REFUSED"
            first_boundary = {"export": "tamper", "phase": "structural", "probe": b0, "semanticReplay": "notReached"}
        elif b0["export"] == "tamper" and b0["class"] in ("semantic", "replay") and b0["name"] not in ("tamper-complete-proof-C",):
            # semantic fail other than the C-unequal assertion
            if "unequal" in (b0.get("assertion") or "") and b0["name"] == "tamper-complete-proof-C":
                pass
            else:
                outcome = "PILOT_REFUSED"
                first_boundary = {"export": "tamper", "phase": "semantic", "probe": b0}
        else:
            outcome = "PILOT_REFUSED"
            first_boundary = {"export": b0["export"], "phase": b0["class"], "probe": b0}

    # If the only failures are none and tamper C-unequal is ok, ADMITS
    if not blocking:
        outcome = "PILOT_ADMITS"
        first_boundary = {
            "export": "tamper",
            "phase": "semantic-after-structural-admission",
            "name": "tamper-complete-proof-C",
            "note": "intended discriminating refuse after complete admission",
        }

    results = {
        "probeCount": len(PROBES),
        "passCount": sum(1 for p in PROBES if p["ok"]),
        "failCount": sum(1 for p in PROBES if not p["ok"]),
        "failed": [{"name": p["name"], "export": p["export"], "class": p["class"], "selector": p["selector"], "assertion": p["assertion"], "operands": p.get("operands"), "detail": p.get("detail"), "v3Status": p.get("v3Status")} for p in PROBES if not p["ok"]],
        "firstPositiveStructural": pos_struct["name"] if pos_struct else None,
        "firstTamperStructural": tamper_struct["name"] if tamper_struct else None,
        "firstPositiveSemantic": pos_sem["name"] if pos_sem else None,
        "tamperSemanticReached": tamper_semantic_reached,
        "notReached": NOTREACHED,
        "withdrawnGrades": WITHDRAWN,
        "missedExistingLawsVsV3": MISSED_LAWS,
        "outcomeHypothesis": outcome,
        "firstBoundary": {
            "export": (first_boundary or {}).get("export"),
            "phase": (first_boundary or {}).get("phase"),
            "name": (first_boundary or {}).get("name") or ((first_boundary or {}).get("probe") or {}).get("name"),
            "selector": ((first_boundary or {}).get("probe") or {}).get("selector"),
            "semanticReplay": (first_boundary or {}).get("semanticReplay"),
            "note": (first_boundary or {}).get("note"),
        } if first_boundary else None,
        "positive": {
            "sha256": pos["sha256"],
            "bytes": pos["bytes"],
            "runId": pos["runId"],
            "proofId": pos["proofId"],
            "structuralOk": pos_struct is None,
        },
        "tamper": {
            "sha256": tamper["sha256"],
            "bytes": tamper["bytes"],
            "runId": tamper["runId"],
            "proofId": tamper["proofId"],
            "structuralOk": tamper_struct is None,
        },
        "expectedPositive": None if expected_pos is None else {
            "proofId": "proof3:" + H("proof-bundle", expected_pos["proof"]),
            "proofC": sha256(C(expected_pos["proof"])),
            "claimedC": sha256(C(pos["proof"])),
            "Cequal": C(expected_pos["proof"]) == C(pos["proof"]),
            "atom": expected_pos["atomValue"],
            "verdict": expected_pos["proof"]["verdict"],
            "usedClaimedProofFields": expected_pos["usedClaimedProofFields"],
        },
        "expectedTamper": None if expected_t is None else {
            "proofId": "proof3:" + H("proof-bundle", expected_t["proof"]),
            "proofC": sha256(C(expected_t["proof"])),
            "claimedC": sha256(C(tamper["proof"])),
            "Cequal": C(expected_t["proof"]) == C(tamper["proof"]),
            "atom": expected_t["atomValue"],
            "verdict": expected_t["proof"]["verdict"],
        },
        "relDocumentSha256": REL_FILE_DIGEST,
        "nativeDocumentSha256": NATIVE_FILE_DIGEST,
        "probes": PROBES,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "diagnostics").mkdir(exist_ok=True)
    (OUT / "diagnostics" / "pilot_selfaudit_probes.json").write_text(json.dumps(results, indent=2, default=str) + "\n")
    print(json.dumps({
        "probeCount": results["probeCount"],
        "passCount": results["passCount"],
        "failCount": results["failCount"],
        "failedNames": [p["name"] for p in results["failed"]],
        "outcomeHypothesis": outcome,
        "firstBoundary": results["firstBoundary"],
        "structuralPositive": results["positive"]["structuralOk"],
        "structuralTamper": results["tamper"]["structuralOk"],
        "tamperSemanticReached": tamper_semantic_reached,
        "expectedPositiveCequal": None if expected_pos is None else C(expected_pos["proof"]) == C(pos["proof"]),
        "notReachedN": len(NOTREACHED),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
