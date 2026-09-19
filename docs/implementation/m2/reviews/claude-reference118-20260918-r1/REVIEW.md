# Independent bounded review — generation corrections reference 118

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-18. Request: `REQUEST.md`.
Subject: frozen `generation-corrections-reference-checkpoint-118`, the correction of my reference 111
findings F-1 to F-4 and N-1 to N-3. Per-finding closure only; nothing is inferred from earlier scoped
reviews. No frozen/selected/product edit; scratch copies only (bytecode writing disabled throughout);
no commit, push or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,030,600 bytes, SHA-256 `315483f7370902950aa3cffd3b1d091126e78972bf209a56b8a3e2c3ff98d340` = request and `archive-pin.json` |
| Members | 1,419/1,419 regular, each length + SHA-256 equal to the manifest, read from the tar before any write; 0 unsafe/extra; re-verified clean after all work |
| Candidate | 1,284/1,284 pins equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified extraction of frozen 116 (1,284 files) |
| Delta | exactly the 13 declared: contract, read-only owner, both kernels, both case files, `check-security-lifecycle.v1.py`, **`check-carrier-v3.py`**, five pin inventories. The 116 model and its envelope binding are unchanged |

`generation_reference.py` differs from 116 only in the `decide` docstring, so my 29,019,601-evaluation
schedule result for 111 (0 lawful diagnoses) carries over unchanged and was not re-run.

**Owner checks reproduced in the required order, fresh output**: envelope receipt 168 / 145 / 1,803 /
6,000 passed → integration **423 / 0** with that receipt → security **581 / 0, 19 sweeps** (anchors 64,
dispatch + floor 71) → integrated carrier **425 / 0**.

## 2. Per-finding closure

| 111 finding | 118 | Status |
|---|---|---|
| **F-1** dispatcher cannot express the marker disposition | `{action, marker}`; QUARANTINE names reason + generation; REFUSE and every already-quarantined outcome carry `marker: null`; malformed witness refuses regardless of old markers; separate `start_floor_disposition` | **Closed at the model boundary** — see §3 and the one integration obligation I-1 |
| **F-2** seven behaviour-changing anchor mutants survive | 40 anchor cases incl. three with a different second capture; sweep now uses `secondInput` | **Closed** — all seven killed, plus the dispatcher TERMINAL-cause gap |
| **F-3** `check-carrier-v3.py` models the old act C | act C and resume require the exact admitted COMMITTED witness at the inherited TERMINAL; nine negatives with no-write checks | **Closed**, one small residual (R-2) |
| **F-4** new generation unknown until its first boundary | disclosed in S7.1 and the read-only owner; no proactive zero floor | **Closed** as a disclosure; the owner declined my optional zero-floor suggestion, which is a legitimate choice and is now stated |
| **N-1** causal independence of captures | obligation written into `decide` and the read-only owner; unequal-capture cases | **Closed** as an obligation (unverifiable by a pure kernel, and the text says so) |
| **N-2** unnamed preconditions | admission-owner table naming six projections and their owners; gaps and unclosed predecessors refuse at S7.1 admission | **Closed** |
| **N-3** one malformed marker blocks the carrier | stated as a conservative rule | **Closed** |

## 3. F-1: does the two-kernel form honestly resolve it, or is a unified model needed first?

**It resolves F-1.** F-1 was that a consumer could not tell marker from no-marker. Now every result
determines it. I checked every cell of my 8,064-cell grid (4 shapes × 2 generations ×
`first_generation` ∈ {1,2} × 6 marker maps × 42 witness observations, real canonical bytes) against
the S7.1 table row by row — marker iff QUARANTINE; closed reason vocabulary; never a second marker for
a quarantined generation; malformed/foreign ⇒ REFUSE with no marker whatever old markers exist;
definite absence over a non-empty journal ⇒ `witnesslessRestore` at the highest generation;
same-generation conditions ⇒ `uncertainTailLoss` at the witness generation; anything later than the
witness ⇒ REFUSE with no marker — plus the ten structural properties from 111: **0 violations**
(1,413 `uncertainTailLoss`, 78 `witnesslessRestore`, 3,749 REFUSE). `start_floor_disposition`:
**99 cells, 0 violations** (absent ⇒ observation only; unreadable ⇒ unavailable; malformed or
wrong-key floor ⇒ REFUSE without marker; admitted marker ⇒ no second marker; floor above tail or
digest mismatch ⇒ `uncertainTailLoss`).

