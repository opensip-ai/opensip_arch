"""TypeScript/JavaScript Run scenarios (complete minimal positive graphs + negatives)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures as F  # noqa: E402
import graph as G  # noqa: E402
import kit  # noqa: E402
import osip  # noqa: E402

L1_SPEC = b"level-specification L1-lexical: TS/JS lexical boundary rules v1"
L0_ID = "L0-verbatim"
L1_ID = "L1-lexical"

# Bodies used by the clone vectors (SYNTHETIC source bytes).
BODY = b"{\n  return a + b;\n}"
BODY_JS = b"{\n  return a + b;\n}"


def _files_ordinary():
    """An ordinary TypeScript project: package.json, a custom-named project config
    inheriting from multiple ORDERED bases (with a REPEATED base whose precedence
    must be retained), a shared base under another filename, and a lockfile."""
    return {
        "package.json": b'{"name":"app","version":"1.0.0","private":true}',
        "package-lock.json": b'{"lockfileVersion":3}',
        "configs/base.strict.json": b'{"compilerOptions":{"strict":true}}',
        "configs/base.node.json": b'{"compilerOptions":{"module":"node16"}}',
        "configs/app.build.json": (b'{"extends":["./base.strict.json","./base.node.json",'
                                   b'"./base.strict.json"],"compilerOptions":{}}'),
        "src/app.ts": b"export function add(a: number, b: number) " + BODY,
        "src/legacy.js": b"export function add(a, b) " + BODY_JS,
        "README.md": b"# app",
    }


def _config_graph(snap):
    def node(p, kind, edges):
        return {"path": p, "contentSha256": snap["inventory"][p]["sha256"],
                "kind": kind, "extendsResolved": list(edges)}
    nodes = [node("configs/app.build.json", "other",
                  ["configs/base.strict.json", "configs/base.node.json",
                   "configs/base.strict.json"]),
             node("configs/base.node.json", "tsconfig", []),
             node("configs/base.strict.json", "tsconfig", [])]
    nodes.sort(key=lambda n: n["path"])
    return {"schemaVersion": 1, "entryConfigPath": "configs/app.build.json",
            "nodes": nodes}


def _node_modules_layout(store):
    entries = []
    for name, ver, path in [("left-pad", "1.3.0", "node_modules/left-pad"),
                            ("@scope/util", "2.0.1", "node_modules/@scope/util")]:
        manifest = ('{"name":"%s","version":"%s","main":"index.js"}' % (name, ver)).encode()
        entries.append({"packageName": name, "packageVersion": ver,
                        "installPath": path, "realPath": path,
                        "contentSha256": store.put_blob(manifest)})
    entries.sort(key=lambda e: e["installPath"])
    return {"schemaVersion": 1, "entries": entries}


def build(store, mode="ordinary", tamper=None):
    """mode: ordinary | jsconfig | synthesized"""
    out = {"mode": mode, "assumptions": [
        "source bytes, installed package manifests, compiler/stdlib trees and the "
        "provider's enumeration are SYNTHETIC trusted observations, not measurements"]}

    tool = F.ts_toolchain(store)
    std = F.ts_stdlib(store)
    prov = F.provider_closure(store, "typescript-semantic")
    ev = F.evaluator_closure(store)
    rc = F.rule_closure(store)
    closures = {c["hex"]: c for c in (tool, std, prov, ev, rc)}

    files = _files_ordinary()
    if mode == "jsconfig":
        files.pop("configs/app.build.json")
        files["shared/base.common.json"] = b'{"compilerOptions":{"target":"es2022"}}'
        files["jsconfig.json"] = b'{"extends":"./shared/base.common.json"}'
    elif mode == "synthesized":
        for p in list(files):
            if p.startswith("configs/"):
                files.pop(p)
        files.pop("package-lock.json")

    cfg = F.config(["clones", "declares", "file"])
    scope = F.scope(["."], excluded=["node_modules", ".git"])
    snap = G.make_snapshot(store, files, scope, cfg, "git", "c" * 40, False)

    lockfile = None
    if "package-lock.json" in files:
        lockfile = {"kind": "package-lock", "path": "package-lock.json",
                    "contentSha256": snap["inventory"]["package-lock.json"]["sha256"]}

    layout = _node_modules_layout(store) if mode != "synthesized" else None
    layout_digest = osip.canonical_record_digest(layout) if layout else None

    if mode == "ordinary":
        graph_rec = _config_graph(snap)
        language_mode, origin = "js-allowjs", "tsconfig"
        honored = F.ts_honored(["dom", "es2022", "esnext"], True, False)
        synthesized, synth_version = None, None
    elif mode == "jsconfig":
        def node(p, kind, edges):
            return {"path": p, "contentSha256": snap["inventory"][p]["sha256"],
                    "kind": kind, "extendsResolved": list(edges)}
        nodes = sorted([node("jsconfig.json", "jsconfig", ["shared/base.common.json"]),
                        node("shared/base.common.json", "other", []),
                        node("configs/base.node.json", "tsconfig", []),
                        node("configs/base.strict.json", "tsconfig", [])],
                       key=lambda n: n["path"])
        # only reachable nodes may be present
        nodes = [n for n in nodes if n["path"] in
                 ("jsconfig.json", "shared/base.common.json")]
        graph_rec = {"schemaVersion": 1, "entryConfigPath": "jsconfig.json",
                     "nodes": nodes}
        language_mode, origin = "js-allowjs", "jsconfig"
        honored = F.ts_honored(["dom", "es2022", "esnext"], True, False)
        synthesized, synth_version = None, None
    else:
        graph_rec = {"schemaVersion": 1, "entryConfigPath": None, "nodes": []}
        language_mode, origin = "js-synthesized", "synthesized"
        honored = F.ts_honored(["dom", "es2022", "esnext"], True, False,
                               module_res="node16")
        honored["strict"] = False
        synthesized = {"allowJs": True, "checkJs": False, "module": "node16",
                       "moduleResolution": "node16", "target": "es2022",
                       "strict": False, "skipLibCheck": True, "types": [],
                       "noEmit": True}
        synth_version = 1

    cfg_paths = [n["path"] for n in graph_rec["nodes"]]
    ctx = F.ts_context(store, tool, std, cfg_paths, language_mode, honored,
                       layout_digest, lockfile)
    if tamper == "context-stdlib-root-not-retained":
        bad = dict(ctx["descriptor"])
        bad["toolchain"] = dict(bad["toolchain"])
        bad["toolchain"]["typescriptStdlibMerkleRoot"] = "f" * 64
        ctx = G.mint_context(store, G.TS_CONTEXT_DOMAIN, bad)
    if tamper == "context-compiler-version-not-from-manifest":
        bad = dict(ctx["descriptor"])
        bad["toolchain"] = dict(bad["toolchain"])
        bad["toolchain"]["compilerVersion"] = "9.9.9"
        ctx = G.mint_context(store, G.TS_CONTEXT_DOMAIN, bad)
    if tamper == "context-config-graph-path-outside-snapshot":
        bad = dict(ctx["descriptor"])
        bad["configProjection"] = dict(bad["configProjection"])
        bad["configProjection"]["configGraphPaths"] = sorted(cfg_paths + ["hidden/x.json"])
        ctx = G.mint_context(store, G.TS_CONTEXT_DOMAIN, bad)
    if tamper == "context-stdlib-inventory-incomplete":
        bad = dict(ctx["descriptor"])
        bad["toolchain"] = dict(bad["toolchain"])
        bad["toolchain"]["standardLibraryComponentDigests"] = \
            bad["toolchain"]["standardLibraryComponentDigests"][:2]
        ctx = G.mint_context(store, G.TS_CONTEXT_DOMAIN, bad)

    retained = {"configGraph": graph_rec, "nodeModulesLayout": layout}
    G.admit_native_context(store, ctx, closures, snap, retained)

    program_roots = sorted(p for p in files if p.endswith((".ts", ".tsx")))
    js_roots = sorted(p for p in files if p.endswith((".js", ".mjs", ".cjs", ".jsx")))
    uni = F.ts_universe(store, ctx, graph_rec, program_roots, js_roots, origin,
                        synthesized, synth_version)
    if tamper == "universe-field-contradicts-context":
        bad = dict(uni["descriptor"])
        bad["checkJs"] = True
        uni = G.mint_universe(store, G.TS_UNIVERSE_DOMAIN, bad)
    if tamper == "rust-context-offered-as-typescript-context":
        rt, rl = F.rust_toolchain(store), F.rust_dev_llvm(store)
        proj = F.cargo_projection(store, [])
        dep = F.dependency_source_set({"path": "Cargo.lock",
                                       "contentSha256": osip.raw_sha256(b"lock"),
                                       "lockfileVersion": 4})
        feats = F.unified_features()
        rctx = F.rust_context(store, rt, rl, proj,
                              "sha256:" + osip.H("native.dependency-source-set.v1", dep),
                              "sha256:" + osip.H("native.unified-features.rust.v1", feats))
        G.bind_universe(store, uni, rctx, None, snap, retained)

    G.bind_universe(store, uni, ctx, None, snap, retained)

    # --- facts ------------------------------------------------------------
    facts, scopes, coverages = [], [], []

    # file fact with inventoried path/hash/length checks
    fp = "src/app.ts"
    inv = snap["inventory"][fp]
    file_payload = {"path": fp, "contentSha256": inv["sha256"], "byteLength": inv["bytes"]}
    if tamper == "file-fact-claims-a-foreign-hash":
        file_payload = dict(file_payload, contentSha256=osip.raw_sha256(b"not these bytes"))
    if tamper == "file-fact-claims-a-path-in-no-snapshot":
        file_payload = {"path": "node_modules/left-pad/index.js",
                        "contentSha256": osip.raw_sha256(b"x"), "byteLength": 1}
    file_fact = G.make_fact(store, snap, "file", "enumerated", uni["hex"], uni["hex"],
                            prov["id"], file_payload,
                            [{"path": file_payload["path"],
                              "blobDigest": snap["inventory"].get(
                                  file_payload["path"], inv)["sha256"],
                              "startByte": 0,
                              "endByte": snap["inventory"].get(
                                  file_payload["path"], inv)["bytes"]}])
    facts.append(file_fact)

    # package fact
    pkg_payload = {"packageName": "app", "packageVersion": "1.0.0",
                   "manifestPath": "package.json"}
    facts.append(G.make_fact(store, snap, "package", "manifest-declared", uni["hex"],
                             uni["hex"], prov["id"], pkg_payload, []))

    # clone facts: a TypeScript body at L0 and at L1, and a JavaScript body
    # produced by the SAME TypeScript engine universe.
    ts_src = files["src/app.ts"]
    ts_start = ts_src.index(b"{")
    ts_anchor = [{"path": "src/app.ts",
                  "blobDigest": snap["inventory"]["src/app.ts"]["sha256"],
                  "startByte": ts_start, "endByte": len(ts_src)}]
    p0, id0, blv0 = G.clone_body_fact_parts(store, uni, ctx, "src/app.ts",
                                            ts_src[ts_start:], L0_ID, L1_SPEC)
    facts.append(G.make_fact(store, snap, "clones", "normalized-body-hash", uni["hex"],
                             uni["hex"], prov["id"], p0, ts_anchor))
    tokens = [("punct", "{"), ("kw", "return"), ("ident", "a"), ("punct", "+"),
              ("ident", "b"), ("punct", ";"), ("punct", "}")]
    p1, id1, _ = G.clone_body_fact_parts(store, uni, ctx, "src/app.ts",
                                         ts_src[ts_start:], L1_ID, L1_SPEC, tokens)
    facts.append(G.make_fact(store, snap, "clones", "normalized-body-hash", uni["hex"],
                             uni["hex"], prov["id"], p1, ts_anchor))

    js_src = files["src/legacy.js"]
    js_start = js_src.index(b"{")
    js_anchor = [{"path": "src/legacy.js",
                  "blobDigest": snap["inventory"]["src/legacy.js"]["sha256"],
                  "startByte": js_start, "endByte": len(js_src)}]
    pjs, idjs, blvjs = G.clone_body_fact_parts(store, uni, ctx, "src/legacy.js",
                                               js_src[js_start:], L0_ID, L1_SPEC)
    facts.append(G.make_fact(store, snap, "clones", "normalized-body-hash", uni["hex"],
                             uni["hex"], prov["id"], pjs, js_anchor))

    out["cloneIdentities"] = {
        "ts_L0": id0, "ts_L1": id1, "js_L0": idjs,
        "ts_body_language_version": blv0,
        "js_body_language_version": blvjs,
        "identical_bytes_different_identity": (id0 != idjs),
        "note": "identical body bytes; the TypeScript engine universe produced a "
                "typescript body and a javascript body, so they never group",
    }

    # --- scopes / coverage -------------------------------------------------
    file_scope = G.make_subject_scope(store, snap, "file", "enumerated", uni["hex"],
                                      uni["hex"], prov["id"], sorted(files))
    scopes.append(file_scope)
    coverages.append(G.make_coverage(store, file_scope,
                                     F.na_entry("file", "enumerated", file_scope)))

    clone_subjects = sorted(["src/app.ts", "src/legacy.js"])
    clone_scope = G.make_subject_scope(store, snap, "clones", "normalized-body-hash",
                                       uni["hex"], uni["hex"], prov["id"], clone_subjects)
    scopes.append(clone_scope)
    coverages.append(G.make_coverage(store, clone_scope,
                                     F.na_entry("clones", "normalized-body-hash",
                                                clone_scope)))

    # a resolved rung with an honest incomplete resolution (RC-3)
    ref_scope = G.make_subject_scope(store, snap, "references", "resolved-binding",
                                     uni["hex"], uni["hex"], prov["id"],
                                     ["sym:src/app.ts#add"])
    scopes.append(ref_scope)
    ue_payload = {"referrer": "sym:src/legacy.js#add", "relation": "references",
                  "edgeKind": "computed-member-access", "targetScope": "module",
                  "targetModule": "src/app.ts", "detail": "m[k]() with runtime k"}
    ue_fact = G.make_fact(store, snap, "unresolved-edge", "observed", uni["hex"],
                          uni["hex"], prov["id"], ue_payload, js_anchor)
    facts.append(ue_fact)
    coverages.append(G.make_coverage(store, ref_scope,
                                     F.entry("references", "resolved-binding", "complete",
                                             ref_scope["commitment"],
                                             ref_scope["subjectCount"], "incomplete",
                                             True, True, "complete", 1,
                                             ["computed-member-access"],
                                             "resolution-incomplete",
                                             None)))  # see MUST-2: no NativeCause member

    return dict(out, store=store, snapshot=snap, closures=closures, context=ctx,
                universe=uni, retained=retained, facts=facts, scopes=scopes,
                coverages=coverages, provider=prov, evaluator=ev, rule=rc,
                files=files, configGraph=graph_rec, layout=layout)
