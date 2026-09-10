# Trust-join assessment — DetectorManifestV1 ↔ closure2 / tree / platform / protocol

**Standing.** Actual Grok native/security owner, isolated `evaluator-successor.v1`. Read-only on W/core. One S1 paragraph added to `security-and-lifecycle.md`. Not independent acceptance. Official suites not run.

**Verdict.** `FINDING_DETECTOR_MANIFEST_NOT_IDENTITY_PREIMAGE`. Existing signed association owner binds the **component** manifest to tree/platform/selected component. It does **not** bind `DetectorManifestV1` listing bytes. Listing inherits those coordinates only after that association, via the admitted `closure2` plus a closed host receipt. `host.closures[].trust='admitted'` is TCB, not the delivery selector.

---

## The exact question

`DetectorManifestV1` body is only `{schemaFamily, schemaMajor, compatibleClosures}` (`additionalProperties` false). Identity §3 says a component manifest for a different tree, platform or selected component is refused by delivery admission. Where does authenticated trust-trio admission bind **this** `closure2` / tree / platform / protocol to **these** unsigned listing bytes?

---

## 1. Finding — two bodies compete for one digest

Identity hashes `closure.manifestDigest` as raw SHA-256 of the admitted **component** manifest body under the security metadata profile, excluding the signature envelope.

| Source | What `closure.manifestDigest` is |
|---|---|
| `identity-and-evidence.md` §3 (lines 250–256) | admitted component-manifest body; signed envelope and role/namespace join retained as operational provenance; different tree/platform/selected component refused by **delivery admission** |
| `identity-schemas.v3.json` `$defs/closure.manifestDigest` | `x-opensip-digest.representation=raw-artifact`; artifact = “the admitted component manifest body bytes under the security metadata profile, excluding the signature envelope” |
| Envelope `urn:opensip:design:signature-envelope:2` | subject `kind=manifest`, domain `opensip.metadata.manifest.1` |
| `security-completion.v1.md` §2.1 | domain tag `opensip.metadata.manifest.1` = DR-103 `manifestSchema` |
| DR-103 `component-manifest-schemas.v11.json` (live cited bytes, sha256 `1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005`, 139492 bytes; **not present** in this isolated tree’s `docs/coop/artifacts/`) | required `kind`, `stableId`, `name`, `version`, `role`, `commands`, `capabilities`, `platforms[]` `{os, arch, tree: TreeCommitment, entrypoint}`, … |
| V-MAN-1 fragment (`security-completion.v1.md` §2.2) | `{"kind":"component","manifestSchemaVersion":1,"name":"typescript-provider",...}` |

`DetectorManifestV1` (`workflows/schemas/evaluator3/detector-manifest.schema.json`, `$id` `urn:opensip:product-v1:workflows:evaluator3:detector-manifest:1`, 1853 bytes, sha256 `ce54903a8806ae5e3d3dcbb3b1a787719af252a802128826b54597ae1f00bd58`) is only those three fields. Its title/description still claim it is the body identity hashes as `closure.manifestDigest`. Those cannot be the same retained bytes: v11 `additional` component fields are required; DetectorManifestV1 `additionalProperties` is false.

W v11 `parse_detector_manifest_body` still treats `blobs[closure.manifestDigest]` as DetectorManifestV1 (family `opensip.product.detector-manifest`, re-hash, schema/order admit). A real admitted component-manifest body therefore yields **no declaration** (`schemaFamily` mismatch → `None`), and a DetectorManifestV1 body occupying that digest **cannot** be the DR-103 document the envelope authenticates.

This is not a hypothetical new feature. It is a conflict of two live claims on one field.

---

## 2. Not-finding — component-manifest ↔ tree/platform **does** have an owner

The pair (signed component-manifest bytes, selected tree/platform/component) is already bound. Selectors, in order:

1. **Identity `closure2`.** `identity-schemas.v3.json` `$defs/closure` required `{schemaVersion:2, kind, manifestDigest, tree, semanticVersion, protocolMajor, platform}`. Identity §3 table: role kind, signed manifest digest, exact executable/data tree, semantic version, protocol major and platform. Swapping `tree` (or `platform` / `protocolMajor` / `kind`) with the same `manifestDigest` **must** mint a different `closure2`. Tree rows are identity `Blob` `{path, sha256, bytes}`.

2. **Delivery / DR-103.** v11 `manifestSchema.platforms[]` (at least one): `{os, arch, tree: TreeCommitment, entrypoint}`. TreeCommitment = `{entries: [{path, type: file\|dir\|symlink, mode, length (files), sha256 (files), target (symlinks)}]}`. RJ-3 refuses path/tree/entrypoint violations. A platform absent from the array is typed unavailability, never a fallback. Identity §3’s “refused by delivery admission” sentence points **here**, not at DetectorManifestV1.

