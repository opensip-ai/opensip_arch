# B3-b2b2b r2: the native workspace observation and the D15 discovery composition (M3-B unit B3-b, sub-unit B3-b2b2b)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 2.** It implements B3-b2b2b of the B3-b plan r2 amendment A3 (`../b3-b/PLAN-r2-A3.md`; Codex `codex-b3b-plan-a3-r1`, ACCEPT), under law M3-B r9 items 19 to 24. Round 1, `../b3-b2b2b-r1/`, describes what this round keeps. This record states the whole unit as it now stands.

**Base.** Product main `d47f989`: B3-b2b2a bound, inventory v205, 168 contract successors. Architecture is at `5c581b5c`.

## r2 changes (Codex `codex-b3b2b2b-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B3B2B2B-R1-RF-1:** admitted index gitlinks were discarded | **Item 6b's outcome carries the gitlinks.** The decision core's `member_verdict` returns `MemberOutcome::Admitted { gitlinks }` or `Refused`, and the native observation converts item 6b's member-relative gitlink paths. **The core** treats an entry at or below a member's gitlink as inside a nested repository: it is `entry-not-in-a-member`, and nothing in it is read or linked. Its `Decision::Members` carries the W-relative gitlinks. **The walk and core** take them as `DiscoveryInvocation.gitlinks` and `WalkRequest.gitlinks`. **They are nested repositories, and no VCS evidence is recorded:**<br>- the walker treats one as a boundary, both in a listing and on an exact root's probe chain, so it never enters it;<br>- the scan core records it in `nestedRepositories`, so an exact join crossing it refuses `JOIN_CROSSES_NESTED_REPOSITORY`.<br>**Branch A:** gitlinks are known only once item 6b admits a member, which is after the trial walk. When any admitted member has one, the walk runs again with them. A refusal that walk gives is recorded as B3-b0 records a trial refusal: no members, and the rows as they stood at the trial (LD-B3B2B2B-10). **Controls:** a real member index with a gitlink at a populated directory with no VCS marker, written by `git update-index --cacheinfo 160000`, in five vectors:<br>- branch B (`b-member-index-gitlink`): the walk never enters it, no unit lies below it, and the entry inside it declares and links nothing;<br>- branch A under both array sources: a root crossing it refuses (`a-root-crosses-index-gitlink-*`), and a root beside it is accepted without the walk entering it (`a-root-beside-index-gitlink-*`).<br>B3-b0 has no index, so its input states each gitlink as its directory's VCS evidence: the nested repository item 21 makes it. The access control allows the one boundary probe this representation difference gives, which the walker also makes of every probed directory: the gitlink directory's own `opensip.json`. **Mutations:** `walker-gitlinks-ignored`, `core-gitlinks-ignored`, `links-below-gitlinks`, `gitlink-walk-skipped`, `gitlink-refusal-not-the-trials`. |
| **B3B2B2B-R1-RF-2:** retained stack directories were not bound to the objects custody judged | **One binding table.** It maps each W-relative path to its object identity: device, inode and kind (`Bindings`). These all bind or check their path:<br>- every directory the native observation opens through its stack;<br>- every by-name observation;<br>- every VCS marker it finds;<br>- the root.<br>A path seen again, by any of them, must be the same object, or the discovery fails with a change. A path bound and later absent is a change too. **Custody is judged on the bound descriptor:** a directory's ACL is captured from the stack's own descriptor for that path, and a regular file's from the descriptor opened for it, which is retained for its read. So custody of a replacement B can never authorize a read through A. **Controls:**<br>- `a_directory_replaced_between_its_open_and_its_custody_is_a_change`: `.cargo` A is opened by the carrier probes, then made world-writable and moved aside, and B takes its name before the carrier-parent custody. The result is a change, and the carrier is never read;<br>- `a_reused_prefix_replaced_under_a_custody_judgment_is_a_change`: a retained `repos` is replaced before the member custody that reuses it;<br>- `a_directory_replaced_before_the_walk_is_a_change`: `packages`, observed in phase one for the globs, is replaced before the walk, and the walk's own binding check catches it.<br>**Mutations:** `binding-mismatch-ignored`, `walker-binding-ignored`. |
| **B3B2B2B-R1-RF-3:** bindings were lost across the phases, the trial walk and item 6b | **The same table runs through phase one, the trial walk, phase two and the final walk:**<br>- the walks run as `discover_downward_bound`, which checks every entry the walker observes against the table and binds the rest;<br>- item 6b's session reports the member directory it opened and admitted (`MemberSession::observe_identified`), which must be the bound object.<br>**Controls:**<br>- `a_member_replaced_after_an_accepted_trial_is_a_change`: branch A, `repos/a` replaced by another conventional repository between the accepted trial and phase two;<br>- `a_member_replaced_between_its_custody_and_item_6b_is_a_change`: branch B.<br>**Mutation:** `item-6b-identity-ignored`. |
| **B3B2B2B-R1-RF-4:** carriers were read from a fresh descriptor, not the custody-bound one | **`bytes` reads from the very descriptor whose capture judged custody.** That is the regular file `custody_entry` opened and captured, retained until its read. After the bounded read it samples the descriptor's status and captures its ACL again. Both must equal the custody capture (the full status, including size and times, and the normalized ACL), or the discovery fails with a change. The read's outcome is a value until these checks finish, and they are funded on the ledger. The same discipline holds for provider manifests. **The decision core** now makes every custody judgment through `custody_entry(rel, object)`, a metadata entry with its ACL captured from the bound object. `entry(rel)` is metadata only. **Control:** `a_carrier_or_manifest_changed_around_its_read_is_a_change`, with four cases, each a change of that path:<br>- the carrier made world-writable before its read;<br>- an ACL write grant added to it before its read;<br>- its bytes appended to during the read;<br>- a provider manifest made world-writable before its read.<br>**The ordinary oversize case** (`b-carrier-oversize`) is refused by custody on its size before any read, and discovery completes. **Mutation:** `post-read-check-dropped`. |
| **NBO-1:** LD-1 accepted | Kept. |
| **NBO-2:** do not claim the retired mutations' global equivalence | **Corrected below.** `trial-refusal-keeps-members` is retired because it is equivalent on these vectors, not globally. The clearing code is kept. No vector reaches a late refusal whose walk provenance carries members (see "Not shown"). |
| **NBO-3:** access tracing does not establish custody consistency | **Acknowledged.** Object identity is now established by the binding table and its race controls (RF-2 to RF-4). The access control stays, for the paths the core requests and the native operations they make. |

