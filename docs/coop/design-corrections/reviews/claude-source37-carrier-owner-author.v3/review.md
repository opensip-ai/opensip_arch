# Source37 carrier owner correction: v3 (encoding-independent exact TEXT grammar)

**Standing.** This is a bounded coauthor continuation of the completed v2 proposal. It is not acceptance, not independent review, and not product durability qualification.

- **What this report does.** It **supersedes the v2 report** only where stated. v1, v2, frozen37 and live history are preserved exactly.
- **Scope of writes.** Everything is in this new runtime.
- **Not done:** root source edits, pins, planning, global suites, product code, commit or push, freeze or activation.
- **Recovery cases.** All 54 product recovery cases (F00–F53) remain **not-executed**.

**Inputs verified (p00).**
- Frozen37 manifest `245ef613…`; the nine files match their exact pins and the v2 hashes.
- Root's captured `captured-carrier.sql` and `captured-attempt.json` are byte-identical to my final v2 DDL (`dc94f97e…`) and attempt-custody schema (`b6e5995a…`).
- The v2 tree is copied exactly (1355 files).

## Assessment

**Root is right.** The v2 bytes admit no hostile value in any encoding. But they refuse every lawful `carrier_format`, `grant_journal_v3` and `attempt_custody` row in UTF-16le and UTF-16be databases (42 over-refusals in each). No owner requires an encoding, so the v2 UTF-8-only restriction was an unforced narrowing, and I withdraw it.

My v2 argument against a NUL guard was wrong. It judged `instr` on its own and ignored the whole-hex guard that stays in the conjunction, which refuses multibyte and malformed characters.

**No counterexample defeats root's conjunction.**

| DDL | UTF-8 | UTF-16le | UTF-16be |
|---|---|---|---|
| frozen37 | 165 holes | 121 holes | 121 holes |
| v2 final | exact | 0 holes, **42 lawful rows refused** | 0 holes, **42 refused** |
| root alternative (derived from v2) | exact | exact | exact |
| **v3** | **exact** | **exact** | **exact** |

"Exact" means 0 holes, 0 over-refusals, and root's counterexamples refused. The matrix (p01) is the byte-safe v2 28-column / 341-variant spec plus 60 (UTF-8) or 50 (UTF-16) encoding-specific hostile rows on the hex columns:
- **UTF-8:** overlong NUL, overlong hex digit, CESU surrogate, lone continuation byte.
- **UTF-16:** lone surrogate, NUL code unit, odd trailing byte.
- **All encodings:** fullwidth and Arabic-Indic digits.

Values are read back as `CAST(... AS BLOB)` and decoded in the observed encoding. Valid affinity conversions, such as integral text into INTEGER stored as integer, are lawful and admitted.

**Every conjunct is necessary** (p01b ablation, all three encodings, four hex shapes). Only the complete conjunction is exact everywhere.

| Candidate | Result |
|---|---|
| complete conjunction (v3 = root) | exact in all three |
| v2 byte length | exact in UTF-8; refuses every lawful value in UTF-16 |
| BLOB instr `instr(CAST(c AS BLOB), x'00')` | exact in UTF-8; refuses every lawful value in UTF-16 |
| TEXT instr with typeof only | admits uppercase, non-hex, whitespace, invalid UTF-8 |
| minus typeof | admits ASCII-hex BLOB |
| minus length | admits short, long and integer values |
| minus instr | admits NUL suffixes |
| minus hex guard | admits uppercase, non-hex and multibyte |
| minus prefix | admits wrong or uppercase prefixes |

## Remedy adopted (root's alternative, exactly)

Each hex column is now:
`typeof(c)='text' AND length(c)=N AND instr(c, char(0))=0 AND <prefix GLOB> AND <hex part> NOT GLOB '*[^0-9a-f]*'`

