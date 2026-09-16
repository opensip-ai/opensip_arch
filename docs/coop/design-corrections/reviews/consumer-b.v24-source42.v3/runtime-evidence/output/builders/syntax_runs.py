"""Synthetic host builder for the syntax-universe Runs (phase 5 'syntax code' / 'syntax data'; candidate measurements;
input-side controls).

Native evidence (facts, scopes, Coverage, inventories, membership) is authored here as a synthetic trusted provider /
host observation over independently chosen repository bytes. Every evaluator output (execution-input derived fields,
proof, witnesses, findings, evidence, seal, Run) is computed by ref/execinputs.py + ref/evaluator.py from those inputs.
An input MUTATION is applied before evaluation, so the tampered Run is internally consistent (fully re-framed and
re-keyed) and any refusal must come from the owning admission boundary, not a stale hash.
Usage: python3 tools/runref.py builders/syntax_runs.py <variant>[~<mutation>] ...
"""
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v3/output"
sys.path.insert(0, OUT + "/ref")

import canonical as K  # noqa: E402
import enumeration as EN  # noqa: E402
import evaluator as EV  # noqa: E402
import execinputs as XI  # noqa: E402
import membership as M  # noqa: E402
import native_ctx as NC  # noqa: E402
import native_facts as NF  # noqa: E402
import schemas  # noqa: E402
import source39 as S39  # noqa: E402
from store import Store  # noqa: E402

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
NE = "native/native-evidence.schemas.v2.json"
REL = "foundation/relation-payload-schemas.v2.json"
ENUM_DOC = "foundation/enumeration-plan.schema.v1.json"
EMIT_DOC = "foundation/evaluator-emission-plan.schema.v1.json"
SYNTAX_CAP_MANIFEST_ID = "ad250d6faa6af1c2c10268e4293f12e3eaec43bc9116bad2a41fa952bac16f34"

CODE_FILES = {
    "src/a.ts": b"export function add(a: number, b: number): number {\n  return a + b;\n}\n",
    "src/b.ts": b"export function sum(a: number, b: number): number {\n  return a + b;\n}\n",
    "scripts/gen.js": b"function gen() {\n  return 42;\n}\nmodule.exports = gen;\n",
    "tools/run.rs": b"fn main() {\n    println!(\"hi\");\n}\n",
}
DATA_FILES = {"README.md": b"# demo\n", "data/config.json": b"{\"k\":1}\n", "LICENSE": b"MIT\n"}
DATA_ONLY_FILES = {"README.md": b"# data only\n", "conf/app.yaml": b"k: 1\n", "data/x.json": b"[1,2]\n", "LICENSE": b"MIT\n"}
SYMBOLS = [  # path, name, declarationKind, exported, signature tokens
    ("src/a.ts", "add", "function", "exported", ["function", "add", "(number,number)", "number"]),
    ("src/b.ts", "sum", "function", "exported", ["function", "sum", "(number,number)", "number"]),
    ("scripts/gen.js", "gen", "function", "not-exported", ["function", "gen", "()"]),
    ("tools/run.rs", "main", "function", "not-exported", ["fn", "main", "()"]),
]
REQ_CODE = {"clones-fact": True, "imports": False, "inventory": True, "syntax": True}
REQ_DATA = {"clones-fact": False, "imports": False, "inventory": True, "syntax": False}
VARIANTS = {
    "syntax-code": {"files": "code", "clones": "complete", "req": REQ_CODE},
    "syntax-mixed-disclosed": {"files": "mixed", "clones": "split-disclosed", "req": REQ_CODE},
    "syntax-mixed-omitted": {"files": "mixed", "clones": "code-only-scope", "req": REQ_CODE},
    "syntax-mixed-falsecomplete": {"files": "mixed", "clones": "false-complete", "req": REQ_CODE},
    "syntax-data": {"files": "data", "clones": "split-disclosed", "req": REQ_DATA},
}
MUTATIONS = {
    "grammar-version-not-from-manifest", "raw-context-record-as-h", "hidden-selected-coverage", "inventory-file-row-dropped",
    "partition-overlap", "l0-span-mismatch", "membership-reordered", "view-producer-not-selected",
    "stage-output-schema-relation-doc", "explicit-endpoint-source", "clone-level-spec-not-in-grammar", "budget-exhausted",
    "unit-kind-other-family", "unit-root-external-sentinel", "row-view-omitted",
    "second-default-unit-binding", "selected-view-not-on-receipt",
}


