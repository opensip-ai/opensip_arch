# C2a-3 addendum map-r1: retire the borrowed map, re-price the local and frame work (G-1, G-2, G-3)

Author: the C2a-3 R2-DEEP author (Claude Opus 5.5, session opensip-c2a3-m), 2026-10-27. **Revision r2, proposed, not
accepted.** §9 answers REVIEW-r1's four findings.
It amends the accepted C2a-3 retention plan r2 and its three accepted addenda (callback-price-r2, funding-price-r3
and slot-carrier-r1) under the lead assent X-C2A3-M. It changes no cap, no law outside C2a-3, and no CI, D4, C2a-1
or K price.

## 1. Why: a counterexample to funding sufficiency

The product draft funds representation work of `1024 + F(481 + 23H) + 128E` edges. Independently source-audited
scoped ledgers, written under callback-price-r2's uniform accounting rule, show that three families exceed their
allowances:

| Family | Allowance in the accepted fee | Audited source count | Audit |
|---|---|---|---|
| Map construction | `173F + 23FH` (shared with destruction) | `405F + 75 + 221ΣV + 70ΣR + 1061L + 362C + 1957J`; the first insert alone is 470 | map-outer-insert-source-r1, SOURCE-AUDIT (130 members) |
| Map destruction | (same) | `465F + 3K_I + 222n - 21H + 327` | map-destruction-source-r1, SOURCE-AUDIT (146 members, f3b682e8…) |
| Collector::begin digest loop | inside the other-local 52F | 4453 per Blob | local-collector-digest-source-r1, SOURCE-AUDIT (33 members, 2c40b33f…) |
| First-loop scaffold | inside 52F | `115F + 190` | local-zip-loops-source-r1, SOURCE-AUDIT (31 members, 6f3f58a5…) |
| Second (map-builder) loop scaffold | inside 52F | up to `237F + 484`, before its bodies | same |
| Slot/frame metadata | `(0, 8n)` | the zip, push and insert routes alone exceed 8 per component | this addendum, §5 |

For one Blob, the map's first insertion (470) already exceeds the whole map allowance (219), and begin's digest loop
is about 85 times the local room. This is the plan's escalation trigger. A larger coefficient on the same shape
would roughly double the per-Blob M and still leave the map's height-dependent terms (`F(870 + 571H)` in order) as
the dominant cost. So this addendum changes the shape first, then prices what remains.

## 2. The selected shape (option B)

1. **The borrowed `BTreeMap` and its builder loop are retired.** The one transfer loop pushes `(blob.path(), bytes)`
   into the single pre-reserved vector, `Vec<(&str, Vec<u8>)>` with capacity F, in candidate order.
2. **The C2a-3k kernel takes that vector by reference:** `retained: &[(&str, Vec<u8>)]` replaces
   `retained: &BTreeMap<&str, &[u8]>`. Its walk, its six charges, its refusal causes, its order and its price are
   unchanged. It copies and allocates nothing. Only the parameter type and the destructuring pattern change. §6 sets
   out the re-review subject.
3. **`Collector::begin` keeps its state and length checks and drops the 32-byte hex comparison.** That comparison
   duplicated K's check of the same digest. An arbitrary false announcement alone is no longer rejected by the
   collector. What matters is that wrong retained bytes cannot be admitted. CI's transfer verifies the stream
   against its pinned row before `finish(true)`, and K re-hashes every retained byte against the candidate's own
   `sha256`. So wrong bytes either fail CI's transfer (`Tree(Digest)`) or fail K (`Closure(Retention(Digest))`). The
   kernel's digest check is not removed, and no other transfer producer is authorized. The sink contract (`VerifiedSink`:
   commit nothing unless `finish(true)`) is unchanged. The begin length comparison becomes `length != expected as u64`,
   lossless under the existing LP64 const assertions. The collector loses its `sha256` field.
