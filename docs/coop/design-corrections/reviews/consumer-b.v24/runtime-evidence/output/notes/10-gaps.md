# Phase 10: design gaps, algorithm freedom and blockers (R-IDENTIFY-GAPS, R-FREEDOM-VS-MISSING, R-BLOCKER-NOT-ADJUST)

## Adjudication rules

- **Algorithm freedom.** The kit fixes the observable result, and hosts may reach it any way they like. Examples: the physical graph accelerator, BFS implementation, store layout, and parsing strategy behind admitted canonical bytes. Freedom is not an issue.
- **Missing or contradictory contract.** Two conforming readers of the selected kit mint different identity-bearing bytes, admit different Runs, produce different public results, or cannot represent a required public field without inventing one. That is a design gap.
- **Severity.**
  - **MUST:** the gap makes a lawful required result unreachable, makes a valid Run unclosable, or leaves identity-bearing bytes undetermined.
  - **SHOULD:** a public or cross-host result is undetermined or contradictory, but it is bounded and does not block the Run itself.
  - **Advisory:** internal naming, drift the kit itself discloses, or process notes.
- **Helper bugs are not gaps.** Every helper failure was corrected from the kit, with the original preserved (HC-1…HC-13).
- **Evidence standard.** Each issue below was re-verified against the exact selector in this session, and most were measured on executed Runs. None depends on an author model.

## MUST

### M1 Required clones-fact census makes default TypeScript/syntax Runs permanently indeterminate; Rust passes the same shape

**Selectors**
- native-evidence.md line 789: default selection requests every registered capability, `required=true`.
- enumeration-plan.schema.v1 `x-opensip-kind-derivation` gives `clones-fact` kinds `[file]`, and `x-opensip-file-membership-extent-law.fileKind` puts every scoped first-party path in that extent, "including data-document, unsupported-file, extensionless".
- identity-schemas.v3 `x-opensip-digest-domains/scopeCapabilityLaw` (TypeScript) and native s1.2 (syntax grammars) force a `language-tier-unsupported`/`capability-missing` partition over those paths.
- execution-inputs contract s5 turns that partition into a required-cell deficiency.
- Contradicted by native-evidence.md line 443: "No syntax Run is made blanket-indeterminate…".

**Measured** (fresh-process closure + replay)
- `ts-clones-required` (tsconfig unit plus its own `package.json`/`tsconfig.json`): ADMIT; every rule passes; the sealed verdict is **indeterminate**.
- `syntax-mixed-disclosed` / `syntax-mixed-omitted`: indeterminate.
- `syntax-mixed-falsecomplete`: REFUSE.
- `rust-mixed-clones-required`, same shape (unit plus `Cargo.toml`/`Cargo.lock`): ADMIT, **pass**.

**Gap.** Under the default profile, no TypeScript unit can seal pass, because a tsconfig unit cannot exist without such files. The census law is also not uniform across universes. This is a contradictory required recipe, not freedom.

### M2 `program-predicate.nodeDigest` names the policy-1 Predicate schema for RuleProgramV2 nodes

**Selector.** foundation/identity-schemas.v3.json `#/$defs/program-predicate/properties/nodeDigest/x-opensip-digest`, lines 2793-2805, names `workflows/schemas/policy-document.schema.json#/$defs/Predicate` with retention `fragment`, located in `ruleProgramDigest` `rules[ruleId].emitWhen`. The program it digests is `policy-document.v2.schema.json#/$defs/RuleProgramV2`.

**Measured**
- The v1 `Predicate` refuses an atom carrying `endpoint`; the v2 `Predicate` admits it.
- `syntax-code~explicit-endpoint-source`, whose atom spells the default `endpoint:"source"`: REFUSE `DIGEST_FRAGMENT_RECORD_REFUSED:$.nodeDigest:policy-document.schema.json#/$defs/Predicate`, reached through `proof.predicateProofs[0].witnessDigest → programPredicateDigest → nodeDigest`.
- The same policy without that spelling: ADMIT.

**Gap.** Every Run whose policy uses a v2-only atom field, including every incoming `endpoint=target` atom, is unclosable under the published digest law. This is conflicting vocabulary in an identity-bearing annotation.

### M3 UnitMembershipV1 unit and row order, and `unitOrdinal` assignment, are unpublished but identity-bearing

**Selectors**
- native-evidence.schemas.v2.json `#/$defs/UnitMembershipV1`: `units` and `rows` are both `x-opensip-order: sequence` (lines 5004-5020).
- native-evidence.md U-1…U-4 (lines 610-646) define which units and rows exist, never their order or ordinal assignment.
- U-4a (line 649) says the rules are "stated once, in `docs/coop/design-corrections/discovery-defaults.py`". That file is **not in the kit**: the manifest has 102 files and no `discovery-defaults*` is present.
- `EnumerationPlanV1.membershipDigest` = raw SHA-256 of C(UnitMembershipV1), which feeds the analysis-spec parameter, then `analysisSpecDigest`, then **PlanId**.

