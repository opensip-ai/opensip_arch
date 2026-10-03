# M3 operability plan r1 — independent review

**Verdict: REQUIRED-FINDINGS — 10 required revisions.**

The direction is useful and the milestone order is broadly right. This revision is not ready for acceptance because it conflates invocation and Run identities, leaves a source-leak path through raw provider output, and proposes effects/messages outside current custody and schema contracts without naming all affected successors. Its logging and crash paths also need explicit bounds and failure behavior.

This is a review of a plan. The fixes below require revised proposals, dependency placement and acceptance controls, not implementation or measurements in this review. No accepted law is changed by this verdict.

## Exact subject and scope

- Subject: [PLAN.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md), **19287 bytes**, SHA-256 `f2005ed0477f1de5690c023945a74a7534396aa2b376eef62ca71d6da65b20d5`.
- Product HEAD/main: `eb0d50398035fe3532dadc332f88cf1d8bc4cb69`.
- Predecessor HEAD: `83f705d8a33ec917cc5b3380e126788b6824d630`.
- Method: static code/JSON/document inspection, byte/hash checks and read-only Git revision checks.
- No product code, crash matrix or test lane was run. No repository file was edited; no commit or push was made. The real OpenSIP home and private 413 UUID fixture were not accessed.
- The companion analysis-quality plan is not an accepted subject of this review. Its mutable current text was consulted only for the timing/measurement join.
- Historical candidate artifacts are not promoted by filename/header. D-369 application selectors, D-372 current product contracts, selected product schemas and accepted M2 owners supply the standing for comparisons.

## Required findings

### OP-R1-01 (P2) — Correct the inventory of existing contracts and current product behavior

**Location:** PLAN.md §1, lines 11–32; §2 K3, line 41

**Problem:** “Concrete contracts don't” and “no … redaction rule … anywhere” are false. DR-125's accepted application names concrete typed SDK APIs and a host-owned configuration registry; distribution-runtime-completion.v2 §8 specifies framing/backpressure/cancellation and deliberately introduces no generic progress frame. DR-114 already specifies construction-time secret exclusion, a two-tier redaction guarantee/disclosure, path handling, ANSI ordering and bounds. Historical operability material also specifies correlation, budget ownership and support-bundle privacy, although its standalone candidate header is not application authority. The product has production stderr writes in CLI bootstrap.rs. The predecessor's last-resort fatal path does not carry logRef, so K3's “every user-facing error” is also overstated.

**Required plan change:** Replace the blanket absence claim with a source-resolved inventory: accepted contracts, existing product behavior, implementation gaps and proposed successors. Cite the DR-125/DR-114 application selectors and current DR-G20.product-v1/DR-G21.product-v1 obligations. Correct the stderr and predecessor-correlation claims. Preserve the genuine unchosen items, such as the proposed tracing stack and file retention defaults.

**Evidence:**

- [opensip_arch/docs/v2/architecture/00-status-and-authority.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/architecture/00-status-and-authority.md:3) — D-372 product authority and D-369 preview application are distinct.
- [opensip_arch/docs/v2/architecture/08-decision-and-readiness-register.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/architecture/08-decision-and-readiness-register.md:314) — DR-125 accepts typed reference SDK APIs and the exact host-owned registry.
- [opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md:513) — Concrete SDK operations and existing-channel/backpressure obligations.
- [opensip_arch/docs/coop/artifacts/doctor-contract.v4.json](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/artifacts/doctor-contract.v4.json:1005) — Existing redaction rules; standing is resolved through DR-114's application, not the artifact header alone.
- [opensip/apps/cli/src/bootstrap.rs](/Users/sb/code/opensip-ai/opensip/apps/cli/src/bootstrap.rs:18) — Production stderr output, also at lines 43 and 64.
- [opensip-cli/packages/cli/src/bootstrap/last-resort-failure-net.ts](/Users/sb/code/opensip-ai/opensip-cli/packages/cli/src/bootstrap/last-resort-failure-net.ts:30) — Fatal projection contains code/message, without universal logRef.

### OP-R1-02 (P1) — Use phase-correct RequestId correlation

**Location:** PLAN.md §3.1, lines 70–78; §3.3, line 86; §4.3, line 142; §5.3, line 170; §6, line 201

