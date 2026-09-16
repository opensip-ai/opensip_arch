# Independent review: report asset verification algorithm and Unix handle adapter trial

Reviewer: Claude (claude-opus-5), fresh session. No subagents, background tasks, commits or pushes.
Standing: independent review of frozen trial bytes only. The PROPOSED standing of
`report-asset-binding.v1.json` is retained as baseline, and no source was amended. This review
does not accept product integration and makes no release, platform-qualification, D9, M1 or
project-readiness claim.

## Verdict

**Sound for the declared trial scope, with one required test-evidence correction (RQ-1).**
I found no implementation defect in the asset algorithm or the Unix handle walk. More than 100
independent probe vectors pass on unmodified subject code (17 probe functions, including a
73-row shape matrix). They cover raw pins, shape and ordering, streams, identity mixing,
completeness, symlink depth, special files and bounded concurrent swaps. However, the
subject's own tests leave 12 non-equivalent mutants alive, so several rules the code implements
and UNIT.md claims are not substantiated by the subject evidence.

I found no accidental release, platform-qualified, D9, M1 or completeness claim in UNIT.md,
root-validation.json, source-pins.json or code comments.

## Scope and custody

- Subject: `/tmp/opensip-implementation/m1-report-assets-subject-01`, 15 files.
- Manifest: `m1-report-assets-subject-01.json`, SHA-256 `489faf76b3c032173dee87496a7ed3f9f6d0325ce7ff889974f28113d444df01`.
- Before and after all work, the file set was exactly 15 files with no extras or symlinks, and every size and SHA-256 matched. The manifest hash was unchanged.
- All 7 `source-pins.json` inputs matched before and after: the binding JSON, the build plan and 5 identity files.
- The subject `identity/` files are byte-equal to `opensip/crates/identity`.
- `Cargo.lock` pins libc 0.2.189 and sha2-const-stable 0.1.0. Both are in the local registry, and every build used `--locked --offline`.
- All building, probing and mutation ran on copies under this review directory with `TMPDIR=<review>/tmp` and `CARGO_TARGET_DIR=<review>/target/*`.
- Toolchain: `/opt/homebrew/Cellar/rust/1.95.0/bin`. cargo, rustc, rustfmt and mkfifo match the root pins. cargo-clippy, clippy-driver, cargo-fmt and rustdoc were used but are not root-pinned; their hashes are recorded in review.json.

## Reproduced checks

| Check | Result |
|---|---|
| `cargo test --locked --offline` (exact copy) | PASS: 7 unit, 3 filesystem |
| `cargo clippy --all-targets -- -D warnings` (root) | PASS |
| `cargo clippy --manifest-path platform/Cargo.toml --all-targets -- -D warnings` | PASS |
| clippy identity, `cargo fmt --all --check` | PASS (fmt is not recorded in root-validation.json) |
| `cargo test -p opensip-identity` | PASS 10 (not exercised by the stated root command) |
| Dependency graph | Production: reporting → identity → sha2-const-stable only. Platform/libc is dev-only. Reporting forbids `unsafe`. |

## Algorithm against the binding and build plan (§767+)

- **Raw anchor.** Pin paths are canonical and the manifest lies under the root. Manifest bytes must be between 1 and 4 MiB, checked before open. The read is capped at length+1, then length equality, then raw SHA-256, all before parse or any member open. This conforms, with the 4 MiB trial narrowing declared.
- **Closed shape.** The exact identity parser refuses duplicate keys, floats, exponents, `-0` and leading zeros. The root and row objects are closed. `schemaVersion` must be exactly 1. `bytes` must be 0..9007199254740990. Roles are a closed set.
- **Projection list.** The list is nonempty, lowercase 64-hex, and strictly ascending. Byte order of fixed-length lowercase hex equals digest byte order, so this matches the spec's ascending-byte-order rule. Compatibility is membership over the whole list.
- **Paths.**
  - Paths are canonical: no leading slash, empty segment, `.`, `..`, backslash or NUL. Length is at most 4096 code points, matching JSON Schema `maxLength` semantics.
  - Paths lie strictly under the root and are strictly byte-sorted and unique.
  - The scheme rule applies to the first segment. That is sufficient because rows must lie under a canonical root.
- **Self-reference.** A row equal to the pinned manifest path refuses `SelfListed`, and this is checked before order. Completeness adds exactly the bundle's own manifest path. `.bak` files and case variants are not excluded.
- **Members.** Every member is verified, which is stricter than "selected" members. Verification fails fast, and the `Result` carries no partial bundle. Bytes are owned. `VerifiedBundle` keeps the manifest digest, root and path privately, so completeness cannot be run against another pin.
- **Completeness.** Checked against a supplied enumeration only; the enumerator is not implemented, as declared.
- **Not implemented, as declared:** compiled `HostAssetPinV1` with `buildChannel`, compiled projection, D9 mapping, and a real bundle.

## Unix adapter

Starting from a retained, host-supplied directory `File`, the adapter:

- lexically refuses empty segments, `.`, `..`, backslash and NUL;
- opens each segment with `openat(O_RDONLY|O_CLOEXEC|O_NOFOLLOW|O_NONBLOCK)`, adding `O_DIRECTORY` for parents;
- checks the kind of each opened descriptor with fstat;
- returns that same `File`.

