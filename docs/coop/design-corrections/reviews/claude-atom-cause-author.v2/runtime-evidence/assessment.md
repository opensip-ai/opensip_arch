# v2 — bounded correction of the v1 atom-cause handoff against root's draft review

**Standing.** Architecture/design/reference authorship by the actual Claude source-author origin
`823bf66b-e92a-4789-ab81-63a1a9dc371d`. Written only to this runtime and to the existing isolated
copy `/tmp/opensip-design-corrections/atom-cause-successor.v1/source`. No frozen33, live-repository,
history, pin-ledger, planning-layer or prior-v1 edit. No product implementation, commit, push or
acceptance. No consumer implementation or output, and no root blind diagnostic, was used as an
input.

**Interpreter for every command:** `/tmp/opensip-architecture-review-env/bin/python -I -B`. Every
command, stdout, stderr and exit is retained under `probes/receipts/<label>/`; a repeated label
takes a numeric suffix, so failed attempts survive.

**Baseline.** v2's BEFORE is the v1 FINAL handoff, confirmed byte-equal before any edit
(`before-hashes.json`, `equalsV1Final: true` on all three files).

---

## 1. Root's four issues — rechecked against the final v1 bytes

None was already fixed. Three were **prose** defects over behaviour the reference already had; one
was a real **reference** defect. Each was re-derived by executing the final v1 bytes, not by reading
alone.

### Issue 1 — the no-owed-bindings return is shared, so "incoming never returns early" was wrong

**Confirmed.** `_native_completeness` computes owed bindings, runs the unavailable-binding scan, and
returns on `missing-relation-coverage` **before** the `endpoint == "source"` branch. Executed
(`b2-prelude-cross-family`): with no owed binding for the relation, **both** endpoints return
`indeterminate`, `missing-relation-coverage`, `universe` projecting to null, `scopeIds` and
`coverageIds` empty.

**Fix (prose).** Section 4 now has a **Shared prelude (both endpoints)** with P1 (unavailable-binding
scan) and P2 (no owed binding → `missing-relation-coverage`, return), stated as reached *before the
endpoint split*. The incoming paragraph now opens "After the shared prelude — **including P2's
return, which incoming takes** — incoming makes **no further** early return". The outgoing steps
renumber 1–4.

### Issue 2 — incoming carries both cross-family shapes

**Confirmed.** Executed with an unavailable rust binding **and** an available rust binding at *UR*,
incoming returns both records: `("cross-family-edge-not-owed", null)` from the prelude and
`("cross-family-edge-not-owed", UR)` from the per-universe accumulation, with value `true` — neither
is blocking. Outgoing shows only the null one, since its per-universe loop does not run.

**Fix (prose).** The incoming paragraph now names **both routes** and says both are retained and
non-blocking, and adds the case root asked to preserve: an owed **same-family** unavailable binding
is different and stays **blocking incoming** (`unavailable-program-binding` plus `unknown`), while
outgoing emits nothing for it and is not poisoned. Executed and controlled
(`test_same_family_unavailable_blocks_incoming_only`: outgoing `true` with no such cause, incoming
`indeterminate` with it).

### Issue 3 — ascending Coverage id did not survive scope pairing — **a real reference defect**

**Confirmed, and reproduced.** Root's retained helper counterexample runs against the v1 bytes in
this runtime (`b1-repro-before`, source sha `b05642b2…`): two scopes over the **same** subject and
**same** source kind, with `coverageScopes` mapping the higher Coverage id to the lower scope id.
`_coverages_for_current_source` and `_select_dep_coverages` walk scopes ascending and concatenate
each scope's matches, so the combined list came out **descending** —
`[coverage2:2222…, coverage2:1111…]` — and `_conservative_entry` produced the carrier
`input-closure-incomplete / lockfile-missing` where the published ascending-Coverage-ID fold gives
`budget-exhausted / null`. The aligned-tag fixtures in v1 concealed exactly this branch.

This is a **specification/reference mismatch at a helper boundary on synthetic helper-only inputs**.
It is **not** an admitted full-Run failure and is not reported as one.

