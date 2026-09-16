# Source43 kit delta: the query projection contract (runtime source43.v1)

## Custody and delta

- **Kit.** `subject/consumer-input-manifest.json` SHA-256 `6d8912f4a78d65946f09047254978570974328ae4d7d883d453f8855347f1beb`, parent `db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d`. All 104 members verified; no unlisted file (`s43-kit-delta.json`, `vectors/phase0-custody.json`, `runs/final-custody.json`).
- **Delta against my own source42 custody rows** (`preserved/s42-v3-final/vectors/phase0-custody.json`): exactly one member changed, none added or removed.
  - `docs/coop/design-corrections/workflows/query-projection-contract.v3.md`: 29699 bytes (SHA-256 `923ff32f…`) → 30278 bytes (`47ccc81c…`).
  - The source42 bytes are **not in my custody** (only their hash). The delta was therefore not diffed. Every law of the current text was re-audited against my helper.
- **Which of my constructions the delta can affect** (`selfcheck/s43-provenance.json`):
  - The only helper that reads the changed member's bytes is `tools/phase9_graph_query.py` (R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR).
  - `ref/schemas.py` loads kit JSON documents only.
  - The only other helper reading kit prose is phase 0 custody, which reads the unchanged five-contract index README.
  - Retained stores are byte-identical to my source42.v3 exports (104/104).
  - Helper bytes are the source42.v3 bytes after the runtime-root rebind only, except the files edited here.
- **My own tool error, preserved.** The first provenance census (`logs/s43-prov.0`) counted every textual mention of the path as a reader, and `charter.md` as kit prose. The corrected census tracks the path variables that actually reach `open()`.

## Law-by-law re-audit (`vectors/graph-query.json#/source43ReAudit/lawAudit`)

| Selector | Law | Unchanged helper | Source43 vectors |
|---|---|---|---|
| s1 | selection by runId / snapshotId / latest; fact-view set | implemented | existing selection vectors |
| s2 step 1 | schema-first; `package` endpoint without `packageManifestPath` → `QUERY.PARAMS_MALFORMED` | implemented | `package-endpoint-without-manifest-path` |
| s2 step 2 | `QUERY.ENDPOINT_AMBIGUOUS` only for two vertex records of one complete tuple; unreachable through the wrapper | implicit | `endpoint-duplicate-vertex-records-refused` |
| s3 | projection table, occupancy, public order | implemented | existing neighbors vectors |
| s4 graph.path row | `edges[i]` is the walked hop `nodes[i]→nodes[i+1]`; may reverse the stored fact under incoming/both; neighbors keep stored orientation | **omitted** (stored orientation) | `path-incoming-edges-report-traversal-hop`, `path-both-edges-report-traversal-hop` |
| s4 walk | FIFO BFS, fact2 order, cap before entry, depth, reach prefix, path witness stop | implemented | existing path/reach vectors |
| s5, s6 | cursor/bounds; disclosure | implemented | existing |
| s7 availability | closed `{retained, partial, purged, expired, corrupt, unavailable, missing}`; `missing` → `evidence.missing`; null / wrong type / unknown → `ReferenceCallPrecondition` host.availability, after request admission | **omitted** (treated as a grant) | `availability-missing-direct-host-report`, 4 precondition vectors, `availability-out-of-vocabulary-after-malformed-request` |
| s7 host adapter | adapter's own out-of-vocabulary observation with a valid RequestId → `SYSTEM.OUTCOME.ILLEGAL_STATE` / `HOST.INVARIANT_VIOLATED`, subject `host.availability`; without a valid RequestId it stays a precondition | **omitted** | `adapter-out-of-vocabulary-observation-host-invariant`, `adapter-without-valid-request-id-stays-precondition` |
| s7 retained record | record failing identity availability admission or naming another Run → `evidence.corrupt`; an admitted record supplies its state | **omitted** | 5 `retained-availability-record-*` vectors |
| s7 close_run | four typed outcomes (EvidenceUnavailable → missing; CompleteReplayMismatch → `evidence.regeneration-mismatch`, subject RunId; other admission → corrupt; other exception → `HOST.INVARIANT_VIOLATED`, subject close_run), never selected by message text | **omitted** (message substring; mismatch reported corrupt; exceptions uncaught) | `close-run-complete-replay-mismatch-regeneration`, `close-run-non-typed-exception-host-invariant`, 8 typed-outcome controls |
| s7 remedies | loss and retained-regeneration carriers verbatim (evaluator-fault-contract.v3 line 98) | **omitted** (own text) | the missing and regeneration vectors assert the route remedy |

## Measurements

- **Unchanged helper on the source43 kit:** `logs/s43-original.0.phase9_graph_query.log`, 53 own vectors, 0 failures. Its own vectors did not discriminate the omitted laws.
- **Corrected helper:** `logs/s43-hc54c.0.phase9_graph_query.log` has 66 vectors (31 valid, 34 invalid, 1 explanatory) and 0 assertion failures. Beyond those it adds:
  - 13 new vectors;
  - 5 precondition vectors;
  - 8 typed-outcome controls;
  - 1 endpoint control.
- **Regeneration-mismatch store.** It was built with my own `tools/tamper_outputs.py` remint: the verdict flipped and every enclosing identity was re-minted. Owner admission and the retained closure admitted it, and replay refused `SEMANTIC_REPLAY_PROOF_MISMATCH:$.verdict`. The query routes it `HOST.IO_FAILURE` / `evidence.regeneration-mismatch` with the RunId as subject. The unchanged helper reported `evidence.corrupt`.
- **Pre/post** (`#/source43ReAudit/prePost`). Each helper's `execute` ran on identical inputs through one summary. Every source43 vector differs from the unchanged helper except two agreement controls: `availability-retained-observed` and `availability-out-of-vocabulary-after-malformed-request`. For the latter, both refuse `QUERY.PARAMS_MALFORMED`, because request admission precedes observation consumption.
- **My own tool errors, preserved:**
  - `logs/s43-hc54.0` asserted that every vector differs, including an agreement control;
  - `logs/s43-hc54b.0` compared asymmetric summaries.

## Standing of my source42.v3 result

- **Byte arithmetic.** The net change is +579 bytes, while the corrected law text is several thousand bytes. So at least part of these laws was already present in the source42 bytes, and my source42.v3 R-GRAPH-QUERY standing rested on a helper that omitted them. It is superseded by HC-54. No other source42.v3 result is affected by the delta.
- **Reading, advisory A-s43-1.** `GraphQueryContextV1.availability` is required, but s7 does not state its value for a successful query with no observation. This is a reference-harness case; a product host always has the current availability record. The reconstruction reports `retained` after `close_run` admits.
