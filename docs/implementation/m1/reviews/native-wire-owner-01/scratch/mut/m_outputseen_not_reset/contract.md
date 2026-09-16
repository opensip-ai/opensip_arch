# Native wire carriers, TS2 and Rust3: author candidate 01

**Standing.** This is an AUTHOR candidate for root and a fresh independent review. It is not an approval, a production wire decoder, an analyzer or product code. Every architecture, product, frozen and evidence byte was read-only, and nothing was committed or pushed. The common-control source chain is the one root completed in `docs/implementation/m1/control-source-route.v1.json`, and historical CANDIDATE labels are not treated as blockers.

**Scope.** Complete, finite carrier mappings for `typescript-semantic` protocol major 2 (TS2) and `rust-semantic` protocol major 3 (Rust3):
- fields, variants, host-state selection and commitments;
- exact source pins;
- scoped supersession selectors with reference checks;
- a private carrier representation that one generator recipe can derive `crates/contracts/src/generated/protocol.rs` and `providers/typescript/src/generated/protocol.ts` from.

## Files

| File | Role |
|---|---|
| `wire-carriers.v1.json` | The declarative carrier input. It holds pins, two CBOR profiles, the private representation, 17 namespaced scalars, 50 records, both frame tables with host-state selectors, 41 handwritten admission rules, the commitment map and the transition overlay. |
| `wire-carriers.meta.schema.json` | The closed grammar of that input. It proves nothing about CBOR, NFC, byte bounds or joins. |
| `successor.json` | 13 scoped supersession rows. Each gives exact selectors, the scope, a disposition, the wire effect, a justification and its reference checks. The file also holds the 8 refuted false gaps and the parents, all pinned and unchanged. |
| `field-coverage.json` | Every inventory row, mapped either to a carrier member, a moved location, a frame, or an explicit not-carried reason. Every cited gap is mapped to its resolution. |
| `check.py`, `tools/check_static.py`, `tools/check_reference.py`, `tools/wirecodec.py` | The reference check. Its output is `check-result.json`. |
| `selftest.py` | Mutation controls. Its output is `selftest-result.json`. |
| `tools/build.py`, `tools/common.py`, `tools/records_ts2.py`, `tools/records_rust3.py`, `tools/rules.py`, `tools/succ.py` | Regenerate the three JSON outputs. They fail on pin drift, an unmapped row, a missing member or an unresolved gap. |

```
OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch python3 tools/build.py
/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B check.py
/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B selftest.py
```

## 1. Carrier input

**Type grammar (closed):**
- scalar kinds: `uint64`, `text`, `bytes`, `bool`, `null`;
- composite kinds: `array`, `nullable`, `ref` to a local `Ts2*`/`Rust3*` name, `extern` to a registered schema pointer with its generator namespace name, and `frame-payload`;
- record kinds: `record`, `variant-record` (a discriminator member, a full member order, and per-variant member types) and `alias`.

Presence is `required` or `optional`. Nullable means present-null and is never omission. Optional means absent and is never null; only the C-2 `planStage` members are optional. Integer literals are decimal strings. A missing `maxItems`, `maxBytes`, `maxScalars` or `maxUtf8Bytes` means the member is bounded only by `maxFramePayloadBytes` (rule `FRAME-LIMIT`), and that is stated, not implied.

**Profiles differ:**

| | `ts2-cbor` (delivery.v2 `canonicalCbor`) | `rust3-cbor` (rust2 `canonicalCbor`) |
|---|---|---|
| Negative integers | CBOR major type 1 down to −2^63 is inside the data model. No TS2 carrier member has a negative type, so a negative value decodes and is then refused as a type mismatch. | Forbidden at decode, before any typing. |
| Map order | Bytewise order of the encoded keys. | Length-first, then bytewise. |

The two map orders are proven equal for text keys over 3,359 keys (`map-order-profiles-equivalent-for-text-keys`). The following are handwritten and not proved by any JSON Schema: NFC, UTF-8 byte bounds, shortest forms, duplicate keys, byte strings, and all joins and commitments. For example, `json-schema-maxlength-not-byte-bound` shows `Handshake1IdentityText` accepting 4,096 × "é", which is 8,192 bytes; the carrier refuses it.

