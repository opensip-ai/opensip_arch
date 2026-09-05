# D-099 — D-006 fleet-class successor plus G03/G04 named identifiers

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a fourth
> turn of CONTESTED D-098. Frozen D-098 subjects are not
> edited. Not a SATISFIED re-record.
> **Decision type:** PREFERENCE-LADEN scoped D-006 successor
> plus RULE-GOVERNED naming of the v3 reserved identifiers.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** execute G03 or G04. **Does not** claim
> QUALIFIED or DEMONSTRATED. **Does not** change D-006
> numeric threshold numerals. **Does not** restore G17.
> **Does not** name G13. **Does not** silently substitute
> Rosetta. **Does not** overturn D-094 or D-098 CONTESTED,
> D-096, or D-097.

D-098 is CONTESTED at `09d0e288509f8b3e58d035290ff26f2e1d29c4ce`.
This cycle inherits the D-098 turn-3 contract
(`coordinator-decisions.D-098.turn3.draft.md`
`5ad6884a06aa450bc2cbc0f286b3366eb9e029922e92a0ae6937868e37e05031`)
except the process-architecture observation, which is
replaced below. ADV-D098-T3 (Codex SHOULD-FIX) accepted.

## Process-architecture observation (replaces D-098 t3 item 2)

Thin, single-architecture artifacts only. Fat/universal
binaries are rejected at preflight.

Launch the **target** binary. Record its PID as T.

- Linux: process/executable arch is `file -L /proc/T/exe`
  (the target PID, never `/proc/self/exe` of the
  inspector). Host arch remains `uname -m`.
- macOS: spawn with explicit `arch -arm64` or
  `arch -x86_64` matching the class. Process arch is that
  spawn arch. Confirm with `file` of the thin launched
  path (one Mach-O slice). Translation:
  `sysctl.proc_translated` read **from a helper exec'd
  under the same `arch`** immediately before exec of the
  target, or from the target via a documented
  `--print-native-arch` / equivalent if present; an
  inspector-process sysctl is not the target observation.

Host, executable, and process architecture must all match
the class. Value 1 → reject. 0 or ENOENT → accept only
with those matching facts. Other error → reject.

Never Intel on Apple Silicon. Never Rosetta.

All other D-098 turn-3 contract text stands: five
operative G03 quantiles, paired 10% from second release,
no weekly-image rebaseline, G04 series, N=21 nearest-rank,
audit-only storage, ImageVersion, `runs-on` label.

## Decision

1. Adopt the inherited D-098 turn-3 contract as amended
   by the process-architecture observation above.
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

- Fourth turn of D-098. Rejected: CONTESTED; new cycle only.
- Keep `/proc/self/exe` or inspector sysctl. Rejected:
  ADV-D098-T3.
- Flip condition 5. Rejected: C2 NOT MET; C5 last.
- Authorize implementation. Rejected: C5 last.

## Readiness effect

Condition 4 becomes MET. Condition 2 stays 4 of 30 NOT MET.
Condition 5 remains NOT MET and last.

## Reversibility

C-D099 plus restore of the two reserved cells, 16-of-18
fragment, PARTLY MET, one-sentence clause, and D-006's
pre-successor exact-machine, exact-OS, and original runner
classes. Does not overturn D-098 CONTESTED.

## Measured inputs at dispatch

| Path | sha256 |
|---|---|
| COORD | `0984005085b96920c2b4d3d561e950853bd40b6d97ee2cac77e457d647fe301b` |
| file 08 | `45dc4611717276c1f1c275982aa7ce787b2fa0b8fffbe1d315e8cb83ddff2206` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-098 commit | `09d0e288509f8b3e58d035290ff26f2e1d29c4ce` |
| D-098 turn-3 subject | `5ad6884a06aa450bc2cbc0f286b3366eb9e029922e92a0ae6937868e37e05031` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