4. **A constant per-component debit, COMPONENT, opens `admit_component_inner`** before CI open. It prepays the
   component's fixed local work (§4.2). This also turns funding-r3's excluded initial bootstrap (the entry to
   `fund_representation`, its first constant debit and that debit's caller transport) into paid work. The trusted
   bootstrap moves to `admit_component_inner`'s entry and its own first constant debit, which is the same policy
   class as MODEL.md (constant, candidate-independent, no allocation).
5. **The frame constructs its slot vector once** (an `if count == 0 { Vec::new() } else { … }` expression, so no live
   Vec is replaced) **and fills it with an explicit push loop** (`while slots.len() < count { slots.push(None) }`)
   instead of `resize_with`, whose `RepeatWith`/`Take`/`for_each`/`SetLenOnDrop` route has no reviewed model.
   `prepare_slots` and `admit` each charge a constant frame debit first, then their n-dependent part (§5).

`proposed/component_admission.rs` and `proposed/component_closure.rs` are the exact proposed product bytes.
`proposed/candidate-vs-5579e0d.diff` is the whole diff against the frozen S1 head 5579e0d (claude/c2a3), including
the test and oracle adjustments the shape needs. The fee oracles and exact-source pins are updated only in the
implementation step after acceptance.

## 3. Accounting rule

This addendum uses callback-price-r2's ACCOUNTING-RULES and funding-r3's MODEL unchanged. A call costs
`ceil(2·arg/64) + ceil(2·result/64)` visits plus its body. A leaf costs 1. A move of a w-byte value that is not a
call transport costs `ceil(2w/64)`. Every visit reserves 64 bytes. Funding-r3's definitions are imported by value
(CALL-TREE.json `importedFundingR3CallTreeSha256` = 3bd71196…bb9a), and the checker asserts byte-equality.

Two conservative choices are explicit:
- **Larger audited counts win.** Where a later SOURCE-AUDIT scoped model counted a route higher than funding-r3's
  granularity, its count is used as an `inherited` primitive naming its subject manifest. These are the first-loop
  scaffold (115F + 190), the specialized Zip scaffold (237n + 484) for the frame's zip, and the debug raw-pointer
  `add` guard chain (65).
- **Debug routes are counted.** `assert_unsafe_precondition!` expansions (`check_{language,library}_ub`, the
  precondition function and its predicate), the `debug_assert` in `layout_array`, and the `ptr::add` guard chain are
  counted although a release std may omit them.

**Trusted, unpriced boundaries (unchanged in kind):**
- the bodies of `__rust_alloc`, `__rust_dealloc` and `__rust_no_alloc_shim_is_unstable_v2`, whose caller interfaces
  are counted;
- WorkScope/WorkLedger mechanism bodies;
- CI's open and transfer bodies (B_open, T), C2a-1's candidate body (C2a₁) and K's body, each charged by its owner;
- the internal field cleanup of a ClosureCandidate (C2a-1 owner), of a RetainedTree (CI owner) and of the core
  roles (receipt owner). Their drop-glue call boundaries are counted here.

## 3.1 Trusted bootstrap endpoints (amending funding-r3 MODEL's initial-debit boundary)

The same policy class as MODEL.md: the minimal, constant, candidate-independent control needed to attempt a first
debit, with no allocation. It is excluded from the application ledger, not paid retroactively. Funding-r3's own
bootstrap (fund's entry, its first constant WorkCost, the first charge's caller transport and its `?`) becomes paid
work inside COMPONENT, but only after COMPONENT succeeds.

**Component (`admit_component_inner`).**
- **Excluded:**
  - the entry transport of `admit_component_inner` (or, on the single-component route, `admit_component`'s entry,
    its `work.scope` call and the closure entry);
  - construction of the constant `WorkCost { 0, COMPONENT, 64·COMPONENT }`;
  - the charge call's argument and result transport;
  - the immediately attached `?`: on success, Try::branch/Continue; on refusal, Break/FromResidual/identity and the
    typed `Budget` return transport of `admit_component_inner`.
- **Endpoint:** the `Result::Err(Budget)` delivered to its immediate owner.
  - On the single route, that owner's `scope` mapping and `map_err(public_failure)` are public mapping, and are not
    exempted.
  - On the set route, the per-component frame row (`admit_per_component`), which was prepaid by `admit`'s debits,
    pays them.
- **Not excluded:** any CI open, pin or retained-tree cleanup, which is CI owner work; earlier admitted components'
  cleanup, which is their own rows; or any later debit's caller work.

**Frame (`prepare_slots`, `admit`), n > 0.** The excluded control is:
- the entry transport, the `work.scope` call and closure entry, the claim destructuring (admit), `components.len()`
  and the `count == 0` test;
- the constant `PREPARE_FIXED`/`ADMIT_FIXED` WorkCost, its charge transport and its immediate `?`;
- on refusal, the scope's Err return and `map_err(public_failure)` Err path.

Everything after the constant debit is paid by `prepare_fixed`/`admit_fixed`, including the variable debit's
arithmetic.

**Frame, n = 0 (zero charge and zero allocation, inherited from slot-carrier-r1 and SD-9).** The whole path is
trusted control.
- `prepare_slots`: the entry, scope and closure entry, `len`, the zero test, `Vec::new()` (`RawVec::new_in` with
  dangling pointer, ZERO_CAP, no allocation), the `PreparedCandidateSlots` construction, Ok, the scope return,
  `map_err` Ok and the function return.
- `admit`: the claim destructuring, `len`, the zero test, `Vec::with_capacity(0)` (the zero-size layout route: no
  allocation), the zip constructor and its immediate terminal `next`, the move of the 136-byte core roles into
  `Self`, Ok, the scope return, `map_err` Ok and the return.
- **Later drops:**
  - The empty slot and admitted vectors' later drops take the zero-capacity `current_memory → None` route, with no
    deallocation.
  - The core roles' later drop is receipt-owner cleanup (X-C2A3-CORE).
- These are constant and allocate nothing. No resource cleanup becomes free by this classification.

## 4. New fee formulas, family by family

### 4.1 Per-Blob local work: LOCAL = 1024 per Blob (replaces other-local 52F and map 173F + 23FH)

`per_blob_local` counts 755 visits. Its parts:

| Part | Visits |
|---|---|
| Loop iteration (inherited) | 115 |
| Length and its checked conversion | 20 |
| Collector construction, including `Vec<u8>::with_capacity` (238) | 243 |
| Path | 4 |
| Transfer call boundary, `map_err` and `?` | 16 |
| begin | 13 |
| finish | 18 |
| into_verified, its `map_err` and `?` | 32 |
| Tuple construction and `Vec::push` without growth | 141 |
| Per-element drop of `(&str, Vec<u8>)`, including the buffer's deallocation route | 153 |

The selected 1024 is the next power of two. A failed Blob's collector buffer drop (148) is covered by that Blob's
unused push and element-drop rows. Earlier elements are dropped once, by their own rows.

### 4.2 Per-component fixed local work: COMPONENT = 1024 (new constant debit)

`component_fixed_local` counts 758 visits, explicit error ceiling included. Its parts:

| Part | Visits |
|---|---|
| Open call boundary, with 264-byte result transport, `map_err(tree_input)` and `?` | 78 |
| fund_representation's entry and first-debit caller (formerly bootstrap) | 13 |
| `Vec<(&str, Vec<u8>)>::with_capacity` and its binding | 239 |
| First-loop fixed scaffold (inherited) | 190 |
| Body getter | 4 |
| Kernel call boundary, `map_err` and `?` | 16 |
| `drop(retained_bytes)` outer glue and deallocation | 149 |
| `AdmittedComponent` construction and return transport | 19 |
| One failure ceiling: map_err Err, the conversion helper, failed `?`, Err return and terminating control | 50 |

### 4.3 Funding (accepted literals kept): FIXED = 1024, SCAN = 256F

The proposed `fund_representation` drops the path maximum, height, comparison, node and bulk arithmetic. The
ledger now gives funding explicit roots, `fund_fixed` and `fund_scan_blob`, rather than subtracting rows from
funding-r3's totals. They use exactly the proposed source's helper calls (18 fixed `add`/`mul`, 2 `checked_sub`,
and 5 per Blob), which the checker counts from the source. Their same-source `candidate.blobs()` loop uses the larger
audited scaffold counts (190 fixed, 115 per Blob), as the transfer loop does.
- `fund_fixed` = 682 ≤ 1024, including funding-r3's one 128-visit post-debit error reserve (its ceiling, 77, is
  unchanged in shape).
