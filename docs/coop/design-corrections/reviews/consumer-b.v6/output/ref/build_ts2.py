"""Vector group A2: the complete minimal positive TypeScript Run descriptor
graph, plus its discriminating negative controls."""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osip import *
from model import *
from build_ts import (S, V, R1_INV, _INVMAP, PROJECT_ID, PLATFORM, TS1_CTX,
                      TS1_UNIV, TS1_UNIV_ID, TS1_ADM, TS1_GRAPH, TS1_GRAPH_D,
                      TS_PROV_CID, EVAL_CID, LAYOUT, LAYOUT_DIGEST,
                      admit_ts_context, bind_ts_universe, ts_context,
                      config_graph, cnode, derive_config_origin, HONORED_R1,
                      blob, inv, closure, lib_component, node_kind)

# ------------------------------------------------------------ capability manifest
CAPREG = CapRegistry(CAPDOMAINS)

CAP_MANIFEST = {
    "schemaVersion": 1,
    "profile": "default",
    "providers": [
        {"providerId": "opensip.provider.typescript",
         "language": "typescript",
         "providerVersionSource": "signed-closure-manifest",
         "toolchainIdentitySource": "native-context-v2",
         "relations": {"clones": "normalized-body-hash", "declares": "syntactic",
                       "file": "enumerated", "package": "manifest-declared",
                       "references": "resolved-binding",
                       "unresolved-edge": "observed", "vcs-change": "vcs-reported"},
         "platformIds": ["macos-aarch64"]}],
    "coverageForAbsent": [
        {"providerId": "opensip.provider.rust", "language": "rust",
         "relationIds": ["calls", "imports", "types"],
         "coverageState": "unavailable", "deficiency": "provider-unavailable"}],
}
viol = CAPREG.admit(CAP_MANIFEST)
assert viol == [], viol
CAP_BYTES = cve1(CAP_MANIFEST)
CAP_ID = capability_manifest_id(CAP_BYTES)
CAP_BYTES_DIGEST = S.put_blob(CAP_BYTES, "capability-manifest CVE1 artifact")

V["CAP-1-positive-manifest-admits-under-the-selected-successor-registry"] = {
    "registrySelectedBy": "identity-and-evidence sec.3 + native-evidence sec.11 "
                          "-> docs/coop/design-corrections/native/capability-manifest-domains.v2.json",
    "gateOrder": CAPDOMAINS["gateOrder"],
    "violations": viol,
    "committedBytesLength": len(CAP_BYTES),
    "capabilityManifestBytesDigest": CAP_BYTES_DIGEST,
    "capabilityManifestId": CAP_ID,
    "recipe": 'SHA256(UTF8("opensip.capability-manifest.v1") || 00 || committedBytes)',
    "unresolvedEdgeIsAdmissibleOnlyUnderRELATION_DOMAIN_V2": True,
}

# key-insertion-order independence (CVE1 sorts map entries by key bytes)
_reordered = {"coverageForAbsent": CAP_MANIFEST["coverageForAbsent"],
              "providers": CAP_MANIFEST["providers"],
              "profile": CAP_MANIFEST["profile"],
              "schemaVersion": CAP_MANIFEST["schemaVersion"]}
V["CAP-2-map-key-insertion-order-does-not-change-the-identity"] = {
    "sameId": capability_manifest_id(cve1(_reordered)) == CAP_ID}


def cap_neg(name, mutate):
    m = json.loads(json.dumps(CAP_MANIFEST))
    mutate(m)
    v = CAPREG.admit(m)
    enc = None
    if not v:
        try:
            enc = capability_manifest_id(cve1(m))
        except Refuse as e:
            enc = "CVE1-REFUSED:" + str(e)
    return {"violations": v, "encodedIdIfGatesPassed": enc}


def _set_sv_true(m): m["schemaVersion"] = True
def _set_sv_str(m): m["schemaVersion"] = "1"
def _extra(m): m["providers"][0]["extra"] = "x"
def _missing(m): del m["providers"][0]["language"]
def _cross_rung(m): m["providers"][0]["relations"]["declares"] = "resolved-callee"
def _unreg_rel(m): m["providers"][0]["relations"]["python-imports"] = "syntactic"
def _unsorted(m): m["providers"][0]["platformIds"] = ["macos-x86_64", "macos-aarch64"]
def _dup_platform(m): m["providers"][0]["platformIds"] = ["macos-aarch64", "macos-aarch64"]
def _dup_provider(m): m["providers"] = m["providers"] + [json.loads(json.dumps(m["providers"][0]))]
def _bad_state(m): m["coverageForAbsent"][0]["coverageState"] = "complete"
def _bad_def(m): m["coverageForAbsent"][0]["deficiency"] = "resolution-incomplete"
def _nonnfc(m): m["providers"][0]["providerId"] = "opensip.provider.typescriptÅ"
def _sv2(m): m["schemaVersion"] = 2

