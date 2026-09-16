# Rust3 wire translation inventory: `rust-semantic` provider protocol major 3

**Standing.** This is a proposed implementation artifact for root review, authored by actual Claude. It is not approval, not a wire change, not a schema document and not product code. It supplies audit `m1-generation-owner-audit-01` item T2 (the Rust3 projection of `rust-provider-protocol.v2` retained selectors), as the TS2 inventory did for T1. No architecture, product or other candidate file was modified. Every unaccepted proposal cited here stays a proposal.

**Scope.** Every member of `docs/coop/artifacts/rust-provider-protocol.v2.json` `$.wireSchema` (`envelope`, `frameSchemas`, `payloadSchemas`, `definitions`), the members reached through its `external` definitions, and the schema-native members that replace them. Dispositions come from `native-evidence.md` §0 rows 117-130, §3.2, §3.6, §4.1a and §9.1-§9.7. Field-level successors come from `native/provider-handshake.schemas.v1.json`, `native/provider-startup.schemas.v1.json`, `native/native-evidence.schemas.v2.json` (non-superseded defs), `native/fact-batch.schema.v3.json`, `native/occupancy-companion.schema.v1.json`, `native/dispatch-binding.schema.v1.json` and `native/protocol3-transitions.v1.json`. `rust-provider-protocol` v1/v3/v4 and their checkers are not owners. `rust-provider-protocol.v2` stays the inherited base: `HelloV3.expectedProtocolContractSha256` pins its bytes. The TS2 translation and the gap-resolution proposals were read for method and cross-reference only.

**Machine form.** `fields.json` holds every row, with source path, pinned sha256, selector and exact original field text. `coverage.json` holds counts, every check result, probes and pins. `tools/build.py` regenerates all three from `tools/common.py` and `tools/rows.py`. It opens sources read-only and fails on:
- source byte drift;
- an uncovered or extra member;
- an unresolvable ref or `$ref`;
- a wire-type mismatch against a resolvable ref;
- an unexpected successor delta;
- a prose/schema member mismatch;
- a moved citation anchor.

`--selftest` applies mutation controls. Logs are in `logs/`.

```
OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch python3 tools/build.py
OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch python3 tools/build.py --selftest
```

## 1. Coverage

- inherited grammar members tabulated: **231** (envelope 5, frameSchemas 21, payloadSchemas 101, definitions 104)
- external expansion rows: **59**; new schema-native member rows: **76**; new frame rows: **6**
- dispositions (rows + frames): {"new": 82, "removed": 4, "replaced": 130, "retained": 105, "unresolved": 32, "value-substituted": 19}
- resolution classes (rows + frames): {"governed": 296, "owner-contradictory": 34, "owner-missing": 42}
- rows whose Rust3 wire type is UNSTATED: 22
- rows/frames with schema-native ref: 235; wire-type cross-checks: 199 checked, 0 not derivable, **0 mismatches**
- transitive `$ref` closure of the Rust3 successor records: 131 refs followed, 54 distinct targets, **0 unresolved**
- member-list comparisons: 34; citation anchors verified: 55; semantic-owner anchors verified: 41
- build failures: **0**

## 2. Conventions

- **Wire type** uses rust2 `canonicalCbor.closedDataModel`: `null`, `bool`, `uint64`, `UTF-8-NFC-text`, `byte-string`, `definite-array`, `definite-text-keyed-map`. Negative integers are forbidden on the Rust wire. `X|null` means present-and-null; rust2 `schemaLanguage.maps` says nullable is never omission. `UNSTATED` means no bounded owner states the CBOR type. Such a row cites a gap and makes no guess.
- **Two wire columns.** `v2 wire` is the inherited type and `Rust3 wire` the major-3 type. A type change (map -> array for capabilities) is visible.
- **Type source** says where the type comes from:
  - field text or a definition;
  - an echo of a typed member;
  - a rust2 algorithm or commitment;
  - a labeled derivation, such as `rust2 limitPolicy.arithmetic` for counts and offsets;
  - the successor schema, or an external owner.

  Derivations are never presented as owner text.
- **Disposition:**
  - `retained`: unchanged.
  - `replaced`: a successor owns the member, with member change `unchanged`, `value-changed`, `moved` or `removed`.
  - `value-substituted`: same name and shape, with a stated supersession of the value domain.
  - `new`: schema-native and absent from v2.
  - `removed`: no Rust3 wire carrier.
  - `unresolved`: no consistent major-3 owner.
- **Resolution class:**
  - `governed`: an owner states the answer.
  - `owner-missing`: no bounded owner states it.
  - `owner-contradictory`: owners disagree.
  - `proposal-pending`: only an unaccepted proposal answers it.
  - `implementation-choice`: no wire question.
- **Shape vs semantic owner.** A schema-native ref owns shape only. The `semantic-owner checks` column names the law that shape cannot express. That law may be a rust2 selector, a reference-model function verified at its line, the dispatch schema, fact-plane or C-2. Those models are executable law within their stated scope. They are not implementation admission code.

## 3. Envelope

The major-3 envelope keeps the five inherited members `{protocolMajor, direction, sequence, frameType, payload}`. All are required and closed. `direction` is Rust-only; the TS2 envelope has no such member.
- **protocolMajor** is exactly 3 (native-evidence.md:122; handshake law `frameAndMajor.rust-semantic`).
- **frameType** is the closed 26-name vocabulary. `Coverage` is renamed `CoverageV3` (:129, :2884). DependencySource{Manifest,Chunk,Seal,Accepted} and NativeContextVerified are added (§9.2). The vocabulary equals the frame set of `protocol3-transitions.v1.json` (checked).
- **sequence and direction** keep the v2 frame precheck. §0 does not supersede it; see R3-G17.
- **payload** is selected by `frameType`, except FactBatch (negotiated token) and Unavailable (phase) (R3-G6).

Framing is 8-byte big-endian length, 32 raw SHA-256 bytes, then the canonical-CBOR payload (rust2 `framing`, 40-byte prefix). It is not CBOR members. No major-3 envelope record name is published (R3-G3). The wire carries none, and this translation proposes no published name.

## 4. Stage identity: C-2 text vs Analyze ordinal vs Plan ordinal

| carrier | member | wire | meaning |
|---|---|---|---|
| `StageRequestV2` | `stageOrdinal` | uint64 | contiguous 0..n-1 in **this** Analyze (= `DispatchBindingV1.analyzeRequestOrdinal`) |
| `StageRequestV2.planStage` | `stageId` | text | exact C-2 stageId text inside the nested, byte-exact C-2 stage; 1..255 through `DispatchBindingV1.expectedStageId`, which names `StageRequestV2.planStage.stageId` |
| `FactBatchV2` / `FactBatchV3` | `stageId` | text (StageIdText) | echo of `planStage.stageId`; never `stageOrdinal`, never `retainedStageOrdinal` |
| `CoverageV3` | `stageId` | text | attributes every `CoverageResultV3` entry (entries carry no stageId/entryOrdinal) |
| `UnavailableV3` | `affectedStageIds` | array of text | all requested stageIds, request order |
| `BudgetExhaustedV3` | `triggerStageId` | text | the stage whose budget unit was exhausted |
| `StageResultV2` | `stageId` | text | exact requested stageId. **No `stageOrdinal` and no `factBatchCount`**, unlike TS `StageResultV1` |
| `PreAnalyzeUnavailableV1` | none | none | no stage member; host derives affected stages from `planAndDomainProjection.selectedStageRule` |
| host only | `retainedStageOrdinal` | none | `execution-plan.stages[].ordinal`; never on the wire (native-evidence.md:3024-3043) |

Differences from TS2:
- Rust nests the C-2 stage (`planStage`), so optional C-2 members (`dependsOn`, `budget`, `capabilityGrants`, `providerId`) are **present only when present in the ExecutionPlan**. A carrier must preserve absence.
- Rust `analysisOrdinal` is `Uint64` with no exact value stated (TS2 fixes 0).
- Rust Analyze carries a host-derived `analysisDomain` (`subjects` + 8-member request keys + `domainCommitment`) instead of TS `requestedCoverageDomain`.

## 5. FactBatch: historical V2 vs negotiated V3

| aspect | historical `FactBatchV2` (`target-attribution-v2` not in both arrays) | negotiated `FactBatchV3` (token in Hello **and** HelloAck) |
|---|---|---|
| owner | rust2 `payloadSchemas.FactBatchV2` (retained, :123); JSON vector `provider-handshake.1#/$defs/RustFactBatchV2Vector` | `opensip.product.fact-batch.3` |
| members | `analysisOrdinal, stageId, batchIndex, candidates` | `schemaVersion(3), analysisOrdinal, stageId, batchIndex, candidates, occupancyCompanions` |
| per-batch commitment | none | none |
| cap | `maxFactBatchCandidates` 4096 | same; companions <= len(candidates) |
| wrong payload for negotiation | `PROVIDER.PROTOCOL_VIOLATION` | `PROVIDER.PROTOCOL_VIOLATION` |
| stage/stream commitments | `stageFacts` / `factStream` over the ordered `FactCandidateV1` stream, whichever payload carried it (handshake law `commitments.rust-semantic`) | same |

`FactCandidateV1` is unchanged under both payloads and has no occupancy member. On the wire, `canonicalRelationPayload` is a CBOR byte string. The fact-batch.3 `canonicalRelationPayloadHex`/`decodedRelationPayload` pair is a JSON-vector transcription and observation.

## 6. Coverage and batch streams

- **Per-stage output order.** Each stage emits zero or more FactBatch frames, then exactly one CoverageV3 (P3-23, P3-24). P3-24 increments `stageIndex`/`stagesCompleted` and resolves to READY_COMPLETE only after the last stage.
- **Candidate stream.** `batchIndex` is contiguous from 0 per stage. `candidateOrdinal` is contiguous from 0 across the batches of a stage and resets at the next stage (v2 T016/T017; `DispatchBindingV1.expectedFirstCandidateOrdinal`). Array order in V3 is `candidateOrdinal` strictly increasing (occupancy vocabulary). Contiguity is a separate stream law.
- **Spool and aggregates.** Each candidate is spooled as deterministic-CBOR of `{analysisOrdinal, stageId, candidate}`. Its exact bytes are checked-added against `maxCandidateSpoolBytes` 1073741824, and one entry against `maxFactCandidatesTotal` 1000000, before allocation (rust2 `limitPolicy.candidateSpoolAccounting`). Request and response payload totals and frame counts are `max{Request,Response}{PayloadBytesTotal,Frames}`.
- **Admission atomicity.** The complete candidate set and Coverage are admitted only after valid Complete, custody, order, bijection, recomputed commitments, zero exit and EOF. Every other outcome discards all candidates. Unavailable and BudgetExhausted may admit terminal exhaustive-unknown Coverage only (rust2 `candidateAtomicity`).
- **Coverage entries.** `CoverageV3.entries[i]` answers `analysisDomain.requestedCoverageDomain[i]`, and the count equals the key count. `key.relation/resolution/subjectScopeCommitment` equal the request key. `key.sourceUniverse/targetUniverse` are the 64-hex suffixes of the request key's universe ids. The request key's `producer`, `producerVersion` and `schemaVersion` stay request coordinates (startup law `coverageFrames.entries`).
- **Terminal coverage.** UnavailableV3 and BudgetExhaustedV3 `coverage` lists CoverageResultV3 in stage-major/key order. Entry k belongs to the stage whose cumulative key range contains k. The pre-Analyze Unavailable carries no coverage; the host mints it after DONE (`pre_analyze_unavailable_conversion`).
- **Commitments (rust2 `commitments`):**
  - Retained: `stageFacts` (`opensip.rust-provider.stage-facts.v2`) and `factStream` (`...fact-stream.v2`).
  - Recipes unchanged over CoverageResultV3 values: `stageCoverage` (`...stage-coverage.v2`) and `coverageStream` (`...coverage-stream.v2`).
  - `subjectScope`, `analysisDomain`, `snapshotManifest` and `preparedOutputBlob/Manifest` are stated.
  - The field-to-domain map for the wrapper and terminal `coverageCommitment` members is not stated (R3-G12).
  - The subject-scope recipe is contested (R3-G4).
- **Budget.** Units work-units/items/bytes use checked increments. Milliseconds is a host deadline and never BudgetExhausted. Overflow is a protocol fault (rust2 `deterministicBudget`).

## 7. Frame table (Rust3, 26 names)

| frame | direction | worker terminal | Rust3 payload | disposition | class | ref | P3 rules | notes | gaps |
|---|---|---|---|---|---|---|---|---|---|
| Hello (inherited) | host-to-worker | False | HelloV3 | replaced | governed | opensip.product.provider-handshake.1#/$defs/HelloV3 | P3-01 |  |  |
| HelloAck (inherited) | worker-to-host | False | HelloAckV3 | replaced | governed | opensip.product.provider-handshake.1#/$defs/HelloAckV3 | P3-02 | identityNegotiated = every identity token present in capabilities |  |
| OpenUniverse (inherited) | host-to-worker | False | OpenUniverseV3 | replaced | governed | opensip.product.provider-startup.1#/$defs/OpenUniverseV3 | P3-03 | guard identityNegotiated=true; otherwise FAULT with sourceBytesSent=false |  |
| UniverseAccepted (inherited) | worker-to-host | False | UniverseAcceptedV3 | replaced | governed | opensip.product.provider-startup.1#/$defs/UniverseAcceptedV3 | P3-04 |  |  |
| SnapshotManifest (inherited) | host-to-worker | False | SnapshotManifestV2 | retained | governed |  | P3-05 |  |  |
| SnapshotFileChunk (inherited) | host-to-worker | False | SnapshotFileChunkV2 | retained | governed |  | P3-06 |  |  |
| SnapshotSeal (inherited) | host-to-worker | False | SnapshotSealV2 | retained | governed |  | P3-07 |  |  |
| SnapshotAccepted (inherited) | worker-to-host | False | SnapshotAcceptedV2 | retained | governed |  | P3-08; P3-09; P3-10 | dependencyMode is true for every admitted OpenUniverseV3, so P3-08 -> READY_DEPENDENCY_MANIFEST; P3-09/P3-10 unreachable |  |
| PreparedOutputManifest (inherited) | host-to-worker | False | UNRESOLVED (inherited PreparedOutputManifestV2) | unresolved | owner-contradictory |  | P3-16 | frame name retained; only when preparedOutputSetId is non-null | R3-G9 |
| PreparedOutputChunk (inherited) | host-to-worker | False | UNRESOLVED (inherited PreparedOutputChunkV2) | unresolved | owner-contradictory |  | P3-17 |  | R3-G9 |
| PreparedOutputSeal (inherited) | host-to-worker | False | UNRESOLVED (inherited PreparedOutputSealV2) | unresolved | owner-contradictory |  | P3-18 |  | R3-G9 |
| PreparedOutputAccepted (inherited) | worker-to-host | False | UNRESOLVED (inherited PreparedOutputAcceptedV2) | unresolved | owner-contradictory |  | P3-19 |  | R3-G9 |
| Analyze (inherited) | host-to-worker | False | AnalyzeV2 | retained | governed |  | P3-22 |  |  |
| FactBatch (inherited) | worker-to-host | False | FactBatchV2 unless target-attribution-v2 is in both Hello and HelloAck arrays; then FactBatchV3 | retained | governed | opensip.product.fact-batch.3# | P3-23 |  | R3-G6 |
| Coverage (inherited) | worker-to-host | False | frame renamed CoverageV3 with payload CoverageV3 | replaced | governed | opensip.product.provider-startup.1#/$defs/CoverageV3 | P3-24 | frame name Coverage does not exist for rust-semantic major 3 (typescript-semantic keeps Coverage) |  |
| Unavailable (inherited) | worker-to-host | True | PreAnalyzeUnavailableV1 in WAIT_NATIVE_CONTEXT_VERIFIED (P3-21); UnavailableV3 in ANALYZING (P3-25) | replaced | governed | opensip.product.provider-startup.1#/$defs/UnavailableV3 | P3-21; P3-25 |  | R3-G6; R3-G17 |
| BudgetExhausted (inherited) | worker-to-host | True | BudgetExhaustedV3 | replaced | governed | opensip.product.provider-startup.1#/$defs/BudgetExhaustedV3 | P3-26 |  |  |
| Complete (inherited) | worker-to-host | True | CompleteV2 | retained | governed |  | P3-27 |  | R3-G13 |
| ProviderFault (inherited) | worker-to-host | True | ProviderFaultV2 | retained | governed |  | P3-28 |  | R3-G14 |
| Cancel (inherited) | host-to-worker | False | CancelV2 | retained | governed |  | P3-29 |  | R3-G14; R3-G17 |
| Cancelled (inherited) | worker-to-host | True | CancelledV2 | retained | governed |  | P3-30 |  | R3-G14 |
| CoverageV3 (new) | worker-to-host | False | CoverageV3 | new | governed | opensip.product.provider-startup.1#/$defs/CoverageV3 | P3-24 | rename of inherited Coverage; next is stage-dependent ANALYZING_OR_READY_COMPLETE |  |
| DependencySourceManifest (new) | host-to-worker | False | DependencySourceManifestV3 | new | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceManifestV3 | P3-11 |  | R3-G11 |
| DependencySourceChunk (new) | host-to-worker | False | UNNAMED (prose member list only) | new | owner-missing |  | P3-12 |  | R3-G3; R3-G10 |
| DependencySourceSeal (new) | host-to-worker | False | DependencySourceSealV3 | new | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3 | P3-13 |  |  |
| DependencySourceAccepted (new) | worker-to-host | False | UNNAMED ('exact seal echo'; shape of DependencySourceSealV3 by echo) | new | owner-missing | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3 | P3-14; P3-15 |  | R3-G3; R3-G10 |
| NativeContextVerified (new) | worker-to-host | False | NativeContextVerifiedV1 | new | governed | opensip.product.provider-startup.1#/$defs/NativeContextVerifiedV1 | P3-20 |  |  |

