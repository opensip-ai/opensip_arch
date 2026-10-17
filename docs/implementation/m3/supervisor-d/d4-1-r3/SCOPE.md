# D4-1 r3: the manifest-class excluded forms, `crates/components/src/manifest.rs` (M3-D r5 item 24)

**Unreviewed candidate, round 3, 2026-10-17. It needs Codex review.** It implements sub-unit D4-1 of the D4 implementation plan r2 (`../d4/PLAN-r2.md`, accepted by Codex in `codex-d4-plan-r2` with NBO-1 carried; lead assent `reviews/codex-d4-plan-r2/lead-assent.json`). The law is M3-D r5 item 24 (`../PROPOSAL-r5.md`:752-825), with D4-T4 and D4-T1's interface half.

**Product base:** main at the lane's start, as `source.json` and `checks.json` record it. **Worktree:** `/Users/sb/code/opensip-ai/opensip-d4-1`. **Changed:** `product-map.json`. The changed paths are:
- `crates/components/src/manifest.rs` (new; it realizes the inventory's planned row);
- `crates/components/src/manifest_tests.rs` (new);
- `crates/components/src/lib.rs` (base-clean; one module declaration, and the crate doc's "nothing here admits a manifest" made exact).

## r3 changes (answering `codex-d4-1-r2`; narrow)

| Item | Disposition | Where |
| --- | --- | --- |
| **D41-R2-RF-1** (observe the boolean predicate's evaluation, not only `tested()` receiving its result) | **Fixed.**<br>**The lazy predicate.** `tested` now takes the predicate as a closure, `tested(|| …)`, records `Compared`, and only then evaluates it, so the predicate's work happens inside the observed wrapper.<br>**The guard against a precomputed captured boolean.** The new test `rf1_every_predicate_is_evaluated_inside_its_wrapper_after_its_charge` pins all five `tested` call sites:<br>- each is exactly a closure over the claim itself (`tested(|| true)` for the empty probe; `tested(|| claim.provenance.source_class == SourceClass::ExplicitlyTrusted)`; `tested(|| claim.role != Role::Analyzer && claim.commands.is_some())`; `tested(|| command.parent.is_none())`; `tested(|| root.is_some_and(|r| r.name != claim.name))`);<br>- each is on the line immediately after its `compare(work)?;`;<br>- each predicate's operands (`SourceClass::ExplicitlyTrusted`, `commands.is_some()`, `parent.is_none()`, `r.name != claim.name`) occur exactly once in the module's production source.<br>A predicate computed before its charge and passed as `tested(\|\| stored)` changes the pinned line and fails this assertion, not the compiler.<br>**Mutations:** four are added, one per predicate site: the predicate precomputed before `compare(work)?` and captured, with `tested` still after it (`codex-d4-1-r2`'s counterexample for EE-1, and the same pattern for EE-5a's (a), (b)-entry and (b)-name tests). The three mutations anchored on `tested` are re-anchored to the closures. That makes 32 in all. | `manifest.rs` (`tested`, and its five calls); `manifest_tests.rs`; `evidence/run_d4_1_checks.py` |

Round 2's accepted parts are unchanged: the wrappers `charge`, `ordered` and `reserve`, the oracle, its grammar, the exact totals, the per-site prefixes, the source-order guard, the capacity checks, and every round 1 and round 2 mutation. Rounds 1 and 2 (`../d4-1-r1/`, `../d4-1-r2/`) are history and are not edited.

## Self-review (the lead's pre-submission checklist, `/tmp/opensip-implementation/PRE-SUBMISSION-CHECKLIST.md`)

1. **Charge before work, and prove the order.** Every allocation (the two index buffers, the refusal vector, the `Cleared` list), judged comparison (the sort, the duplicate pass, the policy order checks, the probes) and judged predicate evaluation (EE-1's class test; EE-5a (a), (b)'s entry and name tests) is charged before it runs. **The proof:** the operation-order oracle and its grammar, the per-site short allowances with no work past the refused site, the source-order guard on `charge`, `reserve`, `.cmp(` and the pushes, and r3's predicate guard. The mutations cover a comparison moved ahead of its charge (four sites), an allocation moved ahead of its charge (three), and a predicate precomputed and captured (four).
   - **Owned copies:** none. The module copies no string or name; each digest is a `[u8; 32]` value pushed into a funded, exact-capacity vector.
   - **Digests:** none computed.
   - **Not charged, stated:** index and counter bookkeeping is uncharged control flow on indices and lengths the module holds, not a judged comparison of claim data. That covers the loop bounds (`low < high`, `width < len`, `i < mid && j < high`), `slice.is_empty()`, `roots != 1` and `windows(2)`. This is the accepted C2a-1 merge-sort precedent. Also uncharged is the analyzer dispatch `claim.role == Role::Analyzer`, which follows (a)'s charged test of the same field. LD-D4-10's accepted prices charge none of these.
2. **Exact charges vs bounds.** The charges are exact executed counts: the comparisons the sort and the probes actually make. `sort_reference_comparisons` and `probe_reference_comparisons` are separate published upper bounds, checked to dominate by `rf1_reference_bounds_dominate_the_model`. Nothing is precharged.
3. **System-call error conventions:** not applicable (no system call).
4. **Pinned-source equality.** The CMS pin compares each property set as an exact ordered list, so a same-cardinality substitution or an addition fails. `ExcludedFormClass`'s six members are pinned by an exhaustive match and their order. The test's nine provider pairs are a test-local input; the host's pinned projection of the embedded matrix is D4-2's (LD-D4-4).
5. **Immutable context pins.** The authorities are published or accepted bytes: M3-D r5, the D4 plan r2 with its review and assent, and J1 r7. The prior rounds' subjects are submitted bytes.
6. **Time and measurement provenance:** not applicable.
7. **Failure latching.** A refused charge returns `Budget` at once, and the platform ledger latches: every later charge on it refuses (`work_ledger.rs`). The module keeps no state across calls.
8. **Disclosure, the untested paths:**
   - `Refusal::Invariant(TooManyClaims)`, more than `u32::MAX` claims, is not executed;
   - the non-test `note`, a no-op, is compiled in the release build but not exercised by a test;
   - D4-T1's path half (J-C10b) and every production caller (D4-2, J3d, J2c) are later units;
   - no executed EE-4 negative exists, since EE-4 has no carrier;
   - no Linux-specific behaviour exists, since the module is platform-free.
9. **Mutations.** All 32 are caught by failing tests, never by a compile error. They cover:
   - **item 1:** work ahead of its charge, allocations ahead of theirs, and precomputed predicates;
   - **item 2:** removed or under-priced charges, and the grown vector;
   - **item 4:** the class order swapped.

   Item 7 has no module state to mutate.

## r2 changes (answering `codex-d4-1-r1`; history)

| Item | Disposition | Where |
| --- | --- | --- |
| **D41-R1-RF-1** (verify that exhaustion precedes work, not only the ledger prefix) | **Fixed with an operation-order oracle and a source-order guard.**<br>**The wrappers.** Every charge goes through `charge`, which records `Charged(cost)` only after the ledger accepts it. Every judged comparison goes through `ordered` or `tested`, which record `Compared` where the comparison is made. Every allocation goes through `reserve`, which records `Allocated`. Each `Cleared` push records `Pushed`. The record is a `#[cfg(test)]` thread-local, armed by the test; nothing is recorded in any other build.<br>**The grammar** (`blocks`): the log must be a sequence of blocks, each a charge followed by exactly the work it funds (two allocations for the index buffers, one for a result, one comparison or push for an edge), with no work outside a block.<br>**The accounting test** (`accounting`) checks that the oracle's charges equal the independent model's in order. Then, at **every** site, a scope one unit short gives `Budget`, the ledger's `used` stops before the site, and the oracle's blocks stop exactly before it. So **no work at or past the refused site occurred**, which the ledger prefix alone could not show. This covers both predicate passes, the sort, the duplicate pass, the probes and the result allocations.<br>**Policy order checks** have their own oracle and per-site test (`rf1_policy_order_checks_charge_before_each_comparison`).<br>**The source-order guard** (`rf1_every_site_goes_through_its_recording_wrapper`) pins that the production source has exactly one raw `work.charge`, one `Vec::with_capacity` and one `.cmp(`, each inside its wrapper, and its three pushes, so no site escapes the oracle.<br>**Capacity:** the refusal vector and the `Cleared` list are asserted to have capacity equal to their length.<br>**Mutations:** the 20 round-1 mutations stay, re-anchored to the wrappers, and 8 are added: a probe's, the policy check's, EE-1's and the duplicate pass's comparison made before its charge (`codex-d4-1-r1`'s named counterexample); each of the three allocations made before its charge; and the refusal vector grown instead of reserved (the plan's count-pass mutation). | `manifest.rs` (the wrappers); `manifest_tests.rs`; `evidence/run_d4_1_checks.py` |
| What each control proves | **Exact total:** every charge's amount, against the independent model. **Oracle charges equal the model:** their order. **The oracle grammar:** each piece of work follows its own charge. **Per-site short allowance:** the ledger prefix, and no work at or past the refused site. **Source guard:** every site is visible to the oracle. **Capacity:** no hidden growth. | §3 |

Round 1's accepted parts are unchanged: the predicates, their order, the projection, the policy, the prices and the closed-world pins. The only production change is that each site now goes through its recording wrapper, and the comparisons are written through `ordered` and `tested` with the same results. Round 1's package (`../d4-1-r1/`) is history and is not edited.

## 1. What it delivers

- **The projection** (LD-D4-2): `ManifestClaims<'a>` with `ReleaseProvenance`, `CommandClaim` and `CapabilityClaim`, pure borrowed data that components never parses. The host builds it in D4-2.
- **`AdmissionPolicy::new`:** three sorted, unique borrowed slices (`reserved_roots`, `provider_relations`, `explicitly_trusted`), each checked strictly ascending at one charged comparison per adjacent pair. An unordered slice refuses `PolicyRefusal::Unordered(slice)`.
- **The predicates, in class order:**
  - **EE-1** (LD-D4-3): `explicitly-trusted` and not on the list. The provenance is the release association's.
  - **EE-3b** (LD-D4-4): a claimed `(relation, rung)` absent from the provider projection, the first unmatched capability refusing.
  - **EE-4:** no carrier, so no predicate (LD-D4-5).
  - **EE-5a** (LD-D4-6), the first arm that holds:
    - (a) a closure-only role with `commands` at all;
    - (b) an analyzer without exactly one parentless entry, or whose root is not named for it;
    - (c) a reserved root key, among the name, the aliases and the analyzer root's aliases.
- **`ExcludedForm {class, arm, manifest_digest}`.** `ExcludedFormClass` has the six members in the one documented order. `Arm` is an internal key.
- **`admit`** (LD-D4-8):
  1. two `u32` index buffers, charged;
  2. a bottom-up merge sort by digest, one edge before each comparison;
  3. a charged adjacent-duplicate pass, refusing `Invariant(DuplicateDigest)`;
  4. a count pass, then either the exact refusal vector and an identical fill pass (`Refusal::Excluded`, by digest then class), or the exact `Cleared` list with one edge per digest.

  More than `u32::MAX` claims refuse `Invariant(TooManyClaims)` before any charge.
- **The prices** (LD-D4-10): every charge is made before its work. A probe is a charged binary search: one edge per comparison, or one for an empty slice. The published reference bounds are `sort_reference_comparisons(n) = n·⌈log₂ n⌉` and `probe_reference_comparisons(m) = ⌈log₂ m⌉ + 1`. Arithmetic in the cost functions saturates, so an overflow is refused by the ledger, never wrapped. Exhaustion is `Refusal::Budget`, never a partial result.

## 2. Decisions within the plan (ID-D4-1-n)

- **ID-D4-1-1. One judge, two passes.** `judge` is the single per-manifest predicate. The count pass and the fill pass both call it with a different sink, so their charges are identical by construction, and the vector is allocated at exactly `k`.
- **ID-D4-1-2. One form per class per manifest.** EE-3b stops at the first unmatched capability, and EE-5a takes the first arm in the order (a), (b), (c). The charges stop with it, the same in both passes.
- **ID-D4-1-3. `Arm` is internal.** It names which arm refused, for the operational record's key, which J1's projection owns (LD-D4-9). It is not a public code.
- **ID-D4-1-4. An analyzer with no `commands` member** is EE-5a (b): zero parentless entries. CMS requires `commands` for an analyzer, so this is a backstop.

## 3. Controls

- **D4-T4 at D4's interface:**
  - every role's positive case;
  - (a) with a non-empty and an empty tree;
  - (b) with two roots, a misnamed root, no root and no `commands`;
  - (c) by the name, a manifest alias and a root alias.
- **D4-T1's interface half:**
  - EE-1 with an empty list, an unlisted publisher and a listed one, and first-party with a list;
  - EE-3b with the `fact` relations (`inventory`'s three, `clones-fact`'s) and a wrong rung refused, and each of the nine provider pairs passing;
  - the digest-then-class order of every form under four input orders;
  - the sorted `Cleared` under three orders, and the empty set;
  - `DuplicateDigest`;
  - each policy slice unordered; empty policy slices.
- **RF-1's independent accounting** (with r2's oracle, above): the test's own model (`model`) computes, from the input, every charge `admit` must make, in order. It uses its own merge sort and binary search to count comparisons, and the types for sizes. For cleared and refused sets in several orders, with several classes on one manifest and with non-empty trust lists:
  - the ledger's total equals the model's exactly;
  - for **every** charge site, a ledger one unit short of it refuses `Budget`, and its `used` equals the charges before the site, so nothing is charged at or past it.

  A separate test checks the reference bounds dominate the actual comparison counts.
- **The closed-world pins** (LD-D4-5):
  - CMS's top-level and `provenance` property sets, each `capability` branch with its `declarationData`, `platform`, each `entry` branch, `command` and `dependency`, read from the pinned `tools/security/inputs/manifest-schema.json`;
  - exhaustive patterns over `ManifestClaims` and its nested claims, and over `ExcludedFormClass`'s six members and their order.
- **The operation-order oracle and the source-order guard** (r2; the r2 changes table).
- **Mutations** (`evidence/run_d4_1_checks.py`, 28 in r2, 32 in r3). Each must fail the focused tests, and a compile failure never counts. Round 2 adds the comparison-before-charge mutations (a probe's, the policy check's, EE-1's, the duplicate pass's), the three allocation-before-charge mutations and the grown vector. The round-1 mutations are:
  - each arm removed;
  - the explicit-trust probe skipped;
  - EE-3b admitting any relation;
  - (a) judging only a non-empty tree;
  - (b)'s name binding and root count weakened;
  - (c)'s root aliases skipped;
  - the class order swapped;
  - the sort removed;
  - the sort's, the duplicate pass's, a probe's, an empty probe's and the `Cleared` fill's charges removed;
  - the refusal vector under-priced;
  - the vector truncated;
  - the duplicate pass removed;
  - the policy order check removed.

## 4. Not claimed

- **No production caller:** D4-2's host adapter and J3d's and J2c's R10a and ER10a wiring follow.
- **D4-T1's path half.** It is J1's J-C10b, on 3a, 3b × {`Published`, `LostRace`, `NotPristine`} and the ephemeral path with and without a trust view.
- **No executed EE-4 negative.**
- **No profile** (LD-D4-SD9).
- **No public projection or record** (LD-D4-9).
- **No qualification.**

## 5. Inventory

`manifest.rs` realizes its planned row, and `manifest_tests.rs` is new. After integration, an additive inventory successor (`/tmp/opensip-implementation/prepare_d4_1_inventory.py`) realizes the one and adds the other. `lib.rs`'s inherited description stays true.
