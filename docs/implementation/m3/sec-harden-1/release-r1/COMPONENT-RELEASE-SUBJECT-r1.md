# COMPONENT-RELEASE-SUBJECT r1: how a component release is spelled as a revocation `release` subject (successor record)

**Author:** claude-sec-predraw-1 (w35), Claude Opus 5.5 / high, R3-FRONTIER.
**Authority:** LD-Q-189 (`coordinator/msg-ldq189.txt`, sha256
`c92b833b49a37be12b8bcdcee7c02275c680b99d5d6beed88b1b52e516761b0a`): option 1. "The open law point, the subject
spelling, is decided by an R3 law call." The coordinator adopts it by receipt on an R3 ADOPTABLE score.
**Status:** proposed. It is scored as its own line in SEC-PREDRAW-1's r3 request.
**Pins:** product `462a7a7e9019aeada6ef0a3ce87b5b6ab8671666`; architecture `342222ffe1586d254249a9ffe41a085f6bc07e99`.

## 1. The gap (verified)

- **The law** names `release` as a revocation subject kind, but never defines it for a component:
  - security-completion v2 (`docs/coop/completion/security-completion.v2.md`:339-340): "Revocation list
    `opensip-revocation.1` ... entries by `subjectKind` `keyId | namespace | release | catalogSnapshot`";
  - the schema (`docs/coop/completion/security-schemas.v8/revocation.schema.json`, entries): `subject` is a string
    of 1 to 256 characters;
  - the product's validator (`crates/security/src/trust/root_payload.rs`:1606-1612) uses the same four kinds and the
    same 256-character bound.
- **The core release is spelled today as the running core's closure id.**
  - `InitialCore` refuses a `release` entry whose `subject` equals its closure (`trust/initial_core.rs`:916-928).
  - The fenced read's `admit_revocation` compares `release` subjects with `ViewClosure.release`, the running core's
    closure (`trust/current_trust_admission.rs`:914-933, :1094).
  - That closure is the core inventory's `closure2:` descriptor id (`trust/core_inventory.rs`:33-41).
- **No component release spelling exists.** So a `release` entry meant for a component is checked against nothing
  (LD-Q-189).

## 2. The candidates, against the coordinator's criteria

A good spelling has to meet four tests:
- a revocation **signer** can know it from the signed material;
- it is **stable across re-signing**;
- it is **unique per release**;
- it fits the **256-character** subject bound.

| Candidate | Signer can know it | Stable across re-signing | One per release | ≤ 256 characters |
|---|---|---|---|---|
| The identity tuple `(stableId, publisher, sourceClass, version)` | yes (catalog row) | yes | yes | **no**: `publisher` and `version` may each be up to 4,194,304 characters (`recovery_catalog.rs` `release_shape`, :97-110), and a tuple also needs an invented delimiter and escaping |
| A component closure id (C2a's `closure2` over a component descriptor) | **no**: it is computed per selected platform at C2a admission, and is not in the signed catalog | yes | **no**: one per platform artifact, up to 16 (`artifacts` 1..=16, :111-112) | yes |
| **`manifestDigest`** (catalog release row) | **yes**: it is a field of the signed catalog's release row (`recovery_catalog.rs` `release_shape`, :81-112, field list :86-96), and security-completion v2:301-302 lists it among `releases[]`' fields, "inside the signed preimage" (:305) | **yes**: it is the raw SHA-256 of the manifest **body**, so re-signing the envelope changes `envelopeDigest`, not `manifestDigest` (the reader checks `raw_sha256(pair.body()) == manifestDigest` separately from `envelopeDigest`, `trust_ordinary_metadata.rs`:349-363, the inventory path R10 runs) | **yes**: one body per release; every platform shares it | **yes**: exactly 64 lowercase hex characters (`root_payload.rs`:77-83 `hex`) |

## 3. The selection

1. **The component spelling.** A `release` revocation entry names a component release exactly when its `subject` is
   **byte-equal to that release's catalog `manifestDigest`**: the 64-character lowercase hexadecimal string as the
   signed catalog row spells it. There is no prefix, case folding or other transformation.
2. **The core spelling is unchanged.** It stays the running core's `closure2:` closure id, as `initial_core.rs`:916-928
   and `admit_revocation` already compare it.
3. **Consistency.** Each `release` subject is the release's own content identity: the core's closure descriptor id,
   or a component's manifest body digest. The two syntaxes cannot coincide. A `closure2:` id contains `:` and is not
   64 lowercase hex characters. So one `release` entry never names both a core and a component.
4. **Scope.** This defines only how a `release` entry names a component release. It does not change the schema, the
   other three kinds, the core's handling, or the list's monotonicity. Nothing new is admitted. The selection only
   lets an existing signed entry exclude a component.
5. **Its consumer** is SEC-PREDRAW-1 P-1 (LD-Q-189 option 1): a component whose release row's `manifestDigest` equals
   any `release` subject of the **same read's** admitted list is refused on the whole-view Continuation row,
   `Continuation("release:<manifestDigest>")`, mirroring `admit_revocation` (:928-933). The live observer's gap
   (`live_observation.rs`:695) is carry **CP-LIVE-OBS-COMPONENT-RELEASE** (LD-Q-189 item 5). This record does not
   change it.

## 4. Rejected alternatives

- **The identity tuple:** it is unbounded against the 256-character subject, and it needs an invented encoding.
- **A component closure id:** the signer does not know it, and it is per platform.
- **`envelopeDigest`:** it changes on re-signing, so a re-signed but otherwise identical release would escape
  revocation.
- **Prefixing, for example `manifest:<hex>`:** this adds a convention that signers would need to learn. The syntaxes
  are already disjoint (§3 item 3).

## 5. Controls (in SEC-PREDRAW-1's code round)

- **C-CRS-1.** A signed list with `{subjectKind: "release", subject: <manifestDigest of component i>}` refuses P-1 on
  the Continuation row. The same list without that entry admits.
- **C-CRS-2.** A subject equal to the component's `envelopeDigest` or `manifestPreimageSha256` does not refuse
  (different identities).
- **C-CRS-3.** An uppercase-hex spelling of the digest does not match (byte equality).
- **C-CRS-4.** The core's `closure2:` subject still refuses the core exactly as today, and never matches a component.
- **C-CRS-5.** A component release revoked under one platform's artifact is refused for every platform (one digest).
