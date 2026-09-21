# Independent review — proposed clock use-age and mapping 302

**Standing:** policy critique of frozen `clock-observation-proposal-wip-302-r1`. Unselected producer/host-ordering candidate that accepts the independent 300 findings. Not native adapter, OS qualification, current authority, or cumulative approval. A separately frozen host-collector pilot 304 is **not** treated as qualification and does **not** change this verdict. Installed product remains `fa72e50`. Prior 298–301 reports were not edited.

Python 3.12.13 `-I -B`. Review-local copies only. Frozen `cases.json` / `mutation-report.json` were not overwritten.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **194332 B, 41 members, SHA256 `f690bba8715af3e6e8308ed808f8b64ee69f7ef6c345b4f9ad85a8a0466953c9`**. Standing: proposed sampling use-age and existing causal mapping; unselected/unqualified. Extract rehashed **41/41**. Live 300 tar `ec72cd97…54e0` and live 301 tar `b6db23ad…906b` match. `projection.py` is byte-identical to parent 300 `model.py` (`5639b0a7…a4b2`). Workflows `FAULT_TO_ERROR['host-io']` = `HOST.IO_FAILURE`; `EXIT['operational-failed']` = 4. D9 maps `HOST.IO_FAILURE` to `(operational-failed, 4, HOST.IO_FAILURE)`.

Independent live: **237 cases / 89 accepted**, equal frozen `cases.json`. Parent 300 formation **132 / 55** retained. 12/12 controls core-equal frozen `mutation-report.json` (SHA256 `f53f22c5…a05f`). Initial `check_mutants.py` non-unique matcher (`exclusive-use-limit` count 2) is preserved in `mutation-check-r1.stdout`; corrected script ran after, production projection unchanged.

---

## What 302 changes relative to 300

Accepted 300 findings: the 1 s **collection** ceiling is restated as an availability/uncertainty engineering choice, not derived precision; a separate **use-age** bound is specified; public mapping uses an existing arm rather than a new CLOCK.* code.

Kept from 300: floor-second W, u128 midpoint-then-floor M, normalized boot UUID, inclusive 1 s sample span, no wall-only fallback, historical replay of stored W/M/B, S4/S6 constants unchanged.

Added:

1. Inclusive 1 s **total use-age** = `guard.after − original.before` (wide ns), requiring each sample to pass 300 formation, same boot, and `guard.before >= original.after`. Not floor-second M or wall elapsed.
2. **Placement:** finish authentication/context/custody first; sample; S4; if writes, prepare 222 proof/deps/temp **before** the final guard; guard immediately before authoritative clock publication; consume in the same control flow (no permit/queue/callback). Report-current uses the same guard with no prep I/O.
3. Guard failure **discards the proposal**; does not publish F/L/anchor; durable proof orphans may remain under 222. Once publication **starts**, original durability/uncertainty applies; no undo/retry-as-never-started.
4. Sampling unavailability **after** platform admission → existing `host-io` → `{class: operational-failed, errorCode: HOST.IO_FAILURE, faultCause: host-io}`, exit 4, **no domainDetail**. NT-TCB, S4 refusals, cancel, observer latch, and write/publication uncertainty keep their owners.

The model proves only the numeric predicate and reuse of mapping constants. It cannot prove nonlinear host state, permit consumption, or provenance.

---

## Findings

### 1. 300 gaps — addressed as policy text, 1 s still unqualified

The rationale correction is real. The use-age predicate is the missing sample-to-write bound, measured conservatively on sleep-inclusive monotonic endpoints, not wall. Mapping names an existing arm instead of inventing CLOCK.*.

**1 s remains an unqualified candidate, not a spec contradiction.** No profile measurement in this freeze (and the 304 pilot is out of scope for this verdict) shows that collection-plus-proof-prep-plus-guard typically fits 1 s under load/suspend. If proof preparation is often longer than 1 s, the candidate is operationally unavailable; that is a qualification result, not a logic error. Do not select 1 s from this archive alone.

