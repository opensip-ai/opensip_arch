# Blind review — consumer-b.v24, source42 (runtime consumer-b.v24-source42.v3)

**Verdict: ACCEPT-RECONSTRUCTABLE** (`blind-review.json#/verdict`, derived by `tools/finalize_review.py` from measured standing).

- **Standing.** This continues my original blind origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514 over the source42 normative kit. Fresh-origin independence is not claimed anew.
- **Runtimes.**
  - `consumer-b.v24-source42.v1`: incomplete, no review; preserved.
  - `consumer-b.v24-source42.v2`: completed the review; preserved in place, and this runtime did not write it.
  - This runtime, `consumer-b.v24-source42.v3`: finishes the same charter's provider-trace payload obligation. My v2 review had mislabelled that obligation (below).
- **Own history.** My earlier consumer-b.v24, source39.v1–v3 and source41.v1 results are preserved read-only and establish nothing about this kit.
- **This review corrects two of my own earlier results:**
  - the source41 exports' helper omission (HC-47);
  - the source42.v2 provider traces, which executed no payload law while R-TRACE-* stood executed (HC-53).
- **Claims.** This review makes no product qualification claim, grants no implementation authorization, and implies no acceptance by any root or owner.
- **Root admission.** External root admission of the exported bytes is a separate gate; its outcome is unobserved here.
- **Future qualification.** Real OS/compiler/crypto/SQLite measurement, provider execution as enforcement proof, host authentication and synthetic TCB enforcement (`F-OS-COMPILER-CRYPTO-SQLITE`, `F-SYNTHETIC-TCB`, `F-AUTH-HOST`) are unperformed and not counted as design omissions.

## This runtime: the provider-trace payload obligation

### The obligation and the reconciliation

- **The obligation.** The charter's "Current incorporated correction owners" (line 248) says: *"When reconstructing the existing provider traces, apply the current negotiated payload selection, exact payload-byte representation and request/batch correlation law."* It belongs to R-TRACE-*.
- **What my v2 output actually did** (bytes preserved at `preserved/s42-v2-final/`):
  - every trace negotiated `target-attribution-v2`, but every `FactBatch` was a frame name with no payload;
  - payload schema validation was listed as a future-host item;
  - the review called FactBatchV3 companions "read but not exercised".
- **Consequence.** Those traces are exact transition evidence only. The v2 R-TRACE-* standing rested on them, so that statement is withdrawn (`blind-review.json#/priorIssueDisposition`).
- **Existing artifacts.** No complete Run retains FactBatch frames, so no existing artifact executed this law, and none is cited as payload evidence.

### What is now executed

`ref/factbatch.py` is new code, built from the kit only. It reconstructs the host ANALYZING entry `buffer_fact_batch_occupancy`, whose parameters include no receipts or views. `vectors/phase3_payload_vectors.py` and the reworked `vectors/phase3_traces.py` execute it (`logs/s42v3-p3b.0`, `.1`: 0 assertion failures). Owners and the full vector list are in `notes/11-provider-trace-payload-law.md`.

**Negotiated vs unnegotiated payloads.** FactBatchV3 is selected iff the token is on both Hello and HelloAck; otherwise historical FactBatchV2 is selected.

| Case (TypeScript and Rust) | Result |
|---|---|
| Token on both, FactBatchV3 | admitted; companions buffered |
| Token on both, empty companions | admitted |
| Token absent, FactBatchV2 | admitted; occupancy omitted; nothing buffered |
| Token absent, FactBatchV3 (or V2 plus `schemaVersion`) | `PROVIDER_RETURN_UNNEGOTIATED_V3` |
| Token on both, FactBatchV2 | `PROVIDER_RETURN_SCHEMA` (V3 required members absent) |
| TypeScript token absent, delivery.v2 FactBatchV1 shape `{facts, batchCommitment}` | `cb24.FACT_BATCH_V2_SCHEMA` (A-s42v3-1) |
| Token on Hello only, or HelloAck only | exchange faults at HelloAck (s9.1 exact echo); no payload version selected, no source byte sent |
| Token on neither | `identityNegotiated` true; the token is not an identity token |

