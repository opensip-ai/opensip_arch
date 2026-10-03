# M3 operability plan r3 review

**Verdict: ACCEPT as a plan.** All six r2 required findings are resolved. OP-R1-07 through OP-R1-10 are now fully resolved, and all four r2 non-blocking observations are addressed. No required finding remains.

Subject: `docs/implementation/m3/operability/PLAN.md`, **70,544 bytes**, SHA-256 `b49035f27abac0b6c6e4eed88fef52de8efa33285f7a5cdb66bd95cad3170c46`. Previous r2: **54,138 bytes**, SHA-256 `a65ea9c7ff8da4315d9649d0fd79cfb81bfc773fe36dd2244e40d9e3d5ac814b`.

Accepted as a plan. No successor, schema/configuration change, signal-to-latch mechanism, file-write custody, post-latch logging exception, optional egress or threat-policy decision is accepted by this verdict. Implementations and qualification remain future work behind the named owners.

## Review basis

I read the request, the full pinned r3 plan, exact r2 plan and prior review, compared the entire diff, and checked the new contracts/source references. Design HEAD: `bbc02c15242679426f735274a4ecb9863c74923c`; product HEAD: `eb0d50398035fe3532dadc332f88cf1d8bc4cb69`; predecessor HEAD: `83f705d8a33ec917cc5b3380e126788b6824d630`. The product and design had no tracked working-tree modifications at the status check. Design HEAD later advanced to `c563c54fd0366148cad8ac6a7f569d9fbbca89a2` for separate M3 unit-plan revisions and reviews; the operability subject and its cited files were unchanged.

This was a single-reviewer static review. No product code, tests, crash matrix or full lanes were run. No real OpenSIP home or private 413 fixture was accessed. No repository file was edited, and no commit or push was made. Only REVIEW.md and review.json were written under the requested output directory. Source checks establish the plan's consistency, not implemented behavior or measured performance.

## Required-finding resolution

| r2 ID | Decision | r3 change and evidence |
|---|---|---|
| OP-R2-01 | Resolved | Discovery refusal, evaluator budget exhaustion, evaluation output bounds, provider exhaustion and required/optional rendering now have separate owning observations and routes. Workspace-unit excess is exit 2 with no Run; evaluator exhaustion uses the sealed Run's COVERAGE.BUDGET_EXHAUSTED route; registered renderer-quota detail alone grants no Coverage mapping. Proposed controls cover the corrected cases. Evidence: [NE:871](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:871), [WPC:140](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md:140), [WS:1376](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:1376). |
| OP-R2-02 | Resolved | The five-phase table distinguishes attempt admission, FinalGate admission, evidence COMMIT, required-step settlement and after-settle handling. Committed-with-latch and CommitUndetermined keep the exact X7 exit-4 projections and their different RunId/ExecutionId disclosure. The new signal-to-latch mechanism and same-step delivery join are explicitly proposed under S-OP-12, with X3D/X7 owners and an M3 dependency. Acceptance here does not choose or authorize that successor. Evidence: [X3D:168](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:168), [X7:98](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/finalization-x7/PROPOSAL.md:98), [WS:224](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:224). |
| OP-R2-03 | Resolved | The elapsed bound from work counters is withdrawn. Native-call stalls and possible process death are disclosed, the p95 goal remains a measurement, stalled samples cannot be excluded, and proposed controls preserve durability/recovery truth rather than inventing a clean timeout refusal. Evidence: [work_ledger.rs:12](/Users/sb/code/opensip-ai/opensip/crates/platform/src/work_ledger.rs:12), [X3D:163](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:163). |
| OP-R2-04 | Resolved | The four outcomes separate successful sufficient/insufficient/unavailable samples from actual syscall, charge and custody failures. Actual failures latch the same operation ledger and stop; no failure is wrapped as successful unknown. Preflight is a future storage-owned charged step inside prepare_commit, after reserve/planning/carrier check and before layout writes, using the existing retained store handle and exact object plan. Evidence: [commit.rs:469](/Users/sb/code/opensip-ai/opensip/crates/storage/src/commit.rs:469), [commit_session.rs:444](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/commit_session.rs:444), [commit_session.rs:516](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/commit_session.rs:516), [X3D:139](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:139), [X3D:261](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:261). |
| OP-R2-05 | Resolved | The unsupported finite aggregate overshoot is withdrawn consistently. Per-file hard caps remain, 512 MiB is a target, a provisional 768 MiB unreclaimed-backlog rule stops new persistent files for that process, and concurrency prevents claiming a fixed aggregate bound. Controls now exercise repeated failed/skipped pruning rather than asserting the previous false total cap. Evidence: [PLAN.md:202](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:202), [PLAN.md:393](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:393), [PLAN.md:429](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:429). |
| OP-R2-06 | Resolved | Inherited blocking stderr is skipped by the hook unless a separately established safe path qualifies through S-OP-7. Regular-file I/O's unbounded kernel stall is disclosed; lock/allocator guarantees are narrower. Crash-file effects are suppressed after a latched or uncertain operation. Normal persistent logging after uncertainty also stops; continuation after a certain latch explicitly requires X3D-owner confirmation through S-OP-7 or suppression applies. Proposed controls match those limitations. Evidence: [PLAN.md:306](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:306), [X3D:163](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:163), [X3D:253](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:253). |

