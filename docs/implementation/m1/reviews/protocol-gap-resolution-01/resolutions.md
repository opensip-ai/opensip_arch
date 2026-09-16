# M1 protocol gap resolution 01: TS2-G1..G12, audit G9 (control) and G10 (report projection)

**Standing:** proposal for root review. It is not an approval, a wire change or product code. Every architecture and product input was read-only. Hashes are of the bytes read on 2026-09-14 from the `opensip_arch` working tree, which has unrelated uncommitted edits, including to `COORDINATOR-DECISIONS.md`. `resolutions.json` is the machine-readable form and carries every selector, quote and patch.

**Scope:** the TS2 gap register in `m1-typescript-wire-translation-01/fields.json`, plus audit gaps G9 and G10 from `m1-generation-owner-audit-01/audit.md`. The source45/application46 design is treated as historical and settled. Rust major-3 gaps are out of scope.

## 1. Summary

| Gap | Disposition | Successor needed | Result |
|---|---|---|---|
| TS2-G1 bstr carrier | IMPLEMENTATION-CHOICE | no | Wire stays CBOR bstr. Private carriers are a Rust `ByteString(Vec<u8>)` newtype and TS `Uint8Array`, with a hex mirror in vectors only. |
| TS2-G2 NFC/CBOR | GOVERNED | no | Handwritten decode-once admission. |
| TS2-G3 stageId bound | GOVERNED | no | `StageIdText` 1..255 applies through `DispatchBindingV1.expectedStageId`. |
| TS2-G4 subjectScopeCommitment | **OWNER-INCONSISTENCY** | **P-1** | `SubjectScopeV1` is retained. Each key carries its own `scope2` text form, and the worker echoes it. |
| TS2-G5 AnchorRefV1 | GOVERNED types + **OWNER-INCONSISTENCY** | **P-2** | `source-span` types are fixed. `fact-ref` cannot be represented in fact2 and is refused. |
| TS2-G6 payload selection | GOVERNED | no | Decode entry points take the state; no tag, no try-each. |
| TS2-G7 same names | GOVERNED | no | Namespace by `$id` and language. |
| TS2-G8 array bounds | GOVERNED | no | Derived handwritten bounds. |
| TS2-G9 wireSchemaCommitment | GOVERNED | no | Historical self-check only; no Hello member. |
| TS2-G10 manifestSha256 | **OWNER-INCONSISTENCY** | **P-3** | Raw `DigestHex` over CBOR entries, with no domain. |
| TS2-G11 unbounded members | GOVERNED | no | ExecutionId grammar, LogicalPath via fact2, frame limit otherwise. |
| TS2-G12 commitment domains | GOVERNED | optional P-4 | Exact field→domain map below. |
| Audit G9 control owner | **OWNER-FOUND** (audit false negative) | no; root confirms selection | `control-protocol-contract.v2` + `control-completion.schema.v3`. |
| Audit G10 report projection | **OWNER-MISSING** | **P-5** | No schema document exists; report.ts is blocked; successor shape proposed. |

Commitment function used throughout (delivery.v2 `commitments.domainRule`):
`C(d, v) = "sha256:" + hex(SHA-256(UTF8(d) || 0x00 || deterministic-CBOR(v)))`.

## 2. Key sources (path, sha256)

