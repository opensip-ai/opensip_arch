# NFM-1 complete candidate native file-manifest computation

ACCEPT-UNIT.

`build` takes supplied `FileRecord` observations and returns one complete candidate array. It counts every record, sorts copies of those records by the raw UTF-8 bytes of `path`, and refuses an equal path after that sort even when the digest or length differs. Each kept row is exactly `byteLength`, `contentSha256`, and `path`. `byteLength` stays the supplied `u64`, encoded with the existing `JsonInteger` range. The wide total is a checked `u128` sum kept beside the array. The existing `canonical_bytes` encoder writes the whole array in that order, under its existing complete 4 MiB bound, and a byte past that bound returns `CanonicalError::ByteLimit` with the buffer dropped. `raw_sha256` of those canonical bytes, the existing `native.dependency-file-manifest.v1` frame from `hash_preimage`, and `raw_sha256` of that frame are returned with the plain count and total. Sorting happens while the observations are still an unadmitted candidate list. The encoder preserves array order. This module does not hash an admitted source witness, construct an owner row, or give the security-owned R3 function a caller-list constructor.

## Subject and candidate

The subject manifest is 5651 bytes, sha256 `a1fa8b702726cee0934c237ff83485e9b20446bfba34f42fb3ece1e71182c552`, schemaVersion 1, unit `NFM-1`, pinned by 25 sorted unique members. Every pin matches the stage.

The candidate is product `d433e5e5b8a0fc1cf11509faddba464c4ccbd711` with five uncommitted product files. Product main is clean at that commit. Architecture HEAD is `2d65da143364fde2b9248f8ab68e2251d0d63707`, the status publication after the charged phase, and the six pinned architecture sources match it. The untracked `docs/implementation/m3/syntax-e/e2s/` tree is outside this unit.

`crates/host/src/lib.rs` grows from 4097 bytes, sha256 `abe1d04f3c291a7caa27f2f3a39973839bfaa935558f48c7aa1ff41b187687e8`, to 4231 bytes, sha256 `c2d5bc1f10a989ea7934d30a41eb80b82ebd5a099f5fd93823c3358ac96add17`. The only addition is a private `mod native_file_manifest` under `#[allow(dead_code)]`. The new module is 3074 bytes, sha256 `1744f1c6a0b4ca58d7f9d0e321ddab49fc9df853832a9d499aa7f74f097ebb68`. The tests are 6293 bytes, sha256 `d377517b7e7cd563d2e23fb6cd7eed794b4261ce5f412b9be4064f64337ad2ff`. The fixture is 1422 bytes, sha256 `20baab4c8c8db53d7f6a27df5c6c72fc3fefab45bafbe349f41474e474e14f52`. Those three paths are new. The stage copies match the candidate bytes.

`design-lock.json` is byte-identical to the base, 611252 bytes, with 136 inventory successors ending at v176 and 154 contract successors. Inventory v176 still has 1174 rows. The new module, tests, and fixture are absent. `Cargo.lock`, `crates/host/Cargo.toml`, the operability checker, dependency policy, guard, source-attempt tests, raw copy, counters, decoder, identity digest and canonical modules, and `native-v2.schema.json` match the pinned base bytes. The domain string is the existing schema domain. The frame prefix remains `opensip.product.v1`.

## Computation

`ManifestError` and `ManifestData` are `pub(crate)`. The external probe against the host metadata reports `E0603` on `opensip_host::native_file_manifest`. A positive probe that names `embedded_schema_registry` compiles. There is no new public error route, filesystem call, process call, or `unsafe` block.

`LogicalPath::parse` preserves the supplied scalar string and performs its existing empty, length, and component checks. It does not apply Unicode normalization. The ordering test keeps composed `é`, decomposed `e` plus U+0301, and `z` distinct, emits them in raw UTF-8 order `e\u{301}`, `z`, `é`, and leaves the input vector unchanged across permutations. The duplicate test refuses the same path for equal and unequal payloads.

The `u64::MAX` control supplies two scalar lengths, expects total `2 * u128::from(u64::MAX)`, and expects the decimal `18446744073709551615` twice in the canonical array. Those lengths are injected quantities. The 4 MiB control uses 36157 zero-digest rows. Extending the first path by 91 ASCII bytes makes the canonical array exactly 4194304 bytes, inside the `LogicalPath` component bound. One further byte selects `ByteLimit`.

The pinned gzip fixture has three regular members, sizes 6, 11, and 0. The focused test decodes that fixture through the existing decoder and reads count 3 and content total 17. `compressed_sha256` is the running SHA-256 of the consumed gzip bytes. The test keeps that digest, the raw array digest, and the native frame digest distinct, and checks both returned digests against `raw_sha256` of the returned buffers.

The three Python vectors recompute to the fixture bytes: an empty array, one ASCII row, and a pair containing U+00E9, a quote, a newline, a zero length, and `u64::MAX`. Each raw-array digest differs from its native frame digest. The Rust test also unframes `native.dependency-file-manifest.v1` and checks that the framed payload encodes back to the same canonical array.

## Census and recorded checks

`tools/operability/exceptions.json` grows from 82763 bytes, sha256 `9acdd657d417f84faa5ba436a8c037fcd62821f01f529933c25c0e979ca0567e`, to 82908 bytes, sha256 `e3cbdc1740e2f740ba790ea0e563a2438caefad68c30c359dbffeafe62ec827d`. The only change is one sorted `mintAudit` row: `crates/host/src/native_file_manifest.rs`, member `from`, kind `call`, count 3. Those are `u128::from`, `BTreeMap::from`, and `i128::from`. All 435 prior rows remain, and every other field remains, including the standing line that this census is lexical and grants no mint authority. The recorded operability result is source 113 with no findings, lock check passed, and mint census 436.

The focused host log is 6 passed and 0 failed, with 250 filtered. The exact bare log is 21 passed and 0 failed: the same 6 tests plus 15 closed decoder tests. The exact compile log is empty. Clippy finished with no warning lines. The release check finished. The formatter log is empty. The whole host suite was not repeated.

Source admission, physical population, custody, same-source provenance, signed profile, owner admission, R3 resolution, full C3a, and qualification remain open. Inventory v177 waits until this code is present on main and receives its own review and bind. Publication is a separate architecture archive and product code commit after acceptance, root assent, and the current source and design checks.
