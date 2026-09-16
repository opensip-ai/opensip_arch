# Bounded normative-publication check — outgoing native-completeness atom causes

**Standing.** Actual Claude source-author origin `823bf66b-…`, READ-ONLY. Not the independent
reviewer, not the blind consumer. **No acceptance.** No source edit, no consumer contact, no
remint, no freeze. Writes confined to this runtime.

**Method.** Normative-only kit: 169 files — published contracts (`.md`) and schemas/registries
(`.json`) under `docs/v2/contracts/` and `docs/coop/design-corrections/`. **Every `.py` is
excluded**, and so are `reviews/`, `disposable/`, `before-image*/`, `quarantine*/`. Where I cite
reference behaviour I say so explicitly and never treat it as normative.

---

## 1. Root's objection to RC-3 is correct. I retract my classification.

I classified RC-3 "factually settled … regardless of any publication question". That reasoning was
wrong, for exactly the reason root gives: **a binding is not Coverage**, and I reached "factually
wrong" only via `atom_model.v1.py:1437` — reference Python, outside the normative kit.

**Census result.** In the whole normative-only kit, `missing-relation-coverage` and
`selector-unbound` occur **6 times each, and every single occurrence is a bare enum/list membership
entry**:

| Selector | Form |
|---|---|
| `foundation/atom-evaluation-contract.v1.md:147` | membership list of the native registry |
| `foundation/evaluator-projection-registry.v1.json` `$defs/AtomCauseCodeV1/enum` (:1181, :1184) | enum items |
| `foundation/identity-schemas.v3.json` :3320/:3334, :3487/:3493, :4888/:4894 | enum items + registry list |
| `workflows/schemas/policy-document.v2.schema.json` :891/:894 | enum items |

The owning registry `identity-schemas.v3.json#/x-opensip-evaluator-deficiency-registry` is
**flat string lists** — measured `anyPerCauseConditionObject: false` — and its `causeLaw` states
only closed membership, `evidenceKind`/`nativeCause` carrier typing, gating derivation, and
"Unknown record shape is refused, never coerced to a cause." `AtomCauseCodeV1` carries one
`description`, which is a **classification** statement, not per-member conditions.

**No clause anywhere states the emission condition for either cause.**

### Are two different cause records consistent with the prose on the exact consumer input?

`syntax-code`, relation `unresolved-edge`, capability `unresolved-edge`: the consumer's retained
EnumerationPlan holds **one binding with `universe: null`**, and no Coverage exists for that
relation at that rung.

Published prose eliminates exactly one candidate: §4 line 74 — *"`unavailable-program-binding` is
an **incoming/global search** concern"* — so that is not available outgoing. It does not choose
among the rest. On the plain reading of the published names and the facts:

* **`missing-relation-coverage`** — there is no Coverage for this relation. **Consistent.**
* **`selector-unbound`** — no available binding at the subject's universe, so the selector is
  unbound. **Consistent.**
* **`uncovered-expected-source-subject`** — the expected source subject is uncovered.
  **Arguably consistent** (nothing published excludes it here).

**Answer: no, it is not determined without `atom_model.v1.py`, and at least two records are
consistent with the prose.** RC-3 is **genuine underspecification**, not a consumer violation.
`scope-without-coverage` is not among the candidates: §4 line 74 conditions it on *"each containing
scope without a paired Coverage"*, and here there is no containing scope.

## 2. What *is* fully published — the shape, and the channel split

Two things I expected to be gaps are in fact completely published, and this narrows the amendment
sharply.

**(a) The causes-vs-`nativeDeficiencies` discriminator is published and partitions cleanly.**
`atom-evaluation-contract.v1.md:137` — *"Native `DeficiencyV2` values from `sufficiency_v2` are a
**separate** `nativeDeficiencies` array"* — plus `AtomCauseCodeV1.description` — *"Native
deficiencies from sufficiency_v2 stay in nativeDeficiencies and use DeficiencyV2 membership; they
are **NOT overloaded here**."* Measured: `AtomCauseCodeV1` (31 members) ∩ `DeficiencyV2`
(9 members) = **∅**. So membership alone decides the array:

* `coverage-unknown`, `missing-relation-coverage`, `selector-unbound`,
  `uncovered-expected-source-subject`, `scope-without-coverage`, `population-unknown`,
  `unavailable-program-binding` → AtomCauseCodeV1 only → atom `causes`.
* `required-relation-missing`, `language-tier-unsupported`, `input-closure-incomplete`,
  `budget-exhausted` → DeficiencyV2 only → `nativeDeficiencies`.

**This closes root's RC-1 bound-check question: `coverage-unknown` belongs in `causes`, not
`nativeDeficiencies`, and the reference is consistent with published law on that axis. No reference
correction is required there.**

**(b) `evaluator-composition-contract.v3.md` §9.5 items 1-3 publish all three record channels
completely** — atom `causes[]`, atom `nativeDeficiencies[]`, and the per-Coverage typed cause from
`entry.deficiency` (item 3, with `inputRefs` overwritten to that Coverage and `universe` = Coverage
key `sourceUniverse`).

