"""PROBE B — a CURRENT target/proof-boundary claim, tested by construction.

Claim under test (atom-evaluation-contract.v1 section 2; target-attribution.schema.v2
properties.logicalPath; occupancy-companion.schema.v1):

  "logicalPath is a non-authoritative hint ONLY when occupancy is external or unknown
   AND kind is file or symbol. MUST be null when occupancy=first-party. MUST be null
   when kind=package."

The two explicit MUSTs are enforced by allOf branches. The word ONLY additionally
excludes kind=unknown. I construct the discriminating instances and ask BOTH schemas
and the reference admission whether they refuse, and then measure whether the two
lawful spellings of one provider claim mint DIFFERENT retained identities.
"""
import hashlib, importlib.util, json, os, sys

DC = '/tmp/opensip-design-corrections/candidate-subject.v26/docs/coop/design-corrections'
sys.path.insert(0, os.path.join(DC, 'foundation'))
from jsonschema import Draft202012Validator

R = {}
TA = json.load(open(os.path.join(DC, 'foundation/target-attribution.schema.v2.json'), encoding='utf-8'))
OC = json.load(open(os.path.join(DC, 'native/occupancy-companion.schema.v1.json'), encoding='utf-8'))


def V(schema, inst):
    v = Draft202012Validator(schema)
    errs = sorted(v.iter_errors(inst), key=lambda e: e.path)
    return [e.message[:120] for e in errs]


U = '0' * 64
base_ta = {
    "schemaVersion": 2, "planId": "plan2:" + "a" * 64, "sourceFactId": "fact2:" + "b" * 64,
    "producerClosure": "closure2:" + "c" * 64, "targetUniverse": U,
    "targetNativeId": "mod:opaque-thing", "kind": "unknown", "occupancy": "external",
    "exported": None, "logicalPath": None, "packageManifestPath": None, "evaluationNativeId": None,
}
base_oc = {
    "schemaVersion": 1, "candidateOrdinal": 0, "targetUniverseId": U,
    "targetNativeId": "mod:opaque-thing", "kind": "unknown", "occupancy": "external",
    "exported": None, "logicalPath": None, "packageManifestPath": None, "evaluationNativeId": None,
}

cases = {}
for name, kind, occ, lp in [
    ("B1 kind=unknown occ=external  logicalPath NULL ", "unknown", "external", None),
    ("B2 kind=unknown occ=external  logicalPath SET  ", "unknown", "external", "src/a.ts"),
    ("B3 kind=unknown occ=unknown   logicalPath SET  ", "unknown", "unknown", "src/a.ts"),
    ("B4 kind=file    occ=external  logicalPath SET  ", "file", "external", "src/a.ts"),
    ("B5 kind=file    occ=first-party logicalPath SET", "file", "first-party", "src/a.ts"),
    ("B6 kind=package occ=external  logicalPath SET  ", "package", "external", "src/a.ts"),
]:
    ta = dict(base_ta, kind=kind, occupancy=occ, logicalPath=lp)
    oc = dict(base_oc, kind=kind, occupancy=occ, logicalPath=lp)
    if kind == "symbol":
        ta["exported"] = oc["exported"] = "unknown"
    if occ == "first-party":
        ta["evaluationNativeId"] = oc["evaluationNativeId"] = "src/a.ts"
    if kind == "package" and occ in ("first-party", "external"):
        ta["packageManifestPath"] = oc["packageManifestPath"] = "pkg/package.json"
    cases[name] = {"targetAttributionV2_errors": V(TA, ta), "occupancyCompanionV1_errors": V(OC, oc),
                   "instance": ta}

for k in sorted(cases):
    c = cases[k]
    print("%s  TAv2:%-7s  OCv1:%-7s" % (
        k, "ADMIT" if not c["targetAttributionV2_errors"] else "REFUSE",
        "ADMIT" if not c["occupancyCompanionV1_errors"] else "REFUSE"))
R["cases"] = {k: {"TAv2": ("ADMIT" if not v["targetAttributionV2_errors"] else "REFUSE"),
                  "OCv1": ("ADMIT" if not v["occupancyCompanionV1_errors"] else "REFUSE"),
                  "errs": v["targetAttributionV2_errors"][:2]} for k, v in cases.items()}

# identity consequence: the two lawful spellings of ONE provider claim
C = importlib.util.spec_from_file_location("canon", os.path.join(DC, 'foundation/canonical.py'))
canon = importlib.util.module_from_spec(C)
C.loader.exec_module(canon)
a = cases["B1 kind=unknown occ=external  logicalPath NULL "]["instance"]
b = cases["B2 kind=unknown occ=external  logicalPath SET  "]["instance"]
da = hashlib.sha256(canon.canonical(a)).hexdigest()
db = hashlib.sha256(canon.canonical(b)).hexdigest()
R["identity_consequence"] = {
    "TargetAttributionV2 identity recipe": "raw SHA-256 of C(record)",
    "digest_logicalPath_null": da, "digest_logicalPath_set": db, "differ": da != db,
    "why_it_matters": ("TargetAttributionV2 digests enter hostCapture.hostDerivedRefs and "
                       "ExecutionInputsV1.selectedRefs, hence C(ExecutionInputsV1), hence "
                       "proof.executionInputsDigest, hence proof3/evidence3/seal3/run3."),
}

# does any internal fault key exist for this position?
R["internal_fault_keys_for_logicalPath"] = [
    k for k in TA["x-opensip-new-internal-faults"]["keys"] if "LOGICAL_PATH" in k]

print()
print(json.dumps(R["identity_consequence"], indent=1))
print("logicalPath fault keys:", R["internal_fault_keys_for_logicalPath"])
json.dump(R, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeB.json', 'w'), indent=1)
