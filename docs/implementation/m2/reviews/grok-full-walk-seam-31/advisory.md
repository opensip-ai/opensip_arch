# Advisory: full structural Run traversal seam

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded seam/API/budget map for composing identity `Walker` with installed evaluator owners. **Not ACCEPT-DESIGN-UNIT. Not implementation. Not ReplayedRun. Not source29 acceptance.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-full-walk-seam-31/review`. No live/frozen/history edits.

Live identity `crates/identity/src/closure.rs` **51535** / `65e30f54…c75f` still has **six** `Unsupported` cuts. Selected identity overlay `identity_model.py` **158739** / `7b6750a9…0da2`. Import-totality helper `workflows_model.v1.py` **142991** / `60dc11e2…b180` is selected. Runtime-14 owners are installed (`import_joins.rs` live). Source29 `inspect_import_payload` is **frozen/not live**. Live lock **21/30**.

Ten selected-Python `open_run_closure` fixtures (exploration-28: 4 packets; exploration-30: 6 import packets) admit. Separate Rust component checks **47+76** pass; **not** a Rust full walk.

## Advisory-19, restated against **current** bytes

Advisory-19 cut 6 said payloadClass not `{parameter, coverage}` is “i.e. **relation**”. Current schema `import.payloadDigest` is `payloadClass: import`, `keyedBy: [kind, payload.payloadDomain]`. The allowlist cut is **relation and import** (any non-parameter/coverage class). Live `registered_payload` still requires `keys.len()==1` (1007–1009), so even adding `"import"` to the allowlist is the **wrong program**.

Stale vs now:

| Advisory-19 | Current |
| --- | --- |
| Coverage-17 / view-18 unselected | Installed (`inspect_coverage_producer`, `inspect_view_joins`) |
| No live stage-output fn | `inspect_stage_output_schema` / `inspect_stage_specs` exist |
| Imports “out of this seam” | `inspect_import_joins` + `inspect_parameter_selection` exist |
| Orchestrator ≈ walk then Plan-native then view-joins | Selected post-walk order is **longer** (below) |
| Owners share remaining Walker `steps` | `inspect_plan_native` / `inspect_view_joins` **copy** `TraversalBudget`; each nested retention uses **independent** local bounds |

Do not treat 19 as the current owner map.

## Six live cuts (current line numbers)

| # | Site | Trigger | Selected Python |
| ---: | --- | --- | --- |
| 1 | `inspect_relation_sources` **321** | `bodyIdentityJoin` present | `relation_payload_rules` during **walk** of fact payload |
| 2 | `digest_field` **791–792** | `retention` `fragment` / `owner-retained` | return without follow (**988–991**); later explicit joins recompute |
| 3 | `digest_field` **803–804** | `artifactClass==producer-interface-stage-output-schema` | walk **blobs only**; **1794** `admit_stage_output_schema` |
| 4 | `digest_field` **811** | `capability-manifest-id` | `capability_ids.add` (**1002**); **1662** admit + **1665** `FOREIGN_CAPABILITY_MANIFEST` |
| 5 | `digest_field` **847** | `h-identity` with `domainSet` (no `domain`) | `admit_frame` (**1021 / 1587**): nested records/identities, context **admission**, universes **stored** |
| 6 | `digest_field` **868–869** | `payloadClass` ∉ `{parameter, coverage}` | `registered_payload` → relation **or import** |

`inspect_local_structure` (**531–549**) / `inspect_identity_record` / `inspect_current_record` still construct `Walker` **without** an owner. Host tests stay fail-closed if that default is preserved.

Walker `visit` (**567–578**) does **not** implement `REFERENCE_SOURCE_JOIN` / `REFERENCE_PLAN_JOIN` (Python **1646–1647**). Default `inspect_local_structure` must **not** gain those joins (partial graphs have no Run). The full-run owner callback must.

## Installed post-walk owners (selected order)

Python after `walk(run)` (**1650**):

1. Root/grant/VCS joins **1654–1687** → live `inspect_run_links` (includes `admit_plan_capability`). Comment at run_links **175–176**: `FOREIGN_CAPABILITY_MANIFEST` is a **walk census**, not this owner.
2. Native contexts/universes **1689–1755** → `inspect_plan_native` (**requires caller-supplied** `observed_contexts` / `observed_universes`). `UNIVERSE_FRAME_UNRETAINED` (**1750–1755**) is **not** in evaluator today.
3. Policy/program **1757–1784** → `inspect_policy_program`.
4. Stages **1788–1794** → `inspect_stage_specs` (schema admit here, not at walk).
5. Proof/finding/predicate **1808–1852** → `inspect_evidence_roots` then `inspect_predicate_witnesses`.
6. Per-view **1853–1948** → `inspect_view_joins` (producer + 16-guards + totality).
7. Import correspondence + global parameters **1951–1986** → `inspect_import_joins` / `inspect_parameter_selection`.
8. Residual `get` of evidence coverage/import/finding (**1987–1988**) — walk should already have visited.

Walk-time (not those owners): H-frames, relation payload, import payload (source29), capability-id **collection**, fragment skip, stage-schema **blob**.

## Recommended seam (not accepted)

**Identity** owns the trait. **No** identity→evaluator edge. Default `inspect_*` unchanged.

```
pub enum OwnerObligation { /* six cuts; payload-class carries the class name */ }

