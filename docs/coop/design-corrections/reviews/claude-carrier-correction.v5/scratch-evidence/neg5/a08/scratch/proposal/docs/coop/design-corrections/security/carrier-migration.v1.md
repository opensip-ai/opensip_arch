# Private carrier-format migration protocol (PROPOSED)

**Standing.** Proposed design/reference correction. PROPOSED-NOT-SELF-ACCEPTED: no acceptance, no
readiness, no application and no implementation authorization. Private design/reference work, not
OS qualification. Authored against frozen Source25
`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`.

**Why this document exists.** The v4 dispatch said the carrier transition used an
"`InstallationTransitionJournalV1`-shaped intent". Root's supplied counterexample
(`carrier-transition-counterexample.json`, reproduced in C13) shows that is wrong on frozen bytes:

- Reusing the closed logical `store-migrate` intent with an unchanged state schema and store
  generation refuses **`TRANSITION.MIGRATE_REQUIRES_SCHEMA_ADVANCE`** and
  **`TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE`**.
- Inventing `operation: "carrier-migrate"` refuses **`TRANSITION.OPERATION:carrier-migrate`**.
- `InstallationTransitionIntentV1` is a closed **11**-member record and
  `InstallationTransitionJournalV1` a closed **20**-member record. Neither has a carrier field, and
  the journal is not an intent.

A carrier-only, physical, single-project act therefore cannot borrow the install-wide logical
transition protocol. This document defines the minimal private protocol instead. It adds no public
operation, no CLI command, no authorization class, no schema member and no enum value.

## 1. Authorization, traced to an existing owner

No new authority is minted and no analysis operation authorizes a lifecycle mutation.

| Question | Existing owner, verbatim |
|---|---|
| Which command may perform it? | `store-gc`, from the frozen workflows command inventory: `owner: "security"`, `requestClass: "lifecycle"`, `authorizationClass: "exclusive-lease"`, `writesTrackedIntent: false`, `steps: ["mutation", "render"]` |
| What lock discipline? | S7: the install-wide fence at level 0 plus `EXCLUSIVE` on the affected project namespace, `LOCK_EX|LOCK_NB`. S7's existing GC law already states "GC census is a `LOCK_EX|LOCK_NB` probe under the fence and a busy probe means retain" and "GC iterates registered namespaces and treats a busy namespace as retain, never as refusal" |
| What reports it? | `store-status`, whose frozen parity fields already include `migration-state` |
| What closes the inherited generation? | The inherited generation-closure authority itself: a `TERMINAL` record with the existing typed cause `grantGenerationClosure`, which the frozen carrier already admits |

So carrier-format migration is **an additional per-namespace maintenance step of the existing
`store-gc` operation**. `writesTrackedIntent: false` is the decisive property: `store-gc` is already
a security-owned, exclusive-lease mutation that writes **no** tracked intent, which is exactly why
it does not drag in the S9.2 transition intent or journal.

A busy namespace is **skipped and retained**, never refused, exactly as GC already behaves. An
unmigrated carrier is fully usable by a format-aware core (§5), so skipping costs nothing.

**Not claimed:** this is not a user-visible feature, not a new flag, and not a reason to widen
`store-gc`'s parity fields. `migration-state` already exists.

## 2. The private intent, and why it is not durable

`CarrierMigrationIntentV1` is a **private, host-projected, never caller-authored** record,
validated before any durable act. It uses the **product/foundation canonicalizer of identity §3**
(no normalization, integers to 2^64−1, raw SHA-256 where a digest is taken) and **not** the
`opensip-metadata-canonical.1` metadata profile, because it is neither signed security metadata nor
a journal record. Per S2 a decoder for one profile never admits the other's documents, so the
profile is stated rather than left to inference.

```
CarrierMigrationIntentV1 {
  recordSchema:      1,
  namespaceId:       the registered project namespace, binary equality,
  projectKeyDigest:  hex64, the carrier's own digest from the admitted project key,
  observedFormat:    1 | 2,        // from the open dispatch, never from a request field
  targetFormat:      3,
  closedGeneration:  i64 >= 1,     // the inherited generation this act closes
  firstGeneration:   i64 >= 2,     // recomputed at act C, never fixed at planning time
  migrationOpRef:    ^op-[0-9a-f]{32}$   // the store-gc operation's own token
}
```

**It is deliberately not persisted.** S9.2 needs a durable intent and journal because its footprint
spans a namespace registry, several leases and a renamed store, and because a half-renamed store is
*ambiguous*. This protocol's three durable acts are each atomic and each **self-describing** (§3),
so there is no ambiguous intermediate state for a durable intent to disambiguate. Persisting one
would add a private record that no recovery decision reads. The `TERMINAL` row's own
`operationRef` — a member the frozen recordSchema-1 body already requires — is the only durable
marker recovery needs, and it adds no field to anything.

## 3. Durability order and the total footprint

Three durable acts, in this order, each its own atomic transaction:

| Act | What becomes durable | Atomicity |
|---|---|---|
| **A** | one `TERMINAL` row appended to the inherited `grant_journal` at tail+1, cause `grantGenerationClosure`, carrying `migrationOpRef` as its `operationRef` | single INSERT under the inherited append triggers |
| **B** | `grant_journal_v3`, `carrier_format` and their triggers created | one DDL transaction; SQLite DDL is transactional, so B is all-or-nothing |
| **C** | the single `carrier_format` row inserted, publishing `first_generation` and `chain_law` | single INSERT, immutable by trigger |

