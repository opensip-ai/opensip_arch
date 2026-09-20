# Independent review — native transition intent and continuity bindings 276

**Standing:** bounded native-Rust review of frozen `native-continuity-bindings-checkpoint-276`. Private `trust_input_bindings` extended with five-operation intent semantics, target-absence joins, and a structural descriptor/operation continuity helper on the **same** guarded operation Budget. **Not** native absence, selected lineage/store, complete-bucket census, durability, clock/deadline admission, transition effects, 273 prepared-outcome composition, 274 event replay, current trust authority, S4 execution, accepted role effects, restore/restriction authorization, historical/current population, non-key subjects, other-root contexts, private-policy merge, artifact/repair/S4/floors, command/role/batch/whole-image effects, native custody/fence/census/writers, source selection, or M3–M6. Archived 275 (`fb4595fa…bff9`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5389288 B, 682 members, SHA256 `3e4d5bf54ed28c2cdfebbff48362e973e5ba1ad147a2de5e7cf555e509a8ffa9`**. Pin, tar, member count, and every `subject.json` hash matched **before** extract; extract rehashed **682/682**. Product-inputs **409/409** live-equal.

Nested parent 275 pin `a56e8640…8804` (5270056 B / 569 / 407 files) equals the reviewed 275 freeze; live trial tar still matches; `trust-before.rs` equals that 275 `trust.rs`. Nested 265 `73c3b3f5…86df`. Nested 230 r3 helper `99288ae0…3c00` (66388 B / 38). Schema `1328ba16…4208`. `Cargo.lock` unchanged vs 275. Inherited 275/274 fixtures byte-identical (`inputs275.ndjson`, `events274.ndjson`). `lib.rs` unchanged.

Product vs 275: **409** files, **406** unchanged, **1** changed (`trust.rs` `25fa906a…4004` — private `trust_input_bindings` plus continuity tests), **2** added (`continuity276.ndjson`, `intent276.ndjson`). No public API. No full workspace rerun (272 506+2 predecessor only).

---

## What 276 adds

Still a private module: `trust_input_bindings` is not in `lib.rs`. The closed `Input` enum now also routes Absence, Intent, Operation, and Event. Full `EventRef`/`NodeRef` is admitted **before** `{sha256,bytes}` projection. Every `Budget.load` charges; owner errors latch `budget.scope`.

**Intent** (`intent(value)`): 270 `TransitionIntentInputV1` shape plus original 265 `admit_transition_intent` for five operations. `core-repair` keeps closure/schema/store; `core-update` changes closure and never lowers schema (`to>=from && schema==store`); `core-rollback` changes closure and never raises schema (`to<=from && schema==store`); `store-migrate` keeps closure and advances schema (`to>from && !store`); `store-rollback` keeps closure and retreats schema (`to<from && !store`). Rollback alone requires a non-null `rollbackDeadline`. **No** generation monotonicity, `+1`, or fresh-generation-zero rule. Deadline remains **lexical** (`TS_RE` / full-string profile), not calendar or current-time checking. Nested 265 kernel has the same five-op / no-`+1` / lexical-deadline contract.

**Absence** (`absence(budget, op, event, store)`): loads actual `TargetAbsenceInput`, original-semantic TransitionIntent, and source-before TrustCapsule on the **same** Budget. Forward/absent only. Sole cross-store shell derives target/source side store from this captured input. Source equals operation store; exact intent raw ref/digest/invocation/Exec; fresh target S; source/target G/K exactly from intent; source image/store/head. Core update or store migration must advance K. No boolean native-absence assertion. Action must be `"continuity"`.

**Descriptor helper** (`descriptor(budget, value, store)`): admits full `PublicationDescriptorV1` plus store/revision/previous projection; loads actual operation. Same-store returns structural operation binding only (empty events, no capsule). Cross-store requires action `"continuity"`, exactly one target-side continuity event with loaded locators checked, event target store/op. Forward: revision 1 / null `previousCapsule` / null `nativeBefore`, then the complete `absence` join, then a charged reload of the absence input to bind exact target store. Ancestor: both before images, source/head, distinct stores, actual target predecessor (`previousCapsule` SHA, `revision+1`, `nativeBefore`); original-semantic rollback intent, lower target K, exact digest/Exec and both image G/K. Returned `Bound` owns operation, matched target events, and all loaded inputs **in order**, including nested absence inputs. This helper does **not** call 273 `bind_descriptor_raw` or 274 event replay.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **216/216** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 31 compiled r2 controls + baseline | **32/32**; core fields/patches/source SHA-equal frozen `mutation-check-r2` |
| Exact live | Python source/fixture probes | **53/53** |
| Inspected | 180 continuity rows / 129 positive | `descriptor_operation` 151 / `join_absence` 29; 166 `original-N` (0–167 minus 161/162); 12 repeat/exact/one-short; 2 coherent guards |
| Inspected | 865 intent rows / 52 positive | five-op × closure × two schemas × three generations × optional lexical deadline, plus near-shape; 18 valid rows carry lexically legal year-99 deadlines; valid backward-generation rows exist |
| Inspected | original 230 helper 195 checks | r4 `originalChecks` length **195**; driver traces only `join_absence`/`descriptor_operation` (168 calls). Remaining owners are **reference coverage**, not native behavioral assertions. Not rerun here. |
| Inspected | 272 workspace 506+2 | predecessor only; not rerun |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): omit intent-semantics, absence-only-forward, operation-action, operation-ref, event-store, absence-intent, absence-invocation, absence-target-not-fresh, absence-target-binding, absence-source-image, absence-source-event-head, descriptor-projection-binding, continuity-event-locator, continuity-forward-initial, continuity-source-binding, continuity-ancestor-predecessor, continuity-intent-binding, continuity-intent-stores.

