# Grant-journal physical carrier, carrierFormat 3 (PROPOSED design/reference correction)

**Standing.** Proposed versioned design/reference artifact resolving COV-03 and the carrier
findings CR-04 / CR-07. Authored by a non-blind actual Claude coauthor against frozen Source25
(manifest `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`; all 12869 members
verified this session). No acceptance, readiness, application or implementation authorization,
and no self-acceptance. Design/reference only: a physical DDL, an open/read dispatch and
reference validation. Not product Rust, not executable storage, not a crash-test result, and
not an OS durability claim. No historical or frozen file is modified by this correction.

**Current standing.** The Source25 authoring baseline stated above is historical and is not relabelled. The current bytes carry the source37 owner correction of review advisories A37-01 to A37-04 (`design-corrections/security/carrier-format.v3.md` §8.1). They remain PROPOSED-NOT-SELF-ACCEPTED and are bound only by whichever candidate manifest selects them; no acceptance, readiness or implementation authorization follows.

**Revision note.** This revises the first draft in two places root identified: §2.1 replaces an
overbroad "nothing is writable" claim with the exact two incompatible cases, and §11 separates the
already-known weak-chain limitation from the distinct wording contradiction this session found.
**Selected companions and their stable normative paths.** These are the current owners; earlier
drafts are retained only as historical evidence and are **never** competing current owners:

| Concern | Selected current owner |
|---|---|
| physical carrier format, dispatch, chain | `design-corrections/security/carrier-format.v3.md` (this file) plus `grant-journal.carrier.v3.sql` and `carrier-dispatch.v3.json` |
| carrier-format migration protocol | `design-corrections/security/carrier-migration.v1.md` |
| SC-TRUST per-carrier floor shape | `design-corrections/security/carrier-highwater.schema.v1.json` |
| bounded read-only recovery, gate, sweep | `architecture/commit-recovery-readonly.v3.md` |
| private attempt custody record | `attempt-custody.schema.v1.json` |

`commit-recovery-readonly.v1.md` and `.v2.md` are superseded. They exist only under the retained
evidence trees and must not be linked as current owners anywhere.

**This revision also reconciles selected documents, not only companions.** §8 previously used table
existence for detection and §9 previously claimed a format-unaware core refuses typed; both
contradicted `carrier-migration.v1.md` and are replaced in place. The older drafts of those
sections are preserved in the retained evidence trees.

**Separately owned, not duplicated here.** Two adjacent items are being authored by a different
actual Claude session, and this correction deliberately does **not** restate or re-decide them:

- **PS01** — the random store-instance identity and the S9 private store-generation lineage. This
  document consumes `storeGenerationDigest` and `StoreGenerationBindingV1` as *inputs* only, and
  adds no law about `storeInstanceId` allocation, lineage validation or restore semantics.
- **PS04** — the report release asset anchor. Nothing here touches report assets, the
  `closure2.kind` vocabulary or release-artifact anchoring.

Where this document must mention either, it names the dependency and stops.

## 1. Three axes, never conflated

The inherited corpus overloads the word *schema*. This correction separates three axes and
requires every reader, writer and migration to name the one it means.

| Axis | Values | Meaning |
|---|---|---|
| carrierFormat | 1, 2, 3 | physical table and trigger shape of the project SQLite carrier |
| recordSchema | 1, 2, 3 | logical journal record **body** format |
| stateSchema | 1, 2 | logical **store state** format (`StoreGenerationBindingV1`, S9) |

All three are security-owned. `stateSchema` never selects a record parser, `recordSchema` never
selects a table, and `carrierFormat` is new in this correction.

The two inherited physical shapes are retrospectively numbered so dispatch can name them.

- **carrierFormat 1** — `security-completion.v1.md` §5.4 embedded DDL: no seq range CHECK, no
  contiguity trigger, no TERMINAL-closure trigger, no reserved-slot trigger.
- **carrierFormat 2** — `security-schemas.v2/grant-journal.sql`: adds the uint53 seq CHECK, the
  `operation_ref` format CHECK, `token NOT NULL` on GRANT, and the three append triggers.
  `security-completion.v8.md` §5.4 states that encoding, DDL, sequence rule, uint53 cap with the
  reserved terminal slot and hash chain are *as v2*, so v8 inherits carrierFormat 2 unchanged.
- **carrierFormat 3** — `grant-journal.carrier.v3.sql` in this directory.

## 2. The defect, established by execution (CR-07)

Control C1 applied the frozen carrierFormat 2 DDL to an in-memory SQLite database and attempted
real inserts. Evidence: `scratch/out/c1.json`.

Current schema-3 `SEAL` is **refused** with `CHECK constraint failed` on `record_type`. Set
algebra over the actual frozen artifacts: the only schema-3 record type the physical DDL does not
admit is `SEAL`; the physical types absent from schema 3 are `AUD`, `CHECKPOINT`, `EXPIRY`,
`MIGRATION`, `NARROW` and `TERMINAL`. The recordSchema-1 body set equals the physical CHECK set
exactly, and the schema-3 set equals `LinearizationV1.journalTypes` exactly.

No physical DDL anywhere in Source25 admits `SEAL`: all four carriers of the DDL text (v1
markdown, v2 `.sql`, `security_unit_lib_v2`, `security_unit_lib_v8`) share the identical
14-member set. Meanwhile `TERMINAL`, which the physical carrier *requires* at the reserved slot,
is not a member of the public schema-3 `JournalRecord`.

### 2.1 The incompatibility is specific, not total

An earlier draft of this document said the current logical journal "cannot be written to any
inherited physical carrier at all". That was overbroad and is corrected here. Control C8
enumerated every case by execution (`scratch/out/c8.json`):