**Measured consequence.** All **16** disputed deficiency records across `syntax-code` and
`rust-partial` — consumer and reference alike — are **§9.5-shape-legal**, all in the atomEI channel
(item 1/2). The consumer's `required-relation-missing` even carries the `universe: null` that item 2
mandates. **The disagreement is entirely in the atom's `causes[]` *content* — the one thing not
published.**

## 3. Bound-check of the whole outgoing native-completeness branch

| Decision point | Published? | Selector |
|---|---|---|
| Partition pairing (containment; `subject_scope_commitment` **or** `coverageScopes`; no fallback) | **yes** | atom §4 L74 |
| Containing scope with no paired Coverage → `scope-without-coverage`, accumulating | **yes** | atom §4 L74 |
| `unavailable-program-binding` excluded outgoing | **yes** | atom §4 L74 |
| Cross-family unavailable → `cross-family-edge-not-owed`, non-blocking | **yes** | atom §4 L74, L92 |
| Recursive `DEPENDS_ON` in the sufficiency view; all `su.causes` retained | **yes** | atom §4 L88 |
| `causes` vs `nativeDeficiencies` array | **yes** | atom §7 L137; `AtomCauseCodeV1.description` |
| Record field derivation for all three channels | **yes** | composition §9.5 items 1-3 |
| **Cause when no owed binding / no available binding at U** | **NO** | — |
| **Cause when no containing scope exists at all** | **NO** | — |
| **Cause when sufficiency is unsatisfied** (`coverage-unknown`), and its `nativeCause`/`universe` | **NO** | — |
| **Branch order: early-return vs accumulate** | **NO** | — |

Four omissions, all in one branch. That is why a single clarification closes them together rather
than fixing causes one at a time — which is the shape root asked for. The ordering gap has
observable consequence: on `syntax-code rule.unresolved-edge-advisory` the consumer emitted 4
records and the reference 2, sharing 1.

**Scope note.** `missing-relation-coverage` and `uncovered-expected-source-subject` appear on the
**consumer side only** in all five runs; I have **no measured reference instance** of either, so I
state no reference field values for them.

## 4. Effect on my earlier findings

| | Earlier | Now |
|---|---|---|
| RC-1 coverageIds must include the `DEPENDS_ON` partition | consumer violation | **unchanged** — atom §4 L88 is explicit (root agrees) |
| RC-1 the `coverage-unknown` record that accompanies it | implied consumer violation | **split out: underspecified** (§3) |
| RC-2 `uncovered-expected-source-subject` | consumer deviation | **underspecified** for the "no containing scope" branch; the L74 *pairing* rule it rests on remains published |
| RC-3 `missing-relation-coverage` vs `selector-unbound` | "factually settled" | **RETRACTED — genuine underspecification** |
| RC-4 composite `scopeIds` | consumer violation | **unchanged** (root agrees) |
| RC-6 `matchingImportCount` | consumer deviation | **strengthened** — composition **L44** and **L261** publish the count law exactly: *"counts = distinct union of descendant atom **known** matches (not uncertain)"* |

## 5. Source conclusion

**A normative amendment IS required**, and it is a publication gap, not a semantic defect: the
reference's behaviour is self-consistent and nothing in it contradicts explicit law on these four
points. **No reference correction is indicated by this check.** The amendment draft is
`amendment-draft.md` in this runtime — contract text only, implementable from published inputs, no
Python name load-bearing.

**Genuinely independent semantic decisions requiring review** (I propose, I do not decide):

1. Whether "no owed binding at all" and "no available binding at U" are **one** cause or two.
2. Which cause the second gets — the two names are near-synonyms on their face.
3. Whether the branch **short-circuits or accumulates**; this changes record cardinality.
4. The `nativeCause` carried by `coverage-unknown`: the reference carries a non-null owner
   `NativeCause` (measured: `body-language-owner-unenumerated`), selected from the view. Which
   entry supplies it, when several could, is an arbitrary choice that must be made deterministic.
5. Whether `uncovered-expected-source-subject` carries `universe: U` or null.

## 6. Corrections to my previous diagnosis, and limits

* **S-3 withdrawn.** My "no `aggregateTermination` record" rested on an **invented key-name
  search**, not on actual envelope fields. It establishes nothing. Root holds exact final20
  multistep/termination controls and owns that assessment; I make no claim there.
* **Public-manifest observation corrected.** The path I reported missing was the **runtime** path.
  The actual live public receipt exists:
  `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/consumer-b.v20/final-public-artifact-manifest.json`,
  sha256 `39d2aa561757c439d9124067604adb83ac4e7591eeb28c0135fa750ccfffaa9b`, 271 300 bytes, 987
  files, `subjectManifestSha256 1cf3db70…`. **My earlier observation must not be relabelled as
  absent retention** — it was a wrong path on my part.
* I did not re-run any suite and did not re-derive the five proofs; §2's record test uses the
  preserved root derivation.
* I read the atom contract in full and targeted sections of composition, plus the registries. I did
  **not** re-read the whole charter or the whole native chapter; "no clause anywhere" is scoped to
  the 169-file normative-only kit and the eight cause tokens censused.
* Whether the consumer placed a code in the wrong *array* is **not observable** from
  `ruleResults[].deficiencies`, where §9.5 merges all three channels. I therefore make no claim
  about the consumer's internal array placement.
* No acceptance of any kind is given or implied.
