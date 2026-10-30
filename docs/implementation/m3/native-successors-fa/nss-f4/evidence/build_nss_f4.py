"""NSS-F4 evidence: the manifest-schema successor copy, its verdict audit, a generator run, and worked vectors.

Usage: python3 -I -B build_nss_f4.py --product <opensip checkout> --arch <opensip_arch checkout> [--check]

Reads (never writes) the product and architecture checkouts. Writes, beside this script's parent directory:
  completion/manifest-schema.completed.v1.json   the successor copy (parent + the six native capability branches)
  evidence/vectors.json                           audit counts, new-case verdicts, the generator result, worked values
The generator run happens in evidence/gen-scratch/ (a copy of the product generator's inputs layout). With --check,
everything is rebuilt in memory and compared; nothing is written except the scratch generator directory.
Nothing here runs a provider, node, cargo or a frame codec.
"""
import argparse
import copy
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PARENT = "docs/implementation/m3/snapshot-plan-c/c2pm-1-r2/completion/manifest-schema.completed.v1.json"
PARENT_PIN = (25247, "80254f9e1fd9a3014f5bba73715f1c882d0d511293cc154cc2b59cfbf9d37353")
HS = "docs/implementation/m3/native-successors-fa/nss-f1/design/native/provider-handshake.schemas.v1.json"
HS_LOCAL = "/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/nss-f1/design/native/provider-handshake.schemas.v1.json"
HS_PIN = (39848, "260fb53558de21301bdb1cb66617a7a19711918160e1d8d48ba8acd2df554a0a")
SUB, VER = "typescript-semantic", 2
# The native capability matrix's semantic TypeScript capabilities and their relation/rung pairs
# (native-capability-matrix.v2.json `capabilities`), the same pairs CMS's preview typescript/1 rows carry.
RELATIONS = [("imports", "resolved-target"), ("references", "resolved-binding"), ("calls", "resolved-callee"),
             ("types", "checked"), ("reachability", "from-resolved-calls")]
