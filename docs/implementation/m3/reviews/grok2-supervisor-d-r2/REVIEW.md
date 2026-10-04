# GROK2 review: M3-D r2, supervisor and common control

**Verdict: REQUIRED-FINDINGS.**

Subject: `docs/implementation/m3/supervisor-d/PROPOSAL.md`, 167305 bytes, sha256 `1f5367dc8fffe9410338fce5dcabd41f7b3b331e39cfd0ad3ef8ced4c964bab8`. r1 bytes are `PROPOSAL-r1.md`, 128473 bytes, sha256 `c6ae10de47ede503ceebdbcd6407b0df0e650f1fe9627ef91e4bec1fd6fa7dfa`. Single reviewer. Law review, not a design-unit or code-unit review. No product cargo, tests, probes, CF-P, Seatbelt, or Landlock. `~/Library/Application Support/OpenSIP` was absent.

CF-P's record matches its pin (40007 bytes, sha256 `6323a1b4df5a35ebb9b206466692d09f1ea477b37365b5179693e526c1352672`). The acceptance gate is met. Accepting r2 would accept D. This round has one remaining finding, so r2 is not accepted.

## Required findings

### RF-1. Four sentences still forbid the first-use prelude reservation

Item 24's decision paragraph and D4-T1 are the right reading of accepted J1 r3. R10a sits after R10's trust read and before R11 and R12, so the durable analysis attempt's ExecutionId, drawn at `CommitSession::open`, does not exist yet (J1:309-311, J1:162, J1:172). On first use, `mint_intent` has already reserved the creation prelude's ExecutionId, and that id names the creation act only (J1:161, J1:172). A refusal at R10a creates no analysis-attempt reservation. D4-T1 checks that the reservation set after the refusal equals the set at R10a's entry: empty, or the prelude's alone. REG:374 and QG:588 say admission-time excluded forms are refused with no ExecutionId. Read against J1, that is no analysis-attempt id.

Four sentences in the same law say something stronger, and they make that lawful first-use refusal a forbidden substitute:

- Line 9 assigns items 24 and 25 the property "refused before any ExecutionId is drawn or reserved". Item 25, at R1, is before `mint_intent` (J1:300). Item 24 is not, on first use.
- Line 696 heads item 24 as "Manifest-class refusals before any ExecutionId is drawn".
- Line 730 lists "an ExecutionId drawn or reserved before these checks" as a forbidden substitute for those checks.
- Line 1168, rewritten in r2, forbids "an excluded form admitted silently, or refused after an ExecutionId is drawn or reserved".

The first-use refusal happens after an ExecutionId has been drawn and reserved. An implementer who follows the forbidden-substitutes list treats D4-T1's prelude-only set as a violation.

Fix: state the prohibition as no analysis-attempt ExecutionId, and keep the prelude reservation as the exception the decision paragraph and D4-T1 already state. Change line 9, the item 24 heading, line 730, and line 1168. Leave item 25 absolute. Leave R10a where it is. Do not bind the prelude id to the analysis attempt.

## Prior findings

- **r1 RF-1, resolved.** The Guaranteed cell sends `SIGKILL` to every current group member, never signals a recycled group id, and records `tree: group-killed` only when `proc_listpids(PROC_PGRP_ONLY)` lists the zombie root alone. A survivor of the reap ceiling is outside the cell: `exit: unreaped` for the root, `tree: incomplete` for a member. The snapshot walks `proc_listchildpids` recursively and retries a full buffer. Not guaranteed (b) is the in-group fork-and-`setsid` window. D5-T2 is best effort, D5-T2b is the window, and D5-T2c is the confirm, including `killpg` `EPERM` (CFP:228). The missing root-alive assertion in D5-T2c is NBO-1.
- **r1 RF-2, resolved.** `closure-recheck-failed` takes J1 r3 row 28 with `DELIVERY.CLOSURE_BYTES_CORRUPT`. `spawn-failed` stays on that row with `DELIVERY.CLOSURE_UNSPAWNABLE`. `session-spec-inconsistent` takes NE:3573's host-invariant route, spelled as row 2's route (`SYSTEM.OUTCOME.ILLEGAL_STATE`, detail absent). Provider-spoken mismatches stay on row 30 (NE:3529).
- **r1 RF-3, resolved.** `revoked` takes row 18 and SL:1306. `observer-fail-stop` takes row 19 and SL:1311. Both keep the S6 kill ladder.
- **r1 RF-4, partly resolved.** R10a, the prelude distinction, the registry proof, the ephemeral placement, item 26's post-draw scope, and SD-6 as its own amendment are sound. The absolute sentences above are the remainder, and they are this round's RF-1.
- **r1 RF-5, resolved.** LX-15 through LX-22 cover the Linux facts the law relies on, each marked partly or not in CF-P. No row is established until a Linux lane runs it. F-1, F-2, F-4, and the ordinary Linux citations point at those rows.

## Decided, not findings

- **R6, the placement.** R10a is a sound pre-draw row against J1's durable order. The ephemeral path runs it after X4T's report-only admission and before the ephemeral draw, and E-3 admits nothing when there is no trust view. SD-6, reviewed on its own, is the right vehicle for amending accepted J1. D4 waits for that acceptance. MC r5 row 8 is narrowed only as a record for M3-C's next revision.
- **R8.** Section F remains an O7 placeholder, binding only once O7 is decided as recommended. Overnight line 9 is still B1. Items 1-27 do not depend on the confinement primitive. Conditional mentions ("under O7", `confinement-refused` only under O7) stay conditional. No ordinary item claims confinement is enforced.
- **R9.** The MX table matches the record: MX-5 adopts the `kern.procargs` deny, parameters are `realpath`-canonical, `file-link` is by name, the symbol comes from `dlsym`, and neither `sandbox_init` mode is used. F-1's status pipe gains the applied byte because `errno` stays 0 and the library writes fd 2. Item 6's fresh empty copy-only scratch answers MX-3. Item 7's `RLIMIT_CORE` of 1 on Linux matches the desk check. Item 4 uses syscall 434 and `P_PIDFD` 3 on glibc 2.34. LX-10's kernel list matches the record. F8's network-namespace drop is the desk check, and the law does not call it a measurement. G1 records the gate as met and does not adopt CF-P's "enforces, on a trivial child" as a D claim.
- **Routes checked against the cited lines.** J1 r3 rows 2, 18, 19, 28, and 30 (J1:617, :633, :634, :643, :645). WS:1375. NE:3573 and NE:3529. SL:1306 and SL:1311. X4:120 and X4:121. REG:374. QG:588.

## Non-blocking observations

- **NBO-1.** D5-T2c does not assert `exit: unreaped` for a root still alive at the reap ceiling. The Guaranteed cell and the escalation sentence already do.
- **NBO-2.** Item 6 states that `/var/tmp` is on disk on both distributions. LX-5 says that fact is not in CF-P. The reason for leaving AL2023 `/tmp` is the measured tmpfs limit (CFP:282).
- **NBO-3.** D4-T1's census bullet observes the durable session draw only (J1:179, J1:428). Registry equality is the assertion that covers the ephemeral and render draws.
- **NBO-4.** The live overnight log is 19975 bytes, sha256 `a32ce9f15130715a45d4878ed0929ec4763dc25b985b1ac0cd3e12c205bda210`. The pin is 19018 bytes, sha256 `20044dcc42406468dedae591bed5aa4c12ca769111c8bc63a47f5ea677267d05`. Line 9 is still B1. The law cites the entry.
