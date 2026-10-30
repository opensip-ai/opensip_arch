"""NSS-F1 evidence: worked vectors and reference checks for the native-context inputs carrier.

Usage: python3 -I -B build_nss_f1.py --product <opensip checkout> --arch <opensip_arch checkout> [--check]

Reads (never writes) the product fixture crates/host/tests/fixtures/native-context-fixtures.current.json,
the product's vendored jsonschema (tools/contracts/python-packages) and the architecture's registered
native-evidence.schemas.v2.json. Writes vectors.json and report.json beside this script, or with --check
compares instead of writing. Nothing here runs a provider, a compiler, cargo or a frame codec.
"""
import argparse
import hashlib
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(HERE, "..", "design", "native", "native-context-inputs.schemas.v1.json")
PREFIX = b"opensip.product.v1\x00"
CTX_DOMAIN = "native.context.typescript.v2"
UNI_DOMAIN = "native.semantic-universe.typescript.v2"
MAX_C = 4 * 1024 * 1024
STARTUP = "docs/implementation/m3/native-successors-fa/rust-commit-alignment-r2/design/native/provider-startup.schemas.v1.json"


# --- C: the foundation canonical JSON (identity-and-evidence section 3), sufficient for these records ---
def c_string(s):
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch in "\b\t\n\f\r":
            out.append({"\b": "\\b", "\t": "\\t", "\n": "\\n", "\f": "\\f", "\r": "\\r"}[ch])
        elif o < 0x20:
            out.append("\\u%04x" % o)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def c_encode(v):
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return c_string(v)
    if isinstance(v, list):
        return "[" + ",".join(c_encode(x) for x in v) + "]"
    if isinstance(v, dict):
        keys = sorted(v, key=lambda k: k.encode("utf-8"))
        return "{" + ",".join(c_string(k) + ":" + c_encode(v[k]) for k in keys) + "}"
    raise TypeError(type(v))


def C(v):
    b = c_encode(v).encode("utf-8")
    if len(b) > MAX_C:
        raise ValueError("C over 4 MiB")
    return b


