"""Final custody re-verification before the verdict: the consumer-input manifest and every member, unchanged since phase 0.
Writes runs/final-custody.json.  Usage: python3 tools/final_custody.py
"""
import hashlib
import json
import os

ROOT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/"
SUBJ = ROOT + "subject/"
# HC-30 (source39) and HC-43 (source41): the ported tool carried the prior kit's expected hashes; the source41 expectations are the
# user-supplied values
# HC-49 (source42): source42 user-supplied values
# HC-55 (source43): source43 user-supplied values (source42: manifest 9c90a1e8..., parent f602fc7e...)
# HC-56 (source44): source44 user-supplied values (source43: manifest 6d8912f4..., parent db43ee76...)
# HC-59 (source45): source45 user-supplied values (source44: manifest a3a5fba8..., parent e873c8db...)
EXPECT_MANIFEST = "707715363ac6249e22a4eb30a628ac61f6e951d2d8de71cc8641cfdeb7a6ee69"
EXPECT_PARENT = "8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155"

mb = open(SUBJ + "consumer-input-manifest.json", "rb").read()
m = json.loads(mb)
bad, listed = [], set()
for f in m["files"]:
    b = open(SUBJ + f["path"], "rb").read()
    if hashlib.sha256(b).hexdigest() != f["sha256"] or len(b) != f["bytes"]:
        bad.append(f["path"])
    listed.add(f["path"])
unlisted = [os.path.relpath(os.path.join(d, x), SUBJ) for d, _, fs in os.walk(SUBJ) for x in fs
            if os.path.relpath(os.path.join(d, x), SUBJ) not in listed | {"consumer-input-manifest.json"}]
phase0 = json.load(open(ROOT + "output/vectors/phase0-custody.json"))
same_rows = [(r["path"], r["sha256"]) for r in phase0["fileRows"]] == [(f["path"], f["sha256"]) for f in m["files"]]
out = {"manifestSha256": hashlib.sha256(mb).hexdigest(), "expectedManifestSha256": EXPECT_MANIFEST,
       "parentSubjectSha256": m.get("parentSubjectSha256"), "expectedParent": EXPECT_PARENT, "files": len(m["files"]),
       "memberFailures": bad, "unlistedFiles": unlisted, "identicalToPhase0Rows": same_rows,
       "charterSha256": hashlib.sha256(open(ROOT + "charter.md", "rb").read()).hexdigest(),
       "requirementsSha256": hashlib.sha256(open(ROOT + "requirements.json", "rb").read()).hexdigest()}
out["result"] = "PASS" if (out["manifestSha256"] == EXPECT_MANIFEST and out["parentSubjectSha256"] == EXPECT_PARENT and not bad and not unlisted and same_rows) else "FAIL"
json.dump(out, open(ROOT + "output/runs/final-custody.json", "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1))
