# Independent bounded review — frozen historical record bodies 152 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `history152-20260919-REQUEST.md`. Scope: the delta of frozen `historical-records-checkpoint-152` over frozen
150 — one `mod` declaration, the new private `journal_store/historical_record.rs` and its fixture. A **pure decoder of
logical recordSchema-1 bodies**: canonical bytes, domain-framed digest, 14 closed shapes. No SQL reader, mirrors,
population, origin, chain, custody or admission claim, and I infer none; the current carrier still refuses inherited
history. No frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit, push or delegation; no
cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,140,420 bytes, SHA-256 `54a2f9995a543f6671a3a23991d5c82bd151baa3cf72dfa6471e1d8e7e93b2ab` = request = `archive-pin.json` |
| Members | 401/401 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 339/339; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 150 extraction (337/337); 336 unchanged; `journal_store.rs` changes by exactly `mod historical_record;`; 2 added |
| Embedded pins | `parent150`, `reference151` equal the real archives |
| Schema inputs | both provenance inputs equal my 151 extraction: `security-schemas.v8/journal-record.schema.json` `3c090afa…d63d`, `security_unit_lib_v8.py` `3e28bc7b…6d40` |
| Owner checks, fresh scratch | 98/98 security tests; strict workspace Clippy clean (on the final bytes) |

No host receipt is claimed for 152; I agree none is needed for a private pure module with no new dependency or caller
(the workspace builds and lints here).

## 2. Evidence

**2.1 The actual schema, structurally** (`probes/table_vs_schema.py`). Parsed from the frozen JSON and from the Rust
source: the 14 kinds; for every kind `required == properties == COMMON + extra` and `additionalProperties: false`;
all eight enums (with the RCO/ICO difference); the four scope arrays' `(maxItems, maxLength, uniqueItems, minLength)`
and `stateClass`; CLN residuals (256 × 256, duplicates permitted); integer ranges (generation and from/toSchema to
i64 max, the four sequences to uint53). **All equal.**

**2.2 Independent differential** (`probes/oracle.py`, `gen_cases.py`, `rust_probe.rs.txt`, `compare.py`). My oracle
is *strict parse + the third-party `jsonschema` Draft 2020-12 validator over the frozen schema file + the pinned
canonicalizer*, not the unit lib's own validator and not the Rust table. My corpus is 4,512 distinct byte strings:
every field missing / eleven wrong types / every foreign field added, all integer edges, every enum value of the
schema tried in every string field plus case/space/newline/truncation variants, every kind re-typed as every other
kind and as `SEAL`, recordSchema 0/−1/2/3; 14 character classes (2/3/4-byte, NFD, Hangul jamo, C0, NUL, DEL, U+2028,
unassigned, noncharacter, PUA, BOM) at every code-point length edge of every bounded string; item-count edges and
duplicate rules for every array; UUID, wall-clock, operationRef and hex lexical variants; 22 non-canonical encodings
of each valid kind (whitespace, key order, escapes, duplicate keys, `1.0`, `1e0`, `01`, `+1`, `-0`, BOM, UTF-16,
two documents, truncation, 20-digit integers) and non-documents.
**4,512 / 4,512 agree (651 admitted, all 14 kinds): acceptance, digest and alias.** On every admitted record the owned
bytes equal the input, re-encoding the owned document reproduces them, and the current `JournalRecord::parse` refuses
them. Error classes are coherent: parse/canonical failures → `Metadata`, 3,578 schema failures → `Shape`, 86
well-formed non-canonical encodings → `NonCanonical`.
**The owner's 1,624 fixture rows re-judged by my oracle: 0 disagreements (214 admitted).**

Facts this establishes, as claimed: lengths are counted in **code points** (64 astral characters admitted, 65
refused); wall-clock is lexical only (`9999-99-99T99:99:99Z` admitted, non-ASCII digits and `z`/`t` refused); scope
duplicates refused, CLN residual duplicates admitted; NFC is required; a schema-1-shaped body with `recordSchema: 3`
or `recordType: "SEAL"` is refused.

