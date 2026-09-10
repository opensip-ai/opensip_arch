"""Shared synthetic-repository builders for the blind reconstruction.

Every OS / compiler / provider observation below is a SYNTHETIC TRUSTED OBSERVATION
(an assumption), never native enforcement proof.
"""

from __future__ import annotations

import hashlib

import opensip_ref as R
import closure as CL
from opensip_ref import C, H, ident, sha256_text, raw, raw_bytes

PROJECT_ID = "prj1-" + "3f" * 32
PLATFORM = "macos-aarch64"


def mkclosure(g, kind, files, semver, protocol=3, platform=PLATFORM):
    tree = []
    for path, data in sorted(files.items()):
        tree.append(g.retain_blob("closure:" + kind + ":" + path, data) | {"path": path})
    tree = sorted(
        [{"path": p, "sha256": raw_bytes(d), "bytes": len(d)} for p, d in files.items()],
        key=lambda r: r["path"],
    )
    for p, d in files.items():
        g.cas.put_bytes(d)
    manifest_body = C({"kind": kind, "semanticVersion": semver, "platform": platform})
    g.cas.put_bytes(manifest_body)
    desc = {
        "schemaVersion": 2,
        "kind": kind,
        "manifestDigest": raw_bytes(manifest_body),
        "tree": tree,
        "semanticVersion": semver,
        "protocolMajor": protocol,
        "platform": platform,
    }
    return g.add_closure(desc), desc


def base_closures(g, ts_compiler_version="5.6.3", rustc_version="1.83.0",
                  grammar_version="1.4.0", platform=PLATFORM):
    out = {}
    out["evaluator"], _ = mkclosure(g, "evaluator", {"bin/evaluator": b"EVAL-v2"}, "2.0.0",
                                    platform=platform)
    out["provider-ts"], _ = mkclosure(g, "provider",
                                      {"bin/ts-provider": b"TSPROV"}, "2.1.0", 2, platform)
    out["provider-rust"], _ = mkclosure(g, "provider",
                                        {"bin/rust-provider": b"RSPROV"}, "3.0.1", 3, platform)
    out["provider-syntax"], _ = mkclosure(g, "provider",
                                          {"bin/syntax-provider": b"SYNPROV"}, "1.2.0", 3, platform)
    out["detector"], _ = mkclosure(g, "detector", {"rules/unused.json": b"RULES"}, "1.0.0",
                                   platform=platform)
    ts_tool_files = {
        "bin/tsc.js": b"TSC-BINARY-" + ts_compiler_version.encode(),
        "bin/node": b"NODE-RUNTIME",
    }
    out["ts-toolchain"], d = mkclosure(g, "toolchain", ts_tool_files, ts_compiler_version, 2, platform)
    out["ts-toolchain-desc"] = d
    stdlib_files = {
        "lib.es2022.d.ts": b"declare-es2022",
        "lib.dom.d.ts": b"declare-dom",
        "lib.decorators.d.ts": b"declare-decorators",
    }
    out["ts-stdlib"], d = mkclosure(g, "stdlib", stdlib_files, ts_compiler_version, 2, platform)
    out["ts-stdlib-desc"] = d
    rust_tool_files = {
        "bin/rustc": b"RUSTC-" + rustc_version.encode(),
        "bin/cargo": b"CARGO-" + rustc_version.encode(),
        "bin/ld": b"LINKER",
        "bin/ar": b"AR",
        "bin/proc-macro-srv": b"PMSRV",
    }
    out["rust-toolchain"], d = mkclosure(g, "toolchain", rust_tool_files, rustc_version, 3, platform)
    out["rust-toolchain-desc"] = d
    out["rust-dev-llvm"], d = mkclosure(g, "rust-dev-llvm", {"lib/libLLVM.so": b"LLVM-19"},
                                        "19.1.0", 3, platform)
    out["rust-dev-llvm-desc"] = d
    grammar_files = {
        "grammars/rust.grammar": b"G-RUST",
        "grammars/typescript.grammar": b"G-TS",
        "grammars/javascript.grammar": b"G-JS",
        "grammars/json.grammar": b"G-JSON",
        "grammars/toml.grammar": b"G-TOML",
        "grammars/markdown.grammar": b"G-MD",
        "grammars/yaml.grammar": b"G-YAML",
        "bundle.manifest": b"BUNDLE-MANIFEST-v1",
        "normalizer/spec.txt": b"NORMALIZER-SPEC",
    }
    out["grammar"], d = mkclosure(g, "grammar", grammar_files, grammar_version, 3, platform)
    out["grammar-desc"] = d
    return out