- `fund_scan_blob` = 217 ≤ 256.

A partial scan at a failing Blob is covered by that Blob's unused scan row. Funding-r3's accepted snapshot stays
byte-identical as provenance, and its older-granularity totals are not reused as proof.

### 4.4 Callback (accepted, unchanged): 128E

### 4.5 The complete per-component M

```
M_objects = [F>0] + F                          # the index vector and F payload buffers
M_edges   = COMPONENT + FIXED + F·(SCAN + LOCAL) + 128E
          = 2048 + 1280F + 128E
M_bytes   = 64·M_edges
          + ([F>0]·(40F + 128))                # R(F·size_of::<(&str, Vec<u8>)>()), 40 asserted LP64
          + Σ(b_i + 128)                       # payload R(b_i)
          + 2B                                 # sink copy streams
```

It is charged as COMPONENT (constant), then FIXED, SCAN and the checked remainder exactly as in funding-r3. The
remainder is `M − COMPONENT − FIXED − SCAN·F`, componentwise and checked.

Retired terms: map nodes `2F·(512 + 128)` and their `2F` objects; `q = 11FH`; `2P·q`; the `10368F` node-array bulk;
H and P as fee inputs; and the `48F` header-move bulk. Every header move is now an explicit transport or move visit
in the ledger.