- The frozen carrier physically admits **8 of the 9** current schema-3 operational record types:
  `GRANT`, `RA`, `ICI`, `RCI`, `ICO`, `RCO`, `REV`, `CLN` all insert cleanly.
- The incompatible cases are exactly two:
  1. the record type **`SEAL`**, refused by the `record_type` CHECK; and
  2. the three **alias-only** machine platform ids on a `GRANT` — `macos-aarch64`,
     `linux-x86_64-gnu`, `linux-aarch64-gnu` — refused by the `platform` CHECK.
     `macos-x86_64` is admitted, because that value is its own display alias.

So the inherited carrier is not globally unusable; it is unusable for the sealing record and for
three quarters of the platform vocabulary. Those two specific cases, plus the reserved-slot
`TERMINAL` requirement, are what the new format has to resolve.

Loosening an enum is still not an option: loosening the physical `record_type` set to admit `SEAL`
would simultaneously leave `TERMINAL` admissible as a public schema-3 record, and loosening the
`platform` set would re-admit spellings that S8 MUST-2 refuses.

## 3. The platform vocabulary defect (CR-04)

The frozen physical `platform` CHECK enumerates exactly the four S8 **display aliases**
(`macos-arm64`, `macos-x86_64`, `linux-x86_64`, `linux-arm64`). S8 MUST-2 names the four
**machine ids** (`macos-aarch64`, `macos-x86_64`, `linux-x86_64-gnu`, `linux-aarch64-gnu`) as the
only machine identity, and refuses an alias presented as a platform with
`GRANT.PLATFORM_DISPLAY_ALIAS_NOT_MACHINE_ID`.

Executed (C1): a `GRANT` carrying `macos-aarch64` or `linux-x86_64-gnu` is refused by the frozen
CHECK; a `GRANT` carrying the alias `macos-arm64` is admitted. Exactly one value, `macos-x86_64`,
is lawfully shared because it is its own alias. Three physical values are alias-only.

S8 also says "historical documents that use the aliases are unchanged". This correction honours
that: inherited rows keep their alias spellings verbatim and are never relabelled (§7, §9).

## 4. Resolution: carry TERMINAL as its frozen recordSchema-1 body

carrierFormat 3 admits the nine schema-3 operational record types plus `TERMINAL`, and segregates
them with one CHECK:

```sql
CHECK ((record_schema = 3 AND record_type <> 'TERMINAL')
    OR (record_schema = 1 AND record_type = 'TERMINAL'))
```

`TERMINAL` is therefore carried as the **already frozen recordSchema-1 TERMINAL body** defined in
`security-schemas.v2/journal-record.schema.json`, with its existing `cause` enum
(`projectPurge`, `grantGenerationClosure`) and its existing domain `opensip.metadata.journal.1`.
It is never admitted as a schema-3 `JournalRecord`, and schema 3 is not widened.

Consequences, all verified by execution (`scratch/out/c2.json`):

- `TERMINAL` offered as `record_schema` 3 is refused; `TERMINAL` as `record_schema` 1 is admitted.
- An operational type offered as `record_schema` 1 is refused, so schema 1 cannot be used as a
  back door for current records.
- No public schema change: `JournalRecord` schema 3, `JournalRecordV2`, the recordSchema-1 bodies,
  `LinearizationV1.journalTypes`, the receipt and D9 are untouched. No new H-domain and no new
  canonical profile is introduced. No public wire major changes.
- `TERMINAL` rows carry no grant-bearing or platform-bearing members (refused by CHECK).

## 5. Laws preserved by carrierFormat 3

Each was re-executed against the new DDL (C2) and produces the inherited refusal:

- **Append-only.** `UPDATE` and `DELETE` abort with *grant journal is append-only*.
- **Contiguity.** `seq` must equal tail+1 per grant generation.
- **TERMINAL closure.** No append after a `TERMINAL` in that generation.
- **uint53 cap and reserved slot.** `seq` range 1..9007199254740991; slot 9007199254740991
  accepts only `TERMINAL`, so an ordinary `SEAL` uses at most 9007199254740990. This is the
  physical narrowing of the logical schema-3 `seq`, which is `I64Positive`. The narrowing is a
  carrier refusal (F32), not a schema change; `CommitRecoveryAssociationV1.journalSeq` already
  states the same bound with maximum 9007199254740990.
- **operation_ref grammar.** `op-` plus 32 lowercase hex, length 35, as one whole TEXT value: storage
  class, character length, no NUL, prefix and hex tail (§5.1). The frozen carrierFormat 2 bytes check only
  the first character after the prefix, and the source37 v1 revision of this DDL checked the tail but still
  admitted an embedded-NUL suffix or an ASCII-hex BLOB; see §5.1.
- **GRANT completeness.** `install_generation_id`, `manifest_digest`, `platform` and `token` all
  present.
- **Witness and high-water laws.** Unchanged in substance; see §8 and §10.

### 5.1 Exact storage class, whole-value grammar and the publication law (source37 owner correction)

