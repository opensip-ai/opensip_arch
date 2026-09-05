# D-102 — D-006 fleet-class successor plus G03/G04 named identifiers

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a fourth
> turn of CONTESTED D-101. Frozen D-101 and D-099 subjects
> are not edited. Not a SATISFIED re-record.
> **Decision type:** PREFERENCE-LADEN scoped D-006 successor
> plus RULE-GOVERNED naming of the v3 reserved identifiers.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** execute G03 or G04. **Does not** claim
> QUALIFIED or DEMONSTRATED. **Does not** change D-006
> numeric threshold numerals. **Does not** restore G17.
> **Does not** name G13. **Does not** silently substitute
> Rosetta. **Does not** overturn D-094, D-098, D-099, or
> D-101 CONTESTED, D-096, or D-097.

D-101 is CONTESTED at `c159c224c8766715b21a1522755aeb235c8335df`.
This cycle restates the D-101 turn-3 contract in this
file's own bytes. ADV-D101-T3-01 accepted: the
disposition row now matches the numbered sequence.
Numbered sequences are unchanged. File-08 writes name
D-102.

| ID | Sev | Disposition |
|---|---|---|
| ADV-D101-T3-01 | SHOULD-FIX | ACCEPTED. Inode-only `stat` after purge immediately before the cold launch, and before an unpurged doctor launch. No `stat` or hash inside the cold/warm pair. |
| D101-T2-MF-1 / ADV-D101-T2-01 | MUST-FIX | Remains accepted: no full-file hash between purge and cold. |
| D101-T1-MF-1 | MUST-FIX | Remains accepted: ISA is the derivation, not `sysctl.proc_cputype`. |

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

**Path/digest identity for timed launches (both
platforms; D101-T2-MF-1 / ADV-D101-T2-01 /
D101-T2-SF-1).** Full-file `sha256(P)` is a data-page
read. `stat` of `(st_dev, st_ino)` is not.

- Before the purge that opens each cold/warm sequence:
  `sha256(P)` must equal D0.
- After that purge, immediately before the cold exec:
  `stat` only. I must equal I0. **Do not** hash here.
- After the cold/warm pair completes: `sha256(P)` must
  equal D0 again.
- Immediately before any launch that has no preceding
  purge in this protocol (`doctor` read-only): `stat`
  only (I == I0). Preflight already bound D0.
- Any mismatch → reject the job and rerun preflight
  from the dedicated architecture launch.

**First qualified release, per accepted VM, G03/G04
help/version.** For each command C in {`--help`, `--version`}
in recorded order:

1. `sha256(P)` must equal D0
2. purge (`sudo purge` / `sync && echo 3 | sudo tee
   /proc/sys/vm/drop_caches`)
3. `stat` P; I must equal I0 (no hash)
4. cold C of the **candidate** (first exec after that purge)
5. warm C of the **candidate** immediately; no other
   command or binary intervenes
6. `sha256(P)` must equal D0

Then, for G04 only, `stat` P (I == I0), one `doctor`
read-only launch (no purge-warm pair). Record order.

**Second-or-later release, per accepted VM.** Previous
qualified binary Prev (digest-pinned) and candidate Cand.
Randomize {Prev,Cand} order; record it. For each command
X in {`--help`, `--version`}, for each binary B in that
order:

1. `sha256(B)` must equal that binary's recorded digest
2. purge
3. `stat` B; I must equal that binary's I0 (no hash)
4. cold X of B
5. warm X of B immediately
6. `sha256(B)` must equal that binary's recorded digest

Then G04 `doctor` read-only of first binary, then of
second, each preceded by `stat` only, recorded order
matching {Prev,Cand}. No intervening other command
inside a cold/warm pair. 21 accepted **matched pairs**
per governed series.

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
2. Record absolute path P, I0=`(st_dev, st_ino)` of P,
   and `sha256(P)=D0`. Reject if `file` of P (and
   `lipo -info` on macOS) shows more than one slice.
   The job must not mutate P concurrently. Timed-launch
   identity is the split check (both platforms).
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
4. Parent `waitpid(T, …)` until the post-`execve` `SIGTRAP`
   that `PTRACE_TRACEME` produces (`WIFSTOPPED`). That
   wait **is** the exec-completion handshake. The parent
   does not need `PTRACE_O_TRACEEXEC`. If `waitpid`
   returns exited or signaled before that stop, reject.
5. Parent re-reads starttime as S1. If S1 ≠ S0 or T is
   not live, reject (PID reuse).
6. Parent opens `/proc/T/exe` `O_RDONLY` and sha256s that
   fd. Must equal D. This is post-exec executable
   identity, not process ABI.
