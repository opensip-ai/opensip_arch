# Independent review — native incoming recovery union 266

**Standing:** bounded native-Rust review of frozen `native-incoming-union-checkpoint-266`. Finite retained|incoming key union and one conservative second filter over already-verified recovery signature groups, after 264 inventory. **Not** catalog/component body semantics, publisher↔namespace↔catalog joins, complete manifest checker (future 254 owner), current/retained population, non-key effects, other-root context authentication, ancestry/floors/S4, role/batch/whole-image, native custody/fence/slot/census/durability/writers, source selection, or M3–M6. Archived 264/265 dual review (`77d081e5…d1ac`), length investigation (`367ae8b1…9b96` + `CORRECTION.md` `efd4d80f…f428`), and 263 (`ba7895f5…dca9`) were not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **4535428 B, 519 members, SHA256 `a4d4a473bf2b44946bff6da34caaf3dc78b47a0d8efa2979b26453836ef0ca86`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 519/519. Product-inputs 373/373 live-equal.

Parent 264 pin `1e505a86…2d08` (4431648 B / 513 / 371 files) matches reviewed 264. Nested 265 `73c3b3f5…86df`, 253 `164dd2fa…f8b7`, 252 r2 `3816972f…ccff`, 250 r2 `dbf1aa27…cf85` match reviewed archives. Included 250 `check_authorization.py` `44a38c7d…cea2b` and 253 `check_quorums.py` `78f7aaf8…6a73` equal those helper extracts.

Product vs 264: **373** files, **370** unchanged, **1** changed (`trust.rs` `9847b43a…9be3`), **2** new fixtures (`incoming-union266-cases.ndjson`, `incoming-union266-isolated-root.ndjson`). `trust-before.rs` equals 264 `trust.rs` (`45877753…fb9d`). Inherited fixtures unchanged.

---

## What 266 adds

Private `incoming_recovery_quorums::prepare` is `budget.scope(|b| prepare_inner(...))` and calls 264 `retained_recovery_payload::prepare` **once** on that same budget.

First-pass proofs (264 authorization, replacement self-ROOT, BUNDLE) seed three groups via `QuorumReport::filtered_again(&empty)` — clone of immutable proof facts, not a caller signer array and not new crypto. Catalog and component envelopes then authenticate under the validated **replacement** root and the supplied retained-key filter. Revocation uses existing `admitted_revocations::verify_revocation` (full list shape/calendar/exact `rootVersion`/ROOT threshold + retained keys). After that reused list crypto, `keyId` subjects must be strict lowercase 64-hex (`decode_hex32`). Reference 253 checks the same codec **before** list crypto; both reject before union/time/effects. No private error-order claim.

One finite `retained ∪ incoming keyId` set refilters **all six** groups, including the list’s own group; each must remain `Met`. `filtered_again` only removes previously verified surviving keys; it preserves root digest, message, namespace, role, and threshold. No new store read, recursive list evaluation, or current-time/effect call. Traversal follows signed manifest order (rootChain, catalog, revocation, manifests). Non-replacement roots are recorded as `unresolved_roots` and never authenticated under the replacement. Non-key list subjects stay in owned list bytes and are not union keys.

Evidence owns 264 retained documents, list evidence, final groups, and the union. Original first-pass proofs remain on the 264 bundle object, distinct from final groups. Neither is activation or current authority. Module/`Error`/`Evidence` are not `pub` (`lib.rs` does not export them).

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **190/190** (264’s 189 plus this one test) |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 8 compiled controls + baseline | **9/9**, SHA-equal frozen `mutation-check-r1` |
| Inspected | 37 signed cases / 13 positive | frozen fixtures from 253 helpers vs 265 `recovery_quorums`; native matches expected blobs |
| Inspected | 13×6 group identities | **78** (kind/path/threshold/surviving signers/root digest/message/namespace/role) |
| Inspected | baseline counters | objects **14**, edges **40**, bytes **18414** |
| Inspected | 264 workspace 486+2 | predecessor receipt only; not rerun |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): skip union filter on RA (`incoming-revokes-old-recovery`); self-ROOT (`isolated-self-root-loses-signer`); BUNDLE (`incoming-revokes-bundle`); catalog; component/manifest.

First fail **other** assertions (not exploit proofs):

- `skip-union-revocation` (LIST): surviving-key set on coherent positive `isolated-self-root-unaffected` (3 vs 2 signers). Isolated self-ROOT cases exist so a list failure cannot mask that control.
- `omit-retained-keys-from-reported-union`: returned union (`unrelated-revocations-preserved`).
- `omit-unresolved-other-root`: returned unresolved path (`other-root.json`).

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | module/`Error`/`prepare` not `pub` |
| `filtered_again(&empty)` then later empty | cannot restore removed keys; digest/message/threshold/namespace preserved |
| `keyId` codec | lowercase `[0-9a-f]{64}` only; uppercase/short/text refuse `KeySubject`; empty subject hits list **shape** first |
| Namespace / keylike-namespace entries | not inserted into union |
| Other-root pair | unresolved; six groups still replacement-only |
| Store cleared after success | owned closure/list bytes remain |
| 253 vs native codec order | 253 before list crypto; 266 after `verify_revocation`; both before union |

Catalog/component **body** publisher and catalog-tuple joins are not asserted here (commented as a later 254-derived owner).

---

## Remaining (do not count closed)

Catalog/component and packaged-policy semantics; complete current+incoming population and non-key effects; other-root historical/current context; held custody/ancestry/floors/S4; role/batch/whole-image; native fence/slot/census/durability/writers; source/runtime selection; M3–M6. Host adapter still owns cap-before-allocation and custody. 266 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. 373 product files: 370 unchanged vs 264. Nested 264/265/253/252/250 pins match reviewed archives.
- [x] **190** security tests, Clippy, and fmt reproduced. Eight controls behave as documented (five wrong admission; LIST skip first fails a positive signer-set; two returned-fact first).
- [x] Same-budget 264 prepare; conservative union refilter of six groups including the list; other-roots unresolved; no public API.
- [ ] **Not** catalog/component body admission, current authority, native custody, or product installation.
