# B3-b2b2a r2: the item-6b session and the handoff binding (M3-B unit B3-b, sub-unit B3-b2b2a)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 2.** It implements B3-b2b2a of the B3-b plan r2 amendment A3 (`../b3-b/PLAN-r2-A3.md`; Codex `codex-b3b-plan-a3-r1`, ACCEPT), under law M3-B r9 item 21 (X2 r9 item 6b).

**Base.** Product main `46c0ebb`: B3-b2b1 bound, inventory v205, 168 contract successors. Architecture is at `cd0f3e52`, which publishes A3.

## r2 changes (Codex `codex-b3b2b2a-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B3B2B2A-R1-RF-1:** the chain counter wraps, despite the never-reused identity | **A checked allocator, `draw_identity(counter)`.** It advances only with `checked_add(1)` by `fetch_update`, so it never wraps. At the end of the space it issues nothing, and `walk_project_chain_waived` fails closed through the existing host I/O refusal (`ProjectChainRefusal::Io`, "chain identity space exhausted"). No public refusal code is added, and ordinary item-6a behaviour is unchanged. **Control:** `the_chain_identity_allocator_never_reuses_an_identity_at_its_end`. A local counter at `u64::MAX - 2` issues two distinct identities, then nothing twice, and stays at `u64::MAX`. The live global counter is untouched. **Mutations:** `allocator-wraps`, and `identity-reused` (now: the counter never advancing). LD-B3B2B2A-1 is revised. |

The lane is `evidence/b3b2b2a-checks-r2/`, and round 1's is kept in `../b3-b2b2a-r1/`.

## What changes

| Path | Change |
| --- | --- |
| `crates/security/src/custody/project_chain.rs` | **`ChainIdentity`:** a private `u64` that `walk_project_chain_waived`, the one construction site, draws from a process-wide counter through the checked `draw_identity` (r2). It is never reused, and `ProjectChain::identity()` returns it. `ProjectChain` stays non-`Clone`. **A closure file:** re-pinned under A1-2. |
| `crates/security/src/custody/git_tracking.rs` | `TrackingObservation` records `root: ChainIdentity`, from `inputs.chain` in `observe_tracking`. **Its equality is the decision and the evidence only,** by a manual `PartialEq`, so `recheck_tracking` is unchanged. Also `NoRepository::retained(chain, observed)` and `MemberSession` (below). |
| `crates/security/src/custody/operation_handoff.rs` | `OperationHandoff::member_precondition()` builds the proof from the subject's own pair: `Eligible { admission, tracking }`, or the registered project's `chain()` and `tracking()`. |
| `crates/security/src/custody/git_tracking_member_tests.rs` | Four tests (below). |
| `crates/security/src/custody/operation_handoff_tests.rs` | One test (below). |
| `tools/security/discovery_census.py`, `discovery_census.json`, `discovery_census_vectors.json` | The `project_chain.rs` closure row is re-pinned, and both files are regenerated (A1-2). |

## The binding

**`NoRepository::retained(chain, observed)`** gives the proof only when two things hold:
- `observed` is `NoRepository`;
- its recorded identity equals `chain`'s.

A chain is told apart from every other retained chain, including a second walk of the same directory and a replacement at the same spelling. This binds the retained object, not its labels (Codex B3B1-R2-RF-1), once the chain and the observation are stored apart, as the operation's subject stores them. B3-b1's borrowed `RootObservation::no_repository` stays.

**Why the identity is outside the equality.** `recheck_tracking` compares a fresh observation with the retained one. Every recheck site re-observes the same retained chain:
- `first_registration` preconditions, over `admission.chain()`;
- the commit-time recheck, over `current.chain`;
- `namespace_lease`, over `root.chain()`;
- `installation_read`, the same inputs.

Including the identity would change nothing there. Excluding it makes item 6a's recheck provably unchanged.

## The item-6b session

`MemberSession::begin(inputs, proof, work)` runs the pass-level checks once: the environment, the global sources and the system sources.
- A pass-level `vcs-unsupported` refusal becomes every member's verdict, and W's device is not sampled.
- Otherwise W's device is sampled once.

`session.observe(member, work)` then runs one member's placement and layout, with exactly `observe_members`' steps and charges. `observe_members` is now `begin`, then `observe` for each member. **Its verdicts and charges are unchanged,** and every B3-b1 control still passes. The decision core's per-candidate `member_verdict` (B3-b2b1) goes through one session per decision (B3-b2b2b).

## Controls

- **`a_retained_proof_needs_the_very_chain_item_6a_walked`:** the same directory, walked twice, is two chains. Each gets the proof only from its own observation, and the two observations compare equal.
- **`no_retained_proof_for_a_repository_or_a_replacement_at_the_same_spelling`:** W in a repository gives no proof. A replacement repository at W's spelling never gets W's proof, nor one of its own.
- **`the_session_gives_observe_members_verdicts_and_charges_one_member_at_a_time`:** three members, one refused. The session's verdicts and ledger charges equal `observe_members`'. Under a pass-level refusal (`GIT_DIR` set) the verdicts are refusals and the charges are still equal.
- **`the_operation_gives_item_6b_its_precondition_from_its_own_subject`:** for an eligible root and a fresh registration, after the fence is released.
- (r2) **`the_chain_identity_allocator_never_reuses_an_identity_at_its_end`.**

## Lead decisions

- **LD-B3B2B2A-1. The allocator never reuses an identity (r2).** It is a checked, never-wrapping allocator. At exhaustion the walk fails closed through the host I/O row, so no public refusal code is added for an unreachable state. **Rejected (r1):** a wrapping counter justified only by infeasibility.
- **LD-B3B2B2A-2. The identity stays out of the recheck's equality** (above). **Rejected:** comparing it, which would be redundant at every site and would make item 6a's unchanged behaviour an argument rather than a fact.
- **LD-B3B2B2A-3. rustfmt.** `git_tracking.rs`, `operation_handoff.rs` and `project_chain.rs` are not rustfmt-clean at the base, so they are not reformatted. The test files are.

## Checks

Lane r2, `evidence/b3b2b2a-checks-r2/`:
- the security suite at base and candidate, with equal failure sets (the 14 pre-existing failures) and five new tests;
- the equality projection: both census files change only at `closure/2`, and the held-out rows stay outstanding;
- rustfmt on the base-clean edited files;
- Clippy, warnings denied;
- the `git_tracking`, `discovery_`, `workspace_declarations` and handoff tests;
- every discovery vector check, FW-01, walk storage, the census controls and the census `--check`;
- the environment exceptions, operability and verify_design.

**Mutations,** each caught by the `git_tracking` tests:
- the proof ignoring the identity;
- the proof ignoring the tracking verdict;
- the identity reused for every chain (the counter never advancing);
- (r2) the allocator wrapping;
- the recheck equality comparing the identity;
- the session ignoring a pass-level refusal.

## Not claimed

- No native observation, composition or caller of the session or the precondition (B3-b2b2b).
- No new paths, so no inventory successor.
- No qualification.
