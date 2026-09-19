# Independent bounded review — generation closure 148 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `closure148-20260919-REQUEST.md`. Scope: the delta of frozen `generation-closure-checkpoint-148` over frozen
147 — `journal_store.rs` and `journal_store/generation_population.rs` — closing my population146 F-1 (a purged
generation counted as a closed predecessor), T-1 (no terminal-cause regressions) and N-1 (no typed disposition).
Historical/floor/association work, custody (124 F-1), leases, fences, writers, consumers and OS selection remain. No
frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit, push or delegation; no cumulative
approval.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,183,576 bytes, SHA-256 `6055400b0efacf4b7357d3f6a41139ef0c0cd0f6d1d42fc8ba7297622538784b` = request and `archive-pin.json` |
| Members | 415/415 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 334/334 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 147 extraction; 332 unchanged; exactly the two stated files changed; no fixture change |
| Host provenance | **host92: 214 sources, all equal the final pins.** host91 differs in both changed files — the disclosed run before the typed getter and expanded tests; not counted |

## 2. What changed (both diffs read in full)
`CheckedRecord` gains `closes_generation`, computed where the record has already passed body admission, row binding,
body digest and chain checks: `terminal && cause == "grantGenerationClosure"`. `closed = terminal` is untouched, so
**both** causes still stop appends. `Generation::end()` returns a `Copy` enum `Open | GrantGenerationClosure |
ProjectPurge` from the last record; `marker()` stays an independent fact. The predecessor rule becomes
`marker.is_some() || end() == GrantGenerationClosure`. Five literal cases added (purged final; purged before open,
marker-only, marked-open; marked-purged predecessor) and `end()` asserted for every admitted generation.

## 3. Evidence

**Owner checks, fresh scratch:** 89/89 security tests; strict workspace Clippy clean.

**3.1 My 146 P1–P4 re-run unchanged** (`io/edges.txt`, diffed against the 146 output): exactly two lines change —
P2 (purged, then open generation 2) and P3 (purged, then marker-only generation 2) go from `ADMITTED gens=[1,2]` to
**`REFUSED PredecessorOpen(1)`**; P1 (purged final) stays admitted; P4 (closure control) stays admitted; every other
edge — one-snapshot isolation, whole-capture refusal, ownership after the database is gone, physical types,
capacity pause, later corruption — is byte-identical to 146. No other law moved.

**3.2 Exhaustive small world with the missing dimension, 6,561 real-SQL scenarios.** My 146 corpus could not see F-1
because every terminal came from one helper. This one adds `purged` and `marked-purged` as kinds (8 kinds, 9⁴
scenarios) and builds purges with **my own** byte-level rewrite of the terminal body rather than the owner's new test
helper. Against an oracle of the reviewed reference law (successor admissible iff the predecessor has an admitted
marker or ends in `grantGenerationClosure`):
- **6,561/6,561 outcomes equal** (1,093 admitted / 2,416 open predecessor / 1,568 gap / 1,484 marker); 0 panics;
- in all 1,093 admitted populations the **typed end of every generation equals the oracle** (`Open`,
  `GrantGenerationClosure`, `ProjectPurge` — a marker never changes it), counts agree, exact budgets admit and each
  one-under refuses;
- an **unmarked purged predecessor is refused with every one of the eight successor kinds** (8 × 133 rows, all
  `open`); a marked purged predecessor behaves like any marked predecessor (91 admitted per closed/marked successor
  kind), as the referenced law says.

**3.3 Cause derivation and append-stop** (`rust_probe3.rs.txt`): a correctly chained fourth record after a TERMINAL
at seq 3 is `REFUSED AfterTerminal` for **both** causes; an ordinary record body with an added `cause` member does not
parse as a journal record, so closure can only ever be derived from an admitted TERMINAL.

**3.4 Mutants** (8, complementary to the owner's two; all compiled; baseline green): **6 killed by owner tests** — the
146 defect re-introduced; the inverted cause; `end()` reporting a marker as closure; `end()` reporting purge as open;
predecessor rule admitting purge; predecessor rule *refusing* a marked purge (stricter than the referenced law — so
that choice is pinned in both directions). **2 survive owner tests and my 6,561 scenarios:**
- *closure derived from the cause without requiring TERMINAL* — **equivalent**: no non-terminal body can carry `cause` (3.3);
- *append-stop lost for `projectPurge`* — **not equivalent**: T-1.

## 4. Closure of population146

| Item | Status |
|---|---|
| **F-1** purged generation accepted as a closed predecessor | **Closed** — reproduced fixed on my unchanged 146 probe; 1,064 purged-predecessor scenarios refuse; re-introducing the defect is killed |
| **T-1** no terminal-cause regressions | **Closed for the predecessor law** — all three successor kinds plus purged final, and the marked-purged allowance, are literal owner cases; see T-1 below for the one remaining cause-dependent behaviour |
| **N-1** no typed disposition | **Closed** — `GenerationEnd`, `Copy`, read-only, asserted per admitted generation; the closure law now lives in one place |
| 146 N-2 (raw octets inside errors) | unchanged, note stands |

## 5. Findings
- **T-1 (low–medium) — "both TERMINAL causes stop appends" is true and unpinned for `projectPurge`.** The request states
  it and the code keeps it (`closed = terminal`), but replacing that line with "only a closure stops appends" passes
  all 89 tests and all my scenarios; on my direct counterexample the mutant **admits four records, one of them after a
  purge terminal**, while 148 refuses `AfterTerminal`. Every existing after-terminal test uses a closure. With 148
  the two causes now deliberately differ in one respect, which is exactly when the respect in which they must *not*
  differ needs its own row. One prefix case (purge terminal + chained record → `AfterTerminal`) closes it.
- **N-1 (note, owner decision recorded)** *Purged + marked may have a successor* is now an explicit, tested choice
  taken from the reference dispatch law, and the README says it is not reinitialisation or writer authority. I agree it
  is what the reference says. It remains the oddest state in the population — a project purged, quarantined, and
  continued — and deserves a sentence in the contract paragraph itself, not only in the reference's code and this
  candidate's README, so that a future reader does not "fix" it in either direction.

No behavioural defect found.

## 6. Bounded verdict
**148: reviewed, no blocking finding. population146 F-1 is closed: closure is derived only from an already admitted
TERMINAL whose cause is `grantGenerationClosure`; my unchanged 146 probe changes in exactly the two defective lines;
6,561 exhaustive real-SQL scenarios — built with an independent purge writer and including the dimension my 146 corpus
lacked — equal the reference law, including the typed end of every admitted generation and exact budgets; 6/8 mutants
die on the owner's tests, one survivor is equivalent, and the other (T-1) shows that append-stop after a purge terminal,
though correct, is not yet pinned.** Not approval of history, floors, association, custody, leases, fences, writers,
consumers, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `generation_population.rs.diff`,
`journal_store.rs.diff`, `owner/`,
`probes/{gen_scenarios.py,rust_probe.rs.txt,rust_probe2.rs.txt,rust_probe3.rs.txt,compare.py,mutation.py,mutation.json,mutation.log}`,
`io/{scenarios.ndjson,scenarios.rust,comparison.json,edges.txt,append-stop.txt}`, `io-appendstop-mutant/append-stop.txt`, `hashes.txt`.