def no_dupes(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError("duplicate key " + k)
        d[k] = v
    return d


def parse_canonical(b):
    """Parse carried bytes and require that they are exactly C of what they decode to."""
    v = json.loads(b.decode("utf-8"), object_pairs_hook=no_dupes,
                   parse_float=lambda s: (_ for _ in ()).throw(ValueError("float")))
    if C(v) != b:
        raise ValueError("not canonical")
    return v


def H(domain, c_bytes):
    frame = PREFIX + domain.encode() + b"\x00" + struct.pack(">Q", len(c_bytes)) + c_bytes
    return hashlib.sha256(frame).hexdigest()


def sha(b):
    return hashlib.sha256(b).hexdigest()


# --- deterministic CBOR length (sizes only; key order does not change length) ---
def head_len(n):
    return 1 if n < 24 else 2 if n < 256 else 3 if n < 65536 else 5 if n < 2 ** 32 else 9


def cbor_len(v):
    if v is None or v is True or v is False:
        return 1
    if isinstance(v, int):
        return head_len(v)
    if isinstance(v, bytes):
        return head_len(len(v)) + len(v)
    if isinstance(v, str):
        n = len(v.encode("utf-8"))
        return head_len(n) + n
    if isinstance(v, list):
        return head_len(len(v)) + sum(cbor_len(x) for x in v)
    if isinstance(v, dict):
        return head_len(len(v)) + sum(cbor_len(k) + cbor_len(x) for k, x in v.items())
    raise TypeError(type(v))


# --- the reference carrier admission (law digestJoins), for the vectors ---
def admit_carrier(resolved, carrier_wire):
    ctx_b, g_b, l_b, root = (carrier_wire[k] for k in ("context", "configGraph", "nodeModulesLayout", "unitRoot"))
    try:
        ctx = parse_canonical(ctx_b)
        parse_canonical(g_b)
        if l_b is not None:
            parse_canonical(l_b)
    except ValueError as e:
        return "refuse:canonical:" + str(e).split(" ")[0]
    if "sha256:" + H(CTX_DOMAIN, ctx_b) != resolved["nativeContextId"]:
        return "refuse:context-digest"
    if sha(g_b) != resolved["tsconfigGraphHash"]:
        return "refuse:config-graph-digest"
    want = ctx["nodeModulesLayoutDigest"]
    if (l_b is None) != (want is None):
        return "refuse:layout-presence"
    if l_b is not None and sha(l_b) != want:
        return "refuse:layout-digest"
    if resolved["nodeModulesInReadSet"] != (l_b is not None):
        return "refuse:node-modules-in-read-set"
    for f in ("languageMode", "packageModuleType"):
        if resolved[f] != ctx[f]:
            return "refuse:overlap:" + f
    if root == "." or root.startswith("/") or root.endswith("/"):
        return "refuse:unit-root-grammar"
    return "admit"


# --- the reference decision order (law recomputation) ---
def decide(graph_refused, context_refused, context_differs, graph_differs):
    if graph_refused:
        return "InputMismatch(config-graph, refused)"
    if context_refused:
        return "InputMismatch(native-context, refused)"
    if context_differs:
        return "PreAnalyzeUnavailableV1(native-context-mismatch)"
    if graph_differs:
        return "InputMismatch(config-graph, differs)"
    return "NativeContextVerifiedV1"


def wire_to_vector(w):
    return {"contextHex": w["context"].hex(), "configGraphHex": w["configGraph"].hex(),
            "nodeModulesLayoutHex": None if w["nodeModulesLayout"] is None else w["nodeModulesLayout"].hex(),
            "unitRoot": w["unitRoot"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--product", required=True)
    ap.add_argument("--arch", required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, os.path.join(a.product, "tools", "contracts", "python-packages"))
    import jsonschema
    from referencing import Registry, Resource

    fx_path = os.path.join(a.product, "crates/host/tests/fixtures/native-context-fixtures.current.json")
    fx_bytes = open(fx_path, "rb").read()
    fx = json.loads(fx_bytes)
    blobs = {b["digest"]: bytes.fromhex(b["hex"]) for b in fx["typescriptUniverse"]["blobs"]}

    def framed(domain):
        tag = PREFIX + domain.encode() + b"\x00"
        (d, b), = [(d, b) for d, b in blobs.items() if b.startswith(tag)]
        assert sha(b) == d
        return b[len(tag) + 8:]

    ctx_b = framed(CTX_DOMAIN)
    resolved = parse_canonical(framed(UNI_DOMAIN))
    ctx = parse_canonical(ctx_b)
    g_b = blobs[resolved["tsconfigGraphHash"]]
    l_b = blobs[ctx["nodeModulesLayoutDigest"]]
    graph = parse_canonical(g_b)
    layout = parse_canonical(l_b)

    checks = {
        "contextIdJoin": "sha256:" + H(CTX_DOMAIN, ctx_b) == resolved["nativeContextId"],
        "configGraphJoin": sha(g_b) == resolved["tsconfigGraphHash"],
        "layoutJoin": sha(l_b) == ctx["nodeModulesLayoutDigest"],
        "nodeModulesInReadSet": resolved["nodeModulesInReadSet"] is True,
        "canonicalReencode": all(C(parse_canonical(x)) == x for x in (ctx_b, g_b, l_b)),
        "fixtureEqualsFixtureContextRecord": ctx == fx["contexts"]["typescript"],
    }
    assert all(checks.values()), checks

    good = {"context": ctx_b, "configGraph": g_b, "nodeModulesLayout": l_b, "unitRoot": ""}
    noncanon = ctx_b.replace(b'{"', b'{ "', 1)
    swapped = dict(json.loads(ctx_b))
    swapped["packageModuleType"] = "module" if ctx["packageModuleType"] != "module" else "commonjs"
    joins = [
        ("positive", good, "admit"),
        ("context-not-canonical-though-hashed", dict(good, context=noncanon), "refuse:canonical:not"),
        ("config-graph-bytes-of-another-graph", dict(good, configGraph=C(dict(graph, entryConfigPath=None, nodes=[]))),
         "refuse:config-graph-digest"),
        ("layout-null-while-context-names-one", dict(good, nodeModulesLayout=None), "refuse:layout-presence"),
        ("layout-bytes-of-another-layout", dict(good, nodeModulesLayout=C({"schemaVersion": 1, "entries": []})),
         "refuse:layout-digest"),
        ("context-of-another-id", dict(good, context=C(swapped)), "refuse:context-digest"),
        ("unit-root-external-sentinel", dict(good, unitRoot="."), "refuse:unit-root-grammar"),
    ]
    join_results = []
    for name, w, want in joins:
        got = admit_carrier(resolved, w)
        assert got == want, (name, got, want)
        join_results.append({"case": name, "expected": want})

    schema = json.load(open(SCHEMA))
    native = json.load(open(os.path.join(a.arch, "docs/coop/design-corrections/native/native-evidence.schemas.v2.json")))
    startup = json.load(open(os.path.join(a.arch, STARTUP)))
    reg = Registry().with_resources([(native["$id"], Resource.from_contents(native)),
                                     (schema["$id"], Resource.from_contents(schema)),
                                     (startup["$id"], Resource.from_contents(startup))])
    universe_v = jsonschema.Draft202012Validator(
        {"$ref": startup["$id"] + "#/$defs/TypeScriptSemanticUniverseV2"}, registry=reg)

    for rec, inst in (("TypeScriptNativeContextV2", ctx), ("TypeScriptConfigGraphV1", graph),
                      ("ResolvedNodeModulesLayoutV1", layout)):
        checks["closedSchemaValid:" + rec] = jsonschema.Draft202012Validator(
            {"$ref": native["$id"] + "#/$defs/" + rec}, registry=reg).is_valid(inst)
    assert all(checks.values()), checks

    def composed(inst):
        """TypeScriptOpenUniverseV3 admission: the record AND its universe under the inherited selector."""
        return validator("TypeScriptOpenUniverseV3").is_valid(inst) and universe_v.is_valid(inst.get("universe"))

    def validator(name):
        return jsonschema.Draft202012Validator({"$ref": schema["$id"] + "#/$defs/" + name}, registry=reg)

    vec_good = wire_to_vector(good)
    universe = {"schemaVersion": 1, "manifestId": "2" * 64, "capabilityManifestId": "3" * 64,
                "runtimeArtifactId": "typescript-runtime", "runtimeArtifactSha256": "4" * 64,
                "providerArtifactId": "typescript-provider", "providerArtifactSha256": "5" * 64,
                "runtimeDescriptorSha256": "6" * 64, "providerDescriptorSha256": "7" * 64, "protocolMajor": 2,
                "providerBuildId": "typescript-provider-fixture", "nodeVersion": "24.16.0", "v8Version": "13.6",
                "modulesAbi": "137", "typescriptVersion": ctx["toolchain"]["compilerVersion"],
                "typescriptCompilerSha256": ctx["toolClosure"]["compiler"],
                "typescriptStdlibMerkleRoot": ctx["toolchain"]["typescriptStdlibMerkleRoot"],
                "platformId": "macos-aarch64", "resolvedInputs": resolved}
    ou = {"executionId": "exec-1", "snapshotId": fx["typescriptUniverse"]["snapshotId"],
          "planId": "plan2:" + "0" * 64, "planIntentCommitment": "sha256:" + "1" * 64,
          "providerId": "typescript-semantic", "universe": universe,
          "universeKey": "sha256:" + H(UNI_DOMAIN, C(resolved)), "nativeContextInputs": vec_good}
    assert ou["universeKey"] == "sha256:" + fx["typescriptUniverse"]["digest"]
    corr = {"executionId": "exec-1", "snapshotId": ou["snapshotId"], "planId": ou["planId"]}
    mm_differs = dict(corr, reason="native-input-mismatch", input="config-graph",
                      recomputation={"outcome": "differs", "planBoundDigest": resolved["tsconfigGraphHash"],
                                     "recomputedDigest": sha(C(dict(graph, nodes=list(reversed(graph["nodes"])))))})
    mm_refused = dict(corr, reason="native-input-mismatch", input="native-context",
                      recomputation={"outcome": "refused", "refusalKey": "native.typescript-profile-option-unsupported"})
    schema_cases = [
        ("NativeContextInputsV1", "carrier-positive", vec_good, True),
        ("NativeContextInputsV1", "carrier-layout-null", dict(vec_good, nodeModulesLayoutHex=None), True),
        ("NativeContextInputsV1", "carrier-project-root-empty", dict(vec_good, unitRoot=""), True),
        ("NativeContextInputsV1", "carrier-unit-root-dir", dict(vec_good, unitRoot="packages/web"), True),
        ("NativeContextInputsV1", "carrier-extra-member", dict(vec_good, closures=[]), False),
        ("NativeContextInputsV1", "carrier-missing-unit-root", {k: v for k, v in vec_good.items() if k != "unitRoot"}, False),
        ("NativeContextInputsV1", "carrier-unit-root-dot", dict(vec_good, unitRoot="."), False),
        ("NativeContextInputsV1", "carrier-unit-root-trailing-slash", dict(vec_good, unitRoot="a/"), False),
        ("NativeContextInputsV1", "carrier-uppercase-hex", dict(vec_good, contextHex=vec_good["contextHex"].upper()), False),
        ("NativeContextInputsV1", "carrier-odd-hex", dict(vec_good, configGraphHex=vec_good["configGraphHex"][:-1]), False),
        ("NativeContextInputsV1", "carrier-empty-layout-bytes", dict(vec_good, nodeModulesLayoutHex=""), False),
        ("TypeScriptOpenUniverseV3", "open-universe-v3-positive", ou, True),
        ("TypeScriptOpenUniverseV3", "open-universe-v3-without-carrier",
         {k: v for k, v in ou.items() if k != "nativeContextInputs"}, False),
        ("TypeScriptPreAnalyzeInputMismatchV1", "mismatch-config-graph-differs", mm_differs, True),
        ("TypeScriptPreAnalyzeInputMismatchV1", "mismatch-native-context-refused", mm_refused, True),
        ("TypeScriptPreAnalyzeInputMismatchV1", "mismatch-config-graph-refused",
         dict(mm_refused, input="config-graph",
              recomputation={"outcome": "refused", "refusalKey": "native.typescript-config-extends-unresolved"}), True),
        ("TypeScriptPreAnalyzeInputMismatchV1", "mismatch-native-context-differs-is-v1s",
         dict(mm_differs, input="native-context"), False),
        ("TypeScriptPreAnalyzeInputMismatchV1", "mismatch-unlisted-refusal-key",
         dict(mm_refused, recomputation={"outcome": "refused", "refusalKey": "native.native-context-lib-not-retained"}), False),
        ("TypeScriptPreAnalyzeInputMismatchV1", "mismatch-context-reason",
         dict(mm_differs, reason="native-context-mismatch"), False),
        ("TypeScriptPreAnalyzeInputMismatchV1", "mismatch-with-coverage", dict(mm_refused, coverage=[]), False),
        ("TypeScriptPreAnalyzeInputMismatchV1", "mismatch-config-graph-with-a-profile-key",
         dict(mm_refused, input="config-graph"), False),
        ("TypeScriptPreAnalyzeInputMismatchV1", "mismatch-native-context-with-an-item-14a-key",
         dict(mm_refused, recomputation={"outcome": "refused",
                                         "refusalKey": "native.typescript-config-extends-unresolved"}), False),
    ]
    schema_results = []
    for defn, name, inst, ok in schema_cases:
        valid = validator(defn).is_valid(inst)
        assert valid == ok, (name, valid)
        schema_results.append({"definition": defn, "case": name, "valid": ok})
    assert mm_differs["recomputation"]["recomputedDigest"] != resolved["tsconfigGraphHash"]
    drop = {k: v for k, v in universe.items() if k != "platformId"}
    composed_cases = [
        ("open-universe-v3-complete-inherited-universe", ou, True),
        ("open-universe-v3-empty-universe", dict(ou, universe={}), False),
        ("open-universe-v3-universe-missing-a-member", dict(ou, universe=drop), False),
        ("open-universe-v3-universe-extra-member", dict(ou, universe=dict(universe, nativeContext="x")), False),
        ("open-universe-v3-universe-protocol-major-1", dict(ou, universe=dict(universe, protocolMajor=1)), False),
    ]
    composed_results = []
    for name, inst, ok in composed_cases:
        got = composed(inst)
        assert got == ok, (name, got)
        composed_results.append({"case": name, "admitted": ok})

    order = []
    for gr in (False, True):
        for cr in (False, True):
            for cd in (False, True):
                for gd in (False, True):
                    if gr and (cr or cd):
                        continue  # no context is derived after a graph refusal
                    if cr and cd:
                        continue  # a refused context has no digest to differ
                    order.append({"graphRefused": gr, "contextRefused": cr, "contextDiffers": cd,
                                  "graphDiffers": gd, "terminal": decide(gr, cr, cd, gd)})

    fixture_carrier = cbor_len(good)
    open_v2 = {k: v for k, v in ou.items() if k != "nativeContextInputs"}
    maximal_carrier = cbor_len({"context": b"x" * MAX_C, "configGraph": b"x" * MAX_C,
                                "nodeModulesLayout": b"x" * MAX_C, "unitRoot": "\U0010ffff" * 4096})
    sizes = {
        "fixtureContextCBytes": len(ctx_b), "fixtureConfigGraphCBytes": len(g_b), "fixtureLayoutCBytes": len(l_b),
        "fixtureCarrierCborBytes": fixture_carrier,
        "fixtureOpenUniverseV2CborBytesIllustrative": cbor_len(open_v2),
        "maximalCarrierCborBytes": maximal_carrier,
        "maxFramePayloadBytes": 67108864,
        "headroomForTheRestOfOpenUniverseBytes": 67108864 - maximal_carrier - cbor_len("nativeContextInputs"),
    }
    vectors = {
        "schemaVersion": 1,
        "standing": "NSS-F1 r1 evidence. Worked carrier vectors from the product's synthetic native-context fixture, standalone schema cases against native-context-inputs.schemas.v1.json, composed OpenUniverseV3 admission cases (the record plus the inherited universe selector; the non-resolvedInputs universe members are illustrative values), the reference carrier joins, the decision order and the size bound. Not a run, not a codec test, not product acceptance.",
        "fixture": {"path": "crates/host/tests/fixtures/native-context-fixtures.current.json",
                    "sha256": sha(fx_bytes), "nativeContextId": resolved["nativeContextId"],
                    "tsconfigGraphHash": resolved["tsconfigGraphHash"],
                    "nodeModulesLayoutDigest": ctx["nodeModulesLayoutDigest"],
                    "universeKey": ou["universeKey"]},
        "fixtureChecks": checks,
        "carrierVector": vec_good,
        "carrierJoins": join_results,
        "schemaCases": schema_results,
        "composedOpenUniverseCases": composed_results,
        "decisionOrder": order,
        "sizes": sizes,
        "schema": {"path": "design/native/native-context-inputs.schemas.v1.json", "sha256": sha(open(SCHEMA, "rb").read())},
    }
    out = json.dumps(vectors, indent=2, sort_keys=True) + "\n"
    path = os.path.join(HERE, "vectors.json")
    if a.check:
        same = open(path).read() == out
        print("vectors.json", "MATCHES" if same else "DIFFERS")
        sys.exit(0 if same else 1)
    open(path, "w").write(out)
    print(json.dumps({"fixtureChecks": checks, "joins": len(join_results), "schemaCases": len(schema_results), "composedCases": len(composed_results),
                      "orderRows": len(order), "sizes": sizes}, indent=1))


if __name__ == "__main__":
    main()
