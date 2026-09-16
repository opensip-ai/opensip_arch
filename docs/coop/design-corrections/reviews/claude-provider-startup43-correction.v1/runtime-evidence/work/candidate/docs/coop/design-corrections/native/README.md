# Native evidence unit — reference model, schemas, cases (PROPOSED, NOT SELF-ACCEPTED)

Authored by actual Claude (native owner) under D-367 delegated design authority
for the D-371 intended product. Evidence for
[`docs/v2/contracts/product-v1/native-evidence.md`](../../../v2/contracts/product-v1/native-evidence.md).
Claude authored the initial corrections; Codex then completed integration fixes
(host composition §14, strict end assertions, removal of the premature
sufficiency shortcut); the post-reset independent Claude review of frozen
`candidate-subject.v1` (retained at `../reviews/post-reset-review.v1/`)
returned MUST-3, SHOULD-4 and SHOULD-7 against this unit, and a new Claude author
session corrected them here (handoff `../reviews/post-reset-author.v1/handoff.md`).
The second independent review, of frozen `candidate-subject.v2`, returned N-1
(nested repository/project boundaries not consumed by unit discovery) and A-3
(explicit Cargo workspace root lost member folding) against this unit; a further
Claude author session corrected them here (`PR2-P3`, `PR2-P22`). A third
independent session, a fresh blind consumer reconstruction of the accepted
`candidate-subject.v5` subset, returned M-1 (no producing recipe for
`subjectScopeCommitment`) and M-2 (no TypeScript native-context record) plus
advisories A-1/A-2 against this unit; a further Claude author session corrected
them here (`CB-M1`, `CB-M2`, `CB-A1`, `CB-A2`) and swept the contract for
integration obligations already discharged in current bytes. These
mixed-author bytes require a fresh independent review of a newly frozen subject.
Design reference only: nothing here is product implementation, a production
serializer, or OS/native qualification. No compiler, provider, Cargo, or
repository code is executed.

This revision answers the twelve retained items of
`reviews/native-author-feedback.v1.md` (F1–F12), seven further CHANGES_REQUIRED
items R1–R7 whose only retained record is `native-cases.v2.json#feedbackMap` and
the table below (no separate review document for them is retained, and none is
claimed), and the post-reset items `PR-MUST-3` / `PR-SHOULD-4`. The file
`reviews/native-fix-handoff.v3.md` is empty (interrupted session) and is cited
nowhere as evidence.

## Files

