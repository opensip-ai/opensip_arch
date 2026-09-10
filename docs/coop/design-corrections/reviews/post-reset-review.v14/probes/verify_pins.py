import hashlib, json, os, sys
ROOT = sys.argv[1]
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

out = {}
def check(pinfile, entries):
    res = {"pinFile": pinfile, "count": len(entries), "ok": [], "stale": [], "missing": []}
    for path, expect in entries:
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            res["missing"].append(path); continue
        a = sha(full)
        (res["ok"] if a == expect else res["stale"]).append(
            path if a == expect else {"path": path, "pinned": expect, "actual": a})
    res["okCount"] = len(res["ok"]); res.pop("ok")
    return res

# foundation / workflows: {"files": {path: sha or {...}}}
for pf in ["docs/coop/design-corrections/foundation/source-pins.v1.json",
           "docs/coop/design-corrections/workflows/source-pins.v1.json"]:
    d = json.load(open(os.path.join(ROOT, pf)))
    ents = []
    f = d["files"]
    if isinstance(f, dict):
        for k, v in f.items():
            ents.append((k, v if isinstance(v, str) else v.get("sha256")))
    else:
        for e in f:
            ents.append((e["path"], e["sha256"]))
    out[pf] = check(pf, ents)

# native / security: {"pins": ...}
for pf in ["docs/coop/design-corrections/native/source-pins.v2.json",
           "docs/coop/design-corrections/security/source-pins.v1.json"]:
    d = json.load(open(os.path.join(ROOT, pf)))
    p = d["pins"]
    ents = []
    if isinstance(p, dict):
        for k, v in p.items():
            if isinstance(v, str): ents.append((k, v))
            elif isinstance(v, dict) and "sha256" in v: ents.append((v.get("path", k), v["sha256"]))
            elif isinstance(v, list):
                for e in v: ents.append((e["path"], e["sha256"]))
    else:
        for e in p: ents.append((e["path"], e["sha256"]))
    out[pf] = check(pf, ents)

out["anyStale"] = any(v["stale"] for v in out.values() if isinstance(v, dict))
out["anyMissing"] = any(v["missing"] for v in out.values() if isinstance(v, dict))
print(json.dumps(out, indent=1))
