# Advisory: full-retained-walk composition seam

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Bounded architecture/source map for composing identity `Walker` with evaluator owners. **Not ACCEPT-DESIGN-UNIT. Not implementation. Not ReplayedRun. Not Coverage-17 or view-18 source acceptance.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-walk-composition-boundary-19/review`. No live/frozen/history edits.

Live identity `crates/identity/src/closure.rs` 50730 / `72a73d74…7360`. Selected identity `open_run_closure` `619d6e3c…41e6`; selected native `e6784aa1…e2b9`. Live evaluator exports context/universe/retention/plan-native/body/capability-support; Coverage producer 17 is frozen-unselected; view-joins 18 is editable layout.

## Actual caller paths (not helper conflation)

**Identity `Walker` is entered only from:**

- `inspect_local_structure` (512–530) → `visit` (547–558) → `walk` → `digest_field` (754–861)
- `inspect_identity_record` (469–487) → `local_record`
- `inspect_current_record` (491–510) → `foreign_record`

Host `schema_sources.rs` calls those. It does **not** call evaluator `inspect_*` from the Walker.

**`inspect_relation_sources` (302–323) is a separate public API**, not invoked from `Walker::digest_field`. After `inspect_relation_snapshot` it refuses `GraphError::Unsupported("relation body identity owner")` if the relation row has `bodyIdentityJoin` (320–321). Host `native_owner_tests.rs` / `schema_sources.rs` call it. Evaluator `inspect_body_identity` (394) calls **`inspect_relation_snapshot` only** (412), then does the body owner itself.

**Selected Python `open_run_closure` walk (950–1031) then `admit_frame` (1587–1642) actually dispatches** native context/universe, relation payload rules (syntax fact + body join), and later capability/stage/plan/view. Rust Walker **stops** at six `Unsupported` cuts instead.

## Six live `Unsupported` cuts

| # | Site | Trigger (actual match) | Selected Python instead |
| --- | ---: | --- | --- |
| 1 | `inspect_relation_sources` **321** | relation row has `bodyIdentityJoin` | `body_identity_join` in `relation_payload_rules` (1480), during **walk** of fact payload |
| 2 | `digest_field` **772–773** | `retention` is `fragment` or `owner-retained` | **returns without follow** (988–991); later explicit joins (`snapshot_joins`, body, stage) recompute |
| 3 | `digest_field` **784–785** | `artifactClass == producer-interface-stage-output-schema` | walk only `blob()` (992–1001 special-cases `registered-schema-document`); **1794** `admit_stage_output_schema` |
| 4 | `digest_field` **792** | `representation == capability-manifest-id` | `capability_ids.add` then **1662** `admit_capability_manifest` |
| 5 | `digest_field` **827–828** | `h-identity` **without** `domain` (uses `domainSet`) | `admit_frame` (1021 / 1587): parse H-frame, nested records/identities, closure-kind, **actual** `admit_native_context`; universes stored, bound later 1727–1736 |
| 6 | `digest_field` **848–850** | `payloadClass` not `parameter`/`coverage` (i.e. **relation**) | `registered_payload` → `relation_payload_rules` (1127): syntax capability + optional body |

Walker `registered_payload` (959–1046) **shape-admits** parameter/coverage only; it never calls `admit_coverage_result_v3`. Coverage producer remains a **post-walk** owner (selected 1934; layout v17 unselected).

`frame_candidate` (1258+) is the live H-frame primitive evaluator universe/context already use. Walker cut 5 does **not** call it.

## Remaining unsupported operations (for a later full walk)

Must be **dispatched**, not skipped:

1. Native H-frames (`domainSet` native-context / native-semantic-universe / nested) → `frame_candidate` + `inspect_native_context` / retain universe row (bind is **Plan-native**, not walk).
2. Relation payload class → `inspect_relation_snapshot` + `inspect_syntax_fact` + `inspect_body_identity` when `bodyIdentityJoin`.
3. Capability-manifest-id → collect + `admit_capability_manifest` / `admit_plan_capability` (Plan bytes join is post-walk 1657–1664).
4. Stage-output schema artifact → `admit_stage_output_schema` equivalent (producer-closure tree membership). **No live evaluator fn**; identity 735–761 is the selected owner. Seam must not invent a silent blob-only success.
5. `fragment` / `owner-retained` → **not** ADMIT; either leave Unsupported until the explicit join runs in the **same** composition, or dispatch that join. Python skip is safe only because `admit_frame`/`snapshot_joins` follow in the same `open_run_closure`. Catching 773 as `Ok(())` without those joins is a bypass.
6. Body via `inspect_relation_sources` 321 — same owner as (2); do not implement two answers.

**Still out of this seam (full graph):** Plan-native 1689; `UNIVERSE_FRAME_UNRETAINED` 1750; policy/program 1757; stages 1788; findings/predicates 1822; **view-joins 1853** (editable 18); Coverage producer 1934 (frozen 17); imports; `close_run` replay.

## Smallest concrete Rust seam

**Identity-owned trait + evaluator impl. Not reverse identity→evaluator. Not catch-`Unsupported`-as-ADMIT.**

Put in **identity** (no evaluator types):

```
pub enum OwnerObligation { /* the six cuts, with digest/annotation/siblings */ }