PREFIX = b"opensip.product.v1\x00"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def jcs(v):
    # RFC 8785 for the integer/string/array/object values used here (no floats).
    return json.dumps(v, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def H(domain, value):
    b = jcs(value)
    return sha(PREFIX + domain.encode() + b"\x00" + struct.pack(">Q", len(b)) + b)


def pinned(path, pin):
    b = open(path, "rb").read()
    if (len(b), sha(b)) != pin:
        sys.exit(f"not at its pin: {path}")
    return b


def ts_tokens():
    if os.path.exists(HS_LOCAL):
        b = pinned(HS_LOCAL, HS_PIN)
    else:
        sys.exit("NSS-F1 handshake copy not found")
    return json.loads(b)["$defs"]["TypeScriptCapabilityToken"]["enum"]


def branches(tokens):
    out = [{
        "type": "object",
        "properties": {
            "capabilityId": {"const": SUB + ".protocol"},
            "roleSubprotocol": {"const": SUB},
            "subprotocolVersion": {"const": VER},
            "declarationData": {
                "type": "object",
                "properties": {
                    "capabilityTokens": {
                        "type": "array",
                        "items": {"type": "string", "enum": list(tokens)},
                        "minItems": 4,
                        "maxItems": len(tokens),
                        "uniqueItems": True,
                    }
                },
                "required": ["capabilityTokens"],
                "additionalProperties": False,
            },
        },
        "required": ["capabilityId", "roleSubprotocol", "subprotocolVersion", "declarationData"],
        "additionalProperties": False,
    }]
    for relation, rung in RELATIONS:
        out.append({
            "type": "object",
            "properties": {
                "capabilityId": {"const": SUB + "." + relation},
                "roleSubprotocol": {"const": SUB},
                "subprotocolVersion": {"const": VER},
                "declarationData": {
                    "type": "object",
                    "properties": {"relation": {"const": relation}, "rung": {"const": rung}},
                    "required": ["relation", "rung"],
                    "additionalProperties": False,
                },
            },
            "required": ["capabilityId", "roleSubprotocol", "subprotocolVersion", "declarationData"],
            "additionalProperties": False,
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--product", required=True)
    ap.add_argument("--arch", required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, os.path.join(a.product, "tools", "contracts", "python-packages"))
    import jsonschema

    parent_bytes = pinned(os.path.join(a.arch, PARENT), PARENT_PIN)
    product_input = open(os.path.join(a.product, "tools/security/inputs/manifest-schema.json"), "rb").read()
    if product_input != parent_bytes:
        sys.exit("product manifest-schema input is not the parent")
    parent = json.loads(parent_bytes)
    if json.dumps(parent, indent=2).encode() + b"\n" != parent_bytes:
        sys.exit("parent serialization is not indent=2 + LF")
    tokens = ts_tokens()
    child = copy.deepcopy(parent)
    child["$defs"]["capability"]["oneOf"].extend(branches(tokens))
    child_bytes = json.dumps(child, indent=2).encode() + b"\n"

    # Structural diff: exactly six appended oneOf branches, nothing else.
    probe = copy.deepcopy(child)
    del probe["$defs"]["capability"]["oneOf"][len(parent["$defs"]["capability"]["oneOf"]):]
    assert probe == parent

    pv = jsonschema.Draft202012Validator(parent)
    cv = jsonschema.Draft202012Validator(child)
    shape = os.path.join(a.product, "crates/security/tests/fixtures/manifest268-shape.ndjson")
    n = agree = parent_ok = 0
    flips = []
    template = None
    for line in open(shape, encoding="utf-8"):
        case = json.loads(line)
        n += 1
        p, c = pv.is_valid(case["value"]), cv.is_valid(case["value"])
        parent_ok += p == case["valid"]
        agree += p == c
        if p != c:
            flips.append(case["label"])
        if template is None and case["label"] == "security-full":
            template = case["value"]
    assert parent_ok == n and agree == n and not flips, (parent_ok, agree, flips[:5])

    # New cases: a TS2 provider (analyzer) manifest built from the fixture's security-full template.
    def provider(caps, major=VER):
        m = copy.deepcopy(template)
        m["capabilities"] = caps
        m["compatibility"]["providerProtocol"] = major
        m["closureProtocolMajor"] = major
        return m

    identity = ["coverage-v3", "fact-identity-fact2", "plan-identity-plan2", "source-identity-snapshot2"]
    base_tokens = sorted(identity + ["multi-stage-analyze-v1", "native-context-inputs-v1", "native-context-v2",
                                     "resolution-completeness-v2", "sealed-vfs-v1", "typescript-semantic-facts-v1",
                                     "unresolved-edge-v1"])
    proto = {"capabilityId": SUB + ".protocol", "roleSubprotocol": SUB, "subprotocolVersion": VER,
             "declarationData": {"capabilityTokens": base_tokens}}

    def rel(r, g):
        return {"capabilityId": SUB + "." + r, "roleSubprotocol": SUB, "subprotocolVersion": VER,
                "declarationData": {"relation": r, "rung": g}}

    cases = [
        ("ts2-protocol-row-only", provider([proto]), True),
        ("ts2-protocol-and-imports-rows", provider([proto, rel("imports", "resolved-target")]), True),
        ("ts2-all-six-rows", provider([proto] + [rel(r, g) for r, g in RELATIONS]), True),
        ("ts2-tokens-in-any-order", provider([dict(proto, declarationData={"capabilityTokens": list(reversed(base_tokens))})]), True),
        ("ts2-with-symbol-census", provider([dict(proto, declarationData={"capabilityTokens": sorted(base_tokens + ["symbol-census-v1"])})]), True),
        ("ts2-unknown-token", provider([dict(proto, declarationData={"capabilityTokens": base_tokens + ["dependency-source-v1"]})]), False),
        ("ts2-duplicate-token", provider([dict(proto, declarationData={"capabilityTokens": base_tokens + ["sealed-vfs-v1"]})]), False),
        ("ts2-three-tokens", provider([dict(proto, declarationData={"capabilityTokens": identity[:3]})]), False),
        ("ts2-protocol-row-extra-member", provider([dict(proto, declarationData={"capabilityTokens": base_tokens, "x": 1})]), False),
        ("ts2-relation-row-wrong-rung", provider([proto, rel("imports", "resolved-binding")]), False),
        ("ts2-native-subprotocol-at-version-1", provider([dict(proto, subprotocolVersion=1)]), False),
        ("ts2-preview-subprotocol-at-version-2", provider([dict(proto, roleSubprotocol="typescript")]), False),
        ("ts2-unregistered-capability-id", provider([dict(rel("imports", "resolved-target"), capabilityId=SUB + ".syntax")]), False),
    ]
    new_results = []
    for name, m, ok in cases:
        p, c = pv.is_valid(m), cv.is_valid(m)
        assert c == ok, (name, c)
        assert not (p and not c), name  # the copy only widens
        new_results.append({"case": name, "copyValid": c, "parentValid": p})

    # The product generator over the copy, in scratch.
    scratch = os.path.join(HERE, "gen-scratch")
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(os.path.join(scratch, "inputs"))
    os.makedirs(os.path.join(scratch, "product/crates/security/src"))
    open(os.path.join(scratch, "inputs/manifest-schema.json"), "wb").write(child_bytes)
    gen = os.path.join(a.product, "tools/security/generators/manifest_shape.py")
    run = subprocess.run([sys.executable, "-I", "-B", gen, scratch], capture_output=True, text=True)
    generated = os.path.join(scratch, "product/crates/security/src/component_manifest_shape.rs")
    gen_result = {"exit": run.returncode, "stderr": run.stderr[-400:],
                  "generatedSha256": sha(open(generated, "rb").read()) if os.path.exists(generated) else None}
    assert run.returncode == 0, gen_result

    # Worked values: X-F4-1's closure joins on the product fixture, and X-F4-4's runtime payload digest.
    fx = json.load(open(os.path.join(a.product, "crates/host/tests/fixtures/native-context-fixtures.current.json")))
    joins = []
    for o in fx["typescriptUniverse"]["objects"]:
        if o["descriptor"].get("kind") in ("toolchain", "stdlib") and o.get("domain") == "closure":
            joins.append({"kind": o["descriptor"]["kind"], "closureId": o["id"],
                          "recomputed": H("closure", o["descriptor"]) == o["id"].split(":")[1]})
    ctx = fx["contexts"]["typescript"]
    runtime_artifact = ctx["toolClosure"]["closureId"].split(":", 1)[1]
    empty_sha = sha(b"")
    payload_rows = [{"path": "etc/openssl.cnf", "sha256": empty_sha, "bytes": 0}]
    payload_record = {"schemaVersion": 1, "files": payload_rows}
    vectors = {
        "schemaVersion": 1,
        "standing": "NSS-F4 r1 evidence. Not a release, not a signature, not product acceptance.",
        "parent": {"path": PARENT, "bytes": PARENT_PIN[0], "sha256": PARENT_PIN[1]},
        "copy": {"bytes": len(child_bytes), "sha256": sha(child_bytes), "appendedBranches": 6},
        "tokens": {"source": HS, "sha256": HS_PIN[1], "enum": tokens},
        "shapeAudit": {"cases": n, "parentReproducesFixture": parent_ok, "parentEqualsCopy": agree, "flips": flips},
        "newCases": new_results,
        "generator": gen_result,
        "closureJoins": {"fixture": "crates/host/tests/fixtures/native-context-fixtures.current.json",
                         "rows": joins,
                         "runtimeArtifactSha256FromContextToolClosure": runtime_artifact},
        "runtimePayload": {"record": payload_record, "jcs": jcs(payload_record).decode(),
                           "runtimePayloadSha256": sha(jcs(payload_record))},
    }
    targets = {
        os.path.join(ROOT, "completion/manifest-schema.completed.v1.json"): child_bytes,
        os.path.join(HERE, "vectors.json"): (json.dumps(vectors, indent=2, sort_keys=True) + "\n").encode(),
    }
    if a.check:
        bad = [p for p, b in targets.items() if not os.path.exists(p) or open(p, "rb").read() != b]
        print("MATCHES" if not bad else "DIFFERS: " + ", ".join(bad))
        sys.exit(1 if bad else 0)
    for p, b in targets.items():
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(b)
    print(json.dumps({"copy": vectors["copy"], "shapeAudit": vectors["shapeAudit"], "newCases": len(new_results),
                      "generator": gen_result["exit"], "runtimePayloadSha256": vectors["runtimePayload"]["runtimePayloadSha256"]},
                     indent=1))


if __name__ == "__main__":
    main()
