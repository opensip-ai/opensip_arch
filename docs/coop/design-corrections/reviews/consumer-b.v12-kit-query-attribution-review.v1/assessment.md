I'll continue the same kit-only origin, verify the new-input hashes, then independently resolve the author's alleged SubjectId/attribution tensions against current owners.Custody is 4/4. Next I’ll read the author’s gap claims against current query, inventory, atom, and attribution owners.**Neither alleged gap is a current-law contradiction.** The retained TS graph is usable as *partial* query input, not as the charter’s discriminating path/reach/pagination/envelope reconstruction. Author whole-Run closure is **not** accepted.

Wrote only `/tmp/opensip-design-corrections/consumer-b.v12-kit-query-attribution-review.v1/output/query-attribution-review.md` and `.json`. New-inputs 4/4 hashes matched (`input-manifest.json` `7ca1f3c9…`). Stores not reminted. Query operations were not executed.

This new store still shows the earlier identity-closure MUSTs (`compilerPackageDigest` not in the toolchain tree; predicate `inputRefs` not a subset of `evaluationInputRefs`). Query remarks below are **diagnostic / not acceptance**.

## Gap 1 — SubjectIdV1 vs file-inventory `nativeSubjectId`

**Not missing law.** Two published grammars:

- File inventory `nativeSubjectId` **is** the snapshot LogicalPath (`src/index.ts`).
- Imports `resolvedTarget` **is** SubjectIdV1 (`file:src/index.ts`).
- `targetNativeId` must equal that payload field.
- Occupancy join **must not parse** `namespace:opaque` to invent first-party.

Exact equality fails, so ephemeral occupancy is not first-party. Sidecar `occupancy=external` is the consistent choice (`TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY` would fire if they stamped first-party). Query vertices keep the **unparsed** strings. Inventory `(file, src/index.ts)` and projected `(file, file:src/index.ts)` are distinct tuples.

Observed: both attributed facts have `externalConsistent=true`. `logicalPath` carries the snapshot path only because occupancy is external.

## Gap 2 — TargetAttributionV1 “DRAFT”

**Not a contradiction.** The schema **title** still says DRAFT. Current owners already register the domain:

- `identity-schemas.v3.json#/x-opensip-digest-domains/byDomain/target-attribution` (canonical-record, that document, preimage)
- `ProofInputRef.domain` includes `target-attribution`
- `execution-inputs` `InputRefV1` and contract §7 treat it as a host-derived selected blob

Draft/historical labels are not blanket authority. Remaining NEW/internal public-detail routes do not un-register the blob. This store **does** select those blobs (`selectedRefs` and `evaluationInputRefs`).

## Query tuple law vs the author’s graph story

`imports@resolved-target` source kind is **symbol**, `nativeSubjectId = payload.importer`. Target kind comes from attribution; `nativeSubjectId = payload.resolvedTarget`. No namespace stripping.

Projected edges:

- `(symbol, module:src/app.ts)` → `(file, file:src/index.ts)`
- `(symbol, module:src/index.ts)` → `(file, file:node_modules/left-pad/index.js)`

The claimed path `module:src/app.ts` ⇝ left-pad over **both** facts **does not exist**: the first target is not the second source. Neighbors at `(symbol, module:src/index.ts)` see only the second fact. Stripping to `(file, src/index.ts)` yields **zero** projected incidence.

Unattributed `fact2:53b10ce1…` is correctly unprojectable.

## Original query input suitability (not execution)

Present if a later admitted Run used this store: two projectable attributed facts; one unprojectable stored fact as a limitation; isolated symbol inventory ids `variable:app` / `variable:n` as empty-neighbor vertices; `imports@syntactic-specifier` is an unsupported **request**, not a missing graph. `calls` / three-endpoint preferences are not MUSTs.

Still missing for the charter reconstruction: a tuple-faithful path/reach chain; executed neighbors/path/reach vectors; `host.latestRunId` / snapshot-run map / cache-loss continuation; bound vs page truncation; malformed envelopes; six-key parity. Author `queryCasesExecuted=false`.

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-kit-query-attribution-review.v1/output/independent/query_attribution_review.py
```
