# Advisory: next bounded owner after Plan-native 14 — relation body identity

**Reviewer:** Grok. Root remains lead. **Not** ACCEPT-DESIGN-UNIT. **Not** frozen-14 review. Did not edit private-14, live, frozen, or history.

Work tree: `/tmp/opensip-implementation/m2-grok-body-join-boundary-15`.

## Sources

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| selected `identity_model.py` | 158555 | `619d6e3c…41e6` |
| selected `native_evidence_model.py` | 319944 | `e6784aa1…e2b9` |
| live `identity-v3.schema.json` | 197480 | `311c1feb…b68f` |
| live `native-v2.schema.json` | 280357 | `e5834d37…7773` |
| live `relation-payload-v2.schema.json` | 57623 | `53380a24…be9a` |
| inventory v14 | 136672 | `20bd2bd4…814d` |
| identity `closure.rs` (13/v4 same cut) | 47631 | `a6dc8b89…319e` |

Cut: `inspect_relation_sources` completes payload + `snapshotJoins`, then `Unsupported("relation body identity owner")` if the relation row has `bodyIdentityJoin` (`closure.rs` 380–382). Walker `payload-class owner joins` remains a **later** import/coverage cut. Identity must not depend on evaluator.

## What the reference join actually is

`relation_source_joins` (~1452) then optional `body_identity_join` (~1481). Today only **`clones`** carries `bodyIdentityJoin` (`relation-payload-v2` 152–168). That row’s `snapshotJoins` is **[]** — the source join **is** the body join (one anchor, `anchorCardinality` 1, must **agree** with `anchorLaw` or `RELATION_ANCHOR_LAW_DRIFT`).

`body_identity_join` (reference functions to implement, not a full Run):

1. `parse_body_frame` (270) on `blob(bodyIdentity without sha256:)` — `BODY_IDENTITY_FORM` / `BODY_FRAME_*`
2. `blob(normalisationVersion)`; domain tag, level, **raw 32-byte** levelVersion (`BODY_IDENTITY_DOMAIN` / `_LEVEL_JOIN` / `_LEVEL_VERSION_JOIN`)
3. Use `fact.sourceUniverse` + registry `languageVersionBinding` — **not** the universe `language` field (engine vs body; `.js` under TS universe is `javascript`; syntax must not mint `syntax` as `languageId`)
4. Follow `contextField` (`sha256-text`) to the **already Plan-selected** context; interpreting closure = `normalizationClosure.path` (`toolchain` vs `grammar`)
5. `admit_normalization_specification` (764) — map at the **interpreting** closure tree, this level’s digest, member of same tree
6. `body_language_version` (310) — derived record; dialect `closed-suffix-table` (TS/syntax, longest suffix) or `selected-compilation-target-edition` (Rust, needs retained `sourceUnitOwnership`, complete enumeration, selected units, unique effective edition)
7. Compare frame `languageId` / `languageVersion` to that projection (`BODY_IDENTITY_LANGUAGE_JOIN` / `_LANGUAGE_VERSION_JOIN`)
8. If level in `recomputableAt` (`L0-verbatim` only): payload = `u32be len || anchor span`; else `parse_token_stream` (292) custody only — **no** tokenizer quality

Coverage `coverage_source_variant_prerequisite` (~1427) is a **different** owner (scope completeness). Do not fold it into this API.

## Ownership: evaluator orchestrates; do not put native in identity

Identity stays: `inspect_relation_payload`, snapshot joins, **pure** `parse_body_frame` / `parse_token_stream` (no native, safe to add on identity). Keep `inspect_relation_sources` **Unsupported** for `bodyIdentityJoin` as the explicit cut — do not have identity `admit_frame` a universe (that follows context and repeats the Plan-14 trap).

**Next bounded evaluator API** (host `dev-dep` only, DAG unchanged):

`inspect_body_identity(inputs, payload_digest, payload_schema_digest, fact, plan_native, budget)`

