# Bounded assistance — physical locations for the transition roles 201 left unplaced

Reviewer: Claude. Date 2026-09-19. **Assistance only**: not a frozen review, not approval of any draft (202 not inspected), no implementation. Sources: my verified 201 extraction only (`claude-reference201-20260919-r1/…/candidate/docs`) — `security/store-transition-protocol.v1.md` incl. corrections 188/190 (below "STP"), `security-and-lifecycle.md` S7/S9.2/S9.2.1/S9.3 ("S&L"), `physical-store-layout.v1.md` ("PSL"), `store-instance-lineage.v1.json`, `security-lifecycle.schemas.v1.json`, `lifecycle-carrier.contract.v2.json`, `commit-recovery-readonly.v3.md`. One read-only look at my verified 200 product tree to check that no selection carrier already exists. Searches saved in `claude-out/io/`.

## 1. What existing law already fixes (before choosing any name)

| Topic | Existing rule | Owner |
|---|---|---|
| Records are immutable shapes | journal = exactly **20** members, intent = **11**, binding `ActiveTransitionBindingV1` = `{executionId, journalRef}`; "This statement does not silently add a field to the public journal schema" | schemas `/schemas/*`; STP l.207 |
| Journal identity | `journalRef` = `security.installation-transition-journal.v1:` + identity over the **whole** journal, *state included* ("Journal identity includes state") — so it changes on every revision | model l.2541; STP corr.190 |
| Journal+binding | "Every journal state change … publishes the journal and its original-execution/current-journal binding as **one atomic, durably confirmed carrier revision**. Separate durable writes are forbidden"; mixed ⇒ every executor incl. terminal cleanup stops `unknown-custody`; no retry guesses or repairs | STP corr.190 |
| One slot | "one active transition slot, not the set of retained historical journals"; retirement makes **absence durable** under the same held fence; "Retained historical bytes and `journalRef` may live outside the active slot, never as a fallback for an absent active slot" | S&L l.1569–1584 |
| Selection | "one atomically published, durably confirmed **pair**: core closure plus full store binding (storeInstanceId, storeGeneration, stateSchema)… observed as exactly the journal's source pair, target pair, or contradictory"; "a partial observation is unavailable, never an inferred pair" | STP l.30–39 |
| Order | `jLEASED → jPREPARING → carrier staged-empty → PREPARING → PREPARED → jPREPARED → last S4 check/floor write → prepared image durable → source fenced by this execution → carrier COMMITTED → jCOMMITTED`; forward: publish root → publish pair → lineage → jDONE; ancestor: apply image to retained target → carrier COMMITTED → jCOMMITTED → publish pair → remove carrier → lineage → jDONE; same-store: jCOMMITTED before pair | STP l.76–95, l.186–192 |
| Source fence | "Its durable record and source trust fencing must have **one recoverable commit boundary**"; "Each store has one current private source-fence attribution slot", initialised `observed-none` at creation, survives DONE/PRESENT, superseded only by the next transition fencing this store as source; unavailable ≠ observed-none; "No opportunistic on-read initialization" | STP l.81–84, corr.188 |
| Image | "exactly FLOOR_KEYS, original ExecutionId, intentDigest and target store generation"; "Once the target is published and its floors are durable, cleanup does not depend on retaining the temporary image" | STP l.127–136 |
| Carrier | states absent/staged-empty/PREPARING/PREPARED/COMMITTED/(forward) published; "own immutable binding must match this original execution/intent"; abort deletes only it; "A caller cannot nominate an arbitrary deletion path"; ancestor = "a separate small staging carrier", never the retained store | STP l.67–72; PSL boundary |
| Lineage | private append-only `StoreLineageNodeV1`, PK = full triple; **"does NOT claim that the public journal record and a private node commit atomically"**; written after jCOMMITTED, forward case only; undetermined barrier ⇒ reconcile: absent → write, byte-identical → done, different → quarantine | lineage `durabilityAndReconciliation`, `privateCompanionSchema` |
| Pre-admission reads are write-free | "Installation registry/trust/**transition** observations before the lease retain their separate write-free admission law; this exception grants them no SQLite side effects"; PSL: `lifecycle.sqlite` has "no pre-admission reader-write exception" | readonly §2; PSL table |
| No cross-file atomicity anywhere | contract `crossDatabaseAtomicityClaim: false`; PSL "no claimed atomicity spans the journal, high-water files, lifecycle or evidence ledger" | contract; PSL |
| Nothing selected yet | the product lifecycle crate is `leases.rs`, `lib.rs`, `locations.rs` — the inventory's `installation.rs` does not exist; the historical contract's `project_selection`/`transition` tables describe per-project **component-generation** selection with another state machine, and PSL says adopting its locator "does not revive" that protocol | 200 product tree; contract; PSL |

