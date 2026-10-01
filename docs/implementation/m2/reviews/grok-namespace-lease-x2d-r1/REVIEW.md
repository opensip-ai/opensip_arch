# X2d r1 — namespace admission and leases

Implementation review. Product worktree `/Users/sb/code/opensip-ai/opensip-x2d` at `0206ce8673ade3689331fe22801458a03646f502`. `git diff` is 75110 bytes, sha256 `90009b2e2fef312064a496bb7402b195146eebf03132876dd066544ce465bbb6`: 6 files, 1620 insertions, 20 deletions. The six product pins match `hashes.txt`. `~/Library/Application Support/OpenSIP` is absent.

Law is X2 r8 item 7, with the ordering note, the r6 fence-free recovery exception left to X6, and items 3, 4, 6a, 8, 9 and 10's X2d row. Item 7a is not built. S7 levels 1 and 2 are nonblocking and never upgraded. X3b r8, as committed at arch `320ee4d38`, puts the floor step under the fence before this lease; this unit does not compose it.

## Item 7

N comes only from the current registry owner's ACTIVE row. Eligible requires classification `Eligible {N, P}` and exactly one ACTIVE row at that N with project P. Registered requires R2's row still ACTIVE and still classifying `Eligible {N, P}`, and the confirmed directory's identity equal to the directory X2c published. Any other classification is `NotEligible`; any other row shape is `Invariant`.

`admit` confirms `host`, `projects` and N as private directories, exactly named, on the parent's device, and opens both carriers no-follow as private regular files (owner, 0600, one link, ACL). It takes no project lock. `NamespaceTarget` borrows the holder, exposes the namespace directory, the row snapshot and the subject, and is the floor-step seam. The probe test takes and releases `writer.lease` through that directory, then the lease succeeds.

`lease_writer` offers APPEND-WRITE (`writer.lease` LOCK_EX|LOCK_NB) and EXCLUSIVE (`writer.lease` LOCK_EX|LOCK_NB, then `readers.lease` LOCK_EX|LOCK_NB). `lease_shared` offers SHARED-READ (`readers.lease` LOCK_SH|LOCK_NB) and is implemented only for `&ReadSession`. There is no upgrade, no serialized form, no Clone and no release method. A busy lock is `RegistrationRow::Busy`. Lock I/O is the host I/O row. `HeldLease`'s drop releases `readers.lease` before `writer.lease`, and `FileLock`'s drop discards an unlock error. That drop runs before the fence: the writer is borrowed `&mut`, so `release` cannot run while the lease lives, and the session is borrowed `&`, so the session cannot be dropped either. A refusal inside `fenced` drops the value the step returned, spends the gate or latches the session, and leaves the fence held.

Item 6a's tracking recheck runs inside the subject's recheck, before confirmation on admit and before the first lock on lease. The locks and the post-lock binding and directory rechecks are one `effect` plus `prepaid`. The reserve is one `LOCK` per lock taken (0 objects, 3 edges, 512 bytes: the kind-check `stat`, `F_GETFD` and `flock`), each locked carrier's reopen and ACL capture, and three directory rebinds. Those constants match the charged helpers. A shortfall spends nothing from the locks. Unlocking on drop is uncharged.

## Judgment calls