**Storage class and grammar (A37-01, revised).** SQLite types values dynamically: a column's TEXT affinity
keeps a BLOB, INTEGER affinity keeps a non-integral REAL, and `length()` and `GLOB` stop at an embedded NUL.
Every carrierFormat 3 column's storage class is therefore enforced, by one of two mechanisms. An explicit
`typeof()` guard states `integer` for `singleton`, `carrier_format`, `first_generation`, `chain_law`,
`migrated_from`, `grantGeneration`, `seq` and `record_schema`, and `text` for `request_ref`, `token`,
`install_generation_id`, `body` and every hex-bearing column. Exact enumeration enforces it for
`record_type` and `platform`: their `IN` lists hold only TEXT literals, and a whole-value comparison never
equals a BLOB, a number or a NUL-suffixed text. Each hex-bearing column (`carrier_format.project_key_digest`
and `migration_op_ref`, and `grant_journal_v3.operation_ref`, `run_id`, `manifest_digest`, `body_sha256` and
`prev_sha256`) is then an exact whole TEXT value: `typeof(column) = 'text'`, `length(column) = N`, no NUL
anywhere (`instr(column, char(0)) = 0`), the prefix `GLOB` where a prefix exists, and
`NOT GLOB '*[^0-9a-f]*'` over the hex part. With no NUL, `length()` and `GLOB` see the whole value, and the
case-sensitive hex class admits only ASCII `0`–`9` and `a`–`f`, so a multibyte or malformed character is
refused by the same conjunction. Removing any one conjunct admits a hostile value. The conjunction evaluates
the TEXT value by character and does not depend on the database text encoding; it was exercised under
UTF-8, UTF-16le and UTF-16be, and no encoding is required of a carrier. CHECKs see values after column
affinity, so an integer supplied as text `'5'` is stored and checked as integer 5. The private
`attempt_custody` DDL applies the same laws: `typeof()` on `store_generation_digest`, `execution_id`,
`operation_ref`, `namespace_id` and `record_schema`, and exact enumeration on `phase` and `settled_outcome`.
Host record admission still validates the closed record bodies; the DDL is defence in depth.

**Revision history of this law.** The source37 v1 correction replaced a first-character-only `GLOB` with a
whole-tail `NOT GLOB` and described the result as exact. Root then reproduced, against those v1 bytes, an
embedded-NUL suffix being admitted in `body_sha256`, `operation_ref` and `run_id`, and an ASCII-hex BLOB
being admitted in `body_sha256` and `project_key_digest`. The exhaustive storage-class matrix run for this
revision found the same NUL and BLOB admissions in every hex-bearing column, a BLOB in every free TEXT
column, and a non-integral REAL in `first_generation` and `grantGeneration`. These are DDL admission
counterexamples, not a demonstrated product exploit. STRICT tables were not selected: they do not refuse an
embedded NUL, and SQLite documents that a database containing a STRICT table cannot be read by libraries
older than 3.37.0, which would contradict the staging in which a format-unaware core still reads historical
generations (§9).

The source37 v2 revision then paired `length(column) = N` with a byte count,
`length(CAST(column AS BLOB)) = N`, assumed a UTF-8 database and described the refusal of every UTF-16
hex-bearing row as failing closed. Root showed that this refused otherwise lawful rows in UTF-16le and
UTF-16be databases, although no earlier owner requires a text encoding for historical SQLite carriers. This
revision replaces the byte count with `instr(column, char(0)) = 0`; with the retained storage class,
character length, prefix and whole-hex guards it gives the same exact grammar in all three encodings, and
the v2 encoding restriction is withdrawn.

**Historical scope.** carrierFormat 1 and 2 bytes are frozen and unchanged. Their `GLOB` checks inspect only
the first character after a prefix, and they also admit embedded-NUL and BLOB values. That weakness is
disclosed, not repaired: historical rows are read as history under recordSchema-1 semantics, are never
re-admitted through the schema-3 gate and can never satisfy a schema-3 `SEAL` join (§9, F46), so a
malformed historical value confers no commitment. No product implementation or deployed carrier was
created from the earlier PROPOSED carrierFormat 3 bytes, including the source37 v1 and v2 revisions. Reference in-memory SQLite instances were created
from them by earlier design checks and review probes, and those instances and their receipts remain
historical evidence. The open dispatch validates definitions byte-exactly, so a carrier created from
earlier bytes is refused `MIGRATION.CORRUPT` rather than read as this definition.

**Publication law (A37-02).** `gj3_append_laws` refuses every append while no `carrier_format` row
exists, so an `{A, B}` footprint cannot acquire a row that a later publication would contradict. A
`carrier_format` CHECK couples `first_generation` to `migrated_from`: exactly 1 on the fresh path, at
least 2 on the migrated path. Act C verifies, in the same transaction that inserts the row, the seven
definitions, that `grant_journal_v3` holds no row and that a surviving witness names the admitted
`projectKeyDigest`; any failure publishes nothing. Both laws live inside existing definitions, so the
seven object names are unchanged.

## 6. Additions beyond the inherited DDL, and why each is needed

| Addition | Reason |
|---|---|
| `platform` CHECK uses the four S8 machine ids | resolves CR-04; alias-only values refused |
| `record_schema` column plus the segregation CHECK | resolves CR-07 without widening schema 3 |
| `run_id` column, NOT NULL on `SEAL` | binds the SEAL to its replayed `run3` identity in the carrier |
| `carrier_format` singleton table | names carrierFormat, `first_generation` and `chain_law` durably |
| `first_generation` trigger | keeps migrated generations out of the new table |
| superseded-generation trigger | enforces WA-13 generation ordering physically |
| no append before the format row | an `{A, B}` footprint holds no row that publication could contradict (§5.1) |
| `first_generation` coupled to `migrated_from` | the fresh path publishes 1; the migrated path publishes at least 2 (§5.1) |
| whole-value storage-class and hex CHECKs | a value is admitted only in its exact storage class and whole grammar: no embedded NUL, BLOB or non-integral REAL (§5.1) |

The last five are genuinely new laws. None can affect an inherited row: all live only on the new
objects. The inherited DDL permitted appending to an older generation; carrierFormat 3 does
not, which is strictly narrower and matches WA-13.

`run_id` is a physical column, not a new body member: the value is already a member of the closed
schema-3 `JournalRecord` (`^run3:[0-9a-f]{64}$`). The column is a carrier-level projection of a
body member that already exists, so it adds no field to any closed schema.

## 7. Migration 1 or 2 → 3