## What changes

| Path | Change |
| --- | --- |
| `crates/security/src/custody/workspace_observation.rs` | **New.** `NativeObservation`, the binding table and the test-only trace and hook. |
| `crates/security/src/custody/workspace_discovery.rs` | **New.** `discover_with_members`, plus the complete `DiscoveryResultV3` and `DiscoveryProvenanceV3` with their serializer. |
| `crates/security/src/custody/workspace_discovery_tests.rs` | **New.** Seven tests: the composition and access control over 25 vectors, and six race controls. |
| `crates/security/src/custody/workspace_discovery_vectors.json` | **New, generated.** 25 cases. |
| `tools/security/workspace_discovery_vectors.py` | **New.** It generates and checks those vectors from B3-b0 at its bound bytes. |
| `crates/security/src/custody/workspace_declarations.rs`, `workspace_declarations_tests.rs` | **(r2)** The trait gains `custody_entry`, and `member_verdict` returns `MemberOutcome`. Every custody judgment goes through `custody_entry`. Entries below a gitlink are disclosed, `Decision::Members` carries the gitlinks, and `Trial::declarations()` is added. B3-b2b1's 154 vectors are unchanged, and its adapter implements the two methods as before. |
| `crates/security/src/custody/git_tracking.rs` | **(r2)** `MemberSession::observe_identified` returns the admitted member directory's status, which `member_layout` already samples (no new charge). `observe` and `observe_members` are unchanged. |
| `crates/security/src/custody/discovery_walk.rs` | `WalkRequest.gitlinks` and `.bound`, `discover_downward_bound`, the walker's binding checks, and gitlinks as boundaries. `discover_downward` is `discover_downward_bound` with no table and no gitlinks, so its charges are unchanged. Also the shared helpers (r1). **A closure file:** re-pinned. |
| `crates/security/src/custody/discovery_scan.rs` | **(r2)** `DiscoveryInvocation.gitlinks`: a gitlink is a nested repository. **A closure file:** re-pinned. |
| `crates/security/src/custody.rs` | Two module declarations. **A closure file:** re-pinned. |
| `crates/security/src/scenario.rs` | The scenario path calls `discover_with_members` with the operation's precondition. |
| `discovery_walk_tests.rs`, `discovery_scan_tests.rs`, `discovery_census_tests.rs` | The new invocation and request fields, empty. |
| `tools/security/discovery_census.py`, `discovery_census.json`, `discovery_census_vectors.json` | Three closure rows are re-pinned, and both files are regenerated. |

