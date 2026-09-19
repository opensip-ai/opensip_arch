# Independent bounded review — historical SQL generation reader 154 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: the user's message of 2026-09-19 for frozen `historical-sql-checkpoint-154` (no separate request file was
named). Scope: the delta over frozen 152 — one `mod` declaration and the new private `journal_store/historical_rows.rs`:
capture of **one requested inherited generation** from the caller's retained SQLite transaction. It admits no carrier
DDL, population, origin, custody, SEAL or current authority, and I infer none. No frozen/selected/product edit; scratch
only, `-I -B`, dedicated targets; no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,212,836 bytes, SHA-256 `4621ec02440f8902a77bee167e28fc3fb9b70cc1ec1641a5ca29ac57ddfc37b8` = request = `archive-pin.json` |
| Members | 410/410 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 340/340; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 152 extraction (339/339); 338 unchanged; `journal_store.rs` changes by exactly `mod historical_rows;`; 1 added |
| Embedded pins | `parent152`, `reference151` equal the real archives; both provenance sources equal my 151 extraction |
| **Embedded DDLs** | the two test-only DDL strings are **byte-identical** to the frozen sources: DDL2 = the whole file `security-schemas.v2/grant-journal.sql`; DDL1 = the fenced block in `security-completion.v1.md` |
| Host pins | host96 receipt: 220 sources all equal the product pins; 8/8 commands exit 0 |
| Owner checks, fresh scratch | 104/104 security tests; strict workspace Clippy clean |

## 2. Evidence