The two 1 s numbers **share one monotonic envelope**. Age includes original collection. A max-span (1 s) original sample leaves **no** remaining budget for compute or guard unless the guard is a zero-span read exactly at `original.after`. That is consistent with “total age” and is an availability coupling the freeze should keep explicit.

### 2. Ordering vs write-ahead — no contradiction found

Sampling after authentication, preparing proof **before** the final guard, and refusing authoritative clock publication on age failure **corrects** 300’s blanket “before any S4 write.” S4 kernel evaluation may run and propose writes; publication of F/L/anchor is what the guard gates. That matches 301: write-ahead is durable only once publication starts; later role/expiry refusal preserves it. Guard failure before admission is not a started write.

Orphans after failed guards are an honest 222 residue, not a clock revision. Automatic cleanup is correctly not authorized here.

**Open, not a cycle in the numeric spec:** native 222 must keep proof/temp-capsule durability off the authoritative clock fields. This proposal assumes that split; the model cannot prove it.

### 3. No impossible atomic guarantee

The text explicitly cannot bound syscall completion or eliminate post-read descheduling. That matches physical reality and the pinned OBSERVER_OBLIGATION style. A passing guard is an admission-check obligation plus qualification of the no-intervening-work path, not `clock_gettime`+fsync atomicity. Good. Native host code that inserts waits after the guard would **invalidate** the predicate; the model cannot enforce that.

### 4. HOST.IO_FAILURE — acceptable existing arm, operationally coarse

Witnesses check out: workflows `FAULT_TO_ERROR['host-io']` and the `operational-fault` branch (no required `domainDetail`); D9 `HOST.IO_FAILURE` → exit 4. `OBSERVER.FAIL_STOP` already uses the same public code. Mutant `misclassify-as-busy` refuses the retry-shaped `LEDGER.BUSY_TIMEOUT` arm.

This is a **new selection** of an existing arm for “cannot obtain a usable current sample,” including span/age/boot-change, which are not disk I/O. Opacity (no CLOCK detail) is the cost of not minting a public diagnostic. **Installation requirement:** host-io recovery/journal paths must not treat sample-age failure as storage corruption. Earlier NT-TCB / S4 / cancel / write owners must not be relabeled. That is integration law, not a wrong constant in `mapping()`.

### 5. Stale guard reuse / effect grant / historical replay

Refused purposes `historical-replay` and `effect-grant`. Guard projection cannot replace the original observation (`substitute-guard-observation` caught; `guard-different-wall-never-substitutes-original` still keeps original W). Report-current cannot skip age (`stale-report-accepted`). Floor-second age is refused. These are the right negatives.

---

## Classification

**Actionable defects in this freeze:** none that make the **policy shape** self-contradictory.

**Still missing / unqualified**

- Measured support for 1 s collection **and** 1 s total use-age (coupled envelope) under load, suspend, and long proof prep. Until then, 1 s is an **unqualified candidate**.
- Native encoding of: no work between guard and dispatch; 222 orphan vs clock fields; host-io must not mean storage recovery; sample taken in admitted namespace.

**Open integration requirements:** as listed in PROPOSAL “Qualification before selection,” plus the host-io operational-response constraint above.

**Reasonable unselected choices:** 1 s vs 10–100 ms; `host-io` vs a future CLOCK detail (they correctly did not mint one); inclusive age.

**Not found:** silent S4/S6/schema change; treating the guard as a new kernel observation; retry-as-never-started after publication start; 304 as qualification.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 302 pins before extract | match |
| Nested 300 / 301 live tars | match |
| Live cases | 237 / 89, equal frozen |
| 12 use-age controls | frozen-equal |
| 300 formation projector | unchanged |
| 1 s freeze / OS qualification | **not decided by this archive** |

---

## Verdicts

- [x] **302 as proposal:** archive verified; 300 findings addressed in text (rationale, use-age, existing-arm mapping); numeric predicate 237/89 and 12/12 reproduce; no impossible atomicity claim; no silent kernel retune.
- [ ] **Not selected.** 1 s remains an unqualified availability candidate. Native host/profile evidence is still required. 304 does not qualify it. No implementation or product installation follows.
