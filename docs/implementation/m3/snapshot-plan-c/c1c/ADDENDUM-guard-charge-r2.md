# C1c plan r4, addendum guard-charge: sealing's read-set guard is charged (LD-C1C-7A), r2 (coordinator, 2026-10-29)

**Status: PROPOSED.** This text is under R3 different-vendor review (`REQUEST-r3.md`). It takes effect only when the
coordinator records its adoption, owner-delegated under OD-AUTO-1, in a **separate adoption receipt**
(`ADOPTION-guard-charge.md`). That receipt pins this file's sha256 as the reviewed bytes. This file is never edited
after review.

**r2 answers R3 review r2** (`REVIEW-r2.md`):
- **Finding 1 (REQUIRED):** §4 now keeps the accepted *T*/*L*/*N* partition.
- **Findings 2 and 3:** §5.3, §5.6 and §2 are clarified.
- **Finding 4:** adoption moves to a separate receipt.

r1 is kept unchanged as `ADDENDUM-guard-charge-r1.md`.

**What it amends:** the accepted C1c plan r4,
`opensip_arch/docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r4.md`
(sha256 `d066487af5608b0375bd0ba1f8eaefda9b8bdbe70d27d96a875ba43cca8fe835`). PLAN-r4's bytes are not edited. Where this
addendum and PLAN-r4 conflict, this addendum controls, and only on the points it names.

**Why:**
- **The conflict:** LD-C1C-7 makes the step-2 guard uncharged. The later C2b plan r4 M1a convention C1
  (`lead-2026-10-25/c2b-m1/M1A-PRICING.md` r6) funds every compute pass, and the work that prices it, before it runs.
- **The ruling it follows:** the R3 review `l5-review/REVIEW-r1.md` (codex-l5-r3, gpt-6-astra/high, verdict
  `L5-RULING: A-NEEDS-REVISION`). That review found "charges nothing" to be a substantive accepted commitment. So C1
  does not supersede it by interpretation; it must be amended expressly. This is that amendment.

## 1. Superseded text

These three passages are superseded for compute charging only:
1. **LD-C1C-7, "The check reads no source, builds no string and charges nothing"** (PLAN-r4 line 114). It is
   replaced by: "The check reads no source and builds no string. Its compute is charged under §2 of addendum
   guard-charge."
2. **LD-C1C-7, "Step 2 allocates nothing and adds no charge"** (line 116). It is replaced by: "Step 2 allocates
   nothing. Its charges are exactly those of §2 of addendum guard-charge."
3. **The §4 control "(r3) The guard: sealing's step 2 makes no allocation and no charge (a source pin and the ledger
   delta)"** (line 242). It is replaced by §5 of this addendum.

## 2. The new rule (LD-C1C-7A)

**Step 2's guard is funded under M1a convention C1.**
- **Each unit of guard work is charged before it runs.** This covers:
  - each layout-digest comparison;
  - for each `ReadSet` row: the chosen-authorization lookup, its prefix comparison, the relative-suffix scan for
    `node_modules` and VCS segments, and the excluded-prefix search.

  The charges go to the snapshot ledger: the same `WorkScope` that LD-C1C-8 charges the read set to.
- **Determining a price is itself funded first (C1).**
  - Any pass that measures a row to compute its guard charge, such as a scan of the row's `/` separators, is either
    charged before it runs, as its own C1 pass, or covered by an explicit source-derived proof that an earlier charge
    already funds it.
  - Including the measuring pass in the returned price does not satisfy this.
- **Exactness:** each actual debit is counted exactly once in the decomposition.
  - Genuinely shared work, such as a traversal that another pass already pays for, is not counted twice.
  - Sharing a loop does not exempt distinct work. An additional comparison, byte examination or measuring scan in
    the same loop is still charged. Under C1, repeated byte examinations count.
  - Conservative, source-derived envelopes are allowed, as M1a permits. Exact model correspondence does not require
    metering only the comparisons taken on each short-circuit path.
  - Every guard charge is in the read-set term (§4).

## 3. What does not change

- **The checks:**
  - the guard still reads no source and builds no string;
  - it allocates nothing;
  - it uses borrowed comparisons only.
- **The semantics:**
  - the eligibility and exclusion semantics;
  - the chosen authorization (the longest eligible retained `realPath`; r4, R3-RF-2);
  - "at least one eligible authorization, uniqueness not required";
  - read-once and inventory-once behaviour.
- **The failure:** a violation is still `SealError::Internal`, and the public refusal is still
  `SNAPSHOT_PRUNED_TREE_NOT_A_READ`.
- **No layout:** with no layout and an empty read set, sealing's output and its charges equal main's (LD-C1A-6).
- **The required order (step 2 before step 3).** The guard's verdict over the whole inventory, in inventory order,
  precedes every step-3 refusal. "Every step-3 refusal" includes budget exhaustion from step-3 charges. The
  comparison below includes under-funded executions: a fused step-3 debit may not use up the allowance needed to reach
  a later step-2 violation. An implementation may fuse the guard into step 3's traversal only under two
  conditions:
  - its observable result equals the separate-pass order for every input with competing failures (a guard
    violation and a step-3 refusal), including which error is returned and the ledger at the error;
  - its code review establishes that equality.

  Otherwise the guard runs as its own pass, charged under §2. This addendum authorizes no change to the failure
  order.

