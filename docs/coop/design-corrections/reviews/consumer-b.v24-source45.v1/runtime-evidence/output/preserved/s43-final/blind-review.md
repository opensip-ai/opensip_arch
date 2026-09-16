# Blind review — consumer-b.v24, source43 (runtime consumer-b.v24-source43.v1)

**Verdict: ACCEPT-RECONSTRUCTABLE** (`blind-review.json#/verdict`, derived by `tools/finalize_review.py` from measured standing).

- **Standing.** This continues my original blind origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514 on the source43 normative kit, from the exact source42.v3 output. Fresh-origin independence is not claimed anew. Every earlier runtime and result is preserved.
- **Claims.** This review makes no product qualification claim, grants no implementation authorization, and implies no acceptance by any root or owner.
- **Root admission.** External root admission of the exported bytes is a separate gate; its outcome is unobserved here.
- **Future qualification.** Real OS/compiler/crypto/SQLite measurement, provider execution as enforcement proof, host authentication and synthetic TCB enforcement (`F-OS-COMPILER-CRYPTO-SQLITE`, `F-SYNTHETIC-TCB`, `F-AUTH-HOST`) are unperformed and not counted as design omissions.

## What the source43 kit changes, and what that affects

- **Kit delta.** Against my own source42 custody rows (`preserved/s42-v3-final/vectors/phase0-custody.json`), exactly one of 104 members changed: `docs/coop/design-corrections/workflows/query-projection-contract.v3.md`.
  - Size: 29699 bytes (SHA-256 `923ff32f…`) → 30278 bytes (`47ccc81c…`).
  - No member was added or removed (`s43-kit-delta.json`).
- **Which constructions the bytes can reach** (`selfcheck/s43-provenance.json`).
  - The graph-query reconstruction (`tools/phase9_graph_query.py`, R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR) is the only helper that reads the changed member.
  - The kit loader reads JSON documents only.
  - The only other prose read is phase 0's unchanged five-contract index.
  - Exported stores are byte-identical to source42.v3 (104/104).
  - Helper bytes are the source42.v3 bytes after the runtime-root rebind, except the files edited here.
- **Source42 bytes not in custody.** I hold only the hash of the old contract, so I did not diff it. Instead I re-audited every law of the current text against my helper.

## Graph query re-audit (HC-54)

**Unchanged helper first.** After only the root rebind, it still passes its own 53 vectors on source43 (`logs/s43-original.0`). Those vectors did not test the laws below.

**Laws it omitted** (`vectors/graph-query.json#/source43ReAudit/lawAudit`):

| Contract selector | Law | Unchanged source42.v3 helper |
|---|---|---|
| s4 `graph.path` row | `edges[i]` is the walked hop `nodes[i]→nodes[i+1]`; under `incoming`/`both` it may reverse the stored fact; `factId` still names the stored fact; neighbors keep stored orientation | reported the stored orientation |
| s7 availability observation | closed vocabulary including `missing` (→ `evidence.missing`); a present null, wrong type or unknown token is a `ReferenceCallPrecondition` for `host.availability`, consumed after request-schema admission | treated `missing` and unknown tokens as a grant and returned results |
| s7 host adapter | an adapter's own out-of-vocabulary observation with a valid RequestId → `SYSTEM.OUTCOME.ILLEGAL_STATE` / `HOST.INVARIANT_VIOLATED`, subject `host.availability` | absent |
| s7 retained availability record | a record failing identity availability admission, or naming another Run, → `evidence.corrupt`; an admitted record supplies its state | absent |
| s7 `close_run` outcomes | EvidenceUnavailable → `evidence.missing`; CompleteReplayMismatch → `HOST.IO_FAILURE` / `evidence.regeneration-mismatch`, subject the RunId; other admission refusal → `evidence.corrupt`; any other exception → `HOST.INVARIANT_VIOLATED`, subject `close_run`; never selected by message text | routed by message substring, reported a replay mismatch as `evidence.corrupt`, let exceptions escape |
| s7 carriers (evaluator-fault-contract.v3 line 98) | loss and retained-regeneration remedies verbatim from `x-opensip-routes` | own remedy text |
| s2 step 2 | `QUERY.ENDPOINT_AMBIGUOUS` kept as a closed refusal, unreachable through the wrapper | implicit only |

