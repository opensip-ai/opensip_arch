# Review: observation session 458c-b1 r2 and inventory v78

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review of the observation session after r1 RF-1. No repository edits and no product cargo.

Worktree `/Users/sb/code/opensip-ai/opensip-458cb` at `42ffa91d57baf6de85ab8c9003631a3cb5e2d02d`. The ten uncommitted product files match hashes.txt, including `product.diff` (77367 bytes, sha256 `725fe0295d242fd105c8f56c1b2b09f27eafef3b02f9573ddde16b6825a465c5`). `~/Library/Application Support/OpenSIP` is absent and is not a symlink. Law is 458c r5 items 5, 6, 7 (the non-doctor part) and 11. Item 8 stays in 458c-b2.

## Verdict

**ACCEPT-UNIT.**

r1 RF-1 is closed. A native ACL-capture failure in step 3 stays a value, the ledger stays open, and step 4 still runs. The write gate still uses the latching capture. Inventory v78 and `successor.json` are the r1 bytes.

## RF-1

`capture_descriptor_acl_observed` charges `descriptor_acl_capture_cost()` and then calls `capture_with` (macOS) or `capture_native`. A native `Err` is returned as `Ok(Err)`. A budget refusal from that charge is `Err` and closes the ledger.

`Reader::member` uses that function. It stores `Io(Capture)` and a custody refusal from `judge_capture` as values and returns `Ok(None)`. `read_members` therefore returns the `Members` value, and `observe` reaches step 4. When the member failure and the recheck both fail, the member failure is the one returned, and `RecheckRefused` records that the recheck ran. The session only calls `capture_descriptor_acl_observed`. `judge_private_file` still calls `capture_descriptor_acl_accounted`, and step 4's reopen goes through that latching path, so a capture failure during the recheck still closes the scope.

`judge_capture` is the shared ACL judgment. The gate wraps its `GateRefusal` in `WorkFailure::Operation` after the latching capture, which is the same custody return `judge_private_file` had. `lock_fence` is still one `try_acquire`.

`a_failed_member_capture_still_runs_step_4_and_stays_the_cause` removes `project-registry.v2`, charges a real capture of `selection.pair`, then substitutes `Malformed`. At `Step::Recheck` it sets `OpenSIP` to `0755`. `directory_custody` on that parent requires mode `0700`, so the recheck returns an error. The steps are Fenced, Reads, Recheck, RecheckRefused. The result is `Io(Capture)` for `selection.pair`, the session is latched, and the fence is free. `session_refusal` still sends that `Malformed` through `gate_refusal` to custody subject `private`.

The lead reported the workspace sum 1120/0 on two runs, the session at 14/14, the gate at 11/11, clippy and fmt clean, `check_package_edges`, and `verify_scratch`. This review did not replay cargo.

## Inventory v78

`repository-file-inventory.v78.json` is 306749 bytes, sha256 `a01568e64f2d2eb20a3b15fac38827c8be8e2711dd097c2b03118696ee589988`. Parent v77 is 304222 bytes, sha256 `642dc4bba855112b9fac2d54079d137c6bed9237cf5b574a5aed09bf22f13ff1`. `successor.json` is 9517 bytes, sha256 `0f35249840e8e05e12b85ede6c473df19b08613515f2c5feee9f8425cbec6acf`. Those two files match the r1 review.

The subject manifest is 2096 bytes, sha256 `9f480577e7a5cfd409c9f40ac348f24c6408cfb15f93543b904cc44630a802d2`. The README is 2586 bytes, sha256 `1ca6641a6c09a5ae58723fef844f2969a08ebfbd13fa3e7063082be3cba6b615`. It names `descriptor_acl_capture.rs`, `filesystem.rs`, and `lib.rs`. The inherited descriptions of those rows still hold: the capture row describes the sample, and the filesystem and lib rows describe the public surface. `read_premise.rs` remains the disclosed stale inherited sentence, deferred to a later contract successor.

Rows stay 741. The only additions are the two session sources. Every inherited row is the r1 value. Packages and pending decisions are unchanged. The eight path-bound overrides and the helper (`c890b35f281bef71bc876088caae13886a6057c71717250348ee008e2612dfda`, 2917 bytes) are unchanged. Re-running `verify_projection.py` with `python3 -I -B` against the architecture tree and `/Users/sb/code/opensip-ai/opensip/design-lock.json` printed 8 rows, PASS, 43 corruptions. `verification.stdout` remains the 124-byte record, sha256 `dcf19ff444814b39edde13a1ab14b27f92ef670656e4ef42ed1ad70a7b577eea`.

## Required findings

None.