def ckey(x):
    return K.C(x)


def sfx(i):
    return i.split(":", 1)[1]


def closure(store, kind, name, files, semver="1.0.0"):
    tree = []
    for path in sorted(files, key=lambda p: p.encode()):
        h = store.put_bytes(files[path], f"closure-tree:{name}:{path}")
        tree.append({"path": path, "sha256": h, "bytes": len(files[path])})
    manifest = K.C({"component": name, "kind": kind, "files": [t["path"] for t in tree]})
    desc = {"schemaVersion": 2, "kind": kind, "manifestDigest": store.put_bytes(manifest, f"closure-manifest:{name}"),
            "tree": tree, "semanticVersion": semver, "protocolMajor": 3, "platform": "any"}
    return store.put_object("closure", desc, f"closure:{name}"), desc


def body_span(data):
    s = data.index(b"{")
    depth = 0
    for i in range(s, len(data)):
        if data[i:i + 1] == b"{":
            depth += 1
        elif data[i:i + 1] == b"}":
            depth -= 1
            if depth == 0:
                return s, i + 1
    raise ValueError("unbalanced")


def build(name):
    variant, _, mut = name.partition("~")
    assert not mut or mut in MUTATIONS, mut
    cfg = VARIANTS[variant]
    store = Store()
    files = {"code": dict(CODE_FILES), "mixed": dict(CODE_FILES, **DATA_FILES), "data": dict(DATA_ONLY_FILES)}[cfg["files"]]
    symbols = [s for s in SYMBOLS if s[0] in files]
    for doc in (ID, NE, REL, ENUM_DOC, EMIT_DOC):
        store.put_bytes(KIT.raw[schemas.norm_rel(doc)], f"schema:{doc}")
    inv_rows = []
    for path in sorted(files, key=lambda p: p.encode()):
        inv_rows.append({"path": path, "sha256": store.put_bytes(files[path], f"source:{path}"), "bytes": len(files[path])})
    inv_bytes = dict(files)
    stage_operation = "cb24.derive-syntax-view"
    # HC-15: the producer closure registers its stage output schema at the interface tree path
    P, _ = closure(store, "provider", "cb24-syntax-provider", {
        "bin/provider": b"synthetic provider executable identity\n",
        S39.stage_output_tree_path(stage_operation): S39.stage_output_schema_bytes(stage_operation, ["view"], "cb24 syntax view stage output")})
    E, _ = closure(store, "evaluator", "cb24-evaluator3", {"bin/evaluator": b"synthetic evaluator3 identity\n"})
    D, _ = closure(store, "detector", "cb24-syntax-pack", {"rules/pack.json": b"{\"pack\":\"cb24.syntax-pack\"}\n"})
    P_UNSELECTED, _ = closure(store, "provider", "cb24-other-provider", {"bin/other": b"another provider\n"})
    level_specs = {"L0-verbatim": b"cb24 L0-verbatim level specification: u32be raw span\n",
                   "L1-lexical": b"cb24 L1-lexical level specification: token kinds keyword identifier operator punct literal\n"}
    gfiles = {"bundle.json": b"{\"bundle\":\"cb24-grammars\",\"version\":\"1.0.0\"}\n", "normalizer/spec.txt": b"cb24 normalizer specification v1\n"}
    for lvl, b in level_specs.items():
        if not (mut == "clone-level-spec-not-in-grammar" and lvl == "L0-verbatim"):
            gfiles[f"levels/{lvl}.spec"] = b
        store.put_bytes(b, f"level-spec:{lvl}")
    # HC-16: the grammar closure (languageVersionBinding.normalizationClosure kind grammar) carries the level map
    gfiles[S39.NSL["closureTreePath"]] = S39.normalization_map_bytes("cb24-normalizer", {lvl: hashlib.sha256(b).hexdigest() for lvl, b in level_specs.items()})
    grammars = []
    for lang, row in sorted(NF.GRAMMARS.items()):
        gb = K.C({"grammar": lang, "suffixes": row["suffixes"], "class": row["syntaxClass"]})
        gfiles[f"grammars/{lang}.grammar"] = gb
        grammars.append({"grammarId": f"cb24-{lang}", "grammarVersion": "1.0.0", "languageId": lang,
                         "suffixes": sorted(row["suffixes"], key=lambda s: s.encode()), "syntaxClass": row["syntaxClass"],
                         "grammarDigest": hashlib.sha256(gb).hexdigest()})
    G, _ = closure(store, "grammar", "cb24-grammars", gfiles, "1.0.0")
    level_hex = {lvl: hashlib.sha256(b).hexdigest() for lvl, b in level_specs.items()}
    ctx = {"schemaVersion": 2, "grammarBundle": {
        "schemaVersion": 1, "closureId": G, "parserName": "cb24-grammar-parser",
        "parserVersion": "1.0.1" if mut == "grammar-version-not-from-manifest" else "1.0.0",
        "bundleDigest": hashlib.sha256(gfiles["bundle.json"]).hexdigest(),
        "grammars": sorted(grammars, key=lambda g: g["grammarId"].encode()),
        "normalizer": {"normalizerId": "cb24-normalizer", "normalizerVersion": "1",
                       "specificationDigest": hashlib.sha256(gfiles["normalizer/spec.txt"]).hexdigest()}}}
    ctx_hex = store.put_frame("native.context.syntax.v2", ctx, "native-context:syntax")
    ctx_ref = store.put_record(ctx, "native-context-as-record") if mut == "raw-context-record-as-h" else ctx_hex
    uni = {"schemaVersion": 2, "nativeContextId": "sha256:" + ctx_hex,
           "selectedGrammarIds": sorted((g["grammarId"] for g in grammars), key=lambda s: s.encode()), "resolutionAttempted": False}
    U = store.put_frame("native.semantic-universe.syntax.v2", uni, "native-universe:syntax")
    adm = NC.admit_native_context(store, ctx_hex, inv_rows)
    bound = {U: NC.bind_universe(store, U, {ctx_hex: adm}, inv_rows)}
    discovery = M.discover_units(inv_bytes)
    membership = M.assign_membership(inv_bytes, discovery)
    if mut == "membership-reordered":
        membership = dict(membership, rows=list(reversed(membership["rows"])))
    # source41 closure controls over the retained record: native U-4b.5 (kind of another family) and U-0 (external sentinel as root)
    if mut == "unit-kind-other-family":
        membership = dict(membership, units=[dict(membership["units"][0], unitKind="ts-program")] + membership["units"][1:])
    if mut == "unit-root-external-sentinel":
        membership = dict(membership, units=[dict(membership["units"][0], rootPath=".")] + membership["units"][1:])
    # HC-19: zero-config discovery (Config2 discovery {}) over a repository with no rust/tsjs unit is the U-9 syntax-only fallback
    # (one DEFAULTED unit at the project root, scope workspaceRoots ["."]); an explicit "." root without a marker would refuse instead.
    scope = M.unit_scope_descriptor(discovery, [], None)
    budget = {"unit": "work-units", "limit": 50 if mut == "budget-exhausted" else 1000000}
    requested = sorted(cfg["req"].items(), key=lambda t: t[0].encode())
    config = {"analysis": {"profileId": "cb24-explicit", "capabilities": [c for c, _ in requested], "budget": budget},
              "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
    vcs = {"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": store.put_record(inv_rows, "source-inventory")}
    project_id = "prj1-" + hashlib.sha256(b"consumer-b.v24:" + variant.encode()).hexdigest()
    snapshot = {"schemaVersion": 2, "projectId": project_id, "sourceInventory": inv_rows,
                "resolvedConfigDigest": store.put_record(config, "configuration"), "scopeDigest": store.put_record(scope, "scope-descriptor"),
                "vcsDigest": store.put_record(vcs, "vcs-observation")}
    snapshot_id = store.put_object("snapshot", snapshot, "snapshot")
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
        cells.append({"capabilityId": cap, "languageMode": "syntax-only", "workspaceRoot": ".", "required": req, "kinds": kinds,
                      "programBindings": [{"ordinal": 0, "provenance": "default-unit",  # HC-47: the U-9 fallback default (contract s1 line 21)
                                           "enumerator": {"status": "selected", "closureId": P}, "nativeContextDigest": ctx_ref,
                                           "universe": U, "programEntry": None, "extents": extents}]})
        # source42 closure control (enumeration contract s1 lines 20-21): a second default-unit binding in the first cell
        if mut == "second-default-unit-binding" and len(cells) == 1:
            cells[0]["programBindings"].append(dict(cells[0]["programBindings"][0], ordinal=1))
    enum = {"schemaVersion": 1, "snapshotId": snapshot_id, "scopeDigest": K.raw_digest(scope),
            "membershipDigest": store.put_record(membership, "unit-membership"), "cells": cells}

    def ref(rid):
        return {"contributionId": "cb24.syntax-pack", "ruleStableId": rid, "semanticsMajor": 1, "programDigest": hashlib.sha256(rid.encode()).hexdigest()}
    clones_atom = {"op": "exists", "relation": "clones", "minResolution": "normalized-body-hash", "filters": []}
    if mut == "explicit-endpoint-source":
        clones_atom = dict(clones_atom, endpoint="source")
    rules = [
        {"ruleId": "cb24.clone-body-present", "ruleProgramRef": ref("cb24.clone-body-present"), "enabled": True, "severity": "warning",
         "gate": False, "subjectEnumeration": {"universe": "syntax", "subjectKind": "file", "include": ["src/**"]},
         "emitWhen": clones_atom, "evidenceUse": [], "messageCode": "clone-body-present"},
        {"ruleId": "cb24.disabled-rule", "ruleProgramRef": ref("cb24.disabled-rule"), "enabled": False, "severity": "note", "gate": False,
         "subjectEnumeration": {"universe": "syntax", "subjectKind": "file"},
         "emitWhen": {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []}, "evidenceUse": []},
        {"ruleId": "cb24.forbidden-symbol", "ruleProgramRef": ref("cb24.forbidden-symbol"), "enabled": True, "severity": "error", "gate": True,
         "subjectEnumeration": {"universe": "syntax", "subjectKind": "symbol"},
         "emitWhen": {"op": "exists", "relation": "declares", "minResolution": "syntactic",
                      "filters": [{"field": "subject", "cmp": "glob", "value": "**/*#forbidden*"}]}, "evidenceUse": []},
        {"ruleId": "cb24.tool-without-body", "ruleProgramRef": ref("cb24.tool-without-body"), "enabled": True, "severity": "error", "gate": True,
         "subjectEnumeration": {"universe": "syntax", "subjectKind": "file"},
         "emitWhen": {"op": "and", "operands": [
             {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": [{"field": "subject", "cmp": "glob", "value": "tools/**"}]},
             {"op": "not", "operand": {"op": "exists", "relation": "clones", "minResolution": "normalized-body-hash", "filters": []}}]},
         "evidenceUse": []},
    ]
    policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "warning", "rules": rules}
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": [
        {"waiverId": "cb24.w-b-clone", "target": {"ruleId": "cb24.clone-body-present", "subjectPath": "src/b.ts"},
         "reason": "synthetic waiver control", "expires": None}]}
    policy_digest = store.put_record(policy, "policy")
    emission = {"schemaVersion": 1, "policyDigest": policy_digest, "rules": [
        {"ruleId": r["ruleId"], "contributionId": "cb24.syntax-pack", "ruleStableId": r["ruleId"], "semanticsMajor": 1,
         "detectorClosure": D, "stabilityClass": "path-stable", "emissionProfile": "declarative-subject-v1"} for r in rules]}
    spec = {"schemaVersion": 2,
            "requestedCapabilities": sorted([{"capabilityId": c, "languageMode": "syntax-only", "workspaceRoot": ".", "required": r}
                                             for c, r in requested], key=ckey),
            "policyPackIds": [],
            "parameters": sorted([{"schemaDigest": KIT.digest(ENUM_DOC), "payloadDigest": store.put_record(enum, "enumeration-plan")},
                                  {"schemaDigest": KIT.digest(EMIT_DOC), "payloadDigest": store.put_record(emission, "emission-plan")}], key=ckey)}
    grant = {"schemaVersion": 2, "projectId": project_id, "principals": [{"kind": "first-party", "closureId": P, "ownerSourceDigest": None}],
             "analysisOperations": ["native-analysis", "read-source"], "scopeDigest": K.raw_digest(scope)}
    vec = json.load(open(OUT + "/vectors/capability-manifests.json"))
    cm = next(p for p in vec["positives"] if p.get("admission", {}).get("capabilityManifestId") == SYNTAX_CAP_MANIFEST_ID)
    cm_bytes = bytes.fromhex(cm["admission"]["committedBytesHex"])
    plan = {"schemaVersion": 2, "snapshotId": snapshot_id, "capabilityManifestId": SYNTAX_CAP_MANIFEST_ID,
            "semanticClosures": sorted([P, E, D], key=ckey), "analysisSpecDigest": store.put_record(spec, "analysis-spec"),
            "resolvedConfigDigest": snapshot["resolvedConfigDigest"], "nativeContextDigests": [ctx_ref], "importIds": [],
            "policyDigest": policy_digest, "waiverDigest": store.put_record(waivers, "waivers"), "scopeDigest": snapshot["scopeDigest"],
            "budget": budget, "semanticGrantDigest": store.put_record(grant, "semantic-grant"),
            "capabilityManifestBytesDigest": store.put_bytes(cm_bytes, "capability-manifest-bytes")}
    plan_id = store.put_object("plan", plan, "plan")
    # HC-15b (own builder error in the first corrected build, logs/s39-hc-build.4.from_scratch.log): outputSchemaDigest is the raw
    # SHA-256 of the member the producer closure registers; the mutation still names another retained document's bytes
    registered = next(r["sha256"] for r in store.get_frame(sfx(P), {"closure"})[1]["tree"] if r["path"] == S39.stage_output_tree_path(stage_operation))
    stage_spec = {"schemaVersion": 2, "planId": plan_id, "producerClosure": P, "operation": stage_operation, "parameters": [],
                  "outputDomains": ["view"], "outputSchemaDigest": KIT.digest(REL) if mut == "stage-output-schema-relation-doc" else registered}
    ss = store.put_record(stage_spec, "stage-spec:0")
    exec_plan = {"schemaVersion": 2, "planId": plan_id, "stages": [{"ordinal": 0, "stageSpecDigest": ss, "requires": [], "outputDomains": ["view"]}]}
    exec_plan_id = store.put_object("execution-plan", exec_plan, "execution-plan")
    VP = P_UNSELECTED if mut == "view-producer-not-selected" else P
    facts, payloads = {}, {}

    def fact(rel, rung, payload, anchors):
        pd = store.put_record(payload, f"fact-payload:{rel}")
        desc = {"schemaVersion": 2, "snapshotId": snapshot_id, "relation": rel, "resolution": rung, "sourceUniverse": U, "targetUniverse": U,
                "producerClosure": VP, "payloadSchemaDigest": KIT.digest(REL), "payloadDigest": pd,
                "anchors": sorted(anchors, key=ckey), "confidenceMillionths": 1000000}
        fid = store.put_object("fact", desc, f"fact:{rel}")
        facts[fid], payloads[fid] = desc, payload
        return fid

    blob_of = {r["path"]: r["sha256"] for r in inv_rows}

    def anchor(path, s, e):
        return {"path": path, "blobDigest": blob_of[path], "startByte": s, "endByte": e}

    for row in inv_rows:
        fact("file", "enumerated", {"path": row["path"], "contentSha256": row["sha256"], "byteLength": row["bytes"]}, [])
    sym_ids, clones_code_paths = [], []
    for path, sname, dk, exported, toks in symbols:
        data = files[path]
        s, e = body_span(data)
        sid = f"sym:{path}#{sname}"
        sym_ids.append(sid)
        fact("declares", "syntactic", {"container": f"file:{path}", "declared": sid, "declarationKind": dk}, [anchor(path, 0, e)])
        blv, lang, refusal = NC.body_language_version(bound[U], path)
        assert refusal is None, refusal
        span = data[s + 1:e] if (mut == "l0-span-mismatch" and path == "src/a.ts") else data[s:e]
        frame0 = NF.build_body_frame("L0-verbatim", level_hex["L0-verbatim"], lang, blv, NF.l0_payload(span))
        fact("clones", "normalized-body-hash", {"bodyIdentity": "sha256:" + store.put_bytes(frame0, f"body-frame:L0:{path}"),
                                                "normalisationLevel": "L0-verbatim", "normalisationVersion": level_hex["L0-verbatim"]},
             [anchor(path, s, e)])
        if path.startswith("src/"):
            toks1 = [("keyword", b"return"), ("identifier", b"a"), ("operator", b"+"), ("identifier", b"b"), ("punct", b";")]
            frame1 = NF.build_body_frame("L1-lexical", level_hex["L1-lexical"], lang, blv, NF.l1_payload(toks1))
            fact("clones", "normalized-body-hash", {"bodyIdentity": "sha256:" + store.put_bytes(frame1, f"body-frame:L1:{path}"),
                                                    "normalisationLevel": "L1-lexical", "normalisationVersion": level_hex["L1-lexical"]},
                 [anchor(path, s, e)])
        clones_code_paths.append(path)
        r = data.find(b"return")
        if r >= 0:
            fact("control-flow", "syntactic", {"from": sid, "to": sid, "edgeKind": "return"}, [anchor(path, r, data.index(b";", r) + 1)])
    if "scripts/gen.js" in files:
        g = files["scripts/gen.js"].index(b"42")
        fact("literal", "syntactic", {"owner": "sym:scripts/gen.js#gen", "literalKind": "number", "valueText": "42"}, [anchor("scripts/gen.js", g, g + 2)])
    if "tools/run.rs" in files:
        h = files["tools/run.rs"].index(b"\"hi\"")
        fact("literal", "syntactic", {"owner": "sym:tools/run.rs#main", "literalKind": "string", "valueText": "hi"}, [anchor("tools/run.rs", h, h + 4)])
    scopes, coverages, in_view = {}, {}, set()
    closed_world = {"deadCodeRepairEligible": False, "dynamicDispatch": "not-applicable", "entryPointsRecognized": "none",
                    "exportsClosed": "unknown", "externalConsumers": "unknown", "nonliteralLoading": "none", "reasons": []}

    def scope_cov(rel, rung, subjects, complete=True, deficiency=None, cause=None, view=True):
        sdesc = {"schemaVersion": 2, "snapshotId": snapshot_id, "sourceUniverse": U, "targetUniverse": U, "relation": rel, "resolution": rung,
                 "enumeratorClosure": P, "subjects": sorted(set(subjects), key=ckey)}
        sid = store.put_object("subject-scope", sdesc, f"scope:{rel}")
        entry = {"relation": rel, "resolution": rung, "coverage": "complete" if complete else "unknown",
                 "examinedUniverse": {"subjectScopeCommitment": "sha256:" + sfx(sid), "subjectCount": len(sdesc["subjects"])},
                 "resolutionCompleteness": {"state": "not-applicable", "attempted": False, "examinedExhaustive": complete,
                                            "stageTerminal": "complete" if complete else None, "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []},
                 "closedWorld": closed_world, "derivationKinds": [], "confidenceMillionths": 1000000, "deficiency": deficiency, "nativeCause": cause}
        payload = {"schemaVersion": 3, "key": {"relation": rel, "resolution": rung, "sourceUniverse": U, "targetUniverse": U,
                                               "subjectScopeCommitment": "sha256:" + sfx(sid)}, "entry": entry}
        cdesc = {"schemaVersion": 2, "scopeId": sid, "payloadSchemaDigest": KIT.digest(NE), "payloadDigest": store.put_record(payload, f"coverage-payload:{rel}")}
        cid = store.put_object("coverage", cdesc, f"coverage:{rel}")
        scopes[sid] = sdesc
        coverages[cid] = (cdesc, payload)
        if view:
            in_view.add(sid)
            in_view.add(cid)
        return sid, cid

    lts = ("language-tier-unsupported", "capability-missing")
    scope_cov("file", "enumerated", fpaths)
    scope_cov("package", "manifest-declared", [])
    for rel in ("declares", "literal", "control-flow"):
        if sym_ids:
            scope_cov(rel, "syntactic", sym_ids)
        else:
            scope_cov(rel, "syntactic", [], False, *lts)
    if mut == "partition-overlap":
        scope_cov("declares", "syntactic", sym_ids[:1])
    data_paths = sorted([p for p in fpaths if p not in clones_code_paths], key=ckey)
    if cfg["clones"] == "complete":
        scope_cov("clones", "normalized-body-hash", fpaths)
    elif cfg["clones"] == "split-disclosed":
        if clones_code_paths:
            scope_cov("clones", "normalized-body-hash", clones_code_paths)
        scope_cov("clones", "normalized-body-hash", data_paths, False, *lts)
    elif cfg["clones"] == "code-only-scope":
        scope_cov("clones", "normalized-body-hash", clones_code_paths)
    else:
        scope_cov("clones", "normalized-body-hash", fpaths)
    hidden = scope_cov("file", "enumerated", fpaths[:1], view=False)[1] if mut == "hidden-selected-coverage" else None
    view = {"schemaVersion": 2, "planId": plan_id, "scopeIds": sorted((s for s in scopes if s in in_view), key=ckey), "facts": sorted(facts, key=ckey),
            "coverageIds": sorted((c for c in coverages if c in in_view), key=ckey), "producerClosure": VP,
            "schemaDigests": sorted([KIT.digest(REL), KIT.digest(NE)], key=ckey)}
    view_id = store.put_object("view", view, "view")
    param_digest = K.raw_digest(enum)
    sym_rows = [{"nativeSubjectId": f"sym:{p}#{n}", "kind": "symbol", "path": p, "qualifiedName": n, "subjectLanguage": EN.subject_language(p),
                 "exported": ex, "signatureTokens": t, "projections": [{"closureId": D, "signatureTokens": t}]} for p, n, _, ex, t in symbols]
    inventories = []
    for ci, cell in enumerate(cells):
        for k in cell["kinds"]:
            ext = next(e["paths"] for e in cell["programBindings"][0]["extents"] if e["kind"] == k)
            if k == "file":
                rows = [{"nativeSubjectId": p, "kind": "file", "path": p, "qualifiedName": p, "subjectLanguage": EN.subject_language(p),
                         "signatureTokens": [], "projections": []} for p in ext]
                if mut == "inventory-file-row-dropped" and cell["capabilityId"] == "clones-fact":
                    rows = rows[1:]
            elif k == "symbol":
                rows = [r for r in sym_rows if r["path"] in ext]
            else:
                rows = []
            inv = {"schemaVersion": 1, "planId": plan_id, "parameterDigest": param_digest, "cellOrdinal": ci, "programOrdinal": 0, "kind": k,
                   "state": "complete", "deficiency": None, "nativeCause": None, "examinedPaths": ext,
                   "rows": sorted(rows, key=lambda r: (r["nativeSubjectId"].encode(), r["path"].encode()))}
            inventories.append((store.put_record(inv, f"subject-inventory:{ci}:{k}"), inv))
    closures_desc = {c: store.get_frame(sfx(c), {"closure"})[1] for c in plan["semanticClosures"]}
    efaults, index = EN.admit_enumeration(plan, plan_id, spec, scope, membership, enum, inventories, bound, closures_desc, inv_bytes)
    if index is None:
        raise SystemExit(f"builder enumeration refused: {efaults}")
    receipts = [{"ordinal": 0, "stageSpecDigest": ss, "producerClosure": P, "outputDomains": ["view"],
                 "outputRefs": [{"domain": "view", "digest": sfx(view_id)}], "state": "complete", "unavailableReason": None}]
    # HC-42 (builder): the synthetic host capture observes each row's s3-attributed views, not the one view on every row
    attributed = XI.attribution_map(enum, receipts, {view_id: view}, scopes)
    observations = {(ci, 0): {"viewDigests": attributed[(ci, 0)], "stageOrdinal": 0, "candidateResultDigest": None} for ci in range(len(cells))}
    # HC-50 (own control error, logs/s42-fin-mut.0.replay_all.log): the second default-unit binding needs its own lawful stage observation,
    # otherwise the captured outcome's null stageOrdinal fails the execution-inputs schema first and masks the cardinality law under test
    if mut == "second-default-unit-binding":
        observations[(0, 1)] = {"viewDigests": attributed[(0, 1)], "stageOrdinal": 0, "candidateResultDigest": None}
    ctx_x = {"enum_index": index, "views": {view_id: view}, "scopes": scopes, "coverages": coverages, "candidates": {}, "vcs_kind": "none"}
    xi, derived, xfaults = XI.build_record(plan, plan_id, exec_plan_id, E, enum, receipts, observations, ctx_x)
    if hidden:
        xi["selectedRefs"] = XI.cset(xi["selectedRefs"] + [{"domain": "coverage", "digest": sfx(hidden)}])
    # source41 closure control (execution-inputs s3 view attribution): the retained claim omits the attributed view from the first row.
    # HC-45 (own tool error, logs/s41-post-mut.0.replay_all.log): the first version changed only the builder observation, which
    # build_record re-derives, so the exported store equalled syntax-code and the "control" admitted without testing anything.
    if mut == "row-view-omitted":
        xi["cellOutcomes"][0] = dict(xi["cellOutcomes"][0], viewDigests=[])
    # source42 closure control (execution-inputs s3 line 53): the view stays on selectedRefs and on the rows, but the complete receipt omits it
    if mut == "selected-view-not-on-receipt":
        xi["hostCapture"]["stageReceipts"][0] = dict(xi["hostCapture"]["stageReceipts"][0], outputRefs=[])
    xi_digest = store.put_record(xi, "execution-inputs")
    inp = EV.Inputs(plan=plan, plan_id=plan_id, exec_plan_id=exec_plan_id, evaluator_closure=E, policy=policy, waivers=waivers,
                    emission=emission, enum_plan=enum, inventories=index["inventories"], views={view_id: view}, scopes=scopes,
                    coverages=coverages, facts=facts, fact_payloads=payloads, bound=bound, imports={}, import_payloads={},
                    import_observations={}, import_scopes={}, import_flags={}, exec_inputs=xi, exec_inputs_digest=xi_digest,
                    required_rows=derived["requiredRows"], scope_document=None, project_id=project_id)
    out = EV.evaluate(inp)
    for d, b in out["blobs"].items():
        assert store.put_bytes(b, "evaluator-output") == d
    for ident, (dom, desc) in out["objects"].items():
        assert store.put_object(dom, desc, f"output:{dom}") == ident
    exported = store.export({"runId": out["runId"], "variant": name})
    os.makedirs(OUT + "/runs", exist_ok=True)
    store_path = f"{OUT}/runs/{name}.store.json"
    with open(store_path, "w") as fh:
        json.dump(exported, fh, sort_keys=True)
    summary = {"variant": name, "mutation": mut or None, "runId": out["runId"], "planId": plan_id, "executionPlanId": exec_plan_id,
               "proofId": out["proofId"], "verdict": out["proof"]["verdict"], "evaluationState": out["proof"]["evaluationState"],
               "ruleOutcomes": {r["ruleId"]: r["outcome"] for r in out["proof"]["ruleResults"]},
               "findingIds": out["proof"]["findingIds"], "waivedFindingIds": out["proof"]["waivedFindingIds"],
               "executionDeficiencies": out["proof"]["executionDeficiencies"],
               "cellOutcomes": [{k: o[k] for k in ("cellOrdinal", "capabilityId", "required", "state", "deficiency", "nativeCause")} for o in xi["cellOutcomes"]],
               "builderEnumerationFaults": efaults, "builderExecutionInputFaults": xfaults, "budget": out["budget"],
               "storeFile": store_path, "storeFileSha256": hashlib.sha256(open(store_path, "rb").read()).hexdigest(),
               "blobCount": len(store.blobs), "objectCount": len(store.objects)}
    with open(f"{OUT}/runs/{name}.build.json", "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    return summary


if __name__ == "__main__":
    for v in sys.argv[1:] or list(VARIANTS):
        s = build(v)
        print(json.dumps({k: s[k] for k in ("variant", "verdict", "evaluationState", "ruleOutcomes", "builderEnumerationFaults", "builderExecutionInputFaults")}))
        print("  execDefs", [(d["cause"], d["nativeCause"]) for d in s["executionDeficiencies"]], "exec-plan", s["executionPlanId"][:24])
        print("  cells", [(c["capabilityId"], c["state"], c["deficiency"], c["nativeCause"]) for c in s["cellOutcomes"]])
