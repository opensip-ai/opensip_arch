# Bounded proposal — trust continuity (closing my 206 R2–R7 under root's eight decisions)

Reviewer: Claude. Date 2026-09-19. **Assistance only**: not a frozen review, no approval; the 208 draft was not inspected. Sources read: `signed-index-trust-contract.v14.json` (SHA-256 `039a5702…6715`, verified; clauses `machine`, `offlineRunningPolicy`, `recoveryAuthorityShape`, `auditAndWaiver`, `airGapPayload`, `monotonicStore` read in full — dump in `claude-out/io/v14_clauses.txt`), `security-completion.v2.md` §4–§5.5, and my verified 201 reference tree (v8, S&L S4/S4.5/S5/S9, STP incl. 188/190, PSL). Nothing executed; no source edited.

I take root's decisions 1–8 as given and do not reopen the scalar/flag-precedence sketches: the capsule persists **event-driven state plus its retained evidence**; the 208 kernel dispatches.

## 0. One existing-law contradiction that shapes everything (flag first)

v14 defines `ST-UNBOOTSTRAPPED` as "**No accepted root/index snapshot for this role**", and builds two rules on that meaning: ordinary `EV-PRESENT-PAYLOAD` from it enters `ST-TRUSTED`, and `EV-REVOKE` from it is **refused** (`fallbackByEvent.EV-REVOKE`: "From ST-UNBOOTSTRAPPED … REFUSE stay" — nothing exists to revoke).
v2 §5.5 / v8 §5.5 / S9 / STP then *reuse the same token* for a different situation — a store that **has** accepted documents and floors but whose standing was reset: "Restoring any SC-TRUST bytes marks **every role** `ST-UNBOOTSTRAPPED` with audit reason `RESTORED`", source fencing → `RESTORED`, migration target → `MIGRATED`.
Composed literally this does two unlawful things: (a) a role in `ST-REVOKED` is reset and the next ordinary payload makes it `TRUSTED` — v14: "`ST-REVOKED` is not this member"; ordinary PRESENT from REVOKED falls to `PAYLOAD-NOT-ADMISSIBLE`; (b) while reset, a newer valid revocation is **refused**. Neither later owner says it intends either effect.
Note what is *not* a problem: `EXPIRED`, `STALE-REVOCATION` and `QUORUM-LOST` are healed by an ordinary payload anyway ("Heals the prior condition"), so resetting them to `UNBOOTSTRAPPED` changes no reachable outcome. The laundering risk is exactly **`ST-REVOKED` and `ST-RECOVERY`**.

**Proposed explicit supersession (one sentence in the current owner):** a standing reset (source fence, migration target creation, ancestor re-selection, declared trust restore) sets to `ST-UNBOOTSTRAPPED` every role **except those in `ST-REVOKED`**, which stay `ST-REVOKED`; `ST-RECOVERY` cannot be present because §4 refuses the transition; and for a role that is `ST-UNBOOTSTRAPPED` *with retained accepted documents* (reason `RESTORED`/`MIGRATED`), `EV-REVOKE` is dispatched as from a bootstrapped state (accept → `ST-REVOKED`), the v14 refusal applying only to the reason-less initial form. Visible behaviour is unchanged for users: `offlineRunningPolicy` refuses identically for `REVOKED` and `UNBOOTSTRAPPED`. This keeps event dispatch intact and needs no precedence over flags.

## 1. Capsule `I/trust/stores/S/state.v1` — exact minimal record (decisions 1, 2, 5, 6, 7)

Product-canonical, raw == canonical(decoded), one replacement-published file, read through the 205/207 retained reader. Proposed cap **16 KiB** (it is constant-size by construction: no arrays that grow with time).

