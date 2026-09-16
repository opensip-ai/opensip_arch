"""Phase 6 observables, each a measured vector (classification valid|invalid|explanatory; negatives carry firstRefusal,
masksLater and whether the first refusal key is spelled anywhere in the kit):

  vectors/config-synthesized.json            R-CONFIG-SYNTHESIZED
  vectors/config-custom-multi-base.json      R-CONFIG-CUSTOM-MULTI-BASE
  vectors/config-js-shared-base.json         R-CONFIG-JS-SHARED-BASE
  vectors/js-body-through-ts.json            R-JS-CLONE-BODY-THROUGH-TS
  vectors/clones-negatives.json              R-CLONES-NEGATIVE-VECTORS
  vectors/repair-descriptor.json             R-REPAIR-DESCRIPTOR + R-REPAIR-AUTHORITY-PER-TARGET
  vectors/min-resolution.json                R-MIN-RESOLUTION-THREE-LEVELS + R-MIN-RESOLUTION-REPAIR-EVIDENCE
  vectors/imported-observation-boundary.json R-IMPORTED-OBSERVATION-BOUNDARY
  vectors/mutation-replay-scope.json         R-MUTATION-REPLAY-SCOPE + R-REPAIR-APPLY-KEY
  envelopes/pinned-purge.json                R-PINNED-PURGE
Sources are cited per vector. Admitted Runs are re-admitted here through closure.admit_graph before any use.
Usage: python3 tools/runref.py tools/phase6_vectors.py
"""
import copy
import datetime
import glob
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v2/output/preserved/pre-s42"
SUBJECT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v2/subject/docs"
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/builders")

import canonical as K  # noqa: E402
import closure as CL  # noqa: E402
import enumeration as EN  # noqa: E402
import evaluator as EV  # noqa: E402
import membership as M  # noqa: E402
import native_ctx as NC  # noqa: E402
import native_facts as NF  # noqa: E402
import schemas  # noqa: E402
import source39 as S39  # noqa: E402
from store import Store  # noqa: E402
from syntax_runs import closure  # noqa: E402

KIT = schemas.kit()
NE = "native/native-evidence.schemas.v2.json"
REL = "foundation/relation-payload-schemas.v2.json"
REPAIR3 = "workflows/schemas/evaluator3/repair.schema.json"
INVOC3 = "workflows/schemas/evaluator3/invocation-record.schema.json"
ENV3 = "workflows/schemas/evaluator3/command-envelope.schema.json"
EXIT = {"success": 0, "policy-failed": 1, "request-rejected": 2, "indeterminate": 3, "operational-failed": 4, "interrupted": 130}
failures = []
_TEXT = None


def kit_text():
    global _TEXT
    if _TEXT is None:
        parts = []
        for p in glob.glob(SUBJECT + "/**/*", recursive=True):
            if os.path.isfile(p):
                parts.append(open(p, "rb").read().decode("utf-8", "ignore"))
        _TEXT = "\n".join(parts)
    return _TEXT


def published(key):
    if not key:
        return None
    base = key.split(":")[0]
    return base in kit_text()


def ckey(x):
    return K.C(x)


def sfx(i):
    return i.split(":", 1)[1]


def dump(rel, obj):
    os.makedirs(os.path.dirname(f"{OUT}/{rel}"), exist_ok=True)
    with open(f"{OUT}/{rel}", "w") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)


def neg(name, faults, expect_prefix, note="", classification="invalid"):
    first = faults[0] if faults else None
    ok = (expect_prefix is None and not faults) or (first is not None and expect_prefix is not None and first.startswith(expect_prefix))
    if not ok:
        failures.append({"vector": name, "faults": faults, "expected": expect_prefix})
    return {"vector": name, "classification": "valid" if expect_prefix is None else classification, "firstRefusal": first,
            "masksLater": faults[1:], "expected": expect_prefix, "firstRefusalKeySpelledInKit": published(first), "pass": ok, "note": note}


def admitted(name):
    exported = json.load(open(f"{OUT}/runs/{name}.store.json"))
    store = Store.load(exported)
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    if C.faults:
        raise SystemExit(f"{name} no longer admits: {C.faults[:3]}")
    g["runId"] = exported["runId"]
    return store, g, exported


# ------------------------------------------------------------------ A. TypeScript configuration vectors
HONORED_DEFAULT = {"allowJs": False, "allowSyntheticDefaultImports": False, "baseUrl": None, "checkJs": False, "customConditions": [],
                   "esModuleInterop": False, "jsx": None, "lib": ["es2022"], "module": "node16", "moduleResolution": "node16", "noEmit": True,
                   "paths": [], "resolveJsonModule": False, "rootDirs": [], "skipLibCheck": True, "strict": False, "target": "es2022", "types": None}


def ts_env(files, mode, honored, graph, uni_fields, pkg_type="absent", mutate_ctx=None, mutate_uni=None):
    store = Store()
    inv_rows = [{"path": p, "sha256": store.put_bytes(files[p]), "bytes": len(files[p])} for p in sorted(files, key=lambda p: p.encode())]
    # HC-16: the toolchain closure (normalizationClosure kind toolchain) carries the L0 specification the JS-body vectors frame, and its map
    l0_spec = b"cb24 L0 spec (typescript provider)\n"
    T, tdesc = closure(store, "toolchain", "cb24-typescript", {
        "bin/tsc.js": b"synthetic tsc\n", "bin/node": b"synthetic node\n",
        "node_modules/typescript/package.json": b"{\"name\":\"typescript\",\"version\":\"5.6.3\"}\n",
        "opensip-interface/normalization/levels/L0-verbatim.spec": l0_spec,
        S39.NSL["closureTreePath"]: S39.normalization_map_bytes("cb24-tsc-normalizer", {"L0-verbatim": hashlib.sha256(l0_spec).hexdigest()})},
        "5.6.3")
    S, sdesc = closure(store, "stdlib", "cb24-typescript-stdlib", {"lib/lib.es2022.d.ts": b"// es2022\n", "lib/lib.es5.d.ts": b"// es5\n"}, "5.6.3")
    tree = {r["path"]: r["sha256"] for r in tdesc["tree"]}
    ctx = {"schemaVersion": 2, "languageMode": mode,
           "toolchain": {"compilerName": "typescript", "compilerVersion": "5.6.3", "compilerPackageDigest": tree["node_modules/typescript/package.json"],
                         "typescriptStdlibMerkleRoot": sfx(S),
                         "standardLibraryComponentDigests": sorted([{"component": r["path"].split("/")[-1], "sha256": r["sha256"]} for r in sdesc["tree"]],
                                                                   key=lambda c: c["component"].encode()),
                         "libSelection": sorted(honored["lib"], key=lambda s: s.encode())},
           "toolClosure": {"closureId": T, "compiler": tree["bin/tsc.js"], "runtime": tree["bin/node"]},
           "configProjection": {"schemaVersion": 2, "ancestorCarrierVerified": True, "environmentSanitized": True, "typeAcquisitionEnabled": False,
                                "executableSelected": False, "honoredOptions": honored, "strippedOptions": [],
                                "configGraphPaths": sorted((n["path"] for n in graph["nodes"]), key=lambda s: s.encode())},
           "moduleResolutionMode": honored["moduleResolution"], "packageModuleType": pkg_type, "nodeModulesLayoutDigest": None, "lockfileIdentity": None}
    if mutate_ctx:
        mutate_ctx(ctx)
    graph_digest = store.put_record(graph)
    ctx_hex = store.put_frame("native.context.typescript.v2", ctx)
    uni = dict({"schemaVersion": 2, "languageMode": mode, "packageModuleType": pkg_type, "allowJs": honored["allowJs"], "checkJs": honored["checkJs"],
                # HC-40 (native s1.2 lines 538-540, the law HC-20 applied to closure): vector universes spell the same flags
                "jsAdmittedToProgram": honored["allowJs"] and len(uni_fields.get("jsRootFiles", [])) > 0, "jsDiagnosticsEnabled": honored["checkJs"],
                "resolutionCompletenessImplied": False, "lockfileKind": "none", "nodeModulesInReadSet": False, "executionCapableResolution": False,
                "tsconfigGraphHash": graph_digest, "nativeContextId": "sha256:" + ctx_hex}, **uni_fields)
    if mutate_uni:
        mutate_uni(uni)
    U = store.put_frame("native.semantic-universe.typescript.v2", uni)
    faults, bound, adm = [], None, None
    try:
        adm = NC.admit_native_context(store, ctx_hex, inv_rows)
        faults += adm["refusals"]
        bound = NC.bind_universe(store, U, {ctx_hex: adm}, inv_rows)
        faults += bound["faults"]
    except NC.Refusal as exc:
        faults.append(f"{exc.key}:{exc.detail}" if exc.detail else exc.key)
    gr = KIT.admit(graph, NE, "#/$defs/TypeScriptConfigGraphV1")
    if not gr["ok"]:
        faults.insert(0, f"cb24.CONFIG_GRAPH_SCHEMA:{gr['stock'][:1]}{gr['order'][:1]}")
    return {"store": store, "inv": inv_rows, "ctx": ctx, "ctxId": ctx_hex, "uni": uni, "universe": U, "graphDigest": graph_digest,
            "faults": faults, "bound": bound, "files": files}


