"""Final custody re-verification before the verdict: the consumer-input manifest and every member, unchanged since phase 0.
Writes runs/final-custody.json.  Usage: python3 tools/final_custody.py
"""
import hashlib
import json
import os

ROOT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/"
SUBJ = ROOT + "subject/"
# HC-30 (source39) and HC-43 (source41): the ported tool carried the prior kit's expected hashes; the source41 expectations are the
# user-supplied values
EXPECT_MANIFEST = "31369cc8c3b71e559c50f107104daff4d6d428e20fb75dc1e3914a2acc1ec6dd"
EXPECT_PARENT = "eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236"

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
