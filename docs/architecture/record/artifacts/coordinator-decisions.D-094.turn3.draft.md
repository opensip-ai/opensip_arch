# D-094 — D-006 fleet-class successor plus G03/G04 named identifiers

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 turn 3 of 3. Same cycle as turns 1 and 2.
> Frozen turn-1 and turn-2 subjects are not edited. Not a
> SATISFIED re-record.
> **Decision type:** PREFERENCE-LADEN scoped D-006 successor
> replacing G03/G04 "exact machine / exact OS" with a
> hosted-fleet-class measurement contract, plus RULE-GOVERNED
> writing of the v3 reserved identifiers once that contract
> exists.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** execute G03 or G04. **Does not** claim
> QUALIFIED or DEMONSTRATED. **Does not** change D-006
> numeric threshold numerals or the regression rule.
> **Does not** restore G17. **Does not** name G13.
> **Does not** silently substitute Rosetta.

Turn-1 subject `coordinator-decisions.D-094.draft.md`
`263d2565ab8f230d99fd9bba7c631a33c431e6cf0eb7355184afaaac1614db5d`
held frozen. Turn-2 subject
`coordinator-decisions.D-094.turn2.draft.md`
`e20f85353aa0543ad56753b754566d9df9d34020bea343a7dbf4c63d5512caae`
held frozen. Turn-1 Claude 2 OBJECT, 0 MUST-FIX, 1 SHOULD-FIX
D094-SF-1. Turn-1 Codex OBJECTIONS, 3 MUST-FIX ADV-D094-01 /
02 / 03. Turn-2 Claude 2 OBJECT, 0 MUST-FIX, 1 SHOULD-FIX
D094-T2-SF-1. Turn-2 Codex OBJECTIONS, 1 MUST-FIX
ADV-D094-T2-01, 1 SHOULD-FIX ADV-D094-T2-02.

| ID | Sev | Disposition |
|---|---|---|
| ADV-D094-01 | MUST-FIX | ACCEPTED at turn 2 in part. Completes here via Route B: D-006's exact-machine / exact-OS requirement is superseded for G03/G04 by the fleet-class contract below. Labels are not one machine. |
| ADV-D094-02 / D094-SF-1 | MUST-FIX / SHOULD-FIX | ACCEPTED at turn 2. Venue and class are the same documented GH public runners. |
| ADV-D094-03 | MUST-FIX | ACCEPTED at turn 2. Apple native-check algorithm stands. |
| ADV-D094-T2-01 | MUST-FIX | ACCEPTED. Route B. Hosted-fleet-class contract, preflight, successor triggers, and cross-VM sample rule are defined here. Stop calling labels one machine or immutable exact pins. |
| ADV-D094-T2-02 | SHOULD-FIX | ACCEPTED. Codex turn-1 verdict word is OBJECTIONS, not OBJECT. |
| D094-T2-SF-1 | SHOULD-FIX | ACCEPTED. Per-platform class trade and warrant recorded. Warrant is D-000 PREFERENCE-LADEN authority for a procurable four-platform set; OBS-T3-02 is the Intel-specific reason, not the sole warrant. Existing ms/RSS numerals remain the intended bar. |

## Scoped D-006 successor

D-006 required this naming act to pin exact machine
identifiers and OS versions. GitHub-hosted public runners
are new VMs per job with weekly image rolls. That is not
one machine. This entry **supersedes** D-006's exact-machine
/ exact-OS requirement **for G03 and G04 only**, replacing
it with the hosted-fleet-class contract below.

D-006 numeric threshold **numerals** and the regress-only
10% rule stand. They now bind to the fleet class, not to a
single host. Analyze RSS and doctor-with-consented-probes
RSS remain outside D-006.

## Per-platform class trade (D094-T2-SF-1)

| Platform | D-006 class | This fleet class | Effect on the same numerals |
|---|---|---|---|
| macos-arm64 | M1-class, 8 GB | `macos-15`, 3-core M1, 7 GB, 14 GB SSD | Smaller machine. The same ms/RSS bars are **stricter**. Accepted. |
| macos-x86_64 | native Intel-class, no RAM named | `macos-15-intel`, 4 CPU, 14 GB, 14 GB SSD, native Intel VM, UDID `4203018E-580F-C1B5-9525-B745CECA79EB` | First sized Intel pin. OBS-T3-02. Accepted. |
| linux-x86_64 | 4 vCPU / 8 GB | `ubuntu-24.04`, 4 CPU, 16 GB, 14 GB SSD, x64, **public-repo** row | Larger machine. The same bars are **easier in RAM headroom**. Extra RAM is not a license to grow the process. Accepted. |
| linux-arm64 | 4 vCPU / 8 GB | `ubuntu-24.04-arm`, 4 CPU, 16 GB, 14 GB SSD, arm64, public-repo row | Same as linux-x86_64. Accepted. |

