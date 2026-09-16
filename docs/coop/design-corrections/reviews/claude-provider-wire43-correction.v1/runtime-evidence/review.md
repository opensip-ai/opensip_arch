# Provider wire corrections on frozen43: TypeScript major 2 and Rust major 3 handshakes and FactBatch (author implementation)

This is author work by the actual Claude author origin `f5617310-c7c7-4d85-acdd-31370f220944`, continuing its completed TS publication assessment at `/tmp/opensip-design-corrections/claude-ts-protocol43-publication-assessment.v1`. It is not independent review, not a blind consumer result, and not acceptance.

What was not done:
- Nothing was frozen.
- No acceptance was bound.
- No global ledger was repinned.
- The author package was not rebuilt.
- No product code was touched.
- Nothing was committed or pushed.
- No LIVE write was made.

The only inputs were frozen43 and this author's own earlier outputs. The reference checks here are design evidence. They are not worker, process or compiler qualification.

## 1. Custody

**Base.** `/tmp/opensip-design-corrections/candidate-subject.v43`, with manifest `…/reviews/candidate-subject.v43.json` at SHA `db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d`.

**Before the work.** All members were verified against the manifest:
- 12913 files, 737769489 bytes;
- 0 missing, 0 mismatched, 0 wrong size, 0 extra.
- Receipt: `receipts/00-frozen43-verify-before.json`.

**Work copy.** `work/candidate` is an exact copy, verified with the same manifest (`receipts/01-work-copy-verify.json`).

**After the work.**
- Frozen43 re-verified twice, `ok=true` with the same counts both times: `receipts/50-frozen43-verify-after.json` (after the controls) and `receipts/52-frozen43-verify-final.json` (after the follow-up wording edit, the final delta and the review writes). The follow-up edit touched only the work and scratch copies.
- The prior assessment runtime's hash index still matches byte for byte (`receipts/51-prior-assessment-runtime-verify.json`).
- The LIVE path was only read, for the manifest.

**Scratch trees.** Two scratch trees exist only in this runtime:
- `scratch-before/candidate` is a frozen43 copy used for the baseline controls.
- `scratch-after/candidate` is a work-copy copy whose `native/source-pins.v2.json` was refreshed there, and only there, so the pin-verifying checker could run.

The scratch-after tree ends byte-equal to the work copy for every changed file (`receipts/42-scratch-equals-work-final.json`).

## 2. What is now resolved in the author copy

| Finding | Before (frozen43) | Resolution |
|---|---|---|
| **TSP43-M1** (MUST): TS major-2 Hello/HelloAck not reconstructible | §9.4 listed capabilities only; the only field-level successor (`HelloV3`) was fixed to major 3 | `TypeScriptHelloV2`, `TypeScriptHelloAckV2` and `TypeScriptProtocolLimitsV1`, field by field; §9.4 text; §0 rows |
| **TSP43-M2** (MUST): token-absent TS FactBatch had two incompatible readings | "historical FactBatchV2" unqualified | Per-language preservation (P1). TS keeps `delivery.v2` `FactBatchV1` `{analysisOrdinal, stageId, batchIndex, facts, batchCommitment}`; Rust keeps `FactBatchV2`. Applied to every active owner note. |
| **TSP43-S1** (SHOULD): major value changed without §0 rows | "exactly 1" selectors unrowed | §0 rows for TS `major`, envelope, HelloV1 and HelloAckV1 |
| **TSP43-S2** (SHOULD): commitment disposition unstated | — | §9.6 and fact-batch v3 `commitments`; §0 FactBatch rows |
| **TSP43-A1**: per-language 4096 cap names | Rust name only | `maxFactBatchFacts` (TS) and `maxFactBatchCandidates` (Rust) |
| **TSP43-A2**: V3 CBOR projection | Descriptions only | Explicit projection law (§9.6 and fact-batch v3 `wireProjection`), executed by the wire model |
| **RW43-M1** (MUST): the Rust counterpart I had flagged | The frozen `HelloV3` admitted a Hello with no `hostBuildId`, `expectedProtocolContractSha256` or `expectedIdentity`, and refused them if present. `HelloAckV3` refused the identity echoes. `ProtocolLimitsV3` was closed at the 8 successor members while §9.3 said "All 24 v2 limits are retained". | `HelloV3`, `HelloAckV3`, `ExpectedRustIdentityV3` and a 32-member `ProtocolLimitsV3` in the successor document; §9.1 and §9.3 text; §0 rows |

