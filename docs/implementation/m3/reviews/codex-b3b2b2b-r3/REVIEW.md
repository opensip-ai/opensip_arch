# B3-B2B2B-r3 review

**Verdict: REQUIRED-FINDINGS.** Two P2 accounting findings remain.

Manifest: 48,640 bytes, SHA-256 `9cf1081d5d4b13ddf583e84f2aa110730c94183cf772fe672f9aa7ee46c03c38`. All 194 members rehashed successfully. All 21 product-map candidate/archive rows and mapped parents, authority pins and the product-lock pin match. Product main is clean at `92624ae00f242d9a56e4305146e1d69665e2ecc5`; candidate HEAD matches that base; architecture HEAD is `271d7eee4759799e9a731c34ff1d2517f2862727`.

## Prior findings first

- **R2 RF-1, the initial trial crossing index-only boundaries: resolved.** The trial, phase_two and re-walk are removed. Branch A uses A4's gate and member decisions before its one member/gitlink-aware walk. Links follow an accepted walk. The bound r4 reference supplies the new priority rather than an unmodeled exception.
- **R2 RF-2, unbound reopened ancestors/Git evidence: functionally resolved.** The identity list includes the opened path chain and the present .git/config/index evidence with the correct W-relative labels. Native member_verdict compares every reported identity before returning either ordinary verdict. The independent preserved-M, preserved-.git and ancestor replacements address the earlier blind spots. The new list's storage accounting is not resolved; see R3 RF-2.
- **R2 RF-3, a manifest usable only once: functionally resolved.** The validated-read cache supports repeated provider requests and charges for returned copies. The copy charge is currently ordered after allocation; see R3 RF-1.

## B3B2B2B-R3-RF-1 — Charge a cached read copy before cloning its buffer (P2)

Locations: `crates/security/src/custody/workspace_observation.rs:540-547`.

The cache-hit path executes kept.clone() before work.charge(owned(raw.len())). FileBytes::Read owns a Vec, so this allocates and copies up to 4 MiB before asking whether the original discovery ledger can fund the copy. With less remaining byte/object budget than the copy needs, the operation performs that storage work and only then returns Budget. The first cache insertion charges before its clone; the repeated-read path must preserve the same ordering. The repeated-manifest vectors show functional reuse, but do not establish the charge-before-allocation requirement.

**Required change:** Inspect the borrowed cached outcome, charge the complete copy cost on the original ledger first, and only then clone it. Preserve non-latching ordinary outcomes and the existing validated-byte semantics.

**Validation:** Add a focused exhausted/insufficient-budget control for a repeated validated read, showing that the cache copy is not performed when its charge refuses. Keep the existing repeated-provider composition vectors and add a mutation or equivalent observation that distinguishes charge-before-copy from charge-after-copy.

## B3B2B2B-R3-RF-2 — Account the new identity collector storage before constructing it (P2)

Locations: `crates/security/src/custody/git_tracking.rs:1363-1388`, `crates/security/src/custody/git_tracking.rs:1453-1456`, `crates/security/src/custody/git_tracking.rs:1478-1491`.

The new MemberIdentities collector constructs an owned prefix path and appends a metadata record for every opened directory, then constructs additional Git-object labels and records, without charging that additional retained storage. Reusing an already charged native status sample does not pay for these new path buffers or Vec growth. STATUS is explicitly a status-read cost (objects 0, edges 1, bytes 512); it is not a path-length-dependent owned-record allowance. A deep member adds the sum of all prefix lengths, not just the member spelling once. Most ancestor/M bindings already exist, so the later native bind calls usually charge nothing; even a newly charged binding pays for another map record after the identity list already exists. Moreover, observe now calls observe_identified and discards the list, adding this allocation work to the legacy path despite the unchanged-charge claim. This is a runtime-accounting issue, separate from the later census upper-bound derivation.

**Required change:** Fund the identity list slots, owned path bytes and their growth before constructing them, or replace the collector with an explicitly accounted/borrowed mechanism that checks identities at the owning boundary. Preserve the legacy observe/observe_members charge contract by making identity collection opt-in if necessary; do not preserve a charge-equality test by leaving new work uncharged. Update the no-new-charge claim and any affected evidence.

**Validation:** Add deep/shared-path identity accounting controls and an insufficient-budget control demonstrating refusal before the new owned records are allocated. Preserve the independent ancestor, member and Git-evidence identity mutations and the existing legacy observe/observe_members verdict-and-charge checks.

