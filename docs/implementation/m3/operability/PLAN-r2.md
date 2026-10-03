# M3 operability plan: logging, observability, resilience and support — proposal r2

2026-10-03. Claude Opus 5.5, implementation lead, at the owner's request ("draft the operability plan"). r1 (`PLAN-r1.md`, sha256 `f2005ed0…`, 19,287 bytes) was reviewed by CODEX2 (method; `reviews/codex-operability-plan-r1/`, REQUIRED-FINDINGS, 10 required and 7 non-blocking). r2 answers all 17. The predecessor `opensip-cli` (HEAD `83f705d8`) supplies lessons (§2). Product main is `eb0d5039`.

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
- Product paths are under `opensip/`; product schemas under `opensip/schemas/sources/`; predecessor paths under `opensip-cli/`.

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
| Outcomes | Exit table 0/1/2/3/4/130; termination branch contract; `interrupted` carries `signal` (SIGINT/SIGTERM/SIGHUP) and a RunId only when a Run committed first; optional export failure is success 0; after-settle is never reclassified; no new D9 family. No run envelope is fabricated before a Plan or Run exists. | WS:1340-1346, 1355-1366, 1376-1378, 1393-1397; `common-v4.schema.json:280` (D9Signal) |
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

Named in §9: S-OP-1 log storage custody; S-OP-2 safe event vocabulary and sink law; S-OP-3 common-control (only under O1(b)); S-OP-4 SDK join; S-OP-5 configuration; S-OP-6 command inventory and output; S-OP-7 crash record; S-OP-8 capacity preflight; S-OP-9 doctor log query and bundle; S-OP-10 OTLP export; S-OP-11 G20/G21 harness authoring.

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

