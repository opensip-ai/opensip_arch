"""Synthetic host builder for the TypeScript-universe Runs (phase 5: TS with node_modules layout, config dependencies,
ScopeDocumentV1 in analysis-spec, imported runtime payload in the graph; candidate 16 measurement; per-language
hidden/mismatched input controls).

Native evidence and the runtime import are authored as synthetic trusted observations over independently chosen bytes;
evaluator outputs are computed by ref/execinputs.py + ref/evaluator.py. An input MUTATION is applied before evaluation
so the tampered Run is internally consistent and any refusal must come from the owning admission boundary.
Usage: builders/ts_runs.py <variant>[~<mutation>] ...
"""
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output/preserved/pre-s42"
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/builders")

import canonical as K  # noqa: E402
import enumeration as EN  # noqa: E402
import evaluator as EV  # noqa: E402
import execinputs as XI  # noqa: E402
import imports as IM  # noqa: E402
import membership as M  # noqa: E402
import native_ctx as NC  # noqa: E402
import native_facts as NF  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402
import source39 as S39  # noqa: E402
from syntax_runs import closure, ckey, sfx  # noqa: E402

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
NE = "native/native-evidence.schemas.v2.json"
REL = "foundation/relation-payload-schemas.v2.json"
ENUM_DOC = "foundation/enumeration-plan.schema.v1.json"
EMIT_DOC = "foundation/evaluator-emission-plan.schema.v1.json"
PDOC1 = "workflows/schemas/policy-document.schema.json"
IE = "workflows/schemas/imported-evidence.schema.json"
CAP_MANIFEST_ID = "742a997a708fce51c354ab414e2f69fd7425ee4884eb4e19378431ead4506408"

FILES = {
    "package.json": b"{\"name\":\"web\",\"version\":\"1.0.0\",\"type\":\"module\"}\n",
    "package-lock.json": b"{\"name\":\"web\",\"lockfileVersion\":3,\"packages\":{}}\n",
    "tsconfig.base.json": b"{\"compilerOptions\":{\"strict\":true,\"target\":\"es2022\",\"module\":\"node16\",\"moduleResolution\":\"node16\",\"skipLibCheck\":true,\"noEmit\":true,\"lib\":[\"es2022\"],\"outDir\":\"dist\"}}\n",
    "tsconfig.json": b"{\"extends\":\"./tsconfig.base.json\",\"include\":[\"src\"]}\n",
    "src/index.ts": b"import { pad } from \"left-pad\";\nimport { helper } from \"./util\";\nexport function main(): string {\n  return helper(pad(\"x\", 3));\n}\n",
    "src/util.ts": b"export function helper(s: string): string {\n  return s.trim();\n}\nfunction unused(): number {\n  return 1;\n}\n",
    "README.md": b"# web\n",
}
FUNCS = [("src/index.ts", "main", "exported", ["function", "main", "()", "string"]),
         ("src/util.ts", "helper", "exported", ["function", "helper", "(string)", "string"]),
         ("src/util.ts", "unused", "not-exported", ["function", "unused", "()", "number"])]
VARIANTS = {"ts-pass": {"clonesRequired": False, "externalCallSeverity": "note"},
            "ts-fail": {"clonesRequired": False, "externalCallSeverity": "error"},
            "ts-clones-required": {"clonesRequired": True, "externalCallSeverity": "note"}}
# Phase 8 comparison family: one project ("cmp"); each variant changes exactly the axis its name gives. Defaults keep the
# ts-* variants byte-identical.
DEFAULT_PACK = b"{\"pack\":\"cb24.ts-pack\"}\n"
UTIL_EXTRA_CALL = (b"import { pad } from \"left-pad\";\nexport function helper(s: string): string {\n  return pad(s.trim(), 1);\n}\n"
                   b"function unused(): number {\n  return 1;\n}\n")
_CMP = {"clonesRequired": False, "externalCallSeverity": "error", "project": "cmp"}
_ALL_RULES = ["cb24.ts.cold-file", "cb24.ts.disabled", "cb24.ts.exported-importer", "cb24.ts.external-call", "cb24.ts.reachable"]
VARIANTS.update({
    "cmp-base": dict(_CMP),
    "cmp-code": dict(_CMP, extraCall=True),
    "cmp-hidden": dict(_CMP, extraCall=True, ruleOverrides={"cb24.ts.external-call": {"enabled": False}}),
    "cmp-scope": dict(_CMP, scopeInclude=["src/index.ts"]),
    "cmp-policy": dict(_CMP, ruleOverrides={"cb24.ts.disabled": {"enabled": True}}),
    "cmp-waiver": dict(_CMP, waivers=[]),
    "cmp-evidence": dict(_CMP, runtimeUtil="observed-hit"),
    "cmp-gbase": dict(_CMP, ruleOverrides={"cb24.ts.cold-file": {"gate": True}}),
    "cmp-gevidence": dict(_CMP, ruleOverrides={"cb24.ts.cold-file": {"gate": True}}, runtimeUtil="observed-hit"),
    "cmp-gmissing": dict(_CMP, ruleOverrides={"cb24.ts.cold-file": {"gate": True}}, noImport=True),
    "cmp-empty": dict(_CMP, ruleOverrides={r: {"enabled": False} for r in _ALL_RULES}),
    "cmp-code-det2": dict(_CMP, extraCall=True, semanticsMajor=2, detectorPack=b"{\"pack\":\"cb24.ts-pack\",\"semantics\":2}\n", detectorVersion="2.0.0"),
    "cmp-code-detc": dict(_CMP, extraCall=True, detectorPack=b"{\"pack\":\"cb24.ts-pack\",\"semantics\":\"1.1\"}\n", detectorVersion="1.1.0",
                          compatListing=True),
    # source39 absence knowledge: a deterministic work budget exhausts before node evaluation, so no rule proves absence
    "cmp-budget": dict(_CMP, budgetLimit=50),
})
MUTATIONS = {"compiler-version-not-from-manifest", "stdlib-inventory-incomplete", "config-graph-path-outside-snapshot",
             "config-node-kind-wrong", "lockfile-digest-mismatch", "universe-contradicts-context", "layout-entry-missing-bytes",
             "import-stale-snapshot", "import-window-mismatch", "import-kind-payload-mismatch", "import-not-in-grant",
             "hidden-import", "scope-document-duplicate", "pruned-read-nested-node-modules", "pruned-read-vcs-tree",
             "unit-kind-not-mode-projection"}


