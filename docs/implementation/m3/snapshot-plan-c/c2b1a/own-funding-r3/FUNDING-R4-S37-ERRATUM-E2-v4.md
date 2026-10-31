# FUNDING-r4 section 3.7, erratum E-2 (v4): the OBJECT entry width is the type's size (LD-Q-112, 2026-10-30)

Additive to FUNDING-r4 (as E-1 was to section 8). Subject of the C2b-1a own-funding r5 review; adopted with the r5
ACCEPT (the coordinator's LD-Q-112). Found by CHANGE-SPEC-r5 section 1.3 (LD-Q-110: extents from types), recorded as
**AUD-18**.

## E-2.1 The defect
FUNDING-r4 section 3.7 prices an insert into the retained objects map `BTreeMap<String, ObjectInput>` with L2's
`btree_insert(members, key, entry)` (`snapshot.rs:117-140`: a new node per level and the root on the allocation side;
the search bytes plus **21 entries moved per level × entry** on the pass side), with the entry width the constant
`OBJECT = 24 + 40 = 64` (`typescript_context.rs`: the `String` key's 24 bytes plus 40 for the value). The value type
`opensip_identity::closure::ObjectInput { domain: IdentityDomain, descriptor: JsonValue }` is **48 bytes** on the
pinned 64-bit target (`JsonValue` 32, the domain discriminant padded to 16), so the entry is **72**, not 64. The other
five entry widths of the unit equal their types' sizes (`MEMBER` 56, `BLOB` 56, the inventory map 32, the basenames map
48, the minted-context map 32 + `size_of::<Minted>()`), each now `const`-asserted; this one did not.

## E-2.2 The correction
The entry width of every own B-tree insert is **`size_of::<K>() + size_of::<T>()` of the map's types**, carried by the
`EntryWidth` trait of the host primitives module and asserted equal to the former constant where that holds. For the
retained objects map the width becomes 72 (today's `size_of`; it follows the type if the type changes, which is the
point of extents-from-types). No formula changes; the input that was a stale constant becomes the type's fact.

## E-2.3 The effect on the insert charge (v2, after REVIEW-r5 OF-R5-5)
L2's `btree_insert(members, key, entry)` (`snapshot.rs:96-139` at dbe4955) uses `h = btree_height(members) = 1 +
bitlen(members)` and charges, with `node = 16 + 11·entry + 12·size_of::<usize>()`:
- objects `h + 1`, edges `12h + 1` (unchanged by the entry width);
- bytes `(h + 1)·(node + owned_record(0).bytes) + 22h·(key + 1) + 21h·entry`: the **allocation side** carries
  `11·entry` bytes in each of the `h + 1` nodes, the **pass side** `21·entry` per level (the unit's `price::btree_insert`
  splits them so).
With the entry 64 → 72 (Δ = 8), per OBJECT insert: **allocation bytes +88(h + 1), pass bytes +168h, total +256h + 88**;
the search bytes, objects and edges are unchanged. At the populations the retained objects map has when an insert
happens:

| members before the insert | h = 1 + bitlen | +alloc | +pass | +total |
| --- | --- | --- | --- | --- |
| 0 | 1 | 176 | 168 | 344 |
| 1 | 2 | 264 | 336 | 600 |
| 2 | 3 | 352 | 504 | 856 |
| 3 | 3 | 352 | 504 | 856 |
| 4..7 | 4 | 440 | 672 | 1,112 |

The OBJECT inserts of a call (`typescript_context.rs` at dbe4955): the mint inserts one object per closure (`:1055`)
and then the snapshot object (`:1065`), at populations 0, 1, 2, …; the retained clone (`:912`) re-inserts the same k
objects at populations 0..k−1. For k objects the increase per pass over the map is `Σ_{i<k} (256·(1 + bitlen(i)) + 88)`:
k = 3: 1,800 bytes (the reviewer's figure); k = 4: 2,656; k = 8: 7,104. In closed form, for a PASS over the retained map that inserts k objects (k = the admitted closures + 1 snapshot) at
populations 0, 1, …, k−1:

    ΔB(k) = Σ_{i<k} (256·(1 + bitlen(i)) + 88) = 344·k + 256·S(k)      bytes per pass,   S(k) = Σ_{i<k} bitlen(i)
    ΔO(k) = Σ_{i<k} (2 + bitlen(i))             = 2·k + S(k)            ledger objects per pass (h + 1 per insert)

and for p passes charged to ONE ledger in one accounting interval, the per-call correction is p·ΔB(k) bytes and p·ΔO(k)
objects. At dbe4955 the two passes are the mint's inserts (`mint_typescript_context`, `:1055`/`:1065`) and the retained
clone's re-inserts (`retained.copied(work)`, `bind_typescript_universe` `:1144`); mint and bind are SEPARATE functions,
each taking a `WorkScope`, and the mint has no non-test caller, so whether p = 1 (each pass funded by its own ledger) or
p = 2 (one ledger funds both) is the binding caller's choice (C1c), not a fact of dbe4955. E-2 therefore publishes BOTH.
The correction is debited where the accepted charge is (inside H4, before the insert).

## E-2.4 Derived maxima (v4)
- The C9 term bound (H21), the generated price tables (F2) and the SLOT matrix do not involve the OBJECT insert
  (w11's diff at af0a4d2: no generated value or pin moved; the ledger fixture generated at af0a4d2 pins the corrected
  charge).
- The owning scope is the pre-Plan resolved-inputs scope of mint/`price_call` (no fit-gate row, BOUND-1 section 7.0).
  k is bounded per ledger profile by the profile's objects cap through p·ΔO(k) ≤ cap (`work_ledger.rs` at dbe4955:
  `OBJECT_LIMIT` 65,536 with `BYTE_LIMIT` 2^28; `SNAPSHOT_OBJECT_LIMIT` 2^25 with `SNAPSHOT_BYTE_LIMIT` 2^41). These are
  NECESSARY-domain bounds (the next k exceeds the cap on objects alone), not feasible maxima: other work on the same
  ledger lowers them, and the ledger checks every dimension on every debit (`work_ledger.rs:386`), so nothing here says
  which dimension a real call exhausts first.

  Per pass (p = 1) and per call with p = 2, against the relevant byte cap:

  | k | ΔB(k) per pass | / 2^28 | 2·ΔB(k) (p = 2) | / 2^28 |
  | --- | ---: | ---: | ---: | ---: |
  | 3 | 1,800 | 6.71·10^-6 | 3,600 | 1.34·10^-5 |
  | 4 | 2,656 | 9.89·10^-6 | 5,312 | 1.98·10^-5 |
  | 8 | 7,104 | 2.65·10^-5 | 14,208 | 5.29·10^-5 |
  | 64 | 104,192 | 3.88·10^-4 | 208,384 | 7.76·10^-4 |
  | 1,024 | 2,711,808 | 1.01·10^-2 | 5,423,616 | 2.02·10^-2 |

  | profile, p | k_max (objects cap) | p·ΔO(k_max) | p·ΔB(k_max) | / byte cap |
  | --- | ---: | ---: | ---: | ---: |
  | `OBJECT_LIMIT` 2^16, p = 1 | 4,915 | 65,534 | 15,950,984 | 5.94·10^-2 of 2^28 |
  | `OBJECT_LIMIT` 2^16, p = 2 | 2,633 | 65,534 | 15,892,016 | 5.92·10^-2 of 2^28 |
  | `SNAPSHOT_OBJECT_LIMIT` 2^25, p = 1 | 1,550,068 | 33,554,413 | 8,329,518,304 | 3.79·10^-3 of 2^41 |
  | `SNAPSHOT_OBJECT_LIMIT` 2^25, p = 2 | 810,263 | 33,554,422 | 8,317,683,664 | 3.78·10^-3 of 2^41 |

  (REVIEW-r8-design's `e2-pass-domains.json` reproduces the four k_max rows.) The dbe4955 call's ACTUAL retained set is
  small (the two supplied closures plus the snapshot: k = 3 in the step-5a ledger fixture; its `call:price` bucket alone
  is 16,145,072 bytes on the bind path at af0a4d2, against which one pass at k = 3 is 1.11·10^-4 and two passes
  2.23·10^-4); the general bound above is for any future caller within the caps, and is to be distinguished from it.
- Not claimed: that any fit margin is unchanged, or that a call at k_max refuses on objects rather than bytes. The cap
  enforcement prevents silent overspend; it proves neither.

## E-2.4a What changed (v2 → v3 → v4)
v2's "a few thousand bytes … below 10^-5" did not hold for every k of its own table (REVIEW-r6-design/r7-design). v3
gave ΔB(k) in closed form with k bounded by the objects cap, but labelled per-PASS numbers as per-call bounds and
asserted the two passes share one ledger, a fit-margin claim and a refusal-order claim (REVIEW-r8-design E2-R8-1/-2).
v4 makes the pass count p explicit, states the accounting interval at dbe4955 (separate mint and bind functions over a
caller-supplied `WorkScope`; p is the binding caller's choice), publishes per-pass AND per-call (p = 2) numbers and
k_max for both p, separates the dbe4955 call's actual k = 3 from the general bound, and drops the margin and order
sentences. The per-insert arithmetic (+88(h+1) / +168h / +256h+88) and the k = 3/4/8 per-pass sums are unchanged. v2
and v3 stay as dispatched (custody G).

## E-2.5 Controls
`EntryWidth`'s `const` assertions for the five equal pairs; the retained-insert controls' pins updated to 72 (w11);
the lexical gate's R3 arity rule (a caller cannot pass a width) and the audit's per-primitive proof of H4 (the width
is read from the types inside the primitive).