```
StoreTrustStateV1 = {
 "capsuleSchema": 1,
 "storeInstanceId": S,                                   // == dir name == admitted marker, else unavailable
 "clock": { …the 11 TrustClockRecordV1 members, verbatim… },
 "heads": { "root":       { "version": n, "node": hex64 },           // → RootChainNodeV1 (§2)
            "catalog":    { "version": n, "sha256": hex64 } | null,
            "revocation": { "version": n, "union": hex64 } | null }, // → RevocationUnionV1 (§2)
 "roles": { "TR-CORE":{R}, "TR-INDEX":{R}, "TR-COMPONENT":{R}, "TR-BUNDLE":{R}, "TR-REPAIR":{R}, "TR-PROFILE":{R} },
 "eventHead": { "seq": k, "sha256": hex64 } | null,      // → last audit event that BECAME current (§3)
 "sourceFence": null | { "executionId": E, "intentDigest": D } }

R = { "state":  "ST-UNBOOTSTRAPPED"|"ST-TRUSTED"|"ST-EXPIRED"|"ST-STALE-REVOCATION"|"ST-QUORUM-LOST"|"ST-REVOKED"|"ST-RECOVERY",
      "resetReason": null | "RESTORED" | "MIGRATED",     // non-null only with ST-UNBOOTSTRAPPED; v2 calls it the *audit reason*
      "revokedBy":   null | { "revocationVersion": n, "eventSeq": k },   // set by EV-REVOKE; cleared ONLY by EV-RECOVER-COMMIT
      "quorumLostBy":null | { "eventSeq": k },                            // set by EV-QUORUM-OBSERVE; cleared by accepted ordinary PRESENT or RECOVER-COMMIT
      "ceremony":    null | { "stagedPayload": hex64, "beganEventSeq": k|null } }  // recovery-typed PRESENT stages; BEGIN sets beganEventSeq
```
- `state` is the **event-driven** state the kernel last produced; nothing recomputes it from the other members. `revokedBy`/`quorumLostBy` are *retained evidence*, there so that `EV-RECOVER-ABORT`'s `toFunction` ("first still-true candidate … else `ST-UNBOOTSTRAPPED`. Never `ST-TRUSTED`") has something to be true about after `ST-RECOVERY` has been the visible state through any number of `EV-CLOCK`s. `EXPIRED`/`STALE` "still true" is evaluated from `clock` at `tEval`; they need no evidence member.
- **Fixed closed map of six** (decision 7): a typed-absent role (S9.1: keys `[]`, threshold 0) keeps its entry, so a root rotation that deactivates a role cannot drop its `revokedBy`. The kernel dispatches no TRUSTED-entry for a role the *currently admitted root* does not activate; absence is read from the root, never stored. No `ACTIVE` flag is persisted: v14's `TRUSTED-entry ACTIVE/INACTIVE` is a property of the code/profile + signature admission in the running core (v2 §2.3 "Activation"), so it gates the kernel call, not the record.
- **Two recoveries stay apart**: `clock.pendingRecoveryChallenge` + `clock.recoveryEpochSerial` are S4.5's clock-floor challenge (S&L l.470–506: "Counters, revocation entries, **role states** … are untouched"); `roles.*.ceremony` is v14's root-recovery ceremony. A migration nulls the former (model l.2293) and must not touch the latter.
- Invariants checked at admission of the capsule (any failure ⇒ **unavailable**, never repaired): `heads.root.version == clock.rootVersion`, likewise catalog ↔ `indexSnapshotVersion`, revocation ↔ `revocationVersion`; `resetReason` null unless state is UNBOOTSTRAPPED; `ceremony.beganEventSeq` non-null iff state is `ST-RECOVERY`; `revokedBy` non-null if state is `ST-REVOKED`; every `eventSeq ≤ eventHead.seq`.
- Writers (all under the installation fence): `republish(prev, kernelOutcome)` cannot reach `sourceFence`; `fence_source(prev, E, D)` is the only setter and performs the standing reset of §0 in the same revision (decision 1).

## 2. History without an unbounded rewritten array (decision 5)

All under `I/trust/` as immutable, content-addressed, exclusive-create files; **looked up only through a reference held by an admitted capsule or node — never by listing** (PSL: a listing is never selection).

