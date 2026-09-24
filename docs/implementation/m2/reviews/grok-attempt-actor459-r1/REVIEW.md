# Review: omission premise 458 r2 and attempt/actor 459 r1

Grok is the single reviewer. Claude Opus 5.5 leads. No repository edits. The native lane is released with this report.

Product `e7bd764` is clean aside from the 27 pinned paths. All 27 hashes match `hashes.txt`.

## Subject A — proposal 458 r2

**ACCEPT.** RF-1 from r1 is closed. Nothing new is wrong.

r1 refused Evidence B because a type name in `installRootFilesystems` does not record the omission fact. r2 requires the matched measured row to carry signed `installAclOmission: "no-acl-stored"`, set only after that boot identity passed the fixture set. A missing member or any other value refuses. A type name alone is never enough. `InitialPlatform` takes the per-descriptor `fstatfs` itself. Until the profile-set schema successor (plan 458b) is selected and a signed row carries the member, Evidence B cannot be minted and omitted ancestors refuse.

The fact is still only “no other principal holds a write grant.” The sentinel, the volume capability bit, a successful syscall, and the legacy writer list stay refusals. Scope stays external ancestors. Unit 461 does not gain Evidence B. Private descendants stay “omission is a refusal.”

## Subject B — attempt, actor, private-access refactor, test lock, inventory 65

**ACCEPT-UNIT.** No required findings. Inventory candidate assessment is ACCEPT with no required findings.

### Attempt and actor

`InitialInstallationAttempt` owns one `WorkLedger::new()` under the owner caps. There is no `Default`, so `mem::take` cannot swap a failed ledger for a fresh one. The ledger field is private and no method replaces it. `begin` sets a process flag before the charged entropy draw; a second `begin` refuses even after drop. A failed `begin` also leaves the flag set, so the process does not get a second attempt. Receipts are not `Clone`. `InitialActor` is constructed only by `observe_actor`, which charges `observe_account_accounted`. `recheck_actor` charges another observation and compares raw UID and home bytes. A receipt whose lineage differs is `WrongAttempt`, latches that attempt, and does not spend another observation. Any refusal latches the attempt. Nothing in this module opens a path.

### Home spelling

The home must be `/` plus nonempty components. `.`, `..`, a trailing slash, a doubled slash, a NUL, and a component over 255 bytes refuse. Nothing is rewritten. The bound is the raw path of I: home bytes plus the four suffix components and their slashes, at most 4096 bytes, and home components plus those four, at most 256. `/` alone refuses. That matches owner §2.

### Private-access refactor

`judge_private_descendant` reads the capture in place. Order is state, missing entry, shape, then each ACE. The slice form is `#[cfg(test)]`. Omission still refuses before a supplied foreign allow is read. The 10 private-access tests passed.

### Test lock and scratch

The first `temp_dir` call on a test thread takes one process-wide mutex and keeps it in a thread-local until that thread exits. A later call on the same thread does not lock again. Fixtures drop when the test returns, while the lock is still held. The full security library suite passed once: 428 passed, 2 ignored, 0 failed. No `ChangedDuringRead`. `find` of `opensip-ancestor457-*` under `$TMPDIR` printed nothing. The ancestor scratch runs `chmod -R -N` before `remove_dir_all`. Product walks are unchanged. The helper is `#[cfg(test)]`.

### Inventory 65

One added path, `crates/security/src/initial_installation.rs`, at file index 233. 713 planned files. `package.json` moves from 509 to 510. The imported schema moves from 576 to 577. Bootstrap, the report package, and installation lineage stay on their indexes. The projection helper is byte-identical to inventory 64 and passed, refusing 28 corruptions. This is layout acceptance, not source approval by itself. The source verdict above covers the new file.

## Replay

| Command | Exit |
|---|---|
| `rustfmt --edition 2024 --check` on every changed `.rs` path | 0 |
| `cargo test --locked --offline -p opensip-security --lib` | 0, 428 passed, 2 ignored |
| `initial_installation` | 0, 5 passed |
| `external_ancestor` | 0, 9 passed |
| `custody` | 0, 55 passed |
| `private_access` | 0, 10 passed |
| `opensip-platform --lib work_ledger` | 0, 6 passed |
| `opensip-platform --doc` | 0, 2 passed |
| `cargo clippy --locked --offline --workspace --all-targets` | 0 |
| inventory 65 `verify_projection.py` | 0, PASS, 28 corruptions refused |

## Observations

- A failed `begin` consumes the process’s one attempt. That matches one attempt, and it means an entropy or budget failure cannot be retried in-process.
- `observe_actor` can be called again after success. A later `recheck_actor` is what notices an account change.
- The test lock serializes security tests that touch the temporary directory for as long as the worker thread lives. This run did not hang and did not skip a test.
