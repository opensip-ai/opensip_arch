# Source37 carrier owner correction: A37-01 to A37-04

**Standing.** This is a bounded coauthor owner correction by an actual Claude session. It is not acceptance, not independent review, and not implementation or durability qualification.

- **Scope of writes.** Everything lives in this new runtime. Frozen and live historical bytes were only read.
- **Not done:** edits to source-pins ledgers or generated planning outputs; freeze, activation, commit or push; product code.
- **Recovery cases.** All 54 product recovery cases (F00–F53) remain **not-executed**.

**Source.** `candidate-subject.v37`, manifest SHA-256 `245ef613…91676680`.
- Verified in p00: 29 read, edited or run files agree with their exact manifest pins.
- p04 re-verified frozen and baseline bytes after all work.

## Owner law checked before any route was chosen

- **S12 rows (security-and-lifecycle.md:1300–1308):**
  - `MIGRATION.CORRUPT` → operational-failed/4/`LEDGER.CORRUPT`.
  - Read-only stable quarantine → `LEDGER.CORRUPT`/`ledger-corrupt` with `domainDetail` omitted.
  - Read-only unreadable, unobserved or unreachable anchor → `HOST.IO_FAILURE`/`host-io`.
  - Read-only foreign carrier or swapped store/namespace → request-rejected/2/`EXTENSION.ADMISSION_REJECTED` (`RECOVERY.REFUSED`).
  - `MIGRATION.CORRUPT` is not reused for ordinary journal corruption.
- **Security model D9 map:** `MIGRATION.CORRUPT` and `RECOVERY.REFUSED` carry exactly those triples.
- **Frozen v8 `reconcile_witness`:** a witness naming another project key returns QUARANTINE, *witness names another carrier*.
- **Read-only v3:** §1 standings; §3 routes a foreign witness to `unknown-quarantine-condition`; Step 4 requires stable observations before any quarantine report.
- **D9 v1.14:** codeMaps `ledger-corrupt↔LEDGER.CORRUPT`, `host-io↔HOST.IO_FAILURE`, `ledger-busy↔LEDGER.BUSY_TIMEOUT`, and `EXTENSION.ADMISSION_REJECTED` is a rejection code. nonAnalysisDerivation rule 5 makes datastore failures operational-failed.
- **carrier-migration §4:** a lawful `{A}` or `{A, B}` prefix is busy/unavailable on read-only, never corruption.

## Dispositions

### A37-01: CORRECTED in the owner DDL
- **Change.** Every hex-bearing carrierFormat 3 column now checks lowercase hex over its whole hex part: prefix `GLOB`, exact length, then `substr(col, prefix+1) NOT GLOB '*[^0-9a-f]*'`.
  - `carrier_format.project_key_digest`, `migration_op_ref`;
  - `grant_journal_v3.operation_ref`, `run_id`, `manifest_digest`, `body_sha256`, `prev_sha256`.
  - The planned private `attempt_custody` DDL applies the same law to `store_generation_digest`, `execution_id` and `operation_ref`.
- **Authority.** Host record admission still owns the record bodies; the DDL is defence in depth.
- **Historical scope.** carrierFormat 1 and 2 bytes stay frozen and still check only the first character, which p01b records.
  - This is disclosed, not repaired: historical rows are read only as history, never pass the schema-3 gate, and can never satisfy a schema-3 SEAL join (F46).
  - The earlier proposed v3 and attempt-custody bytes were never instantiated and are superseded in place.

### A37-02: CORRECTED in the DDL and the protocol
- **DDL.**
  - `gj3_append_laws` refuses every append while no `carrier_format` row exists.
  - A CHECK couples `first_generation` to `migrated_from`: exactly 1 on the fresh path, at least 2 when migrated.
- **Act C (fresh, or resuming `{A, B}`).** It verifies three things in the publishing transaction and publishes nothing if any fails:
  - the seven definitions;
  - an empty `grant_journal_v3`;
  - a surviving witness that names the admitted project digest.
- **Published carriers.** A new row-level check (3a) refuses any `grant_journal_v3` row below `first_generation`.
- The seven object names are unchanged.
- **Why both of the review's options.** The DDL prevents the append on a lawful footprint; the publication and row checks verify rows that did not come through that law.

