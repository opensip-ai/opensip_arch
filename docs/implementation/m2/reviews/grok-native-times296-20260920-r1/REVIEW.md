# Independent review — signed-time source projection 296

**Standing:** bounded native-Rust review of frozen `native-ordinary-times-checkpoint-296`. Module-private `prepare_times` runs the unchanged 295 rooted/scoped proof on the same Budget, then projects calendar-validated source times and presented DocRefs. This is not a complete pre-S4 producer, admitted operational clock, current-head/BEGIN proof, host admission, grant, or product installation. The known 289/295 evaluation-expiry-before-projection gap is documented separately in `ORDERING.md` and is **not** closed by this checkpoint. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Archived 294/295 reports were not edited.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8489248 B, 926 members, SHA256 `7de5863c9767fd5f143f2cc55f42e1131a19210e08c209c8d2dc9a5f0934cdfe`**. Standing: unselected private296 conditional time projection; pre-S4 root ordering and operational authority pending. Extract rehashed **926/926**. Product-inputs **449/449**. Nested parent 295 pin `b54b5bcf…f042` equals reviewed 295; live 295 trial tar matches. Nested 215 r14 `cd338af6…dd9c` / frozen OWNER `d8165f14…19fa` / model `9aa6e56b…d701` match. Nested 225 r2 `84e48e36…c413` / `TIME-PRODUCER.md` `804134cd…0843` match. Nested 265 `73c3b3f5…86df` live-matches. Product vs 295: **449** files, **447** unchanged. Changed only `trust/ordinary_targets.rs` `56dbaa9c…e195`. Added: `times296.ndjson`. `trust_ordinary_roots.rs` remains `423141df…c212`. `plan()` / `coordinate()` / `plan_from_contexts` / `prepare_scoped` / `prepare_rooted` production text is **byte-identical** to 295. `prepare_times` is a module-private `fn` (not `pub(super)`). Not in `lib.rs`.

---

## What `prepare_times` does

Same Budget: `prepare_rooted` (294 scoped inventory + 295 shared ROOT kernel) first. Then, with **no further object reads**, it stamps `issuedAt` from exactly the signed payload manifest, catalog, and revocation-list payload; `newest` is their maximum and **excludes** the root. It separately stamps the bound final root `issuedAt`, catalog `expiresAt`, and root `expiresAt` through product `timestamp_seconds` (closed 20-byte UTC grammar). It retains the complete `RootedEvidence` plus `[manifest, catalog, list]` issued times, the two S4 scalars (`newest`, `root_issued`), the two expiry inputs, and four presented DocRefs from the captured closure: manifest, catalog, revocation, and `rootChain` **last** (the presented final root, not the same-head historical `projected_accepted_ref`). Calendar failure is `TimesError::Calendar` and latches the operation Budget.

60 TEST-ONLY signed cases, **20/20** positives: six source-time permutations, root newer than the three-source maximum, future manifest admitted as a **candidate only**, and invalid manifest/catalog/list calendars that fail and latch. Baseline 11 objects / 30 edges / 18839 B; repeat 11/60/18839; 11 captures. Inherited 295 ROOT/scope refusals remain full-root refusals, including `same-head-expired`, `final-expired`, and `future-successor`. Oracle: 265/294/295 owners then the frozen 225 r2 producer over authenticated conditional facts. Owned proof/time/source identities are checked after input drop.

**Known wiring limit (not a projection-rule defect):** 295's full root helper still applies `verify_root_chain` evaluation expiry/future (`ExpiredNoChain`, `FinalExpired`, `FinalFuture`) against supplied `evaluation_time`/`wall` **before** this projection. 296 therefore cannot stand in for the complete pre-S4 producer. See `ORDERING.md`.

**Executed:** `cargo clean -p opensip-security` then **243/243** with `Compiling opensip-security` (includes 287–295 tests plus the new times test). Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. 13/13 r1 compiled controls core-equal frozen `mutation-check-r1` (live baseline cargo skipped; unpatched targets SHA matched frozen baseline `56dbaa9c…e195`). Frozen mutant dir not overwritten (`report.json` SHA256 `824511f5…d3b4`).

**Controls (1 wrong conditional calendar acceptance):** `calendar-failure-becomes-zero` (`invalid-calendar/manifest` admitted). **12 other-first:** `newest-is-minimum`; `newest-only-manifest` / `newest-only-catalog` / `newest-only-list`; `root-included-in-three-source-maximum` (`root-is-separate-from-newest`); `root-time-from-catalog`; `catalog-expiry-from-root`; `root-expiry-from-catalog`; `catalog-source-ref-is-list`; `presented-root-ref-is-historical-projection` (same-head alternate DocRef); `source-issued-order-reversed`; `calendar-failure-not-latched` (`bad-first-signature` latch). Not operational exploits.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 296 pins before extract | match |
| Nested 295 / 215 r14 / 225 r2 / 265 live tars | match |
| 295 `prepare_rooted` / 294 `prepare_scoped` bytes | unchanged |
| Live `cargo test -p opensip-security` | **243/243** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 296 r1 mutants | 13/13 frozen-equal; 1 wrong / 12 other |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

Distinct pre-time ROOT authentication (planned 297); S4 write-ahead and tEval root/list validity; current vs BEGIN/history/population qualification; active-batch head barrier; bootstrap; minima/completeness/role-record effects; host admission; durable custody/fence/census/writers; source selection; M3–M6. 296 is a conditional source projection on an already-rooted proof, not complete ordinary import, clock authority, or cumulative approval.

---

## Verdicts

- [x] **296:** archive/pins verified; 295 proof unchanged and runs first; three-source maximum excludes root; presented-root issue and expiry scalars are separate; presented root DocRef is closure last; calendar failures latch; 1/12 mutant classification; 243/243, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** a complete pre-S4 producer, current-head/BEGIN proof, host installation, signed-time authority, completeness, grant, or product installation.
