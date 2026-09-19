# Independent review — frozen `stored-pins-checkpoint-177`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 177 bytes — the same-snapshot read of the proposed `active_run_pins` current projection composed over 176's material capture. Separate from my 176 report. Not 178 (unfrozen, not read); no cumulative/authority/host/release approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `7ff4d779a9d62c65434523d4c45b92b99664ae0c9c1fb0a04de672f67c5b006a`, 4,237,164 B — equals request and `archive-pin.json` |
| Members | 433, all regular/safe, verified from the tar before extraction; re-verified at end (`claude-out/pin-verification.json`) |
| Product pins | 350/350; none unpinned (`claude-out/product-pins.json`) |
| Parent | equals **my own verified 176 extraction**: 347 unchanged; changed `ledger_store.rs`, `recovery_material.rs`; added `recovery_pins.rs`. Fixtures unchanged |
| Delta to parent (`claude-out/diffs/changed.diff`) | `recovery_material.rs`: exactly `const DDL` → `pub(super) const DDL`. `ledger_store.rs`: two error variants, `mod recovery_pins`, two private pass-through functions |
| Host receipt 112 | 230 sources equal pins; none failed |
| SHA-256 | `crates/storage/src/ledger_store/recovery_pins.rs` `d80628d5b6e0c7edcd75fade7978951849877dc850e66105169b3e4ec2e2fd2a`;`crates/storage/src/ledger_store.rs` `bd761ede526f8605685ea9b15d0059800e54ee198fc020fd5ede7ea471a00a5d`;`crates/storage/src/ledger_store/recovery_material.rs` `cf67e1bc6fadf791a97ecea5632362315ce69fef22d21ec5b32aaf17a24d44c3` |

## 2. Owner checks re-run

Fresh scratch copy (byte-equal to product), `--offline --locked`, dedicated target: **55 storage tests pass; strict workspace Clippy exit 0** (`claude-out/owner/`). Owner privacy clients: I read the six clients and their stderr — the refusals are the intended diagnostics (E0451/E0616 private fields, E0505, E0515), not incidental compile errors; I did not rebuild them.

## 3. My probe (`claude-out/probes/rust_probe.rs.txt` → `claude-out/io/pins.txt`, bundled SQLite 3.53.2)

| # | Probe | Result |
|---|---|---|
| 1 | 7 own pins (NFC/NFD pair, U+FFFF, astral, case pair) + 500-byte rows under a **foreign store**, a **foreign namespace** and a foreign Run; every (rows 0..=9) × (text 0..=97) | **980 cells, 0 wrong**: Ok iff rows ≥ 7 ∧ text ≥ 95, contents equal my sorted oracle, Run = anchor Run; otherwise `PinReadBudget`. Foreign rows never counted or charged |
| 2 | storage classes under `ignore_check_constraints` | blob pin_id / blob kind → `pin_storage`; invalid UTF-8 and CESU lone surrogate → `pin_text`; `Baseline`, `baseline\0` → `UnknownKind`; integer 5 becomes text `"5"` by column affinity (benign) |
| 3 | schema variants | extra index, extra trigger, rowid table, whitespace change, dropped kind CHECK, same-named view → all `pin_schema`. Lower-case `create table` passes only because SQLite itself normalises that prefix in `sqlite_schema` |
| 4 | no anchor | `pins=None` with no pin table **and with a garbage pin table** — lookup *and* schema check are skipped (as README says) |
| 5 | material body budget 0, valid pins | `RecoveryBodyBudget`; pins discarded |
| 6 | 3 MB name | text budget 10 → `PinReadBudget` before copy; exact 3,000,008 → observed, `names_within_limit=false`; one less → refused |
| 7 | bad first row + short row budget | budget wins; with full budget `UnknownKind`. Never a prefix |
| 8 | forced write + `wal_checkpoint(TRUNCATE)` while holding two Err and one Ok result | busy 0 |
| 9–10 | **UTF-16le database** with the exact DDL | see F-1 |

Probe r1 is preserved as failed evidence (`io/pins-FAILED-r1-utf16-attach.txt`, `probes/rust_probe-r1.rs.txt`): my UTF-16 copy helper used ATTACH, which SQLite refuses across encodings. My error; cases 1–8 of r1 equal r2.

## 4. Mutation (`claude-out/probes/mutation.{py,json,log}`)

cargo tests only (no source pins in play); baseline green first. One mutant ("text exhaustion returns prefix") did not compile and is **not counted**; the owner's own `truncated-prefix-returned` fault covers that ground.

| Mutant | Owner tests | My probe |
|---|---|---|
| invalid UTF-8 read lossily | KILLED | |
| pin failure → `None` | KILLED | |
| row budget checked late | KILLED | |
| **store filter dropped** | SURVIVED | detected (case 1) |
| **namespace filter dropped** | SURVIVED | detected (case 1) |
| **blob values tolerated** | SURVIVED | detected (case 2) |
| **schema check ignores indexes/triggers** | SURVIVED | detected (case 3) |
| **material body budget ignored by pin capture** | SURVIVED | detected (case 5) |
| **`work` and `retained_body_bytes` transposed** | SURVIVED | detected (case 5) |

## 5. Findings

No finding shows the production code returning a wrong inventory for a UTF-8 ledger. One substantive boundary finding and one test-strength finding.