The remaining r1 findings are fully resolved:

- **OP-R1-07: resolved** through OP-R2-01 and OP-R2-02. The cap/failure matrix now respects discovery, Coverage, output and invocation/commit phase owners. The new cancellation join is explicitly blocked on S-OP-12.
- **OP-R1-08: resolved** through OP-R2-03 and OP-R2-05. Queue/record/ring/drain bounds remain explicit, unsupported aggregate retention and elapsed commit-wait guarantees are withdrawn, and loss/stop controls are concrete.
- **OP-R1-09: resolved** through OP-R2-06. The panic path states its actual locking/allocation guarantees, admits possible kernel stalls, skips unsafe inherited stderr and requires crash/log stopping through its named owner join.
- **OP-R1-10: resolved** through OP-R2-04. Capacity sampling is advisory and storage-owned, before layout effects; real observation failures preserve operation latching and stop, while successful unknown capacity may continue.

## Previously non-blocking items

| r2 ID | Decision | Result |
|---|---|---|
| OP-R2-NB-01 | Resolved | Free-text/source fingerprints are P3 and excluded. Provider stderr/fault detail retain counts/truncation rather than digests, and proposed canary controls check derived fingerprints. |
| OP-R2-NB-02 | Resolved | Optional export explicitly preserves every primary termination/exit, with success 0 scoped to its golden example. |
| OP-R2-NB-03 | Resolved | The estimate comes from storage's planned object set inside prepare_commit; no host-side second estimate or premature Plan-sealing size claim remains. |
| OP-R2-NB-04 | Resolved | Memory is net of host allowance, and the floor of one applies only when a provider fits. Zero fit is an explicit successor-owned refusal/lower-ceiling decision. |

## Cancellation and capacity judgments

The five phases now distinguish a storage attempt from FinalGate admission and invocation settlement. A late latch preserves durability while X7 projects `Committed + latchedAfterAdmission` as `DELIVERY.REQUIRED_FAILED` / exit 4 with RunId, and `CommitUndetermined` as `DURABILITY.COMMIT_FAILED` / exit 4 with ExecutionId and no RunId. The plan does not relabel either as an interrupted or Coverage-indeterminate outcome. The signal-as-observer mechanism is explicitly new, blocked on S-OP-12, and assigned to X3D/X7 owners. The same-step delivery ambiguity is also assigned to that successor rather than silently resolved here.

Deferring a second signal through a native effect already issued preserves recovery truth. r3 states honestly that the wait has no established elapsed bound; the count-based work budget does not supply one. Stalled samples are reported in the proposed cancellation measurement. No clean timeout refusal is invented.

The moved disk check is a plausible storage-owned insertion point: end-path reserve, binding/object planning, carrier-capacity read, retained store-root acquisition, then the new observation before `admit_layout`. `I/stores/S` already exists and is opened read-only; `admit_layout` creates/adopts the downstream project namespace, object directories and ledger. This avoids requiring a new directory creation merely to observe capacity. S-OP-8 still owns the actual step, its charges, the positive-insufficiency stop row and any earlier placement decision. Real failed observations latch; successful samples with no useful figure can disclose and continue. Neither a sample nor a positive headroom estimate reserves storage.

O9 still defers raw provider stderr capture beyond M3, which remains reasonable. r3 additionally excludes free-text fingerprints from ordinary sinks. No new source/text capture permission is introduced.

## New citation audit

| Citation group | Assessment |
|---|---|
| NE:871–873; WPC:140–141; PDR:656 | Discovery exit 2, evaluator Coverage budget route, evaluation output-serialization fault and renderer detail-only registration all match. The new evaluation-output-bound row is part of the requested cap/output split, although not separately named in the response table. Evidence: [NE:871](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:871), [WPC:140](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md:140), [PDR:656](/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/public-detail-registry.v1.json:656). |
| WS:1376–1378; X7:99–106 | No-Run and retained-Run delivery failures, late-latch exit 4, undetermined durability exit 4, and optional-effect preservation are correct. Evidence: [WS:1376](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:1376), [X7:98](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/finalization-x7/PROPOSAL.md:98). |
| X3D:158,169–170,185; WS:224–228,1393; commit_session.rs:929–938 | Existing gate states, stop order, cleanup and durability projections support the five-phase reasoning. Signals as latch observers are new, explicitly under S-OP-12; required-delivery phase D is still an owner decision. Source boundary anchors can be sharpened per NB-01. Evidence: [X3D:158](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:158), [WS:224](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:224), [commit_session.rs:929](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/commit_session.rs:929). |
| commit.rs:449–465,370; X3D:128,139,261,383; commit_session.rs:513–516; work_ledger.rs:244–256 | The preflight is not implemented today. The cited sequence permits a new charged observation after reserve, exact planning, carrier check and retained store-root acquisition, before admit_layout. The existing I/stores/S handle is available without creating the projects/N/object/ledger layout. Successful insufficiency is a completed-read decision; actual failures still latch. S-OP-8 owns the added step and insufficiency stop row. Evidence: [commit.rs:449](/Users/sb/code/opensip-ai/opensip/crates/storage/src/commit.rs:449), [commit_session.rs:444](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/commit_session.rs:444), [operation_handoff.rs:696](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/operation_handoff.rs:696), [X3D:139](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:139), [X3D:383](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:383). |
| work_ledger.rs:12–21; X3D:163,213,253–260 | Counters establish work bounds, not native elapsed bounds. Uncertainty suppresses further effects and forfeits settlement; panic/death leaves existing recovery evidence. r3 no longer claims a wall-clock bound. Evidence: [work_ledger.rs:12](/Users/sb/code/opensip-ai/opensip/crates/platform/src/work_ledger.rs:12), [X3D:163](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:163), [X3D:213](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:213), [X3D:253](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md:253). |

