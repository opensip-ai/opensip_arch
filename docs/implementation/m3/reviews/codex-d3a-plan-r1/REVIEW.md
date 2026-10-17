# D3A-PLAN-r1 review

Verdict: **REQUIRED-FINDINGS** — seven required plan corrections and two non-blocking observations.

## Subject verification

Verified the 380-byte subject manifest SHA-256 `83a1581edd2c28975e4c36fec72350c5c49ffc48fa08edf89d76e34d68f955af` and its sole member `d3a/PLAN-r1.md`: 26,606 bytes, SHA-256 `9b2d051d242667b669c2e04d313b7769c8348b23fabd61c4af854df9bae5b454`. Rehashed both before writing. Product HEAD is the requested `a9a84a6fd369e7ca10689d6ab432bead3ad7eef2`; architecture HEAD is `1649a041df87555d682b4a5c30aeda67b16c6d97`.

Read the plan, M3-D r5's applicable state/joins/waits/resource/cleanup/record/outcome and boundary items, S-OP-2's provenance and required event descriptors, the D1a implementation and fixture harness, D2a's interface, and D2b's accepted plan. The pending D2b-1 framing implementation was read only to confirm its whole-frame I/O contract; it is not treated as accepted code.

## Required findings

### D3APLAN-R1-RF-1 — Specify resumable provider I/O on the non-blocking readiness loop

Location: `docs/implementation/m3/supervisor-d/d3a/PLAN-r1.md:67`.

LD-D3A-3 invokes the participant synchronously on non-blocking descriptors and cites D2b-1 read_frame as its reader. That helper is a whole-frame operation: its local prefix/digest/payload buffers and read_exact_or_eof progress are lost on an I/O error, including WouldBlock. A readable pipe need contain only one prefix byte. Calling it again cannot resume the consumed prefix; making the pipe blocking instead can stall health, stderr, exit processing and deadlines. The plan gives the control reader an incremental acquisition design but gives the provider participant no corresponding retained read/write state or yield contract.

Required change: Assign incremental prefix/digest/payload acquisition and pending-write offsets to the participant, preserving bytes and offsets across WouldBlock without supervisor ownership of provider octets. State how complete retained frames reach D2b-1 validation and how callbacks yield so other descriptors and timers run. Add split-at-every-offset, short-write/WouldBlock, partial EOF and interleaved health/deadline controls; coordinate this adapter with D2b-3/-4 rather than treating whole-frame read_frame as resumable.

### D3APLAN-R1-RF-2 — Resolve D1a blocking reap and Drop before promising a finite unreaped settlement

Location: `docs/implementation/m3/supervisor-d/d3a/PLAN-r1.md:86`.

The plan promises Child::reap within 10 seconds, or exit: unreaped, and the same bounded cleanup during unwinding. Actual D1a Child::reap calls wait4(pid, ..., 0) with no timeout. More critically, dropping an unreaped Child calls kill_and_reap, which signals the group and root again and blocks in waitpid(..., 0). Even if D3 first polls has_exited until its deadline and records unreaped, ordinary ownership cleanup re-enters that fallback. This contradicts item 18's stop-signalling-and-settle rule and item 12/14's finite settlement obligation.

Required change: Plan an explicit platform ownership mechanism for an unreaped child at the ceiling, including Drop/unwinding, that preserves the scratch-root hold, never signals again after the ceiling, and cannot block in the fallback. Reap only after observed exit or provide a non-blocking primitive. Keep timeouts and outcomes in D3. Add a seam for a root surviving the ceiling and assert finite settlement, retained custody and no later signal/reap-block on destruction.

### D3APLAN-R1-RF-3 — Assign a normal-end path separately from the interim fault ladder

Location: `docs/implementation/m3/supervisor-d/d3a/PLAN-r1.md:82`.

LD-D3A-6 supplies one ladder for every D3a cause: control cancel, immediate TERM, KILL, reap. The only other normal-end action specified is Participant::close_input. Item 19's normal end instead sends shutdown(reason: normal), closes fd0/fd3, and waits for shutdownAck, observed exit and EOF under the normal-exit grace; expiry enters the fault ladder at T-2. Although cancellation is deferred to D3b, D3a claims clean settlement and D3-T4 now. A successful terminal must not be cancelled or killed merely because no separate normal-end path was assigned.

Required change: Explicitly place normal-end shutdown, descriptor closure, shutdownAck/exit/EOF joins and grace expiry in D3a-1, keeping the interim ladder for faults only; or revise the split and claims so clean operation waits for the unit owning that path. Add clean exit in both interleavings, nonzero exit, missing shutdownAck and no-exit grace-expiry controls with the exact control frames and process events.

