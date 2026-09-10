#!/usr/bin/env python3
"""p17: representative Run/body identity stability across the v10 -> v11 model delta.

The delta touches only the schema-law functions, so no identity should move. Rather than infer
that from the diff, this recomputes identities under BOTH models and compares:
  - identifier() over every registered domain for a fixed representative value
  - the canonical bytes and identity of the registered relation document itself
  - body frame parsing / body language version over the retained frames the model exposes
  - the full source text of the identity-critical modules that were NOT part of the delta
"""
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

V10 = Path("/tmp/opensip-design-corrections/candidate-subject.v10/docs/coop/design-corrections/foundation")
V11 = Path("/tmp/opensip-design-corrections/candidate-subject.v11/docs/coop/design-corrections/foundation")


def load(tag, home):
    spec = importlib.util.spec_from_file_location(tag, home / "identity-model.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[tag] = mod
    spec.loader.exec_module(mod)
    return mod


A, B = load("m10i", V10), load("m11i", V11)
out = {}

# identity-critical sibling modules must be byte-identical
siblings = {}
for name in sorted(set(os.listdir(V10)) | set(os.listdir(V11))):
    if not name.endswith((".py", ".json")):
        continue
    pa, pb = V10 / name, V11 / name
    ha = hashlib.sha256(pa.read_bytes()).hexdigest() if pa.is_file() else None
    hb = hashlib.sha256(pb.read_bytes()).hexdigest() if pb.is_file() else None
    if ha != hb:
        siblings[name] = {"v10": ha, "v11": hb}
out["foundationFilesChanged"] = siblings
out["onlyExpectedFoundationFilesChanged"] = set(siblings) <= {
    "identity-model.py", "check-identity.py", "identity-report.json",
    "source-pins.v1.json", "validation-report.json"}

# identifier() over representative values in every registered domain
DOMAINS = ["run", "plan", "view", "coverage", "finding", "import", "snapshot",
           "semantic-evidence", "proof-bundle", "file", "package"]
VALUE = {"schemaVersion": 1, "probe": "representative", "n": 7,
         "nested": {"a": [1, 2, 3], "b": "x"}}
ids = {}
for d in DOMAINS:
    try:
        ids[d] = {"v10": A.identifier(d, VALUE), "v11": B.identifier(d, VALUE)}
    except Exception as exc:
        ids[d] = {"error": type(exc).__name__}
out["identifierByDomain"] = ids
out["allIdentifiersStable"] = all(
    v.get("v10") == v.get("v11") for v in ids.values() if "error" not in v)

# the registered relation document: canonical bytes and its identity
ca = A.C.canonical(A.RELATION_DOCUMENT)
cb = B.C.canonical(B.RELATION_DOCUMENT)
out["relationDocument"] = {
    "canonicalBytesEqual": ca == cb,
    "sha256v10": hashlib.sha256(ca).hexdigest(),
    "sha256v11": hashlib.sha256(cb).hexdigest(),
    "identityV10": A.identifier("schema-document", A.RELATION_DOCUMENT),
    "identityV11": B.identifier("schema-document", B.RELATION_DOCUMENT),
}
out["relationDocument"]["identityStable"] = (
    out["relationDocument"]["identityV10"] == out["relationDocument"]["identityV11"])

# body frame parse + body language version over a representative retained frame
frames = {}
for label, raw in (
    ("typescript", b'opensip.body.v1\x00typescript\x005.4.2\x00' + b'{"k":1}'),
    ("rust", b'opensip.body.v1\x00rust\x001.79.0\x00' + b'{"k":1}'),
):
    r = {}
    for tag, M in (("v10", A), ("v11", B)):
        try:
            r[tag] = repr(M.parse_body_frame(raw))[:220]
        except Exception as exc:
            r[tag] = "ERR:" + type(exc).__name__ + ":" + str(exc)[:80]
    r["stable"] = r["v10"] == r["v11"]
    frames[label] = r
out["bodyFrames"] = frames
out["bodyFramesStable"] = all(v["stable"] for v in frames.values())

# the relation registry rows themselves
out["registryRowsEqual"] = A.C.canonical(A.RELATIONS) == B.C.canonical(B.RELATIONS)

out["ALL_STABLE"] = (out["allIdentifiersStable"]
                     and out["relationDocument"]["identityStable"]
                     and out["relationDocument"]["canonicalBytesEqual"]
                     and out["bodyFramesStable"]
                     and out["registryRowsEqual"]
                     and out["onlyExpectedFoundationFilesChanged"])
print(json.dumps(out, indent=2))