**Fix (reference), keeping root's preferred simple global rule.** `_unique_pairs` now deduplicates
**and sorts ascending by Coverage id**, and `_coverages_for_current_source` routes its combined
`paired` list through it. Sorting happens **after pairing and dedup**, which is the list the fold
actually reads. Re-executed (`b1-repro-after`, source sha `a5e082a5…`): both the reversed and the
aligned orientation now yield ascending selection and the same carrier `budget-exhausted / null`,
`MISMATCH_PRESENT: false`.

**Fix (prose).** The selection-order block now states that the order a fold reads is the **final
combined list** after pairing and dedup, explains why a per-scope walk can hand it a descending
order, and directs: deduplicate and sort ascending by `coverage2`; do not rely on the scope walk.
Scope order stays ascending `scope2` for `scopeIds` and for deciding unpaired scopes; a Coverage
paired by more than one containing scope appears once.

### Issue 4 — whole-record replacement and tie retention were not spelled out

**Confirmed** by reading `_conservative_entry` and then pinning it with a control.
`resolutionCompleteness` and `closedWorld` are replaced as **entire records**, only on a strictly
worse rank of `state` / `exportsClosed`; ties retain the incumbent whole record; `resolution` and
`rungUnavailableBecause` are never folded and keep the first partition's value.

**Fix (prose).** Fold rule 3 is now a field-by-field list stating: the fold starts from the first
partition's **entire entry**; a later partition changes a field only when **strictly worse**, so
every tie retains the earliest partition; `coverage` and `confidenceMillionths` are scalar;
`resolutionCompleteness` is replaced **whole**, so `attempted`, `examinedExhaustive`,
`stageTerminal`, `unresolvedEdgeCount` and `unresolvedEdgeClasses` arrive **together from whichever
single partition won on `state`** and are **not** independently worst-ranked; `closedWorld` likewise
whole, with its five companion fields riding along and ties keeping the incumbent;
`derivationKinds` is the ordered union; the typed `(deficiency, nativeCause)` carrier is taken
**whole** from the first partition with a non-null `deficiency`; every remaining field, including
`resolution` and `rungUnavailableBecause`, keeps the first partition's value.

---

## 2. The three smaller corrections root named

**`universe` representation.** A new **Cause representation (`universe`)** paragraph states the
boundary: `AtomCauseV1.universe` is **optional and nullable** and the atom record carries the key
only when there is a universe to report; the composition/replay projection reads it with a
defaulting get and writes `evaluation-deficiency`, whose `universe` is **required and nullable**, so
an omitted atom key becomes an explicit `null` there. Where section 4 writes `universe: null` it
names that **logical, projected** value, not a different atom serialization. Both schema locations
are resolved in `b7-clause-citations` (`AtomCauseV1` — `universe` present in `properties`, absent
from `required`; `evaluation-deficiency` — `universe` in `required`). Neither schema nor the recipe
changes.

**Unsupported rationale removed.** The v1 sentence claiming that citing a paired Coverage "would
assert a partition census that was not established" is **deleted**. Outgoing step 3 now says only
what happens: `coverageIds` is empty **because evaluation stops here without evaluating any paired
sibling's Coverage**. Nothing is asserted about what an evidence reference means.

**"One per unpaired scope."** Now explicitly a statement about **accumulation**: the returned
`causes` is then deduplicated and ordered by §7 and the composition Cset law, where identical
records collapse. What the rule fixes is that the cause is accumulated at all and that `scopeIds`
still names every containing scope.

---

## 3. Correcting the v1 report's scope (v1 itself is preserved, unedited)

