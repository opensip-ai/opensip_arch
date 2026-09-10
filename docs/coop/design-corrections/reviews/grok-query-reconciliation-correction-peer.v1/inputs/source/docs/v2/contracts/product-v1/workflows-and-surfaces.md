# Workflows and surfaces — invocations, baselines, comparison, imports, policy, review, repair, outputs

**Standing:** Authored and corrected by actual Claude, Codex and actual Grok under D-367 delegated
design authority for the D-371 intended product. Review and application standing
is governed by the [correction record](../../../coop/design-corrections/README.md)
and central readiness register; mixed-author changes require independent review
and a prospective act naming replacement selectors. Nothing here edits a frozen source, awards a grade,
authorizes implementation or claims platform qualification. Reference evidence is in
[`docs/coop/design-corrections/workflows/`](../../../coop/design-corrections/workflows/README.md):
closed schemas, reference models, hand-authored cases and checkers. Those
are design evidence over synthetic trusted inputs, not product measurement.

**Addresses, subject to independent acceptance:** AR-08 (one operational lifecycle for invocation, attempt, step, Run,
repair and verification), AR-10 (runnable prior detector and portable baseline
custody), AR-11 (typed multi-axis comparison and admitted imported evidence), AR-13
surfaces part (one advertised command/surface inventory and named HTML/agent
parity), AR-16 (provenance-specific remedies, exact outcome goldens, doctor and
delivery behaviour). Owner rows: DR-131/117/133/107 (lifecycle), DR-111/006/130
(baseline), DR-118/122/123 (imports, projections, outcomes), DR-007/112/114.

**Joint interfaces honoured.** Identities are `H(domain, descriptor)` under the
foundation recipe; this unit names domains (§10) and never defines a second
serializer. Unchanged native and input identities retain their major-two recipes: `snapshot2`, `plan2`,
`closure2`, `import2`, `fact2`, `coverage2`, `view2`, `exec-plan2`, `finding-key2`,
with evaluator output `finding3`, `subject3`, `proof3`, `evidence3`, `seal3` and `run3`. Operational identities are the existing `RequestId`
(`req1_`+32 hex) and `ExecutionId` (`exec1_`+32 hex), admitted by the
end-anchored current common schema and identity §2. EXECUTION-ID-V1/C-2 is the
historical grammar provenance; its bare end anchor is explicitly succeeded.
The historical R-1 `execution:<text>` fixture grammar is not admitted. D9 classes, codes and exit numbers are host-owned and unchanged.

The current output dispatch is the incorporated
[evaluator3 workflow projection contract](../../../coop/design-corrections/workflows/workflow-projection-contract.v3.md).
Its closed schemas live under `workflows/schemas/evaluator3/`: envelope,
invocation, command inventory and graph query major3; baseline and comparison
major2; review and repair schema profile2. Embedded policy uses
`policy-document.v2.schema.json` (PolicyDocumentV2). Unchanged scope, waiver,
import, test and operational records keep their explicitly selected owners.
Historical output schemas remain retained evidence and are not an alternative
parser for this profile. An absent unmatched-population field in an old
baseline is never interpreted as an empty population in a new baseline.

Every array in the selected workflow schemas declares
`x-opensip-order` under identity §3. Baseline entries use unique fingerprint
order; pivot closures use unique closure-ID order; source-mapping entries use
unique generated-path order; import blob and repair edit rows use unique path
order. Policy and compiled-program rules retain rule-ID order and waivers retain
waiver-ID order. All other declared sequences preserve order and any repetitions
their schema permits, including argv, predicate operands, attempts, journal
revisions, diagnostics and requested presentation fields. Schema admission checks
the declared order; the shared encoder does not infer sets or reorder inputs.

---

## 0. Superseded selectors (exact) and what replaces them

| Source | Selector | Disposition |
|---|---|---|
| `docs/coop/artifacts/versioning-policy.v8.json` | `$.comparisonSchema.ComparisonResult` (five classifications, `pivotDetectorVersion`) | **Superseded** by the major2 comparison result (§3): nine classifications, explicit pivot chain, audit profiles, typed indeterminacy. |
| `docs/coop/artifacts/versioning-policy.v8.json` | `$.detectorSemanticDelta.theFix.requires` and "B-CSG-04 / CS-04" (dual emission justifies the pivot) | **Corrected**: fact/fingerprint dual emission migrates identity only; the pivot needs the retained or bundled executable closure (§3.3). |
| `docs/coop/architecture/07-outcomes-and-failure.md` | CANDIDATE `CommandEnvelope` major-1 union | **Succeeded** by envelope major 3 (§8): adds `invocation` and `doctor` kinds, mandatory `requestId` and `exitCode`. Major-1 consumers are refused with `REQUEST.SCHEMA_MAJOR_UNSUPPORTED`, never reshaped. |
| `docs/coop/architecture/08-surfaces-and-topology.md`, `docs/MAP-VS-CONTROL.md` | Historical command surface and Map/Control grammar | **Superseded** by the single command inventory (§8) and the advisory boundary (§5). |
| `docs/coop/completion/reference-architecture.v2.md` | Preview analyze/doctor/help command set | Historical D-369 scope; no restriction on §8. |
| `docs/v2/architecture/13-evidence-workflows-and-product-contracts.md` §§5–7, 9 | Workflow, baseline, import and repair prose | **Replaced** by §§1–7 here. |
| `docs/coop/artifacts/c2-plan-stage-schema.v4.json` | `$.planIntent.wireTypes.executionId` | **Provenance retained; admission succeeded** by identity §2 and current `common.schema.json#/$defs/ExecutionId`, with the portable absolute end assertion. The historical bare `$` is not an alternative admission boundary. |
| `docs/coop/artifacts/d9-exit-contract.v1.14.json` | class/code/exit table | **Retained**; §9 adds typed domain detail beside existing codes and maps every detail to one lawful class. |
| `docs/coop/artifacts/d9-exit-contract.v1.14.json` | `$.hostTerminationUnion` field closure and nullability | **Succeeded for product envelope major3** by `common.schema.json#/$defs/StepTermination`: its closed fields include `authority`, `domainDetail` and `faultCause`; no undeclared D9 field is admitted. Optional termination fields remain absent rather than explicitly null. §8's renderer parity record is a separate closed projection: its `run-id` may be null for a non-authoritative result; this is never `termination.runId` and creates no Run authority. Class/code/exit legality remains retained. |

Not touched: root discovery (security/foundation), native cells and import payload
grammars (native §7), identity recipes and retention (identity contract).

---

## 1. Invocation, step, attempt, Run (AR-08)

An invocation is one host request. Its operational identity is `RequestId`, minted
before admission and retained for refusal as well as success. The invocation is an
ordered acyclic list of at most **64 steps**; `StepId` is the zero-based position.
Each admitted attempt of a step receives a fresh `ExecutionId`; a step has at most
**3 attempts**. Only `analysis` and `verify` steps seal or link a content-derived
`run3`. `comparison`, `query`, `render`, `import`, `repair-preview`, `repair-apply`,
`test-execution`, `native-preparation`, `mutation`, `export-delivery` and `doctor` are operational steps
that never mint a Run. Schema: `workflows/schemas/evaluator3/invocation-record.schema.json`.

**Step DAG versus derivation DAG.** The step list is the operational workflow. Each
analysis/verify *attempt* owns exactly one derivation DAG (`exec-plan2`, at most
**1024 stages**) recorded in the attempt's `derivation` binding
(`planId`, `executionPlanId`, `stageCount`, `stagesCompleted`, `firstFailedStage`).
A step never depends on a stage and a stage never references a step. A retry on
identical admitted inputs may bind the same `exec-plan2` and the same Run; attempts
remain separately auditable.

**Dependencies.** `dependsOn` names lower StepIds only (a forward or self reference is
`WORKFLOW.DEPENDENCY_CYCLE`, request-rejected). `requirement` is `required` or
`optional`; a required step may not depend on an optional step
(`WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL`). `dependencyGate` is `completed` (every
dependency completed) or `terminal` (every dependency reached any terminal outcome;
lawful only for `render`/`export-delivery`, which project whatever happened). A
step whose gate is unmet is `skipped` with a typed `skipReason`. Step outcomes are
closed: `completed`, `rejected`, `failed`, `skipped`, `cancelled`, `abandoned`
(crash recovery only).

**Retries.** `retryPolicy=idempotent-retry` is lawful only for `analysis`, `verify`,
`query`, `render`, `doctor` and `export-delivery`, only for `faultCause=ledger-busy`,
and within the 3-attempt budget; exhausting it is `LEDGER.BUSY_TIMEOUT` (4) with
detail `WORKFLOW.RETRY_BUDGET_EXHAUSTED`. `host-io` and every other fault are never
retried. `mutation`, `import`, `repair-preview`, `repair-apply`, `comparison`, `native-preparation` and `test-execution`
carry `retryPolicy=none` by schema; a spec violating this is refused.

**Mutation idempotence and recovery.** Generic `mutation` steps use the bare
64-hex `H("workflow.mutation-intent", MutationReplayScopeV1)`. The closed retained
scope is exactly `{schemaVersion:1,requestId,stepId,projectId,operation}`, with
`operation` equal to `MutationParams.mutationClass`. This explicitly succeeds the
former undefined `{operation,projectId,effect preimage}` description. The key is
operational and scoped to one host-minted request and admitted immutable step;
different fresh requests never deduplicate each other's generic mutations.
`sourceStep` resolves inside that same retained invocation, whose admitted
parameters and completed dependency results are immutable. Before lookup or
replay the host validates the scope and full params, recomputes the key and
requires the retained invocation/project/step/operation binding; a caller cannot
nominate another invocation's scope or change effect inputs under an old key.
Receipt lookup is never an effect-authorization mechanism. A same-scope COMPLETED
receipt permits delivery replay with no second effect. Failure, unknown state or
incomplete execution requires the operation's existing recovery law, not blind
re-execution. Recovery started in a new request retains its own operational scope
and the explicit original journal/intent links required by §§6/12.

**What a step's required receipt carries is published, not inferred.**
`MutationReceiptV1` **requires** both `operation` and `idempotencyKey`, and
`ImportResult` and `NativePreparationResult` both **require** a `receiptId`. The
owning domain for those branches is `workflow.mutation-receipt` — the **mutation**
receipt domain, not the only `receipt2:` one, since §10 also lists
`workflow.verification-link`. So an import step and a native-preparation step each
already owe a receipt carrying **both** required fields, and what was missing was
the binding for each. The operation binding is published as
`repair.schema.json#/x-opensip-mutation-operation-map/byStepKindReceiptOperation`,
beside the enum, and it is a deterministic function of the **step kind**:

| Step kind | Receipt operation | Also carried in a request field? |
|---|---|---|
| `mutation` | the command's row in `byCommandGenericMutationStep` | yes — `MutationParams.mutationClass`, equal to `MutationReplayScopeV1.operation` |
| `repair-apply` | `repair-apply` | no — dedicated step, refused in both generic fields |
| `import` | `import` | no — `ImportParams`; §4's import receipt |
| `native-preparation` | `native-preparation` | no — `NativePreparationParams`; native §14's execution receipt |

Because the binding is by **step kind and not by request class**, the `import`
step of the `analyze` command carries the same operation as the `import`
command's. That is also a worked case of **one operation emitted by two
commands**, which is why this map is *not* an inverse map and must not be read
backwards. A command with none of these four step kinds mints no operation.

**The idempotency key is bound too, and sharing a recipe is not sharing replay
authority.** `receiptIdempotencyKeyByStepKind` publishes, per step kind, the exact
deterministic preimage and the *lookup meaning* separately:

| Step kind | Key | Lookup meaning |
|---|---|---|
| `mutation` | `H("workflow.mutation-intent", MutationReplayScopeV1)` | equal COMPLETED receipt permits delivery replay with no second effect |
| `repair-apply` | raw SHA-256 of `C({operation, projectId, repairPlanId, baseSnapshotId})` | equal completed key performs no second effect |
| `import` | the same H over the closed scope with `operation: "import"` | **delivery only**, within the same retained invocation; never a cross-request dedupe |
| `native-preparation` | the same H with `operation: "native-preparation"` | **not replay**: it identifies that step's receipt and authorizes nothing |

No new H domain, record or authority is introduced: `MutationReplayScopeV1.operation`
**already admits** both tokens — they are two of the 23 — which is a further reason
that domain stays wider than the current generic emitters. The user-supplied import
path is deliberately **not** in the preimage, because §4 keeps it out of identity
entirely. The receipt key is operational and already contains `RequestId`.
`ExecutionId` stays out because this key is scoped to one admitted invocation and
step; each attempt keeps its separate `ExecutionId`. These immutable bindings
grant no execution or retry authority.

**The three non-generic kinds are still not generic replay.** They carry their own
params rather than `MutationParams`, are not generic `mutation` steps, and carry
`retryPolicy=none` by schema. Import custody, mandatory source correspondence and
the staleness disposition are unchanged and re-checked — a receipt substitutes for
none of them. A fresh native preparation is a **new explicit authorized execution**
under its own `AuthorizedExecutionV2` and grant set with **no automatic retry**; a
completed receipt never suppresses one, and this binding grants no permission the
security unit does not already admit.

Across these step kinds, **four** commands do not share their operation's name,
so the operation cannot be derived by name matching. Three use generic mutation steps:
`baseline-upgrade` → `baseline-upgrade-apply` (the operation names the apply
half; the analysis half mints a Run, not a mutation), `policy-init` →
`policy-write` and `waive` → `waiver-change` (both are effect classes covering
more than the one command spelling). The fourth is the execution-class
`native-prepare` → `native-preparation`, whose operation is carried by its own
step kind; it is published with the other three because counting only the
mutation-class commands would leave one command's operation still underivable.
The published set is held **equal** to the commands whose name is not itself a
`MutationOperation` member, so a later rename cannot be added to the vocabulary
without appearing here. Two further facts are disclosed rather than tidied away:
`repair-apply` is bound by its own step kind, and being in the map does **not**
make it admissible in either generic position — both still refuse it by schema;
and `config-write` is the one `MutationOperation` member that **no step kind binds
and no command in this inventory emits**, which is stated rather than removed or
given an invented command, and which stays admissible in the generic field because
narrowing a generic domain to today's emitters would remove a value no finding
asked to remove. Publishing the map adds no command, no operation, no receipt and
no accepted request. What the reference model in this kit does **not** do is emit
an import or native-preparation receipt; that is a stated qualification limit of
the reference evidence and is deliberately distinct from the design law above.

Repair apply is the explicit content-derived exception: it is a dedicated
`repair-apply` step, excluded from generic MutationParams. It uses the raw SHA-256 of
canonical `{operation:"repair-apply",projectId,repairPlanId,baseSnapshotId}` as its
idempotency key. An equal completed key performs no second effect. The original
receipt is immutable; a replay delivery produces a separately identified receipt
with the new request/attempt binding and `replayed=true`. Mutation receipts use
`receipt2:` plus `H('workflow.mutation-receipt', receiptWithoutReceiptId)` and remain
retained when an effect or later verification fails. Read-only recovery inspection
is distinct from separately authorized recovery writes (§6).

**Audit gate ownership.** An analysis step declares `verdictGate=self|delegated`.
`self` applies its Run verdict. `delegated` requires authoritative analysis and a
consuming comparison step: a completed failing Run then contributes operational
success with its RunId, while the comparison owns the regression gate. This lets
inherited findings remain visible without failing the PR. Missing required Coverage
still contributes indeterminate; delegation cannot hide an incomplete analysis.
The comparison result is a distinct closed `ComparisonStepResult`, never a Run.

**Cancellation.** A signal is recorded with the phase at which it arrived.
*before-settle* (some required step not yet terminal): remaining steps are
`cancelled`, the aggregate is `interrupted` (130), and a Run committed by an earlier
step is named in the termination's `runId`. *after-settle* (every required step
already terminal): the aggregate is **not reclassified**; the settled class stands.
Per kind: an analysis attempt aborts and leaves no Run; an import discards its
staged bytes; a repair-apply honours cancellation only before `APPLYING`, and during
the bounded rename loop the journal, not the signal, decides (§6).

**Aggregate termination (D9 ordering preserved).** Over required steps only:
`operational-failed` > `request-rejected` > `policy-failed` > `indeterminate` >
`success`. An optional step's rejection or failure never changes the aggregate.
Policy fail dominates indeterminate across steps exactly as inside one Run, and a
required operational fault dominates a committed failing Run (its `runId` is still
carried). Exit code derives from class by the fixed table only. Ties retain the first
termination carrying domain detail in step order, or the first termination when
none carries detail, so a useful comparison remedy is preserved.

**Ephemeral analysis.** `--ephemeral` produces the second member of the closed
`AnalysisResult` union: `authority=ephemeral`, `durability=not-required`, no `runId`,
no receipt, only semantic `planId`/`evidenceId` so the result can be cited. It cannot
satisfy baseline adoption, repair preview/apply, verify or authoritative replay
(`WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY`, `REQUEST.UNSATISFIABLE`, exit 2). A
failing ephemeral verdict terminates `policy-failed` with `authority=ephemeral`
instead of a `runId`; the branch contract admits exactly one of the two.

**Default invocation.** `opensip` with no arguments is discovery then one durable
authoritative analysis (steps `analysis`, `render`). Retention is DEFAULTED
durable-unbounded (CD-RT-5), disclosed with the storage root before first write.
No policy file is written implicitly.

---

## 2. Portable baseline and runnable prior detector (AR-10)

The major2 baseline artifact lives in the repository as tracked intent
(`opensip.baseline.json`). `baselineId = H('workflow.baseline', descriptor)`. The
descriptor pins: origin ProjectId, source `snapshot2`, the **authoritative** `run3`
and `plan2` (an ephemeral result is refused: `BASELINE.SOURCE_EPHEMERAL`), the
fingerprint recipe (`finding-fingerprint`, major ≥ 2), every contributing detector's
`closure2` with semantics major, the complete **pivot closure** (detector executable,
evaluator, provider, toolchain/stdlib, schema set; each a `closure2` with manifest digest,
protocol major and platform), the evaluation context digests, the **embedded**
policy/scope/waiver documents whose digests equal those context digests, rule
coverage, sorted unique matched entries and explicit unmatched occurrences.
Matched occurrences group only after equal fingerprint preimages and agreement
on every BaselineEntry field. Messages, parameters and citations remain on each
original finding. Unmatched findings retain their finding and subject identities;
they cannot be silently discarded or assigned a guessed stable fingerprint.
Custody (outside identity) carries host release,
export time, `retentionPins` (the Run and every pivot closure) and an optional signed
`closureBundle` reference.

**Fresh CI.** Comparison never reads the origin machine's store. A fresh host admits
the artifact by recomputing `baselineId`, checking schema major, recipe major,
sortedness, context-document digests and project correspondence (same ProjectId, or
explicit `--accept-origin`, else `BASELINE.PROJECT_UNMAPPED` and no comparison). It
resolves each pivot closure from (a) a retained generation, (b) an installed signed
release with the same `closure2`, or (c) the signed closure bundle; all under
**current trust**. A closure that is missing (`pivot-detector-unavailable`), revoked
(`pivot-closure-revoked`) or incompatible with the host's protocol majors/platform
(`pivot-closure-incompatible`) makes E0 unavailable; a revoked closure is never
executed, whatever bytes are present.

**Detector semantics.** Semantics can change within a major, so two-way comparison
is lawful only when the closures are identical (`identical-closure`) or the current
detector's authenticated compatibility listing names the baseline `closure2` as
exactly semantically compatible at the same major (`declared-compatible`).
Security S1 binds this optional listing to the unique regular-file path
`.opensip/detector-compatibility.json` in the already admitted same `closure2`
tree. The listing uses `schemas/evaluator3/detector-manifest.schema.json`;
its exact retained byte length and SHA256 must match the signed tree file.
`closure.manifestDigest` continues to identify the component manifest body.
An absent reserved path means no declaration; a valid empty listing declares
no compatible peers; a present invalid, non-file or unavailable listing refuses
and cannot silently become absence. The host admission origin is one of the
three current-trust paths above. Caller-provided compatibility or trust claims
do not supply that admission. Otherwise the baseline detector
must run over current source (`three-way-pivot`, an authoritative pivot analysis step
planned before the primary one) or the detector's entries are `INDETERMINATE`.
Fingerprint dual emission (`legacyFingerprint`) migrates identity only and never
supplies the prior algorithm. Adoption pins the Run and the pivot closures as
retention roots; loss of a pin is disclosed as partial availability and yields typed
indeterminacy, never a silent two-way fallback. `baseline-upgrade` re-adopts under the
current detector explicitly and is a mutation with its own receipt.

---

## 3. Multi-axis comparison (AR-11)

The major2 comparison result (`comparison2:` = `H('workflow.comparison', descriptor)`)
attributes every fingerprint to the **first** axis at which it changes along a fixed
counterfactual chain evaluated over *current* source:

| Pivot | Facts from | Policy | Scope | Waivers |
|---|---|---|---|---|
| B | baseline artifact entries | prior | prior | prior |
| E0 | prior detector closure over current source | prior | prior | prior |
| E1 | current detector | prior | prior | prior |
| E2 | current detector | current | prior | prior |
| E3 | current detector | current | current | prior |
| E4 | current Run | current | current | current |