pub trait OwnerJoin {
    fn join(&mut self, o: OwnerObligation, budget: TraversalBudget) -> Result<(), GraphError>;
}

pub struct UnsupportedJoin; // current behavior: Err(Unsupported(...)) for all six
```

`Walker` / `inspect_local_structure` / `inspect_relation_sources` take `J: OwnerJoin` (default `UnsupportedJoin` so existing host tests stay fail-closed). At the six sites: `self.owners.join(obligation, budget)?` — **never** `match Unsupported(_) => Ok(())`.

**Evaluator** crate implements `EvaluatorJoin` that, on rehashed supplied bytes:

| Obligation | Dispatch (live unless noted) |
| --- | --- |
| H-frame `native-context` | `frame_candidate(..., Context)` + `inspect_native_context`; closure-kind already in that owner |
| H-frame `native-semantic-universe` | `frame_candidate(..., SemanticUniverse)` only (store row); **bind** is `inspect_plan_native` later |
| H-frame nested | `frame_candidate(..., Nested)` as today in universe bind |
| Relation payload | `inspect_relation_snapshot` + `inspect_syntax_fact`; if `bodyIdentityJoin` → `inspect_body_identity` |
| Body via 321 | same `inspect_body_identity` |
| Capability-manifest-id | record id; post-walk `admit_capability_manifest` / `admit_plan_capability` |
| Stage-output schema | new thin evaluator fn matching identity 735–761, or keep Unsupported until that fn exists — **not** blob-only Ok |
| fragment/owner-retained | Ok **only** if this composition will run the named later join; else stay Unsupported |

**Evaluator orchestrator** (not identity, not a Run token):

```
inspect_retained_walk(inputs, run_id, budget) -> Result<WalkChecks, WalkError>
```

Order matching selected `open_run_closure`: schema walk with `EvaluatorJoin` → capability manifest (1662) → **`inspect_plan_native`** (live) → later **`inspect_view_joins`** when 18 is sourced (calls producer 17 + 16-guards + totality). `WalkChecks` = object/blob/record counts **plus** owner diagnostic counts. **Not** ADMIT, PlanNativeChecks, CoverageAdmission, or `ReplayedRun`.

Identity still `inspect_*` without the trait ⇒ six Unsupported (current product).

## Memo, budget, faults, roles

- `visit` memos `checked.objects` (549–557) **before** walk. Owner H-frame must memo `(digest, domainSet)` like Python `parsed[('frame',digest,domain_set)]` (1588), **after** rehash, **without** skipping owner on a prior structural-only visit.
- `local_record` memos `(sha, kind)` (865–868). Payload-class relation must **not** use that memo to skip `inspect_syntax_fact` / body.
- `spend` (534–538): each owner uses remaining `descriptor_work` / `steps`; `Limit` stays `Limit`.
- Owner `Refused` / native refusals propagate; empty owner refusals are **not** graph ADMIT.
- Closure **kind** stays in `inspect_native_context` / Python 1629–1631; dispatch must not drop it.
- Plan/view **selection** is not proven by walk memo or `StructuralChecks`.

## Tests (necessary)

- Default `UnsupportedJoin`: each of the six sites still `Unsupported(...)` (existing host cases).
- **Forbidden:** `inspect_local_structure` on a clones fact or native-context digest succeeding by matching `Unsupported` → `Ok`.
- Clones fact + `EvaluatorJoin` → `inspect_body_identity` actually run (universe/context rehashed).
- `h-identity` `domainSet=native-context` → `inspect_native_context`; missing grammar closure still refuses.
- `capability-manifest-id` → `admit_capability_manifest`, not collect-and-ignore.
- Stage-output digest → UNREGISTERED / mismatch names, not blob-only Ok.
- `fragment` without later snapshot join → still Unsupported.
- Budget 0 on owner dispatch → `Limit`.
- `WalkChecks` / `StructuralChecks` cannot construct a Run id.

## Internal vs public

`GraphError::Unsupported` and identity `AdmissionError` wraps (`NATIVE_CONTEXT_ADMISSION`, `COVERAGE_PRODUCER_ADMISSION`) are **internal**. Host DomainDetail / D9 (`PROVIDER.PROTOCOL_VIOLATION`, `native.coverage-bijection-mismatch`) remain presentation of **producer REFUSE**, not a mapping of walk `Unsupported` to ADMIT.

## Verdict

**NOT ACCEPTANCE.** Smallest seam: identity `OwnerJoin` defaulting to today’s six Unsupported cuts; evaluator impl dispatches **actual** live owners on rehashed bytes; evaluator `inspect_retained_walk` orchestrates walk then Plan-native (then view-joins when sourced). No reverse DAG edge. No catch-Unsupported-as-ADMIT. Diagnostic counts ≠ Run/replay. Coverage-17 and view-18 stay unselected/editable until their own source units.