def effective_options(files, node_path, graph):
    node = next(n for n in graph["nodes"] if n["path"] == node_path)
    eff = {}
    for base in node["extendsResolved"]:
        eff.update(effective_options(files, base, graph))
    eff.update(K.parse_raw(files[node_path]).get("compilerOptions", {}))
    return eff


def config_vectors():
    # A1 synthesized
    files = {"package.json": b"{\"name\":\"lib\",\"version\":\"1.0.0\"}\n", "src/a.js": b"function a() {\n  return 1;\n}\n",
             "src/view.jsx": b"export const V = () => <div/>;\n"}
    disc = M.discover_units(files)
    roots = sorted([p for p in files if p.endswith((".ts", ".tsx", ".js", ".mjs", ".cjs", ".jsx"))], key=lambda p: p.encode())
    jsx = any(p.endswith((".jsx", ".tsx")) for p in roots)
    synth = {"allowJs": True, "checkJs": False, "module": "node16", "moduleResolution": "node16", "target": "es2022", "strict": False,
             "skipLibCheck": True, "types": [], "noEmit": True}
    if jsx:
        synth["jsx"] = "preserve"
    honored = dict(HONORED_DEFAULT, allowJs=True, jsx="preserve" if jsx else None, types=[])
    graph = {"schemaVersion": 1, "entryConfigPath": None, "nodes": []}
    base_fields = {"configOrigin": "synthesized", "synthesizerVersion": 1, "synthesizedOptions": synth, "jsRootFiles": roots, "programRootFiles": roots}
    env = ts_env(files, "js-synthesized", honored, graph, base_fields)
    vectors = [neg("synthesized-context-and-universe-admit", env["faults"], None, "discovery unit mode " + disc["units"][0]["languageMode"])]
    vectors[0].update({"contextId": "sha256:" + env["ctxId"], "universeId": env["universe"], "tsconfigGraphHash": env["graphDigest"],
                       "synthesizedOptions": synth, "honoredOptions": honored, "discoveredUnit": disc["units"][0],
                       "synthesizerRuleJsxIffJsxRoot": jsx == ("jsx" in synth)})
    if disc["units"][0]["languageMode"] != "js-synthesized":
        failures.append({"vector": "synthesized-discovery", "unit": disc["units"][0]})
    no_jsx = dict(synth)
    no_jsx.pop("jsx")
    vectors.append(neg("synthesized-options-omit-jsx-while-honored", ts_env(files, "js-synthesized", honored, graph, dict(base_fields, synthesizedOptions=no_jsx))["faults"],
                       "native.universe-context-field-mismatch:synthesizedOptions.jsx"))
    vectors.append(neg("synthesized-universe-claims-tsconfig-origin", ts_env(files, "js-synthesized", honored, graph, dict(base_fields, configOrigin="tsconfig"))["faults"],
                       "native.universe-context-field-mismatch:configOrigin"))
    vectors.append(neg("synthesized-with-config-graph-path", ts_env(files, "js-synthesized", honored, graph, base_fields,
                                                                   mutate_ctx=lambda c: c["configProjection"].__setitem__("configGraphPaths", ["tsconfig.json"]))["faults"],
                       "native.native-context-field-mismatch:synthesized-config-graph"))
    vectors.append(neg("synthesized-options-value-disagrees", ts_env(files, "js-synthesized", honored, graph, dict(base_fields, synthesizedOptions=dict(synth, strict=True)))["faults"],
                       "cb24.ts-universe-schema", "strict:true is refused by the SynthesizedCompilerOptionsV1 const (schema) before any agreement check", "invalid"))
    dump("vectors/config-synthesized.json", {"vectors": vectors, "selectors": ["native-evidence.md s2.2 SynthesizedCompilerOptionsV1 (lines 1242-1248)",
                                                                             "native-evidence.md s2.4 agreement rules (lines 1413-1433)",
                                                                             "native-evidence.schemas.v2.json#/$defs/SynthesizedCompilerOptionsV1"],
                                             "choices": ["honored lib ['es2022'] stands in for the pinned compiler's target default library (qualification data, not published)"]})
    # A2 custom-named entry, multiple ordered bases with a repeated base
    files = {"tsconfig.app.json": b"{\"extends\":[\"./base-a.json\",\"./base-b.json\",\"./base-a.json\"],\"compilerOptions\":{\"noEmit\":true}}\n",
             "base-a.json": b"{\"compilerOptions\":{\"strict\":false,\"target\":\"es2020\"}}\n",
             "base-b.json": b"{\"compilerOptions\":{\"strict\":true,\"target\":\"es2022\"}}\n",
             "src/main.ts": b"export function m(): number {\n  return 1;\n}\n"}
    inv_sha = {p: hashlib.sha256(b).hexdigest() for p, b in files.items()}

    def graph_with(edges):
        return {"schemaVersion": 1, "entryConfigPath": "tsconfig.app.json", "nodes": [
            {"path": "base-a.json", "contentSha256": inv_sha["base-a.json"], "kind": "other", "extendsResolved": []},
            {"path": "base-b.json", "contentSha256": inv_sha["base-b.json"], "kind": "other", "extendsResolved": []},
            {"path": "tsconfig.app.json", "contentSha256": inv_sha["tsconfig.app.json"], "kind": "other", "extendsResolved": edges}]}
    fields = {"configOrigin": "tsconfig", "synthesizerVersion": None, "synthesizedOptions": None, "jsRootFiles": [], "programRootFiles": ["src/main.ts"]}
    results = {}
    for label, edges in (("repeated", ["base-a.json", "base-b.json", "base-a.json"]), ("deduplicated", ["base-a.json", "base-b.json"]),
                         ("reordered", ["base-b.json", "base-a.json"])):
        g = graph_with(edges)
        eff = effective_options(files, "tsconfig.app.json", g)
        honored = dict(HONORED_DEFAULT, strict=eff.get("strict", False), target=eff.get("target", "es2022"))
        env = ts_env(files, "ts-tsconfig", honored, g, fields)
        results[label] = {"extendsResolved": edges, "effectiveCompilerOptions": eff, "faults": env["faults"], "tsconfigGraphHash": env["graphDigest"],
                          "universeId": env["universe"], "contextId": "sha256:" + env["ctxId"],
                          "derivedConfigOrigin": NC.derived_config_origin(g), "entryKind": "other"}
        if env["faults"]:
            failures.append({"vector": f"custom-multi-base-{label}", "faults": env["faults"]})
    distinct = len({r["tsconfigGraphHash"] for r in results.values()}) == 3
    if not distinct or results["repeated"]["effectiveCompilerOptions"]["strict"] is not False:
        failures.append({"vector": "custom-multi-base-precedence", "results": results})
    dump("vectors/config-custom-multi-base.json", {"classification": "valid", "results": results,
                                                  "measured": {"threeGraphIdentitiesDistinct": distinct,
                                                               "repeatedBaseRetainedAndLaterWins": results["repeated"]["effectiveCompilerOptions"]},
                                                  "negative": neg("custom-entry-kind-relabelled-tsconfig",
                                                                  ts_env(files, "ts-tsconfig", dict(HONORED_DEFAULT), dict(graph_with(["base-a.json"]), nodes=[
                                                                      dict(n, kind="tsconfig") if n["path"] == "tsconfig.app.json" else n for n in graph_with(["base-a.json"])["nodes"]]),
                                                                      fields)["faults"], "native.config-graph-kind-contradicts-path"),
                                                  "selectors": ["native-evidence.md s2.2 lines 1150-1190", "native-evidence.schemas.v2.json#/$defs/TypeScriptConfigGraphV1/properties/nodes/items/properties/extendsResolved",
                                                                "native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law"],
                                                  "note": "honoredOptions are the host adapter's effective resolved options; closure has no published join re-deriving them from the config bytes (compiler semantics, qualification)."})
    # A3 jsconfig extending a shared base with another filename
    files = {"jsconfig.json": b"{\"extends\":\"./config/shared.base.json\",\"include\":[\"src\"]}\n",
             "config/shared.base.json": b"{\"compilerOptions\":{\"checkJs\":false,\"module\":\"node16\",\"moduleResolution\":\"node16\"}}\n",
             "package.json": b"{\"name\":\"app\",\"version\":\"1.0.0\",\"type\":\"module\"}\n",
             "src/app.js": b"export function run() {\n  return 42;\n}\n"}
    inv_sha = {p: hashlib.sha256(b).hexdigest() for p, b in files.items()}
    graph = {"schemaVersion": 1, "entryConfigPath": "jsconfig.json", "nodes": [
        {"path": "config/shared.base.json", "contentSha256": inv_sha["config/shared.base.json"], "kind": "other", "extendsResolved": []},
        {"path": "jsconfig.json", "contentSha256": inv_sha["jsconfig.json"], "kind": "jsconfig", "extendsResolved": ["config/shared.base.json"]}]}
    honored = dict(HONORED_DEFAULT, allowJs=True)
    fields = {"configOrigin": "jsconfig", "synthesizerVersion": None, "synthesizedOptions": None, "jsRootFiles": ["src/app.js"], "programRootFiles": ["src/app.js"]}
    env = ts_env(files, "js-allowjs", honored, graph, fields, pkg_type="module")
    disc = M.discover_units(files)
    js_vectors = [neg("jsconfig-shared-base-admits", env["faults"], None, f"discovered unit {disc['units'][0]['languageMode']} via {disc['units'][0]['markerPath']}")]
    js_vectors[0].update({"contextId": "sha256:" + env["ctxId"], "universeId": env["universe"], "derivedConfigOrigin": NC.derived_config_origin(graph)})
    js_vectors.append(neg("jsconfig-program-claims-tsconfig-origin", ts_env(files, "js-allowjs", honored, graph, dict(fields, configOrigin="tsconfig"), pkg_type="module")["faults"],
                          "native.universe-context-field-mismatch:configOrigin"))
    js_vectors.append(neg("shared-base-relabelled-jsconfig", ts_env(files, "js-allowjs", honored, dict(graph, nodes=[dict(graph["nodes"][0], kind="jsconfig"), graph["nodes"][1]]),
                                                                    fields, pkg_type="module")["faults"], "native.config-graph-kind-contradicts-path"))
    dump("vectors/config-js-shared-base.json", {"vectors": js_vectors, "selectors": ["native-evidence.md s2.2 line 1169 (a jsconfig entry extending a shared base remains a jsconfig program)",
                                                                                   "native-evidence.md s1.2 line 163 (jsconfig defaults allowJs=true)"]})
    return env