## 5. The operation frame (G-3): replaces the shared slot metadata `(0, 8n, 4n·S_c + 2n·S_r)`

For n > 0:

```
prepare_slots: (0, 1024, 64·1024) then  R(n·S_c) + (0, 256n, 64·256n)
admit:         (0, 2048, 64·2048) then  R(n·S_r) + (0, 1024n, 64·1024n)
```

For n = 0, nothing is charged and nothing is allocated, as slot-carrier-r1 and SD-9 require. The constant control
that reaches that return is in the same trusted bootstrap class as §2.4.

| Row | Counted | Selected | What it covers |
|---|---:|---:|---|
| `slot_fill_iteration` | 165 | 256 | per slot: the push loop and the slot's later drop dispatch |
| `admit_per_component` | 524 | 1024 | per component: the zip next (inherited 237); the C2a-1 boundary with its 136-byte result, `map_err` and `?`; `Option::insert` with its debug `unwrap_unchecked` precondition; the inner call's argument transport; its 272-byte result through `?`; the 264-byte push; and the element's later drop dispatch |
| `prepare_fixed` | 562 | 1024 | the variable-fee arithmetic and debit, `with_capacity`, loop exit, the move of the slot vector out of its branch, construction, map_err, one successful and one refused `claim`, the slot vector's drop, and one failure ceiling |
| `admit_fixed` | 1048 | 2048 | the same pattern with the inherited zip fixed scaffold (484), the 136-byte core move, the admitted vector's drop and one failure ceiling |

The S_c and S_r byte moves are now explicit move and transport visits, so the separate `4n·S_c + 2n·S_r` bulk
terms are retired. S_c = 128 and S_r = 264 are the native sizes published by the S1 build (G-4); the ledger uses
them. A later change of either size changes the counted rows and needs re-review. A further `claim` after the
refused one is caller-frame control with no capability, allocation or candidate access, and is left to C2a-4's
frame.

**The record keeps the actual charges and the bound apart (M-BOUND "Operation-owned slot storage").** The actual
charged frame is the two debits above, once per set. The conservative per-component bound used in a census is
`M_slot(c) = R(S_c) + R(S_r) + (0, 1280 + 3072, 64·(1280 + 3072))`. That is the per-component rows plus one whole
set of fixed rows, charged to each component, so ΣM_slot exceeds the actual frame charge `3072 + 1280n` by
`3072(n − 1)` edges and the extra object allowances for n ≥ 1.

