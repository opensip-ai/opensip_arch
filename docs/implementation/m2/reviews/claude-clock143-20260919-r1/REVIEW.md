# Independent bounded review — public clock-range mapping 143 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `clock143-20260919-REQUEST.md`. Scope: the delta of frozen `clock-detail-checkpoint-143` over frozen 141 — the
**pure mapping** part of my clock134 N-2 / clock139 N-2: `Assessment::public_range_termination(&self)` turns a typed
`TimeRange` refusal into the reference's public termination, and returns nothing for every other assessment. No
envelope emission, renderer, caller, retained invocation or effect authority; 141 N-1 (production placement, raw
kernel reach, typed OS / signed-time inputs, fail-stop) stays open by the owner's statement. No isolated-host repeat
for this private pure mapping (disclosed). No frozen/selected/product edit; scratch builds, dedicated target dirs; no
commit, push or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,062,588 bytes, SHA-256 `1d7ecd9f068a8080e04b07929cccfe7af1196450953408ee5af4d5c70a2cca98` = request and `archive-pin.json` |
| Members | 365/365 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 331/331 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 141 extraction (331/331); 329 unchanged; `trust_time.rs` and `admitted-clock-cases.ndjson` changed |
| Generator inputs | the three hashes in `detail-generation-provenance.json` (138 model, both workflow `common` schemas) equal **my** 138 extraction; `reference138/` pin copies equal the repository's |
| Host receipt | none, as disclosed; 141's host86 is historical only |

## 2. What changed (diff read in full)
One `impl Assessment` block: `Some(Refusal::TimeRange(operand))` → `(2, {class: request-rejected, errorCode:
REQUEST.PRECONDITION_FAILED, domainDetail: {code: TRUST.TIME_RANGE_UNREPRESENTABLE, subject, remedy}})` with a literal
(subject, remedy) pair per operand; anything else → `None`. `&self`, no state. The bridge test now also compares this
value with a new top-level `publicRangeRefusal` member of each of the 44 rows.

## 3. Evidence

**Owner checks, fresh scratch:** 81/81 security tests; strict workspace Clippy clean.

**Fixture and generator, checked without the owner's generator** (`fixture_probe.py`):
- all prior fields of the 44 rows are preserved exactly; every row carries the new member; 22 non-null
  (14 retained / 4 presented / 4 continuity), 22 null, each consistent with the row's own `expected.refusal`;
- for each row I ran reference 138's kernel **and its own `public_details` projector** and built the termination from
  that: **44/44 equal** the fixture;
- all 22 terminations validate as `StepTermination` in **both** workflow schema majors (which since 138 bind subject
  and literal remedy per tag);
- the three literal (subject, remedy) pairs in the Rust source equal reference 138's `CLOCK_RANGE_REMEDIES`
  byte-for-byte.

**Typed-range-only route, 30,000 cases** (my 141 corpus; `rust_probe.rs.txt`, `compare.py`): for each case the probe
mints the sealed projection, evaluates through the bridge and calls the mapping twice.
- **9,863 range refusals → the exact expected termination** for their operand (exit 2, class, error code, detail
  code, subject, remedy; exactly 3 + 3 members);
- **19,970 non-range outcomes → `None`** — proceed, payload-future, the three excursion kinds, fresh-no-context — and
  167 typed errors produce nothing;
- the two calls are equal in every case (no hidden state); exactly three distinct terminations exist, each
  schema-valid in both majors and equal to the reference's D9 row. **0 violations.**

**Mutants** (7, complementary to the owner's four; all compiled; baseline green): **7/7 killed by the owner's test.**
The one I cared about is the first: swapping the (subject, remedy) *pairs* between the retained and presented
operands — every output stays schema-valid, so a schema check alone would pass it, and the user would be told to drop
a document when the installation needs restoration (the r2 F-1 misdiagnosis). It is killed because the fixture pins
the termination **per row**. Also killed: exit 4; class `operational-failed`; the mapping firing for an ordinary
horizon refusal; silence for the continuity operand; the subject member renamed; a remedy losing "Nothing was written."

## 4. Closure

| Item | Status |
|---|---|
| clock134 **N-2** / clock139 **N-2** — typed refusal had no mapping to the public detail, subject and remedy | **Closed for the pure mapping**: exact D9 row, closed three-tag subject, literal per-tag remedy, range-only. Emission through an envelope or renderer is not part of this subject |
| clock138 N-1 (three copies of each remedy) | now **four** (model, two schemas, Rust) — see N-1 |
| clock141 N-1 | open, as stated |

## 5. Findings
No defect found.

- **N-1 (note) — the remedy text now has four copies, and the Rust one is only checked against a frozen fixture.**
  Drift between model and schemas is detected inside the reference (138). Drift between the *reference* and *Rust* is
  detected only if the 44-row fixture is regenerated when the reference changes; the generator records its input
  hashes, which is the right hook. Make "fixture provenance hashes equal the selected reference" a check that fails,
  rather than a file someone reads — otherwise a future remedy edit in the reference leaves Rust silently stale while
  all 81 tests stay green.
- **N-2 (note)** The mapping returns a bare `(u8, JsonValue)`. When an emitter exists it should consume a typed
  value (or this function should return the already-sealed termination type the envelope layer will use), for the
  same reason the record, root and envelope layers were sealed: a tuple can be built by anyone.

## 6. Bounded verdict
**143: reviewed, no finding. The mapping is range-only and exact: on 30,000 cases every typed range refusal yields the
reference's termination for its operand and every other outcome yields nothing; the 44 fixture expectations equal
what reference 138's own projector produces and validate in both schema majors; the Rust literals equal the reference
map byte-for-byte; generator inputs match my 138 extraction; 7/7 mutants are killed, including the schema-valid pair
swap. clock134 N-2 / clock139 N-2 are closed for the pure mapping.** Not approval of emission, rendering, a production
adapter, SQL custody, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust_time.rs.diff`, `owner/`,
`probes/{fixture_probe.py,rust_probe.rs.txt,compare.py,mutation.py,mutation.json,mutation.log}`,
`io/{fixture-probe.json,cases.ndjson,cases.rust,comparison.json,provenance-check.json}`, `hashes.txt`.