The migration is expressible **entirely within the frozen DDL rules**. No constraint or trigger is
disabled, and no inherited row is rewritten, relabelled or reinterpreted. Executed in C2:

1. Under the S7 install fence with `EXCLUSIVE` on the affected namespace, append `TERMINAL` with
   cause `grantGenerationClosure` to the existing `grant_journal` at tail+1. The frozen
   constraints accept it; the frozen TERMINAL trigger then refuses every later append to that
   generation. The `TERMINAL` row carries the **migration operation's own** `op-` token, never a
   released analysis operation's ref.
2. Execute `grant-journal.carrier.v3.sql`. It creates `carrier_format`, `grant_journal_v3` and
   their triggers, and uses `CREATE TABLE IF NOT EXISTS` only for the two inherited non-appending
   side tables (`carrier_quarantine`, `carrier_capacity_pause`).
3. Insert the single `carrier_format` row: `carrier_format` 3, the carrier `projectKeyDigest`,
   `first_generation` = (max inherited generation) + 1, `chain_law` 1, `migrated_from` 1 or 2, and
   the migration op ref. The row is immutable by trigger and a second row is refused.
4. New operational appends go to `grant_journal_v3` in `first_generation` onward.

Executed results: inherited rows byte-identical before and after (the only delta is the new
`TERMINAL` row the frozen constraints themselves admitted); inherited schema objects unchanged;
the legacy alias platform value retained verbatim as `macos-arm64`; an attempt to write generation
1 into `grant_journal_v3` is refused as *grant generation precedes the carrierFormat 3 first
generation*.

**On "a second migration aborts because the table already exists".** That observation belongs to
the historical C2 evidence and is **not** the current recovery law. Under the selected algorithm a
second attempt on an already-migrated carrier reads the published row at step 5, concludes
carrierFormat 3, and does nothing; on an incomplete footprint it validates the object set and
resumes at act C. Object existence is a *resume signal*, never the recovery mechanism, and act B is
never re-run blindly to discover a collision.

**carrierFormat 1 caveat.** carrierFormat 1 has no contiguity or TERMINAL trigger, so after its
`TERMINAL` is appended the "no later append" law is not physically enforced by that database. The
open dispatch therefore marks a carrierFormat 1 generation `closed-by-record, not-trigger-enforced`
and the reader treats any row after its `TERMINAL` as a custody condition, never as valid history.

**Normative addition that must be propagated.** WA-13 states that `grantGeneration` advances only
on whole-generation `REV` and on the uint53 rollover. Carrier-format migration is a third cause of
generation closure. It reuses the existing typed cause `grantGenerationClosure` and changes no
schema, no enum and no wire major, but it *is* a normative addition to WA-13 and is listed as such
in §12.

## 8. Open dispatch

carrierFormat 1 has no version row, so detection is by schema introspection only, never by a
version record. **Detection is keyed on the published format ROW, not on table existence.** An
earlier draft of this section used table existence, which contradicted the commit point defined in
`carrier-migration.v1.md` §3 and would have read an incomplete migration footprint as a
carrierFormat 3 carrier. The row-keyed predicate is what makes the `{A, B}` prefix recoverable:

The seven carrierFormat 3 objects are `carrier_format`, `cf_no_update`, `cf_no_delete`,
`grant_journal_v3`, `gj3_no_update`, `gj3_no_delete`, `gj3_append_laws`. **The row is read last,
and only after the object set is proven complete and valid.** An earlier revision of this section
put the row read in the first branch, which contradicted the very next sentence and would have let
a malformed stub reach a row read.

```
1  names := the carrierFormat 3 object NAMES present in sqlite_master   (names only)
2  if no name of the seven is present            -> goto 6   (read no v3 table at all)
3  if some but not all seven names are present   -> MIGRATION.CORRUPT
4  if any stored definition differs from what the selected creation path produces
                                                 -> MIGRATION.CORRUPT
5  read the carrier_format row where singleton = 1
       row present  -> carrierFormat 3
       row absent   -> if grant_journal_v3 holds any row -> MIGRATION.CORRUPT
                       else INCOMPLETE FOOTPRINT: inherited format; a fresh admitted
                       maintenance attempt resumes at act C
6  if table grant_journal exists and trigger gj_seq_contiguous exists -> carrierFormat 2
7  if table grant_journal exists                                      -> carrierFormat 1
8  no journal table at all -> FRESH INSTALL: create carrierFormat 3 directly
```

Step 4 is load-bearing and separate from step 3: a malformed stub can carry **all seven names**
with wrong definitions, so name presence alone is never sufficient. Steps 3 and 4 both precede any
row read, so a malformed object can neither be mistaken for a published format nor crash the
dispatch.

**Step 8, the fresh-install path.** With no inherited journal table and no carrierFormat 3 object,
the carrier is created directly at carrierFormat 3: acts B and C only. Act A does not apply, because
there is no inherited generation to close, and **no absent table is read**. The published row has
`migrated_from` null, `migration_op_ref` null, `first_generation` 1 and `chain_law` 1.

This selected algorithm is exercised in C18 over the fresh-install path, every lawful durable
prefix, a partial object set and an all-names-wrong-definitions shape. The earlier five-case
evidence from C2 tested the superseded table-existence predicate and is **historical evidence
only**, not evidence for this algorithm.

Additional open-time checks, in order, before any read is admitted:

1. The stored SQL text of `carrier_quarantine` and `carrier_capacity_pause` must byte-equal the
   frozen definition. This closes the `CREATE TABLE IF NOT EXISTS` hole: a pre-existing variant
   can never be silently accepted. Verified equal in C2.