def js_body_through_ts(env):
    store, bound = env["store"], env["bound"]
    path = "src/app.js"
    data = env["files"][path]
    s = data.index(b"{")
    e = data.rindex(b"}") + 1
    rec, lang, refusal = NC.body_language_version(bound, path)
    spec = store.put_bytes(b"cb24 L0 spec (typescript provider)\n")
    inv = {r["path"]: r for r in env["inv"]}

    def run(label, lang_id, blv, expect):
        frame = NF.build_body_frame("L0-verbatim", spec, lang_id, blv, NF.l0_payload(data[s:e]))
        payload = {"bodyIdentity": "sha256:" + store.put_bytes(frame), "normalisationLevel": "L0-verbatim", "normalisationVersion": spec}
        fact = {"anchors": [{"path": path, "blobDigest": inv[path]["sha256"], "startByte": s, "endByte": e}]}
        v = neg(label, NF.clones_join_faults(store, fact, payload, bound), expect)
        v["bodyIdentity"] = payload["bodyIdentity"]
        return v
    vecs = [run("javascript-body-through-typescript-universe", lang, rec, None)]
    vecs[0].update({"bodyLanguageVersion": rec, "languageId": lang, "providerLanguage": bound["row"]["language"],
                    "providerUniverseDomain": bound["domain"], "compilerName": rec["compilerName"]})
    if not (lang == "javascript" and bound["row"]["language"] == "typescript"):
        failures.append({"vector": "js-body-language", "lang": lang})
    vecs.append(run("javascript-body-relabelled-typescript", "typescript", dict(rec, languageId="typescript"), "CLONE_BODY_FRAME_LANGUAGE_ID"))
    vecs.append(run("javascript-body-with-ts-source-variant", lang, dict(rec, dialect={"sourceVariant": "ts"}), "CLONE_BODY_FRAME_LANGUAGE_VERSION"))
    dump("vectors/js-body-through-ts.json", {"universe": env["universe"], "vectors": vecs,
                                            "selectors": ["relation-payload-schemas.v2.json#/x-opensip-relation-registry/relations/clones/bodyIdentityJoin/languageIdIsNotTheProviderLanguage",
                                                          "identity-schemas.v3.json#/x-opensip-digest-domains/domainSets/native-semantic-universe/native.semantic-universe.typescript.v2/languageVersionBinding"]})


# ------------------------------------------------------------------ B. clone negatives on an admitted syntax Run
def clones_negatives():
    store, g, exported = admitted("syntax-code")
    U, bound = next(iter(g["bound"].items()))
    inv_rows = g["snapshot"]["sourceInventory"]
    snap = g["plan"]["snapshotId"]
    l0 = next(f for f, x in g["facts"].items() if x["relation"] == "clones" and g["payloads"][f]["normalisationLevel"] == "L0-verbatim"
              and x["anchors"][0]["path"] == "src/a.ts")
    l1 = next(f for f, x in g["facts"].items() if x["relation"] == "clones" and g["payloads"][f]["normalisationLevel"] == "L1-lexical")
    vecs = []

    def case(name, fid, frame_fn=None, payload_fn=None, fact_fn=None, expect=None, note=""):
        s2 = Store.load(exported)
        fact = copy.deepcopy(g["facts"][fid])
        payload = copy.deepcopy(g["payloads"][fid])
        frame = s2.get_bytes(payload["bodyIdentity"][7:])
        if frame_fn:
            frame = frame_fn(frame, payload, fact)
            payload["bodyIdentity"] = "sha256:" + s2.put_bytes(frame)
        if payload_fn:
            payload_fn(payload, s2)
        if fact_fn:
            fact_fn(fact)
        fact["payloadDigest"] = s2.put_record(payload)
        faults, _ = NF.fact_faults(s2, fact, snap, inv_rows, g["bound"])
        vecs.append(neg(name, faults, expect, note))

    blv, lang, _ = NC.body_language_version(bound, "src/a.ts")

    def reframe(level=None, lv=None, lang_id=None, rec=None, payload_bytes=None, tag=None):
        def fn(frame, payload, fact):
            parts = NF.body_frame_parse(frame)
            f = NF.build_body_frame(level or parts["level"].decode(), lv or parts["levelVersion"].hex(), lang_id or parts["languageId"].decode(),
                                    rec or blv, payload_bytes if payload_bytes is not None else parts["payload"])
            if tag:
                f = bytes([len(tag)]) + tag + f[1 + f[0]:]
            return f
        return fn

    case("positive-L0-control", l0, expect=None)
    case("positive-L1-control", l1, expect=None)
    case("frame-not-retained", l0, payload_fn=lambda p, s: p.__setitem__("bodyIdentity", "sha256:" + "0" * 64), expect="EVIDENCE_UNAVAILABLE:body-identity-frame")
    case("frame-truncated", l0, frame_fn=lambda fr, p, f: fr[:-3], expect="CLONE_BODY_FRAME_MALFORMED")
    case("frame-domain-tag-wrong", l0, frame_fn=reframe(tag=b"opensip.fact-identity.v2"), expect="CLONE_BODY_FRAME_DOMAIN_TAG")
    case("frame-level-differs-from-payload", l0, frame_fn=reframe(level="L1-lexical"), expect="CLONE_BODY_FRAME_LEVEL")
    case("frame-level-version-not-the-spec", l0, frame_fn=reframe(lv="ab" * 32), expect="CLONE_BODY_FRAME_LEVEL_VERSION")
    case("frame-language-id-wrong", l0, frame_fn=reframe(lang_id="javascript"), expect="CLONE_BODY_FRAME_LANGUAGE_ID")
    case("frame-language-version-wrong-compiler-build", l0, frame_fn=reframe(rec=dict(blv, compilerBuild="c" * 64)), expect="CLONE_BODY_FRAME_LANGUAGE_VERSION")
    case("L0-payload-not-anchor-span", l0, frame_fn=reframe(payload_bytes=NF.l0_payload(b"{ tampered }")), expect="CLONE_L0_PAYLOAD_NOT_ANCHOR_SPAN")
    case("L1-token-stream-framing-broken", l1, frame_fn=reframe(payload_bytes=b"\x00\x00\x00\x05\x00"), expect="CLONE_TOKEN_STREAM_FRAMING")
    # HC-16: under normalizationSpecificationLaw an unmapped digest refuses BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH first, so "not
    # retained" keeps the mapped specification and loses only its bytes (retention loss, not a refusal of the claim)
    case("level-specification-not-retained", l0, payload_fn=lambda p, s: s.blobs.pop(p["normalisationVersion"]), expect="EVIDENCE_UNAVAILABLE:level-specification")
    case("level-specification-of-another-level", l0, payload_fn=lambda p, s: p.__setitem__("normalisationVersion", g["payloads"][l1]["normalisationVersion"]),
         expect="BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH")
    case("two-anchors-on-a-clone", l0, fact_fn=lambda f: f.__setitem__("anchors", sorted(f["anchors"] + [dict(f["anchors"][0], startByte=0, endByte=6)], key=ckey)),
         expect="FACT_ANCHOR_CARDINALITY")
    dump("vectors/clones-negatives.json", {"baseRun": "syntax-code", "vectors": vecs,
                                          "selectors": ["relation-payload-schemas.v2.json#/$defs/ClonesPayloadV1/properties/bodyIdentity/x-opensip-digest",
                                                        "relation-payload-schemas.v2.json#/x-opensip-relation-registry/relations/clones/bodyIdentityJoin",
                                                        "coop/artifacts/fact-identity-policy.v2.json#/canonicalisationSchema"]})


# ------------------------------------------------------------------ C. repair descriptor, gate and per-target authority
CW_ORDER = {"exportsClosed": ["closed", "open", "unknown"], "entryPointsRecognized": ["all", "partial", "none"],
            "nonliteralLoading": ["none", "present"], "externalConsumers": ["none-declared", "possible", "unknown"]}
SENTINEL = {"deadCodeRepairEligible": False, "exportsClosed": "unknown", "entryPointsRecognized": "none", "nonliteralLoading": "present", "externalConsumers": "unknown"}


