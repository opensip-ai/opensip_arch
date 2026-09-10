# Query / attribution independent architecture review

Same P4 kit-only reviewer origin. Bounded to the TS author's two alleged normative tensions and original query **input** suitability. Not query execution, not whole-Run admission, not whole-consumer ACCEPT.

**Scoped identity-closure observation (not acceptance):** earlier structural MUST `ts.compilerPackageDigest-is-toolchain-tree-member` is still present on this new store. Query interpretation below is **diagnostic / not acceptance**.

## Custody

- new-inputs manifest `7ca1f3c9e8a68acecf23584998a90bd04ebac4c97f1310a6f076bb29c830003d` match=True
- `query-run-completion-review.md` `5aad9ebbfd9776e197a729b07da1ae83d98a544b452ddf0b20d9aca014b08d2b` match=True
- `query-run-completion-review.json` `59bcab77c5d10b57445bc00d17c8f3e11d0df9a912d8bb2ffd253a71b5b90dfe` match=True
- `query-run-graph-inventory.json` `6b525741231b3258c9e36b40241e803dc28d07223c619197aee5bc2a6b07635c` match=True
- `runs/ts.store.json` `59b7d384f886899083d356a4db41cec3a5cd87b3584027ec3e71cc0adddce062` match=True
- kit `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` match=True
- charter `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` match=True
- this store `59b7d384f886899083d356a4db41cec3a5cd87b3584027ec3e71cc0adddce062`

Command: `/tmp/opensip-architecture-review-env/bin/python -I -B /private/tmp/opensip-design-corrections/consumer-b.v12-kit-query-attribution-review.v1/output/independent/query_attribution_review.py`

Author helper scripts, root checkers, and expected values were not read. Author completion MD/JSON/inventory/store are claims and retained bytes under review.

## Constraint map (required vs permitted)

### G1-SubjectIdV1-vs-file-inventory-nativeSubjectId

**Author claim:** Imports resolvedTarget is file:src/index.ts; file inventory native id is src/index.ts. First-party occupancy cannot match without namespace parsing.

**Real contradiction:** False. **Missing law:** False.

Classification: existing-law identity inequality; inconvenient for first-party occupancy on namespaced SubjectIdV1 file targets, not a gap

Owners:
- `foundation/relation-payload-schemas.v2.json#/$defs/SubjectIdV1`
- `foundation/subject-inventory.schema.v1.json InventoryRowV1.nativeSubjectId (file=LogicalPath)`
- `foundation/target-attribution.schema.v1.json occupancy/targetNativeId and x-opensip-join-law.derivation.never`
- `foundation/atom-evaluation-contract.v1.md §2 Native-id compare is first`
- `workflows/query-projection-contract.v3.md §2–3 tuple (universe,kind,nativeSubjectId,packageManifestPath)`

Required:
- File inventory nativeSubjectId is the snapshot path (equals path).
- imports resolvedTarget is SubjectIdV1 (namespace:opaque).
- targetNativeId equals payload resolvedTarget.
- Never parse SubjectIdV1 spelling to invent kind or occupancy.
- occupancy=first-party iff targetNativeId is a first-party inventory subject of targetUniverse (exact native id).
- Sidecar occupancy=external is consistent when ephemeral is not first-party; occupancy=first-party then refuses TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY.
- Query nativeSubjectId for a projected fact is payload[sourceField]/payload[targetField] as retained; kind is table sourceKind or attribution kind. No invented or stripped namespaces.

Permitted:
- occupancy external|unknown when no exact inventory nativeId match
- external resolved targets that are not first-party inventory remain lawful query vertices via projected-fact endpoints
- logicalPath non-null only when occupancy is external or unknown

Guidance: Keep occupancy=external (or unknown) for namespaced SubjectIdV1 file targets. Do not parse file: off the payload to force first-party. Do not treat inventory path src/index.ts and payload file:src/index.ts as one query vertex.

### G2-TargetAttributionV1-draft-vs-execution-inputs-domain

