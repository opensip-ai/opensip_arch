# D-094 — D-006-conforming G03/G04 machine pins and named harness identifiers

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a SATISFIED
> re-record. Frozen D-093 subjects are not edited. Not a
> fifth D-056 Class A/B SATISFIED.
> **Decision type:** PREFERENCE-LADEN for exact machine pins,
> OS family, cache-state protocol, product sign-off, and the
> native-Intel procurability finding (same class as D-006).
> RULE-GOVERNED for writing the v3 reserved identifiers into
> file 08 once those pins exist (D-086 / D-088 rider).
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** execute G03 or G04. **Does not** claim
> QUALIFIED or DEMONSTRATED. **Does not** change D-006
> numeric thresholds. **Does not** restore G17. **Does not**
> name G13. **Does not** silently substitute Rosetta.
> **Does not** overturn D-006, D-077, D-086, D-088, or D-093.

D-006 is ADOPTED (CONSENT `bfd8a758…`). D-086 is ADOPTED at
`14865abc42c13b9759f5761c2873db03b708ea32`. D-088 is ADOPTED
at `94b28c86a773f3e87c6d8fecc56693f508439199`. D-093 is
ADOPTED at `f7ce35ff0eb310c731b93060775c8ef69b0d36e4`.
This entry does not overturn those.

`gate-harness-naming.v3` already reserved, and forbade
counting as named, the identifiers
`harness.DR-G03.core-startup` and
`harness.DR-G04.core-memory` until a D-006-conforming
successor pins machines, OS versions, cache-state protocol,
product sign-off, and native-Intel procurability, or a D-006
successor routes unprocurability.

## Procurability finding (product sign-off, this date)

Native Intel Mac hardware remains scarcity-exposed
(D-006 OBS-T3-02) and is **procurable** for this pin, not
unprocurable. Evidence used for that finding, not as the
machine identifier:

- GitHub Actions published `macos-15-intel` as the last
  hosted native x86_64 macOS image, available from
  2025-09-19 until the macOS 15 image retires (stated
  August 2027 / Fall 2027). Changelog
  `github.blog/changelog/2025-09-19-github-actions-macos-13-runner-image-is-closing-down`
  and `actions/runner-images#13045`.
- That label is a **measurement venue**. It is allowed only
  when the harness records a native Intel CPU brand string
  and `sysctl.proc_translated = 0`. It is not Rosetta. It is
  not the representativeness pin.

Because procurability is verified, this entry is the
D-006-conforming naming act. It is **not** a D-006 successor
that drops macOS x86_64 or changes numeric thresholds.

## Pins (execute D-006's runner class; do not rewrite it)

1. **macos-arm64-ref.** Apple Mac mini, M1-class entry chip,
   8 GB unified memory, native arm64, macOS 15 Sequoia
   family, SIP and AMFI on.
2. **macos-x86_64-ref.** Apple Mac mini 2018-class, native
   Intel Core i5/i7, 8 GB, native x86_64, macOS 15 Sequoia
   family, SIP and AMFI on. Never Rosetta. Never an Intel
   userspace on Apple Silicon. Never a translated binary.
3. **linux-x86_64-ref.** 4 vCPU / 8 GB, Ubuntu 24.04 LTS,
   x86_64.
4. **linux-arm64-ref.** 4 vCPU / 8 GB, Ubuntu 24.04 LTS,
   aarch64.

Exact image build / Darwin build / AMI or runner-image
digest is recorded in the first harness run record. The
family pins above are the architecture decision. A venue
that does not match the class is rejected at qualification,
not silently substituted.

## Cache-state protocol

**Cold.** Single-user. No other OpenSIP process. Drop page
cache (`sudo purge` on macOS; `sync && echo 3 | sudo tee
/proc/sys/vm/drop_caches` on Linux). First exec of the
gate's `--help` / `--version` (G03) or the D-006 G04
lifecycle commands (`--help`/`--version` and `doctor`
read-only). Record boot-id, purge output, vm_stat or
`/proc/meminfo` before and after, load average, process
list, SIP status, and on macos-x86_64-ref
`sysctl.proc_translated` which must be `0`.

