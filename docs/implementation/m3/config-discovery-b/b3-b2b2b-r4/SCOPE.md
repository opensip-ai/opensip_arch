# B3-b2b2b r4: the native workspace observation and the D15 discovery composition (M3-B unit B3-b, sub-unit B3-b2b2b)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 4.**

It implements B3-b2b2b of the B3-b plan r2 under law M3-B r9 items 19 to 24, as amended by:
- **A3** (`../b3-b/PLAN-r2-A3.md`; Codex `codex-b3b-plan-a3-r1`, ACCEPT);
- **A4** (`../b3-b/PLAN-r2-A4.md`; Codex `codex-b3b-plan-a4-r2`, ACCEPT).

Its authority for D15 is now **B3-b0 r4** (`../b3-b-reference-r4/`, contract successor 169; Codex `codex-b3b0-reference-r4-r2`, ACCEPT-DESIGN-UNIT).

Rounds 1 to 3 (`../b3-b2b2b-r1/` to `../b3-b2b2b-r3/`) describe what this round keeps. This record states the whole unit as it now stands.

**Base:**
- product main `92624ae`: B3-b0 r4 bound, 169 contract successors, inventory v205;
- architecture `271d7eee`.

## r4 changes (Codex `codex-b3b2b2b-r3`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B3B2B2B-R3-RF-1:** a cached read was cloned before its copy was charged | **`copy_kept` charges first.** A repeated request's copy is charged on the discovery ledger as one owned record of its bytes (`owned(len)`), and only then cloned. **Control:** `a_kept_read_is_copied_only_after_its_copy_is_charged`:<br>- a ledger that cannot fund the copy refuses with `Budget`, and the test-only `copy-kept` trace shows nothing was copied;<br>- an ample ledger is charged exactly `owned(4096)`.<br>The repeated-provider vectors stay. **Mutations:** `kept-copy-before-charge` and `kept-copy-uncharged`. |
| **B3B2B2B-R3-RF-2:** the identity collector's storage was uncharged | **Opt-in and charged.** `member_layout` takes `Option<&mut MemberIdentities>`. `observe` and `observe_members` pass `None`: they build no identity record, so their charges are unchanged by construction. `observe_identified` passes the list, and `push_identity` charges each record before building it. A record is its path's bytes plus the list slot holding it and its status (`identity_cost`: `owned` of both). Its length is computed from the segments before the path exists, and a debug assertion checks it. **Controls:**<br>- `identified_observation_charges_each_identity_record_before_building_it`: two members with a deep, shared prefix (`x/y/z`, `x/y/q`). The verdicts equal `observe`'s, `observe` builds nothing, and the identified ledger's use is exactly `observe`'s plus each record's `identity_cost`, shared prefixes counted per record;<br>- `an_identity_record_is_built_only_after_its_charge`: a ledger that cannot fund the record refuses with nothing built (the build closure never runs), and an ample one is charged exactly `identity_cost`.<br>Round 2's session-versus-batch charge equality still passes. **Mutations:** `identity-built-before-charge` and `identity-uncharged`. Round 3's four identity-comparison mutations stay. |
| **NBO-1:** attempt 2 also failed rustfmt | **Corrected below:** attempt 2 failed rustfmt and the member-identity survivor. |