**Exact payload bytes.**
- **Encoder and decoder.** A restricted deterministic-CBOR encoder and decoder are built from fact-plane `canonicalPayloadEncoding`. Every one of its 8 forbidden items has a refusing vector (29 decoder and 10 encoder vectors).
- **Kit cross-check.** Both kit fact-plane vectors re-encode byte-equal and decode equal, and hand-assembled bytes equal the encoder.
- **Admission rule.** Hex transcribes bytes → decode once → decoded equals `decodedRelationPayload` → `deterministic_cbor(decodedRelationPayload) == bytes` → closed relation payload schema.
- **Refused `PROVIDER_RETURN_PAYLOAD_CBOR`:**
  - hex of canonical JSON UTF-8;
  - alphabetical rather than encoded-key order;
  - non-shortest length header;
  - indefinite-length map;
  - one trailing byte;
  - lawful CBOR of a different payload.
- **Discriminating cases:**
  - uppercase hex of the exact bytes refuses only at the schema pattern;
  - byte-exact CBOR carrying an unknown field refuses `FACT_RELATION_PAYLOAD_INVALID`;
  - a missing rung-required field refuses `FACT_RELATION_PAYLOAD_INVALID`, and the masked `TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH` stays listed.

**Request/batch correlation.** `DispatchBindingV1` is derived from the current Analyze stage request (TS `StageRequestV1.stageId`; Rust `StageRequestV2.planStage.stageId`) and a retained Plan fragment, and is admitted against its schema.
- **Positives:**
  - the TypeScript Analyze selects Plan stages 1 and 3 as request ordinals 0 and 1;
  - dispatch (retained 3, request 1) admits;
  - the two batches of one stage correlate at (retained 1, request 0, batch 0, first 0) and (1, 0, 1, 3).
- **`stageId` negatives** — all refuse `PROVIDER_RETURN_STAGE_ID`:
  - `stageId` `"1"` (request ordinal as text);
  - `"3"` (retained ordinal as text);
  - another requested stage;
  - Rust `"0"`;
  - an integer `stageId`, which refuses `PROVIDER_RETURN_SCHEMA` first.
- **Batch negatives:**
  - `analysisOrdinal` mismatch;
  - `batchIndex` gap or replay;
  - candidate stream restarting at 0 or skipping.
  An internal gap is lawful at the order token but refuses `PROVIDER_RETURN_CANDIDATE_STREAM`. Duplicate or reversed ordinals refuse at the schema.
- **Host-internal refusals** — routed to `SYSTEM.OUTCOME.ILLEGAL_STATE`:
  - omitted dispatch (`PROVIDER_RETURN_DISPATCH`);
  - `retainedStageOrdinal` equated with `analyzeRequestOrdinal` (`PROVIDER_RETURN_STAGE_SPEC`);
  - extra dispatch member;
  - plan mismatch;
  - a producer that is not the stage's producer;
  - dispatch derived for another request.
- **Limit.** 4097 candidates refuse at `maxItems`.
- **Explanatory.** An integer lookup of `batch.stageId` raises `ValueError`, and looking up by request ordinal selects the wrong stage.

**Companions.**
- **Admitted:**
  - a partial set with a gap;
  - symbol, file-external and package-first-party companions;
  - an all-null package-unknown companion.
- **Refused on joins:**
  - unknown or prior-batch ordinal (`PROVIDER_RETURN_UNKNOWN_CANDIDATE`; atomic, nothing buffered);
  - target universe not byte-equal;
  - `targetNativeId` differing from the decoded payload field, including the inventory spelling;
  - companions on syntactic imports and calls rungs.
- **Refused at the schema** (16 cases):
  - `planId`, `sourceFactId` and `producerClosure` members;
  - every tested allOf branch;
  - a dot-dot LogicalPath;
  - reversed or duplicate order.
- **Totals.** 71 standalone vectors (13 selection, 9 bytes, 23 correlation, 26 companions), all matching their pre-derived expectations.

**In the traces.**
- **Payloads.** Every FactBatch carries a payload. The entry runs at each FactBatch that reaches ANALYZING, over 25 traces with all 34 rows exercised and pairwise disjoint. Of 21 payloads:
  - 19 were validated: 13 V3 and 1 V2 admitted, 5 refused;
  - 2 were never validated, because the table faults first (WAIT_CANCELLED; post-terminal).
- **Added traces:**
  - negotiated multi-batch Analyze subset;
  - unnegotiated V2;
  - HelloAck omitting the token;
  - V3 without the token;
  - V2 with the token;
  - `stageId` echoing the request ordinal;
  - candidate stream restarting;
  - canonical JSON hex.