| File | Record | Read bound |
|---|---|---|
| `documents/<sha256>` | exact accepted signed document bytes | existing 4 MiB metadata bound |
| `nodes/<sha256>` `RootChainNodeV1` | `{nodeSchema:1, version:n, document:hex64, prev:hex64\|null}` | < 256 B; **authority reads exactly one node** — S5 evaluates N+1..M from the *held* accepted root N; `prev` is audit trail only and is never walked to decide anything |
| `nodes/<sha256>` `RevocationUnionV1` | `{unionSchema:1, version:n, lists:[{version,sha256}…], subjects:[{subjectKind, subject, firstVersion}…]}` sorted, de-duplicated | one file, product 4 MiB bound |

- **No issuer-side superset promise is assumed.** Accepting list v computes `union(prev.subjects, v.entries)`, writes a new union node, and the capsule's `heads.revocation` moves to it. A subject omitted by a newer list stays in the union: that is v14's "forget a revocation observation" prohibition made physical. The union is rewritten only when a list is accepted (rare), never on a clock tick.
- **Only `EV-RECOVER-COMMIT`'s named authorization may drop subjects** (e.g. keys of a replaced root) — it writes a union node whose `lists` starts a new epoch and records the recovery event seq; a generic list refresh can never shrink `subjects`. Whether recovery shrinks the union at all is an owner decision (**Q1**); the safe default is that it does not.
- **Fork/merge**: forward migration copies the three head references (documents are install-level, so nothing is copied). Ancestor re-selection takes, per head, the side with the **greater version**, and for revocation writes a **merged union node** `union(source.subjects, target.subjects)` with `version = max`. This also repairs a hole in today's law: `rollback_floors` sets `rootVersion = max(both)` while the retained target's accepted root is older — counters and heads would disagree; carrying the greater head keeps `heads.*.version == clock.*` true.
- **Bound refusal**: a union that would exceed 4 MiB cannot be written. Refusing the *list* would fail open against the new revocation, so the lawful direction is: the capsule is not advanced and **every role refuses new admission** (resource refusal, existing vocabulary) until an owner-defined compaction exists (**Q2**). State the number: at ~100 B/subject that is ≈40,000 retained subjects.
- The model's `migrate_floors` carries only the six `FLOOR_KEYS` + anchor + challenge; the 11-member record also requires `revocationIssuedAt`, `catalogExpiresAt`, `rootExpiresAt`. They are functions of the head documents, so they travel with the heads — but the current reference text never says so. **Gap to state in the owner.**

## 3. Audit before `EV-RECOVER-COMMIT` (decision 6)

**Existing ownership, checked first:** v14 `auditAndWaiver` defines the record — "Every ATTEMPTED event — including guard failure and fallback — appends `{role, from, to, event, outcome, refusalReason?, payloadDigests, clockObservation}`", plus `ceremonyTermination` for abort — and classes it "operational metadata as the live DR-124 row names that class. It is not sealed evidence." S4.5 names one more record ("audit record `RECOVERY-EPOCH`"). **No owner gives it a carrier.** So this is a missing placement, not a new framework: the records and vocabulary exist; only bytes-on-disk are undecided.

Proposal: `I/trust/stores/S/events/<seq>-<sha256>` = canonical `TrustAuditEventV1 = {auditSchema:1, storeInstanceId:S, seq:k, prev:hex64|null, record:{…exactly the v14 members…}}`, exclusive create, ≤ 4 KiB.
- **Order:** (1) write event k (fsync file + dir); (2) publish the capsule revision whose `eventHead = {k, sha256(event)}` and whose `roles` carry the transition. v14's "EV-RECOVER-COMMIT only after those records exist" is step 1 before step 2. There is one commit point — the capsule rename — and no cross-file atomicity is claimed.
- **No hash cycle:** the event references the *previous event* (`prev`), never a capsule; the capsule references the event. 
- **Orphans prove nothing:** an event file not reachable from the current `eventHead` is a *proposed* transition that did not become current (crash between 1 and 2, or a lost race under the fence). It is inert; a retry writes a new seq-k event with its own hash (exclusive create makes coexistence safe). Never scanned, never adopted.
- **Refused events** are attempted events: they append too, and move `eventHead` with `roles` unchanged. Consequence to accept knowingly: **every decision evaluation already rewrites the capsule** (v8 §4.2 write-ahead `evalHighWater`), and `EV-CLOCK` is an attempted event, so one small event file per evaluation. The chain is read for authority **only at its head**; retention/pruning of old operational metadata is an owner decision (**Q3**) and must never touch an event referenced by a `revokedBy`/`quorumLostBy`/`ceremony` seq.

