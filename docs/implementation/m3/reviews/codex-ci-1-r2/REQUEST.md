# Review request: CI-1-r2 (the profile-1 archive codec; law CI r5 item 3), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-ci-1-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane. Do not take the shared lane lock (`$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock`).
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store, the T2 cache or any held-out material.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`;
  - the package's own pure scripts `evidence/check_pkg_ap_pin.py`, `evidence/fixed_vector.py` and `evidence/receipt_inputs.py`. Run them with `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`, and write their outputs only under this review directory.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/ci-1-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 14063 bytes, SHA-256 `7ca9cc207fa1ccf72acb6b4f868d7532b22912c088f452a2955e39d6c77a4771`, 61 members. Rehash every member.
- **Round history:** this is the first round you review. r1 (`component-install/ci-1-r1/`, uncommitted) was packaged but never submitted. C2a-1 was then integrated at `e770404` and appended to security's `lib.rs`, a candidate path. So r2 is a mechanical rebase: main's `lib.rs` plus r1's same five-line append, and every other candidate byte unchanged, with a fresh lane. SCOPE §6 gives r1's attempt history. You may compare `ci-1-r1/product/` with `ci-1-r2/product/` to confirm that the rebase is mechanical.
- **The candidate base:** product main `01769e93db878836612d9e3d483a054f7ad1da94` (inventory v223 bound; 176 contract successors). The lane ran at this base.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-ci1`, detached at that base. It holds the exact bytes that `product-map.json` lists: 4 files, 2 of them new.

## Authority

- **The implementation plan:** `docs/implementation/m3/component-install/PLAN-r3.md` (your `codex-component-install-plan-r3`, ACCEPT, with amendment CI-A1), sub-unit CI-1, LD-CIP-3, LD-CIP-8 and §4-§6 as they apply to CI-1.
- **The law:** `component-install/PROPOSAL-r5.md` (accepted in your `codex-component-install-r5`; CI-A1 changes no CI-1 text). Items 2, 3 and 9, and controls CI-T1, CI-T2, CI-T5 and CI-T13.
- **PKG-AP:** the `archiveProfile` member of `docs/coop/artifacts/component-packaging-contract.v14.json` (SHA-256 `8321d527843c63592d8e4fd49c3df0ace690da0bcbcd1e268464e578fe30424c`), adopted by reference. Its standing is unchanged.
- **The test-feature site list:** `crates/security/src/crash_matrix_sites.rs` (law X9 r1 item 6; law X8 r3 item 4b).
- **The sources the codec relies on:** the admitted manifest shape's entry bound (`crates/security/src/generated/component_manifest_shape.rs`, the tree's `entries`); CM's `tree_checks`, which admits entries in any order (`component_manifest.rs`); and the identity crate's `RawSha256` (`crates/identity/src/streaming_digest.rs`).

## What to review

`SCOPE.md` gives the change table, the interface, ID-CI1-1 to ID-CI1-8, the controls, the census impact, the lane, and §7, a known CI-2 obligation (amendment CI-A2, a lead decision). Judge:
1. **Admission as PKG-AP's `admissionChecks`, as hostile-input parsing** (LAW item 3):
   - every header recomputed from its row and compared octet for octet (ID-CI1-2), including the field reported when only the checksum differs;
   - the member/row bijection in byte order (ID-CI1-1);
   - every body's length and SHA-256, with pads excluded;
   - pad, trailer and EOF exact;
   - no member name used as a path;
   - nothing executed, interpreted or decompressed.
2. **The length and the capacities, before any read:** `archiveLength` with checked arithmetic, `check_length`, and the stream's refusal at byte `L + 1` (CI-T2). Also the four capacity tokens (CI-T5), and the row invariants as host invariants, kept distinct from capacities.
3. **The streaming verifier:**
   - no allocation, and nothing proportional to the archive;
   - correct at every chunk boundary;
   - the consuming step, so that no verifier survives a refusal;
   - the events' contract for CI-2: `FileBytes` unverified until `MemberEnd`, and `End`'s whole-archive digest.
4. **The emitter:**
   - PKG-AP's byte algorithm and its input rules;
   - the exact fixture predicate (LD-CIP-3);
   - its absence from the release build, by code symbols with a positive control (ID-CI1-6);
   - shared gate 6's by-name entry in X9-1's site list (`crash_matrix_sites.rs`; ID-CI1-8). Is that entry the right authority path under law X9 r1 item 6 and law X8 r3 item 4b?
5. **The pin by reference:** `PROFILE_SOURCE_SHA256`, `LAYOUT` and the capacities against PKG-AP (`check_pkg_ap_pin.py`). Also the fixed vector's independence (`fixed_vector.py`, cross-read by `tarfile` and the system `tar`).
6. **The controls:**
   - CI-T1: one test per PKG-AP case, with mode-max and size-max labelled metadata-only;
   - CI-T2, CI-T5 and CI-T13;
   - the structure and extension controls;
   - the 23 mutations, including plan r3 §5's five.
7. **The census impact:** no bound file changed, and CI-PT-4's binding-derived check (`receipt_inputs.py`). The census `--check` modes were not run, because they need the T2 cache (SCOPE §5). Is CI-PT-4 sufficient for "both receipts unchanged" here?
8. **The lane** `evidence/ci1-r2-checks/`: security 1212 → 1240 passing (28 new, exactly the new test file's), with the same 14 base-environment failures on both sides; warning-denied Clippy, the workspace check and both feature checks; the release build, and the emitter's absence from it by code symbols with its positive control; the focused tests; the PKG-AP pin, the independent fixed vector, `bsdtar` and the vector-equals-pin row; rustfmt (with `lib.rs` append-only); the environment exceptions; operability; the census closure and CI-PT-4; verify_design; and all 23 mutations caught. The runner followed main from `e770404` to `01769e9` under the lock (`rebasedBeforeLane`; only `design-lock.json` changed). Also SCOPE §6's r1 attempt history: attempt 2's two real defects (the unlisted fixture sites, and the name-based release check) and their fixes.
9. **Rules:** no new mint-census call, no environment read, no `let _ =`, no new dependency, and `lib.rs` changed append-only.
10. **SCOPE §7, CI-A2:** the lead has decided that CI-2's package will propose amendment CI-A2, pricing the step-2 byte-order index with CI-A1-b's recipe and a byte-order comparator. CI-A2 is not part of this unit. Judge only two things:
    - whether the gap is correctly stated;
    - whether CI-1's interface (`ArchiveRows` by position, with `Rows/Order` refusing any order that is not strictly ascending) lets CI-2 meet it.
11. **Inventory:** two new rows; an inventory successor follows acceptance.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `CI1-R2-RF-n` / `CI1-R2-NBO-n`. Accepting this unit accepts no CI-2 to CI-4 code.
