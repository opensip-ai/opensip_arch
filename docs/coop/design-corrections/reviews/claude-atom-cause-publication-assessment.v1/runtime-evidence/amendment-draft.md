# Amendment draft — outgoing native-completeness cause law

**Standing.** DRAFT proposed by the source-author origin. **Not applied, not accepted, not frozen.**
Source33 is untouched. This closes the four publication omissions of `assessment.md` §3 in one
place. It is contract text only: every input it names is a published record a normative-only
consumer already holds. **No Python name is load-bearing.**

**Exact placement.** `docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md`,
**§4 "Completeness partitions"**, inserted as a new block **immediately after the `**Outgoing:**`
paragraph (current line 74) and before `**Incoming owed programs**` (current line 76)**. Nothing
else moves; no existing sentence is deleted.

**Design constraints honoured.** No new cause name, no new field, no new semantics. Only the
selection and order already needed to make the existing outgoing branch derivable. Where a choice
is genuinely arbitrary it is marked **[DECISION]** — root decides; I do not.

---

## Proposed text

> **Outgoing cause derivation (normative, deterministic).** For an atom with `endpoint=source`,
> relation *R* at exact rung *G*, current subject *s* in universe *U*, evaluate the following
> **in order**. Each step names the `AtomCauseCodeV1` member it emits into atom `causes`; native
> `DeficiencyV2` values from `sufficiency_v2` go to `nativeDeficiencies` instead, per §7. Steps
> marked **stop** end the derivation for this atom with `value=unknown`; steps marked **continue**
> accumulate and proceed.
>
> Let **owed bindings** be the EnumerationPlan bindings for `capabilityForRelation[R]` — the same
> set §4 already defines for incoming. A binding is **available** when its `universe` is non-null
> and **unavailable** when its `universe` is null.
>
> | # | Condition | Cause | `universe` | `nativeCause` | Then |
> |---|---|---|---|---|---|
> | O-1 | no owed binding exists for `capabilityForRelation[R]` | `missing-relation-coverage` | null | null | **stop** |
> | O-2 | an unavailable owed binding's cell language-family is not owed for *U*'s family | `cross-family-edge-not-owed` | that binding's cell universe field, else null | null | **continue**, non-blocking |
> | O-3 | owed bindings exist but none **available** has `universe = U` | `selector-unbound` | null | null | **stop** |
> | O-4 | no retained subject-scope at exact `(R, G)` **contains** *s* under the §4 pairing law | `uncovered-expected-source-subject` | *U* **[DECISION]** | null | **stop** |
> | O-5 | a containing scope has no paired Coverage | `scope-without-coverage` | *U* | null | **continue**; if any O-5 fired, **stop** after the step |
> | O-6 | for a paired Coverage, `sufficiency_v2` over the §4 line 88 view is not satisfied | `coverage-unknown` | that Coverage key `sourceUniverse` | the carrier selected by O-7 | **continue** to the next paired Coverage |
>
> **O-7 — `nativeCause` for `coverage-unknown`.** Scan the sufficiency view's entries in the
> deterministic order *primary relation first, then each `DEPENDS_ON` relation in the order
> published in §4 line 88*, and take the **first non-null** `nativeCause`; null if none carries
> one. **[DECISION]**
>
> `unavailable-program-binding` is **never** emitted outgoing (see the paragraph above).
> O-1 and O-3 are mutually exclusive by construction. Every cause emitted here is an
> `AtomCauseCodeV1` member and reaches the proof through composition §9.5 item 1; no step here
> emits a `DeficiencyV2`.

---

## What each step closes

| Step | Closes | Previously |
|---|---|---|
| O-1, O-3 | `missing-relation-coverage` vs `selector-unbound` | **unpublished** (assessment §1) |
| O-4 | cause when no containing scope exists | **unpublished** |
| O-6, O-7 | cause and carrier when sufficiency is unsatisfied | **unpublished** |
| stop/continue column | branch order and record cardinality | **unpublished** |
| O-2, O-5 | — | already published at line 74/92; restated only so the order is complete |

## Evidence basis, and its limits

* **O-3 and O-6 match measured reference records**: `selector-unbound` with `universe: null`
  (`syntax-code`), and `coverage-unknown` with `universe` = source universe and `nativeCause:
  body-language-owner-unenumerated` (`rust-partial`). Both are §9.5-item-1 shaped.
* **O-1 and O-4 have no measured reference instance** in the five runs —
  `missing-relation-coverage` and `uncovered-expected-source-subject` appear on the consumer side
  only. Their fields here are **proposals**, not observations. This is why O-4's `universe` is
  marked **[DECISION]**.
* **O-7's scan order is an arbitrary choice.** Some deterministic rule is required; this one is
  the least surprising given §4 line 88 already fixes the `DEPENDS_ON` order. Root should confirm
  or replace it.
* Nothing here is added to make the existing reference pass. If root prefers different answers at
  O-1/O-3/O-4/O-7, the reference — not the contract — is what would then need correcting, and this
  check found no other point where the reference contradicts explicit law.

## Decisions reserved for root

1. O-1 vs O-3 as one cause or two, and which name each takes.
2. O-4's `universe`: *U* or null.
3. Whether O-4/O-5 **stop** or accumulate into O-6.
4. O-7's carrier-selection order.
5. Whether this block belongs in §4 (proposed, beside the pairing law it depends on) or in §7
   beside the cause registry.

**No source file was edited. This draft is not applied.**
