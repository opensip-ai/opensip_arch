"""Detector compatibility listing admission.

Owners: workflows-and-surfaces.md s2 lines 285-300 (security S1 binds the unique regular-file path in the already admitted same
closure2 tree; detector-manifest schema; exact retained byte length and SHA-256), workflow-projection-contract.v3.md s10, s13, s14
(host-only projection {closureId, componentManifestDigest, listing:{path,sha256,bytes}, trustOrigin, compatibleClosures, tree,
platform, protocolMajor}), s15 (the three-field listing cannot occupy closure.manifestDigest).
The kit says a present malformed / unrecognized / missing / mismatched listing "refuses" without naming refusal keys, so the keys
below are cb24-prefixed. Signature verification of the tree is security TCB and is not performed here.
"""
import hashlib

import canonical as K
import schemas

KIT = schemas.kit()
RESERVED = ".opensip/detector-compatibility.json"
DOC = "workflows/schemas/evaluator3/detector-manifest.schema.json"
TRUST_ORIGINS = ("retained-generation", "installed-signed-release", "signed-closure-bundle")


def admit_listing(store, closure_id, desc, trust_origin):
    base = {"closureId": closure_id, "componentManifestDigest": desc["manifestDigest"], "trustOrigin": trust_origin,
            "platform": desc["platform"], "protocolMajor": desc["protocolMajor"], "listing": None, "compatibleClosures": None,
            "firstRefusal": None}
    if trust_origin not in TRUST_ORIGINS:
        return dict(base, state="refused", firstRefusal="cb24.DETECTOR_LISTING_TRUST_ORIGIN_NOT_ADMITTED")
    rows = [r for r in desc["tree"] if r["path"] == RESERVED]
    if not rows:
        return dict(base, state="absent")
    if len(rows) > 1:
        return dict(base, state="refused", firstRefusal="cb24.DETECTOR_LISTING_PATH_NOT_UNIQUE")
    row = rows[0]
    data = store.blobs.get(row["sha256"])
    if data is None:
        return dict(base, state="refused", firstRefusal="cb24.DETECTOR_LISTING_BYTES_MISSING")
    if hashlib.sha256(data).hexdigest() != row["sha256"] or len(data) != row["bytes"]:
        return dict(base, state="refused", firstRefusal="cb24.DETECTOR_LISTING_DIGEST_OR_LENGTH_MISMATCH")
    try:
        value = K.parse_raw(data)
    except K.AdmissionError as exc:
        return dict(base, state="refused", firstRefusal=f"cb24.DETECTOR_LISTING_MALFORMED:{exc.boundary}")
    r = KIT.admit(value, DOC, "#")
    if not r["ok"]:
        return dict(base, state="refused", firstRefusal="cb24.DETECTOR_LISTING_UNRECOGNIZED")
    return dict(base, state="listing", listing={"path": RESERVED, "sha256": row["sha256"], "bytes": row["bytes"]},
                compatibleClosures=value["compatibleClosures"])


def declared_compatible(adm, baseline_closure_id, baseline_major):
    return adm["state"] == "listing" and any(c["closureId"] == baseline_closure_id and c["semanticsMajor"] == baseline_major
                                             for c in adm["compatibleClosures"])
