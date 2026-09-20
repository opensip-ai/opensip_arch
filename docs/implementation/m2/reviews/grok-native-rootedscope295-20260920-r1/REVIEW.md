# Independent review — scoped members plus shared ROOT proof 295

**Standing:** bounded native-Rust review of frozen `native-rooted-scope-checkpoint-295`. Module-private `prepare_rooted` runs 294 `prepare_scoped` first, then the 289 captured-root kernel through `verify_shared` on typed 292 `SharedEvidence`. Presented first-ROOT quorum and ordered proper successors are filtered by the same finite union. Historical original envelope is SHA+length bound only. This is not bootstrap, current-head/BEGIN proof, signed time, completeness, host admission, grant, or product installation. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Archived 294 was not edited (visibility wording was corrected separately; beforeimage preserved).

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8385372 B, 922 members, SHA256 `b54b5bcf28b7a3a1ad3356b6baf498258084e3ddd7986f8c4567e946bd9af042`**. Standing: unselected private295 scoped members plus shared ROOT proof; current context and operational authority pending. Extract rehashed **922/922**. Product-inputs **448/448**. Nested parent 294 pin `89e5e903…b050` equals reviewed 294; live 294 trial tar matches. Nested 215 r14 `cd338af6…dd9c` / model SHA `9aa6e56b…d701` match. Nested 265 `73c3b3f5…86df` live-matches. Live 289 tar `45764043…bf03` matches the reviewed 289 freeze. Product vs 294: **448** files, **445** unchanged. Changed: `trust_ordinary_roots.rs` `423141df…c212`, `trust/ordinary_targets.rs` `d572c733…dd9e`. Added: `rootedscope295.ndjson`. `plan()` / `coordinate()` / `plan_from_contexts` production text is **byte-identical** to 294. `prepare_scoped` remains a module-private `fn` (not `pub(super)`); its body is **byte-identical** to 294. `prepare_rooted`, `verify_shared`, and `RootProof` are not in `lib.rs`. Frozen OWNER `d8165f14…19fa` (48217 B) differs from live OWNER; frozen OWNER is source, live untouched.

---

## What the composition does

289 is factored into `admit_original` (DocRef shape; body load; historical envelope SHA+len only; accepted-root identity) and private `verify_captured`. Existing `prepare` still calls **full** 284 `Q::prepare` with the **same** read order (admit_original → Full quorums → kernel) and still asserts `(42, 8, 8)`. `RootProof` owns original/projected DocRef, presented-first quorum, and exact chain.

`verify_shared` is `pub(super)`: `admit_original` then the **same** kernel on typed `SharedEvidence` retained/unresolved-roots/union. It does not restore all-component DR-112. Original accepted-root provenance remains an external premise.

`verify_captured`: first presented body equals accepted root; last body equals the C.3 signing-root; presented first envelope is `verify_envelope` under accepted keys then `filter_envelope_revoked(union)` and must be `Met`; successors `.skip(1)` enter existing `verify_root_chain` with that union; empty successors keep the original accepted DocRef; rotation projects the last captured DocRef. Historical original envelope is loaded (`let _original_envelope = b.load(...)`) and not reauthenticated under current keys.

Module-private `prepare_rooted` on the same Budget: 294 `prepare_scoped` first (293 inventory always; 290 availability from the exact shared union; unchanged 291 planner; COMPONENT message quorum only if T1 `remaining()[1]`), then `verify_shared(scoped.inventory.shared(), ...)`. New capture order is intentionally scope-first then original DocRef; old 289 order is unchanged. No target exclusion waives ROOT. Invalid selected COMPONENT still refuses; excluded RECOVERY/REVOKED and OLD-hit/key-loss still pass scoped inventory; a bad first ROOT or a bad proper successor still refuses when the component is excluded.

49 TEST-ONLY signed cases, **12/12** positives. Baseline 11 objects / 30 edges / 18839 B; repeat 11/60/18839; 11 captures. Oracle: exact 265 primary chain/crypto/schema plus the frozen 294 `scope` function AST-extracted from the verified script **without** executing fixture generation, plus exact 215 r14 model. Owned proof/scope facts are checked after input drop.

**Preserved failures (reference-only, production algorithm unchanged):**

1. `author-extraction-r1.log`: parent extract stopped before source edits because destination `verified-reference` was missing when `scripts/prepare_scope294_fixtures.py` arrived first. Full parent was rehashed and extraction resumed after creating the directory.
2. `security-integrated-r1` / `clippy-final-r1`: test-only `number(...) as i128` vs native `accepted_version(): i64` (`E0308` at the rooted test assertion). Corrected test cast; `ordinary-targets-before-test-version-type-fix.rs` and failed logs retained.

**Executed:** `cargo clean -p opensip-security` then **242/242** with `Compiling opensip-security` (includes 287/288/289/291/292/293/294 tests plus new rooted test). Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. 13/13 r1 compiled controls core-equal frozen `mutation-check-r1` (live baseline cargo skipped; unpatched roots SHA matched frozen baseline `423141df…c212`). Frozen mutant dir not overwritten (`report.json` SHA256 `d3cd3799…3ec3`).

**Controls (7 wrong conditional acceptances):** `omit-original-accepted-identity` (`accepted-doc-body-only-fork`); `omit-presented-first-identity` (`missing-accepted-prefix`); `omit-final-signing-root-identity` (`final-signing-root-is-not-last`); `omit-first-root-filter` (`first-filter-isolated`); `omit-first-root-quorum-requirement` (`short-first-signature`); `omit-successor-revocation-filter` (`successor-old-filter-isolated`); `discard-proper-successors` (`only-new-successor-quorum`). **6 other-first:** `treat-first-root-as-successor` (over-refusal `Chain(Gap(0))` on same-head); `replace-original-ref-on-same-head` / `preserve-original-ref-after-rotation` (projected-ref equality); `omit-original-envelope-capture` (counters 11/29/18839 vs 11/30/18839); `reauthenticate-historical-envelope` (over-refusal `FirstQuorum` on same-head alternate); `rooted-wrapper-failure-latch` (`bad-first-signature` latch). Not operational exploits.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 295 pins before extract | match |
| Nested 294 / 215 r14 / 265 / live 289 tars | match |
| 294 `prepare_scoped` / 291 planner bytes | unchanged |
| Old 289 `prepare` read order / 42 cases | unchanged |
| Live `cargo test -p opensip-security` | **242/242** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 295 r1 mutants | 13/13 frozen-equal; 7 wrong / 6 other |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

Immutable-core bootstrap; active-batch head-advancement barrier; exact current vs BEGIN/history/population qualification; signed time / minima / completeness / role-record effects; full host-admission gate; durable custody/fence/census/writers; source selection; M3–M6. 295 is a conditional accepted-head ROOT proof on already-scoped shared members, not complete ordinary import or cumulative approval.

---

## Verdicts

- [x] **295:** archive/pins verified; 289 kernel factored without changing full `prepare`; `verify_shared` reuses that kernel on 292 shared evidence; `prepare_rooted` is scope-first then original DocRef on one Budget; presented first-ROOT and proper successors filtered by the finite union; historical envelope not reauthenticated; excluded-component ROOT refusals held; extraction-directory and test-only i64 cast preserved as reference-only; 7/6 mutant classification; 242/242, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** bootstrap, current-head/BEGIN proof, host installation, signed time, completeness, grant, or product installation.