## 4. Prepared trust-continuity companion (decision 3)

Beside the unchanged six-counter `floor-image.v1` in the carrier root (forward `stores/.staging/E/`, ancestor `transitions/stage/E/`): `trust-continuity.v1`, exclusive create, never replaced, **durable before the source fence** (same barrier as the image).
```
TrustContinuityV1 = { "continuitySchema":1, "executionId":E, "intentDigest":D, "case":"forward"|"ancestor",
  "source": { "storeInstanceId","storeGeneration","stateSchema" }, "target": { …same three… },
  "preFenceSourceCapsule": hex64,                       // sha256 of the source capsule bytes at preparation
  "carried": { "heads": {…}, "roles": { six × { "state","revokedBy","quorumLostBy","ceremony" } } } }
```
No member is added to the floor image or the journal; the public 20/11 records are untouched.
- **The stale-digest problem, solved without guessing:** fencing legitimately rewrites the source capsule (`roles` reset, `sourceFence`, `eventHead`), so a whole-capsule digest would false-refuse every resume. Rule by fence observation: `sourceFence` **old** ⇒ require `sha256(source capsule) == preFenceSourceCapsule` (nothing may have moved since preparation: STP forbids any S4 evaluation or floor write between image and fence); `sourceFence == {E,D}` ⇒ require the **continuity projection** of the source capsule — `{heads, roles[*].{revokedBy, quorumLostBy, ceremony}}`, i.e. exactly what fencing does not change — to equal `carried` minus `state`. Anything else ⇒ **unavailable** (missing, other E/D, other bindings) or, with an admitted matching binding and disagreeing content, the existing QUARANTINE row — the same split STP already makes for the floor image.
- **Forward:** the target capsule `I/trust/stores/S_t/state.v1` is created from `carried` + floors copied: each role `ST-REVOKED` stays `ST-REVOKED` with its `revokedBy`; every other role `ST-UNBOOTSTRAPPED`/`MIGRATED` with `quorumLostBy` carried; anchor and clock challenge null (unchanged law); `sourceFence:null`. It must be **complete and durable before carrier COMMITTED / jCOMMITTED / pair selection**; creation is idempotent (byte-identical ⇒ done, different ⇒ unavailable).
- **Ancestor:** republish the retained target capsule: floors per-field max (unchanged law); heads by greater version and merged union (§2); per role `revokedBy` = either side's (greater `revocationVersion`), `quorumLostBy` = either side's; state `ST-REVOKED` if either side is, else `ST-UNBOOTSTRAPPED`/`RESTORED`. Idempotent under retry, like the floor application, and never clears a restriction.
- **Projected-model changes (minimal):** `StoreTransitionObservationV1.floorEvidence` gains a sibling `continuityEvidence {companion, sourceProjection|sourceCapsuleDigest, targetPresent}` with a standing function shaped exactly like `floor_standing` (unavailable / matching / mismatching), consulted in the same two rows that require the image. No new action, no new table row, no new public code.

## 5. Ceremony in progress vs transitions (decision 4)

- **New Phase C store-changing transition**: refuse **before jLEASED or any effect** if any role of the source capsule — or, for an ancestor case, of the retained target capsule — is `ST-RECOVERY`. It is a precondition on host state; the existing class is request-rejected / `REQUEST.PRECONDITION_FAILED`. I found no existing `TRANSITION.*` detail that fits (list in `claude-out/io/`); choosing one or reusing `TRANSITION.REFUSED` is an owner call (**Q4**) — no new public vocabulary is needed either way.
- **Historical Phase B** follows admitted facts: a ceremony cannot have started after jLEASED (the fence is held for the whole transition), so a resumed transition never sees `ST-RECOVERY` it did not refuse at admission; if it does, the capsule changed outside the protocol ⇒ continuity mismatch ⇒ QUARANTINE, not a fresh trust decision.
- **Staged-but-not-begun inputs** (`ceremony.stagedPayload` with state ≠ `ST-RECOVERY`) are carried by the companion, not dropped — dropping would be a silent state change even though re-presenting is cheap. Dropping the *clock* challenge remains lawful and separate.
- **Same-store core updates** leave the capsule untouched, so no continuity companion and no blanket ceremony refusal; their trust gate is the existing S9 structural one (embedded chain reach / reader support, `ROOT.FLOOR_ABOVE_CORE`) plus ordinary S4 admission. One addition worth stating: a core whose readers cannot decode `capsuleSchema` must refuse typed rather than treat the store as uninitialised — the S9 reader-bridge pattern, applied to one more format axis.