pub trait StructuralOwner {
    fn object_context(&mut self, key: &str, domain: IdentityDomain, value: &JsonValue)
        -> Result<(), GraphError>;
    fn obligation(&mut self, o: OwnerObligation, budget: TraversalBudget)
        -> Result<(), GraphError>;
}

pub struct UnsupportedOwner; // object_context Ok(()); obligation => current Unsupported strings
```

`Walker::visit` calls `object_context` after `object()`, before `walk`. Six cuts call `obligation` — **never** `match Unsupported(_) => Ok(())`.

**Optional** public `inspect_local_structure_with` / walk-with-owner returns **only** `StructuralChecks` (object/blob/record/foreign sets). Not an authority token.

**Evaluator** private fixed owner (not caller-supplied):

| Obligation | Dispatch |
| --- | --- |
| `object_context` | `REFERENCE_SOURCE_JOIN` / `REFERENCE_PLAN_JOIN` using Run snapshot/plan ids captured at start |
| H-frame `native-context` | `frame_candidate` + `inspect_native_context`; record digest in **derived** context census |
| H-frame `native-semantic-universe` | `frame_candidate`; **store** row; bind is later `inspect_plan_native` |
| nested domainSet | same `admit_frame` recursion via obligation, charged as a **new** owner invocation |
| `payloadClass==relation` | `inspect_relation_snapshot` + `inspect_syntax_fact`; `bodyIdentityJoin` → `inspect_body_identity`. Rerun **per reference** even if payload blob already decoded (live comment **1054–1055**) |
| `payloadClass==import` | `inspect_import_payload(inputs, import_id, owner_budget)` once source29 is sourced. Recompute `import_id` as `import2:` + identity of **shaped siblings** (the import descriptor). Do **not** invent an id from `payloadDigest`. Until source29 is live, default remains `Unsupported("payload-class owner joins")` |
| body via 321 | same body owner as relation payload; one answer |
| `capability-manifest-id` | **record** id into census only (Python add). Admit stays `inspect_run_links` / `admit_plan_capability`. Default inspect stays Unsupported |
| stage-output schema | **blob** at walk (Python). Admit stays `inspect_stage_specs`. Walk callback `Ok` **only** inside the fixed composition that **mandatorily** runs that owner later |
| `fragment` / `owner-retained` | `Ok` **only** inside that same composition; else stay Unsupported |

**Evaluator complete structural function** (name is root’s):

```
inspect_structural_run(inputs, run_id, limits) -> Result<StructuralRunChecks, _>
```

Accepts **no** caller owner, **no** caller registry, **no** observed census. Derives frame/object/`capability_ids` during traversal, then remaining owners in the selected order above. `inspect_plan_native` receives **derived** digest lists. `UNIVERSE_FRAME_UNRETAINED`: every `fact`/`subject-scope` `sourceUniverse`/`targetUniverse` seen in `object_context` ⊆ derived universe census. `FOREIGN_CAPABILITY_MANIFEST`: walk `capability_ids − {plan.capabilityManifestId}`.

`StructuralRunChecks` = counts (objects, blobs, frames, imports, views, …). **Not** ADMIT, **not** `ReplayedRun`. Replay/custody remain later.

Import-totality **60dc11e2**: two-key import row selection requires **exact strings**. That lives inside `inspect_import_payload` (`select` compares JSON values to string registry fields; non-object payload → `PAYLOAD_IMPORT_UNREGISTERED`). Do not reimplement totality in the Walker.

## Budget (development resource refusals, not Plan work-units / M6)

Three **separate** limits:

1. **Identity walk** `TraversalBudget` — `Walker::spend` as today (`steps`/`depth`/`descriptor_work`).
2. **Max owner invocations** — decrement **once** per `obligation` / nested frame callback. This is the **recursive cap**. Copied owner budgets do **not** provide it.
3. **Per-owner `TraversalBudget`** — copy into each invocation. Nested `inspect_native_frame_inputs` / `inspect_plan_native` keep their documented **independent** per-retention bounds (`plan_native.rs` **67–69**; `view_joins.rs` **154** “copied budgets”).

Do **not** subtract owner `steps` from walk `steps` and call that one aggregate. `Limit` on any of the three is a resource refusal, not a Plan semantic budget (`PLAN_BUDGET_CONFIG_JOIN` / `estimate_evaluation_work` stay other owners).

Missing today: no invocation cap; `inspect_plan_native` copies the **same** `budget` into every retention (`125–126`). That is lawful **if** the complete function charges **one** invocation for `inspect_plan_native` itself and lets it copy internally. Charging one invocation **per nested frame** from the Walker plus letting plan-native copy again is double-walk, not double-count of one aggregate — document which layer owns nested-frame retention (prefer: Walker `admit_frame` records census; plan-native still re-walks with `inspect_native_frame_inputs` as selected, under **its** copied budget).

`NativeRetentionChecks` exposes only `frames`/`blobs`/`closures` **counts**. The walk already has `BTreeSet<(String,[u8;32])>` internally. Crate-private iterators of **actually traversed** `(NativeFrameSet, digest)` are required so nested `admit_frame` identities join Plan census / `UNIVERSE_FRAME_UNRETAINED` without a caller-built list.

## Remaining joins current owners do not cover

Must be **derived in this composition**, not assumed from component checks:

- `REFERENCE_SOURCE_JOIN` / `REFERENCE_PLAN_JOIN` on generic `visit`
- Walk census: `native_contexts`, `native_universes`, `capability_ids`
- `FOREIGN_CAPABILITY_MANIFEST` (explicitly excluded from `inspect_run_links`)
- `UNIVERSE_FRAME_UNRETAINED` (not in `inspect_plan_native`)
- Walk-time relation syntax/body **order** (schema then `inspect_syntax_fact` then body; per-reference, not decode-memo skip)
- Walk-time import two-key payload (`inspect_import_payload`); correspondence stays post-walk `inspect_import_joins`
- Stage-schema **blob at walk** vs **admit at 1794** — do not collapse
- Deferred fragment/owner-retained **only** if later owners in this composition actually run

Component 47+76 passing does **not** prove those joins: those tests call owners with **caller** censuses and never enter Walker cuts.

## Relation nonstring membership

`fact.relation` and `subject-scope.relation` are schema `type: string`. After exact fact/scope shape, `relations::row(..., name: &str)` is reached only with a string. Totality’s nonstring `registry_row` fix is the **import** two-key path. Do **not** broaden relation lookup to `JsonValue` “to be safe”. Regression: a fact that is schema-admitted cannot carry a nonstring relation; a nonstring never reaches `row()`.

## Tests (necessary)

- Default `UnsupportedOwner`: each of the six current strings still produced (existing host cases).
- **Forbidden:** `inspect_local_structure` succeeding by catching `Unsupported`.
- Full composition: `inspect_local_structure` on a Run **without** the complete function still Unsupported on first H-frame / relation / import payload.
- `object_context`: fact with foreign `snapshotId` → `REFERENCE_SOURCE_JOIN`; view with foreign `planId` → `REFERENCE_PLAN_JOIN`; default inspect of a lone fact does **not** emit those.
- Clones fact: syntax then body actually run; second fact sharing payload digest still runs both owners.
- Import: `inspect_import_payload` receives `import2:{identity(siblings)}`, not payload digest; two-key; totality nonstring domain → `PAYLOAD_IMPORT_UNREGISTERED` (when source29 is wired).
- H-frame context missing grammar closure still refuses **during walk**.
- `capability_ids` extra id → `FOREIGN_CAPABILITY_MANIFEST` after `inspect_run_links`.
- Fact `sourceUniverse` not in derived census → `UNIVERSE_FRAME_UNRETAINED`.
- `inspect_plan_native` in the complete function is **not** passed a caller-built census.
- Stage-output walk callback without later `inspect_stage_specs` in the same composition → still Unsupported.
- Invocation budget 0 → `Limit` **before** first obligation; walk budget 0 → `Limit` on first `spend`; per-owner budget 0 → that owner’s `Limit`. A copied per-owner budget of N does **not** claim total owner-work ≤ N.
- `StructuralRunChecks` / `StructuralChecks` cannot construct a Run id.

## Verdict

**NOT ACCEPTANCE.** Recommended seam: identity `StructuralOwner` defaulting to today’s six Unsupported cuts + no-op `object_context`; evaluator private owner + `inspect_structural_run` deriving census then selected remaining owners. Three separate development limits; invocation count is the recursive cap. Source29 import API takes `import_id` recomputed from siblings. Relation nonstring is unreachable after fact shape. Advisory-19’s “relation only” and shared-steps budget story are withdrawn for current bytes. No draft implementation reviewed. `ReplayedRun` remains later replay/custody.