| v1 statement | correction |
|---|---|
| "no fixture in the retained corpus reaches it" (§4 and §9.4 of `v1/assessment.md`) | **Unsupported — I did not replay the retained corpus.** What was actually executed is one retained reference fixture Run and the affected checks; **those did not demonstrate a full-Run failure**. Nothing was established about fixtures that were not run. |
| `a2-surfacing` described as surfacing "as a proof cause" | It builds **synthetic atom inputs** and reads the atom result. It is **atom-cause surfacing**, not a proof bundle and not an admitted retained Run. |
| §8 "Implementability from the normative-only kit", 169 files, `tokensOnlyInThisContract: []` | The 169-file set is a **current-contract `.md`/`.json` census of this tree**; it is **not** the 102-file blind kit, and token presence alone is **not** implementability. v2 replaces the claim with narrower, stronger evidence (`b7-clause-citations`): each **load-bearing** citation resolves to an exact file and JSON pointer with its enum/required list printed. That supports those clauses only and makes no claim about any other kit boundary. |
| observed counts | preserved as observed: v1 took `check-atoms.v1.py` from **70 → 76** cases. v2 takes it **76 → 81**. |

The distinction root asked to preserve is kept throughout: **randomized process sampling of
synthetic inputs** (v1's `a1`/`a2`/`a4`) is reported separately from the **retained real fixture
Run** (v1's `a3`/`a9`, v2's `b4`), which was stable in every execution.

---

## 4. Changed files

Custody (`b6-custody-pins`): 12 899 files both sides, none added, none removed, exactly three differ
from frozen33 — the same three v1 touched. The temporary baseline image `b3` loads inside the
foundation directory is removed in a `finally` block, and this custody run is the check that nothing
was left behind (`onlyInSuccessor: []`).

| path | v1 final sha256 | v2 sha256 | bytes |
|---|---|---|---|
| `foundation/atom-evaluation-contract.v1.md` | `0a3fe11d2150…` | `2d7c25948856…` | 31 923 → 35 755 |
| `foundation/atom_model.v1.py` | `b05642b2d06f…` | `a5e082a5490d…` | 92 277 → 93 272 |
| `foundation/check-atoms.v1.py` | `77786e887abd…` | `c5de4a84167f…` | 102 550 → 111 998 |

Before-images `before/`, after-images `after/`. Reference diff, in full:

```
 def _unique_pairs(pairs: list) -> list:
+    """Dedup by Coverage id, then ASCENDING Coverage id (contract section 4, selection order)."""
     ...
-    return out
+    return sorted(out, key=lambda pair: pair[0])

 def _coverages_for_current_source(...):
     ...
-    return paired, [s for s, _ in containing], unmatched
+    return _unique_pairs(paired), [s for s, _ in containing], unmatched
```

No `[DECISION]`, `TODO`, `TBD` or `XXX` in the contract, and no surviving "never returns early".

---

## 5. Controls

`check-atoms.v1.py`: **76 → 81** cases, `ok: true, passed: 81, failed: 0`
(`probes/receipts/check-atoms-v2/stdout.txt`). Five added:

| control | what it pins |
|---|---|
| `test_no_owed_binding_return_is_shared_by_both_endpoints` | issue 1 — the return fires at both endpoints, universe projects to null, refs empty |
| `test_incoming_keeps_both_cross_family_shapes` | issue 2 — `(null)` and `(S)` both retained, non-blocking |
| `test_same_family_unavailable_blocks_incoming_only` | issue 2 — blocking incoming, silent outgoing |
| `test_same_kind_multi_scope_selection_is_ascending_coverage_id` | issue 3 — two same-kind scopes over one subject, **deliberately reversed** scope-vs-coverage mapping, both endpoints |
| `test_dep_fold_replaces_whole_records_and_keeps_ties` | issue 4 — whole-record RC replacement on worse `state`, whole-record CW **tie retention**, ordered union, `rungUnavailableBecause` from the first partition, minimum confidence, every partition cited |

`b3-controls-discriminate` runs all eleven added controls (v1's six and v2's five) against three
models — v2, the v1-final BEFORE image, and frozen33:

| control | v2 | v1-final | frozen33 |
|---|---|---|---|
| `test_same_kind_multi_scope_selection_is_ascending_coverage_id` | pass | **fail** (`no-program-unit`) | **fail** |
| `test_dep_fold_carrier_is_first_partition_in_selection_order` (v1) | pass | pass | **fail** |
| the other nine | pass | pass | pass |

Read plainly: **only issue 3 changed behaviour.** Its control is the only new one that discriminates
the v1→v2 delta, and it does so deterministically — within one process the install order fixes the
map order. The four controls for issues 1, 2 and 4 pass on all three models because those issues
were defects in the v1 *prose*, not in the reference; their job is to stop the corrected prose and
the reference drifting apart. `test_dep_fold_replaces_whole_records_and_keeps_ties` asserts against
`_conservative_entry` directly, because the folded record's fields are not otherwise observable —
and those fields are exactly what root asked to make implementable without Python.

## 6. Checks re-run, and why only these

Justification: `_unique_pairs` and `_coverages_for_current_source` changed, so every checker that
imports `atom_model.v1.py` — directly, or through `evaluator_replay_model.v3.py` /
`provider_attribution_return_model.v2.py` — is affected. The contract `.md` is executed by no
checker. **The six broad reference groups were not run; root runs those after pin reconciliation.**

| check | exit | identical stdout to v1-final |
|---|---|---|
| `check-atoms.v1.py` | 0 — 81/81 | no, by exactly the five added cases (76 shared results unchanged) |
| `check-replay.v3.py` | 0 | yes |
| `check-semantic-replay.v3.py` | 0 | yes |
| `check-candidate-replay.v3.py` | 0 | yes |
| `check-execution-replay.v3.py` | 0 | yes |
| `check-execution-inputs.v1.py` | 0 | yes |
| `check-provider-attribution-return.v2.py` | 0 | yes |

Retained fixture Run, replayed end to end 8× after the v2 edits (`b4-realrun-after-v2`, atom model
`a5e082a5…`): `run3:ecb4487410dc…`, proof `c18f225f2a11…`, verdict fail, 3 findings, 3 predicates —
identical to the v1 before/after and frozen33 baselines, stable across processes. **This is one
retained fixture, not the retained corpus, and not a claim of complete Run parity.**

## 7. Pins and runner wiring

No checker file was added — the controls extend the existing `check-atoms.v1.py`, which is
**already** wired as job `atoms` in `foundation/run-evaluator3-checks.py`. So **no pin addition is
owed**; the same **15** pin entries as v1 simply carry new digests, across
`native/source-pins.v2.json` and `security/source-pins.v1.json` (`pins/1069`, `1070`, `1073`) and
`workflows/source-pins.v1.json`, `foundation/source-pins.v1.json`,
`foundation/evaluator3-source-pins.v1.json` (`files/1069`, `1070`, `1073`). Full before/after
digests in `changed-file-handoff.json`. No ledger was edited.

## 8. Limits of what was executed here

1. **Not acceptance.** Root owns pin reconciliation, the full groups, and any acceptance decision.
   Full reference validation and independent reviews remain pending.
2. **One retained fixture Run** was replayed. The retained corpus was not replayed; no statement is
   made about fixtures that were not executed.
3. **Root's counterexample and its repro are synthetic helper-only inputs** — not native-schema
   admitted Coverage, not a proof, not an admitted Run. The issue-3 defect is a real
   specification/reference mismatch at a helper boundary, demonstrated at that boundary only.
4. **`b7-clause-citations` covers the amendment's load-bearing citations only.** It is not a kit
   census, not the 102-file blind kit, and not a claim that any other consumer boundary is
   implementable.
5. **The six broad reference groups were not run** here, by instruction.
6. **`ViewEntryV3.coverage` is a two-member enum** (`complete`, `unknown`), while
   `_conservative_entry` ranks an intermediate `partial` and several **pre-existing** checks build
   `coverage: "partial"`. Unreachable on admitted input; reported in v1 and still deliberately
   unchanged, since it is outside this correction and would alter unrelated retained checks.
7. **No new cause tokens or public fields.** `AtomCauseCodeV1`, `DeficiencyV2`, `NativeCause`, the
   three published deficiency channels, and the `AtomCauseV1` / `evaluation-deficiency` schemas and
   projection recipe are all untouched.
