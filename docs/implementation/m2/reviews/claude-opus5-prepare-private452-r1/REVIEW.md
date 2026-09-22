# Review: fresh-private preparation 452

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 22:43–22:47Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted diff on product 0192a70: `crates/platform/src/macos.rs` (`ae135730…`, 15475 B), `crates/platform/src/lib.rs` (`18e582d5…`, 4902 B), `crates/security/src/private_access.rs` (`e6bda4ec…`, 20792 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope.

This does not clear inherited ACEs. It is not creator completion, creator wiring, directory creation, absence authority, per-vnode profile qualification, a commit or a selection. O1 and O2 below should close before `prepare_fresh_private_sample` gains a caller.

## Subject and base

- **Product state.** HEAD is 0192a70. `git status`/`git diff` show exactly the three paths (+142/−4, `evidence/subject-diff-vs-0192a70.patch`), and all three pins match.
- **Base.** The base bytes are exactly those accepted earlier:
  - `macos.rs` `2c3f2592…` and capture `8be0f220…`: 451 r3.
  - `private_access.rs` `6e7e485f…`: 450, plus the adopted a11f267 tests.
  - platform `lib.rs` `6418af15…`: 447.
- **`macos.rs` / `lib.rs`.** `append_owner_zero_allow` loses `#[cfg(test)]` and becomes a `pub fn`, re-exported from platform `lib.rs` under `cfg(macos)`. It gains a regular-file-or-directory gate (my r3 O3) and a SAFETY comment. Its semantics are unchanged: append a zero-rights owner allow, fall back only on ENOENT, write on the same descriptor.
- **`private_access.rs`.** New `pub(crate) prepare_fresh_private_sample(kind, invoking_uid, file, work)`:
  1. Capture, accounted.
  2. If the state is `NotReturned`: run a shape-only precondition (owner, type, exact mode, links) through `assess_private_descendant` with a fabricated `Entries(0)` and no entries, then `work.run(descriptor_acl_capture_cost(), append)`.
  3. Capture again, only on the `NotReturned` path.
  4. Run the real predicate, `assess_private_descendant_capture`, on the final sample.
  5. Errors go to the new `PreparePrivateError {Capture, Append, Access}`.
- **Test.** `fresh_private_file_gains_a_zero_allow_and_a_loose_file_is_not_rewritten`.
- **Nothing is wired.** The module keeps `#[allow(dead_code)]`, and `prepare_fresh_private_sample` has no caller.

## Replay (requested)

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on the three paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed; no warnings |
| 03 | `cargo test --locked --offline -p opensip-platform --lib acl_capture_` | **0** — 12 passed; no warnings |
| 04 | `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 05 | extra: warn-level Clippy on platform + security (all targets) | 0 — only the 2 pre-existing diagnostics (`work_ledger.rs`, `trust/retained_metadata_index.rs`) |

The snapshots before and after the runs are identical. Product HEAD, status and index, all four capture/predicate files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. About 3.4 GB of scratch was deleted.

## Native probe of the claims (`evidence/prepare_probe.rs`, results in `mutants.json`)

The probe was appended to a copy of `private_access.rs` in a copy of the tracked tree. The parent directory's group is my primary group throughout. Every case is an assertion, and **all pass on the candidate**.

| Case | Result on candidate |
|---|---|
| U1 fresh 0600 file | `Ok(Entries(1))`: exactly one (kind 1, rights 0) entry; owner rename-over and unlink Ok |
| U2 prepare the same file again | `Ok(Entries(1))`, still one entry (idempotent, no second append) |
| U3 existing owner allow (read) | `Ok(Entries(1))`: entry unchanged (1, 0x2), **nothing appended** |
| U4 inherited `group:everyone allow read` | `Err(Access(ForeignAclAccess))`: ACL unchanged, **nothing appended** |
| U5 fresh 0700 directory | `Ok(Entries(1))`; owner rmdir Ok |
| U6 0755 directory / U7 hard-linked 0600 file / U8 foreign invoking uid / U9 file judged as directory | `ModeShape` / `LinkCount` / `ForeignOwner` / `ModeShape`: each stays **`NotReturned`** (no write) |
| U10 pipe | `Err(Capture(Operation(Unsupported)))`: refused before any write |
| U11 ledger limited to one capture cost | `Err(Append(Budget(Objects)))` and the file stays **`NotReturned`**: charge before the write. A full success charges exactly 3 × capture cost. |

## Mutants (same copy; owner tests versus reviewer probe)

| Mutant | Owner's tests | Reviewer probe |
|---|---|---|
| Q1 drop the shape precondition (write to loose objects) | **killed** | fails at U6 |
| Q2 append even when the first capture is `Entries` | passes (gap) | fails at U2/U3 |
| Q3 drop the final predicate | passes (gap) | fails at U4 |
| Q4 skip the second capture | **killed** | fails at U1 |
| Q5 append before the charge | passes (gap) | fails at U11 |

The owner's test failures under Q1 and Q4 left two scratch directories, because the new test has no `Drop` guard. They are recorded in `evidence/owner-test-leftovers.txt` and removed; they held a zero-rights allow only.

## Required findings

None. Every claim in the request holds on this host:
- the write happens only on `NotReturned` plus the private shape;
- an existing ACL is not rewritten;
- 0644 is refused and stays `NotReturned`;
- a fresh 0600 file becomes `Entries(1)` and is accepted;
- the final decision is the real predicate on a fresh capture.

## Observations (non-blocking; O1 and O2 before any caller)

- **O1 — pin the three unpinned properties.** Q2, Q3 and Q5 survive the owner's test. Add, as the probe validates:
  - an existing-ACL case: owner allow accepted and unchanged, plus an inherited foreign allow refused and unchanged (U3/U4);
  - a second prepare that does not append (U2);
  - a one-capture budget that refuses before any write (U11).

  Add a `Drop` guard as well, and drop the pointless pre-emptive `remove_dir_all` on a nonce path.
- **O2 — accounting for the new public native write.** `append_owner_zero_allow` is a public, unaccounted native mutation. `prepare_fresh_private_sample` charges it with `descriptor_acl_capture_cost()`, a borrowed capture cost that happens to be conservative:
  - 131 edges and about 7.7 KB, against roughly five calls for the append;
  - the append's work is one fstat, `acl_get_fd_np` (filesec plus an ACL copy of up to 128 entries), one membership mapping, one entry creation, and one set.

  Define a documented append cost in platform, plus `append_owner_zero_allow_accounted`/`_reserved` wrappers as the capture has, and keep the raw function crate-private. Then no crate can perform the native write without a charge. Observation-level precedents exist (`observe_account`, `descriptor_name_matches` are public raw), but a write merits the capture's stricter pattern.
- **O3 — the shape gate fabricates `Entries(0)`.** The precondition calls the private predicate with a fabricated `CapturedAclState::Entries(0)`. This is correct here: it only gates the write, and the final decision is on a real capture (Q3/U4 show that matters). It does reintroduce, inside the module, the fabricated-state idiom that 450 removed from callers. A dedicated `private_shape(kind, uid, metadata)` helper, used by both paths, would remove it.
- **O4 — a side effect survives a later refusal.** If the append succeeds and the second capture or predicate then fails (for example after a concurrent change), the zero-rights owner allow remains. It is harmless (non-granting and owner-neutral) and keeps retries idempotent (U2). Document it.
- **O5 — carried from r3, now relevant in production.**
  - The non-ENOENT fetch branch is still verified by reading only. An injectable fetch seam would pin it.
  - Clearing errno before `acl_get_fd_np` remains optional hardening.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed; `prepare` and the export are `cfg(macos)`.
- Membership resolution and Libc allocations remain profile premises.
- There is no inherited-ACE clearing, creator completion or wiring, directory creation, absence authority, per-vnode profile qualification, commit or selection.