## r3 changes (Codex `codex-b3b2b2b-r2`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B3B2B2B-R2-RF-1:** the first branch-A trial crossed index-only repository boundaries | **Resolved at the authority, by plan amendment A4.**<br>**Branch A decides its members before any walk.** The decision core's `branch_a` runs:<br>1. **the array gate.** It is pure. More than 4,096 roots, then the first malformed root, each refuse with SLM's record as `Decision::ArrayRefused`: `PROJECT.EXPLICIT_PATH_INVALID`, SLM's D9, and the root's raw text (or no path) with the provenance of the walk without members;<br>2. **the member decisions, in path order:** placement and other volumes, the cap, then directory custody and item 6b per candidate, stopping at the first refusal;<br>3. **`PhaseOne::Admitted`,** carrying the admitted members and their W-relative index gitlinks.<br>**The composition walks once** with those members and gitlinks. A refusal is the result, with no members and the rows as they stood (`Admitted::declarations`). Only an accepted walk reaches `links`, the readers' link stage. **Removed:**<br>- `Trial` and `TrialRefused`;<br>- `phase_two`;<br>- the gitlink re-walk;<br>- LD-B3B2B2B-10.<br>**Vectors:** B3-b2b1's member vectors and this unit's composition vectors are regenerated from B3-b0 r4, which takes gitlinks as item 6b's `memberGitlinks` report, as the product does. So the r2 access allowance for the gitlink's `opensip.json` probe is gone. **New composition controls,** under both array sources:<br>- **`a-gitlink-crossing-custody-below-*`:** a world-writable directory below a gitlink is never judged; the record is the crossing.<br>- **`a-member-gitlink-subtree-unlistable-*`:** a selected member whose gitlink holds an unreadable directory and a nested `opensip.json`. Discovery accepts. The paired test `without_its_gitlink_the_unlistable_subtree_fails_the_walk` shows the walk lists it and fails without the gitlink.<br>- **`a-mixed-gitlink-crossing-and-6b-refusal-*`:** the member rule first, by A4's priority.<br>- **Walker-trace assertions:** every composition case with a gitlink checks, through the walker's own test trace, that no walk lists the gitlink, opens below it, or observes anything deeper than its direct children (`check_gitlinks_not_entered`). There are 11 such cases. |
| **B3B2B2B-R2-RF-2:** item 6b did not bind its reopened ancestors and Git evidence | **Every object item 6b opens is bound.** `MemberSession::observe_identified` returns each directory `member_layout` opened from W's child to M, and `M/.git`, `M/.git/config` and `M/.git/index` (`label_in_git`), each with its sample. The native `member_verdict` binds every one in the shared table before the verdict reaches the core. So a replaced ancestor or `.git` is a change before admission. (`MemberIdentities` names the list's type. (r4) Its records are charged before they are built; `observe` builds none.) `observe` and `observe_members` are unchanged. **Controls, each in both branches:**<br>- **`an_ancestor_replaced_around_its_preserved_member_before_item_6b_is_a_change`:** at `before-verdict`, `repos` is moved aside, a world-writable `repos` takes its name, and the original `repos/a` is moved into it. The test asserts the inode is preserved.<br>- **`a_member_git_directory_replaced_before_item_6b_is_a_change`:** `repos/a/.git` is replaced by a fresh repository's, with `repos/a` preserved.<br>- **`a_member_replaced_around_its_preserved_git_directory_before_item_6b_is_a_change`:** only M changes. A new `repos/a` takes the name, holding the original `.git` (its inode preserved), so the member comparison alone catches it.<br>**Each of these, and round 2's member-replacement control, asserts the change is found inside item 6b's verdict** (`changed_before_admission`): that verdict is the core's last request, and no walk listed anything. A change a later observer catches does not pass. The lane's first attempt showed this was needed: `item-6b-ancestors-ignored` and `item-6b-member-ignored` survived, because the walk caught the replacement. Its second showed `item-6b-member-ignored` still survived, because every member replacement also replaced `.git`. Hence the third control.<br>**Mutations, each comparison on its own:**<br>- `item-6b-identities-ignored`;<br>- `item-6b-ancestors-ignored`;<br>- `item-6b-git-evidence-ignored`;<br>- `item-6b-member-ignored`. |
| **B3B2B2B-R2-RF-3:** a provider manifest could be read only once per phase | **A validated read is kept.** The native observation's `read` map holds each path's bounded, post-checked outcome. A repeated `bytes` request returns a copy and charges the ledger for it, so record and link semantics equal the reference's. **Vectors**, in both branches:<br>- `a-two-patch-sources-one-manifest-*` (two sources and a second name on one manifest);<br>- `b-one-manifest-two-sources`;<br>- `b-one-manifest-name-mismatch`.<br>**Mutation:** `read-cache-disabled`. |
| **NBO-1:** the internal partial and retained-read fixes are acceptable | Kept. |
| **NBO-2:** the retired mutations and access limits are stated accurately | **The access record now covers the walk.** The walker's own trace is asserted for gitlinks, and the trial walk no longer exists. **The gate's controls** assert that no directory custody or item-6b verdict is requested (`check_gate`, 6 cases). The member vectors now pin item 6b's consultations exactly (`sixB`, equality). The remaining limits are under "Not shown". |

