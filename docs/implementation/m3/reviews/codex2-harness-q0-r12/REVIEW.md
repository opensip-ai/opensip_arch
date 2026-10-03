# CODEX2 — M3-Q0 r12

**Verdict: REQUIRED-FINDINGS.** One new required finding and two non-blocking observations.

| Reviewed subject | Bytes | SHA-256 |
|---|---:|---|
| DESIGN.md (r12) | 148609 | `72e70548b78843699bde2176231b909af6b549e7b30921b687bb1d6b463f2c36` |
| exploratory-quality-envelope.schema.v1.json (r12) | 60031 | `d05472ec700d8e8282b220f3d0d0b9530d00eafbe8f981eeeebf4c801a75d961` |
| DESIGN-r11.md | 143572 | `c003a06a8d5eaa0ceb414f9458dc52d1fc644b304cf3aa73db6ef00317fac933` |
| exploratory-quality-envelope.schema.v1-r11.json | 59433 | `8769ed0c156d5496d9df6640eab29c1a219303768ede9c417b59dc638d4f6975` |

## Decisions requested

**R11-01 is resolved.** [QD-35](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:867) withdraws macOS settlement, and the [macOS measurement rules](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:882) null `elapsedNanos` while retaining root-reaped timing in a separate informational field. That field does not enter the elapsed median or budgets. Every macOS measured slot has a platform settlement reason, so its row cannot be complete. OI-20 records the missing settlement source. The new calibration cases cover the live-descendant counterexample and ordinary macOS runs.

**R11-N01 is resolved.** The clean inherited mount is under [expected complete](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:886); unavailable Linux and macOS are under [expected incomplete](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:896).

**The full delta fits the response table.** No unrelated substantive change found. Linux settlement remains unchanged. The Linux/D12 disclosure describes the presently supported complete measurement method; the record's standing and D13 dependency still prevent it from independently authorizing qualification. The new informational field has the availability error below.

## Required finding

### C2-Q0-R12-01 — P2 — Allow unavailable informational timing when no root was created

**Locations:** [ENV invariant](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:5), [nullable carrier](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:1659), [mandatory macOS reason](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:867), [informational timing definition](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:882), [failed-slot retention](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:967).

ENV now requires `rootReapedElapsedNanos` to be non-null on a measured slot **if and only if** that slot carries `settlement-unverified-platform`. Every macOS measured slot must carry that reason. This makes availability of a root-reaped duration unconditional on macOS.

**Static counterexample:** a macOS measured launch fails before creating its root. Apple documents that a `posix_spawn` error can create no child. There is then no root-reaping event and no duration meeting the new field's definition. [Apple launch documentation, Return Values](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/posix_spawn.2.html)

The design keeps failed runs in their original slots, forbids rerunning to fill them, and accepts `run-failed` with the defined quantities null. The failed slot therefore remains, with the macOS platform reason and the applicable failure/record reasons. A truthful null informational value passes the nullable structural carrier but violates the new validator invariant. Supplying a number would invent a root-reaped measurement.

**Required correction:** require a root-reaped duration only when root creation, observed reaping and valid monotonic timestamps establish it. Keep the mandatory macOS platform reason and incomplete status, but allow null informational timing with a typed failure or absence explanation when that evidence does not exist. A failed run whose root was actually reaped may still keep its known informational duration. Align ENV's invariant, DESIGN and the reference cases; include a retained macOS failed-launch slot with no root and null informational timing.

## Non-blocking observations

### C2-Q0-R12-N01 — P3 — Qualify or supersede the retained r11 settlement cases

The [old accepted case](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:1056) still promises known elapsed for unavailable Linux **and macOS**, and the [old settlement model](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:1059) lacks a Linux qualifier. The operative r12 rules and new cases correctly override those macOS conclusions. Make the old cases Linux-only or mark their macOS branch superseded, so the current reference suite has one expected result.

### C2-Q0-R12-N02 — P3 — Attribute the OS-dependent rejection to the validator

The [new reference case](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:1071) says the schema rejects a macOS row claiming `within`. Its [complete-row branch](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:1422) has no OS-dependent condition; that rejection follows from the semantic validator's mandatory macOS platform reason. Move this case under the validator heading. The schema does correctly reject the informational field on a complete row.

## Review limits

Static review only: full subject comparison, hash/size checks, schema structure/reference inspection, failure-slot and nulling analysis, three independent review slices and primary Apple documentation. The schema has 41 closed object definitions, no floating-point types and no unresolved local references. No product code, tests, builds, validators, reference implementations, corpus fetches or benchmarks were run. No runtime home was accessed and no commit was created. Writes are confined to the requested r12 review directory.