The before/after discriminator (`receipts/30-before-after-discriminator-rows.json`) shows each defect mechanically:
- Frozen `HelloV3` admits the 4-member unauthenticated shape and refuses the full identity Hello. After the correction this is the other way round.
- Frozen `ProtocolLimitsV3` refuses the 24+8 map and admits the 8-member map. After the correction this is the other way round.
- No frozen43 owner defines any TypeScript major-2 Hello.
- The frozen occupancy gate "omits" all of these identically: a TS `FactBatchV1`, a Rust-shaped `FactBatchV2` on TS, a batch with a wrong commitment, and junk. The corrected `admit_fact_batch` admits the lawful historical payload of each language and refuses the others.

Root's reasoned ambiguity finding is preserved. The earlier generic V2 reading is recorded as a lawful alternate interpretation of the frozen text, not as a helper error. The correction selects per-language preservation.

## 3. Implementation choices

### C1. Successor schema document; the registered bundle is kept
`native/native-evidence.schemas.v2.json` is a registered `payloadSchemaDigest` document (§10 at frozen lines 3102–3113, and model `schema_document_digest`). Editing its bytes would re-register `coverage2` and import payload identities.

So the corrected records live in a new closed document, `native/provider-handshake.schemas.v1.json` (20 defs). A §0 row supersedes `#/$defs/HelloV3`, `#/$defs/HelloAckV3` and `#/$defs/ProtocolLimitsV3` of the registered bundle, following the §10 "Superseded schema annotation (registered bytes kept)" precedent.

### C2. TypeScript Hello (`TypeScriptHelloV2`)
- Keeps the `HelloV1` members unchanged: `hostBuildId` (non-empty NFC text), `expectedProviderDescriptorSha256`, `expectedRuntimeDescriptorSha256` and `limits`.
- Adds `expectedCapabilities` and `identityVersions`.
- Carries no payload `protocolMajor`, as `HelloV1` did not. The envelope and `providerProtocol.major` are exactly 2.

### C3. TypeScript HelloAck (`TypeScriptHelloAckV2`)
- Keeps all 14 `HelloAckV1` members. `protocolMajor` changes from 1 to 2.
- `capabilities` becomes the exact echo of Hello, replacing the fixed three-token array.
- Adds the `identityVersions` echo.

The descriptor binding is explicit (`x-opensip-wire-law.typescriptDescriptorBinding`):
- **Digests:** raw SHA-256 of the RFC 8785 bytes of the verified provider and runtime descriptors. HelloAck echoes both.
- **Provider descriptor fields:** `providerBuildId`, `protocolMajor`, `typescriptVersion`, `typescriptCompilerSha256`, `typescriptStdlibMerkleRoot`, `defaultWorkBudgetProfileId`, `defaultWorkBudgetProfileSha256`.
- **Runtime descriptor fields:** `nodeVersion`, `v8Version`, `modulesAbi`, `platformId`.

### C4. TypeScript limits (`TypeScriptProtocolLimitsV1`)
- Exactly the ten numeric `delivery.v2` `wireSchema.limits` members, with identical values.
- `limitRule` is policy text and never a member.
- No `ProtocolLimitsV3` member applies to TypeScript.

