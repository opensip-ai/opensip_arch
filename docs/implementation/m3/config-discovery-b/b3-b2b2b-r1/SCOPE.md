# B3-b2b2b r1: the native workspace observation and the D15 discovery composition (M3-B unit B3-b, sub-unit B3-b2b2b)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1.** It implements B3-b2b2b of the B3-b plan r2 amendment A3 (`../b3-b/PLAN-r2-A3.md`; Codex `codex-b3b-plan-a3-r1`, ACCEPT), under law M3-B r9 items 19 to 24.

**Base.** Product main `d47f989`: B3-b2b2a bound, inventory v205, 168 contract successors. Architecture is at `5c581b5c`.

## What changes

| Path | Change |
| --- | --- |
| `crates/security/src/custody/workspace_observation.rs` | **New.** `NativeObservation`, the native `WorkspaceObservation`, below. |
| `crates/security/src/custody/workspace_discovery.rs` | **New.** `discover_with_members`, plus the complete `DiscoveryResultV3` and `DiscoveryProvenanceV3` with their serializer. |
| `crates/security/src/custody/workspace_discovery_tests.rs` | **New.** The composition control over the vectors, with the access control. |
| `crates/security/src/custody/workspace_discovery_vectors.json` | **New, generated.** 19 cases. |
| `tools/security/workspace_discovery_vectors.py` | **New.** It generates and checks those vectors from B3-b0 at its bound bytes. |
| `crates/security/src/custody.rs` | Two module declarations. **A closure file:** re-pinned. |
| `crates/security/src/custody/discovery_walk.rs` | `LISTING`, `STATUS`, `MAX_LISTED_ENTRIES`, `MAX_LISTED_NAME_BYTES`, `owned` and `same_object` become `pub(crate)`, for the native observation (LD-B3B2B2B-7). No behaviour changes. **A closure file:** re-pinned. Every census anchor still matches. |
| `crates/security/src/scenario.rs` | The scenario path calls `discover_with_members` with the operation's `member_precondition()` (LD-B3B2B2B-9). |
| `tools/security/discovery_census.py`, `discovery_census.json`, `discovery_census_vectors.json` | The two closure rows are re-pinned, and both files are regenerated (A1-2). |

## The native observation

`NativeObservation` answers the decision core's requests from the lent `DiscoveryRoot`, on the discovery ledger:
- **`entry(rel)`:** one accounted by-name observation (`observe_child_accounted`, `fstatat` no-follow) from the parent directory.
  - The parent is reached from W's retained descriptor by no-follow opens, segment by segment, through a reused stack of the directories last opened.
  - A component that is absent, a link (`ELOOP`) or not a directory reaches nothing.
  - **The ACL is captured where the metadata-only judgment passes** (LD-B3B2B2B-3): for a directory with or without the owner waiver, and for a regular file without it. The object is opened no-follow, matched with its observation, and captured with `capture_descriptor_acl_observed` (non-latching), under the omission premise as the walker normalizes it.
  - Each entry is memoized, so a path is one object for the decision, and a directory later opened through it must match.
- **`markers(rel)`:** positive lookups of `.git`, `.hg`, `.svn` and `.jj` under the directory, each with its kind.
- **`children(rel)`:** one charged listing through the walker's `ListingConversion` and its bounds.
- **`bytes(rel)`:** the file opened no-follow, matched with its observation, and read with `read_bounded_observed` at 4 MiB. A read past the bound is `TooLarge`.
- **`member_verdict(rel)`:** B3-b2b2a's `MemberSession`, begun at the first counted candidate under the handoff's proof (LD-B3B2B2B-6). The verdict is the member refusal's subject.

**Failures.** Host I/O, a change and ledger exhaustion fail the discovery (`WorkspaceRefusal`), and a walker refusal keeps its discovery mapping. A capture refusal other than a change or I/O is the object's unreadable ACL, a custody verdict. Custody and placement verdicts are values and never latch.

## The composition

`discover_with_members(root, upward, invocation, members, work)` runs:
1. **Phase one,** over a native observation.
2. **Branch A:** the trial walk with the provisional members (B3-b2a's walker and core), then phase two over a fresh observation, given the trial's verdict. The accepted trial is the final walk, because its members are the provisional ones (LD-B3B2B2B-4).
3. **Branch B, or W in a repository:** the walk with the decided members.
4. **A member rule's refusal:** the walk without members, whose provenance the refusal carries (LD-B3B2B2B-5, B3-b0's LD-B3B0-5). `PROJECT.SCOPE_LIMIT`'s D9 is request-rejected, exit 2, `REQUEST.UNSATISFIABLE`, and `PROJECT.ROOT_CUSTODY_REFUSED` keeps `CONFIG.INVALID`.
5. **The result:** the complete `DiscoveryResultV3`. It has `memberRepositories` rows with `declaredBy`, `memberConfigs` from the core, and `workspaceDeclarations`, all spelled under W. Its `to_json` gives `DiscoveryResultV3`'s shape. The links are the declaration half of the link set (plan r2 LD-B3B-3).

`members` is `None` when item 6a observed W in a repository, so W2 fails and the readers declare nothing.

## Vectors and controls

**The vectors.** `tools/security/workspace_discovery_vectors.py` builds 19 cases in the walk-vector tree format, reusing the walk tool's builders and SLM adapter unchanged. Each has:
- carriers and manifests as file texts;
- `gitMembers`, which the test makes real repositories with `git init`;
- `gitConfig`, one key that makes item 6b refuse, which the case also states as B3-b0's `memberObservations`;
- `wRepository`.

