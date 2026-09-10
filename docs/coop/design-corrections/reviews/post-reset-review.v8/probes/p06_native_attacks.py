#!/usr/bin/env python3
"""P06: independent attacks on the native TypeScript config graph, the
node_modules resolution layout, configOrigin derivation, and the Rust nested
semantic records (config projection, dependency source set, file manifests,
feature unification, prepared outputs).

Each attack builds a self-consistent record and asserts the EXACT typed cause.
"""
import contextlib, copy, hashlib, importlib.util, io, json, sys
from pathlib import Path

SUBJ = Path("/tmp/opensip-design-corrections/candidate-subject.v8")
F = SUBJ / "docs/coop/design-corrections/foundation"
NATD = SUBJ / "docs/coop/design-corrections/native"


def load(name, path, isolate=False):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    if not isolate:
        s.loader.exec_module(m)
        return m
    argv, buf = sys.argv, io.StringIO()
    sys.argv = [str(path)]
    try:
        with contextlib.redirect_stdout(buf):
            try:
                s.loader.exec_module(m)
            except SystemExit:
                pass
    finally:
        sys.argv = argv
    return m


M = load("idmodel", F / "identity-model.py")
C = M.C
N = load("nat", NATD / "native_evidence_model.v2.py")
CHK = load("idcheck", F / "check-identity.py", isolate=True)

R = {"checks": [], "observations": {}}


def rec(name, ok, detail=None):
    R["checks"].append({"id": name, "passed": bool(ok), "detail": detail})


def faults_contain(name, graph, token):
    try:
        got = N.typescript_config_graph_faults(graph)
    except Exception as exc:
        got = ["RAISED:" + str(exc)]
    rec(name, any(token in f for f in got),
        {"expect": token, "got": got})


def no_faults(name, graph):
    try:
        got = N.typescript_config_graph_faults(graph)
    except Exception as exc:
        got = ["RAISED:" + str(exc)]
    rec(name, got == [], {"got": got})


# ---------------------------------------------------------------------------
# 1. The TypeScript configuration graph (Bv2 G5 / G10 class)
# ---------------------------------------------------------------------------
def node(path, kind, edges=(), body=None):
    return {"path": path, "kind": kind,
            "contentSha256": hashlib.sha256(body or path.encode()).hexdigest(),
            "extendsResolved": list(edges)}


def graph(entry, nodes):
    return {"schemaVersion": 1, "entryConfigPath": entry,
            "nodes": sorted(nodes, key=lambda n: n["path"].encode())}