# ---------------------------------------------------------------------------
# snapshot / plan
# ---------------------------------------------------------------------------


def build_snapshot(g, files, scope_descriptor, config, vcs_kind="git",
                   commit="a" * 40, dirty=False):
    inv = sorted([g.retain_blob(p, d) for p, d in files.items()], key=lambda r: r["path"])
    g.inventory = inv
    R.validate("identity", "#/$defs/source-inventory", inv)
    inv_digest = g.cas.put_record(inv)
    vcs = {
        "schemaVersion": 2,
        "kind": vcs_kind,
        "commitId": commit if vcs_kind != "none" else None,
        "dirty": dirty,
        "sourceInventoryDigest": inv_digest,
    }
    R.validate("identity", "#/$defs/vcs-observation", vcs)
    g.cas.put_record(vcs)
    g.scope_descriptor = scope_descriptor
    g.cas.put_record(scope_descriptor)
    g.config = config
    g.cas.put_record(config)
    snap = {
        "schemaVersion": 2,
        "projectId": PROJECT_ID,
        "sourceInventory": inv,
        "resolvedConfigDigest": raw(config),
        "scopeDigest": raw(scope_descriptor),
        "vcsDigest": raw(vcs),
    }
    R.validate("identity", "#/$defs/snapshot", snap)
    g.snapshot = snap
    g.snapshot_id = ident("snapshot", snap)
    g.cas.put_frame("snapshot", snap)
    return g.snapshot_id


def resolved_config(capabilities, budget_limit=100000, entry_points=None,
                    workspace_roots=None, ignore_paths=None, pack_ids=None,
                    import_ids=None):
    discovery = {}
    if entry_points is not None:
        discovery["entryPoints"] = sorted(entry_points)
    if workspace_roots is not None:
        discovery["workspaceRoots"] = sorted(workspace_roots)
    if ignore_paths is not None:
        discovery["ignorePaths"] = sorted(ignore_paths)
    policy = {}
    if pack_ids:
        policy["packIds"] = sorted(pack_ids)
    evidence = {}
    if import_ids:
        evidence["importIds"] = sorted(import_ids)
    cfg = {
        "analysis": {
            "profileId": "default",
            "capabilities": sorted(set(capabilities)),
            "budget": {"unit": "work-units", "limit": budget_limit},
        },
        "components": {},
        "discovery": discovery,
        "policy": policy,
        "evidence": evidence,
    }
    R.validate("identity", "#/$defs/semantic-configuration", cfg)
    return cfg


def scope_descriptor(roots, prefixes=(), excluded=()):
    sd = {
        "schemaVersion": 2,
        "workspaceRoots": sorted(set(roots), key=lambda s: C(s)),
        "pathPrefixes": sorted(set(prefixes), key=lambda s: C(s)),
        "excludedPathPrefixes": sorted(set(excluded), key=lambda s: C(s)),
    }
    R.validate("identity", "#/$defs/scope-descriptor", sd)
    return sd


def analysis_spec(requests, parameters=(), pack_ids=()):
    rows = sorted(requests, key=lambda r: C(r))
    spec = {
        "schemaVersion": 2,
        "requestedCapabilities": rows,
        "policyPackIds": sorted(pack_ids),
        "parameters": sorted(parameters, key=lambda r: C(r)),
    }
    R.validate("identity", "#/$defs/analysis-spec", spec)
    return spec


def semantic_grant(operations, scope_digest, principals=None):
    pr = principals if principals is not None else [
        {"kind": "first-party", "closureId": "closure2:" + "0" * 64, "ownerSourceDigest": None}
    ]
    sg = {
        "schemaVersion": 2,
        "projectId": PROJECT_ID,
        "principals": sorted(pr, key=lambda p: C(p)),
        "analysisOperations": sorted(set(operations), key=lambda s: C(s)),
        "scopeDigest": scope_digest,
    }
    R.validate("identity", "#/$defs/semantic-grant", sg)
    return sg