7. Parent reads `/proc/T/auxv` as an array of
   `{type, value}` words. `AT_PLATFORM` (15)'s value is
   a **pointer** into T's address space, not the string.
   While T is still stopped, the parent dereferences it
   with `process_vm_readv(T, …)` (or `pread` of
   `/proc/T/mem`) into a 32-byte buffer, stopping at the
   first NUL. Missing type, unreadable pointer, no NUL
   inside 32 bytes, or a failed read → reject. Do not
   call `getauxval()` in the parent. Do not compare the
   raw pointer. The resulting C string is the **process
   ABI** field. Accepted: class `ubuntu-24.04` →
   `x86_64`; class `ubuntu-24.04-arm` → `aarch64`.
   `AT_BASE_PLATFORM` is audit-only, same dereference
   rule.
8. `file` of `/proc/T/exe` is **not** counted as process
   ABI. Never `/proc/self/exe` of the parent. H, E, and
   the AT_PLATFORM string must all match the class.
9. Parent `kill(T, SIGKILL)` and `waitpid`. Discard this
   launch.

**macOS target-process protocol (item 10).** APIs used
here are those present on MacOSX15.4.sdk. That SDK is
the API-availability warrant, not the fleet-class
definition (the class remains workflow label +
CPU/RAM/storage/arch row). `PROC_PIDARCHINFO` /
`struct proc_archinfo` are absent there and are **not**
used. `sysctl.proc_cputype`+PID is **not** used: it was
measured this cycle (D101-T1-MF-1) and returns the host
CPU type, identical for native arm64 and Rosetta x86_64.

**Path identity (preflight).** P is a digest-addressed
measurement projection that the job must not mutate
concurrently. Record I0 = `(st_dev, st_ino)` of P and
D0 = `sha256(P)` before spawn. After all target
observations, re-`stat` P and re-hash: I and D must
equal I0 and D0. Suspension of T does **not** by itself
detect a path swap. Timed-launch identity is the
split check above (hash before purge and after the
pair; `stat` only between purge and cold). macOS
path-hash is weaker than Linux's `/proc/T/exe` fd
hash. Darwin has no fd-to-running-image equivalent.

1. Parent `posix_spawnattr_setflags(POSIX_SPAWN_START_SUSPENDED)`
   and `posix_spawnattr_setarchpref_np` to exactly one
   CPU type: `CPU_TYPE_ARM64` for `macos-15`,
   `CPU_TYPE_X86_64` for `macos-15-intel`. Close-match
   fallback (`arch(1)` trying a near arch) is forbidden.
   Spawn failure → reject.
2. `posix_spawn` of P with `argv_preflight`. Record PID T.
   T is live and stopped before the new image's user-space
   runs. That stop **is** the exec-completion handshake.
3. `proc_pidpath(T)` must equal P. Re-`stat` P; I must
   equal I0; `sha256(P)` must equal D0.
4. Start identity. `n = proc_pidinfo(T, PROC_PIDTBSDINFO,
   0, &bi, PROC_PIDTBSDINFO_SIZE)`. If `n` ≠
   `PROC_PIDTBSDINFO_SIZE`, reject. S =
   `(bi.pbi_start_tvsec, bi.pbi_start_tvusec)`.
   `PROC_PIDT_SHORTBSDINFO` has no start-time members
   and is not used.
5. Process ISA is **derived**, not read from a per-process
   CPU-type API (none exists on MacOSX15.4.sdk among the
   routes discussed in D-099/D-101; `task_for_pid` plus
   a target-memory Mach-O header would, and needs
   entitlements the hosted runner will not grant). The
   derivation:
   - H (`uname -m`) must match the class;
   - E (thin on-disk slice of P) must match the class;
   - D0 binds those bytes;
   - step 1 requested exactly that CPU type and spawn
     succeeded, so any other ISA is unspawnable;
   - step 6 `P_TRANSLATED` of T is 0.
   On macos-15, `P_TRANSLATED=0` means T is native
   arm64; `P_TRANSLATED=1` means T is x86_64 and
   **rejects**. On macos-15-intel, H is x86_64 and no
   translation exists to consider. This is not
   `sysctl.proc_cputype`. This is not a `kinfo_proc`
   CPU-type member. This is not `PROC_PIDARCHINFO`.
6. Translation field of T: `sysctl(CTL_KERN, KERN_PROC,
   KERN_PROC_PID, T)` → `kinfo_proc.kp_proc.p_flag` bit
   `P_TRANSLATED` (`0x00020000`). 1 → reject. 0 → accept
   only if H, E, and this bit all match the class
   (native). Unreadable → reject. Parent
   `sysctl.proc_translated` is **not** this field. A
   helper that prints then `execve`s is **not** this
   field.
