# Joint architecture and design review

**Conclusion: the intended-product design is NOT READY for implementation.** The central architecture is worth preserving, but accepted reference models contain defects, several contracts do not yet join into a complete product, and some current-looking prose describes superseded decisions. This review includes earlier Codex and Claude work, including D-370 and D-371; prior approval was evidence to examine, not an exemption from review.

The design target remains **one complete intended-product design, implemented in stages**. The Fallow-informed ideas belong in its shared host contracts; native TypeScript/JavaScript and Rust capabilities supply ecosystem-specific evidence. They are not TypeScript-only. This review neither expands the selected product nor reverses its exclusions.

Review date: 2026-09-05 America/Los_Angeles (2026-09-06 UTC). Subject: the post-D-371 working tree at base commit `2580a9a8de8cac243b2dd1a09fd76fc7f6c96637`, pinned in [subject-manifest.json](subject-manifest.json). The manifest covers 9,363 files / 384,546,056 bytes copied into an isolated read-only review subject. That is the available corpus, **not a claim that every file was read**.

## What we reviewed and how

Codex independently traced architecture, authority, identity, workflows, configuration, lifecycle, quality and performance contracts and executed selected reference checkers. Actual Claude Code, reporting model `claude-fable-5-1`, conducted three independent cold review passes with only Read/Grep/Glob tools: semantic/evidence, security/operations, and product/workflows. Each resolved binding subjects through recorded application acts and followed relevant dependency chains. The [semantic report](semantic-report.md), [security report](security-report.md), and [product report](product-report.md) retain source locations, counterevidence, strengths, coverage and explicit omissions.

Codex then challenged the findings, including its own, against the contracts and retained executable counterexamples. The [semantic counter-review](semantic-challenge-report.md), [security counter-review](security-challenge-report.md), and [product counter-review](product-challenge-report.md) preserve corrections. Initial reports contain claims later narrowed or withdrawn; **the reconciled findings below control this audit's conclusion**. Original reports are retained verbatim, not silently rewritten into consensus. [Finding dispositions](finding-dispositions.json) map all 36 initial observations into these 16 consolidated findings. The final fixed-subject review and agreement are recorded separately in [alignment.md](alignment.md), including AR-02’s differing severity assessments and AR-10’s combined MEDIUM detector-pivot/HIGH fresh-CI priority. Agreement covers the required corrections and readiness, not unanimity on every severity.

This is substantive design review and reference-model testing. It is not implemented-host validation, platform measurement, release qualification, complete exploration of every historical artifact, or a guarantee that no issue remains. No product implementation or frozen-contract repair is part of this audit.

## Findings in accepted contracts and their reference evidence

### AR-01 — Exact integer admission is not enforced (HIGH; reproduced defect)

The accepted configuration reference admits `schemaVersion: 1.0` and `1e0`. Its budget field also admits `1.0000000000000001`, rounded to `1.0`, and `9007199254740991.1`, rounded before validation. The integer-literal control admits an actual integer. JSON Schema validation does not enforce the exact scalar-type law in this model.

Sources: [host-foundation-model.v1.py](../completion/host-foundation-model.v1.py), `strict`, `validate`, and `configuration`; [configuration schema](../completion/preview-configuration.schema.v1.json), integer budget/schema version; [IMPLEMENTATION-FREEZE.md](../IMPLEMENTATION-FREEZE.md), law 18. [Probe results](reproduced-probes.json) reproduce eight configuration observations. The original foundation checker still passes 210/210.

**Correction:** specify and implement the exact typed admission gate before lossy parsing or scalar comparison, and add nested decimal/exponent/rounding negatives alongside valid integer controls. The [security v8 reference](../completion/security_unit_lib_v8.py) already has exact-type/float refusal cases; reuse that discipline when auditing other adapters, beginning with the untested permission-policy carrier; DR-G13's `schemaMajor: 1.0` also passes. This is a reference-model/corpus defect, not a shipped vulnerability. Primary owner **DR-103**, joined with DR-123/125 and DR-G12.