**Problem:** The record and filename require runId even for pre-scope events, request refusals, doctor and provider startup. OpenSIP's invocation correlator is RequestId; ExecutionId exists only after attempt admission, and a public RunId cannot stand in for an uncommitted candidate or a request with no Run. Ephemeral analysis and metadata/doctor also cannot supply a durable RunId. Repeated requests can inspect the same committed Run, so RunId alone cannot identify one incident. The predecessor's invocation tag named runId is a different concept.

**Required plan change:** Make host-minted RequestId the universal operational correlator and logRef target. Propagate ExecutionId, PlanId, ProjectId and committed/stored RunId only in their lawful phases. Name the allocation-failure emergency case separately, since no valid RequestId exists there. Use RequestId/process identity in filenames and support selection; offer RunId as an additional committed-Run filter. Never stringify an internal candidate RunId into logs or crash records.

**Evidence:**

- [opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:76) — Invocation identity is RequestId, minted before admission and retained for refusals.
- [opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:1340) — No fabricated pre-Plan/pre-Run envelope; interrupted RunId is conditional.
- [opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md:61) — RequestId and admitted ExecutionId have distinct allocation roles.
- [opensip/crates/host/src/request.rs](/Users/sb/code/opensip-ai/opensip/crates/host/src/request.rs:15) — The metadata host already has a host-owned process-custody RequestAuthority.
- [opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:174) — CommitUndetermined retains ExecutionId and has no RunId.

### OP-R1-03 (P1) — Make the no-source promise structural across logs, crash records, bundles and OTLP

**Location:** PLAN.md §3.4–3.5, lines 93–104; §4.2, line 136; §5.3, line 170; §6, lines 196–203

**Problem:** The plan accepts arbitrary provider fields and logs raw captured stderr, then promises that excerpts never appear. A compiler diagnostic or provider error can contain a source line, token, identifier or arbitrary secret in plain text; credentials/path regexes cannot recognize all such content. Redacting the archive afterward does not undo the earlier disk/ring-buffer exposure. A generic total encoder may call arbitrary Debug/Display implementations. Exporting existing spans also exports their attributes unless a separate export policy filters them. The existing DR-114 contract explicitly distinguishes structural secret exclusion from best-effort free-text scrubbing.

**Required plan change:** Define a closed, typed, byte-bounded safe event vocabulary and enforce secret/source exclusion before records enter a queue, crash ring, file or exporter, with the common sink redactor as a final guard. Do not persist or export raw provider stderr under the no-excerpts guarantee; retain safe codes/counts or an explicitly separately consented restricted artifact with an honest disclosure. Specify safe backtrace/config fields, distinguish resolved secret values from allowed handles, and give bundles/OTLP their own allowlisted subsets. Add proposed privacy controls using novel secrets and source snippets in stderr, arbitrary fields, panic/error messages and nested data.

**Evidence:**

- [opensip_arch/docs/v2/architecture/03-configuration-and-security.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/architecture/03-configuration-and-security.md:45) — Resolved configuration secret values are excluded; arbitrary source is not classified by handle terminology.
- [opensip_arch/docs/coop/artifacts/doctor-contract.v4.json](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/artifacts/doctor-contract.v4.json:1012) — Construction guarantees versus best-effort free-text disclosure.
- [opensip_arch/docs/coop/artifacts/doctor-contract.v4.json](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/artifacts/doctor-contract.v4.json:1058) — Raw exception objects are excluded; terminal safety requires ANSI handling before control stripping.
- [opensip_arch/docs/coop/artifacts/doctor-contract.v4.json](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/artifacts/doctor-contract.v4.json:1086) — Every projection consumes already-redacted report data.

### OP-R1-04 (P1) — Name a custody owner for log creation and retention

**Location:** PLAN.md §3.1, lines 72–75; §3.3, lines 86–89; §5.3, lines 170–172; §9 O2/O8

**Problem:** An always-on installation file for every host command conflicts with the accepted no-installation-read/no-write metadata boundary and X10 doctor's observation-only, no-durable-write path. Buffering cannot authorize a later installation write or create an absent installation. A provider's own file in installation state also conflicts with the SDK's absence of raw host filesystem capabilities. Mode bits 0700/0600 alone do not establish the M2 account/ACL, descriptor, no-follow, filesystem and charged-operation custody predicates. Pruning is a mutation requiring authority too.

