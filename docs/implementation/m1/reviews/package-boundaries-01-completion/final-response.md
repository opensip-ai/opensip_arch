**Verdict: changes required, not accepted.** The subject manifest SHA256 is `6706c27f…df06a60`. All three file hashes were the same before and after the review, and none of the 33 read-only input hashes changed.

**Required finding (RF-1):** UNIT.md says stale Cargo metadata cannot hide an added internal dependency. That isn't true. The raw-manifest recheck at `tools/check_package_edges.py:40` reads only the hyphenated dependency tables. Cargo 1.95 still honors `[dev_dependencies]` and `[build_dependencies]`, including under `[target.*]`, for edition 2015 and 2021 manifests. The tool doesn't require edition 2024. I added a forbidden `opensip-contracts -> opensip-host` edge that way after capturing metadata, using real Cargo fixtures, and the check passed in all three forms I tried. Fresh metadata does refuse them.
- **Fix:** either also read the underscore spellings, or refuse non-2024 editions and underscore keys.
- **Tested:** I tried the one-line version on my own copy (`probes/reviewer-fix-underscore.diff`). All 12 tests still pass and all three bypasses are refused.
- **Tests to add:** stale-metadata cases for this form and for `build-dependencies`.

**Advisories:**
1. **Declarations only:** the stale-metadata guarantee covers dependency declarations only. A stale `[lib] path` escape and a stale addition of the provider to the host workspace both pass. Fresh metadata catches both, so the UNIT.md wording should be narrowed.
2. **Weak test coverage:** 13 of my 27 mutations survive the 12 tests. The most important one silently drops `build-dependencies` from the stale-metadata recheck.
3. **Safe but confusing refusals:** an allowed `cfg( windows )` edge and an allowed edition-2021 `[build_dependencies]` edge are both refused.
4. **CLI metadata capture:** it only reproduces offline with `--filter-platform aarch64-apple-darwin`, because `r-efi` isn't cached. The exact capture command should be recorded.
5. **Shared-package comparison:** the "14 shared packages equal" result holds only under that same platform filter.
6. **Hard-coded values:** the provider name and root are hard-coded, and the inventory kind isn't checked against Cargo targets.

**What I confirmed independently:**
- **Tests:** all 12 pass on my copy.
- **Real Cargo probes:** 36 cases built on the actual v3 inventory. 31 behaved as expected; the other 5 are RF-1 and advisories 1 and 3.
- **CLI trial:** fresh metadata produces tool output byte-identical to `cli-boundary-check.json`.
- **Provider isolation trial:**
  - Its edge output reproduces byte-for-byte.
  - The export holds only contracts, identity and the provider. There is no root Cargo manifest, host app, Node or generator files, and the files match the repository.
  - All 13 source pins match.
  - The provider has its own lock and the root lock is unchanged.
  - The 14 shared packages have the same versions and features.
  - The contracts dependency closure is exactly 11 registry packages.
  - My copy of the export built offline with `--locked` and the probe ran.

The trial binary is only a throwaway build probe. This review doesn't cover rustc/provider integration, release readiness, native purity, macros or external features.

The first run's background mutation job was cut off. I reran all 27 mutations in the foreground in the completion directory, and reused first-run probe results only after my rerun of the probes reproduced them exactly. No commits, pushes, inventory changes or installs.

Files are in `/tmp/opensip-implementation/m1-package-boundaries-review-01-completion`:
- review.json
- review.md
- probes/ (scripts and results)
