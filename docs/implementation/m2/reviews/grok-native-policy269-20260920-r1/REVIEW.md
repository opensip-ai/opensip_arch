# Independent review — native packaged recovery policies 269

**Standing:** bounded native-Rust review of frozen `native-packaged-policy-checkpoint-269`. Closed v8 packaged permission-policy bodies as authenticated recovery inventory after 268. **Not** private global/project policy adoption, effective merge, consent approval, grant minting, artifact/repair semantics, current population, other-root contexts, held custody/ancestry/floors/S4, command/role/batch effects, native custody/fence/census/durability/writers, source selection, or M3–M6. Archived 268 (`b31771e1…065b`), 267, 266, and 264/265 were not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **4825912 B, 518 members, SHA256 `9e66cc48b712b5b07b0c763b63cdf0642a092f3486abd82f64b9e3778963f197`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 518/518. Product-inputs 386/386 live-equal.

Nested parent 268 pin `40fbfe5f…a5ba` (5001656 B / 587 / 383 files) equals the reviewed 268 freeze; `trust-before.rs` equals that 268 `trust.rs` (`c135af8f…4297`). Nested 265 `73c3b3f5…86df`, 257 `d1e3122e…c57a`, 254 r1 `a22c65bd…5a01`, 253 `164dd2fa…f8b7`, 252 r2 `3816972f…ccff`, 250 r2 `dbf1aa27…cf85` match reviewed archives. 250 helper `44a38c7d…cea2b`. 257 `check_policies.py` `6747b5a5…2252`.

Product vs 268: **386** files, **382** unchanged, **1** changed (`trust.rs` `25fd3948…7cad`), **3** added (`policy269-{signed,shape,boundaries}.ndjson`). Inherited 268 fixtures unchanged. `trust-before-test-qualification.rs` (`32c9c1c5…e69a`) is the compile-fix beforeimage (tests now call `admitted_roots::admit`; production `admit` for policy bodies is a different private fn). Mutation r1 is driver-error only (`insert(` vs rustfmt `insert((`); r2 selector-only.

---

## What 269 adds

Private `packaged_recovery_policies::prepare` is `budget.scope` and calls 268 `recovery_metadata::prepare` **once** on that budget, then **reloads** the same closure NodeRef and each `permissionPolicies` BlobRef through `Budget.load`. Cached physical bytes still charge reference edges (baseline **14/42/21548** vs 268’s 14/40/21470: +2 edges for the extra closure/policy loads). Empty packaged list is not a missing private policy. Same bytes at two paths remain two entries (no first-member shortcut). No policy envelope is invented.

`admit` closes v8 shape: `policySchema == 1`, scope `global|project`, grants/denies/consents bounds, closed grant/deny/consent/scope objects, exact permission tokens. Then: only `grant.scope.pathPrefixes` through `prefix()`; unique `(stableId, token)` independently on grants and on denies; `metadata_bytes` canonicality; domain preimage `opensip.metadata.policy.1` + NUL + canonical body. Stored raw SHA, that raw-policy domain digest, and any later effective-policy domain remain distinct.

**Prefix profile** (matches 258 `normalized_member_path`): nonempty, ≤1024 **UTF-8 bytes**, NFC, relative, no empty/`.`/`..` segments, no `\` or NUL. Drive-like `C:src`, device-like `CON`, trailing-dot/space **allowed** — do not reuse 268 package `path_ok` or 262 logical metadata path. Consent `resourceScope`/`endpointSet`/`checkIds` (and grant `programs`/`endpoints`/`variables`) stay unique schema strings with **Unicode character** widths. Canonical domain digest still refuses non-NFC on every string.

Evidence owns 268 metadata plus ordered `{path, blob, body, preimage}`. No public API.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **198/198** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 12 compiled controls + baseline | **13/13**, SHA-equal frozen `mutation-check-r2` |
| Exact live | prefix vs 268 `path_ok` | `C:src`/`CON`/`file.`/`file ` policy-admit, package-refuse |
| Inspected | 40 signed / 15 positive | baseline 14/42/21548; empty list; two policies; same bytes/two paths; drive/device/trailing-dot; Unicode byte-exact prefix; opaque consent; duplicate consent rows |
| Inspected | 376 schema cases (335+41) | structural perturbations + array/string/Unicode bounds |
| Inspected | r1 mutation driver | failed before any control; r2 selector only |
| Inspected | 268 workspace 493+2 | predecessor only; not rerun |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): skip exact discriminator (`policySchema` 0); skip prefix (`prefix-parent`); skip duplicate grants; skip duplicate denies.

First fail **other** assertions (not exploit proofs):

- `skip-second-policy`: count 1 vs 2 on `second-valid-policy`.
- `omit-repeat-closure-edge` / `omit-repeat-policy-edge`: counters 14/**41**/21548 vs 14/**42**/21548.
- `raw-sha-is-not-policy-domain` / `effective-domain-is-not-raw-policy`: preimage bytes ≠ `opensip.metadata.policy.1` digest.
- `schema-character-width-is-not-bytes`: valid Unicode-char width `string-unicode-chars/(pathPrefixes)` fails if measured as UTF-8 bytes.
- `package-drive-rule-overrefusal`: `prefix-drive-like-allowed` refused `PathPrefix`.
- `omit-outer-policy-latch`: follow-up prepare not `Err(Closed)`.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | module/`Error`/`prepare` not `pub` |
| 258 `_prepare` | same reload of closure + each policy blob; same domain `opensip.metadata.policy.1`; same grant/deny pair uniqueness; path prefix = `normalized_member_path` |
| Consent `/abs` or `..` in resourceScope | schema-only unique strings; not `prefix()` (`consent-resources-opaque-not-path-prefix` admits) |
| Opaque non-NFC string | canonical `NON_NFC_STRING` even when not a path prefix |
| Duplicate JSON key | parse `DUPLICATE_JSON_KEY` |
| Store cleared after success | owned catalog/policy bodies remain |

---

## Remaining (do not count closed)

Private-policy source adoption and effective merge; artifact/repair semantic closure; complete retained/current population and non-key subjects; other-root contexts; held ancestry/floors/S4; command/role/batch/whole-image effects; native custody/fence/slot/census/durability/writers; source selection; M3–M6. Packaged policy contents are evidence, not operational authority. 269 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. 386 product files: 382 unchanged vs 268. Nested 268/265/257/254/253/252/250 pins match reviewed archives.
- [x] **198** security tests, Clippy, and fmt reproduced. Twelve controls behave as documented (four wrong admissions; eight other-first).
- [x] Same-budget 268 prepare plus charged repeated refs; closed v8 body; policy-prefix profile distinct from 268/262; raw SHA ≠ policy-1 domain ≠ effective domain.
- [ ] **Not** policy adoption/merge, current authority, native custody, or product installation.