**Author claim:** Schema is DRAFT pending root ProofInputRef integration, but execution-inputs.schema.v1.json already names domain target-attribution.

**Real contradiction:** False. **Missing law:** False.

Classification: stale draft title on the record schema; current identity-schemas.v3 and execution-inputs already incorporate the domain. Draft/historical labels are not blanket authority.

Owners:
- `foundation/identity-schemas.v3.json#/x-opensip-digest-domains/byDomain/target-attribution (canonical-record, document foundation/target-attribution.schema.v1.json, retention preimage)`
- `foundation/identity-schemas.v3.json#/$defs/ProofInputRef/properties/domain enum includes target-attribution`
- `foundation/execution-inputs.schema.v1.json#/$defs/InputRefV1 domain enum includes target-attribution`
- `foundation/execution-inputs-contract.v1.md §7 host-derived typed input`
- `foundation/atom-evaluation-contract.v1.md §2 sidecar is provider attestation`
- `query-projection-contract.v3.md §3 imports without TargetAttributionV1 are unprojectable`
- `target-attribution.schema.v1.json title DRAFT; x-opensip-identity.proofInputRef.standing NEW pending root; x-opensip-new-internal-faults NEW/internal public-detail`

Required:
- When selected, target-attribution blobs are canonical-record preimages under identity-schemas.v3 byDomain.
- Query projection of imports@resolved-target requires a retained TargetAttributionV1 for that sourceFactId.
- Do not treat host.cache/host.targetAttributions as public graph evidence (query §8).

Permitted:
- Schema-file title still says DRAFT; that does not un-register the identity-schemas.v3 domain.
- Some public-detail/D9 routes remain NEW/internal; that does not make the record unusable as a selected blob input.

Guidance: Treat TargetAttributionV1 as a current selected canonical-record input where identity-schemas.v3 and execution-inputs name it. Do not refuse or waive based on the schema file's DRAFT title. Remaining NEW/internal fault-route standing is not ProofInputRef absence.

## Current byte observations (TS store)

- Projectable imports@resolved-target facts with TargetAttributionV1: 2
  - `fact2:a5570c5ea598e6292b20fec608e160a06b29c1dc4ac052ee21922b929b0fa6bd` source `{'universe': '2c475675b3b873ebf07ff153339460c55ab8770f266cf8f8f9f0bc0a19de89a8', 'kind': 'symbol', 'nativeSubjectId': 'module:src/index.ts', 'packageManifestPath': ''}` → target `{'universe': '2c475675b3b873ebf07ff153339460c55ab8770f266cf8f8f9f0bc0a19de89a8', 'kind': 'file', 'nativeSubjectId': 'file:node_modules/left-pad/index.js', 'packageManifestPath': ''}` occupancy=external exactNativeIdFirstParty=False externalConsistent=True
  - `fact2:ddc3eeb902d147e7bdacb0b09d0b745b9f0998def6b70df21e15e7ebb63e3cf8` source `{'universe': '2c475675b3b873ebf07ff153339460c55ab8770f266cf8f8f9f0bc0a19de89a8', 'kind': 'symbol', 'nativeSubjectId': 'module:src/app.ts', 'packageManifestPath': ''}` → target `{'universe': '2c475675b3b873ebf07ff153339460c55ab8770f266cf8f8f9f0bc0a19de89a8', 'kind': 'file', 'nativeSubjectId': 'file:src/index.ts', 'packageManifestPath': ''}` occupancy=external exactNativeIdFirstParty=False externalConsistent=True