**The frame's Zip is `Zip(slice::Iter<AuthenticatedComponent>, slice::IterMut<Option<ClosureCandidate>>)`.** The
inherited counts (237 per component, 484 fixed) were audited for `Zip(Map<slice::Iter<u32>, closure>, slice::Iter)`.
Their dominance argument:
- The general and the TrustedRandomAccess-specialized routes have the same skeleton for plain slice iterators.
- The audited route additionally pays, per element, the mapper closure call, its captured-reference load, the
  `u32` cast and a `Vec` index (`blob_closure` 32 and `fn_forward` 34 in funding-r3), which plain slice iterators do
  not have.
- `IterMut::new` and `IterMut::__iterator_get_unchecked` mirror `Iter`'s, with `as_mut_ptr`/`NonNull::from_mut` in
  place of their shared forms. `IntoIterator for &mut [T]` is one forwarding call (3 visits), which is inside the
  replaced closure work.
- Early exit happens at a `?` inside the body, so no terminal `next` runs. That path is cheaper than the counted
  terminal.

The implementation proof should restate this dominance against the pinned `zip.rs` and `slice/iter/macros.rs`; it
establishes no compiler specialization choice.

## 6. The C2a-3k kernel re-review subject

**Accepted unit:** C2A-3K-r1 (product 274dccc; subject manifest
`docs/implementation/m3/snapshot-plan-c/c2a-3k-r1-subject.json`, c3caf5fb…). It is re-opened only for its input
type.

**The change, per `proposed/component_closure.rs`:**
- the signature becomes `retained: &[(&str, Vec<u8>)]`;
- the walk destructures `Some((path, slice))` over `&(&str, Vec<u8>)`;
- the doc comment states the precondition (strictly ascending, as C2a-3 builds it) and the consequence of breaking
  it.

**Must stay identical:** the walk order; the six `work.charge` sites and their immediately-preceding positions; the
two SHA-256 calls; `Retention::{Missing, Length, Digest}` and their order; the published price
`Σ(3 + ⌈len/64⌉ + 1) + ⌈|body|/64⌉ + 2`, plus one per passed-over entry; and the absence of allocation or copying.

**What the review must establish:**
1. **Order no longer comes from the type.** The walk only advances, so a non-ascending or duplicated input can only
   refuse `Missing`, or check a Blob against the first entry at its path. No Blob is accepted without an entry at its
   own path that has its exact length and digest. The comparison count stays ≤ entries + Blobs, as before.
   C2a-3's sole producer builds the vector in candidate order, which is strictly ascending by C2a-1's sort and its
   duplicate pass.
2. **The source pin still holds.** `c2a3k_verifies_without_allocating_and_charges_first` now admits exactly one
   `Vec`, the parameter's element type, and forbids every other allocation spelling.
3. **The kernel tests are unchanged except for one conversion.** The tests still build ordered maps and convert them
   at the call (`ascending`). Lookalike, passed-over, missing, length, digest, body and price controls are
   unchanged. The trust_bootstrap kernel leg converts the same way.
4. **Recommended new control:** non-ascending and duplicate inputs never accept wrong bytes. A duplicate with bad
   bytes first refuses `Digest`; reversed order refuses `Missing`.
5. **The 13 recorded C2a-3k mutations are re-run on the new source.**

## 7. Fit consequence (`ledger-report.json`; no fit, census or native result is claimed)

These are SD-9 r2's §4 illustrative single-component shapes (files and total size at its snapshot figure), with
uniform file sizes. They cover M plus one component's frame only. K, B_open, T, C2a₁ and D4 add to them.

| Shape | New M edges | Accepted r3 M edges | Map order estimate `F(870+571H)` (not a complete bound) | M + frame / 2^24 edges | M + frame / 2^34 edges | Bytes / 2^33 |
|---|---:|---:|---:|---:|---:|---:|
| 1 file | 4,181,504 | 4,179,727 | 2,012 | 0.25 | 0.0002 | 0.40 |
| 1,000 files | 5,890,048 | 5,343,024 | 7,151,000 | 0.35 | 0.0003 | 0.42 |
| 10,000 files | 20,482,048 | 15,941,024 | 94,350,000 | **1.22** | 0.0012 | 0.51 |
| 40,000 files | 71,682,048 | 55,361,024 | 423,080,000 | **4.27** | 0.0042 | 0.81 |

