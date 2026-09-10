# Foundation completion review — phases 0–4 and imported-observation boundary

**Verdict: `FOUNDATION_READY_FOR_INDEPENDENT_RECHECK`**

This is not whole-consumer acceptance, not `ACCEPT-RECONSTRUCTABLE`, and not root admission. The previous other-four-Runs and syntax-code pilot verdicts remain independent recheck requests and are not copied as ACCEPT. All 123 original accept-blocking obligations remain.

## Standing and custody

| Object | SHA-256 | Result |
|---|---|---|
| kit `consumer-input-manifest.json` | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | matches |
| parent frozen SHA | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | matches |
| 80 subject files | kit list | PASS 80/80 |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | unchanged |
| `continuation-inputs.json` | `93114f8a0cae5a51bddeb283f8f74d6d71093713c8c1506d329bd7e3465f3064` | no new peer/root files |

Write root is only `consumer-b.v12-team-foundation-corrections.v1/output`. Path correction record: `path-correction-record.foundation.json` (SHA `066c86a1b9c026589e9cbee13541c4a5f3f0cfa3a6eedcc3871eaa7359d0ff9d`).

## Frozen this pass (byte-identical)

ALL five Run stores and ALL scope-v2 / shared historical `vectors/`, `traces/`, `envelopes/`, `query/`, and prior review files stayed byte-identical. Shared original vectors were preserved at `preserved-failures/foundation-shared-path-original/` before any new exhibit. New work is under `foundation/` so those paths are not erased.

| Store | SHA-256 |
|---|---|
| `runs/syntax-code.store.json` | `0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36` |
| `runs/ts.store.json` | `af2238a65afb0b7d82c5dd5ab1278436d55c4bc3087631d407563346593eb4ca` |
| `runs/rust.store.json` | `e6457494c46b2c8cefc7f6c0779da08de820b26890bc250defe1361b6e29fd4a` |
| `runs/syntax-data.store.json` | `e050875685a7a4f706c98982baeafbce3b15f9c6c4c2ff97c2800a820645ec87` |
| `runs/rust-partial-clones.store.json` | `227856b1dec3c4d051677e156b9b3883613a90dee7e1c8db46670bb95a4e1141` |

## From-scratch command

```
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-foundation-corrections.v1/output/scripts/foundation_reconstruct.py
```

Exit 0. A second run produced byte-identical `foundation/` artifacts. Required assertion or schema/setup failures exit nonzero (`FOUNDATION_ASSERTION_FAILED`).

Producer SHA `21b9e401027568ec59b68750836e192aebd069c12e250084bec9d38e1f3572ed`.

## Original-ID mapping (scoped copy)

Shared `vectors/` and `traces/` stay as frozen scope-v2 evidence. Original IDs map to NEW foundation exhibits:

| Original ID | Kind | Exhibit |
|---|---|---|
| S-FRESH-ORIGIN, S-NOT-PRODUCT, S-KIT-ONLY, S-MANIFEST-VERIFY, S-NO-ORACLE, S-MISSING-DEP-IS-CUSTODY, S-PROFILE-CURRENT, S-CONTINUATION, R-FIVE-CONTRACTS-INDEX, R-SOURCE-MAP-SCOPE, R-CVE1-TYPES-AVAILABLE | standingRule | `foundation/phase-0.json` |
| R-H-HELPER | standaloneCanonicalVector | `foundation/h-helper.json` |
| R-CVE1-EIGHT-TYPES | standaloneCanonicalVector | `foundation/cve1-eight-types.json` |
| R-LEXICAL-ADMISSION | standaloneCanonicalVector | `foundation/lexical-admission.json` |
| R-SEMANTIC-VS-OPERATIONAL | standaloneCanonicalVector | `foundation/semantic-vs-operational.json` |
| R-RAW-VS-PARSED | standaloneCanonicalVector | `foundation/raw-vs-parsed.json` |
| R-ACYCLIC-JOINS | standaloneCanonicalVector | `foundation/acyclic-joins.json` |
| R-CAP-ADMISSION | standaloneCanonicalVector | `foundation/cap-admission.json` |
| R-CAP-NAMED-GATES | standaloneCanonicalVector | `foundation/cap-named-gates.json` |
| R-TRACE-COMPLETE | standaloneTraceVector | `foundation/traces/complete.json` |
| R-TRACE-UNAVAILABLE | standaloneTraceVector | `foundation/traces/unavailable.json` |
| R-TRACE-CANCEL | standaloneTraceVector | `foundation/traces/cancel.json` |
| R-TRACE-FAULT | standaloneTraceVector | `foundation/traces/fault.json` |
| R-TRACE-IDENTITY-BEFORE-SOURCE | standaloneTraceVector | `foundation/traces/identity-before-source.json` |
| R-TRACE-TERMINAL | standaloneTraceVector | `foundation/traces/terminal.json` |
| R-TRACE-EXECUTED-VS-HOST | standingRule | `foundation/traces/executed-vs-host.json` |
| R-RELATION-RUNG-TABLE | standaloneCanonicalVector | `foundation/relation-rung-table.json` |
| R-COUNT-CLASS-ATTEMPT | standaloneCanonicalVector | `foundation/count-class-attempt.json` |
| R-CODE-VS-DATA-MATRIX | standaloneCanonicalVector | `foundation/code-vs-data-matrix.json` |
| R-ENUM-VS-RESOLUTION | standingRule | `foundation/enum-vs-resolution.json` |
| R-ADVERTISED-MODE-PATHS | standingRule | `foundation/advertised-mode-paths.json` |
| R-IMPORTED-OBSERVATION-BOUNDARY | standaloneCanonicalVector | `foundation/imported-observation-boundary.json` |