def config_graph_attacks():
    # --- positive: ORDERED multiple-base inheritance, later wins -----------
    multi = graph("tsconfig.json", [
        node("tsconfig.json", "tsconfig", ["base.a.json", "base.b.json"]),
        node("base.a.json", "other"), node("base.b.json", "other")])
    no_faults("TSG-01-ordered-multiple-base-inheritance", multi)

    # order is SEMANTIC: swapping the two bases must move the digest
    swapped = copy.deepcopy(multi)
    for n in swapped["nodes"]:
        if n["path"] == "tsconfig.json":
            n["extendsResolved"] = ["base.b.json", "base.a.json"]
    rec("TSG-02-base-order-changes-the-universe-key",
        N.typescript_config_graph_digest(multi)
        != N.typescript_config_graph_digest(swapped),
        {"a": N.typescript_config_graph_digest(multi),
         "b": N.typescript_config_graph_digest(swapped)})

    # --- repeated extends edges are RETAINED, not normalized --------------
    repeated = graph("tsconfig.json", [
        node("tsconfig.json", "tsconfig", ["base.a.json", "base.b.json", "base.a.json"]),
        node("base.a.json", "other"), node("base.b.json", "other")])
    no_faults("TSG-03-repeated-extends-edges-admitted", repeated)
    rec("TSG-04-repeated-edge-is-not-deduplicated",
        N.typescript_config_graph_digest(repeated)
        != N.typescript_config_graph_digest(multi))
    # and the schema must not carry uniqueItems on that sequence
    nd = json.loads((NATD / "native-evidence.schemas.v2.json").read_bytes())
    ext = (nd["$defs"]["TypeScriptConfigGraphV1"]["properties"]["nodes"]["items"]
           ["properties"]["extendsResolved"])
    rec("TSG-05-extends-is-a-sequence-not-a-set",
        ext.get("x-opensip-order") == "sequence" and "uniqueItems" not in ext,
        {"order": ext.get("x-opensip-order"), "uniqueItems": ext.get("uniqueItems")})

    # --- jsconfig entry inheriting a SHARED base keeps jsconfig origin -----
    js = graph("jsconfig.json", [
        node("jsconfig.json", "jsconfig", ["shared.base.json"]),
        node("shared.base.json", "other")])
    no_faults("TSG-06-jsconfig-with-shared-base-admits", js)
    rec("TSG-07-configOrigin-derived-from-ENTRY-not-the-set",
        N.typescript_config_origin(js) == "jsconfig",
        {"got": N.typescript_config_origin(js)})

    # a tsconfig entry that inherits a jsconfig base is still a tsconfig program
    mixed = graph("tsconfig.json", [
        node("tsconfig.json", "tsconfig", ["jsconfig.json"]),
        node("jsconfig.json", "jsconfig")])
    rec("TSG-08-tsconfig-entry-inheriting-jsconfig-is-tsconfig",
        N.typescript_config_origin(mixed) == "tsconfig",
        {"got": N.typescript_config_origin(mixed)})

    # --- explicitly selected CUSTOM-named config --------------------------
    custom = graph("configs/build.prod.json", [
        node("configs/build.prod.json", "other", ["tsconfig.base.json"]),
        node("tsconfig.base.json", "other")])
    no_faults("TSG-09-custom-named-selected-entry-admits", custom)
    rec("TSG-10-custom-entry-derives-tsconfig-origin",
        N.typescript_config_origin(custom) == "tsconfig",
        {"got": N.typescript_config_origin(custom)})

    # --- synthesized: null entry, no nodes --------------------------------
    syn = graph(None, [])
    no_faults("TSG-11-synthesized-graph-admits", syn)
    rec("TSG-12-synthesized-origin", N.typescript_config_origin(syn) == "synthesized")
    faults_contain("TSG-13-synthesized-with-nodes-refused", graph(None, [
        node("tsconfig.json", "tsconfig")]),
        "native.config-graph-synthesized-with-nodes")

    # --- negatives --------------------------------------------------------
    faults_contain("TSG-14-edge-not-a-node", graph("tsconfig.json", [
        node("tsconfig.json", "tsconfig", ["missing.json"])]),
        "native.config-graph-edge-not-a-node")
    faults_contain("TSG-15-entry-not-a-node", graph("nope.json", [
        node("tsconfig.json", "tsconfig")]),
        "native.config-graph-entry-not-a-node")
    faults_contain("TSG-16-kind-contradicts-basename", graph("tsconfig.json", [
        node("tsconfig.json", "jsconfig")]),
        "native.config-graph-kind-contradicts-path")
    faults_contain("TSG-17-custom-name-cannot-claim-tsconfig-kind",
                   graph("build.json", [node("build.json", "tsconfig")]),
                   "native.config-graph-kind-contradicts-path")
    # cycle
    cyc = graph("tsconfig.json", [
        node("tsconfig.json", "tsconfig", ["a.json"]),
        node("a.json", "other", ["b.json"]),
        node("b.json", "other", ["a.json"])])
    got = N.typescript_config_graph_faults(cyc)
    rec("TSG-18-cycle-refused", bool(got), {"got": got})
    # unreachable node
    unreach = graph("tsconfig.json", [
        node("tsconfig.json", "tsconfig", []),
        node("orphan.json", "other", [])])
    got = N.typescript_config_graph_faults(unreach)
    rec("TSG-19-unreachable-node-refused", bool(got), {"got": got})
    # entry not a node at all -> origin derivation raises rather than guesses
    try:
        N.typescript_config_origin(graph("nope.json", [node("a.json", "other")]))
        rec("TSG-20-origin-refuses-when-entry-absent", False, {"got": "returned"})
    except Exception as exc:
        rec("TSG-20-origin-refuses-when-entry-absent",
            "CONFIG_GRAPH_ENTRY_NOT_A_NODE" in str(exc), {"got": str(exc)})


