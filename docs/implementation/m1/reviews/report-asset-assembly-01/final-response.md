This is a resumed independent review, in the same session as the report asset reviews 01 and 02, not a fresh session. The assembly enumerator has one required fix, and it is to the tests, not the code; the coverage correction is ready for root to accept on its own. The verdicts are in separate files in `/tmp/opensip-implementation/m1-report-asset-assembly-review-01`.

**Custody.** Both frozen manifests matched their hashes and exact file sets (29 and 6 files) before and after all work. All declared pins matched:
- assembly: 14 source pins, 8 tool pins, and subject-02's manifest (`c20b5e35…`), which is unchanged;
- coverage: 40 input pins, the v2 parent pin, and subject-05's manifest.

I ran everything on copies inside the review directory, with Python `-I -B` and an empty private pycache prefix (it stayed empty), and one Cargo build at a time per target.

## Primary: asset assembly subject01 (`review.json` / `review.md`)

**Verdict: acceptable at trial scope on one condition, RQ-A1 (tests only).** I found no implementation defect. This is not product approval, and the earlier verifier02 acceptance doesn't carry over to this integration.

**Root checks reproduced.**
- The 9 Python tests pass.
- Re-running `build_fixture.py` on the copy produces a manifest, pin and digest byte-identical to the frozen ones.
- The consumer passes `cargo test`, Clippy and fmt.
- The embedded verifier is byte-identical to accepted subject-02, but it no longer carries subject-02's filesystem tests.

**Independent probes (7 Python groups plus Rust interop, all pass):**
- **Inventory:** every directory entry is visited and the role map is exact. Undeclared files, missing files, hidden names, uppercase or Unicode names, symlinks, FIFOs and sockets are all refused.
- **Manifest handling:** only a regular file at exactly the pinned path is skipped, and it is never read, even at 4 MiB+1. Case variants and near-name aliases are refused.
- **Caps:** the projection, role and channel checks happen before any filesystem call. The member cap is checked from `fstat` before reading. The aggregate cap is only checked after hashing, so up to one extra member gets read.
- **Replacement races:** same-length writes, appends and truncates are all caught. Symlink or non-directory swaps during the race escape as a bare `OSError`, which still fails closed. Files added to an already-visited directory and writes after hashing are not caught, as the unit already declares. A concurrent symlink-swap stress run never emitted outside bytes.
- **Custody:** open flags are verified, the tree is never written, and no descriptors leak.
- **Owner schemas:** nested and deep outputs validate against both private schemas.
- **Interop:** the unchanged verifier accepted 19 bundle/projection pairs, including the middle of three and all of 16. The emitted manifests are byte-for-byte canonical under the identity crate.

**RQ-A1.** Of 36 single-edit mutants, 18 meaningful ones survive the 9 permanent tests; my probes catch all of them except T12. The uncaught guards:
- **T18:** row sorting by bytes. The flat test trees can't tell sorted order from traversal order; without the sort, legitimate trees are falsely refused.
- **T04–T08:** replacement detection and the `O_NOFOLLOW`/`O_NONBLOCK` open flags.
- **T13–T15, T20, T26:** the directory, listing, projection, role and segment caps.
- **T19:** empty role maps, which the owner schema forbids.
- **T02/T03:** the checks that stop work before the caps are exceeded.
- **T12, T16, T17, T30:** file size equality, build channel, root-is-directory, and role path under root.

The fix is to add tests (my probes are one reproducible set) or narrow the claims in `UNIT.md`.

**Advisories (non-blocking):**
- Map race-time `OSError` to a typed refusal.
- Pre-check the aggregate cap using `fstat` sizes.
- Change detection is timestamp-based and not a snapshot, and the runtime doesn't check completeness at load, so publication must bind the tree.
- The 4096-byte path limit and the depth check are redundant with the segment caps.
- Windows reserved names like `con` are accepted.
- The subject's socket test fails when TMPDIR is long.
- `jsonschema` isn't byte-pinned.

**Still pending:** D9, the compiled-pin-only route and sole build channel, the actual bundle and its sizing, binding the renderer schema to `projection_sha256`, bootstrap and tool closure, immutable publication and the TR-CORE inventory, and platform/Linux qualification.

## Secondary: coverage prerequisite subject01 (`coverage-review.json` / `coverage-review.md`)

**Verdict: ready for root to accept as a narrow bookkeeping fix.** No issues or defects. It does not select report05.

- **Reproduced:** `check.py` exits 0 and its output equals `root-result.json` exactly.
- **Exact delta:** my own recursive diff finds one added key. The v3 bytes are exactly v2's two-space-indented JSON with that key appended (+44 bytes), and the historical fields are unchanged.
- **Why M1:** the validator accepts only M0 or M1; M2–M6 fail on the `version` row and a missing or malformed value fails. M1 matches the only delivery row that owns `assets.rs` (`commands/version`), follows the convention used by 40 of 41 modules, and is the same value report05's own temporary workaround adds. M0 only passes ordering.
- **Overlay:** I composed report05 with its own hash-verified `apply_overlay` and no workaround. All 323 rows are valid, composing over the uncorrected v2 still fails, and command metadata drift is still detected. `check.py` rejects all five negative controls: value M0, key removed, standing edit, row milestone edit, and a bad pin digest.

**Provenance note:** 24 of the 37 pinned architecture files are untracked in git and 8 have local modifications. The inputs are bound by hash, not by commit, so acceptance should cite the manifest and pin hashes.