| File | Role |
|---|---|
| `native_evidence_model.v2.py` | reference model; imports `../foundation/canonical.py` (exact parse/canonical/H), `../foundation/identity-model.py` (`import2` identifier) and `../discovery-defaults.py` (the ONE shared discovery rule, including the boundary prefix rule); `discover_units`/`assign_membership`/`unit_scope_descriptor` consume the security instrument's `AdmittedBoundaryInventoryV1` (U-8); validates workflow payloads/wrapper records against the pinned workflow schema documents through a `referencing` closure (no network) |
| `native-evidence.schemas.v2.json` | the registered closed Draft 2020-12 bundle, definition count in the generated report `schemas.defs` (native payloads, units v2, the TypeScript native context family `TypeScriptNativeContextV2`/`TypeScriptToolchainIdentityV1`/`TypeScriptToolClosureV1`/`TypeScriptConfigProjectionV2`, `SubjectScopeCommitmentV1`, `CoverageAdmissionV1`, `NativeContextAdmissionV1`, `UnitDiscoveryV1`/`PrunedTreeV1`/`UnitBoundariesV1`/`AdmittedBoundaryInventoryV1`, generated-file rows, import registry rows, context, coverage, protocol, matrix, stage authority) |
| `provider-handshake.schemas.v1.json` | closed field-level provider handshake records: `TypeScriptHelloV2`/`TypeScriptHelloAckV2`/`TypeScriptProtocolLimitsV1` (typescript-semantic major 2), `HelloV3`/`HelloAckV3`/`ExpectedRustIdentityV3`/`ProtocolLimitsV3` (rust-semantic major 3, superseding the same-named definitions of the registered bundle), historical `TypeScriptFactBatchV1Vector`/`RustFactBatchV2Vector`, and the `x-opensip-wire-law` binding rules |
| `provider_wire_model.v1.py` | wire reference loaded by the model: executes the handshake and FactBatch joins a schema cannot express (descriptor digests and fields, identity/token/identityVersions echoes, contract digest, limit CBOR equality, candidate CBOR projection, TypeScript batch commitment); frames nothing and qualifies no worker |
| `provider-startup.schemas.v1.json` | closed startup and coverage successor records: `TypeScriptOpenUniverseV2`/`TypeScriptUniverseAcceptedV2`/`TypeScriptSemanticUniverseV2`, `OpenUniverseV3`/`UniverseAcceptedV3`/`RustSemanticUniverseV2`, `NativeContextVerifiedV1`, `PreAnalyzeUnavailableV1`, `TypeScriptCoverageV2`/`CoverageV3`, `TypeScriptUnavailableV2`/`UnavailableV3`, `TypeScriptBudgetExhaustedV2`/`BudgetExhaustedV3`, and the `x-opensip-startup-law` |
| `typescript-protocol2-order.v1.json` | published typescript-semantic major-2 abstract event machine: the inherited delivery.v2 order plus the section 9.4/9.7 insertions |
| `provider_startup_model.v1.py` | startup admissions and the TypeScript order interpreter loaded by the model; `provider_startup_exchange` and `pre_analyze_unavailable_conversion` live in the model because they compose the native coverage owners |
| `native-cases.v2.json` | hand-authored positive and negative/adversarial cases, counts in the generated report `cases`, with the F1–F12, R1–R7, PR-*, PR2-* and CB-* map |
| `check_native_evidence.v2.py` | pin verification, exact typed admission + schema validation, case runner, matrix validation, report writer |
| `native-capability-matrix.v2.json` | one cell per capability × language mode, counts in the generated report `matrix`, over the four machine platform ids (`linux-x86_64-gnu`, `linux-aarch64-gnu`, `macos-aarch64`, `macos-x86_64`, the security S8 vocabulary); platform-invariant design, no cell qualified |
| `native-evidence-report.v2.json` | generated report of the last pinned run (the pinned run is regenerated only after Codex re-pins; unpinned runs of the corrected bytes are retained in the author handoff directory) |
| `source-pins.v2.json` | SHA-256 of every consumed source (foundation canonical/identity/schemas, the three workflow schema documents, Config2 schema, sibling contracts), plus primary web references read on 2026-09-06 |
| `initial-author-response.json` | prior session's terminal record (quota), retained for audit; never edited |

## Commands

Run from this directory with the review environment (Python 3.12, jsonschema 4.25.1):

```
/tmp/opensip-architecture-review-env/bin/python -I -B check_native_evidence.v2.py --regenerate-pins
/tmp/opensip-architecture-review-env/bin/python -I -B check_native_evidence.v2.py
```

The first command rewrites `source-pins.v2.json` from current bytes; the second
refuses to run cases if any pinned byte differs (exit 2), otherwise runs all
cases and exits 0 only when every case passes, every capability×mode cell is
present, every object schema is closed, and every item F1–F12 and R1–R7 has at
least one case. Reviewers should run only the second command against the
delivered pins.

## Exact replacement selector table

