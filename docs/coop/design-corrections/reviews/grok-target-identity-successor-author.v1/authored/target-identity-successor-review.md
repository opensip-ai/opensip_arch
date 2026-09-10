# Target-identity successor — coauthor authoring review

Standing: actual Grok DESIGN COAUTHOR continuation of
`grok-target-identity-design-options.v1` COMPLETE22. Codex agreed Option B.
This is isolated architecture/design/reference authoring in
`/tmp/opensip-design-corrections/target-identity-successor.v1`.
Not product implementation. Not commit/push. Not live normative application.
Not readiness or acceptance. Not blind standing. P7 Rust/syntax-data full
grades are unaccepted. P7 `import.producerClosure=provider` is independently
correct and is **not** repaired here; root merges a separate closure-kind
patch.

Frozen24 (`candidate-subject.v24`, manifest
`a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb`,
12797 files) was not edited. Isolated copy verification: 12797 files,
mismatches none.

## Final field / profile / channel decisions

1. **Missing mapping vs malformed.** Occupancy=unknown or absent sidecar
   yields unknown/uncertain where the fact *could* occupy `E`. It is never
   payload-inequality known nomatch for file/package. Malformed first-party
   sidecars (null `evaluationNativeId`, missing package path, nonunique
   inventory join, schemaVersion≠2) are **admission refusals**. Known
   incompatible kind or universe remains nomatch. Same-grammar symbol
   payload≠N remains nomatch so unrelated symbol facts are not poisoned.

2. **Ephemeral exact-id still exists.** Host MAY derive first-party occupancy
   when `targetNativeId` uniquely equals an inventory native id (symbols;
   accidental C15 colon-path files). Precedence: admit sidecar if present;
   prefer independently known ephemeral fields; sidecar `external` while
   ephemeral is first-party refuses. Host MUST NOT parse namespaces.
   Package-path cases are closed: first-party required inventory join;
   external required query coordinate; unknown all package/logical/eval
   fields null.

3. **Uniqueness.** Per-fact `(planId, sourceFactId)` remains the sidecar
   uniqueness. Added conflict only:
   `(producerClosure, targetUniverse, targetNativeId)` among first-party V2
   records that **disagree** on occupancy identity
   (`TARGET_ATTRIBUTION_PROVIDER_OCCUPANCY_CONFLICT`). Different providers’
   equal opaque strings are **not** one identity. Discriminating controls
   exist for both.

4. **External package graph identity.** `kind=package` GraphEndpoint still
   requires `packageManifestPath`. External package sidecars therefore
   **require** `packageManifestPath` as the endpoint coordinate, not as a
   first-party inventory join. Query `nativeSubjectId` stays the opaque
   payload id. Unknown package is unprojectable.

5. **Profile.** This successor **selects TargetAttributionV2**. V1 sidecars
   refuse. Missing sidecar does **not** restore historical payload-vs-N
   nomatch. Evaluator output profile remains **3** (subject3/finding3/proof3/run3
   recipes unchanged). Frozen24 remains replayable only under frozen24’s own
   selected V1 schema/profile. No dual-runtime product. graph-query
   schemaMajor remains 3.

6. **Provider return/capture.** TargetAttributionV2 is the typed companion
   return of the fact-producing Plan-selected provider. Host captures
   admitted bytes into `hostCapture.hostDerivedRefs`
   (`domain=target-attribution`). `producerClosure` must equal the source
   fact’s producer and the fact must appear in a selected view.
   Protocol3 phases/frames and native payload grammar are unchanged.
   Shared platform law; no new language modes.

No remaining normative contradiction that blocks this isolated successor.
Public-detail/D9 registration of new TARGET_ATTRIBUTION_* keys remains
NEW/internal, same standing as the V1 keys.

## What was implemented

- New `foundation/target-attribution.schema.v2.json` (selected).
- Atom occupancy-identity compare; V1 sidecar refusal; provider capture join
  in execution-inputs.
- Query first-party imports targets project onto inventory vertices.
- Schema-admitted FILE/PACKAGE positives; symbol/external/unknown/malformed
  controls; illegal `resolvedTarget='src/a.ts'` bypass removed.
- Strong owner `close_run` + `execute_graph_query` for the FILE positive
  and namespaced-id logical negative.

## Focused reference results (pre-seal; not a global suite)

| Check | Result | Scope |
|---|---|---|
| `check-atoms.v1.py` | 66/66 pass | atom unit maps; includes P-FILE/P-PACKAGE and N-controls |
| `check-semantic-replay.v3.py` | 18/18 pass | includes `imports-file-first-party-exists` and `imports-file-none-false-on-mapped-target` through `identity-model.v3.close_run` |
| `check-query-projection.v3.py` | 114/114 pass (was 109) | five new owner-admitted imports occupancy controls via `execute_graph_query` |
| `check-execution-inputs.v1.py` | mismatches [] | V2 host-derived sidecar not a stage output |

Commands (review env):

```text
/tmp/opensip-architecture-review-env/bin/python -I -B check-atoms.v1.py --output DIR
/tmp/opensip-architecture-review-env/bin/python -I -B check-semantic-replay.v3.py --out DIR
/tmp/opensip-architecture-review-env/bin/python -I -B check-query-projection.v3.py --out DIR
/tmp/opensip-architecture-review-env/bin/python -I -B check-execution-inputs.v1.py --receipt PATH
```

