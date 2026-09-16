# M1 generation source-owner audit 01

Standing: bounded read-only implementation-review audit to guide M1 generation.
It is not a review of the accepted architecture, not approval of a generator
recipe, and not an M1 completion or qualification claim. No product or
architecture file was edited. Source45/application46 acceptance and the
metadata2 successor are treated as settled.

Machine-readable companion: `audit.json` (same findings, with hashes).

## 0. Inputs read (exact bytes)

| Path | sha256 |
|---|---|
| docs/v2/architecture/implementation-boundaries-and-build-plan.md (§615–910) | 8e6e8babd30bc3421f605efea9aae4b2d4a5c3c4cbfa4315bbf74cbe4ccbd33b |
| docs/v2/architecture/14-repository-and-module-layout.md | c7b10bf6d0f98d196d4509c5b972cd87f4af27bf9a56b9ffe5a240f93ee6287e |
| docs/v2/architecture/repository-file-inventory.v1.json | 47909b561a7ea0e5960bda3e5eadd768fe733712e051255fade4ed40c9c4dad8 |
| docs/v2/architecture/implementation-normative-inputs.v13.json (34 rows, all hashes verified) | af228325492828b0ea5d6779601725a981bb467d0195e976a4247350c972c153 |
| docs/implementation/m1/metadata-unit.v1.json (ACCEPTED-DESIGN-UNIT, fullM1Complete=false) | 3ba8cc4658ca96a4f01c51eb5c38e82e756217b50838c61429a1597c0f1c7816 |
| docs/implementation/m1/metadata-v2/successor.json | 9d3248218da03a80d3cdc75f0118b2cb20fdc451be207ea632aa27a17f2d4080 |
| docs/implementation/m1/metadata-v2/sources.json | db23b6e0d6fe09366fa1575d93a6c26f1d92f3cf2a538db2d04c98af6d3fea9d |
| docs/v2/contracts/product-v1/native-evidence.md (§0, §9.1–9.5, §9.7) | 83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0 |
| docs/coop/artifacts/delivery.v2.json (`$.typescriptSemanticSubstrate.providerProtocol`) | 47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3 |
| docs/coop/artifacts/rust-provider-protocol.v2.json (`$.wireSchema`) | 6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b |
| docs/coop/design-corrections/native/protocol3-transitions.v1.json | b0aca55d89482be14e9c34554c1febb66d9751754b7c3057a383a010515feb0b |
| docs/coop/design-corrections/native/typescript-protocol2-order.v1.json | 007ef7affce224c7bac6af3bb7897e86691085e2dd788f4a613e45c1fa5b8bbb |
| docs/v2/architecture/02-distribution-and-components.md (control-protocol lines) | 5a110ef00dbc3bd91fd9075c08b6ba25cd306921f91f9d2b42e619dd470626fb |
| docs/v2/architecture/report-asset-binding.v1.json (projection lines) | 71363c0637d4405d9394782f805f33c294588834990614388a26a2dbd98027a6 |
| docs/coop/design-corrections/reviews/candidate-subject.v45.json (membership only) | 8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155 |
| docs/coop/design-corrections/reviews/application-subject.v46.json (`files` rows only) | dab6e00fc3ccf82f015941bc767a10b18be9e6ca5f1c8598fa1fe9a4d05743f7 |
| /tmp/opensip-implementation/m1-full-generator-trial-01/source-map.json | 593a0d87845c494c56199cac44c1e068cc7133d7f8920a7ba9e4bf33ad5cf113 |
| /tmp/opensip-implementation/m1-full-generator-trial-01/result.json | 3cba09e1c309996a083075c6b44e753ac7e54bb989b92eb87e6f1f2977687aac |

Membership: every owner cited below is a byte-matching member of
candidate-subject.v45, including delivery.v2 and rust-provider-protocol.v2. The
exception is the three `docs/implementation/m1/metadata-v1/*` paths. Application46
`files` after-images match current bytes for the rows it carries.

## 1. Trial facts that change the plan

1. **Metadata-v1 paths are wrong for the trial.** It registers
   `docs/implementation/m1/metadata-v1/{command-envelope,command-inventory,metadata}.schema.json`.
   Their bytes match metadata-v2 (6b5638…, b3ab43…, a58de9…). The accepted unit is
   metadata-v2, and build plan §724–731 requires the canonical path of the selected
   owner. The registry rows must name `metadata-v2/` paths. No byte change is needed.