s1, s2 step 1, s3, the s4 walk, s5, s6, the s7 request rows and s8 were already implemented, and their earlier vectors still pass.

**Corrected helper.** `logs/s43-hc54c.0` ran 66 vectors (31 valid, 34 invalid, 1 explanatory) with 0 assertion failures. It adds:
- 13 new vectors;
- 5 reference-precondition vectors;
- 8 typed-outcome controls;
- 1 endpoint-ambiguity control.

**Key measurements:**
- **Path orientation.** Over `cmp-code`, an `incoming` path `left-pad → main` reports its edge as `left-pad → main`; the stored fact is `main → left-pad`. A `both` path `helper → main` likewise reports the walked hop.
- **Availability observations.** `missing` refuses `HOST.IO_FAILURE` / `evidence.missing` (exit 4) with the loss-carrier remedy. Null, `3`, `stale` and `Retained` are reference preconditions. The adapter's `stale` routes `HOST.INVARIANT_VIOLATED`. Without a valid RequestId, the adapter stays a precondition.
- **Retained availability records.** A `purged` record → `evidence.purged`. A `partial` record → success with `availability: partial`. A record naming another Run, carrying state `missing`, or having duplicate-key bytes → `evidence.corrupt`.
- **Regeneration mismatch.** My own `tools/tamper_outputs.py` flipped the verdict and re-minted every enclosing identity. Owner graph admission and the independent retained closure both admit that store; replay refuses `SEMANTIC_REPLAY_PROOF_MISMATCH:$.verdict`. The query then routes `evidence.regeneration-mismatch` with the tampered RunId as subject, where the unchanged helper said `evidence.corrupt`.
- **Non-typed exception.** A `close_run` that raises `RuntimeError("EVIDENCE_UNAVAILABLE:…")` routes `HOST.INVARIANT_VIOLATED`, subject `close_run`; the unchanged helper crashed.
- **Pre/post.** Both helpers' `execute` ran on identical inputs through one summary (`#/source43ReAudit/prePost`). Every new vector differs from the unchanged helper except two agreement controls: an observed `retained`, and a malformed request whose `QUERY.PARAMS_MALFORMED` precedes the out-of-vocabulary observation.
- **Own tool errors, preserved.**
  - `logs/s43-hc54.0` asserted that every vector differs, including an agreement control.
  - `logs/s43-hc54b.0` passed with an asymmetric pre/post summary.
  - `logs/s43-prov.0` was a provenance census that counted textual mentions as readers.

**Consequence for my source42.v3 result.** The contract grew by only 579 bytes, while the corrected law text runs to thousands of bytes. So at least part of these laws was already in the source42 bytes, and my source42.v3 R-GRAPH-QUERY standing rested on a helper that omitted them. That standing is superseded here.

## The source42.v3 provider-trace payload work

The source42.v3 negotiated payload selection, exact deterministic-CBOR payload bytes, DispatchBindingV1 request/batch correlation and companion association (HC-51, HC-53) stand within the unchanged original scope.
- **Owners unchanged.** Every owner they apply is byte-identical in source43: fact-batch v3, dispatch-binding v1, occupancy-companion v1, the provider-target-attribution return law, fact-plane v1, rust-provider-protocol v2, delivery v2, native-evidence.md.
- **Reuse.** Their helpers are rebound-only, so they are reused as exact source42 measurements (`logs/s42v3-p3b.0`, `.1`: 71 standalone vectors, 25 payload-carrying traces, 0 failures). Checkpoint 3 was re-recorded from those artifacts (`logs/s43-cp.1`). Advisory A-s42v3-1 is carried.

## Executed fresh versus reused

