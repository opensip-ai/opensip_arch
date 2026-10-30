# LD-D1B-A r2: the confined launch's representation and its status settlement (M3-D r5 F-1), by value (D1b author, 2026-10-30)

**Status: PROPOSED.** Under R3 different-vendor review (`REQUEST-A-r2.md`, Codex gpt-6-astra/high). It takes effect
only when the coordinator records its adoption (OD-AUTO-1; LD-Q-35) in a separate receipt pinning this file's sha256.
Never edited after review; a revision is a new file.

**Why R3.** LD-Q-35 put the representation at R2 with the plan unless an SD-3 or F-1 invariant moved or was in doubt.
The R2 review (`../review/REVIEW-plan-r1.md`, D1BPLAN-R1-RF-1) found that plan r1's A3 moved F-1's `A`-plus-exec-code
row for `Ax`, and that A4 left the unsettled status's owner open. This text replaces plan r1's A1–A6. It **keeps every
F-1 row as written** and adds only what F-1 leaves unstated, each stated below as new.

**r2 answers R3 review r1** (`REVIEW-A-r1.md`, `LD-D1B-A: REQUIRED-FINDINGS`; r1 is kept unchanged):
- **LDA-R1-RF-1 and RF-2: the exec witness is withdrawn.** r1 added a `NOTE_EXEC` condition to F-1's success row, which
  changed that row and needed a lossless exec/exit join. r2 keeps F-1's success row exactly: `A` then EOF, supervision
  continues. D1a's exit source is unchanged (no added interest, no second registration). The one consequence, a launcher
  killed from outside between writing `A` and `execve`, is stated as a residual (§5) and routed by existing law. §1's
  "unchanged" list is now true; the additions are listed as such in §1a, each against the item it specializes.
- **LDA-R1-RF-3:** §5 defines the one pending state (no EOF on fd 6 yet), its bound (item 14's existing handshake
  deadline, not reset), the outcome at that bound for every pending combination, retry conditions, observation-source
  failure, `EPIPE` on fd 5 (corrected reason), and how interruption enters item 12's order.
- **LDA-R1-NBO-1:** §3 states that the exec-error class survives into the spawned settlement (`Cause::SpawnFailed`
  carries it), so the `x` branch routes host I/O through the spawned path, not only through `run_error_route`.

**What it amends, by value:** M3-D r5 (`opensip_arch/docs/implementation/m3/supervisor-d/PROPOSAL.md`, sha256
`36c26161…44db0`), section F-1, filling the slot SD-3 (`sd-3-r1/CONTRACT.md`, contract 155) leaves to D1b: "it does not
select an omitted record encoding, numeric failure-code list or public failure detail … any genuine remaining
representation gap must be published with its owner before that first consumer". No accepted byte is edited.

## 1. Unchanged (F-1 and SD-3, restated so that review can check nothing moves)
- **The order:** read the record from fd 5 and close it; (Linux: parent-death signal and `getppid` check); `RLIMIT_CORE`;
  verify the descriptor set and mark fd 6 close-on-exec; apply the profile and check it took effect; write `A`; `execve`.
- **The bound:** the record is at most 64 KiB.
- **The `A` byte:** written only after the apply and the check both succeed, and before `execve`.
- **F-1's status rows, exactly:** `A` alone then EOF → none, supervision continues; `A`, then one failure code, then EOF
  → `spawn-failed`; one failure code alone → `confinement-refused`; nothing → `confinement-refused`.
- **The refusal rule (F-4):** available but an apply step fails → refuse the launch; never run unconfined.
- **Item 22's spawn-failed route:** `DELIVERY.CLOSURE_UNSPAWNABLE` for the closure's own errors (`ENOENT`, `EACCES`,
  `ENOEXEC`); D3's existing routing sends any other spawn error to `HOST.IO_FAILURE` `host-io`
  (`supervisor_records.rs::run_error_route`). That split is a **route** within the `spawn-failed` settlement and is
  unchanged.

