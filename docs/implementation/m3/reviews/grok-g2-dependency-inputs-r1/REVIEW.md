# Rust G2 declared dependency-manifest/member byte checks r1

Verdict: ACCEPT-UNIT.

`check_declared_dependency_inputs` runs the accepted universe, context, and retained-input joins first. It then retains the selected `Cargo.lock` raw bytes and checks each package file manifest's identity, count, byte sum, and member bytes. `DependencyInputChecks` keeps those universe checks, the dependency digest, and the package, file, and byte counts. It grants no authenticated provenance, complete dependency input, activated-feature derivation, `Cargo.lock` parse, tarball or vendor-checksum admission, import or acquisition admission, dependency mount, context, universe, or Plan admission, `NativeContextVerified`, or execution or provider authority. Other verification and provenance labels remain caller declarations. Full owner semantics stay upstream. Full G2, provider launch, and product qualification stay open.

## Declared bytes and counts

The selected dependency id is the universe `dependencySourceSetId` with its `sha256:` prefix removed, loaded as a nested `native.dependency-source-set.v1` frame. The snapshot inventory row whose path is the lock path supplies the length, and `blob` plus `require_length` retain the lock `contentSha256` preimage at that length. A missing, substituted, or length-conflicting lock blob refuses. The fixture lock is opaque raw bytes. This function does not parse `Cargo.lock` syntax, tuples, sources, or revisions.

Each package `fileManifestSha256` is framed as the nested H preimage of `native.dependency-file-manifest.v1`. Current-schema admission owns sorted unique paths: `uniqueItems` and `x-opensip-order` `path` refuse a reversed path, a repeated path, and an escape before member bytes are consumed. A missing or substituted manifest preimage, and a foreign nested domain presented as the manifest, refuse.

`fileCount` must equal the admitted manifest length. `totalBytes` must equal the checked `uint64` sum of declared `byteLength` values; overflow is `CountOverflow` before those member blobs are read. Each `contentSha256`/`byteLength` pair is then retained exactly. The length memo is local to the immutable request. A repeated digest with the same length is not hashed again, and a conflicting length returns `BlobLength`. Shared bytes still count once per manifest row and once per package. The cross-package file and byte totals use checked addition.

`checksumVerification` equal to `mismatch` refuses the observation. `tarball-matched`, `self-consistent`, `not-applicable`, `registry-authenticated`, and `declared` are left as labels. The result type has no provenance or authentication token. `lockChecksum` is not recomputed. Local errors are `DependencyInputError` values with static field names, not new wire vocabulary. The library performs no filesystem, tool, compiler, provider, or measurement call.

The diff changes no package edge, default provider, or production Rust pin.

The worktree is detached at `7f354afde6b08f1ebf1055e82a39a719bffeec11`. The only product changes are `lib.rs` appending `dependency_inputs`, plus the two new files. The evidence diff is 33713 bytes, sha256 `c8d30bcbd0656d4cdb5014cd6e2ba822d04af21007579dd4b29451afa5b9803d`. The `lib.rs` hunk matches `git diff`, and both new-file bodies match the worktree. Pinned schemas and the four architecture authorities match, including the accepted v164 unit. The author log records 95 library tests, including the 13 new dependency-input tests, and warning-denied Clippy, both exit 0, under `nice -n 10`, locked offline Cargo, and a mode `0700` scratch. The supplied script does not assign `HOME`. The OpenSIP support directory is absent. This review did not rerun Cargo, rustfmt, or Clippy.

## Inventory

Subject manifest sha256 `df5a9ff32058160c9104c7f4df90eee23ecf306d97812cb70983672cd6e6029e` (1468 bytes). Its seven files match.

Candidate `repository-file-inventory.v165.json` is 613658 bytes, sha256 `b66c5dea181c22e697bf7609985bdf15391eb37aa1de7913575bc4faf557df40`. Parent v164 is 612452 bytes, sha256 `dc9ba6b87ef35582da4ebe80c4d46d61c4a26b64dd8c87fd125b3a6311627910`. Successor `docs/implementation/m2/rust-g2-dependency-inputs-inventory-v165/successor.json` is 307533 bytes, sha256 `c7666d09e61a391d6cf0290e1325b9033403a22f1e90b78283b11e232bcccd1d`.

v165 has 1065 sorted unique paths. The additions are `providers/rust/src/dependency_inputs.rs` at index 803 (package `opensip-rust-provider`, role validator) and `providers/rust/src/dependency_inputs_tests.rs` at index 804 (role test). All 1063 parent rows are unchanged. Packages stay 20 and pending decisions stay 9. The candidate standing sentence remains the v164 I1-b2 sentence. The successor standing names the Rust G2 declared dependency-manifest/member byte authoring component. All 103 description projections keep the v164 before and effective text, keyed by stable path. Three selectors move by two: `schemas/sources/imported-v1.schema.json` 870 to 872, `tools/check_crash_matrix.py` 903 to 905, and `tools/tests/test_check_crash_matrix.py` 1010 to 1012.
