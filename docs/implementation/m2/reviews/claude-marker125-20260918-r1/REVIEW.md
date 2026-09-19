# Independent bounded review — quarantine marker reference 125

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-18. Request: `REQUEST.md`.
Subject: frozen `quarantine-marker-reference-checkpoint-125`, the concrete schema/codec/factory for the
marker r2 decisions with my Q-1, Q-2, Q-3. Scoped to those bytes: missing schema/body rules are reported
separately from external integration obligations; nothing here is 118 I-2 closure, physical SQL admission,
marker insertion, writer lease or current authority. No frozen/selected/product edit; scratch copies with
bytecode writing disabled; no commit, push or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,101,776 bytes, SHA-256 `3d052ac49199b2ef7d04c2f1e277682b151424e8e2023b4d77e4c2669c08a12a` = request and `archive-pin.json` |
| Members | 1,398/1,398 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified clean afterwards |
| Candidate | 1,284/1,284 pins equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 122 extraction |
| Delta | the 12 declared: contract, `carrier-migration.v1.md`, `security-lifecycle.schemas.v1.json`, `operational_file_reference.py`, `generation_dispatch_reference.py`, `check-security-lifecycle.v1.py`, `check-carrier-v3.py`, five pin inventories. The primary model is unchanged from 122 |

**Owner checks reproduced, required order, fresh output**: envelope receipt 168 / 145 / 1,803 / 6,000
passed → integration **423 / 0** with that receipt → security **581 / 0, 22 sweeps** (codec 167 unchanged,
marker shape/row/factory 515, factory grid 2,040) → integrated carrier **435 / 0**.

## 2. What was added (read in full)
- `CarrierQuarantineMarkerV1`: closed nine-member schema.
- Codec kind `quarantine-marker` with `_marker_shape`: strict ints (schema 1, generation 1..2⁶³−1, tail
  0..2⁵³−1), lower-hex digests, tail digest null **iff** tail 0, and the condition ↔ reason ↔ hash ↔
  positive-tail binding exactly as the contract paragraph states it.
- `decode_marker_row`: requires `PRAGMA encoding` UTF-8, `typeof` = integer/text/integer/text, native `int`
  and `str` mirrors, then strict decode of the exact octets, then project + generation + reason + tail
  mirror equality (`ROW_STORAGE`, `ROW_MIRROR`).
- `quarantine_marker_body`: runs `open_disposition`, returns `None` unless QUARANTINE, derives the
  condition from the *same* admitted observations with floor conditions first, hashes only the causal
  file, takes the tail digest from the projected row's own admitted digest, and passes its own output
  through the codec.
- Contract: Q-1 (`tail-above-witness` is COMMITTED-only, in the table row too), Q-3 (own-format
  `body_sha256`, no v3 recomputation of inherited rows), non-causal observation loss disclosed;
  migration: a quarantined highest inherited generation refuses act C.

## 3. Evidence

**Factory against my own oracle** (`probes/factory_vs_oracle.py` — the oracle from my marker-r2
adjudication, extended to all nine fields; it never calls the factory to decide): **2,040 marker cells: every
body equals my oracle in all nine fields**, every one round-trips through `decode_marker_row`, every one
validates against the schema; and no body is produced for any non-QUARANTINE disposition. Condition
distribution identical to r2 (tail-0 only for committed-above-tail 120, non-adjacent-pending 80,
floor-above-tail 600).

**Real SQLite rows** (`probes/row_and_shape.py`; table created from the frozen DDL):

| Row | Result |
|---|---|
| UTF-8 database, canonical TEXT body | ADMITTED |
| **UTF-16le database**, same insert | `ROW_STORAGE` |
| body stored as BLOB; tail `'five'`; tail `5.5`; **tail NULL** | `ROW_STORAGE` ×4 |
| tail inserted as `'5'` or `5.0` | ADMITTED — SQLite's INTEGER affinity stores an integer, and `typeof` says so |
| row generation / reason / tail differing from the body; body naming another project | `ROW_MIRROR` ×4 |
| trailing newline; `json.dumps` spacing | `NONCANONICAL_BYTES` |
| `markerSchema 1.0`; embedded NUL with trailing bytes | `DECODE` |
| unknown member | `SHAPE` |