**It leaves one new, smaller obligation, and that one is order-sensitive — I-1.** The README says the
writer "must compose applicable floor checks before reconciliation" and that this composition is
external. It is not a formality. `probes/compose-and-floor.json`: rows 1–2 present, witness
`PENDING(1,3)`, floor at 5 (a namespace rollback with an append in flight). `dispatch` alone says
**REVERT**; `start_floor_disposition` alone says **QUARANTINE uncertainTailLoss(1)**. Floor-first writes
nothing to the witness and quarantines; reconcile-first *writes* `COMMITTED(1,2)` into a generation the
floor then quarantines — exactly the witness repair S7.1 forbids in a quarantined generation, and it
destroys the witness that evidenced the rollback. So: **118 is acceptable as the reference; a single
composed `open_disposition` with its own cases should exist before Rust integration**, because that is
where the order will otherwise be decided by whoever writes the caller. I do not think it must block
this checkpoint — the law states the order, and both kernels are individually right.

## 4. Mutation
`probes/mutation.py` — my 111 mutant set re-based on the 118 text, plus 14 new disposition and floor
mutants; judged by the owner's two sweeps called directly, so no pin gate can produce a kill:
**55 mutants, 50 killed, 5 survived.**
- All seven 111 F-2 gaps and both TERMINAL-cause mutants: killed.
- All 14 new ones killed: QUARANTINE without marker, wrong target generation, swapped reasons (both
  directions), malformed or foreign witness or later-journal-generation proposing a marker, malformed
  witness deferring to an old marker again, `FLOOR_ABSENT` treated as OK, floor above tail, floor
  digest, floor key generation, admitted marker ignored, malformed floor proposing a marker, unreadable
  floor treated as absent.
- Survivors: four I already classified as equivalent in 111 (unreadable short-circuits before
  `_stable`; `OK` implies COMMITTED; REVERT/ADVANCE imply PENDING; the forward-gap conjunct is implied),
  and **"superseded scope decided from W1 alone"**, which needs a witness generation that *decreases*
  between the two reads with `k > t`. One case would pin it.

Act C (`probes/actc-mutants.json`, integrated carrier check on a scratch tree; it has no pin gate):
strict-int check removed → 2 failures (so `True == 1` under dict equality is genuinely guarded);
digest and closed shape ignored → 4 failures; precondition skipped → 18 failures;
**TERMINAL-tail requirement removed → 425 / 0, survives.**

## 5. Remaining findings

- **R-1 (low–medium, text vs model)** — S7.1 l.837 still says "A forward generation gap **or COMMITTED
  positive sequence over an absent generation refuses**." With 118's vocabulary "refuse" means no
  marker, but the model (deliberately, per the README) sends a positive COMMITTED or a non-adjacent
  PENDING over an *empty, lawfully bound* next generation to `reconcile_witness`:
  `COMMITTED(2,5)` and `PENDING(2,3)` over a closed generation 1 give **QUARANTINE
  `uncertainTailLoss` at generation 2**, i.e. a marker and therefore continuation eligibility. I think
  the model is right (that is a lost tail of generation 2, and the table's first rows say so). The
  sentence should be narrowed to the unbound case (gap, or predecessor neither closed nor
  quarantined), which the model does REFUSE.
- **R-2 (low)** — no carrier case has a witness that exactly matches an inherited tail which is *not*
  a TERMINAL (act A not performed), so the `tail[2] != 'TERMINAL'` conjunct is unpinned.
- **R-3 (low)** — the surviving "W1 alone" mutant above.
- **I-1 (integration obligation, §3)** — composed open disposition, floor-first, with cases.
- **I-2 (integration obligation)** — everything in the admission-owner table is still prose: complete
  rows with recomputed domain-framed digests, contiguity, origin, predecessor closure, typed file
  presence, marker admission, one snapshot per capture, a genuinely fresh second capture. 118 is honest
  that neither kernel establishes them; the Rust integration review must find each one implemented,
  not assumed.
- Unchanged and outside this correction: D3–D6, R-1/R-2/R-3 of the signed-security group, Linux,
  targets, selection.

## 6. Bounded verdict

**Reference 118: reviewed, no blocking finding. 111 F-1, F-2, F-3, F-4 and N-1 to N-3 are closed at
the reference/model boundary; F-1 specifically is resolved without a unified model, on condition that
I-1 is met before integration. R-1 is a wording correction the next successor should carry.** Not
approval of any writer, capture layer, SQL admission, marker writer or Rust code; not cumulative
approval or selection.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `generation_reference.diff`,
`contract.diff`, `check-carrier.diff`, `checks/*`, `probes/*` (including the preserved failed first
mutation script), `hashes.txt`.
