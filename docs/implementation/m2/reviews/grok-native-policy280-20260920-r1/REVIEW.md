# Independent review — native effective permission-policy merger 280

**Standing:** bounded native-Rust review of frozen `native-effective-policy-checkpoint-280`. Pure private 265 v8 permission-policy narrowing on the **same** guarded operation Budget. **Not** native source capture/absence, selected project identity, custody, consent enforcement, policy adoption, packaged-policy operational authority, physical capsule/reference admission, clock/effects/populations, native fence/census/durable writers, source selection, or M3–M6. Archived 279 (`1545af9c…13b6`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5575964 B, 530 members, SHA256 `6aa2c69b09c171e50d803b310a0a8311c8b812b2fa7cc4edd8f7e3008edd9604`**. Pin, tar, member count, and every `subject.json` hash matched **before** extract; extract rehashed **530/530**. Product-inputs **419/419** live-equal.

Nested parent 279 pin `8b081b4f…4e9d` (5603648 B / 567 / 413 files) equals the reviewed 279 freeze; live trial tar still matches; `trust-before.rs` equals that 279 `trust.rs`. Nested 265 `73c3b3f5…86df`. `Cargo.lock` and `lib.rs` unchanged vs 279. Inherited 279 fixtures byte-identical.

Product vs 279: **419** files, **412** unchanged, **1** changed (`trust.rs` `60f76daf…60c4` — `include!("trust_policy.rs")` plus `pub(super)` on packaged `shape`/`prefix`), **6** added (`trust_policy.rs` `bc028e3b…da56` and five `policy280*` fixtures). No public API. No full workspace rerun (277 515+2 predecessor only).

---

## What 280 adds

Private module `effective_permission_policy` is included from `trust.rs` and is **not** in `lib.rs`. `merge(budget, global, context)` receives owned JSON through `Source::Body` or `Source::Missing` and a closed `Context::Global` / `Context::Project`. Missing global becomes EMPTY_GLOBAL (`policyScope=global`, empty grants/denies/consents). Missing policy for a selected project becomes EMPTY_PROJECT: **no** global grant inheritance. Global context has no project source. These values do not prove native file absence, a selected project, custody, consent, or adoption.

Both selected sources run the existing **metadata** canonical profile (4 MiB, depth 64, NFC, signed integers) then complete v8 permission-policy shape **before** semantic merging. Scope labels, normalized grant path prefixes and duplicate grant/deny pairs collect sorted unique diagnostic reasons. Denies from either source dominate. A project can only narrow a corresponding global grant. Omitted scope fields inherit; supplied empty arrays narrow to nothing; path containment is whole-segment (`child == parent` or `child.strip_prefix(parent)` then `/`); `stateClass` must agree; other scope arrays must be subsets. Global-only scope array order is retained; merged project arrays are sorted. Any widening refuses the **entire** result.

Consents use exact reference `json.dumps(sort_keys=True)` **default** ASCII-escaped, spaced-key encoding (`quoted_ascii`) for dedup/intersection; consent arrays keep given order. Source digests use `opensip.metadata.policy.1`; the result uses `opensip.metadata.policy-effective.1`, both with a NUL separator and canonical bytes. `Effective` owns source documents, body, canonical bytes and digest after inputs and Budget drop.

Work stays in `budget.scope(|_| { ... })` with **no** `Budget.load` / invented object or edge charges. Tests retain an earlier object and two edges, assert counters stay `(1, 2, 5)` across repeated merges, and require subsequent use to fail after any refusal.

**Derived output bound:** source admission still stops at 4 MiB. Effective output is an internal derived value capped at `2 * MAX_BYTES + 1024`. A real 4,194,303-byte source produces 4,194,409 effective bytes globally and 4,194,471 with a selected inheriting project. Six boundary cases cover source sizes cap−1 / cap / cap+1 in both contexts; cap+1 is refused by the explicit native source profile (the isolated reference merger would accept those two). Production merging did not change for the 252→251 fixture adapter or the Rust 2024 test-pattern compile fix.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **224/224** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | `rustfmt --check --edition 2024` on `trust_policy.rs` | **pass** (include-file; Cargo fmt does not traverse it) |
| Exact live | 20 compiled r1 controls + baseline | **21/21**; core fields/patches/source SHA-equal frozen `mutation-check-r1` |
| Exact live | Python source/fixture probes | **38/38** |
| Inspected | 1081 ordinary rows / 251 positive | both contexts; missing sources; grant/deny; inherited 269 shape/bounds; consent ASCII-vs-Unicode |
| Inspected | 6 large-boundary cases | source 4194303/4194304/4194305 × global/project; last pair refused |
| Inspected | 265 v8 oracle SHA `3e28bc7b…6d40` | fixture report; not rerun here |
| Inspected | 277 workspace 515+2 | predecessor only; not rerun |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): `scope-widening-allowed`, `state-class-widening-allowed`, `text-prefix-not-segment`, `skip-duplicate-pairs`.

