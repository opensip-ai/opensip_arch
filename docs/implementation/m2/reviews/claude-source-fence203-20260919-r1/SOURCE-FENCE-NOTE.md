# SOURCE-FENCE-NOTE — follow-up to my transition203 assistance, Q3 (and Q1)

Separate note; `REVIEW.md` here is unchanged (its `hashes.txt` still verifies). **Assistance only, not approval.** Sources: my verified 201 reference extraction and my verified 204 product extraction (read-only); no drafts, no historical review archives.

## 0. Withdrawal of my option (b) as I worded it
In §6 of `REVIEW.md` I proposed an attribution-leading file with the trust-role change *derived*: "a store whose attribution names an execution whose journal is ≥ the fence point is fenced by definition". Root's objection is correct and the wording is wrong on three counts:
1. **186 has a row where the journal is still PREPARED and the fence is already this execution's** (`PREPARED | this | source | PREPARED/COMMITTED → RESUME-COMMIT`). The order is `… prepared image durable → source fenced by this execution → carrier COMMITTED → jCOMMITTED`: the fence precedes *any* later journal revision. A definition needing journal ≥ COMMITTED cannot produce that observation.
2. The fence must outlive the journal: "A fence remains after DONE, slot retirement, and ordinary PRESENT" (corr.188). After retirement there is no active journal to derive anything from.
3. It made trust *standing* a function of lifecycle state, while PRESENT must be able to change standing on its own ("PRESENT changes trust standing but never clears this attribution").
So the fence observation has to be a **self-sufficient durable fact in the store's own trust state**, written at the irreversible act. What survives from (b) is only the ordering instinct; the mechanism below replaces it.

## 1. What the actual trust-state owners define (codec and carrier, not paths)

| Fact | Evidence |
|---|---|
| The retained trust record has a closed shape: `TrustClockRecordV1`, **11 members** — the six `FLOOR_KEYS` (`rootVersion, indexSnapshotVersion, revocationVersion, evalHighWater, lastAccepted, recoveryEpochSerial`) + `anchor, pendingRecoveryChallenge, revocationIssuedAt, catalogExpiresAt, rootExpiresAt` | `security-lifecycle.schemas.v1.json` `/schemas/TrustClockRecordV1`; model `FLOOR_KEYS` l.2281 |
| **Roles are not in that record.** They exist as a prose string in the transition model (`new['roles'] = 'ST-UNBOOTSTRAPPED:MIGRATED …'`, `after['roles'] = 'ST-UNBOOTSTRAPPED:RESTORED'`, `oldStoreMark='RESTORED'`) and as "per-role state (`ST-*`)" in the historical SC-TRUST member list | model l.2291–2296, l.2316; `security-completion.v1.md` §5.1 l.446 |
| **"Source trust fencing" concretely = the source store's roles become `ST-UNBOOTSTRAPPED:RESTORED`** ("after commit the stage-1 core observes RESTORED and refuses until a schema-1-verifiable payload at or above the floors"); and that role alone is not attribution ("RESTORED alone is not attribution", "A … trust role RESTORED alone proves no progress") | model l.2296; S&L l.1688, l.1225; STP l.54 |
| Trust state is **store-bound in law**: prepared-image equality is against "the fenced **source** floors" / "per-field max(fenced source, **retained target**)"; rollback sets floors "to the maximum of **both stores**"; a migrated store "may lawfully rest with floors carried and roles `ST-UNBOOTSTRAPPED:MIGRATED`" | STP l.127–136; S&L l.1239–1242, l.1699–1700 |
| The only carrier any owner names is **install-level**: v1 §5.1 "`trust.sqlite` at the install root, WAL … separate file … so lifecycle restore cannot carry trust state", repeated by PSL's row "General trust database \| `trust.sqlite` \| Existing SC-TRUST owner" | v1 l.452; PSL l.26 |
| The **product implements no trust-state carrier**: `security/src/trust_time.rs` is a pure assessment whose header says it does not "persist a floor" and returns proposed writes (`floor_write`, `anchor_write`, `last_write`); `trust.rs` is metadata/signature/root codec. No file or table holds a trust record or roles | 204 product tree |
| Restore law: "Trust floors are excluded from lifecycle backups and generation rollback; any declared restore marks every role `ST-UNBOOTSTRAPPED` with reason `RESTORED` and keeps the restored counters … as floors"; evidence restore "restores no trust floor" | v8 §5.5; lineage `floorsAndAuthority` |
| Pre-lease trust observations are physically write-free with **no SQLite exception** | readonly §2 (195/197) |

