"""source43.v1 setup probe (read-only on the kit): verify the supplied consumer-input manifest and every member, and compute the delta
against my own source42 custody rows (output/vectors/phase0-custody.json as copied from my source42.v3 output). Also verifies that the
copied output still names the source42.v3 root (paths to adapt). Writes output/s43-kit-delta.json. Usage: python3 output/s43_kit_delta.py
"""
import hashlib
import json
import os

ROOT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/"
SUBJ = ROOT + "subject/"
OUT = ROOT + "output/"
EXPECT_MANIFEST = "6d8912f4a78d65946f09047254978570974328ae4d7d883d453f8855347f1beb"
EXPECT_PARENT = "db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d"
OLD_ROOT = "consumer-b.v24-source42.v3"

mb = open(SUBJ + "consumer-input-manifest.json", "rb").read()
m = json.loads(mb)
bad, listed = [], set()
for f in m["files"]:
    b = open(SUBJ + f["path"], "rb").read()
    if hashlib.sha256(b).hexdigest() != f["sha256"] or len(b) != f["bytes"]:
        bad.append(f["path"])
    listed.add(f["path"])
unlisted = sorted(os.path.relpath(os.path.join(d, x), SUBJ) for d, _, fs in os.walk(SUBJ) for x in fs
                  if os.path.relpath(os.path.join(d, x), SUBJ) not in listed | {"consumer-input-manifest.json"})
old_rows = json.load(open(OUT + "vectors/phase0-custody.json"))["fileRows"]
old = {r["path"]: r["sha256"] for r in old_rows}
new = {f["path"]: f["sha256"] for f in m["files"]}
changed = sorted(p for p in set(new) & set(old) if new[p] != old[p])
refs = []
for sub in ("ref", "builders", "tools", "vectors", "preserved/pre-s42/ref", "preserved/pre-s42/builders", "preserved/pre-s42/tools", "preserved/pre-s42/vectors"):
    base = OUT + sub
    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            if name.endswith(".py") and OLD_ROOT in open(os.path.join(base, name), encoding="utf-8").read():
                refs.append(f"{sub}/{name}")
top_py = [x for x in os.listdir(OUT) if x.endswith(".py") and OLD_ROOT in open(OUT + x, encoding="utf-8").read()]
n_files = sum(len(fs) for _, _, fs in os.walk(OUT))
out = {"manifestSha256": hashlib.sha256(mb).hexdigest(), "expectedManifest": EXPECT_MANIFEST,
       "parentSubjectSha256": m.get("parentSubjectSha256"), "expectedParent": EXPECT_PARENT,
       "manifestKeys": [k for k in m if k != "files"], "manifestMeta": {k: v for k, v in m.items() if k != "files"},
       "fileCount": len(m["files"]), "memberFailures": bad, "unlisted": unlisted,
       "deltaVsOwnSource42Rows": {"added": sorted(set(new) - set(old)), "removed": sorted(set(old) - set(new)), "changed": changed,
                                  "changedBytes": {p: [next(r["bytes"] for r in old_rows if r["path"] == p) if "bytes" in old_rows[0] else None,
                                                       next(f["bytes"] for f in m["files"] if f["path"] == p)] for p in changed},
                                  "unchanged": sum(1 for p in set(new) & set(old) if new[p] == old[p])},
       "charterSha256": hashlib.sha256(open(ROOT + "charter.md", "rb").read()).hexdigest(),
       "requirementsSha256": hashlib.sha256(open(ROOT + "requirements.json", "rb").read()).hexdigest(),
       "copiedOutputFileCount": n_files, "executablePyNamingSource42v3Root": refs, "topLevelPyNamingSource42v3Root": top_py}
out["result"] = "PASS" if out["manifestSha256"] == EXPECT_MANIFEST and out["parentSubjectSha256"] == EXPECT_PARENT and not bad and not unlisted and len(m["files"]) == 104 else "FAIL"
json.dump(out, open(OUT + "s43-kit-delta.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("executablePyNamingSource42v3Root",)}, indent=1))
print("executable py naming v3 root:", len(refs))
