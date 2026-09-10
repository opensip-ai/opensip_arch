"""Vector group A: TypeScript / JavaScript graphs (contexts, config graphs,
universes, facts, Coverage, view, proof, evidence, seal, Run)."""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osip import *
from model import *

S = Store()
V = {}   # vector name -> result


def blob(path, content):
    b = content.encode("utf-8") if isinstance(content, str) else content
    d = S.put_blob(b, "source:" + path)
    return {"path": path, "sha256": d, "bytes": len(b)}, b


def inv(rows):
    rows = sorted(rows, key=lambda r: r["path"].encode())
    check_order(rows, "path", "source-inventory")
    return rows


def closure(kind, tree, semver, protomajor, platform, manifest_body):
    rec = {"schemaVersion": 2, "kind": kind,
           "manifestDigest": S.put_blob(manifest_body, "manifest:" + kind),
           "tree": sorted(tree, key=lambda b: b["path"].encode()),
           "semanticVersion": semver, "protocolMajor": protomajor,
           "platform": platform}
    cid = S.mint("closure", rec)
    return cid, rec


PROJECT_ID = "prj1-" + "7c" * 32
PLATFORM = "macos-aarch64"

# ------------------------------------------------------------------ closures
tsc_bin, _ = blob("bin/tsc.js", "TSC-EXE-BYTES")
node_bin, _ = blob("bin/node", "NODE-RUNTIME-BYTES")
tspkg, _ = blob("package.json", "TS-COMPILER-PACKAGE-MANIFEST")
TS_TOOL_CID, TS_TOOL = closure("toolchain", [tsc_bin, node_bin, tspkg],
                               "5.6.2", 2, PLATFORM, b"TS-TOOLCHAIN-MANIFEST-BODY")

lib_es2022, _ = blob("lib.es2022.d.ts", "declare-es2022")
lib_dom, _ = blob("lib.dom.d.ts", "declare-dom")
lib_es5, _ = blob("lib.es5.d.ts", "declare-es5")          # unselected, still inventoried
TS_STDLIB_CID, TS_STDLIB = closure("stdlib", [lib_es2022, lib_dom, lib_es5],
                                   "5.6.2", 2, PLATFORM, b"TS-STDLIB-MANIFEST-BODY")

prov_ts, _ = blob("bin/provider-ts", "TS-PROVIDER-BYTES")
TS_PROV_CID, TS_PROV = closure("provider", [prov_ts], "1.0.0", 2, PLATFORM,
                               b"TS-PROVIDER-MANIFEST-BODY")
ev_bin, _ = blob("bin/evaluator", "EVALUATOR-BYTES")
EVAL_CID, EVAL = closure("evaluator", [ev_bin], "1.0.0", 0, PLATFORM,
                         b"EVALUATOR-MANIFEST-BODY")


def lib_component(n):
    """The published libSelection -> component join: 'lib.' + fold(n) + '.d.ts'."""
    return "lib." + n.lower() + ".d.ts"


STDLIB_COMPONENTS = sorted(
    [{"component": os.path.basename(b["path"]), "sha256": b["sha256"]}
     for b in TS_STDLIB["tree"]], key=lambda r: r["component"].encode())

# ---------------------------------------------------------------- repository R1
# Ordinary TypeScript project: reads node_modules, resolves bare specifiers,
# tsconfig extends MULTIPLE ORDERED BASES INCLUDING A REPEAT.
r1 = {}
r1["tsconfig.json"], _ = blob("tsconfig.json",
                              '{"extends":["./configs/base.a.json","./configs/base.b.json","./configs/base.a.json"]}')
r1["configs/base.a.json"], _ = blob("configs/base.a.json", '{"compilerOptions":{"strict":true}}')
r1["configs/base.b.json"], _ = blob("configs/base.b.json", '{"compilerOptions":{"strict":false}}')
r1["package.json"], _ = blob("package.json", '{"name":"app","private":true}')
r1["package-lock.json"], _ = blob("package-lock.json", '{"lockfileVersion":3}')
r1["src/index.ts"], _ = blob("src/index.ts", 'import {pad} from "left-pad";\nexport function main(){ return pad("x",3); }\n')
r1["src/util.ts"], _ = blob("src/util.ts", 'export function helper(){ return 1; }\n')
R1_INV = inv(list(r1.values()))

