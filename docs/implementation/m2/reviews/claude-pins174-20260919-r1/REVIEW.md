# Independent bounded review — pure pin-inventory budget law, 174 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `pins174-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); README/PLAN and the full delta
read. Scope: the delta of frozen `pin-budget-checkpoint-174` over frozen 172 — `storage/src/pin_inventory.rs` (new, 170
production lines), its fixture `pin-budget174.json`, and the `mod` line in `storage/lib.rs`. A **pure law over a
caller-supplied complete inventory**: no SQL observation or completeness, no pin fact, lease, write, purge consent,
publication receipt or authority; Run identity admission is the caller's; an empty inventory within budget is **not** a
valid `PinnedPurgeDisclosure`. I infer none of those. No frozen/selected/product edit; scratch only, `-I -B`, dedicated
targets; no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,212,624 bytes, SHA-256 `a0b7f46686fa1066155345cfdb6c8c60b1e50e4e6085526f155e7f8e060d088c` = request = `archive-pin.json` |
| Members | 418/418 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 349/349; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 172 extraction (347/347); 346 unchanged; `lib.rs` changes by exactly `#[allow(dead_code)] mod pin_inventory;`; 2 added |
| Source law | `pin-fixture-provenance.json` names `foundation/pin_budget_reference.py` `196f5628…0dbf` — equal to the file in **my verified 173 extraction**; fixture SHA-256 `78f18a7c…1e7c` equals the pinned fixture |
| Host pins | host108 receipt: 229 sources all equal the product pins; no command failed |
| Owner checks, fresh scratch | 47/47 storage tests; strict workspace Clippy clean |

## 2. The port, clause by clause
Constants (256 scalars, 4,096 pins, 2,088,960 bytes), the four kinds, the three consequences, the fixed object
overhead, per-row overhead and comma accounting, the string-size rule (2-byte short escapes for `" \ \b \f \n \r \t`,
6 bytes for other C0 controls, otherwise UTF-8 width — DEL, U+2028 and `/` are **not** escaped), `u64` checked
addition, exact-string identity (no normalisation, no case folding), kind-aware no-op, the name rule applying to
**new** names only unless first publication, and the two independent ceilings with the legacy rule
`new > ceiling && (first || old ≤ ceiling || new ≥ old)` are the reference's, in the reference's order. Additions that
go only in the strict direction: `DifferentRun` (the reference takes one `run_id` for both sides), and `String` makes
lone surrogates unrepresentable. Rows are owned in a `BTreeMap` (byte-sorted view); fields are private with read-only
accessors; `within_budget()` carries the comment that empty ≠ disclosure.

## 3. Evidence
**3.1 Owner fixture recomputed** (`probes/fixture_check.py`): all 46 cases × 5 expectations (both measures, the
disposition, both expanded-input digests) recomputed from the frozen-173 reference plus an independent materialised
measure — **0 differences**.

