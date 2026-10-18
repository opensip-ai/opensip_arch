# Review: D4-2 r1

**Verdict: REQUIRED-FINDINGS**

The frozen subject manifest has the requested SHA-256 (`ce39894126d80d8e4404f242b873b45c361e2c1f52e7b10f4351eb6c49eac127`). All 61 listed members match their recorded sizes and digests, and every declared source authority and stacked-unit pin matches the architecture base.

## Required findings

### D4-2-R1-RF-1 — Price the actual `BTreeMap` lookup comparisons conservatively

`crates/host/src/component_admission.rs:93-94` charges `manifest::probe_reference_comparisons(object.len())` and then calls `BTreeMap::get`. That helper is the binary-search bound `ceil(log2(m)) + 1`; it is conservative for D4-1's sorted-slice probe, but it is not a bound for Rust 1.95's `BTreeMap` lookup. The pinned Rust implementation linearly scans the keys within each B-tree node (`alloc/src/collections/btree/search.rs:225-230`), and a node can hold 11 keys (`node.rs:43-44`).

This undercharges a real path in this unit. The authenticated release row has nine sorted fields. Its `publisher` and `sourceClass` lookups at `component_admission.rs:200-201` can compare six and seven keys respectively in the single leaf, while `probe_reference_comparisons(9)` charges only five edges. The existing `lookup-uncharged` mutation proves that removing the charge is detected; it does not prove that the charged bound covers the executed comparisons.

Replace the binary-search price with a proven conservative bound for the actual map lookup, or perform an explicitly charged search whose comparisons are observable. Add a control covering a late release-row key and a mutation that makes the bound insufficient. The one-unit-short budget evidence must then show refusal before the lookup whose work would exceed the allowance.

## Verified evidence

- The product map has exactly 13 paths, including exactly the two declared new paths. Every parent pin matches product base `4e475c753002d21ed99e0d53e64218e55af0cb1f`; every current candidate file matches both its candidate pin and archived copy. The worktree is based at that commit and has no changed or untracked path outside the map.
- D4-1 and CI-2 are ancestors of the product base. The product lock at that base matches the source record. The adapter remains library-only with no production caller or production wiring.
- The trust owner retains the ordinary reader's reserved set and lends it through the public view; the adapter borrows the authenticated component and release association, builds the three-pass claims projection, uses the nine-member provider projection, passes an empty explicit-trust slice, and invokes the integrated D4-1 judge. Fixture gates and the host-to-components package edge are represented in the candidate and preserved evidence.
- The completed lane records every required row passing. Its comparisons show security at 1281/1283 passes with the same 14 inherited failures and host at 418/427 with the same nine inherited failures. The package explicitly avoids claiming a fresh whole-suite pass.
- The prior lane records exactly two surviving mutations: `allocation-before-its-charge` and `parent-dropped`. The takeover repair changes only the host test source, preserves the original source, broadens the allocation guard to count typed `::with_capacity` calls, and adds a validated body/view/real-judge child-parent control. The mutation identities and order are unchanged. In the completed evidence all 13 mutations end in runtime test failures, with no compile-failure credit.
- The scope discloses unexecuted invariant branches, the split reader/judge evidence, later production wiring, the absent path half/profile/record, and the need for a separate inventory successor after integration. No product qualification or full D4 closure follows.

## Non-blocking observations

None.
