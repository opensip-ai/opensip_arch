# D4-1 r2: the manifest-class excluded forms, `crates/components/src/manifest.rs` (M3-D r5 item 24)

**Unreviewed candidate, round 2, 2026-10-17. It needs Codex review.** It implements sub-unit D4-1 of the D4 implementation plan r2 (`../d4/PLAN-r2.md`, accepted by Codex in `codex-d4-plan-r2` with NBO-1 carried; lead assent `reviews/codex-d4-plan-r2/lead-assent.json`). The law is M3-D r5 item 24 (`../PROPOSAL-r5.md`:752-825), with D4-T4 and D4-T1's interface half.

**Product base:** main at the lane's start, as `source.json` and `checks.json` record it. **Worktree:** `/Users/sb/code/opensip-ai/opensip-d4-1`. **Changed:** `product-map.json`. The changed paths are:
- `crates/components/src/manifest.rs` (new; it realizes the inventory's planned row);
- `crates/components/src/manifest_tests.rs` (new);
- `crates/components/src/lib.rs` (base-clean; one module declaration, and the crate doc's "nothing here admits a manifest" made exact).

## r2 changes (answering `codex-d4-1-r1`)

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
- **Mutations** (`evidence/run_d4_1_checks.py`, 28 in r2). Each must fail the focused tests, and a compile failure never counts. Round 2 adds the comparison-before-charge mutations (a probe's, the policy check's, EE-1's, the duplicate pass's), the three allocation-before-charge mutations and the grown vector. The round-1 mutations are:
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
