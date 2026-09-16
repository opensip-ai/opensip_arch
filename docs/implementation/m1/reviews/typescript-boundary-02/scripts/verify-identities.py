#!/usr/bin/env python3
"""Separates the identities in play and recomputes each independently:
  1. outer root manifest sha256 (file bytes)
  2. author freeze-manifest.json raw sha256 (file bytes) vs the outer row
  3. author declared aggregateSha256 (algorithm from freeze-manifest.mjs) recomputed
     from the ACTUAL tree, not from the author's rows
  4. per-package treeSha256 recomputed from the actual tree
  5. lock integrity / versions / install scripts, and archived tarball hashes,
     plus a byte comparison of the two archived tarballs against the materialized trees.
usage: verify-identities.py SUBJECT_ROOT OUTER_MANIFEST OUT.json
"""
import base64, hashlib, io, json, os, stat, sys, tarfile

root, outer_path, out = sys.argv[1:4]
sha = lambda b: hashlib.sha256(b).hexdigest()
res = {}

outer_raw = open(outer_path, "rb").read()
res["outerManifestSha256"] = sha(outer_raw)
outer = json.loads(outer_raw)
rows = {r["path"]: r for r in outer["files"]}

fm_raw = open(os.path.join(root, "freeze-manifest.json"), "rb").read()
fm = json.loads(fm_raw)
res["authorFreezeRawSha256"] = sha(fm_raw)
res["authorFreezeOuterRowSha256"] = rows["freeze-manifest.json"]["sha256"]
res["authorFreezeDeclaredAggregate"] = fm["aggregateSha256"]

# walk actual tree the way freeze-manifest.mjs does: readdirSync().sort() (JS default sort = UTF-16 code unit order)
def js_sorted(names):
    return sorted(names, key=lambda s: s.encode("utf-16-be"))
LAUNCHER = {"launch-public.py", "process.json", "prompt.md", "public-events.jsonl", "result.json", "response.json", "final-response.md", "process-completion.json"}
entries = []
def walk(rel):
    for name in js_sorted(os.listdir(os.path.join(root, rel) if rel else root)):
        r = f"{rel}/{name}" if rel else name
        a = os.path.join(root, r)
        st = os.lstat(a)
        if stat.S_ISLNK(st.st_mode):
            entries.append({"path": r, "type": "symlink", "target": os.readlink(a)})
        elif stat.S_ISDIR(st.st_mode):
            if not (r + "/").startswith("trial/work/"):
                walk(r)
        else:
            entries.append({"path": r, "type": "file", "sha256": sha(open(a, "rb").read()), "bytes": st.st_size, "mode": format(st.st_mode & 0o777, "o")})
walk("")
files = [e for e in entries if e["path"] != "freeze-manifest.json" and e["path"] not in LAUNCHER]
line = lambda f, strip="": f'{f["type"]}\0{f["path"][len(strip):]}\0{f.get("sha256") or f.get("target")}'
agg = sha("\n".join(line(f) for f in files).encode())
res["recomputedAggregateFromActualTree"] = agg
res["aggregateMatchesDeclared"] = agg == fm["aggregateSha256"]
res["authorRowsEqualActualRows"] = [ {k: v for k, v in r.items() if k != "group"} for r in fm["files"]] == files
# outer manifest = author rows + the author freeze row?
outer_minus = [r for r in outer["files"] if r["path"] != "freeze-manifest.json"]
res["outerRowsMinusFreezeEqualAuthorRows"] = outer_minus == fm["files"]
res["outerRowCount"] = len(outer["files"])
res["authorRowCount"] = len(fm["files"])

lock = json.load(open(os.path.join(root, "trial/package-lock.json")))
pk = []
for key, meta in lock["packages"].items():
    if not key:
        continue
    prefix = f"trial/{key}/"
    tree = [f for f in files if f["path"].startswith(prefix) and "node_modules/" not in f["path"][len(prefix):]]
    manifest = json.load(open(os.path.join(root, "trial", key, "package.json")))
    pk.append({"path": key, "version": manifest["version"], "lockVersion": meta.get("version"),
               "hasInstallScript": bool(meta.get("hasInstallScript")), "treeSha256": sha("\n".join(line(f, prefix) for f in tree).encode()),
               "files": len(tree), "integrity": meta.get("integrity"), "scriptsInManifest": sorted((manifest.get("scripts") or {}).keys())})