**Two statements of one shape agree**: 40,000 single- and double-member mutations of seven valid bodies
(one per condition): codec shape and JSON schema give the same verdict on **40,000 / 40,000**
(1,708 valid, 38,292 refused).

**Mutation** (owner marker sweeps called directly, plus the integrated carrier check for the migration
mutant; neither path has a pin gate): **18 mutants — 14 killed by assertion, 2 stopped by an exception
inside the sweep (reported separately, not as assertion kills), 2 survived.** Killed include: reason no
longer tied to condition; tail digest null-iff-zero dropped; a floor condition carrying a witness hash and
vice versa; upper-case hex; tail bound widened to 2⁶³; encoding unchecked; storage classes unchecked;
project or generation not mirrored; PENDING-below-tail labelled `tail-above-witness` (Q-1); hashes
swapped; tail digest from the first row; and **Q-2 — removing the inherited-quarantine refusal fails 8
carrier checks** (427/8).

## 4. Findings

**Missing schema/body rules**
- **B-1 (low, tests) — the positive-tail rules are enforced but unpinned.** "`witness-absent` admitted at
  tail 0" and "`equal-seq-different-digest` / `tail-above-witness` admitted at tail 0" both survive the
  515 checks. Codec and schema both enforce them (my 40,000-case agreement run refuses them), so this is
  a missing negative, not a missing rule: add one tail-0 body per condition.
- **B-2 (note)** — the shape cannot express that `committed-above-tail` implies a witness sequence above
  the tail, because the witness sequence is deliberately not a field; the hash is the only witness
  evidence. Consistent with "must not claim to re-prove the old cause"; nothing to change.

**External integration obligations (not defects of 125)**
- **E-1** — everything `decode_marker_row` is *told*: the `PRAGMA encoding` value, the four `typeof`
  results and `CAST(body AS BLOB)` must come from the **same snapshot** as the journal rows, read by the
  storage layer, never from a driver's text conversion. The contract says so; no code does it yet.
- **E-2** — generation binding (M-2): populated or lawfully bound empty generation, no gaps, no
  marker-only future generations, inherited history admitted by its own origin rule. The factory and
  decoder both state that the complete admitted carrier/history snapshot is a precondition.
- **E-3** — the marker *insert* itself: inside the admitted writer transaction, once per generation
  (`PRIMARY KEY`), body and three mirror columns from one factory result.
- **E-4** — Q-2's refusal is modelled in the carrier simulator with synthetic admitted projections; the
  migration executor that must perform the same check does not exist.

## 5. Closure of my marker-r2 items
| Item | Status |
|---|---|
| M-1 integer tail, null malformed | **Closed** — shape + real-SQLite NULL row refused |
| M-2 generation bound to history | Stated as precondition (E-2); not checkable inside a row decoder |
| M-3 octet-exact comparison, UTF-8 encoding | **Closed** — UTF-16 database and BLOB storage refused on a real database |
| Q-1 COMMITTED-only `tail-above-witness` | **Closed** — table row, enum note and factory agree; mutant killed |
| Q-2 quarantined inherited generation vs migration | **Closed in law and simulator** — act C refuses, 8 checks; executor pending (E-4) |
| Q-3 own-format tail digest | **Closed** — contract and factory docstring; the factory never recomputes |
| O-1 both file hashes | Declined by the owner; the loss of the non-causal observation is now **explicitly disclosed**, which is what I asked for if it was declined |

## 6. Bounded verdict
**Reference 125: reviewed, no blocking finding. The marker schema, codec kind, row decoder and causal
factory are mutually consistent and agree with my independent oracle on every marker-proposing state;
M-1, M-3, Q-1, Q-2, Q-3 are closed; B-1 is a two-case test follow-up.** E-1 to E-4 remain integration
obligations. Not 118 I-2 closure, not approval of SQL admission, marker writing, migration execution or
any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `codec.diff`, `dispatch.diff`,
`checks/*`, `probes/factory_vs_oracle.py` + `factory-vs-oracle.json`, `row_and_shape.py` +
`row-and-shape.json`, `mutation.{py,json}`, `hashes.txt`.