- **Refused payloads.** Each refused payload faults the exchange as `payload:fact-batch-refused(KEY)`. Its public route (`input-*-invalid:provider-return` → operational-failed `PROVIDER.PROTOCOL_VIOLATION`) is checked equal to the s10 fault projection.
- **TypeScript exchanges.** They now use TypeScript caps and major 2 (A-s42v3-1).

**Standing of these results.**
- **Executed.** These are executed schema, byte and join checks on constructed payloads. They are not future-host items merely because no worker process is spawned.
- **Not claimed:**
  - actual worker-process enforcement;
  - OS, provider or compiler qualification.
- **Key binding.** Every internal key is labelled `kit-text` (4), `key-name` (12) or `cb24` (3) in `traces/payload-vectors.json#/keyBindings`. The check order is my own, and every check runs.

### Helper corrections made in this runtime

| HC | What | Selector | Original failure (preserved) |
|---|---|---|---|
| HC-51 | `ref/schemas.py` knew only the identity s3 order tokens and refused every lawful FactBatchV3 with `ORDER_ANNOTATION_UNKNOWN`. `PayloadKit` adds exactly the published `candidateOrdinal` token; `ref/schemas.py` is byte-unchanged. A census finds the token only in `fact-batch.schema.v3.json`, so no earlier result is affected. | `occupancy-companion.schema.v1.json#/x-opensip-order-vocabulary/candidateOrdinal` | `traces/payload-vectors.json#/hc51`: the unchanged Kit refuses all 40 batches the token admits |
| HC-52 | Runtime adaptation: rebinding (100 files, 120 occurrences), v2 final bytes of changed files preserved, runtime labels | — | `rebind-v3-manifest.json`, `preserved/s42-v2-final/manifest.json` |
| HC-53 | Phase-3 traces omitted the charter-incorporated FactBatch payload law (above) | charter line 248; native s9.1, s9.6; FactBatchV3, DispatchBindingV1, OccupancyCompanionV1; fact-plane `canonicalPayloadEncoding` | `preserved/s42-v2-final/vectors/phase3_traces.py` and `traces/*.json`; first-run own construction errors `logs/s42v3-p3.0` (IndexError) and `logs/s42v3-p3.1` (TypeScript major 2 sent to HelloV3) |

### Reused versus executed here

- **Executed fresh in v3** (`logs/s42v3-*`):
  - the payload vectors and payload-carrying traces;
  - phase 0 custody and checkpoints 0–3;
  - final custody (twice: before phase 10 and before phase 11);
  - phases 10 and 11.
- **Reused unchanged from v2.** No input or helper they execute changed: `ref/schemas.py` and `ref/protocol3.py` are byte-unchanged, and the new code is in new files. The reused results are:
  - builds and stores;
  - the 27 exported positives and their run ids;
  - from-scratch closure, export replay and the admission log;
  - mutation replay, tamper and retention negatives;
  - the pre/post matrix and provenance;
  - phases 4–9 vectors and checkpoints 4–9.
  They are cited below with their original v1/v2 log labels. No complete Run was rerun.

## Why the verdict is ACCEPT-RECONSTRUCTABLE

Every charter condition was evaluated on executed results, not counts:

- **Requirements.** All 123 requirements and 8 standing rules are executed; none failed and none is unexecuted (`requirement-status.json`; checkpoints 0–11 with unioned ID sets). R-TRACE-* now rest on the payload-carrying traces and vectors as well as the transitions. The 3 future-qualification items are recorded as not demanded.
- **Positives.** All 27 claimed complete positives were (v2 measurements, reused):
  - validated against their owning schemas, including the published kit keywords;
  - admitted by owner graph admission with every cross-record join;
  - closed by the independent retained-closure walker;
  - replayed from the exported store with byte-equal proofs and reachable output-set equality;
  - exported with complete object tables and every blob keyed by digest.
- **Negatives and controls.**
  - The designed negative refuses.
  - All 32 retention/reference-class negatives pass.
  - All nine closure controls refuse on their own laws.
  - The provider-trace payload law ran with 0 assertion failures.