### C5. Rust Hello (`HelloV3`)
- Keeps every `HelloV2` member: `hostBuildId`, `expectedProtocolContractSha256` and `expectedIdentity` (`ExpectedRustIdentityV3`, whose `protocolMajor` is 3).
- Replaces the `RustProviderCapabilityV2` record with the token array. That replacement was already explicit in frozen `HelloV3` and §9.1.
- Keeps `identityVersions`.
- `limits` is `ProtocolLimitsV3`.
- **Major placement:** top-level `protocolMajor` is kept from the superseded `HelloV3`, and `expectedIdentity.protocolMajor` from `ExpectedRustIdentityV2`. Both are exactly 3, and so is the envelope.

### C6. Rust HelloAck (`HelloAckV3`)
- `{protocolMajor:3, providerBuildId, rustCommitHash, hostTriple, targetTriple, sysrootDigest, capabilities, identityVersions}`.
- The five identity members equal `Hello.expectedIdentity`, and `protocolMajor` equals `expectedIdentity.protocolMajor`. This is the `HelloAckV2` rule.
- `capabilities` and `identityVersions` echo Hello exactly.

### C7. Contract digest selection
`expectedProtocolContractSha256` is the raw SHA-256 of the exact bytes of `docs/coop/artifacts/rust-provider-protocol.v2.json`, pinned at `6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b`. That is the "exact selected v2 artifact bytes" `HelloV2` names, and the Rust base that remains selected for every non-superseded selector.
- It authenticates that retained base only.
- No successor-document digest is added. That would be a new digest input, not an inherited one.
- The major-3 successor law is identified on the wire by `protocolMajor` 3, the token set, `identityVersions` and the exact 32-member limits map.
- Recorded residual: a successor-document digest would be a separate owner decision. It is not claimed here.

### C8. Rust identity source
`expectedIdentity` comes from the selected Plan semantic-universe row's retained `resolved-inputs.v2` `rust-v1` members of the same names. Only `rust-v1.resolvedInputs` is superseded. That row's `deliveryJoin` binds these members to the verified signed release and the sidecar handshake; see also `rust-provider-protocol.v2` `requestProjection.identity`. The checker verifies that the row carries all six members.

### C9. Token-array order
Both languages use strictly unique arrays in ascending UTF-8 order (`x-opensip-order: utf8`), drawn from per-language enums that each contain the four identity tokens.
- **TypeScript:** inherited from `HelloAckV1` ("exact sorted array").
- **Rust:** replaces frozen `sequence`, so that exact recursive equality equals token-set equality. That is what the reference `negotiate()` already compares.
- Hello equals the selected signed row sorted; HelloAck equals Hello.

### C10. FactBatch
- **Negotiated:** `FactBatchV3` for both languages, field set unchanged.
- **Not negotiated:**
  - TS `FactBatchV1`: JSON vector `TypeScriptFactBatchV1Vector`, `analysisOrdinal` const 0, `facts` of at most `maxFactBatchFacts`, `batchCommitment`.
  - Rust `FactBatchV2`: `RustFactBatchV2Vector`, `candidates` of at most `maxFactBatchCandidates`.
  - Both reuse the fact-batch v3 candidate item by registered `$ref`.
- **Violation:** a V3 payload without the token, or a historical payload with it, is `PROVIDER.PROTOCOL_VIOLATION`.

### C11. Commitments
- **`FactBatchV3`:** carries no per-batch commitment.
- **TS `commitments.domains.factBatch`:** applies to `FactBatchV1.batchCommitment` only:

  `sha256:hex(SHA-256("opensip.ts-provider.fact-batch.v1" || 0x00 || deterministic-CBOR(wire facts)))`

- **Stage and stream commitments:**
  - TS `StageResultV1.factCommitment` and `CompleteV1.factStreamCommitment`, and Rust `stageFacts` and `factStream`, remain over the ordered `FactCandidateV1` stream whichever payload carried it.