Axis order is code (B→E0), detection (E0→E1), policy (E1→E2), scope (E2→E3),
waiver (E3→E4, by waived status). E1–E3 are pure re-evaluations of retained current
facts under the baseline's embedded documents. They are available only when their
results were actually bound; an unchanged axis is `not-needed`, and a required
unbound re-evaluation is `unavailable` with typed indeterminacy. E0 is
`not-needed` when the detector is unchanged or declared compatible, `available`
when the pivot ran, `unavailable` otherwise. Classifications are `UNCHANGED`,
`CODE-NET-NEW`, `CODE-FIXED`, `DETECTION-DELTA`, `POLICY-DELTA`, `SCOPE-DELTA`,
`WAIVER-DELTA`, `EVIDENCE-DELTA`, `INDETERMINATE`; each entry also records
`presence` at every pivot and `subsequentDeltas` (later axes at which it changed
again). Deleting a waiver while adding a bug therefore yields one `WAIVER-DELTA` and
one `CODE-NET-NEW`; a bug introduced and simultaneously hidden by disabling the rule
is `CODE-NET-NEW` with `subsequentDeltas=[policy]`.

**Evidence for presence.** The fingerprint population is the union of B and
all admitted E0–E4 results, including fingerprints present only in a pivot.
A known matched finding establishes presence even when waived; waiver status
is a separate axis. Absence of a particular fingerprint requires complete
subject enumeration, determinate `emitWhen` proof roots for every selected
subject, and that fingerprint absent from the exact admitted emission set.
A known finding on another subject does not invalidate this negative knowledge.
All-false roots establish the stronger claim that the rule emitted no findings.
Required execution deficiencies still affect the overall Run and comparison
verdict; they do not retract a determinate per-rule fingerprint result.
An advisory `pass` alone does not establish absence. A false root may retain
unknown child witnesses under the published three-valued composition law;
those witnesses do not turn a determinate false root into unknown. Unknown
roots, incomplete enumeration, disabled evaluation and exhausted budgets do
not establish a negative result. Known hits remain usable in a partial result.

E1–E3 preserve current non-substituted inputs: selected source, configuration,
provider/toolchain contexts, imports, native facts and Coverage, subject
inventories, attribution/search records and candidate-producer evidence.
Plan-bound envelopes are compared by their retained semantic contents after
removing only the explicitly substituted parent locators. A policy, scope or
waiver remint cannot authorize replacement of native evidence. E0 uses the
prior detector and its admitted dependencies over current source and can
therefore have different native contexts and evidence. Snapshot membership
alone is not proof that native extraction examined a path; a counterfactual
requiring evidence outside the attested extraction extent is unavailable.

**Detector union.** Comparison covers the union of baseline and current detectors.
Added detectors set E0 false. Removed detectors require the actual current-trusted
prior detector pivot and set E1–E4 false; E0 must never be substituted with B.
Consequently a new bug hidden by removing its detector remains CODE-NET-NEW and
can gate. Missing prior execution is indeterminate, including detector removal.

**Evidence axis.** Compare the exact bound `import2` identity sets per kind, with
payload/correspondence/scope/observation digests retained in each BoundImport.
Replacing an artifact with another of the same kind is still an evidence change
(`evidence-content-changed`). For a rule with declared `evidenceUse`: if required evidence is
absent on the current side the entry is `INDETERMINATE`
(`required-evidence-unavailable`) and the rule's coverage is unsatisfied; if
availability changed and the rule gates on either side, attribution is
`INDETERMINATE` (`evidence-availability-changed`); only for a non-gating rule may a
presence change be `EVIDENCE-DELTA`. Required evidence loss can never disappear as a
non-gating delta.

**Audit profiles select gate semantics explicitly** (schema `AuditProfile`):

| Profile | Gates CODE-NET-NEW | Gates newly live via policy/scope/waiver | Gates all current live | New waiver suppresses net-new | Rule gating under |
|---|---|---|---|---|---|
| `code-regression` (default for `audit`) | yes | no | no | no | baseline or current |
| `policy-change` | yes | yes | no | no | baseline or current |
| `full-current` | yes | yes | yes | yes | current only |
| `report-only` | no | no | no | yes | current only |

A `CODE-NET-NEW` entry that is not live in current (hidden by a later policy/scope
change or by a waiver added in the same change) still gates under
`baseline-or-current` with `gateReason=code-net-new-policy-hidden`. Verdict is `fail`
if any entry gates, else `indeterminate` if any `INDETERMINATE` entry belongs to a
gating rule or a current gating rule has unsatisfied/unknown required Coverage or
evidence, else `pass`. Rule deficiencies are enumerated independently of findings;
zero emitted findings never establish complete analysis. Whole-comparison indeterminacy (unmapped project,
unsupported schema/recipe major, context document mismatch) performs no comparison
and emits zero entries with a typed remedy. Enum precedence never decides a gate.

---

## 4. Imported evidence: one wrapper, typed payloads (AR-11)

There is exactly one import identity: `importId = 'import2:' + H('import', wrapper)`
where the wrapper is the foundation `import` descriptor (schemaVersion 2, kinds
`runtime|test|history|dependency|prepared`). Each kind admits exactly one canonical
payload domain. Native runtime/test/history formats are adapter inputs normalized
into the workflow-owned payload before wrapping.

| Kind | Admitted payload domain | Owner |
|---|---|---|
| runtime | `workflow.import-payload.runtime.v1` | workflow |
| test | `workflow.import-payload.test.v1` | workflow |
| history | `workflow.import-payload.history.v1` | workflow |
| dependency | `native.import-payload.dependency-source.v1` | native |
| prepared | `native.import-payload.prepared-output.v1` | native |

The closed registry names the exact schema document and JSON selector. Its
`payloadSchemaDigest` is raw SHA-256 of the entire schema document's bytes;
`payloadDigest` is raw SHA-256 of the canonical validated payload. The host validates
the selected payload, source correspondence, foundation scope descriptor,
BuildIdentityV1, ImportObservationV1 and wrapper using the trusted local schema
closure. Merely carrying a recognized payloadDomain is insufficient. Caller-supplied
schema bytes must equal the registry document exactly. No network schema resolution
is allowed. All auxiliary digests are raw SHA-256 of their canonical closed records;
those preimages are retained. The `import2` wrapper alone uses the H-domain recipe.
The same payload with different provenance or observation semantics is a different import.

Any other pairing is `IMPORT.KIND_PAYLOAD_MISMATCH`; an unregistered payload schema is
`IMPORT.PAYLOAD_SCHEMA_UNREGISTERED`; no artifact-supplied schema is ever admitted.
`opensip import KIND PATH` is a mutation step with an import receipt; the user-named
PATH is a `UserInputPath` opened through the security unit's nofollow custody and
never enters identity; every path inside a payload is a strict `LogicalPath`.

Source correspondence is mandatory (`IMPORT.MAPPING_REQUIRED`, `CONFIG.INVALID`):
the shared closed SourceCorrespondence union in common.schema.json,
`exact-snapshot` or `vcs-revision` with VCS/build/mapping fields. Staleness
against a Plan is a closed table (`StalenessRule`): snapshot-equal → `current`,
consumable; snapshot-differs / commit-differs → `stale`, unmapped-only;
commit-equal-dirty → `unverifiable`, unmapped-only; build-identity-differs →
`wrong-build`, unmapped-only. An equal clean commit is consumable only with an
admitted SourceMappingV1 whose source paths and hashes join the current snapshot
inventory; an equal commit without that mapping remains unmapped-only. Corrupt bytes → refused (`IMPORT.ARTIFACT_CORRUPT`).
Explicitly selecting a stale import for a Plan is `REQUEST.PRECONDITION_FAILED`
with `IMPORT.STALE_FOR_PLAN` (2). Unmapped-only evidence may be listed and queried
but never feeds a predicate.

**No-hits is not non-use.** Runtime subjects carry `observed-hit`,
`observable-unhit`, `unobservable` or `unmapped`. `observed-hit` supplies positive
execution evidence and `observable-unhit` supplies bounded negative evidence,
always together with the observation window and population; `unobservable`/`unmapped` never become unhit signals and the schema
refuses a hit count on them. One window never establishes universal non-use;
runtime coverage is never OpenSIP Coverage. History payloads are advisory priority
inputs unless a policy predicate explicitly declares `evidenceUse` for them.

**A repair evidence requirement over one of these two relations has its own
owning outcome law**, `imported-evidence.schema.json#/x-opensip-imported-requirement-law`
(§6). It is separate from native §4.6 because these relations mint no `fact2` and
carry no Coverage, and **each kind is projected through its own payload**: a
runtime requirement reads `observability`, `observationWindow` and
`observedPopulation`; a history requirement reads `revisionRange` and
`collectionScope`, which are its bounds fields; `HistoryPayloadV1` also carries
subjects and has no runtime observation-window, population or observability
fields. Neither kind may report the other's outcomes.

**A repair target is a fingerprint, not a path, and the join is published.**
`RepairPlanDescriptor.targets` are `finding-key2:` **fingerprints**, while
`RuntimeSubject` is keyed by `{path, symbol?}` and `HistorySubject` by `{path}`.
The deterministic projection is
`imported-evidence.schema.json#/x-opensip-imported-requirement-law/targetSubjectProjection`:
each target must be a finding of the evidence Run named by `evidenceRunId` (preview
already refuses one that is not); that `finding-key2` identity is the H identity of
the retained foundation `finding-fingerprint` descriptor, whose retention is
`preimage` and whose bytes are therefore re-hashed at Run closure; and its
`subjectKey` supplies the path and qualified name used for matching. The projection
does not classify the target by `kind`, whose vocabulary is not closed here. A
runtime row matches on path and, if it names a symbol, on qualified name; another
symbol's row does not match. A runtime row with no symbol and every history row
provide **file** granularity, with `granularityWidenedToFile` disclosed in the
projection and successful outcome. A symbol-naming runtime row provides the
format's path-and-name granularity, not an exact match of the whole subject key:
neither format distinguishes `language`, `kind` or `discriminator`. Distinct
findings can therefore project to the same observation. This stated limit applies
to every such projection; it cannot establish execution or non-execution of a
particular subject variant beyond the captured granularity. More than one
matching subject **refuses**: an ambiguous projection is not resolved by choosing
one. A target with no matching subject is unsupported — never satisfied, and never
read as evidence of non-use.

