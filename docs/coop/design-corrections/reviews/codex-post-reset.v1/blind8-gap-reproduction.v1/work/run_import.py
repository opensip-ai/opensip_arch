"""CB-IMP: a Run with an actual REGISTERED imported payload record.

Exercises the one `import2` wrapper, the closed payload registry row, the
mandatory source correspondence, the observation record, and the
imported-observation boundary (no imported observation is Coverage, and one
window is never a universal negative).
"""
from __future__ import annotations

import assemble
import build
import closure as CL
import osip
import schemas
from build import Fixture, coverage_entry
from osip import C, H, raw_sha256, record_digest

PLATFORM = "macos-aarch64"
TS_VERSION = "5.6.3"
IMPORTED_EVIDENCE_DOC = ("docs/coop/design-corrections/workflows/schemas/"
                         "imported-evidence.schema.json")
IMPORTED_EVIDENCE_DIGEST = osip.doc_digest(IMPORTED_EVIDENCE_DOC)

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
    fx = Fixture("cb-import")
    m = mutate or {}
    fx.add_file("package.json", b'{"name":"cb","version":"1.0.0","private":true}\n')
    fx.add_file("src/a.ts", b"export const a = 1;\n")
    fx.add_file("tsconfig.json", b'{"compilerOptions":{"lib":["es2022"]}}\n')
    fx.s.put_raw(osip.doc_bytes(IMPORTED_EVIDENCE_DOC),
                 "schema-document:imported-evidence")
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
    imp_prov, _, _ = fx.closure("coverage-producer", "provider",
                                {"bin/c8": b"#coverage tool\n"}, "1.0.0", PLATFORM,
                                protocol_major=1)
    imp_adapt, _, _ = fx.closure("runtime-adapter", "adapter",
                                 {"bin/adapter": b"#normalizer\n"}, "1.0.0",
                                 PLATFORM, protocol_major=1)

    graph = {"schemaVersion": 1, "entryConfigPath": "tsconfig.json",
             "nodes": [{"path": "tsconfig.json",
                        "contentSha256": inv["tsconfig.json"]["sha256"],
                        "kind": "tsconfig", "extendsResolved": []}]}
    graph_digest = fx.rec(graph, "native", "#/$defs/TypeScriptConfigGraphV1", "graph")
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
           "tsconfigGraphHash": graph_digest, "nativeContextId": None}

    A = assemble.Assembly(
        fx, capabilities=["inventory"],
        spec_rows=[{"capabilityId": "inventory", "languageMode": "ts-tsconfig",
                    "workspaceRoot": ".", "required": True}],
        grant_ops=("read-source", "native-analysis", "read-import"),
        capability_manifest=CAP_MANIFEST)
    ctx_hex = A.add_context("native.context.typescript.v2", ctx,
                            "#/$defs/TypeScriptNativeContextV2")
    uni["nativeContextId"] = "sha256:" + ctx_hex
    uni_hex = A.add_universe("native.semantic-universe.typescript.v2", uni,
                             "#/$defs/TypeScriptUniverseV2ResolvedInputs", "universe")
    A.seal_snapshot()

    # ---- the import2 wrapper -------------------------------------------
    payload = {"payloadDomain": "workflow.import-payload.runtime.v1",
               "format": "v8-json",
               "observationWindow": {"startUtc": "2026-09-01T00:00:00Z",
                                     "endUtc": "2026-09-02T00:00:00Z"},
               "observedPopulation": "test-suite",
               "subjects": [
                   {"path": "src/a.ts", "symbol": "a",
                    "observability": "observed-hit", "hits": 12},
                   {"path": "src/a.ts", "symbol": "b",
                    "observability": "observable-unhit", "hits": 0},
                   {"path": "package.json", "observability": "unmapped"}],
               "mappingGaps": ["package.json is not an executable subject"]}
    if m.get("hits_on_unmapped"):
        payload["subjects"][2]["hits"] = 3
    pd = fx.rec(payload, "imported-evidence", "#/$defs/RuntimePayloadV1",
                "runtime payload")
    corr = {"kind": "exact-snapshot", "snapshotId": A.snapshot_id}
    if m.get("commit_name_alone"):
        corr = {"kind": "vcs-revision",
                "vcsRevision": {"system": "git", "commit": "c" * 40, "dirty": False},
                "buildIdentity": "ci-4711", "sourceMappingDigest": None}
    cd = fx.rec(corr, "common", "#/$defs/SourceCorrespondence", "correspondence")
    bd = fx.rec({"schemaVersion": 1, "buildIdentity": "ci-4711"},
                "imported-evidence", "#/$defs/BuildIdentityV1", "build identity")
    iscope = build.scope_descriptor(["."], [], [])
    sd = fx.rec(iscope, "identity", "#/$defs/scope-descriptor", "import scope")
    obs = {"schemaVersion": 1, "kind": "runtime",
           "window": {"startUtc": "2026-09-01T00:00:00Z",
                      "endUtc": "2026-09-02T00:00:00Z"},
           "population": "test-suite", "selection": None, "revisionRange": None}
    od = fx.rec(obs, "imported-evidence", "#/$defs/ImportObservationV1", "observation")
    raw_artifact = b'{"result":[{"url":"file:///src/a.ts","functions":[]}]}\n'
    fx.s.put_raw(raw_artifact, "original coverage artifact")
    wrapper = {"schemaVersion": 2, "kind": "runtime",
               "payloadSchemaDigest": (
                   "0" * 64 if m.get("unregistered_payload_schema")
                   else IMPORTED_EVIDENCE_DIGEST),
               "payloadDigest": pd, "sourceCorrespondenceDigest": cd,
               "buildDigest": bd, "producerClosure": imp_prov,
               "adapterClosure": imp_adapt,
               "blobs": [{"path": "coverage/v8.json",
                          "sha256": raw_sha256(raw_artifact),
                          "bytes": len(raw_artifact)}],
               "scopeDigest": sd, "observationDigest": od,
               "completeness": "partial",
               "omissions": ["stdout-not-captured"]}
    if m.get("incomplete_without_omissions"):
        wrapper["omissions"] = []
    if m.get("adapter_closure_is_provider"):
        wrapper["adapterClosure"] = prov_cid
    import_hex = fx.hid("import", wrapper, "identity", "#/$defs/import", "import2")
    import_id = "import2:" + import_hex

    A.seal_plan([prov_cid, eval_cid, tool_cid, std_cid], import_ids=[import_id])
    facts = [A.add_fact("file", "enumerated", uni_hex, uni_hex, prov_cid,
                        {"path": p, "contentSha256": r["sha256"],
                         "byteLength": r["bytes"]}, [])
             for p, r in sorted(inv.items())]
    s_file, h_file = A.add_scope("file", "enumerated", uni_hex, uni_hex, prov_cid,
                                 sorted(inv))
    c_file = A.add_coverage(s_file, h_file, coverage_entry(
        "file", "enumerated", "sha256:" + h_file, len(inv), "complete"))
    view = A.seal_view(prov_cid, [s_file], facts, [c_file],
                       [build.RELATION_DOC_DIGEST, build.NATIVE_DOC_DIGEST,
                        IMPORTED_EVIDENCE_DIGEST])
    run_id = A.seal_run(eval_cid, prov_cid, [view])
    A.extra = {"importId": import_id, "wrapper": wrapper, "payload": payload,
               "correspondence": corr, "observation": obs}
    return fx, A, run_id
