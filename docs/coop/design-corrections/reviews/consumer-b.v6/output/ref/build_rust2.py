"""Vector group B2: the complete minimal positive Rust Run, the clones
ownership disclosure derivation, and the Rust hidden/mismatched-input refusals."""
import sys, os, json, hashlib, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osip import *
from model import *
from build_ts import S, V, PROJECT_ID, blob, inv, closure, EVAL_CID
from build_ts2 import (CAP_MANIFEST, CAP_BYTES, CAP_ID, CAP_BYTES_DIGEST, NA_RC,
                       CW_CLOSED, CapRegistry)
from build_ts3 import LEVEL_SPEC
from build_rust import *
import build_rust as R

RSU = "native.semantic-universe.rust.v2"
UA = UNIV_A_ID.split(":")[1]

# ---------------------------------------------------- Rust snapshot and Plan
RS_SEM_CONFIG = {"analysis": {"profileId": "default",
                              "capabilities": ["clones-fact", "inventory", "syntax"],
                              "budget": {"unit": "work-units", "limit": 500000}},
                 "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
RS_CFG_D = S.put_record(RS_SEM_CONFIG, "semantic-configuration rust")
RS_SCOPE_DESC = {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [],
                 "excludedPathPrefixes": sorted([".git", "crates/core/target",
                                                 "crates/legacy/target", "target",
                                                 "tool#1/target"], key=lambda s: C(s))}
RS_SCOPE_D = S.put_record(RS_SCOPE_DESC, "scope-descriptor rust")
RS_INV_D = S.put_record(R2_INV, "source-inventory rust")
RS_VCS = {"schemaVersion": 2, "kind": "git", "commitId": "9a" * 20, "dirty": False,
          "sourceInventoryDigest": RS_INV_D}
RS_VCS_D = S.put_record(RS_VCS, "vcs-observation rust")
RS_SNAP = {"schemaVersion": 2, "projectId": PROJECT_ID, "sourceInventory": R2_INV,
           "resolvedConfigDigest": RS_CFG_D, "scopeDigest": RS_SCOPE_D,
           "vcsDigest": RS_VCS_D}
RS_SNAP_ID = S.mint("snapshot", RS_SNAP)

RS_SPEC = {"schemaVersion": 2,
           "requestedCapabilities": sorted([
               {"capabilityId": "inventory", "languageMode": "rust-cargo",
                "workspaceRoot": ".", "required": True},
               {"capabilityId": "clones-fact", "languageMode": "rust-cargo",
                "workspaceRoot": ".", "required": True}], key=lambda r: C(r)),
           "policyPackIds": ["pack.default"], "parameters": []}
RS_SPEC_D = S.put_record(RS_SPEC, "analysis-spec rust")
RS_GRANT = {"schemaVersion": 2, "projectId": PROJECT_ID,
            "principals": [{"kind": "first-party", "closureId": RS_PROV_CID,
                            "ownerSourceDigest": None}],
            "analysisOperations": sorted(["read-source", "native-analysis"], key=lambda s: C(s)),
            "scopeDigest": RS_SCOPE_D}
RS_GRANT_D = S.put_record(RS_GRANT, "semantic-grant rust")
RS_POLICY = {"schemaVersion": 1, "policyId": "pack.default", "rules": []}
RS_POLICY_D = S.put_record(RS_POLICY, "PolicyDocumentV1 rust")
RS_WAIVERS = {"schemaVersion": 1, "waivers": []}
RS_WAIVER_D = S.put_record(RS_WAIVERS, "WaiverSetV1 rust")
RS_PROG = {"schemaVersion": 1, "policyDigest": RS_POLICY_D, "rules": []}
RS_PROG_D = S.put_record(RS_PROG, "RuleProgramV1 rust")

RS_PLAN = {"schemaVersion": 2, "snapshotId": RS_SNAP_ID, "capabilityManifestId": CAP_ID,
           "semanticClosures": sorted([RS_PROV_CID, EVAL_CID], key=lambda s: C(s)),
           "analysisSpecDigest": RS_SPEC_D, "resolvedConfigDigest": RS_CFG_D,
           "nativeContextDigests": [RS_ADM["contextId"].split(":")[1]],
           "importIds": [], "policyDigest": RS_POLICY_D, "waiverDigest": RS_WAIVER_D,
           "scopeDigest": RS_SCOPE_D, "budget": RS_SEM_CONFIG["analysis"]["budget"],
           "semanticGrantDigest": RS_GRANT_D,
           "capabilityManifestBytesDigest": CAP_BYTES_DIGEST}
RS_PLAN_ID = S.mint("plan", RS_PLAN)


def rs_scope(relation, rung, subjects):
    rc0(relation, rung)
    subs = sorted(set(subjects), key=lambda s: C(s))
    check_order(subs, "canonical-set", "subjects")
    d = {"schemaVersion": 2, "snapshotId": RS_SNAP_ID, "sourceUniverse": UA,
         "targetUniverse": UA, "relation": relation, "resolution": rung,
         "enumeratorClosure": RS_PROV_CID, "subjects": subs}
    sid = S.mint("subject-scope", d)
    return d, sid, "sha256:" + sid.split(":")[1]


def rs_fact(relation, rung, payload, anchors):
    rc0(relation, rung)
    r = RELREG[relation]
    law = r["anchorLaw"]
    n = len(anchors)
    if law["class"] == "inventory" and n != 0:
        raise Refuse("FACT_ANCHOR_CARDINALITY", relation)
    if law["class"] == "body-identity" and n != 1:
        raise Refuse("FACT_ANCHOR_CARDINALITY", relation)
    if law["class"] == "source-text" and n < 1:
        raise Refuse("FACT_ANCHOR_CARDINALITY", relation)
    pd = S.put_record(payload, "relation payload " + relation)
    f = {"schemaVersion": 2, "snapshotId": RS_SNAP_ID, "relation": relation,
         "resolution": rung, "sourceUniverse": UA, "targetUniverse": UA,
         "producerClosure": RS_PROV_CID, "payloadSchemaDigest": RELATION_SCHEMA_DIGEST,
         "payloadDigest": pd, "anchors": sorted(anchors, key=lambda a: C(a)),
         "confidenceMillionths": 1000000}
    return f, S.mint("fact", f), payload


def rs_coverage(scope_id, relation, rung, e, commitment, n):
    payload = {"schemaVersion": 3,
               "key": {"relation": relation, "resolution": rung, "sourceUniverse": UA,
                       "targetUniverse": UA, "subjectScopeCommitment": commitment},
               "entry": e}
    rc1(relation, rung, e)
    pd = S.put_record(payload, "CoverageResultV3 rust")
    cov = {"schemaVersion": 2, "scopeId": scope_id,
           "payloadSchemaDigest": COVERAGE_SCHEMA_DIGEST, "payloadDigest": pd}
    return payload, cov, S.mint("coverage", cov)


def rs_entry(relation, rung, cov, commitment, n, deficiency=None, cause=None):
    return {"relation": relation, "resolution": rung, "coverage": cov,
            "examinedUniverse": {"subjectScopeCommitment": commitment, "subjectCount": n},
            "resolutionCompleteness": dict(NA_RC), "closedWorld": dict(CW_CLOSED),
            "derivationKinds": [], "confidenceMillionths": 1000000,
            "deficiency": deficiency, "nativeCause": cause}


# --- inventory facts for every inventoried path (file@enumerated is TOTAL)
rs_file_facts, rs_file_ids = [], []
for row in R2_INV:
    f, fid, pl = rs_fact("file", "enumerated",
                         {"path": row["path"], "contentSha256": row["sha256"],
                          "byteLength": row["bytes"]}, [])
    rs_file_facts.append((f, fid, pl)); rs_file_ids.append(fid)
RS_FILE_SCOPE, RS_FILE_SID, RS_FILE_COMMIT = rs_scope(
    "file", "enumerated", [r["path"] for r in R2_INV])
RS_FILE_ENTRY = rs_entry("file", "enumerated", "complete", RS_FILE_COMMIT, len(R2_INV))
_, RS_FILE_COV, RS_FILE_COV_ID = rs_coverage(RS_FILE_SID, "file", "enumerated",
                                             RS_FILE_ENTRY, RS_FILE_COMMIT, len(R2_INV))

# --- package facts (three manifests declare packages; the workspace root does not)
rs_pkg = []
for mp, name in (("crates/core/Cargo.toml", "core"), ("crates/legacy/Cargo.toml", "legacy"),
                 ("tool#1/Cargo.toml", "tool1")):
    f, fid, pl = rs_fact("package", "manifest-declared",
                         {"manifestPath": mp, "packageName": name, "packageVersion": "0.1.0"}, [])
    rs_pkg.append((f, fid, pl))
RS_PKG_SCOPE, RS_PKG_SID, RS_PKG_COMMIT = rs_scope("package", "manifest-declared",
                                                   ["core", "legacy", "tool1"])
RS_PKG_ENTRY = rs_entry("package", "manifest-declared", "complete", RS_PKG_COMMIT, 3)
_, RS_PKG_COV, RS_PKG_COV_ID = rs_coverage(RS_PKG_SID, "package", "manifest-declared",
                                           RS_PKG_ENTRY, RS_PKG_COMMIT, 3)

# --- clones facts under selection A (2021) and the tool1 body (2024)
RS_CLONE_PATHS = ["crates/core/src/shared.rs", "tool#1/src/main.rs"]
rs_clone = []
for p, span in ((RS_CLONE_PATHS[0], SHARED_SPAN),
                (RS_CLONE_PATHS[1], (10, len('fn main() { let z = 3; println!("{}", z); }')))):
    bid, blv, fr = rs_body(UNIV_A, OWN_A, p, span)
    row = R2_MAP[p]
    f, fid, pl = rs_fact("clones", "normalized-body-hash",
                         {"bodyIdentity": bid, "normalisationLevel": "L0-verbatim",
                          "normalisationVersion": LEVEL_SPEC["L0-verbatim"]},
                         [{"path": p, "blobDigest": row["sha256"],
                           "startByte": span[0], "endByte": span[1]}])
    rs_clone.append((f, fid, pl, blv))
RS_CL_SCOPE, RS_CL_SID, RS_CL_COMMIT = rs_scope("clones", "normalized-body-hash", RS_CLONE_PATHS)
RS_CL_ENTRY = rs_entry("clones", "normalized-body-hash", "complete", RS_CL_COMMIT, 2)
_, RS_CL_COV, RS_CL_COV_ID = rs_coverage(RS_CL_SID, "clones", "normalized-body-hash",
                                         RS_CL_ENTRY, RS_CL_COMMIT, 2)

# --- an L1 normalized-level clone body (retained token stream, not recomputable)
TOKENS = [("kw", "let"), ("ident", "x"), ("punct", "="), ("num", "1"), ("punct", ";")]
_blv_l1 = body_language_version(RSU, RS_CTX, UNIV_A, "crates/core/src/shared.rs", OWN_A)
BID_L1, FR_L1 = body_identity("L1-lexical", LEVEL_SPEC["L1-lexical"],
                              _blv_l1["languageId"], _blv_l1, token_stream_payload(TOKENS))
S.put_blob(FR_L1, "body frame L1 rust")
V["RS-CLONE-L1-normalized-level-retained-custody"] = {
    "level": "L1-lexical",
    "levelSpecificationDigest": LEVEL_SPEC["L1-lexical"],
    "levelSpecificationRetained": S.has(LEVEL_SPEC["L1-lexical"]),
    "tokenStreamFraming": "u32be token_count || (u16be kind_len||kind || u32be val_len||val)*",
    "tokenStreamHex": token_stream_payload(TOKENS).hex(),
    "bodyIdentity": BID_L1,
    "differsFromL0": BID_L1 != rs_clone[0][2]["bodyIdentity"],
    "hostCannotRecomputeAtL1": True,
    "whatIsRequiredInstead": "exact retained preimage custody + framed-identity check + "
                             "well-formed stream framing; this qualifies no normalizer",
    "levelSpecificationCustody": "normalisationVersion is the RAW SHA-256 of the exact "
                                 "retained canonical level-specification bytes; a human "
                                 "version label is insufficient and an opaque caller hash "
                                 "is inadmissible."}

# ---------------------------------------------- Rust view / proof / seal / Run
RS_VIEW = {"schemaVersion": 2, "planId": RS_PLAN_ID,
           "scopeIds": sorted([RS_FILE_SID, RS_PKG_SID, RS_CL_SID], key=lambda s: C(s)),
           "facts": sorted(rs_file_ids + [x[1] for x in rs_pkg] + [x[1] for x in rs_clone],
                           key=lambda s: C(s)),
           "coverageIds": sorted([RS_FILE_COV_ID, RS_PKG_COV_ID, RS_CL_COV_ID], key=lambda s: C(s)),
           "producerClosure": RS_PROV_CID,
           "schemaDigests": sorted([RELATION_SCHEMA_DIGEST, COVERAGE_SCHEMA_DIGEST],
                                   key=lambda s: C(s))}
RS_VIEW_ID = S.mint("view", RS_VIEW)
RS_STAGE = {"schemaVersion": 2, "planId": RS_PLAN_ID, "producerClosure": RS_PROV_CID,
            "operation": "native.analyze", "parameters": [],
            "outputDomains": sorted(["coverage", "fact", "subject-scope", "view"], key=lambda s: C(s)),
            "outputSchemaDigest": COVERAGE_SCHEMA_DIGEST}
RS_STAGE_D = S.put_record(RS_STAGE, "stage-spec rust")
RS_EXEC = {"schemaVersion": 2, "planId": RS_PLAN_ID,
           "stages": [{"ordinal": 0, "stageSpecDigest": RS_STAGE_D, "requires": [],
                       "outputDomains": RS_STAGE["outputDomains"]}]}
RS_EXEC_ID = S.mint("execution-plan", RS_EXEC)
RS_REFS = sorted([{"domain": "view", "digest": RS_VIEW_ID.split(":")[1]},
                  {"domain": "coverage", "digest": RS_FILE_COV_ID.split(":")[1]},
                  {"domain": "coverage", "digest": RS_PKG_COV_ID.split(":")[1]},
                  {"domain": "coverage", "digest": RS_CL_COV_ID.split(":")[1]},
                  {"domain": "rule-program", "digest": RS_PROG_D},
                  {"domain": "policy", "digest": RS_POLICY_D},
                  {"domain": "waiver", "digest": RS_WAIVER_D},
                  {"domain": "native-context", "digest": RS_ADM["contextId"].split(":")[1]},
                  {"domain": "analysis-spec", "digest": RS_SPEC_D},
                  {"domain": "capability-manifest", "digest": CAP_ID},
                  {"domain": "schema", "digest": RELATION_SCHEMA_DIGEST},
                  {"domain": "schema", "digest": COVERAGE_SCHEMA_DIGEST}], key=lambda r: C(r))
RS_PROOF = {"schemaVersion": 2, "planId": RS_PLAN_ID, "executionPlanId": RS_EXEC_ID,
            "evaluatorClosure": EVAL_CID, "ruleProgramDigest": RS_PROG_D,
            "evaluationInputRefs": RS_REFS, "predicateProofs": [], "findingIds": [],
            "verdict": "pass"}
RS_PROOF_ID = S.mint("proof-bundle", RS_PROOF)
RS_EVID = {"schemaVersion": 2, "planId": RS_PLAN_ID, "viewIds": [RS_VIEW_ID],
           "coverageIds": RS_VIEW["coverageIds"], "importIds": [], "findingIds": [],
           "proofBundleId": RS_PROOF_ID}
RS_EVID_ID = S.mint("semantic-evidence", RS_EVID)
RS_SEAL = {"schemaVersion": 2, "planId": RS_PLAN_ID, "executionPlanId": RS_EXEC_ID,
           "evidenceId": RS_EVID_ID, "evaluatorClosure": EVAL_CID,
           "policyDigest": RS_POLICY_D, "proofBundleId": RS_PROOF_ID, "verdict": "pass"}
RS_SEAL_ID = S.mint("evaluation-seal", RS_SEAL)
RS_RUN = {"schemaVersion": 2, "projectId": PROJECT_ID, "snapshotId": RS_SNAP_ID,
          "planId": RS_PLAN_ID, "evidenceId": RS_EVID_ID, "evaluationSealId": RS_SEAL_ID,
          "capabilityManifestId": CAP_ID}
RS_RUN_ID = S.mint("run", RS_RUN)

V["RS-RUN-1-complete-minimal-positive-rust-run"] = {
    "snapshotId": RS_SNAP_ID, "planId": RS_PLAN_ID,
    "nativeContextDigests": RS_PLAN["nativeContextDigests"],
    "nativeContextDomain": "native.context.rust.v2",
    "sourceUniverse": UA, "universeDomain": RSU,
    "rustUniversePathIsActuallyExercised": True,
    "nestedRetainedRecords": {
        "DependencySourceSetV1": DEPSET_ID, "UnifiedFeaturesV1": UNIFIED_ID,
        "DependencyFileManifestV1": DEP_MANIFEST_ID,
        "CargoConfigProjectionV2 (H suffix)": PROJECTION_H,
        "SourceUnitOwnershipV1": OWN_A_ID, "PreparedOutputSetV3": None},
    "scopes": {"file@enumerated": RS_FILE_SID, "package@manifest-declared": RS_PKG_SID,
               "clones@normalized-body-hash": RS_CL_SID},
    "coverageIds": RS_VIEW["coverageIds"], "factCount": len(RS_VIEW["facts"]),
    "viewId": RS_VIEW_ID, "executionPlanId": RS_EXEC_ID, "proofBundleId": RS_PROOF_ID,
    "evidenceId": RS_EVID_ID, "evaluationSealId": RS_SEAL_ID, "runId": RS_RUN_ID,
    "mixedEditionBodiesInOneUniverse": {
        "crates/core/src/shared.rs": rs_clone[0][3]["dialect"],
        "tool#1/src/main.rs": rs_clone[1][3]["dialect"]},
    "verdict": "pass"}

# --------------------------- clones ownership DISCLOSURE derivation (CB3-MUST-5)
OWNERSHIP_CAUSE = {"BODY_LANGUAGE_OWNERSHIP_REQUIRED": "body-language-ownership-missing",
                   "BODY_LANGUAGE_OWNER_UNENUMERATED": "body-language-owner-unenumerated",
                   "BODY_LANGUAGE_OWNER_AMBIGUOUS": "body-language-owner-ambiguous"}
NO_CAUSE = {"BODY_LANGUAGE_OWNER_NOT_COMPILED", "BODY_LANGUAGE_OWNER_NOT_SELECTED"}


def owed_clone_coverage(universe, own, subjects):
    """Derive the OWED (deficiency, nativeCause) from the COMMITTED ownership
    record and THIS scope's subjects, in the selection law's own order."""
    if own is None:
        k = "BODY_LANGUAGE_OWNERSHIP_REQUIRED"
        return ("unknown", "input-closure-incomplete", OWNERSHIP_CAUSE[k], k)
    if own["enumeration"] == "partial":
        k = "BODY_LANGUAGE_OWNER_UNENUMERATED"
        return ("unknown", "input-closure-incomplete", OWNERSHIP_CAUSE[k], k)
    for s in subjects:
        try:
            rust_dialect(own, universe["edition"], s)
        except Refuse as e:
            if e.code == "BODY_LANGUAGE_OWNER_AMBIGUOUS":
                return ("unknown", "input-closure-incomplete",
                        OWNERSHIP_CAUSE[e.code], e.code)
            if e.code in NO_CAUSE:
                continue          # per-body refusal, COMPATIBLE with coverage complete
            raise
    return ("complete", None, None, None)


CASES = {}
for label, univ, own, subs in [
    ("ordinary-selection", UNIV_A, OWN_A, RS_CLONE_PATHS),
    ("partial-enumeration", UNIV_E, OWN_E, RS_CLONE_PATHS),
    ("no-committed-ownership", UNIV_F, None, RS_CLONE_PATHS),
    ("selected-owners-disagree", UNIV_D, OWN_D, ["crates/core/src/shared.rs"]),
    ("deliberately-excluded-owner", UNIV_D2, OWN_D2, ["tool#1/src/main.rs"]),
]:
    cov, dfc, cause, key = owed_clone_coverage(univ, own, subs)
    CASES[label] = {"coverage": cov, "deficiency": dfc, "nativeCause": cause,
                    "selectionLawKey": key,
                    "d9Class": ("indeterminate (3) / VERDICT.INDETERMINATE"
                                if dfc else "no deficiency"),
                    "mintsBodyIdentity": cov == "complete"}
V["RS-CLONE-OWNERSHIP-DISCLOSURE"] = CASES

# empty clone view under PARTIAL ownership must NOT claim complete Coverage
EMPTY_SCOPE, EMPTY_SID, EMPTY_COMMIT = rs_scope("clones", "normalized-body-hash",
                                                ["crates/core/src/shared.rs"])
_cov, _def, _cause, _key = owed_clone_coverage(UNIV_E, OWN_E, ["crates/core/src/shared.rs"])
EMPTY_ENTRY = rs_entry("clones", "normalized-body-hash", _cov, EMPTY_COMMIT, 1, _def, _cause)
_, EMPTY_COV, EMPTY_COV_ID = rs_coverage(EMPTY_SID, "clones", "normalized-body-hash",
                                         EMPTY_ENTRY, EMPTY_COMMIT, 1)
_neg = {}


def _try(name, fn):
    try:
        fn(); _neg[name] = "NOT-REFUSED (defect)"
    except Refuse as e:
        _neg[name] = str(e)


def _prereq(entry_, universe, own, subs, refusal_prefix="COVERAGE_DIALECT"):
    cov, dfc, cause, key = owed_clone_coverage(universe, own, subs)
    if entry_["coverage"] != cov:
        raise Refuse(refusal_prefix + "_PREREQUISITE",
                     f"claimed {entry_['coverage']}, owed {cov}")
    if cov == "unknown" and entry_["deficiency"] is None:
        raise Refuse(refusal_prefix + "_UNDISCLOSED", "")
    if entry_["deficiency"] != dfc:
        raise Refuse(refusal_prefix + "_DEFICIENCY_MISMATCH",
                     f"{entry_['deficiency']} != {dfc}")
    if entry_["nativeCause"] != cause:
        raise Refuse(refusal_prefix + "_CAUSE_MISMATCH",
                     f"{entry_['nativeCause']} != {cause}")
    return True


_prereq(EMPTY_ENTRY, UNIV_E, OWN_E, ["crates/core/src/shared.rs"])
_try("RS-N7-empty-clone-view-claiming-COMPLETE-under-partial-ownership",
     lambda: _prereq(rs_entry("clones", "normalized-body-hash", "complete", EMPTY_COMMIT, 1),
                     UNIV_E, OWN_E, ["crates/core/src/shared.rs"]))
_try("RS-N8-unknown-with-a-NULL-deficiency-is-an-undisclosed-gap",
     lambda: _prereq(rs_entry("clones", "normalized-body-hash", "unknown", EMPTY_COMMIT, 1),
                     UNIV_E, OWN_E, ["crates/core/src/shared.rs"]))
_try("RS-N9-unrelated-but-schema-valid-deficiency",
     lambda: _prereq(rs_entry("clones", "normalized-body-hash", "unknown", EMPTY_COMMIT, 1,
                              "budget-exhausted", None),
                     UNIV_E, OWN_E, ["crates/core/src/shared.rs"]))
_try("RS-N10-right-deficiency-with-a-NULL-cause",
     lambda: _prereq(rs_entry("clones", "normalized-body-hash", "unknown", EMPTY_COMMIT, 1,
                              "input-closure-incomplete", None),
                     UNIV_E, OWN_E, ["crates/core/src/shared.rs"]))
_try("RS-N11-right-deficiency-with-the-WRONG-ownership-cause",
     lambda: _prereq(rs_entry("clones", "normalized-body-hash", "unknown", EMPTY_COMMIT, 1,
                              "input-closure-incomplete", "body-language-owner-ambiguous"),
                     UNIV_E, OWN_E, ["crates/core/src/shared.rs"]))

# -------------------------------- Rust hidden / mismatched input refusals
_try("RS-N12-crateRootPath-not-in-the-analysed-snapshot",
     lambda: bind_rust_universe(dict(UNIV_A, crateRootPaths=sorted(
         UNIV_A["crateRootPaths"] + ["crates/ghost/src/lib.rs"], key=lambda p: p.encode())),
         RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_A), R2_INV))