## What was actually checked

Expected behavior is from the normative kit only. Assertions check the promised gate, identity, or transition, not merely that a file exists or that some refusal occurred.

- **C/H.** Published recipe `H(D,X)=SHA256(ASCII("opensip.product.v1")||00||ASCII(D)||00||uint64BE(len(C(X)))||C(X))`. Snapshot A/B inhabit `identity-schemas.v3.json#/$defs/snapshot` with a Blob-array `sourceInventory` (not `{schemaVersion,entries}`). Measured `snapshot2:3324a39a…` ≠ `snapshot2:496d2081…` after a `vcsDigest` change.
- **Semantic vs operational.** Same paired snapshot identities. RequestId/ExecutionId/wall clock are not Run/snapshot fields; stuffing `requestId` into `#/$defs/run` is additionalProperties refuse.
- **CVE1 eight types.** Round-trip of `null`, `false`, `true`, `unsigned-64`, `negative-signed-64`, `NFC-UTF8-string`, `array`, `string-keyed-map` from `resolved-inputs.v2.json#planIdContract.canonicalValueEncoding`. Map key-order independence. Negatives: non-NFC string, float.
- **Lexical / raw-vs-parsed.** RAW bytes, not `json.loads`. Original discriminating refusals retained with named codes: duplicate key, float, exponent, `-0`, leading zero, integer range, unpaired surrogate, BOM, unescaped control. Duplicate raw `{"a":1,"a":2}` is distinct from encoding `{"a":1}`; `C(true)` ≠ `C(1)`.
- **Acyclic joins.** Schema-valid snapshot→plan→view→proof-bundle→semantic-evidence→evaluation-seal→run. Proof does not carry `evidenceId`/`runId`. Cycle attempt `proof.evidenceId` is additionalProperties refuse.
- **Capability-manifest admission BEFORE encoding.** CAP-MANIFEST-ID-V1 recomputes `hex(SHA-256(UTF8("opensip.capability-manifest.v1")||0x00||CVE1(manifest)))` = `6e6f63c79285d280ea21d109c8eb6ce2f4107d464210c013a0f08d7d6d72652b`. Named first-refusal gates in order ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER. Boolean/`"1"` `schemaVersion` → ADM-TYPE; extra/missing key → ADM-CLOSED; `ALL-SUPPORTED` and `calls=enumerated` → ADM-DOMAIN; unsorted `platformIds`/`providers` → ADM-ORDER (`masksLater` false). Combined boolean `schemaVersion` plus extra key first-refuses ADM-TYPE and masks CLOSED/DOMAIN/ORDER.
- **Protocol traces.** Transition matching against `protocol3-transitions.v1.json` is executed. Frame payload schema and native process spawn are labeled future-host assumptions. Complete → DONE/`complete`. Unavailable → DONE/`unavailable`. Cancel → `cancelled`. Deadline → FAULT. HelloAck identity tokens before OpenUniverse; unmatched OpenUniverse is P3-34 with `sourceBytesSent` false. Post-terminal `FactBatch` is `post-terminal-frame`.
- **Registry.** 13 relations from `relation-payload-schemas.v2.json`. File ladder is `["enumerated"]`; no resolved rung invented. RC-1/RC-2 applied: `file@enumerated` is `not-applicable`/`attempted=false` with and without facts; `imports@resolved-target` is complete with zero unresolved edges and incomplete with one. Grammar registry: typescript has `clones@normalized-body-hash`; json is data-document with no body identity. Frozen stores inspected read-only: 5 file facts, all `resolution=enumerated`. All six advertised language modes have a representable analysis path.
- **Imported-observation boundary.** Retained schema-valid `RuntimePayloadV1` (`istanbul-json`, not a free-form JSON blob) and `import2:e52a84643da40c64d94a586444b2340446db24ec1915066752b5dffde8044af8`. That identity is not `fact2` and is not native Coverage. Frozen TS Run import `import2:1bdd740b9ce2b4639c7c12b5abbce5d95937bebd6ba70981d58dc4eafcc70eaa` is cited read-only.

## Helper corrections

Each correction records the original failure, selector, and change (`foundation/helper-corrections.json`). Historical shared-path vectors were not rewritten.

## Pending outside this task

Phases 5–11 complete Runs and Include properties, workflow envelopes, query, remaining standalone vectors, evaluator replay, deliver/verdict. Independent four-Run review and pilot review are other actors. Do not treat those scopes as closed here.

## Exhibit hashes

See `foundation-completion-review.json` `exhibitHashes` and `foundation/reconstruction-results.json`.
