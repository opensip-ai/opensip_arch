# Independent bounded review — complete fresh-carrier generation population 146 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `population146-20260919-REQUEST.md`. Scope: the delta of frozen `generation-population-checkpoint-146` over
frozen 144 — `capture_population` and the new private module `journal_store/generation_population.rs`: the
fresh-population part of 118 I-2 and the consumer side of my marker144 N-1. A private admitted population is **not**
filesystem custody, a lease, a fence or writer authority; inherited history, historical floors, association joins and
bracketed reads remain separate. The 144 T-1 fixture gap is inherited and corrected in 147, not here. During this
review the owner reported a defect in 146 (terminal cause); I assess it independently in §4 and do not treat the
planned 148 fix as reviewed. No frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit,
push or delegation; no cumulative approval.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,196,464 bytes, SHA-256 `83025ebfe2dbf736fbc70f411634e2165c0f4d637cf7e6010b44ab702a96903c` = request and `archive-pin.json` |
| Members | 420/420 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 334/334 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 144 extraction; 332 unchanged; `journal_store.rs` changed, `generation_population.rs` added; no fixture change |
| Host provenance | **host90: 214 sources, all equal the final pins.** host89 differs in both changed files — the disclosed run before the owned project digest was added; not counted for final bytes |

## 2. What the reader does (module read in full)
One `UNION` over `grant_journal_v3` and `carrier_quarantine` enumerates `(generation, typeof)` in order, `LIMIT
max+1`, on the snapshot's existing read transaction. For each: bound on distinct generations; `typeof` must be
`integer`; the number must be 1 for the first and previous + 1 afterwards (`Gap`); the previous generation must be
closed or marked (`PredecessorOpen`); the prefix is read by the existing reader with the **remaining** record and byte
budgets; the marker is read by the 144 reader with the remaining byte budget — absent is lawful, admitted is charged,
**unusable refuses the whole capture** and carries the observation (with its raw octets) in the error. Any SQL, prefix
or bound error refuses everything. The result owns the project digest, the generations, and the totals.

## 3. Evidence

**Owner checks, fresh scratch:** 89/89 security tests; strict workspace Clippy clean (final bytes).

**3.1 Exhaustive small world, 2,407 real-SQL scenarios** (`gen_scenarios.py`, `rust_probe.rs.txt`, `compare.py`). Every
subset of generations {1,2,3,4} with each generation one of six kinds — open, closed, marker-only, marked-open,
closed-and-marked, malformed marker — i.e. 7⁴ = 2,401, plus six with generations 0, 5 and 9. Each is built in a fresh
database with the owner's row helpers, read through a fresh snapshot, and compared with an oracle I wrote from the
README law (origin 1, no gaps, predecessor closed-or-marked, malformed marker refuses, last generation may be open):
- **2,407/2,407 outcomes equal the oracle** (428 admitted, 706 gap, 558 open predecessor, 715 marker); 0 panics;
- for all 428 admitted populations: generation count, record count and marker count equal the scenario; numbering is
  1..n; **re-reading with exactly the consumed (generations, records, bytes) budget succeeds, and with any one of the
  three reduced by one it is refused**. Budgets are total, exact and independent.
(One scenario of my first list needed journal rows for generation 0, which the row helper cannot build — my harness
error; first output kept.)

**3.2 Edges on real SQL** (`rust_probe2.rs.txt` → `io/edges.txt`):
- *one snapshot*: a snapshot opened before generation 2 **and a malformed marker** were written still admits
  generation 1; a fresh snapshot refuses the **whole** capture (`MarkerUnavailable{generation: 2, raw: …}`), generation
  1 included; the owned population survives the snapshot and the database file being removed, digest intact;
- *144 N-1*: `capture_marker(99)` still answers `Absent` on a one-generation carrier while the population says `[1]`
  — the population, not the point query, is the membership authority, as the request says;
- *physical types* (rows written with `ignore_check_constraints`): TEXT `'x'`, REAL `1.5`, BLOB → `PhysicalGeneration`;
  TEXT `'2'` and REAL `2.0` are converted to integer 2 by column affinity and then refused by the prefix reader
  (`RowBinding`, the body says generation 1); NULL, 0 and −1 cannot be inserted at all (NOT NULL / the carrier's own
  trigger); integer 3 after 1 → `Gap{2,3}`;
- a capacity-pause row for a non-existent generation 7 is ignored (separate protocol input, as stated);
- *later corruption*: a wrong body digest in generation 3 refuses the population although `capture(1)` alone still
  reads — the reader does not ignore generations the caller did not ask about.