First fail **other** assertions (not exploit proofs):

- `omit-absence-source` / `omit-absence-source-binding`: later reason `absence-source-image`.
- `omit-continuity-intent-case`: later reason `absence-target-binding`.
- `omit-link-operation-store`: extra capture `original-114` **2 vs 1**.
- `omit-continuity-target-event`: panic missing target (`trust.rs:4303`).
- `omit-continuity-target-binding`: later reason `event-store`.
- `omit-continuity-target-before`: panic on null field (`trust.rs:4341`).
- `new-generation-must-increase` / `new-generation-must-plus-one` / `calendar-instead-of-lexical-deadline`: over-refusals of valid 865-matrix rows.
- `omit-nested-owned-inputs`: lost nested loaded-input facts (`original-20`).
- `reset-operation-budget`: `original-0` counters **(0,0,0) vs (3,3,2604)**.
- `omit-failure-latch`: follow-up call is not `BudgetError::Closed`.

Frozen `mutation-check-r1`/`r2` were not overwritten. r2 baseline `sourceSha256` is current `trust.rs` `25fa906a…4004`. Production functions (intent/absence/descriptor, excluding `#[cfg(test)]`) are byte-identical to `trust-before-operation-guard-cases.rs` (r1 baseline file SHA `32c2872e…2896`); only tests/fixtures in the same file changed for the r2 guard rows.

---

## Focused findings

### Prior budget / cache

130 of 180 continuity rows start with already captured objects **and** consumed edges (`prior.edges > 0` and nonempty `prior.objects`). Native tests prime the same Budget: `budget.retain(collection, rawHex)` for each prior object, then `budget.edge(prior.edges)`. The fixture preparer records that prelude with a `TrackingWork` wrapper over original `Work.load` (typed collection plus exact pre-call raw cache/edge count) without changing original load semantics. Every repeated reference still charges; direct errors latch; facts survive store/budget drop.

`original-144` is the documented r1 mismatch: nested helper on a **partially consumed** budget. Current row is `valid=False`, reason `operation-object-budget`, `prior.edges=21`, 16 prior objects, `captures=0`. The r1 fixture driver (`fixture-driver-before-shared-prelude.py`) had **no** `TrackingWork` and **no** prior retain/edge priming, so a fresh budget could admit after the original consumed budget refused. r2 records the exact prelude.

### Two explicitly symbolic excluded calls

Original tracing saw **168** helper calls; **2** are deliberate hash-UNVERIFIED symbolic-cycle resolver calls (`descriptor_operation` indexes **161** and **162**, `workType: "Unverified"`). Store values are **dicts**, not bytes, so they cannot be represented as native verified captures. They are excluded from the native corpus with complete separate evidence `reference-fixtures-r4/symbolic-excluded.json`. Native `original-*` labels skip 161/162 (`original-160` → `original-163`). All 195 original 230 checks still appear in the r4 report; no native content-hash cycle is claimed.

### Coherent operation guards

r1 `omit-operation-action` and `omit-operation-ref` **escaped** (`expectedOutcome` false): the original corpus lacked isolated absence action/ref cases for this helper. r2 added independently coherent `absence-coherent-wrong-action` (refuses `operation-action`) and `absence-wrong-operation-bytes` (refuses `operation-ref`). `continuity-before-operation-guards.ndjson` is 178 rows and lacks those two labels. Production functions unchanged. Live r2 replay catches both as wrong admissions.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | `trust_input_bindings` not exported from `lib.rs` |
| Five-op arms | exact match of 265 keep/change/advance/retreat rules |
| No generation `+1` in intent | production `intent` has neither `+1` nor monotonicity; 265 kernel neither |
| Deadline xor rollback | non-null deadline iff rollback op; no calendar check |
| Year-99 deadlines | 18 valid intent rows keep a lexically legal impossible calendar |
| EventRef/NodeRef before load | shared `load` helper; shape then `{sha256,bytes}` then `Budget.load` |
| Helper does not run 273/274 | `absence`/`descriptor` contain no `bind_descriptor_raw` / `publication_events` |
| Nested absence inputs | forward path `inputs.extend(joined.inputs)` |
| Same-store descriptor | empty events, no capsule |
| Forward initial | revision 1, null previous, null `nativeBefore` |
| Ancestor predecessor | `revision+1` and constructed `nativeBefore` |
| Corpus | 180/129/130 and 865/52 asserted in tests and counted in fixtures |
| Symbolic 161/162 | Unverified dict-store; absent from native labels |
| Guards | both isolated rows present; r1 escaped; r2 caught |

---

## Remaining (do not count closed)

Full restriction/history/root/list/quorum and restore proof composition; complete clock/publication/accepted role effects/base selection; current/historical populations/nonkeys/other roots/private policy merge/artifacts/repair/S4/floors/whole-state effects; native custody/fence/slots/census/durability/writers; runtime/source selection; M3–M6. Structural helper is not native absence, lineage, census, durability, or whole-proof authority. These are private review candidates, not shipped behavior.

---

## Verdict

- [x] Archive/pins/members verified. 409 product files: 406 unchanged vs 275. Nested 275/265/230 pins match live trial archives.
- [x] **216** security tests, Clippy, and fmt reproduced. Thirty-one compiled r2 controls behave as documented (eighteen wrong admissions; thirteen other-first).
- [x] Five-op intent with no generation `+1`/monotonic and lexical (not calendar) deadline; absence forward-only on the same Budget; descriptor does not run 273/274; prelude cache recorded; two Unverified symbolic calls excluded; r2 coherent action/ref guards caught.
- [ ] **Not** native absence, selected lineage, census, durability, clock/deadline admission, transition effects, current authority, or product installation.