### F-1 (medium-low, fail-open on a claimed refusal) — a UTF-16 ledger is accepted, and malformed stored text is *aliased to a different valid name* rather than refused
README: "unreadable text … refuse the whole capture". Nothing in `open_existing`/`configure`/`ReadSnapshot::open` or the pin schema comparison constrains `PRAGMA encoding`; the `sqlite_schema.sql` text of a UTF-16 database is identical, so the exact-DDL check passes. The reader then validates the UTF-8 that SQLite's transcoder *produces*, not what is stored. Measured:

| Stored UTF-16le pin_id | Read result |
|---|---|
| `D800 0041` (high surrogate then "A") | **Ok, name U+10041** |
| `DC00 0041` (lone low then "A") | **Ok, name U+10041** |
| genuine `D800 DC41` together with `D800 0041` (two PK-distinct rows) | `DuplicateName` (closed) |
| lone `D800` / `DC00` at end | `pin_text` (closed) |

So three byte-distinct stored identities read as one name; singly, each is admitted silently. The row CHECK (`length(CAST(pin_id AS BLOB))>0`) accepts them, so no constraint bypass is needed. Consequences today are bounded — this is a disclosure inventory with no writer — but the README's future writer must "update this projection atomically", and a name the reader reports will not match the stored key in a `WHERE pin_id=?`. Also the `text_bytes` budget then measures transcoded bytes (disclosed) of text that is not the stored value (not disclosed).
Systemic remedy (not a per-column patch): one owner decision on ledger text encoding, enforced once at `ReadSnapshot::open`/`open_existing` (`PRAGMA encoding` must be UTF-8, else a typed configuration refusal), which also covers every earlier text column in this module; plus one UTF-16 negative. If UTF-16 ledgers are meant to be legal, the law must instead say how malformed UTF-16 is detected (e.g. compare `CAST(pin_id AS BLOB)` round-trip), which is more invasive.

### T-1 (test strength, medium) — six behaviour-changing faults pass all 55 tests
The owner tests vary only the Run. Store and namespace scoping — two of the three key columns that make this a *scoped* read — are unexercised; so are non-text storage classes (the `pin_storage` arm has no test at all), schema companions (index/trigger), and the composition with 176's body budget (every pin test passes 16 MiB, so ignoring or **transposing** the two adjacent `usize` limits is invisible). The transposition survivor makes my 176 N-1 concrete: it is now a five-positional-argument call with two interchangeable `usize`s followed by a struct of two more. Remedies: foreign-store and foreign-namespace rows in the scoping test; a blob row; an extra-index schema negative; one pin read with body budget 0 expecting `RecoveryBodyBudget`. A newtype for the body budget would turn the transposition into a compile error.

### N-1 (note) — with no anchor the pin schema is not examined
`pins=None` is returned even when `active_run_pins` is garbage. Disclosed ("No anchor skips the lookup") and harmless for this reader, but a host must not read `None` as "pin schema admitted". The accessor doc says "no joined Run, so no pin lookup"; adding "and no schema judgement" would close the gap.

### N-2 (note) — text budget is charged before UTF-8 validation
So a row with invalid UTF-8 that also exceeds the text budget reports `PinReadBudget`, not `pin_text`. Both refuse the whole capture; only a future host mapper needs the precedence. Actual order measured: row count, storage class, text budget, UTF-8, then (after the loop) empty/kind/duplicate.

### N-3 (note) — `ORDER BY pin_id COLLATE BINARY` is not what orders the result
`Inventory::from_rows` re-keys into a `BTreeMap`; removing the ORDER BY is an equivalent mutant (I did not count it). The SQL order only fixes *which* row trips the row budget, which is unobservable since refusal is whole-capture. Harmless; in a UTF-16 database BINARY order would differ from Rust order, another reason for F-1's single-encoding rule.

## 6. Claims checked and confirmed

Same `ReadSnapshot` for material and pins (owner hook test + code reading: one `snapshot` borrowed through both calls; fresh-snapshot fault killed by owner); Run comes only from the joined anchor; whole-capture refusal on every failure I produced, never `None`, empty or prefix; max+1 row advance distinguishes exhaustion; charge precedes copy; legacy over-limit observable within explicit bounds with `within_budget=false`; SQL released on Ok and Err; private fields; no production creator/writer of the table (grep: DDL executed only under `cfg(test)` and on an in-memory expectation connection).

## 7. Earlier findings

176 T-1/T-2 are against 176 bytes and are not addressed or regressed here (176 files otherwise byte-identical apart from DDL visibility). 176 N-1 is upgraded by evidence to part of T-1 above. 172 N-1, 175 F-1/F-2 remain with their owners.

## 8. Limits

Synthetic storage fixtures; bundled SQLite 3.53.2 only — the UTF-16 transcoder behaviour in F-1 is version-dependent (newer/older SQLite may map the malformed pairs to U+FFFD instead, which is still aliasing). I did not measure heap, did not test big-endian UTF-16, and did not rebuild owner privacy clients. Probe code was appended to a scratch copy's test module only.

## 9. Verdict (bounded)

**For UTF-8 ledgers the frozen 177 reader behaves as claimed on every case I could construct (980-cell grid, 0 wrong). F-1 is a real hole in the "unreadable text refuses" claim and wants one owner decision on ledger encoding; T-1 lists six faults the owner suite cannot see.** No approval of the proposed DDL as a selected schema, of any writer, or of cumulative readiness.