## What changes

| Path | Change |
| --- | --- |
| `crates/security/src/custody/workspace_observation.rs` | **New.** `NativeObservation`, the binding table, the validated-read map (r3) and the test-only trace and hook. |
| `crates/security/src/custody/workspace_discovery.rs` | **New.** `discover_with_members`: (r3) one walk, and branch A's links after it. Also the complete `DiscoveryResultV3` and `DiscoveryProvenanceV3` with their serializer. |
| `crates/security/src/custody/workspace_discovery_tests.rs` | **New.** Twelve tests: the composition and access control over 41 vectors, with the walker-trace and gate assertions; the paired unlistable-subtree control; nine race controls; and (r4) the kept-copy charge control. |
| `crates/security/src/custody/workspace_discovery_vectors.json` | **New, generated.** 41 cases. |
| `tools/security/workspace_discovery_vectors.py` | **New.** It generates and checks those vectors from B3-b0 r4 at its bound bytes. |
| `crates/security/src/custody/workspace_declarations.rs` | **(r3)** `branch_a`, `Admitted`, `links` and `Decision::ArrayRefused`, replacing the trial phase. **(r2)** The trait gains `custody_entry`, `member_verdict` returns `MemberOutcome`, and entries below a gitlink are disclosed. |
| `crates/security/src/custody/workspace_declarations_tests.rs`, `workspace_member_vectors.json`, `tools/security/workspace_member_vectors.py` | **(r3)** Regenerated from B3-b0 r4. There are 189 cases (154 before); two non-string arrays are listed by id. The adapter compares branch A's walk members and gitlinks, and item 6b's consultations exactly (`sixB`). It separates forbidden lookups from forbidden reads (`forbiddenReads`; LD-B3B2B2B-15). The tripwire fires only in the custody-and-6b phase (LD-B3B2B2B-13). |
| `crates/security/src/custody/git_tracking.rs` | **(r2, r3, r4)** `MemberSession::observe_identified` returns every object `member_layout` opened (`MemberIdentities`). Each record is charged before it is built (`push_identity`, `identity_cost`). `observe` and `observe_members` collect nothing, so their charges are unchanged. |
| `crates/security/src/custody/discovery_walk.rs` | `WalkRequest.gitlinks` and `.bound`, `discover_downward_bound`, the walker's binding checks, and gitlinks as boundaries. **A closure file:** re-pinned. |
| `crates/security/src/custody/discovery_scan.rs` | `DiscoveryInvocation.gitlinks`: a gitlink is a nested repository. **A closure file:** re-pinned. |
| `crates/security/src/custody.rs` | Two module declarations. **A closure file:** re-pinned. |
| `crates/security/src/scenario.rs` | The scenario path calls `discover_with_members` with the operation's precondition. |
| `git_tracking_member_tests.rs` (rustfmt-clean at base, so formatted; (r4) two accounting controls), `discovery_walk_tests.rs`, `discovery_scan_tests.rs`, `discovery_census_tests.rs` | The new arguments and fields. |
| `tools/security/discovery_census.py`, `discovery_census.json`, `discovery_census_vectors.json` | Three closure rows are re-pinned, and both files are regenerated. |

## Lead decisions

LD-B3B2B2B-1 to 9 and 11 are kept as rounds 1 and 2 state them, with these changes:
- **LD-4 (r3): one walk.** The final walk is the only walk, in both branches.
- **LD-10: withdrawn.** There is no trial, so no trial refusal and no unmodeled mixed case. A4 settles the mixed case's priority, and B3-b0 r4 pins it.

