# Independent bounded review — read-only generation reference 111

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-18. Request: `REQUEST.md`.
Subject: frozen `readonly-generation-reference-checkpoint-111` — the first review of the combined
normative text, models and cases after my D2 r1–r3 adjudications. Those adjudications were of owner
*choices*; nothing here is inferred from them. No frozen, selected or product byte was edited; checks,
mutants and probes ran on scratch copies under `claude-out/`; no commit, push or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,026,352 bytes, SHA-256 `050104a287797487bc833bb85c630119fc3e8f4e87d5b5b3149a4be334009a55` = request and `archive-pin.json` |
| `subject.json` | SHA-256 `9399293ce49ddfdedef0fc34ff56d5e38d7ab7a3c8fc6f9e8cf8d7f1837df3d2` |
| Members | 1,429/1,429 regular, each length + SHA-256 equal to the manifest, read from the tar before any write; 0 unsafe/extra; re-verified after all work |
| Candidate | 1,284/1,284 `frozen-candidate.json` pins equal on disk; none unpinned |
| Parent | `parent-inputs.json` (1,280) equals **my own** verified extraction of frozen 108 file by file |
| Delta | 10 changed + 4 added = the 14 declared: contract `security-and-lifecycle.md` (+100/−1), `commit-recovery-readonly.v3.md` (+72/−11), `carrier-migration.v1.md` (3 rows), `carrier-highwater.schema.v1.json`, `check-security-lifecycle.v1.py` (+61/−2), five pin inventories; new `generation_reference.py` (143 l.), `generation_dispatch_reference.py` (76 l.), `generation-cases.v1.json` (29), `generation-dispatch-cases.v1.json` (49 + 5 floor controls) |

(My first pin comparison mis-keyed paths and is preserved as `candidate-pins.failed-r1.json`.)

**Reviewer error, disclosed.** I ran two checker `--help` commands from inside my *extraction* without
`PYTHONDONTWRITEBYTECODE`, which created 14 `__pycache__/*.pyc` files there; my end-of-review
re-verification caught it ("extra files in extraction"). Every extracted member still hashed equal to
the manifest, and the frozen archive and the repository were never touched. The stray files were moved
(not deleted) to `claude-out/stray-r1/` with a note and the extraction re-verifies clean. All
substantive checks and probes ran on the separate scratch copy `claude-out/tree`.

**Owner checks reproduced in the required order, fresh output, scratch tree, UCD-15 interpreter**:
envelope receipt 168 explicit / 145 composition / 1,803 differential / 6,000 fuzz, passed → integration
**423 / 0** using that receipt → security **581 / 0** with the three relevant sweeps 167 / 49 / 54 →
integrated carrier **406 / 0**. The scratch tree is byte-identical to the extraction afterwards. I did
not rerun foundation, workflows or native (unchanged except pins).

## 2. Is the exact 111 prospective law coherent? — Yes

I read S2.1, S7.1, the read-only owner, the floor schema and the migration rows in full against each
other and against the two kernels. I found no contradiction and no rule that produces a lawful false
diagnosis or an unanchored confirmation beyond the selected interior limit.

- **D2 r3 H-1** (marker/reason table, no-continuation limit): present in S7.1 "Writer marker
  disposition" and the read-only "No-marker refusal limit". *Closed in the text; not in the model —
  F-1.*
- **H-2** (precedence): "Dispatch precedence" puts carrier-format §8 steps 1–3 first and defines the
  lawful witness on `{A}`/`{A,B}`. Closed.
- **H-3**: adopted as SHOULD with the loss disclosed, and correctness explicitly independent of it.
- **H-4**: explicit zero floor defined (never over a positive floor, never inferred from absence);
  lower W2 after retry is the `lowerWitnessGeneration` candidate.
- **Final-floor law, counter/base/migration/quarantine continuation**: one statement each, mutually
  consistent; "eligibility never grants an execution permission" appears where it must.
- **F22 precedence**: floor-above-tail and floor-digest precede the `k > t` branch, which precedes
  the join, which precedes the marker; all as the text orders them, and the kernel follows it.
- **Malformed file stability**: validation is *performed* on stable bytes and its failure is
  reportable (my C2a); `Present(empty)` is malformed, `Absent` needs presence evidence, unreadable is
  unavailable and two failed reads are never "stable" — text and kernel agree.