2. `carrier_format.project_key_digest` must equal the carrier's own `projectKeyDigest` derived from
   the admitted project key. A mismatch is a **carrier project binding mismatch**, not migration
   corruption: nothing in the migration footprint is inconsistent, but the carrier's own binding names
   another project, the condition the frozen `reconcile_witness` reports as *witness names another
   carrier*. It never borrows `MIGRATION.CORRUPT`; its route is §8.1.
3. `max(grantGeneration)` in `grant_journal` must be strictly less than
   `carrier_format.first_generation`, and no inherited row may follow a `TERMINAL` in its generation;
   otherwise the published generation boundary is violated (the F51 split-brain custody condition)
   and the carrier is `MIGRATION.CORRUPT` at a writer or maintenance open.
3a. `min(grantGeneration)` in `grant_journal_v3`, when any row exists, must be at least
   `carrier_format.first_generation`; otherwise `MIGRATION.CORRUPT`. The corrected DDL already refuses
   such a row; this check verifies rows, not only definitions.
4. Witness reconciliation runs exactly as `security_unit_lib_v8.reconcile_witness` specifies. C1
   reproduced all 14 rows of the v8 §5.4 table against the frozen implementation with no
   deviation. Reconciliation is unchanged by this correction.
5. The SC-TRUST high-water comparison (v8 §5.4 fence handoff) runs as specified and is a separate
   step: the frozen `reconcile_witness` is pure and does **not** consult the high-water
   (verified in C1).

### 8.1 Phase-specific public routes (source37 owner correction)

Every route below is an existing D9 v1.14 class, exit, `errorCode` and `faultCause`; nothing is minted.
The phase decides which existing route applies, never a new class. Machine-readable:
`carrier-dispatch.v3.json#/publicProjectionByPhase`. Security owner rows: S12.

| Phase | Observation | Internal standing | class / exit / errorCode / faultCause | `domainDetail` |
|---|---|---|---|---|
| writer or maintenance open | partial object set; all names with an invalid definition; a `grant_journal_v3` row with no published row; a published boundary violated (checks 3, 3a) | migration footprint not a lawful prefix | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt` | `MIGRATION.CORRUPT` |
| writer or maintenance open | F51: inherited generation at or above `first_generation`, or an inherited row after `TERMINAL` | `split-brain-custody-condition` | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt` | `MIGRATION.CORRUPT` |
| writer or maintenance open | published `project_key_digest` (check 2) or a surviving witness names another project | carrier project binding mismatch | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt` | omitted |
| maintenance act C (fresh or `{A, B}` resume) | a `grant_journal_v3` row, a partial set or invalid definition; or a witness naming another project | as the rows above | as above; **nothing is published** | as above |
| read-only recovery | the association's `storeGenerationDigest`, `namespaceId` or `journalCarrierDigest` differs from the admitted binding | `binding-unusable` | request-rejected / 2 / `EXTENSION.ADMISSION_REJECTED` / — | `RECOVERY.REFUSED`, typed subject |
| read-only recovery | association names the admitted carrier, but the carrier's own row or witness names another project; an unlawful footprint; or F51 | `unknown-quarantine-condition` | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt` | omitted |
| read-only recovery | F46: association names a generation below the `first_generation` read in the same journal snapshot | `unknown-carrier-incompatible` | operational-failed / 4 / `HOST.IO_FAILURE` / `host-io` | omitted |
| read-only recovery | lawful `{A}` or `{A, B}` prefix (`carrier-migration.v1.md` §4), or an unstable observation | `unavailable-busy` | operational-failed / 4 / `LEDGER.BUSY_TIMEOUT` / `ledger-busy` | `PROJECT.BUSY` |

**Why a digest mismatch is not migration corruption.** A partial object set, an invalid definition, a
row before publication and a violated generation boundary are failures of the migration footprint
itself, so `MIGRATION.CORRUPT` names their remedy. A project digest mismatch leaves that footprint
intact: the carrier at this namespace carries another project's binding. The frozen v8 witness law
already treats the same fact as a carrier quarantine, and S12 keeps journal-carrier quarantine free of
`MIGRATION.CORRUPT` so that one code never carries two remedies. On read-only recovery the
association's own carrier naming decides first: an association that names another carrier is the
existing `binding-unusable` refusal of the recovery request.

**Why F46 is `HOST.IO_FAILURE`.** An association is written only with a committed carrierFormat 3
`SEAL`, so one naming a historical generation contradicts two retained owners. That is the
`unknown-custody` family (`HOST.IO_FAILURE`, `host-io`): not a caller defect (request-rejected), not a
stably observed quarantine (`LEDGER.CORRUPT`) and not contention. It never becomes not-committed or a
confirmation.

**Interrupted state and stale custody.** Each phase re-evaluates every predicate from the bytes it
reads at that open or in that journal snapshot: a cached verdict, `first_generation`,
`projectKeyDigest` or earlier successful open is never reused. A writer or maintenance refusal appends
nothing, publishes nothing and writes no marker, because `carrier_quarantine.reason` keeps its inherited
enum; the next open detects the same condition again. Read-only recovery writes nothing, uses
`MIGRATION.CORRUPT` on no path, and reports the quarantine-condition row only with its Step 4 stable
observations, otherwise `unavailable-busy`. A lawful `{A}` or `{A, B}` prefix stays a resumable
interrupted migration, never a corruption diagnosis. No route confirms, negates or settles an attempt,
merges split-brain rows, rewrites the immutable format row or grants authority.

## 9. Read dispatch

Every generation lives entirely in exactly one table, and generations are totally ordered per
project, so the union is unambiguous.

| Generation location | carrierFormat | recordSchema admitted | Reader rule |
|---|---|---|---|
| `grant_journal`, gen < `first_generation` | 1 or 2 | 1 only | historical; no `SEAL` is representable |
| `grant_journal_v3`, gen >= `first_generation` | 3 | 3 operational, 1 for `TERMINAL` | current |