**3.3 Privacy** (`compile_boundaries.py`, clients in the parent module): **8/8 rejected inside my line** — population
literal, generation literal around a genuine prefix, dropping a generation, taking a marker through `generations()`,
parent-written inherent impl building a population from genuine generations, `Clone`, `Default`, admitted-marker
literal. Two compile and mark the boundary: `GenerationPrefix` is still a plain parent type (it cannot become a
population), and the single-generation marker query remains callable. (My "baseline" entry is marked unexpected
because I appended a bare attribute with no item — harness slip; the two compiling clients show the tree builds.)

**3.4 Mutants** (11, complementary to the owner's four; all compiled; baseline green): **11/11 killed by the owner's
tests** — origin not required, generation bound off by one, marker bytes uncharged, journal bytes uncharged, records
uncharged, `typeof` check removed, journal-only and marker-only enumeration, marker alone not closing, terminal alone
not closing, zeroed project digest.

## 4. Findings

- **F-1 (medium–high; owner-reported during this review, independently confirmed) — a purged generation counts as a
  closed predecessor.** `closed_or_marked` tests `records.last().terminal`; `terminal_body` admits both
  `grantGenerationClosure` and `projectPurge`; the reviewed reference's predecessor law is
  `_closed(rows) = last row is TERMINAL, schema 1, cause grantGenerationClosure` (`generation_dispatch_reference.py`
  l.16–18, unchanged since 125). On real SQL (`edges.txt`, rows built by rewriting the terminal cause and recomputing
  its body digest): generation 1 ending in `projectPurge` followed by an **open generation 2 is `ADMITTED gens=[1,2]`**
  (P2), and followed by a marker-only generation 2 likewise (P3); the control with `grantGenerationClosure` is
  identical (P4). My own oracle did not catch it, because it and all 2,407 scenarios use the owner's row helper, whose
  terminal is always a closure — the same blind spot as the owner's 18 cases: **no test anywhere has a purged
  generation.** Impact: the population presents "project purged, then a new generation" as lawful history to whatever
  consumes it. The fix the owner describes (closure cause for the predecessor rule, general terminal semantics kept
  for append-stop) is the right shape; two things to settle when writing it:
  (i) what a purged **final** generation means for the consumer — P1 is admitted today, which is right for a reader,
  but the population does not expose the cause, so a consumer cannot tell "closed" from "purged";
  (ii) whether *purged + marked* may have a successor. The reference says yes (`… or predecessor in markers`); that is
  worth an explicit owner sentence, since a marker on a purged generation is an odd state.
- **T-1 (medium) — terminal cause is absent from every population test.** Whatever the fix, the regression set needs
  purged-predecessor rows for open, marker-only and marked successors, in isolation (each row violating only this
  rule), and a purged final generation.
- **N-1 (note)** `Generation` exposes `prefix()` and `marker()` but not whether the generation is closed, purged, open
  or marked; the consumer will recompute that from the prefix. Exposing one typed disposition from the owner module
  would keep the closure law in one place — which is exactly where F-1 came from.
- **N-2 (note)** `PopulationError::MarkerUnavailable` owns the unusable observation including raw octets, which is
  right for restoration diagnostics; remember it when errors are logged or rendered — those octets are arbitrary
  database content.

## 5. Unresolved limits
Fresh carriers only (`open` refuses migration and inherited tables; the origin guard is exercised by the owner's test
through direct field mutation). macOS host, bundled SQLite. Budgets bound what is *returned*; SQLite's own sorting for
the `UNION … ORDER BY` is not bounded by them, as disclosed. Nothing here is custody, exclusion, a lease or a writer.

## 6. Bounded verdict
**146: reviewed; one confirmed defect (F-1), otherwise as specified. On 2,407 exhaustive real-SQL scenarios the reader
equals an independent oracle of the stated law, with exact, total and independent budgets; it reads one snapshot,
refuses the whole capture on a malformed marker, a non-integer generation, a gap, an open predecessor or later
corruption; the owned population survives its source; privacy holds (8/8); 11/11 mutants die on the owner's tests.
But a generation ended by `projectPurge` is accepted as a closed predecessor, contrary to the reviewed reference law —
reproduced on real SQL — and no test contains a purged generation. 146 should not be consumed as population authority
until that is corrected and pinned.** Not approval of custody, leases, fences, writers, inherited history, OS, release
or any cumulative standing; the planned 148 fix is not reviewed here.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `journal_store.rs.diff`, `owner/`,
`probes/{gen_scenarios.py,rust_probe.rs.txt,rust_probe2.rs.txt,compare.py,compile_boundaries.py,compile-boundaries.json,compile-boundaries.log,compile-*.stderr,mutation.py,mutation.json,mutation.log}`,
`io/{scenarios.ndjson,scenarios.rust,scenarios.FAILED-r1-gen0-journal-rows-not-buildable.rust,comparison.json,edges.txt}`, `hashes.txt`.