**Owner choice, adjudicated as asked — agreed.** A decrease `W1 > W2` with both later than `A.g` does
not add a current-generation diagnosis to a historical result. In row H the witness only *selects* the
row; the anchor is the requested generation's final floor, TERMINAL tail, marker absence and `stableH`,
none of which a current-generation anomaly touches, and S7 item 7 gives that anomaly to the
current-generation doctor. Reporting it here would let one defect produce corruption reports for every
historical attempt. If W2 is *below* `A.g` it is no longer "solely among later generations" and the
kernel retries, then offers L — consistent. I did not previously approve this; I do now.
**Clock clarification — agreed**: S4.5 lowers the evaluation-time floor bound in its record; no act
lowers a journal sequence floor. The old schema sentence did conflate them.

## 3. Reviewer evidence

**Frozen read-only kernel over my own schedules** (`probes/schedule_vs_kernel*.py`): real canonical
witness/floor bytes through the real codec, ten separately timed reads per decision, every
non-decreasing placement, memoised captures.

| Schedule | Evaluations | Lawful `unknown-quarantine-condition` |
|---|---|---|
| S1 closure and first new-generation SEAL in one operation | 2,571,804 | 0 |
| S2 closure is the final append | 8,078,954 | 0 |
| S3 crash after TERMINAL, next start copy | 4,625,438 | 0 |
| S4 crash at `PENDING(2,1)` → `COMMITTED(2,0)` | 13,743,405 | 0 |

The kernel's historical numbers equal my independent r3-adjudication model exactly (S2 `(1,2)`
116,886 confirms, S3 67,824, S1 36,209 and S4 515,340 `historical-floor-insufficient`). Adverse steps,
with reads allowed to straddle them: witness-only rollback → `lowerWitnessGeneration` /
`witness-tail-condition`; namespace rollback → `floor-above-tail`; truncated closed generation →
`closed-tail-unavailable` and `superseded-sequence-unavailable` (not busy); row at the floor sequence
substituted → `floor-digest`; interior substitution → confirm (selected limit) or `seal-join` at `k`;
`projectPurge` TERMINAL → `closed-tail-unavailable`; GRANT or other-run row at `k` → `seal-join`;
foreign-project witness → `witnessOtherProject`.

**Frozen dispatcher, exhaustive small grid** (`probes/dispatch_grid_r3.py`): 4 shapes × 2 generations ×
`first_generation` ∈ {1,2} × 6 marker maps × 42 witness observations = **8,064 cells, 0 violations** of
ten properties (nothing later than W hidden; no OK/REVERT/ADVANCE in a quarantined generation;
eligibility needs a marker; absent witness only with `witnesslessRestore`; INIT only on a truly empty
carrier; malformed/foreign never act; predecessor closed or quarantined; empty base names
`first_generation`; malformed marker ⇒ unavailable; no exception). Two earlier versions of my
forward-gap property were wrong (they flagged the lawful successor of a quarantined or closed
generation); both are preserved with a note.

**Mutation** (`probes/mutation.py`): 42 mutants of the two kernels judged by the owner's two sweeps
called directly — no source-pin gate is in that path, so every kill is a semantic assertion.
**28 killed, 14 survived**; then each survivor re-run in my schedule harness (`probes/survivors.json`).

**108 N-1 closed**: `bytearray`, `memoryview`, `bytes` subclass and `str` are `BYTES_REQUIRED` for both
kinds; loosening the guard to `isinstance(bytes)` or to any bytes-like now fails the sweep
(`probes/n1-mutants.json`). **108 N-2 closed** as a decision: S2.1 declares codec-local labels
advisory, non-public and not a cross-language identity.

## 4. Findings

No blocking finding against the normative text. Three medium follow-ups on the *executable* owners.

### F-1 (medium) — the dispatcher cannot express S7.1's marker disposition
S7.1 makes marker presence the gate for continuation, and its table separates
"marker `uncertainTailLoss`", "marker `witnesslessRestore`" and "none; refuse without marker". The model
returns the single token `QUARANTINE` for all of them: **4,984 of 8,064 cells**, covering 64
malformed/empty-file cells and 160 foreign-project cells (no marker by the table), 78 absent-witness
cells (`witnesslessRestore`) and 4,682 same- or cross-generation cells whose disposition the token
does not determine. No case pins a disposition either. An implementer working from the model cannot
derive whether to write a marker — and the text says a wrong choice is permanent in one direction
(no-marker refusals have no continuation) and authority-relevant in the other. Related: a malformed
witness yields `already-quarantined-refuse` whenever *any* marker exists, even for a generation
quarantined and continued long ago. Return a typed disposition (`{refuse, marker: reason | none}`) and
pin the table's eight rows as cases.