Five limits carry over and are enforced rather than assumed.
**Satisfied does not mean positive**: `observed-hit` is positive execution
evidence and `observable-unhit` is *bounded negative* evidence, both can satisfy,
and the disclosure records which did. **No imported observation establishes a
universal negative** — one window is not universal non-use — and imported evidence
can never *by itself* establish the native closed world or authorize an unsafe
`delete`/`replace`: that gate stays the evidence Run's own `ClosedWorldV2` (§6).
It may still be an **additional required condition** alongside an
already-established native basis, so it is wrong to say it never affects
applicability; an unsatisfied imported requirement makes an otherwise-eligible
plan inapplicable. **Whole-versus-partial** is decided by the requirement's
`completeness` field: `complete` needs every plan target supported,
`partial-acceptable` at least one. That enum already existed, but **this reading of
it for an imported requirement over plan targets is selected here** and was not
previously published. A target that is unobservable or outside the history
collection scope therefore only names the cause *more precisely when the support
test fails* — it does not veto a lawful `partial-acceptable` requirement that has a
supported target. **Bounds are separate from support**: an insufficient observation
window or revision range applies under both completeness values, because it is a
property of the observation rather than of the target count. And **required versus
optional** stays where `evidenceUse` puts it — an optional absence remains the
`IMPORT.ABSENT_FOR_PREDICATE` disclosure and is satisfied *by absence* rather than
by evidence. That declaration reaches the requirement boundary as a **typed
boolean**; a non-boolean refuses, so there is no `unknown` state to default and no
falsy value is read as optional.

---

## 5. Declarative policy DSL, authoring test, candidate → inspect → review

**DSL.** `PolicyDocumentV2` is closed data: rules with a `ruleProgramRef`
(contribution, stable id, semantics major, program digest), `enabled`, `severity`
(`note|warning|error`), `gate`, a `subjectEnumeration` (universe, subject kind,
include/exclude globs over `LogicalPath` with only `*`, `?` and whole-segment `**`),
an `emitWhen` predicate tree and `evidenceUse` declarations. Predicates are exactly
the evaluator's set: atoms `exists|none|count-at-most|all-covered` over a relation,
minimum resolution and typed field filters (`eq|neq|in|prefix|glob|gte|lte`), plus
`and|or|not`, depth ≤ 8, ≤ 64 nodes per rule, ≤ 512 rules. Evaluation is strong
Kleene: under incomplete Coverage `exists` is true on a match else indeterminate,
`none` false on a match else indeterminate, `count-at-most` false above N else
indeterminate, `all-covered` indeterminate. A true predicate emits a finding; false
is a retained no-match; an indeterminate gating rule is a typed deficiency. An atom
over imported evidence must be declared in `evidenceUse`; required evidence absent
makes the rule indeterminate, optional evidence absent is disclosed as
`IMPORT.ABSENT_FOR_PREDICATE` and is not a gating deficiency. There is no string
expression, hook, script, include or exec key; any such key is a schema violation
(`POLICY.IMPERATIVE_KEY_REFUSED`). Policy, ScopeDocumentV1 and resolved WaiverSetV1
digests are raw SHA-256 of their canonical closed documents, retained as blobs.
The compiled RuleProgramV2 separately hashes its policy digest and ordered rule
programs to proof.ruleProgramDigest; these are auxiliary hashes, not H identities.
The exact endpoint, native field projection and imported test-filter grammars
are in that policy schema and the incorporated atom contract. Identity §4 and
the composition contract own independent subject enumeration, complete tree
replay, full finding emission, waiver membership and budget semantics. Declared
required evidence remains distinct from retained nonblocking branch diagnostics.

**Waivers.** A waiver targets a fingerprint or `(ruleId, subjectPath)` with a reason
and `expires` (date or null). Expiry and duplicates are resolved at **Plan
construction** against the admitted trust clock: expired waivers leave the effective
set and are disclosed (`POLICY.WAIVER_EXPIRED`), two waivers on one target refuse
(`POLICY.DUPLICATE_WAIVER`, `CONFIG.INVALID`), and the Plan's `waiverDigest` is that of
the *resolved* effective set, keeping evaluation pure. `opensip waive` is the explicit
tracked-intent write; nothing writes a waiver implicitly.

**Authoring test.** `opensip policy test SUITE` is Query class. A suite supplies the
candidate policy, waivers, an `asOfDate`, optional test-only overrides and cases with
typed fact fixtures (subjects, facts, declared Coverage, available evidence kinds) or
a bounded source fixture. Facts cases are evaluated by the deterministic fixture
verifier (the finite declarative fixture evaluator; this is reference evidence, not
qualification of the production evaluator or native providers); sources cases run only under an ephemeral non-authoritative Plan with
bundled providers and otherwise report `not-executable`. Expectations are
`finding{ruleId,minCount,maxCount,subjects}`, `no-finding`, `verdict`, `indeterminate`.
The result (`policytest2:`) records candidate and effective digests, resolver
acceptance and refusals, applied overrides, waiver resolution and
`enforcementUnchanged=true`; the same suite always yields the same result identity.

**Candidate → inspect → review (Map side).** `opensip candidates` lists
`Candidate` records derived from one sealed Run: findings plus advisory kinds
(`clone-candidate`, `low-confidence-unused`, `runtime-unhit`, `history-stale`) with an
evidence level. Only a finding on a gating rule is `controlBearing`. `opensip inspect`
returns a bounded `InspectionBundle` (≤ 4096 facts, Coverage, imports, limitations).
`opensip review join` records a `ReviewDisposition` (`accept|reject|defer`, reviewer
principal human/model/policy-rule, note, `suppressUntil` ≤ 365 days) as a mutation
with a receipt. The disposition schema admits no verdict, Run, baseline or
authorization field: review can never mint a Control verdict or authorize a repair.
`reject`/`defer` suppress the candidate from listings until `suppressUntil` or until
its fingerprint changes; expired suppressions resurface with `previouslyReviewed`.
`opensip review brief` is an advisory, bounded (≤ 1000) ordering labelled with its
producer (a model producer names its `closure2`); truncation is explicit.

---

## 6. Repair preview, apply, verify (AR-08)

Three separately authorized steps; schemas in `repair.schema.json`.

**Preview** (`repair-preview`, Query class) requires an **authoritative** evidence Run
(`REPAIR.EVIDENCE_RUN_NOT_AUTHORITATIVE` for ephemeral) whose availability is retained
and whose sealed assurance is replayable (else the plan is not applicable with
`REPAIR.EVIDENCE_RUN_UNAVAILABLE`), a recipe closure admitted under current trust
(`REPAIR.RECIPE_TRUST_REVOKED`; an absent admission is also refused), targets present in that Run, and a live tree equal to
the Run's snapshot (`REPAIR.SOURCE_MOVED`). It emits `RepairPlanV1`
(`repairplan2:` = `H('workflow.repair-plan', descriptor)`) bound to `snapshot2`,
`run3`, `plan2`, exact per-file edits (`replace|delete|create`, preimage digest from
the snapshot inventory, postimage digest and bytes; ≤ 4096 files, ≤ 16 MiB each,
≤ 64 MiB total), evidence requirements, the recipe's permitted edit scope (an edit
outside it is `REPAIR.EDIT_OUTSIDE_PERMITTED_SCOPE`), `applicable`, unmet
preconditions and limitations. Destructive unused-code recipes additionally require
native closed-world resolution evidence; an advisory similarity or runtime-cold
signal alone never authorizes deletion. Preview never writes.

**The closed-world gate reads the evidence Run; the descriptor carries a
projection.** The guard covers **every `delete` and every `replace` edit** in the
plan — the unsafe-action set is those two actions, without qualification, and this
paragraph narrows it in no way. If the plan contains one, the prerequisite is
decided against the evidence Run's own native `ClosedWorldV2` (native §4.5) —
the record that contract closes at seven members — **before** any descriptor is
built: `deadCodeRepairEligible=false` reports
`REPAIR.CLOSED_WORLD_NOT_ESTABLISHED` with that record's own `reasons` in the
remedy, and an `imported-prepared-declared` evidence origin reports the same code,
because a DECLARED prepared expansion is not authority for an unsafe repair.

`dynamicDispatch` is **not** a global veto and must not be read as one. Native
§4.5 makes dynamic-edge effects **target-relative**: `affected_targets` marks the
subjects a dynamic edge could reach, and §4.6 turns that into
`resolution-incomplete` for a universal negative **about an affected subject**.
So a present dynamic edge disqualifies the claims that depend on the subjects it
reaches; it does not by itself disqualify an unrelated target in the same Run.
The roles here are distinct and are not merged: preview **admits** each evidence
requirement's `relation`/`minResolution` against the registered vocabulary and its
relation's own ladder (`admit_atom`, which is vocabulary admission, not an
evidence judgement), and then **consumes** that requirement's own `satisfied`
value; the semantic sufficiency behind it is owned by native §4.6
`sufficiency_v2` and the §4.5 affected-target evidence, per requirement, and is
never collapsed into one flag.

**Which vocabulary `EvidenceRequirement.deficiency` carries, and when it is
required.** Preview admits a requirement over **either evidence plane**, so the
field carries the vocabulary of **that requirement's** plane and the plane is
decided at admission from the relation's registry membership — the same place the
two planes are already separated — never from the value.

* **Native plane** — the thirteen native fact relations. The value is native
  §4.6's `DeficiencyV2`, named here through the drift-checked mirror
  `common.schema.json#/$defs/NativeSufficiencyDeficiency` because this bundle
  resolves only its own URNs.
* **Imported plane** — `runtime-observation` and `history-change`. Those relations
  mint no `fact2` and have no Coverage entry, so `sufficiency_v2` has nothing to
  range over and is not asked. Their outcomes are owned by
  `imported-evidence.schema.json#/x-opensip-imported-requirement-law` and mirrored
  as `common.schema.json#/$defs/ImportedRequirementDeficiency`; every member names
  an already-published import condition and is bound to the payload field that
  grounds it, and each kind reports only the outcomes **its own** payload can
  ground — enforced at **both** the producer and this admission (§4). The
  requirement record gains no field: plan `targets` supply the per-target scope
  through the published fingerprint projection, `completeness` decides
  whole-versus-partial under the reading selected in §4, and `evidenceUse` supplies
  required-versus-optional as a typed boolean. The bounded observation demand is
  owned by the **admitted recipe closure** named by `recipe.closureId` — `RecipeRef`
  carries no such wire field and none is claimed.

The two vocabularies are **disjoint**, and a cross-plane value — a native
requirement claiming `import-unmapped-only`, or an imported one claiming
`resolution-incomplete` — is refused at admission, as is an outcome of the wrong
imported **kind**, such as a history range cause on a runtime relation. This schema
**deliberately leaves the authoritative registry lookup to admission**: it admits
either vocabulary and does not attempt to reproduce the relation registries, which
it could not fetch rows from in any case. That is a design choice about where the
authority lives, not a limitation of JSON Schema — a schema *can* branch on a
property's `const`/`enum` even where the base type is a broader string — and
duplicating a registry as schema conditionals would create exactly the drift this
contract set avoids elsewhere. The division is stated rather than implied.