## 1a. Additions, each against the rule it specializes (none changes §1)
| Addition | Specializes | Scope |
|---|---|---|
| §2 record layout and checks; §3 the code bytes | F-1 steps 1 and 6 ("one failure code"), SD-3's delegated representation | the launch phase only |
| §4 completed sequences outside F-1's table → `confinement-refused` | F-1's table (which lists only well-formed sequences); F-4's refusal rule | the launch phase only |
| §5 the pending state's bound and outcome | item 14's handshake deadline (spawn to `selectAck`), not reset at launch acceptance | until fd 6's EOF; after it, item 14 applies unchanged |
| §6 no protocol byte and signal-only teardown while pending | items 12, 13 and 19's write and teardown rules | until fd 6's EOF; after it, items 12, 13 and 19 apply unchanged |
| §7 descriptors; §8 starting state | items 5 and 7 | the launcher |

## 2. New: the record (fd 5)
- **Size:** at most 65,536 bytes (64 KiB), read by the launcher to EOF; a 65,537th byte refuses with `r`.
- **Layout, in order:** the four bytes `OSL1`; one byte, the profile id (1 = `macos-provider`; no other id in a build
  without debug assertions); the target path; argc as an unsigned 16-bit **big-endian** integer, at least 1; argc argv
  strings; the profile's parameters in its fixed order, `SCRATCH`, `TARGET`, `CLOSURE_ROOT`. Each string is an unsigned
  32-bit **big-endian** length and then that many bytes, nonempty, with no NUL. Nothing follows.
- **Checks:** `argv[0]` equals the target path; `TARGET` equals the target path; every path is absolute and byte-equal
  to its `realpath` (F-1 r2). The host canonicalizes before encoding; the launcher refuses otherwise (`r` for a format
  failure, `n` for a path that is not canonical).
- **Not in the macOS record:** F-1's loader path, which the Linux profile uses (F-2, Landlock `EXECUTE`); D1b-L adds it
  with the Linux profile ids.

## 3. New: the failure codes (fd 6), one byte each
- **Before `A`:** `r` record; `n` noncanonical path; `d` descriptor set; `c` core limit; `u` a profile symbol does not
  resolve; `p` the apply returned failure; `k` the check did not return 1.
