"""NSS-F4 binding (X-NSS4-B; F4 plan r4 section 5a): materialize the adopted successor in FA-2's form.

Usage (python3.14 -I -B):
    build_binding.py --source <lead nss-f4 dir> --arch <opensip_arch checkout> --product <opensip checkout>
                     --base-product <commit> [--check]

Deterministic. It reads only the adopted NSS-F4 directory, the architecture checkout and the product checkout
(git reads the base product blobs). It writes, or with --check compares:

  architecture, docs/implementation/m3/native-successors-fa/:
    nss-f4/<every adopted NSS-F4 file>        byte copies (the adoption receipt's table, checked first)
    nss-f4/product/tools/security/inputs/manifest-schema.json, sources.json
    nss-f4/product/crates/security/src/generated/component_manifest_shape.rs
                                              byte copies of the product rows (c2pm-body-r1's layout)
    nss-f4/materialization-map.json, nss-f4/successor.json, nss-f4-subject.json
  product:
    tools/security/inputs/manifest-schema.json (the CMS successor copy), tools/security/inputs/sources.json (re-pinned).

The generated shape is not written here: tools/generate_security_tables.py --write produces it from the pinned inputs
(run it after this script, then this script again, so the arch copy is the regenerated file; --check then requires
the generator's --check to be clean as well, which the binding's XB-1 runs). nss-f4/README.md is read from disk. The
unit's assent (nss-f4-unit.json) and the lock row follow the binding's independent review.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

BASE = "docs/implementation/m3/native-successors-fa"
UNIT = BASE + "/nss-f4"
SUBJECT = BASE + "/nss-f4-subject.json"
SUCCESSOR = UNIT + "/successor.json"
MAP = UNIT + "/materialization-map.json"
README = UNIT + "/README.md"
BUILD = UNIT + "/evidence/build_binding.py"

# ADOPTION-NSS-F4.md, "What was reviewed", and HANDOFF-ADOPTION.md section 1.
COPIED = [
    "ADOPTION-NSS-F4.md", "NSS-F4-r3.md", "overrides.json", "completion/manifest-schema.completed.v1.json",
    "evidence/build_overrides.py", "evidence/build_nss_f4.py", "evidence/vectors.json",
]
ADOPTED = {
    "NSS-F4-r3.md": "27a9a9bc6ef54a0ac0456606143ebadd82cc3325c1c5684b6818e1a0ec3abf8b",
    "completion/manifest-schema.completed.v1.json":
        "e698f9d6ae305a2fbd2e4b47c1f66a77c712667350eac3e16227acb4f9df6af4",
    "overrides.json": "049f1fa5d9e78a6e5561ea3627062fd9b7dad1682f1409294bd45ec9b56986cb",
}
COPY = "completion/manifest-schema.completed.v1.json"
SCHEMA = "tools/security/inputs/manifest-schema.json"
SOURCES = "tools/security/inputs/sources.json"
SHAPE = "crates/security/src/generated/component_manifest_shape.rs"
OLD_SCHEMA = (25247, "80254f9e1fd9a3014f5bba73715f1c882d0d511293cc154cc2b59cfbf9d37353")
CMS_PARENT = "docs/implementation/m3/snapshot-plan-c/c2pm-1-r2/completion/manifest-schema.completed.v1.json"
STANDING = (
    "PROPOSED NSS-F4 r3 contract successor (adopted LD-COORD-NSSF4; F4 plan r4 X-NSS4-B binding): the TypeScript "
    "release-closure interface rulings. The universe's runtimeArtifactSha256 and providerArtifactSha256 are the "
    "closure2 suffixes of the toolchain closure T and the provider closure P (X-F4-1); the TypeScript native "
    "capability surface is six typescript-semantic/2 branches, a protocol row carrying the capability tokens and five "
    "relation rows, in a complete successor copy of the component manifest schema, with C2PM-1's analyzer "
    "subprotocol selected for TypeScript at major 2 (X-F4-3); runtimePayloadSha256 is SHA-256 of JCS({schemaVersion "
    "1, files}) over an explicit runtime-support inventory, exactly {etc/openssl.cnf} at M3 (X-F4-4). Six insert-only "
    "passage overrides; the copy only appends oneOf branches, and every existing manifest keeps its verdict. No "
    "release-format byte, retained identity, vector or PlanId changes.")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin(path, raw):
    return {"path": path, "bytes": len(raw), "sha256": sha(raw)}


def dump(value):
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode("ascii")


def git_show(repo, commit, path):
    return subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"], check=True,
                          capture_output=True).stdout


def fail(msg):
    sys.exit("build_binding: " + msg)


def product_edits(product, base, src):
    copy = src[COPY]
    blobs = {p: git_show(product, base, p) for p in (SCHEMA, SOURCES, SHAPE)}
    if (len(blobs[SCHEMA]), sha(blobs[SCHEMA])) != OLD_SCHEMA:
        fail("base manifest schema is not the CMS parent")
    old = (f'"bytes": {OLD_SCHEMA[0]},\n      "sha256": "{OLD_SCHEMA[1]}"')
    text = blobs[SOURCES].decode("utf-8")
    if text.count(old) != 1:
        fail("sources.json manifest-schema row")
    sources = text.replace(old, f'"bytes": {len(copy)},\n      "sha256": "{sha(copy)}"').encode("utf-8")
    shape = open(os.path.join(product, SHAPE), "rb").read()
    if f"// SHA256 {sha(copy)}".encode() not in shape:
        fail("the product's generated shape is not regenerated from the copy (run generate_security_tables --write)")
    return {SCHEMA: copy, SOURCES: sources}, shape, blobs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--arch", required=True)
    ap.add_argument("--product", required=True)
    ap.add_argument("--base-product", required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    src = {}
    for rel in COPIED:
        raw = open(os.path.join(a.source, rel), "rb").read()
        if rel in ADOPTED and sha(raw) != ADOPTED[rel]:
            fail("adopted file differs from the receipt: " + rel)
        src[rel] = raw
    cms_parent = open(os.path.join(a.arch, CMS_PARENT), "rb").read()
    if (len(cms_parent), sha(cms_parent)) != OLD_SCHEMA:
        fail("the architecture CMS parent is not the product's base input")

    product_out, shape, blobs = product_edits(a.product, a.base_product, src)
    arch_out = {UNIT + "/" + rel: raw for rel, raw in src.items()}
    for p, raw in product_out.items():
        arch_out[UNIT + "/product/" + p] = raw
    arch_out[UNIT + "/product/" + SHAPE] = shape

    files = []
    for p, after in sorted(dict(product_out, **{SHAPE: shape}).items()):
        files.append({"productPath": p, "candidatePath": UNIT + "/product/" + p,
                      "before": {"bytes": len(blobs[p]), "sha256": sha(blobs[p])},
                      "after": {"bytes": len(after), "sha256": sha(after)}})
    arch_out[MAP] = dump({
        "schemaVersion": 1,
        "standing": ("Exact product bytes for NSS-F4's binding (X-NSS4-B): each candidate is copied to its product path. "
                     "The manifest schema is the adopted CMS successor copy; sources.json re-pins it; the shape is "
                     "regenerated from it by tools/generate_security_tables.py. Independent review and root assent are "
                     "required before selection. The native selection, AnalyzerSubprotocol's production constructor, "
                     "the extended pair rule, Hello's array and the universe's artifact members belong to later units "
                     "(X-NSS4-SEC, X-NSS4-D, X-NSS4-C4)."),
        "baseProductHead": a.base_product,
        "files": files,
    })

    overrides = json.loads(src["overrides.json"])["passageOverrides"]
    parent_paths = sorted({o["parent"]["path"] for o in overrides} | {CMS_PARENT})
    parents = [pin(p, open(os.path.join(a.arch, p), "rb").read()) for p in parent_paths]
    pmap = {r["path"]: r for r in parents}
    for o in overrides:
        if pmap.get(o["parent"]["path"]) != o["parent"]:
            fail("override parent is not at its pinned bytes: " + o["parent"]["path"])
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
