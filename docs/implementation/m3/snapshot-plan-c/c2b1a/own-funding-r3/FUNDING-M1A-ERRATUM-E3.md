# M1a erratum E-3: destruction is funded by the allocation charge (version-frozen for design review r7; LD-Q-117 E, LD-Q-117-B)

Law-class (an M1a erratum), proposed by the C2b-1a author (w11:p1, `c2b1/ERRATUM-PROPOSAL-M1a-deallocation.md`, sha256 0a3e22bc8e9ce6ff23fcc93d91bf442baf2144a055dbf194b31cfff5f0a6c067) with the coordinator's wording fix applied; version-frozen here by the r6/r7 audit author (w25:p3) as the review subject with its own verdict line `C2B1A-E3: ACCEPT | REQUIRED-FINDINGS`; adopted on ACCEPT under OD-AUTO-1 with the E-1 receipt pattern. The amortization premise of LD-Q-117-B is stated explicitly in E-3.1; E-3.2 delimits the scope.

## E-3.0 The proposer's text (verbatim)

# Proposed M1a erratum: deallocation is funded by the allocation charge (C2b-1a author, w11:p1, 2026-10-30)

For LD-Q-117 E. Routed to the coordinator for R3 adoption; the base text for **E-3** (LD-Q-117-B), with the coordinator's wording fix applied: construction AND later charged growth; reallocation covered by the growth charge.

**Finding.** M1a (`docs/implementation/m3/snapshot-plan-c/c2b/law-revision-r4/PLAN.md`, the M1a paragraph) requires
"every allocation and input-proportional work family" to be mapped to a covering charge. It says nothing about the work
of freeing, so no accepted clause states that destruction (drop glue) is covered. Earlier C2b-1a texts asserted
"drops are uncharged under M1a", but that is a reading, not a citation.

**Proposed erratum (one paragraph, added to M1a):**

> *Destruction.* Freeing a value's storage is covered by the charges of the charged operations that allocated its
> storage or wrote its elements (construction AND later charged growth, such as push or insert), and is not charged
> again. Each allocation is freed at most once. Dropping a value releases exactly the allocations those charged
> operations made, and visits exactly the elements they wrote. A reallocation on growth frees the old buffer, and that
> free is covered by the growth charge that caused it. The drop work of a value is therefore at most a constant
> multiple of the work its covering charges already funded: one free per charged allocation, plus one element visit
> per element written under a charge. This holds amortized over the value's lifetime, since nothing frees what was
> never allocated.
>
> The rule applies only where every owned value in the charged scope was created by a charged operation, and no type
> in that scope implements `Drop` with work beyond freeing. Under CHANGE-SPEC-r7 the owned values of priced code are
> facade types created by charged constructors, and there are no generics, `impl Drop`, futures or `async`.

**Effect.** No price, cap, BOUND-1 term or published figure changes. The erratum states the basis that LD-Q-117 E asks
the r7 spec to cite, and that REVIEW-r6-design R6D-5 found missing.


## E-3.1 The amortization premise (LD-Q-117-B)

Each allocation made under a charge is freed at most once, and freeing it costs at most a constant factor of the work its allocation charge funded (one free per charged allocation; one element visit per element written under a charge; a reallocation on growth frees the old buffer under the growth charge that caused it). Over a value's lifetime the destruction work is therefore bounded by a constant multiple of the charges already debited for it: nothing is freed that was not allocated under a charge, and nothing is visited that was not written under one.

## E-3.2 Scope

The rule covers exactly the facade values of a priced module: values created by the charged constructors and grown by the charged operations of the primitives modules (CHANGE-SPEC-r7 sections B and E). It presupposes that no type reachable from priced code implements `Drop` with work beyond freeing (checked by the facade surface list), that priced code holds no generic values and no futures (CHANGE-SPEC-r7 sections B and C), and that a `WorkFailure` leaving a value partially built drops exactly what was charged before the refusal (M1a's refusal rule: the partial value is dropped, never copied). It states what the allocation charge covers; it changes no price, cap, BOUND-1 term or published figure.
