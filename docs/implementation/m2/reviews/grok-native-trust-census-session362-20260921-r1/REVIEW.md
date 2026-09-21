# Independent review — native current/census session 362

**Standing:** bounded native-**security** review of frozen `native-trust-census-session-checkpoint-362`. Extends 361 so the **same** `Budget`, native fence, every original current `Head`, and every retained 345 `SuppliedCensus` are rechecked together. Copied `ProvisionalSuccessorCounts` are **structural diagnostics only** (no CLEAN/BEHIND/FORK, no current authority). Product remains `fa72e50`. Prior 361 REVIEW `36b24bbd…4e81` (7748 B), 360 `1990e91f…4921`, store-binding 358 `REVIEW.md` `cf1903f4…17ff` and `ADDENDUM.md` `84da081d…9a8b` were read and are **unchanged**. Separate `SOURCE-NOTE.md` covers the S9 standing question and is **not** this code verdict. **363** host bundle is WIP and is **not** this freeze.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dir **not** overwritten. **This review reproduced:** `native_read_session::` **13**, rustdoc **4** `compile_fail`, Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **31** security includes, **14** compiled controls + 13-test baseline. Full security **388** **not rerun**. Frozen author: native-session-r1 **12** then 13th late-malformed-branch test; security-r1 **388**/0/2 plus 4 doctests. No 362 source/test failure history.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 361 archive **570 / 6892608 B / `dda64d61…9f83`** / 507 product pins rehashed before 362 extract. Independent rehash of 362 tar, 594 members, and extract: 0 mismatches.

Frozen archive: **7029028 B, 594 members, SHA256 `b4a45c7582e8d878d2f25cd4130e684d8d1c0eea2f8bd626f16b6124433cfea8`**. 507 product pins.

Product vs 361: **504** unchanged, **3** changed, **0** added:

| Path | SHA256 / bytes |
|---|---|
| `crates/security/src/lib.rs` | `d3d809ad…eb82` / 20318 |
| `crates/security/src/trust.rs` | `a3f5e283…de00` / 623629 |
| `crates/security/src/trust/native_read_session.rs` | `1fe4d4f5…b874` / 35020 (was `32a7fd6b…ddfa` / 17693) |

`Cargo.lock` identical. `native_census.rs`, `native_current.rs`, and `directory_provers.rs` **byte-identical** to 361 (no 344/345 algorithm edit). 126 fixtures unchanged. Public reexport adds `ProvisionalSuccessorCounts` only.

---

## Shared budget / census / errors

`observe_successors` delegates to existing 345 `native_census::capture` on `fence.native_guard().as_supplied()` with store from **first independently parsed C**. Same `Budget.scope`. Before the attempt, after a new census (before push), and after **failed** census, `check_all` rechecks fence, I/carrier `same_filesystem`, **all** original Heads, and **all** already-retained censuses. New census is not pushed on failure (`censuses` stays empty; no counts returned). Foreign names are charged by 345 before the callback; callback `Err` plus fence mutation still postchecks and latches `Closed`.

`latest_successor_counts`: `None` means no census requested. `publication_root_observed_missing` vs `immediate_bucket_observed_missing: Some(true|false)` distinguishes root-absent / bucket-missing / observed-empty. Counts of candidates/following/supported are copied structural fields only.

Live counters matched the freeze law: initial current `(4, 7, 4207)`; missing bucket `(10, 38, 9105)`; empty `(11, 41, 9108)`; repeat empty `(11, 75, 9111)`. Edge bound 40 refuses where 41 succeeds. 0/1/2 structurally supported following branches. Later current/dependency/bucket changes fail **all** consumers. Late malformed following branch returns no counts and closes the session.

No File/root/guard/Budget/reset escape. Two existing + two session compile_fail doctests still apply.

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `native_read_session::` | **13 passed** |
| `--doc` | **4 compile_fail passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **31** includes | exit 0 |
| Full 388 | **not rerun** |

---

## Mutants

Fourteen compiled controls + 13-test baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 **not** overwritten). Live `report.json` SHA256 **`d52c9c19ae177410eaf43c2147a32e796a265327a11c0a5c358860207435f1b6`**, **byte-identical** to frozen **r1**. All **15** compiled.

| Control | First failure |
|---|---|
| `skip-request-prevalidation` | Null request not `Current(Reference)` before IO |
| `skip-postcheck-on-capture-error` | failed current capture skips original-fence postcheck |
| `skip-recheck-latch` | repaired path revives session |
| `skip-raw-consumption-recheck` | `raw_current` after source change |
| `drop-previous-original-heads` | Heads not cumulative |
| `reset-budget-for-every-repeat` | exhausted budget reset on `observe_again` |
| `skip-original-head-rechecks` | original current replace/delete/ancestor accepted |
| `skip-independent-current-store-comparison` | mismatched G/K vs independent `C.store` |
| `skip-all-retained-census-rechecks` | later current/dependency/bucket change not closing consumers |
| `reset-budget-before-census` | edge-40 census succeeds after reset |
| `drop-prior-census-objects` | second empty census does not retain prior objects |
| `skip-failed-census-postcheck` | failed foreign callback skips prior-fence postcheck |
| `truncate-structurally-supported-count` | supported count capped at 1 |
| `skip-later-following-branches` | later following links not walked (345 `directory_provers` temporary patch only) |
| baseline | 13 `native_read_session::` |

---

## Findings

362 is the requested **shared-budget current+census session**: 345 census under 361 fence/Budget/all original Heads; failed census still rechecks and latches; counts are structural; `None` is “not requested.” It does **not** close CLEAN/BEHIND/FORK, profile, or current authority.

**Actionable defects in this freeze:** none that make shared Budget, retained census objects, failed-census postcheck, missing-vs-empty, later-following ownership, or latch-on-malformed-branch self-contradictory with the 13 tests, 4 doctests, and 14 compiled controls.

**Coverage, not a freeze contradiction:** `fixture_at` remains SYNTHETIC/`cfg(test)`. Sequential samples are not ABA. Three-member `C.store` comparison remains the 358 ADDENDUM’s provisional check (see `SOURCE-NOTE.md` for S9.3 standing; native five-member handle/registry still unimplemented).

**Must not be counted closed:** `StoreGenerationBindingV1`; namespace/handle/registry; core/profile; CLEAN/BEHIND/FORK; current authority; writers; **363** host bundle; M2–M6; OS-home provenance.

---

## Remaining (do not count closed)

363 if later requested is a **separate** host bundle, not this report. Five-member binding via admitted handle/registry. 323/229, 350 profile FS-name law on these Files, active-slot, writers.

---

## Verdicts

- [x] **362 as frozen private shared-budget current/census session:** archive verified against parent 361; three security-only deltas; 345 census unchanged; same Budget/fence/all Heads/all censuses; live 13+4 doctests; Clippy/fmt31; 14 compiled controls frozen-r1-equal. Native-session-r1 12-test image is history before the 13th late-branch test. Matches the census-session request, not current authority or 363.
- [ ] **Not** `StoreGenerationBindingV1`, selected-I/current authority, CLEAN/BEHIND/FORK, 363 host bundle, writers, or product installation.