def span_of(data, needle, start=0):
    i = data.index(needle, start)
    return i, i + len(needle)


def func_span(data, name):
    i = data.index(b"function " + name.encode())
    if data[max(0, i - 7):i] == b"export ":
        i -= 7
    s = data.index(b"{", i)
    depth = 0
    for j in range(s, len(data)):
        if data[j:j + 1] == b"{":
            depth += 1
        elif data[j:j + 1] == b"}":
            depth -= 1
            if depth == 0:
                return i, s, j + 1
    raise ValueError(name)


def build(name):
    variant, _, mut = name.partition("~")
    assert not mut or mut in MUTATIONS, mut
    cfg = VARIANTS[variant]
    files = {**FILES, **({"src/util.ts": UTIL_EXTRA_CALL} if cfg.get("extraCall") else {})}
    # HC-21: identity s3 sourceInventory - bytes the Plan-selected TS context read from its committed node_modules layout are snapshot
    # rows (membership syntax-only / host-ignore-convention) joined to the layout at Run closure; unread pruned material is not.
    if mut != "layout-entry-missing-bytes":
        files["node_modules/left-pad/package.json"] = b"{\"name\":\"left-pad\",\"version\":\"1.3.0\"}\n"
    if mut == "pruned-read-nested-node-modules":
        files["node_modules/left-pad/node_modules/evil/index.js"] = b"module.exports = 1;\n"
    if mut == "pruned-read-vcs-tree":
        files["node_modules/left-pad/.git/config"] = b"[core]\n"
    store = Store()
    for doc in (ID, NE, REL, ENUM_DOC, EMIT_DOC, PDOC1, IE):
        store.put_bytes(KIT.raw[schemas.norm_rel(doc)], f"schema:{doc}")
    inv_rows = [{"path": p, "sha256": store.put_bytes(files[p], f"source:{p}"), "bytes": len(files[p])} for p in sorted(files, key=lambda p: p.encode())]
    inv = {r["path"]: r for r in inv_rows}
    # HC-16: the toolchain closure (normalizationClosure kind toolchain) carries the level specification and its map
    level_spec = b"cb24 L0-verbatim level specification (typescript provider)\n"
    T, _ = closure(store, "toolchain", "cb24-typescript", {
        "bin/tsc.js": b"synthetic tsc\n", "bin/node": b"synthetic node runtime\n",
        "node_modules/typescript/package.json": b"{\"name\":\"typescript\",\"version\":\"5.6.3\"}\n",
        "opensip-interface/normalization/levels/L0-verbatim.spec": level_spec,
        S39.NSL["closureTreePath"]: S39.normalization_map_bytes("cb24-tsc-normalizer", {"L0-verbatim": hashlib.sha256(level_spec).hexdigest()})},
        "5.6.3")
    libs = {"lib/lib.es5.d.ts": b"// es5\n", "lib/lib.es2022.d.ts": b"// es2022\n", "lib/lib.dom.d.ts": b"// dom\n"}
    S, sdesc = closure(store, "stdlib", "cb24-typescript-stdlib", libs, "5.6.3")
    stage_operation = "cb24.derive-ts-view"
    # HC-15: the producer closure registers its stage output schema at the interface tree path
    P, _ = closure(store, "provider", "cb24-ts-provider", {
        "bin/provider": b"synthetic ts provider\n",
        S39.stage_output_tree_path(stage_operation): S39.stage_output_schema_bytes(stage_operation, ["view"], "cb24 typescript view stage output")})
    E, _ = closure(store, "evaluator", "cb24-evaluator3", {"bin/evaluator": b"synthetic evaluator3 identity\n"})
    dfiles = {"rules/pack.json": cfg.get("detectorPack", DEFAULT_PACK)}
    if cfg.get("compatListing"):
        base_d = closure(Store(), "detector", "cb24-ts-pack", {"rules/pack.json": DEFAULT_PACK})[0]
        dfiles[".opensip/detector-compatibility.json"] = K.C({"schemaFamily": "opensip.product.detector-manifest", "schemaMajor": 1,
                                                             "compatibleClosures": [{"closureId": base_d, "semanticsMajor": 1}]})
    D, _ = closure(store, "detector", "cb24-ts-pack", dfiles, cfg.get("detectorVersion", "1.0.0"))
    CP, _ = closure(store, "provider", "cb24-coverage-producer", {"bin/istanbul": b"synthetic coverage producer\n"})
    AD, _ = closure(store, "adapter", "cb24-istanbul-adapter", {"bin/adapter": b"synthetic istanbul adapter\n"})
    tdesc = store.get_frame(sfx(T), {"closure"})[1]
    tree = {r["path"]: r["sha256"] for r in tdesc["tree"]}
    honored = {"allowJs": False, "allowSyntheticDefaultImports": False, "baseUrl": None, "checkJs": False, "customConditions": [],
               "esModuleInterop": False, "jsx": None, "lib": ["es2022"], "module": "node16", "moduleResolution": "node16", "noEmit": True,
               "paths": [], "resolveJsonModule": False, "rootDirs": [], "skipLibCheck": True, "strict": True, "target": "es2022", "types": None}
    lp_bytes = b"{\"name\":\"left-pad\",\"version\":\"1.3.0\"}\n"
    lp_digest = hashlib.sha256(lp_bytes).hexdigest() if mut == "layout-entry-missing-bytes" else store.put_bytes(lp_bytes, "node-modules:left-pad")
    layout = {"schemaVersion": 1, "entries": [{"packageName": "left-pad", "packageVersion": "1.3.0", "installPath": "node_modules/left-pad",
                                               "realPath": "node_modules/left-pad", "contentSha256": lp_digest}]}
    components = sorted([{"component": r["path"].split("/")[-1], "sha256": r["sha256"]} for r in sdesc["tree"]], key=lambda c: c["component"].encode())
    if mut == "stdlib-inventory-incomplete":
        components = [c for c in components if c["component"] != "lib.dom.d.ts"]
    graph_paths = ["tsconfig.base.json", "tsconfig.json"]
    extra_cfg = b"{\"compilerOptions\":{}}\n"
    if mut == "config-graph-path-outside-snapshot":
        graph_paths = ["tsconfig.base.json", "tsconfig.extra.json", "tsconfig.json"]
    ctx = {"schemaVersion": 2, "languageMode": "ts-tsconfig",
           "toolchain": {"compilerName": "typescript", "compilerVersion": "5.6.4" if mut == "compiler-version-not-from-manifest" else "5.6.3",
                         "compilerPackageDigest": tree["node_modules/typescript/package.json"], "typescriptStdlibMerkleRoot": sfx(S),
                         "standardLibraryComponentDigests": components, "libSelection": ["es2022"]},
           "toolClosure": {"closureId": T, "compiler": tree["bin/tsc.js"], "runtime": tree["bin/node"]},
           "configProjection": {"schemaVersion": 2, "ancestorCarrierVerified": True, "environmentSanitized": True, "typeAcquisitionEnabled": False,
                                "executableSelected": False, "honoredOptions": honored,
                                "strippedOptions": [{"option": "outDir", "reason": "emits-output"}], "configGraphPaths": graph_paths},
           "moduleResolutionMode": "node16", "packageModuleType": "module",
           "nodeModulesLayoutDigest": store.put_record(layout, "node-modules-layout"),
           "lockfileIdentity": {"kind": "package-lock", "path": "package-lock.json",
                                "contentSha256": hashlib.sha256(b"other lockfile").hexdigest() if mut == "lockfile-digest-mismatch" else inv["package-lock.json"]["sha256"]}}
    ctx_hex = store.put_frame("native.context.typescript.v2", ctx, "native-context:typescript")
    nodes = [{"path": "tsconfig.base.json", "contentSha256": inv["tsconfig.base.json"]["sha256"], "kind": "tsconfig" if mut == "config-node-kind-wrong" else "other",
              "extendsResolved": []},
             {"path": "tsconfig.json", "contentSha256": inv["tsconfig.json"]["sha256"], "kind": "tsconfig", "extendsResolved": ["tsconfig.base.json"]}]
    if mut == "config-graph-path-outside-snapshot":
        nodes.insert(1, {"path": "tsconfig.extra.json", "contentSha256": hashlib.sha256(extra_cfg).hexdigest(), "kind": "other", "extendsResolved": []})
        nodes[2]["extendsResolved"] = ["tsconfig.base.json", "tsconfig.extra.json"]
    graph = {"schemaVersion": 1, "entryConfigPath": "tsconfig.json", "nodes": nodes}
    uni = {"schemaVersion": 2, "languageMode": "ts-tsconfig", "configOrigin": "tsconfig", "synthesizerVersion": None, "synthesizedOptions": None,
           "packageModuleType": "module", "allowJs": mut == "universe-contradicts-context", "checkJs": False, "jsAdmittedToProgram": False,
           "jsDiagnosticsEnabled": False, "resolutionCompletenessImplied": False, "jsRootFiles": [], "programRootFiles": ["src/index.ts", "src/util.ts"],
           "lockfileKind": "package-lock", "nodeModulesInReadSet": True, "executionCapableResolution": False,
           "tsconfigGraphHash": store.put_record(graph, "tsconfig-graph"), "nativeContextId": "sha256:" + ctx_hex}
    U = store.put_frame("native.semantic-universe.typescript.v2", uni, "native-universe:typescript")
    adm = NC.admit_native_context(store, ctx_hex, inv_rows)
    bound = {U: NC.bind_universe(store, U, {ctx_hex: adm}, inv_rows)}
    inv_bytes = dict(files)
    discovery = M.discover_units(inv_bytes)
    membership = M.assign_membership(inv_bytes, discovery)
    # source41 closure control over the retained record: native U-4b.5 (a ts-tsconfig unit spelled js-program)
    if mut == "unit-kind-not-mode-projection":
        membership = dict(membership, units=[dict(u, unitKind="js-program") if u["languageFamily"] == "tsjs" else u for u in membership["units"]])
    # HC-19: zero-config discovery (Config2 discovery {}), so the retained DISCOVERED unit provenance agrees with the configuration
    scope = M.unit_scope_descriptor(discovery, [], None)
    budget = {"unit": "work-units", "limit": cfg.get("budgetLimit", 1000000)}
    requested = sorted({"calls": True, "clones-fact": cfg["clonesRequired"], "imports": True, "inventory": True, "reachability": True,
                        "syntax": True}.items(), key=lambda t: t[0].encode())
    config = {"analysis": {"profileId": "cb24-explicit", "capabilities": [c for c, _ in requested], "budget": budget},
              "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
    vcs = {"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": store.put_record(inv_rows, "source-inventory")}
    project_id = "prj1-" + hashlib.sha256(b"consumer-b.v24:" + cfg.get("project", variant).encode()).hexdigest()
    snapshot = {"schemaVersion": 2, "projectId": project_id, "sourceInventory": inv_rows,
                "resolvedConfigDigest": store.put_record(config, "configuration"), "scopeDigest": store.put_record(scope, "scope-descriptor"),
                "vcsDigest": store.put_record(vcs, "vcs-observation")}
    snapshot_id = store.put_object("snapshot", snapshot, "snapshot")
    # runtime import
    util_hit = cfg.get("runtimeUtil") == "observed-hit"
    artifact = b"{\"src/index.ts\":{\"s\":{\"0\":5}},\"src/util.ts\":{\"s\":{\"0\":" + (b"3" if util_hit else b"0") + b"}}}\n"
    window = {"startUtc": "2026-09-01T00:00:00Z", "endUtc": "2026-09-08T00:00:00Z"}
    rpayload = {"payloadDomain": "workflow.import-payload.runtime.v1", "format": "istanbul-json", "observationWindow": window,
                "observedPopulation": "test-suite", "mappingGaps": [],
                "subjects": [{"path": "src/index.ts", "observability": "observed-hit", "hits": 5},
                             {"path": "src/util.ts", "observability": "observed-hit" if util_hit else "observable-unhit", "hits": 3 if util_hit else 0}]}
    import_scope = {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": ["src"], "excludedPathPrefixes": []}
    ikind = "history" if mut == "import-kind-payload-mismatch" else "runtime"
    obs_true = {"schemaVersion": 1, "kind": "runtime", "window": window, "population": "test-suite", "selection": None, "revisionRange": None}
    obs_stored = dict(obs_true)
    if mut == "import-window-mismatch":
        obs_stored["window"] = {"startUtc": "2026-09-01T00:00:00Z", "endUtc": "2026-09-09T00:00:00Z"}
    if ikind == "history":
        obs_stored = {"schemaVersion": 1, "kind": "history", "window": None, "population": None, "selection": None, "revisionRange": None}
    corr_snapshot = "snapshot2:" + "e" * 64 if mut == "import-stale-snapshot" else snapshot_id
    wrapper = {"schemaVersion": 2, "kind": ikind, "payloadSchemaDigest": KIT.digest(IE), "payloadDigest": store.put_record(rpayload, "import-payload:runtime"),
               "sourceCorrespondenceDigest": store.put_record({"kind": "exact-snapshot", "snapshotId": corr_snapshot}, "source-correspondence"),
               "buildDigest": store.put_record({"schemaVersion": 1, "buildIdentity": None}, "build-identity"),
               "producerClosure": CP, "adapterClosure": AD,
               "blobs": [{"path": "coverage/coverage-final.json", "sha256": store.put_bytes(artifact, "import-artifact"), "bytes": len(artifact)}],
               "scopeDigest": store.put_record(import_scope, "import-scope"),
               "observationDigest": store.put_record(obs_stored, "import-observation"), "completeness": "complete", "omissions": []}
    import_id = store.put_object("import", wrapper, "import:runtime")
    plan_imports = [] if (mut == "hidden-import" or cfg.get("noImport")) else [import_id]
    fpaths = EN.file_extent(membership, scope, ".")
    cells = []
    for cap, req in requested:
        kinds = sorted(EN.KIND_DERIVATION[cap], key=lambda k: k.encode())
        extents = []
        for k in kinds:
            if k == "file":
                paths = fpaths
            elif k == "package":
                named, failed = EN.named_manifests(inv_bytes, fpaths)
                paths = sorted({n["path"] for n in named} | set(failed), key=ckey)
            else:
                paths = EN.symbol_extent(bound[U], fpaths, membership)
            extents.append({"kind": k, "paths": paths})
        cells.append({"capabilityId": cap, "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": req, "kinds": kinds,
                      "programBindings": [{"ordinal": 0, "provenance": "default-unit", "enumerator": {"status": "selected", "closureId": P},
                                           "nativeContextDigest": ctx_hex, "universe": U, "programEntry": "tsconfig.json", "extents": extents}]})
    enum = {"schemaVersion": 1, "snapshotId": snapshot_id, "scopeDigest": K.raw_digest(scope),
            "membershipDigest": store.put_record(membership, "unit-membership"), "cells": cells}

    major = cfg.get("semanticsMajor", 1)

    def ref(rid):
        return {"contributionId": "cb24.ts-pack", "ruleStableId": rid, "semanticsMajor": major, "programDigest": hashlib.sha256(rid.encode()).hexdigest()}
    fp_desc = {"schemaVersion": 2, "ruleStableId": "cb24.ts.reachable", "detectorSemanticsMajor": major,
               "subjectKey": {"language": "typescript", "kind": "symbol", "logicalPath": "src/index.ts", "qualifiedName": "main",
                              "discriminator": hashlib.sha256(K.C(FUNCS[0][3])).hexdigest()}, "relatedSubjectKeys": []}
    main_fingerprint = K.identifier("finding-fingerprint", fp_desc)
    rules = sorted([
        {"ruleId": "cb24.ts.cold-file", "ruleProgramRef": ref("cb24.ts.cold-file"), "enabled": True, "severity": "warning", "gate": False,
         "subjectEnumeration": {"universe": "typescript", "subjectKind": "file", "include": ["src/**"]},
         "emitWhen": {"op": "exists", "relation": "runtime-observation", "minResolution": "observed", "evidence": "runtime",
                      "filters": [{"field": "observability", "cmp": "eq", "value": "observable-unhit"}]},
         "evidenceUse": [{"kind": "runtime", "requirement": "required"}]},
        {"ruleId": "cb24.ts.disabled", "ruleProgramRef": ref("cb24.ts.disabled"), "enabled": False, "severity": "error", "gate": True,
         "subjectEnumeration": {"universe": "typescript", "subjectKind": "file"},
         "emitWhen": {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []}, "evidenceUse": []},
        {"ruleId": "cb24.ts.exported-importer", "ruleProgramRef": ref("cb24.ts.exported-importer"), "enabled": True, "severity": "error", "gate": True,
         "subjectEnumeration": {"universe": "typescript", "subjectKind": "export"},
         "emitWhen": {"op": "exists", "relation": "imports", "minResolution": "resolved-target", "filters": []}, "evidenceUse": []},
        {"ruleId": "cb24.ts.external-call", "ruleProgramRef": ref("cb24.ts.external-call"), "enabled": True, "severity": cfg["externalCallSeverity"],
         "gate": True, "subjectEnumeration": {"universe": "typescript", "subjectKind": "symbol"},
         "emitWhen": {"op": "exists", "relation": "calls", "minResolution": "resolved-callee",
                      "filters": [{"field": "target", "cmp": "prefix", "value": "npm:"}]}, "evidenceUse": [], "messageCode": "external-call"},
        {"ruleId": "cb24.ts.reachable", "ruleProgramRef": ref("cb24.ts.reachable"), "enabled": True, "severity": "warning", "gate": False,
         "subjectEnumeration": {"universe": "typescript", "subjectKind": "symbol"},
         "emitWhen": {"op": "and", "operands": [
             {"op": "exists", "relation": "reachability", "minResolution": "from-resolved-calls", "filters": []},
             {"op": "count-at-most", "relation": "calls", "minResolution": "resolved-callee", "filters": [], "n": 5}]}, "evidenceUse": []},
    ], key=lambda r: r["ruleId"].encode())
    for r in rules:
        r.update(cfg.get("ruleOverrides", {}).get(r["ruleId"], {}))
    policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "warning", "rules": rules}
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": cfg.get("waivers", [
        {"waiverId": "cb24.w-main-reachable", "target": {"fingerprint": main_fingerprint}, "reason": "synthetic fingerprint waiver", "expires": None}])}
    scope_doc = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": cfg.get("scopeInclude", ["src/**"]), "exclude": []}
    policy_digest = store.put_record(policy, "policy")
    emission = {"schemaVersion": 1, "policyDigest": policy_digest, "rules": [
        {"ruleId": r["ruleId"], "contributionId": "cb24.ts-pack", "ruleStableId": r["ruleId"], "semanticsMajor": major, "detectorClosure": D,
         "stabilityClass": "path-stable", "emissionProfile": "declarative-subject-v1"} for r in rules]}
    params = [{"schemaDigest": KIT.digest(ENUM_DOC), "payloadDigest": store.put_record(enum, "enumeration-plan")},
              {"schemaDigest": KIT.digest(EMIT_DOC), "payloadDigest": store.put_record(emission, "emission-plan")},
              {"schemaDigest": KIT.digest(PDOC1), "payloadDigest": store.put_record(scope_doc, "scope-document")}]
    if mut == "scope-document-duplicate":
        params.append({"schemaDigest": KIT.digest(PDOC1), "payloadDigest": store.put_record(dict(scope_doc, exclude=["src/util.ts"]), "scope-document-2")})
    spec = {"schemaVersion": 2,
            "requestedCapabilities": sorted([{"capabilityId": c, "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": r} for c, r in requested], key=ckey),
            "policyPackIds": [], "parameters": sorted(params, key=ckey)}
    ops = ["native-analysis", "read-import", "read-source"] if (plan_imports and mut != "import-not-in-grant") else ["native-analysis", "read-source"]
    grant = {"schemaVersion": 2, "projectId": project_id, "principals": [{"kind": "first-party", "closureId": P, "ownerSourceDigest": None}],
             "analysisOperations": ops, "scopeDigest": K.raw_digest(scope)}
    vec = json.load(open(OUT + "/vectors/capability-manifests.json"))
    cm = next(p for p in vec["positives"] if p.get("admission", {}).get("capabilityManifestId") == CAP_MANIFEST_ID)
    plan = {"schemaVersion": 2, "snapshotId": snapshot_id, "capabilityManifestId": CAP_MANIFEST_ID,
            "semanticClosures": sorted([P, E, D], key=ckey), "analysisSpecDigest": store.put_record(spec, "analysis-spec"),
            "resolvedConfigDigest": snapshot["resolvedConfigDigest"], "nativeContextDigests": [ctx_hex], "importIds": plan_imports,
            "policyDigest": policy_digest, "waiverDigest": store.put_record(waivers, "waivers"), "scopeDigest": snapshot["scopeDigest"],
            "budget": budget, "semanticGrantDigest": store.put_record(grant, "semantic-grant"),
            "capabilityManifestBytesDigest": store.put_bytes(bytes.fromhex(cm["admission"]["committedBytesHex"]), "capability-manifest-bytes")}
    plan_id = store.put_object("plan", plan, "plan")
    # HC-15b (own builder error in the first corrected build, logs/s39-hc-build.4.from_scratch.log): outputSchemaDigest is the raw
    # SHA-256 of the member the producer closure registers, not the native bundle digest
    registered = next(r["sha256"] for r in store.get_frame(sfx(P), {"closure"})[1]["tree"] if r["path"] == S39.stage_output_tree_path(stage_operation))
    stage_spec = {"schemaVersion": 2, "planId": plan_id, "producerClosure": P, "operation": stage_operation, "parameters": [],
                  "outputDomains": ["view"], "outputSchemaDigest": registered}
    ss = store.put_record(stage_spec, "stage-spec:0")
    exec_plan_id = store.put_object("execution-plan", {"schemaVersion": 2, "planId": plan_id,
                                                       "stages": [{"ordinal": 0, "stageSpecDigest": ss, "requires": [], "outputDomains": ["view"]}]}, "execution-plan")
    facts, payloads = {}, {}

    def fact(rel, rung, payload, anchors):
        desc = {"schemaVersion": 2, "snapshotId": snapshot_id, "relation": rel, "resolution": rung, "sourceUniverse": U, "targetUniverse": U,
                "producerClosure": P, "payloadSchemaDigest": KIT.digest(REL), "payloadDigest": store.put_record(payload, f"fact-payload:{rel}"),
                "anchors": sorted(anchors, key=ckey), "confidenceMillionths": 1000000}
        fid = store.put_object("fact", desc, f"fact:{rel}")
        facts[fid], payloads[fid] = desc, payload

    def anchor(path, s, e):
        return {"path": path, "blobDigest": inv[path]["sha256"], "startByte": s, "endByte": e}

    # HC-21: file facts cover the first-party file extent; a read row inside a pruned tree is a snapshot input, not a file subject
    for r in inv_rows:
        if r["path"] in fpaths:
            fact("file", "enumerated", {"path": r["path"], "contentSha256": r["sha256"], "byteLength": r["bytes"]}, [])
    fact("package", "manifest-declared", {"packageName": "web", "packageVersion": "1.0.0", "manifestPath": "package.json"}, [])
    idx, utl = files["src/index.ts"], files["src/util.ts"]
    code_paths = ["src/index.ts", "src/util.ts"]
    sym_ids = [f"ts:{p}" for p in code_paths] + [f"ts:{p}#{n}" for p, n, _, _ in FUNCS]
    for p in code_paths:
        fact("declares", "syntactic", {"container": f"file:{p}", "declared": f"ts:{p}", "declarationKind": "module"}, [anchor(p, 0, len(files[p]))])
    lvl = store.put_bytes(b"cb24 L0-verbatim level specification (typescript provider)\n", "level-spec:L0")
    for p, n, _, _ in FUNCS:
        d, s0, e0 = func_span(files[p], n)
        fact("declares", "syntactic", {"container": f"ts:{p}", "declared": f"ts:{p}#{n}", "declarationKind": "function"}, [anchor(p, d, e0)])
        blv, lang, refusal = NC.body_language_version(bound[U], p)
        assert refusal is None, refusal
        frame = NF.build_body_frame("L0-verbatim", lvl, lang, blv, NF.l0_payload(files[p][s0:e0]))
        fact("clones", "normalized-body-hash", {"bodyIdentity": "sha256:" + store.put_bytes(frame, f"body-frame:{p}#{n}"),
                                                "normalisationLevel": "L0-verbatim", "normalisationVersion": lvl}, [anchor(p, s0, e0)])
        r0 = files[p].index(b"return", s0)
        fact("control-flow", "syntactic", {"from": f"ts:{p}#{n}", "to": f"ts:{p}#{n}", "edgeKind": "return"}, [anchor(p, r0, files[p].index(b";", r0) + 1)])
    fact("imports", "resolved-target", {"importer": "ts:src/index.ts", "specifier": "left-pad", "resolvedTarget": "npm:left-pad@1.3.0"},
         [anchor("src/index.ts", *span_of(idx, b"import { pad } from \"left-pad\";"))])
    fact("imports", "resolved-target", {"importer": "ts:src/index.ts", "specifier": "./util", "resolvedTarget": "ts:src/util.ts"},
         [anchor("src/index.ts", *span_of(idx, b"import { helper } from \"./util\";"))])
    fact("calls", "resolved-callee", {"caller": "ts:src/index.ts#main", "calleeText": "helper", "resolvedCallee": "ts:src/util.ts#helper"},
         [anchor("src/index.ts", *span_of(idx, b"helper(pad("))])
    fact("calls", "resolved-callee", {"caller": "ts:src/index.ts#main", "calleeText": "pad", "resolvedCallee": "npm:left-pad@1.3.0#pad"},
         [anchor("src/index.ts", *span_of(idx, b"pad(\"x\", 3)"))])
    if cfg.get("extraCall"):
        fact("imports", "resolved-target", {"importer": "ts:src/util.ts", "specifier": "left-pad", "resolvedTarget": "npm:left-pad@1.3.0"},
             [anchor("src/util.ts", *span_of(utl, b"import { pad } from \"left-pad\";"))])
        fact("calls", "resolved-callee", {"caller": "ts:src/util.ts#helper", "calleeText": "pad", "resolvedCallee": "npm:left-pad@1.3.0#pad"},
             [anchor("src/util.ts", *span_of(utl, b"pad(s.trim(), 1)"))])
    fact("reachability", "from-resolved-calls", {"origin": "ts:src/index.ts#main", "reachable": "ts:src/util.ts#helper"},
         [anchor("src/index.ts", *span_of(idx, b"helper(pad("))])
    fact("literal", "syntactic", {"owner": "ts:src/index.ts#main", "literalKind": "string", "valueText": "x"}, [anchor("src/index.ts", *span_of(idx, b"\"x\""))])
    fact("literal", "syntactic", {"owner": "ts:src/index.ts#main", "literalKind": "number", "valueText": "3"}, [anchor("src/index.ts", *span_of(idx, b"3)"))])
    fact("literal", "syntactic", {"owner": "ts:src/util.ts#unused", "literalKind": "number", "valueText": "1"}, [anchor("src/util.ts", *span_of(utl, b"1;"))])
    scopes, coverages = {}, {}
    closed = {"deadCodeRepairEligible": False, "dynamicDispatch": "resolved", "entryPointsRecognized": "all", "exportsClosed": "closed",
              "externalConsumers": "none-declared", "nonliteralLoading": "none", "reasons": []}

    def scope_cov(rel, rung, subjects, complete=True, deficiency=None, cause=None):
        sd = {"schemaVersion": 2, "snapshotId": snapshot_id, "sourceUniverse": U, "targetUniverse": U, "relation": rel, "resolution": rung,
              "enumeratorClosure": P, "subjects": sorted(set(subjects), key=ckey)}
        sid = store.put_object("subject-scope", sd, f"scope:{rel}")
        resolved = rung in NF.RESOLVED
        rc = ({"state": "complete", "attempted": True, "examinedExhaustive": True, "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
              if resolved else {"state": "not-applicable", "attempted": False, "examinedExhaustive": complete,
                                "stageTerminal": "complete" if complete else None, "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []})
        entry = {"relation": rel, "resolution": rung, "coverage": "complete" if complete else "unknown",
                 "examinedUniverse": {"subjectScopeCommitment": "sha256:" + sfx(sid), "subjectCount": len(sd["subjects"])},
                 "resolutionCompleteness": rc, "closedWorld": closed, "derivationKinds": [], "confidenceMillionths": 1000000,
                 "deficiency": deficiency, "nativeCause": cause}
        payload = {"schemaVersion": 3, "key": {"relation": rel, "resolution": rung, "sourceUniverse": U, "targetUniverse": U,
                                               "subjectScopeCommitment": "sha256:" + sfx(sid)}, "entry": entry}
        cd = {"schemaVersion": 2, "scopeId": sid, "payloadSchemaDigest": KIT.digest(NE), "payloadDigest": store.put_record(payload, f"coverage-payload:{rel}")}
        cid = store.put_object("coverage", cd, f"coverage:{rel}")
        scopes[sid], coverages[cid] = sd, (cd, payload)

    scope_cov("file", "enumerated", fpaths)
    scope_cov("package", "manifest-declared", ["web"])
    for rel in ("declares", "literal", "control-flow"):
        scope_cov(rel, "syntactic", sym_ids)
    scope_cov("imports", "resolved-target", sym_ids)
    scope_cov("calls", "resolved-callee", sym_ids)
    scope_cov("reachability", "from-resolved-calls", sym_ids)
    # HC-14/HC-17: bodyEligibilityLaw.census - configuration and data files stay inventoried and are owed no clones partition, so the
    # default Run returns one complete partition over the eligible paths. The original disclosed partition over package.json,
    # tsconfig and README is preserved in preserved/s39-original/builders/ts_runs.py.
    scope_cov("clones", "normalized-body-hash", [p for p in fpaths if S39.body_eligible("native.semantic-universe.typescript.v2", p)])
    view = {"schemaVersion": 2, "planId": plan_id, "scopeIds": sorted(scopes, key=ckey), "facts": sorted(facts, key=ckey),
            "coverageIds": sorted(coverages, key=ckey), "producerClosure": P, "schemaDigests": sorted([KIT.digest(REL), KIT.digest(NE)], key=ckey)}
    view_id = store.put_object("view", view, "view")
    param_digest = K.raw_digest(enum)
    sym_rows = [{"nativeSubjectId": f"ts:{p}", "kind": "symbol", "path": p, "qualifiedName": p, "subjectLanguage": "typescript", "exported": "not-exported",
                 "signatureTokens": ["module", p], "projections": [{"closureId": D, "signatureTokens": ["module", p]}]} for p in code_paths]
    sym_rows += [{"nativeSubjectId": f"ts:{p}#{n}", "kind": "symbol", "path": p, "qualifiedName": n, "subjectLanguage": "typescript", "exported": ex,
                  "signatureTokens": t, "projections": [{"closureId": D, "signatureTokens": t}]} for p, n, ex, t in FUNCS]
    inventories = []
    for ci, cell in enumerate(cells):
        for k in cell["kinds"]:
            ext = next(e["paths"] for e in cell["programBindings"][0]["extents"] if e["kind"] == k)
            if k == "file":
                rows = [{"nativeSubjectId": p, "kind": "file", "path": p, "qualifiedName": p, "subjectLanguage": EN.subject_language(p),
                         "signatureTokens": [], "projections": []} for p in ext]
            elif k == "package":
                rows = [{"nativeSubjectId": "web", "kind": "package", "path": "package.json", "qualifiedName": "web", "subjectLanguage": "json",
                         "signatureTokens": [], "projections": []}]
            else:
                rows = [r for r in sym_rows if r["path"] in ext]
            record = {"schemaVersion": 1, "planId": plan_id, "parameterDigest": param_digest, "cellOrdinal": ci, "programOrdinal": 0, "kind": k,
                      "state": "complete", "deficiency": None, "nativeCause": None, "examinedPaths": ext,
                      "rows": sorted(rows, key=lambda r: (r["nativeSubjectId"].encode(), r["path"].encode()))}
            inventories.append((store.put_record(record, f"subject-inventory:{ci}:{k}"), record))
    closures_desc = {c: store.get_frame(sfx(c), {"closure"})[1] for c in plan["semanticClosures"]}
    efaults, index = EN.admit_enumeration(plan, plan_id, spec, scope, membership, enum, inventories, bound, closures_desc, inv_bytes)
    if index is None:
        raise SystemExit(f"enumeration refused {efaults}")
    im = IM.admit_import(store, import_id, wrapper, plan)
    receipts = [{"ordinal": 0, "stageSpecDigest": ss, "producerClosure": P, "outputDomains": ["view"],
                 "outputRefs": [{"domain": "view", "digest": sfx(view_id)}], "state": "complete", "unavailableReason": None}]
    # HC-42 (builder): the synthetic host capture observes each row's s3-attributed views, not the one view on every row
    attributed = XI.attribution_map(enum, receipts, {view_id: view}, scopes)
    observations = {(ci, 0): {"viewDigests": attributed[(ci, 0)], "stageOrdinal": 0, "candidateResultDigest": None} for ci in range(len(cells))}
    ctx_x = {"enum_index": index, "views": {view_id: view}, "scopes": scopes, "coverages": coverages, "candidates": {}, "vcs_kind": "none"}
    xi, derived, xfaults = XI.build_record(plan, plan_id, exec_plan_id, E, enum, receipts, observations, ctx_x)
    if mut == "hidden-import":
        xi["selectedRefs"] = XI.cset(xi["selectedRefs"] + [{"domain": "import", "digest": sfx(import_id)}])
    xi_digest = store.put_record(xi, "execution-inputs")
    flags = im["flags"] or {"consumable": True, "staleness": "current"}
    imap = {import_id: wrapper} if plan_imports else {}
    inp = EV.Inputs(plan=plan, plan_id=plan_id, exec_plan_id=exec_plan_id, evaluator_closure=E, policy=policy, waivers=waivers, emission=emission,
                    enum_plan=enum, inventories=index["inventories"], views={view_id: view}, scopes=scopes, coverages=coverages, facts=facts,
                    fact_payloads=payloads, bound=bound, imports=imap, import_payloads={i: rpayload for i in imap},
                    import_observations={i: (obs_true if ikind == "runtime" else obs_stored) for i in imap}, import_scopes={i: import_scope for i in imap},
                    import_flags={i: flags for i in imap}, exec_inputs=xi, exec_inputs_digest=xi_digest,
                    required_rows=derived["requiredRows"], scope_document=scope_doc, project_id=project_id)
    out = EV.evaluate(inp)
    for d, b in out["blobs"].items():
        assert store.put_bytes(b, "evaluator-output") == d
    for ident, (dom, desc) in out["objects"].items():
        assert store.put_object(dom, desc, f"output:{dom}") == ident
    os.makedirs(OUT + "/runs", exist_ok=True)
    store_path = f"{OUT}/runs/{name}.store.json"
    with open(store_path, "w") as fh:
        json.dump(store.export({"runId": out["runId"], "variant": name}), fh, sort_keys=True)
    proof = out["proof"]
    summary = {"variant": name, "mutation": mut or None, "runId": out["runId"], "planId": plan_id, "executionPlanId": exec_plan_id,
               "verdict": proof["verdict"], "evaluationState": proof["evaluationState"],
               "ruleOutcomes": {r["ruleId"]: r["outcome"] for r in proof["ruleResults"]},
               "findings": [(f["finding"]["ruleId"], f["subjectPath"], f["finding"]["correspondence"]["state"]) for f in out["findings"]],
               "waivedFindingIds": proof["waivedFindingIds"], "mainFingerprint": main_fingerprint,
               "executionDeficiencies": [(d["cause"], d["nativeCause"]) for d in proof["executionDeficiencies"]],
               "cellOutcomes": [(o["capabilityId"], o["required"], o["state"], o["deficiency"], o["nativeCause"]) for o in xi["cellOutcomes"]],
               "builderFaults": {"enumeration": efaults, "executionInputs": xfaults, "import": im["faults"],
                                 "context": adm["refusals"], "universe": bound[U]["faults"]},
               "budget": out["budget"], "storeFile": store_path, "storeFileSha256": hashlib.sha256(open(store_path, "rb").read()).hexdigest()}
    with open(f"{OUT}/runs/{name}.build.json", "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    return summary


if __name__ == "__main__":
    for v in sys.argv[1:] or list(VARIANTS):
        s = build(v)
        print(json.dumps({k: s[k] for k in ("variant", "verdict", "ruleOutcomes", "findings", "executionDeficiencies", "builderFaults")}))
        print("  cells", s["cellOutcomes"], "waived", len(s["waivedFindingIds"]))
