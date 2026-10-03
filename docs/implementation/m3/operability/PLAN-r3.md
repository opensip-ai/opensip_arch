# M3 operability plan: logging, observability, resilience and support — proposal r3

2026-10-03. Claude Opus 5.5, implementation lead, at the owner's request ("draft the operability plan"). r1 (`PLAN-r1.md`, sha256 `f2005ed0…`, 19,287 bytes) was reviewed by CODEX2 (method; `reviews/codex-operability-plan-r1/`, REQUIRED-FINDINGS, 10 required and 7 non-blocking). r2 answers all 17. r2 (`PLAN-r2.md`, sha256 `a65ea9c7…`, 54,138 bytes) was reviewed by CODEX2 (`reviews/codex-operability-plan-r2/`, REQUIRED-FINDINGS): OP-R1-01 to -06 resolved, OP-R1-07 to -10 partly resolved, six new required findings OP-R2-01 to -06 and four non-blocking. r3 answers them and changes nothing else of substance. The predecessor `opensip-cli` (HEAD `83f705d8`) supplies lessons (§2). Product main is `eb0d5039`.

## Standing

**This is a plan, not law and not a contract successor.** It changes no accepted contract, schema, gate or register row. Every change it needs is named in §9 with its owning authority and is made later through its own reviewed successor; §8 orders the work behind those successors. Successor labels `S-OP-n` and every number marked *provisional* are proposals. Nothing here has been measured or run.

**Owner decisions.** O4 (OTLP export) and O7 (hostile-input confinement) are owner decisions and remain **open**. Context from the owner's decisions recorded in the accepted analysis-quality plan (AQP §11): AL2023 joins the platform population (D11), MCP is the `agent-serve` transport at M5 with LSP after the resident host (D10), and the resident host is staged to M5 (D5).

**Companion.** The analysis-quality plan (AQP, r4 accepted) makes OpenSIP *right*; this plan makes it *diagnosable and robust in daily use*. AQP INC-8 (AQP:390) places reuse provenance in this plan's §4.1 operational record, never in canonical Coverage; §4.1 keeps that.

Short names:
- **WS / IE / AQ:** `docs/v2/contracts/product-v1/{workflows-and-surfaces,identity-and-evidence,admission-and-qualification}.md`
- **REG:** `docs/v2/architecture/08-decision-and-readiness-register.md`; **F02 / F03:** `docs/v2/architecture/{02-distribution-and-components,03-configuration-and-security}.md`; **SYN:** `…/11-three-reviewer-direction-synthesis.md`; **CH13:** `…/13-evidence-workflows-and-product-contracts.md`
- **APP:** `docs/coop/completion/architecture-application.v1.json` (D-369 application); **DRC:** `docs/coop/completion/distribution-runtime-completion.v2.md`; **CC:** `docs/coop/completion/control-completion.contract.v5.md`
- **QG:** `docs/coop/design-corrections/qualification-gates.applied.v1.json`; **PCS:** `docs/coop/design-corrections/foundation/product-configuration.schema.v2.json`; **CINV:** `docs/coop/design-corrections/workflows/command-inventory.v3.json`
- **DC4:** `docs/coop/artifacts/doctor-contract.v4.json` (`df2e7175…`); **OPV10:** `docs/coop/artifacts/operability.v10.json` (`9bacbbf4…`, V1 candidate, historical)
- **X3D / OWN / X10 / P458C:** M2 owners `docs/implementation/m2/{commit-session-x3d/PROPOSAL.md, initial-root-binding-owner-selection-v1/owner.md, read-cli-x10/PROPOSAL.md, read-premise-458c/PROPOSAL.md}`
- **AQP:** `docs/implementation/m3/analysis-quality/PLAN.md`
- **NE:** `docs/v2/contracts/product-v1/native-evidence.md`; **WPC:** `docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md`; **PDR:** `docs/coop/design-corrections/public-detail-registry.v1.json`; **X7:** `docs/implementation/m2/finalization-x7/PROPOSAL.md`
- Product paths are under `opensip/`; product schemas under `opensip/schemas/sources/`; predecessor paths under `opensip-cli/`.

---

## r3 changes and review responses

r3 answers CODEX2's r2 review. Its six required findings also finish the partly resolved OP-R1-07 to -10. r2 is preserved as `PLAN-r2.md` (`a65ea9c7…`, the reviewed subject).

| Finding | Section | Change |
|---|---|---|
| OP-R2-01 discovery and output routes (completes OP-R1-07) | §5.2, §10 | The grouped "semantic cap" row is split by owning observation. Workspace-unit excess is a discovery refusal: `REQUEST.UNSATISFIABLE`, exit 2, no Run (NE:871-873). Evaluator exhaustion is indeterminate `COVERAGE.BUDGET_EXHAUSTED` on the sealed Run (WPC:140). Provider exhaustion keeps its own protocol/Coverage join. Required output failure has the delivery routes with and without a committed Run (WS:1376-1377; X7:99). `OUTPUT.RENDERER_QUOTA_EXCEEDED` is only a registered detail (PDR:656), so no route is inferred from it. Controls cover workspace rejection and required-renderer failure with a retained Run. |
| OP-R2-02 commit versus settle (completes OP-R1-07) | §5.2, §5.5, §9 S-OP-12 | The cancellation join is written by phase: before attempt admission, before FinalGate admission, with the evidence COMMIT in flight, after commit but before settle, and after settle. After FinalGate admission the commit outcome stands and X7's projections apply: Committed with the latch goes to `DELIVERY.REQUIRED_FAILED`, and CommitUndetermined to `DURABILITY.COMMIT_FAILED`, both exit 4 (X7:99-101). Neither is `interrupted`. "All map to 130" is qualified. Treating the signal as a FinalGate latch observer is new and goes to S-OP-12. |
| OP-R2-03 no elapsed bound (completes OP-R1-08) | §5.5, §10 | Withdrawn: "bounded by the commit's own budget". The work ledger counts objects, edges, bytes and records, not time (`work_ledger.rs:12-21`). A second signal inside an admitted native effect waits for it to return, and that wait has **no established wall-clock bound**. The only exit is process death, which leaves M2 recovery evidence. A time-bound mechanism is named only as a possible future successor. A stalled-native-operation control is added. |
| OP-R2-04 failed observation latches (completes OP-R1-10) | §5.4, §10 | A successful observation without a meaningful figure ("capacity unavailable") discloses and continues. A failed syscall, budget charge or custody recheck latches the attempt ledger like any failed charge (`commit_session.rs:513-516`) and stops by the existing route. It is never wrapped as "unknown" (X3D:261, 383). No law change. With OP-R2-NB-03 the check becomes a storage-owned step inside `prepare_commit`, before `admit_layout`. |
| OP-R2-05 no finite overshoot (completes OP-R1-08) | §3.3, §9 O2, §10 | The finite aggregate-overshoot claim is withdrawn. 512 MiB is a best-effort target, and each file keeps its 64 MiB hard cap. A stop rule ends persistent logging for a process when it can't reclaim a backlog past a provisional 768 MiB. That bounds each process's excess to one file, but it gives no finite aggregate bound, because nothing bounds the number of concurrent writers. The plan says so. |
| OP-R2-06 panic I/O (completes OP-R1-09) | §5.3, §10 | The hook writes stderr only through a path known not to block; otherwise it skips the write, and the coded line comes from the normal termination path after unwinding. All crash-file effects are suppressed after a latched or uncertain operation, and persistent log writes stop after an uncertain one. The "bounded" and "no deadlock" claims are narrowed to "takes no lock, allocates nothing". The residual limitation is stated: a regular-file write can block with no elapsed bound. Controls for a full stderr pipe and a stalled file are added. |
| OP-R2-NB-01 | §3.2 | Digests are classified by provenance. A fingerprint of free text is P3, so provider stderr and `fault` detail are reduced to `{bytes, truncated}` with no digest. Canary controls also check derived fingerprints. |
| OP-R2-NB-02 | §1.1, §4.2 | "Export failure is success 0" becomes "optional export failure does not change the primary termination or exit" (X7:106). WS:1378 is kept as the success-case example. |
| OP-R2-NB-03 | §5.4, §9 S-OP-8 | The preflight uses storage's own object plan inside `prepare_commit`, after the end-path reserve, binding and carrier check, and before `admit_layout`. The host keeps no second estimate. |
| OP-R2-NB-04 | §5.2 | A zero-fit case (no provider fits the memory budget) has a defined outcome under S-OP-5: a refusal before any provider starts, or an admitted lower ceiling. The floor of 1 applies only when one provider fits. |