| Pinned source | Selector | Disposition | Contract § |
|---|---|---|---|
| `docs/coop/artifacts/delivery.v2.json` | `$.rustSemanticSubstrate.repositoryExecution.withGrant` | superseded (disclosed trusted-code execution; `DISCLOSURE-ONLY` unless truth table says otherwise) | §5 |
| `docs/coop/artifacts/delivery.v2.json` | `$.rustSemanticSubstrate.offlineAssets` | extended (sealed `DependencySourceSetV1`) | §3 |
| `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.wireSchema.definitions.CoverageResultV1.completenessRule` | superseded (`CoverageResultV3`, five-state resolution completeness) | §4.3 |
| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.repositoryExecution.preparedOwner`, `$.repositoryExecution.forbidden` | relabeled (design invariant, not confinement; worker executes nothing) | §5.3, §5.5 |
| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.wireSchema.definitions.RepositoryResolutionV2`, `...CoverageResultV2`, `$.wireSchema.payloadSchemas.UnavailableV2.fields.reason`, `$.limits`, `$.orderingAndStateMachine.stateRecord.phaseValues` | superseded (protocol major 3, identity negotiation) | §9 |
| `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.providerProtocol.major`, `...wireSchema.frameEnvelope.fields.protocolMajor`, `...wireSchema.payloadSchemas.HelloV1`, `...HelloAckV1` | superseded (typescript-semantic major 2: `TypeScriptHelloV2`/`TypeScriptHelloAckV2`, every inherited member kept) | §9.4 |
| `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.payloadSchemas.FactBatchV1`, `...frameSchemas.FactBatch.payloadType`, `...commitments.domains.factBatch` | retained without `target-attribution-v2`; `FactBatchV3` with it | §9.1, §9.6 |
| `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.providerProtocol.ordering.normalPhases`, `...closedWorkerToHostFrames`, `...wireSchema.frameSchemas` | extended (`NativeContextVerified` before Analyze) | §9.4 |
| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.protocolIdentity.protocolMajor`, `$.wireSchema.envelope.fields.protocolMajor`, `$.wireSchema.payloadSchemas.HelloV2`, `...HelloAckV2`, `$.wireSchema.definitions.ExpectedRustIdentityV2` | superseded (rust-semantic major 3: `HelloV3`/`HelloAckV3`, identity and contract digest kept) | §9.1 |
| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.wireSchema.payloadSchemas.FactBatchV2`, `$.wireSchema.frameSchemas.FactBatch.payloadType` | retained without `target-attribution-v2`; `FactBatchV3` with it | §9.1, §9.6 |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` (registered bytes kept) | `#/$defs/HelloV3`, `#/$defs/HelloAckV3`, `#/$defs/ProtocolLimitsV3` | superseded by `provider-handshake.schemas.v1.json` | §0, §9 |
| `docs/coop/artifacts/delivery.v2.json` | `...payloadSchemas.OpenUniverseV1`, `...UniverseAcceptedV1`, `...definitions.SnapshotId`, `...PlanId`, `...TypeScriptSemanticUniverseV1`, `...TypeScriptSemanticUniverseKey` | superseded (major 2: `TypeScriptOpenUniverseV2`/`TypeScriptUniverseAcceptedV2`, snapshot2/plan2, native universe identity) | §9.7 |
| `docs/coop/artifacts/delivery.v2.json` | `...payloadSchemas.CoverageV1`, `...definitions.CoverageResultV1`, `...UnavailableV1`, `...BudgetExhaustedV1`, `...StageResultV1.fields.coverageCommitment`, `...CompleteV1.fields.coverageStreamCommitment`, supervision `coveragePayload` rows | superseded (frame `Coverage` kept; `CoverageResultV3` entries in the inherited wrappers) | §9.7 |
| `docs/coop/artifacts/delivery.v2.json` | `...ordering.unavailableTerminal`, `...supervision.cleanUnavailable.allowedImmediatelyAfter`, `...CancelledV1.fields.observedPhase` | extended (pre-Analyze `Unavailable`; `snapshot` over the inserted interval) | §9.7 |
| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `...OpenUniverseV2`, `...UniverseAcceptedV2`, `...definitions.SnapshotId`, `...PlanId`, `...RustUniverseV1`, `$.planAndDomainProjection` universe id algorithms | superseded (major 3: `OpenUniverseV3`/`UniverseAcceptedV3`, derived modes) | §9.7 |
| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `...frameSchemas.Coverage`, `...CoverageV2`, `...UnavailableV2`, `...BudgetExhaustedV2`, `$.commitments.stageCoverage`, `$.commitments.coverageStream`, `...StageResultV2` | superseded (frame `CoverageV3`; `CoverageResultV3` entries; pre-Analyze payload at P3-21) | §9.2, §9.7 |
| `docs/coop/artifacts/resolved-inputs.v2.json` | `$.planIdContract.semanticUniverseSchemas.rust-v1.resolvedInputs`, `...typescript-v1.resolvedInputs` | superseded (`rust-v2`, `typescript-v2`) | §2 |
| `docs/coop/artifacts/resolved-inputs.v2.json` | `$.projectModel.semanticUniverse.perProvider.{rust,typescript}.ifIncomplete` | superseded (`input-closure-incomplete`) | §10 |
| `docs/coop/artifacts/fact-plane.v1.json` | `$.sufficiency.rule`, `$.sufficiency.completenessRule`, `$.deficiencyVocabulary.values`, `$.requirementSchema.fields.completeness`, `$.knownLimitations[5]` | superseded (requirement v2, view entry v3, sufficiency v2) | §4 |
| `docs/coop/artifacts/fact-plane.v1.json` | `$.relationRegistry.relations`, `$.factRecordContractV1.relationPayloadSchemaRegistryV1.schemas` | extended (`unresolved-edge`; grammars reused inside `fact2`) | §4.4 |
| `docs/coop/artifacts/check-fact-plane.py` | `sufficiency` (lines 571–612) | superseded (`sufficiency_v2`, no early exit; v1 kept as oracle) | §4.6 |
| `docs/coop/completion/language-quality-matrix.completed.v2.json` | `$.rows` | extended (JS, Rust, cross-TS/JS cells) | §1 |
| `docs/coop/artifacts/c2-plan-stage-schema.v4.json` | `$.coverageKey.key[subjectScopeCommitment]` | retained (shape) and extended (successor producing recipe; the retained `SHAPE ONLY` deferral and example encoding are unchanged historical bytes) | §4.1, §4.1a |
| `docs/coop/artifacts/fact-identity-policy.v2.json` | `$.normalisationLadder`, `$.canonicalisationSchema` | retained | §6 |
| `docs/coop/design-corrections/workflows/schemas/{imported-evidence,common,test-execution}.schema.json` (current bytes) | `PayloadRegistryV1`, `ImportWrapperV2`, `RuntimePayloadV1`, `HistoryPayloadV1`, `TestPayloadV1`, `SourceCorrespondence`, `SourceMappingV1` | joined (single canonical payload per kind; raw-SHA wrapper digests; verified per-file mapping) | §7 |
| `docs/coop/design-corrections/foundation/identity-schemas.v2.json` | `scope-descriptor`, `analysis-spec`, `semantic-grant.principals[].kind` | joined (unit scopes; default capability selection; principal kind `trusted-repository-code`) | §1.4, §5.1 |
| `docs/coop/design-corrections/foundation/product-configuration.schema.v2.json` | `$.properties.discovery` | joined (explicit roots/entries/ignores consumed by unit discovery under the shared rule) | §1.4 |
| `docs/coop/design-corrections/discovery-defaults.py` (shared, new) | `enumerate_units`, `classify_path`, `normalize_explicit_root`, `conventional_excluded_prefixes`, `classify_boundary`, `classify_custody_exclusion`, `boundary_excluded_prefixes`, `boundary_inventory_from_provenance` | consumed (one discovery rule and one boundary rule for security and native) | §1.4 U-4a, U-7, U-8, Config2 join |
| `docs/coop/design-corrections/security/security_lifecycle_model_v1.py` `boundary_inventory` / `AdmittedBoundaryInventoryV1` | the admitted authority boundaries this instrument consumes | joined (security decides the boundary; native never re-derives it) | §1.4 U-8, §13 H-8 |

