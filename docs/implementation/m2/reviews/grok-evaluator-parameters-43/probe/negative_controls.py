#!/usr/bin/env python3
"""Discriminating malformed/semantic negatives vs selected required_parameters and rust owner."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

OVERLAY = Path(
    "/tmp/opensip-implementation/m2-enumeration-join-trial-41/reference/"
    "archroot/docs/coop/design-corrections/foundation"
)
REQ = Path("/tmp/opensip-implementation/m2-evaluator-parameters-trial-43/reference-check/requests.ndjson")
BIN = Path("/tmp/opensip-implementation/m2-grok-evaluator-parameters-43/review/probe/harness/target/debug/retained-graph-harness")
OUT = Path("/tmp/opensip-implementation/m2-grok-evaluator-parameters-43/review/probe/negatives.json")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def blob_map(req):
    return {r["digest"]: bytes.fromhex(r["hex"]) for r in req["blobs"]}


def obj_map(req):
    return {r["id"]: r for r in req["objects"]}


def store_blob(req, value, C):
    raw = C.canonical(value)
    digest = hashlib.sha256(raw).hexdigest()
    req["blobs"] = [b for b in req["blobs"] if b["digest"] != digest]
    req["blobs"].append({"digest": digest, "hex": raw.hex()})
    return digest


def set_plan(req, plan, IM):
    pid = IM.identifier("plan", plan)
    req["objects"] = [o for o in req["objects"] if o["id"] != req["planId"] and o["id"] != pid]
    req["objects"].append({"id": pid, "domain": "plan", "descriptor": plan})
    req["planId"] = pid


def rust(req):
    raw = json.dumps(req).encode() + b"\n"
    r = subprocess.run([str(BIN)], input=raw, capture_output=True)
    if r.returncode != 0:
        return {"error": f"harness:{r.returncode}", "stderr": r.stderr.decode()[:500]}
    return json.loads(r.stdout.decode().splitlines()[0])


def py_eval(model, req):
    objects = {r["id"]: (r["domain"], r["descriptor"]) for r in req["objects"]}
    blobs = blob_map(req)
    plan = objects[req["planId"]][1]
    spec = model.C.parse(blobs[plan["analysisSpecDigest"]])
    try:
        selected, policy, emission = model.required_parameters(plan, spec, blobs, objects, model.E.M)
        return {"ok": True, "selected": list(selected), "policySchemaMajor": policy.get("schemaMajor")}
    except Exception as exc:
        msg = str(exc)
        return {"ok": False, "errorType": type(exc).__name__, "error": msg}


def main():
    if sys.flags.int_max_str_digits != 0:
        return 2
    model = load("evaluator_input_v3", OVERLAY / "evaluator_input_model.v3.py")
    IM = model.E.M
    C = model.C
    base = json.loads(REQ.read_text().splitlines()[0])
    blobs = blob_map(base)
    plan0 = obj_map(base)[base["planId"]]["descriptor"]
    spec0 = C.parse(blobs[plan0["analysisSpecDigest"]])
    emission0 = C.parse(blobs[next(p["payloadDigest"] for p in spec0["parameters"] if p["schemaDigest"].startswith("ac9ae438"))])
    policy0 = C.parse(blobs[plan0["policyDigest"]])

    cases = []

    def run(name, req, note):
        py = py_eval(model, req)
        rs = rust(req)
        rs_err = rs.get("error")
        cases.append({"id": name, "note": note, "python": py, "rust": {"error": rs_err, "ok": "error" not in rs}})

    # 1 missing emission parameter
    q = copy.deepcopy(base)
    plan = copy.deepcopy(plan0)
    spec = copy.deepcopy(spec0)
    spec["parameters"] = [p for p in spec["parameters"] if not p["schemaDigest"].startswith("ac9ae438")]
    plan["analysisSpecDigest"] = store_blob(q, spec, C)
    set_plan(q, plan, IM)
    run("missing-emission-parameter", q, "EVALUATOR_REQUIRED_PARAMETER_MISSING emission")

    # 2 unregistered schemaDigest
    q = copy.deepcopy(base)
    plan = copy.deepcopy(plan0)
    spec = copy.deepcopy(spec0)
    spec["parameters"][0]["schemaDigest"] = "00" * 32
    plan["analysisSpecDigest"] = store_blob(q, spec, C)
    set_plan(q, plan, IM)
    run("unregistered-schema-digest", q, "EVALUATOR_PARAMETER_UNREGISTERED")

    # 3 duplicate emission row
    q = copy.deepcopy(base)
    plan = copy.deepcopy(plan0)
    spec = copy.deepcopy(spec0)
    em = next(p for p in spec["parameters"] if p["schemaDigest"].startswith("ac9ae438"))
    spec["parameters"] = spec["parameters"] + [copy.deepcopy(em)]
    plan["analysisSpecDigest"] = store_blob(q, spec, C)
    set_plan(q, plan, IM)
    run("duplicate-emission-parameter", q, "EVALUATOR_PARAMETER_DUPLICATE")

    # 4 policyDigest mismatch on emission
    q = copy.deepcopy(base)
    plan = copy.deepcopy(plan0)
    spec = copy.deepcopy(spec0)
    emission = copy.deepcopy(emission0)
    emission["policyDigest"] = "11" * 32
    digest = store_blob(q, emission, C)
    for p in spec["parameters"]:
        if p["schemaDigest"].startswith("ac9ae438"):
            p["payloadDigest"] = digest
    plan["analysisSpecDigest"] = store_blob(q, spec, C)
    set_plan(q, plan, IM)
    run("emission-policy-digest-mismatch", q, "EVALUATOR_POLICY_BINDING")

    # 5 policy schemaMajor 1
    q = copy.deepcopy(base)
    plan = copy.deepcopy(plan0)
    policy = copy.deepcopy(policy0)
    policy["schemaMajor"] = 1
    plan["policyDigest"] = store_blob(q, policy, C)
    emission = copy.deepcopy(emission0)
    emission["policyDigest"] = plan["policyDigest"]
    spec = copy.deepcopy(spec0)
    digest = store_blob(q, emission, C)
    for p in spec["parameters"]:
        if p["schemaDigest"].startswith("ac9ae438"):
            p["payloadDigest"] = digest
    plan["analysisSpecDigest"] = store_blob(q, spec, C)
    set_plan(q, plan, IM)
    run("policy-schema-major-1", q, "EVALUATOR_POLICY_BINDING or Record schema")

    # 6 rule totality: drop last emission rule
    q = copy.deepcopy(base)
    plan = copy.deepcopy(plan0)
    spec = copy.deepcopy(spec0)
    emission = copy.deepcopy(emission0)
    if emission.get("rules"):
        emission["rules"] = emission["rules"][:-1]
    digest = store_blob(q, emission, C)
    for p in spec["parameters"]:
        if p["schemaDigest"].startswith("ac9ae438"):
            p["payloadDigest"] = digest
    plan["analysisSpecDigest"] = store_blob(q, spec, C)
    set_plan(q, plan, IM)
    run("emission-rule-totality-short", q, "EVALUATOR_EMISSION_RULE_TOTALITY")

    # 7 fingerprint namespace duplicate
    q = copy.deepcopy(base)
    plan = copy.deepcopy(plan0)
    spec = copy.deepcopy(spec0)
    emission = copy.deepcopy(emission0)
    if len(emission.get("rules") or []) >= 2:
        emission["rules"][1]["ruleStableId"] = emission["rules"][0]["ruleStableId"]
        emission["rules"][1]["semanticsMajor"] = emission["rules"][0]["semanticsMajor"]
        # keep ruleId distinct so totality can pass
    digest = store_blob(q, emission, C)
    for p in spec["parameters"]:
        if p["schemaDigest"].startswith("ac9ae438"):
            p["payloadDigest"] = digest
    plan["analysisSpecDigest"] = store_blob(q, spec, C)
    set_plan(q, plan, IM)
    run("duplicate-fingerprint-namespace", q, "NAMESPACE or totality first")

    # 8 unregistered policy universe
    q = copy.deepcopy(base)
    plan = copy.deepcopy(plan0)
    policy = copy.deepcopy(policy0)
    if policy.get("rules"):
        policy["rules"][0]["subjectEnumeration"]["universe"] = "cobol"
    plan["policyDigest"] = store_blob(q, policy, C)
    emission = copy.deepcopy(emission0)
    emission["policyDigest"] = plan["policyDigest"]
    spec = copy.deepcopy(spec0)
    digest = store_blob(q, emission, C)
    for p in spec["parameters"]:
        if p["schemaDigest"].startswith("ac9ae438"):
            p["payloadDigest"] = digest
    plan["analysisSpecDigest"] = store_blob(q, spec, C)
    set_plan(q, plan, IM)
    run("policy-universe-unregistered", q, "EVALUATOR_POLICY_UNIVERSE_UNREGISTERED or Record schema")

    # 9 detector closure is provider
    q = copy.deepcopy(base)
    plan = copy.deepcopy(plan0)
    spec = copy.deepcopy(spec0)
    emission = copy.deepcopy(emission0)
    provider = next(o["id"] for o in q["objects"] if o["domain"] == "closure" and o["descriptor"].get("kind") == "provider")
    for row in emission.get("rules") or []:
        row["detectorClosure"] = provider
    digest = store_blob(q, emission, C)
    for p in spec["parameters"]:
        if p["schemaDigest"].startswith("ac9ae438"):
            p["payloadDigest"] = digest
    plan["analysisSpecDigest"] = store_blob(q, spec, C)
    set_plan(q, plan, IM)
    run("detector-closure-is-provider", q, "EVALUATOR_EMISSION_CLOSURE_KIND")

    # 10 detectorClosure listed in plan but missing object
    q = copy.deepcopy(base)
    plan = copy.deepcopy(plan0)
    spec = copy.deepcopy(spec0)
    emission = copy.deepcopy(emission0)
    ghost = "closure2:" + "ab" * 32
    plan["semanticClosures"] = list(plan["semanticClosures"]) + [ghost]
    for row in emission.get("rules") or []:
        row["detectorClosure"] = ghost
    digest = store_blob(q, emission, C)
    for p in spec["parameters"]:
        if p["schemaDigest"].startswith("ac9ae438"):
            p["payloadDigest"] = digest
    plan["analysisSpecDigest"] = store_blob(q, spec, C)
    set_plan(q, plan, IM)
    run("detector-closure-missing-object", q, "Python KeyError vs rust Record MissingObject")

    OUT.write_text(json.dumps(cases, indent=2) + "\n")
    for c in cases:
        py = c["python"]
        rs = c["rust"]
        print(f"{c['id']:36} py={py.get('errorType') or 'ok'}:{(py.get('error') or '')[:60]!s:60} rust={'ok' if rs['ok'] else (rs.get('error') or '')[:80]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