Ownership at both `unsafe` sites is correct: the descriptor is wrapped immediately and closed on every error path. Root selection and authentication stay with the host, as declared. A root handle opened through a symlink is accepted.

## Review probes (all PASS on unmodified subject code)

Probe sources are in `probe-src/`, with hashes in review.json.

| Probe | What it established |
|---|---|
| P-VALID | Manifest then asset, each opened once. Whitespace and `\/`/`/` escapes are admitted because the raw pin binds exact bytes. The projection is accepted at the first or last sorted position. |
| P-PIN | These pins refuse with **zero opens**: 10 bad roots (including `c:`, `https:` with a lexically-under manifest, and 4097 characters), 6 bad manifest paths, and bytes of 0, 4 MiB+1 and u64::MAX. Exactly 4 MiB opens, then refuses on length. |
| P-RAW | A same-length, independently valid manifest under the wrong pin refuses `Digest`. Length ±1, an empty stored file and one appended byte refuse `Length`. No member is ever opened. |
| P-SHAPE | 73-row matrix with exact error and exact open list. Covers top-level types, `schemaVersion` 2/0/"1"/01/-1/null/2^64, BOM, trailing data, depth 40, row types, missing/extra/duplicate keys, role variants, `bytes` in string/-1/-0/23.0/2.3e1/023/2^53-1/2^64-1 form, uppercase/63/65/non-hex/space/number digests, unsorted/duplicate/empty/non-array schema lists, incompatibility, JSON-escaped NUL and backslash, 4096 vs 4097 code points (including 2-byte characters), Z<a and z<é byte order, duplicates, and self-listing in either position. |
| P-STREAM | Growing streams at 0/1/7/16384/16385/100000 bytes consume exactly expected+1 while being interrupted. Trickle reads succeed. A flipped digest, a zero-length wrong digest, WouldBlock/Other/UnexpectedEof after partial data, and readers claiming more than the buffer all refuse without panic. MAX_LENGTH+1 refuses without reading. |
| P-MULTI | In a three-member bundle, a corrupt third member refuses after three opens. A missing second member refuses without opening the third. |
| P-MIX | A same-length asset from another bundle refuses. Mutating the asset between the manifest read and the member open refuses `Digest`. Two valid bundles under different roots cannot cross-complete. |
| P-COMPLETE | These refuse `Unlisted`: empty, missing manifest or asset, duplicate manifest, duplicate asset, `MANIFEST.json` alias, unlisted `.hidden`. Outside-root, root itself, trailing slash, dot segment and absolute paths refuse `Path`. |
| P-FS-DEPTH | A real symlink substituted at `share`, `share/report`, a nested subdir, the asset leaf or the manifest leaf refuses the bundle, even though ordinary path lookup still resolves. |
| P-FS-MISC / SPECIAL | Dangling links, loops, a regular file used as a parent, a directory leaf, a directory-symlink leaf and a 300-byte component refuse. A FIFO as leaf or parent refuses within a 5 s watchdog. `/dev/null`, `zero`, `random` and `urandom` refuse. |
| P-FS-HARDLINK | A hardlinked asset is admitted, as declared. A write through an outside alias is caught by the digest, and previously returned bytes are unchanged. |
| P-FS-ROOTSWAP | The retained root still verifies the original bundle after the root is renamed and replaced by a real attacker directory. |
| P-FS-RACE | Over 1.5 s of concurrent rename swaps, the handle walk returned **zero** outside bytes: parent ok/refused 4955/18640, leaf 6263/10347. A naive path read observed outside bytes 5899 and 6598 times, so the race window was live. This is bounded evidence, not proof. |
| P-FS-CASE | TMPDIR is **case-insensitive**. Row `APP.js` and pin `MANIFEST.JSON` verify at load against lowercase files. Exact completeness over the real enumeration refuses. See PI-4. |
| P-FLAGS | FD_CLOEXEC and O_RDONLY are set, and **O_NONBLOCK remains set** (AD-1). |
| P-THROUGHPUT | raw_sha256 on 1/8/32 MiB: debug 34/239/973 ms, release 8/36/79 ms (~400 MiB/s). Allocation capacity equals data length. |

## Mutation assessment (throwaway copies only)

- **Subject tests kill:** raw pre-open bound, asset order/duplicates, self-listing, compatibility, the +1 read cap, the Interrupted retry, length equality, the digest check, empty assets, open object shape, completeness manifest and dedup, role mapping, the length maximum, dot segments, verifying only the first member, O_NOFOLLOW, O_NONBLOCK (FIFO test hangs until timeout), the leaf fstat, the root directory check, and platform dot segments.
- **Subject tests miss (non-equivalent):**
  - M01 scheme rule
  - M02 pin path validation
  - M03 zero-byte pin
  - M05 schema-list order
  - M06 uppercase hex
  - M07 4096 bound
  - M14 over-reporting reader guard
  - M18 empty schema list
  - M19 `schemaVersion` 0
  - M21 completeness path admission
  - M28 compatibility over the whole list
  - P08 O_CLOEXEC
