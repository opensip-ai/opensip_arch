#!/usr/bin/env python
"""Independent verification of the frozen v17 subject against its manifest.

Checks, for every declared file: existence, byte length, SHA256.
Also walks the snapshot root to find UNDECLARED inventory (files present on
disk but absent from the manifest) and any non-regular-file entries.

Writes a JSON report to the path given as argv[1].
"""
import hashlib
import json
import os
import sys

MANIFEST = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v17.json"
DECLARED_MANIFEST_SHA = "8cfe6d20a7d49b819f7c2eb2578afcaa5037048ed290ff1867fdcd6789cf3a9c"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    out_path = sys.argv[1]

    with open(MANIFEST, "rb") as fh:
        raw = fh.read()
    manifest_sha = hashlib.sha256(raw).hexdigest()
    m = json.loads(raw)
    root = m["snapshotRoot"]

    report = {
        "manifestPath": MANIFEST,
        "manifestSha256": manifest_sha,
        "manifestShaMatchesDeclared": manifest_sha == DECLARED_MANIFEST_SHA,
        "manifestBytes": len(raw),
        "snapshotRoot": root,
        "declaredFileCount": m["fileCount"],
        "declaredTotalBytes": m["totalBytes"],
        "filesListLength": len(m["files"]),
    }

    missing = []
    size_mismatch = []
    hash_mismatch = []
    ok = 0
    total_bytes = 0
    declared_paths = set()
    dup_paths = []

    for entry in m["files"]:
        p = entry["path"]
        if p in declared_paths:
            dup_paths.append(p)
        declared_paths.add(p)
        full = os.path.join(root, p)
        if not os.path.isfile(full):
            missing.append(p)
            continue
        st = os.stat(full)
        if st.st_size != entry["bytes"]:
            size_mismatch.append(
                {"path": p, "declared": entry["bytes"], "actual": st.st_size}
            )
            continue
        actual = sha256_file(full)
        if actual != entry["sha256"]:
            hash_mismatch.append(
                {"path": p, "declared": entry["sha256"], "actual": actual}
            )
            continue
        ok += 1
        total_bytes += st.st_size

    # Undeclared inventory walk
    undeclared = []
    symlinks = []
    empty_dirs = []
    on_disk_count = 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        if not dirnames and not filenames:
            empty_dirs.append(os.path.relpath(dirpath, root))
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            on_disk_count += 1
            if os.path.islink(full):
                symlinks.append(rel)
            if rel not in declared_paths:
                try:
                    sz = os.stat(full).st_size
                except OSError:
                    sz = None
                undeclared.append({"path": rel, "bytes": sz})

    report.update(
        {
            "verifiedOk": ok,
            "missing": missing,
            "missingCount": len(missing),
            "sizeMismatch": size_mismatch,
            "sizeMismatchCount": len(size_mismatch),
            "hashMismatch": hash_mismatch,
            "hashMismatchCount": len(hash_mismatch),
            "duplicateDeclaredPaths": dup_paths,
            "sumVerifiedBytes": total_bytes,
            "totalBytesMatchesDeclared": total_bytes == m["totalBytes"],
            "onDiskFileCount": on_disk_count,
            "undeclaredCount": len(undeclared),
            "undeclared": undeclared[:500],
            "symlinkCount": len(symlinks),
            "symlinks": symlinks[:200],
            "emptyDirCount": len(empty_dirs),
            "emptyDirs": empty_dirs[:200],
        }
    )
    report["allDeclaredFilesIntact"] = (
        not missing and not size_mismatch and not hash_mismatch and ok == len(m["files"])
    )

    with open(out_path, "w") as fh:
        json.dump(report, fh, indent=1, sort_keys=True)

    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("undeclared", "symlinks", "emptyDirs",
                                   "missing", "sizeMismatch", "hashMismatch")},
                     indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
