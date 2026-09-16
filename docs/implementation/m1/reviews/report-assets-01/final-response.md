The algorithm and the Unix adapter are sound for what the trial says it covers, but one required fix remains: the subject's own tests don't prove several rules the code implements. I found no code defects. The review is in `review.json` and `review.md` in the review directory.

**Custody.** Before and after all work, the manifest SHA-256 was still `489faf76…df01` and all 15 files matched exactly, with no extras. All 7 source pins matched, and the 5 identity files are byte-identical to `opensip/crates/identity`. `Cargo.lock` pins libc 0.2.189 and sha2-const-stable 0.1.0, and every build ran `--locked --offline`. cargo, rustc, rustfmt and mkfifo match the recorded tool pins. I built only on copies, with my own `TMPDIR` and `CARGO_TARGET_DIR`, and wrote only inside the review directory.

**Reproduced checks.** On an exact copy:
- `cargo test`: 7 unit and 3 filesystem tests pass.
- Clippy with `-D warnings` passes for the root and platform crates (and for identity), and `cargo fmt --check` passes.
- The only production dependencies are identity and sha2-const-stable; the platform crate is a test-only dependency.

**Probes (17 functions, all pass on unmodified code):**
- **Pin checks:** bad pins are refused before anything is opened, and length then digest are checked before parsing or opening any member. Pin variants covered: bad root, bad manifest path, 0 bytes, 4 MiB+1, and a same-length valid manifest under the wrong pin.
- **Manifest shape:** a 73-row matrix of malformed shape, numbers, digests, roles, paths, ordering, duplicates and self-listing, each checked for the exact error and exact files opened.
- **Byte reads:** growing, interrupted, failing and over-reporting streams (including zero-length) read at most expected+1 bytes and never return partial results.
- **Identity mixing:** changing a member between the manifest read and the member open is caught.
- **Completeness:** 12 refusal cases plus success in either order, including the `.bak` and case-variant manifest names.
- **Real filesystem:**
  - Symlinks at every depth, FIFOs (no blocking), `/dev` devices, and swapping out the retained root are all refused.
  - Hardlinks are allowed, as the trial states.
  - In 1.5 s of concurrent symlink swaps, the handle walk never returned outside bytes. Plain path reads saw them about 6,000 times, so the race was really happening. This is bounded evidence, not proof.

**Mutation testing.** On throwaway copies, 12 meaningful mutants survive the subject's tests: the pin path checks and scheme rule, the zero-byte pin, schema-list order, lowercase-only hex, the 4096-character limit, the guard against readers reporting too many bytes, the non-empty schema list, `schemaVersion` = 1, path checks in completeness, whole-list compatibility, and `O_CLOEXEC`. My probes kill all of them. The only survivors left are equivalent or overlapping defenses.

**Required issue (RQ-1).** Add test vectors that kill those mutants and assert the exact error, plus an `FD_CLOEXEC` check. Otherwise, narrow the coverage sentence in `UNIT.md`. No code change is needed.

**Pending integration duties.** The 12 PI items in the review are not trial defects. The ones that matter most:
- **Compiled pin:** replace `FixturePin` with the private compiled pin and its build channel and projection, and resolve the 4 MiB manifest limit.
- **Real enumerator:** completeness needs an enumerator that also refuses non-regular files.
- **macOS case aliasing:** the temp filesystem here is case-insensitive. A row `APP.js` and a pinned `MANIFEST.JSON` both load against lowercase files. Release assembly for macOS must refuse paths that collide under case folding or Unicode normalization.
- **Memory limits:** set per-member and total size caps. Hashing measures about 400 MiB/s in release builds.
- **Projection binding:** the verified bundle doesn't record which projection it was checked against.
- **Remaining integration:** D9 failure mapping and Linux qualification.

Advisories include that `O_NONBLOCK` stays set on the returned file, and that a device file is opened before it is refused.

No release, platform, D9, M1 or completeness claim is made, and I found none by accident in the subject.