**Required plan change:** Add a named installation/security/log-storage successor in §9 before enabling installation logging. Define which admitted write capability creates, opens, rotates and deletes logs, with original-owner custody checks and bounded charged work. Keep metadata and observation-only commands on an explicitly nonpersistent sink unless their exact laws are separately succeeded. Do not initialize or repair an installation to log a refusal. Use host-owned files for provider events, or specify an independently reviewed brokered write capability; never hand providers raw installation paths.

**Evidence:**

- [opensip_arch/docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md:91) — Observation and durable/write capabilities are distinct; metadata has the stronger boundary.
- [opensip_arch/docs/implementation/m2/read-cli-x10/PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/read-cli-x10/PROPOSAL.md:28) — Doctor never creates and writes nothing durable.
- [opensip_arch/docs/implementation/m2/read-premise-458c/PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/read-premise-458c/PROPOSAL.md:21) — Read path has no creation effect; operational/private descendants do not borrow the ancestor ACL-omission premise.
- [opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md:535) — Provider effects are typed and brokered; no raw scratch path is handed out.
- [opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md:581) — No public raw filesystem/network/process capability in the SDK.
- [opensip/apps/cli/src/bootstrap.rs](/Users/sb/code/opensip-ai/opensip/apps/cli/src/bootstrap.rs:8) — Current metadata/doctor ingress explicitly writes nothing durably.

### OP-R1-05 (P1) — Treat diagnostic and progress frames as common-control successors

**Location:** PLAN.md §3.5, lines 99–106; §5.1, line 150; §8, line 221; §9 O1/O8

**Problem:** O1 treats the M3 provider-protocol law as the place to add diagnostic/progress frames, but the common control contract is already closed to sixteen message types and independently negotiated from provider subprotocols. The selected SDK explicitly says no generic progress frame is introduced and derives progress from admitted stage/counter observations. A new provider subprotocol cannot silently add messages to control major 1. The plan also leaves whether arbitrary counters constitute meaningful progress undefined; a spinning or blocked worker can emit counters indefinitely.

**Required plan change:** Keep O1 before the M3 protocol law, but name the DR-102 common-control schema/framing/state/compatibility successor and DR-125 SDK join in §9, alongside the affected TS/Rust protocol joins and G20/G21 controls. Decide whether safe diagnostics/progress can use existing observations or require an independently negotiated extension/major change. Specify direction/state windows, bounds, overflow/refusal fates and old-peer behavior. Bind progress to admitted work units/phases, with defined legitimate long-phase behavior and an independent deadline; counter traffic alone is not progress evidence.

**Evidence:**

- [opensip_arch/docs/coop/completion/control-completion.contract.v5.md](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/completion/control-completion.contract.v5.md:9) — Sixteen common-control types; unknown fields/schema violations refuse.
- [opensip_arch/docs/coop/completion/control-completion.contract.v5.md](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/completion/control-completion.contract.v5.md:24) — Control frame limits and negotiation are already specified.
- [opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md:556) — SDK aliases are not new wire tokens; no generic progress frame.
- [opensip/schemas/sources/control-v3.schema.json](/Users/sb/code/opensip-ai/opensip/schemas/sources/control-v3.schema.json) — Selected closed oneOf enumerates hello through shutdownAck, with no diagnostic/progress member.
- [opensip_arch/docs/coop/design-corrections/qualification-gates.applied.v1.json](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/qualification-gates.applied.v1.json:423) — Current G21 requires containment across the named hostile corpus and selected population.

### OP-R1-06 (P2) — Name the configuration and public-output contract changes

**Location:** PLAN.md §3.1, line 78; §3.2, line 82; §4.1, line 122; §4.3, line 142; §5.2, lines 161–164; §9 O3/O8

**Problem:** Routing new logging/retention/limit fields through the existing resolver does not make them admitted configuration. Product configuration is closed and currently has no logging section; SDK operability fields require host-reviewed mappings. Termination and domain-detail objects are also closed and admit neither logRef nor logWriteFailures. The current envelope's diagnostics carrier is bounded text, not an arbitrary object for structured timing/counter fields. O8 names SDK and doctor successors but omits these configuration, command/flag and output joins.

