# Source37 carrier owner correction: v2 (exact storage class and whole-value grammar)

**Standing.** This is a bounded coauthor continuation of the completed v1 nine-file proposal. It is not acceptance, not independent review, and not product durability qualification.

- **What this report does.** It **supersedes the v1 report** only where stated below. The v1 runtime, report and bytes are retained unaltered.
- **Scope of writes.** Everything is in this new runtime. Frozen37 and live history were only read.
- **Not done:** pins, generated planning outputs, global suites, product code, commit or push, freeze or activation.
- **Recovery cases.** All 54 product recovery cases (F00–F53) remain **not-executed**.

**Inputs verified (p00).**
- Frozen37 manifest SHA-256 `245ef613…91676680`; the nine files match their exact manifest pins and the v1 after-hashes.
- Root's captured DDL is byte-identical to the v1 final DDL (`f0a22382…`).
- `work/v1final` and `work/edited` equal the whole v1 edited tree (1355 files; manifest `6fb445f4…`).

## Finding: root's counterexamples are real, and the gap was wider

The SQLite semantics behind them, observed on 3.50.4:
- `length()` stops at an embedded NUL: 64 hex characters plus NUL and Z measure 64, but 66 bytes.
- `GLOB` sees only the part before the NUL.
- An ASCII-hex BLOB keeps storage class `blob`, has length 64, and passes `NOT GLOB`.
- CHECK constraints see values **after** column affinity.

An exhaustive matrix (p01d) covered 28 columns and 341 variants. Its rule: an admitted row must store the lawful storage class and whole-value grammar, and every lawful value must be admitted.

| Tree | Holes | Over-refusals | Root counterexamples | UTF-16 database |
|---|---|---|---|---|
| frozen37 | 105 | 0 | admitted | admits |
| v1 final | 49 | 0 | admitted | admits |
| **v2** | **0** | **0** | **refused** | **fails closed** |

The 49 v1 holes break down as:
- **All 10 hex columns, not only the three root named:** NUL suffix, NUL+Z suffix, NUL followed by invalid UTF-8, and ASCII-hex BLOB.
- **BLOBs in the free TEXT columns:** `request_ref`, `token`, `install_generation_id`, `body`, `namespace_id`.
- **A non-integral REAL** (2.5, also given as text `'2.5'`) in `first_generation` (migrated path) and `grantGeneration`.

The enumerated TEXT columns and the other INTEGER columns were already exact.

These are DDL admission counterexamples, not a demonstrated product exploit; host record admission remains separate.

## Remedy (owner DDL and planned private DDL)

- **Storage class.** Every carrierFormat 3 and `attempt_custody` column states its storage class with `typeof()`.
  - `integer`: `singleton`, `carrier_format`, `first_generation`, `chain_law`, `migrated_from`, `grantGeneration`, `seq`, `record_schema` (both DDLs).
  - `text`: `request_ref`, `token`, `install_generation_id`, `body`, `namespace_id`, and every hex column.
- **Hex columns** (`project_key_digest`, `migration_op_ref`, `grant_journal_v3.operation_ref`, `run_id`, `manifest_digest`, `body_sha256`, `prev_sha256`, `store_generation_digest`, `execution_id`, `attempt_custody.operation_ref`):
  `typeof(c)='text' AND length(c)=N AND length(CAST(c AS BLOB))=N AND <prefix GLOB> AND substr(c, prefix+1) NOT GLOB '*[^0-9a-f]*'`.
  - Character length stops at NUL; byte length counts every byte. They agree only for a NUL-free ASCII value, so GLOB then sees the whole value.
- **Enumerated columns** (`record_type`, `platform`, `phase`, `settled_outcome`) are unchanged: whole-value comparison never equals a BLOB or a NUL-suffixed text, and the matrix confirms it.
- **No lawful row is refused**, because CHECKs see post-affinity values (0 over-refusals). Triggers, keys, the seven object names and the dispatch are unchanged.
- **Encoding.** Byte lengths assume the database text encoding UTF-8, the SQLite default fixed at creation. A UTF-16 database refuses every hex-bearing row: it fails closed.
- **Rejected alternatives.**
  - *STRICT tables* don't catch an embedded NUL. SQLite also documents that pre-3.37.0 libraries cannot read a database containing a STRICT table, which would contradict the staging in which a format-unaware core still reads history.
  - *A NUL-only `instr` test* misses a multibyte value with the same character count.
- **Historical scope.** carrierFormat 1 and 2 bytes stay frozen and still admit first-character-only, embedded-NUL and BLOB `operation_ref` values (observed). This is disclosed, not repaired: history is never re-admitted through the schema-3 gate and can never satisfy a SEAL join (F46).

## Superseded v1 claims (wording corrected in the source)

1. **"Never instantiated / no instance or table was ever created from earlier bytes."** This appeared in the v1 DDL comment, carrier-format §5.1, dispatch `ddlGrammar.historicalScope` and the attempt-custody note. It is inaccurate: earlier design checks and review probes did create reference in-memory SQLite instances.
   - It is now scoped to product: *no product implementation or deployed carrier or ledger table was created from the earlier bytes*.
   - Reference instances and their receipts remain historical evidence.
   - Because the open dispatch validates definitions byte-exactly, a carrier created from earlier bytes is refused `MIGRATION.CORRUPT`.
2. **"The whole-tail `NOT GLOB` grammar is exact."** This appeared in the v1 DDL comment, carrier-format §§5, 5.1 and 6, dispatch `ddlGrammar.law` and `authority`, and the v1 review's A37-01. It is incomplete because of the NUL and BLOB admissions.
   - Carrier-format §5.1 now carries a **revision history** of this law.
