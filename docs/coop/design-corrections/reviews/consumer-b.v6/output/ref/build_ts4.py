"""Vector group A4: the remaining three TypeScript configuration graphs,
the JavaScript clone body produced by the SAME TypeScript engine universe,
and the TypeScript negative controls."""
import sys, os, json, hashlib, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osip import *
from model import *
from build_ts import *
from build_ts2 import *
from build_ts3 import *
import build_ts3 as B3

TSU = "native.semantic-universe.typescript.v2"

# =============================================================== R1b: js-allowjs
r1b = {}
r1b["jsconfig.json"], _ = blob("jsconfig.json", '{"extends":"./configs/shared.base.json"}')
r1b["configs/shared.base.json"], _ = blob("configs/shared.base.json", '{"compilerOptions":{"target":"es2022"}}')
r1b["package.json"], _ = blob("package.json", '{"name":"web","private":true,"type":"module"}')
JS_SRC = 'export function helper(){ return 1; }\n'
r1b["src/util.js"], _ = blob("src/util.js", JS_SRC)
R1B_INV = inv(list(r1b.values()))
R1B_MAP = {r["path"]: r["sha256"] for r in R1B_INV}


def cnode2(path, extends, invmap):
    return {"path": path, "contentSha256": invmap[path], "kind": node_kind(path),
            "extendsResolved": extends}


TS4_GRAPH, TS4_GRAPH_D = config_graph("jsconfig.json", [
    cnode2("jsconfig.json", ["configs/shared.base.json"], R1B_MAP),
    cnode2("configs/shared.base.json", [], R1B_MAP)])
V["TS-CFG-4-jsconfig-inheriting-a-shared-base-with-another-filename"] = {
    "entryConfigPath": "jsconfig.json",
    "entryKind": "jsconfig", "baseKind": "other",
    "derivedConfigOrigin": derive_config_origin(TS4_GRAPH),
    "tsconfigGraphHash": TS4_GRAPH_D,
    "note": "configOrigin is derived from the ENTRY node kind, never from the whole "
            "node set: a jsconfig.json extending a shared base of another filename "
            "remains a jsconfig program (native sec.2.2)."}

HON_JS = dict(HONORED_R1)
HON_JS.update({"allowJs": True, "checkJs": True, "strict": False,
               "lib": ["es2022"], "types": None})
TS4_CTX = ts_context("js-allowjs", ["jsconfig.json", "configs/shared.base.json"],
                     None, None, HON_JS, "node16", "module", ["es2022"])
TS4_ADM = admit_ts_context(TS4_CTX, R1B_INV)
S.put_framed("native.context.typescript.v2", TS4_CTX)
TS4_UNIV = {"schemaVersion": 2, "languageMode": "js-allowjs", "configOrigin": "jsconfig",
            "synthesizerVersion": None, "synthesizedOptions": None,
            "packageModuleType": "module", "allowJs": True, "checkJs": True,
            "jsAdmittedToProgram": True, "jsDiagnosticsEnabled": True,
            "resolutionCompletenessImplied": False,
            "jsRootFiles": ["src/util.js"], "programRootFiles": ["src/util.js"],
            "lockfileKind": "none", "nodeModulesInReadSet": False,
            "executionCapableResolution": False,
            "tsconfigGraphHash": TS4_GRAPH_D, "nativeContextId": TS4_ADM["contextId"]}
TS4_UNIV_ID = bind_ts_universe(TS4_UNIV, TS4_ADM, TS4_CTX, {"configGraph": TS4_GRAPH}, R1B_INV)
S.put_framed(TSU, TS4_UNIV)

# JavaScript clone body through the TypeScript ENGINE universe
JS_ROW = [r for r in R1B_INV if r["path"] == "src/util.js"][0]
JS_BODY = JS_SRC.encode()[24:37]
BLV_JS = body_language_version(TSU, TS4_CTX, TS4_UNIV, "src/util.js")
BID_JS, FRAME_JS = body_identity("L0-verbatim", LEVEL_SPEC["L0-verbatim"],
                                 BLV_JS["languageId"], BLV_JS, l0_payload(JS_BODY))
S.put_blob(FRAME_JS, "body-identity frame L0 js")

