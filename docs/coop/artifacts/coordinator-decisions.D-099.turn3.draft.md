# D-099 — D-006 fleet-class successor plus G03/G04 named identifiers

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 turn 3 of 3. Same cycle as turns 1 and 2.
> Frozen turn-1 and turn-2 subjects are not edited. Not a
> fourth turn of D-098. Not a SATISFIED re-record.
> **Decision type:** PREFERENCE-LADEN scoped D-006 successor
> plus RULE-GOVERNED naming of the v3 reserved identifiers.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** execute G03 or G04. **Does not** claim
> QUALIFIED or DEMONSTRATED. **Does not** change D-006
> numeric threshold numerals. **Does not** restore G17.
> **Does not** name G13. **Does not** silently substitute
> Rosetta. **Does not** overturn D-094 or D-098 CONTESTED,
> D-096, or D-097.

Turn-1 subject `coordinator-decisions.D-099.draft.md`
`458dae40f8c77b7986ba4287448a4aa4ffdbcaccd6864d1612b97d6cd1afda08`
held frozen. Turn-2 subject
`coordinator-decisions.D-099.turn2.draft.md`
`4e34c7f0c16a1c7c761405504c8294e4152a5eddd470a559a47dbd933f61832c`
held frozen. Claude 2 OBJECT, 1 MUST-FIX D099-T2-MF-1,
0 SHOULD-FIX, 1 NOTE D099-T2-N-1. Codex OBJECTIONS,
0 MUST-FIX, 2 SHOULD-FIX ADV-D099-T2-01 / ADV-D099-T2-02.

| ID | Sev | Disposition |
|---|---|---|
| D099-T2-MF-1 | MUST-FIX | ACCEPTED. This table carries only this cycle's dispatch inputs, each label unique. |
| ADV-D099-T2-02 | SHOULD-FIX | ACCEPTED. Same table repair. No historical D-098 pin block. |
| ADV-D099-T2-01 | SHOULD-FIX | ACCEPTED. Preflight uses a dedicated stopped-after-exec launch of the digest-pinned thin target. Linux process ABI is `/proc/T/auxv` AT_PLATFORM, not `file` of the executable. macOS translation is T's `kinfo_proc` `P_TRANSLATED` after exec, not parent `sysctl.proc_translated`. |
| D099-T2-N-1 | NOTE | ACCEPTED. The macOS translation field is named below. |

D-098 is CONTESTED at `09d0e288509f8b3e58d035290ff26f2e1d29c4ce`.
This is a new cycle. The contract lives in this file's bytes.

## Scoped D-006 successor

Exact-machine / exact-OS superseded **for G03 and G04
only**. Numerals stand. The 10% rule stands and **activates
from the second qualified release** (D-006). Analyze RSS
and doctor-with-consented-probes RSS remain outside D-006.

## Per-platform class trade

| Platform | D-006 class | This fleet class | Effect |
|---|---|---|---|
| macos-arm64 | M1-class, 8 GB | `macos-15`, 3-core M1, 7 GB, 14 GB SSD, arm64 | Stricter. Accepted. |
| macos-x86_64 | native Intel-class | `macos-15-intel`, 4 CPU, 14 GB, 14 GB SSD, native Intel VM, UDID `4203018E-580F-C1B5-9525-B745CECA79EB` | OBS-T3-02. Accepted. |
| linux-x86_64 | 4 vCPU / 8 GB | `ubuntu-24.04`, 4 CPU, 16 GB, 14 GB SSD, x64, public-repo | Extra RAM is not a license to grow. Accepted. |
| linux-arm64 | 4 vCPU / 8 GB | `ubuntu-24.04-arm`, 4 CPU, 16 GB, 14 GB SSD, arm64, public-repo | Same. Accepted. |

Warrant: D-000 PREFERENCE-LADEN, same class as D-006.
OBS-T3-02 is the Intel reason, not the sole warrant.
Source: GitHub hosted-runners public table, 2026-08-14.
`macos-26-intel` is not this class. Private 2 CPU / 8 GB
is not this class.

## Hosted-fleet-class measurement contract

**Pinned object.** Fleet class = workflow label + documented
public-repo CPU/RAM/storage/arch row. New VM per job.
Labels are not one machine.

