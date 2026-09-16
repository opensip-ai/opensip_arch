#!/usr/bin/env python3
"""Real temporary-file build/pin/read fixture for the PS-04 report-asset binding.

Builds an actual release tree in a temporary directory, emits the private asset
manifest excluding exactly the pinned manifest path, computes the host-embedded
pin over the manifest's stored bytes, then reads it back through the modelled
load path. Mutations exercise the refusals the design claims.

This is design evidence over a temporary filesystem. It is not product code, not
a release build, not a browser test and establishes no qualification.

Usage: check_report_asset_fixture.py [--json]
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROLES = {"script", "style", "font", "image", "notice"}


# --- modelled admission (mirrors report-asset-binding.v1.json) ---------------

def canonical_relative_path(value):
    if not isinstance(value, str) or not value or len(value) > 4096:
        return False
    if value.startswith("/") or value.endswith("/"):
        return False
    if "\\" in value or "\0" in value or "//" in value or "://" in value:
        return False
    return all(part not in ("", ".", "..") for part in value.split("/"))


def admit_manifest(document, asset_root, manifest_path):
    if not isinstance(document, dict):
        return "not-an-object"
    if set(document) != {"schemaVersion", "projectionSchemaSha256s", "assets"}:
        return "member-set"
    version = document["schemaVersion"]
    if isinstance(version, bool) or not isinstance(version, int) or version != 1:
        return "schema-version"
    digests = document["projectionSchemaSha256s"]
    if not isinstance(digests, list) or not digests:
        return "projection-digests-empty"
    if len(set(digests)) != len(digests) or digests != sorted(digests):
        return "projection-digests-order-or-duplicate"
    assets = document["assets"]
    if not isinstance(assets, list) or not assets:
        return "assets-empty"
    seen = []
    for row in assets:
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "bytes", "role"}:
            return "asset-member-set"
        if not canonical_relative_path(row["path"]):
            return "asset-path-noncanonical"
        if not row["path"].startswith(asset_root + "/"):
            return "asset-path-outside-root"
        if row["path"] == manifest_path:
            return "MANIFEST_SELF_LISTED"
        if row["role"] not in ROLES:
            return "asset-role"
        if isinstance(row["bytes"], bool) or not isinstance(row["bytes"], int) or row["bytes"] < 0:
            return "asset-bytes"
        if not (isinstance(row["sha256"], str) and len(row["sha256"]) == 64
                and all(c in "0123456789abcdef" for c in row["sha256"])):
            return "asset-digest-shape"
        seen.append(row["path"])
    if len(set(seen)) != len(seen):
        return "asset-path-duplicate"
    if seen != sorted(seen):
        return "assets-unsorted"
    return None


def build_release_tree(root, assets, manifest_rel, asset_root, projection_digests):
    """Write real files, emit the manifest excluding itself, return the pin."""
    for rel, payload in assets.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
    rows = []
    for rel, payload in sorted(assets.items()):
        role = ("notice" if rel.endswith(".txt")
                else "style" if rel.endswith(".css") else "script")
        rows.append({"path": rel, "sha256": hashlib.sha256(payload).hexdigest(),
                     "bytes": len(payload), "role": role})
    document = {"schemaVersion": 1,
                "projectionSchemaSha256s": sorted(projection_digests),
                "assets": rows}
    raw = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    manifest_file = root / manifest_rel
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    manifest_file.write_bytes(raw)
    return {"schemaVersion": 1, "assetRoot": asset_root,
            "assetManifestPath": manifest_rel,
            "assetManifestSha256": hashlib.sha256(raw).hexdigest(),
            "assetManifestBytes": len(raw), "buildChannel": "release"}


def check_completeness(root, document, pin):
    """Every regular file under assetRoot except exactly the pinned manifest."""
    listed = {row["path"] for row in document["assets"]}
    present = set()
    base = root / pin["assetRoot"]
    for dirpath, _dirnames, filenames in os.walk(base):
        for name in filenames:
            full = Path(dirpath) / name
            if full.is_symlink():
                return "SYMLINK_UNDER_ASSET_ROOT"
            present.add(str(full.relative_to(root)))
    excluded = {pin["assetManifestPath"]}
    extra = present - listed - excluded
    if extra:
        return "EXTRA_UNLISTED_FILE:" + sorted(extra)[0]
    missing = listed - present
    if missing:
        return "LISTED_FILE_ABSENT:" + sorted(missing)[0]
    return None


def load_path(root, pin, selected_projection=None):
    """Modelled load: locate, length-bound, digest, parse, completeness, members."""
    manifest_file = root / pin["assetManifestPath"]
    if not manifest_file.is_file() or manifest_file.is_symlink():
        return "manifest-not-a-regular-file"
    if not pin["assetManifestPath"].startswith(pin["assetRoot"] + "/"):
        return "manifest-outside-asset-root"
    raw = manifest_file.read_bytes()
    if len(raw) != pin["assetManifestBytes"]:
        return "manifest-length-mismatch"
    if hashlib.sha256(raw).hexdigest() != pin["assetManifestSha256"]:
        return "manifest-digest-mismatch"
    try:
        document = json.loads(raw)
    except ValueError:
        return "manifest-unparseable"
    refusal = admit_manifest(document, pin["assetRoot"], pin["assetManifestPath"])
    if refusal:
        return refusal
    refusal = check_completeness(root, document, pin)
    if refusal:
        return refusal
    if selected_projection is not None and \
            selected_projection not in document["projectionSchemaSha256s"]:
        return "projection-incompatible"
    for row in document["assets"]:
        member = root / row["path"]
        if not member.is_file() or member.is_symlink():
            return "member-not-a-regular-file:" + row["path"]
        payload = member.read_bytes()
        if len(payload) != row["bytes"]:
            return "member-length-mismatch:" + row["path"]
        if hashlib.sha256(payload).hexdigest() != row["sha256"]:
            return "member-digest-mismatch:" + row["path"]
    return None


# --- fixture ----------------------------------------------------------------

PROJECTION = hashlib.sha256(b"report-projection-schema-v1").hexdigest()
ASSETS = {
    "report/app.js": b"console.log('offline');\n",
    "report/style.css": b"body{margin:0}\n",
    "report/NOTICE.txt": b"third party notices\n",
}
ASSET_ROOT = "report"
MANIFEST_REL = "report/asset-manifest.json"


def fresh(tmp):
    root = Path(tempfile.mkdtemp(dir=tmp))
    pin = build_release_tree(root, dict(ASSETS), MANIFEST_REL, ASSET_ROOT, [PROJECTION])
    return root, pin


def main():
    results = []
    failures = []

    def case(name, expected, mutate=None, projection=PROJECTION):
        with tempfile.TemporaryDirectory() as tmp:
            root, pin = fresh(tmp)
            if mutate is not None:
                pin = mutate(root, pin) or pin
            actual = load_path(root, pin, projection)
            ok = (actual == expected) if isinstance(expected, str) or expected is None \
                else bool(actual and actual.startswith(expected[0]))
            results.append({"case": name, "expected": expected, "actual": actual, "ok": ok})
            if not ok:
                failures.append(name + ": expected " + str(expected) + ", got " + str(actual))

    def mutate_manifest_bytes(root, pin):
        target = root / pin["assetManifestPath"]
        raw = bytearray(target.read_bytes())
        raw[-2] = raw[-2] ^ 0x20
        target.write_bytes(bytes(raw))

    def truncate_manifest(root, pin):
        target = root / pin["assetManifestPath"]
        target.write_bytes(target.read_bytes()[:-1])

    def mutate_member(root, pin):
        target = root / "report/app.js"
        target.write_bytes(b"console.log('tampered and longer');\n")

    def mutate_member_same_length(root, pin):
        target = root / "report/app.js"
        raw = bytearray(target.read_bytes())
        raw[8] = raw[8] ^ 0x20
        target.write_bytes(bytes(raw))

    def extra_file(root, pin):
        (root / "report/extra.js").write_bytes(b"// not listed\n")

    def remove_member(root, pin):
        (root / "report/style.css").unlink()

    def self_list(root, pin):
        target = root / pin["assetManifestPath"]
        document = json.loads(target.read_bytes())
        document["assets"].append({"path": pin["assetManifestPath"],
                                   "sha256": "0" * 64, "bytes": 1, "role": "script"})
        document["assets"].sort(key=lambda r: r["path"])
        raw = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
        target.write_bytes(raw)
        pin = dict(pin)
        pin["assetManifestSha256"] = hashlib.sha256(raw).hexdigest()
        pin["assetManifestBytes"] = len(raw)
        return pin

    def wrong_root(root, pin):
        pin = dict(pin)
        pin["assetRoot"] = "assets"
        return pin

    def manifest_outside_root(root, pin):
        moved = root / "asset-manifest.json"
        shutil.move(str(root / pin["assetManifestPath"]), str(moved))
        pin = dict(pin)
        pin["assetManifestPath"] = "asset-manifest.json"
        return pin

    def symlinked_member(root, pin):
        target = root / "report/app.js"
        payload = target.read_bytes()
        outside = root / "outside.js"
        outside.write_bytes(payload)
        target.unlink()
        try:
            target.symlink_to(outside)
        except OSError:
            target.write_bytes(payload)
            return None
        return None

    case("accepts-a-well-formed-release-tree", None)
    case("rejects-a-mutated-manifest-byte", "manifest-digest-mismatch", mutate_manifest_bytes)
    case("rejects-a-truncated-manifest", "manifest-length-mismatch", truncate_manifest)
    case("rejects-a-mutated-member", ("member-length-mismatch",), mutate_member)
    case("rejects-an-equal-length-mutated-member", ("member-digest-mismatch",),
         mutate_member_same_length)
    case("rejects-an-extra-unlisted-file", ("EXTRA_UNLISTED_FILE",), extra_file)
    case("rejects-a-listed-file-that-is-absent", ("LISTED_FILE_ABSENT",), remove_member)
    case("rejects-a-self-listed-manifest", "MANIFEST_SELF_LISTED", self_list)
    case("rejects-a-wrong-asset-root", "manifest-outside-asset-root", wrong_root)
    case("rejects-a-manifest-outside-the-asset-root", "manifest-outside-asset-root",
         manifest_outside_root)
    case("rejects-a-symlinked-member", ("SYMLINK_UNDER_ASSET_ROOT",), symlinked_member)
    case("rejects-an-unsupported-projection", "projection-incompatible",
         None, hashlib.sha256(b"other-projection").hexdigest())

    with tempfile.TemporaryDirectory() as tmp:
        root, pin = fresh(tmp)
        document = json.loads((root / pin["assetManifestPath"]).read_bytes())
        listed = {row["path"] for row in document["assets"]}
        coverage = {
            "assetRootFilesOnDisk": sorted(
                str((Path(d) / n).relative_to(root))
                for d, _s, f in os.walk(root / ASSET_ROOT) for n in f),
            "listedMembers": sorted(listed),
            "pinnedManifestPath": pin["assetManifestPath"],
            "manifestIsListed": pin["assetManifestPath"] in listed,
            "everyFileCoveredOnceByRowOrPin":
                sorted(listed | {pin["assetManifestPath"]}) ==
                sorted(str(Path(d).relative_to(root) / n)
                       for d, _s, f in os.walk(root / ASSET_ROOT) for n in f),
        }

    result = {
        "control": "check_report_asset_fixture",
        "fixture": "real temporary release tree, built then read back",
        "cases": {"count": len(results), "passed": sum(1 for r in results if r["ok"]),
                  "failed": [r for r in results if not r["ok"]], "detail": results},
        "coverageProof": coverage,
        "failures": failures,
        "status": "PASS" if not failures and coverage["everyFileCoveredOnceByRowOrPin"]
                  and not coverage["manifestIsListed"] else "FAIL",
        "limits": "Temporary-filesystem design evidence. Not product code, not a release "
                  "build, not a browser or parity test, and no qualification claim.",
    }
    print(json.dumps(result, indent=1))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