declared = {p["path"]: p for p in fm["toolClosure"]["packageList"]}
res["packages"] = len(pk)
res["packageTreeMismatches"] = [p["path"] for p in pk if declared[p["path"]]["treeSha256"] != p["treeSha256"] or declared[p["path"]]["files"] != p["files"]]
res["versionMismatches"] = [p["path"] for p in pk if p["version"] != p["lockVersion"]]
res["lockInstallScripts"] = [p["path"] for p in pk if p["hasInstallScript"]]
res["manifestLifecycleScripts"] = {p["path"]: [s for s in p["scriptsInManifest"] if s in ("preinstall", "install", "postinstall", "prepare")] for p in pk if any(s in ("preinstall", "install", "postinstall", "prepare") for s in p["scriptsInManifest"])}
res["gypOrBindingFiles"] = [f["path"] for f in files if f["path"].startswith("trial/node_modules/") and (f["path"].endswith("binding.gyp") or f["path"].endswith(".node"))]
tc = [f for f in files if f["path"].startswith("trial/node_modules/")]
res["toolClosureEntries"] = len(tc)
res["toolClosureSymlinks"] = [f["path"] for f in tc if f["type"] == "symlink"]
res["toolClosureBytes"] = sum(f.get("bytes", 0) for f in tc)
# symlink targets stay inside trial/node_modules
res["symlinkEscapes"] = [f["path"] for f in tc if f["type"] == "symlink" and not os.path.normpath(os.path.join(os.path.dirname(f["path"]), f["target"])).startswith("trial/node_modules/")]
res["filesNotInAnyLockPackage"] = [f["path"] for f in tc if not any(f["path"].startswith(f"trial/{k}/") for k in lock["packages"] if k)]

# tarball custody: hash and byte-compare against materialized tree
pins = json.load(open(os.path.join(root, "provenance/pins.json")))
tar_report = {}
for name, key in (("dependency-cruiser-18.3.1.tgz", "node_modules/dependency-cruiser"), ("typescript-6.0.3.tgz", "node_modules/typescript")):
    raw = open(os.path.join(root, "provenance", name), "rb").read()
    s512 = "sha512-" + base64.b64encode(hashlib.sha512(raw).digest()).decode()
    t = tarfile.open(fileobj=io.BytesIO(raw))
    tar_files = {}
    for m in t.getmembers():
        if m.isfile():
            rel = m.name.split("/", 1)[1]
            tar_files[rel] = sha(t.extractfile(m).read())
    mat = {}
    base = os.path.join(root, "trial", key)
    for f in files:
        if f["path"].startswith(f"trial/{key}/") and f["type"] == "file":
            mat[f["path"][len(f"trial/{key}/"):]] = f["sha256"]
    diff = sorted(set(tar_files) ^ set(mat)) + sorted(k for k in tar_files if k in mat and tar_files[k] != mat[k])
    tar_report[name] = {"sha256": sha(raw), "sha512": s512, "matchesLockIntegrity": s512 == lock["packages"][key]["integrity"],
                        "matchesPinsSha256": sha(raw) == pins["independentTarballHashes"][name]["sha256"],
                        "tarFiles": len(tar_files), "materializedFiles": len(mat), "byteDifferences": diff[:20], "identical": not diff}
res["tarballs"] = tar_report
res["pinsLockfileSha256Matches"] = sha(open(os.path.join(root, "trial/package-lock.json"), "rb").read()) == pins["lockfile"]["sha256"]
res["pinsManifestSha256Matches"] = sha(open(os.path.join(root, "trial/package.json"), "rb").read()) == pins["manifest"]["sha256"]
res["lockRegistryHosts"] = sorted({(m.get("resolved") or "").split("/")[2] for k, m in lock["packages"].items() if k and m.get("resolved")})
res["lockPackagesWithoutIntegrity"] = [k for k, m in lock["packages"].items() if k and not m.get("integrity")]
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items()}, indent=1)[:6000])