**2.3 TERMINAL agreement in both directions** (`rust_probe2.rs.txt`, 6,136 inputs = my corpus + the owner's): every
TERMINAL the historical decoder admits is admitted by the existing `terminal_body` with equal document, bytes and
digest (23); none is admitted only by the historical decoder. Eight non-canonical TERMINAL encodings are accepted by
`terminal_body` **alone** — it canonicalises and leaves the `body != canonical` refusal to its caller
(`GenerationPrefix::verify`, l. 315), whereas `decode` gates itself. Not a defect; a difference a future shared caller
should know (N-3).

**2.4 Privacy** (`compile_boundaries.py`, clients in the parent): **10/10 rejected inside my line** — record literal,
replacing digest or bytes, writing through `raw()` / `document()`, `Clone`, reaching `shape`, `into()` a
`JournalRecord`, passing a historical record where a current one is expected, a parent-written forging impl. Three
compile and mark the line (N-1).

**2.5 Mutants** (`mutation.py`, 24, all compiled, baseline green): 16 killed by the owner's corpus. 8 survive it:
**3 are detected by my corpus (T-1)**, 3 are vocabulary extensions that no sampled corpus can kill (N-2), 2 are
equivalent (disclosed below).

## 3. Findings
- **T-1 (low–medium) — three boundaries the README relies on are not in the 1,624 rows.** Each mutant passes all 98
  tests and is caught by my corpus:
  | Surviving mutant | Why it matters | Isolating row |
  |---|---|---|
  | `recordSchema` 1 **or 3** admitted | "no relabel to 3": a schema-1-shaped body claiming schema 3 would be owned as history with a journal.1 digest | any valid body with `recordSchema: 3` (14 of my cases) |
  | `"SEAL"` admitted as a schema-1 kind | "never … a schema3 SEAL" | one schema-1-shaped body with `recordType: "SEAL"` |
  | wall-clock `…z` admitted | lexical pattern is the *only* check on this field | `2026-09-17T00:00:00z` |
  The test's own assertion "`JournalRecord::parse` refuses every admitted body" does not cover the first two: it only
  runs on rows that exist.
- **N-1 (note, claim slightly ahead of the type)** "exposes platform strings only through
  `platform_historical_alias`": `document()` returns the whole value, so the parent reads `platform` directly (client
  compiles). The accessor is a *name* that prevents accidental relabelling, not an enforcement. If the alias
  distinction must survive into 154/155 consumers, prefer typed accessors over `document()` there. Likewise the
  separation from the current parser is a run-time refusal (tested on all 651 + 214), not a type-level impossibility
  of *trying*.
- **N-2 (note, method)** Closed vocabularies cannot be pinned by sampling: adding `HE-3`, a fifth REV reason or a third
  TERMINAL cause survives both corpora, because only a row carrying the invented word can see it. §2.1 is the check
  that covers this class (tables equal today); it is cheap enough to keep as an owner check beside the fixture.
- **N-3 (note)** see §2.3: `terminal_body` is tolerant where `decode` is strict; keep the canonical gate with whichever
  function a unified reader calls.
- **N-4 (note, data hygiene for the next layers)** As the frozen schema allows, free strings admit C0 controls
  (escaped in canonical bytes, so no raw NUL ever appears), DEL, U+2028, noncharacters, unassigned and private-use code
  points. They are faithfully owned history; anything that renders, logs or compares them (154's SQL mirrors, D9
  projections) must treat them as opaque data.
- **N-5 (note, evidence)** `history-fixture-provenance.json` still says 1,623 cases; the 1,624th is explained only in
  `followup-r2.json`. The retained r1 survivor and the added RCO-INDETERMINATE row are honest and I confirm the row
  (owner mutant killed on r2); a reader needs both files to reconstruct the corpus.
- **Disclosed, my own mutants that prove nothing:** digest over the re-encoded document (equal to `raw` behind the
  `NonCanonical` gate) and alias falling back to `token` (GRANT always has both) are equivalent.

No behavioural defect found.

## 4. Bounded verdict
**152: reviewed, no blocking finding and no behavioural defect. The decoder equals the actual frozen v8 schema
structurally (kinds, closed required sets, enums, bounds) and behaviourally on 4,512 independent cases judged by a
third-party validator plus the pinned canonicalizer, and on the owner's 1,624 rows re-judged the same way — 0
disagreements; it owns exactly the canonical input bytes and the journal.1 domain-framed digest; records cannot be
forged, edited, cloned or converted into current records (10/10). T-1: `recordSchema: 3`, `recordType: "SEAL"` and a
lower-case `z` are refused today but no owner row pins them — three rows close it.** Not approval of SQL reading,
mirrors, population, origin, chain diagnostics, custody, selection or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `owner/`,
`probes/{oracle.py,gen_cases.py,rust_probe.rs.txt,rust_probe2.rs.txt,compare.py,table_vs_schema.py,compile_boundaries.py,compile-boundaries.json/.log,compile-*.stderr,mutation.py,mutation.json,mutation.log}`,
`io/{cases.ndjson,rust.ndjson,compare.txt,compare.json,terminal-agreement.txt,table-vs-schema.txt,table-vs-schema-FAILED-r1.txt}`
(the FAILED file is my extractor's bracket slip, preserved), `hashes.txt`.
