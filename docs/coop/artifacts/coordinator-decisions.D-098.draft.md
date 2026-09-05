# D-098 — D-006 fleet-class successor plus G03/G04 named identifiers

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a fourth
> turn of CONTESTED D-094. Frozen D-094–D-097 subjects are
> not edited. Not a SATISFIED re-record. Not a user-amendment
> grant.
> **Decision type:** PREFERENCE-LADEN scoped D-006 successor
> replacing G03/G04 exact-machine / exact-OS with a
> hosted-fleet-class measurement contract, plus RULE-GOVERNED
> writing of the v3 reserved identifiers once that contract
> exists. Same class as D-006 (numbers/class bind to a
> reviewed product pin).
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** execute G03 or G04. **Does not** claim
> QUALIFIED or DEMONSTRATED. **Does not** change D-006
> numeric threshold numerals. **Does not** restore G17.
> **Does not** name G13. **Does not** silently substitute
> Rosetta. **Does not** overturn D-094 CONTESTED, D-096, or
> D-097.

D-094 is CONTESTED at `4172141db867fa33c7ca3c49e77ed2795978aff8`.
D-097 is ADOPTED at `11691723d2a4b959daf9ddf5ac3df3977f8259ac`
(withdrawal; D-096 (A) stays unsatisfied). This cycle is
the C4 naming retry, not a C2 owner grant.

| ID | Sev | Disposition |
|---|---|---|
| ADV-D094-T3-01 | MUST-FIX | ACCEPTED. Paired same-VM/same-image compare, or rebaseline. |
| ADV-D094-T3-02 | MUST-FIX | ACCEPTED. N=21, nearest-rank ceil(p×N), separate `--help` / `--version` series. Ranks 11/20/21. |
| ADV-D094-T3-03 | SHOULD-FIX | ACCEPTED. Host, executable, and process architecture all match. Translation check on both macOS classes. RAM/storage observables defined. |
| ADV-D094-T2-01 | MUST-FIX | ACCEPTED via Route B. Labels are a fleet class, not one machine. |
| D094-T2-SF-1 | SHOULD-FIX | ACCEPTED. Class-trade table and warrant recorded. |

## Scoped D-006 successor

D-006's exact-machine / exact-OS requirement is superseded
**for G03 and G04 only**. Numerals and the 10% regress-only
rule stand and now bind to this fleet class. Analyze RSS
and doctor-with-consented-probes RSS remain outside D-006.

## Per-platform class trade

| Platform | D-006 class | This fleet class | Effect |
|---|---|---|---|
| macos-arm64 | M1-class, 8 GB | `macos-15`, 3-core M1, 7 GB, 14 GB SSD, arm64 | Smaller. Bars **stricter**. Accepted. |
| macos-x86_64 | native Intel-class | `macos-15-intel`, 4 CPU, 14 GB, 14 GB SSD, native Intel VM, UDID `4203018E-580F-C1B5-9525-B745CECA79EB` | First sized Intel pin. OBS-T3-02. Accepted. |
| linux-x86_64 | 4 vCPU / 8 GB | `ubuntu-24.04`, 4 CPU, 16 GB, 14 GB SSD, x64, public-repo | Larger RAM. Extra RAM is not a license to grow the process. Accepted. |
| linux-arm64 | 4 vCPU / 8 GB | `ubuntu-24.04-arm`, 4 CPU, 16 GB, 14 GB SSD, arm64, public-repo | Same. Accepted. |

Warrant: D-000 PREFERENCE-LADEN product sign-off of a
procurable four-platform set (same class as D-006's
thresholds). OBS-T3-02 is the Intel reason, not the sole
warrant for the other three. Source: GitHub hosted-runners
public table, 2026-08-14. `macos-26-intel` is not this
class. Private-repo 2 CPU / 8 GB is not this class.
Infeasible bar → successor with measurement, never silent
waiver.

## Hosted-fleet-class measurement contract

**Pinned object.** Fleet class = workflow label + documented
public-repo CPU/RAM/storage/arch row. New VM per job.
Labels are not one machine and not an immutable digest.

**Sample unit.** One job → one `--help` sample and one
`--version` sample as **separate series**. G04 series are
the D-006 lifecycle commands.

**N and quantiles.** N=21 accepted jobs per series per
(cold, warm) per platform. Estimator: nearest-rank,
rank = ceil(p × N). For N=21: p50=11, p95=20, p99=21.
Invalid preflight jobs are replaced, not counted.