**New:**
- **LD-B3B2B2B-12. In branch A the links follow the walk.** B3-b0 r4's step 3 walks before the readers' link stage. A walk refusal carries the rows as they stood, and no provider manifest is read. The core's `links` runs on a fresh native observation over the same binding table, as phase two did.
- **LD-B3B2B2B-13. The short circuit is the custody-and-6b phase's.** B3-b2b1's tripwire fired on any lookup after its trial. It now fires on a candidate's directory custody or its item-6b verdict. The placement lookups that form and count the candidates precede that phase (A4-2 step 2; Codex B3BA4-R1-NBO-2).
- **LD-B3B2B2B-14. A non-string root is not a product input.** The product's arrays are strings: Config2 admits `workspaceRoots` as strings, and `--workspace-root` takes text. So B3-b0 r4's two non-string gate cases are listed by id (`nonStringArray`), not run.
- **LD-B3B2B2B-16. A walk-refusal vector carries a member configuration.** `a-walk-refuses-crossing-*` gives `repos/a` its own `opensip.json`, so clearing `memberConfigs` on a walk refusal is observable. The lane's first attempt showed it was not: `walk-refusal-keeps-members` survived, because the serializer takes `memberRepositories` from the composition's own rows.
- **LD-B3B2B2B-15. Forbidden reads and forbidden lookups are separate.** B3-b0 r4's `notRead` paths below a gitlink are looked up by the reference's own placement (its LD-B3B0-16). So the member vectors hold them as `forbiddenReads`, which the core must never read. Its lookups are bounded by the `consulted` comparison. `notObserved` stays `forbidden`: no lookup, read or listing.

## Checks

Lane r4, `evidence/b3b2b2b-checks-r4/`. Round 3's lane and its two earlier attempts are in `../b3-b2b2b-r3/evidence/`. In round 3, the first attempt failed on:
- Clippy (`type_complexity` on the identity list);
- rustfmt (`git_tracking_member_tests.rs`);
- the three mutation survivors named above.

The second failed on rustfmt and the `item-6b-member-ignored` survivor (r4, NBO-1). The third passed. This round's lane is:
- the security suite at base and candidate, with equal failure sets and fourteen new tests (twelve composition, two member-accounting);
- the host's scenario-driven discovery tests;
- Clippy, with and without `scenario-fixtures`;
- rustfmt;
- every vector check: composition, workspace member, discovery member, walk, scan, upward and rule;
- FW-01, walk storage, the census controls and the census;
- the equality projection: only `closure/0`, `closure/4` and `closure/6` change;
- environment, operability and verify_design.

**Mutations (thirty-four, judged by the workspace and `git_tracking` tests):**
- round 2's, less the four that targeted the trial or the gitlink re-walk;
- **branch A's walk:** `walk-without-members`, `branch-a-walk-without-gitlinks`, `branch-b-walk-without-gitlinks`, `walk-refusal-keeps-members`, `walk-refusal-rows-dropped`;
- **the gate:** `grammar-gate-skipped`, `size-gate-skipped`, `gate-path-spelled`, `gate-detail-not-per-source`;
- **item 6b's identities:** the four listed under RF-2, replacing `item-6b-identity-ignored`;
- `read-cache-disabled`;
- `member-refusal-rows-dropped`, renamed from round 2's `member-refusal-keeps-walk-members`;
- (r4) `kept-copy-before-charge`, `kept-copy-uncharged`, `identity-built-before-charge` and `identity-uncharged`.

## Not shown

- (r3) Round 2's gap is closed: a walk refusal whose provenance carries members is now reached, by the `a-walk-refuses-*` and gitlink-crossing cases. `walk-refusal-keeps-members` pins its clearing. A refusal at the 4,096-unit limit itself is still not reached.
- A native read failure other than the bound, from host I/O, has no deterministic control. It fails the discovery as host I/O. The unreadable directory of the paired control is such a failure in the walk, not a read.
- Branch A's link stage reads manifests after the walk. No race control replaces a manifest between the walk and its read other than the existing `before-read` controls.

## Inventory

New paths for the inventory after acceptance:
- `crates/security/src/custody/workspace_observation.rs`;
- `crates/security/src/custody/workspace_discovery.rs`;
- `crates/security/src/custody/workspace_discovery_tests.rs`;
- `crates/security/src/custody/workspace_discovery_vectors.json`;
- `tools/security/workspace_discovery_vectors.py`.

## Not claimed

- No T2 link-map control and no joint sweep (B3-b2b2c).
- No member-observation bound (B3-b3a).
- No CLI composition (J1).
- No qualification.