1. The code lives in `opensip-security` and uses `FileLock`. `lifecycle::leases` is a private module, and security has no edge to lifecycle. The two-lock order matches that module's `acquire_project`. No crate edge is added.
2. Two phases are the right seam. `admit_namespace` returns a lock-free target; only `lease_*` locks, and it reruns the subject, directory and carrier rechecks before the first lock. A closure inside one call would hide the point X3b-3 needs.
3. The fence borrow enforces "X2d does not release the fence" and "lease, then fence". Until X2e the value can only be rechecked or dropped. Unlock errors on drop are not reported, which matches a type that has no release method.
4. The write gate offers APPEND-WRITE and EXCLUSIVE. The read session offers SHARED-READ only, and its `admit_namespace` builds only `Eligible`. The fence-free recovery selector is not built.
5. Eligible admission checks custody of `host`, `projects`, N and both carriers. It does not require X2c's exact two-entry footprint. A Registered subject still runs `recheck_registered`, which calls `confirm_footprint`. That is the right split inside X2d. X2e and X3b-3 must not run `FencedNamespace::recheck` on a Registered subject after the carrier and witness appear in N unless that footprint check is relaxed.
6. The rows match item 8. FirstUseCandidate and a constructed `NotEligible(Eligible)` are invariant. RecoveryNeeded and OneSided are `identity-recovery-required`. Contradiction is `identity-contradiction`. A missing `host`, `projects`, N or carrier is the incomplete row. Custody subjects stay `private`, `symlink`, `not-a-regular-file` and `volume-unsupported`. A changed owner is `required-files-changed`. Busy is the new `RegistrationRow::Busy`, naming the existing `LEDGER.BUSY_TIMEOUT` / `PROJECT.BUSY` row. No public code is added.
7. Busy spends the gate or latches the session, like every other refusal on these ledgers. With one gate per process, the backoff retry outside the fence belongs to the composition owner, not to X2d.
8. Admit rechecks the subject, then confirms, then the holder's full recheck. Lease rechecks the subject, both directories and both carriers before the lock, then each locked carrier's name binding and the directories, then the holder's recheck.
9. The post-lock work is reserved before the first `flock`. The budget test cuts the session at 0/4 through 3/4 of the measured lease and each cut refuses with no lock held and the fence still held.
10. Trust groups, environment and system sources are arguments of each call. There is no production wrapper.
11. Item 7 names no transition gate. `transitions_quiet` is untouched and stays registration-only.
12. `ordinary_writer.rs`'s inventory description is the v105 text, carried by value. It does not mention the lease. That refresh stays with the description-only successor already named at inventory 97, 101, 102 and 105. The descriptions of `custody.rs`, `installation_read.rs` and `first_registration.rs` are also unchanged and remain true: the session gains a shared lease and not a write capability, and `first_registration.rs` still takes no lease.

## Inventory v110

Parent v105 is 359222 bytes, sha256 `ebd9cf3361d4f854adcfbe8fcffd8e6e5ca9bd0af38315f950638212b5934a08`. Candidate v110 is 363022 bytes, sha256 `8a7aad24ddea50c4eac58667659b900cbaf732b5aed04fef8b360af1736995a0`. Subject manifest is 2135 bytes, sha256 `4ba60b8b47529cfe8fed82b809570918e9a48ae5be38e1f2a7ca4dd4ecc869f8`. Successor record is 20199 bytes, sha256 `b3dce33a4c7e3ba6a5294fb726c1e35b166bb23e2a56c120a17456c80d9e1b23`.

All 785 parent file rows are equal by value. The two added paths are `namespace_lease.rs` and `namespace_lease_tests.rs`. `packages` and `pendingDecisions` are equal. The standing sentence is the v110 header. `build_v110.py` was not rerun: it writes the candidate and the successor into the architecture tree.

`verify_projection` against the worktree lock: 16 rows, 83 corruptions refused. `verify_scratch` appending v110 over that lock: passed, 71 inventory successors, 72 contract successors, 16 inheritance rows, v110 selected. `check_package_edges --lane host` against v110 passed. Security's resolved edges stay identity, platform and evaluator. There is no lifecycle edge.

## Replay

`cargo test --locked --offline -p opensip-security --lib namespace_lease`: 11 passed, 0 failed. `cargo clippy --locked --offline -p opensip-security --all-targets -- -D warnings` passed. `rustfmt --check --edition 2024` passed on `namespace_lease.rs`, `namespace_lease_tests.rs` and `first_registration.rs`. `ordinary_writer.rs` was one line off rustfmt at `0206ce8`; the new `namespace_lease` import is grouped with the file's existing unsorted uses, so the file's rustfmt delta is now an import reorder. `installation_read.rs` keeps the base file's rustfmt delta; the added hunks do not enlarge it. The workspace suite and workspace clippy were not replayed.

## Verdict

ACCEPT-UNIT. Inventory v110 is ACCEPT on v105. No required findings.
