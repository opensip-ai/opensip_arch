# Report asset assembly subject01: resumed independent review

This is a **resumed** independent review in the same Claude session as report-assets review01 and review02. It is not a fresh session. No subagents, background tasks, commits, pushes or private session inspection were used. Root acceptance is separate.

The coverage prerequisite has its own verdict in `coverage-review.md`.

## Verdict

**Conditionally acceptable at trial scope, with one required test-adequacy correction (RQ-A1).**

- **No concrete implementation defect found.** Every enumerator behavior UNIT.md describes held under independent probes on real files.
- **Verifier interop works.** The byte-identical accepted verifier02 accepts the emitted manifests for nested, 16-segment and 16-projection bundles under every projection.
- **The permanent tests fall short.** The subject's 9 Python tests leave 18 non-equivalent mutants alive, so many claimed guards are unsubstantiated by permanent evidence.

This does not approve the product. It also does not carry verifier02's unit acceptance over to this integration.

## Custody and pins

- **Subject:** `/tmp/opensip-implementation/m1-report-asset-assembly-subject-01`, manifest SHA-256 `c72765728a14b14b56b6b51bf55e7ee5186156076ed33d2d519e8abc8cc5f454`, exactly 29 files. Set, sizes and hashes matched before and after.
- **source-pins.json:** all 14 entries match both the copy and the source. The verifier's 13 files are byte-identical to accepted subject-02 (manifest `c20b5e35…`, unchanged). The binding input is byte-equal to the architecture file.
  - Not carried: subject-02's `tests/filesystem.rs` and metadata files.
- **Tool pins:** all 8 root tool pins match (Python 3.14.6 `b502cb4c…`, and the Rust 1.95.0 tools).
- **Isolation:** all execution ran on copies inside this review directory, with a private TMPDIR, separate Cargo targets (one build per target) and `python -I -B -X pycache_prefix=<empty>`. The prefix held 0 entries throughout. `build_fixture.py` wrote only to the mutable copy.

## Reproduced root checks

| Check | Result |
|---|---|
| Python tests (`-I -B`) | PASS 9 |
| `build_fixture.py` on copy | PASS; owner schemas valid; the regenerated `manifest.json`, `pin.json` and `manifest-digest.rs` are byte-identical to frozen |
| consumer `cargo test --locked --offline` | PASS 1 (three projections, including the middle) |
| consumer clippy `-D warnings`, `fmt --check` | PASS |
| verifier / platform tests (informational) | PASS 15 / 1 |

## Assessment

- **Complete inventory.** The walk is a descriptor walk from the caller's root fd:
  - every entry gets `lstat(nofollow)`, then an `openat` segment open with `O_RDONLY|O_CLOEXEC|O_NOFOLLOW|O_NONBLOCK` (`|O_DIRECTORY` for directories), then an fstat `(dev, ino)` match;
  - no name filter is applied;
  - the role map is exact: undeclared files and missing declared files both refuse;
  - empty directories are admitted and don't change the output bytes.
- **Manifest exclusion and self-case.** Only a regular file at exactly `assetManifestPath` (a direct root child) is excluded.
  - It is excluded unread, even at 4 MiB+1.
  - Refused at that path: directory, symlink, dangling link, FIFO, socket.
  - `Manifest.json` and `MANIFEST.JSON` refuse through the namespace. `.bak`, near names and a nested `manifest.json` refuse as undeclared. A declared backup is an ordinary member.
- **Namespace (private build policy).** Segments match `[a-z0-9][a-z0-9._-]*`, at most 255 bytes, no trailing dot, at most 16 segments. This removes case and normalization aliases without widening public LogicalPath, and the verifier grammar is unchanged. `PATH_LIMIT` is unreachable (4095 < 4096). Windows reserved names are admitted.
- **Caps (private build-policy proposals; no sizing claim).**

  | Cap | Value | When it is enforced |
  |---|---|---|
  | Projection digests | 16 | before any filesystem call |
  | Roles | 4096 | before any filesystem call; empty roles also refused |
  | Directories | 4096 | counted during the walk, root included |
  | Listing entries | 4097 | after `listdir`, before any per-entry stat |
  | Member | 16 MiB | fstat size checked before reading (0 bytes read at 16 MiB+1) |
  | Aggregate | 32 MiB | after each member is hashed; at most one member of excess work (48 MiB read before refusal) |
  | Manifest | 4 MiB | after construction; reachable within the other caps |

- **Replacement and growth.** Refused: replacement between lstat and open, a same-length write with mtime restored (ctime still changes), append, truncate, and directory changes.
  - A symlink, removed entry or non-directory swapped in during the race escapes as a bare OSError (ELOOP/ENOENT/ENOTDIR). This fails closed but is not a typed refusal.
  - Declared and confirmed undetected: files added to an already-visited subdirectory, and members changed after hashing.
  - A 1.5 s concurrent symlink-swap stress never emitted outside bytes.
