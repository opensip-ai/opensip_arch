#!/usr/bin/env python3
"""P00: full custody verification of the frozen subject against its manifest.

Checks every declared file's sha256 + byte length, and enumerates any
undeclared file present in the snapshot root. Read-only.
"""
import hashlib, json, os, sys

MANIFEST = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v8.json"
REQUIRED = "cafcd839d44228677c74f5a4baed22d4fa7f384ada542fbbe8c4e74ef3e62d70"
ROOT = "/tmp/opensip-design-corrections/candidate-subject.v8"


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    man_bytes = open(MANIFEST, "rb").read()
    man_sha = hashlib.sha256(man_bytes).hexdigest()
    out = {
        "manifestSha256": man_sha,
        "manifestShaMatchesRequired": man_sha == REQUIRED,
        "declaredFileCount": None,
        "declaredTotalBytes": None,
        "verifiedOk": 0,
        "hashMismatch": [],
        "lengthMismatch": [],
        "missing": [],
        "undeclared": [],
        "observedTotalBytes": 0,
    }
    m = json.loads(man_bytes)
    out["declaredFileCount"] = m["fileCount"]
    out["declaredTotalBytes"] = m["totalBytes"]
    out["snapshotRootMatches"] = m["snapshotRoot"] == ROOT
    out["standing"] = m["standing"]

    declared = {}
    for e in m["files"]:
        declared[e["path"]] = (e["sha256"], e["bytes"])
    out["declaredUniquePaths"] = len(declared)
    out["declaredListLen"] = len(m["files"])

    for rel, (want_sha, want_len) in sorted(declared.items()):
        ap = os.path.join(ROOT, rel)
        if not os.path.isfile(ap):
            out["missing"].append(rel)
            continue
        got_len = os.path.getsize(ap)
        got_sha = sha256_file(ap)
        out["observedTotalBytes"] += got_len
        if got_len != want_len:
            out["lengthMismatch"].append({"path": rel, "want": want_len, "got": got_len})
        if got_sha != want_sha:
            out["hashMismatch"].append({"path": rel, "want": want_sha, "got": got_sha})
        if got_len == want_len and got_sha == want_sha:
            out["verifiedOk"] += 1

    for dirpath, _dirnames, filenames in os.walk(ROOT):
        for fn in filenames:
            ap = os.path.join(dirpath, fn)
            rel = os.path.relpath(ap, ROOT)
            if rel not in declared:
                out["undeclared"].append({"path": rel, "bytes": os.path.getsize(ap),
                                          "sha256": sha256_file(ap)})

    out["totalBytesMatch"] = out["observedTotalBytes"] == out["declaredTotalBytes"]
    out["CUSTODY_CLEAN"] = (
        out["manifestShaMatchesRequired"]
        and not out["hashMismatch"] and not out["lengthMismatch"]
        and not out["missing"] and not out["undeclared"]
        and out["verifiedOk"] == out["declaredFileCount"]
        and out["totalBytesMatch"]
    )
    json.dump(out, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