If a bar later proves infeasible on a class, the lawful path
is a successor **with the measurement attached**, never a
silent waiver (D-006 falsifiability note).

Warrant: D-000 PREFERENCE-LADEN product sign-off of a
procurable four-platform set. OBS-T3-02 is why Intel is the
GH Intel VM rather than a 2018 Mac mini. It is not claimed
as the sole warrant for the arm64 or Linux re-pins.

`macos-26-intel` exists and is not this class. The 2025
"last x86_64 image" recital stays withdrawn. Private-repo
2 CPU / 8 GB Linux rows are not this class.

## Hosted-fleet-class measurement contract

**What is pinned.** A **fleet class**, identified by the
workflow label plus the documented public-repo CPU / RAM /
storage / architecture row retrieved 2026-08-14 from
`https://docs.github.com/en/actions/reference/runners/github-hosted-runners`.
Each job is a new VM of that class. Labels are not one
machine and are not an immutable image digest.

**Fail-closed preflight (every sample).** Record and
require:

1. workflow label exact match
2. architecture exact match
3. CPU count exact match to the table
4. RAM GB exact match to the table
5. storage GB exact match to the table
6. OS family exact match (macOS 15 / Ubuntu 24.04)
7. CPU brand string
8. image version / runner-image identity as the runner
   reports it
9. native-architecture check (below)

Any mismatch discards the sample. It is not averaged in.

**Native-architecture check (macos-x86_64 class).** Record
host model, CPU architecture/brand, process architecture,
and the Rosetta query.

- `sysctl.proc_translated = 1` → reject
- `= 0` → accept only with independent native-Intel
  host and process facts
- OID absent (ENOENT) → accept only with those same facts
- any other error → reject

Never measure Intel on Apple Silicon. Never Rosetta.

**Same-label changes that require a reviewed successor.**

- documented CPU count, RAM, storage, or architecture change
- label retirement or replacement
- OS family change (macOS 15→26, Ubuntu 24.04→26.04)

**Same-label changes that do not require a successor.**

- a new VM instance per job (expected)
- weekly runner-image software roll **within** the same OS
  family, provided preflight still matches label / arch /
  CPU / RAM / storage

Those rolls are recorded (image identity on every sample).
They are not a pin change.

**Cross-VM, cross-release measurement.**

- A qualification result is the p50/p95/p99 of **N=11**
  independent jobs on fresh VMs of the class, cold and warm
  separately, after preflight.
- Release-to-release regression (D-006 10% rule) compares
  those distributions on the **same fleet class**, not on
  a reused VM and not across a successor-triggering class
  change.
- A single-VM number is not a qualification result.

**Cache-state protocol (unchanged in substance).** Cold:
single-user, no other OpenSIP process, drop page cache
(`sudo purge` / `sync && echo 3 | sudo tee
/proc/sys/vm/drop_caches`), first exec, record boot-id,
purge output, vm_stat or `/proc/meminfo`, load average,
process list, SIP status, and the preflight set. Warm:
immediately after one completed cold pair, same binary
path, no intervening purge. No unattended OS update during
that job.

## Decision

1. Adopt the scoped D-006 successor, the four fleet
   classes, the class-trade table, and the fleet-class
   measurement contract above.
2. Write the v3 reserved identifiers into file 08 as named.
   They remain not authored and not QUALIFIED.
3. Condition 4's named-harness half becomes 18 of 18
   required. Owners remain 22 of 22. Claims half remains
   abstinence. Standing becomes **MET**. MET is not
   QUALIFIED. MET does not authorize implementation.
4. **Exact file-08 edits, and no others:**
   - Replace this unique G03 harness-cell prefix (once):

```
reserved, not named (D-006 machine pins owed; D-086). cold-cache harness, p50/p95/p99, fixed runner image
```

     with

```
named: harness.DR-G03.core-startup (D-094; D-006 fleet-class successor; not authored; not QUALIFIED). cold-cache harness, p50/p95/p99, fleet class
```

   - Replace this unique G04 harness-cell prefix (once):

