# Independent bounded review — dispatch composed into the physical bracket, 168 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: received as a chat message (`claude-out/REQUEST-as-read.md`); subject README read. Scope: the delta of frozen
`dispatch-capture-checkpoint-168` over frozen 166 — `carrier_dispatch.rs` (seal, non-current observation, transfer
type), `bracketed_capture.rs` (bracket consumes the dispatch), `journal_store.rs` (`Configuration` error; sealed
`from_admitted_connection`), `generation_anchor.rs` (tests). **No** host mapper, custody, location relation, ABA or
exclusion claim, and I infer none. No frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit,
push or delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 8,187,144 bytes, SHA-256 `aa058c1c025844be0cfdeda5e31ca08e1074deafe70c4386d7801b08b3dd7432` = request = `archive-pin.json` |
| Members | 863/863 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 345/345; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 166 extraction (345/345); 341 unchanged, 4 changed, 0 added |
| Host pins | host104 receipt: 225 sources all equal the product pins; no command failed |
| Owner checks, fresh scratch | 138/138 security tests; strict workspace Clippy clean |

## 2. What changed (read in full)
The bracket is now: witness-before → floor-before → **dispatch** (names, exact definitions, row — one connection, one
snapshot) → `into_carrier()`. `Current` hands the *same* `CurrentCarrierSnapshot` to `capture_population` and the two
after-reads, with no reopen. `NonCurrent` drops the SQL reader, then returns `Err(CaptureError::NonCurrent(..))` owning
the kind, the ≤ 7 definition records and the two before-observations: no population, no after-reads, no anchor input.
`read_only_carrier_connection` raises `Configuration` for connection settings and journal mode; `Definition` is left
for schema text. `from_admitted_connection` takes the private-field `AdmittedCarrierConnection`, produced only by
`admit_connection`, which really runs definition admission.

## 3. Evidence
**3.1 My 166 dispatch probe, unchanged, on this tree** (27 Python-built carriers): output identical to 166 **except
exactly the two F-1 rows** — zero-byte file and non-WAL database now `Read(Configuration)`; the corrupt footprints stay
`Read(Definition)`. The same-snapshot measurements are unchanged (a writer performing acts B **and** C after the names
read does not change the captured kind; a new capture sees `PublishedCurrent`).

**3.2 The real bracket over the same carriers** (`probes/rust_probe_bracket.rs.txt` → `io/dispatch/bracket.ndjson`;
malformed witness on disk, floor absent; the hook rewrites the witness after the before-reads):
- 12 non-current carriers → `NonCurrent` with the right kind (3 `BoundCarrierMissing`, 5 `ObservedInherited1/2`, 4
  `IncompletePublication`), 0 or 7 owned records, `witness_before = Present("{")`, `floor_before = Absent`; the hook
  ran **2** phases — nothing was read after the dispatch; the later witness rewrite is not in the evidence;
- 3 published carriers → a bracket with all **5** phases; `witness_after` sees the rewrite, `witness_before` does not;
- 12 refusals keep their class: `Carrier(Io)`, `Carrier(Configuration)` ×2, `Carrier(Sql NotADatabase)`,
  `Carrier(Binding)` ×2, `Carrier(Definition)` ×2, `Dispatch(PartialFootprint)` ×4.
- **SQL release, with a forced write** (r2 — my first measurement without a write could not conflict with any reader
  and is preserved as `bracket-r1-no-forced-write.ndjson`): `wal_checkpoint(TRUNCATE)` while the result is still held is
  **0 for all 12 non-current results and all refusals, 1 for the 3 current brackets** — exactly the design (a current
  bracket holds its transaction until `into_observations`; `read` detaches, 150/156).

**3.3 The anchor path did not move**: my frozen-150 physical differential (adapted only to the 164 `FileSource` type)
through the composed bracket — 12,432 reads + 96 between-capture scenarios judged by the reference law → **0
mismatches**, capture counts equal, no reader left between captures or in held assessments.

**3.4 Closure, executed** (`probes/mutation.py`, 10, all compiled, baseline green): my five 166 T-1 survivors and the
F-1 conflation — **all killed** by the owner's tests; plus four composition mutants (non-current reader leaked with
`forget`; non-current evidence losing its records; witness/floor swapped in non-current evidence; dispatch `Read`
errors losing their class) — **all killed**.