def capability_manifest(profile, providers, absent):
    return {
        "schemaVersion": 1,
        "profile": profile,
        "providers": providers,
        "coverageForAbsent": absent,
    }


def build_plan(g, closures, context_hexes, analysis_spec_rec, semantic_grant_rec,
               policy, waivers, manifest, import_ids=()):
    committed, cap_id = R.capability_manifest_id(manifest)
    g.cas.put_bytes(committed)
    g.analysis_spec = analysis_spec_rec
    g.cas.put_record(analysis_spec_rec)
    g.semantic_grant = semantic_grant_rec
    g.cas.put_record(semantic_grant_rec)
    g.policy = policy
    g.cas.put_record(policy)
    g.cas.put_record(waivers)
    plan = {
        "schemaVersion": 2,
        "snapshotId": g.snapshot_id,
        "capabilityManifestId": cap_id,
        "capabilityManifestBytesDigest": raw_bytes(committed),
        "semanticClosures": sorted(set(closures), key=lambda s: C(s)),
        "analysisSpecDigest": raw(analysis_spec_rec),
        "resolvedConfigDigest": raw(g.config),
        "nativeContextDigests": sorted(set(context_hexes), key=lambda s: C(s)),
        "importIds": sorted(import_ids, key=lambda s: C(s)),
        "policyDigest": raw(policy),
        "waiverDigest": raw(waivers),
        "scopeDigest": raw(g.scope_descriptor),
        "budget": g.config["analysis"]["budget"],
        "semanticGrantDigest": raw(semantic_grant_rec),
    }
    R.validate("identity", "#/$defs/plan", plan)
    g.plan = plan
    g.plan_id = ident("plan", plan)
    g.cas.put_frame("plan", plan)
    return g.plan_id


EMPTY_WAIVERS = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}


def simple_policy(rule_id, relation, min_resolution, op="none", gate=True,
                  severity="error", subject_kind="symbol", evidence_use=(), n=None,
                  evidence=None):
    atom = {"op": op, "relation": relation, "minResolution": min_resolution, "filters": []}
    if n is not None:
        atom["n"] = n
    if evidence is not None:
        atom["evidence"] = evidence
    rule = {
        "ruleId": rule_id,
        "ruleProgramRef": {
            "contributionId": "opensip.first-party.rules",
            "ruleStableId": rule_id,
            "semanticsMajor": 2,
            "programDigest": raw_bytes(b"rule-program-" + rule_id.encode()),
        },
        "enabled": True,
        "severity": severity,
        "gate": gate,
        "subjectEnumeration": {"universe": "native", "subjectKind": subject_kind},
        "emitWhen": atom,
        "evidenceUse": list(evidence_use),
    }
    doc = {
        "schemaFamily": "opensip.product.policy",
        "schemaMajor": 1,
        "gateSeverityAtLeast": "warning",
        "rules": [rule],
    }
    R.validate("policy-document", "#/$defs/PolicyDocumentV1", doc)
    return doc


def compile_program(policy):
    prog = {
        "schemaVersion": 1,
        "policyDigest": raw(policy),
        "rules": [
            {"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"], "emitWhen": r["emitWhen"]}
            for r in policy["rules"]
        ],
    }
    R.validate("policy-document", "#/$defs/RuleProgramV1", prog)
    return prog


# ---------------------------------------------------------------------------
# scope / coverage / fact helpers
# ---------------------------------------------------------------------------


def make_scope(g, relation, rung, src_u, tgt_u, enumerator, subjects):
    sc = {
        "schemaVersion": 2,
        "snapshotId": g.snapshot_id,
        "sourceUniverse": src_u,
        "targetUniverse": tgt_u,
        "relation": relation,
        "resolution": rung,
        "enumeratorClosure": enumerator,
        "subjects": sorted(set(subjects), key=lambda s: C(s)),
    }
    return g.add_scope(sc), sc


