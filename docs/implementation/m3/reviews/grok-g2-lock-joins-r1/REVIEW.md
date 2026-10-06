# G2 retained Cargo.lock tuple joins r1

ACCEPT-DESIGN-UNIT. implementationVerdict ACCEPT-UNIT. requiredFindings empty.

Subject manifest `docs/implementation/m3/native-g/g2-lock-joins-r1-subject.json` is 2152 bytes, sha256 `4e721707fde341196c1813349850f3abf67a5cf50c87cec654cdac6c45e43576`. All 10 members match that manifest. Successor `docs/implementation/m3/native-g/g2-lock-joins-r1/successor.json` is 2771 bytes, sha256 `365784b23b8092049593398bb2959e4deb2c01ef8539ff1ad541c4d9dce908a5`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Candidates are the other nine members, in record order, with the manifest pins. Standing: "PROPOSED G2 exact retained lock tuple/checksum/version selective diagnostic; two existing files, no full lock/Cargo/DS/features/native admission".

Product HEAD `efef74eae721c33b1c1b1b5030b463e26cf14fdb` and architecture HEAD `958eca821363996a5bca8e023adda5fdf3793133` are the pinned bases and are tracked-clean. The implementation verdict is the two existing product files. Stage copies match the candidate.

| Path | Before | After |
|---|---|---|
| `providers/rust/src/dependency_inputs.rs` | 9056 / `97e4302cb523aaa51f289fd501b97e7598dec7f2aa0b258230bf15f76b50a733` | 14597 / `a50331159e43ae403bcc17d3a7a3d3120f469e119c11368a78b9deeae1ad68f9` |
| `providers/rust/src/dependency_inputs_tests.rs` | 22854 / `29fee1ff23268f66d209f977bf07de4e96dfa91dd4642b9133040976157eec9b` | 31984 / `8b7231aa284f518258b3351b9bf61bc7ec66bc3300a27d8b466e39419a820464` |

Removing the inserted lock API from the new Rust file reproduces the accepted checker byte for byte, including `check_declared_dependency_inputs` and the helpers. The old test file is an exact prefix: 13 existing `#[test]` functions stay, and nine are appended.

## Parents

All three parents are already accepted, and the architecture bytes match the pins.

