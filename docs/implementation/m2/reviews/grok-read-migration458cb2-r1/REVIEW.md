# Review: installation-reader migration 458c-b2 and inventory v79

Grok is the single reviewer. Claude Opus 5.5 leads. No repository edits and no product cargo.

Worktree `/Users/sb/code/opensip-ai/opensip-458cb2` at `0ce4c72512bfd65684895f3d6b896daaabe5b7bb`. The sixteen uncommitted product files match hashes.txt. `product.diff` is 131777 bytes, sha256 `c37f3e1d583363889d6fcdff8a85cc0a5319cc0dc9793ddd5fafa047d95a3cf6`. `~/Library/Application Support/OpenSIP` is absent and is not a symlink. Law is 458c r5 items 5, 6, 8 and 9.

## Verdict

**ACCEPT-UNIT.**

`InstallationReadFence::acquire` is the production entry onto a complete observation. Captures charge the session ledger, return a value failure with the ledger still open, run the full recheck, and then latch. A budget refusal from a capture's own charge closes the ledger. Inventory v79 adds four rows and keeps every inherited row equal to v78.

## Item 8

`acquire` takes no groups. It runs the read platform, begins one observation session, and retains that session only when I is complete. `retain` observes, requires `complete()`, and builds `ReadSession` on that session's ledger, with the fence, the retained chain, the account, and the receipt. `ReadSession.groups` is empty, and `supplied_actor` returns the uid with that empty set, so every judgment is the owner's.

Host `installation_records`, `installation_selection`, `installation_lineage` and `installation_trust`, and storage `native_marker`, keep `&InstallationReadFence` and the `capture_leaf` / `capture_descendant` shape. Their sources are unchanged in this unit. The trust readers take `&dyn HeldFence`. `SuppliedInstallationFence` implements that view for supplied-root tests. `ReadSession` implements it for the observation path.

`NativeInstallationFence::try_acquire` remains on the old fence and is reached from that fence's tests. `SuppliedInstallationFence::try_acquire` remains inside the trust test modules (`native_census`, `native_current`, `native_platform`, `native_record_capture`). `NativeInstallationRoot::capture` remains for that old fence body and for supplied-root tests until 461. The production text of the listed readers calls the held-fence and read-fence API. The pin records `InstallationReadFence::acquire` as `fn() -> Result<InstallationReadFence, InstallationTermination>`. This review read those call sites and did not replay the pin under cargo.

`observe_bound_operational_file_with_policy` still calls `inspect_directory_path`. That consumer, with path binding, directory binding, `FileLock::observe_descriptor` and the macOS loader, stays with 461. Files under I keep `inspect_operational_file`. `Budget::charged` forwards `account` and `edge` onto the session ledger. `directory_record_capture.rs` and `directory_name_scan.rs` are unchanged and stay on that observer.

## Items 5 and 6

A capture opens only through the retained I. Each directory prefix is charged, opened, judged private, required to carry its exact name, and required to sit on H's filesystem. Each file is judged private, regular and capped, named, filesystem-checked, read, judged again, and reopened by name so the identity matches. `judge_directory` and `judge_file` use `capture_descriptor_acl_observed`. A missing file, a custody refusal, a name or filesystem mismatch, or an identity mismatch comes back as `Ok(Err)`, so the ledger stays open. `capture` then runs the full recheck and latches. The full recheck covers the receipt, the chain, `observation.required()` plus every file captured since, and the receipt again. When the capture and the recheck both fail, the capture stays the cause. A budget `Err` from the capture's own charge makes `step` latch and return before that recheck. That is the same budget rule accepted for 458c-b1.

There is one ledger, at 65536 objects, 131072 edges and 268435456 bytes. `Budget::charged` keeps those local caps and sends the trust readers' charges to the session sink. A limit failure is `WORK.BUDGET_EXHAUSTED` on `SYSTEM.OUTCOME.ILLEGAL_STATE`, fault `host-invariant`. `ObservationSession::begin` allocates one session per process. `retain` consumes it.

## Judgments

1. **Light held-fence check: ACCEPT.** Between full rechecks, `ReadSession::recheck_held` confirms the lock descriptor's name and that `lifecycle.fence` under the retained I is still the one-link regular file of the locked identity. `ProvisionalHeldFile::bytes`, `filesystem` and `contributing_filesystems` call `recheck_capture`, which checks that fence identity, each retained edge, and the file (private, identity, name, filesystem). `InstallationReadFence::recheck` is the full session recheck. It runs after every capture, on success and after a value failure. Fence mode and ACL, and the chain above I, belong to that full recheck. `consumption_rechecks_the_original_file_and_the_held_fence` fails `bytes()` on file mutations and catches a mode change of H or of `lifecycle.fence` on `InstallationReadFence::recheck`. The request's per-recheck edge counts were not measured here.