### AR-02 — Quality-report acceptance lacks independent subject and oracle binding (MEDIUM; reproduced reference-validation gap)

The DR-G13 validator compares executable digests in one candidate field with another candidate field. Changing both copies consistently still passes against unchanged trusted runner inventory. Setting every fixture's expected and actual count to zero also passes. The pinned corpus contains nonempty expected observations, but this validator does not derive the expected result from that oracle.

Sources: [check_g13_result_design_v4.py](../completion/check_g13_result_design_v4.py), `HARDWARE` and `valid`; [quality corpus](../completion/quality-corpus-manifest.v1.json); [quality contract](../completion/analysis-quality-completion.v2.md), exact-set thresholds and mandatory result/fixture/subject joins. [Probe results](reproduced-probes.json) include a positive control and three mutations. The original DR-G13 checker passes 58/58.

**Correction:** bind reports to an independently supplied signed subject, derive expected observations from the pinned corpus, and bind actual observations to the authenticated measurement producer. Counts and a claimed `expectationMatched` boolean cannot alone establish exact-set equality. Preserve adversarial mutations in a reviewed validator successor. Actual measurement acquisition remains qualification work; the design intends a trusted report producer. Both Codex and Claude identify the missing binding. The product lens ranked the reference defect HIGH; the semantic lens ranked the qualification join MEDIUM. This report uses the narrower MEDIUM characterization and does not claim an exploit of an existing CI service. Primary **DR-118**, with DR-121 and DR-G13.

### AR-03 — Automatic project discovery lacks a shared-directory trust boundary (MEDIUM; contract omission)

Without an explicit project path, the foundation walks to the nearest ancestor containing a regular `opensip.json`, stopping only at filesystem root. A different user able to write a shared ancestor can place that file and influence the selected root and configuration. Configuration cannot grant permissions, but it can choose component pins/holds, scopes and budget; selecting an unintended broader root can widen inputs. Actual cross-user report disclosure was not executed.

Source: [host foundation](../completion/host-foundation-completion.v2.md), §§1–3. Operational-root ownership checks do not specify the project-discovery boundary.

**Correction:** define trusted discovery boundaries and config-file provenance, including directory writability and explicit override behavior. Ownership of a root-owned shared directory alone is insufficient. Require deterministic shared-parent, nested-project, symlink and CI cases. Primary **DR-103**, with DR-104/125, DR-G12/DR-G18.

### AR-04 — A future clock excursion has no reviewed trust-floor recovery (MEDIUM; contract defect)

An operation writes `evalHighWater = max(recorded, wallClock, lastAccepted)` before expiry evaluation. A wall clock accidentally advanced years into the future therefore leaves ordinary current metadata expired even after the clock is corrected. Restore preserves the high-water mark. The lockout may last until real/signed time catches up; “permanently bricked” is too strong.

Sources: [security v8](../completion/security-completion.v8.md), §§4.2/5.5; [security v2](../completion/security-completion.v2.md), §4.2; [reference evaluation_time](../completion/security_unit_lib_v8.py). This consequence follows from the published transition; no OS clock was changed.

**Correction:** design and review forward-jump handling or recovery together with expiry, revocation and anti-rollback invariants, and retain excursion/correction cases. A convenient time clamp or floor reset is not accepted by this review. Primary **DR-112**, DR-G08.

### AR-05 — Expired-root recovery and live trust revocation need explicit transitions (MEDIUM; defects by omission at security joins)

Two separate traces need closure. An offline install receiving root N+1 after N expired needs a rule distinguishing successor-chain signature verification from the final root's freshness check. A long-running operation needs the path by which a newly accepted trust revocation invalidates its grants and pending effects. Existing journal `trust-revoked` vocabulary, process-death recovery and re-verification on a new operation do not by themselves define live invalidation.

