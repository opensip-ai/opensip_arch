# C3 R6 pinned source and one producer fixture r1

ACCEPT. requiredFindings empty. fullR6Complete false. fullC3aComplete false. productQualification false.

This is the scoped evidence archive. It does not bind an inventory, amend CRATE-ARCHIVE-1, or accept full R6 or C3a. J3b and the other accepted units stay closed.

Subject manifest `docs/implementation/m3/snapshot-plan-c/c3-r6-producer-evidence-r1-subject.json` is 10158 bytes, sha256 `f5556d711bbddfd97b7ebd2466b454ccd1b1445966be6f2b70b2b12d7be0588e`. All 43 members match their byte and hash pins. Their paths are sorted and unique.

## Provenance

Product HEAD is base `bf1ce2566120bcb7db339c3c8a1ee3853f300c8c`. Architecture HEAD is base `50f54d52c50d17ad45dfc6c4b650826c7cbd230d`. `PROPOSAL-r7.md` at that architecture commit is 157110 / `a1ee9386da5913c135932891f6f8041cc72834b9bd531b1e6a51ccfccc1d40c6`. Product `tools/host/dependency-policy.json` is 4373 / `5b15dab94caf7fc0ff0cc2e5e22ad9614081c029ca51ef4f03059f9d0d810b2d`, and the staged copy is the same bytes. Product `crates/identity/src/descriptors.rs` is 27429 / `0477db5b64f63902fb07af5b02d4a7f39d752fbbb1a9165725c64e3c1d3e5e12`. `probe/logical_path.rs` is 2745 / `42d6721015d51be7cea9f2cff303486cbaf64666526bf585bf24a6e400ebb4b0` and is a byte prefix of that file. Its `parse` is the function at `descriptors.rs:31`.

The installed Cargo binary contains commit `f2d3ce0bd7f24a49f8f72d9000448f8838c4e850`. `rustc-version.txt` records rustc 1.95.0 commit `59807616e1fa2540724bfbac14d7976d7e4a3860`, and that string is in the same Cargo binary. Cargo and rustc were not executed. The pinned `Cargo.lock` has one `tar` 0.4.45 row, checksum `22692a6476a21fa75fdfc11d452fda482af402c008cdbaf3476414e122040973`, and one `flate2` 1.1.9 row, checksum `843fba2746e448b37e26a819579957415c8cef339bf08564fe8b7ddbd959573c`. Both `.crate` files match those checksums. `tar-0.4.45/src/builder.rs`, `tar-0.4.45/src/header.rs`, and `flate2-1.1.9/src/gz/mod.rs` are regular archive members and are byte-identical to the copied sources. Cargo's own lock also names `miniz_oxide` 0.8.9. The inflater rows used here are the policy rows, `miniz_oxide` 0.9.1 and `adler2` 2.0.1, and those crate bytes match the policy checksums.

The r7 descriptions came from docs.rs `latest`, so their line numbers are not the pinned lines. The pinned writes match the described behavior, and no profile amendment is selected. `tar` uses `GzBuilder.filename` and `Compression::best`, one `Header::new_gnu` per entry, the `<name>-<version>/` prefix, deterministic on-disk metadata, and `append_data` for on-disk and generated regular files. `into_inner` calls `finish`, which writes 1,024 zero bytes. A path that does not fit the 100-byte name gets one `L` record named `././@LongLink`, a payload of the path plus one NUL, and a regular-header name truncated to a valid UTF-8 prefix. `new_gnu` sets magic `ustar ` and version ` \0`. A 12-byte size uses base-256 once the value no longer fits eleven octal digits. flate2 writes the filename with `as_bytes_with_nul`.

## Producer

`package-run.json` records `/usr/bin/nice -n 10`, Cargo `package --no-verify --locked --offline --allow-dirty`, exit 0, and private `TMPDIR` `.../opensip-c3-producer-x1_2y7w3`. That directory is still mode `0700`. The fixture manifest has no dependencies. Its lock names only `opensip-c3-archive-probe` 0.1.0. The Unicode path component is 160 bytes.

`producer.crate` is 938 / `ad1d0755b27478b4b1ec0129756269bbddbf0140642cc23b97a0a386463c3341`. The live package path named by the oracle is the same bytes. Independent gzip and raw-header reads agree with `producer-oracle.json`: `CM` 8, `FNAME` only, filename `opensip-c3-archive-probe-0.1.0.crate`, inflated 10752, five regular files, 4660 content bytes, and 1024 trailing zero bytes. All six headers have GNU magic and a matching checksum. The `L` payload is 213 bytes, the 212-byte path plus one NUL and no other NUL. The following regular name is 100 bytes, valid UTF-8, and a byte prefix of that path. `tarfile` reports the same five regular members and the same content hashes. `Cargo.toml.orig`, `payload.txt`, and `src/lib.rs` match the fixture bytes.

Read sizes 1, 7, 511, 512, 4096, and 32768 each inflate that archive to the same 10752 bytes, five files, 4660 content bytes, and 1024-byte zero end, with no unused gzip tail. The D3 bound holds at each of those sizes. Those are the six sizes in `exact_pinned_cargo_long_name_archive_passes_incremental_profile`, which records the same counts.

## Controls

`tests.log` records 15 passed and 0 failed. Those names are the fifteen `#[test]` functions in `probe.rs`. The recorded rustc argv includes `-D warnings`. `build.log` is empty. The compiler was not rerun. The linked `libminiz_oxide.rlib` is still 556112 / `26014582ff81ba0ad677664af89b708bd6eaaa020b25b56f7b6d8071cd70636f`, and `libadler2.rlib` is still 67328 / `a68280dc31a589b9359a17cbed60b9f0892a601b3909ebc555d3d5b5437bede8`.

The five inflater inputs decompress to their pinned inflated bytes. `fixtures.json` compressed lengths are the raw DEFLATE spans inside those gzip members: 70477, 13329, 1342, 2, and 100035. The two policy archives contain only type `0` members and a 1024-byte zero end. `miniz_oxide` 0.9.1 has 23 files and 296000 content bytes. `adler2` 2.0.1 has 13 files and 38832 content bytes.

The FNAME loop treats the terminating NUL as one of the 4,096 bytes. `source.json` leaves that reading pending and does not select it as successor law. This producer's filename field is 37 bytes, so the reading does not decide the fixture. `long_header_byte_prefix_may_split_utf8` builds its own 100-byte prefix, checks that the prefix is not valid UTF-8, and accepts it under rule 4's raw byte-prefix comparison. The Cargo archive above does not use that split prefix.

The probe source has no lock-checksum authentication, acquisition or final-set counter, scratch materialization, activation, wrapper custody, or NIJ-1 join. Full R6 still owes the product-library pin-time report over T2 after lawful C3a integration. `~/Library/Application Support/OpenSIP` is absent. Neither repository was edited.
