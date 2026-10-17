# C1C-PLAN-r4 review

**Verdict: ACCEPT.** No required findings or nonblocking observations. This accepts the implementation plan, not code, integration, a census refresh or product qualification.

## Subject and base verification

Verified the 950-byte manifest, SHA-256 `fe38baf6d718ecc3b1025f4a1e111eace35da39ec0a02afcb4cab4ee0bd0c752`, and all four members:

- PLAN-r4.md: 48,221 bytes, `d066487af5608b0375bd0ba1f8eaefda9b8bdbe70d27d96a875ba43cca8fe835`.
- PLAN-r3.md: 42,023 bytes, `852df6d8b70353a51e4e4ef218dc074d2aa8f12a61bbcd73e281530ce85dded3`.
- PLAN-r2.md: 33,396 bytes, `682088c37c89adf1ca846f91b7caf27b4264cea66876c13c3ad19ae8aaae8186`.
- PLAN-r1.md: 22,877 bytes, `b9c040834b12535cd88f0ea4c6bbf9c2682c5a1507d1fb14dc13698e3ad01eb4`.

The three history members retain their reviewed pins. Live product HEAD `b7538549b727e13013f36d3b7c2e2917e767f3f2` and architecture HEAD `bd77891d106cd40a0e9e33962aee7e9e4ada7505` match the manifest bases.

Git byte comparison confirms the claimed unchanged sources between `3d1d771` and `b753854`: snapshot_walk.rs, discovery_rule.rs, snapshot_source.rs, host snapshot.rs and snapshot_seal.rs, snapshot_ledger_model.py, snapshot_ledger_census.py and discovery_census.py. Also checked discovery_walk.rs, workspace_declarations.rs, identity descriptors.rs, evaluator plan_native.rs and native-v2.schema.json. The base movement changes D2b-0b's generation inputs/outputs and audit plus its design-lock binding, not these authorities.

## C1CPLAN-R3-RF-1: addressed

The split, LD-C1C-8/9/13 and checks consistently assign C1c-0 its retention model/anchor changes, regenerated soundness vectors, fixed-cap/2x evidence and companion-receipt recipe/pin impact before acceptance. C1c-1 extends the accepted recipe instead of deferring or re-pricing C1c-0's work. The former pins-only claim is removed.

The distinction between moving and copying is supported by the inspected implementation:

- Cargo keys are already charged before insertion by key_cost, which delegates to owned: one object, zero edges, key bytes plus the conservative record overhead. Removing a key on frame exit does not refund cumulative work. Keeping that same set and moving it by value into WalkEvidence needs no new key copy or set allocation. The current walk visits a directory path once; retaining keys from completed sibling subtrees does not add another insertion for that same path.
- classify_path tests Cargo membership only for prefixes before target segments of the current path. Each tested prefix is an ancestor. Keeping a completed non-ancestor root cannot create a new matching prefix. Existing path-shaped classification charges do not depend on the number of retained Cargo roots. The proposed identical-classification and exact-charge-equivalence controls are therefore appropriate, including the mutation that copies rather than moves a key.
- Member-root retention is explicitly a new charged copy. MAX_MEMBERS is 64; LogicalPath permits at most 4,096 Unicode scalars, hence at most 16,384 UTF-8 bytes per key. With the inspected owned overhead of 128 bytes, the conservative copy term is at most 64 objects, zero edges and 1,056,768 charged bytes. This is a sourced upper bound for the new member copies, not an assertion that the full future implementation has passed its cap gate.

The model must reflect the changed retention lifetime and member-copy term and pass its native soundness controls. C1c-0's r9 fixed-cap/2x gate remains mandatory; acceptance of this plan does not substitute for that future evidence or authorize raising caps. Directory/Cargo work otherwise assigned to the typed-refusal regime remains there, charged and never truncated.

LD-C1C-9 now distinguishes the discovery_rule.rs whole-file closure re-pin from the snapshot source/model/recipe changes. Both receipt impacts are owned by C1c-0; C1c-1 later changes the companion recipe on that accepted base. This accounting is consistent with the declared changes.

## C1CPLAN-R3-RF-2: addressed

LD-C1C-7 requires at least one eligible retained authorization. Charged preparation records the longest eligible exact-directory prefix as an index into the sorted retained realPath set; sealing checks that admitted prefix, the relative suffix and the retained exclusions by borrowed comparison. It does not require unique coverage and does not reopen sources or allocate during the guard.

The node_modules/a plus node_modules/a/subpackage control now reads and inventories the shared x.ts once, chooses the latter authorization and preserves both manifest digest joins. The exactly-one-coverage and wrong-chosen-prefix mutations directly test the revised rule. Identical-realPath deduplication, per-layout-row digest checks and the single capture remain separate obligations. The fixed-size chosen index and its preparation/search work are explicitly included in C1c-1's term.

The nested-node_modules negative remains: an enclosing package cannot authorize a suffix crossing another node_modules segment. A separately listed nested directory supplies its own eligible authorization. The new overlap rule does not weaken that boundary.

## Regression assessment

No regression identified against rounds 1–3's accepted requirements:

- Full-path VCS, Cargo-output and exact root/member .opensip exclusions retain their evidence sources and no-open/no-reach timing controls. Ordinary lookalikes remain eligible. The shared rule owns the tables; discovery's outermost classification semantics remain unchanged.
- Opaque WalkEvidence comes from the session's own walk. Member-root equality is checked against retained evidence; extent/layout same-root and Plan-selection provenance remain explicit composition preconditions. Dependency-tree Cargo markers are charged no-follow status observations, never extra source reads.
- The walk's exact SnapshotExtent applies before descent, capture reach/origin changes and admission. Ignored/boundary-excluded required manifests remain leftovers. First-party workspace-link manifests keep Walk origin and the existing digest join.
- Capture reuse, observation comparisons, no retry, the custody distinction, raw case-sensitive suffixes, candidate-path grammar, special-file handling, no-layout identity preservation, operational origin outside identity and joint item-5 bounds remain.
- Charged preparation and allocation-free sealing remain separated. The structural guard does not claim to prove host read completeness. Typed refusals and separate Budget failure remain.
- The full cumulative C1c-1 gate includes accepted retention and VCS work plus its own read-set preparation, buffers, observations, row/session work and overlap traversal. Per-layout bounds are not treated as a global layout bound. A no-layout census is not measured read-set evidence; synthetic/native soundness and the fixed-cap derivation remain required.
- Receipt evidence is per receipt and separate from passing generated-output checks. A sub-unit joins an interval only before freeze, otherwise owns a new reviewed interval, including after earlier closed C1b/C1c-0 refreshes. C2b's intervening changes are tracked, earlier refreshes cover no later edit, and dependent work cannot rely on stale receipts.

The preparatory C1c-0/C2b/C1c-1 integration edge, C1b shared-file rebase/anchor duties and Q1–Q5 rulings are retained. The layout resolver and its ledger-routing choices remain separately reviewed C2 work; this acceptance does not decide them by implication.

## Review boundaries

Used only read-only reading, hashing, JSON parsing and Git queries. No Cargo, rustc, builds, tests, lanes, network, panes or delegation. No private fixture, installation directory, signing keys, held trees, T2 stores or cache were accessed. Neither repository, worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