3. **Envelope TCB.** `verify_envelope` already-accepted signers (stated TCB in `security_lifecycle_model_v1.py` header). Message is 32-byte `preimageSha256` under `opensip.metadata.manifest.1`. `storedSha256` is the admission digest of the stored component-manifest bytes. Authenticates **those** bytes, not a `closure2`.

4. **Catalog.** `urn:opensip:design:catalog:1` `releases[]` required `{stableId, publisher, sourceClass, version, manifestDigest, manifestPreimageSha256, envelopeDigest, hostCoreConstraint, artifacts[{platform, archiveProfileId, archiveDigest, sha256}]}`. TR-INDEX signed. **No `closure2` field.** Platform bind is per-artifact archive, not the identity Blob list.

5. **Registry.** `registry.schema.json` entries key `{stableId, provenance, version, manifestDigest, signatureRef, …, catalogSnapshotVersion, catalogPreimageSha256}`. **No `closure2`.**

6. **Trust trio** (`workflows-and-surfaces.md` §2). Fresh host resolves each pivot closure from (a) retained generation, (b) installed signed release with the **same `closure2`**, or (c) signed `closureBundle`; all under current trust. Baseline custody `closureBundle` is only `{path, sha256, bytes}` (`evaluator3/baseline-artifact.schema.json`); “signature/trust admission is the security unit’s contract.” DR-126 inventory (`opensip.metadata.inventory.1`) is `{path, sha256}` over executable bytes (TR-CORE), plus TR-BUNDLE container lists — tree packaging, not a DetectorManifestV1 listing.

**Inheritance for a listing that is not the hashed body:** after (2)–(6) admit `closure2` *C*, the listing is used only for *C*. Tree/platform/protocol are *C*’s identity members. The listing body does not need those fields.

**Tree-swap retaining signed component-manifest bytes:** new `closure2` *C′*. Path (b) “same `closure2`” does not admit *C′*. Catalog match on `manifestDigest` alone does not name *C′*. Delivery (v11 selected `platforms[].tree` vs presented tree) is the refuse for pairing those signed bytes with a different tree. Identity `open_run_closure` does **not** implement that refuse (next section).

---

## 3. Finding — no signed selector binds DetectorManifestV1 bytes to a `closure2`

Searched: catalog, registry, envelope domains, v11 `manifestSchema` fields, lock selected tuples, baseline `closureBundle`, DR-126 inventory. None lists `compatibleClosures` or DetectorManifestV1. None names `closure2` on a release row.

W v11 (root; this owner did not edit) now has `project_admitted_detector_compatibility` (`workflow_projection_model.v3.py`):

- Requires `host.closures[closureId].trust=='admitted'` and `bytes != missing`.
- Parses DetectorManifestV1 from `blobs[objects[id].manifestDigest]`.
- Copies `tree` / `platform` / `protocolMajor` from the **object-map closure descriptor**.
- Optional `trustOrigin` ∈ `{retained-generation, installed-signed-release, signed-closure-bundle}` from the host record; omitted if absent.
- Explicitly not signature verification.

That copy of tree is from the unsigned identity descriptor after a TCB flag. It is not RJ-3 / v11 `platforms[]` comparison. `admitted_manifest_compatible_with` still keys only on `trust==admitted`.

`identity-model.v3.py` `digest_field` for `raw-artifact` (`closure.manifestDigest`): require `blobs[digest]` and `SHA-256(bytes)==digest`. Comment: “A raw artifact is retained bytes and nothing more.” No component-manifest parse. No `platforms[]` vs `closure.tree` compare. `close_run` is evaluator3 replay; `open_run_closure` is owner-closure of retained descriptors.

**Unsigned user tree-swap retaining DetectorManifestV1 bytes:** descriptor `{manifestDigest: listingDigest, tree: attacker, …}` mints *C′*. Identity retains the listing bytes under that digest and closes *C′* if the Blob list is internally consistent. Delivery cannot compare tree out of a three-field listing. Catalog does not list *C′*. Trust-trio (b) does not admit *C′* as the installed release’s `closure2`. The remaining hole is a host that marks `host.closures[C′].trust='admitted'` (fixture TCB) or that treats catalog `manifestDigest` match as closure admission. W’s projector would then attach the listing to the attacker tree.

