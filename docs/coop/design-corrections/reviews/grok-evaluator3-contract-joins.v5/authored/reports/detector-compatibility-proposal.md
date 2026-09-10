# Detector compatibility — owner projection after existing trust admission

**Standing.** Actual Grok native/security owner assessment. Workflow files were read only. This is a join proposal for root to attach to workflow v10 delivery. Not a second schema fork. Not signature verification. Not product qualification.

## The gap

Workflows-and-surfaces §2 already requires two-way comparison only when closures are identical or the **current detector's signed manifest lists the baseline `closure2` as exactly semantically compatible at the same major** (`declared-compatible`), under current trust. Workflow v1 `resolve_detectors` still takes a caller `compatibleWith` list. Workflow v3 projection **refuses** caller `compatibleWith` and will fill it only from an admitted manifest body. Until that body is an owner projection **after** security admission, `declared-compatible` has no retained input.

Identity already hashes `closure.manifestDigest` as raw SHA-256 of the admitted component-manifest **body**, excluding the signature envelope (`identity-schemas.v3` closure, raw-artifact). Security already admits signed roots, catalogs, revocation, and closures through the trust trio:

1. retained generation
2. current installed signed release with the same `closure2`
3. signed `closureBundle`

all under current trust. Envelope kinds (`opensip-signature-envelope.2`) include `catalog` (TR-INDEX). Reference `verify_envelope` is a TCB assumption: the model consumes **already-accepted signer sets**, not a caller `signatureVerified` boolean.

There is no security-owned **projection** of the compatibility listing after that admission. That is the missing owner.

## Do not fork the body schema

Workflow already published

`workflows/schemas/evaluator3/detector-manifest.schema.json`  
`$id`: `urn:opensip:product-v1:workflows:evaluator3:detector-manifest:1`  
`DetectorManifestV1`: `{schemaFamily: opensip.product.detector-manifest, schemaMajor: 1, compatibleClosures: [{closureId, semanticsMajor}]}`.

That is the unsigned body. Do **not** mint a second `DetectorCompatibilityManifest` document in security schemas. If the product name is wanted, it is an alias of this body, not a parallel `$id`.

`parse_detector_manifest_body` / `admitted_manifest_compatible_with` already:

- require `host.closures[closureId].trust == admitted` and `bytes != missing`
- require the closure object in the retained map
- parse body at `blobs[manifestDigest]`
- return `[]` if the body is not this family/major
- never set `signatureVerified`

Those helpers are workflow **projection**. They must not become the trust admission.

## Proposed owner projection (security, after existing admission)

After the host has admitted the detector `closure2` by the trust trio (retained generation / installed signed release / signed bundle), project:

```
DetectorCompatibilityProjectionV1 = {
  closureId,            // closure2: of the current detector
  manifestDigest,       // raw SHA-256 of the admitted body (equals closure.manifestDigest)
  trustOrigin,          // retained-generation | installed-signed-release | signed-closure-bundle
  compatibleClosures    // exact body.compatibleClosures, already schema-admitted
}
```

Rules:

- Projection runs **only** if the closure is already admitted. Missing, revoked, or protocol/platform-incompatible closures never yield a listing (`pivot-detector-unavailable` / `pivot-closure-revoked` / `pivot-closure-incompatible` remain).
- Bytes at `manifestDigest` are the retained body. Re-hash; disagree with `closure.manifestDigest` refuses. Do not re-encode under a second profile.
- Validate the body against the **single** W schema above. Additional properties refuse.
- `compatibleClosures[].closureId` is `closure2:`. `semanticsMajor` is the listing major. Order is unique `closureId` (schema `x-opensip-order`).
- Empty `compatibleClosures` is a lawful complete listing (no declared-compatible peers). Absent/non-family body is **not** an empty listing: it is “no compatibility declaration”, so comparison cannot take `declared-compatible` (W already returns `[]` and then only exact closureId+semanticsMajor identity).
- No field `signatureVerified`. Trust is the admission receipt (`trust=admitted` + `trustOrigin`), not a canned boolean on the projection.
- Reference signature verification remains TCB (`verify_envelope` already accepted). Closure identity (`closure2` + tree + `manifestDigest`) is not release authority. Catalog/role/namespace join is delivery/security admission, already owned.

## `ruleStableId` / `semanticsMajor` join

Do **not** put `ruleStableId` on each `compatibleClosures` row. That would duplicate EvaluatorEmissionPlanV1 and invite caller maps.

Join:

- Emission binding: `(ruleId, ruleStableId, semanticsMajor, detectorClosure)` — Plan-committed.
- Manifest listing: `(peerClosure2, semanticsMajor)` — detector-level, same major as §2.
- Declared-compatible for a rule holds iff the **current** emission `detectorClosure` is admitted, its projected listing contains the **baseline** detector `closure2` at **that** `semanticsMajor`, and emission `semanticsMajor` equals the listing row.

One detector closure serving several `ruleStableId`s at one major is one listing. A major disagreement is not declared-compatible.

Workflow v1 `resolve_detectors(..., compatibleWith)` is historical. Current intended fill is `emission_detectors_with_admitted_compatibility` after this projection.

## What security already owns (do not restate as new admission)

- Root/catalog/revocation envelopes and TR-* roles
- Current-trust resolution of a `closure2` from retained generation, installed signed release, or signed bundle
- Revocation of a closure (never execute revoked bytes)
- Protocol-major / platform incompatibility of a pivot closure
- `closure.manifestDigest` raw-artifact identity (identity contract)

## Required root/W joins (not done here)

1. Treat W `DetectorManifestV1` as the one body schema. Do not add a security copy.
2. Host adapter: after closure admission, retain body bytes keyed by `manifestDigest`, project `DetectorCompatibilityProjectionV1`, pass that into comparison instead of `host.closures[].trust` plus a caller list.
3. Decide encoding of the body vs identity’s “security metadata profile” sentence: envelope is metadata; listing body should be the exact retained bytes already hashed. Do not parse with a second canonicalizer that can disagree.
4. Fixture closures whose `manifestDigest` is not this family remain “no declaration” (empty projection), not declared-compatible.
5. Workflow v1 caller `compatibleWith` path stays historical; it is not current admission.

## Qualification limits

This proposal does not verify signatures, does not qualify a release, and does not claim a canned `verified=true`. Synthetic `trust=admitted` in workflow fixtures is a TCB assumption, the same class as security `signers` already-accepted. Independent release qualification remains G07/G08/G15.
