#!/usr/bin/env python3
"""Independent subject custody verifier (pre- and post-review).

Verifies, against the frozen manifest:
  1. manifest file SHA256 itself
  2. every declared file's SHA256 and byte length
  3. undeclared-file inventory (anything present under the snapshot root
     that the manifest does not declare)
  4. declared-but-missing files

Read-only with respect to the subject and the original repository.
"""
import hashlib
import json
import os
import sys

MANIFEST = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v15.json"
EXPECTED_MANIFEST_SHA = "5ec7928426c7a91e323240337dc382c4de32bd4e5f2626eba92c8991067b365f"
SUBJECT = "/tmp/opensip-design-corrections/candidate-subject.v15"


def sha256_and_len(path):
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as fh:
        while True:
            b = fh.read(1 << 20)
            if not b:
                break
            h.update(b)
            n += len(b)
    return h.hexdigest(), n


def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "unspecified"
    out = {"phase": phase}

    msha, mlen = sha256_and_len(MANIFEST)
    out["manifestSha256"] = msha
    out["manifestBytes"] = mlen
    out["manifestShaMatchesExpected"] = (msha == EXPECTED_MANIFEST_SHA)
    if not out["manifestShaMatchesExpected"]:
        out["fatal"] = "manifest sha mismatch"
        print(json.dumps(out, indent=2))
        return 2

    man = json.load(open(MANIFEST))
    files = man["files"]
    out["declaredFileCount"] = len(files)
    out["manifestFileCountField"] = man.get("fileCount")
    out["manifestTotalBytesField"] = man.get("totalBytes")
    out["snapshotRoot"] = man.get("snapshotRoot")

    # Normalise the declared-entry shape without assuming key names.
    sample = files[0] if isinstance(files, list) else None
    out["declaredEntryKeys"] = sorted(sample.keys()) if isinstance(sample, dict) else None

    mismatches = []
    missing = []
    declared_paths = set()
    total_declared_bytes = 0

    entries = files if isinstance(files, list) else [
        dict(v, path=k) for k, v in files.items()
    ]

    for e in entries:
        rel = e.get("path") or e.get("relativePath") or e.get("file")
        exp_sha = e.get("sha256") or e.get("sha256Hex") or e.get("hash")
        exp_len = e.get("bytes")
        if exp_len is None:
            exp_len = e.get("length", e.get("size"))
        declared_paths.add(rel)
        if isinstance(exp_len, int):
            total_declared_bytes += exp_len
        full = os.path.join(SUBJECT, rel)
        if not os.path.isfile(full):
            missing.append(rel)
            continue
        got_sha, got_len = sha256_and_len(full)
        if got_sha != exp_sha or (exp_len is not None and got_len != exp_len):
            mismatches.append({
                "path": rel,
                "expectedSha256": exp_sha, "actualSha256": got_sha,
                "expectedBytes": exp_len, "actualBytes": got_len,
            })

    out["declaredBytesSum"] = total_declared_bytes
    out["hashMismatchCount"] = len(mismatches)
    out["hashMismatches"] = mismatches[:25]
    out["declaredButMissingCount"] = len(missing)
    out["declaredButMissing"] = missing[:25]

    # Undeclared inventory
    present = set()
    for dirpath, dirnames, filenames in os.walk(SUBJECT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fn in filenames:
            present.add(os.path.relpath(os.path.join(dirpath, fn), SUBJECT))
    undeclared = sorted(present - declared_paths)
    out["presentFileCount"] = len(present)
    out["undeclaredFileCount"] = len(undeclared)
    out["undeclaredFiles"] = undeclared[:50]

    out["CLEAN"] = (
        out["manifestShaMatchesExpected"]
        and not mismatches and not missing and not undeclared
        and len(present) == len(declared_paths)
    )
    print(json.dumps(out, indent=2))
    return 0 if out["CLEAN"] else 1


if __name__ == "__main__":
    sys.exit(main())
