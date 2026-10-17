# CI-1 r1: the profile-1 archive codec (law CI r5 item 3)

**Unreviewed candidate, 2026-10-17. It needs Codex review.** It implements sub-unit CI-1 of the component installation implementation plan r3 (`../PLAN-r3.md`, accepted by Codex `codex-component-install-plan-r3` with amendment CI-A1). The law is "component release installation and tree custody" (`../PROPOSAL.md`: r5 under its acceptance note, with CI-A1; r5's bytes are `../PROPOSAL-r5.md`). CI-A1 changes no CI-1 text.

**Product base:** main at the lane's start, as `source.json` and `checks.json` record it. **Worktree:** `/Users/sb/code/opensip-ai/opensip-ci1`, detached at that base. **Changed:** four files, two of them new (`product-map.json`).

## 1. What changes

| File | Change |
| --- | --- |
| `crates/security/src/archive_profile.rs` (new) | The codec: the plan, the streaming verifier, the header recomputation, and the fixture-only emitter. |
| `crates/security/src/archive_profile_tests.rs` (new) | CI-1's controls: PKG-AP's 15 cases (CI-T1), CI-T2, CI-T5 and CI-T13, plus the structure, stream and extension controls. |
| `crates/security/src/crash_matrix_sites.rs` | X9-1's pinned list of test-feature sites gains **shared gate 6**, by name: `archive_profile.rs`, joint predicate, 2 sites (`emit` and `EmitRefusal`), with its module-doc entry (ID-CI1-8). |
| `crates/security/src/lib.rs` | Appends `pub mod archive_profile;` with its comment. The file is base-dirty for rustfmt, so the change is append-only, and the lane checks that the candidate begins with the base's exact bytes. |

There is no new dependency. The codec uses the identity crate's `RawSha256` and `raw_sha256`, as LAW item 3 says ("the product's own code and the identity crate's SHA-256").

## 2. The interface

- **`TreeRow { path, mode, kind: RowKind::{File { length, sha256 }, Dir, Symlink { target } } }`**: one TreeCommitment row, borrowed. `mode` is the integer value of the row's octal mode string, and `sha256` is the raw digest.
- **`trait ArchiveRows { count(), row(position) }`**: the tree's rows **in member order**. It is implemented for `[TreeRow]`. CI-2 implements it over the borrowed manifest and its order index, so the codec copies no row.
- **`ArchivePlan::new(&rows)`** checks every row and computes PKG-AP's `archiveLength` with checked arithmetic. It refuses with:
  - `Capacity { position, capacity }` for PKG-AP's four capacity tokens. These are LAW's `archive-capacity`, before any read (CI-T5);
  - `Rows { position, invariant }` for a property the admitted manifest already guarantees: 1 to 100,000 rows, strictly ascending byte order, and non-empty, NUL-free text. Seeing one is the caller's bug.
- **`plan.length()`, `plan.read_limit()`** (the length plus one) and **`plan.check_length(observed)`**. The last judges the archive's sampled size before any byte is read (CI-T2).
- **`plan.verifier()`** returns an **`ArchiveVerifier`**. Its `step(self, &mut input) -> Result<(Self, Option<ArchiveEvent>), ArchiveRefusal>` consumes bytes from the front of the caller's input. Its events are:
  - `Header { position }`: the header equals the row's;
  - `FileBytes { position, bytes }`: a slice of the caller's own buffer, unverified until the member ends;
  - `MemberEnd { position }`: for a file, its length, SHA-256 and pad are verified;
  - `End { sha256 }`: the trailer is exact, and `sha256` is the whole archive's raw SHA-256, for CI-2 to compare with `archiveDigest`.

  `finish(self)` at the input's end refuses `Truncated` unless the trailer completed. Bytes after the trailer refuse `TrailingBytes`, at the first such byte, so a reader needs at most `read_limit()` bytes.
- **`emit(entries, payloads)`**, under exactly `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))` (plan LD-CIP-3), is PKG-AP's byte algorithm:
  - step 1 sorts the entries by code point;
  - every file must have exactly its payload, with the row's length and SHA-256 (`SIZE-OR-DIGEST-MISMATCH`);
  - a payload keyed by a dir or symlink row, by no row, or twice refuses.
- **The pin by reference.** `PROFILE_ID`, `PROFILE_SOURCE` and `PROFILE_SOURCE_SHA256` name PKG at its pinned SHA-256. `LAYOUT` is PKG-AP's `headerLayout.fields` table. The lane's `check_pkg_ap_pin.py` compares the following with PKG's own JSON:
  - the hash, the profile id and the layout;
  - the capacities and the capacity tokens;
  - the typeflag bytes and the length formula;
  - the CI-T1 test names against `goldenAndNegativeCases`.

## 3. Implementation decisions

- **ID-CI1-1. Rows arrive in member order, and the order is checked, not trusted.** PKG-AP orders members by the code points of the NFC path, which is UTF-8 byte order. TreeCommitment entries carry no order: CM admits them in any order. So member `i` is the `i`-th row in byte order. The plan refuses `Rows/Order` unless every row is strictly after the previous one. A caller that supplied a wrong order would otherwise admit a non-canonical archive. The codec does not sort: it charges nothing, and allocates nothing. **The order index is CI-2's** (see section 7).
- **ID-CI1-2. Headers are compared octet for octet against the recomputed header.** The expected 512 bytes are built from the row in the verifier's fixed state, and each incoming byte is compared at its offset, across any chunk boundary. No input is buffered and no field is decoded.

  The refusal names the first differing field other than `chksum`, or `chksum` when only the checksum differs. That is why a re-checksummed typeflag `0x00`, or a re-checksummed nonzero uid, refuses at `typeflag` or `uid`, not at `chksum`.
- **ID-CI1-3. A refused step consumes the verifier.** As with `RawSha256`, a refusal leaves no verifier that could continue or finish a prefix.
- **ID-CI1-4. Pads and the trailer are checked byte for byte,** and the file digest excludes the pad (PKG-AP `bijection.fileBody`). The whole-archive digest covers every byte, the trailer included.
- **ID-CI1-5. The length is judged twice.** First, `check_length` compares it with the observed size before any read. Then the stream refuses at the first byte past the trailer.
- **ID-CI1-6. The emitter is absent from release.** The lane reads code symbols, not names, because rustc's metadata records the names of cfg-stripped items too (attempt 2 below):
  - `release-emitter-absent`: the release rlib defines the codec's `archive_profile::field_at` and no `archive_profile::emit`;
  - `fixture-emitter-present`: the positive control. A debug build with `scenario-fixtures` defines both.
- **ID-CI1-8. The fixture site is pinned by name.** X9-1's source pin (`crash_matrix_sites.rs`, law X9 r1 item 6; law X8 r3 item 4b: "one site list, one joint predicate, extended by name") fails on any unlisted test-feature site. Plan r3 LD-CIP-3 places CI-1's emitter under exactly the joint predicate. So the list gains shared gate 6, `archive_profile.rs` with 2 sites, as X3d r8 item 13 added gate 5. That file is test-only, and it is in neither receipt's bound set (`receipt_inputs.py`).
- **ID-CI1-7. The entry-count bound** is 1 to 100,000 rows, from the admitted manifest shape (`component_manifest_shape.rs`, the tree's `entries`: `!a.is_empty() && a.len() <= 100000`), as LAW's capacity table cites it. No new constant is introduced. Each other constant is PKG-AP's, checked by the pin.

## 4. Controls

- **CI-T1:** one test per PKG-AP case, named after it, `at_archive_identity` to `at_archive_noncanon_uid`. The lane checks that the 15 names are exactly PKG-AP's list.
  - `at_archive_mode_max` and `at_archive_size_max` are labelled metadata-only. They are codec-capacity cases (PKG-AP permits a synthetic, metadata-only fixture), never installable signed positives.
  - `at_archive_fixed_vector` pins an archive length and SHA-256 computed by `evidence/fixed_vector.py`. That is a second encoder, written from PKG-AP's text alone. Python's `tarfile` and the system `tar` cross-read its output, and the lane checks that the script's values equal the test's pins.
- **CI-T2:** a length mismatch refuses at `check_length`, before any member event. A longer stream refuses at byte `L + 1`, and every truncation refuses at the input's end.
- **CI-T5:** a 101-byte path or target refuses `Capacity` at the plan. Without a plan no verifier exists, so nothing is read.
- **CI-T13:** a source pin. The codec's source names no network, process, spawn, environment, filesystem, `unsafe` or `let _ =` API.
- **Further controls:**
  - the event sequence is identical at ten chunk sizes from 1 to 65,536;
  - NUL pads and trailer are required;
  - PAX and GNU typeflags, a PAX extended-header member, GNU magic and a prefix-split name all refuse;
  - octets after a field's terminator, and numeric alternatives that a decoder would accept, refuse;
  - the row invariants;
  - the length formula;
  - the emitter's payload refusals;
  - the layout's contiguity;
  - the emitter's fixture predicate, as a source pin.
- **Mutations (23):** each must fail the focused tests. They include plan r3 §5's five for CI-1:
  - a header compared by decoded fields;
  - typeflag `0x00` accepted;
  - the length checked after reading;
  - a PAX or GNU extension accepted;
  - a pad byte unchecked.

  The other 18:
  - a noncanonical uid accepted;
  - the checksum unchecked, or computed under a NUL mask;
  - the trailer unchecked, trailing bytes accepted, or a truncation accepted;
  - the file digest unchecked;
  - each capacity off by one;
  - the row order trusted;
  - the length formula without its trailer, or with a wrong pad;
  - the trailer left out of the archive digest;
  - the emitter padded to a blocking factor, left unsorted, or not checking digests.

## 5. Census and receipts

CI-1 changes no census-bound file (plan LD-CIP-8: "unchanged" for both receipts). The lane checks this two ways:
- **`census-closure-unchanged`:** the discovery `CLOSURE` check used by earlier lanes.
- **`receipt-inputs-unchanged` (CI-PT-4, `evidence/receipt_inputs.py`):** the script loads both census tools' own binding code and derives each receipt's bound file set from it:
  - **discovery** (`receipt_bindings`): its tool, `CLOSURE`, the member model and the reference-loading product sources;
  - **companion** (`bindings`): those, its four tools and `snapshotSources` (the model's snapshot files and anchors, the session files and anchors, the work ledger and `ANCHORED`).

  It then asserts that the changed-file set misses both sets, and that the four committed receipt files are byte-equal to base.

**No census mode is run.** The `--check` modes need the T2 cache, which this unit may not read. Plan §6's "both census `--check`s" is therefore met by CI-PT-4's binding check, which the plan names as the freshness-relevant evidence. Byte-equal receipts are recorded, not claimed as freshness.

## 6. The lane

`evidence/ci1-r1-checks/` (`run_ci1_checks.py`), one lane hold, nice 10, private 0700 TMPDIR. Main moves while lanes queue, so once the runner holds the lock, it moves the worktree to main's head. It does so only when main descends from the worktree's base and changed no candidate path; `checks.json` records it as `rebasedBeforeLane`.

**Attempt history** (the earlier attempts are not packaged; they are kept at `/tmp/opensip-implementation/ci1-r1-checks-attempt{1,2}`):
1. **Attempt 1** stopped at its first assertion: main had moved while it waited for the lock. Hence the move-to-main step above.
2. **Attempt 2**, at main `caa71e2`, found two real defects, and was stopped before its mutations:
   - security's `crash_matrix_sites::every_test_feature_site_is_on_the_pinned_list` failed on the candidate only, three runs of three in isolation: the emitter's two sites were unlisted. Fixed by ID-CI1-8;
   - `release-emitter-absent` failed because it searched for item names, which rustc's metadata keeps for cfg-stripped items. Replaced by ID-CI1-6's symbol check and its positive control.

   Its other steps passed: clippy, the workspace check, both feature checks, the release build, the focused tests, the PKG-AP pin, the fixed vector and `bsdtar`, the environment exceptions, operability, and both census checks.
3. **Attempt 3**, at main `caa71e2`, passed every row, with all 23 mutations caught. Main then moved to `813d559` (C1c-0), which appended to security's `lib.rs`, a candidate path. So the candidate was rebased: main's `lib.rs` plus this unit's same five-line append. The lane was then re-run, so that the packaged lane covers the exact reviewed bytes. Attempt 3 is kept at `/tmp/opensip-implementation/ci1-r1-checks-attempt3`.
4. **Attempt 4** is the packaged lane, at main `813d559`. **Every row passed** (`checks.json`, `allPassed: true`):
   - **Security's suite:** 1198 passing at base and 1226 on the candidate, so 28 new tests, exactly the new test file's. The same 14 failures on both sides: base failures from the shared environment (`commit_authority::seal_binding_tests` and `custody::operation_handoff::tests::session`), none of them CI-1's. Equal suite counts.
   - **Static checks:** warning-denied all-targets Clippy, the workspace all-targets check, and the `scenario-fixtures` and `crash-matrix` checks.
   - **Release and fixture builds:** the release build; `release-emitter-absent` and its positive control `fixture-emitter-present`.
   - **Focused tests:** the focused CI-1 tests (`archive_profile::`).
   - **Pins and the fixed vector:** `pkg-ap-pin` (12 checks); `fixed-vector-independent` and `fixed-vector-bsdtar`; and `fixed-vector-equals-pin`.
   - **Repository checks:**
     - rustfmt on the edited base-clean files, with `lib.rs` base-dirty and checked append-only;
     - the environment exceptions;
     - operability's source census with its mint audit (no findings);
     - `census-closure-unchanged`;
     - `receipt-inputs-unchanged` (23 discovery-bound and 37 companion-bound files, none changed; the four receipt files byte-equal to base);
     - verify_design.
   - **Mutations:** all 23 caught.

## 7. For the lead: a CI-2 pricing gap (not CI-1's)

LAW's `B_install` step 2 streams the archive's members in PKG-AP's member order, which is byte order of the full path. The TreeCommitment's entries are unordered, so CI-2 must map member `i` to its row: it needs a byte-order index over the `n` rows. **No `B_install` row prices that index.**
- CI-A1-b prices only step 4's index, which is in **component** order, a different order: `a-x` precedes `a/b` in byte order, but follows it in component order.
- The recommended correction for CI-2's plan or law is the same recipe at step 2: two `u32` buffers (objects 2, bytes `2·n·size_of::<u32>()`, checked), and at most `n·⌈log₂ n⌉` charged comparisons, with a byte-order comparator.
- Alternatively, one index could serve both steps, if step 4's walk were derived from byte order. It cannot be done simply, because byte order does not keep each directory's descendants contiguous.

CI-1 is unaffected: its `ArchiveRows` takes whichever order index CI-2 builds, and refuses one that is not byte-ordered.

## 8. Not delivered

- Work charging: the codec is pure. CI-2 prices its reads and owns the ledger.
- The mapping of refusals to LAW item 8's rows: CI-2 and CI-4.
- The trust bridge (C2a-1's), the store, the installer and the retained tree (CI-2 and CI-3).
- C2a-2's archive emission through `emit`.
