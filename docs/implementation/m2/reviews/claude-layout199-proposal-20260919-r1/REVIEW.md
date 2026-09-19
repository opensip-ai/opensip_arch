# Bounded assistance — B-8 physical layout: what is already law, what is missing

Reviewer: Claude. Date 2026-09-19. **Assistance only**: not a frozen review, not approval of any draft, no source read outside my verified 197 extraction (`claude-reference197-20260919-r1/…/candidate/docs`), no product/draft inspection, no edits. Evidence: `claude-out/io/path_law_search.txt`, `role_location_search.txt` (tree-wide searches; every quotation below was read at the cited line).

**Correction of my own 194 proposal first.** B-8 said the layout relation "is not stated anywhere". That was wrong for the grant journal: I searched prose and missed the JSON owner you found. It was also imprecise in asking for a "per-generation witness": the law has **one** witness per carrier.

## 1. Path decisions that already exist

| Role | Existing law | Owner (line) | Standing |
|---|---|---|---|
| Install root | resolved by the host foundation from the account database; no `HOME`/`XDG_*`/`PATH` | S3 (S&L l.160–163); foundation cases refuse `XDG_STATE_HOME` | current |
| Fence | `<installRoot>/lifecycle.fence` | S7 lock table l.770, l.856; model `LOCK_ORDER[0]` | current, prose = model |
| Lifecycle DB | file name `lifecycle.sqlite`; `trust.sqlite` and `per-project/grant-journal.sqlite` are **separate files**, no cross-database atomicity | `lifecycle-carrier.contract.v2.json` `database` (l.23–37) | pinned; `status: PROPOSED-DESIGN-CARRIER-V2…` — it is the only path owner, but it is not an accepted contract |
| Trust store | "its own SQLite database `trust.sqlite` at the install root … separate … so lifecycle restore cannot carry trust state" | `security-completion.v1.md` §5.1 l.452 | historical lineage (v8 §5.1 "as v2") |
| Namespace directory | `<host-owned project-state-root>/projects/<N>/`, `N` = canonical lowercase UUIDv4 from the registry; `projectKey` "NEVER interpolated into filesystem paths"; created exclusive/no-follow/0700 under the fence, dir+parent fsync **before** the registry commit; an existing directory is never adopted | same contract `projectRegistry.locator/newRoot/namespaceCrashCleanup` (l.193–199) | as above |
| `project-state-root` concretely | the foundation model addresses per-project host files as `host/projects/{namespace}/permission-policy.json`; v8 §8 l.517: `projects/<namespaceId>/spawns/<spawnId>/` "(the foundation's layout)" | `host-foundation-model.v2.py` l.167; v8 l.517 | consistent with `<installRoot>/host/` being the project-state-root, but **no sentence says so** |
| Grant journal | `…/projects/<N>/grant-journal.sqlite` | contract locator | as above |
| Project leases | `<namespace>/writer.lease` (LOCK_EX\|NB), `<namespace>/readers.lease` (LOCK_SH\|NB; EXCLUSIVE = LOCK_EX\|NB) | S7 l.771–772, l.854–856; model l.1850–1851 | current, prose = model. `<namespace>` itself is not defined there |
| Namespace identity | "A private namespace UUID is an operational storage locator, bound one-to-one to ProjectId; it does not enter semantic identities" | identity §2 l.44–46 | current |
| Store instance marker | `storeInstanceId` (hex32) "persisted in that store's own root before the store is first published, and never rewritten"; three-way marker observation | S9.3 l.1810–1830; `store-instance-lineage.v1.json` `identityAndMarkers` | "proposed, not accepted" in its own heading |
| Ledger ↔ store | association PK `(storeGenerationDigest, namespaceId, executionId)`; `storeGenerationDigest = SHA-256(canonical{schemaVersion, namespaceId, storeInstanceId, storeGeneration, stateSchema})`; "a receipt … sitting under a different store generation is detected" | `commit-recovery-plan.v1.json`; lineage `canonicalDigestRecipe`; `attempt-custody.schema.v1.json` l.190–194 | current |
| Carrier identity | `journalCarrierDigest` = "Existing journal projectKeyDigest from the security-owned carrier binding, **not a hash of a caller-supplied path**" = witness and `CarrierHighWaterV1.projectKeyDigest`; carrierFormat is deliberately **not** in the store binding | plan; `carrier-dispatch.v3.json` carrierJoinNotes; lineage `axisSeparation` | current |
| Witness | one per carrier, names `(projectKeyDigest, grantGeneration)`, "Witness generation never decreases"; exact-bytes private operational **file** | v8 §5.4; S7.1 l.923–940; S2.1 l.118–133 | current; **no path** |
| Floors | "keyed by `(projectKeyDigest, grantGeneration)`… Retain one bounded record per observed generation… **Store migration/rollback copies this collection forward; lifecycle rollback or backup cannot reset it**"; "per-carrier/per-generation SC-TRUST floor" files; absence ≠ zero | S7.1 l.941–950; S2.1; readonly l.535–539 | current; **no path** |
| Trust floors (six `FLOOR_KEYS`) | migration copies forward, rollback takes max, never lowered except S4.5; excluded from lifecycle backup/generation rollback | v8 §5.5; lineage `floorsAndAuthority`; 186 protocol | current |