The value carried is the **satisfaction/deficiency projection** of its producer's
result, not that result: `sufficiency_v2` also returns `causes` on both branches
and may return `disclosures` on a failing branch. Those are producer result arrays
and are fields of no retained record; what is retained is the evidence the
evaluation read, so the projection drops nothing that was retained. Presence is **typed**: `deficiency` is **required
exactly when `satisfied` is false** and **forbidden when it is true**, `satisfied`
must be an actual boolean, and an explicit `null` is refused in both branches
because a present key with a null value is not an absent key. Both boundaries — the
schema and the preview admission — decide that same law and are held equal on an
enumerated shape table. The field previously named
`D9Deficiency`, which cannot express four of the nine outcomes its only producer
emits — `derivation-policy-unmet`, `external-consumers-unknown`,
`input-closure-incomplete` and `resolution-incomplete` — leaving three conforming
readings and no document choosing between them: write the D9-mapped value, which
is `verdict-indeterminate` for **all four** and so cannot tell
`resolution-incomplete` (the outcome §4.6 step 6 mandates for a universal
negative under `unresolvedEdgePolicy=forbid` over an affected target, and the one
a destructive unused-code recipe turns on) from three unrelated causes; write the
sufficiency value and be schema-invalid; or omit the field and drop the
disclosure. Retyping this one per-requirement field is the correction.
`D9Deficiency` is **unchanged** and still carries every whole-Run and
comparison-step termination — three of its members name evaluation, baseline and
query outcomes no per-requirement evaluation can produce — and the public D9
route for a Run carrying such a requirement is still native §10's. The value is a
**disclosure, not an authorization**: `applicable` is false whenever any
requirement is unsatisfied, the exact cause is carried into that requirement's
unmet precondition so two different causes are two different remedies, the
evidence authority remains the sealed Run named by `evidenceRunId`, and any edit
to the value mints a different `repairPlanId` that no authorization names.
That unmet precondition is emitted once per unsatisfied requirement and carries
the existing `REPAIR.EVIDENCE_RUN_UNAVAILABLE` code, which here says that the
evidence Run cannot supply what this repair requires and asserts nothing about the
Run having been purged or lost — `evidence.purged` and `evidence.missing` keep
their own distinct meaning in query results. Preview therefore reaches that one
code by two routes, the retained-availability and replayable-assurance failure of
the first paragraph above and this per-requirement insufficiency, and the remedy
is what tells them apart: the retention entry's remedy names the Run-level
restoration that route needs, while the per-requirement entry's remedy names that
requirement's `relation`, `minResolution`, evidence plane and exact `deficiency`.
`EvidenceRequirement.deficiency` remains the typed cause carrier: no
per-deficiency detail code is minted, because the closed public registry is not
where a per-requirement outcome vocabulary belongs. An unsatisfied requirement
with an empty `unmetPreconditions` is **not** a conforming projection — the schema
alone admits that shape, and the emission is decided at admission, the same
division of labour already stated for the deficiency vocabulary.

`RepairPlanDescriptor.closedWorld` is then the **five-field projection** of the
evidence record — `deadCodeRepairEligible`, `exportsClosed`,
`entryPointsRecognized`, `nonliteralLoading`, `externalConsumers`, with
`dynamicDispatch` and `reasons` dropped — and `repair.schema.json` closes it at
exactly those five, so a literal copy of `ClosedWorldV2` is refused there. **The
projection grants no evidence authority of its own.** It is a descriptor: no edit
to it can make a plan applicable, since the whole descriptor is the preimage of
`repairPlanId` (`H('workflow.repair-plan', descriptor)`) and apply requires a
security authorization bound to that exact `repairPlanId`, base snapshot and
project. The authority stays the sealed Run named by `evidenceRunId`: the
prerequisite above is decided against **that** Run's own full record, including
the two members the descriptor does not carry. No claim is made here that a later
step re-reads it — `repair verify` seals a **new** Run over the freshly
re-snapshotted tree (`appliedSnapshotId` → `verifiedSnapshotId`) and compares
remaining and net-new findings; it does not re-open the original evidence Run.

**Apply** (`repair-apply`, mutation) is bound to the exact `repairPlanId`, base
snapshot and project by a security-unit authorization (`REPAIR.CONSENT_NOT_BOUND`);
CI requires policy consent. Current recipe trust and live authorization are checked
again immediately before apply. It journals `RepairApplyJournalV1` through
`PREPARING → STAGED → APPLYING → APPLIED → COMMITTED`: every postimage is written to a
same-directory temp and digest-verified, every preimage is re-verified against the
live file (`REPAIR.TARGET_PREIMAGE_MISMATCH` leaves `FAILED_CLEAN`), renames proceed in
ascending path order, then the tree is re-snapshotted (`appliedSnapshotId`) and the
receipt written. A fault during `APPLYING` restores every renamed target
(`FAILED_ROLLED_BACK`, rollback `completed`); a renamed target that is neither
preimage nor postimage is `RECOVERY_BLOCKED` with the paths listed and no automatic
action. Replaying apply with the same idempotency key returns the completed receipt
with a new replay delivery receipt and `replayed=true`; the original is preserved.

**Recover** (`repair-recover`) is a closed table over journal state: PREPARING/STAGED
→ discard temps (`FAILED_CLEAN`); APPLYING → roll back renamed (`FAILED_ROLLED_BACK`)
or block if a target is unrecognized; APPLIED/INDETERMINATE → verify every exact
postimage and the complete applied-path set before re-snapshot and commit;
COMMITTED/FAILED_* → none; RECOVERY_BLOCKED → refuse (`HOST.IO_FAILURE`,
`REPAIR.RECOVERY_BLOCKED`, exit 4). Every recovery mutation requires an authorization
bound to this repairPlanId and journal requestId; inspection alone is read-only.
Restore verifies all available retained preimage hashes before its first write.
Corrupt bytes yield LEDGER.CORRUPT / REPAIR.PREIMAGE_CORRUPT (4) with no target change.
Unavailable bytes return an exact restore intent and REPAIR.RECOVERY_REQUIRES_BROKER,
without claiming rollback completed. Recovery never re-applies an edit.

**Verify** (`verify`) always admits a **fresh snapshot** after apply; it never reuses
the pre-apply Run. If the fresh snapshot differs from `appliedSnapshotId` the step is
`REQUEST.PRECONDITION_FAILED` / `REPAIR.SOURCE_MOVED` and no Run is sealed; otherwise
it seals a new authoritative Run and reports `VerificationOutcome`
(applied/verified snapshot, targets remaining, net-new findings). A separate immutable VerificationLinkV1 binds receiptId, verificationRunId, both
snapshots and the verification request/step. The apply receipt is never rewritten
and remains retained if verification fails.

---

## 7. Explicitly authorized test execution (AR-08)

Repository code execution is disabled by default. `opensip test run` (request class
`execution`) is admitted only when: the security unit admits a `RepoExecutionGrantV2`
with principal `P-TRUSTED-REPO`, execution class `test-runner`, bound to this
project, snapshot digest and the exact `argv` digest, expiry operation-end, never
inherited (`TEST.PRINCIPAL_NOT_ADMITTED` otherwise); CI uses a pre-existing policy
record (`TEST.INTERACTIVE_CONSENT_IN_CI`); `argv[0]` is a `LogicalPath` member of the
sealed snapshot or a member of the declared toolchain `closure2`
(`TEST.ARGV_NOT_IN_CLOSURE`); the working directory is the project root or a
`LogicalPath` inside it; the environment is constructed from an allowlist only, `PATH`
is never copied (`TEST.ENV_NOT_ALLOWLISTED`) and is set to the toolchain closure; and
the live tree still equals the `afterStep` snapshot. There is no shell string and no
interpolation anywhere in the schema.

The step **discloses** and does not confine: `effects.network/subprocess/
filesystemWrite` are `DISCLOSURE-ONLY` unless the security unit's platform truth
table measures a primitive; a claimed enforcement without a measured primitive is
refused (`TEST.CONFINEMENT_CLAIM_REFUSED`). The mandatory sentence before spawn is
"Repository test command will run with your user authority. OpenSIP does not prevent
network access or other effects on this platform." Output is bounded and truncation
is recorded. The outcome is a `TestPayloadV1` wrapped as an `import2` of kind `test`
— evidence, never Coverage and never a verdict; a verdict may depend on it only
through a declared policy predicate. Imported independently prepared test results
are the supported alternative.

---

## 8. Command inventory, outputs and parity (AR-13 surfaces, AR-16)

`workflows/command-inventory.v3.json` is the single intended inventory,
validated by `workflows/schemas/evaluator3/command-inventory.schema.json`; the checker refuses a command name
outside the closed enum and requires every golden to be reachable by the model.

| Group | Commands |
|---|---|
| analysis | `opensip` (default: discovery + durable analyze), `analyze [--ephemeral] [--baseline]`, `fit` (advisory whole-repository report), `audit --baseline [--audit-profile] [--closure-bundle]`, `repair verify` |
| query | `recommend` (advisory next-step suggestions from discovery), `query OP`, `baseline show`, `policy show`, `policy test`, `candidates`, `inspect`, `review brief`, `repair preview` |
| mutation | `import`, `baseline adopt|export|upgrade`, `policy init`, `waive`, `review join`, `repair apply`, `repair recover`, `purge` |
| execution | `test run`, `native prepare` (both explicitly authorized) |
| lifecycle / serve / meta | `install`, `update`, `core update|repair|rollback`, trust/store commands, `doctor`, `agent serve`, `help`, `version`, `completion` |

Only `policy init`, `waive`, `baseline adopt|export|upgrade` write tracked intent.
Advisory projections never offer SARIF or manufacture a Control verdict. `fit`
may run an authoritative analysis by default and then return an advisory report;
its underlying sealed Run retains its own verdict.

