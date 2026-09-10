#!/usr/bin/env python
"""P4 - M-1: subjectScopeCommitment producing recipe, scope2 join, and the two
adversarial properties the prompt names (no trusted claimant digest, no circular
universe authority).

Independent oracle: I recompute the commitment from the PROSE recipe alone using
raw hashlib + my own reading of the H frame, and compare to the model. Then I
attack the boundary.
"""
import hashlib, importlib.util, json, sys
from pathlib import Path

DC = Path("/tmp/opensip-design-corrections/candidate-subject.v6/docs/coop/design-corrections")


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


sys.path.insert(0, str(DC / "foundation"))
N = load("nem", DC / "native/native_evidence_model.v2.py")
C = N.C

out = {"probe": "P4-M1-subject-scope-commitment"}

SNAP = "snapshot2:" + "a" * 64
SRC_U, TGT_U = "b" * 64, "c" * 64
ENUM = "closure2:" + "d" * 64
SUBJECTS = ["src/z.ts#zed", "src/a.ts#alpha", "src/m.ts#mid"]

desc = N.subject_scope_descriptor(SNAP, "references", "resolved-binding",
                                  SRC_U, TGT_U, ENUM, SUBJECTS)
model = N.subject_scope_commitment(desc)


# --- independent H frame implemented from identity-and-evidence.md prose ------
def my_canonical(v):
    """Minimal canonical encoder for this descriptor shape (strings/ints/lists/dicts)."""
    if isinstance(v, dict):
        items = sorted(v.items(), key=lambda kv: kv[0].encode("utf-8"))
        return b"{" + b",".join(my_canonical(k) + b":" + my_canonical(x)
                                for k, x in items) + b"}"
    if isinstance(v, list):
        return b"[" + b",".join(my_canonical(x) for x in v) + b"]"
    if isinstance(v, bool):
        return b"true" if v else b"false"
    if isinstance(v, int):
        return str(v).encode()
    if isinstance(v, str):
        esc = v.replace("\\", "\\\\").replace('"', '\\"')
        return b'"' + esc.encode("utf-8") + b'"'
    raise TypeError(type(v))


def my_H(domain, x):
    c = my_canonical(x)
    return hashlib.sha256(b"opensip.product.v1" + b"\x00" + domain.encode()
                          + b"\x00" + len(c).to_bytes(8, "big") + c).hexdigest()


mine_hex = my_H("subject-scope", desc)
out["independentOracle"] = {
    "myCanonicalBytes": my_canonical(desc).decode()[:220] + "...",
    "myH_subject_scope": mine_hex,
    "modelScopeId": model["scopeId"],
    "modelCommitment": model["subjectScopeCommitment"],
    "recipeReproducesFromProseAlone": model["scopeId"] == "scope2:" + mine_hex,
    "commitmentIsSameDigestAsScope2": model["subjectScopeCommitment"] == "sha256:" + mine_hex,
    "identicalSuffix": model["scopeId"].removeprefix("scope2:")
                       == model["subjectScopeCommitment"].removeprefix("sha256:"),
    "subjectCount": model["subjectCount"],
}

# --- exact enumerated set semantics ------------------------------------------
out["enumeratedSet"] = {
    "storedSubjectsAreCanonicalSetOrdered":
        desc["subjects"] == sorted(SUBJECTS, key=C.canonical),
    "inputOrderIrrelevant":
        N.subject_scope_commitment(N.subject_scope_descriptor(
            SNAP, "references", "resolved-binding", SRC_U, TGT_U, ENUM,
            list(reversed(SUBJECTS))))["subjectScopeCommitment"]
        == model["subjectScopeCommitment"],
}
try:
    N.subject_scope_descriptor(SNAP, "references", "resolved-binding", SRC_U, TGT_U,
                               ENUM, SUBJECTS + [SUBJECTS[0]])
    out["enumeratedSet"]["duplicateRefuses"] = False
except Exception as e:
    out["enumeratedSet"]["duplicateRefuses"] = True
    out["enumeratedSet"]["duplicateError"] = str(e)

# binds the snapshot, not only the subject list
alt = N.subject_scope_descriptor("snapshot2:" + "f" * 64, "references",
                                 "resolved-binding", SRC_U, TGT_U, ENUM, SUBJECTS)
out["enumeratedSet"]["bindsSnapshotNotOnlySubjects"] = (
    N.subject_scope_commitment(alt)["subjectScopeCommitment"]
    != model["subjectScopeCommitment"])
# binds the enumerator closure
alt2 = N.subject_scope_descriptor(SNAP, "references", "resolved-binding", SRC_U, TGT_U,
                                  "closure2:" + "e" * 64, SUBJECTS)