- **Closed vocabulary.** Every event name is registered with a typed field schema. Field types are limited to a sealed `SafeField` set: closed enum codes (D9 codes, DomainDetail codes, provider-subprotocol reason enums), integers, durations, byte counts, digests, the identities of §3.1, versions, platform IDs, rule IDs, and project-relative paths with line numbers. No `Debug` or `Display` of arbitrary values; no error objects (DC4:1058), only an error code and a closed error-kind enum. A non-safe value fails to compile. r1's "total encoder with typed placeholders" is replaced by this compile-time closure.
- **Privacy classes:** **P0** codes, counts, durations, versions, platform; **P1** correlation identities; **P2** project structure (relative paths, line numbers, rule IDs, file and directory names, which may themselves be sensitive, DC4:1074); **P3** free text and source bytes. P3 has no `SafeField` type and cannot be logged.
- **Secrets.** A resolved secret value is a type with no `SafeField`, `Debug` or `Display` implementation; a test proves it. A handle name (when DR-108 lands) is P2. Environment variables appear only by declared name, never value.
- **Provider output.** Raw provider stderr is captured up to the negotiated bound (`handshake-v1.schema.json:281-282`, `maxStderrBytes` 262,144), held in memory, and reduced at settle to `{bytes, sha256, truncated}`, the shape test execution already uses (`test-execution-v1.schema.json:340-348`). Its text is never written to a log, crash ring, bundle or exporter. The control `fault` detail (CC:36, ≤ 1,024 bytes) is treated the same: digest and length only. Providers that need a diagnosable reason use the provider-subprotocol's closed reason enums, which are P0. A separately consented restricted capture is O9.
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
- **Retention.** The 512 MiB total is a **bounded best-effort target, not a hard cap.** A hard cap needs a shared reservation ledger, which is not worth its cost for M3. Pruning runs at writer start and on rotation, under a non-waiting try-lock on a log-directory lock (S-OP-1); if the lock is busy, that pass is skipped. It deletes only closed files (an active file is held by its writer's advisory lock), oldest first, until the total is ≤ 512 MiB. Active and crash files count. Worst-case overshoot is (concurrent writers × 64 MiB) + (≤ 32 retained crash files × 64 KiB). Age retention is 14 days.
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
- **Diagnostics.** Providers report through what exists: the provider-subprotocol's closed responses (`UnavailableV1`, `BudgetExhaustedV1` …; DRC:556-568) carry P0 reason codes; `fault` and stderr are digested (§3.2). The host emits the records.
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
- **Failure is observational.** A bounded queue (provisional 1 MiB), a 1 s shutdown, drop with a count. Export failure is success 0 (WS:1378) and never changes a verdict.
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

**Concurrency (OP-NB-06).** Automatic host concurrency is `clamp(min(cpus − 1, ⌊memory budget ÷ per-provider RSS ceiling⌋), 1, 16)`, all provisional. The observed CPU and memory and the resolved value go in the operational record, never the Plan. A control checks that results are identical at concurrency 1 and at the automatic value.

**Every failure class keeps its own route.** r1's "each cap hit is a typed deficiency that marks the result incomplete" is withdrawn.

| Class | Phase | Route (existing) | Run effect |
|---|---|---|---|
| Semantic work budget, candidate or graph cap | analysis | provider `BudgetExhaustedV1` / `EVALUATION.WORK_BUDGET_EXHAUSTED`, `PROJECT.WORKSPACE_UNIT_LIMIT`, `OUTPUT.RENDERER_QUOTA_EXCEEDED` under the owned Coverage rules | honestly incomplete Coverage; no clean partial (CH13:102-105) |
| Malformed, oversized or out-of-window frame; RF2 | any provider stage | G21 containment, `provider-protocol` fault cause (WS:1358-1361) | candidate discarded; not "incomplete analysis" |
| Deadline, liveness failure, RSS breach, crash, unexpected exit | any provider stage | G21 containment and its Coverage/D9 mapping (F02:199-206) | candidate discarded; sealed evidence untouched |
| Host I/O failure | before commit admission | `operational-failed`, `host-io` | no Run |
| Capacity insufficient (§5.4) | before `prepare_commit` | `operational-failed`, `host-io`, `HOST.IO_FAILURE` detail | no Run; no store effect |
| User interrupt | before settle | `interrupted` 130 with `signal`; RunId only if committed (WS:1364) | candidate discarded |
| User interrupt or forced second stage | after commit admission | the commit's own outcome stands: `Committed` keeps its class; `CommitUndetermined` stays undetermined (X3D:170) | never reclassified (WS:1393) |
| Required output failure | after commit | `DELIVERY.REQUIRED_FAILED` (WS:1376) | Run retained |
| Host panic | before commit admission | `operational-failed`, `host-invariant` where the termination layer is reachable | no Run |
| Host panic | after commit admission | no outcome manufactured; recovery evidence stands (X3D:213) | unchanged |
| Optional observability loss: dropped records, sink failure, export failure, crash-record failure | any | nonsemantic counters and one `diagnostics` line | none, ever |

No D9 or Coverage mapping change is proposed. A dedicated capacity detail code is optional under S-OP-8.

### 5.3 Panics and crash records (OP-R1-09; S-OP-7)

- **What can produce a record.** Only a Rust panic in the host, and only best-effort. SIGKILL, the OOM killer, `abort()` from native code, stack overflow and power loss produce none. Provider crashes are recorded by the host's normal supervision path, not by this one.
- **The hook is minimal and non-reentrant**, after the predecessor's last-resort net (K8):
  1. An atomic flag marks the process as crashing. A nested panic, or a panic while the flag is set, goes straight to `abort` with no further work.
  2. It takes no logger, storage, journal or ledger lock, does no formatting beyond copying static strings, allocates nothing, and does not symbolize a backtrace. The panic payload is not read. It uses only the panic location (`&'static str` file and line), the build version, platform ID, RequestId, ExecutionId if any, and the current phase code, all preformatted at admission.
  3. It writes one fixed coded line to fd 2 with `write(2)`: `HOST.INVARIANT_VIOLATED request=req1_… (see crash record)` or, with no descriptor, the same line without the suffix.
  4. If the invocation holds a crash descriptor, it does one bounded `write(2)` (≤ 64 KiB) of the preformatted header plus the crash ring. The descriptor was opened owner-only, append and no-follow by S-OP-1's write capability when that capability was admitted. It does no `fsync`, rename or barrier.
- **Fallbacks.** No descriptor (metadata, doctor, observation-only, pre-admission): stderr line only. A failed write (ENOSPC, EIO): nothing more. A failed stderr: nothing.
- **After a latched or uncertain operation**, the hook does only the two writes above to already-admitted descriptors. It does no retry, reconciliation, journal append or cleanup, and manufactures no Run outcome (X3D:163, 196). The top-level boundary maps an unwind to `operational-failed`/`host-invariant` only before commit admission (§5.2).
- **Records** are operational state, owner-only, under S-OP-1 retention; at most 32 retained. They explain and never drive recovery.

### 5.4 Disk-capacity preflight (OP-R1-10; S-OP-8)

- **Advisory, not a guarantee.** One `fstatvfs` on the admitted store directory handle (original-handle custody, charged to the operation's work budget) reads available bytes and inodes. It is compared with a conservative bound: the declared object bytes that `prepare_commit` step 2 already reserves against (X3D:128), plus a provisional 25 % and 16 MiB allocation overhead, plus the inodes for the planned objects.
- **Placement.** After Plan sealing, when the planned bytes are known, and before `prepare_commit` (`commit.rs:465`), so before `admit_layout`'s directory creation and attempt admission. It does **not** precede effects already taken when the commit session opened (lease and journal records under X3b/X3c); S-OP-8 must state whether to move it earlier.
- **Three outcomes.** Positive insufficiency: refused before any store effect, `operational-failed`/`host-io` with `HOST.IO_FAILURE` (or a dedicated detail if S-OP-8 adds one through the detail-registry owner). Unknown (filesystem reports no meaningful figure) or failed observation: proceed, with a `diagnostics` disclosure. Sufficient: proceed.
- **Nothing downstream changes.** A passing sample suppresses no later ENOSPC, quota, inode, I/O, barrier or CommitUndetermined handling. No reservation is claimed.
- **Logging under pressure** degrades to counters (§3.3). **Doctor** may report headroom under S-OP-9.

### 5.5 Cancellation (K7; OP-NB-02)

- **Two stages.** The first SIGINT, SIGTERM or SIGHUP cancels cooperatively: no new work is admitted, providers get `cancel` with reason `user` (CC:37), and the edge is logged. A second signal, or a grace expiry (provisional 2 s), forces provider-tree kill, also logged. All map to `interrupted` 130 with the received `signal`.
- **Commit critical section.** A second signal arriving between attempt admission and `publish`'s return is deferred until the commit outcome is known; that wait is bounded by the commit's own budget. The settled outcome is then reported and never reclassified. A hard process deadline never rewrites M2 commit or cleanup truth; process death leaves the recovery evidence M2 already handles.
- **Goal, not threshold:** p95 ≤ 2 s and max reported, from first-signal delivery to process exit, over 20 trials per workload, with logging at its default level, on AQP's pinned medium and stress workloads. Worst teardown and drain observations are retained.
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
| **M3** | `tracing` stack with nonpersistent sinks; the vocabulary and per-sink allowlists; all §3.3 bounds and loss marker; phase spans and the operational record as harness instrumentation; supervision primitive and liveness; the outcome matrix in tests; two-stage cancellation; enforcement checks. Then, once accepted: the file sink and retention (S-OP-1), crash records (S-OP-7), capacity preflight (S-OP-8), public `-v`/`--log-level` (S-OP-5, S-OP-6). G20/G21 controls authored now (S-OP-11), including the §10 privacy, bounds, crash, capacity and cancellation controls. | S-OP-1, 2, 5, 6, 7, 8, 11 |
| **M4** | `request` line in every human renderer and `--timings` (S-OP-6); public reuse disclosure (AQP INC-8); doctor per-request log query (S-OP-9); generated runbook. | S-OP-6, S-OP-9 |
| **M5** | `doctor --bundle` (S-OP-9, O5); OTLP export if O4 approves (S-OP-10); resident-host supervision and restart policy (AQP INC-6), alongside MCP `agent-serve`. | O4, O5, S-OP-9, S-OP-10 |
| **M6** | Qualification on `harness.DR-G20.product-v1` and `harness.DR-G21.product-v1` (QG:403-441) over the selected platform population, AL2023 only through its accepted DR-126 successor (AQP D11); cancellation and overhead measurements reported against the provisional goals. | S-OP-11; DR-126 successor |

---

## 9. Decisions and successors

Authority: **owner** means product scope, egress, consent and threat posture; **lead** means technical mechanism. Accepting this plan accepts no successor; each is reviewed on its own. Labels are provisional.

| ID | Decision | Authority | Status | Recommendation |
|---|---|---|---|---|
| O1 | Provider diagnostics and liveness channel | lead | proposed | (a) existing observations only (§3.6) |
| O2 | Log layout and retention defaults | lead | proposed | §3.3–§3.4 provisional values; best-effort aggregate cap |
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
| S-OP-7 Crash-record custody and stopping join | §5.3 path; descriptor admission; relation to X3D stopping rules | Security + storage, with the X3D owner | M3 crash records |
| S-OP-8 Capacity preflight | Observation, charging, placement relative to session open and `prepare_commit`, D9 mapping, optional detail code | Platform + storage + D9/detail registry owner (DR-007/DR-123) | M3 preflight |
| S-OP-9 Doctor log query and bundle | Operational-file reads, consented output write, member classes and limits | DR-114 Operability + security | M4 query, M5 bundle |
| S-OP-10 OTLP export | Host egress effect, export allowlist, bounds | Host-effect owners (DR-105) + output; after O4 | M5 |
| S-OP-11 G20/G21 harness authoring | Operability and containment corpora, including §10 controls | QG owners: Component architecture + CLI/operability (G20); Supervisor + protocol + operability (G21) | M3 controls, M6 qualification |

---

## 10. Proposed controls

Authored at M3 under S-OP-11; qualified at M6.

| Area | Controls |
|---|---|
| Privacy (OP-R1-03) | Unique canary tokens and novel secrets (random high-entropy, low-entropy passphrase, unknown formats) and source snippets injected into provider stderr, `fault` detail, file and directory names, I/O error messages, panic payloads and nested configuration values. Every byte stream (file, stderr, crash ring, bundle, captured OTLP) must contain no canary outside P2 names. Compile-fail tests for a non-`SafeField` value and a secret type. |
| Correlation (OP-R1-02) | Every record has the right RequestId; no ExecutionId before admission; no RunId for candidate, undetermined or ephemeral runs; allocation failure emits only the emergency line. |
| Custody (OP-R1-04) | Metadata, doctor and refused requests leave the installation byte-identical and never create it; no provider receives a log path. |
| Bounds (OP-R1-08) | Provider stderr flood at 10× its bound; event storm; stalled writer (blocked FIFO): producers and cancellation unaffected; unwritable sink (EACCES, ENOSPC, EIO): counters only, outcome unchanged; 8 parallel writers: no interleaving, aggregate within the stated overshoot; cancellation with a full queue meets the drain deadline. |
| Outcomes (OP-R1-07) | One case per §5.2 row, including no clean partial, interrupt before and after commit admission, and optional-sink loss. |
| Crash (OP-R1-09) | Panic under a logger lock, under a commit lock, nested panic, full or unwritable disk, absent installation, no descriptor; no deadlock, no second panic, no further effect after an uncertain commit. |
| Capacity (OP-R1-10) | Space consumed after the sample, quota and inode exhaustion, failure at each commit stage after a passing sample, unknown observation. |
| Liveness (OP-R1-05) | Spinning provider sending traffic without admitted progress; blocked provider; legitimate long phase that completes within the deadline. |
| Overhead | Results identical with logging off and on, and at concurrency 1 and automatic; overhead and loss measured on AQP workloads before defaults are frozen. |

## Not claimed

- No contract, schema, gate or register row is changed; every successor in §9 is future work.
- No bound, default, latency or overhead has been measured; all are provisional.
- The opensip-cli lessons come from reading its code, not running it.
- No product code, test or crash matrix was run for this revision.