# node_modules is PRUNED by segment: NOT an inventory row. It is a retained
# resolution read-set observation joined by digest (ResolvedNodeModulesLayoutV1).
nm_manifest = b'{"name":"left-pad","version":"1.3.0"}'
NM_DIGEST = S.put_blob(nm_manifest, "node_modules manifest")
LAYOUT = {"schemaVersion": 1, "entries": [
    {"packageName": "left-pad", "packageVersion": "1.3.0",
     "installPath": "node_modules/left-pad", "realPath": "node_modules/left-pad",
     "contentSha256": NM_DIGEST}]}
check_order(LAYOUT["entries"], {"by": ["installPath"]}, "layout")
LAYOUT_DIGEST = S.put_record(LAYOUT, "ResolvedNodeModulesLayoutV1")


def config_graph(entry, nodes):
    nodes = sorted(nodes, key=lambda n: n["path"].encode())
    check_order(nodes, {"by": ["path"]}, "configGraph.nodes")
    rec = {"schemaVersion": 1, "entryConfigPath": entry, "nodes": nodes}
    # reachability + acyclicity + edges name another node (native sec.2.2)
    byp = {n["path"]: n for n in nodes}
    for n in nodes:
        for e in n["extendsResolved"]:
            if e not in byp:
                raise Refuse("CONFIG_GRAPH_EDGE_NOT_A_NODE", e)
    seen, stack = set(), [entry] if entry else []
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        stack.extend(byp[p]["extendsResolved"])
    if entry is not None and seen != set(byp):
        raise Refuse("CONFIG_GRAPH_UNREACHABLE_NODE", str(set(byp) - seen))
    return rec, S.put_record(rec, "TypeScriptConfigGraphV1")


def derive_config_origin(graph):
    """configOrigin is DERIVED from the retained record, never asserted."""
    if graph["entryConfigPath"] is None and graph["nodes"] == []:
        return "synthesized"
    entry = [n for n in graph["nodes"] if n["path"] == graph["entryConfigPath"]][0]
    return "jsconfig" if entry["kind"] == "jsconfig" else "tsconfig"


def node_kind(path):
    b = os.path.basename(path)
    return "tsconfig" if b == "tsconfig.json" else ("jsconfig" if b == "jsconfig.json" else "other")


def cnode(path, extends):
    return {"path": path, "contentSha256": _digest_of(path), "kind": node_kind(path),
            "extendsResolved": extends}


_INVMAP = {}


def _digest_of(path):
    return _INVMAP[path]


for row in R1_INV:
    _INVMAP[row["path"]] = row["sha256"]

TS1_GRAPH, TS1_GRAPH_D = config_graph("tsconfig.json", [
    cnode("tsconfig.json", ["configs/base.a.json", "configs/base.b.json", "configs/base.a.json"]),
    cnode("configs/base.a.json", []),
    cnode("configs/base.b.json", []),
])
V["TS-CFG-1-ordinary-tsconfig-multiple-ordered-bases-with-repeat"] = {
    "record": TS1_GRAPH, "tsconfigGraphHash": TS1_GRAPH_D,
    "derivedConfigOrigin": derive_config_origin(TS1_GRAPH),
    "note": "extendsResolved is x-opensip-order sequence: the REPEATED base is retained "
            "and later-wins precedence is preserved. Deduplicating it is a different record."}

