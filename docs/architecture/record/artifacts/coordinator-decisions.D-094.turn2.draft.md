# D-094 — D-006 runner-class successor plus G03/G04 named identifiers

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Frozen
> turn-1 subject is not edited. Not a SATISFIED re-record.
> **Decision type:** PREFERENCE-LADEN scoped D-006 successor
> for the G03/G04 runner class, plus RULE-GOVERNED writing of
> the v3 reserved identifiers once those exact pins exist.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** execute G03 or G04. **Does not** claim
> QUALIFIED or DEMONSTRATED. **Does not** change D-006
> numeric thresholds or the regression rule. **Does not**
> restore G17. **Does not** name G13. **Does not**
> silently substitute Rosetta.

Turn-1 subject `coordinator-decisions.D-094.draft.md`
`263d2565ab8f230d99fd9bba7c631a33c431e6cf0eb7355184afaaac1614db5d`
held frozen. Claude 2 OBJECT, 0 MUST-FIX, 1 SHOULD-FIX
D094-SF-1. Codex OBJECT, 3 MUST-FIX ADV-D094-01 / 02 / 03.

| ID | Sev | Disposition |
|---|---|---|
| ADV-D094-01 | MUST-FIX | ACCEPTED. Pin one exact procurable machine per platform. No i5/i7 alternative. No deferral of image identity to first run. |
| ADV-D094-02 | MUST-FIX | ACCEPTED. Turn-1 2018 Mac mini 8 GB pin is not verified procurable. The procurable native-Intel machine is the documented GitHub-hosted `macos-15-intel` VM (4 CPU / 14 GB). That requires a scoped D-006 runner-class successor, recorded here, not a false procurability finding for the 2018 mini. |
| ADV-D094-03 | MUST-FIX | ACCEPTED. Native-architecture check follows Apple's documented algorithm: value 1 = translated (reject); value 0 = native if the OID exists; ENOENT = native only when independent host/process facts establish native Intel. Unexpected errors reject. |
| D094-SF-1 | SHOULD-FIX | ACCEPTED. Same as ADV-D094-02. Venue and pin are now the same object. |

D-006 is ADOPTED (CONSENT `bfd8a758…`). This entry is the
OBS-T3-02 successor-decision path for the runner class
only. Numeric thresholds stand. D-086 / D-088 / D-093 stand.

## Scoped D-006 successor (runner class only)

D-006's named class was: macOS arm64 M1-class 8 GB; macOS
x86_64 native Intel-class never Rosetta; Linux 4 vCPU / 8 GB.

Turn-1 tried to keep that class and cite `macos-15-intel` as
procurability evidence for a different machine. That failed.

This turn replaces the G03/G04 execution class with the
**GitHub-hosted public-repository standard runners**
documented at
`https://docs.github.com/en/actions/reference/runners/github-hosted-runners`
as retrieved 2026-08-14. Product sign-off: those four
machines are the representative qualification venues.

## Exact pins (one machine per platform)

1. **macos-arm64-ref.** Workflow label `macos-15`. Hardware:
   3-core Apple M1, 7 GB RAM, 14 GB SSD, arm64. Source:
   GitHub-hosted runners reference, public-repo table,
   2026-08-14. OS: macOS 15 as shipped on that image.
2. **macos-x86_64-ref.** Workflow label `macos-15-intel`.
   Hardware: 4 CPU, 14 GB RAM, 14 GB SSD, native Intel VM.
   Source: same table. OS: macOS 15 as shipped on that
   image. Not `macos-26-intel`. Not Rosetta. Not Apple
   Silicon. Static UDID documented by GitHub:
   `4203018E-580F-C1B5-9525-B745CECA79EB`.
3. **linux-x86_64-ref.** Workflow label `ubuntu-24.04`.
   Hardware: 4 CPU, 16 GB RAM, 14 GB SSD, x64. Source:
   same public-repo table. OS: Ubuntu 24.04 as shipped on
   that image. Not the private-repo 2 CPU / 8 GB row.
4. **linux-arm64-ref.** Workflow label `ubuntu-24.04-arm`.
   Hardware: 4 CPU, 16 GB RAM, 14 GB SSD, arm64. Source:
   same public-repo table. OS: Ubuntu 24.04 as shipped on
   that image.

A later label, CPU/RAM, or image-family change is a reviewed
successor. Silent drift is forbidden. The first harness run
records the live image build for audit; it does not choose
the pin.

`macos-26-intel` exists on the same table. It is not this
pin. The 2025 "last x86_64 image" recital is withdrawn.

## Procurability

Each pin is the documented public GitHub-hosted runner of
that label. Procurability is the present publication of
that table. This finding is about those four machines, not
about a 2018 Mac mini.

## Native-architecture check

Record host model, CPU architecture/brand, process
architecture, and the Rosetta query.

