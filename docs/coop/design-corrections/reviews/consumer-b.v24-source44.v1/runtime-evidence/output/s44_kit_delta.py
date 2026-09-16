"""source44.v1 setup probe (read-only on the kit): verify the supplied consumer-input manifest and every member, and compute the delta
against my own source43 custody rows (output/vectors/phase0-custody.json as copied from my source43.v1 output). Also lists copied code that
still names the source43.v1 root (paths to adapt). Writes output/s44-kit-delta.json. Usage: python3 output/s44_kit_delta.py
"""
import hashlib
import json
import os

ROOT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/"
SUBJ = ROOT + "subject/"
OUT = ROOT + "output/"
EXPECT_MANIFEST = "a3a5fba87d944fdec8e28165f42ad13b0268b03d0493eddf77bc32b0833e348f"
EXPECT_PARENT = "e873c8db7b50f8d4bc4c6b1754239fb200b11f4e5d0f23b1ceaa6ea17297a32b"
OLD_ROOT = "consumer-b.v24-source43.v1"

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
old = {r["path"]: r for r in old_rows}
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
       "deltaVsOwnSource43Rows": {"added": sorted(set(new) - set(old)), "removed": sorted(set(old) - set(new)), "changed": changed,
                                  "addedRows": [new[p] for p in sorted(set(new) - set(old))],
                                  "changedBytes": {p: [old[p]["bytes"], new[p]["bytes"]] for p in changed},
                                  "changedSha": {p: [old[p]["sha256"], new[p]["sha256"]] for p in changed},
                                  "unchanged": sum(1 for p in set(new) & set(old) if new[p]["sha256"] == old[p]["sha256"])},
       "charterSha256": hashlib.sha256(open(ROOT + "charter.md", "rb").read()).hexdigest(),
       "requirementsSha256": hashlib.sha256(open(ROOT + "requirements.json", "rb").read()).hexdigest(),
       "copiedOutputFileCount": sum(len(fs) for _, _, fs in os.walk(OUT)), "executablePyNamingSource43Root": refs}
out["result"] = "PASS" if out["manifestSha256"] == EXPECT_MANIFEST and out["parentSubjectSha256"] == EXPECT_PARENT and not bad and not unlisted and len(m["files"]) == 107 else "FAIL"
json.dump(out, open(OUT + "s44-kit-delta.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "executablePyNamingSource43Root"}, indent=1))
print("executable py naming source43 root:", len(refs))
