### 9.3a Rust subject scope by reference (negotiated `subject-scope-reference-v1`)

**The inherited rule.** `rust-provider-protocol.v2` `planAndDomainProjection.subjectsAlgorithm`
puts every non-empty `.rs` file of the sealed snapshot into each Rust stage's
`analysisDomain.subjects`, inline in `StageAnalysisDomainV2`, and refuses before spawn when there
are more than `maxSubjectsPerStage` (256). `Analyze` is one frame of at most
`maxFramePayloadBytes`, and it repeats that array in every stage. The array is a pure function of
the `SnapshotManifest` the worker has already accepted, as `delivery.v2` `SubjectScopeV1` already
treats the `typescript-semantic` file set. Field-level records are in
`docs/implementation/m3/native-successors-fa/rust3-lim/design/native/rust-subject-scope.schemas.v1.json`
("the subject-scope schema"; closed, with its `x-opensip-subject-scope-law`).

**Negotiated stage requests, not a new frame.** Capability token `subject-scope-reference-v1`
(§9.1) is an optional, non-identity `rust-semantic` token, negotiated by the existing exact echo.
When it is on both Hello and HelloAck, every member of the `stages` array of the Rust `Analyze`
payload is a `StageRequestV3` instead of a `StageRequestV2`. This holds in the inherited
`AnalyzeV2` and, when `symbol-census-v1` is also negotiated, in §9.8's `AnalyzeV3`. It holds for
every subject count, 256 or fewer included. When the token is absent, `StageRequestV2` remains
unchanged. A `StageRequestV3` without the token, or a `StageRequestV2` with it, is
`PROVIDER.PROTOCOL_VIOLATION`. The token is independent of `target-attribution-v2` and
`symbol-census-v1`; every combination of the three is lawful.

**The records.**
- `StageRequestV3` = `{stageOrdinal, planStage, analysisDomain}`. `stageOrdinal` and
  `planStage` are exactly `StageRequestV2`'s, in name, type and law. `analysisDomain` is a
  `StageAnalysisDomainV3`.
- `StageAnalysisDomainV3` = `{subjectScope, requestedCoverageDomain, domainCommitment}`.
  `requestedCoverageDomain` is exactly `StageAnalysisDomainV2`'s (with §0's key-commitment rule).
  `domainCommitment` keeps its recipe, `commitments.analysisDomain` over
  `{subjects, requestedCoverageDomain}`, where `subjects` is the reconstructed array below. It
  therefore equals the `StageAnalysisDomainV2` value for the same inputs.
- `RustSubjectScopeV1` = `{scopeKind: "nonempty-rs-files", subjectCount,
  subjectScopeCommitment}`. `subjectCount` is the length of the reconstructed array, and
  `subjectScopeCommitment` is `commitments.subjectScope` over it. It carries no `snapshotId`:
  `Analyze` already carries it, and every `subjectId` hashes it.

**One array, rebuilt by both sides, never sent.** The subjects array is `subjectsAlgorithm`
steps 1, 2, 4 and 5 over the accepted manifest, with step 3's (`subjectsAlgorithm[2]`) sort,
duplicate and empty rules but without its comparison with `maxSubjectsPerStage`.
- **The host** builds it before spawn from the sealed snapshot, as now. `sameInputsRule`,
  `wireRule` and `independentDerivationRequirement` apply to `StageAnalysisDomainV3` unchanged.
- **The worker** rebuilds it after `SnapshotAccepted` from the manifest it accepted. Before any
  analysis it requires `subjectCount`, `subjectScopeCommitment` and `domainCommitment` to equal its
  own recomputation, for every stage. On any difference it ends with `ProviderFault`
  `input-rejected`, so the attempt is `PROVIDER.PROTOCOL_VIOLATION` with no facts, no Coverage
  and no Run (§10).

Membership and non-membership are proved from bytes already on the wire. The commitments that
§0 retains as the inherited proofs of the file set (`commitments.subjectScope`,
`domainCommitment`) are unchanged in recipe and value; only the array's transport changes.

**Bounds.** The limits map is unchanged: `ProtocolLimitsV3` keeps all 32 members and values,
and Hello still checks it by exact equality. Under the token, `maxSubjectsPerStage` bounds only
the historical inline array, which is not sent. The subject scope is bounded by the manifest it
is drawn from: `subjectCount` is at least 1 and at most the accepted `SnapshotSeal.entryCount`,
which is at most `maxSnapshotEntries` (200,000). The sealed snapshot's own bounds apply before
any of these: 100,000 inventory rows, a 4 MiB descriptor and 8 GiB in total. Every other limit, `limitPolicy` and `semanticBudgetSeparation`
apply unchanged. Lifting the cap lifts no response bound: `maxFactCandidatesTotal`,
`maxCandidateSpoolBytes`, `maxResponsePayloadBytesTotal` and `maxResponseFrames` still fault, and
never manufacture `BudgetExhausted`.

**Work is still charged per subject.** `deterministicBudget` is unchanged. One checked
`work-units` increment precedes each canonical `(stage, subjectOrdinal, Coverage entryOrdinal)`
tuple, over the reconstructed ordinals. A stage budget therefore pays for every subject, its
exhaustion is a clean `BudgetExhausted`, and an overflow is a protocol fault.

**When the token is needed (Plan time).** The host knows the subject count before spawn. The
token is a token the Plan needs (§9.1, step 1) for a `rust-semantic` worker exactly when the
array is longer than `maxSubjectsPerStage`. A signed row without the token is then never spawned,
and the affected keys are `unknown / provider-unavailable` with cause `capability-missing`. Otherwise
the token is optional, and when it is negotiated it is used. Nothing splits, truncates or samples
the array, and no stage is given a subset of it.

**Reading rule.** Some texts name `StageRequestV2` or `StageAnalysisDomainV2` as the source of a
Rust stage's `stageOrdinal`, `planStage` or `requestedCoverageDomain`. Under the token, each such
text reads the same member of `StageRequestV3` or `StageAnalysisDomainV3`. These texts are:
- §9.6's stage correlation;
- the execution-inputs contract's stage-id echo;
- the startup law's pre-Analyze conversion;
- §9.8's `AnalyzeV3.stages`.

**Unchanged.** Protocol major stays 3, and TypeScript major 2. No frame, phase, terminal, limit
member, identity version, commitment recipe or `H` domain is added. `expectedProtocolContractSha256`,
`protocol3-transitions.v1.json` and the Coverage, fact and census laws are unchanged.
`typescript-semantic` is unaffected. Its requested domain already names the file set by reference
(`delivery.v2` `SubjectScopeV1`, `all-snapshot-files`), and its limits (§9.4) have no subject
member.