```
reserved, not named (D-006 machine pins owed; D-086). same runners and lifecycle commands
```

     with

```
named: harness.DR-G04.core-memory (D-094; D-006 fleet-class successor; not authored; not QUALIFIED). same fleet classes and lifecycle commands
```

   - Replace this unique condition-4 "Measured now" fragment
     (once):

```
**16 of 18 required gates name a recorded identifier** (D-086 / D-088; not authored; not QUALIFIED); G03/G04 remain required and unnamed pending a D-006-conforming successor
```

     with

```
**18 of 18 required gates name a recorded identifier** (D-086 / D-088 / D-094; not authored; not QUALIFIED); G03/G04 named under D-094 hosted-fleet-class contract
```

   - Replace the condition-4 standing cell `| **PARTLY MET** |`
     (once in the snapshot table) with `| **MET** |`.
   - In "What that means in one sentence", replace only
     `condition 4 is PARTLY MET` with `condition 4 is MET`.
5. Does not edit other D-088 gate-harness cells. Does not
   name G13. Does not restore G17. Does not mark any DR row
   SATISFIED. Does not authorize `docs/v2/implementation/`.

## Alternatives

- Route A: pin a single self-hosted physical host per
  platform. Rejected for this cycle: no such lab is
  recorded as procurable. Intel 2018 mini remains
  unverified (ADV-D094-02).
- Keep calling labels "one machine" / "exact pins".
  Rejected: ADV-D094-T2-01.
- Leave G03/G04 reserved after the fleet contract exists.
  Rejected: the D-086 reservation was for missing pins;
  the fleet-class contract is the successor pin.
- Confine the successor to Intel only and keep D-006's
  8 GB / 4-vCPU-8 GB classes for the other three.
  Rejected: those classes are not the procurable GH
  public rows; mixing would re-create venue/pin split.
- Change the numeric threshold numerals. Rejected: the
  numerals stay; their binding class is what changes, and
  that trade is recorded.
- Require literal `sysctl.proc_translated = 0` on Intel.
  Rejected: ADV-D094-03.
- Flip condition 5. Rejected: C2 is NOT MET; C5 is last.
- Authorize implementation. Rejected: C5 last.

## Readiness effect

Condition 4 becomes MET (18 of 18 named required gates;
22 of 22 owners; no QUALIFIED/DEMONSTRATED claim).
Condition 2 stays 4 of 30 and NOT MET. Condition 5 remains
NOT MET and last. No SATISFIED. No implementation
directory.

## Reversibility

C-D094 plus restore of the two reserved harness-cell
prefixes, the 16-of-18 fragment, the PARTLY MET standing
cell, the "condition 4 is PARTLY MET" clause, and D-006's
pre-successor exact-machine requirement and runner class.
Does not overturn D-086, D-088, D-093, or D-006 numeric
threshold numerals.

## Measured inputs at turn-3 dispatch

| Path | sha256 |
|---|---|
| COORD | `4ec069882b41ab5e14668e86cfac8dd977ac850c495c9f4f2ccadf05be107f20` |
| file 08 | `45dc4611717276c1f1c275982aa7ce787b2fa0b8fffbe1d315e8cb83ddff2206` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-086 commit | `14865abc42c13b9759f5761c2873db03b708ea32` |
| D-088 commit | `94b28c86a773f3e87c6d8fecc56693f508439199` |
| D-093 commit | `f7ce35ff0eb310c731b93060775c8ef69b0d36e4` |
| turn-1 subject | `263d2565ab8f230d99fd9bba7c631a33c431e6cf0eb7355184afaaac1614db5d` |
| turn-2 subject | `e20f85353aa0543ad56753b754566d9df9d34020bea343a7dbf4c63d5512caae` |
| Claude 2 turn 1 | `2dcb0d20157944e34f417cf8a1882203393ca62f9d2b1e7ec651d7068f0bda10` |
| Codex turn 1 | `76a3dc34f1139db68f96af8d18338820d9e5ec064b06b99c5122df9d09d83374` |
| Claude 2 turn 2 | `fcfe3b251c4399466695ceb629c6d5a38db06e7a3bbab79bad8351a850e33bfd` |
| Codex turn 2 | `940b336b1faf83aaddac33851b215b1b5aaca81f2620584695260f7b865e00b3` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