**A precedes B and C.** If objects were published while the inherited generation stayed open, the
carrier would hold one generation in two tables and a format-unaware core could keep appending to
it. Closing first removes that window.

**C is the commit point, and detection is keyed on the row, not the tables.** The open dispatch
reads carrierFormat 3 if and only if the `carrier_format` **row** with `singleton = 1` exists.
Tables without the row are an incomplete footprint, not a format-3 carrier. This is the change that
makes B recoverable rather than merely idempotent.

**`first_generation` is recomputed at C**, as `max(grantGeneration)` over the inherited table plus
one, under the same held `EXCLUSIVE` lease. It is never fixed at planning time, so a benign
interleaving (§5) cannot make it stale.

### Total recovery over every durable prefix

There is no torn state to repair, because each act is atomic and the physical state is
self-describing. Recovery is a decision function, not a rollback:

| Durable prefix | Observable state | Carrier standing | Resume action |
|---|---|---|---|
| ∅ | no `TERMINAL` at the inherited tail, no new objects | carrierFormat 1 or 2, generation open | none; a later `store-gc` may start at A |
| **{A}** | inherited tail is `TERMINAL`; no new objects | carrierFormat 1 or 2, generation **closed** | resume at **B**, recomputing `closedGeneration`. This is the "failure after TERMINAL and before final metadata" case |
| **{A, B}** | new objects exist, `carrier_format` has **no row** | still carrierFormat 1 or 2 by detection | resume at **C**, after verifying the existing object definitions byte-equal the selected DDL; otherwise `MIGRATION.CORRUPT` |
| {A, B, C} | `carrier_format` row present | carrierFormat 3 | none; complete |

**Commit uncertainty on A** is resolved from frozen fields only. Re-read the inherited tail: a
`TERMINAL` whose `operationRef` equals this operation's `migrationOpRef` means our own A became
durable, so proceed to B. A `TERMINAL` with a different `operationRef` means another operation
closed the generation, which is harmless — proceed to B. No `TERMINAL` means A did not become
durable, so retry A. A re-append can never double-apply, because the frozen
`gj_seq_contiguous` trigger refuses any append to a generation that already holds a `TERMINAL`.

**Commit uncertainty on B or C** is resolved by re-reading the same predicates; both acts are
idempotent under the prefix table.

"A second migration aborts because the table already exists" is **not** recovery and is not relied
on. Object existence is a resume signal in prefix {A, B}, and B verifies definitions rather than
assuming them.

**Nothing is rewritten, no constraint or trigger is disabled, and no old row is relabelled.** The
`TERMINAL` body is the frozen recordSchema-1 TERMINAL body; the private protocol adds no public
field to it.

## 4. What the read-only reader must do meanwhile

A read-only recovery or query that opens a carrier in prefix {A} or {A, B} observes a lawful
carrier whose newest generation is closed. It must report the ordinary busy/unavailable standing
for a carrier that cannot currently accept an append — never a corruption diagnosis, and never a
claim about any committed attempt. The bracketed capture protocol of
`commit-recovery-readonly.v3.md` already produces that outcome, because a closed generation is a
lawful stable state, not an adverse witness or floor condition.

## 5. An honest physical limit: detectable, not preventable

A core that predates `carrierFormat` entirely looks only for `grant_journal`. After migration it
cannot see `carrier_format`, so it cannot be made to refuse. Its lawful reaction to a
`TERMINAL`-closed generation is to roll to a **new generation in the inherited table**, which can
collide numerically with `first_generation`.

- **Prevention is impossible within the inherited format**, which has no mechanism to refuse. Saying
  otherwise would be an overclaim.
- **Detection is exact**: the read dispatch treats any generation greater than or equal to
  `first_generation` appearing in the **inherited** table as a split-brain custody condition, never
  as valid history, and never merges it into the current generation sequence.
- **The mitigation is the existing ordered-release pattern**, not a new mechanism. S9 already ships
  a stage-2 core under the stage-1 catalog so every install updates by its ordinary path. The
  format-3-capable core ships first; migration is enabled only once the install's selected core
  generation is at or above that release. Until then `store-gc` skips the step.
- For **carrierFormat 1** the limit is wider, because that format has no `TERMINAL`-closure trigger
  at all, so a format-1-only core could append *into* the closed generation. The reader law already
  marks such generations `closed-by-record, not-trigger-enforced`, and any row after the `TERMINAL`
  is a custody condition.

This is the same class of limit as the inherited weak chain: a consequence of migrating an
immutable format, disclosed rather than engineered away.

## 6. What this does not touch

- No logical `stateSchema` change. `carrierFormat` and `stateSchema` stay separate axes, and this
  protocol changes neither the state schema nor the store generation.
- No `InstallationTransitionIntentV1`, `InstallationTransitionJournalV1`, transition `operation`
  enum, `core_transition_affected_namespaces`, or `recover_transition_journal`.
- No public wire major, no public operation, no new authorization class, no new CLI command, no new
  `DomainDetailCode`.
- **PS-01** owns the random store-instance identity and the S9 private store-generation lineage; its
  binding tuple and digest shape are unchanged and are consumed here as inputs only. Lineage
  allocation is not duplicated here — it is in `owner-correction.v3`.
- **PS-04** (report release asset anchor) is untouched.
- Native-evidence schemas are untouched, so the seven reminted Runs on their exact new digest are
  unaffected.