### A37-03: CORRECTED with phase-specific routes
A published `project_key_digest`, or a witness, that names another project is a **carrier project binding mismatch**, not migration corruption. The migration footprint itself is intact, the frozen v8 law already calls this a carrier quarantine, and S12 keeps one remedy per code.

| Phase | Observation | Route |
|---|---|---|
| writer or maintenance open; act C publication | carrier's own binding names another project | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt`, `domainDetail` omitted; nothing appended or published |
| writer or maintenance open; act C publication | partial objects, invalid definitions, v3 rows before publication, violated published boundary (incl. F51) | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt`, detail `MIGRATION.CORRUPT` |
| read-only recovery | association's `journalCarrierDigest`, `storeGenerationDigest` or `namespaceId` differs from the admitted binding | `binding-unusable`: request-rejected / 2 / `EXTENSION.ADMISSION_REJECTED`, `RECOVERY.REFUSED` (existing S12 row) |
| read-only recovery | association names the admitted carrier, but the carrier's own binding names another project, or the footprint is unlawful, or F51 | `unknown-quarantine-condition`: `LEDGER.CORRUPT` / `ledger-corrupt`, omitted; requires Step 4, otherwise `unavailable-busy` |

`MIGRATION.CORRUPT` is used on **no** read-only path.

### A37-04: CORRECTED, routes assigned
- **F46 `unknown-carrier-incompatible`:** operational-failed / 4 / `HOST.IO_FAILURE` / `host-io`, `domainDetail` omitted. It is never not-committed and never a confirmation.
  - An association is written only with a committed carrierFormat 3 SEAL, so one naming a historical generation contradicts two retained owners. That places it in the `unknown-custody` family.
  - It is not a caller defect and not a stable quarantine.
  - The comparison uses `first_generation` read in the same journal snapshot.
- **F51 `split-brain-custody-condition`:**
  - At a writer or maintenance open, `MIGRATION.CORRUPT` (the existing post-detection boundary check).
  - On read-only recovery, the quarantine-condition row under Step 4, otherwise `unavailable-busy`.
  - It is re-detected at every open, writes nothing, and never merges rows.
- **Where recorded:** new S12 rows, the read-only §1 row and paragraph, carrier-format §8.1, and dispatch `publicProjectionByPhase`.
- **Unchanged:** the plan case records in `commit-recovery-plan.v1.json` and `carrier-fault-cases.v1.json` keep their standings, so the generated failure matrix does not change.

### Other advisories
- **A37-05 and A37-06:** not owned (root, query). No edit.
- **A37-07:** owned wording corrected; build-plan lines routed to root.
  - Current-standing notes were added to carrier-format.v3.md, commit-recovery-readonly.v3.md and carrier-migration.v1.md; the Source25 baseline is not relabelled.
  - store-instance-lineage.v1.json gained a note that the current plan holds F00–F53.
  - The build-plan lines 10, 19, 1041, 1045 and 1085 are root's.
- **A37-08:** not owned (native registered-schema successor). No edit.
- **S37-01/02/03:** not owned. No edit.
- **Termination R1/R2:** not extended.
  - Every carrier route validates under both the current and the R1/R2 StepTermination (p05).
  - The new request-rejected code check covers only the carrier `binding-unusable` route and asserts no global rejection-code partition. The `finding.show` HOST.IO_FAILURE exit-2 route is untouched.

## Interrupted migration, recovery and authority
- **No cached state.** Every predicate is re-read from the bytes of that open or that journal snapshot. No cached verdict, `first_generation`, `projectKeyDigest` or earlier successful open is ever reused.
- **Refusals write nothing.** Writer and maintenance refusals append, publish and mark nothing; `carrier_quarantine.reason` keeps its inherited enum.
- **Interrupted prefixes stay resumable.** A lawful `{A}` or `{A, B}` prefix remains a resumable migration: the reader reports busy, and a fresh admitted attempt resumes at C under its own lease.
- **No authority granted.** No route confirms, negates or settles an attempt, merges split-brain rows, rewrites the immutable format row, or grants authority.

## Exact edits
`proposed-edits.diff` (SHA-256 `806c785e04c61fa2fcc8b47939319d25109d9e648f25ce65a176d67090af6758`, 1097 lines) covers 9 files.

| File | before | after |
|---|---|---|
| security/grant-journal.carrier.v3.sql | `23902324…` | `f0a22382…` |
| security/carrier-format.v3.md | `04e6271d…` | `0095e61a…` |
| security/carrier-migration.v1.md | `0295d5e0…` | `446c73dc…` |
| security/carrier-dispatch.v3.json | `0603be7f…` | `55d5597d…` |
| security/check-carrier-v3.py | `137f5cb7…` | `37f370b0…` |
| architecture/attempt-custody.schema.v1.json | `37f1445c…` | `eb1e8755…` |
| architecture/commit-recovery-readonly.v3.md | `a60b048c…` | `3b32d24a…` |
| architecture/store-instance-lineage.v1.json | `2ff48b40…` | `919d1717…` |
| contracts/product-v1/security-and-lifecycle.md | `42bafae6…` | `9ca85de1…` |

Full hashes are in `review.json` and `receipts/p02-apply-edits.json`.

## Controls and receipts
- **p01 / p01b, the review's carrier probe replayed.**
  - Baseline reproduces the review exactly: every non-hex tail ADMITs, and a generation-1 append before publication is published below `first_generation`.
  - Edited: every grammar violation and every pre-publication append refuses. The review's exact format row (first_generation 5 with no migration fields) is itself refused, by design.
  - p01's crash on the edited copy (it did not catch a refused format row) is **preserved**; p01b replaces it.
- **p03, owner validator `check-integrated-carrier.v1.py`.** Baseline 87/0; edited **201/0**, with 114 new source37 controls:
  - SQLite admission for every hex column;
  - the publication and `first_generation` law;
  - an executable open dispatch over real carrier states: interrupted fresh `{B}` and migrated `{A, B}`, act C resume, foreign witness, foreign published digest, association mismatch, F46, F51 re-detected after a clean open, partial or invalid definitions, and rows below first;
  - every projection checked against the selected StepTermination schema, D9 codeMaps, the security model map, S12 rows and the read-only §1 table.
- **p05.** All nine routes are admitted by both the current and the R1/R2 StepTermination schemas and are D9-legal.
- **p06, discrimination.** The edited validator was run over hybrid trees:
  - with the baseline DDL restored, **25** source37 failures;
  - with the baseline S12 and read-only table restored, **5** route-row failures;
  - no pre-existing check failed in either.
- **p04, drift for root.** Frozen and baseline bytes are unchanged, and no other file in the edited tree differs.

## Report to root: bindings that drift until rebind
Computed by p04, not executed:
- **Candidate37 manifest pins:** all 9 files.
- **implementation-normative-inputs.v5:** 8 files (all but check-carrier-v3.py).
- **implementation-coverage sources:** 8.
- **Planning contractSections:** `security-and-lifecycle:12` value and selector drift; `:13`–`:16` selector drift only (line shift).
- **Source-pins ledgers:** foundation evaluator3/foundation/native/security/workflows, all 9 files in each.
- **Expected checker failures until rebind:** reference-group pin checks, the planning checker and package verification.
- **Unchanged:** the generated commit-recovery section and its inputs.

## Limits
- **Reference only.** In-memory SQLite plus a reference dispatch; no OS durability, crash, lock, process or on-disk behaviour. F00–F53 remain not-executed.
- **Witness and stability not simulated.** Witness digests are supplied as parameters, and the Step 4 stability rule is asserted as data law without simulating bracket timing.
- **Act B atomicity not re-exercised.** Rows before publication or below first were injected by lifting and reinstalling the append trigger with byte-identical text (disclosed harness).
- **Historical measurements.** C1–C18 were not rerun, and their evidence is not in the repository.
- **Suites not run.** Reference groups, pin verification, the planning checker and package verification were not run.
- **Discrimination gaps.**
  - p06 does not test the widened wording inside the two existing S12 rows; their class, exit and code are unchanged.
  - Some hybrid-ddl scenario failures cascade from the admitted append.
- **Whole-carrier swap.** A swap that carries a consistent foreign witness and floor stays in the already-disclosed undetected whole-root substitution class.
- **No new marker.** No durable quarantine marker was added, so refusals are re-detected at each open.
- **identity-and-evidence.md** was not edited; it has no route rows and does not contradict these routes.
- **F46 → HOST.IO_FAILURE** is a reasoned selection among existing rows; root owns whether to adopt it.
- **Not acceptance.** An independent review of the corrected bytes is still required.

All subprocesses ran in the foreground and have completed; no background process was started.