| Key | Path | sha256 |
|---|---|---|
| delivery2 | docs/coop/artifacts/delivery.v2.json | 47b6cfd1…e3cabf3 |
| nativeMd | docs/v2/contracts/product-v1/native-evidence.md | 83b99783…ca0 |
| identityMd | docs/v2/contracts/product-v1/identity-and-evidence.md | c82404f3…cd4f |
| workflowsMd | docs/v2/contracts/product-v1/workflows-and-surfaces.md | 1ee203e3…6ff6ed |
| identitySchemas3 | docs/coop/design-corrections/foundation/identity-schemas.v3.json | a76c9e2f…3db21 |
| handshake / startup | native/provider-handshake.schemas.v1.json / provider-startup.schemas.v1.json | 9090e2ad…5f84 / 1e35a77b…729c |
| dispatch | native/dispatch-binding.schema.v1.json | 868c3cf2…df938 |
| factPlane | docs/coop/artifacts/fact-plane.v1.json | 90572008…b4d |
| rust2 / checkRust2 | rust-provider-protocol.v2.json / check-rust-provider-protocol.py | 6308a98c…793b / c190ee7f…502e |
| nativeModel / startupModel | native_evidence_model.v2.py / provider_startup_model.v1.py | 7d1c0acf…d7be / 3f75b859…d494 |
| attributionModel | foundation/provider_attribution_return_model.v2.py | 2cfac924…7abd |
| controlContract2 | docs/coop/artifacts/control-protocol-contract.v2.json | c50a79fe…bdca |
| controlSchema3 | docs/coop/completion/control-completion.schema.v3.json | 2929de62…c46a98c |
| controlContract5 / freeze5 / review5 | control-completion.contract.v5.md / .freeze.v5.json / .independent-review.v5.json | ebfb1178…cd9 / 0e4a020f…84f5 / dc31dd4d…2d23 |
| application1 | docs/coop/completion/architecture-application.v1.json | 15b3932a…d7f3 |
| envelope4 | docs/implementation/m1/metadata-v2/command-envelope.schema.json | 6b563861…0ea8 |
| layout / reportInventory / reportAssetBinding | 14-repository-and-module-layout.md / prototype-report-inventory.md / report-asset-binding.v1.json | c7b10bf6…287e / 3f4d4dd2…c3a0 / 71363c06…27a6 |
| register / decisions | 08-decision-and-readiness-register.md / COORDINATOR-DECISIONS.md | de21a7e0…95fe / cccc2dda…e4e4 |

## 3. TypeScript major 2 resolutions

### TS2-G1: CBOR byte string (implementation choice)

The wire is unchanged: CBOR major type 2, definite length, no tags. fact-plane `candidateSchema.transportRepresentation` and handshake `candidateCborProjection` already make hex a vector-only transcription.

- `SnapshotFileChunkV1.bytes`: 1..1048576 bytes.
- `FactCandidateV1.canonicalRelationPayload`: 1..1048576 bytes. It must decode once to the registry schema and re-encode byte-equal.
- Projection document: add a private `$defs/WireByteString` = `{"x-opensip-wire-type":"byte-string"}` with per-use min/max byte annotations. It has no JSON `type` and is never a wire validator.
- Rust: a `protocol::wire::ByteString(Vec<u8>)` newtype whose codec accepts only bstr. Length is checked from the prefix before allocation.
- TS: `Uint8Array`.
- Vectors: lowercase hex (`canonicalRelationPayloadHex`; for chunks, a vector-only `<member>Hex` if ever authored).
- Commitment preimages carry the bstr, never hex.

### TS2-G2: NFC and canonical CBOR (governed)

The rule is delivery.v2 `canonicalCbor.decodeRule`: decode once under the closed schema, re-encode and compare. Refuse duplicate or unknown keys, non-shortest integers, floats, tags, indefinite items, non-NFC text and wrong map order.

JSON-Schema `maxLength` bounds (`StageIdText`, the fact-batch text caps) count Unicode scalar values. UTF-8 byte bounds apply only where an owner says bytes. Any violation is `PROVIDER.PROTOCOL_VIOLATION`.

### TS2-G3: stageId bound (governed)

`dispatch#/properties/expectedStageId` is `maxLength 255` and is defined as "StageRequestV1.stageId". native-evidence §9.6 requires a dispatch binding for each requested stage and refuses if it is omitted. Therefore:

- `StageRequestV1.stageId`, `StageResultV1.stageId` and the `dependsOn[]` items are all `StageIdText`: NFC text, 1..255.
- A Plan stage whose id cannot satisfy this is never projected. That is a pre-spawn host invariant refusal: no spawn, no new public code.

### TS2-G4: subjectScopeCommitment (owner inconsistency → P-1)

The two sides:

- **Retained:** delivery.v2 `RequestedCoverageDomainV1.workerRule` ("every key.subjectScopeCommitment to equal subjectScope.subjectScopeCommitment") and `coverageDomain.keyConstruction.subjectScopeCommitment`.
- **Current:** native-evidence §4.1a (lines 1889–1986) and identity §3 (lines 287–294) define the key commitment as the per-key `scope2`. Startup `coverageFrames.entries` requires `entries[i].key.subjectScopeCommitment == keys[i]`. The native model builds one descriptor per requested key (`pre_analyze_unavailable_conversion`) and checks it in `admit_coverage_result_v3`.

Keys of one stage differ in target universe and relation, so the two rules cannot both hold. §0 names no superseding row for them; line 136 covers only C-2 v4.

Decision:

