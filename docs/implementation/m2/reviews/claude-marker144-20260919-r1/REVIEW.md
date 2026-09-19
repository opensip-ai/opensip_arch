# Independent bounded review — quarantine markers from a retained SQLite snapshot 144 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `marker144-20260919-REQUEST.md`. Scope: the delta of frozen `marker-snapshot-checkpoint-144` over frozen 143 —
`CurrentCarrierSnapshot::capture_marker` and the new private module `journal_store/marker_rows.rs` — against the
marker contract I reviewed as reference 125 (its codec is byte-identical in 142: `8fb8fb02…`). One component of
118 I-2: a private admitted marker owns bytes; it is **not** whole-population, history, custody, writer, lease, fence,
consumer or OS authority, and no inherited reader is claimed. No frozen/selected/product edit; scratch only, Python
`-I -B`, dedicated Cargo targets; no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,176,248 bytes, SHA-256 `61f4f684e7df0442f2f0e9ec7fa850f6fde9f2f39916dd61ee0d8c0cf281b361` = request and `archive-pin.json` |
| Members | 420/420 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 333/333 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 143 extraction; 330 unchanged; `journal_store.rs` changed; `marker_rows.rs` and `marker-row-cases.ndjson` added |
| Host provenance | **host88: 213 sources, all equal the final product pins.** host87: 212 equal, `marker_rows.rs` differs — the disclosed pre-Clippy run; I do not count it for final bytes. The pre-Clippy before-image differs from the final file in exactly one expression, `!x.is_some_and(\|n\| n >= 1)` → `x.is_none_or(\|n\| n < 1)`, which is logically identical |

## 2. What the reader does (module and delta read in full)
`capture_marker` refuses `generation < first_generation` (`Historical`) and a zero bound, then runs **one** statement on
the snapshot's existing connection: the three mirror columns, `CAST(body AS BLOB)` and the four `typeof()` values,
`LIMIT 2`. No row → `Absent`. A blob over the bound → `Unusable(Bound)` without copying; a non-blob cast →
`Unusable(Storage)`. Otherwise the octets are owned, then: storage classes must be exactly
integer/text/integer/text and `PRAGMA encoding` UTF-8; strict metadata parse; closed nine members; schema 1;
generation ≥ 1; tail in 0..2^53−1; hex project digest; tail digest null iff tail 0; the seven-condition table with
reason, null/hex and tail>0 rules; canonical re-encoding must equal the raw octets; the four mirrors (generation,
reason, tail, SHA-256 of the project key). SQL errors propagate as errors. The snapshot itself (unchanged) byte-compares
the stored DDL with the frozen definition, so `grantGeneration` really is an `INTEGER PRIMARY KEY`: the second-row
branch and non-integer generations are unreachable defensive code.

## 3. Evidence

**Owner checks, fresh scratch:** 85/85 security tests; strict workspace Clippy clean on final bytes.

**3.1 Real-SQLite differential, 3,895 rows** (`gen_rows.py`, `rust_probe.rs.txt`, `compare.py`). Every case is first
inserted into a real database built from the frozen DDL (which I checked occurs byte-for-byte in the Rust carrier
DDL), read back with `typeof()` and `CAST(body AS BLOB)`, and judged by reference 142's `decode_marker_row`; then the
same insert is made through rusqlite and read through a fresh `CurrentCarrierSnapshot`. Bodies: nine valid markers
(one per condition, generation 7, tail 2^53−1), 6,000 one/two-member mutations over a 30-value pool, and byte-level
variants (trailing LF, leading space, BOM, Python spacing, unsorted keys, `1.0`/`1e0`, duplicate key, embedded NUL +
tail, invalid and overlong UTF-8, empty, `null`, `[]`, lone-surrogate escape, truncation, two documents); rows with
differing generation / reason / tail / project, tails as NULL, text `'5'` and `'five'`, REAL 5.0 and 5.5, BLOB; bodies
stored as BLOB.
- **admission agrees in 3,895/3,895** (95 admit); 0 panics, 0 errors, **never `Absent` for a present row**;
- every admitted marker owns octets equal to the inserted bytes and a document equal to their parse; **every
  unusable row returns the exact raw octets**;
- refusal classes line up (`ROW_STORAGE`↔Storage 45, `ROW_MIRROR`↔Mirror 54, `NONCANONICAL_BYTES`↔NonCanonical 36,
  decode 258, shape 3,398) except 9 rows where a lone-surrogate *key* is `SHAPE` in the reference and `Decode` in
  Rust — class only.
(Two first attempts failed in my harness — a JSON float in my case line, then a comment I placed inside a
conditional chain — both outputs kept.)

**3.2 Snapshot, bounds, engine limit, encodings** (`rust_probe2.rs.txt` → `io/snapshot.txt`):
- a snapshot opened while the marker existed still **admits the original 398 bytes** after the writer deletes it and
  inserts garbage; a snapshot opened before sees `Absent`; a fresh one sees `Unusable(Decode)`; repeated reads are stable;