### D3APLAN-R1-RF-4 — Give scratch measurement and removal a real work bound

Location: `docs/implementation/m3/supervisor-d/d3a/PLAN-r1.md:106`.

LD-D3A-12 bounds the walk by scratch bytes plus one and by item 16's process-class counts. Those counts bound processes, not filesystem entries or depth. One provider process can create many empty files or nested empty directories without crossing the byte cap. Cutting the walk off after one provider entry (or 16 tool entries) would reject lawful scratch; not cutting it off leaves work and allocation unbounded. Existing ChildScratch::remove also uses recursive remove_tree and list(dir), which collects a directory's names into an unbounded Vec, so a new bounded measuring walk alone does not establish item 20's bounded cleanup.

Required change: Specify the separate measurement and cleanup work/depth/allocation disciplines and the fate at exhaustion. Cite an actual source for filesystem work bounds or obtain the necessary lead/owner decision; do not reuse process counts as entry counts. Keep policy in D3 and pass budgets to platform mechanisms. Cover many zero-byte entries, deep directories, symlinks, retained-scratch failures and cleanup exhaustion without changing admission merely because removal failed.

### D3APLAN-R1-RF-5 — Do not omit required record fields when a code table is not yet sourced

Location: `docs/implementation/m3/supervisor-d/d3a/PLAN-r1.md:103`.

LD-D3A-10 proposes leaving an event field out until its table has a pinned source. S-OP-2 item 23 specifies required fields, including provider.process.spawned.protocol, provider.stage.changed.stage/state and provider.process.reaped.exit_class/rss_unit. Item 21 requires those events, not reduced substitutes. Also, registry-literal provenance expressly permits reviewed literal release tables; it does not require every such table to be copied from an external closed enum. Refusing to invent protocol members is sound, but silently omitting required fields is not that provenance rule.

Required change: Resolve every required event field and table in the plan or make its unresolved authority an explicit blocker to that event/unit completion. Use protocol-enum or generated-contract where applicable and reviewed registry-literal tables where authorized. Preserve the required descriptor shape, optionality, identities and units. Extend C-2 checks to compare new event descriptors with the required field inventory; do not claim a complete item 21 while required fields are absent.

### D3APLAN-R1-RF-6 — Make fixture fd1 byte-clean before replaying framed provider traffic

Location: `docs/implementation/m3/supervisor-d/d3a/PLAN-r1.md:96`.

The proposed fixture is a libtest executable invoked with arguments selecting an ignored test. Libtest itself writes its test banner/progress to stdout before the helper runs; disabling capture does not suppress those bytes. The existing D1a test source explicitly handles this at process_tests.rs:239 by searching for a D1FIX marker after libtest text. That is acceptable for D1a text reports, but D3's framed participant must reject the same prefix noise. Stripping it in the participant would violate the wire/no-translation boundary and invalidate the intended controls.

Required change: Specify a first-party test fixture entry point that writes only the intended fd1 wire bytes from process start, with controlled stderr and exit behavior. A dedicated test-support executable or harness-free entry point is permitted by item 1; an extra inventory row is not a reason to prohibit it. If retaining libtest, demonstrate a concrete pre-output dispatch/suppression mechanism. Add a raw fd1 byte-equality control and forbid filtering harness text in the participant.

### D3APLAN-R1-RF-7 — Assign item 16 tool materialization accounting and its distinct bound

Location: `docs/implementation/m3/supervisor-d/d3a/PLAN-r1.md:54`.

The D3a-2 scope lists item 16 bounds but omits the tool-materialization row: at most 32 GiB admitted candidate content plus 1 GiB working space, checked host-side before each write, as copies rather than links, with ToolScratchBound. LD-D3A-12 discusses only the two 2 GiB provider scratch limits, and the checks have no materialization-specific case. MC item 12 explicitly depends on D law's adapter scratch bound. A provider settlement walk cannot replace this host-side tool accounting or apply the provider 2 GiB limit to admitted tool content.

Required change: Allocate the host-side accounting interface and its invocation owner explicitly, including the distinct tool/provider limits, checked arithmetic before writes, whole admitted copies, ToolScratchBound and J1 projection ownership. If C3's materializer enforces it, state that seam and what D3 supplies rather than claiming the row implicitly. Add exact-bound/one-over and wrong-provider-limit controls without materializing large private fixtures.

## Non-blocking observations