**Decisive consequence of the write-free row:** the active slot and the selection pair are read by *every* command before any lease (S9.2.1 observers, report-only surfaces). A WAL SQLite table would make those reads create sidecars. So both must be **plain single files**, replacement-published. That also happens to be the only honest way to get 190's atomicity: one rename of one file.

## 2. Proposed minimal layout (all relative to `I`; all outside every store and outside `host/projects/N`)

```
transitions/
  active.slot                 ActiveTransitionSlotV1 — journal + binding, ONE file            (§3)
  retired/E.slot              optional retained terminal revision, E = original ExecutionId  (§3, Q2)
  stage/E/                    ancestor-stage carrier ONLY (forward keeps stores/.staging/E)  (§5)
    carrier.v1                TransitionCarrierV1 — state + binding, replacement-published
selection.pair                InstallationSelectionV1 — core closure + store triple, ONE file (§4)
stores/.staging/E/carrier.v1  same record inside the forward tree; travels with the rename    (§5)
stores/S/carrier.v1           = the above after publication (state `published`)
stores/S/source-fence.v1      SourceFenceAttributionV1 — the store's single current slot     (§6)
stores/.staging/E/floor-image.v1  |  transitions/stage/E/floor-image.v1   PreparedFloorImageV1 (§7)
lineage.sqlite  or  transitions/lineage/<S>-<G>-<schema>.node   StoreLineageNodeV1            (§8, Q4)
```
Component grammars reuse 200's parsers (E, S, canonical decimal); no new variable component kind except the lineage file name if files are chosen. No public identity, schema member, command or error vocabulary. PSL's marker and `trust/journal-floors` are untouched; the six-counter image is a different file in a different place from any `G.floor`.

## 3. Active slot: journal + binding as one revision