**Byte strings.**
- On the wire: CBOR major type 2, always.
- Rust: `protocol::wire::ByteString(Vec<u8>)`, with the length checked before allocation.
- TypeScript: an owned `Uint8Array`.
- JSON vectors only: a lowercase hex `<member>Hex` field.

There is no JSON array, base64 or hex form on the wire, and no generated JSON carrier. The wire examples refuse hex text, a JSON array and empty bytes.

**Selection without tags.**
- `FactBatch`: selector `negotiated-target-attribution-v2` (the token in both Hello arrays).
- `Unavailable`: selector `host-phase`, which must be `WAIT_NATIVE_CONTEXT_VERIFIED` or `ANALYZING`; any other phase has no row.

Decode entry points take the selector and never try alternatives. No wire tag is added.

**Namespaces.**
- `Ts2*`: successors of the delivery.v2 wire schema.
- `Rust3*`: successors of the rust2 wire schema, plus the §9.2 records.
- Externs keep the generator candidate03 names: `Handshake1*`, `Startup1*`, `Native2*`, `Occupancy1*`.

There is no bare `CoverageKeyV2`, `FactCandidateV1`, `AnchorRefV1`, `FactBatchV3` or `StageResult*` name. Specifically:
- `Ts2CoverageKeyV1` is the 8-member TS request key;
- `Rust3CoverageKeyV2` is the 8-member rust2 request key;
- `Native2CoverageKeyV2` is the 5-member entry key.

Anchor order differs per language, so `Ts2FactCandidateV1` and `Rust3FactCandidateV1` are separate records.

**Private names are not wire versions.** `Ts2FrameV2`, `Rust3ProviderFrameV3`, `Rust3DependencySourceChunkV3`, `Rust3DependencySourceAcceptedV3` and `Rust3PreparedOutput*V3` are type names only. No `protocolMajor`, frame name, member name or CBOR type changes anywhere in this candidate.

## 2. Resolutions

### 2.1 Per-key scope2 in both languages (`SUCC-PER-KEY-SCOPE2`)

**The contradiction.**
- delivery.v2 `RequestedCoverageDomainV1.workerRule` and `coverageDomain.keyConstruction` put one per-stage `SubjectScopeV1` commitment into every key. rust2 `coverageDomainAlgorithm` does the same with `commitments.subjectScope`.
- native-evidence §4.1a (line 1889), identity §3 (lines 287–294) and startup `coverageFrames.entries` require each key to carry its own `scope2`.
- Keys in one stage differ in relation, rung and target, so the two rules cannot both hold. `scope2-keys-differ` shows three different values.

