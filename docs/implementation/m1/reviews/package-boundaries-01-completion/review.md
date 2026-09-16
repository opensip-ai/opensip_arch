# Package boundaries review — subject 01

**Verdict: changes-required** (not accepted)

Subject manifest SHA256 `6706c27f63b828753df15b679e27628ead3b7902a16de6136b7fe81e7df06a60`. All 3 file hashes matched before and after. 33 read-only input hash entries (subject, manifest, candidate, export, trial JSONs, root lock, inventory) are unchanged.

## Required finding

**RF-1 — Stale metadata can still hide an added internal edge.** `tools/check_package_edges.py:40` rechecks only `dependencies`, `build-dependencies` and `dev-dependencies`. Cargo 1.95 still honors `[dev_dependencies]`/`[build_dependencies]`, including under `[target.*]`, for editions 2015 and 2021. The tool does not require edition 2024. With metadata captured before the edit, these real Cargo fixtures all **pass**:
- a forbidden `opensip-contracts -> opensip-host` edge in edition 2021 `[dev_dependencies]`
- the same edge with no edition key
- the same edge in edition 2021 `[target.'cfg(windows)'.build_dependencies]`

That contradicts UNIT.md's stale-metadata claim. Fresh metadata does refuse them.

Fix: read the underscore spellings (see `probes/reviewer-fix-underscore.diff`; with it all 12 subject tests pass and all three become `forbidden manifest internal edge`), or refuse non-2024 editions and underscore keys. Also add stale regression tests for this form and for `build-dependencies`.

## Advisories
1. **Stale guarantee is declaration-only.** A stale `[lib] path` escape and a stale host-workspace addition of `providers/rust` both pass; fresh metadata refuses both. Narrow the UNIT.md wording.
2. **Mutation coverage.** 13 of 27 mutants survive the 12 tests. The most important survivor is "manifest ignores build-dependencies". Others: optional-flag comparison on either side, workspace_root check, duplicate owner, manifest pathless and owner-path checks, manifest name, local missing from resolve, inventory path escape, empty workspace, default members.
3. **Fail-closed false refusals.** An allowed `cfg( windows )` edge and an allowed edition-2021 `[build_dependencies]` edge both refuse with "declarations differ".
4. **CLI metadata capture command.** It needs `--filter-platform aarch64-apple-darwin` to reproduce offline, because `r-efi` isn't cached. Record the exact command.
5. **14-shared equality is platform-filtered.** It holds for aarch64-apple-darwin; an unfiltered check was not possible offline.
6. **Hard-coded values.** The provider name/root are hard-coded and inventory kind isn't checked against targets. Later new tool paths still need additive inventory review.

## Independent evidence
- **Subject tests:** 12/12 pass on the reviewer copy.
- **Real-Cargo probes:** 36 cases rebound to actual v3 inventory rows (`probes/probe_real_cargo.py`, `probe-results.json`). 31 behaved as expected; the 5 unexpected ones are RF-1 and advisories 1 and 3. Covered:
  - allowed normal, alias, optional-feature, cfg/triple target, build, dev and provider-lane edges
  - forbidden edges in every form, including an alias spoof and provider↔host in both directions
  - a non-inventory crate, workspace crossing, lib/build/symlink target escape, workspace inheritance, wrong lane, wrong root
  - stale additions
- **Mutations:** 27 mutants, 14 killed by the subject tests (`probes/mutation-results.json`, complete foreground run).
- **Root CLI trial:** fresh filtered metadata equals the stored file except the target/build directory. The tool output is byte-identical to `cli-boundary-check.json`. It refuses under the wrong lane and the wrong root.
- **Provider isolation trial:**
  - `package-edges.json` reproduced byte-for-byte.
  - The export has 17 files: only contracts, identity and providers/rust. There is no root Cargo.toml, apps, Node, generator, `.cargo` config or `build.rs`, and the files equal the repository dirs.
  - All 13 source pins match in the repository and the export.
  - A copy of the export built with `--locked --offline` in reviewer scratch, the probe passed, and the copy was unchanged afterwards.
  - The provider has its own 15-package lock and the root lock is unchanged.
  - 14 shared packages have equal versions and features.
  - The contracts closure is exactly the 11 registry packages.

## Limits
- No rustc/provider integration, release, product install, M1 completion, purity, macro/`#[path]`/`include!` or external-feature qualification; the trial binary is a disposable probe.
- Metadata isn't attested.
- The mutation set is reviewer-chosen.
- The review-01 background mutation run was interrupted. The mutation evidence here is a complete rerun; the review-01 probe outputs were reused only after the baseline rerun matched them exactly.
- No commit, push, inventory amendment or install.
