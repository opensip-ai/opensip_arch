Trial02 is conditionally accepted at unit scope. This is not product approval. Review01's required issue is resolved and I found no concrete defects in the delta. `review.json` and `review.md` are in `/tmp/opensip-implementation/m1-report-assets-review-02`.

**Pins.**
- **Manifest and files:** the manifest hash is still `c20b5e35…5d76dd`, and all 18 files matched in set, size and SHA-256 before and after.
- **Test origins:** `test-origins.json` correctly pins my review01 originals.
- **Other pins:** source pins, identity exports, `Cargo.lock` and all 8 tool pins match.
- **Isolation:** builds ran on an exact copy with their own `TMPDIR` and `CARGO_TARGET_DIR`, and I wrote only in the new review directory.
- **What changed:**
  - 3 files changed (`UNIT.md`, `root-validation.json`, `src/lib.rs`) and 3 are new (`asset_tests.rs`, `file_flags.rs`, `test-origins.json`).
  - The platform source is unchanged.
  - The adopted tests match the originals apart from formatting, the removed performance probe, one new projection assertion, and a new check in the flags test that `fcntl` succeeded. No assertion was removed.

**Commands.** All ran `--locked --offline`:
- Root tests: 15 unit and 3 filesystem tests pass, none ignored.
- Platform tests: the flags test passes, none ignored.
- Clippy with `-D warnings` passes for root and platform, and `cargo fmt --check` passes.

These match the root's reported counts.

**The twelve prior survivors.** I re-ran them against the final tests rather than assuming the adoption covered them:
- All 12 are now caught. P08 (`O_CLOEXEC`) is caught only by the platform test command, so that command has to stay in the routine.
- With only the adopted test files removed, all 12 survive again, so the adopted tests are what catch them.
- My first mutation runs gave misleading results: copying preserved old file timestamps, so cargo reused stale builds. I set those results aside, fixed the copy step, and re-ran everything. This is recorded in the review.

**Independent probes (all pass):**
- **Projection:** with a manifest listing A, B and C, verifying with each returns exactly that projection. Unlisted values are refused before any member is opened, and verifying the same source under two projections gives separate bundles.
- **Unchanged behavior:** verified bytes stay owned and don't change when the source changes. The trusted `AssetSource` boundary is unchanged, and no failure exposes a partial bundle.
- **API privacy (8 compile checks):** outside code can't construct a bundle, read or write the projection field, change asset bytes, or clone a bundle.
- **Filesystem:** review01's 7 filesystem probes, which weren't adopted, still pass on the unchanged adapter.

**Advisories (non-blocking):**
- **Projection test gap:** a mutant that stores the first or last listed schema instead of the checked projection survives the permanent tests. The code is correct; one assertion on the middle entry of a multi-schema manifest would close the gap.
- **`UNIT.md`:** some superseded historical sentences remain.
- **Flags test cleanup:** the flags test leaves its PID-named temp directory behind when it fails.
- **Adapter behavior:** `O_NONBLOCK` stays set on returned files and device files can be opened before being refused. This is already acknowledged in `UNIT.md`.

**Explicitly pending:**
- The real asset inventory, the compiled pin and build channel, and joining the projection to the compiled schema.
- A real build enumeration.
- A portable policy for path aliases that differ only by case or Unicode normalization.
- Manifest and whole-bundle sizing.
- D9 delivery mapping.
- Platform, Linux and release integration.

No performance probe was adopted or run, and no runtime or release qualification is claimed.
