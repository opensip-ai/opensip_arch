#!/usr/bin/env python3
"""Corrected tool-closure package summaries (review-03).

The author generator (harness/freeze-manifest.mjs closure()) receives a
.../node_modules root and then builds package prefixes as `${dir}/${key}` with
key = node_modules/<pkg>, i.e. .../node_modules/node_modules/<pkg>/, so every
package summary is files=0 with the empty-tree sha256. This script:

  1. reproduces the defect from the frozen outer-manifest rows (author prefix rule);
  2. recomputes membership with the correct prefix from the same rows, using the
     author's own digest line format, and asserts every package is nonempty;
  3. accounts for every closure entry (package member or named non-package extra);
  4. ties package file counts/bytes to the archived tarballs where acquired;
  5. cross-checks the rows against the actual frozen tree (lstat);
  6. runs drift controls on a scratch copy (byte flip, added file, removed package,
     mode change, symlink retarget) and requires each to change exactly the
     affected summary or fail the nonempty assertion.

Never writes the frozen subject or its manifest.
usage: closure-summaries.py SUBJECT OUTER_MANIFEST SCRATCH OUT.json
"""
import hashlib, io, json, os, shutil, stat, sys, tarfile

subject, outer_path, scratch, out = sys.argv[1:5]
sha = lambda b: hashlib.sha256(b).hexdigest()
EMPTY = sha(b"")
rows = json.load(open(outer_path))["files"]
author = json.load(open(os.path.join(subject, "freeze-manifest.json")))

npm_lock = json.load(open(os.path.join(subject, "baseline/subject-02-trial/package-lock.json")))["packages"]
CLOSURES = {
    "checker": ("checker/node_modules", {f"node_modules/{n}": npm_lock[f"node_modules/{n}"] for n in ["typescript", "enhanced-resolve", "graceful-fs", "tapable"]}),
    "baseline": ("baseline/subject-02-trial/node_modules", {k: v for k, v in npm_lock.items() if k}),
    "pnpmContractsLane": ("inputs/pnpm-provision-05/node_modules", {"node_modules/.pnpm/typescript@6.0.3/node_modules/typescript": {"version": "6.0.3"}}),
}

def line(r, base):
    return f"{r['type']}\0{r['path'][len(base):]}\0{r['mode']}\0{r.get('sha256') or r.get('target')}"

def summarize(entries, root, packages, prefix_rule):
    files = [r for r in entries if r["type"] != "directory" and r["path"].startswith(root + "/")]
    out_pk, member = [], {}
    for key, meta in packages.items():
        base = prefix_rule(root, key)
        tree = [r for r in files if r["path"].startswith(base) and "node_modules/" not in r["path"][len(base):]]
        for r in tree:
            member.setdefault(r["path"], []).append(key)
        out_pk.append({"package": key, "version": meta.get("version"), "prefix": base, "files": len(tree),
                       "bytes": sum(r.get("bytes", 0) for r in tree),
                       "treeSha256": sha("\n".join(line(r, base) for r in tree).encode())})
    return files, out_pk, member

author_rule = lambda root, key: f"{root}/{key.replace('node_modules/', 'node_modules/', 1)}/"   # as frozen: ${dir}/${key}/
fixed_rule = lambda root, key: f"{root}/{key[len('node_modules/'):]}/"

report = {"standing": "reviewer-corrected closure package summaries; frozen author manifest preserved unchanged", "closures": {}}
all_ok = True
for name, (root, packages) in CLOSURES.items():
    _, buggy, _ = summarize(rows, root, packages, author_rule)
    files, fixed, member = summarize(rows, root, packages, fixed_rule)
    declared = {p["package"]: p for p in author["toolClosures"][name]["packages"]}
    extras = sorted(p for p in (r["path"] for r in files) if p not in member)
    multi = sorted(p for p, ks in member.items() if len(ks) > 1)
    empty = [p["package"] for p in fixed if p["files"] == 0 or p["treeSha256"] == EMPTY]
    c = {
        "root": root, "closureEntriesNonDirectory": len(files),
        "authorDeclaredZeroFilePackages": sum(1 for p in declared.values() if p["files"] == 0 and p["treeSha256"] == EMPTY),
        "authorDeclaredPackages": len(declared),
        "defectReproducedFromRows": all(p["files"] == 0 and p["treeSha256"] == EMPTY for p in buggy)
                                    and all(declared[p["package"]]["treeSha256"] == p["treeSha256"] for p in buggy),
        "authorPrefixExample": buggy[0]["prefix"], "correctedPrefixExample": fixed[0]["prefix"],
        "correctedNonemptyAll": not empty, "correctedEmptyPackages": empty,
        "entriesInMoreThanOnePackage": multi,
        "nonPackageEntries": extras,
        "accounting": {"packageMembers": len(member), "nonPackage": len(extras), "total": len(files), "balanced": len(member) + len(extras) == len(files)},
        "packages": fixed,
    }
    all_ok &= c["correctedNonemptyAll"] and not multi and c["accounting"]["balanced"]
    report["closures"][name] = c