The r2 table below is the r2 record. Its OP-R1-07 to -10 rows are completed by the rows above.

---

## r2 changes and review responses

| Finding | Section | Change |
|---|---|---|
| OP-R1-01 inventory | §1, §2 K3 | The blanket "no concrete contracts / no redaction rule" claim is replaced by a source-resolved inventory: accepted law (DR-125 and DR-114 application selectors, DRC §8 and §8.1, CC's closed control set, DC4 redaction, DR-G20/G21 `product-v1` obligations), current product behavior (production stderr in `bootstrap.rs`), gaps, and successors. K3 no longer claims universal predecessor `logRef`. |
| OP-R1-02 correlation | §3.1, §3.4, §4.3, §5.3, §6 | Host-minted `RequestId` is the universal correlator and `logRef` target. ExecutionId, PlanId, ProjectId and committed RunId appear only in their lawful phases. Allocation failure is a named emergency case. Filenames and bundle selection use RequestId; committed RunId is an extra filter. Candidate RunIds are never stringified. |
| OP-R1-03 no-source | §3.2, §4.2, §5.3, §6, §10 | Closed, typed, byte-bounded event vocabulary with privacy classes, enforced at construction before any queue, ring, file or exporter. The sink scrubber is a final guard only. Raw provider stderr and free-text fault detail are never persisted or exported (bytes, digest and truncation only). Per-sink allowlists for file, crash ring, bundle and OTLP. Canary-based privacy controls. |
| OP-R1-04 custody | §3.4, §9 S-OP-1 | Named log-storage custody successor S-OP-1 before any installation log file. Metadata and observation-only commands (doctor included) use a nonpersistent sink. No installation is created or repaired to log. Providers never get log paths; the host writes their events. |
| OP-R1-05 control frames | §3.6, §9 O1, S-OP-3/S-OP-4 | Recommendation O1(a): no new control message; diagnostics and progress use existing admitted observations (DRC:573-576; CC:33-36). O1(b), a new frame, would need the named DR-102 common-control successor S-OP-3 plus the DR-125 SDK join S-OP-4. Progress is bound to admitted stage transitions, never to provider-asserted counters; long phases are governed by the independent deadline and health liveness. |
| OP-R1-06 config and output | §3.5, §4.1, §4.3, §9 S-OP-5/S-OP-6 | Named configuration successor (PCS has no logging section) and command-inventory/output successor (CINV `sharedFlags` has no `-v`, `--log-level` or `--timings`). Correlation reuses the envelope's required `requestId`; loss counts reuse bounded `diagnostics`. Nothing is added to StepTermination or DomainDetail. Operational settings are classified `host.operability.nonsemantic`; outcome-affecting limits stay release constants or the existing semantic `analysis.budget`. |
| OP-R1-07 outcomes | §5.2 | Outcome matrix by cap or failure class and lifecycle phase: semantic exhaustion through Coverage, protocol and supervision faults through their D9 fault joins, interruption through the cancellation and commit join, observability loss through nonsemantic counters. Committed and CommitUndetermined outcomes stand. No D9 or Coverage mapping change is proposed. |
| OP-R1-08 bounds | §3.3, §10 | Provisional queue, record, field, depth, pre-scope and crash-ring budgets; admission before allocation; drop policy that never blocks; nonrecursive loss marker; drain deadlines; a bounded best-effort aggregate retention cap with stated worst-case overshoot and writer/pruner coordination. Flood, saturation, unwritable-sink, parallel-writer and cancellation controls. |
| OP-R1-09 crash path | §5.3, §9 S-OP-7 | Minimal non-reentrant crash path: no logger or storage locks, no formatting, no backtrace symbolization, one bounded write to a descriptor admitted earlier. Names which terminations can produce a record (only a Rust panic) and the fallbacks. After a latched or uncertain commit it does no further effect. Named crash-record custody and stopping join S-OP-7. |
| OP-R1-10 disk preflight | §5.4, §9 S-OP-8 | Advisory capacity observation on the admitted store handle (bytes and inodes), placed before `prepare_commit` and stated honestly as not preceding earlier session-open effects. Positive insufficiency, unknown and failed observations are distinct. All ENOSPC, I/O, barrier and CommitUndetermined handling is unchanged. Named platform/storage/commit successor S-OP-8. No reservation claimed. |
| OP-NB-01 | §4.1, §8 | M3 timings are internal harness instrumentation until S-OP-6 lands. Component privacy and failure controls are authored at M3, not first exercised at M6. Qualification binds to `harness.DR-G20/G21.product-v1` and the selected population, with AL2023 only through its DR-126 successor. |
| OP-NB-02 | §3.3, §5.5 | All defaults are labeled provisional. The cancellation goal names its statistic, start and end events and workloads, with logging enabled, and keeps worst-case observations. A hard deadline never overrides M2 commit or cleanup truth. |
| OP-NB-03 | §4.2 | OTLP export stays observational, bounded and without implicit endpoint or resource discovery; it is separated from required-delivery export. |
| OP-NB-04 | §6 | The bundle separates read-only inputs from one consented, bounded output write; member classes and byte limits are listed before writing; raw stores and free text are excluded. |
| OP-NB-05 | §7 | Narrow APIs plus structural checks with an audited exception list, covering direct stdio, `var_os`/`vars`, process spawning and TS provider code, with negative controls. Annotated swallows become a typed disposition. |
| OP-NB-06 | §5.2 | Automatic concurrency has a floor of 1 and a memory-derived ceiling; the resolved value goes in the operational record, not the Plan. |
| OP-NB-07 | §2 | ADR count corrected to 181 `docs/decisions/ADR-*.md`; the fallback claim is scoped to `runOffThreadOrInProcess`; lessons are code-read, not runtime-proven; OpenSIP maps SIGTERM to its own `interrupted` 130, never 143. |

---

## 1. What exists: law, product, gaps

r1's "concrete contracts don't exist" was wrong. Accepted law already fixes much of the SDK, control, doctor and redaction surface. What it lacks is a host logging, retention, crash-record and support-bundle law.

### 1.1 Accepted law (D-369 preview application; D-372 product contracts)

| Area | What is fixed | Source |
|---|---|---|
| DR-125 common SDK | SATISFIED under D-369: "typed reference SDK APIs and exact host-owned capability/configuration registry accepted; G20/G21 execution remains". Application row inherits `component-sdk-contract.v4.json` and selects D.SDK = DRC §8. D-372 disposition retains the SDK/control/broker contract. | REG:314, REG:434; APP:3860-3868; APP:620-628 |
| DRC §8 SDK | Concrete `ProviderSession` operations (`emitFacts`, `emitCoverage`, `reportFault`, `reportResources`, `complete`, `cancellation`). "No generic progress frame is introduced; the host derives progress from admitted stage/counter observations." Non-authoritative diagnostics may use "the existing bounded stderr channel and carry no protocol meaning". SDK owns framing, backpressure and cancellation and "never hide[s] dropped messages". No raw filesystem/network/process capability; no scratch path. Configuration classes closed to `host.analysis.semantic` and `host.operability.nonsemantic`; a new field needs a reviewed host-owned mapping. Secret handles deferred with DR-108. F02's "exact SDK APIs … remain implementation design" (F02:197) is superseded here for the preview. | DRC:513-601 (522-533, 541, 573-579, 581-585, 588-601) |
| Common control | Closed to sixteen message types (hello … shutdownAck), unknown fields refused (RF2), frame bounds 65,536 bytes pre-helloAck and ≤ 16 MiB after, free strings ≤ 1,024 UTF-8 bytes. `health`/`healthReport` (ready/busy/stopping), `resourceReport` (residentBytes, cpuNanoseconds, openHandles), `fault` (opaque detail), `cancel` (user/deadline/supervisor-fault). Selected by D-369 as C.BODIES. Product schema `control-v3.schema.json` is a closed `oneOf` of exactly these sixteen. | CC:9-15, 20-25, 29-41, 56-58; APP:1016-1021; `opensip/schemas/sources/control-v3.schema.json:5-907` |
| DR-114 doctor | SATISFIED under D-369 (modes, actor joins, bounded report, consent and outcome rules). Application inherits `doctor-actor-join-integration-contract.v8.json`; its ID-DEP selectors pin DC4. DRC §8.1: core mode reads no project; neither mode loads component code or executes a provider. | REG:303, REG:424; APP:2832-2840, APP:7569-7575; DRC:603-610 |
| DC4 redaction | Two tiers: a structural GUARANTEE for host-constructed members over classified sources (secret value never present, handle plus presence only) and a best-effort DISCLOSURE tier for free text (pattern scrub, ANSI then C0 stripping, length bounds). Raw error objects never present. No secret previews. Express exclusions include analyzed source text and arbitrary high-entropy strings. Every projection consumes the already-redacted report. | DC4:1005-1086 (1012-1028, 1058-1065, 1070, 1074, 1086) |
| Secret scope | Resolved configuration secret values are excluded from PlanId, digests, diagnostics and support bundles; the rule "does not classify arbitrary analyzed source text as a configuration secret". | F03:47-58 |
| Invocation identity | `RequestId` (`req1_` + 32 hex) minted before admission, retained for refusal and success; fresh `ExecutionId` per admitted attempt; only `analysis` and `verify` seal a Run. | WS:76-84; IE:61-63 |
| Outcomes | Exit table 0/1/2/3/4/130; termination branch contract; `interrupted` carries `signal` (SIGINT/SIGTERM/SIGHUP) and a RunId only when a Run committed first; optional export failure does not change the primary termination (success 0 in the WS:1378 golden; X7:106); after-settle is never reclassified; no new D9 family. No run envelope is fabricated before a Plan or Run exists. | WS:1340-1346, 1355-1366, 1376-1378, 1393-1397; `common-v4.schema.json:280` (D9Signal) |
| Envelope carriers | `command-envelope-v7` is closed and *requires* `requestId`; `diagnostics` is ≤ 256 `BoundedText` (≤ 1,024 chars). `StepTermination` and `DomainDetail` are closed and carry no `logRef` or loss field. | `command-envelope-v7.schema.json:12, 35, 143`; `common-v4.schema.json:132, 641, 750` |
| Configuration | Closed PCS root: `schemaVersion, analysis, components, discovery, policy, evidence, retention, ui`, every section `additionalProperties: false`; no logging or operability section. `retention` governs the store, not logs. | PCS:1-6; AQ:43-53 |
| Commands and flags | CINV is the single closed inventory; `sharedFlags` has no `-v`, `--log-level` or `--timings`. | WS:1088-1093; CINV:1634 |
| Offline and egress | No implicit telemetry or required egress in ordinary analysis; optional export cannot change a verdict. No hidden environment input. | AQ:346; WS:1378; CH13:59-62 |
| DR-G20 / DR-G21 | Current harnesses `harness.DR-G20.product-v1` (owner Component architecture + CLI/operability; current contract WS) and `harness.DR-G21.product-v1` (owner Supervisor + protocol + operability; current contract AQ). G20 requires envelope/diagnostic parity, redaction/bounds/audit correlation, broker/cancellation/resource behavior, no unstructured logs. G21 requires core survival, kill/reap/cleanup, candidate discard, sealed-evidence preservation, bounded redacted diagnostics, Coverage/D9/UI/exit goldens, and "does not claim security confinement". Both DESIGN-CONTRACT-ACCEPTED, unqualified, harness unauthored. | QG:403-421, 423-441; REG:365-366 |
| M2 custody | Observation-only and durable/write capabilities are distinct; metadata commands keep a stronger no-installation-read boundary. Doctor is `Outside`, never creates, writes nothing durable. The read premise never applies to operational files or private descendants. Uncertain commit or barrier refuses every further effect; no reconciliation after uncertainty; panic or abort leaves recovery evidence. | OWN:91-95; X10:32-34; P458C:21-31; X3D:163, 196, 213 |
| Historical | OPV10 (V1 candidate, not applied; cited by REG:311 for projections) already states phase-correct correlation ("No event fabricates an identity for a lifecycle phase in which it does not exist"), phase-derived budget ownership, captured-but-never-parsed producer output, and RequestId as support-bundle correlation metadata. It informs this plan; it grants nothing. | OPV10:65-104, 178-191, 257 |

### 1.2 The product today (`eb0d5039`)

- **Stderr.** Production writes exist: `apps/cli/src/bootstrap.rs:18-21` (request-identity allocation failure, exit 4), `:43-46` (required metadata projection failed) and `:64-67` (output emission failed). Each is a fixed coded line. All other `eprintln!` sites are test-only (`crates/security/src/lib.rs:267` gates the census module).
- **Correlation.** `crates/host/src/request.rs:15-55` has a host-owned, process-custody `RequestAuthority` that mints `req1_` identifiers for the explicitly nonpersistent metadata host; durable host audit belongs to the writing ingress (X10:34).
- **No logging framework** (no `tracing` dependency), no panic hook (default unwind), no log or crash files, no capacity check.
- **Commit.** `crates/storage/src/commit.rs:370` (`admit_layout` creates or opens store state), `:449-468` (`prepare_commit` order: reserve, binding, capacity, layout, attempt admission, objects with barriers), `:571` (`publish`).

### 1.3 Genuine gaps (no law yet)

Host log format, levels, sinks and file layout; log storage custody and retention; crash records; the safe event vocabulary; public verbosity and timing switches; disk-capacity observation; the support bundle; cancellation latency. SYN:258-266 also lists resource/overload semantics, disk pressure, support without telemetry, source privacy in bundles and dumps, and hostile-input confinement; SYN is steering advice, not register law.

### 1.4 Proposed successors

Named in §9: S-OP-1 log storage custody; S-OP-2 safe event vocabulary and sink law; S-OP-3 common-control (only under O1(b)); S-OP-4 SDK join; S-OP-5 configuration; S-OP-6 command inventory and output; S-OP-7 crash record; S-OP-8 capacity preflight; S-OP-9 doctor log query and bundle; S-OP-10 OTLP export; S-OP-11 G20/G21 harness authoring; S-OP-12 cancellation and commit join.

---

## 2. Lessons from opensip-cli

A static read of `opensip-cli` at `83f705d8` (181 `docs/decisions/ADR-*.md` files; r1's "184" was wrong). These are capabilities seen in code, not runtime-proven reliability.

**Keep:**
- **K1. Error catalog.** 252 coded definitions with orthogonal axes and generated documentation (`docs/public/70-reference/18-error-code-index.md:16`); a `normalizeFailure` with an emergency fallback (`packages/core/src/lib/failure-envelope.ts:83-98`). OpenSIP's D9 codes and DomainDetail remedies are the analogue; generate docs from code.
- **K2. One supervision primitive.** `packages/core/src/runtime/fork-and-settle.ts`: deadline, RSS and payload caps, bounded stderr, TERM→KILL tree kill (`:160-184`), single settlement. Callers can still vary bounds, so the primitive's existence does not prove uniform use.
- **K3. Invocation correlation.** A run-scoped id is propagated to children (`fork-and-settle.ts:104`, `OPENSIP_RUN_ID`) and bound into scoped log records (`packages/core/src/lib/logger.ts:236-246`); diagnostics may carry `logRef` (`packages/cli/src/bootstrap/report-failure.ts:105-114`). **Not universal:** the last-resort fatal path writes code and message only (`packages/cli/src/bootstrap/last-resort-failure-net.ts:30-41`). The predecessor's `runId` is an invocation tag; OpenSIP's equivalent is `RequestId`, not RunId (§3.1).
- **K4. Honest degradation.** Visible truncation; setup faults never produce a findings envelope.
- **K5. Conventions enforced by tooling.**
- **K6. Telemetry that can't hurt a run.** Opt-in; shutdown raced against a timeout (`packages/cli/src/telemetry/sdk-init.ts:249-276`). Its environment configuration (`:141-150`, `OTEL_EXPORTER_OTLP_ENDPOINT`) is not inherited.
- **K7. Two-stage cancellation.** `packages/cli/src/bootstrap/interrupt-abort.ts:21` (2,000 ms window), both edges logged. Its POSIX 130/143 projection (`:50`) is **not** inherited: OpenSIP's `interrupted` is 130 for SIGINT, SIGTERM and SIGHUP (WS:1355; D9Signal).
- **K8. A minimal fatal path.** The last-resort net deliberately avoids re-entering logger transports and cleanup (`last-resort-failure-net.ts:2-9`). §5.3 adopts that shape.

**Fix:**
- **F1.** Log docs drifted from code.
- **F2. Fragile log file.** The UTC filename is fixed at setup (`logger.ts:201-214`); synchronous append with a silent catch (`:283-289`); date-only pruning; no size cap; shared file across processes.
- **F3.** Binary `--debug`.
- **F4.** Four divergent redaction regex sets, none at the sink.
- **F5.** No durable fatal record (`last-resort-failure-net.ts:22-53`).
- **F6.** No support bundle or runbook.
- **F7.** `runOffThreadOrInProcess` falls back to in-process work after a fork failure with only a logger warning (`packages/core/src/runtime/subprocess-transport.ts:272-291`). This is that helper, not all subprocess dispatch.
- **F8.** Heartbeats tracked receipt liveness, not admitted work.
- **F9.** `packages/core/src/lib/runtime-lease.ts` is 7,584 lines; M2's lease and crash-matrix law replaces it.
- **F10.** No disk-space check.
- **F11.** Telemetry and limits configured by environment variable; forbidden here (CH13:59-62).

---

## 3. Logging

### 3.1 Model and correlation identities (OP-R1-02)

- **Framework (proposed, unchosen by law):** Rust `tracing` with one host-owned subscriber stack. Events are emitted only through the typed vocabulary of §3.2.
- **Universal correlator: `RequestId`**, from the host's `RequestAuthority` (`request.rs:15-55`). Every record, crash record and bundle selection keys on it. It is opaque and carries no timestamp, path or user (OPV10:257).
- **Phase-lawful identities.** A field appears only when the identity exists:

| Identity | Lawful from | Never |
|---|---|---|
| `RequestId` | allocation, before parsing or admission (WS:78) | supplied by a caller; `clientCorrelationId` stays separate untrusted metadata (OPV10:191) |
| `ProjectId` | project admission | before admission, or for metadata/doctor core mode |
| `PlanId` | Plan sealing | before |
| `ExecutionId` | attempt admission (IE:61-63) | before; it is kept for CommitUndetermined (X3D:130-132, 176) |
| `RunId` | `Committed` publish, or a stored-Run read | for a candidate, an uncommitted or undetermined attempt, or an ephemeral analysis |

  An internal candidate RunId is never stringified into any record, crash record or diagnostic. A request that reads a committed Run (`query`, `inspect`) logs the RunId as a read subject; two such requests stay distinct incidents by RequestId.
- **Emergency case.** When `RequestAuthority::begin` fails (`EntropyUnavailable` or `CollisionExhausted`), no valid RequestId exists. The existing fixed line `HOST.IO_FAILURE: request identity allocation failed.` (`bootstrap.rs:18-21`) stays the only output: no record, no file, no crash record.
- **Record shape:** `{ts, level, event, requestId, [projectId], [planId], [executionId], [runId], [component], [phase], fields}`; `event` is a registered `domain.component.action` name (§3.2).
- **Levels:** `error`, `warn`, `info`, `debug`, `trace`, with per-target filters (F3). File default `info`; stderr off unless asked (§3.5).

### 3.2 Safe event vocabulary and privacy (OP-R1-03; S-OP-2)

The guarantee is structural, at construction, not at the sink. This follows DC4's split: a guarantee only over host-constructed members, best-effort scrubbing for anything else (DC4:1012-1028).

- **Closed vocabulary.** Every event name is registered with a typed field schema. Field types are limited to a sealed `SafeField` set: closed enum codes (D9 codes, DomainDetail codes, provider-subprotocol reason enums), integers, durations, byte counts, digests classified by provenance (a digest of a content-addressed identity or closure is P1; a digest of free text or source is a fingerprint of private content and is P3, so it is not loggable), the identities of §3.1, versions, platform IDs, rule IDs, and project-relative paths with line numbers. No `Debug` or `Display` of arbitrary values; no error objects (DC4:1058), only an error code and a closed error-kind enum. A non-safe value fails to compile. r1's "total encoder with typed placeholders" is replaced by this compile-time closure.
- **Privacy classes:** **P0** codes, counts, durations, versions, platform; **P1** correlation identities; **P2** project structure (relative paths, line numbers, rule IDs, file and directory names, which may themselves be sensitive, DC4:1074); **P3** free text and source bytes. P3 has no `SafeField` type and cannot be logged.
- **Secrets.** A resolved secret value is a type with no `SafeField`, `Debug` or `Display` implementation; a test proves it. A handle name (when DR-108 lands) is P2. Environment variables appear only by declared name, never value.
- **Provider output.** Raw provider stderr is captured up to the negotiated bound (`handshake-v1.schema.json:281-282`, `maxStderrBytes` 262,144), held in memory, and reduced at settle to `{bytes, truncated}`. Test execution's `{bytes, digest}` shape (`test-execution-v1.schema.json:340-348`) is a representation precedent, not a logging permission; its digest of free text would be P3 here. Its text is never written to a log, crash ring, bundle or exporter. The control `fault` detail (CC:36, ≤ 1,024 bytes) is treated the same: length only. Providers that need a diagnosable reason use the provider-subprotocol's closed reason enums, which are P0. A separately consented restricted capture is O9.
- **Per-sink allowlists:**

| Sink | Classes |
|---|---|
| file (S-OP-1) | P0–P2 |
| stderr (human) | P0–P2 |
| crash ring (§5.3) | P0–P1, plus the phase and event name |
| support bundle (§6) | P0–P1 by default; P2 only with the bundle's explicit consent |
| OTLP export (§4.2) | P0 only, plus an export-local trace ID; no RequestId, path or rule ID unless S-OP-10 admits one |

- **Final guard.** One scrubber at every sink: ANSI first, then C0 controls (DC4:1062-1065), length bound with a truncation marker, known credential shapes. It is a DISCLOSURE-tier backstop; the guarantee is the vocabulary.
- **Panic payloads** are never recorded (§5.3).

### 3.3 Bounds on the whole path (OP-R1-08)

All numbers are provisional, to be tuned by the overhead and loss measurements in §10.

| Bound | Provisional value | Behavior at the bound |
|---|---|---|
| encoded record | 4 KiB; ≤ 32 fields; depth ≤ 2; string field ≤ 256 bytes | refused at construction; one `log.record_refused` count |
| in-process queue | 2 MiB and 4,096 records, whichever first | space is reserved before encoding (admission before allocation); when full, the new record is dropped and counted by level |
| pre-scope buffer | 64 KiB / 256 records | drop-newest, counted |
| crash ring | 64 KiB preallocated, ≤ 256 records | overwrite oldest |
| per file | 64 MiB hard | rotate before exceeding |
| total retained | 512 MiB target | see retention below |
| drain on normal exit | 200 ms | abandon, count, exit unchanged |
| drain on cancellation | 100 ms, inside the §5.5 goal | as above |
| export shutdown (M5) | 1 s | as above |

- **Never blocks.** Producers never wait on the writer. Control-plane, supervision and cancellation paths emit only through non-blocking enqueue; a full queue drops.
- **Nonrecursive loss marker.** Loss counters are atomics, one per reason and level. They are written once at drain as a single reserved `log.loss` record that bypasses the queue, through a preallocated slot. A cap hit never emits through the saturated path.
- **Visibility.** If any record was lost, the envelope's existing `diagnostics` (`BoundedText`) gets one line, e.g. `operational log incomplete: 412 records dropped (queue full)`, where the command produces an envelope. Loss never changes Coverage, termination, exit or a committed Run (§5.2).
- **Retention (r3).** 512 MiB is a **best-effort target. No finite aggregate bound is claimed.** Each file has a real 64 MiB hard cap, and age retention is 14 days. Pruning runs at writer start and on rotation, under a non-waiting try-lock on a log-directory lock (S-OP-1). It deletes only closed files, oldest first; an active file is held by its writer's advisory lock. Active and crash files count toward the total.
- **Stop rule.** Before opening any new log or crash file, at start or on rotation, the writer measures the retained total by listing the directory under S-OP-1. Suppose the total exceeds the provisional backlog threshold of 768 MiB (target plus 256 MiB), and the writer's own prune pass cannot bring it below that because the lock is busy, a deletion fails or the listing fails. Then the writer opens no new file: persistent logging stops for the rest of that process. Records go to the nonpersistent ring and count as dropped, and one `diagnostics` line discloses the stop. If a pruner is killed, process death releases its lock; the next writer re-evaluates, and a half-finished pass leaves only closed files to retry.
- **What the stop rule bounds.** The check precedes every open, so one process holds at most one log file (≤ 64 MiB) and one crash file (≤ 64 KiB) beyond the threshold. Writers check concurrently, though, and nothing in this plan bounds how many host processes run at once. The aggregate is therefore at most 768 MiB plus about 64 MiB per writer that passed its check at the same time, and that is **not a finite bound in general**. Optional loss never changes an outcome (§5.2).
- **Aggregate.** Logging memory is about 2.2 MiB per host process (queue, ring, pre-scope buffer), counted inside the host's RSS budget.

### 3.4 Sinks and custody (OP-R1-04; S-OP-1)

No log file is written until S-OP-1 is accepted. S-OP-1 decides which admitted write capability creates, opens, rotates and prunes log files, under original-owner custody: account and ACL predicates, retained descriptors, no-follow opens, filesystem identity, charged bounded work. Mode bits alone are not custody. Logs are operational metadata under DR-124's state-class separation (REG:433): never evidence, never authority, never read by recovery.

| Command class | Sink | Why |
|---|---|---|
| metadata (`--version`, `help` …) | nonpersistent: stderr only if requested; ring discarded at exit | no installation read (OWN:95; P458C:23) |
| doctor and observation-only surfaces | nonpersistent | doctor writes nothing durable (X10:32-34); the observation path admits no write (OWN:95) |
| commands holding an admitted durable/write capability | host-owned file, under S-OP-1 | the same invocation already holds write authority |
| requests refused before admission | nonpersistent | an installation is never created, initialized or repaired to log a refusal |

- **Pre-scope events** stay in the §3.3 pre-scope buffer. They are flushed to a file only if the same invocation later holds S-OP-1's write capability; otherwise they are discarded at exit, and the count is disclosed if an envelope exists.
- **Layout (proposed, inside S-OP-1's root):** `logs/<UTC date at open>/<requestId>-<pid>-<role>.jsonl`, where `role` is `host` or a host-assigned component slot. A date change rotates at write time (F2).
- **Providers never get a log path** (DRC:541, 581-583). The host writes every provider-attributed record into its own file.

### 3.5 Configuration and switches (OP-R1-06; S-OP-5, S-OP-6)

- **Configuration.** PCS is closed and has no logging section (PCS:5, root `additionalProperties: false`). Routing new fields "through the resolver" does not admit them. S-OP-5 proposes an `operability` section (`log.level`, `log.retentionDays`, `log.retentionBytes`, `concurrency`), each mapped by the host and classified `host.operability.nonsemantic` (DRC:588-601), with provenance through the existing resolver. The existing `retention` section governs the store and is not overloaded. No environment side channel (CH13:59-62).
- **What stays out of user configuration.** Settings that can change a result are not nonsemantic. Per-provider deadline, RSS ceiling and frame bounds stay release constants and existing protocol constants (CC:24); semantic work budgets stay in `analysis.budget` (PCS `analysis.budget`). Changing them is a release or semantic-input change, not an operability setting.
- **Switches.** CINV `sharedFlags` (CINV:1634) has none of `-v`, `-vv`, `--log-level <filter>` or `--timings`. S-OP-6 adds them with grammar, owners and golden reachability (WS:1091-1093). Until it lands, the stderr sink and timings exist only in development and harness builds.

### 3.6 Provider diagnostics and liveness (OP-R1-05; O1)

Common control is closed at sixteen messages (CC:11; `control-v3.schema.json`), and DRC §8 deliberately adds no progress frame (DRC:573-576). A provider subprotocol cannot add control messages under control major 1.

**O1, recommendation (a): no new message.**
- **Diagnostics.** Providers report through what exists: the provider-subprotocol's closed responses (`UnavailableV1`, `BudgetExhaustedV1` …; DRC:556-568) carry P0 reason codes; `fault` and stderr are reduced to length and truncation (§3.2). The host emits the records.
- **Progress** is host-derived from **admitted** stage transitions and admitted message counts: accepted `FactBatchV1` and `CoverageV1` per universe, snapshot chunks acknowledged, stage changes. Provider-asserted counters are not progress evidence, and counter traffic alone proves nothing.
- **Liveness** uses existing `health`/`healthReport` (nonce-matched; CC:33-34, 50-54) and `resourceReport` (CC:35) inside their state windows. A missed health response within the provisional 5 s window is a liveness fault.
- **Long phases.** A legitimate long phase (whole-program type checking before the first `FactBatchV1`) emits no progress. Absence of progress is logged as `supervision.no_progress` at intervals, never as a fault. Only the independent wall-clock deadline, a liveness failure, a resource breach or a protocol violation is a fault (§5.1).

**O1(b), if chosen instead**, a typed diagnostic or progress frame, requires before the M3 protocol law: S-OP-3, a DR-102 common-control successor (schema, framing, direction and state windows, per-frame and per-run bounds, overflow and refusal fates, negotiation and old-peer behavior: an independently negotiated extension or a control major 2, with DR-127 skew rules); S-OP-4, the DR-125 SDK join; the TS major 2 and Rust major 3 protocol joins (REG:413); and G20/G21 control additions. Under (a), S-OP-4 is still needed as a record join stating the stderr and fault-detail disposition and the progress derivation.

---

## 4. Observability

### 4.1 Timings, phases and the operational record

- **Phase spans:** discovery, snapshot and sealing, plan, each provider (start, analysis, teardown), admission and replay, evaluation, commit, delivery, plus cache and reuse decisions. These are AQP's phase timings (AQP:340); one mechanism serves both plans.
- **The operational record.** A host-owned, typed, nonsemantic record keyed by RequestId and, once admitted, ExecutionId. It holds phase timings (wall, CPU, peak RSS per process), resolved operational settings and observed hardware (§5.2), loss counters (§3.3), and the **reuse disclosure** required by AQP INC-8: which results were recomputed and which were reused producer work. It is outside Run identity, Coverage, PlanId and every digest, like OPV10's non-semantic attempt link (OPV10:257). Canonical Coverage never carries reuse provenance (AQP:390).
- **Carriers by milestone.** At M3 the record goes to the log file (S-OP-1) and the AQP exploratory envelope (AQP:417-425): internal harness instrumentation, not a public surface (OP-NB-01). At M4, `--timings` and a public reuse disclosure need S-OP-6: either lines in the existing bounded `diagnostics`, or a new closed envelope member with schema, generated bindings and renderer parity. No field is added to StepTermination or DomainDetail.
- **Cost.** Monotonic clock only; nothing touches identity or evidence. A no-op sink cannot change results (OPV10:79); a control runs with logging off and on and compares results.

### 4.2 Optional OTLP export (M5; O4, owner, open)

- Off by default. Enabled only by explicit configuration naming an endpoint, plus the host egress grant. No endpoint or resource discovery, no `OTEL_*` environment input (F11).
- **Payload.** A separate export allowlist: P0 metrics and span names and durations; no RequestId, path, rule ID or free text unless S-OP-10 admits them. Metrics: command duration, phase durations, provider faults by class, finding and indeterminate counts by rule *category*, cache reuse ratio.
- **Failure is observational.** A bounded queue (provisional 1 MiB), a 1 s shutdown, drop with a count. Export failure does not change the primary termination or exit, whatever its class (X7:106; WS:1378 is the success-case golden), and never changes a verdict.
- **Not required delivery.** Optional export is distinct from any future required-delivery export contract (AQ:346).
- **Purpose.** Fleet trend tracking of speed and indeterminate rates.

### 4.3 Correlation surfaces

- **JSON and agent output** already carry the required envelope `requestId` (`command-envelope-v7.schema.json:12, 35`). That is the `logRef`; no new field.
- **Human output** prints one `request req1_…` line on every non-success termination, and on success under `-v`. This is a renderer join in S-OP-6 at M4 with parity goldens.
- **Doctor log query** ("records for request R" or "for committed Run X") reads operational files, which the read premise excludes (P458C:31). It needs S-OP-9 (DR-114 successor) and S-OP-1's read rules. M4.

---

## 5. Resilience

### 5.1 Supervision (K2, F8; extends DR-G21's corpus at M3)

One supervision primitive for every component process: the wall-clock deadline; liveness by health ping (§3.6); RSS ceiling from `resourceReport` and OS observation; frame bounds enforced by the host independently (DRC:577-579); bounded stderr capture; process-tree kill TERM→KILL (provisional 1 s escalation, 10 s hard ceiling for reaping, as OPV10:1543-1544); exactly-once settlement. No restarts: providers are one-shot per semantic universe; the M5 resident host brings its own policy under AQP INC-6. No silent weaker fallback (F7).

### 5.2 Limits, concurrency and the outcome matrix (OP-R1-07)

**Concurrency (OP-NB-06).** Automatic host concurrency is `clamp(min(cpus − 1, ⌊memory budget ÷ per-provider RSS ceiling⌋), 1, 16)`, all provisional. The observed CPU and memory and the resolved value go in the operational record, never the Plan. A control checks that results are identical at concurrency 1 and at the automatic value. The memory budget is net of the host's own allowance, including logging (§3.3). **Zero fit (OP-R2-NB-04).** If no provider fits (the quotient is 0), the floor of 1 does not apply. S-OP-5 and supervision define the outcome: either a refusal before any provider starts, or an explicitly admitted lower per-provider ceiling. The clamp's floor never silently overcommits memory.

**Every failure class keeps its own route.** r1's "each cap hit is a typed deficiency that marks the result incomplete" is withdrawn.

| Class | Phase | Route (existing) | Run effect |
|---|---|---|---|
| Workspace-unit excess (> 4,096 first-party units) | discovery, before any Plan | `request-rejected`, `REQUEST.UNSATISFIABLE`, detail `PROJECT.WORKSPACE_UNIT_LIMIT`, exit 2; never truncation (NE:871-873) | no Run |
| Evaluator work budget | evaluation preflight | `indeterminate` 3, reason `COVERAGE.BUDGET_EXHAUSTED`; the sealed Run's termination carries D9 deficiency `budget-exhausted`; detail `EVALUATION.WORK_BUDGET_EXHAUSTED` (WPC:140) | Run sealed indeterminate |
| Evaluation output bound | evaluation | `operational-failed`, `OUTPUT.SERIALIZATION_FAILED`, `output-serialization`; detail `EVALUATION.OUTPUT_BOUND_EXCEEDED` (WPC:141) | per that route |
| Provider candidate or graph exhaustion | provider stage | provider `BudgetExhaustedV1` (DRC:563-565) under its exact native protocol/Coverage join; this plan infers no route | as that join fixes |
| Required projection or renderer failure, no committed Run | delivery | `operational-failed` 4, `DELIVERY.REQUIRED_FAILED`, detail `DELIVERY.REQUIRED_PROJECTION_FAILED`; no runId (WS:1377) | no Run |
| Required renderer failure after commit | delivery | `operational-failed` 4, `DELIVERY.REQUIRED_FAILED`, `delivery-required`, detail `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`; runId retained (WS:1376; X7:99) | Run retained |
| `OUTPUT.RENDERER_QUOTA_EXCEEDED` | rendering | a registered detail code only (PDR:656); its route belongs to the renderer and delivery owner, and this plan infers none from the enum | — |
| Optional output or export failure | after required delivery | disclosed on its own surface; termination unchanged (X7:106) | none |
| Malformed, oversized or out-of-window frame; RF2 | any provider stage | G21 containment, `provider-protocol` fault cause (WS:1358-1361) | candidate discarded; not "incomplete analysis" |
| Deadline, liveness failure, RSS breach, crash, unexpected exit | any provider stage | G21 containment and its Coverage/D9 mapping (F02:199-206) | candidate discarded; sealed evidence untouched |
| Host I/O failure | before commit admission | `operational-failed`, `host-io` | no Run |
| Capacity insufficient (§5.4) | inside `prepare_commit`, before `admit_layout` | a decision over a completed observation, like `CarrierCapacityExhausted` (X3D:139): `operational-failed`, `host-io`, `HOST.IO_FAILURE` detail; stop row fixed by S-OP-8 | no Run; no store effect |
| User interrupt, any phase | per §5.5 | the phase-specific join in §5.5: `interrupted` 130 only before FinalGate admission or before settle; X7's exit-4 projections after FinalGate admission; settled class after settle | per §5.5 |
| Host panic | before FinalGate admission | `operational-failed`, `host-invariant` where the termination layer is reachable after unwinding | no Run |
| Host panic | after FinalGate admission | no outcome manufactured; recovery evidence stands (X3D:213) | unchanged |
| Optional observability loss: dropped records, sink failure, export failure, crash-record failure | any | nonsemantic counters and one `diagnostics` line | none, ever |

No D9 or Coverage mapping change is proposed: every row uses an existing route, or defers to the owning join without choosing one. A dedicated capacity detail code is optional under S-OP-8.

### 5.3 Panics and crash records (OP-R1-09; S-OP-7)

- **What can produce a record.** Only a Rust panic in the host, and only best-effort. SIGKILL, the OOM killer, `abort()` from native code, stack overflow and power loss produce none. Provider crashes are recorded by the host's normal supervision path, not by this one.
- **The hook is minimal and non-reentrant**, after the predecessor's last-resort net (K8). It replaces Rust's default hook, so the default stderr print does not run.
  1. An atomic flag marks the process as crashing. A nested panic, or a panic while the flag is set, goes straight to `abort` with no further work.
  2. It takes no logger, storage, journal or ledger lock, does no formatting beyond copying preformatted bytes, allocates nothing, symbolizes no backtrace and never reads the panic payload. Its inputs are the panic location (`&'static str` file and line), plus the build version, platform ID, RequestId, ExecutionId if any, and phase code, all preformatted at admission. So it cannot deadlock on a lock the panicking code holds. That is the whole claim; there is no general no-deadlock or time-bound claim.
  3. **Stderr only when known not to block (OP-R2-06).** fd 2 is inherited and may be a full pipe, a stopped terminal or a stalled file, and a write can then block. The hook writes its fixed coded line only through a write path established at startup that cannot block: a separate open file description opened `O_NONBLOCK` on a pipe or socket, where the platform provides one without changing the inherited shared description. S-OP-7 establishes which platforms do; until it does, none qualify and the hook skips the write. The user-facing coded line normally comes from the top-level termination path after unwinding (§5.2). That is ordinary output with ordinary blocking behavior, and it is absent on a nested panic or abort.
  4. **Crash file.** The hook writes one `write(2)` of at most 64 KiB (preformatted header plus crash ring) only if two conditions hold. First, the invocation holds a crash descriptor opened owner-only, append and no-follow under S-OP-1's write capability. Second, no operation of the invocation is latched or uncertain. A process-wide atomic records that state; the session sets it when a ledger latches or an uncertain outcome is classified. There is no `fsync`, rename or barrier.
- **Residual limitation.** `O_NONBLOCK` does not make regular-file I/O nonblocking. A crash-file write to a stalled disk or network filesystem can block in the kernel, with **no elapsed bound**. The panicking thread then stalls, and the process may not exit until the write returns or the process is killed. Not claimed: a bounded hook, a guaranteed record, or freedom from kernel-level stalls.
- **Fallbacks.** No crash descriptor (metadata, doctor, observation-only, pre-admission), or a latched or uncertain operation: no crash file. A failed write (ENOSPC, EIO): nothing more.
- **After a latched or uncertain operation (OP-R2-06)**, every crash-file effect is suppressed. Already-open descriptors are no exception to X3D's stopping rules (X3D:163, 253-260). After an **uncertain** outcome, persistent log writes also stop for that invocation: records stay in the nonpersistent ring and count as dropped. After a **certain** latch, the log file is not the latched ledger's work and continues. S-OP-7 must confirm that with the X3D owner, or the same suppression applies. The hook does no retry, reconciliation, journal append or cleanup, and manufactures no Run outcome (X3D:163, 196). The top-level boundary maps an unwind to `operational-failed`/`host-invariant` only before FinalGate admission (§5.2).
- **Records** are operational state, owner-only, under S-OP-1 retention; at most 32 retained. They explain and never drive recovery.

### 5.4 Disk-capacity preflight (OP-R1-10; S-OP-8)

- **Advisory, not a guarantee.** A storage-owned, charged step (S-OP-8; OP-R2-NB-03) does one `fstatvfs` on the admitted store directory handle, under original-handle custody, and reads available bytes and inodes. It compares them with storage's own object plan: the declared object bytes that `prepare_commit` reserves against (X3D:128), plus a provisional 25 % and 16 MiB allocation overhead, plus the inodes for the planned objects. The host keeps no second estimate.
- **Placement.** Inside `prepare_commit` (`commit.rs:449-465`): after step 0's end-path reserve, the binding and the carrier-capacity check, and before `admit_layout`'s directory creation (`commit.rs:370`) and attempt admission. Ledger and reserve ordering are preserved. It does **not** precede effects already taken when the commit session opened (lease and journal records under X3b/X3c); S-OP-8 must state whether to move it earlier.
- **Four outcomes (OP-R2-04).**
  1. *Observation succeeded, sufficient:* continue.
  2. *Observation succeeded, insufficient:* refuse before any store effect. This is a decision over a completed read, as `CarrierCapacityExhausted` is (X3D:139), not a native failure: `operational-failed`/`host-io` with `HOST.IO_FAILURE`, or a dedicated detail if S-OP-8 adds one through the detail-registry owner.
  3. *Observation succeeded but carries no meaningful figure ("capacity unavailable"):* disclose in `diagnostics` and continue.
  4. *Observation failed:* a failed syscall, a refused budget charge or a failed custody recheck latches the attempt ledger, as any failed charge does (`commit_session.rs:513-516`; `work_ledger.rs:244-256`). The session then stops by the existing phase-specific route (X3D item 9's host I/O or budget row). It is never wrapped as a successful "unknown" to keep the ledger open (X3D:261, 383). This needs no law change.
- **Nothing downstream changes.** A passing sample suppresses no later ENOSPC, quota, inode, I/O, barrier or CommitUndetermined handling. No reservation is claimed.
- **Logging under pressure** degrades to counters (§3.3). **Doctor** may report headroom under S-OP-9.

### 5.5 Cancellation (K7; OP-NB-02)

- **Two stages.** The first SIGINT, SIGTERM or SIGHUP cancels cooperatively: no new work is admitted, providers get `cancel` with reason `user` (CC:37), and the edge is logged. A second signal, or a grace expiry (provisional 2 s), forces provider-tree kill, also logged. The resulting termination depends on the phase (below). OpenSIP never uses 143.
- **The cancellation join by phase (OP-R2-02; S-OP-12).** The signal is recorded with the phase in which it arrived (WS:224).

| Phase | What the signal does | Projection |
|---|---|---|
| A. Before attempt admission | cooperative cancel; no commit starts | `interrupted` 130 with `signal`; runId only for a Run committed by an earlier step (WS:224-227) |
| B. Attempt admitted, before FinalGate admission (`commit_session.rs:929-935`) | **proposed (S-OP-12):** the signal fetch-ORs the operation's existing FinalGate latch, as an observer latch does (X3D:158, 185). A latch before admission means state 2: no permit, the staged transaction rolls back, and a durable SEAL stays uncommitted history (X3D:169). `finish` runs per X3D item 7. | `interrupted` 130 with `signal`; no runId from this attempt |
| C. FinalGate admitted; evidence COMMIT under the permit (`commit_session.rs:937-938`) | the latch is propagated (state 3); the COMMIT's own durability outcome stands (X3D:170) | `Committed` + `latchedAfterAdmission`: X7's F16 row, `operational-failed` 4, `DELIVERY.REQUIRED_FAILED`, runId retained, no delivery phase (X7:99-100). `CommitUndetermined`: `operational-failed` 4, `DURABILITY.COMMIT_FAILED`, `durability-commit`, executionId in the remedy subject, no runId (X7:101). **Not** `interrupted`. |
| D. Commit returned unlatched; some required step not yet terminal | WS's before-settle rule: remaining steps are cancelled | `interrupted` 130 with `signal`, naming the committed runId (WS:224-227). S-OP-12 decides, with the X7 owner, whether a signal during the same step's required delivery takes this row or X7's latched row. |
| E. Every required step terminal | nothing is reclassified | the settled class stands (WS:227-228, 1393) |

  Treating the signal as a FinalGate latch observer is new; it is S-OP-12, owned with the X3D and X7 owners. Until S-OP-12 is accepted, no signal sets the latch. A signal in phase B is acted on after `publish` returns: by row D or E for `Committed`, or by X7's `CommitUndetermined` row.
- **The second stage inside a native effect (OP-R2-03).** A second signal arriving while an admitted native effect is in flight waits for that effect to return. In phase C that is the evidence COMMIT; in phase B it is a journal commit, barrier or object write already issued. **That wait has no established wall-clock bound.** The work ledger counts objects, edges, bytes and records, not time (`work_ledger.rs:12-21`), and its scopes enforce budgets, not native-call timeouts. A stalled native call stalls the wait. The only exit is process death (for example SIGKILL), which leaves the recovery evidence M2 already handles (X3D:213). It never produces an invented clean refusal or a rewrite of committed or uncertain durability (X3D:163). Outside an in-flight native effect, the forced stage proceeds immediately. A reviewed time-bound mechanism (platform, commit and supervision, with an honest timeout fate) is possible as a future successor; this plan does not propose one.
- **Goal, not threshold:** p95 ≤ 2 s and max reported, from first-signal delivery to process exit, over 20 trials per workload, with logging at its default level, on AQP's pinned medium and stress workloads. Worst teardown and drain observations are retained. Samples that land in a stalled native effect are reported, not excluded. The goal is a measurement, not a bound.
- **Control:** a cancelled run never leaves a clean-looking result (CH13:104-105).

### 5.6 Hostile input (O7, owner, open)

The analyzed repository is attacker-controllable in CI. G21 "does not claim security confinement" (QG:429), and DR-128 holds the post-MVP sandbox boundary (REG:317). This plan does not decide O7. Recommendation: OS-level confinement where each platform allows it, otherwise a documented "run untrusted repositories in a container" requirement. Needed before M3 providers ship.

---

## 6. Support

**`opensip doctor --bundle`** (M5; S-OP-9, a DR-114 successor; O5). Default doctor's no-write, no-execution, no-egress behavior is unchanged (DRC:603-610).
- **Inputs (read-only, observation path):** version, platform and installation state; resolved configuration with provenance, secret values excluded (F03:47); names of declared environment variables, never values; lock and lease state; provider versions; disk headroom; safe log and crash records for selected RequestIds (committed RunId as an extra filter).
- **Output:** one consented write of a bounded archive (provisional 32 MiB, per-member caps) to a user-chosen destination outside the project and installation. It alters no project, trust, recovery or installation metadata.
- **Before writing,** it lists every member, its privacy class and size, and asks. P2 members need their own consent (§3.2).
- **Never included:** source, raw journal, ledger or store files, provider stderr text (never stored), free text.

**A troubleshooting runbook** generated where possible: D9 codes and remedies from the catalog (K1), events from the vocabulary registry; hand-written sections for slow runs, indeterminate results, provider faults, lock contention and full disks. Log layout, limits and defaults are generated from code constants (F1).

---

## 7. Enforcement (K5; OP-NB-05)

Narrow APIs plus structural checks, with an audited exception list naming the owning module for each exception: output and terminal, termination, platform, supervision, configuration resolver, crash path.
- **Stdio:** clippy `print_stdout`/`print_stderr`, plus a source check for `std::io::stdout`/`stderr`, raw fd 1/2 writes and `libc::write`.
- **Environment:** `disallowed_methods` for `std::env::var`, `var_os`, `vars` and `vars_os` outside the resolver and the platform owners that legitimately read process state.
- **Processes:** `std::process::Command` only inside supervision and the platform's custody owners; `process::exit` and `abort` only in termination and the crash path.
- **Events:** emission only through the registry macro; a test rejects unregistered or dynamically built names.
- **Swallowed errors:** a typed `dispose(err, Disposition::…)` helper over a closed enum replaces `// swallow-ok`; a test rejects bare `let _ =` on `Result` outside the audited list.
- **TS provider code:** lint bans on `console`, `process.env`, `child_process` and `fs` outside the SDK.
- **Negative controls:** a planted direct stderr write, ambient environment read, unregistered event, dynamic event name, raw spawn and false disposition each make the check fail.

---

## 8. Milestones

| Milestone | Work | Depends on |
|---|---|---|
| **Before the M3 provider protocol law** | O1 decided; if (b), S-OP-3 and S-OP-4 accepted. S-OP-4 record join under (a). O7 decided by the owner. S-OP-2 vocabulary drafted. AQP INC-1 to INC-8 in the same law. | O1, O7, S-OP-2/3/4 |
| **M3** | `tracing` stack with nonpersistent sinks; the vocabulary and per-sink allowlists; all §3.3 bounds and loss marker; phase spans and the operational record as harness instrumentation; supervision primitive and liveness; the outcome matrix in tests; two-stage cancellation; enforcement checks. Then, once accepted: the file sink and retention (S-OP-1), crash records (S-OP-7), capacity preflight (S-OP-8), the cancellation latch join (S-OP-12), public `-v`/`--log-level` (S-OP-5, S-OP-6). G20/G21 controls authored now (S-OP-11), including the §10 privacy, bounds, crash, capacity and cancellation controls. | S-OP-1, 2, 5, 6, 7, 8, 11, 12 |
| **M4** | `request` line in every human renderer and `--timings` (S-OP-6); public reuse disclosure (AQP INC-8); doctor per-request log query (S-OP-9); generated runbook. | S-OP-6, S-OP-9 |
| **M5** | `doctor --bundle` (S-OP-9, O5); OTLP export if O4 approves (S-OP-10); resident-host supervision and restart policy (AQP INC-6), alongside MCP `agent-serve`. | O4, O5, S-OP-9, S-OP-10 |
| **M6** | Qualification on `harness.DR-G20.product-v1` and `harness.DR-G21.product-v1` (QG:403-441) over the selected platform population, AL2023 only through its accepted DR-126 successor (AQP D11); cancellation and overhead measurements reported against the provisional goals. | S-OP-11; DR-126 successor |

---

## 9. Decisions and successors

Authority: **owner** means product scope, egress, consent and threat posture; **lead** means technical mechanism. Accepting this plan accepts no successor; each is reviewed on its own. Labels are provisional.

| ID | Decision | Authority | Status | Recommendation |
|---|---|---|---|---|
| O1 | Provider diagnostics and liveness channel | lead | proposed | (a) existing observations only (§3.6) |
| O2 | Log layout and retention defaults | lead | proposed | §3.3–§3.4 provisional values. Per-file 64 MiB hard cap; 512 MiB aggregate best-effort target with no finite aggregate bound; stop rule at a 768 MiB backlog that can't be reclaimed |
| O3 | Operability configuration placement | lead | proposed | S-OP-5 `operability` section, nonsemantic; outcome-affecting limits stay constants or semantic budgets |
| O4 | OTLP export | **owner** (egress) | **open** | opt-in configuration plus egress grant at M5, P0 allowlist |
| O5 | Bundle contents and consent | lead, owner sign-off | proposed | §6; never source or free text |
| O6 | Limit defaults and cancellation goal | lead, by measurement | proposed | §5.2, §5.5 provisional; set from AQP measurements |
| O7 | Hostile-input confinement | **owner** (threat) | **open** | OS confinement where available, else a documented container requirement |
| O9 | A restricted, consented capture of raw provider stderr | lead, owner sign-off | proposed | not at M3; revisit with S-OP-9 if support needs it |

r1's O8 (contract placement) is replaced by the successor table below.

| Successor | Content | Owning authority | Blocks |
|---|---|---|---|
| S-OP-1 Operational log storage and custody | Which admitted write capability creates, opens, rotates and prunes logs and crash files; original-owner custody predicates; log-directory lock; charged bounded work; read rules for doctor | Security (installation custody, OWN lineage) + storage (DR-124 state classes, DR-109) | M3 file sink, S-OP-7, S-OP-9 |
| S-OP-2 Safe event vocabulary and sink law | Registry, `SafeField` set, privacy classes, per-sink allowlists, §3.3 bounds and loss marker | DR-125 owners: Component architecture + CLI/operability/security | M3 logging |
| S-OP-3 Common-control successor | Diagnostic/progress message, windows, bounds, negotiation, old-peer behavior (only if O1(b)) | DR-102 protocol authority, with DR-127 | M3 protocol law under (b) |
| S-OP-4 SDK join | (a): record join for the stderr and fault-detail disposition and admitted-progress derivation; (b): SDK methods for the new frame; TS major 2 and Rust major 3 joins | DR-125 owners | M3 protocol law |
| S-OP-5 Configuration successor | PCS `operability` section, host mapping, `host.operability.nonsemantic` classification, provenance | DR-103 admission/configuration owners | public log configuration |
| S-OP-6 Command inventory and output successor | `-v`, `--log-level`, `--timings`; human `request` line; timing and reuse disclosure carriers; renderer parity goldens | DR-123 Product/CLI + output/operability | M3 public switches, M4 surfaces |
| S-OP-7 Crash-record custody and stopping join | §5.3 path; descriptor admission; which platforms provide a nonblocking stderr path; the latched/uncertain suppression flag; whether log writes after a certain latch are outside X3D stopping | Security + storage, with the X3D owner | M3 crash records |
| S-OP-8 Capacity preflight | Storage-owned charged step inside `prepare_commit` before `admit_layout`, using storage's object plan; placement relative to session open; stop row for positive insufficiency; failed observation latches; optional detail code | Platform + storage + D9/detail registry owner (DR-007/DR-123) | M3 preflight |
| S-OP-9 Doctor log query and bundle | Operational-file reads, consented output write, member classes and limits | DR-114 Operability + security | M4 query, M5 bundle |
| S-OP-10 OTLP export | Host egress effect, export allowlist, bounds | Host-effect owners (DR-105) + output; after O4 | M5 |
| S-OP-12 Cancellation and commit join | The signal as a FinalGate latch observer (phase B); phase D versus X7's latched row during required delivery; no elapsed-bound claim | Storage + security (X3D owner) + host finalization (X7 owner) | M3 cancellation |
| S-OP-11 G20/G21 harness authoring | Operability and containment corpora, including §10 controls | QG owners: Component architecture + CLI/operability (G20); Supervisor + protocol + operability (G21) | M3 controls, M6 qualification |

---

## 10. Proposed controls

Authored at M3 under S-OP-11; qualified at M6.

| Area | Controls |
|---|---|
| Privacy (OP-R1-03) | Unique canary tokens and novel secrets (random high-entropy, low-entropy passphrase, unknown formats) and source snippets injected into provider stderr, `fault` detail, file and directory names, I/O error messages, panic payloads and nested configuration values. Every byte stream (file, stderr, crash ring, bundle, captured OTLP) must contain no canary outside P2 names. Compile-fail tests for a non-`SafeField` value and a secret type. Canaries are also checked as derived fingerprints (SHA-256 of each canary), which must appear in no sink (OP-R2-NB-01). |
| Correlation (OP-R1-02) | Every record has the right RequestId; no ExecutionId before admission; no RunId for candidate, undetermined or ephemeral runs; allocation failure emits only the emergency line. |
| Custody (OP-R1-04) | Metadata, doctor and refused requests leave the installation byte-identical and never create it; no provider receives a log path. |
| Bounds (OP-R1-08, OP-R2-05) | Provider stderr flood at 10× its bound; event storm; stalled writer (blocked FIFO): producers and cancellation unaffected; unwritable sink (EACCES, ENOSPC, EIO): counters only, outcome unchanged; 8 parallel writers: no interleaving and each file within 64 MiB. Repeated busy-lock passes across rotations, deletion failure, listing failure and a pruner killed mid-pass: the stop rule fires, the process opens no further file, the loss is disclosed, and each process's excess over the threshold is at most one file. No aggregate bound is asserted. Cancellation with a full queue meets the drain deadline. |
| Outcomes (OP-R1-07, OP-R2-01) | One case per §5.2 row, including: workspace over 4,096 units → exit 2, no Run; evaluator budget → indeterminate `COVERAGE.BUDGET_EXHAUSTED` on a sealed Run; required projection failure with no Run → exit 4, no runId; required renderer failure after commit → exit 4, runId retained; optional export failure under each primary class → termination unchanged; no clean partial; optional-sink loss. |
| Crash (OP-R1-09, OP-R2-06) | Panic under a logger lock, under a commit lock, nested panic, full or unwritable disk, absent installation, no descriptor. stderr is a full blocking pipe: the hook skips the write and never blocks on it. Crash file on a stalled filesystem (injected stall): the documented unbounded stall is observed and reported, not hidden. Panic after a latched or after an uncertain operation: no crash-file bytes, and no log bytes after uncertainty. No lock-induced deadlock, no second panic. |
| Capacity (OP-R1-10, OP-R2-04) | Space consumed after a passing sample, then ENOSPC; quota and inode exhaustion; failure at each commit stage after a passing sample. Successful observation with no meaningful figure: disclosed, continues. Failed `fstatvfs` (injected EIO), refused budget charge, failed custody recheck: the ledger latches and the existing stop route applies, with no continuation. Positive insufficiency: refused before `admit_layout`, with no store effect. |
| Cancellation (OP-R2-02, OP-R2-03) | A signal in each of phases A–E of §5.5, with the expected projection, including Committed-with-latch → exit 4 with runId and CommitUndetermined → exit 4 with executionId. Stalled native operation plus a second signal (injected stall in the evidence COMMIT and in a barrier): the process keeps waiting, invents no refusal, and projects per X7 after return; SIGKILL during the stall leaves M2 recovery evidence. Operation-count exhaustion is never treated as an elapsed timeout. |
| Liveness (OP-R1-05) | Spinning provider sending traffic without admitted progress; blocked provider; legitimate long phase that completes within the deadline. |
| Overhead | Results identical with logging off and on, and at concurrency 1 and automatic; overhead and loss measured on AQP workloads before defaults are frozen. |

## Not claimed

- No contract, schema, gate or register row is changed; every successor in §9 is future work.
- No bound, default, latency or overhead has been measured; all are provisional.
- No finite aggregate log-retention bound, no elapsed bound on a second-signal wait inside a native effect, and no elapsed bound on the panic hook's crash-file write.
- The opensip-cli lessons come from reading its code, not running it.
- No product code, test or crash matrix was run for this revision.