These are focused pre-seal runs. Global source-pins / whole-suite receipts
were **not** regenerated and are **not** claimed passed.

## Changed-files inventory (vs frozen24, reviews excluded)

New:

| bytes | sha256 | path |
|---|---|---|
| 19173 | `1ec8c07ae18558671de8d8a9f703767eae67ce18f27500a6a534fd29a7bc67a2` | `docs/coop/design-corrections/foundation/target-attribution.schema.v2.json` |

Changed:

| bytes | sha256 | path |
|---|---|---|
| 22290 | `030e9e9cea54ec93667be86e4e59b68f6a307e7847d2115621b71f77b704f7b3` | `foundation/atom-evaluation-contract.v1.md` |
| 90962 | `99d9d79fe5ace3c22595791924b89fad7a2cdbc38835425c605db8779703e6c4` | `foundation/atom_model.v1.py` |
| 88385 | `e11879db009e5fbe28f50e0472f388f8f00629dcb44548c61637e861aeef9525` | `foundation/check-atoms.v1.py` |
| 61213 | `cedae4090f14f18dcdba7dc87ca7c707c2319dcc7f13cff2fca57d8f8c280ce4` | `foundation/check-execution-inputs.v1.py` |
| 22589 | `e1ff5ee2cd2985b9d12587ec6c3171eda5f7165f07d6ffce8b8219cbc1ca8aca` | `foundation/check-semantic-replay.v3.py` |
| 59285 | `26e7f3018dd013ade6450460d4f9b53d2e0ea53e12836a9fe12ce8f03e7ccccc` | `foundation/evaluator-projection-registry.v1.json` |
| 39520 | `3eb0f2794fd2e0aa0d5b1585a04f8e118dcddb6928f8962db67c262d9506eb03` | `foundation/evaluator_semantic_fixture.v3.py` |
| 15464 | `1e7cf5fee2842cb66e499bdf3209c585e05c667a43da40726dd3ba29bd2b3a23` | `foundation/execution-inputs-contract.v1.md` |
| 71178 | `bdd22a5027ad152c6d221171466f061997f83e79d0033c0d2c159429e09cc5e3` | `foundation/execution_inputs_model.v1.py` |
| 138007 | `b748ab305d2d4ccb38ab2ffeb91061168334d41bf4d8424280e937488c659f82` | `foundation/identity-model.v3.py` |
| 184087 | `366e840db364805f9d90727c81e7ea85331d5ad560a566896a6fecb639405939` | `foundation/identity-schemas.v3.json` |
| 1904 | `01a21472b14d130b69baa53ca08f69d1f5aabd07e2240567d67518daa68ab414` | `foundation/shared-profile-decisions.v1.md` |
| 47911 | `23e7246e135daa77361b81601e2e61eacd52b9f5ede6340a03d164136cb23b4f` | `workflows/check-query-projection.v3.py` |
| 19101 | `f89d9fcd020d2c4611ec15faaffdb88e1e3c51c20851b12c8a47d6fbddba450e` | `workflows/query-projection-contract.v3.md` |
| 54283 | `083b16dcc57ede784b5c20168d22a56733c79ebf4b909286bf952c3925b41b95` | `workflows/query_projection_model.v3.py` |
| 119487 | `f5eb51304c10816e93a532f806d5764b9f238fd2e35791097d22d48cafb533d1` | `docs/v2/contracts/product-v1/identity-and-evidence.md` |
| 263758 | `f616fa641f320ebf9dbbae95f8ff5798c8c9a086c92b2dde92db99bbba42ff97` | `docs/v2/contracts/product-v1/native-evidence.md` |

`foundation/` prefixes above are under `docs/coop/design-corrections/`.

## Required root pin / merge work

1. Add `foundation/target-attribution.schema.v2.json` to
   evaluator3/native/workflow/security source-pins. Point
   `identity-schemas.v3.json` byDomain (already pointed in this tree) and
   pin inventories at the hashes above.
2. Merge root’s **separate** import/closure-kind enforcement patch into
   `identity-model.v3.py` after this handoff. This authoring did not edit
   general `import.producerClosure=provider` enforcement. The two edits
   should not overlap if root only adds closure-kind checks on import
   records.
3. Do **not** rewrite frozen24 or historical review evidence.
4. Regenerate whole-suite receipts only after both patches are merged.
   This session’s focused checks used documented pre-seal pin state and
   do not substitute for sealed global suites.
5. Register new TARGET_ATTRIBUTION_* internal keys in public-detail/D9
   when root integrates (same pending standing as V1 keys).
6. `check-array-orders.py` will need to observe the new v2 schema on the
   next pinned run.

## Honest remaining findings

- Schema-admitted positives are **representation**. Synthetic full Runs
  through `close_run` are **not** compiler extraction truth.
- Incoming `none=true` under complete sufficiency for an *unmapped*
  namespaced file is now **indeterminate** (C14 risk closed). A fully
  admitted `none=true` on an external occupancy with complete search was
  not newly constructed as a strong Run in this turn; atom-level
  external nomatch and missing-sidecar unknown were.
- Global pin seal, readiness, application, and independent reviews are
  not done.
- Native protocol3 wire frames were not extended; capture is the
  existing host-derived typed-input channel with an explicit producer
  join.

No acceptance or readiness is claimed.