**Governed series (G03).** For each platform, each command
in {`--help`, `--version`}, each state in {cold, warm}:
one scalar latency series. N=21 accepted jobs. Estimator:
nearest-rank, rank = ceil(p × N) → p50=11, p95=20, p99=21.
Invalid jobs replaced, not counted.

**Governed series (G04).** For each platform, each command
in {`--help`, `--version`, `doctor` read-only}, each of
{steady baseline RSS, peak RSS}: one series of 21 samples.
Cold/warm applies to `--help` and `--version` RSS the same
way as G03. `doctor` read-only is one launch per sample
(no warm pair). Analyze and consented-probe RSS remain
excluded. Absolute numerals: **every** accepted sample must
be ≤ the D-006 bound (help/version 40/50 MB; doctor
read-only 60/100 MB).

**First qualified release, per accepted VM, G03/G04
help/version.** For each command C in {`--help`, `--version`}
in recorded order:

1. purge (`sudo purge` / `sync && echo 3 | sudo tee
   /proc/sys/vm/drop_caches`)
2. cold C of the **candidate** (first exec after that purge)
3. warm C of the **candidate** immediately; no other
   command or binary intervenes

Then, for G04 only, one `doctor` read-only launch (no
purge-warm pair). Record order.

**Second-or-later release, per accepted VM.** Previous
qualified binary P (digest-pinned) and candidate C.
Randomize {P,C} order; record it. For each command X in
{`--help`, `--version`}:

1. purge
2. cold X of first binary
3. warm X of first binary immediately
4. purge
5. cold X of second binary
6. warm X of second binary immediately

Then G04 `doctor` read-only of first binary, then of
second, recorded order matching {P,C}. No intervening
other command inside a cold/warm pair. 21 accepted
**matched pairs** per governed series.

**Paired 10% formula (second release onward).** Operative
G03 quantities are **only** D-006's five: cold p50, cold
p95, cold p99, warm p95, warm p99. Warm p50 may be
recorded as telemetry and **must not** fail qualification.
For each operative G03 quantity: compute that rank of the
21 candidate samples and of the 21 previous samples on
the **same** 21 current VMs. Require
candidate_p / previous_p ≤ 1.10 (previous_p > 0). For each G04 series: compute the median
of the 21 candidate samples and of the 21 previous
samples on those VMs; require candidate_median /
previous_median ≤ 1.10. No pooling across commands or
metrics. If P cannot execute on the current class, do not
auto-rebaseline: open a reviewed successor or use D-006's
full waiver. Weekly image rolls do **not** suppress this
rule. Sameness of image/brand is **within each pair** on
that VM; the 21 VMs may mix weekly images as paired
strata.

**Thin-only scope.** Thin, single-architecture artifacts
only, and only for the digest-pinned **measurement
projection** used as G03/G04 evidence (the on-disk path P
whose sha256 is D below). Fat/universal images fail
preflight. A later shipped fat product artifact cannot be
that projection without a reviewed successor. This entry
does not forbid a future fat ship; it forbids using one as
G03/G04 evidence.

**Preflight (every job; fail-closed).** Architecture
observation is a **dedicated** launch of the same P+D.
It is never a G03/G04 timing sample. After the fields
below are recorded the preflight child is `SIGKILL`ed
and reaped. Timing samples of the same P+D then proceed
without ptrace or suspend. If P or D changes, preflight
re-runs.

Shared, before spawn:

1. label: record the measurement manifest `runs-on`
   literal; must equal the class label
2. Record absolute path P and `sha256(P)=D`. Reject if
   `file` of P (and `lipo -info` on macOS) shows more
   than one slice.
3. Host arch H = `uname -m`. Executable arch E = `file`
   of the on-disk thin path P (one slice). E is **not**
   the process-ABI field.
4. CPU count: `sysctl -n hw.ncpu` / `nproc`; macos-arm64=3;
   others=4
5. RAM: macos `sysctl -n hw.memsize` bytes; Linux
   `MemTotal` kB × 1024. GiB = bytes/1024³. Match 7/14/16
   ±0.75 GiB
6. storage: **audit-only**. Record `df -k /` 1024-byte
   blocks field (second column) × 1024. Never fail the
   job on this field
7. OS family: macos `sw_vers -productVersion` major=15;
   Linux `/etc/os-release` `VERSION_ID=24.04`
8. CPU brand: macos `sysctl -n machdep.cpu.brand_string`;
   Linux `/proc/cpuinfo` `model name`. Recorded stratum
