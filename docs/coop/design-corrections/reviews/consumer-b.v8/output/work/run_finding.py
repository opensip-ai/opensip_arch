"""CB-RUN-FIND: a complete positive Run whose predicate is TRUE, so the rule's
emission condition produces a finding.

Exercises finding-key2, finding2, finding-parameters, the declaration-signature
DISCRIMINATOR recipe, and the finding-citation closure (a citation cannot
introduce an extra authoritative input root).
"""
from __future__ import annotations

import assemble
import build
import closure as CL
import osip
from build import Fixture, coverage_entry
from osip import C, H, raw_sha256, record_digest

PLATFORM = "macos-aarch64"
TS_VERSION = "5.6.3"

POLICY = {
    "schemaFamily": "opensip.product.policy", "schemaMajor": 1,
    "gateSeverityAtLeast": "error",
    "rules": [{
        "ruleId": "inventory-present",
        "ruleProgramRef": {"contributionId": "opensip.first-party.detectors",
                           "ruleStableId": "inventory-present",
                           "semanticsMajor": 1, "programDigest": "0" * 64},
        "enabled": True, "severity": "error", "gate": True,
        "subjectEnumeration": {"universe": "repository", "subjectKind": "file"},
        "emitWhen": {"op": "exists", "relation": "file",
                     "minResolution": "enumerated", "filters": []},
        "evidenceUse": [], "messageCode": "cb.inventory-present"}]}

CAP_MANIFEST = {
    "schemaVersion": 1, "profile": "default",
    "providers": [{"providerId": "opensip.provider.typescript",
                   "language": "typescript",
                   "providerVersionSource": "closure-manifest",
                   "toolchainIdentitySource": "native-context",
                   "relations": {"file": "enumerated"},
                   "platformIds": [PLATFORM]}],
    "coverageForAbsent": []}


