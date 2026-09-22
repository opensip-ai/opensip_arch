# Re-review: create one private regular file 453 r2

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation (so no workflow was used, despite ultracode). All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 23:28–23:33Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/security/src/private_access.rs` on product 1df6373 (`d160d37d…`, 31643 B) | **ACCEPT-UNIT, this source boundary only** | none |

review.json carries top-level `"verdict": "ACCEPT-UNIT"` and `requiredFindings: []`, and `sourceVerdict` repeats the scope. This is not the installation creator. It is not parent admission, directory creation, absence authority, per-vnode profile qualification, a commit or a selection. O1 below should close before any caller.

## Subject

- **Product state.** HEAD is 1df6373, which holds the 452-r4-accepted bytes; the rejected r1 version was never committed. `git status`/`git diff` show only this path (+171/−0, `evidence/subject-diff-vs-1df6373.patch`), and the pin matches.
- **`create_private_regular_file(parent, name, uid, work)`.**
  1. **Validate the name.** `to_str()`; empty, `.`, `..` or containing `/` → `Name`. No native work happens before this.
  2. **Reserve the whole operation.** `follow = capture + append + capture`, computed with checked addition. Then `work.effect(create_cost {1 object, 1 edge, 0 bytes}, follow, |post| …)`, which charges the effect and all follow-ups **before** the action.
  3. **Inside the action:** `create_new` with mode 0600, then `file.set_permissions(0600)` on the descriptor (an fchmod), then `prepare_fresh_private_sample_reserved`. That runs a reserved capture, `private_shape`, a reserved append, a reserved capture, and finally the real predicate.
  4. **Errors** come back as `WorkFailure<PreparePrivateError>`. Budget failures are lifted to the top level by `lift_capture`/`lift_append`.
- **Doc comment.** "A later refusal can leave that file behind."
- **Test.** `created` → `Entries(1)` with mode 0600; `a/b`, `""`, `.`, `..` → `Name`; a `{1,1,1}` ledger → `Budget`, and `unpaid` does not exist.

## 453 r1 closure

| r1 item | Status |
|---|---|
| **RF-1**: creation before any charge | **closed.** `work.effect` reserves create + both captures + append before `open`. Probe C1 and C1b show nothing is created under any insufficient ledger (including one edge short), and C8 shows a success consumes exactly the full reservation. Mutant E1 (nothing reserved before create) is killed by the owner's test. |
| O1: residual file after refusal | **documented** (doc comment). A retry with the same name still fails `AlreadyExists` (C2). |
| O2: path-based parent | open (carried; C6 unchanged) |
| O3: umask | **closed.** `set_permissions(0600)` on the descriptor; probe C0 under **umask 0277** gives mode 600 and is accepted. |
| O4: name tests | **closed** (`""`, `.`, `..`, `a/b` tested; non-UTF-8 is covered by the probe only) |

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check crates/security/src/private_access.rs` | **0** |
| 02 | `cargo test --locked --offline -p opensip-security --lib private_access` | **0** — 10 passed; no warnings |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | **0** — 0 warnings |
| 04 | extra: warn-level Clippy on security | 0 — only the 2 pre-existing diagnostics |

The snapshots before and after the runs are identical. Product HEAD, status and index, all four capture/predicate files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. TMPDIR had zero leftovers. About 3.4 GB of scratch was deleted.

## Native probe (`evidence/create_probe.rs`; normal umask and umask 0277)

The probe was appended to a copy, run and removed. **All 22 cases pass on the candidate, at both umasks.**

| Case | Result |
|---|---|
| C0 create `ok` | `Ok(Entries(1))`, mode 600, also under umask 0277 |
| C1 `{1,1,1}` ledger | `Err(Budget(Objects))`, **file absent** |
| C1b ledger = create + capture + append + capture | `Ok(Entries(1))`; one edge short gives `Err(Budget(Edges))`, file absent |
| C8 success | ledger used equals the full reservation exactly |
| C2 parent with inheritable `group:everyone allow read` | `Err(Access(ForeignAclAccess))`; ACL still exactly the inherited (1, 0x2) entry (nothing appended); residual file (documented); retry gives `Create(AlreadyExists)` |
| C9 parent with inheritable owner allow | `Ok(Entries(1))`; entry unchanged (1, 0x2), nothing appended |
| C3 `""`, `.`, `..`, `a/b`, `/abs`, non-UTF-8 / NUL | `Name` each / `Create(InvalidInput)`; directory listing unchanged |
| C4 existing name / C5 final symlink | `Create(AlreadyExists)`: existing file untouched / symlink target not created |
| C6 parent given through a symlink | `Ok`, and the file lands in the target (carried O3) |

## Mutants (copy restored and re-verified)

| Mutant | Owner's tests | Reviewer probe |
|---|---|---|
| E1 nothing reserved before create | **killed** | fails |
| E2 no `set_permissions` | passes | passes at the normal umask; **fails under umask 0277** (mode 400) |
| E3 reserved preparation skips the final predicate | passes (gap) | **fails at C2: the create returns `Ok(Entries(1))` with an inherited foreign allow** |
| E4 reserved preparation appends even to an existing ACL | passes (gap) | fails at C2 (an entry is appended) |
| E5 drop the `/` check | **killed** | fails |

## Required findings

None. RF-1 is closed and verified natively, and every claim in the request holds.

## Observations (non-blocking; O1 before any caller)

- **O1 — the duplicated preparation's `Entries` branch is unpinned.** `prepare_fresh_private_sample_reserved` is a second copy of the preparation algorithm. The owner's create test exercises only its `NotReturned` path.
  - E3 shows the risk: dropping its final predicate would make a create under a parent with an inheritable foreign allow **succeed**, returning a file that grants foreign read. No owner test notices. E4, appending to an existing ACL, is likewise unpinned.
  - Preferred fix: **one algorithm.** Give the reserved implementation a `kind` parameter and make `prepare_fresh_private_sample` a thin wrapper, `work.effect(WorkCost::default(), capture + append + capture, |post| reserved(kind, …))`, so the existing, well-pinned prepare tests cover both callers. The trade-off is that the accounted path then reserves all follow-ups up front, which is conservative.
  - Alternative: add create tests under an inheriting parent, with the probe's C2/C9 shapes: foreign → `Access`, with nothing appended; owner → accepted, unchanged.
- **O2 — the umask fix is unpinned.** E2 survives at the normal test umask. The security crate forbids `unsafe`, so the test cannot change the process umask. Either accept the reviewer evidence (probe under umask 0277), or run a check in a child process started with a restrictive umask.
- **O3 — the parent is still a path (carried r1 O2).** It is a kernel-resolved `&Path`, followed through symlinks (C6) and CWD-relative when relative. Before any caller, take an admitted `RetainedDirectory` and create handle-relatively (`openat` with `O_CREAT|O_EXCL|O_NOFOLLOW`), as the platform filesystem layer does.
- **O4 — the residual file blocks retries.** It is documented, but a retry with the same name fails `AlreadyExists` indefinitely. A handle-relative version could remove the file on refusal after an inode identity check.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed.
- Mutation measures test strength; it is not a proof.
- This is not the installation creator, parent admission, directory creation, absence authority, per-vnode profile qualification, a commit or a selection.