- generation 0 and negative → `Historical`; generation 2 and `i64::MAX` with no row → `Absent` (no population claim — N-1);
- bound = length admits, length − 1 → `Unusable(Bound, raw none)`, 0 → `Bound` error, `usize::MAX` admits;
- a 5 MiB body → **SQL `TooBig` error** under the snapshot's 4 MiB `SQLITE_LIMIT_LENGTH`, never absence; a 3 MB body →
  `Unusable(Bound)` without a copy;
- UTF-16le/be: no row → `Absent`; a valid marker as TEXT → `Unusable(Storage)` with the 796 UTF-16 octets; the valid
  UTF-8 octets as BLOB → `Unusable(Storage)`;
- another project key → the snapshot refuses to open (`Binding`); a reason written with
  `ignore_check_constraints` → `Unusable(Mirror)`.

**3.3 Mutants** (17, complementary to the owner's eight; all compiled; baseline green; stage 1 the 85 owner tests,
stage 2 my two probes): **13 killed by owner tests** — each `typeof` requirement, the encoding check, canonical
bytes, all four mirrors, bound off-by-one, over-bound reported as absent, unusable dropping its raw bytes, null tail
digest at a positive tail, `witness-absent` at tail 0. **4 survive the owner's tests and are detected by my corpus** —
T-1.

## 4. Findings

- **T-1 (medium) — two admission rules are masked in the 166-row fixture, so removing them passes all 85 tests.**
  (a) *A floor condition may also carry a witness hash*: with `is_null("witnessSha256")` removed from the floor arm,
  **41 of my rows flip from `Unusable(Shape)` to admitted**. The fixture's two relevant rows
  (`cross-condition-floor-*`) change only the condition of a witness-type marker, so `floorSha256` is null and *that*
  refuses them. (b) *Tail bound*: with the 2^53−1 bound widened to 2^63, **7 rows flip to admitted**; the fixture's
  `field-observedTailSeq-9007199254740992` leaves the row's `observed_tail_seq` at its old value, so the mirror
  refuses it first. Both are the pattern I reported in purge137: a negative case that violates two rules pins neither.
  Add a floor marker with a valid floor hash *and* a witness hash, and a body/row pair that agree on a tail of 2^53.
  Both rules are killed on the reference side (125), so this is a fixture-derivation gap, not a contract gap.
  (c)/(d) *class only*: generation 0 (Shape → Mirror) and a mirror failure reported as `Shape` also survive, because
  the fixture test asserts `Unusable { raw: Some(..) }` without the reason. If `UnusableReason` is going to drive a
  consumer (restoration vs. retry), assert it per row; if not, say it is diagnostic only.
- **N-1 (note, consumer obligation) — `Absent` means "no row for this number", not "this generation has no marker".**
  `capture_marker(i64::MAX)` and `capture_marker(2)` on a carrier whose only generation is 1 both return `Absent`.
  The README says so ("not generation-population authority"); the composition that consumes it must first establish
  that the generation exists in the same snapshot, or a caller can obtain a clean absence by asking about a generation
  that was never there.
- **N-2 (note)** A present marker in a UTF-16 carrier is `Unusable(Storage)` with raw octets, while absence in the same
  carrier is a lawful `Absent`. That asymmetry is what reference 125 decided and is implemented exactly; it does mean a
  UTF-16 carrier can never hold a usable marker, so whoever writes markers must refuse such carriers up-front.
- **N-3 (note)** `max_body_bytes` bounds the *copy*, not the read: SQLite has already materialised up to 4 MiB before
  the length is compared. That is bounded by the snapshot's engine limit and disclosed; callers should not read the
  parameter as a memory ceiling.

No behavioural defect found in the reader.

## 5. Unresolved limits
macOS host; bundled SQLite of this build. Same-snapshot is shown for one connection and WAL mode, which the snapshot
enforces. Nothing here establishes why a marker exists, that the generation population is complete, custody of the
file, or any writer behaviour; `AdmittedMarker` is private to `journal_store` and has no consumer yet.

## 6. Bounded verdict
**144: reviewed, no blocking finding. On 3,895 real-SQLite rows the reader admits exactly what the reviewed marker
contract admits, never reports a present row as absent, returns exact raw octets for every admitted and unusable row,
reads through the retained snapshot in both directions, turns engine-limit overflow into an error and handles both
UTF-16 encodings as specified; 13/17 of my mutants die on the owner's tests. T-1: two shape rules (witness hash on a
floor condition; tail bound) and the unusable *class* are not pinned by the fixture because other rules mask them —
two isolated rows close it. N-1 is the obligation that matters for whoever consumes `Absent`.** Not approval of
population, history, custody, writers, consumers, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `journal_store.rs.diff`, `owner/`,
`probes/{gen_rows.py,rust_probe.rs.txt,rust_probe2.rs.txt,compare.py,mutation.py,mutation.json,mutation.log}`,
`io/{rows.ndjson,rows.rust,rows.FAILED-r1-float-in-harness-line.rust,rows.FAILED-r2-my-comment-truncated-generator-line.rust,generation-stats.json,comparison.json,snapshot.txt}`, `hashes.txt`.