def build_run(mutate=None):
    fx = Fixture("cb-finding")
    m = mutate or {}
    fx.add_file("package.json", b'{"name":"cb","version":"1.0.0","private":true}\n')
    fx.add_file("src/a.ts", b"export function add(a: number, b: number) { return a; }\n")
    fx.add_file("tsconfig.json", b'{"compilerOptions":{"lib":["es2022"]}}\n')
    inv = {r["path"]: r for r in fx.inventory()}

    tool_cid, _, tm = fx.closure("typescript-toolchain", "toolchain",
                                 {"bin/tsc.js": b"#tsc\n", "bin/node": b"#node\n"},
                                 TS_VERSION, PLATFORM, protocol_major=2)
    std_cid, _, sm = fx.closure("typescript-stdlib", "stdlib",
                                {"lib/lib.es2022.d.ts": b"declare var y: any;\n"},
                                TS_VERSION, PLATFORM, protocol_major=2)
    prov_cid, _, _ = fx.closure("typescript-provider", "provider",
                                {"bin/p": b"#p\n"}, "1.0.0", PLATFORM, protocol_major=2)
    eval_cid, _, _ = fx.closure("evaluator", "evaluator", {"bin/e": b"#e\n"},
                                "1.0.0", PLATFORM, protocol_major=2)
    det_cid, _, _ = fx.closure("inventory-detector", "detector",
                               {"bin/d": b"#detector\n"}, "1.0.0", PLATFORM,
                               protocol_major=2)

    graph = {"schemaVersion": 1, "entryConfigPath": "tsconfig.json",
             "nodes": [{"path": "tsconfig.json",
                        "contentSha256": inv["tsconfig.json"]["sha256"],
                        "kind": "tsconfig", "extendsResolved": []}]}
    gd = fx.rec(graph, "native", "#/$defs/TypeScriptConfigGraphV1", "graph")
    honored = {"allowJs": False, "checkJs": False, "module": "node16",
               "moduleResolution": "node16", "target": "es2022", "strict": True,
               "skipLibCheck": True, "noEmit": True, "types": None,
               "lib": ["es2022"], "baseUrl": None, "paths": [], "rootDirs": [],
               "resolveJsonModule": False, "allowSyntheticDefaultImports": False,
               "esModuleInterop": False, "customConditions": [], "jsx": None}
    ctx = {"schemaVersion": 2, "languageMode": "ts-tsconfig",
           "toolchain": {"compilerName": "typescript", "compilerVersion": TS_VERSION,
                         "compilerPackageDigest": tm["bin/tsc.js"],
                         "typescriptStdlibMerkleRoot": std_cid.split(":")[1],
                         "standardLibraryComponentDigests": [
                             {"component": "lib.es2022.d.ts",
                              "sha256": sm["lib/lib.es2022.d.ts"]}],
                         "libSelection": ["es2022"]},
           "toolClosure": {"compiler": tm["bin/tsc.js"], "runtime": tm["bin/node"],
                           "closureId": tool_cid},
           "configProjection": {"schemaVersion": 2, "ancestorCarrierVerified": True,
                                "environmentSanitized": True,
                                "typeAcquisitionEnabled": False,
                                "executableSelected": False,
                                "honoredOptions": honored, "strippedOptions": [],
                                "configGraphPaths": ["tsconfig.json"]},
           "moduleResolutionMode": "node16", "packageModuleType": "absent",
           "nodeModulesLayoutDigest": None, "lockfileIdentity": None}
    uni = {"schemaVersion": 2, "languageMode": "ts-tsconfig",
           "configOrigin": "tsconfig", "synthesizerVersion": None,
           "synthesizedOptions": None, "packageModuleType": "absent",
           "allowJs": False, "checkJs": False, "jsAdmittedToProgram": False,
           "jsDiagnosticsEnabled": False, "resolutionCompletenessImplied": False,
           "jsRootFiles": [], "programRootFiles": ["src/a.ts"],
           "lockfileKind": "none", "nodeModulesInReadSet": False,
           "executionCapableResolution": False,
           "tsconfigGraphHash": gd, "nativeContextId": None}

    A = assemble.Assembly(
        fx, capabilities=["inventory"],
        spec_rows=[{"capabilityId": "inventory", "languageMode": "ts-tsconfig",
                    "workspaceRoot": ".", "required": True}],
        policy=POLICY, capability_manifest=CAP_MANIFEST)
    ctx_hex = A.add_context("native.context.typescript.v2", ctx,
                            "#/$defs/TypeScriptNativeContextV2")
    uni["nativeContextId"] = "sha256:" + ctx_hex
    uni_hex = A.add_universe("native.semantic-universe.typescript.v2", uni,
                             "#/$defs/TypeScriptUniverseV2ResolvedInputs", "universe")
    A.seal_snapshot()
    A.seal_plan([prov_cid, eval_cid, tool_cid, std_cid, det_cid])

    facts = {p: A.add_fact("file", "enumerated", uni_hex, uni_hex, prov_cid,
                           {"path": p, "contentSha256": r["sha256"],
                            "byteLength": r["bytes"]}, [], label=p)
             for p, r in sorted(inv.items())}
    s_file, h_file = A.add_scope("file", "enumerated", uni_hex, uni_hex, prov_cid,
                                 sorted(inv))
    c_file = A.add_coverage(s_file, h_file, coverage_entry(
        "file", "enumerated", "sha256:" + h_file, len(inv), "complete"))
    view = A.seal_view(prov_cid, [s_file], list(facts.values()), [c_file],
                       [build.RELATION_DOC_DIGEST, build.NATIVE_DOC_DIGEST])

    # ---- the finding ---------------------------------------------------
    # identity section 3: `discriminator` is raw SHA-256 of the canonical JSON
    # ORDERED string array of declaration-signature tokens, in GRAMMAR order,
    # with repeated tokens retained and bodies/positions excluded.
    tokens = ["typescript", "function", "add", "generic-arity:0",
              "(", "a", ":", "number", ",", "b", ":", "number", ")"]
    fx.s.put_record(tokens, "declaration-signature tokens")
    discriminator = raw_sha256(C(tokens))
    fp = {"schemaVersion": 2, "ruleStableId": "inventory-present",
          "detectorSemanticsMajor": 1,
          "subjectKey": {"language": "typescript", "kind": "function",
                         "logicalPath": "src/a.ts", "qualifiedName": "add",
                         "discriminator": discriminator},
          "relatedSubjectKeys": []}
    fp_hex = fx.hid("finding-fingerprint", fp, "identity",
                    "#/$defs/finding-fingerprint", "finding-fingerprint")
    params = {"schemaVersion": 2, "messageCode": "cb.inventory-present",
              "parameters": {"path": "src/a.ts", "count": 3, "gating": True}}
    pdg = fx.rec(params, "identity", "#/$defs/finding-parameters",
                 "finding-parameters")
    refs = [{"domain": "fact", "digest": facts["src/a.ts"].split(":")[1]},
            {"domain": "coverage", "digest": c_file.split(":")[1]}]
    if m.get("cite_unretained_fact"):
        refs = [{"domain": "fact", "digest": "0" * 64}]
    if m.get("cite_blob_not_an_input"):
        refs = refs + [{"domain": "blob", "digest": inv["src/a.ts"]["sha256"]}]
    finding = {"schemaVersion": 2, "fingerprint": "finding-key2:" + fp_hex,
               "ruleClosure": det_cid, "subjectId": "function:src/a.ts#add",
               "messageCode": "cb.inventory-present", "parameterDigest": pdg,
               "severity": "error",
               "evidenceRefs": sorted(refs, key=lambda r: C(r))}
    if m.get("finding_message_code_drift"):
        finding["messageCode"] = "cb.other"
    if m.get("rule_closure_is_provider"):
        finding["ruleClosure"] = prov_cid
    f_hex = fx.hid("finding", finding, "identity", "#/$defs/finding", "finding")
    A.witness_facts = [facts["src/a.ts"]]
    run_id = A.seal_run(eval_cid, prov_cid, [view], predicate_value="true",
                        verdict="fail", findings=["finding2:" + f_hex])
    A.extra = {"findingId": "finding2:" + f_hex,
               "fingerprint": "finding-key2:" + fp_hex,
               "discriminator": discriminator, "signatureTokens": tokens,
               "findingParameters": params, "verdict": "fail"}
    return fx, A, run_id