The tool adds B3-b0's `vcsMarkers` side table for every directory's markers, because the adapter records only the first. It runs B3-b0's `discover`, recording its access with B3-b2b1's recorder.

**The cases:**
- branch B, Cargo and npm, with links, globs and literal entries;
- candidates excluded by placement (another VCS marker) and by item 6b (an `include.path`);
- a member's own contents: its `opensip.json`, a nested repository and SX-1;
- the 65-candidate cap;
- W in a repository;
- custody: a group-writable carrier, an ACL-granted carrier and a world-writable member directory;
- branch A under both array sources: accepted, a placement refusal after the trial, item 6b's refusal, and the trial refusing, once for an absent root and once for a crossing into a member's nested repository.

**The composition test.** Each case is built as a scratch tree under a scratch H. Item 6a observes W's retained chain, `NoRepository::retained` gives the proof, and `discover_with_members` composes. **The complete record and the link rows equal B3-b0's,** with W spelled `/h/w`.

**The access control.** A test-only trace records every request the decision core makes and every platform operation the native observation makes. Then:
- every lookup, read, listing and 6b request is one B3-b0 made;
- every native operation touches a requested path, an ancestor of one (a directory open), or a VCS marker of a directory whose markers were asked.

## Lead decisions

- **LD-B3B2B2B-1. How "the pending shape is removed" is realized.** Plan r2 section 3 and A3 say the pending shape is removed. This unit makes the composition's `DiscoveryResultV3` the only emittable discovery record, with the only serializer, and the scenario consumes it. The core's `DiscoveryProvenancePending` stays as the walk and core's internal partial. It has no serializer, it is never emitted, and the composition always completes it. **Reason:** the walker, core, census tooling and the B2-b2, B2-b3 and B3-b2a vectors all consume the pending partial, and renaming or completing it in the core would change those reviewed records without changing behaviour. **Codex is asked whether this satisfies the plan's statement or whether the type must be removed.**
- **LD-B3B2B2B-2. One observation per phase.** Branch A's phases are separated by the trial walk, so each phase has its own memoized observation on the same ledger. Within a phase a path is one object. Across the phases, each observation and the walk check object identity against what they themselves observed. A change between them is a race, which C1's per-read custody covers.
- **LD-B3B2B2B-3. The ACL capture policy** (above). It is the walker's rule (capture exactly where the metadata-only judgment passes), applied to every object the core may judge. A directory is judged with and without the waiver, because the core's member-directory custody uses it. A capture refusal other than a change or I/O is `ACL_UNREADABLE`, never a pass.
- **LD-B3B2B2B-4. The accepted trial walk is the final walk.** No second walk runs.
- **LD-B3B2B2B-5. A member rule's refusal re-walks without members,** as B3-b0's `refused` does.
- **LD-B3B2B2B-6. The item-6b session begins lazily,** at the first counted candidate. With no candidate, no pass-level source is read.
- **LD-B3B2B2B-7. The walker's helpers are shared, not duplicated:** `ListingConversion` and its bounds, `STATUS`, `owned` and `same_object`. Making them `pub(crate)` re-pins `discovery_walk.rs`.
- **LD-B3B2B2B-8. Links:** `providerMember` is spelled under W, and `packageDir` stays W-relative, as in B3-b0's rows.
- **LD-B3B2B2B-9. The scenario path.** `MemberInputs` come from the lent root (its premise and its check that a filesystem is H's), with the scenario's empty environment and system sources, and `trust_groups`.

## Census (A1-2)

Both census files differ from the base only in `closure/0` (`discovery_walk.rs`) and `closure/6` (`custody.rs`). The held-out rows were already outstanding at the base, and they stay so. See `evidence/b3b2b2b-checks-r1/equality-projection.json`.

## Checks

Lane r1, `evidence/b3b2b2b-checks-r1/`:
- the security suite at base and candidate, with equal failure sets and one new test;
- the host's scenario-driven discovery tests (`discovery_flag_tests`);
- Clippy, warnings denied, on security with and without `scenario-fixtures`;
- rustfmt on new and base-clean edited files;
- the composition, member, walk, scan, upward and rule vector checks;
- FW-01, walk storage, the census controls and the census `--check`;
- the equality projection;
- the environment exceptions, operability and verify_design.

**Mutations,** each caught by the `workspace_discovery` tests:
- a regular file's ACL never captured;
- the `.git` marker missed;
- listings dropped;
- the 6b subject dropped;
- the precondition ignored;
- the refusal path, member rows or declaration paths left unspelled;
- the scope-limit D9 altered;
- a member-rule refusal dropping its declaration rows (named `member-refusal-keeps-walk-members` in the lane);
- the trial walk run without the provisional members.

**Two mutations from the pre-submission lane are retired as equivalent** (that lane is not archived):
- **A `.git` file taken for a directory.** Item 6b's own layout then refuses the member with the same subject, `git-not-directory`. It is replaced by `git-marker-missed`.
- **A trial refusal keeping its members.** For every refusal these vectors reach, including a crossing into a member's nested repository, the walk's refusal provenance holds no members. Clearing them, as B3-b0 does, is kept for faithfulness. Whether a walk refusal can ever carry members, for example at the 4,096-unit limit, is not shown here. The crossing case was added to look for a difference, and confirms there is none.

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