## 8. Field rows: every inherited member

Source for every row: `docs/coop/artifacts/rust-provider-protocol.v2.json` sha256 `6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b`; the exact selector and original field text are in `fields.json` (`rows[].source`).

### envelope (`RustProviderEnvelopeV2`; no published major-3 record name, R3-G3)

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| protocolMajor | required | uint64 | uint64 | exactly 3 (inherited field text 'uint64 exactly 2') | value-substituted | governed |  | field-text | wire.admit_hello: envelope protocolMajor == 3 before payload admission; wire.admit_hello_ack |  |
| direction | required | UTF-8-NFC-text | UTF-8-NFC-text | enum host-to-worker\|worker-to-host; equals the frame row direction | retained | governed |  | field-text | rp2.transitionAstV2 framePrecheck directionMatchesFrameSchema; chk2.step_frame |  |
| sequence | required | uint64 | uint64 | exact next sequence for its direction; each direction starts at 0; a counter at 18446744073709551615 refuses | retained | governed |  | field-text | rp2.transitionAstV2 framePrecheck sequenceEqualsDirectionCounter/directionCounterLessThan; chk2.step_frame | R3-G17 |
| frameType | required | UTF-8-NFC-text | UTF-8-NFC-text | closed 26-name vocabulary (inherited 21 minus Coverage; plus CoverageV3, DependencySourceManifest, DependencySourceChunk, DependencySourceSeal, DependencySourceAccepted, NativeContextVerified); lawful per concrete phase | value-substituted | governed |  | field-text | p3.transitions first match; no row -> P3-34 FAULT; ne.protocol3_run |  |
| payload | required | definite-text-keyed-map | definite-text-keyed-map | exact closed payload map selected by frameType, except FactBatch (negotiated token) and Unavailable (phase); payload <= maxFramePayloadBytes 67108864 | retained | governed |  | field-text | rp2.canonicalCbor decodeRule; rp2.framing allocationRule | R3-G6 |

### payloadSchemas.HelloV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| hostBuildId | required | UTF-8-NFC-text | UTF-8-NFC-text | IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/HelloV3/properties/hostBuildId | definition IdentityText | wire.admit_hello: equals trusted hostBuildId | R3-G2 |
| expectedProtocolContractSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex = raw SHA-256 of rust-provider-protocol.v2.json bytes 6308a98c...793b; authenticates the inherited base only | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/HelloV3/properties/expectedProtocolContractSha256 | field-text | wire.admit_hello: CONTRACT_PIN and CONTRACT_DIGEST; hs.law expectedProtocolContractSha256 |  |
| expectedIdentity | required | definite-text-keyed-map | definite-text-keyed-map | ExpectedRustIdentityV3 (6 members; protocolMajor 3) | replaced (value-changed) | governed | opensip.product.provider-handshake.1#/$defs/HelloV3/properties/expectedIdentity | field-text | wire.admit_hello: identityFields equal the selected Plan rust-v1 row |  |
| expectedCapabilities | required | definite-text-keyed-map | definite-array | RustCapabilitiesV3: 4..13 unique RustCapabilityToken, strictly ascending UTF-8, four identity tokens (inherited: closed 6-member RustProviderCapabilityV2 map) | replaced (value-changed) | governed | opensip.product.provider-handshake.1#/$defs/HelloV3/properties/expectedCapabilities | field-text | wire.admit_hello: equals the UTF-8-sorted signed capability row; hs.law capabilityArrays (order not JSON-Schema checkable) |  |
| limits | required | definite-text-keyed-map | definite-text-keyed-map | ProtocolLimitsV3: exactly 32 uint64 constants (24 inherited identical + 8 of §9.3) | replaced (value-changed) | governed | opensip.product.provider-handshake.1#/$defs/HelloV3/properties/limits | field-text | rp2.limitsHandshake semantic and deterministic-CBOR byte equality; wire.admit_hello: LIMITS |  |

### payloadSchemas.HelloAckV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| protocolMajor | required | uint64 | uint64 | exactly 3 (inherited exactly 2); equals Hello expectedIdentity.protocolMajor | replaced (value-changed) | governed | opensip.product.provider-handshake.1#/$defs/HelloAckV3/properties/protocolMajor | field-text | wire.admit_hello_ack: IDENTITY_ECHO |  |
| providerBuildId | required | UTF-8-NFC-text | UTF-8-NFC-text | IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control; exact Hello expectedIdentity value | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/HelloAckV3/properties/providerBuildId | successor schema (inherited text: exact Hello expectedIdentity value) | wire.admit_hello_ack: IDENTITY_ECHO |  |
| rustCommitHash | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex; exact Hello expectedIdentity value | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/HelloAckV3/properties/rustCommitHash | successor schema; resolved-inputs.v2 rust-v1 digestFields | wire.admit_hello_ack: IDENTITY_ECHO |  |
| hostTriple | required | UTF-8-NFC-text | UTF-8-NFC-text | IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control; exact Hello expectedIdentity value | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/HelloAckV3/properties/hostTriple | successor schema | wire.admit_hello_ack: IDENTITY_ECHO |  |
| targetTriple | required | UTF-8-NFC-text | UTF-8-NFC-text | IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control; exact Hello expectedIdentity value | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/HelloAckV3/properties/targetTriple | successor schema | wire.admit_hello_ack: IDENTITY_ECHO |  |
| sysrootDigest | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex; exact Hello expectedIdentity value | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/HelloAckV3/properties/sysrootDigest | successor schema; rust-v1 digestFields | wire.admit_hello_ack: IDENTITY_ECHO |  |
| capabilities | required | definite-text-keyed-map | definite-array | RustCapabilitiesV3; exact echo of Hello expectedCapabilities (same members, same order) | replaced (value-changed) | governed | opensip.product.provider-handshake.1#/$defs/HelloAckV3/properties/capabilities | successor schema (inherited: exact recursive equality with Hello record) | wire.admit_hello_ack: CAPABILITY_ECHO |  |

### payloadSchemas.OpenUniverseV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| executionId | required | UTF-8-NFC-text | UTF-8-NFC-text | IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control (startup ExecutionIdText minLength 1; IdentityText rules by admission); the host value is exec1_[0-9a-f]{32} (identity-and-evidence.md:63-72), a subset | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/OpenUniverseV3/properties/executionId | field text 'IdentityText exact AttemptRecord value' | start.admit_open_universe: exact AttemptRecord value; NFC + IdentityText | R3-G2 |
| snapshotId | required | UTF-8-NFC-text | UTF-8-NFC-text | SnapshotId2 ^snapshot2:[0-9a-f]{64} (inherited ^snap1:sha256:[0-9a-f]{64}$) | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/OpenUniverseV3/properties/snapshotId | definition SnapshotId -> SnapshotId2 | start.admit_open_universe: equals the verified Plan snapshot2 |  |
| planId | required | UTF-8-NFC-text | UTF-8-NFC-text | PlanId2 ^plan2:[0-9a-f]{64} (inherited ^plan1:sha256:[0-9a-f]{64}$) | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/OpenUniverseV3/properties/planId | definition PlanId -> PlanId2 | start.admit_open_universe: equals the verified plan2 |  |
| planIntentCommitment | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text; exact AttemptRecord/ExecutionPlan value | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/OpenUniverseV3/properties/planIntentCommitment | field-text | start.admit_open_universe: OPEN_UNIVERSE_CORRELATION |  |
| providerId | required | UTF-8-NFC-text | UTF-8-NFC-text | const rust-semantic | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/OpenUniverseV3/properties/providerId | field-text |  |  |
| universe | required | definite-text-keyed-map | definite-text-keyed-map | RustSemanticUniverseV2: 21-member rust-v1 map, protocolMajor 3, resolvedInputs RustUniverseV2ResolvedInputs | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/OpenUniverseV3/properties/universe | field-text | start.admit_open_universe: handshakeJoin (6 members) equals HelloV3.expectedIdentity; nativeContextId suffix in plan.nativeContextDigests |  |
| repositoryResolution | required | definite-text-keyed-map | definite-text-keyed-map | RepositoryResolutionV3 {dependencySourceSetId, preparedOutputSetId\|null, authorizationId\|null, workerExecutesRepositoryCode:false, effects\|null} | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/OpenUniverseV3/properties/repositoryResolution | field-text | start.admit_open_universe: REPOSITORY_RESOLUTION_JOIN; ne.protocol3_open_universe_event: derived dependencyMode/preparedMode |  |

### payloadSchemas.UniverseAcceptedV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| executionId | required | UTF-8-NFC-text | UTF-8-NFC-text | exact recursive echo of OpenUniverse | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/UniverseAcceptedV3/properties/executionId | echo (no v2 field text): OpenUniverse (inherited fields.all) | start.admit_universe_accepted: UNIVERSE_ACCEPTED_ECHO |  |
| snapshotId | required | UTF-8-NFC-text | UTF-8-NFC-text | SnapshotId2 ^snapshot2:[0-9a-f]{64} echo | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/UniverseAcceptedV3/properties/snapshotId | echo (no v2 field text): OpenUniverse | start.admit_universe_accepted: UNIVERSE_ACCEPTED_ECHO |  |
| planId | required | UTF-8-NFC-text | UTF-8-NFC-text | PlanId2 ^plan2:[0-9a-f]{64} echo | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/UniverseAcceptedV3/properties/planId | echo (no v2 field text): OpenUniverse | start.admit_universe_accepted: UNIVERSE_ACCEPTED_ECHO |  |
| providerId | required | UTF-8-NFC-text | UTF-8-NFC-text | const rust-semantic echo | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/UniverseAcceptedV3/properties/providerId | echo (no v2 field text): OpenUniverse |  |  |
| universe | required | definite-text-keyed-map | definite-text-keyed-map | RustSemanticUniverseV2 echo (no digest-only echo) | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/UniverseAcceptedV3/properties/universe | echo (no v2 field text): OpenUniverse | start.admit_universe_accepted: UNIVERSE_ACCEPTED_ECHO |  |
| repositoryResolution | required | definite-text-keyed-map | definite-text-keyed-map | RepositoryResolutionV3 echo | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/UniverseAcceptedV3/properties/repositoryResolution | echo (no v2 field text): OpenUniverse | start.admit_universe_accepted: UNIVERSE_ACCEPTED_ECHO |  |

### payloadSchemas.SnapshotManifestV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| snapshotId | required | UTF-8-NFC-text | UTF-8-NFC-text | SnapshotId2 ^snapshot2:[0-9a-f]{64} via exact OpenUniverse echo | value-substituted | governed | opensip.product.provider-startup.1#/$defs/SnapshotId2 | echo (no v2 field text): OpenUniverse.snapshotId |  |  |
| manifestSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex = lowercase hex SHA-256(deterministic-CBOR(entries)); no domain, no prefix | retained | governed |  | rust2 $.commitments.snapshotManifest | rp2.commitments snapshotManifest: worker recomputes |  |
| entries | required | definite-array | definite-array | items SnapshotEntryV2; 1..maxSnapshotEntries 200000; strict ascending unique CanonicalPath (UTF-8 bytes) | retained | governed |  | field-text | rp2.limitPolicy allocation; rp2.requestProjection snapshot |  |

### payloadSchemas.SnapshotFileChunkV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| snapshotId | required | UTF-8-NFC-text | UTF-8-NFC-text | SnapshotId2 ^snapshot2:[0-9a-f]{64} via exact manifest/OpenUniverse echo | value-substituted | governed | opensip.product.provider-startup.1#/$defs/SnapshotId2 | echo (no v2 field text): SnapshotManifest.snapshotId |  | R3-G16 |
| path | required | UTF-8-NFC-text | UTF-8-NFC-text | CanonicalPath of one kind=file manifest entry, in manifest order | retained | governed |  | echo (no v2 field text): SnapshotEntryV2.path (field text 'path/index/offset exact contiguous manifest order') |  |  |
| chunkIndex | required | uint64 | uint64 | contiguous from 0 per path | retained | governed |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G15 |
| byteOffset | required | uint64 | uint64 | exact cumulative prior chunk bytes of that path (checked add) | retained | governed |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text | rp2.limitPolicy arithmetic | R3-G15 |
| bytes | required | byte-string | byte-string | non-empty; 1..maxSnapshotChunkBytes 1048576 | retained | governed |  | field-text | rp2.limitPolicy allocation: length before allocation | R3-G1 |

### payloadSchemas.SnapshotSealV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| snapshotId | required | UTF-8-NFC-text | UTF-8-NFC-text | SnapshotId2 ^snapshot2:[0-9a-f]{64} echo | value-substituted | governed | opensip.product.provider-startup.1#/$defs/SnapshotId2 | echo (no v2 field text): manifest |  |  |
| manifestSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex echo of SnapshotManifest.manifestSha256 | retained | governed |  | echo (no v2 field text): manifest (fields.all 'exact checked aggregates') |  |  |
| entryCount | required | uint64 | uint64 | exact entries length (<= 200000) | retained | governed |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G15 |
| totalFileBytes | required | uint64 | uint64 | exact checked sum of file byteLength; <= maxSnapshotTotalFileBytes 8589934592 | retained | governed |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text | rp2.limitPolicy aggregateAccounting | R3-G15 |
| totalChunkCount | required | uint64 | uint64 | exact emitted chunk count | retained | governed |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G15 |

### payloadSchemas.SnapshotAcceptedV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| snapshotId | required | UTF-8-NFC-text | UTF-8-NFC-text | SnapshotId2 ^snapshot2:[0-9a-f]{64} echo of SnapshotSeal | value-substituted | governed | opensip.product.provider-startup.1#/$defs/SnapshotId2 | echo (no v2 field text): seal |  |  |
| manifestSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex; exact SnapshotSeal value after byte/digest/VFS validation | retained | governed |  | echo (no v2 field text): seal |  |  |
| entryCount | required | uint64 | uint64 | exact SnapshotSeal value | retained | governed |  | echo (no v2 field text): seal; derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G15 |
| totalFileBytes | required | uint64 | uint64 | exact SnapshotSeal value | retained | governed |  | echo (no v2 field text): seal; derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G15 |
| totalChunkCount | required | uint64 | uint64 | exact SnapshotSeal value | retained | governed |  | echo (no v2 field text): seal; derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G15 |

### payloadSchemas.PreparedOutputManifestV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| planId | required | UTF-8-NFC-text | UTF-8-NFC-text | PlanId2 ^plan2:[0-9a-f]{64} via exact OpenUniverse echo | value-substituted | governed | opensip.product.provider-startup.1#/$defs/PlanId2 | echo (no v2 field text): OpenUniverse.planId |  | R3-G9 |
| manifestSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | inherited: hex SHA-256(deterministic-CBOR(entries)) over PreparedOutputEntryV2 entries | unresolved | owner-contradictory |  | rust2 $.commitments.preparedOutputManifest |  | R3-G9 |
| entries | required | definite-array | definite-array | inherited: PreparedOutputEntryV2[] 0..maxPreparedOutputEntries 256, contiguous ordinal, rust-v1 row order | unresolved | owner-contradictory |  | field-text | chk2.validate_prepared (inherited v2 law) | R3-G9 |

### payloadSchemas.PreparedOutputChunkV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| planId | required | UTF-8-NFC-text | UTF-8-NFC-text | inherited echo; plan2 substitution not enumerated for this frame | unresolved | owner-missing |  | echo (no v2 field text): manifest |  | R3-G9; R3-G16 |
| outputOrdinal | required | uint64 | uint64 | inherited: manifest outputOrdinal, in ordinal/chunk/offset order | unresolved | owner-contradictory |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G9 |
| chunkIndex | required | uint64 | uint64 | inherited: contiguous from 0 per ordinal | unresolved | owner-contradictory |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G9 |
| byteOffset | required | uint64 | uint64 | inherited: exact cumulative prior bytes | unresolved | owner-contradictory |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G9 |
| bytes | required | byte-string | byte-string | inherited: non-empty; 1..maxPreparedOutputChunkBytes 1048576 | unresolved | owner-contradictory |  | field-text |  | R3-G9; R3-G1 |

### payloadSchemas.PreparedOutputSealV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| planId | required | UTF-8-NFC-text | UTF-8-NFC-text | inherited echo; plan2 substitution not enumerated for this frame | unresolved | owner-missing |  | echo (no v2 field text): manifest |  | R3-G9; R3-G16 |
| manifestSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | inherited: echo of manifest | unresolved | owner-contradictory |  | echo (no v2 field text): manifest |  | R3-G9 |
| entryCount | required | uint64 | uint64 | inherited: exact checked aggregate | unresolved | owner-contradictory |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G9 |
| totalBlobBytes | required | uint64 | uint64 | inherited: exact checked sum; <= maxPreparedOutputTotalBlobBytes 1073741824 | unresolved | owner-contradictory |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G9 |
| totalChunkCount | required | uint64 | uint64 | inherited: exact checked aggregate | unresolved | owner-contradictory |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G9 |