## Review items → resolution → cases

| # | Resolution in contract | Cases |
|---|---|---|
| F1 | four identity tokens + `identityVersions` negotiated before OpenUniverse; unspawned if absent; `fact2` for unresolved-edge | `negotiation-*`, `protocol3-open-universe-without-identity-faults`, `protocol3-happy-path-*` |
| F2 | one foundation `import2` wrapper; raw digests vs `H(domain, record)` | `import2-*` |
| F3 | DS-1 self-consistent vendored tree = `declared`; only locked tarball digest = `registry-authenticated`; mutation fixture | `ds1-*`, `ds2-*`, `ds3-*`, `ds5-*`, `missing-external-crate` |
| F4 | prepared sets are inert rows only; executable row kinds refused from import and host; dylibs load only inside `AuthorizedExecutionV2` | `prepared-*`, `stale-generated-blob-*`, `authorized-execution-*`, `execution-not-authorized-ci` |
| F5 | exact rustflags allowlist; every tool in `ToolClosureV1`; no system linker fallback | `rustflags-*`, `cargo-config-tool-outside-closure-refused`, `authorized-execution-no-bundled-linker-refused` |
| F6 | RC-2 needs attempted + exhaustive + complete stage + zero edges; bijection recheck | `rc2-*`, `coverage-bijection-*`, `protocol3-crash-*`, `protocol3-budget-*`, `computed-access-m-k` |
| F7 | `ClosedWorldV2`; `private:true` alone is unknown; dynamic edges propagate; `deadCodeRepairEligible` | `private-true-alone-is-not-closed`, `nonliteral-loading-opens-world`, `exports-open-world`, `dynamic-edge-propagates-*`, `framework-*` |
| F8 | canonical/identity imported from foundation; closed schemas; exact-int/const validator | `float-spelled-integer-refused`, `identity-vector-*`, `closed-schema-rejects-extra-property`, `native-context-v2-schema-*` |
| F9 | language stays in fact identity; `cross-tsjs` candidate mode under `tsjs-erasure-v1` | `clone-cross-tsjs-*`, `clone-false-positive-boundary` |
| F10 | verified ancestor carrier (CC-1..CC-5), private empty `CARGO_HOME`, no env, no claimed Cargo switch | `cargo-config-*` |
| F11 | `allowJs` = program membership, `checkJs` = diagnostics; effective `allowJs`: jsconfig nodes supply `true` per file before inheritance, then an `allowJs` value wins (including `false`), otherwise it derives from effective `checkJs`; `resolutionCompletenessImplied=false` | `js-allowjs-checkjs-not-completeness`, `ts-tsconfig-explicit-allowjs-false-excludes-js`, `tsconfig-checkjs-only-admits-js`, `tsconfig-checkjs-only-without-js-roots`, `jsconfig-explicit-allowjs-false-excludes-js`, `js-no-tsconfig`, `js-esm-cjs-mixed` |
| F12 | `TypeDerivationV1` provenance; `native.confidence.v1` declared-exact | `types-derivation-provenance-not-probability` |
| R1 | per-language co-located units (`WorkspaceUnitV2`); deepest-within-family membership; workspace folding; no erasure; honest unsupported files; scope descriptor | `units-*`, `mixed-native-partial` |
| R2 | `generated-file` rows + read-only virtual `OUT_DIR`; include/include_str/include_bytes consumption; strict bounds; kind decides, media type is not trust proof; capture keeps data, discards executable products | `generated-file-*`, `preparation-capture-*`, `prepared-dylib-import-refused-not-inert` |
| R3 | one canonical payload schema document per kind; adapter shapes normalize first; raw-SHA wrapper digests joined to workflow `ImportWrapperV2`; schema-document digests; `SourceMappingV1` per-file mapping | `import2-*`, `correspondence-*` |
| R4 | `repository-code` = `trusted-repository-code` = `P-TRUSTED-REPO`; `authorizationRef` outside Plan; `preparedResolution`; prepared availability implies no grant | `authorized-execution-interactive-with-declared-owner-disclosed`, `prepared-imported-inert-implies-no-host-execution-grant`, `prepared-inert-expansion-admitted-worker-executes-nothing` |
| R5 | import-only bodies excluded as candidates; kept bodies hash verbatim | `clone-import-only-body-excluded-and-kept-bodies-hash-verbatim` |
| R6 | Config2 `discovery` join; full registered TS/JS/Rust capability defaults; no preview constant | `units-default-capabilities-full-tsjs-rust-registry-no-preview`, `units-explicit-config2-workspace-root-without-marker-is-config-invalid`, `units-explicit-root-dot-*` |
| R7 | faulted worker mints no facts/Run (operational record only); admitted incomplete inputs seal an authoritative indeterminate-3 Run; existing D9 codes only, typed detail in coverage2 | `fault-worker-diagnostics-never-mint-facts-or-run`, `admitted-incomplete-inputs-yield-authoritative-indeterminate-3`, `d9-unknown-detail-never-exit-zero` |
| PR-MUST-3 | ONE shared discovery rule (`../discovery-defaults.py`): pruned trees by exact segment (node_modules, VCS, Cargo `target` only at a Cargo root); installed manifests never units; typed first-party cap; `.` sentinel and grammar shared with security | `units-installed-dependencies-are-pruned-by-segment-*`, `units-4200-installed-package-manifests-*`, `units-explicit-root-dot-*`, `too-many-units-rejected` |
| PR-SHOULD-4 | sufficiency v2 has no early exit; confidence floor evaluated for every requirement (Codex removed the shortcut; regression retained) | `sufficiency-v2-confidence-floor-precedes-one-rung-existential-shortcut` |
| PR2-P3 | admitted boundary inventory from security (nested repositories/projects, custody exclusions) consumed by unit discovery, membership and the scope descriptor; explicit roots crossing a boundary refuse; inventory not produced over this marker inventory refuses; standalone instrument discloses `source=none` | `units-nested-repository-and-nested-project-are-excluded-*`, `units-explicit-root-crossing-*`, `units-launch-inside-a-deliberate-nested-config-*`, `units-standalone-instrument-*`, `units-boundary-inventory-whose-pruned-trees-disagree-*`, `units-custody-excluded-*` |
| PR2-P22 | explicit Cargo workspace root keeps member folding and member `target` pruning; a member selected alone is its own package unit | `units-explicit-cargo-workspace-root-keeps-member-folding-and-member-target-pruning` |
| CB-M1 | `subjectScopeCommitment` = the foundation `subject-scope` (`scope2`) identity in the native `sha256:` text form, over the host's own exhaustive enumeration; checked at the admitted producer boundary (`admit_coverage_result_v3`) and at coverage use (`coverage_view_use`); no native domain, no second preimage, no claimant-supplied authority | `subject-scope-commitment-*`, `coverage-admission-*`, `coverage-commitment-chosen-by-the-claimant-*`, `coverage-producer-chosen-narrower-*`, `coverage-examined-subject-count-*`, `coverage-key-naming-a-universe-*`, `coverage-complete-claimed-over-*`, `coverage-incomplete-over-an-exhaustive-*`, `coverage-use-requires-*`, `coverage2-whose-subject-scope-*`, `coverage2-never-admitted-*` |
| CB-M2 | closed `TypeScriptNativeContextV2` (domain `native.context.typescript.v2`) carrying `typescriptStdlibMerkleRoot`, the compiler/runtime tool closure and the effective config projection; retained stdlib/compiler trees; universe and Plan binding; worker recomputation; a Rust descriptor is refused | `typescript-native-context-*`, `typescript-standard-library-change-*`, `typescript-compiler-change-*`, `typescript-stdlib-*`, `typescript-tool-digest-*`, `rust-native-context-offered-*`, `typescript-universe-bound-*`, `worker-recomputed-typescript-context-*` |
| CB-A1 | `rustcDevLlvmDigest` is cited with its nesting (`NativeContextV2.toolchain`), as is `typescriptStdlibMerkleRoot` (`TypeScriptNativeContextV2.toolchain`); both are joined by re-prefixing to `closure2:` and recomputing against the retained closure | `typescript-native-context-admits-against-retained-stdlib-and-compiler-closures`, `typescript-stdlib-merkle-root-that-names-no-retained-closure-refuses` |
| CB-M2b | Codex coauthor-note corrections on the draft: universe/context overlapping-field binding, complete stdlib declaration inventory with no basename ambiguity, deduplicating `plan.nativeContextDigests`, the corrected platform-specificity statement, and the registered coverage payload-schema digest | `typescript-universe-field-contradicting-*`, `typescript-universe-agreeing-*`, `typescript-context-bytes-that-are-not-the-admitted-ones-*`, `typescript-stdlib-inventory-missing-*`, `typescript-stdlib-tree-with-two-paths-*`, `typescript-context-identity-is-platform-specific-*`, `coverage-payload-schema-digest-a-caller-chose-*`, `typescript-universe-bound-without-the-retained-context-refuses` |
| CB-A2 | one digest, three admitted textual forms (foundation typed prefix / native `Sha256Text` / bare `DigestHex` suffix), stated in contract §11 and checked | `subject-scope-commitment-is-the-scope2-identity-in-native-sha256-text-form`, `plan-native-context-digests-are-bare-hex-while-native-records-use-sha256-text` |

