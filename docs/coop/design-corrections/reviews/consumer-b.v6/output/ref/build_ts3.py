"""Vector group A3: the complete positive TypeScript Run, its clone body
identities (TS body and JS body through the SAME TypeScript engine), the other
three configuration graphs, and the discriminating negative controls."""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osip import *
from model import *
from build_ts import *
from build_ts2 import *
import build_ts2 as B

TSU = "native.semantic-universe.typescript.v2"

# ---------------------------------------------------- level specifications
LEVEL_SPEC = {}
for lvl in ("L0-verbatim", "L1-lexical", "L2-comment-insensitive",
            "L3-identifier-insensitive"):
    body = f"OPENSIP-LEVEL-SPEC/{lvl}/lexical-boundaries+token-kind-registry+directive-classification+transform-order+replacement-bytes".encode()
    LEVEL_SPEC[lvl] = S.put_blob(body, "level-specification " + lvl)

# --------------------------------------------------------------- TS Run facts
SUBJ_PATHS = [r["path"] for r in R1_INV]

file_facts, file_fact_ids = [], []
for row in R1_INV:
    f, fid, pl = fact("file", "enumerated",
                      {"path": row["path"], "contentSha256": row["sha256"],
                       "byteLength": row["bytes"]}, [])
    snapshot_joins(f, pl, R1_INV)
    file_facts.append((f, fid, pl))
    file_fact_ids.append(fid)

FILE_SCOPE, FILE_SCOPE_ID, FILE_COMMIT = subject_scope("file", "enumerated", SUBJ_PATHS)
FILE_ENTRY = entry("file", "enumerated", "complete", commitment=FILE_COMMIT,
                   count=len(SUBJ_PATHS))
FILE_COV_PAYLOAD, FILE_COV, FILE_COV_ID = coverage(
    FILE_SCOPE_ID, "file", "enumerated", FILE_ENTRY, FILE_COMMIT, len(SUBJ_PATHS))


def coverage_inventory_totality(scope, entry_, facts, inventory):
    """file@enumerated is TOTAL over the inventory: a complete result must carry
    a fact for every one of its subjects the snapshot contains, matching on EVERY
    matchOn coordinate (not relation+rung alone)."""
    ct = RELREG[scope["relation"]].get("coverageTotality")
    if not ct or entry_["coverage"] != "complete":
        return True
    inv_paths = {r["path"] for r in inventory}
    have = set()
    for f, fid, pl in facts:
        if all(f[c] == scope[c] for c in ("snapshotId", "relation", "resolution",
                                          "sourceUniverse", "targetUniverse")):
            have.add(pl[ct["pathField"]])
    for s in scope["subjects"]:
        if s in inv_paths and s not in have:
            raise Refuse(ct["refusal"], s)
    return True


coverage_inventory_totality(FILE_SCOPE, FILE_ENTRY, file_facts, R1_INV)

# declares@syntactic over src/util.ts  (source-text class: >= 1 anchor)
util_bytes = open(os.devnull).close() or b'export function helper(){ return 1; }\n'
UTIL_ROW = [r for r in R1_INV if r["path"] == "src/util.ts"][0]
DECL_F, DECL_FID, DECL_PL = fact(
    "declares", "syntactic",
    {"container": "src/util.ts", "declarationKind": "function", "declared": "helper"},
    [{"path": "src/util.ts", "blobDigest": UTIL_ROW["sha256"], "startByte": 0,
      "endByte": UTIL_ROW["bytes"]}])
snapshot_joins(DECL_F, DECL_PL, R1_INV)
DECL_SCOPE, DECL_SCOPE_ID, DECL_COMMIT = subject_scope(
    "declares", "syntactic", ["symbol:src/util.ts#helper"])
DECL_ENTRY = entry("declares", "syntactic", "complete", commitment=DECL_COMMIT, count=1)
_, DECL_COV, DECL_COV_ID = coverage(DECL_SCOPE_ID, "declares", "syntactic",
                                    DECL_ENTRY, DECL_COMMIT, 1)

# clones@normalized-body-hash: TypeScript body under the TypeScript engine
BODY_SPAN = (24, 37)
BODY_BYTES = util_bytes[BODY_SPAN[0]:BODY_SPAN[1]]
BLV_TS = body_language_version(TSU, TS1_CTX, TS1_UNIV, "src/util.ts")
BID_TS_L0, FRAME_TS_L0 = body_identity("L0-verbatim", LEVEL_SPEC["L0-verbatim"],
                                       BLV_TS["languageId"], BLV_TS,
                                       l0_payload(BODY_BYTES))
