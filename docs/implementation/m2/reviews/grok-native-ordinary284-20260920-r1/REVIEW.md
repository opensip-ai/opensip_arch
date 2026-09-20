# Independent review — ordinary member signatures and finite revocation union 284

**Standing:** bounded native-Rust review of frozen `native-ordinary-quorums-checkpoint-284`. Authenticates ordinary catalog, revocation-list, and component envelopes under a **supplied** signing root, then rechecks every internally verified group against the **finite union** of retained and incoming key revocations, on the **same** 283 operation Budget. **Not** root-chain/current/history admission, catalog/component semantic body admission, current revocation population, time, accepted-role effects, custody, or M3–M6. All root pairs, **including the supplied signing-root pair**, remain explicitly unresolved. Zero root signatures are intentional. Archived 283 (`df1532f6…71ad`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5707920 B, 530 members, SHA256 `adbdba19b9259064063c0c397cfe1cf8fc37183927b9e3439132c1d17d8c122d`**. Pin, tar, member count, and every `subject.json` hash matched **before** extract; extract rehashed **530/530**. Product-inputs **428/428** live-equal.

Nested parent 283 pin `95ef4502…fff5` (5626836 B / 584 / 426 files) equals the reviewed 283 freeze; live trial tar still matches; `trust-before.rs` equals that 283 `trust.rs`. Nested 265 `73c3b3f5…86df`. `Cargo.lock`, `lib.rs`, `trust_ordinary_inventory.rs`, and 283 fixtures unchanged.

Product vs 283: **428** files, **425** unchanged, **1** changed (`trust.rs` `2c1fcb78…fa46` — `include!("trust_ordinary_quorums.rs")`), **2** added (`trust_ordinary_quorums.rs` `e8151c7f…018d`, `ordinary284.ndjson`). No public API. No isolated-host/OS qualification rerun.

---

## What 284 adds

`ordinary_quorums::prepare` calls 283 `ordinary_inventory::prepare` on the same Budget. The BUNDLE proof is already 282-authenticated. Catalog and component envelopes use `verify_envelope` with their actual kinds (not a Payload shortcut), binding raw body, metadata preimage, role, and delegated namespace. The revocation owner admits the full closed list, actual calendar timestamps, and exact `rootVersion`, then verifies ROOT signatures. `keyId` subjects require the exact lowercase 64-hex codec; namespace/release/catalog subjects are **not** keys.

Every initially verified group must be `Met` after the supplied retained-key filter. A finite **second** pass builds `union = retained ∪ incoming keyIds` and `filtered_again(&union)` on **BUNDLE, catalog, list, and every component**. The newly delivered list does **not** exempt itself. No recursive trust discovery, extra physical read, or mutable current-trust lookup.

Root `EnvelopeKind::Root` pairs are skipped for signature admission and appended to `unresolved_roots`. Invalid root signatures therefore cannot become root authority through this owner.

`Evidence` owns the complete 283 result, admitted list, union set, each filtered group's kind/path/threshold/message/signers, and every unresolved root path after inputs and Budget drop.

Catalog/component bodies in these fixtures are deliberately minimal and **not** semantically admitted; the next owner must validate those bodies and catalog joins.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo clean -p opensip-security` then `cargo test -p opensip-security` | **230/230**, `Compiling opensip-security`, includes `ordinary_quorums::tests::actual_ordinary_member_signatures_and_union_preserve_shared_budget_evidence` |
| Exact live | `cargo test --workspace` | **529** passed (matches frozen 527 unit/integration + 2 compile-fail docs) |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | `rustfmt --check --edition 2024` on all **4** include files | **pass** |
| Exact live | 13 compiled r1 controls + baseline | **14/14**; core fields/patches/source SHA-equal frozen `mutation-check-r1` |
| Exact live | Python source/fixture probes | **26/26** |
| Inspected | 46 signed cases / 12 initial / 12 repeated | baseline 12 objects / 31 edges / 16239 bytes; repeat 12/62/16239; 12 physical captures |
| Inspected | test-only helper compile fix | `tests-before-local-helpers.rs`; production unchanged |
| Inspected | 277 workspace 515+2 | predecessor; this checkpoint **did** rerun workspace (529) |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): `omit-union-payload`, `omit-union-catalog`, `omit-union-revocation`, `omit-union-manifest`, `omit-union-threshold`, `discard-incoming-population`.

First fail **other** (not exploit proofs):

- `discard-retained-population`: owned union missing retained keys (set mismatch, not `left: true`).
- `nonkeys-treated-as-keys`: `left: false` / `right: true` (over-refusal of `keylike-namespace-not-key`).
- `lose-unresolved-roots`: `[]` vs `["root.json"]`.
- `root-pair-misclassified-as-admitted`: `left: false` / `right: true` (tries to verify zero-signature root as a member group).
- `wrong-member-signature-route`: `left: false` / `right: true` (Payload route over-refuses Catalog/Manifest).
- `lose-owned-group-path`: `None` vs `Some("catalog.json")`.
- `omit-failure-latch`: counters `(12, 62, 16546)` vs `(12, 31, 16546)`.

Frozen `mutation-check-r1` was not overwritten. r1 baseline SHA is current `trust_ordinary_quorums.rs` `e8151c7f…018d`.

---

## Focused findings

### Finite union second pass includes BUNDLE and the list itself

Omitting any of Payload/Catalog/Revocation/Manifest from the second pass is a **wrong admission**. Filtering only with the original retained set (`discard-incoming-population`) is also a wrong admission: incoming keyIds must be able to drop a previously Met group, including the list that carried them.

### Non-keys are not keys

Only `subjectKind == keyId` with a valid hex32 codec enters the union. Treating all subjects as keys over-refuses `keylike-namespace-not-key`. Namespace revocations are inert here.

### Supplied root stays unresolved

`EnvelopeKind::Root` never enters `verify_envelope` in this owner. `root-pair-unresolved-with-invalid-signatures` and `additional-root-remains-unresolved` stay successful with those paths listed. Misclassifying a root pair as an admitted member over-refuses the valid zero-signature root fixture.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | not in `lib.rs`; included from `trust.rs` |
| 283 first | `R::prepare` on the same Budget |
| Union | `revoked.clone()` then incoming `keyId`s; `filtered_again` on all groups |
| List self-exemption | comment + `incoming-list-cannot-exempt-itself` fixture |
| 46/12/12 | asserted and counted |
| Four-kind shortfalls | payload/catalog/revocation/manifest present |
| Deferred semantics | `catalog-and-manifest-semantics-pending` |
| Test-only compile fix | beforeimage retained |

---

## Remaining (do not count closed)

Ordinary root-chain/current/history admission; complete catalog/component semantics and identity/digest/namespace/constraint joins; current revocation population and non-key effects; time/accepted-role effects; physical capsule/artifact/repair/command integration; private policy custody/absence/adoption; fences/census/durable writers; runtime/source selection; M3–M6. These are private review candidates, not shipped behavior.

---

## Verdict

- [x] Archive/pins/members verified. 428 product files: 425 unchanged vs 283. Nested 283/265 pins match live trial archives.
- [x] **230** security tests after `cargo clean -p opensip-security`, **529** workspace tests, Clippy, cargo fmt, rustfmt of all four include files. Thirteen compiled r1 controls behave as documented (six wrong admissions; seven other-first).
- [x] Same-Budget 283 inventory; catalog/list/component crypto; finite retained∪incoming key union; list cannot self-exempt; all roots including supplied remain unresolved.
- [ ] **Not** current-root/chain/population, catalog/component body semantics, time, custody, operational grant, or product installation.