Sources: [security v1](../completion/security-completion.v1.md), §§3/4, especially §4.3 OD-112-3’s decided `alreadyRunning=refuse`; [security v8](../completion/security-completion.v8.md), §§2/5/7; [security architecture](../../v2/architecture/03-configuration-and-security.md), revocation law; [journal schema](../completion/security-schemas.v8/journal-record.schema.json), REV. The expired-root omission is LOW severity with medium confidence; the live-revocation defect is MEDIUM for the full product (LOW for the preview). These are contract traces, not demonstrated production attacks. Selection change, component trust revocation and permission revocation must remain distinct.

**Correction:** retain expired-intermediate/root-update cases with anti-rollback and final-freshness checks; define trust-counter observation, revocation linearization, cancellation, cleanup and completed-before-revocation disclosure for live effects. Primary **DR-112**, with DR-105, DR-G08/DR-G09.

## Product contracts that still need to join

These findings refine D-371's existing OPEN obligations. They do not imply that D-371 claimed those contracts were complete.

### AR-06 — Supported platforms must be decoupled from an accidentally narrow measurement population (MEDIUM; integration gap)

The current profile admits exact macOS build/kernel/loader identities, and Linux's measured Ubuntu kernel flavor/series plus ext4. Its qualification rule permits only profiles measured on the named hosted class. Thus an ordinary machine outside those observations can refuse despite sharing an advertised OS/CPU family. APFS/ext4 and stable birth-time further narrow support. Containers and bind mounts are conditionally admitted when their actual observations satisfy the profile; NFS, SMB, overlay, 9p, virtiofs and tmpfs are excluded.

Sources: [security v8](../completion/security-completion.v8.md), §§8.3–8.7; [foundation](../completion/host-foundation-completion.v2.md), §§1–2; [current scope](../../v2/architecture/10-mvp-and-future-scope.md). Multiple release profiles are possible; one example fixture is not the entire future support set. Narrow fail-closed admission is deliberate, not intrinsically incorrect. A companion LOW documentation hazard remains: security v8 §8.6 describes the Linux consequence but does not disclose the macOS build-specific refusal from §8.3.

**Correction:** select and publish the actual supported population, update the measurement/profile contract to qualify it, and test profile availability across normal OS updates. Preserve the stated trust guarantees; replacing exact identity with a broad ABI check is not automatically safe. Primary **DR-126**, with DR-119, DR-G13/DR-G22.

### AR-07 — Rust semantic depth needs sealed dependency inputs and an honest execution boundary (MEDIUM; integration gap)

The Rust protocol transports sealed project files and prepared generated outputs, but the reviewed join does not explain how external crate source/metadata reaches the semantic worker without ambient filesystem or network access. Separately, a preparation grant promises network-disabled repository-controlled execution while the accepted permission model largely discloses rather than enforces process/network bounds. A grant alone does not supply confinement. Repository-controlled code is outside security v8 §1’s first-party trusted computing base; an in-host execution grant needs an explicitly modeled principal and authority boundary at DR-105 before admission.

Sources: [resolved inputs](../artifacts/resolved-inputs.v2.json), `projectModel.semanticUniverse` and `rust-v1`; [Rust protocol](../artifacts/rust-provider-protocol.v2.json), `repositoryExecution`, `preparedOutputCustody`; [permission table](../artifacts/permission-truth-tables.v7.json); [security architecture](../../v2/architecture/03-configuration-and-security.md).

**Correction:** name supported native cells and input acquisition/custody explicitly; provide a sealed dependency-source/metadata path and a reviewed preparation/import boundary. Preserve useful semantics for supported nongenerated scopes and truthful indeterminate results elsewhere. D-371 excludes *automatic* repository execution, not every separately authorized operation; prepared external input is a design option, not an already completed solution. No silent sandbox/DR-128 scope expansion. Primary **DR-118**, with DR-119/120/105 and DR-011-R05. Dependency-path absence is medium-confidence, bounded by the searched subjects.

### AR-08 — Invocation, repair and verification need one operational lifecycle (HIGH; known open contract)