- **Kit custody** is PASS at phase 0 and again at the end, in this runtime.
- **No new MUST or SHOULD issue** is supported by the source42 text. The TypeScript major-2 wire publication gap is advisory: the current s9.1 text determines the result.
- **No open helper failure.** Every helper defect found (HC-47..HC-53) had a precise kit or own-tool answer. Each was corrected with its original failure preserved. Every current-source-dependent result was re-executed after the last change to the code it uses.

## Input custody

- **Kit.** `subject/consumer-input-manifest.json` SHA-256 `9c90a1e849b1a33fb1aec507d6a4f59632fc3497922c99de847e4802fb89db05`, parent frozen manifest `f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307`, 104 members. Every member's SHA-256 and length verified; no unlisted file; rows identical to phase 0 (`vectors/phase0-custody.json`).
- **Re-verified at the end** (`runs/final-custody.json`: PASS). Charter SHA-256 is `ac6d2e4e…` and requirements SHA-256 is `e3c33234…`. Both equal the v2 runtime's apart from the root-relocated runtime path; the 123/8/3 IDs are unchanged.
- **Kit delta.** Against my own source41 custody rows, exactly two documents changed, both read in full: `foundation/enumeration-contract.v1.md` and `foundation/execution-inputs-contract.v1.md`.

## Continuation record for v2 (history)

- **v1 → v2.** v2 verified its copy equal to the v1 output (4566 files) and rebound it before execution (`rebind-v2-manifest.json`).
- **Executed fresh in v2** (`logs/s42v2-*`):
  - HC-50 control rebuild;
  - replay of all 71 stores;
  - from-scratch closure;
  - export replay and admission log;
  - pre/post matrix and provenance;
  - custody;
  - phases 1–3 vectors (transition-only; superseded by v3);
  - checkpoints.
- **Reused in v2 as exact v1 measurements** (logs `s42-original*`, `s42-fin-*`):
  - builds;
  - tamper;
  - discovery and mode vectors;
  - phases 4–8 vectors;
  - graph query and run termination;
  - retention negatives.
- **Own execution error in v2, preserved.** `logs/s42v2-fin2.7.final_custody.log` failed because final custody ran before phase 0; it was re-run successfully (`logs/s42v2-cp.5`).

## How the reconstruction was carried out

1. **Port.** My own source41 helpers were ported with only the runtime root rebound (`port-manifest.json`).
2. **Unchanged run first.** They ran unchanged against source42 (`logs/s42-original*`), and the output tree was preserved byte-for-byte (`preserved/s42-original-state/`) before any change. That state is re-executable at `preserved/pre-s42/`.
3. **Correct from the kit.** Helpers were corrected only from the kit (`tools/hc_source42.py`; HC-51..HC-53 above):

| HC | What was wrong | Source42 selector | Original failure (preserved) |
|---|---|---|---|
| HC-47 | Enumeration bindings put the U-1 marker into `programEntry` on `default-unit` bindings (`tsconfig.json`, `Cargo.toml`) and labelled the U-9 syntax default `explicit-plan-selection`. Admission had no null rule, no derived-entry join against the retained `entryConfigPath`, no explicit-entry join and no default-unit cardinality check. | `enumeration-contract.v1.md` s1 lines 20-47; `enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/programEntry/description` (unchanged since source41) | `logs/s42-original.7.from_scratch.log`: all 27 admit; the rebuilt stores have run ids identical to my 27 source41 exports |
| HC-48 | View-attribution candidates were also drawn from the claimed `selectedRefs`; a `selectedRefs` view on no complete receipt was not refused `EXECUTION_INPUTS_SELECTED_COVER` | `execution-inputs-contract.v1.md` s3 line 53 | unchanged code refuses that control only as `EXECUTION_INPUTS_REF_POINTER` |
| HC-49 | Runtime adaptations: a discovery vector path to the source41 layout; the negatives' pre column; custody hashes; s42 pre/post and provenance tools; the v2 root rebinding | — | `logs/s42-original-disc.0.discovery_vectors.log` (FileNotFoundError) |
| HC-50 | Own control error: the first second-default-binding control lacked a stage observation and was refused by a schema fault of my own capture, masking the law under test | own tool | `logs/s42-fin-mut.0.replay_all.log` |

## Own source41 defect, measured