**Required plan change:** Extend §9 with named configuration-schema/resolution/provenance and command-inventory/output successors, owned by their existing authorities. Specify exact lawful carriers for correlation, write-loss counts and timings, reusing existing bounded diagnostics where sufficient. Any new member requires its closed schema, generated bindings and renderer-parity join; do not decorate D9 terminations ad hoc. Classify purely operational settings as nonsemantic while preserving declared semantic resource/work-budget inputs and existing protocol constants. Add their dependencies to the M3/M4 milestones.

**Evidence:**

- [opensip_arch/docs/coop/design-corrections/foundation/product-configuration.schema.v2.json](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/foundation/product-configuration.schema.v2.json:5) — Root and sections reject unknown properties; root sections exclude logging.
- [opensip_arch/docs/v2/contracts/product-v1/admission-and-qualification.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/admission-and-qualification.md:43) — Closed configuration fields and normal admission/resolution law.
- [opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md:588) — Operability configuration fields require reviewed host-owned mapping.
- [opensip/schemas/sources/common-v4.schema.json](/Users/sb/code/opensip-ai/opensip/schemas/sources/common-v4.schema.json) — StepTermination and DomainDetail are closed without logRef/logWriteFailures.
- [opensip/schemas/sources/command-envelope-v7.schema.json](/Users/sb/code/opensip-ai/opensip/schemas/sources/command-envelope-v7.schema.json) — Closed envelope; diagnostics is an array of at most 256 BoundedText values.

### OP-R1-07 (P1) — Preserve separate outcomes for semantic exhaustion, operational faults and log loss

**Location:** PLAN.md §5.1, line 156; §5.2, lines 162–165; §5.5, lines 183–186

**Problem:** “Each [cap] hit is a typed deficiency that marks the result incomplete” collapses different legal fates. An analysis-work/candidate budget can produce incomplete Coverage, but a malformed/oversized protocol frame or a known host/provider operational fault follows its owned fault/D9 route. Losing optional log/trace records must not change semantic Coverage or a committed result. The same blanket rule can also turn a provider fault into mere incomplete analysis. Two-stage forced exit cannot erase a committed or CommitUndetermined outcome.

**Required plan change:** Add a small outcome matrix by cap/failure class and lifecycle phase: semantic exhaustion through the exact owned Coverage rule; protocol/supervision/host I/O through their existing D9 fault joins; user interruption through the cancellation/commit join; optional observability exhaustion through nonsemantic loss counters. Preserve sealed results and uncertain commit state. Name a D9/Coverage successor only for an actual proposed mapping change. Include no-clean-partial, pre/post-commit cancellation and optional-sink-loss controls in the M3 method, then qualify the expanded corpus at M6.

**Evidence:**

- [opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:1353) — Closed classes, fault causes and phase-correct interrupted RunId.
- [opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:1371) — Distinct unavailable/corrupt closure, delivery and optional export fates; after-settle is not reclassified.
- [opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:168) — After-admission Committed and CommitUndetermined outcomes stand.
- [opensip_arch/docs/coop/design-corrections/qualification-gates.applied.v1.json](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/qualification-gates.applied.v1.json:427) — G21 separately requires candidate discard, sealed-evidence preservation, Coverage and D9 goldens.

### OP-R1-08 (P1) — Bound the complete logging path, not only file size

**Location:** PLAN.md §3.1, lines 75–78; §3.3, lines 87–88; §3.5, lines 102–104; §5.2; §5.5, line 185

**Problem:** “Non-blocking writer” leaves no queue byte/count bound, record/field/depth bound, pre-scope-buffer bound or overflow/backpressure policy. An event-count limit does not bound queued bytes or provider stderr traffic. A blocking fallback or unbounded flush can defeat the proposed cancellation target; an unbounded queue can exhaust the core under a provider flood. Independent process files with pruning only at startup/rotation do not by themselves enforce a 512 MiB installation-wide ceiling, especially with concurrent active files. Logging a cap hit through the saturated sink can recursively produce more events.

