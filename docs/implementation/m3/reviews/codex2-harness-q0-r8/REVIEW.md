# CODEX2 — M3-Q0 r8 review

**Verdict: REQUIRED-FINDINGS. Five required findings; two non-blocking observations.**

QD-30 makes C2-Q0-R6-01 moot by withdrawing the event-channel mechanism. The replacement still permits incomplete inventory and incorrect image counters, and its failure and split-batch paths conflict with the retained measurement rules.

## Subjects and scope

| Subject | Bytes | SHA-256 |
|---|---:|---|
| `docs/implementation/m3/harness/DESIGN.md` | 120918 | `c958fdabce364316773b7238a98a6b2de118355f95f65872bd0c8e3a6dba89a8` |
| `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json` | 57369 | `cc6f3cb842b65fc1b7b2802a1769ade3d712e593578ee2dcfae4b17753b57ea4` |

Hashes match REQUEST.md. The retained r7 DESIGN/schema hashes also match the revision metadata. All ten DESIGN diff hunks and the schema changes fit the r8 table and associated metadata/preregistration/index changes. No unrelated scope change was found. r7 was not treated as an accepted review.

## Required findings

### C2-Q0-R8-01 — Cover creation paths that suppress automatic attachment (P1)

Locations: [DESIGN:769](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:769), :782, :791–797.