- `SubjectScopeV1` is fully retained: `C("opensip.coverage.subject-scope.v1", sorted SnapshotFileSubjectV1[])`, `subjectCount` equal to the number of `kind=file` entries, and still inside `domainCommitment`.
- `CoverageKeyV1.subjectScopeCommitment` = `"sha256:"` + the hex of `scope2 = H("subject-scope", D_key)`, where D_key is:
  - `schemaVersion` 2
  - `snapshotId`: the snapshot2 id
  - `sourceUniverse`, `targetUniverse`: the key's universe-id suffixes
  - `relation`, `resolution`: the key's own
  - `enumeratorClosure`: the Plan-selected TS provider closure2
  - `subjects`: the host's enumeration
- The host mints it before spawn, and the same descriptor feeds coverage admission and pre-Analyze conversion.
- The worker still recomputes `subjectScope` and `domainCommitment`. For each key it checks only the `Sha256Text` form and echoes the value; it does not recompute it, because no wire member carries enumeratorClosure or subjects, and no new channel is added.
- Wire effect: none.

### TS2-G5: AnchorRefV1 (governed types; fact-ref → P-2)

`source-span` types:

| Member | Type and value |
|---|---|
| `snapshotId` | text: the exact OpenUniverse snapshot2 id (startup `identityMembers` exact-echo class) |
| `path` | NFC text 1..4096, equal to a `kind=file` manifest path |
| `contentSha256` | DigestHex equal to that entry's digest; becomes fact2 `blobDigest` (attribution model `_span_key_candidate`; §9.6 line 3110) |
| `startByte`, `endByte` | uint64, with startByte < endByte ≤ byteLength |
| `factId` | null |

**The fact-ref contradiction:**

- fact-plane `anchorSchema.variants.fact-ref` (FACT-ID-V1) is retained.
- But `TypeScriptCapabilitiesV2` makes `fact-identity-fact2` mandatory.
- identity-schemas v3 `fact.anchors.items` is closed to `{path, blobDigest, startByte, endByte}`.
- §9.1 says FACT-ID-V1 is never relabeled.

So `kind=fact-ref` is refused at candidate admission (`PROVIDER.PROTOCOL_VIOLATION`) before fact2 minting. The vocabulary and shape are unchanged.

Count: non-empty on the wire, bounded by the frame limit. At mint: at most 100000 and within the relation `anchorLaw`. The fact-batch.3 cap of 4096 is a vector bound only.

### TS2-G6: payload selection (governed)

The handshake law `factBatch.negotiated` and `violation`, and startup `preAnalyzeUnavailable.phase`, decide the payload.

- Rust: `decode_fact_batch(bytes, negotiated)` returns `FactBatchPayload::{V1,V3}`, and `decode_unavailable(bytes, phase)` returns `UnavailablePayload::{PreAnalyze,PostAnalyze}`. The variant is fixed by host state before decoding. There is no untagged serde and no wire tag; these enums are host selectors.
- TS: named validators per state.
- Any other payload in that state is `PROVIDER.PROTOCOL_VIOLATION`.

### TS2-G7: same names (governed)

- `protocol::typescript2::{FactCandidateV1, CoverageKeyV1, AnchorRefV1, …}` come from the projection document.
- The native `CoverageKeyV2`/`CoverageResultV3` stay in the evidence module; Rust major 3 stays separate.
- The universe join is by suffix (startup `coverageFrames.entries`).

### TS2-G8: derived bounds (governed, handwritten)

- `affectedStageIds`: exactly the requested stage ids in order, 1..1024.
- Unavailable/BudgetExhausted `coverage`: the sum of requested keys, 1..131072, and the payload ≤ 67108864 bytes.
- Coverage `entries`: equal to the stage key count, ≤ 128.

### TS2-G9: wireSchemaCommitment (governed)

No TS2 Hello member carries a contract digest (handshake `frameAndMajor`). `96ffbe7b…` stays recomputable over the unchanged bytes and serves as a source-pin self-check. The projection document is identified by its registry sha256. No new domain is minted.

### TS2-G10: manifestSha256 (owner inconsistency → P-3)

The two readings:

- The field text is "DigestHex over deterministic-CBOR entries".
- The retained `commitments.domains.snapshotManifest` plus `domainRule` would give a `sha256:`-prefixed, domain-separated value.

Decision: `manifestSha256` = lowercase hex of `SHA-256(deterministic-CBOR(entries))`, with no domain and no prefix. Seal and Accepted echo it. Reasons:

- The type `DigestHex` (`^[0-9a-f]{64}$`) cannot hold a `sha256:` value.
- rust2 `commitments.snapshotManifest` states exactly this recipe, and checkRust2 line 1048 executes it.

The `snapshotManifest` domain is unused for major 2.

### TS2-G11: unbounded members (governed)

- ExecutionId: exactly `^exec1_[0-9a-f]{32}(?![\s\S])`, 38 bytes (identity §2; startup `ExecutionIdText` defers to admission).
- Anchor path: LogicalPath through the fact2 inventory join.
- Manifest, chunk and link-target paths: no bound beyond the frame limit. The host emits only inventory paths, and the worker must not refuse more strictly than the host constructs.
- Universe ids: `Sha256Text`.

### TS2-G12: field → commitment domain map (governed; optional P-4)

§0 line 126 and startup `coverageFrames.commitments` say "recipes and domains unchanged". Each field text matches exactly one of the eight retained domains, and checkRust2 lines 852–1129 apply the same structure.

| Field | Value |
|---|---|
| `TypeScriptCoverageV2.coverageCommitment` | `C("opensip.ts-provider.stage-coverage.v1", entries)` |
| `StageResultV1.coverageCommitment` | `C(stage-coverage.v1, that stage's entries)` (equals its Coverage frame value) |
| `CompleteV1.coverageStreamCommitment` | `C("opensip.ts-provider.coverage-stream.v1", all entries, stage-major)` |
| `TypeScriptUnavailableV2.coverageCommitment` | `C(coverage-stream.v1, coverage)` |
| `TypeScriptBudgetExhaustedV2.coverageCommitment` | `C(coverage-stream.v1, coverage)` |
| `StageResultV1.factCommitment` | `C("opensip.ts-provider.stage-facts.v1", stage candidates)` |
| `CompleteV1.factStreamCommitment` | `C("opensip.ts-provider.fact-stream.v1", all candidates)` |
| `FactBatchV1.batchCommitment` | `C("opensip.ts-provider.fact-batch.v1", facts)`; absent on V3 |
| `RequestedCoverageDomainV1.domainCommitment` | `C("opensip.ts-provider.requested-coverage-domain.v1", {subjectScope, keys})` |
| `SubjectScopeV1.subjectScopeCommitment` | `C("opensip.coverage.subject-scope.v1", SnapshotFileSubjectV1[])` |
| `CoverageKeyV1.subjectScopeCommitment` | scope2 text form (G4) |
| `manifestSha256` | raw DigestHex (G10) |

An empty fact stream commits the empty CBOR array (`0x80`); coverage is never empty.

## 4. Audit G9: common control protocol owner (owner found)

The audit's §3.3 "no owner" is a false negative. It searched only v2 architecture, contracts, native and v13 inputs.

- **Semantics and framing:** `control-protocol-contract.v2.json` is DR-102's accepted design contract (D-015). The register marks DR-102 SATISFIED at line 291, and the current D-372 disposition at line 413 reads "Retain byte-opaque common control framing". It is a source45 member.
- **Closed bodies:** `control-completion.schema.v3.json` (`urn:opensip:design:control-schema:3`). Its freeze v5 was reviewed "NO-OBJECTION-WITHIN-REPAIR-SCOPE" (review v5, 0 must-fix). It is pinned by `architecture-application.v1.json` units.control, which D-369 bound. The current DR-125 disposition at line 434 reads "Retain common SDK/control/broker contract". Contract v5 states: "The accepted authority remains control-protocol-contract.v2.json … This package supplies the previously incomplete typed body/state details."

Implementation decisions:

- **Encoding:** UTF-8 JSON on fd3/fd4, non-canonical, with no identity derived from control bytes. Provider planes stay opaque CBOR octets on fd0/fd1.
- **Envelope:** `{type, seq 1..2^53-1, controlMajor, body}`, closed. `type` is a real discriminator, so the carrier is an internally tagged enum of 16 variants.
- **Framing (handwritten):** a 4-byte big-endian body length. 0 is refused. Up to 65536 before helloAck; afterwards the negotiated value, between 65536 and 16777216.
- **Bodies (schema v3):**
  - hello and helloAck, with ≤128 subprotocol tuples; role and subprotocol ≤128 bytes.
  - select/selectAck: the tuple.
  - refusal: `RF-1..RF-8`; `supportedControlMajors[1..16]` iff RF-1; `decisionClass PR-1..PR-9` iff RF-6; detail ≤1024 bytes.
  - ping/pong/health: nonce ≤128 bytes. healthReport adds `ready|busy|stopping`.
  - resourceReport: three uint53 values. fault: detail ≤1024 bytes.
  - cancel: `user|deadline|supervisor-fault`. shutdown: `normal|cancelled|refused|fault`. shutdownAck: `{}`.
  - effectRequest: `HE-1|HE-2` plus two references ≤1024 bytes.
  - effectResult: three uint53 sequences with outcomeSeq > decisionSeq, `REVERSIBLE|IRREVERSIBLE`, `COMPLETED|FAILED|INDETERMINATE`, and an optional resultRef.
