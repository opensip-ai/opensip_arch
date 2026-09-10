#!/usr/bin/env python3
"""p01: full custody verification of the frozen v11 subject.

Verifies EVERY declared file's sha256 and byte length, and inventories any
undeclared file present under the snapshot root. Run before and after all
other probe work.
"""
import hashlib
import json
import os
import sys

MANIFEST = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v11.json"
EXPECT_MANIFEST_SHA = "a03b7fe987ee886101a6d5b85bf4b0760f59b06a5a9e9c5f627accb9a7263bdf"
EXPECT_PRED_SHA = "82c1be11d3b61908b2a45ebb6e59e71bb5cb31d8450a96a61857ced430e786fd"


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(phase):
    raw = open(MANIFEST, "rb").read()
    man_sha = hashlib.sha256(raw).hexdigest()
    m = json.loads(raw)
    root = m["snapshotRoot"]

    out = {
        "phase": phase,
        "manifestSha256": man_sha,
        "manifestShaMatches": man_sha == EXPECT_MANIFEST_SHA,
        "predecessorManifestSha256": m.get("predecessorManifestSha256"),
        "predecessorShaMatches": m.get("predecessorManifestSha256") == EXPECT_PRED_SHA,
        "snapshotRoot": root,
        "declaredFileCount": m["fileCount"],
        "declaredTotalBytes": m["totalBytes"],
    }

    declared = {}
    for e in m["files"]:
        declared[e["path"]] = (e["sha256"], e["bytes"])
    out["manifestEntryCount"] = len(m["files"])
    out["manifestPathsUnique"] = len(declared) == len(m["files"])

    missing, digest_mismatch, length_mismatch = [], [], []
    total = 0
    for path, (sha, nbytes) in sorted(declared.items()):
        full = os.path.join(root, path)
        if not os.path.isfile(full):
            missing.append(path)
            continue
        st = os.stat(full)
        if st.st_size != nbytes:
            length_mismatch.append(
                {"path": path, "declared": nbytes, "actual": st.st_size})
        actual = sha256_file(full)
        if actual != sha:
            digest_mismatch.append(
                {"path": path, "declared": sha, "actual": actual})
        total += st.st_size

    # undeclared inventory: every real path under root not in the manifest
    undeclared = []
    symlinks = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if os.path.islink(full):
                symlinks.append(rel)
            if rel not in declared:
                undeclared.append(rel)
        for name in dirnames:
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                symlinks.append(os.path.relpath(full, root) + "/")

    out.update({
        "verifiedCount": len(declared) - len(missing),
        "observedTotalBytes": total,
        "totalBytesMatches": total == m["totalBytes"],
        "missing": missing,
        "digestMismatch": digest_mismatch,
        "lengthMismatch": length_mismatch,
        "undeclared": sorted(undeclared),
        "undeclaredCount": len(undeclared),
        "symlinks": sorted(symlinks),
    })
    out["CUSTODY_INTACT"] = (
        out["manifestShaMatches"]
        and out["predecessorShaMatches"]
        and not missing
        and not digest_mismatch
        and not length_mismatch
        and not undeclared
        and not symlinks
        and out["totalBytesMatches"]
        and out["manifestPathsUnique"]
    )
    print(json.dumps(out, indent=2))
    return 0 if out["CUSTODY_INTACT"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "pre"))