## 6. Restore, and not deadlocking the source fence (decision 8)

Two different acts, which current text already separates (lineage `floorsAndAuthority`):
- **Evidence restore / portable adoption** ⇒ a **fresh S′** ("A newly materialized store receives its own fresh identity", "restores no trust floor", "never impersonates its source"). Its capsule is created new with `sourceFence:null`; if S′ is to become selected that is a forward transition from the currently selected store and §4 governs what it inherits. No attribution problem arises.
- **Declared trust restore of the same S** (v2 §5.5: SC-TRUST "backed up, if at all, as a separate SC-TRUST set"; "restore itself is the trigger"). **There is no existing authorized path**: the 45-command inventory has `trust-refresh`, `trust-import`, `trust-recovery-challenge`, `trust-recovery-import`, `trust-doctor` and no restore entry, and the "restore marker" v2 mentions has no defined mechanism. So this is a genuine missing owner (**Q5**), and nothing should be implemented as if it existed.
  When it is defined, the rule that avoids the deadlock I created in 206 (where I called a restored attribution *unavailable* — which, with corr.188's "unavailable stops unknown-custody", would make the store unfenceable forever): the restore is itself a fenced, authorized capsule **publication**, refused unless the **active transition slot is confirmed absent**; it publishes the restored content with the §0 standing reset (`RESTORED`), an audit event recording the restore, heads/union merged *upward* against the immutable documents still on disk (v2's "counters below any document still on disk" check becomes a merge, never a lowering), and `sourceFence` **as restored**. With no active slot, no execution can mistake that attribution for its own: any later transition carries a new E, observes an *old* fence, and lawfully supersedes it. Historical attribution stays honest — it says what the restored timeline said, and the audit event says when that timeline was reinstated.

## 7. What this closes, and what remains for root
Closed by proposal: R2 (§0, §4), R3 (§2), R4 (§3), R5 (`quorumLostBy` evidence = the accepted observation's event seq; the event record already carries `payloadDigests`/`clockObservation`), R6 (§1 fixed map), R7 (§1 no persisted flag). R1 (pin v14 + v2 clauses in the candidate) is untouched and is a prerequisite for freezing any of this.
Owner decisions: **Q1** may `EV-RECOVER-COMMIT` shrink the revocation union; **Q2** union over-bound behaviour/compaction; **Q3** audit-event retention; **Q4** refusal detail for ceremony-in-progress; **Q5** the declared trust-restore path and its marker; **Q6** whether `RESTORED` reset should also preserve `ST-RECOVERY` when a *restore* (not a transition) meets an in-progress ceremony — I would refuse the restore, by symmetry with §5.
Contradictions with precise existing law, restated: (i) §0 — v14 `ST-UNBOOTSTRAPPED` semantics vs "marks every role" resets; (ii) §2 — `rollback_floors` max counters vs the target's older accepted documents; (iii) §2 — `migrate_floors` omits three required record members; (iv) §3 — audit records are mandated with no carrier; (v) §6 — restore is mandated fail-closed with no authorized path.

## 8. Limits
Owner-text proposal; no model or product code written or run; bounds are estimates except those inherited from existing parsers. v14's `honestyRepairs*`, fixture classes and `g06/g08` sections and the v2 schemas were not read. This is assistance for root to reconcile, author and freeze; I will review the frozen bytes independently and nothing here is acceptance of them.
