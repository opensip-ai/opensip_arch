# Query42 discrepancy assessment: consumer vectors vs strong-owner captures (frozen source42)

**Author:** bounded AUTHOR f5617310-c7c7-4d85-acdd-31370f220944.

**Standing:**
- This is an author diagnosis. It is not independent source acceptance and not a blind reconstruction.
- Nothing was written to LIVE, frozen42, historical inputs, root, independent85 or consumer runtimes; independent85's runtime was neither read nor contacted.
- The consumer's code and results were read only to understand its interpretation. Every adjudication below rests on normative source selectors and discriminating owner measurements.

## Verified inputs

| Input | Verified value |
|---|---|
| frozen42 manifest | sha256 `f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307`; 12913 members, 737766584 bytes, 0 missing/mismatched/extra, before and after |
| consumer vectors | `f47edb50affbab018390c6599d3aae5b780af826ad30a4f4b29b5e1416111884` |
| root replay verification | `139799cd8a0438f06b959dfc58f477a2db229328c619876dc523a25be7826a54` |
| root capture reports | cmp-base `6000c8f5…`, cmp-code `8aa8e4da…` (unchanged) |
| root transport reader | `6fa376bb…`, matches its pin |
| root query reader | `6e0cd4ac…`, matches its pin |
| consumer exports | cmp-base `f4039acf…`, cmp-code `a1e19ef7…`, equal to root report `exportSha256` |
| frozen owners | `query_projection_model.v3.py` `bb9de8f7c7fece1bee3cdda9b9f0c93f4afa33a0a17ec822db8db2dc77a2a62c`; `identity-model.v3.py` `a6dc5f997b5b9502d185d1b68a61765516ccf5f64f1c33a4282682ebee2803dc` |

Receipts: `receipts/inputs-verify.json`, `receipts/inputs-verify-final.json`.

**Method.**
- **Probe** (`tools/probe_owner.py`, receipt `receipts/probe-owner-base.json` `01d6293f…`):
  - decodes the exact exports with root's pinned transport;
  - fully admits each Run (`open_run_closure` plus `close_run`) before any query;
  - executes every captured vector with its exact request and host observations;
  - retains the complete owner carrier, including the actual `QueryRefusal.envelope(host)`, the termination and the private diagnostic.
- **Discriminators:** marked NEW-WORLD. They use only the owner's own issued tokens or explicitly varied lawful host observations. No cursor was translated and no vector was rewritten.

## Summary of classifications

| # | Discrepancy | Classification | Blocker? |
|---|---|---|---|
| 1 | page-1 `nextCursor` hash; owner refuses consumer page-2 tokens | **permitted choice**: opaque host token encoding freedom. Neither implementation is wrong. | no |
| 2 | `path-both-direction` edge endpoint orientation | **normative gap**: `GraphPathEdge` orientation under `incoming`/`both` is unspecified, while backends must reproduce "the same result". A clarification is proposed. | not a consumer or reference defect; needs an owner decision |
| 3 | `availability-partial`: consumer `partial`, owner `retained` | **reference defect** (strong owner discards the observed current availability). Correction proposed. | yes, until the correction or an equivalent owner decision is integrated |
| 4 | success `termination` presence, `resolutionLimitations.note` prose, refusal `remedy`/`subject` prose | **permitted choice**: optional, bounded explanatory content. All 23 consumer failure envelopes are route-identical to the owner's. | no |

## 1. Cursor binding and preimage

**Normative selectors.**
- `query-projection-contract.v3.md` §5 `:136`: "**Cursor.** Opaque token, max 256 chars. Reference form `q3.<runId-64hex>.<selectionHash64>.<position>` binds project+Run+fact-views+operation+effective params (including materialized `includeStart` default)+order+position. The token grants no authority … Continuation requires request `view.{runId}` equal to the bound Run. Rebuild from the same available closure is allowed."
- `schemas/evaluator3/graph-query.schema.json#/$defs/Page/properties/cursor.description`: "Opaque **host** token bound to projectId+runId+factViewDigests+operation+effective params/order+page position … Reference form q3…".
- `workflows-and-surfaces.md:1174-1178`: a continuation binds project, Run, fact views, operation, effective parameters, ordering and position; incompatible continuation inputs cause the contract's typed refusal.
- §7 table `:185`: cursor bind mismatch routes `request-rejected` / `REQUEST.PRECONDITION_FAILED` / `QUERY.CURSOR_MISMATCH`.
- A search of the product contracts, the workflows contracts and the evaluator3 schemas found no cursor or token portability requirement across hosts or implementations.

