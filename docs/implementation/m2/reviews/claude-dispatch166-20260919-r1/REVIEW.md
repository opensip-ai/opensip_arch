# Independent bounded review — names-first read-only carrier dispatch 166 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: received as a chat message (`claude-out/REQUEST-as-read.md`); subject README read. Scope: the delta of frozen
`carrier-dispatch-checkpoint-166` over frozen 164 — new `journal_store/carrier_dispatch.rs`; the shared read-only
connection / definition admission extracted from `CurrentCarrierSnapshot::open`; `from_admitted_connection`; tests for
my 162 T-1. Not wired into the physical bracket or any host route; no authority, custody or SQLite-path claim, and I
infer none. No frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit, push or delegation; no
cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,241,976 bytes, SHA-256 `7ff2a63885765e3a5de976ea7690477473c12020f8838c5767522f72da5020a4` = request = `archive-pin.json` |
| Members | 437/437 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 345/345; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 164 extraction (344/344); 342 unchanged, 2 changed, 1 added |
| Host pins | host102 receipt: 225 sources all equal the product pins; no command failed |
| Owner checks, fresh scratch | 133/133 security tests; strict workspace Clippy clean |

## 2. Dispatch law vs the code (carrier-format.v3 §8 steps 1–8; `readOnlyStandingOfDispatchResult`)
| Law | Code | |
|---|---|---|
| 1 names only, from `sqlite_master` | one `SELECT type,name,sql … WHERE name COLLATE NOCASE IN (seven) … LIMIT 8` — first statement after `BEGIN`, so it fixes the snapshot | ✔ (it also reads the `sql` text, as owned evidence; no table is read) |
| 2 none present → 6–8, "read no v3 table at all" | `objects.is_empty()` → only two further `sqlite_schema` lookups | ✔ no absent table is touched |
| 3 some but not all → corrupt | `objects.len() != 7` → `PartialFootprint` (also **more** than seven: a trigger may reuse a table's name) | ✔ |
| 4 any definition differs → corrupt, **before any row read** | `admit_carrier_definitions` (exact inherited + current DDL) precedes both row queries | ✔ |
| 5 row present → format 3; absent + v3 rows → corrupt; absent → incomplete | `EXISTS(carrier_format)` → `from_admitted_connection` on the **same connection**; else `RowsBeforePublication` / `IncompletePublication` | ✔ |
| 6 / 7 inherited 2 / 1 by table + trigger **names** | `type='table' … 'grant_journal'`, then trigger `gj_seq_contiguous`, both NOCASE | ✔ names-only, as the README says |
| 8 no journal table → fresh install (read-only: bound carrier observed absent) | `BoundCarrierMissing`; nothing is created | ✔ |

The five kinds and three errors map one-to-one onto the law's dispatch results (`fresh-install`, `carrierFormat1/2`,
`incomplete-footprint`, `carrierFormat3`, `migration-footprint-corrupt`) — with one exception, F-1.

