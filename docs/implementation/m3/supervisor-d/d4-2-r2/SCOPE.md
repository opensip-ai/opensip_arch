# D4-2 r2: the trust owner's admission view and the host's R10a adapter (M3-D r5 item 24)

**Unreviewed candidate round 2, 2026-10-18. It needs Codex review.** It implements sub-unit D4-2 of the D4 implementation plan r2 (`../d4/PLAN-r2.md`, accepted in `codex-d4-plan-r2`; lead assent `reviews/codex-d4-plan-r2/lead-assent.json`): LD-D4-2, LD-D4-3, LD-D4-4, LD-D4-12 and LD-D4-13, with §5's D4-2 controls. It stacks on D4-1 (r3, integrated at `114d2ac`) and on CI-2/CI-3 (integrated at `d113fa7`), as the plan's §6 ordering note requires: both change `trust_admitted_components.rs`.

**Product base:** `4e475c753002d21ed99e0d53e64218e55af0cb1f` as the completed takeover lane records. **Worktree:** `/Users/sb/code/opensip-ai/opensip-d4-2`. **Changed:** see `product-map.json`. There are two new paths, `crates/host/src/component_admission.rs` and its tests, and eleven changed ones.

## Initial takeover test repair and first completed lane (history)

The earlier saved lane `d4-2-checks-r1b` retained two surviving mutations. It remains a failed historical attempt; its checks, controls and the two relevant logs are archived under `evidence/prior-failed-lane/`.

Only the host test source changed during takeover. The allocation guard now counts `::with_capacity(`, including explicitly typed vector allocations. A new behavioral control admits a validated analyzer with a root and a child carrying its parent, with the child's spelling reserved only at the root namespace. The cleared digest must equal the body digest. Dropping the child's parent now manufactures a second root and fails that control. Original test bytes and the repair rationale are archived; production candidate code is unchanged by the repair.

The new complete lane has all required rows passing: security 1281 baseline / 1283 candidate with the same 14 inherited failures, and host 418 baseline / 427 candidate with the same nine inherited failures. That is two added security controls and nine added host controls, not a claim that either whole suite is failure-free. Formatting, warning-denied all-targets Clippy, workspace/feature/release checks, package edges, focused controls, environment/operability/census/design checks pass. All thirteen unchanged mutations are caught by runtime test failures, including the two prior survivors; compilation failure is not credit. No product qualification follows.

## Round 2: D4-2-R1-RF-1 resolved

CODEX2 found that the original sorted-slice logarithmic price did not cover actual BTreeMap comparisons. The member lookup now charges max(number of object keys, 1) before get, a conservative all-keys bound for the pinned implementation's disjoint root-to-leaf node scan. This changes only the host adapter and its tests; the other eleven candidate files and the pinned product base remain byte-identical to round 1. D4-1's sorted-slice policy and all public interfaces remain unchanged. The local Rust implementation pin and proof are in evidence/takeover-repair/lookup-bound-proof.json.

The tenth host control uses the actual nine release-row key names, covering publisher, sourceClass and the final version key. Nine edges funds the lookup; eight refuses before get, with zero partial charge and a latched ledger. The complete source-order guard pins the precharge before the single get site. A new lookup-underpriced mutation restores the old five-edge price and must fail that control at runtime.

The r2 lane deliberately reuses the exact unchanged r1 baseline and security-suite evidence. reused-evidence.json records the base, the two changed host paths and the unchanged security closure; the original full lane is archived in the first submission. The host candidate suite is fresh (418 baseline / 428 candidate passes, with the same nine inherited failures); security retains its original 1281/1283 passes with the same fourteen inherited failures. All ordinary checks and all fourteen mutations are fresh and pass. No new whole-suite, qualification or production-composition claim follows from the evidence reuse.

## 1. What it delivers

- **The reader keeps its reserved set (LD-D4-13).** `trust_ordinary_metadata.rs`'s ordinary reader moves its `reserved_names` set (`reservedRootCommands`, :91) into its `Evidence` after the loop. It is the very set every manifest was validated against, never rebuilt.
- **The admission view (LD-D4-2, LD-D4-3).** The public `AdmissionView<'a>` (`trust_admitted_components.rs`) holds each verified component as C2a-1's bridge lends it (`AuthenticatedComponent`), and borrows the reserved set.
  - Only the trust owner builds one, through `Evidence::admission_view(work)`. Its one allocation is charged first, at `admission_view_cost(n)`. Under the joint fixture predicate, `AdmissionView::fixture` also builds one, for tests.
  - It exposes `components()` and `reserved_roots()` (ascending).
  - A component's provenance is its catalog **release row**, the root-authenticated association. It is not Clone and authorizes nothing.