## Lead decisions

LD-B3B2B2B-1 to 9 are round 1's, kept, with these changes:
- **LD-2 (r2): one binding table, not one observation per phase.** Round 1's per-phase argument is withdrawn (RF-3). Each phase's native observation is still fresh: its memo and its stack. But the identity table is one for the whole discovery, shared with both walks and item 6b.
- **LD-3 (r2):** the capture is taken from the bound descriptor, through `custody_entry` only. Metadata-only lookups capture nothing.
- **LD-4 (r2):** the accepted trial walk is the final walk unless an admitted member has a gitlink. Then the walk runs again with the gitlinks.

**New:**
- **LD-B3B2B2B-10. A refusal that only the members' gitlinks give is the trial's refusal.** In branch A the trial walk runs without the gitlinks: they are known only after the member decisions, and observing members before the trial would break B3-b2b1's short-circuit order (Codex B3B2B1-R1-RF-2). When the re-walk with the gitlinks refuses, its refusal is recorded as B3-b0 records a trial refusal. That is the walk's refusal and provenance, with no members and the rows as they stood at the trial. It is what B3-b0 gives when the gitlink is stated as VCS evidence. **Not modeled by B3-b0:** a case where a gitlink crossing in one member and a member-rule refusal of another would both apply. The product reports the member-rule refusal first, because it is decided before the re-walk. B3-b0, seeing the gitlink as a physical marker, would report the crossing.
- **LD-B3B2B2B-11. Gitlinks are nested repositories, never VCS evidence.** The walker records nothing in an entry's `vcs` for one. It is an invocation input, as the member roots are, and the scan core lists it with the repositories it observed.

## Checks

Lane r2, `evidence/b3b2b2b-checks-r2/`:
- the security suite at base and candidate, with equal failure sets and seven new tests;
- the host's scenario-driven discovery tests;
- Clippy, with and without `scenario-fixtures`;
- rustfmt;
- every vector check: composition, workspace, member, walk, scan, upward and rule;
- FW-01, walk storage, the census controls and the census;
- the equality projection: only `closure/0`, `closure/4` and `closure/6` change;
- environment, operability and verify_design.

**Mutations (twenty):**
- round 1's eleven, with three anchors retargeted to the r2 code: `acl-never-captured`, `verdict-subject-dropped` and `trial-walk-without-members`;
- the five gitlink mutations;
- the two binding mutations;
- `item-6b-identity-ignored`;
- `post-read-check-dropped`.

## Not shown

- A late walk refusal whose provenance carries members, for example at the 4,096-unit limit, is not reached by these vectors. The member-clearing code that B3-b0's trial refusal implies is kept.
- A native read failure other than the bound, from host I/O, has no deterministic control here. It fails the discovery as host I/O.

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
