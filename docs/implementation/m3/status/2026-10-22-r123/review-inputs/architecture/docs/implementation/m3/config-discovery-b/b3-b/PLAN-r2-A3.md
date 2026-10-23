# B3-b plan r2, amendment A3: B3-b2b2 in three steps

**Lead plan amendment, 2026-10-17. Unreviewed.** It amends the accepted B3-b plan r2 (`PLAN-r2.md`), as amended by A1 (`PLAN-r2-A1.md`, Codex `codex-b3b2a-r1`) and A2 (`PLAN-r2-A2.md`, Codex `codex-b3b-plan-a2-r2`). Law M3-B r9 is unchanged.

**Bound so far:**
- B3-b2a, at product `58d450c`;
- B3-b2b1, at product `167ab6a`, the decision core, with its inventory v205 at lock `46c0ebb`.

## A3-1. B3-b2b2 in three steps

A2-1 defines B3-b2b2 as five pieces:
- the native observation;
- item 6b over the counted candidates;
- the NoRepository binding across the operation handoff;
- the composition with `workspaceDeclarations` serialized;
- section 3's T2 link-map controls and the joint sweep.

Under A3 these are delivered in three steps. **Every obligation of A2-1's B3-b2b2 stays, and lands in one of them.**

### B3-b2b2a: the item-6b session and the handoff binding (`git_tracking.rs`, `project_chain.rs`, `operation_handoff.rs`)

- **A process-unique `ProjectChain` identity.** A private, never-reused `u64` is drawn from a process-wide counter when `walk_project_chain` builds the chain. `ProjectChain` stays non-`Clone`.
  - Item 6a's `observe_tracking` records it in `TrackingObservation`.
  - The observation's equality, which `recheck_tracking` compares, stays the tracking verdict and the evidence only. **Item 6a is unchanged.** Its every recheck site already re-observes the same retained chain: the admission's, or the registered project's, moved and not re-walked.
- **`NoRepository::retained(chain, observation)`.** It is the proof for a chain whose identity equals the observation's, when the observation is `NoRepository`. This binds a retained object, not a label (Codex B3B1-R2-RF-1), once the chain and the observation are stored apart. `RootObservation::no_repository` stays.
- **`OperationHandoff::member_precondition()`.** It builds that proof from the subject's own pair: `Eligible { admission, tracking }`, or the registered project's chain and tracking.
- **The item-6b session (A2 r2's "pass-level sources once").** `MemberSession::begin(inputs, proof, work)` checks the environment, the global sources and the system sources once. `session.observe(member, work)` then gives one member's verdict, so the decision core's per-candidate `member_verdict` (B3-b2b1, Codex B3B2B1-R1-RF-2) costs one pass-level check per decision. `observe_members` becomes `begin`, then `observe` for each member, with its verdicts and charges unchanged. B3-b1's controls stay.
- **Census.** `project_chain.rs` is a closure file, so A1-2's re-pin and equality projection apply.

### B3-b2b2b: the native observation and the composition

- **The native `WorkspaceObservation`,** on the discovery ledger, from the lent `DiscoveryRoot`:
  - no-follow opens from W, segment by segment;
  - each entry by an accounted by-name observation;
  - the ACL captured, with the premise, where the metadata-only judgment passes, as the walker captures (LD-B3B2B1-6);
  - positive lookups of `.git`, `.hg`, `.svn` and `.jj`;
  - listings converted as the walker converts them;
  - bounded 4 MiB reads with the accounted capture;
  - a path seen twice must be the same object.

  Host I/O and exhaustion fail the discovery. Custody and placement verdicts are values, decided outside charged scopes so they never latch (B3-b1's lesson).
- **`member_verdict`** goes through B3-b2b2a's session, under the handoff's proof.
- **`discover_with_members`:**
  - phase one;
  - branch A's trial walk with the provisional members (B3-b2a's walker), then phase two;
  - branch B, or W in a repository, with the decided members;
  - for a member-rule refusal, the walk with no members and the refusal record (with `PROJECT.SCOPE_LIMIT`'s D9: request-rejected, exit 2, `REQUEST.UNSATISFIABLE`);
  - the complete `DiscoveryProvenanceV3`, with `memberRepositories` rows (path and `declaredBy`), `memberConfigs` and `workspaceDeclarations`, spelled under W. The pending shape is removed.
- **The scenario path** calls it.
- **Census.** The census closure files this touches are re-pinned under A1-2:
  - `discovery_scan.rs`, for the completed provenance;
  - `custody.rs`, if a declaration is added.
- **Controls:**
  - real scratch trees with synthetic conventional `.git` members, and real carriers and manifests, for both readers and both branches;
  - root-in-repository;
  - the access record of the native observation against the decision core's;
  - non-latching refusals.
- **Vectors.** Pass two's records stay B3-b2a's member vectors. The decision stays B3-b2b1's vectors. The composition is compared with B3-b0's complete result over the same trees: the result as `discover` returns it, with `memberRepositories` rows and `workspaceDeclarations`.

### B3-b2b2c: section 3's T2 link-map controls and the joint sweep, unchanged

- **(a)** The `vcs: none` reconstruction of each lead-readable T2 workspace, from the pinned store manifests and the overlay's carrier. The link stage runs with the overlay's members supplied through the test-only seam at the link stage (plan r2 NBO-1; never a production placement bypass). The derived links must equal the overlay's map, by `overlayDigest`.
- **(b)** The same reconstructions, with each member given a synthetic conventional `.git`, through the unchanged product discovery.
- **The joint sweep.** The P3 fixture, extended with members, runs through the walker and B2-c1's native unit instrument. A removed member refuses `native.boundary-inventory-mismatch`.

Held-out workspaces are never read.

## A3-2. Why

- **The binding is a security boundary** that has needed two review rounds already (B3-b1 r2 and r3). It deserves a review of its own, against unchanged item 6a.
- **The native observation and composition** are I/O, custody and ledger work over an accepted decision core.
- **The T2 controls** are data reconstruction over the store and overlays.

Each is one subject. **Rejected:** one B3-b2b2 unit, which would mix all three, plus two closure re-pins.

## A3-3. Steps (section 5, as amended by A1 to A3)

1. B3-b0, B3-b1, B3-b2a and B3-b2b1 (bound).
2. **B3-b2b2a, then B3-b2b2b, then B3-b2b2c,** each followed by its inventory where it adds paths.
3. B3-b3a, B3-b3b and B3-b3c, as section 4.3 and A2-3 step 4 state, with A2's carried observation that placement and listing charges are paid at zero members.
4. The status round.