2. **Recheck scope and the budget bound: ACCEPT.** `ProvisionalHeldFile::recheck` covers the fence identity, the retained edges and the file. The full recheck after each capture reopens the observation's required files and every file this session has captured. Item 5 step 4 asks for that required-file limb. Trust and census captures charge through `Budget::charged` and are not pushed onto `ReadSession.captured`. `native_read_session` calls `fence.recheck()` once after the batch. `check_all` between samples uses `recheck_held`. Lineage calls `capture_descendant` once per node, so each node pays a full recheck. A chain that exhausts 131072 edges ends on the budget row and latches. That is item 6: a limit failure is unavailability, and there is no branch-local reset. `an_exhausted_session_ledger_refuses_on_the_budget_row_and_latches` refuses the next `capture_leaf` as `BudgetExhausted` and latches. `a_failed_capture_still_runs_the_full_recheck_and_stays_the_cause` returns `Incomplete` for a missing file after spending edges past the recheck. The request's admission, capture and recheck edge figures were not measured here.

3. **Latch after a value failure: ACCEPT.** A missing file is `Incomplete` as a value. Step 4 runs, then the session latches. A recheck failure leaves the latch set. On the value-failure path the earlier capture stays the cause, including when the recheck also fails. A budget refusal inside the capture closes the ledger and skips step 4.

4. **Empty supplied groups: ACCEPT.** `acquire` has no groups argument. The session's supplied set is empty. Judgments use the owner predicate.

5. **Private descendants, legacy file observer: ACCEPT.** Directories and files the read session opens are judged by `judge_directory`, `judge_file` and `judge_capture`. Trust captures keep `inspect_operational_file`, now charged on the session ledger. Retiring that observer is 461. Item 9 holds for the readers this unit moves: their root-to-H path is the held fence, and the omitted-ACL mapping at `check_descriptor_observation` stays with 461.

6. **Five stale descriptions: ACCEPT.** `installation_observation.rs`, `installation_session.rs`, `read_premise.rs`, `native_read_session.rs` and `installation_fence.rs` are byte-equal to v78. The successor leaves them on the inherited text. The README names each stale sentence and defers a description override to a later contract successor, as 468a did and as the `read_premise.rs` sentence was accepted in 458c-b1.

## Inventory v79

`repository-file-inventory.v79.json` is 310321 bytes, sha256 `baf79f6f655bde83a4622d6bd22c37e1294ff4a36646048ceef99f8f5e5a355f`. Parent v78 is `docs/implementation/m2/repository-file-inventory.v78.json`, 306749 bytes, sha256 `a01568e64f2d2eb20a3b15fac38827c8be8e2711dd097c2b03118696ee589988`. `successor.json` is 9639 bytes, sha256 `339df91e6b7ea15c0cea834a681fac60cb20e1762dfedfa1690f41def79e989a`. The subject manifest is 2078 bytes, sha256 `b94964db46ffe3c8595313e2f2fd23146a7ece520ef5a81353da377a4c942b84`. The README is 3584 bytes, sha256 `255ead0a11f89a99ec1e002c762922e2d38f21eeae4e0c4b2e09b6111c296e3b`.

Rows go from 741 to 745. Paths stay sorted and unique. The path set is v78 plus `installation_read.rs` (service, proposed, opensip-security), `installation_read_fixture.rs` (test), `installation_read_tests.rs` (test) and `installation_observation_tests.rs` (test). Every inherited row equals its v78 value. Packages and pending decisions are unchanged. Standing is retitled to the installation-reader migration layout and keeps the same non-qualification sentence. The successor records `inheritedRowsEqualByValue`, `packageDependencyGraphUnchanged` and `pendingDecisionsInheritedUnchanged`, and its parent pin is v78.

The eight path-bound overrides are unchanged: `apps/cli/src/bootstrap.rs`, `apps/report/package.json`, `crates/host/src/installation_lineage.rs`, `crates/identity/src/store_lineage.rs`, `crates/security/src/initial_installation.rs`, `crates/security/src/private_access.rs`, `package.json` and `schemas/sources/imported-v1.schema.json`. The last four selectors move with the four inserted rows. The helper is `c890b35f281bef71bc876088caae13886a6057c71717250348ee008e2612dfda`, 2917 bytes. Re-running `verify_projection.py` with `python3 -I -B` against the architecture tree and `/Users/sb/code/opensip-ai/opensip/design-lock.json` printed 8 rows, PASS, 43 corruptions. `verification.stdout` is the 124-byte record, sha256 `dcf19ff444814b39edde13a1ab14b27f92ef670656e4ef42ed1ad70a7b577eea`.

The lead reported the workspace sum 1123/0 on two runs, the migrated readers at 30/30, clippy and fmt clean, `check_package_edges --lane host`, and `verify_scratch` with v79. This review did not replay cargo.

## Required findings

None.