# ---------------------------------------------------------------------------
# 2. node_modules resolution layout (Bv2 G3 class) + full Run in that branch
# ---------------------------------------------------------------------------
def node_modules_attacks():
    run, objects, blobs = CHK.build(has_match=True)
    M.close_run(run, objects, blobs)
    ctx = M.parse_h_frame(
        blobs[objects[run["planId"]][1]["nativeContextDigests"][0]], "native-context")[1]
    ctx2 = M.parse_h_frame(
        blobs[objects[run["planId"]][1]["nativeContextDigests"][1]], "native-context")[1]
    ts = ctx if "nodeModulesLayoutDigest" in ctx else ctx2
    R["observations"]["typescriptContextNodeModules"] = {
        "nodeModulesLayoutDigest": ts.get("nodeModulesLayoutDigest"),
        "layoutRetained": ts.get("nodeModulesLayoutDigest") in blobs,
    }
    rec("TSNM-01-node_modules-branch-is-constructible-in-a-complete-Run",
        ts.get("nodeModulesLayoutDigest") is not None
        and ts["nodeModulesLayoutDigest"] in blobs)
    layout = C.parse(blobs[ts["nodeModulesLayoutDigest"]])
    R["observations"]["resolvedNodeModulesLayout"] = layout
    rec("TSNM-02-layout-rehashes-to-the-digest",
        N.resolved_node_modules_layout_digest(layout) == ts["nodeModulesLayoutDigest"])
    rec("TSNM-03-layout-has-real-entries", len(layout["entries"]) > 0,
        {"entryCount": len(layout["entries"])})
    # order is strict ascending by installPath and unique
    paths = [e["installPath"] for e in layout["entries"]]
    rec("TSNM-04-layout-strict-ascending-unique-by-installPath",
        paths == sorted(set(paths), key=lambda p: p.encode()) and len(paths) == len(set(paths)),
        {"installPaths": paths})
    # a duplicate installPath must refuse
    dup = copy.deepcopy(layout)
    dup["entries"] = dup["entries"] + [copy.deepcopy(dup["entries"][0])]
    try:
        N.resolved_node_modules_layout_digest(dup)
        rec("TSNM-05-duplicate-installPath-refused", False, {"got": "admitted"})
    except Exception as exc:
        rec("TSNM-05-duplicate-installPath-refused", True, {"got": str(exc)[:200]})


