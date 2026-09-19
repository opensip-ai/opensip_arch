# Independent adjudication r2 — carrier quarantine marker owner decisions

Reviewer: Claude (actual independent reviewer; Codex owns the choice). 2026-09-18.
Standing: **design adjudication of unselected decisions**; no schema, model or code is approved, no
implicit adoption, no cumulative approval. r1 stays unchanged. No frozen/selected/product edit, commit,
push or delegation.

## 1. Exact bytes reviewed
`quarantine-marker-owner-decisions-r2-20260918.md`, 4,189 bytes, SHA-256
`373564625cdb9d4fad00297426175c0b9d2ac62ed04db5677dcdab58e50e1ba7` (copy in `claude-out/`). Owners as
pinned in r1 (`claude-quarantine-marker-20260918-r1/claude-out/owners-read.txt`, frozen 120), plus the
frozen-120 `generation_dispatch_reference.py` used executably below and `carrier-migration.v1.md`.

## 2. Verdict
**M-1, M-2 and M-3 are closed as decisions, and the forensic fields with their condition binding are
coherent: total and unambiguous on every marker-proposing state I could enumerate.** Concrete authoring
can proceed. Three cases are not yet handled (Q-1 to Q-3) — two of them are exactly the
"inherited-generation" kind you asked about — and one simplification is offered (O-1).

| r1 | r2 | Assessment |
|---|---|---|
| **M-1** nullable tail | required integer `0..CAP`; column stays nullable for the frozen DDL; null is malformed under the profile | **Closed.** |
| **M-2** generation bound to history | populated, or lawfully bound empty base / immediate-next, from one journal+marker snapshot; gaps and marker-only future generations refuse; `first_generation` is the first **v3** generation and inherited history is admitted by its own origin/closure rules | **Closed**, and the inherited-origin distinction is a correction to my r1 wording ("below the first retained generation" was too loose). |
| **M-3** octet-exact comparison | UTF-8 database encoding; `CAST(body AS BLOB)` after a separate TEXT storage-class check; no driver transcoding; scoped to this marker boundary only | **Closed.** |
| §4 evidence lost | nine closed body fields; `condition` enum of seven; tail digest null iff tail 0; exactly one causal file hash; the body factory consumes admitted observations, not caller-supplied fields; historical admission checks shape/consistency/mirrors and "must not claim to re-prove the old cause" | **Adopted coherently.** That last sentence is the right limit. |

## 3. Totality and the equal-sequence / zero-tail cases — checked executably
`claude-out/condition_totality.py` drives the frozen-120 `open_disposition` with real canonical witness and
floor bytes (9 shape pairs × 2 `first_generation` × 37 witness observations incl. wrong-digest witnesses ×
7 floor observations), and for every result that proposes a marker derives the r2 `condition` from the
observations by r2's own rules. **2,040 marker cells: exactly one condition applies in every cell, the
reason matches in every cell, 0 problems.**

| Condition | tail 0 | tail > 0 |
|---|---|---|
| committed-above-tail | 120 | 136 |
| non-adjacent-pending | 80 | 184 |
| floor-above-tail | 600 | 288 |
| tail-above-witness | — | 224 |
| equal-seq-different-digest | — | 104 |
| floor-digest-mismatch | — | 192 |
| witness-absent (`witnesslessRestore`) | — | 112 |

So the cases you asked about are handled: **zero tail** occurs only for the three conditions where it
can (lawfully bound empty generation with a positive COMMITTED or non-adjacent PENDING witness, or a
positive floor), and there `observedTailSha256 = null` is forced, never chosen; **equal sequence** needs
tail > 0 by the witness shape (seq 0 carries a null digest and PENDING 0 is malformed), and a COMMITTED
witness above the tail with a wrong digest is `committed-above-tail` only, because equality of sequence
is the discriminator; `witness-absent` always has tail > 0, as r2 requires, because the dispatcher
proposes that marker only over a populated highest generation.

## 4. Not yet handled

- **Q-1 — align the S7.1 table with r2's precedence for a PENDING witness below the tail.** S7.1's row
  reads "Same-generation tail above witness sequence, **either state**", and its next row is
  "non-adjacent PENDING". A PENDING witness with `seq < tail` satisfies both. r2 resolves it
  (`tail-above-witness` is COMMITTED-only; any PENDING that is neither `tail` nor `tail+1` is
  `non-adjacent-pending`), and that matches `reconcile_witness`. But once `condition` is a stored,
  closed, consistency-checked field, the table and the enum must say the same thing, or a future
  admission check will find a lawfully written marker "inconsistent". Edit the table row to "COMMITTED".
- **Q-2 — a quarantined *inherited* generation cannot migrate under the current law, and nothing says
  so.** Migration act A appends `TERMINAL` to the inherited tail, but a marked generation is
  `failClosedNoAppend`; act C (118/120) requires the witness COMMITTED at the inherited TERMINAL, which
  therefore can never exist. M-2's "predecessor closure **or already-admitted marker**" would bind the
  first v3 generation through the marker, but the migration protocol has no such route. Either state
  that a carrier whose highest inherited generation is quarantined is not migratable in this profile
  (continuation first happens in the inherited format, or not at all), or define the act-A/act-C variant
  that binds `first_generation` through the marker. It is a small decision, but it is the one place
  where marker admission and migration law meet.
- **Q-3 — which digest is `observedTailSha256` for an inherited generation?** r2 says "domain digest of
  the admitted tail row". For carrierFormat 1/2 rows the read-only owner already says historical
  generations are "chain-unverifiable where the prospective encoding does not recompute". Say that the
  field is the tail row's **admitted `body_sha256` under that generation's own format rule**, not a v3
  domain recomputation, so that a marker on an inherited generation is writable and checkable.
- (minor) State that `witnessSha256` / `floorSha256` use the same function as the read-only
  `offendingSha256` — plain SHA-256 of the exact file octets — so a reader's earlier diagnosis and the
  writer's marker can be correlated.

## 5. Option, not a requirement

- **O-1 — record both file hashes whenever the file was present, and let `condition` alone name the
  cause.** r2 nulls the non-causal hash. When the floor quarantines, the witness was necessarily present
  and valid (floor selection requires it), and it is about to be overwritten by continuation; when the
  witness quarantines, a floor may well exist. Keeping both costs 64 bytes, loses no checkability — the
  rules become "`witnessSha256` null iff `witness-absent`; `floorSha256` non-null for the two floor
  conditions, otherwise null iff the floor was absent" — and preserves the second observation in exactly
  the situation (rollback with an append in flight) where both files are evidence. If you prefer r2's
  stricter one-hash rule for its simpler consistency check, that is defensible; just note that the
  non-causal file's state is then unrecoverable.

## 6. Agreed without comment
Kind name `quarantine-marker`; file-backed versus SQL-row-backed documented; all 167 parent codec checks
retained with byte/result comparison against the parent; no filesystem-presence contract for a row;
floor checks suppress a witness marker when floor admission refuses (this is 120's chosen precedence);
final writer/reader integration still owns complete snapshot admission and authority.

## 7. Bounded verdict
**Marker r2: M-1 to M-3 closed; forensic fields and condition binding coherent and executably total
(2,040 / 2,040). Carry Q-1 (table wording), Q-2 (quarantined inherited generation vs migration) and Q-3
(tail digest for inherited rows) into the concrete schema/model, which needs its own review.** Approves
no schema, model or code.
