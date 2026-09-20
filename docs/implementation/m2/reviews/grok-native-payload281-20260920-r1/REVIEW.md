# Independent review — native payload-v1 declaration and metadata index 281

**Standing:** bounded native-Rust review of frozen `native-payload-index-checkpoint-281`. Structural metadata **index** over a trusted capture callback for payload schema 1 (ordinary and legacy `recovery` **label**) alongside schema 2 recovery-only. **Not** signature authentication, root-chain admission, current revocation, ordinary import authorization, filesystem custody, bounded native capture, current operational authority, or M3–M6. A successful pair binds **bytes and a declaration**; it is not a signature result. Archived 280 (`0c92bf4f…97be`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5538860 B, 498 members, SHA256 `35fad57557dc030b264458734fdc608e66ca35afe427b7f52ef2b1077490cb24`**. Pin, tar, member count, and every `subject.json` hash matched **before** extract; extract rehashed **498/498**. Product-inputs **422/422** live-equal.

Nested parent 280 pin `6aa2c69b…9604` (5575964 B / 530 / 419 files) equals the reviewed 280 freeze; live trial tar still matches; `trust-before.rs` equals that 280 `trust.rs`. Nested 265 `73c3b3f5…86df`. Payload-v1 schema `payload.schema.json` SHA256 `bb9ab011b8b8d3f819552a7aa8924a1df9e6e00abf447f0a5e99330060b43da0`. `Cargo.lock`, `lib.rs`, and `trust_policy.rs` plus 280 policy fixtures unchanged vs 280.

Product vs 280: **422** files, **418** unchanged, **1** changed (`trust.rs` `3db6d4fd…4a17`), **3** added (`payload281-shape.ndjson`, `payload281-paths.ndjson`, `payload281-index.ndjson`). No public API. No full workspace rerun (277 515+2 predecessor only).

---

## What 281 adds

**Dedicated recovery verifier** still uses `payload_shape` → `payload_shape_version(v, true)`: schema **2 only**, kind `recovery`, nine member fields, closed root-recovery authorization `{body, envelope}` pair.

**Index dispatcher** `index_payload_shape` accepts a **strict integer** schema 1 or 2:

- Schema 1: eight closed member fields, **no** authorization pair. Kind may be `ordinary` or the legacy `recovery` **label**. A legacy label does not create recovery authority.
- Schema 2: recovery-only, nine fields, authorization pair.

Declaration preflight `admit` now uses `index_payload_shape`. Unicode 15 NFC/casefold, path alias, reserved frame names (`payload.json` / `payload.sig.json`), file-parent, and declared-edge checks are unchanged. Authorization body plus exact **once-listed** envelope is required **only when** the RA object is present (schema 2). Index stores `authorization_envelope: Option<String>` from the declaration; it does **not** synthesize a path for schema 1.

Member-path **shape** still uses lexical timestamps and the first-character-NUL schema quirk (`first char != '/'`, remaining chars `!= NUL`). Path **preflight** rejects any NUL (`path.contains(['\\', '\\0'])`). Slot-owned body kinds, listed-path presence, cached-content accounting, shared Budget and fail-stop remain.

Synthetic index envelopes have **invalid cryptography by design**. Pairing is byte+declaration identity only.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **227/227** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 12 compiled r1 controls + baseline | **13/13**; core fields/patches/source SHA-equal frozen `mutation-check-r1` |
| Exact live | Python source/fixture probes | **31/31** |
| Inspected | 537 shape rows / 37 positive | every row also asserts dedicated `payload_shape` ≡ `recovery==true`; 35 schema-1 positives; 2 schema-2 positives |
| Inspected | 28 schema-1 preflight / 7 positive | `payload281-paths.ndjson`; inherited 262 preflight remains 28/5 |
| Inspected | 54 actual `Index::new` cases | 25 built, 10 fully selected; owned pairs after drop |
| Inspected | 277 workspace 515+2 | predecessor only; not rerun |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): `dedicated-recovery-accepts-payload1`, `schema2-ordinary-kind-allowed`, `schema1-extra-authorization-allowed`, `schema1-root-chain-empty`, `recovery-auth-exact-pair-lost`.

First fail **other** assertions (not exploit proofs):

- `index-rejects-payload1` / `legacy-kind-overrefusal` / `schema1-requires-authorization` / `paths-use-recovery-dispatch`: `left: false` / `right: true` on schema-1 preflight or index construction (over-refusal).
- `schema1-missing-auth-panics`: panic asserting RA key on schema 1.
- `drop-declared-edge-charges` / `same-content-path-presence-skipped`: first fail inherited 280 packaged-policy **counters** (e.g. `(14, 30, 21548)` vs `(14, 42, 21548)`), because the mutant filter is `trust::root_payload::`.

Frozen `mutation-check-r1` was not overwritten. r1 baseline `sourceSha256` is current `trust.rs` `3db6d4fd…4a17`. No escaped controls. Initial fixture-generator keyword-spacing SyntaxError beforeimage is retained (`prepare-before-keyword-spacing-fix.py`). No production correction was required by that syntax error.

---

## Focused findings

### Structural indexing is not authentication

`Index::new` parses metadata, admits declaration paths, charges listed edges, and pairs retained bytes to declared SHA/kind. Comments and tests state there is no signature verification, filesystem custody, or current-authority claim. Dedicated `verify_recovery_bundle_document` still authenticates schema-2 recovery separately and still calls `payload_shape`, not the index dispatcher.

### Schema 1 must not grow recovery authority

Schema 1 has eight fields and no RA. Extra `rootRecoveryAuthorization` is a **wrong admission**. Requiring RA on schema 1 over-refuses valid ordinary/legacy rows. Allowing schema 2 `ordinary` is a **wrong admission**. Pointing `payload_shape` at `index_payload_shape` is a **wrong admission** of schema-1 rows into the dedicated recovery verifier.

### Optional RA path is not fabricated

`authorization_envelope` is `Option<String>` filled only when the member exists. Schema 1 does not invent an envelope path. Once-listed envelope equality remains schema-2-only.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | `index_payload_shape` / `payload_shape` not in `lib.rs` |
| Dedicated vs index | `payload_shape` = recovery-true; index dispatches 1 and 2 |
| Schema 1 kinds | `recovery` **or** (`!recovery` and `ordinary`) |
| Path NUL | preflight rejects `\\0`; member shape keeps first-char quirk |
| 537/37, 28/7, 54/25/10 | asserted in tests and counted in fixtures |
| Payload-v1 schema | `bb9ab011…3da0` |
| 280 policy | `trust_policy.rs` and `policy280.ndjson` byte-identical |

---

## Remaining (do not count closed)

Ordinary metadata authentication and retained-closure composition; physical capsule/reference admission; clock/accepted-role effects and population; artifact/repair/full command composition; native source custody/adoption; fences/census/durable writers; runtime selection; M3–M6. These are private review candidates, not shipped behavior.

---

## Verdict

- [x] Archive/pins/members verified. 422 product files: 418 unchanged vs 280. Nested 280/265 pins match live trial archives.
- [x] **227** security tests, Clippy, and fmt reproduced. Twelve compiled r1 controls behave as documented (five wrong admissions; seven other-first). No workspace rerun.
- [x] Schema 1 ordinary/legacy index without RA; schema 2 recovery-only with RA pair; dedicated recovery verifier stays schema-2; byte pairing is not signature authentication or current authority.
- [ ] **Not** metadata authentication, custody, current operational authority, or product installation.