- **Where applied:** 7 replacements in the carrier DDL and 3 in the private attempt-custody DDL.
- **Equality verified:** the v3 DDL statements equal root's substitution applied to v2 (comment lines excluded), and the attempt-custody DDL equals it exactly. No `AS BLOB` predicate remains (p05b).
- **No encoding requirement.** I removed the v2 UTF-8 assumption, the "fails closed" justification, the dispatch `encodingAssumption` key and the "no lawful row is refused" wording. The dispatch now states `encodingIndependence`.
- **Storage class, stated accurately.** Every column's storage class is enforced by either:
  - an explicit **`typeof()`**: the INTEGER columns (`singleton`, `carrier_format`, `first_generation`, `chain_law`, `migrated_from`, `grantGeneration`, `seq`, both `record_schema`), the free TEXT columns (`request_ref`, `token`, `install_generation_id`, `body`, `namespace_id`) and all 10 hex columns; or
  - **exact enumeration**: `record_type`, `platform`, `phase`, `settled_outcome`, whose IN lists of TEXT literals never equal a BLOB, number or NUL-suffixed text.
- **Kept unchanged:** the v2 storage-class laws, the publication and `first_generation` law, object names, triggers, keys, dispatch, the historical scope (frozen v1/v2 bytes still admit NUL/BLOB/first-character-only, disclosed), and the STRICT rejection.
- **Revision history.** Carrier-format §5.1 now records v1 → v2 → v3, and the historical scope names "including the source37 v1 and v2 revisions".

## Routes: unchanged

No contradiction emerged. Only dispatch `ddlGrammar` changed; S12, the read-only v3 doc, carrier-migration, lineage and `publicProjectionByPhase` are byte-equal to v2. All 9 routes are admitted by the selected StepTermination (`4a6e5775…`) and the retained R1/R2 schema (`36124787…`), and are D9-legal (p05b).

| Phase / standing | Route |
|---|---|
| writer/maintenance open: migration footprint corrupt; F51 split brain | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt`, detail `MIGRATION.CORRUPT` |
| writer/maintenance open and act C: carrier project binding mismatch | same class/code, detail omitted |
| act C: migration footprint corrupt | as the first row |
| read-only: binding-unusable | request-rejected / 2 / `EXTENSION.ADMISSION_REJECTED`, `RECOVERY.REFUSED` |
| read-only: unknown-quarantine-condition | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt`, omitted |
| read-only: unknown-carrier-incompatible (F46) | operational-failed / 4 / `HOST.IO_FAILURE` / `host-io`, omitted |
| read-only: unavailable-busy | operational-failed / 4 / `LEDGER.BUSY_TIMEOUT` / `ledger-busy`, `PROJECT.BUSY` |

## Files: frozen37 → v2 → v3

| File | frozen37 | v2 | v3 |
|---|---|---|---|
| security/grant-journal.carrier.v3.sql | `23902324…` | `dc94f97e…` | **`b82d63c0…`** |
| security/carrier-format.v3.md | `04e6271d…` | `33415107…` | **`10608c16…`** |
| security/carrier-migration.v1.md | `0295d5e0…` | `446c73dc…` | unchanged |
| security/carrier-dispatch.v3.json | `0603be7f…` | `ea9cf5d1…` | **`62b1958e…`** |
| security/check-carrier-v3.py | `137f5cb7…` | `c1bd6259…` | **`4948301d…`** |
| architecture/attempt-custody.schema.v1.json | `37f1445c…` | `b6e5995a…` | **`60a88154…`** |
| architecture/commit-recovery-readonly.v3.md | `a60b048c…` | `3b32d24a…` | unchanged |
| architecture/store-instance-lineage.v1.json | `2ff48b40…` | `919d1717…` | unchanged |
| contracts/product-v1/security-and-lifecycle.md | `42bafae6…` | `9ca85de1…` | unchanged |