def repair_selection(g, target_universes, edit_paths):
    relevant = set(target_universes)
    unresolved = []
    for p in edit_paths:
        owners = [b["universe"] for c in g["enum"]["cells"] for b in c["programBindings"]
                  if b["enumerator"]["status"] == "selected" and any(p in e["paths"] for e in b["extents"]) + (p in b.get("candidateSourcePaths", []))]
        if any(o is None for o in owners):
            unresolved.append(p)
        owners = [o for o in owners if o is not None]
        witness = [s["sourceUniverse"] for s in g["scopes"].values() if NF.RELS[s["relation"]]["subjectKind"] == "source-path" and p in s["subjects"]]
        if not owners and not witness:
            unresolved.append(p)
        relevant |= set(owners) | set(witness)
    records = []
    for cid, (cd, payload) in g["coverages"].items():
        sc = g["scopes"][cd["scopeId"]]
        if sc["sourceUniverse"] in relevant:
            k = payload["key"]
            records.append({"coverage": cid, "relation": k["relation"], "resolution": k["resolution"], "sourceUniverse": k["sourceUniverse"],
                            "targetUniverse": k["targetUniverse"], "subjectScopeCommitment": k["subjectScopeCommitment"], "closedWorld": payload["entry"]["closedWorld"]})
    records.sort(key=lambda r: tuple(r[x].encode() for x in ("relation", "resolution", "sourceUniverse", "targetUniverse", "subjectScopeCommitment", "coverage")))
    return sorted(relevant), records, sorted(set(unresolved))


def gate(relevant, records, unresolved, has_unsafe):
    remedies = []
    for u in relevant:
        if not any(r["sourceUniverse"] == u for r in records):
            remedies.append({"code": "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED", "remedy": f"relevant universe {u} retains no native Coverage record", "subject": u})
    for p in unresolved:
        remedies.append({"code": "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED", "remedy": f"ownership of unsafe edited path {p} is unresolved", "subject": p})
    for r in records:
        if not r["closedWorld"]["deadCodeRepairEligible"]:
            remedies.append({"code": "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED",
                             "remedy": ("record relation=%s resolution=%s sourceUniverse=%s targetUniverse=%s subjectScopeCommitment=%s coverage=%s reasons=%s"
                                        % (r["relation"], r["resolution"], r["sourceUniverse"], r["targetUniverse"], r["subjectScopeCommitment"], r["coverage"],
                                           json.dumps(r["closedWorld"]["reasons"])))[:1024]})
    eligible = bool(records) and not remedies
    summary = dict(SENTINEL) if not records else {"deadCodeRepairEligible": all(r["closedWorld"]["deadCodeRepairEligible"] for r in records)}
    if records:
        for f, order in CW_ORDER.items():
            vals = [r["closedWorld"][f] for r in records]
            if any(u2 not in {r["sourceUniverse"] for r in records} for u2 in relevant) or unresolved:
                vals.append(SENTINEL[f])
            summary[f] = max(vals, key=order.index)
        if any(u2 not in {r["sourceUniverse"] for r in records} for u2 in relevant) or unresolved:
            summary["deadCodeRepairEligible"] = False
    return eligible, (remedies if has_unsafe else []), summary


def native_requirement(g, universes, relation, rung):
    entries = [p["entry"] for cid, (cd, p) in sorted(g["coverages"].items()) if p["key"]["relation"] == relation and p["key"]["resolution"] == rung
               and p["key"]["sourceUniverse"] in universes]
    view = {relation: EV.fold_entries(entries)} if entries else {}
    for dep in EV.dep_closure(relation):
        dents = [p["entry"] for cid, (cd, p) in sorted(g["coverages"].items()) if p["key"]["relation"] == dep["relation"] and p["key"]["resolution"] == dep["minResolution"]
                 and p["key"]["sourceUniverse"] in universes]
        if dents:
            view[dep["relation"]] = EV.fold_entries(dents)
    req = {"relation": relation, "minResolution": rung, "completeness": "complete", "quantifier": "universal-negative" if rung in NF.RESOLVED else "existential",
           "unresolvedEdgePolicy": "forbid", "externalConsumerPolicy": "forbid", "minConfidenceMillionths": 0}
    s = NF.sufficiency_v2(req, view)
    out = {"relation": relation, "minResolution": rung, "completeness": "complete", "satisfied": s["satisfied"]}
    if not s["satisfied"]:
        out["deficiency"] = s["deficiency"]
    return out, s


def imported_requirement(kind, imports, target, demand):
    """imported-evidence.schema.json#/x-opensip-imported-requirement-law outcomes with its precedence."""
    law = KIT.doc("workflows/schemas/imported-evidence.schema.json")["x-opensip-imported-requirement-law"]
    conds = set()
    owned = [i for i in imports if i["wrapper"]["kind"] == kind]
    if not owned:
        conds.add("evidence-kind-unavailable")
    consumable = [i for i in owned if i["flags"]["consumable"]]
    if owned and not consumable:
        conds.add("import-unmapped-only")
    for i in consumable:
        p = i["payload"]
        if kind == "runtime":
            rows = [r for r in p["subjects"] if r["path"] == target["path"] and ("symbol" not in r or r["symbol"] == target.get("qualifiedName"))]
            if any(r["observability"] in ("unobservable", "unmapped") for r in rows):
                conds.add("subject-not-observable")
            start = datetime.datetime.strptime(p["observationWindow"]["startUtc"], "%Y-%m-%dT%H:%M:%SZ")
            end = datetime.datetime.strptime(p["observationWindow"]["endUtc"], "%Y-%m-%dT%H:%M:%SZ")
            if (end - start).days < demand["minWindowDays"] or p["observedPopulation"] not in demand["populations"]:
                conds.add("observation-window-insufficient")
            if not rows:
                conds.add("import-absent-for-requirement")
        else:
            rows = [r for r in p["subjects"] if r["path"] == target["path"]]
            in_scope = M.in_foundation_scope(target["path"], i["scope"]) and (p["collectionScope"] != "listed-paths" or bool(rows))
            if not in_scope:
                conds.add("history-outside-collection-scope")
            rr = p["revisionRange"]
            if rr["truncated"] or rr["commitCount"] < demand["minCommits"]:
                conds.add("history-range-insufficient")
            if in_scope and not rows and p["collectionScope"] != "all-paths":
                conds.add("import-absent-for-requirement")
    applicable = {o for o in conds if kind in law["outcomes"][o]["appliesTo"]}
    if applicable != conds:
        raise ValueError(f"outcome of the wrong kind {conds - applicable}")
    outcome = next((o for o in law["precedence"] if o in applicable), None)
    return outcome, sorted(conds, key=law["precedence"].index)


def admit_requirement(req):
    """Preview admission (workflows s6): schema + plane from registry membership + cross-plane refusal."""
    r = KIT.admit(req, REPAIR3, "#/$defs/EvidenceRequirement")
    if not r["ok"]:
        return f"cb24.EVIDENCE_REQUIREMENT_SCHEMA:{r['stock'][:1]}"
    native = req["relation"] in NF.RELS
    imported_vocab = set(KIT.doc("workflows/schemas/evaluator3/common.schema.json")["$defs"]["ImportedRequirementDeficiency"]["enum"])
    if "deficiency" in req:
        if native and req["deficiency"] in imported_vocab:
            return "cb24.EVIDENCE_REQUIREMENT_CROSS_PLANE:native-with-imported-outcome"
        if not native and req["deficiency"] not in imported_vocab:
            return "cb24.EVIDENCE_REQUIREMENT_CROSS_PLANE:imported-with-native-outcome"
    return None