On macos-x86_64-ref:

- `sysctl.proc_translated = 1` → reject (translated).
- `sysctl.proc_translated = 0` → accept only with
  independent facts showing native Intel host and process.
- OID absent (ENOENT) → accept only with the same
  independent native-Intel facts (Apple's documented
  native mapping).
- Any other error → reject.

Never measure Intel on Apple Silicon. Never Rosetta.

## Cache-state protocol

**Cold.** Single-user. No other OpenSIP process. Drop page
cache (`sudo purge` on macOS; `sync && echo 3 | sudo tee
/proc/sys/vm/drop_caches` on Linux). First exec of the
gate commands. Record boot-id, purge output, vm_stat or
`/proc/meminfo` before and after, load average, process
list, SIP status, host/process architecture, and the
native-architecture check above.

**Warm.** Immediately after one completed cold pair, same
binary path, no intervening purge, no other workload.
Record the same traces plus that purge was not repeated.

**Fixed image.** No unattended OS update during the sample
window. Analyze RSS and doctor-with-consented-probes RSS
remain outside D-006 (unchanged). Thresholds unchanged.

## Decision

1. Adopt the scoped D-006 runner-class successor and the
   four exact pins, cache-state protocol, native-architecture
   check, and procurability finding above.
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
named: harness.DR-G03.core-startup (D-094; D-006 runner-class successor + exact GH-hosted pins; not authored; not QUALIFIED). cold-cache harness, p50/p95/p99, fixed runner image
```

   - Replace this unique G04 harness-cell prefix (once):

```
reserved, not named (D-006 machine pins owed; D-086). same runners and lifecycle commands
```

     with

```
named: harness.DR-G04.core-memory (D-094; D-006 runner-class successor + exact GH-hosted pins; not authored; not QUALIFIED). same runners and lifecycle commands
```

   - Replace this unique condition-4 "Measured now" fragment
     (once):

```
**16 of 18 required gates name a recorded identifier** (D-086 / D-088; not authored; not QUALIFIED); G03/G04 remain required and unnamed pending a D-006-conforming successor
```

     with

```
**18 of 18 required gates name a recorded identifier** (D-086 / D-088 / D-094; not authored; not QUALIFIED); G03/G04 named under D-094 exact GH-hosted pins
```

   - Replace the condition-4 standing cell `| **PARTLY MET** |`
     (once in the snapshot table) with `| **MET** |`.
   - In "What that means in one sentence", replace only
     `condition 4 is PARTLY MET` with `condition 4 is MET`.
5. Does not edit other D-088 gate-harness cells. Does not
   name G13. Does not restore G17. Does not mark any DR row
   SATISFIED. Does not authorize `docs/v2/implementation/`.

## Alternatives

- Keep the 2018 Mac mini 8 GB pin and cite `macos-15-intel`
  as its procurability evidence. Rejected: ADV-D094-02 /
  D094-SF-1.
- Leave G03/G04 unnamed and only record the successor.
  Rejected: once exact procurable pins exist, GHN-V1-B2 no
  longer blocks naming.
- Use `macos-26-intel` or `-latest` labels. Rejected: pin
  is `macos-15-intel` / `macos-15`.
- Use the private-repo 2 CPU / 8 GB Linux row. Rejected:
  this pin is the public-repo 4 CPU / 16 GB row.
- Require literal `sysctl.proc_translated = 0` on Intel.
  Rejected: ADV-D094-03; Apple maps ENOENT to native.
- Change D-006 numeric thresholds. Rejected: out of scope.
- Present 16 of 18 after naming, or 18 of 16. Rejected:
  GHN-V2-B1.
- Claim QUALIFIED. Rejected: nothing executed.
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
pre-successor runner class. Does not overturn D-086,
D-088, D-093, or D-006 numeric thresholds.

## Measured inputs at turn-2 dispatch

| Path | sha256 |
|---|---|
| COORD | `4ec069882b41ab5e14668e86cfac8dd977ac850c495c9f4f2ccadf05be107f20` |
| file 08 | `45dc4611717276c1f1c275982aa7ce787b2fa0b8fffbe1d315e8cb83ddff2206` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-086 commit | `14865abc42c13b9759f5761c2873db03b708ea32` |
| D-088 commit | `94b28c86a773f3e87c6d8fecc56693f508439199` |
| D-093 commit | `f7ce35ff0eb310c731b93060775c8ef69b0d36e4` |
| turn-1 subject | `263d2565ab8f230d99fd9bba7c631a33c431e6cf0eb7355184afaaac1614db5d` |
| Claude 2 turn 1 | `2dcb0d20157944e34f417cf8a1882203393ca62f9d2b1e7ec651d7068f0bda10` |
| Codex turn 1 | `76a3dc34f1139db68f96af8d18338820d9e5ec064b06b99c5122df9d09d83374` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
