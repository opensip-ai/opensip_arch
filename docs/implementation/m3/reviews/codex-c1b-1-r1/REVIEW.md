# C1B-1-r1 review

**Verdict: REQUIRED-FINDINGS.** One required finding, no non-blocking observations.

Subject manifest: `70edd99be8cc9f43ea11d3e643c5a7b0cd777460175d11fcbc29630ddbec7c6f` (15,535 bytes, 67 members).

## C1B1-R1-RF-1 — Remove or charge repository-proof construction allocations (P2)

`crates/security/src/custody/git_tracking.rs:1611-1616` constructs a `Vec<&[u8]>` and, for every candidate ancestor, two owned labels through nested `label` calls. `SnapshotRoot::from_operation` calls this helper without a `WorkScope`. These allocations reconstruct information from X2's existing evidence; they are new work, not allocations already paid for when X2 collected that evidence. A root below its repository causes repeated prefix allocations before the correct ancestor is found.

The submitted VCS model and envelope do not account for these allocations. The exact-charge test also misses them: `Observed::vcs` constructs `self.subject()` and its `SnapshotRoot` before constructing the ledger (`snapshot_vcs_tests.rs:166-179`). Consequently, all nine charge comparisons can pass while the production lending does additional uncharged work. The unit's complete-term requirement and shared-ledger accounting are not discharged by charging only after this preparation.

Derive the repository proof from borrowed labels and spelling slices without heap allocations, or charge the allocations before they occur on the caller's shared ledger, preserve typed budget failures, and extend the model and derivation. An allocation-free proof constructor is sufficient; no cap increase is requested. Preserve identity binding and innermost selection. Cover deeply nested selection and nested repositories, and extend the allocation/source control to include proof construction. If allocations remain, add exact-charge and one-unit-short budget controls for this path.

## Requested rulings

**Q1:** Accepted. Existing S3 configuration-file custody may refuse a stable file larger than 4 MiB before any read, using head-custody, loose-ref-custody or packed-refs-custody. Exactly 4 MiB is read subject to the shared budget and then parsed. The corresponding oversized reason remains for growth after judgment. This is an explicit adjustment to the plan control, not a larger cap or permission to bypass custody.

**Q2:** The separate complete VCS derivation suffices for this unit under the accepted r9 conditional-margin regime; adding the worst-case envelope to every per-entry census row is not required. The row model must continue to identify what it actually prices. All non-row work, including VCS and any charged proof construction, shares the same remaining margin. RF-1 must be resolved before the complete-term claim is accepted. The batch refresh still requires its pre-run review, frozen final input bindings, current receipt bindings and post-run review; unchanged stale receipts establish no renewed margin or product qualification.

## Verified subject and implementation

Independently rehashed all 67 manifest members, all 14 source authority pins, the recorded product lock, all 13 worktree/archive candidates and all 10 existing parent files. The candidate remains detached at `1749259df87b3c8cdb24d909264a80f52d2c9f4a`; its changed/untracked paths match the 13-file map. Both base-dirty files retain their entire base prefixes. The architecture checkout has advanced beyond the recorded architecture base; this review binds the exact manifest and authority bytes, not an assumption that the live checkout HEAD is that base.

Taking the subject in `snapshot_source.rs` is acceptable: it still uses the operation's own subject, tracking observation and retained chain. The proof checks chain identity and searches innermost first. W comes from the `NoRepository` proof's own chain. RF-1 concerns allocation accounting, not these provenance checks.

The Git resolver implements detached HEAD, one symbolic level, loose-before-packed resolution, unborn refusal, full packed-file validation with strict ascending names and peel adjacency, and the stated UTF-8 ref-name restriction. The ascending-order and UTF-8 restrictions are conservative supported-subset choices. Long target-directory errors are classified before link/non-directory handling; nonregular files retain their separate file refusal. Custody and home-volume checks precede content reads; the enclosing .git metadata is compared with X2's sample. Member reach uses borrowed segments and charged marker checks, and checks devices. Unsupported reasons preserve their member projection and budget failures stay typed. The selected-root, member-count and subject preconditions are enforced. Record-length formulas match the canonical encoding controls, including escaped paths and the maximum 1,573,798-byte record.

The read/reach model follows the implemented charge sites, with nine native prediction cases and two multibyte reach pricing controls. The unbuildable 16-by-255 four-byte-name shape is explicitly a pricing control, while the 256-segment shape is exercised natively. Independently reproduced D*=226 and model H*=1,363,957. At the plan coordinates, the submitted VCS term is (173,706 objects, 2,164,854 edges, 1,577,723,559 bytes), within the plan's term in each component. The larger H* is explained by omitted target copying and post-custody status reads that the implementation does not perform. These arithmetic checks do not cure RF-1. D*/H* remain evidence coordinates; the 4 MiB read ceiling and shared-ledger exhaustion remain distinct bounds.

All five regenerated existing JSON outputs differ from their base versions only in pin fields. The closure change is exactly `git_tracking.rs`. Independently ran the permitted receipt-specific checker: both receipt byte strings equal their accepted refresh baseline; the existing batch delta is C1b-0 plus C1c-0; C1b-1's own deltas and their cumulative unions match the declared sets. Each receipt's ten held-out rows remain stale and its margin outstanding. No held-out contents or cache were inspected.

## Validation and limits

Independently ran only the four permitted checks: model `--check`, operability source census, VCS derivation and receipt-specific checker. All passed; operability reports 114 rows and no findings. The receipt checker temporarily used REVIEW.md as its permitted output; this final review replaces that temporary content.

Inspected the pinned lane evidence rather than rerunning Rust or cache-dependent checks. Security rises from 1,248 to 1,270 passing tests with the same 14 failures; host remains 412 passes with the same eight failures. Focused VCS tests show 22 passes and focused tracking/source tests 41 passes. All 11 mutations have actual focused-test failures, rather than compilation failures alone. Recorded warning-denied all-targets Clippy, scoped rustfmt, append-only checks, three census checks, FW-01, environment exceptions, operability and verify_design pass. Existing walk/opener/session predictions remain unchanged. No new production mint-census call, environment read or `let _ =` was found in the added implementation.

The three new paths still need the separately reviewed inventory successor. Sealing/schema integration, J2's route, the combined batch refresh and product qualification remain outside this unit. No repository, worktree or control file was edited; no build, lane, network operation or delegation was performed.