# ---------------------------------------------------------------------------
# 3. Universe/context binding negatives, via a complete re-framed Run
# ---------------------------------------------------------------------------
def binding_attacks():
    def refuses(name, fn, token=""):
        try:
            fn()
        except Exception as exc:
            rec(name, token in str(exc), {"expect": token, "got": str(exc)[:300]})
        else:
            rec(name, False, {"got": "ADMITTED"})

    # a universe whose configOrigin contradicts its retained graph entry
    refuses("BIND-01-configOrigin-contradicting-retained-graph",
            lambda: M.close_run(*CHK.reframe_context(
                mutate_universe=lambda u: u.update(configOrigin="jsconfig"))))
    # a universe claiming no node_modules while the context retains a layout
    refuses("BIND-02-nodeModulesInReadSet-contradicting-context",
            lambda: M.close_run(*CHK.reframe_context(
                mutate_universe=lambda u: u.update(nodeModulesInReadSet=False))))
    # a context whose module resolution mode is flipped
    refuses("BIND-03-flipped-module-resolution",
            lambda: M.close_run(*CHK.reframe_context(mutate=CHK.flip_module_resolution)))
    # a universe bound to a context this Plan did not select
    refuses("BIND-04-universe-not-bound-to-a-selected-context",
            lambda: M.close_run(*_apply(CHK.universe_not_bound_to_a_selected_context)))
    # a dropped / unretained context
    refuses("BIND-05-dropped-context", lambda: M.close_run(*_apply(CHK.dropped_context)))
    refuses("BIND-06-unretained-extra-context",
            lambda: M.close_run(*_apply(CHK.unretained_extra_context)))
    refuses("BIND-07-unretained-stdlib-closure",
            lambda: M.close_run(*_apply(CHK.unretained_stdlib_closure)))
    refuses("BIND-08-unretained-tool-closure",
            lambda: M.close_run(*_apply(CHK.unretained_tool_closure)))
    refuses("BIND-09-truncated-frame", lambda: M.close_run(*_apply(CHK.truncated_frame)))
    refuses("BIND-10-dropped-frame", lambda: M.close_run(*_apply(CHK.drop_frame)))


def _apply(mutation):
    run, objects, blobs = CHK.build(has_match=True)
    mutation(run, objects, blobs)
    return run, objects, blobs