7. Re-read start identity into S1 with the same
   `PROC_PIDTBSDINFO` size check. If S1 ≠ S or T is not
   live, reject. Repeat the path-identity check (I, D).
8. Never Intel on Apple Silicon. Never Rosetta.
9. Parent `kill(T, SIGKILL)` and wait. Discard this launch.

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
named: harness.DR-G03.core-startup (D-102; D-006 fleet-class successor; not authored; not QUALIFIED). cold-cache harness, p50/p95/p99, fleet class
```

   - Replace (once):

```
reserved, not named (D-006 machine pins owed; D-086). same runners and lifecycle commands
```

     with

```
named: harness.DR-G04.core-memory (D-102; D-006 fleet-class successor; not authored; not QUALIFIED). same fleet classes and lifecycle commands
```

   - Replace (once):

```
**16 of 18 required gates name a recorded identifier** (D-086 / D-088; not authored; not QUALIFIED); G03/G04 remain required and unnamed pending a D-006-conforming successor
```

     with

```
**18 of 18 required gates name a recorded identifier** (D-086 / D-088 / D-102; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract
```

   - Replace `| **PARTLY MET** |` (once in the snapshot
     table) with `| **MET** |`.
   - Replace only `condition 4 is PARTLY MET` with
     `condition 4 is MET`.
5. Does not name G13. Does not restore G17. Does not mark
   any DR row SATISFIED. Does not satisfy D-096 (A). Does
   not authorize `docs/v2/implementation/`.

## Alternatives

- Use `PROC_PIDARCHINFO`. Rejected: absent from
  MacOSX15.4.sdk; ADV-D099-T3-01.
- Use `sysctl.proc_cputype`+PID as process arch.
  Rejected: D101-T1-MF-1; measured as host CPU type.
- Use `task_for_pid` plus a target-memory Mach-O
  header. Rejected: needs entitlements the hosted
  runner will not grant.
- Use a `kinfo_proc` CPU-type member. Rejected:
  D099-T3-MF-1; that member does not exist.
- Use `PROC_PIDT_SHORTBSDINFO` for start time. Rejected:
  D099-T3-SF-1; no such members.
- Claim suspension detects a path swap. Rejected:
  ADV-D101-T1-01.
- Hash P between purge and cold exec. Rejected:
  D101-T2-MF-1 / ADV-D101-T2-01; that is a warm.
- Count `file` of `/proc/T/exe` as process ABI. Rejected:
  ADV-D099-T2-01.
- Compare the raw AT_PLATFORM pointer, or `getauxval()`
  in the parent. Rejected: ADV-D099-T3-N-01.
- Read translation from the parent or from a pre-exec
  helper. Rejected: ADV-D099-T2-01.
- Mix preflight into a timed `--help`/`--version` sample.
  Rejected: that launch is discarded.
- Fourth turn of D-099 or D-101. Rejected: CONTESTED;
  new cycle only.
- Flip condition 5. Rejected: C2 NOT MET; C5 last.
- Authorize implementation. Rejected: C5 last.

## Readiness effect

Condition 4 becomes MET. Condition 2 stays 4 of 30 NOT MET.
Condition 5 remains NOT MET and last.

## Reversibility

C-D102 plus restore of the two reserved cells, 16-of-18
fragment, PARTLY MET, one-sentence clause, D-006's
pre-successor exact-machine and exact-OS requirements,
and the original D-006 runner classes (M1-class 8 GB;
native Intel-class; Linux 4 vCPU / 8 GB). Does not
overturn D-101 CONTESTED.

## Measured inputs at turn-1 dispatch

| Path | sha256 |
|---|---|
| COORD (live) | `151e8896c8785fee56c5c8856112b793df3ab930babae1b107ced9958ce1c50c` |
| file 08 | `45dc4611717276c1f1c275982aa7ce787b2fa0b8fffbe1d315e8cb83ddff2206` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-101 CONTESTED predecessor commit | `c159c224c8766715b21a1522755aeb235c8335df` |
| D-101 turn-3 subject | `ba5f8fc8ae336de0073642fd6e3ac2bc549988256b20068e2864df3ff1e66eae` |
| D-101 Claude 2 turn 3 | `8e3828071c789ec2f05903ee1ed44af376b88751957f6ebf8e90bfa10d8c6921` |
| D-101 Codex turn 3 | `b0819a1dc14522c37d0caef61bdfec9c19778af622e44f9ac6b21e1931da6209` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
