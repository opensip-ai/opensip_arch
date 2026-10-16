# B3-b2a r1: the S3 walk and core with supplied D15 members (M3-B unit B3-b, sub-unit B3-b2a)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.** It implements the walker-and-core half of section 3 of the accepted B3-b plan r2 (`../b3-b/PLAN-r2.md`; Codex `codex-b3b-plan-r2`), as split by plan amendment A1 (`../b3-b/PLAN-r2-A1.md`), submitted with this unit. The law is M3-B r9 item 22 (D15 members entered as ordinary directories) and item 19's SX-1 (the `.opensip` anchor at each member root).

**Base.** Product main `25972e1`: 168 contract successors (B3-b0 bound), inventory v202. B3-b1 (item 6b) is accepted (Codex `codex-b3b1-r3`; product code `5b87728`, architecture `a97a1245`), and its inventory v203 follows. B3-b2a does not depend on it, because the member set is supplied, and the two touch disjoint paths. B3-b2a's lane ran at `25972e1`. At integration, B3-b2a's exact reviewed bytes are applied on main after B3-b1 and v203, and the census check and the `discovery_` tests are re-run there.

## What changes

| Path | Change |
| --- | --- |
| `crates/security/src/custody/discovery_walk.rs` | `WalkRequest.member_roots` and `Walk.members`. `discover_downward` passes the invocation's existing `member_roots`, which B2-a and B2-b thread through the shared rule and the scan. **The member roots reach the shared rule** at the three sites that passed an empty set: `classify_entry` for each listed directory, and `classify_path` on the probe chain and at a judged root. So SX-1's `.opensip` anchor applies at each member root, and a member root is not a crossing. **A member root is not a boundary:** its VCS evidence and its own `opensip.json` do not end the descent, in the listing and on the probe chain. The VCS evidence is still observed and recorded on its entry. |
| `crates/security/src/custody/discovery_scan.rs` | **A member is not a nested repository.** It is recorded in `memberRepositories`, from the supplied set. **A member's own `opensip.json` is not a nested project;** it is recorded in `memberConfigs` and never read (item 22). **Unreadable-ACL anchors** are classified with the member roots, as the walk is. |
| `crates/security/src/custody/discovery_walk_tests.rs` | `run_case` reads an optional `members` list from a vector. `check_vectors` is shared by the walk vectors and a new test, `every_member_vector_matches_the_reference_population_evidence_and_records`, over the member vectors. Six existing `WalkRequest` literals pass the empty set. |
| `crates/security/src/custody/discovery_scan_tests.rs` | `run` reads an optional `members` list from a scan vector's input. A new test, `every_member_scan_vector_is_reproduced`, covers the member vectors' `scanCases` (LD-B3B2A-6). |
| `tools/security/discovery_member_vectors.py` | **New.** It generates and checks the member vectors from B3-b0 at its accepted bytes (pinned: `member_reader_reference.py`, B2-b0's `discovery_scan_reference.py`, and B2-b0's `evidence/check.py` for its synthetic-tree helpers). |
| `crates/security/src/custody/discovery_member_vectors.json` | **New, generated.** Twelve walk cases and four scan cases. |
| `tools/security/discovery_census.py` | **The `CLOSURE` rows** for `discovery_walk.rs` and `discovery_scan.rs` are re-pinned (A1-2). No anchor, constant or model step changes. |
| `crates/security/src/custody/discovery_census.json`, `discovery_census_vectors.json` | **Regenerated** (`--write`, lead-readable stores only). They differ from the base only in the two closure rows and in the held-out rows' standing (below). |

## The member vectors

