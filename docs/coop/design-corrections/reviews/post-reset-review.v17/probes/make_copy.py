#!/usr/bin/env python
"""Make a named disposable FULL exact copy of the frozen v17 subject and record
custody for it. Never touches the frozen snapshot or the live repo.

usage: make_copy.py <copy-name>
"""
import hashlib
import json
import os
import shutil
import sys

REV = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews"
SRC = "/tmp/opensip-design-corrections/candidate-subject.v17"
BASE = "/tmp/opensip-design-corrections/post-reset-review.v17/copies"


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    name = sys.argv[1]
    dst = os.path.join(BASE, name)
    if os.path.exists(dst):
        print("EXISTS, refusing to overwrite:", dst)
        sys.exit(2)
    shutil.copytree(SRC, dst, symlinks=True)

    with open(os.path.join(REV, "candidate-subject.v17.json"), "rb") as fh:
        m = json.loads(fh.read())

    bad = []
    ok = 0
    declared = set()
    for e in m["files"]:
        declared.add(e["path"])
        full = os.path.join(dst, e["path"])
        if not os.path.isfile(full):
            bad.append({"path": e["path"], "problem": "missing"})
            continue
        if os.stat(full).st_size != e["bytes"]:
            bad.append({"path": e["path"], "problem": "length"})
            continue
        if sha_file(full) != e["sha256"]:
            bad.append({"path": e["path"], "problem": "sha"})
            continue
        ok += 1

    extra = []
    for dp, _, fns in os.walk(dst):
        for fn in fns:
            rel = os.path.relpath(os.path.join(dp, fn), dst)
            if rel not in declared:
                extra.append(rel)

    rec = {
        "copyName": name,
        "copyRoot": dst,
        "sourceSnapshot": SRC,
        "baseManifestSha256":
            "8cfe6d20a7d49b819f7c2eb2578afcaa5037048ed290ff1867fdcd6789cf3a9c",
        "declared": len(m["files"]),
        "verifiedByteExact": ok,
        "problems": bad,
        "undeclaredInCopy": extra,
        "byteExactVsManifest": ok == len(m["files"]) and not bad and not extra,
        "phase": "post-copy-pre-execution",
    }
    out = os.path.join(BASE, name + ".custody.json")
    with open(out, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in rec.items()
                      if k not in ("problems", "undeclaredInCopy")},
                     indent=1, sort_keys=True))
    print("problems:", len(bad), "undeclared:", len(extra))


if __name__ == "__main__":
    main()