- **The host adapter** (`crates/host/src/component_admission.rs`, `judge(view, work)`) projects the view into D4-1's borrowed `ManifestClaims`, builds the `AdmissionPolicy` and runs `manifest::admit`.
  - **The policy** is the reader's reserved list, `PROVIDER_RELATIONS` and `EXPLICITLY_TRUSTED`.
  - **`PROVIDER_RELATIONS`** is the static, pinned nine-pair projection of the embedded matrix (LD-D4-4).
  - **`EXPLICITLY_TRUSTED`** is empty at M3 (LD-D4-3).
  - **Provenance** (`publisher`, `sourceClass`) is read from the release row, and so is the digest (`manifestDigest`).
  - **The projection** comes in three charged passes: the fields and sizes; every alias spelling into one exact list, plus each capability's relation and rung; then the commands, slicing those spellings, and the claims.
  - **Refusals** are typed. `AdmissionFailure` is `Excluded`, `Invariant(Judge | Policy | Projection)` or `Budget`.
- **The package edge** `opensip-host → opensip-components`, which inventory v229's `opensip-host` row permits, with its `Cargo.lock` line.
- **Fixture gate 9, added by name.** The admission view's fixtures are named as shared fixture gate 9 in `crash_matrix_sites.rs`'s pinned site list, as gates 6 to 8 were (law X9 r1 item 6; law X8 r3 item 4b, "one site list, one joint predicate, extended by name"). It adds five joint sites: two in `trust_admitted_components.rs`, and one each in `root_payload.rs`, `trust.rs` and `lib.rs`.
- **The fixtures (LD-D4-12).**
  - `root_payload.rs`'s `admission_fixture_bodies()` (an append) is C2a-2's every-role bodies plus an analyzer at 1.0.5 whose provenance says `explicitly-trusted`.
  - `component_fixtures.rs`'s release rows now take `publisher` and `sourceClass` from the body's own provenance, not a literal, so that analyzer's signed release row says so. Every pre-existing body is `opensip`/`first-party`, so their rows' bytes are unchanged; C2a-2's byte-for-byte tests still pass.
  - The public `admission_fixture_components()` (joint predicate) gives the host's tests those six bodies as `TestComponent`s, through the real body validation, with release rows built from the body.

## 2. Decisions within the plan (ID-D4-2-n)

- **ID-D4-2-1. The end-to-end chain is two controls joined by one public type.** The ordinary reader is internal to security, with no public entry yet; R10's trust-view API is J3d's. The judge lives in components, which security cannot depend on. So:
  - **security's control** runs the real ordinary reader over the six signed bodies. It shows the reader admits all six, including the signed `explicitly-trusted` analyzer. The view lends each release row's provenance, equal to the body's, so exactly one says `explicitly-trusted`. The view borrows the reader's own reserved set, by pointer identity.
  - **host's control** runs the same public `AdmissionView` (fixture-built over the same six bodies) through the adapter and the judge. The explicitly-trusted analyzer refuses EE-1, and the five others clear.

  No single test spans the reader and the judge (§5).
- **ID-D4-2-2. Lookups in the validated value are charged at a published bound.** Each member lookup in a validated JSON object is charged `max(len, 1)` edges before it is made. In pinned Rust 1.95, a root-to-leaf B-tree lookup tests keys in disjoint nodes without revisiting them, so it performs no more than len key comparisons; an empty lookup retains one edge for its empty check. This declared bound is conservative, not an executed-count claim. D4-1's logarithmic sorted-slice price is unchanged and does not price this map. Each spelling comparison (role, source class), each hex byte decoded and each push into a funded vector is one edge, charged first.
- **ID-D4-2-3. A validated value missing a required field** is `Invariant(Projection)`, a host invariant. Security's shape validation makes it unreachable.

## 3. Controls

- **security (`trust_bootstrap_tests.rs`):**
  - `d4_2_the_admission_view_lends_the_release_association_and_the_readers_reserved_set`: the real reader over six signed bodies; the view's charge (objects 1, bytes `6 · size_of::<AuthenticatedComponent>()`); provenance from the release row; one `explicitly-trusted` and five `first-party`; the reserved set by pointer identity; one unit short of the allocation refuses `Budget`, with nothing charged;
  - `d4_2_the_admission_views_allocation_follows_its_charge`: the source guard on the view's one allocation.