**Fail-closed preflight (every job).**

1. workflow label exact match
2. host, executable, and process architecture all match
   the class
3. CPU count exact: macos-arm64=3; others=4
   (`sysctl -n hw.ncpu` / `nproc`)
4. RAM GiB = observed_bytes/1024³ matches table 7/14/16
   within ±0.75 GiB (`hw.memsize` / `MemTotal`)
5. storage advertised 14 GB; admit root size in [10, 20]
   GB (`df -k /`); record observed
6. OS family exact (macOS 15 / Ubuntu 24.04)
7. CPU brand recorded (stratum)
8. image identity recorded as the runner reports it
9. translation check on **both** macOS classes: 1 reject;
   0 or ENOENT accept only with independent matching
   host/process facts; other error reject

Never Intel on Apple Silicon. Never Rosetta.

**Successor-triggering class changes.** Documented CPU,
RAM, storage, or architecture change; label retirement
or replacement; OS family change.

**Regression.**

- First qualified release: absolute D-006 numerals only.
- Later, **same** image identity and **same** CPU brand:
  on each of the N VMs, run previous qualified binary and
  candidate binary in randomized order. The 10% rule
  applies to those **paired** per-percentile results.
- If image identity or CPU brand differs: **rebaseline**.
  Absolute numerals only. The 10% rule does not span a
  rebaseline. Weekly image rolls force rebaseline, not
  unpaired same-class compare.

**Cache-state.** Cold: single-user, drop page cache
(`sudo purge` / `sync && echo 3 | sudo tee
/proc/sys/vm/drop_caches`), first exec, record preflight
plus boot-id, purge output, vm_stat/`MemTotal`, load
average, process list, SIP. Warm: immediately after one
completed cold pair, same binary, no intervening purge.

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
named: harness.DR-G03.core-startup (D-098; D-006 fleet-class successor; not authored; not QUALIFIED). cold-cache harness, p50/p95/p99, fleet class
```

   - Replace (once):

```
reserved, not named (D-006 machine pins owed; D-086). same runners and lifecycle commands
```

     with

```
named: harness.DR-G04.core-memory (D-098; D-006 fleet-class successor; not authored; not QUALIFIED). same fleet classes and lifecycle commands
```

   - Replace (once):

```
**16 of 18 required gates name a recorded identifier** (D-086 / D-088; not authored; not QUALIFIED); G03/G04 remain required and unnamed pending a D-006-conforming successor
```

     with

```
**18 of 18 required gates name a recorded identifier** (D-086 / D-088 / D-098; not authored; not QUALIFIED); G03/G04 named under D-098 hosted-fleet-class contract
```

   - Replace `| **PARTLY MET** |` (once in the snapshot
     table) with `| **MET** |`.
   - Replace only `condition 4 is PARTLY MET` with
     `condition 4 is MET`.
5. Does not name G13. Does not restore G17. Does not mark
   any DR row SATISFIED. Does not satisfy D-096 (A). Does
   not authorize `docs/v2/implementation/`.

## Alternatives

- Fourth turn of D-094. Rejected: CONTESTED; new cycle only.
- Unpaired same-class historical compare. Rejected:
  ADV-D094-T3-01.
- N=11. Rejected: ADV-D094-T3-02.
- Change D-006 numerals. Rejected: numerals stay.
- Flip condition 5. Rejected: C2 NOT MET; C5 last.
- Authorize implementation. Rejected: C5 last.

## Readiness effect

Condition 4 becomes MET. Condition 2 stays 4 of 30 NOT MET.
Condition 5 remains NOT MET and last.

## Reversibility

C-D098 plus restore of the two reserved cells, 16-of-18
fragment, PARTLY MET, one-sentence clause, and D-006's
pre-successor exact-machine requirement. Does not overturn
D-086, D-088, D-093, D-094 CONTESTED, D-096, or D-097.

## Measured inputs at dispatch

| Path | sha256 |
|---|---|
| COORD | `17262fe0d40b8a41fae8d5391691809eb436102b842118652e042695ee749326` |
| file 08 | `45dc4611717276c1f1c275982aa7ce787b2fa0b8fffbe1d315e8cb83ddff2206` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-094 commit | `4172141db867fa33c7ca3c49e77ed2795978aff8` |
| D-097 commit | `11691723d2a4b959daf9ddf5ac3df3977f8259ac` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