# control: same three edges deduplicated -> DIFFERENT retained record and hash
TS1B_GRAPH, TS1B_GRAPH_D = config_graph("tsconfig.json", [
    cnode("tsconfig.json", ["configs/base.a.json", "configs/base.b.json"]),
    cnode("configs/base.a.json", []),
    cnode("configs/base.b.json", []),
])
V["TS-CFG-1b-control-dedup-of-a-repeated-base-is-a-different-record"] = {
    "tsconfigGraphHash": TS1B_GRAPH_D,
    "differsFrom_TS_CFG_1": TS1B_GRAPH_D != TS1_GRAPH_D}


def ts_context(language_mode, config_graph_paths, lockfile, layout_digest,
               honored, module_resolution, package_module_type, lib_sel):
    proj = {"schemaVersion": 2, "ancestorCarrierVerified": True,
            "environmentSanitized": True, "typeAcquisitionEnabled": False,
            "executableSelected": False, "honoredOptions": honored,
            "strippedOptions": [
                {"option": "outDir", "reason": "emits-output"},
                {"option": "typeRoots", "reason": "acquires-types-from-the-network"}],
            "configGraphPaths": sorted(config_graph_paths, key=lambda p: p.encode())}
    check_order(proj["configGraphPaths"], "utf8", "configGraphPaths")
    ctx = {"schemaVersion": 2, "languageMode": language_mode,
           "toolchain": {"compilerName": "typescript", "compilerVersion": TS_TOOL["semanticVersion"],
                         "compilerPackageDigest": tspkg["sha256"],
                         "typescriptStdlibMerkleRoot": TS_STDLIB_CID.split(":")[1],
                         "standardLibraryComponentDigests": STDLIB_COMPONENTS,
                         "libSelection": sorted(lib_sel, key=lambda s: s.encode())},
           "toolClosure": {"compiler": tsc_bin["sha256"], "runtime": node_bin["sha256"],
                           "closureId": TS_TOOL_CID},
           "configProjection": proj, "moduleResolutionMode": module_resolution,
           "packageModuleType": package_module_type,
           "nodeModulesLayoutDigest": layout_digest,
           "lockfileIdentity": lockfile}
    return ctx


def admit_ts_context(ctx, inventory):
    """native sec.2.4 admission, re-run at Run closure over retained bytes."""
    tc = ctx["toolClosure"]
    stdlib_hex = ctx["toolchain"]["typescriptStdlibMerkleRoot"]
    for cid, kind in ((tc["closureId"], "toolchain"),
                      ("closure2:" + stdlib_hex, "stdlib")):
        d = cid.split(":")[1]
        if not S.has(d):
            raise Refuse("native.native-context-closure-unretained", cid)
        rec = S.reframe_check(d, "closure")
        if rec["kind"] != kind:
            raise Refuse("native.native-context-closure-kind-mismatch", cid)
        if H("closure", rec) != d:
            raise Refuse("native.native-context-closure-identity-mismatch", cid)
    tool_tree = {b["sha256"] for b in S.reframe_check(tc["closureId"].split(":")[1], "closure")["tree"]}
    for f in ("compiler", "runtime"):
        if tc[f] not in tool_tree:
            raise Refuse("native.native-context-tool-not-in-closure", f)
    if ctx["toolchain"]["compilerPackageDigest"] not in tool_tree:
        raise Refuse("native.native-context-tool-not-in-closure", "compilerPackageDigest")
    if ctx["toolchain"]["compilerVersion"] != S.reframe_check(
            tc["closureId"].split(":")[1], "closure")["semanticVersion"]:
        raise Refuse("native.native-context-compiler-version-not-from-manifest",
                     ctx["toolchain"]["compilerVersion"])
    # stdlib inventory must be COMPLETE and basename-unambiguous
    st = S.reframe_check("closure2:".join([""]) + stdlib_hex if False else stdlib_hex, "closure")
    basenames = [os.path.basename(b["path"]) for b in st["tree"]]
    if len(set(basenames)) != len(basenames):
        raise Refuse("native.native-context-stdlib-tree-ambiguous-basename", "")
    declared = {r["component"]: r["sha256"] for r in ctx["toolchain"]["standardLibraryComponentDigests"]}
    for b in st["tree"]:
        bn = os.path.basename(b["path"])
        if bn not in declared:
            raise Refuse("native.native-context-stdlib-inventory-incomplete", bn)
        if declared[bn] != b["sha256"]:
            raise Refuse("native.native-context-stdlib-tree-mismatch", bn)
    # libSelection -> component membership + honored-lib set equality
    ho = ctx["configProjection"]["honoredOptions"]
    for n in ctx["toolchain"]["libSelection"]:
        if lib_component(n) not in declared:
            raise Refuse("native.native-context-lib-not-retained", n)
    if len(set(n.lower() for n in ctx["toolchain"]["libSelection"])) != len(ctx["toolchain"]["libSelection"]):
        raise Refuse("native.native-context-field-mismatch", "duplicate-lib-selection")
    if {n.lower() for n in ctx["toolchain"]["libSelection"]} != {m.lower() for m in ho["lib"]}:
        raise Refuse("native.native-context-field-mismatch", "libSelection")
    if ctx["moduleResolutionMode"] != ho["moduleResolution"]:
        raise Refuse("native.native-context-field-mismatch", "moduleResolution")
    # snapshot joins
    ipaths = {r["path"]: r for r in inventory}
    for p in ctx["configProjection"]["configGraphPaths"]:
        if p not in ipaths:
            raise Refuse("native.native-context-config-path-outside-snapshot", p)
    lf = ctx["lockfileIdentity"]
    if lf is not None:
        if lf["path"] not in ipaths or ipaths[lf["path"]]["sha256"] != lf["contentSha256"]:
            raise Refuse("native.native-context-lockfile-outside-snapshot", str(lf))
    # nodeModulesLayoutDigest is a retained canonical record (blobJoin, NOT snapshot)
    if ctx["nodeModulesLayoutDigest"] is not None and not S.has(ctx["nodeModulesLayoutDigest"]):
        raise Refuse("native.native-context-layout-unretained", "")
    return {"language": "typescript", "contextId": "sha256:" + H("native.context.typescript.v2", ctx)}