- `docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py`, 319894 / `4f800faaf75c36ffd38fa9ae0f3618bee1bedbe586026e280326b0d7d73ebca8`, is a candidate of the bound b-s9 successor and a parent of the bound G2 system-inputs successor.
- `docs/implementation/m3/native-g/toml-views-r1/product/tools/identity/dependency-policy.json`, 56472 / `c1e2f006f51a2c5b6c85214e6963816318f6d39204d86a9ff59004942f6176a5`, is a candidate of the bound TOML-views successor. Product `tools/identity/dependency-policy.json` and `crates/identity/src/toml.rs` (13423 / `55294d354966713f4d11fd79117138e1a21f3ac849580646033681a362684c0e`) and `crates/identity/src/lib.rs` (3274 / `27e4bbf2f35612dbd696baefe28045ffffd3faf473e710134aa67d9a3c2a32cf`) match that bound unit. No pending policy bytes are selected.
- `docs/v2/contracts/product-v1/native-evidence.md`, 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`, is a design-lock input.

`schemas/sources/native-v2.schema.json` stays 280357 / `e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773`. `crates/identity/src/schema_registry.rs` stays 26815 / `a6e34a2fd26e8db5cdb639bdd8921067683fe79653345895f868949cd617cad3`. `Cargo.lock` stays 13130 / `532e04105b6157d25fb52f7379e3b8ae2cd67741711e6cb15a731d9cd7c23bf1`.

## Law and behavior

Native evidence §3.1 requires exact `Cargo.lock` `[[package]]` name and version, `sourceId` equal to the lock `source` string or `""` for a path package, and `lockChecksum` equal to the lock `checksum` or null for git and path. `parse_cargo_lock` admits only lock versions 3 and 4, requires package name and version, and defaults a missing source to `""` and a missing checksum to null. Its later lookup string is inside `dependency_source_set_admit`. This diagnostic keeps the three fields as the tuple `(name, version, sourceId)`.

`check_declared_lockfile_joins` calls `check_declared_dependency_inputs` first. That accepted path still runs the universe, context, nested-frame, snapshot, dependency-manifest, member, and inventoried lock-byte retention checks. The new function then loads that same retained blob and parses it with `opensip_identity::parse_toml`, which reads the whole document before exposing fields. `TomlError` (`ByteLimit`, `RecursionLimit`, `NodeLimit`, `InvalidUtf8`, `Syntax`) stays `DependencyLockError::Parse`. Those bounds remain the parser's local development limits (`MAX_NODES` is 1_000_000 in the accepted TOML module).

The root `version` must be a TOML integer. `u8::from_str_radix` uses the view's normalized digits and radix. The value must be 3 or 4 and equal the descriptor `lockfileIdentity.lockfileVersion`. A string, bool, value outside 3 and 4, an integer that does not fit in `u8`, or a parsed value that differs from the descriptor is `Shape("version")` or `Version`.

Each lock row must be a table with string `name` and `version`. A missing `source` becomes `""`; a missing `checksum` stays `None`. The map stores every checksum under that exact tuple. There is no trim, case-fold, or delimiter encoding. For each descriptor package, zero matches is `MissingTuple(index)` and any count other than one is `AmbiguousTuple(index)`. The single retained checksum must equal `lockChecksum`, and JSON null means absence. Descriptor `lockChecksum` is already schema-limited to 64 lowercase hex or null by `DependencyPackageSourceV1` before this join. The comparison copies that string; it does not recompute a registry digest.

A missing `package` key leaves the row count at 0. Unselected rows, including duplicate unselected rows, stay in that count only. Success returns `DependencyLockChecks`: the upstream dependency observations, `lockfile_version`, and `lock_package_rows`.

`DependencyLockError` is local: `Inputs`, `Parse`, `Shape`, `Version`, `MissingTuple`, `AmbiguousTuple`, `Checksum`. DS-1 through DS-6, source kind, acquisition, vendor and tarball authentication, git provenance, activated features, and completeness remain in the reference model's `dependency_source_set_admit`. This function does not read Cargo metadata, the filesystem, or the environment, and it does not mint `NativeContextVerified`, Plan, or Run.

The nine new controls use the existing owned fixtures (`example.invalid`, inert blobs, and the unadmitted sysroot fixture). They cover an exact version-4 tuple join after the retained checks; versions 3 and 4 spelled as decimal, `+4`, `0x4`, `0o4`, and `0b100`; refusals for 2, 5, `-4`, a 2^128 literal, and a parsed 3 against a declared 4; each tuple coordinate alone; duplicate selected rows; checksum equality, absence, and mismatch; omitted and empty path sources; full-document syntax and field-type errors; an empty package array and duplicate unselected rows with descriptor package count 0; and missing or shorter substituted lock bytes on the existing retained-input error.

## Evidence and inventory

Supplied logs, read only. The authoring script `evidence/checks.py` takes the lane lock, runs rustfmt and Cargo, and writes its own checks file. It was not executed.

`evidence/unit-tests.log` (13274 / `42b9bd6f3af38d8ed750075ac8fea423681de4056a90152d0b08cdeb3f02f9ba`) is `cargo test --locked --offline` of `providers/rust` on the candidate. It finished the test profile in 17.51s, ran 126 tests, and reported `ok. 126 passed; 0 failed` in 4.40s. All nine new tests passed, as did the existing lock-byte retention test. That is the prior 117 Rust-provider library tests plus these nine.

`evidence/clippy.log` (917 / `b766a14825cbc96030b6f36b04e8adf06e90ebc88a6459fef3c6f66f4833f82f`) is the authoring script's `cargo clippy --locked --offline --lib -- -D warnings` run. It checks `opensip-rust-provider` on the candidate and finishes the dev profile in 13.12s with no warning text. `evidence/format.log` is empty. `evidence/checks.json` records `passed` true, `newTests` 9, private `0700` directory `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-g2-lock-3r0_a73z`, inventory 166, and `qualification` false.

Inventory v166 is still 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`, the last inventory successor. Both Rust paths are already rows. Row keys are `description`, `generated`, `package`, `path`, `role`, and `standing`, with no content sha256. Across 967 tracked product files, the candidate differs only in these two Rust files and `design-lock.json`.

The candidate lock is 560797 / `8065495fd247dd4f9941a9bb7fc3187b26388854b910e26ca878e7bd254d2b64` (111 contract successors). HEAD is 562569 / `5d50b000506de4935219491049dae5759283b9e2c4e48e7a621fb2970565764c` (113). The candidate lock is a prefix. The two later records are the already-bound G2 system-inputs successor `c7fc94c91ec832eb09f359ae1c881b65b32088265420d26d927ecec485505c76` and the TOML-views successor `33c92dc7afdf704008ab0a18dc24478319f9de852035ff27fef0f32da5f86649`. Approvals, inputs, the 126 inventory successors, and inheritance match. The code commit lands on HEAD and leaves that lock in place. Design-lock binding is a separate commit. Nothing is pushed.

`~/Library/Application Support/OpenSIP` is absent. This record does not admit a Cargo lock, a dependency source set, native context, a provider, or a qualification.
