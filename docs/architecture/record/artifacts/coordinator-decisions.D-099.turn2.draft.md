# D-099 — D-006 fleet-class successor plus G03/G04 named identifiers

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Frozen
> turn-1 subject is not edited. Not a fourth turn of D-098.
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
held frozen. Claude 2 OBJECT, 0 MUST-FIX, 1 SHOULD-FIX
D099-SF-1. Codex OBJECTIONS, 0 MUST-FIX, 1 SHOULD-FIX
ADV-D099-01.

| ID | Sev | Disposition |
|---|---|---|
| D099-SF-1 | SHOULD-FIX | ACCEPTED. This subject carries the full contract in its own bytes. It does not adopt a CONTESTED cycle by digest reference. |
| ADV-D099-01 | SHOULD-FIX | ACCEPTED. Target-process observation uses a live child PID, thin binaries, and a same-PID exec handshake. |

D-098 is CONTESTED at `09d0e288509f8b3e58d035290ff26f2e1d29c4ce`.
This is a new cycle.

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

**Preflight (every job; fail-closed).**

1. label: record the measurement manifest `runs-on`
   literal; must equal the class label
2. **Thin binaries only.** Fat/universal images fail
   preflight. Host arch: `uname -m`. Executable arch:
   `file` of the on-disk thin path (one slice). Process
   arch: parent `fork`s, records child PID T **before**
   exec, child `execve`s the thin target (same PID T
   after exec). While T is live, Linux reads
   `file -L /proc/T/exe` (never `/proc/self/exe` of the
   parent). macOS: spawn via `arch -arm64` or
   `arch -x86_64` matching the class; parent records T
   and `proc_pidpath(T)` of the live child; `file` of
   that thin path is the process arch. A short command
   is held live with a pipe until the parent has sampled
   T. Translation is read from the **child** after exec
   (helper that execs the target under the same `arch`,
   printing `sysctl.proc_translated` then `_exit`, is
   not a substitute for sampling T). All three match the
   class
3. CPU count: `sysctl -n hw.ncpu` / `nproc`; macos-arm64=3;
   others=4
4. RAM: macos `sysctl -n hw.memsize` bytes; Linux
   `MemTotal` kB × 1024. GiB = bytes/1024³. Match 7/14/16
   ±0.75 GiB
5. storage: **audit-only**. Record `df -k /` 1024-byte
   blocks field (second column) × 1024. Never fail the
   job on this field
6. OS family: macos `sw_vers -productVersion` major=15;
   Linux `/etc/os-release` `VERSION_ID=24.04`
7. CPU brand: macos `sysctl -n machdep.cpu.brand_string`;
   Linux `/proc/cpuinfo` `model name`. Recorded stratum
8. image version: record the GitHub Actions `Set up job`
   image version / `ImageVersion` (not `RUNNER_TRACKING_ID`)
9. translation, both macOS classes: `sysctl.proc_translated`
   1 reject; 0 or ENOENT accept only with independent
   matching host/process facts; other error reject

Never Intel on Apple Silicon. Never Rosetta.

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
- Fourth turn of D-094. Rejected: CONTESTED.
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
native Intel-class; Linux 4 vCPU / 8 GB).

## Measured inputs at turn-2 dispatch

| Path | sha256 |
|---|---|
| COORD | `17262fe0d40b8a41fae8d5391691809eb436102b842118652e042695ee749326` |
| file 08 | `45dc4611717276c1f1c275982aa7ce787b2fa0b8fffbe1d315e8cb83ddff2206` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-094 commit | `4172141db867fa33c7ca3c49e77ed2795978aff8` |
| D-097 commit | `11691723d2a4b959daf9ddf5ac3df3977f8259ac` |
| turn-1 subject | `bd45626e0a0cdc1b6e798a4f5276fbb09646debdd832cf19180d8bed4d4dc264` |
| turn-2 subject | `1be52e83df90b1ac7c02b0937cb62f861821b517c77c45905cda0dd7f4479a1b` |
| Claude 2 turn 1 | `6ab7b4217b109cd238efb5b67ae7fadacf22eca1a61be405fea456b6d217bbcf` |
| Codex turn 1 | `0f042c1791726540d8f6e9d6e2753a7c7b62d59cd40d9c93a867d9593251e426` |
| Claude 2 turn 2 | `b813b9437db64d6d48c76c0baeee3f75c00515a6eb4393813d52b25120b9a2bc` |
| D-098 commit | `09d0e288509f8b3e58d035290ff26f2e1d29c4ce` |
| COORD | `0984005085b96920c2b4d3d561e950853bd40b6d97ee2cac77e457d647fe301b` |
| turn-1 subject | `458dae40f8c77b7986ba4287448a4aa4ffdbcaccd6864d1612b97d6cd1afda08` |
| Claude 2 turn 1 | `9016bc8125fdf6262e1867c2b3f6ffc7d46e889c8ebd290bc5d386c55f907642` |
| Codex turn 1 | `13b40bd21ec4d9930f7890a0223d535b081ecf768de121388c4840e7c4f9b89e` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