- **Executed fresh in source43.v1** (`logs/s43-*`):
  - **Graph query:** unchanged (`s43-original.0`) and corrected (`s43-hc54c.0`).
  - **Positives, from scratch:** `s43-fin.0` ran from-scratch closure and complete proof replay of all 27 claimed positives in fresh processes. Each passed owner graph admission, the independent retained closure, semantic replay and reachable output-set equality. The designed negative `syntax-mixed-falsecomplete` refuses `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`.
  - **Export replay** (`s43-fin.1`): 27/27 byte-equal recomputed proofs.
  - **Per-record admission log** (`s43-fin.2`): 0 failures.
  - **Custody and records:** phase 0 custody, checkpoints 1–8 re-recorded (`s43-cp.*`), checkpoint 9, provenance, final custody, phases 10–11.
- **Reused as exact source42 measurements**, not re-executed in source43 (`selfcheck/s43-provenance.json#/reusedExactSource42Measurements`):
  - phases 1–2 vectors;
  - phase 3 traces and payload vectors;
  - phase 4 tables, phases 5–8 vectors, discovery/mode vectors and run termination;
  - the positive builds and controls;
  - mutation replay of 71 stores;
  - tamper controls;
  - retention negatives and reference census;
  - the source42 unchanged-vs-corrected matrix and provenance.

  Reuse holds because the only kit change is prose no other helper reads, helper bytes are rebound-only, and stores are byte-identical.

## Why the verdict is ACCEPT-RECONSTRUCTABLE

- **Requirements.** All 123 requirements and 8 standing rules are executed; none failed and none is unexecuted (`requirement-status.json`; checkpoints 0–11 with unioned ID sets). The 3 future-qualification items are recorded as not demanded.
- **Positives.** All 27 claimed complete positives meet every condition below:
  - they have exact exported object tables and all blobs keyed by digest;
  - they were validated against owning schemas including published kit keywords (source42 record validation, re-logged fresh in `s43-fin.2`);
  - they were closed by owner graph admission and the independent retained closure;
  - they were replayed with byte-equal proofs, fresh on the source43 runtime.
- **Graph query.** It is re-audited against the only changed owner. Every omitted law is corrected from the kit, with the original behaviour measured.
- **Negatives and controls** (reused, unaffected): all 32 retention negatives pass and all nine closure controls refuse.
- **Kit custody** is PASS at phase 0 and again at the end.
- **Issues.** No new MUST or SHOULD issue is supported by the source43 text.
- **Helpers.** No open helper failure remains. HC-54 and HC-55 have precise kit or own-tool answers, with original failures preserved.

## Input custody

- **Kit.** `subject/consumer-input-manifest.json` SHA-256 `6d8912f4a78d65946f09047254978570974328ae4d7d883d453f8855347f1beb`, parent frozen subject `db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d`, 104 members. Every SHA-256 and length verified; no unlisted file (`vectors/phase0-custody.json`).
- **Re-verified at the end** (`runs/final-custody.json`: PASS). Charter SHA-256 `33eddd58…`, requirements SHA-256 `6a59306a…`; the 123/8/3 IDs are unchanged.
- **Runtime setup:**
  - `rebind-s43-manifest.json`: 102 files, 121 occurrences;
  - `preserved/s42-v3-final/manifest.json`: source42.v3 bytes of every changed file;
  - `preserved/s42-v3-final/runs-manifest.json`: hashes of 404 copied result files.

## Helper corrections

| HC | What | Selector | Original failure (preserved) |
|---|---|---|---|
| HC-54 | Graph-query omissions listed above | `query-projection-contract.v3.md` s2, s4, s7; `evaluator-fault-observation.schema.v3.json#/x-opensip-routes`; `identity-schemas.v3.json#/$defs/availability` | `logs/s43-original.0`; `vectors/graph-query.json#/source43ReAudit/prePost`; own tool errors `logs/s43-hc54.0`, `logs/s43-hc54b.0` |
| HC-55 | Runtime adaptation: root rebind, source43 custody hashes, runtime labels, preservation manifests | — | `rebind-s43-manifest.json` (exit 1 on runtime labels only) |
| HC-47..HC-53 | source42 corrections: enumeration `programEntry`, view attribution, runtime adaptations, own control rebuild, `candidateOrdinal` order token, provider-trace payload law | as recorded in `tools/hc_source42.py` | preserved in `preserved/` and logs |

## Claimed complete positives and exact exports

