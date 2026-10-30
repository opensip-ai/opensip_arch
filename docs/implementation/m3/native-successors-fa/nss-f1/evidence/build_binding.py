"""NSS-F1 binding (X-NSS-B; F1 plan r6 section 3.12.1): materialize the adopted successor in FA-2's form.

Usage (python3.14 -I -B):
    build_binding.py --source <lead nss-f1 dir> --arch <opensip_arch checkout> --product <opensip checkout>
                     [--base-product <commit>] [--check]

Deterministic. It reads only the adopted NSS-F1 directory, the architecture checkout and the product checkout
(git is used only to read base blobs of the product). It writes, or with --check compares:

  architecture, docs/implementation/m3/native-successors-fa/:
    nss-f1/<every adopted NSS-F1 file>        byte copies (NSS-F1 adoption receipt: "copied unchanged")
    nss-f1/product/schemas/sources/native-context-inputs-v1.schema.json
                                              the product copy of the new schema (its design bytes)
    nss-f1/product/schemas/admission-registry.json, admission-source-map.json, registry.json, source-map.json
    nss-f1/product/tools/contracts/generator-closure.json
                                              byte copies of the product's five re-pinned live-pin files
    nss-f1/materialization-map.json, nss-f1/successor.json, nss-f1-subject.json
  product:
    schemas/sources/handshake-v1.schema.json, schemas/sources/native-context-inputs-v1.schema.json,
    the five live pins, crates/identity/src/schema_registry.rs (the handshake SourcePin),
    crates/components/tests/data/native-rust3-profile-cases.v1.json (currentAuthority) and the two digest
    constants that pin that fixture in crates/components/src/provider_protocol/rust3/replay_tests.rs.

Every product edit is computed from the base product blob, so --check is meaningful after the edits.
successor.json's passageOverrides are overrides.json's, verbatim and in order. nss-f1/README.md is read from
disk (written by the binding author). The unit's assent (nss-f1-unit.json) is not built here: it pins the
binding's independent review, which follows this candidate.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

BASE = "docs/implementation/m3/native-successors-fa"
UNIT = BASE + "/nss-f1"
SUBJECT = BASE + "/nss-f1-subject.json"
SUCCESSOR = UNIT + "/successor.json"
MAP = UNIT + "/materialization-map.json"
README = UNIT + "/README.md"
BUILD = UNIT + "/evidence/build_binding.py"
BASE_PRODUCT = "d64341073e9e89266729e1e6d9b18110649007b7"

# The adopted files (ADOPTION-NSS-F1.md, "These files and this receipt are copied unchanged").
COPIED = [
    "ADOPTION-NSS-F1.md", "NSS-F1-r2.md", "overrides.json", "section-9-5a.md",
    "design/native/native-context-inputs.schemas.v1.json", "design/native/provider-handshake.schemas.v1.json",
    "product/schemas/sources/handshake-v1.schema.json",
    "evidence/bound-selectors.txt", "evidence/bound_selectors.py", "evidence/build_nss_f1.py",
    "evidence/build_overrides.py", "evidence/vectors.json",
]
# The receipt's own table, checked before anything is copied.
ADOPTED = {
    "NSS-F1-r2.md": "9e4a5839fe69f36408553b5f2aee6b21161a66651bc82223cb23e9d6bfa6503a",
    "section-9-5a.md": "9a021ab79d636a61664ffd65dc7a531bb118d0d6a4c2032e5152a06dec81945f",
    "design/native/native-context-inputs.schemas.v1.json":
        "c6bb1eeac84ea57332be5765d74516e3e5562a4d902d9575daffcef10bf6e730",
    "design/native/provider-handshake.schemas.v1.json":
        "260fb53558de21301bdb1cb66617a7a19711918160e1d8d48ba8acd2df554a0a",
    "product/schemas/sources/handshake-v1.schema.json":
        "260fb53558de21301bdb1cb66617a7a19711918160e1d8d48ba8acd2df554a0a",
    "overrides.json": "723ff2ef53fa6af3b49526770d56885cd62cdaf44e429119dfdfd565ee4cc832",
}
NEW_SCHEMA_ID = "opensip.product.native-context-inputs.1"
NEW_SCHEMA_SRC = "design/native/native-context-inputs.schemas.v1.json"
NEW_PRODUCT = "schemas/sources/native-context-inputs-v1.schema.json"
HS_PRODUCT = "schemas/sources/handshake-v1.schema.json"
HS_SRC = "product/schemas/sources/handshake-v1.schema.json"
HS_ID = "opensip.product.provider-handshake.1"
OLD_HS = (38182, "1fc57cbc8d71dfae9ec6ce9534415c60e810de5aa39134d95a37209ce2694edb")
OLD_HS_ARCH = BASE + "/rust-commit-alignment-r2/product/schemas/sources/handshake-v1.schema.json"

AREG, AMAP, REG, SMAP, CLOSURE = ("schemas/admission-registry.json", "schemas/admission-source-map.json",
                                  "schemas/registry.json", "schemas/source-map.json",
                                  "tools/contracts/generator-closure.json")
LIVE_PINS = [AREG, AMAP, REG, SMAP, CLOSURE]
IDENTITY = "crates/identity/src/schema_registry.rs"
FIXTURE = "crates/components/tests/data/native-rust3-profile-cases.v1.json"
REPLAY = "crates/components/src/provider_protocol/rust3/replay_tests.rs"

NE = "docs/v2/contracts/product-v1/native-evidence.md"
RCA = BASE + "/rust-commit-alignment-r2"
PARENTS = [NE, RCA + "/design/native/provider-startup.schemas.v1.json",
           RCA + "/product/schemas/sources/startup-v1.schema.json",
           RCA + "/design/native/provider-handshake.schemas.v1.json", OLD_HS_ARCH,
           "docs/coop/design-corrections/native/typescript-protocol2-order.v1.json"]
STANDING = (
    "PROPOSED NSS-F1 r2 native contract successor (adopted LD-COORD-NSSF1; F1 plan r6 X-NSS-B binding): the TS2 "
    "native-context inputs carrier. A new optional, non-identity typescript-semantic capability token "
    "native-context-inputs-v1 adds nativeContextInputs to OpenUniverse (TypeScriptOpenUniverseV3: the retained "
    "context, configuration-graph and layout preimage bytes and the unit root) and a token-gated pre-Analyze "
    "TypeScriptPreAnalyzeInputMismatchV1. Text passage overrides of native-evidence (nine, insert-only, one of them "
    "appending section 9.5a), JSON Pointer overrides of the two provider-startup copies (four each) and of the "
    "TypeScript protocol-2 order table (one), complete successor copies of the two provider-handshake copies, a new "
    "schema document with its product copy, and byte copies of the five re-pinned product live-pin files. Without "
    "the token every frame, payload, vector, identity and PlanId is byte-identical. No major, frame, phase, "
    "terminal, limit member or identity version changes.")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin(path, raw):
    return {"path": path, "bytes": len(raw), "sha256": sha(raw)}


def dump(value):
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode("ascii")


def jdump(value):
    # The product's JSON files round-trip exactly through this form (checked on the base blobs).
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def git_show(repo, commit, path):
    return subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"], check=True,
                          capture_output=True).stdout


def fail(msg):
    sys.exit("build_binding: " + msg)


def one(text, old, new):
    if text.count(old) != 1:
        fail("edit anchor is not unique: " + old[:80])
    return text.replace(old, new)


def rust_digest(hexdigest, indent="            "):
    nums = [str(b) for b in bytes.fromhex(hexdigest)]
    # rustfmt's layout for these arrays: as many as fit in 99 columns (the observed layout of this file).
    lines, cur = [], indent
    for n in nums:
        piece = n + ","
        if cur != indent and len(cur) + 1 + len(piece) > 99:
            lines.append(cur)
            cur = indent + piece
        else:
            cur = cur + ("" if cur == indent else " ") + piece
    lines.append(cur)
    return "\n".join(lines)


def product_edits(product, base, src):
    hs = src[HS_SRC]
    new = src[NEW_SCHEMA_SRC]
    hs_new = (len(hs), sha(hs))
    new_pin = (len(new), sha(new))
    unit_hs = UNIT + "/" + HS_SRC
    unit_new = UNIT + "/product/" + NEW_PRODUCT
    out = {HS_PRODUCT: hs, NEW_PRODUCT: new}
    blobs = {p: git_show(product, base, p) for p in LIVE_PINS + [IDENTITY, FIXTURE, REPLAY, HS_PRODUCT]}
    if (len(blobs[HS_PRODUCT]), sha(blobs[HS_PRODUCT])) != OLD_HS:
        fail("base handshake is not the RCA-r2 parent")
    for p in LIVE_PINS + [FIXTURE]:
        if jdump(json.loads(blobs[p])) != blobs[p]:
            fail("base JSON does not round-trip: " + p)

    # admission-registry.json: the handshake row, and the new row in schemaId order.
    areg = json.loads(blobs[AREG])
    rows = areg["sources"]
    [hrow] = [r for r in rows if r["schemaId"] == HS_ID]
    if (hrow["bytes"], hrow["sha256"]) != OLD_HS:
        fail("admission registry handshake row")
    hrow["bytes"], hrow["sha256"] = hs_new
    if any(r["schemaId"] == NEW_SCHEMA_ID for r in rows) or any(a["schemaId"] == HS_ID for a in areg["aliases"]):
        fail("admission registry already has the new row, or aliases the handshake")
    rows.append({"schemaId": NEW_SCHEMA_ID, "sourcePath": NEW_PRODUCT, "bytes": new_pin[0], "sha256": new_pin[1]})
    rows.sort(key=lambda r: r["schemaId"])
    out[AREG] = jdump(areg)
    areg_arch = UNIT + "/product/" + AREG

    # admission-source-map.json: the registry's architecture source, the handshake row, and the new row placed
    # after the last row whose schemaId sorts before it (the map keeps its own order).
    amap = json.loads(blobs[AMAP])
    amap["registryArchitectureSource"] = {"path": areg_arch, "bytes": len(out[AREG]), "sha256": sha(out[AREG])}
    [hrow] = [r for r in amap["sources"] if r["schemaId"] == HS_ID]
    if hrow["architectureSource"] != {"path": OLD_HS_ARCH, "bytes": OLD_HS[0], "sha256": OLD_HS[1]}:
        fail("admission source map handshake row")
    hrow["architectureSource"] = {"path": unit_hs, "bytes": hs_new[0], "sha256": hs_new[1]}
    ids = [r["schemaId"] for r in amap["sources"]]
    at = max(i for i, s in enumerate(ids) if s.startswith("opensip.product.") and s < NEW_SCHEMA_ID) + 1
    amap["sources"].insert(at, {"schemaId": NEW_SCHEMA_ID, "implementationPath": NEW_PRODUCT,
                                "architectureSource": {"path": unit_new, "bytes": new_pin[0],
                                                       "sha256": new_pin[1]}})
    out[AMAP] = jdump(amap)

    # source-map.json (generation): the handshake row's architecture source only.
    smap = json.loads(blobs[SMAP])
    [hrow] = [r for r in smap["sources"] if r["schemaId"] == HS_ID]
    if hrow["architectureSource"] != {"path": OLD_HS_ARCH, "bytes": OLD_HS[0], "sha256": OLD_HS[1]}:
        fail("source map handshake row")
    hrow["architectureSource"] = {"path": unit_hs, "bytes": hs_new[0], "sha256": hs_new[1]}
    out[SMAP] = jdump(smap)

    # generator-closure.json: the handshake and source-map pins.
    closure = json.loads(blobs[CLOSURE])
    byp = {r["path"]: r for r in closure["files"]}
    if (byp[HS_PRODUCT]["bytes"], byp[HS_PRODUCT]["sha256"]) != OLD_HS:
        fail("closure handshake pin")
    if (byp[SMAP]["bytes"], byp[SMAP]["sha256"]) != (len(blobs[SMAP]), sha(blobs[SMAP])):
        fail("closure source-map pin")
    byp[HS_PRODUCT]["bytes"], byp[HS_PRODUCT]["sha256"] = hs_new
    byp[SMAP]["bytes"], byp[SMAP]["sha256"] = len(out[SMAP]), sha(out[SMAP])
    out[CLOSURE] = jdump(closure)

    # registry.json (generation): the handshake source digest, the recipe's source set and closure digest.
    reg = json.loads(blobs[REG])
    [hrow] = [r for r in reg["sources"] if r["schemaId"] == HS_ID]
    if hrow["sourceSha256"] != OLD_HS[1]:
        fail("registry handshake row")
    hrow["sourceSha256"] = hs_new[1]
    [recipe] = reg["recipes"]
    if recipe["generatorClosureSha256"] != sha(blobs[CLOSURE]) or OLD_HS[1] not in recipe["sourceSha256s"]:
        fail("registry recipe")
    recipe["sourceSha256s"] = sorted(hs_new[1] if s == OLD_HS[1] else s for s in recipe["sourceSha256s"])
    recipe["generatorClosureSha256"] = sha(out[CLOSURE])
    out[REG] = jdump(reg)

    # identity SOURCE_PINS: the handshake pin (bytes and digest as a decimal array).
    text = blobs[IDENTITY].decode("utf-8")
    old = (f'        id: "{HS_ID}",\n        path: "{HS_PRODUCT}",\n        bytes: {OLD_HS[0]},\n'
           f'        sha256: [\n{rust_digest(OLD_HS[1])}\n        ],')
    new_text = (f'        id: "{HS_ID}",\n        path: "{HS_PRODUCT}",\n        bytes: {hs_new[0]},\n'
                f'        sha256: [\n{rust_digest(hs_new[1])}\n        ],')
    out[IDENTITY] = one(text, old, new_text).encode("utf-8")

    # The rust3 profile fixture's currentAuthority, and the two constants pinning the fixture's bytes.
    fx = json.loads(blobs[FIXTURE])
    if fx["currentAuthority"]["path"] != HS_PRODUCT or fx["currentAuthority"]["sha256"] != OLD_HS[1]:
        fail("fixture currentAuthority")
    fx["currentAuthority"]["sha256"] = hs_new[1]
    out[FIXTURE] = jdump(fx)
    text = blobs[REPLAY].decode("utf-8")
    old_fx = f'"{sha(blobs[FIXTURE])}"'
    if text.count(old_fx) != 2:
        fail("replay fixture digest constants")
    out[REPLAY] = text.replace(old_fx, f'"{sha(out[FIXTURE])}"').encode("utf-8")
    return out, blobs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--arch", required=True)
    ap.add_argument("--product", required=True)
    ap.add_argument("--base-product", default=BASE_PRODUCT)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    src = {}
    for rel in COPIED:
        raw = open(os.path.join(a.source, rel), "rb").read()
        if rel in ADOPTED and sha(raw) != ADOPTED[rel]:
            fail("adopted file differs from the receipt: " + rel)
        src[rel] = raw

    arch_out = {UNIT + "/" + rel: raw for rel, raw in src.items()}
    arch_out[UNIT + "/product/" + NEW_PRODUCT] = src[NEW_SCHEMA_SRC]
    product_out, blobs = product_edits(a.product, a.base_product, src)
    for p in LIVE_PINS:
        arch_out[UNIT + "/product/" + p] = product_out[p]

    files = [{"productPath": HS_PRODUCT, "candidatePath": UNIT + "/" + HS_SRC,
              "before": {"bytes": OLD_HS[0], "sha256": OLD_HS[1]},
              "after": {"bytes": len(src[HS_SRC]), "sha256": sha(src[HS_SRC])}},
             {"productPath": NEW_PRODUCT, "candidatePath": UNIT + "/product/" + NEW_PRODUCT, "before": None,
              "after": {"bytes": len(src[NEW_SCHEMA_SRC]), "sha256": sha(src[NEW_SCHEMA_SRC])}}]
    for p in LIVE_PINS:
        files.append({"productPath": p, "candidatePath": UNIT + "/product/" + p,
                      "before": {"bytes": len(blobs[p]), "sha256": sha(blobs[p])},
                      "after": {"bytes": len(product_out[p]), "sha256": sha(product_out[p])}})
    arch_out[MAP] = dump({
        "schemaVersion": 1,
        "standing": ("Exact product bytes for NSS-F1's binding (X-NSS-B): each candidate is copied to its product path. "
                     "The binding also re-pins the handshake SourcePin in crates/identity/src/schema_registry.rs, the "
                     "currentAuthority of crates/components/tests/data/native-rust3-profile-cases.v1.json and that "
                     "fixture's two digest constants in rust3/replay_tests.rs, which this map does not fix. The new "
                     "schema is admission-registered only: its Rust embedding, identity source pin and generated "
                     "carriers, the regenerated outputs and the native-carriers-v1 records belong to later units. "
                     "Independent review and root assent are required before selection."),
        "baseProductHead": a.base_product,
        "files": files,
    })

    overrides = json.loads(src["overrides.json"])["passageOverrides"]
    parents = sorted([pin(p, open(os.path.join(a.arch, p), "rb").read()) for p in PARENTS], key=lambda r: r["path"])
    pmap = {r["path"]: r for r in parents}
    for o in overrides:
        if pmap.get(o["parent"]["path"]) != o["parent"]:
            fail("override parent is not a pinned parent: " + o["parent"]["path"])
    disk = {p: open(os.path.join(a.arch, p), "rb").read() for p in (README, BUILD)}
    candidates = sorted([pin(p, b) for p, b in dict(arch_out, **disk).items()], key=lambda r: r["path"])
    successor = dump({"schemaVersion": 1, "standing": STANDING, "parents": parents,
                      "passageOverrides": overrides, "candidates": candidates})
    arch_out[SUCCESSOR] = successor
    subject = sorted(candidates + [pin(SUCCESSOR, successor)], key=lambda r: r["path"])
    arch_out[SUBJECT] = dump({"schemaVersion": 1, "files": subject})

    targets = [(a.arch, p, b) for p, b in sorted(arch_out.items())] + \
              [(a.product, p, b) for p, b in sorted(product_out.items())]
    if a.check:
        bad = [os.path.join(r, p) for r, p, b in targets
               if not os.path.isfile(os.path.join(r, p)) or open(os.path.join(r, p), "rb").read() != b]
        print("MATCHES" if not bad else "DIFFERS: " + ", ".join(bad))
        sys.exit(1 if bad else 0)
    for root, p, b in targets:
        os.makedirs(os.path.dirname(os.path.join(root, p)), exist_ok=True)
        open(os.path.join(root, p), "wb").write(b)
    for root, p, b in targets:
        print(sha(b), len(b), ("arch " if root == a.arch else "product ") + p)


if __name__ == "__main__":
    main()