2. **The trial generated nothing.** result.json shows exitCode 101 and outputBytes 0.
   typify-impl 0.8.0 panics with `if/then/else schemas are not supported`, and 19 of
   the 28 documents use if/then/else, including envelope4 (21 sites), inventory4 (11),
   identity v3 (12) and invocation3 (29). Even the schema-native subset has no working
   generator yet. That is the first blocker, ahead of any protocol projection.
3. **The "old" docs are required dependencies, not leftovers.** A `$id`-keyed ref
   closure from envelope4, inventory4 and metadata1 reaches 19 documents, including
   `evaluator3:command-envelope:3` (via inventory4 → envelope3),
   `evaluator3:command-inventory:3` (via invocation3), `workflows:policy-document`
   (v1), `workflows:policy-test` (v1) and `workflows:common`. You cannot drop them to
   avoid name collisions. Across the 28 documents, 100 definition names repeat.
4. **Three definitions inside the 28 are superseded.** `native-evidence.schemas.v2.json#/$defs/HelloV3`,
   `HelloAckV3` and `ProtocolLimitsV3` are superseded by the same-named definitions in
   `provider-handshake.schemas.v1.json` (native-evidence.md §0, last native row). The
   only ref to them is HelloV3 → ProtocolLimitsV3 inside the same superseded group,
   so excluding all three leaves the closure intact. The trial's
   "every root/definition" selection emits both copies.
5. **AtomSuccessorV1.** `policy-document.v2.schema.json#/$defs/AtomSuccessorV1` is a
   "Proposed Atom extension". Its `filters/items` ref `#/$defs/FieldFilterSuccessorV1`
   is dangling, and nothing references it. This is the only dangling ref in the 28.
   Under a roots-based closure it is not selected, so no special exclusion is needed.
   The trial's ad-hoc exclusion remains unaccepted.

## 2. Output-by-output owner map

| Output | Schema-native owners available (in the 28, with corrections) | Missing owner / translation |
|---|---|---|
| crates/contracts/src/generated/identity.rs | identity-schemas.v3.json | none found |
| crates/contracts/src/generated/evidence.rs | native-evidence.schemas.v2 (excluding HelloV3/HelloAckV3/ProtocolLimitsV3), fact-batch v3, occupancy-companion v1, dispatch-binding v1, imported-evidence, test-execution | none required. Selection of explicit def entrypoints is still needed. |
| crates/contracts/src/generated/invocation.rs | evaluator3 invocation-record:3 (+ its closure) | none found |
| crates/contracts/src/generated/output.rs | metadata-v2 envelope4, inventory4, metadata1 (+ closure incl. envelope3/inventory3) | **Report projection schema owner not named** (G10) |
| crates/contracts/src/generated/protocol.rs | provider-handshake v1, provider-startup v1, fact-batch v3; native-evidence DependencySourceManifestV3/DependencySourceSealV3/RepositoryResolutionV3/UnavailableReasonV3/PreparedOutputSetV3/PreparedOutputRowV3/CoverageResultV3/CoverageKeyV2 | **TS2 and Rust3 envelopes, frame tables and retained payloads (field grammars); common control frames (no owner)** |
| crates/contracts/src/generated/mod.rs | module-index only; registry bytes are its input | none. It must list exactly the Rust recipe's siblings, so all six Rust files belong to one recipe. |
| providers/typescript/src/generated/protocol.ts | TS subset of provider-handshake/startup, fact-batch v3, occupancy, CoverageResultV3 closure | **TS2 envelope, frame table and retained payloads (field grammar)** |
| apps/report/src/generated/report.ts | "same selected output schema as Rust" (chapter 14 row 556) | **Report projection schema document not identified** (G10) |

## 3. Missing required surfaces: exact source, selector and standing

### 3.1 typescript-semantic protocol major 2 (protocol.rs, protocol.ts)

Base: `docs/coop/artifacts/delivery.v2.json` sha256
`47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3`. The prefix is `$.typescriptSemanticSubstrate.providerProtocol.wireSchema`, and it is a
field-description grammar (`closed/required/optional/fields` with prose types). The
disposition authority is native-evidence.md §0 (sha 83b99783…ca0) plus §9.4/§9.7.