- **After `A`:** `e` `execve` failed with `ENOENT`; `a` with `EACCES`; `f` with `ENOEXEC`; `x` with any other error.
  All four are F-1's "one failure code" after `A`, so **all four settle `spawn-failed`**. The code only selects item 22's
  existing route: `e`, `a`, `f` → `DELIVERY.CLOSURE_UNSPAWNABLE`; `x` → `HOST.IO_FAILURE` `host-io`, exactly as D3 routes
  an unspawnable `posix_spawn` today. (Plan r1's `Ax` → `host-fault` is withdrawn.)
- **(r2, NBO-1) The class survives the settlement.** A confined launch has spawned, so its `spawn-failed` is a settlement,
  not a `RunError`. D3's settlement cause carries the class (`Cause::SpawnFailed(Unspawnable | HostIo)`), and its owner
  route is `ClosureUnspawnable` for `e`, `a`, `f` and `HostIo` for `x`. The `TeardownCause` stays `spawn-failed`.

## 4. New: what F-1's table does not list (completed statuses)
The host reads fd 6 to EOF and keeps at most three bytes. Any completed sequence that is not one of F-1's rows with the
codes above (`AA`, `Ap`, `pA`, `rr`, `z`, three or more bytes, and so on) settles **`confinement-refused`**. Reason: the
launch was not shown to have applied and then exec'd. It is never continued.

## 5. New: the one pending state, its bound, and observation failures
- **The pending state.** From the spawn until the host reads EOF on fd 6. There is no other: at EOF the bytes are
  classified (§1, §3, §4) and the phase settles at once.
- **Its bound.** Item 14's handshake deadline, measured from the spawn as for any provider, and **not reset** when the
  launch settles as `A` then EOF; the handshake that follows has what remains of it.
- **The outcome at the bound, for every pending combination** (nothing read, `A` read, a failure code read, or a prefix
  that is already malformed): **`confinement-refused`**, subject step `unsettled`. Reason: **the required launch was not
  established** by the bound. This is a host observation boundary, not a claim about which image ran. It is never
  `handshake-deadline`, whose route is the provider's (item 22). Item 19's ladder then kills the group and reaps, with
  signal rungs only (§6).
- **Retry, not failure.** `EAGAIN` and `EINTR` on either launch channel are retried within the bound.
- **Observation-source failure.** Any other read error on fd 6, or write error on fd 5 other than `EPIPE`, is item 22's
  `host-fault` (a host I/O failure on a channel). It is not evidence that the launcher did or did not exec.
- **`EPIPE` on fd 5.** fd 5 has no reader: the launcher closed it (as it does after reading, F-1 step 1) or has exited.
  The host stops writing and fd 6 decides, within the same bound. `EPIPE` alone shows neither that the launcher is gone
  nor that it refused.
- **Interruption and the first cause.** User cancellation, revocation and observer fail-stop enter item 12's merged
  order exactly as for an unconfined child, and the first cause wins. While the phase is pending, the teardown they start
  takes item 19's signal rungs only (§6). A completed status the host had already read before the first cause does not
  replace that cause.
- **Residual: a kill between `A` and `execve`.** The launcher does nothing between writing `A` and `execve`. If it is
  killed from outside in that window, fd 6 closes at its death, the host reads `A` then EOF, and F-1's row continues
  supervision; the child's exit is then item 13's `unexpected-exit`. At this layer that is indistinguishable from the
  provider being killed from outside immediately after `execve`, which existing law already routes the same way. F-1
  provides no exec witness, and this text adds none (r2, withdrawing r1's).

## 6. New: no protocol byte before settlement
Until fd 6 settles as `A` then EOF (the whole of §5's pending state), the host writes nothing on fd 0 or fd 3: no frame, no control `cancel` and no
in-band `Cancel`. A teardown that starts during the launch phase skips item 19's in-band rungs and goes to its signal
rungs (group TERM, then KILL, then reap). The record (fd 5) is written by the supervision loop, non-blocking, one write
per turn, and its write end closed when done.

## 7. New: descriptors
The launcher receives the class set at fds 0 to 4, fd 5 (the record's read end) and fd 6 (the status's write end), and
nothing else (`POSIX_SPAWN_CLOEXEC_DEFAULT`). After closing fd 5 it requires exactly 0 to 4 and 6 open, by `F_GETFD`
over the descriptor table (D1-T5's method), and marks fd 6 close-on-exec, else `d`.

## 8. New: the launcher leaves the target's starting state as D1a set it (item 7)
The launcher changes no signal disposition or mask, no environment variable, and no working directory between its own
start and `execve`; D1a's spawn attributes (`SETSIGDEF` over every signal, an empty mask) therefore reach the target.
In particular a runtime that ignores `SIGPIPE` before user code (the Rust standard runtime does) is not used: the
launcher's entry point bypasses it (D1BPLAN-R1-RF-2). Its only state changes are F-1's: fd 5 closed, fd 6
close-on-exec, `RLIMIT_CORE` 0, the profile.

## 9. Consequences
- **Public surface:** none. `spawn-failed`'s routes are item 22's; `confinement-refused` is D1B-S's row 60.
- **D3:** a settlement cause `confinement-refused` (already in the registry's `TeardownCause`) and the launch phase.
- **D1a:** its spawn gains the confined form (the launcher, slots 5 and 6); its exit source is unchanged.
- **D1B-S** names its `<step>` subjects from §3–§5: `record`, `noncanonical`, `descriptors`, `core-limit`, `symbol`,
  `apply`, `check`, `no-status` (nothing then EOF), `unsettled` (§5: the bound reached while pending), `malformed`
  (§4: a completed sequence outside the table).

## 10. Questions for the reviewer
1. With the exec witness withdrawn, does any of §2–§8 still move an F-1 or SD-3 invariant (§1)?
2. §5: is the pending state's bound and outcome complete, and is the `A`-to-`execve` residual acceptable as stated?