**Required plan change:** Specify provisional bounded queue/buffer/record budgets, admission before allocation, a nonrecursive reserved loss marker/counter and a deliberate drop policy that never blocks control/cancellation or changes analysis results. Put a deadline on normal/cancel/export draining and distinguish graceful completion from forced termination. Define whether the total retention cap is hard or an explicitly bounded best-effort target, how concurrent writers/pruners coordinate, and how active/crash files count. Include aggregate host/process resource budgeting and proposed flood, saturation, unwritable-sink, parallel-writer and cancellation controls; measurements can tune values later.

**Evidence:**

- [opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/completion/distribution-runtime-completion.v2.md:574) — SDK owns backpressure/cancellation and cannot hide dropped messages.
- [opensip_arch/docs/coop/design-corrections/qualification-gates.applied.v1.json](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/qualification-gates.applied.v1.json:408) — G20 redaction/bounds/cancellation/resource evidence.
- [opensip_arch/docs/coop/design-corrections/qualification-gates.applied.v1.json](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/qualification-gates.applied.v1.json:428) — G21 core survival and bounded diagnostics.
- [opensip-cli/packages/cli/src/telemetry/sdk-init.ts](/Users/sb/code/opensip-ai/opensip-cli/packages/cli/src/telemetry/sdk-init.ts:249) — Predecessor has an explicit timeout race for shutdown; the new file writer needs its own bound.

### OP-R1-09 (P1) — Make panic diagnostics bounded and subordinate to M2 stopping rules

**Location:** PLAN.md §3.3, line 88; §5.3, lines 170–173; §9 O2/O8

**Problem:** Flushing the normal writer from the panic hook and promising a durable backtrace/last-N record has no failure-context design. A panic can occur while holding logger/storage locks or inside serialization; re-entering those paths can deadlock or panic again. Backtrace collection, formatting and durability work can allocate or block. An uncertain M2 commit/barrier already forbids further effects, and the plan's generic hook has no separately admitted authority for another installation write. SIGKILL, abort/OOM and power loss cannot be promised a hook-generated record. Keeping the record out of recovery decisions is correct but does not settle these effect and liveness conflicts.

**Required plan change:** Name the crash-record custody/stopping join in §9. Describe a minimal, non-reentrant, bounded best-effort crash path using already-admitted safe resources when available, without logger/storage lock acquisition, arbitrary formatting or unbounded flush/barrier work. Define absence/failure fallbacks and exactly which termination mechanisms can produce a record. After a latched/uncertain operation, perform only separately authorized diagnostics and permitted release work; do not retry, reconcile or manufacture a Run outcome. Propose controls for panic under logger/commit locks, nested panic, full/unwritable disk and absent installation.

**Evidence:**

- [opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:163) — Uncertain commit/barrier refuses further effects and preserves CommitUndetermined.
- [opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:196) — No reconciliation after uncertain outcome.
- [opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:213) — Panic/abort leaving finish unrun preserves recovery evidence, not cleanup success.
- [opensip-cli/packages/cli/src/bootstrap/last-resort-failure-net.ts](/Users/sb/code/opensip-ai/opensip-cli/packages/cli/src/bootstrap/last-resort-failure-net.ts:2) — Existing minimal fatal path deliberately avoids re-entering logger transports/cleanup.

### OP-R1-10 (P1) — Treat disk preflight as advisory and place it before the owned effects

**Location:** PLAN.md §5.4, line 177; §8, line 222; §9

**Problem:** A free-space sample cannot guarantee “not a mid-commit failure”: concurrent writes, quotas, allocation overhead, inode exhaustion and storage errors can still fail an admitted write. “Before a durable commit” is also too late to promise “before any durable step.” The current prepare_commit already admits/creates directories and ledger state, commits attempt custody, and publishes objects with barriers before final Run publication. The plan names no platform/storage/commit successor for the new observation, its charging/order, its unknown-space case or its refusal mapping.

**Required plan change:** Describe an advisory capacity check against the actual admitted target filesystem and conservative planned overhead, and identify the exact earliest effect boundary it precedes. Add a named platform/storage/commit successor and existing D9 mapping in §9; retain original-handle custody, budgets, reserved settlement work and lock order. Define positive insufficiency separately from an unavailable/failed observation. Preserve all actual ENOSPC/I/O/barrier/CommitUndetermined handling after a successful preflight. Add proposed controls for space consumed after the sample, quota/inode exhaustion and failure at each relevant commit stage; do not claim a reservation unless one is actually implemented and reviewed.