| Selector under wireSchema | Standing per §0 | Replacement / action |
|---|---|---|
| `frameEnvelope` | retained; `fields.protocolMajor` value superseded 1→2 | translate with value 2 |
| `frameSchemas` | retained; extended with worker→host `NativeContextVerified` | translate + add row (payload `NativeContextVerifiedV1`, provider-startup) |
| `payloadSchemas.HelloV1`, `HelloAckV1` | superseded | `TypeScriptHelloV2`/`TypeScriptHelloAckV2` (provider-handshake) |
| `payloadSchemas.OpenUniverseV1`, `UniverseAcceptedV1`; `definitions.SnapshotId`, `PlanId`, `TypeScriptSemanticUniverseV1`, `TypeScriptSemanticUniverseKey` | superseded for major 2 | `TypeScriptOpenUniverseV2`/`TypeScriptUniverseAcceptedV2`/`TypeScriptSemanticUniverseV2`, `SnapshotId2`/`PlanId2` (provider-startup) |
| `payloadSchemas.CoverageV1`, `UnavailableV1`, `BudgetExhaustedV1`; `definitions.CoverageResultV1` | superseded | `TypeScriptCoverageV2`, `TypeScriptUnavailableV2`/`PreAnalyzeUnavailableV1`, `TypeScriptBudgetExhaustedV2`; entries `CoverageResultV3` |
| `payloadSchemas.FactBatchV1` | retained when `target-attribution-v2` not negotiated | translate. The negotiated form is `FactBatchV3` (schema-native). |
| `payloadSchemas.SnapshotManifestV1`, `SnapshotFileChunkV1`, `SnapshotSealV1`, `SnapshotAcceptedV1`, `AnalyzeV1`, `CompleteV1`, `CancelV1`, `CancelledV1` | not listed as superseded → retained (CancelledV1 semantics extended, no enum change) | **translate** |
| `definitions.DigestHex`, `Sha256Text`, `ExecutionId`, `PlanIntentCommitment`, `SnapshotEntryV1`, `ProviderWorkBudgetV1`, `StageRequestV1`, `SnapshotFileSubjectV1`, `SubjectScopeV1`, `RequestedCoverageDomainV1`, `AnchorRefV1`, `FactCandidateV1`, `CoverageKeyV1`, `StageResultV1` | retained (ExecutionId/PlanIntentCommitment explicitly; universe-typed members of CoverageKeyV1/FactCandidateV1 re-typed; StageResultV1.coverageCommitment recommits over V3 values) | **translate** |
| `limits` (10 numeric members) | retained; already schema-native as `TypeScriptProtocolLimitsV1` | none |
| `commitments`, `canonicalCbor`, `multiStageAnalyze`, `stageRequestProjection`, `coverageDomain` | retained policy/recipes | not carriers. Handwritten owners; do not generate. |

### 3.2 rust-semantic protocol major 3 (protocol.rs)

Base: `docs/coop/artifacts/rust-provider-protocol.v2.json` sha256
`6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b`, prefix
`$.wireSchema`. Its in-file status is `CANDIDATE-NOT-APPLIED`. It is nevertheless the
**selected inherited base**: native-evidence.md §9.1 pins these bytes as the
`HelloV3.expectedProtocolContractSha256` subject. The v3/v4 artifacts in the same
directory are not the owner. The frame table is §9.2, and the transition table is
protocol3-transitions.v1.json (sha b0aca55d…), whose `rowPayloads` name payloads only
for P3-01/02/03/04/20/21/24/25/26.