**Measured.** `syntax-code~membership-reordered` has its rows reversed. That is schema-valid, and it is refused only by this reconstruction's own chosen derivation order (`cb24.UNIT_MEMBERSHIP_DERIVATION`).

**Gap.** Two conforming hosts mint different PlanIds for one repository. The recipe lives in an excluded file, so any reader must invent it.

### M4 `detectorId` has no derivation, yet it is identity-bearing in portable baselines and the E0 detector join

**Selectors**
- evaluator3 `baseline-artifact.schema.json` `#/$defs/DetectorClosureEntry` and `#/$defs/BaselineEntry` both require `detectorId`, a CanonicalIdentifier with no description. DetectorClosureEntry also carries a separate `contributionId`.
- `comparison-result.schema.json` Entry and DetectorDisposition likewise.
- workflow-projection-contract.v3 s11 (line 190): "E0 detector join is the exact baseline selected `{detectorId → (closureId, semanticsMajor)}` map … Extra, missing, or major-disagreeing detectors refuse".
- evaluator-emission-plan rows carry `contributionId`/`ruleStableId`/`detectorClosure` but no `detectorId`.
- A kit-wide search finds no other definition.

**Measured.** This reconstruction had to choose `detectorId = contributionId` (vectors/baseline-audit.json `cb24Choices`). That choice enters `baselineId = H('workflow.baseline', descriptor)`.

**Gap.** A baseline exported by one conforming host has a different identity, and fails the exact E0 map join, on another. That defeats the "Fresh CI" portability of workflows s2 lines 274-283.

### M5 The query parity field `query-response` has no carrier in the JSON parity reference

**Selectors**
- workflows-and-surfaces.md lines 1055-1060: the query command's parity fields include `query-response`, "the complete owner-admitted GraphQueryResponseV1 … human, JSON and agent renderers preserve its typed content".
- workflows/command-inventory.v3.json query `parityFields`.
- The renderers table: "the CommandEnvelope major 3 is the parity reference for every other renderer".
- `workflows/schemas/evaluator3/command-envelope.schema.json` is `additionalProperties: false`. Its fields are schemaFamily…findings; `query` is only the compact `QueryResult`, and no field holds a GraphQueryResponseV1.

**Measured.** vectors/graph-query.json `measuredQueryResponseCarrier`: adding the complete response to an otherwise valid query envelope is refused by the schema, for every response vector.

**Gap.** A conforming JSON renderer cannot emit a required parity field. This reconstruction carries `{envelope, queryResponse}` (cb24), which is an invention.

## SHOULD

### S1 No closed registry of stage output schema documents

- **Selectors.** identity-schemas.v3 `#/$defs/stage-spec.outputSchemaDigest` requires "exact complete registered stage output schema document bytes" (identity s3). But `x-opensip-payload-registry` lists payload and parameter documents only.
- **Measured.** `syntax-code~stage-output-schema-relation-doc` gives the same planId, a different `executionPlanId`, and both Runs ADMIT with complete replay.
- **Gap.** Hosts diverge on exec-plan2, proof3, seal3 and run3 for one Plan. It is bounded: the PlanId is stable.

### S2 Clone level-specification custody join is unnamed

- **Selectors.** `SyntaxGrammarBundleV1.normalizer.specificationDigest` is singular. FACT-IDENTITY BH-1 versions each level. Identity s3 joins `levelVersion` to "the retained specification" without naming which record carries per-level digests. TS and Rust contexts have no normalizer record.
- **Measured.** `syntax-code~clone-level-spec-not-in-grammar` is refused only by `cb24.CLONE_LEVEL_SPEC_NOT_IN_GRAMMAR_CLOSURE`; a literal reader admits it.

### S3 Zero-config syntax-only unit and scope

- **Selectors.** enumeration-contract s1 promises "one tsjs/rust/syntax-only unit per directory". But native U-1 names markers only for tsjs and rust, syntax-only files have `unitOrdinal: null` (line 178), and `unit_scope_descriptor` derives workspaceRoots from units.
- **Gap.** No rule mints the syntax-only cell or scope for a repository with no compilation unit. An explicit `.` root without a marker refuses (`native.explicit-root-without-marker`). This reconstruction used an explicit selection.

### S4 `NativeCoverageAccountV1.targetUniverse` value

- **Selector.** execution-inputs s5 says `targetUniverse` is "deliberately not joined". It never states the carried value, or whether an admitted-target relation owes one account per target universe.
- **Gap.** The field is inside C(ExecutionInputsV1), so it feeds `executionInputsDigest` and proof3. Cross-universe hosts diverge; every Run here is same-universe.

### S5 `argvDigest` recipe