**Evidence:**

- [opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:128) — Existing work reservation, attempt-custody COMMIT and object barriers precede publication.
- [opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:163) — Actual uncertain commit/barrier outcomes remain authoritative.
- [opensip/crates/storage/src/commit.rs](/Users/sb/code/opensip-ai/opensip/crates/storage/src/commit.rs:364) — admit_layout can create/open durable store state.
- [opensip/crates/storage/src/commit.rs](/Users/sb/code/opensip-ai/opensip/crates/storage/src/commit.rs:450) — prepare_commit order and reservation/refusal rules.
- [opensip/crates/storage/src/commit.rs](/Users/sb/code/opensip-ai/opensip/crates/storage/src/commit.rs:564) — Final publication is a later, separately guarded transaction.

## Compatibility dispositions

| Proposal | Disposition |
|---|---|
| Installation log/crash files | Requires an admitted log-storage/custody owner and explicit read/write boundary; O2 location/defaults alone is insufficient. OP-R1-04/09. |
| Diagnostic/progress control frames | Requires the common-control and SDK successors before M3 provider protocol work; existing major-1 control is closed. OP-R1-05. |
| OTLP export | Compatible as the proposed future optional host effect once O4's explicit grant is resolved, with OP-R1-03/08's payload and liveness controls. No export is authorized by this review. |
| Disk preflight | Compatible only as advisory observation with owned ordering, charging and outcomes; a successful sample cannot suppress later I/O/uncertain-commit handling. OP-R1-10. |
| Panic hook versus M2 recovery | The proposed separation from recovery authority is correct. Record creation/flush still needs bounded, independently lawful stopping behavior. OP-R1-09. |
| Doctor support bundle | O8 already names a DR-114 successor. Specify consented output effects and safe content without changing the default doctor's no-write/no-execution/no-egress behavior. OP-NB-04. |
| New settings, flags and public fields | Requires explicit configuration/inventory/projection joins or identified existing legal carriers; no ad hoc D9 fields. OP-R1-06. |

## Predecessor spot-checks

These checks establish source behavior/patterns at the pinned HEAD; they do not establish runtime reliability or exhaustive coverage of every §2 claim.

| Plan lesson | Static evidence and conclusion |
|---|---|
| K1 error catalog | `docs/public/70-reference/18-error-code-index.md:16` reports 252 registered definitions and generated documentation. `packages/core/src/lib/failure-envelope.ts:83–98` has a bounded normalizer and an emergency fallback catch. Corroborated as code/design, not execution evidence. |
| K2 supervision / F8 heartbeat | `packages/core/src/runtime/fork-and-settle.ts` has deadlines, RSS/payload limits, stderr capture, tree termination and a single-settle latch. TERM→KILL is visible at 171–184. The heartbeat tracks receipt/liveness rather than admitted work progress. Options/custom environment builders mean the primitive's existence is not proof that every caller uses identical bounds. |
| K3 correlation | The helper propagates `OPENSIP_RUN_ID` when context has an ID (90–105); scoped logger correlation is visible in `packages/core/src/lib/logger.ts:236–246`. Universal error correlation is not proved: the last-resort fatal path has no logRef. Preserve the invocation-correlation pattern using OpenSIP RequestId. |
| F2/F3/F10 logging | `packages/core/src/lib/logger.ts:201–214` chooses the UTC filename during setup; 283–289 uses synchronous JSON append and silently catches failure; 300 onward prunes by date. This supports the fixed-date, serialization/write-loss and missing size-pressure concerns. |
| K6/F11 telemetry | `packages/cli/src/telemetry/sdk-init.ts:141–150` gates initialization through `OTEL_EXPORTER_OTLP_ENDPOINT`; 249–276 races shutdown against a timeout. The bounded optional-export pattern is useful; its environment configuration is not inherited into the new resolver contract. |
| K7 cancellation | `packages/cli/src/bootstrap/interrupt-abort.ts` logs first/forced edges, uses a 2000 ms grace, and projects POSIX 130/143. OpenSIP must retain its own D9/custody joins. |
| F5 fatal failures | `packages/cli/src/bootstrap/last-resort-failure-net.ts:22–53` writes a minimal coded stderr line and force-exits without re-entering logger transports. No durable fatal-record write exists in that path. |
| F7 weaker fallback | `packages/core/src/runtime/subprocess-transport.ts:265–291` explicitly falls back to in-process work after a fork failure with a logger warning. This is a specific helper, not a claim about all subprocess dispatch. |
| F9 lease complexity / survey count | `packages/core/src/lib/runtime-lease.ts` is 7,584 lines. The named ADR markdown pattern has 181 files. The line count is confirmed; neither it nor this static review proves crash qualification. |