**Renderers.** `human` v1, `json` v3 (the `CommandEnvelope` major 3 is the parity
reference), `sarif` v1 (analysis class only; results equal envelope findings
one-to-one, verdict/deficiency in run properties), `html` v1 (analysis and query;
static single file, no script-fetched data, shows resolution completeness and
disclosures), `agent` v1 (the JSON envelope plus `agentHints` that never alter a
parity field). Each command names its `parityFields`; every applicable renderer must
carry semantically equal values for them. Every advertised SARIF command (`default`,
`analyze`, `audit`, `repair-verify`) must declare the common fields `run-id`,
`verdict`, `required-coverage`, `deficiency`, `findings`, `termination-class` and
`retention-disclosure`; inventory admission refuses an omission. SARIF results
and run properties are taken from this same declared host projection, as are
human/JSON/HTML/agent values; no renderer reads an undeclared findings field or
substitutes null for a present verdict/deficiency. Audit adds its comparison
fields while preserving the current analysis result. Repair verification adds
applied/verified snapshot, snapshot-match, targets-remaining and net-new-findings
fields while preserving the fresh verification Run's findings and verdict.
An empty findings array is a real empty result; it is never inferred from a
missing projection field. Ephemeral analysis retains its existing no-Run rule:
`run-id` is explicitly null in the projection's non-authoritative case,
never a fabricated Run. Required-output failure still follows the law below.
The host projection must be total over the selected command's `parityFields`
before a renderer consumes it: every field has its schema-admitted value,
including an explicit null only where that field permits it. A missing field
or projection exception is a required-delivery operational fault, not an empty
result or a successful partial rendering: `operational-failed`, exit 4,
`faultCause=delivery-required`, `DELIVERY.REQUIRED_FAILED`. If a Run was already
committed, the termination retains its RunId and the after-commit detail below;
otherwise no RunId is invented. This classification also covers a pure reference
projection helper raising `KeyError`; that exception alone is not a public
termination. Actual host exception handling and renderer conformance remain
DR-G17/DR-G20 implementation qualification obligations.
Requesting a non-applicable format is
`REQUEST.UNKNOWN_OPTION` / `OUTPUT.FORMAT_NOT_APPLICABLE` (2). Failure of the selected
required renderer **after** a committed Run is `DELIVERY.REQUIRED_FAILED` (4) with
detail `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, the `runId` in the termination, and
no rewrite of the Run; failure of an optional export sink leaves `success`.

**Query.** The twenty closed operations remain read-only. The current schema is
`workflows/schemas/evaluator3/graph-query.schema.json` major 3. The incorporated
[query projection contract](../../../coop/design-corrections/workflows/query-projection-contract.v3.md)
owns the complete selection, endpoint, result, ordering, traversal, continuation
and evidence-disclosure laws for `graph.neighbors`, `graph.path` and `graph.reach`.
It does not replace the artifact-specific owners of the other seventeen operations.

Graph requests may select `run3`, `snapshot2` or `latest`; before traversal they
resolve to one concrete retained Run and an exact fact-view selection. An empty
resolver domain is `IDENTITY.UNKNOWN`; ambiguity is a typed refusal. A graph
response never echoes an unresolved `latest` alias as its resolved view. Endpoint
identity includes the selected universe and native identity, so equal paths in
different analysis universes cannot silently collapse. Results retain their fact
provenance. Database row IDs and backend iteration order are not public identity
or ordering rules.

The bounded graph contract distinguishes a page boundary from exhaustion of the
logical operation. Page size is at most 1,000; produced items at most 100,000;
semantic depth at most 64; visited nodes at most 1,000,000. `maxDepth` defines the
requested search distance, not an implicit promise of unbounded reachability.
`completeness=required` refuses genuinely unfinished work at an operation bound
with `QUERY.COMPLETENESS_UNMET` (3); exactly reaching a limit with no owed work is
not incompleteness. Best-effort reports any truncation explicitly. A continuation
can page only the bounded result and never reset the work budget; its last page
can remain truncated with no cursor. Total-count disclosure distinguishes an
exact total from a lower bound.

A continuation binds the project, concrete retained Run and fact views,
operation, effective parameters, ordering and position. Publication of a newer
Run cannot change that selection. Index loss permits rebuilding from the same
available closure; unavailable retained evidence or incompatible continuation
inputs cause the contract's typed refusal, never a switch to a newer Run.

For the graph operations, traversal completion and retained evidence sufficiency
are separate typed disclosures, including relevant Coverage, scope, deficiency
and resolution limitations. Exhausting stored edges, returning no rows, or
ending pagination cannot itself prove that no callers exist. Any such finding
must retain the existing native/evaluator authority and citations. All query
responses carry their owned view, evidence disclosure, availability and `advisory`;
the other seventeen operations retain their existing Coverage field. `advisory` is
true exactly for `comparison.diff`, `candidate.list`, `inspection.show` and
`review.brief`. The three graph operations are not advisory and do not seal a Run.

The query command's required parity fields are `resolved-view`, `availability`,
`truncated`, `total-items`, `termination-class` and `query-response`. The last is
the **complete owner-admitted GraphQueryResponseV1**, including the full context,
items and any optional termination; human, JSON and agent renderers preserve its
typed content. For non-graph operations the existing Coverage field stays inside
that response. Graph evidence is not reduced to a synthetic Coverage scalar.
The first four scalar fields are exact projections of the response context;
`termination-class` comes from the enclosing command's actual StepTermination.
If the response carries termination, its entire object must equal the enclosing
termination. The envelope and response must identify the same project. Missing
required query disclosure follows the existing required-delivery fault law.

The envelope's compact `QueryResult` remains a separate record. For graph.*,
`items` is the number of rows on the current page, `truncated` equals the context
flag, `advisory` is false, and `nextCursor` is present exactly when the context
has the identical token. `completenessMet` is true exactly when `countBasis=exact`:
the declared stored-edge operation has completed, even if further pages remain
to be delivered. This is neither native closed-world evidence nor a claim that
all pages were delivered. A lower-bound result therefore has
`completenessMet=false`, including an intermediate page whose `truncated` flag
is false. The other seventeen operations retain their owned summary semantics.
The reference `workflows/query_surface_projection.v3.py` checks these joins and
projects the complete response; it does not admit a Run or prove traversal.

**Doctor.** `opensip doctor` produces a typed report over closures, trust, store,
platform, project marker and the offline window. A produced report is `success` (0)
even when defects are found (detail `DOCTOR.DEFECTS_FOUND`); CI must inspect
`doctor.defectsFound`. Only an unproducible report is `HOST.IO_FAILURE` (4).

A `doctor` report is a **different invocation** and therefore cannot deliver the
absences of an analysis invocation; `DoctorResult.defects[]` remains the
environment report it always was.

**Release-availability absence rides the invocation that selected it.**
`CommandEnvelope.availability` (`CapabilityAvailabilityV1` =
`{stepCount, totalNoticeCount, steps[]}`, each step
`CapabilityAvailabilityStepV1` = `{stepId, noticeCount, notices[]}`) carries
every capability the selected product requires (native §1.4) that this release
did not declare available, for **every requested unit of every analysis step** —
a single-step command projects one step, and a named multi-step invocation
projects one entry per analysis step that made a selection. Each notice carries the complete ownership tuple in **typed
fields** — `capabilityId`, `languageMode`, `workspaceRoot` — with the existing
code `native.capability-unavailable` (a `const`, since the record declares one
condition); the tuple is never concatenated into a `subject`, because
`workspaceRoot` is a `UserInputPath` bounded at 4096 while `BoundedText` is 1024
and a truncated path would collapse two distinct units into one indistinguishable
notice. The collection is composed **per step** —
`{stepCount, totalNoticeCount, steps[≤64]}`, each step
`{stepId, noticeCount, notices[≤1024]}` — because 1024 is the
`analysis-spec.requestedCapabilities` bound and *not* an invocation-wide one: two
admitted selections of 1023 requests each compose 2046 notices, and no notice is
discarded to fit. A step that made no selection contributes no entry, a step that
found nothing absent contributes an empty entry, and the same tuple may recur in
different steps. Order is the selection's own.

Envelope membership alone would **not** deliver it: `render` selects a command's
declared `parityFields`, so `capability-availability` is a declared parity field
of **every** `requestClass: analysis` command — `default`, `analyze`, `fit`,
`audit` and `repair-verify` — and every applicable renderer carries it: human,
JSON, SARIF, HTML and agent. Because it is *declared*, it is also **required**:
the host projection must be total over the command's parity fields, so a caller
whose invocation selected nothing supplies the explicit empty collection
(`{stepCount: 0, totalNoticeCount: 0, steps: []}`) rather than omitting the
field, and an omission is a required-delivery operational fault under the law
above, never a successful partial rendering.

It is **advisory** — it terminates nothing, mints no Coverage, grants no Control
verdict or repair authority, and is never a clone `Candidate`, since published
Candidate records represent actual candidates. `AnalysisResult` is a closed union
and is not widened to carry it.

**Failure envelopes carry their errors.** A `kind=failure` envelope requires a
nonempty `errors` array of `DomainDetail`; where a step termination's optional
`domainDetail` is absent, the composition in native §10 supplies the array from
the route's own detail code, and where it is present `errors` is exactly that
detail so the two surfaces never disagree. Before a Plan or Run exists no run
envelope is fabricated.

---

## 9. D9 goldens and typed detail (AR-16)

Exit codes are the existing table: success 0, policy-failed 1, request-rejected 2,
indeterminate 3, operational-failed 4, interrupted 130. Termination branch contract
(schema-enforced): success carries no error/reason/signal; policy-failed carries
`runId` or `authority=ephemeral`; request-rejected/operational-failed carry
`errorCode` (operational also a non-none `faultCause` from the observation:
host-io, ledger-busy, ledger-corrupt, cas-link, provider-protocol, durability-commit,
delivery-required, output-serialization, extension-install-io, serve-protocol,
host-invariant);
indeterminate carries `reasonCodes`; interrupted carries `signal` and a `runId` only
when a Run was committed before the interrupt. `DomainDetailCode` is explanatory
detail beside an existing code, never a termination code. Selected goldens (the complete retained set
is in the inventory and exercised by the model):

| Situation | Class / exit | Code | Detail / remedy |
|---|---|---|---|
| fresh project, providers installed | success 0 | — | DEFAULTED durable retention disclosed; no policy file written |
| required provider closure not installed | indeterminate 3 | `COVERAGE.PROVIDER_UNAVAILABLE` | `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` → `opensip install provider-typescript` |
| installed closure bytes corrupt / unspawnable | operational-failed 4 | `HOST.IO_FAILURE` | `DELIVERY.CLOSURE_BYTES_CORRUPT` / `DELIVERY.CLOSURE_UNSPAWNABLE` → `opensip doctor` |
| selected renderer fails after commit | operational-failed 4 | `DELIVERY.REQUIRED_FAILED` | `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`; runId retained |
| optional export sink fails | success 0 | — | egress never changes a verdict |
| `--ephemeral` with baseline/repair prerequisite | request-rejected 2 | `REQUEST.UNSATISFIABLE` | `WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY` |
| pivot closure missing / revoked / unmapped project | indeterminate 3 | `BASELINE.RECIPE_UNSUPPORTED` | `BASELINE.PIVOT_DETECTOR_UNAVAILABLE` / `..._CLOSURE_REVOKED` / `BASELINE.PROJECT_UNMAPPED` |
| required evidence lost in audit | indeterminate 3 | `VERDICT.INDETERMINATE` | `COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE` → re-import |
| unmapped / corrupt import artifact | request-rejected 2 | `CONFIG.INVALID` | `IMPORT.MAPPING_REQUIRED` / `IMPORT.ARTIFACT_CORRUPT` |
| duplicate waiver / imperative policy key | request-rejected 2 | `CONFIG.INVALID` | `POLICY.DUPLICATE_WAIVER` / `POLICY.IMPERATIVE_KEY_REFUSED` |
| repair preimage mismatch / source moved | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | `REPAIR.TARGET_PREIMAGE_MISMATCH` / `REPAIR.SOURCE_MOVED` |
| recovery blocked | operational-failed 4 | `HOST.IO_FAILURE` | `REPAIR.RECOVERY_BLOCKED`; journal retained |
| CI interactive test consent / confinement claim | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | `TEST.INTERACTIVE_CONSENT_IN_CI` / `TEST.CONFINEMENT_CLAIM_REFUSED` |
| doctor report with defects | success 0 | — | `DOCTOR.DEFECTS_FOUND`; inspect typed outcome |
| SIGINT before / after settle | interrupted 130 / settled class | — | after-settle is never reclassified |

The exact class/detail pairing is determined by the golden observation and
closed schemas. Disclosure-only success details do not imply a clean doctor
report or grant authority. No new D9 family is introduced.

---

## 10. Identity recipes and evidence limits

H domains here are `workflow.baseline` (`baseline2:`), `workflow.comparison`
(`comparison2:`), `workflow.repair-plan` (`repairplan2:`),
`workflow.mutation-receipt` and `workflow.verification-link` (`receipt2:`),
`workflow.policy-test-result` (`policytest2:`), and `workflow.candidate`
(`candidate2:`). `workflow.mutation-intent` addresses the closed operational
MutationReplayScopeV1 (§1), returning its bare 64-hex H value. Import wrappers use foundation `import`. Auxiliary policy, scope,
resolved waiver, rule program, payload, correspondence, build, observation and
schema-document digests use raw SHA-256 of the exact preimage described above.
`PolicyTestResultV1.suiteDigest` is the bare 64-hex result of
`H("workflow.policy-test-suite", PolicyTestSuiteV1)`, over the entire closed
admitted suite before override application; the suite is retained with the result.
This is an H identity, distinct from raw SHA-256 of the suite's canonical bytes.
Candidate/effective policy digests remain raw SHA-256 of their respective closed
PolicyDocumentV2 canonical bytes. Exact typed admission precedes schema validation;
one foundation canonicalizer is used.

## 11. Reference evidence and remaining integration work

The retained workflow-surface checker compiles fourteen schemas and exercises invocation, comparison, imports,
policy, repair, test admission and surface projections. The retained report gives
exact case/check counts and source hashes. Pivot presence, OS custody observations,
trust, native resolution and effect measurements are trusted synthetic inputs;
no provider, repository command, renderer, ledger or filesystem is executed.
Passing these checks neither qualifies a platform nor independently accepts the design.

Actual Claude authored the initial model and a partial second correction. Codex
then corrected admission, recovery, comparison, fixtures and this prose after
Claude hit its quota. These mixed bytes require fresh independent Claude review.
The host composition and preparation/core lifecycle joins are specified in §12.
The integration status tracks independent review and decision-application blockers;
reference checks do not award readiness or implementation permission.

## 12. Completed host joins (Codex integration correction)

The candidate inventory includes `native prepare` and `core update|repair|rollback`.
Native preparation has a closed NativePreparationParams/NativePreparationResult
branch, no Run and no automatic retry. Native §14 and security S15 own its exact
execution admission, receipt, interruption and prepared-import publication rules.
Core operations are mutation steps bound to a retained CoreTransitionIntentV1 and
security's EXCLUSIVE migration journal. The inventory is the sole command list;
all trust/store placeholders now carry declared candidate syntax.

Test execution consumes the host projection returned only after complete
RepoExecutionGrantV2 schema admission and the security decision. Its platform IDs
are macos-aarch64, macos-x86_64, linux-x86_64-gnu and linux-aarch64-gnu. The actual
security grant reference is retained in the step result. `P-TRUSTED-REPO` remains a
workflow principal spelling; the security and semantic principal identities do not
change. `integration-host-model.py` exercises those exact joins across all four
platforms and per-owner native preparation.

Repair apply likewise consumes a host projection created only after complete
RepairApplyAuthorizationV1 admission. The host rehashes the plan, derives the
expected recipe from that descriptor, checks positive current recipe admission,
and matches the command's exact authorization reference to the admitted record.
The journal retains that complete security authorization reference. Unit repair
fixtures use synthetic authorization projections; the integration model supplies
the real security decision. Neither a caller's claimed admission nor the absence
of a revocation establishes this authority.

Candidate identity hashes `{projectId,kind,key}` under workflow.candidate, excluding
RunId. A finding uses its finding fingerprint as key; a native advisory uses its
producer-defined sourceFingerprint (the normalized relevant source/observation
identity, never only a path). The Candidate record separately names the current
Run. Review suppression therefore survives a new Run with unchanged evidence;
changed evidence resurfaces. Expiry uses actual Gregorian calendar dates, at most
365 days. This changes advisory presentation only, never findings, proofs, baseline
membership, Control verdicts or execution authority.

SourceMapping admission binds both its exact target snapshotId and every source
inventory hash. The native and workflow import builders produce byte-identical
wrappers for the same admitted payload and auxiliary records; integration checks
recompute all retained auxiliary preimage hashes. These are reference joins, not
independent acceptance or qualification of actual native producers.

**The import mirror is authoritative, not descriptive (CB3-SHOULD-1/2).** One
import has one `importId` over one wrapper, and that wrapper is admitted through
**two** documents: the foundation record
`identity-schemas.v3.json#/$defs/import`, which is the authority, and its
declared exact mirror `imported-evidence.schema.json#/$defs/ImportWrapperV2`.
`ImportScopeDescriptor` mirrors the foundation `scope-descriptor` the same way.
Both mirrors carried the words "exact mirror" while disagreeing about what they
admit, in **both** directions, so the byte-identical-wrapper claim above failed
for exactly the inputs the two documents disagreed about:

- the foundation record declares `omissions` and the three scope-descriptor
  arrays `canonical-set` (strictly ascending canonical bytes) while the mirrors
  declared `sequence` (any order) — so an import with `omissions: ["b","a"]`, or
  a scope descriptor with unsorted `workspaceRoots`, was admissible through the
  workflow document and refused by the foundation document that owns the same
  digest preimage;
- the mirror required `blobs` `minItems: 1` and `maxItems: 4096` while the
  foundation record permitted zero and allowed 100000 — a disagreement at **both**
  ends, and the two ends resolve differently (below);
- resolved through their respective primitives, the mirror bound blob rows to
  `common#/$defs/Blob` — `LogicalPath` grammar, `bytes ≤ 268435456` — while the
  foundation record used an unconstrained text path and `bytes ≤ 2^64-1`. That
  pair is invisible unless the `$ref`s are resolved, and it was not reported.

The order and the path grammar resolve to the **foundation** values, which the
mirrors now restate: the foundation record owns the digest preimage, and
`identity-and-evidence` §3 already states both the `canonical-set` annotation
and the logical-path grammar. The **maximum** and the byte bound resolve to the
**import unit's own published hostile-input bounds** — `imported-evidence`'s
top-level description explicitly selects "at most 4096 blobs" and "artifact at
most 268435456 bytes" — carried as a distinct foundation `import-blob` record so
the bound applies to imports and is not silently imposed on `source-inventory` or
closure `tree` rows. Narrowing the foundation record from 100000 to the published
4096 is a stated compatibility change.

**The minimum resolves the other way: `blobs` is `0..4096`.** `blobs` is the
inventory of **auxiliary asset** members, and it is *not* the import's mandatory
custody. The payload bytes and the exact registered schema **document** bytes are
retained and re-hashed independently by registered-payload admission, and those
obligations hold identically when the array is empty — so a self-contained
normalized payload may lawfully retain no auxiliary asset. Three published facts
settle it:

- `ImportedEvidenceRecordV1.sourcePath` is a `UserInputPath`, which the workflow
  common schema defines as *"never enters any content identity; recorded in
  operational records only"*, paired with a receipt;
- **no join anywhere** binds `sourcePath` to a member of `wrapper.blobs`; the
  only `sourcePath` joins belong to `SourceMappingV1`, which binds
  `sourceSha256` to the **snapshot inventory**;
- the archive-member rule — *"an archive member outside the wrapper's `blobs` is
  never read"* (**§3 PO-4**, not §6) — restricts **reading** and is satisfied
  vacuously by an empty list; it never requires that a member exist.

An earlier revision of this contract argued `minItems: 1` from
"`adapterClosure` asserts an adapter ran over the bytes `sourcePath` names, so
the payload could not otherwise be re-derived". **That argument is withdrawn.**
It rested on a field the contract explicitly excludes from every content
identity, and requiring one arbitrary blob would not have established
original-input custody. The foundation record's zero-blob admissibility was
intentional, and observing that the two mirror documents disagreed did not show
otherwise: agreement is a property of the documents, not evidence about which
admitted set is correct.

Agreement is **proved, not asserted**: a semantic differential validates the
same instance against both documents and requires identical admit/refuse
verdicts, with each case sitting on a boundary the two documents once disagreed
about, and with a discriminating-negative floor so the check cannot pass by both
documents being permissive.

The step kind must equal its parameter kind before dispatch. A query-labelled step
cannot carry execution parameters. Review reject/defer always requires an explicit
finite expiry; an indefinite suppression is refused. The host also validates the
retained RuleProgramV2 against the admitted PolicyDocumentV2, resolves the exact
waiver preimage and constructs policy-derivation3 from the same Plan/proof/verdict.
The integration fixture exercises those joins through foundation replay and
reference commit for a finite no-match policy case; full native/DSL qualification
remains separate.

Missing required detector or policy/scope/waiver re-evaluation makes the comparison
indeterminate whenever an enabled rule gates under the selected audit profile,
even when both observed finding sets are empty. Missing evaluation can hide a
finding that appears in neither set; entry counts cannot prove its absence. An
independently established failing gate still dominates indeterminate, as in D9.

Policy evaluation discloses every rule whose required input or coverage is
indeterminate. Only an enabled gating rule at the policy's severity threshold
can make the Control verdict indeterminate. A non-gating rule's unknown result
remains unknown for policy-test finding/no-finding expectations, while leaving
the gate verdict unchanged. Missing required evidence and incomplete coverage
follow the same rule; neither can silently become an authoritative no-match.