Each case is a walk-vector tree (the walk tool's own format and observation adapter, imported unchanged) with a supplied set of admitted member roots. The security test materializes the tree in scratch and walks it natively with those member roots. It then runs the core and compares, against B3-b0's pass two (`_finish`) with the same members:
- the population;
- the evidence and custody inputs;
- the records;
- any refusal;
- the boundary inventory.

**The twelve walk cases:**
- `members-automatic`: two members entered under an automatic source, with:
  - units inside them;
  - each `.git` as a `vcs-tree` row;
  - a member's own `opensip.json` in `memberConfigs`;
  - SX-1 at a member root (`m1/.opensip`);
  - a nested repository and a nested project inside a member, kept as boundaries;
  - Cargo `target` under a member's Cargo root;
  - a sibling non-member repository as a boundary.
- `member-nested-path`: members below an intermediate directory.
- Under each of config workspace roots and `--workspace-root` (six cases):
  - `members-exact-roots-*`: exact roots inside members;
  - `member-root-in-nested-repository-*`: a root inside a member's nested repository, which still refuses (`PROJECT.EXPLICIT_PATH_INVALID`);
  - `member-root-at-member-*`: a root at the member itself.
- `member-root-below-member-anchor-*`, under each source: an exact root below a member's SX-1 anchor. The probe chain refuses at `m1/.opensip` (`PROJECT.EXPLICIT_PATH_INVALID`) and never opens it.
- `member-directory-custody`: a member whose directory fails custody. Its units are excluded, and it is still not a boundary.
- `no-member-control`: no member among repositories. This is the control, identical to B2-b0's walk.

**The four scan cases (`scanCases`).** These are synthetic observed scopes in the scan-vector format, built with B2-b0's checker helpers. Each is computed by the same B3-b0 pass two and the same population as the walk cases. A member root `m1` has its SX-1 anchor `m1/.opensip` either ACL-unreadable or readable, under each of the marker-inventory bases `observed-inventory` and `not-enumerated`. Under the observed inventory, the unreadable anchor's count is `not-enumerated`, and the readable one's is 0, because the anchor is never entered.

## Lead decisions

- **LD-B3B2A-1. B3-b2 in two steps** (plan amendment A1-1). B3-b2a is the walker and core with a supplied member set. B3-b2b is the readers, placement, item 6b's composition, `workspaceDeclarations`, links and the T2 controls. **Rejected:** one unit. It would put the closure change and the readers' dispositions in one review, where the plan otherwise keeps one subject per review.
- **LD-B3B2A-2. The closure is re-pinned here** (A1-2), with section 4.2's equality projection for this change (`evidence/b3b2a-checks-r1/equality-projection.json`). Without it, product main's census `--check` would fail from this commit until B3-b3a. **The held-out margin is outstanding from this commit until B3-b3b.** The ten held-out rows read `outstanding: held-out (blind receipt stale)`, and `heldOutMargin` reads `outstanding`. No held-out store is opened. **Rejected:**
  - leaving main's census check failing until B3-b3a;
  - a blind run per closure change.
- **LD-B3B2A-3. The expected population restores what the walker observes of a member before entering it.** B3-b0's `_finish` hides each member's own VCS evidence and its root `opensip.json` from SLM: they decide membership, not boundaries. But the native walk observes both at the member root before entering, as it observes every directory. So the vector computes B2-b0's `walker_population` under B3-b0's member-aware rule (`_PopulationRule`) and restores those two facts at each member root. **The records are B3-b0's, unchanged.** The reference is not changed.
- **LD-B3B2A-4. Records without the reader half.**
  - `memberRepositories` are listed by path from the supplied set. B3-b2b adds the rows with their 6b verdicts.
  - `workspaceDeclarations` is absent; B3-b2b's readers write it. The vectors delete it from B3-b0's result and compare the rest.
- **LD-B3B2A-6. Scan cases where a scratch tree cannot reach.** The core classifies unreadable-ACL directories against the member roots. A scratch tree cannot hold an unreadable ACL, as the walk-vector tool states. So that classification is tested over synthetic observed scopes in the scan-vector format, generated from B3-b0, as B2-b2's scan vectors are from B2-b0. **Found by the pre-submission lane:** that lane (`b3b2a-checks-r0-presubmission`, not archived) ran with the first ten walk cases, and two mutations survived, `probe-member-anchor-dropped` and `unreadable-anchor-members-dropped`. They were coverage gaps, not defects. The two probe-chain walk cases and the four scan cases were added, and lane r1 catches both mutations.
- **LD-B3B2A-5. A supplied member is listed even if its directory fails custody** (`member-directory-custody`). The supplied set is what item 6b admitted. The custody failure excludes its units, as for any directory; it does not make the member a nested repository. This is B3-b0's verdict.

## Equality projection (plan r2 section 4.2, A1-2)

`evidence/b3b2a-checks-r1/equality-projection.json` compares the base and candidate census files structurally. **The only changed paths:**
- in both files, `closure/0` (`discovery_walk.rs`) and `closure/4` (`discovery_scan.rs`), bytes and SHA-256;
- in `discovery_census.json` only:
  - the ten held-out entries' `status` (`blind-census` → `outstanding: held-out (blind receipt stale)`);
  - their composed `result`, which is withdrawn;
  - `heldOutMargin` (`holds (blind census)` → `outstanding`).

**Unchanged:** every lead-readable row, field by field, and every census vector's prediction.

## Checks

Lane r1, `evidence/b3b2a-checks-r1/`:
- the security suite at base and candidate (`--no-fail-fast`), with equal failure sets and two new passing tests;
- the equality projection;
- rustfmt on the edited files (all four are rustfmt-clean at base);
- Clippy, warnings denied, all targets;
- the `discovery_` tests;
- the member, walk, scan, upward and rule vector checks;
- the FW-01 pin;
- the walk-storage and census-tool controls;
- the census `--check` over the lead-readable stores;
- the environment exceptions;
- the operability source census;
- verify_design.

**Mutations.** Each one patches a closure file, and the `discovery_` tests must fail. The gate skips the closure-pin test, so each mutation must be caught by a behavioural test:
- a member is a boundary in the listing;
- a probed member is a boundary;
- the SX-1 member anchor is dropped in the listing;
- the SX-1 member anchor is dropped on the probe chain;
- `discover_downward` drops the members;
- a member is recorded as a nested repository;
- `memberRepositories` is dropped;
- `memberConfigs` is dropped;
- a member's `opensip.json` is a nested project;
- unreadable anchors are classified without the members.

## Inventory

New paths for the inventory after acceptance:
- `tools/security/discovery_member_vectors.py`;
- `crates/security/src/custody/discovery_member_vectors.json`.

## Not claimed

- No reader, placement, item 6b composition or link. No production caller supplies a member, so product discovery is unchanged.
- No extension of the census cost model, and no member-descent validation: those are B3-b3a's.
- The held-out margin is outstanding, not held, until B3-b3b.
- No qualification.
