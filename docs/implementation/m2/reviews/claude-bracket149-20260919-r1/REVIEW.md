# Independent bounded review — bracketed raw capture 149 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `bracket149-20260919-REQUEST.md`. Scope: the delta of frozen `bracket-capture-checkpoint-149` over frozen 148
— one module declaration and the new private `journal_store/bracketed_capture.rs`: **physical read ordering and
ownership only** — witness-before, floor-before → fresh `CurrentCarrierSnapshot` and whole population → witness-after,
floor-after. No decoder, anchor decision, ledger join, retained-ancestor custody, exclusion, lease, fence, grant,
writer or commitment is claimed, and I infer none; path, key, leaves and budgets are caller context, not authority.
No frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit, push or delegation; no
cumulative approval.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,180,904 bytes, SHA-256 `a2340f072cb6225395cd94a770ef9e76cfe92db99d5ac80f3eb83ac5943e5e06` = request and `archive-pin.json` |
| Members | 389/389 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 335/335 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 148 extraction; 333 unchanged; `journal_store.rs` changes by exactly `mod bracketed_capture;`; one file added; generation and marker predicates untouched |
| Host pins | host93 receipt: 215 sources, all equal the product pins |

## 2. What it does (module read in full)
`capture(spec)` calls the private `capture_inner(spec, |_| {})`. The inner function performs five real operations in
order, calling the hook after each: `capture_operational_bytes` for witness then floor; `CurrentCarrierSnapshot::open`
(which begins the read transaction and reads inside `open`, so the SQL snapshot is fixed *between* the before and after
file reads) and `capture_population`; then witness and floor again. Any carrier or population error returns `Err` and
the two before-observations are dropped — no partial capture. File observations are never errors: `Absent`,
`Present(bytes)` and `Unreadable(reason)` are owned as observed. `BracketedCapture` has private fields, read-only
accessors, no `Clone`, and **retains the snapshot** (its read transaction stays open).

## 3. Evidence

**Owner checks, fresh scratch:** 93/93 security tests; strict workspace Clippy clean.

**3.1 Sequencing with a distinct write at every phase** (`rust_probe.rs.txt` → `io/bracket.txt`; my probe sits in the
child test module because the hook is unreachable anywhere else — see 3.3). Both files are rewritten and the journal
extended in *every* hook call:
- observations: `Wb = w@start`, `Fb = f@after-WitnessBefore`, `Wa = w@after-Population`, `Fa = f@after-WitnessAfter` —
  each read sees exactly the writes that preceded it and none that followed;
- population: 2 records — the rows appended after the two before-reads are inside the snapshot, the row **and the
  marker** written after the population read are not;
- after `capture` returns, the **retained** snapshot still reads the old state (2 records, marker absent).

**3.2 File states and failures.**
- witness a directory, floor a dangling symlink → four `Unreadable(Io …)`, capture still succeeds; witness deleted and
  floor filled between the SQL read and the after-reads → `Wb=Present, Fb=Present(""), Wa=Absent, Fa=Present("grew")`:
  absence, present-empty and unreadable stay distinct and owned on each side independently;
- file bound = size → `Present`; size − 1 → `Unreadable(Bound)`; bound 0 → `Unreadable(Context)`;
- journal path missing, wrong project key, malformed marker, generation budget 0, body budget 10 → `Err` (`Carrier` /
  `Population`) in every case, **never a capture**, and the hook sequence stops at `[WitnessBefore, FloorBefore]`;
- witness and floor under different retained parents work; a leaf of `../witness` is `Unreadable(Context)`.

**3.3 Privacy** (`compile_boundaries.py`, clients in the parent module): **8/8 rejected inside my line** — a capture
literal assembled from a genuine snapshot and population, replacing one observation, swapping the population, calling
`capture_inner` from the parent (E0603: the phase hook is private to the child), a parent-written inherent impl,
moving the retained snapshot out, writing through an accessor, `Clone`. Two compile and mark the boundary: an
`OperationalBytesObservation` value can be built by anyone (it cannot be put *into* a capture), and the production
entry is callable with caller-chosen context, as the owner says.

**3.4 Mutants** (7, complementary to the owner's three; all compiled; baseline green): **6 killed by owner tests** —
floor-before reading the witness source, witness-after reading the floor source, before-reads in the other order,
before/after swapped in the returned struct, after-reads with an unbounded budget, population taken from a *second*
snapshot opened after the after-reads. **1 survives owner tests and is detected by my probe** — T-1.

## 4. Findings

- **T-1 (low) — the order of the two after-reads is unpinned.** Reading floor-after before witness-after (with the
  phase labels kept in sequence) passes all 93 tests; my probe sees it (`Wa` becomes `w@after-WitnessAfter`). The
  owner's test writes in the first three hooks only. The *before* order is pinned, so either the after order matters
  equally — then write in the `WitnessAfter` hook too — or it does not, and the module comment should say the two
  sides are unordered within themselves. The reference capture takes the four values without an order, so this is
  about making the Rust statement "witness then floor on both sides" either tested or not claimed.
- **N-1 (note, consumer obligation) — a held capture pins the WAL.** While a `BracketedCapture` is alive,
  `PRAGMA wal_checkpoint(TRUNCATE)` from a writer reports busy `(1, 2, 0)`; after it is dropped, `(0, 0, 0)`. Retaining
  the transaction is deliberate and I agree with it; the consumer must bound the lifetime of a capture (assess, then
  drop), or a long-lived read-only assessment will grow the WAL and delay checkpoints for the writer.
- **N-2 (note, caller context)** Nothing relates the three locations to each other: a floor leaf of
  `journal.sqlite` is read as an ordinary file (observed: `Unreadable(Bound)` — refused by size only, not by
  identity; I did not run it with a larger bound), and the same leaf could be given for
  witness and floor. That is "caller context, not authority" as stated; whoever builds the `CaptureSpec` from admitted
  custody owns these joins, and the later assessor must not treat "four observations exist" as "four distinct, correct
  files were read".
- **N-3 (note, scope)** A missing journal is `Err(Carrier(Io NotFound))`, so a fresh installation (no carrier yet —
  the reference's `INIT` disposition) cannot be expressed as a capture; that case needs its own path in the
  composition.
- **N-4 (note)** The bracket detects change *across* the SQL read; it cannot show that a file was stable *between*
  its two reads (A→B→A). The module header already says it proves no file stability; repeat that where the two-capture
  decision is written.

No behavioural defect found.

## 5. Bounded verdict
**149: reviewed, no blocking finding. The five physical reads happen in the stated order with the SQL snapshot fixed
between the file reads; each observation sees exactly the writes that preceded it; the population and the retained
snapshot exclude later rows and markers; absence, empty and unreadable stay distinct per side; every carrier or
population failure yields no capture; the capture cannot be forged, edited, cloned or hooked from outside its module
(8/8); 6/7 ordering mutants die on the owner's tests. T-1: the after-side read order is claimed but untested. N-1 (a
held capture pins the WAL) and N-2 (no relation between the three caller-chosen locations) are obligations for the
composition.** No claim beyond observed facts was found in the module or README. Not approval of decoding, anchor
decisions, custody, exclusion, leases, fences, writers, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `owner/`,
`probes/{rust_probe.rs.txt,compile_boundaries.py,compile-boundaries.json,compile-boundaries.log,compile-*.stderr,mutation.py,mutation.json,mutation.log}`,
`io/bracket.txt`, `hashes.txt`.