### C12. CBOR projection
- The wire candidate is the vector candidate with `decodedRelationPayload` removed and `canonicalRelationPayload = bytes(canonicalRelationPayloadHex)`.
- Admission requires `hex == deterministic-CBOR(decodedRelationPayload)`.
- With text keys only, the two inherited map-order rules (TS bytewise, Rust length-first) select the same order.

### C13. Reference wrapper (`native/provider_wire_model.v1.py`)
It executes `admit_hello`, `admit_hello_ack` and `admit_fact_batch`, plus `validate_wire` and `published_limits`. The native model re-exports them as `admit_provider_hello`, `admit_provider_hello_ack`, `admit_provider_fact_batch`, `validate_provider_wire` and `provider_wire_limits`.
- Its wire CBOR encoder adds only the byte-string case and reuses the fact-plane `_cbor_head`.
- Stated scope: no framing, process, relation-grammar or anchor admission, and no qualification.

### C14. Occupancy gate
`provider_attribution_return_model.v2._token_gate` behaviour is unchanged. It has a new docstring saying it is capture-only and not historical-payload validation. Its conflicting note label `unnegotiated-fact-batch-v2` is renamed `unnegotiated-historical-fact-batch`; no test asserted the label.

### C15. TypeScript success order
In §9.4 and the §0 "Extended" row, `NativeContextVerified` goes between `SnapshotAccepted` and `Analyze`, as determined by §9.1 step 4 and §9.4. The order sentence explicitly changes no Coverage frame selector.

### C16. Contract §12
Counts are corrected to the derived values (428 cases, 115 definitions; frozen text said 375 and 100, already stale before this change). The wire-evidence sentence is added.

## 4. Delta (`delta-final/`)

`delta-final/files.json` has per-file before/after SHA-256 and sizes, and `delta-final/unified.patch` has 3799 lines. The earlier `delta/` directory is kept; it was generated before the follow-up wording edit.

| Path | Status | Before → after SHA-256 |
|---|---|---|
| `docs/v2/contracts/product-v1/native-evidence.md` | modified | `66c6b82b…24cd` → `4bbc42e0…9bd07` |
| `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json` | added | — → `9090e2ad…5f84` |
| `docs/coop/design-corrections/native/provider_wire_model.v1.py` | added | — → `a2a8b9d1…6295` |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | modified | `6ffc6659…faf3` → `0dead507…7c4c` |
| `docs/coop/design-corrections/native/check_native_evidence.v2.py` | modified | `7103b86c…7ce9` → `e9d653ff…6f72` |
| `docs/coop/design-corrections/native/native-cases.v2.json` | modified (+24 fixtures, +40 cases, prior bytes preserved) | `c16fc62b…4d60` → `e475aff5…600c` |
| `docs/coop/design-corrections/native/fact-batch.schema.v3.json` | modified (descriptions / `x-opensip-negotiation` only; validation keywords unchanged) | `a963abd3…0de2` → `b0ebc133…24e0` |
| `docs/coop/design-corrections/native/occupancy-companion.schema.v1.json` | modified (`x-opensip-wire` text only) | `983864b1…861b` → `d2bbbcc4…e14f` |
| `docs/coop/design-corrections/native/README.md` | modified (file and selector tables) | `277f7f4a…767f` → `5aacf73b…aa3b` |
| `docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json` | modified (two worker notes) | `2d5719b5…523f` → `b3862636…43d1` |
| `docs/coop/design-corrections/foundation/provider_attribution_return_model.v2.py` | modified (docstring and label) | `efb5f883…098e` → `2cfac924…7abd` |
| `docs/coop/design-corrections/foundation/execution_inputs_model.v1.py` | modified (one `NEEDED_ROOT` note) | `66a15add…9ea1` → `edeb02b8…92dd` |
| `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` | modified (two notes) | `8521f362…a2e1` → `22ee2507…ec29` |