Reader laws:

- A historical generation's `platform` value is surfaced as `platformHistoricalAlias` and is
  **never** presented as an S8 machine id, never rewritten, and never joined to
  `RepoExecutionGrantV2.platformId` or a truth-table key.
- A historical generation can never satisfy a schema-3 `SEAL` join, because no `SEAL` row can
  exist there. A recovery request whose association names such a generation returns
  `unknown-carrier-incompatible` (F31/F46), never `not-committed`; its public route is §8.1.
- Historical bytes are read under recordSchema-1 semantics. They are not relabelled as schema 3
  and are not re-admitted through the schema-3 gate. This preserves the existing
  `JournalRecordV2` law, which exists "only to identify historical bytes so they are refused as
  current rather than relabelled".
- `AUD`, `CHECKPOINT`, `EXPIRY`, `MIGRATION` and `NARROW` rows may exist in historical
  generations and are readable as history. They are not writable in carrierFormat 3 (C2 refuses
  all five) and never enter `LinearizationV1`.

**Reader bridge, and a withdrawn claim about the transition protocol.** An earlier draft said the
carrier-format transition was "an S9-governed store transition" using an
"`InstallationTransitionJournalV1`-shaped intent". **Both halves are withdrawn.** Root's frozen-owner
counterexample, reproduced in C13, shows a carrier-only transition cannot reuse the closed logical
`store-migrate` intent — it refuses `TRANSITION.MIGRATE_REQUIRES_SCHEMA_ADVANCE` and
`TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE` — and an invented `carrier-migrate` refuses
`TRANSITION.OPERATION`. Further, `InstallationTransitionJournalV1` is a closed 20-member **journal**,
not an intent, and neither it nor the closed 11-member intent has any carrier field. The protocol is
instead the private one in `carrier-migration.v1.md`, authorized as a per-namespace maintenance step
of the existing `store-gc` operation.

**Reader staging, corrected.** An earlier draft of this section said a carrierFormat-{1,2}-only
core "refuses a carrierFormat 3 carrier **typed**". That contradicted `carrier-migration.v1.md` §5
and is withdrawn: a core that predates `carrierFormat` looks only for `grant_journal`, cannot see
`carrier_format`, and therefore **cannot be made to refuse**. Only a core that already knows the
axis can refuse on it. The accurate statement is:

- A **carrierFormat-aware** core that supports only {1, 2} refuses a carrierFormat 3 carrier typed
  and keeps its prior generation until it expires. This is the S9 dual-reader pattern and it works.
- A **format-unaware** core cannot refuse at all. Its lawful reaction to a `TERMINAL`-closed
  generation is to roll to a new generation in the inherited table, which can collide numerically
  with `first_generation`.
- That collision is therefore **detectable, not preventable**: any generation at or above
  `first_generation` appearing in the **inherited** table is a split-brain custody condition, never
  valid history, and is never merged into the current generation sequence (public route §8.1). The mitigation is the
  existing ordered-release discipline — ship the format-aware core first, enable migration only
  once the install's selected core generation is at or above that release. That is an
  implementation and release obligation, and it is a **selected disclosed limitation**, not an
  unresolved architectural question.

Floors (`rootVersion`, `indexSnapshotVersion`, `revocationVersion`, `evalHighWater`,
`lastAccepted`, `recoveryEpochSerial`) copy forward unchanged; a poisoned floor is not lowered, and
only S4.5 lowers it.

## 10. Body bytes, digests and the chain

These were never stated together in one place, and one of them is stated *nowhere* precisely.
carrierFormat 3 pins all three explicitly.

- `body` is `opensip-metadata-canonical.1` bytes in domain `opensip.metadata.journal.1`
  (carrierFormat 1 DDL comment).
- `body_sha256` is the **domain-framed** digest
  `SHA256("opensip.metadata.journal.1" || 0x00 || C(body))`, *not* `SHA256(body)`. Established by
  execution in C1 against the frozen `security_unit_lib_v8.record_body_sha`:
  `body_sha256_is_domain_framed = true`, `body_sha256_is_raw_sha256_of_body = false`.
  This matters because the followup review's recovery predicate asserts
  `body_sha256[j] == SHA256(body[j])`; a validator implementing that literally would reject every
  lawful record (§11).
- `prev_sha256[1]` is the genesis value
  `SHA256("opensip.journal.genesis.1" || 0x00 || projectKey_utf8 || 0x00 || ascii(grantGeneration))`,
  which is `security_unit_lib_v8.genesis_prev`.
- `prev_sha256[k]` for k > 1 is specified in the whole corpus by exactly one artifact: the
  carrierFormat 1 DDL comment `-- chain: sha256 of previous record's body_sha256||seq`. There is
  no reference implementation of it (`genesis_prev` is defined but has **zero** call sites, C1),
  and no retained fixture anywhere in Source25 carries a concrete `prev_sha256` value. The byte
  encoding of `||` and of `seq` is therefore **not pinned by any frozen artifact**.

**carrierFormat 3 pins it as `chain_law` 1:**
`prev_sha256[k] = SHA256(ascii_hex(body_sha256[k-1]) || ascii_decimal(k-1))`, no separator.

**This is a prospective choice, not a derivation.** An earlier draft claimed it was "the only
reading consistent with both operands being TEXT columns". That was wrong and is withdrawn:
`body_sha256` is a TEXT column but **`seq` is an INTEGER column**, so the column types force no
reading at all. The encoding is selected because it is a reasonable reading of the inherited DDL
comment, and for no stronger reason. `chain_law` records that a choice was made.

The DDL **refuses** any other value: `CHECK (chain_law = 1)`. Value 2 is not selected and not
implemented, so the carrier does not advertise an alternative that does not exist.