**Exact preimage comparison.** Both hashes reproduce exactly with the owner's `canonical.canonical`. Effective params equal the request params for this request (no `includeStart`; the endpoint is already canonical).

- **Owner** (`query_projection_model.v3.py` `selection_hash`) → `0143c88c0d70b2b5c3333a23f31300557bb9a8ff4cf96a250f448e0d21e7c8d4`:
  `{"factViewDigests":["view2:9bb0c687…ed244"],"operation":"graph.neighbors","params":{"direction":"outgoing","endpoint":{"kind":"symbol","nativeSubjectId":"ts:src/index.ts#main","universe":"0b62f4e8…ef9bc"},"minResolution":"resolved-callee","relation":"calls"},"projectId":"prj1-abce1fba…29cf5","runId":"run3:88d6ffc5…87e54"}`
- **Consumer** (`phase9_graph_query.py` `selection_hash`) → `842048242abf784efa5114f74a19ab6d604db6e3522324ad0bb3994969f6b58d`: the identical record plus `"order":"query-projection-contract.v3 s3/s4"`.
- **The only record difference is the `order` member.** Both bind the published inputs, and "order" is itself a listed binding component. The contract fixes *what* is bound and calls the token opaque. It publishes a *reference form*, not a mandated preimage recipe, so encoding freedom is expressly allowed.