S.put_blob(FRAME_TS_L0, "body-identity frame L0 ts")
CL_F, CL_FID, CL_PL = fact(
    "clones", "normalized-body-hash",
    {"bodyIdentity": BID_TS_L0, "normalisationLevel": "L0-verbatim",
     "normalisationVersion": LEVEL_SPEC["L0-verbatim"]},
    [{"path": "src/util.ts", "blobDigest": UTIL_ROW["sha256"],
      "startByte": BODY_SPAN[0], "endByte": BODY_SPAN[1]}])
snapshot_joins(CL_F, CL_PL, R1_INV)
CL_SCOPE, CL_SCOPE_ID, CL_COMMIT = subject_scope("clones", "normalized-body-hash",
                                                 ["src/util.ts"])
CL_ENTRY = entry("clones", "normalized-body-hash", "complete", commitment=CL_COMMIT, count=1)
_, CL_COV, CL_COV_ID = coverage(CL_SCOPE_ID, "clones", "normalized-body-hash",
                                CL_ENTRY, CL_COMMIT, 1)


def body_identity_join(f, payload, inventory, universe_domain, context, universe,
                       ownership=None):
    """The clones bodyIdentityJoin, re-derived at closure: the frame is fetched,
    re-hashed, parsed and every component joined to something already admitted."""
    law = RELREG["clones"]["bodyIdentityJoin"]
    if len(f["anchors"]) != law["anchorCardinality"]:
        raise Refuse("FACT_ANCHOR_CARDINALITY", "clones")
    if law["anchorCardinality"] != RELREG["clones"]["anchorLaw"]["cardinality"]:
        raise Refuse("RELATION_ANCHOR_LAW_DRIFT", "clones")
    hexid = payload["bodyIdentity"].split(":")[1]
    if not S.has(hexid):
        raise Refuse("EVIDENCE_UNAVAILABLE", hexid)
    fr = S.cas[hexid]
    if hashlib.sha256(fr).hexdigest() != hexid:
        raise Refuse("BODY_FRAME_DIGEST", hexid)
    # parse the framed preimage
    i = 0

    def take_u8():
        nonlocal i
        n = fr[i]; i += 1
        v = fr[i:i + n]; i += n
        return v
    tag = take_u8()
    if tag != b"opensip.fact-identity.v1":
        raise Refuse("BODY_FRAME_DOMAIN_TAG", tag.decode("latin1"))
    level_id = take_u8().decode()
    level_ver = take_u8()
    lang_id = take_u8().decode()
    lang_ver = take_u8()
    import struct as _s
    plen = _s.unpack(">I", fr[i:i + 4])[0]; i += 4
    pay = fr[i:i + plen]; i += plen
    if i != len(fr):
        raise Refuse("BODY_FRAME_TRAILING_BYTES", str(len(fr) - i))
    if level_id != payload["normalisationLevel"]:
        raise Refuse("BODY_FRAME_LEVEL_MISMATCH", level_id)
    if level_ver != bytes.fromhex(payload["normalisationVersion"]):
        raise Refuse("BODY_FRAME_LEVEL_VERSION_MISMATCH", level_ver.hex())
    if not S.has(payload["normalisationVersion"]):
        raise Refuse("EVIDENCE_UNAVAILABLE", "level-specification")
    a = f["anchors"][0]
    expect_lang = body_language_id(universe_domain, a["path"])
    if lang_id != expect_lang:
        raise Refuse("BODY_FRAME_LANGUAGE_MISMATCH", f"{lang_id}!={expect_lang}")
    if lang_id not in UNIVROWS[universe_domain]["languageVersionBinding"]["bodyLanguages"]:
        raise Refuse("BODY_FRAME_LANGUAGE_NOT_PRODUCED_BY_THIS_UNIVERSE", lang_id)
    blv = body_language_version(universe_domain, context, universe, a["path"], ownership)
    if lang_ver != hashlib.sha256(C(blv)).digest():
        raise Refuse("BODY_FRAME_LANGUAGE_VERSION_MISMATCH", lang_ver.hex())
    if level_id == "L0-verbatim":
        src = S.cas[a["blobDigest"]]
        span = src[a["startByte"]:a["endByte"]]
        if pay != l0_payload(span):
            raise Refuse("BODY_L0_PAYLOAD_NOT_THE_ANCHOR_SPAN", "")
    return {"levelId": level_id, "languageId": lang_id, "blv": blv,
            "payloadLen": plen, "l0InnerLen": (_s.unpack(">I", pay[:4])[0]
                                               if level_id == "L0-verbatim" else None)}


TS_CLONE_JOIN = body_identity_join(CL_F, CL_PL, R1_INV, TSU, TS1_CTX, TS1_UNIV)