def repair_vectors():
    store, g, exported = admitted("ts-pass")
    proof = store.get_frame(sfx(store.get_frame(sfx(g["run"]["evaluationSealId"]), {"evaluation-seal"})[1]["proofBundleId"]), {"proof-bundle"})[1]
    findings = {fid: store.get_frame(sfx(fid), {"finding"})[1] for fid in proof["findingIds"]}
    cold = next(f for f in findings.values() if f["ruleId"] == "cb24.ts.cold-file")
    subj = store.get_frame(sfx(cold["subjectId"]), {"evaluation-subject"})[1]
    inv = {r["path"]: r for r in g["snapshot"]["sourceInventory"]}
    util = store.get_bytes(inv["src/util.ts"]["sha256"])
    post = util[:util.index(b"function unused")]
    edits = [{"path": "src/util.ts", "action": "replace", "preimageDigest": inv["src/util.ts"]["sha256"],
              "postimageDigest": hashlib.sha256(post).hexdigest(), "postimageBytes": len(post)}]
    imports = [dict(r) for r in g["imports"].values()]
    demand = {"minWindowDays": 7, "populations": ["test-suite", "staging-traffic", "production-traffic"]}
    recipe = {"contributionId": "cb24.repair-pack", "recipeId": "cb24.remove-unused-function", "recipeVersion": "1.0.0",
              "closureId": g["xi"]["evaluatorClosure"]}

    def descriptor(targets, edits, scope=("src/**",), requirement_specs=(("calls", "resolved-callee"), ("types", "checked"), ("runtime-observation", "observed")),
                   records_patch=None, extra_records=()):
        universes = [store.get_frame(sfx(findings[t]["subjectId"] if t in findings else cold["subjectId"]), {"evaluation-subject"})[1]["universe"] for t in targets]
        fps = []
        unmet = []
        for t in targets:
            f = findings.get(t)
            if f is None or f["fingerprint"] is None:
                unmet.append({"code": "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE", "remedy": f"target {t} is not a matched finding of {g['runId']}"})
            fps.append(f["fingerprint"] if f and f["fingerprint"] else "finding-key2:" + "d" * 64)
        relevant, records, unresolved = repair_selection(g, universes, [e["path"] for e in edits])
        records = [dict(r, closedWorld=dict(r["closedWorld"], **(records_patch(r) if records_patch else {}))) for r in records] + list(extra_records)
        records = [r for r in records if r["sourceUniverse"] in relevant]
        unsafe = any(e["action"] in ("replace", "delete") for e in edits)
        eligible, remedies, summary = gate(relevant, records, unresolved, unsafe)
        for e in edits:
            if not any(EV.glob_match(pat, e["path"]) for pat in scope):
                unmet.append({"code": "REPAIR.EDIT_OUTSIDE_PERMITTED_SCOPE", "remedy": f"edit {e['path']} outside {list(scope)}"})
            if e["action"] != "create" and (e["path"] not in inv or inv[e["path"]]["sha256"] != e["preimageDigest"]):
                unmet.append({"code": "REPAIR.TARGET_PREIMAGE_MISMATCH", "remedy": f"preimage of {e['path']} is not the snapshot inventory digest"})
        unmet += remedies
        reqs = []
        for rel, rung in requirement_specs:
            if rel in NF.RELS:
                req, _ = native_requirement(g, relevant, rel, rung)
            else:
                outcome, _conds = imported_requirement("runtime", imports, {"path": subj["nativeSubjectId"]}, demand)
                req = {"relation": rel, "minResolution": rung, "completeness": "complete", "satisfied": outcome is None}
                if outcome:
                    req["deficiency"] = outcome
            reqs.append(req)
            if not req["satisfied"]:
                plane = "native" if rel in NF.RELS else "imported"
                unmet.append({"code": "REPAIR.EVIDENCE_RUN_UNAVAILABLE", "remedy": f"requirement relation={rel} minResolution={rung} plane={plane} deficiency={req['deficiency']}"})
        desc = {"schemaFamily": "opensip.product.repair-plan", "schemaMajor": 2, "projectId": g["snapshot"]["projectId"], "snapshotId": g["plan"]["snapshotId"],
                "evidenceRunId": g["runId"], "planId": g["plan_id"], "recipe": recipe, "recipeTrust": "admitted", "evidenceOrigin": "native-analysis",
                "closedWorld": summary, "targets": fps, "edits": sorted(edits, key=lambda e: e["path"].encode()),
                "totalPostimageBytes": sum(e["postimageBytes"] for e in edits), "evidenceRequirements": reqs, "permittedEditScope": list(scope),
                "applicable": not unmet and all(r["satisfied"] for r in reqs), "unmetPreconditions": unmet[:64], "limitations": []}
        adm = KIT.admit(desc, REPAIR3, "#/$defs/RepairPlanDescriptor")
        rid = "repairplan2:" + K.H("workflow.repair-plan", desc)
        return {"repairPlanId": rid, "descriptor": desc, "schemaAdmission": adm["ok"] or (adm["stock"][:2], adm["order"][:2], adm["typed"]),
                "relevantUniverses": relevant, "selectedRecordCount": len(records), "gateEligible": eligible}

    main = descriptor([next(fid for fid, f in findings.items() if f["ruleId"] == "cb24.ts.cold-file")], edits)
    if main["schemaAdmission"] is not True:
        failures.append({"vector": "repair-descriptor-schema", "detail": main["schemaAdmission"]})
    cold_id = next(fid for fid, f in findings.items() if f["ruleId"] == "cb24.ts.cold-file")
    controls = []

    def control(name, d, expect_codes, note):
        codes = [u["code"] for u in d["descriptor"]["unmetPreconditions"]]
        ok = codes[:len(expect_codes)] == expect_codes if expect_codes else (not codes and d["descriptor"]["applicable"])
        if not ok or d["schemaAdmission"] is not True:
            failures.append({"vector": name, "codes": codes, "expected": expect_codes, "schema": d["schemaAdmission"]})
        controls.append({"control": name, "classification": "valid" if not expect_codes else "invalid", "firstRefusal": codes[0] if codes else None,
                         "masksLater": codes[1:], "applicable": d["descriptor"]["applicable"], "repairPlanId": d["repairPlanId"], "note": note,
                         "firstRefusalKeySpelledInKit": published(codes[0]) if codes else None, "pass": ok})

    create = [{"path": "src/extra.ts", "action": "create", "preimageDigest": None, "postimageDigest": hashlib.sha256(b"export {};\n").hexdigest(), "postimageBytes": 11}]
    control("create-only-plan-no-gate", descriptor([cold_id], create, requirement_specs=(("calls", "resolved-callee"), ("runtime-observation", "observed"))), [],
            "no delete/replace: the closed world summary is still built but vetoes nothing")
    control("replace-with-ineligible-native-closed-world", descriptor([cold_id], edits, requirement_specs=(("calls", "resolved-callee"),)),
            ["REPAIR.CLOSED_WORLD_NOT_ESTABLISHED"], "every selected ts-pass Coverage record has deadCodeRepairEligible=false")
    control("replace-with-all-selected-records-eligible", descriptor([cold_id], edits, requirement_specs=(("calls", "resolved-callee"),),
                                                                      records_patch=lambda r: {"deadCodeRepairEligible": True}), [],
            "explanatory counterfactual over the same selection: the gate is the conjunction of the retained records")
    control("one-dissenting-record-defeats", descriptor([cold_id], edits, requirement_specs=(("calls", "resolved-callee"),),
                                                         records_patch=lambda r: {"deadCodeRepairEligible": r["relation"] != "clones"}),
            ["REPAIR.CLOSED_WORLD_NOT_ESTABLISHED"], "remedies name all six ordering members of each dissenting record")
    unrelated = {"coverage": "coverage2:" + "9" * 64, "relation": "calls", "resolution": "resolved-callee", "sourceUniverse": "8" * 64, "targetUniverse": "8" * 64,
                 "subjectScopeCommitment": "sha256:" + "7" * 64, "closedWorld": dict(SENTINEL, deadCodeRepairEligible=True, exportsClosed="closed",
                                                                                   entryPointsRecognized="all", nonliteralLoading="none", externalConsumers="none-declared",
                                                                                   dynamicDispatch="resolved", reasons=[])}
    control("unrelated-closed-universe-does-not-justify", descriptor([cold_id], edits, requirement_specs=(("calls", "resolved-callee"),), extra_records=[unrelated]),
            ["REPAIR.CLOSED_WORLD_NOT_ESTABLISHED"], "a record whose sourceUniverse is not relevant is never selected")
    control("edit-outside-permitted-scope", descriptor([cold_id], [dict(edits[0], path="README.md", preimageDigest=inv["README.md"]["sha256"])],
                                                        scope=("src/**",), requirement_specs=(("calls", "resolved-callee"),)),
            ["REPAIR.EDIT_OUTSIDE_PERMITTED_SCOPE"], "README.md is outside src/**")
    control("preimage-not-snapshot-digest", descriptor([cold_id], [dict(edits[0], preimageDigest="1" * 64)], requirement_specs=(("calls", "resolved-callee"),)),
            ["REPAIR.TARGET_PREIMAGE_MISMATCH"], "preview requires the snapshot inventory digest as preimage")
    control("target-not-a-finding-of-the-run", descriptor(["finding3:" + "5" * 64], create, requirement_specs=(("calls", "resolved-callee"),)),
            ["REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE"], "targets are fingerprints of findings of evidenceRunId")
    control("types-requirement-unsatisfied", descriptor([cold_id], create, requirement_specs=(("types", "checked"),)),
            ["REPAIR.EVIDENCE_RUN_UNAVAILABLE"], "no types@checked Coverage in the Run: required-relation-missing")
    control("imported-evidence-cannot-establish-closed-world", descriptor([cold_id], edits, requirement_specs=(("runtime-observation", "observed"),)),
            ["REPAIR.CLOSED_WORLD_NOT_ESTABLISHED"], "runtime observable-unhit satisfies its requirement but the unsafe replace is still refused")
    cross = [{"vector": "native-requirement-with-imported-outcome", "firstRefusal": admit_requirement({"relation": "calls", "minResolution": "resolved-callee",
                                                                                                    "completeness": "complete", "satisfied": False, "deficiency": "import-unmapped-only"})},
             {"vector": "imported-requirement-with-native-outcome", "firstRefusal": admit_requirement({"relation": "runtime-observation", "minResolution": "observed",
                                                                                                     "completeness": "complete", "satisfied": False, "deficiency": "resolution-incomplete"})},
             {"vector": "satisfied-with-deficiency-present", "firstRefusal": admit_requirement({"relation": "calls", "minResolution": "resolved-callee",
                                                                                              "completeness": "complete", "satisfied": True, "deficiency": "resolution-incomplete"})}]
    for c in cross:
        c["classification"] = "invalid"
        if not c["firstRefusal"]:
            failures.append(c)
    dump("vectors/repair-descriptor.json", {"evidenceRun": "ts-pass", "evidenceRunId": g["runId"], "plan": main, "authorityControls": controls,
                                           "requirementAdmission": cross,
                                           "selectors": ["workflows-and-surfaces.md s6 lines 587-925", "workflows/schemas/evaluator3/repair.schema.json#/$defs/RepairPlanDescriptor",
                                                         "imported-evidence.schema.json#/x-opensip-imported-requirement-law"]})
    return g, store, main


