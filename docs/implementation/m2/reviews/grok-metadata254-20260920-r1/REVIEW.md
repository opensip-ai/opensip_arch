# Independent review — recovery catalog/component metadata 254 r1

**Standing:** bounded frozen-byte review of `recovery-metadata-wip-254-r1`. **Not** full metadata admission, staging, current registry/time/floors, native publication, or 7-suite relocation. Owner assistance (`OWNER.md` `8b148484…5e36`, `CORRECTION.md` `480bacd9…91cf`) is a **separate** report and was not edited. 253 review unchanged (`dcb6b43b…3169`).

Python 3.12.13 `-I -B`, Unicode 15.0.0. OpenSSL 3.6.3. Siblings reconstructed from verified 253/252/251/250/248 extracts. Frozen fixture/variant/key directories were not overwritten.

---

## Verification

Frozen archive: **121232 B, 116 members, SHA256 `a22c65bd13be119207a49af3252bfe35af9846ff5b4e79dd1ae0ecfbc9d45a01`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 116/116. Standing: Incomplete WIP.

`metadata_reference.py` SHA256 `f4082c50ad60ecdeb1d8b9ed16fafa1b24050893b64a5e0a5b0b1a88565c5076`. Local `dependency-pins.json` 9/9. Quorum adapter is **one** internal return member `retainedMetadata` over pinned 253 source `d708990d…e788` (`quorum-adapter-delta.json` rebuilds exactly). No caller crypto facts, no extra `Verifier.verify`, no new `Operation` capture.

Included keys are **TEST ONLY**. Helpers reproduced **250 42 / 252 32 / 253 35** while minting them.

---

## What 254 binds

Same `Operation` as 253. Adapter returns already-prepared retained metadata; body checks allocate **no** fresh captures. Catalog: existing `I.CATALOG` shape, integer `catalogSchema`, calendar `issuedAt < expiresAt`, unique `(stableId, publisher, sourceClass, version)`, completed SemVer + `MF.interval` on `hostCoreConstraint`.

Each **presented** component: full inherited structural checker `check_manifest_completed_v1.validate` (not a parallel schema). Host `manifest_contexts` keys must equal presented manifest paths; allowed fields only `approvedExceptions` / `hostClassificationMap` / `liveNames`; `reservedNames` taken from **signed catalog** `reservedRootCommands`. Context custody/current registry remain pending. Component cannot self-approve classifications. `verifyArtifacts` / preview flags refused as extra context fields.

Then unique catalog tuple match; `body.publisher ==` already-verified envelope `namespace`; exact **raw** body hash, **canonical** preimage, **raw** envelope hash, and **exact** `hostCoreConstraint`. Unpresented catalog releases are allowed (corpus case). High `rootVersionRequired` / `revocationVersionRequired` and old catalog expiry **pass** this slice; activation minima stay pending (215 B.5). v8 `solve` ≥ law is **not** reimplemented here.

Standing `authenticated-recovery-catalog-component-bindings-only` with six pending owners (host context/registry; policy/repair/artifact; retained revocation/non-key subjects; other roots; floors/compatibility/S4; command/role/native publication).

---

## Reproduction

Fresh `metadata-fixtures-live` and work-copy `variant-fixtures-r1` / `metadata-variants-r1`. Frozen generated keys/results not overwritten.

| Corpus | Result |
|---|---|
| `check_inherited.py` | **187 / 187**, adapter delta exact, Unicode 15.0.0 |
| `check_metadata.py` | **48 / 48** equal frozen `metadata-fixtures-r1/metadata-report.json` |
| Counters | objects **14**, edges **40**, bytes **21470** |
| `check_variants.py` | **9 / 9** core-equal frozen results |

Controls: omit structural `MF.validate`; publisher/namespace; raw body / preimage / envelope digest; compatibility; duplicate tuple; catalog interval; outer fail-stop. Baseline refuses; mutant returns incorrect bounded standing. Variant path SHA differs from local `S=Path` rewrite.

---

## Independent probes / source limits

| Probe | Result |
|---|---|
| Adapter vs 253 source | single `retainedMetadata` splice; rebuild equal |
| Signature rerun / extra Operation | absent in `metadata_reference.py` |
| Exact required-version pairing | **not** in 254 (deferred pending owner) |
| Reverse “ship all catalog releases” | **not** implemented; extra release case **passes** |
| Host context field lock | extra `verifyArtifacts` refused |
| Self-classification without host map | refused |
| Raw digest vs preimage | **separate** joins |
| Old catalog / requiredVersion 999 | **passes**; floors pending |
| Policy/artifact | pending owner asserted |

v8 line 171 ≥ minima remain **outside** this slice (activation). A naïve `solve(` substring on `metadata_reference.py` matches `.resolve(`; 254 does **not** call `compatibility-selection-model.v8.solve`.

No contrary source was found that would make unpresented catalog rows required or turn 215 B.5 into exact root/list pairing. Owner-assistance equality/reverse-completeness inferences stay **non-normative** (see `CORRECTION.md`).

---

## Remaining (do not count closed)

Host context custody and current registry identity/retirement; policy/repair/artifact closure; retained revocation completeness and non-key subjects; other-root chain context; held-root ancestry, floors, current compatibility windows, S4; command/role/batch and native publication. Fixture policy/artifact bodies remain unverified.

---

## Verdict

- [x] Archive/pins/members verified. **187 / 48 / 9** reproduced. Helpers 42+32+35 observed. Counters 14/40/21470.
- [x] Reuses full completed manifest checker (not a 251-extraction hole) and 253 quorums on one Operation. Catalog/component joins match presented members only; activation ≥/expiry pending.
- [x] Independent checks: adapter delta, no crypto rerun, host context lock, unpresented releases allowed, raw vs preimage distinct, deferred floors.
- [ ] **Not** full member admission, staging, current trust, or native authority.