- **What the unchanged run shows.** The unchanged helpers rebuild all 27 positives with the run ids of my source41 exports and admit them. Their retained enumeration plans carry `programEntry: "tsconfig.json"` (17 ts-/cmp-* Runs) and `programEntry: "Cargo.toml"` (6 rust-* Runs) on `default-unit` bindings.
- **What the corrected code does with those exact original bytes** (`selfcheck/s42-prepost-matrix.json`): it refuses the 23 TS/cmp/Rust positives `ENUMERATION_BINDING_PROGRAM_ENTRY:…:default-unit-non-null` and admits the 4 syntax positives. Their `explicit-plan-selection` spelling is unrefused by any published rule (advisory A-s42-3).
- **Rebuilt positives.** They carry `programEntry: null` on default bindings and a `default-unit` U-9 binding. Both codes admit all 27, and every identity changed.

## Claimed complete positives and exact exports

These are unchanged from source42.v2: byte-identical copies, not rebuilt in v3. Each export is `runs/<run>.store.json` (object table plus every blob). Each Run also has a from-scratch closure (`runs/<run>.replay.fromscratch.json`), an export replay (`runs/<run>.replay-export.json`) and an admission log (`runs/<run>.records.json`).

| Run | runId |
|---|---|
| cmp-base | `run3:88d6ffc50e2a8d517717056b7c0ccfa3c072be624f6919b733b17514fb987e54` |
| cmp-budget | `run3:75ec6326c6d05a14b38c353d1f777f30a241ad4063f8343e044ddcce914bc32b` |
| cmp-code-det2 | `run3:7a497d82a68ba4e0d00a4d3adcb0f13a7cd9ce649290afc2923113c65386519d` |
| cmp-code-detc | `run3:fea6a4a34d5db63516c21d76b01d42104d694c416b704b83ca06da24168d8ace` |
| cmp-code | `run3:a3bfb0189bb733319998b7e73b591c224af02ab5590807be1f77dc65eea621ee` |
| cmp-empty | `run3:30fa2312888fb3f713f93c16d9d738ceab9f783b1f70cb90ca08887c78aea57c` |
| cmp-evidence | `run3:246a66a78dd5ae2295ca9acddd47da72e8a440597da15db82c45991ba84ff455` |
| cmp-gbase | `run3:aa2f9d693435f628c7a78954caadd4c29555c098b147b0a84b658e00c76b2855` |
| cmp-gevidence | `run3:38035e4aa373bf5d28c6d2c4d09d3fed5504f8e79fb26a5a9292716d802db796` |
| cmp-gmissing | `run3:f835ecc0f6d25ffced088711d86fbf7a79ef1eeca587a9037c52d3e0cb914737` |
| cmp-hidden | `run3:e6fa7975683e9fc3f1ec01cc5cfd4104151d24c3a7a3de4862bbb0d2486614ef` |
| cmp-policy | `run3:593cad18396ebc40f76f84eefb3d3703d8b381ff8cf0cf82a0cc422db79762e2` |
| cmp-scope | `run3:c279f39f370b7f41dd2bb141b746d45a62d69cef16071c47aa92851a78cf3ec6` |
| cmp-waiver | `run3:326ea9f0dabde3ec9e1e64d9255da463335816d449641ab3f0e4cf810896c96c` |
| rust-ambiguous | `run3:bb9ad3b2ae295becbe0ef721b7db00b8c00e12ba633a1f5493547d49e7f33536` |
| rust-extra-unit | `run3:58b08c269351e27614c2f828172cdbbd304c7ab6e29cdb72a25e23790419407a` |
| rust-mixed-clones-required | `run3:359566e8cc476189d433257117f30edea16cfdbc1863e21b17a8e8df7d32398c` |
| rust-mixed | `run3:0552d2c2279cdf940d5826f8f58bf64d78f63a3014838583b47eec2605aa1db7` |
| rust-partial | `run3:77be524d9da78ecfbb0bc0b643f65ddf3e9b6679b940c7bae7ff9588aef60db3` |
| rust-same-file-2021 | `run3:f0293580d253e8f73221970cfa38d87a7006580ba15fae17522f38aa85ab050b` |
| syntax-code | `run3:fffddf0afc41de4ba5053bc5737bb4c2f2bf7e372174891387b31a8094d03d69` |
| syntax-data | `run3:1113e38c6bbcd36d6c84cfebf59293b4eb667d1360d51bb9e78955563f06197d` |
| syntax-mixed-disclosed | `run3:10132b141bb04b7084879388e02561f51182012b00ab3ab05706162a043b68f3` |
| syntax-mixed-omitted | `run3:e401b7165eae4ca77d3de06731450356f1b919162c91a07d71ae5112af6ba43a` |
| ts-clones-required | `run3:cd4a8fe63d4e0fee7179fc7894bd88d1d323c7b16e1c03fdc53938df1c5ca836` |
| ts-fail | `run3:f94885357fa9eb41d92d061283cd83a6e58f2a26893890a219578fb087db321a` |
| ts-pass | `run3:54a0a7cfba1b7061160c481e51cde4a54bae9c0a50a57e63475d4b4a35a9d2fa` |

