# Grant-journal physical carrier, carrierFormat 3 (PROPOSED design/reference correction)

**Standing.** Proposed versioned design/reference artifact resolving COV-03 and the carrier
findings CR-04 / CR-07. Authored by a non-blind actual Claude coauthor against frozen Source25
(manifest `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`; all 12869 members
verified this session). No acceptance, readiness, application or implementation authorization,
and no self-acceptance. Design/reference only: a physical DDL, an open/read dispatch and
reference validation. Not product Rust, not executable storage, not a crash-test result, and
not an OS durability claim. No historical or frozen file is modified by this correction.

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
14-member set. So the current logical journal cannot be written to any inherited physical carrier
at all, while `TERMINAL`, which the physical carrier *requires* at the reserved slot, is not a
member of the public schema-3 `JournalRecord`.

Those two facts are jointly unsatisfiable, which is exactly why loosening an enum is not an
option: loosening the physical set would admit `TERMINAL` as a public schema-3 record, and
loosening nothing leaves `SEAL` unwritable.

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
- **operation_ref grammar.** `op-` plus 32 lowercase hex, length 35.
- **GRANT completeness.** `install_generation_id`, `manifest_digest`, `platform` and `token` all
  present.
- **Witness and high-water laws.** Unchanged in substance; see §8 and §10.

## 6. Additions beyond the inherited DDL, and why each is needed

| Addition | Reason |
|---|---|
| `platform` CHECK uses the four S8 machine ids | resolves CR-04; alias-only values refused |
| `record_schema` column plus the segregation CHECK | resolves CR-07 without widening schema 3 |
| `run_id` column, NOT NULL on `SEAL` | binds the SEAL to its replayed `run3` identity in the carrier |
| `carrier_format` singleton table | names carrierFormat, `first_generation` and `chain_law` durably |
| `first_generation` trigger | keeps migrated generations out of the new table |
| superseded-generation trigger | enforces WA-13 generation ordering physically |

The last two are genuinely new laws. Neither can affect an inherited row: both live only on the
new table. The inherited DDL permitted appending to an older generation; carrierFormat 3 does
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
the legacy alias platform value retained verbatim as `macos-arm64`; a second migration aborts on
*table carrier_format already exists*; an attempt to write generation 1 into `grant_journal_v3` is
refused as *grant generation precedes the carrierFormat 3 first generation*.

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
version record. Executed detection predicate (C2, all five cases correct):

```
if   table grant_journal_v3 exists and table carrier_format exists -> carrierFormat 3
elif table grant_journal exists and trigger gj_seq_contiguous exists -> carrierFormat 2
elif table grant_journal exists -> carrierFormat 1
else -> empty carrier; create carrierFormat 3
```

Additional open-time checks, in order, before any read is admitted:

1. The stored SQL text of `carrier_quarantine` and `carrier_capacity_pause` must byte-equal the
   frozen definition. This closes the `CREATE TABLE IF NOT EXISTS` hole: a pre-existing variant
   can never be silently accepted. Verified equal in C2.
2. `carrier_format.project_key_digest` must equal the carrier's own `projectKeyDigest` derived from
   the admitted project key; otherwise `MIGRATION.CORRUPT`.
3. `max(grantGeneration)` in `grant_journal` must be strictly less than
   `carrier_format.first_generation`; otherwise `MIGRATION.CORRUPT`.
4. Witness reconciliation runs exactly as `security_unit_lib_v8.reconcile_witness` specifies. C1
   reproduced all 14 rows of the v8 §5.4 table against the frozen implementation with no
   deviation. Reconciliation is unchanged by this correction.
5. The SC-TRUST high-water comparison (v8 §5.4 fence handoff) runs as specified and is a separate
   step: the frozen `reconcile_witness` is pure and does **not** consult the high-water
   (verified in C1).

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
  `unknown-carrier-incompatible` (F31/F46), never `not-committed`.
- Historical bytes are read under recordSchema-1 semantics. They are not relabelled as schema 3
  and are not re-admitted through the schema-3 gate. This preserves the existing
  `JournalRecordV2` law, which exists "only to identify historical bytes so they are refused as
  current rather than relabelled".
- `AUD`, `CHECKPOINT`, `EXPIRY`, `MIGRATION` and `NARROW` rows may exist in historical
  generations and are readable as history. They are not writable in carrierFormat 3 (C2 refuses
  all five) and never enter `LinearizationV1`.

**S9 intent and reader bridge.** The carrier-format transition is an S9-governed store transition
and reuses the existing mechanism rather than inventing one: the install-wide fence is held for
the whole transition; the affected namespace set is the single project namespace enumerated from
the registry; `EXCLUSIVE` is taken non-blocking and all-or-nothing; an
`InstallationTransitionJournalV1`-shaped intent names the exact lease set and is written only
after every lease is held; crash recovery runs as the first act under the next fence acquisition,
from the durable footprint only, before any admission. Reader staging mirrors S9's dual-reader
pattern: a carrierFormat-{1,2}-only core refuses a carrierFormat 3 carrier **typed** and keeps
its prior generation until it expires; a carrierFormat-{1,2,3} core reads both. Floors
(`rootVersion`, `indexSnapshotVersion`, `revocationVersion`, `evalHighWater`, `lastAccepted`,
`recoveryEpochSerial`) copy forward unchanged; a poisoned floor is not lowered, and only S4.5
lowers it.

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
`prev_sha256[k] = SHA256(ascii_hex(body_sha256[k-1]) || ascii_decimal(k-1))`, no separator, both
operands as their TEXT column spellings. This is the only reading consistent with both operands
being TEXT columns.

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

Three conclusions follow, and the first is a defect not previously named:

1. **The v8 witness detects no interior substitution at all, under either chain law.** The closed
   witness shape is `{witnessSchema, projectKeyDigest, grantGeneration, seq, state, bodySha256}`
   with "no other member". `bodySha256` is the *tail body* digest; substituting any interior body
   leaves it unchanged. So no witnessed anchor as currently specified authenticates any interior
   prefix.
2. This contradicts the stated intent of carrierFormat 1 §5.4 — *"Hash chain. Tamper-evidence for
   audit, not tamper-proof; **the chain head is in the witness**."* The chain head is **not** in
   the v8 witness (`witness_carries_chain_head = false`, C2). Two frozen historical documents
   disagree about what the witness holds. The v8 closed shape governs; the v1 sentence is
   inaccurate as a description of v8.
3. The inherited `chain_law` 1 chain head binds only the immediately previous body digest and
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
| C. signed tail attestation | signature over the tail at each append | defeats the coherent-rewrite case, but requires a signing key available at every append, contradicting the offline posture and §5.6's cost budget |

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
| `commit-recovery-readonly.v1.md` | new file | architecture/storage |
| `implementation-boundaries-and-build-plan.md` | minimal patch: COV-03 resolved, recovery algorithm reference, new fault cases | architecture |
| `commit-recovery-plan.v1.json` | minimal patch: F38–F48 added | architecture |

Unavoidable cross-contract additions, each stated rather than assumed:

1. **WA-13 gains a third generation-closure cause** (carrier-format migration), using the existing
   typed `grantGenerationClosure`. No schema, enum or wire major changes. Must be propagated to
   the WA-13 reference text and the S9 footprint table.
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