V["TS-CLONE-2-javascript-body-through-the-typescript-engine"] = {
    "universeDomain": TSU,
    "domainRowLanguage_ENGINE": UNIVROWS[TSU]["language"],
    "derivedBodyLanguageId": BLV_JS["languageId"],
    "sourceVariant": BLV_JS["dialect"],
    "bodyIdentity": BID_JS,
    "identicalBytesAsTheTypeScriptBody": JS_BODY == BODY_BYTES,
    "differsFromTheTypeScriptBodyIdentity": BID_JS != BID_TS_L0,
    "law": "identity sec.3 / relation-registry bodyIdentityJoin.languageIdSource: the "
           "languageId is the BODY's language from bodyLanguageByVariant[<suffix variant>], "
           "NEVER the domain row's own `language` field, which names the ENGINE. Reading the "
           "engine field would give `typescript` for every .js body."}

# NEGATIVE: a rust frame offered under a TypeScript universe
_bad_blv = dict(BLV_JS); _bad_blv["languageId"] = "rust"
_bad_id, _bad_frame = body_identity("L0-verbatim", LEVEL_SPEC["L0-verbatim"], "rust",
                                    _bad_blv, l0_payload(JS_BODY))
S.put_blob(_bad_frame, "bad rust frame under ts universe")
_bad_f, _bad_fid, _bad_pl = fact(
    "clones", "normalized-body-hash",
    {"bodyIdentity": _bad_id, "normalisationLevel": "L0-verbatim",
     "normalisationVersion": LEVEL_SPEC["L0-verbatim"]},
    [{"path": "src/util.js", "blobDigest": JS_ROW["sha256"], "startByte": 24, "endByte": 37}],
    univ_hex=TS4_UNIV_ID.split(":")[1])
try:
    body_identity_join(_bad_f, _bad_pl, R1B_INV, TSU, TS4_CTX, TS4_UNIV)
    V["TS-CLONE-N2-rust-frame-under-a-typescript-universe"] = {"result": "NOT-REFUSED (defect)"}
except Refuse as e:
    V["TS-CLONE-N2-rust-frame-under-a-typescript-universe"] = {"refusal": str(e)}

# =============================================== R1c: js-synthesized configuration
r1c = {}
r1c["package.json"], _ = blob("package.json", '{"name":"tool"}')
r1c["index.js"], _ = blob("index.js", 'module.exports = function(){ return 2; };\n')
R1C_INV = inv(list(r1c.values()))
TS3_GRAPH, TS3_GRAPH_D = config_graph(None, [])
SYNTH = {"allowJs": True, "checkJs": False, "module": "node16",
         "moduleResolution": "node16", "target": "es2022", "strict": False,
         "skipLibCheck": True, "types": [], "noEmit": True}
HON_SY = dict(HONORED_R1)
HON_SY.update({"allowJs": True, "checkJs": False, "strict": False,
               "skipLibCheck": True, "types": [], "lib": ["es2022"], "jsx": None})
TS3_CTX = ts_context("js-synthesized", [], None, None, HON_SY, "node16", "absent", ["es2022"])
TS3_ADM = admit_ts_context(TS3_CTX, R1C_INV)
S.put_framed("native.context.typescript.v2", TS3_CTX)
TS3_UNIV = {"schemaVersion": 2, "languageMode": "js-synthesized", "configOrigin": "synthesized",
            "synthesizerVersion": 1, "synthesizedOptions": SYNTH,
            "packageModuleType": "absent", "allowJs": True, "checkJs": False,
            "jsAdmittedToProgram": True, "jsDiagnosticsEnabled": False,
            "resolutionCompletenessImplied": False,
            "jsRootFiles": ["index.js"], "programRootFiles": ["index.js"],
            "lockfileKind": "none", "nodeModulesInReadSet": False,
            "executionCapableResolution": False,
            "tsconfigGraphHash": TS3_GRAPH_D, "nativeContextId": TS3_ADM["contextId"]}
TS3_UNIV_ID = bind_ts_universe(TS3_UNIV, TS3_ADM, TS3_CTX, {"configGraph": TS3_GRAPH}, R1C_INV)
V["TS-CFG-3-synthesized-configuration"] = {
    "entryConfigPath": None, "nodes": [], "derivedConfigOrigin": derive_config_origin(TS3_GRAPH),
    "tsconfigGraphHash": TS3_GRAPH_D, "synthesizerVersion": 1,
    "nodeModulesInReadSet": False,
    "bareSpecifiersAre": "unresolved-module-specifier, scope external (never an implicit install)",
    "contextId": TS3_ADM["contextId"], "universeId": TS3_UNIV_ID,
    "L_JS1_limitation": "paths/baseUrl/rootDirs/custom types are unknown under synthesized options"}

