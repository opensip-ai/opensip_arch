# Review02: narrow delta review of report asset trial02

Reviewer: Claude (claude-opus-5), fresh session. No subagents, background tasks, commits, pushes or private session inspection.

## Verdict

**Conditionally accepted at unit scope.** This is not product approval.

- **Review01 RQ-1 is resolved.** All twelve previously surviving mutants are now detected by the final permanent root and platform tests. With only the adopted test files removed, all twelve survive again, so the detection comes from the adoption.
- **The new `projection_sha256` is correct.** It is private and immutable, and it holds exactly the projection that passed the membership check.
- **Nothing else changed in behavior.** The trusted `AssetSource` boundary and the private owned bytes behave as before.
- **No concrete defect was found.** There are no required issues.

Every pending integration item below stays open.

## Pins and custody

- **Subject:** `/tmp/opensip-implementation/m1-report-assets-subject-02`.
- **Manifest:** `m1-report-assets-subject-02.json`, SHA-256 `c20b5e35e4e91f4e55c31353790ea8a1b120ff191fb1eba59b64dbaf5f5d76dd`.
- **Exact 18 files:** set, sizes and SHA-256 all matched before and after, with no extras or symlinks.
- **Delta versus subject-01** (whose manifest `489faf76…df01` is unchanged):
  - Changed: `UNIT.md`, `root-validation.json`, `src/lib.rs`.
  - New: `src/asset_tests.rs`, `platform/tests/file_flags.rs`, `test-origins.json`.
  - The other 12 files are byte-identical, including `platform/src/lib.rs`, `src/tests.rs` and `tests/filesystem.rs`.
- **Source pins:** all 7 `source-pins.json` inputs matched before and after.
- **Test origins:** both `test-origins.json` inputs match their pins (`review_probes.rs` 28e96350…, 22238 bytes; `review_flags.rs` ee4d7ccb…, 1138 bytes).
- **Identity:** the 5 identity files are byte-equal to `opensip/crates/identity`.
- **Cargo.lock:** unchanged.
- **Tool pins:** all 8 `root-validation.json` tool pins match hash and size.
- **Isolation:** builds ran on an exact copy of the declared closure inside this review directory, with its own `TMPDIR` and `CARGO_TARGET_DIR`. Nothing outside this directory was written.

## Delta verification

- **`src/lib.rs`.** Three additions only:
  - a private `projection_sha256: [u8; 32]` field;
  - a `projection_sha256(&self) -> &[u8; 32]` accessor;
  - `projection_sha256: *projection` at the single success site, which is reached only after the compatibility membership check.

  Plus the `mod asset_tests` declaration. The public API gains exactly that accessor. The algorithm, `AssetSource`, `FixturePin` and completeness are unchanged.
- **`src/asset_tests.rs` versus review01 `review_probes.rs`.** All eight non-performance groups are present. The only changes are:
  - rustfmt reflow;
  - a let-chain and `is_multiple_of`;
  - a new module comment;
  - removal of the ignored throughput probe;
  - one added projection assertion.

  No vector or assertion was removed, which matches `test-origins.json`.
- **`platform/tests/file_flags.rs`.** It now uses strict `create_dir` and asserts that `fcntl` succeeded. That closes a vacuity gap: an `F_GETFD` return of -1 would previously have satisfied the `FD_CLOEXEC` bit check.
- **`UNIT.md` / `root-validation.json`.** The appended trial02 paragraph and the root counts are accurate and reproduced (see AD-2 for retained historical sentences).

## Commands and results

Toolchain: `/opt/homebrew/Cellar/rust/1.95.0/bin`.

| Command | Result |
|---|---|
| `cargo test --locked --offline` | PASS: 15 unit, 3 filesystem, 0 ignored |
| `cargo test --locked --offline --manifest-path platform/Cargo.toml` | PASS: 1 (`file_flags`), 0 ignored |
| `cargo clippy --locked --offline --all-targets -- -D warnings` | PASS |
| `cargo clippy --locked --offline --manifest-path platform/Cargo.toml --all-targets -- -D warnings` | PASS |
| `cargo fmt --all --check` | PASS |
| `cargo test --locked --offline -p opensip-identity` | PASS 10 (informational) |
| `cargo tree -e normal,build` | reporting → identity → sha2-const-stable; platform remains dev-only |

The root observation of 15 root unit + 3 root FS + 1 platform group, with no ignored groups, is reproduced exactly.

## Independent tests (review copy only)

- **D-PROJ (`delta_projection_is_exactly_the_checked_member`): PASS.**
  - The manifest lists [A,B,C]. Verifying with A, B or C returns exactly that projection, not the first or last listed.
  - Unlisted values refuse `Incompatible` after opening only the manifest, with no bundle: D, zeros, 0xff.., the manifest digest, the asset digest.
  - The same source and pin verified under A and then C give separate bundles with the same bytes and distinct projections.
  - Completeness is unaffected.
