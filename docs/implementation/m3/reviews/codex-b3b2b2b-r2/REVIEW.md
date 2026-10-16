# B3-B2B2B-r2 review

**Verdict: REQUIRED-FINDINGS.** Three required findings remain.

Manifest: `9bcfdf22d792e7135aeef8ba99b8a08668e857e1fcf2c4a7332385188ef14bb2`, 16,804 bytes. All 69 members rehashed successfully. All 18 product-map rows match candidate/archive bytes and their mapped parents. Source authority pins and the product-lock pin match. Product main is clean at `d47f9892d5709a1e108c4ecf9a9f60ed7aae12b2`; candidate HEAD is the same base; architecture HEAD is `5c581b5c5a4e22ff3fa28d5e9f522df92a27c4a0`.

## Round-one findings first

| Round-one finding | Assessment |
| --- | --- |
| RF-1, discarded gitlinks | Partly resolved. Item 6b now returns them, links below them are suppressed, and the final walk/scan record them as nested repositories. The first branch-A trial still crosses them and can return an incorrect earlier refusal; see R2 RF-1. |
| RF-2, stack/custody object mismatch | Resolved for the reported native-observation path. All stack opens establish a binding; later observations compare it, and custody captures the bound descriptor. |
| RF-3, cross-observer identity loss | Partly resolved. The shared table spans phases and walks and compares final member identities. Item 6b still reopens ancestors without consulting it; see R2 RF-2. |
| RF-4, fresh descriptor/stale custody on reads | Resolved for a single read. The captured descriptor is retained, the read outcome stays provisional, and full status plus normalized ACL are compared after the read. Repeated use has a new functional regression; see R2 RF-3. |

## B3B2B2B-R2-RF-1 — The first branch-A trial still crosses index-only repository boundaries (P1)

Locations: `crates/security/src/custody/workspace_discovery.rs:171-187`, `crates/security/src/custody/workspace_discovery.rs:254-269`, `crates/security/src/custody/discovery_walk.rs:1047-1110`.

R1 RF-1 is only partly resolved. The final walk receives admitted gitlinks, but the initial branch-A trial always receives an empty gitlink set. That trial can already enter and list an index-only nested repository, and any refusal or native error from that traversal returns before item 6b discovers the boundary. For example, use a valid member repos/a, an index gitlink sub with no physical sub/.git, and array root repos/a/sub/x. Make x world-writable. The first trial traverses sub and custody-refuses x; phase_two immediately returns TrialRefused, so the gitlink-aware re-walk never occurs. With the nested-repository boundary present, the required result is JOIN_CROSSES_NESTED_REPOSITORY before custody below that boundary. Similarly, selecting repos/a itself can cause an invalid listed name or I/O failure inside sub to abort discovery even though that subtree must stay outside the walk. The five new cases use benign interiors and do not expose this. LD-10 also explicitly discloses a second precedence divergence when another member refuses before the gitlink-aware re-walk. A later corrected record cannot undo observations the first trial was forbidden to make.

**Required change:** Resolve the gitlink/trial ordering so no trial descent or result is authorized by a provisional assumption that index-only boundaries do not exist. Preserve the accepted cap and short-circuit requirements; if their reconciliation requires changing the accepted plan or reference, resolve and bind that authority explicitly rather than declaring the mixed case unmodeled. A re-walk after an already completed unrestricted trial is insufficient.

**Validation:** Add both array-source controls for a join through a gitlink whose descendant fails custody, and for a selected member root whose gitlink subtree would fail listing. Assert the boundary result and that the first walk never enters the gitlink interior. Add the mixed gitlink-crossing/other-member-refusal case and bind its precedence to the accepted authority.

## B3B2B2B-R2-RF-2 — Item 6b does not bind its reopened ancestors to the custody-judged chain (P1)

Locations: `crates/security/src/custody/git_tracking.rs:1369-1381`, `crates/security/src/custody/git_tracking.rs:1420-1464`, `crates/security/src/custody/workspace_observation.rs:599-610`.

R1 RF-3 is only partly resolved. observe_identified returns the final member directory sample, overwriting sampled on each path component; NativeObservation binds only candidate. The session independently opens and samples every ancestor but never compares those objects to Bindings. A branch-A counterexample preserves the member inode: after phase-two custody of repos and repos/a, at before-verdict, rename repos to an aside, create a replacement repos directory with mode 0777, and move the original a directory into the replacement. Item 6b now traverses the new, unjudged repos, checks only its device and VCS-marker absence, and admits the original a inode. The final-member bind succeeds. With no gitlinks the accepted trial is reused, so no later bound walk observes the replacement ancestor. Discovery can therefore accept despite traversing a parent different from the one whose custody passed. The existing replacement controls replace the member inode as well and consequently miss this case. The session likewise does not share the table for its independently opened .git evidence.

**Required change:** Bind or compare the actual directory chain used by item 6b, not only its final member sample. Use the shared identity checks at the corresponding opens, or pass the already bound retained chain into the session. Preserve the existing unbound observe/observe_members behavior and charges where required. Include the Git objects already observed by placement/walking in the promised cross-observer identity consistency.

**Validation:** Add a branch-A before-verdict control that replaces an ancestor while moving the original member into it, preserving the member inode, with the new ancestor failing custody. Require a change before admission. Also control replacement of a previously bound .git directory while preserving M, and mutate ancestor/evidence comparisons independently of the final-M comparison.

## B3B2B2B-R2-RF-3 — A provider manifest can be read only once per phase (P2)

Locations: `crates/security/src/custody/workspace_observation.rs:460-472`, `crates/security/src/custody/workspace_observation.rs:535-550`, `crates/security/src/custody/workspace_declarations.rs:1066-1068`, `crates/security/src/custody/workspace_declarations.rs:1158-1165`.

