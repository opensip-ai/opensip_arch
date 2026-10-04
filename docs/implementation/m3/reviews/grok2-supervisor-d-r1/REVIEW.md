# GROK2 review: M3-D r1, supervisor and common control

**Verdict: REQUIRED-FINDINGS.**

Subject: `docs/implementation/m3/supervisor-d/PROPOSAL.md`, 128473 bytes, sha256 `c6ae10de47ede503ceebdbcd6407b0df0e650f1fe9627ef91e4bec1fd6fa7dfa`. Single reviewer. Law review, not a design-unit or code-unit review. No product cargo, tests, probes, CF-P, Seatbelt, or Landlock. `~/Library/Application Support/OpenSIP` was absent.

CF-P has not run. That is the acceptance gate (M3P:85, M3P:213, M3P:261). It is not a finding. An ACCEPT on this round would have meant accept subject to r2 recording CF-P's outcome with no other change. These findings are other changes. r2 still records CF-P.

## Required findings

### RF-1. The macOS Guaranteed cell and the descendant snapshot over-claim

Item 18's Guaranteed cell says every process in the child's group at the group `SIGKILL` is killed, and that the root is reaped. The escalation paragraph of the same item records `exit: unreaped` when the root is still alive at the reap ceiling, and the host then stops signalling. Linux records `tree: incomplete` for an uninterruptible wait. The macOS cell does not. The `proc_listpids(PROC_PGRP_ONLY)` confirm has no stated result when it fails or the group is not empty.

`proc_listchildpids` (SDK27 `usr/include/libproc.h:95`) takes one parent pid and a flat buffer. The law says the host snapshots the live descendant tree with that call and never says to call it on each returned pid. A grandchild is not a direct child of the root. After `setsid` it is also outside the group, so the group kill does not take it. D5-T2 expects the snapshot path to kill that grandchild. The Not guaranteed row does not list it. Row (c) covers a process created after the snapshot by an already escaped process. A process still in the group can fork and `setsid` in the window after the snapshot and before the group `SIGKILL`.

The Consequence row is the right settlement claim: macOS tree settlement is not claimed, and the report is `tree: group-killed, platform-limited`. The Linux sweep stays conditional on LX-7 and LX-8 and discloses `tree: incomplete`. That half is sound.

Fix: carve survivors of the reap ceiling out of Guaranteed; state the confirm's failure result; walk `proc_listchildpids` recursively; put the in-group fork-and-`setsid` window on the Not guaranteed row or close it.

### RF-2. The pre-spawn closure recheck is sent through NE:3529

Item 22 maps every `spawn-refused` settlement to `operational-failed` 4 and `PROVIDER.PROTOCOL_VIOLATION`, as a capability or identity mismatch before any stage (NE:3529). NE:3529 is HelloAck identity, OpenUniverse before negotiation, coverage faults, and worker fault. Item 26's closure recheck is the session factory comparing bytes before any provider frame. WS:1375 and J1 r1 row 28 (`PROPOSAL-r1.md:511`) map corrupt or unspawnable closure bytes to `HOST.IO_FAILURE` and `DELIVERY.CLOSURE_BYTES_CORRUPT` / `DELIVERY.CLOSURE_UNSPAWNABLE`. The `spawn-failed` row already chooses WS:1375 over DLV:1170. That choice stands. The recheck is the corrupt-bytes half of the same cell.

Fix: closure recheck takes J1 row 28. HelloAck, an in-protocol RF3 echo, and `effectRequest` stay on `PROVIDER.PROTOCOL_VIOLATION`. A tuple mismatch the provider has not spoken is a host-side row.

### RF-3. Revocation and fail-stop share one public route

Item 19 puts both trust-observer revocation and fail-stop on settlement cause `revoked`. Item 22 routes that cause to SL:1311, `OBSERVER.FAIL_STOP`. SL:1311 is fail-stop and I/O failure: `operational-failed` 4, `HOST.IO_FAILURE`. SL:1306 is revoked-during-operation: `request-rejected` 2, `EXTENSION.ADMISSION_REJECTED`. J1 r1 row 18 is revocation (`TRUST.COMPONENT_REVOKED_DURING_OPERATION`). Row 19 is fail-stop (`OBSERVER.FAIL_STOP`). The S6 kill ladder can still cover both. The public code cannot.