The designed negative `syntax-mixed-falsecomplete` refuses `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE` at owner graph admission.

**From-scratch command** (reads only exported stores and the kit, one fresh process per Run):
`cd /private/tmp/opensip-design-corrections/consumer-b.v24-source42.v3/output && /tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py && /tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py`

## Independent vectors and results

| Area | Result | Artifact / log (runtime) |
|---|---|---|
| C/H, CVE1, lexical admission, raw vs parsed, acyclic joins | 0 failures | `vectors/phase1-canonical.json`, `logs/s42v2-cp.1` (v2, reused) |
| capability manifests, four gates | 5 positives, 19 negatives, 0 failures | `logs/s42v2-cp.2` (v2, reused) |
| protocol3 traces with FactBatch payload law | 25 traces; all 34 rows exercised, pairwise disjoint; 21 FactBatch payloads (14 admitted: 13 V3, 1 V2; 5 refused; 2 faulted before payload) | `traces/*.json`, `logs/s42v3-p3b.1` (v3) |
| FactBatch payload/correlation vectors | 71 vectors, 29 decoder, 10 encoder, 4 exchange controls, 3 explanatory, 2 kit cross-checks; 0 failures | `traces/payload-vectors.json`, `logs/s42v3-p3b.0` (v3) |
| relation/rung table, RC-0..RC-6, cell-outcome derivation | 17 rows, 16 RC vectors, 10 outcome vectors, 0 failures | `logs/s42-fin-p4to9.0` (v1) |
| discovery, U-0, U-1/s1.2 modes, U-4b, U-8, U-9 | 29 vectors, 0 failures | `logs/s42-fin-disc.0` (v1) |
| phases 5, 6, 7 and 8 vectors | 0 failures; 45/45 public termination goldens | `logs/s42-fin-p4to9.1`–`.5` (v1) |
| analysis-Run termination | 28 Runs, 9 candidate checks, 30 host compositions, 0 failures | `logs/s42-fin-p4to9.8` (v1) |
| graph query | 53 vectors, 0 failures | `logs/s42-fin-p4to9.6` (v1) |
| from-scratch closure | 27/27 positives admit through all four stages; designed negative refuses | `logs/s42v2-fin2.2` (v2) |
| export replay | 27/27 byte-equal recomputed proofs | `logs/s42v2-fin2.3` (v2) |
| per-record admission log | 27 positives, 0 failures | `logs/s42v2-fin2.4` (v2) |
| mutation replay | 71 stores: 29 admit (27 positives + 2 lawful controls), 42 refuse | `logs/s42v2-fin2.1` (v2) |
| tamper | every semantic control refused by replay; every identity control refused before replay | `logs/s42-fin-tamper.*` (v1) |
| retention/reference-class negatives | 32 constructed, all pass | `logs/s42-fin-neg.0` (v1) |
| unchanged vs corrected helpers | table below | `logs/s42v2-fin2.5` (v2) |