def bind_ts_universe(u, admission, ctx, retained, inventory):
    """native sec.2.4 / sec.11 binding: retained context bytes are REQUIRED."""
    if ctx is None:
        raise Refuse("native.universe-context-not-supplied", "")
    if admission["language"] != "typescript":
        raise Refuse("native.native-context-language-mismatch", admission["language"])
    if u["nativeContextId"] != admission["contextId"]:
        raise Refuse("native.universe-context-binding-mismatch", u["nativeContextId"])
    if "sha256:" + H("native.context.typescript.v2", ctx) != u["nativeContextId"]:
        raise Refuse("native.universe-context-binding-mismatch",
                     "context-bytes-are-not-the-admitted-ones")
    graph = retained.get("configGraph")
    if graph is None:
        raise Refuse("native.universe-retained-inputs-not-supplied", "configGraph")
    if raw(graph) != u["tsconfigGraphHash"]:
        raise Refuse("native.universe-config-graph-mismatch", "")
    if {n["path"] for n in graph["nodes"]} != set(ctx["configProjection"]["configGraphPaths"]):
        raise Refuse("native.universe-context-field-mismatch", "configGraphPaths")
    ipaths = {r["path"]: r["sha256"] for r in inventory}
    for n in graph["nodes"]:
        if ipaths.get(n["path"]) != n["contentSha256"]:
            raise Refuse("native.universe-config-node-not-inventoried", n["path"])
    if u["configOrigin"] != derive_config_origin(graph):
        raise Refuse("native.universe-context-field-mismatch", "configOrigin")
    for f in ("languageMode", "packageModuleType"):
        if u[f] != ctx[f]:
            raise Refuse("native.universe-context-field-mismatch", f)
    ho = ctx["configProjection"]["honoredOptions"]
    for uf, cf in (("allowJs", "allowJs"), ("checkJs", "checkJs")):
        if u[uf] != ho[cf]:
            raise Refuse("native.universe-context-field-mismatch", uf)
    if u["jsAdmittedToProgram"] != ho["allowJs"] or u["jsDiagnosticsEnabled"] != ho["checkJs"]:
        raise Refuse("native.universe-context-field-mismatch", "jsAdmittedToProgram")
    if u["nodeModulesInReadSet"] != (ctx["nodeModulesLayoutDigest"] is not None):
        raise Refuse("native.universe-context-field-mismatch", "nodeModulesInReadSet")
    lk = "none" if ctx["lockfileIdentity"] is None else ctx["lockfileIdentity"]["kind"]
    if u["lockfileKind"] != lk:
        raise Refuse("native.universe-context-field-mismatch", "lockfileKind")
    if ctx["nodeModulesLayoutDigest"] is not None:
        if retained.get("nodeModulesLayout") is None:
            raise Refuse("native.universe-retained-inputs-not-supplied", "nodeModulesLayout")
        if raw(retained["nodeModulesLayout"]) != ctx["nodeModulesLayoutDigest"]:
            raise Refuse("native.universe-layout-mismatch", "")
    if (u["synthesizedOptions"] is None) != (u["configOrigin"] != "synthesized"):
        raise Refuse("native.universe-context-field-mismatch", "synthesizedOptions")
    return "sha256:" + H("native.semantic-universe.typescript.v2", u)