**Wrapper (private, product-canonical, raw bytes == canonical(decoded), like the marker):**
`ActiveTransitionSlotV1 = {"slotSchema":1,"executionId":E,"journalRef":R,"journal":{…the exact 20 members…}}`
- The 20-member record is embedded **verbatim as a value**; nothing is added to it. `executionId`+`journalRef` *are* `ActiveTransitionBindingV1`'s two members, lifted unchanged.
- Admission recomputes `R' = domain + identity(journal)` from the embedded journal and requires `R' == journalRef`, then projects the binding. A stored-but-redundant `journalRef` is deliberate: it is what makes 188's "projection is checked against the canonical journal identity" a real check that catches a wrapper assembled from two revisions, rather than a tautology.
- **One publication boundary:** write `active.slot.tmp-<E>` (exclusive, no-follow, 0600) → fsync file → `rename` over `active.slot` → fsync `transitions/`. A crash leaves either the old complete revision or the new complete revision; there is no state in which journal and binding come from different revisions *by crash*. That is the whole claim; nothing about two files is asserted.
- **Old mixed or foreign states fail unavailable:** unparsable/non-canonical/oversized bytes, `R' != journalRef`, `executionId` failing the grammar, a leftover from a split-file prototype (journal file without wrapper, or wrapper without journal) ⇒ *unavailable* ⇒ `unknown-custody`, including for ABORTED/DONE cleanup (corr.188). Never "absent", never repaired, never re-derived from `retired/`. Causal uncertainty stays: a slot that cannot be admitted blocks registration and mutators exactly as S&L l.1576–1580 says.
- **Undetermined barrier** on the rename or directory fsync (A10): refuse every further effect; next fence re-reads. The observed revision is whichever complete file is there; the state machine tolerates both because each journal step "follows completed facts".
- **Temp files:** `active.slot.tmp-*` are never read as evidence. Only the fence holder may remove them, and only ones whose `<E>` equals the admitted slot's original E or when the slot is confirmed absent; otherwise leave them (Q5).
- **Retirement:** absence must be durable ⇒ `unlink(active.slot)` + fsync dir. If history is retained (Q2): first *copy* the terminal bytes to `retired/E.slot` (exclusive create, fsync file+dir), then unlink. **Not a hard link** — 198/200's operational-file predicate refuses `links != 1`. Crash between the two: both exist; the executor sees an active terminal slot, re-runs retirement; an existing `retired/E.slot` must be byte-identical (done) or the retirement stops unavailable. `retired/` is never consulted to fill an absent slot (S&L l.1582).
- **Bound:** the journal embeds `registry` and `leaseSet` for *all* namespaces, so its size is not constant. Pick a cap (S2.1's 4 MiB loader bound is the natural existing number) and enforce it at **admission of the intent, before jLEASED is written** — a transition that could not be journaled must refuse before it has any effect, not fail to publish mid-way.

## 4. Installation selection pair

`selection.pair`: `InstallationSelectionV1 = {"selectionSchema":1,"coreClosure":…,"storeInstanceId":S,"storeGeneration":n,"stateSchema":k}` — private, canonical, one file, same temp→fsync→rename→fsync-dir publication. The atomic *pair* of STP l.30 is then literally one rename: "no new core/old store mixed selection is exposed" holds by construction.
- Observation is three-valued against the admitted journal: equals source pair / equals target pair / **anything else = contradictory** (⇒ the protocol's QUARANTINE row) ; unreadable/non-canonical/missing-while-a-store-exists = **unavailable**, "never an inferred pair".
- Identity never comes from this file alone: `S` must equal `stores/S/store-instance.v1` and the five-member binding must match (PSL).
- First installation: the creator publishes `selection.pair` last, after the first store root and marker are durable. Absent `selection.pair` with no `stores/` entry is first use; absent with any store present is unavailable, not first use (mirrors PSL's marker rule).
- **No atomicity with the slot is claimed or needed.** STP already orders them as separate durable steps (forward: root published → pair → lineage → jDONE; same-store: jCOMMITTED → pair) and the table has rows for each side of each gap (`COMMITTED/this/source/published` → publish pair; `COMMITTED/this/target/…` → finish).
- If a core-closure selection carrier already exists in a distribution owner I did not have in this tree, the pair must **subsume** it, not sit beside it — two carriers re-create exactly the "two-selection ambiguity" STP l.35 closes (Q1).

## 5. Carriers and their state/binding record

One record type in both cases: `TransitionCarrierV1 = {"carrierSchema":1,"executionId":E,"intentDigest":D,"case":"forward"|"ancestor","state":"staged-empty"|"PREPARING"|"PREPARED"|"COMMITTED"|"published"}` at `<carrier root>/carrier.v1`, replacement-published per state change (one file ⇒ state and binding cannot disagree).
- **Forward:** carrier root = `stores/.staging/E/` (PSL, unchanged). The record sits *inside* the tree, so when the root is renamed to `stores/S` the binding travels with it — this answers my 199 W-1 point that after publication the path no longer carries E. STP treats publication as a durable fact the journal follows, and its observation vocabulary has both COMMITTED and published for the forward carrier. Observe `published` as **location**, not as a byte: `carrier.v1` state COMMITTED found under `stores/S/` (marker == S) ≡ published; found under `.staging/E/` ≡ COMMITTED. Then no write is needed across the rename and no window exists where bytes say one thing and the directory another. (If the owner prefers an explicit byte, it must be written after the rename and the pre-write window defined as COMMITTED-at-final-location ≡ published anyway.)
- **Ancestor:** carrier root = `transitions/stage/E/` — outside `stores/`, so it can never be mistaken for, renamed into, or deleted as a store; "never repackages or renames the retained ancestor store" holds structurally. `published` is not a lawful state there (STP: ancestor + published ⇒ QUARANTINE).
- **Abort target is computed, not supplied:** the only deletable paths are `stores/.staging/E` (case forward) or `transitions/stage/E` (case ancestor) for the slot's *original* E, and only after `carrier.v1` in it admits with that E and D. A directory whose record names another execution is "stage carrier does not belong to the active transition execution" ⇒ QUARANTINE row, no deletion. Absent root = `absent` with `carrierBinding` null — consistent with the reference's presence/binding check.
- **Cleanup ownership:** lifecycle (fence holder) removes the carrier root, then fsyncs the parent, *then* writes jABORTED (STP l.84–85). **A carrier root never exists without its record:** create `E.tmp-<nonce>/` beside the final name, write and fsync `carrier.v1` (state `staged-empty`) inside it, fsync the directory, then rename it to `E` and fsync the parent. Since the journal leads creation (jPREPARING precedes staged-empty), a crash leaves either no `E` (carrier `absent`, lawful at PREPARING → ABORT row) or an attributed `E`. A directory named `E` with no admissible record is therefore not a crash state of this protocol: it is *unavailable*, never `absent` and never deletable by name. `*.tmp-*` leftovers follow Q5.

## 6. Source-fence record

`stores/S/source-fence.v1`: `SourceFenceAttributionV1 = {"fenceSchema":1,"attribution":null}` at creation (= observed-none) or `{"fenceSchema":1,"attribution":{"executionId":E,"intentDigest":D}}`. Inside the store because it is *per store* and must survive retirement, PRESENT and re-selection (corr.188), and must not be reset by anything outside the store.
- **The hard part — "one recoverable commit boundary" with source trust fencing — is not solved by naming a file.** If trust fencing of the source is a row/role change in that store's trust state and the attribution is a separate file, there are two writes. Two honest options: **(a)** put the attribution *in the same carrier and transaction* as the trust-role change (then this file does not exist and the "record" is a row); **(b)** keep the file and define the boundary as the file, with the trust-role change **derived**: a store whose attribution names an execution whose journal is ≥ the fence point is fenced *by definition*, and the role write is an idempotent follow-up that recovery re-applies. (b) matches STP's own warning that "the host must not infer attribution from an unrelated trust-role update" — the attribution leads, the role follows. I recommend (b); it is a genuine owner decision (Q3).
- Unavailable (unreadable, non-canonical, **or missing in a store that has a marker**) is unknown, never observed-none — a store created before this record existed is exactly corr.188's "older carrier without an admitted attribution representation". No on-read initialisation.

## 7. Prepared six-counter floor image

`floor-image.v1` inside the carrier root (forward: `stores/.staging/E/`, ancestor: `transitions/stage/E/`): `PreparedFloorImageV1 = {"imageSchema":1,"executionId":E,"intentDigest":D,"toStoreGeneration":n,"floors":{exactly the six FLOOR_KEYS}}`. Written once, exclusive create + fsync file + fsync dir, never replaced — "prepared image durable" is that barrier, and it precedes the source-fence write.
- Living in the carrier root gives it the carrier's lifetime for free: abort deletes it with the carrier; for ancestor it goes when the stage carrier is removed after the pair is published; for forward it travels into `stores/S/` and may be deleted once "the target is published and its floors are durable" (cleanup must not depend on it — so its later absence at `DONE` is lawful and must not be read as damage).
- A second create for the same E finding an existing file: byte-identical ⇒ done; different ⇒ unavailable (the last-S4-evaluation rule means a re-preparation with other values is a protocol violation, not a refresh).
- Name and directory keep it disjoint from `trust/journal-floors/N/G.floor`; nothing in a store transition touches that collection (PSL).

## 8. Lineage table

Existing law wants append-only, PK = triple, byte-identical reconciliation, and claims **no** atomicity with the journal. It is read only by executors under the fence (not pre-admission), so SQLite is lawful here, but it buys nothing: one node per *forward selection* is a tiny, write-once set, and "absent → write, byte-identical → done, different → quarantine" is precisely exclusive-create file semantics. Proposal: `transitions/lineage/<S>-<G>-<schema>.node` = canonical `StoreLineageNodeV1`, exclusive create, never replaced; lookups by full triple are a path construction (no listing as authority). If the owner prefers the table the lineage JSON literally names (`crates/lifecycle/src/journal_store.rs` "durableRetention"), `lineage.sqlite` at `I` with 187's BEFORE INSERT no-replace guard on the PK is the equivalent (Q4). Either way outside every store — a node describes stores and must survive their reclamation.

## 9. Crash walk-through at the two boundaries asked about

| Crash point | What is on disk | Observation | Table row |
|---|---|---|---|
| during slot publication PREPARED→COMMITTED | complete old **or** complete new `active.slot`; maybe a `.tmp-E` | admits as PREPARED or COMMITTED, binding coherent either way | both have rows (`PREPARED/this/source/COMMITTED` and `COMMITTED/this/source/COMMITTED`) |
| slot file torn by media/tamper, or split prototype leftovers | non-canonical / `R' != journalRef` | unavailable | `unknown-custody`; no release, no retirement |
| during pair publication | complete source pair or complete target pair | source / target | `COMMITTED … source` → publish pair; `… target` → finish |
| pair file names neither | contradictory | QUARANTINE row | — |
| between image durable and source fence | image present, attribution old | `fence old` | ABORT rows (pre-fence); image removed with carrier |
| between attribution write and trust-role write (option b) | attribution = this E | `fence this` | never ABORT; recovery re-applies role |
| retirement copy done, unlink not | `retired/E.slot` + active terminal | active terminal | RELEASE-ONLY/retire again; copy must be byte-identical |

## 10. Genuine owner decisions
- **Q1** does a core-closure selection carrier already exist in a distribution owner outside this tree? If yes, `selection.pair` must replace/subsume it.
- **Q2** retain terminal slots (`retired/E.slot`) or not. S&L allows, does not require. Retention costs the copy step and a bound on `retired/` growth; omission loses local forensics only.
- **Q3** source-fence boundary: row-in-transaction (a) vs attribution-leads file (b).
- **Q4** lineage as exclusive-create files vs a guarded table.
- **Q5** who may delete `*.tmp-*` and unattributable stage directories (I propose: nobody automatically).
- **Q6** journal size cap and where it is refused (I propose: intent admission, 4 MiB).
- **Q7** forward `published`: location-derived (my recommendation) vs an explicit byte.

## 11. Limits
Location/atomicity proposal from owner text; nothing executed, no file-system behaviour measured; rename/fsync durability on the target file systems is the owed native qualification (PSL already requires staging and final roots on one qualified local file system — the same must be said of `transitions/` and `selection.pair` temp files, which must be created in the destination directory). I did not consult historical review archives or any draft. This note is not acceptance of whatever root freezes; I will review those bytes independently.
