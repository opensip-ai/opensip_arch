#!/usr/bin/env python3
"""p15: did root apply ONLY the released coauthor delta, unmodified?

Compares, byte for byte:
  - the coauthor's retained author-source files  vs  the applied v11 files
  - the retained `before` images                 vs  the frozen v10 files
so that "root applied only the released delta" is checked from bytes rather than asserted.

Also verifies the same for the normative insert application, and checks the fixture checker's
declared SHA provenance (integration-fixtures.py claims to be extracted from a specific
check-identity.py digest).
"""
import hashlib
import json
import os

V10 = "/tmp/opensip-design-corrections/candidate-subject.v10"
V11 = "/tmp/opensip-design-corrections/candidate-subject.v11"
DC = "docs/coop/design-corrections"
REL = f"{DC}/reviews/codex-post-reset.v1/released-coauthor-delta.v11"
NORM = f"{DC}/reviews/codex-post-reset.v1/normative-annotation-clarification.v11"
AUTH = f"{DC}/reviews/digest-corrections-author.v9/author-source"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


out = {}
custody = json.load(open(os.path.join(V11, REL, "custody.json")))
rows = []
for entry in custody["files"]:
    path = entry["path"]
    applied = sha(os.path.join(V11, path))
    released = sha(os.path.join(V11, entry["actualReleasedSource"]))
    before_v10 = sha(os.path.join(V10, path))
    retained_before = sha(os.path.join(V11, REL, "before", os.path.basename(path)))
    rows.append({
        "path": path,
        "declaredBefore": entry["beforeSha256"],
        "declaredAfter": entry["afterSha256"],
        "frozenV10": before_v10,
        "frozenV11applied": applied,
        "coauthorReleasedSource": released,
        "retainedBeforeImage": retained_before,
        "beforeMatchesV10": before_v10 == entry["beforeSha256"],
        "afterMatchesV11": applied == entry["afterSha256"],
        "appliedEqualsReleasedSource": applied == released,
        "retainedBeforeEqualsV10": retained_before in (None, before_v10),
    })
out["sourceDelta"] = rows
out["sourceDeltaClean"] = all(
    r["beforeMatchesV10"] and r["afterMatchesV11"] and r["appliedEqualsReleasedSource"]
    and r["retainedBeforeEqualsV10"] for r in rows)

# the normative insert application: before/after images vs the frozen trees
DOC = "docs/v2/contracts/product-v1/identity-and-evidence.md"
out["normativeInsert"] = {
    "beforeImageSha": sha(os.path.join(V11, NORM, "before.md")),
    "frozenV10DocSha": sha(os.path.join(V10, DOC)),
    "afterImageSha": sha(os.path.join(V11, NORM, "after.md")),
    "frozenV11DocSha": sha(os.path.join(V11, DOC)),
    "agreedInsertSha": sha(os.path.join(V11, NORM, "agreed-insert.md")),
    "coauthorAgreedSha": sha(os.path.join(
        V11, f"{DC}/reviews/digest-corrections-author.v9/CODEX-AGREED-NORMATIVE-INSERT.md")),
}
n = out["normativeInsert"]
n["beforeEqualsV10"] = n["beforeImageSha"] == n["frozenV10DocSha"]
n["afterEqualsV11"] = n["afterImageSha"] == n["frozenV11DocSha"]
n["insertEqualsCoauthorAgreed"] = n["agreedInsertSha"] == n["coauthorAgreedSha"]
out["normativeInsertClean"] = (
    n["beforeEqualsV10"] and n["afterEqualsV11"] and n["insertEqualsCoauthorAgreed"])

# fixture checker provenance: integration-fixtures.py declares its producing checker digest
fx = open(os.path.join(V11, f"{DC}/integration-fixtures.py")).read()
declared = None
for line in fx.split("\n")[:6]:
    if "check-identity.py SHA256" in line:
        declared = line.strip().rstrip(".").split()[-1]
out["fixtureProvenance"] = {
    "declaredProducerSha256": declared,
    "actualCheckIdentitySha256": sha(os.path.join(V11, f"{DC}/foundation/check-identity.py")),
    "matches": declared == sha(os.path.join(V11, f"{DC}/foundation/check-identity.py")),
    "note": "synthetic shared-fixture construction is NOT an independent oracle; this only "
            "verifies the fixture names the checker it was actually extracted from",
}

out["ALL_CLEAN"] = (out["sourceDeltaClean"] and out["normativeInsertClean"]
                    and out["fixtureProvenance"]["matches"])
print(json.dumps(out, indent=2))
