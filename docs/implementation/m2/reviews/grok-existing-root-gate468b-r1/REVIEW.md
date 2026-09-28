# Review: durable write gate 468b and inventory 75

Grok is the single reviewer. Claude Opus 5.5 leads. Review of the write gate after creation and inventory v75, against law 468 r5 items 2 to 6. No repository edits.

Product worktree `/Users/sb/code/opensip-ai/opensip-468b` at `f482f986adc321f3feb248bf927dcc6cdbeba345`. The five product files match `hashes.txt`. `product.diff` is that diff (60004 bytes, sha256 `12894daba3233e44656338a1d0382f81acc6e50be5b2363911364378659a1584`). The subject manifest matches `existing-root-gate-inventory-v75-subject.json` (1902 bytes, sha256 `970f734502df9b532ccb5c3248f27b0d887c395c6084a0859b0b4c88da22d08f`).

## Verdict

**ACCEPT-UNIT.**

## Gate

`DurableBarrierQualification` is sealed. Only `InitialPlatform` implements it, and it lends `barrier_policy`, `is_home_filesystem`, and `omission_premise`. `admit` takes that qualification and nothing from the creator. The test pins that function type. `NativeInstallationFence::try_acquire` is not called. The lock is one nonblocking `FileLock::try_acquire` on the descriptor opened no-follow through the retained I.

`DurableWriteGate::begin` takes the process flag and a ledger at 65536 objects, 131072 edges and 256 MiB. `admit` latches before the steps, so success, `Busy`, and every refusal leave the gate closed. A second `begin` in the process is refused.

Step 0 checks the account with `admit_account`, then `observe_parent` with `OpenSipJudgment::Private`. The premise reaches the root-to-H prefix, `Library`, and `Application Support` through `judge_ancestor`. `OpenSIP` is judged private inside that walk, and I is opened through the retained `OpenSIP` and judged private. H, `OpenSIP`, and I are checked against the platform's home filesystem. A missing final name is `Absent`.

Step 1 opens `lifecycle.fence` through I, judges it private, checks the name, and takes the lock. `Busy` returns before any recheck or barrier.

Step 2 rechecks the account, every retained name, the chain under the same premise, `OpenSIP` and I as private, I's identity through the parent, the three filesystem samples, the locked fence by identity, link count, type and name, and the required files. Those files are the fence, `project-registry.v2`, `selection.pair`, the endpoint marker, the node chain from `relative_components`, and `trust/stores/S/state.v1`. The pair, marker, and nodes are decoded to find the next path. A missing or undecodable file, or a broken node chain, is `Incomplete`.

Steps 3 to 5 are one effect. It reserves both barrier costs and twice the measured step 2 cost before either barrier. I's barrier runs, then the parent barrier on the retained `OpenSIP` handle. A failed step 3 skips step 4. Step 5 still runs, and a barrier failure remains the reported cause. Each live receipt is checked with `is_for` on that handle, and apfs accepts `FullFlush` or the primitive's `Fsync`. `DurableInstallation` holds the lock, the chain, the files, and both barrier kinds. It is private and not `Clone`.

The eleven tests use a scratch H from `test_scratch::temp_dir()` and `HomeSource::Fixture`. They cover the success order, a busy lock, recheck refusals before and after the barriers, a replaced file, a failed barrier with the second recheck still running, a short ledger, one gate per process, an omitted ACL at component 0 only when the premise is absent, an omitted ACL on `OpenSIP` or I refused with a premise, and a 48-deep home kept under half of each cap. `~/Library/Application Support/OpenSIP` is absent.

## Inventory v75

v75 is v74 plus `installation_admission.rs` (`service`) and `installation_admission_tests.rs` (`test`): 731 rows become 733, sorted, with nothing removed and no inherited row changed. The eight projection rows are the five carried overrides plus `store_lineage.rs`, `initial_installation.rs`, and `private_access.rs`. Each parent selector matches v74. The helper is the v74 checker with the row count set to 8. Its recorded run is 8 projection rows, PASS, and 43 corruptions refused.