### payloadSchemas.PreparedOutputAcceptedV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| planId | required | UTF-8-NFC-text | UTF-8-NFC-text | PlanId2 ^plan2:[0-9a-f]{64} echo | value-substituted | governed | opensip.product.provider-startup.1#/$defs/PlanId2 | echo (no v2 field text): seal |  | R3-G9 |
| manifestSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | inherited: exact PreparedOutputSeal value | unresolved | owner-contradictory |  | echo (no v2 field text): seal |  | R3-G9 |
| entryCount | required | uint64 | uint64 | inherited: exact PreparedOutputSeal value | unresolved | owner-contradictory |  | echo (no v2 field text): seal |  | R3-G9 |
| totalBlobBytes | required | uint64 | uint64 | inherited: exact PreparedOutputSeal value | unresolved | owner-contradictory |  | echo (no v2 field text): seal |  | R3-G9 |
| totalChunkCount | required | uint64 | uint64 | inherited: exact PreparedOutputSeal value | unresolved | owner-contradictory |  | echo (no v2 field text): seal |  | R3-G9 |

### payloadSchemas.AnalyzeV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | uint64 | uint64; one Analyze per child (protocolIdentity.oneAnalyzePerChild); no exact value stated (TS2 is exactly 0) | retained | governed |  | derived: RustFactBatchV2Vector/fact-batch.3/DispatchBindingV1 analysisOrdinal echoes are Uint64 | dispatch: expectedAnalysisOrdinal |  |
| executionId | required | UTF-8-NFC-text | UTF-8-NFC-text | IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control; exact OpenUniverse echo | retained | governed |  | echo (no v2 field text): OpenUniverse.executionId |  |  |
| snapshotId | required | UTF-8-NFC-text | UTF-8-NFC-text | SnapshotId2 ^snapshot2:[0-9a-f]{64} echo | value-substituted | governed | opensip.product.provider-startup.1#/$defs/SnapshotId2 | echo (no v2 field text): OpenUniverse.snapshotId |  |  |
| planId | required | UTF-8-NFC-text | UTF-8-NFC-text | PlanId2 ^plan2:[0-9a-f]{64} echo | value-substituted | governed | opensip.product.provider-startup.1#/$defs/PlanId2 | echo (no v2 field text): OpenUniverse.planId |  |  |
| stages | required | definite-array | definite-array | items StageRequestV2; 1..maxAnalyzeStages 256; every selected stage (kind fact-derivation, operator semantic-provider, providerId rust-semantic) in exact verified ExecutionPlan order | retained | governed |  | field-text | rp2.planAndDomainProjection selectedStageRule; rp2.transitionAstV2 T015 stageCount |  |

### payloadSchemas.FactBatchV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | uint64 | exact Analyze analysisOrdinal echo | retained | governed | opensip.product.provider-handshake.1#/$defs/RustFactBatchV2Vector/properties/analysisOrdinal | successor vector (no v2 field text) | dispatch: == expectedAnalysisOrdinal; wire.admit_fact_batch: CORRELATION |  |
| stageId | required | UTF-8-NFC-text | UTF-8-NFC-text | StageIdText 1..255 (code points): C-2 stageId text echo of StageRequestV2.planStage.stageId; not stageOrdinal, not retainedStageOrdinal | retained | governed | opensip.product.provider-handshake.1#/$defs/RustFactBatchV2Vector/properties/stageId | successor vector + DispatchBindingV1.expectedStageId maxLength 255 | dispatch: == expectedStageId | R3-G2 |
| batchIndex | required | uint64 | uint64 | contiguous from 0 per stage | retained | governed | opensip.product.provider-handshake.1#/$defs/RustFactBatchV2Vector/properties/batchIndex | successor vector | rp2.transitionAstV2 T016 nextBatchIndex; dispatch: == expectedBatchIndex |  |
| candidates | required | definite-array | definite-array | items FactCandidateV1; 1..maxFactBatchCandidates 4096; candidateOrdinal contiguous from 0 across the stage's batches | retained | governed | opensip.product.provider-handshake.1#/$defs/RustFactBatchV2Vector/properties/candidates | field-text | rp2.transitionAstV2 T016 firstCandidateOrdinal/candidateCount; dispatch: expectedFirstCandidateOrdinal; wire.admit_fact_batch: BATCH_CANDIDATE_CAP; rp2.limitPolicy candidateSpoolAccounting |  |

### payloadSchemas.CoverageV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | uint64 | Uint64 (not const) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/CoverageV3/properties/analysisOrdinal | successor schema |  |  |
| stageId | required | UTF-8-NFC-text | UTF-8-NFC-text | StageIdText; current requested stage; attributes every entry | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/CoverageV3/properties/stageId | successor schema | start.admit_coverage_frame: COVERAGE_STAGE |  |
| entries | required | definite-array | definite-array | items CoverageResultV3; schema 1..4096; count == len(requestedCoverageDomain) <= 256; entries[i] answers keys[i] | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/CoverageV3/properties/entries | field-text | start.admit_coverage_frame: COVERAGE_BIJECTION/COVERAGE_KEY_CORRESPONDENCE; ne.admit_coverage_result_v3 | R3-G8 |
| coverageCommitment | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text over the ordered CoverageResultV3 entries; domain not named by field text | replaced (value-changed) | owner-missing | opensip.product.provider-startup.1#/$defs/CoverageV3/properties/coverageCommitment | field-text |  | R3-G12 |

### payloadSchemas.UnavailableV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | uint64 | Uint64 | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/UnavailableV3/properties/analysisOrdinal | successor schema |  |  |
| affectedStageIds | required | definite-array | definite-array | items StageIdText; all requested stageIds in request order; schema minItems 1, no maxItems (derived <= 256) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/UnavailableV3/properties/affectedStageIds | successor schema description '(inherited)'; no v2 field text |  | R3-G8 |
| reason | required | UTF-8-NFC-text | UTF-8-NFC-text | enum capability-missing\|dependency-source-incomplete\|generated-cfg-unavailable\|identity-version-mismatch\|prepared-output-not-inert\|prepared-output-stale\|semantic-universe-incomplete\|snapshot-resolution-input-missing\|unsupported-compiler-mode (inherited 4; never native-context-mismatch) | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/UnavailableV3/properties/reason | field-text | start.admit_unavailable: pre-Analyze reason refused after Analyze | R3-G7 |
| coverage | required | definite-array | definite-array | items CoverageResultV3 unknown/provider-unavailable, stage-major/key order; schema minItems 0, no maxItems (derived 1..65536) | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/UnavailableV3/properties/coverage | field-text | ne.admit_coverage_result_v3 | R3-G8 |
| coverageCommitment | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text over coverage; domain not named by field text | replaced (value-changed) | owner-missing | opensip.product.provider-startup.1#/$defs/UnavailableV3/properties/coverageCommitment | field-text |  | R3-G12 |

### payloadSchemas.BudgetExhaustedV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | uint64 | Uint64 | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/BudgetExhaustedV3/properties/analysisOrdinal | successor schema |  |  |
| triggerStageId | required | UTF-8-NFC-text | UTF-8-NFC-text | StageIdText; one requested stage whose budget was exhausted | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/BudgetExhaustedV3/properties/triggerStageId | successor schema | rp2.transitionAstV2 T020 budgetMatchesCurrentStage |  |
| unit | required | UTF-8-NFC-text | UTF-8-NFC-text | enum work-units\|bytes\|items; equals the stage budget unit (never milliseconds) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/BudgetExhaustedV3/properties/unit | field-text | rp2.deterministicBudget |  |
| limit | required | uint64 | uint64 | exact requested stage budget limit (C-2 stageBudgetV1 1..9223372036854775807) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/BudgetExhaustedV3/properties/limit | successor schema; c2 v3 $.planIntent.wireTypes.stageBudgetV1 |  |  |
| observed | required | uint64 | uint64 | uint64; relation to limit not stated by the v2 grammar | replaced (unchanged) | owner-missing | opensip.product.provider-startup.1#/$defs/BudgetExhaustedV3/properties/observed | successor schema | rp2.deterministicBudget checked increments | R3-G14 |
| coverage | required | definite-array | definite-array | items CoverageResultV3 unknown/budget-exhausted, stage-major/key order; schema minItems 0, no maxItems | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/BudgetExhaustedV3/properties/coverage | field-text | ne.admit_coverage_result_v3 | R3-G8 |
| coverageCommitment | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text over coverage; domain not named by field text | replaced (value-changed) | owner-missing | opensip.product.provider-startup.1#/$defs/BudgetExhaustedV3/properties/coverageCommitment | field-text |  | R3-G12 |

### payloadSchemas.CompleteV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | uint64 | exact Analyze analysisOrdinal | retained | governed |  | derived (analysisOrdinal echoes are Uint64) |  |  |
| stageResults | required | definite-array | definite-array | items StageResultV2; exactly one per Analyze stage in request order (<= 256) | retained | governed |  | field-text | rp2.candidateAtomicity admitOn valid Complete | R3-G13 |
| factStreamCommitment | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text; domain opensip.rust-provider.fact-stream.v2 over stage-major FactCandidateV1 values, whichever payload carried them | retained | governed |  | rust2 $.commitments.factStream | rp2.commitments factStream |  |
| coverageStreamCommitment | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text; domain opensip.rust-provider.coverage-stream.v2 over stage-major CoverageResultV3 values | value-substituted | governed |  | rust2 $.commitments.coverageStream (field name) | rp2.commitments coverageStream | R3-G12 |

### payloadSchemas.ProviderFaultV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| executionId | required | UNSTATED | UNSTATED | type and nullability unstated (fault is lawful before OpenUniverse) | retained | owner-missing |  | UNSTATED |  | R3-G14 |
| analysisOrdinal | required | UNSTATED | UNSTATED | type and nullability unstated (fault is lawful before Analyze) | retained | owner-missing |  | UNSTATED |  | R3-G14 |
| phase | required | UNSTATED | UNSTATED | no field text; vocabulary unstated | retained | owner-missing |  | UNSTATED |  | R3-G14 |
| faultKind | required | UTF-8-NFC-text | UTF-8-NFC-text | enum compiler-crash\|internal-invariant\|input-rejected | retained | governed |  | field-text |  |  |
| detailCode | required | UNSTATED | UNSTATED | diagnostic only, never D9 authority; normalizes to provider-protocol | retained | owner-missing |  | UNSTATED | rp2.responseProjection typedFault | R3-G14 |

### payloadSchemas.CancelV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| executionId | required | UNSTATED | UNSTATED | type and nullability unstated (Cancel is lawful before OpenUniverse) | retained | owner-missing |  | UNSTATED |  | R3-G14 |
| analysisOrdinal | required | UNSTATED | UNSTATED | type and nullability unstated | retained | owner-missing |  | UNSTATED |  | R3-G14 |
| reason | required | UTF-8-NFC-text | UTF-8-NFC-text | const user-interrupt | retained | governed |  | field-text |  |  |

### payloadSchemas.CancelledV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| executionId | required | UNSTATED | UNSTATED | exact Cancel echo; type unstated | retained | owner-missing |  | echo (no v2 field text): Cancel |  | R3-G14 |
| analysisOrdinal | required | UNSTATED | UNSTATED | exact Cancel echo; type unstated | retained | owner-missing |  | echo (no v2 field text): Cancel |  | R3-G14 |
| observedPhase | required | UTF-8-NFC-text | UTF-8-NFC-text | exact concrete phase at Cancel receipt; phase vocabulary is the 22 major-3 phases (superseded 18); lawful subset unstated | value-substituted | owner-missing |  | field text; protocol3-transitions.v1.json $.phases |  | R3-G14 |

### definitions (records without a member list)

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| IdentityText | required | UTF-8-NFC-text | UTF-8-NFC-text | IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control | retained | governed | opensip.product.provider-handshake.1#/$defs/IdentityText | field-text | rp2.schemaLanguage text byte bound | R3-G2 |
| DigestHex | required | UTF-8-NFC-text | UTF-8-NFC-text | ^[0-9a-f]{64}$ (schema-native end anchor (?![\s\S])) | retained | governed | opensip.product.provider-handshake.1#/$defs/DigestHex | field-text |  |  |
| Sha256Text | required | UTF-8-NFC-text | UTF-8-NFC-text | ^sha256:[0-9a-f]{64}$ | retained | governed | opensip.product.provider-handshake.1#/$defs/Sha256Text | field-text |  |  |
| SnapshotId | required | UTF-8-NFC-text | UTF-8-NFC-text | SnapshotId2 ^snapshot2:[0-9a-f]{64} (inherited ^snap1:sha256:[0-9a-f]{64}$) | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/SnapshotId2 | field-text |  |  |
| PlanId | required | UTF-8-NFC-text | UTF-8-NFC-text | PlanId2 ^plan2:[0-9a-f]{64} (inherited ^plan1:sha256:[0-9a-f]{64}$) | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/PlanId2 | field-text |  |  |
| CanonicalPath | required | UTF-8-NFC-text | UTF-8-NFC-text | NFC slash-relative path; no leading slash, backslash, NUL, drive prefix, empty, dot or dot-dot segment; no schema-native equivalent (native-evidence CanonicalPath pattern is weaker) | retained | governed |  | field-text | rp2.schemaLanguage text rule | R3-G2 |
| RustUniverseV1 | required | definite-text-keyed-map | definite-text-keyed-map | complete external rust-v1 value -> RustSemanticUniverseV2 | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2 | external resolved-inputs.v2 rust-v1 | start.admit_open_universe |  |
| C2PlanStageV3 | required | definite-text-keyed-map | definite-text-keyed-map | exact closed C-2 fact-derivation stage (recursive validation against pinned c2 v3 bytes) | retained | governed |  | external c2-plan-stage-schema.v3 | c2.stageSchemas; rp2.planAndDomainProjection planStageByteRule |  |
| FactCandidateV1 | required | definite-text-keyed-map | definite-text-keyed-map | closed 14-member fact-plane candidate; canonicalRelationPayload is a byte string | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items | external fact-plane candidateSchema | fp.candidate; wire.admit_fact_batch |  |

### definitions.ProtocolLimitsV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| maxFramePayloadBytes | required | uint64 | uint64 | const 67108864; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxFramePayloadBytes | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxSnapshotChunkBytes | required | uint64 | uint64 | const 1048576; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxSnapshotChunkBytes | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxSnapshotEntries | required | uint64 | uint64 | const 200000; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxSnapshotEntries | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxSnapshotTotalFileBytes | required | uint64 | uint64 | const 8589934592; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxSnapshotTotalFileBytes | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxPreparedOutputChunkBytes | required | uint64 | uint64 | const 1048576; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxPreparedOutputChunkBytes | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxPreparedOutputEntries | required | uint64 | uint64 | const 256; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxPreparedOutputEntries | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxPreparedOutputTotalBlobBytes | required | uint64 | uint64 | const 1073741824; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxPreparedOutputTotalBlobBytes | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxAnalyzeStages | required | uint64 | uint64 | const 256; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxAnalyzeStages | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxRelationsPerStage | required | uint64 | uint64 | const 64; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxRelationsPerStage | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxSubjectsPerStage | required | uint64 | uint64 | const 256; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxSubjectsPerStage | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxRequestedCoverageKeysPerStage | required | uint64 | uint64 | const 256; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxRequestedCoverageKeysPerStage | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxFactBatchCandidates | required | uint64 | uint64 | const 4096; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxFactBatchCandidates | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxFactCandidatesTotal | required | uint64 | uint64 | const 1000000; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxFactCandidatesTotal | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxCanonicalRelationPayloadBytes | required | uint64 | uint64 | const 1048576; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxCanonicalRelationPayloadBytes | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxCoverageEntriesPerFrame | required | uint64 | uint64 | const 4096; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxCoverageEntriesPerFrame | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxCandidateSpoolBytes | required | uint64 | uint64 | const 1073741824; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxCandidateSpoolBytes | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxRequestPayloadBytesTotal | required | uint64 | uint64 | const 9663676416; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxRequestPayloadBytesTotal | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxResponsePayloadBytesTotal | required | uint64 | uint64 | const 1073741824; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxResponsePayloadBytesTotal | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxRequestFrames | required | uint64 | uint64 | const 1000000; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxRequestFrames | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxResponseFrames | required | uint64 | uint64 | const 1000000; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxResponseFrames | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxStderrBytes | required | uint64 | uint64 | const 262144; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxStderrBytes | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| maxScratchBytes | required | uint64 | uint64 | const 2147483648; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxScratchBytes | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| cancellationGraceMilliseconds | required | uint64 | uint64 | const 5000; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/cancellationGraceMilliseconds | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |
| normalExitGraceMilliseconds | required | uint64 | uint64 | const 5000; identical in ProtocolLimitsV3 | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/normalExitGraceMilliseconds | rule 'every member is uint64' + top-level $.limits | rp2.limitsHandshake; rp2.limitPolicy |  |

