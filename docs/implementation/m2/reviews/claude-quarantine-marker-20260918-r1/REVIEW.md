# Independent adjudication — prospective `carrier_quarantine` marker body admission

Reviewer: Claude (actual independent reviewer; Codex owns the choice). 2026-09-18.
Standing: **design adjudication of an unselected owner proposal.** No code, schema or integration is
approved. No frozen/selected/product edit, commit, push or delegation.

## 1. Exact bytes reviewed
`quarantine-marker-owner-proposal-20260918.md`, 3,984 bytes, SHA-256
`a91e30eaed052a65ca6b211041cef9615c7739478166185efc6e0e969e9b0f3c` (copy in `claude-out/`).
Owners read from my verified scratch copy of frozen **120** and hashed in `claude-out/owners-read.txt`:
`security-completion.v1.md`, `grant-journal.carrier.v3.sql`, `carrier-dispatch.v3.json`,
`carrier-format.v3.md`, `security_unit_lib_v8.py`, `security-and-lifecycle.md`,
`operational_file_reference.py`.

## 2. Q1 — did you miss an existing owner? **No.**
I searched the whole 1,284-file candidate for `carrier_quarantine`, `carrierQuarantine` and
`quarantineRecord`. Ten files mention the table; **none defines the body, and no executable ever inserts
a row**:
- `security-completion.v1.md` l.513 names it `carrierQuarantineRecord: external, non-appending` and gives
  only the four columns; l.543 gives the two reasons and "`failClosedNoAppend` and continuation only on a
  new generation";
- `security_unit_lib_v2.py` / `_v8.py` carry the DDL text only; `security-schemas.v2/` has no schema for it
  (it has one for every other record family);
- `carrier-format.v3.md` and `carrier-dispatch.v3.json` require the stored DDL to byte-equal the frozen
  definition and say a refusal "writes no quarantine marker"; `check-carrier-v3.py` checks the DDL string;
- S7.1 (111/118/120) and the read-only owner speak of "admitted" and "malformed" markers without saying
  what admission is.
You are right that `lifecycle-carrier.contract.v2.json` is a different table. So this is a genuine gap,
and S7.1 is the right owner, because S7.1 is what made marker *contents* load-bearing (they gate
continuation).

## 3. Q2 — is the minimal profile coherent? **Yes, with three changes.**

Agreed as proposed: canonical metadata JSON with exact `raw == C(value)`; closed fields; body ↔ row
mirror equality; project bound to the admitted carrier; **storage-class checks independent of declared
affinity** (needed: `body TEXT` can hold a BLOB and `observed_tail_seq INTEGER` can hold text or real;
only the `INTEGER PRIMARY KEY` is type-rigid); one complete generation map from the same snapshot as the
journal rows; unknown `markerSchema` or anything malformed ⇒ continuation unavailable, no repair, no
second marker, no guessed reason; read-only still reports presence; opaque experimental bodies are
explicitly unsupported rather than upgraded.

- **M-1 — drop the nullable `observedTailSeq` from markerSchema 1.** Every condition that writes a marker
  has an admitted tail: all five `uncertainTailLoss` rows and `witnesslessRestore` ("definite absence
  with a **non-empty admitted journal**"), and the lawfully bound empty generation has tail **0**, not
  "unknown". The proposal itself says the automatic writer always has the count. Then null describes no
  lawful writer, only a state a reader must reason about ("never substitutes for zero, never supplies a
  floor"). Keep the column nullable because the DDL is frozen, but make the *profile* require an integer
  `0..CAP`, and treat a null row under markerSchema 1 as malformed. Smaller state space, and the one
  forensic fact the marker carries is never missing.
- **M-2 — bind the marker generation to the carrier's history.** "Positive i64" is not enough: my 111
  grid showed the dispatcher accepting a marker for a generation with no rows over an empty journal.
  Admission should require the generation to be populated, or to be the *lawfully bound* empty next
  generation (120's wording), and refuse a marker beyond that or below the first retained generation.
  This belongs with the "complete unique generation map" rule.
- **M-3 — evaluate canonical equality on the stored bytes, not on SQLite's text.** State that the body is
  compared as the exact octets (`CAST(body AS BLOB)` or equivalent) and that the database text encoding
  must be UTF-8; otherwise `raw == C(value)` is checked against a transcoding.

## 4. Q3 — evidence this would lose
The marker is the **only record that survives continuation**: the first append of the next generation
overwrites the witness, and the floor of a quarantined generation is never raised again. With
`reason + observedTailSeq` alone, the five conditions that share `uncertainTailLoss` are indistinguishable
afterwards, and for "equal sequence, different digest" the sequence evidences nothing at all. I agree
with excluding raw witness bytes, timestamps and signatures. I recommend three bounded, closed,
non-authoritative additions, all in the spirit the read-only owner already adopted ("SHA-256 of the exact
stable offending bytes plus a bounded reason, never raw contents"):
1. `condition` — a closed enum naming the S7.1 table row (committed-above-tail, equal-seq-different-digest,
   tail-above-witness, non-adjacent-pending, floor-above-tail, floor-digest-mismatch, witness-absent);
2. `observedTailSha256` — the digest of the tail row the writer saw (null iff tail 0);
3. `witnessSha256` / `floorSha256` — of the exact offending file bytes, each nullable when that file was
   not the cause or was absent.
None is a grant, a repair instruction or an input to dispatch; dispatch keeps using `reason` only. If you
prefer to stay at the stated minimum, say explicitly that the cause of a quarantine is *not* recoverable
after continuation — that is then a disclosed limit, not an oversight.

No compatibility route is lost: nothing has ever written this table, and "no deployed product marker
persistence exists" matches what I found.

## 5. Q4 — reuse the exact-metadata codec? **Yes, as you prefer, with two cautions.**
Share the strict decode and `raw == C(value)` core; add a marker-specific closed shape; keep the row
mirror and storage-class checks in storage. Cautions: (a) adding a third kind edits the reviewed 108
codec — its kind set is closed and tested ("journal", `None`, list refused; 167 checks), so the successor
needs new cases for the marker kind **and** a proof that witness and floor behaviour are byte-for-byte
unchanged; (b) the module speaks of operational *files* and distinguishes Present / Absent / Unreadable
at a filesystem boundary. A marker is a row: its presence comes from the SQL snapshot, and "unreadable"
is a SQLite error. Name the kind so that nobody wires the file-presence contract to it — e.g. an
"operational record" vocabulary with `witness` and `floor` as file-backed kinds and `quarantine-marker`
as row-backed.

## 6. Bounded verdict
**No existing owner was missed. The proposal is coherent and appropriately small; before authoring, make
M-1 (no nullable tail in schema 1), M-2 (generation bound to history) and M-3 (octet-exact comparison),
and decide §4 either by adding the three bounded evidence fields or by disclosing that a quarantine's
cause is unrecoverable after continuation.** Design choice only; approves no schema, code or integration.