Full hashes are in `review.json`.
- **Complete nine-file diff, frozen37 → v3:** `proposed-edits.diff` (`f7ff95c4…`, 1426 lines).
- **v2 → v3 diff:** `v2-to-v3.diff` (`8495dadb…`, 446 lines).

## Focused results

- **Owner `check-integrated-carrier.v1.py`:**
  - frozen37 87/0;
  - v2 final 247/0;
  - **v3 362/0**, with 275 source37 checks of which 177 are storage checks.
- **New checker controls:**
  - all 28 columns × 3 encodings: lawful values admitted in exact storage class, and no hostile value stored outside the law (including encoding-specific malformed TEXT);
  - root counterexamples refused per encoding;
  - a structural check: typeof or enumeration per column, length and NUL guard per hex column, no byte-length or BLOB predicate;
  - **UTF-16le and UTF-16be carrierFormat 2 carriers migrate, publish, admit a lawful SEAL, and still refuse NUL and BLOB values**;
  - the dispatch states encoding independence.
- **Discrimination (p04), the v3 validator over hybrids; all 12 expectations met:**
  - v2 DDL restored: 301/61. **Only** storage controls fail (UTF-16 lawful admission for every table, the UTF-16 migration scenario, and the byte-length structural check); no UTF-8 failure; publication, scenario and route controls are kept.
  - frozen37 DDL restored: 289/73. Storage (NUL/BLOB in every encoding), publication and scenario controls fail.
  - frozen37 S12 and read-only restored: 357/5. Only route rows fail.
- **p05b:** adoption equality, routes, wording, drift and custody all OK; only 5 files differ from v2.

## Superseded v2 claims

- **UTF-8-only encoding requirement:** byte lengths assumed UTF-8 and the refusal was called fail-closed (DDL, carrier-format §5.1, dispatch `encodingAssumption`, attempt-custody note).
- **"No lawful row is refused":** carrier-format §5.1 and dispatch `storageClassLaw`.
- **"Every column states its storage class with `typeof()`":** now "typeof or exact enumeration".
- **v2 rejected-alternative reasoning on instr:** replaced by the complete-conjunction assessment above.
- **v2 limit that a UTF-16 inherited carrier could not publish carrierFormat 3:** v3 migrates and seals one.

## Preserved failures

- **p05 exited 1.** Its wording scan flagged the checker's own negative control `'encodingAssumption' not in _S37_G` as stale. p05b reruns p05's exact source, classifying only that line; everything else in p05 already passed.
- **Pre-run fix.** Before any execution, a stray tab-indented placeholder loop was removed from the ablation probe; it would have raised `TabError`. No receipt existed for the earlier bytes.

## Report to root

- **Changed files.** Vs frozen37: the same nine. Vs v2: DDL, carrier-format, dispatch, checker, attempt-custody.
- **Bindings awaiting rebind:** unchanged from v1/v2 — manifest pins 9, normative-inputs v5 8, coverage sources 8, and 5 pin ledgers each listing all 9. No new planning section drift.

## Limits

- **Reference only.** In-memory SQLite 3.50.4 under three encodings; F00–F53 not executed.
- **Encoding independence** is observed for `length()`, `instr()`, `substr()`, `GLOB` and `typeof()` on this SQLite version only. Availability of `instr()`/`char()` (3.7.15/3.7.16) is from release history, not measured.
- **UTF-16 migration control** covers one inherited v2 shape per UTF-16 encoding; it is not migration qualification.
- **The oracle** is my transcription of owner patterns, and the hostile set is finite.
- **`namespace_id` length** counts characters before any NUL; NUL-containing free TEXT is admitted as TEXT, and host admission owns that content.
- **Enumerated columns** rely on whole-value comparison; they were exercised but carry no explicit `typeof`.
- **STRICT unreadability** remains documentation-based.
- **No suites run.** No reference groups, pins, planning checker or package verification; drift is computed.
- **Not acceptance.** Root assessment and independent review are required before integration.

All subprocesses ran in the foreground and have completed.