### definitions.ExpectedRustIdentityV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| protocolMajor | required | uint64 | uint64 | exactly 3 (inherited exactly 2) | replaced (value-changed) | governed | opensip.product.provider-handshake.1#/$defs/ExpectedRustIdentityV3/properties/protocolMajor | field-text |  |  |
| providerBuildId | required | UTF-8-NFC-text | UTF-8-NFC-text | IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control; selected Plan rust-v1 row value | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ExpectedRustIdentityV3/properties/providerBuildId | successor schema (inherited fields.remaining 'exact verified release/rust-v1 identity') |  |  |
| rustCommitHash | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ExpectedRustIdentityV3/properties/rustCommitHash | successor schema; rust-v1 digestFields |  |  |
| hostTriple | required | UTF-8-NFC-text | UTF-8-NFC-text | IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ExpectedRustIdentityV3/properties/hostTriple | successor schema |  |  |
| targetTriple | required | UTF-8-NFC-text | UTF-8-NFC-text | IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ExpectedRustIdentityV3/properties/targetTriple | successor schema |  |  |
| sysrootDigest | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex | replaced (unchanged) | governed | opensip.product.provider-handshake.1#/$defs/ExpectedRustIdentityV3/properties/sysrootDigest | successor schema; rust-v1 digestFields |  |  |

### definitions.RustProviderCapabilityV2

Inherited external: `resolved-inputs-rust-provider-join.v2.json#capabilityHandshakeBinding`

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| providerId | required | UTF-8-NFC-text |  | member removed: the record is replaced by the RustCapabilitiesV3 token array | replaced (removed) | governed | opensip.product.provider-handshake.1#/$defs/RustCapabilitiesV3 | resolved-inputs-rust-provider-join.v2 $.capabilityHandshakeBinding.fields |  |  |
| language | required | UTF-8-NFC-text |  | member removed: the record is replaced by the RustCapabilitiesV3 token array | replaced (removed) | governed | opensip.product.provider-handshake.1#/$defs/RustCapabilitiesV3 | resolved-inputs-rust-provider-join.v2 $.capabilityHandshakeBinding.fields |  |  |
| providerVersionSource | required | UTF-8-NFC-text |  | member removed: the record is replaced by the RustCapabilitiesV3 token array | replaced (removed) | governed | opensip.product.provider-handshake.1#/$defs/RustCapabilitiesV3 | resolved-inputs-rust-provider-join.v2 $.capabilityHandshakeBinding.fields |  |  |
| toolchainIdentitySource | required | UTF-8-NFC-text |  | member removed: the record is replaced by the RustCapabilitiesV3 token array | replaced (removed) | governed | opensip.product.provider-handshake.1#/$defs/RustCapabilitiesV3 | resolved-inputs-rust-provider-join.v2 $.capabilityHandshakeBinding.fields |  |  |
| relations | required | definite-text-keyed-map |  | member removed: the record is replaced by the RustCapabilitiesV3 token array | replaced (removed) | governed | opensip.product.provider-handshake.1#/$defs/RustCapabilitiesV3 | resolved-inputs-rust-provider-join.v2 $.capabilityHandshakeBinding.fields |  |  |
| platformIds | required | definite-array |  | member removed: the record is replaced by the RustCapabilitiesV3 token array | replaced (removed) | governed | opensip.product.provider-handshake.1#/$defs/RustCapabilitiesV3 | resolved-inputs-rust-provider-join.v2 $.capabilityHandshakeBinding.fields |  |  |

### definitions.ToolPathV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| artifact_id | required | UTF-8-NFC-text |  | no Rust3 provider-wire carrier: RepositoryResolutionV3 is closed without toolPaths (the shape survives only as C-2 grant parameters, off this wire) | removed (removed) | governed |  | field text |  |  |
| bundle_relative_path | required | UTF-8-NFC-text |  | no Rust3 provider-wire carrier: RepositoryResolutionV3 is closed without toolPaths (the shape survives only as C-2 grant parameters, off this wire) | removed (removed) | governed |  | field text |  |  |
| file_sha256 | required | UTF-8-NFC-text |  | no Rust3 provider-wire carrier: RepositoryResolutionV3 is closed without toolPaths (the shape survives only as C-2 grant parameters, off this wire) | removed (removed) | governed |  | field text |  |  |
| role | required | UTF-8-NFC-text |  | no Rust3 provider-wire carrier: RepositoryResolutionV3 is closed without toolPaths (the shape survives only as C-2 grant parameters, off this wire) | removed (removed) | governed |  | field text |  |  |

### definitions.RepositoryResolutionV2

Inherited variants: {"disabled": "mode=disabled; grantId and commitment null; network=false; output/tool arrays empty", "prepared": "mode=prepared; grantId non-null; network=false; output rows exact rust-v1; toolPaths exact tag-10 tool_paths; commitment equals deterministic prepared manifest reconstructed from committed blobs"}

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| mode | required | UTF-8-NFC-text |  | enum disabled\|prepared; removed (prepared mode is now preparedOutputSetId != null, host-derived) | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3 | variants text |  |  |
| grantId | required | UTF-8-NFC-text\|null |  | removed (no stated successor; authorizationId is a new member, not declared a rename) | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3 | variants text |  |  |
| projectId | required | UTF-8-NFC-text |  | removed | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3 | resolved-inputs-rust-provider-join.v2 providerRequestProjection |  |  |
| network | required | bool | definite-text-keyed-map\|null | false; replaced by disclosed effects copied from AuthorizedExecutionV2 (effects.network is an EffectV1) | replaced (moved) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3/properties/effects | variants text |  |  |
| buildScriptOutputs | required | definite-array |  | removed (rust-v1 rows superseded) | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3 | variants text |  |  |
| procMacroOutputs | required | definite-array |  | removed (rust-v1 rows superseded) | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3 | variants text |  |  |
| toolPaths | required | definite-array |  | removed | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3 | variants text |  |  |
| preparedOutputManifestCommitment | required | UTF-8-NFC-text\|null |  | removed | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3 | variants text; resolved-inputs-rust-provider-join.v2 preparedOutputManifestBinding.manifestCommitment |  |  |

### definitions.SnapshotEntryV2

Inherited variants: {"file": "byteLength/digest/executable non-null; targetBytes null", "symlink": "targetBytes non-empty; other variant fields null"}

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| path | required | UTF-8-NFC-text | UTF-8-NFC-text | CanonicalPath; entries strict ascending unique by UTF-8 bytes | retained | governed |  | SnapshotManifestV2.fields.entries |  |  |
| kind | required | UTF-8-NFC-text | UTF-8-NFC-text | enum file\|symlink | retained | governed |  | variants keys |  |  |
| byteLength | required | uint64\|null | uint64\|null | file: non-null content length; symlink: null | retained | governed |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text; subjectsAlgorithm 'byteLength is greater than zero' |  | R3-G15 |
| contentSha256 | required | UNSTATED\|null | UNSTATED\|null | file: non-null digest (form unstated; enters SubjectV2.subjectId preimage); symlink: null | retained | owner-missing |  | UNSTATED (variants give nullability only) |  | R3-G15 |
| executable | required | UNSTATED\|null | UNSTATED\|null | file: non-null; symlink: null | retained | owner-missing |  | UNSTATED (variants give nullability only) |  | R3-G15 |
| targetBytes | required | UNSTATED\|null | UNSTATED\|null | symlink: non-empty target (requestProjection.snapshot 'symlink target bytes remain in the manifest'); file: null | retained | owner-missing |  | UNSTATED (CBOR type not stated) |  | R3-G15; R3-G1 |

### definitions.PreparedOutputBlobV2

Inherited variants: {"build-script": "ownerId equals the rust-v1 row packageId and configuration equals its exact cfg array", "proc-macro": "ownerId equals the rust-v1 row crateId and configuration is the empty array"}

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| kind | required | UTF-8-NFC-text | UTF-8-NFC-text | inherited enum build-script\|proc-macro (PreparedOutputRowV3 kinds differ) | unresolved | owner-contradictory |  | variants keys |  | R3-G9 |
| ownerId | required | UTF-8-NFC-text | UTF-8-NFC-text | inherited: rust-v1 row packageId or crateId (rows superseded) | unresolved | owner-contradictory |  | variants text |  | R3-G9 |
| configuration | required | definite-array | definite-array | inherited: exact rust-v1 cfg array or [] | unresolved | owner-contradictory |  | variants text |  | R3-G9 |
| content | required | byte-string | byte-string | inherited: exact byte string, possibly empty | unresolved | owner-contradictory |  | field-text |  | R3-G9; R3-G1 |

### definitions.PreparedOutputEntryV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| outputOrdinal | required | uint64 | uint64 | inherited: contiguous from 0; build-script rows then proc-macro rows | unresolved | owner-contradictory |  | field-text |  | R3-G9 |
| kind | required | UTF-8-NFC-text | UTF-8-NFC-text | inherited: build-script\|proc-macro | unresolved | owner-contradictory |  | PreparedOutputBlobV2 variants |  | R3-G9 |
| planRow | required | definite-text-keyed-map | definite-text-keyed-map | inherited: exact rust-v1 row (superseded by rust-v2) | unresolved | owner-contradictory |  | field-text |  | R3-G9 |
| logicalPath | required | UTF-8-NFC-text | UTF-8-NFC-text | inherited: .opensip/prepared/v2/<ordinal>-<planRow.outputDigest>.blob | unresolved | owner-contradictory |  | field-text |  | R3-G9 |
| blobByteLength | required | uint64 | uint64 | inherited: exact deterministic-CBOR blob length | unresolved | owner-contradictory |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G9 |
| blobSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | inherited: DigestHex of exact blob bytes == planRow.outputDigest | unresolved | owner-contradictory |  | field-text |  | R3-G9 |
| contentByteLength | required | uint64 | uint64 | inherited: exact content length | unresolved | owner-contradictory |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G9 |
| contentSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | inherited: SHA-256 of exact content bytes | unresolved | owner-contradictory |  | field-text |  | R3-G9 |

### definitions.SubjectV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| subjectOrdinal | required | uint64 | uint64 | contiguous from 0 in path order | retained | governed |  | rust2 subjectsAlgorithm | chk2.derive_subjects |  |
| subjectId | required | UTF-8-NFC-text | UTF-8-NFC-text | 'rust-file:sha256:' + hex(SHA-256(UTF8(opensip.rust-provider.subject.v2) \|\| 0x00 \|\| deterministic-CBOR({snapshotId, path, contentSha256, byteLength}))); the snapshotId input becomes snapshot2 text | value-substituted | owner-missing |  | rust2 subjectsAlgorithm | chk2.derive_subjects | R3-G16 |
| path | required | UTF-8-NFC-text | UTF-8-NFC-text | CanonicalPath of a non-empty .rs file entry | retained | governed |  | rust2 subjectsAlgorithm |  |  |
| startByte | required | uint64 | uint64 | exactly 0 | retained | governed |  | rust2 subjectsAlgorithm |  |  |
| endByte | required | uint64 | uint64 | entry byteLength (> 0) | retained | governed |  | rust2 subjectsAlgorithm |  |  |

### definitions.CoverageKeyV2

Inherited external: `c2-plan-stage-schema.v3.json#coverageKey.key`

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| relation | required | UTF-8-NFC-text | UTF-8-NFC-text | one planStage.relations member (C-2 order); fact-plane registry | retained | governed |  | c2 v3 coverageKey.key + rust2 coverageDomainAlgorithm | rp2.planAndDomainProjection coverageDomainAlgorithm; fp.registry | R3-G7 |
| resolution | required | UTF-8-NFC-text | UTF-8-NFC-text | every rung of the relation's fact-plane ladder, weakest first | retained | governed |  | rust2 coverageDomainAlgorithm |  | R3-G7 |
| sourceUniverseId | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text; native semantic-universe identity sha256:hex(H(native.semantic-universe.rust.v2, universe.resolvedInputs)) (inherited opensip.rust-provider.universe.v2 recipe superseded) | value-substituted | governed |  | rust2 coverageDomainAlgorithm | start.admit_coverage_frame: sourceUniverse suffix join | R3-G7 |
| targetUniverseId | required | UTF-8-NFC-text | UTF-8-NFC-text | native semantic-universe identity of each target: [source] for same-only, else the admitted target set (inherited opensip.semantic-universe.v2 recipe superseded) | value-substituted | governed |  | rust2 coverageDomainAlgorithm | start.admit_coverage_frame: targetUniverse suffix join | R3-G7 |
| subjectScopeCommitment | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text; value recipe contested (rust2 per-stage subjectScope vs §4.1a per-key scope2) | retained | owner-contradictory |  | rust2 $.commitments.subjectScope | ne.admit_coverage_result_v3; ne.subject_scope_commitment | R3-G4; R3-G7 |
| producer | required | UTF-8-NFC-text | UTF-8-NFC-text | const rust-semantic | retained | governed |  | rust2 coverageDomainAlgorithm |  |  |
| producerVersion | required | UTF-8-NFC-text | UTF-8-NFC-text | verified providerBuildId (HelloV3.expectedIdentity.providerBuildId) | retained | governed |  | rust2 coverageDomainAlgorithm |  |  |
| schemaVersion | required | uint64 | uint64 | the relation payload registry schemaVersion | retained | governed |  | rust2 coverageDomainAlgorithm |  |  |

### definitions.StageAnalysisDomainV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| subjects | required | definite-array | definite-array | items SubjectV2; 1..maxSubjectsPerStage 256; identical for every selected stage | retained | governed |  | rust2 subjectsAlgorithm | chk2.validate_domain; rij.analysisDomainBinding |  |
| requestedCoverageDomain | required | definite-array | definite-array | items CoverageKeyV2 (rust2, 8 members); 1..maxRequestedCoverageKeysPerStage 256; canonical nested-loop order relation/rung/target (not sorted); duplicates refuse | retained | governed |  | rust2 coverageDomainAlgorithm | chk2.validate_domain; rp2.planAndDomainProjection wireRule | R3-G4 |
| domainCommitment | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text; opensip.rust-provider.analysis-domain.v2 over {subjects, requestedCoverageDomain}; recipe retained, committed value changes with substituted keys | value-substituted | governed |  | rust2 $.commitments.analysisDomain | chk2.validate_domain | R3-G4 |

### definitions.StageRequestV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| stageOrdinal | required | uint64 | uint64 | contiguous 0..n-1 in THIS Analyze order (== DispatchBindingV1.analyzeRequestOrdinal; never assumed == retainedStageOrdinal) | retained | governed |  | field text 'contiguous Analyze order' | dispatch: analyzeRequestOrdinal |  |
| planStage | required | definite-text-keyed-map | definite-text-keyed-map | C2PlanStageV3: exact nested C-2 stage bytes; optional C-2 members present only when present in the ExecutionPlan | retained | governed |  | field-text | rp2.planAndDomainProjection planStageByteRule |  |
| analysisDomain | required | definite-text-keyed-map | definite-text-keyed-map | StageAnalysisDomainV2: exact host reconstruction | retained | governed |  | field-text | rp2.planAndDomainProjection wireRule; chk2.validate_domain |  |

