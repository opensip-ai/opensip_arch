# G2 declared inflated tar-member observation r1

ACCEPT-DESIGN-UNIT. implementationVerdict ACCEPT-UNIT. requiredFindings empty.

Subject manifest `docs/implementation/m3/native-g/g2-tar-members-r1-subject.json` is 2770 bytes, sha256 `1a29f8fa16a6ccec9ad7b71853b141919b47db81dc21efac80f80fd9816a6e84`. All 13 members match the stage bytes. Their paths are sorted and unique, and `successor.json` appears once. Successor `docs/implementation/m3/native-g/g2-tar-members-r1/successor.json` is 2900 bytes, sha256 `8286bcecf071df0efb1c967013b3a66b7adc89cc1553fefbfc557861ebabaa84`. Keys are `schemaVersion`, `standing`, `parents`, `passageOverrides`, and `candidates`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Standing: "PROPOSED G2 declared inflated tar-member observation only; no gzip/full decoder/importer/worker authority".

`candidates` is the other 12 subject members. The record path is absent. Each candidate pin equals its subject pin, and the candidate paths are sorted and unique.

Product HEAD `3d34fc1b31c44e5ccca2f6f9a3cfe1e4519e3c41` and architecture HEAD `6d6d10fa4c8bff0fbef952d257bb9e9fba11aaba` are the pinned bases. Product is tracked-clean (967 files). Architecture is tracked-clean. Its untracked drafts stay outside this unit. `~/Library/Application Support/OpenSIP` is absent. Against that product tree, the candidate differs in exactly the two Rust files below. Stage copies match the candidate bytes, and those bytes match `productAfter`. The same paths at the product base match `productBefore`. `design-lock.json` does not yet contain this successor.

## Parent and authority

One parent. Admitted NE `docs/v2/contracts/product-v1/native-evidence.md` is 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`. That pin is architecture HEAD and design-lock input 43. DS-2 (NE:1681) still requires the exact `.crate` tarball whose SHA-256 equals `lockChecksum`, deterministic extraction into the CAS, and a host-computed file manifest. This helper does not extract, hash, or join a lock. There is no passage override.

C r7 is pinned authority and is not a successor parent. `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md` is 157110 / `a1ee9386da5913c135932891f6f8041cc72834b9bd531b1e6a51ccfccc1d40c6`. `docs/implementation/m3/reviews/codex2-snapshot-plan-c-r7/review.json` is 6476 / `a2af42ba44ca696f1f7d497f54f89f115fdda0a942d25ef9f6ced101bd116329`, verdict ACCEPT, requiredFindings empty, subjectSha256 that law hash. Item 12 CRATE-ARCHIVE-1 rules 2–6 and D2 are the grammar used below. Rule 1 gzip, D1, D3, D4, acquisition and set bounds, and the outside-profile public disposition stay with the importer. This record does not admit C3.

Inventory v166 remains 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`, the lock's last inventory candidate. `dependency_inputs.rs` stays role `validator`. `dependency_inputs_tests.rs` stays role `test`. Neither row pins content.

## Observation

`providers/rust/src/dependency_inputs.rs` inserts 6194 bytes before `optional_lock_text` and deletes none. The pre-existing preimage constructor, helpers, and `mod tests` stay byte-identical around that insertion. No `Cargo.toml` or inflater dependency changes.

`observe_declared_tar_members(name, version, inflated)` borrows the caller slice. `Ok` is returned only after the end region passes, so a late error drops the map. `DeclaredTarMember` holds an existing `LogicalPath` and `&[u8]`. `path()` is the root-stripped logical string. `content()` is the member bytes, padding excluded. Results come from a `BTreeMap`, so paths are sorted and unique.

Rule 2: a non-zero block must be `ustar␠` at bytes 257..263 and version `␠\0` at 263..265. The unsigned sum, with bytes 148..156 treated as spaces, must equal `tar_octal` of that field. `size` is octal, or positive GNU base-256 whose value is above `0o77777777777`. Bit `0x40` (negative base-256), a non-octal digit, and a checked multiply or add that overflows become `Size`. Mode, uid, gid, mtime, uname, gname, the ustar prefix, and padding are not copied into the observation; the checksum still covers the header. Offsets use `checked_add`. A size that does not fit `usize`, or a payload or its padding that runs past the slice, refuses.