- p05b confirms no stale wording remains in any of the nine files.

The v1 route, publication-law and drift findings stand.

## Routes: kept

No contradiction emerged.
- Only dispatch `ddlGrammar` changed.
- S12, the read-only v3 doc, carrier-migration, store lineage and `publicProjectionByPhase` are byte-equal to v1.
- All nine routes are admitted by the selected StepTermination (`4a6e5775…`) and the retained R1/R2 schema (`36124787…`), and are D9-legal (p05b).

## Files: frozen37 → v1 → v2

| File | frozen37 | v1 | v2 |
|---|---|---|---|
| security/grant-journal.carrier.v3.sql | `23902324…` | `f0a22382…` | **`dc94f97e…`** |
| security/carrier-format.v3.md | `04e6271d…` | `0095e61a…` | **`33415107…`** |
| security/carrier-migration.v1.md | `0295d5e0…` | `446c73dc…` | `446c73dc…` (unchanged) |
| security/carrier-dispatch.v3.json | `0603be7f…` | `55d5597d…` | **`ea9cf5d1…`** |
| security/check-carrier-v3.py | `137f5cb7…` | `37f370b0…` | **`c1bd6259…`** |
| architecture/attempt-custody.schema.v1.json | `37f1445c…` | `eb1e8755…` | **`b6e5995a…`** |
| architecture/commit-recovery-readonly.v3.md | `a60b048c…` | `3b32d24a…` | `3b32d24a…` (unchanged) |
| architecture/store-instance-lineage.v1.json | `2ff48b40…` | `919d1717…` | `919d1717…` (unchanged) |
| contracts/product-v1/security-and-lifecycle.md | `42bafae6…` | `9ca85de1…` | `9ca85de1…` (unchanged) |

Full hashes are in `review.json`.
- **Complete nine-file diff, frozen37 → v2:** `proposed-edits.diff` (`21654ca7…`, 1360 lines).
- **v1 → v2 diff:** `v1-to-v2.diff` (`b7c628d1…`, 556 lines).
- The intermediate p02 diffs are kept in `receipts/`.

## Focused results

- **Owner `check-integrated-carrier.v1.py`:** v1 final 201/0; **v2 final 247/0**, with 160 source37 checks of which 62 are storage checks.
- **New storage controls in `check-carrier-v3.py`:**
  - per column, canonical lawful values are admitted in their exact storage class, and no hostile value (NUL, BLOB, REAL, invalid UTF-8, multibyte, prefix, length) is stored outside the law;
  - root's five counterexamples are refused;
  - a structural check that every column states its storage class and every hex column both lengths;
  - lawful admission under UTF-8 and fail-closed under UTF-16;
  - the dispatch law is present;
  - the disclosed carrierFormat 2 history.
- **Checker fix.** The invalid-definition scenario's mutation now anchors on text present in every DDL revision.
- **Discrimination (p04b), the v2 validator over hybrid trees; all expectations met:**
  - v2 tree with the **v1 DDL** restored: 226/21, and **only** storage controls fail;
  - v2 tree with the **frozen37 DDL** restored: 211/36 — storage, publication and scenario controls fail;
  - v2 tree with the **frozen37 S12 and read-only table** restored: 242/5 — only route-row controls fail.
- **p05b (routes, wording, drift):** all OK.
- **Custody:** frozen37, the v1 runtime and the v1-final copy are unchanged; only 5 files differ from v1; no extra files.

## Preserved failures

- **p01 on frozen37:** crashed decoding an admitted invalid-UTF-8 value. Replaced by byte-safe p01b.
- **p01b on edited, strict:** the corrected DDL refuses the UTF-16 setup row (intended), which p01b did not catch. Replaced by p01c.
- **p01c ×3:** the spec-reuse namespace lacked `re`. Replaced by p01d.
- **p04:** the mutation anchor existed only in the v2 DDL, causing 2 non-storage failures in the v1-DDL hybrid. Fixed in the checker by p02b; p04b meets every expectation.

## Report to root

- **Changed files.** Vs frozen37: the same 9 as v1. Vs v1: DDL, carrier-format, dispatch, checker, attempt-custody.
- **Bindings awaiting root rebind.** Unchanged from v1:
  - manifest pins: 9;
  - normative-inputs v5: 8;
  - coverage sources: 8;
  - 5 pin ledgers, each listing all 9.
  - v2 adds no planning section drift beyond v1's, because it does not touch security-and-lifecycle.md.
- **Unchanged:** generated planning inputs, pin ledgers and the v2 carrier DDL of the frozen corpus.

## Limits

- **Reference only.** In-memory SQLite only; F00–F53 not executed.
- **STRICT readability** rests on SQLite documentation. The NUL result alone is measured and sufficient.
- **UTF-16 inherited carriers.** An inherited carrier created UTF-16 (none known) could not publish carrierFormat 3 without a reviewed successor. It fails closed.
- **`namespace_id` length** counts characters before any NUL; the record's own maxLength governs. NUL-containing free text is admitted as TEXT, and host admission owns that content.
- **Enumerated columns** rely on whole-value comparison; they were exercised but not given explicit `typeof` guards.
- **The oracle** is this author's transcription of the owner patterns.
- **Some hybrid-frozenddl scenario failures cascade** from the admitted pre-publication append.
- **No suites run.** No reference groups, pin verification, planning checker or package verification; drift is computed.
- **Not acceptance.** Root integration awaits substantive assessment and independent review.

All subprocesses ran in the foreground and have completed.