The run ids are unchanged from source42 (the stores are byte-identical) and were re-derived fresh by `logs/s43-fin.0`. Each export is `runs/<run>.store.json` (object table plus every blob). Each Run also has a from-scratch closure (`runs/<run>.replay.fromscratch.json`), an export replay (`runs/<run>.replay-export.json`) and an admission log (`runs/<run>.records.json`).

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

**From-scratch command** (reads only exported stores and the kit, one fresh process per Run):
`cd /private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output && /tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py && /tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py`

## Independent vectors and results

| Area | Result | Artifact / log (standing) |
|---|---|---|
| graph query (neighbors/path/reach, selection, cursor, disclosure, failures, parity) | 66 vectors, 0 failures; source43 re-audit pre/post measured | `vectors/graph-query.json`, `logs/s43-hc54c.0` (fresh) |
| from-scratch closure and complete replay | 27/27 positives admit through all four stages; designed negative refuses | `logs/s43-fin.0` (fresh) |
| export replay | 27/27 byte-equal recomputed proofs | `logs/s43-fin.1` (fresh) |
| per-record admission log | 27 positives, 0 failures | `logs/s43-fin.2` (fresh) |
| C/H, CVE1, lexical admission, raw vs parsed, acyclic joins | 0 failures | `logs/s42v2-cp.1` (reused) |
| capability manifests, four gates | 5 positives, 19 negatives, 0 failures | `logs/s42v2-cp.2` (reused) |
| protocol3 traces with FactBatch payload law | 25 traces, all 34 rows; 21 FactBatch payloads (14 admitted, 5 refused, 2 faulted before payload) | `logs/s42v3-p3b.1` (reused) |
| FactBatch payload/correlation vectors | 71 vectors, 29 decoder, 10 encoder; 0 failures | `logs/s42v3-p3b.0` (reused) |
| relation/rung table, RC-0..RC-6, cell outcomes | 17 rows, 16 RC vectors, 10 outcome vectors | `logs/s42-fin-p4to9.0` (reused) |
| discovery, U-0, U-1/s1.2, U-4b, U-8, U-9 | 29 vectors, 0 failures | `logs/s42-fin-disc.0` (reused) |
| phases 5–8 vectors | 0 failures; 45/45 public termination goldens | `logs/s42-fin-p4to9.1`–`.5` (reused) |
| analysis-Run termination | 28 Runs, 9 candidate checks, 30 host compositions | `logs/s42-fin-p4to9.8` (reused) |
| mutation replay | 71 stores: 29 admit, 42 refuse | `logs/s42v2-fin2.1` (reused) |
| tamper | every semantic control refused by replay | `logs/s42-fin-tamper.*` (reused) |
| retention/reference-class negatives | 32 constructed, all pass | `logs/s42-fin-neg.0` (reused) |

## Issues

### newMustIssues

None.

### newShouldIssues

None.

### Disposition of my own earlier results

- **source42.v3 graph query:** the R-GRAPH-QUERY standing is superseded by HC-54, measured above. It was an own helper omission, not a kit gap.
- **source42.v3 provider-trace payload work:** retained; its owners are unchanged.
- **source42.v2 provider-trace limitation:** stays withdrawn (HC-53).
- **source41 claimed positives:** stay superseded (HC-47).
- **Source42 advisories:** carried; their owner documents are unchanged.

### Advisories (nonblocking)

