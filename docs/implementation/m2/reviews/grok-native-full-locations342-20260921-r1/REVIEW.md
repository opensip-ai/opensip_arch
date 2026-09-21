# Independent review — full-reference native capture 342

**Standing:** bounded native-**security** review of frozen `native-full-locations-checkpoint-342`. Private `capture` locates immutable bytes from a **complete typed 127 reference** under a **borrowed** 341 `SuppliedInstallationFence`. Routes are explicit: Objects `trust/objects/H`, Records `trust/records/H`, Events `trust/stores/S/events/seq-H`, Publications `by-predecessor/P/H` or `initial/S/H` with schema-valid initial S. **No** path inference, hash search, collection alias, or fallback. `Captured` **borrows** the fence for its lifetime and owns prefix handles, original `File`, and raw `Arc`. This is **not** semantic JSON admission, selected I/actor, FS qualification, current authority, 5s scheduler, or writers. Original structural callbacks still take only collection/digest/cap and **cannot** yet use these locators. Installed product remains `fa72e50`. 341 and 340 REVIEW were read and are **unchanged**.

Python 3.12.13 `-I -B` for pin/extract. Rust 1.95.0 `--offline --locked`. Frozen mutant dirs not overwritten. Author Python syntax failure pre-extraction preserved. Test strengthening r1/r2/r3: **no production fix**. mutation-r1 baseline **FAILED 311/1/2** (`installation_fence_busy_path_still_checks_changed_root` `Root(Descriptor(ChangedDuringRead))` on **initial** acquire, before deliberate chmod) — **not a kill**; all 14 r1 mutants still compiled and caught. **Final is security-r3 / 312 / mutation-r2** with `RUST_TEST_THREADS=1`. Serial harness is **test concurrency**, not profile qualification or host-change impossibility. No new `unsafe`/dependency.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6849716 B, 619 members, SHA256 `5b1ccb9b2a724ad43d49e41a996f8bb996f74d4a6ee8b6655e006ef10c92a755`**. Extract 619/619. Parent 341 live tar SHA `24117a22…2a69` (6832908 / 544 / 489). 341 REVIEW `0731e5b1…beb9` and 340 REVIEW `5db5d5dd…bffa` unchanged.

Product vs 341: **486** unchanged, **3** changed (`trust.rs` include; `directory_record_capture.rs` `pub(super)` `Phase`/`check_name`/`read_one`; `installation_fence.rs` `supplied_actor()`), **1** added (`native_record_capture.rs` SHA256 `9806b39b…0b4e` 25618 B). libc `=0.2.189`.

---

## Routes, bound, File, budget, cache, fence

**Locator (before IO):** exact member set per collection; SHA 64-hex; Events store 32-hex + integer sequence; Publications previous 64-hex or Null; initial StoreId only when Publications+Null; 127 `admit` of the full reference (and StoreId). Extra 1 MiB `"path"` field is `Reference`/`Shape` with counters `(0,0,0)`. Invalid sequence 0 / store `"g"*32` / `../escape` refuse pre-IO.

**Capture under borrowed fence:** `check_prefix` (fence recheck + all prefix 333/339 policy + fence) → for each parent: **edge charge**, bind, prefix recheck even on failed open, 333 inspect, `Budget::directory` (inode identity **after** open — disclosed, not retroactive descriptor preallocation) → file **edge** → `capture(..., presence=true)` so cache **never** skips native `read_one` with `cap.min(declared length)` on original File → exact `raw.len() == declared` → construct `Captured` → `recheck`. Repeat capture shares raw `Arc` (`ptr_eq`) but still opens a File; delete path then fail. `presence=false` mutant fails **second** legitimate cache hit because `retained` File is missing (`Error::Reference`) — **owned-File availability**, not a demo of unsafe missing-file acceptance.

**Accounting:** Objects/Records `(3,5,3)`; Events/Publications `(5,9,3)` for `abc`. One-short object/edge/byte refuse. Declared length 2 → 335 Bound; 4 → `Length`; content `bad` → digest fail.

**Post-read:** prefix relocate, leaf-parent relocate, file rewrite, root chmod, **lock-carrier swap** all refuse and latch. Symlink / case / parent-case refuse. Cross-collection / wrong sequence / wrong store / wrong predecessor despite cached bytes refuse.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-security`, `RUST_TEST_THREADS=1`:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **312 passed / 0 failed / 2 ignored**; 110.23s; 7 `native_locations_*` ok; no `ChangedDuringRead` |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **25** included modules | exit 0 |

---

## Mutants

**r1 (historical):** baseline FAILED 311/1/2 as above; 14 compiled controls caught. Evidence retained; **not** a kill.

**r2 (final, `RUST_TEST_THREADS=1`):** 14 compiled controls + full-security baseline replayed into `grok-out/io/mutation-check-live` (frozen r1/r2 **not** overwritten). Live `report.json` SHA256 **`4fc7f84e…a008`**, **byte-identical** to frozen r2. All **15** compiled.

| Control | First failure (class) |
|---|---|
| `objects-use-records` | Objects unwrap fail |
| `event-wrong-sequence` | Events unwrap fail |
| `publication-wrong-predecessor` | Publications unwrap fail |
| `skip-full-reference-shape` | extra-field/shape pre-IO not refused |
| `skip-initial-store-shape` | invalid initial S not refused |
| `skip-directory-budget` | `(1,3,3)` vs `(3,5,3)` |
| `skip-parent-lookup-budget` | `(3,3,3)` vs `(3,5,3)` |
| `cache-without-fresh-file` | second capture no owned File |
| `skip-exact-length` | declared 4 accepted |
| `ignore-declared-read-bound` | declared 2 not Bound |
| `skip-final-recheck` | prefix relocate `Ok` |
| `only-first-prefix-policy` | leaf-parent relocate `Ok` |
| `skip-fence-rechecks` | carrier swap `Ok` |
| `skip-original-file-stability` | file rewrite `Ok` |
| baseline | 312 / 2 ignored |

---

## Findings

342 is a **full-locator** native reader under a borrowed 341 fence, with shape-before-IO, exact routes, original-File lifetime, and `presence=true`. It does not migrate structural callbacks, select I, or close 337 profile/fence-through-consumption.

**Actionable defects in this freeze:** none that make `Locator`/`capture`/`Captured` self-contradictory with those bounds on the macOS 312 tests (serial) and 14 r2 controls.

**Must not be counted closed:** callback migration; selected I/actor; FS profile; 5s scheduler; writers; semantic admission; current authority; Linux; M2–M6.

---

## Remaining (do not count closed)

Migrate collection/digest/cap callbacks to carry **full reference + initial S**; fence-through-consumption; 337 planted-name/profile; Event/Publication locator completeness for existing consumers; M2–M6.

---

## Verdicts

- [x] **342 as frozen private full-reference native capture:** archive verified; 341/340 preserved; five exact routes; 127 shape pre-IO; borrowed 341 fence; original File + `presence=true`; live 312/2 ignored (`RUST_TEST_THREADS=1`); Clippy/fmt25; r1 baseline fail **not** a kill; r2 14 controls + baseline frozen-equal.
- [ ] **Not** semantic admission, selected-I authority, callback migration, census, or product installation.