The new citations support the substantive conclusions. A few line ranges can be made more precise as noted below; they do not reveal a contradictory contract.

## Changes beyond the response table

The substantive diff follows the response table, with the explicit consistency extension named in REQUEST.md. No unrelated substantive change was found.

Normal persistent log writes stop after uncertainty. After a certain latch, continuation is conditional on X3D-owner confirmation through S-OP-7; otherwise suppression applies. The uncertain half is in OP-R2-06's response; the certain-latch condition is an extension beyond that row's literal wording, explicitly disclosed in the request. See [PLAN.md:310](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:310). The evaluation-output-bound row from WPC:141 elaborates OP-R2-01. New aliases, revised milestone dependencies, successor ownership, O2 wording and proposed controls implement the advertised findings. The r2 response table remains byte-for-byte the same as a clearly labeled historical record; its superseded claims are not r3 guarantees. Other areas, including O9 deferral, owner-open egress/threat choices, support milestones, enforcement and predecessor lessons, have no substantive revision.

## Non-blocking follow-ups

### OP-R3-NB-01 — Tighten a few new source-line anchors

Location: Response table; §5.4; §5.5, [PLAN.md:35](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:35). The cited source files support the statements, but commit_session.rs:513–516 ends at the heading of charge's comment rather than its latch rule at 516–525. The evidence COMMIT call is at 939, following the cited 937–938 boundary. work_ledger.rs:244–256 reaches the scope guard; closure/latching behavior is clearer at 248–270 and 489–494. These are pointer-precision issues, not contrary evidence.

Use the exact implementation ranges when preparing the successors so reviewers land directly on the behavior being cited.

Evidence: [commit_session.rs:516](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/commit_session.rs:516), [commit_session.rs:929](/Users/sb/code/opensip-ai/opensip/crates/security/src/custody/commit_session.rs:929), [work_ledger.rs:248](/Users/sb/code/opensip-ai/opensip/crates/platform/src/work_ledger.rs:248), [work_ledger.rs:489](/Users/sb/code/opensip-ai/opensip/crates/platform/src/work_ledger.rs:489).

### OP-R3-NB-02 — Pin stopping to write admission in S-OP-7

Location: §5.3; §10 crash, [PLAN.md:310](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:310). The suppression policy is now explicit and owner-gated. Its later implementation must also cover the asynchronous writer, already queued records and the reserved loss marker. A write already in flight when uncertainty is classified may complete afterward; an atomic state flag alone does not explain the admission boundary. The proposed 'no log bytes after uncertainty' control should distinguish new effects from completion of an effect already issued.

S-OP-7 should define the linearization point for persistent-write admission and suppression, cover all writer/drain/rotation paths, and exercise uncertainty with a populated queue and a write in flight. Report any completion of prior admitted I/O honestly rather than imposing a retrospective byte-arrival guarantee. This belongs to the named successor and does not reopen the resolved r2 policy finding.

Evidence: [PLAN.md:307](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:307), [PLAN.md:200](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:200), [PLAN.md:411](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:411).

### OP-R3-NB-03 — Preserve signal arrival phase when acting on a deferred signal

Location: §5.5 fallback; S-OP-12, [PLAN.md:338](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:338). The plan correctly records arrival phase, but the interim sentence permits a phase-B signal to be acted on by 'row D or E' after publish returns. S-OP-12 should make clear that later processing time cannot turn a signal recorded before invocation settle into an after-settle signal. The result must still preserve any durability/failure outcome that arose while the native effect was in flight.

Pin arrival-phase handling in S-OP-12 and its controls, including a deferred pre-settle signal processed after commit return, and an actually after-settle signal. Keep X7's Committed-with-latch/CommitUndetermined precedence and the plan's explicit no-rewrite rule. The plan already states the governing arrival-phase rule; this is a clarification for the future join.

Evidence: [WS:224](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/workflows-and-surfaces.md:224), [PLAN.md:328](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:328), [PLAN.md:415](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:415).

These follow-ups sharpen the cited evidence and the already named successor work. They do not require another operability-plan review before the owners proceed to draft those successors.
