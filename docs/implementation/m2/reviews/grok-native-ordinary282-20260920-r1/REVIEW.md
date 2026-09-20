# Independent review — authenticated ordinary BUNDLE under a supplied root 282

**Standing:** bounded native-Rust review of frozen `native-ordinary-bundle-checkpoint-282`. Real Ed25519 **BUNDLE** signatures on a payload-v1 ordinary manifest, bound to a current-125 DocRef on the **same** guarded Budget, under a **supplied** validated root and a **supplied** retained revoked-key set. That root has passed document validation; this owner does **not** establish current-root admission, chain/history, current population, time, filesystem custody, member authentication, or operational grant. Archived 281 (`94ed66e5…954a`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5609660 B, 568 members, SHA256 `4b832a3ab26c2d930d6fd39c41ed2d001a6c1e921ab9eee4232d8a033764a0eb`**. Pin, tar, member count, and every `subject.json` hash matched **before** extract; extract rehashed **568/568**. Product-inputs **424/424** live-equal.

Nested parent 281 pin `35fad575…cb24` (5538860 B / 498 / 422 files) equals the reviewed 281 freeze; live trial tar still matches; `trust-before.rs` equals that 281 `trust.rs`. Nested 265 `73c3b3f5…86df`. `Cargo.lock`, `lib.rs`, `trust_policy.rs`, and 281 payload fixtures unchanged.

Product vs 281: **424** files, **421** unchanged, **1** changed (`trust.rs` `7d1c5402…1550` — `include!("trust_ordinary_bundle.rs")`), **2** added (`trust_ordinary_bundle.rs` `d758dcab…736e`, `ordinary282.ndjson`). No public API (`ordinary_bundle` is not in `lib.rs`). No full workspace rerun (277 515+2 predecessor only).

---

## What 282 adds

`ordinary_bundle::authenticate` admits complete current-125 **DocRef** shape **before** I/O, then `Budget.load`s body and envelope as Objects (raw SHA + exact length; both reference edges charged even on cache hits). `SignedDocument` owns the raw pair. Full 281 `index_payload_shape` precedes object access; **only schema 1 and kind `ordinary`** take this route. Schema 2 recovery and the schema-1 legacy `recovery` **label** return `Error::Route`. Declared paths run complete preflight; **member bytes are not loaded**.

`verify_envelope` uses `CURRENT_ENVELOPE_READER` with `EnvelopeKind::Payload`: kind/domain/role/namespace, stored SHA, metadata preimage, root digest, cryptographic message. Verified signers are filtered by the supplied retained revoked-key set; filtered quorum must be `Met`. No caller `authenticated:` flag or substituted signer list.

`Evidence` owns root value/canonical/digest, DocRef, raw signed document, paths, envelope/quorum proof, and revoked population after inputs and Budget drop. Failure closes the same Budget.

Lexically shaped but impossible-calendar `issuedAt` is accepted **here**; time admission is a separate owner.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` after forced rebuild | **228/228**, including `ordinary_bundle::tests::actual_ordinary_signatures_refs_budget_and_owned_evidence_match_reference` |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | `rustfmt --check --edition 2024` on `trust_policy.rs` and `trust_ordinary_bundle.rs` | **pass** |
| Exact live | 13 compiled r2 controls + baseline | **14/14**; core fields/patches/source SHA-equal frozen `mutation-check-r2` |
| Exact live | Python source/fixture probes | **29/29** |
| Inspected | 66 signed cases / 9 initial / 8 repeated successes | root1/root2, threshold/revoked/unknown extra, bad sig/domain/role/ns/stored/preimage, coherent whitespace, schema2 refused, legacy recovery refused, lexical calendar, 7 top-level non-object/missing-field isolates |
| Inspected | r1 `omit-payload-shape` escape | expectedOutcome **false**, exit 0; later path/shape still refused malformed objects |
| Inspected | 59-row beforeimage | `ordinary-before-toplevel-cases.ndjson`; r1 driver/keys/logs retained |
| Inspected | 277 workspace 515+2 | predecessor only; not rerun |

**Live-test note:** the first `cargo test` against a copied 281 incremental target finished in 0.13s with **227** tests and did not compile `trust_ordinary_bundle.rs`. Touching sources forced `Compiling opensip-security` and **228** tests. Mutant replay used that rebuilt target. Do not treat the stale 227 run as 282 coverage.

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): `allow-legacy-recovery-label`, `accept-short-quorum`, `omit-portable-alias`, `omit-reserved-frame`, `omit-file-parent`.

First fail **other** assertions (not exploit proofs):

- `omit-full-docref-shape`: extra edge charge `(0, 1, 0)` vs `(0, 0, 0)` (load without DocRef admit).
- `omit-payload-shape` (r2): **panic** on signed non-object/missing top-level fields (`body-top-level/*`), not `left: true`.
- `omit-revoked-key-filter`: signer-set mismatch (revoked keys remain in `valid`).
- `wrong-envelope-route`: `left: false` / `right: true` (over-refusal of valid Payload).
- `lose-root-identity`: digest `00…00` vs actual root digest.
- `lose-owned-revoked-population` / `lose-owned-reference`: empty set / `Null` vs owned facts after drop.
- `omit-failure-latch`: counters `(2, 4, 1941)` vs `(2, 2, 1941)` (follow-up not closed).

Frozen `mutation-check-r1`/`r2` were not overwritten. r2 baseline source SHA matches current `trust_ordinary_bundle.rs` `d758dcab…736e` and `trust.rs` `7d1c5402…1550`. Production functions did not change between r1 escape and r2 fixture isolates.

---

## Focused findings

### Supplied root is not current-root authority

Tests call `admit(&q["root"], [true, true])` and pass that `ValidatedRootPayload` in. Success proves BUNDLE signatures under **that** root and the supplied revoked-key filter. It does not admit the root as current, walk history, or authorize members/catalog/list.

### Schema 1 ordinary only

`index_payload_shape` then `payloadSchema==1 && payloadKind==ordinary`. `signed-schema2-route-refused` and `body/legacy-recovery` are refused as `Route`. Allowing the legacy recovery label is a **wrong admission**.

### r1 payload-shape escape, r2 panic catch

r1 omitted `index_payload_shape`; later path/object checks still refused the original 59 malformed rows, so the control exited 0. r2 added seven actually signed `body-top-level/{null,scalar,bool,array,empty-object,missing-schema,missing-kind}` cases. The same omission now panics on `object(&manifest)` — caught, classified **other-first**, not a wrong-admission boolean.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | not in `lib.rs`; included from `trust.rs` |
| DocRef before load | `S::admit(DocRef)` then Objects body/envelope |
| Envelope kind | `CURRENT_ENVELOPE_READER` + `EnvelopeKind::Payload` |
| Revoked then Met | `filter_envelope_revoked` before quorum `Met` |
| 66/9/8 | asserted in tests and counted in fixtures |
| Isolates | 7 `body-top-level/*`; 59-row beforeimage |
| r1 vs r2 | omit-payload-shape escaped r1; r2 panic-caught |
| Calendar | `body/lexical-impossible-calendar` present |

---

## Remaining (do not count closed)

Ordinary retained inventory; root-chain/catalog/list/component authentication and finite-union recheck; current root/population/history; physical capsule admission; clock and accepted-role effects; artifacts/repair/commands; native private-policy custody/absence/adoption; fences/census/durable writers; runtime/source selection; M3–M6. These are private review candidates, not shipped behavior.

---

## Verdict

- [x] Archive/pins/members verified. 424 product files: 421 unchanged vs 281. Nested 281/265 pins match live trial archives.
- [x] **228** security tests (after forced rebuild), Clippy, cargo fmt, and rustfmt of both include files. Thirteen compiled r2 controls behave as documented (five wrong admissions; eight other-first). No workspace rerun.
- [x] Real BUNDLE signatures under a supplied validated root and supplied revoked-key filter; schema-1 ordinary only; DocRef+Budget loads; r1 payload-shape escape repaired by signed top-level isolates (panic, not wrong admission).
- [ ] **Not** current-root admission, full member authority, time, custody, operational grant, or product installation.