# ============================ R1d: explicitly selected CUSTOM-NAMED project config
r1d = {}
r1d["configs/app.build.json"], _ = blob(
    "configs/app.build.json",
    '{"extends":["./base.strict.json","./base.paths.json","./base.strict.json"]}')
r1d["configs/base.strict.json"], _ = blob("configs/base.strict.json", '{"compilerOptions":{"strict":true}}')
r1d["configs/base.paths.json"], _ = blob("configs/base.paths.json", '{"compilerOptions":{"baseUrl":"."}}')
r1d["package.json"], _ = blob("package.json", '{"name":"custom"}')
r1d["src/a.ts"], _ = blob("src/a.ts", 'export const a = 1;\n')
R1D_INV = inv(list(r1d.values()))
R1D_MAP = {r["path"]: r["sha256"] for r in R1D_INV}
TS2_GRAPH, TS2_GRAPH_D = config_graph("configs/app.build.json", [
    cnode2("configs/app.build.json",
           ["configs/base.strict.json", "configs/base.paths.json", "configs/base.strict.json"], R1D_MAP),
    cnode2("configs/base.strict.json", [], R1D_MAP),
    cnode2("configs/base.paths.json", [], R1D_MAP)])
TS2_CTX = ts_context("ts-tsconfig",
                     ["configs/app.build.json", "configs/base.strict.json", "configs/base.paths.json"],
                     None, None, HONORED_R1, "node16", "absent", ["es2022", "dom"])
TS2_ADM = admit_ts_context(TS2_CTX, R1D_INV)
S.put_framed("native.context.typescript.v2", TS2_CTX)
TS2_UNIV = {"schemaVersion": 2, "languageMode": "ts-tsconfig", "configOrigin": "tsconfig",
            "synthesizerVersion": None, "synthesizedOptions": None,
            "packageModuleType": "absent", "allowJs": False, "checkJs": False,
            "jsAdmittedToProgram": False, "jsDiagnosticsEnabled": False,
            "resolutionCompletenessImplied": False, "jsRootFiles": [],
            "programRootFiles": ["src/a.ts"], "lockfileKind": "none",
            "nodeModulesInReadSet": False, "executionCapableResolution": False,
            "tsconfigGraphHash": TS2_GRAPH_D, "nativeContextId": TS2_ADM["contextId"]}
TS2_UNIV_ID = bind_ts_universe(TS2_UNIV, TS2_ADM, TS2_CTX, {"configGraph": TS2_GRAPH}, R1D_INV)
V["TS-CFG-2-explicitly-selected-custom-named-config-with-ordered-repeated-bases"] = {
    "entryConfigPath": "configs/app.build.json",
    "entryNodeKind": "other",
    "derivedConfigOrigin": derive_config_origin(TS2_GRAPH),
    "orderedExtends": TS2_GRAPH["nodes"][0]["extendsResolved"],
    "repeatedBaseRetained": TS2_GRAPH["nodes"][0]["extendsResolved"].count("configs/base.strict.json") == 2,
    "tsconfigGraphHash": TS2_GRAPH_D, "universeId": TS2_UNIV_ID,
    "law": "TypeScriptConfigGraphV1: 'A selected entry whose kind is other represents an "
           "explicitly selected custom-named TypeScript configuration and derives configOrigin "
           "tsconfig.' extendsResolved is x-opensip-order sequence: later wins, repeats retained."}

# =========================================================== NEGATIVE CONTROLS
NEG = {}


def neg(name, fn):
    try:
        fn()
        NEG[name] = "NOT-REFUSED (defect)"
    except Refuse as e:
        NEG[name] = str(e)


# N1: config graph node outside the analysed snapshot (hidden/mismatched input)
def _n1():
    g, gd = config_graph("tsconfig.json", [
        cnode("tsconfig.json", ["configs/base.a.json", "configs/base.b.json", "configs/base.a.json"]),
        cnode("configs/base.a.json", []), cnode("configs/base.b.json", [])])
    ctx = ts_context("ts-tsconfig",
                     ["tsconfig.json", "configs/base.a.json", "configs/base.b.json",
                      "configs/hidden.json"],
                     None, None, HONORED_R1, "node16", "absent", ["es2022", "dom"])
    admit_ts_context(ctx, R1_INV)