**Genuine missing owner (must be resolved before Q3 can be closed):** *which SC-TRUST members are store-bound and where that store-bound state lives.* 186 cannot work unless the six floors and the roles exist **per store instance**; the only named carrier is one install-level `trust.sqlite`. Nothing says how v1's member list (accepted root documents, index snapshot bytes, revocation list, per-role state, counters, high-water) splits between the two. I cannot settle that from existing text; everything below is conditional on the split "documents install-level, *state record* store-bound", which is the only reading under which the 186 floor laws are meaningful.
A second existing conflict, independent of this note: a **WAL** `trust.sqlite` read by fence-only report surfaces (`trust doctor`) creates sidecars, against the write-free law. 197 resolved this only for ledger/journal.

## 2. The two candidates, against root's three requirements
R1 PRESENT changes standing without clearing attribution · R2 after retirement the old source stays fenced until PRESENT · R3 a durable fence observation exists immediately after the irreversible act, before any later journal revision.

### A. One-file store trust capsule (recommended)
`stores/S/trust-state.v1` — private, product-canonical, raw == canonical(decoded), replacement-published (temp in the same directory → fsync → rename → fsync dir):
```
StoreTrustStateV1 = { "capsuleSchema": 1,
                      "storeInstanceId": S,                 // must equal the marker: a capsule copied from another store is misbound
                      "clock": { …the 11 TrustClockRecordV1 members, verbatim, nothing added… },
                      "roles": <the owner's per-role state>, // today only prose; needs its closed shape (see §3)
                      "sourceFence": null | { "executionId": E, "intentDigest": D } }
```
- **The irreversible act is one rename** that changes `roles → ST-UNBOOTSTRAPPED:RESTORED` *and* `sourceFence → {E, D}` together. That *is* "one recoverable commit boundary" (STP l.82), without claiming anything about two files. **R3**: the observation is complete the instant the rename is durable; the journal can still be PREPARED. Crash before ⇒ old capsule ⇒ `fence old` ⇒ ABORT rows; crash after ⇒ `fence this` ⇒ never ABORT.
- **R1/R2**: PRESENT republishes the capsule with new `roles`/`anchor`; `sourceFence` is copied verbatim. Fenced *standing* lives in `roles` and ends at PRESENT; *attribution* lives in `sourceFence` and ends only when the next transition fences this store as its source (corr.188) — two members, two lifetimes, one file, so neither is a derived or unjoined copy of the other.
- **Not clearing by accident is a codec property, not a convention**: every S4 floor write and PRESENT also rewrites this file (floors and attribution share it). Give storage/security exactly two writers: `republish(prev, |clock, roles| …)` whose closure cannot reach `sourceFence`, and `fence_source(prev, E, D)` which is the only function that sets it and also sets the RESTORED role. A test that any `republish` output has byte-identical `sourceFence` pins R1.
- Creation: a new store gets its capsule with `sourceFence: null` (= observed-none) before first publication, like the marker. A store with a marker but no admissible capsule is **unavailable**, never observed-none — corr.188's "older carrier without an admitted attribution representation". No on-read initialisation.
- 186 joins fall out of one file: `fromFloors`/`targetFloors` are the `clock` six keys of the two capsules; ancestor "apply the prepared max-floor image to the retained target idempotently" is a republish of the target capsule. A retained ancestor keeps the attribution from when *it* was last a source — an **old** fence relative to the current execution, which is what the table expects.
- Restore/backup: the capsule is inside the store root, so a declared store restore brings counters back — exactly the case v8 §5.5 already governs (mark every role RESTORED, keep restored counters as floors). Evidence-bundle restore/adoption must exclude it ("restores no trust floor"). `sourceFence` after a declared restore: treat as **unavailable**, not as the source's attribution (a restored store "never impersonates its source", S&L l.1908) — owner to confirm.
- Reads are plain bounded file reads ⇒ compatible with the write-free pre-lease law, and with 202's reader (subject to my 202 W-1 about returning the descriptor observation).
- Single writer holds: floor writes and transitions are already under the installation fence (PSL: "Existing floor advance/write authority remains under the installation fence").