An analysis derivation DAG does not define a workflow that analyzes, queries stored evidence, adopts policy/baseline changes, applies a repair, and verifies a new snapshot. An immutable source-bound Run cannot silently become the identity of all those operations. The repair constraint mentions separately authorized tests, but a Rust resolution grant is not a general test runner and the current admitted command/effect classes do not provide that execution contract.

Sources: [product contracts](../../v2/architecture/13-evidence-workflows-and-product-contracts.md), §§5/9; [surfaces](../architecture/08-surfaces-and-topology.md), multi-stage workflows; [control contract](../completion/control-completion.contract.v5.md); [current scope](../../v2/architecture/10-mvp-and-future-scope.md).

**Correction:** bind operational invocation/step attempts to source-bound analysis Runs and action artifacts; define required/optional dependencies, cancellation, retry/idempotence, aggregate exits and post-mutation verification. Select and contract any test-execution capability separately, including subprocess/input/output authority and failure paths. Imported test evidence and executed verification are different operations. Primary **DR-131**, with DR-117/133/105/107/109/125 and evidence/D9 owners.

### AR-09 — Authoritative identity, retention and persistence remain a full-product blocker (HIGH; known open contract)

Detailed identity recipes exist, but presence, application and closure of required inputs are different questions. Run identity/attempt identity, evaluation-authority sealing, proof references and canonical encodings need one accepted dependency chain. The private preview project namespace and the inherited host-owned ProjectId marker/registry also need an explicit join for moves, clones, tenant isolation and storage.

Sources: [freeze](../IMPLEMENTATION-FREEZE.md), §7.1; [blueprint](../IMPLEMENTER-BLUEPRINT.md), current-head table and correction box; [evidence identity recipes](../artifacts/evidence-identity-recipes.v5.json); [resolved inputs](../artifacts/resolved-inputs.v2.json), `projectIdContract`; [foundation](../completion/host-foundation-completion.v2.md). Applied identity material does not authorize choosing an otherwise reserved Run recipe. In particular, the freeze’s statement that the RunId and EvidenceDigest chains “bottom out in capabilityManifestId” is stale: the remaining dependencies include the unapplied evaluation-authority seal and the [canonical-JSON profile](../artifacts/canonical-json-profile.v1.json) with unresolved UR-1–UR-5. The DR-001 crosswalk must correct that dependency statement.

The binding CD-RT-5 durable-default choice must survive reconciliation with stale “no policy means ephemeral/refuse” prose. The full-product default command must state its request class and explain first-use writes. Custody, retained/current availability, replay, cache, backup, purge, privacy and D9 need one integrated writer/authority model.

**Correction:** resolve actual remaining identity inputs and authority, then bind durable request admission, consent/default provenance and lifecycle. Do not invent a missing preimage, reverse CD-RT-5 silently, or count the non-authoritative preview as closure. Primary **DR-002**, with DR-004–009/011/109/113/124.

### AR-10 — Baseline comparison needs runnable prior semantics and portable custody (HIGH; integration gap)

The detector pivot requires the prior detector to run on current code. Fact-identity dual emission supplies fingerprint migration, not an older executable algorithm. Its citation as the supplier of runnable prior semantics is incorrect. A fresh CI runner also needs an admitted baseline/evidence closure and a compatible pivot implementation; a reference to a previous machine's local store is insufficient.

Sources: [versioning v8](../artifacts/versioning-policy.v8.json), `detectorSemanticDelta.theFix.requires`; [fact identity](../artifacts/fact-identity-policy.v2.json), migration witness; [lifecycle](../../v2/architecture/04-lifecycle-delivery-and-operations.md), retention roots; [product contracts](../../v2/architecture/13-evidence-workflows-and-product-contracts.md), §6.

**Correction:** define retained or bundled prior algorithms, compatible executable closures, baseline export/import custody and removal/expiry behavior. Test a clean CI machine across a detector-major change. Existing indeterminate fallback is safe and must remain; no claim that every version change necessarily fails. Primary **DR-111**, with DR-006/107/122/123/127/130 and DR-011-R13.