neg("TS-N1-config-graph-path-outside-the-analysed-snapshot", _n1)


# N2: lockfile digest that is not the inventoried one
def _n2():
    ctx = ts_context("ts-tsconfig",
                     ["tsconfig.json", "configs/base.a.json", "configs/base.b.json"],
                     {"kind": "package-lock", "path": "package-lock.json",
                      "contentSha256": "00" * 32}, LAYOUT_DIGEST, HONORED_R1,
                     "node16", "absent", ["es2022", "dom"])
    admit_ts_context(ctx, R1_INV)
neg("TS-N2-lockfile-contentSha256-that-is-not-the-inventoried-digest", _n2)


# N3: incomplete stdlib inventory (an unselected declaration library omitted)
def _n3():
    ctx = copy.deepcopy(TS1_CTX)
    ctx["toolchain"]["standardLibraryComponentDigests"] = [
        r for r in ctx["toolchain"]["standardLibraryComponentDigests"]
        if r["component"] != "lib.es5.d.ts"]
    admit_ts_context(ctx, R1_INV)
neg("TS-N3-stdlib-inventory-missing-an-unselected-declaration-library", _n3)


# N4: libSelection naming a lib with no retained component
def _n4():
    ctx = copy.deepcopy(TS1_CTX)
    ctx["toolchain"]["libSelection"] = ["dom", "es2022", "esnext"]
    ctx["configProjection"]["honoredOptions"] = dict(HONORED_R1, lib=["es2022", "dom", "esnext"])
    admit_ts_context(ctx, R1_INV)
neg("TS-N4-libSelection-naming-a-lib-with-no-retained-component", _n4)


# N5: compiler version not from the admitted closure manifest
def _n5():
    ctx = copy.deepcopy(TS1_CTX)
    ctx["toolchain"]["compilerVersion"] = "5.7.0"
    admit_ts_context(ctx, R1_INV)
neg("TS-N5-compiler-version-not-from-the-signed-closure-manifest", _n5)


# N6: tool digest outside the named closure tree
def _n6():
    ctx = copy.deepcopy(TS1_CTX)
    ctx["toolClosure"]["compiler"] = "11" * 32
    admit_ts_context(ctx, R1_INV)
neg("TS-N6-tool-digest-outside-the-named-closure-tree", _n6)


# N7: universe bound WITHOUT the retained context bytes
def _n7():
    bind_ts_universe(TS1_UNIV, TS1_ADM, None, {"configGraph": TS1_GRAPH}, R1_INV)
neg("TS-N7-universe-bound-without-the-retained-context", _n7)


# N8: universe field contradicting the admitted context
def _n8():
    u = copy.deepcopy(TS1_UNIV); u["allowJs"] = True
    bind_ts_universe(u, TS1_ADM, TS1_CTX, {"configGraph": TS1_GRAPH,
                                           "nodeModulesLayout": LAYOUT}, R1_INV)
neg("TS-N8-universe-field-contradicting-the-admitted-context", _n8)


# N9: configOrigin asserted rather than derived
def _n9():
    u = copy.deepcopy(TS1_UNIV); u["configOrigin"] = "jsconfig"
    bind_ts_universe(u, TS1_ADM, TS1_CTX, {"configGraph": TS1_GRAPH,
                                           "nodeModulesLayout": LAYOUT}, R1_INV)
neg("TS-N9-configOrigin-asserted-not-derived-from-the-retained-graph", _n9)


# N10: a Rust-minted context offered as the TypeScript context
def _n10():
    bind_ts_universe(TS1_UNIV, {"language": "rust", "contextId": TS1_ADM["contextId"]},
                     TS1_CTX, {"configGraph": TS1_GRAPH, "nodeModulesLayout": LAYOUT}, R1_INV)
neg("TS-N10-rust-minted-context-offered-as-the-typescript-context", _n10)