### definitions.CoverageResultV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| stageId | required | UTF-8-NFC-text | UTF-8-NFC-text | moved to the CoverageV3 wrapper stageId | replaced (moved) | governed | opensip.product.provider-startup.1#/$defs/CoverageV3/properties/stageId | field-text |  |  |
| entryOrdinal | required | uint64 |  | removed: array index i of entries answers requestedCoverageDomain.keys[i] | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3 | derived: rust2 deterministicBudget 'Coverage entryOrdinal' | start.admit_coverage_frame: positional bijection |  |
| coverageState | required | UTF-8-NFC-text | UTF-8-NFC-text | -> entry.coverage enum complete\|unknown (RC-6: complete requires examinedExhaustive) | replaced (moved) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/ViewEntryV3/properties/coverage | field-text | ne.admit_coverage_result_v3 |  |
| key | required | definite-text-keyed-map | definite-text-keyed-map | -> key CoverageKeyV2 (native-evidence, 5 members: relation, resolution, sourceUniverse, targetUniverse bare 64-hex, subjectScopeCommitment) | replaced (value-changed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageKeyV2 | field-text | start.admit_coverage_frame: equals keys[i] by suffix projection; ne.admit_coverage_result_v3 §4.1a steps 1-4 | R3-G4; R3-G7 |
| deficiency | required | UTF-8-NFC-text\|null | UTF-8-NFC-text\|null | -> entry.deficiency DeficiencyV2 (9 values) \| null (inherited: null \| provider-unavailable \| budget-exhausted) | replaced (moved) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/ViewEntryV3/properties/deficiency | field-text |  |  |

### definitions.StageResultV2

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| stageId | required | UTF-8-NFC-text | UTF-8-NFC-text | exact requested stage id (StageIdText by echo) | retained | owner-missing |  | echo (no v2 field text): planStage.stageId (fields.all) |  | R3-G13 |
| factCount | required | uint64 | uint64 | exact recomputed candidate count | retained | owner-missing |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G13 |
| coverageEntryCount | required | uint64 | uint64 | exact recomputed CoverageResultV3 entry count | retained | owner-missing |  | derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text |  | R3-G13 |
| factCommitment | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text; opensip.rust-provider.stage-facts.v2 over the stage's ordered FactCandidateV1 values, whichever payload carried them | retained | owner-missing |  | rust2 $.commitments.stageFacts (field name) | rp2.commitments stageFacts | R3-G13 |
| coverageCommitment | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text; stageCoverage recipe/domain unchanged over CoverageResultV3 values (§9.7) | value-substituted | owner-missing |  | rust2 $.commitments.stageCoverage (field name) | rp2.commitments stageCoverage | R3-G12; R3-G13 |

## 9. External expansions (members reached through `external` definitions)

### C2PlanStageV3 (source `docs/coop/artifacts/c2-plan-stage-schema.v3.json` $.stageSchemas.common / $.stageSchemas.kinds.fact-derivation)

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| kind | required | UTF-8-NFC-text | UTF-8-NFC-text | const fact-derivation | retained | governed |  | c2 v3 $.stageSchemas.common.required | rp2.planAndDomainProjection selectedStageRule |  |
| stageId | required | UTF-8-NFC-text | UTF-8-NFC-text | C-2 stageId text; unique; 1..255 by DispatchBindingV1.expectedStageId (which names StageRequestV2.planStage.stageId); c2 v3 states no type/bound | retained | governed |  | c2 v3 $.stageSchemas.common.required; dispatch-binding expectedStageId | dispatch: expectedStageId | R3-G2 |
| dependsOn | optional | definite-array | definite-array | optional; stageId texts of earlier stages | retained | governed |  | c2 v3 $.stageSchemas.common.optional; workflow.stages text |  |  |
| budget | optional | definite-text-keyed-map | definite-text-keyed-map | optional; stageBudgetV1 {unit work-units\|milliseconds\|bytes\|items, limit 1..9223372036854775807} | retained | governed |  | c2 v3 $.stageSchemas.common.optional; c2 v3 planIntent.wireTypes.stageBudgetV1 | rp2.deterministicBudget |  |
| relations | required | definite-array | definite-array | fact-plane registry relation names; <= maxRelationsPerStage 64 | retained | governed |  | c2 v3 $.stageSchemas.kinds.fact-derivation.required | fp.registry |  |
| operator | required | UTF-8-NFC-text | UTF-8-NFC-text | const semantic-provider for selected stages (C-2 enum builtin-extractor\|semantic-provider\|external-scanner) | retained | governed |  | c2 v3 $.stageSchemas.kinds.fact-derivation.operatorAuthority |  |  |
| capabilityGrants | optional | definite-array | definite-array | optional; AdmissionDescriptorV1.capabilityGrants[*].grantId texts | retained | governed |  | c2 v3 $.stageSchemas.kinds.fact-derivation.optional |  |  |
| providerId | optional | UTF-8-NFC-text | UTF-8-NFC-text | optional in C-2; const rust-semantic for every selected stage | retained | governed |  | c2 v3 $.stageSchemas.kinds.fact-derivation.optional; selectedStageRule |  |  |

### FactCandidateV1 (source `docs/coop/artifacts/fact-plane.v1.json` $.factRecordContractV1.candidateSchema.fields)

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| candidateOrdinal | required | uint64 | uint64 | contiguous within the attributed stage from 0 (resets each stage); transport-only | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/candidateOrdinal | field-text | rp2.transitionAstV2 T016/T017; dispatch: expectedFirstCandidateOrdinal |  |
| relation | required | UTF-8-NFC-text | UTF-8-NFC-text | requested by the stage; registry key | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/relation | field-text | fp.registry |  |
| resolution | required | UTF-8-NFC-text | UTF-8-NFC-text | rung of the relation's ladder | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/resolution | field-text | fp.registry |  |
| layer | required | UTF-8-NFC-text | UTF-8-NFC-text | the relation's registry layer | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/layer | field-text | fp.registry |  |
| producer | required | UTF-8-NFC-text | UTF-8-NFC-text | const rust-semantic | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/producer | field-text |  |  |
| producerVersion | required | UTF-8-NFC-text | UTF-8-NFC-text | verified providerBuildId (HelloV3.expectedIdentity.providerBuildId) | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/producerVersion | field-text |  |  |
| schemaVersion | required | uint64 | uint64 | exact host registry schemaVersion | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/schemaVersion | field-text | fp.candidate |  |
| language | required | UTF-8-NFC-text | UTF-8-NFC-text | const rust | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/language | field-text |  |  |
| sourceUniverseId | required | UTF-8-NFC-text | UTF-8-NFC-text | Sha256Text; native rust v2 semantic-universe identity (== OpenUniverse universe identity) | value-substituted | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/sourceUniverseId | field-text |  | R3-G7 |
| targetUniverseId | required | UTF-8-NFC-text | UTF-8-NFC-text | native semantic-universe identity of a host-admitted target; same-only relations require == source | value-substituted | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/targetUniverseId | field-text |  | R3-G7 |
| confidenceMillionths | required | uint64 | uint64 | 0..1000000 | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/confidenceMillionths | field-text |  |  |
| relationSchemaId | required | UTF-8-NFC-text | UTF-8-NFC-text | exact host registry schemaId | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/relationSchemaId | field-text | fp.candidate |  |
| canonicalRelationPayload | required | byte-string | byte-string | deterministic-CBOR bytes; <= maxCanonicalRelationPayloadBytes 1048576; decode once, re-encode equal | retained | governed |  | wireAdjustment 'canonicalRelationPayload is a byte string' | fp.candidate; wire.admit_fact_batch: CANDIDATE_PAYLOAD_BOUND | R3-G1 |
| anchors | required | definite-array | definite-array | items AnchorRefV1; non-empty; sorted ascending by CVE1(anchor) bytes, unique (vector maxItems 4096) | retained | governed | opensip.product.fact-batch.3#/properties/candidates/items/properties/anchors | field-text | fp.anchor | R3-G5 |

### AnchorRefV1 (source `docs/coop/artifacts/fact-plane.v1.json` $.factRecordContractV1.anchorSchema)

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| kind | required | UTF-8-NFC-text | UTF-8-NFC-text | enum source-span\|fact-ref | retained | governed |  | anchorSchema.variants keys | fp.anchor |  |
| snapshotId | required | UNSTATED\|null | UNSTATED\|null | source-span: non-null; fact-ref: null; snapshot2 substitution not enumerated | retained | owner-missing |  | UNSTATED |  | R3-G5; R3-G16 |
| path | required | UTF-8-NFC-text\|null | UTF-8-NFC-text\|null | source-span: normalized project-relative NFC path of a sealed file; fact-ref: null | retained | governed |  | fact-plane sourceSpanSchema.rule |  | R3-G5 |
| contentSha256 | required | UNSTATED\|null | UNSTATED\|null | source-span: sealed file digest (form unstated); fact-ref: null | retained | owner-missing |  | UNSTATED |  | R3-G5 |
| startByte | required | UNSTATED\|null | UNSTATED\|null | source-span: [startByte,endByte) non-empty in bounds; fact-ref: null | retained | owner-missing |  | UNSTATED |  | R3-G5 |
| endByte | required | UNSTATED\|null | UNSTATED\|null | as startByte | retained | owner-missing |  | UNSTATED |  | R3-G5 |
| factId | required | UNSTATED\|null | UNSTATED\|null | fact-ref: FACT-ID-V1 (conflicts with mandatory fact2); source-span: null | retained | owner-contradictory |  | UNSTATED |  | R3-G5 |

### RustUniverseV1 (source `docs/coop/artifacts/resolved-inputs.v2.json` $.planIdContract.semanticUniverseSchemas.rust-v1.required)

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| schemaVersion | required | uint64 | uint64 | const 1 | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/schemaVersion | rust-v1 constants |  |  |
| manifestId | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex (64 lowercase hex) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/manifestId | rust-v1 digestFields/digestRepresentation |  |  |
| capabilityManifestId | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex (64 lowercase hex) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/capabilityManifestId | rust-v1 digestFields/digestRepresentation |  |  |
| providerArtifactId | required | UTF-8-NFC-text | UTF-8-NFC-text | const rust-provider | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/providerArtifactId | rust-v1 constants |  |  |
| providerArtifactSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex (64 lowercase hex) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/providerArtifactSha256 | rust-v1 digestFields/digestRepresentation |  |  |
| toolchainArtifactId | required | UTF-8-NFC-text | UTF-8-NFC-text | const rust-toolchain-bundle | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/toolchainArtifactId | rust-v1 constants |  |  |
| toolchainArtifactSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex (64 lowercase hex) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/toolchainArtifactSha256 | rust-v1 digestFields/digestRepresentation |  |  |
| protocolMajor | required | UNSTATED | uint64 | const 3 (rust-v1 states no constant; deliveryJoin equals the handshake) | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/protocolMajor | successor schema | start.admit_open_universe: handshakeJoin |  |
| providerBuildId | required | UNSTATED | UTF-8-NFC-text | NfcText (non-empty; NFC by admission); rust-v1 states no text type | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/providerBuildId | successor schema | start.admit_open_universe: handshakeJoin (IdentityText in HelloV3 vs NfcText here; equality closes the bound) |  |
| rustCommitHash | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex (64 lowercase hex) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/rustCommitHash | rust-v1 digestFields/digestRepresentation |  |  |
| rustcVersion | required | UNSTATED | UTF-8-NFC-text | NfcText (non-empty; NFC by admission); rust-v1 states no text type | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/rustcVersion | successor schema |  |  |
| cargoVersion | required | UNSTATED | UTF-8-NFC-text | NfcText (non-empty; NFC by admission); rust-v1 states no text type | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/cargoVersion | successor schema |  |  |
| hostTriple | required | UNSTATED | UTF-8-NFC-text | NfcText (non-empty; NFC by admission); rust-v1 states no text type | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/hostTriple | successor schema | start.admit_open_universe: handshakeJoin (IdentityText in HelloV3 vs NfcText here; equality closes the bound) |  |
| targetTriple | required | UNSTATED | UTF-8-NFC-text | NfcText (non-empty; NFC by admission); rust-v1 states no text type | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/targetTriple | successor schema | start.admit_open_universe: handshakeJoin (IdentityText in HelloV3 vs NfcText here; equality closes the bound) |  |
| sysrootDigest | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex (64 lowercase hex) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/sysrootDigest | rust-v1 digestFields/digestRepresentation |  |  |
| rustcDevLlvmDigest | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex (64 lowercase hex) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/rustcDevLlvmDigest | rust-v1 digestFields/digestRepresentation |  |  |
| standardLibraryComponentDigests | required | definite-text-keyed-map | definite-text-keyed-map | open map: component name -> DigestHex | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/standardLibraryComponentDigests | rust-v1 digestRepresentation |  |  |
| providerBinarySha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex (64 lowercase hex) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/providerBinarySha256 | rust-v1 digestFields/digestRepresentation |  |  |
| licenseNoticeBundleSha256 | required | UTF-8-NFC-text | UTF-8-NFC-text | DigestHex (64 lowercase hex) | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/licenseNoticeBundleSha256 | rust-v1 digestFields/digestRepresentation |  |  |
| platformId | required | UNSTATED | UTF-8-NFC-text | NfcText (non-empty; NFC by admission); rust-v1 states no text type | replaced (unchanged) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/platformId | successor schema |  |  |
| resolvedInputs | required | definite-text-keyed-map | definite-text-keyed-map | RustUniverseV2ResolvedInputs (14 members; wholesale supersession) | replaced (value-changed) | governed | opensip.product.provider-startup.1#/$defs/RustSemanticUniverseV2/properties/resolvedInputs | field-text |  |  |

### RustUniverseV1.resolvedInputs (source `docs/coop/artifacts/resolved-inputs.v2.json` $.planIdContract.semanticUniverseSchemas.rust-v1.resolvedInputs.required)

| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| edition | required | UNSTATED |  | same-name member of RustUniverseV2ResolvedInputs; wholesale supersession, equality not asserted | replaced (value-changed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/edition | resolved-inputs.v2 rust-v1.resolvedInputs text |  |  |
| cfg | required | definite-array |  | removed by wholesale supersession (no rename is stated) | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs | resolved-inputs.v2 rust-v1.resolvedInputs text |  |  |
| packageLockIdentity | required | definite-array |  | removed by wholesale supersession (no rename is stated) | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs | resolved-inputs.v2 rust-v1.resolvedInputs text |  |  |
| resolvedPackages | required | definite-array |  | removed by wholesale supersession (no rename is stated) | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs | resolved-inputs.v2 rust-v1.resolvedInputs text |  |  |
| rustflags | required | definite-array |  | same-name member of RustUniverseV2ResolvedInputs; wholesale supersession, equality not asserted | replaced (value-changed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/rustflags | resolved-inputs.v2 rust-v1.resolvedInputs text |  |  |
| crateRootPaths | required | definite-array |  | same-name member of RustUniverseV2ResolvedInputs; wholesale supersession, equality not asserted | replaced (value-changed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/crateRootPaths | resolved-inputs.v2 rust-v1.resolvedInputs text |  |  |
| executionCapableResolution | required | bool |  | same-name member of RustUniverseV2ResolvedInputs; wholesale supersession, equality not asserted | replaced (value-changed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/executionCapableResolution | resolved-inputs.v2 rust-v1.resolvedInputs text |  |  |
| buildScriptOutputs | required | definite-array |  | removed by wholesale supersession (no rename is stated) | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs | resolved-inputs.v2 rust-v1.resolvedInputs text |  |  |
| procMacroOutputs | required | definite-array |  | removed by wholesale supersession (no rename is stated) | replaced (removed) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs | resolved-inputs.v2 rust-v1.resolvedInputs text |  |  |

## 10. New schema-native members on the Rust3 wire

| record.member | Rust3 wire | bounds / vocabulary | class | ref / source | semantic-owner checks | gaps |
|---|---|---|---|---|---|---|
| HelloV3.protocolMajor | uint64 | const 3 (kept from the superseded native-evidence.schemas.v2 HelloV3) | governed | opensip.product.provider-handshake.1#/$defs/HelloV3/properties/protocolMajor | wire.admit_hello |  |
| HelloV3.identityVersions | definite-text-keyed-map | IdentityVersionsV1 {snapshot:2, plan:2, fact:2, coverage:3} | governed | opensip.product.provider-handshake.1#/$defs/HelloV3/properties/identityVersions |  |  |
| HelloAckV3.identityVersions | definite-text-keyed-map | exact echo of Hello identityVersions | governed | opensip.product.provider-handshake.1#/$defs/HelloAckV3/properties/identityVersions | wire.admit_hello_ack: IDENTITY_VERSIONS_ECHO |  |
| ProtocolLimitsV3.maxDependencySourcePackages | uint64 | const 4096 | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxDependencySourcePackages | rp2.limitsHandshake |  |
| ProtocolLimitsV3.maxDependencySourceEntries | uint64 | const 1000000 | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxDependencySourceEntries | rp2.limitsHandshake |  |
| ProtocolLimitsV3.maxDependencySourceTotalBytes | uint64 | const 8589934592 | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxDependencySourceTotalBytes | rp2.limitsHandshake |  |
| ProtocolLimitsV3.maxDependencySourceChunkBytes | uint64 | const 1048576 | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxDependencySourceChunkBytes | rp2.limitsHandshake |  |
| ProtocolLimitsV3.maxUnresolvedEdgesPerStage | uint64 | const 1000000 | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxUnresolvedEdgesPerStage | rp2.limitsHandshake |  |
| ProtocolLimitsV3.maxCfgSets | uint64 | const 4 | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxCfgSets | rp2.limitsHandshake |  |
| ProtocolLimitsV3.maxExpansionRows | uint64 | const 1000000 | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxExpansionRows | rp2.limitsHandshake |  |
| ProtocolLimitsV3.maxGeneratedFileRows | uint64 | const 1000000 | governed | opensip.product.provider-handshake.1#/$defs/ProtocolLimitsV3/properties/maxGeneratedFileRows | rp2.limitsHandshake |  |
| RustUniverseV2ResolvedInputs.schemaVersion | uint64 | const 2 | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/schemaVersion |  |  |
| RustUniverseV2ResolvedInputs.edition | definite-text-keyed-map | open map -> integer 2015\|2018\|2021\|2024 | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/edition |  |  |
| RustUniverseV2ResolvedInputs.lockfileIdentity | definite-text-keyed-map | LockfileIdentityV1 | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/lockfileIdentity |  |  |
| RustUniverseV2ResolvedInputs.dependencySourceSetId | UTF-8-NFC-text | Sha256Text (native.dependency-source-set.v1) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/dependencySourceSetId |  |  |
| RustUniverseV2ResolvedInputs.unifiedFeaturesId | UTF-8-NFC-text | Sha256Text (native.unified-features.rust.v1) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/unifiedFeaturesId |  |  |
| RustUniverseV2ResolvedInputs.nativeContextId | UTF-8-NFC-text | Sha256Text (native.context.rust.v2); suffix in plan.nativeContextDigests | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/nativeContextId | start.admit_open_universe |  |
| RustUniverseV2ResolvedInputs.cfgSets | definite-array | 1..4 {cfgSetId, cfg} | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/cfgSets |  |  |
| RustUniverseV2ResolvedInputs.rustflags | definite-text-keyed-map | RustflagsProjectionV1 | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/rustflags |  |  |
| RustUniverseV2ResolvedInputs.crateRootPaths | definite-array | 0..100000 CanonicalPath, utf8 order | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/crateRootPaths |  |  |
| RustUniverseV2ResolvedInputs.configProjectionSha256 | UTF-8-NFC-text | bare 64-hex suffix of H(native.cargo-config-projection.v2, ...) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/configProjectionSha256 |  |  |
| RustUniverseV2ResolvedInputs.executionCapableResolution | bool | prepared products consumed as inert data only | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/executionCapableResolution |  |  |
| RustUniverseV2ResolvedInputs.preparedOutputSetId | UTF-8-NFC-text\|null | Sha256Text (native.prepared-output-set.v3) \| null | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/preparedOutputSetId |  |  |
| RustUniverseV2ResolvedInputs.preparedResolution | UTF-8-NFC-text | enum none\|host-prepared\|imported-inert | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/preparedResolution |  |  |
| RustUniverseV2ResolvedInputs.sourceUnitOwnershipId | UTF-8-NFC-text\|null | Sha256Text \| null | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RustUniverseV2ResolvedInputs/properties/sourceUnitOwnershipId |  |  |
| RepositoryResolutionV3.dependencySourceSetId | UTF-8-NFC-text | Sha256Text; required non-null; == universe.resolvedInputs.dependencySourceSetId | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3/properties/dependencySourceSetId | start.admit_open_universe: REPOSITORY_RESOLUTION_JOIN |  |
| RepositoryResolutionV3.preparedOutputSetId | UTF-8-NFC-text\|null | Sha256Text \| null; == universe.resolvedInputs.preparedOutputSetId | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3/properties/preparedOutputSetId | start.admit_open_universe: REPOSITORY_RESOLUTION_JOIN |  |
| RepositoryResolutionV3.authorizationId | UTF-8-NFC-text\|null | Sha256Text \| null; null when preparedOutputSetId is null or the preparation is imported-descriptor | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3/properties/authorizationId | start.admit_open_universe: REPOSITORY_RESOLUTION_JOIN |  |
| RepositoryResolutionV3.workerExecutesRepositoryCode | bool | const false | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3/properties/workerExecutesRepositoryCode |  |  |
| RepositoryResolutionV3.effects | definite-text-keyed-map\|null | {subprocess, filesystemWrite, network, environment} of EffectV1 \| null; null exactly when authorizationId is null | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/RepositoryResolutionV3/properties/effects | start.admit_open_universe: authorizationId-effects pairing |  |
| DependencySourceManifestV3.dependencySourceSetId | UTF-8-NFC-text | Sha256Text; == OpenUniverse repositoryResolution.dependencySourceSetId | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceManifestV3/properties/dependencySourceSetId |  |  |
| DependencySourceManifestV3.manifestSha256 | UTF-8-NFC-text | DigestHex; digest annotation 'exact transport manifest frame bytes as sent' (self-referential); no recipe | owner-contradictory | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceManifestV3/properties/manifestSha256 |  | R3-G11 |
| DependencySourceManifestV3.entries | definite-array | 0..1000000 (maxDependencySourceEntries); uniqueItems; order law unstated (x-opensip-order sequence); [] for an empty set | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceManifestV3/properties/entries |  | R3-G11 |
| DependencySourceManifestV3.entries[].packageKey | UTF-8-NFC-text | text 1..4096; grammar and join to DependencyPackageSourceV1 unstated | owner-missing | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceManifestV3/properties/entries/items/properties/packageKey |  | R3-G11 |
| DependencySourceManifestV3.entries[].path | UTF-8-NFC-text | CanonicalPath pattern, 1..4096 | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceManifestV3/properties/entries/items/properties/path |  | R3-G2 |
| DependencySourceManifestV3.entries[].byteLength | uint64 | uint64 | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceManifestV3/properties/entries/items/properties/byteLength |  |  |
| DependencySourceManifestV3.entries[].contentSha256 | UTF-8-NFC-text | DigestHex of the retained member bytes | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceManifestV3/properties/entries/items/properties/contentSha256 |  |  |
| DependencySourceSealV3.dependencySourceSetId | UTF-8-NFC-text | Sha256Text echo | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3/properties/dependencySourceSetId |  |  |
| DependencySourceSealV3.manifestSha256 | UTF-8-NFC-text | DigestHex echo | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3/properties/manifestSha256 |  | R3-G11 |
| DependencySourceSealV3.entryCount | uint64 | uint64; 0 for an empty set | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3/properties/entryCount |  |  |
| DependencySourceSealV3.totalBytes | uint64 | uint64; maxDependencySourceTotalBytes 8589934592 exists, binding not restated | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3/properties/totalBytes |  |  |
| DependencySourceSealV3.totalChunkCount | uint64 | uint64; 0 for an empty set (no chunk) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3/properties/totalChunkCount |  |  |
| DependencySourceChunk(unnamed).dependencySourceSetId | UNSTATED | member named by native-evidence.md:2877 only; no type, bound or order | owner-missing | native-evidence.md:2877 |  | R3-G10; R3-G3 |
| DependencySourceChunk(unnamed).packageKey | UNSTATED | member named by native-evidence.md:2877 only; no type, bound or order | owner-missing | native-evidence.md:2877 |  | R3-G10; R3-G3 |
| DependencySourceChunk(unnamed).path | UNSTATED | member named by native-evidence.md:2877 only; no type, bound or order | owner-missing | native-evidence.md:2877 |  | R3-G10; R3-G3 |
| DependencySourceChunk(unnamed).chunkIndex | UNSTATED | member named by native-evidence.md:2877 only; no type, bound or order | owner-missing | native-evidence.md:2877 |  | R3-G10; R3-G3 |
| DependencySourceChunk(unnamed).byteOffset | UNSTATED | member named by native-evidence.md:2877 only; no type, bound or order | owner-missing | native-evidence.md:2877 |  | R3-G10; R3-G3 |
| DependencySourceChunk(unnamed).bytes | UNSTATED | member named by native-evidence.md:2877 only; maxDependencySourceChunkBytes 1048576 exists but is not bound by the row | owner-missing | native-evidence.md:2877 |  | R3-G10; R3-G3; R3-G1 |
| DependencySourceAccepted(unnamed).dependencySourceSetId | UTF-8-NFC-text | exact DependencySourceSeal echo after digest/VFS validation | owner-missing | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3/properties/dependencySourceSetId |  | R3-G10; R3-G3 |
| DependencySourceAccepted(unnamed).manifestSha256 | UTF-8-NFC-text | exact DependencySourceSeal echo after digest/VFS validation | owner-missing | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3/properties/manifestSha256 |  | R3-G10; R3-G3 |
| DependencySourceAccepted(unnamed).entryCount | uint64 | exact DependencySourceSeal echo after digest/VFS validation | owner-missing | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3/properties/entryCount |  | R3-G10; R3-G3 |
| DependencySourceAccepted(unnamed).totalBytes | uint64 | exact DependencySourceSeal echo after digest/VFS validation | owner-missing | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3/properties/totalBytes |  | R3-G10; R3-G3 |
| DependencySourceAccepted(unnamed).totalChunkCount | uint64 | exact DependencySourceSeal echo after digest/VFS validation | owner-missing | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/DependencySourceSealV3/properties/totalChunkCount |  | R3-G10; R3-G3 |
| NativeContextVerifiedV1.nativeContextId | UTF-8-NFC-text | Sha256Text == OpenUniverse.universe.resolvedInputs.nativeContextId | governed | opensip.product.provider-startup.1#/$defs/NativeContextVerifiedV1/properties/nativeContextId | start.admit_native_context_verified |  |
| NativeContextVerifiedV1.recomputedNativeContextId | UTF-8-NFC-text | Sha256Text; worker recomputation; equal | governed | opensip.product.provider-startup.1#/$defs/NativeContextVerifiedV1/properties/recomputedNativeContextId | start.admit_native_context_verified |  |
| NativeContextVerifiedV1.equal | bool | const true | governed | opensip.product.provider-startup.1#/$defs/NativeContextVerifiedV1/properties/equal |  |  |
| PreAnalyzeUnavailableV1.executionId | UTF-8-NFC-text | ExecutionIdText == OpenUniverse (rust-semantic IdentityText) | governed | opensip.product.provider-startup.1#/$defs/PreAnalyzeUnavailableV1/properties/executionId | start.admit_unavailable |  |
| PreAnalyzeUnavailableV1.snapshotId | UTF-8-NFC-text | SnapshotId2 == OpenUniverse | governed | opensip.product.provider-startup.1#/$defs/PreAnalyzeUnavailableV1/properties/snapshotId | start.admit_unavailable |  |
| PreAnalyzeUnavailableV1.planId | UTF-8-NFC-text | PlanId2 == OpenUniverse | governed | opensip.product.provider-startup.1#/$defs/PreAnalyzeUnavailableV1/properties/planId | start.admit_unavailable |  |
| PreAnalyzeUnavailableV1.reason | UTF-8-NFC-text | const native-context-mismatch | governed | opensip.product.provider-startup.1#/$defs/PreAnalyzeUnavailableV1/properties/reason |  |  |
| PreAnalyzeUnavailableV1.nativeContextId | UTF-8-NFC-text | Sha256Text == universe.resolvedInputs.nativeContextId | governed | opensip.product.provider-startup.1#/$defs/PreAnalyzeUnavailableV1/properties/nativeContextId | start.admit_unavailable |  |
| PreAnalyzeUnavailableV1.recomputedNativeContextId | UTF-8-NFC-text | Sha256Text; differs from nativeContextId | governed | opensip.product.provider-startup.1#/$defs/PreAnalyzeUnavailableV1/properties/recomputedNativeContextId | start.admit_unavailable; ne.pre_analyze_unavailable_conversion: host mints coverage after DONE |  |
| FactBatchV3.schemaVersion | uint64 | const 3 (payload discriminator; not FactCandidateV1.schemaVersion) | governed | opensip.product.fact-batch.3#/properties/schemaVersion |  |  |
| FactBatchV3.analysisOrdinal | uint64 | uint64 echo of AnalyzeV2.analysisOrdinal | governed | opensip.product.fact-batch.3#/properties/analysisOrdinal | dispatch: expectedAnalysisOrdinal |  |
| FactBatchV3.stageId | UTF-8-NFC-text | StageIdText 1..255 (code points): C-2 stageId text echo of StageRequestV2.planStage.stageId; not stageOrdinal, not retainedStageOrdinal | governed | opensip.product.fact-batch.3#/properties/stageId | dispatch: expectedStageId |  |
| FactBatchV3.batchIndex | uint64 | contiguous from 0 per stage | governed | opensip.product.fact-batch.3#/properties/batchIndex | dispatch: expectedBatchIndex |  |
| FactBatchV3.candidates | definite-array | wire items FactCandidateV1 (bstr payload); 1..4096 (maxFactBatchCandidates); JSON-vector ref | governed | opensip.product.fact-batch.3#/properties/candidates | wire.admit_fact_batch | R3-G1 |
| FactBatchV3.occupancyCompanions | definite-array | OccupancyCompanionV1 (10 members, allOf branches); 0..len(candidates); strictly increasing candidateOrdinal naming this batch | governed | opensip.product.fact-batch.3#/properties/occupancyCompanions | wire.admit_fact_batch: COMPANION_CANDIDATE |  |
| CoverageResultV3.schemaVersion | uint64 | const 3 | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3/properties/schemaVersion |  |  |
| CoverageResultV3.key | definite-text-keyed-map | CoverageKeyV2 (native-evidence, 5 members) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3/properties/key |  | R3-G7 |
| CoverageResultV3.entry | definite-text-keyed-map | ViewEntryV3 (10 members; schema-native, not expanded here) | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3/properties/entry | ne.admit_coverage_result_v3; ne.coverage_bijection |  |
| CoverageKeyV2@native-evidence.relation | UTF-8-NFC-text | Relation enum; == keys[i].relation | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageKeyV2/properties/relation | start.admit_coverage_frame | R3-G7 |
| CoverageKeyV2@native-evidence.resolution | UTF-8-NFC-text | Rung enum; == keys[i].resolution | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageKeyV2/properties/resolution | start.admit_coverage_frame | R3-G7 |
| CoverageKeyV2@native-evidence.sourceUniverse | UTF-8-NFC-text | bare 64-hex suffix of keys[i].sourceUniverseId | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageKeyV2/properties/sourceUniverse | start.admit_coverage_frame | R3-G7 |
| CoverageKeyV2@native-evidence.targetUniverse | UTF-8-NFC-text | bare 64-hex suffix of keys[i].targetUniverseId | governed | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageKeyV2/properties/targetUniverse | start.admit_coverage_frame | R3-G7 |
| CoverageKeyV2@native-evidence.subjectScopeCommitment | UTF-8-NFC-text | Sha256Text; == keys[i].subjectScopeCommitment and the host-minted scope2 text form | owner-contradictory | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageKeyV2/properties/subjectScopeCommitment | ne.admit_coverage_result_v3 | R3-G4 |

## 11. Member-list comparisons (mechanical; each has a declared expected delta, and drift fails the build)

| comparison | kept | removed | added | same order | ok | note |
|---|---|---|---|---|---|---|
| payloadSchemas.HelloV2 -> provider-handshake HelloV3 | 5/5 | [] | ["protocolMajor", "identityVersions"] | True | True |  |
| payloadSchemas.HelloAckV2 -> provider-handshake HelloAckV3 | 7/7 | [] | ["identityVersions"] | True | True |  |
| definitions.ExpectedRustIdentityV2 -> ExpectedRustIdentityV3 | 6/6 | [] | [] | True | True |  |
| definitions.ProtocolLimitsV2 -> provider-handshake ProtocolLimitsV3 | 24/24 | [] | ["maxDependencySourcePackages", "maxDependencySourceEntries", "maxDependencySourceTotalBytes", "maxDependencySourceChunkBytes", "maxUnresolvedEdgesPerStage", "maxCfgSets", "maxExpansionRows", "maxGeneratedFileRows"] | True | True |  |
| payloadSchemas.OpenUniverseV2 -> provider-startup OpenUniverseV3 | 7/7 | [] | [] | True | True |  |
| payloadSchemas.UniverseAcceptedV2 -> UniverseAcceptedV3 | 6/6 | [] | [] | True | True |  |
| payloadSchemas.CoverageV2 -> CoverageV3 | 4/4 | [] | [] | True | True |  |
| payloadSchemas.UnavailableV2 -> UnavailableV3 (P3-25) | 5/5 | [] | [] | True | True |  |
| payloadSchemas.UnavailableV2 -> PreAnalyzeUnavailableV1 (P3-21) | 1/5 | ["analysisOrdinal", "affectedStageIds", "coverage", "coverageCommitment"] | ["executionId", "snapshotId", "planId", "nativeContextId", "recomputedNativeContextId"] | True | True |  |
| payloadSchemas.BudgetExhaustedV2 -> BudgetExhaustedV3 | 7/7 | [] | [] | True | True |  |
| payloadSchemas.FactBatchV2 -> RustFactBatchV2Vector (not negotiated) | 4/4 | [] | [] | True | True |  |
| payloadSchemas.FactBatchV2 -> fact-batch.3 (negotiated) | 4/4 | [] | ["schemaVersion", "occupancyCompanions"] | True | True |  |
| definitions.CoverageResultV2 -> native-evidence CoverageResultV3 | 1/5 | ["stageId", "entryOrdinal", "coverageState", "deficiency"] | ["entry", "schemaVersion"] | True | True |  |
| definitions.RepositoryResolutionV2 -> native-evidence RepositoryResolutionV3 | 0/8 | ["mode", "grantId", "projectId", "network", "buildScriptOutputs", "procMacroOutputs", "toolPaths", "preparedOutputManifestCommitment"] | ["authorizationId", "dependencySourceSetId", "effects", "preparedOutputSetId", "workerExecutesRepositoryCode"] | True | True | network -> effects is the only stated correspondence (native-evidence.md:2887-2888) |
| definitions.RustProviderCapabilityV2 -> RustCapabilitiesV3 (token array; no members) | 0/6 | ["providerId", "language", "providerVersionSource", "toolchainIdentitySource", "relations", "platformIds"] | [] | True | True |  |
| rust-v1 (RustUniverseV1) -> RustSemanticUniverseV2 | 21/21 | [] | [] | True | True |  |
| rust-v1.resolvedInputs -> RustUniverseV2ResolvedInputs | 4/9 | ["cfg", "packageLockIdentity", "resolvedPackages", "buildScriptOutputs", "procMacroOutputs"] | ["cfgSets", "configProjectionSha256", "dependencySourceSetId", "lockfileIdentity", "nativeContextId", "preparedOutputSetId", "preparedResolution", "schemaVersion", "sourceUnitOwnershipId", "unifiedFeaturesId"] | False | True |  |
| fact-plane candidateSchema (FactCandidateV1) -> fact-batch.3 JSON-vector candidate | 13/14 | ["canonicalRelationPayload"] | ["canonicalRelationPayloadHex", "decodedRelationPayload"] | True | True | vector form, not a wire record |
| SUPERSEDED native-evidence HelloV3 -> provider-handshake HelloV3 | 4/4 | [] | ["hostBuildId", "expectedProtocolContractSha256", "expectedIdentity"] | False | True |  |
| SUPERSEDED native-evidence HelloAckV3 -> provider-handshake HelloAckV3 | 3/3 | [] | ["providerBuildId", "rustCommitHash", "hostTriple", "targetTriple", "sysrootDigest"] | False | True |  |
| SUPERSEDED native-evidence ProtocolLimitsV3 -> provider-handshake ProtocolLimitsV3 | 8/8 | [] | ["maxFramePayloadBytes", "maxSnapshotChunkBytes", "maxSnapshotEntries", "maxSnapshotTotalFileBytes", "maxPreparedOutputChunkBytes", "maxPreparedOutputEntries", "maxPreparedOutputTotalBlobBytes", "maxAnalyzeStages", "maxRelationsPerStage", "maxSubjectsPerStage", "maxRequestedCoverageKeysPerStage", "maxFactBatchCandidates", "maxFactCandidatesTotal", "maxCanonicalRelationPayloadBytes", "maxCoverageEntriesPerFrame", "maxCandidateSpoolBytes", "maxRequestPayloadBytesTotal", "maxResponsePayloadBytesTotal", "maxRequestFrames", "maxResponseFrames", "maxStderrBytes", "maxScratchBytes", "cancellationGraceMilliseconds", "normalExitGraceMilliseconds"] | False | True |  |
| §9.1 HelloV3 prose (native-evidence.md:2816-2818) | 7/7 | [] | [] | True | True |  |
| §9.1 ExpectedRustIdentityV3 prose (:2823-2826) | 6/6 | [] | [] | True | True |  |
| §9.1 HelloAckV3 prose (:2830-2831) | 8/8 | [] | [] | True | True |  |
| §9.2 DependencySourceManifest prose (:2876) | 3/3 | [] | [] | False | True |  |
| §9.2 DependencySourceManifest prose (:2876) entries[] items | 4/4 | [] | [] | False | True |  |
| §9.2 DependencySourceSeal prose (:2878) | 5/5 | [] | [] | False | True |  |
| §9.2 DependencySourceChunk prose (:2877) vs translation rows | 6/6 | [] | [] | True | True |  |
| §9.2 NativeContextVerifiedV1 prose (:2881) | 3/3 | [] | [] | True | True |  |
| §9.2 CoverageV3 wrapper prose (:2884) | 4/4 | [] | [] | True | True |  |
| §9.2 RepositoryResolutionV3 prose (:2886-2887) | 5/5 | [] | [] | False | True |  |
| §9.7 OpenUniverseV3 prose (:3178-3179) | 7/7 | [] | [] | True | True |  |
| §9.7 UniverseAcceptedV3 prose (:3188-3189) | 6/6 | [] | [] | True | True |  |
| §9.7 PreAnalyzeUnavailableV1 prose (:3206-3207) | 6/6 | [] | [] | True | True |  |

## 12. Vocabulary, limit and pin checks

- Unavailable reasons: v2 ['semantic-universe-incomplete', 'snapshot-resolution-input-missing', 'unsupported-compiler-mode', 'generated-cfg-unavailable']; §9.2 adds ['native-context-mismatch', 'dependency-source-incomplete', 'prepared-output-stale', 'prepared-output-not-inert', 'capability-missing', 'identity-version-mismatch']; startup `UnavailableV3` = startup law = (v2 ∪ adds) − native-context-mismatch: True. native-evidence `UnavailableReasonV3` − startup: ['native-context-mismatch', 'node-modules-outside-read-set']; startup − native-evidence: ['generated-cfg-unavailable', 'semantic-universe-incomplete', 'snapshot-resolution-input-missing', 'unsupported-compiler-mode'] (R3-G7; not referenced by any Rust3 carrier).
- `RustCapabilityToken` = native `CapabilityToken` − typescript-semantic-facts-v1 and maxItems = count: True.
- 22 phases, §9.2 prose == protocol3-transitions: True; phases added over v2 `phaseValues`: ['READY_DEPENDENCY_MANIFEST', 'RECEIVING_DEPENDENCY', 'WAIT_DEPENDENCY_ACCEPTED', 'WAIT_NATIVE_CONTEXT_VERIFIED'].
- Limits: {"okV2EqualsRows": true, "okHandshakeFirst24EqualV2": true, "okHandshakeLast8EqualSection93": true, "okSupersededNativeEvidenceNames": true}.
- `expectedProtocolContractSha256` pin equals the bytes read: True.
- C-2 selectors v3 vs v4: {"common": true, "kinds.fact-derivation": true, "coverageKey.key": false, "coverageKey.key field names and order": true}. Where `coverageKey.key` is unequal while its field names and order are equal, v4 adds per-field annotations (jsonType/checked/wireType/boundHere); rust2 references v3, and §0:136 names only v4.

## 13. Ordering: protocol3-transitions vs retained v2 transitionAstV2 (R3-G17)

- §0:118 supersedes only `stateRecord.phaseValues`: True.
- Cancel in START: v2 T023 allows True; P3 `*PRE_COMPLETE` includes START False.
- Unavailable: v2 T019 guard `{"op": "all", "items": [{"op": "eq", "left": "state.stageIndex", "right": {"const": 0}}, {"op": "eq", "left": "state.outputSeen", "right": {"const": false}}]}`; P3-25 guard `None`.
- FactBatch: v2 T016 guarded True, P3-23 guard `None`; BudgetExhausted: v2 T020 guarded True, P3-26 guard `None`.
- v2 `preparedOutputCustody.order`: "SnapshotAccepted, then when repositoryResolution.mode=prepared PreparedOutputManifest, zero or more PreparedOutputChunk, PreparedOutputSeal, PreparedOutputAccepted, then Analyze. Disabled mode goes directly from SnapshotAccepted to Analyze."; P3-08 next `READY_DEPENDENCY_MANIFEST`, P3-20 next `READY_ANALYZE`.

## 14. Executable-owner facts

- `check-rust-provider-protocol-v2.py` targets `rust-provider-protocol.v2.json` and executes rust-provider domains ['analysis-domain', 'subject', 'subject-scope', 'universe']; it contains none of stage-facts/stage-coverage/fact-stream/coverage-stream: True.
- `check-rust-provider-protocol.py` targets `rust-provider-protocol.v1.json` with domains ['coverage-stream.v1', 'fact-stream.v1', 'stage-coverage.v1', 'stage-facts.v1', 'subject-scope.v1']; it is not a v2 owner (R3-G19).

## 15. Common-control separation

- Rust provider plane: transport "inherited stdin/stdout byte pipes"; stdout rule "stdout is protocol-only from child start through EOF. A non-frame byte, truncation, digest mismatch, noncanonical payload or post-terminal byte is provider-protocol.". Provider frames are CBOR on fd0/fd1 only.
- Candidate control owner `docs/coop/artifacts/control-protocol-contract.v2.json` in-file fields: {"artifact": "control-protocol-contract.v2", "version": 2, "status": "CANDIDATE-NOT-APPLIED", "reviewStatus": "AWAITING-INDEPENDENT-REVIEW", "sealRecommendation": "DO-NOT-SEAL", "binds": "NOTHING", "registerRow": "DR-102"}; descriptor layout keys ['fd0_stdin', 'fd1_stdout', 'fd2_stderr', 'fd3_controlIn', 'fd4_controlOut', 'platformNote']; control schema `$id` `urn:opensip:design:control-schema:3`. Its own-version surface text begins: "The control protocol versions ITSELF: proposed controlProtocolMajor = 1 for this candidate. It is its own DR-111 compatibility-matrix row (file 04 line 175 name...".
- Translation consequence: no control member, discriminator or framing byte enters any Rust3 carrier; `controlMajor` is a separate axis from provider protocolMajor 3; the owner selection is R3-G18 (proposal-pending). Rust v2 itself is in-file `{"status": "CANDIDATE-NOT-APPLIED", "reviewStatus": "AWAITING-INDEPENDENT-REVIEW"}` yet is the pinned inherited base (`HelloV3.expectedProtocolContractSha256`; audit §3.2).

## 16. JSON Schema is not CBOR admission (probes, R3-G2)

- IdentityText: a 4096-code-point NFC string of 8192 UTF-8 bytes is admitted by the JSON Schema: True; violates the v2 4096-byte bound: True.
- native-evidence `CanonicalPath` pattern vs the v2 CanonicalPath rule: {"a//b": {"nativeEvidencePatternAdmits": true, "v2RuleAdmits": false}, "C:/x": {"nativeEvidencePatternAdmits": true, "v2RuleAdmits": false}, "a/./b": {"nativeEvidencePatternAdmits": false, "v2RuleAdmits": false}, "../x": {"nativeEvidencePatternAdmits": false, "v2RuleAdmits": false}, "/x": {"nativeEvidencePatternAdmits": false, "v2RuleAdmits": false}, "src/lib.rs": {"nativeEvidencePatternAdmits": true, "v2RuleAdmits": true}}.
- StageIdText maxLength 255 counts code points (510 UTF-8 bytes possible).
- Not checkable by any pinned JSON Schema: NFC; shortest-form integers and lengths; absence of floats, tags, negative integers and indefinite items; duplicate or non-text keys; length-first map key order; decode-once/re-encode byte equality; byte-string lengths; x-opensip-order utf8/candidateOrdinal/sequence; cross-record echoes and joins; commitments; the frame digest prefix. `Uint64` as a JSON integer also cannot express the CBOR major-type-0 encoding.

## 17. Gap register

| id | class | title | action | cited by |
|---|---|---|---|---|
| R3-G1 | implementation-choice | CBOR byte strings have no JSON Schema wire mirror | root carrier selection; the wire stays CBOR major type 2, definite length | 7 rows |
| R3-G2 | governed | NFC, UTF-8 byte bounds, uint64-only integers, canonical CBOR and CanonicalPath are not JSON-Schema admission | handwritten decode-once admission; no wire change | 7 rows |
| R3-G3 | owner-missing | Unnamed major-3 records: envelope, DependencySourceChunk and DependencySourceAccepted payloads | root/owner naming; do not reuse RustProviderEnvelopeV2 or invent a published name | 13 rows |
| R3-G4 | owner-contradictory | subjectScopeCommitment: rust2 per-stage commitments.subjectScope vs §4.1a per-key scope2 | owner decision; no recipe chosen here | 5 rows |
| R3-G5 | owner-contradictory | AnchorRefV1 member wire types unstated; fact-ref contradicts mandatory fact2 | owner statement; recorded UNSTATED | 7 rows |
| R3-G6 | governed | Payload selected by host state, not by a wire discriminator | state-parameterized decode entry points; no wire change | 3 rows |
| R3-G7 | governed | Same-named records inside the Rust3 wire and across languages | namespace by owner $id; never merge by bare name | 14 rows |
| R3-G8 | governed | Successor array bounds weaker than inherited derivable bounds | handwritten derived bounds; schema not edited | 4 rows |
| R3-G9 | owner-contradictory | PreparedOutput frames: no major-3 payload owner; inherited payload joins superseded rows | owner successor for PreparedOutput{Manifest,Chunk,Seal,Accepted} payloads; generate no carrier until then | 34 rows |
| R3-G10 | owner-missing | DependencySourceChunk and DependencySourceAccepted have no field-level schema | owner field-level publication; types recorded UNSTATED | 13 rows |
| R3-G11 | owner-contradictory | DependencySourceManifestV3.manifestSha256 recipe is self-referential; entry order and packageKey grammar unstated | owner recipe/order statement | 5 rows |
| R3-G12 | owner-missing | Coverage commitment field -> domain map unstated | owner confirmation of each field's domain before implementing recipes | 5 rows |
| R3-G13 | owner-missing | StageResultV2 superseded with no successor record | owner record or explicit retention statement | 7 rows |
| R3-G14 | owner-missing | ProviderFaultV2/CancelV2/CancelledV2 member types, nullability and phase vocabulary unstated | owner field-level statement; recorded UNSTATED | 13 rows |
| R3-G15 | owner-missing | Retained v2 members whose wire types are only derivable | owner confirmation; derivations are labeled, not asserted as owner text | 12 rows |
| R3-G16 | owner-missing | Identity echo substitution not enumerated for every carrier | owner enumeration; echo rows carry the transitive substitution with this gap | 5 rows |
| R3-G17 | owner-contradictory | protocol3-transitions vs retained v2 transitionAstV2: ordering divergences | owner reconciliation of the major-3 machine; supervisors must not pick silently | 3 rows |
| R3-G18 | proposal-pending | Common control protocol owner selection is a proposal | root confirmation; no control carrier in Rust3 provider translation | 0 rows |
| R3-G19 | proposal-pending | Citation defect in the unaccepted gap-resolution proposal | correct the proposal's citations before review | 0 rows |

### R3-G1: CBOR byte strings have no JSON Schema wire mirror (implementation-choice)

SnapshotFileChunkV2.bytes, PreparedOutputChunkV2.bytes, PreparedOutputBlobV2.content, FactCandidateV1.canonicalRelationPayload and the prose-only DependencySourceChunk.bytes are CBOR byte strings (rust-provider-protocol.v2 schemaLanguage.bytes; SnapshotEntryV2.targetBytes is untyped, see R3-G15). No schema-native record carries them; fact-batch.3 canonicalRelationPayloadHex is a JSON-vector transcription only. TS2-G1's ByteString/Uint8Array carrier choice is an unaccepted proposal and is not assumed here.

### R3-G2: NFC, UTF-8 byte bounds, uint64-only integers, canonical CBOR and CanonicalPath are not JSON-Schema admission (governed)

rust-provider-protocol.v2 canonicalCbor/schemaLanguage require NFC, byte-counted bounds, shortest integers, no negative integers, no floats/tags, length-first map order and decode-once/re-encode equality. The JSON Schema IdentityText maxLength counts code points (a 4096-code-point NFC string can exceed 4096 UTF-8 bytes; probe in coverage.json). native-evidence.schemas.v2 CanonicalPath's pattern admits an empty segment and a drive prefix that the v2 CanonicalPath rule refuses (probe). StageIdText maxLength 255 counts code points. Schema validity is never CBOR admission.

### R3-G3: Unnamed major-3 records: envelope, DependencySourceChunk and DependencySourceAccepted payloads (owner-missing)

Only the envelope protocolMajor value is superseded (native-evidence.md:122); no successor name for RustProviderEnvelopeV2 is published (audit G4). §9.2 gives DependencySourceChunk a member list and DependencySourceAccepted 'exact seal echo' with no record name (audit G5/G8). The wire carries no record names, so this is a naming/registry gap, not a wire gap.

### R3-G4: subjectScopeCommitment: rust2 per-stage commitments.subjectScope vs §4.1a per-key scope2 (owner-contradictory)

rust-provider-protocol.v2 coverageDomainAlgorithm puts one commitments.subjectScope value (domain opensip.rust-provider.subject-scope.v2 over the stage SubjectV2 array) in every key of a stage. native-evidence §4.1a (:1889-1947) makes key.subjectScopeCommitment the per-key scope2 over {snapshotId, sourceUniverse, targetUniverse, relation, resolution, enumeratorClosure, subjects}, and startup coverageFrames.entries requires entries[i].key.subjectScopeCommitment == keys[i]. Keys of one stage differ in relation/rung/target, so both cannot hold. §0 names neither rust2 commitments.subjectScope nor analysisDomain as superseded (§0:136 covers c2 v4 only; rust2 references c2 v3). StageAnalysisDomainV2.domainCommitment and examinedUniverse.subjectCount (len(D.subjects) vs SubjectV2) inherit the question. Proposal P-1 addresses typescript-semantic only.

### R3-G5: AnchorRefV1 member wire types unstated; fact-ref contradicts mandatory fact2 (owner-contradictory)

fact-plane anchorSchema gives nullability and variants but no CBOR types for snapshotId/contentSha256/startByte/endByte/factId, and no Rust major-3 owner restates them (startup identityMembers does not list anchor snapshotId). fact-ref names FACT-ID-V1 while RustCapabilitiesV3 requires fact-identity-fact2 and identity-schemas.v3 fact anchors have no fact reference. Proposal P-2 (names rust-semantic major 3) would refuse fact-ref; it is unaccepted.

### R3-G6: Payload selected by host state, not by a wire discriminator (governed)

FactBatch is FactBatchV2 or FactBatchV3 by target-attribution-v2 in both token arrays (handshake law factBatch; §0:123); Unavailable is PreAnalyzeUnavailableV1 in WAIT_NATIVE_CONTEXT_VERIFIED (P3-21) or UnavailableV3 in ANALYZING (P3-25) (startup law preAnalyzeUnavailable.phase). The selection is governed; the carrier form (state-parameterized decode, no tag, no try-each) is an implementation choice (TS2-G6 proposal form not assumed).

### R3-G7: Same-named records inside the Rust3 wire and across languages (governed)

rust-provider-protocol.v2 CoverageKeyV2 (8 members; request key in StageAnalysisDomainV2) and native-evidence.schemas.v2 CoverageKeyV2 (5 members; CoverageResultV3 entry key, bare-hex universes) BOTH appear on the Rust major-3 wire. FactCandidateV1 is language-specific in values (producer/language/producerVersion source). StageResultV2 (5 members) is not TS StageResultV1 (7). native-evidence.schemas.v2 UnavailableReasonV3 (7 values) differs from the startup UnavailableV3.reason enum (9 values) that P3-25 actually admits; no Rust3 carrier references UnavailableReasonV3 (closure check).

### R3-G8: Successor array bounds weaker than inherited derivable bounds (governed)

UnavailableV3.affectedStageIds has minItems 1 and no maxItems (derived <= maxAnalyzeStages 256); UnavailableV3/BudgetExhaustedV3.coverage have minItems 0 and no maxItems (derived 1..65536 = 256 stages x 256 keys, and <= maxFramePayloadBytes); CoverageV3.entries maxItems 4096 exceeds the derived per-stage key count <= maxRequestedCoverageKeysPerStage 256.

### R3-G9: PreparedOutput frames: no major-3 payload owner; inherited payload joins superseded rows (owner-contradictory)

§9.2 :2880 keeps the four PreparedOutput frames 'as above for inert rows only'. The inherited PreparedOutputManifestV2 entries (PreparedOutputEntryV2.planRow = exact rust-v1 buildScriptOutputs/procMacroOutputs row) and PreparedOutputBlobV2 variants (build-script/proc-macro owned by rust-v1 packageId/crateId) join rows that §0:130 supersedes (rust-v2 resolvedInputs carries preparedOutputSetId, PreparedOutputSetV3 rows of kinds build-script-directives|macro-expansion|generated-file). RepositoryResolutionV2.preparedOutputManifestCommitment/mode are superseded (§0:118). preparedOutputCustody.order still reads 'when repositoryResolution.mode=prepared'. startup identityMembers substitutes planId for PreparedOutputManifest/PreparedOutputAccepted but not Chunk/Seal. Whether entries stay PreparedOutputEntryV2 or become PreparedOutputRowV3-based is unstated (audit G6).

### R3-G10: DependencySourceChunk and DependencySourceAccepted have no field-level schema (owner-missing)

native-evidence.md:2877 lists DependencySourceChunk {dependencySourceSetId, packageKey, path, chunkIndex, byteOffset, bytes} with no wire types, bounds or order law; maxDependencySourceChunkBytes exists (§9.3) but the frame row does not bind it. :2879 DependencySourceAccepted is 'exact seal echo after digest/VFS validation'; its shape follows DependencySourceSealV3 by echo only.

### R3-G11: DependencySourceManifestV3.manifestSha256 recipe is self-referential; entry order and packageKey grammar unstated (owner-contradictory)

native-evidence.schemas.v2 DependencySourceManifestV3/DependencySourceSealV3 manifestSha256 carry x-opensip-digest raw-artifact 'the exact transport manifest frame bytes as sent', but manifestSha256 is itself a member of that manifest frame, so the stated preimage contains its own digest. No recipe analogous to rust2 commitments.snapshotManifest (hex SHA-256 of deterministic-CBOR(entries)) is stated. entries is x-opensip-order 'sequence' with uniqueItems and no sort key; packageKey is text 1..4096 with no grammar or join to DependencyPackageSourceV1.

### R3-G12: Coverage commitment field -> domain map unstated (owner-missing)

rust2 commitments define stageCoverage (opensip.rust-provider.stage-coverage.v2) and coverageStream (opensip.rust-provider.coverage-stream.v2), but the CoverageV2, UnavailableV2 and BudgetExhaustedV2 field texts do not name a domain for coverageCommitment; StageResultV2 says only 'v2 commitments'. §9.7 :3283-3287 lists the fields and says recipes/domains are unchanged over CoverageResultV3 values without mapping them. The v2 checker executes none of the stage/stream fact or coverage commitments; the v1 checker (not an owner) used *.v1 domains. Proposal P-4 is typescript-semantic only.

### R3-G13: StageResultV2 superseded with no successor record (owner-missing)

native-evidence.md:129 lists $.wireSchema.definitions.StageResultV2 as superseded for major 3, but no StageResultV3 is published; §9.7 :3286-3287 only states that StageResultV2.coverageCommitment's recipe is unchanged over CoverageResultV3 values. Members are carried here with that value substitution, pending an owner record.

### R3-G14: ProviderFaultV2/CancelV2/CancelledV2 member types, nullability and phase vocabulary unstated (owner-missing)

rust-provider-protocol.v2 gives field text only for ProviderFaultV2.faultKind/detailCode, CancelV2.reason and CancelledV2 'all'. executionId/analysisOrdinal types and nullability are unstated even though Cancel and ProviderFault are lawful before OpenUniverse/Analyze. ProviderFaultV2.phase has no text; CancelledV2.observedPhase is 'exact concrete phase' whose vocabulary (§0:118 phaseValues) is superseded by the 22 major-3 phases, with no statement of which subset is lawful. The v2 checker types none of these payloads; the v1 checker's types (nullable, handshake|universe|snapshot|analysis) are not an owner. BudgetExhaustedV2.observed's relation to limit is also unstated in v2.

### R3-G15: Retained v2 members whose wire types are only derivable (owner-missing)

SnapshotEntryV2.contentSha256, executable and targetBytes have no type text (variants give only nullability; targetBytes 'non-empty'). Chunk indexes/offsets and Seal/Accepted aggregates have no per-field type; this translation derives uint64 from limitPolicy.arithmetic ('count, offset ... additions use checked uint64') and records that derivation in typeSource.

### R3-G16: Identity echo substitution not enumerated for every carrier (owner-missing)

startup identityMembers enumerates SnapshotManifest/SnapshotSeal/SnapshotAccepted snapshotId, Analyze, PreparedOutputManifest/PreparedOutputAccepted planId, Cancel/Cancelled executionId and PreAnalyzeUnavailableV1. It does not name SnapshotFileChunkV2.snapshotId, PreparedOutputChunkV2/PreparedOutputSealV2.planId, AnchorRefV1.snapshotId, or the snapshotId inside the SubjectV2.subjectId preimage (subjectsAlgorithm), whose value necessarily changes with snapshot2 but is not restated.

### R3-G17: protocol3-transitions vs retained v2 transitionAstV2: ordering divergences (owner-contradictory)

§0:118 supersedes only orderingAndStateMachine.stateRecord.phaseValues, and protocol3-transitions claims to state existing behaviour exactly. Yet (a) v2 T023 permits Cancel in START while P3-29 uses *PRE_COMPLETE, which excludes START (P3-34 FAULT); (b) v2 T019 admits Unavailable only at stageIndex 0 before any output, while P3-25 is unguarded; (c) v2 T016/T020 FactBatch and BudgetExhausted guards and the framePrecheck direction/sequence/overflow law have no P3 rows (P3 ownedByProse covers payload validation only); (d) preparedOutputCustody.order ('Disabled mode goes directly from SnapshotAccepted to Analyze') contradicts P3-08 dependency custody and P3-20. (c) is plausibly retained law; (a), (b) and (d) are divergent.

### R3-G18: Common control protocol owner selection is a proposal (proposal-pending)

Rust provider frames own stdin/stdout (rust2 protocolIdentity.transport, framing.stdoutRule). The m1-protocol-gap-resolution-01 claim that control-protocol-contract.v2 plus control-completion.schema.v3 own common control (fd3/fd4, controlMajor independent of Rust major 3) is unaccepted and needs root registry-route confirmation; the contract's own in-file status/binds fields (coverage.json controlOwner) do not by themselves establish acceptance.

### R3-G19: Citation defect in the unaccepted gap-resolution proposal (proposal-pending)

m1-protocol-gap-resolution-01/resolutions.md cites docs/coop/artifacts/check-rust-provider-protocol.py (c190ee7f...) as 'checkRust2' (line 1048 manifest recipe; lines 852-1129 commitment structure). That checker targets rust-provider-protocol.v1.json (its line 27) and is listed in FROZEN_V1_HASHES by check-rust-provider-protocol-v2.py (line 64); its commitment domains are *.v1. The rust2 commitments text itself still states snapshotManifest = hex(SHA-256(deterministic-CBOR(entries))), so TS2-G10's Rust precedent survives, but TS2-G12's 'checkRust2 applies the same structure' support does not.

## 18. Same-name trace (never merge by bare name)

- **CoverageKeyV2 twice on the Rust3 wire.**
  - The rust2 `definitions.CoverageKeyV2` is the 8-member request key in `StageAnalysisDomainV2.requestedCoverageDomain` (external c2 v3 `coverageKey.key`). Its `sourceUniverseId`/`targetUniverseId` are Sha256Text native identities.
  - native-evidence `CoverageKeyV2` is the 5-member entry key inside `CoverageResultV3`: bare-hex universes and no producer, producerVersion or schemaVersion. Rows keyed `CoverageKeyV2@native-evidence.*` are that record.
  - TS `CoverageKeyV1` is a third record and is not on this wire.
- **FactCandidateV1** is one fact-plane shape. Per language, `producer` (`rust-semantic`), `language` (`rust`), `producerVersion` (HelloV3 identity) and universe-id supersession (:128 for Rust, :125 for TS) differ.
- **StageResultV2** (5 members) is not TS `StageResultV1` (7). **UnavailableReasonV3** (native-evidence, 7 values) is not the startup `UnavailableV3.reason` enum (9).

## 19. Unaccepted proposals and their Rust3 standing

| proposal (m1-protocol-gap-resolution-01) | Rust3 applicability | standing here |
|---|---|---|
| TS2-G1 ByteString / Uint8Array carrier | same question for Rust bstr members | not assumed; R3-G1 implementation choice |
| TS2-G3 StageIdText via dispatch | `dispatch-binding.schema.v1.json` `expectedStageId` itself names `StageRequestV2.planStage.stageId` | this translation cites the schema text directly, not the proposal |
| P-1 per-key scope2 (typescript-semantic only) | does not address rust2 `commitments.subjectScope` | R3-G4 open |
| P-2 fact-ref refusal (names rust-semantic major 3) | would close the fact-ref half of R3-G5 | PROPOSAL; R3-G5 open |
| P-3 manifestSha256 raw DigestHex (TS) | Rust already governed: rust2 `commitments.snapshotManifest` | no proposal needed for Rust |
| P-4 coverage field->domain map (typescript-semantic only) | Rust equivalent absent | R3-G12 open |
| P-5 report projection | not provider wire | out of scope |
| G9 control owner found / P-6 | control is a separate plane (§15) | R3-G18 proposal-pending |
| citations to `check-rust-provider-protocol.py` as "checkRust2" | that file is the v1 checker | R3-G19 citation defect |

## 20. Final account: genuine unresolved issues

Only an owner can close the following. None is closed here, and no carrier should be generated for a contradictory item until it is closed.
1. **R3-G9 PreparedOutput frames (owner-contradictory).** The four frames exist in the major-3 machine (P3-16..19), but their inherited payloads join rust-v1 rows that §0:130 supersedes. No field-level successor exists.
2. **R3-G4 subjectScopeCommitment (owner-contradictory).** rust2 uses one per-stage `subject-scope.v2` value for all keys; §4.1a and startup coverage correspondence require the per-key scope2. `domainCommitment` and `subjectCount` depend on it.
3. **R3-G17 ordering (owner-contradictory).** protocol3-transitions diverges from the non-superseded v2 transition rules: Cancel in START, the Unavailable-before-output guard, and v2 prepared-custody order text.
4. **R3-G11 DependencySourceManifestV3.manifestSha256 (owner-contradictory).** The digest preimage is self-referential and no recipe is given; the entry order and packageKey grammar are unstated.
5. **R3-G10 / R3-G3 (owner-missing).** DependencySourceChunk has no field types; DependencySourceAccepted, DependencySourceChunk and the envelope have no record names.
6. **R3-G12 / R3-G13 (owner-missing).** The coverage commitment field-to-domain map is unstated. StageResultV2 is "superseded" with no successor record.
7. **R3-G14 / R3-G15 / R3-G16 (owner-missing).** ProviderFault/Cancel/Cancelled member types, nullability and phase vocabulary are unstated. SnapshotEntryV2 variant types are unstated. Echo substitutions are not enumerated for chunk/seal/anchor and subject-id preimages.
8. **R3-G5 AnchorRefV1 (owner-missing types; fact-ref contradicts fact2).** P-2 remains an unaccepted proposal.
9. **R3-G18 / R3-G19 (proposal-pending).** The control owner route needs root confirmation, and the gap-resolution proposal's Rust checker citations are wrong.

Governed but not expressible in JSON Schema (handwritten admission, not gaps in ownership): R3-G2, R3-G6, R3-G7, R3-G8. Carrier representation: R3-G1.

## 21. Source pins (bytes read)

| path | sha256 | bytes | git |
|---|---|---|---|
| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b` | 61698 |  |
| `docs/v2/contracts/product-v1/native-evidence.md` | `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0` | 329013 | M |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f` | 135448 | M |
| `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json` | `9090e2ad51b767a176f51da09f201803d1cc82c047ade68102adcae1ee3a5f84` | 32009 | ?? |
| `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` | `1e35a77bae8d9c20171a934e9c16e4de4d7ce98bb024016d7e17cf9b0b38729c` | 33341 | ?? |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043` | 277967 | M |
| `docs/coop/design-corrections/native/fact-batch.schema.v3.json` | `b0ebc133df8763f6cd5f3716542321eba21c69714fca368fbe31ba57677a24e0` | 10028 | ?? |
| `docs/coop/design-corrections/native/occupancy-companion.schema.v1.json` | `d2bbbcc49adbb130d0bb010fee0b4cf25af7727f730fc329725fa62cd46ae14f` | 8821 | ?? |
| `docs/coop/design-corrections/native/dispatch-binding.schema.v1.json` | `868c3cf241af9ecc205ba7d078354e38a7db5132974120c046ac23a2dd1df938` | 4568 | ?? |
| `docs/coop/design-corrections/native/protocol3-transitions.v1.json` | `b0aca55d89482be14e9c34554c1febb66d9751754b7c3057a383a010515feb0b` | 14845 | M |
| `docs/coop/design-corrections/native/provider_wire_model.v1.py` | `a2a8b9d116552856412e4257069f8c75debd6d8b2fe165407477fb7b28e46295` | 19099 | ?? |
| `docs/coop/design-corrections/native/provider_startup_model.v1.py` | `3f75b859b45c4fc6d5e5c8ede642a981d8d83bdf55d8e19ef7c9ffe7d5e8d494` | 16245 | ?? |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `7d1c0acf2c7d74e52c6570bba66dcb846c03710f64cb61a2c83bd1c39abab8be` | 319376 | M |
| `docs/coop/design-corrections/native/source-pins.v2.json` | `ef2da049061341ee75250e2b262544d53ff3dbd24da642679f40bc1a48cb17bf` | 219232 | M |
| `docs/coop/artifacts/fact-plane.v1.json` | `9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d` | 59168 |  |
| `docs/coop/artifacts/resolved-inputs.v2.json` | `0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43` | 107615 |  |
| `docs/coop/artifacts/resolved-inputs-rust-provider-join.v2.json` | `435ec9cdd45a85255df0c099238bd0a3e1c10e88960716cd84649030d6482d47` | 16770 |  |
| `docs/coop/artifacts/c2-plan-stage-schema.v3.json` | `3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285` | 112128 |  |
| `docs/coop/artifacts/c2-plan-stage-schema.v4.json` | `4876284790462968549f834b866c7ffc5f7be1c43b583169570c1947c5c4af39` | 174430 |  |
| `docs/coop/artifacts/check-rust-provider-protocol-v2.py` | `7b967b888fc172b27268fae2f59273e5cf10b58b97db7c1f19a15657826a48e4` | 105962 |  |
| `docs/coop/artifacts/check-rust-provider-protocol.py` | `c190ee7f62552ec342f5da1f66ba2b840cdffd5cd5cddb25e5987c315ee1502e` | 125802 |  |
| `docs/coop/artifacts/control-protocol-contract.v2.json` | `c50a79fef566ecccbd8913a3d309b0cf7332f7d77f892474a548ef3d7b4ebdca` | 80533 |  |
| `docs/coop/completion/control-completion.schema.v3.json` | `2929de62e9eb3a3dc78959eaf3d50361b8d1f895d086940724c1c743ac46a98c` | 22476 |  |
| `docs/implementation/README.md` | `d4aad574086892e31addf5a0263084fee694e195650d07270dbfb8e275ed73c3` | 7503 | ?? |
| `docs/implementation/m1/reviews/generation-owner-audit-01/audit.md` | `1423515e44f4a35b3a4433e65fdffa3914a4f4e0e0d12e47452914adb88c5903` | 24669 | ?? |
| `/tmp/opensip-implementation/m1-typescript-wire-translation-01/fields.json` | `4c211bb5fd28115b9fad3384d978b3911dd8f1f63cbd6fcf2e633430a27efe6a` | 243789 |  |
| `/tmp/opensip-implementation/m1-typescript-wire-translation-01/coverage.json` | `b288c30de9cbb98e9f8d09a4f9c34fa7780ac74c5a338046cce40e69e62d22f2` | 675 |  |
| `/tmp/opensip-implementation/m1-typescript-wire-translation-01/translation.md` | `c579ae5ca206c4ba22aef3874d9afd66e8a54f511052e546f347eafe093e6213` | 78094 |  |
| `/tmp/opensip-implementation/m1-protocol-gap-resolution-01/resolutions.md` | `c60af837f526b2de5982c7abdb94f4400687a61d04aae0c516c1fe692ea90781` | 24484 |  |

`docs/implementation/README.md` changed on disk during authoring (first read sha256 `e1204151c30bff15e541c927afc03e3f671b43e0f760c11e49388022b14f8572`, 14955 bytes); the pin above is the re-read. Its new text records the common-control owner chain as under root verification and changes no Rust3 disposition.

native/source-pins.v2.json agreement for pinned paths: {"docs/coop/artifacts/rust-provider-protocol.v2.json": true, "docs/v2/contracts/product-v1/native-evidence.md": true, "docs/v2/contracts/product-v1/identity-and-evidence.md": true, "docs/coop/design-corrections/native/provider-handshake.schemas.v1.json": true, "docs/coop/design-corrections/native/provider-startup.schemas.v1.json": true, "docs/coop/design-corrections/native/native-evidence.schemas.v2.json": true, "docs/coop/design-corrections/native/fact-batch.schema.v3.json": true, "docs/coop/design-corrections/native/occupancy-companion.schema.v1.json": true, "docs/coop/design-corrections/native/dispatch-binding.schema.v1.json": true, "docs/coop/design-corrections/native/protocol3-transitions.v1.json": true, "docs/coop/design-corrections/native/provider_wire_model.v1.py": true, "docs/coop/design-corrections/native/provider_startup_model.v1.py": true, "docs/coop/design-corrections/native/native_evidence_model.v2.py": true, "docs/coop/artifacts/fact-plane.v1.json": true, "docs/coop/artifacts/resolved-inputs.v2.json": true, "docs/coop/artifacts/c2-plan-stage-schema.v4.json": true}
