# Independent bounded review — conditional anchor assessment 150 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `anchor150-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`).
Scope: the delta of frozen `anchor-assessment-checkpoint-150` over frozen 149 — `generation_anchor.rs` (new),
its 41-case fixture, `CapturedObservations`/`into_observations` in `bracketed_capture.rs`, and the two regressions for
my 148 T-1 and 149 T-1. Read-only, private, conditional. **Not** a ledger join, custody, location binding, fresh-INIT,
ABA exclusion, marker write, lease, fence, writer or commitment; `Consistent` is not confirmed commitment. No
frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit, push or delegation; no cumulative
approval.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,203,132 bytes, SHA-256 `8cac4b34a456f201b25e6e09c3e0b68ce1b470fc8d95d533c06fa574eec948e0` = request = `archive-pin.json` |
| Members | 446/446 regular, length + SHA-256 equal to `subject.json`, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 337/337 equal; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 149 extraction, 335/335; 333 unchanged, 2 changed (`journal_store.rs`, `bracketed_capture.rs`), 2 added (`generation_anchor.rs`, fixture); embedded `parent149`/`reference145` pins equal the real archives |
| Fixture provenance | the three named reference files equal my 145 extraction; **all 41 × 4 expectations recomputed from the frozen reference: 0 differences**; labels equal the reference's own 41 cases (`io/fixture-check.txt`) |
| Host pins | host95 receipt: 217 sources, all equal the product pins; 8/8 commands exit 0 |
| Owner checks, fresh scratch | 97/97 security tests; strict workspace Clippy clean |

## 2. What it is (read in full)
`evaluate` is a line-for-line port of `generation_reference.capture`; `decide` of `decide`. I compared them clause by
clause: same order of refusals, same stability rule (two failed reads are never stable), same offending-hash rule.
`assess` is the **adapter**: it takes the project digest from the admitted population (not from the query or a file),
selects the requested generation, projects its admitted rows, sets `quarantined` from the admitted marker and
`closed` from `GenerationEnd::GrantGenerationClosure` exactly. `read_inner` = capture → assess → **detach** → decide;
only `CaptureRequired` leads to one more real capture; two is the structural maximum.

## 3. Evidence

**3.1 Physical differential against the reference law** (`probes/rust_probe.rs.txt`, `probes/compare.py`). My own
builders write real SQLite carriers (11 layouts: open, closed, purged, closed+open, marked, purged-marked+successor,
closed-marked, empty, marker-only successor, three generations) and real witness/floor files (absent, malformed,
foreign project, committed/pending at tail, pending-next, above tail, wrong digest, for generations 1–4; floors absent,
malformed, zero, one, wrong digest, tail, above tail, other generation, other project); queries over generations 1–3,
sequences 1–4, with the digest, **run only** or **operation only** wrong. Each line records what *I wrote*; Python
feeds that to the frozen reference and compares standing, reason, offending hash, limitation and **number of
captures**. **58,680 production `read` calls: 0 mismatches** (13,038 one-capture, 45,642 two-capture; all 20 reachable
reasons occur, 210 `Consistent` across all four anchors).

**3.2 Between the two captures** (96 fresh carriers through `read_inner`'s hook): fixing the witness, appending a
row, inserting a marker, inserting a *broken* marker, closing and advancing to generation 2, removing the floor,
deleting the journal — **0 mismatches**. The hook runs exactly when a second capture is due (never after `Consistent`
or `Unknown`); the first evidence held equals the bytes on disk *then*, the second the bytes on disk *later*, with
their own record counts.

**3.3 No retained WAL reader (149 N-1).** In every one of the 64 retry scenarios a forced write plus
`wal_checkpoint(TRUNCATE)` *between* the captures reports busy = 0; in all 88 scenarios where the journal still exists
the same holds **while the finished assessment is still held**. Owner mutant `forget(_snapshot)` and my R5 (detach only
after the second capture) are both killed by the owner's test.

**3.4 Inside one capture** (`probes/rust_probe2.rs.txt` → `io/within.txt`, via the private phase hook): witness
changing during the SQL read → `Retry` on the witness anchor; floor changing on the witness anchor → still
`Consistent` (as the reference: only the anchoring file must be stable); floor changing on the floor anchor → `Retry`;
byte-identical replacement → stable; a change after the last witness read is not seen (README's A→B→A limit, stated).

**3.5 Privacy** (`probes/compile_boundaries.py`, clients in the parent module): **15/15 rejected inside my line** —
assessment literal with a chosen standing, replacing the standing, writing through `standing()`, swapping evidence,
owned-observations literal/edit/`Clone`, assessment `Clone`, unchecked query literal, `read_inner`, `decide`,
`evaluate`, judgment literal, reading a judgment field, parent-written forging impl. Five compile and mark the line:
see N-2.

**3.6 Mutants** (`probes/mutation.py`, 17, all compiled, baseline green; chosen where the owner's eight are not).
8 killed by the owner's tests (row digest from the wrong column, operation join, tail equality in `decide`, late
detach, and four `evaluate`/`decide` clauses). **9 survive all 97 owner tests; every one is detected by my corpus** —
F-1.

## 4. Findings

- **F-1 (medium, test gap at the claimed seam) — the sealed-population adapter is almost untested.** The request says
  the actual entry "uses exact `GenerationEnd::GrantGenerationClosure`" and assesses "admitted population + file
  observations". All 41 reference cases enter *below* the adapter (`evaluate` with a hand-built `Journal`, `closed`
  computed by the test itself), and the one physical fixture has a single open generation with one SEAL and no marker.
  Consequently these compile and pass everything:

  | Surviving mutant | My corpus |
  |---|---|
  | A1 `closed` = any TERMINAL — **the population146 F-1 defect re-introduced at this seam** (a purged generation anchors `historical-sc-trust-floor`) | 27 mismatches |
  | A2 `closed` always false | 150 |
  | A3 marker ignored (`generation-quarantined` never produced) | 294 |
  | A4 first generation assessed instead of the requested one | 1,656 |
  | A5 / A6 after-slot filled with the before observation (stability always true) | within-capture probe |
  | A8 run join short-circuited | 432 (only with the isolating right-digest/wrong-run query; my first corpus missed it too — disclosed, `io/r1-before-wrong-run/`) |
  | A10 project taken from the witness file instead of the admitted population (`witnessOtherProject` disappears) | 2,368 |
  | R6 second-capture failure reported as `UnavailableBusy` | 16 |

  Five physical cases would pin them: a closed and a **purged** historical generation under a later witness; a marked
  generation with a joining SEAL; a two-generation carrier queried for generation 2; one capture whose witness (and
  one whose floor) changes during the SQL read, asserted through `read_inner`/`assess`; a foreign-project witness on a
  real carrier; a right-digest/wrong-run query; and a failing second capture.
- **F-2 (low, semantics to decide) — a malformed marker is an error here, a standing in the reference.** The reference
  input is `quarantine_present (including malformed marker)` → `unknown-custody / generation-quarantined`. The product
  cannot reach that: a malformed marker in **any** generation fails `capture_population`, so `read` returns
  `Err(Population(MarkerUnavailable))` — also when the queried generation is a different, healthy, closed one, and also
  when it appears only before the *second* capture (then the first capture's evidence, including an offending-file hash,
  is dropped with it). Refusing is conservative and I do not ask for it to change; but the host must map this error to
  *unknown custody*, never to "busy, try again", and the README's list of results (consistency / unknown / quarantine
  condition / unavailable) should name this fifth outcome. Today nothing pins it (R6 survives).