9. image version: record the GitHub Actions `Set up job`
   image version / `ImageVersion` (not `RUNNER_TRACKING_ID`)

**Linux target-process protocol (item 10).**

1. Parent `fork()`. Record child PID T immediately.
2. Parent reads `/proc/T/stat` field 22 (starttime) as S0.
   Unreadable → `SIGKILL`, reject.
3. Child: `ptrace(PTRACE_TRACEME, 0, 0, 0)` then
   `execve(P, argv_preflight, env)`. `argv_preflight` may
   be `[P, "--help"]`. This launch is not timed.
4. Parent `waitpid(T, …)` until exec-stop (`WIFSTOPPED`
   and `SIGTRAP` from `PTRACE_O_TRACEEXEC` / TRAPeme).
   That wait **is** the exec-completion handshake. If
   `waitpid` returns exited or signaled before that stop,
   reject.
5. Parent re-reads starttime as S1. If S1 ≠ S0 or T is
   not live, reject (PID reuse).
6. Parent opens `/proc/T/exe` `O_RDONLY` and sha256s that
   fd. Must equal D. This is post-exec executable
   identity, not process ABI.
7. Parent reads `/proc/T/auxv` and takes `AT_PLATFORM`.
   This is the **process ABI** field. Accepted values:
   class `ubuntu-24.04` → `x86_64`; class
   `ubuntu-24.04-arm` → `aarch64`. Missing `AT_PLATFORM`,
   unreadable auxv, or any other value → reject.
   `AT_BASE_PLATFORM` is audit-only.
8. `file` of `/proc/T/exe` is **not** counted as process
   ABI. Never `/proc/self/exe` of the parent. H, E, and
   `AT_PLATFORM` must all match the class.
9. Parent `kill(T, SIGKILL)` and `waitpid`. Discard this
   launch.

**macOS target-process protocol (item 10).**

1. Parent `posix_spawnattr_setflags(POSIX_SPAWN_START_SUSPENDED)`
   and `posix_spawnattr_setarchpref_np` to exactly one
   CPU type: `CPU_TYPE_ARM64` for `macos-15`,
   `CPU_TYPE_X86_64` for `macos-15-intel`. Close-match
   fallback (`arch(1)` trying a near arch) is forbidden.
   Spawn failure → reject.
2. `posix_spawn` of P with `argv_preflight`. Record PID T.
   T is live and stopped before the new image's user-space
   runs. That stop **is** the exec-completion handshake.
3. `proc_pidpath(T)` must be P (same inode). sha256 of
   that path must equal D.
4. Start identity S = `proc_pidinfo(T, PROC_PIDT_SHORTBSDINFO)`
   start `tv_sec`/`tv_usec`. Unreadable → reject.
5. Process arch field: `sysctl(CTL_KERN, KERN_PROC,
   KERN_PROC_PID, T)` → `kinfo_proc` CPU type of T after
   exec. Accepted: `macos-15` → `CPU_TYPE_ARM64`;
   `macos-15-intel` → `CPU_TYPE_X86_64`. Other or
   unreadable → reject. `file` of `proc_pidpath(T)` is
   executable metadata, not this field.
6. Translation field of T: the same `kinfo_proc`, Darwin
   process flag `P_TRANSLATED` (`0x00020000`).
   1 → reject. 0 → accept only if H, E, and process CPU
   type all match the class. Unreadable → reject.
   Parent `sysctl.proc_translated` is **not** this field.
   A helper that prints then `execve`s is **not** this
   field.
7. Never Intel on Apple Silicon. Never Rosetta.
8. Parent `kill(T, SIGKILL)` and wait. Discard this launch.

Any failed field, handshake, digest mismatch, PID reuse,
fat image, arch mismatch, `P_TRANSLATED=1`, or unreadable
field makes the job invalid. Invalid jobs are replaced,
not counted.

**Successor-triggering class changes.** Documented CPU,
RAM, storage, or architecture change; label retirement
or replacement; OS family change.

**Cache traces.** Record preflight, boot-id, purge output,
vm_stat/`MemTotal`, load average, process list, SIP.

## Decision

1. Adopt the successor, class-trade table, and fleet-class
   contract above.
2. Write the v3 reserved identifiers into file 08 as named.
   Not authored. Not QUALIFIED.