- **host (`component_admission_tests.rs`):**
  - the provider table against the embedded matrix, member by member and in order, with the `fact` and `candidate-only` members excluded;
  - every role clears, in digest order;
  - a lawful child command retains its explicit parent and stays outside the reserved root namespace;
  - a lawful child command retains its explicit parent and stays outside the reserved root namespace;
  - the explicitly-trusted analyzer refuses EE-1, alone;
  - provenance comes from the release row: a first-party body joined to an explicitly-trusted row refuses EE-1;
  - the reader's reserved list is the one judged: reserving the fixtures' name refuses EE-5a (c) for all five, and an empty list clears them;
  - the no-trust-view case;
  - late nine-key release lookups funded at nine edges and refused one unit short, with no partial charge and a latched ledger;
  - every short allowance refuses `Budget` (objects and edges), and the exact allowance clears;
  - the source-order guards: the one allocation inside `reserve` after its charge, including explicitly typed `Vec::<T>::with_capacity` sites; the one lookup inside `member` after its charge; each of the seven pushes, both spelling comparisons and the hex-byte decode after their one-edge charges.
- **Mutations** (`evidence/takeover-repair/run_d4_2_checks_r2.py`, 14). Each must fail the focused tests, never by a compile error:
  - the reserved list not passed;
  - a same-size substitution in the provider table;
  - provenance read from the body;
  - a non-empty explicit-trust list;
  - a push before its charge;
  - an allocation before its charge;
  - a lookup uncharged;
  - the map lookup underpriced at the former logarithmic sorted-slice bound;
  - a role compared before its charge;
  - the digest decoded wrong;
  - the command parent dropped;
  - the reader's reserved set rebuilt;
  - the view's allocation uncharged;
  - the fixture release identity hard-coded.

## 4. Self-review (`/tmp/opensip-implementation/PRE-SUBMISSION-CHECKLIST.md`)

1. **Charge before work, and prove the order.** Every allocation goes through `reserve`, every member lookup through `member`, and every push, spelling comparison and hex byte follows its own one-edge charge. The view's one allocation follows its charge.
   - **The proof:** the host's complete source-order guard (`d4_2_every_work_site_follows_its_charge`) and the security guard, with mutations moving a push, an allocation and a comparison ahead of their charges. No operation-order oracle is used here; the complete guards are the alternative the checklist allows.
   - **Owned copies:** none. Every string is borrowed from the validated value or the release row. The fixture function's copies are under the joint fixture predicate only.
   - **Not charged, stated:** length and index bookkeeping on local vectors (`raw.len() != 64`, the slice-range sums in pass 3, the `saturating_add` counters).
2. **Exact charges vs bounds.** Pushes, spelling comparisons and the hex decode are exact executed counts. A member lookup is charged at the declared map-key bound for its object's size (ID-D4-2-2): a bound, stated as one, not an exact count. Nothing else is precharged.
3. **System-call error conventions:** not applicable (no system call).
4. **Pinned-source equality.** `PROVIDER_RELATIONS` is checked against the embedded matrix member by member, in order, so a same-size substitution (a mutation) and a source-side addition both fail. `EXPLICITLY_TRUSTED` is pinned empty.
5. **Immutable context pins.** The authorities are the accepted D4 plan r2, with its review and assent; the integrated D4-1 r3 and CI-2 r2 units; and M3-D r5.
6. **Time and measurement provenance:** not applicable.
7. **Failure latching.** A refused charge returns `Budget` at once, and the ledger latches. The adapter keeps no state.
8. **Disclosure, the untested paths:**
   - no single test spans the real reader and the judge (ID-D4-2-1);
   - `Invariant(Projection)` (ID-D4-2-3) and `Invariant(Policy)` are not executed, since validated values and the pinned slices cannot reach them;
   - the production caller (R10a's wiring: J3d, J2c, with C2a-4) and D4-T1's path half are later units;
   - the reserved-root list in the signed catalog fixtures is empty (the shared catalog literal). So the reserved set's identity is shown by pointer equality over the real reader, and its effect is shown by a non-empty list in the host's fixture view.
9. **Mutations.** All 14 must be caught by failing tests; the lane checks each one.

## 5. Not claimed

- No production caller.
- No trust-view API (J3d's).
- No D4-T1 path half (J-C10b).
- No profile (LD-D4-SD9).
- No record or envelope (LD-D4-9).
- No product qualification.

## 6. Inventory

Two new paths: `crates/host/src/component_admission.rs` and `component_admission_tests.rs`. After integration, an additive inventory successor (`/tmp/opensip-implementation/prepare_d4_2_inventory.py`) adds both rows. The changed paths' inherited descriptions are judged in that round.
