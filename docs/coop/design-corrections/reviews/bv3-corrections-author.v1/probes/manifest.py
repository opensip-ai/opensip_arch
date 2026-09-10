#!/usr/bin/env python3
"""Compute a deterministic per-file + aggregate manifest for a tree.

Used to (a) prove the working copy still matches frozen v12 at baseline and
(b) account for every changed/added/deleted byte in the released delta.
"""
import hashlib
import json
import os
import sys


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build(root):
    entries = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            if os.path.islink(full) or not os.path.isfile(full):
                continue
            rel = os.path.relpath(full, root)
            entries[rel] = {
                "sha256": file_sha256(full),
                "bytes": os.path.getsize(full),
            }
    agg = hashlib.sha256()
    for rel in sorted(entries):
        agg.update(rel.encode("utf-8"))
        agg.update(b"\0")
        agg.update(entries[rel]["sha256"].encode("ascii"))
        agg.update(b"\n")
    return {
        "root": os.path.abspath(root),
        "fileCount": len(entries),
        "manifestSha256": agg.hexdigest(),
        "files": entries,
    }


if __name__ == "__main__":
    out = build(sys.argv[1])
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w") as fh:
            json.dump(out, fh, indent=2, sort_keys=True)
    print(json.dumps({k: out[k] for k in ("root", "fileCount", "manifestSha256")}, indent=2))