3. Condition 4 becomes 18 of 18 named required gates.
   Owners 22 of 22. Standing **MET**. MET is not QUALIFIED.
   MET does not authorize implementation.
4. **Exact file-08 edits, and no others:**
   - Replace (once):

```
reserved, not named (D-006 machine pins owed; D-086). cold-cache harness, p50/p95/p99, fixed runner image
```

     with

```
named: harness.DR-G03.core-startup (D-099; D-006 fleet-class successor; not authored; not QUALIFIED). cold-cache harness, p50/p95/p99, fleet class
```

   - Replace (once):

```
reserved, not named (D-006 machine pins owed; D-086). same runners and lifecycle commands
```

     with

```
named: harness.DR-G04.core-memory (D-099; D-006 fleet-class successor; not authored; not QUALIFIED). same fleet classes and lifecycle commands
```

   - Replace (once):

```
**16 of 18 required gates name a recorded identifier** (D-086 / D-088; not authored; not QUALIFIED); G03/G04 remain required and unnamed pending a D-006-conforming successor
```

     with

```
**18 of 18 required gates name a recorded identifier** (D-086 / D-088 / D-099; not authored; not QUALIFIED); G03/G04 named under D-099 hosted-fleet-class contract
```

   - Replace `| **PARTLY MET** |` (once in the snapshot
     table) with `| **MET** |`.
   - Replace only `condition 4 is PARTLY MET` with
     `condition 4 is MET`.
5. Does not name G13. Does not restore G17. Does not mark
   any DR row SATISFIED. Does not satisfy D-096 (A). Does
   not authorize `docs/v2/implementation/`.

## Alternatives

- Add warm p50 as a sixth G03 gate. Rejected: ADV-D098-T2-01.
- Weekly-image automatic rebaseline. Rejected: ADV-D098-01.
- Leave G04 series implicit. Rejected: ADV-D098-02.
- Fail guest-root size as the 14 GB class. Rejected:
  ADV-D098-03; advertised class ≠ df.
- Count `file` of `/proc/T/exe` as process ABI. Rejected:
  ADV-D099-T2-01.
- Read translation from the parent or from a pre-exec
  helper. Rejected: ADV-D099-T2-01 / D099-T2-N-1.
- Mix preflight into a timed `--help`/`--version` sample.
  Rejected: that launch is discarded.
- Fourth turn of D-098. Rejected: CONTESTED; new cycle only.
- Flip condition 5. Rejected: C2 NOT MET; C5 last.
- Authorize implementation. Rejected: C5 last.

## Readiness effect

Condition 4 becomes MET. Condition 2 stays 4 of 30 NOT MET.
Condition 5 remains NOT MET and last.

## Reversibility

C-D099 plus restore of the two reserved cells, 16-of-18
fragment, PARTLY MET, one-sentence clause, D-006's
pre-successor exact-machine and exact-OS requirements,
and the original D-006 runner classes (M1-class 8 GB;
native Intel-class; Linux 4 vCPU / 8 GB). Does not
overturn D-098 CONTESTED.

## Measured inputs at turn-3 dispatch

| Path | sha256 |
|---|---|
| COORD (live) | `0984005085b96920c2b4d3d561e950853bd40b6d97ee2cac77e457d647fe301b` |
| file 08 | `45dc4611717276c1f1c275982aa7ce787b2fa0b8fffbe1d315e8cb83ddff2206` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-098 CONTESTED predecessor commit | `09d0e288509f8b3e58d035290ff26f2e1d29c4ce` |
| D-099 turn-1 subject | `458dae40f8c77b7986ba4287448a4aa4ffdbcaccd6864d1612b97d6cd1afda08` |
| D-099 Claude 2 turn 1 | `9016bc8125fdf6262e1867c2b3f6ffc7d46e889c8ebd290bc5d386c55f907642` |
| D-099 Codex turn 1 | `13b40bd21ec4d9930f7890a0223d535b081ecf768de121388c4840e7c4f9b89e` |
| D-099 turn-2 subject | `4e34c7f0c16a1c7c761405504c8294e4152a5eddd470a559a47dbd933f61832c` |
| D-099 Claude 2 turn 2 | `fcbb2bfcc1fe34bbd3d8908c289d5cabafa9911cff410a83f97cab3ed93639e8` |
| D-099 Codex turn 2 | `03ae1f97e62001436d536d5ba3917e3be2bdc2953b6fb97a8ae51dc2b19f91cd` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