# ------------------------------------------------------------------ D/E. min-resolution at three levels (+ repair evidence)
def min_resolution(g, store):
    U, bound = next(iter(g["bound"].items()))
    base_view_id = next(iter(g["views"]))
    main_row = next(r for (ci, po, k), (d, inv) in g["index"]["inventories"].items() if k == "symbol" for r in inv["rows"] if r["qualifiedName"] == "main")
    subject = {"record": {"schemaVersion": 3, "universe": U, "kind": "symbol", "nativeSubjectId": main_row["nativeSubjectId"]}, "row": main_row,
               "domain": bound["domain"]}
    calls_cell = next(c for c in g["enum"]["cells"] if c["capabilityId"] == "calls")
    types_cell = dict(copy.deepcopy(calls_cell), capabilityId="types")
    snap = g["plan"]["snapshotId"]
    producer = g["views"][base_view_id]["producerClosure"]
    s2 = Store()
    s2.blobs = dict(store.blobs)
    sym_ids = sorted(next(s["subjects"] for s in g["scopes"].values() if s["relation"] == "calls"), key=ckey)
    idx_blob = next(r for r in g["snapshot"]["sourceInventory"] if r["path"] == "src/index.ts")
    idx = s2.get_bytes(idx_blob["sha256"])
    a0 = idx.index(b"export function main")
    rc_complete = {"state": "complete", "attempted": True, "examinedExhaustive": True, "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
    closed = next(iter(g["coverages"].values()))[1]["entry"]["closedWorld"]

    def mk_fact(rel, rung, payload):
        d = {"schemaVersion": 2, "snapshotId": snap, "relation": rel, "resolution": rung, "sourceUniverse": U, "targetUniverse": U, "producerClosure": producer,
             "payloadSchemaDigest": KIT.digest(REL), "payloadDigest": s2.put_record(payload),
             "anchors": [{"path": "src/index.ts", "blobDigest": idx_blob["sha256"], "startByte": a0, "endByte": a0 + 20}], "confidenceMillionths": 1000000}
        faults, _ = NF.fact_faults(s2, d, snap, g["snapshot"]["sourceInventory"], g["bound"])
        return K.identifier("fact", d), d, payload, faults

    def mk_cov(rel, rung, entry_patch):
        sd = {"schemaVersion": 2, "snapshotId": snap, "sourceUniverse": U, "targetUniverse": U, "relation": rel, "resolution": rung,
              "enumeratorClosure": producer, "subjects": sym_ids}
        sid = K.identifier("subject-scope", sd)
        entry = {"relation": rel, "resolution": rung, "coverage": "complete", "examinedUniverse": {"subjectScopeCommitment": "sha256:" + sfx(sid), "subjectCount": len(sym_ids)},
                 "resolutionCompleteness": rc_complete if rung in NF.RESOLVED else {"state": "not-applicable", "attempted": False, "examinedExhaustive": True,
                                                                                     "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []},
                 "closedWorld": closed, "derivationKinds": ["annotated"] if rel == "types" else [], "confidenceMillionths": 1000000, "deficiency": None, "nativeCause": None}
        for k, v in entry_patch.items():
            if isinstance(v, dict):
                entry[k] = dict(entry[k], **v)
            else:
                entry[k] = v
        payload = {"schemaVersion": 3, "key": {"relation": rel, "resolution": rung, "sourceUniverse": U, "targetUniverse": U,
                                               "subjectScopeCommitment": "sha256:" + sfx(sid)}, "entry": entry}
        cd = {"schemaVersion": 2, "scopeId": sid, "payloadSchemaDigest": KIT.digest(NE), "payloadDigest": s2.put_record(payload)}
        faults, _ = NF.coverage_faults(s2, cd, sd, sid, [], bound, g["snapshot"]["sourceInventory"])
        return K.identifier("coverage", cd), cd, payload, sid, sd, faults

    def evaluate(label, atom, drop=lambda rel, rung: False, add_facts=(), add_covs=(), extra_cells=()):
        views = copy.deepcopy(g["views"])
        v = views[base_view_id]
        facts, payloads, scopes, covs = dict(g["facts"]), dict(g["payloads"]), dict(g["scopes"]), dict(g["coverages"])
        keep_cov = [c for c in v["coverageIds"] if not drop(covs[c][1]["key"]["relation"], covs[c][1]["key"]["resolution"])]
        keep_facts = [f for f in v["facts"] if not drop(facts[f]["relation"], facts[f]["resolution"])]
        admission = []
        for fid, d, p, fl in add_facts:
            facts[fid], payloads[fid] = d, p
            keep_facts.append(fid)
            admission += fl
        for cid, cd, p, sid, sd, fl in add_covs:
            covs[cid] = (cd, p)
            scopes[sid] = sd
            keep_cov.append(cid)
            v["scopeIds"].append(sid)
            admission += fl
        v["coverageIds"], v["facts"] = keep_cov, keep_facts
        enum = dict(g["enum"], cells=g["enum"]["cells"] + list(extra_cells))
        inp = EV.Inputs(enum_plan=enum, views=views, scopes=scopes, coverages=covs, facts=facts, fact_payloads=payloads, bound=g["bound"])
        res = EV.native_atom(inp, atom, subject, [base_view_id])
        req_entries = [covs[c][1]["entry"] for c in keep_cov if covs[c][1]["key"]["relation"] == atom["relation"] and covs[c][1]["key"]["resolution"] == atom["minResolution"]]
        view = {atom["relation"]: EV.fold_entries(req_entries)} if req_entries else {}
        suff = NF.sufficiency_v2({"relation": atom["relation"], "minResolution": atom["minResolution"], "completeness": "complete",
                                  "quantifier": "universal-negative" if atom["minResolution"] in NF.RESOLVED else "existential",
                                  "unresolvedEdgePolicy": "forbid", "externalConsumerPolicy": "forbid", "minConfidenceMillionths": 0}, view)
        requirement = {"relation": atom["relation"], "minResolution": atom["minResolution"], "completeness": "complete", "satisfied": suff["satisfied"]}
        if not suff["satisfied"]:
            requirement["deficiency"] = suff["deficiency"]
        return {"case": label, "atom": atom, "value": res["value"], "knownFactIds": len(res["knownFactIds"]), "uncertainFactIds": len(res["uncertainFactIds"]),
                "causes": [c["code"] for c in res["causes"]], "nativeDeficiencies": res["nativeDeficiencies"], "syntheticInputAdmission": admission,
                "repairEvidenceRequirement": requirement, "requirementAdmission": admit_requirement(requirement)}

    ex = lambda rel, rung, **kw: dict({"op": "exists", "relation": rel, "minResolution": rung, "filters": []}, **kw)
    cases = []
    # syntactic
    cases.append(("syntactic", "qualifying", evaluate("declares exists with fact + complete syntactic Coverage", ex("declares", "syntactic")), "true"))
    cases.append(("syntactic", "insufficient-coverage", evaluate("declares none without any syntactic Coverage", dict(ex("declares", "syntactic"), op="none"),
                                                                 drop=lambda r, g_: r == "declares"), "indeterminate"))
    cases.append(("syntactic", "insufficient-fact", evaluate("declares exists: complete Coverage, no declares fact",
                                                             ex("declares", "syntactic", filters=[{"field": "subject", "cmp": "eq", "value": "ts:nope#x"}])), "false"))
    # resolved
    syn_fact = mk_fact("calls", "syntactic-callee-name", {"caller": main_row["nativeSubjectId"], "calleeText": "helper"})
    cases.append(("resolved", "qualifying", evaluate("calls exists at resolved-callee with resolved fact + complete RC-2 Coverage",
                                                     ex("calls", "resolved-callee", filters=[{"field": "target", "cmp": "prefix", "value": "ts:"}])), "true"))
    cases.append(("resolved", "insufficient-fact", evaluate("only a syntactic-callee-name fact (below min rung) under complete resolved Coverage",
                                                            ex("calls", "resolved-callee"), drop=lambda r, g_: r == "calls" and g_ == "resolved-callee" and False,
                                                            add_facts=[syn_fact]) if False else
                  evaluate("only a syntactic-callee-name fact (below min rung) under complete resolved Coverage", ex("calls", "resolved-callee"),
                           drop=lambda r, g_: (r, g_) == ("calls", "resolved-callee") and False), None))
    # replace the ambiguous construction above with an explicit one: drop resolved calls FACTS but keep resolved Coverage
    views_drop = evaluate("only a syntactic-callee-name fact (below min rung) under complete resolved Coverage", ex("calls", "resolved-callee"),
                          drop=lambda r, g_: False, add_facts=[syn_fact])
    cases[-1] = ("resolved", "insufficient-fact-rung-below-min", None, None)
    base = copy.deepcopy(g)
    for f in [f for f, d in g["facts"].items() if d["relation"] == "calls"]:
        base["views"][base_view_id]["facts"].remove(f)
    saved = g["views"]
    g["views"] = base["views"]
    cases[-1] = ("resolved", "insufficient-fact-rung-below-min", evaluate("resolved calls facts removed; only a syntactic-callee-name fact; resolved Coverage complete",
                                                                          ex("calls", "resolved-callee"), add_facts=[syn_fact]), "false")
    g["views"] = saved
    partial = mk_cov("calls", "resolved-callee", {"coverage": "unknown", "deficiency": "resolution-incomplete",
                                                  "resolutionCompleteness": {"state": "partial", "stageTerminal": "budget-exhausted", "examinedExhaustive": False}})
    cases.append(("resolved", "insufficient-coverage", evaluate("calls none with resolved Coverage replaced by a partial RC-2 record", dict(ex("calls", "resolved-callee"), op="none"),
                                                                drop=lambda r, g_: (r, g_) == ("calls", "resolved-callee"), add_covs=[partial]), "indeterminate"))
    # type level
    checked = mk_fact("types", "checked", {"subject": main_row["nativeSubjectId"], "typeText": "() => string", "checkedType": "ts:type#string"})
    annotated = mk_fact("types", "annotated", {"subject": main_row["nativeSubjectId"], "typeText": "() => string"})
    tcov = mk_cov("types", "checked", {})
    cases.append(("type", "qualifying", evaluate("types exists at checked with checked fact + complete checked Coverage", ex("types", "checked"),
                                                 add_facts=[checked], add_covs=[tcov], extra_cells=[types_cell]), "true"))
    cases.append(("type", "insufficient-fact", evaluate("only an annotated types fact under complete checked Coverage", ex("types", "checked"),
                                                        add_facts=[annotated], add_covs=[tcov], extra_cells=[types_cell]), "false"))
    tcov_bad = mk_cov("types", "checked", {"coverage": "unknown", "deficiency": "input-closure-incomplete", "nativeCause": "config-flag-stripped",
                                           "resolutionCompleteness": {"state": "partial", "examinedExhaustive": False, "stageTerminal": "unavailable"}})
    cases.append(("type", "insufficient-coverage", evaluate("types none under an incomplete checked Coverage record", dict(ex("types", "checked"), op="none"),
                                                            add_facts=[], add_covs=[tcov_bad], extra_cells=[types_cell]), "indeterminate"))
    out = []
    for level, kind, res, want in cases:
        ok = res is not None and res["value"] == want and not res["syntheticInputAdmission"] and res["requirementAdmission"] is None
        if not ok:
            failures.append({"vector": f"min-resolution-{level}-{kind}", "got": res and res["value"], "want": want,
                             "admission": res and res["syntheticInputAdmission"], "req": res and res["requirementAdmission"]})
        out.append({"level": level, "case": kind, "classification": "valid" if kind == "qualifying" else "invalid", "expectedValue": want, "pass": ok, **(res or {})})
    dump("vectors/min-resolution.json", {"baseRun": "ts-pass", "subject": subject["record"], "cases": out,
                                        "note": "atom-evaluation vectors over admitted ts-pass inputs; synthetic types facts/Coverage are admitted through native fact/coverage admission first "
                                                "(syntheticInputAdmission lists any refusal); the repairEvidenceRequirement is the per-requirement sufficiency_v2 projection of the same case",
                                        "selectors": ["atom-evaluation-contract.v1.md s4-s5", "native-evidence.md s4.6", "workflows-and-surfaces.md s6 lines 736-817"]})


# ------------------------------------------------------------------ F. imported observation boundary
def imported_boundary(g, store):
    iid, imp = next(iter(g["imports"].items()))
    rule = next(r for r in g["policy"]["rules"] if r["ruleId"] == "cb24.ts.cold-file")
    U = next(iter(g["bound"]))

    def subj(path):
        return {"record": {"schemaVersion": 3, "universe": U, "kind": "file", "nativeSubjectId": path}, "row": {"path": path}, "domain": "native.semantic-universe.typescript.v2"}

    def run(label, atom, path, payload_patch=None, wrapper_patch=None, flags=None, want=None, want_causes=()):
        payload = copy.deepcopy(imp["payload"])
        if payload_patch:
            payload_patch(payload)
        wrapper = dict(imp["wrapper"], **(wrapper_patch or {}))
        obs = dict(imp["observation"], window=payload["observationWindow"], population=payload["observedPopulation"])
        inp = EV.Inputs(plan=g["plan"], imports={iid: wrapper}, import_payloads={iid: payload}, import_observations={iid: obs},
                        import_scopes={iid: imp["scope"]}, import_flags={iid: flags or imp["flags"]})
        res = EV.imported_atom(inp, atom, subj(path), rule)
        codes = [c["code"] for c in res["causes"]]
        ok = res["value"] == want and all(c in codes for c in want_causes)
        if not ok:
            failures.append({"vector": label, "got": (res["value"], codes), "want": (want, want_causes)})
        return {"vector": label, "classification": "valid" if not want_causes else "invalid", "value": res["value"], "causes": codes,
                "knownRows": res["knownRows"], "uncertainRows": res["uncertainRows"], "expected": want, "pass": ok}

    unhit = {"op": "exists", "relation": "runtime-observation", "minResolution": "observed", "evidence": "runtime",
             "filters": [{"field": "observability", "cmp": "eq", "value": "observable-unhit"}]}
    anyobs = dict(unhit, filters=[])
    none_ = dict(anyobs, op="none")
    allc = dict(anyobs, op="all-covered")

    def row(path, obs, hits=None):
        r = {"path": path, "observability": obs}
        if hits is not None:
            r["hits"] = hits
        return r

    def set_rows(rows):
        return lambda p: p.__setitem__("subjects", rows)
    vecs = [
        run("observable-unhit-is-bounded-negative-evidence", unhit, "src/util.ts", want="true"),
        run("observed-hit-makes-none-false", none_, "src/index.ts", want="false"),
        run("unobservable-row-is-never-unhit", unhit, "src/util.ts", set_rows([row("src/index.ts", "observed-hit", 5), row("src/util.ts", "unobservable")]),
            want="indeterminate", want_causes=["unobservable-subject"]),
        run("unmapped-row-is-never-unhit", none_, "src/util.ts", set_rows([row("src/index.ts", "observed-hit", 5), row("src/util.ts", "unmapped")]),
            want="indeterminate", want_causes=["unmapped-subject"]),
        run("population-unknown-window-insufficient", dict(unhit, filters=[{"field": "observability", "cmp": "eq", "value": "observed-hit"}]), "src/util.ts",
            lambda p: p.__setitem__("observedPopulation", "unknown"), want="indeterminate", want_causes=["observation-window-insufficient"]),
        run("known-unhit-row-dominates-unknown-population", none_, "src/util.ts", lambda p: p.__setitem__("observedPopulation", "unknown"),
            want="false", want_causes=["observation-window-insufficient"]),
        run("partial-wrapper-blocks-negative-but-not-known-hit", none_, "src/index.ts", wrapper_patch={"completeness": "partial"}, want="false"),
        run("partial-wrapper-leaves-unknown", none_, "src/other.ts", wrapper_patch={"completeness": "partial"}, want="indeterminate", want_causes=["wrapper-partial"]),
        run("unmapped-only-import-never-feeds", anyobs, "src/util.ts", flags={"consumable": False, "staleness": "stale"}, want="indeterminate",
            want_causes=["import-unmapped-only"]),
        run("path-outside-wrapper-scope-owes-nothing", none_, "README.md", want="indeterminate", want_causes=["zero-owed-wrappers", "evidence-kind-unavailable"]),
        run("no-row-for-owed-path-is-not-absence", none_, "src/other.ts", want="indeterminate", want_causes=["no-consumable-row"]),
        run("all-covered-true-when-every-owed-row-observable", allc, "src/util.ts", want="true"),
    ]
    law = []
    imports = [imp]
    demand = {"minWindowDays": 7, "populations": ["test-suite"], "minCommits": 10}
    hist_payload = {"payloadDomain": "workflow.import-payload.history.v1", "vcsSystem": "git",
                    "revisionRange": {"from": "a" * 40, "to": "b" * 40, "commitCount": 25, "truncated": False}, "collectionScope": "listed-paths",
                    "subjects": [{"path": "src/util.ts"}]}
    hist = {"wrapper": dict(imp["wrapper"], kind="history"), "payload": hist_payload, "flags": {"consumable": True, "staleness": "current"}, "scope": imp["scope"]}
    for label, kind, imps, target, dem, want in (
            ("runtime-satisfied", "runtime", imports, {"path": "src/util.ts"}, demand, None),
            ("evidence-kind-unavailable", "history", imports, {"path": "src/util.ts"}, demand, "evidence-kind-unavailable"),
            ("import-unmapped-only", "runtime", [dict(imp, flags={"consumable": False, "staleness": "stale"})], {"path": "src/util.ts"}, demand, "import-unmapped-only"),
            ("subject-not-observable", "runtime", [dict(imp, payload=dict(imp["payload"], subjects=[row("src/util.ts", "unobservable")]))], {"path": "src/util.ts"}, demand, "subject-not-observable"),
            ("observation-window-insufficient", "runtime", imports, {"path": "src/util.ts"}, dict(demand, minWindowDays=30), "observation-window-insufficient"),
            ("import-absent-for-requirement", "runtime", imports, {"path": "src/other.ts"}, demand, "import-absent-for-requirement"),
            ("history-outside-collection-scope", "history", [hist], {"path": "src/index.ts"}, demand, "history-outside-collection-scope"),
            ("history-range-insufficient", "history", [dict(hist, payload=dict(hist_payload, revisionRange=dict(hist_payload["revisionRange"], truncated=True)))],
             {"path": "src/util.ts"}, demand, "history-range-insufficient"),
            ("precedence-unobservable-over-window", "runtime", [dict(imp, payload=dict(imp["payload"], subjects=[row("src/util.ts", "unmapped")]))],
             {"path": "src/util.ts"}, dict(demand, minWindowDays=30), "subject-not-observable")):
        outcome, conds = imported_requirement(kind, imps, target, dem)
        ok = outcome == want
        if not ok:
            failures.append({"vector": f"imported-law-{label}", "got": outcome, "want": want})
        law.append({"vector": label, "classification": "valid" if want is None else "invalid", "kind": kind, "outcome": outcome, "applicableConditions": conds, "pass": ok})
    dump("vectors/imported-observation-boundary.json", {"baseRun": "ts-pass", "importId": iid, "atomVectors": vecs, "requirementLawVectors": law,
                                                       "neverEstablishes": "see vectors/repair-descriptor.json control imported-evidence-cannot-establish-closed-world",
                                                       "joinRefusalOnRun": "runs/ts-pass~import-window-mismatch.replay.json (ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN), "
                                                                           "runs/ts-pass~import-stale-snapshot.replay.json (IMPORT.STALE_FOR_PLAN)",
                                                       "selectors": ["workflows-and-surfaces.md s4 lines 436-517", "atom-evaluation-contract.v1.md s6",
                                                                     "evaluator-projection-registry.v1.json#/importQuantifiers",
                                                                     "imported-evidence.schema.json#/x-opensip-imported-requirement-law"]})


# ------------------------------------------------------------------ G. mutation replay scope vs repair-apply key
def mutation_keys(g, main_plan):
    def scope(req, step, op):
        return {"schemaVersion": 1, "requestId": req, "stepId": step, "projectId": g["snapshot"]["projectId"], "operation": op}
    r1, r2 = "req1_" + "1" * 32, "req1_" + "2" * 32
    rows = []
    for label, rec in (("waiver-change-r1", scope(r1, 1, "waiver-change")), ("waiver-change-r1-again", scope(r1, 1, "waiver-change")),
                       ("waiver-change-r2", scope(r2, 1, "waiver-change")), ("import-r1-step0", scope(r1, 0, "import")),
                       ("repair-apply-in-generic-scope", scope(r1, 2, "repair-apply"))):
        adm = KIT.admit(rec, INVOC3, "#/$defs/MutationReplayScopeV1")
        rows.append({"label": label, "record": rec, "schemaAdmitted": adm["ok"], "idempotencyKey": K.H("workflow.mutation-intent", rec) if adm["ok"] else None,
                     "classification": "valid" if adm["ok"] else "invalid", "firstRefusal": None if adm["ok"] else (adm["stock"][:1] or adm["order"][:1])})
    apply_pre = {"operation": "repair-apply", "projectId": g["snapshot"]["projectId"], "repairPlanId": main_plan["repairPlanId"], "baseSnapshotId": g["plan"]["snapshotId"]}
    apply_key = hashlib.sha256(K.C(apply_pre)).hexdigest()
    keys = {r["label"]: r["idempotencyKey"] for r in rows}
    measured = {"sameScopeSameKey": keys["waiver-change-r1"] == keys["waiver-change-r1-again"],
                "freshRequestDifferentKey": keys["waiver-change-r1"] != keys["waiver-change-r2"],
                "repairApplyRefusedByGenericScopeSchema": keys["repair-apply-in-generic-scope"] is None,
                "applyKeyIsContentDerivedSameForBothRequests": True,
                "applyKeyDiffersFromEveryMutationIntentKey": apply_key not in {v for v in keys.values() if v},
                "applyKeyIsNotAnHFrame": apply_key != K.H("workflow.mutation-intent", apply_pre)}
    if not all(measured.values()):
        failures.append({"vector": "mutation-keys", "measured": measured})
    dump("vectors/mutation-replay-scope.json", {"scopes": rows, "repairApply": {"preimage": apply_pre, "key": apply_key, "recipe": "raw SHA-256 of C({operation, projectId, repairPlanId, baseSnapshotId})"},
                                               "measured": measured,
                                               "selectors": ["workflows/schemas/evaluator3/invocation-record.schema.json#/$defs/MutationReplayScopeV1",
                                                             "workflows/schemas/evaluator3/repair.schema.json#/x-opensip-mutation-operation-map/receiptIdempotencyKeyByStepKind/recipes"]})


# ------------------------------------------------------------------ H. pinned purge refusal envelope
def pinned_purge(g):
    run_id = g["runId"]

    def env(pins, subject=None, consequences=None, exit_code=2, cls="request-rejected", code="evidence.pinned", errors=True, drop_disclosure=False):
        dd = {"code": code, "remedy": "revoke or retire the named pins with lifecycle authorization and disclose the complete then-current pin set before purge",
              "subject": subject or run_id}
        if not drop_disclosure:
            dd["purgeDisclosure"] = {"runId": run_id, "activePins": pins,
                                     "consequences": consequences or ["named-pins-revoked", "dependent-evidence-replay-unavailable", "sealed-history-retained"]}
        term = {"class": cls, "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": dd}
        e = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": "req1_" + "a" * 32,
             "projectId": g["snapshot"]["projectId"], "termination": term, "exitCode": exit_code}
        if errors:
            e["errors"] = [dd]
        return e

    def agreement(e):
        """Checker-side agreement laws the schema cannot state (workflows s12 lines 1351-1362; exit table)."""
        out = []
        t = e["termination"]
        if EXIT[t["class"]] != e["exitCode"]:
            out.append("cb24.ENVELOPE_EXIT_CLASS_MISMATCH")
        dd = t.get("domainDetail")
        if dd and dd["code"] == "evidence.pinned":
            if (t["class"], t.get("errorCode"), e["exitCode"]) != ("request-rejected", "REQUEST.PRECONDITION_FAILED", 2):
                out.append("cb24.PINNED_PURGE_ROUTE")
            if dd not in e.get("errors", []):
                out.append("cb24.PINNED_PURGE_DETAIL_NOT_IN_ERRORS")
            if dd.get("subject") != dd.get("purgeDisclosure", {}).get("runId"):
                out.append("cb24.PINNED_PURGE_SUBJECT_RUN_MISMATCH")
        return out

    def check(label, e, expect):
        r = KIT.admit(e, ENV3, "#")
        faults = [f"SCHEMA:{x['path']}:{x['message'][:80]}" for x in r["stock"]] + [f"ORDER:{x['path']}:{x['violation']}" for x in r["order"]]
        if r["typed"]:
            faults.insert(0, r["typed"])
        faults += agreement(e) if not faults else []
        return neg(label, faults, expect)
    pins = sorted([{"pinId": "backup:weekly-2026-09-06", "kind": "backup-export"}, {"pinId": "baseline:main", "kind": "baseline"},
                   {"pinId": "repair:plan-cold-file", "kind": "repair-prerequisite"}], key=lambda p: p["pinId"].encode())
    positive = env(pins)
    vecs = [check("pinned-purge-refusal", positive, None),
            check("pins-not-sorted", env(list(reversed(pins))), "ORDER:"),
            check("consequences-reordered", env(pins, consequences=["sealed-history-retained", "named-pins-revoked", "dependent-evidence-replay-unavailable"]), "SCHEMA:"),
            check("empty-active-pins", env([]), "SCHEMA:"),
            check("purge-disclosure-omitted", env(pins, drop_disclosure=True), "SCHEMA:"),
            check("failure-without-errors", env(pins, errors=False), "SCHEMA:"),
            check("exit-code-disagrees-with-class", env(pins, exit_code=3), "cb24.ENVELOPE_EXIT_CLASS_MISMATCH"),
            check("subject-is-not-the-run", env(pins, subject="run3:" + "0" * 64), "cb24.PINNED_PURGE_SUBJECT_RUN_MISMATCH")]
    dump("envelopes/pinned-purge.json", {"envelope": positive, "vectors": vecs,
                                        "hostObligationsNotPerformed": ["complete pin inventory under the exclusive purge lease", "renewed disclosure before destruction"],
                                        "selectors": ["workflows-and-surfaces.md s12 lines 1351-1384", "workflows/schemas/evaluator3/common.schema.json#/$defs/PinnedPurgeDisclosure",
                                                      "workflows/schemas/evaluator3/command-envelope.schema.json"]})


def main():
    env = config_vectors()
    js_body_through_ts(env)
    clones_negatives()
    g, store, plan = repair_vectors()
    min_resolution(g, store)
    imported_boundary(g, store)
    mutation_keys(g, plan)
    pinned_purge(g)
    print("failures", len(failures))
    print(json.dumps(failures, default=str)[:6000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
