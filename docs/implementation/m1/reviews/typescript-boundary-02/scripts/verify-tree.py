#!/usr/bin/env python3
"""Independent tree verifier: walks a root with lstat (no symlink following) and
compares every entry against the outer manifest's rows. Writes a snapshot JSON.

usage: verify-tree.py MANIFEST ROOT OUT.json [--ignore-prefix P ...]
"""
import hashlib, json, os, stat, sys

manifest_path, root, out = sys.argv[1], sys.argv[2], sys.argv[3]
ignore = [a for a in sys.argv[4:] if a != "--ignore-prefix"]
rows = json.load(open(manifest_path))["files"]
expected = {r["path"]: r for r in rows}

actual = {}
for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
    for name in sorted(dirnames + filenames):
        full = os.path.join(dirpath, name)
        rel = os.path.relpath(full, root)
        st = os.lstat(full)
        if stat.S_ISDIR(st.st_mode):
            continue
        entry = {"mode": format(stat.S_IMODE(st.st_mode), "o")}
        if stat.S_ISLNK(st.st_mode):
            entry["type"] = "symlink"
            entry["target"] = os.readlink(full)
        elif stat.S_ISREG(st.st_mode):
            entry["type"] = "file"
            entry["bytes"] = st.st_size
            h = hashlib.sha256()
            with open(full, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            entry["sha256"] = h.hexdigest()
        else:
            entry["type"] = "other"
        actual[rel] = entry

def ignored(p):
    return any(p.startswith(i) for i in ignore)

problems = []
for p, r in expected.items():
    a = actual.get(p)
    if a is None:
        problems.append({"path": p, "problem": "missing"})
        continue
    for k in ("type", "mode", "bytes", "sha256", "target"):
        if k in r and r[k] != a.get(k):
            problems.append({"path": p, "problem": k, "expected": r[k], "actual": a.get(k)})
    if a["type"] == "symlink" and "target" not in r:
        problems.append({"path": p, "problem": "symlink-without-recorded-target", "actual": a.get("target")})
extra = sorted(p for p in actual if p not in expected and not ignored(p))
for p in extra:
    problems.append({"path": p, "problem": "unexpected", "actual": actual[p]})

# empty directories are invisible to a file manifest; record them separately
empty_dirs = []
for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
    if not dirnames and not filenames:
        empty_dirs.append(os.path.relpath(dirpath, root))

tree_digest = hashlib.sha256(json.dumps(actual, sort_keys=True).encode()).hexdigest()
summary = {
    "root": root,
    "manifestRows": len(rows),
    "actualEntries": len(actual),
    "types": {t: sum(1 for a in actual.values() if a["type"] == t) for t in ("file", "symlink", "other")},
    "totalBytes": sum(a.get("bytes", 0) for a in actual.values()),
    "problems": problems,
    "emptyDirs": empty_dirs,
    "actualTreeDigest": tree_digest,
}
json.dump({"summary": summary, "actual": actual}, open(out, "w"), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in summary.items() if k != "problems"}, indent=1))
print("problems:", len(problems))
for p in problems[:30]:
    print(" ", p)