V["TS-CLONE-1-typescript-body-L0-double-length-prefix"] = {
    "anchor": {"path": "src/util.ts", "startByte": BODY_SPAN[0], "endByte": BODY_SPAN[1]},
    "spanBytes": BODY_BYTES.decode(),
    "rawByteLen": len(BODY_BYTES),
    "l0PayloadHex": l0_payload(BODY_BYTES).hex(),
    "outerFrameComponentHex": (len(l0_payload(BODY_BYTES)).to_bytes(4, "big")
                               + l0_payload(BODY_BYTES)).hex(),
    "payloadLenEqualsRawPlus4": TS_CLONE_JOIN["payloadLen"] == len(BODY_BYTES) + 4,
    "bodyLanguageVersionRecord": BLV_TS,
    "languageVersionRaw32Hex": hashlib.sha256(C(BLV_TS)).hexdigest(),
    "bodyIdentity": BID_TS_L0,
    "framePreimageHex": FRAME_TS_L0.hex(),
    "note": "Reading the span bytes AS the payload (single prefix) yields a different "
            "identity; identity sec.3 names which of the two grammatical readings is admitted."}

# NEGATIVE: the single-prefix reading
_wrong = body_frame("L0-verbatim", bytes.fromhex(LEVEL_SPEC["L0-verbatim"]),
                    BLV_TS["languageId"], hashlib.sha256(C(BLV_TS)).digest(), BODY_BYTES)
V["TS-CLONE-N1-single-length-prefix-reading-is-a-different-identity"] = {
    "wrongIdentity": "sha256:" + hashlib.sha256(_wrong).hexdigest(),
    "differsFromAdmitted": hashlib.sha256(_wrong).hexdigest() != BID_TS_L0.split(":")[1]}

# --------------------------------------------------------- view / proof / run
VIEW = {"schemaVersion": 2, "planId": PLAN_ID,
        "scopeIds": sorted([FILE_SCOPE_ID, DECL_SCOPE_ID, CL_SCOPE_ID], key=lambda s: C(s)),
        "facts": sorted(file_fact_ids + [DECL_FID, CL_FID], key=lambda s: C(s)),
        "coverageIds": sorted([FILE_COV_ID, DECL_COV_ID, CL_COV_ID], key=lambda s: C(s)),
        "producerClosure": TS_PROV_CID,
        "schemaDigests": sorted([RELATION_SCHEMA_DIGEST, COVERAGE_SCHEMA_DIGEST],
                                key=lambda s: C(s))}
for k, ann in (("scopeIds", "canonical-set"), ("facts", "canonical-set"),
               ("coverageIds", "canonical-set"), ("schemaDigests", "canonical-set")):
    check_order(VIEW[k], ann, k)
VIEW_ID = S.mint("view", VIEW)

STAGE_SPEC = {"schemaVersion": 2, "planId": PLAN_ID, "producerClosure": TS_PROV_CID,
              "operation": "native.analyze", "parameters": [],
              "outputDomains": sorted(["coverage", "fact", "subject-scope", "view"],
                                      key=lambda s: C(s)),
              "outputSchemaDigest": COVERAGE_SCHEMA_DIGEST}
STAGE_SPEC_DIGEST = S.put_record(STAGE_SPEC, "stage-spec")
EXEC_PLAN = {"schemaVersion": 2, "planId": PLAN_ID,
             "stages": [{"ordinal": 0, "stageSpecDigest": STAGE_SPEC_DIGEST,
                         "requires": [], "outputDomains": STAGE_SPEC["outputDomains"]}]}
check_order(EXEC_PLAN["stages"], "ordinal", "stages")
EXEC_PLAN_ID = S.mint("execution-plan", EXEC_PLAN)

NODE = POLICY["rules"][0]["emitWhen"]
NODE_DIGEST = S.put_record(NODE, "Predicate node p")
PROG_PRED = {"schemaVersion": 2, "ruleProgramDigest": RULE_PROGRAM_DIGEST,
             "ruleId": "no-orphan-util", "predicateId": "p", "operation": "none",
             "nodeDigest": NODE_DIGEST}
PROG_PRED_DIGEST = S.put_record(PROG_PRED, "program-predicate")
WITNESS = {"schemaVersion": 2, "programPredicateDigest": PROG_PRED_DIGEST,
           "matchingFactIds": [], "coverageIds": sorted([DECL_COV_ID], key=lambda s: C(s)),
           "countLimit": None, "childPredicateIds": []}
WITNESS_DIGEST = S.put_record(WITNESS, "predicate-witness")