Rule 3: only literal `0` and `L` pass. NUL, links `1`/`2`/`K`, devices `3`/`4`/`6`, directories `5`, contiguous `7`, pax `x`/`g`, sparse `S`/`M`/`V`/`N`, and other bytes, including `Z`, are `EntryType`.

Rule 4 and D2: an `L` payload must be 2..=16385 before any payload slice. The header name must be `././@LongLink`. The payload must end in one NUL and contain no other NUL. The path before that NUL must be UTF-8 of at most 4096 scalars. The next header must be type `0`, and its NUL-trimmed name must be a byte prefix of the long name. An `L` before another `L` or any other type is `LongName`. A pending `L` at the first zero block refuses. The effective path is the long name when one was pending, otherwise the NUL-trimmed 100-byte name.

Rule 5: that path must be UTF-8 and must begin with the exact `{name}-{version}/` prefix. The remainder goes to `LogicalPath::parse` (`descriptors.rs:31`), which rejects empty, `.`, `..`, empty components, `\`, NUL, and the scalar and component bounds, and does not normalize. A second insert of the same logical string is `Duplicate`.

Rule 6: the first all-zero 512-byte block starts the end region. That region, including the first zero block, must be all zero, a multiple of 512, and 1024..=10240 bytes. A zero block is not required to carry GNU magic.

`DeclaredTarError` is `Truncated`, `Header`, `Checksum`, `Size`, `EntryType`, `LongName`, `Path`, `Duplicate`, or `EndRegion`. Header `Checksum` is this parser's local sum check. The function does not construct `CratePreimageError::Checksum`, a mismatch label, or a public `missing:` / `undecodable:` reason. It does not inflate gzip, check a trailer, CRC, or ISIZE, apply D1 or D3, read a lock or manifest, count an acquisition or admitted set, materialize a tree, or authorize import, native context, Plan, or Run. The doc comment leaves M3-L's in-effect gate unchanged, and this diff does not touch it.

## Controls

`evidence/checks.py`, `evidence/tests.py`, `evidence/author.py`, and `evidence/freeze.py` were not run. The supplied logs were read.

`dependency_inputs_tests.rs` keeps the product-base bytes as a prefix (42921 bytes) and appends 7999 bytes. The provider had 163 `#[test]` functions; the file adds these 13: `declared_tar_members_are_sorted_and_borrow_exact_binary_contents`, `declared_tar_long_name_uses_effective_utf8_path_at_a_truncated_header`, `declared_tar_long_name_prefix_need_not_fill_the_header`, `declared_tar_metadata_and_padding_do_not_enter_member_observations`, `declared_tar_duplicate_effective_paths_refuse_whole_observation`, `declared_tar_all_nonprofile_types_refuse_including_null_regular_spelling`, `declared_tar_wrong_root_and_nonlogical_paths_refuse`, `declared_tar_checksum_and_gnu_magic_are_enforced`, `declared_tar_end_region_has_exact_named_bounds_and_zero_blocks`, `declared_tar_late_failure_never_yields_partial_members`, `declared_tar_long_name_control_records_refuse_orphans_chains_and_mismatch`, `declared_tar_d2_rejects_oversize_long_names_before_payload_slicing`, and `declared_tar_size_octal_and_positive_base256_follow_the_profile`. The borrow control keeps `z\0\xff` at the archive pointer and sorts `a.rs` before `z.rs`. Metadata and `0xaa` padding stay out of `content`. A 16386-byte `L` refuses before the missing payload is sliced. Base-256 `1` and a `0xff` sign byte refuse; base-256 `0x200000000` is the first value above the 11-digit octal range.

`unit-tests.log` is `cargo test --locked --offline --manifest-path providers/rust/Cargo.toml --lib`: 176 passed, 0 failed, 0 ignored, 0 filtered out. All 13 new names are `ok`. `clippy.log` is the same package with `-- -D warnings`: zero `warning:` lines, zero `error:` lines, `Finished`. `format.log` is empty (0 bytes / `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). `checks.json` records `passed` true, `newTests` 13, inventory 166, and `qualification` false. This review does not select qualification.

After this dual acceptance and root assent, `verify_design` runs on the current main lock, the two Rust files land in one code commit, and this bind lands in a separate lock commit. Nothing is pushed. The record does not grant C3 or product qualification.