- **D-OWNED (`delta_owned_bytes_and_trusted_source_behaviour_unchanged`): PASS.**
  - After success, replacing and dropping the source leaves the bundle's bytes, their heap address, path and projection unchanged.
  - An aliasing source that serves identical bytes under another backing name is accepted. This is the declared trusted-source boundary, not a sandbox.
  - The alias with its target missing refuses `Io`.
  - Same-length different bytes refuse `Digest`.
  - A reader failing after 5 bytes refuses `Io`.
  - A missing manifest refuses `Io` with only the manifest opened.
  - No failure exposes a partial bundle or a projection.
- **CF-PRIVACY: 8/8.** From an external test crate:
  - The control (reading `*b.projection_sha256()`) compiles.
  - Constructing `VerifiedBundle` or `VerifiedAsset` fails with E0451.
  - Reading the private field fails with E0616.
  - Assigning through `projection_sha256()` or `manifest_sha256()`, or mutating asset bytes, fails with E0594.
  - `clone()` fails with E0308, because the bundle is not `Clone`.
- **R01-FS: 7/7 re-run, not adopted.** Review01's filesystem probes still pass on the unchanged adapter:
  - symlinks at every depth;
  - FIFOs and `/dev` entries;
  - hardlink write-through;
  - case aliasing (TMPDIR is case-insensitive);
  - retained-root substitution;
  - bounded concurrent swaps, with zero outside bytes returned while naive path reads saw them thousands of times.

## Mutation assessment

Method: fresh-mtime throwaway copies. Each mutant runs `cargo test --locked --offline --no-fail-fast` for the root package, then for `--manifest-path platform/Cargo.toml`. A control run passed first in each mode.

| Prior survivor | Final permanent tests | Without adopted tests |
|---|---|---|
| M01 no scheme check | killed: `asset_tests::probe_pin_admission…` | survives |
| M02 no pin path validation | killed: `probe_pin_admission…` | survives |
| M03 zero-byte pin | killed: `probe_pin_admission…` | survives |
| M05 schema list checks dupes only | killed: shape/order matrix | survives |
| M06 uppercase hex | killed: shape/order matrix | survives |
| M07 no 4096 bound | killed: shape/order matrix | survives |
| M14 no lying-reader guard | killed: stream probe | survives |
| M18 empty schema list | killed: shape/order matrix | survives |
| M19 schemaVersion ≤ 1 | killed: shape/order matrix | survives |
| M21 completeness path check | killed: completeness matrix + identity mix | survives |
| M28 compatibility on last schema only | killed: valid control | survives |
| P08 no O_CLOEXEC | killed: platform `file_flags` (the root suite passes, so the platform command is needed) | survives |

New projection mutants:

| Mutant | Final tests | With review02 probes |
|---|---|---|
| N01 projection zero | killed | killed |
| N02 projection = manifest digest | killed | killed |
| N03 first listed schema retained | **survives** | killed |
| N04 last listed schema retained | **survives** | killed |

**Invalidated runs.** My first review02 runs copied the tree with its old mtimes, so cargo reused stale builds. The symptoms were a platform failure on lib-only mutants and a root failure on the platform-only P08. Those results are quarantined as `mutation-*-stale-mtime-invalid.json` and not relied on. After correcting the driver, all modes were re-run on fresh target dirs. Review01's driver shared this weakness, but its recorded outcomes are corroborated by the `original` and `final` runs above.

## Advisories (non-blocking)

- **AD-1:** The permanent projection test doesn't pin *which* listed digest is kept, so N03 and N04 survive. The code is correct. Add a middle-element assertion for a multi-schema manifest, as in D-PROJ, before the compiled-schema join relies on the field.
- **AD-2:** `UNIT.md` still contains superseded historical sentences: "Seven unit groups…", "review is pending", and a run line without the platform command. Mark them historical when next edited.
- **AD-3:** `file_flags.rs` names its temp dir by PID, creates it strictly, and cleans it up only on success. Induced failures left directories behind here, and a recycled PID in the same TMPDIR would fail spuriously. Use a drop guard or a unique suffix.
- **AD-4:** Review01's filesystem probes were not adopted, which RQ-1 did not require. They still pass, and the case-alias observation feeds the pending alias policy.
- **AD-5:** Unchanged and already acknowledged: O_NONBLOCK stays set on returned regular files, and a device leaf's open routine can run before fstat refuses it. Both stay within the trusted installation root.
- **AD-6:** Completeness is independent of the projection. That is correct for this owner, and the renderer must still join the projection to the compiled selection.

## Explicitly pending (not implied by this acceptance)

- Actual asset inventory and offline bundle; the private compiled `HostAssetPinV1` and sole `buildChannel`; joining `projection_sha256` to the compiled selected projection.
- Real build enumeration that is complete, never follows symlinks, and refuses non-regular entries.
- A portable path alias collision policy covering case folding and Unicode normalization.
- Manifest profile fit, whole-bundle and per-member sizing, and memory budgets.
- D9 delivery mapping.
- Platform/host `AssetSource` integration with no production reporting→platform edge, Linux qualification, release assembly, and TR-CORE inventory inclusion.

## Scope

Unit-level delta review on macOS arm64 over fixture pins. No performance probe was adopted or run. No runtime, browser, platform, Linux, race-exhaustive, release, D9, M1 or product qualification is claimed. The PROPOSED standing of the binding design is retained, and no source was amended.