| Selector | Standing per §0/§9 | Replacement / action |
|---|---|---|
| `envelope` (`RustProviderEnvelopeV2`) | retained; `fields.protocolMajor` value superseded 2→3 | **translate**. No V3 envelope name is given (gap G4). |
| `frameSchemas` | `Coverage` renamed `CoverageV3`; §9.2 adds DependencySource{Manifest,Chunk,Seal,Accepted}, NativeContextVerified | **translate + add rows** from §9.2 table |
| `payloadSchemas.HelloV2`, `HelloAckV2`; `definitions.ExpectedRustIdentityV2`, `RustProviderCapabilityV2` | superseded | `HelloV3`/`HelloAckV3`/`ExpectedRustIdentityV3`/`RustCapabilitiesV3` (provider-handshake) |
| `limits` | superseded | `ProtocolLimitsV3` (provider-handshake) |
| `payloadSchemas.OpenUniverseV2`, `UniverseAcceptedV2`; `definitions.SnapshotId`, `PlanId`, `RustUniverseV1` | superseded | `OpenUniverseV3`/`UniverseAcceptedV3`/`RustSemanticUniverseV2`, `SnapshotId2`/`PlanId2` (provider-startup) |
| `payloadSchemas.CoverageV2`, `UnavailableV2`, `BudgetExhaustedV2`; `definitions.CoverageResultV2`, `StageResultV2`, `RepositoryResolutionV2` | superseded | `CoverageV3`, `UnavailableV3`/`PreAnalyzeUnavailableV1`, `BudgetExhaustedV3` (provider-startup); `RepositoryResolutionV3`, `CoverageResultV3` (native-evidence.schemas) |
| `payloadSchemas.FactBatchV2` | retained when `target-attribution-v2` not negotiated | **translate** |
| `payloadSchemas.SnapshotManifestV2`, `SnapshotFileChunkV2`, `SnapshotSealV2`, `SnapshotAcceptedV2`, `AnalyzeV2`, `CompleteV2`, `ProviderFaultV2`, `CancelV2`, `CancelledV2` | not superseded → retained | **translate** |
| `payloadSchemas.PreparedOutput{Manifest,Chunk,Seal,Accepted}V2` | §9.2: "as above for inert rows only"; row kinds restricted (§3.6) | **gap G6**: modified, no field-level successor |
| `definitions.IdentityText`, `DigestHex`, `Sha256Text`, `CanonicalPath`, `ToolPathV2`, `SnapshotEntryV2`, `PreparedOutputBlobV2`, `PreparedOutputEntryV2`, `C2PlanStageV3`, `SubjectV2`, `CoverageKeyV2`, `StageAnalysisDomainV2`, `StageRequestV2`, `FactCandidateV1` | retained (universe-id values substituted per §9.7) | **translate**; name clashes G7 |
| §9.2 `DependencySourceManifest`/`DependencySourceSeal` | new | schema-native `DependencySourceManifestV3`/`DependencySourceSealV3` |
| §9.2 `DependencySourceChunk` | new; member list only | **gap G5** |
| §9.2 `DependencySourceAccepted` | new; "exact seal echo" | derivable as SealV3 shape; name needs a reviewed choice |
| `limitPolicy`, `limitsHandshake`, `commitments`, `canonicalCbor`, `schemaLanguage`, `orderingAndStateMachine`, `planAndDomainProjection`, `requestProjection` | retained law/recipes | not carriers. Handwritten owners. |

### 3.3 Common control frames (protocol.rs "negotiated control/provider frame carriers")