### F-2 (medium) — seven behaviour-changing anchor mutants survive the selected sweeps
All seven change outcomes in my harness: second witness not validated; floor digest unchecked; SEAL
join ignores `run`; join accepts any schema-3 kind; H decided from W1 alone (one-sided confirm); H
accepts any TERMINAL cause; Case A confirms without `stableW`. Cause: 29 cases, few with W1 ≠ W2, none
with a floor-row mismatch, a `projectPurge` tail, a non-SEAL or other-run row at `k`; and the sweep
builds its "second capture" by evaluating the **same inputs** again. The schedule models that would
catch several of these are trial evidence, not part of the pinned checks, so they give no regression
protection. Of the other seven survivors, five are equivalent (unreadable short-circuits before
`_stable`; `dispatch == 'OK'` already implies COMMITTED; REVERT/ADVANCE imply PENDING; the empty-generation
state filter duplicates `reconcile_witness`; the forward-gap conjunct is implied), one is the
dispatcher's TERMINAL-cause check (same gap), one was not distinguished by my corpus.

### F-3 (medium) — `check-carrier-v3.py` still models the old act C
`carrier-migration.v1.md` now requires a witnessed act A and, for act C and the `{A,B}` resume, the
same-project witness **COMMITTED at the inherited TERMINAL sequence and digest**. `check-carrier-v3.py`
is unchanged (`_s37_publish` checks only that a surviving witness names the project), so its 406 passes
say nothing about the new precondition: publishing with a PENDING witness or one at `t−1` is accepted by
the executable model and refused by the law. Law ahead of model; update before selection.

### F-4 (low, disclose) — every new generation is `unknown-custody` until its first fenced boundary
The floor for `(project, G+1)` does not exist until a boundary at which W names G+1, so in S1–S3 the
first SEAL of generation 2 is `unknown-custody: floor-absent` in 72 of 78 evaluations and confirms only
after the end copy; in S4 the crash path happens to write the zero floor and it always confirms.
Refusing on an absent floor is the right safety choice (absence may be deletion), but the
availability-limit paragraph discusses only H. Disclose it; optionally allow the explicit zero floor of
G+1 to be written at the boundary where W is COMMITTED at TERMINAL(G) — a zero floor anchors nothing.

### Notes
- **N-1 Causal independence of the two captures is a caller obligation the kernel cannot check**:
  `decide(c, c)` diagnoses. The owner sweep itself uses that pattern. State the obligation where
  `decide` is documented and make at least one case use two genuinely different captures.
- **N-2 Preconditions.** Both kernels say "already admitted". That is sufficient only if the external
  admission supplies: carrier-format steps 1–3; *all* rows of the requested generation with
  domain-framed digests recomputed by the caller (the join trusts `row['digest']`); `quarantine_present`
  true for a malformed marker; one snapshot per capture; the presence classification. The dispatcher
  additionally does not check generation gaps (rows in 2, none in 1, `first_generation = 1`) or that
  the predecessor of a *populated* witness generation is closed. Name the owner of each.
- **N-3** A single malformed marker for any generation makes the whole carrier
  `quarantine-marker-unavailable`. Conservative and consistent with the text; list it with the
  no-continuation limits.

## 5. Not reviewed

Foundation, workflows and native trees (pins only); the owner's schedule scripts and mutant scripts
(read for orientation, not audited); SQL, file capture, locking, marker writes, migration execution —
none exists here. No Rust, no target, D3–D6 untouched. My schedules are two generations, ≤ 3 rows, one
writer, synthetic digests: bounded evidence, not a concurrency or power-loss proof.

## 6. Bounded verdict

**Reference 111: reviewed. The prospective law is coherent and I found no blocking defect in it; D2
H-1 to H-4 are resolved in the text, 108 N-1/N-2 are closed, and the owner's two explicit choices are
agreed. F-1, F-2 and F-3 should be closed before Rust integration or selection builds on the models;
F-4 is a disclosure.** Not approval of any implementation, not cumulative approval, not selection.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `*.diff`, `checks/*`,
`probes/*` (incl. preserved failed runs), `hashes.txt`.