## Nonblocking observations

- **OP-NB-01.** The milestone direction is sound: decide O1/O7 before M3 protocol work; implement operational infrastructure with M3; complete public renderer/log-query joins at M4; defer optional bundle/export/resident features to M5; perform release qualification at M6. Label M3 timings as internal-harness instrumentation until their public CLI delivery exists. Author component privacy/failure controls with M3 rather than treating M6 as their first exercise. Bind qualification to the current product-v1 G20/G21 harnesses and selected platform population, including AL2023 only through its accepted platform successor.

- **OP-NB-02.** 64 MiB per file, 14 days and 512 MiB total are reasonable provisional local-log defaults, not measured daily-use guarantees. A ≤2 s cancellation goal is useful, but the plan currently calls it a target. Measure with instrumentation enabled on pinned medium and stress workloads; define the sampled statistic and start/end boundaries, and retain worst-case teardown/flush observations. Preserve M2 commit/cleanup truth if a hard process deadline expires. Measure log loss/overhead and support retention sufficiency before freezing defaults.

- **OP-NB-03.** OTLP is correctly off by default, configuration-selected, delayed to M5 and subject to a host egress grant. This is compatible as an optional future effect when O4 is resolved; its privacy controls are required by OP-R1-03. Keep exporter failure observational, with bounded queue/shutdown and no implicit endpoint/resource discovery or new required egress. Explicitly separate optional export from any future required-delivery export contract.

- **OP-NB-04.** The bundle is already named as a DR-114 successor in O8, so its new surface is not silently claimed as current law. The phrase “read-only … writes one archive” needs a precise input/output distinction. Define read-only operational inputs and a separately consented, bounded output write to a selected destination; do not alter project, trust, recovery or installation metadata to produce it. Enumerate member/privacy classes, byte limits and redactions before writing, and exclude raw storage dumps and arbitrary log text.

- **OP-NB-05.** Rust tracing, host-owned sink redaction, generated catalogs and scoped lints are useful choices. The stated checks are incomplete enforcement by themselves: print lints do not cover direct stdio writes, std::env::var does not cover var_os/vars, and a swallow-ok comment does not establish the failure's lawful disposition. TS provider boundaries also need enforcement. Specify targeted structural checks or narrow APIs plus explicit audited exceptions for native platform/termination/output owners. Use negative controls for direct stderr, ambient environment/process paths, unregistered/dynamic events and false swallow annotations. Avoid blanket bans that force legitimate custody code into the configuration resolver.

- **OP-NB-06.** CPU-count-minus-one can yield zero on a one-CPU lane and can overcommit memory when several providers approach their individual RSS ceilings. Give automatic concurrency a positive floor and a reviewed upper bound derived from both available execution capacity and aggregate memory/work budgets. Record the observed hardware and resolved default in operational provenance; keep workload-dependent defaults out of undeclared semantic inputs.

- **OP-NB-07.** The predecessor survey's primary implementation lessons are corroborated by static code reads, not runtime qualification. The checkout contains 181 docs/decisions/ADR-*.md files, rather than the stated 184. Correct or define the ADR count, scope the in-process fallback claim to runOffThreadOrInProcess, and describe capabilities seen in code rather than empirically proven success. Do not inherit the predecessor's SIGTERM 143 into OpenSIP's closed D9 vocabulary without its own successor.

## Acceptance boundary

A revised plan can retain the framework choice, proposed local defaults, O1's early timing and the M3–M6 sequence. Resolve the ten findings by naming lawful identities/carriers, safe content and bounded failure paths, and by adding the missing successor owners/dependencies. Actual thresholds, product qualification and crash results remain future evidence; this review supplies none.