Inherited historical artifacts are unchanged: `delivery.v2.json`, `rust-provider-protocol.v2.json`, `resolved-inputs.v2.json`, the registered `native-evidence.schemas.v2.json` and `protocol3-transitions.v1.json`.

### Root obligations, not done here

**Repins.** `delta-final/repin-index.json` lists the ledgers that still name a before-digest:
- `native/`, `security/`, `workflows/`, `foundation/` and `foundation/evaluator3-` `source-pins` ledgers;
- `docs/v2/architecture/implementation-normative-inputs.v9/v10/v11.json`;
- `implementation-planning-sources.v1.json`;
- `implementation-coverage.v1.json`.

The two added files also need adding to the native ledger. The exact native-ledger delta applied in scratch is `receipts/21-after-scratch-repin-delta.json` plus `receipts/38-after-scratch-repin-final-delta.json`.

**Generated reports.**
- The work copy's `native/native-evidence-report.v2.json` is intentionally not regenerated; the post-correction report exists only in scratch-after.
- The execution-inputs checker's `neededRootInputs` output text changes with the `NEEDED_ROOT` note.

## 5. Reference controls

All controls ran with `/tmp/opensip-architecture-review-env/bin/python -I -B`. Every command's full stdout, stderr and exit code is a receipt.

| Control | Receipt | Result |
|---|---|---|
| Frozen native checker (scratch-before) | `20-before-native-checker.json` | PASS 388/388, exit 0 |
| Corrected native checker (scratch-after, scratch pins) | `22-after-native-checker.json` | PASS 428/428, exit 0; `providerWire.faults=[]`, 32 Rust / 10 TS limits, §9.3=8, §9.4=10 |
| Corrected native checker after mutation restores | `35-after-native-checker-post-mutation.json` | PASS 428/428 |
| Corrected native checker, final bytes | `39-after-native-checker-final.json` | PASS 428/428 |
| Provider attribution checker, before / after | `23-…`, `24-…` | 47/47 both |
| Execution-inputs checker, before / after | `25-…`, `26-…` | exit 0 both, `mismatches: []`; after shows the corrected note |
| Before/after discriminator (frozen owners vs corrected) | `30-before-after-discriminator-rows.json` | 16 rows as in §2 |
| Actual refusal text of every provider-wire step | `31-audit-wire-cases-rows.json` | Every negative is refused for its stated key (§6) |
| Mutation controls, first run | `32-mutation-controls-results.json` | 4 of 6 applied and all detected. 2 **not applied**: constructor mistakes, one `old` string matched twice (TS/Rust `maxStderrBytes`), one had the wrong indentation. Kept as recorded. |
| Mutation controls, corrected run | `34-mutation-controls-v2-results.json` | 6 of 6 applied, each exit 1 with the expected FAIL evidence |

**What the checker now holds the successor to.** It re-derives the following from published inputs:
- TS limits from `delivery.v2` and from the §9.4 prose;
- Rust limits from `rust-provider-protocol.v2` (24) plus the §9.3 prose (8);
- that every `HelloV1`, `HelloAckV1`, `handshakeRequired`, `HelloV2`, `HelloAckV2`, `ExpectedRustIdentityV2` and frozen `HelloV3`/`HelloAckV3` member survives;
- that every TS HelloAck member is bound to a descriptor member or an echo;
- that the descriptor members exist;
- that the `rust-v1` row sources the identity;
- that the contract digest matches the artifact bytes;
- per-language token enums and `identityVersions`;
- no open objects.

**Where expected values come from.** The case expectations were authored without the model (`tools/author_wire_cases.py`):
- descriptor digests with `hashlib` over stdlib sorted compact JSON;
- candidate and wire CBOR with third-party `cbor2` canonical encoding;
- the TS batch commitment with `hashlib`.

The positive TS `FactBatchV1` case additionally checks the model's commitment against the checker's own `domainSha256Hex` oracle over the `cbor2` bytes.