### AR-11 — Comparison and imported evidence need typed, identity-bound successors (MEDIUM; known open contracts)

The closed comparison result vocabulary does not yet express the required separation of detector, policy, scope, waiver and evidence-availability changes. Imported runtime/test/history inputs likewise need admitted identity, build/source mapping, observation window and completeness semantics that affect planning and predicates without becoming hidden inputs.

Sources: [versioning v8](../artifacts/versioning-policy.v8.json), `comparisonSchema`; [resolved inputs](../artifacts/resolved-inputs.v2.json), `planIdContract`; [product contracts](../../v2/architecture/13-evidence-workflows-and-product-contracts.md), §§6–7; [D9](../artifacts/d9-exit-contract.v1.14.json).

**Correction:** author versioned comparison/import contracts and typed cause/remediation mappings, with stale/wrong-build/corrupt/unmapped evidence and policy-only delta cases. A new D9 family by a particular name is not required if an existing lawful typed route suffices. Observation of no hits is not universal non-use. Primary **DR-111** for comparison; **DR-118** for evidence intake, joined to DR-006/007/119/120/122/123.

### AR-12 — Examining every subject does not establish complete reference resolution (HIGH; semantic contract defect)

Claude's counter-review supplied a stronger case after Codex challenged the initial finding: module A exports `foo`; module B imports A as `m` and calls `m[k]()` with a runtime string. Examining every subject and emitting the known binding for `m` does not establish that `foo` has no consumer. The transport's completeness rule commits the exhaustive examined subject/target partition; the reference payload has no explicit unresolved-target representation, and sufficiency accepts a complete resolved-binding view. The contract needs to prevent examination-complete from being interpreted as resolution-complete by a universal-negative predicate.

Sources: [delivery](../artifacts/delivery.v2.json), `CoverageResultV1.completenessRule`; [C-2 coverage key](../artifacts/c2-plan-stage-schema.v4.json), `subjectScopeCommitment`; [fact plane](../artifacts/fact-plane.v1.json), reference payload, sufficiency and R1-FP-03; [sufficiency checker](../artifacts/check-fact-plane.py). This is a contract counterexample, not an executed dead-code finding or repair. The current model can refuse safely with `coverage=unknown`; the defect is the missing resolution-completeness obligation and accurate deficiency/remedy for unresolved edges, not the lack of that fallback.

**Correction:** explicitly bind complete coverage to the requested relation/rung and predicate's closed-world assumptions, including unresolved/dynamic edges, and retain the computed-access counterexample. A subject-set commitment alone cannot prove resolution completeness. Use a reviewed completeness rule or richer representation as needed, with truthful deficiency and D9 mapping; no new global scalar ranking. This must gate authoritative no-consumer findings and repair prerequisites. Primary **DR-004**, with DR-005/006/118/133 and DR-011-R01.

### AR-13 — Native cells, discovery and advertised output surfaces need exact acceptance contracts (MEDIUM; known open contracts)

TypeScript conformance does not establish JavaScript support. Name JS without tsconfig, ESM/CommonJS and allowJs/checkJs behavior explicitly. Root discovery must reconcile inherited explicit/config/VCS boundary rules with the preview's ancestor-or-CWD rule and define monorepo units. HTML and agent projections need named applicability, versioning, semantic parity and required-output failure contracts under the existing output owners.

Sources: [scope](../../v2/architecture/10-mvp-and-future-scope.md); [resolved inputs](../artifacts/resolved-inputs.v2.json), `projectModel`; [operability](../artifacts/operability.v10.json), `projectionParity`; [foundation](../completion/host-foundation-completion.v2.md), §2.

**Correction:** exact TS/JS/Rust cells and mixed-language/monorepo cases; one effective discovery rule and advertised command/surface inventory; named HTML/agent parity coverage. Existing umbrella rows already own these areas—the gap is contract specificity, not absence of all ownership. Primary **DR-119** for cells, **DR-103** for discovery, **DR-122** for projections; DR-118/123/125/131 join.