Fix: split the cause. Revocation takes row 18 and SL:1306. Fail-stop takes row 19 and SL:1311.

### RF-4. C4a is after the ExecutionId draw

Line 9 says items 24–26 are DR-G29 refusals with no ExecutionId. Item 24 places manifest-class refusals inside C4a Plan construction, before attempt admission, and concludes that no ExecutionId is minted. D4-T1 watches the attempt-admission counter.

J1 r1 draws the ExecutionId at `CommitSession::open` (R12, J-γ), before capture and before the Plan (`PROPOSAL-r1.md:241`, `:274-276`, `:344-345`). J-ε is C4a. Phase A, which J1 calls before attempt admission, includes the whole analysis and ends at the attempt row (`PROPOSAL-r1.md:131`, `:403`). WS:81 gives each admitted attempt a fresh ExecutionId; it does not draw that id at the attempt row. REG:374 and QG:588 require admission-time excluded forms to be refused with no ExecutionId, and separately require post-admission substitutions to be rejected before any stage. Item 26 already follows the second rule. Item 25 can still sit in request validation before R12.

Fix: run EE-1, EE-3b, the manifest part of EE-4, and EE-5a before R12. Point D4-T1 at `CommitSession::open`. Leave item 26 after the draw. Narrow line 9 so it does not cover item 26.

### RF-5. F-8 omits two Linux facts section F uses

The law says each Linux fact it relies on is an LX id and is not established. F-2 applies `PR_SET_NO_NEW_PRIVS` before Landlock and seccomp. F-4 probes Landlock ABI, seccomp filter mode, and `no_new_privs`. LX-10 is the Landlock ABI. LX-14 is seccomp arguments for `clone` flags and the `clone3` fallback. Filter-mode availability and `PR_SET_NO_NEW_PRIVS` have no row, so the CF-P desk check does not include them.

Fix: add those rows and cite them from F-2 and F-4.

## Decided, not findings

- **R2.** Counting stderr into K7 `{bytes, truncated}` matches the only lawful M3 consumer. OPP:171's hold and draft ML item 12.1 differ in retention only. See NBO-1.
- **R3.** The EOF-then-exit hold is a host join (F02:171-177; CPC's EOF and process-death join). It is not a reorder of semantic frames (F02:168-169).
- **R4.** The 1 GiB TS2 aggregate is host-only, has no wire member, and follows the DLV:1163 wall-clock mapping.
- **R5, the other half.** `spawn-failed` correctly prefers WS:1375 to DLV:1170.
- **R7.** Item 23 agrees with HD §9.3 on the leaf, nested subreapers, the no-leaf drain, and macOS.
- **R8, apart from RF-5.** Ordinary items do not depend on O7. F-4's disclose-versus-refuse split matches the recommendation. F-7 is the three plan controls plus process creation and the tool-tree residual. No sandbox claim.
- **EE-3b.** Represented as an analyzer command or a capability outside the provider matrix. The manifest shape also requires `permissions` and other objects. No schema body was found in which those objects claim the EE-3b powers, so this is not a finding.
- **Citations checked and matching for the rows above:** CC:9-11 (sixteen message types; CC:171 is a replay command, not the inventory); CPC descriptor layout and the EOF join; DLV:1133; NE:3529 and NE:3837-3850; SL:1306 and SL:1311; WS:81 and WS:1375; REG:374; QG:588; J1 r1's pipeline and rows 18, 19, and 28; OPP:171 and OPP:401; S-OP-2 r4 K7; HD:844-910; SDK27 `libproc.h:95`.

## Pin drift

Judged against the pinned bytes. The subject hash matches. The subject is tracked at arch `839018434`; the request said it was untracked until acceptance. Live M3-E1 and the overnight log have moved. Overnight line 9 is still B1 / O7. Details are NBO-7 in `review.json`.