_try("RS-N13-lockfile-bytes-that-are-not-the-inventoried-ones",
     lambda: bind_rust_universe(dict(UNIV_A, lockfileIdentity=dict(LOCKID, contentSha256="00" * 32)),
         RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_A), R2_INV))
_try("RS-N14-cfgSet-dropping-a-base-cfg",
     lambda: bind_rust_universe(dict(UNIV_A, cfgSets=[{"cfgSetId": "primary", "cfg": ["unix"]}]),
         RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_A), R2_INV))
_try("RS-N15-duplicate-cfgSetId",
     lambda: bind_rust_universe(dict(UNIV_A, cfgSets=[UNIV_A["cfgSets"][0], UNIV_A["cfgSets"][0]]),
         RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_A), R2_INV))
_try("RS-N16-universe-bound-without-the-retained-nested-input-records",
     lambda: bind_rust_universe(UNIV_A, RS_ADM, RS_CTX, {"sourceUnitOwnership": OWN_A}, R2_INV))
_try("RS-N17-prepared-output-set-retained-but-selected-by-no-universe",
     lambda: bind_rust_universe(UNIV_A, RS_ADM, RS_CTX,
         dict(RETAINED, sourceUnitOwnership=OWN_A,
              preparedOutputSet={"schemaVersion": 3}), R2_INV))