| Control | Unchanged helpers | Corrected helpers |
|---|---|---|
| `ts-pass~default-unit-program-entry` | admitted | `ENUMERATION_BINDING_PROGRAM_ENTRY:0:0:default-unit-non-null` |
| `rust-mixed~default-unit-program-entry` | admitted | `ENUMERATION_BINDING_PROGRAM_ENTRY:0:0:default-unit-non-null` |
| `ts-pass~explicit-entry-not-graph-entry` | admitted | `ENUMERATION_BINDING_PROGRAM_ENTRY:0:0:explicit-entry` |
| `syntax-code~second-default-unit-binding` | `ENUMERATION_INVENTORY_MISSING_RECORD` | `cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY:0` |
| `syntax-code~selected-view-not-on-receipt` | `EXECUTION_INPUTS_REF_POINTER` | `EXECUTION_INPUTS_SELECTED_COVER:view-not-on-receipt` |
| `syntax-code~unit-kind-other-family`, `~unit-root-external-sentinel`, `~row-view-omitted`, `ts-pass~unit-kind-not-mode-projection` | refused (source41 laws already corrected) | refused on the same laws |
| lawful FactBatchV3 (40 vector payloads) | `ORDER_ANNOTATION_UNKNOWN` (HC-51) | admitted by the published `candidateOrdinal` token |

## Issues

### newMustIssues

None.

### newShouldIssues

None.

### Disposition of my own earlier results

- **The source41 claimed positives and their ACCEPT recommendation are superseded** by an own helper omission (HC-47, measured above). This is not a kit gap: the schema description has stated the law since source41.
- **Source41 view attribution (HC-42)** is tightened by the source42 text (HC-48).
- **My source42.v2 provider-trace limitation is withdrawn as inaccurate (HC-53).** The v2 R-TRACE-* standing rested on transition-only traces; the payload law is now executed. This is not a kit gap.
- **Source41 advisories** are carried below; their owner documents are unchanged.

### Advisories (nonblocking)

- **A-c1.** Internal refusal names no kit owner publishes are still spelled `cb24.*`; `blind-review.json#/advisories` lists the measured set.
- **A-c2.** The inherited `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination. The successor D9 artifact is a disclosed live obligation (native lines 3313-3327).
- **A-c3.** Exact-snapshot import correspondence changes `import2` on every source change (workflows s3 lines 440-449).
- **A-n1.** In the closed per-entry IndeterminateReason order, reason (3) is unreachable for entries (workflows s3 lines 402-411).
- **A-n6.** A rust unit's `languageMode` is decided by the mode table but not restated by U-4b.2 and not enforced by U-4b.5 (native lines 165-172, 741-746, 797-799, 1070-1072, 1842-1847).
- **A-v2-1.** Composition s7 does not scope typed-prefix closure explicitly to outputs (s7 line 74; s5 line 54; identity lines 597-600, 627-631).
- **A-v2-2.** `policy-derivation3` is outside the reachable output set (composition s7 lines 70, 76).
- **A-v2-3.** Identity s3 (lines 441-467) calls its digest vocabularies closed while the native and relation bundles publish their own.
- **A-s41-1.** run-termination s7.6 step 1 (line 330) names no key; the s6 key (line 173) is applied at both boundaries.
- **A-s41-2.** U-1's "an omitted value defaults to false" (native lines 656-659) reads against s1.2's `checkJs` fallback (lines 524-526, 562-563); s1.2 is applied.
- **A-s42-1.** Enumeration contract s1 line 21 makes `default-unit` at most one binding per cell at ordinal 0 but names no refusal key; the reconstruction uses its own `cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY` (`runs/syntax-code~second-default-unit-binding`).
- **A-s42-2.** The contract names `ENUMERATION_BINDING_PROGRAM_ENTRY` for a non-null default `programEntry` (lines 26, 37) but not for a derived-entry or explicit-entry mismatch against the retained `entryConfigPath`. Native U-0 (line 650) attributes that join to the same key, which is applied to all three (`runs/ts-pass~explicit-entry-not-graph-entry`).
- **A-s42-3.** Lines 21-22 make a sole syntax-only binding `default-unit`, but no published rule or key refuses the `explicit-plan-selection` spelling with `programEntry: null`, and the two spellings mint different enumeration-plan digests.
  - Measured: the 4 original syntax positives with the explicit spelling admit under the corrected code, with identities different from the rebuilt `default-unit` ones.
  - Determinate by text, unenforced; no refusal is invented.
- **A-s42v3-1 (new).** TypeScript major 2 is published only as deltas (native s9.4) over the delivery.v2 major-1 wire, which leaves two gaps:
  - **Unnegotiated FactBatch payload.** s9.1 (lines 2785-2791) names it "historical FactBatchV2" for both majors. The only published FactBatchV2 closed list is Rust's (rust-provider-protocol.v2 line 411). delivery.v2 still publishes TypeScript FactBatchV1 `{facts, batchCommitment}` (lines 855, 874), and native s0's superseded-selector table (lines 114-116) does not list it.
  - **Hello schema.** No TypeScript major-2 Hello/HelloAck schema exists; HelloV3 fixes `protocolMajor` 3 (native-evidence.schemas.v2.json line 4035).

  The current s9.1 sentence and the FactBatchV3 schema determine the result:
  - a TypeScript FactBatchV1-shaped unnegotiated payload refuses (`traces/payload-vectors.json#SEL-ts-unnegotiated-delivery-v2-FactBatchV1-shape`); its member set equals FactBatchV1's, so the alternative reading would admit it;
  - TypeScript Hello payloads are admitted on the shared HelloV3 members with `protocolMajor` substituted (`traces/controls.json#/helloSchemas`).

