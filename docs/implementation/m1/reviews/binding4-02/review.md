# Independent review: binding4 correction candidate02 and architecture source preflight

**Verdict: ACCEPT-UNIT.** There are no required findings.

- **Subject manifest SHA-256:** `e8043832dc9193e049726ceb1140467752a7fc7898516dc26b7e0d688a1cc59a`. It was checked before and after the review.
- **Scope:** only the four subject files. This review does not cover product integration or qualification, and it does not accept the adapter, closure or drift checks. It approves no new contract or inventory unit.

## What was verified

**Subject integrity**
- The manifest hash and all 4 file hashes and byte counts match both before and after the review.
- The subject was copied to `subject-copy/` before any output. `diff -r` shows the copy identical to the subject at the end.
- Neither tree contains bytecode.

**Change against accepted candidate01**
- The lock is byte-identical.
- The test diff removes no lines: 38 original tests plus 12 binding-history and 6 source-binding tests, 56 in total.
- The verifier changes add only the following:
  - a guard on the candidate path
  - the v4 JSON-content guard on line selectors
  - a comment documenting the sort order
  - `generation_sources`
  - the `--implementation` dispatch
- The live product files equal candidate01.

**Tests and real runs**
- **Tests:** 56 of 56 pass (Python 3.14.6).
- **Real CLI with `--implementation` against adapter subject-03 and the real architecture checkout:**
  - It exits 0 with `passed=true` and 46 inputs.
  - It verifies 28 sources: 5 lock inputs, 3 metadata-v2 candidates and 20 other accepted-overlay rows.
  - `executedGeneratorCode` and `productQualification` are both false.
  - The output equals the root `source-preflight.json`.
- **Root real-mirror probes, re-run here:** 14 of 14 met. R13, the line/pointer alias on real inventory3, now refuses.

**Independent v4 probes: 42 of 42 met**

These covered:
- **Old semantics:**
  - v2 and v3 verify, and a v3 JSON line selector still passes.
  - The same selector in v4 refuses.
  - Line selectors on text documents in v4 still pass.
- **Three-hop inheritance:**
  - Base projects to final index 3.
  - A stale index, an intermediate-parent entry, an extra-key entry and a null entry all refuse.
  - Identical ancestor meanings collapse into one entry.
  - Conflicting ancestors refuse.
  - A conflicting direct override refuses; an identical one suppresses the entry.
  - Order is lexicographic across 12 rows.
- **Aliases:**
  - JSON is detected by content, not by suffix, in both directions.
  - Line selectors on JSON contract members refuse.
  - Duplicate-key and BOM edge cases behave consistently.
  - Pointer aliases using leading zeros or escapes refuse.
  - Mixed selectors refuse.
- **Reuse:** candidate and overlay paths, earlier unit records, forward parents, branches and cycles.
- **Malformed data:** controlled errors for chain entries, candidate paths and version 4.0.

**Independent source-preflight probes: 35 of 35 met**

Refusals:
- **Repin attempts:** a local full repin of an accepted path whose bytes changed; bytes changed on disk.
- **Wrong sources:**
  - an unaccepted trial schema on disk
  - a superseded source-manifest row
  - the metadata-v1 previous candidate
- **Local copy and symlinks:** a copy differing by one byte; a file symlink; a directory symlink escaping the root; a symlinked map.
- **Map and registry agreement:**
  - coverage on either side
  - a duplicate registry path
  - owner mismatch
  - an open top-level map key
  - schemaVersion `true` or `1.0`
  - an uppercase digest
  - an `$id` change made in both map and registry
- **Other:** a missing root, and an invalid design, which is reported before the implementation.

Also verified:
- The accepted v3 adapter lock verifies 28 sources.
- The v2 derivation refuses envelope4.
- CLI exit codes are 0 and 1.
- The watched architecture and adapter files are unchanged.

**Mutation testing: 43 mutants (24 prior, 19 new)**
- The 56 tests kill 35. Prior mutants: 22 of 24 killed, which confirms the claim; M08 and M22 are equivalent.
- Tests and probes together kill every non-equivalent mutant.

## Advisories (non-blocking)

- **B4R2-A01: the preflight accepts any row in the accepted overlay, not only lock inputs.**
  - It binds bytes, not the meaning after passage overrides.
  - It verifies an unrelated accepted schema (S19).
  - It verifies the base inventory v1 JSON (S18), a passage-override parent with no `$id`, when both sides omit `schemaId`.
  - Real data is not affected: every real row has an ID, and none is an override parent.
  - Consider requiring IDs, refusing override parents, or narrowing sources to lock inputs plus contract candidates.
- **B4R2-A02: owner, major and profile are only checked for local consistency between map and registry (S15).**
  - Rows are open (S17).
  - Duplicate mappings of one architecture source are allowed (S20).
  - Paths are not confined to `schemas/` (S21).
  - These belong to the separate adapter checks.
- **B4R2-A03: the tests miss six mutants, all killed by the probes.**
  - N05: the join ignores the digest. This matters because the architecture working tree has uncommitted changes.
  - N09: owner fields are not compared.
  - N14: duplicate registry paths are allowed.
  - N15: contract candidates are not selected.
  - N16: the map is not closed.
  - N19: the v3 contract unit is ignored.
- **B4R2-A04: JSON detection edge cases.** A JSON file with duplicate keys counts as text, so line selectors are allowed. This creates no alias, because no pointer can address that file. Document it.
- **B4R2-A05: uncontrolled exception types.**
  - A non-JSON source raises `JSONDecodeError` (S22).
  - An override parent path given as a list raises `TypeError` (V39, carried CB-A06).
  - The CLI still exits 1.
- **B4R2-A06: the implementation root's own lock and verifier are not checked.** Adapter-03 carries the older v3 lock and verifier, and it still verifies (S33). This matches the stated trust model: the caller starts from the reviewed checkout.
- **B4R2-A07: status of the review01 advisories.**
  - Resolved: B4-A01, B4-A02 (for v4), B4-A03, and the candidate-path half of B4-A04.
  - Still apply: B4-A05 and the carried CB-A02, CB-A04, CB-A05 and CB-A06.
  - The review01 probe re-run gives 43 of 46. The three differences (C12, C25, C27) are exactly the intended stricter refusals.

## Limits

- This is a developer preflight only. It is not an execution guard or attestation, and it does not accept adapter, closure, options or output content.
- The base approvals, inventory3, metadata-v2 and the substance of the schemas were not reaudited. Non-empty multi-hop inheritance was exercised only synthetically or on mirrors.
- The architecture working tree has uncommitted changes. Verification relies on exact pins, and no git write commands were run.
- The unchanged v1–v3 guards were not re-mutated.
- **Artifacts:**
  - the copy and hash records: `subject-copy/`, `before-hashes.txt`, `after-hashes.txt`
  - run outputs and re-runs: `out/`, `prior/`, `root-rerun/`
  - the probe and mutation scripts: `probe_v4.py`, `probe_sources.py`, `mutate.py`
  - the result JSON files