- Unprojectable stored imports facts: [{'factId': 'fact2:53b10ce1811f1aa4669230f8c9a616719bac8740319a0f212a68d07d2e571da5', 'reason': 'imports@resolved-target without TargetAttributionV1', 'payload': {'importer': 'file:src/index.ts', 'resolvedTarget': 'file:node_modules/left-pad/index.js', 'specifier': 'left-pad'}}]
- Author two-fact path exists under tuple law: **False** witness=None
- imports source kind is symbol and nativeSubjectId is payload.importer (e.g. module:src/app.ts). Target kind is attribution.kind=file and nativeSubjectId is payload.resolvedTarget (file:src/index.ts). The second fact source is symbol/module:src/index.ts, which is not the first fact's target file/file:src/index.ts. Tuple law does not identify those endpoints. Author hopCount>=1 over both facts invents a chain by stripping namespaces/kinds.
- Neighbors at (symbol, `module:src/index.ts`): ['fact2:a5570c5ea598e6292b20fec608e160a06b29c1dc4ac052ee21922b929b0fa6bd']
- Neighbors at stripped (file, `src/index.ts`) — invented by dropping namespace: []
- Neighbors at (file, `file:src/index.ts`) payload target form: ['fact2:ddc3eeb902d147e7bdacb0b09d0b745b9f0998def6b70df21e15e7ebb63e3cf8']

## Original query input suitability (not execution)

Charter needs: graph.neighbors / path / reach over admitted retained Run; canonical units/order; historical pagination / latest / cache-loss continuation bound to view.runId; endpoint membership (known vs QUERY.ENDPOINT_UNKNOWN); evidence limitations vs stored-edge completion; operation bounds vs page boundaries; malformed/mismatched failure envelopes; full six-key human/JSON/agent parity

Supported as retained graph *inputs* if a later close_run admitted this store:
- Two projectable imports@resolved-target facts exist with TargetAttributionV1 — enough to form neighbor rows at their exact tuples.
- One stored imports fact without attribution is correctly unprojectable (limitation, not absence).
- Isolated symbol inventory ids (if present as evaluationInputRefs subject-inventory rows) are lawful empty-neighbor vertices.
- imports@syntactic-specifier is not a projectable request (QUERY.RELATION_UNSUPPORTED) — not a missing graph.
- calls@resolved-callee / three-endpoint counts are peer suggestions, not MUSTs.

Missing for the original discriminating reconstruction:
- Connected path/reach from module:src/app.ts to left-pad under tuple law: the two projectable facts do not share an endpoint tuple, so they are two stars not one path.
- Query cases themselves (neighbors/path/reach responses, cursors, host.latestRunId, host.runsForSnapshot, testBounds, failure envelopes, six-key parity) are not executed — author states queryCasesExecuted=false.
- historical pagination / latest / cache-loss need host observations not present in the store.
- malformed/mismatched envelopes are request/schema/host, not this store.
- Whole-Run close_run of this new store is not established here; compilerPackageDigest tree-membership and predicate-inputRefs subset still fail as scoped identity-closure observations.

Peer `calls@resolved-callee` / three-endpoint preferences are not MUSTs.

## Satisfiability examples (reasoning evidence, not Run admission)

{
  "standing": "kit-derived reasoning examples; not replacement graph admission",
  "gap1_jointly_satisfiable": {
    "inventoryFileNativeId": "src/index.ts",
    "payloadResolvedTarget": "file:src/index.ts",
    "exactEquality": false,
    "parseForbidden": true,
    "lawfulOccupancy": "external (or unknown if no sidecar). first-party would require targetNativeId to equal inventory nativeSubjectId without parsing.",
    "queryVerticesRemainDistinct": {
      "inventory": [
        "<U>",
        "file",
        "src/index.ts",
        ""
      ],
      "projectedTarget": [
        "<U>",
        "file",
        "file:src/index.ts",
        ""
      ],
      "projectedSource": [
        "<U>",
        "symbol",
        "module:src/app.ts",
        ""
      ]
    }
  },
  "gap1_unsatisfiable_if_author_demands_first_party_and_no_parse": {
    "set": [
      "file inventory nativeSubjectId MUST be snapshot LogicalPath",
      "targetNativeId MUST equal payload resolvedTarget SubjectIdV1",
      "never parse SubjectIdV1 spelling to invent occupancy",
      "occupancy=first-party MUST mean targetNativeId is a first-party inventory subject"
    ],
    "result": "Those four cannot hold together for occupancy=first-party on a namespaced file SubjectIdV1. They CAN hold together if occupancy is external/unknown. Not a missing law."
  }
}

No normative design edit. No graph remint.

