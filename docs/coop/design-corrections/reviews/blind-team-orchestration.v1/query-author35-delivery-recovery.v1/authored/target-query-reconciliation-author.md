# Target query reconciliation — author (M3 / S1)

**Standing:** proposed correction only. Not scoped self-acceptance, not final peer
review, not pin reseal, not product implementation. Root integrates and reviews.

Role: same actual Grok coauthor, now **author** for bounded M3 query
reconciliation (plus S1). COMPLETE51 CHANGES_REQUIRED peer report is retained
**unchanged**. M1 provider-return and M2 identity-contradiction are out of
scope (separate copy; not read or written).

`target-identity-successor.v1` and frozen24 were read-only. Writes are this
task output only.

## Prior finding dispositions

| Id | Prior (COMPLETE51) | This proposal |
|---|---|---|
| **M3** | MUST: query projects raw sidecar occupancy; unknown sidecar + exact-id inventory unprojectable though atom matches | **ADDRESSED in proposed bytes** — `execute_graph_query` consumes `atom_model._reconcile_attribution` over retained Run inventories/sidecars. Owner Run controls pass. Not a final peer verdict. |
| **S1** | SHOULD: query contract leftover TargetAttributionV1 in fact law and wrapper step 4 | **ADDRESSED in proposed bytes** — table/fact law/step 4 name reconciled V2 occupancy; V1 is historical/not selected. |
| M1 | MUST provider return | Unchanged; not this patch |
| M2 | MUST sidecar overwrite of exact-id occupancy | Unchanged; query imports current `_reconcile_attribution` signature. M2 should preserve that signature. |

## What changed

Query projection no longer reads raw sidecar `occupancy` / `evaluationNativeId`
as the occupancy identity. `execute_graph_query` builds atom-shaped inputs
**only** from the admitted Run:

- `proof.evaluationInputRefs` domain `subject-inventory` and `target-attribution`
- plan registered enumeration-plan parameter
- producer closures named by selected facts and those sidecars, looked up in
  the retained `objects` map

It then calls `atom_model._reconcile_attribution` (exact-id ephemeral first-party
when payload native id uniquely equals one inventory native id; known ephemeral
fields override unknown sidecar). Payload bytes are attached onto the retained
fact record because Run facts store `payloadDigest`, not an inline payload.
No SubjectIdV1 namespace parse. `host.targetAttributions` / cache / standing
are ignored. Unselected store blobs are not read.

Projection rules after reconcile:

- **First-party:** inventory spelling (`nativeId`, package path).
- **External:** opaque payload id; packages still need `packageManifestPath`.
- **Multi-kind imports:** unknown occupancy with no unique exact-id →
  `unprojectable-fact`.
- **Single-kind** (`calls`/`references`/…): unknown occupancy still projects
  the payload native id (lawful external/unknown vertex).

Historical V1 sidecars are unprojectable on this profile (`TARGET_ATTRIBUTION_SCHEMA_VERSION`).
They are not selected; frozen24 V1 remains historical.

`atom_model.v1.py` is **not** in this proposal. Coordination for M2: keep
`_reconcile_attribution(fact, spec, inputs)` and `_ephemeral_target(fact, spec, inputs)`
and `AtomAdmissionError.key`. If M2 later wants a public adapter, add it
instead of a second occupancy implementation. Query does not duplicate provider
authority.

## Proposed paths and hashes

Patch: `target-query-reconciliation.patch`
SHA-256 `3f76e1562f05c26d609e7d7b467898400d9eb1220452f63a5cc523873375068a`
(28442 bytes), relative to `target-identity-successor.v1`.

| Path | SHA-256 | bytes |
|---|---|---|
| `docs/coop/design-corrections/workflows/query_projection_model.v3.py` | `4c9c91215fb70653ae75b563f6ba38788e410eb4004c4e9765e3bc08e8259e0a` | 58283 |
| `docs/coop/design-corrections/workflows/query-projection-contract.v3.md` | `a7c642849cf380fd878541fee816955ae3651a09ab8a0926e93456a7f839f4c2` | 20762 |
| `docs/coop/design-corrections/workflows/check-query-projection.v3.py` | `f90f100142bcbeaab546aa270365c82b5f9b28f972da152e29cbc3787230054c` | 52470 |
| `docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py` | `87aed7412091f67103c815f35c8ce9714037348d4d71f3771fda88119a76ae5e` | 40539 |

Full files live under `output/proposed/<repo-relative path>`.

Fixture default `imports_occupancy="mapped-file"` preserves the existing
imports-file sidecar graph. New modes: `exact-id-symbol`,
`unknown-sidecar-symbol`, `unmapped-file`.

## Checks (disposable overlay, pre-seal)

Source inputs hashed (successor vs proposed) before overlay. Global pins were
not resealed; `run-evaluator3-checks.py` was **not** invoked and is not claimed
as a whole-suite pass. No pin bypass.

Disposable work: `output/disposable/work` (successor `docs/` minus reviews,
proposed files overlaid). Python `/tmp/opensip-architecture-review-env/bin/python -I -B`.

| Command | Exit | Result |
|---|---|---|
| `check-query-projection.v3.py --report …/query-projection.receipt.json` | 0 | **123/123** required checks, 0 failed |
| `check-semantic-replay.v3.py --output …/semantic-replay` | 0 | **passed 18** (default mapped-file fixture unchanged) |

New owner-admitted `execute_graph_query` controls (all ok):

- `owner-imports-symbol-exact-id-no-sidecar-query` + `…-atom-run-agrees` (Run verdict fail, ≥1 finding; query incoming `symbol:foo` has the edge)
- `owner-imports-unknown-sidecar-unique-inventory-query` + `…-atom-run-agrees` (unknown sidecar does not erase exact-id occupancy; `host.targetAttributions` does not grant occupancy)
- `owner-imports-file-occupies-inventory-vertex` + `owner-imports-mapped-file-atom-run-agrees` (ordinary mapped file)
- `owner-imports-unmapped-no-exact-id-unprojectable` + empty incoming on `a.ts` + atom Run findingCount 0

First failure: none in this focused pair. Earlier disposable attempts failed on
missing `public-detail-registry` / `artifacts/delivery.v4.json` until the copy
included full `docs/` minus reviews; those were copy-scope faults, not design
failures.

## Review-tree custody (original report unchanged)

The COMPLETE51 peer markdown/json are not edited.

The public CLI background completion
`ab4ca65fd9fe87be919a76651de90db7a35e653274c3ccf14f1f1a3bbecd7054` recorded an
**initial whole-tree hash comparison** of successor vs frozen24, including
review-tree **file bytes**. That is hash-only file identity, not a semantic
read of review histories.

The peer report limitation that said the review tree “was not hashed as part of
the change-set” described the **later bounded source-content inspection**, which
did not open review-history documents. Hash-only access need not imply semantic
history read. This handoff distinguishes:

1. Initial hashing (whole tree, including review-tree bytes; hash-only).
2. Later bounded inspection of the 18-file change-set and owning laws (no
   review-history content read).

Root retained that background notice verbatim with an exact hash-only
exception. That is public custody metadata, not substantive agreement with
review-history claims.

## Limitations

- Not final peer review of these proposed bytes.
- M1/M2 remain open on the original successor.
- Query currently imports private `_reconcile_attribution`; if M2 renames it
  without a shim, this overlay will fail at first occupancy call.
- Global evaluator3 pin ledger is stale; focused passes are pre-seal.
- No compiler/host/platform qualification; no new graph kinds or per-language
  Runs.
