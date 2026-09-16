#!/usr/bin/env python3
"""Independent exact-tree verifier (review-03). lstat only, never follows symlinks.
Checks every manifest row (file/directory/symlink: type, octal mode, bytes, sha256,
symlink target), reports unexpected extra entries, and hashes extra pinned files
(e.g. the Node binary) given as --pin PATH.

usage: verify-tree.py MANIFEST ROOT OUT.json [--ignore-prefix P]... [--pin PATH]...
"""
import hashlib, json, os, stat, sys

manifest_path, root, out = sys.argv[1:4]
rest = sys.argv[4:]
ignore = [rest[i + 1] for i, a in enumerate(rest) if a == "--ignore-prefix"]
pins = [rest[i + 1] for i, a in enumerate(rest) if a == "--pin"]
rows = json.load(open(manifest_path))["files"]
expected = {r["path"]: r for r in rows}

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def describe(full):
    st = os.lstat(full)
    e = {"mode": format(stat.S_IMODE(st.st_mode), "o")}
    if stat.S_ISLNK(st.st_mode):
        e.update(type="symlink", target=os.readlink(full))
    elif stat.S_ISDIR(st.st_mode):
        e["type"] = "directory"
    elif stat.S_ISREG(st.st_mode):
        e.update(type="file", bytes=st.st_size, sha256=sha(full))
    else:
        e["type"] = "other"
    return e

actual = {}
for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
    for name in dirnames + filenames:
        full = os.path.join(dirpath, name)
        actual[os.path.relpath(full, root)] = describe(full)

problems = []
for p, r in expected.items():
    a = actual.get(p)
    if a is None:
        problems.append({"path": p, "problem": "missing"}); continue
    for k in ("type", "mode", "bytes", "sha256", "target"):
        if k in r and r[k] != a.get(k):
            problems.append({"path": p, "problem": k, "expected": r[k], "actual": a.get(k)})
    for k in ("sha256", "bytes", "target"):
        if k in a and k not in r:
            problems.append({"path": p, "problem": "unrecorded-" + k, "actual": a[k]})
for p in sorted(actual):
    if p not in expected and not any(p == i.rstrip("/") or p.startswith(i) for i in ignore):
        problems.append({"path": p, "problem": "unexpected", "actual": actual[p]})

pinned = {}
for p in pins:
    real = os.path.realpath(p)
    st = os.stat(real)
    pinned[p] = {"realpath": real, "bytes": st.st_size, "mode": format(stat.S_IMODE(st.st_mode), "o"), "sha256": sha(real),
                 "lstat": describe(p)}
types = {}
for a in actual.values():
    types[a["type"]] = types.get(a["type"], 0) + 1
summary = {"root": root, "manifestRows": len(rows), "actualEntries": len(actual), "types": types,
           "fileBytes": sum(a.get("bytes", 0) for a in actual.values()), "problems": problems,
           "treeDigest": hashlib.sha256(json.dumps(actual, sort_keys=True).encode()).hexdigest(), "pinned": pinned}
json.dump({"summary": summary, "actual": actual}, open(out, "w"), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in summary.items() if k != "problems"}, indent=1))
print("problems:", len(problems))
for p in problems[:25]:
    print(" ", json.dumps(p)[:300])