## What required invention

No record, identity or refusal outcome had to be invented. Named readings, each measured or stated beside its alternative:
- A-s42-1: a key for the cardinality refusal;
- A-s42-2: one key for all three entry joins;
- A-s42-3: `default-unit` for the sole syntax binding;
- A-s42v3-1: FactBatchV2 for TypeScript unnegotiated payloads; shared HelloV3 members for TypeScript Hello;
- the payload-law check order (mine; every check runs) and its internal keys:
  - labelled `kit-text`, `key-name` or `cb24`;
  - where the kit binds no key to a check, only the public route (`PROVIDER.PROTOCOL_VIOLATION` or `SYSTEM.OUTCOME.ILLEGAL_STATE`) is kit-determined;
- carried: A-s41-1, A-s41-2, A-v2-1, A-n6.

## Limitations

- run-termination s7.5 row 2 and s5 stage-terminal carriers are exercised by vectors, not on built Runs.
- The retained-closure walker names what it delegates to owner graph admission, which runs as its own stage.
- The census pairs `canonical-record/owner-retained`, `raw-artifact/owner-retained` and `snapshot-path/not-joined` occur in no constructed positive and have no negative.
- No positive uses an explicit-plan-selection binding, a js-synthesized or jsconfig default binding, or a Rust explicit binding. Those `programEntry` branches are exercised only by the explicit-entry control and by reading.
- **Provider-trace payload law scope.**
  - It is executed on constructed trace and vector payloads, not on built Runs, which retain no FactBatch frames.
  - The retained Plan fragment is a host observation, not an admitted ExecutionPlan.
  - Not constructed by these vectors:
    - post-terminal `bind_worker_occupancy` (fact2 minting, native views, stageReceipts, TargetAttributionV2 projection and capture, C15);
    - payload bodies of other frames;
    - anchor admission of the constructed candidates.
  - No actual worker-process enforcement is claimed.
- **Not constructed by any original requirement; read but not exercised:** PolicyTestSuiteV2 and the U-8 boundary-inventory superset join.
- `discovery-defaults.py` was neither read nor used.
- Root admission of the exported bytes is unobserved.
- **Product qualification.** This review makes no product qualification claim and no implementation authorization; all future-qualification items remain unperformed.

## Retained outputs

- **Machine-readable review:** `blind-review.json`. It holds the verdict basis, issues, advisories with selectors and measurements, dispositions, HC records, `source42v3Continuation` (payload-law summary, reused vs executed), positives with run ids, and `requirementStatus`.
- **Checkpoints and status:** `checkpoints/phase-0.json` … `phase-11.json`; `requirement-status.json`.
- **Notes:**
  - `notes/00-session-standing.md` (v2 and v3 continuation records);
  - `notes/01-source42-law-deltas.md`;
  - `notes/07-phase7-reconstruction.md`;
  - `notes/08-subsystem-owners.md`;
  - `notes/09-reconstruction.md`;
  - `notes/10-gaps.md`;
  - `notes/11-provider-trace-payload-law.md`.
- **Code:** `ref/` (new: `ref/factbatch.py`), `builders/`, `tools/`, `vectors/` (new: `vectors/payload_fixtures.py`, `vectors/phase3_payload_vectors.py`).
- **Results and logs:** `runs/`, `envelopes/`, `traces/` (new: `traces/payload-vectors.json`), `negatives/`, `selfcheck/`, `logs/`.
- **Own history:**
  - `preserved/` (new: `preserved/s42-v2-final/` with manifest);
  - the preserved source42.v1 and v2 runtimes in place.
