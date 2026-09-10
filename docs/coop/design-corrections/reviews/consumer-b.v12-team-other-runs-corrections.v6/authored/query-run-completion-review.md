# Query-run completion (B12 retained-Run graph preparation)

**Verdict: `QUERY_RUN_READY_FOR_INDEPENDENT_RECHECK`**

Same original fresh B12 kit-only author origin. Previous foundation-corrections.v2 is complete and frozen. This pass prepares the **existing TypeScript Run** for the original charter’s retained-Run graph-query reconstruction. It does not add a language, Run kind, product engine, or design semantics. It is not independent review, not automatic acceptance, and not whole-consumer ACCEPT.

`R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` is **not executed**. Graph support is not measured query output.

## Custody

| Object | SHA-256 |
|---|---|
| original-consumer-charter.txt | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` |
| requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` |
| parent subject | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` |
| kit | 80/80 PASS |
| team-inputs.json | `d46c603d921fbf6e6c48ac4100550922ba735bd42382015b3fc1d13862d331b4` |
| six peer reports | PASS vs team-inputs.json |

Peer reports are scope/input observations, not an admission oracle. Charter quantifier is **at-least-one** admitted retained Run. Peer preference for `calls@resolved-callee` and for a three-endpoint count are suggestions. Normalized clones are not required on each language Run; the other four stores stay frozen.

## From-scratch commands (all exit 0)

Second produce is hash-identical. Replay compares C of the complete expected proof to the retained claim. Tamper remints proof/evidence/seal/run then semantically refuses.

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-query-run-corrections.v1/output/scripts/build_ts_run.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-query-run-corrections.v1/output/scripts/replay_from_export.py \
  /tmp/opensip-design-corrections/consumer-b.v12-team-query-run-corrections.v1/output/runs/ts.store.json
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-query-run-corrections.v1/output/scripts/replay_from_export.py --tamper \
  /tmp/opensip-design-corrections/consumer-b.v12-team-query-run-corrections.v1/output/runs/ts.store.json
```

Path redirects: `path-correction-record.query-run.v1.json`. Predecessor TS bytes: `preserved-failures/ts-v5-pre-query-graph/`. Other four stores, foundation artifacts, and existing workflow/query/envelope/vector/trace/checkpoint files: freeze `frozen-this-pass.query-run.v1.json`, **0 mismatches** after rebuild.

## New TypeScript identities

| Field | Value |
|---|---|
| store | `runs/ts.store.json` `59b7d384f886899083d356a4db41cec3a5cd87b3584027ec3e71cc0adddce062` 709674 bytes / 139 blobs |
| runId | `run3:8170fc2c58c49759e89b3994ba92cf2d59f27a7721ac88698985628e2d2057db` |
| planId | `plan2:2193bfbf720142c308aac604a68f8277784e79fa18a41828f729a610342b273e` |
| snapshotId | `snapshot2:2b5a75be1edc1b7334275923a0cde8ab3be91752d3fdce86f823b353972f8536` |
| viewId | `view2:fb50f12e13ec1e479936b82cf658ed9e58dc41d89a83158fbdc4f85c2dd13f7a` |
| proofId | `proof3:d494f00867e8ad48fdf6b21dd7a5ce92381c4f83ce8c0f251b733eb970927c86` |
| evidenceId | `evidence3:9f81be77bb65675bfc80220b2844e1bb555556a6f2bcbfef312280f24abfd07a` |
| sealId | `seal3:344a745261264ee918d9ab17a71894f19e02fc2e824ac19be1075f4b77425ab7` |
| importId | `import2:86b1b376eafc5832422721f095788bdc6980682380fd563268141f3a3a9298f1` |
| verdict | pass |

Old→new store `ca1b44df…` → `59b7d384…`. Old run `run3:9fb05cf2…` → `run3:8170fc2c…`.

## Smallest useful discriminating graph

Retained admitted facts, not invented edges. Projectable rung is `imports@resolved-target` with TargetAttributionV1, consistent with the existing TS imports witness (bare specifier `left-pad`, `node_modules`, ScopeDocumentV1, import payload).

| Fact | Payload | Attribution |
|---|---|---|
| `fact2:ddc3eeb9…` | `module:src/app.ts` → `file:src/index.ts` (`./index`) | `c296b9c2…` kind=file occupancy=external |
| `fact2:a5570c5e…` | `module:src/index.ts` → `file:node_modules/left-pad/index.js` (`left-pad`) | `32e786be…` kind=file occupancy=external |
| `fact2:53b10ce1…` | `file:src/index.ts` → left-pad **without** attribution | stored; omitted at projection |

Imports Coverage `coverage2:5d75f248…` is complete over three importer subjects. Isolated symbol inventory vertices `variable:app` and `variable:n` have no incident projected imports. File@enumerated Coverage is complete over all seven snapshot paths.

Machine map: `query-run-graph-inventory.json`. Frozen `query/` files were not rewritten.

## Structural / semantic status

- Stock schema checks: all `stockOk`.
- Structural admission: **pass**, 89 joins, 0 failures. Previously unchecked file@enumerated snapshot totality, complete file-inventory extent equality, imports anchor/SubjectIdV1, and TargetAttributionV1 joins were admitted rather than waived by old passing labels.
- Semantic replay: complete expected proof from admitted inputs; C equal; derived verdict pass.
- Tamper: replacement graph admitted then semantically refused.
- If structural admission had refused, replay would be notReached and this verdict would be `QUERY_RUN_INCOMPLETE`.

## Frozen (unchanged)

| Store | SHA-256 |
|---|---|
| syntax-code.store.json | `0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36` |
| rust.store.json | `3b4daf1caa81f11cbaa255feede860c27fc81dd27b92e1f31cb9de634570d791` |
| syntax-data.store.json | `00fce98f9683084563b1bf54e1119813fc97d670250e49fd7d56ad5fe57e5099` |
| rust-partial-clones.store.json | `89fd6accbc6181217e6605fbc6b4a058520b7ae8ce0cda3523f4a0a86b1a004c` |

Foundation 25 artifacts and 88 workflow/scope files plus 21 four-run sidecars: byte-identical.

## Limitations

- Query cases were not executed. Do not treat graph support as `graph.neighbors` / `path` / `reach` results, historical pagination, bound truncation, failure envelopes, or human/JSON/agent parity.
- Selected file evaluation subjects remain `{src/index.ts}` so the existing `file-present` none-atom stays false. `src/app.ts` is in the snapshot, membership, file/clones facts, and symbol inventory.
- Attribution occupancy is external: payload `file:path` SubjectIdV1 cannot equal inventory LogicalPath without parsing the namespace, which the join law forbids.
- This origin’s `close_run` exhibition is `close_execution_and_proof` plus `replay_from_export` over exported bytes.

## Missing or contradictory norms (not existing-law mistakes)

1. **SubjectIdV1 vs file inventory nativeSubjectId.** Imports `resolvedTarget` is `file:src/index.ts`; file inventory native id is `src/index.ts`. First-party occupancy cannot match without namespace parsing.
2. **TargetAttributionV1 draft standing.** The schema is DRAFT pending root ProofInputRef integration, but `execution-inputs.schema.v1.json` already names domain `target-attribution`. Records are retained as that blob domain.

Existing-law corrections this pass: file facts for every snapshot path; TargetAttributionV1 on the two projectable imports; symbol importers on those facts.