### AR-14 — Delivery stages need state and trust continuity (MEDIUM; integration gap)

The preview intentionally admits closed major-one vocabularies and has no general cross-major bridge. The full product needs evidence, repair, update and import surfaces beyond them. Its future stage transitions need a defined path for operational state and trust floors; the explicit legacy-prototype coexistence decision does not alone cover upgrades between OpenSIP's own future stages.

Sources: [compatibility matrix](../completion/compatibility-matrix.completed.v5.json), S-STATE/S-CTRL/S-SCHEMA; [distribution runtime](../completion/distribution-runtime-completion.v2.md), §3; [security v8](../completion/security-completion.v8.md), trust-floor preservation; [scope](../../v2/architecture/10-mvp-and-future-scope.md), delivery stages.

A concrete transition case is [root admission](../completion/security_unit_lib_v8.py): schema-one admission refuses an active TR-REPAIR role and nonempty `kernelAttestationKeys`, and the stage-one reader has no schema-two chain. DR-107/110/130 must specify a fresh-install path or a verified schema/core transition that the earlier trust state can authenticate.

**Correction:** design supported update/migration ordering, compatibility refusal, rollback and trust-floor continuity now. Closed enums are not themselves bugs and should not be opened speculatively. Historical preview non-continuity is disclosed; it does not prove all future upgrades impossible. Primary **DR-107**, with DR-110/111/112/130. Concurrent same-project agent operations also need explicit workload/lease cases at DR-107/125 and DR-G18; no deadlock was proven.

## Documentation and remediation accuracy

### AR-15 — Effective decisions need one readable current account (MEDIUM; documentation hazard)

The blueprint already explains that capabilityManifestId and policyOutcome.derivationDigest recipes were completed in applied heads, while parts of the freeze/register still call them unproduced. Retention prose still describes a blocked/defaultless state superseded by CD-RT-5. Some manifests self-describe as unadopted although a later act binds their bytes. The application manifest’s `observedSha256` annotations are authoring residue ignored by its checker; its actual pins remain authoritative. Duplicated section numbers 10–12 in security v8 must not be treated as unique heading selectors. Preview-era gate exclusions are easy to mistake for full-product standing. The [SEALED product-boundary chapter](../architecture/01-product-boundary.md) still lists Windows and a Rust V1 spine without a D-371 applicability annotation; the command vocabularies in [surfaces](../architecture/08-surfaces-and-topology.md), [Map versus Control](../../MAP-VS-CONTROL.md), and the [preview reference](../completion/reference-architecture.v2.md) also need one explicit current inventory.

Sources: [blueprint correction](../IMPLEMENTER-BLUEPRINT.md), §5.1; [freeze](../IMPLEMENTATION-FREEZE.md), §7.1; [evidence chapter](../architecture/06-evidence-and-persistence.md); [application manifest](../completion/architecture-application.v1.json); [central register](../../v2/architecture/08-decision-and-readiness-register.md).

**Correction:** a current narrative/head/obligation crosswalk through DR-001/011 and existing review owners. Preserve frozen evidence bytes and annotate their historical applicability rather than rewriting old acceptance. Give each obligation an accountable lead; D-371 already forbids substituting row counts for contract closure, so no new “completion loophole” is claimed. Primary **DR-001**, with DR-006/009/011 and DR-201–205.

### AR-16 — Missing-input and operational outcomes need precise user guidance (LOW; contract/documentation refinements)

Incomplete input closure currently shares provider-unavailable vocabulary whose generic remedy is installing/enabling the provider; when the provider is installed but dependency inputs are absent, that guidance misdirects users and agents. Provider-returned Unavailable and selected executable delivery failure already have different lawful outcomes (respectively indeterminate/exit 3 and delivery failure/exit 4); the initial “three outcomes for one request” claim was withdrawn. A core-only installation's unselected/missing default closure still needs an explicit admission golden.