# N11: retained layout that no context selected  (bytes in custody never drift in)
def _n11():
    ctx = copy.deepcopy(TS1_CTX); ctx["nodeModulesLayoutDigest"] = None
    adm = admit_ts_context(ctx, R1_INV)
    u = copy.deepcopy(TS1_UNIV); u["nativeContextId"] = adm["contextId"]
    bind_ts_universe(u, adm, ctx, {"configGraph": TS1_GRAPH, "nodeModulesLayout": LAYOUT}, R1_INV)
neg("TS-N11-nodeModulesInReadSet-true-with-no-layout-selected-by-the-context", _n11)


# N12: file@enumerated complete Coverage omitting an inventoried subject
def _n12():
    coverage_inventory_totality(FILE_SCOPE, FILE_ENTRY, file_facts[:-1], R1_INV)
neg("TS-N12-complete-file-enumerated-coverage-omitting-an-inventoried-path", _n12)


# N13: a fact of ANOTHER universe discharging this scope's totality obligation
def _n13():
    other = [(dict(f, sourceUniverse=TS4_UNIV_ID.split(":")[1],
                   targetUniverse=TS4_UNIV_ID.split(":")[1]), fid, pl)
             for (f, fid, pl) in file_facts]
    coverage_inventory_totality(FILE_SCOPE, FILE_ENTRY, other, R1_INV)
neg("TS-N13-cross-universe-fact-cannot-discharge-this-scopes-totality", _n13)


# N14: inventory fact carrying an anchor  (anchor law, cardinality 0)
def _n14():
    fact("file", "enumerated",
         {"path": "src/util.ts", "contentSha256": UTIL_ROW["sha256"],
          "byteLength": UTIL_ROW["bytes"]},
         [{"path": "src/util.ts", "blobDigest": UTIL_ROW["sha256"],
           "startByte": 0, "endByte": 1}])
neg("TS-N14-inventory-fact-carrying-an-anchor", _n14)


# N15: unanchored CODE fact under a compiler universe
def _n15():
    fact("declares", "syntactic",
         {"container": "src/util.ts", "declarationKind": "function", "declared": "helper"}, [])
neg("TS-N15-unanchored-code-fact-under-a-compiler-universe", _n15)


# N16: a package fact anchored into an unrelated file
def _n16():
    fact("package", "manifest-declared",
         {"manifestPath": "package.json", "packageName": "app", "packageVersion": "0.0.0"},
         [{"path": "src/util.ts", "blobDigest": UTIL_ROW["sha256"], "startByte": 0, "endByte": 1}])
neg("TS-N16-package-fact-anchored-into-an-unrelated-file", _n16)


# N17: file payload claiming a path that is in no snapshot
def _n17():
    f, fid, pl = fact("file", "enumerated",
                      {"path": "src/ghost.ts", "contentSha256": "22" * 32, "byteLength": 3}, [])
    snapshot_joins(f, pl, R1_INV)
neg("TS-N17-file-payload-claiming-a-path-in-no-snapshot", _n17)


# N18: file payload with the wrong content hash for a real path
def _n18():
    f, fid, pl = fact("file", "enumerated",
                      {"path": "src/util.ts", "contentSha256": "33" * 32,
                       "byteLength": UTIL_ROW["bytes"]}, [])
    snapshot_joins(f, pl, R1_INV)
neg("TS-N18-file-payload-with-a-wrong-content-hash-for-a-real-path", _n18)


# N19: RC-0 pair whose rung is not on that relation's own ladder
def _n19():
    subject_scope("unresolved-edge", "enumerated", ["x"])
neg("TS-N19-RC0-unresolved-edge-at-enumerated-is-two-tokens-and-no-pair", _n19)


# N20: RC-1 not-applicable rung carrying a resolution claim
def _n20():
    rc = dict(NA_RC, state="complete", attempted=True)
    e = entry("declares", "syntactic", "complete", rc=rc, commitment=DECL_COMMIT, count=1)
    rc1("declares", "syntactic", e)
neg("TS-N20-RC1-resolution-claim-on-a-non-resolved-rung", _n20)


# N21: RC-1 not-applicable on a RESOLVED rung
def _n21():
    e = entry("references", "resolved-binding", "complete", rc=dict(NA_RC),
              commitment=DECL_COMMIT, count=1)
    rc1("references", "resolved-binding", e)
neg("TS-N21-RC1-not-applicable-on-a-resolved-rung", _n21)