## 3. Evidence
**3.1 Carriers built independently** (`probes/gen_dispatch.py`, Python `sqlite3` + the frozen DDL files; 27 files):
WAL database with no tables / a foreign table / a **view** named `grant_journal` → `BoundCarrierMissing`; legacy 1 and 2
(also with a tampered definition — names-only, and a table spelled `GRANT_JOURNAL`) → `ObservedInherited1/2`, 0 objects;
legacy + acts A,B and a fresh seven-object footprint without a row → `IncompletePublication`, 7 objects; published
fresh / migrated 1 / migrated 2 → `PublishedCurrent` with a borrowed current snapshot; other project key → `Binding`;
six of seven names (with an inherited table present), a lone `Carrier_Format` table, and **eight** matches (a trigger
reusing the name `grant_journal_v3`) → `PartialFootprint`; all seven names with one wrong body, and an **index** standing
in for a trigger name → `Definition`; missing path → `Io(NotFound)` and **no file is created**. 25/25 expectations met;
2 observations → F-1. (The frozen v3 DDL refused my attempt to insert a v3 row without a format row, so that state needs
a bypass; the owner's test covers it and its mutant is killed.)

**3.2 Same SQL snapshot** (`io/snapshot.txt`, private hook, separate writer connection): a writer performing acts **B
and C** after the names read → the capture still says `ObservedInherited1`; a writer publishing the row after the names
read → still `IncompletePublication`; in both, a **new** capture says `PublishedCurrent`. While a dispatch is held,
`wal_checkpoint(TRUNCATE)` is busy (1); after drop, 0 — the retained connection is a live reader by design (N-2).

**3.3 Private / lifetime surface** (`probes/compile-boundaries.log`): 7/7 rejected — dispatch literal, re-classifying,
editing the owned definitions, reaching the hook, a borrowed current snapshot outliving its dispatch (E0515), moving the
current snapshot out, `Clone`. Three compile and mark the line (N-1).

**3.4 Mutants** (`probes/mutation.py`, 9, all compiled, baseline green): 4 killed by the owner's tests. **5 survive all
133 tests and are each caught by my carriers — T-1.**

**3.5 162 T-1:** the record-budget and independent logical-budget propagation tests are present; the logical one uses a
valid generation-1 marker so the UTF-8 stored cap cannot mask the fault — a correct reading of why my suggested
"total − 1" alone would not isolate it. I did not re-run my two 162 mutants here (the owner reports both killed; the
production lines are unchanged since 162).

## 4. Findings
- **F-1 (low–medium) — one error value covers two results the law routes to opposite public classes.** A carrier file
  that is **zero bytes**, or a database **not in WAL mode**, returns `Err(Read(Definition))` — the same value as "all
  seven names present, one definition wrong". The law sends the second to `migration-footprint-corrupt` →
  `unknown-quarantine-condition` → `LEDGER.CORRUPT`, but describes the first as "the bound carrier is lost, **emptied**
  or a fallback" → `fresh-install` → `unknown-custody` → `HOST.IO_FAILURE`. `CarrierReadError::Definition` is raised by
  `read_only_carrier_connection` for connection configuration and journal mode *and* by definition admission for schema
  text, so a host mapper (168 and later) cannot tell "this is not a carrier at all" from "this carrier's footprint is
  corrupt" — and would report corruption for an emptied file. Give the connection/journal-mode refusals their own
  variant (or have dispatch classify an empty schema before the WAL requirement), and pin one zero-byte and one
  non-WAL case.
- **T-1 (low) — five narrow regressions pass all 133 tests; my carriers catch each.**
  | Surviving mutant | Isolating carrier |
  |---|---|
  | more than seven matching names tolerated | seven objects + a trigger reusing the name `grant_journal_v3` |
  | a **view** named `grant_journal` counts as an inherited table (law: table) | that view |
  | inherited table matched case-sensitively | table spelled `GRANT_JOURNAL` |
  | inherited observed although **some** v3 names exist (law step 3 must win over 6/7) | legacy + six of seven names |
  | owned definition records dropped for current carriers | any published carrier (`objects()` length) |
- **N-1 (note, constructor surface)** `CurrentCarrierSnapshot::from_admitted_connection(c, key, inherited)` is private
  to `journal_store`, and "admitted" is a naming contract: inside the module it accepts any `Connection` (client
  compiles) and re-validates the **row**, not the definitions. Today both callers admit first, and `InheritedFormat`
  cannot be fabricated, so nothing is wrong; a sealed `AdmittedCarrierConnection` returned by
  `admit_carrier_definitions` would make "definitions before row" a type fact rather than call-order discipline,
  which is the property this candidate exists to guarantee.
- **N-2 (note)** `CapturedDispatch` always retains its connection and read transaction — also for the three
  non-current kinds, where only a classification and ≤ 7 owned records are needed. You state 168 will release SQL
  explicitly; until then the 149 N-1 obligation (bound the lifetime) applies to every holder of a dispatch.
- **N-3 (note)** `ObservedInherited1/2` are names-only by design: a tampered legacy definition is still "observed
  inherited" (demonstrated). That is right for F46 (`unknown-carrier-incompatible` "from the object names alone"), and
  the README says so; no consumer may treat these kinds as admission of the inherited format — 155's exact admission
  is reached only on the published path.

No behavioural defect found in the dispatch itself.

## 5. Bounded verdict
**166: reviewed, no blocking finding. The dispatch follows carrier-format §8 step for step: names first and
case-insensitively, no absent table read, partial (or excess) footprints refused, all exact definitions before any row
read, rows-before-publication distinguished from an incomplete publication, and the current snapshot built on the same
connection without reopening — and everything after the names read is in one SQL snapshot even when a writer performs
acts B and C in between (measured). A dispatch cannot be forged, re-classified, edited or cloned, and its borrowed
current snapshot cannot outlive it (7/7). F-1: a zero-byte or non-WAL file yields the same `Definition` error as a
corrupt footprint, although the law routes them to `unknown-custody` and `LEDGER.CORRUPT` respectively — separate them
before a host mapper consumes this. T-1: five narrow regressions are unpinned.** Not approval of bracket wiring, host
routes, custody, SQLite path binding or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{gen_dispatch.py, rust_probe.rs.txt, mutation.py, mutation.json, mutation.log, compile-boundaries.json/.log}`,
`io/{scenarios.json, rust.ndjson, snapshot.txt}` (`io/dbs/` regenerable with `gen_dispatch.py`), `hashes.txt`.