The public `DomainDetailCode` vocabulary is the single closed
`public-detail-registry.v1.json` registry shared by identity, security, native
analysis and workflows. The common schema is generated or drift-checked against
its exact entries. Owners register stable details before emitting them; an
unknown detail refuses admission. Dynamic paths or refusal explanations travel
in bounded `subject`/`remedy` fields, never as newly invented codes. The canonical
storage detail is `storage.backup-choice-required`; the earlier uppercase draft
spelling is not admitted. `evidence.expired`, `evidence.purged`, `evidence.missing`
and `evidence.corrupt` retain their distinct meaning in query results.

`evidence.pinned` is the foundation-owned refusal for a direct purge blocked by
active pins. It projects as `request-rejected`, `REQUEST.PRECONDITION_FAILED`,
exit 2, in a failure CommandEnvelope with that DomainDetail in both the
termination and `errors`. The detail's `subject` equals the requested RunId and
its required `purgeDisclosure` is the closed common-schema
`PinnedPurgeDisclosure`: the same RunId, the complete current `activePins`
inventory sorted uniquely by UTF-8 `pinId`, and the three ordered consequences
`named-pins-revoked`, `dependent-evidence-replay-unavailable`,
`sealed-history-retained`. Each operational pin name identifies a host-ledger
pin scoped to this Run and declares `baseline`, `repair-prerequisite`,
`backup-export` or `other-authorized`; names are not content hashes or permission
tokens. No pins are omitted, truncated or aggregated into an anonymous count.
Pin admission bounds each name to 256 Unicode scalar characters and each Run to
4,096 active pins, so the complete refusal stays representable; a new pin that
would exceed these bounds refuses durable admission under the existing retention
precondition rule before any protected operation starts.

The host observes that inventory under the exclusive purge lease and preserves
all named pins on refusal. A later destructive attempt requires the existing
lifecycle authorization and disclosure of its then-current complete pin set;
a flag, this disclosure or the pure projection helper confers no authority.
Revocation and purge occur in the existing protected mutation transaction; a
changed pin inventory requires renewed disclosure before destruction. Shared
bytes and sealed history retain identity §5's rules. JSON, human and agent
purge output preserve the exact named pins and consequences as the
`purge-disclosure` parity field. The reference `pinned_purge_refusal` constructs
the closed refusal from synthetic trusted ledger observations; it implements
neither ledger pin discovery nor destructive authorization.
`validate_pinned_purge_refusal` checks schema and internal field agreement; it
cannot establish inventory completeness without the host ledger. Before emitting
the refusal, the host compares the disclosed named pins with the complete current
set it observed under the exclusive lease. A schema-valid subset does not satisfy
that obligation. This comparison and the renewed disclosure before destruction
remain host responsibilities; accepting the public envelope grants no authority.

The host projects the unit's existing D9 class/code into StepTermination, checks
the declared exit and host faultCause, and attaches the registered domainDetail.
This changes no D9 class, code, precedence or exit. JSON is the parity reference
for CLI, SARIF, HTML and agent output; renderers preserve the exact detail and
remedy or report an explicit projection loss. Goldens include actual security,
native and evidence-availability details, rather than leaving the detail absent.
Trust-recovery import's authorization class is `recovery-authority-quorum`:
only the selected recoveryAuthority keys count, never ordinary root keys.

Evidence-change attribution is deliberately conservative in this product
contract: it includes no counterfactual pivot that replays old source under a
new runtime/test observation. A changed import identity can therefore make an
evidence-dependent comparison indeterminate, including under `full-current`;
that profile does not turn an uncertain attribution into a claim of regression.
Use a fresh authoritative analysis to enforce a rule against its current bound
runtime/test evidence. For CI, a composed invocation can require that current
assessment and a separate static-code regression comparison. Default regression
policies keep observational runtime/history signals advisory. This preserves the
usefulness of richer assessments without treating two observation windows as
equivalent. A future evidence-pivot recipe requires its own reviewed successor.

The host must compute and bind every E1–E3 re-evaluation required by a changed
axis; these are required workflow steps, not options a caller may omit. A host
failure to execute a computable step is an operational failure under the existing
D9 mapping. Typed comparison indeterminacy is reserved for unavailable required
inputs or unsupported admitted recipes, with the missing input named. The
reference model's `boundPivots` set is a synthetic host observation of completed
work, never a user-supplied permission to skip evaluation.

Field-filter types are closed: `confidenceMillionths` permits only integer `gte`/`lte`; the other fields use string `eq`/`neq`/`prefix`/`glob` or string-array `in`. Incompatible field/operator pairs are invalid policy input, never string coercions or silently false predicates.

Core transition lock scope is derived from the admitted `CoreTransitionIntentV1` and the host registry under the installation fence. A same-schema core update/repair keeps the selected store and pinned generations; rollback reselects the rollback store. A schema change or rollback requires every registered namespace, sorted by locator bytes, with nonblocking all-or-nothing EXCLUSIVE acquisition and reverse release. The caller cannot supply `reselectsStore` or a smaller namespace set. Store migrate/rollback use the same installation transition protocol (security S7); their command authorization class is `core-transition-leases`.

Explicit CLI workspace roots may normalize one terminal slash before constructing canonical configuration. Config2 itself contains strict logical paths (plus `.` root sentinel); malformed Config2 is rejected before either discovery instrument. The custody instrument's synthetic direct inputs exercise this CLI normalization and do not bypass Config2 schema admission.

Test-step admission validates the complete closed TestExecutionStepParams before any nested access and requires consentSource to equal the actual admitted security grant projection (`interactive-explicit` -> `interactive-consent`, policy-record -> pre-existing-policy). A caller cannot relabel interactive consent as policy consent for CI. Live source movement in a test step has TEST.SOURCE_MOVED, separately from repair's condition. Intake imports become analysis inputs only through the identity contract's retained source-correspondence join.

The public-detail registry separates public records from internal decision aliases. Host projection always emits PROJECT.WORKSPACE_UNIT_LIMIT for the shared discovery cap (security, shared-helper and native paths) and PROJECT.EXPLICIT_PATH_INVALID for malformed explicit roots; diagnostic counts/reasons travel in subject. Internal WORKSPACE_UNIT_LIMIT, native.too-many-units and native.explicit-root-grammar are never public enum values. The native table key provider-unavailable/capability-missing projects as native.capability-unavailable. The removed pre-Plan projection refusal is retired with no alias. Thus the same shared condition has one machine detail code independent of the instrument that detected it.

Recovery in a later invocation uses the security S10.2 RepairRecoveryAuthorizationV1 and the closed RepairRecoveryIntentV1 retained by its mutation step. The host validates the original journal/plan, admits the fresh authorization and passes a trusted projection to the recovery mechanics; the journal retains the full security.repair-recovery-authorization.v1 reference. The observed journal-state digest prevents a grant from authorizing a changed recovery state. Immediate compensating rollback inside a still-running admitted apply attempt remains part of that apply's broker authority (including cleanup after revocation); it does not fabricate a fresh recovery authorization. The same guarded preimage/postimage mechanics serve both paths, and no public request can invoke those mechanics without admission.


Installation operations (all five core/store operations) retain the same closed intent through mutation inputDescriptorDigest. Security S9.2 owns InstallationTransitionJournalV1. Each durable revision is addressed by the full H('security.installation-transition-journal.v1', revision) reference; its state changes therefore produce a new reference. The installation journal location under the fence selects the current revision, never a caller-supplied reference. An initial mutation Attempt retains installationJournalRefs in durable write order, including failed or abandoned attempts; no field is present if no journal was written. Its first revision is LEASED after the complete derived lock set was acquired. A fresh recovery Attempt instead retains installationRecoveryStartRef, exactly the current revision observed under the fence; its installationJournalRefs begin with that observed revision and then contain the new durable revisions written by this attempt. That first observation is not falsely counted as a write by the recovering attempt. This is operational custody evidence, excluded from Run identity. A host validates each reference/preimage and its intentDigest against the step before retaining it. On crash, journal recovery is the first action under the next installation fence, before project admission. It revalidates the closed intent, recomputes its digest and derived lease set over the frozen registry, and rejects mismatches before interpreting the recovery table. A self-consistent hash cannot make an invalid lease scope lawful.

Journal revision order is LEASED → PREPARING → PREPARED → COMMITTED → DONE, or ABORTED from a precommit state. A recovery that determines RESUME-COMMIT from the store footprint first retains COMMITTED if needed, then DONE; it never rewrites history to imply an unobserved earlier commit. The host binds the frozen intent and immutable registry/scope fields across every retained revision.


Before ordinary project admission, the host inserts a required installation-recovery mutation step if the fenced installation journal requires recovery. It uses the journal's original operation and retained CoreTransitionIntentV1 as inputDescriptorDigest, and a fresh host-minted RequestId/ExecutionId for the recovery invocation/attempt. The built-in workflow name is the originating installation command (from the closed command inventory); this is a host-started recovery invocation, not a second execution of that command's update recipe or an implicit mutation retry. Only the already-journaled transition may be completed or aborted through S9.2; caller parameters cannot nominate an installationRecoveryStartRef or grant extra effects. If recovery fails or is busy, ordinary project admission does not proceed. Terminal DONE/ABORTED journals need release/cleanup only. The new attempt links to the observed durable revision and never appends fictional writes to or rewrites an earlier abandoned Attempt. A recovery segment may begin in any closed state; it must bind that starting reference, retain the same admitted intent/registry/scope, and follow the state table. This gives PREPARED→COMMITTED→DONE recovery a representable independent history while the original attempt remains LEASED→PREPARING→PREPARED.


There is one explicit consent mapping, applied only after actual security admission:

| Security consent.mode | TestExecutionStepParams.consentSource | RepairApplyParams.consentSource |
|---|---|---|
| interactive-explicit | interactive-consent | interactive |
| policy-record | pre-existing-policy | policy |

These field-specific spellings do not define independent authorization mechanisms. Test and repair projections carry the mapped source, and repair additionally carries the admitted CI observation; their workflow mechanics require exact equality with the selected step/context. Interactive consent refuses in CI at security admission. Policy-record consent is valid both in CI and outside CI when the actual policy admission succeeds. Relabelling an admitted grant's source is refused. A completed idempotent repair replay performs no mutation; it returns the existing receipt under the existing replay contract.


### Numeric comparisons and metric redistribution (FW-11)

The inherited architecture13 §6 comparability restriction is binding here: a numeric
comparison needs the same metric definition, supplied diff scope and comparison
base; incompatible inputs must be reported incompatible, never presented as an
improvement. Typed scope/policy/waiver/evidence deltas remain distinct from code
changes. Moving complexity or findings between regions without a comparable
behavioral result is redistribution, not evidence of behavioral improvement.
