"""Run every vector group and emit the machine-readable vector record."""
import sys, os, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.dirname(HERE)

import build_ts, build_ts2, build_ts3, build_ts4          # noqa: F401
import build_rust, build_rust2                            # noqa: F401
import build_syntax                                       # noqa: F401
import build_workflow, build_suff, build_final            # noqa: F401
from build_ts import V, S
from model import registered_pairs, RELATION_SCHEMA_DIGEST, COVERAGE_SCHEMA_DIGEST

V["TABLE-1-complete-registered-relation-rung-applicability"] = {
    "authority": "foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry"
                 " (the SINGLE ladder authority; native_evidence_model LADDERS and "
                 "capability-manifest-domains.v2 RELATION-LADDER-DOMAIN-V2 are declared "
                 "mirrors, drift-checked exactly and IN ORDER)",
    "relationCount": 13,
    "registeredPairCount": len(registered_pairs()),
    "resolvedRungSet": ["resolved-target", "resolved-binding", "resolved-callee",
                        "checked", "from-resolved-calls"],
    "rows": registered_pairs(),
    "rc1Law": "state is decided by the RUNG through membership in the closed five-member "
              "resolved set, NEVER by how many rungs the relation's ladder has - reachability "
              "is one-rung and its single rung IS resolved, so it is never not-applicable",
    "rc0RunsFirst": "the (relation, rung) pair must be REGISTERED before any state rule; the "
                    "rung vocabulary is shared across relations so a schema-valid resolution "
                    "proves nothing, and RC-1 assigns NO state to an unrecognised pair",
    "factFreeEntriesAreJudgedTheSameWay": True,
    "appliedToRetainedScopesAndCoverageEvenWithNoFactPresent": True,
    "registeredPayloadSchemaDocumentDigests": {
        "relation payloads (foundation/relation-payload-schemas.v2.json)":
            RELATION_SCHEMA_DIGEST,
        "CoverageResultV3 (native/native-evidence.schemas.v2.json)":
            COVERAGE_SCHEMA_DIGEST}}

V["STORE-1-content-addressed-store-summary"] = {
    "retainedObjects": len(S.cas),
    "retentionModes": {
        "preimage": "the exact preimage bytes retained UNDER this digest; the closure "
                    "checker fetches and re-hashes",
        "fragment": "a canonical sub-object of an already retained record, recomputed there "
                    "(closed to program-predicate.nodeDigest)",
        "derived": "recomputed from another retained artifact (closed to capabilityManifestId "
                   "and to sourceUnitOwnership.unitId / body-language-version)",
        "owner-retained": "retained and admitted by the named owning contract; joined by "
                          "digest equality only (closed to owner-source-set[]."
                          "ownerFileManifestSha256)"},
    "oneStoreKeyedByRawSHA256HoldsAllThree":
        "raw artifacts, canonical records and H PREIMAGE FRAMES, because H(D,X) is SHA256 of "
        "the framed preimage"}

payload = {
    "producer": "blind consumer-B v6 independent reconstruction",
    "codec": "C (identity-and-evidence sec.3), independently implemented from the prose",
    "identity": 'H(D,X) = SHA256(ASCII("opensip.product.v1")||00||ASCII(D)||00||'
                'uint64BE(len(C(X)))||C(X))',
    "capabilityManifest": 'SHA256(UTF8("opensip.capability-manifest.v1")||00||committedBytes), '
                          'committedBytes = CVE1(CapabilityManifestV1)',
    "vectorCount": len(V),
    "vectors": V,
}
p = os.path.join(OUT, "vectors.json")
with open(p, "w") as f:
    json.dump(payload, f, indent=1, sort_keys=False, ensure_ascii=False)
print("wrote", p, len(V), "vector groups,", len(S.cas), "retained objects")

# a compact index for the review
idx = {}
for k, v in V.items():
    if isinstance(v, dict):
        neg = {kk: vv for kk, vv in v.items() if isinstance(vv, str) and
               ("NOT-REFUSED" in vv)}
        idx[k] = {"keys": len(v), "unexpectedlyAdmitted": neg}
    else:
        idx[k] = {"keys": 0, "unexpectedlyAdmitted": {}}
bad = {k: v for k, v in idx.items() if v["unexpectedlyAdmitted"]}
print("groups with an unexpectedly-admitted negative:", bad if bad else "NONE")