## Observations and limitations

- All provider/adapter/OS observations (edges, tokens, vendored digests, stage
  terminals, ancestor config presence, environment, linker availability, `OUT_DIR`
  listings, marker files, registry rows) are fixture-asserted trusted inputs. The
  model decides host behavior; it measures nothing.
- Cargo config discovery and rustc flag semantics are pinned to primary
  documentation read on 2026-09-06 (URLs in `source-pins.v2.json`). The verified
  ancestor carrier is a first-party design rule, not a demonstrated Cargo switch.
- The static determination of `include!(concat!(env!("OUT_DIR"), …))` sites is a
  fixture input; a real site extractor and its completeness are qualification work.
- The `tsjs-erasure-v1` projection operates on token kinds supplied by fixtures;
  a real tokenizer and its determinism are qualification work.
- Protocol transitions are an abstract host machine; framing, byte limits,
  process death and EOF are not exercised.
- No cell is QUALIFIED; the four platform families are asserted design-invariant.
- The workflow schema documents and the shared discovery module are consumed by
  pinned bytes; if their owner changes them, pins fail and this unit re-pins after re-review.
- The boundary inventory is a TRUSTED ADMITTED INPUT: fixtures assert what the
  security instrument would have exported; the security checker's
  `admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery`
  sweep exercises the actual export end to end. The empty
  `reviews/native-fix-handoff.v3.md` is no longer a consumed source (its stale
  pin entry disappears when Codex re-pins).

## Handoff

All cross-owner joins are closed in contract §13 with current spellings; the
two conflicts an earlier revision recorded there (workflow auxiliary digests,
security `AuthorizedExecutionV1` spelling) are resolved in current bytes. The
H-8 integration join is implemented in `../integration-host-model.py`
(`admit_repository_discovery`) and asserted by `../check-integration.py`
(`host-nested-boundaries-*`, `security-native-shared-*`), so contract §13 no
longer records it as owed. Codex completed current pin/report recording and the
identity-contract commitment/context recipes, plus mandatory agreement between
duplicated effective compiler-option records. The host reference composes native
context admission with universe and Plan inputs, and checks the Coverage-to-view
scope join. The actual coauthor handoff and its exact original source files remain
in `../reviews/blind-corrections-author.v1/`; those earlier source hashes do not
claim to authenticate subsequent Codex integration. A new frozen subject, actual
independent review and fresh blind reconstruction are still required.
NOT SELF-ACCEPTED.
