# Proposal assistance — 186 Q1: store-changing core operations, and `old.present=false`

Reviewer: Claude. 2026-09-19. **Assistance only** — not a frozen-byte review, not acceptance, no implementation or cumulative approval. No candidate, frozen, selected or repository file was edited; no 185/186 draft was inspected. W ordering and last-floor-write-before-image are treated as the owner's *proposed*, unaccepted choices.
Tree: my verified 181 extraction (`claude-phases181-20260919-r1/…/candidate`). "S&L" = `docs/v2/contracts/product-v1/security-and-lifecycle.md`; "lineage" = `docs/v2/architecture/store-instance-lineage.v1.json`; "model" = `security_lifecycle_model_v1.py` (byte-identical since 175). Line numbers are in that tree.
Evidence: `claude-out/q1_probe.py` → `q1_probe.txt` (real, unchanged writer model).

## 0. Answer

**Neither exists coherently.** The owners give two incompatible answers, and no owner states a distinct, safely ordered selection law for core operations:

- The **lineage owner** says a schema-raising `core-update` *is* the S9 store transition: it is listed under `forward-selection` with `"physicalStore": "a new store is materialized and the predecessor is fenced RESTORED per A5"`.
- The **writer model, S9.2 and an owner vector** say every core operation is journal-only: at `PREPARED` it aborts "because the published generation was never selected", with no footprint consulted.

If both are true, the model ABORTs a schema-raising `core-update` whose old store is already fenced — the same defect as 181 F-1, for a second family of operations. A third, separate contradiction concerns `store-rollback` (§2, C3), which affects my own 186 table.

## 1. What each owner says (citations)

| # | Owner | Statement |
|---|---|---|
| a | S&L S9.2 l.1428–1433; lineage A4 | `core-update` "never lowers the schema, selects a new store generation exactly when the schema changes"; `core-rollback` "never raises the schema" |
| b | S&L l.1443–1452 (pair law); lineage A4b | for **both** core-update and core-rollback a changed schema selects a different store (`TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE`); "the S9 footprint above already owns the re-selection of a retained store" |
| c | lineage `nodeWritingRule.cases` | `forward-selection`: operations = `store-migrate`, **"core-update with a raised schema"**; fixtures `intentStoreMigrate (3,1)->(4,2)`, `intentUpdateSchemaChange (3,1)->(4,2)`; physicalStore = "a new store is materialized and **the predecessor is fenced RESTORED per A5**". `ancestor-reselect`: `store-rollback`, **"core-rollback with a retreated schema"**; "the retained predecessor store is re-opened" |
| d | lineage `nodeWritingRule.principle` | "The selection case is a pure function of the ADMITTED intent and never reads the stored node set" — selection by the pair law, not by operation name |
| e | lineage `floorsAndAuthority.authorizedTransition` | names all five operations and applies A5 to them: "a migration COPIES THE FLOORS FORWARD into the new store; a rollback … sets them to the MAXIMUM of both stores" |
| f | S&L S7 l.811–819; model `core_transition_affected_namespaces` | every registered namespace is leased "when the from/to state schema differ or a store is re-selected" — so a store-changing core operation already takes the *store* lock set |
| g | model `STORE_OPERATIONS = ('store-migrate','store-rollback')`; `recover_transition_journal` | the footprint is consulted only for those two names; any other operation at `PREPARED` → ABORT |
| h | S&L S9.2 crash-recovery paragraph (l.≈1485); lineage A6 and `recoveryTotality.ownerPrecedenceAtPrepared` | "a core operation aborts (the published generation was never selected; GC census reclaims it)" |
| i | owner vector `crash-at-prepared-core-update-aborts-the-unselected-generation` | uses `journal_UpdateSchemaChange_prepared` — a **schema-raising** core-update — with no footprint, expecting ABORT |
| j | S&L S9 bridge l.1083–1095 | ordered release: the stage-2 core ships under the schema-1 catalog so installs update "by its ordinary path" (same schema); "(4) state migration 1→2 runs under EXCLUSIVE" as its own step. Only a stage-2 core has `state-decoder.v2` (writer) |
| k | S&L S15 l.≈2280 | "Schema transition requires the reader-first stage and profile binding from S9; rollback preserves maximum observed trust/revocation floors" — said of the core commands |
| l | model `migrate_floors` | returns `oldStoreMark='RESTORED'` and `downgradeNoReturn`: "after commit the stage-1 core observes RESTORED and refuses" — the fence is what protects against an older core reusing the old store |

