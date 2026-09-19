# Independent bounded review — composed-open reference 120

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-18. Request: `REQUEST.md`.
Subject: frozen `composed-open-reference-checkpoint-120`, addressing my reference 118 I-1, R-1, R-2, R-3
and 116 N-1, N-2. Per-finding closure; nothing inferred from earlier scoped reviews. No frozen/selected/
product edit; scratch copies with bytecode writing disabled; no commit, push or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,075,948 bytes, SHA-256 `85937fd5da8fa834cc1a7c6d21fa84992558fdbc3a2d58e23c49644e68fe2cbc` = request and `archive-pin.json` |
| Members | 1,389/1,389 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified clean afterwards |
| Candidate | 1,284/1,284 pins equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 118 extraction |
| Delta | the 11 declared: contract, `generation_dispatch_reference.py`, both case files, `check-security-lifecycle.v1.py`, `check-carrier-v3.py`, five pin inventories. The model (`security_lifecycle_model_v1.py`) and `generation_reference.py` are unchanged |

**Owner checks reproduced, required order, fresh output**: envelope receipt 168 / 145 / 1,803 / 6,000
passed → integration **423 / 0** → security **581 / 0, 19 sweeps** (anchors 65, dispatch/floor/open
141, catalog 30) → integrated carrier **427 / 0**.

## 2. What changed
`open_disposition(project_key, first_generation, rows, markers, witness_observation,
floor_observation)`: (1) `dispatch(…, _reconcile=False)` binds carrier, markers, witness and
generation and returns every refusal, marker proposal for absence, continuation or unavailability —
or an internal `RECONCILE` token; (2) for that token only, `start_floor_disposition` on the **witness
generation's** rows; anything other than `OK` / `FLOOR_ABSENT` is returned; (3) otherwise the ordinary
`dispatch`. The contract states the order, says "no ADVANCE or REVERT may be executed from the
lower-level dispatcher before the composed result", rewrites both empty-generation sentences, and names
the catalog snapshot version's owner and range.

## 3. Evidence

**Composition grid against my own oracle** (`probes/open_grid.py`; the oracle is written from S7.1's
prose and never calls `open_disposition`): 3 shapes × 2 generations × `first_generation` ∈ {1,2} ×
5 marker maps × 28 witness observations × 12 floor observations of the witness generation =
**30,240 cells, 0 violations** of: oracle equality; the internal token never returned; no
OK/REVERT/ADVANCE/INIT where the floor quarantines; marker iff QUARANTINE; never a second marker.
The floor changed the plain dispatcher's answer in 4,500 cells — including **360 REVERT → QUARANTINE and
100 ADVANCE → QUARANTINE**, which is exactly the 118 I-1 hazard — and in none of them did a witness act
survive.

**Mutation** (owner sweeps called directly; no pin gate in that path): my 118 set re-based plus seven
composed-open mutants — **62 run, 55 killed, 6 survived, 1 harness error** (an anchor of mine that does
not exist in the 120 text; not counted either way — my grid asserts that property instead).
- Order reversed (reconcile before floor), floor ignored, `FLOOR_ABSENT` blocking reconciliation,
  preliminary refusal bypassed for a quarantined generation: all **killed**.
- 118 R-3 ("superseded scope from W1 alone"): now **killed**.
- Act C with the TERMINAL-tail requirement removed: now **2 failures** (was 425 / 0) — 118 R-2.
- Catalog numeric comparison (`"07"` matching 7): now **killed**; all five catalog mutants killed — 116 N-1.
- Survivors: the four I classified as equivalent in 111/118, and **two new ones, both real** (§4 F-1).

## 4. Findings

- **F-1 (low–medium, tests) — which generation's floor and rows the composition uses is unpinned.**
  Two mutants survive all 141 owner checks: selecting the floor of **generation 1 always**, and checking
  the floor against the rows of the **highest-numbered generation key** instead of the witness
  generation. Both are real: in my grid they produce **4,176** and **30** oracle violations
  (`probes/survivors.json`), the second including a *false quarantine* — witness `COMMITTED(1,2)`, rows
  1–2, floor at 1, an empty generation-2 key present ⇒ `QUARANTINE uncertainTailLoss(1)` instead of `OK`.
  The 70 open cases evidently never combine a witness generation other than 1 (or a higher empty
  generation key) with a positive floor. A handful of generation-2 cases closes it.
- **F-2 (note) — `dispatch` alone still returns REVERT/ADVANCE without any floor check**, and
  `_reconcile=False` is a keyword on a public function. The contract sentence forbidding acts from the
  lower-level dispatcher is the right rule; in the Rust integration make the lower-level function
  private to the composed entry so the wrong order is unrepresentable rather than forbidden.
- **F-3 (note, chosen precedence)** — a malformed or wrong-key floor now *suppresses* a tail-loss marker
  the witness would have earned (2,048 cells: plain `QUARANTINE` → composed `REFUSE`). That follows the
  table ("malformed witness/floor … none; refuse without marker") and the no-continuation limit, so a
  damaged floor file makes the carrier permanently refused in this profile. Coherent; list it with the
  disclosed limits so it is a decision and not a surprise.
- **F-4 (note, inherited limit)** — `FLOOR_ABSENT` lets reconciliation proceed, as v8's start sequence
  always did. A writer cannot tell "never created" from "deleted"; only the first operation of a
  generation can lawfully have rows without a floor. The read-only side refuses on absence; the writer
  side cannot, or no generation could ever start. Worth one sentence.

## 5. Closure

| Finding | Status |
|---|---|
| **118 I-1** composed, floor-first open disposition with cases | **Satisfied as a reference** before Rust integration: one inert result, order proven on 30,240 cells against an independent oracle, order-reversal mutant killed. F-1 should be closed in the same successor that feeds the Rust port. |
| **118 R-1** text vs model on empty generations | **Closed** — both sentences now distinguish an *unbound* generation (refuse, no marker) from a *lawfully bound empty* one (same-generation table ⇒ `uncertainTailLoss`). |
| **118 R-2** unpinned TERMINAL-tail conjunct | **Closed** — mutant now fails 2 checks; non-TERMINAL inherited tail refuses act C with no SQL writes. |
| **118 R-3** W1-only superseded mutant | **Closed** — killed. |
| **116 N-1** non-canonical decimal subjects | **Closed** — numeric-comparison mutant killed; sweep 24 → 30. |
| **116 N-2** owner of the version's range | **Closed** — admitted catalog `snapshotVersion`, 1..2⁶³−1, owned by catalog admission and closure construction; absent member cannot match. |
| **118 I-2** external admission obligations | **Open by design**; nothing here implements SQL admission, file capture, marker writing, leases or authority. |

## 6. Bounded verdict
**Reference 120: reviewed, no blocking finding. 118 I-1 is satisfied at the reference level; 118 R-1,
R-2, R-3 and 116 N-1, N-2 are closed. F-1 (two surviving generation-selection mutants, both real) is
the one follow-up I would want before the Rust port copies these cases.** Not approval of any writer,
capture, SQL admission or Rust code; not cumulative approval or selection.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `dispatch.diff`, `contract.diff`,
`checks/*`, `probes/open_grid.py` + `open-grid.json`, `mutation.{py,json,log}`, `survivors.{py,json}`,
`actc_mutants.py` + `actc-mutants.json`, `catalog_mutants.py` + `catalog-mutants.json`, `hashes.txt`.
