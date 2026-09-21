# Independent review — native trust read session 361

**Standing:** bounded native-**security** review of frozen `native-trust-read-session-checkpoint-361`. `NativeTrustReadSession` borrows one opaque `InstallationReadFence`, owns one cumulative trust `Budget` (65536 objects / 131072 edges / 256 MiB) and **every original** 344 current `Head`, and compares a fully validated 127 `StoreBinding` request to independently parsed `C.store`. This is **provisional** current observation, **not** current authority, `StoreGenerationBindingV1`, namespace/handle/registry, core/profile, census, or writers. Product remains `fa72e50`. Prior 360 REVIEW `1990e91f…4921` (5574 B, no ADDENDUM), 359 `ebe45147…9baf`, store-binding ADDENDUM `84da081d…9a8b` were read and are **unchanged**. **362** census extension is WIP and is **not** this freeze or this approval. Separate source-standing work is queued and does not block this provisional-only review.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dir **not** overwritten. **This review reproduced:** `native_read_session::` **7**, rustdoc **4** `compile_fail` (2 existing ProvisionalHeldFile E0505/E0515 + 2 new session fence drop/escape), Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **31** security includes, **8** compiled controls + seven-test baseline. Full security **382** **not rerun**. Frozen author record: native-session-r3 **7**; security-r1 **382**/0/2 plus 4 doctests.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 360 archive **545 / 6891316 B / `145e511c…bb28`** / 506 product pins rehashed before 361 extract. Independent rehash of 361 tar, 570 members, and extract: 0 mismatches.

Frozen archive: **6892608 B, 570 members, SHA256 `dda64d61d50314b2062e288b0b9b6828f750afa54ec26ce2f4eea3eec43d9f83`**. 507 product pins.

Product vs 360: **502** unchanged, **4** changed, **1** added (security only):

| Path | SHA256 / bytes |
|---|---|
| `crates/security/src/lib.rs` | `857022ce…c1fd` / 20290 |
| `crates/security/src/trust.rs` | `c15f1a93…28ad` / 623558 |
| `crates/security/src/installation_observation.rs` | `c696ef49…d451` / 34147 |
| `crates/security/src/trust/native_current.rs` | `aebf456c…6825` / 25188 |
| `crates/security/src/trust/native_read_session.rs` **added** | `32a7fd6b…ddfa` / 17693 |

`Cargo.lock` byte-identical to 360. 126 security fixtures unchanged. `store_id` is `pub(super)` only; `native_guard` / `same_filesystem` are `pub(crate)`; `fixture_at` is `cfg(test)` `pub(crate)`. Public crate root reexports `NativeTrustReadSession` / `NativeTrustReadError` on macOS. No host/storage/lifecycle source delta. No census/immutable/profile join in this file.

---

## Session / budget / latch / comparison

`capture` validates the complete request with existing `store_id` (three members + `Definition::StoreBinding` admit) **before** `capture_head` IO. 344 `capture_head` still compares independently decoded `C.store` to that expected triple (`native_current.rs` equality). `check_all` runs fence + I/carrier `same_filesystem` (355 predicate: local/nonunion/nondegenerate, device+fsid+name+type+subtype) and every retained Head prefix-pair and File sample against actual I, **before and after** even a failed capture. New Head is pushed only on success; old Heads are never cleared or replaced by a reopen.

`observe_again` rechecks, then recaptures using `store_claim()` from **first C**, under the **same** Budget. `recheck` / failed `scope` latch `Budget::Closed`; repairing the path does not revive the session. `raw_current` / `store_claim` recheck first; store claim is from captured C, not request JSON. `counters` are diagnostics. No public File/root/guard/Budget/reset.

---

## Failure history (must not be hidden)

| Run | Result | Notes |
|---|---|---|
| native-session-r1 | **did not compile** | `Budget::scope` Result inference; fixture `JsonInteger` constructors |
| native-session-r2 | **5** focused | before prevalidation-before-IO + failed-capture postcheck tests |
| native-session-r3 | **7** focused | freeze image |
| security-r1 | **382**/0/2 + **4** doctests | this review did not rerun 382 |

Templates precede `author-final.patch`; product bytes are authoritative. r1 compile failure is **not** a test pass or control kill.

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `native_read_session::` | **7 passed** |
| `--doc` | **4 compile_fail passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **31** includes | exit 0 |
| Full 382 | **not rerun** |

---

## Mutants

Eight compiled controls + seven-test baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 **not** overwritten). Live `report.json` SHA256 **`6e5ad8e6ba4f3aa0f9992403c1499e7c88d7cdeb9d5e61c8024d5ab16e0051bc`**, **byte-identical** to frozen **r1**. All **9** compiled.

| Control | First failure |
|---|---|
| `skip-request-prevalidation` | Null request is not `Current(Reference)` before IO (fence 666 would win) |
| `skip-postcheck-on-capture-error` | failed capture skips original-fence postcheck |
| `skip-recheck-latch` | repaired path revives session (`Closed` not latched) |
| `skip-raw-consumption-recheck` | `raw_current` returns bytes after source change |
| `drop-previous-original-heads` | `heads.len()` not cumulative |
| `reset-budget-for-every-repeat` | exhausted edge budget reset on `observe_again` |
| `skip-original-head-rechecks` | replace/delete/ancestor of original current accepted |
| `skip-independent-current-store-comparison` | mismatched G/K request accepted vs independent `C.store` |
| baseline | 7 `native_read_session::` |

---

## Findings

361 is the requested **provisional native-current session**: one fence, one Budget, all original Heads, StoreBinding prevalidation, independent C.store comparison, FS identity via the 355 predicate, latch-on-failure, no File/Budget escape. Later census/profile **must** reuse this Budget and these Files; that join is **not** in this freeze (362 is separate WIP).

**Actionable defects in this freeze:** none that make prevalidation-before-IO, failed-capture postcheck, Closed latch, retained original Heads, cumulative Budget, or independent `C.store` comparison self-contradictory with the 7 tests, 4 doctests, and 8 compiled controls.

**Coverage, not a freeze contradiction:** `fixture_at` remains SYNTHETIC/`cfg(test)` account-home. Sequential samples are not ABA/hostile-kernel. Three-member request vs `C.store` remains the 358 ADDENDUM’s **provisional comparison**, not `StoreGenerationBindingV1`.

**Must not be counted closed:** five-member `StoreGenerationBindingV1`; namespace/handle/registry; 344 as authority; core/profile allowlist; successor census / 362; active-slot; current authority; writers; M2–M6; OS-home provenance.

---

## Remaining (do not count closed)

362 if later requested is a **separate** census extension, not this report. Independent security current vs five-member binding (ADDENDUM). 323/229, 350 profile FS-name law on these Heads, active-slot, writers.

---

## Verdicts

- [x] **361 as frozen private provisional native-current session:** archive verified against parent 360; five security-only deltas; one fence + one Budget + all original Heads; StoreBinding before IO; independent `C.store`; latch Closed; live 7+4 doctests; Clippy/fmt31; 8 compiled controls frozen-r1-equal. r1 compile failure and r2 five-test image are history. Matches the session request, not current authority or 362.
- [ ] **Not** `StoreGenerationBindingV1`, selected-I/current authority, 362 census, writers, or product installation.