**Honest compatibility limit.** This is a *prospective* pinning, recorded in
`carrier_format.chain_law`. It cannot be claimed as byte-compatible with carrierFormat 1 or 2
instances, because no such instance and no fixture exists in the reviewed corpus to compare
against. For a historical generation the reader recomputes the chain under `chain_law` 1 and
reports `chain-consistent` or **`chain-unverifiable`**. `chain-unverifiable` is a diagnostic, never
tamper and never invalidation. No old row is rewritten to make a chain verify.

## 11. What a witnessed anchor can actually prove (CR-08)

Root's premise is correct and this correction does not overclaim. The measurement is stronger and
narrower than the followup states. Control C2 built real records with the frozen digest
functions, substituted an interior body, recomputed the successor `prev_sha256`, and compared what
each candidate anchor field would see.

| Substitution | `chain_law` | tampered carrier self-consistent | seen by witness `bodySha256` | seen by chain-head `prev_sha256` |
|---|---|---|---|---|
| at seq 1 | 1 | yes | **no** | **no** |
| at seq 2 (= tail-1) | 1 | yes | **no** | yes |
| at seq 1 | 2 (recursive) | yes | **no** | yes |
| at seq 2 | 2 (recursive) | yes | **no** | yes |

Three conclusions follow. **Attribution matters here, so it is stated plainly:**

1. **The weak-chain / tail-body limitation itself is not a new finding.** Root's original task
   statement already said the inherited `prev_sha` formula "binds only previous body digest/index,
   NOT a recursive cryptographic chain; it cannot cryptographically authenticate all interior
   bodies against a tail", and the followup review states the same bound in its §4.2. What this
   control adds is the *measurement* — an executed matrix showing exactly which candidate anchor
   field sees which substitution — not the limitation.
2. **The v8 witness detects no interior substitution at all, under either chain law.** The closed
   witness shape is `{witnessSchema, projectKeyDigest, grantGeneration, seq, state, bodySha256}`
   with "no other member". `bodySha256` is the *tail body* digest; substituting any interior body
   leaves it unchanged. So no witnessed anchor as currently specified authenticates any interior
   prefix, and a recursive chain alone would not change that.
3. **The distinct new finding is a wording contradiction between two frozen documents.**
   carrierFormat 1 §5.4 states *"Hash chain. Tamper-evidence for audit, not tamper-proof; **the
   chain head is in the witness**."* The chain head is **not** in the v8 witness
   (`witness_carries_chain_head = false`, C2). This is separate from the weak-chain limitation in
   (1): it is a claim about *where the anchor lives*, and the two historical documents disagree.
   The v8 closed shape governs; the v1 sentence is inaccurate as a description of v8. This needs an
   owner disposition, not a silent edit, because both documents are immutable.
4. The inherited `chain_law` 1 chain head binds only the immediately previous body digest and
   index. Even if the witness *did* carry the chain head, `chain_law` 1 would detect a
   substitution at seq t-1 and miss every earlier one.

**Therefore:** protected custody plus a surviving witness and floor **can** confirm that the
requested `SEAL` row is present now with its joined digest, `operationRef` and `runId`; that the
sequence is contiguous; that the tail is the one the retained anchor names; and that no rollback
below the last *observed* operation boundary has occurred. They **cannot** authenticate the
interior prefix. Where the anchor or join is unavailable the answer is **`unknown`**, explicitly
not invalidation. The conclusion class is `confirmed-under-retained-custody`, never
"cryptographically proven". This is the same bound v8 §5.4 "Detection bound (honest)" and §5.5
already state for coherent whole-carrier rollback.

This does not block recovery, because the authoritative evidence that an attempt committed is the
**evidence-ledger receipt plus private association**, not the journal prefix. The journal join is a
corroborating custody check, and that is all this correction claims for it.

### Stronger physical authentication: explicit versioned options, with costs

Not adopted here. Recorded for root's decision. Note that option A alone is **insufficient** —
the executed matrix above shows the witness field is the binding constraint, not the chain law.

| Option | Change | Cost |
|---|---|---|
| A. recursive chain only | `chain_law` 2: `prev_sha256[k] = SHA256(prev[k-1] \|\| body_sha256[k-1] \|\| dec(k-1))` | one extra hash input per append (negligible). **Does not help alone**: the witness still carries only `bodySha256`. New `carrier_format.chain_law` value; no public schema change; cannot apply to existing generations without rewriting rows, which is forbidden |
| B. witness carries the chain head | new `witnessSchema` 2 adding a `chainHead` member | the v8 witness shape is a **frozen closed** shape with "no other member", so this needs a new witness schema version, a dual-reader for witness 1 and 2, and reconciliation-table review. No public wire major changes, but it touches a frozen security boundary |
| A + B together | both | the only combination that authenticates an arbitrary interior prefix against a witnessed anchor. Still does **not** defeat a coherent whole-carrier rewrite performed while no operation was running with witness and floor rewritten consistently; that needs external attestation |
| C. signed tail attestation | signature over the tail at each append | defeats the coherent-rewrite case, but needs a signing key available at every append, which is a key-custody and per-append cost question. An earlier draft claimed this inherently requires networking and breaks offline operation; that is **withdrawn as unsupported** — a local key does neither |

**Recommendation.** If root wants the stronger property, adopt **A + B** for carrierFormat 3 only,
where no instance exists yet, and leave carrierFormat 1 and 2 generations at `chain_law` 1 with
`chain-unverifiable` reporting. Do not adopt A alone: it would add a law and buy nothing
observable. `carrier_format.chain_law` exists in the DDL precisely so this is a recorded
versioned decision rather than a silent reinterpretation.

## 12. Change set and cross-contract impact

Owner change set, kept minimal:

| Artifact | Change | Owner |
|---|---|---|
| `grant-journal.carrier.v3.sql` | new file | security |
| `carrier-format.v3.md` (this file) | new file | security |
| `carrier-dispatch.v3.json` | new file | security |
| `carrier-highwater.schema.v1.json` | new file | security |
| `commit-recovery-readonly.v3.md` | new file, selected current owner | architecture/storage |
| `carrier-migration.v1.md` | new file, selected current owner | security |
| `attempt-custody.schema.v1.json` | new file (minimal private owner contract) | storage/ledger |
| `implementation-boundaries-and-build-plan.md` | minimal patch: COV-03 resolved, recovery algorithm reference, new fault cases | architecture |
| `commit-recovery-plan.v1.json` | minimal patch: F38–F53 added, F38–F49 identities and meanings unchanged, F32 root route untouched | architecture |
| **candidate25** `docs/v2/contracts/product-v1/identity-and-evidence.md` | minimal patch: attempt-custody phase, read-only recovery selectors, narrow assurance limit | identity |
| **candidate25** `docs/v2/contracts/product-v1/security-and-lifecycle.md` | minimal patch: S1 selection, S6 gate + reader rule, S9 carrier bridge and generation closure, S12 projections | security |

Only **two** candidate25 owner files are patched. The security schema bundle
(`security-lifecycle.schemas.v1.json`) is deliberately **not** touched: the new private records
live beside the association in the planning artifacts, not in the security bundle, so root can
merge this with the separately authored PS01 and PS04 work without collisions.

Unavoidable cross-contract additions, each stated rather than assumed:

1. **WA-13 gains a third generation-closure cause** (carrier-format migration), using the existing
   typed `grantGenerationClosure`. No schema, enum or wire major changes. Note that `WA-13` appears
   **only** in the immutable historical `security-completion.v8.md`; it has no occurrence in the
   current owner. The successor statement is therefore added to the current owner
   (`security-and-lifecycle.md` §9), and the historical v8 text is left exactly as it is.
2. **S9 gains a carrierFormat reader bridge** alongside the existing root-schema and
   state-decoder bridges. Same mechanism, new axis. No new lock mode.
3. **A new closed shape `CarrierHighWaterV1`** (§10 of `carrier-dispatch.v3.json` and
   `carrier-highwater.schema.v1.json`). The SC-TRUST high-water currently has *no* closed shape
   law: the only stated field list is carrierFormat 1's `{project, grantGeneration, lastSeq,
   tailSha256}`, while the witness beside it has a strict closed shape validated before any
   comparison. The recovery algorithm's floor case depends on `H.lastSeq` and `H.tailSha256`, so
   the floor record needs the same shape discipline the witness already has. It also renames
   `project` to `projectKeyDigest` to match v8's carrier naming. This is a new private record,
   not a public wire schema.

Nothing else changes. Public wire majors are preserved: `run3`, `exec1_`, the receipt, `JournalRecord`
schema 3, `JournalRecordV2`, the recordSchema-1 bodies, `LinearizationV1`, D9 classes and codes,
and the four identity representations are all untouched.

## 13. Reference validation and limits

`check-carrier-v3.py` in this directory is the reference validator. It re-runs the executed
controls and additionally validates the new JSON artifacts against Draft 2020-12 and the
frozen vocabularies they claim to join.

What was actually executed this session, in the reference environment
(`/tmp/opensip-architecture-review-env/bin/python` 3.12.13, SQLite 3.50.4, jsonschema 4.25.1):

- C1: frozen carrier laws, record-type and platform set algebra, digest semantics, and the full
  14-row `reconcile_witness` table against the frozen implementation.
- C2: the proposed DDL — 35 admit/refuse probes, migration with before/after row comparison, the
  five-case open dispatch, and the anchor-field discrimination matrix.
- C3: the read-only recovery algorithm (21 cases) and the commit-admission gate (7 cases plus 15
  exhaustive latch interleavings) as executable models.
- C4: reference validation of the new artifacts and of the two minimal patches.

What is **not** established: OS durability, `fsync`/`F_FULLFSYNC` behaviour, real process
isolation, SQLite behaviour under real crashes, lock behaviour under real contention, Rust
compilation or borrow-checking of any API sketch, and any qualification gate. Every crash case
below F00 remains `not-executed`. The reserved-slot probes used a disclosed in-memory harness that
lifts and reinstalls a trigger verbatim, because the slot is unreachable by contiguous append in
bounded time; no frozen file was touched. All SQLite work was in-memory; no carrier file was
created, opened or migrated on disk.

**Integrated fresh-install boundary.** An all-seven-valid-object footprint without a format row and without an inherited `grant_journal` is an interrupted fresh installation. No carrier format is published yet; a separately admitted maintenance attempt resumes act C with `first_generation = 1`, `chain_law = 1`, and null `migrated_from`/`migration_op_ref`. It appends no TERMINAL. Inherited-table maximum/generation checks apply only when that table exists; published-row field checks apply only after the row exists. No absent table or absent row is queried to make this decision. This scopes the common recovery table and post-detection checks to the fresh path already selected above.

**Evidence custody and diagnosis vocabulary.** Evidence: the `scratch/out/cN.json` and other
`scratch/` citations in this document and the dispatch are relative to the original
author review runtime, not companion files at these normative paths. They add no
law and their presence must not be inferred from a citation. The current
`check-integrated-carrier.v1.py` reconstructs the historical validator layout from
the selected normative companions and runs `check-carrier-v3.py`; that rerun is
new reference evidence, not reproduction of the original C1–C18 measurements.
`witnessMalformed` is a read-only recovery diagnosis only. It deliberately is not
a durable `carrier_quarantine.reason`: read-only recovery cannot write a marker,
and this revision preserves the inherited quarantine table definition.