- **Version axis:** `controlMajor` 1 is independent of TS major 2 and Rust major 3 (DR-111 line 421; contract v2 `handshake.ownVersionSurface`). Subprotocol tuples are opaque.
- **Handwritten in `crates/components/src/control_protocol.rs`:** framing, `x-maxUtf8Bytes`, refusal if/then/else, the 16×8×2 state matrix, RF precedence and correlation. Effect messages stay inert until the security journal activation that review v5 lists under `pendingJoins`.
- **protocol.ts:** no control carriers for M1. Provider fd3/fd4 participation is contract v2 T-4, routed to DR-103/DR-120.
- **Root confirmation:** schema v3 is reached only through `architecture-application.v1.json`, not directly as a source45 member. D-372 keeps compatible preview constraints binding through the named source inventory. Root should confirm the registry selection; no design text change is needed.

## 5. Audit G10: report document projection (owner missing → P-5)

What the owners say:

- report-asset-binding requires a sha256 for each "complete supported report projection schema document".
- Layout row 556 generates report.ts "from the same selected output schema as Rust"; row 463 says projection.rs builds "bounded optional exploration data".
- workflows §8: HTML values come from "this same declared host projection", and the JSON envelope is the parity reference.
- The report inventory (lines 212–224) says graph and history data reach the reports "through embedded host projections", that "the embedded projection/schema mapping must follow those exact applicability sets before UI implementation", and that the feature rows "do not add arbitrary fields to closed CommandEnvelope schemas".

Envelope4 is closed. It holds `run`, `findings`, `availability`, per-surface records, and a `queryResponse` only for graph-query surfaces. It has no history, catalog, analysis-command graph or symbol exploration panels. `Renderer` in inventory4 names no schema. A search of docs (excluding reviews) found no report projection schema. **Envelope4 alone cannot be the report projection.**

Decision:

- **M1:** output.rs envelope4 carriers proceed. report.ts and the report-projection carriers are recorded as blocked (open AUDIT-G10); nothing is generated as a stand-in.
- **Successor proposal for the workflow/output owner (DR-122/DR-123):**
  - Document: `workflows/schemas/evaluator3/report-projection.schema.json`, `$id urn:opensip:product-v1:workflows:evaluator3:report-projection:1`.
  - Root members: `schemaFamily` const, `schemaMajor` 1, `command` (the exact 8-command HTML set), and a required `envelope` that `$ref`s command-envelope:4 and is the only parity source.
  - Closed `panels`, each optional and wrapped `{state present|omitted|unavailable, reason?, data?}`:
    - `evidence`: native `CoverageResultV3[]`
    - `graph`: graph-query:3 `GraphQueryResponseV1[]`
    - `comparison`: comparison:2
    - `history`: `{runId, envelope}[]`
    - `catalog`: UQ-1
  - A missing required panel is `DELIVERY.REQUIRED_PROJECTION_FAILED`.
  - The document's raw sha256 is what goes into `projectionSchemaSha256s`.

## 6. Patch text (exact)

**P-1** (native-evidence.md §0, new row after line 126):
> | `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.definitions.RequestedCoverageDomainV1.workerRule` (the clause "requires every key.subjectScopeCommitment to equal subjectScope.subjectScopeCommitment"), `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.coverageDomain.keyConstruction.subjectScopeCommitment` | **Superseded** for typescript-semantic major 2 by §4.1a. Each `CoverageKeyV1.subjectScopeCommitment` is `"sha256:"` plus the 64-hex of the host-minted `scope2` of that key's own subject-scope descriptor (key relation/rung, source/target universe suffixes, Plan-selected enumerator closure, host enumeration). `SubjectScopeV1` (shape, `opensip.coverage.subject-scope.v1` value and `subjectCount`) and `RequestedCoverageDomainV1.domainCommitment` are **retained**. The worker still recomputes both, and it echoes each key commitment without recomputing it. No member, type or pattern changes. The `coverageDomain.vectors` key commitments are historical. |