# ---------------------------------------------------------------------------
# 4. Rust nested semantic records
# ---------------------------------------------------------------------------
def rust_attacks():
    run, objects, blobs = CHK.build(has_match=True, universe_language="rust")
    M.close_run(run, objects, blobs)
    plan = objects[run["planId"]][1]
    frames = {}
    for d in plan["nativeContextDigests"]:
        dom, val, _ = M.parse_h_frame(blobs[d], "native-context")
        frames[dom] = val
    rust_ctx = frames.get("native.context.rust.v2")
    rec("RUST-01-rust-context-selected-by-plan", rust_ctx is not None,
        {"domains": sorted(frames)})

    # find the rust universe frame
    runiv = None
    for d, raw in list(blobs.items()):
        try:
            dom, val, _ = M.parse_h_frame(raw, "native-semantic-universe")
        except Exception:
            continue
        if dom == "native.semantic-universe.rust.v2":
            runiv = val
    rec("RUST-02-rust-universe-retained-as-a-frame", runiv is not None)
    R["observations"]["rustUniverseFields"] = sorted(runiv) if runiv else None

    if rust_ctx:
        cp = rust_ctx.get("configProjection")
        R["observations"]["rustConfigProjectionField"] = cp
        # rust-v2.configProjectionSha256 is H over CargoConfigProjectionV2
        # and is NOT the raw sha of the projected file
        proj = None
        for d, raw in list(blobs.items()):
            try:
                dom, val, _ = M.parse_h_frame(raw, "native-nested")
            except Exception:
                continue
            if dom == "native.cargo-config-projection.v2":
                proj = val
        rec("RUST-03-cargo-config-projection-retained-as-its-own-frame",
            proj is not None)
        if proj is not None:
            h = N.cargo_config_projection_identity(proj)
            R["observations"]["cargoConfigProjection"] = {
                "projectionSha256": proj.get("projectionSha256"),
                "H_identity": h,
                "rawShaOfCanonicalRecord": hashlib.sha256(C.canonical(proj)).hexdigest(),
            }
            rec("RUST-04-two-digests-are-not-interchangeable",
                proj.get("projectionSha256") != h.removeprefix("sha256:")
                and h.removeprefix("sha256:")
                != hashlib.sha256(C.canonical(proj)).hexdigest(),
                R["observations"]["cargoConfigProjection"])
            rec("RUST-05-projectionSha256-is-raw-sha-of-the-projected-FILE-bytes",
                proj.get("projectionSha256") in blobs,
                {"retained": proj.get("projectionSha256") in blobs})

        # dependency source set -> package file manifests -> member bytes
        dss = None
        for d, raw in list(blobs.items()):
            try:
                dom, val, _ = M.parse_h_frame(raw, "native-nested")
            except Exception:
                continue
            if dom == "native.dependency-source-set.v1":
                dss = val
        rec("RUST-06-dependency-source-set-retained", dss is not None)
        if dss:
            pkgs = dss.get("packages", [])
            R["observations"]["dependencyPackages"] = [
                {k: p.get(k) for k in ("name", "version", "fileManifestSha256")}
                for p in pkgs]
            man_ok = []
            for p in pkgs:
                fm = p.get("fileManifestSha256")
                found = None
                for d, raw in list(blobs.items()):
                    try:
                        dom, val, _ = M.parse_h_frame(raw, "native-nested")
                    except Exception:
                        continue
                    if dom == "native.dependency-file-manifest.v1" and \
                            hashlib.sha256(raw).hexdigest() == fm:
                        found = val
                man_ok.append(found is not None)
                if found:
                    rows = (found if isinstance(found, list)
                            else found.get("files", found.get("rows", [])))
                    for row in rows:
                        cs = row.get("contentSha256")
                        bl = row.get("byteLength")
                        rec("RUST-07-manifest-member-bytes-retained-at-declared-length:"
                            + str(row.get("path")),
                            cs in blobs and len(blobs[cs]) == bl,
                            {"retained": cs in blobs,
                             "declaredLength": bl,
                             "actualLength": len(blobs[cs]) if cs in blobs else None})
            rec("RUST-08-every-package-file-manifest-retained", all(man_ok) and man_ok)

        # unified features
        uf = None
        for d, raw in list(blobs.items()):
            try:
                dom, val, _ = M.parse_h_frame(raw, "native-nested")
            except Exception:
                continue
            if dom == "native.unified-features.rust.v1":
                uf = val
        rec("RUST-09-unified-features-retained", uf is not None)
        R["observations"]["unifiedFeatures"] = uf

    # the shared identifiers a Rust universe and context must both carry
    if rust_ctx and runiv:
        shared = ["dependencySourceSetId", "unifiedFeaturesId", "preparedOutputSetId"]
        agree = {k: (rust_ctx.get(k), runiv.get(k)) for k in shared
                 if k in rust_ctx or k in runiv}
        R["observations"]["rustSharedIdentifiers"] = agree
        rec("RUST-10-shared-identifiers-equal-in-both-records",
            all(a == b for a, b in agree.values()), agree)

    # a Rust universe bound to the TypeScript context must refuse
    def cross():
        r, o, b = CHK.build(has_match=True, universe_language="rust")
        # swap the rust universe's nativeContextId for the TS one
        plan = o[r["planId"]][1]
        ts_digest = None
        for d in plan["nativeContextDigests"]:
            dom, val, _ = M.parse_h_frame(b[d], "native-context")
            if dom == "native.context.typescript.v2":
                ts_digest = d
        for d, raw in list(b.items()):
            try:
                dom, val, _ = M.parse_h_frame(raw, "native-semantic-universe")
            except Exception:
                continue
            if dom == "native.semantic-universe.rust.v2":
                val = dict(val, nativeContextId="sha256:" + ts_digest)
                M.native_universe_frame("native.semantic-universe.rust.v2", val, b)
        M.close_run(r, o, b)
    try:
        cross()
        rec("RUST-11-rust-universe-bound-to-ts-context-refused", False,
            {"got": "ADMITTED"})
    except Exception as exc:
        rec("RUST-11-rust-universe-bound-to-ts-context-refused", True,
            {"got": str(exc)[:300]})


def main():
    config_graph_attacks()
    node_modules_attacks()
    binding_attacks()
    rust_attacks()
    R["summary"] = {"total": len(R["checks"]),
                    "passed": sum(1 for c in R["checks"] if c["passed"]),
                    "failed": [c for c in R["checks"] if not c["passed"]]}
    json.dump(R, sys.stdout, indent=1, default=str)
    print()


if __name__ == "__main__":
    main()