**Mutations detected (receipt 34).** Each of these made the checker fail:
1. Renaming a TS limit.
2. Dropping `expectedProtocolContractSha256` from `HelloV3`.
3. Drifting `maxCfgSets` in the §9.3 prose.
4. Unbinding `nodeVersion` from the runtime descriptor.
5. Disabling the batch-commitment comparison.
6. Disabling the Rust identity echo.

## 6. The 40 provider-wire cases

**Positive (9).**
- TS2 Hello, and HelloAck with descriptor echoes.
- Rust3 Hello with identity, contract digest and 32 limits; Rust3 HelloAck identity echo.
- `target-attribution-v2` negotiated in both languages.
- Published limit maps.
- TS `FactBatchV1` with the commitment oracle.
- Rust `FactBatchV2` without a per-batch commitment.
- `FactBatchV3` in both languages.

**Negative (31).**
- TS Hello refused when:
  - it uses the superseded major-3 shape;
  - a legacy limit is omitted;
  - `limitRule` is present as a member;
  - a limit value is changed;
  - the tokens are out of UTF-8 order;
  - the envelope says major 1;
  - the descriptor digest mismatches;
  - the tokens are not the signed row.
- TS HelloAck refused when:
  - the runtime or provider-build echo changes;
  - a descriptor member is dropped;
  - it says major 1;
  - the token echo mismatches;
  - it has an extra member;
  - the runtime digest echo mismatches.
- Rust Hello refused when:
  - it uses the superseded 4-member shape;
  - it carries only the 8 successor limits;
  - it contains a TS token;
  - the contract digest is wrong;
  - the identity is not the Plan row;
  - the envelope says major 2.
- Rust HelloAck refused when:
  - the identity echo changes;
  - it says major 2;
  - `identityVersions` is changed.
- FactBatch refused when:
  - the TS batch commitment is wrong;
  - a TS batch arrives in the Rust V2 shape, or a Rust batch in the TS V1 shape;
  - a V3 payload arrives without the token;
  - a historical payload arrives with the token (both languages);
  - the candidate hex is not the CBOR of the decoded payload;
  - a TS V3 batch has a nonzero `analysisOrdinal`.

## 7. Adjacent frame ownership and handshake-to-Analyze order

### Resolved
TS major-2 success path: Hello/HelloAck → OpenUniverse/UniverseAccepted → snapshot custody → `NativeContextVerified` → Analyze. This is determined by §9.1 step 4 and §9.4, and recorded as an "Extended" §0 row for:
- `delivery.v2` `providerProtocol.ordering.normalPhases`
- `closedWorkerToHostFrames`
- `wireSchema.frameSchemas`

TypeScript still has no published transition table; `protocol3-transitions.v1.json` is Rust-only. No TS state machine is claimed.

### Still unresolved (reported, not fixed)

Each of these is a real field-level or ordering contradiction. Fixing any of them needs an owner decision beyond these corrections.

**ADJ-2 (MUST): pre-Analyze `Unavailable(native-context-mismatch)` has no constructible payload or lawful order in either language.**
- *Owners requiring it:*
  - `native-evidence.md` §2.3 "refuses with `Unavailable(native-context-mismatch)` before Analyze" (frozen 1449–1451);
  - §2.4 (1607–1609);
  - the §9.2 `NativeContextVerified` row;
  - §9.4;
  - `protocol3-transitions.v1.json` row P3-21 (`Unavailable` in `WAIT_NATIVE_CONTEXT_VERIFIED`).
- *Inherited payloads and orders still in force:*
  - `delivery.v2` `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.payloadSchemas.UnavailableV1`: `analysisOrdinal` "exactly 0", `affectedStageIds` "all requested stageIds", and `coverage` with one entry per requested key.
  - `$.typescriptSemanticSubstrate.providerProtocol.ordering.unavailableTerminal`: "permitted only immediately after Analyze".
  - `$.typescriptSemanticSubstrate.supervision.cleanUnavailable.allowedImmediatelyAfter`: "Analyze".
  - `rust-provider-protocol.v2` `$.wireSchema.payloadSchemas.UnavailableV2`: requires `analysisOrdinal`, `affectedStageIds` and a "stage-major exhaustive domain" `coverage`. §0 supersedes only its `fields.reason`.
