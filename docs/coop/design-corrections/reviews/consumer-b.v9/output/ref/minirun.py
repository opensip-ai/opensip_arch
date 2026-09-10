"""A minimal complete Run with one switch per closure law, so each negative
flips exactly one thing and the first observed refusal boundary is legible."""
from __future__ import annotations

import hashlib

import assemble as A
import build as B
import canon as K
import kit
import native as N
import scenarios as S
from store import Store, split_id

SRC = b"export function f() { return 1; }\n"
PKG = b'{"name":"mini","version":"1.0.0","private":true}\n'
TSCONFIG = b'{"compilerOptions":{"lib":["es2022"]}}\n'
BODY_START = SRC.index(b"{")
BODY_END = SRC.index(b"}\n") + 1


def build(**sw):
    s = Store()
    files = {"package.json": PKG, "tsconfig.json": TSCONFIG, "src/a.ts": SRC}
    if sw.get("deleted_vcs_change"):
        pass
    scope = B.scope_descriptor(["."])
    config = B.default_config(["inventory", "clones-fact"],
                              budget_limit=sw.get("config_budget", 100000))
    snap_id, snap, inventory = B.make_snapshot(s, files, scope, config)
    inv = {r["path"]: r for r in inventory}

    ctx, ctx_hex, cids = S.ts_context(
        s, language_mode="ts-tsconfig", config_graph_paths=["tsconfig.json"],
        lockfile=None, node_modules_digest=None)
    if sw.get("ctx_mutate"):
        ctx = sw["ctx_mutate"](s, ctx)
        ctx_hex = K.H("native.context.typescript.v2", ctx)
        s.put_native_identity("native.context.typescript.v2", ctx)

    graph = {"schemaVersion": 1, "entryConfigPath": "tsconfig.json", "nodes": [
        {"path": "tsconfig.json", "contentSha256": inv["tsconfig.json"]["sha256"],
         "kind": "tsconfig", "extendsResolved": []}]}
    u, u_hex = S.ts_universe(s, ctx, ctx_hex, language_mode="ts-tsconfig",
                             config_graph=graph, program_roots=["src/a.ts"])

    prov_id, _ = S.provider_closure(s, "typescript-semantic")
    prov2_id, _ = S.provider_closure(s, "other-provider", "2.0.0")
    eval_id, _ = S.evaluator_closure(s)
    det_id, _ = S.detector_closure(s)
    manifest = B.capability_manifest(providers=[B.provider_capability(
        "typescript-semantic", "typescript",
        {"clones": "normalized-body-hash", "file": "enumerated"},
        ["linux-x86_64-gnu"])])
    cm_id, cm_bd, _ = B.commit_capability_manifest(s, manifest)

    caps = sw.get("requested_capabilities") or [
        {"capabilityId": "inventory", "languageMode": "ts-tsconfig",
         "workspaceRoot": ".", "required": True}]
    params = sw.get("spec_parameters") or []
    spec = {"schemaVersion": 2, "requestedCapabilities": caps,
            "policyPackIds": ["cb9.pack"], "parameters": params}
    grant_digest, _ = A.semantic_grant(s, snap["scopeDigest"])
    policy_digest = s.put_record(POLICY)
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
               "waivers": []}
    waiver_digest = s.put_record(waivers)
    closures = [prov_id, eval_id, det_id]
    if sw.get("drop_provider_from_closures"):
        closures = [eval_id, det_id]
    ctx_digests = [ctx_hex]
    if sw.get("context_digest_mode") == "raw-payload":
        # the raw canonical payload retained under ITS OWN digest, so the
        # digest matches and the FRAME PREFIX is the boundary reached
        ctx_digests = [s.put_blob(K.C(ctx))]
    elif sw.get("context_digest_mode") == "unregistered-domain":
        ctx_digests = [s.put_blob(K.frame("native.context.cobol.v2", ctx))]
    plan_id, plan = B.make_plan(
        s, snap_id, snap, cm_id, cm_bd, closures, spec, ctx_digests,
        policy_digest, waiver_digest, grant_digest,
        {"unit": "work-units", "limit": sw.get("plan_budget", 100000)})

    other_snap_id = None
    if sw.get("wrong_source_join"):
        other_snap_id, _, _ = B.make_snapshot(
            s, {"other.ts": b"x\n"}, scope, config, commit="c" * 40)

    scopes, facts, coverages = {}, {}, {}
    s1_id, s1 = B.make_scope(s, snap_id, u_hex, u_hex, "file", "enumerated",
                             prov_id, [r["path"] for r in inventory])
    scopes[s1_id] = s1
    if sw.get("partition_overlap"):
        s1b_id, s1b = B.make_scope(s, snap_id, u_hex, u_hex, "file", "enumerated",
                                   prov_id, ["src/a.ts"])
        scopes[s1b_id] = s1b
    for row in inventory:
        fid, f = B.make_fact(
            s, other_snap_id or snap_id, "file", "enumerated", u_hex, u_hex,
            prov_id,
            {"path": row["path"],
             "contentSha256": (("de" * 32) if sw.get("file_digest_lie")
                               and row["path"] == "src/a.ts" else row["sha256"]),
             "byteLength": (row["bytes"] + 1) if sw.get("file_length_lie")
             and row["path"] == "src/a.ts" else row["bytes"]},
            [{"path": "src/a.ts", "blobDigest": inv["src/a.ts"]["sha256"],
              "startByte": 0, "endByte": 4}] if sw.get("inventory_anchor") else [])
        facts[fid] = f
    if sw.get("package_fact_borrowed_anchor"):
        pid, pf = B.make_fact(
            s, snap_id, "package", "manifest-declared", u_hex, u_hex, prov_id,
            {"manifestPath": "package.json", "packageName": "mini",
             "packageVersion": "1.0.0"},
            [{"path": "src/a.ts", "blobDigest": inv["src/a.ts"]["sha256"],
              "startByte": 0, "endByte": 4}])
        facts[pid] = pf
    if sw.get("unanchored_code_fact"):
        did, df = B.make_fact(s, snap_id, "declares", "syntactic", u_hex, u_hex,
                              prov_id,
                              {"container": "mod:src/a.ts", "declared": "sym:f",
                               "declarationKind": "function"}, [])
        facts[did] = df
    if sw.get("foreign_producer_fact"):
        gid, gf = B.make_fact(s, snap_id, "file", "enumerated", u_hex, u_hex,
                              prov2_id,
                              {"path": "src/a.ts",
                               "contentSha256": inv["src/a.ts"]["sha256"],
                               "byteLength": inv["src/a.ts"]["bytes"]}, [])
        facts[gid] = gf

    entry_kw = sw.get("coverage_kwargs") or {}
    for sid, sc in list(scopes.items()):
        cid, _, payload = B.make_coverage(
            s, sid, sc, B.coverage_entry(
                sc["relation"], sc["resolution"],
                sw.get("commitment") or ("sha256:" + split_id(sid, "scope2")),
                sw.get("subject_count", len(sc["subjects"])), **entry_kw))
        if sw.get("coverage_schema_lie"):
            desc = {"schemaVersion": 2, "scopeId": sid,
                    "payloadSchemaDigest": "ab" * 32,
                    "payloadDigest": s.put_record(payload)}
            cid = s.put_identity("coverage", desc)
        coverages[cid] = {"scopeId": sid, "payload": payload}

    view_id, view = B.make_view(
        s, plan_id, list(scopes), list(facts), list(coverages),
        prov2_id if sw.get("view_producer_lie") else prov_id,
        schema_digests=["ff" * 32] if sw.get("view_schema_unregistered") else None)

    sd, _ = B.make_stage(s, plan_id, prov_id, "native.analyze",
                         ["fact", "coverage"], kit.doc_digest("native"))
    ep_id, _ = B.make_exec_plan(s, plan_id, [
        {"ordinal": 0, "stageSpecDigest": sd, "requires": [],
         "outputDomains": sorted(["fact", "coverage"], key=K.C)}])
    out = A.finish_run(
        s, plan_id=plan_id, plan=plan, snapshot_id=snap_id,
        views={view_id: view}, view_ids=[view_id], scopes=scopes, facts=facts,
        coverages=coverages, policy=POLICY, policy_digest=policy_digest,
        waivers=waivers, rule_program=A.compile_program(POLICY, policy_digest),
        evaluator_closure_id=eval_id, detector_closure_id=det_id,
        exec_plan_id=ep_id, universe_language={u_hex: "typescript"},
        capability_manifest_id=cm_id)
    if sw.get("hidden_finding_evidence"):
        fin = dict(out["findings"][0]) if out["findings"] else None
        if fin is None:
            orphan = None
        else:
            fin = dict(fin)
            fin["evidenceRefs"] = sorted(
                fin["evidenceRefs"] + [{"domain": "fact", "digest": "cc" * 32}],
                key=K.C)
            new_fid = s.put_identity("finding", fin)
            ev = dict(out["evidence"])
            ev["findingIds"] = sorted([new_fid], key=K.C)
            ev_id = s.put_identity("semantic-evidence", ev)
            pr = dict(out["proof"])
            pr["findingIds"] = sorted([new_fid], key=K.C)
            pr_id = s.put_identity("proof-bundle", pr)
            ev["proofBundleId"] = pr_id
            ev_id = s.put_identity("semantic-evidence", ev)
            seal = dict(out["seal"], evidenceId=ev_id, proofBundleId=pr_id)
            seal_id = s.put_identity("evaluation-seal", seal)
            run = dict(out["run"], evidenceId=ev_id, evaluationSealId=seal_id)
            out["runId"] = s.put_identity("run", run)
    out.update({"store": s, "universeHex": u_hex, "contextHex": ctx_hex,
                "planId": plan_id, "snapshotId": snap_id,
                "inventory": inventory, "providerClosure": prov_id,
                "otherProvider": prov2_id, "viewId": view_id,
                "capabilityManifestId": cm_id})
    return out


POLICY = {
    "schemaFamily": "opensip.product.policy", "schemaMajor": 1,
    "gateSeverityAtLeast": "error",
    "rules": [{"ruleId": "cb9.mini", "enabled": True, "severity": "error",
               "gate": True,
               "ruleProgramRef": {"contributionId": "cb9.native",
                                  "ruleStableId": "cb9.mini",
                                  "semanticsMajor": 1, "programDigest": "77" * 32},
               "subjectEnumeration": {"universe": "typescript",
                                      "subjectKind": "file",
                                      "include": ["src/a.ts"]},
               "emitWhen": {"op": "exists", "relation": "file",
                            "minResolution": "enumerated", "filters": []},
               "evidenceUse": [], "messageCode": "cb9.mini.file"}]}