**Choice.** For both languages, each request key's `subjectScopeCommitment` is `"sha256:"` + the hex of `H('subject-scope', D_key)`, where `D_key` is:
- `schemaVersion` 2 and `snapshotId`;
- `sourceUniverse` and `targetUniverse` (the key's 64-hex suffixes);
- `relation` and `resolution` (the key's own);
- `enumeratorClosure` (the Plan-selected provider `closure2`);
- `subjects` (the host enumeration).

The host mints this value before spawn, and the same descriptor drives `admit_coverage_result_v3` and pre-Analyze conversion. The worker checks only the `Sha256Text` shape, and requires `entries[i].key` and `examinedUniverse` to echo `keys[i]`.

**Preserved per stage:**
- TS: the whole `SubjectScopeV1` (shape, `opensip.coverage.subject-scope.v1` recipe and `subjectCount`), which both sides still recompute, and its place in `domainCommitment`.
- Rust: `subjects`/`SubjectV2` and the `analysis-domain.v2` recipe. rust2 `commitments.subjectScope` stays a named recipe with no wire carrier.

The domain commitments keep their recipes; their values change because the keys change.

**Reference owners run:**
- `scope2-ts2-admits` and `scope2-rust3-admits` run the startup `admit_coverage_frame` and the native `admit_coverage_result_v3` over the native-cases fixture, and both are admitted.
- `scope2-per-stage-value-refused`: both inherited per-stage values are refused with `native.subject-scope-commitment-mismatch`.

### 2.2 Anchors: wire rule vs shared fact2 rule; fact-ref (`SUCC-ANCHOR-RULES`, `SUCC-FACT-REF-REFUSED`)

**Wire anchor rule** (provider candidates, both languages; this is the retained fact-plane.v1 `sourceSpanSchema.rule`):
- `source-span` requires `snapshotId` to be the OpenUniverse snapshot2 text.
- `path` must be a `kind=file` manifest path, and `contentSha256` must be that entry's DigestHex.
- `startByte` and `endByte` are uint64 with **startByte < endByte ≤ byteLength** (non-empty).
- Count is 1..100000. The 4096 limit is a JSON-vector bound only.

**Shared fact2 rule** (identity-model.v3.py:1892 `ANCHOR_RANGE`: `0<=a<=b<=len(raw)`, plus `ANCHOR_UTF8`) is **unchanged and not narrowed**. Zero-length fact2 anchors stay admissible from other producers. The non-empty requirement applies at provider-wire admission only.

`fact2-anchor-range-permits-empty` evaluates the exact pinned source expression. `anchor-empty-interval-refused-on-wire` shows the wire refusal.

**fact-ref.** `fact-identity-fact2` is a mandatory identity token in both token sets, and identity-schemas.v3 `fact.anchors` items are closed to `{path, blobDigest, startByte, endByte}`. So `kind=fact-ref` is `PROVIDER.PROTOCOL_VIOLATION` at candidate admission, before minting. The variant stays shape-decodable only so that the refusal is one typed outcome.

**Order.** The owners select different orders, and this candidate does not merge them:
- TS2: deterministic-CBOR bytes (delivery.v2 `AnchorRefV1.ordering`).
- Rust3: CVE1 bytes (fact-plane `anchorSchema.ordering`, which rust2 references unadjusted).

`anchor-order-languages-differ` shows the same pair sorting as `[b, aa]` under CBOR and `[aa, b]` under CVE1.

### 2.3 TS2 snapshot manifest digest (`SUCC-TS2-MANIFEST-DIGEST`)

`manifestSha256` = lowercase hex `SHA-256(deterministic-CBOR(entries))`, with no domain and no prefix; Seal and Accepted echo it. The inherited general `snapshotManifest` domain is not applied to this member, because `DigestHex` cannot hold `sha256:`. `ts2-manifest-domain-form-refused` checks this, and `ts2-manifest-digest-raw` agrees with the reference wire encoder.

**Citation correction.** The earlier proposal cited `check-rust-provider-protocol.py` as the v2 checker ("checkRust2"). That file is the **v1** checker:
- line 27 is `PROTOCOL = "rust-provider-protocol.v1.json"`;
- line 1048 is its manifest recipe;
- its stage and stream domains are `*.v1`;
- `check-rust-provider-protocol-v2.py` pins it in `FROZEN_V1_HASHES` and computes no `manifestSha256`.

The owner for the raw recipe is the rust2 `commitments.snapshotManifest` **text**. Neither checker is an owner. `citation-v1-checker-is-v1` checks all of this.

### 2.4 Rust dependency sources (`SUCC-DEPSRC-DIGEST`, `SUCC-DEPSRC-RECORDS`)

**The self-reference.** native-evidence.schemas.v2 annotates `DependencySourceManifestV3/SealV3.manifestSha256` as the "exact transport manifest frame bytes as sent". That preimage contains `manifestSha256` itself, so no value satisfies it (`depsrc-self-referential-unsatisfiable`).

**Non-self-referential recipe.** `manifestSha256` = lowercase hex `SHA-256(deterministic-CBOR(entries))`. This is the existing rust2 `commitments.snapshotManifest` recipe, and §3.2 invokes "the same … discipline as the snapshot". The registered schema bytes stay unedited because their raw digest is registered; the §0 HelloV3 precedent does the same.

**entries order:** strictly ascending `(packageKey, path)` by UTF-8 bytes. This equals `DependencySourceSetV1.packages` order (name, version, sourceId), then `DependencyFileManifestV1` path order within each package.

**packageKey grammar:** `name SP version SP sourceId`, naming exactly one package row. It is the same spelling as the native model's set key and `UnifiedFeaturesV1.activated[].packageKey`. The two orders agree because Cargo names and versions contain no byte ≤ 0x20.

**Joins.**
- One package's rows are exactly its file manifest: `H(native.dependency-file-manifest.v1)` = `fileManifestSha256`, the row count = `fileCount`, and the byte sum = `totalBytes`.
- Every package appears, and §9.3 limits apply.
- An empty set sends `entries []`, a digest of `SHA-256(0x80)`, seal counts of 0 and no chunk.

**Records.**
- `Rust3DependencySourceChunkV3` has exactly the §9.2 members: `{dependencySourceSetId Sha256Text, packageKey, path Native2CanonicalPath, chunkIndex, byteOffset uint64, bytes 1..maxDependencySourceChunkBytes}`.
- `Rust3DependencySourceAcceptedV3` is an alias of `Native2DependencySourceSealV3` (an exact echo).

**Checks:** `depsrc-file-manifest-join` runs the native model's `dependency_source_set_admit` and `file_manifest_identity`; also `depsrc-order-and-key` and `depsrc-empty-set`.

### 2.5 PreparedOutput frames on current records (`SUCC-PREPARED-V3`)

**Why.** The rust2 V2 payloads join rust-v1 `buildScriptOutputs` and `procMacroOutputs` rows, which §0 line 130 supersedes, so no V2 value can be constructed for a major-3 universe. A scoped successor is therefore unavoidable.

**Frame and member names are kept.** Only value domains change:
- `entries[i]` answers `PreparedOutputSetV3.rows[i]`, and `outputOrdinal` = i.
- `kind` is the row kind, restricted to the three inert kinds.
- `planRow` is the exact Plan-bound `Native2PreparedOutputRowV3`.
- `logicalPath` = `.opensip/prepared/v3/<i>-<blob.sha256>.blob`.
- `blobByteLength`/`blobSha256` = `row.blob`.
- `contentByteLength`/`contentSha256` equal the blob values, because the `PreparedOutputBlobV2` wrapper is gone.
- A generated-file row requires `generated.blob == blob`, as the native model's `preparation_capture` constructs it.
- The manifest recipe stays raw hex over entries. `planId` is plan2 on all four frames. Chunks carry the exact inert bytes.

**Links to the prebuild and native-context records.**
- *Worker:* every `inputBinding.dependencySourceSetId` equals `repositoryResolution.dependencySourceSetId`, and every `cfgSetId` names a universe `cfgSet`.
- *Host, before spawn:* `H(native.prepared-output-set.v3, {3, preparation, rows = entries[*].planRow})` equals `preparedOutputSetId`, which is also the universe and `NativeContextV2` value. `prepared-v3-set-identity-join` checks this with the native model.

**Read authority.** Generated files mount read-only at `.opensip/out/v1/<ownerKey>/<logicalPath>`. Expansion and directive rows are looked up by site or owner (§3.6 PO-4).

**Limits.**
- Author choice, needing reviewer attention: the entry count is split as macro-expansion ≤ `maxExpansionRows`, generated-file ≤ `maxGeneratedFileRows`, and build-script-directives ≤ `maxPreparedOutputEntries` (256, the v2 per-owner analogue).
- Blob bytes ≤ `maxPreparedOutputTotalBlobBytes`.
- The encoded manifest must fit in `maxFramePayloadBytes`. If it does not, there is no spawn: this is a host invariant (operational-failed / `SYSTEM.OUTCOME.ILLEGAL_STATE`, as in delivery.v2 `overflowFate`).

**Checks:** `prepared-v3-entries-from-set` uses the admitted native fixture set; also `prepared-v3-v2-planrow-refused` and `prepared-v3-v2-kind-refused`.

### 2.6 Major-3 transition precedence and terminal guards (`SUCC-TRANSITION-PRECEDENCE`)

**Precedence.** `protocol3-transitions.v1.json` is the only matching table. rust2 `framePrecheck` (direction, sequence and overflow) and the T016/T020 payload guards are retained as pre-match admission, with the same FAULT outcome.

**Divergences settled:**
- **(a) Cancel in START.** P3-29 `*PRE_COMPLETE` has no START row. The host never sends Cancel before Hello, and interrupted/130 precedence is unchanged. TS2 keeps T2-18 from START.
- **(b) Unavailable after output.** rust2 T019 guards Unavailable with stageIndex 0 and no output. §0 supersedes only `phaseValues`, and P3 claims to state existing behaviour exactly, so the dropped guard is retained law. The overlay adds `outputSeen=false` to P3-25: reset at Analyze, and set by FactBatch or CoverageV3.
  - The published table admits `FactBatch, Unavailable` (trace P3-25); the overlay faults with P3-34 (`p3-unavailable-after-output-faults`).
  - Eleven other traces run identically through the native model's `protocol3_run` and the overlay (`p3-overlay-differential`).
  - TS2's T2-14 already carries this guard (`ts2-order-unchanged`).
- **(d) Custody order.** SnapshotAccepted → dependency-source custody (always) → prepared custody iff `preparedOutputSetId` ≠ null → NativeContextVerified or pre-Analyze Unavailable → Analyze (§9.1 step 4, lines 2863–2866). This supersedes the rust2 `preparedOutputCustody.order`.

**Terminal guards** are P3 `preMatchLaw`, unchanged: FAULT absorbs; frames after a terminal fault; process faults apply from any phase.

### 2.7 Commitment field → domain map (`SUCC-COMMIT-MAP`)

`C(d,v) = "sha256:" + hex(SHA-256(UTF8(d) || 0x00 || deterministic-CBOR(v)))`.

| Field | TS2 domain (`opensip.ts-provider.*`) | Rust3 domain (`opensip.rust-provider.*`) |
|---|---|---|
| Coverage-frame `coverageCommitment`; `StageResult.coverageCommitment` | `stage-coverage.v1` (stage entries) | `stage-coverage.v2` |
| `Complete.coverageStreamCommitment`; Unavailable/BudgetExhausted `coverageCommitment` | `coverage-stream.v1` (stage-major entries) | `coverage-stream.v2` |
| `StageResult.factCommitment` | `stage-facts.v1` (wire candidates of the stage) | `stage-facts.v2` |
| `Complete.factStreamCommitment` | `fact-stream.v1` | `fact-stream.v2` |
| `FactBatchV1.batchCommitment` | `fact-batch.v1` (V3: none) | none |
| Request domain commitment | `requested-coverage-domain.v1` | `analysis-domain.v2` |
| Key `subjectScopeCommitment` | foundation `H('subject-scope')` (§2.1) | same |
| `manifestSha256` | raw hex over entries | raw hex (snapshot, dependency source, prepared) |

**Basis.** The preimage shape decides the domain:
- per-stage ordered entries are `stageCoverage`;
- stage-major arrays across all requested stages are `coverageStream`, so terminal coverage belongs there.

An empty stream commits `0x80`. `commit-ts2-fact-batch-matches-wire-model` runs `admit_fact_batch` and agrees byte for byte.

### 2.8 Missing or unnamed records and types

- **ProviderFaultV2 / CancelV2 / CancelledV2** (`SUCC-RUST3-FAULT-CANCEL`):
  - `executionId` is IdentityText | null and `analysisOrdinal` is uint64 | null. Each is null iff OpenUniverse or Analyze has not been sent or received, and otherwise equals it. This is the TS `CancelV1` rule.
  - `phase` and `observedPhase` name the host phase in which the fault was received or the Cancel sent. That is one of the 16 `*PRE_COMPLETE` phases; START is refused.
  - `detailCode` is IdentityText; `reason` is const `user-interrupt`.
- **BudgetExhaustedV3.observed** = limit + 1 (`SUCC-RUST3-OBSERVED`). A stage without a budget, or with a milliseconds budget, cannot BudgetExhaust.
- **SnapshotEntryV2 variants** (`SUCC-RUST3-SNAPSHOT-ENTRY`):
  - file: `byteLength` uint64, `contentSha256` DigestHex, `executable` bool, `targetBytes` null;
  - symlink: `targetBytes` a byte string of 1..frame bytes, and every other variant member null.
- **StageResultV2** is retained with value substitution; see §3.
- **Identity echo substitutions** (`SUCC-ECHO-ENUMERATION`) now also cover:
  - SnapshotFileChunk `snapshotId` (both languages);
  - AnchorRefV1 source-span `snapshotId`;
  - PreparedOutput Chunk and Seal `planId`;
  - the `snapshotId` inside the rust2 `SubjectV2.subjectId` preimage.
- **Explicit bounds:**
  - `Ts2ExecutionIdText` = `^exec1_[0-9a-f]{32}` (identity §2). This is narrower than `Startup1ExecutionIdText` but refuses nothing the host constructs.
  - `Ts2ProjectPath` is 1..4096 scalars, the identity LogicalPath bound.
  - `Rust3CanonicalPath` is the rust2 rule at ≤ 4096 bytes (C-2 `canonicalRelativePath`).
  - `Rust3PackageKey` and `Rust3CanonicalIdentifier` (C-2 grantId) are defined above.

## 3. False gaps refuted (no version bump)

- **R3-G13, StageResultV2 has no successor.** §9.7 names `StageResultV2.coverageCommitment` among the recipes that are unchanged over CoverageResultV3 values, so the supersession is of values, not of members.
- **R3-G15, integer types only derivable.** rust2 `schemaLanguage.integer` together with `closedDataModel` makes every integer uint64.
- **TS2-G3, stageId bound.** DispatchBinding `expectedStageId` (maxLength 255) is defined as the request `stageId`.
- **G6, payload selection.** The handshake and startup law already select the payload; the input only publishes the selectors.
- **TS2-G9, wireSchemaCommitment.** It is not a Hello member.
- **R3-G18, control owner.** Closed by the root control route.
- **R3-G17(c), T016/T020 guards absent from P3.** These are payload admission (P3 `ownedByProse`).
- **R3-G3, names.** Private type names are not wire.

## 4. Verification (reference check, not qualification)

**`check.py`: 133 checks, 0 failed.** They cover:
- 29 source pins;
- the input grammar;
- 47 member lists compared to owner required lists, including C-2 optional presence and the §9.2 prose list;
- frame sets, directions and terminals against delivery.v2 and rust2, and payload names against the TS2 order table, P3 and P3 `rowPayloads`;
- limit and enum literals against `ProtocolLimitsV3`/`TypeScriptProtocolLimitsV1`, fact-plane layers and P3 phases;
- that the scalar shapes equal their extern definitions;
- that the 67-node extern `$ref` closure is byte-free and non-negative;
- map-order equivalence;
- the citations and anchor sources;
- field coverage: TS2 200 rows (182 inherited + 18 new) and Rust3 372 rows (5 envelope + 205 grammar + 59 external + 76 new + 27 frames);
- every successor reference check.

**Reference owners executed** in the pinned reference env:
- `native_evidence_model.v2`: `subject_scope_commitment`/`descriptor`, `admit_coverage_result_v3`, `protocol3_run`, `dependency_source_set_admit`, `file_manifest_identity`, `prepared_output_set_admit`/`identity`;
- `provider_startup_model.v1`: `admit_coverage_frame`, `typescript_protocol2_run`;
- `provider_wire_model.v1`: `admit_fact_batch`, `wire_cbor`.

**Wire examples** decode and type-check real CBOR under each profile. The invalid cases cover:
- negative integers, per profile;
- non-shortest encodings, map order, duplicate keys, floats, tags, indefinite items and non-NFC text;
- bytes supplied as hex or as an array, and empty bytes;
- unknown or missing members;
- omitted vs present null, and absent vs null optional;
- FactBatchV3 without the token, and an Unavailable payload in the wrong phase or with an unlawful selector;
- frame names from the other language;
- the envelope major;
- variant null discipline;
- ExecutionId trailing newline;
- echo, digest and observed-limit refusals.

**`selftest.py`** seeds 16 defects: a renamed member, a changed limit, an integer literal, a bare name, a dropped P3 guard, anchor order, a frame terminal, bytes turned into text, a dropped fact-ref variant, a commitment domain, a coverage row, a gap resolution, a selector, nullable turned optional, a scalar pattern, and a dangling successor check. Each must fail at least one check; see `selftest-result.json`.

**Not claimed.** The codec in `tools/wirecodec.py` is test scaffolding, not a production wire decoder. No generator run, product execution, analyzer, CBOR codec qualification, or M2/M3 admission is claimed.

## 5. Remaining

**Truly remaining contradictions: none.** The following are author choices that the reviewer should confirm, not open gaps:
1. The PreparedOutput entry-limit split (§2.5).
2. `outputSeen` guard retention on P3-25, and no Cancel in START (§2.6).
3. The ProviderFault/Cancelled phase = host phase at receipt or send (§2.8).
4. The narrower `Ts2ExecutionIdText` and 4096-unit path bounds.
5. Anchor count 100000 enforced at the wire, equal to the fact2 mint bound.

**Future qualification, separate from contract completeness:**
- generator support for the `bytes`, `variant-record`, `alias`, `frame-payload` and `optional` kinds;
- M2 implementation of every handwritten admission rule;
- M3 host and provider codecs and analyzers;
- measured PreparedOutput manifest sizes against the frame limit;
- root binding of this candidate after independent review.