**3.5 Seal / privacy** (`probes/compile-boundaries.log`): 8/8 rejected — raw `Connection` into
`from_admitted_connection` (E0308), seal literal around an unadmitted connection, swapping the connection inside a
seal, non-current observation literal, non-current capture literal, writing through its accessor, `Clone`, bracket
literal with an invented population. Three compile and are exactly the limits the README states (N-1).

## 4. Findings
No defect and no finding of substance.
- **N-1 (note, stated limits — confirmed, not more)** `admit_connection` seals *any* connection the module holds after
  really admitting its definitions: the seal is "definitions admitted at this snapshot", not read-only, not `BEGIN`,
  not custody. `DispatchedCarrier` is a plain transfer enum (the parent owns `CurrentCarrierSnapshot` anyway). An
  **unconsumed** `CapturedDispatch` still holds its reader. All three are in the README; I agree with how they are
  worded.
- **N-2 (note, for the host mapper that does not exist yet)** A lawful, fully observed classification
  (`NonCurrent`) travels on the **error** channel beside I/O and corruption refusals, and — as with 150 F-2 — a
  non-current result on the *second* capture discards the first capture's evidence. Both are deliberate and tested.
  The mapper must therefore branch on the variant, never on `is_err()`: `NonCurrent(BoundCarrierMissing)` →
  `unknown-custody`, `ObservedInherited*` → `unknown-carrier-incompatible`, `IncompletePublication` →
  `unavailable-busy`, `Carrier(Configuration)` → `unknown-custody`, `Carrier(Definition)` / `Dispatch(*)` → the
  footprint-corrupt route with its stable-observation rule (carrier-format §8.1, `readOnlyStandingOfDispatchResult`).
  A table like this belongs next to the type when the mapper is written.
- **N-3 (note)** For non-current kinds the malformed witness on disk is, correctly, *not* evaluated (F46 / names-only:
  "needs no witness comparison"); it is retained as bytes. Nothing downstream should re-derive a quarantine condition
  from `witness_before` of a `NonCurrentCapture`.
- Carried and still open by your own statement: no relation between the journal location and the two file bindings
  (149 N-2), A→B→A, exclusion, 124 F-1 / 118 I-2, 150 F-2 host mapping, 165 writer disposition.

## 5. Closure of my 166 items
| Item | Status |
|---|---|
| **F-1** one `Definition` error for "not a carrier" and "corrupt footprint" | **Closed** — `Configuration` vs `Definition`; zero-byte and non-WAL pinned; mutant killed; my probe moves in exactly those two rows |
| **T-1** five unpinned regressions | **Closed** — all five killed by one named test |
| **N-1** "admitted" as a naming contract | **Closed** — sealed `AdmittedCarrierConnection`; raw connection rejected by type |
| **N-2** every dispatch holds a live reader | **Closed for the bracket** — non-current SQL released before evidence is returned (measured with a forced write); unconsumed dispatch still holds it, as stated |
| **N-3** names-only inherited kinds | restated accurately |

## 6. Bounded verdict
**168: reviewed, no finding of substance. The physical bracket now consumes the real dispatch: a published carrier
keeps one admitted SQL snapshot from the names read through the population to the final file reads without reopening; a
missing, inherited or unpublished carrier returns sealed owned evidence (kind, definition records, the two
before-observations) with its SQL reader already released, no after-reads and no anchor input; refusals keep their
class, and "not a carrier" is now distinguishable from "corrupt footprint". On my 27 independent carriers only the two
F-1 rows moved; my 150 anchor corpus gives 0 mismatches through the composed bracket; all ten of my mutants — the six
carried from 166 and four new — are killed by the owner's tests; the seal cannot be forged or bypassed by type (8/8).**
Not approval of a host mapper (none exists), custody, location relation, ABA/exclusion, or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{rust_probe_bracket.rs.txt, rust_probe150-adapted.rs.txt, mutation.py, mutation.json, mutation.log, compile-boundaries.json/.log}`,
`io/dispatch/{scenarios.json, rust.ndjson, snapshot.txt, bracket.ndjson, bracket-r1-no-forced-write.ndjson}`,
`io/anchor150/{between.ndjson, *-compare.json, compare.txt}` (the large `physical.ndjson` is removed after comparison),
`hashes.txt`. The dispatch probe and carriers are the unchanged files of my 166 review.
