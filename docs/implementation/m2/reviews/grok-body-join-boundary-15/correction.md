# Correction: body-join advisory claimed the wrong reference order

**Not fresh-blind.** Original `report.md` / `report.json` preserved (`d72507c9…ee43` / `a5805fe1…014d`) as `initial-report.md` / `initial-report.json`. No source edits. Root remains lead.

Root is right about current selected `open_run_closure` (`619d6e3c…`). The initial advisory mixed **later FullRun composition** into **current walk-time body joins**.

## Exact callers (current reference)

Definitions are nested inside `open_run_closure` (909). **Execution of the walk is 1650**, before the native Plan block at 1689:

```
1650  walk(SCHEMA['$defs']['run'], run)
1688  # native contexts and semantic universes
1690  NATIVE_CONTEXT_SET_JOIN
1715–1743  per-universe language / prepared / UNIVERSE_CONTEXT_NOT_SELECTED / bind / grant
```

`walk` follows digest annotations. A fact payload (`payloadClass: relation`) reaches `registered_payload` → `relation_payload_rules` (1297):

| Line | Call | Fault if it fails |
| --- | ---: | --- |
| 1313 | `anchor_law(row, fact)` | `FACT_ANCHOR_CARDINALITY:…` (clones: **exactly 1**; extra or zero) or `RELATION_ANCHOR_LAW_MISSING` |
| 1314 | `syntax_capability_supported(fact)` | syntax capability scope faults |
| 1331 | `relation_source_joins(value, row, fact)` | snapshot path/content/length; then body join |

`relation_source_joins` 1480: `if 'bodyIdentityJoin' in row: body_identity_join(...)`.

`body_identity_join` **does** follow the universe’s own `contextField` **during this walk**, not after Plan selection:

```
1510  admit_frame(fact['sourceUniverse'], 'native-semantic-universe')
1522–1525  contextField sha256-text → admit_frame(context_digest, 'native-context')
```

`admit_frame` on universe (1640–1641) stores nested retained and **does not** bind. `admit_frame` on context (1624–1639) **does** run closure kind + `admit_native_context`. That is local frame/context retention, not `UNIVERSE_CONTEXT_NOT_SELECTED`.

Comment 1518–1520 says the named context is *the same id close_run later requires to be Plan-selected*. That is a **later FullRun obligation**, not a gate already applied at 1510–1525.

`RELATION_ANCHOR_LAW_DRIFT` (1540–1542) is **only** `anchorLaw.cardinality != bodyIdentityJoin.anchorCardinality` (registry disagreement). Extra anchors never reach it: `anchor_law` already refused `FACT_ANCHOR_CARDINALITY` at 1249–1251. Initial test 4 was wrong.

## What the initial advisory got wrong

| Initial claim | Current reference |
| --- | --- |
| Body diagnostic **requires** Plan-native 14 selected universe+context pair first | Walk-time body join **precedes** Plan native block; `admit_frame(universe)` then `admit_frame(context)` locally |
| Plan14 output is a selected-pair token for 15 | `PlanNativeChecks` is private **counts** only; it is not pair authority |
| Making Plan set-join a prerequisite of body 15 | Would **change** reference fault order (selected-set / SET_JOIN after walk, not before body join) |
| Extra anchors → `RELATION_ANCHOR_LAW_DRIFT` | Extra anchors → `FACT_ANCHOR_CARDINALITY` via `anchor_law` **before** `relation_source_joins` |

## Separate: recommended future vs current behavior

**Current (implement body15 this way):** local rehashed fact/payload/snapshot + `parse_body_frame` / projection / interpreting-closure normalization / L0 span or L1–L3 token custody. May `admit_frame` (or retention **context/nested/universe-without-Plan-bind**) as `body_identity_join` does. **No** Plan/capability/coverage/globalRun claim. Identity `inspect_relation_sources` stays `Unsupported("relation body identity owner")`. Draft body-registry remains private unaccepted.

**Later FullRun composition (do not bake into body15):** after walk, native block 1689+ still does SET_JOIN, vocabulary, `UNIVERSE_CONTEXT_NOT_SELECTED` **before** missing selected context, bind, grant, pruned-tree. That is close_run / Plan-native 14 territory, not a predecessor token for the body diagnostic.

Evaluator orchestration and a possible inventory-15 `body_identity.rs` remain **layout advice**, not a claim that reference currently waits on Plan14.

**Verdict: NOT ACCEPTANCE.** This file only corrects the order/fault facts.