## Other requested judgments

The core restructure matches r4's branch-A order: the 4,096-root size check precedes global grammar; gate paths stay raw and gate details are source-specific. The no-members walk supplies provenance without replacing the chosen gate verdict. Placement/volume rules precede the member cap; directory custody and item 6b then short-circuit together in candidate order. Admitted carries the member/gitlink inputs and pre-link declaration rows. A walk refusal clears member and member-config provenance; only acceptance reaches links. LD-12 correctly prevents provider reads following a walk refusal. D9 and path spelling remain consistent with the accepted reference.

The vector changes are appropriate. walk pins the members, gitlinks and status at the branch-A walk seam; sixB pins the actual reference consultation set. forbiddenReads preserves a read prohibition without incorrectly forbidding the reference's permitted placement metadata lookups; forbidden remains the stronger lookup/read/listing exclusion. The tripwire is properly scoped to candidate custody/6b, as A4 allows earlier placement. LD-14's two non-string arrays are explicitly listed and excluded because the product input types admit only strings; this is a transparent representational exclusion, not a claim those reference inputs ran natively.

The composition controls materially resolve the earlier gaps:

- The walker's own trace rejects listing a gitlink, opening below it or deeper observations, rather than inferring non-entry solely from the final record.
- check_gate and the gate cases exclude candidate decisions; the member vectors additionally cover exact consultation behavior.
- The paired unlistable-subtree control shows that a real walk failure appears when the index boundary is removed.
- changed_before_admission requires the last core request to be item 6b's verdict and no walker listing, preventing later observers from masking a missing identity comparison.
- The independent ancestor, member and Git-evidence mutations distinguish those comparisons. The member-configuration refusal vectors make clearing memberConfigs observable (LD-16).
- The repeated-provider vectors cover two patch sources and a name-mismatch disposition in both branches.

The remaining required controls concern the new accounting paths, not a missing A4 boundary/priority case. Ordinary custody outcomes remain values outside charged operation errors; retained reads use their custody-captured descriptor and postcheck full status plus normalized ACL before exposing bytes. The internal pending provenance remains an acceptable non-emittable partial behind the complete V3 serializer. The binding table remains shared through the member decision, walk and branch-A links.

Read-only comparison independently confirms that both census JSON files differ from base only in bytes/SHA fields at closure indices 0, 4 and 6. The scenario still uses the operation's own precondition, the lent root's omission premise and home-filesystem predicate, trust groups, and its empty environment/system-source inputs. No later margin or qualification gate is claimed closed.

## Checks and evidence

Freshly ran only the three permitted checks, all passing:

- Operability source: 114 rows, no findings.
- workspace_discovery_vectors.py --check against bound B3-b0 r4.
- workspace_member_vectors.py --check against bound B3-b0 r4.

The pinned final lane records 14 equal base/candidate failures and eleven new passes. Library passes increase 1,145 to 1,156, with five ignored at each subject; adding six documentation tests gives totals 1,151 to 1,162. This is equal-failure-set evidence, not a green full suite. The composition run has eleven passes, the focused discovery/member run ninety, and host discovery_flag_tests seven. Both warning-denied Clippy configurations, formatting, all vector checks, census controls/check, operability, environment checks and verify_design are recorded passing. All thirty mutation logs show successful compilation and failing tests, and controls.json records all caught.

Attempt 1 retains its Clippy/formatting failures and three mutation survivors. Attempt 2 retains the remaining member-identity survivor and a formatting failure. The final lane records all checks passing; the new independently preserved-.git case explains why the final-M comparison is now observable.

**B3B2B2B-R3-NBO-1 — The second lane attempt also failed formatting.** SCOPE says the second attempt failed only on the member-identity mutation survivor, but attempt2/checks.json also records rustfmt-edited exit 1. The final attempt records both formatting and mutations passing, so this history wording does not block the final checks; align the description when refreshing the package.

No Cargo, rustc, tests, builds, lane or census tool was run in this review. No network, other panes or delegation was used. No private fixture, installation directory, signing key, held tree or T2 held-out entry/store/overlay was read. The accounting findings are source-derived; no new budget experiment was executed. B3-b2b2c's T2/joint controls, B3-b3a/b/c's bound and margins, J1 and qualification remain separate. Only REVIEW.md and review.json in the requested directory were written; neither repository, worktree nor any control file was edited.