for nm, fn in [
    ("CAP-N1-ADM-TYPE-boolean-is-not-an-integer", _set_sv_true),
    ("CAP-N2-ADM-TYPE-numeric-string-is-not-an-integer", _set_sv_str),
    ("CAP-N3-ADM-CLOSED-undeclared-key-on-a-record", _extra),
    ("CAP-N4-ADM-CLOSED-missing-required-key", _missing),
    ("CAP-N5-ADM-DOMAIN-rung-of-another-relations-ladder", _cross_rung),
    ("CAP-N6-ADM-DOMAIN-unregistered-relation-key", _unreg_rel),
    ("CAP-N7-ADM-ORDER-unsorted-platformIds", _unsorted),
    ("CAP-N8-ADM-ORDER-duplicate-is-an-ordering-violation", _dup_platform),
    ("CAP-N9-ADM-ORDER-duplicate-providerId-row", _dup_provider),
    ("CAP-N10-ADM-DOMAIN-coverageState-outside-the-one-member-domain", _bad_state),
    ("CAP-N11-ADM-DOMAIN-deficiency-outside-the-five-member-domain", _bad_def),
    ("CAP-N12-CVE1-refuses-a-non-NFC-string-after-the-gates-pass", _nonnfc),
    ("CAP-P2-declared-OPEN-schemaVersion-2-passes-the-gates-and-moves-the-id", _sv2),
]:
    V[nm] = cap_neg(nm, fn)

