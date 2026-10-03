# CODEX2 review — M3-Q0 r4

**Verdict: REQUIRED-FINDINGS.** Both r3 required findings are resolved. One new required finding affects the host RSS identity join introduced while addressing r3 N01. No substantive change outside the revision table was found.

Reviewed subjects:

- `docs/implementation/m3/harness/DESIGN.md`: 107,617 bytes; SHA-256 `f7afe2755e21c0f11dfb2fb071d4d8a89d293a1932b1590c1ad385df0fa9adec`.
- `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json`: 53,642 bytes; SHA-256 `b6c7d8ae34eb0ac4759a3b9ec330cc6b914c69aee2534932d95c08c9c3fb3006`.

Both match REQUEST.md. Retained r3 subjects also match their recorded hashes, `b69c918f5fa5976285970dcda015cd98e3f04da706bf4c62d89a3c5900d73a04` and `f38b3f2046172b4365179694fe625a7936e107b95c937f341606c404de7fd96b`. ENV below means the reviewed r4 schema.

## R3 finding resolution

| Finding | Resolution | Evidence |
|---|---|---|
| C2-Q0-R3-01 — missing warmup reason carrier | **RESOLVED** | ENV:215–291,1468,1580–1587 requires nonempty `slotReasons` rows with typed priming, warmup or measured slots. DESIGN:795–807,817–823 carries warmup-only failures without changing measured positions and consults the correct slot for coverage. |
| C2-Q0-R3-02 — reasons erasing known samples | **RESOLVED** | DESIGN:797–807,820–842 and ENV:5 define quantity-specific invalidation. Missing/invalid operational records preserve all four numeric samples, any affected slot still makes the batch incomplete, and aggregates remain available when their inputs exist. |

R3-N02 is resolved at DESIGN:749–758: successful calibration cases and expected-incomplete loss cases are separated. R3-N01's buffering, ambiguity rejection, retained history and birth-history-only sentinel explanation are supplied at DESIGN:731–744. Its new host-key reconciliation needs the correction below.

## Required finding

### C2-Q0-R4-01 — Kernel process start precedes the proposed host-join interval (P2)

**Locations:** DESIGN:710,730–734,769. **Relation:** new error in the response to C2-Q0-R3-N01.

The new join maps a host record to the lifetime whose interval **from the fork-event timestamp to the terminal record contains the host's process start**. The stated identity uses kernel process start time. That start is established before the fork notification is timestamped.

Linux v6.18 assigns `start_time` and `start_boottime` at `fork.c:2181–2182`, then calls `proc_fork_connector` at line 2279. The connector separately timestamps that later notification with `ktime_get_ns()`. Thus a genuine kernel start precedes the interval's lower endpoint. [Fork source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/fork.c), [connector source](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/connector/cn_proc.c).

The representations also differ: `/proc` stat field 22 derives from time-namespace-adjusted boot time converted to clock ticks; connector timestamps are monotonic nanoseconds. Units, clock domains and quantization need an explicit bridge. [Proc stat source](https://raw.githubusercontent.com/torvalds/linux/v6.18/fs/proc/array.c).

Even after normalization on an unsuspended host, a single unambiguous lifetime can have:

```text
host kernel start:     100.000 s
fork notification:     100.001 s
terminal record:       100.200 s
```

The correct host start is outside `[100.001, 100.200]`. DESIGN:769 therefore finds no match and forces `unjoinable-identity`/`incomplete`, despite correct records and no loss or PID reuse.

The rejection is conservative and prevents false PASS, but breaks the intended complete-run path for valid host RSS observations.

**Required change:** retain an explicit same-generation bridge between the host's kernel-start identity and the harness lifetime generation, with defined clock domains, units and tick quantization. Match through that bridge, or specify sound generation bounds whose lower endpoint can precede actual creation. Keep unavailable or ambiguous bridges incomplete. Add a design reference case where kernel start precedes its fork notification and the registered bridge joins it correctly. Do not discard an unmatched host value.

No additional non-blocking observations are raised.

## Listed reference cases

Static inspection confirms the accepted examples at DESIGN:825–829 are representable:

- warmup-0 `record-missing` preserves all 28 measured values and eligible aggregates;
- measured-0 `record-missing` preserves all four values;
- `event-loss` removes own high-water sum and peak while retaining elapsed, concurrent sum and the eligible median;
- `run-failed` invalidates all four numeric benchmark samples in that slot.

The schema rejects the cases at DESIGN:830–836: empty `slotReasons`, empty reasons within a slot, warmup index 3, legacy `runReasons`, reasons on a complete variant, and a reasoned row claiming `within`. The declared semantic rules reject the cases at :837–842: incorrect per-quantity nulling, a null measured value justified only by a warmup reason, and duplicate affected-slot rows.

This was static inspection of the schema and rule text. No validator or reference implementation was executed, and the author's claim of having performed reference checks was not independently reproduced.

## Change scope and verification

All eight DESIGN diff hunks and four schema diff hunks map to the declared table: revision metadata, the two required fixes, N01/N02 RSS clarification, validator reference cases and the QD-27 decisions-index entry. The schema changes only its description, the `slotReason` definition, and replacement of `runReasons` with typed `slotReasons`. All 40 object schemas remain closed; no number-typed fields were introduced. The required finding is within the declared N01 response, not hidden scope expansion.

Review used read-only static comparison with retained r3 subjects/review and primary Linux v6.18 source for the new join. No product code, tests, builds, validator runs, corpus fetches, benchmarks or runtime-home access; no commits. Only the requested two r4 review artifacts were written.