def entry(relation, rung, coverage, state, attempted, exhaustive, terminal,
          edge_count=0, edge_classes=(), deficiency=None, cause=None,
          exports_closed="closed", entry_points="all", nonliteral="none",
          external="none-declared", dispatch="not-applicable", reasons=(),
          dead_code=True, derivation_kinds=(), confidence=1000000,
          commitment=None, subject_count=0):
    return {
        "relation": relation,
        "resolution": rung,
        "coverage": coverage,
        "examinedUniverse": {"subjectScopeCommitment": commitment, "subjectCount": subject_count},
        "resolutionCompleteness": {
            "state": state,
            "attempted": attempted,
            "examinedExhaustive": exhaustive,
            "stageTerminal": terminal,
            "unresolvedEdgeCount": edge_count,
            "unresolvedEdgeClasses": sorted(edge_classes),
        },
        "closedWorld": {
            "exportsClosed": exports_closed,
            "entryPointsRecognized": entry_points,
            "nonliteralLoading": nonliteral,
            "externalConsumers": external,
            "dynamicDispatch": dispatch,
            "reasons": list(reasons),
            "deadCodeRepairEligible": dead_code,
        },
        "derivationKinds": sorted(derivation_kinds),
        "confidenceMillionths": confidence,
        "deficiency": deficiency,
        "nativeCause": cause,
    }


def make_coverage(g, scope_id, scope, ent):
    commitment = "sha256:" + scope_id[len("scope2:"):]
    ent = dict(ent)
    ent["examinedUniverse"] = {
        "subjectScopeCommitment": commitment,
        "subjectCount": len(scope["subjects"]),
    }
    payload = {
        "schemaVersion": 3,
        "key": {
            "relation": scope["relation"],
            "resolution": scope["resolution"],
            "sourceUniverse": scope["sourceUniverse"],
            "targetUniverse": scope["targetUniverse"],
            "subjectScopeCommitment": commitment,
        },
        "entry": ent,
    }
    R.validate("native", "#/$defs/CoverageResultV3", payload)
    desc = {
        "schemaVersion": 2,
        "scopeId": scope_id,
        "payloadSchemaDigest": R.NATIVE_DOC_DIGEST,
        "payloadDigest": raw(payload),
    }
    return g.add_coverage(desc, payload), payload


def make_fact(g, relation, rung, src_u, tgt_u, producer, payload, anchors=(),
              confidence=1000000):
    desc = {
        "schemaVersion": 2,
        "snapshotId": g.snapshot_id,
        "relation": relation,
        "resolution": rung,
        "sourceUniverse": src_u,
        "targetUniverse": tgt_u,
        "producerClosure": producer,
        "payloadSchemaDigest": R.RELATION_DOC_DIGEST,
        "payloadDigest": raw(payload),
        "anchors": sorted(anchors, key=lambda a: C(a)),
        "confidenceMillionths": confidence,
    }
    return g.add_fact(desc, payload), desc


def anchor(g, path, start, end):
    row = g.inv_row(path)
    return {"path": path, "blobDigest": row["sha256"], "startByte": start, "endByte": end}


def make_view(g, plan_id, scope_ids, fact_ids, coverage_ids, producer):
    v = {
        "schemaVersion": 2,
        "planId": plan_id,
        "scopeIds": sorted(set(scope_ids), key=lambda s: C(s)),
        "facts": sorted(set(fact_ids), key=lambda s: C(s)),
        "coverageIds": sorted(set(coverage_ids), key=lambda s: C(s)),
        "producerClosure": producer,
        "schemaDigests": sorted({R.RELATION_DOC_DIGEST, R.NATIVE_DOC_DIGEST}, key=lambda s: C(s)),
    }
    return g.add_view(v), v


# ---------------------------------------------------------------------------
# proof / evidence / seal / run for a single retained no-match predicate
# ---------------------------------------------------------------------------


