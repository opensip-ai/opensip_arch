# Review: parent observation 460 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Source review of the read half of owner step 5. No repository edits.

Product `9c53c94`. `git status` is exactly the seven pinned paths. All seven hashes match `hashes.txt`. No new file.

## Verdict

**REQUIRED-FINDINGS.** Two findings, both in the new reservations. The walk’s admission rules hold.

## Answers

1. **Every new wrapper charges before its closure.** `open_accounted`, `open_child_directory_if_present_accounted`, `observe_child_absent_accounted`, `observe_filesystem_accounted`, `capture_descriptor_acl_accounted`, `descriptor_name_matches_accounted`, and `recheck_exact_names_accounted` all call `work.run` before the open, capture, name sample, or filesystem sample. `NotFound` on a child open becomes `Ok(None)` inside that scope, so a missing fixed ancestor does not latch the ledger. The reservations for the root-to-H open, the present-child open, and the filesystem sample are short of status reads those closures perform. That is RF-1 and RF-2.

2. **The refusals match the ancestor rules.** An omitted ACL with no premise is `AncestorAclOmitted`; on this Mac that is component 0 (`/`). `NoAclSentinel` stays `Ancestor { AclUnreadable }` because the premise arm requires `CapturedAclState::NotReturned`. A premise whose lineage is not this attempt’s latches via `require_lineage` and returns `WrongAttempt` before any open; the used counter is unchanged. Home and child opens use `O_NOFOLLOW`, so a symlink is `Open` or `ChildOpen`, not `MissingAncestor`. A file at a fixed name is `ENOTDIR`, so it is also `ChildOpen`. A renamed root-to-H component fails the closing `recheck` or the final `recheck_exact_names` (`NameChanged`). Each retained fixed child is checked twice with `descriptor_name_matches_accounted`. `OpenSIP` is `observe_private_directory`: omitted ACL, mode other than `0700`, and a foreign allow refuse, and Evidence B is not applied there. Group or other write, including on H, is `GroupWrite` or `OthersWrite` from `check_external_ancestor`. Root-owned directories with no group or other write stay eligible. `Library` and `Application Support` may keep other read and search.

3. **`preview-v1` absence is one `fstatat` with `AT_SYMLINK_NOFOLLOW` on the retained `OpenSIP` handle**, and only after `Library`, `Application Support`, and `OpenSIP` have been opened. `ENOENT` is `FinalNameAbsent`. A dangling symlink, a file, or a directory at that name is `FinalNamePresent`. Any other error is `Absence` and latches the attempt.

4. **`run` and `require_lineage` do not reset the attempt.** `run` returns `Budget(Closed)` once the attempt is latched, otherwise `ledger.scope`, then `latch_on` sets the flag on any error. It does not replace the ledger or clear `used` or `failed`. `require_lineage` sets `latched` on a mismatch and never clears it. `begin` still swaps the process flag before the lineage draw. `begin_on` is private. `for_tests` is `cfg(test)` and takes the caller’s flag, so a second production `begin` still refuses.

5. **This result is an observation.** `InstallationParentObservation` exposes `outcome`, `home`, and `ancestor`. It has no create method and no barrier receipt. `FinalNameAbsent` is the absence sample. `AclOmissionPremise` has only `#[cfg(test)] for_tests`, so production cannot mint Evidence B and every omitted ancestor refuses. The test admit path samples that descriptor with `observe_filesystem_accounted` and requires local, not union, and a type name in the premise list. It does not read a signed `installAclOmission` row. That row remains unit 462.

The existing `RootObservation` walk is untouched: the `installation_root.rs` diff inserts the new block after `NativeInstallationRoot` and adds tests.

## Required findings

### RF-1: The root-to-H open and the present-child open leave out the kind-check status read

`RetainedDirectory::from_retained_handle` calls `File::metadata` on every handle `root` and `child` return. `retained_path_open_cost` prices the root open, one open per component, and a closing recheck of one reopen plus two comparison stats per directory: `edges = 4N + 4` for `N` child components. Those two comparison stats are the `same` reads. The kind-check `metadata` on the retained handle and on each temporary recheck handle is outside that count: `2(N+1)` status reads inside `open_accounted`. Opening `/` is the `N = 0` case the new test locks at 4 edges; that open performs the initial open, its kind-check, the recheck reopen, its kind-check, and two comparison stats: 6 operations. `recheck_exact_names_cost` uses the same short `recheck_cost_for` twice, so the final name recheck repeats the shortfall.

`open_child_directory_cost` prices one `openat` edge and `name.len() + 1` bytes. A present child still goes through `from_retained_handle`. Each existing `Library`, `Application Support`, and `OpenSIP` therefore performs a status read the reservation does not include. A missing child returns before that read.

Failure: a ledger whose remaining edges equal `retained_path_open_cost(home).edges` admits `open_accounted`. For `/Users/sb` (`N = 2`) the closure still performs 6 kind-check status reads the budget does not record, and a present `Library` adds one more through `open_child_directory_if_present_accounted`. `accounted_open_and_name_recheck_charge_their_published_cost` asserts `ledger.used()` equals the published cost, so the short formula passes. The attempt records the walk as fully charged. Price each `from_retained_handle` status read as an edge and its `stat` buffer as bytes, the same way `child_absence_observation_cost` prices one `fstatat`, in both `retained_path_open_cost` / `recheck_cost_for` and `open_child_directory_cost`.

### RF-2: The filesystem-sample cost omits the status buffer its comment counts

`descriptor_filesystem_observation_cost` says it counts the status read and the `fstatfs`, and “the status and statfs output buffers.” `edges` is 2. `bytes` is `size_of::<statfs>() + size_of::<DescriptorFilesystem>()`. `observe_filesystem` calls `file.metadata()` before `fstatfs`. `child_absence_observation_cost` in the same change adds `size_of::<libc::stat>()`.

Failure: premise admission calls `observe_filesystem_accounted` on an omitted ancestor. A ledger whose remaining bytes equal the published cost admits that call, and the closure still materializes the `metadata` status buffer. The passing parent tests take this path on `/` whenever the test premise is supplied. The byte reservation for that sample is short by one status buffer per omitted ancestor `admits` inspects.

## Replay

Rust is `/opt/homebrew/Cellar/rust/1.95.0/bin`. `cargo --locked --offline`.

- `rustfmt --edition 2024 --check` on the seven pinned `.rs` paths: exit 0.
- `cargo test -p opensip-platform --lib`: 162 passed.
- `cargo test -p opensip-security --lib -- creator_parent initial_installation installation_root`: 19 passed.
- `cargo test -p opensip-platform --lib -- accounted child_absence`: 4 passed. The `accounted` filter also matches the account-observation test.
- `cargo clippy --workspace --all-targets -- -D warnings`: exit 0.
- `cargo test -p opensip-security --lib`: 433 passed, 2 ignored.
- `$TMPDIR` has no `opensip-parent460-*` or `opensip-ancestor457-*` entries.

Do not commit.
