# Review: C2a3 proposed callback coefficient16E plan addendum r1

**Verdict: REQUIRED-FINDINGS**

**Scope:** `callback-price-plan-addendum-only`

The frozen subject manifest SHA-256 is `bfac5fe66b5504e9e192ed0c33d0d9b3ae22448374d9be3ef9de453b78c43d31`. All 16 declared members are ordinary files and match their declared byte counts and SHA-256 values.

## Required finding

### C2A3-CBPA-R1-RF-1 — HIGH — the explicit 16-stage successful-callback ledger omits source work

**Files and lines:** `subject/STAGES.json:94-203,333-347`; `subject/inputs/product/component_admission.rs:296-305`; `subject/inputs/rust/alloc/vec/mod.rs:2877-2886,3499-3500`; `subject/inputs/rust/alloc/vec/spec_extend.rs:50-56`; `subject/ADDENDUM.md:13-15`.

**Concrete failure:** The selected coefficient is justified as one visit for each of exactly 16 disjoint source stages, with receiver, iterator, and call-argument transport explicitly represented. The frozen source contains work absent from those rows:

- `append_elements` performs the runtime `count > 0` comparison and branch before `copy_nonoverlapping`. The `copy-metadata` row contains only the three copy arguments and their output transport; it contains no operand or result for that comparison/branch. No other row accounts for it.
- The ledger moves directly from `Collector::chunk` into iterator construction and later into `append-count`. It does not identify the `Vec` receiver plus fat-slice forwarding at `extend_from_slice`, or the `Vec` receiver plus constructed iterator forwarding into the selected `spec_extend` implementation. Other boundaries, such as `Vec::reserve` to `RawVec::reserve` and then `RawVecInner::reserve`, explicitly charge both input and output argument transport. The subject supplies no uniform conservation or fusion rule that makes the omitted forwarding free while charging those later boundaries.

Because all 16 visits are already assigned, the frozen inventory does not establish that 16 visits cover the successful path under its own explicit accounting rules. The arithmetic report merely checks the declared rows and therefore cannot detect these omissions.

**Required correction:** Re-freeze an exhaustive, consistently partitioned successful-path ledger. It must account for the `count > 0` predicate and the two forwarding boundaries, or state and apply a precise source-stage fusion/conservation rule uniformly to every call boundary. Recompute each affected operand total and the required callback coefficient; if the corrected partition exceeds 16 visits or 64 candidate bytes in a visit, revise the proposed coefficient and exact `(objects, edges, bytes)` delta. Preserve the refusal-path accounting and all existing implementation, re-freeze, test, native, aggregate-fit, and review obligations.

## Other assessed properties

The arithmetic shape itself is correct: changing `8E` to `16E` changes the fee by exactly `(0, 8E, 512E)`, leaves `q = 11FH` and the `237F + 23FH` terms unchanged, and does not duplicate fixed `128`, scan `12F`, or the remaining local `52F`. The frozen product source still contains the old `8E` coefficient, consistent with a plan-only subject.

Under the accepted conditional prefix invariant, `k <= capacity - len` selects the false `needs_to_grow` branch, so the cold allocation path is not part of a successful chunk. The sticky, inactive, and overrun refusal paths also fit below 16 visits when `fail`'s `None` test and assignment are counted separately. Those facts do not repair the incomplete successful-path inventory.

The addendum correctly preserves old queued images, requires a separately reviewed implementation and fresh source/native evidence, leaves caps and controls unchanged, and does not claim a complete M bound, unit acceptance, or qualification.

Evidence remains limited to the frozen plan, source excerpts, conditional prior arguments, and unexecuted arithmetic/control reports. Candidate operand totals, the `u8: TrivialClone` specialization premise, LP64 layouts, compiler/source correspondence, native behavior, the complete M bound, whole-census fit, and product qualification are not established here.
