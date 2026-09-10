I’ll fix the ordinary-path bugs in the five owned files, add a real incoming-search schema, and put regression checks in v5. First I’ll locate the existing glob helper, policy filter bounds, and the completeness/import paths that the 16 fixtures missed.I’ll add a real incoming-search schema, then rewrite completeness, glob, import occupancy, and kind admission so ordinary cases stop failing.Rewriting the atom model next so completeness, glob, import occupancy, and kind admission follow the owner helpers instead of the broken ordinary-path shortcuts.Fixed the ordinary-path bugs in the owned isolated files and added a typed incoming-search input. Frozen/live sources were not edited. **Not full-graph replay.**

## Owned files

| File | SHA-256 |
|---|---|
| `evaluator-projection-registry.v1.json` | `e000a81382cc62cc13059357cd34a3129a91b02a8faa501a1a0652b4c9b1e401` |
| `target-attribution.schema.v1.json` | `545dc06b46bd4c3bd0ae8f0500a4fcc4f80685ed836173051286a171abb7538b` |
| `atom-evaluation-contract.v1.md` | `f2435af10feb9037e1ab93e34b11999a16a0cb23421dfa44bfdd3920cf1ede94` |
| `atom_model.v1.py` | `577a0e947f0d19158b9bb7d1baba42bcd9b6acbc0c3df37153ab72a704d99bb9` |
| `check-atoms.v1.py` | `48ec7375455c598dca9592329c251c4b34af6c9cd30cd1bbfc6f4995d4000a98` |
| `incoming-search.schema.v1.json` **new** | `8d8fdc63d041ac3e6dc26a8c06086b76bb3d0c7bbeee4307b23251d10dd6f638` |

Helpers: `grok-atom-contract.v5/check-atoms.report.json`, `hashes.json`.

## Checks

`/tmp/opensip-architecture-review-env/bin/python -I -B …/check-atoms.v1.py` → **30/30**. Draft 2020-12 metaschema on all three JSON schemas. Unit scans of admitted maps, **not** Run admission/replay.

## Bug fixes (1–10)

1. Symbol/package expected IDs from inventory rows only; extent paths are file IDs only; partial/unavailable ⇒ `population-unknown`. Bindings deduped by universe.
2. Outgoing completeness uses **exact requested rung** and only scopes/coverages that **contain the current source**. Independent other-subject partitions do not block. Scope without Coverage ⇒ `scope-without-coverage`. Incoming accounts **every** represented *S→V* plus *S→U* search (Coverage first).
3. Sufficiency view includes actual `DEPENDS_ON` Coverage; no fictional completes; all `su.causes` retained. Unknown export treated as exported (owes closed-world) + `target-export-unknown`. Unresolved-edge `targetModule` is not compared to opaque native IDs.
4. Wrong subject kind ⇒ `ATOM_KIND_INCOMPATIBLE` (not vacuous `none`). Completeness always run; causes kept when known values dominate.
5. Glob is `workflows_model.v1.glob_match` (`**/*.ts` matches root `a.ts`). Filters admit via `FieldFilterSuccessorV1` (max 16) plus this relation’s ladder for `resolution`.
6. Runtime covering polarity rows vs filter matches are separate; complete unhit + filter `observed-hit` ⇒ `none` true / `exists` false. Partial wrappers always record incompleteness (count≤N unknown; exists still true).
7. History applies subject/resolution/subjectKind filters. Partial+match ⇒ `none` false. No fabricated ordinal-0 address. Overload path+QN ⇒ `overload-ambiguous`, not a positive. `test-result` `subjectKind` implemented.
8. Closed input keys; missing Plan-selected wrapper refuses `ATOM_IMPORT_WRAPPER_MISSING`. Scope is `ImportScopeDescriptor` via `scopeDigest` or explicit `normalized-import-scope-descriptor` adapter. No default consumable/staleness=current.
9. `IncomingSearchV1` is a real canonical-record input: Plan2 + provider + *S*/*U* + relation@rung + scope/inventory refs + search/closed-world claims. Schema, uniqueness, joins. Coverage *S→U* wins; partial cannot be overridden; no Cartesian keys.
10. Non-resolved all-covered: `existential`+`complete`. Resolved: `universal-negative`+`complete`. DSL has no extra minConfidence/derivationPolicy (defaults 0/`any`). Result arrays sorted unique.

## Limits

Does not compose boolean nodes, findings, waivers, or proof3. Does not admit native/import/Coverage graphs. Enumeration files and identity-schemas.v3 untouched. Root registers `incoming-search` if it keeps this input.