Superseded history to avoid reviving: v1 l.450 says SC-TRUST is "included in the install-root backup" — v8 §5.5 excludes trust floors. v1's "SC-TRUST high-water **witness** `{project, grantGeneration, lastSeq, tailSha256}`" (l.541) is what is now the **floor** (`CarrierHighWaterV1`, renamed `projectKeyDigest`, carrier-format l.669–676); v8's write-ahead *witness* is a different object. The two words swapped meaning between v1 and v8.

## 2. What is missing

1. **`<namespace>` and `<host-owned project-state-root>` are never equated**, with each other or with `<installRoot>/host/projects/<N>`. Three owners each name a piece.
2. **No store-root location law at all**: where instances live, what the marker file is called, how "publish/rename the target root" (186 protocol) relates siblings.
3. **No ledger path**, and no sentence that the ledger is inside the selected store instance — it follows from the binding (rows are "under" a store generation) but is not said.
4. **No witness path.** Carrier-format l.672 says "the witness beside it" in passing; nothing normative.
5. **No floor path, and an open ownership question**: S2.1 calls the floor a *file*; v1/v8 call it SC-TRUST state (`trust.sqlite`). Both cannot be the physical truth.
6. **The per-generation floor collection has no store-transition recovery law.** 186's prepared image is "exactly FLOOR_KEYS" (six trust counters). S7.1 says the transition "copies this collection forward", but no image, equality rule or table row covers a crash mid-copy of the collection. This is a protocol gap that a layout merely exposes.

## 3. The constraints that decide the layout (each from an existing law)

**Lease domain vs store transitions ⇒ leases outside every store.** S7's core-transition set takes EXCLUSIVE on every registered namespace "in namespace-locator byte order" and journals that exact set *before* the target store exists; the fence and leases are then held across `publish target root → publish pair`. A lease file inside a store root would be a different inode in source and target: at publication a process still on the old closure handle (S9.2 lets existing processes keep theirs) and one on the new would hold "the same" lease on two inodes. The lease identity must therefore be the registry's namespace directory, which no store transition renames. That is exactly where S7 + the contract put it.

**Carrier digest/generation ⇒ one journal per namespace, outside every store, never per generation.** (a) `journalCarrierDigest` is a function of `projectKey` only; (b) the ledger's unique key `(journalCarrierDigest, grantGeneration, journalSeq)` and "witness generation never decreases" make `grantGeneration` a row axis inside one carrier; (c) carrierFormat is kept out of the store binding so that carrier migration never changes a `storeGenerationDigest`. If the journal lived inside a store, `store rollback` would re-select an *older journal* while the floors are carried at max — every ancestor re-selection would then be "project rollback below an observed floor" and quarantine. The law only works if the journal (and its witness, which must reconcile against that tail) is store-independent. The contract's locator already says so.

**Floors retained outside rollback ⇒ trust-owned, monotone across instances, never under anything a lifecycle backup/generation rollback restores.** Two compatible readings exist: *(A)* one install-level trust-owned collection that no store owns — then "copies forward" is vacuous but harmless; *(B)* a trust-owned subtree inside each store instance, copied forward by migration and max-merged by rollback — this is what "Store migration/rollback copies this collection forward" and the per-store source/target floors of the 186 protocol literally describe. **I recommend (B) only if gap 6 is closed in the same owner; otherwise (A)**, because (A) has no crash window to specify: the collection is simply never touched by a store transition, and S7.1's "never lowers … never overwrites a different generation" is enforced at one place. Owner decision; both respect v8 §5.5.

**Ledger ⇒ inside the selected store instance, per namespace.** Follows from the association PK and from S7 locking all namespaces exactly when the schema changes or a store is re-selected.

## 4. Minimal compatible relative layout (proposal for the missing roles only)