Sources: [delivery](../artifacts/delivery.v2.json), `providerDeliveryFailure` and package resolution; [fact plane](../artifacts/fact-plane.v1.json), deficiency remedies; [D9](../artifacts/d9-exit-contract.v1.14.json); [distribution runtime](../completion/distribution-runtime-completion.v2.md). Also disclose the decided offline trust-refresh window and doctor's successful-report/exit-zero behavior when defects are found; CI must inspect the typed outcome.

**Correction:** provenance-specific cause/remediation and command goldens, plus readable offline/doctor guidance. Do not change exit codes by editorial inference. Primary **DR-123**, with DR-007/112/114/118/131.

## What remains sound

- The common host owns authority, planning, policy, storage and output; providers contribute evidence and the evaluator stays pure.
- Facts, findings, Coverage, verdicts and operational outcomes are distinct. Failed required output after a committed Run does not rewrite that Run.
- Provider output remains candidate data until the complete protocol transaction, successful process exit and EOF. Partial/faulted transactions do not leak findings into authority.
- Sealed inputs, explicit native capability limits and refusal of ambient tool substitution support reproducibility.
- Advisory/model judgments cannot become Control verdicts or authorize repairs. Runtime observations and clone similarity do not prove safe deletion.
- Lifecycle fence/lease ordering, non-blocking census, reference-safe retention and crash reconciliation address real failure classes. No deadlock was demonstrated by this review.
- Trust floors, deny-by-absence policy and honest disclosure of confinement limits are valuable constraints to preserve while closing the gaps above.

## Validation and limits

| Executed reference check | Result | What it establishes |
|---|---:|---|
| Host foundation | 210/210 | Retained configuration/foundation scenarios, with injected native observations |
| Security v8 | 864/864 | Retained schema, signature, witness, journal and security model cases |
| Lifecycle carrier v2 | 200/200 | Reference lifecycle behavior, including real SQLite/filesystem/process-death exercises with trusted callbacks |
| Control completion v5 | 484/484 | Retained control/protocol design cases |
| DR-G13 result validator | 58/58 | Retained synthetic report validation cases |

Total: **1,816 passing reference checks**, plus **12 retained adversarial/control observations** exposing AR-01/02. AR-12 is a separate source-level counterexample and is not included in those execution counts. The [portable probe](reproduce-probes.py) and [observed results](reproduced-probes.json) are retained. The baseline reports are [foundation](host-foundation-baseline-report.json), [security](security-baseline-report.json), [lifecycle](lifecycle-baseline-report.json), [control](control-baseline-report.json), and [DR-G13](g13-baseline-report.json). These counts do not establish production behavior or absence of defects.

The review environment used Python 3.12 and jsonschema 4.25.1; detailed versions and pins are in reports. Claude read source and Codex's retained observations; Claude did not independently execute those checkers. No full cross-platform host, native analyzer, repair engine or release was run. No live source was modified during cold review. Validation of the final review record and navigation is in [validation.json](validation.json).

## Correction order and readiness

1. Correct the accepted admission and gate-evidence defects, and settle discovery/trust recovery and live-revocation boundaries with retained negative cases.
2. Select exact supported platform/native capability cells, input acquisition and execution boundaries; make their support population and limitations reviewable.
3. Close identity, authoritative evidence, retention and state/trust continuity contracts. Define invocation/Run/attempt relationships before dependent workflows.
4. Complete baseline/pivot, comparison/import, policy/review/repair/verification and output contracts with joined success, partial, failure, cancellation and recovery scenarios.
5. Refresh the current narrative and claim matrix, then independently review the corrected integrated design. Design acceptance precedes implementation authorization; product qualification follows implementation.

The [central readiness register](../../v2/architecture/08-decision-and-readiness-register.md#unified-product-design-readiness) remains the sole readiness checklist. The AR findings name correction obligations at its existing rows, not a parallel completion regime. This audit supplies evidence for those owners; it grants no SATISFIED grades, does not accept an unreviewed contract successor and does not authorize implementation. D-369 remains a historical scoped acceptance; D-370/D-371 remain the selected product direction.