**P-2** (native-evidence.md §0, new row):
> | `docs/coop/artifacts/fact-plane.v1.json`, `docs/coop/artifacts/delivery.v2.json` | `$.factRecordContractV1.anchorSchema.variants.fact-ref`, `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.definitions.AnchorRefV1.variants.fact-ref` | **Not admitted** under `fact-identity-fact2`, which is mandatory for typescript-semantic major 2 and rust-semantic major 3: `identity-schemas.v3.json#/$defs/fact/properties/anchors` has no fact reference, and FACT-ID-V1 is never relabeled (§9.1). A candidate anchor with `kind=fact-ref` is `PROVIDER.PROTOCOL_VIOLATION` before any `fact2` is minted. The `kind` vocabulary and `AnchorRefV1` shape are unchanged. A `source-span` anchor's `snapshotId` is the exact OpenUniverse `snapshot2` text (startup `identityMembers` exact-echo class), `contentSha256` is the manifest entry's DigestHex and becomes `fact2` `blobDigest`, and `startByte`/`endByte` are uint64. |

**P-3** (native-evidence.md §0 row at line 119, sentence appended after "…are **retained**;"):
> Within the retained `commitments`, `domains.snapshotManifest` does not apply to `SnapshotManifestV1`/`SnapshotSealV1`/`SnapshotAcceptedV1.manifestSha256`. That member stays its field-level `DigestHex` = lowercase hex of raw SHA-256 over deterministic-CBOR(`entries`), with no domain or `sha256:` prefix, as in `rust-provider-protocol.v2` `commitments.snapshotManifest`.

**P-4** (optional; §0 row at line 126, replacing its last sentence):
> Commitment recipes and domains are unchanged over the `CoverageResultV3` values: the `Coverage` wrapper `coverageCommitment` and `StageResultV1.coverageCommitment` use `stageCoverage` over that stage's entries; `CompleteV1.coverageStreamCommitment` and the `TypeScriptUnavailableV2`/`TypeScriptBudgetExhaustedV2` `coverageCommitment` use `coverageStream` over the stage-major array.

**P-5:** a new `report-projection.schema.json` (§5 shape), plus layout row edits:
> | `crates/contracts/src/generated/output.rs` | model; generated | Generated command envelope carriers and report projection carriers from `workflows:evaluator3:report-projection:1` and its closure. |
>
> | `apps/report/src/generated/report.ts` | model; generated | Generate projection carriers and runtime shape-validation support from `workflows:evaluator3:report-projection:1`, the same selected output schema as Rust; exact generator remains pending, and shape validity grants no semantic authority. |

**P-6** (correction to the implementation audit, not an owner patch): audit §3.3 and the §2 protocol.rs row should name `control-protocol-contract.v2.json` together with `control-completion.schema.v3.json` as the control owners (text in the JSON).

## 7. Code changes

1. **Registry:** add `control-completion.schema.v3.json` (sha 2929de62…) to recipe `contracts-rust`, with module segment `control_schema_3` and validator owner `control_protocol.rs`. Its refusal branch uses if/then/else, so it needs the dialect adapter or a handwritten check.
2. **TS2 projection document:** add `WireByteString` (G1). Type `StageIdText` on request/result/dependsOn (G3), AnchorRefV1 members (G5) and the ExecutionId grammar (G11).
3. **`provider_protocol.rs` and the TS codec:**
   - no gate: G2, G6, G8, the G12 map;
   - gated on P-3: G10 DigestHex;
   - gated on P-1: G4 echo rule;
   - gated on P-2: G5 fact-ref refusal.
4. **Host coverage-domain projection:** one subject-scope descriptor per key before spawn, reused at admission and in pre-Analyze conversion (G4).
5. **`control_protocol.rs`:** framing, byte bounds, state matrix, RF precedence; effect messages stay inert.
6. **report.ts and the output.rs report projection:** blocked on P-5.

## 8. Unresolved (truly)

- **UQ-1:** report panel limits (graph, history, evidence, total embedded bytes) and the owner record for the rule/capability/recipe catalog panel. The report inventory requires measured thresholds and forbids inheriting prototype budgets, and no current schema defines a catalog display record. Owner: DR-122/DR-123 workflow/output.