```
<installRoot>/                                   existing (foundation)
  lifecycle.fence                                existing S7
  lifecycle.sqlite   trust.sqlite                existing names (contract / v1 §5.1)
  host/                                          = <host-owned project-state-root>   ← NEW sentence only
    projects/<N>/                                = S7 <namespace>                    ← NEW sentence only
      writer.lease  readers.lease                existing S7
      grant-journal.sqlite (+ -wal, -shm)        existing contract; 197 WAL profile
      grant-journal.witness                      NEW: fixed sibling name; S2.1 bytes
      [reading A] floors/<G>.floor               NEW: G = canonical decimal 1..2^63-1
  stores/                                        NEW
    <storeInstanceId>/                           NEW: hex32 = the marker value it must contain
      store-instance.v1                          NEW name for the S9.3 marker (S2.1-style exact bytes)
      projects/<N>/ledger.sqlite (+ -wal, -shm)  NEW
      [reading B] trust/journal-floors/<projectKeyDigest>/<G>.floor
    .staging/<executionId>/                      NEW: the 186 forward carrier before publication (rename within stores/)
```
Notes: (i) the directory *name* `<storeInstanceId>` is a locator, never the identity — S9.3 requires reading the marker, and "a directory called final … is not progress proof" (186 reference docstring); require name == marker and treat inequality as `unreadable`. (ii) Under reading A the floor path needs no `projectKeyDigest` component because `<N>` ↔ ProjectId ↔ projectKey is one-to-one; the file *content* still carries both key members and S7.1 requires validating "both key/member bindings" — the path never substitutes for that. (iii) Nothing here is public identity: `N`, `storeInstanceId`, digests and `G` are all existing private values; no new schema member, no historical schema touched. (iv) Rename-publication requires `.staging` and the final root on one filesystem — this ties to the owed local-filesystem admission.

## 5. Why the path constructors cannot cross namespaces or store instances

1. **Closed component grammars, no free strings.** Only four variable components exist: UUIDv4-lowercase, hex32, hex64, canonical decimal. Each is one `Normal` component by construction; none can contain `/`, `.`, `..`, NUL or case variants. `projectKey` has no constructor into a path (contract: never interpolated).
2. **Values come only from admitted handles, never from requests.** `N` from the registry row matched while the root binding is verified; `storeInstanceId` from the admitted installation pair *and* re-read from the marker through the retained store directory; `projectKeyDigest`/`G` from the admitted witness/association. Readonly l.398 already says "never derive that binding from request fields".
3. **One namespace value feeds every leg.** A `NamespacePaths` value is built once from one admitted `N` and yields the lease, journal, witness and (with a store handle) ledger locations; there is no API taking two namespace arguments, so lease-of-A with ledger-of-B is unrepresentable. It should be obtainable only from the lease guard (lifecycle's `SuppliedLeaseDomain{install, namespaces}`), which is the planned `lifecycle→storage` edge from 195's build plan.
4. **One store handle feeds the ledger leg**, created only from the selected pair (or, in S9.2.1 recovery, from the journal's source/target pair), and validated by marker read. A retained sibling instance at the same numeric generation has a different hex32 and therefore a different directory and a different `storeGenerationDigest`; the association join (`binding-unusable`) is the second, independent check.
5. **Descriptor-relative, not string-relative.** Build with `openat` from retained directory handles (`RetainedDirectoryPath`, 191/193) so the S7 operational-chain predicates and the 195 before/after rechecks apply to the same objects the names resolved to; a constructor returning a `PathBuf` for SQLite is unavoidable (B-7), so it must be recheck-bracketed as 195 §2 prescribes.
6. **No enumeration as authority.** S7 forbids deriving the namespace set "from user input or a directory listing"; the same must hold for `stores/` — GC census may list, selection may not.

## 6. Genuine owner decisions (not mechanism)

- **Q1** equate `<namespace>` = `<host-owned project-state-root>/projects/<N>` = `<installRoot>/host/projects/<N>` in one current owner (S7 is the natural place), and cite the contract rather than restating it. The contract's standing is PROPOSED; decide whether the current owner adopts the locator or merely references it.
- **Q2** floor placement A vs B, together with gap 6 (collection copy across a store transition: image, equality, crash rows).
- **Q3** floor physical form: S2.1 "file" vs SC-TRUST `trust.sqlite` table. S2.1 is the later, current text; if files win, say that `trust.sqlite` does not hold them.
- **Q4** marker file name/bytes and "directory name == marker" rule (S9.3 is itself still "proposed, not accepted").
- **Q5** witness sibling name; whether the witness is covered by the 197 SHARED-READ effect paragraph (it is a plain file — no engine side effects — so it should stay strictly write-free for readers).

Mechanism work that can proceed without these: typed component newtypes and grammar tests; `NamespacePaths` from one `N`; marker reader with three-way observation; refusing name≠marker.

## 7. Limits
Searched the 197 tree only (docs under `coop/completion`, `coop/design-corrections`, `v2`); historical review archives deliberately not consulted, per request. I did not read product source for this note, so nothing here says what the Rust crates currently do. The layout is a proposal for root to reconcile, author and freeze; I will review the frozen bytes independently and this note is not acceptance of them.