**Warm.** Immediately after one completed cold pair, same
binary path, no intervening purge, no other workload.
Record the same traces plus that purge was not repeated.

**Fixed image.** No unattended OS update during the sample
window. Analyze RSS and doctor-with-consented-probes RSS
remain outside D-006 (unchanged).

## Decision

1. Record the pins, cache-state protocol, product
   sign-off, and native-Intel procurability finding above
   as the D-006-conforming G03/G04 naming act.
2. Write the v3 reserved identifiers into file 08 as named.
   They remain not authored and not QUALIFIED.
3. Condition 4's named-harness half becomes 18 of 18
   required. Owners remain 22 of 22. Claims half remains
   abstinence. Standing becomes **MET**. MET is not
   QUALIFIED. MET does not authorize implementation.
4. **Exact file-08 edits, and no others:**
   - Replace this unique G03 harness-cell prefix (occurs
     once):

```
reserved, not named (D-006 machine pins owed; D-086). cold-cache harness, p50/p95/p99, fixed runner image
```

     with

```
named: harness.DR-G03.core-startup (D-094; D-006 machine pins recorded; not authored; not QUALIFIED). cold-cache harness, p50/p95/p99, fixed runner image
```

   - Replace this unique G04 harness-cell prefix (occurs
     once):

```
reserved, not named (D-006 machine pins owed; D-086). same runners and lifecycle commands
```

     with

```
named: harness.DR-G04.core-memory (D-094; D-006 machine pins recorded; not authored; not QUALIFIED). same runners and lifecycle commands
```

   - Replace this unique condition-4 "Measured now" fragment
     (occurs once):

```
**16 of 18 required gates name a recorded identifier** (D-086 / D-088; not authored; not QUALIFIED); G03/G04 remain required and unnamed pending a D-006-conforming successor
```

     with

```
**18 of 18 required gates name a recorded identifier** (D-086 / D-088 / D-094; not authored; not QUALIFIED); G03/G04 named under D-006-conforming pins (D-094)
```

   - Replace the condition-4 standing cell `| **PARTLY MET** |`
     (occurs once in the snapshot table) with
     `| **MET** |`.
   - In "What that means in one sentence", replace only
     `condition 4 is PARTLY MET` with
     `condition 4 is MET`.
5. Does not edit D-088's other gate-harness cells. Does not
   name G13. Does not restore G17. Does not mark any DR row
   SATISFIED. Does not authorize `docs/v2/implementation/`.

## Alternatives

- Leave G03/G04 unnamed until a physical lab exists.
  Rejected: D-006 required this naming act; procurability
  is verified; continued 16/18 is not forced.
- Treat `macos-15-intel` as the machine identifier.
  Rejected: it is a venue; the representativeness pin is
  the 2018-class native Intel Mac mini.
- Measure Intel on Rosetta or on Apple Silicon.
  Rejected: D-006 SF-02 / OBS-T3-02.
- Route unprocurability and drop macOS x86_64. Rejected:
  procurability is verified; this is not that successor.
- Present 18 of 16, or keep 16 of 18 after naming.
  Rejected: GHN-V2-B1 / D-088 arithmetic.
- Count reserved v3 identifiers as already named.
  Rejected: GHN-V1-B2; zero progress until this act.
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
prefixes, the 16-of-18 condition-4 fragment, the PARTLY MET
standing cell, and the "condition 4 is PARTLY MET" clause.
Does not overturn D-006, D-086, D-088, or D-093.

## Measured inputs at dispatch

| Path | sha256 |
|---|---|
| COORD | `4ec069882b41ab5e14668e86cfac8dd977ac850c495c9f4f2ccadf05be107f20` |
| file 08 | `45dc4611717276c1f1c275982aa7ce787b2fa0b8fffbe1d315e8cb83ddff2206` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-086 commit | `14865abc42c13b9759f5761c2873db03b708ea32` |
| D-088 commit | `94b28c86a773f3e87c6d8fecc56693f508439199` |
| D-093 commit | `f7ce35ff0eb310c731b93060775c8ef69b0d36e4` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