- `plan_native` = output of Plan-native 14 for this fact’s `sourceUniverse`: selected context digest, context **owner already run**, universe `admit_frame` **without** context follow, merged `retained` (config graph / layout / rust ownership).
- Call identity payload inspect first.
- If relation has no `bodyIdentityJoin`, this API is `Law` / not-applicable (other relations stay on `inspect_relation_sources` Ok).
- **Do not** call `inspect_native_retention` on the universe. **Do not** accept caller ADMIT. **Do not** walk grants, pruned-tree, or facts→`UNIVERSE_FRAME_UNRETAINED`.
- Check `fact.sourceUniverse` equals the 14-admitted universe digest and `universe.nativeContextId` equals the 14-selected context (`sha256:` vs bare hex as in 14). If the named context is **unselected**, that is 14’s `UNIVERSE_CONTEXT_NOT_SELECTED`, not a body-identity fetch.
- Then steps 1–8 above using **supplied** universe/context/retained + identity blob accessors.
- Rust dialect uses `retained.sourceUnitOwnership` from 14 universe nested identity, not a new walk.

Import `payloadClass` / walker `payload-class owner joins` is **not** this slice.

## Inventory 14 vs a new file

Inventory 14 (`20bd2bd4…`) adds only `native_retention.rs`, `plan_native.rs`, `native-plan-registry.json`. **Do not** stuff body identity into `plan_native.rs` (Plan census/grant) or `native_universe.rs` (binders).

**Need inventory 15** (additive, same 20-package DAG):

- `crates/evaluator/src/body_identity.rs` (new)
- optional `lib.rs` export only
- **no** new JSON registry if the join is read from existing `opensip.product.relation-payload.2` / identity-v3 `languageVersionBinding` / `normalizationSpecificationLaw`
- identity may add `parse_body_frame` / `parse_token_stream` in `crates/identity/src/` (also inventory 15 if those paths are new)

## Does body identity require full Plan-selected universe checks first?

**Selected universe + context pair: yes. Full Plan native block: no.**

Required predecessor: Plan-native 14 census — `NATIVE_CONTEXT_SET_JOIN`, context **owner**, universe retain **without** early context bind, `UNIVERSE_CONTEXT_NOT_SELECTED` before missing-blob, then bind. Body identity consumes that pair (comment 1518–1520: context is the one close_run already required to be Plan-selected).

Not required first: grant operations, `snapshot_pruned_tree_faults`, capability vocabulary (except the universe must already be a selected language), fact/scope universe subset.

If 15 internally `admit_frame(universe)` then `admit_frame(context)`, an unselected missing context becomes unavailable **before** 14’s selected-set fault — same trap as retention-13 universe roots.

## Tests (bounded, no full Run)

1. `clones` + `inspect_relation_sources` still `Unsupported("relation body identity owner")`; payload inspect Ok.
2. L0 TS `.ts` / `.js` / `.d.ts` (longest suffix); `.js` under TS universe → `languageId=javascript`.
3. L0 syntax universe: `languageId` from dialect table, never `syntax`.
4. L0 span mismatch / wrong anchor path / extra anchors → `BODY_IDENTITY_BODY_SPAN` / `RELATION_ANCHOR_LAW_DRIFT`.
5. L1–L3 well-formed token stream vs trailing bytes; do not execute a normalizer.
6. `normalisationVersion` blob missing vs map missing vs wrong level vs digest not in interpreting closure tree.
7. Universe names unselected context: **14** refuses `UNIVERSE_CONTEXT_NOT_SELECTED`; 15 is not invoked / must not fetch.
8. 15 called with mismatched supplied context vs `nativeContextId` → typed identity mismatch, not bind.
9. Rust: missing ownership retained, `partial` enumeration, path not compiled, not selected, disagreeing editions.
10. Unlisted suffix → dialect `onUnknown` (eligibility is coverage’s job if no body is derived).
11. Frame `languageVersion` hex-as-bytes vs raw 32.
12. Extra unrelated blob does not change the join.
13. Identity still has no evaluator dependency; host tests remain `dev-dep`.

## Limits

Not full `open_run_closure`. Not import payload owner. Not coverage dialect completeness. Not 14 acceptance. Not caller ADMIT or replay.

**Verdict: NOT ACCEPTANCE.**
