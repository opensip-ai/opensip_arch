#!/usr/bin/env python3
"""p14: verify the coauthor assessment's own empirical claims, and its cited hashes.

The assessment is a coauthor artifact, not an oracle. Its two load-bearing measurements are the
justification for the exact final wording, so they are re-measured here independently:

  (a) a nested governed occurrence declaring `retention: not-joined` admits WITH a reason,
      WITHOUT a reason, and with an EMPTY reason  -> "admission checks the declared retention,
      not the presence or content of that prose"
  (b) a directly annotated TOP-LEVEL non-governed property (UInt64, retention preimage, no join)
      refuses with RELATION_DIGEST_LAW_RESIDUE, while the SAME annotation on a NESTED non-governed
      member produces no sighting and admits -> "top-level selector properties"

Also re-hashes every file digest the assessment cites.
"""
import copy
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

V11 = Path("/tmp/opensip-design-corrections/candidate-subject.v11")
F = V11 / "docs/coop/design-corrections/foundation"
A = V11 / "docs/coop/design-corrections/reviews/digest-corrections-author.v9"

spec = importlib.util.spec_from_file_location("m", F / "identity-model.py")
M = importlib.util.module_from_spec(spec)
sys.modules["m"] = M
spec.loader.exec_module(M)
C = M.C

out = {}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ---- cited hashes
out["citedHashes"] = {
    "CODEX-PROPOSED": {
        "cited": "a3705e7e1cf69301cb0646b919a71eb5da5a6e0d4540648ecf6ede65bbdf2c5e",
        "actual": sha(A / "CODEX-PROPOSED-NORMATIVE-CLARIFICATION.md"),
        "citedBytes": 3908,
        "actualBytes": os.path.getsize(A / "CODEX-PROPOSED-NORMATIVE-CLARIFICATION.md")},
    "CODEX-AGREED": {
        "cited": "32db349536ffc74081b5081aa698f9966d100485268fc24822fde2a1a94cd13f",
        "actual": sha(A / "CODEX-AGREED-NORMATIVE-INSERT.md"),
        "citedBytes": 2825,
        "actualBytes": os.path.getsize(A / "CODEX-AGREED-NORMATIVE-INSERT.md")},
    "CODEX-PUBLIC-NOTE": {
        "cited": "e16c5c84aa277a2e75a01b8e220cdb17996444993c933038a943fab3dd8672c5",
        "actual": sha(A / "CODEX-PUBLIC-NOTE.md"),
        "citedBytes": 3621,
        "actualBytes": os.path.getsize(A / "CODEX-PUBLIC-NOTE.md")},
    "identity-model.py(corrected)": {
        "cited": "de3ae06bac169cf3b41b9cea43c2b0c7113ed2de6b4a3ae164fc8b4d9cc77557",
        "actual": sha(F / "identity-model.py"),
        "citedBytes": None,
        "actualBytes": os.path.getsize(F / "identity-model.py")},
}
out["allCitedHashesMatch"] = all(
    v["cited"] == v["actual"] for v in out["citedHashes"].values())


def verdict(name, d):
    try:
        M.relation_annotation_closure(name, d)
        return "ADMIT"
    except C.AdmissionError as exc:
        return str(exc)
    except Exception as exc:
        return "OTHER:" + type(exc).__name__


# ---- (a) nested governed not-joined, with/without/empty reason
def nested_not_joined(reason_mode):
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    ann = {"representation": "raw-artifact", "retention": "not-joined",
           "authority": "probe"}
    if reason_mode == "with":
        ann["reason"] = "a stated reason"
    elif reason_mode == "empty":
        ann["reason"] = ""
    d["$defs"]["FilePayloadV1"]["properties"]["probe"] = {
        "type": "object",
        "properties": {"inner": dict({"$ref": "#/$defs/DigestHex"},
                                     **{"x-opensip-digest": ann})}}
    return d


out["claimA_nestedNotJoinedReason"] = {
    mode: verdict("file", nested_not_joined(mode))
    for mode in ("with", "without", "empty")}
out["claimA_holds"] = all(v == "ADMIT" for v in out["claimA_nestedNotJoinedReason"].values())

# control: the same nested occurrence with a JOINED retention must refuse as unjoinable,
# so claimA's admissions are caused by the not-joined declaration and not by nesting itself
d = copy.deepcopy(M.RELATION_DOCUMENT)
d["$defs"]["FilePayloadV1"]["properties"]["probe"] = {
    "type": "object",
    "properties": {"inner": dict({"$ref": "#/$defs/DigestHex"}, **{"x-opensip-digest": {
        "representation": "raw-artifact", "retention": "preimage", "authority": "probe"}})}}
out["claimA_control_nestedJoinedRetention"] = verdict("file", d)

# ---- (b) top-level vs nested directly annotated NON-governed property
ANN_PREIMAGE = {"representation": "raw-artifact", "retention": "preimage",
                "authority": "probe"}


def nongoverned(placement):
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    node = dict({"$ref": "#/$defs/UInt64"}, **{"x-opensip-digest": ANN_PREIMAGE})
    if placement == "top-level":
        d["$defs"]["FilePayloadV1"]["properties"]["stray"] = node
    else:
        d["$defs"]["FilePayloadV1"]["properties"]["stray"] = {
            "type": "object", "properties": {"inner": node}}
    return d


out["claimB"] = {
    "topLevel": verdict("file", nongoverned("top-level")),
    "nested": verdict("file", nongoverned("nested")),
}
cov_top = M.relation_digest_annotation_coverage(nongoverned("top-level"))
cov_nested = M.relation_digest_annotation_coverage(nongoverned("nested"))
out["claimB"]["topLevelSightingPaths"] = [
    s["path"] for s in cov_top["sightings"] if "stray" in s["path"]]
out["claimB"]["nestedSightingPaths"] = [
    s["path"] for s in cov_nested["sightings"] if "stray" in s["path"]]
out["claimB_holds"] = (
    out["claimB"]["topLevel"].startswith("RELATION_DIGEST_LAW_RESIDUE:file:stray")
    and out["claimB"]["nested"] == "ADMIT"
    and out["claimB"]["nestedSightingPaths"] == [])

# ---- all six declared refusal causes are reachable (the assessment's last table row)
out["sixCausesReachable"] = {}
print(json.dumps(out, indent=2))