**2.1 Carriers the reader never saw being built** (`probes/gen_carriers.py`, `rust_probe.rs.txt`, `compare.py`). My
writer is Python `sqlite3` executing the *frozen DDL files themselves*, with bodies from the pinned v8 canonicalizer and
my own chain arithmetic — not the owner's Rust helpers. 289 database files, 319 scenarios, both DDLs × UTF-8 / UTF-16le /
UTF-16be: all 14 kinds ending in each terminal cause, open and empty generations, a second generation, an absent
generation; four chain disagreements (wrong mid-chain value, upper-case hex, non-hex, another project's genesis);
three digest failures (wrong, upper-case, unframed); 17 mirror/physical-type cases per DDL × encoding; gaps, start at 2,
rows after each terminal cause, two terminals (DDL2's trigger dropped only for construction); body generation and body
sequence not matching the row; non-canonical, schema-3 SEAL and `recordSchema: 3` bodies; exact and one-under limits for
records, stored octets and logical bytes; generation 0/−1; and — by patching the database *file* — lone high/low
surrogates inside a UTF-16 body, a body in the other endianness, BOM-prefixed bodies, invalid UTF-8 and a raw NUL.
**319 / 319 as expected**: row count, every digest, SHA-256 of every stored body, every observed previous-digest string,
encoding, chain standing, end — or the exact error class. For every admitted row the stored octets are exactly the
database-encoding form of the owned logical UTF-8 bytes.

**2.2 Chain is diagnostic, body is not**: all 24 chain disagreements are admitted as `Unverifiable` with the observed
strings retained verbatim (including upper-case and non-hex); all 18 digest disagreements are refused.

**2.3 Mirrors under SQLite's own transcoding** (`mirror_transcoding.py`). Only the body is decoded from exact octets;
the mirror columns arrive through SQLite's UTF-16→UTF-8 conversion. I patched only the mirror to a lone high / low
surrogate while the body held U+FFFD or U+1F600, both endiannesses: **8/8 refused (`RowBinding`)** — I found no
physically malformed mirror that compares equal.

**2.4 Transaction ownership** (`io/transactions.txt`, real WAL file, separate writer connection):
autocommit → `SnapshotRequired`; within one transaction a second capture does not see a row committed meanwhile; a new
transaction does (and reports its wrong chain value as `Unverifiable`). Three facts about what `is_autocommit() ==
false` does *not* establish — N-1.

**2.5 Privacy** (`compile_boundaries.py` + `-r2`): 12/12 rejected — prefix/row literals, upgrading `chain`, changing
`end`, dropping rows, replacing stored octets, writing through `rows()`/`stored_body()`, `Clone`, reaching
`logical_bytes`, converting into a current `GenerationPrefix`, a forging impl. (My first `rows()` client used `todo!()`
and proved nothing; replaced, both preserved.) Bare `End`/`ChainStanding` values, `Limits` and the entry itself are
plain caller context, as stated.

**2.6 Mutants** (`mutation.py`, 23, all compiled, baseline green; narrower than the owner's ten whole-check removals):
14 killed by the owner's tests. 9 survive them: **5 detected by my carriers (T-1)**; 3 not meaningful (disclosed); 1
unreachable through SQLite (N-4).

## 3. Findings
- **F-1 (low–medium, historical compatibility — an owner decision is being made implicitly).** The mirror rule is
  "column = body member when the body has it, **NULL when it does not**", for request_ref, token,
  install_generation_id, manifest_digest and platform. I could not find that law in the frozen sources. What they say:
  DDL1's CHECK requires install/manifest/platform on GRANT but **not `token`** (DDL2 adds it), and the column comment is
  "PT-* on grant-bearing records". So (a) a DDL1 GRANT row with `token` NULL is *lawful under its own frozen DDL* and is
  refused here (`d1-*-mirror-DDL1-permits-GRANT-token-null` → `RowBinding`); (b) a legacy writer that also stamped the
  token or request id on NARROW/EXPIRY rows would be refused. Refusal is of the **whole generation**, and from 155 on, of
  the whole carrier. Being strict is defensible ("refuse, never guess"), and no real legacy writer may exist; but it is
  a compatibility decision, not a derivation. Please either cite the source of the NULL-iff-absent rule or record it as
  an explicit owner choice with its consequence (unreadable, never relabelled) — and keep the one DDL1-only case as a
  named test so the choice is visible.
- **T-1 (low) — five narrow regressions pass all 104 tests; my carriers catch each.**
  | Surviving mutant | Isolating carrier |
  |---|---|
  | mirror may be NULL although the body has the value | `request_ref` NULL on an RA row (9 cases) |
  | body `seq` not bound to the row's `seq` (README lists "body generation mismatches"; the sequence twin is absent) | body seq 2 stored at row 1 |
  | non-hex / upper-case previous digest still `Consistent` | 64 × `z`; upper-case genesis |
  | genesis previous computed for generation 1 regardless of the request | a consistent generation 2 |
  | lone surrogate replaced by U+FFFD instead of refused | file-patched UTF-16 body |
- **N-1 (note, transaction ownership)** `is_autocommit() == false` is the whole precondition. It is also true (T5) for a
  deferred `BEGIN` that has not read yet — the snapshot then starts at *this* reader's first statement, not at `BEGIN`;
  (T6) inside the caller's own **write** transaction, whose uncommitted rows are captured as history; (T7) under a bare
  `SAVEPOINT`. None is a defect of a reader that says "the caller retains the transaction", but the opening owner must
  be the one that guarantees read-only + already-reading (155 does: `query_only`, its own `BEGIN`, earlier reads).
- **N-2 (note)** `records: usize::MAX` is `Bound`, not "unlimited" (the `+1` probe row overflows `i64`); harmless,
  worth a line where limits are documented.
- **N-3 (note)** Rows whose `grantGeneration` is not the requested INTEGER are invisible to this reader by
  construction (`WHERE grantGeneration = ?`); text/real/blob generations in the legacy table are the population
  owner's to find. "Empty" therefore means exactly what the README says and no more.
- **N-4 (note)** The odd-length UTF-16 refusal is unreachable through SQLite (it stores UTF-16 text with an even byte
  count; I could not construct a counter-example, and the mutant survives both suites). Keep it — it is the right
  defence if the octets ever arrive by another route.
- **Disclosed, my own mutants that prove nothing:** "chain continues from the observed value" was a no-op edit (my
  slip); "query not ordered by seq" is equivalent under both frozen DDLs because the WITHOUT ROWID primary key already
  yields `(grantGeneration, seq)` order — the `ORDER BY` is still right to keep.

No behavioural defect found.

## 4. Bounded verdict
**154: reviewed, no blocking finding and no behavioural defect. On 319 scenarios over 289 databases built by an
independent writer from the frozen DDL files, in all three encodings, the reader returns exactly the expected rows,
digests, stored octets, observed chain strings, diagnostics and error classes; chain disagreement never invalidates and
body disagreement always does; rows after either terminal cause, gaps, wrong physical types, malformed UTF-16 and
foreign-schema bodies are refused; a prefix cannot be forged, upgraded or converted into a current prefix (12/12).
F-1: the NULL-iff-absent mirror rule is stricter than frozen DDL1 and is not cited — decide it explicitly. T-1: five
narrow regressions are unpinned by the owner's tests.** Not approval of carrier DDL admission, population, origin,
custody, SEAL joins, selection or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `owner/`,
`probes/{gen_carriers.py (r2), gen_carriers-r1.py, mirror_transcoding.py, rust_probe.rs.txt, compare.py, compile_boundaries.py, compile-boundaries.json/.log, compile-boundaries-r2.json, compile-*.stderr, mutation.py, mutation.json, mutation.log}`,
`io/{scenarios.json, rust.ndjson, compare.txt, compare.json, transactions.txt, mirror/, r1-utf16-harness-slip/}`
(`io/dbs/` holds the 289 databases; regenerate with `gen_carriers.py`), `hashes.txt`.
Harness slips, preserved: r1 tried to store malformed UTF-16 through Python's UTF-8 API (SQLite re-encoded it; 8 rows
tested nothing — r2 patches the file); one compile client and one mutant were vacuous.