def seal_run(g, view_ids, verdict="pass", predicate_value="false", scope_ids=(),
             matching_facts=(), coverage_ids=()):
    rule = g.policy["rules"][0]
    node = g.rule_program["rules"][0]["emitWhen"]
    prog_pred = {
        "schemaVersion": 2,
        "ruleProgramDigest": raw(g.rule_program),
        "ruleId": rule["ruleId"],
        "predicateId": "p",
        "operation": node["op"],
        "nodeDigest": raw(node),
    }
    R.validate("identity", "#/$defs/program-predicate", prog_pred)
    g.cas.put_record(prog_pred)
    witness = {
        "schemaVersion": 2,
        "programPredicateDigest": raw(prog_pred),
        "matchingFactIds": sorted(matching_facts, key=lambda s: C(s)),
        "coverageIds": sorted(coverage_ids, key=lambda s: C(s)),
        "countLimit": node.get("n") if node.get("op") == "count-at-most" else None,
        "childPredicateIds": [],
    }
    R.validate("identity", "#/$defs/predicate-witness", witness)
    g.cas.put_record(witness)
    inputs = sorted(
        [{"domain": "view", "digest": v[len("view2:"):]} for v in view_ids]
        + [{"domain": "rule-program", "digest": raw(g.rule_program)}]
        + [{"domain": "policy", "digest": raw(g.policy)}],
        key=lambda r: C(r),
    )
    exec_plan = {
        "schemaVersion": 2,
        "planId": g.plan_id,
        "stages": [],
    }
    stage_spec = {
        "schemaVersion": 2,
        "planId": g.plan_id,
        "producerClosure": g.plan["semanticClosures"][0],
        "operation": "native-analysis",
        "parameters": [],
        "outputDomains": ["fact", "coverage"],
        "outputSchemaDigest": R.NATIVE_DOC_DIGEST,
    }
    R.validate("identity", "#/$defs/stage-spec", stage_spec)
    g.cas.put_record(stage_spec)
    exec_plan["stages"] = [
        {"ordinal": 0, "stageSpecDigest": raw(stage_spec), "requires": [],
         "outputDomains": sorted(stage_spec["outputDomains"], key=lambda s: C(s))}
    ]
    R.validate("identity", "#/$defs/execution-plan", exec_plan)
    exec_plan_id = ident("execution-plan", exec_plan)
    g.cas.put_frame("execution-plan", exec_plan)
    proof = {
        "schemaVersion": 2,
        "planId": g.plan_id,
        "executionPlanId": exec_plan_id,
        "evaluatorClosure": g.evaluator_closure,
        "ruleProgramDigest": raw(g.rule_program),
        "evaluationInputRefs": inputs,
        "predicateProofs": [
            {
                "ruleId": rule["ruleId"],
                "subjectId": "subject:root",
                "predicateId": "p",
                "operation": node["op"],
                "inputRefs": inputs,
                "scopeIds": sorted(scope_ids, key=lambda s: C(s)),
                "value": predicate_value,
                "witnessDigest": raw(witness),
            }
        ],
        "findingIds": [],
        "verdict": verdict,
    }
    R.validate("identity", "#/$defs/proof-bundle", proof)
    proof_id = ident("proof-bundle", proof)
    g.cas.put_frame("proof-bundle", proof)
    union = sorted({c for v in view_ids for c in g.views[v]["coverageIds"]}, key=lambda s: C(s))
    evidence = {
        "schemaVersion": 2,
        "planId": g.plan_id,
        "viewIds": sorted(view_ids, key=lambda s: C(s)),
        "coverageIds": union,
        "importIds": list(g.plan["importIds"]),
        "findingIds": [],
        "proofBundleId": proof_id,
    }
    R.validate("identity", "#/$defs/semantic-evidence", evidence)
    evidence_id = ident("semantic-evidence", evidence)
    g.cas.put_frame("semantic-evidence", evidence)
    seal = {
        "schemaVersion": 2,
        "planId": g.plan_id,
        "executionPlanId": exec_plan_id,
        "evidenceId": evidence_id,
        "evaluatorClosure": g.evaluator_closure,
        "policyDigest": g.plan["policyDigest"],
        "proofBundleId": proof_id,
        "verdict": verdict,
    }
    R.validate("identity", "#/$defs/evaluation-seal", seal)
    seal_id = ident("evaluation-seal", seal)
    g.cas.put_frame("evaluation-seal", seal)
    run = {
        "schemaVersion": 2,
        "projectId": PROJECT_ID,
        "snapshotId": g.snapshot_id,
        "planId": g.plan_id,
        "evidenceId": evidence_id,
        "evaluationSealId": seal_id,
        "capabilityManifestId": g.plan["capabilityManifestId"],
    }
    R.validate("identity", "#/$defs/run", run)
    g.cas.put_frame("run", run)
    return proof, evidence, seal, run