## 2. Exact contradictions

**C1 — (c) vs (g,h,i).** Probe §A/§B: `intentUpdateSchemaChange` is a `forward-selection` by the pair law, yet the footprint is not consulted for it. `journal_UpdateSchemaChange` at `PREPARED` with the **old store already fenced `RESTORED`** and the new store `PREPARED` → **ABORT**; at `COMMITTED` with an unfenced old store and no new store, or with `both` → RESUME-COMMIT. The rationale in (h) — "never selected; GC reclaims it" — is true of a *core closure generation* and false of a fenced store. Either (c) is wrong about the fence, or (g,h,i) are wrong about the abort.

**C2 — no ordering law for the two selections.** A schema-raising core-update selects a new core closure **and** a new store under one journal with one `COMMITTED`. No owner says which switch happens first, or which of them is the point of no return. (l) implies it must be the store fence (it is what stops the old core reusing the old store). (j) adds a feasibility constraint nobody states: the process performing the transition must be able to *write* the target schema, so a stage-1 core cannot execute a schema-raising core-update at all — which is exactly why the bridge orders "update core, then migrate".

**C3 — `store-rollback` is routed to a table that cannot describe it.** It is in `STORE_OPERATIONS`, but (c) says it *re-opens a retained store* and writes no migrating root, while `migration_recover` only knows `old.unbootstrappedReason` and a `new` migrating/final root. Probe §C, `journal_StoreRollback` at `PREPARED`: nothing migrating → **QUARANTINE**; retained target still marked RESTORED → QUARANTINE; no footprint → QUARANTINE; and with the *forward* store `final` (i.e. the ordinary state of the store being rolled back **from**) → **RELEASE-ONLY → DONE**, declaring the rollback complete because a forward migration once completed. So a crashed store-rollback is either unrecoverable or wrongly finished; there is no owner vector for it (the 11 recovery vectors contain no rollback). The same applies to a schema-retreating core-rollback under any fix of C1.
**This limits my 186 table:** it was derived from the forward-migration sequence only. It is a table for `forward-selection`; it must not be applied to `ancestor-reselect`.

**C4 — (f) vs (g).** The lock set is already decided by the pair law ("schema differ or store re-selected"); recovery is decided by operation name. Two classifiers for one property.

## 3. Options

| | Decision | Consequence |
|---|---|---|
| **O1 (recommended)** | One store-selection protocol, chosen by the **selection case of the journaled intent** (pair law: same-store / forward-selection / ancestor-reselect), never by operation name. A core operation whose case is not same-store embeds that protocol; the store fence is the single point of no return for the whole transition; the core-closure switch happens only after the store is `final` (forward) or re-selected (ancestor), idempotently, inside RESUME-COMMIT | Aligns (c)(d)(e)(f)(l) and S15 (k). Reuses an existing principle — (d) — instead of inventing one. Replaces `operation in STORE_OPERATIONS` with the case function the lineage companion already has. Core operations that are same-store keep today's journal-only table unchanged (that is where "never selected; GC reclaims it" is true). Vector (i) must gain a footprint: with an unfenced old store its ABORT expectation is preserved |
| O2 | Forbid store-changing core operations: `core-update`/`core-rollback` must keep schema and store; schema moves only through `store migrate|rollback` | Simplest physics and matches the bridge (j). But contradicts (a)(b)(c)(k), changes `admit_transition_intent`, and `intentUpdateSchemaChange` is the base fixture of most journal vectors and of the three-namespace lease cases — the most invasive option for the reference, and S15 plainly intends core rollback to carry a schema retreat |
| O3 | A distinct law for core operations: fence the old store only **after** `COMMITTED` | Makes (h) true, but creates a second physical protocol for the same act with the opposite fence/commit order, contradicts (c)'s "per A5" and S9's sequence, and doubles what the host must qualify. Not minimal |

**Recommendation: O1**, with three sentences the owner must add whatever else is chosen:
1. *Executor capability:* the executing core must hold a writer for the target schema (forward) or a reader for it (ancestor); otherwise the intent is refused at admission, before any journal. This turns (j) from folklore into law and explains when a combined transition is even possible.
2. *Single commit point:* for a non-same-store transition the store fence (forward) — or its ancestor equivalent, §4 — is the point of no return; the core-closure selection is completed after it and is never a reason to abort.
3. *Ancestor re-selection needs its own footprint vocabulary* (§4); until it exists, recovery of a crashed rollback is honestly "unknown custody", not QUARANTINE-as-corruption and never RELEASE-ONLY.