_try("RS-N18-unified-features-computed-for-another-targetTriple",
     lambda: bind_rust_universe(UNIV_A, RS_ADM, RS_CTX,
         dict(RETAINED, sourceUnitOwnership=OWN_A,
              unifiedFeatures=dict(UNIFIED, targetTriple="x86_64-unknown-linux-gnu")), R2_INV))
_try("RS-N19-configProjectionSha256-carrying-the-raw-FILE-digest-instead-of-the-H-suffix",
     lambda: bind_rust_universe(dict(UNIV_A, configProjectionSha256=PROJECTION["projectionSha256"]),
         RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_A), R2_INV))
_try("RS-N20-configProjectionSha256-carrying-raw-SHA256-of-C(record)",
     lambda: bind_rust_universe(dict(UNIV_A, configProjectionSha256=raw(PROJECTION)),
         RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=OWN_A), R2_INV))
_try("RS-N21-ownership-unit-id-not-derived-from-its-own-four-field-preimage",
     lambda: bind_rust_universe(
         dict(UNIV_A, sourceUnitOwnershipId="sha256:" + S.put_framed(
             "native.source-unit-ownership.v1",
             dict(OWN_A, units=sorted([dict(u, unitId="sha256:" + "00" * 32) if u["unitId"] == U_TOOL1_BIN else u
                                       for u in OWN_A["units"]], key=lambda x: x["unitId"])))),
         RS_ADM, RS_CTX, dict(RETAINED, sourceUnitOwnership=dict(
             OWN_A, units=sorted([dict(u, unitId="sha256:" + "00" * 32) if u["unitId"] == U_TOOL1_BIN else u
                                  for u in OWN_A["units"]], key=lambda x: x["unitId"]))), R2_INV))
_try("RS-N22-tool-digest-outside-the-signed-closure-tree",
     lambda: admit_rust_context(dict(RS_CTX, toolClosure=dict(RS_CTX["toolClosure"],
                                                              linker="99" * 32)), R2_INV))
_try("RS-N23-rustc-version-not-from-the-admitted-closure-manifest",
     lambda: admit_rust_context(dict(RS_CTX, toolchain=dict(RS_CTX["toolchain"],
                                                            rustcVersion="1.84.0")), R2_INV))
_try("RS-N24-replaced-cargo-config-outside-the-analysed-snapshot",
     lambda: admit_rust_context(dict(RS_CTX, configProjection=dict(
         PROJECTION, replacedSnapshotConfigs=[".cargo/config.toml", "hidden/.cargo/config.toml"])),
         R2_INV))
V["RS-NEGATIVES"] = _neg