### B. Attribution row in the same authoritative trust transaction
Sound **iff** the store-bound state is itself one SQLite database per store: then `UPDATE roles … ; INSERT OR … attribution` in one `BEGIN IMMEDIATE … COMMIT FULL` is a single boundary and meets R1–R3 as well as A (attribution table untouched by PRESENT's statement; guard with a 187-style trigger that only the fence statement may replace the row).
Costs that A does not have: (i) every pre-lease trust read opens a WAL database and creates sidecars — the unresolved write-free conflict above becomes load-bearing for *every* command; (ii) it needs the 195–198 reader controls and sidecar custody for one more database per store; (iii) if instead the row were put in the install-level `trust.sqlite` while floors/roles are per store, the boundary is two carriers again — **that variant must be rejected**, as must any file holding a copy of the role beside an authoritative role elsewhere.

**Recommendation: A**, conditional on §3. It is the smallest representation in which the fence observation is self-sufficient, PRESENT and the fence have separate members, and no two-object atomicity is asserted.

## 3. What root must decide (I cannot derive these)
- **D1 (blocking)** the store-bound vs install-level split of SC-TRUST members, and that the store-bound part is the capsule's `clock`+`roles`. Until then neither A nor B has an authoritative place to put the role.
- **D2** the closed shape of `roles`. No current schema has one; the model carries a sentence. The capsule should not freeze a prose string.
- **D3** `sourceFence` after a declared store restore: unavailable (my reading) or preserved.
- **D4** whether `trust.sqlite` at `I` remains WAL given fence-only readers, or whether those surfaces may not open it — existing conflict, surfaced here because B would multiply it.
- **D5** if A: capsule size cap (11 small members + roles; 4 KiB is ample) and the reader's bound.

## 4. Q1 — is there an existing executable-core selection carrier?
**None that I can find in the current owners or the product.** Current text only *presupposes* one: "the selected core closure is an immutable generation" (S&L l.886), "execute the selected closure by verified handle" (`admission-and-qualification.md` l.211), "currently selected signed core closure" (S&L l.2342), STP's "core closure plus full store binding" pair — no location, record or codec. The historical `lifecycle-carrier.contract.v2.json` selection (`generation` / `project_selection` / `transition` tables in `lifecycle.sqlite`) is a different mechanism in three ways: it is **per project** (`project_selection.projectKey`) where 186's pair is install-wide; it selects **component generations** with its own `PREPARING→VERIFIED→READY→COMMITTED` machine and `txId`; and PSL adopted only its namespace locator, explicitly not "the historical registry's superseded identity or lease protocol". The product lifecycle crate contains `leases.rs`, `lib.rs`, `locations.rs` only. So `selection.pair` (or its equivalent) does not collide with anything existing; the open point is the reverse one — a distribution/launcher owner must eventually *consume* this pair to start the core, and that owner is not in this tree.

## 5. Limits
Text and source reading only; nothing executed. The capsule is a proposal for root to reconcile, author and freeze; I will review the frozen bytes independently. My earlier 203 §6 should be read with §0 of this note.