**3.2 My corpus, two oracles** (`probes/gen_cases.py`, `rust_probe.rs.txt`, `compare.py`; owner's recipe format so the
product's own expander is exercised, but none of its expectations). Expected values come from the frozen reference
**and** from *materialising the actual disclosure object and measuring its canonical JSON bytes* — asserted equal to
the reference counter for every case at generation time, so the counter the product mirrors is shown to be the real
byte length, which the product never builds. 1,995 cases: 26 character classes (`/ < & '`, quote, backslash, the five
short escapes, NUL, U+001F, DEL, U+0080, 2/3/4-byte boundaries, U+2028, U+FFFD, U+FFFF, U+10FFFF, NFD) × lengths
1/255/256/257 × {new, first publication, legacy retained + another pin, kind change only}; count 4095/4096/4097/4100 →
4095…4101 × first; same-size kind change and rename over the ceiling; order-only difference; equal and empty first
publication; **disclosure bytes solved to exactly 2,088,959 / 2,088,960 / 2,088,961**; legacy over-bytes (strict
decrease / +1 / equal / first publication); the ceilings crossed (over count only with bytes rising; over both with
count falling and bytes rising, both falling, bytes falling with count equal); malformed (empty name, unknown and empty
kind, exact duplicate) and the two *non*-duplicates (NFC vs NFD, case) ; 1,500 random pairs.
**1,995 / 1,995 agree** on count, bytes, name flag, budget flag, byte-sorted rows and disposition (1,064 admit-changed,
39 admit-unchanged, 268 no-op, 579 name / 31 count / 6 byte refusals, 8 unavailable).

**3.3 Mutants** (`probes/mutation.py`, 21, all compiled, baseline green; complementary to the owner's eleven): 17 killed
by the owner's 46-case test. 4 survive it: **3 detected by my corpus (T-1)**, 1 equivalent.

## 4. Findings
- **T-1 (low) — three regressions pass all 47 tests; my corpus catches each.**
  | Surviving mutant | Why the 46 cases miss it | Isolating case |
  |---|---|---|
  | DEL (U+007F) counted as a 6-byte escape | no fixture name contains DEL | one name with U+007F |
  | `/` counted as a 2-byte escape | no fixture name contains `/` — and my own corpus r3 missed it too (disclosed; r4 adds it) | one name with `/` |
  | first publication granted the legacy strict-decrease exception | the fixture's three over-ceiling first-publication cases do not *decrease* | before 4,100 pins → after 4,097, `first = true` → must refuse |
  All three are exactly the places where a "helpful" JSON writer or a merged code path would diverge from the selected
  canonical form and law; three fixture rows close them.
- **N-1 (note, input bound of the test path)** The product JSON reader refuses inputs over 1 MiB (`ByteLimit`), so
  large inventories can only reach this law through recipes or a non-JSON path; my r2 lost its seven largest cases to
  that limit until I re-expressed them as `series` (preserved). Relevant to the owed SQL observer: a 2 MB disclosure is
  lawful here but cannot round-trip through that reader as one document.
- **N-2 (note)** `InventoryError` is finer than the reference's single `InventoryUnavailable`, and the *order* of
  checks differs (empty name → kind → duplicate → bytes, versus bytes first in Python). Every such input is
  unavailable in both; only the class name could differ, and nothing consumes it yet.
- **N-3 (note)** The legacy-within-ceiling variant of the rule (`first || new ≥ old`) is equivalent — if `old ≤
  ceiling < new` then `new ≥ old` — so that clause is documentation, not behaviour. Harmless; it mirrors the reference.
- Stated and owed, correctly: SQL pin observation and completeness, transactions, purge, disclosure construction and
  its schema (non-empty), identity admission, host, selection.

No behavioural defect found.

## 5. Bounded verdict
**174: reviewed, no blocking finding and no behavioural defect. The Rust law is a clause-for-clause port of the frozen
reference: on 1,995 independent cases — including every escape class, scalar-versus-byte-versus-UTF-16 name lengths,
the count ceiling at 4,096/4,097, disclosure bytes solved to exactly 2,088,959/2,088,960/2,088,961, independent legacy
strict decrease for count and bytes, first publication, kind-aware no-op, duplicates and unknown kinds — it equals both
the reference and the byte length of the actually materialised canonical disclosure, with 0 mismatches; all 46 owner
expectations and their expanded-input digests recompute exactly; 17 of my 21 mutants die on the owner's test. T-1:
DEL, `/` and "first publication must not inherit the legacy exception" are unpinned by the 46 cases.** Not SQL
completeness, not a disclosure, not purge consent, authority or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `owner/`,
`probes/{gen_cases.py (r4), gen_cases-FAILED-r1.py, rust_probe.rs.txt, compare.py, fixture_check.py, mutation.py, mutation_r2.py, mutation.json, mutation-r1.json, mutation.log}`,
`io/{cases.ndjson, rust.ndjson, compare.txt, compare.json, compare-r3-before-solidus.txt, fixture-check.txt, r1-seven-cases-over-the-json-reader-limit/}`,
`hashes.txt`. Harness slips, preserved: r1 byte-target solver assumed one filler row; r2 exceeded the product JSON
reader's 1 MiB limit on seven cases; r3 lacked `/`.