# archive ties
arch_dir = os.path.join(subject, "provenance/archives")
ties = {}
for arc in sorted(a for a in os.listdir(arch_dir) if a.endswith(".tgz")):
    pkg = arc.rsplit("-", 1)[0]
    t = tarfile.open(fileobj=io.BytesIO(open(os.path.join(arch_dir, arc), "rb").read()))
    members = {m.name.split("/", 1)[1]: m.size for m in t.getmembers() if m.isfile()}
    for name, c in report["closures"].items():
        for p in c["packages"]:
            if p["package"].endswith("/" + pkg):
                ok = p["files"] == len(members) and p["bytes"] == sum(members.values())
                ties.setdefault(arc, {})[name] = {"packageFiles": p["files"], "archiveFiles": len(members), "packageBytes": p["bytes"], "archiveBytes": sum(members.values()), "match": ok}
                all_ok &= ok
report["archiveTies"] = ties

# rows vs actual tree for every closure entry
def actual_row(rel):
    full = os.path.join(subject, rel)
    st = os.lstat(full)
    r = {"path": rel, "mode": format(stat.S_IMODE(st.st_mode), "o")}
    if stat.S_ISLNK(st.st_mode): r.update(type="symlink", target=os.readlink(full))
    elif stat.S_ISDIR(st.st_mode): r["type"] = "directory"
    else: r.update(type="file", bytes=st.st_size, sha256=sha(open(full, "rb").read()))
    return r
mism = []
for name, (root, _) in CLOSURES.items():
    for r in rows:
        if r["path"] == root or r["path"].startswith(root + "/"):
            a = actual_row(r["path"])
            if {k: v for k, v in r.items() if k != "group"} != a:
                mism.append(r["path"])
report["rowsMatchActualTree"] = {"mismatches": mism[:20], "count": len(mism)}
all_ok &= not mism

# drift controls on a scratch copy of the checker closure
def tree_rows(base_dir, rel_root):
    out_rows = []
    for dp, dn, fn in os.walk(os.path.join(base_dir, rel_root)):
        for n in sorted(dn + fn):
            full = os.path.join(dp, n)
            rel = os.path.relpath(full, base_dir)
            st = os.lstat(full)
            r = {"path": rel, "mode": format(stat.S_IMODE(st.st_mode), "o")}
            if stat.S_ISLNK(st.st_mode): r.update(type="symlink", target=os.readlink(full))
            elif stat.S_ISDIR(st.st_mode): r["type"] = "directory"
            else: r.update(type="file", bytes=st.st_size, sha256=sha(open(full, "rb").read()))
            out_rows.append(r)
    return out_rows

root, packages = CLOSURES["checker"]
shutil.rmtree(scratch, ignore_errors=True)
shutil.copytree(os.path.join(subject, root), os.path.join(scratch, root), symlinks=True)
def digests():
    _, pk, _ = summarize(tree_rows(scratch, root), root, packages, fixed_rule)
    return {p["package"]: (p["files"], p["treeSha256"]) for p in pk}
baseline = digests()
controls = []
def control(label, action, expect_changed, expect_empty=None):
    global all_ok
    shutil.rmtree(scratch); shutil.copytree(os.path.join(subject, root), os.path.join(scratch, root), symlinks=True)
    action(os.path.join(scratch, root))
    d = digests()
    changed = sorted(k for k in d if d[k] != baseline[k])
    empty = sorted(k for k in d if d[k][0] == 0)
    ok = changed == sorted(expect_changed) and (expect_empty is None or empty == sorted(expect_empty))
    all_ok &= ok
    controls.append({"control": label, "changedPackages": changed, "emptyPackages": empty, "expectedChanged": expect_changed, "pass": ok})
def flip(p):
    f = os.path.join(p, "tapable/package.json"); b = bytearray(open(f, "rb").read()); b[-2] ^= 1; open(f, "wb").write(b)
control("byte flip in tapable/package.json", flip, ["node_modules/tapable"])
control("added file in graceful-fs", lambda p: open(os.path.join(p, "graceful-fs/extra.js"), "w").write("x"), ["node_modules/graceful-fs"])
control("mode change in enhanced-resolve/package.json", lambda p: os.chmod(os.path.join(p, "enhanced-resolve/package.json"), 0o600), ["node_modules/enhanced-resolve"])
control("typescript package removed (must be detected as empty)", lambda p: shutil.rmtree(os.path.join(p, "typescript")), ["node_modules/typescript"], ["node_modules/typescript"])
def retarget(p):
    os.symlink("../tapable/package.json", os.path.join(p, "graceful-fs/linked.json"))
control("symlink added in graceful-fs", retarget, ["node_modules/graceful-fs"])
control("no change", lambda p: None, [])
shutil.rmtree(scratch, ignore_errors=True)
report["driftControls"] = controls
report["allAssertionsPass"] = all_ok
json.dump(report, open(out, "w"), indent=1)
print(json.dumps({n: {k: c[k] for k in ("authorDeclaredZeroFilePackages", "authorDeclaredPackages", "defectReproducedFromRows", "correctedNonemptyAll", "accounting", "nonPackageEntries")} for n, c in report["closures"].items()}, indent=1))
print(json.dumps({"archiveTies": ties, "rowsMatchActualTree": report["rowsMatchActualTree"], "driftControls": controls, "allAssertionsPass": all_ok}, indent=1))