Identity Blob `{path, sha256, bytes}` is also not field-equal to v11 TreeCommitment `{path, type, mode, length, sha256, target}`. That mapping is implied by identity §3’s delivery sentence and is not a closed equality in `identity-model.v3`. Not a second schema; a named join remainder on the **component** path.

---

## 4. Design law vs reference TCB

| Claim | Class | Source |
|---|---|---|
| `closure2` concatenates kind+digest+tree+version+protocol+platform | **design law** | identity §3; `identity-schemas.v3` `$defs/closure` |
| `manifestDigest` is component-manifest body, envelope excluded | **design law** | identity §3; schema `raw-artifact` annotation |
| Different tree/platform/selected component refused by delivery | **design law** | identity §3 sentence; owner = DR-103 v11 `platforms[]` + RJ-3 |
| Envelope authenticates component-manifest stored/preimage bytes | **design law** | envelope.2; `security-completion.v1` §2.2; RJ-4 |
| Catalog authenticates release digest + per-platform archive | **design law** | `catalog.schema.json` |
| Trust trio admits **that** `closure2` | **design law** | workflows-and-surfaces §2 |
| `verify_envelope` already-accepted `signers` | **TCB assumption** | `security_lifecycle_model_v1.py` header |
| `host.closures[].trust='admitted'` | **TCB assumption** | W projector docstring; detector-manifest schema description; v5 proposal; this assessment |
| `open_run_closure` compares tree to `platforms[]` | **not implemented** (ref) | `identity-model.v3` `raw-artifact` branch |
| DetectorManifestV1 **is** `closure.manifestDigest` preimage | **false against identity/DR-103** | W schema title/description; `parse_detector_manifest_body`; projection-contract §13 |

---

## 5. Closed receipt (no second verifier, no second body)

Because (3) has no signed association owner for the listing bytes, do **not** mint a second envelope domain or a security copy of DetectorManifestV1.

After existing crypto TCB association of the **component** manifest (envelope + catalog + v11 delivery + trust-trio on `closure2` *C*):

```
DetectorCompatibilityReceiptV1 = {
  closureId,          // admitted closure2 (already includes tree/platform/protocolMajor)
  manifestDigest,     // identity raw-artifact of the component-manifest body (= C.manifestDigest)
  admissionOrigin     // retained-generation | installed-signed-release | signed-closure-bundle
}
```

Rules:

- Receipt exists only if *C* is already admitted by the trio. Missing / revoked / protocol-or-platform-incompatible → no receipt (`pivot-detector-unavailable` / `pivot-closure-revoked` / `pivot-closure-incompatible` remain).
- Parse DetectorManifestV1 **only** under a receipt, from host-retained listing bytes that are **not** `closure.manifestDigest`. Keep the single W `$id`. Empty `compatibleClosures` is a complete listing; absent/non-family listing is “no declaration,” not an empty listing.
- Do not put `tree`/`platform`/`protocolMajor` on the listing body. They are *C*’s. Do not put `signatureVerified` on the receipt.
- Do not treat catalog `manifestDigest` match as admission of a swapped-tree `closure2`.
- W v11 `project_admitted_detector_compatibility` already has the receipt **shape** (`closureId`, `manifestDigest`, optional `trustOrigin`, plus a copy of descriptor tree/platform/protocolMajor). The remaining defect is still hashing DetectorManifestV1 as `closure.manifestDigest` and taking tree from the object-map descriptor under a TCB `trust` flag. This owner does not edit W.

v5 `DetectorCompatibilityProjectionV1` is this receipt plus `compatibleClosures`. Keep the listing as the W body; do not also claim it is identity’s component-manifest preimage.

---

## 6. SEAL / array (read; not re-executed)

Root prefix helper: `_RUN3 = re.compile(r'^run3:[0-9a-f]{64}$')` with `fullmatch` (`security_lifecycle_model_v1.py`). Trailing newline is `SEAL_RUN_ID_INVALID`. Adapter case `prefix-trailing-newline-refused` present. `analysis-seal-root.v1.json`: 9/9 `passed: true`, not product qualification. Official pin-gated suites **not** run. Adapter **not** re-run this turn. User-stated array 105 after 3 sequence annotations not re-measured here.

---

## 7. Chapter amendment

One paragraph, `security-and-lifecycle.md` S1, immediately after the signed-document/admission sentence. States inheritance via admitted `closure2` after component-manifest TCB; DetectorManifestV1 must not occupy `closure.manifestDigest`; receipt after association; `trust='admitted'` is TCB. Native-evidence and admission-and-qualification unchanged this turn.

W files, identity model/schemas, pins, official checkers: not modified.
