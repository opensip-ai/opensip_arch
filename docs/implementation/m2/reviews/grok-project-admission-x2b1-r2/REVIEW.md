# X2b-1 project admission r2

ACCEPT-UNIT. Inventory v88 is ACCEPT.

Worktree `/Users/sb/code/opensip-ai/opensip-x2b` at `5b5f04cf3132d4aa91ced618d4b40544f2aaf2f5`. `product.diff` is 75293 bytes, sha256 `141d970e7da08eb422f24e21dc62eaa97091f4e987f827b627ca3a699ae7257c`, ten files (1680 insertions, 8 deletions). Pins match hashes.txt. Real `~/Library/Application Support/OpenSIP` is absent.

Replay, Rust 1.95.0, `cargo test --locked --offline`, `CARGO_TARGET_DIR` under this review directory, then removed. `opensip-security` lib filter `project_admission`: 17 passed, 0 failed, 642 filtered out. `opensip-platform` lib filter `directory_volume`: 4 passed, 0 failed, 210 filtered out. The four platform tests are the existing volume-frame tests. The volume-cost charge is the security test `the_volume_sample_is_charged_at_its_true_cost_before_it_runs`. Workspace suite, clippy, fmt, `check_package_edges`, and verify_scratch were not replayed.

## r1 findings

RF-1 is closed. `directory_volume_observation_cost` sums two `status_read_cost` values (objects 0, one edge, the status buffer), two `descriptor_filesystem_observation_cost` values (objects 1, edges 2, `statfs` plus the status buffer plus the filesystem value), and the attribute read (`size_of::<libc::attrlist>()` plus the 40-byte buffer, and one edge). That is the work `observe_with` performs: a metadata sample, `observe_filesystem`, the volume-UUID attribute, `observe_filesystem` again, and a closing metadata sample. `sample_incarnation` passes that cost to `work.run`, which charges it before the closure calls `observe_volume`. A ledger one byte short of that cost returns `Budget`. A ledger holding exactly that cost completes the sample. Both tests passed.

RF-2 is closed. `config_refusal` and `marker_directory_refusal` send a chain row of `HostIo` out as `Chain`, and every other refusal stays `CONFIG.CUSTODY_REFUSED` or `marker-directory-custody`. `ProjectChainRefusal::row` already maps `DescriptorAclCaptureError::Io` and `ProjectChainRefusal::Io` to `HostIo`. `marker_capture_refusal` maps `DescriptorAclCaptureError::Io` to `ProjectAdmissionRefusal::Io` and every other capture error to `marker-custody`. An open of `opensip.json`, `.opensip`, or `project-id.v1` that is not the named absence or kind case returns `Io`. `judge_capture` returns only a private-predicate custody refusal, and that failure stays `marker-custody`. The tests inject capture `Io` and assert host I/O, and they keep `OthersWrite` on config custody, `RootAclOmitted` on `marker-directory-custody`, and `Unsupported` on `marker-custody`. Those tests passed.

`ProjectAdmissionRefusal::row` still has an arm that would publish subject `custody` for a `ConfigCustody` inner whose chain row is `HostIo` or `ExplicitPath`. `examine` and `config_refusal` route host I/O to `Chain` before that arm.

## Inventory

v88 is 327409 bytes, sha256 `30dea59355d07378dbc27487e5eaa71e9798d8006beb03973336d338b71d5fa9`. Parent v87 is 324832 bytes, sha256 `f4240a79718874c8d8e323750b918b11a86ec0b22f7e050f30b53f2472a8d209`, matching the file on disk and the successor parent. Rows go from 760 to 762. The added paths are `project_admission.rs` and `project_admission_tests.rs`. No row is removed. Every inherited row is equal by value. Packages, dependencies, and pending decisions are unchanged. Standing is retitled for this unit. Paths are sorted. Successor `docs/implementation/m2/project-admission-inventory-v88/successor.json` is 20169 bytes, sha256 `6f418fa444e8429abe641e3b28c4f8edcdc9f3c8740ba40df577595646b97277`. Subject `docs/implementation/m2/project-admission-inventory-v88-subject.json` is 2106 bytes, sha256 `9904c7cf5b56b2c72c00b334ebb9d2b45119eeecac73c78fed44c00a8fe1e5e9`.

The `installation_read.rs` description is the v87 text and still ends "Nothing walks from the root again." That sentence is false. `ReadSession::admit_project_root` opens the launch or the explicit path from `/` through retained no-follow handles, and `walk_project_chain` then opens the selected root from `/`, both charged on the session ledger. `verify_design` rejects an inventory successor that changes an inherited row. The v88 README records the sentence as false and gives the replacement: "Captures never walk from the root again; `admit_project_root` alone walks from `/` to the launch or explicit path and the selected project root (law X2 r5, unit X2b-1), charged on the session ledger." That replacement matches the code. Captures still open through the retained installation. This session entry is the walk from `/`. A description-only contract successor is how 461b refreshes an inherited sentence an additive successor carries by value. Recording that successor text closes r1's inventory finding. The row stays the parent value.

`project_chain.rs` still says the root takes S3 directory custody. `judge_project_object` also applies that judgment to the configuration file. No sentence of the carried description is false. The README defers that understatement to the same kind of successor.

The two new descriptions describe this unit. The test row lists the selection, classification, and session cases. The volume-cost test and the capture-I/O test sit beside that list, and each listed case remains what the tests check.

## Judgment calls

r1 calls 1 through 9 stand on this rebase. Call 4's capture `Io` is the host I/O row above. The admission still carries its classification and grants nothing until item 6a's tracking. H remains `Chain::home_spelling`. There is still no write-gate entry.