HONORED_R1 = {"allowJs": False, "checkJs": False, "module": "node16",
              "moduleResolution": "node16", "target": "es2022", "strict": True,
              "skipLibCheck": True, "noEmit": True, "types": [],
              "lib": ["es2022", "dom"], "baseUrl": None, "paths": [], "rootDirs": [],
              "resolveJsonModule": True, "allowSyntheticDefaultImports": True,
              "esModuleInterop": True, "customConditions": [], "jsx": None}

TS1_CTX = ts_context("ts-tsconfig",
                     ["tsconfig.json", "configs/base.a.json", "configs/base.b.json"],
                     {"kind": "package-lock", "path": "package-lock.json",
                      "contentSha256": _INVMAP["package-lock.json"]},
                     LAYOUT_DIGEST, HONORED_R1, "node16", "absent",
                     ["es2022", "dom"])
TS1_ADM = admit_ts_context(TS1_CTX, R1_INV)
TS1_CTX_ID = S.put_framed("native.context.typescript.v2", TS1_CTX)

TS1_UNIV = {"schemaVersion": 2, "languageMode": "ts-tsconfig", "configOrigin": "tsconfig",
            "synthesizerVersion": None, "synthesizedOptions": None,
            "packageModuleType": "absent", "allowJs": False, "checkJs": False,
            "jsAdmittedToProgram": False, "jsDiagnosticsEnabled": False,
            "resolutionCompletenessImplied": False,
            "jsRootFiles": [], "programRootFiles": ["src/index.ts", "src/util.ts"],
            "lockfileKind": "package-lock", "nodeModulesInReadSet": True,
            "executionCapableResolution": False,
            "tsconfigGraphHash": TS1_GRAPH_D,
            "nativeContextId": TS1_ADM["contextId"]}
TS1_UNIV_ID = bind_ts_universe(TS1_UNIV, TS1_ADM, TS1_CTX,
                               {"configGraph": TS1_GRAPH, "nodeModulesLayout": LAYOUT}, R1_INV)
S.put_framed("native.semantic-universe.typescript.v2", TS1_UNIV)

V["TS-CTX-1-ordinary-project-reads-node_modules"] = {
    "contextId": TS1_ADM["contextId"],
    "planBareHex": TS1_ADM["contextId"].split(":")[1],
    "universeId": TS1_UNIV_ID,
    "universeBareHex": TS1_UNIV_ID.split(":")[1],
    "nodeModulesLayoutDigest": LAYOUT_DIGEST,
    "layoutIsNotSnapshotInventory": all(
        e["installPath"] not in {r["path"] for r in R1_INV} for e in LAYOUT["entries"]),
    "bareSpecifierResolves": True}
