# Independent bounded review — marker regressions 147 (Rust, test-only)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `marker147-20260919-REQUEST.md`. Scope: the delta of frozen `marker-regressions-checkpoint-147` over frozen
146 — a `cfg(test)` fixture consumer and `marker-row-cases.ndjson` — closing my marker144 T-1 (a–d). No new producer
or classification law; unusable reasons stay private diagnostics and every unusable marker still refuses a population.
No isolated-host repeat for a test-only change (disclosed; parent 146 host90 is not a claim about the new rows).
146 F-1 (purged predecessor) is unchanged in this tree and is not part of this subject. No frozen/selected/product
edit; scratch only, `-I -B`, dedicated targets; no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,084,684 bytes, SHA-256 `ffda96d55b995365b78f228c4a886fe58ab8e30157905389032230a61d61e971` = request and `archive-pin.json` |
| Members | 369/369 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 334/334 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 146 extraction; 332 unchanged |
| Production bytes | only `journal_store.rs` and the fixture changed; **all three diff hunks lie inside `fn sql_marker_rows_match_reviewed_reference` in the `#[cfg(test)] mod carrier_tests`**; `marker_rows.rs` and `generation_population.rs` are pin-identical to 146 |
| Fixture | 166 → 168 rows; the original 166 rows' fields are **unchanged**; every row gains `expectedReason`; 25 admit / 143 refuse |

## 2. Evidence

**Owner checks, fresh scratch:** 89/89 security tests; strict workspace Clippy clean.

**Reference class oracle, re-derived without the owner's generator** (`fixture_oracle.py`): each of the 168 rows is
inserted into a real SQLite database built from the frozen DDL, read back with `typeof()` and `CAST(body AS BLOB)`, and
judged by the reference codec (`8fb8fb02…`, byte-identical in 125/142/145). Mapping the reference error to the Rust
class gives **168/168 equal to `expectedReason`**: 25 admitted, Shape 123, Decode 7, Mirror 7, NonCanonical 3,
Storage 3.

**The two new rows isolate their rule.** `isolated-floor-with-valid-floor-and-witness-hashes`: condition
`floor-above-tail`, floor hash hex **and** witness hash hex, generation / reason / tail / project all consistent with
the physical row — the only violated rule is "a floor condition carries no witness hash".
`isolated-tail-over-cap-with-matching-physical-tail`: body tail 2^53 **and** physical tail 2^53, everything else
consistent — the only violated rule is the tail cap. This is exactly the one-violation-per-negative form T-1 asked for.

**Kill power** (`probes/mutation.py`): my four mutants that **survived the owner's tests on 144** are re-run unchanged
and are all **killed** — (a) witness hash on a floor condition (the isolated row is admitted by the mutant: `Present`),
(b) tail bound 2^63, (c) generation 0 by the shape rule, (d) mirror reported as Shape (class assertions:
`left: "Shape" / right: "Mirror"`). Four variants I added are killed as well: the **symmetric** rule (a witness
condition carrying a floor hash), a cap one too generous (2^53 admitted), Storage reported as Shape, NonCanonical
reported as Decode. **8/8.** Both mechanisms contribute: the isolated rows catch admission changes, the per-row reason
assertion catches class changes — including on the older, still-masked rows, where a masked rule now shows up as a
different class.

## 3. Closure of marker144

| Item | Status |
|---|---|
| **T-1(a)** witness hash on a floor condition masked | **Closed** — isolated row; mutant killed; symmetric rule also pinned |
| **T-1(b)** tail cap masked by the mirror | **Closed** — isolated row with matching physical tail; bound mutants killed at the exact boundary |
| **T-1(c)**, **(d)** unusable class not asserted | **Closed** — `expectedReason` asserted for all 143 refusals, equal to an independently re-derived reference class |
| N-1..N-3 | consumer/writer obligations, unchanged (N-1 is what 146 implements) |

## 4. Findings
None. One remark: the masking pattern (144 T-1, 137 T-1, 146 F-1's blind spot) keeps recurring because negatives are
written by hand. The fixture generator now records provenance; having it *assert* that each negative's first refusal
is the intended rule would stop the next instance at authoring time.

## 5. Bounded verdict
**147: reviewed, no finding. Production Rust is unchanged (all hunks inside one `cfg(test)` function; both reader
modules pin-identical); the original 166 rows are untouched; all 168 expected reasons re-derive from the reference
codec on real SQLite; the two new rows each violate exactly one rule; my four 144 survivors and four variants are
killed (8/8). marker144 T-1 (a–d) is closed.** Test-only; no isolated-host repeat. Not approval of consumers, custody,
writers, history, OS, release or any cumulative standing; 146 F-1 remains open in this tree.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `owner/`,
`probes/{fixture_oracle.py,mutation.py,mutation.json,mutation.log}`, `io/fixture-oracle.json`, `hashes.txt`.