out["enumeratedSet"]["bindsEnumeratorClosure"] = (
    N.subject_scope_commitment(alt2)["subjectScopeCommitment"]
    != model["subjectScopeCommitment"])

# --- adversarial: claimant-supplied digest is never authority -----------------
SCHEMA_DIGEST = N.schema_document_digest(N.NATIVE_SCHEMA_DOC)


def coverage_payload(commitment, subject_count, examined_commitment=None):
    ec = examined_commitment if examined_commitment is not None else commitment
    return {
        "schemaVersion": 3,
        "key": {"relation": "references", "resolution": "resolved-binding",
                "sourceUniverse": SRC_U, "targetUniverse": TGT_U,
                "subjectScopeCommitment": commitment},
        "entry": {"relation": "references", "resolution": "resolved-binding",
                  "examinedUniverse": {"subjectScopeCommitment": ec,
                                       "subjectCount": subject_count},
                  "coverage": "complete",
                  "resolutionCompleteness": {"state": "complete", "attempted": True,
                                             "examinedExhaustive": True,
                                             "stageTerminal": "complete",
                                             "unresolvedEdgeCount": 0,
                                             "unresolvedEdgeClasses": []},
                  "closedWorld": {"exportsClosed": "closed", "entryPointsRecognized": "all",
                                  "nonliteralLoading": "none", "externalConsumers": "none-declared",
                                  "dynamicDispatch": "resolved", "deadCodeRepairEligible": True,
                                  "reasons": []},
                  "derivationKinds": ["annotated"], "confidenceMillionths": 1000000,
                  "deficiency": None, "nativeCause": None},
    }


good = N.admit_coverage_result_v3(coverage_payload(model["subjectScopeCommitment"], 3), desc, [])
out["positiveAdmission"] = {"result": good["result"], "coverageId": good.get("coverageId"),
                            "scopeId": good.get("scopeId"),
                            "refusals": good.get("refusals")}

forged = N.admit_coverage_result_v3(
    coverage_payload("sha256:" + "9" * 64, 3), desc, [])
out["claimantChosenCommitmentRefused"] = {
    "result": forged["result"], "refusals": forged.get("refusals")}

narrower = N.admit_coverage_result_v3(
    coverage_payload(model["subjectScopeCommitment"], 2), desc, [])
out["narrowerExaminedPartitionRefused"] = {
    "result": narrower["result"], "refusals": narrower.get("refusals")}

foreign_schema = N.admit_coverage_result_v3(
    coverage_payload(model["subjectScopeCommitment"], 3), desc, [],
    payload_schema_digest="7" * 64)
out["callerChosenSchemaDigestRefused"] = {
    "result": foreign_schema["result"], "refusals": foreign_schema.get("refusals")}

# --- adversarial: no circular universe authority ------------------------------
# The descriptor D must not be reachable from anything that names a scope/coverage/view/run.
sub_scope_schema = None
fnd = json.loads((DC / "foundation/identity-schemas.v2.json").read_text())
sub_scope_schema = fnd["$defs"]["subject-scope"]
out["acyclicity"] = {
    "subjectScopeFields": sorted(sub_scope_schema.get("properties", {}).keys()),
    "namesNoScopeCoverageViewOrRun": not any(
        t in json.dumps(sub_scope_schema).lower()
        for t in ("coverageid", "viewid", "runid", "evidenceid", "sealid")),
}
# universe descriptors must not name a scope/coverage
nat = json.loads((DC / "native/native-evidence.schemas.v2.json").read_text())
for uname in ("TypeScriptUniverseV2ResolvedInputs", "RustUniverseV2ResolvedInputs"):
    u = nat["$defs"].get(uname, {})
    blob = json.dumps(u).lower()
    out["acyclicity"][uname + "_namesNoScopeOrCoverage"] = not any(
        t in blob for t in ("subjectscopecommitment", "coverageid", "scopeid", "viewid", "runid"))


def VIEW(sids,cids):
    return {"schemaVersion":2,"planId":"plan2:"+"a"*64,"scopeIds":sorted(sids),"facts":[],
            "coverageIds":sorted(cids),"producerClosure":"closure2:"+"d"*64,"schemaDigests":[]}
ok_view  = N.coverage_view_use(VIEW([model["scopeId"]],[good["coverageId"]]),[good])
bad_view = N.coverage_view_use(VIEW(["scope2:"+"0"*64],[good["coverageId"]]),[good])
never    = N.coverage_view_use(VIEW([model["scopeId"]],["coverage2:"+"8"*64]),[good])
out["coverageViewUse"]={"inViewAdmits":ok_view["result"],
  "outsideViewRefused":{"result":bad_view["result"],"refusals":bad_view.get("refusals")},
  "neverAdmittedRefused":{"result":never["result"],"refusals":never.get("refusals")}}
import json;print(json.dumps(out,indent=1))