**Discriminating measurements (NEW-WORLD, owner's own tokens only).**
- **Foreign token:** the owner refuses the consumer token on both page-2 vectors with a complete schema-admitted envelope: `request-rejected` / `REQUEST.PRECONDITION_FAILED` / `QUERY.CURSOR_MISMATCH`, exit 2, `projectId` present, no `run`. That is the published route for an incompatible continuation.
- **Own token:** the owner's page-1 token on the same page-2 request (`view.runId` bound, host `latestRunId` naming a newer Run) returns page 2. The context shows `traversalCoverage=complete` with no further cursor, and its items equal the consumer's page-2 items.
- **Cache:** the same request with host cache present returns an identical response (`cacheInvariant=true`).

**Conclusion.** Both implementations satisfy the binding law with their own tokens. Cross-implementation token acceptance is not required, so the two page-2 vectors are not a cross-host conformance control. I did no cursor translation to make any control pass.

## 2. `path-both-direction` edge orientation

**Normative selectors.**
- Contract §3 `:76-80`: projected edge `source`/`target` come from the fact and payload.
- §4 `:95`: path law; canonical BFS, `fact2`-order adjacency, shortest path, lex-least `fact2` tie-break.
- §4 `:98`: "`outgoing` follows source→target; `incoming` follows reverse; `both` treats the projected edge as undirected."
- §4 `:102-116`: the canonical walk processes "eligible directed hops", and "Other backend strategies must reproduce the same result and disclosure".
- Schema `GraphPathEdge {factId, source, target}` has no description. `GraphPathRow` is `nodes`/`edges` in `sequence` order, with "One simple path …" and no orientation statement.
- Maintained controls (`check-query-projection.v3.py` path goldens) check only hop count and `factId`.

**Measurements.** Lawful admitted cmp-code endpoints; stored fact `fact2:44e53189…` is `main→helper` (`calls@resolved-callee`).

| Query | Owner edge source→target | Owner `edges[i]` chains `nodes[i]→nodes[i+1]` |
|---|---|---|
| path helper→main `both` (the vector) | helper→main (reversed) | yes |
| path helper→main `incoming` | helper→main (reversed) | yes |
| path main→helper `outgoing` | main→helper (stored) | yes |
| neighbors `both` at helper | main→helper (stored; neighbor rows keep fact orientation) | n/a |

- **Consumer:** its path row keeps the stored `main→helper` orientation, so its edge does not chain its `nodes`.
- **Schema:** both path responses admit.

**Conclusion: normative gap.** Both representations are coherent and schema-admitted, and neither contradicts a published sentence. Yet the contract requires every backend to reproduce the same result. The owner's representation is not an algorithm error, and the consumer's is not a helper defect.

**Proposed clarification** (§4, documentation only; no schema bytes): "A `graph.path` row reports the hops its walk took: `edges[i]` is the directed hop from `nodes[i]` to `nodes[i+1]` … `factId` still names the stored fact. `graph.neighbors` rows keep the projected fact's own source→target."
- It pins the strong reference's existing behaviour, so no reference code changes.
- Two controls (`path-incoming-edges-are-traversed-hops`, `path-both-edges-are-traversed-hops`) pin it.
- **Owner decision:** stored orientation is an equally coherent alternative that would require a reference change.

## 3. `availability-partial-does-not-grant-or-refuse`

**Positive admission law (unchanged, both agree).** Contract §7 `:160`: "`retained`, `partial` and an omitted observation neither refuse nor grant: `close_run` still decides … The observation cannot grant retained authority."
- Both implementations admit the same Run and return identical items.
- The existing control `host-availability-partial-cannot-admit-missing-bytes` still refuses.

**Response-field law (separate).**
- `identity-and-evidence.md:1721-1725`: "Current availability is a separate monotonic-generation record: retained, partial, expired, purged, corrupt or unavailable, with exact missing references and cause … sealed assurance and historical verdict never change. **A query reports both.**"
- Contract §7 `:160`: identity availability "is a trusted current host observation".
- `workflows-and-surfaces.md:1185`: "All query responses carry their owned view, evidence disclosure, availability …"; `:1190` makes `availability` a required parity field.
- `graph-query.schema.json#/$defs/GraphOperationResponseContext/properties/availability`: required, enum including `partial`.

**Measurement.** For an omitted, `retained` or `partial` observation, frozen42's owner returns `context.availability="retained"` with identical items (sha `ed465d59…`). Two lines produce this: `observe_availability` returns `"retained"` for `partial`, and `execute_graph_query` passes a hardcoded `"retained"` to `finish_operation`. An owner response with `partial` substituted is schema-admitted.

**Conclusion: reference defect.** The strong owner upgrades an observed current `partial` availability to `retained` in the successful response, erasing the disclosure identity law says a query reports. The consumer's `partial` is consistent with the law. Owner admission, items and all refusal routes are otherwise correct.

**Residual note, not a blocker.** No sentence states the value for an *omitted* observation. Both implementations report `retained` after `close_run` admission. The correction preserves that without claiming it as new law.

## 4. Optional termination, limitation notes and refusal prose

- **Termination.** `GraphQueryResponseV1.termination` is optional (schema `required` omits it). `workflows-and-surfaces.md:1193` says "any optional termination", and `:1198` says "If the response carries termination, its entire object must equal the enclosing termination." Owner responses without termination and without notes still admit. The consumer's success envelopes carry `{class: success}`, and its `indeterminate` responses include the equal termination. **Permitted choice.**
- **Notes.** `resolutionLimitations[].note` is optional `BoundedText`. Every limitation `kind`, `factId`, relation, rung and count field agrees; only `note` prose differs, or is absent. **Permitted choice.**
- **Refusals.** For all 23 captured consumer failure vectors, the owner's actual envelope equals the consumer's on every route field: `kind`, `exitCode`, `requestId`, `projectId` presence/value, `termination.class`/`errorCode`/`faultCause`, `domainDetail.code`, `errors[].code` count, and absence of `run`.
  - Only `remedy`/`subject` differ. Contract §7 `:156`: "Refusal messages are diagnostic; the table below selects every public route."
  - All consumer failure envelopes and all consumer positive responses admit under the owner's schemas.
  - The two page-2 consumer positives are refused by the owner as a foreign-token continuation (§1 above).
  - **Permitted choice.**

## Proposed correction (author copy only; proposal, not acceptance)

`correction.patch` has sha256 `4c32d6c3abcc78d8794ba53eb11b03c0989b6eb45561bceb520bb0dbc3b10738` (10714 bytes). `delta-manifest.json` lists each file below; every base file is byte-identical to frozen42.

| File | Base sha256 | After sha256 |
|---|---|---|
| `workflows/query_projection_model.v3.py` | `bb9de8f7c7fece1bee3cdda9b9f0c93f4afa33a0a17ec822db8db2dc77a2a62c` | `9a8f9c09c70cf56aff8f353b7592fb5ce0eb2a58ad101a08a1ce56f006568b7c` |
| `workflows/check-query-projection.v3.py` | `8e2c2b6b4b202cb630e99c97d095a5efe34d0bf34aca8cf81d1dd6bfddc5ed52` | `466d6abb2a9ccdb2be7e6a0b655e9e33cef94fc64d5facdfb478bc6b58a531f9` |
| `workflows/query-projection-contract.v3.md` | `923ff32fc9e063f8c9af00bb7943f77bb47a09d876826ca425e0cd580cee8a4b` | `47ccc81ccc33263520affe0340946aba5178bcac33131de88e6be638a1718d5f` |

**Changes.**
- **Model (item 3):** `observe_availability` returns an observed `retained`/`partial` as observed, with omitted still `retained`. `execute_graph_query` passes it to `finish_operation`. The internal `traverse_projected_graph` constant is unchanged, and so are refusal routes and the precondition.
- **Contract:** one §7 sentence (item 3) and one §4 sentence (item 2).
- **Checker:** 5 new controls.
  - Availability: `host-availability-partial-reported-in-response` (the discriminator); `…-partial-changes-only-availability` and `…-retained-and-omitted-report-retained` (preserved positives).
  - Path: the two hop-orientation pins.
- **Unchanged:** no schema bytes, identity or native owner, or `workflows-and-surfaces.md`.

**Receipts** (runtime copies, 1347 files ×2, 0 mismatches; `receipts/copy-trees.json`)

| Run | Checks | Failed | Report sha256 |
|---|---|---|---|
| `check-query-projection` base | 204 | 0 (exit 0) | `7fd0b56bbe7e8b4a7844e286a755caf340d02982638845ea49f8319fb335b697` |
| patched | 209 | 0 (exit 0) | `111ca6166c1822cf1e9578a505be6209e60a2c9f96bfd7a20ad5fc2a336848fb` |
| controls-only (frozen model + patched checker) | 209 | 1 (exit 1): exactly `host-availability-partial-reported-in-response`, detail `retained` | `8de602672395629118de63e83add7d9548543ce43fcde0843e0fb9791f2ef5f0` |

- **Comparison** (`receipts/compare-base-patched.json`): the 204 shared checks are unchanged.
- **Exact-vector probe on the patched tree** (`receipts/probe-owner-patched.json` `1e4663c0…`): across all vectors the only difference is `availability-partial-does-not-grant-or-refuse` `/owner/response/context/availability` (`retained`→`partial`), plus the matching NEW-WORLD partial row. Every refusal route, cursor outcome and orientation result is unchanged.

## Boundaries and limitations

- **Not captured.** Three vectors are left for root accounting and were not inferred: `neighbors-evidence-limitations-with-complete-traversal` (run `syntax-mixed-disclosed`), `missing-retained-bytes` (`cmp-code~missing-bytes`) and `corrupt-retained-bytes` (`cmp-code~corrupt-bytes`). The `cmp-scope` wrapper failure is root bookkeeping ("No vectors for explicit Run label"), not a query issue. The wrapper metadata's trailing-`\n` quoting defect was not used; the per-run `report.json` files were.
- **Standing of evidence.** Owner outcomes are reference executions over exact exported stores after full admission. They are not product qualification, renderer parity or application acceptance. I did not run consumer code; its behaviour is taken from its recorded vectors and source.
- **Not run:** broad suites, pins, planning, source freeze, and independent85 artifacts.
- **Owner decisions.** The §4 path clarification is a choice between two coherent representations. The §7 availability sentence restates identity law for the response field. The omitted-observation value is left as a noted, non-blocking unstated point.
- **Integration.** Owned hashes of the three files change, and pin updates belong to root.

## Remaining blocker

**Item 3** (strong-owner availability disclosure) remains until root integrates the correction or an equivalent owner decision.
- **Item 2** needs an owner decision on the orientation rule. Neither current implementation is defective under present law.
- **Items 1 and 4** are not blockers.
