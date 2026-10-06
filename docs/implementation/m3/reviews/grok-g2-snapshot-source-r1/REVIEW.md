# Rust G2 declared snapshot-to-source byte join r1 — ACCEPT-UNIT

This accepts the pure constructor that joins one recomputed `snapshot2` descriptor to retained raw bytes. Full snapshot admission, G1 transport, full G2, G2-v launch, and product qualification remain open.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-g2-source-snapshot` is detached at `a67d90711076ab1f54c9457754b2c27d0dfa696d`. `providers/rust/src/lib.rs` is modified and `providers/rust/src/source_snapshot.rs` is untracked. `evidence/g2-snapshot-source.diff` is 14396 bytes, sha256 `9b1aebbcacc8a847f6477b6710ecf4ca97ae8628ee3052333aeb69b1682c8619`. The new file body matches the worktree. The `lib.rs` hunk applied to `HEAD` matches the worktree.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `providers/rust/src/lib.rs` | 194 | `0d0da199a847df62346ed942881cb17834bedf85c83e787b8513b6e1f96645e3` |
| `providers/rust/src/source_snapshot.rs` | 13506 | `7f2d27eabd55dfbc1f268ab18acba6c2947bb7d6ef8244e5df30c2f492d75894` |

`HEAD` `lib.rs` is the accepted source-loader crate root, 169 bytes, sha256 `509caa649bcf00f486754aaa523a338ce057766b21e7349857caa9375464b708`. The hunk adds `pub mod source_snapshot`. `sealed_vfs.rs` and `compiler_adapter.rs` match those accepted bytes (`20e7bd8bc9192a12e6bfe908433ec0db3ffbfb864927739c5815784c0cc49d27`, `0e97afd6b86988d2a50d4652c6246ced7c0cfd2fc3314a3ed4d5be8c1eedfa44`). `main.rs`, `Cargo.toml`, and `Cargo.lock` match `HEAD`. The manifest still has edition 2024, `rust-version` 1.95, and no feature or dependency change.

`schemas/sources/identity-v3.schema.json` is 198423 bytes, sha256 `eb6ec9571f0a14f88139a42184a54d2dfc50042be304174ac23dce90bf3580b0`, the same pin `RegisteredSchemas` requires for `urn:opensip:product-v1:identity:v3`. M3-PLAN-r10, native-evidence, snapshot plan C r6, and the bound v157 source-loader unit record match the subject authority pins. `design-lock.json` matches `HEAD` (545275 bytes, sha256 `66d434aeb6253c6738aea46d4b37c47ef0c2b5a968dbabeca8528c4b93982baa`). Its 103 inheritance rows are parented on inventory v157.

## Join

`from_snapshot` takes `RetainedInputs`, a snapshot id, an explicit virtual directory, and a schema work budget. `RetainedInputs::object` requires the snapshot domain, canonicalizes the descriptor through `encode` (the 4 MiB `MAX_BYTES` cap), and admits `/$defs/snapshot` under the pinned identity schema. Admission enforces `additionalProperties: false`, the six required snapshot fields, `sourceInventory` `maxItems` 100000, and `Blob` rows of `path`, lowercase `sha256`, and `bytes`. `ordered` then requires a logical path and strict path order. The recomputed identifier must be `snapshot2:` plus that digest. A supplied raw hash is not accepted in place of that candidate. Snapshot closure-role rows do not apply, and the constructor does not resolve `resolvedConfigDigest`, `scopeDigest`, or `vcsDigest`.

Every `sourceInventory` row is kept. There is no extension, language, or empty-file filter and no directory walk. `LogicalPath::parse` admits the row path. `blob` rehashes the retained bytes and refuses a missing or substituted blob. Each declared length is checked, including a later path that names a digest already copied. The first verified copy is stored in an `Arc<[u8]>`; later aliases clone that `Arc`. Rows become `SealedSource` entries and nothing else. An extra retained blob receives no path. Any missing, tampered, or wrong-length blob, or any `SealedSource` refusal, returns before a namespace exists. The returned bytes are the owned `Arc`, so replacing or dropping the caller buffers leaves the namespace unchanged. The constructor performs no filesystem read. C r6 item 5 keeps symlinks out of `sourceInventory`; this function neither follows a symlink nor invents one. It builds no dependency catalog, prepared-source catalog, chunked S-R recipe, or 200000-entry substitution.

The ten new tests cover every declared row, shared content, an empty file, a non-UTF-8 file, exclusion of an unrelated blob, a missing blob, a digest substitution, a shared-digest length mismatch, a descriptor substitution, a foreign domain, unsorted and duplicate paths, `..` and a backslash, a file/directory collision, an empty inventory with no ambient path, and survival after the caller map is replaced and dropped. The test module reads the public registered schema sources through `source_requirements` and does not execute the owned byte literals.

## Retained checks

The reviewer did not run rustfmt, Cargo, or a producer. The retained `checks.json` completed at `2026-10-06T16:43:08.760098+00:00` on scratch `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-g2-snapshot-z5dk1i6r`, with `laneOwned` true and `nice` 10. `T1ProducerRan`, `providerLaunched`, `repositoryCodeExecuted`, `fullSnapshotAdmission`, `contextAdmitted`, and `productQualification` are false. `~/Library/Application Support/OpenSIP` was absent at this review, and the Darwin temp `opensip-lanes.lock` was absent. No `HOME` assignment was made.

`unit-tests.log` records 16 tests, 0 failed, 0.11s, after a 0.26s compile: the six accepted loader tests and the ten new join tests. `clippy.log` is the two-line `--lib --tests -D warnings` finish (184 bytes) with no warning text, exit 0.

## Inventory v158

Candidate `docs/implementation/m2/repository-file-inventory.v158.json` is 605254 bytes, sha256 `db650c79d493c833179c3a5e5e4a73d4eef7a7879545fb9e55be249e05f5ca34`. Parent v157 is 604664 bytes, sha256 `a4a327db896a68e359c8a099aa328176d0152f0e8cd0d176651c5b20a58385fe`. Successor record is 307473 bytes, sha256 `aa2b75adb9be798c1720e9a9658a4cf79bd0fd06a57c62d8c34c3804a3ee7317`. Subject manifest is 1455 bytes, sha256 `c500a7b6ae7350f51e26ff44b6ac35485809c87e96880cfdc719eb09d8df7617`. Its seven member hashes match the staged candidate, README, successor, and four evidence files. The subject manifest is the only staged file outside that list.

v158 adds exactly `providers/rust/src/source_snapshot.rs` at index 806 (package `opensip-rust-provider`, role `adapter`, `generated: false`, `standing: proposed`). Files stay sorted and unique. All 1050 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v157 I1-b2 sentence. `plannedRowsChanged` is empty. The successor standing names the Rust G2 declared snapshot-to-source byte join.

The 103 design-lock passages, parented on v157, keep their before and effective text by path. One hundred selectors stay. Because the new file sorts at index 806, three selectors move by one: `schemas/sources/imported-v1.schema.json` from `/files/859/description` to `/files/860/description`, `tools/check_crash_matrix.py` from `/files/892/description` to `/files/893/description`, and `tools/tests/test_check_crash_matrix.py` from `/files/997/description` to `/files/998/description`. No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Full capture and completeness, configuration, scope, and VCS joins, sealed transport, contextual selection, dependency and prepared sources, G1, full G2, G2-v launch, and product qualification remain open.