INPUT_REFS = sorted([
    {"domain": "view", "digest": VIEW_ID.split(":")[1]},
    {"domain": "coverage", "digest": DECL_COV_ID.split(":")[1]},
    {"domain": "coverage", "digest": FILE_COV_ID.split(":")[1]},
    {"domain": "coverage", "digest": CL_COV_ID.split(":")[1]},
    {"domain": "rule-program", "digest": RULE_PROGRAM_DIGEST},
    {"domain": "policy", "digest": POLICY_DIGEST},
    {"domain": "waiver", "digest": WAIVER_DIGEST},
    {"domain": "native-context", "digest": TS1_ADM["contextId"].split(":")[1]},
    {"domain": "analysis-spec", "digest": ANALYSIS_SPEC_DIGEST},
    {"domain": "capability-manifest", "digest": CAP_ID},
    {"domain": "schema", "digest": RELATION_SCHEMA_DIGEST},
    {"domain": "schema", "digest": COVERAGE_SCHEMA_DIGEST},
], key=lambda r: C(r))
check_order(INPUT_REFS, "canonical-set", "evaluationInputRefs")

PROOF = {"schemaVersion": 2, "planId": PLAN_ID, "executionPlanId": EXEC_PLAN_ID,
         "evaluatorClosure": EVAL_CID, "ruleProgramDigest": RULE_PROGRAM_DIGEST,
         "evaluationInputRefs": INPUT_REFS,
         "predicateProofs": [{"ruleId": "no-orphan-util", "subjectId": "src/util.ts#helper",
                              "predicateId": "p", "operation": "none",
                              "inputRefs": [r for r in INPUT_REFS
                                            if r["domain"] in ("view", "coverage")],
                              "scopeIds": sorted([DECL_SCOPE_ID], key=lambda s: C(s)),
                              "value": "indeterminate", "witnessDigest": WITNESS_DIGEST}],
         "findingIds": [], "verdict": "indeterminate"}
check_order(PROOF["predicateProofs"], "predicate", "predicateProofs")
PROOF_ID = S.mint("proof-bundle", PROOF)

EVIDENCE = {"schemaVersion": 2, "planId": PLAN_ID, "viewIds": [VIEW_ID],
            "coverageIds": VIEW["coverageIds"], "importIds": [], "findingIds": [],
            "proofBundleId": PROOF_ID}
EVIDENCE_ID = S.mint("semantic-evidence", EVIDENCE)
SEAL = {"schemaVersion": 2, "planId": PLAN_ID, "executionPlanId": EXEC_PLAN_ID,
        "evidenceId": EVIDENCE_ID, "evaluatorClosure": EVAL_CID,
        "policyDigest": POLICY_DIGEST, "proofBundleId": PROOF_ID,
        "verdict": "indeterminate"}
SEAL_ID = S.mint("evaluation-seal", SEAL)
RUN = {"schemaVersion": 2, "projectId": PROJECT_ID, "snapshotId": SNAP_ID,
       "planId": PLAN_ID, "evidenceId": EVIDENCE_ID, "evaluationSealId": SEAL_ID,
       "capabilityManifestId": CAP_ID}
RUN_ID = S.mint("run", RUN)

V["TS-RUN-1-complete-minimal-positive-typescript-run"] = {
    "projectId": PROJECT_ID,
    "snapshotId": SNAP_ID, "planId": PLAN_ID,
    "nativeContextDigests": PLAN["nativeContextDigests"],
    "sourceUniverse": UNIV_HEX,
    "universeDomain": TSU,
    "subjectScopes": {"file@enumerated": FILE_SCOPE_ID,
                      "declares@syntactic": DECL_SCOPE_ID,
                      "clones@normalized-body-hash": CL_SCOPE_ID},
    "subjectScopeCommitment_file": FILE_COMMIT,
    "commitmentIsTheSameDigestAsScope2": FILE_COMMIT.split(":")[1] == FILE_SCOPE_ID.split(":")[1],
    "coverageIds": VIEW["coverageIds"],
    "factCount": len(VIEW["facts"]),
    "viewId": VIEW_ID, "executionPlanId": EXEC_PLAN_ID, "proofBundleId": PROOF_ID,
    "evidenceId": EVIDENCE_ID, "evaluationSealId": SEAL_ID, "runId": RUN_ID,
    "acyclic": {"proofExcludesEvidenceAndRun": ("evidenceId" not in PROOF and "runId" not in PROOF),
                "evidenceIncludesProof": EVIDENCE["proofBundleId"] == PROOF_ID,
                "sealIncludesBoth": SEAL["evidenceId"] == EVIDENCE_ID and SEAL["proofBundleId"] == PROOF_ID,
                "runIncludesSeal": RUN["evaluationSealId"] == SEAL_ID},
    "verdict": "indeterminate",
    "verdictReason": "no-consumer predicate over references@resolved-binding has no admitted "
                     "view entry for that relation: sufficiency v2 step 1 required-relation-missing; "
                     "strong-Kleene 'none' is indeterminate, never an authoritative no-match."}