First fail **other** assertions (not exploit proofs):

- `missing-project-inherits-global`: body mismatch `absence/True/False/True` (grants present vs EMPTY_PROJECT empty grants).
- `ignore-global-denies` / `ignore-project-denies`: deny list empty vs expected union.
- `deny-after-widen-check`: `left: false` / `right: true` (valid mismatch, not `left: true`).
- `skip-path-admission`: later `POLICY.PROJECT_WIDENS_SCOPE` vs `POLICY.PATH_PREFIX_NOT_NORMALIZED`.
- `skip-scope-label`: missing `POLICY.SCOPE_LABEL` among collected reasons.
- `skip-source-shape`: panic/later shape path.
- `consents-use-global`: extra consents vs intersection.
- `consents-utf8-sort`: `consent-ascii-order` body mismatch.
- `global-list-order-sorted` / `project-lists-unsorted`: array order mismatch.
- `source-domain-wrong` / `effective-domain-wrong`: digest mismatch.
- `drop-owned-sources`: sources `[]` vs owned documents.
- `derived-source-cap-overrefusal`: over-refusal of valid cap−1/cap derived output (`added=0` `left: false` / `right: true`).
- `omit-failure-latch`: follow-up not `BudgetError::Closed`.

Frozen `mutation-check-r1` was not overwritten. r1 baseline `sourceSha256` is current `trust_policy.rs` `bc028e3b…da56`. No escaped controls. Initial driver trailing-newline assert beforeimage is retained (`check-policy-mutants-before-trailing-newline-fix.py`).

---

## Focused findings

### Missing selected project is EMPTY_PROJECT, not inheritance

`Context::Project(Source::Missing)` still calls `source(..., "project")`, which materializes empty project policy. The `missing-project-inherits-global` mutant treating Missing as `None` (global-only merge) first-fails on body mismatch, not as `left: true`. Deny-by-absence is therefore present; it is not native proof of a missing file.

### Derived cap is separate from source 4 MiB

`effective_bytes` uses `2 * MAX_BYTES + 1024`. A 4,194,303-byte source yields 4,194,409 / 4,194,471 effective bytes. Cap+1 sources (4,194,305) refuse in both contexts. Tightening the derived cap to the source 4 MiB over-refuses the valid large-output tests.

### Consent encoding is Python default JSON, not UTF-8 sort

`consent_key` matches `json.dumps(sort_keys=True)` default ASCII/`", "`/`": "` separators. `consents-utf8-sort` first-fails `consent-ascii-order`. Array order is meaningful.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | merger not in `lib.rs`; included from `trust.rs` |
| Packaged validators | `shape`/`prefix` now `pub(super)` |
| Pure scope | no `b.load` |
| 1081/251 | asserted in tests and counted in fixtures |
| Six bounds | cap−1/cap admitted; cap+1 refused |
| 252→251 beforeimage | `policy-fixtures-before-null-context-fix.json` positive 252 |
| Rust 2024 test-pattern beforeimage | `policy-before-test-pattern-fix.rs` present |
| Python dumps separators | spaced ASCII default |

---

## Remaining (do not count closed)

Private source capture/absence and selection; adoption/consent enforcement; physical capsule/reference admission; clock and accepted-role effects; current/historical population; ordinary metadata authentication; artifact/repair semantics; full operation composition; native custody/fences/census/durable writers; runtime/source selection; M3–M6. These are private review candidates, not shipped behavior.

---

## Verdict

- [x] Archive/pins/members verified. 419 product files: 412 unchanged vs 279. Nested 279/265 pins match live trial archives.
- [x] **224** security tests, Clippy, cargo fmt, and include-file rustfmt reproduced. Twenty compiled r1 controls behave as documented (four wrong admissions; sixteen other-first). No workspace rerun.
- [x] Missing=empty; deny union; whole-segment paths; Python `json.dumps` consents; domain-separated digests; derived `2*4MiB+1024` bound; same-Budget fail-stop with no invented I/O.
- [ ] **Not** native source/absence/custody/project selection/consent/adoption, current operational authority, or product installation.