bytes removes the retained descriptor from files. A subsequent custody_entry for the same path returns the cached custodied entry and does not restore the descriptor, so the second bytes call fails with Invariant("bytes-without-descriptor"). The accepted decision core legitimately calls manifest for each declaration entry before deduplicating links. For example, two Cargo patch sources can both name package a at repos/a, giving two distinct entries but the same repos/a/Cargo.toml. The first link succeeds and the second fails the entire discovery. Even two patch names pointing to one directory, one of which should merely disclose a name mismatch, trigger this failure. The synthetic decision adapter supports repeated reads; the native implementation no longer does.

**Required change:** Support repeated valid requests for the same file, preferably through an accounted cache of the already validated bytes or parsed manifest. If retaining and rereading the descriptor instead, reset its offset and preserve the custody/post-read checks; simply leaving it open at EOF is not a fix. Keep the record and link semantics equal to the reference.

**Validation:** Add a real composition vector with two distinct Cargo patch-source entries targeting one provider manifest, and another with a repeated target whose package name mismatches one entry. Both must complete with the reference record and links, without an invariant failure. Exercise both membership branches.

## Remaining requested judgments

LD-2's shared table replaces the unsound per-phase-only argument and handles the supplied races. Its claim of consistency through item 6b is too broad until RF-2 is fixed. LD-4's accepted-trial reuse is appropriate only when the relevant boundary and binding obligations hold. LD-10 is not accepted as a complete resolution: it corrects benign final records but cannot correct forbidden initial traversal, an earlier refusal, or the admitted mixed-case precedence difference. LD-11 is a sound representation choice: index gitlinks are boundary inputs, not fabricated filesystem VCS observations. Its effectiveness still depends on knowing them before the affected traversal.

The metadata/custody split avoids opening ordinary metadata-only lookups for ACL capture. The native layer retains no-follow traversal, positive marker lookups, walker listing conversion, bounded reads and a lazily begun session. Ordinary custody decisions and bounded-read outcomes are values outside the charged scopes; no new ordinary-refusal latch was identified. Budget exhaustion and host I/O remain failures. The required findings concern which objects/traversals are authorized and repeatable file consumption.

On the covered static cases, no-members refusal walks, D9 mapping, complete V3 serialization and path spelling follow the reference. Scope-limit D9 remains request-rejected / exit 2 / REQUEST.UNSATISFIABLE. Provider member paths are absolute under W, while packageDir stays relative. The pending internal type need not be removed merely to change its name.

**B3B2B2B-R2-NBO-1 — The internal partial and retained-read fixes are acceptable.** LD-1 remains acceptable: the complete result has the provenance serializer, while the pending core is an internal partial. R1 RF-2 is resolved for the reported native-stack mismatch: opens and observations bind the object, and directory custody captures the bound retained descriptor. R1 RF-4 is resolved for a single consumption: bytes uses the captured descriptor and validates full status and normalized ACL after the provisional bounded read, before releasing bytes. RF-3 above identifies a separate repeated-consumption regression.

**B3B2B2B-R2-NBO-2 — Retired-mutation and access-control limits are now stated accurately.** The .git-file-as-directory mutation remains redundant with unchanged item-6b layout refusal for its stated case. Retiring trial-refusal-keeps-members is justified only as equivalent on the covered vectors, not globally; r2 correctly says so and retains the clearing code. The access trace checks native-observation request paths, including an explicit gitlink opensip.json probe allowance, but does not cover the initial trial walker or individually trace item-6b operations. Its passes therefore do not settle RF-1 or RF-2. The missing late-refusal and host-read-error controls are disclosed; the oversize fixture exercises metadata refusal before reading, rather than a bounded-read error followed by postchecks.

The scenario uses the operation's own member precondition, the lent root's omission premise and home-filesystem predicate, and the scenario's empty environment/system sources plus trust groups. The archived host discovery_flag_tests all pass. This is scenario composition; production J1 integration is still deferred.

## Verification and evidence

I ran only the two expressly permitted checks, in the candidate:

- Operability source check: passed, 114 rows, no findings.
- workspace_discovery_vectors.py --check with the requested architecture/packages roots: passed against bound B3-b0 bytes.

Read-only JSON comparison independently confirms that each census file changes only the bytes/SHA fields at closure indices 0, 4 and 6, exactly as the archived equality projection states. The new no-binding checks are conditional, and existing callers receive empty gitlink sets. The outstanding workspace/full-ledger and held-out margin work is not claimed closed.

The pinned evidence records:

- Identical base/candidate failure sets: 14 failures. Library passes increase 1,145 to 1,152, with five ignored in each. Adding six documentation tests gives the reported 1,151 to 1,158 totals. The full suite remains failing at both subjects.
- Seven workspace-discovery tests pass: the 25-vector comparison/access test and six deterministic race tests. The focused discovery/member run has 90 passes; the host flag run has seven passes.
- Warning-denied Clippy passes both with and without scenario-fixtures. Formatting, all listed vector checks, FW-01/storage, census controls/check, environment exceptions, operability and verify_design are recorded passing.
- All twenty mutation logs show successful test compilation followed by a failing test, rather than a compile error. controls.json names the matching twenty mutations as caught.

The vectors and hooks materially improve r1, but none covers an initial trial refusal below an index-only boundary, an ancestor replacement preserving M's inode, or two declaration entries reading one manifest. The examples in the findings are derived from the source; I did not run new tests, builds, the lane or the census.

No private fixture, installation directory, key, held tree or T2 held-out entry/store/overlay was read. No network, other pane or delegation was used. B3-b2b2c's T2/joint controls, B3-b3a's bound, later margin work, J1 and qualification remain outside this unit. Only REVIEW.md and review.json in the requested directory were written.