## 4. The consequences, stated

- **Successful seals:** their ledger delta and remaining allowance change by the guard's charges. A valid operation
  that previously succeeded with a near-exact budget can now refuse with budget exhaustion, at the guard or later in
  sealing.
- **Under-funded seals:** when the remaining budget cannot fund a guard charge, sealing refuses with budget
  exhaustion before that check runs. So an invalid row that an under-funded seal never reaches is reported as budget
  exhaustion, not `Internal`.
- **Sufficiently funded seals:** an invalid row still fails the guard as `Internal`. No budget argument removes a
  required non-budget refusal (successor law item 4).
- **The read-set term:** it gains the guard's charges, including any separate measuring pass and any separate guard
  pass.
- **The partition is unchanged (r2, R3 review r2 finding 1).** Each actual charge is assigned once, under the
  existing definitions in successor-law item 1:
  - **To *T*:**
    - the bounded guard work per inventory row, with its measuring work;
    - any separate guard traversal's bounded inventory work;
    - any fixed, bounded guard work.
  - **To *N*:** layout-count-dependent setup or comparisons, and other existing non-row or refusal work. Each such
    item needs an explicit, source-derived assignment under the inherited *N* definition and its remaining-margin
    condition.
  - **Never to *L*:** no guard work goes to *L* merely because it consumes layout evidence. C2's resolver charges and
    the accepted *L*max are unchanged.

  The pricing review and the fit claim (§6) carry the same partition. This correction needs no rerun of M3 and no
  cap change.

## 5. The controls (they replace the line-242 control)

1. **Allocation and source reads:** step 2 makes no allocation and reads no source, checked by a source pin. This is
   checked separately from the charge.
2. **Exact ledger delta:** for the valid, overlapping (longest eligible prefix), nested-`node_modules`, VCS-segment
   and first-party-link cases, the guard's ledger delta equals the model's price.
3. **Funding boundaries:** each control uses a valid fixture, with all earlier and later required sealing work
   funded, and depletes one named budget component.
   - With exact whole-seal funding, the seal admits.
   - One unit short, at a guard charge or at a measuring charge (or the charge that covers it, under §2), it refuses
     with budget exhaustion at the predicted point.
   - The control records which component was depleted and where the refusal happened.
   - It also observes that the protected work did not run. Final ledger equality alone cannot detect a charge moved
     after its work.
4. **Budget before the check:** an under-funded seal with an invalid row refuses with budget exhaustion before the
   guard check that the row would fail.
5. **Invalid rows, sufficiently funded:** a row injected below an excluded prefix fails as `Internal`. So does a row
   whose chosen authorization is not a prefix of it, and one whose suffix crosses `node_modules`.
6. **Mutations, each detected by a control:**
   - remove a guard charge;
   - move a guard charge after the work it funds;
   - remove the measuring charge, or move it after the measuring pass. Where §2's prior-funding alternative is used,
     the mutation removes or weakens the charge that actually covers the measuring pass, or the proved coverage. It
     does not invent an additional debit.
7. **Competing failures:** one control per competing pair shows the required step-2-before-step-3 result (§3).
8. **No layout:** sealing's output and charge equal main's.

## 6. The fit gate (it governs the freeze)

The read-set term, with the guard's charges, is priced in C1c-1 pricing r2. P-RF-1's repaired maximization proof
must show, componentwise, under the accepted variant and the inherited guarantee premises:

2·(*T*sound_new + *L*max) ≤ {2^25 objects, 2^34 edges, 2^41 bytes}

- **Status of the r1 margin:** pricing r1's byte margin (290,260,728,350) is provisional, not an accepted margin.
- **The review:** the proof and its source/model correspondence are independently reviewed before the freeze.
- **If any component is negative:** C1c-1 stops and escalates to the coordinator for a separately reviewed law/cap
  decision. Neither dropping the guard charge nor raising a cap is authorized here.

## 7. What remains gated

This addendum does not accept, or close:
- pricing r1 or r2;
- the source, the model or any runtime evidence;
- a cap change;
- C1c-1's integration, binding, receipt interval or qualification.

Those keep their own gates under C1c-1's plan. At its binding, C1c-1 copies this addendum, once adopted, beside
PLAN-r4 in the architecture repository, as `c1c/ADDENDUM-guard-charge-r2.md`, with its adoption receipt, and the inventory records both.

## Adoption

Adoption is recorded only in `ADOPTION-guard-charge.md`, never in this file. That receipt records:
- the reviewed bytes, as this file's sha256;
- the review artifact's path and sha256, and its verdict;
- the date and the words "owner-delegated under OD-AUTO-1";
- the owner notification.

At binding, C1c-1 copies this file and the receipt unchanged. The receipt identifies the adopted successor of PLAN-r4.
