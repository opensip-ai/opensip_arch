# Review: C2a3 proposed callback coefficient128E uniform-accounting addendum r2

**Verdict: ACCEPT-PLAN-ADDENDUM**

**Scope:** `callback-price-plan-addendum-only`

The frozen subject manifest SHA-256 is `d5f89ce6abf6ffdfd6d42fc003d4547713c20848bc4c1ed9d0d4af41ffd2033d`. All 32 declared members are ordinary files and match their declared byte counts and SHA-256 values.

No required findings.

The revision closes `C2A3-CBPA-R1-RF-1`. The call tree now represents the `Vec::extend_from_slice` and `SpecExtend<u8, slice::Iter>` forwarding boundaries, the runtime `count > 0` predicate, and a uniform rule for every named nonleaf argument and nonunit return: `ceil(2 * active_tuple_bytes / 64)`. The rule is applied without tail or wrapper fusion. In particular, the 40-byte `RawVecInner::reserve` and `needs_to_grow` argument tuples each consume two visits.

The successful path matches the frozen source order and bodies:

- `Collector::chunk` accounts for callback transport, sticky/state guards, both length queries, remaining arithmetic, comparison, and the mutable `bytes` field borrow.
- `extend_from_slice` constructs a slice iterator, forwards the 16-byte active iterator state into the `u8: TrivialClone` specialization, reconstructs the borrowed slice through `as_slice`/`make_slice`, and forwards it to `append_elements`.
- Both iterator ZST predicates are explicit. The non-ZST `u8` path accounts for length, pointer formation, end pointer, pointer difference, and raw-slice formation.
- `append_elements` accounts for source length, the full Vec/RawVec/RawVecInner reserve chain, `Layout`, capacity and false `needs_to_grow` gate, current length, `count > 0`, the complete Vec/RawVec/RawVecInner/NonNull pointer chain, destination offset, fat-to-thin source cast, copy metadata, and length mutation.
- Under the previously reviewed prefix invariant, `additional <= capacity - len`; the grow branch is unreachable on an accepted chunk. No allocator loop or other variable metadata loop is selected. Payload copy streams remain separately charged as `2k`.

Applying the declared rule gives 29 transport visits and 37 bounded semantic-leaf visits, for 66 candidate visits. The selected 128-visit coefficient is therefore conservative within this conditional logical-source model. The failed paths also reconcile: sticky, inactive, and overrun callbacks cost 2, 6, and 10 candidate visits respectively, including callback-entry transport and `fail` transport plus tag mutation.

The semantic leaf boundary is coherent with the owning M model at plan scope. It is limited to fixed-field/tag/length queries, fixed-arity scalar operations, pointer/reference operations, fixed iterator construction, slice formation, and copy-intrinsic semantics. It does not admit arbitrary user helpers, variable metadata algorithms, allocation, growth, hashing, or comparator work as leaves. The captured helper sources support the selected `u8: TrivialClone` path and fixed wrapper topology. Optional core precondition machinery remains an explicit trusted semantic condition rather than a claim about disabled checks, machine work, or qualification.

The revised formula expands to `M_edges = 128 + F*(237 + 23H) + 128E`, with `scalar_edges = M_edges - q` and `q = 11FH`. Relative to the current `8E` draft, the exact additional cost is `(0, 120E, 7680E)`. Object, storage, payload-copy, header, comparison, and map-bulk terms are unchanged. Fixed `128`, prepaid scan `12F`, remaining local `52F`, and begin/finish/digest obligations remain separate; callback slack is not reassigned to them.

This acceptance is limited to the conditional policy, accounting model, and implementation plan. Candidate active widths and primitive contracts remain unproved source/ABI conditions. Exact-byte publication and lead assent, a separately reviewed implementation, updated test oracle and meaningful controls, fresh source/native evidence, complete M accounting, aggregate census and positive-boundary fit, unit acceptance, integration, and product qualification remain required. Existing queued images retain only their old frozen scopes.