- **N-1 (note) — `ConditionalStanding` is a plain enum.** Any code in `journal_store` can build
  `Consistent { anchor: "invented" }`, and `limitation()` answers for it. It cannot be put into an `AnchorAssessment`
  (rejected), so the rule for the next consumer is the same as for 149's observations: accept `&AnchorAssessment`,
  never a bare standing. `assess()` is also `pub(super)` though only `read_inner` needs it; it yields an opaque
  `Judgment`, so this is surface, not authority.
- **N-2 (note) — detaching is a property of `read`, not of captures.** `bracketed_capture::capture` still returns a
  transaction-holding value to any caller in the parent; 149 N-1 is closed for this consumer, not by construction.
- **N-3 (note, reference property)** `hazard` with `floorCovers = true` is unreachable in the reference and therefore
  here: `lastSeq ≥ k > t` is always caught earlier as `floor-above-tail`. 0 of 58,680 reads and 0 of 41 fixtures reach
  it; the quarantine arm for hazards is dead law, worth a line in the reference one day.
- **Carried, as the README says and I confirm unchanged:** 149 N-2 (no relation between journal, witness and floor
  locations), 149 N-3 (missing journal is a carrier error, no INIT), 149 N-4 (A→B→A), 124 F-1 (retained-ancestor
  custody). I infer no closure.

No behavioural defect found.

## 5. Closure of my earlier findings
| Finding | Status in 150 |
|---|---|
| closure148 **T-1** append stop after a `projectPurge` terminal | **Closed** — isolated owner case (purge terminal + correctly chained fourth row → `AfterTerminal`); owner mutant killed |
| bracket149 **T-1** after-read order unpinned | **Closed** — the hook now writes at `WitnessAfter` and asserts `f3`; owner mutant (my 149 survivor) killed |
| bracket149 **N-1** held capture pins the WAL | **Closed for `read`** — §3.3; see N-2 for the remaining surface |

## 6. Bounded verdict
**150: reviewed, no blocking finding and no behavioural defect. The predicate and decision equal the reviewed
reference on all 41 reference cases (recomputed by me) and on 58,680 + 96 real-SQLite/real-file production reads with
0 mismatches, including capture counts; at most two captures, the second genuinely independent; no WAL reader survives
between captures or in a held assessment; an assessment cannot be forged, edited or cloned (15/15). F-1: nine mutants
of the adapter and of `read_inner` — among them the 146 purge-as-closed defect — pass all owner tests; the claim "exact
`GrantGenerationClosure`" is currently true but unpinned. F-2: a malformed marker is a capture error rather than the
reference's unknown standing; the host mapping must be stated.** Not approval of the ledger join, location binding,
custody, INIT, ABA exclusion, writers, OS, release or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{rust_probe.rs.txt (r3), rust_probe-r1-full-corpus.rs.txt, rust_probe-r2.rs.txt, rust_probe2.rs.txt, compare.py, fixture_check.py, compile_boundaries.py, compile-boundaries.json/.log, compile-*.stderr, mutation.py, mutation.json, mutation-r1.json, mutation.log}`,
`io/{physical.ndjson.xz (+ .sha256 of the uncompressed file; `xz -dk` before `compare.py`), between.ndjson, *-compare.json, compare.txt, within.txt, fixture-check.txt, r1-before-wrong-run/}`, `hashes.txt`.
Harness slips, preserved: the first mutation run was stopped by me (stage 2 too slow on the full corpus; resumed with an
env-gated thinner corpus, `CLAUDE_150_FAST`); corpus r1 lacked the wrong-run query.