- **A-c1.** Internal refusal names no kit owner publishes are still spelled `cb24.*`; `blind-review.json#/advisories` lists the measured set.
- **A-c2.** The inherited `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination; the successor D9 artifact is a disclosed live obligation (native lines 3313-3327).
- **A-c3.** Exact-snapshot import correspondence changes `import2` on every source change (workflows s3 lines 440-449).
- **A-n1.** In the closed per-entry IndeterminateReason order, reason (3) is unreachable for entries (workflows s3 lines 402-411).
- **A-n6.** A rust unit's `languageMode` is decided by the mode table but not restated by U-4b.2 and not enforced by U-4b.5.
- **A-v2-1.** Composition s7 does not scope typed-prefix closure explicitly to outputs.
- **A-v2-2.** `policy-derivation3` is outside the reachable output set.
- **A-v2-3.** Identity s3 calls its digest vocabularies closed while the native and relation bundles publish their own.
- **A-s41-1.** run-termination s7.6 step 1 names no key; the s6 key is applied at both boundaries.
- **A-s41-2.** U-1's omitted-`allowJs` default reads against s1.2's `checkJs` fallback; s1.2 is applied.
- **A-s42-1.** Enumeration s1 names no refusal key for a second `default-unit` binding; `cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY` is used.
- **A-s42-2.** `ENUMERATION_BINDING_PROGRAM_ENTRY` is applied to all three entry joins.
- **A-s42-3.** No published rule refuses the `explicit-plan-selection` spelling of a sole syntax-only binding.
- **A-s42v3-1.** TypeScript major 2 is published only as deltas over delivery.v2: "historical FactBatchV2" and no TypeScript Hello schema. The current s9.1 text is applied.
- **A-s43-1 (new).** Query s7 does not state `GraphQueryContextV1.availability` for a successful query with no availability observation, although the field is required. This is a reference-harness case, since a product host always holds the availability record (identity-and-evidence lines 1721-1725). The reconstruction reports `retained` after `close_run` admits.

## What required invention

No record, identity or refusal outcome had to be invented. Named readings, each measured or stated beside its alternative:
- A-s43-1: `retained` when no availability observation is supplied;
- graph-query typed outcomes: reconstructed by normalizing my own `close_run` structured refusal (refusing stage plus leading typed key; detail text never selects a route);
- carried: A-s42v3-1, A-s42-1, A-s42-2, A-s42-3, A-s41-1, A-s41-2, A-v2-1, A-n6.

## Limitations

- **Source42 query bytes.** They are not in my custody, so the delta was assessed by a full law-by-law re-audit rather than a diff.
- **Reuse.** Every measurement other than the graph query, from-scratch closure/replay, export replay, admission log, custody and checkpoints is reused from source42 with custody. It was not re-executed in source43.
- **Graph query adapter and records.** The host-adapter route and retained availability-record admission are exercised as reference vectors, not as an implemented host adapter or evidence store.
- **Provider-trace payload law.** It is executed on constructed payloads, not on built Runs. The post-terminal `bind_worker_occupancy` capture is not constructed. No worker-process enforcement is claimed.
- run-termination s7.5 row 2 and s5 stage-terminal carriers are exercised by vectors, not on built Runs.
- The retained-closure walker names what it delegates to owner graph admission, which runs as its own stage.
- Census pairs that no constructed positive contains have no negative.
- **Enumeration branches.** No positive uses an explicit-plan-selection binding, a js-synthesized or jsconfig default binding, or a Rust explicit binding.
- **Read but not constructed:** PolicyTestSuiteV2 and the U-8 boundary-inventory superset join.
- `discovery-defaults.py` was neither read nor used.
- **Root admission.** Root admission of the exported bytes is unobserved.
- **Product qualification.** This review makes no product qualification claim and no implementation authorization; all future-qualification items remain unperformed.

## Retained outputs

- **Machine-readable review:** `blind-review.json`. It holds the verdict basis, issues, advisories, dispositions, `source43Continuation` (kit delta, graph-query re-audit, fresh vs reused, provenance), HC records, positives with run ids, and `requirementStatus`.
- **Checkpoints and status:** `checkpoints/phase-0.json` … `phase-11.json`; `requirement-status.json`.
- **Notes:**
  - `notes/00-session-standing.md` (source42.v2, v3 and source43 continuation records);
  - `notes/10-gaps.md`;
  - `notes/11-provider-trace-payload-law.md`;
  - `notes/12-source43-query-contract.md`;
  - earlier notes 01, 07–09.
- **Code:** `ref/`, `builders/`, `tools/` (new: `tools/hc_source43.py`, `tools/provenance_s43.py`, `tools/summarize_s43_query.py`), `vectors/`.
- **Results and logs:** `runs/`, `envelopes/`, `traces/`, `negatives/`, `selfcheck/` (new: `selfcheck/s43-provenance.json`), `logs/` (new: `s43-*`).
- **Own history:** `preserved/` (new: `preserved/s42-v3-final/`); the source42.v1–v3 runtimes are preserved in place.