**D3APLAN-R1-NBO-1 — Make the single-owner substitute for the stated CAS explicit** (`docs/implementation/m3/supervisor-d/d3a/PLAN-r1.md:81`). One loop owner, a terminal state guard, a private non-Clone settlement and a one-time take can provide exactly-once delivery. Option::take alone describes one-time consumption, not necessarily one-time construction; item 12 literally says the transition is guarded by compare-and-swap. State the construction/transition invariant and have the lead explicitly accept the single-owner equivalent, or retain the literal guard. Exercise re-entry, late events and Drop after a taken settlement.

**D3APLAN-R1-NBO-2 — Document the typed accounting and final-output handoff at the participant seam** (`docs/implementation/m3/supervisor-d/d3a/PLAN-r1.md:71`). ParticipantStep currently names status, progress and candidate count. Specify how D3 enforces TS2 aggregate payload bytes without reading provider octets itself, distinguishes boundary EOF from truncated frames, and receives a one-shot verified terminal/output capability for clean settlement, release or discard. Byte counts and opaque owned handles can preserve the no-provider-octets seam; a candidate count is not evidence that commitments recomputed. Keep the real-codec reruns in D5 and add a bad-commitment fixture gate control.

## Reviewer questions and retained decisions

**Q1 — split and ladder.** Three separately reviewed units are sensible: loop/state/joins, then ceilings, then admission gating/records. Building the neutral core ahead of real codecs is reasonable if its fixture scope and D5 reruns remain explicit. Deferring descendant sweep, user cancellation/revocation and harness integration is honest; the interim must still provide a usable clean path and finite settlement, as RF-2 and RF-3 require. The LadderUnavailable gate must prevent production use of unsupported ladders.

**Q2 — ProcessEvent and Participant.** Landing the exact already-planned ProcessEvent definition early is appropriate, with one shared definition consumed unchanged by both codecs. It adds no process-event kind or semantic translation. Keeping the participant as the only fd1 reader/fd0 writer is correct; RF-1 addresses the necessary non-blocking adapter. The supervisor must retain the EOF-after-terminal hold and append actual exit before held EOF, drain before the merged death event, and never manufacture zero-exit or deadline for another cause.

**Q3 — fixtures.** The dev-dependency-only test-fixture feature, structural release exclusion and non-debug refusal fit item 1. Its exposed construction path must remain test-only. The proposed libtest wire producer needs RF-6's correction; it cannot reuse D1a's text-marker filtering.

**Q4 — records.** Adding Project-only identity requirements for tool events is an ordinary registration using existing safe kinds, consistent with item 21; it needs renderer, correlation and drift coverage too. Refusing required fields is not an acceptable substitute for resolving their code tables (RF-5). No new SafeField kind, privacy class or sink is needed.

**Q5 — outcome join.** A typed owner-route discriminator without D9 codes is appropriate. J2 retains public projection and goldens. Preserve the table's distinction between provider behavior (including host-detected liveness/resource breaches), host I/O/spec/recheck failures, and trust-observer causes. The interrupted override applies before FinalGate admission; later signal/finalization joins remain J's.

The numeric waits stated in LD-D3A-7 match item 14, including Rust3's negotiated 5,000 ms values, TS2's separate grace, typed expiry and no configuration. The 8 GiB/250 ms sampled ceiling and provider scratch sizes are sourced, and asserted low RSS must not clear an observed breach. RF-4 concerns the invented use of process counts as filesystem work bounds, and RF-7 the missing tool bound, rather than those sourced numeric values.

A policy-free resident sampling primitive and held-descriptor filesystem mechanisms belong in platform; ceilings, work budgets and outcomes belong in D3. The control prefix-before-body reader and bound-plus-four buffer correctly address D2a's acquisition observation. Preserve partial-write offsets around ControlSession::send, since that call advances codec state before transport completion.

The proposed controls cover the main state matrix, event ordering, EOF joins, liveness-versus-progress, stderr reduction, discard, nonzero exit and cleanup noninterference. They need the additional controls identified in the findings. In particular test impossible/destructor and partial-I/O paths, not just successful polling. Fixture progress is not admitted real-codec progress, and fixture-only runs remain outside codec conformance.

## Boundaries

This is a plan review, not implementation acceptance. No compiler, Cargo, tests, builds, generators or lanes were run. Only read-only inspection, hashing, JSON parsing and Git queries were used. No network, other pane or delegation; no private 413 fixture, installation, signing key, held tree, T2 store or cache was accessed. Neither repository, worktrees nor control files were edited. Only the requested REVIEW.md and review.json were written.
