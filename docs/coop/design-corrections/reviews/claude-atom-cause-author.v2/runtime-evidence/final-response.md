All four issues rechecked against the final v1 bytes by execution, not by reading. **None was already fixed.** Three were defects in my v1 *prose*; one was a real reference defect.

## Root's four issues

**1 — shared no-owed-bindings return.** Confirmed: the `missing-relation-coverage` return sits before the endpoint split, so incoming takes it too. My "incoming never returns early" was wrong. §4 now has a **Shared prelude (both endpoints)** — P1 unavailable-binding scan, P2 no-owed-binding return — and the incoming claim is conditional on it. Outgoing steps renumber 1–4.

**2 — both incoming cross-family shapes.** Confirmed by execution: incoming returns `(cross-family-edge-not-owed, null)` from the prelude *and* `(…, UR)` from per-universe accumulation, value `true` — neither blocking. Both routes are now named, plus the case you asked to preserve: same-family unavailable is **blocking incoming** (`unavailable-program-binding` + unknown) while outgoing emits nothing and is not poisoned.

**3 — selection order through scope pairing — the one real defect.** Your counterexample reproduces against v1 bytes `b05642b2…`: the combined list came out `[coverage2:2222…, coverage2:1111…]`, carrier `input-closure-incomplete/lockfile-missing` instead of `budget-exhausted/null`. Fixed your way — `_unique_pairs` now dedups **and** sorts ascending by Coverage id, and `_coverages_for_current_source` routes its combined list through it, i.e. sorting after pairing/dedup. Re-run on `a5e082a5…`: `MISMATCH_PRESENT: false`, both orientations ascending, same carrier. Reported as a helper-boundary spec/reference mismatch on synthetic inputs — **not** a full-Run failure.

**4 — whole-record fold.** Rule 3 now spells out: fold starts from the first partition's entire entry; only strictly-worse replaces, so ties retain the earliest; `resolutionCompleteness` and `closedWorld` replace **whole** (their nested fields arrive together from the winning record and are *not* independently ranked); ordered union; whole typed carrier; `resolution` and `rungUnavailableBecause` stay from the first partition.

## The three smaller corrections

`universe` now has its own paragraph: `AtomCauseV1.universe` optional+nullable with the key omitted, projecting through the composition recipe to the required-nullable `evaluation-deficiency.universe`. `universe: null` is identified as the logical/projected value, not a different atom serialization; schemas and recipe untouched. The "partition census" rationale is **deleted** — step 3 now says only that evaluation stops before evaluating any paired sibling. "One per unpaired scope" is scoped to accumulation before §7/composition dedup.

## v1 report scope, corrected (v1 preserved unedited)

- "no fixture in the retained corpus reaches it" — **withdrawn as unsupported.** I replayed one retained fixture Run plus the affected checks; those did not demonstrate a full-Run failure. Nothing is established about fixtures I did not run.
- `a2-surfacing` relabelled: synthetic atom inputs, **atom-cause surfacing** — not a proof, not an admitted Run.
- The 169-file census is a current-contract census of this tree, **not** the 102-file blind kit, and token presence isn't implementability. Replaced with clause-location evidence for the amendment's load-bearing citations only (all 10 resolved to file + JSON pointer).
- Counts preserved as observed: v1 70→76; v2 76→81.

## Controls and checks

81/81 pass. Across three models (v2 / v1-final / frozen33), **only** `test_same_kind_multi_scope_selection_is_ascending_coverage_id` discriminates the v1→v2 delta — the four others pass everywhere because issues 1, 2 and 4 were prose defects. The fold-record control asserts against `_conservative_entry` directly, since those fields aren't otherwise observable.

Re-ran only what the model edit justifies: the six atom-model consumers, all exit 0 and **byte-identical to v1-final**; plus the retained fixture Run 8× → `run3:ecb44874…` / proof `c18f225f…`, unchanged. The six broad groups were not run.

Custody: 12 899 files, nothing added, the same three files changed. v1, the root review runtime and frozen33 have zero files modified. No checker file added — `check-atoms.v1.py` is already job `atoms` in `run-evaluator3-checks.py`, so **no pin addition is owed**; the same 15 pin entries carry new digests, no ledger edited.

Deliverables: `assessment.md`, `assessment.json` (`9b4add31…`), `changed-file-handoff.json` (`013bc08c…`), before/after images, 20 receipts including the one failed probe attempt. No acceptance claimed.