# ------------------------------------------------------------------- snapshot
SEM_CONFIG = {
    "analysis": {"profileId": "default",
                 "capabilities": ["clones-fact", "inventory", "syntax", "unresolved-edge"],
                 "budget": {"unit": "work-units", "limit": 1000000}},
    "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
RESOLVED_CONFIG_DIGEST = S.put_record(SEM_CONFIG, "semantic-configuration")

SCOPE_DESC = {"schemaVersion": 2, "workspaceRoots": ["."],
              "pathPrefixes": [],
              "excludedPathPrefixes": [".git", "node_modules"]}
for k in ("workspaceRoots", "pathPrefixes", "excludedPathPrefixes"):
    SCOPE_DESC[k] = sorted(SCOPE_DESC[k], key=lambda s: C(s))
    check_order(SCOPE_DESC[k], "canonical-set", k)
SCOPE_DIGEST = S.put_record(SCOPE_DESC, "scope-descriptor")

SOURCE_INV_DIGEST = S.put_record(R1_INV, "source-inventory")
VCS = {"schemaVersion": 2, "kind": "git",
       "commitId": "4f" * 20, "dirty": False,
       "sourceInventoryDigest": SOURCE_INV_DIGEST}
VCS_DIGEST = S.put_record(VCS, "vcs-observation")

SNAP = {"schemaVersion": 2, "projectId": PROJECT_ID, "sourceInventory": R1_INV,
        "resolvedConfigDigest": RESOLVED_CONFIG_DIGEST, "scopeDigest": SCOPE_DIGEST,
        "vcsDigest": VCS_DIGEST}
SNAP_ID = S.mint("snapshot", SNAP)

ANALYSIS_SPEC = {"schemaVersion": 2,
                 "requestedCapabilities": sorted([
                     {"capabilityId": "inventory", "languageMode": "ts-tsconfig",
                      "workspaceRoot": ".", "required": True},
                     {"capabilityId": "syntax", "languageMode": "ts-tsconfig",
                      "workspaceRoot": ".", "required": True},
                     {"capabilityId": "clones-fact", "languageMode": "ts-tsconfig",
                      "workspaceRoot": ".", "required": True}], key=lambda r: C(r)),
                 "policyPackIds": ["pack.default"], "parameters": []}
check_order(ANALYSIS_SPEC["requestedCapabilities"], "canonical-set", "requestedCapabilities")
ANALYSIS_SPEC_DIGEST = S.put_record(ANALYSIS_SPEC, "analysis-spec")

GRANT = {"schemaVersion": 2, "projectId": PROJECT_ID,
         "principals": [{"kind": "first-party", "closureId": TS_PROV_CID,
                         "ownerSourceDigest": None}],
         "analysisOperations": sorted(["read-source", "native-analysis"], key=lambda s: C(s)),
         "scopeDigest": SCOPE_DIGEST}
GRANT_DIGEST = S.put_record(GRANT, "semantic-grant")

POLICY = {"schemaVersion": 1, "policyId": "pack.default", "rules": [
    {"ruleId": "no-orphan-util", "ruleProgramRef":
        {"contribution": "first-party", "stableId": "R-ORPHAN", "semanticsMajor": 2,
         "programDigest": "ab" * 32},
     "enabled": True, "severity": "warning", "gate": True,
     "subjectEnumeration": {"universe": "typescript", "subjectKind": "symbol",
                            "include": ["src/**"], "exclude": []},
     "emitWhen": {"op": "none", "relation": "references",
                  "minResolution": "resolved-binding", "filters": []},
     "evidenceUse": []}]}
POLICY_DIGEST = S.put_record(POLICY, "PolicyDocumentV1")
WAIVERS = {"schemaVersion": 1, "waivers": []}
WAIVER_DIGEST = S.put_record(WAIVERS, "WaiverSetV1")
RULE_PROGRAM = {"schemaVersion": 1, "policyDigest": POLICY_DIGEST,
                "rules": [{"ruleId": "no-orphan-util",
                           "ruleProgramRef": POLICY["rules"][0]["ruleProgramRef"],
                           "emitWhen": POLICY["rules"][0]["emitWhen"]}]}
RULE_PROGRAM_DIGEST = S.put_record(RULE_PROGRAM, "RuleProgramV1")

PLAN = {"schemaVersion": 2, "snapshotId": SNAP_ID,
        "capabilityManifestId": CAP_ID,
        "semanticClosures": sorted([TS_PROV_CID, EVAL_CID], key=lambda s: C(s)),
        "analysisSpecDigest": ANALYSIS_SPEC_DIGEST,
        "resolvedConfigDigest": RESOLVED_CONFIG_DIGEST,
        "nativeContextDigests": [TS1_ADM["contextId"].split(":")[1]],
        "importIds": [], "policyDigest": POLICY_DIGEST, "waiverDigest": WAIVER_DIGEST,
        "scopeDigest": SCOPE_DIGEST,
        "budget": SEM_CONFIG["analysis"]["budget"],
        "semanticGrantDigest": GRANT_DIGEST,
        "capabilityManifestBytesDigest": CAP_BYTES_DIGEST}
PLAN_ID = S.mint("plan", PLAN)

# --------------------------------------------------------------- scopes / facts
UNIV_HEX = TS1_UNIV_ID.split(":")[1]


def subject_scope(relation, rung, subjects, univ_hex=UNIV_HEX, snap=SNAP_ID,
                  enumerator=TS_PROV_CID):
    rc0(relation, rung)
    subs = sorted(set(subjects), key=lambda s: C(s))
    check_order(subs, "canonical-set", "subjects")
    d = {"schemaVersion": 2, "snapshotId": snap, "sourceUniverse": univ_hex,
         "targetUniverse": univ_hex, "relation": relation, "resolution": rung,
         "enumeratorClosure": enumerator, "subjects": subs}
    sid = S.mint("subject-scope", d)
    return d, sid, "sha256:" + sid.split(":")[1]


def fact(relation, rung, payload, anchors, univ_hex=UNIV_HEX, snap=SNAP_ID,
         producer=TS_PROV_CID, confidence=1000000):
    rc0(relation, rung)
    r = RELREG[relation]
    law = r["anchorLaw"]
    if law["class"] == "inventory" and len(anchors) != 0:
        raise Refuse("FACT_ANCHOR_CARDINALITY", f"{relation}: {len(anchors)} != 0")
    if law["class"] == "body-identity" and len(anchors) != 1:
        raise Refuse("FACT_ANCHOR_CARDINALITY", f"{relation}: {len(anchors)} != 1")
    if law["class"] == "source-text" and len(anchors) < 1:
        raise Refuse("FACT_ANCHOR_CARDINALITY", f"{relation}: {len(anchors)} < 1")
    if r["universeRule"] == "same-only" and univ_hex != univ_hex:
        raise Refuse("FACT_UNIVERSE_RULE", relation)
    got = set(payload)
    need = set(r["inheritedRequired"])
    if not need <= got:
        raise Refuse("FACT_PAYLOAD_REQUIRED", str(sorted(need - got)))
    allowed = need | set(r["inheritedOptional"])
    if not got <= allowed:
        raise Refuse("FACT_PAYLOAD_UNDECLARED", str(sorted(got - allowed)))
    rr = r["rungs"].get(rung, {})
    for f in rr.get("required", []):
        if f not in payload:
            raise Refuse("FACT_RUNG_REQUIRED_FIELD", f)
    for f in rr.get("forbidden", []):
        if f in payload:
            raise Refuse("FACT_RUNG_FORBIDDEN_FIELD", f)
    pd = S.put_record(payload, "relation payload " + relation)
    anch = sorted(anchors, key=lambda a: C(a))
    check_order(anch, "canonical-set", "anchors")
    f = {"schemaVersion": 2, "snapshotId": snap, "relation": relation,
         "resolution": rung, "sourceUniverse": univ_hex, "targetUniverse": univ_hex,
         "producerClosure": producer, "payloadSchemaDigest": RELATION_SCHEMA_DIGEST,
         "payloadDigest": pd, "anchors": anch, "confidenceMillionths": confidence}
    return f, S.mint("fact", f), payload


def snapshot_joins(f, payload, inventory):
    """The per-relation snapshotJoins the registry publishes, applied to EVERY
    owning fact, independently of the payload decode memo."""
    ip = {r["path"]: r for r in inventory}
    rel = f["relation"]
    for j in RELREG[rel].get("snapshotJoins", []):
        if j.get("unless") and payload.get(j["unless"]["field"]) == j["unless"]["equals"]:
            continue
        p = payload[j["pathField"]]
        if p not in ip:
            raise Refuse("SNAPSHOT_JOIN_PATH_NOT_INVENTORIED", f"{rel}:{p}")
        if j["form"] == "inventoried-file":
            if ip[p]["sha256"] != payload[j["digestField"]]:
                raise Refuse("SNAPSHOT_JOIN_DIGEST", p)
            if ip[p]["bytes"] != payload[j["lengthField"]]:
                raise Refuse("SNAPSHOT_JOIN_LENGTH", p)
            if not S.has(payload[j["digestField"]]):
                raise Refuse("EVIDENCE_UNAVAILABLE", p)   # retention loss, not a false claim
    for a in f["anchors"]:
        if a["path"] not in ip:
            raise Refuse("ANCHOR_SOURCE", a["path"])
        if ip[a["path"]]["sha256"] != a["blobDigest"]:
            raise Refuse("ANCHOR_SOURCE", a["path"])
        if not (0 <= a["startByte"] <= a["endByte"] <= ip[a["path"]]["bytes"]):
            raise Refuse("ANCHOR_RANGE", a["path"])
    return True


def coverage(scope_id, relation, rung, entry, commitment, subject_count):
    rc0(relation, rung)
    payload = {"schemaVersion": 3,
               "key": {"relation": relation, "resolution": rung,
                       "sourceUniverse": UNIV_HEX, "targetUniverse": UNIV_HEX,
                       "subjectScopeCommitment": commitment},
               "entry": entry}
    if entry["relation"] != relation or entry["resolution"] != rung:
        raise Refuse("native.coverage-entry-key-mismatch", relation)
    if entry["examinedUniverse"]["subjectScopeCommitment"] != commitment:
        raise Refuse("native.examined-universe-commitment-mismatch", "")
    if entry["examinedUniverse"]["subjectCount"] != subject_count:
        raise Refuse("native.examined-universe-subject-count-mismatch", "")
    rc1(relation, rung, entry)
    pd = S.put_record(payload, "CoverageResultV3")
    cov = {"schemaVersion": 2, "scopeId": scope_id,
           "payloadSchemaDigest": COVERAGE_SCHEMA_DIGEST, "payloadDigest": pd}
    return payload, cov, S.mint("coverage", cov)


NA_RC = {"state": "not-applicable", "attempted": False, "examinedExhaustive": True,
         "stageTerminal": "complete", "unresolvedEdgeCount": 0,
         "unresolvedEdgeClasses": []}
CW_CLOSED = {"exportsClosed": "closed", "entryPointsRecognized": "all",
             "nonliteralLoading": "none", "externalConsumers": "none-declared",
             "dynamicDispatch": "resolved", "reasons": [],
             "deadCodeRepairEligible": True}


def entry(relation, rung, cov="complete", rc=None, deficiency=None, cause=None,
          commitment=None, count=0, derivation=None, closed_world=None):
    return {"relation": relation, "resolution": rung, "coverage": cov,
            "examinedUniverse": {"subjectScopeCommitment": commitment,
                                 "subjectCount": count},
            "resolutionCompleteness": rc or dict(NA_RC),
            "closedWorld": closed_world or CW_CLOSED,
            "derivationKinds": derivation or [],
            "confidenceMillionths": 1000000,
            "deficiency": deficiency, "nativeCause": cause}