Chapter 14 row 431 names `crates/components/src/control_protocol.rs` ("common control
frames"). `02-distribution-and-components.md` (sha 5a110ef0…) mentions a common
control protocol but says "Concrete schemas remain DR-103". The bounded search (v2
architecture/contracts, native and v13 inputs) found **no JSON Schema and no field
grammar** for control frames. This is gap G9: there is no current source owner. Do
not invent one. Either the owner names a source, or protocol.rs explicitly carries
provider frames only and the control portion is recorded as unowned/open.

### 3.4 Report projection (output.rs, report.ts)

Chapter 14 says report.ts is generated "from the same selected output schema as
Rust", and output.rs holds "command envelope and report projection carriers".
report-asset-binding.v1.json requires `projectionSchemaSha256s` over "complete
supported report projection schema document(s)". No document in the 28 or in the
bounded contract search is identified as *the* report projection schema. This is gap
G10. The registry needs an explicit reviewed owner mapping (build plan §729–730).
Deriving it from a filename or from envelope4 by assumption is not acceptable.

### 3.5 Security/private lifecycle schemas absent from the 28

| Path | sha256 | Finding |
|---|---|---|
| docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json | f66d2c617084825e3cdb9a855a151c10aa66625968b40ef91fc6bb3be39423f4 | Container document (`schemas` map, no `$id`) of security/lifecycle records |
| docs/v2/architecture/attempt-custody.schema.v1.json | 60a881545e63a9e8e1601c874c048aacf26f52ed6761a6489f8075fc9993d2ab | Self-described "Private local operational record. Not a public request, wire schema…" |
| docs/coop/design-corrections/security/carrier-highwater.schema.v1.json | 1bbfd9135bd9492ef5b1df328aacdb959b0440a9e21312763f88609f4b966f82 | Private per-carrier floor |
| docs/coop/completion/security-schemas.v2/journal-record.schema.json | 3c090afa5f6232f626d234f8c40e77615779557609302f6666f8090dde0ad63d | Journal record (v13 input) |

All are v13 inputs and source45 members. None is referenced by any of the 28. The
eight generated inventory rows describe public inert contract carriers
(identity/evidence/invocation/output/protocol, TS protocol, report). **These schemas
are not required inputs for the eight outputs.** Their admission belongs to
handwritten security/storage owners (M2). If any is later registered,
security-lifecycle needs an explicit owner mapping because it has no `$id` or major.

## 4. Smallest correct generation entrypoint/owner strategy (recommendation)

1. **Three recipes.** Recipe `contracts-rust` owns all six Rust files, which is
   forced by the mod.rs sibling rule. Recipe `typescript-provider-protocol` owns
   protocol.ts. Recipe `report-projection` owns report.ts. Sources can be shared, but
   outputs cannot.
2. **Explicit root entrypoints per output, closure by `$ref`.** Replace "every
   root/definition" with a reviewed options file that lists `{schemaId, pointer}`
   roots per output file. Take the transitive closure within registered sources. This
   leaves out AtomSuccessorV1 with no special case and makes superseded-def exclusion
   explicit.
3. **Superseded definitions are a denylist in the options file**, each row carrying
   `{sourceSha256, pointer, supersededBy:{sourceSha256, pointer}, authority:"native-evidence.md §0"}`.
   The initial rows are native-evidence HelloV3/HelloAckV3/ProtocolLimitsV3 →
   provider-handshake. A root or closure that reaches a denied pointer refuses.
4. **Namespacing by schema `$id` and major, never by bare def name.** Generate one
   Rust submodule per registered `$id` inside each output file, for example
   `output::workflows_evaluator3_command_envelope_v4::CommandEnvelope` versus
   `…_command_envelope_v3::…`, `workflows_common` versus `workflows_evaluator3_common_v3`,
   and `policy_document_v1` versus `policy_document_v2`. The TS files use the same
   segments as export-name prefixes or namespaces. Keep the mapping table `$id` →
   module segment in the options file. Do not dedupe identical-looking defs across
   documents: 100 collisions, many with different majors.
5. **Protocol field grammars get new derived JSON Schema projection documents, not
   generator-side parsing of prose.** Create, under a later reviewed task, two
   documents with distinct `$id`s such as
   `urn:opensip:implementation:m1:projection:typescript-semantic-protocol:2` and
   `…:rust-semantic-protocol:3`. Each def carries provenance
   `{sourcePath, sourceSha256, selector, disposition: retained|value-substituted|extended}`.
   These documents are registered sources with `semanticValidatorOwner` naming the
   handwritten admission, and they `$ref` provider-handshake/provider-startup/fact-batch/native-evidence
   for superseding types. Put language in the namespace
   (`protocol::typescript2::FactCandidateV1` versus `protocol::rust3::FactCandidateV1`)
   because the two bases define different same-named records (FactCandidateV1,
   DigestHex, Sha256Text, SnapshotId, PlanId). The TS provider recipe roots only the
   typescript2 projection plus TS handshake/startup defs, and never Rust3 carriers.
6. **Generator dialect.** The recipe needs a generator closure that handles 2020-12
   `if/then/else`, or a separately reviewed dialect adapter whose loss is tested (as
   metadata-v2 did for the reference validator). The current typify 0.8.0 trial
   cannot produce any of the eight files.

## 5. Can the schema-native subset ship as staged partial implementation?

**Yes, conditionally, as a labelled engineering checkpoint. It must not claim M1
complete.** The constraints come from the accepted text:

- Build plan §748 says "The initial recipe covers all eight generated inventory
  files", and §757–765 says every inventory path occurs exactly once, with generator
  selection "before creating generated product files, using … a drift trial that
  exercises all eight target files". Checking in a generated product tree that
  omits protocol.rs, protocol.ts or report.ts would contradict this.
- The consistent staged form is to generate **all eight files** in the drift trial.
  identity/evidence/invocation/output/mod are full. protocol.rs and protocol.ts
  contain only the schema-native handshake/startup/fact-batch/native-evidence subset.
  report.ts is blocked on G10 unless an owner is mapped. The registry or coverage then
  records the open projection sources G1–G10 as unresolved, and the M1 completeness
  check must fail while they are open. No handwritten stand-in carriers go into
  `generated/`.
- M1's stated demonstrations (help/version envelope4 metadata, identity vectors) use
  output.rs and identity.rs, not provider frames. Provider protocol consumers are M3.
  Staging does not block the M1 metadata path.
- Precondition: none of this ships until a generator actually emits the
  if/then/else-bearing schemas (§1.2).
- Whether an eight-file drift trial with a partial protocol population satisfies
  §765 is an interpretation for the root reviewer. This audit does not approve it.

## 6. Translation classification

**Required (M1 complete / eight-file coverage):**

- T1: TS2 projection of delivery.v2 retained selectors (§3.1 "translate" rows), with frameEnvelope protocolMajor=2 and the NativeContextVerified frame row.
- T2: Rust3 projection of rust-provider-protocol.v2 retained selectors (§3.2 "translate" rows), with envelope protocolMajor=3, CoverageV3 rename and the §9.2 new frame rows.
- T3: Report projection owner mapping (G10). This is an owner decision, not a translation, and must precede report.ts.
- T4: Control-frame owner decision (G9). Either name a source or explicitly scope protocol.rs to provider frames.
- T5: Registry path correction from metadata-v1 to metadata-v2 (same bytes).
- T6: Superseded-def denylist and `$id` namespacing table (options file).

**Precision gaps to resolve during T1/T2 (do not invent):**

- G1: TS2/Rust retained fields use prose types ("exact OpenUniverse value", "current requested stage", "uint64 exactly 0"). The carrier type must come from the referenced member. Constraint text stays with handwritten admission. Only HelloV1/FactBatchV1/CancelledV1/AnalyzeV1 and six definitions were sampled here, so a per-field table is required.
- G2: `SnapshotId`/`PlanId` are superseded (snapshot2/plan2) only through §9.7's "every later member that is an exact echo carries the same text". Retained payloads (SnapshotManifest, Analyze, and so on) need a recorded substitution per selector.
- G3: Universe-coordinate members in retained TS `CoverageKeyV1`/`FactCandidateV1` and Rust `CoverageKeyV2`/`StageRequestV2` change value domain (native semantic-universe id / 64-hex suffix). Each must be recorded as value-substituted.
- G4: No name is given for the major-3 Rust envelope (only the protocolMajor value is superseded). A reviewed name is needed; do not silently reuse `RustProviderEnvelopeV2`.
- G5: `DependencySourceChunk` has only a member list in §9.2 (`dependencySourceSetId, packageKey, path, chunkIndex, byteOffset, bytes`), with no wire types or bounds.
- G6: `PreparedOutput{Manifest,Chunk,Seal,Accepted}` for major 3 is "as above for inert rows only". It is not stated whether manifest entries stay `PreparedOutputEntryV2` or use native-evidence `PreparedOutputRowV3`.
- G7: Same-named records across owners: `CoverageKeyV2` (rust-provider-protocol.v2 definitions and native-evidence.schemas.v2) and `FactCandidateV1` (delivery.v2 and rust-provider-protocol.v2). They were not compared in this audit. The owner selection must be explicit.
- G8: `DependencySourceAccepted` is an "exact seal echo" with no record name.

**Optional / not needed as generation inputs:**

- delivery.v2 `commitments`, `canonicalCbor`, `multiStageAnalyze`, `stageRequestProjection`, `coverageDomain`, `supervision`, `identity`. These are retained law for handwritten codecs and admission.
- rust-provider-protocol.v2 `limitPolicy`, `limitsHandshake`, `commitments`, `schemaLanguage`, `orderingAndStateMachine`, `planAndDomainProjection`.
- protocol3-transitions.v1 and typescript-protocol2-order.v1. These are state-machine tables for handwritten supervisors, not carriers.
- security-lifecycle.schemas.v1, attempt-custody.schema.v1, carrier-highwater.schema.v1, journal-record.schema (§3.5).
- Other historical protocol versions (rust-provider-protocol v1/v3/v4, delivery v1/v3–v5) are not owners for TS2/Rust3 carriers.
- `x-opensip-startup-law` and similar `x-` annotations: the generator must ignore them as validators.

## 7. Limits of this audit

- Rust/TS retained-payload field precision was sampled, not exhaustively tabulated.
- The control-frame and report-projection "not found" results cover the bounded
  sources listed above, not every historical document.
- No generator, drift trial or schema validation was run. Checks were limited to
  hashes, `$id`/`$ref` closure, def-name collisions, if/then/else counts and manifest
  membership.
