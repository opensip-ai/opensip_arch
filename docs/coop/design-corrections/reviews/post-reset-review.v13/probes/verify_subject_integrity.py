#!/usr/bin/env python
"""Independent subject integrity verification for candidate-subject.v13.

Authored fresh for this review. Verifies, for the frozen subject tree:
  * every declared file exists, with exact declared sha256 and byte length
  * no undeclared files exist anywhere under the snapshot root
  * declared aggregate fileCount/totalBytes agree with recomputed values

Usage: verify_subject_integrity.py <manifest.json> <phase-label> <out.json>
"""
import hashlib
import json
import os
import sys


def sha256_and_len(path):
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            n += len(chunk)
            h.update(chunk)
    return h.hexdigest(), n


def main():
    manifest_path, phase, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    raw = open(manifest_path, "rb").read()
    manifest_sha = hashlib.sha256(raw).hexdigest()
    manifest = json.loads(raw)
    root = manifest["snapshotRoot"]

    declared = {}
    for entry in manifest["files"]:
        declared[entry["path"]] = entry

    missing, hash_mismatch, len_mismatch = [], [], []
    total_bytes = 0
    for rel, entry in sorted(declared.items()):
        full = os.path.join(root, rel)
        if not os.path.isfile(full):
            missing.append(rel)
            continue
        actual_sha, actual_len = sha256_and_len(full)
        total_bytes += actual_len
        want_sha = entry.get("sha256")
        want_len = entry.get("bytes", entry.get("length"))
        if want_sha is not None and actual_sha != want_sha:
            hash_mismatch.append(
                {"path": rel, "declared": want_sha, "actual": actual_sha}
            )
        if want_len is not None and actual_len != want_len:
            len_mismatch.append(
                {"path": rel, "declared": want_len, "actual": actual_len}
            )

    # Undeclared-file inventory: walk the entire snapshot root.
    on_disk = set()
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            on_disk.add(os.path.relpath(full, root))
    undeclared = sorted(on_disk - set(declared))

    # Symlinks are a distinct custody concern: a symlink can point outside the
    # frozen tree and would not be covered by content hashing.
    symlinks = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in list(dirnames) + list(filenames):
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                symlinks.append(
                    {
                        "path": os.path.relpath(full, root),
                        "target": os.readlink(full),
                    }
                )

    result = {
        "phase": phase,
        "manifestPath": manifest_path,
        "manifestSha256": manifest_sha,
        "snapshotRoot": root,
        "declaredFileCount": manifest.get("fileCount"),
        "declaredTotalBytes": manifest.get("totalBytes"),
        "declaredEntries": len(declared),
        "recomputedTotalBytes": total_bytes,
        "missingCount": len(missing),
        "missing": missing[:50],
        "hashMismatchCount": len(hash_mismatch),
        "hashMismatch": hash_mismatch[:50],
        "lengthMismatchCount": len(len_mismatch),
        "lengthMismatch": len_mismatch[:50],
        "undeclaredCount": len(undeclared),
        "undeclared": undeclared[:200],
        "symlinkCount": len(symlinks),
        "symlinks": symlinks[:50],
        "fileCountAgrees": manifest.get("fileCount") == len(declared) == len(on_disk),
        "totalBytesAgrees": manifest.get("totalBytes") == total_bytes,
    }
    result["clean"] = (
        not missing
        and not hash_mismatch
        and not len_mismatch
        and not undeclared
        and result["fileCountAgrees"]
        and result["totalBytesAgrees"]
    )
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("missing", "hashMismatch", "lengthMismatch",
                                   "undeclared", "symlinks")}, indent=2))
    return 0 if result["clean"] else 1


if __name__ == "__main__":
    sys.exit(main())