The structural proof assumes every descendant of a traced task automatically attaches. Linux explicitly skips trace-event selection for `CLONE_UNTRACED`; the listed ptrace options do not override that path. ([Linux fork source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/fork.c), [child ptrace initialization](https://raw.githubusercontent.com/torvalds/linux/v6.18/include/linux/ptrace.h))

A traced parent can create a child with `CLONE_UNTRACED | SIGCHLD`. That child can allocate a brief peak and exit without exec, so the exec-only filter observes nothing. It can also disappear between cgroup checks. All **known** tracees finish with successful reads, but the child's counter is absent. Containment sampling does not prove it never existed.

**Required:** establish an admission or observation rule covering attachment-suppressing creation paths, including clone/clone3, and reliably mark unsupported births `untraced-process`/incomplete. Automatic attachment alone is not that rule. Add the short-lived, no-exec child case; it must never be complete with its counter omitted.

### C2-Q0-R8-02 — An exec-entry read is not the old image's final counter (P1)

Locations: [DESIGN:782](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:782), :783–786, :794, :833–835.

Seccomp stops before the exec syscall body. Linux subsequently reads/copies argv and env strings from the old address space, then replaces that address space before the EXEC stop. ([Linux exec source](https://raw.githubusercontent.com/torvalds/linux/v6.18/fs/exec.c), `copy_strings`, `begin_new_exec`, `exec_mmap` and `PTRACE_EVENT_EXEC`)

Consider a single-threaded process whose valid argument strings are in nonresident file-backed mapped pages. The entry `VmHWM` read succeeds. Kernel argument copying then faults those old-image pages, increasing its high-water after the read. Successful exec discards the old mm; there is no old-thread EXIT stop, and the subsequent EXEC stop sees the new image. Every stated structural condition can pass with an understated counter. A periodic concurrent sample need not capture that interval.

**Required:** obtain a validated terminal counter covering the old image through retirement, or report `own-counter-missing`/incomplete for transitions whose final value is unavailable. An entry snapshot alone cannot close the image. Add a calibration case in which exec itself first faults the argument pages.

### C2-Q0-R8-03 — Shared-mm history is not a new child's own peak (P2)

Locations: [DESIGN:779](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:779), :782–786; withdrawal table at :53.

`CLONE_VM` retains the same mm, and `VmHWM` reports that mm's historical high-water. A distinct TGID does not give it a fresh history. ([Linux clone memory handling](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/fork.c), `copy_mm`; [VmHWM source](https://raw.githubusercontent.com/torvalds/linux/v6.18/fs/proc/task_mmu.c), `task_mem`)

A parent peaks at 100 MiB, releases most memory, then vforks/posix_spawns a child that immediately execs. The child's pre-exec read still carries the parent's earlier 100 MiB, from before the child existed. Summing that segment and the parent's segment counts the history twice. All reads and stops can succeed, so this is an incorrect metric rather than lost evidence. r7 explicitly exempted the shared pre-exec segment; r8 removed that ownership rule.

**Required:** restore the justified shared-mm/pre-exec exception or specify a correct own-counter ownership source. Unsupported sharing must be incomplete. Calibrate a parent peak **before** vfork and verify that it is not counted again for the child.

### C2-Q0-R8-04 — Failed attachment/detachment changes execution (P2)

Locations: [DESIGN:763](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:763), :765–768, :795, :801, :880–881, :926–927.

The root installs its exec-trace filter before SEIZE. With no tracer, `SECCOMP_RET_TRACE` returns `ENOSYS` without executing the syscall. ([Kernel seccomp documentation](https://docs.kernel.org/userspace-api/seccomp_filter.html))

Thus a failed attachment cannot simply continue the root untraced into the measured binary as :801 promises. The filter blocks that first exec. Controlled detachment similarly changes future exec outcomes, as :795 acknowledges. Yet `tracer-unavailable` and `tracer-failed` retain elapsed and (a), and the unavailable reference case expressly rejects null elapsed. Those samples can describe failed bootstrap or altered execution rather than the requested workload.

**Required:** define a filter-free untraced path before irreversible filter installation, or classify the affected execution as failed and apply null-all handling. For controlled failure, specify tracee cleanup and distinguish a measurement failure from one that changes workload execution. Preserve the failed slot; do not silently replace it. Calibrate forced attachment failure after setup and detachment before a required exec. Retained values are valid only when the intended execution remains valid.

### C2-Q0-R8-05 — Split batches need distinct identities and pairing rules (P2)

Locations: [DESIGN:812](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:812), :888–902; [ENV:5](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:5), :1406–1410, :1458–1498, :1594–1598.

QD-31 requires separate physical timing and RSS batches. The retained canonical `batchId` tuple has round, workload, workflow, reset, control and retry ordinal, but no measurement role. Both first batches have the same tuple and ID. Their separate operational records therefore collide on `(batchId, slot)`. Using ordinal 2 for RSS consumes the retry ordinal and makes the traced RSS batch the highest-ordinal final verdict. One envelope has one `roundId`, so round cannot distinguish the pair here.

The new `rssBatchId` check only names a Q6 batch with the same configuration. It does not establish distinct roles, same retry attempt, slot provenance, RSS failure propagation or which values/status drive the final result. It also does not resolve the identical IDs.

**Required:** separate measurement role from retry ordinal in identity/carriers, and define the physical pair's evidence, reset/priming, per-slot sample sources, incompleteness propagation and finality. Update schema, validator and reference cases together. Cover first/retry pairs, reject self/wrong-role/wrong-ordinal links, and show that RSS failure retains valid untraced elapsed while making the paired result incomplete.

## Answers to the remaining checks

- **Ordinary attachment and takeover:** initial child stops and option inheritance support the ordinary traced paths. `GETEVENTMSG` is the correct former-TID basis for non-leader exec bookkeeping. These facts do not repair R8-01 or the final-counter gap. ([ptrace documentation](https://man7.org/linux/man-pages/man2/ptrace.2.html))
- **Early leader:** reading the exiting worker's task entry is sound under the ptrace lifecycle. The zombie leader remains unreapable while subthreads remain, retaining the lookup anchor; this does not warrant another rejection finding. ([Linux exit source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/exit.c), `wait_consider_task`; [proc task lookup](https://raw.githubusercontent.com/torvalds/linux/v6.18/fs/proc/base.c))
- **Tracer death and Yama:** EXITKILL and the parent's `tracer-died`/null-all path are sound for attached tasks. Scope-dependent availability is reasonable; the untraced continuation needs R8-04. ([Linux tracer-exit source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/ptrace.c), `exit_ptrace`)
- **O7:** no independent weakening was found in the specified tracer, which does not rewrite syscalls or state. Seccomp precedence preserves denials; the outside-domain Landlock direction is supported. This is compatibility design/calibration, not acceptance of the still-pending owner decision or D-law launch prerequisites at M3-PLAN:308–345. ([Kernel seccomp documentation](https://docs.kernel.org/userspace-api/seccomp_filter.html), [Landlock ptrace restrictions](https://docs.kernel.org/userspace-api/landlock.html))
- **Timing:** measuring overhead and fixing the selection rule before measurement is reasonable. R8-04 and R8-05 block the stated failure/split paths.
- **Earlier findings:** C2-Q0-R6-01 is moot because its mechanism was withdrawn. Combined-mode batch/slot joins and the per-quantity iff rule remain. Split batches need R8-05; changed execution needs R8-04's appropriate nulling. The exact host key, compatible namespaces, retained unresolved values and rule that host values cannot replace missing counters remain at :821–826.

## Non-blocking observations

**C2-Q0-R8-N01:** make the stop classifier explicit (:774–776,:788–790). Auto-attach `EVENT_STOP/SIGTRAP` resumes without injecting a signal; actual job-control stops use LISTEN; genuine signal-delivery stops reinject their signal. GETEVENTMSG supplies a child TID rather than clone flags, so obtain actual thread-group membership at the stop. The stated approach is implementable with those distinctions. ([ptrace documentation](https://man7.org/linux/man-pages/man2/ptrace.2.html))

**C2-Q0-R8-N02:** pin the spread statistic, pairing/order, workload aggregation and both selector inputs for QD-31 (:554,:810–814). Overhead ppm and selected mode alone cannot reproduce the spread predicate. The already-required preregistration can supply this detail.

## Verification limits

These counterexamples are static inferences from the specified rules and primary Linux sources, not executed experiments. D12 calibration remains required; passing the listed fixtures alone would not establish the omitted cases.

No product code, tests, builds, validators, reference implementations, corpus fetches or benchmarks were run. No runtime home was accessed and no commit was created. Only REVIEW.md and review.json were written in the requested r8 temporary directory.