- **Selectors.** Security `RepoExecutionGrantV2.argvDigest` (Hex64, no description; security-lifecycle.schemas.v1.json lines 2843/3710). security-and-lifecycle.md lines 1065, 1115 and 1122 bind "argv digest". `TestPayloadV1.argvDigest` has the same shape.
- **Gap.** No preimage or encoding is published. A grant minted by one conforming component and admitted by another cannot be matched. This reconstruction chose raw SHA-256 of C(argv) (vectors/test-prep-repair-authorization.json).

### S6 Failure goldens with no DomainDetail, although failure envelopes require `errors[]`

- **Selectors.** command-inventory.v3 goldens `doctor-report-not-producible` (operational-failed HOST.IO_FAILURE), `query-latest-empty` (request-rejected IDENTITY.UNKNOWN) and `envelope-major-unsupported` carry no `domainDetail`. The Golden schema makes it optional. command-envelope `kind=failure` requires `errors` with minItems 1.
- The route registry's `envelopeErrorsComposition` covers only native route keys. query-projection-contract s7 assigns `QUERY.VIEW_UNKNOWN` to an empty latest resolver, which `query-latest-empty` omits.
- **Measured.** envelopes/public-termination.json: 40 of 43 goldens form complete admitted examples. These 3 cannot form a failure envelope without inventing a detail.

### S7 IndeterminateReason cannot express unknown absence that has no evidence or pivot cause

- **Selectors.** comparison-result `#/$defs/IndeterminateReason` (14 members). workflows s3 lines 348-352: unknown roots or incomplete enumeration do not establish absence.
- **Measured.** tools/phase8_compare.py labels such an entry `pivot-reevaluation-unavailable` with `reasonApproximated: true`. It is the closest member, and wrong.

## Advisories

- **A1** Unannotated 64-hex digest fields: `execution-inputs.schema.v1` (16 positions) and `incoming-search.schema.v1` (3). It is not stated whether identity s3's closing digest law reaches them.
- **A2** Owner drift in selectors. `enumeration-plan.schema.v1` and `subject-inventory.schema.v1` annotations name identity-schemas.v2; the selected owner is v3. The constraints are byte-identical.
- **A3** Charter prose says "101 kit files"; the manifest lists 102 hash-exact files (runs/final-custody.json PASS).
- **A4** Whether pruned-tree bytes (node_modules, Cargo target) enter `snapshot.sourceInventory` is not decided in one place. Choice: not inventoried.
- **A5** The TypeScript universe `jsAdmittedToProgram`/`jsDiagnosticsEnabled` derivation is unwritten. Choice: allowJs, and allowJs ∧ checkJs.
- **A6** `finding.correspondence.reason` is singular while several correspondence conditions can co-occur. Choice: first in the s9.5 table order.
- **A7** `CellProgramOutcomeV1.viewDigests` observation-vs-derived standing (candidate 15).
- **A8** Abbreviated internal refusal keys (`…_CAUSE_MISMATCH`, `…_DEFICIENCY_MISMATCH`) and other unnamed internal refusals carry cb24 names in this reconstruction:
  - detector listing refusals;
  - E0 pivot joins;
  - the test consent relabel;
  - native-preparation grant joins;
  - query projectId mismatch, which has no s7 row.
- **A9** Rule outcome when a required evidenceUse kind is unavailable but the root branch is decided elsewhere (candidate 13). Choice: indeterminate for gating rules.
- **A10** D9 successor artifact. The inherited d9-exit-contract.v1.14 alone refuses the lawful `host-invariant` termination. The kit itself records a mandatory live cross-unit `successorArtifactObligation`; measured in vectors/d9-extension-precedence.json.
- **A11** `TestExecutionStepParams.effects` uses a closed `EnforcementValue` enum without the `ENFORCED-PLATFORM:<primitive>` form that its own description and security `EnforcementV1` admit. A measured platform primitive could not be expressed. Today's truth table has none.
- **A12** `gateReason` has no member for a CODE-NET-NEW entry hidden by a detector-semantics change. It gates with `code-net-new-policy-hidden`.
- **A13** A required-projection failure before commit has no registered DomainDetail for the mandatory failure `errors[]`. It is carried as a termination only (envelopes/purge-replay-output-failure.json).
- **A14** Exact-snapshot import correspondence changes `import2` on every code change. Any gating evidence rule then attributes INDETERMINATE (`evidence-content-changed`) on any source change. The kit discloses this (workflows lines 1395-1405); measured in `cmp-code-det2`.

## Blocker statement (R-BLOCKER-NOT-ADJUST)

None of these gaps blocked building the promised vectors: every acceptBlocking requirement was executed. Wherever a recipe was missing, the choice is recorded as cb24 and named here, with its selector. No meaning was adjusted to reach acceptance, and no author code was imported. Because MUST and SHOULD gaps remain, the verdict is **CHANGES_REQUIRED**, not BLOCKED.