**Under the current snapshot interim (2^21 / 2^24 / 2^33):**
- Even the accepted r3 price could not hold the 10,000- and 40,000-file shapes once K's ≈2^24 edges are added. SD-9
  §4's figures already use the whole edge cap on S alone.
- The corrected price raises small-file M from about 1,350 to about 1,800–2,050 edges per file.
- Large single files are dominated by the accepted callback 128E term, which is unchanged.

**Under the accepted C2b successor caps (2^25 / 2^34 / 2^41):** every shape uses ≤ 0.5% of each coordinate. Those
caps reach R10a only if `snapshot_profile()` stays SD-9's interim after M5 adopts them, which is SD-9's question and
not this addendum's.

X-SD9-1 and X-SD9-2 stay open. A failing census stays a failure, and no cap moves without the owner.

## 8. What this addendum does not do

It does not:
- change CI, D4, C2a-1, K's price, a cap, the export map (beyond the kernel parameter type), the failure sum or its
  normalization, the core handoff or its (5,128,5863) fee, or the slot-carrier API;
- establish primitive contracts, native ABI beyond the S1 sizes, allocator bodies, complete M, census, fit, unit
  acceptance or qualification.

The implementation step then:
1. applies the proposed bytes;
2. updates the independent category oracle and the exact-source pins;
3. adds the §6 control and the frame-charge controls (the actual charge record per §5);
4. re-runs the C2a-3k mutations;
5. runs build, Clippy `-D warnings`, the tests and the lane, then the whole-candidate R2-DEEP review.

The disorder control `c2a3k_out_of_order_or_duplicate_input_never_accepts_wrong_bytes` (already in the prototype)
and `component_fixed_debit_refuses_before_ci_open` are mandatory in that gate.

## 9. Response to REVIEW-r1 (REQUIRED-FINDINGS, subject 372b0ee4…f60d)

- **RF-1 (expand allocation/deallocation helpers): fixed.**
  - Expanded routes:
    - `layout_array`'s debug assertion: two `Layout::size` calls; `pad_to_align` →
      `size_rounded_up_to_custom_alignment` (its `alignment.as_usize`, two unchecked intrinsics, mask and `and`);
      `Layout::alignment`; and `from_size_alignment_unchecked` with its library-UB precondition over
      `is_size_alignment_valid`;
    - `Alignment::as_usize` → `as_nonzero` and `NonZero::get`;
    - `Alignment::new` → `Alignment::new_unchecked`, with its language-UB precondition over `is_power_of_two`.
  - Every Vec construction, push and drop user picks these up by reference: `vec_with_capacity` 189 → 238,
    `inner_deallocate` 98 → 123, and `layout_array` = 86.
  - Effect on the rows:
    - per-Blob local 681 → 755, component fixed 684 → 758, `prepare_fixed` 487 → 562 and `admit_fixed`
      974 → 1048;
    - the selected literals PREPARE_FIXED 512 → 1024 and ADMIT_FIXED 1024 → 2048, with the frame formula
      `3072 + 1280n`;
    - LOCAL and COMPONENT stay 1024.
- **RF-2 (replaced empty slot vector): fixed by refactoring.** `prepare_slots` now binds `slots` once from an `if`
  expression, so no live Vec is overwritten. The ledger counts the 24-byte move out of the branch. The source check
  refuses `let mut slots = Vec::new();`.
- **RF-3 (funding recount): fixed.** Funding now has explicit roots with the larger audited loop counts (§4.3): fixed
  682 ≤ 1024 and scan 217 ≤ 256. The checker ties their helper counts to the proposed source.
- **RF-4 (multiplier): removed.** The map column is relabelled as an order estimate, not a complete bound.
- **Notes taken:**
  - §2.3 is rephrased in terms of wrong retained bytes;
  - the disorder controls are mandatory (§8);
  - §3.1 defines the bootstrap endpoints and enumerates the n = 0 path;
  - §5 states the Zip dominance argument for `Zip(Iter, IterMut)`;
  - S_c and S_r stay published by the exact build (`c2a3_published_native_slot_sizes_of_this_build`).
  - The remaining carrier widths (256, 40, 136, 32) are to be asserted by the implementation's ABI control.
