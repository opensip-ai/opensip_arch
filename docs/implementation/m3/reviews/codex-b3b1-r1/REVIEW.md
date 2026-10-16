# B3-B1 r1 review

Verdict: **REQUIRED-FINDINGS**.

Subject: `545c8ec8af428a7d1a3b4a7e87e038a5ad106c9005b84925899661a8b0243594` (6,307-byte manifest). All 27 members rehash correctly. Both product-map candidate files match their archived bytes and the worktree; the existing file's parent matches the exact product base. Source authority and design-lock pins also match. Product main is clean at `2b297e68e07aeae31a3fe71b6fb227f9758dcc5a`; the detached candidate is at that base with exactly the two advertised source changes. Architecture HEAD matches `67b8f8bcaa6e25804a61b56693a87b6b39da311e`.

## Required findings

### B3B1-R1-RF-1 — P1: Native ACL capture refusals still latch the shared ledger

Locations: candidate `git_tracking.rs:851-872`, `project_chain.rs:635-637`, platform `filesystem/descriptor_acl_capture.rs:192-201`, and `work_ledger.rs:278-300`.

`config_decided`, the environment decision and the index decode correctly move their ordinary refusal decisions outside charged scopes. The custody path still calls `judge_project_object`, directly for `.git` and through `judge_file` for configuration and index. That judge calls `capture_descriptor_acl_accounted`. On macOS its `capture_accounted_in` executes `capture_with(...).map_err(WorkFailure::Operation)` inside `work.run`.

A native `DescriptorAclCaptureError::Changed`, `Malformed` or `Unsupported` therefore closes the ledger. These are not host-I/O errors: `chain_failure` maps them to the appropriate `VcsUnsupported` custody subject, and `member_failure`/`observe_members` catch them as ordinary member refusals. Catching the error does not reopen the ledger. With a second valid member, its next charge fails `Budget(Closed)`; with a lone refused member, an enclosing `ledger.scope` converts the apparent successful verdict vector to `Budget(Closed)` at scope completion. The corresponding global-source capture can similarly prevent LD-1's all-members refusal vector from escaping successfully.

This is a source-traced failure, not a test run by this reviewer. It follows directly from the capture helper, error translation and ledger guard. Existing 0664 index and 0777 `.git` controls exercise successful native captures followed by pure custody refusals; they do not cover a native capture failure. The configuration-latch mutation proves only the configuration path.

Required: use a 6b-specific custody/capture path with the same charges and subjects, carrying ordinary capture failures as values until outside the charged scopes. The platform already exposes an observed capture variant, although the ownership/custody composition still needs a proper implementation. Keep 6a's existing behavior unchanged; host I/O and actual budget failures must still fail the pass. Add deterministic capture-failure controls for a refused first member followed by an admitted member, a lone refusal, and a pass-level source; assert both the original refusal and successful enclosing ledger completion.

### B3B1-R1-RF-2 — P1: The NoRepository proof is transferable to an unrelated root

Locations: candidate `git_tracking.rs:1037-1040` and `1107-1139`.

`NoRepository` borrows only a `TrackingObservation`. The observation holds the tracking enum and evidence samples; it does not bind the proof to a retained W. `observe_members` ignores `_root` and instead obtains W from the independently supplied `TrackingInputs.chain`. No identity check relates them.

A caller can observe a non-repository W_A, obtain its token, then call `observe_members` with that token and a retained chain for W_B inside a repository. All lifetimes may coexist. Environment/global/system checks do not establish W_B's W2 status, and the member walk starts below W_B, so a conventional W_B/m can be admitted. The signature thus requires evidence that some root had NoRepository, rather than item 21's precondition for the W actually used.

Required: bind the proof to the exact observed root/chain and derive the member root from that proof, or reject mismatched inputs using the retained binding before member work. Add a cross-root substitution control. The existing `w_inside_a_repository_gives_no_precondition` test and its mutation do not cover substitution: they only verify the enum predicate on the same observation. A caller convention is insufficient for the claimed type-enforced precondition.

## Other requested rulings

The 6a refactor is mechanically faithful on inspection. `repository` invokes the extracted layout with the original `config`, then performs the same index charge, marker-path derivation, decode and marker match. The missing-index return is equivalent. Global and system sources also receive the original configuration function. Native call order, sample order, charges and refusal mappings in those existing paths are preserved; this does not imply 6b can reuse every helper without accounting for continuation, as RF-1 shows.

The member path uses retained no-follow directory opens and device comparisons, with positive VCS-marker checks at intermediate directories and M. Layout reuses 6a's closed Git configuration/index rules and returns decoded gitlinks. I found no added read of HEAD, refs, packed-refs or shared-index bytes. Positive absence probes of commondir/config.worktree are the explicitly required layout checks, not reads of those files. The implementation adds no member write or fenced recheck evidence; temporary sample vectors are discarded.

LD-1's pass-level refusal policy is appropriate because unsupported effective configuration excludes every affected member, while branch-B handling must remain disclosure. Its implementation remains subject to RF-1. LD-2's distinction between host I/O/budget failures and ordinary unsupported-member verdicts is appropriate. LD-3's `evidence-changed` for a now-absent, linked or non-directory placement component, or a new intervening `.git`, is reasonable. LD-4's synthetic device mismatch exercises the comparison without claiming a mounted-volume integration test. LD-5 correctly preserves 6a's decoder verdict: a real split index can fail `index-malformed` before reaching the `link` extension, and need not be relabeled. Item 23's no-owner-waiver rule is retained by the Git-object judgments. The caller-owned placement, ordering, disjointness and 64/65 cap remain B3-b2 integration obligations; this library unit has no product caller yet.

## Controls and evidence

The seven tests represent the item-21 fixture list: conventional layout, `.git` file, configuration exclusions, commondir, split index, gitlink extraction, intervening `.hg`, repository-root precondition, synthetic device mismatch and 64 members. The 65-member cap is expressly deferred to B3-b2 before observation. The mixed-refusal capture and cross-root cases above are missing.

I parsed the archived base and candidate logs: both have the same 14 failing test names; aggregate passes rise from 1,128 to 1,135 across two suites. The suite is therefore not fully green, but the reported failure-set comparison is accurate. The focused log reports 30 passing git_tracking tests. Archived warning-denied all-target Clippy, environment, census and verify_design evidence reports success. These were inspected, not rerun. The census closure excludes git_tracking.rs; its unchanged receipt is not a bound for the future member producer.

The eight archived mutation logs show behavioral test failures rather than compilation failures, at assertions relevant to the device check, marker checks, configuration latch, gitlinks, environment, precondition predicate and volume subject. They are meaningful controls, but not proofs against the two findings.

**B3B1-R1-NBO-1:** controls.json claims nine caught mutations and the runner includes `linked-worktree-dropped`, but that mutation's log is absent from both the archived directory and the manifest. Archive it in the next evidence package. The ordinary commondir control and mutation recipe remain inspectable, so this is an evidence-completeness observation rather than a separate blocking code defect.

The only executable check run by this reviewer was the expressly permitted operability source census in the candidate worktree: `passed: true`, 114 rows, no findings. No Cargo, rustc, test, build, lane, census or network command was run. No private fixture, installation directory, signing key, held tree or T2 held-out entry was read. No panes or delegation were used. Neither repository, the worktree nor control files were edited; only REVIEW.md and review.json were written in the requested directory.
