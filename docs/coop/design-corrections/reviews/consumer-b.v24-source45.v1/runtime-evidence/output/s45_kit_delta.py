"""source45.v1 setup probe (read-only on the kit). It does three things:
  - verifies the supplied consumer-input manifest and every member;
  - computes the delta against my own source44 custody rows (output/vectors/phase0-custody.json as copied from my source44.v1 output);
  - lists copied code that still names the source44.v1 root (paths to adapt).
Writes output/s45-kit-delta.json. Usage: python3 output/s45_kit_delta.py
"""
import hashlib
import json
import os

ROOT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/"
SUBJ = ROOT + "subject/"
OUT = ROOT + "output/"
EXPECT_MANIFEST = "707715363ac6249e22a4eb30a628ac61f6e951d2d8de71cc8641cfdeb7a6ee69"
EXPECT_PARENT = "8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155"
OLD_ROOT = "consumer-b.v24-source44.v1"

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
p0 = json.load(open(OUT + "vectors/phase0-custody.json"))
old = {r["path"]: r for r in p0["fileRows"]}
new = {f["path"]: f for f in m["files"]}
changed = sorted(p for p in set(new) & set(old) if new[p]["sha256"] != old[p]["sha256"])
refs = []
for sub in ("ref", "builders", "tools", "vectors", "preserved/pre-s42/ref", "preserved/pre-s42/builders", "preserved/pre-s42/tools", "preserved/pre-s42/vectors"):
    base = OUT + sub
    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            if name.endswith(".py") and OLD_ROOT in open(os.path.join(base, name), encoding="utf-8").read():
                refs.append(f"{sub}/{name}")
out = {"manifestSha256": hashlib.sha256(mb).hexdigest(), "expectedManifest": EXPECT_MANIFEST,
       "parentSubjectSha256": m.get("parentSubjectSha256"), "expectedParent": EXPECT_PARENT,
       "manifestMeta": {k: v for k, v in m.items() if k != "files"}, "fileCount": len(m["files"]), "memberFailures": bad, "unlisted": unlisted,
       "priorRowsRuntime": p0.get("runtime"), "priorRowsManifestSha256": p0.get("manifest", {}).get("sha256"),
       "deltaVsOwnSource44Rows": {"added": sorted(set(new) - set(old)), "removed": sorted(set(old) - set(new)), "changed": changed,
                                  "addedRows": [new[p] for p in sorted(set(new) - set(old))],
                                  "changedBytes": {p: [old[p]["bytes"], new[p]["bytes"]] for p in changed},
                                  "changedSha": {p: [old[p]["sha256"], new[p]["sha256"]] for p in changed},
                                  "unchanged": sum(1 for p in set(new) & set(old) if new[p]["sha256"] == old[p]["sha256"])},
       "charterSha256": hashlib.sha256(open(ROOT + "charter.md", "rb").read()).hexdigest(),
       "requirementsSha256": hashlib.sha256(open(ROOT + "requirements.json", "rb").read()).hexdigest(),
       "copiedOutputFileCount": sum(len(fs) for _, _, fs in os.walk(OUT)), "executablePyNamingSource44Root": refs}
out["result"] = "PASS" if out["manifestSha256"] == EXPECT_MANIFEST and out["parentSubjectSha256"] == EXPECT_PARENT and not bad and not unlisted and len(m["files"]) == 107 else "FAIL"
json.dump(out, open(OUT + "s45-kit-delta.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("executablePyNamingSource44Root", "manifestMeta")}, indent=1))
print("executable py naming source44 root:", len(refs))