- **Trust and custody.**
  - Every open is dir_fd-relative, single-segment, and carries no write flags.
  - The tree and its mtimes are unchanged, and there are no fd leaks on success, refusal or OSError paths.
  - Re-enumerating through the same fd gives identical bytes.
  - A regular-file root fd refuses. A root opened by the caller through a symlink is accepted, since root selection is caller custody.
- **Owner schemas.** The fixture, a nested bundle and a deep bundle validate against the copied `HostAssetPinV1` and `ReportAssetManifestV1`. The nested bundle's traversal order differs from byte order and includes zero-byte members and all five roles; the deep bundle has 16 segments, a 3846-character path and 16 projections. In Rust, the emitted manifests equal the identity `canonical_bytes(parse_json(..))`.
- **Projection choices.** All 3 (including the middle) and all 16 were verified; `projection_sha256` equals each selection.

## Independent probes and results

Sources:
- `probe-src/assembly_probes.py`, results in `assembly-probe-results.json`.
- `probe-src/assembly_interop_probe.rs`.

Hashes are in review.json.

| Probe | Result |
|---|---|
| p01 owner schema, byte order, interop bundles | PASS |
| p02 caps before IO, observed work bounds | PASS |
| p03 manifest exact exclusion / self-case | PASS |
| p04 extra, unlisted, hidden, nonregular, directory rows | PASS |
| p05 replacement, growth, declared race limits, stress | PASS |
| p06 open flags, fd hygiene, no writes, root fd | PASS |
| p07 projection choices, portable namespace | PASS |
| Rust interop via unchanged verifier | PASS: 19 bundle/projection pairs; canonical bytes; clippy clean |

## Mutation assessment

36 single-edit mutants of the tool were run, with a control passing in each mode.

- **Subject tests kill 16:** T01, T09, T10, T11, T21–T23, T27–T29, T31–T36.
- **Survive subject tests (non-equivalent, 18):**
  - T02: member size pre-check
  - T03: running aggregate check
  - T04: file identity check
  - T05: directory identity check
  - T06: post-open regular-file check
  - T07: `O_NOFOLLOW`
  - T08: `O_NONBLOCK`
  - T12: size equality
  - T13: directory cap
  - T14: listing cap
  - T15: projection cap
  - T16: channel check
  - T17: root-is-directory check
  - T18: **byte-order row sort**
  - T19: empty roles
  - T20: role cap
  - T26: segment cap
  - T30: role path under root
- **Equivalent:** T24 and T25.
- **Review probes** kill everything except T10, T12, T24, T25, T27, T31 and T32. T10, T27, T31 and T32 are killed by the subject tests, so the combined suite leaves only T12 (redundant with timestamps here) and the equivalent T24/T25.

## Required issue

**RQ-A1: permanent tests don't match the claimed behavior.**

- **Byte-order row sorting (T18):** the flat test trees can't distinguish sorted rows from traversal order.
- **Replacement races (T04/T05/T06/T08):** the detection UNIT.md claims is not exercised.
- **Claimed caps (T13/T14/T15/T20/T26):** directory, listing, projection, role and segment caps are untested.
- **Owner-schema minItems (T19):** empty roles are not tested.
- **Caps before excessive work (T02/T03):** the member pre-check and running aggregate check are untested.

Remedy: add permanent vectors, for which probes p01–p07 are a reproducible sufficient set, or narrow the claims. No code change is required.

## Advisories

- **AA-1:** Race-time OSError should be mapped to a refusal code, or callers must treat any exception as refusal.
- **AA-2:** The aggregate cap could pre-check with the fstat size to avoid up to 16 MiB of excess reading.
- **AA-3:** Change detection is timestamp-based and not a snapshot. Because the runtime doesn't check completeness at load, publication custody must bind the tree.
- **AA-4:** `PATH_LIMIT` and the depth check are redundant. Windows reserved names are admitted.
- **AA-5:** The subject's socket test requires a short TMPDIR (AF_UNIX path limit).
- **AA-6:** The embedded verifier no longer carries its filesystem tests, and the consumer covers only flat interop.
- **AA-7:** `jsonschema` is not byte-pinned. The fixture's "independent" digest comes from the same generator process.

## Pending, explicitly not claimed

- D9 delivery mapping.
- The compiled-pin-only route: private compiled `HostAssetPinV1` plus sole `buildChannel`; the emitted pin is never a runtime authority file.
- The actual offline bundle and licenses, with real sizing.
- Renderer schema binding of `projection_sha256`.
- Bootstrap, source and tool closure.
- Immutable publication and release inventory (TR-CORE).
- Host/platform `AssetSource` without a production reporting→platform edge.
- Linux and platform qualification.

No source promotion, report implementation, M1 or release qualification is claimed. The synthetic fixtures are not the OpenSIP report UI.