## 4. What an ancestor-reselect footprint has to say (sketch for the owner, not a design)

From (c)/(e)/A5: the retained target store exists throughout and carries `RESTORED`; the forward store is the one being left; floors become max(both); no store is created or renamed. The observable facts are therefore: is the target's `RESTORED` mark cleared; is the forward store fenced (it must be, or a newer core could keep writing it — the mirror of (l)); is the prepared max-floor image present and matching. The point of no return is the analogue of `RESTORED`: fencing the forward store. Everything in my 186 proposal about precedence, the wrapper observation, the image equality check and the totality sweep carries over; the *cells* do not. S9's "it refuses when the new store accepted a root the old core cannot verify" is, as 181 decided for the forward case, a pre-fence refusal.

## 5. `old.present = false`: three different things, not one

Probe §D: the member is carried in every footprint and **read by nothing** (0 of 48 states change). The lineage owner already has the right vocabulary for store-root observations (S&L S9.3 l.≈1768–1777): "exactly one of: a **readable** identity; **absent**, meaning no store root is present; or **unreadable**… An unreadable marker is never treated as absence, and an absence must be observed, never inferred from a missing observation. **The store a transition comes from always exists, so its marker is always required.**" Applying that:

| Observation of the *from* store | Meaning | Disposition |
|---|---|---|
| could not be observed (I/O, permission, unreadable root/marker) | **unavailable custody** | wrapper `('unavailable', None)` → stop `unknown-custody`; writer model not called; nothing inferred |
| observed **absent** while a journal for it is active | **proven contradiction** | QUARANTINE `MIGRATION.CORRUPT` in every journal state |
| observed present | proceed to the table | — |

Why observed absence is a contradiction and never lawful lag: the only lawful deleter of a retained old store is the GC census after the rollback window; `store-gc` is a *nonexecuting mutator* in the 181 companion, which requires confirmed active-slot **absence** — so GC cannot run while any journal, even `DONE`, is active. Therefore no lawful sequence produces "active journal + from-store absent". (If the owner ever lets GC run with a terminal journal present, this row must change with it; that dependency should be written next to the rule.)
The **target** store is different and must not inherit this row: for a forward selection S9.3 already says an absent target at `LEASED`/`PREPARING`/after abort "is expected and must never be read as corruption"; after the point of no return it is a contradiction (186 table). For an ancestor re-selection the target is a retained store and is required in every phase.
So: keep `present`, but make it three-valued and per-store — `fromStore: present|absent|unobservable`, `targetStore: …` — rather than a boolean on `old`. A boolean cannot express "unobservable", and collapsing unobservable into `false` would turn an I/O error into a corruption verdict; collapsing it into `true` would let recovery act on a store nobody saw.

## 6. Tests this implies (each fails today)

1. `core-update (3,1)->(4,2)`, `PREPARED`, old `RESTORED`, new `migrating/PREPARED` → RESUME-COMMIT (or, pre-decision, anything but ABORT); today **ABORT**.
2. Same journal, `COMMITTED`, old unfenced + no new store → QUARANTINE; today RESUME-COMMIT.
3. Same-store `core-update`/`core-repair`/`core-rollback` at `PREPARED` → ABORT, footprint not consulted (**control: unchanged**).
4. `store-rollback`, `PREPARED`, forward store `final` and target still fenced → must **not** be RELEASE-ONLY/DONE; today it is.
5. `store-rollback`, `PREPARED`, nothing migrating → must not be `MIGRATION.CORRUPT` merely because no migrating root exists; today it is.
6. From-store observed absent, any state → QUARANTINE; from-store unobservable → `unknown-custody` with the model not called; both distinct from present (today all three are indistinguishable).
7. Classifier agreement: for every admitted intent, "recovery consults a store protocol" ⇔ `core_transition_affected_namespaces` reports a store re-selection or schema change ⇔ lineage selection case ≠ same-store (closes C4 mechanically).

## 7. Limits

I read S9, S9.2, S9.2.1, S9.3, S7, S15, the lineage companion's anchors/cases/floors/recovery sections, and the model's intent, affected-namespace, recovery and floor functions. I did not find any physical description of how a core-closure generation is "selected" (the switch itself), so C2's ordering is argued from (l), not from an owner of that act — if such an owner exists outside these files, it should be cited in 186. §4 is a sketch from prose; I did not model it. No approval of any kind is implied.