- *Discriminator:* a worker detecting the mismatch in `WAIT_NATIVE_CONTEXT_VERIFIED` has received no Analyze, so it cannot produce requested stage IDs or requested-domain coverage. The TS order refuses any `Unavailable` before Analyze.
- *Alternatives:*
  - (a) A closed pre-Analyze `Unavailable` variant without stage or coverage members, with the host synthesizing unknown/provider-unavailable Coverage from the Plan's requested domains.
  - (b) Analyze before `NativeContextVerified`, which contradicts "before Analyze" and the P3 row order.
  - (c) Route the mismatch to `ProviderFault`/`FAULT`, which changes the provider-unavailable deficiency route to operational-failed.

**ADJ-3 (MUST): OpenUniverse and UniverseAccepted field-level successors are not published for either language.**
- *§9.1 step 3* says OpenUniverse carries "`snapshot2`, `plan2`, the universe descriptor including `nativeContext`, and `RepositoryResolutionV3`", without a language qualifier. `RepositoryResolutionV3` requires a non-null `dependencySourceSetId`, but §9.4 says TypeScript has no dependency-source frames.
- *Inherited payloads still in force:*
  - `delivery.v2` `…payloadSchemas.OpenUniverseV1`: `snapshotId SnapshotId`, `planId PlanId`, `universe TypeScriptSemanticUniverseV1`, `universeKey`.
  - `…UniverseAcceptedV1`.
  - `rust-provider-protocol.v2` `$.wireSchema.payloadSchemas.OpenUniverseV2` (`universe RustUniverseV1`, `repositoryResolution`) and `UniverseAcceptedV2`.
  - §0 supersedes only `definitions.RepositoryResolutionV2`.
- *Model inconsistency:* `protocol3-transitions.v1.json` `stateUpdates` sets `dependencyMode`/`preparedMode` "from the frame's booleans", but `OpenUniverseV2` has no booleans.
- *Discriminator:* a TS OpenUniverse with or without `repositoryResolution`; `snapshotId` as a v1 `SnapshotId` or as the `snapshot2` identity.
- *Alternatives:*
  - (a) keep the member names with successor types;
  - (b) new members `snapshot2`/`plan2`/`nativeContext`.

  Either way the owner also decides whether the mode flags derive from `RepositoryResolutionV3` or become explicit members.

**ADJ-4 (SHOULD): Coverage frame name.**
- *Rust:* `rust-provider-protocol.v2` `$.wireSchema.frameSchemas.Coverage` (payload `CoverageV2`) against the native §9.2 Frame column `CoverageV3` and P3-24 frame `CoverageV3`. For Rust, the §9.2 table plus P3-24 determine the frame name `CoverageV3`, so only a §0 row is missing.
- *TypeScript:* `delivery.v2` `frameSchemas.Coverage` against §9.4 "adds … `CoverageV3`". This is undetermined: frame type text `Coverage` with a V3 payload, or `CoverageV3`.
- My §9.4 order sentence was re-worded to change no Coverage selector (`receipts/37a-…`).

**ADJ-5 (SHOULD): `CancelledV1.observedPhase` has no value for the new interval.**
`delivery.v2` `…payloadSchemas.CancelledV1.fields.observedPhase` is the enum `handshake|universe|snapshot|analysis`, with no value for a Cancel during the new `NativeContextVerified` interval.
- *Alternatives:* reuse `snapshot`, or add a member.

