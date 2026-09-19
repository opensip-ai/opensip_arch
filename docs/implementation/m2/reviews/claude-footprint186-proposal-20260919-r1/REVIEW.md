# Proposal assistance — 186: complete store-transition recovery table, prepared-evidence representation, floor freshness

Reviewer: Claude. 2026-09-19. **Assistance only** — not a frozen-byte review, not acceptance, not implementation approval, no cumulative approval. No candidate, frozen, selected or repository file was edited; I did not look at any 185 or 186 draft. Tree used: my verified 181 extraction (`claude-phases181-20260919-r1/…/candidate`; writer model byte-identical since 175).
Evidence: `claude-out/footprint_table_probe.py` → `footprint_table_summary.txt` (headline) and `footprint_table_full.txt` (all 168 rows: state, proposed action, reachability, current model's answer). Three earlier runs of the probe failed on my own assertions and are preserved as `…-r1/-r2/-r3-FAILED.py`; each failure was informative and changed the proposal (image relevance is narrower than I first wrote — see §3).

## 0. The precondition nobody has written down: a write-order law

The journal state and the store footprint are **two** durable records. Whether a combination is "lawful lag" or "contradiction" depends entirely on which is written first at each step, and no owner states that today (S9 gives the footprint steps; S9.2 gives journal states; neither orders them against each other). Every table — the current one included — silently assumes an order. I therefore state one, **W**, and derive everything from it mechanically; if the owner prefers a different order the probe regenerates the table by editing one list.

**W** (store operation, first pass): `j=LEASED` → `j=PREPARING` → new root created (`migrating/None` → `/PREPARING` → `/PREPARED`) → `j=PREPARED` → **prepared floor image durable** → old store fenced `RESTORED` → new `migrating/COMMITTED` → `j=COMMITTED` → rename to `final` → `j=DONE` → slot retirement.
**Abort** is lawful only while the old store is *not* `RESTORED`: delete migrating root (and image) → `j=ABORTED`.
Principle: the journal **leads** into the stage that starts creating effects (`PREPARING`) and **follows** facts (`PREPARED`, `COMMITTED`, `DONE`, `ABORTED`); `RESTORED` additionally requires `j=PREPARED` and the image. W is chosen because it is the only order under which the existing S9.2 rule "LEASED/PREPARING → ABORT without consulting the footprint" is sound.

## 1. What the current model does over the full product (measured)

Product: 6 journal states × {old unfenced, RESTORED} × 7 new-store shapes × {image absent, present} = 168. Under W, 23 are reachable crash points; 145 are contradictory.

- **139 of the 145 contradictory states are not quarantined** by the unchanged model: 54 ABORT, 56 RELEASE-ONLY, 29 RESUME-COMMIT. **32 are ABORT with the old store already `RESTORED`** (my 181 F-1, now complete: every `LEASED`/`PREPARING` journal with a fenced old store, plus `PREPARED` with `migrating/None|PREPARING`). **25 are `COMMITTED` journals resumed without reading the footprint** (including `both`, `absent`, `migrating/PREPARING`, and an unfenced old store). The 56 RELEASE-ONLY are `DONE`/`ABORTED` journals released whatever the stores look like (e.g. `ABORTED` with a fenced old store and no new store).
- **One reachable state is wedged**: `j=PREPARED`, old unfenced, new `absent` — a crash *inside abort*, after the migrating root was deleted and before `j=ABORTED`. The model answers `QUARANTINE / MIGRATION.CORRUPT`. Nothing is wrong with that installation; abort merely needs to finish. (The owner vector `crash-at-prepared-store-operation-without-a-footprint-quarantines` covers a *missing footprint observation*, which is a different thing and should stay a refusal — see §4.)
- The model cannot see the prepared image at all (the footprint has no such member), so 181's "missing prepared evidence" law has nothing to bind to.

## 2. Precedence (unchanged where it exists; two additions)

1. Journal closed shape / known state — else `QUARANTINE MIGRATION.CORRUPT`. *(existing)*
2. Fence held — else `REFUSE TRANSITION.FENCE_NOT_HELD`. *(existing)*
3. Live registry == frozen registry and digest — else `QUARANTINE`. *(existing)*
4. Exact journaled lease set re-acquired — else `BUSY PROJECT.BUSY`. *(existing)*
5. **Store operation only: footprint observation available** — else stop `unknown-custody` at the composition (§4); the model is never called with a missing observation. *(new placement; today a missing dict is `QUARANTINE`, which 181's own text says is wrong for merely unreadable evidence)*
6. Journal × footprint table (§3). *(replaces: footprint consulted only for `PREPARED`)*
7. **Image check, only in the two cells that need it** (§3). *(new)*
Registry and lease checks stay *before* the footprint on purpose: BUSY must not be masked by, or leak, footprint diagnostics, and a registry mismatch already makes the footprint uninterpretable. Terminal journals keep passing 3–4 (181 kept exact lease re-acquisition for terminal states).

## 3. Proposed complete table (store operations; `both` is always `QUARANTINE`)

| journal | old unfenced | old `RESTORED` |
|---|---|---|
| `LEASED` | new `absent` → **ABORT**; anything else → QUARANTINE | always QUARANTINE |
| `PREPARING` | new `absent` or `migrating/{None,PREPARING,PREPARED}` → **ABORT**; `migrating/COMMITTED`, `final` → QUARANTINE | always QUARANTINE |
| `PREPARED` | `migrating/PREPARED` → **ABORT**; `absent` → **ABORT** (abort-in-progress, idempotent — fixes the wedge); else QUARANTINE | `migrating/PREPARED` → **RESUME-COMMIT** from step 3 *if image present and matching*; `migrating/COMMITTED` → RESUME-COMMIT from step 4 *(same image condition)*; image absent → **unknown-custody**; image mismatching → QUARANTINE; **every other shape → QUARANTINE (never ABORT)** |
| `COMMITTED` | always QUARANTINE (a commit marker cannot exist over an unfenced old store) | `migrating/COMMITTED` → **RESUME-COMMIT** step 4 (image condition as above); `final` → **RESUME-COMMIT, journal-only** (only `j=DONE` remains); else QUARANTINE |
| `DONE` | always QUARANTINE | `final` → **RELEASE-ONLY**; else QUARANTINE |
| `ABORTED` | new `absent` → **RELEASE-ONLY**; else QUARANTINE | always QUARANTINE |

Probe-verified properties: total over all 168 states; safe (expected action) on all 23 reachable states; QUARANTINE or unknown-custody on every contradictory one; **no ABORT anywhere with `old=RESTORED`**.

- **ABORT boundary** = the `RESTORED` fence, not the journal state and not the new-store state. The current `migration_recover` tests the new-store state *first* and only then looks at the old store; the order of those two tests is the whole of 181 F-1. Its rationale string "old state untouched" should be asserted, not assumed.
- **Terminal RELEASE-ONLY** becomes conditional: `DONE` requires `RESTORED + final`; `ABORTED` requires unfenced + absent. A terminal journal over any other store shape is a contradiction and must not be retired (retirement would destroy the only evidence of what was attempted). This is stricter than today and is the one place where the read-only observer is affected: it currently passes a coherent terminal journal on internal checks alone. I would **not** make readers consult the store footprint (they hold no store custody); say instead that the reader barrier judges the *journal* and the executor judges journal × footprint — and accept that a reader can pass a terminal journal an executor will later quarantine.
- **Image relevance is narrow** (this is what my failed r1/r2 runs taught me): it decides only `old=RESTORED ∧ new=migrating`. Before `RESTORED` a stray image is garbage that abort deletes; once the new store is `final` the image has been consumed. Do not make image presence a global invariant.
- **Core operations** keep the existing journal-only table (`PREPARED` → ABORT: published generation never selected). **Open question Q1:** a `core-update`/`core-rollback` whose schema changes "selects a new store generation" (S9.2) — if that path ever fences an old store, it needs this table too; `STORE_OPERATIONS` is only the two store commands today. I could not settle this from the prose.
- **W-dependence to decide (Q2):** `j=PREPARED + RESTORED + final` is unreachable under W (journal `COMMITTED` precedes the rename) and so quarantines; today it is RELEASE-ONLY. If the owner wants rename-before-journal, flip that one step in W and the cell becomes a lawful journal-lag resume. Either is fine; it must be chosen.
- `old.present = false` is carried in every footprint and read by nothing. Either define it (an old store that vanished after `RESTORED` but before `final` is custody loss) or remove it from the shape.

## 4. Representing unavailable prepared evidence — recommendation: wrapper observation, no closed-schema successor

Facts: `TransitionRecoveryV1.action` is a closed enum `{ABORT, RESUME-COMMIT, RELEASE-ONLY, QUARANTINE, BUSY, REFUSE}` and `MigrationRecoveryV1.action` a closed enum; both objects are `additionalProperties:false`; the refusal-code list is closed; the **footprint input has no schema at all**. "Unknown custody" is not a recovery *action* — in 181 it is already a *stop* of the composition (`executor_phases_reference.historical`), exactly like the slot observation `('present', j) | ('absent', None) | ('unavailable', None)`.

**Choose the wrapper.** `storeFootprintObservation = ('available', footprint) | ('unavailable', None)`, consumed by `recover_installation_transition`/`historical`: `unavailable` → stop `unknown-custody` before the writer model is called (precedence step 5). Inside an *available* footprint add one closed member, `preparedFloorImage: 'absent' | 'matching' | 'mismatching'` (host-computed, §5), giving the table its image column. Consequences: no new action, no new refusal code, no successor to either closed output schema, the 43 journal vectors' `outputSchema` stays valid; "unreadable" and "absent" are distinguishable, which 180/182 already require elsewhere ("never infer a value after a failed read").
The successor-schema route (a new `REFUSE-CUSTODY` action or refusal code) would reopen two closed enums, the public-detail projection (S12.1) and every report golden, to express something that is not a decision of the writer model. Not recommended.
What I *would* add, additively: a closed **input** schema for the footprint (`StoreFootprintObservationV1`), since none exists and the table is only as good as the shape it is total over — `WEIRD` states are currently caught by an `else`, and a missing `new.state` key is a Python `None`.

## 5. Floor freshness — assessment of the owner's choice

Choice: image taken after the final first-pass floor write, immediately before `RESTORED`, under the fence; no intervening floor evaluation; resume retains the exact prepared/fenced floor evidence. **Sound, and better than my "max on resume" alternative, provided it is made checkable rather than procedural:**

1. **Make the invariant an equality the resumer verifies**: after fencing, the old store can no longer be written, so at resume `image.floors == fencedOldStore.floors` must hold exactly (for rollback: `image == max(fenced new, retained old)`, the existing `rollback_floors` law). That is what `preparedFloorImage: matching | mismatching` means. Equality is strictly stronger than max and turns "no intervening evaluation" from a promise into a detected contradiction (`mismatching` → QUARANTINE).
2. **Bind the image to the attempt**: include the journal's `intentDigest` (or journal ref) and `toStoreGeneration`. A crash inside abort can leave a stray image; without binding, a later attempt could adopt it. Unbound or foreign image ⇒ treat as `absent`.
3. **One existing sentence conflicts and must be reconciled (Q3):** S15, as amended by 181, says "the first-pass commit of a newly admitted Phase C transition rechecks generation and current target trust". A trust recheck is an S4 decision evaluation with a write-ahead floor. If "commit" means the `COMMITTED` marker (step 3), that evaluation happens **after** `RESTORED` — when the old store is fenced and the new one not yet selected — so there is no lawful place for its floor write, and it would violate "no intervening floor evaluation". Resolution consistent with the choice: for store operations the recheck is the *last act before the image is taken*; after the image, no S4 evaluation occurs until the new store is `final` (Phase C of a later entry / ordinary PRESENT). Say so in S15 and S9.
4. The image must carry only `FLOOR_KEYS`; anchor and pending challenge are excluded by the existing law and should be asserted absent, so the resting state of 181 is what resumption produces.
5. Poisoned floors: equality preserves them by construction; keep "only S4.5 lowers".

## 6. What must change (reference side) and what may not claim "unchanged" any more

| Artefact | Change |
|---|---|
| `security_lifecycle_model_v1.py` | `migration_recover` becomes journal-aware (or a new joined function; keep the footprint-only classifier for the journal-less S9 use); `RESTORED` tested before new-state; `COMMITTED`/`DONE`/`ABORTED` consult the footprint; image column. **The "writer predicates unchanged / AST-equivalent" claim ends here** — 186 should say so plainly |
| `migration-cases.v1.json` | successor file with `preparedFloorImage`; keep v1 as historical evidence of the v1 function |
| `transition-journal-cases.v1.json` | successor adding store `COMMITTED`/terminal/contradiction vectors (there is **no** store-operation `COMMITTED` vector today — the only `COMMITTED` vector is a core rollback); existing 11 recovery expectations are preserved by the table when `preparedFloorImage: matching` is supplied |
| `security-lifecycle.schemas.v1.json` | additive input schema only; output schemas untouched |
| `security-lifecycle-report.v1.json`, `check-security-lifecycle.v1.py` | regenerated / new case family + the totality sweep below |
| `integration-host-model.py` | `recover_installation_transition` takes the observation wrapper; `installation_recovery_attempt` history for the new abort-in-progress and journal-only resume cells |
| `executor_phases_reference.py`, `executor_phases_checks.v1.py`, `check-integration.py` (l.620 fixture) | wrapper + contradictory-footprint negatives |
| S9, S9.2, S9.2.1, S15; lineage A6 fact | write-order law W; the table; Q3 wording |
| product | none yet — no Rust consumer of the recovery table exists in my verified trees; host recovery remains owed |

## 7. Concrete counterexample tests (each fails on the current model)

1. `PREPARED`, old `RESTORED`, new `migrating/PREPARING` → must be QUARANTINE; today **ABORT**.
2. `PREPARED`, old `RESTORED`, new `migrating/None` → QUARANTINE; today **ABORT**.
3. `PREPARING`, old `RESTORED`, new `migrating/PREPARED` → QUARANTINE; today **ABORT** (footprint never read).
4. `LEASED`, old `RESTORED`, new `final` → QUARANTINE; today **ABORT**.
5. `COMMITTED`, old `RESTORED`, new `both` → QUARANTINE; today **RESUME-COMMIT**.
6. `COMMITTED`, old **unfenced**, new `migrating/COMMITTED` → QUARANTINE; today RESUME-COMMIT.
7. `COMMITTED`, old `RESTORED`, new `absent` → QUARANTINE; today RESUME-COMMIT.
8. `PREPARED`, old unfenced, new `absent` → **ABORT** (finish the abort); today QUARANTINE — the wedge.
9. `DONE`, old unfenced, new `absent` → QUARANTINE; today RELEASE-ONLY. `ABORTED`, old `RESTORED`, new `absent` → QUARANTINE; today RELEASE-ONLY.
10. `PREPARED`, `RESTORED`, `migrating/PREPARED`, image `absent` → stop unknown-custody; image `mismatching` → QUARANTINE; `matching` → RESUME-COMMIT step 3 (positive control — the existing owner vector).
11. Footprint observation `unavailable` → unknown-custody, and the writer model is **not called** (spy), vs today's QUARANTINE for a missing dict.
12. Through `sequence`: cases 1, 5 and 9 must not reach retirement or Phase C (today 1 and 5 return `journal-admitted-only`).
13. **Totality sweep** as a standing check: the 168-state product, asserting no `ABORT` with `old=RESTORED`, and that the set of non-QUARANTINE cells equals the reachable set generated from W — so the table and the write-order law cannot drift apart. This is the control that would have caught 181 F-1.
Mutants worth planting: old/new test order swapped back; `COMMITTED` short-circuit restored; terminal RELEASE-ONLY made unconditional; image column ignored; `unavailable` mapped to QUARANTINE; abort-in-progress cell reverted.

## 8. Limits

Derived under an explicit write-order assumption (W) that the owner must confirm or replace; Q1–Q3 are genuinely open. I modelled a single store transition with a binary old-store fence and did not model `old.present=false`, rollback's two-store max in the probe (argued in §5 only), partial renames, or lineage (PS-01) steps between terminal state and retirement. The probe's "proposed" function is a sketch to test totality and safety, not a proposed implementation. No approval of any kind is implied.