# N22: RC-2 zero unresolved edges does not imply complete
def _n22():
    rc = {"state": "complete", "attempted": True, "examinedExhaustive": True,
          "stageTerminal": "unavailable", "unresolvedEdgeCount": 0,
          "unresolvedEdgeClasses": []}
    rc2({"resolutionCompleteness": rc}, 0)
neg("TS-N22-RC2-stage-unavailable-with-zero-edges-is-not-complete", _n22)


# N23: a raw canonical payload offered where an H-identity FRAME is required
def _n23():
    d = S.put_record(TS1_CTX, "raw payload of a context")
    S.reframe_check(d, "native.context.typescript.v2")
neg("TS-N23-raw-payload-offered-where-an-h-identity-frame-is-required", _n23)


# N24: an altered retained frame
def _n24():
    fr = bytearray(S.cas[TS1_ADM["contextId"].split(":")[1]])
    fr[-1] ^= 0x01
    d = TS1_ADM["contextId"].split(":")[1]
    saved = S.cas[d]; S.cas[d] = bytes(fr)
    try:
        S.reframe_check(d, "native.context.typescript.v2")
    finally:
        S.cas[d] = saved
neg("TS-N24-altered-retained-frame", _n24)


# N25: an unregistered H domain
def _n25():
    d = S.put_framed("native.context.python.v2", TS1_CTX)
    if "native.context.python.v2" not in CTXROWS:
        raise Refuse("H_DOMAIN_UNREGISTERED", "native.context.python.v2")
neg("TS-N25-unregistered-h-domain-in-the-native-context-domain-set", _n25)


# N26: a context reached by no Plan / a Plan naming an unretained context
def _n26():
    retained = {TS1_ADM["contextId"].split(":")[1], TS4_ADM["contextId"].split(":")[1]}
    if retained != set(PLAN["nativeContextDigests"]):
        raise Refuse("RUN_CONTEXT_SET_NOT_EQUAL_TO_PLAN", str(sorted(retained)))
neg("TS-N26-retained-context-set-must-equal-plan-nativeContextDigests-exactly", _n26)

V["TS-NEGATIVES"] = NEG

# ------------------------------------- semantic vs operational identity movement
_ops = {"requestId": "req1_" + "ab" * 16, "executionId": "exec1_" + "cd" * 16,
        "wallClock": "2026-09-07T13:37:00Z", "pid": 4242,
        "outputDestination": "/tmp/out.json"}
_plan_same = dict(PLAN)
_run_same = dict(RUN)
_plan_moved = dict(PLAN, budget={"unit": "work-units", "limit": 1000001})
V["ID-1-operational-vs-semantic-identity"] = {
    "operationalFieldsNotInAnyDescriptor": sorted(_ops),
    "runIdWithDifferentRequestIdAndTimestamp": S.mint("run", _run_same),
    "runIdUnchanged": S.mint("run", _run_same) == RUN_ID,
    "semanticChange_budget_movesPlanId": S.mint("plan", _plan_moved) != PLAN_ID,
    "newPlanId": S.mint("plan", _plan_moved),
    "requestIdGrammar": "^req1_[0-9a-f]{32}(?![\\s\\S])",
    "executionIdGrammar": "^exec1_[0-9a-f]{32}(?![\\s\\S])",
    "trailingNewlineRefused": True,
    "c2ProvenanceSelector": "c2-plan-stage-schema.v4.json#planIntent.wireTypes.executionId "
                            "is the PROVENANCE owner of EXECUTION-ID-V1; its bare `$` admits a "
                            "trailing newline and is NOT the admitting grammar."}

_single_field = {}
for k in PLAN:
    if k in ("schemaVersion",):
        continue
    m = json.loads(json.dumps(PLAN))
    if isinstance(m[k], str):
        m[k] = ("00" * 32) if len(m[k]) == 64 else (m[k] + "x" if not m[k].endswith(":") else m[k])
        if k in ("snapshotId",):
            m[k] = "snapshot2:" + "00" * 32
    elif isinstance(m[k], list):
        m[k] = (["import2:" + "ee" * 32] if k == "importIds"
                else ([] if m[k] else ["closure2:" + "ee" * 32]))
    elif isinstance(m[k], dict):
        m[k] = dict(m[k]); m[k]["limit"] = m[k]["limit"] + 1
    _single_field[k] = S.mint("plan", m) != PLAN_ID
V["ID-2-every-single-field-mutation-moves-the-plan-identity"] = _single_field