### Observations (no change made)
- **rustCommitHash representation.** `resolved-inputs.v2` `rust-v1.digestFields` gives `rustCommitHash` as 64-hex, while native `ToolchainIdentityV1.rustCommitHash` is 40-hex. No owner states they must be equal, and `HelloV3` follows the Plan-row source (64-hex). If an owner later joins the handshake to `NativeContextV2.toolchain`, the representations conflict.
- **Missing join artifact.** The external `resolved-inputs-rust-provider-join.v2.json` named by `RustProviderCapabilityV2` is not present in frozen43. Its role is replaced by the token array, so nothing depends on it.
- **Stale planning wording.** Non-normative planning text still says "shared identity tokens/HelloV3 contracts" for TS2/Rust3:
  - `docs/v2/architecture/14-repository-and-module-layout.md:612`
  - `repository-file-inventory.v1.json:1810`
  - `implementation-boundaries-and-build-plan.md:718`

  Historical major-1/major-2 statements also remain (`04-lifecycle-delivery-and-operations.md:178-179`, `05-v1-to-v2-relationship.md:39`). None of these is a protocol owner, and none was edited.
- **Stale README counts.** The native `README.md` counts (100 records, 132 cases, 60 cells) were already stale and were left untouched.

## 8. Commands (from this runtime root)

```
python -I -B tools/verify_and_copy.py verify <frozen43> receipts/00-frozen43-verify-before.json
python -I -B tools/verify_and_copy.py copy <frozen43> work/candidate receipts/01-work-copy-verify.json
python -I -B tools/run_logged.py 10-author-handshake-schema … tools/author_handshake_schema.py work/candidate
python -I -B tools/run_logged.py 11-author-wire-cases … tools/author_wire_cases.py work/candidate
python -I -B tools/run_logged.py 12-apply-text-edits … tools/apply_text_edits.py work/candidate
(copy work → scratch-after, frozen43 → scratch-before)
python -I -B tools/run_logged.py 20/23/25-before-* … check_native_evidence.v2.py | check-provider-attribution-return.v2.py | check-execution-inputs.v1.py   (scratch-before)
python -I -B tools/run_logged.py 21-after-scratch-repin … tools/scratch_repin.py scratch-after/candidate …
python -I -B tools/run_logged.py 22/24/26-after-* …   (scratch-after)
python -I -B tools/run_logged.py 30-before-after-discriminator … tools/before_after.py <frozen43> work/candidate …
python -I -B tools/run_logged.py 31-audit-wire-cases … tools/audit_wire_cases.py scratch-after/candidate …
python -I -B tools/run_logged.py 32-mutation-controls … tools/mutation_controls.py …      (kept; 2 constructor mistakes)
python -I -B tools/run_logged.py 34-mutation-controls-v2 … tools/mutation_controls.v2.py …
python -I -B tools/run_logged.py 35-after-native-checker-post-mutation …
python -I -B tools/run_logged.py 37a/37b-followup-edit-* … tools/apply_followup_edit.py <root>
python -I -B tools/run_logged.py 38-after-scratch-repin-final … ; 39-after-native-checker-final …
python -I -B tools/run_logged.py 40-make-delta / 41-make-delta-final … tools/make_delta.py <frozen43> work/candidate delta[-final]
python -I -B tools/verify_and_copy.py verify <frozen43> receipts/50-frozen43-verify-after.json
```

## 9. Limits
- **Author work.** Integration, repins, broad combined suites, freezing, and fresh independent and blind review belong to root.
- **What was not exercised.** The JSON-vector wire records do not exercise frame length, digest or sequence bytes, deterministic-CBOR decoding of real frames, process lifetime, or compiler output.
- **Descriptor digests.** These hash `canonical.py` bytes, which equal RFC 8785 only for the fixture value domain.
- **What the wire model skips.** It does not validate relation payload grammar or anchors.
- **What stays open.** ADJ-2 to ADJ-5 remain open and are not claimed fixed. The contract digest authenticates the inherited base only (C7).