- **Equivalent or overlapping defenses:** M08 (tail length is subsumed by `canonical_path`), P03/P05/P09 (`O_DIRECTORY`, the parent fstat and the next openat's ENOTDIR overlap; `O_NOFOLLOW` still refuses parent symlinks).
- **With reviewer probes:** every non-equivalent mutant is killed.

## Required issue

**RQ-1: The subject tests do not substantiate several implemented and claimed rules.**
The 12 surviving mutants listed above cover rules from the private schemas and from UNIT.md's own adapter description (O_CLOEXEC). UNIT.md's coverage sentence overstates what the seven unit groups show. The lexical group asserts only `is_err`, so a wrong refusal reason would pass.

Remedy: add vectors that kill these mutants and assert the exact `AssetError`, plus an FD_CLOEXEC assertion. The probe matrices here are one sufficient set. Alternatively, narrow the UNIT.md claim. No implementation change is needed.

## Pending final-integration duties (not trial defects)

1. **PI-1, compiled pin.** Replace the public `FixturePin` and `verify_fixture_assets` with the private compiled `HostAssetPinV1` (schemaVersion, sole `buildChannel`, visible development channel). Select it together with the real projection schema digest and the actual offline bundle. No caller path may reach rendering.
2. **PI-2, manifest profile.** The trial uses a 4 MiB/32-container profile, while the private design permits up to 9007199254740990 bytes. Final assembly must prove the actual manifest fits, or select a reviewed private profile.
3. **PI-3, enumerator.** Build a real enumerator that is complete, uses target semantics, never follows symlinks, and **refuses non-regular entries** (symlinks, FIFOs, sockets, devices) under the root. `fixture_completeness` only sees the regular paths it is given.
4. **PI-4, case and normalization aliasing on macOS.** Byte-unique paths and byte-exact self-exclusion do not survive extraction onto case- or normalization-insensitive filesystems. Assembly for the macOS platform rows must refuse colliding rows, including collisions with the manifest path, and check extracted trees. A self-exclusion bypass is infeasible because it would need a self-referential digest, but colliding rows would collapse at install. This is an owner input, not an amendment made here.
5. **PI-5, resource budgets.**
   - A member may declare up to ~9 PB.
   - All bytes are held in memory together, and hashing runs after the full read.
   - `try_reserve` does not prevent overcommit OOM kills.
   - Owners still need per-member and aggregate caps and memory budgets. Measured throughput is in P-THROUGHPUT.
6. **PI-6, projection binding.** `VerifiedBundle` does not retain the projection it was checked against, or the pinned length. Make the projection a compile-time constant or bind it into the verified type.
7. **PI-7, subset selection.** A renderer subset needs explicit checked selection and must never ignore a missing selected asset.
8. **PI-8, D9 mapping.** Apply it only for asset-consuming renderers: `DELIVERY.REQUIRED_FAILED` with exit 4 before commit; the after-commit detail with a retained RunId after commit; optional surfaces leave the aggregate unchanged; no format downgrade.
9. **PI-9, host AssetSource.** The host implements `AssetSource` over platform handles with no production reporting→platform edge. Record the trial's dev-only edge under enforcement item 1.
10. **PI-10, Linux.** Build and qualify the adapter on Linux, and qualify races beyond these bounded probes.
11. **PI-11, content offline checks.** Scanning asset bytes for network references belongs to the built-browser offline checks; the trial checks paths only.
12. **PI-12, install-time provenance.** Include the manifest and members in the TR-CORE signed inventory (B14/B12).

## Advisories

- **AD-1:** `O_NONBLOCK` stays set on the returned file. It is harmless for regular files; clear it or document it.
- **AD-2:** A device leaf is opened before fstat refuses it, so a driver's open routine can run. This is inside the trusted-install boundary (B10). An optional `fstatat(AT_SYMLINK_NOFOLLOW)` pre-check or Linux `O_PATH` would add defense in depth.
- **AD-3:** Error granularity is coarse (all lexical errors are `Shape`; missing, extra and duplicate paths are all `Unlisted`). Adequate for the trial.
- **AD-4:** The stated root command does not run identity tests. The fmt result is not recorded. The clippy, fmt and rustdoc binaries are not pinned.
- **AD-5:** The overlapping parent checks (M08, P03, P05, P09) are defense in depth, not defects.
- **AD-6:** Build emission should write one canonical byte form so pins are reproducible.

## Security and bounds scope

- **Established:**
  - Pin-before-parse and pin-before-member ordering.
  - Reads capped at expected+1, with allocation driven by actual data and no partial results.
  - Owned bytes that later source changes cannot alter.
  - A per-segment no-follow handle walk that refuses special files without blocking and survives root and leaf substitution under the probes.
- **Not established:**
  - Authenticity of the host or root selection (TCB, B1/B10).
  - Defense against a hostile same-process `AssetSource`; the trait is a trusted-host boundary, not a sandbox.
  - Hardlink, mount and case/normalization policy.
  - Linux behavior, exhaustive race freedom and memory budgets.
  - D9 integration, a real bundle, and the release inventory.
